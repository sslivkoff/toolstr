from __future__ import annotations

import typing

from .. import indents


def print(
    *text: typing.Any,
    style: typing.Optional[str] = None,
    indent: str | int | None = None,
    **rich_kwargs: typing.Any,
) -> None:
    import rich.console
    import rich.theme

    if indent is not None:
        text = (indents.indent_block(str(text[0]), indent=indent),) + tuple(
            text[1:]
        )

    console = rich.console.Console(
        theme=rich.theme.Theme(inherit=False),
    )
    console.print(*text, style=style, **rich_kwargs)


def add_style(text: str, style: str | None) -> str:
    if style is None:
        return text
    else:
        return '[' + style + ']' + text + '[/' + style + ']'
