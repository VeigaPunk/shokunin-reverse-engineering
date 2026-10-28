import json, os, re, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-46")
import attest  # noqa: E402

ROOT = LANE
REV = "0425224756791b414454df28a9abf93dcdf154ce"
S = os.environ["HYAKU_SCRATCH"]
spec = attest.SPECS["r46"]
skill = attest.gate.show(ROOT, REV, "SKILL.md")
files = lambda p: attest.gate.show(ROOT, REV, p)  # noqa: E731
out = {}


def sc(text, label):
    c, r = attest.score(text, files, "r46", "v2", REV)
    out[label] = {"exit": c, "failing": r.get("failing", r.get("reason")),
                  "rows": r.get("rows"), "refs": r.get("refs")}
    return c, r


blocks = attest.craft_blocks(skill)
marked = [b for b in blocks if spec["marker"] in b][0]
assert skill.count(marked) == 1, "block not uniquely replaceable"

sc(skill, "P0-baseline")

# ---- CL13(e): a column-zero bullet inside / after the block ------------------
sc(skill.replace(marked, marked + "- **scratch note.** body\n", 1), "P1-bullet-after-block")
first = marked.splitlines()[0]
sc(skill.replace(first, first + "\n- **scratch note.** body", 1), "P2-bullet-inside-block")

# ---- clause 3: row width and exit set (no mutation covers these) ------------
data = [l for l in marked.splitlines() if l.strip().startswith("| R45-CL")]
out["_data_rows"] = len(data)
sc(skill.replace(data[0], data[0].rstrip() + " extra |", 1), "P3-row-five-cells")
sc(skill.replace(data[0], re.sub(r"\| 1 \|$", "| 3 |", data[0].rstrip()), 1), "P4-exit-cell-three")

# ---- clause 5: path set / resolvability / unmatchable citations ------------
refs_line = [l for l in marked.splitlines() if l.strip().startswith("Refs:")][0]
def refs_with(extra, label):
    sc(skill.replace(refs_line, refs_line.rstrip() + extra, 1), label)

refs_with(", `corpus/SOURCES.md:1`", "P5-ref-outside-allow")
refs_with(", `corpus/lessons/nope.md:5`", "P6-ref-absent-at-rev")
refs_with(", `SKILL.md:12`, `docs/plan.md:3`", "P7-ref-unmatchable-prefix")
refs_with(", `tools/round-45/frozen-path-preflight.py:1`", "P8-ref-round45-tool")

# ---- clause 6: the S142 literal (no mutation drops it) ---------------------
sc(skill.replace("Source S142.", "Source (none).", 1), "P9-no-S142")

# ---- positive control: a *different* valid block ---------------------------
row14 = ("| R45-CL13 a restated 44-line artefact with unselectored refs | the citations "
         "were accepted without a selector | refs | 1 |")
variant = skill.replace(data[1], data[1].rstrip() + "\n" + row14, 1)
variant = variant.replace(refs_line, refs_line.rstrip() + ", `corpus/lessons/round-46.md:18-19`", 1)
variant = variant.replace("the clause is exercised from below only",
                          "only the lower bound was ever exercised", 1)
sc(variant, "P10-valid-variant-14-rows")

# ---- Q1: delete / swap a mutation -----------------------------------------
orig = list(attest.MUTATIONS)


def battery(label, muts, spec_mut=None):
    attest.MUTATIONS = muts
    if spec_mut:
        spec_mut()
    try:
        b = attest.run_battery(ROOT, REV, "r46", S)
        c, r = attest.score(skill, files, "r46", "v2", REV, battery=b)
        out[label] = {"exit": c, "failing": r.get("failing", r.get("reason")),
                      "battery": {k: v for k, v in b.items() if k != "fixtures"},
                      "fixture_names": [f["name"] for f in b.get("fixtures", [])]}
    finally:
        attest.MUTATIONS = list(orig)
        attest.SPECS["r46"]["v1_min_rows"] = 8


battery("P11-baseline-battery", orig)
battery("P12-delete-one-mutation",
        [m for m in orig if m[0] != "missing-routed-id"])
battery("P13-swap-mutation-same-count",
        [(n, attest.m_two_markers if n == "missing-routed-id" else f) for n, f in orig])
battery("P14-duplicate-a-mutation",
        orig[:-1] + [("no-vocab-arm", attest.m_self_refs)])
battery("P15-stricter-v1-row-floor",
        orig, lambda: attest.SPECS["r46"].__setitem__("v1_min_rows", 10))
battery("P16-v1-floor-eleven",
        orig, lambda: attest.SPECS["r46"].__setitem__("v1_min_rows", 11))

print(json.dumps(out, indent=1))
