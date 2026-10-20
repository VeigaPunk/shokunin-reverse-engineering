# NoHarmProducer — round-16 `controls.py`

## Deliverable

New file: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/controls.py`
(stdlib-only, ~290 lines, mirroring `round-15/measure.py` style and exit
discipline). No other repo files touched. Report class: `git_object_bytes`.

## Behavior

`python3 [-I] .ufo/waves/round-16/controls.py <before> <after>` — both names
resolved via `git rev-parse --verify <name>^{commit}`, then all reads go
through `git ls-tree -r -z` (blob SHAs) and `git show <rev>:<path>` (raw
bytes). Worktree never touched; nothing executed. Exit 0 = report emitted;
exit 2 = usage, unresolvable revision, or missing structural anchor.
`"conformance_gate": false` is explicit in the report; no verdict field.

Report fields (per parent's ReportOnly/argv direction):

- `invocation.argv` verbatim plus `argv_note`, `sys.flags.isolated`, and a
  `producing_command` rendered with `-I` only when actually used — discharges
  the round-15 spotcheck items 1 and 3 (`corpus/lessons/
  round-15-verifier-spotcheck.md:185,187`: invocation consistency and
  producing-command provenance for control booleans).
- `revisions`: supplied names and pinned resolved commit SHAs.
- `log_old_prefix["LOG.md"]`: `prefix_preserved` (byte-prefix retention,
  append-only) distinct from `byte_identical`, plus `appended_bytes`.
- `old_lessons_prefix` / `old_knowledge_prefix`: per-file byte-prefix
  retention for every `.md` present at BEFORE under `corpus/lessons` and
  `corpus/knowledge` (append-only tolerated; rewrite flagged).
- `prior_verifiers_unchanged`: full-blob-SHA equality for every
  `corpus/lessons/*-verifier-spotcheck.md` present at BEFORE (r12–r15).
- `frozen_baselines`: per-file blob equality for all paths at BEFORE under
  `.ufo/waves/round-14/`, `.ufo/waves/round-15/`, and
  `evidence/round-1-2026-10-15/` — covers quote-fidelity script
  (`round-14/tools/quote-fidelity.py`), the original frozen controls
  (`round-14/fixtures/expected.json`), and the supplemental round-15
  `boundary-fixtures/` set routed for discoverability at spotcheck :186.
  `quote_script_unchanged` summarized separately.
- `craft.before` / `craft.after`: `craft_sha256` over the command-A craft
  slice (`SKILL.md` `## Queue-drain craft ` → next `\n## `), `rule_blocks`,
  `citation_resolved_rules` — replicating `SCORECARD.md:103-117` exactly
  (knowledge-file existence + in-range line citations only; labelled "not a
  semantic or all-pointer audit" in-field).
- `sources_registry`: `corpus/SOURCES.md` rows keyed by id; every cell except
  column 11 (`used-by`) must be unchanged or is listed under
  `immutable_violations` (column indices named); `used-by` diffs are reported
  under `allowed_used_by_deltas` — matching lesson wording "Only permitted
  `used-by` changes on existing rows" (`corpus/lessons/round-15.md:39`).

## Defects caught and fixed in flight (via parent relay)

1. `USED_BY_COLUMN` was 10 (`recheck`); `line.split('|')` keeps the leading
   empty string, so `used-by` is index 11. Without the fix a permitted
   `used-by` edit would have been falsely reported as an immutable-cell
   violation. Now 11.
2. `producing_command` printed `python3` without `-I` while L1 is expected to
   run with `-I` (round-15 spotcheck item 1). Now the command interpolates
   `sys.flags.isolated`, and `argv_note` states that `sys.argv` excludes
   interpreter flags.
3. A duplicate `invocation` key (stale block shadowing the corrected one)
   briefly existed mid-edit after a range-put reorder; the stale block was
   removed and `craft`/`sources_registry`/`evidence_class` keys re-verified
   present in the final dict.
4. (Final relay, applied) `producing_command` previously reconstructed
   `python3` + only `-I`, dropping other interpreter flags and revision
   quoting. Now `orig_argv` (full original command line, interpreter flags
   retained), `executable` (`sys.executable`), and `producing_command` =
   `shlex.join(sys.orig_argv)` are emitted; `argv_note` directs outer L1
   receipts to carry the exact subprocess argv unmodified. Git-inherited
   `GIT_*` environment influence is documented in the docstring as a
   limitation rather than hardened — outside this round's narrow scope.

## Evidence anchors

- Baseline commit `6235498b…` from `claims.json`.
- Command-A recipe replicated verbatim: `SCORECARD.md:92-123`.
- Row-split convention verified against `measure.py:76-85`
  (`line.split("|")`, `cell(row, index)`; tiers read at index 4, statuses at
  8 — consistent with leading-empty indexing).
- Registry row already naming the supplemental baseline:
  `SKILL.md:450` (quote-fidelity row, pinned-values cell).
- Prior controls record: `.ufo/waves/round-15/no-harm-controls.json`
  (booleans without producing commands — the gap this script closes).

## Limits / non-claims

- Not executed (wave rule: L1 verifies once post-integration). Syntax/logic
  reviewed against `measure.py` only; a runtime defect may remain — flagged
  for L1 smoke: `python3 -I .ufo/waves/round-16/controls.py 6235498b HEAD`.
- Prefix/`unchanged` booleans are byte facts, not conformance; the script
  asserts no pass/fail, no score, no capability.
- `prefix_preserved` cannot distinguish "append" from "rewrite that happens
  to share a prefix" beyond byte semantics — this is the honest bound.
- Frozen set is enumerated by path prefix at BEFORE; a frozen file under
  another tree (e.g. `.ufo/gates/`, `.ufo/rounds/`) is out of the default
  set — `FROZEN_PREFIXES` is a named constant, extendable without logic
  change.
- Git subprocesses inherit the caller environment; `GIT_DIR`/`GIT_OBJECT_*`
  variables could redirect object reads. Recorded as a limitation in the
  docstring; constraining it is out of this round's scope.

## Risks / blockers

- If L1 wants `.ufo/gates/citation-drift/expected.json` or
  `.ufo/rounds/interactive-r1/` pinned too, add the prefix — these gate
  tables legitimately evolve, so they were left out deliberately.
- `git -z` ls-tree parsing assumes no quoted paths (all repo paths are
  ASCII); `-z` makes that exact.
- Tools installed/upgraded: none.
