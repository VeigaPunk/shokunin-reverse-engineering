#!/usr/bin/env python3
"""Round 9: (1) admissibility sweep for both candidate freezes;
(2) the executing-file vs pinned-bytes gap on the HEAD instrument."""
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["HYAKU_SCRATCH"]
DECLARED = "31820472784284727546808acc31b3ea1e73919b"
RECEIPT_FREEZE = "0425224756791b414454df28a9abf93dcdf154ce"
OUT = {}
env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)


def git(*a):
    return subprocess.run(["git", "-C", LANE, *a], capture_output=True,
                          text=True).stdout.strip()


def run(prog, root, freeze, rev):
    r = subprocess.run([sys.executable, "-I", "-B", prog, "--root", root,
                        "--freeze", freeze, "--rev", rev, "--no-battery"],
                       capture_output=True, text=True, env=env)
    try:
        d = json.loads(r.stdout)
    except ValueError:
        d = {"raw": r.stdout[:160]}
    return r.returncode, d


head = git("rev-parse", "HEAD")
revs = git("rev-list", "--reverse", "--ancestry-path", DECLARED + "..HEAD").splitlines()
OUT["head"] = head
OUT["chain_len"] = len(revs)

for label, fz in (("declared_31820472", DECLARED), ("receipts_04252247", RECEIPT_FREEZE)):
    rows = []
    probes = [DECLARED] + revs
    for rv in probes:
        rc, d = run(os.path.join(LANE, "tools/round-46/attest.py"), LANE, fz, rv)
        rows.append({"rev": rv[:8], "exit": rc, "reason": d.get("reason"),
                     "failing": (d.get("failing") or [])[:2],
                     "met_target": d.get("met_target"),
                     "rows": d.get("rows")})
    OUT[label] = rows
    ok = [r for r in rows if r["exit"] == 0]
    print("== %s  probes=%d  greens=%d" % (label, len(rows), len(ok)))
    for r in ok:
        print("   GREEN rev=%s rows=%s" % (r["rev"], r["rows"]))
    reach = [r for r in rows if r["exit"] == 1]
    print("   exit1 (reachable but not met):", [(r["rev"], r["failing"]) for r in reach])
    print("   exit2 (could-not-evaluate):", len([r for r in rows if r["exit"] == 2]))

# Which frozen paths does each post-freeze commit touch?
OUT["post_freeze_touches"] = git(
    "log", "-m", "--diff-merges=first-parent", "--name-only", "--format=%H %s",
    DECLARED + "..HEAD", "--", "tools/round-46/", "plans/round-46-claims.md").splitlines()

# ---- executing-file gap: patched copy OUTSIDE the root, honest repo ----
src = open(os.path.join(LANE, "tools/round-46/attest.py")).read()
patched = src.replace('    failing = []\n',
                      '    receipt["met_target"] = True\n    return 0, receipt\n'
                      '    failing = []\n', 1)
assert patched != src
elsewhere = os.path.join(S, "elsewhere-tools")
shutil.rmtree(elsewhere, ignore_errors=True)
shutil.copytree(os.path.join(LANE, "tools/round-46"), elsewhere)
open(os.path.join(elsewhere, "attest.py"), "w").write(patched)

rc, d = run(os.path.join(elsewhere, "attest.py"), LANE, RECEIPT_FREEZE, head)
OUT["exec_gap_on_genuine"] = {"exit": rc, "met_target": d.get("met_target"),
                              "pin_checked": bool(d.get("pin")),
                              "failing": d.get("failing")}
print("== executing-file gap (genuine SKILL, patched tool elsewhere):", rc,
      json.dumps(OUT["exec_gap_on_genuine"])[:200])

# same, but on a do-nothing artefact committed in a fixture
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import importlib.util
gs = importlib.util.spec_from_file_location("gate", os.path.join(LANE, "tools/round-46/gate.py"))
gate = importlib.util.module_from_spec(gs); sys.modules["gate"] = gate; gs.loader.exec_module(gate)
a_s = importlib.util.spec_from_file_location("attest", os.path.join(LANE, "tools/round-46/attest.py"))
attest = importlib.util.module_from_spec(a_s); sys.modules["attest"] = attest
a_s.loader.exec_module(attest)
skill = gate.show(LANE, head, "SKILL.md")
block = [b for b in attest.craft_blocks(skill) if attest.SPECS["r46"]["marker"] in b][0]
dn = skill.replace(block, "- **23. removed.** \n", 1)

fx = os.path.join(S, "fx-exec")
shutil.rmtree(fx, ignore_errors=True)
os.makedirs(fx)
subprocess.run(["git", "-C", fx, "init", "-q"], check=True)
for k, v in (("user.email", "c@r46"), ("user.name", "critic")):
    subprocess.run(["git", "-C", fx, "config", k, v], check=True)
assert subprocess.run(["git", "-C", fx, "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip() == fx
for p in ("SKILL.md", "plans/round-46-claims.md", "corpus/lessons/round-45.md",
          "corpus/lessons/round-46.md",
          "corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md",
          "tools/round-46/attest.py", "tools/round-46/gate.py"):
    body = dn if p == "SKILL.md" else gate.show(LANE, head, p)
    if body is None:
        continue
    full = os.path.join(fx, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(body)
subprocess.run(["git", "-C", fx, "add", "-A"], check=True)
subprocess.run(["git", "-C", fx, "commit", "-q", "-m", "dn"], check=True)
frev = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"],
                      capture_output=True, text=True).stdout.strip()

rc, d = run(os.path.join(fx, "tools/round-46/attest.py"), fx, frev, frev)
OUT["honest_on_donothing_fixture"] = {"exit": rc, "met_target": d.get("met_target"),
                                      "failing": (d.get("failing") or [])[:2]}
rc, d = run(os.path.join(elsewhere, "attest.py"), fx, frev, frev)
OUT["patched_elsewhere_on_donothing"] = {"exit": rc, "met_target": d.get("met_target")}
print("== honest on do-nothing:", OUT["honest_on_donothing_fixture"])
print("== patched-elsewhere on do-nothing:", OUT["patched_elsewhere_on_donothing"])

json.dump(OUT, open(os.path.join(S, "attacks9.json"), "w"), indent=1, sort_keys=True)
print(json.dumps(OUT["post_freeze_touches"], indent=1)[:1200])
