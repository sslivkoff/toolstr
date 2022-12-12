from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import numpy as np

import toolstr

from .. import formats
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
    char_dict: spec.GridCharDict | spec.SampleMode | None = None,
    color_grid: np.typing.NDArray | None = None,  # type: ignore
    color_map: typing.Mapping[int, str] | None = None,
) -> str:

    import numpy as np

    # determine chart dict and related parameters
    if char_dict is None:
        char_dict = 'whole'
    if isinstance(char_dict, str):
        char_dict = char_dicts.get_char_dict(char_dict)
    if rows_per_cell is None or columns_per_cell is None:
        single_char_index = next(iter(char_dict.keys()))
        rows_per_cell = len(single_char_index)
        columns_per_cell = len(single_char_index[0])

    array = array[::-1]
    rows, columns = array.shape
    super_rows = rows / rows_per_cell
    super_columns = columns / columns_per_cell

    new_rows = []
    super_rows = np.vsplit(array, super_rows)  # type: ignore
    for sr, super_row in enumerate(super_rows):  # type: ignore
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
    chrome_style: str | None = None,
    tick_label_style: str | None = None,
    tick_label_format: spec.NumberFormat | None = None,
    tick_label_oom: bool = True,
) -> str:

    import numpy as np

    tick_indices = (
        np.linspace(0, grid['n_rows'] - 1, n_ticks).round().astype(int)
    )

    if tick_label_format is None:
        tick_label_format = {}

    label_width = width - (label_gap + tick_length)
    rows = []
    for r in range(grid['n_rows']):

        row_center = grid_utils.get_row_center(row=r, grid=grid)
        if abs(row_center) < 1e-10:
            row_center = 0

        row_format: spec.NumberFormat = dict(tick_label_format)  # type: ignore
        if tick_label_oom and 'order_of_magnitude' not in row_format:
            if row_center < 0.01:
                order_of_magnitude = False
                scientific = True
            elif row_center < 1000:
                order_of_magnitude = False
                scientific = False
            else:
                order_of_magnitude = True
                scientific = False
            row_format['order_of_magnitude'] = order_of_magnitude
            row_format['scientific'] = scientific
        if 'decimals' not in row_format:
            if row_format.get('scientific'):
                row_format['decimals'] = 1
            elif row_center < 1000:
                row_format['decimals'] = 3
            else:
                row_format['decimals'] = 1

        row_format.setdefault('trailing_zeros', True)

        label = toolstr.format(
            row_center,
            **row_format
        )
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

        if tick_label_style is not None:
            label = formats.add_style(label, tick_label_style)
        tick_form = tick_body * (tick_length - 1) + tick
        if chrome_style is not None:
            tick_form = formats.add_style(tick_form, chrome_style)
        row = label + ' ' * label_gap + tick_form
        rows.append(row)

    rows = rows[::-1]

    return '\n'.join(rows)


def render_x_axis(
    grid: spec.Grid,
    n_ticks: int = 3,
    tick_length: int = 2,
    include_label_gap: bool = False,
    formatter: typing.Callable[[typing.Any], str] | None = None,
    chrome_style: str | None = None,
    tick_label_style: str | None = None,
    tick_label_format: str | None = 'date',
) -> str:

    import numpy as np

    if formatter is None:
        if tick_label_format == 'date':
            import functools

            formatter = functools.partial(
                formats.format_timestamp,
                representation='TimestampDate',
            )
        elif tick_label_format == 'age':
            import tooltime

            def formatter(xval: tooltime.Timestamp) -> str:
                phrase = tooltime.get_age(xval, 'TimelengthPhrase')
                return phrase.split(', ')[0]

        elif tick_label_format == 'iso':
            import functools

            formatter = functools.partial(
                formats.format_timestamp,
                representation='TimestampISOPretty',
            )

        elif tick_label_format is None:

            def formatter(xval: tooltime.Timestamp) -> str:
                return toolstr.format(xval)

        else:
            raise Exception('invalid value for tick_label_format')

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

    if chrome_style is not None:
        rows = [formats.add_style(row, chrome_style) for row in rows]
    if tick_label_style is not None:
        labels = formats.add_style(labels, tick_label_style)

    rows.append(labels)

    return '\n'.join(rows)
