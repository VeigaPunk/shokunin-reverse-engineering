# RV-6 — citation-drift coverage for `ev_` rechecks

## Scope and verdict

C3 candidate (a): extend the citation-drift pointer table to grade the `recheck:` fields of the three recently added Evidence-ID entries. **VERIFIED gap; patch text prepared, not applied to the instrument.** I changed no gate, custody path, corpus entry, or tracked file. The scratch measurement uses the actual probe functions with a read-only Git-object overlay; it makes no Git mutations.

## First-hand re-derivation at HEAD

`git log -1 --format='%H %s'` returned:

```text
0436f4940283072db08e73c0117195847c50d31d arc3-loop1-round11: records — SCORECARD round section, LOG entry, round report + scope re-key to EOF (measured at work commit 5ee13b3)
```

The source fields are present in the committed files at:

- `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5` — `inspect-evm-interface` recheck command, expected `ev_…` ID, and disk-backed `/var/tmp` requirement.
- `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7` — REA command source `evidence/rederive-commands.txt` plus `recompute-ids.mjs` projection/path-field check.
- `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7` — pinned identity, `/var/tmp`, recorded calls, `recompute-ids.py`, and `/tmp` exclusion.

Command and output for the pointer-table coverage count:

```text
$ python3 - <<'PY'
import json
p='.ufo/gates/citation-drift/pointer-table.json'
t=json.load(open(p))
paths=[
 'corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md',
 'corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md',
 'corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md',
]
print(f'entry_rows={len(t["entries"])}')
for path in paths:
 rows=[r for key in ('entries','quoted') for r in t.get(key,[]) if r.get('file')==path or r.get('target')==path]
 print(f'{path}: recheck-grade-rows={len(rows)} ids={[r.get("id") for r in rows]}')
PY
entry_rows=57
corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md: recheck-grade-rows=0 ids=[]
corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md: recheck-grade-rows=0 ids=[]
corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md: recheck-grade-rows=0 ids=[]
```

Baseline instrument command and output:

```text
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --rev HEAD --strict
CITATION_DRIFT_ROOT: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

The clean result is consistent with the measured blind spot: none of those three source files is read by the existing 57-entry table.

## Patch text (proposed only)

Append these three objects to `entries` in `.ufo/gates/citation-drift/pointer-table.json` (before the `quoted` array). `anchor` plus `pin_line` grades both the recheck field's content and its current location; a missing/changed field becomes `citation_dead`, and a moved field becomes `citation_moved`.

```json
{
  "id": "r7-evm-entry-recheck",
  "kind": "anchor",
  "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
  "pin_line": 5,
  "must_match": "^recheck: .*TMPDIR=/var/tmp/.*inspect-evm-interface .*--format json.*ev_[0-9a-f]{64}.*disk-backed here\\.$",
  "note": "Grades the entry recheck command, its expected Evidence ID, and the host-specific disk-backed scratch requirement."
},
{
  "id": "r10-rust-entry-recheck",
  "kind": "anchor",
  "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
  "pin_line": 7,
  "must_match": "^recheck: .*evidence/rederive-commands\\.txt.*recompute-ids\\.mjs.*semantic projection ID.*path-bearing fields.*",
  "note": "Grades the recheck command source and the independent projection/path-field recomputation it names."
},
{
  "id": "r11-artifact-entry-recheck",
  "kind": "anchor",
  "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
  "pin_line": 7,
  "must_match": "^recheck: .*identity\\.txt.*TMPDIR.*directory under `/var/tmp`.*calls\\.txt.*recompute-ids\\.py.*Do not use `/tmp` for scratch\\.$",
  "note": "Grades the pinned package identity, disk-backed scratch, recorded calls, ID recomputation, and /tmp exclusion."
}
```

Re-serialize the table using its existing two-space JSON formatting and update only `pointer_table.sha256` in `.ufo/gates/citation-drift/expected.json` in the same change. First-hand scratch serialization measured 60 entries and this table digest:

```text
2187f361403c9c13d861b41c210ab2e8c123c77203020c53c64aa2a55d7f0602
```

This hash is for the exact proposed rows above appended to the current table; the re-pin must be recomputed if the table bytes or rows change.

## Seeded-fault measurement

Reproducer: `.ufo/waves/arc3-loop1-round12/claims/c3/RV-6/seeded-fault.py`; command:

```text
python3 .ufo/waves/arc3-loop1-round12/claims/c3/RV-6/seeded-fault.py
```

It writes the candidate table and expected pin only inside a `TemporaryDirectory` under `/var/tmp`. To preserve the read-only Git requirement, a `git_show` overlay substitutes one source line in memory; no repository object, source, or instrument is edited. It then calls the shipped `run_check` and `report` functions with the unmodified baseline table and with the proposed table.

Clean candidate result:

```text
BASELINE_TABLE_ENTRIES: 57
BASELINE_RECHECK_ROWS: r7=0 r10=0 r11=0
PATCH_TABLE_ENTRIES: 60
PATCH_POINTER_TABLE_SHA256: 2187f361403c9c13d861b41c210ab2e8c123c77203020c53c64aa2a55d7f0602
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

Each seed was applied separately to its source `recheck:` line. In all three baseline cases, the table made zero reads of the seeded file and returned `clean findings=0 exit=0`. With the proposed row, the source was read once and the actual probe returned one `citation_dead`, exit 1:

| Seed | Scratch overlay | Baseline | Proposed table |
|---|---|---|---|
| r7, line 5 | `TMPDIR=/var/tmp/` → `TMPDIR=/tmp/` | `BASELINE_READS: 0`; `clean findings=0 exit=0` | `citation_dead entry=r7-evm-entry-recheck`; `failed findings=1 exit=1` |
| r10, line 7 | `evidence/rederive-commands.txt` → `evidence/missing-rederive-commands.txt` | `BASELINE_READS: 0`; `clean findings=0 exit=0` | `citation_dead entry=r10-rust-entry-recheck`; `failed findings=1 exit=1` |
| r11, line 7 | changed source text “directory under /var/tmp” to “directory under /tmp” (source paths are Markdown-backticked) | `BASELINE_READS: 0`; `clean findings=0 exit=0` | `citation_dead entry=r11-artifact-entry-recheck`; `failed findings=1 exit=1` |

Full first-hand run output is reproducible with the command above; the measured output includes the exact finding IDs and verdicts. No scratch path is used as a durable evidence pointer.

## Per-item verdicts and limits

- **VERIFIED — r7 recheck coverage:** source line `:5` is present; baseline table has zero rows for this file; `/tmp` substitution is silent on baseline and `citation_dead` under the proposed row.
- **VERIFIED — r10 recheck coverage:** source line `:7` is present; baseline table has zero rows; missing-command-source substitution is silent on baseline and detected by the proposed row.
- **VERIFIED — r11 recheck coverage:** source line `:7` is present; baseline table has zero rows; scratch-path substitution is silent on baseline and detected by the proposed row.
- **REPRODUCED — proposed instrument delta:** clean table remains clean (0 findings); each one-line fault changes from baseline clean/zero source reads to one `citation_dead`/exit 1.

This is textual drift coverage, not command execution or a gate that verifies the referenced evidence files exist or recomputes Evidence IDs. The proposed rows only grade the specified recheck contract cues. The probe and custody tool remain untouched as required.
