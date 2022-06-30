from __future__ import annotations

import typing


def print(
    *text: str, style: typing.Optional[str] = None, **rich_kwargs: typing.Any
) -> None:
    import rich.console

    console = rich.console.Console()
    console.print(*text, style=style, **rich_kwargs)


def add_style(text: str, style: str) -> str:
    return '[' + style + ']' + text + '[/' + style + ']'
