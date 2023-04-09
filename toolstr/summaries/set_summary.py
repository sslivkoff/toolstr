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
    include_visuals: bool = True,
    title: str | None = None,
    **kwargs: typing.Sequence[typing.Any],
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

    if len(intersection) == len(lhs) and len(lhs) == len(rhs):
        relation = lhs_name + ' = ' + rhs_name
    elif len(lhs_only) == 0:
        relation = lhs_name + ' ⊂ ' + rhs_name
    elif len(rhs_only) == 0:
        relation = lhs_name + ' ⊃ ' + rhs_name
    elif len(intersection) == 0:
        relation = lhs_name + ' ∩ ' + rhs_name + ' = Ø'
    else:
        relation = ''

    rows: list[list[typing.Any]] = [
        [lhs_name, len(lhs_set)],
        [rhs_name, len(rhs_set)],
        [lhs_name + ' - ' + rhs_name, len(lhs_only)],
        [rhs_name + ' - ' + lhs_name, len(rhs_only)],
        [lhs_name + ' ∩ ' + rhs_name, len(intersection)],
        [lhs_name + ' ∪ ' + rhs_name, len(union)],
    ]

    for row in rows:
        row.append(row[-1] / len(union))

    if include_visuals:
        visuals = _create_set_visuals(
            lhs=lhs,
            rhs=rhs,
            lhs_only=lhs_only,
            rhs_only=rhs_only,
            union=union,
        )
        for visual, row in zip(visuals, rows):
            row.append(visual)

        labels = ['', 'size', '% of ∪', 'visual']
    else:
        labels = ['', 'size', '% of ∪']

    if title is None:
        title = 'Overlap between sets'
    outlines.print_text_box(title)

    if relation != '':
        print()
        print(relation)
    print()
    tables.print_table(
        rows,
        labels=labels,
        column_formats={'% of ∪': {'percentage': True, 'decimals': 1}},
    )

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


def _create_set_visuals(
    *,
    lhs: typing.Sequence[typing.Any],
    rhs: typing.Sequence[typing.Any],
    lhs_only: typing.Sequence[typing.Any],
    rhs_only: typing.Sequence[typing.Any],
    union: typing.Sequence[typing.Any],
    visual_width: int = 30,
    left_cap: str = '└',
    right_cap: str = '┘',
    empty_cap: str = '╵',
) -> typing.Sequence[str]:

    # left_cap: str = '├',
    # right_cap: str = '┤',
    # empty_cap: str = '│',
    # left_cap = '←'
    # right_cap = '→'
    left_cap = '└'
    right_cap = '┘'

    visual_width = 30
    n_per_char = len(union) / visual_width
    if len(lhs) == 0:
        n_left_chars = 1
        lhs_visual = empty_cap
    else:
        n_left_chars = round(len(lhs) / n_per_char)
        n_left_chars = max(2, n_left_chars)
        lhs_visual = left_cap + '─' * (n_left_chars - 2) + right_cap
    lhs_visual = lhs_visual.ljust(visual_width)

    if len(rhs) == 0:
        n_right_chars = 1
        rhs_visual = empty_cap
    else:
        n_right_chars = round(len(rhs) / n_per_char)
        n_right_chars = max(2, n_right_chars)
        rhs_visual = left_cap + '─' * (n_right_chars - 2) + right_cap
    rhs_visual = rhs_visual.rjust(visual_width)

    if len(lhs_only) == 0:
        n_lhs_only_chars = 1
        lhs_only_visual = empty_cap
    else:
        n_lhs_only_chars = visual_width - n_right_chars + 1
        lhs_only_visual = left_cap + '─' * (n_lhs_only_chars - 2) + right_cap
    lhs_only_visual = lhs_only_visual.ljust(visual_width)

    if len(rhs_only) == 0:
        n_rhs_only_chars = 1
        rhs_only_visual = empty_cap
    else:
        n_rhs_only_chars = visual_width - n_left_chars + 1
        rhs_only_visual = left_cap + '─' * (n_rhs_only_chars - 2) + right_cap
    rhs_only_visual = rhs_only_visual.rjust(visual_width)

    left_intersection_pad = n_lhs_only_chars - 1
    right_intersection_pad = n_rhs_only_chars - 1
    n_intersection_chars = (
        visual_width - left_intersection_pad - right_intersection_pad
    )
    intersection_visual = (
        ' ' * left_intersection_pad
        + left_cap
        + '─' * (n_intersection_chars - 2)
        + right_cap
        + ' ' * right_intersection_pad
    )

    union_visual = left_cap + '─' * (visual_width - 2) + right_cap

    return (
        lhs_visual,
        rhs_visual,
        lhs_only_visual,
        rhs_only_visual,
        intersection_visual,
        union_visual,
    )

