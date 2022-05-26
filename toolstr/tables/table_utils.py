from __future__ import annotations

import typing
import types
from typing_extensions import TypedDict

from .. import formatting
from .. import outlines
from .. import spec
from . import multiline_tables


if typing.TYPE_CHECKING:
    import rich.console

    class TableStyleContext(TypedDict):
        cell: typing.Any
        str_cell: str
        row: typing.Sequence[typing.Any]
        str_row: typing.Sequence[str]
        labels: typing.Sequence[str]
        str_labels: typing.Sequence[str]
        r: int
        c: int

    Row = typing.Sequence[typing.Any]
    Style = typing.Union[str, typing.Callable[[TableStyleContext], str]]
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
    labels: typing.Sequence[str] | None = None,
    *,
    add_row_index: bool = False,
    row_start_index: int = 1,
    missing_columns: typing.Literal['fill', 'clip', 'error'] = 'error',
    empty_str: str = '',
    format: FormatKwargs | None = None,
    column_format: ColumnData[FormatKwargs] | None = None,
    return_str: bool = False,
    #
    # io
    file: typing.TextIO | None = None,
    console: rich.console.Console | None = None,
    use_styles: bool | None = None,
    #
    # table
    label_location: HeaderLocation | None = None,
    max_table_width: int | None = None,
    column_widths: typing.Sequence[int] | None = None,
    indent: str | int | None = None,
    outer_gap: int | str | None = None,
    column_gap: int | str | None = None,
    separate_all_rows: bool = False,
    compact: bool | int = False,
    border: str | spec.BorderChars | None = None,
    label_border: str | spec.BorderChars | None = None,
    outer_border: str | spec.BorderChars | None = None,
    #
    # cell
    justify: spec.HorizontalJustification = 'right',
    column_justify: ColumnData[spec.HorizontalJustification] | None = None,
    label_justify: ColumnData[spec.HorizontalJustification] | None = None,
    label_vertical_justify: ColumnData[spec.VerticalJustification]
    | None = 'bottom',
    style: Style | None = None,
    column_style: ColumnData[Style] | None = None,
    label_style: ColumnData[Style] | None = None,
) -> str | None:

    # filter row separators
    rows, separator_indices = _filter_separator_indices(rows, separate_all_rows)

    # check missing columns
    rows, labels = _fix_missing_data(rows, labels, missing_columns, empty_str)

    # add row index
    rows, labels = _add_index(rows, labels, add_row_index, row_start_index)

    # convert cells and labels to str
    str_cells, str_labels, column_widths, use_styles = _stringify_all(
        rows=rows,
        labels=labels,
        column_widths=column_widths,
        format=format,
        column_format=column_format,
        empty_str=empty_str,
        justify=justify,
        column_justify=column_justify,
        label_justify=label_justify,
        label_vertical_justify=label_vertical_justify,
        style=style,
        column_style=column_style,
        label_style=label_style,
        use_styles=use_styles,
        add_row_index=add_row_index,
    )

    # layout table as single str
    table_as_str = _convert_table_to_str(
        str_cells=str_cells,
        str_labels=str_labels,
        column_widths=column_widths,
        compact=compact,
        indent=indent,
        max_table_width=max_table_width,
        label_location=label_location,
        border=border,
        column_gap=column_gap,
        outer_gap=outer_gap,
        label_border=label_border,
        outer_border=outer_border,
        separator_indices=separator_indices,
    )

    # return or print table
    if return_str:
        return table_as_str
    else:
        _print_table(table_as_str, use_styles, console, file)
        return None


def _should_use_styles(use_styles: bool | None) -> bool:

    # check that value of use_styles has proper value
    if not isinstance(use_styles, bool) and use_styles is not None:
        raise Exception('use_styles should be bool or None')

    if use_styles is None:

        # use styles if rich is importable
        try:
            import rich

            use_styles = True
        except ImportError:
            use_styles = False

    elif use_styles:

        # test whether rich can be imported
        try:
            import rich
        except ImportError:
            raise Exception('rich required for styles, e.g. `pip install rich`')

    return use_styles


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
    labels: typing.Sequence[str] | None,
    missing_columns: typing.Literal['clip', 'fill', 'error'],
    empty_str: str,
) -> tuple[list[typing.Sequence[typing.Any]], typing.Sequence[str] | None]:
    min_columns = 1_000_000_000
    max_columns = 0
    for row in rows:
        n_row_columns = len(row)
        min_columns = min(min_columns, n_row_columns)
        max_columns = max(max_columns, n_row_columns)
    if labels is not None:
        min_columns = min(min_columns, len(labels))
        max_columns = max(max_columns, len(labels))
    if min_columns != max_columns:
        if missing_columns == 'error':
            raise Exception(
                'different numbers of columns, use missing_columns="clip" or missing_columns="fill"'
            )
        elif missing_columns == 'clip':
            rows = [row[:min_columns] for row in rows]
            if labels is not None:
                labels = labels[:min_columns]
        elif missing_columns == 'fill':
            rows = [
                list(row) + [empty_str] * (max_columns - len(row))
                for row in rows
            ]
            if labels is not None:
                labels = list(labels) + [''] * (max_columns - len(labels))
    return rows, labels


def _add_index(
    rows: list[typing.Sequence[typing.Any]],
    labels: typing.Sequence[str] | None,
    add_row_index: bool,
    row_start_index: int,
) -> tuple[list[typing.Sequence[typing.Any]], typing.Sequence[str] | None]:
    if add_row_index:
        if labels is not None:
            if isinstance(add_row_index, str):
                index_name = add_row_index
            else:
                index_name = ''
            labels = [index_name] + list(labels)
        rows = [
            [str(row_start_index + r)] + list(row) for r, row in enumerate(rows)
        ]

    return rows, labels


def _stringify_all(
    rows: typing.Sequence[typing.Sequence[typing.Any]],
    labels: typing.Sequence[str] | None,
    column_widths: typing.Sequence[int] | None,
    empty_str: str,
    format: FormatKwargs | None,
    column_format: ColumnData[FormatKwargs] | None,
    add_row_index: bool,
    justify: spec.HorizontalJustification,
    column_justify: ColumnData[spec.HorizontalJustification] | None,
    label_justify: spec.HorizontalJustification
    | ColumnData[spec.HorizontalJustification]
    | None,
    label_vertical_justify: ColumnData[spec.VerticalJustification] | None,
    use_styles: bool | None,
    style: Style | None,
    column_style: ColumnData[Style] | None,
    label_style: ColumnData[Style] | None,
) -> tuple[list[list[str]], list[list[str]], typing.Sequence[int], bool]:

    # determine number of columns
    if len(rows) > 0:
        n_columns = len(rows[0])
    elif labels is not None:
        n_columns = len(labels)
    else:
        return [], [], [], False

    # convert cells to str
    column_format = _convert_column_dict_to_list(
        column_format, n_columns, labels
    )
    str_cells = [
        _stringify_cells(row, format, column_format, empty_str) for row in rows
    ]
    if labels is not None:
        label_lines = multiline_tables._split_multiline_row(
            labels,
            vertical_justify=label_vertical_justify,
        )
        str_labels = [
            _stringify_cells(label_line, format, None, empty_str)
            for label_line in label_lines
        ]
    else:
        str_labels = []

    # determine column widths
    if column_widths is None:
        column_widths = _get_column_widths(str_cells + str_labels)

    # trim and justify cells to column widths
    column_justify = _convert_column_dict_to_list(
        column_justify, n_columns, labels
    )
    str_cells = [
        _trim_justify(str_row, column_widths, column_justify, justify)
        for str_row in str_cells
    ]
    if label_justify is None:
        label_justify = 'right'
    if isinstance(label_justify, list) and add_row_index:
        label_justify = [label_justify[0]] + label_justify
    label_justify = _convert_column_dict_to_list(
        label_justify, n_columns, labels
    )
    str_labels = [
        _trim_justify(str_label, column_widths, label_justify, justify)
        for str_label in str_labels
    ]

    # add styles to rows and label
    if use_styles is None:
        use_styles = _should_use_styles(use_styles)
    if use_styles:

        # arrange column style specifications
        column_style = _convert_column_dict_to_list(
            column_style, n_columns, labels
        )

        # style rows
        str_cells = _stylize_rows(
            rows=rows,
            str_rows=str_cells,
            style=style,
            column_style=column_style,
            labels=labels,
            str_labels=str_labels,
        )

        # stylize label
        if isinstance(label_style, list) and add_row_index:
            label_style = [label_style[0]] + label_style
        label_style = _convert_column_dict_to_list(
            label_style, n_columns, labels
        )
        if isinstance(label_style, list) and len(label_style) != len(
            str_labels[0]
        ):
            raise Exception('label_style has wrong length')

        str_labels = _stylize_rows(
            rows=str_labels,
            str_rows=str_labels,
            style=None,
            column_style=label_style,
            labels=labels,
            str_labels=str_labels,
        )

    return str_cells, str_labels, column_widths, use_styles


def _get_column_widths(str_cells: list[list[str]]) -> list[int]:
    if len(str_cells) > 0:
        n_columns = len(str_cells[0])
    else:
        return []
    max_column_widths: list[int] = [0] * n_columns
    for row_str_cells in str_cells:
        for c, str_cell in enumerate(row_str_cells):
            if '[' in str_cell:
                import rich.text

                cell_width = rich.text.Text.from_markup(str_cell).cell_len
            else:
                cell_width = len(str_cell)
            if cell_width > max_column_widths[c]:
                max_column_widths[c] = cell_width

    return max_column_widths


@typing.overload
def _convert_column_dict_to_list(
    column_data: None,
    n_columns: int,
    labels: typing.Sequence[str] | None,
) -> None:
    ...


@typing.overload
def _convert_column_dict_to_list(
    column_data: ColumnData[T],
    n_columns: int,
    labels: typing.Sequence[str] | None,
) -> typing.Sequence[T | None]:
    ...


def _convert_column_dict_to_list(
    column_data: ColumnData[T] | None,
    n_columns: int,
    labels: typing.Sequence[str] | None,
) -> None | typing.Sequence[T | None]:
    """convert a dict of column data to a list of column data"""

    if labels is not None and len(labels) != n_columns:
        raise Exception('mismatching number of columns')

    if column_data is None:
        return column_data

    if isinstance(column_data, list):
        if len(column_data) != n_columns:
            raise Exception('mismatching number of columns')
        return column_data

    elif isinstance(column_data, str):
        return [column_data] * n_columns  # type: ignore

    elif isinstance(column_data, dict):

        if all(isinstance(item, int) for item in column_data.keys()):
            return [column_data.get(c) for c in range(n_columns)]
        elif all(isinstance(item, str) for item in column_data.keys()):
            if labels is None:
                raise Exception('must provide labels for named column data')
            return [column_data.get(label) for label in labels]
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
                cell_format = None
                if column_format is not None:
                    cell_format = column_format[c]
                if format is not None and cell_format is None:
                    cell_format = format

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


def _trim_justify(
    str_row: typing.Sequence[str],
    column_widths: typing.Sequence[int],
    column_justify: typing.Sequence[None | spec.HorizontalJustification] | None,
    justify: spec.HorizontalJustification,
) -> list[str]:
    """trim or justify cells in row to target sizes"""

    if column_justify is not None and len(column_justify) != len(str_row):
        raise Exception('wrong length of list')

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


def _stylize_rows(
    rows: typing.Sequence[typing.Sequence[typing.Any]],
    str_rows: list[list[str]],
    labels: typing.Sequence[typing.Any] | None,
    str_labels: list[list[str]],
    style: Style | None,
    column_style: ColumnData[Style] | None,
) -> list[list[str]]:

    stylized_rows = []
    for r, (row, str_row) in enumerate(zip(rows, str_rows)):

        stylized_row = []
        for c, (cell, str_cell) in enumerate(zip(row, str_row)):

            # use column style if specified, otherwise use global style
            if column_style is not None and column_style[c] is not None:
                cell_style: Style | None = column_style[c]
            elif style is not None:
                cell_style = style
            else:
                cell_style = None

            # if a function, call with table style context
            if isinstance(cell_style, types.FunctionType):
                table_style_context: TableStyleContext = {
                    'cell': cell,
                    'str_cell': str_cell,
                    'row': row,
                    'str_row': str_row,
                    'labels': labels,
                    'str_labels': str_labels,
                    'r': r,
                    'c': c,
                }
                cell_style = cell_style(table_style_context)

            # apply style if present
            if cell_style is not None:
                if not isinstance(cell_style, str):
                    raise Exception('could not convert style to str')
                str_cell = (
                    '[' + cell_style + ']' + str_cell + '[/' + cell_style + ']'
                )
            stylized_row.append(str_cell)

        stylized_rows.append(stylized_row)

    return stylized_rows


def _process_label_location(
    label_location: HeaderLocation | None,
) -> tuple[bool, bool]:

    if isinstance(label_location, str):
        top_label = label_location == 'top'
        bottom_label = label_location == 'bottom'
    elif isinstance(label_location, (tuple, list)):
        top_label = 'top' in label_location
        bottom_label = 'bottom' in label_location
    elif label_location is None:
        top_label = True
        bottom_label = False
    else:
        raise Exception('unknown label_location format')

    return top_label, bottom_label


def _convert_table_to_str(
    str_cells: list[list[str]],
    str_labels: list[list[str]],
    column_widths: typing.Sequence[int],
    compact: bool | int,
    indent: str | int | None,
    max_table_width: int | None,
    label_location: HeaderLocation | None,
    border: str | spec.BorderChars | None,
    label_border: str | spec.BorderChars | None,
    outer_border: bool | str | spec.BorderChars | None,
    column_gap: int | str | None,
    outer_gap: int | str | None,
    separator_indices: set[int],
) -> str:

    # use compact format
    if compact:
        if outer_gap is None:
            outer_gap = ''
        if column_gap is None:
            column_gap = ''
        border = outlines.get_border_chars()
        border['vertical'] = ' ' * int(compact)
        border['cross'] = border['horizontal']

    # determine border styles
    if border is None:
        border = outlines.get_border_chars()
    elif isinstance(border, str):
        border = outlines.get_border_chars_by_name(border)

    # determine label border style
    if label_border is None:
        label_border = border
    elif isinstance(label_border, str):
        label_border = outlines.get_border_chars_by_name(label_border)

    # determine outer border style
    if isinstance(outer_border, bool):
        if outer_border:
            outer_border = label_border
        else:
            outer_border = None
    if isinstance(outer_border, str):
        outer_border = outlines.get_border_chars_by_name(outer_border)

    # determine whether borders match
    label_equals_inner = label_border['cross'] == border['cross']
    if outer_border is not None:
        outer_equals_inner = outer_border['cross'] == border['cross']
        label_equals_outer = label_border['cross'] == outer_border['cross']
    else:
        outer_equals_inner = True
        label_equals_outer = True

    # determine gaps and delimiters
    if column_gap is None:
        column_gap = '  '
    if isinstance(column_gap, int):
        column_gap = ' ' * column_gap
    if isinstance(outer_gap, int):
        outer_gap = ' ' * outer_gap
    if outer_gap is None:
        outer_gap = column_gap

    # render rows as strs
    inner_delimiter = column_gap + border['vertical'] + column_gap
    formatted_rows = [
        outer_gap + inner_delimiter.join(str_row) + outer_gap
        for str_row in str_cells
    ]
    row_separator = _build_row_separator(
        column_widths=column_widths,
        border=border,
        column_gap=column_gap,
        outer_gap=outer_gap,
    )

    # render label as strs
    if len(str_labels) > 0:

        # build label delimiter
        if not label_equals_outer and not label_equals_inner:
            label_vertical = ' '
        else:
            label_vertical = label_border['vertical']
        label_delimiter = column_gap + label_vertical + column_gap

        # build label rows
        formatted_labels = [
            outer_gap + label_delimiter.join(str_label) + outer_gap
            for str_label in str_labels
        ]

        # build top label row separator
        if label_equals_inner:
            label_cross: spec.BorderCharName = 'cross'
        else:
            if label_equals_outer:
                label_cross = 'lower_t'
            else:
                label_cross = 'horizontal'
        label_top_row_separator = _build_row_separator(
            column_widths=column_widths,
            border=label_border,
            column_gap=column_gap,
            outer_gap=outer_gap,
            cross_symbol=label_cross,
        )

        # build bottom label row separator
        if label_equals_inner:
            label_cross = 'cross'
        else:
            if label_equals_outer:
                label_cross = 'upper_t'
            else:
                label_cross = 'horizontal'
        label_bottom_row_separator = _build_row_separator(
            column_widths=column_widths,
            border=label_border,
            column_gap=column_gap,
            outer_gap=outer_gap,
            cross_symbol=label_cross,
        )

    # determine label positions
    top_label = False
    bottom_label = False
    if len(str_labels) > 0:
        top_label, bottom_label = _process_label_location(label_location)

    # add outer borders
    if outer_border is not None:

        # get outer parameters
        if outer_equals_inner:
            outer_left_t = outer_border['left_t']
            outer_right_t = outer_border['right_t']
        else:
            outer_left_t = outer_border['vertical']
            outer_right_t = outer_border['vertical']

        # add outer border to formatted rows
        outer_vertical = outer_border['vertical']
        formatted_rows = [
            outer_vertical + formatted_row + outer_vertical
            for formatted_row in formatted_rows
        ]

        # add outer border to row separator
        row_separator = outer_left_t + row_separator + outer_right_t

        # add outer border to label rows
        formatted_labels = [
            outer_vertical + formatted_label + outer_vertical
            for formatted_label in formatted_labels
        ]

        # load more chars
        outer_horizontal = outer_border['horizontal']

        # create top outer border
        if top_label:
            top_interface = label_equals_outer
        else:
            top_interface = outer_equals_inner
        if top_interface:
            upper_t = outer_border['upper_t']
        else:
            upper_t = outer_border['horizontal']
        top_border_separator = (
            len(column_gap) * outer_horizontal
            + upper_t
            + len(column_gap) * outer_horizontal
        )
        upper_left = outer_border['upper_left']
        upper_right = outer_border['upper_right']
        top_border = (
            upper_left
            + outer_horizontal * len(outer_gap)
            + top_border_separator.join(
                [outer_horizontal * width for width in column_widths]
            )
            + outer_horizontal * len(outer_gap)
            + upper_right
        )

        # create bottom outer border
        if bottom_label:
            bottom_interface = label_equals_outer
        else:
            bottom_interface = outer_equals_inner
        if bottom_interface:
            lower_t = outer_border['lower_t']
        else:
            lower_t = outer_border['horizontal']
        bottom_border_separator = (
            len(column_gap) * outer_horizontal
            + lower_t
            + len(column_gap) * outer_horizontal
        )
        lower_left = outer_border['lower_left']
        lower_right = outer_border['lower_right']
        bottom_border = (
            lower_left
            + outer_horizontal * len(outer_gap)
            + bottom_border_separator.join(
                [outer_horizontal * width for width in column_widths]
            )
            + outer_horizontal * len(outer_gap)
            + lower_right
        )

        # add outer border to label row separator
        if label_equals_outer:
            outer_left_t = outer_border['left_t']
            outer_right_t = outer_border['right_t']
        else:
            outer_left_t = outer_border['vertical']
            outer_right_t = outer_border['vertical']
        label_top_row_separator = (
            outer_left_t + label_top_row_separator + outer_right_t
        )
        label_bottom_row_separator = (
            outer_left_t + label_bottom_row_separator + outer_right_t
        )

    # gather lines
    lines = []
    if top_label:
        for formatted_label in formatted_labels:
            lines.append(formatted_label)
        lines.append(label_top_row_separator)
    for r, formatted_row in enumerate(formatted_rows):
        lines.append(formatted_row)
        if r in separator_indices:
            lines.append(row_separator)
    if bottom_label:
        lines.append(label_bottom_row_separator)
        for formatted_label in formatted_labels:
            lines.append(formatted_label)
    if outer_border is not None:
        lines = [top_border] + lines + [bottom_border]

    # add indent
    if isinstance(indent, int):
        indent = ' ' * indent
    if indent:
        lines = [indent + line for line in lines]

    # trim table width
    if max_table_width is not None:
        ellipses = True
        trimmed_lines = []
        for line in lines:
            if len(line) > max_table_width:
                if ellipses:
                    line = line[: max_table_width - 3] + '...'
                else:
                    line = line[:max_table_width]
            trimmed_lines.append(line)
        lines = trimmed_lines

    # concatenate lines
    table_as_str = '\n'.join(lines)

    return table_as_str


def _build_row_separator(
    column_widths: typing.Sequence[int],
    border: spec.BorderChars,
    column_gap: str,
    outer_gap: str,
    cross_symbol: spec.BorderCharName = 'cross',
) -> str:

    horizontal = border['horizontal']
    cross = border[cross_symbol]

    cgap = len(column_gap)
    ogap = len(outer_gap)

    delimiter = cgap * horizontal + cross + cgap * horizontal
    spaces = [column_width * horizontal for column_width in column_widths]
    return ogap * horizontal + delimiter.join(spaces) + ogap * horizontal


def _print_table(
    table_as_str: str,
    use_styles: bool,
    console: rich.console.Console | None,
    file: typing.TextIO | None,
) -> None:

    if use_styles:

        if console is None:
            import rich.console

            console = rich.console.Console(
                file=file,
                theme=rich.theme.Theme(inherit=False),
                width=10000,
                color_system='truecolor',
            )
        console.print(table_as_str)

    else:
        print(table_as_str)
