import math

from . import grid_utils


def create_blank_raster(grid, container_format='array', cell_format=int):

    if container_format == 'array':
        import numpy as np

        if cell_format == int:
            return np.zeros((grid['n_rows'], grid['n_columns']), dtype=int)
        elif cell_format is str:
            return np.zeros((grid['n_rows'], grid['n_columns']), dtype='<U1')
        else:
            raise Exception('unknown cell format: ' + str(cell_format))

    elif container_format == 'list_of_rows':
        if cell_format is int:
            cell = 0
        elif cell_format is str:
            cell = ' '
        else:
            raise Exception('unknown cell format: ' + str(cell_format))

        return [[[cell] * grid['n_columns']] for row in grid['n_rows']]

    elif container_format == 'list_of_columns':
        if cell_format is int:
            cell = 0
        elif cell_format is str:
            cell = ' '
        else:
            raise Exception('unknown cell format: ' + str(cell_format))

        return [[[cell] * grid['n_rows']] for row in grid['n_columns']]

    else:
        raise Exception('unknown container_format: ' + str(container_format))


def rasterize_by_column(yvals, grid):
    import numpy as np

    assert len(yvals) == grid['n_columns']

    row_borders = grid_utils.get_row_borders(grid)
    raster = create_blank_raster(grid)
    for column, yval in enumerate(yvals):
        row = np.searchsorted(row_borders, yval) - 1
        if 0 <= row and row < grid['n_rows']:
            raster[row, column] = 1

    return raster


def rasterize_by_lines(yvals, grid):
    import skimage.draw

    assert len(yvals) == grid['n_columns']

    raster = create_blank_raster(grid)
    for column, yval in enumerate(yvals[:-1]):
        row = grid_utils.get_row(yval, grid)
        row_next = grid_utils.get_row(yvals[column + 1], grid)

        rows, columns = skimage.draw.line(
            row,
            column,
            row_next,
            column + 1,
        )
        mask = (rows >= 0) * (columns >= 0)
        rows = rows[mask]
        columns = columns[mask]
        raster[rows, columns] = 1

    return raster


candlestick_color_map = {
    0: '#e15241',
    1: '#4eaf0a',
}


def add_column_line(column, from_row, to_row, raster):
    min_row = min(from_row, to_row)
    max_row = max(from_row, to_row)

    if min_row < 0:
        min_row = 0
    if min_row >= raster.shape[1]:
        min_row = raster.shape[1] - 1

    if max_row < 0:
        max_row = 0
    if max_row >= raster.shape[1]:
        max_row = raster.shape[1] - 1

    raster[min_row : (max_row + 1), column] = 1


def raster_candlesticks(ohlc, sample_grid, render_grid, justify='left'):
    raster = create_blank_raster(sample_grid)
    color_grid = create_blank_raster(render_grid)
    n_render_lines = min(len(ohlc), math.floor(render_grid['n_columns'] / 2))
    for c in range(n_render_lines):
        open_row = grid_utils.get_row(yval=ohlc[c][0], grid=sample_grid)
        high_row = grid_utils.get_row(yval=ohlc[c][1], grid=sample_grid)
        low_row = grid_utils.get_row(yval=ohlc[c][2], grid=sample_grid)
        close_row = grid_utils.get_row(yval=ohlc[c][3], grid=sample_grid)

        if justify == 'left':
            first_column = c * 4
        elif justify == 'right':
            first_column = c * 4 + 1
        else:
            raise Exception('unknown justification: ' + str(justify))

        wick_column = first_column + 1
        last_column = first_column + 2

        # candle body
        add_column_line(
            from_row=open_row,
            to_row=close_row,
            column=first_column,
            raster=raster,
        )
        add_column_line(
            from_row=open_row,
            to_row=close_row,
            column=last_column,
            raster=raster,
        )

        # candle wick
        add_column_line(
            from_row=low_row,
            to_row=high_row,
            column=wick_column,
            raster=raster,
        )

        if ohlc[c][0] >= ohlc[c][3]:
            color_grid[:, 2 * c : 2 * c + 2] = 0
        else:
            color_grid[:, 2 * c : 2 * c + 2] = 1

    return {
        'raster': raster,
        'color_grid': color_grid,
    }


def raster_bar_chart(values, grid, bar_width, bar_gap, start_gap=0):
    raster = create_blank_raster(grid)

    for v, value in enumerate(values):

        from_row = grid_utils.get_row(yval=0, grid=grid)
        from_row = 1
        to_row = grid_utils.get_row(yval=value, grid=grid)
        to_row = max(1, to_row)
        first_column = start_gap + v * (bar_width + bar_gap)
        last_column = first_column + bar_width

        for column in range(first_column, last_column):
            add_column_line(
                from_row=from_row,
                to_row=to_row,
                column=column,
                raster=raster,
            )

    return raster

