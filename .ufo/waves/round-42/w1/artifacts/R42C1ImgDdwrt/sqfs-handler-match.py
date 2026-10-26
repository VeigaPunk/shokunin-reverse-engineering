#!/usr/bin/env python3
"""Match unblob 26.6.4 SquashFS handler PATTERNS against bytes of an image.

Patterns are taken mechanically from the installed handler source, not retyped:
each PATTERNS block's HexString hex-token line (the one that is not a comment
line) is turned into a regex, with [N] becoming N wildcard bytes.

Usage: sqfs-handler-match.py <handler.py> <image> [more images...]
Reads bytes only; no extractor, no carving.
"""
import re
import sys

TOKEN = re.compile(r"\[(\d+)\]|([0-9A-Fa-f]{2})")


def handlers_from_source(path):
    src = open(path, encoding="utf-8").read()
    out = []
    # split on top-level class definitions
    for block in re.split(r"(?m)^class ", src)[1:]:
        name_m = re.search(r'NAME = "([^"]+)"', block)
        if not name_m:
            continue
        pats = []
        for hs in re.finditer(r'HexString\(\s*"""(.*?)"""', block, re.S):
            for line in hs.group(1).splitlines():
                s = line.strip()
                if not s or s.startswith("//"):
                    continue
                toks = TOKEN.findall(s)
                if not toks:
                    continue
                parts = []
                for wild, byte in toks:
                    parts.append(b"." * int(wild) if wild else re.escape(bytes([int(byte, 16)])))
                pats.append(b"".join(parts))
        if pats:
            out.append((name_m.group(1), pats))
    return out


def scan(data, pats, limit=8):
    hits = []
    for p in pats:
        # patterns anchor at the candidate offset: search all positions
        for m in re.finditer(b"(?=" + p + b")", data, re.S):
            hits.append(m.start())
            if len(hits) >= limit:
                return hits
    return hits


if __name__ == "__main__":
    handlers = handlers_from_source(sys.argv[1])
    print("handlers parsed:", len(handlers))
    for name, pats in handlers:
        print(f"  {name}: {len(pats)} pattern(s)")
    for img in sys.argv[2:]:
        data = open(img, "rb").read()
        print(f"\n== {img} ({len(data)} bytes)")
        for name, pats in handlers:
            h = scan(data, pats)
            if h:
                print(f"  MATCH {name} at {h}")
