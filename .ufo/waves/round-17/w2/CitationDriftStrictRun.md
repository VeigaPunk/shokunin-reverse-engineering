# CitationDriftStrictRun — citation-drift probe, strict mode, at da64646

Seat: `KaidokuR17.CitationDriftStrictRun` (wave 2, falsify). Target: the
round-17 integrated tree at `da64646adcb19c1ede7537b799b8c7d283fe43da`.

## Ran

```
python3 -I -B .ufo/gates/citation-drift/citation-drift-probe.py \
  --root . --rev da64646adcb19c1ede7537b799b8c7d283fe43da \
  --table .ufo/gates/citation-drift/pointer-table.json \
  --expected .ufo/gates/citation-drift/expected.json --strict
```

Verbatim capture: `.ufo/waves/round-17/w2/citation-drift-head.json`.

## Head result (observation)

`CITATION_DRIFT_VERDICT: clean findings=0 exit=0`, empty stderr. The verdict
is **correct**, not a blind pass — three independent confirmations:

1. `sha256sum` of the live pointer table equals the pin in
   `expected.json:12` (`7994eec7…`), so all 60 `entries` + 5 `quoted` rows
   were actually graded; the tamper preflight ran and passed.
2. Every round-17 edit to a pinned surface landed **below or off** every
   pinned line (verified via
   `git diff b563c79..da64646 -- SKILL.md LOG.md corpus/README.md`):
   - `LOG.md`: +36 appended at `@@ -2029,3` — quoted pins at `LOG.md:1012`
     (`log1005-quoted-claim`) and `LOG.md:1442` (`log1442-shonen-repoint`)
     are untouched; LOG is append-only so they can never shift.
   - `SKILL.md`: in-place row edits at `@@ -445` (citation-drift /
     custody-pair rows) plus +34 appended at `@@ -505` — the graded rows
     are `anchor` entries with no `pin_line`, and the `extracted` pins at
     `SKILL.md:246/248/252/254` sit above all insertions. Spot-read of
     `da64646:SKILL.md` around those lines confirms unchanged content.
   - `corpus/README.md`: 1 in-place line edit at `@@ -32`; extracted pins
     at `:22` and `:175` unaffected.
   - `SCORECARD.md`, `README.md`, `SHONEN.md`, `PROVINCE.md`: no diff this
     round (`git diff --stat` shows zero).
3. Negative controls on `/tmp` copies (repo files untouched): mutating one
   `must_match` in a table copy → `citation_dead`, exit 1; mutated table
   against the real `expected.json` → `pointer_table_tampered`, exit 2. The
   instrument discriminates at this rev.

## Findings
**No drift defect.** No pinned README/SKILL/SCORECARD line shifted; verdict
clean is the true answer for the pinned set.

**Coverage observation (not a probe defect — a table-maintenance note for
L1):** round 17 introduced new in-repo `file:line` citations on durable
surfaces that the pointer table (frozen at `7994eec7…`, doc at
`pointer-table.json:2`) does not pin: `LOG.md` entry lines for
R16-PROVENANCE cite `LOG.md:2012`, `corpus/lessons/round-16.md:154`,
`.ufo/waves/round-16/verification.json:419`, and
`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` (added at
`LOG.md:2059-2062` in the `da64646` tree). If the gate's remit is "every
line-number citation on committed surfaces," these are unenforced. `LOG.md`
is append-only so `:2012` is naturally stable; the corpus/verification
targets are the ones that could drift silently.

## Boundary notes

- `expected.json:4` pins the frozen-run verdict (`failed`,
  `citation_dead`) at `679af5d…`; a clean verdict at `da64646` is a
  different measurement, consistent with the file's own note
  (`expected.json:5`). No contradiction.
- `expected.json:16` pins `config-toml-landmarks`, but the current table
  contains zero `@`-snapshot targets; the pin is inert, not defective.

## Files written

- `.ufo/waves/round-17/w2/citation-drift-head.json` (stdout/stderr/exit)
- `.ufo/waves/round-17/w2/CitationDriftStrictRun.md` (this report)

No tool installs. No files outside the w2 lane were modified; mutation
fixtures lived only in `/tmp` (`/tmp/cd-table-mut.json`,
`/tmp/cd-expected-mut.json`).

Report: .ufo/waves/round-17/w2/CitationDriftStrictRun.md
