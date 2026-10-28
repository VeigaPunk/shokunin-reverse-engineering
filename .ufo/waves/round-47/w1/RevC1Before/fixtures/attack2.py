#!/usr/bin/env python3
"""RevC1Before part 2: body-split bounds, the unbound executing core, and a denominator edit."""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Before"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = LANE + "/.ufo/waves/round-47/w1/RevC1Before"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
CRAFT = "## Queue-drain craft "
os.makedirs(OUT + "/fixtures", exist_ok=True)


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=env or dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))


def show(root, rev, path):
    return sh(["git", "-C", root, "show", f"{rev}:{path}"]).stdout


def newrepo(name, at=FREEZE):
    d = S + "/" + name
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", LANE, d])
    sh(["git", "-C", d, "checkout", "-q", at])
    sh(["git", "-C", d, "config", "user.email", "fx@round47"])
    sh(["git", "-C", d, "config", "user.name", "round47 fixture"])
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert top == d, (top, d)
    return d


def commit(d, msg):
    sh(["git", "-C", d, "add", "-A"])
    r = sh(["git", "-C", d, "commit", "-q", "--allow-empty", "-m", msg])
    assert r.returncode == 0, r.stderr[:300]
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def insert_at_craft_end(skill, block):
    head, rest = skill.split(CRAFT, 1)
    sec, tail = rest.split("\n## ", 1)
    return head + CRAFT + sec.rstrip("\n") + "\n\n" + block.strip("\n") + "\n\n## " + tail


def arms_exact(block):
    out, notes = [], []
    for line in block.splitlines():
        if line.startswith("| R46-CL"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            notes.append(f"{cells[0].split()[0]}: {cells[2]}")
            cells[2] = cells[2].split(":")[0].strip("` ")
            out.append("| " + " | ".join(cells) + " |")
        else:
            out.append(line)
    text = "\n".join(out)
    return text.replace("  Refs:", "  Arms: " + " / ".join(notes) + "\n\n  Refs:", 1)


def run(d, freeze, rev, tag, outname):
    out = d + f"/_fx/{outname}.json"
    os.makedirs(d + "/_fx", exist_ok=True)
    env = dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S)
    r = subprocess.run([sys.executable, "-I", "-B", d + "/tools/round-47/exact.py",
                        "--root", d, "--freeze", freeze, "--rev", rev, "--json-out", out],
                       capture_output=True, text=True, env=env)
    rec = json.load(open(out)) if os.path.exists(out) else {}
    if rec:
        shutil.copy(out, f"{OUT}/fixtures/{outname}.json")
    print(f"{tag}: exit {r.returncode} | "
          f"{(rec.get('failing') or rec.get('reason') or 'GREEN')}"
          f"{' | battery ' + json.dumps({k: v for k, v in rec['battery'].items() if k != 'fixtures'}) if isinstance(rec.get('battery'), dict) else ''}"
          f"{' | dirty=' + json.dumps(rec.get('dirty')) if 'dirty' in rec else ''}")
    return r.returncode, rec


res = {}
sk_freeze = show(LANE, FREEZE, "SKILL.md")
block = open(S + "/block24.txt").read().strip("\n")
fixed = arms_exact(block)

# ---- A: body-bound variants (does a column-zero bold line end block 24?) -------------
d = newrepo("fxa")
for name, blk in (
        ("11-later-rule-after-block", fixed + "\n\n- **25. A later rule.** body\n"),
        ("12-inner-bold-in-body", fixed.replace("  Refs:", "- **26. Inner bold.** body\n\n  Refs:", 1)),
        ("13-inner-fenced-bold", fixed.replace("  Refs:", "```\n- **27. Fenced demo.** body\n```\n\n  Refs:", 1))):
    open(d + "/SKILL.md", "w").write(insert_at_craft_end(sk_freeze, blk))
    rev = commit(d, name)
    code, rec = run(d, FREEZE, rev, name, name)
    res[name] = {"exit": code, "rev": rev, "rule_blocks": rec.get("rule_blocks"),
                 "block_is_last": rec.get("block_is_last"), "failing": rec.get("failing")}

# ---- B: a committed claim amendment (frozen path change) at the measured rev ---------
d = newrepo("fxb")
claims = show(LANE, FREEZE, "plans/round-47-claims.md")
open(d + "/plans/round-47-claims.md", "w").write(
    claims.replace("**Causal separability.**",
                   "**Amendment (test).** a post-freeze edit of a frozen path.\n\n"
                   "**Causal separability.**", 1))
open(d + "/SKILL.md", "w").write(insert_at_craft_end(sk_freeze, fixed))
rev = commit(d, "amend-claims-and-land")
code, rec = run(d, FREEZE, rev, "14-frozen-path-changed-committed", "14-frozen-path-changed-committed")
res["14-frozen-path-changed-committed"] = {"exit": code, "rev": rev,
                                          "frozen_path_changed": rec.get("frozen_path_changed")}

# ---- C: uncommitted tamper of tools/round-46/gate.py (NOT a frozen path) -------------
gate = d + "/tools/round-46/gate.py"
orig = open(gate).read()
assert orig.count('"-m", "--diff-merges=first-parent"') == 1
tampered = orig.replace(
    "    if receipt[\"frozen_path_changed\"]:\n"
    "        receipt[\"reason\"] = \"frozen_path_changed\"\n"
    "        return 2, receipt\n", "    return 0, receipt\n", 1)
assert tampered != orig
open(gate, "w").write(tampered)
code, rec = run(d, FREEZE, rev, "15a-gate-tamper-neutered-changed", "15a-gate-tamper-neutered-changed")
res["15a-gate-tamper-neutered-changed"] = {"exit": code, "failing": rec.get("failing"),
                                          "frozen_path_changed": rec.get("frozen_path_changed")}

# ---- D: same tamper, but for the dirty arm, with a dirty frozen file ------------------
open(gate, "w").write(orig)
recp = d + "/tools/round-47/record.py"
open(recp, "a").write("# uncommitted edit of a frozen path\n")
code, rec = run(d, FREEZE, rev, "15b-dirty-frozen-file-committed-gate", "15b-dirty-frozen-file-committed-gate")
res["15b-dirty-frozen-file-committed-gate"] = {"exit": code, "reason": rec.get("reason"),
                                               "dirty": rec.get("dirty")}
open(gate, "w").write(orig.replace(
    '    """Uncommitted paths under the union of the given pathspecs (R45-CL15: union, not replace)."""',
    '    """Uncommitted paths under the union of the given pathspecs (R45-CL15: union, not replace)."""\n'
    "    return []\n", 1))
code, rec = run(d, FREEZE, rev, "15c-gate-tamper-neutered-dirty", "15c-gate-tamper-neutered-dirty")
res["15c-gate-tamper-neutered-dirty"] = {"exit": code, "reason": rec.get("reason"),
                                         "dirty": rec.get("dirty"),
                                         "failing": rec.get("failing")}
open(gate, "w").write(orig)
os.remove(recp) if False else None
sh(["git", "-C", d, "checkout", "--", "tools/round-47/record.py"])

json.dump(res, open(f"{OUT}/fixtures/attack2-summary.json", "w"), indent=1)
