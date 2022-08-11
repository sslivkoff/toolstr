from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import tooltime

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
