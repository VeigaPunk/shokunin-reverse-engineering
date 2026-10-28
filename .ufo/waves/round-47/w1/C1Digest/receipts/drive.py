#!/usr/bin/env python3
"""C1Digest driver — verify R47-C1 clause 6 on the frozen counter, then measure a
candidate block 24 in a fixture clone.  Reads the lane read-only via `git show`;
writes only under $HYAKU_SCRATCH and inside the clone it creates."""
import hashlib
import importlib.util
import json
import os
import re
import subprocess

S = "/fast/scratch/hyaku/kaidoku-r47/C1Digest"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
CLONE = os.path.join(S, "clone")
SELF_REL = "tools/round-47/exact.py"
GATE_REL = "tools/round-46/gate.py"
MARK = "\n## Config custody for live-probe rounds (SOP)"


def git(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)


def lane_show(rev, path):
    r = git(LANE, "show", f"{rev}:{path}")
    if r.returncode != 0:
        raise SystemExit(f"lane show failed {rev}:{path}")
    return r.stdout


out = {"freeze": FREEZE, "steps": []}


def step(name, **kw):
    kw["step"] = name
    out["steps"].append(kw)
    print(json.dumps({k: kw[k] for k in kw if k in
                      ("step", "exit", "failing", "reason", "value")}, sort_keys=True))


# ---------------------------------------------------------------- A. the frozen module
mod = os.path.join(S, "mod")
frozen = {}
for rel in (SELF_REL, GATE_REL):
    full = os.path.join(mod, rel)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    body = lane_show(FREEZE, rel)
    frozen[rel] = body
    with open(full, "w") as fh:
        fh.write(body)
    step("frozen-bytes", path=rel, value=hashlib.sha256(body.encode()).hexdigest())

spec = importlib.util.spec_from_file_location("exact47", os.path.join(mod, SELF_REL))
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)

SRC = frozen[SELF_REL]
SELF_SHA = hashlib.sha256(SRC.encode()).hexdigest()
lit = re.search(r"^MUTATIONS = \[(.*?)^MUT_DIGEST", SRC, re.S | re.M).group(1)
NAMES = re.findall(r'\("([^"]+)",', lit)
MUT_SHA = hashlib.sha256("\n".join(NAMES).encode()).hexdigest()
D3 = hashlib.sha256("\n".join(NAMES[:3]).encode()).hexdigest()
step("mutations-names", value=NAMES)
step("mutations-digest-independent", value=MUT_SHA,
     matches_module_constant=(MUT_SHA == ex.MUT_DIGEST),
     matches_module_names=([n for n, _ in ex.MUTATIONS] == NAMES))
step("mutations-digest-first3", value=D3)
step("mutations-digest-sorted",
     value=hashlib.sha256("\n".join(sorted(NAMES)).encode()).hexdigest())
step("mutations-digest-trailing-newline",
     value=hashlib.sha256(("\n".join(NAMES) + "\n").encode()).hexdigest())
step("interpreter-pin-expected", value=SELF_SHA)

# ---------------------------------------------------------------- B. fixture clone
if not os.path.isdir(CLONE):
    r = subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", LANE, CLONE],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("clone failed: " + r.stderr[:400])
top = git(CLONE, "rev-parse", "--show-toplevel").stdout.strip()
if os.path.realpath(top) != os.path.realpath(CLONE):
    raise SystemExit(f"clone toplevel mismatch: {top}")
for k, v in (("user.email", "c1digest@round47"), ("user.name", "c1digest fixture")):
    git(CLONE, "config", k, v)
step("clone-toplevel", value=os.path.realpath(top))
head0 = git(CLONE, "rev-parse", "HEAD").stdout.strip()
step("clone-head", value=head0, is_freeze=(head0 == FREEZE))

base_skill = lane_show(FREEZE, "SKILL.md")
if base_skill.count(MARK) != 1:
    raise SystemExit("craft/next-section anchor is not unique in the freeze SKILL.md")
if "exactness-table v3" in base_skill:
    raise SystemExit("freeze SKILL.md already carries the v3 marker")

with open(os.path.join(S, "block_fixed.md")) as fh:
    FIXED = fh.read()
if not FIXED.endswith("\n"):
    FIXED += "\n"
if MUT_SHA not in FIXED or SELF_SHA not in FIXED:
    raise SystemExit("block_fixed.md does not carry the measured pins")

work_skill = open(os.path.join(LANE, "SKILL.md")).read()
DRAFTED = "- **24. " + work_skill.split("- **24. ", 1)[1].split("\n## Config custody", 1)[0]
step("drafted-block-source",
     value="uncommitted worktree SKILL.md, the - **24. item through its Refs line",
     bytes=len(DRAFTED.encode()), sha256=hashlib.sha256(DRAFTED.encode()).hexdigest())


def skill_with(block):
    return base_skill.replace(MARK, "\n" + block.rstrip("\n") + "\n" + MARK, 1)


def commit(path, text, msg):
    full = os.path.join(CLONE, path)
    os.makedirs(os.path.dirname(full) or CLONE, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)
    git(CLONE, "add", path)
    c = git(CLONE, "commit", "-q", "-m", msg)
    if c.returncode != 0:
        raise SystemExit("commit failed: " + c.stderr[:400])
    return git(CLONE, "rev-parse", "HEAD").stdout.strip()


def run_cli(name, rev, freeze=FREEZE, note=""):
    cmd = ["python3", "-I", "-B", os.path.join(LANE, SELF_REL), "--root", CLONE,
           "--freeze", freeze, "--rev", rev]
    env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1800)
    try:
        rec = json.loads(r.stdout)
    except Exception:
        rec = {"unparsable_stdout": r.stdout[:600], "stderr": r.stderr[:600]}
    step(name, cmd=" ".join(cmd), exit=r.returncode, failing=rec.get("failing"),
         reason=rec.get("reason"), profile=rec.get("profile"),
         battery=rec.get("battery"), rows=rec.get("rows"),
         arm_tokens=rec.get("arm_tokens"), routed_counts=rec.get("routed_counts"),
         mutations_sha256=rec.get("mutations_sha256"),
         interpreter_sha256=rec.get("interpreter_sha256"),
         refs=rec.get("refs"), block_is_last=rec.get("block_is_last"),
         header_ok=rec.get("header_ok"), frozen_path_changed=rec.get("frozen_path_changed"),
         rule_blocks=rec.get("rule_blocks"), marker_occurrences=rec.get("marker_occurrences"),
         note=note)
    return r.returncode, rec


# C1 — the block as currently drafted in the lane worktree
c1 = commit("SKILL.md", skill_with(DRAFTED), "candidate: block 24 as drafted in the worktree")
run_cli("C1-drafted", c1, note="the lane worktree's own block, unchanged")
# C2 — the corrected rows
c2 = commit("SKILL.md", skill_with(FIXED), "candidate: block 24 with bare arm tokens")
run_cli("C2-fixed", c2, note="bare-token arm cells plus the Arms paragraph")
# C3 — clause-6 isolation: digest over the first three names
c3text = FIXED.replace(MUT_SHA, D3, 1)
assert c3text != FIXED
c3 = commit("SKILL.md", skill_with(c3text), "candidate: digest over three names")
run_cli("C3-digest-three-names", c3)
# C4 — clause-6 isolation: mutation names removed
c4text = FIXED.replace(" over `" + "`, `".join(NAMES) + "`", "", 1)
assert c4text != FIXED
c4 = commit("SKILL.md", skill_with(c4text), "candidate: mutation names removed")
run_cli("C4-names-removed", c4)
# C5 — hole probe: a correct pin first, a stale pin later in the same block
c5text = FIXED.replace("  Refs:", "  History: an earlier draft pinned `mutations_sha256:"
                       + D3 + "` over three of the four names.\n\n  Refs:", 1)
assert c5text != FIXED
c5 = commit("SKILL.md", skill_with(c5text), "candidate: second, stale mutation pin")
run_cli("C5-second-stale-pin", c5)
# C6 — hole probe: the block denies the binding it satisfies
c6text = FIXED.replace(
    " over `" + "`, `".join(NAMES) + "`",
    " while the battery scores only `flag-order-drift`; `substring-arm`, `duplicate-routed-id` "
    "and `stale-mutations-digest` are named here as unscored", 1)
assert c6text != FIXED
c6 = commit("SKILL.md", skill_with(c6text), "candidate: names present, binding denied")
run_cli("C6-names-denied", c6)

# C7 — the worktree's amended frozen paths, committed (the landing hazard)
c7 = None
amended_claims = open(os.path.join(LANE, "plans/round-47-claims.md")).read()
amended_record = open(os.path.join(LANE, "tools/round-47/record.py")).read()
frozen_claims = lane_show(FREEZE, "plans/round-47-claims.md")
frozen_record = lane_show(FREEZE, "tools/round-47/record.py")
drift = {"claims_changed": amended_claims != frozen_claims,
         "record_py_changed": amended_record != frozen_record}
if any(drift.values()):
    with open(os.path.join(CLONE, "plans/round-47-claims.md"), "w") as fh:
        fh.write(amended_claims)
    with open(os.path.join(CLONE, "tools/round-47/record.py"), "w") as fh:
        fh.write(amended_record)
    git(CLONE, "add", "plans/round-47-claims.md", "tools/round-47/record.py")
    git(CLONE, "commit", "-q", "-m", "landing hazard: amended frozen paths")
    c7 = git(CLONE, "rev-parse", "HEAD").stdout.strip()
    step("frozen-drift", value=drift, commit=c7)
    run_cli("C7-frozen-drift-freeze-still-C0", c7, freeze=FREEZE,
            note="freeze still cited as the original commit")
    run_cli("C7b-frozen-drift-freeze-at-C7", c7, freeze=c7,
            note="two-freeze series: the commit carrying the amended claims is the freeze")

out["commits"] = {"C1": c1, "C2": c2, "C3": c3, "C4": c4, "C5": c5, "C6": c6, "C7": c7}
with open(os.path.join(S, "runs.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print("DRIVER_OK")
