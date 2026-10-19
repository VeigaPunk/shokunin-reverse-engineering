#!/usr/bin/env python3
"""C3 seeded-fault measurement for the applied PL-4 pointer-table rows.

The live table now carries the three pl4-* recheck rows (uncommitted worktree
edit), so the probe cannot be run plain against it: cited files resolve via
`git show <rev>:<path>`, and while the three corpus files are unchanged at
HEAD, a faithful seeded measurement overlays the mutations in memory instead
of touching any repository file.

This script imports the real probe module, shims `git_show` for the three
corpus paths only (everything else delegates to the real HEAD lookup), copies
the live patched table + expected.json into /var/tmp scratch, then:

  1. CONTROL   - clean overlay of the three recheck lines -> exit 0
  2. SEEDED x3 - exactly one mutated recheck line per run -> exactly one
                 `citation_dead` for that row's id, strict exit 1

Mutations (one per run, non-cumulative):
  pl4-r7-recheck : TMPDIR=/var/tmp/... -> TMPDIR=/tmp/... (scratch-dir change)
  pl4-r10-recheck: evidence/rederive-commands.txt -> evidence/rederive-commands-missing.txt
  pl4-r11-recheck: recompute-ids.py -> recompute-ids-CHANGED.py
"""
import hashlib
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
PROBE_PATH = ROOT / ".ufo/gates/citation-drift/citation-drift-probe.py"
TABLE_PATH = ROOT / ".ufo/gates/citation-drift/pointer-table.json"
EXPECTED_PATH = ROOT / ".ufo/gates/citation-drift/expected.json"

TARGETS = [
    "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
    "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
    "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
]

# entry id -> (file, needle, replacement) applied to that file's cited line
MUTATIONS = {
    "pl4-r7-recheck": (
        TARGETS[0], 5,
        "TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck",
        "TMPDIR=/tmp/kaidoku-ex3-r7-recheck",
    ),
    "pl4-r10-recheck": (
        TARGETS[1], 7,
        "evidence/rederive-commands.txt",
        "evidence/rederive-commands-missing.txt",
    ),
    "pl4-r11-recheck": (
        TARGETS[2], 7,
        "recompute-ids.py",
        "recompute-ids-CHANGED.py",
    ),
}


def main():
    spec = importlib.util.spec_from_file_location("citation_drift_probe",
                                                  PROBE_PATH)
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)

    table_bytes = TABLE_PATH.read_bytes()
    table = json.loads(table_bytes)
    print("TABLE entries=%d quoted=%d exempt=%d sha256=%s"
          % (len(table["entries"]), len(table["quoted"]),
             len(table["exempt"]), hashlib.sha256(table_bytes).hexdigest()))

    original_git_show = probe.git_show
    originals = {p: original_git_show(str(ROOT), "HEAD", p)[0] for p in TARGETS}
    if any(t is None for t in originals.values()):
        raise SystemExit("one or more corpus entries are absent at HEAD")

    with tempfile.TemporaryDirectory(prefix="r12-c3-", dir="/var/tmp") as scr:
        scr = Path(scr)
        scratch_table = scr / "pointer-table.json"
        scratch_expected = scr / "expected.json"
        shutil.copyfile(TABLE_PATH, scratch_table)
        shutil.copyfile(EXPECTED_PATH, scratch_expected)

        def evaluate(label, overlay, expected_id=None):
            def git_show(root, rev, path):
                if path in overlay:
                    return overlay[path], None
                return original_git_show(root, rev, path)

            probe.git_show = git_show
            findings = probe.run_check(str(ROOT), "HEAD", str(scratch_table),
                                       str(scratch_expected), None)
            code = findings.verdict(strict=True)
            for finding, entry, detail in findings.rows:
                print("CITATION_DRIFT: %s entry=%s %s" % (finding, entry, detail))
            print("%s: findings=%d strict_exit=%d" % (label, len(findings.rows), code))
            if expected_id is None:
                ok = code == 0 and not findings.rows
            else:
                ok = (code == 1 and len(findings.rows) == 1
                      and findings.rows[0][0] == "citation_dead"
                      and findings.rows[0][1] == expected_id)
            if not ok:
                raise SystemExit("%s: unexpected rows=%r exit=%d"
                                 % (label, findings.rows, code))

        evaluate("CONTROL", originals)
        for entry_id, (path, line_no, needle, replacement) in MUTATIONS.items():
            lines = originals[path].splitlines(keepends=True)
            if lines[line_no - 1].count(needle) != 1:
                raise SystemExit("%s: needle not unique on %s:%d"
                                 % (entry_id, path, line_no))
            lines[line_no - 1] = lines[line_no - 1].replace(needle, replacement, 1)
            overlay = dict(originals)
            overlay[path] = "".join(lines)
            evaluate("SEEDED %s" % entry_id, overlay, entry_id)

    probe.git_show = original_git_show
    print("SCRATCH: /var/tmp only; no Git writes; no worktree writes")


if __name__ == "__main__":
    main()
