#!/usr/bin/env python3
"""R67-C1 independent gap audit (seat ExecGapAudit, round-67 w1).

Imports the pinned round-50 scoring engine by path and applies the two frozen
gap rules directly.  The round-67 wrapper (tools/round-67/avm-le-counter.py) is
NOT imported: this re-derives the per-carrier gap accounting from the engine's
own primitives plus a local recount of the disposition families.

Outputs audit.json next to this script.  Read-only over the repo; the only
writes are the named output file (and nothing under /tmp).
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
ENGINE = REPO / "tools/round-50/c1-counter.py"
ENGINE_PIN = "9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813"
RULES = {
    "round-50": REPO / "tools/round-50/gap-rule.json",
    "round-67": REPO / "tools/round-67/gap-rule-v2.json",
}
RULE_PINS = {
    "round-50": "43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef",
    "round-67": "e66ba022ee3607c9fe74f141902c012b2418ad6d800589b6d2fb888084a4169e",
}
CARRIERS = REPO / "tools/round-50/carriers.json"
BASE_REV = "a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92"
FREEZE_REV = "3663e6b21dccf4c4957f459301156664d8b151d6"
AFTERDIR = "corpus/evidence/round-50/c1"
IDS = ("g7581", "g7582", "c6490", "c6430")
OUT = Path(__file__).with_name("audit.json")


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest() if raw is not None else None


def load_engine():
    digest = sha_bytes(ENGINE.read_bytes())
    if digest != ENGINE_PIN:
        raise SystemExit("engine pin mismatch: %s" % digest)
    spec = importlib.util.spec_from_file_location("c1_counter_r50_audit", ENGINE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod, digest


def show(rev, path):
    p = subprocess.run(["git", "-C", str(REPO), "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def recount(mod, nonreg, gaps_list, diags, model, root, output_directory):
    """Independent replay of the three disposition families.

    Returns the resolved sets plus every violation the engine's boolean would
    encode, without calling disposition_check for the answer.
    """
    allowed = model.get("allowed") or {}
    structural = model.get("structural") or {}
    required = model.get("required") or {}
    removed = model.get("removed") or {}

    by_rel = {rel: (kind, detail) for rel, kind, detail in nonreg}
    rows_at = {}
    for rel, _kind, _detail in nonreg:
        rows_at.setdefault(mod.strip_rel(rel), []).append(rel)

    gapped = {}            # row rel -> [gap kinds]
    structural_counts = Counter()
    violations = []
    unresolved_gaps = []
    gap_kind_counts = Counter()
    for g in gaps_list:
        if not isinstance(g, dict):
            violations.append("non-object gap")
            continue
        kind = g.get("kind")
        rp = g.get("relative_path")
        gap_kind_counts[str(kind)] += 1
        if rp is None:
            if kind not in structural:
                violations.append("structural gap kind %r not allowed" % (kind,))
                continue
            structural_counts[kind] += 1
            continue
        if kind in structural:
            violations.append("structural kind %r carries a path %r" % (kind, rp))
            continue
        rel_in_root = mod.extract_rel(rp, root)
        hits = rows_at.get(rel_in_root, []) if rel_in_root else []
        if len(hits) != 1:
            unresolved_gaps.append({"relative_path": rp, "resolved_rel": rel_in_root,
                                    "hits": len(hits)})
            violations.append("gap path %r matches %d non-regular entries"
                              % (rp, len(hits)))
            continue
        entry_kind = by_rel[hits[0]][0]
        if kind not in allowed.get(entry_kind, []):
            violations.append("gap kind %r not allowed for %r entry %r"
                              % (kind, entry_kind, hits[0]))
            continue
        gapped.setdefault(hits[0], []).append(kind)

    for kind, n in structural_counts.items():
        if n > structural[kind]:
            violations.append("structural gaps %r: %d > %d" % (kind, n, structural[kind]))

    removal_name = removed.get("diagnostic")
    removal_kinds = removed.get("kinds") or []
    removed_rels = {}
    removal_paths = []
    removal_problems = []
    for d in diags:
        if mod.diagnostic_typename(d) != removal_name:
            continue
        rel = mod.diagnostic_rel(d, root, output_directory)
        if rel is None:
            removal_problems.append({"diagnostic": d.get("report"), "problem": "unresolved"})
            violations.append("removal diagnostic not resolvable under the root")
            continue
        hits = rows_at.get(rel, [])
        if len(hits) != 1:
            removal_problems.append({"rel": rel, "problem": "matches %d rows" % len(hits)})
            violations.append("removal resolves to %d non-regular entries at %r"
                              % (len(hits), rel))
            continue
        entry_kind = by_rel[hits[0]][0]
        if entry_kind not in removal_kinds:
            removal_problems.append({"rel": hits[0], "kind": entry_kind,
                                     "problem": "kind not in removed.kinds"})
            violations.append("removal at %r names a %r entry" % (rel, entry_kind))
            continue
        if gapped.get(hits[0]):
            removal_problems.append({"rel": hits[0], "problem": "also gapped"})
            violations.append("entry %r is both gapped and removed" % (hits[0],))
            continue
        removed_rels[hits[0]] = removed_rels.get(hits[0], 0) + 1
        removal_paths.append({"path": hits[0], "kind": entry_kind,
                              "target": (d.get("report") or {}).get("target")})

    # Entry classes the rule can ever ask about: kinds that allow at least one
    # gap kind. `dir` (and any kind with allowed == []) is tree-shape only and
    # outside the disposition accounting by construction.
    entry_classes = {k for k, v in allowed.items() if v}
    silent_admitted = []
    undispositioned = []
    undispositioned_entry_classes = []
    missing_required = []
    for rel, kind, detail in nonreg:
        disposed = bool(gapped.get(rel) or removed_rels.get(rel))
        silent_ok = False
        if not disposed:
            labels = (removed.get("silent") or {}).get(kind)
            if labels and mod.silent_detail_matches(detail, labels):
                silent_ok = True
                silent_admitted.append({"path": rel, "kind": kind, "detail": detail})
        if not disposed and not silent_ok:
            undispositioned.append({"path": rel, "kind": kind, "detail": detail})
            if kind in entry_classes:
                undispositioned_entry_classes.append(
                    {"path": rel, "kind": kind, "detail": detail})
        need = required.get(kind, bool(allowed.get(kind)))
        if need and not disposed and not silent_ok:
            missing_required.append({"path": rel, "kind": kind, "detail": detail})

    if missing_required:
        violations.append("required entry with no disposition (no gap, no removal, "
                          "no silent label): %d row(s), first %r"
                          % (len(missing_required),
                             [r["path"] for r in missing_required[:8]]))

    res = {
        "violations": violations,
        "gap_kind_counts": dict(gap_kind_counts),
        "structural_gap_counts": dict(structural_counts),
        "structural_allowance": dict(structural),
        "gapped": {rel: sorted(set(ks)) for rel, ks in sorted(gapped.items())},
        "gapped_kind_census": dict(Counter(by_rel[rel][0] for rel in gapped)),
        "removals": removal_paths,
        "removal_kind_census": dict(Counter(p["kind"] for p in removal_paths)),
        "removal_problems": removal_problems,
        "silent_admitted": silent_admitted,
        "silent_kind_census": dict(Counter(p["kind"] for p in silent_admitted)),
        "undispositioned": sorted(undispositioned, key=lambda r: r["path"]),
        "undispositioned_by_kind": dict(Counter(r["kind"] for r in undispositioned)),
        "entry_classes": sorted(entry_classes),
        "undispositioned_entry_classes": sorted(undispositioned_entry_classes,
                                                key=lambda r: r["path"]),
        "undispositioned_entry_classes_by_kind": dict(
            Counter(r["kind"] for r in undispositioned_entry_classes)),
        "dir_rows": sum(1 for _r, k, _d in nonreg if k == "dir"),
        "dir_rows_disposed": sum(1 for rel, k, _d in nonreg
                                 if k == "dir" and (gapped.get(rel) or removed_rels.get(rel))),
        "missing_required": sorted(missing_required, key=lambda r: r["path"]),
        "missing_required_by_kind": dict(Counter(r["kind"] for r in missing_required)),
        "unresolved_gap_paths": unresolved_gaps,
    }
    return res


def main():
    mod, engine_digest = load_engine()
    spec_doc = json.loads(CARRIERS.read_text(encoding="utf-8"))
    carriers = {c["id"]: c for c in spec_doc["carriers"]}
    if tuple(carriers) != IDS:
        raise SystemExit("carrier ids drift: %r" % (tuple(carriers),))

    audit = {
        "schema": "kaidoku-r67-w1-gap-audit-v1",
        "seat": "ExecGapAudit",
        "claim": "R67-C1",
        "wrapper_imported": False,
        "engine": {"path": str(ENGINE.relative_to(REPO)), "sha256": engine_digest,
                   "pin": ENGINE_PIN, "pin_ok": engine_digest == ENGINE_PIN},
        "revs": {"base": BASE_REV, "freeze": FREEZE_REV},
        "carriers_spec": {"path": str(CARRIERS.relative_to(REPO)),
                          "sha256": sha_bytes(CARRIERS.read_bytes()),
                          "bytes_equal_at_freeze": show(
                              FREEZE_REV, str(CARRIERS.relative_to(REPO)))
                          == CARRIERS.read_bytes(),
                          "bytes_equal_at_base": show(
                              BASE_REV, str(CARRIERS.relative_to(REPO)))
                          == CARRIERS.read_bytes(),
                          "target": spec_doc.get("target"),
                          "projection": spec_doc.get("projection"),
                          "ids": list(carriers)},
        "scope": {
            "re_derived": "per-carrier disposition accounting (gaps_ok) under the "
                          "round-50 and round-67 gap rules over the four committed "
                          "round-50 envelopes, without importing the round-67 wrapper",
            "not_evaluated": [
                "carriers_matched / met_target / exit_code of the full measure() "
                "(documentation bindings + four carrier data runs: L1's job)",
                "byte-level oracle re-derivation via unsquashfs (needs the vendor "
                "carrier cache; the committed oracle table bytes are pinned here instead)",
            ],
        },
        "rules": {},
        "rule_delta": {},
        "decisions": {},
        "carriers": {},
        "aggregate": {},
        "checks": [],
        "verdict": {},
        "blocking_findings": [],
    }

    def check(name, ok, detail=None):
        audit["checks"].append({"name": name, "ok": bool(ok),
                                "detail": detail if detail is not None else ""})
        return bool(ok)

    # ---- rules -------------------------------------------------------------
    models = {}
    for label, path in RULES.items():
        raw = path.read_bytes()
        digest = sha_bytes(raw)
        model, probs = mod.gap_rule_model(raw)
        freeze_raw = show(FREEZE_REV, str(path.relative_to(REPO)))
        base_raw = show(BASE_REV, str(path.relative_to(REPO)))
        audit["rules"][label] = {
            "path": str(path.relative_to(REPO)),
            "sha256": digest,
            "pin": RULE_PINS[label],
            "pin_ok": digest == RULE_PINS[label],
            "bytes_equal_at_freeze": freeze_raw == raw,
            "bytes_equal_at_base": base_raw == raw if base_raw is not None else None,
            "model": model,
            "model_problems": probs,
        }
        models[label] = model
        check("rule %s sha256 matches pin" % label, digest == RULE_PINS[label], digest)
        check("rule %s parses clean" % label, probs == [], probs)
        check("rule %s bytes unchanged at freeze" % label, freeze_raw == raw)

    r50, r67 = models["round-50"], models["round-67"]
    delta = {
        "allowed_equal": r50["allowed"] == r67["allowed"],
        "structural_equal": r50["structural"] == r67["structural"],
        "removed_diagnostic_equal": (r50["removed"].get("diagnostic")
                                     == r67["removed"].get("diagnostic")),
        "removed_kinds_equal": (r50["removed"].get("kinds")
                                == r67["removed"].get("kinds")),
        "removed_disposition_equal": (r50["removed"].get("disposition")
                                      == r67["removed"].get("disposition")),
        "removed_silent_r50": r50["removed"].get("silent"),
        "removed_silent_r67": r67["removed"].get("silent"),
        "required_r50": r50["required"],
        "required_r67": r67["required"],
        "required_diff": {k: [r50["required"].get(k), r67["required"].get(k)]
                          for k in sorted(set(r50["required"]) | set(r67["required"]))
                          if r50["required"].get(k) != r67["required"].get(k)},
    }
    audit["rule_delta"] = delta
    check("carriers.json bytes unchanged at freeze and base",
          audit["carriers_spec"]["bytes_equal_at_freeze"]
          and audit["carriers_spec"]["bytes_equal_at_base"],
          {"freeze": audit["carriers_spec"]["bytes_equal_at_freeze"],
           "base": audit["carriers_spec"]["bytes_equal_at_base"]})
    check("rules agree on allowed", delta["allowed_equal"])
    check("rules agree on structural", delta["structural_equal"])
    check("rules agree on removed diagnostic/kinds/disposition",
          delta["removed_diagnostic_equal"] and delta["removed_kinds_equal"]
          and delta["removed_disposition_equal"])
    check("only required.char-device differs between rules",
          delta["required_diff"] == {"char-device": [True, False]},
          delta["required_diff"])
    check("round-67 rule drops the per-row char-device silent label",
          delta["removed_silent_r50"] == {"char-device": ["247:0"]}
          and not delta["removed_silent_r67"],
          {"r50": delta["removed_silent_r50"], "r67": delta["removed_silent_r67"]})

    # ---- per carrier, per rule --------------------------------------------
    decisions_aggregate = {label: [] for label in RULES}
    for cid in IDS:
        c = carriers[cid]
        npath = c["nonregular"]
        rpath = "%s/%s/after.json" % (AFTERDIR, cid)
        env_raw = (REPO / rpath).read_bytes()
        env = json.loads(env_raw)
        nr_raw = (REPO / npath).read_bytes()
        nonreg, nerr = mod.parse_nonregular(nr_raw)
        if nerr is not None:
            raise SystemExit("nonregular table %s: %s" % (cid, nerr))

        root, how = mod.subject_root(env)
        files = mod.published(env)
        diags = mod.diagnostics(env)
        gaps_list = mod.gaps(env)
        od = (env.get("parameters") or {}).get("output_directory")

        integrity = {
            "nonregular_path": npath,
            "nonregular_sha256": sha_bytes(nr_raw),
            "nonregular_equal_at_freeze": show(FREEZE_REV, npath) == nr_raw,
            "nonregular_equal_at_base": show(BASE_REV, npath) == nr_raw,
            "envelope_path": rpath,
            "envelope_sha256": sha_bytes(env_raw),
            "envelope_equal_at_freeze": show(FREEZE_REV, rpath) == env_raw,
            "envelope_equal_at_base": show(BASE_REV, rpath) == env_raw,
            "carrier_sha256": c.get("sha256"),
            "subject_digest": ((env.get("subject") or {}).get("digest") or {}).get("sha256")
            if isinstance(env.get("subject"), dict) else None,
            "subject_pin_ok": (((env.get("subject") or {}).get("digest") or {}).get("sha256")
                               if isinstance(env.get("subject"), dict) else None) == c.get("sha256"),
        }
        check("%s nonregular table unchanged at freeze" % cid,
              integrity["nonregular_equal_at_freeze"])
        check("%s envelope unchanged at freeze" % cid,
              integrity["envelope_equal_at_freeze"])
        check("%s envelope unchanged at base" % cid,
              integrity["envelope_equal_at_base"])
        check("%s envelope subject digest equals the carrier pin" % cid,
              integrity["subject_pin_ok"], integrity["subject_digest"])

        kind_census = dict(sorted(Counter(k for _r, k, _d in nonreg).items()))
        row = {
            "integrity": integrity,
            "extract_root": root,
            "extract_root_source": how,
            "squashfs_roots": mod.squashfs_roots(env),
            "oracle_files": None,
            "published_files": len(files),
            "published_rels": len(mod.published_rels(files, root,
                                                    mod.nested_roots(env, root))),
            "nonregular_entries": len(nonreg),
            "nonregular_kind_census": kind_census,
            "nonregular_published": mod.nonregular_published(files, nonreg, root),
            "diagnostics": len(diags),
            "gaps": len(gaps_list),
            "rules": {},
        }
        oraw = (REPO / c["oracle"]).read_text(encoding="utf-8")
        orows, oerr = mod.parse_oracle(oraw.encode())
        row["oracle_files"] = len(orows)
        row["oracle_error"] = oerr

        check("%s single squashfs_v4_le root" % cid, len(row["squashfs_roots"]) == 1,
              row["squashfs_roots"])
        check("%s no published regular file equals a non-regular path" % cid,
              row["nonregular_published"] == [], row["nonregular_published"])

        for label, model in models.items():
            engine_ok, engine_why = mod.disposition_check(
                gaps_list, diags, nonreg, model, root, od)
            rec = recount(mod, nonreg, gaps_list, diags, model, root, od)
            entry = {
                "gaps_ok": engine_ok,
                "engine_note": engine_why,
                "recount_agrees": (not rec["violations"]) == engine_ok,
                "recount_violations": rec["violations"],
                "gap_kind_counts": rec["gap_kind_counts"],
                "structural_gap_counts": rec["structural_gap_counts"],
                "structural_allowance": rec["structural_allowance"],
                "gapped_entries": len(rec["gapped"]),
                "gapped_kind_census": rec["gapped_kind_census"],
                "removals": rec["removals"],
                "removal_kind_census": rec["removal_kind_census"],
                "silent_admitted": rec["silent_admitted"],
                "silent_kind_census": rec["silent_kind_census"],
                "undispositioned": rec["undispositioned"],
                "undispositioned_by_kind": rec["undispositioned_by_kind"],
                "entry_classes": rec["entry_classes"],
                "undispositioned_entry_classes": rec["undispositioned_entry_classes"],
                "undispositioned_entry_classes_by_kind":
                    rec["undispositioned_entry_classes_by_kind"],
                "dir_rows": rec["dir_rows"],
                "dir_rows_disposed": rec["dir_rows_disposed"],
                "missing_required": rec["missing_required"],
                "missing_required_by_kind": rec["missing_required_by_kind"],
                "unresolved_gap_paths": rec["unresolved_gap_paths"],
            }
            row["rules"][label] = entry
            decisions_aggregate[label].append({"id": cid, "gaps_ok": engine_ok,
                                               "missing_required":
                                               len(rec["missing_required"]),
                                               "undispositioned":
                                               len(rec["undispositioned"])})
            check("%s [%s] independent recount reproduces the engine verdict" % (cid, label),
                  entry["recount_agrees"], entry["recount_violations"])
            check("%s [%s] every path gap resolves to exactly one row" % (cid, label),
                  rec["unresolved_gap_paths"] == [], rec["unresolved_gap_paths"])
            check("%s [%s] no symlink is undispositioned" % (cid, label),
                  rec["undispositioned_by_kind"].get("symlink", 0) == 0
                  and rec["missing_required_by_kind"].get("symlink", 0) == 0,
                  {"undispositioned": rec["undispositioned_by_kind"],
                   "missing_required": rec["missing_required_by_kind"]})
            check("%s [%s] no undispositioned path outside the char-device entry class"
                  % (cid, label),
                  set(rec["undispositioned_entry_classes_by_kind"]) <= {"char-device"},
                  rec["undispositioned_entry_classes_by_kind"])
            check("%s [%s] dir rows are outside the rule's entry classes and disposed by none"
                  % (cid, label),
                  "dir" not in rec["entry_classes"] and rec["dir_rows_disposed"] == 0,
                  {"entry_classes": rec["entry_classes"],
                   "dir_rows": rec["dir_rows"],
                   "dir_rows_disposed": rec["dir_rows_disposed"]})
            sym_total = kind_census.get("symlink", 0)
            sym_disposed = (rec["gapped_kind_census"].get("symlink", 0)
                            + rec["removal_kind_census"].get("symlink", 0))
            check("%s [%s] symlinks split exactly into gap + removal" % (cid, label),
                  sym_disposed == sym_total,
                  {"total": sym_total, "gapped": rec["gapped_kind_census"].get("symlink", 0),
                   "removed": rec["removal_kind_census"].get("symlink", 0)})
            check("%s [%s] every gap is path-resolved except the structural allowance"
                  % (cid, label),
                  set(rec["gap_kind_counts"]) <= {"unpublished-entry", "depth-limited"},
                  rec["gap_kind_counts"])
        audit["carriers"][cid] = row
        audit["decisions"][cid] = {label: row["rules"][label]["gaps_ok"]
                                   for label in RULES}

    # ---- class-level assertions -------------------------------------------
    char_census = {cid: audit["carriers"][cid]["nonregular_kind_census"].get("char-device", 0)
                   for cid in IDS}
    dir_census = {cid: audit["carriers"][cid]["nonregular_kind_census"].get("dir", 0)
                  for cid in IDS}
    char_paths = {cid: [r for r in audit["carriers"][cid]["rules"]["round-67"]
                        ["undispositioned_entry_classes"] if r["kind"] == "char-device"]
                  for cid in IDS}
    char_rows = {cid: {rel for rel, k, _d in
                       mod.parse_nonregular((REPO / carriers[cid]["nonregular"]).read_bytes())[0]
                       if k == "char-device"} for cid in IDS}
    audit["aggregate"] = {
        "char_device_census": char_census,
        "dir_census": dir_census,
        "char_device_definitions_equal_census_round67": all(
            len(char_paths[cid]) == char_census[cid]
            and {r["path"] for r in char_paths[cid]} == char_rows[cid]
            for cid in IDS),
        "undispositioned_round67_raw_by_kind": dict(Counter(
            k for cid in IDS
            for k in audit["carriers"][cid]["rules"]["round-67"]["undispositioned_by_kind"]
            for _ in range(audit["carriers"][cid]["rules"]["round-67"]
                           ["undispositioned_by_kind"][k]))),
        "undispositioned_round67_entry_class_by_kind": dict(Counter(
            k for cid in IDS
            for k in audit["carriers"][cid]["rules"]["round-67"]
            ["undispositioned_entry_classes_by_kind"]
            for _ in range(audit["carriers"][cid]["rules"]["round-67"]
                           ["undispositioned_entry_classes_by_kind"][k]))),
        "undispositioned_round50_entry_class_by_kind": dict(Counter(
            k for cid in IDS
            for k in audit["carriers"][cid]["rules"]["round-50"]
            ["undispositioned_entry_classes_by_kind"]
            for _ in range(audit["carriers"][cid]["rules"]["round-50"]
                           ["undispositioned_entry_classes_by_kind"][k]))),
        "undispositioned_round67_entry_class_per_carrier": {
            cid: audit["carriers"][cid]["rules"]["round-67"]
            ["undispositioned_entry_classes_by_kind"] for cid in IDS},
        "undispositioned_round50_entry_class_per_carrier": {
            cid: audit["carriers"][cid]["rules"]["round-50"]
            ["undispositioned_entry_classes_by_kind"] for cid in IDS},
        "gaps_ok_counts": {label: sum(1 for d in decisions_aggregate[label] if d["gaps_ok"])
                           for label in RULES},
        "decisions": decisions_aggregate,
        "no_block_device_rows": all(
            "block-device" not in audit["carriers"][cid]["nonregular_kind_census"]
            for cid in IDS),
        "no_fifo_or_socket_rows": all(
            not ({"fifo", "socket"} & set(audit["carriers"][cid]["nonregular_kind_census"]))
            for cid in IDS),
    }
    check("char-device census is 13/13/1/1",
          char_census == {"g7581": 13, "g7582": 13, "c6490": 1, "c6430": 1},
          char_census)
    check("round-67 undispositioned entry-class set is exactly the char-device class, "
          "13/13/1/1",
          set(audit["aggregate"]["undispositioned_round67_entry_class_by_kind"])
          == {"char-device"}
          and audit["aggregate"]["undispositioned_round67_entry_class_by_kind"]
          == {"char-device": 28}
          and {cid: v.get("char-device", 0) for cid, v in audit["aggregate"]
               ["undispositioned_round67_entry_class_per_carrier"].items()}
          == char_census
          and audit["aggregate"]["char_device_definitions_equal_census_round67"],
          {"per_carrier": audit["aggregate"]
           ["undispositioned_round67_entry_class_per_carrier"]})
    check("round-50 undispositioned entry-class set is char-device 12/12/0/0 "
          "(dev/led 247:0 silent-admitted on all four)",
          audit["aggregate"]["undispositioned_round50_entry_class_by_kind"]
          == {"char-device": 24}
          and audit["aggregate"]["undispositioned_round50_entry_class_per_carrier"]
          == {"g7581": {"char-device": 12}, "g7582": {"char-device": 12},
              "c6490": {}, "c6430": {}},
          audit["aggregate"]["undispositioned_round50_entry_class_per_carrier"])
    check("round-50 rule: gaps_ok on 2 of 4 (before-arm)",
          audit["aggregate"]["gaps_ok_counts"]["round-50"] == 2,
          audit["aggregate"]["decisions"])
    check("round-67 rule: gaps_ok on 4 of 4",
          audit["aggregate"]["gaps_ok_counts"]["round-67"] == 4,
          audit["aggregate"]["decisions"])
    check("the two round-50 FALSE carriers are exactly g7581 and g7582",
          sorted(cid for cid, d in audit["decisions"].items()
                 if not d["round-50"]) == ["g7581", "g7582"],
          audit["decisions"])
    check("no block-device rows (class_disposition claim holds)",
          audit["aggregate"]["no_block_device_rows"])
    check("no fifo/socket rows", audit["aggregate"]["no_fifo_or_socket_rows"])

    # ---- verdict ----------------------------------------------------------
    audit["verdict"] = {}
    for cid in IDS:
        r50d = audit["carriers"][cid]["rules"]["round-50"]
        r67d = audit["carriers"][cid]["rules"]["round-67"]
        audit["verdict"][cid] = (
            "round-50 rule: %s, %d required char-device row(s) undisposed "
            "(of %d char-device rows); round-67 rule: %s, %d required row(s) "
            "undisposed, %d char-device row(s) carry no per-row disposition "
            "(class is not required); symlinks %s"
            % ("PASS" if r50d["gaps_ok"] else "FAIL",
               len(r50d["missing_required"]),
               audit["carriers"][cid]["nonregular_kind_census"].get("char-device", 0),
               "PASS" if r67d["gaps_ok"] else "FAIL",
               len(r67d["missing_required"]),
               len(r67d["undispositioned_entry_classes"]),
               "all disposed (%d gap, %d removal)"
               % (r67d["gapped_kind_census"].get("symlink", 0),
                  r67d["removal_kind_census"].get("symlink", 0))))
    audit["blocking_findings"] = [c for c in audit["checks"] if not c["ok"]]
    audit["all_checks_ok"] = not audit["blocking_findings"]

    OUT.write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "out": str(OUT),
        "all_checks_ok": audit["all_checks_ok"],
        "gaps_ok_counts": audit["aggregate"]["gaps_ok_counts"],
        "char_device_census": char_census,
        "undispositioned_round67_entry_class_by_kind":
            audit["aggregate"]["undispositioned_round67_entry_class_by_kind"],
        "undispositioned_round50_entry_class_per_carrier":
            audit["aggregate"]["undispositioned_round50_entry_class_per_carrier"],
        "missing_required_round50": {
            cid: len(audit["carriers"][cid]["rules"]["round-50"]["missing_required"])
            for cid in IDS},
        "blocking_findings": audit["blocking_findings"],
    }, indent=1, sort_keys=True))
    return 0 if audit["all_checks_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
