#!/usr/bin/env python3
"""EX-18 (arc3-loop1-round2): apply RV-11's H1 patch text to a copy of the
census instrument. Verifies every replacement landed; prints a diff.
Usage: apply-h1.py <v10.py> <out.py>"""
import sys, hashlib, difflib

src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
before = hashlib.sha256(text.encode()).hexdigest()

H1 = [(
"""    out, counts, filelines = {}, {}, {}
    for f in files:
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError:
            counts[f] = {"lines": 0, "loci": 0}
            filelines[f] = None
            continue
""",
"""    out, counts, filelines, unreadable = {}, {}, {}, []
    for f in files:
        try:
            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()
        except OSError as ex:
            unreadable.append("%s: %s" % (f, type(ex).__name__))
            counts[f] = {"lines": 0, "loci": 0}
            filelines[f] = None
            continue
"""), (
"""    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok
""",
"""    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\
         and (not g11) and g2_ok and (not unreadable)
"""), (
"""    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
""",
"""    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)
    print("UNREADABLE (could-not-evaluate): %r" % unreadable)
""")]

out = text
for old, new in H1:
    if out.count(old) != 1:
        print("APPLY-FAIL: anchor count=%d for %r" % (out.count(old), old[:60]))
        sys.exit(3)
    out = out.replace(old, new)

open(dst, "w", encoding="utf-8").write(out)
after = hashlib.sha256(out.encode()).hexdigest()
print("APPLIED hunks=3  before_sha256=%s  after_sha256=%s" % (before, after))
d = difflib.unified_diff(text.splitlines(), out.splitlines(),
                         "c1-census-v10.py+" + before[:12],
                         "h1-candidate+" + after[:12], lineterm="", n=2)
print("\n".join(d))
