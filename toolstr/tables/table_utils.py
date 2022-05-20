"""

TODO
- outer borders
- row separators
- header_border_style different from border_style
    - also use header_border_style for the outer_border if active
- multiline headers

Saving until later
- multiline cells
    - need to get row separator feature working first
    - can get multline headers working first
    multiline_cells: bool | None = None,

"""
from __future__ import annotations

import typing
import types

from .. import formatting
from .. import outlines
from .. import spec


if typing.TYPE_CHECKING:
    import rich.console

    Row = typing.Sequence[typing.Any]
    Style = typing.Union[str, typing.Callable[..., str]]
    HeaderSingleLocation = typing.Literal['top', 'bottom']
    HeaderPluralLocation = typing.Tuple[
        HeaderSingleLocation,
        HeaderSingleLocation,
    ]
    HeaderLocation = typing.Union[HeaderSingleLocation, HeaderPluralLocation]

    T = typing.TypeVar('T')
    ColumnData = typing.Union[
        typing.Sequence[typing.Union[T, None]],
        typing.Mapping[typing.Union[str, int], typing.Union[T, None]],
    ]

    FormatKwargs = typing.Mapping[str, typing.Any]


def print_table(
    #
    # content
    rows: typing.Sequence[typing.Any],
    headers: typing.Sequence[str] | None = None,
    add_row_index: bool = False,
    row_start_index: int = 1,
    missing_columns: typing.Literal['clip', 'fill', 'error'] = 'error',
    empty_str: str = '',
    format: FormatKwargs | None = None,
    column_format: ColumnData[FormatKwargs] | None = None,
    return_str: bool = False,
    #
    # io
    file: typing.TextIO | None = None,
    console: rich.console.Console | None = None,
    use_styles: bool = True,
    use_rich: bool | None = None,
    #
    # table
    header_location: HeaderLocation | None = None,
    max_table_width: int | None = None,
    column_widths: typing.Sequence[int] | None = None,
    indent: str | int | None = None,
    outer_gap: int | str | None = None,
    column_gap: int | str | None = None,
    compact: bool = False,
    outer_borders: bool = False,
    border_style: str | spec.BorderCharSet | None = None,
    #
    # cell
    justify: spec.HorizontalJustification = 'right',
    column_justify: ColumnData[spec.HorizontalJustification] | None = None,
    header_justify: ColumnData[spec.HorizontalJustification] | None = None,
    style: Style | None = None,
    column_style: ColumnData[Style] | None = None,
    header_style: ColumnData[Style] | None = None,
) -> str | None:

    # filter row separators
    rows, separator_indices = _filter_separator_indices(rows)

    # check missing columns
    rows, headers = _fix_missing_data(rows, headers, missing_columns, empty_str)

    # add row index
    rows, headers = _add_index(rows, headers, add_row_index, row_start_index)

    # convert cells and headers to str
    str_cells, str_headers, column_widths = _stringify_all(
        rows=rows,
        headers=headers,
        column_widths=column_widths,
        format=format,
        column_format=column_format,
        empty_str=empty_str,
        justify=justify,
        column_justify=column_justify,
        header_justify=header_justify,
        style=style,
        column_style=column_style,
        header_style=header_style,
        use_styles=use_styles,
    )

    # layout table as single str
    table_as_str = _convert_table_to_str(
        str_cells=str_cells,
        str_headers=str_headers,
        column_widths=column_widths,
        compact=compact,
        indent=indent,
        max_table_width=max_table_width,
        header_location=header_location,
        border_style=border_style,
        column_gap=column_gap,
        outer_gap=outer_gap,
        outer_borders=outer_borders,
    )

    # return or print table
    if return_str:
        return table_as_str
    else:
        _print_table(table_as_str, use_rich, use_styles, console, file)


def _filter_separator_indices(rows):
    filtered = []
    indices = []
    for row in rows:
        if row is None:
            index = len(filtered) - 1
            if index < 0:
                raise Exception('cannot start with a row separator')
            indices.append(index)
        filtered.append(row)
    return filtered, indices


def _fix_missing_data(rows, headers, missing_columns, empty_str):
    min_columns = float('inf')
    max_columns = 0
    for row in rows:
        n_row_columns = len(row)
        min_columns = min(min_columns, n_row_columns)
        max_columns = max(max_columns, n_row_columns)
    if headers is not None:
        min_columns = min(min_columns, len(headers))
        max_columns = max(max_columns, len(headers))
    if min_columns != max_columns:
        if missing_columns == 'error':
            raise Exception(
                'different numbers of columns, use missing_columns="clip" or missing_columns="fill"'
            )
        elif missing_columns == 'clip':
            rows = [row[:min_columns] for row in rows]
            if headers is not None:
                headers = headers[:min_columns]
        elif missing_columns == 'fill':
            rows = [
                row + [empty_str] * (max_columns - len(row)) for row in rows
            ]
            if headers is not None:
                headers = headers + [''] * (max_columns - len(headers))
    return rows, headers


def _add_index(rows, headers, add_row_index, row_start_index):
    if add_row_index:
        if headers is not None:
            if isinstance(add_row_index, str):
                index_name = add_row_index
            else:
                index_name = ''
            headers = [index_name] + list(headers)
        rows = [[str(row_start_index + r)] + row for r, row in enumerate(rows)]

    return rows, headers


def _stringify_all(
    rows,
    headers,
    column_widths,
    format,
    column_format,
    empty_str,
    justify,
    column_justify,
    header_justify,
    style,
    column_style,
    header_style,
    use_styles,
):

    # convert cells to str
    column_format = _convert_column_dict_to_list(column_format, headers)
    str_cells = [
        _stringify_cells(row, format, column_format, empty_str) for row in rows
    ]
    if headers is not None:
        str_headers = _stringify_cells(headers, format, None, empty_str)
    else:
        str_headers = None

    # determine column widths
    if column_widths is None:
        column_widths = _get_column_widths(str_cells, str_headers)

    # trim and justify cells to column widths
    column_justify = _convert_column_dict_to_list(column_justify, headers)
    str_cells = [
        _trim_justify_cells(str_row, column_widths, column_justify, justify)
        for str_row in str_cells
    ]
    if headers is not None:
        if header_justify is None:
            header_justify = 'right'
        if isinstance(header_justify, str):
            header_justify = [header_justify] * len(headers)
        str_headers = _trim_justify_cells(
            str_headers, column_widths, header_justify, justify
        )

    # add styles
    if use_styles:
        column_style = _convert_column_dict_to_list(column_style, headers)
        str_cells = [
            _stylize_row(str_row, style, column_style) for str_row in str_cells
        ]
        if headers is not None:
            str_headers = _stylize_row(str_headers, style, header_style)

    return str_cells, str_headers, column_widths


def _get_column_widths(str_cells, str_headers):
    if len(str_cells) > 0:
        n_columns = len(str_cells[0])
    elif len(str_headers) > 0:
        n_columns = len(str_headers)
    else:
        return []
    max_column_widths: list[int] = [0] * n_columns
    for row_str_cells in str_cells:
        for c, str_cell in enumerate(row_str_cells):
            cell_width = len(str_cell)
            if cell_width > max_column_widths[c]:
                max_column_widths[c] = cell_width
    if str_headers is not None:
        while len(str_headers) > len(max_column_widths):
            max_column_widths.append(0)
        for c, header in enumerate(str_headers):
            if len(header) > max_column_widths[c]:
                max_column_widths[c] = len(header)

    return max_column_widths


def _convert_column_dict_to_list(
    column_data: ColumnData[T],
    headers: typing.Sequence[str] | None = None,
) -> typing.Sequence[T | None]:
    """convert a dict of column data to a list of column data"""

    if column_data is None or isinstance(column_data, list):
        return column_data

    elif isinstance(column_data, dict):

        if all(isinstance(item, int) for item in column_data.keys()):
            n_columns = max(column_data.keys())
            return [column_data.get(c) for c in range(n_columns)]
        elif all(isinstance(item, str) for item in column_data.keys()):
            if headers is None:
                raise Exception('must provide headers for named column data')
            return [column_data.get(header) for header in headers]
        else:
            raise Exception('unknown column data')

    else:
        raise Exception('unknown format: ' + str(column_data))


def _stringify_cells(row, format, column_format, empty_str):
    row_str_cells = []
    for c, cell in enumerate(row):

        if cell is None:
            cell = empty_str

        # convert to str
        if isinstance(cell, str):
            as_str = cell
        else:
            if isinstance(cell, (int, float)):

                # get format kwargs
                cell_format: typing.Mapping[str, typing.Any] | None
                if format is not None:
                    cell_format = format
                elif column_format is not None:
                    cell_format = column_format[c]
                else:
                    cell_format = None

                # format as str
                if cell_format is not None:
                    as_str = formatting.format(cell, **cell_format)
                else:
                    as_str = formatting.format(cell)

            else:
                as_str = str(cell)

        # use only first line
        if '\n' in as_str:
            as_str = as_str.split('\n')[0]

        row_str_cells.append(as_str)

    return row_str_cells


def _trim_justify_cells(
    str_row: typing.Sequence[str],
    column_widths: typing.Sequence[int],
    column_justify: typing.Sequence[spec.HorizontalJustification | None] | None,
    justify: spec.HorizontalJustification,
) -> list[str]:
    """trim or justify cells in row to target sizes"""

    output = []
    for c, cell in enumerate(str_row):
        length = len(cell)
        width = column_widths[c]
        if length >= width:

            # trim
            output.append(cell[:width])

        else:

            # determine justification
            cell_justify = None
            if column_justify is not None:
                cell_justify = column_justify[c]
            if cell_justify is None:
                cell_justify = justify

            # justify
            output.append(formatting.hjustify(cell, cell_justify, width))

    return output


def _stylize_row(row, style, column_style):
    stylized_row = []
    for c, cell in enumerate(row):
        if column_style is not None and column_style[c] is not None:
            cell_style: typing.Callable | str | None = column_style[c]
        elif style is not None:
            cell_style = style
        else:
            cell_style = None
        if cell_style is not None:
            if isinstance(cell_style, types.FunctionType):
                cell_style = cell_style(cell)
            if not isinstance(cell_style, str):
                raise Exception('could not convert style to str')
            cell = '[' + cell_style + ']' + cell + '[/' + cell_style + ']'
        stylized_row.append(cell)
    return stylized_row


def _process_header_location(
    header_location: str | tuple | list | None,
) -> tuple[bool, bool]:

    if isinstance(header_location, str):
        top_header = header_location == 'top'
        bottom_header = header_location == 'bottom'
    elif isinstance(header_location, (tuple, list)):
        top_header = 'top' in header_location
        bottom_header = 'bottom' in header_location
    elif header_location is None:
        top_header = True
        bottom_header = False
    else:
        raise Exception('unknown header_location format')

    return top_header, bottom_header


def _convert_table_to_str(
    str_cells,
    str_headers,
    column_widths,
    compact,
    indent,
    max_table_width,
    header_location,
    border_style,
    column_gap,
    outer_gap,
    outer_borders,
):

    # use compact format
    if compact:
        outer_gap = ''
        column_gap = ''
        border_style = outlines.get_border_chars()
        border_style['vertical'] = ' '
        border_style['cross'] = border_style['horizontal']

    # determine border styles
    if border_style is None:
        border_style = outlines.get_border_chars()
    if isinstance(border_style, str):
        border_style = outlines.get_border_chars_by_name(border_style)
    horizontal = border_style['horizontal']
    vertical = border_style['vertical']
    cross = border_style['cross']

    # determine gaps and delimiters
    if indent is None:
        indent = ''
    if isinstance(indent, int):
        indent = ' ' * indent
    if column_gap is None:
        column_gap = '  '
    if isinstance(column_gap, int):
        column_gap = ' ' * column_gap
    if isinstance(outer_gap, int):
        outer_gap = ' ' * outer_gap
    if outer_gap is None:
        outer_gap = column_gap
    column_delimiter = column_gap + vertical + column_gap

    # render rows as strs
    formatted_rows = []
    for str_row in str_cells:

        # concatenate subcomponents
        formatted_row = outer_gap + column_delimiter.join(str_row) + outer_gap
        if outer_borders:
            formatted_row = vertical + formatted_row + vertical
        formatted_row = indent + formatted_row

        # trim
        if max_table_width is not None:
            if len(formatted_row) > max_table_width:
                formatted_row = formatted_row[:max_table_width]

        formatted_rows.append(formatted_row)

    if str_headers is not None:
        # stylize header

        formatted_header = (
            outer_gap + column_delimiter.join(str_headers) + outer_gap
        )
        if outer_borders:
            formatted_header = vertical + formatted_header + vertical
        formatted_header = indent + formatted_header
        separator_delimiter = (
            len(column_gap) * horizontal + cross + len(column_gap) * horizontal
        )
        separator_spaces = [
            column_width * horizontal for column_width in column_widths
        ]
        row_separator = (
            len(outer_gap) * horizontal
            + separator_delimiter.join(separator_spaces)
            + len(outer_gap) * horizontal
        )
        if outer_borders:
            row_separator = (
                border_style['left_t'] + row_separator + border_style['right_t']
            )
        row_separator = indent + row_separator

    # determine header positions
    top_header = False
    bottom_header = False
    if str_headers is not None:
        top_header, bottom_header = _process_header_location(header_location)

    if outer_borders:
        upper_left = border_style['upper_left']
        upper_right = border_style['upper_right']
        upper_t = border_style['upper_t']
        top_border_separator = (
            len(column_gap) * horizontal
            + upper_t
            + len(column_gap) * horizontal
        )
        top_border = (
            upper_left
            + horizontal * len(outer_gap)
            + top_border_separator.join(
                [horizontal * width for width in column_widths]
            )
            + horizontal * len(outer_gap)
            + upper_right
        )

        lower_left = border_style['lower_left']
        lower_right = border_style['lower_right']
        lower_t = border_style['lower_t']
        bottom_border_separator = (
            len(column_gap) * horizontal
            + lower_t
            + len(column_gap) * horizontal
        )
        bottom_border = (
            lower_left
            + horizontal * len(outer_gap)
            + bottom_border_separator.join(
                [horizontal * width for width in column_widths]
            )
            + horizontal * len(outer_gap)
            + lower_right
        )

    # gather lines
    lines = []
    if top_header:
        lines.append(formatted_header)
        lines.append(row_separator)
    # lines.extend(formatted_rows)
    for formatted_row in formatted_rows:
        lines.append(formatted_row)
        # lines.append(row_separator)
    if bottom_header:
        lines.append(row_separator)
        lines.append(formatted_header)
    if outer_borders:
        lines = [top_border] + lines + [bottom_border]
    table_as_str = '\n'.join(lines)

    return table_as_str


def _print_table(table_as_str, use_rich, use_styles, console, file):
    if use_rich is None:
        if console is not None:
            use_rich = True
        else:
            use_rich = use_styles
    if use_rich:
        import rich.console

        if console is None:
            console = rich.console.Console(
                file=file,
                theme=rich.theme.Theme(inherit=False),
            )
        console.print(table_as_str, overflow='ignore')
    else:
        print(table_as_str)
