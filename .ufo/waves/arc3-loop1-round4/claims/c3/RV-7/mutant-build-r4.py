#!/usr/bin/env python3
"""RV-7 mutant builder for the LANDED r4 revision (EX-21, `29bb45ae…`).

Reverts exactly one fix at a time, so the mutation test attributes cleanly:

  MUT-A  sidecar/neighbour guard reverted -> out-only check   -> (a) returns
  MUT-B  mkdir guard reverted -> bare mkdir outside the try   -> (b) returns
  MUT-C  coverage basis reverted -> stanza count              -> (c) returns

Each pattern is matched against the landed bytes; the script reports which
patterns matched so a revision change is visible, never silent.

usage: mutant-build-r4.py <landed.py> <outdir>
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


MUTANTS = {
    "MUT-A-guard-out-only": [
        ("""        for cand, cand_res in candidates:
            if (cand_res in guarded_names or cand_res in neighbours
                    or any(_same_file(cand, g) for g in guarded)):""",
         """        for cand, cand_res in candidates[:1]:
            if (cand_res in guarded_names
                    or any(_same_file(cand, g) for g in guarded)):"""),
    ],
    "MUT-B-mkdir-outside-try": [
        ("""        try:
            out.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:  # e.g. a path component is a regular file, or ELOOP
            print("USAGE: cannot create the receipt directory (%s): %s" % (exc, out.parent),
                  file=sys.stderr)
            return EXIT_USAGE
        try:""",
         """        out.parent.mkdir(parents=True, exist_ok=True)
        try:"""),
    ],
    "MUT-C-coverage-stanzas": [
        ("""    have = distinct_paths(ref_sections)""",
         """    have = {Path(s["path"]).expanduser().resolve() for s in ref_sections}
    _ = have"""),
        ("""            % (len(have), required, " ".join(unaccounted) if unaccounted else "(none)"))
    return len(have) >= required, line""",
         """            % (len(ref_sections), required, " ".join(unaccounted) if unaccounted else "(none)"))
    return len(ref_sections) >= required, line"""),
        ("""            print("USAGE: reference covers %d of the required %d distinct paths"
                  % (len(distinct_paths(a_sections)), require),""",
         """            print("USAGE: reference covers %d of the required %d distinct paths"
                  % (len(a_sections), require),"""),
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
    ok = len(matched) == len(pairs)
    print("%-26s sha256=%s  matched=%s/%s  changed=%s  %s"
          % (name, sha(text)[:16], len(matched), len(pairs), text != src,
             "FULL" if ok else "PARTIAL"))
