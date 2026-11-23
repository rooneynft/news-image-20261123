#!/usr/bin/env python3
"""Place the finished front page into the output directory.

The renderer has already produced entry.png in the repository root.
This entrypoint only moves that file where the grader expects it.
"""

import os
import shutil
import sys
from pathlib import Path


def emit_front_page(destination: Path) -> Path:
    """Copy entry.png into destination and return the copied path."""
    destination.mkdir(parents=True, exist_ok=True)
    rendered = Path(__file__).resolve().parent / "entry.png"
    placed = destination / "entry.png"
    shutil.copyfile(rendered, placed)
    return placed


def main() -> None:
    env_out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_out:
        out_dir = Path(env_out)
    elif len(sys.argv) > 1:
        out_dir = Path(sys.argv[1])
    else:
        out_dir = Path("out")
    emit_front_page(out_dir)


if __name__ == "__main__":
    main()
