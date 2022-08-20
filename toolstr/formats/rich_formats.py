from __future__ import annotations

import typing

from . import positional_formats


def get_styled_width(text: str) -> int:
    import rich.text

    return rich.text.Text.from_markup(text).cell_len


def fit_styled_width(text: str, width: int, ellipses: bool = False) -> str:
    import rich.text

    if ellipses:
        width = width - 3

    fitted = rich.text.Text.from_markup(text).fit(width)[0].markup

    if ellipses:
        fitted = fitted + '...'

    return fitted


def print(
    *text: typing.Any,
    style: typing.Optional[str] = None,
    indent: str | int | None = None,
    **rich_kwargs: typing.Any,
) -> None:
    import rich.console
    import rich.theme

    if indent is not None:
        text = (positional_formats.indent_block(str(text[0]), indent=indent),) + tuple(
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
