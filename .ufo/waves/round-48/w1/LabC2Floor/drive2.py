#!/usr/bin/env python3
"""LabC2Floor — R48-C2 floor probe, pass 2.

Card C2: same minimal green card as card C but with seats/window on their own
lines (real card style), so the counter's own mutations behave as designed.
Then the lane-side baseline runs at the true freeze.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = "/fast/scratch/hyaku/kaidoku-r48/LabC2Floor"
D = os.path.join(S, "fix1")
CTR = os.path.join(LANE, "tools/round-48/record2.py")
REC = os.path.join(S, "receipts")
ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def git(*a):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True,
                          env=ENV)


def w(path, content):
    with open(os.path.join(D, path), "w") as fh:
        fh.write(content)


def commit(msg):
    git("add", "-A")
    git("commit", "-q", "-m", msg)
    return git("rev-parse", "HEAD").stdout.strip()


def run(tag, args, stdout=None, code=None, cmd=None):
    if stdout is None:
        t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
        p = subprocess.run(["/usr/bin/python3", CTR, *args],
                           capture_output=True, text=True, cwd=S, env=ENV)
        stdout, code = p.stdout, p.returncode
        cmd = "python3 " + CTR + " " + " ".join(args)
        stderr_head = p.stderr[:400]
    else:
        t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
        stderr_head = ""
    with open(os.path.join(REC, tag + ".stdout"), "w") as fh:
        fh.write(stdout)
    env = {"tag": tag, "utc": t0, "exit": code, "cmd": cmd,
           "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
           "stdout_file": os.path.join(REC, tag + ".stdout"),
           "stderr_head": stderr_head}
    with open(os.path.join(REC, tag + ".env.json"), "w") as fh:
        fh.write(json.dumps(env, indent=1) + "\n")
    print(f"== {tag}: exit {code} sha {env['stdout_sha256'][:16]}")
    return stdout


top = git("rev-parse", "--show-toplevel").stdout.strip()
assert os.path.realpath(top) == os.path.realpath(D)
F = git("rev-list", "--max-parents=0", "HEAD").stdout.strip()
print("fixture F =", F)

AXES = ("# SCORECARD (fixture)\n\n## Owned axes\n\n"
        "| axis | score | evidence |\n"
        "|---|---|---|\n"
        "| coverage | 9.0 → 10.0 | recipe gives 1/1 |\n"
        "| depth | 9.0 → 10.0 | blocks resolved 1/1 |\n"
        "| calibration | 10.0 | n/a |\n\n")
P47 = "`.ufo/waves/round-47/w1-dispatch.json`"
P48 = "`.ufo/waves/round-48/w1-dispatch.json`"
RCP = "`.ufo/waves/round-48/l1/scores/c2-green.json`"
WIN = f"`git log {F}..{F} -- tools/` is empty."
REV = f"The landing measured `{F}`."

CARD_C2 = AXES + (
    "## Round 47 — stub C2\n\n"
    f"Claim R47-C1. Seats were read off {P47}.\n\n"
    "Waves: 2 + 0 = 2 seats.\n\n"
    f"{WIN} {REV}\n\n"
    "## Round 48 — stub C2\n\n"
    f"Claims R48-C1 and R48-C2. Dispatch {P48}.\n\n"
    "Waves: 3 + 0 = 3 seats.\n\n"
    f"{WIN} {REV}\n\n"
    f"The counter receipt {RCP} was read as atoms 6 and exempted 9 "
    "(the exempted figure is wrong on purpose; a correction repairs it).\n\n"
    "## Record corrections — round 47\n\n"
    f"- corrects path {RCP[1:-1]}: the cited receipt exists at rev\n"
    f"- corrects rev {F}: resolves to a fixture commit\n\n"
    "## Record corrections — round 48\n\n"
    "- corrects seats round-47: 1 waves, 2 seats total\n"
    "- corrects axes depth: 1/1 — re-derived from the card's own rows\n"
    "- corrects quote round-48: exempted 0 — the receipt cell reads 0\n")

w("SCORECARD.md", CARD_C2)
RC2 = commit("rev C2: minimal green card, realistic layout")
print("RC2 =", RC2)
run("C2-minimal-green-nobattery",
    ["--root", D, "--freeze", F, "--rev", RC2, "--profile", "v3", "--no-battery"])
out = run("C2-minimal-green-withbattery",
          ["--root", D, "--freeze", F, "--rev", RC2, "--profile", "v3"])
r = json.loads(out)
print("   failing:", json.dumps(r.get("failing")))
b = r.get("battery", {})
print("   battery:", json.dumps({k: b.get(k) for k in
      ("forgeries_total", "v2_green", "v3_green", "genuine_green", "crash")}))
for fx in b.get("fixtures", []):
    print("     fx:", json.dumps(fx))

# hand-applied mutations on card C2, scoring the MUTATED text under v3
sys.path.insert(0, os.path.join(LANE, "tools/round-48"))
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("record2_ctr", CTR)
ctr = importlib.util.module_from_spec(spec)
sys.modules["record2_ctr"] = ctr
spec.loader.exec_module(ctr)
files = lambda p: ctr.gate.show(D, RC2, p)  # noqa: E731
for name, fn in ctr.MUTATIONS:
    text, _ = fn(CARD_C2, {"files": files})
    if text == CARD_C2:
        print(f"   hand-mutation {name}: NO-OP on this card")
        continue
    c3, r3 = ctr.score(text, files, D, RC2, "v3", battery=None)
    print(f"   hand-mutation {name}: v3 exit {c3} "
          f"failing={json.dumps(r3.get('failing', r3.get('reason')))[:220]}")

# ---- lane baseline controls ---------------------------------------------
FREEZE = "ac02a79ff84133220d01ce3b59a4789b7004dbc5"   # A2 = claims-declared freeze
A1 = "dc73587a8b9c1a23ba5a91dc7707ac7381a8b873"        # prompt-declared (stale)
run("lane-v3-at-A2-freeze",
    ["--root", LANE, "--freeze", FREEZE, "--rev", FREEZE,
     "--profile", "v3", "--no-battery"])
run("lane-v2-at-A2-freeze",
    ["--root", LANE, "--freeze", FREEZE, "--rev", FREEZE,
     "--profile", "v2", "--no-battery"])
run("lane-v3-prompt-freeze-stale",
    ["--root", LANE, "--freeze", A1, "--rev", FREEZE,
     "--profile", "v3", "--no-battery"])
