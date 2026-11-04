#!/usr/bin/env python3
"""Critic attacks A and B on R67-C1.  Uses only the shipped instrument code
paths (load_engine, patch_engine, show, prior_pins, gap_rule_model,
disposition_check, subject_root, gaps, diagnostics, nonregular_published)."""
import importlib.util
import json
import shutil
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
FREEZE = "3663e6b21dccf4c4957f459301156664d8b151d6"
REV = "a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92"
S = Path("/fast/scratch/hyaku/kaidoku-r67/CriticClaims")
OUT = S / "o"


def load_counter():
    spec = importlib.util.spec_from_file_location(
        "r67_counter", REPO / "tools/round-67/avm-le-counter.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def attack_a(counter, engine):
    spec_doc = json.loads(engine.show(REPO, FREEZE, "tools/round-50/carriers.json"))
    prior, sources = engine.prior_pins(REPO, FREEZE, spec_doc)
    rows = []
    for c in spec_doc["carriers"]:
        pin = (c.get("sha256") or "").lower()
        rows.append({"id": c["id"], "pin": pin, "pin_in_prior": pin in prior,
                     "carrier_fresh_ok": bool(pin) and pin not in prior})
    full = list(engine.CLAUSES)
    dropped = list(counter.DROPPED_CLAUSES)
    kept = [c for c in full if c not in dropped]
    work = OUT / "a-work"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    # exactly what score() does: rule resolves to an absolute path
    patches = counter.patch_engine(
        engine, (REPO / counter.RULE_V2).resolve(), work)
    abs_rule = engine.GAPRULE
    rel_rule = counter.RULE_V2
    return {
        "attack": "A relabelled-carrier / freshness drop",
        "clause_attacked": "carriers_matched 4 of 4 (freshness dropped by patch)",
        "prior_pins_sources": sources,
        "prior_pin_count": len(prior),
        "per_carrier": rows,
        "all_pins_in_prior": all(r["pin_in_prior"] for r in rows),
        "carrier_fresh_ok_false_for_all": all(not r["carrier_fresh_ok"] for r in rows),
        "clauses_full": full,
        "clauses_patched": kept,
        "dropped_clauses": dropped,
        "patch_recorded_by_instrument": patches,
        "gaprule_after_patch": abs_rule,
        "gaprule_is_absolute": str(abs_rule).startswith("/"),
        "show_absolute_rule_at_freeze": engine.show(REPO, FREEZE, abs_rule) is not None,
        "show_relative_rule_at_freeze": engine.show(REPO, FREEZE, rel_rule) is not None,
        "measured_full_clause_max_matched": 0 if all(
            not r["carrier_fresh_ok"] for r in rows) else "not bounded by freshness",
    }


def rule_of(doc):
    return json.dumps(doc).encode()


def attack_b(counter, engine):
    by_id = {c["id"]: c for c in json.loads(
        engine.show(REPO, FREEZE, "tools/round-50/carriers.json"))["carriers"]}
    v2 = json.loads((REPO / counter.RULE_V2).read_text())
    r50 = json.loads((REPO / counter.RULE_R50).read_text())
    attack = json.loads(json.dumps(v2))
    attack["required"]["symlink"] = False
    attack["class_disposition"]["symlink"] = (
        "attack: waives symlinks too, same shape as the control's junk rule")
    alloff = json.loads(json.dumps(v2))
    for k in alloff["required"]:
        alloff["required"][k] = False
    alloff["class_disposition"]["*"] = "attack: every class not required"
    models = {}
    for name, doc in (("r50", r50), ("v2", v2), ("symlink-waived", attack),
                      ("all-required-off", alloff)):
        m, probs = engine.gap_rule_model(rule_of(doc))
        models[name] = (m, probs)
    per = {}
    envelopes = {}
    for cid, c in by_id.items():
        env = json.loads(engine.show(
            REPO, REV, "corpus/evidence/round-50/c1/%s/after.json" % cid))
        envelopes[cid] = env
        nonreg, nerr = engine.parse_nonregular(
            engine.show(REPO, REV, c["nonregular"]))
        if nerr is not None:
            raise SystemExit("nonregular %s: %s" % (cid, nerr))
        root, how = engine.subject_root(env)
        od = (env.get("parameters") or {}).get("output_directory")
        gaps = engine.gaps(env)
        diags = engine.diagnostics(env)
        row = {"extract_root_source": how}
        for name, (model, _p) in models.items():
            ok, why = engine.disposition_check(gaps, diags, nonreg, model, root, od)
            row[name] = {"gaps_ok": ok, "note": why}
        per[cid] = row
    # red fixture: drop one symlink unpublished-entry gap on the first carrier
    cid = list(by_id)[0]
    c = by_id[cid]
    env = envelopes[cid]
    nonreg, _ = engine.parse_nonregular(engine.show(REPO, REV, c["nonregular"]))
    root, _how = engine.subject_root(env)
    od = (env.get("parameters") or {}).get("output_directory")
    diags = engine.diagnostics(env)
    gaps = engine.gaps(env)
    kinds = {engine.strip_rel(rel): kind for rel, kind, _d in nonreg}
    dropped = None
    kept = []
    for g in gaps:
        rel = engine.extract_rel(g.get("relative_path") or "", root) \
            if g.get("relative_path") else None
        if dropped is None and rel and kinds.get(rel) == "symlink" \
                and g.get("kind") == "unpublished-entry":
            dropped = rel
            continue
        kept.append(g)
    red = {"dropped_symlink_gap": dropped}
    for name, (model, _p) in models.items():
        ok, why = engine.disposition_check(kept, diags, nonreg, model, root, od)
        red[name] = {"gaps_ok": ok, "note": why}
    return {
        "attack": "B rule-scope: a laxer rule is indistinguishable in --score",
        "clause_attacked": "run under the round-67 gap rule",
        "rule_problems": {k: v[1] for k, v in models.items()},
        "per_carrier_gaps_ok": per,
        "gaps_ok_counts": {name: sum(1 for v in per.values() if v[name]["gaps_ok"])
                           for name in models},
        "red_fixture_symlink_removed": red,
        "score_accepts_any_rule_path": True,
        "score_rule_pin_present": False,
        "note": ("the score path only pins the engine (ENGINE_PIN); the rule is "
                 "read at the freeze commit at whatever path --gap-rule names, "
                 "and the receipt records its sha256 but no clause compares it "
                 "to the claims.json pin e66ba0..."),
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    counter = load_counter()
    engine, digest = counter.load_engine(REPO)
    doc = {"engine_sha256": digest,
           "engine_pin": counter.ENGINE_PIN,
           "counter_sha256": counter.sha256_file(
               REPO / "tools/round-67/avm-le-counter.py"),
           "predicate": counter.PREDICATE}
    doc["A"] = attack_a(counter, engine)
    doc["B"] = attack_b(counter, engine)
    (OUT / "attack-A-B-c1.json").write_text(
        json.dumps(doc, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: doc[k] for k in ("A", "B")}, indent=1, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
