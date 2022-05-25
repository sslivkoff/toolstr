from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import tooltime

from . import spec


def hjustify(
    text: str,
    justification: spec.HorizontalJustification,
    width: int,
) -> str:

    if width < len(text):
        return text[:width]

    if justification == 'left':
        return text.ljust(width)
    elif justification == 'right':
        return text.rjust(width)
    elif justification == 'center':
        return text.center(width)
    else:
        raise Exception('unknown justification: ' + str(justification))


def vjustify(
    text: str,
    justification: spec.VerticalJustification,
    height: int,
) -> str:

    n_lines = text.count('\n') + 1

    # check if exceeds height
    if n_lines > height:
        return '\n'.join(text.split('\n')[:height])

    missing = height - n_lines
    if justification == 'top':
        return text + '\n' * missing
    elif justification == 'bottom':
        return '\n' * missing + text
    elif justification == 'center':
        top = int(missing / 2)
        bottom = missing - top
        return '\n' * top + text + '\n' * bottom
    else:
        raise Exception('unknown justification: ' + str(justification))


def format(
    value: typing.Any,
    format_type: typing.Literal['number', 'timestamp'] | None = None,
    **kwargs: typing.Any,
) -> str:

    if format_type is None:

        if isinstance(value, bool):
            return str(value)

        # python3.7 compatibility
        # supports_int = isinstance(value, typing.SupportsFloat)
        supports_int = hasattr(value, '__int__')

        if supports_int:
            format_type = 'number'

    if format_type == 'number':
        return format_number(value, **kwargs)
    elif format_type == 'timestamp':
        return format_timestamp(value, **kwargs)
    else:
        raise Exception('unknown format_type: ' + str(format_type))


def format_nbytes(
    nbytes: int | float,
    decimals: int = 2,
    commas: bool = False,
    **format_kwargs: typing.Any,
) -> str:
    if not isinstance(nbytes, int):
        raise Exception('input must be integer')
    elif nbytes < 0:
        raise Exception('input must be non-negative')
    elif nbytes == 0:
        return '0B'
    else:
        prefixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
        divisions = 0
        while nbytes >= 1024:
            nbytes = nbytes / 1024
            divisions = divisions + 1
            if divisions + 1 >= len(prefixes):
                break
        number_str = format_number(
            nbytes,
            decimals=decimals,
            commas=commas,
            **format_kwargs,
        )
        return number_str + prefixes[divisions]


def format_timestamp(
    timestamp: tooltime.Timestamp,
    representation: tooltime.TimestampExtendedRepresentation = 'TimestampISO',
    **kwargs: typing.Any,
) -> str:
    import tooltime

    converted: typing.Any = tooltime.convert_timestamp(
        timestamp,
        to_representation=representation,  # type: ignore
        **kwargs,
    )
    if isinstance(converted, str):
        return converted
    else:
        return str(converted)


def format_number(
    value: typing.SupportsFloat,
    percentage: bool = False,
    scientific: typing.Optional[bool] = None,
    signed: bool = False,
    commas: bool = True,
    decimals: typing.Optional[int] = None,
    nonfractional_decimals: typing.Optional[int] = None,
    fractional_decimals: typing.Optional[int] = None,
    trailing_zeros: bool = False,
    prefix: typing.Optional[str] = None,
    postfix: typing.Optional[str] = None,
    order_of_magnitude: bool = False,
    oom_blank: str = '',
) -> str:
    """
    TODO:
    - sigfigs
    - signed
    """

    if order_of_magnitude:
        value, new_postfix = _get_order_of_magnitude(value, oom_blank)
        if postfix is None:
            postfix = new_postfix
        else:
            postfix = postfix = new_postfix

    # determine default formatting
    numeric = spec.to_numeric_type(value)
    if percentage:
        numeric = numeric * 100
        scientific = False
    if scientific is None and abs(numeric) < 0.0001 and numeric != 0:
        scientific = True
    if decimals is None:
        if abs(numeric) >= 1:
            if isinstance(value, int):
                nonfractional_decimals = 0
                decimals = 0
            else:
                if nonfractional_decimals is None:
                    nonfractional_decimals = 2
                decimals = nonfractional_decimals
        if abs(numeric) < 1:
            if fractional_decimals is None:
                if scientific:
                    fractional_decimals = 3
                else:
                    fractional_decimals = 6
            decimals = fractional_decimals

    if scientific:
        format_str = '{:,.' + str(decimals) + 'e}'
    elif decimals == 0:
        format_str = '{:,d}'
        if not isinstance(numeric, int):
            numeric = round(numeric)
    else:
        format_str = '{:,.' + str(decimals) + 'f}'

    # remove commas
    if not commas:
        format_str = format_str.replace(',', '')

    # add sign
    if signed:
        format_str = format_str.replace(':', ':+')

    # format
    formatted = format_str.format(numeric)

    # remove trailing zeros
    if trailing_zeros is not None and not trailing_zeros:
        if '.' in formatted:
            formatted = formatted.rstrip('0')
            if formatted[-1] == '.':
                formatted = formatted[:-1]

        if scientific:
            significand, mantissa = formatted.split('e')
            significand = significand.rstrip('0')
            if significand[-1] == '.':
                significand = significand[:-1]
            formatted = significand + 'e' + mantissa

    # add percentage sign
    if percentage:
        formatted += '%'

    # add prefix and postfix
    if prefix is not None:
        formatted = prefix + formatted
    if postfix is not None:
        formatted = formatted + postfix

    return formatted


def format_change(
    from_value: typing.Optional[spec.Numeric] = None,
    to_value: typing.Optional[spec.Numeric] = None,
    series: typing.Optional[typing.Sequence[spec.Numeric]] = None,
    **format_kwargs: typing.Any,
) -> str:
    if from_value is None or to_value is None:
        if series is None:
            raise Exception(
                'must specify either series, or from_value and to_value'
            )
        from_value = series[0]
        to_value = series[-1]

    # arrow = '→'
    arrow = '⟶'
    percent_change = format(
        to_value / from_value - 1,
        percentage=True,
        signed=True,
    )
    return (
        format(from_value, **format_kwargs)
        + ' '
        + arrow
        + ' '
        + format(to_value, **format_kwargs)
        + ' ('
        + percent_change
        + ')'
    )


def _get_order_of_magnitude(
    value: typing.SupportsFloat,
    oom_blank: str = '',
) -> tuple[typing.Union[int, float], str]:
    value = spec.to_numeric_type(value)
    abs_value = abs(value)
    if abs_value >= 1e18:
        raise NotImplementedError('value too big')
    elif abs_value >= 1e15:
        return value / 1e15, 'Q'
    elif abs_value >= 1e12:
        return value / 1e12, 'T'
    elif abs_value >= 1e9:
        return value / 1e9, 'B'
    elif abs_value >= 1e6:
        return value / 1e6, 'M'
    elif abs_value >= 1e3:
        return value / 1e3, 'K'
    else:
        return value, oom_blank
