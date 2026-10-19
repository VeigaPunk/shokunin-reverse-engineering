#!/usr/bin/env python3
"""EX-03 self-identity claim scanner (round-2 c1 adversary-executor seat).

Purpose: decide, by measurement, whether the drafted queue-drain rule #14
("an artifact that records its own byte-identity must re-derive it after every
revision") is *enforceable* — i.e. whether a mechanical checker can detect the
stale/mismatched class — and how large the class is in the round-1 wave.

Unit of measurement, stated explicitly:
  A file "carries a self-bound identity" iff it contains a 64-hex sha256 token
  that equals the sha256 of the file itself (read-only, no writes).
  A file "carries an identity-block claim" iff some line matches
  <int> bytes [..] <int> lines  (the EX-12 canonical form, optional commas).
  Reading: an identity block is 'self' when the accompanying sha256 token on
  the block (or within +/-2 lines) equals the file's own hash, 'other' when it
  matches some other file's hash under the scanned root, 'unknown' otherwise.

Usage: selfid-probe.py [--json] ROOT...
"""
import hashlib
import json
import os
import re
import sys

SHA_RE = re.compile(r"\b([0-9a-f]{64})\b")
BLOCK_RE = re.compile(
    r"([\d,]+)\s*bytes?[^\n]{0,40}?([\d,]+)\s*lines?", re.IGNORECASE)
INT_RE = re.compile(r"([\d,]+)")


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # skip caches and binary blobs
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "node_modules")]
        for name in filenames:
            yield os.path.join(dirpath, name)


def num(tok):
    digits = tok.replace(",", "")
    return int(digits) if digits.isdigit() else -1


def scan(path):
    try:
        raw = open(path, "rb").read()
    except OSError as exc:
        return {"path": path, "error": str(exc)}
    if b"\x00" in raw[:8192]:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    own = hashlib.sha256(raw).hexdigest()
    lines = text.splitlines()
    shas = []
    for i, line in enumerate(lines, 1):
        for m in SHA_RE.finditer(line):
            shas.append((i, m.group(1)))
    self_bound = [s for (_, s) in shas if s == own]
    self_prefix = [s for (_, s) in shas if s != own and own.startswith(s[:8])]
    blocks = []
    for i, line in enumerate(lines, 1):
        m = BLOCK_RE.search(line)
        if not m:
            continue
        size, nlines = num(m.group(1)), num(m.group(2))
        near = [s for (ln, s) in shas if abs(ln - i) <= 2]
        blocks.append({
            "line": i,
            "claim_size": size,
            "claim_lines": nlines,
            "size_matches_file": size == len(raw),
            "lines_matches_file": nlines == len(lines),
            "size_anywhere_in_file_other": None,
            "sha_near": [s[:12] for s in near],
            "sha_near_self": any(s == own for s in near),
        })
    return {
        "path": path,
        "size": len(raw),
        "lines": len(lines),
        "own_sha_prefix": own[:12],
        "sha_tokens": len(shas),
        "self_bound_tokens": [s[:12] for s in self_bound],
        "own_prefix_tokens": [s[:12] for s in self_prefix],
        "identity_blocks": blocks,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    rows = []
    for root in args:
        for path in sorted(walk(root)):
            row = scan(path)
            if row:
                rows.append(row)
    summary = {
        "files_scanned": len(rows),
        "files_with_self_bound_sha": sum(1 for r in rows if r.get("self_bound_tokens")),
        "files_with_identity_block": sum(1 for r in rows if r.get("identity_blocks")),
        "identity_blocks_total": sum(len(r.get("identity_blocks") or []) for r in rows),
        "blocks_size_mismatch": sum(
            1 for r in rows for b in (r.get("identity_blocks") or [])
            if not b["size_matches_file"]),
        "blocks_lines_mismatch": sum(
            1 for r in rows for b in (r.get("identity_blocks") or [])
            if not b["lines_matches_file"]),
    }
    if as_json:
        print(json.dumps({"summary": summary, "rows": rows}, indent=1, sort_keys=True))
    else:
        print(json.dumps(summary, sort_keys=True))
        for r in rows:
            if r.get("self_bound_tokens") or r.get("identity_blocks"):
                print(f'  {r["path"]} size={r["size"]} lines={r["lines"]} '
                      f'own={r["own_sha_prefix"]} self_bound={r.get("self_bound_tokens")} '
                      f'blocks={len(r.get("identity_blocks") or [])}'
                      + (f' FIRST_BLOCK@{r["identity_blocks"][0]["line"]} '
                         f'size_ok={r["identity_blocks"][0]["size_matches_file"]} '
                         f'lines_ok={r["identity_blocks"][0]["lines_matches_file"]}'
                         if r.get("identity_blocks") else ""))


if __name__ == "__main__":
    main()
