#!/usr/bin/env python3
"""Build the README art for write-without-ai-slop: paper and a red pen.

Usage:
    python3 .github/readme/make_art.py            write every SVG in this folder
    python3 .github/readme/make_art.py --check    exit 1 if the files on disk differ from a fresh build

Standard library only. The output is deterministic, so --check can run in CI.
The art holds no version or test counts, so it never goes stale when those change.
The text and the pen strokes are positioned with textLength, so they line up in any font.
"""
import sys
from pathlib import Path
from artlib import *
from scenes import SCENES
from story import STORY
from demo import demo

HERE = Path(__file__).resolve().parent

ART = (("hero", SCENES[0][1]), ("tryit", STORY[0][1]), ("demo", demo), ("robots", STORY[1][1]), ("zoo", SCENES[1][1]), ("results", STORY[2][1]))


def main(argv):
    built = {f"{name}.svg": fn() for name, fn in ART}
    if "--check" in argv:
        stale = [n for n, text in built.items() if not (HERE / n).exists() or (HERE / n).read_text(encoding="utf-8") != text]
        for n in stale:
            print(f"{n} differs from a fresh build; run make_art.py")
        return 1 if stale else 0
    for n, text in built.items():
        (HERE / n).write_text(text, encoding="utf-8")
        print(n, len(text.encode("utf-8")), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
