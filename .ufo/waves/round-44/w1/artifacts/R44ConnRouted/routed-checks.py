#!/usr/bin/env python3
"""R44ConnRouted read-only routed-defect checks.

Seat: R44ConnRouted. Runs fixed read-only commands against the kaidoku lane tree,
the pinned fixture bytes and one fetched upstream source, and writes one receipt per
command: seat, command, exit code, stdout sha256, stdout bytes, wall time, and a bounded
stdout/stderr head. Honest capture: a non-zero exit is recorded as-is; nothing is retried.

Scratch: <HYAKU_SCRATCH>/kaidoku-r44/probe-R44ConnRouted-* with TMPDIR set there; removed
on exit. Receipts go to the wave dir, never to scratch.

Usage: python3 -I -B routed-checks.py --lane <LANE> --out <RECEIPTS.json>
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

SEAT = "R44ConnRouted"
BASE = "c29360e3ba5381a5ab69e372d0d9577970f85018"
UNBLOB_URL = ("https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/"
              "python/unblob/handlers/filesystem/squashfs.py")
FIX = "corpus/evidence/round-42/c2/fixtures"
CARRIERS = [
    "v1-le--squashfs_v1.0_le.bin", "v1-be--squashfs_v1.0_be.bin",
    "v2-le--squashfs_v2.0_le.bin", "v2-be--squashfs_v2.0_be.bin",
]
NS = ["v2ns-le--squashfs_v2.0_le.bin", "v2ns-be--squashfs_v2.0_be.bin"]

FIXPIN_PY = """import json, hashlib, glob, os, sys
d = json.load(open('tools/round-42/fixtures.json'))
bad = 0
for f in d['fixtures']:
    g = sorted(glob.glob(os.path.join(__FIX__, f['id'] + '--*')))
    if len(g) != 1:
        print('MISSING', f['id'], g); bad += 1; continue
    b = open(g[0], 'rb').read()
    s = hashlib.sha256(b).hexdigest() == f['sha256']
    z = len(b) == f['size']
    print(f['id'], f['handler'], f['endian'], os.path.basename(g[0]), 'sha_ok=%s size_ok=%s' % (s, z))
    bad += (not s) + (not z)
print('fixtures_checked', len(d['fixtures']), 'failures', bad)
sys.exit(1 if bad else 0)
"""


def run(cid, desc, cmd, cwd, env, expect):
    t0 = time.monotonic()
    p = subprocess.run(["bash", "-c", cmd], cwd=cwd, env=env,
                       capture_output=True, timeout=600)
    wall = time.monotonic() - t0
    out = p.stdout
    return {
        "seat": SEAT,
        "check": cid,
        "description": desc,
        "command": cmd,
        "cwd": cwd,
        "exit_code": p.returncode,
        "expected_exit": expect,
        "stdout_sha256": hashlib.sha256(out).hexdigest(),
        "stdout_bytes": len(out),
        "wall_seconds": round(wall, 3),
        "stdout_head": out[:1500].decode("utf-8", "replace"),
        "stderr_head": p.stderr[:600].decode("utf-8", "replace"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scratch-base", default=os.path.join(
        os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"), "kaidoku-r44"))
    a = ap.parse_args()
    lane = os.path.abspath(a.lane)
    os.makedirs(a.scratch_base, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="probe-R44ConnRouted-", dir=a.scratch_base)
    env = dict(os.environ)
    env["TMPDIR"] = scratch  # explicit: never inherit /tmp
    try:
        pin = os.path.join(scratch, "fixpin.py")
        with open(pin, "w") as fh:
            fh.write(FIXPIN_PY.replace("__FIX__", repr(os.path.join(lane, FIX))))
        names = " ".join(f"{FIX}/{n}" for n in CARRIERS + NS)
        v12 = " ".join(f"{FIX}/{n}" for n in CARRIERS)
        checks = [
            ("K01", "lane toplevel is the lane (host guard)",
             "git rev-parse --show-toplevel", 0),
            ("K02", "base is ancestor of lane HEAD",
             f"git merge-base --is-ancestor {BASE} HEAD; echo ancestor_exit=$?", 0),
            ("K03", "fixtures are plain git blobs (no LFS pointer, no .gitattributes)",
             f"git ls-files -s {FIX} | sort; test ! -e .gitattributes; echo gitattributes_absent=$?", 0),
            ("K04", "fixture bytes vs tools/round-42/fixtures.json sha256/size pins (14 files)",
             f"python3 -I -B {pin}", 0),
            ("K05", "libmagic file -b on v1/v2 carriers and v2ns",
             f"file -b {names}", None),
            ("K06", "first 4 bytes (magic) of v1/v2/v2ns carriers",
             f"for f in {names}; do printf '%s ' \"$f\"; head -c 4 \"$f\" | od -An -c; done", 0),
            ("K07", "unsquashfs 4.7.5 -s superblock and compression lines, v1/v2 carriers",
             f"for f in {v12}; do echo \"== $f\"; unsquashfs -s \"$f\" 2>&1 | grep -E 'Found a valid|Data is|Inodes are|Fragments are'; done", 0),
            ("K08", "unsquashfs 4.7.5 -lls exit and member-line count, v1/v2 carriers",
             f"for f in {v12}; do unsquashfs -lls \"$f\" >/dev/null 2>&1; e=$?; echo \"$f exit=$e members=$(unsquashfs -lls \"$f\" 2>/dev/null | grep -c '^-')\"; done", 0),
            ("K09", "unsquashfs 4.7.5 -lls on v2ns (nonstandard magic) must refuse",
             f"unsquashfs -lls {FIX}/{NS[0]} >/dev/null 2>&1; echo exit=$?", 1),
            ("K10", "fixtures.json compression labels for v1/v2 carriers (declared, not measured)",
             "python3 -I -B -c \"import json;d=json.load(open('tools/round-42/fixtures.json'));"
             "[print(f['id'],f['handler'],f['endian'],f['compression']) for f in d['fixtures'] if f['handler'] in ('squashfs_v1','squashfs_v2')]\"", 0),
            ("K11", "literal /tmp or /var/tmp string paths in round-39/42/43 tools",
             "grep -rnE \"['\\\"](/var)?/tmp\" tools/round-39 tools/round-42 tools/round-43 --include='*.py' --include='*.sh'; echo grep_exit=$?", None),
            ("K12", "gettempdir() fallbacks (TMPDIR-unset path resolves to /tmp) in round-40..43 tools",
             "grep -rn 'gettempdir' tools/round-40 tools/round-41 tools/round-42 tools/round-43 --include='*.py' | wc -l; echo grep_exit=$?", 0),
            ("K13", "round-42 counter magic table carries nonstandard zlqs/sqlz",
             "grep -n 'zlqs\\|sqlz' tools/round-42/c1-counter.py; echo grep_exit=$?", 0),
            ("K14", "round-42 counter scratch_root body and TMPDIR reads",
             "sed -n '532,545p' tools/round-42/c1-counter.py; echo TMPDIR_reads=$(grep -c 'TMPDIR' tools/round-42/c1-counter.py)", 0),
            ("K15", "committed evidence files that cite reapable /fast/scratch/hyaku absolute paths",
             "grep -rl '/fast/scratch/hyaku/' corpus/evidence | wc -l", 0),
            ("K16", "round-44 tools dir at lane HEAD (C1/C2 counters not yet written)",
             "test -d tools/round-44; echo exists=$?", None),
            ("K17", "draft anchors in plans/round-44-claims.md",
             "grep -n 'stay equal at FREEZE and REV\\|relaxed ONLY\\|C2.s rubric targets\\|--json-out <OUT>\\|measured 2026-10-28\\|--work <SCRATCH>' plans/round-44-claims.md", 0),
            ("K18", "M43-2 origin: raw numstat predicate in round-43 C2 scorer",
             "grep -n 'sources_numstat_three_additions' tools/round-43/c2-score-r43.py", 0),
            ("K19", "round-43 W2 surviving linter mutants recorded",
             "grep -c 'SURVIVED' .ufo/waves/round-43/w2/R43W2C2MapMut.md", 0),
            ("K20", "unblob 26.6.4 squashfs handler (fetched to scratch): sasquatch dependency for v1/v2",
             f"curl -fsSL --max-time 60 -o \"$TMPDIR/unblob-squashfs-26.6.4.py\" {UNBLOB_URL} && "
             "sha256sum \"$TMPDIR/unblob-squashfs-26.6.4.py\" && "
             "grep -n 'EXECUTABLE = \\|class SquashFSv1Handler\\|class SquashFSv2Handler\\|class SquashFSv2NonStandardHandler\\|def get_dependencies\\|return \\[self.EXECUTABLE' \"$TMPDIR/unblob-squashfs-26.6.4.py\"", 0),
            ("K21", "unsquashfs -lls member path prefix on v1/v2 carriers (oracle path normalization)",
             f"for f in {v12}; do unsquashfs -lls \"$f\" 2>/dev/null | grep '^-' | head -2; done", 0),
        ]
        receipts = []
        for cid, desc, cmd, expect in checks:
            r = run(cid, desc, cmd, lane, env, expect)
            receipts.append(r)
            print(f"{cid} exit={r['exit_code']} wall={r['wall_seconds']}s sha={r['stdout_sha256'][:12]}", flush=True)
        doc = {
            "seat": SEAT,
            "lane": lane,
            "base": BASE,
            "scratch": "removed on exit",
            "note": "read-only observations; expected_exit is informational, not a score",
            "receipts": receipts,
        }
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, "w") as fh:
            json.dump(doc, fh, indent=1)
            fh.write("\n")
        print("wrote", a.out)
        return 0
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
