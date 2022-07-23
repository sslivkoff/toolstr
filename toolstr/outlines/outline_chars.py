from __future__ import annotations

import typing
from typing_extensions import TypedDict

from .. import spec


class BorderCharsKwargs(TypedDict, total=False):
    thick: typing.Optional[bool]
    double: typing.Optional[bool]
    dashes: typing.Optional[int]
    ascii: typing.Optional[bool]
    double_horizontal: typing.Optional[bool]
    double_vertical: typing.Optional[bool]
    thick_horizontal: typing.Optional[bool]
    thick_vertical: typing.Optional[bool]
    rounded: typing.Optional[bool]
    style: str | None


def get_border_chars_by_name(name: str) -> spec.BorderChars:

    category_keys = {
        'thick',
        'double',
        'dashes',
        'ascii',
        'double_horizontal',
        'double_vertical',
        'thick_horizontal',
        'thick_vertical',
        'rounded',
    }

    styles = []
    kwargs: BorderCharsKwargs = {}
    for key in name.split(' '):
        if key in category_keys:
            kwargs[key] = True  # type: ignore
        else:
            styles.append(key)

    if len(styles) > 0:
        kwargs['style'] = ' '.join(styles)

    return get_border_chars(**kwargs)


def get_border_chars(
    thick: typing.Optional[bool] = None,
    double: typing.Optional[bool] = None,
    dashes: typing.Optional[int] = None,
    ascii: typing.Optional[bool] = None,
    double_horizontal: typing.Optional[bool] = None,
    double_vertical: typing.Optional[bool] = None,
    thick_horizontal: typing.Optional[bool] = None,
    thick_vertical: typing.Optional[bool] = None,
    rounded: typing.Optional[bool] = None,
    style: str | None = None,
) -> spec.BorderChars:
    """
    TODO: rounded corners
    """

    # set defaults
    if thick is None:
        thick = thick_horizontal and thick_vertical
    if double is None:
        double = double_horizontal and double_vertical
    if dashes is None:
        dashes = 0
    if ascii is None:
        ascii = False

    # validate parameters
    if (
        (double_horizontal and thick_horizontal)
        or (double_horizontal and thick_vertical)
        or (double_vertical and thick_horizontal)
        or (double_vertical and thick_vertical)
    ):
        raise Exception('cannot mix horizontal/vertical split styles')
    mixed = (
        double_horizontal
        or double_vertical
        or thick_horizontal
        or thick_vertical
    )

    if ascii:
        border_style: spec.BorderChars = {
            'horizontal': '-',
            'vertical': '|',
            'upper_left': '-',
            'upper_right': '-',
            'lower_left': '-',
            'lower_right': '-',
            'cross': '+',
            'upper_t': '-',
            'lower_t': '-',
            'left_t': '|',
            'right_t': '|',
        }
    elif (not thick) and (not double) and (dashes == 0) and not mixed:
        border_style = {
            'horizontal': '─',
            'vertical': '│',
            'upper_left': '┌',
            'upper_right': '┐',
            'lower_left': '└',
            'lower_right': '┘',
            'cross': '┼',
            'upper_t': '┬',
            'lower_t': '┴',
            'left_t': '├',
            'right_t': '┤',
        }
    elif (not thick) and double and (dashes == 0) and not mixed:
        border_style = {
            'horizontal': '═',
            'vertical': '║',
            'upper_left': '╔',
            'upper_right': '╗',
            'lower_left': '╚',
            'lower_right': '╝',
            'cross': '╬',
            'upper_t': '╦',
            'lower_t': '╩',
            'left_t': '╠',
            'right_t': '╣',
        }
    elif thick and (not double) and (dashes == 0) and not mixed:
        border_style = {
            'horizontal': '━',
            'vertical': '┃',
            'upper_left': '┏',
            'upper_right': '┓',
            'lower_left': '┗',
            'lower_right': '┛',
            'cross': '╋',
            'upper_t': '┳',
            'lower_t': '┻',
            'left_t': '┣',
            'right_t': '┫',
        }
    elif (not thick) and (not double) and dashes == 2 and not mixed:
        border_style = {
            'horizontal': '╌',
            'vertical': '╎',
            'upper_left': '┌',
            'upper_right': '┐',
            'lower_left': '└',
            'lower_right': '┘',
            'cross': '┼',
            'upper_t': '┬',
            'lower_t': '┴',
            'left_t': '├',
            'right_t': '┤',
        }
    elif thick and (not double) and dashes == 2 and not mixed:
        border_style = {
            'horizontal': '╍',
            'vertical': '╏',
            'upper_left': '┏',
            'upper_right': '┓',
            'lower_left': '┗',
            'lower_right': '┛',
            'cross': '╋',
            'upper_t': '┳',
            'lower_t': '┻',
            'left_t': '┣',
            'right_t': '┫',
        }
    elif (not thick) and (not double) and dashes == 3 and not mixed:
        border_style = {
            'horizontal': '┄',
            'vertical': '┆',
            'upper_left': '┌',
            'upper_right': '┐',
            'lower_left': '└',
            'lower_right': '┘',
            'cross': '┼',
            'upper_t': '┬',
            'lower_t': '┴',
            'left_t': '├',
            'right_t': '┤',
        }
    elif thick and (not double) and dashes == 3 and not mixed:
        border_style = {
            'horizontal': '┅',
            'vertical': '┇',
            'upper_left': '┏',
            'upper_right': '┓',
            'lower_left': '┗',
            'lower_right': '┛',
            'cross': '╋',
            'upper_t': '┳',
            'lower_t': '┻',
            'left_t': '┣',
            'right_t': '┫',
        }
    elif (not thick) and (not double) and dashes == 3 and not mixed:
        border_style = {
            'horizontal': '┈',
            'vertical': '┊',
            'upper_left': '┌',
            'upper_right': '┐',
            'lower_left': '└',
            'lower_right': '┘',
            'cross': '┼',
            'upper_t': '┬',
            'lower_t': '┴',
            'left_t': '├',
            'right_t': '┤',
        }
    elif thick and (not double) and dashes == 3 and not mixed:
        border_style = {
            'horizontal': '┉',
            'vertical': '┋',
            'upper_left': '┏',
            'upper_right': '┓',
            'lower_left': '┗',
            'lower_right': '┛',
            'cross': '╋',
            'upper_t': '┳',
            'lower_t': '┻',
            'left_t': '┣',
            'right_t': '┫',
        }
    elif thick_horizontal and (not double) and dashes == 0:
        border_style = {
            'horizontal': '━',
            'vertical': '│',
            'upper_left': '┍',
            'upper_right': '┑',
            'lower_left': '┕',
            'lower_right': '┙',
            'cross': '┿',
            'upper_t': '┯',
            'lower_t': '┷',
            'left_t': '┝',
            'right_t': '┥',
        }
    elif thick_vertical and (not double) and dashes == 0:
        border_style = {
            'horizontal': '─',
            'vertical': '┃',
            'upper_left': '┎',
            'upper_right': '┒',
            'lower_left': '┖',
            'lower_right': '┚',
            'cross': '╂',
            'upper_t': '┰',
            'lower_t': '┸',
            'left_t': '┠',
            'right_t': '┨',
        }
    elif (not thick) and double_horizontal and dashes == 0:
        border_style = {
            'horizontal': '═',
            'vertical': '│',
            'upper_left': '╒',
            'upper_right': '╕',
            'lower_left': '╘',
            'lower_right': '╛',
            'cross': '╪',
            'upper_t': '╤',
            'lower_t': '╧',
            'left_t': '╞',
            'right_t': '╡',
        }
    elif (not thick) and double_vertical and dashes == 0:
        border_style = {
            'horizontal': '─',
            'vertical': '║',
            'upper_left': '╓',
            'upper_right': '╖',
            'lower_left': '╙',
            'lower_right': '╜',
            'cross': '╫',
            'upper_t': '╥',
            'lower_t': '╨',
            'left_t': '╟',
            'right_t': '╢',
        }
    else:
        raise Exception('could not find specified borders')

    if rounded:
        border_style['upper_left'] = '╭'
        border_style['upper_right'] = '╮'
        border_style['lower_left'] = '╰'
        border_style['lower_right'] = '╯'

    if style:
        border_style = {  # type: ignore
            key: '['
            + style
            + ']'
            + typing.cast(str, value)
            + '[/'
            + style
            + ']'
            for key, value in border_style.items()
        }

    return border_style
