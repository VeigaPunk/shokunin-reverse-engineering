#!/usr/bin/env python3
"""VZ-3 cross-check: tool v2 receipt vs VZ-3's independent capture (read-only).

Usage: vz3-compare-receipt-vs-independent.py <tool-receipt> <independent-capture>

Compares, per path: sha256, size, inode, mtime_epoch, ctime_epoch. Exits 0 iff
every comparable field agrees on every path that appears in both files.
"""
import re
import sys


def parse_tool(path):
    text = open(path, encoding="utf-8").read()
    out = {}
    for part in re.split(r"^PATH:\s*", text, flags=re.M)[1:]:
        head, _, rest = part.partition("\n")
        p = head.strip()

        def g(key):
            m = re.search(r"^%s:\s*(\S+)\s*$" % key, rest, re.M)
            return m.group(1) if m else None

        out[p] = {
            "sha256": g("SHA256"),
            "size": g("SIZE"),
            "inode": g("INODE"),
            "mtime_epoch": g("MTIME_EPOCH"),
            "ctime_epoch": g("CTIME_EPOCH"),
            "mtime_utc_render": g("MTIME_UTC_RENDER"),
        }
    return out


def parse_independent(path):
    text = open(path, encoding="utf-8").read()
    out = {}
    for block in text.split("PATH: ")[1:]:
        lines = block.splitlines()
        p = lines[0].strip()
        d = {}
        for ln in lines[1:]:
            if ": " not in ln:
                continue
            k, _, v = ln.partition(": ")
            d[k.strip()] = v.strip()
        m = re.match(r"(\d+)\s+MODE:\s*(\S+)\s+INODE:\s*(\d+)", d.get("SIZE", ""))
        out[p] = {
            "sha256": d.get("SHA256"),
            "size": m.group(1) if m else None,
            "inode": m.group(3) if m else None,
            "mtime_epoch": d.get("MTIME_EPOCH"),
            "ctime_epoch": d.get("CTIME_EPOCH"),
            "mtime_utc_render": d.get("MTIME_UTC"),
        }
    return out


def main():
    tool = parse_tool(sys.argv[1])
    indep = parse_independent(sys.argv[2])
    keys = ("sha256", "size", "inode", "mtime_epoch", "ctime_epoch", "mtime_utc_render")
    rc = 0
    paths = set(tool) & set(indep)
    print("compared paths: %d (tool=%d indep=%d)" % (len(paths), len(tool), len(indep)))
    if len(paths) != len(tool) or len(paths) != len(indep):
        print("SET-MISMATCH: tool-only=%s indep-only=%s"
              % (sorted(set(tool) - set(indep)), sorted(set(indep) - set(tool))))
        rc = 1
    for p in sorted(paths):
        bad = [k for k in keys if tool[p].get(k) != indep[p].get(k)]
        if bad:
            rc = 1
            print("PATH %s: MISMATCH %s" % (p, ", ".join(
                "%s tool=%r indep=%r" % (k, tool[p].get(k), indep[p].get(k)) for k in bad)))
        else:
            print("PATH %s: AGREE (%d/%d fields)" % (p, len(keys), len(keys)))
    print("VZ3-CROSSCHECK: %s" % ("AGREE" if rc == 0 else "DISAGREE"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
