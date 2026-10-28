#!/usr/bin/env python3
"""LabC2Floor — R48-C2 floor probe.

Builds a fixture git repo (scratch only), commits the real frozen claims file +
tools/round-48 bytes at F, then scores card variants:

  A   strict hypothesis card: claim id + path + rev + seats only       (floor green?)
  A2  A minus the round-48 seats atom, plus a seats correction for 48  (correction route)
  B   oracle-green card with NO claim ids                              (floor's unique bite)
  C   minimal fully-green card                                         (exit 0 + battery)
  CF  C + the axes-correction-forged mutation applied BY HAND          (survives v3?)

Every run: exact cmd, exit, stdout sha256, UTC, receipt file under $S/receipts.
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
os.makedirs(REC, exist_ok=True)

ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def git(*a):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True,
                          env=ENV)


def w(path, content):
    full = os.path.join(D, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(content)


def commit(msg):
    git("add", "-A")
    git("commit", "-q", "-m", msg)
    return git("rev-parse", "HEAD").stdout.strip()


def run(tag, args):
    t0 = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(["/usr/bin/python3", CTR, *args],
                       capture_output=True, text=True, cwd=S, env=ENV)
    with open(os.path.join(REC, tag + ".stdout"), "w") as fh:
        fh.write(p.stdout)
    env = {"tag": tag, "utc": t0, "exit": p.returncode,
           "cmd": "python3 " + CTR + " " + " ".join(args),
           "stdout_sha256": hashlib.sha256(p.stdout.encode()).hexdigest(),
           "stdout_file": os.path.join(REC, tag + ".stdout"),
           "stderr_head": p.stderr[:400]}
    with open(os.path.join(REC, tag + ".env.json"), "w") as fh:
        fh.write(json.dumps(env, indent=1) + "\n")
    print(f"== {tag}: exit {p.returncode} sha {env['stdout_sha256'][:16]}")
    try:
        r = json.loads(p.stdout)
        print("   failing:", json.dumps(r.get("failing", r.get("reason"))))
        if "floor" in r:
            print("   floor:", json.dumps(r["floor"]))
        if "battery" in r:
            print("   battery:", json.dumps(
                {k: r["battery"].get(k) for k in
                 ("forgeries_total", "v2_green", "v3_green", "genuine_green",
                  "crash")}))
            for fx in r["battery"].get("fixtures", []):
                print("     fx:", json.dumps(fx))
    except ValueError:
        print("   stdout head:", p.stdout[:200])
    return p.returncode, p.stdout


# ---------------------------------------------------------------- fixture
subprocess.run(["rm", "-rf", D], check=False)
r = subprocess.run(["git", "init", "-q", D], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
top = git("rev-parse", "--show-toplevel").stdout.strip()
assert os.path.realpath(top) == os.path.realpath(D), (top, D)
print("fixture toplevel:", top)

# F = freeze commit: ONLY the frozen paths (real bytes).
subprocess.run(["cp", os.path.join(LANE, "plans/round-48-claims.md"),
                os.path.join(D, "claims.tmp")], check=True)
os.makedirs(os.path.join(D, "plans"), exist_ok=True)
os.rename(os.path.join(D, "claims.tmp"), os.path.join(D, "plans/round-48-claims.md"))
os.makedirs(os.path.join(D, "tools/round-48"), exist_ok=True)
for f in ("census2.json", "census2.py", "meanings.py", "record2.py"):
    subprocess.run(["cp", os.path.join(LANE, "tools/round-48", f),
                    os.path.join(D, "tools/round-48", f)], check=True)
F = commit("freeze: claims + tools/round-48")
print("F =", F)

# R_A: oracle bytes + support files + card A.
subprocess.run(["cp", os.path.join(LANE, "tools/round-47/record.py"),
                os.path.join(D, "record.tmp")], check=True)
os.makedirs(os.path.join(D, "tools/round-47"), exist_ok=True)
os.rename(os.path.join(D, "record.tmp"), os.path.join(D, "tools/round-47/record.py"))

w("tools/x.py", "X = 1\n")
w("SKILL.md",
  "# fixture skill\n\n## Queue-drain craft notes\n\n"
  "- **rule one** the only rule cites `tools/x.py:1` as its resolving reference.\n")
w("corpus/README.md",
  "# corpus\n\n## Coverage map\n\n- `2026-10-28-x` mapped.\n\n## Other\n\nend.\n")
w("corpus/knowledge/2026-10-28-x.md", "# x\n")
w(".ufo/waves/round-47/w1-dispatch.json",
  json.dumps({"counts": {"spawn": 2}}) + "\n")
w(".ufo/waves/round-48/w1-dispatch.json",
  json.dumps({"counts": {"spawn": 3}}) + "\n")
w(".ufo/waves/round-48/l1/scores/c2-green.json",
  json.dumps({"atoms": 6, "exempted": 0, "corrections": 3,
              "mismatches": []}) + "\n")

AXES = ("# SCORECARD (fixture)\n\n## Owned axes\n\n"
        "| axis | score | evidence |\n"
        "|---|---|---|\n"
        "| coverage | 9.0 → 10.0 | recipe gives 1/1 |\n"
        "| depth | 9.0 → 10.0 | blocks resolved 1/1 |\n"
        "| calibration | 10.0 | n/a |\n\n")

SEATS47 = "Waves: 2 + 0 = 2 seats."
SEATS48 = "Waves: 3 + 0 = 3 seats."
WIN = (f"The window `{F}..{F} -- tools/` is empty.")
REV = f"The landing measured `{F}`."
P47 = "`.ufo/waves/round-47/w1-dispatch.json`"
P48 = "`.ufo/waves/round-48/w1-dispatch.json`"
RCP = "`.ufo/waves/round-48/l1/scores/c2-green.json`"

CARD_A = AXES + (
    "## Round 47 — stub A\n\n"
    f"Claim R47-C1. Seats were read off {P47}. {SEATS47} {REV}\n\n"
    "## Round 48 — stub A\n\n"
    f"Claims R48-C1 and R48-C2. Dispatch {P48}. {SEATS48} {REV}\n")

CARD_A2 = AXES + (
    "## Round 47 — stub A2\n\n"
    f"Claim R47-C1. Seats were read off {P47}. {SEATS47} {REV}\n\n"
    "## Round 48 — stub A2\n\n"
    f"Claims R48-C1 and R48-C2. Dispatch {P48}. {REV} "
    "No seat total is stated here at all.\n\n"
    "## Record corrections — round 48\n\n"
    "- corrects seats round-48: 1 waves, 3 seats total\n")

CARD_B = AXES + (
    "## Round 47 — stub B (no claim ids)\n\n"
    f"Seats were read off {P47}. {SEATS47} {WIN} {REV}\n\n"
    "## Round 48 — stub B (no claim ids)\n\n"
    f"Dispatch {P48}. {SEATS48} {WIN} {REV}\n\n"
    "## Record corrections — round 47\n\n"
    f"- corrects path {P48[1:-1]}: the dispatch file exists at rev\n"
    f"- corrects rev {F}: resolves to a fixture commit\n\n"
    "## Record corrections — round 48\n\n"
    "- corrects axes depth: 1/1 — re-derived from the card's own rows\n")

CARD_C = AXES + (
    "## Round 47 — stub C\n\n"
    f"Claim R47-C1. Seats were read off {P47}. {SEATS47} {WIN} {REV}\n\n"
    "## Round 48 — stub C\n\n"
    f"Claims R48-C1 and R48-C2. Dispatch {P48}. {SEATS48} {WIN} {REV}\n"
    f"The counter receipt {RCP} was read as atoms 6 and exempted 9 "
    "(the exempted figure is wrong on purpose; a correction repairs it).\n\n"
    "## Record corrections — round 47\n\n"
    f"- corrects path {RCP[1:-1]}: the cited receipt exists at rev\n"
    f"- corrects rev {F}: resolves to a fixture commit\n\n"
    "## Record corrections — round 48\n\n"
    "- corrects seats round-47: 1 waves, 2 seats total\n"
    "- corrects axes depth: 1/1 — re-derived from the card's own rows\n"
    "- corrects quote round-48: exempted 0 — the receipt cell reads 0\n")

w("SCORECARD.md", CARD_A)
RA = commit("rev A: strict hypothesis card")
print("RA =", RA)
run("A-strict-floor-only",
    ["--root", D, "--freeze", F, "--rev", RA, "--profile", "v3", "--no-battery"])

w("SCORECARD.md", CARD_A2)
RA2 = commit("rev A2: seats via correction only")
print("RA2 =", RA2)
run("A2-seats-via-correction",
    ["--root", D, "--freeze", F, "--rev", RA2, "--profile", "v3", "--no-battery"])

w("SCORECARD.md", CARD_B)
RB = commit("rev B: oracle-green, no claim ids")
print("RB =", RB)
run("B-oracle-green-floor-red",
    ["--root", D, "--freeze", F, "--rev", RB, "--profile", "v3", "--no-battery"])

w("SCORECARD.md", CARD_C)
RC = commit("rev C: minimal green card")
print("RC =", RC)
run("C-minimal-green-nobattery",
    ["--root", D, "--freeze", F, "--rev", RC, "--profile", "v3", "--no-battery"])
run("C-minimal-green-withbattery",
    ["--root", D, "--freeze", F, "--rev", RC, "--profile", "v3"])

# CF: the axes-correction-forged mutation applied BY HAND to card C
# (exactly what _m_axes_correction_forged produces), scored v3.
sys.path.insert(0, os.path.join(LANE, "tools/round-48"))
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import importlib.util  # noqa: E402
spec = importlib.util.spec_from_file_location("record2_ctr", CTR)
ctr = importlib.util.module_from_spec(spec)
sys.modules["record2_ctr"] = ctr
spec.loader.exec_module(ctr)
files = lambda p: ctr.gate.show(D, RC, p)  # noqa: E731
forged_text, _ = ctr._m_axes_correction_forged(CARD_C, {"files": files})
code, rec = ctr.score(forged_text, files, D, RC, "v3", battery=None)
out = {"applied_mutation": "axes-correction-forged",
       "note": "forged line lands in a duplicate dead section on a card that "
               "already carries `## Record corrections — round 48`",
       "exit": code, "receipt": rec}
blob = json.dumps(out, indent=1)
with open(os.path.join(REC, "CF-axes-forgery-on-landed-card.stdout"), "w") as fh:
    fh.write(blob)
env = {"tag": "CF-axes-forgery-on-landed-card",
       "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "exit": code,
       "cmd": "record2._m_axes_correction_forged(CARD_C) -> score(v3)",
       "stdout_sha256": hashlib.sha256(blob.encode()).hexdigest(),
       "stdout_file": os.path.join(REC, "CF-axes-forgery-on-landed-card.stdout")}
with open(os.path.join(REC, "CF-axes-forgery-on-landed-card.env.json"), "w") as fh:
    fh.write(json.dumps(env, indent=1) + "\n")
print("== CF forged-on-landed: exit", code, "failing:", rec.get("failing"))

# also score the OTHER mutations by hand against card C for completeness
for name, fn in ctr.MUTATIONS:
    text, _ = fn(CARD_C, {"files": files})
    c3, r3 = ctr.score(text, files, D, RC, "v3", battery=None)
    print(f"   hand-mutation {name}: v3 exit {c3} "
          f"failing={json.dumps(r3.get('failing', r3.get('reason')))[:200]}")
