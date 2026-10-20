# DRAFT — LOG.md "round-17 measured records and final integration" (w2, author-side, not integrated)

Draft notes (not part of the LOG entry; delete on integration):

- Placement: append after the current last line of LOG.md, which is line 2067 at
  `da64646` (the round-17 declared entry at LOG.md:2033-2067). The w1 draft's
  anchor "line 2031" is stale.
- Every `<SLOT …>` is filled only by the L1 post-integration execution pass. Text
  marked "attack-pass" is what w2 observed by re-running retained files or
  `git` objects at `da64646adcb19c1ede7537b799b8c7d283fe43da`; the final pass
  must re-run it and may overwrite it. Nothing here is a final measurement.
- Temporal wording: this draft quotes no during-run stability phrase. The only
  permitted form is "pre and post maps equal at two named instants". The
  round-16 phrases (LOG.md:2012, corpus/lessons/round-16.md:154,
  .ufo/waves/round-16/verification.json:419) are not reused as claims; they
  appear only in correction bullets that say "temporal stability not evidenced".

---

## 2026-10-20 — round-17 measured records and final integration

Source revision: `<SLOT final-source-sha>` (baseline
`b563c799d97774aae4351276fe43cb897311e349`; predictions frozen at
`271167473d87ef710f07ecdd98caf0ce12091686`, byte-identical to that commit
through `da64646`). Commands, argv, cwd, exits and output hashes:
`.ufo/waves/round-17/verification.json` (`<SLOT sha256>`; not present at
`da64646`).

- Selftests, each run once (`python3 -B -I <tool> --selftest`): pins `<SLOT>`
  (attack-pass CLEAN cases=7), retain `<SLOT>` (3), carrier-run `<SLOT>` (2),
  log-extract `<SLOT>` (8), predict `<SLOT>` (17), compare `<SLOT>` (10),
  invocation-audit `<SLOT>` (6), temporal-sweep `<SLOT>` (6), buildinfo-probe
  `<SLOT>` (11), receipt-validate `<SLOT>` (5), carrier-census `<SLOT>` (10),
  measure.py `<SLOT>`, controls.py `<SLOT>` (attack-pass CLEAN cases=11).
  Every selftest that was run exited 0 at `da64646`.
- Pins red case: `<SLOT exit 1, mutated path named>`; green case `<SLOT exit 0>`.
  The red output is a temporary fixture and is not retained unless `<SLOT path>`
  records it.
- R16-PROVENANCE sweep (`temporal-sweep.py --root <LANE> --rev <SLOT>
  --sites-rev b563c799d97774aae4351276fe43cb897311e349`): baseline sites `<SLOT 4>`,
  corrected `<SLOT 0>`, unqualified `<SLOT 4>`; at `<SLOT rev>` sites `<SLOT 4>`,
  corrected `<SLOT 4>`, unqualified `<SLOT 0>` (attack-pass at `da64646`). The
  baseline count depends on the widened site list and `corpus/knowledge/`; the
  pre-widening tool counted 2 at the same baseline (w1 TemporalSweepTool report).
  The sweep is a fixed-wording census and is not a semantic finding. The four
  correction lines are LOG.md:2059-2062.
- Mid-run pin evidence: each run retains pre and post pin maps with UTC instants
  and an equal compare (8/8, attack-pass). Mid-run checks ran at a 30 s throttle
  (`tools/carrier-run.py:35`, `:422-433`), but the receipts retain no mid-run
  count, map or instant. `pins_changed_during_run` is written only on drift and
  is absent from all eight receipts. `<SLOT: either retain mid-run records and
  cite them, or write "pre and post maps only; mid-run checks not retained">`.
  The round-17 knowledge entry and Gate table must match whichever form is kept.
- R16-INVOCATION (`invocation-audit.py --root <LANE> --rev <SLOT>`): attack-pass at
  `da64646`: rows 17, exercised_match 6, labelled_unexercised 0,
  unlabelled_variant 11. Baseline `b563c79`: rows 7, exercised_match 5,
  unlabelled_variant 2 (citation-drift, custody-pair). The citation-drift row
  matches the round-16 argv at `27b8fc1` (`.ufo/waves/round-16/verification.json`),
  not a round-17 re-exercise. The custody-pair row cites
  `.ufo/waves/round-17/verification.json`, which is not yet retained. Ten
  round-17 tool rows have no retained argv. Final unlabelled count
  `<SLOT before 2> → <SLOT after>`. The contract's `M → 0` is `<SLOT met / not
  met>`.
- Carrier runs (eight `runs/<label>/receipt.json`, REA 6.5.0, Ghidra 12.1.4).
  Attack-pass at `da64646`: analyze exit 0, carrier-run exit 0, observation exit
  0 and compare exit 0 for 8/8; pins pre/post equal over 146 paths for 8/8; one
  bound session and zero unbound sessions for 8/8. Per label: ghidra.log sha256
  `<SLOT>`, polls `<SLOT>`, analyze Evidence ID (`steps.analyze.evidence_id`)
  `<SLOT>`.
- Run environment: `pro-op` ran with `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000`
  (`runs/pro-op/receipt.json` `rea_ghidra_env`; `run-carriers.sh:17`). The other
  seven ran with no override. `run-carriers.sh:15` removes each run directory
  before writing, so earlier attempts are not retained. `<SLOT: one attempt per
  label, or list the attempts>`.
- Prediction comparison (`compare.py`): 8/8 exit 0, five fields each (40/40
  field matches). Observed routes: none ×4 (calib-shfmt, pro-containerd-shim,
  pro-esbuild-0.27.7, pro-op), info ×2 (calib-esbuild-0.25.12,
  pro-esbuild-0.21.5), fallback ×2 (pro-notesmd-cli, pro-aether). Not compared:
  the prediction's `extra_expectations`, the log classification, and analyzer
  errors. Unpredicted: pro-aether `Go analysis failure` with
  `java.io.EOFException: Unable to read past EOF` after a successful fallback
  bootstrap (`runs/pro-aether/logs/*/ghidra.log:97,177`; `Go strings found: 7200`
  at line 207). Cause UNKNOWN. pro-esbuild-0.27.7 has no version, so its five
  compared fields are null or false by construction. `<SLOT mismatches n>`.
- Receipt validation (`receipt-validate.py runs/<label>/receipt.json`, eight
  receipts): attack-pass 0/8 valid; each finding `unrecognized_shape` at `$`.
  The validator classifies a carrier receipt only when `steps` is a list
  (`tools/receipt-validate.py:95-104`); `carrier-run.py` writes `steps` as an
  object keyed `analyze` and `inspect-go-binary`. `<SLOT validate exit per
  receipt>`. The capability row is admitted only if every receipt validates:
  `<SLOT admitted / not admitted>`.
- Controls (`controls.py b563c799d97774aae4351276fe43cb897311e349 <SLOT rev>`):
  attack-pass exit 0. Old LOG prefix preserved (2627 bytes appended; not
  byte-identical by design); old knowledge prefixes 94/94; old lesson prefixes
  20/20; prior verifier files 5/5 identical; 14,943 prior wave and evidence blobs
  identical; QUALITY rows 1–18 identical, rows 19 and 20 added; SOURCES 23→30,
  immutable cells identical. `conformance_gate` is a constant `false`
  (`controls.py:370`) and is not a verdict.
- Source census (`measure.py <SLOT rev>`): knowledge entries 94→95, mapped 95,
  missing 0, dangling 0. SOURCES rows 23→30; tiers A21/B1/C1→A26/B2/C2; statuses
  mined 22→28, rejected 1→2 (S028).
- Scorecard and axes: `<SLOT: SCORECARD round-17 section appended, with axis
  verdicts from measured values only; or "not appended at <rev>">`. Falsifier
  status (attack-pass): temporal-sweep unqualified 4→0 `<SLOT met>`;
  invocation-audit unlabelled 2→11 `<SLOT not met>`; pins red case exit 1 naming
  the path `<SLOT met, retained?>`; QUALITY row 19 presence 0→1 `<SLOT met>`;
  C2 retained runs with pinned carrier, Evidence ID, log sha256 and prediction
  comparison 0→8 `<SLOT met on fields, receipts invalid>`; capability row for
  retained Ghidra-session log 0 `<SLOT not admitted unless receipt-validate
  exits 0>`.
- Limits: no target execution (REA analyze is static; carriers were never run);
  no Go 1.27 symbol recovery claimed; no selector law changed (r16 `selection.py`
  reused as-is); no SHONEN `[x]`, promotion or outside verification by author
  seats. Tool installs or updates in this round: `<SLOT: tool, version, channel,
  reason; none by this draft's author pass>`.
