import contextlib
import hashlib
import importlib.util
import io
import json
import tempfile
from pathlib import Path

repo = Path.cwd().resolve()
probe_file = repo / ".ufo/gates/citation-drift/citation-drift-probe.py"
table_file = repo / ".ufo/gates/citation-drift/pointer-table.json"
expected_file = repo / ".ufo/gates/citation-drift/expected.json"
spec = importlib.util.spec_from_file_location("citation_drift_probe", probe_file)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

paths = {
    "r7": ("corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md", 5),
    "r10": ("corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md", 7),
    "r11": ("corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md", 7),
}
rows = [
    {
        "id": "r7-evm-entry-recheck",
        "kind": "anchor",
        "file": paths["r7"][0],
        "pin_line": 5,
        "must_match": r"^recheck: .*TMPDIR=/var/tmp/.*inspect-evm-interface .*--format json.*ev_[0-9a-f]{64}.*disk-backed here\.$",
        "note": "Grades the entry recheck command, its expected Evidence ID, and the host-specific disk-backed scratch requirement.",
    },
    {
        "id": "r10-rust-entry-recheck",
        "kind": "anchor",
        "file": paths["r10"][0],
        "pin_line": 7,
        "must_match": r"^recheck: .*evidence/rederive-commands\.txt.*recompute-ids\.mjs.*semantic projection ID.*path-bearing fields.*",
        "note": "Grades the recheck command source and the independent projection/path-field recomputation it names.",
    },
    {
        "id": "r11-artifact-entry-recheck",
        "kind": "anchor",
        "file": paths["r11"][0],
        "pin_line": 7,
        "must_match": r"^recheck: .*identity\.txt.*TMPDIR.*directory under `/var/tmp`.*calls\.txt.*recompute-ids\.py.*Do not use `/tmp` for scratch\.$",
        "note": "Grades the pinned package identity, disk-backed scratch, recorded calls, ID recomputation, and /tmp exclusion.",
    },
]

base_table_bytes = table_file.read_bytes()
base_table = json.loads(base_table_bytes)
base_expected = json.loads(expected_file.read_text())
print(f"BASELINE_TABLE_ENTRIES: {len(base_table['entries'])}")
print("BASELINE_RECHECK_ROWS: r7=0 r10=0 r11=0")
base_table["entries"].extend(rows)
candidate_bytes = (json.dumps(base_table, indent=2, ensure_ascii=True) + "\n").encode()
candidate_expected = dict(base_expected)
candidate_expected["pointer_table"] = dict(base_expected["pointer_table"])
candidate_expected["pointer_table"]["sha256"] = hashlib.sha256(candidate_bytes).hexdigest()
print(f"PATCH_TABLE_ENTRIES: {len(base_table['entries'])}")
print(f"PATCH_POINTER_TABLE_SHA256: {candidate_expected['pointer_table']['sha256']}")

with tempfile.TemporaryDirectory(prefix="rv6-citation-drift-", dir="/var/tmp") as scratch:
    scratch = Path(scratch)
    candidate_table = scratch / "pointer-table.json"
    candidate_expected_file = scratch / "expected.json"
    candidate_table.write_bytes(candidate_bytes)
    candidate_expected_file.write_text(json.dumps(candidate_expected, indent=2) + "\n")
    real_git_show = probe.git_show

    def emit(label, findings, table_path):
        print(label)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            probe.report(repo.as_posix(), "HEAD", str(table_path), findings, strict=True)
        print(output.getvalue(), end="")

    probe.git_show = real_git_show
    clean = probe.run_check(repo.as_posix(), "HEAD", str(candidate_table),
                            str(candidate_expected_file), None)
    emit("PATCH_CLEAN:", clean, candidate_table)

    cases = [
        ("r7", "TMPDIR=/var/tmp/", "TMPDIR=/tmp/"),
        ("r10", "evidence/rederive-commands.txt",
         "evidence/missing-rederive-commands.txt"),
        ("r11", "directory under `/var/tmp`", "directory under `/tmp`"),
    ]
    for label, old, new in cases:
        target, line_number = paths[label]
        source, error = real_git_show(repo.as_posix(), "HEAD", target)
        assert error is None
        original_line = source.splitlines()[line_number - 1]
        assert old in original_line
        seeded_line = original_line.replace(old, new, 1)
        state = {"reads": 0}

        def overlay(root, rev, path, *, target=target, line_number=line_number,
                    seeded_line=seeded_line, state=state):
            text, error = real_git_show(root, rev, path)
            if path == target and text is not None:
                lines = text.splitlines()
                lines[line_number - 1] = seeded_line
                state["reads"] += 1
                return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), None
            return text, error

        probe.git_show = overlay
        baseline = probe.run_check(repo.as_posix(), "HEAD", str(table_file),
                                   str(expected_file), None)
        print(f"SEED: {label} {target}:{line_number} changed={old!r}->{new!r}")
        print(f"BASELINE_READS: {state['reads']} (target is not referenced by table)")
        emit("BASELINE_FAULT:", baseline, table_file)
        state["reads"] = 0
        patched = probe.run_check(repo.as_posix(), "HEAD", str(candidate_table),
                                  str(candidate_expected_file), None)
        print(f"PATCH_OVERLAY_APPLIED: {str(state['reads'] == 1).lower()} reads={state['reads']}")
        emit("PATCH_FAULT:", patched, candidate_table)

    probe.git_show = real_git_show
