#!/usr/bin/env python3
"""RevC1Before part 4: cheap structural checks (no battery) + the A1-freeze before-control."""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Before"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = LANE + "/.ufo/waves/round-47/w1/RevC1Before"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
A1 = "9018c53b16503c8d06d398b75503406508119946"
CRAFT = "## Queue-drain craft "


def sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))


def show(root, rev, path):
    return sh(["git", "-C", root, "show", f"{rev}:{path}"]).stdout


def newrepo(name, at):
    d = S + "/" + name
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", LANE, d])
    sh(["git", "-C", d, "checkout", "-q", at])
    sh(["git", "-C", d, "config", "user.email", "fx@round47"])
    sh(["git", "-C", d, "config", "user.name", "round47 fixture"])
    assert sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip() == d
    return d


def commit(d, msg):
    sh(["git", "-C", d, "add", "-A"])
    r = sh(["git", "-C", d, "commit", "-q", "--allow-empty", "-m", msg])
    assert r.returncode == 0, r.stderr[:200]
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
    return "\n".join(out).replace(
        "  Refs:", "  Arms: " + " / ".join(notes) + "\n\n  Refs:", 1)


def run(d, freeze, rev, outname, tag, extra=("--no-battery",)):
    out = d + f"/_fx/{outname}.json"
    os.makedirs(d + "/_fx", exist_ok=True)
    r = subprocess.run([sys.executable, "-I", "-B", d + "/tools/round-47/exact.py",
                        "--root", d, "--freeze", freeze, "--rev", rev,
                        "--json-out", out, *extra],
                       capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    rec = json.load(open(out)) if os.path.exists(out) else {}
    if rec:
        shutil.copy(out, f"{OUT}/fixtures/{outname}.json")
    print(f"{tag}: exit {r.returncode} | {(rec.get('failing') or rec.get('reason') or 'GREEN')}")
    return r.returncode, rec


res = {}
sk = show(LANE, FREEZE, "SKILL.md")
block = open(S + "/block24.txt").read().strip("\n")
fixed = arms_exact(block)

# --- the before-control scored at the A1 (declared) freeze ---------------------------
d = newrepo("fxe", A1)
code, rec = run(d, A1, A1, "ctl-c1-0-do-nothing-at-A1", "ctl-c1-0-do-nothing-at-A1",
                extra=())
res["ctl-c1-0-do-nothing-at-A1"] = {"exit": code, "rule_blocks": rec.get("rule_blocks"),
                                    "marker_occurrences": rec.get("marker_occurrences"),
                                    "block_present": rec.get("block_present"),
                                    "failing": rec.get("failing")}

# --- structural variants (no battery) ------------------------------------------------
cases = {}
cases["18-marker-quoted-in-fence-elsewhere"] = insert_at_craft_end(
    sk.replace("\n## Queue-drain craft (",
               "\nThe marker is `<!-- exactness-table v3 -->` in a fence.\n\n## Queue-drain craft (", 1),
    fixed)
rows = fixed.splitlines()
two_ids = []
for line in rows:
    if line.startswith("| R46-CL3"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        cells[0] = "R46-CL3 R46-CL6"
        line = "| " + " | ".join(cells) + " |"
    two_ids.append(line)
cases["19-trigger-names-two-ids"] = insert_at_craft_end(sk, "\n".join(two_ids))
exit3 = []
for line in fixed.splitlines():
    if line.startswith("| R46-CL4"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        cells[3] = "3"
        line = "| " + " | ".join(cells) + " |"
    exit3.append(line)
cases["20-exit-cell-3"] = insert_at_craft_end(sk, "\n".join(exit3))
phantom = sk.split(CRAFT, 1)
head, rest = phantom
sec, tail = rest.split("\n## ", 1)
sec = sec.replace("- **23. ", "- **24. Phantom rule that is not rule 24.**\n\n- **23. ", 1)
cases["21-two-blocks-titled-24"] = head + CRAFT + sec.rstrip("\n") + "\n\n" + fixed + "\n\n## " + tail

d = newrepo("fxf", FREEZE)
for name, text in cases.items():
    open(d + "/SKILL.md", "w").write(text)
    rev = commit(d, name)
    code, rec = run(d, FREEZE, rev, name, name)
    res[name] = {"exit": code, "rule_blocks": rec.get("rule_blocks"),
                 "block_is_last": rec.get("block_is_last"),
                 "failing": rec.get("failing")}

json.dump(res, open(f"{OUT}/fixtures/attack4-summary.json", "w"), indent=1)
