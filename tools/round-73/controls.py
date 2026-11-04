#!/usr/bin/env python3
"""controls.py - round-73 instrument (do-nothing controls for R73-C1..C3).

Frozen before any claim data (QUALITY #33).  Each arm takes the cheapest route
that SKIPS the round's claimed work and scores it with the claim's own counter.

  c1_no_kernel_channel   the round-72 seam probe at the declaration revision
                         has eleven arms and no A12 at all: the base world the
                         round-73 probe must move is 11 of 11 with no kernel
                         channel, so A12's arrival is the round's work.
  c1_blind_witness       the round-73 `a12_verdict` fed a forged run whose
                         kernel samples are forced clean, and one whose
                         child-side dumps are dirty: both must return ok false,
                         so the arm cannot pass on a blind witness or on a
                         world where there is no lie to catch.
  c2_do_nothing          the record audit at the base revision reports six
                         mismatches; a control that agrees with the base world
                         would mean the atoms do not bind the routed defects.
  c2_lying_receipt       an audit receipt whose atom rows all say `ok true`
                         while `mismatch_count` says 6 is rejected by the
                         audit's own `--validate` (derived-count agreement).
  c3_base_world          the three reader defects applied to the round-72
                         route bytes survive (`--patch-set r73base`, survivors
                         3): the do-nothing world the round-73 route must beat.
  c3_no_case             the round-73 route with the three new cases dropped
                         from its registry fails its own selftest naming
                         `case-inventory`, so the registry binding is
                         load-bearing and a silently dropped case cannot
                         shrink the surface.

Exit: 0 every control met its declared expectation; 1 a control did not; 2
could-not-evaluate.  Writes one JSON receipt; all scratch lives under --work.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

PROBE72 = "tools/round-72/seam-probe.py"
PROBE73 = "tools/round-73/seam-probe.py"
ROUTE72 = "tools/round-72/packed-elf.py"
ROUTE73 = "tools/round-73/packed-elf.py"
BATTERY = "tools/round-73/mutation-check.py"
AUDIT = "tools/round-73/record-audit.py"
NEW_CASES = ("git-reader-allowlisted-exec", "checker-readelf-allowlisted-exec",
             "implicit-capsule-polluted-raw-log")
REA_PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"


def run(argv: list[str], timeout: int = 2400) -> dict:
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    payload = None
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        for chunk in reversed(proc.stdout.splitlines()):
            chunk = chunk.strip()
            if chunk.startswith("{"):
                try:
                    payload = json.loads(chunk)
                    break
                except json.JSONDecodeError:
                    continue
    return {"rc": proc.returncode, "json": payload,
            "stdout_tail": proc.stdout[-1200:], "stderr_tail": proc.stderr[-1200:]}


def load_module(path: str):
    spec = importlib.util.spec_from_file_location(
        "k73_" + os.path.basename(path).replace("-", "_").replace(".", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--base-rev", required=True)
    ap.add_argument("--decl-rev", required=True)
    ap.add_argument("--receipt-rev")
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--commitment", required=True)
    ap.add_argument("--expect-upx", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    if not os.path.isdir(args.work):
        print(json.dumps({"unevaluable": f"--work is not a directory: {args.work}"}),
              file=sys.stderr)
        return 2
    scratch = tempfile.mkdtemp(prefix="controls-", dir=args.work)
    lane = lambda p: os.path.join(root, p)
    needed = [lane(PROBE72), lane(PROBE73), lane(ROUTE72), lane(ROUTE73),
              lane(BATTERY), lane(AUDIT), os.path.abspath(args.receipt),
              os.path.abspath(args.expect_upx)]
    missing = [p for p in needed if not os.path.exists(p)]
    if missing:
        print(json.dumps({"unevaluable": f"missing input: {missing}"}),
              file=sys.stderr)
        return 2
    arms = {}

    # c1_no_kernel_channel
    res = run([sys.executable, "-I", "-B", lane(PROBE72), "--root", root,
               "--rev", args.decl_rev,
               *(["--receipt-rev", args.receipt_rev] if args.receipt_rev else []),
               "--tool", ROUTE73, "--battery", BATTERY, "--pkg", REA_PKG,
               "--work", scratch, "--receipt", args.receipt,
               "--nonce-commitment", args.commitment,
               "--expect-upx", os.path.abspath(args.expect_upx)])
    payload = res["json"] or {}
    ids = [a.get("id") for a in payload.get("arms") or []]
    arms["c1_no_kernel_channel"] = {
        "rc": res["rc"], "target": payload.get("target"),
        "arms_passed": payload.get("arms_passed"), "arm_ids": ids,
        "met": (payload.get("target") == 11 and "A12_kernel_witness" not in ids
                and res["rc"] == 0)}

    # c1_blind_witness
    probe = load_module(lane(PROBE73))
    allow = probe.CHILD_ENV_KEYS
    clean = {"keys": sorted(allow), "canary_present": False,
             "home_under": True, "tmpdir_under": True}
    dirty = {"keys": sorted(allow) + ["KAIDOKU_ENV_CANARY"],
             "canary_present": True, "home_under": False, "tmpdir_under": False}
    genuine = {"rc": 0, "kernel": {"git": clean, "readelf": clean}}
    forged_clean = {"kernel": {"git": clean, "readelf": clean},
                    "shims": {"git": {**clean, "keys_exact": True},
                              "readelf": {**clean, "keys_exact": True}}}
    forged_dirty = {"kernel": {"git": dirty, "readelf": dirty},
                    "shims": {"git": {**clean, "keys_exact": True},
                              "readelf": {**clean, "keys_exact": True}}}
    dirty_shims = {"kernel": {"git": dirty, "readelf": dirty},
                   "shims": {"git": dirty, "readelf": dirty}}
    blind = probe.a12_verdict(genuine, forged_clean, allow)
    honest = probe.a12_verdict(genuine, forged_dirty, allow)
    no_lie = probe.a12_verdict(genuine, dirty_shims, allow)
    arms["c1_blind_witness"] = {
        "blind_ok": blind["ok"], "blind_detected": blind["forged_detected"],
        "honest_ok": honest["ok"], "no_lie_ok": no_lie["ok"],
        "met": (blind["ok"] is False and blind["forged_detected"] is False
                and honest["ok"] is True and no_lie["ok"] is False)}

    # c2_do_nothing
    res = run([sys.executable, "-I", "-B", lane(AUDIT), "--root", root,
               "--rev", args.base_rev])
    payload = res["json"] or {}
    arms["c2_do_nothing"] = {
        "rc": res["rc"], "mismatch_count": payload.get("mismatch_count"),
        "mismatches": payload.get("mismatches"),
        "met": (res["rc"] == 1 and payload.get("mismatch_count") == 6
                and payload.get("mismatches") == [
                    "D1_c2_evidence_hash", "D2_c2_pin_conjunct",
                    "D3_record_gate_disclosures", "D4_c3_exit_code",
                    "D5_provenance_trio_open", "D6_nudge_rationale"])}

    # c2_lying_receipt
    lying = os.path.join(scratch, "audit-lying.json")
    atoms = [{"id": f"D{i}", "ok": True, "detail": "claimed"}
             for i in range(1, 8)]
    with open(lying, "w", encoding="utf-8") as fh:
        json.dump({"atoms": atoms, "mismatches": ["D1", "D2", "D3", "D4", "D5", "D6"],
                   "mismatch_count": 6, "ok": True}, fh)
    res = run([sys.executable, "-I", "-B", lane(AUDIT), "--validate", lying])
    payload = res["json"] or {}
    arms["c2_lying_receipt"] = {
        "rc": res["rc"], "defects": payload.get("defects"),
        "met": res["rc"] == 1 and bool(payload.get("defects"))}

    # c3_base_world
    res = run([sys.executable, "-I", "-B", lane(BATTERY), "--root", root,
               "--rev", args.base_rev, "--tool", ROUTE72,
               "--patch-set", "r73base", "--work", scratch])
    payload = res["json"] or {}
    arms["c3_base_world"] = {
        "rc": res["rc"], "survivors": payload.get("survivors"),
        "survivor_count": payload.get("survivor_count"),
        "expected_survivors": payload.get("expected_survivors"),
        "met": (res["rc"] == 0 and payload.get("survivor_count") == 3
                and payload.get("survivors") == list(
                    ("git_reader_env_dropped", "readelf_env_dropped",
                     "implicit_capsule_dropped")))}

    # c3_no_case
    with open(lane(ROUTE73), encoding="utf-8") as fh:
        text = fh.read()
    stripped = text
    for name in NEW_CASES:
        stripped = stripped.replace(f'    "{name}",\n', "")
    if stripped == text:
        print(json.dumps({"unevaluable": "c3_no_case could not drop a case"}),
              file=sys.stderr)
        return 2
    no_case = os.path.join(scratch, "route-no-case.py")
    with open(no_case, "w", encoding="utf-8") as fh:
        fh.write(stripped)
    shutil.copy(lane("tools/round-73/capsule_audit.py"),
                os.path.join(scratch, "capsule_audit.py"))
    res = run([sys.executable, "-I", "-B", no_case, "--selftest",
               "--work", scratch])
    payload = res["json"] or {}
    arms["c3_no_case"] = {
        "rc": res["rc"], "failed": payload.get("failed"),
        "cases": payload.get("cases"),
        "stdout_tail": res["stdout_tail"][-400:],
        "stderr_tail": res["stderr_tail"][-400:],
        "met": (res["rc"] == 1
                and "case-inventory" in (payload.get("failed") or []))}

    ok = all(a.get("met") is True for a in arms.values())
    out = {"instrument": "tools/round-73/controls.py",
           "base_rev": args.base_rev, "decl_rev": args.decl_rev,
           "receipt": args.receipt, "commitment": args.commitment,
           "work_dir": scratch, "arms": arms, "ok": ok}
    text_out = json.dumps(out, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text_out + "\n")
    print(text_out)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
