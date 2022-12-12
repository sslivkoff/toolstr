from __future__ import annotations

import typing

from .. import formats
from .. import outlines
from .. import tables


def print_set_diff(
    lhs: typing.Sequence[typing.Any] | None = None,
    rhs: typing.Sequence[typing.Any] | None = None,
    *,
    lhs_name: str = 'lhs',
    rhs_name: str = 'rhs',
    verbose: int = 1,
    **kwargs: typing.Sequence[typing.Any]
) -> None:
    if lhs is not None and rhs is not None:
        pass
    elif kwargs is not None and len(kwargs) == 2:
        items = list(kwargs.items())
        lhs_name, lhs = items[0]
        rhs_name, rhs = items[1]
    else:
        raise Exception('must specify sets as kwargs or as lhs/rhs')

    # ensure they are sets
    if lhs is None or rhs is None:
        raise Exception('must specify lhs and rhs')
    lhs_set = set(lhs)
    rhs_set = set(rhs)

    lhs_only = sorted(lhs_set - rhs_set)
    rhs_only = sorted(rhs_set - lhs_set)
    intersection = sorted(lhs_set & rhs_set)
    union = sorted(lhs_set | rhs_set)

    rows = [
        [lhs_name, len(lhs_set)],
        [rhs_name, len(rhs_set)],
        [lhs_name + ' - ' + rhs_name, len(lhs_only)],
        [rhs_name + ' - ' + lhs_name, len(rhs_only)],
        [lhs_name + ' ∩ ' + rhs_name, len(intersection)],
        [lhs_name + ' ∪ ' + rhs_name, len(union)],
    ]

    outlines.print_text_box('Sizes')
    tables.print_table(rows)  # , labels=['', 'size'])

    if verbose >= 2:
        outlines.print_text_box('{ ' + lhs_name + ' - ' + rhs_name + ' }')
        formats.print('size =', len(lhs_only))
        tables.print_table(
            rows=[[item] for item in lhs_only],
            add_row_index=True,
            justify='left',
        )

        outlines.print_text_box('{ ' + rhs_name + ' - ' + lhs_name + ' }')
        formats.print('size =', len(rhs_only))
        tables.print_table(
            rows=[[item] for item in rhs_only],
            add_row_index=True,
            justify='left',
        )

    if verbose >= 3:
        outlines.print_text_box('{ ' + rhs_name + ' ∩ ' + lhs_name + ' }')
        formats.print('size =', len(intersection))
        tables.print_table(
            rows=[[item] for item in intersection],
            add_row_index=True,
            justify='left',
        )

    if verbose >= 4:
        outlines.print_text_box('{ ' + rhs_name + ' ∪ ' + lhs_name + ' }')
        formats.print('size =', len(union))
        tables.print_table(
            rows=[[item] for item in union],
            add_row_index=True,
            justify='left',
        )

