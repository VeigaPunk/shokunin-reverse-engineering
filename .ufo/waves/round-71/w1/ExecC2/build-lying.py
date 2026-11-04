#!/usr/bin/env python3
"""ExecC2 independent lying-field forgery builder (R71-C2 rederivation).

Cuts six receipts from the round-70 landing material, relabels each to the
round-70 FIRST-CUT world and lies in exactly one verdict-relevant field per
shape.  Written independently for the w1 attack wave; the declared clause map
comes from plans/round-71-claims.md (R71-C2), not from the shipped battery.
"""
import copy
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
MATERIAL = os.path.join(ROOT, ".ufo/waves/round-70/l1/scores/c3-at-landing.json")
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lying")
FIRST_CUT_REV = "4737a542ae3b1b910d8fe43efbd572bc578b07c6"
LANDING_REV = "7c155617bb42dadf1725b88a06fe3f235c364f0a"
TOOL = "tools/round-70/packed-elf.py"

SHAPES = ["L1_unpacked-counts", "L2_packed-sha", "L3_section-list",
          "L4_runs-argv", "L5_refusal", "L6_format"]


def blob_sha256(rev: str, path: str = TOOL) -> str:
    proc = subprocess.run(["git", "-C", ROOT, "show", f"{rev}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(f"git show {rev}:{path} failed: {proc.stderr.decode()}")
    return hashlib.sha256(proc.stdout).hexdigest()


def relabel(receipt: dict) -> None:
    """Move the producer fields to the first-cut world (rev + instrument)."""
    receipt["rev"] = FIRST_CUT_REV
    receipt["instrument"] = {"path": TOOL, "sha256": blob_sha256(FIRST_CUT_REV),
                             "rev": FIRST_CUT_REV}


def apply_lie(receipt: dict, shape: str) -> str:
    carriers = receipt["carriers"]
    if shape == "L1_unpacked-counts":
        assert isinstance(carriers[0].get("unpacked_counts"), dict)
        before = carriers[0]["unpacked_counts"]["procedure_count"]
        carriers[0]["unpacked_counts"]["procedure_count"] = before + 1
        return f"carriers[0].unpacked_counts.procedure_count {before} -> {before + 1}"
    if shape == "L2_packed-sha":
        before = carriers[1].get("packed_sha256")
        carriers[1]["packed_sha256"] = "0" * 64
        assert before is not None and before != "0" * 64
        return f"carriers[1].packed_sha256 {before[:12]}... -> zeros"
    if shape == "L3_section-list":
        before_rc = carriers[2].get("upx_list_rc")
        carriers[2]["section_count"] = 3
        carriers[2]["upx_list_rc"] = 1
        return (f"carriers[2].section_count -> 3, upx_list_rc {before_rc} -> 1")
    if shape == "L4_runs-argv":
        argv = carriers[0]["runs"]["pack"]["argv"]
        assert "--best" in argv
        carriers[0]["runs"]["pack"]["argv"] = [a for a in argv if a != "--best"]
        return f"carriers[0].runs.pack.argv {argv} -> {carriers[0]['runs']['pack']['argv']}"
    if shape == "L5_refusal":
        refusal = carriers[0].get("refusal")
        assert isinstance(refusal, dict), "carriers[0] has no refusal row"
        before = refusal.get("packed_rc")
        refusal["packed_rc"] = 0
        return f"carriers[0].refusal.packed_rc {before} -> 0"
    if shape == "L6_format":
        fmt = carriers[3].get("format")
        assert isinstance(fmt, dict), "carriers[3] has no format row"
        before = fmt.get("type")
        fmt["type"] = "DYN (Position-Independent Executable file)"
        assert before != fmt["type"], "L6 lie would be a no-op"
        return f"carriers[3].format.type {before!r} -> {fmt['type']!r}"
    raise SystemExit(f"unknown shape {shape}")


def main() -> int:
    with open(MATERIAL, encoding="utf-8") as fh:
        material = json.load(fh)
    if material.get("rev") != LANDING_REV:
        raise SystemExit(f"material rev {material.get('rev')} != {LANDING_REV}")
    os.makedirs(OUTDIR, exist_ok=True)
    manifest = {"builder": "ExecC2 independent builder",
                "material": MATERIAL, "material_rev": material["rev"],
                "first_cut_rev": FIRST_CUT_REV,
                "first_cut_instrument_sha256": blob_sha256(FIRST_CUT_REV),
                "landing_instrument_sha256": material["instrument"]["sha256"],
                "shapes": {}}
    # honest control: relabelled, no lie
    honest = copy.deepcopy(material)
    relabel(honest)
    honest_path = os.path.join(OUTDIR, "honest-relabel.json")
    with open(honest_path, "w", encoding="utf-8") as fh:
        json.dump(honest, fh, indent=1, sort_keys=True)
    manifest["honest_control"] = honest_path
    for shape in SHAPES:
        receipt = copy.deepcopy(material)
        relabel(receipt)
        note = apply_lie(receipt, shape)
        path = os.path.join(OUTDIR, f"{shape}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=1, sort_keys=True)
        manifest["shapes"][shape] = {"path": path, "lie": note}
        print(f"{shape}: {note}")
    with open(os.path.join(OUTDIR, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
    print(f"first_cut instrument.sha256 = {blob_sha256(FIRST_CUT_REV)}")
    print(f"honest control: {honest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
