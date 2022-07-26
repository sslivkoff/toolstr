from __future__ import annotations

import functools
import typing

from .. import blocks
from .. import formats
from .. import indents
from . import char_dicts
from . import grid_utils
from . import raster_utils
from . import render_utils


rows_per_cell = 4
columns_per_cell = 2
char_dict = char_dicts.get_braille_dict()


def render_line_plot(
    xvals: typing.Sequence[int | float],
    yvals: typing.Sequence[int | float],
    n_rows: int,
    n_columns: int,
) -> str:

    non_none_xvals = [xval for xval in xvals if xval is not None]
    non_none_yvals = [yval for yval in yvals if yval is not None]

    xmin = min(non_none_xvals)
    xmax = max(non_none_xvals)
    xrange = xmax - xmin

    ymin = min(non_none_yvals)
    ymax = max(non_none_yvals)
    yrange = ymax - ymin

    grid = grid_utils.create_grid(
        n_rows=n_rows,
        n_columns=n_columns,
        xmin=xmin - 0.0 * xrange,
        xmax=xmax + 0.0 * xrange,
        ymin=0,
        ymax=ymax + 0.1 * yrange,
    )

    render_grid = grid_utils.create_grid(
        n_rows=int(n_rows / rows_per_cell),
        n_columns=int(n_columns / columns_per_cell),
        xmin=xmin - 0.0 * xrange,
        xmax=xmax + 0.0 * xrange,
        ymin=0,
        ymax=ymax + 0.1 * yrange,
    )

    raster = raster_utils.rasterize_line_plot(
        xvals=xvals,
        yvals=yvals,
        grid=grid,
    )

    plot = render_utils.render_supergrid(
        array=raster,
        rows_per_cell=rows_per_cell,
        columns_per_cell=columns_per_cell,
        char_dict=char_dict,
    )

    y_axis = render_utils.render_y_axis(
        grid=render_grid,
    )

    y_axis_width = len(y_axis.split('\n')[0])
    graph = blocks.concatenate_blocks([y_axis, plot])

    formatter = functools.partial(
        formats.format_timestamp,
        representation='TimestampDate',
    )
    x_axis = render_utils.render_x_axis(
        grid=render_grid,
        formatter=formatter,
    )
    x_axis = indents.indent_block(x_axis, indent=y_axis_width)

    return graph + '\n' + x_axis


def print_line_plot(
    xvals: typing.Sequence[int | float],
    yvals: typing.Sequence[int | float],
    n_rows: int,
    n_columns: int,
) -> None:
    plot = render_line_plot(
        xvals=xvals,
        yvals=yvals,
        n_rows=n_rows,
        n_columns=n_columns,
    )
    print(plot)
