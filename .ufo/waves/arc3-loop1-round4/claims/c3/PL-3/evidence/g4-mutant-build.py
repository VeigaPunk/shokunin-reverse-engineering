#!/usr/bin/env python3
"""PL-3 sabotage-arm builder — reverts exactly one landed hunk per mutant.

Run: python3 g4-mutant-build.py <landed-tool> <outdir>
Base: .ufo/gates/custody-pair/custody-pair.py
      sha256 29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf (1343 lines)
Each anchor is asserted to occur exactly once (refuses otherwise).
Outputs g4-sabotage-arms.txt were produced by running `selftest --scratch <fresh>`
against each mutant; each fails exactly its own case (27/28, exit 3).
"""
import hashlib
import sys
from pathlib import Path

BASE = "29bb45ae0fd795e54e85d8749a163159aead181b42e9d3af399326b968b30acf"

MUTANTS = {
    "M1-no-sidecar-arm": (
        "        candidates = ((out, out.resolve()), (sidecar, sidecar.resolve()))",
        "        candidates = ((out, out.resolve()),)",
    ),
    "M2-stanza-count": (
        "    return len(have) >= required, line",
        "    return len(ref_sections) >= required, line",
    ),
    "M3-unguarded-mkdir": (
        """        try:
            out.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:  # e.g. a path component is a regular file, or ELOOP
            print("USAGE: cannot create the receipt directory (%s): %s" % (exc, out.parent),
                  file=sys.stderr)
            return EXIT_USAGE
""",
        "        out.parent.mkdir(parents=True, exist_ok=True)\n",
    ),
    "M4-no-absent-note": (
        '''                "notes": notes + ["both sides record the path absent — the MATCH is an agreement"
                                  " on absence, not a verified presence (declared ruling: only"
                                  " error-carrying stanzas are UNEVALUABLE)"],''',
        '                "notes": notes,',
    ),
}


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src_path, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    src = src_path.read_text(encoding="utf-8")
    sha = hashlib.sha256(src.encode()).hexdigest()
    print("base %s %s" % (sha, "OK" if sha == BASE else "UNEXPECTED"))
    if sha != BASE:
        return 1
    outdir.mkdir(parents=True, exist_ok=True)
    for name, (old, new) in MUTANTS.items():
        n = src.count(old)
        assert n == 1, (name, n)
        out = outdir / (name + ".py")
        out.write_text(src.replace(old, new, 1), encoding="utf-8")
        print("wrote %-22s %s" % (name, hashlib.sha256(out.read_bytes()).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
