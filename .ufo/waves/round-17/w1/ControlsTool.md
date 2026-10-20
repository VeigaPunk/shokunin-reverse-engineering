# ControlsTool — round-17 controls.py (w1)

## Files changed
- `.ufo/waves/round-17/controls.py` (new; only file written by this seat besides this report). 533 lines. No other file touched.

## Behavior implemented (contract § `W/measure.py and W/controls.py`)
Generalizes `.ufo/waves/round-16/controls.py` without editing it. Per-revision data is read only via `git ls-tree`/`git show` on resolved commits (`Rev`, controls.py:88-120); the worktree is never touched.

Contract clauses -> code:
- "old LOG prefix retained" -> `log_old_prefix` for `APPEND_ONLY=["LOG.md"]` via `prefix_report` (controls.py:198-212, 338-340).
- "all old lessons/knowledge prefixes retained" -> `old_lessons_prefix`/`old_knowledge_prefix`, byte-prefix check over every `corpus/lessons/*.md` / `corpus/knowledge/*.md` present at BEFORE (controls.py:226-239, 341-345).
- "prior `*-verifier-spotcheck.md` byte-identical" -> `prior_verifiers_unchanged` (controls.py:337).
- "pre-existing `.ufo/waves/**` and `evidence/**` blobs byte-identical" -> `prior_wave_evidence_blobs` (controls.py:242-265): scope derived from the BEFORE tree itself under `FROZEN_PREFIXES=[".ufo/waves/","evidence/"]` (controls.py:56) — generalizes r16's hardcoded round-14/round-15 + one evidence dir. Retains `quote_script_unchanged` for the r14 `tools/quote-fidelity.py` row.
- "QUALITY rows 1-18 unchanged" -> `quality_admission_rows` (controls.py:268-289): parses numbered `| n |` lines inside `## Admission criteria` of `corpus/QUALITY.md` (`admission_rows`, controls.py:174-195, scoped so the "Signals" table is excluded); requires every BEFORE row byte-identical at AFTER and reports added row numbers. Generalizes "1-18" to "every row present at BEFORE"; r17 row 19 lands as `added_rows:["19"]`, never a violation.
- "retaining argv/orig_argv and resolved revisions" -> `invocation` block keeps `sys.argv`, `sys.orig_argv`, `isolated`, `producing_command` (shlex.join), plus `revisions` with both names and resolved SHAs (controls.py:329-333, 351-368).
- Retained from r16 for depth: `craft` command-A replication (SKILL.md `## Queue-drain craft`, controls.py:124-154) and `sources_registry` immutability with used-by column exception (controls.py:292-319).
- `--selftest` builds a temp `git init` repo, commits clean-append and red-mutation fixtures, asserts prefix/frozen/quality/revision checks (controls.py:336-502); exits 0/1.
- Exits: 0 report emitted, 2 usage/unresolvable/missing anchor; no conformance gate (`conformance_gate: false`).

## Required run (BEFORE=AFTER=b563c799d97774aae4351276fe43cb897311e349)
- `python3 -I .ufo/waves/round-17/controls.py b563c79... b563c79...` -> **exit 0**, JSON on stdout (sort_keys, indent 2).
- `--selftest` -> `SELFTEST: CLEAN cases=11`, exit 0.

Observed output summary (all-retained run):
- `prior_wave_evidence_blobs`: checked=unchanged=**14943**, `quote_script_unchanged: true`.
- `quality_admission_rows`: rows_before=rows_after=**18**, `prior_rows_byte_identical: true`, `added_rows: []` — consistent with QUALITY.md at baseline having admission rows 1-18 (observed: `git show b563c79:corpus/QUALITY.md` rows numbered 1..18).
- `log_old_prefix.LOG.md`: `prefix_preserved: true`, `byte_identical: true`, `appended_bytes: 0`.
- `old_lessons_prefix`: 20/20 prefix-preserved; `old_knowledge_prefix`: 94/94.
- `prior_verifiers_unchanged`: 5 files, all `unchanged: true`.
- `craft` before==after: 17 rule blocks, 17 citation-resolved, identical `craft_sha256`.
- `sources_registry`: 23 rows both sides, `immutable_cells_unchanged: true`.

## Observation vs inference / limits
- Observation: all fields above are blob-SHA or byte comparisons over `git ls-tree`/`git show` output; equal revision -> all-retained as shown.
- Inference: a real AFTER that appends to LOG.md/lessons/knowledge and QUALITY row 19, leaving the 14,943 frozen blobs and rows 1-18 untouched, will report clean on every no-harm field; this is the intended round-17 shape per contract.
- Limits (stated in the script docstring, controls.py:1-48): byte checks only — no semantic, pointer, or temporal-stability audit; `prefix_preserved` is append-only, not "unchanged during"; git reads inherit caller `GIT_*` env (unhardened, recorded); QUALITY check covers only the `## Admission criteria` numbered rows, not the signals table; craft check is command-A's bounded citation range check, not correctness.
- Selftest coverage gap (observed): fixture QUALITY/SOURCES are minimal (3 admission rows, 1 SOURCES row); the red case mutates one frozen blob and one quality row, not the lessons/knowledge prefix or craft section.

## Tooling
No installs; stdlib + `git` only (per contract: Python 3 stdlib, `python3 -I` runnable).
