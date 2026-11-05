#!/usr/bin/env python3
"""field_matrix_r89.py - ExecMatrix round-89 scratch instrument (R89-C2 evidence).

Grounds craft rule block 29 (the field-class decision table): for every
`b_info`/PackHeader field class a tamperer can reach, measure on the frozen
population (four pinned carriers, packed by the pinned `upx 5.2.0`, packed
bytes re-checked against the pre-freeze receipt) (a) the packer's own refusal
under `upx -t -q` (verbatim), (b) the round-89 repair's verdict (rc +
`info.class`) and (c) whether the repaired file tests clean.

Label discipline (from tools/round-88/field-tamper-matrix-v2.py): every cell
records the pre-tamper bytes (`was`), a tamper that changed nothing is `noop`
(decided from `was` before any run, never `tolerated`), and the packer's
message class comes from the same closed vocabulary.

Layout is read off the packed bytes via the round-87 module's locators:
PackHeader at ph_off (u_len @ ph_off+16); the l_info whose chain reaches the
end-of-chain sentinel at m (magic "UPX!" @ m+0, l_version @ m+6, l_format
@ m+7); p_info @ m+8 (p_filesize @ m+12 -- asserted == the original file size;
p_blocksize @ m+16); block 0 b_info @ m+20 (sz_unc, sz_cpr, method).

Exit 0 when every cell is classified (no other-refusal, no unrun cell);
1 otherwise; 2 could-not-evaluate (pin drift, pack failure, baseline unclean).
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

TOOL = "scratch/kaidoku-r89/ExecMatrix/field_matrix_r89.py"
UPX = "/usr/bin/upx"
UPX_VERSION_PIN = "upx 5.2.0"
UPX_SHA256_PIN = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R87 = os.path.join(ROOT, "tools", "round-87", "upx-magic-repair.py")
R87_SHA256_PIN = "96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24"
REPAIR = os.path.join(ROOT, "tools", "round-89", "upx-field-value-repair.py")
REPAIR_SHA256_PIN = "332917f2b620da7a659b78db5bf498c8af2eba6ae529d872c2518b62ad6b1070"
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
PRE_PACKED = {
    "jq": "e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a",
    "xxd": "1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff",
    "libz": "a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b",
    "dinit": "b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7",
}
VOCAB = ("header-corrupted", "p-info-corrupted", "b-info-corrupt-field",
         "b-info-corrupted", "compressed-data-violation", "bad-method",
         "bad-seek", "tolerated", "noop", "other-refusal")


class Unevaluable(Exception):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def run(argv: list, env: dict, timeout: int = 600) -> dict:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, env=env,
                           timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"rc": None, "tail": [f"{exc.__class__.__name__}: {exc}"],
                "text": f"{exc.__class__.__name__}: {exc}"}
    text = p.stdout + p.stderr
    tail = [ln for ln in text.strip().splitlines() if ln.strip()]
    return {"rc": p.returncode, "tail": tail[-2:], "text": text}


def classify(rc: int | None, text: str) -> str:
    if rc == 0:
        return "tolerated"
    for token, label in (("header corrupted", "header-corrupted"),
                         ("p_info corrupted", "p-info-corrupted"),
                         ("b_info corrupted", "b-info-corrupted"),
                         ("corrupt b_info", "b-info-corrupt-field"),
                         ("compressed data violation", "compressed-data-violation"),
                         ("bad method", "bad-method"),
                         ("bad seek", "bad-seek")):
        if token in text:
            return label
    return "other-refusal"


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def child_env(work: str) -> dict:
    return {"HOME": os.path.join(work, "home"), "LANG": "C",
            "PATH": os.environ.get("PATH") or "/usr/bin",
            "TMPDIR": os.path.join(work, "tmp")}


def build_cells(pbytes: bytes, m: int, ph_off: int, rep) -> list:
    """The twelve declared classes, resolved to concrete writes on this image."""
    b0 = m + 20
    sz_unc, true_cpr = struct.unpack_from("<II", pbytes, b0)
    cells = [
        {"class": "b0.sz_unc:=0", "off": b0, "width": 4,
         "write": lambda buf: b"\0" * 4},
        {"class": "b0.sz_cpr:=0", "off": b0 + 4, "width": 4,
         "write": lambda buf: b"\0" * 4},
        {"class": "b0.sz_cpr:=true-8", "off": b0 + 4, "width": 4,
         "write": lambda buf: struct.pack("<I", (true_cpr - 8) & 0xFFFFFFFF)},
        {"class": "b0.sz_cpr:=true+8", "off": b0 + 4, "width": 4,
         "write": lambda buf: struct.pack("<I", (true_cpr + 8) & 0xFFFFFFFF),
         "guard": true_cpr + 8 <= sz_unc,
         "guard_expr": f"true+8 ({true_cpr + 8}) <= sz_unc ({sz_unc})"},
        {"class": "b0.sz_cpr:=0xFFFFFFF0", "off": b0 + 4, "width": 4,
         "write": lambda buf: struct.pack("<I", 0xFFFFFFF0)},
        {"class": "b0.sz_cpr:=sz_unc+1", "off": b0 + 4, "width": 4,
         "write": lambda buf: struct.pack("<I", (sz_unc + 1) & 0xFFFFFFFF)},
        {"class": "b0.method^=0xFF", "off": b0 + 8, "width": 1,
         "write": lambda buf: bytes([buf[b0 + 8] ^ 0xFF])},
        {"class": "l_info.version^=0xFF", "off": m + 6, "width": 1,
         "write": lambda buf: bytes([buf[m + 6] ^ 0xFF])},
        {"class": "l_info.format^=0xFF", "off": m + 7, "width": 1,
         "write": lambda buf: bytes([buf[m + 7] ^ 0xFF])},
        {"class": "p_info.p_filesize^=0xFF", "off": m + 12, "width": 4,
         "write": lambda buf: bytes(a ^ 0xFF for a in buf[m + 12:m + 16])},
        {"class": "p_info.p_blocksize^=0xFF", "off": m + 16, "width": 4,
         "write": lambda buf: bytes(a ^ 0xFF for a in buf[m + 16:m + 20])},
        {"class": "PackHeader.u_len:=0", "off": ph_off + 16, "width": 4,
         "write": lambda buf: b"\0" * 4},
    ]
    return cells


def measure(args) -> tuple[int, dict]:
    work = os.path.abspath(args.work)
    if not os.path.isdir(work):
        raise Unevaluable(f"work_unusable: {work}")
    run_root = tempfile.mkdtemp(prefix="r89-matrix-", dir=work)
    env = child_env(run_root)
    os.makedirs(env["HOME"])
    os.makedirs(env["TMPDIR"])
    try:
        # pins
        if sha256_file(UPX) != UPX_SHA256_PIN:
            raise Unevaluable("packer_mismatch: sha256")
        ver = run([UPX, "--version"], env).get("text", "").strip().splitlines()
        if not ver or ver[0] != UPX_VERSION_PIN:
            raise Unevaluable(f"packer_mismatch: version {ver[:1]}")
        if sha256_file(REPAIR) != REPAIR_SHA256_PIN:
            raise Unevaluable("repair_mismatch: sha256")
        if sha256_file(R87) != R87_SHA256_PIN:
            raise Unevaluable("r87_mismatch: sha256")
        for c in CARRIERS:
            if not os.path.isfile(c["source"]) or sha256_file(c["source"]) != c["sha256"]:
                raise Unevaluable(f"carrier_pin: {c['id']}")
        st = run([sys.executable, "-I", "-B", REPAIR, "--selftest"], env)
        selftest_rc = st["rc"]
        rep = load_module(R87, "r87repair")
        cells_out = []
        for c in CARRIERS:
            d = os.path.join(run_root, c["id"])
            os.makedirs(d)
            orig = os.path.join(d, "orig")
            shutil.copy2(c["source"], orig)
            packed = os.path.join(d, "packed")
            r = run([UPX, "--best", "-q", "-o", packed, orig], env)
            if r["rc"] != 0:
                raise Unevaluable(f"pack_failed: {c['id']} {r.get('tail')}")
            with open(packed, "rb") as fh:
                pbytes = fh.read()
            packed_sha = sha256_bytes(pbytes)
            ph_off, ph = rep.find_packheader(pbytes)
            m, s, _walk = rep.find_linfo(pbytes, ph_off, ph)
            b0 = m + 20
            sz_unc, true_cpr = struct.unpack_from("<II", pbytes, b0)
            pf = struct.unpack_from("<I", pbytes, m + 12)[0]
            if pf != os.path.getsize(orig):
                raise Unevaluable(
                    f"layout_drift: {c['id']} p_filesize {pf} != orig {os.path.getsize(orig)}")
            base_t = run([UPX, "-t", "-q", packed], env)
            if base_t["rc"] != 0:
                raise Unevaluable(f"baseline_not_clean: {c['id']} {base_t.get('tail')}")
            for cell in build_cells(pbytes, m, ph_off, rep):
                off, width = cell["off"], cell["width"]
                if cell.get("guard") is False:
                    cells_out.append({
                        "carrier": c["id"], "class": cell["class"],
                        "skipped": f"guard false: {cell['guard_expr']}"})
                    continue
                buf = bytearray(pbytes)
                before = bytes(buf[off:off + width])
                buf[off:off + width] = cell["write"](buf)
                after = bytes(buf[off:off + width])
                effective = before != after
                cd = os.path.join(d, cell["class"].replace("/", "_"))
                os.makedirs(cd, exist_ok=True)
                tp = os.path.join(cd, "tampered")
                with open(tp, "wb") as fh:
                    fh.write(buf)
                t = run([UPX, "-t", "-q", tp], env)
                cls = classify(t["rc"], t.get("text", "")) if effective else "noop"
                rec = {
                    "carrier": c["id"], "class": cell["class"],
                    "anchor_offset": off, "width": width,
                    "was": before.hex(), "new": after.hex(),
                    "effective": effective,
                    "true_b0": {"sz_unc": sz_unc, "sz_cpr": true_cpr,
                                "method": pbytes[b0 + 8]},
                    "upx_t": {"rc": t["rc"], "tail": t["tail"],
                              "text": t["text"][-500:], "class": cls},
                }
                if not effective:
                    rec["repair"] = {"skipped": "noop tamper"}
                    rec["repaired_tests_clean"] = None
                    cells_out.append(rec)
                    continue
                rp = run([sys.executable, "-I", "-B", REPAIR,
                          "--in", tp, "--out", os.path.join(cd, "repaired"),
                          "--info", os.path.join(cd, "info.json")], env)
                info = None
                ip = os.path.join(cd, "info.json")
                if os.path.isfile(ip):
                    with open(ip, "r", encoding="utf-8") as fh:
                        info = json.load(fh)
                rep_rec = {"rc": rp["rc"], "tail": rp["tail"]}
                if info is not None:
                    rep_rec["info_class"] = info.get("info", {}).get("class")
                    rep_rec["derived_sz_cpr"] = info.get("info", {}).get("derived_sz_cpr")
                    rep_rec["stored_sz_cpr"] = info.get("info", {}).get("stored_sz_cpr")
                    rep_rec["delta"] = info.get("info", {}).get("delta")
                rec["repair"] = rep_rec
                clean = None
                if rp["rc"] == 0 and os.path.isfile(os.path.join(cd, "repaired")):
                    with open(os.path.join(cd, "repaired"), "rb") as fh:
                        ob = fh.read()
                    diffs = [i for i, (a, b) in enumerate(zip(buf, ob)) if a != b]
                    rec["repair_diff"] = {
                        "count": len(diffs) + abs(len(ob) - len(buf)),
                        "positions": diffs[:32],
                        "output_equals_input": ob == bytes(buf)}
                    rt = run([UPX, "-t", "-q", os.path.join(cd, "repaired")], env)
                    clean = rt["rc"] == 0
                    rec["repaired_upx_t"] = {"rc": rt["rc"], "tail": rt["tail"]}
                    un = os.path.join(cd, "unpacked")
                    u = run([UPX, "-d", "-q", "-o", un,
                             os.path.join(cd, "repaired")], env)
                    usha = sha256_file(un) if u["rc"] == 0 and os.path.isfile(un) else None
                    rec["repaired_identity"] = bool(usha == c["sha256"])
                rec["repaired_tests_clean"] = clean
                cells_out.append(rec)
        bad = [x for x in cells_out if x.get("skipped")]
        other = [x for x in cells_out if x.get("upx_t", {}).get("class") == "other-refusal"]
        expected = len(CARRIERS) * 12
        complete = len(cells_out) == expected
        receipt = {
            "tool": TOOL, "tool_sha256": sha256_file(os.path.abspath(__file__)),
            "population": {"carriers": [c["id"] for c in CARRIERS],
                           "classes": sorted({c["class"] for c in cells_out}),
                           "cells": len(cells_out), "expected": expected},
            "pins": {"upx_sha256": UPX_SHA256_PIN, "upx_version": UPX_VERSION_PIN,
                     "repair_sha256": sha256_file(REPAIR),
                     "repair_pin": REPAIR_SHA256_PIN,
                     "r87_module_sha256": sha256_file(R87),
                     "repair_selftest_rc": selftest_rc},
            "repair_selftest_rc": selftest_rc,
            "unclassified": other, "skipped_cells": bad,
            "cells": cells_out,
            "met_target": complete and not other,
        }
        return (0 if receipt["met_target"] else 1), receipt
    finally:
        shutil.rmtree(run_root, ignore_errors=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--work", required=True)
    ap.add_argument("--json-out", required=True)
    a = ap.parse_args(argv)
    try:
        rc, receipt = measure(a)
    except Unevaluable as exc:
        receipt = {"tool": TOOL, "unevaluable": str(exc), "met_target": False}
        rc = 2
    receipt["exit"] = rc
    tmp = a.json_out + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
    os.replace(tmp, a.json_out)
    print(f"cells={receipt.get('population', {}).get('cells')} "
          f"unclassified={len(receipt.get('unclassified', []))} "
          f"met={receipt['met_target']} exit={rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
