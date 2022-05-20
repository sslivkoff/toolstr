from __future__ import annotations

import typing

from .. import spec
from . import table_utils


def print_multiline_table(
    rows: list[typing.Sequence[typing.Any]],
    headers: typing.Sequence[str] | None = None,
    row_height: int | None = None,
    row_heights: typing.Sequence[int] | None = None,
    add_row_index: bool = False,
    row_start_index: int = 1,
    vertical_justify: spec.VerticalJustification
    | table_utils.ColumnData[spec.VerticalJustification] = 'center',
    **table_kwargs: typing.Any
) -> str | None:

    # add row index
    rows, headers = table_utils._add_index(
        rows, headers, add_row_index, row_start_index
    )

    # determine height of each row
    if row_heights is None:
        if row_height is not None:
            row_heights = [row_height] * len(rows)
        else:
            row_heights = []
            for row in rows:
                height = _get_row_height(row)
                row_heights.append(height)

    # proces vertical justification
    if headers is not None:
        n_columns = len(headers)
    elif len(rows) > 0:
        n_columns = len(rows[0])
    else:
        n_columns = 0
    if isinstance(vertical_justify, str):
        vertical_justify = [
            typing.cast(spec.VerticalJustification, vertical_justify)
        ] * n_columns
    else:
        vertical_justify = table_utils._convert_column_dict_to_list(
            vertical_justify,
            n_columns,
            headers,
        )

    # create row group for each row
    new_rows: typing.List[None | typing.Sequence[typing.Any]] = []
    for row, height in zip(rows, row_heights):

        # add row separator
        if len(new_rows) > 0:
            new_rows.append(None)

        # split into lines
        row_group = _split_multiline_row(row, height, vertical_justify, headers)

        # add new rows to new_rows
        for group_row in row_group:
            new_rows.append(group_row)

    return table_utils.print_table(
        rows=new_rows,
        headers=headers,
        **table_kwargs,
    )


def _get_row_height(row: typing.Sequence[str]) -> int:
    height = 1
    for cell in row:
        if isinstance(cell, str):
            cell_height = cell.count('\n') + 1
            height = max(height, cell_height)
    return height


def _split_multiline_row(
    row: typing.Sequence[str],
    height: int | None = None,
    vertical_justify: table_utils.ColumnData[spec.VerticalJustification]
    | None = None,
    headers: typing.Sequence[str] | None = None,
) -> list[list[typing.Any]]:

    # determine row height
    if height is None:
        height = _get_row_height(row)

    if vertical_justify is None:
        vertical_justify = 'top'
    if not isinstance(vertical_justify, list):
        vertical_justify = table_utils._convert_column_dict_to_list(
            vertical_justify, n_columns=len(row), headers=headers
        )

    row_group: list[list[typing.Any]] = [[] for r in range(height)]
    for c, cell in enumerate(row):

        # split cell into individual lines
        if isinstance(cell, str):
            cell_lines = cell.split('\n')
        else:
            cell_lines = [cell]
        cell_height = len(cell_lines)
        extra_height = height - cell_height

        # clip overflowing cell lines
        if len(cell_lines) > height:
            cell_lines = cell_lines[:height]

        # insert empty lines based on justification
        column_justify = vertical_justify[c]
        if column_justify == 'top':
            full_lines: typing.Sequence[typing.Any] = (
                cell_lines + [None] * extra_height  # type: ignore
            )
        elif column_justify == 'bottom':
            full_lines = [None] * extra_height + cell_lines  # type: ignore
        elif column_justify == 'center':
            extra_top = int(extra_height / 2)
            extra_bottom = extra_height - extra_top
            full_lines = (
                [None] * extra_top + cell_lines + [None] * extra_bottom  # type: ignore
            )
        else:
            raise Exception('unknown justification')

        # insert lines into row groups
        for group_row, cell_line in zip(row_group, full_lines):
            group_row.append(cell_line)

    return row_group
