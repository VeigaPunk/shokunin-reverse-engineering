#!/usr/bin/env python3
"""CR-4 (arc3-loop1-round3) — build write-guard reference variants in scratch.

Variants of the guard block at custody-pair.py:562-566:
  L1  literal extension per the frozen C2 claim:  out ∈ set(paths) ∪ CUSTODY_PATHS
      (both sides .resolve())
  L2  half-fix trap: out .resolve() vs the scope side unresolved
  L3  strengthened reference: resolve both sides + os.path.samefile inode check +
      the derived sidecar path guarded too + ELOOP/unreadable alias fails closed

usage: build-variants.py <src custody-pair.py> <scratch dir>
"""
import hashlib
import pathlib
import sys

SRC = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
OUTDIR = pathlib.Path(sys.argv[2])

ORIG = """        out = Path(args.out).expanduser()
        warn_if_tmp(out)
        if out.resolve() in {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}:
            print("USAGE: refusing to write a receipt over a custody path: %s" % out, file=sys.stderr)
            return EXIT_USAGE
"""

L1 = ORIG.replace(
    "for p in CUSTODY_PATHS}", "for p in [*paths, *CUSTODY_PATHS]}")

L2 = ORIG.replace(
    "if out.resolve() in {Path(p).expanduser().resolve() for p in CUSTODY_PATHS}:",
    "if out.resolve() in {Path(p).expanduser() for p in [*paths, *CUSTODY_PATHS]}:")

L3_HELPER = '''
def guard_hits(cand: Path, scope) -> bool:
    """True when cand aliases (by resolved path or by inode) any scoped path.
    Unresolvable cand (e.g. symlink loop) fails closed."""
    try:
        cand_r = cand.resolve()
    except OSError:
        return True
    resolved = set()
    for p in scope:
        p = p if isinstance(p, Path) else Path(p)
        try:
            resolved.add(p.expanduser().resolve())
        except OSError:
            continue
    if cand_r in resolved:
        return True
    for p in scope:
        p = p if isinstance(p, Path) else Path(p)
        p = p.expanduser()
        try:
            if cand.exists() and p.exists() and os.path.samefile(cand, p):
                return True
        except OSError:
            continue
    return False


'''
L3_BLOCK = """        out = Path(args.out).expanduser()
        warn_if_tmp(out)
        for cand in (out, out.with_name(out.name + ".sha256")):
            if guard_hits(cand, [*paths, *CUSTODY_PATHS]):
                print("USAGE: refusing to write a receipt over a guarded path: %s" % cand,
                      file=sys.stderr)
                return EXIT_USAGE
"""
L3 = SRC.replace("def cmd_paths(_args) -> int:", L3_HELPER + "def cmd_paths(_args) -> int:")
assert L3.count(L3_HELPER) == 1, "L3 helper anchor not unique"
L3 = L3.replace(ORIG, L3_BLOCK)

for name, text in (("L1", SRC.replace(ORIG, L1)), ("L2", SRC.replace(ORIG, L2)), ("L3", L3)):
    assert text != SRC, "%s replacement did not apply" % name
    assert text.count(ORIG.replace("for p in CUSTODY_PATHS}", "for p in [*paths, *CUSTODY_PATHS]}")) >= 0
    dest = OUTDIR / ("tool-%s.py" % name)
    dest.write_text(text, encoding="utf-8")
    print("%s  %s  sha256=%s" % (name, dest, hashlib.sha256(dest.read_bytes()).hexdigest()))

print("src sha256=%s" % hashlib.sha256(SRC.encode()).hexdigest())
print("L1 guard line:", [l.strip() for l in SRC.replace(ORIG, L1).splitlines() if "in {" in l and "paths" in l][0])
print("L2 guard line:", [l.strip() for l in SRC.replace(ORIG, L2).splitlines() if "in {" in l and "paths" in l][0])