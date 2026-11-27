#!/usr/bin/env python3
"""Entry point for the news-image bounty (2026-11-27 edition).

Finds the single PNG in this repository's root — entry.png, the
finished front page — copies it to /output/entry.png, and proves the
copy is stable by hashing the output twice and requiring both digests
to agree. Standard library only, so it runs in the grading sandbox
exactly as it runs here.
"""

import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    pngs = sorted(
        name for name in os.listdir(ROOT)
        if name.lower().endswith(".png")
        and os.path.isfile(os.path.join(ROOT, name))
    )
    if len(pngs) != 1:
        print("expected exactly one PNG in %s, found %d: %s"
              % (ROOT, len(pngs), pngs), file=sys.stderr)
        return 1
    source = os.path.join(ROOT, pngs[0])

    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(source, DEST)

    first = digest(DEST)
    shutil.copyfile(source, DEST)
    second = digest(DEST)
    if first != second:
        print("unstable output: %s != %s" % (first, second),
              file=sys.stderr)
        return 1

    size = os.path.getsize(DEST)
    print("entry.png sha256: %s" % first)
    print("entry.png bytes: %d" % size)
    if size > 1024 * 1024:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    print("ok: deterministic copy verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
