# ControlsRun — wave-2 FALSIFY report (controls sweep)

Seat: `KaidokuR17.ControlsRun`. Target revisions: BEFORE `b563c799d97774aae4351276fe43cb897311e349`, AFTER `da64646adcb19c1ede7537b799b8c7d283fe43da`.

## Command run

`python3 -I -B .ufo/waves/round-17/controls.py b563c79… da64646…` → exit 0, stdout saved verbatim to `.ufo/waves/round-17/w2/controls.json` (45,527 lines, parsed cleanly as JSON; `invocation.isolated: true`, `conformance_gate: false`, resolved revisions match inputs).

## Non-clean controls — verdicts

All non-clean report fields verified against `git diff` of the two revisions; none is a real harm:

| Control | Observation | Verdict |
|---|---|---|
| `log_old_prefix.LOG.md` | `byte_identical: false`, `prefix_preserved: true`, `appended_bytes: 2627` | Permitted. `git diff` shows a single pure-append hunk at file tail (round-17 entry). |
| `sources_registry.allowed_used_by_deltas` | S003 and S023 changed only at cell index 11 (used-by) | Permitted per CORPUS contract rule 2; both AFTER cells are the BEFORE cell plus appended entries (pure append). |
| `sources_registry.added_rows` | S024–S030 (7 new rows) | Permitted; registry growth by new S-ids is the design (`added_rows` reported, never rejected). |
| `quality_admission_rows.added_rows` | rows `19`, `20` added; `prior_rows_byte_identical: true`, `violations: {}` | Permitted; rows 1–18 byte-identical (verified in QUALITY.md diff: two `+` lines only). |

Clean controls: `old_lessons_prefix` 20/20, `old_knowledge_prefix` 94/94, `prior_verifiers_unchanged` 5/5, `prior_wave_evidence_blobs` 14,943/14,943 + `quote_script_unchanged: true`, `craft` identical sha256 `e12b60ce…` / 17 rule_blocks / 17 citation_resolved_rules at both revisions, `sources_registry.immutable_cells_unchanged: true`.

## Defects found

1. **Stale docstring (cosmetic) — `.ufo/waves/round-17/controls.py:23-24`**: says "r17 fixes rows 1-18 and appends row 19"; the actual diff appends rows **19 and 20** (LOG.md round-17 entry documents "QUALITY #19/#20"; `corpus/lessons/round-17.md` + knowledge file ground row 20). Same staleness in `contract.md:118` ("QUALITY row 19" for measure.py). Functional behavior is correct — added rows are reported in `added_rows`, never rejected — so this is documentation drift only, not a logic defect.

2. **Uncovered mutation surface (observation, contract-scoped) — controls.py covers none of `PROVINCE.md`, `corpus/README.md`, `SKILL.md` outside the `## Queue-drain craft` section, `corpus/SOURCES.md` non-row lines (`## Paths`/`## Leads`/round-note prose), or other lane files (`SCORECARD.md`, `AGENTS.md`, `MINT.md`, `SHONEN.md`, `README.md`, `.ufo/gates/**`, `.ufo/rounds/**`).** This round all six mutations outside `.ufo/waves/round-17/` (LOG/PROVINCE/SKILL/QUALITY/README/SOURCES modified; knowledge+lesson added — full `git diff --name-status` = 6 M + 2 A outside the wave dir, 259 A inside) are the documented, intended edits (LOG.md entry lists each). But a stray or hostile edit to any of those paths — e.g. rewriting a `.ufo/gates/citation-drift/` pinned fixture or a SKILL registry row silently — passes every control. `contract.md:120-123` scopes the tool to exactly what it checks, so this is a residual by-design blind spot for wave-3 attention, not a contract violation.

## Cross-checks performed (all pass)

- `USED_BY_COLUMN = 11` (controls.py:65) verified against live rows: index 11 is the used-by cell in every S001/S003/S024 row.
- S023 used-by asymmetry vs S003 investigated: S003 gained `corpus/lessons/round-17.md` + the r17 knowledge file; S023 gained only the knowledge file. `corpus/lessons/round-17.md:65` explicitly documents the intended S023 delta ("the same plus `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`"), and that bookkeeping line is the *only* S023 mention in round-17.md — so the omission is deliberate and recorded, not a defect. S024/S025/S026/S029 used-by cells contain exactly {knowledge file, lessons/round-17.md}, matching each file's actual S-references (verified by grep over `git show` output); S027/S028/S030 correctly list only the lesson (not cited by the knowledge file).
- `frozen_report` deletion coverage: `unchanged_report` (controls.py:219-220) flags `missing_at_after`, so a deleted prior-wave blob would surface.
- `admission_rows` keying (controls.py:192) would catch row renumbering as `row_absent_at_after` + new row — robust for this round's shape.
- No carrier executed; all checks were `git` object reads, `grep`/`awk` on `git show` output, and Python JSON parsing with `-B`.

## Installs

None.

## Summary

controls.json at lane revision `da64646` shows **zero real harms**: every non-clean field is a permitted, documented mutation (LOG append, S003/S023 used-by appends, QUALITY rows 19–20, SOURCES S024–S030). Two findings recorded: one stale docstring (controls.py:23-24, cosmetic) and one contract-scoped blind spot over non-registry lane files and `.ufo/gates/` fixtures.
