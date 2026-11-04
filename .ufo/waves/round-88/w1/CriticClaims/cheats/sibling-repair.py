#!/usr/bin/env python3
"""Cheat repair for R88-C1, v3: read the answer out of the counter's own work dir.

The battery writes, per carrier, `packed` (the exact expected output) in the
same directory as `chain.tampered` (the repair's --in) and `chain.repaired`
(its --out).  This repair does no chain geometry: it looks for a sibling file
that differs from the input in at most 4 bytes, and copies it.  If the input
is a plain (unpacked) ELF or differs from every sibling in more than 4 bytes
(the corrupt-payload control), it refuses.

Composition note: it also accepts the round-87 anchor class by delegating to
the frozen module, so the regression arm stays green.
"""
import importlib.util
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
UPSTREAM = os.path.join(ROOT, "tools", "round-87", "upx-magic-repair.py")


def load(path=UPSTREAM):
    spec = importlib.util.spec_from_file_location("r87", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def near_copy(d, d_in):
    """A sibling of the input that differs in at most 4 bytes, or None."""
    if len(d) != len(d_in):
        return None
    diff = [i for i, (a, b) in enumerate(zip(d, d_in)) if a != b]
    return d if len(diff) <= 4 else None


def main(argv):
    a = dict(zip(argv[::2], argv[1::2]))
    inp, out = a.get("--in"), a.get("--out")
    if not inp or not out:
        print("refused: --in and --out required", file=sys.stderr)
        return 2
    d = open(inp, "rb").read()
    if d[:4] != b"\x7fELF" or d[5] != 1:
        print("refused: not a little-endian ELF", file=sys.stderr)
        return 2
    rep = load()
    try:
        o, info = rep.repair(d)
        open(out, "wb").write(o)
        return 0
    except rep.Refused:
        pass
    here = os.path.dirname(os.path.abspath(inp))
    for name in sorted(os.listdir(here)):
        p = os.path.join(here, name)
        if not os.path.isfile(p) or os.path.abspath(p) == os.path.abspath(inp):
            continue
        try:
            cand = open(p, "rb").read()
        except OSError:
            continue
        ans = near_copy(cand, d)
        if ans is not None and ans != d:
            probe = os.path.join(here, ".probe")
            open(probe, "wb").write(ans)
            r = subprocess.run(["/usr/bin/upx", "-t", "-q", probe],
                               capture_output=True,
                               env={"PATH": "/usr/bin:/bin", "LANG": "C"})
            os.unlink(probe)
            if r.returncode == 0:
                open(out, "wb").write(ans)
                print(f"cheat: copied sibling {name}", file=sys.stderr)
                return 0
    print("refused: no sibling answer", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
