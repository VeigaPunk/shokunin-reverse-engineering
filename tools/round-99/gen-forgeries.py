#!/usr/bin/env python3
"""gen-forgeries.py - round-99 red-fixture generator for R99-C2.

Writes standalone forgeries of a PE repair into --out-dir, each a one-decision
text transform of --base (the round-99 candidate draft) or a fixed body.  Each
must score below TARGET on tools/round-99/pe-upx-trunc-battery.py; the scores
are committed before the candidate lands (plans/round-99-claims.md).

  g2-refuse-all      refuses every input (positive arms must catch it)
  g3-trunc-only      the truncation refusal, but returns every other input
                     unchanged (no repair)
  g4-fixed-992       PackHeader taken at file offset 992 when its checksum
                     validates there (round-98 CriticC1 f1h + truncation)
  g5-size-cache      returns a cached pristine pack keyed by input size from
                     $FORGERY_CACHE (round-98 f2 + truncation); the cache is
                     built by build-size-cache.py over the pinned carriers
  g6-lazy-anchor     first window offset with a PE format byte and version
                     10..14, no checksum (round-98 f7 + truncation)
  g7-over-refuse     refuses unless the file ends exactly at the aligned end
                     of the last section (refuses every overlay)
  g8-oracle-caller   runs `upx -t` on its own output and refuses on failure
                     (the packer as the candidate's oracle)
Usage: gen-forgeries.py --base <candidate.py> --out-dir <dir>
"""
import argparse
import os
import sys


def must_replace(s, old, new, tag):
    if old not in s:
        raise SystemExit("anchor missing for %s: %r" % (tag, old[:60]))
    return s.replace(old, new, 1)


FIND_OLD = '''    if len(found) != 1:
        raise Refuse("packheader-candidates:%d" % len(found))
    return found.pop()'''
REPAIR_HEAD = '''def repair(data):
    b = bytearray(data)
    secs, rsrc_rva = sections(b)
'''
TRUNC_OLD = '''    if len(b) < end:
        raise Refuse('''
REPLACE_OLD = '''        os.replace(tmp, a.out)
        tmp = None'''


def build(base):
    out = {}
    out["g2-refuse-all"] = ('#!/usr/bin/env python3\n"""forgery g2: refuses everything."""\n'
                            'import sys\nprint("refused: truncated (forgery g2)", file=sys.stderr)\n'
                            'sys.exit(2)\n')
    out["g3-trunc-only"] = must_replace(
        base, REPAIR_HEAD, REPAIR_HEAD + '''    return bytes(b), {"packheader": None, "format": None, "changes": []}
''', "g3")
    out["g4-fixed-992"] = must_replace(
        base, FIND_OLD, '''    if ph_ok(b, 992):
        return 992
    raise Refuse("packheader-candidates:0")''', "g4")
    out["g5-size-cache"] = must_replace(
        base, REPAIR_HEAD, REPAIR_HEAD + '''    cache = os.environ.get("FORGERY_CACHE", "")
    p = os.path.join(cache, "%d.upx" % len(data))
    if cache and os.path.exists(p):
        with open(p, "rb") as fh:
            return fh.read(), {"packheader": None, "format": None, "changes": ["cache"]}
    return bytes(b), {"packheader": None, "format": None, "changes": []}
''', "g5")
    out["g6-lazy-anchor"] = must_replace(
        base, '''            if ph_ok(b, i):
                found.add(i)''', '''            if i + PH_LEN <= len(b) and b[i + 5] in PE_FORMATS and 10 <= b[i + 4] <= 14:
                found.add(i)
                break
        if found:
            break''', "g6")
    out["g6-lazy-anchor"] = must_replace(
        out["g6-lazy-anchor"], FIND_OLD, '''    if not found:
        raise Refuse("packheader-candidates:0")
    return min(found)''', "g6b")
    out["g7-over-refuse"] = must_replace(base, TRUNC_OLD, '''    if len(b) != end:
        raise Refuse(''', "g7")
    g8 = must_replace(base, "import tempfile\n", "import tempfile\nimport subprocess\n", "g8a")
    out["g8-oracle-caller"] = must_replace(g8, REPLACE_OLD, '''        if subprocess.run(["/usr/bin/upx", "-t", "-q", tmp], capture_output=True).returncode != 0:
            return refuse("truncated (oracle said no)", a.json)
        os.replace(tmp, a.out)
        tmp = None''', "g8b")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    with open(a.base) as fh:
        base = fh.read()
    os.makedirs(a.out_dir, exist_ok=True)
    for name, body in sorted(build(base).items()):
        with open(os.path.join(a.out_dir, name + ".py"), "w") as fh:
            fh.write(body)
        print(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
