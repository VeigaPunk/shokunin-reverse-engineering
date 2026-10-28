import json, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-46")
import attest, registry  # noqa: E402

ROOT = LANE
REV = "0425224756791b414454df28a9abf93dcdf154ce"
S = os.environ["HYAKU_SCRATCH"]
out = {}
skill = registry.gate.show(ROOT, REV, "SKILL.md")
files = lambda p: registry.gate.show(ROOT, REV, p)  # noqa: E731


# ---------- C1: the citation blind spot, with a landing assertion ----------
spec = attest.SPECS["r46"]
block = [b for b in attest.craft_blocks(skill) if spec["marker"] in b][0]
refs_line = [l for l in block.splitlines() if l.strip().startswith("Refs:")][0]
v = skill.replace(refs_line, refs_line.rstrip() + ", `SKILL.md:12`, `docs/plan.md:3`", 1)
assert "`docs/plan.md:3`" in v and "`SKILL.md:12`" in v, "landing failed"
c, r = attest.score(v, files, "r46", "v2", REV)
out["N1-c1-cite-out-of-tree"] = {"exit": c, "failing": r.get("failing"), "refs": r.get("refs")}

v2 = skill.replace(refs_line, refs_line.rstrip() + ", `SKILL.md`", 1)
assert v2 != skill
c, r = attest.score(v2, files, "r46", "v2", REV)
out["N2-c1-cite-no-selector-out-of-tree"] = {"exit": c, "failing": r.get("failing")}

# removing *every* S142 mention must be red (clause 6 token)
v3 = skill.replace("S142", "S999")
assert "S142" not in v3.split(spec["marker"])[1].split("## ")[0]
c, r = attest.score(v3, files, "r46", "v2", REV)
out["N3-c1-no-S142"] = {"exit": c, "failing": r.get("failing")}

# ---------- C2: ghost row inserted *by line index* ----------------------
rspec = registry.SPECS["r46"]
lines = skill.splitlines()
head_i = [i for i, l in enumerate(lines) if registry.HEAD in l][0]
tail_i = [i for i, l in enumerate(lines) if registry.TAIL in l][0]
sep_i = [i for i in range(head_i, tail_i)
         if lines[i].strip().startswith("|") and registry.is_sep(
             [c.strip() for c in lines[i].strip().strip("|").split("|")])][0]
ghost = ("| `tools/round-41/ghost-tool.py` | probe — a row for a path that exists at "
         "no revision | 0=met; 1=not met; 2=unknown | none | none | none | nobody |")
new = lines[:sep_i + 1] + [ghost] + lines[sep_i + 1:]
v4 = "\n".join(new) + ("\n" if skill.endswith("\n") else "")
assert ghost in v4
c, r = registry.score(v4, files, "r46", "v2", REV)
out["N4-c2-ghost-row-in-section"] = {"exit": c, "failing": r.get("failing"),
                                     "registry_rows": r.get("registry_rows"),
                                     "absent": r.get("absent_at_rev")}
c, r = registry.score(v4, files, "r46", "v1", REV)
out["N5-c2-ghost-row-v1"] = {"exit": c, "failing": r.get("failing")}

# a census row whose *verdict map* is thin but is shadowed by a good duplicate
# (does the first-wins map still let an honest thin row pass?)
path0 = json.loads(files("tools/round-46/census.json"))["paths"][0]
row0 = [l for l in lines[head_i:tail_i] if l.strip().startswith("| `" + path0 + "`")][0]

# ---------- C2: swap that duplicates a v1-green mutation ----------
orig = list(registry.MUTATIONS)
registry.MUTATIONS = [(("off-section-2", "skill", registry.m_off_section)
                       if n == "no-header" else (n, k, f)) for n, k, f in orig]
try:
    b = registry.run_battery(ROOT, REV, "r46", S)
    c, r = registry.score(skill, files, "r46", "v2", REV, battery=b)
    out["N6-c2-swap-no-header-for-off-section"] = {
        "exit": c, "failing": r.get("failing"),
        "battery": {k: v for k, v in b.items() if k != "fixtures"},
        "fixture_names": [f["name"] for f in b.get("fixtures", [])]}
finally:
    registry.MUTATIONS = list(orig)

print(json.dumps(out, indent=1))
