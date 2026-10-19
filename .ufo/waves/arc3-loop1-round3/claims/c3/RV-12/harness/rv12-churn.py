#!/usr/bin/env python3
"""RV-12 churn harness: per-entry, history-derived fragility inputs.

For each table entry, over every revision of its citing file (git object
history, the same source the probe reads):
  shift_events      revisions where lines were inserted ABOVE the pinned line
                    (a line pin moved; `exact`/`extracted`/`quoted` fire)
  pin_needle_ok     revisions where the needle matched AT the pinned line
  pin_other_text    revisions where the pinned line exists but lacks the needle
  size_history      first/last revision line counts
Renames of the citing file are detected with --diff-filter=R.
"""
import argparse
import json
import os
import re
import subprocess

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"


def git(*args):
    p = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True)
    return p.stdout.decode("utf-8", "replace")


def lines_at(rev, path):
    out = git("show", "%s:%s" % (rev, path))
    if not out:
        return None
    return out.splitlines()


def revs_of(path):
    out = git("log", "--format=%H", "--", path)
    return [r for r in out.splitlines() if r]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    table = json.load(open(args.table))
    entries = list(table.get("entries", [])) + \
        [dict(e, kind="quoted") for e in table.get("quoted", [])]

    report = {}
    for e in entries:
        eid = e.get("id")
        path = e["file"]
        revs = revs_of(path)          # newest first
        pin = e.get("line")
        needle = e.get("must_match")
        rows = []
        prev = None
        shifts = 0
        ok = other = 0
        first_len = last_len = None
        for rev in revs:
            L = lines_at(rev, path)
            if L is None:
                continue
            if last_len is None:
                last_len = len(L)
            first_len = len(L)
            if isinstance(pin, int) and 1 <= pin <= len(L):
                m = bool(re.search(needle, L[pin - 1])) if needle else None
                if m:
                    ok += 1
                else:
                    other += 1
            else:
                m = None
            if prev is not None and isinstance(pin, int):
                # revs iterate newest-first: for the pair (prev, L) the NEWER
                # revision is prev. An insertion above the pin in the newer
                # revision = prev is longer AND the first differing index sits
                # above the pin.
                n = min(len(prev), len(L))
                i = 0
                while i < n and prev[i] == L[i]:
                    i += 1
                if len(prev) > len(L) and i + 1 < pin and len(L) >= pin:
                    # only count when the pinned line already existed in the
                    # older revision: appends into a shorter file are not a
                    # shift of a pin that did not exist yet
                    shifts += 1
            rows.append({"rev": rev[:10], "lines": len(L), "pin_match": m})
            prev = L
        renames = [l for l in git("log", "--diff-filter=R", "--format=%H %s",
                                  "--", path).splitlines()]
        report[eid] = {"file": path, "line": pin, "kind": e.get("kind"),
                       "revisions": len(rows), "shift_events_above_pin": shifts,
                       "pin_needle_ok_revs": ok, "pin_other_text_revs": other,
                       "lines_first_seen": last_len, "lines_at_oldest": first_len,
                       "rename_commits": renames[:3],
                       "sample": rows[:3] + rows[-3:] if len(rows) > 6 else rows}
    json.dump(report, open(args.out, "w"), indent=1)
    for k, v in report.items():
        print("%-32s revs=%3d shifts=%3d pinok=%3d pinother=%3d len %s->%s" %
              (k, v["revisions"], v["shift_events_above_pin"],
               v["pin_needle_ok_revs"], v["pin_other_text_revs"],
               v["lines_first_seen"], v["lines_at_oldest"]))


if __name__ == "__main__":
    main()