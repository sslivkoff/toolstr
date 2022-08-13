from __future__ import annotations

import functools
import typing

from .. import blocks
from .. import formats
from .. import indents
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
    xtick_format: str | None = 'date',
    yaxis_kwargs: typing.Mapping[typing.Any, typing.Any] | None = None,
    char_dict: str | spec.GridCharDict | None = None,
) -> str:

    if char_dict is None:
        char_dict = 'braille'
    char_dict = char_dicts.get_char_dict(char_dict)
    single_char = next(iter(char_dict.keys()))
    rows_per_cell = len(single_char)
    columns_per_cell = len(single_char[0])

    non_none_xvals = [xval for xval in xvals if xval is not None]
    non_none_yvals = [yval for yval in yvals if yval is not None]

    xmin = min(non_none_xvals)
    xmax = max(non_none_xvals)
    xrange = xmax - xmin

    ymin = min(non_none_yvals)
    ymax = max(non_none_yvals)
    yrange = ymax - ymin

    grid_ymin = max(ymin - 0.1 * yrange, 0)

    grid = grid_utils.create_grid(
        n_rows=n_rows,
        n_columns=n_columns,
        xmin=xmin - 0.0 * xrange,
        xmax=xmax + 0.0 * xrange,
        ymin=grid_ymin,
        ymax=ymax + 0.1 * yrange,
    )

    render_grid = grid_utils.create_grid(
        n_rows=int(n_rows / rows_per_cell),
        n_columns=int(n_columns / columns_per_cell),
        xmin=xmin - 0.0 * xrange,
        xmax=xmax + 0.0 * xrange,
        ymin=grid_ymin,
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
    if line_style is not None:
        new_lines = [
            formats.add_style(line, line_style)
            for line in plot.split('\n')
        ]
        plot = '\n'.join(new_lines)

    y_axis_width = 9
    if yaxis_kwargs is None:
        yaxis_kwargs = {}
    y_axis = render_utils.render_y_axis(
        grid=render_grid,
        width=y_axis_width,
        chrome_style=chrome_style,
        tick_label_style=tick_label_style,
        **yaxis_kwargs
    )

    graph = blocks.concatenate_blocks([y_axis, plot])

    if xtick_format == 'date':
        formatter = functools.partial(
            formats.format_timestamp,
            representation='TimestampDate',
        )
    elif xtick_format == 'age':
        import tooltime

        def formatter(xval: tooltime.Timestamp) -> str:  # type: ignore
            phrase = tooltime.get_age(xval, 'TimelengthPhrase')
            return phrase.split(', ')[0]

    else:
        formatter = None
    x_axis = render_utils.render_x_axis(
        grid=render_grid,
        formatter=formatter,
        chrome_style=chrome_style,
        tick_label_style=tick_label_style,
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
