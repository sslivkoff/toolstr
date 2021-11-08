import tooltime


def format(value, format_type=None, **kwargs):

    if format_type is None:
        number_types = (
            'int',
            'float',
            'int16',
            'int32',
            'int64',
            'float16',
            'float32',
            'float64',
        )
        if type(value).__name__ in number_types:
            format_type = 'number'

    if format_type == 'number':
        return format_number(value, **kwargs)
    elif format_type == 'timestamp':
        return tooltime.create_timestamp(value, **kwargs)
    else:
        raise Exception('unknown format_type: ' + str(format_type))


def format_number(
    value,
    percentage=False,
    scientific=None,
    signed=False,
    commas=True,
    decimals=None,
    nonfractional_decimals=None,
    fractional_decimals=None,
    trailing_zeros=False,
    prefix=None,
    postfix=None,
):
    """
    TODO:
    - sigfigs
    - signed
    """

    # determine default formatting
    if percentage:
        value = value * 100
        scientific = False
    if scientific is None and abs(value) < 0.0001 and value != 0:
        scientific = True
    if decimals is None:
        if abs(value) >= 1:
            if nonfractional_decimals is None:
                nonfractional_decimals = 2
            decimals = nonfractional_decimals
        if abs(value) < 1:
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
    else:
        format_str = '{:,.' + str(decimals) + 'f}'

    # remove commas
    if not commas:
        format_str = format_str.replace(',', '')

    # add sign
    if signed:
        format_str = format_str.replace(':', ':+')

    # format
    formatted = format_str.format(value)

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


def format_change(from_value=None, to_value=None, series=None, **format_kwargs):
    if from_value is None and to_value is None:
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
        + ' ' + arrow + ' '
        + format(to_value, **format_kwargs)
        + ' (' + percent_change + ')'
    )

