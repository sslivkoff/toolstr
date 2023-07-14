from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import toolcli

    class NestedDiff(typing.TypedDict):
        type: typing.Literal['type', 'keys', 'value', 'length', 'order']
        index: typing.Sequence[typing.Any]
        lhs: typing.Any
        rhs: typing.Any


#
# # equality checks
#


def nested_repr(nested: typing.Any) -> str:
    import json

    return json.dumps(nested, sort_keys=True)


def nested_equal(lhs: typing.Any, rhs: typing.Any) -> bool:
    return nested_repr(lhs) == nested_repr(rhs)


#
# # str conversion
#


def print_nested_diff(
    lhs: typing.Any,
    rhs: typing.Any,
    *,
    lhs_name: str | None = None,
    rhs_name: str | None = None,
    styles: typing.Mapping[str, str] | toolcli.StyleTheme | None = None,
    indent: bool | int | str | None = None,
    verbose: int | bool = 2,
    max_depth: int | None = None,
    max_branches: int | None = None,
    max_branches_per_depth: typing.Mapping[int, int] | None = None,
    max_diffs: int | None = None,
) -> None:
    import toolstr

    as_str = create_nested_diff_str(
        lhs=lhs,
        rhs=rhs,
        lhs_name=lhs_name,
        rhs_name=rhs_name,
        styles=styles,
        indent=indent,
        verbose=verbose,
        max_depth=max_depth,
        max_branches=max_branches,
        max_branches_per_depth=max_branches_per_depth,
        max_diffs=max_diffs,
    )
    toolstr.print(as_str)


def create_nested_diff_str(
    lhs: typing.Any,
    rhs: typing.Any,
    *,
    lhs_name: str | None = None,
    rhs_name: str | None = None,
    styles: typing.Mapping[str, str] | toolcli.StyleTheme | None = None,
    indent: bool | int | str | None = None,
    verbose: int | bool = 2,
    max_depth: int | None = None,
    max_branches: int | None = None,
    max_branches_per_depth: typing.Mapping[int, int] | None = None,
    max_diffs: int | None = None,
) -> str:
    import toolstr

    if lhs_name is None:
        lhs_name = 'lhs'
    if rhs_name is None:
        rhs_name = 'rhs'

    # gather diffs
    diffs = get_nested_diffs(
        lhs=lhs,
        rhs=rhs,
        max_depth=max_depth,
        max_branches=max_branches,
        max_branches_per_depth=max_branches_per_depth,
    )
    add_ellipsis = False
    if max_diffs is not None and len(diffs) > max_diffs:
        diffs = diffs[:max_diffs]
        add_ellipsis = True

    # convert diffs to rows
    rows = []
    for diff in diffs:
        index = '.'.join(str(item) for item in diff['index'])
        lhs_value = diff['lhs']
        rhs_value = diff['rhs']
        if diff['type'] == 'keys':
            lhs_value = ' '.join(lhs_value)
            rhs_value = ' '.join(rhs_value)
        elif diff['type'] == 'order':
            if lhs_value is None:
                lhs_value = ''
            if rhs_value is None:
                rhs_value = ''
        row = [diff['type'], index, lhs_value, rhs_value]
        rows.append(row)

    # convert to table
    if styles is None:
        styles = {}
    as_str: str = toolstr.print_multiline_table(  # type: ignore
        rows=rows,
        labels=['type', 'index', lhs_name, rhs_name],
        column_justify={'index': 'left', lhs_name: 'left', rhs_name: 'left'},
        label_justify='left',
        vertical_justify='top',
        return_str=True,
        max_column_widths=[6, 30, 32, 32],
        compact=3,
        label_style=styles.get('metavar'),
        border=styles.get('content'),
        indent=indent,
        separate_all_rows=False,
    )
    if add_ellipsis:
        as_str = as_str + '\n...'
    return as_str


#
# # gather nested diffs
#


def get_nested_diffs(
    lhs: typing.Any,
    rhs: typing.Any,
    max_depth: int | None = None,
    max_branches: int | None = None,
    max_branches_per_depth: typing.Mapping[int, int] | None = None,
) -> typing.Sequence[NestedDiff]:
    diff: NestedDiff
    if nested_equal(lhs, rhs):
        return []
    elif type(lhs) is not type(rhs):
        lhs_type = type(lhs).__name__
        rhs_type = type(rhs).__name__
        diff = {'type': 'type', 'index': [], 'lhs': lhs_type, 'rhs': rhs_type}
        return [diff]
    elif isinstance(lhs, dict):
        return get_dict_diffs(lhs, rhs)
    elif isinstance(lhs, (list, tuple)):
        return get_list_diffs(lhs, rhs)
    elif isinstance(lhs, str):
        size = 32
        lhs_chunks = [lhs[i : i + size] for i in range(0, len(lhs), size)]
        rhs_chunks = [rhs[i : i + size] for i in range(0, len(rhs), size)]
        diff = {
            'type': 'value',
            'index': [],
            'lhs': '\n'.join(lhs_chunks),
            'rhs': '\n'.join(rhs_chunks),
        }
        return [diff]
    elif isinstance(lhs, (int, float, bool)):
        diff = {'type': 'value', 'index': [], 'lhs': lhs, 'rhs': rhs}
        return [diff]
    else:
        raise Exception('not a valid nested type: ' + str(type(lhs)))


def get_dict_diffs(
    lhs: typing.Mapping[typing.Any, typing.Any],
    rhs: typing.Mapping[typing.Any, typing.Any],
    ignore_order: bool = True,
) -> typing.Sequence[NestedDiff]:
    diffs = []
    diff: NestedDiff

    # process inputs
    lhs_keys = list(lhs.keys())
    rhs_keys = list(rhs.keys())
    lhs_key_set = set(lhs_keys)
    rhs_key_set = set(rhs_keys)

    # diff in order
    if not ignore_order and lhs_keys != rhs_keys:
        diff = {'type': 'order', 'index': [], 'lhs': None, 'rhs': None}
        diffs.append(diff)

    # diff in keys
    if lhs_key_set != rhs_key_set:
        lhs_only = sorted(lhs_key_set - rhs_key_set)
        rhs_only = sorted(rhs_key_set - lhs_key_set)
        diff = {'type': 'keys', 'index': [], 'lhs': lhs_only, 'rhs': rhs_only}
        diffs.append(diff)

    # diff in values
    common_keys = lhs_key_set & rhs_key_set
    for key in common_keys:
        if not nested_equal(lhs[key], rhs[key]):
            sub_diffs = get_nested_diffs(lhs[key], rhs[key])
            for sub_diff in sub_diffs:
                diff = sub_diff.copy()
                diff['index'] = [key] + list(sub_diff['index'])
                diffs.append(diff)

    return diffs


def get_list_diffs(
    lhs: typing.Sequence[typing.Any],
    rhs: typing.Sequence[typing.Any],
) -> typing.Sequence[NestedDiff]:
    diffs = []
    diff: NestedDiff

    # diff in length
    if len(lhs) != len(rhs):
        diff = {'type': 'length', 'index': [], 'lhs': len(lhs), 'rhs': len(rhs)}
        diffs.append(diff)

    # diff in values
    for i, (lhs_item, rhs_item) in enumerate(zip(lhs, rhs)):
        if not nested_equal(lhs_item, rhs_item):
            sub_diffs = get_nested_diffs(lhs_item, rhs_item)
            for sub_diff in sub_diffs:
                diff = sub_diff.copy()
                diff['index'] = [i] + list(sub_diff['index'])
                diffs.append(diff)

    return diffs

