#!/usr/bin/env python3
"""Round 29 pre-seen screen for frozen selector test sets (QUALITY row 44; mistake M28-4).

Reads committed bytes at --rev only. Two seen-sets, one per kind of answer:

  name_seen  (R29-C1; the answer is a function name): every 8-hex-digit token, with or without
             0x, that appears as a whole word in any tracked file at --rev (git grep over the whole
             tree, case-insensitive). This is deliberately wider than a lookup cache: a selector the
             lane ever wrote down beside a name is excluded.
  flag_seen  (R29-C2; the answer is openchain's `filtered` flag): every selector with a tracked
             openchain response at --rev: a file named openchain-[0x]<sel>[...].json, or any
             tracked .json whose body has result.function.<0xsel> (the openchain response shape).

--check <tsv> --kind name|flag: counts first-column selectors of the TSV (header skipped) that are
in the chosen seen-set. Exit 0 when none are, 1 otherwise; prints the overlap.
"""
import argparse
import json
import re
import subprocess
import sys

TOKEN = re.compile(r"\b(?:0[xX])?([0-9a-fA-F]{8})\b")
OC_NAME = re.compile(r"(?:^|/)openchain-(?:0x)?([0-9a-fA-F]{8})\b[^/]*\.json$")


def tracked(root, rev):
    out = subprocess.run(["git", "-C", root, "ls-tree", "-r", "--name-only", rev],
                         capture_output=True, text=True, check=True).stdout
    return [p for p in out.split("\n") if p]


def name_seen(root, rev):
    proc = subprocess.run(["git", "-C", root, "grep", "-I", "-h", "-o", "-i", "-w", "-E",
                           r"(0x)?[0-9a-f]{8}", rev, "--", "."], capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise SystemExit("git grep failed: %s" % proc.stderr.strip())
    seen = set()
    for line in proc.stdout.split("\n"):
        tok = line.split(":", 1)[-1].strip().lower()
        if tok.startswith("0x"):
            tok = tok[2:]
        if re.fullmatch(r"[0-9a-f]{8}", tok):
            seen.add(tok)
    return seen


def flag_seen(root, rev):
    paths = tracked(root, rev)
    seen = set()
    jsons = []
    for p in paths:
        m = OC_NAME.search(p)
        if m:
            seen.add(m.group(1).lower())
        if p.endswith(".json"):
            jsons.append(p)
    proc = subprocess.Popen(["git", "-C", root, "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    data, _ = proc.communicate("".join("%s:%s\n" % (rev, p) for p in jsons).encode())
    i = 0
    while i < len(data):
        nl = data.index(b"\n", i)
        head = data[i:nl].split()
        i = nl + 1
        if len(head) < 3 or head[1] != b"blob":
            continue
        size = int(head[2])
        body = data[i:i + size]
        i += size + 1
        if b'"function"' not in body:
            continue
        try:
            obj = json.loads(body)
        except ValueError:
            continue
        fn = obj.get("result", {}).get("function") if isinstance(obj, dict) and isinstance(obj.get("result"), dict) else None
        if isinstance(fn, dict):
            for k in fn:
                k = k.lower()
                if k.startswith("0x") and re.fullmatch(r"0x[0-9a-f]{8}", k):
                    seen.add(k[2:])
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--check", required=True)
    ap.add_argument("--kind", choices=["name", "flag"], required=True)
    a = ap.parse_args()
    seen = name_seen(a.root, a.rev) if a.kind == "name" else flag_seen(a.root, a.rev)
    sels = [l.split("\t")[0].lower() for l in open(a.check, encoding="utf-8").read().splitlines()[1:] if l]
    hit = [s for s in sels if s in seen]
    print("kind=%s rev=%s test_selectors=%d seen_set=%d overlap=%d %s" % (
        a.kind, a.rev, len(sels), len(seen), len(hit), " ".join(hit)))
    return 1 if hit else 0


if __name__ == "__main__":
    sys.exit(main())
