#!/usr/bin/env python3
"""R45-CL18 reproducer vs round 46: same history, two freeze instruments.

Shape (the round-45 lesson's own): one frozen FILE named only on the command line
(`--freeze-path` in round 45) plus one frozen DIRECTORY named by the pathspec. The
history is: freeze -> tamper the file -> restore the exact bytes.

Round 45's preflight must read `clean` (the hole). Round 46's gate must read exit 2
with `restored` naming the file (the closure).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1RevRestoredUnion"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R45 = os.path.join(LANE, "tools/round-45/frozen-path-preflight.py")
LIB = os.path.join(S, "lib")
sys.path.insert(0, LIB)
os.makedirs(LIB, exist_ok=True)
shutil.copyfile(os.path.join(LANE, "tools/round-46/gate.py"), os.path.join(LIB, "gate.py"))
if LIB not in sys.path:
    sys.path.insert(0, LIB)
import gate  # noqa: E402

CLAIMS = "plans/round-46-claims.md"
CLAIMS_BODY = ("# claims\n\n## Frozen paths (exact)\n\n"
               "- `plans/round-46-claims.md`\n- `tools/round-46/`\n\n## After\n\ntail\n")
FILES = {CLAIMS: CLAIMS_BODY,
         "tools/round-46/gate.py": "print('gate')\n",
         "tools/round-46/attest.py": "print('attest')\n"}

rows = []


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sh(argv, cwd=None, quiet=True):
    r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    return r


def put(d, rel, text):
    full = os.path.join(d, rel)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def main():
    d = tempfile.mkdtemp(dir=S, prefix="cl18-")
    assert sh(["git", "-C", d, "init", "-q"]).returncode == 0
    for k, v in (("user.email", "r46@fixture"), ("user.name", "r46 fixture")):
        sh(["git", "-C", d, "config", k, v])
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    for p, t in FILES.items():
        put(d, p, t)
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "commit", "-q", "-m", "freeze"])
    fz = sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()

    put(d, CLAIMS, CLAIMS_BODY + "tampered\n")
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "commit", "-q", "-m", "tamper"])
    put(d, CLAIMS, CLAIMS_BODY)
    sh(["git", "-C", d, "add", "-A"])
    sh(["git", "-C", d, "commit", "-q", "-m", "restore"])
    rev = sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()

    log = sh(["git", "-C", d, "log", "--oneline", f"{fz}..{rev}"]).stdout
    print("fixture=%s\nfreeze=%s\nrev=%s\nrange log:\n%s" % (d, fz, rev, log))

    # --- round 45's instrument: the frozen file is named only by --freeze-path.
    r45 = sh([sys.executable, "-I", "-B", R45, "--root", d, "--freeze", fz,
              "--rev", rev, "--pathspec", "tools/round-46/",
              "--freeze-path", CLAIMS])
    rows.append({"case": "R45-CL18 reproducer on round-45 preflight",
                 "cmd": "%s -I -B %s --root %s --freeze %s --rev %s --pathspec tools/round-46/ --freeze-path %s"
                        % (sys.executable, R45, d, fz, rev, CLAIMS),
                 "exit": r45.returncode,
                 "stdout_sha256": hashlib.sha256(r45.stdout.encode()).hexdigest(),
                 "utc": now()})
    print("\n== round-45 preflight ==\nexit=%d" % r45.returncode)
    try:
        rec = json.loads(r45.stdout)
        print(json.dumps({k: rec.get(k) for k in ("touched", "blob_changed", "restored", "verdict")},
                         indent=1))
    except ValueError:
        print(r45.stdout[:400])

    # --- round 46's gate, library call.
    code, receipt = gate.freeze_state(d, fz, rev, CLAIMS)
    rows.append({"case": "round-46 gate.freeze_state on the same history",
                 "cmd": "gate.freeze_state(%s, %s, %s)" % (d, fz, rev),
                 "exit": code,
                 "stdout_sha256": hashlib.sha256(json.dumps(receipt, sort_keys=True).encode()).hexdigest(),
                 "utc": now()})
    print("\n== round-46 gate.freeze_state ==\nexit=%d" % code)
    print(json.dumps({k: receipt.get(k) for k in
                      ("touched", "blob_changed", "restored", "frozen_path_changed", "reason")},
                     indent=1))

    # --- round 46's two counters, end to end (they short-circuit on the freeze arm).
    for tool in ("attest.py", "registry.py"):
        argv = [sys.executable, "-I", "-B", os.path.join(LANE, "tools/round-46", tool),
                "--root", d, "--freeze", fz, "--rev", rev]
        r = sh(argv)
        try:
            out = json.loads(r.stdout)
        except ValueError:
            out = {"raw": r.stdout[:200], "stderr": r.stderr[:200]}
        rows.append({"case": "round-46 %s end-to-end" % tool,
                     "cmd": " ".join(argv), "exit": r.returncode,
                     "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
                     "utc": now()})
        print("\n== round-46 %s ==\nexit=%d reason=%s frozen_path_changed=%s restored=%s"
              % (tool, r.returncode, out.get("reason"),
                 out.get("frozen_path_changed"), out.get("restored")))

    with open(os.path.join(S, "cl18-receipts.json"), "w") as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
    shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    main()
