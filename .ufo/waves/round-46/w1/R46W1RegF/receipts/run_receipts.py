"""Re-run the seat's probes in one controlled pass, capturing honest receipts."""
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RegF"
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
F = "31820472784284727546808acc31b3ea1e73919b"
Z = "0" * 40
PY = [sys.executable, "-I", "-B"]

CASES = [
    ("fetch-vendor --selftest", "fv/selftest",
     PY + [f"{L}/tools/round-41/fetch-vendor.py", "--selftest"]),
    ("fetch-vendor no args", "fv/noargs",
     PY + [f"{L}/tools/round-41/fetch-vendor.py"]),
    ("fetch-vendor --cache only", "fv/cacheonly",
     PY + [f"{L}/tools/round-41/fetch-vendor.py", "--cache", f"{S}/fv/cache2"]),
    ("fetch-vendor broken chain link", "fv/badlink",
     PY + [f"{L}/tools/round-41/fetch-vendor.py", "--spec", f"{S}/fv/bad.json",
           "--cache", f"{S}/fv/cache3b"]),
    ("fetch-vendor invalid JSON spec", "fv/badjson",
     PY + [f"{L}/tools/round-41/fetch-vendor.py", "--spec", f"{S}/fv/broken.json",
           "--cache", f"{S}/fv/cache4b"]),
    ("fetch-vendor nonexistent spec", "fv/nospec",
     PY + [f"{L}/tools/round-41/fetch-vendor.py", "--spec", f"{S}/fv/nope.json",
           "--cache", f"{S}/fv/cache5b"]),
    ("fetch-vendor --help", "fv/help",
     PY + [f"{L}/tools/round-41/fetch-vendor.py", "--help"]),
    ("c1-counter --selftest", "c1/selftest",
     PY + [f"{L}/tools/round-45/c1-counter.py", "--selftest"]),
    ("c1-counter no args", "c1/noargs",
     PY + [f"{L}/tools/round-45/c1-counter.py"]),
    ("c1-counter unknown rev", "c1/unknownrev",
     PY + [f"{L}/tools/round-45/c1-counter.py", "--root", L, "--freeze", F,
           "--rev", Z]),
    ("c1-counter score at freeze", "c1/atfreeze",
     PY + [f"{L}/tools/round-45/c1-counter.py", "--root", L, "--freeze", F,
           "--rev", F, "--json-out", f"{S}/c1/at-freeze.json"]),
    ("heldout-gen-v4 --selftest", "hg/selftest",
     PY + [f"{L}/tools/round-42/heldout-gen-v4.py", "--seed", F, "--selftest",
           "--scratch", f"{S}/hg/work"]),
    ("heldout-gen-v4 no --seed", "hg/noseed",
     PY + [f"{L}/tools/round-42/heldout-gen-v4.py", "--selftest"]),
    ("heldout-gen-v4 short seed", "hg/badseed",
     PY + [f"{L}/tools/round-42/heldout-gen-v4.py", "--seed", "zz", "--selftest"]),
    ("heldout-gen-v4 unknown class", "hg/badclass",
     PY + [f"{L}/tools/round-42/heldout-gen-v4.py", "--seed", F, "--out",
           f"{S}/hg/out-h3b", "--classes", "nope"]),
    ("frozen C2 scorer over rows.md", "check_rows",
     PY + [f"{S}/check_rows.py",
           f"{L}/.ufo/waves/round-46/w1/R46W1RegF/rows.md"]),
]


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


out = []
for label, stem, argv in CASES:
    start = utc()
    p = subprocess.run(argv, capture_output=True, env=ENV, cwd=S, timeout=1800)
    end = utc()
    rec = {"case": label,
           "argv": argv[2:],
           "start_utc": start, "end_utc": end,
           "exit": p.returncode,
           "stdout_sha256": hashlib.sha256(p.stdout).hexdigest(),
           "stdout_bytes": len(p.stdout),
           "stderr_sha256": hashlib.sha256(p.stderr).hexdigest(),
           "stderr_tail": p.stderr.decode("utf-8", "replace").strip().splitlines()[-1:] }
    open(os.path.join(S, stem + ".out"), "wb").write(p.stdout)
    open(os.path.join(S, stem + ".err"), "wb").write(p.stderr)
    out.append(rec)
    print(json.dumps(rec, sort_keys=True))

json.dump(out, open(os.path.join(S, "receipts.json"), "w"), indent=1)
