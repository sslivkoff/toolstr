from __future__ import annotations

import typing

from .. import formats
from .. import spec
from . import char_dicts
from . import grid_utils
from . import raster_utils
from . import render_utils


def render_line_plot(
    xvals: typing.Sequence[int | float],
    yvals: typing.Sequence[int | float],
    n_rows: int,
    n_columns: int,
    line_style: str | None = None,
    chrome_style: str | None = None,
    tick_label_style: str | None = None,
    xaxis_kwargs: typing.Mapping[typing.Any, typing.Any] | None = None,
    yaxis_kwargs: typing.Mapping[typing.Any, typing.Any] | None = None,
    char_dict: spec.SampleMode | spec.GridCharDict | None = None,
    y_axis_width: int = 9,
) -> str:

    import numpy as np

    # determine char dict
    if char_dict is None:
        char_dict = 'braille'
    if isinstance(char_dict, str):
        char_dict = char_dicts.get_char_dict(char_dict)
    single_char_index = next(iter(char_dict.keys()))
    rows_per_cell = len(single_char_index)
    columns_per_cell = len(single_char_index[0])

    # determine bounds of render grid
    xvals = np.array(xvals, dtype=float)  # type: ignore
    yvals = np.array(yvals, dtype=float)  # type: ignore
    xmask = ~np.isnan(xvals)
    ymask = ~np.isnan(yvals)
    mask = xmask * ymask
    non_none_xvals = xvals[mask]  # type: ignore
    non_none_yvals = yvals[mask]  # type: ignore
    xmin = min(non_none_xvals)
    xmax = max(non_none_xvals)
    xrange = xmax - xmin
    ymin = min(non_none_yvals)
    ymax = max(non_none_yvals)
    yrange = ymax - ymin
    grid_ymin = max(ymin - 0.1 * yrange, 0)

    # create grid in which to render plot
    grid = grid_utils.create_grid(
        n_rows=n_rows * rows_per_cell,
        n_columns=n_columns * columns_per_cell,
        xmin=xmin - 0.0 * xrange,
        xmax=xmax + 0.0 * xrange,
        ymin=grid_ymin,
        ymax=ymax + 0.1 * yrange,
    )
    render_grid = grid_utils.create_grid(
        n_rows=n_rows,
        n_columns=n_columns,
        xmin=xmin - 0.0 * xrange,
        xmax=xmax + 0.0 * xrange,
        ymin=grid_ymin,
        ymax=ymax + 0.1 * yrange,
    )

    # render raster of line plot
    raster = raster_utils.rasterize_line_plot(
        xvals=xvals,
        yvals=yvals,
        grid=grid,
    )

    # render as supergrid
    plot = render_utils.render_supergrid(
        array=raster,
        rows_per_cell=rows_per_cell,
        columns_per_cell=columns_per_cell,
        char_dict=char_dict,
    )

    # stylize plot line
    if line_style is not None:
        new_lines = [
            formats.add_style(line, line_style)
            for line in plot.split('\n')
        ]
        plot = '\n'.join(new_lines)

    # create y axis
    if yaxis_kwargs is None:
        yaxis_kwargs = {}
    y_axis = render_utils.render_y_axis(
        grid=render_grid,
        width=y_axis_width,
        chrome_style=chrome_style,
        tick_label_style=tick_label_style,
        **yaxis_kwargs
    )
    graph = formats.concatenate_blocks([y_axis, plot])

    # create x axis
    if xaxis_kwargs is None:
        xaxis_kwargs = {}
    x_axis = render_utils.render_x_axis(
        grid=render_grid,
        chrome_style=chrome_style,
        tick_label_style=tick_label_style,
        **xaxis_kwargs
    )
    x_axis = formats.indent_block(x_axis, indent=y_axis_width)
    graph = graph + '\n' + x_axis

    return graph


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
