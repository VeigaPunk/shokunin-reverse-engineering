#!/usr/bin/env python3
"""RV-7 mutant builder — revert one fix at a time on a revised tool.

Targeted textual reversion (not hunk indices), so each mutant changes exactly
one fix and the load-bearing check attributes cleanly:

  MUT-A  sidecar guard reverted  (guard checks `out` only)      -> (a) returns
  MUT-B  mkdir moved back outside the guarded try               -> (b) returns
  MUT-C  coverage count back to stanza multiplicity             -> (c) returns

usage: mutant-build.py <revised.py> <outdir>
prints one line per mutant: name, sha256, and whether each pattern matched.
"""
import hashlib
import sys
from pathlib import Path

REV = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
src = REV.read_text()


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


# ---- the three "fix" shapes as they appear in the revised tool -------------
# Each entry: (mutant-name, list of (fixed-form, reverted-form) candidate pairs)
MUTANTS = {
    "MUT-A-sidecar-guard-reverted": [
        # variant 1: loop over (out, sidecar)
        ("""        sidecar = out.with_name(out.name + ".sha256")
        for cand in (out, sidecar):
            if cand.resolve() in {g.resolve() for g in guarded} or any(_same_file(cand, g) for g in guarded):
                print("USAGE: refusing to write a receipt or sidecar over a path it measures"
                      " or a custody path (path or inode): %s" % cand, file=sys.stderr)
                return EXIT_USAGE
""",
         """        sidecar = out.with_name(out.name + ".sha256")
        if out.resolve() in {g.resolve() for g in guarded} or any(_same_file(out, g) for g in guarded):
            print("USAGE: refusing to write a receipt over a path it measures or a custody path"
                  " (path or inode): %s" % out, file=sys.stderr)
            return EXIT_USAGE
"""),
        # variant 2: explicit two-clause check
        ("""        if (out.resolve() in {g.resolve() for g in guarded} or any(_same_file(out, g) for g in guarded)
                or sidecar.resolve() in {g.resolve() for g in guarded}
                or any(_same_file(sidecar, g) for g in guarded)):""",
         """        if (out.resolve() in {g.resolve() for g in guarded} or any(_same_file(out, g) for g in guarded)):"""),
    ],
    "MUT-B-mkdir-outside-try": [
        ("""        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text, encoding="utf-8")""",
         """        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            out.write_text(text, encoding="utf-8")"""),
    ],
    "MUT-C-coverage-stanzas": [
        ("""            % (len(have), required, " ".join(unaccounted) if unaccounted else "(none)"))
    return len(have) >= required, line""",
         """            % (len(ref_sections), required, " ".join(unaccounted) if unaccounted else "(none)"))
    return len(ref_sections) >= required, line"""),
        ("""            print("USAGE: reference covers %d of the required %d paths" % (len(have), require),""",
         """            print("USAGE: reference covers %d of the required %d paths" % (len(a_sections), require),"""),
    ],
}

for name, pairs in MUTANTS.items():
    text = src
    matched = []
    for i, (fixed, reverted) in enumerate(pairs):
        if fixed in text:
            text = text.replace(fixed, reverted)
            matched.append(i)
    out = OUT / (name + ".py")
    out.write_text(text)
    print("%-34s sha256=%s  matched-variants=%s  changed=%s"
          % (name, sha(text)[:16], matched, text != src))
