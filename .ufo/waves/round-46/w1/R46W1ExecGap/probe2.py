#!/usr/bin/env python3
"""Full-stdout capture for the a6 fixture's battery runs (aggregates were truncated)."""
import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r46/R46W1ExecGap")
import driver as D  # noqa: E402

S = D.S
os.environ["TMPDIR"] = S
os.environ["HYAKU_SCRATCH"] = S
real = D.lane_show(D.HEAD, "tools/round-45/frozen-path-preflight.py")
attest_head = os.path.join(S, "bin", "r46-head", "attest.py")
d, rev = D.build_fixture("fx-a6-battery", real)
out = {"rev": rev, "skill_sha256": D.sha(open(os.path.join(d, "SKILL.md"), "rb").read())}
try:
    for key, argv in (
        ("v1_battery_on", ["--spec", "r45", "--profile", "v1"]),
        ("v1_notrim", ["--spec", "r45", "--profile", "v1", "--no-battery"]),
    ):
        p = subprocess.run(["/usr/bin/python3", "-I", "-B", attest_head, "--root", d,
                            "--freeze", rev, "--rev", rev, *argv],
                           capture_output=True, text=True, cwd=d)
        rec = {"cmd": " ".join([attest_head, "--root", d, "--freeze", rev, "--rev",
                                rev] + argv), "exit": p.returncode,
               "stdout_sha256": D.sha(p.stdout.encode()),
               "stderr_sha256": D.sha(p.stderr.encode()), "utc": D.utc(),
               "stdout": p.stdout, "stderr": p.stderr}
        out[key] = rec
finally:
    D.shutil.rmtree(d, ignore_errors=True)

with open(os.path.join(S, "battery-full.json"), "w") as fh:
    json.dump(out, fh, indent=1)

b = json.loads(out["v1_battery_on"]["stdout"])["battery"]
print("rev", rev, "skill", out["skill_sha256"][:16])
print({k: b[k] for k in ("forgeries_total", "v1_green", "v2_green", "genuine_green",
                         "v2_crash", "genuine_exit")})
print("v1 exit", out["v1_battery_on"]["exit"],
      "sha", out["v1_battery_on"]["stdout_sha256"][:12])
for f in b["fixtures"]:
    print(" ", f["name"], f.get("v1_exit"), f.get("v2_exit"),
          f.get("error") or (f.get("v1_failing") or [])[:1])
