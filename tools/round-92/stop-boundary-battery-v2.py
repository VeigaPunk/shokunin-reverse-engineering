#!/usr/bin/env python3
"""stop-boundary-battery-v2.py - round-92 counter (R92-C2, calibration).

Successor to `tools/round-91/stop-boundary-battery.py` (round-91 counter left
unchanged: its frozen label is historical). It scores a refusal command on the
same class `T7-chain-stop-boundary` (packed UPX 5.2.0 `--best` little-endian
ELF; last block before the chain stop has `sz_cpr` moved by -7 or +7) over FIVE
carriers: the four round-91 carriers (jq, xxd, libz, docker-init) plus one
UNSEEN carrier (`/usr/bin/xz`) that no round-91 cheat table, carrier list or
hash table names. 5 carriers x 2 directions = 10 tampered cells, plus the intact
control on each carrier (5 arms).

Per tampered cell the command runs on a private input listed AFTER the child
exits (QUALITY 170). Classes:

- **refused** - rc != 0, no output file, input left alone;
- **typed**   - a refused cell whose rc is 2 AND whose last stdout line is a JSON
                object carrying a `refused` key (the round-91 contract's typed
                refusal, QUALITY 177); a rc-1 exit is refused but not typed;
- **unsafe**  - rc 0 and an output that differs from the input OUTSIDE the
                tampered 4-byte window (QUALITY 176);
- **silent**  - rc 0 and output byte-identical to the input (QUALITY 167);
- **recovered / partial / other** - anything else (none is expected here).

Intact control (QUALITY 166): on each carrier's intact packed bytes the command
must return rc 0 with output byte-identical to the input.

Frozen label: `refused R of C; typed T; unsafe U; intact I of 5`. `met_target`
requires the label to equal `--expect` exactly, `C == 10`, `T == 10`, `U == 0`,
`R == 10` and `I == 5`, with exit 0. The receipt pins the command and counter
sha256 values, the packer sha256 and every carrier's pinned and packed sha256.
Scratch is `--work` (TMPDIR honoured; no `/tmp` writes).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import importlib.util

TOOL = "tools/round-92/stop-boundary-battery-v2.py"
UPX = "/usr/bin/upx"
UPX_SHA256 = "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
CARRIERS = [
    ("jq", "/usr/bin/jq", "e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806"),
    ("xxd", "/usr/bin/xxd", "7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65"),
    ("libz", "/usr/lib/libz.so.1.3.2", "6c78c5e58c3bb49a1cd151a95cdf1a17fe07a91a57a59e0279b984c533075ca9"),
    ("dinit", "/usr/bin/docker-init", "0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115"),
    ("xz-unseen", "/usr/bin/xz", "24c477492f40fd8b1b6eca2d6cc020e47d4c9c11ee1bfb9ba57fb8e2f6a11bda"),
]
DIRECTIONS = (-7, 7)
DEFAULT_REPAIR = "tools/round-91/upx-stop-boundary-repair.py"
R87 = "tools/round-87/upx-magic-repair.py"
R88 = "tools/round-88/upx-chain-repair.py"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str) -> str:
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def env_for(work: str) -> dict:
    tmp = os.path.join(work, "tmp")
    home = os.path.join(work, "home")
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(home, exist_ok=True)
    return {"PATH": os.environ.get("PATH") or "/usr/bin", "LANG": "C",
            "HOME": home, "TMPDIR": tmp}


def run(argv: list, env: dict, timeout: int = 900) -> dict:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, env=env, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"rc": None, "error": f"{exc.__class__.__name__}: {exc}", "stdout": "", "tail": []}
    return {"rc": p.returncode, "stdout": p.stdout,
            "tail": (p.stdout + p.stderr).strip().splitlines()[-2:]}


def layout(packed: bytes, rep, r88) -> tuple:
    """(b0, the walkable first-segment blocks) for the packed bytes."""
    ph_off, ph = rep.find_packheader(packed)
    best = (None, [])
    for m in r88.l_info_candidates(packed, ph_off, ph):
        b0 = m + 20
        if b0 + 12 > ph_off:
            continue
        su0, _ = struct.unpack_from("<II", packed, b0)
        if su0 == 0:
            continue
        method = packed[b0 + 8]
        q, blocks = b0, []
        while q + 12 <= ph_off:
            su, sc = struct.unpack_from("<II", packed, q)
            if su == 0 or sc == 0 or sc > su or q + 12 + sc > ph_off \
                    or packed[q + 8] not in (method, ph["method"]):
                break
            blocks.append({"block": q, "sz_unc": su, "sz_cpr": sc})
            q += 12 + sc
        if len(blocks) > len(best[1]):
            best = (b0, blocks)
    return best


def invoke(repair: str, data: bytes, env: dict, work: str) -> dict:
    box = tempfile.mkdtemp(prefix="inv-", dir=work)
    src, dst = os.path.join(box, "in"), os.path.join(box, "out")
    with open(src, "wb") as fh:
        fh.write(data)
    rec = run([sys.executable, "-I", "-B", repair, "--in", src, "--out", dst], env, 600)
    after = sorted(os.listdir(box))  # QUALITY 170: list after the child exits
    out = None
    if os.path.isfile(dst):
        with open(dst, "rb") as fh:
            out = fh.read()
    rec.update({"box_after": after, "output": out})
    return rec


def typed_refusal(stdout: str) -> bool:
    """True when the last stdout line is a JSON object with a `refused` key."""
    lines = [ln for ln in stdout.strip().splitlines() if ln.strip()]
    if not lines:
        return False
    try:
        obj = json.loads(lines[-1])
    except ValueError:
        return False
    return isinstance(obj, dict) and "refused" in obj


def score_cell(repair: str, tampered: bytes, block: dict, env: dict, work: str,
               packer_test) -> dict:
    rec = invoke(repair, tampered, env, work)
    out = rec.get("output")
    rc = rec.get("rc")
    row = {"tampered_block": block["block"], "stored_sz_cpr": block["sz_cpr"],
           "rc": rc, "box_after": rec.get("box_after"), "tail": rec.get("tail"),
           "typed": False}
    if rc == 0 and out is not None:
        lo, hi = block["block"] + 4, block["block"] + 8
        if len(out) != len(tampered):
            row["class"] = "unsafe"
            row["detail"] = f"length {len(out)} != {len(tampered)}"
        elif out == tampered:
            row["class"] = "silent"
        else:
            outside = [i for i, (a, b) in enumerate(zip(tampered, out))
                       if a != b and not (lo <= i < hi)]
            if outside:
                row["class"] = "unsafe"
                row["outside_window"] = outside[:8]
            else:
                row["class"] = "recovered" if packer_test(out, env, work) else "partial"
    elif rc not in (0, None) and out is None:
        row["class"] = "refused"
        row["typed"] = rc == 2 and typed_refusal(rec.get("stdout", ""))
    else:
        row["class"] = "other"
    return row


def packer_test(data: bytes, env: dict, work: str) -> bool:
    box = tempfile.mkdtemp(prefix="pt-", dir=work)
    p = os.path.join(box, "cand")
    with open(p, "wb") as fh:
        fh.write(data)
    return run([UPX, "-t", "-q", p], env)["rc"] == 0


def pack(src: str, work: str, env: dict) -> bytes:
    box = tempfile.mkdtemp(prefix="pack-", dir=work)
    inp, outp = os.path.join(box, "in"), os.path.join(box, "packed")
    shutil.copyfile(src, inp)
    os.chmod(inp, 0o755)
    r = run([UPX, "--best", "-q", "-o", outp, inp], env)
    if r["rc"] != 0 or not os.path.isfile(outp):
        raise RuntimeError(f"pack failed for {src}: {r}")
    with open(outp, "rb") as fh:
        return fh.read()


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def score(args) -> tuple:
    root = os.path.abspath(args.root)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    env = env_for(work)
    repair = os.path.join(root, args.repair_cmd)
    if not os.path.isfile(repair):
        return 2, {"tool": TOOL, "unevaluable": f"no repair command at {args.repair_cmd}"}
    if sha256_file(UPX) != UPX_SHA256:
        return 2, {"tool": TOOL, "unevaluable": "packer sha256 drift"}
    rep = _load(os.path.join(root, R87), "r87")
    r88 = _load(os.path.join(root, R88), "r88")
    cells, intact, carriers = [], [], {}
    for cid, src, pin in CARRIERS:
        if sha256_file(src) != pin:
            return 2, {"tool": TOOL, "unevaluable": f"carrier pin drift: {cid}"}
        packed = pack(src, work, env)
        b0, blocks = layout(packed, rep, r88)
        carriers[cid] = {"source_sha256": pin, "packed_sha256": sha256_bytes(packed),
                         "blocks": len(blocks)}
        if not blocks:
            return 2, {"tool": TOOL, "unevaluable": f"no walkable chain: {cid}"}
        rec = invoke(repair, packed, env, work)
        same = rec.get("rc") == 0 and rec.get("output") == packed
        intact.append({"carrier": cid, "rc": rec.get("rc"), "identity": same,
                       "box_after": rec.get("box_after")})
        last = blocks[-1]
        for delta in DIRECTIONS:
            value = last["sz_cpr"] + delta
            if not (0 < value <= last["sz_unc"]):
                cells.append({"carrier": cid, "delta": delta, "class": "out-of-range"})
                continue
            t = bytearray(packed)
            struct.pack_into("<I", t, last["block"] + 4, value)
            row = score_cell(repair, bytes(t), last, env, work, packer_test)
            row.update({"carrier": cid, "delta": delta, "stored": last["sz_cpr"],
                        "value": value, "block_index": len(blocks) - 1})
            cells.append(row)
    scored = [c for c in cells if c.get("class") != "out-of-range"]
    refused = sum(1 for c in scored if c["class"] == "refused")
    typed = sum(1 for c in scored if c.get("typed"))
    unsafe = sum(1 for c in scored if c["class"] == "unsafe")
    silent = sum(1 for c in scored if c["class"] == "silent")
    recovered = sum(1 for c in scored if c["class"] == "recovered")
    intact_ok = sum(1 for i in intact if i["identity"])
    label = (f"refused {refused} of {len(scored)}; typed {typed}; unsafe {unsafe}; "
             f"intact {intact_ok} of {len(intact)}")
    met = (label == args.expect and len(scored) == 10 and typed == 10 and unsafe == 0
           and intact_ok == 5 and refused == 10)
    return (0 if met else 1), {
        "tool": TOOL, "class": "T7-chain-stop-boundary", "repair": args.repair_cmd,
        "repair_sha256": sha256_file(repair),
        "counter_sha256": sha256_file(os.path.join(root, TOOL)),
        "revision": args.rev, "cells": cells, "intact": intact, "carriers": carriers,
        "counts": {"scored": len(scored), "refused": refused, "typed": typed,
                   "unsafe": unsafe, "silent": silent, "recovered": recovered,
                   "intact": intact_ok},
        "expect": args.expect, "label": label, "met_target": met,
        "exit": 0 if met else 1,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--repair-cmd", default=DEFAULT_REPAIR)
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--expect", required=True,
                    help="frozen label: 'refused 10 of 10; typed 10; unsafe 0; intact 5 of 5'")
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    code, receipt = score(args)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(receipt.get("label", receipt.get("unevaluable")), "met", receipt.get("met_target"),
          "exit", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
