# MeasureTool — round-17 measure.py

## Files changed
- `.ufo/waves/round-17/measure.py` (new, executable) — the only implementation file written.

## What it does (observation)
Modeled on `.ufo/waves/round-16/measure.py:1-165` (same git-objects-only approach,
`git show`/`git ls-tree`, exit 0 emitted / 2 could-not-evaluate, JSON
`indent=2, sort_keys=True`). Deviations from r16, all required by
`contract.md:115-123`:

- `census(root, revision)` is parameterized by repo root
  (`measure.py:74-180`) so `--selftest` (`measure.py:226-299`) can exercise it
  against a `tempfile.mkdtemp()` fixture repo built with `git init`/`commit`
  under synthetic author env (`measure.py:203-224`). Selftest: 22 checks —
  case A anchors-only → all presences 0; case B artifacts committed → all
  presences 1. Observed: `SELFTEST: CLEAN cases=22`, exit 0.
- Retains `argv` and `orig_argv` in the result (`measure.py:306-308`;
  `orig_argv` via `getattr(sys, "orig_argv", sys.argv)`).
- New presences per contract `## W/measure.py` (`contract.md:116-120`):
  each of the 11 `W/tools/*.py` (`measure.py:31-44,151`), `measure.py` and
  `controls.py` themselves, knowledge entry
  `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, QUALITY row
  `| 19 |`, SCORECARD `## Capabilities` row containing the literal
  `retained REA Ghidra-session log`, SKILL registry rows matching kind cell
  `(probe|gate|tool)\s*/\s*kaidoku` AND referencing `.ufo/waves/round-17/`
  (names listed), blobs matching `.ufo/waves/round-17/runs/*/receipt.json`
  (count + paths), SOURCES row/tier/status histograms (tier = cell idx 4,
  status = cell idx 8, per `SOURCES.md` header `| id|source|kind|tier|scope|
  anchor|teaches|status|...`), README `## Coverage map` tokens vs
  `corpus/knowledge/` stems (`mapped`/`missing`/`dangling`).

## Baseline run (observation)
`python3 -I .ufo/waves/round-17/measure.py b563c799d97774aae4351276fe43cb897311e349`
→ exit 0. All new-artifact presences 0: `tools` map all 0 (`tools_present: 0`),
`measure_py: 0`, `controls_py: 0`, `C2_knowledge_entry: 0`,
`C1_quality_row19: 0`, `C2_scorecard_capability_row: 0`,
`skill_registry_rows_new_tools: 0`, `run_receipts: 0`. Baseline bookkeeping:
`knowledge_files: 94`, `mapped: 94`, `missing/dangling: []`,
`sources_rows: 23`, `tiers {A:21,B:1,C:1}`, `statuses {mined:22,rejected:1}`.

## Anchors used
- `contract.md:115-123` — measure.py/controls.py spec.
- `contract.md:80-88` — registry-row definition reused for the SKILL scan.
- Baseline `SCORECARD.md:615-623` — `## Capabilities` table (file at repo root,
  not `corpus/`).
- Baseline `corpus/QUALITY.md:28` — row 18 last row before row 19 insertion.

## Limits / inference
- Presence only: a `1` means the blob/row/wording exists at REV, never that a
  tool works, a receipt validates, or a row was admitted. Docstring states this.
- SKILL registry detection keys on any `.ufo/waves/round-17/` path mention in a
  kaidoku-kind row (inference: L1 will register tools with their committed
  paths; a row naming a r17 tool by another spelling would be missed).
- `sys.orig_argv` requires Python ≥3.10; fallback to `sys.argv` if absent.
- No installs performed; no tools run beyond this seat's own script and
  read-only git queries.
