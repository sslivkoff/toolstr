from __future__ import annotations

import typing


def print(
    *text: str, style: typing.Optional[str] = None, **rich_kwargs: typing.Any
) -> None:
    import rich.console
    import rich.theme

    console = rich.console.Console(
        theme=rich.theme.Theme(inherit=False),
    )
    console.print(*text, style=style, **rich_kwargs)


def add_style(text: str, style: str | None) -> str:
    if style is None:
        return text
    else:
        return '[' + style + ']' + text + '[/' + style + ']'
