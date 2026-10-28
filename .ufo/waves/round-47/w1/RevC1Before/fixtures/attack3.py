#!/usr/bin/env python3
"""RevC1Before part 3: dirty-arm tamper, self-declared freeze denominator edit, determinism."""
import hashlib
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


def sh(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))


def show(root, rev, path):
    return sh(["git", "-C", root, "show", f"{rev}:{path}"]).stdout


def newrepo(name, at=FREEZE):
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
    return "\n".join(out).replace(
        "  Refs:", "  Arms: " + " / ".join(notes) + "\n\n  Refs:", 1)


def run(d, freeze, rev, outname, tag, extra=()):
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
    print(f"{tag}: exit {r.returncode} | {(rec.get('failing') or rec.get('reason') or 'GREEN')}"
          f" | dirty={rec.get('dirty')}"
          f"{' | battery ' + json.dumps({k: v for k, v in rec['battery'].items() if k != 'fixtures'}) if isinstance(rec.get('battery'), dict) else ''}")
    return r.returncode, rec, out


sk = show(LANE, FREEZE, "SKILL.md")
block = open(S + "/block24.txt").read().strip("\n")
fixed = arms_exact(block)
res = {}

# ---- 15d: pristine tree, dirty frozen file, executed gate.py tampered ---------------
d = newrepo("fxc", at=LANE + "")
sh(["git", "-C", d, "checkout", "-q", FREEZE])
open(d + "/SKILL.md", "w").write(insert_at_craft_end(sk, fixed))
rev = commit(d, "land-fixed")
code, rec, _ = run(d, FREEZE, rev, "15d-baseline-clean", "15d-baseline-clean")
res["15d-baseline-clean"] = {"exit": code, "failing": rec.get("failing")}
open(d + "/tools/round-47/record.py", "a").write("# uncommitted edit of a frozen path\n")
code, rec, _ = run(d, FREEZE, rev, "15e-dirty-frozen-pristine-gate", "15e-dirty-frozen-pristine-gate")
res["15e-dirty-frozen-pristine-gate"] = {"exit": code, "reason": rec.get("reason")}
gate = d + "/tools/round-46/gate.py"
orig = open(gate).read()
open(gate, "w").write(orig.replace(
    '    """Uncommitted paths under the union of the given pathspecs (R45-CL15: union, not replace)."""',
    '    """Uncommitted paths under the union of the given pathspecs (R45-CL15: union, not replace)."""\n'
    "    return []\n", 1))
code, rec, _ = run(d, FREEZE, rev, "15f-dirty-frozen-neutered-dirty-arm", "15f-dirty-frozen-neutered-dirty-arm")
res["15f-dirty-frozen-neutered-dirty-arm"] = {"exit": code, "reason": rec.get("reason"),
                                              "dirty": rec.get("dirty"),
                                              "failing": rec.get("failing")}
open(gate, "w").write(orig)
sh(["git", "-C", d, "checkout", "--", "tools/round-47/record.py"])

# ---- 16: a denominator edit inside the pinned interpreter, self-declared freeze -----
d = newrepo("fxd")
ex = d + "/tools/round-47/exact.py"
body = open(ex).read()
b2 = body.replace(',\n             ("flag-order-drift", _m_flag_order)]', ']', 1)
assert b2 != body
b2 = b2.replace('for key, want in (("forgeries_total", 4), ("v2_green", 4), ("v3_green", 0),',
                'for key, want in (("forgeries_total", 3), ("v2_green", 3), ("v3_green", 0),', 1)
assert '("forgeries_total", 3)' in b2
open(ex, "w").write(b2)
newdigest = hashlib.sha256("\n".join(
    ["substring-arm", "duplicate-routed-id", "stale-mutations-digest"]).encode()).hexdigest()
newpin = hashlib.sha256(b2.encode()).hexdigest()
freeze2 = commit(d, "denominator-edit-plus-declared-freeze")
blk = fixed
blk = blk.replace("mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112",
                  "mutations_sha256:" + newdigest, 1)
blk = blk.replace("interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c",
                  "interpreter_sha256:" + newpin, 1)
assert newdigest in blk and newpin in blk
open(d + "/SKILL.md", "w").write(insert_at_craft_end(sk, blk))
land = commit(d, "land-with-reduced-denominator")
code, rec, _ = run(d, d and freeze2, land, "16-reduced-denominator", "16-reduced-denominator")
res["16-reduced-denominator"] = {"exit": code, "freeze": freeze2, "rev": land,
                                 "mutations_sha256": rec.get("mutations_sha256"),
                                 "mutations_sha256_expected": rec.get("mutations_sha256_expected"),
                                 "battery": {k: v for k, v in (rec.get("battery") or {}).items()
                                             if k != "fixtures"},
                                 "failing": rec.get("failing")}
code1, rec1, _ = run(d, FREEZE, land, "16b-reduced-denominator-old-freeze",
                     "16b-reduced-denominator-old-freeze")
res["16b-reduced-denominator-old-freeze"] = {"exit": code1, "reason": rec1.get("reason"),
                                             "failing": rec1.get("failing")}

# ---- 17: determinism, same rev twice ------------------------------------------------
code_a, rec_a, path_a = run(d, freeze2, land, "17-det-a", "17-determinism-a")
code_b, rec_b, path_b = run(d, freeze2, land, "17-det-b", "17-determinism-b")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
res["17-determinism"] = {"exit_a": code_a, "exit_b": code_b,
                         "sha_a": sha(path_a), "sha_b": sha(path_b),
                         "identical": sha(path_a) == sha(path_b)}

json.dump(res, open(f"{OUT}/fixtures/attack3-summary.json", "w"), indent=1)
