#!/usr/bin/env python3
"""contract-probe.py - round-70 instrument (R70-C1 corroboration; the R69-C2
probe, hardened).

Round 68's reviewer found the route's promised contract was prose (M68-8,
ADV-2/ADV-3): a missing `node` and a refused `--work` escaped as a Python
traceback with exit 1, the packer pin was recorded but never enforced, and the
carrier records named neither format nor packing mode.  Round 69 froze this
probe; round 70 closes the routed M69-8 counter defect: A5/A6 no longer trust
the receipt's word but bind it to its producer (QUALITY #114 executed by the
corroborating reader too) - the receipt's recorded revision must equal --rev,
its recorded instrument hash must equal the blob of the instrument at that
revision, and every carrier row is re-derived from the instrument's own frozen
CARRIERS/DECLARED_ORIG tables (id, pin, source, kind, ceiling, original
procedure count, the ceiling/orig ratio relation, packed <= ceiling), from
`readelf -h` of the pinned source, and from the run's own pack argv.  The
harness child's HOME lives inside --work (never a /tmp fallback) and every
scratch root is a per-run mkdtemp.  Six arms against the instrument under test
(committed bytes, black box):

  A1 missing_node      a PATH without `node`       -> exit 2, unevaluable names node
  A2 work_unusable     an unwritable --work root   -> exit 2, unevaluable names work
  A3 packer_identity   --upx <impostor script>     -> exit 2, the packer pin refuses it
                       (the version clause on a pre-hash-first instrument, the
                       sha256 clause on a hash-first one, impostor in both cases)
  A4 packer_sha256     --upx <real upx + 1 byte>   -> exit 2, packer sha256 refused
  A5 carrier_record    receipt carriers bound to the frozen tables and re-derived
                       (identity, format, mode, counts, ratio, arms)
  A6 packer_pin        receipt `packer` pins equal the host packer, and the
                       receipt is bound to its producer (rev + instrument hash)

A5/A6 read a receipt produced by a real run (`--receipt`); a receipt whose
producer fields do not match the invoked bytes fails both arms with the named
clause, so a fabricated receipt that merely asserts green fields cannot pass.

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
import tempfile

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
           extra: list[str], path: str | None = None, home: str | None = None) -> dict:
    # No /tmp fallback (round-69 M69-11): the harness child's HOME lives inside
    # --work, or is omitted entirely when the caller is probing that behavior.
    env = {"PATH": path or os.environ.get("PATH", "/usr/bin"),
           "LANG": os.environ.get("LANG", "C")}
    if home is not None:
        env["HOME"] = home
    proc = subprocess.run([sys.executable, "-I", "-B", instrument,
                           "--root", root, "--rev", rev, "--pkg", pkg,
                           "--work", work, *extra],
                          capture_output=True, text=True, timeout=900, env=env)
    return {"rc": proc.returncode, "env_keys": sorted(env),
            "unevaluable": (parse_unevaluable(proc.stdout, proc.stderr) or {}).get("unevaluable"),
            "stdout_tail": proc.stdout[-300:], "stderr_tail": proc.stderr[-300:]}


def arm(aid: str, ok: bool, observed: dict) -> dict:
    return {"id": aid, "ok": bool(ok), "observed": observed}


def load_registry(blob_path: str):
    """Import the frozen instrument module (constants only run at import)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("r70_instrument_under_probe", blob_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def arms_from_receipt(receipt_path: str | None, root: str, rev: str, tool: str,
                      blob_path: str) -> tuple[list[dict], list[dict], dict]:
    if not receipt_path:
        return ([arm("A5_carrier_record", False, {"missing": "no --receipt"}),
                 arm("A6_packer_pin", False, {"missing": "no --receipt"})], {}, {})
    try:
        with open(receipt_path, encoding="utf-8") as fh:
            receipt = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        return ([arm("A5_carrier_record", False, {"receipt_unreadable": str(exc)}),
                 arm("A6_packer_pin", False, {"receipt_unreadable": str(exc)})], {}, {})
    mod = load_registry(blob_path)
    registry = {c["id"]: c for c in mod.CARRIERS}
    declared_orig = dict(getattr(mod, "DECLARED_ORIG", {}))
    # Producer binding (QUALITY #114): the receipt is only scoreable when its
    # recorded revision equals --rev and its recorded instrument hash equals
    # the blob of the instrument at that revision.
    producer_fail = []
    blob_sha = None
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"],
                          capture_output=True)
    if proc.returncode != 0:
        producer_fail.append(f"git show {rev}:{tool} failed rc={proc.returncode}")
    else:
        blob_sha = hashlib.sha256(proc.stdout).hexdigest()
    instrument = receipt.get("instrument")
    if not isinstance(instrument, dict) or not instrument:
        producer_fail.append("receipt.instrument absent")
    else:
        if instrument.get("path") != tool:
            producer_fail.append(f"instrument.path {instrument.get('path')} != {tool}")
        if blob_sha is not None and instrument.get("sha256") != blob_sha:
            producer_fail.append(f"instrument.sha256 {instrument.get('sha256')} != "
                                 f"blob at {rev}")
    if receipt.get("rev") != rev:
        producer_fail.append(f"receipt.rev {receipt.get('rev')} != {rev}")
    # A5: every carrier record is bound to the frozen table and re-derived.
    failures, seen = [], []
    for c in receipt.get("carriers") or []:
        cid = c.get("id")
        row = registry.get(cid)
        if row is None:
            failures.append(f"{cid}: not in the frozen carrier table")
            continue
        missing = [k for k in ("name", "format", "packing_mode", "pin", "source", "runs")
                   if not c.get(k)]
        if missing:
            failures.append(f"{cid}: missing {missing}")
            continue
        derived_pin = sha256_file(c["source"]) if os.path.exists(c["source"]) else None
        derived_format = elf_format(c["source"])
        pack_argv = (c.get("runs") or {}).get("pack", {}).get("argv") or []
        if c["pin"] != row["sha256"]:
            failures.append(f"{cid}: pin {c['pin']} != frozen table {row['sha256']}")
        elif derived_pin != c["pin"]:
            failures.append(f"{cid}: pin {c['pin']} != source sha256 {derived_pin}")
        if c["source"] != row["source"]:
            failures.append(f"{cid}: source {c['source']} != frozen table {row['source']}")
        if c.get("kind") != row["kind"]:
            failures.append(f"{cid}: kind {c.get('kind')} != frozen table {row['kind']}")
        if derived_format != c["format"]:
            failures.append(f"{cid}: format {c['format']} != readelf {derived_format}")
        if c["packing_mode"] != mod.PACKING_MODE or "--best" not in pack_argv:
            failures.append(f"{cid}: packing_mode {c['packing_mode']!r} "
                            f"vs pack argv {pack_argv}")
        if c.get("ok") is not True or any(v is not True for v in (c.get("arms") or {}).values()):
            failures.append(f"{cid}: carrier not ok or an arm not true")
        if c.get("before_ceiling") != row["before_max_procedures"]:
            failures.append(f"{cid}: ceiling {c.get('before_ceiling')} != frozen table "
                            f"{row['before_max_procedures']}")
        orig_counts = c.get("orig_counts") or {}
        packed_counts = c.get("packed_counts") or {}
        orig_proc = orig_counts.get("procedure_count")
        packed_proc = packed_counts.get("procedure_count")
        if cid in declared_orig and orig_proc != declared_orig[cid]:
            failures.append(f"{cid}: orig_procedures {orig_proc} != declared "
                            f"{declared_orig[cid]}")
        if isinstance(packed_proc, int) and packed_proc > row["before_max_procedures"]:
            failures.append(f"{cid}: packed {packed_proc} > ceiling "
                            f"{row['before_max_procedures']}")
        ratio = c.get("before_ceiling_ratio")
        if isinstance(orig_proc, int) and isinstance(ratio, (int, float)) \
                and orig_proc > 0:
            want = round(row["before_max_procedures"] / orig_proc, 4)
            if ratio != want:
                failures.append(f"{cid}: before_ceiling_ratio {ratio} != "
                                f"ceiling/orig {want}")
        seen.append({"id": cid, "name": c["name"], "format": c["format"],
                     "packing_mode": c["packing_mode"], "pin": c["pin"]})
    if len((receipt.get("carriers") or [])) != len(registry):
        failures.append(f"carrier rows {len(receipt.get('carriers') or [])} != "
                        f"frozen table {len(registry)}")
    if sorted(x.get("id") for x in receipt.get("carriers") or []
              if isinstance(x, dict)) != sorted(registry):
        failures.append("carrier ids do not match the frozen table")
    if not seen and not failures:
        failures.append("no carriers in receipt")
    a5 = arm("A5_carrier_record", not failures and not producer_fail,
             {"carriers": seen, "failures": failures, "producer": producer_fail})
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
    a6_fail.extend(producer_fail)
    a6 = arm("A6_packer_pin", not a6_fail,
             {"packer": {k: packer.get(k) for k in
                         ("upx", "sha256", "version", "sha256_pin", "version_pin",
                          "pin_enforced")},
              "host_sha256": host_sha, "host_version": host_version, "failures": a6_fail})
    meta = {"registry_ids": sorted(registry), "declared_orig": declared_orig,
            "blob_sha256": blob_sha}
    return [a5, a6], meta, {"producer_fail": producer_fail}


def check(work: str, root: str, rev: str, tool: str, pkg: str,
          receipt_path: str | None) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"], capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed rc={proc.returncode}")
    scratch = tempfile.mkdtemp(prefix="contract-probe-", dir=work)
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
    fake = os.path.join(scratch, "upx-impostor")
    with open(fake, "w", encoding="utf-8") as fh:
        fh.write("#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then echo 'upx 5.2.0'; exit 0; fi\n"
                 "echo 'upx 5.1.0'; exit 3\n")
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
    clause = str(a3["unevaluable"] or "")
    arms.append(arm("A3_packer_identity",
                    a3["rc"] == 2 and "packer" in clause
                    and ("version" in clause or "sha256" in clause), a3))
    a4 = invoke(instrument, root, rev, pkg, work, ["--upx", bumped])
    arms.append(arm("A4_packer_sha256",
                    a4["rc"] == 2 and "packer" in str(a4["unevaluable"] or "")
                    and "sha256" in str(a4["unevaluable"] or ""), a4))
    receipt_arms, registry_meta, producer_meta = arms_from_receipt(
        receipt_path, root, rev, tool, instrument)
    arms.extend(receipt_arms)
    failed = [a["id"] for a in arms if not a["ok"]]
    return {"instrument": tool, "rev": rev, "receipt": receipt_path,
            "instrument_sha256": hashlib.sha256(proc.stdout).hexdigest(),
            "registry": registry_meta,
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
        print(json.dumps({"schema": "kaidoku-r70-contract-probe-v1",
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
