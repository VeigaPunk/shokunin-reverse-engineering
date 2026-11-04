#!/usr/bin/env python3
"""Round-78 seat RevengerInstruments: the honest limit set, measured.

Two probes the acceptance table cannot show:

  1. a named receipt that its own `--validate` rejects, but whose fields match
     the cell, is accepted by both the round-77 binder and the round-78 gate's
     record scan (neither re-validates the named receipt);
  2. the scope numbers: how many clauses the round-77 binder binds versus how
     many the round-78 gate's record scan binds on the same committed record.

Every byte is read at a named revision; fixture repos live under --work.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from probe import (  # noqa: E402
    GATE, INSTRUMENTS, Fatal, child_env, commit_all, git, git_blob,
    load_gate, sha256_bytes,
)


def run(argv, work):
    return subprocess.run(argv, capture_output=True, text=True,
                          env=child_env(work), cwd=work)


def self_contradicting_receipt(lane: pathlib.Path, work: pathlib.Path,
                               gate_rev: str) -> dict:
    gate = load_gate(lane, gate_rev, work)
    demo = pathlib.Path(work, "demo-limits")
    if demo.exists():
        import shutil
        shutil.rmtree(demo)
    scores = ".ufo/waves/round-78/l1/scores"
    (demo / scores).mkdir(parents=True)
    (demo / "tools/round-77").mkdir(parents=True)
    (demo / "SCORECARD.md").write_text(
        "# demo scorecard\n\n## Capabilities\n\n"
        "| Capability | What it can now do | Evidence pointer | "
        "First-working round |\n|---|---|---|---|\n")
    (demo / "PROVINCE.md").write_text(
        "# demo province\n\n## Core\n\n"
        "- **Core — demo:** `.ufo/waves/round-78/l1/scores/bad.json` records "
        "the verdict (D24 true, mismatch_count 9).\n")
    instrument_blob = pathlib.Path(lane, INSTRUMENTS["verdict-bind"]).read_bytes()
    (demo / INSTRUMENTS["verdict-bind"]).write_bytes(instrument_blob)
    # internally impossible: cells [] but bound_clauses 2, mismatch_count 9 with
    # defects [], ok false, validate.defects ["x"] -- its own validate rejects it
    bad = {
        "schema": "kaidoku-r77-verdict-bind-v1",
        "rev": "0" * 40,
        "instrument": {"path": INSTRUMENTS["verdict-bind"],
                       "sha256": sha256_bytes(instrument_blob)},
        "atoms": [{"id": "D24_capability_rows", "ok": True}],
        "mismatch_count": 9, "defects": [], "ok": False,
        "cells": [], "population": {"bound_clauses": 2},
        "validate": {"defects": ["x"], "bound_clauses": 2},
    }
    (demo / scores / "bad.json").write_text(json.dumps(bad, indent=1) + "\n")
    rev = commit_all(demo, "demo: a self-contradicting named receipt", work)
    bad["rev"] = rev
    (demo / scores / "bad.json").write_text(json.dumps(bad, indent=1) + "\n")
    rev = commit_all(demo, "demo: pin the receipt to its own revision", work)

    vb = pathlib.Path(lane, INSTRUMENTS["verdict-bind"]).resolve()
    out = pathlib.Path(work, "limits", "vb.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    run_vb = run([sys.executable, "-I", "-B", str(vb), "--root", str(demo),
                  "--rev", rev, "--json-out", str(out)], work)
    audit = json.loads(out.read_text()) if out.is_file() else {}
    validate = run([sys.executable, "-I", "-B", str(vb),
                    "--validate", str(demo / scores / "bad.json")], work)
    scan = gate.scan_record(str(demo), rev,
                            {"receipt_auth", "value_mismatch",
                             "unbound_verdict", "qualified_atom",
                             "near_miss_field", "negated_verdict"})
    return {
        "named_receipt": bad,
        "receipt_validate_verdict": {
            "exit": validate.returncode,
            "defects": json.loads(validate.stdout)["defects"]},
        "verdict_bind_audit": {
            "exit": run_vb.returncode,
            "mismatch_count": audit.get("mismatch_count"),
            "bound_clauses": (audit.get("population") or {}).get(
                "bound_clauses"),
            "defects": audit.get("defects")},
        "round78_scan_record": {
            k: scan[k] for k in ("bound_clauses", "mismatch_count", "findings")},
        "neither_validates_the_named_receipt": (
            validate.returncode == 1 and run_vb.returncode == 0
            and not scan["findings"]),
        "demo_rev": rev,
    }


def main() -> int:
    lane = pathlib.Path(sys.argv[1]).resolve()
    work = pathlib.Path(sys.argv[2]).resolve()
    gate_rev = sys.argv[3]
    out_path = pathlib.Path(sys.argv[4])
    work.mkdir(parents=True, exist_ok=True)
    try:
        data = self_contradicting_receipt(lane, work, gate_rev)
    except Fatal as exc:
        print(json.dumps({"fatal": str(exc)}))
        return 2
    out_path.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: data[k] for k in
                      ("neither_validates_the_named_receipt",)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
