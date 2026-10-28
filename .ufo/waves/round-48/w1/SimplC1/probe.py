#!/usr/bin/env python3
"""SimplC1 probe — score() a fully-good artefact over real rev bytes; class probes."""
import json, sys, os
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = sys.argv[1]
sys.path.insert(0, os.path.join(LANE, "tools/round-48"))
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
import meanings as M

files = lambda p: M.gate.show(LANE, FREEZE, p)
out = {}

# --- A: census_rederive return type vs doc["paths"] (post-A3 shape) ---------------
derived = M.census_rederive(files)
doc = M.census_doc(files)
out["types"] = {
    "derived_type": type(derived).__name__,
    "doc_paths_type": type(doc["paths"]).__name__,
    "derived_paths_eq_doc_paths(line437)": derived.get("paths") == doc["paths"],
    "derived_eq_whole_doc": derived == doc,
    "named_but_absent": derived.get("named_but_absent"),
}

# --- B: a fully-good artefact scored over REAL freeze bytes -----------------------
paths = doc["paths"]
skill = M.skill_text(M.good_block(), M.good_registry(paths))
code, rec = M.score(skill, files, "v3", FREEZE, battery=None)
out["good_artefact"] = {
    "code": code, "met_target": rec.get("met_target"),
    "census_rederived_equal": rec.get("census_rederived_equal"),
    "registry_rows": rec.get("registry_rows"), "census_paths": rec.get("census_paths"),
    "meaning_rows_failed": rec.get("meaning_rows_failed"),
    "unresolved_citations": rec.get("unresolved_citations"),
    "refs": rec.get("refs"), "cited": rec.get("cited"),
    "failing": rec.get("failing"),
}

# --- C: meaning_classes() on crafted cells ---------------------------------------
cells = {
    "genuine": "0=met, the target holds; 1=not met, a clause is false; 2=could-not-evaluate, the revision is unusable",
    "negated_zero(A4 now red)": "0=not met; 1=violation; 2=usage",
    "forged_1eq_measured": "0=met; 1=measured; 2=error",
    "forged_1eq_scored": "0=met; 1=scored; 2=usage",
    "forged_1eq_prepared": "0=met; 1=prepared; 2=absent",
    "forged_1eq_failureware": "0=met; 1=failureware; 2=usage",
    "dup_genuine": "0=met, the target holds; 1=met, the target holds; 2=could-not-evaluate, the revision is unusable",
}
out["meaning_classes"] = {k: M.meaning_classes(v) for k, v in cells.items()}

# --- D: end-to-end: one registry row with a 'measured' not-met meaning ------------
bad_verdict = "0=met; 1=measured; 2=error"
skill2 = M.skill_text(M.good_block(), M.good_registry(paths, bad_verdict))
code2, rec2 = M.score(skill2, files, "v3", FREEZE, battery=None)
out["measured_endtoend"] = {"code": code2, "meaning_rows_failed": rec2.get("meaning_rows_failed"),
                            "meaning_failures": rec2.get("meaning_failures"),
                            "failing": rec2.get("failing")}

# --- E: MUST_KNOW dead conjunct + SELF-selector exemption --------------------------
# E1: knowledge citation absent -> fires anyway (cited nonempty iff HARD_REF matched)
refs_noknow = ("`corpus/lessons/round-47.md:30-50`, `corpus/lessons/round-46.md:57-66`, "
               "`plans/round-48-claims.md:20`, `plans/round-48-claims.md:40`, "
               "`tools/round-48/census2.json:1`")
skill3 = M.skill_text(M.good_block(refs=refs_noknow), M.good_registry(paths))
code3, rec3 = M.score(skill3, files, "v3", FREEZE, battery=None)
out["must_know_absent"] = {"code": code3, "failing": rec3.get("failing")}
# E2: the conjunct's truth value is constant given cited non-empty
out["hard_ref_search_truthy_when_cited"] = bool(M.HARD_REF.search(M.good_block()))
# E3: SELF cited with NO selector: exempt from selector + existence checks
refs_self = GOOD = ("`tools/round-48/meanings.py`, `corpus/lessons/round-47.md:30-50`, "
                    "`corpus/lessons/round-46.md:57-66`, "
                    "`corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`, "
                    "`plans/round-48-claims.md:20`")
skill4 = M.skill_text(M.good_block(refs=refs_self), M.good_registry(paths))
code4, rec4 = M.score(skill4, files, "v3", FREEZE, battery=None)
out["self_noselector"] = {"code": code4, "refs": rec4.get("refs"),
                          "unresolved": rec4.get("unresolved_citations"),
                          "failing": rec4.get("failing")}

# --- F: mutation protocol dead channels ------------------------------------------
out["mutations"] = {
    "names": [n for n, _ in M.MUTATIONS],
    "mut_digest": M.MUT_DIGEST,
    "overrides_all_empty_dict": all(fn(skill, None)[1] == {} for _, fn in M.MUTATIONS),
}

# --- G: v2/v3 discrimination on real mutation output over REAL rev bytes -----------
base = M._fixture_files(LANE, FREEZE)
base["SKILL.md"] = skill
fx = lambda p: base.get(p)
g = {}
for name, fn in M.MUTATIONS:
    text, _ = fn(skill, None)
    c2, r2 = M.score(text, fx, "v2", FREEZE, battery=None)
    c3, r3 = M.score(text, fx, "v3", FREEZE, battery=None)
    g[name] = {"v2_exit": c2, "v3_exit": c3, "changed": text != skill,
               "v2_failing": r2.get("failing", r2.get("reason")),
               "v3_failing": r3.get("failing", r3.get("reason"))}
out["forgery_exits_over_real_bytes"] = g

print(json.dumps(out, indent=1, sort_keys=True))
