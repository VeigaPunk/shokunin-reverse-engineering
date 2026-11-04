#!/usr/bin/env python3
"""ExecRedControls - round-67 w1 red-control battery over the committed envelopes.

Extends the wrapper's own --control (avm-le-counter.py, two red fixtures) to the
class boundaries and the rejection surface of tools/round-67/gap-rule-v2.json.

It calls the pinned round-50 engine's own `disposition_check` and
`nonregular_published` (same import and pin as ExecPins) and its own gap-rule
model, on data rewritten from the committed round-50 after-receipts at the base
revision. Every fixture gets its OWN extract root and its OWN trusted run root
under scratch, and the rewrite is asserted to preserve resolution (otherwise a
fixture could pass vacuously).

Writes red.json next to this file. Exit 0 iff every fixture fires as declared and
the wrapper control reproduces.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
LANE = REPO / ".ufo/waves/round-67/w1/ExecRedControls"
SCRATCH = Path("/fast/scratch/hyaku/kaidoku-r67/ExecRedControls")
COUNTER = REPO / "tools/round-67/avm-le-counter.py"
# The dispatch card pins f78ed365 (the blob at the operative freeze 3663e6b).
# The instrument was superseded at 1e7fe7b7 (absolute -> lane-relative GAPRULE
# name; the engine reads its rule through `git show <rev>:<path>`), disclosed in
# claims.json A10 / instrument_supersessions, and the before record re-taken.
COUNTER_FREEZE_PIN = "f78ed365ab1d014fb2e80bdee611796dfb4667c9e2ab8f16f2893fdb7c5e0320"
ENGINE = REPO / "tools/round-50/c1-counter.py"
ENGINE_PIN = "9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813"
RULE_V2 = REPO / "tools/round-67/gap-rule-v2.json"
RULE_V2_PIN = "e66ba022ee3607c9fe74f141902c012b2418ad6d800589b6d2fb888084a4169e"
RULE_R50 = REPO / "tools/round-50/gap-rule.json"
RULE_R50_PIN = "43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef"
CARRIERS = "tools/round-50/carriers.json"
REV = "a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92"
FREEZE = "3663e6b21dccf4c4957f459301156664d8b151d6"
TARGET = 4

MALICIOUS = "MaliciousSymlinkRemoved"
DEV_BLOCK = "dev/sda1"        # synthetic: no block-device row exists on these carriers
DEV_FIFO = "dev/fifo-test"    # synthetic: no fifo row exists on these carriers


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_engine():
    digest = sha256_file(ENGINE)
    if digest != ENGINE_PIN:
        raise SystemExit("engine drifted: %s != %s" % (digest, ENGINE_PIN))
    spec = importlib.util.spec_from_file_location("c1_counter_r50", ENGINE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod, digest


def load_fixture(mod, cid):
    """(gaps, diags, nonreg, real_od) for a committed round-50 envelope."""
    spec = json.loads(mod.show(REPO, REV, CARRIERS))
    by_id = {c["id"]: c for c in spec["carriers"]}
    c = by_id[cid]
    env = json.loads(mod.show(REPO, REV,
                              "corpus/evidence/round-50/c1/%s/after.json" % cid))
    nonreg, nerr = mod.parse_nonregular(mod.show(REPO, REV, c["nonregular"]))
    assert nerr is None, nerr
    real_root, how = mod.subject_root(env)
    assert real_root is not None, how
    od = (env.get("parameters") or {}).get("output_directory")
    assert isinstance(od, str) and os.path.isabs(od)
    return dict(gaps=mod.gaps(env), diags=mod.diagnostics(env), nonreg=nonreg,
                real_root=real_root, real_od=od, env=env)


def rewrite(fx, cid, fid):
    """A fixture copy with its OWN extract root and trusted run root."""
    data = load_fixture(fx["mod"], cid)
    base = SCRATCH / "fixtures" / fid
    od = str(base / "run" / "extract")
    root = "fx-%s/firmware.bin_extract" % fid
    (base / "run" / "extract").mkdir(parents=True, exist_ok=True)
    (base / "run" / "rea" / root).mkdir(parents=True, exist_ok=True)
    gaps = []
    for g in data["gaps"]:
        g = dict(g)
        rp = g.get("relative_path")
        if rp is None:
            g["input_path"] = "$output/%s" % root
        else:
            rel = fx["mod"].extract_rel(rp, data["real_root"])
            assert rel is not None, rp
            g["relative_path"] = "%s/%s" % (root, rel)
            g["input_path"] = "$output/%s/%s" % (root, rel)
        gaps.append(g)
    diags = json.loads(json.dumps(data["diags"]))
    for d in diags:
        rel = fx["mod"].diagnostic_rel(d, data["real_root"], data["real_od"])
        assert rel is not None, d.get("report")
        d["report"]["link"] = "%s/run/rea/%s/%s" % (base, root, rel)
    out = dict(gaps=gaps, diags=diags, nonreg=list(data["nonreg"]), root=root,
               od=od, base=str(base), env=data["env"],
               scratch_rel="fixtures/" + fid)
    # the rewrite must resolve end to end before any mutation is applied
    ok, note = fx["mod"].disposition_check(out["gaps"], out["diags"],
                                           out["nonreg"], fx["model_v2"],
                                           out["root"], out["od"])
    if not ok:
        raise SystemExit("fixture %s baseline does not resolve: %s" % (fid, note))
    return out


def check(fx, d, model):
    return fx["mod"].disposition_check(d["gaps"], d["diags"], d["nonreg"],
                                       model, d["root"], d["od"])


def path_in_root(d, rel):
    return "%s/%s" % (d["root"], rel)


def gap(rel, kind, root_path=None, dependencies=None):
    rp = root_path
    return {"kind": kind, "input_path": ("$output/" + rp) if rp else None,
            "relative_path": rp, "handler": None, "provider_id": None,
            "range": None, "root_file_range": None,
            "dependencies": dependencies or [], "continuation_id": "red"}


def removal(d, rel, trusted=None):
    base = trusted if trusted is not None else "%s/run/rea" % d["base"]
    return {"input_path": "$input", "report": {
        "__typename__": MALICIOUS, "severity": "WARNING",
        "link": "%s/%s/%s" % (base, d["root"], rel),
        "target": "/var/tmp/log"}}


def add_row(d, rel, kind, detail=None):
    d["nonreg"].append((rel, kind, detail))


def dropped_rows(nonreg_before, nonreg_after):
    return [r for r in nonreg_before if r not in nonreg_after]


def git_bytes(rev_path: str):
    p = subprocess.run(["git", "-C", str(REPO), "cat-file", "-p", rev_path],
                       capture_output=True)
    return p.stdout, p.returncode


def commit_subject(commit: str) -> str:
    p = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%s", commit],
                       capture_output=True, text=True)
    return p.stdout.strip()


def main() -> int:
    if sha256_file(RULE_R50) != RULE_R50_PIN:
        raise SystemExit("rule r50 drifted")
    mod, engine_digest = load_engine()
    fx = {"mod": mod}
    spec_cs = importlib.util.spec_from_file_location("r67counter", COUNTER)
    counter_mod = importlib.util.module_from_spec(spec_cs)
    assert spec_cs.loader is not None
    spec_cs.loader.exec_module(counter_mod)
    v2 = json.loads(RULE_V2.read_text(encoding="utf-8"))
    r50 = json.loads(RULE_R50.read_text(encoding="utf-8"))
    model_v2, probs_v2 = mod.gap_rule_model(json.dumps(v2).encode())
    model_r50, probs_r50 = mod.gap_rule_model(json.dumps(r50).encode())
    fx["model_v2"], fx["model_r50"] = model_v2, model_r50

    # The instrument and its rule are being corrected under disclosure inside
    # this round, so nothing is pinned by a number copied from the dispatch
    # card: the working files must equal the blobs at HEAD, and the numbers the
    # counter and the claims file declare are recorded beside them.
    claims = json.loads((REPO / ".ufo/waves/round-67/claims.json").read_text())
    declared = ((claims.get("instruments") or {})
                .get("tools/round-67/avm-le-counter.py"))
    working = sha256_file(COUNTER)
    head_raw, head_rc = git_bytes("HEAD:tools/round-67/avm-le-counter.py")
    head_digest = hashlib.sha256(head_raw).hexdigest() if head_rc == 0 else None
    head_commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                                 capture_output=True, text=True).stdout.strip()
    recorded_supersessions = claims.get("instrument_supersessions") or []
    touched = subprocess.run(["git", "-C", str(REPO), "log", "--format=%H",
                              "--reverse", "%s..HEAD" % FREEZE, "--",
                              "tools/round-67/avm-le-counter.py"],
                             capture_output=True, text=True).stdout.split()

    rule_working = sha256_file(RULE_V2)
    rule_head_raw, rule_head_rc = git_bytes("HEAD:tools/round-67/gap-rule-v2.json")
    rule_head_digest = (hashlib.sha256(rule_head_raw).hexdigest()
                        if rule_head_rc == 0 else None)
    rule_declared_claims = ((claims.get("instruments") or {})
                            .get("tools/round-67/gap-rule-v2.json"))
    rule_declared_counter = getattr(counter_mod, "RULE_V2_PIN", None)

    doc = {"schema": "kaidoku-r67-w1-exec-red-controls-v1",
           "seat": "ExecRedControls", "claim": "R67-C1", "rev": REV,
           "freeze": FREEZE,
           "pins": {"counter": {"path": str(COUNTER.relative_to(REPO)),
                                "sha256_at_run": working},
                    "engine": {"path": str(ENGINE.relative_to(REPO)),
                               "sha256": engine_digest},
                    "rule_v2": {"path": str(RULE_V2.relative_to(REPO)),
                                "sha256_at_run": rule_working,
                                "declared_in_counter": rule_declared_counter,
                                "declared_in_claims": rule_declared_claims,
                                "head_blob_sha256": rule_head_digest,
                                "all_four_agree": len({rule_working,
                                                       rule_head_digest,
                                                       rule_declared_counter,
                                                       rule_declared_claims}) == 1},
                    "rule_r50": {"path": str(RULE_R50.relative_to(REPO)),
                                 "sha256": RULE_R50_PIN}},
           "import": {"call": "importlib.util.spec_from_file_location"
                              "('c1_counter_r50', %s)" % ENGINE,
                      "engine_sha256_asserted": True,
                      "entry_points": ["disposition_check", "nonregular_published",
                                       "gap_rule_model", "parse_nonregular",
                                       "subject_root", "diagnostic_rel", "gaps",
                                       "diagnostics", "published", "extract_rel"]}}

    # carrier_fresh_ok now stays in the clause set: the claim is that none of the
    # four pins is one an earlier C1 freeze already scored
    frozen_spec = json.loads(mod.show(REPO, FREEZE, CARRIERS))
    prior, prior_sources = mod.prior_pins(REPO, FREEZE, frozen_spec)
    carrier_pins = {c.get("sha256") for c in frozen_spec.get("carriers") or []
                    if isinstance(c, dict)}
    doc["carrier_fresh_ok_support"] = {
        "prior_pin_count": len(prior),
        "prior_pin_sources": prior_sources,
        "carrier_pins_in_prior": sorted(p for p in carrier_pins & set(prior) if p),
        "freshness_holds": not (carrier_pins & set(prior)),
        "clauses": list(getattr(counter_mod, "CLAUSES", ())) or
                   [c for c in mod.CLAUSES],
        "dropped_clauses": getattr(counter_mod, "DROPPED_CLAUSES", ()),
    }

    # --- step 1: reproduce the wrapper's own control, fresh, and compare -------
    lane_ctl = LANE / "wrapper-control.json"
    fresh = SCRATCH / "wrapper-control.json"
    cp = subprocess.run([sys.executable, "-I", "-B", str(COUNTER), "--control",
                         "--root", str(REPO), "--rev", REV,
                         "--work", str(SCRATCH / "ctl"), "--out", str(fresh)],
                        capture_output=True, text=True,
                        env={**os.environ, "TMPDIR": str(SCRATCH)})
    ctl = json.loads(fresh.read_text(encoding="utf-8"))
    lane_ctl.write_bytes(fresh.read_bytes())
    l1_pre = REPO / ".ufo/waves/round-67/l1/pre/control-dryrun.json"

    # the superseded blob (the one the dispatch card pins) must score the same
    # control: the correction touches only --score's GAPRULE name
    freeze_blob = SCRATCH / "counter-at-freeze.py"
    gs = subprocess.run(["git", "-C", str(REPO), "show",
                         "%s:tools/round-67/avm-le-counter.py" % FREEZE],
                        capture_output=True)
    freeze_blob.write_bytes(gs.stdout)
    frozen_ctl_path = LANE / "wrapper-control-at-freeze-blob.json"
    fp = subprocess.run([sys.executable, "-I", "-B", str(freeze_blob), "--control",
                         "--root", str(REPO), "--rev", REV,
                         "--work", str(SCRATCH / "ctl-freeze"),
                         "--out", str(frozen_ctl_path)],
                        capture_output=True, text=True,
                        env={**os.environ, "TMPDIR": str(SCRATCH)})
    frozen_ctl = json.loads(frozen_ctl_path.read_text(encoding="utf-8"))
    numbers = ("gaps_ok_round50", "gaps_ok_round67", "control_ok", "exit_code",
               "per_carrier", "rule_v2_sha256", "rule_r50_sha256", "target")

    # the corrections: patch_engine must yield a lane-relative GAPRULE, and the
    # engine's git-object lookup must resolve it at the freeze
    class _Stub:
        GAPRULE = AFTERDIR = ENTRY = STEM = CORE_HEADING = FRONTIER_MARK = None
        PROV_BASE = PROV_SEGMENT = WORK_OVERRIDE = None
        OPENED_DATES = ()
        CLAUSES = ("carrier_present", "carrier_fresh_ok")

    patches = counter_mod.patch_engine(_Stub, RULE_V2, SCRATCH / "pework", REPO)
    lookup = subprocess.run(["git", "-C", str(REPO), "show",
                             "%s:%s" % (FREEZE, _Stub.GAPRULE)],
                            capture_output=True)
    abs_lookup = subprocess.run(["git", "-C", str(REPO), "show",
                                 "%s:%s" % (FREEZE, str(RULE_V2))],
                                capture_output=True)
    chain = []
    for commit in [FREEZE] + touched:
        raw, rc = git_bytes("%s:tools/round-67/avm-le-counter.py" % commit)
        chain.append({"commit": commit,
                      "sha256": hashlib.sha256(raw).hexdigest() if rc == 0 else None,
                      "subject": commit_subject(commit),
                      "disclosed_in_claims": commit in {
                          s.get("commit") for s in recorded_supersessions}})
    rea = getattr(counter_mod, "REA_PKG_R67", None)
    rea_check = {"present": isinstance(rea, dict)}
    if isinstance(rea, dict):
        pkg_json = os.path.join(rea.get("package_root", ""), "package.json")
        lock_candidates = [
            os.path.join(os.path.dirname(rea.get("package_root", "")),
                         "package-lock.json"),
            os.path.join(os.path.dirname(os.path.dirname(rea.get("package_root", ""))),
                         "package-lock.json")]
        lock = next((p for p in lock_candidates if os.path.isfile(p)), None)
        rea_check.update({
            "version": rea.get("version"),
            "package_root": rea.get("package_root"),
            "package_root_exists": os.path.isdir(rea.get("package_root", "")),
            "package_json_sha256_matches_host": (
                os.path.isfile(pkg_json)
                and sha256_file(pkg_json) == rea.get("package_json_sha256")),
            "package_lock_path": lock,
            "package_lock_sha256_matches_host": (
                lock is not None
                and sha256_file(lock) == rea.get("package_lock_sha256")),
            "supersedes": rea.get("supersedes"),
        })
    module_doc = COUNTER.read_text(encoding="utf-8").split('"""')[1]
    numeric = re.search(r"patching exactly (\w+) things", module_doc)
    ctl_path = getattr(counter_mod, "CONTROL_RECEIPT", None)
    ctl_raw = mod.show(REPO, REV, ctl_path) if ctl_path else None
    ctl_head_raw, ctl_head_rc = (git_bytes("HEAD:%s" % ctl_path) if ctl_path
                                 else (b"", 1))
    ctl_head = json.loads(ctl_head_raw) if ctl_head_rc == 0 else {}
    doc["instrument_pins"] = {
        "dispatch_pin": COUNTER_FREEZE_PIN,
        "dispatch_pin_is_freeze_blob": chain[0]["sha256"] == COUNTER_FREEZE_PIN,
        "declared_pin_in_claims": declared,
        "declared_matches_working_file": declared == working,
        "working_file_sha256": working,
        "head_commit": head_commit,
        "head_blob_sha256": head_digest,
        "working_matches_head": working == head_digest,
        "chain": chain,
        "commits_touching_instrument_since_freeze": touched,
        "claims_supersessions_recorded": len(recorded_supersessions),
        "undisclosed_instrument_commits": [
            c["commit"] for c in chain
            if c["commit"] not in (FREEZE,) and not c["disclosed_in_claims"]],
        "gaprule_patch": {
            "value": _Stub.GAPRULE,
            "lane_relative": _Stub.GAPRULE == str(RULE_V2.relative_to(REPO)),
            "resolves_at_freeze": lookup.returncode == 0,
            "blob_sha256": hashlib.sha256(lookup.stdout).hexdigest(),
            "absolute_path_lookup_exit": abs_lookup.returncode,
        },
        "patch_surface": {
            "returned_keys": sorted(patches),
            "replaces_mod_rea_package_problems": hasattr(_Stub,
                                                         "rea_package_problems"),
            "documented_patch_count_word": numeric.group(1) if numeric else None,
            "docstring_names_rea_replacement": "rea_package_problems" in module_doc,
            "clauses_unchanged": patches["dropped_clauses"] == [],
            "engine_clause_count": len(mod.CLAUSES),
            "note": "the engine checks the REA package through this attribute; the "
                    "wrapper replaces it wholesale. The numbered list says 'five "
                    "things' and does not name that replacement, though the receipt "
                    "carries patches.rea_pkg",
        },
        "control_receipt_binding": {
            "path": ctl_path,
            "present_at_rev": ctl_raw is not None,
            "rev_note": "rev is the measured revision; the base %s predates the "
                        "round-67 files, so the score's rev must be >= the freeze"
                        % REV[:8],
            "present_at_head": ctl_head_rc == 0,
            "sha256_at_head": (hashlib.sha256(ctl_head_raw).hexdigest()
                               if ctl_head_rc == 0 else None),
            "equals_seat_copy": ctl_head_raw == lane_ctl.read_bytes(),
            "control_ok": ctl_head.get("control_ok"),
            "gaps_ok_round50": ctl_head.get("gaps_ok_round50"),
            "gaps_ok_round67": ctl_head.get("gaps_ok_round67"),
            "receipt_counter_sha256": (ctl_head.get("counter") or {}).get("sha256"),
            "receipt_rule_v2_sha256": ctl_head.get("rule_v2_sha256"),
            "receipt_counter_matches_instrument": (
                (ctl_head.get("counter") or {}).get("sha256") == working),
            "receipt_rule_matches_rule_under_test": (
                ctl_head.get("rule_v2_sha256") == rule_working),
            "binds_second_conjunct": bool(ctl_head.get("control_ok") is True
                                          and ctl_head.get("gaps_ok_round50") == 2),
        },
        "rea_pkg_repin": rea_check,
        "control_with_freeze_blob": {
            "exit": fp.returncode,
            "gaps_ok_round50": frozen_ctl["gaps_ok_round50"],
            "gaps_ok_round67": frozen_ctl["gaps_ok_round67"],
            "same_numbers_as_working": all(frozen_ctl[k] == ctl[k]
                                           for k in numbers),
            "delta_is_counter_digest_only": (
                {k: v for k, v in frozen_ctl.items() if k != "counter"}
                == {k: v for k, v in ctl.items() if k != "counter"}),
        },
    }

    pre = json.loads(l1_pre.read_text())
    number_keys = ("gaps_ok_round50", "gaps_ok_round67", "control_ok", "exit_code",
                   "target", "per_carrier", "rule_r50_sha256")
    same_numbers = all(ctl.get(k) == pre.get(k) for k in number_keys)
    differing = sorted(k for k in set(ctl) | set(pre) if ctl.get(k) != pre.get(k))

    doc["wrapper_control"] = {
        "command": "python3 -I -B tools/round-67/avm-le-counter.py --control "
                   "--rev %s" % REV,
        "exit_code": cp.returncode,
        "fresh_sha256": sha256_file(lane_ctl),
        "byte_identical_to_l1_pre": lane_ctl.read_bytes() == l1_pre.read_bytes(),
        "same_numbers_as_l1_pre": same_numbers,
        "differing_top_level_fields": differing,
        "l1_pre_control_dryrun_sha256": sha256_file(l1_pre),
        "gaps_ok_round50": ctl["gaps_ok_round50"],
        "gaps_ok_round67": ctl["gaps_ok_round67"],
        "control_ok": ctl["control_ok"],
        "target": ctl["target"],
        "counter_sha256": ctl["counter"]["sha256"],
        "engine_sha256": ctl["engine"]["sha256"],
        "per_carrier": {k: {"gaps_ok_round50": v["gaps_ok_round50"],
                            "gaps_ok_round67": v["gaps_ok_round67"],
                            "note_round50": v["gaps_note_round50"]}
                        for k, v in ctl["per_carrier"].items()},
        "red_controls": ctl["red_controls"],
    }

    # --- independent recompute of the same 2/4 from the raw envelopes ---------
    recompute = {}
    census = {}
    stored = {}
    for cid in mod.IDS:
        data = load_fixture(mod, cid)
        stored[cid] = data
        ok_v2, why_v2 = mod.disposition_check(
            data["gaps"], data["diags"], data["nonreg"], model_v2,
            data["real_root"], data["real_od"])
        ok_50, why_50 = mod.disposition_check(
            data["gaps"], data["diags"], data["nonreg"], model_r50,
            data["real_root"], data["real_od"])
        recompute[cid] = {"round67": ok_v2, "round50": ok_50,
                          "note_round67": why_v2, "note_round50": why_50}
        kinds = {}
        for _rel, kind, _detail in data["nonreg"]:
            kinds[kind] = kinds.get(kind, 0) + 1
        census[cid] = {"rows": len(data["nonreg"]), "kinds": kinds,
                       "gaps": len(data["gaps"]), "removals": len(data["diags"]),
                       "char_device_details": sorted(
                           d for _r, k, d in data["nonreg"]
                           if k == "char-device" and d is not None)}
    doc["carrier_census"] = {
        "per_carrier": census,
        "synthetic_only_kinds": sorted(
            {"block-device", "fifo", "socket"}
            - {k for v in census.values() for k in v["kinds"]}),
        "note": "block-device/fifo/socket rows do not exist on these four "
                "carriers; fixtures (a)/(b) append them to a real envelope",
    }

    doc["independent_recompute"] = {
        "per_carrier": recompute,
        "gaps_ok_round67": sum(1 for v in recompute.values() if v["round67"]),
        "gaps_ok_round50": sum(1 for v in recompute.values() if v["round50"]),
        "matches_wrapper": (
            sum(1 for v in recompute.values() if v["round67"]) == ctl["gaps_ok_round67"]
            and sum(1 for v in recompute.values() if v["round50"]) == ctl["gaps_ok_round50"]),
    }

    # --- rule delta: the model differs from round 50 exactly as declared -------
    def model_view(m):
        return {"allowed": m["allowed"], "required": m["required"],
                "structural": m["structural"], "removed": m["removed"]}
    v2m, r50m = model_view(model_v2), model_view(model_r50)
    req_delta = {k: [r50m["required"].get(k), v2m["required"].get(k)]
                 for k in set(v2m["required"]) | set(r50m["required"])
                 if v2m["required"].get(k) != r50m["required"].get(k)}
    doc["rule_delta"] = {
        "model_problems": {"round67": probs_v2, "round50": probs_r50},
        "allowed_identical": v2m["allowed"] == r50m["allowed"],
        "structural_identical": v2m["structural"] == r50m["structural"],
        "removed_diagnostic_identical": (v2m["removed"].get("diagnostic")
                                         == r50m["removed"].get("diagnostic")),
        "removed_kinds_identical": (v2m["removed"].get("kinds")
                                    == r50m["removed"].get("kinds")),
        "removed_silent": {"round50": r50m["removed"].get("silent"),
                           "round67": v2m["removed"].get("silent")},
        "required_delta": req_delta,
        "model_ignores": sorted(set(v2) - {"claim", "allowed", "required",
                                           "structural", "removed"}),
        "model_has_class_disposition": "class_disposition" in v2m,
        "round67_claim_key_absent": "claim" not in v2,
    }

    # --- rule decomposition: which single field produces 4/4 ------------------
    v2_true = json.loads(json.dumps(v2))
    v2_true["required"]["char-device"] = True
    m_v2t, p_v2t = mod.gap_rule_model(json.dumps(v2_true).encode())
    v2_silent = json.loads(json.dumps(v2))
    v2_silent["removed"]["silent"] = {"char-device": ["247:0"]}
    m_v2s, p_v2s = mod.gap_rule_model(json.dumps(v2_silent).encode())
    v2_claim = json.loads(json.dumps(v2))
    v2_claim["claim"] = "R67-C1"
    _m_v2c, p_v2c = mod.gap_rule_model(json.dumps(v2_claim).encode())

    def score_all(model):
        out = {}
        for cid, data in stored.items():
            ok, _why = mod.disposition_check(data["gaps"], data["diags"],
                                             data["nonreg"], model,
                                             data["real_root"], data["real_od"])
            out[cid] = ok
        return out

    flipped = score_all(m_v2t)
    with_silent = score_all(m_v2s)
    doc["rule_decomposition"] = {
        "only_required_char_device_differs": req_delta == {
            "char-device": [True, False]},
        "flip_char_device_back_to_required": {
            "per_carrier": flipped,
            "gaps_ok": sum(1 for v in flipped.values() if v),
            "equals_round50": flipped == {k: v["round50"]
                                          for k, v in recompute.items()},
            "problems": p_v2t,
        },
        "restore_round50_silent_row_on_v2": {
            "per_carrier": with_silent,
            "gaps_ok": sum(1 for v in with_silent.values() if v),
            "changes_any_carrier": with_silent != {
                k: v["round67"] for k, v in recompute.items()},
            "problems": p_v2s,
        },
        "adding_a_claim_key_would_fail_the_binding": {
            "problems": p_v2c,
            "would_fail": bool(p_v2c),
            "note": "gap_rule_model hard-codes claim R50-C1; the round-67 rule "
                    "must stay claim-less or b:gap_rule_ok is false",
        },
    }

    # --- fixtures -------------------------------------------------------------
    fixtures = []

    def run_fixture(fid, spec_ref, desc, cid, mutate, expect_v2, want_v2,
                    expect_r50, want_r50, clause):
        d = rewrite(fx, cid, fid)
        before_gaps, before_rows = len(d["gaps"]), list(d["nonreg"])
        base_v2, base_note = check(fx, d, model_v2)
        mutate(d)
        v2ok, v2note = check(fx, d, model_v2)
        r50ok, r50note = check(fx, d, model_r50)
        rec = {
            "id": fid, "spec_ref": spec_ref, "carrier": cid,
            "description": desc,
            "own_root": d["root"],
            "own_trusted_run_root": (d["scratch_rel"] + "/run"),
            "output_directory": d["scratch_rel"] + "/run/extract",
            "baseline_round67_pass": base_v2,
            "baseline_note": base_note,
            "delta": {"gaps": len(d["gaps"]) - before_gaps,
                      "nonregular_rows": len(d["nonreg"]) - len(before_rows),
                      "rows_dropped": dropped_rows(before_rows, d["nonreg"])},
            "round67": {"expected": expect_v2, "observed": "pass" if v2ok else "fail",
                        "note": v2note,
                        "reason_matches": bool((not want_v2) or re.search(want_v2, v2note)),
                        "correct": bool((v2ok == (expect_v2 == "pass"))
                                        and (not want_v2 or re.search(want_v2, v2note)))},
            "round50": {"expected": expect_r50, "observed": "pass" if r50ok else "fail",
                        "note": r50note,
                        "reason_matches": bool((not want_r50) or re.search(want_r50, r50note)),
                        "correct": bool((r50ok == (expect_r50 == "pass"))
                                        and (not want_r50 or re.search(want_r50, r50note)))},
            "clause": clause,
        }
        rec["fired_correctly"] = (rec["round67"]["correct"]
                                  and rec["round50"]["correct"]
                                  and base_v2)
        fixtures.append(rec)
        return d

    # baseline at fixture level: the round-50 measurement failure the claim repairs
    run_fixture("base-g7581", "-", "unmutated g7581 envelope under its own root: the "
                "round-50 rule still fails on the 13 unrecorded char devices",
                "g7581", lambda d: None,
                "pass", None, "fail", r"required entry with no disposition.*dev/pts/0",
                "gaps_ok")
    run_fixture("base-c6490", "-", "unmutated c6490 envelope under its own root",
                "c6490", lambda d: None,
                "pass", None, "pass", None, "gaps_ok")

    # (a) block-device class boundary
    def a0(d):
        add_row(d, DEV_BLOCK, "block-device")
    run_fixture("a0-block-device-no-gap", "(a)", "append a block-device oracle row "
                "with NO gap: the class is not required, so this must NOT fail",
                "c6490", a0, "pass", None, "pass", None, "gaps_ok")

    def a1(d):
        add_row(d, DEV_BLOCK, "block-device")
        d["gaps"].append(gap(path_in_root(d, DEV_BLOCK), "unpublished-entry",
                             path_in_root(d, DEV_BLOCK)))
    run_fixture("a1-block-device-with-gap", "(a)+", "append a block-device row WITH "
                "an unpublished-entry gap: allowed.block-device is [], so the rule "
                "rejects the gap while waiving the row",
                "g7581", a1, "fail", r"not allowed for 'block-device' entry",
                "fail", r"not allowed for 'block-device' entry", "gaps_ok")

    # (b) fifo class boundary
    def b0(d):
        add_row(d, DEV_FIFO, "fifo")
        d["gaps"].append(gap(path_in_root(d, DEV_FIFO), "unpublished-entry",
                             path_in_root(d, DEV_FIFO)))
    run_fixture("b0-fifo-with-gap", "(b)-before", "append a fifo row WITH its "
                "unpublished-entry gap: the gap is admitted and the class is not "
                "required", "c6490", b0, "pass", None, "pass", None, "gaps_ok")

    def b1(d):
        add_row(d, DEV_FIFO, "fifo")
    run_fixture("b1-fifo-gap-removed", "(b)", "append a fifo row whose "
                "unpublished-entry gap is ABSENT: fifo is not required, so this "
                "must NOT fail", "c6490", b1, "pass", None, "pass", None, "gaps_ok")

    def b2(d):
        add_row(d, DEV_FIFO, "fifo")
        d["gaps"].append(gap(path_in_root(d, DEV_FIFO),
                             "missing-extractor-dependency",
                             path_in_root(d, DEV_FIFO)))
    run_fixture("b2-fifo-wrong-gap-kind", "(b)+", "a fifo row with a gap kind that "
                "is not in allowed.fifo", "g7581", b2,
                "fail", r"not allowed for 'fifo' entry", "fail",
                r"not allowed for 'fifo' entry", "gaps_ok")

    # (c) gap kind not in allowed for its entry kind
    def c0(d):
        for g in d["gaps"]:
            if g.get("kind") == "unpublished-entry":
                g["kind"] = "depth-limited"
                break
    run_fixture("c0-structural-kind-with-path", "(c)", "a depth-limited gap that "
                "carries a path (structural kinds may not)", "g7581", c0,
                "fail", r"structural gap kind 'depth-limited' carries a path",
                "fail", r"structural gap kind 'depth-limited' carries a path",
                "gaps_ok")

    def c1(d):
        d["gaps"].append(gap(path_in_root(d, "bin"), "unpublished-entry",
                             path_in_root(d, "bin")))
    run_fixture("c1-gap-on-empty-allowed-kind", "(c)+", "an unpublished-entry gap "
                "naming a dir row (allowed.dir == [])", "g7581", c1,
                "fail", r"not allowed for 'dir' entry", "fail",
                r"not allowed for 'dir' entry", "gaps_ok")

    def c2(d):
        d["gaps"].append(gap(path_in_root(d, "bin/adsl"),
                             "missing-extractor-dependency",
                             path_in_root(d, "bin/adsl")))
    run_fixture("c2-foreign-kind-with-path", "(c)+", "a REA-only gap kind carrying "
                "a symlink path", "g7581", c2, "fail", r"not allowed for 'symlink'",
                "fail", r"not allowed for 'symlink'", "gaps_ok")

    def c3(d):
        d["gaps"].append(gap(None, "missing-extractor-dependency"))
    run_fixture("c3-pathless-foreign-kind", "(c)+", "a path-less gap kind with no "
                "structural allowance", "g7581", c3,
                "fail", r"no path and no structural allowance", "fail",
                r"no path and no structural allowance", "gaps_ok")

    def c4(d):
        d["gaps"].append(gap(None, "depth-limited"))
    run_fixture("c4-structural-allowance-exceeded", "(c)+", "a second path-less "
                "depth-limited gap (allowance 1)", "g7581", c4,
                "fail", r"structural gaps over allowance", "fail",
                r"structural gaps over allowance", "gaps_ok")

    def c5(d):
        d["gaps"].append(gap(None, "unknown-chunk-handler"))
    run_fixture("c5-zero-allowance-kind", "(c)+", "one path-less "
                "unknown-chunk-handler gap (allowance 0)", "g7581", c5,
                "fail", r"structural gaps over allowance", "fail",
                r"structural gaps over allowance", "gaps_ok")

    # (d) removal diagnostics
    def d1(d):
        target = "dev/led"          # char-device, detail 247:0
        for x in d["diags"]:
            rel = fx["mod"].diagnostic_rel(x, d["root"], d["od"])
            if rel == "dev/log":
                x["report"]["link"] = "%s/run/rea/%s/%s" % (d["base"], d["root"], target)
                break
        d["gaps"].append(gap(path_in_root(d, "dev/log"), "unpublished-entry",
                             path_in_root(d, "dev/log")))
    run_fixture("d1-removal-names-char-device", "(d)", "a MaliciousSymlinkRemoved "
                "diagnostic naming a char-device entry (removed.kinds is symlink "
                "only)", "g7581", d1, "fail", r"names a 'char-device' entry",
                "fail", r"names a 'char-device' entry", "removal")

    def d2(d):
        add_row(d, DEV_FIFO, "fifo")
        for x in d["diags"]:
            rel = fx["mod"].diagnostic_rel(x, d["root"], d["od"])
            if rel == "dev/log":
                x["report"]["link"] = "%s/run/rea/%s/%s" % (d["base"], d["root"], DEV_FIFO)
                break
        d["gaps"].append(gap(path_in_root(d, "dev/log"), "unpublished-entry",
                             path_in_root(d, "dev/log")))
    run_fixture("d2-removal-names-fifo", "(d)+", "a removal diagnostic naming a fifo "
                "entry", "g7581", d2, "fail", r"names a 'fifo' entry", "fail",
                r"names a 'fifo' entry", "removal")

    def d3(d):
        d["gaps"].append(gap(path_in_root(d, "dev/log"), "unpublished-entry",
                             path_in_root(d, "dev/log")))
    run_fixture("d3-gapped-and-removed", "(d)+", "a symlink entry that is both "
                "gapped and removed (exclusivity)", "g7581", d3,
                "fail", r"both gapped and removed", "fail",
                r"both gapped and removed", "removal")

    def d4(d):
        for x in d["diags"]:
            rel = fx["mod"].diagnostic_rel(x, d["root"], d["od"])
            if rel == "dev/log":
                x["report"]["link"] = "/var/tmp/log"
                break
        d["gaps"].append(gap(path_in_root(d, "dev/log"), "unpublished-entry",
                             path_in_root(d, "dev/log")))
    run_fixture("d4-removal-outside-trusted-root", "(d)+", "a removal link outside "
                "the trusted run root", "g7581", d4,
                "fail", r"without a path under the root", "fail",
                r"without a path under the root", "removal")

    def d5(d):
        for x in d["diags"]:
            rel = fx["mod"].diagnostic_rel(x, d["root"], d["od"])
            if rel == "dev/log":
                x["report"]["link"] = "%s/run/rea/%s/dev/ghost" % (d["base"], d["root"])
                break
        d["gaps"].append(gap(path_in_root(d, "dev/log"), "unpublished-entry",
                             path_in_root(d, "dev/log")))
    run_fixture("d5-removal-names-no-row", "(d)+", "a removal diagnostic that "
                "resolves to no non-regular entry", "g7581", d5,
                "fail", r"removal resolves to 0 non-regular entries", "fail",
                r"removal resolves to 0 non-regular entries", "removal")

    # (e) detail scoping: the waiver is class-wide, not row-scoped
    def e1(d):
        d["nonreg"] = [(rel, kind, "999:9" if kind == "char-device" else det)
                       for rel, kind, det in d["nonreg"]]
    run_fixture("e1-char-device-new-detail", "(e)", "the c6490 char device with a "
                "detail the round-50 silent row never listed: round 50 fails, round "
                "67 admits it with no evidence at all", "c6490", e1,
                "pass", None, "fail", r"dev/led", "gaps_ok")

    # (h) kind spelling drift is unrequired at the function level
    def h1(d):
        add_row(d, "dev/x", "char_device")
    d_h = run_fixture("h1-kind-spelling-drift", "(h)", "a row whose kind is spelled "
                      "char_device: an unknown kind defaults to not-required, so the "
                      "function admits it; the score-level gap_rule_ok binding is what "
                      "catches it", "c6490", h1, "pass", None, "pass", None, "gaps_ok")
    uncovered = sorted({"char_device"} - set(model_v2["allowed"]))
    fixtures[-1]["score_level_binding"] = {
        "kinds_seen_extra": uncovered,
        "gap_rule_ok_would_be_false": bool(uncovered),
        "note": "measure() computes uncovered = kinds_seen - allowed keys; a drifted "
                "kind therefore fails b:gap_rule_ok even though disposition_check "
                "alone admits the row"}

    # --- (f) publication check over every kind ---------------------------------
    d_f = rewrite(fx, "g7581", "f-publication")
    add_row(d_f, DEV_BLOCK, "block-device")
    add_row(d_f, DEV_FIFO, "fifo")
    files = mod.published(d_f["env"])
    probes = {"symlink": "bin/adsl", "char-device": "dev/led", "dir": "bin",
              "fifo": DEV_FIFO, "block-device": DEV_BLOCK}
    invented = []
    for kind, rel in probes.items():
        fp = "%s/%s" % (d_f["root"], rel)
        invented.append((kind, rel, fp))
        files.append((fp, "0" * 64, 0))
    files.append(("%s/usr/bin/not-a-nonregular-entry" % d_f["root"], "0" * 64, 0))
    hits = mod.nonregular_published(files, d_f["nonreg"], d_f["root"])
    publication = {
        "id": "f-publication", "spec_ref": "(f)", "own_root": d_f["root"],
        "probes": [{"kind": k, "rel": rel, "named": fp in hits}
                   for k, rel, fp in invented],
        "non_entry_regular_file_named": ("%s/usr/bin/not-a-nonregular-entry"
                                        % d_f["root"]) in hits,
        "all_five_kinds_named": all(fp in hits for _k, _r, fp in invented),
        "clause": "nonregular_unpublished_ok"}
    publication["fired_correctly"] = (publication["all_five_kinds_named"]
                                      and not publication["non_entry_regular_file_named"])

    # --- (g) fail-closed on an unknown root ------------------------------------
    d_g = rewrite(fx, "g7581", "g-root-none")
    g_ok, g_note = mod.disposition_check(d_g["gaps"], d_g["diags"], d_g["nonreg"],
                                         model_v2, None, d_g["od"])
    root_none = {"id": "g-root-none", "spec_ref": "(g)", "expected": "fail",
                 "observed": "pass" if g_ok else "fail", "note": g_note,
                 "clause": "gaps_ok",
                 "fired_correctly": (not g_ok) and "no extract root" in g_note}

    doc["fixtures"] = fixtures
    doc["supplementary"] = {"publication": publication, "root_none": root_none}

    required_ids = ["a0-block-device-no-gap", "b1-fifo-gap-removed",
                    "c0-structural-kind-with-path", "d1-removal-names-char-device"]
    by_id = {f["id"]: f for f in fixtures}
    doc["seat_required_fixtures"] = {
        "ids": required_ids,
        "all_correct": all(by_id[i]["fired_correctly"] for i in required_ids),
        "polarity": {i: {"expected_round67": by_id[i]["round67"]["expected"],
                         "observed": by_id[i]["round67"]["observed"]}
                     for i in required_ids}}
    doc["all_fixtures_correct"] = all(f["fired_correctly"] for f in fixtures)
    doc["instrument_moved_during_run"] = sha256_file(COUNTER) != working
    doc["control_reproduced"] = (
        ctl["gaps_ok_round50"] == 2 and ctl["gaps_ok_round67"] == TARGET
        and ctl["control_ok"] is True and cp.returncode == 0
        and doc["wrapper_control"]["same_numbers_as_l1_pre"]
        and doc["independent_recompute"]["matches_wrapper"]
        and doc["instrument_pins"]["working_matches_head"]
        and doc["pins"]["rule_v2"]["all_four_agree"]
        and doc["carrier_fresh_ok_support"]["freshness_holds"]
        and doc["instrument_pins"]["control_receipt_binding"]["binds_second_conjunct"]
        and doc["instrument_pins"]["gaprule_patch"]["lane_relative"]
        and doc["instrument_pins"]["gaprule_patch"]["resolves_at_freeze"]
        and doc["instrument_pins"]["control_with_freeze_blob"]["same_numbers_as_working"]
        and not doc["instrument_moved_during_run"])
    doc["verdict"] = ("battery_green" if (doc["control_reproduced"]
                                          and doc["all_fixtures_correct"]
                                          and (doc["seat_required_fixtures"]
                                               ["all_correct"])
                                          and publication["fired_correctly"]
                                          and root_none["fired_correctly"])
                      else "battery_red")
    (LANE / "red.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n",
                                   encoding="utf-8")
    print(json.dumps({"verdict": doc["verdict"],
                      "control_reproduced": doc["control_reproduced"],
                      "fixtures_correct": sum(1 for f in fixtures
                                              if f["fired_correctly"]),
                      "fixtures_total": len(fixtures),
                      "publication": publication["fired_correctly"],
                      "root_none": root_none["fired_correctly"],
                      "wrapper": [ctl["gaps_ok_round50"], ctl["gaps_ok_round67"]],
                      "out": str(LANE / "red.json")}, indent=1, sort_keys=True))
    return 0 if doc["verdict"] == "battery_green" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(SCRATCH, ignore_errors=True)
