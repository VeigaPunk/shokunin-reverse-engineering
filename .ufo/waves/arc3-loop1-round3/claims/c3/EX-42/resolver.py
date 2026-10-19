#!/usr/bin/env python3
"""EX-42 census resolution pass: resolve every A-row stated line/range at HEAD,
and locate every B-row file target (basename or path) in the committed tree."""
import re
import subprocess
import os
import json

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "HEAD"


def git(*args):
    p = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def blob_lines(path):
    rc, out = git("show", "%s:%s" % (REV, path))
    if rc != 0:
        return None
    return out.splitlines()


def main():
    rows = []
    with open("/var/tmp/ex42-census/citations2.tsv") as fh:
        next(fh)
        for ln in fh:
            commit, citing, hl, kind, token = ln.rstrip("\n").split("\t")
            rows.append(dict(commit=commit, citing=citing, head_line=hl, kind=kind, token=token))

    # A rows: resolve
    print("### A rows — stated line/range resolution at HEAD")
    for r in rows:
        if r["kind"] != "A":
            continue
        m = re.match(r"(.+?):(\d+)(?:-(\d+))?$", r["token"])
        target, lo = m.group(1), int(m.group(2))
        hi = int(m.group(3)) if m.group(3) else lo
        lines = blob_lines(target)
        if lines is None:
            print("MISSING\t%s -> %s" % (r["citing"], r["token"]))
            continue
        n = len(lines)
        state = "OK" if 1 <= lo <= hi <= n else "OUT-OF-RANGE"
        print("%s\t%s citing %s (%d lines)\t%s" % (state, r["citing"] + ":" + str(r["head_line"]),
                                                   r["token"], n, r["token"]))
        for i in range(lo, min(hi, n) + 1):
            print("      %d| %s" % (i, lines[i - 1][:170]))
    print()
    print("### B rows — target location in tree at HEAD")
    uniq = {}
    for r in rows:
        if r["kind"] != "B":
            continue
        uniq.setdefault(r["token"], []).append("%s:%s" % (r["citing"], r["head_line"]))
    for tok, cites in sorted(uniq.items()):
        if tok.startswith("."):
            rc, out = git("cat-file", "-e", "%s:%s" % (REV, tok[2:] if tok.startswith("./") else tok))
            print(("EXISTS " if rc == 0 else "ABSENT ") + tok + "  <- " + ",".join(cites[:4]))
        elif "/" in tok:
            rc, out = git("cat-file", "-e", "%s:%s" % (REV, tok))
            print(("EXISTS " if rc == 0 else "ABSENT ") + tok + "  <- " + ",".join(cites[:4]))
        else:
            rc, out = git("ls-tree", "-r", "--name-only", REV)
            hits = [p for p in out.splitlines() if os.path.basename(p) == tok]
            print(("FOUND(%d) " % len(hits)) + tok + "  -> " + ";".join(hits[:3]) + "  <- " + ",".join(cites[:3]))


if __name__ == "__main__":
    main()