#!/usr/bin/env python3
"""provenance-check.py - round-69 corroboration gate (not a frozen claim counter).

The round-69 critic showed that the frozen C2 probe and C3 checker read a receipt's
fields without binding the receipt to the instrument and revision that produced it
(`.ufo/waves/round-69/w1/CriticClaims.md` §R69-C2/R69-C3: fabricated receipts pass).
The predicates themselves name "the measured run's receipt", so this gate checks that
naming directly, against the frozen instrument's OWN `CARRIERS` table read from the
measured revision:

  provenance   receipt.instrument.sha256 == --instrument-sha256, and
               receipt.instrument.rev == receipt.rev == --rev
  carriers     exactly the frozen table's ids, in table order; each source and pin
               equal to the table; each format equal to `readelf -h` of the pinned
               source; packing_mode equal to the instrument's PACKING_MODE
  ceilings     each before_ceiling equals the table's; each ratio equals
               round(ceiling/orig, 4); each packed procedure count <= its ceiling
  arms         every arm true on every carrier, control rcs nonzero
  packer       sha256/version equal the instrument's pins and pin_enforced true

It never runs the route and never writes the lane; it reads committed bytes, the
receipt and the host's inert pinned files.

Exit: 0 the receipt is the measured run's and self-consistent; 1 a named clause
fails; 2 could-not-evaluate (unknown revision, unreadable receipt, unimportable
instrument).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

UPX = "/usr/bin/upx"


class Unevaluable(Exception):
    """Exit-2 class: the gate cannot evaluate, so it claims nothing."""


def sha256_file(path: str) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_instrument(root: str, rev: str, tool: str, work: str):
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"], capture_output=True)
    if proc.returncode != 0:
        raise Unevaluable(f"git show {rev}:{tool} failed rc={proc.returncode}")
    scratch = tempfile.mkdtemp(prefix="provenance-", dir=work)
    path = os.path.join(scratch, "instrument.py")
    with open(path, "wb") as fh:
        fh.write(proc.stdout)
    spec = importlib.util.spec_from_file_location("r69_instrument", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, importlib.util


def elf_format(path: str) -> dict | None:
    proc = subprocess.run(["readelf", "-h", path], capture_output=True, text=True)
    keys = {"Class": "class", "Data": "data", "Type": "type", "Machine": "machine"}
    found = {}
    for line in (proc.stdout + proc.stderr).splitlines():
        m = re.match(r"^\s*(Class|Data|Type|Machine):\s+(.+?)\s*$", line)
        if m and keys[m.group(1)] not in found:
            found[keys[m.group(1)]] = m.group(2)
    return found if len(found) == 4 else None


def check(work: str, root: str, rev: str, tool: str, instrument_sha: str,
          receipt_path: str) -> dict:
    if not os.path.isdir(work):
        raise Unevaluable(f"--work is not a directory: {work}")
    with open(receipt_path, encoding="utf-8") as fh:
        try:
            receipt = json.load(fh)
        except json.JSONDecodeError as exc:
            raise Unevaluable(f"receipt unreadable: {exc}") from exc
    module, _ = load_instrument(root, rev, tool, work)
    carriers_table = getattr(module, "CARRIERS", None)
    packing_mode = getattr(module, "PACKING_MODE", None)
    upx_sha = getattr(module, "UPX_SHA256_PIN", None)
    upx_version = getattr(module, "UPX_VERSION_PIN", None)
    if not carriers_table or not packing_mode:
        raise Unevaluable("the frozen instrument exposes no CARRIERS/PACKING_MODE table")
    failing = []
    inst = receipt.get("instrument") or {}
    if inst.get("sha256") != instrument_sha:
        failing.append(f"instrument.sha256 {inst.get('sha256')} != {instrument_sha}")
    if receipt.get("rev") != rev:
        failing.append(f"receipt.rev {receipt.get('rev')} != {rev}")
    blob = subprocess.run(["git", "-C", root, "show", f"{rev}:{tool}"], capture_output=True)
    if blob.returncode != 0:
        failing.append(f"the instrument blob is absent at {rev}")
    else:
        import hashlib
        if hashlib.sha256(blob.stdout).hexdigest() != instrument_sha:
            failing.append("the instrument blob at the measured revision is not the pin")
    if inst.get("rev") and subprocess.run(
            ["git", "-C", root, "cat-file", "-e", f"{inst['rev']}^{{commit}}"],
            capture_output=True).returncode != 0:
        failing.append(f"instrument.rev {inst.get('rev')} is not a commit")
    claimed = receipt.get("claims") or []
    if claimed != ["R69-C1", "R69-C2", "R69-C3"]:
        failing.append(f"claims {claimed} != the declared three")
    carriers = receipt.get("carriers") or []
    if [c.get("id") for c in carriers] != [c["id"] for c in carriers_table]:
        failing.append(f"carrier ids {[c.get('id') for c in carriers]} != "
                       f"{[c['id'] for c in carriers_table]}")
    for entry in carriers_table:
        row = next((c for c in carriers if c.get("id") == entry["id"]), None)
        if row is None:
            continue
        cid = entry["id"]
        if row.get("source") != entry["source"] or row.get("pin") != entry["sha256"]:
            failing.append(f"{cid}: source/pin differ from the frozen table")
        if row.get("packing_mode") != packing_mode:
            failing.append(f"{cid}: packing_mode {row.get('packing_mode')!r} != {packing_mode!r}")
        if not os.path.exists(entry["source"]):
            failing.append(f"{cid}: pinned source absent")
            continue
        derived_format = elf_format(entry["source"])
        if row.get("format") != derived_format:
            failing.append(f"{cid}: format {row.get('format')} != readelf {derived_format}")
        orig = (row.get("orig_counts") or {}).get("procedure_count")
        packed = (row.get("packed_counts") or {}).get("procedure_count")
        ceiling = row.get("before_ceiling")
        if ceiling != entry["before_max_procedures"]:
            failing.append(f"{cid}: before_ceiling {ceiling} != {entry['before_max_procedures']}")
        if not isinstance(orig, int) or orig <= 0:
            failing.append(f"{cid}: orig procedure_count absent")
        else:
            expected_ratio = round(entry["before_max_procedures"] / orig, 4)
            if row.get("before_ceiling_ratio") != expected_ratio:
                failing.append(f"{cid}: ratio {row.get('before_ceiling_ratio')} != {expected_ratio}")
        if not isinstance(packed, int) or not isinstance(ceiling, int) or packed > ceiling:
            failing.append(f"{cid}: packed {packed} above ceiling {ceiling}")
        for arm, value in (row.get("arms") or {}).items():
            if value is not True:
                failing.append(f"{cid}:{arm} not true")
        ctrl = row.get("control") or {}
        if ctrl.get("list_rc") == 0 or ctrl.get("decompress_rc") == 0:
            failing.append(f"{cid}: control rc not negative")
    packer = receipt.get("packer") or {}
    if packer.get("pin_enforced") is not True:
        failing.append("packer.pin_enforced not true")
    if upx_sha and packer.get("sha256") != upx_sha:
        failing.append(f"packer.sha256 {packer.get('sha256')} != {upx_sha}")
    if upx_version and packer.get("version") != upx_version:
        failing.append(f"packer.version {packer.get('version')!r} != {upx_version!r}")
    if os.path.exists(UPX) and sha256_file(UPX) != upx_sha:
        failing.append("host /usr/bin/upx does not match the frozen sha256 pin")
    return {"gate": "R69-provenance", "met": not failing, "failing": failing,
            "receipt": receipt_path, "rev": rev, "instrument_sha256": instrument_sha,
            "carriers": [c.get("id") for c in carriers]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--tool", default="tools/round-69/packed-elf.py")
    ap.add_argument("--instrument-sha256", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--work", default=None)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    work = args.work or tempfile.mkdtemp(prefix="provenance-work-")
    created = args.work is None
    try:
        receipt = check(work, args.root, args.rev, args.tool, args.instrument_sha256,
                        args.receipt)
    except Unevaluable as exc:
        print(json.dumps({"gate": "R69-provenance", "unevaluable": str(exc)}), file=sys.stderr)
        return 2
    finally:
        if created:
            shutil.rmtree(work, ignore_errors=True)
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    print(text)
    return 0 if receipt["met"] else 1


if __name__ == "__main__":
    sys.exit(main())
