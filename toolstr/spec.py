import typing


def to_numeric(value: typing.SupportsFloat) -> typing.Union[int, float]:
    if isinstance(value, typing.SupportsInt) and type(
        value
    ).__name__.startswith('int'):
        return int(value)
    else:
        return float(value)

