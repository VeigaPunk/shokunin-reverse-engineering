#!/usr/bin/env python3
"""controls.py - round-70 do-nothing and positive controls (all three claims).

A target a do-nothing control can reach is not an improvement (fleet lesson;
kaidoku r29 C1, kake r34).  Each control below either skips the claimed work or
runs the base (round-69) instrument at the routed defect, scored so the
defect's presence is observable and the claim's target is out of reach:

  c1-base-accepts-forged    the base reader accepts an F1 wrong-rev shape cut
                            from the genuine round-69 receipt: unbound receipts
                            are the base's status quo, so "accepts receipts"
                            is never the claim
  c1-constant-battery       a fabricated battery receipt (no mutant rows) is
                            rejected by tools/round-70/mutation-check.py --validate
  c2-base-execformat-crash  the base instrument turns an exec-format-less --upx
                            into a Python traceback with exit 1 (the leak the
                            claim closes)
  c2-base-impostor-runs     the base instrument EXECUTES an impostor packer
                            (its execution log appears) before refusing it -
                            the S-1 seam, present at the base
  c2-new-refuses-unrun      the frozen instrument refuses the same impostor
                            with the sha256 clause and the log stays absent
                            (positive control for the claim's own property)
  c3-base-three-carrier     the base checker scores the round-69 receipt met
                            true at target 3 with no static-exe carrier - the
                            world the base already holds, so target 4 with a
                            static carrier is out of a do-nothing control's reach
  c3-new-rejects-old-receipt the frozen checker rejects the round-69 receipt on
                            its producer binding (instrument.sha256 clause) -
                            the binding is load-bearing, not decoration

Exit 0 when every control shows what it must show, 1 otherwise, 2 on bad argv
or an unreadable revision.  `--validate <receipt>` checks structural honesty.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/round-70/controls.py"


class Unevaluable(Exception):
    """Exit-2 class: the controls cannot be scored, so they claim nothing."""


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
            "stderr": proc.stderr[-4000:]}


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


def load(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise Unevaluable(f"material unreadable: {path}: {exc}")


def check(work: str, root: str, rev: str, base_rev: str, tool: str, base_tool: str,
          battery: str, r69_receipt: str, pkg: str) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    scratch = tempfile.mkdtemp(prefix="controls-", dir=work)
    reader = blob_to(root, rev, tool, scratch, "reader.py")
    base_reader = blob_to(root, base_rev, base_tool, scratch, "base-reader.py")
    battery_blob = blob_to(root, rev, battery, scratch, "battery.py")
    material = load(r69_receipt)
    arms = []
    failures = []

    # c1 - the base reader accepts a wrong-rev shape (the routed defect).
    c1dir = os.path.join(scratch, "c1")
    os.makedirs(c1dir)
    forged = dict(material)
    forged["rev"] = base_rev
    forged_path = os.path.join(c1dir, "c1-wrong-rev.json")
    with open(forged_path, "w", encoding="utf-8") as fh:
        json.dump(forged, fh, indent=1, sort_keys=True)
    b = run([sys.executable, "-I", "-B", base_reader, "--check-receipt", forged_path])
    bjson = json_out(b["stdout"]) or {}
    ok1 = b["rc"] == 0 and bjson.get("met") is True
    arms.append({"id": "c1-base-accepts-forged", "ok": ok1,
                 "observed": {"rc": b["rc"], "met": bjson.get("met"),
                              "receipt_rev": forged["rev"]}})
    if not ok1:
        failures.append("c1: base reader did not accept the wrong-rev shape")

    # c1 - a constant battery receipt is rejected by --validate.
    constant = os.path.join(scratch, "constant-battery.json")
    with open(constant, "w", encoding="utf-8") as fh:
        json.dump({"survivors": [], "killed": [], "mutants": [], "pristine_ok": True,
                   "ok": True, "work_dir": scratch, "target_sha256": "f" * 64}, fh)
    v = run([sys.executable, "-I", "-B", battery_blob, "--validate", constant])
    vjson = json_out(v["stdout"]) or {}
    ok2 = v["rc"] == 1 and bool(vjson.get("defects"))
    arms.append({"id": "c1-constant-battery", "ok": ok2,
                 "observed": {"rc": v["rc"], "defects": vjson.get("defects")}})
    if not ok2:
        failures.append("c1: constant battery receipt was not rejected")

    # c2 - the base instrument turns an exec-format-less --upx into a traceback.
    c2dir = tempfile.mkdtemp(prefix="c2-exec-", dir=work)
    notelf = os.path.join(c2dir, "not-an-elf")
    with open(notelf, "wb") as fh:
        fh.write(b"DEFINITELY-NOT-AN-ELF-OR-SCRIPT\x00\x01\x02\x03garbage")
    os.chmod(notelf, 0o755)
    e = run([sys.executable, "-I", "-B", base_reader, "--root", root, "--rev",
             base_rev, "--pkg", pkg, "--work", c2dir, "--upx", notelf])
    ok3 = e["rc"] == 1 and "Traceback" in e["stderr"]
    arms.append({"id": "c2-base-execformat-crash", "ok": ok3,
                 "observed": {"rc": e["rc"], "traceback": "Traceback" in e["stderr"],
                              "stderr_tail": e["stderr"][-300:]}})
    if not ok3:
        failures.append(f"c2: base exec-format leak not observed (rc {e['rc']})")

    # c2 - the base instrument executes the impostor before refusing it.
    c3dir = tempfile.mkdtemp(prefix="c2-imp-", dir=work)
    log = os.path.join(c3dir, "executed.log")
    impostor = os.path.join(c3dir, "upx-impostor")
    with open(impostor, "w", encoding="utf-8") as fh:
        fh.write(f"#!/bin/sh\necho 'upx 5.2.0'\ntouch {log}\nexit 0\n")
    os.chmod(impostor, 0o755)
    i = run([sys.executable, "-I", "-B", base_reader, "--root", root, "--rev",
             base_rev, "--pkg", pkg, "--work", c3dir, "--upx", impostor])
    ok4 = os.path.exists(log)
    arms.append({"id": "c2-base-impostor-runs", "ok": ok4,
                 "observed": {"rc": i["rc"], "impostor_executed": os.path.exists(log),
                              "clause": (json_out(i["stderr"]) or {}).get("unevaluable")}})
    if not ok4:
        failures.append("c2: base impostor-execution seam not observed")

    # c2 - the frozen instrument refuses the same impostor without running it.
    c4dir = tempfile.mkdtemp(prefix="c2-new-", dir=work)
    log2 = os.path.join(c4dir, "executed.log")
    impostor2 = os.path.join(c4dir, "upx-impostor")
    with open(impostor2, "w", encoding="utf-8") as fh:
        fh.write(f"#!/bin/sh\necho 'upx 5.2.0'\ntouch {log2}\nexit 0\n")
    os.chmod(impostor2, 0o755)
    n = run([sys.executable, "-I", "-B", reader, "--root", root, "--rev", rev,
             "--pkg", pkg, "--work", c4dir, "--upx", impostor2])
    njson = json_out(n["stdout"] + n["stderr"]) or {}
    ok5 = (n["rc"] == 2 and "sha256" in str(njson.get("unevaluable"))
           and not os.path.exists(log2))
    arms.append({"id": "c2-new-refuses-unrun", "ok": ok5,
                 "observed": {"rc": n["rc"], "clause": njson.get("unevaluable"),
                              "impostor_executed": os.path.exists(log2)}})
    if not ok5:
        failures.append(f"c2: frozen instrument did not refuse the impostor unrun "
                        f"(rc {n['rc']}, clause {njson.get('unevaluable')})")

    # c3 - the base checker's world: met true, target 3, no static carrier.
    b3 = run([sys.executable, "-I", "-B", base_reader, "--check-receipt", r69_receipt])
    b3json = json_out(b3["stdout"]) or {}
    kinds = b3json.get("kinds") or []
    ok6 = (b3["rc"] == 0 and b3json.get("met") is True
           and b3json.get("target") == 3 and "static-exe" not in kinds)
    arms.append({"id": "c3-base-three-carrier", "ok": ok6,
                 "observed": {"rc": b3["rc"], "met": b3json.get("met"),
                              "target": b3json.get("target"), "kinds": kinds}})
    if not ok6:
        failures.append("c3: base three-carrier world not observed")

    # c3 - the frozen checker rejects the round-69 receipt on its producer binding.
    l3 = run([sys.executable, "-I", "-B", reader, "--check-receipt", r69_receipt,
              "--root", root, "--rev", rev])
    l3json = json_out(l3["stdout"]) or {}
    ok7 = l3["rc"] == 1 and any("instrument.sha256" in str(f)
                                for f in l3json.get("failing") or [])
    arms.append({"id": "c3-new-rejects-old-receipt", "ok": ok7,
                 "observed": {"rc": l3["rc"],
                              "failing": (l3json.get("failing") or [])[:4]}})
    if not ok7:
        failures.append("c3: frozen checker did not reject the round-69 receipt "
                        "on the producer binding")

    out = {"schema": "kaidoku-r70-controls-v1", "rev": rev, "base_rev": base_rev,
           "instrument": tool, "base_instrument": base_tool,
           "r69_receipt": r69_receipt, "arms": arms,
           "ok": not failures, "failures": failures, "scratch": scratch}
    return out


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": "controls-receipt", "unevaluable": str(exc)}))
        return 2
    defects = []
    arms = receipt.get("arms")
    if not isinstance(arms, list) or len(arms) != 7:
        defects.append(f"arms absent or not 7 ({len(arms) if isinstance(arms, list) else 'x'})")
    for a in arms or []:
        if not isinstance(a.get("id"), str) or not isinstance(a.get("ok"), bool):
            defects.append(f"{a.get('id')}: malformed arm row")
    if receipt.get("ok") is not True and not (receipt.get("failures") or []):
        defects.append("ok false with no named failure")
    if receipt.get("ok") is True and any(a.get("ok") is not True
                                         for a in arms or []):
        defects.append("ok true over a false arm row")
    out = {"validate": "controls-receipt", "path": path, "ok": not defects,
           "defects": defects, "arms": len(arms) if isinstance(arms, list) else 0}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not defects else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--base-rev")
    ap.add_argument("--tool")
    ap.add_argument("--base-tool")
    ap.add_argument("--battery")
    ap.add_argument("--r69-receipt")
    ap.add_argument("--pkg")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.validate:
        return validate(args.validate)
    if not (args.root and args.rev and args.base_rev and args.tool and args.base_tool
            and args.battery and args.r69_receipt and args.pkg and args.work):
        print("controls: --root, --rev, --base-rev, --tool, --base-tool, --battery, "
              "--r69-receipt, --pkg and --work are required", file=sys.stderr)
        return 2
    try:
        receipt = check(args.work, args.root, args.rev, args.base_rev, args.tool,
                        args.base_tool, args.battery, args.r69_receipt, args.pkg)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r70-controls-v1",
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
