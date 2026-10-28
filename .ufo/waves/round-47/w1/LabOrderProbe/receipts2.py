#!/usr/bin/env python3
"""Second pass: CLI-form receipts (real stdout sha256) + the freeze arm on a frozen restore."""
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
import gate   # noqa: E402
import exact  # noqa: E402

ENV = dict(os.environ, GIT_AUTHOR_NAME="fx", GIT_AUTHOR_EMAIL="fx@fx",
           GIT_COMMITTER_NAME="fx", GIT_COMMITTER_EMAIL="fx@fx", LC_ALL="C")
RECS = []


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(argv, cwd, label):
    r = subprocess.run(argv, cwd=cwd, env=ENV, capture_output=True)
    rec = {"id": label, "cmd": argv, "cwd": cwd, "exit": r.returncode,
           "stdout_bytes": len(r.stdout),
           "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
           "stdout_head": r.stdout.decode("utf-8", "replace")[:600],
           "stderr_head": r.stderr.decode("utf-8", "replace")[:600], "utc": utc()}
    RECS.append(rec)
    return rec, r.stdout


GATE_SRC = open(os.path.join(LANE, "tools", "round-46", "gate.py")).read()
VARIANTS = {
    "frozen": GATE_SRC,
    "late_m": GATE_SRC.replace('"--diff-merges=first-parent", "--name-status", "-z",',
                               '"--diff-merges=first-parent", "--name-status", "-m", "-z",', 1),
    "no_merges": GATE_SRC.replace('"--diff-merges=first-parent", "--name-status", "-z",',
                                  '"--diff-merges=first-parent", "--name-status", '
                                  '"--no-merges", "-z",', 1),
}
CLI = os.path.join(LANE, "tools", "round-47", "exact.py")

# --- CLI receipts on persistent one-commit fixtures -------------------------------
out = {"counter_cli": {}, "freeze_arm": {}}
for tag, src in VARIANTS.items():
    files = {"SKILL.md": exact.skill_text(exact.good_block()),
             "plans/round-47-claims.md": exact.CLAIMS_BODY,
             "corpus/lessons/round-46.md": "lesson line\n" * 240,
             "tools/round-47/exact.py": open(os.path.join(LANE, "tools", "round-47",
                                                          "exact.py")).read(),
             "tools/round-46/gate.py": src}
    d, rev = exact._repo(files, S, prefix="cli-" + tag + "-")
    jf = os.path.join(S, "cli-%s.json" % tag)
    rec, raw = run([sys.executable, "-I", "-B", CLI, "--root", d, "--freeze", rev,
                    "--rev", rev, "--profile", "v3"], d,
                   "M9-cli-" + tag)
    body = json.loads(raw.decode()) if raw.strip() else {}
    out["counter_cli"][tag] = {
        "fixture": d, "rev": rev, "exit": rec["exit"],
        "stdout_sha256": rec["stdout_sha256"], "stdout_bytes": rec["stdout_bytes"],
        "gate_order_literal": body.get("gate_order_literal"),
        "gate_order_reversed": body.get("gate_order_reversed"),
        "failing": body.get("failing"),
        "battery": {k: (body.get("battery") or {}).get(k) for k in
                    ("forgeries_total", "v2_green", "v3_green", "genuine_green", "crash")},
        "receipt_keys": sorted(body)[:12],
        "frozen_path_changed": body.get("frozen_path_changed"),
    }

# --- the freeze arm on a frozen path changed then restored ----------------------
d3, _ = exact._repo({"plans/round-47-claims.md":
                  "# claims\n\n## Frozen paths (exact)\n\n- `tools/frozen.txt`\n\n## After\n",
                  "tools/frozen.txt": "v1\n"}, S, prefix="restore-")
fz = subprocess.run(["git", "-C", d3, "rev-parse", "HEAD"], capture_output=True,
                    text=True).stdout.strip()
subprocess.run(["git", "-C", d3, "commit", "-q", "--allow-empty", "-m", "keep"], env=ENV,
               check=True)  # ensure a distinct freeze->rev range
with open(os.path.join(d3, "tools/frozen.txt"), "w") as fh:
    fh.write("v2\n")
subprocess.run(["git", "-C", d3, "add", "-A"], env=ENV, check=True)
subprocess.run(["git", "-C", d3, "commit", "-q", "-m", "change"], env=ENV, check=True)
with open(os.path.join(d3, "tools/frozen.txt"), "w") as fh:
    fh.write("v1\n")
subprocess.run(["git", "-C", d3, "add", "-A"], env=ENV, check=True)
subprocess.run(["git", "-C", d3, "commit", "-q", "-m", "restore"], env=ENV, check=True)
back = subprocess.run(["git", "-C", d3, "rev-parse", "HEAD"], capture_output=True,
                      text=True).stdout.strip()
for tag in ("frozen", "no_merges"):
    p = os.path.join(S, "gate2_%s.py" % tag)
    open(p, "w").write(VARIANTS[tag])
    spec = __import__("importlib.util", fromlist=["util"]).spec_from_file_location("g2_" + tag, p)
    mod = __import__("importlib.util", fromlist=["util"]).module_from_spec(spec)
    spec.loader.exec_module(mod)
    code, rc = mod.freeze_state(d3, fz, back, "plans/round-47-claims.md")
    out["freeze_arm"][tag] = {"fixture": d3, "freeze": fz, "rev": back, "exit": code,
                              "reason": rc.get("reason"),
                              "blob_changed": rc.get("blob_changed"),
                              "touched": rc.get("touched"),
                              "restored": rc.get("restored"),
                              "frozen_path_changed": rc.get("frozen_path_changed")}

out["receipts"] = RECS
dest = sys.argv[1]
with open(dest, "w") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps(out["counter_cli"], indent=1))
print(json.dumps(out["freeze_arm"], indent=1))
print("wrote", dest, hashlib.sha256(open(dest, "rb").read()).hexdigest())
