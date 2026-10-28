#!/usr/bin/env python3
"""RevC1Before: attack the C1 before-state and the exact.py parser in a fixture repo."""
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Before"
FX = S + "/fx"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = LANE + "/.ufo/waves/round-47/w1/RevC1Before"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
CRAFT = "## Queue-drain craft "
MARKER = "<!-- exactness-table v3 -->"
os.makedirs(OUT + "/fixtures", exist_ok=True)


def git(*args):
    return subprocess.run(["git", "-C", FX, *args], capture_output=True, text=True)


def show(rev, path, root=LANE):
    return subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True, text=True).stdout


def insert_at_craft_end(skill, block):
    head, rest = skill.split(CRAFT, 1)
    sec, tail = rest.split("\n## ", 1)
    return head + CRAFT + sec.rstrip("\n") + "\n\n" + block.strip("\n") + "\n\n## " + tail


def arms_exact(block):
    """Rewrite each v3-arm cell to the bare token, keeping its prose as a note line."""
    out, notes = [], []
    for line in block.splitlines():
        if line.startswith("| R46-CL"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            tok = cells[2].split(":")[0].strip("` ")
            notes.append(f"  {cells[0].split()[0]}: {cells[2]}")
            cells[2] = tok
            out.append("| " + " | ".join(cells) + " |")
        else:
            out.append(line)
    text = "\n".join(out)
    marker = "  Refs:"
    i = text.index(marker)
    return text[:i] + "  Arms: " + " / ".join(n.strip() for n in notes) + "\n\n" + text[i:]


def rows_hole_minus(block):
    out = []
    for line in block.splitlines():
        if line.startswith("| R46-CL"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells[1] = "-"
            out.append("| " + " | ".join(cells) + " |")
        else:
            out.append(line)
    return "\n".join(out)


skill = show(FREEZE, "SKILL.md")
block = open(S + "/block24.txt").read().strip("\n")
fixed = arms_exact(block)

variants = {}
variants["01-genuine-as-landed"] = insert_at_craft_end(skill, block)
variants["02-arms-exact-token"] = insert_at_craft_end(skill, fixed)
variants["03-heading-no-trailing-space"] = variants["02-arms-exact-token"].replace(
    "## Queue-drain craft (rounds 5-12, distilled in round 13)", "## Queue-drain craft", 1)
variants["04-decoy-h3-earlier-real-absent"] = skill.replace(
    "\n## Queue-drain craft (",
    "\n### Queue-drain craft notes\n\n" + fixed.strip("\n") + "\n\n## Queue-drain craft (", 1)
variants["05-fenced-quote-earlier-genuine-at-end"] = insert_at_craft_end(
    skill.replace("\n## Queue-drain craft (",
                  "\nA doc quotes the heading `" + CRAFT + "` verbatim.\n\n") ,
    fixed) if False else insert_at_craft_end(
        skill.replace("\n## Queue-drain craft (",
                      "\n```\n" + CRAFT + "(example heading quoted in a fence)\n```\n\n"
                      "## Queue-drain craft (", 1), fixed)
variants["06-column-zero-bold-in-body"] = variants["02-arms-exact-token"].replace(
    "\n\n  Refs:", "\n\n- **24. A nested rule quoted in the body.** text\n\n  Refs:", 1)
variants["07-fenced-bold-in-body"] = variants["02-arms-exact-token"].replace(
    "\n\n  Refs:", "\n\n```\n- **25. A rule shown inside a fence.** demo\n```\n\n  Refs:", 1)
variants["08-empty-v2-hole-cells"] = insert_at_craft_end(skill, rows_hole_minus(fixed))
variants["09-traversal-ref"] = variants["02-arms-exact-token"].replace(
    "`plans/round-47-claims.md:45-113`", "`corpus/lessons/../../SCORECARD.md:1-5`", 1)
refs_line = [l for l in fixed.splitlines() if l.strip().startswith("Refs:")][0]
dup = ("  Refs: `corpus/lessons/round-46.md:57-66`, `corpus/lessons/round-46.md:57-66`, "
       "`tools/round-47/exact.py`")
variants["10-duplicate-refs"] = insert_at_craft_end(skill, fixed).replace(refs_line, dup, 1)

results = []
base_head = git("rev-parse", "HEAD").stdout.strip()
for name, text in variants.items():
    with open(FX + "/SKILL.md", "w") as fh:
        fh.write(text)
    git("add", "SKILL.md")
    c = git("-c", "user.email=fx@round47", "-c", "user.name=fx", "commit", "-q", "--allow-empty", "-m", name)
    if c.returncode != 0:
        print("commit failed", name, c.stderr[:200])
        sys.exit(1)
    rev = git("rev-parse", "HEAD").stdout.strip()
    out = FX + f"/_fx/{name}.json"
    os.makedirs(FX + "/_fx", exist_ok=True)
    r = subprocess.run([sys.executable, "-I", "-B", FX + "/tools/round-47/exact.py",
                        "--root", FX, "--freeze", FREEZE, "--rev", rev,
                        "--json-out", out], capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    rec = {}
    if os.path.exists(out):
        rec = json.load(open(out))
        shutil.copy(out, f"{OUT}/fixtures/{name}.json")
    results.append({"variant": name, "rev": rev, "exit": r.returncode,
                    "rule_blocks": rec.get("rule_blocks"),
                    "marker_occurrences": rec.get("marker_occurrences"),
                    "block_present": rec.get("block_present"),
                    "block_is_last": rec.get("block_is_last"),
                    "failing": rec.get("failing"),
                    "reason": rec.get("reason"),
                    "battery": rec.get("battery"),
                    "unresolved": rec.get("unresolved_citations")})
    print(name, "exit", r.returncode, "|", (rec.get("failing") or rec.get("reason") or "GREEN"))

json.dump(results, open(f"{OUT}/fixtures/attack-summary.json", "w"), indent=1)
print("\nHEAD", git("rev-parse", "HEAD").stdout.strip(), "from", base_head)
