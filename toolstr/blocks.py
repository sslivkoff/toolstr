from __future__ import annotations

import typing


def concatenate_blocks(blocks: typing.Sequence[str]) -> str:
    """concatenate blocks of text horizontally"""

    # split blocks into lines
    blocks_lines = [block.split('\n') for block in blocks]
    n_lines = len(blocks_lines[0])
    for block_lines in blocks_lines:
        if len(block_lines) != n_lines:
            raise Exception(
                'every block needs to have the same number of lines'
            )

    # concatenate into new lines
    new_lines = []
    for pieces in zip(*blocks_lines):
        new_lines.append(''.join(pieces))

    return '\n'.join(new_lines)
