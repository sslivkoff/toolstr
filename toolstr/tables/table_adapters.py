from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import pandas as pd

from . import table_utils


def print_dataframe_as_table(
    df: pd.DataFrame,
    columns: typing.Sequence[typing.Any] | None = None,
    include_index: bool = True,
    **table_kwargs: typing.Any,
) -> str | None:

    # promote index columns to plain columns
    if include_index:
        df = df.reset_index()

    # compile columns
    if columns is not None:
        # filter columns
        df = df[[column for column in columns]]
    else:
        # use all columns
        columns = list(df.columns.values)

    # convert to list of lists
    rows = df.values.tolist()

    return table_utils.print_table(rows=rows, headers=columns, **table_kwargs)


def print_dict_of_lists_as_table(
    dict_of_lists: typing.Mapping[typing.Any, typing.Sequence[typing.Any]],
    keys: typing.Sequence[typing.Any] | None = None,
    **table_kwargs: typing.Any,
) -> str | None:

    # determine keys
    if keys is None:
        keys = list(dict_of_lists.keys())

    # create rows
    rows = [list(row) for row in zip(*[dict_of_lists[key] for key in keys])]

    return table_utils.print_table(rows=rows, headers=keys, **table_kwargs)


def print_list_of_dicts_as_table(
    list_of_dicts: typing.Sequence[typing.Mapping[typing.Any, typing.Any]],
    keys: typing.Sequence[typing.Any] | None = None,
    **table_kwargs: typing.Any,
) -> str | None:

    # determine keys
    if keys is None:
        keys = []
        key_set = set()
        for item in list_of_dicts:
            for key in item.keys():
                if key not in key_set:
                    keys.append(key)
                    key_set.add(key)

    # format into rows
    rows = []
    for item in list_of_dicts:
        row = []
        for key in keys:
            row.append(item.get(key))
        rows.append(row)

    return table_utils.print_table(rows=rows, headers=keys, **table_kwargs)
