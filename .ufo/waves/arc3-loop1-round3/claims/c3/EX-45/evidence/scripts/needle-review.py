#!/usr/bin/env python3
"""EX-45 needle-quality review harness (scratch, read-only against the repo).

Reads a pointer table + expected.json, resolves citing/target files as Git
objects at a named rev (same resolution the probe uses), and reports for every
entry:
  L  live: must_match resolves per the entry's kind semantics
  A  anchor: pinned line number correct at rev; hits at rev
  B  boundedness: regex static audit (unbounded wildcards, bare capture groups)
  S  shift window: for exact/quoted entries, how many lines a pure line-shift
     (insertion above the pin) can move the target before the needle notices;
     a hit at p+delta keeps the entry green -> silent window
  T  target-side: for extracted entries, the named target line(s) and their
     content at rev; multiplicity of the pattern within the citing line.

Usage: needle-review.py --root DIR --rev REV --table PATH [--json OUT]
"""
import argparse
import json
import re
import subprocess
import sys


def git_show(root, rev, path):
    p = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8", "replace")


def lines_of(root, rev, path):
    t = git_show(root, rev, path)
    return None if t is None else t.splitlines()


WILD = [
    (r"\.\*", "unbounded `.*`"),
    (r"\.\+", "unbounded `.+`"),
    (r"\[\\s\\S\]\*", "unbounded [\\s\\S]*"),
    (r"\\w\*", "unbounded \\w*"),
    (r"\\s\*", "unbounded \\s*"),
]

# a capture group is "bounded" if the captured text class is digits only
DIGITS = re.compile(r"^(\\d|\[0-9\]|\[\\d\])")


def audit_regex(pat):
    flags = []
    for rx, label in WILD:
        if re.search(rx, pat):
            flags.append(label)
    return flags


def group_class_bounded(pat):
    """Best-effort: does every capturing group capture digits?"""
    out = []
    for i, frag in enumerate(re.findall(r"\((?:\?:)?((?:[^()\\]|\\.)*)\)", pat)):
        if DIGITS.match(frag.strip()) or frag.strip() in ("\\d+", "[0-9]+", "[0-9]{1,}"):
            out.append((i + 1, frag.strip(), "digits"))
        else:
            out.append((i + 1, frag.strip(), "not-digits"))
    return out


def entry_review(entry, root, rev, quoted=False):
    r = {"id": entry.get("id", "<unnamed>"), "kind": "quoted" if quoted else entry.get("kind"),
         "file": entry.get("file")}
    citing = lines_of(root, rev, entry["file"])
    if citing is None:
        r["live"] = "FILE-ABSENT-at-rev"
        return r
    r["citing_lines"] = len(citing)
    kind = r["kind"]

    if kind == "anchor":
        hits = [i + 1 for i, l in enumerate(citing)
                if re.search(entry["must_match"], l)]
        r["hits"] = hits
        pin = entry.get("pin_line")
        r["pin_line"] = pin
        if not hits:
            r["live"] = "DEAD"
        elif pin is not None and pin not in hits:
            r["live"] = "MOVED"
        else:
            r["live"] = "OK"
        r["moved_blind_by_design"] = pin is None
        r["boundedness"] = audit_regex(entry["must_match"])
        r["gap_silent_window"] = None
        return r

    n = entry.get("line")
    r["pin_line"] = n
    if not isinstance(n, int) or not (1 <= n <= len(citing)):
        r["live"] = "OUT-OF-RANGE"
        return r
    citing_line = citing[n - 1]
    r["citing_text"] = citing_line[:160]

    if kind in ("exact", "quoted"):
        ok = bool(re.search(entry["must_match"], citing_line))
        hits = [i + 1 for i, l in enumerate(citing)
                if re.search(entry["must_match"], l)]
        r["hits"] = hits
        r["live"] = "OK" if ok else "DEAD"
        r["boundedness"] = audit_regex(entry["must_match"])
        if kind == "quoted" and not ok:
            r["live"] = "RECORD-WORDS-MISSING"
        # shift window: nearest matching line above/below the pin
        below = [h for h in hits if h > n]
        above = [h for h in hits if h < n]
        r["gap_silent_window"] = {
            "down": (min(below) - n) if below else None,
            "up": (n - max(above)) if above else None,
        }
        return r

    if kind == "extracted":
        m = re.search(entry["pattern"], citing_line)
        r["pattern"] = entry["pattern"]
        r["pattern_boundedness"] = audit_regex(entry["pattern"])
        r["group_classes"] = group_class_bounded(entry["pattern"])
        if not m:
            r["live"] = "NO-PATTERN-HIT"
            return r
        r["pattern_hit"] = m.group(0)
        findall = re.findall(entry["pattern"], citing_line)
        r["pattern_multiplicity"] = len(findall)
        tg = entry.get("target_group", 1)
        tge = entry.get("target_group_end", tg)
        try:
            lo, hi = int(m.group(tg)), int(m.group(tge) or m.group(tg))
        except (IndexError, ValueError):
            r["live"] = "GROUP-UNREADABLE"
            return r
        tgt = entry["target"]
        r["target"] = "%s:%d-%d" % (tgt, lo, hi)
        tlines = lines_of(root, rev, tgt)
        if tlines is None:
            r["live"] = "TARGET-ABSENT"
            return r
        r["target_lines"] = len(tlines)
        window = int(entry.get("window", 0))
        lo2, hi2 = lo - window, hi + window
        if not (1 <= lo2 <= hi2 <= len(tlines)):
            r["live"] = "TARGET-OUT-OF-RANGE"
            r["target_range"] = "%d-%d of %d" % (lo2, hi2, len(tlines))
            return r
        blob = "\n".join(tlines[lo2 - 1:hi2])
        ok = bool(re.search(entry["must_match"], blob, re.M))
        r["live"] = "OK" if ok else ("STAMP-HISTORICAL" if entry.get("stamp") else "DEAD")
        r["target_text"] = tlines[lo2 - 1][:160]
        # target-side shift window: matching lines of must_match in target
        thits = [i + 1 for i, l in enumerate(tlines)
                 if re.search(entry["must_match"], l, re.M)]
        r["target_hits"] = thits
        below = [h for h in thits if h > hi2]
        above = [h for h in thits if h < lo2]
        r["target_gap_window"] = {
            "end_down": (min(below) - hi2) if below else None,
            "start_up": (lo2 - max(above)) if above else None,
        }
        r["boundedness"] = audit_regex(entry["must_match"])
        return r

    r["live"] = "UNKNOWN-KIND"
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--table", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()
    table = json.load(open(a.table))
    rows = []
    for e in table.get("entries", []):
        rows.append(entry_review(e, a.root, a.rev))
    for e in table.get("quoted", []):
        rows.append(entry_review(e, a.root, a.rev, quoted=True))
    bad = [r for r in rows if r.get("live") not in ("OK",)]
    out = {"rev": a.rev, "table": a.table, "count": len(rows),
           "not_live": [r["id"] for r in bad], "rows": rows}
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1, sort_keys=True)
    for r in rows:
        mark = "OK " if r.get("live") == "OK" else "!! "
        extra = ""
        if r.get("gap_silent_window"):
            extra = " shift-window=%s" % r["gap_silent_window"]
        if r.get("pattern_multiplicity", 1) > 1:
            extra += " pattern-multiplicity=%d" % r["pattern_multiplicity"]
        print("%s%-32s %-9s line=%s live=%s%s hits=%s%s"
              % (mark, r["id"], r["kind"], r.get("pin_line"), r.get("live"),
                 extra, r.get("hits"), (" boundedness=%s" % r["boundedness"])
                 if r.get("boundedness") else ""))
        if r["kind"] == "extracted" and r.get("live") != "OK":
            print("      target=%s live=%s" % (r.get("target"), r.get("live")))
    print("TOTAL=%d NOT-LIVE=%d %s" % (len(rows), len(bad), bad and [b["id"] for b in bad]))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())