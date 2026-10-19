#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
PROBE_PATH = ROOT / ".ufo/gates/citation-drift/citation-drift-probe.py"
TABLE_PATH = ROOT / ".ufo/gates/citation-drift/pointer-table.json"
EXPECTED_PATH = ROOT / ".ufo/gates/citation-drift/expected.json"
PATCH_PATH = Path(__file__).with_name("proposed-entries.json")
TARGETS = [
    "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
    "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
    "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
]
MUTATIONS = {
    "arc3r7-evm-recheck": (
        "TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck",
        "TMPDIR=/tmp/kaidoku-ex3-r7-recheck",
    ),
    "arc3r10-rust-recheck": ("recompute-ids.mjs", "recompute-ids-CHANGED.mjs"),
    "arc3r11-artifact-recheck": ("recompute-ids.py", "recompute-ids-CHANGED.py"),
}


def main():
    spec = importlib.util.spec_from_file_location("citation_drift_probe", PROBE_PATH)
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)

    patch_entries = json.loads(PATCH_PATH.read_text())
    table = json.loads(TABLE_PATH.read_text())
    original_ids = {entry.get("id") for entry in table.get("entries", [])}
    if any(entry["id"] in original_ids for entry in patch_entries):
        raise SystemExit("patch IDs already exist in the live table")
    table["entries"].extend(patch_entries)
    table_bytes = (json.dumps(table, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    expected = json.loads(EXPECTED_PATH.read_text())
    expected["pointer_table"]["sha256"] = hashlib.sha256(table_bytes).hexdigest()

    original_git_show = probe.git_show
    originals = {
        path: original_git_show(str(ROOT), "HEAD", path)[0]
        for path in TARGETS
    }
    if any(text is None for text in originals.values()):
        raise SystemExit("one or more corpus entries are absent at HEAD")

    with tempfile.TemporaryDirectory(prefix="rv4-recheck-", dir="/var/tmp") as scratch:
        scratch = Path(scratch)
        scratch_table = scratch / "pointer-table.json"
        scratch_expected = scratch / "expected.json"
        scratch_table.write_bytes(table_bytes)
        scratch_expected.write_text(json.dumps(expected, ensure_ascii=False, indent=2) + "\n")

        def evaluate(label, overlay, expected_id=None):
            def git_show(root, rev, path):
                if path in overlay:
                    return overlay[path], None
                return original_git_show(root, rev, path)

            probe.git_show = git_show
            findings = probe.run_check(
                str(ROOT), "HEAD", str(scratch_table), str(scratch_expected), None
            )
            code = findings.verdict(strict=True)
            ids = findings.ids()
            if expected_id is None:
                valid = code == 0 and not findings.rows
            else:
                valid = code == 1 and ids == {"citation_dead"} and any(
                    row[1] == expected_id for row in findings.rows
                )
            if not valid:
                raise SystemExit(
                    f"{label}: unexpected exit={code}, findings={findings.rows!r}"
                )
            details = "; ".join(f"{kind} entry={entry}" for kind, entry, _ in findings.rows)
            if not details:
                details = "no findings"
            print(f"{label}: {details}; strict_exit={code}")

        evaluate("CONTROL", originals)
        by_id = {entry["id"]: entry for entry in patch_entries}
        for entry_id, (before, after) in MUTATIONS.items():
            entry = by_id[entry_id]
            path = entry["file"]
            lines = originals[path].splitlines(keepends=True)
            line_index = entry["line"] - 1
            if lines[line_index].count(before) != 1:
                raise SystemExit(f"{entry_id}: expected one mutation needle on {path}:{entry['line']}")
            lines[line_index] = lines[line_index].replace(before, after, 1)
            overlay = dict(originals)
            overlay[path] = "".join(lines)
            evaluate(f"SEEDED {entry_id}", overlay, entry_id)
    probe.git_show = original_git_show
    print(f"SCRATCH: /var/tmp only; no Git writes; live instrument/table/expected unchanged")


if __name__ == "__main__":
    main()
