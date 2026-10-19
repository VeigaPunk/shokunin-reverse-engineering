#!/usr/bin/env python3
"""Run citation-drift's proposed recheck rows against a scratch overlay.

The gate source and all unmutated target files come from the current HEAD Git
objects. The scratch overlay changes exactly one recheck line; no Git command
writes objects or refs and no live instrument or custody path is modified.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

DOCS = {
    "r7": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
    "r10": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
    "r11": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
}
GATE = ".ufo/gates/citation-drift/citation-drift-probe.py"
TABLE = ".ufo/gates/citation-drift/pointer-table.json"
EXPECTED = ".ufo/gates/citation-drift/expected.json"

NEW_ROWS = [
    {
        "id": "rv3-r7-evm-recheck",
        "kind": "exact",
        "file": DOCS["r7"],
        "line": 5,
        "must_match": r"^recheck: .*TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*inspect-evm-interface.*--format json",
        "note": "Grade the R7 entry's recheck command, disk-backed scratch requirement and operation."
    },
    {
        "id": "rv3-r10-rust-recheck",
        "kind": "exact",
        "file": DOCS["r10"],
        "line": 7,
        "must_match": r"^recheck: .*rederive-commands\.txt.*recompute-ids\.mjs.*read-only",
        "note": "Grade the R10 entry's command record, independent Evidence-ID recomputation and read-only scope.",
    },
    {
        "id": "rv3-r11-inspect-artifact-recheck",
        "kind": "exact",
        "file": DOCS["r11"],
        "line": 7,
        "must_match": r"^recheck: .*TMPDIR.*calls\.txt.*recompute-ids\.py.*Do not use.*scratch",
        "note": "Grade the R11 entry's disk-backed scratch instruction, exact calls, recomputation and /tmp exclusion.",
    },
]


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True)


def git_show(root: Path, rev: str, path: str) -> str:
    return git(root, "show", f"{rev}:{path}")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: seeded-fault.py REPOSITORY_ROOT")
    repo = Path(sys.argv[1]).resolve()
    rev = git(repo, "rev-parse", "HEAD").strip()
    gate_source = git_show(repo, rev, GATE)
    table = json.loads(git_show(repo, rev, TABLE))
    expected = json.loads(git_show(repo, rev, EXPECTED))
    table["entries"].extend(NEW_ROWS)

    with tempfile.TemporaryDirectory(prefix="kaidoku-rv3-citation-", dir="/var/tmp") as tmp:
        scratch = Path(tmp)
        scratch_gate = scratch / "citation-drift-probe.py"
        scratch_gate.write_text(gate_source, encoding="utf-8")
        scratch_table = scratch / "pointer-table.json"
        table_bytes = (json.dumps(table, indent=2, ensure_ascii=True) + "\n").encode()
        scratch_table.write_bytes(table_bytes)
        expected.setdefault("pointer_table", {})["sha256"] = hashlib.sha256(table_bytes).hexdigest()
        scratch_expected = scratch / "expected.json"
        scratch_expected.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")

        overlay = scratch / "overlay"
        for path in DOCS.values():
            target = overlay / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(git_show(repo, rev, path), encoding="utf-8")

        spec = importlib.util.spec_from_file_location("rv3_citation_drift", scratch_gate)
        if spec is None or spec.loader is None:
            raise RuntimeError("cannot load scratch copy of citation-drift gate")
        gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate)
        original_git_show = gate.git_show

        def overlay_git_show(root: str, requested_rev: str, path: str):
            candidate = overlay / path
            if candidate.is_file():
                return candidate.read_text(encoding="utf-8"), None
            return original_git_show(root, requested_rev, path)

        gate.git_show = overlay_git_show
        total = len(table.get("entries", [])) + len(table.get("quoted", []))
        print(f"REVISION: {rev}")
        print(f"PATCH_TABLE: entries={len(table['entries'])} quoted={len(table.get('quoted', []))} total={total} sha256={hashlib.sha256(table_bytes).hexdigest()}")

        baseline = gate.run_check(str(repo), rev, str(scratch_table), str(scratch_expected), None)
        baseline_exit = baseline.verdict(strict=True)
        print(f"SCRATCH_BASELINE: verdict={'clean' if baseline_exit == 0 else 'failed' if baseline_exit == 1 else 'could-not-evaluate'} findings={len(baseline.rows)} exit={baseline_exit}")
        if baseline_exit != 0 or baseline.rows:
            for finding, entry, detail in baseline.rows:
                print(f"BASELINE_FINDING: {finding} entry={entry} {detail}")
            return 1

        r11 = overlay / DOCS["r11"]
        lines = r11.read_text(encoding="utf-8").splitlines()
        line_no = NEW_ROWS[2]["line"]
        original = lines[line_no - 1]
        if "recompute-ids.py" not in original:
            raise RuntimeError("R11 scratch fault seed no longer matches its source line")
        lines[line_no - 1] = original.replace("recompute-ids.py", "recompute-ids.txt", 1)
        r11.write_text("\n".join(lines) + "\n", encoding="utf-8")

        faulted = gate.run_check(str(repo), rev, str(scratch_table), str(scratch_expected), None)
        fault_exit = faulted.verdict(strict=True)
        fault_ids = sorted(faulted.ids())
        print(f"SEEDED_FAULT: {DOCS['r11']}:{line_no} recompute-ids.py -> recompute-ids.txt")
        for finding, entry, detail in faulted.rows:
            print(f"FAULT_FINDING: {finding} entry={entry} {detail}")
        print(f"SCRATCH_FAULT: verdict={'clean' if fault_exit == 0 else 'failed' if fault_exit == 1 else 'could-not-evaluate'} findings={len(faulted.rows)} ids={fault_ids} exit={fault_exit}")
        expected_id = "rv3-r11-inspect-artifact-recheck"
        if fault_exit != 1 or fault_ids != ["citation_dead"] or not any(row[1] == expected_id for row in faulted.rows):
            return 1
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
