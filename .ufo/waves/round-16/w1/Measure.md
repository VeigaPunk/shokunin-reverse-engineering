# Measure — round-16 immutable presence census

## Files changed

- `.ufo/waves/round-16/measure.py` — new; stdlib-only clone of the round-15
  census shape (`git rev-parse --verify` → `ls-tree -r --name-only` →
  `git show <rev>:<path>`), adapted to the four routed C2 discharges.

## Behavior

`python3 .ufo/waves/round-16/measure.py <REV>` emits JSON; exit 0 on completed
census, 2 on usage error, unresolvable commit, unreadable required file, a
missing `## Coverage map` section, or an empty SOURCES table. It reads only
committed bytes and computes no verdict — every `C*` field is a 0/1 presence
proxy, not a pass.

## Field → route mapping

- `C1_round16_knowledge_entry` / `_files`: corpus/knowledge stems matching
  `^2026-10-\d{2}-r16-.*selection`; the exact filename is left to the
  EntryDraft/L1 integration (r15 convention: `2026-10-20-r15-…`), so the
  regex matches any dated `r16-*selection*` stem rather than a guessed name.
- `C1_selection_probe` / `_fixtures` / `_selfcheck`: presence of
  `selection.py`, `selection-fixtures.json`, `selfcheck.py` under
  `.ufo/waves/round-16/` (the claim's "boundary cases + entry" pieces).
- `C2_quality_row18`: QUALITY.md has a `| 18 |` row (lesson-grounded criterion
  for the routed defects; does not change row 17 — presence only).
- `C2_supplement_baseline_in_quote_fidelity_row`: the `| quote-fidelity |`
  registry row in SKILL.md (currently `SKILL.md:450`, pinned-values cell
  references only `.ufo/waves/round-14/fixtures/expected.json`) additionally
  names `.ufo/waves/round-15/boundary-fixtures/expected.json` — spotcheck
  route 2 (`round-15-verifier-spotcheck.md:186`).
- `C2_named_r15_correction_isolated_absolute_recheck`: within the r15
  knowledge entry `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`,
  the section starting at the exact heading `^## Round-16 correction[^\n]*$`
  (append-only convention, cf. round-14 lesson `Round-15 correction —
  virtual-dispatch advisory`, `corpus/lessons/round-14.md:144`) contains both
  the `-I` isolation flag and an absolute path to
  `.ufo/waves/round-15/snapshot-inventory.py`. Exact heading anchor, not a
  `correction` substring scan: the older `Named correction:` reference at
  `R15_ENTRY:39` (pointing at the round-14 lesson) would otherwise open the
  "section" and let unrelated later text produce a false hit. Route 1
  (`spotcheck:185`): recorded argv used `python3 -I` + absolute script;
  current `recheck:` line (`:3`) omits both.
- `C2_shonen_line_names_historical_round` / `_still_says_this_round`: the
  `asserted:` line following the `Instructions executable` box in SHONEN.md
  (currently `SHONEN.md:10`) contains `2026-10-15` and not `this round` —
  route 4 (`spotcheck:188`). The second field keeps the failure observable
  explicit at REVs where the line is absent or unrewritten.
- `C2_controls_script`: presence of `.ufo/waves/round-16/controls.py`
  (producing-command provenance for no-harm booleans — route 3,
  `spotcheck:187`; the script is specified to persist its own argv).
- Bookkeeping (unchanged semantics from r15): `knowledge_files`, `mapped`,
  `missing`, `dangling`, `sources_rows`, `tiers` (SOURCES col 4), `statuses`
  (col 8).

## Anchors and limits

- **Execution disclosure (actual):** one check WAS run here — `python3 -m py_compile .ufo/waves/round-16/measure.py` returned `COMPILES` (syntax-only; it generated `__pycache__/measure.cpython-314.pyc`, since removed). No measurement run, fixture tree, git mutation, or other check was executed; the probe itself was never invoked. L1 gate owns the red/green run.
- Same parse anchors as `.ufo/waves/round-15/measure.py:52-105`: coverage
  split on `## Coverage map` (`corpus/README.md:11`), source rows
  `^\|\s*S\d{3,}\s*\|`, map stems `2026-10-\d{2}-[a-z0-9-]+`.
- Presence ≠ proof: a `1` never asserts the correction's wording is admitted,
  the criterion is sound, controls.py runs, or selection.py matches source
  law. At the current baseline `6235498` every `C*` field reads 0 — expected
  red-before state; no run was performed here (edit-wave rule).
- Correction check requires the `## Round-16 correction` heading and both
  tokens inside that trailing section; a correction under any other heading
  or without `-I`/absolute path reads 0. Bounded marker semantics retained.
- Usage guidance and the stderr usage line carry `python3 -I` per route-1
  invocation consistency.
- Not verified: after the single `py_compile` disclosure above, no further
  checks ran — the tightened regex, usage lines, and this rewrite are
  unexecuted. L1 gate owns the red/green run.

No tool installs; no scope outside `.ufo/waves/round-16/`.
