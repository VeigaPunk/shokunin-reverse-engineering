#!/usr/bin/env python3
"""contract-probe.py - round-69 instrument (R69-C2, operability, capability).

Round 68's reviewer found the route's promised contract was prose (M68-8,
ADV-2/ADV-3): a missing `node` and a refused `--work` escaped as a Python
traceback with exit 1, the packer pin was recorded but never enforced, and the
carrier records named neither format nor packing mode.  This probe drives the
instrument under test (committed bytes, black box) through six arms:

  A1 missing_node      a PATH without `node`       -> exit 2, unevaluable names node
  A2 work_unusable     an unwritable --work root   -> exit 2, unevaluable names work
  A3 packer_version    --upx <script "upx 5.1.0">  -> exit 2, packer version refused
  A4 packer_sha256     --upx <real upx + 1 byte>   -> exit 2, packer sha256 refused
  A5 carrier_record    receipt carriers name name, format, packing_mode and pin,
                       and each equals this probe's own derivation from the
                       pinned source bytes and the run's own pack argv
  A6 packer_pin        receipt `packer` carries version_pin, sha256_pin and
                       pin_enforced true, and the measured packer equals them

A5/A6 read a receipt produced by a real run (`--receipt`); the probe never
trusts a receipt the instrument did not write.

Exit: 0 all six arms pass; 1 arms failed, each named with its observation; 2
could-not-evaluate (unknown revision, missing host tool, bad argv).
`--validate <receipt>` checks a probe receipt's structural honesty (0 well
formed, 1 a named defect, 2 unreadable).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

UPX = "/usr/bin/upx"
PACKING_MODE = "upx --best"


class Unevaluable(Exception):
    """Exit-2 class: the probe cannot score, so it claims nothing."""


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def elf_format(path: str) -> dict | None:
    proc = subprocess.run(["readelf", "-h", path], capture_output=True, text=True)
    keys = {"Class": "class", "Data": "data", "Type": "type", "Machine": "machine"}
    found = {}
    for line in (proc.stdout + proc.stderr).splitlines():
        m = re.match(r"^\s*(Class|Data|Type|Machine):\s+(.+?)\s*$", line)
        if m and keys[m.group(1)] not in found:
            found[keys[m.group(1)]] = m.group(2)
    return found if len(found) == 4 else None


def parse_unevaluable(stdout: str, stderr: str) -> dict | None:
    for text in (stdout, stderr):
        for chunk in [text] + text.splitlines()[::-1]:
            chunk = chunk.strip()
            if not chunk.startswith("{"):
                continue
            try:
                payload = json.loads(chunk)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict) and "unevaluable" in payload:
                return payload
    return None


def invoke(instrument: str, root: str, rev: str, pkg: str, work: str,
           extra: list[str], path: str | None = None) -> dict:
    env = {"PATH": path or os.environ.get("PATH", "/usr/bin"),
           "HOME": os.environ.get("HOME", "/tmp"),
           "LANG": os.environ.get("LANG", "C")}
    proc = subprocess.run([sys.executable, "-I", "-B", instrument,
                           "--root", root, "--rev", rev, "--pkg", pkg,
                           "--work", work, *extra],
                          capture_output=True, text=True, timeout=900, env=env)
    return {"rc": proc.returncode,
            "unevaluable": (parse_unevaluable(proc.stdout, proc.stderr) or {}).get("unevaluable"),
            "stdout_tail": proc.stdout[-300:], "stderr_tail": proc.stderr[-300:]}


def arm(aid: str, ok: bool, observed: dict) -> dict:
    return {"id": aid, "ok": bool(ok), "observed": observed}


def arms_from_receipt(receipt_path: str | None) -> tuple[list[dict], list[dict]]:
    if not receipt_path:
        return ([arm("A5_carrier_record", False, {"missing": "no --receipt"}),
                 arm("A6_packer_pin", False, {"missing": "no --receipt"})])
    try:
        with open(receipt_path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return ([arm("A5_carrier_record", False, {"receipt_unreadable": str(exc)}),
                 arm("A6_packer_pin", False, {"receipt_unreadable": str(exc)})])
    # A5: every carrier record names its identity, and the probe re-derives it.
    failures, seen = [], []
    for c in receipt.get("carriers") or []:
        cid = c.get("id")
        missing = [k for k in ("name", "format", "packing_mode", "pin", "source", "runs")
                   if not c.get(k)]
        if missing:
            failures.append(f"{cid}: missing {missing}")
            continue
        derived_pin = sha256_file(c["source"]) if os.path.exists(c["source"]) else None
        derived_format = elf_format(c["source"])
        pack_argv = (c.get("runs") or {}).get("pack", {}).get("argv") or []
        if derived_pin != c["pin"]:
            failures.append(f"{cid}: pin {c['pin']} != source sha256 {derived_pin}")
        if derived_format != c["format"]:
            failures.append(f"{cid}: format {c['format']} != readelf {derived_format}")
        if c["packing_mode"] != PACKING_MODE or "--best" not in pack_argv:
            failures.append(f"{cid}: packing_mode {c['packing_mode']!r} "
                            f"vs pack argv {pack_argv}")
        if c.get("ok") is not True or any(v is False for v in (c.get("arms") or {}).values()):
            failures.append(f"{cid}: carrier not ok or an arm false")
        seen.append({"id": cid, "name": c["name"], "format": c["format"],
                     "packing_mode": c["packing_mode"], "pin": c["pin"]})
    if not seen and not failures:
        failures.append("no carriers in receipt")
    a5 = arm("A5_carrier_record", not failures,
             {"carriers": seen, "failures": failures})
    # A6: the pin is enforced, recorded, and true of the host packer.
    packer = receipt.get("packer") or {}
    host_sha = sha256_file(UPX) if os.path.exists(UPX) else None
    version_proc = subprocess.run([UPX, "--version"], capture_output=True, text=True) \
        if os.path.exists(UPX) else None
    host_version = (version_proc.stdout.strip().splitlines() or [""])[0] if version_proc else None
    a6_fail = []
    for key in ("version_pin", "sha256_pin", "pin_enforced", "sha256", "version"):
        if key not in packer:
            a6_fail.append(f"packer.{key} absent")
    if packer.get("pin_enforced") is not True:
        a6_fail.append("packer.pin_enforced not true")
    if packer.get("sha256_pin") != host_sha or packer.get("sha256") != host_sha:
        a6_fail.append(f"packer sha256 {packer.get('sha256')} / pin "
                       f"{packer.get('sha256_pin')} != host {host_sha}")
    if packer.get("version_pin") != host_version or packer.get("version") != host_version:
        a6_fail.append(f"packer version {packer.get('version')} / pin "
                       f"{packer.get('version_pin')} != host {host_version!r}")
    a6 = arm("A6_packer_pin", not a6_fail,
             {"packer": {k: packer.get(k) for k in
                         ("upx", "sha256", "version", "sha256_pin", "version_pin",
                          "pin_enforced")},
              "host_sha256": host_sha, "host_version": host_version, "failures": a6_fail})
    return [a5, a6]


def check(work: str, root: str, rev: str, tool: str, pkg: str,
          receipt_path: str | None) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"], capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed rc={proc.returncode}")
    scratch = os.path.join(work, "contract-probe")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    instrument = os.path.join(scratch, os.path.basename(tool))
    with open(instrument, "wb") as fh:
        fh.write(proc.stdout)
    path_bin = os.path.join(scratch, "pathbin")
    os.makedirs(path_bin)
    for tool_name in ("git", "readelf", "upx"):
        found = shutil.which(tool_name)
        if not found:
            raise Unevaluable(f"host tool absent: {tool_name}")
        os.symlink(found, os.path.join(path_bin, tool_name))
    ro = os.path.join(scratch, "ro")
    os.makedirs(ro)
    os.chmod(ro, 0o500)
    fake = os.path.join(scratch, "upx-5.1.0")
    with open(fake, "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then echo 'upx 5.1.0'; exit 0; fi\n"
                 "exit 3\n")
    os.chmod(fake, 0o755)
    bumped = os.path.join(scratch, "upx-bumped")
    with open(UPX, "rb") as src, open(bumped, "wb") as dst:
        shutil.copyfileobj(src, dst)
        dst.write(b"\0")
    os.chmod(bumped, 0o755)
    arms = []
    a1 = invoke(instrument, root, rev, pkg, work, [], path=path_bin)
    arms.append(arm("A1_missing_node",
                    a1["rc"] == 2 and "node" in str(a1["unevaluable"] or ""), a1))
    a2 = invoke(instrument, root, rev, pkg, ro, [])
    arms.append(arm("A2_work_unusable",
                    a2["rc"] == 2 and "work" in str(a2["unevaluable"] or ""), a2))
    a3 = invoke(instrument, root, rev, pkg, work, ["--upx", fake])
    arms.append(arm("A3_packer_version", a3["rc"] == 2, a3))
    a4 = invoke(instrument, root, rev, pkg, work, ["--upx", bumped])
    arms.append(arm("A4_packer_sha256",
                    a4["rc"] == 2 and "packer" in str(a4["unevaluable"] or "")
                    and "sha256" in str(a4["unevaluable"] or ""), a4))
    arms.extend(arms_from_receipt(receipt_path))
    failed = [a["id"] for a in arms if not a["ok"]]
    return {"instrument": tool, "rev": rev, "receipt": receipt_path,
            "instrument_sha256": hashlib.sha256(proc.stdout).hexdigest(),
            "arms": arms, "arms_passed": len(arms) - len(failed),
            "target": len(arms), "failed": failed, "ok": not failed}


def validate(path: str) -> int:
    try:
        with open(path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"validate": "contract-probe-receipt", "unevaluable": str(exc)}))
        return 2
    defects = []
    arms = receipt.get("arms")
    if not isinstance(arms, list) or not arms:
        defects.append("arms absent or empty")
        arms = []
    for a in arms:
        if not isinstance(a.get("id"), str):
            defects.append("an arm has no id")
        if not isinstance(a.get("ok"), bool):
            defects.append(f"{a.get('id')}: ok not a bool")
        if not isinstance(a.get("observed"), dict) or not a.get("observed"):
            defects.append(f"{a.get('id')}: no observation")
    derived = [a.get("id") for a in arms if a.get("ok") is True]
    if receipt.get("arms_passed") != len(derived):
        defects.append("arms_passed disagrees with the arm rows")
    if sorted(receipt.get("failed") or []) != sorted(
            a.get("id") for a in arms if a.get("ok") is not True):
        defects.append("failed disagrees with the arm rows")
    out = {"validate": "contract-probe-receipt", "path": path, "ok": not defects,
           "defects": defects, "arms": len(arms)}
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0 if not defects else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--tool")
    ap.add_argument("--pkg")
    ap.add_argument("--work")
    ap.add_argument("--receipt")
    ap.add_argument("--json-out")
    ap.add_argument("--validate")
    args = ap.parse_args(argv)
    if args.validate:
        return validate(args.validate)
    if not (args.root and args.rev and args.tool and args.pkg and args.work):
        print("contract-probe: --root, --rev, --tool, --pkg and --work are required",
              file=sys.stderr)
        return 2
    try:
        receipt = check(args.work, args.root, args.rev, args.tool, args.pkg, args.receipt)
    except Unevaluable as exc:
        print(json.dumps({"schema": "kaidoku-r69-contract-probe-v1",
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
