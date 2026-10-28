#!/usr/bin/env python3
"""C1Digest part 3 — measure the candidate block (bare tokens + Arms paragraph) on the
pinned revision, and dump every variant block as a paste-ready file."""
import hashlib
import json
import os
import shutil
import subprocess

S = "/fast/scratch/hyaku/kaidoku-r47/C1Digest"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "2e4ae43463aabdae707f8c8a4daa41441ad67a71"
CLONE = os.path.join(S, "clone2")
SELF_REL = "tools/round-47/exact.py"


def git(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)


def lane_show(rev, path):
    r = git(LANE, "show", f"{rev}:{path}")
    if r.returncode != 0:
        raise SystemExit(f"lane show failed {rev}:{path}")
    return r.stdout


out = {"rev": REV, "steps": []}


def step(name, **kw):
    kw["step"] = name
    out["steps"].append(kw)
    print(json.dumps({k: kw[k] for k in kw if k in
                      ("step", "exit", "failing", "reason", "value")}, sort_keys=True))


src = lane_show(REV, SELF_REL)
NAMES = [n for n in ("substring-arm", "duplicate-routed-id", "stale-mutations-digest",
                     "flag-order-drift")]
assert all('("%s",' % n in src for n in NAMES)
MUT_SHA = hashlib.sha256("\n".join(NAMES).encode()).hexdigest()
D3 = hashlib.sha256("\n".join(NAMES[:3]).encode()).hexdigest()
SELF_SHA = hashlib.sha256(src.encode()).hexdigest()

skill = lane_show(REV, "SKILL.md")
landed = "- **24. " + skill.split("- **24. ", 1)[1].split("\n## Config custody", 1)[0]
with open(os.path.join(S, "block_fixed.md")) as fh:
    fixed = fh.read().rstrip("\n") + "\n"

# candidate SKILL.md = the pinned revision with the candidate block swapped in
cand = skill.replace(landed, fixed, 1)
if cand == skill:
    raise SystemExit("candidate swap was a no-op")
head = git(CLONE, "rev-parse", "HEAD").stdout.strip()
step("clone2-head-before", value=head)
git(CLONE, "checkout", "-q", "-B", "cand", REV)
with open(os.path.join(CLONE, "SKILL.md"), "w") as fh:
    fh.write(cand)
git(CLONE, "add", "SKILL.md")
c = git(CLONE, "commit", "-q", "-m", "candidate: bare tokens plus the Arms paragraph")
if c.returncode != 0:
    raise SystemExit("commit failed: " + c.stderr[:400])
crev = git(CLONE, "rev-parse", "HEAD").stdout.strip()
step("candidate-commit", value=crev, block_sha256=hashlib.sha256(fixed.encode()).hexdigest())

cmd = ["python3", "-I", "-B", os.path.join(LANE, SELF_REL), "--root", CLONE,
       "--freeze", REV, "--rev", crev]
env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=1800)
rec = json.loads(r.stdout)
step("P1-candidate", cmd=" ".join(cmd), exit=r.returncode, failing=rec.get("failing"),
     reason=rec.get("reason"), rows=rec.get("rows"), arm_tokens=rec.get("arm_tokens"),
     refs=rec.get("refs"), routed_counts=rec.get("routed_counts"),
     mutations_sha256=rec.get("mutations_sha256"),
     interpreter_sha256=rec.get("interpreter_sha256"),
     battery={k: v for k, v in (rec.get("battery") or {}).items() if k != "fixtures"})

# dump every variant block, derived from the pinned landed block
NAMELIST = " over `" + "`, `".join(NAMES) + "`"
variants = {
    "landed-at-2e4ae43.md": landed,
    "candidate-arms-paragraph.md": fixed,
    "K1-digest-first3.md": landed.replace(MUT_SHA, D3, 1),
    "K2-digest-sorted.md": landed.replace(
        MUT_SHA, hashlib.sha256("\n".join(sorted(NAMES)).encode()).hexdigest(), 1),
    "K3-digest-trailing-newline.md": landed.replace(
        MUT_SHA, hashlib.sha256(("\n".join(NAMES) + "\n").encode()).hexdigest(), 1),
    "K4-names-removed.md": landed.replace(NAMELIST, "", 1),
    "K5-both-broken.md": landed.replace(MUT_SHA, D3, 1).replace(NAMELIST, "", 1),
    "K6-second-stale-pin.md": landed.replace(
        "  Refs:", "  History: an earlier draft pinned `mutations_sha256:" + D3
        + "` over three of the four names.\n\n  Refs:", 1),
    "K7-names-denied.md": landed.replace(
        NAMELIST, " while the battery scores only `flag-order-drift`; `substring-arm`, "
        "`duplicate-routed-id` and `stale-mutations-digest` are named here as unscored", 1),
}
vdir = os.path.join(S, "variant-blocks")
os.makedirs(vdir, exist_ok=True)
digests = {}
for name, text in variants.items():
    with open(os.path.join(vdir, name), "w") as fh:
        fh.write(text if text.endswith("\n") else text + "\n")
    digests[name] = hashlib.sha256(text.encode()).hexdigest()
step("variant-block-digests", value=digests)
json.dump(out, open(os.path.join(S, "runs3.json"), "w"), indent=1, sort_keys=True)
print("DRIVER3_OK")
