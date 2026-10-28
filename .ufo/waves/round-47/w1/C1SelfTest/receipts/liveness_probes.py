#!/usr/bin/env python3
"""R47 C1SelfTest — liveness probes for the clauses no selftest case covers.

For each uncovered clause, build one artefact whose ONLY defect that clause names, score
it with the frozen counter's v3 profile, then score the identical artefact with the clause
deleted.  frozen=1 / deleted=0 proves the clause is a live, exclusively-responsible guard
(an uncovered guard).  frozen=0 would prove it dead.

The interpreter pin is the reason each fixture stages its own exact.py bytes: score()
compares interpreter_sha256 against the file at rev, so a fixture carrying the frozen
bytes would report a pin mismatch unrelated to the defect under test.

Also records, for the landing drafter, the citation floor the frozen counter actually
enforces (clause 8 waives the line selector for the self token but still counts it in
`refs >= 3`).

Usage: HYAKU_SCRATCH=<scratch> python3 -B liveness_probes.py <lane-root> <scratch> <out.json>
"""
import hashlib
import importlib.util
import json
import os
import shutil
import sys

LANE, S, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.environ["TMPDIR"] = S
os.environ["HYAKU_SCRATCH"] = S


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


FROZEN = load(os.path.join(LANE, "tools/round-47/exact.py"), "exact_frozen")
MUTATED = {}
for slug in ("C1-block-is-last", "C3-four-cells", "C3-exit-set", "C4-one-id-per-row",
             "C6-mutation-names", "C8-refs-floor", "C8-must-cite", "C8-allowlist",
             "C9-battery-counts", "C5-arm-exact", "Z-malformed-branch"):
    p = os.path.join(S, slug, "tools/round-47/exact.py")
    if os.path.exists(p):
        MUTATED[slug] = load(p, "m_" + slug.replace("-", "_"))


def probe(mod, kw=None, smut=None, profile="v3", battery=None):
    """Score one artefact built from `mod`, staging `mod`'s own bytes as the interpreter."""
    files = {"plans/round-47-claims.md": mod.CLAIMS_BODY,
             "corpus/lessons/round-46.md": "lesson line\n" * 240,
             "tools/round-47/exact.py": open(mod.__file__).read(),
             "tools/round-46/gate.py": open(mod.gate.__file__).read()}
    block = mod.good_block(**(kw or {}))
    skill = mod.skill_text(block)
    if smut:
        skill = smut(skill, block)
    files["SKILL.md"] = skill
    d = None
    try:
        d, rev = mod._repo(files, S, prefix="probe-")
        code, rec = mod.score(skill, lambda p: mod.gate.show(d, rev, p), profile, rev,
                              battery=battery)
        return {"exit": code, "failing": rec.get("failing") or rec.get("reason") or "CLEAN",
                "refs": rec.get("refs"), "cited": rec.get("cited")}
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)


R = FROZEN
PB = {
 "C1-block-is-last": ("a second craft block after the marked one", {}, lambda t, b: t.replace(
     "\n## Next section", "- **25. A later rule.** body\n\n## Next section")),
 "C3-four-cells": ("a five-cell row with a valid exit cell",
     {"rows": R.GOOD_ROWS[:3] + [("R46-CL6", "hole", "order", "1", "extra")]}, None),
 "C3-exit-set": ("exit cell `3`",
     {"rows": R.GOOD_ROWS[:3] + [("R46-CL6", "hole", "order", "3")]}, None),
 "C4-one-id-per-row": ("one row names two ids, another names none", {"rows": [
     ("R46-CL2 R46-CL3", "hole", "symbol", "1"), ("R46-CL4", "hole", "digest", "1"),
     ("R46-CL6", "hole", "order", "1"), ("no routed id", "hole", "order", "1")]}, None),
 "C6-mutation-names": ("block drops the name `flag-order-drift`", {}, lambda t, b: t.replace(
     " substring-arm, duplicate-routed-id, stale-mutations-digest, flag-order-drift",
     " substring-arm, duplicate-routed-id, stale-mutations-digest")),
 "C8-refs-floor": ("one line-selected citation only", {"refs": "`corpus/lessons/round-46.md:10-30`"}, None),
 "C8-must-cite": ("three resolving refs, none of them round-46.md", {"refs":
     "`plans/round-47-claims.md:20`, `plans/round-47-claims.md:21`, `plans/round-47-claims.md:22`"}, None),
 "C8-allowlist": ("a resolving ref outside ALLOW (tools/round-46/gate.py:1)", {"refs":
     R.GOOD_REFS.replace("plans/round-47-claims.md:20", "tools/round-46/gate.py:1")}, None),
 "C9-battery-counts": ("battery.forgeries_total=3", {}, None),
}
BAD_BATTERY = {"forgeries_total": 3, "v2_green": 4, "v3_green": 0,
               "genuine_green": 1, "crash": 0}

out = {"driver": os.path.abspath(__file__),
       "driver_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
       "frozen_exact_sha256": hashlib.sha256(open(FROZEN.__file__, "rb").read()).hexdigest(),
       "probes": [], "attacks": []}

for slug, (defect, kw, smut) in PB.items():
    bat = BAD_BATTERY if slug == "C9-battery-counts" else None
    f = probe(FROZEN, kw, smut, battery=bat)
    m = probe(MUTATED[slug], kw, smut, battery=bat)
    verdict = ("LIVE-EXCLUSIVE (uncovered)" if f["exit"] == 1 and m["exit"] == 0
               else "DEAD" if f["exit"] == 0 else "NOT-ISOLATED")
    out["probes"].append({"clause": slug, "defect": defect, "frozen": f,
                          "clause_deleted": m, "verdict": verdict})
    print(f"{slug:20s} frozen={f['exit']} {str(f['failing'])[:66]:66s} deleted={m['exit']} {verdict}")

# --- attacks a landing drafter needs to know about --------------------------------
out["attacks"].append({"name": "citation-floor-two-selected",
    "claim": "clause 8: at least three citations carry a line selector",
    **probe(FROZEN, {"refs": "`corpus/lessons/round-46.md:10-30`, "
                             "`corpus/lessons/round-46.md:40-60`"})})
out["attacks"].append({"name": "citation-floor-one-selected",
    **probe(FROZEN, {"refs": "`corpus/lessons/round-46.md:10-30`"})})


def move_names(t, b):
    t = t.replace(" names substring-arm, duplicate-routed-id, stale-mutations-digest, "
                  "flag-order-drift.", ".")
    return t.replace("  Refs:", "  (aside, no structure: substring-arm / duplicate-routed-id / "
                     "stale-mutations-digest / flag-order-drift)\n  Refs:")


out["attacks"].append({"name": "mutation-names-as-loose-words", **probe(FROZEN, smut=move_names)})
out["attacks"].append({"name": "no-craft-section-exit-2",
    **probe(FROZEN, smut=lambda t, b: t.replace("## Queue-drain craft (test) ",
                                                "## Something else "))})
out["attacks"].append({"name": "selector-out-of-range",
    **probe(FROZEN, {"refs": R.GOOD_REFS.replace(":10-30", ":230-400")})})
out["attacks"].append({"name": "malformed-heading-still-2-without-the-branch",
    **probe(MUTATED["Z-malformed-branch"],
            smut=lambda t, b: t.replace("## Queue-drain craft (test) ",
                                        "## Queue-drain craft"))})
out["attacks"].append({"name": "five-rows", **probe(FROZEN, {
    "rows": R.GOOD_ROWS + [("R46-CL7", "extra", "order", "1")]})})
out["attacks"].append({"name": "three-rows", **probe(FROZEN, {"rows": R.GOOD_ROWS[:3]})})

for a in out["attacks"]:
    print(f"attack {a['name']:44s} exit={a['exit']} {str(a['failing'])[:60]}")
json.dump(out, open(OUT, "w"), indent=1)
print("LIVE-EXCLUSIVE:", sum(p["verdict"].startswith("LIVE") for p in out["probes"]),
      "of", len(out["probes"]))
