#!/usr/bin/env python3
"""stop-boundary-repair-battery-v3.py - round-93 counter (R93-C1, calibration).

Scores a REPAIR command on the round-91 class `T7-chain-stop-boundary` exactly
like `tools/round-92/stop-boundary-repair-battery.py` over its five public
carriers (jq, xxd, libz, docker-init, xz; 10 near cells +/-7, 10 far cells +/-40,
5 intact controls), then adds the **fresh-pack held-out arm** that the round-92
named limits (M92-d, CHEAT-D, CHEAT-E) asked for:

A nonce-marked source (`FRESH_SOURCES`, sha-pinned) is packed fresh at measure
time, so no precomputed table of the five public carriers can contain its bytes:

- the source is mutated with a run nonce (`KAIDOKU-R93-` + 16 hex chars) written
  into the largest non-executable PT_LOAD segment (a region the packer compresses,
  so `upx -d` reproduces the mutated bytes byte-identically);
- the mutated source is packed twice with the pinned UPX (`--best`); both outputs
  must be byte-equal (determinism guard) and the fresh packed image must differ
  from every public packed image (table-miss precondition);
- its last block is tampered by the near directions (-7/+7) and far directions
  (-40/+40), plus an intact control: 2 near cells, 2 far cells, 1 intact.

A fresh near cell is **repaired** only when it meets the round-92 repaired class
(output == the fresh packed bytes) AND the output round-trips: `upx -d` on the
output reproduces the mutated source bytes byte-for-byte. Far cells must be
refused. The fresh intact control must return the input byte-identical.

Refusal typing is **strict** (round-92 ReviewerContract note 3): `typed_strict`
counts a cell only when rc == 2 AND the last stdout line is a JSON object whose
`refused` value is a non-empty string; `{"refused": null}` is refused-untyped.

Frozen label: `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6;
far-refused 12 of 12; fresh-roundtrip 2 of 2`. `met_target` requires the label
to equal `--expect` exactly, every merged count atom true, and every fresh
provenance atom true (marker present in the mutated source, absent from the
original, determinism, no collision with any public packed image). Exit 0 iff
met. Scratch is `--work`; every child sees `TMPDIR` under it (env_for).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import secrets
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "tools/round-93/stop-boundary-repair-battery-v3.py"
R92_BATTERY = os.path.join(HERE, "..", "round-92", "stop-boundary-repair-battery.py")
DEFAULT_REPAIR = "tools/round-92/upx-stop-boundary-search-repair.py"
FAR_DELTAS = (-40, 40)
MARKER_PREFIX = b"KAIDOKU-R93-"
# (cid, absolute source path, pinned sha256 of the unpacked source)
FRESH_SOURCES = [
    ("env", "/usr/bin/env",
     "a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301"),
]
PUBLIC_LABEL = ("repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; "
                "far-refused 10 of 10")
FROZEN_LABEL = ("repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; "
                "far-refused 12 of 12; fresh-roundtrip 2 of 2")
PT_LOAD = 1
PF_X = 1


def _load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


b92 = _load(R92_BATTERY, "r92_repair_battery")
v2 = b92.v2


def mutate_source(raw: bytes, nonce_hex: str) -> tuple:
    """Write `KAIDOKU-R93-<nonce>` into the largest non-exec PT_LOAD segment.

    Returns (mutated bytes, info dict). Deterministic for a given source and
    nonce; the site is the middle of the segment's file image, so the marker
    never straddles the segment end."""
    if raw[:4] != b"\x7fELF":
        raise ValueError("fresh source is not an ELF")
    if raw[4] != 2:
        raise ValueError("fresh source is not little-endian 64-bit")
    e_phoff = struct.unpack_from("<Q", raw, 0x20)[0]
    e_phentsize, e_phnum = struct.unpack_from("<HH", raw, 0x36)
    best = None
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        p_type, p_flags = struct.unpack_from("<II", raw, off)
        if p_type != PT_LOAD or (p_flags & PF_X):
            continue
        p_offset, p_filesz = struct.unpack_from("<QQ", raw, off + 8)
        if p_filesz < 64:
            continue
        if best is None or p_filesz > best[2]:
            best = (off, i, p_filesz, p_offset)
    if best is None:
        raise ValueError("no non-executable PT_LOAD segment")
    p_filesz, p_offset = best[2], best[3]
    site = p_offset + p_filesz // 2
    marker = MARKER_PREFIX + nonce_hex.encode()
    if site + len(marker) > p_offset + p_filesz:
        raise ValueError("marker would straddle the segment end")
    mut = bytearray(raw)
    mut[site:site + len(marker)] = marker
    info = {"segment_index": best[1], "marker_offset": site,
            "marker_bytes": len(marker)}
    return bytes(mut), info


def strict_typed(rec: dict) -> bool:
    """rc 2 and the last stdout line is a JSON object whose `refused` value is
    a non-empty string (the strict parsing round-92 ReviewerContract asked for)."""
    if rec.get("rc") != 2:
        return False
    lines = [ln for ln in (rec.get("stdout") or "").strip().splitlines() if ln.strip()]
    if not lines:
        return False
    try:
        obj = json.loads(lines[-1])
    except ValueError:
        return False
    if not isinstance(obj, dict) or "refused" not in obj:
        return False
    val = obj["refused"]
    return isinstance(val, str) and val.strip() != ""


def roundtrip_sha(data: bytes, env: dict, work: str):
    """`upx -d` on data; the decompressed bytes' sha256, or None."""
    box = tempfile.mkdtemp(prefix="rt-", dir=work)
    cand, outp = os.path.join(box, "cand"), os.path.join(box, "dec")
    with open(cand, "wb") as fh:
        fh.write(data)
    r = v2.run([v2.UPX, "-d", "-q", "-o", outp, cand], env, 300)
    if r["rc"] != 0 or not os.path.isfile(outp):
        return None
    with open(outp, "rb") as fh:
        return v2.sha256_bytes(fh.read())


def score_fresh_cell(repair: str, tampered: bytes, block: dict, packed: bytes,
                     env: dict, work: str) -> dict:
    """Classify one fresh cell like the round-92 battery's score_cell, but keep
    the output bytes so the `upx -d` roundtrip can run without re-invoking."""
    rec = v2.invoke(repair, tampered, env, work)
    out = rec.get("output")
    rc = rec.get("rc")
    row = {"tampered_block": block["block"], "stored_sz_cpr": block["sz_cpr"],
           "rc": rc, "box_after": rec.get("box_after"), "tail": rec.get("tail"),
           "stdout": rec.get("stdout", ""), "output": out}
    if rc == 0 and out is not None:
        lo, hi = block["block"] + 4, block["block"] + 8
        if out == packed:
            row["class"] = "repaired"
        elif len(out) != len(tampered):
            row["class"] = "unsafe"
            row["detail"] = f"length {len(out)} != {len(tampered)}"
        elif out == tampered:
            row["class"] = "silent"
        else:
            outside = [i for i, (a, b) in enumerate(zip(tampered, out))
                       if a != b and not (lo <= i < hi)]
            row["class"] = "unsafe" if outside else "wrong"
            if outside:
                row["outside_window"] = outside[:8]
    elif rc not in (0, None) and out is None:
        row["class"] = "refused"
        row["typed_strict"] = strict_typed(rec)
    else:
        row["class"] = "other"
    return row


def fresh_arm(repair: str, env: dict, work: str, rep, r88, public_shas: dict,
              root: str) -> dict:
    out = {"carrier": None, "cells": [], "intact": None, "provenance": {},
           "unevaluable": None}
    if len(FRESH_SOURCES) != 1:
        out["unevaluable"] = "fresh arm expects exactly one source"
        return out
    cid, src, pin = FRESH_SOURCES[0]
    out["carrier"] = "fresh-" + cid
    if v2.sha256_file(src) != pin:
        out["unevaluable"] = f"fresh source pin drift: {cid}"
        return out
    with open(src, "rb") as fh:
        raw = fh.read()
    nonce = secrets.token_hex(8)
    try:
        mut, minfo = mutate_source(raw, nonce)
    except ValueError as exc:
        out["unevaluable"] = f"fresh mutation failed: {exc}"
        return out
    marker = MARKER_PREFIX + nonce.encode()
    prov = out["provenance"]
    prov.update({"source": src, "source_sha256": pin, "nonce": nonce,
                 "marker_offset": minfo["marker_offset"],
                 "marker_in_mutated": marker in mut,
                 "marker_absent_in_original": marker not in raw})
    src_path = os.path.join(work, "fresh-src.bin")
    with open(src_path, "wb") as fh:
        fh.write(mut)
    try:
        packed1 = v2.pack(src_path, work, env)
        packed2 = v2.pack(src_path, work, env)
    except RuntimeError as exc:
        out["unevaluable"] = f"fresh pack failed: {exc}"
        return out
    prov["deterministic"] = packed1 == packed2
    prov["fresh_packed_sha256"] = v2.sha256_bytes(packed1)
    prov["collides_public_packed"] = prov["fresh_packed_sha256"] in set(public_shas)
    b0, blocks = v2.layout(packed1, rep, r88)
    prov["blocks"] = len(blocks)
    if not prov["marker_in_mutated"] or not prov["marker_absent_in_original"] \
            or not prov["deterministic"] or prov["collides_public_packed"] \
            or not blocks:
        out["unevaluable"] = "fresh provenance atoms failed"
        return out
    last = blocks[-1]
    for kind, deltas in (("near", v2.DIRECTIONS), ("far", FAR_DELTAS)):
        for delta in deltas:
            value = last["sz_cpr"] + delta
            if not (0 < value <= last["sz_unc"]):
                out["cells"].append({"carrier": out["carrier"], "kind": kind,
                                     "delta": delta, "class": "out-of-range"})
                continue
            t = bytearray(packed1)
            struct.pack_into("<I", t, last["block"] + 4, value)
            row = score_fresh_cell(repair, bytes(t), last, packed1, env, work)
            row.update({"carrier": out["carrier"], "kind": kind, "delta": delta,
                        "stored": last["sz_cpr"], "value": value,
                        "block_index": len(blocks) - 1})
            if row.get("class") == "repaired" and row.get("output") is not None:
                dec = roundtrip_sha(row["output"], env, work)
                row["roundtrip"] = dec == v2.sha256_bytes(mut)
                if not row["roundtrip"]:
                    row["class"] = row["class"]
            out["cells"].append(row)
    rec = v2.invoke(repair, packed1, env, work)
    out["intact"] = {"carrier": out["carrier"], "rc": rec.get("rc"),
                     "identity": rec.get("rc") == 0 and rec.get("output") == packed1,
                     "box_after": rec.get("box_after"),
                     "typed_strict": strict_typed(rec) if rec.get("rc") not in (0, None) else None}
    return out


def score(args) -> tuple:
    root = os.path.abspath(args.root)
    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    repair = os.path.join(root, args.repair_cmd)
    if not os.path.isfile(repair):
        return 2, {"tool": TOOL, "unevaluable": f"no repair command at {args.repair_cmd}"}
    if v2.sha256_file(v2.UPX) != v2.UPX_SHA256:
        return 2, {"tool": TOOL, "unevaluable": "packer sha256 drift"}

    pub_args = argparse.Namespace(root=args.root, repair_cmd=args.repair_cmd,
                                  work=args.work, rev=args.rev,
                                  expect=PUBLIC_LABEL, json_out=None)
    code92, pub = b92.score(pub_args)
    if "unevaluable" in pub:
        pub["tool"] = TOOL
        pub["stage"] = "public"
        return 2, pub
    public_shas = {c["packed_sha256"] for c in pub["carriers"].values()}
    env = v2.env_for(work)
    rep = v2._load(os.path.join(root, v2.R87), "r87")
    r88 = v2._load(os.path.join(root, v2.R88), "r88")
    fresh = fresh_arm(repair, env, work, rep, r88, public_shas, root)
    if fresh.get("unevaluable"):
        return 2, {"tool": TOOL, "stage": "fresh", "unevaluable": fresh["unevaluable"],
                   "provenance": fresh.get("provenance", {})}

    near = [c for c in fresh["cells"] if c["kind"] == "near"
            and c.get("class") != "out-of-range"]
    far = [c for c in fresh["cells"] if c["kind"] == "far"
           and c.get("class") != "out-of-range"]
    fresh_repaired = sum(1 for c in near if c["class"] == "repaired")
    roundtrip_ok = sum(1 for c in near if c.get("class") == "repaired")
    fresh_far_refused = sum(1 for c in far if c["class"] == "refused")
    fresh_intact_ok = 1 if fresh["intact"]["identity"] else 0

    counts = {
        "scored": pub["counts"]["scored"] + len(near),
        "repaired": pub["counts"]["repaired"] + fresh_repaired,
        "wrong": pub["counts"]["wrong"],
        "unsafe": pub["counts"]["unsafe"],
        "refused": pub["counts"]["refused"] + sum(1 for c in near if c["class"] == "refused"),
        "silent": pub["counts"]["silent"],
        "intact": pub["counts"]["intact"] + fresh_intact_ok,
        "far": pub["counts"]["far"] + len(far),
        "far_refused": pub["counts"]["far_refused"] + fresh_far_refused,
        "fresh_scored": len(near),
        "fresh_repaired": fresh_repaired,
        "fresh_roundtrip": roundtrip_ok,
        "fresh_far": len(far),
        "fresh_far_refused": fresh_far_refused,
    }
    label = (f"repaired {counts['repaired']} of {counts['scored']}; "
             f"wrong {counts['wrong']}; unsafe {counts['unsafe']}; "
             f"intact {counts['intact']} of 6; "
             f"far-refused {counts['far_refused']} of {counts['far']}; "
             f"fresh-roundtrip {counts['fresh_roundtrip']} of {counts['fresh_scored']}")
    prov = fresh["provenance"]
    prov_ok = (prov.get("marker_in_mutated") and prov.get("marker_absent_in_original")
               and prov.get("deterministic") and not prov.get("collides_public_packed"))
    met = (label == args.expect and counts["scored"] == 12 and counts["repaired"] == 12
           and counts["wrong"] == 0 and counts["unsafe"] == 0
           and counts["intact"] == 6 and counts["far"] == 12
           and counts["far_refused"] == 12
           and counts["fresh_scored"] == 2 and counts["fresh_roundtrip"] == 2
           and counts["fresh_far"] == 2 and counts["fresh_far_refused"] == 2
           and bool(prov_ok))
    receipt = {
        "tool": TOOL, "class": "T7-chain-stop-boundary", "repair": args.repair_cmd,
        "repair_sha256": v2.sha256_file(repair),
        "counter_sha256": v2.sha256_file(os.path.join(root, TOOL)),
        "imported_r92_battery_sha256": v2.sha256_file(R92_BATTERY),
        "imported_v2_sha256": v2.sha256_file(
            os.path.join(root, "tools/round-92/stop-boundary-battery-v2.py")),
        "revision": args.rev,
        "public_label": pub["label"], "public_met": pub["met_target"],
        "public_carriers": pub["carriers"], "public_cells": pub["cells"],
        "public_intact": pub["intact"],
        "fresh_cells": fresh["cells"], "fresh_intact": fresh["intact"],
        "fresh_provenance": prov,
        "counts": counts, "expect": args.expect, "label": label,
        "met_target": met, "exit": 0 if met else 1,
    }
    return (0 if met else 1), receipt


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--repair-cmd", default=DEFAULT_REPAIR)
    ap.add_argument("--work", required=True)
    ap.add_argument("--rev", default="worktree")
    ap.add_argument("--expect", required=True, help="frozen label: %r" % FROZEN_LABEL)
    ap.add_argument("--json-out")
    args = ap.parse_args(argv)
    code, receipt = score(args)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
    print(receipt.get("label", receipt.get("unevaluable")), "met",
          receipt.get("met_target"), "exit", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
