#!/usr/bin/env python3
"""Clause-5 attack: arm-cell battery over the landed block 24.

Every variant is a one-commit fixture repo built from the lane's pinned bytes; the
frozen instrument is executed from the lane worktree against --root <fixture>.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

S = os.environ["S"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
INSTR = LANE + "/tools/round-47/exact.py"
REV = open(os.path.join(S, "PIN_REV")).read().strip()
MARK = "<!-- exactness-table v3 -->"


def git(root, *a):
    return subprocess.run(["git", "-C", root, *a], capture_output=True, text=True)


def lane_show(path):
    r = git(LANE, "show", f"{REV}:{path}")
    assert r.returncode == 0, (path, r.stderr)
    return r.stdout


NEEDED = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
          "tools/round-46/gate.py", "corpus/lessons/round-46.md",
          "corpus/lessons/round-45.md"]
BASE = {p: lane_show(p) for p in NEEDED}
SKILL = BASE["SKILL.md"]

craft_head = "## Queue-drain craft "
sec_start = SKILL.index(craft_head)
sec_end = SKILL.index("\n## ", sec_start)
CRAFT = SKILL[sec_start:sec_end]
blocks = re.split(r"(?m)^- \*\*", CRAFT)[1:]
assert SKILL.count(MARK) == 1 and MARK in blocks[-1], "landed block 24 not found"
BLOCK = blocks[-1]

# block span inside SKILL (exact substring, so a fixture is the lane's bytes + one edit)
b_start = SKILL.rindex("- **24. ")
b_end = sec_end
assert SKILL[b_start:b_end].endswith(BLOCK), "block span mismatch"
BLOCK_TEXT = SKILL[b_start:b_end]


def rows_of(block):
    lines = block.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("|")]
    return lines, idx


def set_arm(block, n, value):
    """Replace the v3-arm cell of data row `n` (0-based), keeping every other byte."""
    lines, idx = rows_of(block)
    data = idx[2:]  # idx[0] header, idx[1] separator
    li = data[n]
    raw = lines[li]
    lead = raw[:len(raw) - len(raw.lstrip())]
    cells = raw.strip().strip("|").split("|")
    assert len(cells) == 4, cells
    cells[2] = f" {value} "
    lines[li] = lead + "|" + "|".join(cells) + "|"
    return "\n".join(lines)


def set_arms(block, values):
    out = block
    for i, v in enumerate(values):
        out = set_arm(out, i, v)
    return out


def mk_repo(name, block):
    d = os.path.join(S, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        git(d, "config", k, v)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert top == d, (top, d)
    files = dict(BASE)
    files["SKILL.md"] = SKILL[:b_start] + block + SKILL[b_end:]
    for p, text in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    git(d, "add", "-A")
    r = git(d, "commit", "-q", "-m", "fixture")
    assert r.returncode == 0, r.stderr
    return d, git(d, "rev-parse", "HEAD").stdout.strip()


def run(root, rev, profile, battery=False):
    cmd = [sys.executable, "-B", INSTR, "--root", root, "--freeze", rev, "--rev", rev,
           "--profile", profile]
    if not battery:
        cmd.append("--no-battery")
    t = subprocess.run(cmd, capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
                       cwd=S, timeout=900)
    try:
        out = json.loads(t.stdout)
    except Exception:
        out = {"unparsed_stdout": t.stdout[:2000], "stderr": t.stderr[-1000:]}
    return {"cmd": " ".join(cmd), "exit": t.returncode,
            "stdout_sha256": hashlib.sha256(t.stdout.encode()).hexdigest(),
            "failing": out.get("failing") or out.get("reason"),
            "arm_tokens": out.get("arm_tokens"), "rows": out.get("rows"),
            "battery": out.get("battery")}


CELLS = ["order", "order-ish", " order ", "`order`", "order,once", "ORDER", ""]
results = {"rev": REV, "instrument_sha256": hashlib.sha256(
    open(INSTR, "rb").read()).hexdigest(),
    "instrument_at_rev_sha256": hashlib.sha256(
        BASE["tools/round-47/exact.py"].encode()).hexdigest(),
    "block_text_sha256": hashlib.sha256(BLOCK_TEXT.encode()).hexdigest(),
    "cases": []}

# genuine block, both profiles, no battery
d, r = mk_repo("genuine", BLOCK_TEXT)
results["cases"].append({"case": "genuine", "fixture": d, "rev": r,
                         "v3": run(d, r, "v3"), "v2": run(d, r, "v2")})

for i, cell in enumerate(CELLS):
    d, r = mk_repo(f"cell{i}", set_arm(BLOCK_TEXT, 0, cell))
    results["cases"].append({"case": f"row1-arm={cell!r}", "fixture": d, "rev": r,
                             "v3": run(d, r, "v3"), "v2": run(d, r, "v2")})

# vacuity probes
probes = {
    "all-four-arms-order": set_arms(BLOCK_TEXT, ["order"] * 4),
    "arms-permuted": set_arms(BLOCK_TEXT, ["once", "digest", "order", "symbol"]),
    "blobberish": set_arm(BLOCK_TEXT, 0, "blobberish"),
    "unbalanced-backtick": set_arm(BLOCK_TEXT, 0, "`order"),
    "token-plus-comment": set_arm(BLOCK_TEXT, 0, "`order`<!-- digest -->"),
}
for name, blk in probes.items():
    d, r = mk_repo(name.replace("-", "_"), blk)
    results["cases"].append({"case": name, "fixture": d, "rev": r,
                             "v3": run(d, r, "v3"), "v2": run(d, r, "v2")})

# the claim's own target on the genuine block: full battery
d, r = mk_repo("genuine_battery", BLOCK_TEXT)
results["full_battery"] = {"fixture": d, "rev": r, "v3": run(d, r, "v3", battery=True)}

with open(os.path.join(S, "results.json"), "w") as fh:
    json.dump(results, fh, indent=1)
print(json.dumps(results, indent=1))
