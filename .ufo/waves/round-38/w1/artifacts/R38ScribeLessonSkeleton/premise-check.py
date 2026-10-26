#!/usr/bin/env python3
"""Pre-freeze premise check (fix for the stale be-dependency premise, M38-3).

Compares a written premise about BE-v4 SquashFS extraction with a two-arm live
measurement of the same carrier:

  off-path arm  REA/unblob run with the declared extractor hidden from PATH
  on-path arm   the same run with the declared extractor resolvable

If a document asserts "no external extractor" (or the equivalent) while the
off-path arm carries a `missing-extractor-dependency` gap naming an executable
and the on-path arm publishes files from the same bytes, the premise is false and
this exits 1, quoting the offending line. Otherwise exit 0.

Quoted spans ("…", “…”, 「…」) are removed before matching: a lesson that must quote
the false sentence as evidence is not asserting it. Bare prose is.

usage: premise-check.py --off OFF.json --on ON.json DOC [DOC ...]
"""
import argparse
import json
import re
import sys

ASSERTION = re.compile(
    r"no external extractor|without any external extractor|no external extractor dependency",
    re.IGNORECASE,
)
QUOTED = re.compile(r'"[^"]*"|“[^”]*”|「[^」]*」')


def arms(off_path: str, on_path: str) -> tuple[list[str], list[str], list[str]]:
    deps: list[str] = []
    gap_kinds: list[str] = []
    off = json.load(open(off_path))
    n = off.get("normalized_result") or {}
    for gap in n.get("extraction_gaps") or []:
        gap_kinds.append(gap.get("kind") or "")
        deps.extend(gap.get("dependencies") or [])
    on = json.load(open(on_path))
    on_files = len((on.get("normalized_result") or {}).get("files") or [])
    return gap_kinds, sorted(set(deps)), ["files=%d" % on_files] if on_files else []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--off", required=True)
    ap.add_argument("--on", required=True)
    ap.add_argument("docs", nargs="+")
    a = ap.parse_args()

    gap_kinds, deps, on_note = arms(a.off, a.on)
    falsified = "missing-extractor-dependency" in gap_kinds and bool(deps) and bool(on_note)
    print(f"off-path gaps: {gap_kinds or '[]'} deps: {deps or '[]'}")
    print(f"on-path {on_note[0] if on_note else 'files=0'}")
    if not falsified:
        print("premise-check: evidence does not decide the premise (needs an off-path gap naming an executable and a non-empty on-path run)")
        return 2

    hits: list[str] = []
    for doc in a.docs:
        for lineno, line in enumerate(open(doc, encoding="utf-8", errors="replace"), 1):
            if ASSERTION.search(QUOTED.sub("", line)):
                hits.append(f"{doc}:{lineno}: {line.strip()}")
    if hits:
        print("\n".join(hits))
        print(f"premise-check: FAIL - {len(hits)} assertion(s) contradicted by {deps} on this host", file=sys.stderr)
        return 1
    print("premise-check: ok - no document under check asserts the extractor-free premise")
    return 0


if __name__ == "__main__":
    sys.exit(main())
