"""Entry point for the news-image-20261125 make.fun entry.

The repository ships a finished poster, entry.png, that sums up the world
news of Wednesday 25 November 2026. This program copies those exact bytes
to the grader's output directory as entry.png, so the two grading runs
write identical files. Standard library only; no network.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    # Guard against a truncated copy: the judge must see the whole image.
    if target.stat().st_size != SOURCE.stat().st_size:
        raise IOError("copied entry.png is incomplete")


if __name__ == "__main__":
    main()
