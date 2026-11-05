#!/usr/bin/env python3
"""matrix.py - tamper matrix and evidence cells for the independently derived
round-90 law (seat ExecDeriveIndep, wave r90-w1).

Drives szcpr_law.py exactly as a counter would (subprocess, files, exit
codes), scores the six P1 cells (jq / xxd / docker-init x stored-7 / stored+7
at first-segment block index 1) and the two declared undecidability cells,
cross-checks the chain geometry against the repo's round-87 tool, and writes
every receipt under the seat's receipts/ directory.  Nothing outside the seat
dir and the scratch dir is written.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path

LAW = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-90/"
           "w1/ExecDeriveIndep/szcpr_law.py")
R87 = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-87/"
           "upx-magic-repair.py")
R88 = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-88/"
           "upx-chain-repair.py")
SCRATCH = Path("/fast/scratch/hyaku/kaidoku-r90/ExecDeriveIndep")
SEAT = LAW.parent
RECEIPTS = SEAT / "receipts"
PACKED = SCRATCH / "packed"
ORIG = SCRATCH / "orig"
UPX = "/usr/bin/upx"
PY = [sys.executable, "-I", "-B"]

CARRIERS = ["jq", "xxd", "docker-init", "libz.so.1.3.2"]
P1_CARRIERS = ["jq", "xxd", "docker-init"]
PINS = {
    "jq": ("e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806", 30800),
    "xxd": ("7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65", 38928),
    "libz.so.1.3.2": ("6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9", 108560),
    "docker-init": ("0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115", 851288),
}


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(cmd: list[str]) -> dict:
    t0 = time.perf_counter()
    cp = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    return {"cmd": " ".join(str(c) for c in cmd), "rc": cp.returncode,
            "stdout": cp.stdout, "stderr": cp.stderr,
            "elapsed_s": round(time.perf_counter() - t0, 3)}


def law_run(mode: str, inp: Path, out: Path | None = None, **kw) -> dict:
    cmd = PY + [str(LAW), mode, "--in", str(inp), "--json"]
    if out is not None:
        cmd += ["--out", str(out)]
    for k, v in kw.items():
        cmd += [f"--{k.replace('_', '-')}", str(v)]
    r = run(cmd)
    r["info"] = json.loads(r["stdout"]) if r["rc"] in (0, 2) and r["stdout"].strip() else None
    return r


def upx_t(p: Path) -> dict:
    return run([UPX, "-t", str(p)])


def upx_d(p: Path, out: Path) -> dict:
    return run([UPX, "-d", str(p), "-o", str(out)])


def cell_arms(name: str, packed: Path, tampered: Path, out: Path,
              repair: dict, tag: str) -> dict:
    """The three P1 arms for a repaired candidate."""
    bin_dir = RECEIPTS / "binaries"
    bin_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(tampered, bin_dir / f"{tag}-tampered.upx")
    shutil.copy2(out, bin_dir / f"{tag}-out.upx")
    pin, pin_size = PINS[name]
    eq = out.read_bytes() == packed.read_bytes()
    t = upx_t(out)
    dec = SCRATCH / "dec" / f"{tag}.dec"
    dec.parent.mkdir(parents=True, exist_ok=True)
    d = upx_d(out, dec)
    dec_ok = False
    if d["rc"] == 0 and dec.exists():
        dec_ok = sha256_file(dec) == pin and dec.stat().st_size == pin_size
    return {
        "arm1_bytes_equal_intact": eq,
        "arm2_upx_t_rc0": t["rc"] == 0,
        "arm2_upx_t": {"rc": t["rc"], "stderr_tail": t["stderr"][-200:]},
        "arm3_upx_d_pin": dec_ok,
        "arm3_upx_d": {"rc": d["rc"], "stderr_tail": d["stderr"][-200:]},
        "repair_rc": repair["rc"],
        "repair_verdict": (repair["info"] or {}).get("verdict"),
        "repair_info": repair["info"],
        "recovered": repair["rc"] == 0 and eq and t["rc"] == 0 and dec_ok
                     and (repair["info"] or {}).get("verdict") == "recovered",
    }


def main() -> int:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    (SCRATCH / "tamper").mkdir(parents=True, exist_ok=True)
    (SCRATCH / "dec").mkdir(parents=True, exist_ok=True)
    report = {"dumps": {}, "baselines": {}, "crosscheck_r87": {},
              "crosscheck_r88": {}, "p1_cells": [], "evidence_cells": []}

    # 1. chain-layout dumps -------------------------------------------------
    for name in CARRIERS:
        src = PACKED / f"{name}.upx"
        r = law_run("dump", src)
        if r["rc"] != 0:
            print(f"FATAL dump {name}: {r}", file=sys.stderr)
            return 1
        (RECEIPTS / f"dump-{name}.json").write_text(json.dumps(r["info"], indent=1))
        report["dumps"][name] = {
            "u_len": r["info"]["u_len"], "accounted_total": r["info"]["accounted_total"],
            "covers_full_u_len": r["info"]["covers_full_u_len"],
            "blocks_first": r["info"]["blocks_first"],
            "first_stop": r["info"]["first_stop"], "resume": r["info"]["resume"],
            "sentinel": r["info"]["sentinel"],
            "first_sum": r["info"]["first_sum"], "resumed_sum": r["info"]["resumed_sum"],
            "block1": r["info"]["first_segment"][1] if len(r["info"]["first_segment"]) > 1 else None,
            "last_first_block": r["info"]["last_first_block"],
        }
        print(f"dump {name}: covered {r['info']['accounted_total']}/{r['info']['u_len']}")

    # 2. baselines: intact packed passes -t and -d reproduces the pin -------
    for name in CARRIERS:
        src = PACKED / f"{name}.upx"
        t = upx_t(src)
        dec = SCRATCH / "dec" / f"baseline-{name}"
        d = upx_d(src, dec)
        pin, pin_size = PINS[name]
        ok = d["rc"] == 0 and dec.exists() and sha256_file(dec) == pin \
            and dec.stat().st_size == pin_size
        report["baselines"][name] = {"upx_t_rc": t["rc"], "upx_d_rc": d["rc"],
                                     "upx_d_pin_match": ok}
        assert t["rc"] == 0, f"baseline -t failed {name}"
        assert ok, f"baseline -d pin mismatch {name}"

    # 3. cross-check geometry against the repo's round-87 tool --------------
    for name in CARRIERS:
        src = PACKED / f"{name}.upx"
        out87 = SCRATCH / "x87" / name
        out87.parent.mkdir(parents=True, exist_ok=True)
        r = run(PY + [str(R87), "--in", str(src), "--out", str(out87), "--json"])
        info = json.loads(r["stdout"]) if r["stdout"].strip() else None
        r88o = SCRATCH / "x88" / name
        r88o.parent.mkdir(parents=True, exist_ok=True)
        r88 = run(PY + [str(R88), "--in", str(src), "--out", str(r88o), "--json"])
        info88 = json.loads(r88["stdout"]) if r88["stdout"].strip() else None
        mine = report["dumps"][name]
        agree = None
        if info:
            agree = {
                "blocks_first": info["walk"]["blocks_first"] == mine["blocks_first"],
                "resume": info["walk"]["resume"] == mine["resume"],
                "sentinel_plus4": info["anchors"]["b_info_end"] == mine["sentinel"] + 4,
            }
        report["crosscheck_r87"][name] = {"rc": r["rc"], "agree": agree}
        report["crosscheck_r88"][name] = {"rc": r88["rc"],
                                          "class": (info88 or {}).get("class")}
        (RECEIPTS / f"r87-crosscheck-{name}.json").write_text(json.dumps(
            {"r87": info, "mine": report["dumps"][name]}, indent=1))

    # 4. the six P1 cells ----------------------------------------------------
    for name in P1_CARRIERS:
        packed = PACKED / f"{name}.upx"
        data = packed.read_bytes()
        dump = json.loads((RECEIPTS / f"dump-{name}.json").read_text())
        b1 = dump["first_segment"][1]
        off, sz_unc, sz_cpr = b1["offset"], b1["sz_unc"], b1["sz_cpr"]
        for delta in (-7, 7):
            val = sz_cpr + delta
            assert 0 < val <= sz_unc, f"{name} b1 stored{delta:+d} out of range"
            tag = f"p1-{name}-b1-delta{delta:+d}"
            tam = SCRATCH / "tamper" / f"{tag}.upx"
            buf = bytearray(data)
            struct.pack_into("<I", buf, off + 4, val)
            tam.write_bytes(bytes(buf))
            tt = upx_t(tam)
            out = SCRATCH / "tamper" / f"{tag}.out"
            rep = law_run("repair", tam, out)
            arms = cell_arms(name, packed, tam, out, rep, tag)
            # decidability sweep on the tampered file
            dv = law_run("derivations", tam, block_offset=off)
            cell = {"cell": tag, "carrier": name, "block_index": 1,
                    "block_offset": off, "stored_sz_cpr": sz_cpr,
                    "delta": delta, "tampered_value": val,
                    "upx_t_on_tampered": {"rc": tt["rc"],
                                          "stderr_tail": tt["stderr"][-200:]},
                    "class_evidence_violation": "compressed data violation"
                                                in tt["stderr"],
                    **arms,
                    "derivations_deciding": (dv["info"] or {}).get("values_derived_reaching_u_len"),
                    "derivations_rows": (dv["info"] or {}).get("rows"),
                    "repair_elapsed_s": (rep["info"] or {}).get("elapsed_s")}
            report["p1_cells"].append(cell)
            print(f"{tag}: recovered={cell['recovered']} verdict={cell['repair_verdict']} "
                  f"deciding={cell['derivations_deciding']}")

    # 5. evidence cells ------------------------------------------------------
    # (a) last first-segment block before the stop: under-determined
    name = "docker-init"
    packed = PACKED / f"{name}.upx"
    data = packed.read_bytes()
    dump = json.loads((RECEIPTS / f"dump-{name}.json").read_text())
    lb = dump["last_first_block"]
    off, sz_unc, sz_cpr = lb["offset"], lb["sz_unc"], lb["sz_cpr"]
    val = sz_cpr - 7
    assert 0 < val <= sz_unc
    tag = "undecidable-last-block-docker-init"
    tam = SCRATCH / "tamper" / f"{tag}.upx"
    buf = bytearray(data)
    struct.pack_into("<I", buf, off + 4, val)
    tam.write_bytes(bytes(buf))
    out = SCRATCH / "tamper" / f"{tag}.out"
    rep = law_run("repair", tam, out)
    dv = law_run("derivations", tam, block_offset=off)
    unchanged = out.read_bytes() == tam.read_bytes()
    cell = {"cell": tag, "carrier": name, "block_index": lb["index"],
            "block_offset": off, "stored_sz_cpr": sz_cpr,
            "tampered_value": val, "repair_verdict": (rep["info"] or {}).get("verdict"),
            "repair_rc": rep["rc"], "bytes_unchanged": unchanged,
            "accepted_candidates": (rep["info"] or {}).get("accepted"),
            "derivations": dv["info"]}
    report["evidence_cells"].append(cell)
    shutil.copy2(tam, RECEIPTS / "binaries" / f"{tag}-tampered.upx")
    print(f"{tag}: verdict={cell['repair_verdict']} unchanged={unchanged} "
          f"deciding={dv['info']['values_derived_reaching_u_len']}")

    # (b) libz: chain under-accounts u_len, exact-total rule cannot decide
    name = "libz.so.1.3.2"
    packed = PACKED / f"{name}.upx"
    data = packed.read_bytes()
    dump = json.loads((RECEIPTS / f"dump-{name}.json").read_text())
    b1 = dump["first_segment"][1]
    off, sz_unc, sz_cpr = b1["offset"], b1["sz_unc"], b1["sz_cpr"]
    val = sz_cpr - 7
    assert 0 < val <= sz_unc
    tag = "undecidable-libz-undercovering"
    tam = SCRATCH / "tamper" / f"{tag}.upx"
    buf = bytearray(data)
    struct.pack_into("<I", buf, off + 4, val)
    tam.write_bytes(bytes(buf))
    out = SCRATCH / "tamper" / f"{tag}.out"
    rep = law_run("repair", tam, out)
    dv = law_run("derivations", tam, block_offset=off)
    unchanged = out.read_bytes() == tam.read_bytes()
    tt = upx_t(tam)
    cell2 = {"cell": tag, "carrier": name, "block_index": 1,
             "block_offset": off, "stored_sz_cpr": sz_cpr,
             "tampered_value": val, "repair_verdict": (rep["info"] or {}).get("verdict"),
             "repair_rc": rep["rc"], "bytes_unchanged": unchanged,
             "upx_t_on_tampered_rc": tt["rc"],
             "derivations": dv["info"]}
    report["evidence_cells"].append(cell2)
    shutil.copy2(tam, RECEIPTS / "binaries" / f"{tag}-tampered.upx")
    print(f"{tag}: verdict={cell2['repair_verdict']} unchanged={unchanged} "
          f"deciding={dv['info']['values_derived_reaching_u_len']}")

    # (c) calibration extras: intact idempotence and plain-ELF refusal
    rep = law_run("repair", PACKED / "jq.upx", SCRATCH / "tamper" / "cal-jq.out")
    cal1 = {"cell": "cal-intact-jq", "rc": rep["rc"],
            "verdict": (rep["info"] or {}).get("verdict"),
            "unchanged": (SCRATCH / "tamper" / "cal-jq.out").read_bytes()
                         == (PACKED / "jq.upx").read_bytes()}
    rep = law_run("repair", PACKED / "libz.so.1.3.2.upx",
                  SCRATCH / "tamper" / "cal-libz.out")
    cal2 = {"cell": "cal-intact-libz", "rc": rep["rc"],
            "verdict": (rep["info"] or {}).get("verdict"),
            "unchanged": (SCRATCH / "tamper" / "cal-libz.out").read_bytes()
                         == (PACKED / "libz.so.1.3.2.upx").read_bytes()}
    rep = law_run("repair", ORIG / "jq", SCRATCH / "tamper" / "cal-plain.out")
    cal3 = {"cell": "cal-plain-elf-refused", "rc": rep["rc"],
            "refused": (rep["info"] or {}).get("refused", "")[:120],
            "nothing_written": not (SCRATCH / "tamper" / "cal-plain.out").exists()}
    report["evidence_cells"] += [cal1, cal2, cal3]
    print(f"cal: {cal1['verdict']} / {cal2['verdict']} / rc={cal3['rc']}")

    (RECEIPTS / "matrix.json").write_text(json.dumps(report, indent=1))
    p1_ok = sum(1 for c in report["p1_cells"] if c["recovered"])
    print(f"P1 {p1_ok} of {len(report['p1_cells'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
