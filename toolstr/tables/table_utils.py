from __future__ import annotations

import typing
import types

from .. import formatting
from .. import outlines
from .. import spec
from . import multiline_tables


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
        str,
        typing.Sequence[typing.Union[T, None]],
        typing.Mapping[typing.Union[str, int], typing.Union[T, None]],
    ]

    FormatKwargs = typing.Mapping[str, typing.Any]


def print_table(
    #
    # content
    rows: typing.Sequence[None | typing.Sequence[typing.Any]],
    headers: typing.Sequence[str] | None = None,
    *,
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
    separate_all_rows: bool = False,
    compact: bool = False,
    outer_borders: bool | None = None,
    border_style: str | spec.BorderChars | None = None,
    header_border_style: str | spec.BorderChars | None = None,
    outer_border_style: str | spec.BorderChars | None = None,
    #
    # cell
    justify: spec.HorizontalJustification = 'right',
    column_justify: ColumnData[spec.HorizontalJustification] | None = None,
    header_justify: ColumnData[spec.HorizontalJustification] | None = None,
    header_vertical_justify: ColumnData[spec.VerticalJustification]
    | None = 'bottom',
    style: Style | None = None,
    column_style: ColumnData[Style] | None = None,
    header_style: ColumnData[Style] | None = None,
) -> str | None:

    # filter row separators
    rows, separator_indices = _filter_separator_indices(rows, separate_all_rows)

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
        header_vertical_justify=header_vertical_justify,
        style=style,
        column_style=column_style,
        header_style=header_style,
        use_styles=use_styles,
        add_row_index=add_row_index,
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
        header_border_style=header_border_style,
        outer_border_style=outer_border_style,
        separator_indices=separator_indices,
    )

    # return or print table
    if return_str:
        return table_as_str
    else:
        _print_table(table_as_str, use_rich, use_styles, console, file)
        return None


def _filter_separator_indices(
    rows: typing.Sequence[None | typing.Sequence[typing.Any]],
    separate_all_rows: bool,
) -> tuple[list[typing.Sequence[typing.Any]], set[int]]:

    filtered: list[typing.Sequence[typing.Any]] = []
    indices = set()
    for row in rows:
        if row is None:
            index = len(filtered) - 1
            if index < 0:
                raise Exception('cannot start with a row separator')
            indices.add(index)
        else:
            filtered.append(row)

    if separate_all_rows:
        indices = set(range(len(rows) - 1))

    return filtered, indices


def _fix_missing_data(
    rows: list[typing.Sequence[typing.Any]],
    headers: typing.Sequence[str] | None,
    missing_columns: typing.Literal['clip', 'fill', 'error'],
    empty_str: str,
) -> tuple[list[typing.Sequence[typing.Any]], typing.Sequence[str] | None]:
    min_columns = 1_000_000_000
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
                list(row) + [empty_str] * (max_columns - len(row))
                for row in rows
            ]
            if headers is not None:
                headers = list(headers) + [''] * (max_columns - len(headers))
    return rows, headers


def _add_index(
    rows: list[typing.Sequence[typing.Any]],
    headers: typing.Sequence[str] | None,
    add_row_index: bool,
    row_start_index: int,
) -> tuple[list[typing.Sequence[typing.Any]], typing.Sequence[str] | None]:
    if add_row_index:
        if headers is not None:
            if isinstance(add_row_index, str):
                index_name = add_row_index
            else:
                index_name = ''
            headers = [index_name] + list(headers)
        rows = [
            [str(row_start_index + r)] + list(row) for r, row in enumerate(rows)
        ]

    return rows, headers


def _stringify_all(
    rows: typing.Sequence[typing.Sequence[typing.Any]],
    headers: typing.Sequence[str] | None,
    column_widths: typing.Sequence[int] | None,
    empty_str: str,
    format: FormatKwargs | None,
    column_format: ColumnData[FormatKwargs] | None,
    use_styles: bool,
    add_row_index: bool,
    justify: spec.HorizontalJustification,
    column_justify: ColumnData[spec.HorizontalJustification] | None,
    header_justify: spec.HorizontalJustification
    | ColumnData[spec.HorizontalJustification]
    | None,
    header_vertical_justify: ColumnData[spec.VerticalJustification] | None,
    style: Style | None,
    column_style: ColumnData[Style] | None,
    header_style: ColumnData[Style] | None,
) -> tuple[list[list[str]], list[list[str]] | None, typing.Sequence[int]]:

    # determine number of columns
    if len(rows) > 0:
        n_columns = len(rows[0])
    elif headers is not None:
        n_columns = len(headers)
    else:
        return [], None, []

    # convert cells to str
    column_format = _convert_column_dict_to_list(
        column_format, n_columns, headers
    )
    str_cells = [
        _stringify_cells(row, format, column_format, empty_str) for row in rows
    ]
    if headers is not None:
        header_lines = multiline_tables._split_multiline_row(
            headers,
            vertical_justify=header_vertical_justify,
        )
        str_headers = [
            _stringify_cells(header_line, format, None, empty_str)
            for header_line in header_lines
        ]
    else:
        str_headers = None

    # determine column widths
    if column_widths is None:
        if str_headers is not None:
            column_widths = _get_column_widths(str_cells + str_headers)
        else:
            column_widths = _get_column_widths(str_cells)

    # trim and justify cells to column widths
    column_justify = _convert_column_dict_to_list(
        column_justify, n_columns, headers
    )
    str_cells = [
        _trim_justify_cells(str_row, column_widths, column_justify, justify)
        for str_row in str_cells
    ]
    if str_headers is not None:
        if header_justify is None:
            header_justify = 'right'
        if isinstance(header_justify, list) and add_row_index:
            header_justify = [header_justify[0]] + header_justify
        header_justify = _convert_column_dict_to_list(header_justify, n_columns, headers)
        if header_justify is not None and len(header_justify) != len(
            str_headers[0]
        ):
            raise Exception('header_justify has wrong length')
        str_headers = [
            _trim_justify_cells(
                str_header, column_widths, header_justify, justify
            )
            for str_header in str_headers
        ]

    # add styles
    if use_styles:
        column_style = _convert_column_dict_to_list(
            column_style, n_columns, headers
        )
        str_cells = [
            _stylize_row(str_row, style, column_style) for str_row in str_cells
        ]
        if str_headers is not None:
            if isinstance(header_style, list) and add_row_index:
                header_style = [header_style[0]] + header_style
            if isinstance(header_style, str):
                header_style = [header_style] * len(str_headers[0])
            if header_style is not None and len(header_style) != len(
                str_headers[0]
            ):
                raise Exception('header_style has wrong length')
            str_headers = [
                _stylize_row(str_header, style, header_style)
                for str_header in str_headers
            ]

    return str_cells, str_headers, column_widths


def _get_column_widths(str_cells: list[list[str]]) -> list[int]:
    if len(str_cells) > 0:
        n_columns = len(str_cells[0])
    else:
        return []
    max_column_widths: list[int] = [0] * n_columns
    for row_str_cells in str_cells:
        for c, str_cell in enumerate(row_str_cells):
            cell_width = len(str_cell)
            if cell_width > max_column_widths[c]:
                max_column_widths[c] = cell_width

    return max_column_widths


@typing.overload
def _convert_column_dict_to_list(
    column_data: None,
    n_columns: int,
    headers: typing.Sequence[str] | None,
) -> None:
    ...


@typing.overload
def _convert_column_dict_to_list(
    column_data: ColumnData[T],
    n_columns: int,
    headers: typing.Sequence[str] | None,
) -> typing.Sequence[T | None]:
    ...


def _convert_column_dict_to_list(
    column_data: ColumnData[T] | None,
    n_columns: int,
    headers: typing.Sequence[str] | None,
) -> None | typing.Sequence[T | None]:
    """convert a dict of column data to a list of column data"""

    if column_data is None or isinstance(column_data, list):
        return column_data

    elif isinstance(column_data, str):
        return [column_data] * n_columns  # type: ignore

    elif isinstance(column_data, dict):

        if all(isinstance(item, int) for item in column_data.keys()):
            return [column_data.get(c) for c in range(n_columns)]
        elif all(isinstance(item, str) for item in column_data.keys()):
            if headers is None:
                raise Exception('must provide headers for named column data')
            return [column_data.get(header) for header in headers]
        else:
            raise Exception('unknown column data')

    else:
        raise Exception('unknown format: ' + str(column_data))


def _stringify_cells(
    row: typing.Sequence[typing.Any],
    format: FormatKwargs | None,
    column_format: typing.Sequence[None | typing.Mapping[str, typing.Any]]
    | None,
    empty_str: str,
) -> list[str]:
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
    column_justify: typing.Sequence[None | spec.HorizontalJustification] | None,
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


def _stylize_row(
    row: list[str],
    style: Style | None,
    column_style: ColumnData[Style] | None,
) -> list[str]:
    stylized_row = []
    for c, cell in enumerate(row):
        if column_style is not None and column_style[c] is not None:
            cell_style: Style | None = column_style[c]
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
    header_location: HeaderLocation | None,
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
    str_cells: list[list[str]],
    str_headers: list[list[str]] | None,
    column_widths: typing.Sequence[int],
    compact: bool,
    indent: str | int | None,
    max_table_width: int | None,
    header_location: HeaderLocation | None,
    border_style: str | spec.BorderChars | None,
    header_border_style: str | spec.BorderChars | None,
    outer_border_style: str | spec.BorderChars | None,
    column_gap: int | str | None,
    outer_gap: int | str | None,
    outer_borders: bool | None,
    separator_indices: set[int],
) -> str:

    # use compact format
    if compact:
        outer_gap = ''
        column_gap = ''
        border_style = outlines.get_border_chars()
        border_style['vertical'] = ' '
        border_style['cross'] = border_style['horizontal']

    if outer_borders is None:
        outer_borders = outer_border_style is not None

    # determine border styles
    if border_style is None:
        border_style = outlines.get_border_chars()
    if isinstance(border_style, str):
        border_style = outlines.get_border_chars_by_name(border_style)
    horizontal = border_style['horizontal']
    vertical = border_style['vertical']
    cross = border_style['cross']

    if header_border_style is None:
        header_border_style = border_style
    elif isinstance(header_border_style, str):
        header_border_style = outlines.get_border_chars_by_name(
            header_border_style
        )
    if outer_border_style is None:
        outer_border_style = header_border_style
    elif isinstance(outer_border_style, str):
        outer_border_style = outlines.get_border_chars_by_name(
            outer_border_style
        )
    outer_equals_inner = outer_border_style['cross'] == border_style['cross']
    header_equals_inner = header_border_style['cross'] == border_style['cross']
    header_equals_outer = (
        header_border_style['cross'] == outer_border_style['cross']
    )

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
    outer_vertical = outer_border_style['vertical']

    # render rows as strs
    formatted_rows = []
    for str_row in str_cells:

        # concatenate subcomponents
        formatted_row = outer_gap + column_delimiter.join(str_row) + outer_gap
        if outer_borders:
            formatted_row = outer_vertical + formatted_row + outer_vertical
        formatted_row = indent + formatted_row

        formatted_rows.append(formatted_row)

    # build row separator
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
        if outer_equals_inner:
            outer_left_t = outer_border_style['left_t']
            outer_right_t = outer_border_style['right_t']
        else:
            outer_left_t = outer_border_style['vertical']
            outer_right_t = outer_border_style['vertical']
        row_separator = outer_left_t + row_separator + outer_right_t

    if str_headers is not None:
        # stylize header

        header_vertical = header_border_style['vertical']
        header_horizontal = header_border_style['horizontal']
        if header_equals_inner:
            header_cross = header_border_style['cross']
        else:
            if header_equals_outer:
                header_cross = header_border_style['lower_t']
            else:
                header_cross = header_border_style['horizontal']
                header_vertical = ' '

        header_column_delimiter = column_gap + header_vertical + column_gap

        formatted_headers = []
        for str_header in str_headers:
            formatted_header = (
                outer_gap + header_column_delimiter.join(str_header) + outer_gap
            )
            if outer_borders:
                formatted_header = (
                    outer_vertical + formatted_header + outer_vertical
                )
            formatted_header = indent + formatted_header

            formatted_headers.append(formatted_header)

        separator_delimiter = (
            len(column_gap) * header_horizontal
            + header_cross
            + len(column_gap) * header_horizontal
        )
        header_separator_spaces = [
            column_width * header_horizontal for column_width in column_widths
        ]
        header_row_separator = (
            len(outer_gap) * header_horizontal
            + separator_delimiter.join(header_separator_spaces)
            + len(outer_gap) * header_horizontal
        )
        if outer_borders:
            if header_equals_outer:
                outer_left_t = outer_border_style['left_t']
                outer_right_t = outer_border_style['right_t']
            else:
                outer_left_t = outer_border_style['vertical']
                outer_right_t = outer_border_style['vertical']
            header_row_separator = (
                outer_left_t + header_row_separator + outer_right_t
            )

    row_separator = indent + row_separator

    # determine header positions
    top_header = False
    bottom_header = False
    if str_headers is not None:
        top_header, bottom_header = _process_header_location(header_location)

    if outer_borders:
        outer_horizontal = outer_border_style['horizontal']
        upper_left = outer_border_style['upper_left']
        upper_right = outer_border_style['upper_right']
        if header_equals_outer:
            upper_t = outer_border_style['upper_t']
        else:
            upper_t = outer_border_style['horizontal']
        if outer_equals_inner:
            lower_t = outer_border_style['lower_t']
        else:
            lower_t = outer_border_style['horizontal']
        top_border_separator = (
            len(column_gap) * outer_horizontal
            + upper_t
            + len(column_gap) * outer_horizontal
        )
        top_border = (
            upper_left
            + outer_horizontal * len(outer_gap)
            + top_border_separator.join(
                [outer_horizontal * width for width in column_widths]
            )
            + outer_horizontal * len(outer_gap)
            + upper_right
        )

        lower_left = outer_border_style['lower_left']
        lower_right = outer_border_style['lower_right']
        bottom_border_separator = (
            len(column_gap) * outer_horizontal
            + lower_t
            + len(column_gap) * outer_horizontal
        )
        bottom_border = (
            lower_left
            + outer_horizontal * len(outer_gap)
            + bottom_border_separator.join(
                [outer_horizontal * width for width in column_widths]
            )
            + outer_horizontal * len(outer_gap)
            + lower_right
        )

    # gather lines
    lines = []
    if top_header:
        for formatted_header in formatted_headers:
            lines.append(formatted_header)
        lines.append(header_row_separator)
    for r, formatted_row in enumerate(formatted_rows):
        lines.append(formatted_row)
        if r in separator_indices:
            lines.append(row_separator)
    if bottom_header:
        lines.append(header_row_separator)
        for formatted_header in formatted_headers:
            lines.append(formatted_header)
    if outer_borders:
        lines = [top_border] + lines + [bottom_border]

    # trim table width
    if max_table_width is not None:
        ellipses = True
        trimmed_lines = []
        for line in lines:
            if len(line) > max_table_width:
                if ellipses:
                    line = line[:max_table_width - 3] + '...'
                else:
                    line = line[:max_table_width]
            trimmed_lines.append(line)
        lines = trimmed_lines

    table_as_str = '\n'.join(lines)

    return table_as_str


def _print_table(
    table_as_str: str,
    use_rich: bool | None,
    use_styles: bool,
    console: rich.console.Console | None,
    file: typing.TextIO | None,
) -> None:
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
                width=10000,
            )
        console.print(table_as_str)
    else:
        print(table_as_str)
