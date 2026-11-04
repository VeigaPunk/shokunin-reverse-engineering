#!/usr/bin/env python3
"""ExecC2's OWN A5/A6 re-derivation (never runs tools/round-69/contract-probe.py).

A5: every carrier record names identity, and the record is re-derived from the
    pinned source bytes with MY readelf parser (a different regex construction
    than the instrument's elf_format) and my own sha256.
A6: the packer pin is recorded, enforced and true of the host packer.
Plus my own clause check of R69-C3's carrier invariants (kind, ratios, pins)
because the same receipt is the A5/A6 evidence and must be internally honest.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys

UPX = "/usr/bin/upx"
PACKING_MODE = "upx --best"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def header(path):
    out = subprocess.run(["readelf", "-h", path], capture_output=True, text=True)
    text = out.stdout + out.stderr
    want = {"Class": "class", "Data": "data", "Type": "type", "Machine": "machine"}
    got = {}
    for line in text.splitlines():
        parts = line.split(":", 1)
        if len(parts) != 2:
            continue
        key = parts[0].strip()
        if key in want and want[key] not in got:
            got[want[key]] = parts[1].strip()
    return got if len(got) == 4 else None


def check(path, label):
    with open(path, encoding="utf-8") as fh:
        r = json.load(fh)
    a5, a6 = [], []
    for c in r.get("carriers") or []:
        cid = c.get("id")
        missing = [k for k in ("name", "format", "packing_mode", "pin", "source", "runs")
                   if not c.get(k)]
        if missing:
            a5.append(f"{cid}: missing {missing}")
            continue
        src = c["source"]
        d_fmt = header(src) if __import__("os").path.exists(src) else None
        d_pin = sha(src) if __import__("os").path.exists(src) else None
        argv = (c.get("runs") or {}).get("pack", {}).get("argv") or []
        pack_rc = (c.get("runs") or {}).get("pack", {}).get("rc")
        if d_pin != c["pin"]:
            a5.append(f"{cid}: pin {c['pin']} != my sha256 {d_pin}")
        if d_fmt != c["format"]:
            a5.append(f"{cid}: format {c['format']} != my readelf {d_fmt}")
        if c["packing_mode"] != PACKING_MODE:
            a5.append(f"{cid}: packing_mode {c['packing_mode']!r} != {PACKING_MODE!r}")
        if "--best" not in argv:
            a5.append(f"{cid}: --best absent from pack argv {argv}")
        if pack_rc != 0:
            a5.append(f"{cid}: pack rc {pack_rc}")
        if c.get("ok") is not True or any(v is False for v in (c.get("arms") or {}).values()):
            a5.append(f"{cid}: carrier not ok or an arm false")
    packer = r.get("packer") or {}
    host_sha = sha(UPX) if __import__("os").path.exists(UPX) else None
    hv = subprocess.run([UPX, "--version"], capture_output=True, text=True).stdout
    host_version = (hv.strip().splitlines() or [""])[0]
    for k in ("version_pin", "sha256_pin", "pin_enforced", "sha256", "version"):
        if k not in packer:
            a6.append(f"packer.{k} absent")
    if packer.get("pin_enforced") is not True:
        a6.append("packer.pin_enforced not true")
    if packer.get("sha256") != host_sha or packer.get("sha256_pin") != host_sha:
        a6.append(f"packer sha {packer.get('sha256')} / pin {packer.get('sha256_pin')} != host {host_sha}")
    if packer.get("version") != host_version or packer.get("version_pin") != host_version:
        a6.append(f"packer version {packer.get('version')} / pin {packer.get('version_pin')} != host {host_version!r}")
    # C3 clause re-derivation on the same receipt (kind, ratio, pin, fold)
    c3 = []
    target = r.get("target")
    kinds = sorted({c.get("kind") for c in r.get("carriers") or []})
    if target != 3:
        c3.append(f"target {target} != 3")
    if r.get("carriers_matched") != 3:
        c3.append(f"carriers_matched {r.get('carriers_matched')} != 3")
    if r.get("control_ok") is not True:
        c3.append("control_ok not true")
    if r.get("failing") != []:
        c3.append(f"failing {r.get('failing')}")
    for c in r.get("carriers") or []:
        ratio = c.get("before_ceiling_ratio")
        if not isinstance(ratio, (int, float)) or ratio > 0.75:
            c3.append(f"{c.get('id')}: ratio {ratio} > 0.75")
        if c.get("pin") and c.get("source") and __import__("os").path.exists(c["source"]):
            if sha(c["source"]) != c["pin"]:
                c3.append(f"{c.get('id')}: source pin drift")
    if "shared-object" not in kinds:
        c3.append(f"no shared-object: kinds {kinds}")
    seam = packer.get("upx")
    pack0 = [((c.get("runs") or {}).get("pack", {}).get("argv") or [None])[0]
             for c in r.get("carriers") or []]
    out = {"label": label, "receipt": path, "A5": {"ok": not a5, "failures": a5},
           "A6": {"ok": not a6, "failures": a6},
           "C3_clauses": {"ok": not c3, "failures": c3, "kinds": kinds},
           "packer_upx_seam": seam, "pack_argv0": pack0,
           "seam_equals_used": bool(pack0) and all(p == seam for p in pack0)}
    print(json.dumps(out, indent=1, sort_keys=True))
    return out


if __name__ == "__main__":
    outs = [check(p, l) for p, l in zip(sys.argv[1::2], sys.argv[2::2])]
    json.dump(outs, open("/fast/scratch/hyaku/kaidoku-r69/ExecC2/rederive.json", "w"), indent=1)
