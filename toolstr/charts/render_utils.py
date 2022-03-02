import toolstr

# from . import chart_dicts
from . import grid_utils


def array_to_tuple(array):
    return tuple(tuple(row) for row in array)


def render_supergrid(array, rows_per_cell, columns_per_cell, char_dict):
    import numpy as np

    array = array[::-1]
    rows, columns = array.shape
    super_rows = rows / rows_per_cell
    super_columns = columns / columns_per_cell

    new_rows = []
    for super_row in np.vsplit(array, super_rows):
        new_row = []
        for super_cell in np.hsplit(super_row, super_columns):
            as_tuple = array_to_tuple(super_cell)
            new_row.append(char_dict[as_tuple])

        new_row = ''.join(new_row)
        new_rows.append(new_row)

    return '\n'.join(new_rows)


def render_y_axis(grid, width=8, n_ticks=4, tick_length=2, label_gap=0):

    import numpy as np

    tick_indices = (
        np.linspace(0, grid['n_rows'] - 1, n_ticks).round().astype(int)
    )

    label_width = width - (label_gap + tick_length)
    rows = []
    for r in range(grid['n_rows']):

        row_center = grid_utils.get_row_center(row=r, grid=grid)
        if abs(row_center) < 1e-14:
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


def render_x_axis(grid, n_ticks=3, tick_length=2, include_label_gap=False):

    import numpy as np

    tick_indices = (
        np.linspace(0, grid['n_columns'] - 1, n_ticks).round().astype(int)
    )

    rows = []

    # tick row
    if n_ticks == 0:
        tick_row = '─' * grid['n_columns']
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
    tick_row = ''.join(tick_row)
    rows.append(tick_row)

    # tick length rows
    if tick_length <= 0:
        raise NotImplementedError()
    elif tick_length == 1:
        pass
    else:
        tick_length_row = tick_row
        tick_length_row = tick_length_row.replace('─', ' ')
        tick_length_row = tick_length_row.replace('┌', '╵')
        tick_length_row = tick_length_row.replace('┬', '╵')
        tick_length_row = tick_length_row.replace('┐', '╵')
        for i in range(tick_length - 1):
            rows.append(tick_length_row)

    # label gap
    if include_label_gap:
        rows.append('')

    # label row
    labels = ' ' * grid['n_columns']
    xmin_label = toolstr.format(grid['xmin'], order_of_magnitude=True)
    xmax_label = toolstr.format(grid['xmax'], order_of_magnitude=True)
    labels = xmin_label + labels[len(xmin_label) :]
    labels = labels[: -len(xmax_label)] + xmax_label
    if n_ticks > 2:
        for tick_index in tick_indices[1:-1]:
            column_center = grid_utils.get_column_center(tick_index, grid)
            label = toolstr.format(column_center, order_of_magnitude=True)
            label_start = 1 + tick_index - int(np.ceil(len(label) / 2))
            labels = (
                labels[:label_start]
                + label
                + labels[label_start + len(label) :]
            )

    rows.append(labels)

    return '\n'.join(rows)

