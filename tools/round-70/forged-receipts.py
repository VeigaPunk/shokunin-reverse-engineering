#!/usr/bin/env python3
"""forged-receipts.py - round-70 instrument (R70-C1 calibration, capability).

The receipt readers are proven able to fail on forged evidence (round-69
M69-8; QUALITY #114): ten forged shapes, each a minimal mutation of the
genuine round-69 landing receipt, are scored by BOTH the base readers
(tools/round-69/packed-elf.py --check-receipt and tools/round-69/contract-probe.py
at the base revision, which accept every shape) and the frozen round-70 readers
(tools/round-70/packed-elf.py --check-receipt --root . --rev <landing> and
tools/round-70/contract-probe.py), each shape carrying the clause that must
name its rejection:

  F1 wrong-rev          the recorded measured revision is swapped for the base
  F2 wrong-instrument   instrument.sha256 is zeroed
  F3 relabelled-source  a carrier row's source/pin are relabelled to another binary
  F4 ratio-underived    a before_ceiling_ratio that is not ceiling/orig (0.7)
  F5 inflated-orig      an original procedure count that contradicts the declared one
  F6 before-over-limit  a packed procedure count above its ceiling
  F7 rows-vs-matched    a dropped carrier row while carriers_matched keeps counting it
  F8 dropped-arm        a carrier whose identity_ok arm is missing
  F9 unknown-carrier    a carrier id that is not in the frozen table
  F10 absent-instrument the instrument block removed entirely

The genuine receipts still pass: the round-70 checker accepts the measured
run's receipt, and the round-70 probe scores it 6 of 6.  The battery also pins
tools/round-70/mutation-check.py: a wrong --expect-target-sha256 and a
--min-pristine-cases above the true floor each fail with their named clause,
two green runs sharing one --work record distinct work_dir values, and
--validate rejects a constant battery receipt with no mutant rows.

Exit: 0 every arm shows what it must; 1 the failing arms named; 2 could-not-
evaluate (unknown revision, unreadable material, bad argv).  `--selftest`
runs in-memory fixture cases including the wrong-world negative control that
shows the base-acceptance assertion can fail.  `--validate <receipt>` checks
a battery receipt's structural honesty.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/round-70/forged-receipts.py"


class Unevaluable(Exception):
    """Exit-2 class: the battery cannot score, so it claims nothing."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_to(root: str, rev: str, tool: str, scratch: str, name: str) -> str:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed rc={proc.returncode}")
    path = os.path.join(scratch, name)
    with open(path, "wb") as fh:
        fh.write(proc.stdout)
    os.chmod(path, 0o755)
    return path


def run(argv: list[str], timeout: int = 900) -> dict:
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    return {"rc": proc.returncode, "stdout": proc.stdout[-100000:],
            "stderr": proc.stderr[-2000:]}


def json_out(text: str) -> dict | None:
    stripped = text.strip()
    if stripped.startswith("{"):
        try:
            payload = json.loads(stripped)
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            pass
    for chunk in text.splitlines()[::-1]:
        chunk = chunk.strip()
        if not chunk.startswith("{"):
            continue
        try:
            payload = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    return None


def load_material(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise Unevaluable(f"material unreadable: {path}: {exc}")


def forge(material: dict, shape: str, base_rev: str) -> dict:
    """One minimal mutation per shape; the rest of the receipt stays genuine."""
    r = copy.deepcopy(material)
    if shape == "F1_wrong-rev":
        r["rev"] = base_rev
    elif shape == "F2_wrong-instrument":
        r["instrument"]["sha256"] = "0" * 64
    elif shape == "F3_relabelled-source":
        pin = sha256_bytes(open("/bin/ls", "rb").read()) if os.path.exists("/bin/ls") \
            else "e" * 64
        r["carriers"][0]["source"] = "/bin/ls"
        r["carriers"][0]["pin"] = pin
    elif shape == "F4_ratio-underived":
        r["carriers"][0]["before_ceiling_ratio"] = 0.7
    elif shape == "F5_inflated-orig":
        r["carriers"][0]["orig_counts"]["procedure_count"] = 5000
    elif shape == "F6_before-over-limit":
        r["carriers"][0]["packed_counts"]["procedure_count"] = 200
    elif shape == "F7_rows-vs-matched":
        r["carriers"] = [c for c in r["carriers"] if c.get("id") != "xxd"]
    elif shape == "F8_dropped-arm":
        del r["carriers"][0]["arms"]["identity_ok"]
    elif shape == "F9_unknown-carrier":
        r["carriers"][1]["id"] = "nope"
    elif shape == "F10_absent-instrument":
        del r["instrument"]
    elif shape == "F3L_relabelled-landing":
        pin = sha256_bytes(open("/bin/ls", "rb").read()) if os.path.exists("/bin/ls") \
            else "e" * 64
        r["carriers"][0]["source"] = "/bin/ls"
        r["carriers"][0]["pin"] = pin
    elif shape == "F9L_unknown-landing":
        r["carriers"][1]["id"] = "nope"
    else:
        raise Unevaluable(f"unknown shape: {shape}")
    return r


SHAPES = [
    ("F1_wrong-rev", "rev"),
    ("F2_wrong-instrument", "instrument.sha256"),
    ("F3_relabelled-source", "source"),
    ("F4_ratio-underived", "before_ceiling_ratio"),
    ("F5_inflated-orig", "orig_procedures"),
    ("F6_before-over-limit", "packed"),
    ("F7_rows-vs-matched", "carrier rows"),
    ("F8_dropped-arm", "arm identity_ok missing"),
    ("F9_unknown-carrier", "unknown carrier id"),
    ("F10_absent-instrument", "instrument absent"),
]
PROBE_SHAPES = {"F1_wrong-rev", "F2_wrong-instrument", "F3_relabelled-source",
                "F9_unknown-carrier", "F10_absent-instrument"}
# Landing-world identity shapes: cut from the landing receipt, so their
# producer fields are valid for the landing pair and only the frozen-table
# binding can reject them (removes the producer mismatch masking).
LANDING_PROBE_SHAPES = {"F3L_relabelled-landing": "source",
                        "F9L_unknown-landing": "unknown carrier id"}
PROBE_ARM_BY_SHAPE = {"F1_wrong-rev": "A6_packer_pin", "F2_wrong-instrument": "A6_packer_pin",
                      "F10_absent-instrument": "A6_packer_pin",
                      "F3_relabelled-source": "A5_carrier_record",
                      "F9_unknown-carrier": "A5_carrier_record",
                      "F3L_relabelled-landing": "A5_carrier_record",
                      "F9L_unknown-landing": "A5_carrier_record"}


def write_shape(shape_dir: str, shape: str, material: dict, base_rev: str) -> str:
    os.makedirs(shape_dir, exist_ok=True)
    path = os.path.join(shape_dir, f"{shape}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(forge(material, shape, base_rev), fh, indent=1, sort_keys=True)
    return path


def check(work: str, root: str, rev: str, base_rev: str, tool: str, base_tool: str,
          probe: str, base_probe: str, base_probe_rev: str, battery: str,
          base_material_path: str, landing_material_path: str, pkg: str) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    scratch = tempfile.mkdtemp(prefix="forged-receipts-", dir=work)
    reader = blob_to(root, rev, tool, scratch, "reader.py")
    base_reader = blob_to(root, base_rev, base_tool, scratch, "base-reader.py")
    probe_blob = blob_to(root, rev, probe, scratch, "probe.py")
    base_probe_blob = blob_to(root, base_probe_rev, base_probe, scratch, "base-probe.py")
    battery_blob = blob_to(root, rev, battery, scratch, "battery.py")
    base_material = load_material(base_material_path)
    landing_material = load_material(landing_material_path)
    shapes_out = []
    failures = []
    for shape, clause in SHAPES:
        shape_dir = os.path.join(scratch, shape)
        path = write_shape(shape_dir, shape, base_material, base_rev)
        # the base reader accepts every shape (the routed defect, reproduced)
        b = run([sys.executable, "-I", "-B", base_reader, "--check-receipt", path])
        bjson = json_out(b["stdout"]) or {}
        base_ok = b["rc"] == 0 and bjson.get("met") is True
        # the frozen checker rejects the shape, naming its clause
        l = run([sys.executable, "-I", "-B", reader, "--check-receipt", path,
                 "--root", root, "--rev", rev])
        ljson = json_out(l["stdout"]) or {}
        landed = any(clause in str(f) for f in ljson.get("failing") or [])
        row = {"shape": shape, "declared_clause": clause, "receipt": path,
               "base_rc": b["rc"], "base_met": bjson.get("met"),
               "landing_rc": l["rc"],
               "landing_failing": (ljson.get("failing") or [])[:6],
               "clause_found": landed}
        # the frozen probe rejects the identity shapes on its receipt arms
        if shape in PROBE_SHAPES:
            p = run([sys.executable, "-I", "-B", probe_blob, "--root", root,
                     "--rev", rev, "--tool", tool, "--pkg", pkg, "--work", shape_dir,
                     "--receipt", path])
            pjson = json_out(p["stdout"]) or {}
            armmap = {a.get("id"): a.get("ok") for a in (pjson.get("arms") or [])
                      if a.get("id") in ("A5_carrier_record", "A6_packer_pin")}
            declared_arm = PROBE_ARM_BY_SHAPE[shape]
            row["probe_landing_rc"] = p["rc"]
            row["probe_declared_arm"] = declared_arm
            row["probe_arms"] = armmap
            rejected = (p["rc"] == 1 and armmap.get(declared_arm) is False)
            if not rejected:
                failures.append(f"{shape}: frozen probe did not reject it on "
                                f"{declared_arm} (rc {p['rc']}, arms {armmap})")
            pb = run([sys.executable, "-I", "-B", base_probe_blob, "--root", root,
                      "--rev", base_probe_rev, "--tool", base_tool, "--pkg", pkg,
                      "--work", shape_dir, "--receipt", path])
            row["probe_base_rc"] = pb["rc"]
            if pb["rc"] != 0:
                failures.append(f"{shape}: base probe did not accept it")
        if not base_ok:
            failures.append(f"{shape}: base reader did not accept it "
                            f"(rc {b['rc']}, met {bjson.get('met')})")
        if l["rc"] != 1 or not landed:
            failures.append(f"{shape}: frozen checker did not name its clause "
                            f"'{clause}' (rc {l['rc']}, failing "
                            f"{(ljson.get('failing') or [])[:3]})")
        shapes_out.append(row)
    landing_probe_rows = []
    for shape, clause in LANDING_PROBE_SHAPES.items():
        shape_dir = os.path.join(scratch, shape)
        lmat = load_material(landing_material_path)
        if not isinstance(lmat, dict) or not lmat.get("carriers"):
            raise Unevaluable("landing material unusable for landing-world shapes")
        path = write_shape(shape_dir, shape, lmat, base_rev)
        p = run([sys.executable, "-I", "-B", probe_blob, "--root", root,
                 "--rev", rev, "--tool", tool, "--pkg", pkg, "--work", shape_dir,
                 "--receipt", path])
        pjson = json_out(p["stdout"]) or {}
        armmap = {a.get("id"): a.get("ok") for a in (pjson.get("arms") or [])
                  if a.get("id") in ("A5_carrier_record", "A6_packer_pin")}
        declared_arm = PROBE_ARM_BY_SHAPE[shape]
        ok = p["rc"] == 1 and armmap.get(declared_arm) is False \
            and armmap.get("A6_packer_pin") is True
        landing_probe_rows.append({"shape": shape, "declared_clause": clause,
                                   "declared_arm": declared_arm, "receipt": path,
                                   "probe_rc": p["rc"], "probe_arms": armmap, "ok": ok})
        if not ok:
            failures.append(f"{shape}: frozen probe did not reject it on {declared_arm} "
                            f"with A6 true (rc {p['rc']}, arms {armmap})")
    # the genuine receipts still pass the frozen readers
    g = run([sys.executable, "-I", "-B", reader, "--check-receipt",
             landing_material_path, "--root", root, "--rev", rev])
    gjson = json_out(g["stdout"]) or {}
    gp = run([sys.executable, "-I", "-B", probe_blob, "--root", root, "--rev", rev,
              "--tool", tool, "--pkg", pkg, "--work", scratch,
              "--receipt", landing_material_path])
    gpjson = json_out(gp["stdout"]) or {}
    genuine = {"checker_rc": g["rc"], "met": gjson.get("met"),
               "probe_rc": gp["rc"], "probe_arms_passed": gpjson.get("arms_passed"),
               "probe_target": gpjson.get("target")}
    if g["rc"] != 0 or gjson.get("met") is not True:
        failures.append("genuine landing receipt rejected by the frozen checker")
    if gp["rc"] != 0 or gpjson.get("arms_passed") != gpjson.get("target"):
        failures.append("genuine landing receipt rejected by the frozen probe")
    # the battery's own pins
    wrong_pin = run([sys.executable, "-I", "-B", battery_blob, "--root", root,
                     "--rev", rev, "--tool", tool, "--patch-set", "r70",
                     "--work", scratch, "--expect-target-sha256", "dead" * 8])
    wpjson = json_out(wrong_pin["stdout"]) or {}
    wrong_pin_named = "target pin mismatch" in json.dumps(wpjson)
    floor = run([sys.executable, "-I", "-B", battery_blob, "--root", root,
                 "--rev", rev, "--tool", tool, "--patch-set", "r70",
                 "--work", scratch, "--min-pristine-cases", "24"])
    fljson = json_out(floor["stdout"]) or {}
    floor_named = "pristine.cases" in json.dumps(fljson)
    w1 = run([sys.executable, "-I", "-B", battery_blob, "--root", root,
              "--rev", rev, "--tool", tool, "--patch-set", "r70",
              "--work", scratch, "--min-pristine-cases", "0"])
    w2 = run([sys.executable, "-I", "-B", battery_blob, "--root", root,
              "--rev", rev, "--tool", tool, "--patch-set", "r70",
              "--work", scratch, "--min-pristine-cases", "0"])
    wa = (json_out(w1["stdout"]) or {}).get("work_dir")
    wb = (json_out(w2["stdout"]) or {}).get("work_dir")
    constant = os.path.join(scratch, "constant-battery.json")
    with open(constant, "w", encoding="utf-8") as fh:
        json.dump({"survivors": [], "killed": [], "mutants": [], "pristine_ok": True,
                   "ok": True, "work_dir": scratch, "target_sha256": "f" * 64}, fh)
    val = run([sys.executable, "-I", "-B", battery_blob, "--validate", constant])
    work_arm_ok = (bool(wa) and bool(wb) and wa != wb
                   and w1["rc"] == 0 and w2["rc"] == 0
                   and (json_out(w1["stdout"]) or {}).get("ok") is True
                   and (json_out(w2["stdout"]) or {}).get("ok") is True)
    battery_arms = {
        "wrong_pin_rc": wrong_pin["rc"], "wrong_pin_named": wrong_pin_named,
        "floor_rc": floor["rc"], "floor_named": floor_named,
        "work_dir_distinct": work_arm_ok,
        "work_run_rcs": [w1["rc"], w2["rc"]],
        "constant_validate_rc": val["rc"],
    }
    if wrong_pin["rc"] != 1 or not wrong_pin_named:
        failures.append(f"battery wrong-pin arm failed (rc {wrong_pin['rc']}, "
                        f"named {wrong_pin_named})")
    if floor["rc"] != 1 or not floor_named:
        failures.append(f"battery floor arm failed (rc {floor['rc']}, "
                        f"named {floor_named})")
    if not battery_arms["work_dir_distinct"]:
        failures.append("battery work_dir arms not distinct")
    if val["rc"] != 1:
        failures.append(f"constant battery receipt not rejected by --validate "
                        f"(rc {val['rc']})")
    out = {"schema": "kaidoku-r70-forged-receipts-v1", "rev": rev,
           "base_rev": base_rev, "base_probe_rev": base_probe_rev,
           "instrument": tool, "base_instrument": base_tool,
           "base_material": base_material_path,
           "landing_material": landing_material_path,
           "shapes": shapes_out, "landing_probe_shapes": landing_probe_rows,
           "genuine": genuine,
           "battery_arms": battery_arms,
           "ok": not failures, "failures": failures}
    return out


def selftest(root: str, base_rev: str, base_tool: str, work: str | None) -> int:
    """In-memory fixture cases; the wrong-world control shows the base arm can fail."""
    cases = []
    material = {"rev": "a" * 40, "instrument": {"path": "x", "sha256": "b" * 64},
                "target": 1, "carriers_matched": 1, "control_ok": True,
                "met_target": True, "failing": [],
                "carriers": [{"id": "solo", "kind": "executable", "ok": True,
                              "arms": {"detected": True, "before_ok": True,
                                       "identity_ok": True, "recovery_ok": True,
                                       "control_ok": True},
                              "before_ceiling": 10, "before_ceiling_ratio": 0.05,
                              "orig_counts": {"procedure_count": 200},
                              "packed_counts": {"procedure_count": 3}}]}
    f1 = forge(material, "F1_wrong-rev", "c" * 40)
    cases.append(("forge-f1-rev-swapped", f1["rev"] == "c" * 40
                  and material["rev"] == "a" * 40))
    f2 = forge(material, "F2_wrong-instrument", "c" * 40)
    cases.append(("forge-f2-instrument-zeroed", f2["instrument"]["sha256"] == "0" * 64))
    f10 = forge(material, "F10_absent-instrument", "c" * 40)
    cases.append(("forge-f10-instrument-absent", "instrument" not in f10))
    f8 = forge(material, "F8_dropped-arm", "c" * 40)
    cases.append(("forge-f8-arm-missing", "identity_ok" not in f8["carriers"][0]["arms"]))
    f4 = forge(material, "F4_ratio-underived", "c" * 40)
    cases.append(("forge-f4-ratio-set", f4["carriers"][0]["before_ceiling_ratio"] == 0.7
                  and material["carriers"][0]["before_ceiling_ratio"] == 0.05))
    # wrong-world negative control: a shape cut from a receipt the base reader's
    # own target rejects must FAIL the base-acceptance arm - the guard can fail.
    world4 = dict(material)
    world4["target"] = 4
    world4["carriers_matched"] = 4
    fixture_root = work or os.environ.get("TMPDIR") or tempfile.gettempdir()
    work_dir = tempfile.mkdtemp(prefix="forged-selftest-", dir=fixture_root)
    try:
        path = write_shape(work_dir, "F1_wrong-rev", world4, "c" * 40)
        reader = blob_to(root, base_rev, base_tool, work_dir, "reader.py")
        b = run([sys.executable, "-I", "-B", reader, "--check-receipt", path])
        cases.append(("wrong-world-control-fails-base-arm", b["rc"] != 0))
        registered_cases = ("forge-f1-rev-swapped", "forge-f2-instrument-zeroed",
                            "forge-f10-instrument-absent", "forge-f8-arm-missing",
                            "forge-f4-ratio-set",
                            "wrong-world-control-fails-base-arm")
        names = [n for n, _ in cases] + ["case-inventory"]
        cases.append(("case-inventory", names == list(registered_cases)
                      + ["case-inventory"]))
        failed = [name for name, ok in cases if not ok]
        print(json.dumps({"selftest": TOOL, "cases": len(cases), "failed": failed,
                          "ok": not failed}, indent=1))
        return 0 if not failed else 1
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": "forged-receipts-battery", "unevaluable": str(exc)}))
        return 2
    defects = []
    shapes = receipt.get("shapes")
    if not isinstance(shapes, list) or not shapes:
        defects.append("shapes absent or empty")
    for s in shapes or []:
        if not isinstance(s.get("shape"), str) or not s.get("declared_clause"):
            defects.append(f"{s.get('shape')}: shape or clause absent")
        if s.get("base_rc") != 0 or s.get("landing_rc") != 1:
            defects.append(f"{s.get('shape')}: rc pair not (0, 1)")
    if not isinstance(receipt.get("genuine"), dict) or not receipt.get("genuine"):
        defects.append("genuine arm absent")
    out = {"validate": "forged-receipts-battery", "path": path, "ok": not defects,
           "defects": defects, "shapes": len(shapes or [])}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not defects else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--tool")
    ap.add_argument("--base-tool")
    ap.add_argument("--probe")
    ap.add_argument("--base-probe")
    ap.add_argument("--base-probe-rev")
    ap.add_argument("--battery")
    ap.add_argument("--base-material")
    ap.add_argument("--landing-material")
    ap.add_argument("--pkg")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.validate:
        return validate(args.validate)
    if args.selftest:
        if not (args.root and args.base_rev and args.base_tool and args.work):
            print("forged-receipts: --selftest requires --root, --base-rev, "
                  "--base-tool and --work (the fixture root must be a caller-owned "
                  "scratch directory, never a platform temp default)", file=sys.stderr)
            return 2
        return selftest(args.root, args.base_rev, args.base_tool, args.work)
    need = ("--root, --rev, --base-rev, --tool, --base-tool, --probe, --base-probe, "
            "--base-probe-rev, --battery, --base-material, --landing-material, "
            "--pkg and --work are required")
    if not (args.root and args.rev and args.base_rev and args.tool and args.base_tool
            and args.probe and args.base_probe and args.base_probe_rev
            and args.battery and args.base_material and args.landing_material
            and args.pkg and args.work):
        print(f"forged-receipts: {need}", file=sys.stderr)
        return 2
    try:
        receipt = check(args.work, args.root, args.rev, args.base_rev, args.tool,
                        args.base_tool, args.probe, args.base_probe,
                        args.base_probe_rev, args.battery, args.base_material,
                        args.landing_material, args.pkg)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r70-forged-receipts-v1",
                          "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
