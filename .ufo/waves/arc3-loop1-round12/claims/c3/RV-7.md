# RV-7 — citation-drift coverage for corpus `recheck:` lines

Claim: C3 operability, improve an instrument. Scope chosen: extend the citation-drift pointer table to grade the `recheck:` lines in the new r7/r10/r11 `ev_` corpus entries. This is a patch proposal only; no gate, expected file, corpus entry, or other tracked file was edited.

## First-hand measurements

`git rev-parse HEAD` returned:

```text
0436f4940283072db08e73c0117195847c50d31d
```

I loaded the three source entries and the current pointer table from `HEAD` with read-only `git show`, found each first line beginning `recheck:`, and counted pointer-table rows with the same `file` and `line`:

```text
BASELINE_RECHECK: corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5 graded_rows=0 ids=[]
BASELINE_RECHECK: corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7 graded_rows=0 ids=[]
BASELINE_RECHECK: corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7 graded_rows=0 ids=[]
```

Thus 3/3 of these `recheck:` lines have no table row grading them at this revision. The line numbers and contents are independently visible at r7 entry `:5`, r10 entry `:7`, and r11 entry `:7`. The pointer table currently has no corresponding citation rows; its existing `entries` and grading semantics are in `.ufo/gates/citation-drift/pointer-table.json` and `.ufo/gates/citation-drift/citation-drift-probe.py:168-211`.

The unmodified probe was run against immutable `HEAD`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 .ufo/gates/citation-drift/citation-drift-probe.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev HEAD --snapshot-dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift --strict
```

Exact result:

```text
CITATION_DRIFT_ROOT: /home/vgpnk/Projects/shokunin/kaidoku-shokunin
CITATION_DRIFT_REVISION: HEAD
CITATION_DRIFT_TABLE: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/citation-drift/pointer-table.json
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
SHELL_EXIT=0
```

Verdict: **REPRODUCED** — this clean baseline is consistent with the static gap: no finding is possible for the three currently unregistered recheck lines.

## Patch text (not applied)

Append these objects to `.ufo/gates/citation-drift/pointer-table.json`'s `entries` array:

```json
{
  "id": "rv7-recheck-r7-evm",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md",
  "line": 5,
  "must_match": "TMPDIR=/var/tmp/kaidoku-ex3-r7-recheck.*inspect-evm-interface",
  "note": "The r7 recheck pins its REA verb and the required disk-backed TMPDIR."
},
{
  "id": "rv7-recheck-r10-rust",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md",
  "line": 7,
  "must_match": "recompute-ids\\.mjs",
  "note": "The r10 recheck names the independent semantic Evidence-ID recomputation script."
},
{
  "id": "rv7-recheck-r11-artifact",
  "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md",
  "line": 7,
  "must_match": "TMPDIR.*under `/var/tmp`.*calls\\.txt.*recompute-ids\\.py",
  "note": "The r11 recheck pins its disk-backed scratch instruction, exact calls list, and ID recomputation."
}
```

In `.ufo/gates/citation-drift/expected.json`, replace the current `pointer_table.sha256` (`1b3ab955478b5d40f428d733bc482e4037f83bceaa1a39e9046ef82ca6d42d4b`) with:

```text
4249f2727c9c0e8c4313d85b292adb7f280bacca7a7338c748aed6e70f2dbce2
```

That new digest was computed over the complete current pointer table plus these exact objects, serialized as two-space-indented JSON with a final newline. Any integration should recompute it from the landed bytes. The existing frozen-run guard checks this pin before grading entries (`citation-drift-probe.py:294-319`).

## Scratch verification

I used `/var/tmp/kaidoku-rv7-c3-final.117KiH/` only. The scratch pointer table included the proposed three entries and its scratch `expected.json` pinned the new table digest. Running the real probe source against `HEAD` with these scratch inputs yielded:

```text
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
PATCH_CLEAN_EXIT=0
```

For the seeded fault, I changed only the r11 scratch copy's phrase `under `/var/tmp`` to `under `/tmp``. A transparent PATH shim supplied that modified file only for the probe's `git show HEAD:<r11-path>` request and delegated all other Git commands to the real Git executable; no Git object or repository file was changed. The real probe then reported:

```text
CITATION_DRIFT: citation_dead entry=rv7-recheck-r11-artifact corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7 lacks 'TMPDIR.*under `/var/tmp`.*calls\\.txt.*recompute-ids\\.py'
CITATION_DRIFT_VERDICT: failed findings=1 exit=1
SEEDED_FAULT_EXIT=1
```

Verdict: **REPRODUCED** — the added entries accept the current source and flag this seeded loss of the declared disk-backed scratch requirement. The scratch patch table's SHA-256 was `4249f2727c9c0e8c4313d85b292adb7f280bacca7a7338c748aed6e70f2dbce2`.

## Boundaries and verdicts

- **VERIFIED** — `HEAD` is `0436f4940283072db08e73c0117195847c50d31d`.
- **REPRODUCED** — 3/3 named `recheck:` lines have zero grading rows at `HEAD`; the exact line references are given above.
- **REPRODUCED** — the original probe reports `clean findings=0 exit=0`; the scratch patch is clean, and the r11 seeded fault becomes `citation_dead` with strict exit 1.
- **UNVERIFIABLE** — this does not establish that any referenced REA cache, fixture, command, or output is live or that the recheck instructions execute successfully. The proposal grades selected text on each `recheck:` line; it is not a general `recheck:` parser or command runner.
- The instrument's built-in `--selftest` was not run: the source constructs default `tempfile` directories at `.ufo/gates/citation-drift/citation-drift-probe.py:349,416`, which would use the prohibited `/tmp` scratch location. The actual CLI baseline and seeded-fault paths above were exercised instead.
- No custody path was opened. No instrument, expected file, pointer table, corpus, province, skill, scorecard, or log was changed.
