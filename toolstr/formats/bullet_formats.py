from __future__ import annotations

import typing

import functools

from . import positional_formats
from . import rich_formats


def create_bullet_str(
    value: typing.Any,
    *,
    bullet_str: str | None = None,
    number: int | None = None,
    key: typing.Any | None = None,
    colon_str: str | None = None,
    bullet_style: str | None = None,
    value_style: str | None = None,
    key_style: str | None = None,
    colon_style: str | None = None,
    styles: typing.Mapping[str, str] | None = None,
    indent: int | str | None = None,
) -> str:

    if bullet_style is None and styles is not None:
        bullet_style = styles.get('title')
    if value_style is None and styles is not None:
        value_style = styles.get('description')
    if key_style is None and styles is not None:
        key_style = styles.get('option')
    if colon_style is None and styles is not None:
        colon_style = styles.get('title')

    # construct bullet
    if bullet_str is None:
        if number is not None:
            bullet_str = str(number) + '. '
        else:
            bullet_str = '- '
    bullet_str = rich_formats.add_style(text=bullet_str, style=bullet_style)
    as_str = bullet_str

    # construct key
    if key is not None:
        if colon_str is None:
            colon_str = ': '
        colon_str = rich_formats.add_style(text=colon_str, style=colon_style)
        key = rich_formats.add_style(text=str(key), style=key_style)
        as_str = as_str + key + colon_str

    # construct value
    value = rich_formats.add_style(text=str(value), style=value_style)
    as_str = as_str + value

    # add indent
    if indent is not None:
        indent = positional_formats.indent_to_str(indent)
        as_str = indent + as_str

    return as_str


@functools.wraps(create_bullet_str)
def print_bullet(*args: typing.Any, **kwargs: typing.Any) -> None:
    as_str = create_bullet_str(*args, **kwargs)
    rich_formats.print(as_str)
