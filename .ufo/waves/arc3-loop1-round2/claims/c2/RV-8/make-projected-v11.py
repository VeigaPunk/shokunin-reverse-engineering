#!/usr/bin/env python3
"""RV-8 — build a projected v11 on scratch from the frozen H1/H3 patch texts.

Source: the sealed patch texts
  .ufo/waves/arc3-loop1-round1/claims/c3/RV-11/proposed-missing-file-guard.patch.md   (H1)
  .ufo/waves/arc3-loop1-round1/claims/c3/CR-5/proposed-g2-positive-floor.patch.md    (H3)
applied to a COPY of .ufo/gates/c1-census-v10.py. Never touches the real target.

Usage: python3 make-projected-v11.py SRC OUT   (writes OUT; exits 0 iff both
hunks matched their anchors exactly; prints one line per applied hunk)
"""
import sys

H1_OLD_1 = """    out, counts, filelines = {}, {}, {}
    for f in files:
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            counts[f] = {"lines": 0, "loci": 0}
            filelines[f] = None
            continue"""
H1_NEW_1 = """    out, counts, filelines, unreadable = {}, {}, {}, []
    for f in files:
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError as ex:
            unreadable.append("%s: %s" % (f, type(ex).__name__))
            counts[f] = {"lines": 0, "loci": 0}
            filelines[f] = None
            continue"""

H1_OLD_2 = """    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok"""
H1_NEW_2 = """    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok and (not unreadable)"""
H1_OLD_3 = """    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)"""
H1_NEW_3 = """    print("SCOPE-ERRORS (marker assertions): %r" % scope_errors)
    print("UNREADABLE (could-not-evaluate): %r" % unreadable)"""


def main():
    src, out = sys.argv[1], sys.argv[2]
    txt = open(src, encoding="utf-8").read()
    applied = []

    for tag, old, new in (("H1.1", H1_OLD_1, H1_NEW_1),
                          ("H1.2", H1_OLD_2, H1_NEW_2),
                          ("H1.3", H1_OLD_3, H1_NEW_3)):
        if old not in txt:
            print("ANCHOR-MISS %s" % tag)
            return 2
        txt = txt.replace(old, new, 1)
        applied.append(tag)
    if "unreadable" not in txt:
        print("H1-GATE-MISS (TEXT-report gate not inserted; seal demands it)")
        return 2

    # H3 needs to be smuggled in: the sealed patch text's optional stronger form
    # FAILs when current-ok loci == 0; the core fix alone is applied here, so the
    # verdict test can distinguish 'no loci' from 'clean run'.
    g2_old = """    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)"""
    g2_new = """    g2_ok = len(out.get("current-ok", [])) > 0"""
    if g2_old not in txt:
        print("ANCHOR-MISS H3")
        return 2
    txt = txt.replace(g2_old, g2_new, 1)
    applied.append("H3")

    open(out, "w", encoding="utf-8").write(txt)
    print("PROJECTED-V11 written %s hunks=%s" % (out, ",".join(applied)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
