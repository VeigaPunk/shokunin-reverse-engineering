#!/usr/bin/env python3
"""New round-69 mutants for tools/round-69/packed-elf.py (MutBattery seat)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kaidoku-r69/MutBattery"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FROZEN = os.path.join(LANE, "tools/round-69/packed-elf.py")
FROZEN_SHA = "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc"
OP_FREEZE = "f15998102f1ce3569e61faa2ac6f286bc414538e"
REA = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
PY = sys.executable

sys.path.insert(0, os.path.join(LANE, "tools/round-69"))
import controls  # noqa: E402  (frozen synthetic-receipt builder)

MUTANTS = [
    ("MB01_control_default",
     '                 control_ok: bool = True) -> dict:',
     '                 control_ok: bool = False) -> dict:',
     "carrier_arms default control_ok"),
    ("MB02_fold_empty_control",
     '    control_ok = bool(carriers) and all(c["arms"]["control_ok"] for c in carriers)',
     '    control_ok = all(c["arms"]["control_ok"] for c in carriers)',
     "fold empty-set control"),
    ("MB03_fold_missing_control_arm",
     'c["arms"]["control_ok"] for c in carriers',
     'c["arms"].get("control_ok", True) for c in carriers',
     "fold absent control arm"),
    ("MB04_fold_matched_ge",
     'met_target": matched == target and control_ok}',
     'met_target": matched >= target and control_ok}',
     "fold matched == target"),
    ("MB05_receipt_ratio_bound",
     'or ratio > 0.75:',
     'or ratio > 1.0:',
     "check_receipt ratio bound"),
    ("MB06_receipt_shared_object",
     'if "shared-object" not in kinds:',
     'if "executable" not in kinds:',
     "check_receipt shared-object clause"),
    ("MB07_elf_format_len",
     '    return found if len(found) == 4 else None',
     '    return found if len(found) >= 3 else None',
     "elf_format completeness"),
    ("MB08_preflight_order",
     '''    for tool in ("node", "git", "readelf"):
        if shutil.which(tool) is None:
            raise Unevaluable(f"missing_tool: {tool}")
    if not os.path.isfile(upx) or not os.access(upx, os.X_OK):
        raise Unevaluable(f"missing_tool: upx ({upx})")
    if not os.path.isdir(pkg) or not os.path.isfile(os.path.join(pkg, "package.json")):
        raise Unevaluable(f"missing_tool: rea package ({pkg})")
    if check_work:
        if not os.path.isdir(work):
            raise Unevaluable(f"work_unusable: not a directory ({work})")
        try:
            probe = tempfile.mkdtemp(prefix="preflight-", dir=work)
            os.rmdir(probe)
        except OSError as exc:
            raise Unevaluable(f"work_unusable: not writable ({work}: {exc.__class__.__name__})")''',
     '''    if check_work:
        if not os.path.isdir(work):
            raise Unevaluable(f"work_unusable: not a directory ({work})")
        try:
            probe = tempfile.mkdtemp(prefix="preflight-", dir=work)
            os.rmdir(probe)
        except OSError as exc:
            raise Unevaluable(f"work_unusable: not writable ({work}: {exc.__class__.__name__})")
    for tool in ("node", "git", "readelf"):
        if shutil.which(tool) is None:
            raise Unevaluable(f"missing_tool: {tool}")
    if not os.path.isfile(upx) or not os.access(upx, os.X_OK):
        raise Unevaluable(f"missing_tool: upx ({upx})")
    if not os.path.isdir(pkg) or not os.path.isfile(os.path.join(pkg, "package.json")):
        raise Unevaluable(f"missing_tool: rea package ({pkg})")''',
     "preflight node/before-work order"),
    ("MB09_preflight_tool_order",
     '    for tool in ("node", "git", "readelf"):',
     '    for tool in ("git", "node", "readelf"):',
     "preflight tool tuple order"),
    ("MB10_section_branch_sentinel",
     'if "There are no sections in this file" in readelf_text:',
     'if "There are no section headers in this file" in readelf_text:',
     "section_count no-sections sentinel"),
    ("MB11_section_branch_return",
     '''    if "There are no sections in this file" in readelf_text:
        return 0''',
     '''    if "There are no sections in this file" in readelf_text:
        return 1''',
     "section_count no-sections return"),
    ("MB12_refusal_code_floor",
     'and (model.get("refusal_code_bytes") or 0) > 200)',
     'and (model.get("refusal_code_bytes") or 0) > 0)',
     "refusal 200-byte floor"),
    ("MB13_refusal_unpacked_rc",
     '''        refusal_ok = (model["refusal_packed_rc"] != 0 and model["refusal_unpacked_rc"] == 0
                      and model.get("refusal_symbol_present") is True''',
     '''        refusal_ok = (model["refusal_packed_rc"] != 0
                      and model.get("refusal_symbol_present") is True''',
     "refusal unpacked_rc clause"),
    ("MB14_receipt_met_target",
     '''    if receipt.get("met_target") is not True:
        failing.append("met_target not true")
''',
     '',
     "check_receipt met_target clause"),
    ("MB15_receipt_failing_truthiness",
     '    if receipt.get("failing") != []:',
     '    if receipt.get("failing"):',
     "check_receipt failing == []"),
    ("MB16_receipt_counts",
     '''            failing.append(f"{cid}: counts absent")''',
     '''            pass''',
     "check_receipt counts presence"),
    ("MB17_receipt_arm_value",
     '            if value is not True:',
     '            if value is False:',
     "check_receipt arm value identity"),
    ("MB18_ratio_constant",
     '''                "before_ceiling_ratio": round(
                    c["before_max_procedures"] / orig_counts["procedure_count"], 4),''',
     '''                "before_ceiling_ratio": round(0.0, 4),''',
     "score() ratio derivation"),
    ("MB19_check_work_false",
     'packer_env = preflight(upx, pkg, work, check_work=not skip_run)',
     'packer_env = preflight(upx, pkg, work, check_work=False)',
     "preflight work gate"),
    ("MB20_version_fallback",
     '    version = version[0] if version else ""',
     '    version = version[0] if version else UPX_VERSION_PIN',
     "preflight version pin fallback"),
]


def run(argv, env=None, timeout=300):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, env=env)
    return {"argv": argv, "rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def selftest(path):
    rec = run([PY, "-I", "-B", path, "--selftest"])
    payload = None
    for text in (rec["stdout"], rec["stderr"]):
        try:
            cand = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(cand, dict) and "cases" in cand:
            payload = cand
            break
    rec["parsed"] = payload
    return rec


def check_receipt(path, receipt):
    rec = run([PY, "-I", "-B", path, "--check-receipt", receipt])
    payload = None
    for text in (rec["stdout"], rec["stderr"]):
        try:
            cand = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(cand, dict) and "check" in cand:
            payload = cand
            break
    rec["parsed"] = payload
    return rec


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")


def build_receipts(dirpath):
    receipts = {}
    receipts["pass"] = controls.synthetic_receipt(False)
    receipts["loose"] = controls.synthetic_receipt(True)
    exec3 = controls.synthetic_receipt(False)
    for c in exec3["carriers"]:
        if c["id"] == "libz":
            c["kind"] = "executable"
    receipts["exec3"] = exec3
    metfalse = controls.synthetic_receipt(False)
    metfalse["met_target"] = False
    receipts["metfalse"] = metfalse
    nofail = controls.synthetic_receipt(False)
    del nofail["failing"]
    receipts["nofail"] = nofail
    nocounts = controls.synthetic_receipt(False)
    nocounts["carriers"][2].pop("orig_counts")
    nocounts["carriers"][2].pop("packed_counts")
    receipts["nocounts"] = nocounts
    nulls = controls.synthetic_receipt(False)
    nulls["carriers"][0]["arms"]["identity_ok"] = None
    receipts["nullarm"] = nulls
    liar = controls.synthetic_receipt(False)
    for c in liar["carriers"]:
        if c["id"] == "libz":
            c["before_ceiling_ratio"] = 0.0001  # ceiling 120 / orig 184 = 0.6522
    receipts["ratio_liar"] = liar
    dupe = controls.synthetic_receipt(False)
    dupe["carriers"][1] = json.loads(json.dumps(dupe["carriers"][0]))
    receipts["dupe"] = dupe
    ids = controls.synthetic_receipt(False)
    for i, c in enumerate(ids["carriers"]):
        c["id"] = f"carrier-{i}"
    receipts["ids"] = ids
    paths = {}
    for name, obj in receipts.items():
        p = os.path.join(dirpath, f"receipt-{name}.json")
        write_json(p, obj)
        paths[name] = p
    return paths


def preflight_probe(path, work, env, upx=None):
    argv = [PY, "-I", "-B", path, "--root", LANE, "--rev", OP_FREEZE,
            "--pkg", REA, "--work", work]
    if upx:
        argv += ["--upx", upx]
    rec = run(argv, env=env)
    payload = None
    for text in (rec["stdout"], rec["stderr"]):
        for chunk in [text] + text.splitlines()[::-1]:
            chunk = chunk.strip()
            if not chunk.startswith("{"):
                continue
            try:
                cand = json.loads(chunk)
            except json.JSONDecodeError:
                continue
            if isinstance(cand, dict) and "unevaluable" in cand:
                payload = cand
                break
        if payload:
            break
    rec["unevaluable"] = (payload or {}).get("unevaluable")
    return rec


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    work = os.path.join(SCRATCH, "work")
    os.makedirs(work, exist_ok=True)
    receipts = build_receipts(SCRATCH)
    with open(FROZEN, "rb") as fh:
        source_bytes = fh.read()
    import hashlib
    frozen_sha = hashlib.sha256(source_bytes).hexdigest()
    assert frozen_sha == FROZEN_SHA, frozen_sha
    source = source_bytes.decode("utf-8")

    # pristine copy
    pristine = os.path.join(SCRATCH, "pristine-packed-elf.py")
    with open(pristine, "wb") as fh:
        fh.write(source_bytes)
    base_selftest = selftest(pristine)
    base_receipts = {n: check_receipt(pristine, p) for n, p in receipts.items()}
    print(json.dumps({"phase": "baseline",
                      "selftest": {k: base_selftest[k] for k in ("rc",)},
                      "parsed": base_selftest["parsed"],
                      "receipts": {n: {"rc": r["rc"],
                                       "failing": (r["parsed"] or {}).get("failing")}
                                   for n, r in base_receipts.items()}},
                     indent=1, sort_keys=True))

    # preflight arm fixtures
    pathbin = os.path.join(SCRATCH, "pathbin")
    os.makedirs(pathbin, exist_ok=True)
    for tool_name in ("git", "readelf", "upx"):
        found = shutil.which(tool_name)
        link = os.path.join(pathbin, tool_name)
        if found and not os.path.exists(link):
            os.symlink(found, link)
    ro = os.path.join(SCRATCH, "ro")
    os.makedirs(ro, exist_ok=True)
    os.chmod(ro, 0o500)
    env_no_node = {"PATH": pathbin, "HOME": os.environ.get("HOME", "/root"),
                   "LANG": os.environ.get("LANG", "C")}
    env_normal = {"PATH": os.environ.get("PATH", "/usr/bin"),
                  "HOME": os.environ.get("HOME", "/root"),
                  "LANG": os.environ.get("LANG", "C")}
    base_arms = {
        "A1_missing_node": preflight_probe(pristine, work, env_no_node),
        "A2_work_unusable": preflight_probe(pristine, ro, env_normal),
        "combined_node_and_work": preflight_probe(pristine, ro, env_no_node),
    }

    results = []
    for mid, old, new, site in MUTANTS:
        count = source.count(old)
        row = {"id": mid, "site": site, "old": old, "new": new,
               "match_count": count}
        if count != 1:
            row["verdict"] = "unevaluable"
            row["error"] = f"patch site matched {count} times"
            results.append(row)
            continue
        mutant = os.path.join(SCRATCH, mid + "-packed-elf.py")
        with open(mutant, "w", encoding="utf-8") as fh:
            fh.write(source.replace(old, new, 1))
        with open(mutant, "rb") as fh:
            row["sha256"] = hashlib.sha256(fh.read()).hexdigest()
        st = selftest(mutant)
        row["selftest"] = {"rc": st["rc"],
                           "cases": (st["parsed"] or {}).get("cases"),
                           "failed": (st["parsed"] or {}).get("failed"),
                           "ok": (st["parsed"] or {}).get("ok")}
        cr = {}
        for name, path in receipts.items():
            r = check_receipt(mutant, path)
            cr[name] = {"rc": r["rc"],
                        "failing": (r["parsed"] or {}).get("failing"),
                        "met": (r["parsed"] or {}).get("met")}
        row["check_receipt"] = cr
        diff = {n: {"pristine_rc": base_receipts[n]["rc"], "mutant_rc": cr[n]["rc"]}
                for n in receipts if cr[n]["rc"] != base_receipts[n]["rc"]}
        row["receipt_rc_deviations"] = diff
        row["preflight"] = {
            "A1_missing_node": preflight_probe(mutant, work, env_no_node),
            "A2_work_unusable": preflight_probe(mutant, ro, env_normal),
            "combined_node_and_work": preflight_probe(mutant, ro, env_no_node),
        }
        for k in row["preflight"]:
            row["preflight"][k] = {"rc": row["preflight"][k]["rc"],
                                   "unevaluable": row["preflight"][k]["unevaluable"]}
        if st["rc"] != 0:
            failed = (st["parsed"] or {}).get("failed") or []
            row["verdict"] = "killed_by_selftest"
            row["killed_case"] = failed
        elif diff:
            row["verdict"] = "killed_by_check_receipt"
        else:
            row["verdict"] = "survived"
        row["preflight_deviations"] = {
            k: {"pristine": (base_arms[k]["unevaluable"]),
                "mutant": row["preflight"][k]["unevaluable"]}
            for k in base_arms
            if (base_arms[k]["unevaluable"] != row["preflight"][k]["unevaluable"]
                or base_arms[k]["rc"] != row["preflight"][k]["rc"])}
        results.append(row)

    out = {"frozen_sha256": frozen_sha, "frozen_path": FROZEN,
           "operative_freeze_rev": OP_FREEZE,
           "baseline": {"selftest": base_selftest["parsed"],
                        "receipts": {n: {"rc": base_receipts[n]["rc"],
                                         "failing": (base_receipts[n]["parsed"] or {}).get("failing"),
                                         "met": (base_receipts[n]["parsed"] or {}).get("met")}
                                     for n in receipts},
                        "preflight": {k: {"rc": v["rc"], "unevaluable": v["unevaluable"]}
                                      for k, v in base_arms.items()}},
           "receipts": receipts,
           "mutants": results,
           "counts": {"total": len(results),
                      "survived": sum(1 for r in results if r["verdict"] == "survived"),
                      "killed_by_selftest": sum(1 for r in results if r["verdict"] == "killed_by_selftest"),
                      "killed_by_check_receipt": sum(1 for r in results if r["verdict"] == "killed_by_check_receipt"),
                      "unevaluable": sum(1 for r in results if r["verdict"] == "unevaluable")}}
    write_json(os.path.join(SCRATCH, "results.json"), out)

    # restore pristine bytes and prove it
    with open(pristine, "wb") as fh:
        fh.write(source_bytes)
    with open(pristine, "rb") as fh:
        restored = hashlib.sha256(fh.read()).hexdigest()
    with open(FROZEN, "rb") as fh:
        lane_after = hashlib.sha256(fh.read()).hexdigest()
    print(json.dumps({"phase": "restoration", "restored_sha256": restored,
                      "matches_frozen": restored == FROZEN_SHA,
                      "lane_file_sha256": lane_after,
                      "lane_untouched": lane_after == FROZEN_SHA},
                     indent=1))
    os.chmod(ro, 0o700)


if __name__ == "__main__":
    main()
