#!/usr/bin/env python3
"""merge-mirror.py — build the scratch lane mirror and insert the normalized append block.

Mirror layout (mirror root == the lane root, so the census resolves used-by paths exactly
as it does for the real lane):
  <mirror>/corpus/...            copy of the lane corpus
  <mirror>/SKILL.md, <mirror>/tools/...  non-corpus used-by targets copied from the lane
  append rows inserted at the end of the `## Registry` table

Never writes into the lane: --lane is read-only, --mirror is wiped and rebuilt.
"""
import argparse
import os
import re
import shutil
import sys


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def registry_rows(text):
    """(id, url, scope, status, usedby) for each Registry table row."""
    out = []
    in_registry = False
    for line in text.splitlines():
        t = line.lstrip(" ")
        ind = len(line) - len(t)
        if ind <= 3 and t.startswith("## "):
            in_registry = t[3:].strip() == "Registry"
            continue
        if ind <= 3 and t.startswith("# "):
            in_registry = False
            continue
        if not in_registry or ind > 3 or not t.startswith("|"):
            continue
        body = t[1:]
        if body.endswith("|"):
            body = body[:-1]
        c = [x.strip() for x in body.split("|")]
        if len(c) < 11 or c[0] == "id":
            continue
        if all(re.fullmatch(r":?-+:?", x) for x in c if x):
            continue
        out.append((c[0], c[1], c[4], c[7], c[10]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--mirror", required=True)
    ap.add_argument("--block", default="", help="normalized append block (optional)")
    ap.add_argument("--place", nargs="*", default=[],
                    help="repo-relative knowledge files to place into the mirror (from --lane)")
    ap.add_argument("--place-pair", action="append", nargs=2, default=[],
                    metavar=("SRC", "REL"),
                    help="place SRC at REL inside the mirror (draft entries not yet in the lane)")
    args = ap.parse_args()

    lane = os.path.abspath(args.lane)
    mirror = os.path.abspath(args.mirror)
    if mirror == lane or mirror.startswith(lane + os.sep):
        print(f"refusing to build the mirror inside the lane: {mirror}", file=sys.stderr)
        return 2

    if os.path.isdir(mirror):
        shutil.rmtree(mirror)
    os.makedirs(mirror)
    shutil.copytree(os.path.join(lane, "corpus"), os.path.join(mirror, "corpus"),
                    symlinks=True)

    sources = os.path.join(mirror, "corpus", "SOURCES.md")
    text = read(sources)

    if args.block:
        block_rows = [ln.rstrip("\n") for ln in read(args.block).splitlines() if ln.strip()]
        lines = text.splitlines()
        # Insert directly before the next `## ` heading after `## Registry`.
        start = lines.index("## Registry")
        insert_at = len(lines)
        for i in range(start + 1, len(lines)):
            if lines[i].startswith("## "):
                insert_at = i
                break
        # Walk back over blank lines so the block stays inside the table.
        while insert_at > start + 1 and lines[insert_at - 1].strip() == "":
            insert_at -= 1
        lines[insert_at:insert_at] = block_rows
        text = "\n".join(lines) + "\n"
        with open(sources, "w", encoding="utf-8") as fh:
            fh.write(text)

    for src, rel in args.place_pair:
        if not os.path.exists(src):
            print(f"WARN place-pair source absent: {src}", file=sys.stderr)
            continue
        dst = os.path.join(mirror, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    for rel in args.place:
        src = os.path.join(lane, rel)
        if not os.path.exists(src):
            print(f"WARN place target absent in lane: {rel}", file=sys.stderr)
            continue
        dst = os.path.join(mirror, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    # Copy any used-by target the mirror still lacks, when the lane has it.
    copied = []
    for _id, _src, _scope, _status, usedby in registry_rows(text):
        for rel in (x.strip() for x in usedby.split(",")):
            if not rel or rel == "\u2014":
                continue
            dst = os.path.join(mirror, rel)
            if os.path.exists(dst):
                continue
            src = os.path.join(lane, rel)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                copied.append(rel)
            else:
                print(f"WARN used-by target absent in lane too: {rel}", file=sys.stderr)

    print(f"mirror={mirror}")
    print(f"registry_rows={len(registry_rows(text))}")
    print(f"extra_usedby_copied={copied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
