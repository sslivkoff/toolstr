from __future__ import annotations

import typing

from .. import formats
from .. import indents
from .. import spec
from . import outline_chars


def print_outlined_text(
    text: str,
    width: typing.Optional[int] = None,
    justify: typing.Optional[spec.HorizontalJustification] = None,
    upper_border: typing.Optional[bool] = None,
    lower_border: typing.Optional[bool] = None,
    left_border: typing.Optional[bool] = None,
    right_border: typing.Optional[bool] = None,
    pad: typing.Optional[int] = None,
    upper_pad: typing.Optional[int] = None,
    lower_pad: typing.Optional[int] = None,
    left_pad: typing.Optional[int] = None,
    right_pad: typing.Optional[int] = None,
    style: str | None = None,
    indent: str | int | None = None,
    **border_style: typing.Any,
) -> None:

    string = get_outlined_text(
        text=text,
        width=width,
        justify=justify,
        upper_border=upper_border,
        lower_border=lower_border,
        left_border=left_border,
        right_border=right_border,
        pad=pad,
        upper_pad=upper_pad,
        lower_pad=lower_pad,
        left_pad=left_pad,
        right_pad=right_pad,
        style=style,
        **border_style,
    )

    if indent is not None:
        string = indents.indent_block(block=string, indent=indent)

    if style is not None:
        formats.print(string)
    else:
        print(string)


def print_text_box(
    text: str,
    width: typing.Optional[int] = None,
    justify: typing.Optional[spec.HorizontalJustification] = None,
    upper_pad: int = 0,
    lower_pad: int = 0,
    left_pad: int = 1,
    right_pad: int = 1,
    style: str | None = None,
    **border_style: typing.Any,
) -> None:
    print_outlined_text(
        text,
        width=width,
        justify=justify,
        upper_border=True,
        lower_border=True,
        left_border=True,
        right_border=True,
        upper_pad=upper_pad,
        lower_pad=lower_pad,
        left_pad=left_pad,
        right_pad=right_pad,
        style=style,
        **border_style,
    )


def print_header(
    text: str,
    width: typing.Optional[int] = None,
    justify: typing.Optional[spec.HorizontalJustification] = None,
    pad: int = 0,
    style: str | None = None,
    **border_style: typing.Any,
) -> None:
    print_outlined_text(
        text,
        width=width,
        justify=justify,
        pad=pad,
        upper_border=False,
        lower_border=True,
        left_border=False,
        right_border=False,
        style=style,
        **border_style,
    )


def get_outlined_text(
    text: str,
    width: typing.Optional[int] = None,
    justify: typing.Optional[spec.HorizontalJustification] = None,
    upper_border: typing.Optional[bool] = None,
    lower_border: typing.Optional[bool] = None,
    left_border: typing.Optional[bool] = None,
    right_border: typing.Optional[bool] = None,
    pad: typing.Optional[int] = None,
    upper_pad: typing.Optional[int] = None,
    lower_pad: typing.Optional[int] = None,
    left_pad: typing.Optional[int] = None,
    right_pad: typing.Optional[int] = None,
    style: str | None = None,
    **border_style: typing.Any,
) -> str:

    # set defaults
    if justify is None:
        justify = 'left'

    text_lines = text.split('\n')

    # process padding
    if pad is not None:
        if upper_pad is None:
            upper_pad = pad
        if lower_pad is None:
            lower_pad = pad
        if left_pad is None:
            left_pad = pad
        if right_pad is None:
            right_pad = pad
    if left_pad is None:
        left_pad = 0
    if right_pad is None:
        right_pad = 0
    left_pad_str = left_pad * ' '
    right_pad_str = right_pad * ' '
    if upper_pad is not None:
        text_lines = [''] * upper_pad + text_lines
    if lower_pad is not None:
        text_lines = text_lines + [''] * lower_pad

    # compute widths
    if left_border and right_border:
        border_width = 2
    elif left_border or right_border:
        border_width = 1
    else:
        border_width = 0
    pad_width = left_pad + right_pad
    if width is None:
        max_line_width = max(len(line) for line in text_lines)
        width = border_width + pad_width + max_line_width
    text_width = width - border_width - pad_width

    # get border chars
    border_chars = outline_chars.get_border_chars(**border_style)

    # set line prefixes and postfixes
    if left_border:
        upper_left_prefix = border_chars['upper_left']
        middle_left_prefix = border_chars['vertical']
        lower_left_prefix = border_chars['lower_left']
    else:
        upper_left_prefix = ''
        middle_left_prefix = ''
        lower_left_prefix = ''
    if right_border:
        upper_right_postfix = border_chars['upper_right']
        middle_right_postfix = border_chars['vertical']
        lower_right_postfix = border_chars['lower_right']
    else:
        upper_right_postfix = ''
        middle_right_postfix = ''
        lower_right_postfix = ''

    # add upper border
    outlined = ''
    if upper_border:
        outlined = (
            upper_left_prefix
            + (text_width + pad_width) * border_chars['horizontal']
            + upper_right_postfix
            + '\n'
        )

    # add text
    for line in text_lines:
        if len(line) > text_width:
            line = line[: text_width - 3] + '...'
        if justify == 'left':
            line = line.ljust(text_width)
        elif justify == 'right':
            line = line.rjust(text_width)
        elif justify == 'center':
            line = line.center(text_width)
        elif justify is not None:
            pass
        else:
            raise Exception('unknown justification: ' + str(justify))
        line = (
            middle_left_prefix
            + left_pad_str
            + line
            + right_pad_str
            + middle_right_postfix
        )
        line = line.rstrip()
        outlined += line + '\n'

    # add lower border
    if lower_border:
        outlined += (
            lower_left_prefix
            + (text_width + pad_width) * border_chars['horizontal']
            + lower_right_postfix
        )

    outlined = outlined.rstrip()

    if style is not None:
        outlined = formats.add_style(outlined, style)

    return outlined