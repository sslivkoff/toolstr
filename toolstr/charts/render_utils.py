from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import numpy as np

import toolstr

from .. import spec
from . import char_dicts
from . import grid_utils


def array_to_tuple(
    array: typing.Sequence[typing.Any],
) -> typing.Tuple[typing.Tuple[typing.Any, ...], ...]:
    return tuple(tuple(row) for row in array)


def render_supergrid(
    array: np.typing.NDArray,  # type: ignore
    rows_per_cell: int | None = None,
    columns_per_cell: int | None = None,
    char_dict: spec.GridCharDict | None = None,
    sample_mode: spec.SampleMode | None = None,
    color_grid: np.typing.NDArray | None = None,  # type: ignore
    color_map: typing.Mapping[int, str] | None = None,
) -> str:

    if rows_per_cell is None or columns_per_cell is None or char_dict is None:
        rows_per_cell, columns_per_cell = spec.sample_mode_size[sample_mode]
        char_dict = char_dicts.get_char_dict(sample_mode)

    import numpy as np

    array = array[::-1]
    rows, columns = array.shape
    super_rows = rows / rows_per_cell
    super_columns = columns / columns_per_cell

    new_rows = []
    super_rows = np.vsplit(array, super_rows)
    for sr, super_row in enumerate(super_rows):
        new_row = []
        super_cells: np.typing.NDArray = np.hsplit(super_row, super_columns)  # type: ignore
        for sc, super_cell in enumerate(super_cells):

            # get char
            as_tuple = array_to_tuple(super_cell)
            char_str = char_dict[as_tuple]

            # get color
            if color_grid is not None and char_str not in [' ', '⠀']:
                color = color_map[color_grid[sr, sc]]  # type: ignore
                char_str = '[' + color + ']' + char_str + '[/' + color + ']'

            new_row.append(char_str)

        new_rows.append(''.join(new_row))

    return '\n'.join(new_rows)


def render_y_axis(
    grid: spec.Grid,
    width: int = 8,
    n_ticks: int = 4,
    tick_length: int = 2,
    label_gap: int = 0,
) -> str:

    import numpy as np

    tick_indices = (
        np.linspace(0, grid['n_rows'] - 1, n_ticks).round().astype(int)  # type: ignore
    )

    label_width = width - (label_gap + tick_length)
    rows = []
    for r in range(grid['n_rows']):

        row_center = grid_utils.get_row_center(row=r, grid=grid)
        if abs(row_center) < 1e-10:
            row_center = 0

        label = toolstr.format(row_center, order_of_magnitude=True)
        label = label[:label_width]
        label = label.rjust(label_width)

        if r == 0:
            tick = '┘'
            tick_body = '╶'
        elif r + 1 == grid['n_rows']:
            tick = '┐'
            tick_body = '╶'
        elif r in tick_indices:
            tick = '┤'
            tick_body = '╶'
        else:
            tick = '│'
            tick_body = ' '
            label = ' ' * label_width

        row = label + ' ' * label_gap + tick_body * (tick_length - 1) + tick
        rows.append(row)

    rows = rows[::-1]

    return '\n'.join(rows)


def render_x_axis(
    grid: spec.Grid,
    n_ticks: int = 3,
    tick_length: int = 2,
    include_label_gap: bool = False,
    formatter: typing.Callable[[typing.Any], str] | None = None,
) -> str:

    import numpy as np

    tick_indices: np.NDArray = (  # type: ignore
        np.linspace(0, grid['n_columns'] - 1, n_ticks).round().astype(int)
    )

    rows = []

    # tick row
    if n_ticks == 0:
        rows.append('─' * grid['n_columns'])
    elif n_ticks == 1:
        raise Exception()
    else:

        gaps = tick_indices[1:] - tick_indices[:-1]
        tick_row = ['┌']
        for g, gap in enumerate(gaps - 1):
            tick_row.extend('─' * gap)
            if g + 1 == len(gaps):
                continue
            tick_row.append('┬')
        tick_row.append('┐')
        rows.append(''.join(tick_row))

    # tick length rows
    if tick_length <= 0:
        raise NotImplementedError()
    elif tick_length == 1:
        pass
    else:
        tick_length_row = rows[-1]
        tick_length_row = tick_length_row.replace('─', ' ')
        tick_length_row = tick_length_row.replace('┌', '╵')
        tick_length_row = tick_length_row.replace('┬', '╵')
        tick_length_row = tick_length_row.replace('┐', '╵')
        for i in range(tick_length - 1):
            rows.append(tick_length_row)

    # label gap
    if include_label_gap:
        rows.append('')

    if formatter is None:
        import functools

        formatter = functools.partial(toolstr.format, order_of_magnitude=True)

    # label row
    labels = ' ' * grid['n_columns']
    xmin_label = formatter(grid['xmin'])
    xmax_label = formatter(grid['xmax'])
    labels = xmin_label + labels[len(xmin_label) :]
    labels = labels[: -len(xmax_label)] + xmax_label
    if n_ticks > 2:
        for tick_index in tick_indices[1:-1]:
            column_center = grid_utils.get_column_center(tick_index, grid)
            label = formatter(column_center)
            label_start = 1 + tick_index - int(np.ceil(len(label) / 2))
            labels = (
                labels[:label_start]
                + label
                + labels[label_start + len(label) :]
            )

    rows.append(labels)

    return '\n'.join(rows)
