from __future__ import annotations

import typing


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
