import json, os, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-46")
import registry  # noqa: E402

ROOT = LANE
REV = "0425224756791b414454df28a9abf93dcdf154ce"
S = os.environ["HYAKU_SCRATCH"]
spec = registry.SPECS["r46"]
skill = registry.gate.show(ROOT, REV, "SKILL.md")
files = lambda p: registry.gate.show(ROOT, REV, p)  # noqa: E731
out = {}


def sc(text, label, profile="v2"):
    c, r = registry.score(text, files, "r46", profile, REV)
    out[label] = {"profile": profile, "exit": c,
                  "failing": r.get("failing", r.get("reason")),
                  "registered": len(r.get("registered", [])),
                  "registry_rows": r.get("registry_rows"),
                  "absent": r.get("absent_at_rev"), "thin": r.get("thin")}
    return c, r


sc(skill, "Q0-baseline")

mid, err = registry.split_section(skill, spec)
assert err is None, err
lines = skill.splitlines()
sep = [i for i, l in enumerate(lines)
       if l.strip().startswith("|") and registry.is_sep(
           [c.strip() for c in l.strip().strip("|").split("|")])]
head_i = [i for i, l in enumerate(lines) if registry.HEAD in l][0]
first_sep = min(i for i in sep if i > head_i)
ghost = ("| `tools/round-41/ghost-tool.py` | probe — a row for a path that exists at "
         "no revision | 0=met; 1=not met; 2=unknown | none | none | none | nobody |")
sc(skill.replace(lines[first_sep], lines[first_sep] + "\n" + ghost, 1), "Q1-ghost-row-v2")
sc(skill.replace(lines[first_sep], lines[first_sep] + "\n" + ghost, 1), "Q2-ghost-row-v1", "v1")

# a census path removed from the section: must be unregistered
census = json.loads(files("tools/round-46/census.json"))
paths = census["paths"] if isinstance(census, dict) else census
victim = paths[0]
row = [l for l in lines if l.strip().startswith("| `" + victim + "`")][0]
sc(skill.replace(row + "\n", "", 1), "Q3-drop-census-row")

orig = list(registry.MUTATIONS)


def battery(label, muts):
    registry.MUTATIONS = muts
    try:
        b = registry.run_battery(ROOT, REV, "r46", S)
        c, r = registry.score(skill, files, "r46", "v2", REV, battery=b)
        out[label] = {"exit": c, "failing": r.get("failing", r.get("reason")),
                      "battery": {k: v for k, v in b.items() if k != "fixtures"},
                      "fixture_names": [f["name"] for f in b.get("fixtures", [])]}
    finally:
        registry.MUTATIONS = list(orig)


battery("Q4-baseline-battery", orig)
battery("Q5-delete-one-mutation", [m for m in orig if m[0] != "no-header"])
battery("Q6-swap-mutation-same-count",
        [(n, k, registry.m_fenced if n == "no-header" else f) for n, k, f in orig])
print(json.dumps(out, indent=1))
