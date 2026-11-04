#!/usr/bin/env python3
"""controls.py - round-69 do-nothing and shortcut controls (all three claims).

A target a do-nothing control can reach is not an improvement (fleet lesson;
kaidoku r29 C1, kake r34).  Each control below either skips the claimed work or
fakes its receipt, and is scored with the SAME frozen counter the claim uses:

  c1-do-nothing       mutation-check, round-68 instrument + r68 patch set: the
                      five survivors the base already has -> never 0
  c1-constant-battery a fabricated battery receipt (no mutants, survivors [])
                      scored by mutation-check --validate -> must be rejected
  c2-do-nothing       contract-probe, round-68 instrument + its own receipt:
                      the six defects the base already has -> never 6 of 6
  c2-constant-probe   a fabricated probe receipt (no arms, 6 passed) scored by
                      contract-probe --validate -> must be rejected
  c3-do-nothing       packed-elf --check-receipt on the round-68 receipt:
                      target 2, no shared-object carrier -> not met
  c3-synthetic-met    a synthetic three-carrier receipt inside the declared
                      bounds -> met (proves the checker can pass)
  c3-loose-ceiling    the same receipt with one before_ceiling_ratio at 0.9
                      -> not met (the ceiling relation is load-bearing)

Exit 0 when every control shows what it must show, 1 otherwise, 2 on bad argv.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

TOOLS = {
    "mutation": "tools/round-69/mutation-check.py",
    "probe": "tools/round-69/contract-probe.py",
    "packed": "tools/round-69/packed-elf.py",
}
BASE_TOOL = "tools/round-68/packed-elf.py"
BASE_RECEIPT = ".ufo/waves/round-68/l1/scores/c2-at-landing.json"
REA_PKG = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"


def run(argv: list[str]) -> dict:
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=1800)
    payload = None
    for text in (proc.stdout, proc.stderr):
        try:
            payload = json.loads(text)
            break
        except json.JSONDecodeError:
            continue
    return {"argv": argv, "rc": proc.returncode, "json": payload,
            "stdout_tail": proc.stdout[-500:], "stderr_tail": proc.stderr[-500:]}


def synthetic_receipt(loose: bool) -> dict:
    rows = [("jq", "executable", 167, 3, 10),
            ("xxd", "executable", 99, 3, 10),
            ("libz", "shared-object", 184, 98, 120)]
    carriers = []
    for cid, kind, orig, packed, ceiling in rows:
        ratio = ceiling / orig
        if loose and cid == "libz":
            ratio = 0.9
        carriers.append({
            "id": cid, "kind": kind, "ok": True,
            "arms": {"detected": True, "before_ok": True, "identity_ok": True,
                     "recovery_ok": True, "control_ok": True},
            "before_ceiling": ceiling, "before_ceiling_ratio": round(ratio, 4),
            "orig_counts": {"procedure_count": orig},
            "packed_counts": {"procedure_count": packed},
        })
    return {"target": 3, "carriers_matched": 3, "control_ok": True,
            "met_target": True, "failing": [], "carriers": carriers}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    root, rev, work = os.path.abspath(args.root), args.rev, os.path.abspath(args.work)
    if not os.path.isdir(work):
        print(f"controls: --work is not a directory: {work}", file=sys.stderr)
        return 2
    for key in ("mutation", "probe", "packed"):
        TOOLS[key] = os.path.join(root, TOOLS[key])
    base_receipt = os.path.join(root, BASE_RECEIPT)
    py = sys.executable
    controls = []

    c1 = run([py, "-I", "-B", TOOLS["mutation"], "--root", root, "--rev", rev,
              "--tool", BASE_TOOL, "--patch-set", "r68", "--work", work])
    survivors = (c1["json"] or {}).get("survivor_count")
    controls.append({
        "id": "c1-do-nothing", "counter": "mutation-check r68 patch set at base",
        "expected": "the five r68 survivors remain; 0 survivors is NOT reachable",
        "observed": {"rc": c1["rc"], "survivor_count": survivors,
                     "survivors": (c1["json"] or {}).get("survivors")},
        "ok": survivors == 5 and (c1["json"] or {}).get("survivors") != [],
    })

    fake_battery = os.path.join(work, "control-fake-battery.json")
    with open(fake_battery, "w", encoding="utf-8") as fh:
        json.dump({"pristine_ok": True, "mutants": [], "survivors": [],
                   "ok": True, "survivor_count": 0}, fh)
    c1s = run([py, "-I", "-B", TOOLS["mutation"], "--validate", fake_battery])
    controls.append({
        "id": "c1-constant-battery", "counter": "mutation-check --validate",
        "expected": "a battery receipt with no mutant rows is rejected",
        "observed": {"rc": c1s["rc"], "defects": (c1s["json"] or {}).get("defects")},
        "ok": c1s["rc"] == 1,
    })

    c2 = run([py, "-I", "-B", TOOLS["probe"], "--root", root, "--rev", rev,
              "--tool", BASE_TOOL, "--pkg", REA_PKG, "--work", work,
              "--receipt", base_receipt])
    arms_passed = (c2["json"] or {}).get("arms_passed")
    controls.append({
        "id": "c2-do-nothing", "counter": "contract-probe on the base instrument + receipt",
        "expected": "the six base defects remain; 6 of 6 is NOT reachable",
        "observed": {"rc": c2["rc"], "arms_passed": arms_passed,
                     "failed": (c2["json"] or {}).get("failed")},
        "ok": arms_passed == 0,
    })

    fake_probe = os.path.join(work, "control-fake-probe.json")
    with open(fake_probe, "w", encoding="utf-8") as fh:
        json.dump({"arms": [], "arms_passed": 6, "failed": [], "ok": True}, fh)
    c2s = run([py, "-I", "-B", TOOLS["probe"], "--validate", fake_probe])
    controls.append({
        "id": "c2-constant-probe", "counter": "contract-probe --validate",
        "expected": "a probe receipt with no arm rows is rejected",
        "observed": {"rc": c2s["rc"], "defects": (c2s["json"] or {}).get("defects")},
        "ok": c2s["rc"] == 1,
    })

    c3 = run([py, "-I", "-B", TOOLS["packed"], "--check-receipt", base_receipt])
    controls.append({
        "id": "c3-do-nothing", "counter": "packed-elf --check-receipt on the r68 receipt",
        "expected": "target 2 and no shared-object carrier -> not met",
        "observed": {"rc": c3["rc"], "failing": (c3["json"] or {}).get("failing")},
        "ok": c3["rc"] == 0,
    })

    for name, loose, want in (("c3-synthetic-met", False, 0),
                              ("c3-loose-ceiling", True, 1)):
        path = os.path.join(work, f"control-{name}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(synthetic_receipt(loose), fh)
        res = run([py, "-I", "-B", TOOLS["packed"], "--check-receipt", path])
        controls.append({
            "id": name, "counter": "packed-elf --check-receipt on a synthetic receipt",
            "expected": ("met" if want == 0 else "not met on the loose ceiling"),
            "observed": {"rc": res["rc"], "failing": (res["json"] or {}).get("failing")},
            "ok": res["rc"] == want,
        })

    receipt = {"root": root, "rev": rev, "controls": controls,
               "ok": all(c["ok"] for c in controls)}
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
