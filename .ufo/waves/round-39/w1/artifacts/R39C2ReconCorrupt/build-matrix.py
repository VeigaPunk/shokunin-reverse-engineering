#!/usr/bin/env python3
"""Assemble artifacts/run-matrix.json + feature-table.md from the saved envelopes.

usage: python3 build-matrix.py   (run from this artifact directory)
Reads ONLY files in this directory: envelopes/, sasquatch-stderr/, inputs/.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import corrupt  # noqa: E402
from envelope_features import features  # noqa: E402

# run name -> (envelope stem, carrier file, clean carrier for offset description,
#              sasquatch-stderr stem or None, build note)
RUNS = [
    ("ta-clean", "ta-clean", "ta-be-gzip.sqsh", "ta-be-gzip.sqsh", "ta-clean", "basis: gen-squashfs --endian be --comp gzip"),
    ("tb-clean", "tb-clean", "tb-be-gzip.sqsh", "tb-be-gzip.sqsh", "tb-clean", "basis: gen-squashfs --endian be --comp gzip"),
    ("tc-clean", "tc-clean", "tc-be-gzip.sqsh", "tc-be-gzip.sqsh", "tc-clean", "basis: gen-squashfs --endian be --comp gzip"),
    ("td-clean", "td-clean", "td-be-gzip.sqsh", "td-be-gzip.sqsh", "td-be-gzip", "basis with in-tree + escaping symlink"),
    ("te-clean", "te-clean", "te-be-gzip.sqsh", "te-be-gzip.sqsh", None, "basis with in-tree symlink only"),
    ("tf-clean", "tf-clean", "tf-be-gzip.sqsh", "tf-be-gzip.sqsh", None, "basis with escaping symlink only"),
    ("ta-v1", "ta-v1-zero-id-table", "ta-be-gzip-v1.sqsh", "ta-be-gzip.sqsh", "ta-v1-zero-id-table", "corrupt(): zero id metadata block"),
    ("tb-v1", "tb-v1-zero-id-table", "tb-be-gzip-v1.sqsh", "tb-be-gzip.sqsh", "tb-v1-zero-id-table", "corrupt(): zero id metadata block"),
    ("tc-v1", "tc-v1-zero-id-table", "tc-be-gzip-v1.sqsh", "tc-be-gzip.sqsh", "tc-v1-zero-id-table", "corrupt(): zero id metadata block"),
    ("td-v1", "td-v1", "td-be-gzip-v1.sqsh", "td-be-gzip.sqsh", "td-be-gzip-v1", "corrupt() on symlink tree"),
    ("ta-xz-v1", "ta-xz-v1", "ta-be-xz-v1.sqsh", "ta-be-xz.sqsh", "ta-be-xz-v1", "corrupt() on xz image"),
    ("ta-v2", "ta-v2-zero-first-data-block", "ta-v2-zero-first-data-block.sqsh", "ta-be-gzip.sqsh", "ta-v2-zero-first-data-block", "zero first data block (rejected)"),
    ("tb-v2", "tb-v2-zero-first-data-block", "tb-v2-zero-first-data-block.sqsh", "tb-be-gzip.sqsh", "tb-v2-zero-first-data-block", "zero first data block (rejected)"),
    ("tc-v2", "tc-v2-zero-first-data-block", "tc-v2-zero-first-data-block.sqsh", "tc-be-gzip.sqsh", "tc-v2-zero-first-data-block", "zero first data block (rejected)"),
    ("ta-v3", "ta-v3-flip-inode-table", "ta-v3-flip-inode-table.sqsh", "ta-be-gzip.sqsh", "ta-v3-flip-inode-table", "flip inode type MSB (runner-up)"),
    ("tb-v3", "tb-v3-flip-inode-table", "tb-v3-flip-inode-table.sqsh", "tb-be-gzip.sqsh", "tb-v3-flip-inode-table", "flip inode type MSB (runner-up)"),
    ("tc-v3", "tc-v3-flip-inode-table", "tc-v3-flip-inode-table.sqsh", "tc-be-gzip.sqsh", "tc-v3-flip-inode-table", "flip inode type MSB (runner-up)"),
    ("ta-v4", "ta-v4-zero-directory-table", "ta-v4-zero-directory-table.sqsh", "ta-be-gzip.sqsh", "ta-v4-zero-directory-table", "zero directory table (runner-up)"),
    ("tb-v4", "tb-v4-zero-directory-table", "tb-v4-zero-directory-table.sqsh", "tb-be-gzip.sqsh", "tb-v4-zero-directory-table", "zero directory table (runner-up)"),
    ("tc-v4", "tc-v4-zero-directory-table", "tc-v4-zero-directory-table.sqsh", "tc-be-gzip.sqsh", "tc-v4-zero-directory-table", "zero directory table (runner-up)"),
    ("ta-v5", "ta-v5-corrupt-block-length", "ta-v5-corrupt-block-length.sqsh", "ta-be-gzip.sqsh", "ta-v5-corrupt-block-length", "block length -> 2 (rejected)"),
    ("tb-v5", "tb-v5-corrupt-block-length", "tb-v5-corrupt-block-length.sqsh", "tb-be-gzip.sqsh", "tb-v5-corrupt-block-length", "block length -> 2 (rejected)"),
    ("tc-v5", "tc-v5-corrupt-block-length", "tc-v5-corrupt-block-length.sqsh", "tc-be-gzip.sqsh", "tc-v5-corrupt-block-length", "block length -> 2 (rejected)"),
    ("ta-clean-nodep", "ta-clean-nodep", "ta-be-gzip.sqsh", "ta-be-gzip.sqsh", None, "control: sasquatch-v4be unreachable on child PATH"),
    ("ta-v1-rerun", "ta-v1", "ta-be-gzip-v1.sqsh", "ta-be-gzip.sqsh", "ta-v1-zero-id-table", "repeat of ta-v1, separate REA outdir"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_sasquatch(stem):
    if stem is None:
        return None
    base = os.path.join(HERE, "sasquatch-stderr", stem)
    out = {}
    for suffix, key in ((".exit.txt", "exit"), (".stderr.txt", "stderr")):
        p = base + suffix
        if os.path.exists(p):
            out[key] = open(p, "r", errors="replace").read()
    if "stderr" in out:
        lines = [l.rstrip("\n") for l in out["stderr"].splitlines() if l.strip()]
        out["stderr_first_line"] = lines[0] if lines else ""
        out["stderr_fatal_line"] = next(
            (l for l in lines if l.startswith("FATAL ERROR")), "")
        del out["stderr"]
    if "exit" in out:
        out["exit"] = int(out["exit"].strip())
    return out


def main():
    rows = []
    for run, stem, carrier, clean, sq_stem, note in RUNS:
        env_path = os.path.join(HERE, "envelopes", stem + ".envelope.json")
        env = json.load(open(env_path))
        carrier_path = os.path.join(HERE, "inputs", carrier)
        row = {
            "run": run,
            "build": note,
            "carrier": "inputs/" + carrier,
            "carrier_sha256": sha256(carrier_path),
            "envelope": "envelopes/" + stem + ".envelope.json",
            "rea_ok": env.get("ok"),
            "features": features(env),
            "sasquatch_direct": read_sasquatch(sq_stem),
        }
        if "v1" in note or "corrupt()" in note:
            base = open(os.path.join(HERE, "inputs", clean), "rb").read()
            row["corruption_offsets"] = corrupt.describe(base)
        rows.append(row)
    matrix = {
        "wave": "round-39 w1",
        "seat": "R39C2ReconCorrupt",
        "rea": "rea-agents 6.5.0 extract-firmware --format json --full-output",
        "unblob": "26.6.4",
        "sasquatch": "sasquatch-v4be 4.5.1",
        "feature_definition": {
            "H": "normalized_result.chunks[].handler starting with squashfs",
            "G": "normalized_result.extraction_gaps[].kind",
            "D": "union of extraction_gaps[].dependencies",
            "BE": "diagnostics[].report.command naming sasquatch, '-be' standalone token",
            "SR": "MaliciousSymlinkRemoved under raw_result",
            "P": "len(normalized_result.files)",
        },
        "runs": rows,
    }
    with open(os.path.join(HERE, "run-matrix.json"), "w") as f:
        json.dump(matrix, f, indent=1, sort_keys=True)
        f.write("\n")

    hdr = ("| run | carrier sha256[:12] | H | G | D | BE | SR | P | extraction_failed | "
           "sasquatch exit | stderr first line |")
    sep = "|" + "---|" * 11
    lines = [hdr, sep]
    for r in rows:
        f = r["features"]
        sq = r["sasquatch_direct"] or {}
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["run"], r["carrier_sha256"][:12],
            ",".join(f["H"]) or "-", ",".join(f["G"]) or "-", ",".join(f["D"]) or "-",
            f["BE"], f["SR"], f["P"], f["extraction_failed"],
            sq.get("exit", "not run"),
            (sq.get("stderr_first_line") or "-").replace("|", "\\|")))
    with open(os.path.join(HERE, "feature-table.md"), "w") as f:
        f.write("# R39-C2 corruption recon — REA feature table\n\n")
        f.write("\n".join(lines) + "\n")
    print("wrote run-matrix.json (%d runs) and feature-table.md" % len(rows))


if __name__ == "__main__":
    main()
