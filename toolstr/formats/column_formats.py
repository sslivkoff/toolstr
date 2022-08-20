from __future__ import annotations

import math
import typing

from . import positional_formats


def columnize(
    text: str,
    *,
    n_columns: int | None = None,
    max_height: int | None = None,
    header_height: int | None = None,
    gap: int | str | None = None,
) -> str:
    """number of columns is determined by n_columns or height

    TODO: implement flexbox justification styles
    - https://css-tricks.com/snippets/css/a-guide-to-flexbox/
    """

    columns = _raw_columnize(
        text=text,
        n_columns=n_columns,
        max_height=max_height,
        header_height=header_height,
    )

    # upper block
    min_height = len(columns[-1])
    columnized = positional_formats.concatenate_blocks(
        [column[:min_height] for column in columns],
        gap=gap,
    )

    # lower block
    if min_height < len(columns[0]):
        lower_block = positional_formats.concatenate_blocks(
            [column[min_height:] for column in columns[:-1]],
            gap=gap,
        )
        columnized = columnized + '\n' + lower_block

    return columnized


def _raw_columnize(
    text: str,
    *,
    n_columns: int | None = None,
    max_height: int | None = None,
    header_height: int | None = None,
) -> typing.Sequence[typing.Sequence[str]]:

    lines = text.split('\n')

    if header_height is None:
        header_height = 0
    header = lines[:header_height]
    remaining_lines = lines[header_height:]

    if max_height is None and n_columns is None:
        raise Exception('must specify max_height or n_columns')
    if n_columns is not None:
        max_height = math.ceil(len(lines) / n_columns)
    if max_height is None:
        raise Exception('must specify max_height')

    columns = []
    while len(remaining_lines) > 0:
        column = header + remaining_lines[: max_height - header_height]
        columns.append(column)
        column_size = len(column)
        remaining_lines = remaining_lines[column_size:]

    return columns
