#!/usr/bin/env python3
"""Replay the R47-C2 landing on the lane's own SCORECARD bytes, in a scratch clone.

Pinned rev: 62e33f7dd75c8e3285967b26419842c106f6c965 (the card that carries
`## Record corrections — round 47`). Counter: byte-frozen record.py from 5017e1f.
"""
import hashlib
import json
import os
import subprocess
import sys

S = os.environ["HYAKU_SCRATCH"]
COUNT = os.path.join(S, "frozen", "tools", "round-47", "record.py")
C = os.path.join(S, "fix", "lane")
PIN = "62e33f7dd75c8e3285967b26419842c106f6c965"
OUT = os.path.join(S, "runs")
os.makedirs(OUT, exist_ok=True)
RUNS = []


def g(*args):
    r = subprocess.run(["git", "-C", C, *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("git failed: %s :: %s" % (" ".join(args), r.stderr))
    return r.stdout


def commit(msg):
    g("add", "-A")
    g("commit", "-q", "-m", msg)
    return g("rev-parse", "HEAD").strip()


def run(name, rev, expect):
    path = os.path.join(C, "receipts", name + ".json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cmd = [sys.executable, "-I", "-B", COUNT, "--root", C, "--rev", rev,
           "--json-out", path]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S))
    try:
        rec = json.loads(r.stdout)
    except ValueError:
        rec = {"raw": r.stdout[:400], "stderr": r.stderr[-400:]}
    row = {"variant": name, "rev": rev, "expect_exit": expect, "exit": r.returncode,
           "cmd": " ".join(cmd), "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest(),
           "sections": rec.get("sections"), "atoms": rec.get("atoms"),
           "atoms_by_class": rec.get("atoms_by_class"),
           "mismatches": [m.get("atom", "")[:90] for m in rec.get("mismatches", [])],
           "exempted": [e.get("atom", "")[:60] for e in rec.get("exempted", [])],
           "corrections": rec.get("corrections"),
           "corrections_bad": [b.get("detail") for b in (rec.get("corrections_bad") or [])],
           "failing": rec.get("failing"), "reason": rec.get("reason"),
           "battery": {k: v for k, v in (rec.get("battery") or {}).items()
                       if k in ("correction_forgeries", "forgeries_green")},
           "receipt": path}
    RUNS.append(row)
    print(json.dumps({k: row[k] for k in ("variant", "exit", "expect_exit", "sections",
                                          "atoms", "mismatches", "exempted",
                                          "corrections", "corrections_bad", "failing",
                                          "battery")}, indent=1))
    return row


assert os.path.realpath(g("rev-parse", "--show-toplevel").strip()) == \
    os.path.realpath(C), "clone toplevel mismatch"
g("config", "user.email", "r47@fixture.invalid")
g("config", "user.name", "r47 replay")

CARD = os.path.join(C, "SCORECARD.md")
base = g("show", PIN + ":SCORECARD.md")

# R0 — the card as landed today, at the pinned rev
run("R0-pinned-card-as-is", PIN, 1)

FALSE45 = "Wave 1: 40 seats; wave 2: 32 seats"
TIPC = "0425224..<tip>"

# R1 — the natural append: an empty `## Round 47` after the corrections section
r1 = base + "\n## Round 47 — depth\n\nLanding under way; no self-assessment atoms yet.\n"
open(CARD, "w").write(r1)
rev1 = commit("R1: append an empty ## Round 47 after the corrections section")
run("R1-append-empty-round47-after-corrections", rev1, 1)

# R2 — the same, but the round section sits above the corrections section and the
# round-45 seats correction is dropped (it can no longer name an atom in scope)
lines = base.splitlines(True)
head = []
tail = []
seen = False
for ln in lines:
    if ln.startswith("## Record corrections"):
        seen = True
    (tail if seen else head).append(ln)
head2 = "".join(head)
assert "## Round 47" not in head2
r2 = (head2 + "\n## Round 47 — depth\n\nLanding under way; no self-assessment atoms yet.\n\n"
      + "".join(tail))
r2 = "".join(ln for ln in r2.splitlines(True)
             if not ln.startswith("- corrects seats round-45:"))
r2 = r2.replace("  window it meant, and `git log --name-status --format=` over it prints nothing.",
                "  window it meant, and `git log --name-status --format=` over it prints nothing.\n"
                "- corrects seats round-46: 2 waves, 80 seats total")
open(CARD, "w").write(r2)
rev2 = commit("R2: round 47 above corrections, round-45 correction withdrawn")
run("R2-round47-above-corrections-withdrawn", rev2, 1)

# R3 — R2 plus the one edit the frozen counter forces: rewrite the round-46 <tip>
# sentence so a concrete window pair exists in scope
r3 = r2.replace(TIPC, "332f4884..58eb04b6")
assert r3 != r2
open(CARD, "w").write(r3)
rev3 = commit("R3: concrete window pair planted in the round-46 sentence")
row3 = run("R3-concrete-window-planted", rev3, 0)

# R4 — a second `## Record corrections — round 47` block appended at the end
r4 = r3 + ("\n## Record corrections — round 47\n\n"
           "Amendment: re-stated after re-measurement.\n\n"
           "- corrects seats round-46: 2 waves, 999 seats total\n")
open(CARD, "w").write(r4)
rev4 = commit("R4: a second corrections block appended (append-only habit)")
run("R4-second-corrections-block", rev4, 0)

# what the green card still says
landed = g("show", rev3 + ":SCORECARD.md")
hits = [i + 1 for i, ln in enumerate(landed.splitlines()) if FALSE45 in ln]
print(json.dumps({"false_sentence_still_present_at_lines": hits,
                  "grep": "git show %s:SCORECARD.md | grep -n 'wave 2: 32 seats'" % rev3[:8]},
                 indent=1))
json.dump({"clone": C, "pin": PIN, "runs": RUNS,
           "false_sentence_lines_in_R3": hits},
          open(os.path.join(OUT, "replay.json"), "w"), indent=1)
print("REPLAY saved:", os.path.join(OUT, "replay.json"))
