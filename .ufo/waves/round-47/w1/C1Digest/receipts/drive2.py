#!/usr/bin/env python3
"""C1Digest part 2 — freeze-series matrix and clause-6 isolation on the landed block 24.

Measures the frozen counter at the pinned revision 2e4ae43 across every declared
freeze, then mutates ONLY the clause-6 atoms (digest pin, mutation names) of the
landed block inside a fixture clone and records which failing entries move.
"""
import ast
import hashlib
import importlib.util
import json
import os
import re
import subprocess

S = "/fast/scratch/hyaku/kaidoku-r47/C1Digest"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE0 = "5017e1f7299c3a812e87e7950148f54313dd279e"
A1 = "9018c53b16503c8d06d398b75503406508119946"
A2 = "62e33f7dd75c8e3285967b26419842c106f6c965"
REV = "2e4ae43463aabdae707f8c8a4daa41441ad67a71"      # A3, the revision pinned now
CLONE = os.path.join(S, "clone2")
SELF_REL = "tools/round-47/exact.py"


def git(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)


def lane_show(rev, path):
    r = git(LANE, "show", f"{rev}:{path}")
    if r.returncode != 0:
        raise SystemExit(f"lane show failed {rev}:{path}")
    return r.stdout


out = {"freeze0": FREEZE0, "a1": A1, "a2": A2, "rev": REV, "steps": []}


def step(name, **kw):
    kw["step"] = name
    out["steps"].append(kw)
    print(json.dumps({k: kw[k] for k in kw if k in
                      ("step", "exit", "failing", "reason", "value")}, sort_keys=True))


SRC = lane_show(FREEZE0, SELF_REL)
SELF_SHA = hashlib.sha256(SRC.encode()).hexdigest()
tree = ast.parse(SRC)
names_ast = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(
            getattr(t, "id", None) == "MUTATIONS" for t in node.targets):
        names_ast = [elt.elts[0].value for elt in node.value.elts]
lit = re.search(r"^MUTATIONS = \[(.*?)^MUT_DIGEST", SRC, re.S | re.M).group(1)
names_re = re.findall(r'\("([^"]+)",', lit)
MUT_SHA = hashlib.sha256("\n".join(names_re).encode()).hexdigest()
step("names-ast", value=names_ast, agrees_with_regex=(names_ast == names_re))
step("digest-over-ast-names", value=hashlib.sha256("\n".join(names_ast).encode()).hexdigest(),
     equals_digest_over_regex=(hashlib.sha256("\n".join(names_ast).encode()).hexdigest()
                               == MUT_SHA))
D3 = hashlib.sha256("\n".join(names_ast[:3]).encode()).hexdigest()
DSORT = hashlib.sha256("\n".join(sorted(names_ast)).encode()).hexdigest()
DNL = hashlib.sha256(("\n".join(names_ast) + "\n").encode()).hexdigest()
step("variant-digests", value={"first3": D3, "sorted": DSORT, "trailing_nl": DNL,
                               "canonical": MUT_SHA})

# ---------------------------------------------------------------- fixture clone at REV
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
c = git(CLONE, "checkout", "-q", REV)
if c.returncode != 0:
    raise SystemExit("checkout failed: " + c.stderr[:400])
head = git(CLONE, "rev-parse", "HEAD").stdout.strip()
if head != REV:
    raise SystemExit(f"clone is at {head}, not {REV}")
step("clone2-head", value=head)
dirty = git(CLONE, "status", "--porcelain").stdout.strip()
step("clone2-status", value=dirty or "clean")


def run_cli(name, rev, freeze, note=""):
    cmd = ["python3", "-I", "-B", os.path.join(LANE, SELF_REL), "--root", CLONE,
           "--freeze", freeze, "--rev", rev]
    env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1800)
    try:
        rec = json.loads(r.stdout)
    except Exception:
        rec = {"unparsable_stdout": r.stdout[:600], "stderr": r.stderr[:600]}
    step(name, cmd=" ".join(cmd), exit=r.returncode, failing=rec.get("failing"),
         reason=rec.get("reason"), freeze_in_receipt=rec.get("freeze"),
         rev_in_receipt=rec.get("rev"),
         frozen_path_changed=rec.get("frozen_path_changed"),
         mutations_sha256=rec.get("mutations_sha256"),
         mutations_sha256_expected=rec.get("mutations_sha256_expected"),
         interpreter_sha256=rec.get("interpreter_sha256"),
         interpreter_sha256_expected=rec.get("interpreter_sha256_expected"),
         refs=rec.get("refs"), rows=rec.get("rows"), arm_tokens=rec.get("arm_tokens"),
         routed_counts=rec.get("routed_counts"), block_is_last=rec.get("block_is_last"),
         header_ok=rec.get("header_ok"), battery=rec.get("battery"), note=note)
    return r.returncode, rec


# freeze-series matrix: which --freeze makes the count evaluable at REV
for label, fz in (("R0-freeze0", FREEZE0), ("R1-A1", A1), ("R2-A2", A2),
                  ("R3-A3-equals-REV", REV)):
    run_cli(label, REV, fz, note="freeze-series matrix at the pinned revision")

# ---------------------------------------------------------------- clause-6 isolation
skill = lane_show(REV, "SKILL.md")
block = "- **24. " + skill.split("- **24. ", 1)[1].split("\n## Config custody", 1)[0]
step("landed-block-sha256", value=hashlib.sha256(block.encode()).hexdigest(),
     bytes=len(block.encode()), pins=[MUT_SHA in block, SELF_SHA in block],
     names_named=[n in block for n in names_ast])


def commit_skill(text, msg):
    with open(os.path.join(CLONE, "SKILL.md"), "w") as fh:
        fh.write(text)
    git(CLONE, "add", "SKILL.md")
    cc = git(CLONE, "commit", "-q", "-m", msg)
    if cc.returncode != 0:
        raise SystemExit("commit failed: " + cc.stderr[:400])
    return git(CLONE, "rev-parse", "HEAD").stdout.strip()


def with_block(new_block):
    return skill.replace(block, new_block, 1)


NAMELIST = " over `" + "`, `".join(names_ast) + "`"
assert NAMELIST in block, "landed block does not carry the exact name list sentence"

variants = [
    ("K1-digest-first3", block.replace(MUT_SHA, D3, 1), "clause 6: digest over three names"),
    ("K2-digest-sorted", block.replace(MUT_SHA, DSORT, 1), "clause 6: digest over sorted names"),
    ("K3-digest-trailing-nl", block.replace(MUT_SHA, DNL, 1),
     "clause 6: digest with a trailing newline"),
    ("K4-names-removed", block.replace(NAMELIST, "", 1), "clause 6: names removed"),
    ("K5-both-broken", block.replace(MUT_SHA, D3, 1).replace(NAMELIST, "", 1),
     "clause 6: stale digest and names removed"),
    ("K6-second-stale-pin", block.replace(
        "  Refs:", "  History: an earlier draft pinned `mutations_sha256:" + D3
        + "` over three of the four names.\n\n  Refs:", 1),
     "hole probe: a correct pin first, a stale pin later"),
    ("K7-names-denied", block.replace(
        NAMELIST, " while the battery scores only `flag-order-drift`; `substring-arm`, "
        "`duplicate-routed-id` and `stale-mutations-digest` are named here as unscored", 1),
     "hole probe: the four names appear while the block denies the binding"),
]
for name, text, note in variants:
    if text == block:
        raise SystemExit(f"{name}: mutation was a no-op")
    rev = commit_skill(with_block(text), name)
    run_cli(name, rev, REV, note=note)

# the landed block itself, with the battery, at REV already ran as R3
out["commits"] = {s["step"]: s.get("rev_in_receipt") for s in out["steps"]}
with open(os.path.join(S, "runs2.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print("DRIVER2_OK")
