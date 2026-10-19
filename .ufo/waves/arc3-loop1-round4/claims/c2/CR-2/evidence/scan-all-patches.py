#!/usr/bin/env python3
"""CR-2 sweep: byte-level conformance of EVERY c2 patch text against the base.

For each fenced -/+ hunk: (a) every context and '-' line must be byte-equal to
some base line (report the base line it matches / first divergence);
(b) line neutrality: #'-' == #'+'; (c) target file from the hint.
Usage: scan-all-patches.py <BASE-PROVINCE> <PATCH> [<PATCH>...]
"""
import re
import sys

FENCE = re.compile(r"^```")
PATH_HINT = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|sh|json|toml|txt))`")


def hunks(text):
    lines = text.splitlines()
    i, cur = 0, None
    while i < len(lines):
        m = PATH_HINT.search(lines[i])
        if m:
            cur = m.group(1)
        if FENCE.match(lines[i]):
            body, j = [], i + 1
            while j < len(lines) and not FENCE.match(lines[j]):
                body.append(lines[j]); j += 1
            minus = [b[1:] for b in body if b.startswith("-") and not b.startswith("---")]
            plus = [b[1:] for b in body if b.startswith("+") and not b.startswith("+++")]
            ctx = [b[1:] for b in body if b.startswith(" ")]
            if minus and plus:
                hint = cur
                for b in body[:3]:
                    if b.startswith("# file:"):
                        hint = b.split(":", 1)[1].strip()
                    elif b.startswith("# ") and "/" in b:
                        hint = b[2:].strip().split()[0].rstrip(":")
                yield hint, ctx, minus, plus
            i = j + 1
            continue
        i += 1


def main(argv):
    base = open(argv[1], encoding="utf-8").read().splitlines()
    total_defects = 0
    for p in argv[2:]:
        try:
            text = open(p, encoding="utf-8").read()
        except OSError as ex:
            print("!! cannot read %s: %s" % (p, ex)); continue
        n = 0
        for hint, ctx, minus, plus in hunks(text):
            n += 1
            probs = []
            if len(minus) != len(plus):
                probs.append("LINE-COUNT %d-/%d+ (not neutral)" % (len(minus), len(plus)))
            for kind, group in (("ctx", ctx), ("del", minus)):
                for ln in group:
                    if ln in base:
                        continue
                    # find nearest base line for the divergence report
                    near = min(base, key=lambda b: sum(a != c for a, c in zip(ln, b)) + abs(len(ln) - len(b)))
                    probs.append("%s-line NOT in base: %r  (nearest base: %r)" % (kind, ln[:70], near[:70]))
            status = "OK " if not probs else "DEFECT"
            if probs:
                total_defects += len(probs)
            print("%s hunk %d [%s] ctx=%d del=%d add=%d" % (status, n, hint or "?", len(ctx), len(minus), len(plus)))
            for pr in probs:
                print("      %s" % pr)
        if n == 0:
            print("   (no fenced -/+ hunks found)")
    print("\nTOTAL DEFECTS: %d" % total_defects)
    return 1 if total_defects else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
