#!/usr/bin/env python3
"""field-tamper-matrix.py - round-88 instrument (R88-C2, depth).

`upx -t` answers a different typed refusal for every field a tamperer can
reach in a packed UPX 5.2.0 little-endian ELF, and tolerates some fields
entirely.  This instrument measures that matrix instead of asserting it:
four sha256-pinned carriers x seventeen single-field tampers, each cell
recording `upx -t` exit, the message class UPX itself prints, `upx -d` exit
and whether the unpacked bytes still equal the carrier pin.

Message classes (closed vocabulary, parsed from UPX's own last line):
  header-corrupted          "header corrupted"
  p-info-corrupted          "p_info corrupted"
  b-info-corrupt-field      "corrupt b_info"      (l_info.p_blocksize)
  b-info-corrupted          "b_info corrupted"    (a b_info field)
  compressed-data-violation "compressed data violation"
  tolerated                 `upx -t` exits 0
  other-refusal             non-zero exit, no recognised message

Offsets come from the round-87 module's own locators on the *packed* file
(`find_packheader` -> validated PackHeader; `find_linfo` -> the l_info whose
chain reaches the end-of-chain sentinel; block 0 = l_info + 20).  Every tamper
writes into a private copy; the carriers are never modified.

Exit: 0 matrix complete and fully classified; 1 unclassified or short cells;
2 could-not-evaluate (pin drift, missing tool, bad argv, refused --work).

--selftest runs the classifier and the table on in-memory strings.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile

TOOL = "tools/round-88/field-tamper-matrix.py"
UPX_VERSION_PIN = "upx 5.2.0"
UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
R87_REPAIR = "tools/round-87/upx-magic-repair.py"
CARRIERS = [
    {"id": "jq", "source": "/usr/bin/jq",
     "sha256": "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"},
    {"id": "xxd", "source": "/usr/bin/xxd",
     "sha256": "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"},
    {"id": "libz", "source": "/usr/lib/libz.so.1.3.2",
     "sha256": "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9"},
    {"id": "dinit", "source": "/usr/bin/docker-init",
     "sha256": "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115"},
]
# (field, anchor, byte offset inside the anchor, width)
FIELDS = [
    ("ph-checksum", "ph", 31, 1),
    ("ph-u_adler", "ph", 8, 4),
    ("ph-c_adler", "ph", 12, 4),
    ("ph-u_len", "ph", 16, 4),
    ("ph-c_len", "ph", 20, 4),
    ("ph-u_file_size", "ph", 24, 4),
    ("ph-method", "ph", 6, 1),
    ("ph-level", "ph", 7, 1),
    ("ph-filter", "ph", 28, 1),
    ("l-checksum", "l", 4, 2),
    ("l-size", "l", 8, 4),
    ("l-p_filesize", "l", 12, 4),
    ("l-p_blocksize", "l", 16, 4),
    ("b0-sz_unc", "b0", 0, 4),
    ("b0-sz_cpr", "b0", 4, 4),
    ("b0-method", "b0", 8, 1),
    ("sentinel-sz_cpr", "s", 4, 4),
]
VOCAB = ("header-corrupted", "p-info-corrupted", "b-info-corrupt-field",
         "b-info-corrupted", "compressed-data-violation", "tolerated",
         "other-refusal")


class Unevaluable(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def classify(rc: int | None, text: str) -> str:
    if rc == 0:
        return "tolerated"
    for token, label in (("header corrupted", "header-corrupted"),
                         ("p_info corrupted", "p-info-corrupted"),
                         ("b_info corrupted", "b-info-corrupted"),
                         ("corrupt b_info", "b-info-corrupt-field"),
                         ("compressed data violation", "compressed-data-violation")):
        if token in text:
            return label
    return "other-refusal"


def run(argv: list, env: dict, timeout: int = 900) -> dict:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, env=env,
                           timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"argv": argv, "rc": None, "tail": [f"{exc.__class__.__name__}: {exc}"],
                "stdout": ""}
    tail = (p.stdout + p.stderr).strip().splitlines()
    return {"argv": argv, "rc": p.returncode, "tail": tail[-2:],
            "stdout": p.stdout, "text": p.stdout + p.stderr}


def child_env(work: str) -> dict:
    return {"HOME": os.path.join(work, "home"), "LANG": "C",
            "PATH": os.environ.get("PATH") or "/usr/bin",
            "TMPDIR": os.path.join(work, "tmp")}


def load_r87(root: str):
    path = os.path.join(os.path.abspath(root), R87_REPAIR)
    spec = importlib.util.spec_from_file_location("r87repair", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod, sha256_file(path)


def anchors(packed: bytes, rep) -> dict:
    ph_off, ph = rep.find_packheader(packed)
    m, s, walk = rep.find_linfo(packed, ph_off, ph)
    return {"ph": ph_off, "l": m, "b0": m + 20, "s": s,
            "header": ph, "walk": walk}


def measure(args) -> tuple[int, dict]:
    work = os.path.abspath(args.work)
    if not os.path.isdir(work):
        raise Unevaluable(f"work_unusable: {work}")
    run_root = tempfile.mkdtemp(prefix="r88-matrix-", dir=work)
    env = child_env(run_root)
    os.makedirs(env["HOME"]); os.makedirs(env["TMPDIR"])
    try:
        if not os.path.isfile(args.upx):
            raise Unevaluable(f"missing_tool: upx ({args.upx})")
        if sha256_file(args.upx) != UPX_SHA256_PIN:
            raise Unevaluable("packer_mismatch: sha256")
        ver = run([args.upx, "--version"], env).get("stdout", "").strip().splitlines()
        if not ver or ver[0] != UPX_VERSION_PIN:
            raise Unevaluable(f"packer_mismatch: version {ver[:1]}")
        for c in CARRIERS:
            if not os.path.isfile(c["source"]) or sha256_file(c["source"]) != c["sha256"]:
                raise Unevaluable(f"carrier_pin: {c['id']}")
        rep, r87_sha = load_r87(args.root)
        cells, per_class = [], {k: 0 for k in VOCAB}
        for c in CARRIERS:
            d = os.path.join(run_root, c["id"])
            os.makedirs(d)
            orig = os.path.join(d, "orig")
            shutil.copy2(c["source"], orig)
            packed = os.path.join(d, "packed")
            r = run([args.upx, "--best", "-q", "-o", packed, orig], env)
            if r["rc"] != 0:
                raise Unevaluable(f"pack_failed: {c['id']} {r.get('tail')}")
            with open(packed, "rb") as fh:
                pbytes = fh.read()
            a = anchors(pbytes, rep)
            base_t = run([args.upx, "-t", "-q", packed], env)
            base_u = run([args.upx, "-d", "-q", "-o", os.path.join(d, "base.unpacked"), packed], env)
            if base_t["rc"] != 0 or base_u["rc"] != 0:
                raise Unevaluable(f"baseline_not_clean: {c['id']}")
            for field, anchor, rel, width in FIELDS:
                off = a[anchor] + rel
                if off + width > len(pbytes):
                    raise Unevaluable(f"offset_out_of_range: {c['id']} {field}")
                buf = bytearray(pbytes)
                before = bytes(buf[off:off + width])
                buf[off:off + width] = b"\0" * width
                tp = os.path.join(d, f"{field}.tampered")
                with open(tp, "wb") as fh:
                    fh.write(buf)
                t = run([args.upx, "-t", "-q", tp], env)
                cls = classify(t["rc"], t.get("text", ""))
                un = os.path.join(d, f"{field}.unpacked")
                u = run([args.upx, "-d", "-q", "-o", un, tp], env)
                usha = sha256_file(un) if u["rc"] == 0 and os.path.isfile(un) else None
                cell = {"carrier": c["id"], "field": field, "anchor": anchor,
                        "offset": off, "width": width, "was": before.hex(),
                        "upx_t_rc": t["rc"], "class": cls,
                        "message": (t.get("tail") or [""])[-1][:160],
                        "upx_d_rc": u["rc"], "identity": usha == c["sha256"]}
                per_class[cls] += 1
                cells.append(cell)
        unclassified = [x for x in cells if x["class"] == "other-refusal"]
        complete = len(cells) == len(CARRIERS) * len(FIELDS)
        met = complete and not unclassified
        receipt = {"tool": TOOL, "tool_sha256": sha256_file(os.path.abspath(__file__)),
                   "r87_module_sha256": r87_sha,
                   "pins": {"upx_sha256": UPX_SHA256_PIN, "upx_version": UPX_VERSION_PIN},
                   "population": {"carriers": [c["id"] for c in CARRIERS],
                                  "fields": [f[0] for f in FIELDS],
                                  "cells": len(cells), "expected": len(CARRIERS) * len(FIELDS)},
                   "per_class": per_class, "unclassified": unclassified,
                   "cells_detail": cells, "met_target": met}
        return (0 if met else 1), receipt
    finally:
        shutil.rmtree(run_root, ignore_errors=True)


def selftest() -> int:
    fails, ncases = [], 0

    def check(name, cond):
        nonlocal ncases
        ncases += 1
        if not cond:
            fails.append(name)

    check("vocab-closed", len(VOCAB) == 7)
    check("fields-seventeen", len(FIELDS) == 17)
    check("tolerated", classify(0, "Tested 1 file.") == "tolerated")
    check("header", classify(1, "upx: f: CantUnpackException: header corrupted 3") == "header-corrupted")
    check("p-info", classify(1, "upx: f: CantUnpackException: p_info corrupted") == "p-info-corrupted")
    check("b-info-field", classify(1, "upx: f: CantUnpackException: corrupt b_info") == "b-info-corrupt-field")
    check("b-info", classify(1, "upx: f: CantUnpackException: b_info corrupted") == "b-info-corrupted")
    check("payload", classify(1, "upx: f: Exception: compressed data violation") == "compressed-data-violation")
    check("unknown", classify(1, "upx: f: SomethingElse") == "other-refusal")
    check("none-rc", classify(None, "") == "other-refusal")
    check("precedence", classify(1, "b_info corrupted") == "b-info-corrupted")
    print(f"SELFTEST cases={ncases} failures={len(fails)} {' '.join(fails)}".rstrip())
    return 0 if not fails else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root", default=".")
    ap.add_argument("--upx", default="/usr/bin/upx")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.work or not a.json_out:
        print("could-not-evaluate: --work and --json-out are required", file=sys.stderr)
        return 2
    try:
        rc, receipt = measure(a)
    except Unevaluable as exc:
        receipt = {"tool": TOOL, "unevaluable": str(exc), "met_target": False}
        rc = 2
    receipt["exit"] = rc
    with open(a.json_out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
    print(f"cells={receipt.get('population', {}).get('cells')} "
          f"per_class={receipt.get('per_class')} met={receipt['met_target']} exit={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
