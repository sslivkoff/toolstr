import typing


HorizontalJustification = typing.Literal['left', 'right', 'center']


class BorderCharSet(typing.TypedDict):
    horizontal: str
    vertical: str
    upper_left: str
    upper_right: str
    lower_left: str
    lower_right: str


Numeric = typing.Union[int, float]


def to_numeric(value: typing.SupportsFloat) -> typing.Union[int, float]:
    if isinstance(value, typing.SupportsInt) and type(
        value
    ).__name__.startswith('int'):
        return int(value)
    else:
        return float(value)

