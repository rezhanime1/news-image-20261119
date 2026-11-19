"""News-image entry for 19 November 2026: ship the rendered front page.

The front page (news.png) is drawn offline by render_frontpage.py and
bundled with this repository. This program only copies it to the output
path, so both grading runs write identical bytes. Standard library
only; it never touches the network.
"""

import os
import shutil
from pathlib import Path

ASSET_NAME = "news.png"
MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IEND_TAIL = b"IEND"


def _check_png(data: bytes) -> None:
    """Refuse anything that is not one whole 1024x1024 PNG under the gate."""
    if len(data) > MAX_BYTES:
        raise SystemExit(f"entry.png is {len(data)} bytes, over the 1 MiB gate")
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png does not start with the PNG signature")
    if IEND_TAIL not in data[-12:]:
        raise SystemExit("entry.png is truncated: no IEND chunk at the end")
    # IHDR follows the 8-byte signature: 4-byte length, "IHDR", then
    # width and height as big-endian uint32.
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, not 1024x1024")


def main() -> None:
    here = Path(__file__).resolve().parent
    asset = here / ASSET_NAME
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(asset, target)
    _check_png(target.read_bytes())
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
