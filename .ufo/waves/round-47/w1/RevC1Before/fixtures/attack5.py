#!/usr/bin/env python3
"""RevC1Before part 5: re-run the decisive attacks on the CURRENT landed block at the A6 freeze."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/RevC1Before"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = LANE + "/.ufo/waves/round-47/w1/RevC1Before"
A6 = "f54b3b6de9085d3db449ed5d0916296cb29c1f6d"
HEAD = "31b092d17e77f5064c919383a9bc1e6cbfd2d1ff"
CRAFT = "## Queue-drain craft "
MARKER = "<!-- exactness-table v3 -->"
HARD = re.compile(r"((?:corpus|plans|tools)/[A-Za-z0-9._/-]+)(?::(\d+)(?:-(\d+))?)?")


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def show(rev, path):
    return sh(["git", "-C", LANE, "show", f"{rev}:{path}"]).stdout


def newrepo(name, at=A6):
    d = S + "/" + name
    shutil.rmtree(d, ignore_errors=True)
    sh(["git", "clone", "-q", "--shared", LANE, d])
    sh(["git", "-C", d, "checkout", "-q", at])
    for k, v in (("user.email", "fx@round47"), ("user.name", "round47 fixture")):
        sh(["git", "-C", d, "config", k, v])
    assert sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip() == d
    return d


def commit(d, msg):
    sh(["git", "-C", d, "add", "-A"])
    r = sh(["git", "-C", d, "commit", "-q", "--allow-empty", "-m", msg])
    assert r.returncode == 0, r.stderr[:200]
    return sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()


def run(d, freeze, rev, outname, tag, extra=()):
    out = d + f"/_fx/{outname}.json"
    os.makedirs(d + "/_fx", exist_ok=True)
    r = subprocess.run([sys.executable, "-I", "-B", d + "/tools/round-47/exact.py",
                        "--root", d, "--freeze", freeze, "--rev", rev,
                        "--json-out", out, *extra], capture_output=True, text=True,
                       env=dict(os.environ, HYAKU_SCRATCH=S, TMPDIR=S))
    rec = json.load(open(out)) if os.path.exists(out) else {}
    if rec:
        shutil.copy(out, f"{OUT}/fixtures/{outname}.json")
    first = (rec.get("failing") or ["GREEN"])[0] if not rec.get("reason") else rec["reason"]
    print(f"{tag}: exit {r.returncode} | {str(first)[:110]}")
    return r.returncode, rec


def craft_span(skill):
    head, rest = skill.split(CRAFT, 1)
    sec, tail = rest.split("\n## ", 1)
    return head, sec, tail


skill_head = show(HEAD, "SKILL.md")
h, sec, tail = craft_span(skill_head)
blocks = re.split(r"(?m)^- \*\*", sec)[1:]
marker_blocks = [b for b in blocks if MARKER in b]
assert len(marker_blocks) == 1, len(marker_blocks)
block_text = "- **" + marker_blocks[0].rstrip("\n") + "\n"
res = {}
print("landed block chars", len(block_text), "rows",
      len([l for l in block_text.splitlines() if l.startswith("| R46-CL")]))

d = newrepo("fxg")

# ---- baseline: the current landed block at the A6 freeze ----------------------------
open(d + "/SKILL.md", "w").write(skill_head)
rev0 = commit(d, "landing-as-at-" + HEAD[:8])
code, rec = run(d, A6, rev0, "P0-baseline-head-block", "P0-baseline")
res["P0-baseline-head-block"] = {"exit": code, "rev": rev0, "refs": rec.get("refs"),
                                 "arm_tokens": rec.get("arm_tokens"),
                                 "failing": rec.get("failing")}

# ---- P1: the block lives in an earlier `### Queue-drain craft notes`, real H2 empty --
stripped = skill_head.replace(block_text, "", 1)
assert MARKER not in stripped.split(CRAFT)[1].split("\n## ")[0]
p1 = stripped.replace("\n## Queue-drain craft (",
                      "\n### Queue-drain craft notes\n\n" + block_text.strip("\n") +
                      "\n\n## Queue-drain craft (", 1)
open(d + "/SKILL.md", "w").write(p1)
rev = commit(d, "P1-decoy-h3")
code, rec = run(d, A6, rev, "P1-decoy-h3-real-section-absent", "P1-decoy-h3")
res["P1-decoy-h3-real-section-absent"] = {"exit": code, "rev": rev,
                                          "rule_blocks": rec.get("rule_blocks"),
                                          "block_present": rec.get("block_present"),
                                          "failing": rec.get("failing")}

# ---- P2: every v2-hole cell says nothing -------------------------------------------
holes = []
for line in block_text.splitlines():
    if line.startswith("| R46-CL"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        cells[1] = "-"
        line = "| " + " | ".join(cells) + " |"
    holes.append(line)
open(d + "/SKILL.md", "w").write(skill_head.replace(block_text, "\n".join(holes) + "\n", 1))
rev = commit(d, "P2-empty-hole-cells")
code, rec = run(d, A6, rev, "P2-empty-hole-cells", "P2-empty-hole-cells")
res["P2-empty-hole-cells"] = {"exit": code, "rev": rev, "failing": rec.get("failing")}

# ---- P3: three citations, one document repeated ------------------------------------
refs = [l for l in block_text.splitlines() if l.strip().startswith("Refs:")][0]
one_doc = "  Refs: `corpus/lessons/round-46.md:57-66`, `corpus/lessons/round-46.md:21`, `plans/round-47-claims.md:118`\n"
open(d + "/SKILL.md", "w").write(skill_head.replace(refs, one_doc.strip("\n"), 1))
rev = commit(d, "P3-two-documents-repeated")
code, rec = run(d, A6, rev, "P3-three-citations-two-documents", "P3-three-citations-two-documents")
res["P3-three-citations-two-documents"] = {"exit": code, "rev": rev, "refs": rec.get("refs"),
                                           "cited": rec.get("cited"), "failing": rec.get("failing")}

# ---- P4: a phantom block titled 24 before the real one ------------------------------
open(d + "/SKILL.md", "w").write(
    skill_head.replace("- **23. ", "- **24. Phantom rule.** body\n\n- **23. ", 1))
rev = commit(d, "P4-two-blocks-titled-24")
code, rec = run(d, A6, rev, "P4-two-blocks-titled-24", "P4-two-blocks-titled-24")
res["P4-two-blocks-titled-24"] = {"exit": code, "rev": rev, "rule_blocks": rec.get("rule_blocks"),
                                  "failing": rec.get("failing")}

# ---- P5/P6: traps that redden a legitimate landing ---------------------------------
open(d + "/SKILL.md", "w").write(skill_head.replace(
    block_text, block_text + "\n- **25. A later rule.** body\n", 1))
rev = commit(d, "P5-later-rule")
code, rec = run(d, A6, rev, "P5-later-rule", "P5-later-rule")
res["P5-later-rule"] = {"exit": code, "rev": rev, "failing": rec.get("failing")}

open(d + "/SKILL.md", "w").write(skill_head.replace(
    "\n## Queue-drain craft (", "\nThe marker is `" + MARKER + "`.\n\n## Queue-drain craft (", 1))
rev = commit(d, "P6-marker-quoted")
code, rec = run(d, A6, rev, "P6-marker-quoted-elsewhere", "P6-marker-quoted-elsewhere")
res["P6-marker-quoted-elsewhere"] = {"exit": code, "rev": rev, "failing": rec.get("failing")}

# ---- P7: frozen-path change, then an uncommitted edit of the executed gate.py ------
d2 = newrepo("fxh")
claims = show(A6, "plans/round-47-claims.md")
open(d2 + "/plans/round-47-claims.md", "w").write(
    claims.replace("**Causal separability.**",
                   "**Amendment (test).** a post-freeze edit of a frozen path.\n\n"
                   "**Causal separability.**", 1))
open(d2 + "/SKILL.md", "w").write(skill_head)
rev2 = commit(d2, "P7-frozen-path-changed")
code, rec = run(d2, A6, rev2, "P7-frozen-path-changed", "P7-frozen-path-changed")
res["P7-frozen-path-changed"] = {"exit": code, "rev": rev2,
                                 "frozen_path_changed": rec.get("frozen_path_changed")}
gate = d2 + "/tools/round-46/gate.py"
orig = open(gate).read()
open(gate, "w").write(orig.replace(
    "    if receipt[\"frozen_path_changed\"]:\n"
    "        receipt[\"reason\"] = \"frozen_path_changed\"\n"
    "        return 2, receipt\n", "    return 0, receipt\n", 1))
code, rec = run(d2, A6, rev2, "P7b-gate-tamper", "P7b-gate-tamper")
res["P7b-gate-tamper"] = {"exit": code, "rev": rev2, "failing": rec.get("failing"),
                          "frozen_path_changed": rec.get("frozen_path_changed")}
open(gate, "w").write(orig)

# ---- P8: denominator edit inside the pinned interpreter + self-declared freeze ------
d3 = newrepo("fxi")
ex = d3 + "/tools/round-47/exact.py"
body = open(ex).read()
b2 = body.replace(',\n             ("flag-order-drift", _m_flag_order)]', ']', 1)
assert b2 != body
b2 = b2.replace('(("forgeries_total", 4), ("v2_green", 4), ("v3_green", 0),',
                '(("forgeries_total", 3), ("v2_green", 3), ("v3_green", 0),', 1)
assert '("forgeries_total", 3)' in b2
open(ex, "w").write(b2)
dig = hashlib.sha256("\n".join(["substring-arm", "duplicate-routed-id",
                                "stale-mutations-digest"]).encode()).hexdigest()
pin = hashlib.sha256(b2.encode()).hexdigest()
freeze2 = commit(d3, "P8-denominator-edit")
blk = block_text
blk = re.sub(r"mutations_sha256:[0-9a-f]{64}", "mutations_sha256:" + dig, blk, count=1)
blk = re.sub(r"interpreter_sha256:[0-9a-f]{64}", "interpreter_sha256:" + pin, blk, count=1)
open(d3 + "/SKILL.md", "w").write(skill_head.replace(block_text, blk, 1))
land = commit(d3, "P8-land")
code, rec = run(d3, freeze2, land, "P8-reduced-denominator", "P8-reduced-denominator")
res["P8-reduced-denominator"] = {"exit": code, "freeze": freeze2, "rev": land,
                                 "battery": {k: v for k, v in (rec.get("battery") or {}).items()
                                             if k != "fixtures"},
                                 "mutations_sha256": rec.get("mutations_sha256"),
                                 "mutations_sha256_expected": rec.get("mutations_sha256_expected"),
                                 "failing": rec.get("failing")}
code, rec = run(d3, A6, land, "P8b-reduced-denominator-A6-freeze", "P8b-under-A6-freeze")
res["P8b-reduced-denominator-A6-freeze"] = {"exit": code, "rev": land,
                                            "reason": rec.get("reason"),
                                            "failing": rec.get("failing")}

json.dump(res, open(f"{OUT}/fixtures/attack5-summary.json", "w"), indent=1)
