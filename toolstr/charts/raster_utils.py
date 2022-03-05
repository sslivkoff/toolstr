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

