from __future__ import annotations

import typing

from . import positional_formats

if typing.TYPE_CHECKING:
    import typing_extensions

    RichColorSystem = typing_extensions.Literal[
        None,
        'auto',
        'standard',
        '256',
        'truecolor',
        'windows',
    ]

    class _FormatDefaults(typing.TypedDict):
        color_system: RichColorSystem


_format_defaults: _FormatDefaults = {'color_system': None}


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


def set_default_color_system(color_system: RichColorSystem) -> None:
    _format_defaults['color_system'] = color_system


def print(
    *text: typing.Any,
    style: typing.Optional[str] = None,
    indent: str | int | None = None,
    color_system: RichColorSystem = None,
    **rich_kwargs: typing.Any,
) -> None:
    import rich.console
    import rich.theme

    if indent is not None:
        text = (
            positional_formats.indent_block(str(text[0]), indent=indent),
        ) + tuple(text[1:])

    if color_system is None:
        color_system = _format_defaults['color_system']

    if color_system is not None:
        kwargs = {'color_system': color_system}
    else:
        kwargs = {}
    console = rich.console.Console(
        theme=rich.theme.Theme(inherit=False),
        **kwargs,  # type: ignore
    )
    console.print(*text, style=style, **rich_kwargs)


def add_style(text: str, style: str | None, *, per_line: bool = False) -> str:
    if style is None or style == '':
        return text
    else:
        if per_line and '\n' in text:
            lines = text.split('\n')
            styled_lines = [
                add_style(line, style, per_line=False) for line in lines
            ]
            return '\n'.join(styled_lines)

        else:
            return '[' + style + ']' + text + '[/' + style + ']'
