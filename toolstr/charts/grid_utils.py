from __future__ import annotations

import typing

from toolstr import spec

if typing.TYPE_CHECKING:
    import numpy

    NumpyArray = numpy.typing.NDArray


def get_row_borders(grid: spec.Grid) -> NumpyArray:
    import numpy as np

    return np.linspace(grid['ymin'], grid['ymax'], grid['n_rows'] + 1)


def get_column_borders(grid: spec.Grid) -> NumpyArray:
    import numpy as np

    return np.linspace(grid['xmin'], grid['xmax'], grid['n_columns'] + 1)


def get_row_centers(grid: spec.Grid) -> NumpyArray:
    row_borders = get_row_borders(grid)
    return (row_borders[1:] + row_borders[:-1]) / 2


def get_column_centers(grid: spec.Grid) -> NumpyArray:
    column_borders = get_column_borders(grid)
    return (column_borders[1:] + column_borders[:-1]) / 2


def get_row_delta(grid: spec.Grid) -> typing.Union[int, float]:
    return (grid['ymax'] - grid['ymin']) / grid['n_rows']


def get_column_delta(grid: spec.Grid):
    return (grid['xmax'] - grid['xmin']) / grid['n_columns']


def get_cell_borders(row: int, column: int, grid: spec.Grid):
    row_delta = get_row_delta(grid)
    column_delta = get_column_delta(grid)
    return (
        grid['xmin'] + column_delta * column,
        grid['xmin'] + column_delta * (column + 1),
        grid['ymin'] + row_delta * row,
        grid['ymin'] + row_delta * (row + 1),
    )


def get_row_center(row: int, grid: spec.Grid):
    row_delta = get_row_delta(grid)
    return grid['ymin'] + row_delta / 2.0 + row_delta * row


def get_column_center(column: int, grid: spec.Grid):
    column_delta = get_column_delta(grid)
    return grid['xmin'] + column_delta / 2.0 + column_delta * column


def get_row(
    yval: typing.Union[typing.SupportsInt, typing.SupportsFloat],
    grid: spec.Grid,
) -> int:
    row_borders = get_row_borders(grid)
    if yval < row_borders[0]:
        return -1
    elif yval > row_borders[-1]:
        return grid['n_rows']
    else:
        import numpy as np

        return np.searchsorted(row_borders, yval) - 1

