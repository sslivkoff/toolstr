import typing
from typing_extensions import Literal, TypedDict


HorizontalJustification = Literal['left', 'right', 'center']


class BorderCharSet(TypedDict):
    horizontal: str
    vertical: str
    upper_left: str
    upper_right: str
    lower_left: str
    lower_right: str


Numeric = typing.Union[int, float]


def to_numeric(value: typing.SupportsFloat) -> typing.Union[int, float]:

    # python3.7 compatibility
    # supports_int = isinstance(value, typing.SupportsInt)
    supports_int = hasattr(value, '__int__')

    if supports_int and type(value).__name__.startswith('int'):
        return int(value)  # type: ignore
    else:
        return float(value)

