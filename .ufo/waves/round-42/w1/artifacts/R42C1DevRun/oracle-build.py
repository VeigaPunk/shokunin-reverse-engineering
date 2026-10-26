#!/usr/bin/env python3
"""R42C1DevRun oracle builder.

Given a SquashFS v3 listing from sasquatch -lls and the tree extracted by
sasquatch into a directory, emit:

  oracle-regular.tsv    relpath TAB sha256 TAB size  (regular files)
  oracle-nonregular.tsv relpath TAB kind TAB detail  (dir|symlink|char-device|
                        block-device|fifo|socket; detail = link target, or
                        maj:min for devices, else empty)
  oracle-list-7z.tsv    relpath TAB size TAB attr   (from 7z l, cross-check)

Usage: oracle-build.py --lls LLS --extracted DIR --out OUTFILE_STEM
        [--7z-list FILE]
"""
import argparse
import hashlib
import os
import re
import sys

LINE_RE = re.compile(
    r"^(?P<mode>[a-z-][rwxst-]{9}) (?P<owner>\S+/\S+) +"
    r"(?P<size>\d+|\d+,\s*\d+) (?P<mtime>\d{4}-\d\d-\d\d \d\d:\d\d) "
    r"(?P<name>\S+(?: \S+)*?)(?: -> (?P<target>.*))?$"
)


def parse_lls(path):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            m = LINE_RE.match(line)
            if not m:
                continue
            mode_s = m.group("mode")
            kind = mode_s[0]
            size_s = m.group("size")
            if "," in size_s:
                size = None
                detail = size_s.replace(" ", "")
            else:
                size = int(size_s)
                detail = ""
            name = m.group("name")
            if name.startswith("squashfs-root"):
                rel = name[len("squashfs-root"):].lstrip("/")
            else:
                rel = name.lstrip("/")
            if m.group("target") is not None:
                detail = m.group("target")
            rows.append((rel, kind, size, detail))
    return rows


def kind_of(mode_char):
    return {
        "d": "dir",
        "l": "symlink",
        "c": "char-device",
        "b": "block-device",
        "p": "fifo",
        "s": "socket",
        "-": "file",
    }.get(mode_char, mode_char)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lls", required=True)
    ap.add_argument("--extracted", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--7z-list")
    args = ap.parse_args()

    rows = parse_lls(args.lls)
    regular = []
    nonregular = []
    for rel, kind, size, detail in rows:
        if rel == "":
            continue  # root dir
        k = kind_of(kind)
        if k == "file":
            regular.append((rel, size))
        else:
            nonregular.append((rel, k, detail))

    reg_out = []
    for rel, size in regular:
        full = os.path.join(args.extracted, rel)
        try:
            with open(full, "rb") as fh:
                digest = hashlib.sha256(fh.read()).hexdigest()
        except OSError as e:
            digest = f"ERROR:{e}"
        reg_out.append((rel, digest, size))

    with open(args.out + "-regular.tsv", "w", encoding="utf-8") as fh:
        for rel, digest, size in sorted(reg_out):
            fh.write(f"{rel}\t{digest}\t{size}\n")
    with open(args.out + "-nonregular.tsv", "w", encoding="utf-8") as fh:
        for rel, k, detail in sorted(nonregular):
            fh.write(f"{rel}\t{k}\t{detail}\n")

    if getattr(args, "7z_list"):
        # 7z l -slt block format: "Path = ..." / "Folder = +|-" /
        # "Size = N" / "Mode = drwxr-xr-x" ...
        records = []
        cur = None
        with open(getattr(args, "7z_list"), encoding="utf-8", errors="replace") as z:
            for raw in z:
                line = raw.rstrip("\n")
                if line.startswith("Path = "):
                    if cur is not None:
                        records.append(cur)
                    cur = {"path": line[len("Path = "):]}
                elif cur is not None:
                    if line.startswith("Folder = "):
                        cur["folder"] = line[len("Folder = "):].strip()
                    elif line.startswith("Size = "):
                        cur["size"] = line[len("Size = "):].strip()
                    elif line.startswith("Mode = "):
                        cur["mode"] = line[len("Mode = "):].strip()
        if cur is not None:
            records.append(cur)
        with open(args.out + "-list-7z.tsv", "w", encoding="utf-8") as fh:
            for r in records:
                mode = r.get("mode", "")
                size = r.get("size", "")
                kind = mode[0] if mode else ("dir" if r.get("folder") == "+" else "")
                fh.write(f"{r['path']}\t{size}\t{kind}\n")
        print(f"7z records={len(records)}")
    print(f"rows={len(rows)} regular={len(regular)} "
          f"nonregular={len(nonregular)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
