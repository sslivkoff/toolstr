from __future__ import annotations

import typing

from .. import spec
from . import table_utils


def print_multiline_table(
    rows,
    headers,
    row_height: int | None = None,
    row_heights: typing.Sequence[int] | None = None,
    add_row_index: bool = False,
    row_start_index: int = 1,
    vertical_justify: str
    | table_utils.ColumnData[spec.VerticalJustification] = 'center',
    **table_kwargs
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
                height = 1
                for cell in row:
                    if isinstance(cell, str):
                        cell_height = cell.count('\n') + 1
                        height = max(height, cell_height)
                row_heights.append(height)

    if isinstance(vertical_justify, str):
        if headers is not None:
            n_columns = len(headers)
        elif len(rows) > 0:
            n_columns = len(rows[0])
        else:
            n_columns = 0
        vertical_justify = [vertical_justify] * len(headers)
    else:
        vertical_justify = table_utils._convert_column_dict_to_list(
            vertical_justify,
            headers,
        )

    # create row group for each row
    new_rows = []
    for row, height in zip(rows, row_heights):

        row_group = [[] for r in range(height)]
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
                full_lines = cell_lines + [None] * extra_height
            elif column_justify == 'bottom':
                full_lines = [None] * extra_height + cell_lines
            elif column_justify == 'center':
                extra_top = int(extra_height / 2)
                extra_bottom = extra_height - extra_top
                full_lines = (
                    [None] * extra_top + cell_lines + [None] * extra_bottom
                )
            else:
                raise Exception('unknown justification')

            # insert lines into row groups
            for group_row, cell_line in zip(row_group, full_lines):
                group_row.append(cell_line)

        # add new rows to new_rows
        if len(new_rows) > 0:
            new_rows.append(None)
        for group_row in row_group:
            new_rows.append(group_row)

    return table_utils.print_table(
        rows=new_rows,
        headers=headers,
        **table_kwargs,
    )
