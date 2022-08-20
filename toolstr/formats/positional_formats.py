from __future__ import annotations

import typing

from .. import spec


def hjustify(
    text: str,
    justification: spec.HorizontalJustification,
    width: int,
) -> str:

    # account for rich formatting
    if '[' in text:
        import rich.text

        plain_width = rich.text.Text.from_markup(text).cell_len
        width += len(text) - plain_width

    if width < len(text):
        return text[:width]

    if justification == 'left':
        return text.ljust(width)
    elif justification == 'right':
        return text.rjust(width)
    elif justification == 'center':
        return text.center(width)
    elif justification == 'raw':
        return text[:width].ljust(width)
    else:
        raise Exception('unknown justification: ' + str(justification))


def vjustify(
    text: str,
    justification: spec.VerticalJustification,
    height: int,
) -> str:

    n_lines = text.count('\n') + 1

    # check if exceeds height
    if n_lines > height:
        return '\n'.join(text.split('\n')[:height])

    missing = height - n_lines
    if justification == 'top':
        return text + '\n' * missing
    elif justification == 'bottom':
        return '\n' * missing + text
    elif justification == 'center':
        top = int(missing / 2)
        bottom = missing - top
        return '\n' * top + text + '\n' * bottom
    else:
        raise Exception('unknown justification: ' + str(justification))


def concatenate_blocks(
    blocks: typing.Sequence[str | typing.Sequence[str]],
    *,
    gap: int | str | None = None,
) -> str:
    """concatenate blocks of text horizontally"""

    # split blocks into lines
    blocks_lines: typing.MutableSequence[typing.Sequence[str]] = []
    for block in blocks:
        if isinstance(block, str):
            blocks_lines.append(block.split('\n'))
        else:
            blocks_lines.append(block)
    n_lines = len(blocks_lines[0])
    for block_lines in blocks_lines:
        if len(block_lines) != n_lines:
            raise Exception(
                'every block needs to have the same number of lines'
            )

    if gap is None:
        gap = ''
    elif isinstance(gap, int):
        gap = ' ' * gap
    elif isinstance(gap, str):
        pass
    else:
        raise Exception('unknown gap format: ' + str(type(gap)))

    # concatenate into new lines
    new_lines = []
    for pieces in zip(*blocks_lines):
        new_lines.append(gap.join(pieces))

    return '\n'.join(new_lines)


def indent_block(block: str, indent: typing.Union[str, int, None]) -> str:
    indent = indent_to_str(indent)
    lines = block.split('\n')
    new_lines = [indent + line for line in lines]
    return '\n'.join(new_lines)


def indent_to_str(indent: typing.Union[str, int, None]) -> str:
    """convert input into an indent, whether a str or an int number of spaces

    useful for user facing functions with flexible input constraints
    """
    if indent is None:
        return ''
    elif isinstance(indent, int):
        return ' ' * indent
    elif isinstance(indent, str):
        return indent
    else:
        raise Exception('unknown indent format')
