from __future__ import annotations

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


class Grid(TypedDict):
    n_rows: int
    n_columns: int
    xmin: typing.Union[int, float]
    xmax: typing.Union[int, float]
    ymin: typing.Union[int, float]
    ymax: typing.Union[int, float]


Numeric = typing.Union[int, float]


def to_numeric_type(value: typing.SupportsFloat) -> typing.Union[int, float]:

    # python3.7 compatibility
    # supports_int = isinstance(value, typing.SupportsInt)
    supports_int = hasattr(value, '__int__')

    if supports_int and type(value).__name__.startswith('int'):
        return int(value)  # type: ignore
    else:
        return float(value)

