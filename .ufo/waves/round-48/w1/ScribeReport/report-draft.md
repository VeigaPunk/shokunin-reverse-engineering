# Round 48 — draft `## Work performed` and `## Landed changes`

Drafted by seat `ScribeReport` from `plans/round-48-claims.md@dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`
and the wave-1 receipts under `.ufo/waves/round-48/w1/`. Nothing has landed yet; every
`Landed changes` row is a **pending** slot for the L1's landing commit hash — do not publish
this section until the hash, re-measure receipts and LOG entry exist. `~` boxes only.

## Work performed

- Declared the round: two claims on the two tied-lowest axes — R48-C1 depth (craft rule
  block 25, the verdict-meaning matrix over routed defects `R46-CL7`/`R47-CL10`, interpreter
  `tools/round-48/meanings.py`, registry re-bound by meaning over `tools/round-48/census2.json`)
  and R48-C2 calibration (`tools/round-48/record2.py` re-deriving `SCORECARD.md` from committed
  bytes); no coverage claim. Evidence: `plans/round-48-claims.md@dc73587a` lines 14–22, 39–108.

- Measured both frozen counters at the freeze revision, before any landing. C1 (`meanings.py`
  `--freeze dc73587a… --rev dc73587a…`): exit 1 — `marker_occurrences 0 != 1`,
  `marker_block_count 0 != 1`, `rule_blocks 24`, battery `skipped` (`frozen_path_changed: []`).
  Evidence: `.ufo/waves/round-48/w1/C1Pins/receipt.json` (stdout sha256 `594e618c…`,
  UTC 2026-10-28T18:47:07Z), `w1/C1Battery-2/receipt.json`, `w1/C1Struct-2/meanings-dc73587a.json`,
  `.ufo/waves/round-48/controls/ctl-c1-0-do-nothing.json`.

- Confirmed the base comparison is honestly unevaluable, not red: at `--rev
  61b87d742032e65fca9c38267d7d6ed7e555edad` the C1 counter exits 2 (`freeze is not an ancestor
  of rev`); a 2 never counts toward the target. Evidence:
  `.ufo/waves/round-48/w1/C1Struct-2/meanings-61b87d74.json`, `w1/C1Struct-2/receipt.json`.

- Re-derived the frozen census: `census2.py` at freeze bytes yields 42 paths,
  `named_but_absent: []`; committed `tools/round-48/census2.json` sha256
  `403b4c143b020f1a30905258543758b11992dbd2235358575fb09f63473d7b59` equals the freeze-rev
  derivation exactly. The worktree derivation differs (sha256 `36556d11…`, identical 42-path
  set) because the worktree claims file names 5 round-48 paths vs 4 at freeze — a data drift
  the path-set comparison alone conceals. Evidence: `.ufo/waves/round-48/w1/C1Census.md`,
  `w1/ExecCensus.md`.

- Measured the registry gap the landing must close: at the freeze revision the `SKILL.md`
  instrument-registry section carries 40 rows against the 42 census paths — missing
  `tools/round-48/meanings.py` and `tools/round-48/record2.py`; no extras, no duplicates.
  Evidence: `.ufo/waves/round-48/w1/C1Census.md` (registry-path diff at freeze).

- Found four frozen-side defects in the C1 counter that constrain what a landing can score —
  reported as findings, not fixed (frozen bytes): (a) clause 8's census equality compares
  `census_rederive()`'s dict to `doc["paths"]`'s list (`meanings.py:290-298`, `:429-444`) and
  can never be true even when the derivation is byte-exact — C1 is un-greenable as frozen;
  (b) `registry_rows()` parses only lines starting `| ` + backtick, so a data row `|  ` +
  backtick is silently skipped — a forged registry row escapes both path-set and meaning
  checks; (c) the lexical meaning classes accept `0=not met; 1=violation; 2=usage` as
  success/not-met/unevaluable (`\bmet\b` matches inside `not met`); (d) the three-class model
  does not fit probe/library instruments (e.g. `gate.py` has no standalone verdict map).
  Evidence: `w1/C1Census.md`, `w1/CritAxis.md`, `w1/C1Gold.md`, `w1/C1RowsB.md`,
  `w1/C1Semantic.md`, `w1/CritSeparability.md`.

- Pinned the C1 digest values the block must carry: `interpreter_sha256` =
  `74b8da35b4c47c7732bc2cb5a69a3c048e8e1f22ccf93b506cba9a71cd90816d` and `MUT_DIGEST` =
  `25ce025f8b2be63a5122583191cbf7588db7dc2894c869fac2ab075a84f5c1ea` over the four mutation
  name+body pairs; isolated digest probes confirm a names-only pin differs (`dbf00169…`) and a
  body edit changes the value (`f2d80306…`). Evidence: `w1/C1Block.md`, `w1/C1Pins.md`,
  `w1/C1SelfTest.md`.

- Ran the C1 selftest green (`MEANINGS_SELFTEST: cases=16 failures=0`, exit 0, UTC
  2026-10-28T18:47:03Z) and proposed five missing adversarial cases (body-only mutation edit,
  `not met` inside exit 0, two-class segment, one-segment placeholder, census duplicate).
  Evidence: `.ufo/waves/round-48/w1/C1SelfTest.md`.

- Verified the arm-binding asymmetry at source level: v3 compares each row's arm cell to
  `EXPECTED_ARM` (`meanings.py:351-370`) while v2 checks only routed-id presence (`:372-375`) —
  the `permuted-arm` hole is real; a measured permuted-arm fixture was attempted but the
  harness lacked `census_text` (`KeyError`) — recorded as not run, not as a result.
  Evidence: `w1/C1IdsArms/report.md` (+ `fixtures/` reserved but invalid).

- Drafted the C1 landing material: block-25 bytes carrying the marker, two rows with arm
  cells `meaning` (R46-CL7) / `floor` (R47-CL10), both pins, and ≥5 line-selected citations
  including `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`;
  plus the two registry-row drafts for the round-48 counters. Evidence:
  `w1/C1Block/block.md`, `w1/C1NewRows/rows.md`, `w1/C1Refs.md`, `.ufo/waves/round-48/l1/block25.md`.

- Measured C2 at the freeze revision: exit 1 — round-47 oracle green (44 atoms,
  `mismatches []`, `met_target true`, executed from `--rev` bytes), but three structural
  clauses fail: `round-47: no seat atom and no re-derived seats correction`; `no ## Record
  corrections — round 48 line re-derived`; `quoted numbers with no backing receipt: 1`
  (`exempted 2`). Battery `skipped`. Evidence: `w1/C2Floor/receipt.json`,
  `w1/C2Battery/receipt.json`, `w1/C2Oracle/receipt.json` (stdout sha256 `f0bf3d66…` at three
  independent runs), `controls/ctl-c2-0-do-nothing.json`.

- Confirmed the hole C2 exists to close: the identical card scores `met_target: true` under
  `--profile v2` (ported round-47 semantics). Evidence:
  `.ufo/waves/round-48/controls/ctl-c2-1-v2-profile.json`, `w1/C2Corr.md` (v2 green probes).

- Verified amendment A1 retired the vacuous score-cell clause: the parser now binds `cell[0]` —
  `axis_score_cells` coverage `[138,138]` score `[9.72,10.0]`, depth `[24,24]` score
  `[10.0,10.0]`, `axis_score_bad []`; the A1-before control shows the old `axis_score_cells {}`.
  Stale-score rejection itself remains **not run**. Evidence: `w1/C2Axes.md`,
  `controls/ctl-c2-a1-before.json`.

- Proved the quote-correction machinery end-to-end at `score()` level: a `- corrects quote
  round-47: exempted 1 (receipt .ufo/waves/round-47/l1/scores/c2-at-A7.json)` line re-derives
  (`corrections_bad []`) and clears `quotes_bad`; an already-right correction and an
  out-of-window round-45 correction are each rejected with a named reason. Evidence:
  `w1/C2Quote/report.md` + `misquote-repaired.json`, `already-right-parsed.json`,
  `outside-window.json`, `sha256.txt`.

- Probed the correction classes: a well-formed `axes` correction `24/24` is accepted and
  `999/999` rejected in `corrections_bad`; a malformed `seats` line is v3-red / v2-green
  (`score()`-level probes, not full `evaluate()`). A well-formed forged `axes` correction
  green under v2 was not achieved — recorded limitation. Evidence: `w1/C2Corr.md`.

- Established the oracle provenance boundary: replacing the worktree `tools/round-47/record.py`
  with a stub leaves the receipt byte-identical (sha256 `f0bf3d66…`) — the oracle truly
  executes from `--rev`; but `tools/round-46/gate.py` is imported from the worktree
  (`record2.py:35-37`) and is not revision-pinned, so worktree `gate.py` can still move C2
  verdicts (code-path finding; an isolated exploit was not measured — the extracted-script run
  failed `ModuleNotFoundError`). Evidence: `w1/C2Oracle.md`, `w1/C2OracleLimit.md`.

- Documented the battery gate: `evaluate()` runs the forgery battery only when the genuine
  card is green, so every forgery result is conditional on landing; at the freeze revision
  both batteries report `skipped` and no v3-red/v2-green forgery measurement exists — by
  design, not by omission. Evidence: `w1/C2Battery.md`, `w1/C2Floor.md`, `w1/C2Gold.md`,
  `w1/C1V2.md`, `controls/ctl-c1-0-do-nothing.json`.

- Reviewed causal separability: C1 never reads `SCORECARD.md`, C2 never reads `SKILL.md`;
  the two claims land and score independently; the shared input is the frozen
  `tools/round-46/gate.py` infrastructure, not a claimed surface. Evidence:
  `w1/CritSeparability.md`.

- Flagged a freeze-identity discrepancy for L1 reconciliation before the report cites
  `plans/round-48-claims.md@<freeze>`: `git log --format=%H -1 -- plans/round-48-claims.md`
  returns `ac02a79ff84133220d01ce3b59a4789b7004dbc5` (= HEAD at observation time), not the
  declared `dc73587a…`; the file's own derivation sentence yields the *latest* claims-touching
  commit, and any later rev whose claims bytes differ trips `frozen_path_changed` → exit 2.
  Evidence: `w1/CritClaims.md`, `w1/C2LandingGate.md`.

- Scouted the LOG contract: the round-48 entry takes the 46/47-generation heading
  `### Round 48 — <clause>`, appended as line 3436 (blank 3435), bold `- **Label.**` bullets,
  optional `### Round 48 claim ledger`; the claims file binds SKILL/SCORECARD only, so this is
  convention not a frozen clause. Evidence: `w1/ScoutLog.md`.

- Recorded honest negatives as negatives: gold-artefact C1 fixture not constructed; v2-profile
  C1 control not run (no landed block-25 artefact exists); landing preflight not run;
  failing-registry-row census not enumerable pre-landing; stale-score-cell attack not run;
  tautology v3-red/v2-green pair not established. Evidence: `w1/C1Gold.md`, `w1/C1V2.md`,
  `w1/C2LandingGate.md`, `w1/C1RowsA.md`, `w1/C2Axes.md`, `w1/C2Floor.md`.

## Landed changes

All slots pending — fill the commit hash and the post-landing re-measure receipts at landing.

| Change | Content evidence | Acceptance | Commit |
|---|---|---|---|
| `SKILL.md` gains craft rule block 25 — marker `<!-- verdict-meaning-table v1 -->`, header `trigger \| v1 hole \| v2 arm \| exit`, two rows keyed `R46-CL7→meaning`, `R47-CL10→floor`, `mutations_sha256:25ce025f…`, `interpreter_sha256:74b8da35…`, ≥5 resolving line-selected citations incl. one `corpus/knowledge/` entry | `w1/C1Block/block.md`, `l1/block25.md`, `w1/C1Refs.md` | claims §123-126; C1 clauses 1-7 | pending |
| Instrument-registry section gains rows for `tools/round-48/meanings.py` and `tools/round-48/record2.py` and repairs every verdict map that lacks its meaning class (40→42 rows, `0=success / 1=not-met / 2=unevaluable`, three distinct, no placeholders) | `w1/C1Census.md` (gap), `w1/C1NewRows/rows.md` (draft rows) | claims §127-128; C1 clause 8 | pending |
| `SCORECARD.md` gains `## Round 48`, `## Record corrections — round 48` (re-derived `seats` correction for round 47; `quote` correction binding `exempted 2`→1 to receipt `.ufo/waves/round-47/l1/scores/c2-at-A7.json`), and Owned-axes head update | `w1/C2Floor.md`, `w1/C2Quote/report.md` + `misquote-repaired.json`, `w1/C2Corr.md` | claims §129-131; C2 clauses 2-5 | pending |
| `LOG.md` gains `### Round 48 — …` at line 3436 (append-only, 46/47-generation form) | `w1/ScoutLog.md` | convention (not a frozen clause) | pending |
| Post-landing re-measure: both frozen counters at the landing rev — C2 expects green iff the three failing clauses land (floor/corrections/quote) **and** the battery then runs; C1 blocked by the frozen dict-vs-list census comparator (`meanings.py:429-444`) unless the L1's registry landing and the comparator defect are reconciled — a vacuous or comparator-blocked C1 green must not be claimed | `w1/C2Battery.md`, `w1/C1Census.md`, `w1/CritAxis.md` | claims kill rules; `frozen_path_changed` must stay `[]` | pending |
