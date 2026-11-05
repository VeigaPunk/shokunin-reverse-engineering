#!/usr/bin/env python3
"""CriticC2 scratch generator: one-decision text transforms of the landed candidate.

Writes forgeries into <clone>/tools/round-99/critic/ (scratch clone only).
"""
import os
import sys

S = "/fast/scratch/hyaku/kaidoku-r99/CriticC2"
CLONE = S + "/clone"
OUT = CLONE + "/tools/round-99/critic"


def must_replace(s, old, new, tag):
    if s.count(old) != 1:
        raise SystemExit("anchor count %d for %s: %r" % (s.count(old), tag, old[:70]))
    return s.replace(old, new, 1)


base = open(CLONE + "/tools/round-99/upx-pe-repair.py", encoding="utf-8").read()
TRUNC = "    if len(b) < end:"
ENDLINE = '    end = (last["rptr"] + last["rsize"] + falign - 1) // falign * falign'
ANCHOR = "    i = find_packheader(b, secs)"
REPLACE = "        os.replace(tmp, a.out)"
disable = lambda s: must_replace(s, TRUNC, "    if 0:", "disable-trunc")

forg = {}

# fa: refusal keyed on the battery's two cut patterns (raw end - 1, UPX1 midpoint); no alignment term.
forg["fa-cutpattern"] = must_replace(
    base, TRUNC,
    '    if len(b) in (last["rptr"] + last["rsize"] - 1, secs[1]["rptr"] + secs[1]["rsize"] // 2):',
    "fa")

# fb: last-section raw end WITHOUT FileAlignment (honest test otherwise).
forg["fb-noalign"] = must_replace(base, ENDLINE, '    end = last["rptr"] + last["rsize"]', "fb")

# fc1: pure size modulo FileAlignment.
forg["fc1-size-mod"] = must_replace(base, TRUNC, "    if len(b) % falign:", "fc1")

# fc2: size modulo FileAlignment gated by the raw end.
forg["fc2-size-mod-gated"] = must_replace(base, TRUNC, "    if len(b) % falign and len(b) < end:", "fc2")

# fd: UPX! (PackHeader) position relative to the end, fixed constant 57888 (t32's end - UPX!).
forg["fd-upx-fixed-k"] = must_replace(
    disable(base), ANCHOR,
    ANCHOR + '\n    if len(b) - i < 57888:\n        raise Refuse("truncated: upx-relative")', "fd")

# fe: PackHeader c_len bound (stream end = header + c_len), no section arithmetic.
forg["fe-clen-bound"] = must_replace(
    disable(base), ANCHOR,
    ANCHOR + '\n    if len(b) < i + PH_LEN + struct.unpack_from("<I", b, i + 20)[0]:\n'
             '        raise Refuse("truncated: clen")', "fe")

# fg: oracle caller, static-screen evasion through an `os` alias (no forbidden token text).
forg["fg-oracle-alias"] = must_replace(
    base, REPLACE,
    '        import os as o\n'
    '        if o.system("/usr/bin/upx -t -q \'%s\' >/dev/null 2>&1" % tmp) != 0:\n'
    '            return refuse("truncated (oracle said no)", a.json)\n' + REPLACE, "fg")

os.makedirs(OUT, exist_ok=True)
for name, text in forg.items():
    with open(os.path.join(OUT, name + ".py"), "w", encoding="utf-8") as fh:
        fh.write(text)
    print(name, len(text))
sys.exit(0)
