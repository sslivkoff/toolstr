from __future__ import annotations

import typing
from typing_extensions import Literal


def draw_line(
    row_start: int,
    column_start: int,
    row_end: int,
    column_end: int,
    backend: Literal['c', 'python'] | None = None,
) -> tuple[typing.Sequence[int], typing.Sequence[int]]:
    """draw a line in a grid of pixels

    if available will use skimage for better performance
    """

    # determine backend
    if backend is None:
        try:
            import skimage.draw  # type: ignore

            backend = 'c'
        except ImportError:
            backend = 'python'

    # draw line
    if backend == 'c':
        return skimage.draw.line(  # type: ignore
            row_start,
            column_start,
            row_end,
            column_end,
        )
    elif backend == 'python':
        return draw_line_python(
            row_start,
            column_start,
            row_end,
            column_end,
        )
    else:
        raise Exception('unknown backend: ' + str(backend))


def draw_line_python(
    r0: int,
    c0: int,
    r1: int,
    c1: int,
) -> tuple[typing.Sequence[int], typing.Sequence[int]]:
    """python implementation of line drawing algorithm

    adapted from skimage._draw._line
    see https://github.com/scikit-image/scikit-image/blob/a9f13618a94f421926e3b002f70b88df7e68469d/skimage/draw/_draw.pyx#L44
    """

    import numpy as np

    steep = 0
    r = r0
    c = c0
    dr = abs(r1 - r0)
    dc = abs(c1 - c0)

    rr: typing.MutableSequence[int] = np.zeros(max(dc, dr) + 1, dtype=np.int64)  # type: ignore
    cc: typing.MutableSequence[int] = np.zeros(max(dc, dr) + 1, dtype=np.int64)  # type: ignore

    if (c1 - c) > 0:
        sc = 1
    else:
        sc = -1
    if (r1 - r) > 0:
        sr = 1
    else:
        sr = -1
    if dr > dc:
        steep = 1
        c, r = r, c
        dc, dr = dr, dc
        sc, sr = sr, sc
    d = (2 * dr) - dc

    for i in range(dc):
        if steep:
            rr[i] = c
            cc[i] = r
        else:
            rr[i] = r
            cc[i] = c
        while d >= 0:
            r = r + sr
            d = d - (2 * dc)
        c = c + sc
        d = d + (2 * dr)

    rr[dc] = r1
    cc[dc] = c1

    return rr, cc
