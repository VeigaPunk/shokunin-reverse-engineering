#!/usr/bin/env python3
"""EX-14 pre-flight: predict the census impact of a patch text BEFORE applying.

The census is a line-anchored instrument: PROVINCE.md's declared scope table
names fixed line ranges.  Two failure modes a patch can cause:

  (a) a LINE-COUNT change -> every row below the edit shifts -> UNDECLARED
      loci or SCOPE-ERRORS (marker line now outside its own range);
  (b) a LOCUS introduced into an UNDECLARED region -> UNDECLARED, exit 1.

This script parses a patch text with the census's OWN regexes (imported, not
re-typed), computes the post-apply line count, and reports per file:
  - line delta (must be 0 for PROVINCE.md per the C2 claim),
  - every added line that would carry a locus, with its post-apply line number
    and the scope class the census would assign it.

Exit 0 = pre-flight clean for the given file set; 1 = predicted census defect.
"""
import argparse, importlib.util, os, re, sys

CENSUS = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py"


def load_census():
    spec = importlib.util.spec_from_file_location("c1census", CENSUS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_added(text):
    """-> list of (target_or_None, post_apply_line_hint, added_line)"""
    out, target, newline = [], None, None
    for line in text.splitlines():
        m = re.match(r"^--- (?:a/)?(\S+)", line)
        if m:
            target = m.group(1)
            continue
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
        if m:
            newline = int(m.group(3))
            continue
        if newline is None:
            continue
        if line.startswith("\\"):
            continue
        if line.startswith("+"):
            out.append((target, newline, line[1:]))
            newline += 1
        elif line.startswith("-"):
            pass
        else:
            newline += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--patch", action="append", default=[])
    args = ap.parse_args()
    C = load_census()

    rc = 0
    for p in args.patch:
        txt = open(p, encoding="utf-8", errors="replace").read()
        # only fenced diff-ish content matters; parse the whole file, the
        # @@/--- markers are unambiguous
        added = parse_added(txt)
        if not added:
            print("%s: no added lines parsed (no unified-diff content)" % p)
            continue
        print("== %s: %d added lines ==" % (p, len(added)))
        for target, ln, content in added:
            f = os.path.basename(target) if target else "?"
            path = os.path.join(args.root, f)
            if not os.path.exists(path):
                print("  %s: no scoped file, skipped" % f)
                continue
            lines = open(path, encoding="utf-8").read().splitlines()
            nlines = len(lines)
            if not C.REA_GATE.search(content):
                print("  %s:+%d  (no gate token — inert)" % (f, ln))
                continue
            hits = []
            for m in C.PIN.finditer(content):
                hits.append(("pin", m.group(1)))
            spans = [(m.start(), m.end()) for m in C.PIN.finditer(content)]
            for m in C.VER.finditer(content):
                if any(s <= m.start() < e for s, e in spans):
                    continue
                hits.append(("bare", m.group(0)))
            for m in C.PTR.finditer(content):
                hits.append(("ptr", m.group(0)))
            cls, ml, mr = C.scope_of(f, ln)
            verdict = "UNDECLARED -> FAIL" if cls is None else "%s" % cls
            print("  %s:+%d  gate-token, hits=%s  scope=%s  %s"
                  % (f, ln, hits or "(none: gated but no needle)", cls, verdict))
            if cls is None and hits:
                rc = 1
            if cls is None and not hits:
                print("      note: gate token only, no needle — census inert, still undeclared-safe")
        # line-count delta per file
        for f in sorted({os.path.basename(t) for t, _, _ in added if t}):
            path = os.path.join(args.root, f)
            if not os.path.exists(path):
                continue
            n = len(open(path, encoding="utf-8").read().splitlines())
            delta = sum(1 for t, _, _ in added if t and os.path.basename(t) == f) \
                - sum(1 for l in txt.splitlines() if l.startswith("-") and not l.startswith("---"))
            print("  LINE-DELTA(%s) approx=%+d  (base %d)" % (f, delta, n))
    return rc


if __name__ == "__main__":
    sys.exit(main())
