#!/usr/bin/env python3
"""controls.py - round-72 instrument (do-nothing controls for R72-C1..C3).

Frozen before any claim data (QUALITY #33).  Each arm takes the cheapest route
that SKIPS the round's claimed work and scores it with the claim's own counter:

  c1_base_world       the round-72 seam probe, run at the declaration revision
                      but pointed at the round-71 route (`--tool
                      tools/round-71/packed-elf.py`), scores 9 of 11 arms:
                      A10 is fail-closed without the checker's clauses and A11
                      observes the inherited caller environment.  If either
                      base arm came back true, the arm or target would be
                      wrong.
  c2_base_survivor    the A10 self-mutant applied by the frozen battery to the
                      round-71 probe with patch set r71 SURVIVES (survivor
                      count 1): the do-nothing world the round-72 probe must
                      beat with 0 survivors.
  c3_base_accepts     the round-71 receipt checker accepts the round-71 route
                      receipt whose `child_env_observed` summary lies about a
                      polluted capsule (rc 0, met true), while the round-72
                      capsule audit rejects the same pair naming `canary`.
  c1_constant_probe   an all-true arms receipt with empty observations is
                      rejected by the probe's `--validate`.
  c2_constant_survivors
                      a mutation receipt that claims zero survivors while a
                      mutant row reads `survived` is rejected by `--validate`.

Exit: 0 every control met its declared expectation; 1 a control did not; 2
could-not-evaluate.  Writes one JSON receipt; all scratch lives under --work.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

PROBE = "tools/round-72/seam-probe.py"
ROUTE72 = "tools/round-72/packed-elf.py"
ROUTE71 = "tools/round-71/packed-elf.py"
PROBE71 = "tools/round-71/seam-probe.py"
BATTERY = "tools/round-72/mutation-check.py"
AUDIT = "tools/round-72/capsule-audit.py"
CAPSULE = ".ufo/waves/round-71/l1/scores/c1-env-at-landing.jsonl"
AUDITJSON = ".ufo/waves/round-71/l1/scores/c1-env-audit.json"


def run(argv: list[str], timeout: int = 2400) -> dict:
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    payload = None
    text = proc.stdout.strip()
    if text.startswith("{"):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None
    if payload is None:
        for chunk in reversed(proc.stdout.splitlines()):
            chunk = chunk.strip()
            if not chunk.startswith("{"):
                continue
            try:
                payload = json.loads(chunk)
                break
            except json.JSONDecodeError:
                continue
    return {"rc": proc.returncode, "json": payload,
            "stdout_tail": proc.stdout[-1500:], "stderr_tail": proc.stderr[-1500:]}


def rebase(receipt_path: str, log_path: str, out: str) -> dict:
    with open(receipt_path, encoding="utf-8") as fh:
        receipt = json.load(fh)
    receipt.setdefault("child_env_observed", {})["log"] = log_path
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return receipt


def polluted_capsule(genuine: str, out: str) -> int:
    """Copy the genuine capsule and add one record carrying the canary key."""
    with open(genuine, "rb") as fh:
        lines = [line for line in fh.read().split(b"\n") if line.strip()]
    record = json.loads(lines[0].decode("utf-8"))
    env = dict(record.get("env") or {})
    env["KAIDOKU_ENV_CANARY"] = "control-canary"
    record["env"] = env
    record["argv"] = ["/usr/bin/upx", "--version"]
    with open(out, "wb") as fh:
        fh.write(b"\n".join(lines + [json.dumps(record, sort_keys=True).encode()]) + b"\n")
    return len(lines) + 1


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
    capsule = lane(CAPSULE)
    audit_json = lane(AUDITJSON)
    scripts = [lane(PROBE), lane(ROUTE72), lane(ROUTE71), lane(PROBE71),
               lane(BATTERY), lane(AUDIT)]
    missing = [p for p in scripts + [capsule, audit_json, args.receipt] if not os.path.exists(p)]
    if missing:
        print(json.dumps({"unevaluable": f"missing input: {missing}"}), file=sys.stderr)
        return 2
    upx = os.path.abspath(args.expect_upx)
    if not os.path.isfile(upx):
        print(json.dumps({"unevaluable": f"--expect-upx absent: {upx}"}), file=sys.stderr)
        return 2
    rebased = os.path.join(scratch, "receipt-rebased.json")
    rebase(args.receipt, capsule, rebased)
    polluted = os.path.join(scratch, "capsule-polluted.jsonl")
    records = polluted_capsule(capsule, polluted)
    lying = os.path.join(scratch, "receipt-lying.json")
    rebase(args.receipt, polluted, lying)
    arms = {}

    # c1_base_world
    res = run([sys.executable, "-I", "-B", lane(PROBE), "--root", root,
               "--rev", args.decl_rev,
               *(["--receipt-rev", args.receipt_rev] if args.receipt_rev else []),
               "--tool", ROUTE71,
               "--battery", "tools/round-70/mutation-check.py",
               "--pkg", REA_PKG, "--work", scratch,
               "--receipt", rebased, "--nonce-commitment", args.commitment,
               "--expect-upx", upx])
    payload = res["json"] or {}
    arms["c1_base_world"] = {
        "rc": res["rc"], "arms_passed": payload.get("arms_passed"),
        "target": payload.get("target"), "failed": payload.get("failed"),
        "a11": next((a for a in payload.get("arms") or []
                     if a.get("id") == "A11_checker_env"), None),
        "a10": next((a for a in payload.get("arms") or []
                     if a.get("id") == "A10_run_binding"), None),
        "met": (res["rc"] == 1 and payload.get("arms_passed") == 9
                and payload.get("target") == 11
                and sorted(payload.get("failed") or []) ==
                ["A10_run_binding", "A11_checker_env"])}

    # c2_base_survivor
    res = run([sys.executable, "-I", "-B", lane(BATTERY), "--root", root,
               "--rev", args.base_rev, "--tool", PROBE71,
               "--patch-set", "r71", "--work", scratch])
    payload = res["json"] or {}
    arms["c2_base_survivor"] = {
        "rc": res["rc"], "survivors": payload.get("survivors"),
        "survivor_count": payload.get("survivor_count"),
        "expected_survivors": payload.get("expected_survivors"),
        "met": (res["rc"] == 0 and payload.get("survivor_count") == 1
                and payload.get("survivors") == ["A10_binding_force_true"])}

    # c3_base_accepts (the round-71 checker at the declaration rev, so the
    # receipt's producer binding matches its own bytes)
    res = run([sys.executable, "-I", "-B", lane(ROUTE71), "--root", root,
               "--rev", args.decl_rev, "--check-receipt", lying,
               "--nonce-commitment", args.commitment])
    payload = res["json"] or {}
    audit = run([sys.executable, "-I", "-B", lane(AUDIT), "--capsule", polluted,
                 "--audit", audit_json])
    audit_payload = audit["json"] or {}
    arms["c3_base_accepts"] = {
        "checker_rc": res["rc"], "met": payload.get("met"),
        "failing": payload.get("failing"),
        "has_capsule_clause": "clauses" in payload,
        "audit_rc": audit["rc"], "audit_ok": audit_payload.get("ok"),
        "audit_failures": audit_payload.get("failures"),
        "polluted_records": records,
        "met_control": (res["rc"] == 0 and payload.get("met") is True
                        and payload.get("failing") == []
                        and "clauses" not in payload
                        and audit["rc"] == 1 and audit_payload.get("ok") is False
                        and "canary" in (audit_payload.get("failures") or []))}

    # c1_constant_probe
    constant = os.path.join(scratch, "constant-probe.json")
    with open(constant, "w", encoding="utf-8") as fh:
        json.dump({"arms": [{"id": f"A{i}", "ok": True, "observed": {}}
                            for i in range(1, 12)],
                   "arms_passed": 11, "target": 11, "failed": []}, fh)
    res = run([sys.executable, "-I", "-B", lane(PROBE), "--validate", constant])
    arms["c1_constant_probe"] = {
        "rc": res["rc"], "ok": (res["json"] or {}).get("ok"),
        "defects": (res["json"] or {}).get("defects"),
        "met": res["rc"] == 1 and (res["json"] or {}).get("ok") is False}

    # c2_constant_survivors
    constant = os.path.join(scratch, "constant-mutation.json")
    with open(constant, "w", encoding="utf-8") as fh:
        json.dump({"pristine_ok": True,
                   "target_sha256": "aa" * 32, "work_dir": scratch,
                   "mutants": [{"id": "M", "rc": 0, "failed": [],
                                "applied": True, "verdict": "survived"}],
                   "survivors": []}, fh)
    res = run([sys.executable, "-I", "-B", lane(BATTERY), "--validate", constant])
    arms["c2_constant_survivors"] = {
        "rc": res["rc"], "ok": (res["json"] or {}).get("ok"),
        "defects": (res["json"] or {}).get("defects"),
        "met": res["rc"] == 1 and (res["json"] or {}).get("ok") is False}

    # The c3 arm carries two verdicts: `met` is the base checker's acceptance
    # (true by design) and `met_control` is the full arm (checker accepts AND
    # the audit rejects).  Only the strict one may gate the control
    # (round-72 ReviewerGates).
    ok = all((a.get("met_control") if "met_control" in a else a.get("met")) is True
             for a in arms.values())
    out = {"instrument": "tools/round-72/controls.py",
           "base_rev": args.base_rev, "decl_rev": args.decl_rev,
           "receipt": args.receipt, "commitment": args.commitment,
           "capsule": capsule, "polluted_capsule_records": records,
           "work_dir": scratch, "arms": arms, "ok": ok}
    text = json.dumps(out, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if ok else 1


REA_PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"

if __name__ == "__main__":
    sys.exit(main())
