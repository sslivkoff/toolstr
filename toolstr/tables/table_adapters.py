from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from typing_extensions import TypeGuard
    import pandas as pd  # type: ignore
    import polars as pl

from . import table_utils


def print_dataframe_as_table(
    df: pl.DataFrame
    | pd.DataFrame
    | typing.Sequence[pl.DataFrame | pd.DataFrame],
    columns: typing.Sequence[typing.Any] | None = None,
    include_index: bool = True,
    **table_kwargs: typing.Any,
) -> str | None:
    if _is_polars_dataframe(df) or _is_pandas_dataframe(df):
        rows, columns = _dataframe_to_rows(
            df, include_index=include_index, columns=columns
        )
    elif isinstance(df, (list, tuple)):
        rows = []
        candidate_columns = None
        for item in df:
            if _is_polars_dataframe(item) or _is_pandas_dataframe(item):
                df_rows, df_columns = _dataframe_to_rows(
                    item, include_index=include_index, columns=columns
                )
                rows += df_rows
                if candidate_columns is None:
                    candidate_columns = df_columns
                else:
                    if candidate_columns != df_columns:
                        raise Exception('columns do not match')
            elif item is None:
                rows.append(None)
            elif isinstance(item, (list, tuple)):
                rows += item
            else:
                raise Exception('invalid format')
        columns = candidate_columns

    else:
        raise Exception('invalid dataframe format: ' + str(type(df)))

    return table_utils.print_table(rows=rows, labels=columns, **table_kwargs)


def _dataframe_to_rows(
    df: pl.DataFrame | pd.DataFrame,
    include_index: bool = True,
    columns: typing.Sequence[typing.Any] | None = None,
) -> tuple[typing.Sequence[typing.Sequence[typing.Any]], typing.Sequence[str]]:

    if _is_polars_dataframe(df):
        if columns is not None:
            df = df.select(columns)
        if columns is None:
            columns = list(df.columns)
        rows = df.rows()

    elif _is_pandas_dataframe(df):
        # promote index columns to plain columns
        if include_index:
            if df.index.name is not None:
                name = df.index.name
            else:
                name = 'index'
            if columns is not None and name not in columns:
                columns = [name] + list(columns)
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

    else:
        raise Exception('invalid dataframe format: ' + str(type(df)))

    return rows, columns


def _is_polars_dataframe(df: typing.Any) -> TypeGuard[pl.DataFrame]:
    for parent in type(df).__mro__:
        if parent.__module__.startswith('polars'):
            return True
    else:
        return False


def _is_pandas_dataframe(df: typing.Any) -> TypeGuard[pd.DataFrame]:
    for parent in type(df).__mro__:
        if parent.__module__.startswith('pandas'):
            return True
    else:
        return False


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

    return table_utils.print_table(rows=rows, labels=keys, **table_kwargs)


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

    return table_utils.print_table(rows=rows, labels=keys, **table_kwargs)

