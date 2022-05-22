from __future__ import annotations

import typing
from typing_extensions import Literal, TypedDict

if typing.TYPE_CHECKING:

    import numpy.typing

    class NumberFormat(TypedDict, total=False):
        percentage: bool
        scientific: bool | None
        signed: bool
        commas: bool
        decimals: int | None
        nonfractional_decimals: int | None
        fractional_decimals: int | None
        trailing_zeros: bool
        prefix: str | None
        postfix: str | None
        order_of_magnitude: bool
        oom_blank: str


HorizontalJustification = Literal['left', 'right', 'center']
VerticalJustification = Literal['top', 'bottom', 'center']


class BorderChars(TypedDict):
    horizontal: str
    vertical: str
    upper_left: str
    upper_right: str
    lower_left: str
    lower_right: str
    cross: str
    upper_t: str
    lower_t: str
    left_t: str
    right_t: str


BorderCharName = Literal[
    'horizontal',
    'vertical',
    'upper_left',
    'upper_right',
    'lower_left',
    'lower_right',
    'cross',
    'upper_t',
    'lower_t',
    'left_t',
    'right_t',
]


SampleMode = Literal[
    None,
    'height_split',
    'width_split',
    'quadrants',
    'braille',
]

# (rows, columns)
sample_mode_size = {
    None: (1, 1),
    'height_split': (8, 1),
    'width_split': (1, 8),
    'quadrants': (2, 2),
    'braille': (4, 2),
}

GridCharDict = dict[tuple[tuple[int, ...], ...], str]


class Grid(TypedDict):
    n_rows: int
    n_columns: int
    xmin: typing.Union[int, float]
    xmax: typing.Union[int, float]
    ymin: typing.Union[int, float]
    ymax: typing.Union[int, float]


# Raster = typing.Union[
#     list[list[list[int | str]]],
#     numpy.typing.ndarray[typing.Any, numpy.dtype],
# ]
# Raster = numpy.typing.ndarray[typing.Any, numpy.dtype],
Raster = typing.Any


Numeric = typing.Union[int, float]


def to_numeric_type(value: typing.SupportsFloat) -> typing.Union[int, float]:

    # python3.7 compatibility
    # supports_int = isinstance(value, typing.SupportsInt)
    supports_int = hasattr(value, '__int__')

    if supports_int and type(value).__name__.startswith('int'):
        return int(value)  # type: ignore
    else:
        return float(value)
