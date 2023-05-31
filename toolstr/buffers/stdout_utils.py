from __future__ import annotations

import contextlib


@contextlib.contextmanager
def write_stdout_to_file(
    path: str,
    mode: str = 'w',
    create_dir: bool = True,
) -> None:
    import io
    import os
    import sys

    if create_dir:
        os.makedirs(os.path.dirname(path), exist_ok=True)

    output_buffer = io.StringIO()
    stdout = sys.stdout
    sys.stdout = output_buffer
    try:
        yield None
    finally:
        sys.stdout = stdout
        with open(path, mode) as f:
            f.write(output_buffer.getvalue())

