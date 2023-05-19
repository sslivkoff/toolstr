from __future__ import annotations

import contextlib


@contextlib.contextmanager
def write_stdout_to_file(path: str, mode: str = 'w') -> None:
    import sys
    import io

    output_buffer = io.StringIO()
    stdout = sys.stdout
    sys.stdout = output_buffer
    try:
        yield None
    finally:
        sys.stdout = stdout
        with open(path, mode) as f:
            f.write(output_buffer.getvalue())

