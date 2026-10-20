# Round 17 W2 — pre-judgment of the learning-trend verdicts

Revision attacked: `da64646adcb19c1ede7537b799b8c7d283fe43da` (baseline
`b563c799d97774aae4351276fe43cb897311e349`; predictions frozen at
`271167473d87ef710f07ecdd98caf0ce12091686`). Read-only: no REA
analyze/search/decompile, no analyzeHeadless, no carrier executed, no file
edited except this report. Python always `-B`; scratch in `/tmp`. No tool
install or upgrade was needed.

## Answer first — the honest verdicts

The table is INFERENCE from the observations cited below (commands and outputs
are under Findings / bounded no-findings). This is an author-side w2 falsify
seat, not the outside closure.

LEARNING.md:26-38 asks for one verdict each, from artifacts, not self-assessment.

| Trend | Honest verdict at this revision | Why |
|---|---|---|
| **expansion** | **unchanged as ground; no `improved`.** If the entry is left as landed, the strict LEARNING harm condition (`an admitted entry fails the bar it was admitted under`) applies -> **harmed** until corrected. | The new entry is on the held Go row, not uncovered ground; its `source:` cites only `mined` rows (necessary, not sufficient). The only expansion observable left is the capability row, and it is absent (`measure.py` -> `C2_scorecard_capability_row: 0`), while its gate (`receipt-validate.py` exit 0) fails on all 8 receipts. |
| **quality** | **unchanged at best; not `improved`.** The r16 `:95` overclaim correction is real, but the admitted entry fails its own stated `recheck:` and its mid-run equality sentence lacks retained instants; `improved` is available only after F1/F2 are fixed. | Old 94 knowledge entries are byte-identical; no existing entry re-verified/superseded by a new entry. The new entry's `recheck:` returns exit 1 on every carrier receipt (F1), and its "no mid-run check differed"/Gate "pins equal pre/mid/post" is not backed by retained mid-run records (F2). |
| **discernment** | **unchanged** for round 17's own gate; a blanket `improved` would be self-attestation. | The round's Gate is explicitly author-side (`corpus/lessons/round-17.md:22`); no non-author sampled r17 admits/rejects. The r16 outside routes are only partly discharged: provenance -> QUALITY #19 (grounded, cites the r16 spotcheck); invocation -> citation-drift fixed, but the generalized claim fails 2 -> 11 unlabelled rows and the custody-pair row cites a receipt that does not exist (F3). |

What "Go held ground" means here: `corpus/README.md:35` already listed
r14/r15/r16 on this row; the r17 entry was appended to it (map 94/94 ->
95/95, `w2/measure-base.json`, `w2/measure-head.json`). The lane's own
precedent says this is not expansion: `SCORECARD.md:2218` (r14), `:2282`
(r15), `:2307` ("the new entry deepens held Go, not expansion"), `:2339`
(r16), `:2317` ("no capability-table row"). The r17 entry itself opens by
saying r14-r16 held this ground (`knowledge/2026-10-20-r17-go-carrier-diagnostics.md:9-12`).

The *only* path to `expansion: improved` at this revision is the capability
admission ("a capability admitted to SCORECARD.md", LEARNING.md:30-31). That
requires F1 fixed first: `claims.json` C2 says the capability row is entered
"only if receipt-validate exits 0"; the validator currently rejects the round's
own receipts. With F1 fixed and the row entered, the ground entry itself still
stays `unchanged`; only the capability observable moves.

## Findings

### F1 (High) — the receipt gate rejects all eight of the round's own carrier receipts; the new entry's `recheck:` therefore fails

- `tools/receipt-validate.py:98` classifies `carrier` only when
  `isinstance(receipt.get("steps"), list)`; `:284` then iterates
  `receipt.get("steps") or []` as a list.
- `tools/carrier-run.py:275` initializes `"steps": {}` and `:349` assigns the
  dict keyed by step name (`inspect-go-binary`, `analyze`, `search:*`).
- Command (the eight explicit `runs/<label>/receipt.json` paths; labels
  `calib-esbuild-0.25.12 calib-shfmt pro-aether pro-containerd-shim
  pro-esbuild-0.21.5 pro-esbuild-0.27.7 pro-notesmd-cli pro-op`):
  `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py
  .ufo/waves/round-17/runs/calib-esbuild-0.25.12/receipt.json
  .ufo/waves/round-17/runs/calib-shfmt/receipt.json
  .ufo/waves/round-17/runs/pro-aether/receipt.json
  .ufo/waves/round-17/runs/pro-containerd-shim/receipt.json
  .ufo/waves/round-17/runs/pro-esbuild-0.21.5/receipt.json
  .ufo/waves/round-17/runs/pro-esbuild-0.27.7/receipt.json
  .ufo/waves/round-17/runs/pro-notesmd-cli/receipt.json
  .ufo/waves/round-17/runs/pro-op/receipt.json`
  -> `{"invalid": 8, "receipts": 8, "unreadable": 0, "valid": 0}` exit 1;
  every receipt is `kind: "unknown"` with finding
  `unrecognized_shape: receipt matches neither retain nor carrier shape`.
- Both selftests are green with mutually incompatible shapes:
  `pins.py --selftest` -> `SELFTEST: CLEAN cases=7` (red case observed);
  `carrier-run.py --selftest` -> `SELFTEST: CLEAN cases=2` (asserts
  `steps["analyze"]`, dict); `receipt-validate.py --selftest` ->
  `SELFTEST: CLEAN cases=5` (fixture at `:470` uses `"steps": [ ... ]`).
  The pair is only tested against itself, never producer -> validator.
- Consequence: the new entry's `recheck:`
  (`knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3`) returns exit 1 on
  every stated receipt; `claims.json` C2's capability admission gate cannot
  pass; the SKILL `receipt-validate` gate is not able to validate the round's
  own artifacts.
- Smallest fix: normalize in the validator — accept `dict` in `classify`,
  and iterate `steps.values()` in the step checks (or normalize to a list
  before both); add one selftest case built from a `carrier-run.py`-shaped
  receipt (dict `steps`). Re-run; expected `valid: 8, exit 0`.

### F2 (High, calibration) — the admitted entry and its Gate/Mistakes claim mid-run pin equality that the retained receipts do not record

- Entry `:27-29`: "were hashed before, every 30 s during, and after each
  session ... All eight pre/post compares are equal and no mid-run check
  differed."
- Lesson `:26`: "8 receipts ... pins equal pre/mid/post"; lesson `:73`:
  "`tools/pins.py` (pre, 30 s mid-run and post maps with timestamps)".
- Observed: `sed -n '386,445p' .ufo/waves/round-17/tools/carrier-run.py`
  shows a throttled mid-run snapshot that records **only**
  `rec["pins_changed_during_run"]` when a comparison differs; the snapshot
  itself, its timestamp and a check count are not retained.
  Key-walk all 8 receipts (`python3 -B` over `json.load`, collecting keys
  containing `pins_`) -> every label prints exactly
  `['/pins_compare', '/pins_post', '/pins_pre']`; no
  `pins_changed_during_run` and no mid-run map exists. The step's `polls`
  field counts log-scan cycles, not pin checks; no pin-check count or
  timestamp is recorded.
- Consequence: the pre/post equality is evidenced (146 paths, equal maps,
  UTC timestamps); the **mid**-run equality and "pre/mid/post" are not
  evidenced at named instants. QUALITY #19 (`QUALITY.md:29`), admitted this
  round, says temporal-stability claims need records at named instants and
  that equal maps show only the recorded instants. The entry repeats the class
  R16-PROVENANCE was added to stop.
- Smallest fix: reword cheaply, no rerun — entry: "pre/post maps are equal;
  the tool checked every 30 s and would record a changed path, but the mid-run
  maps/instants were not retained, so only pre/post equality is evidenced";
  Gate `:26` and Mistakes `:73` the same. Or, if a mid-run claim is wanted,
  retain timestamp + map digest per check in `carrier-run.py` and rerun.

### F3 (High, calibration) — C1(b)'s own falsifier fails: unlabelled registry rows 2 -> 11, and the custody-pair row cites a receipt that does not exist

- `SKILL.md:449` (custody-pair) says "exercised argv retained in
  `.ufo/waves/round-17/verification.json`"; `SKILL.md:448` (citation-drift)
  names the same file as an exercised argv source.
- `git cat-file -e da64646:.ufo/waves/round-17/verification.json` -> exit 128
  (path does not exist at the revision; the draft measured-records file is not
  landed).
- `python3 -I -B .ufo/waves/round-17/tools/invocation-audit.py --root . --rev da64646...`
  -> `rows: 17, exercised_match: 6, labelled_unexercised: 0,
  unlabelled_variant: 11`; custody-pair has `matched_receipt: null`, and the
  10 new round-17 registry rows are also unlabelled.
- Baseline b563c79 -> `rows: 7, exercised_match: 5, labelled_unexercised: 0,
  unlabelled_variant: 2` (citation-drift, custody-pair). Citation-drift is now
  `exercised_match` (against round-16's receipt); custody-pair is not.
- `corpus/lessons/round-17.md:74` says "Both rows now advertise the exercised
  isolated absolute argv, re-exercised this round with retained argv"; `LOG.md:2065-2066`
  says "SKILL rows citation-drift/custody-pair aligned in place". Both are
  false at this revision for custody-pair (and the new rows).
- w1 already recommended the honest form: `w1/ScoutRegistryRows.md:21`
  ("no argv receipt anywhere"; receipt has no argv field) and
  `w1/draft-lesson-mistakes.md:15` ("exercised; argv not retained" with its
  receipt path).
- Consequence: `claims.json` C1(b) "unlabelled M -> 0" is 2 -> 11; the round's
  own falsifier is red, and the lesson/LOG claim is a fresh instance of the
  reference-drift class R16-INVOCATION targeted.
- Smallest fix: create the promised `.ufo/waves/round-17/verification.json`
  with the actual argv for the round-17 tools and a custody-pair `capture`
  argv (or label custody-pair "exercised; argv not retained" with
  `arc3-loop1-round2/claims/c3/EX-33/receipts/custody-live.v2.json`, and label
  placeholder rows "unexercised variant"), then rerun the audit; do not write
  "M -> 0" until the audit prints 0. Correct lesson/LOG wording first.

### F4 (High, expansion) — the promised capability row is absent, and its gate cannot pass

- `SCORECARD.md:617-622` has four capability rows; none names
  `retained REA Ghidra-session log`. SCORECARD has no round-17 section, and
  `git diff --name-only b563c79 da64646 -- SCORECARD.md` is empty.
- `measure.py:46` `CAPABILITY_TEXT = "retained REA Ghidra-session log"`;
  running `python3 -I -B .ufo/waves/round-17/measure.py da64646...` ->
  `C2_scorecard_capability_row: 0`, `scorecard_capability_rows_matching: 0`.
  (`w2/measure-head.json` retains the same result; base was 0 too.)
- `claims.json` C2 says the row is entered only if `receipt-validate.py` exits
  0; F1 shows exit 1 on all 8 receipts.
- Consequence: the only expansion observable the round claims is not landed,
  and its stated gate is failed. The 8 bound runs and `pins` are real
  (see no-findings), but the capability is not admitted to the scorecard.
- Smallest fix: fix F1, run the validator on the 8 receipts (expect valid 8,
  exit 0), then enter the capability row in SCORECARD with the entry + receipt
  pointers and re-run `measure.py` at the new revision. If not, record
  `expansion: unchanged` and drop the capability claim.

### F5 (Low) — the new entry's body cites a non-existent frozen commit

- Entry `:37`: "committed at `2716747` before the first run." The real frozen
  commit is `271167473d87ef710f07ecdd98caf0ce12091686` (short `2711674`):
  `git cat-file -e 2716747^{commit}` -> exit 128; `git show -s` on the real
  hash -> 2026-10-20 10:46:45 -0300. Entry line 1 and lesson `:26` use the
  correct hash.
- Smallest fix: replace `2716747` with `2711674`.

### Observational note (no finding) — the r16 temporal correction lives in LOG/lesson, not in the r16 file

- The r16 overclaim at `knowledge/2026-10-20-r16-go-selection-preview.md:95`
  is corrected by named lines (`LOG.md:2062`, lesson corrections), not in the
  entry itself. That matches the lane's append-only convention and the r16
  spotcheck's instruction ("never rewrite filed bytes"), so no harm — recorded
  here as a no-finding with the caveat that a reader of the entry alone still
  sees the overclaim. QUALITY #19's model is exactly "a named append-only line
  carrying the exact file:line", so this is compliant; no fix required.

## Bounded no-findings (what I checked and did not find broken)

- Run integrity: all 8 `carrier-run.exit 0`, `compare.exit 0`,
  `compare.json all_match: true`, `pins_compare.equal: true`,
  `bound_sessions: 1`, `unbound_sessions: 0`. Go version / route / bootstrap
  fields match the entry table: `go1.27.0-X:nodwarf5` none/missing,
  `go1.23.12` info, `go1.25.8` fallback->1.25.0, `go1.25.14` fallback->1.25.0,
  `go1.20.12` info, `go1.27.2` none/missing, `go1.26.8` none/missing,
  esbuild 0.27.7 no build info; all 8 report
  `x86:LE:64:default:golang`.
- Freeze before observation: 18 prediction files (8 pairs + SHA256SUMS +
  carriers.tsv) are in commit `2711674` at 13:46:45 UTC; first receipt pre
  snapshot 13:47:05.973 and first analyze start 13:47:06.688 — before the first
  run. Calib carriers were pilot-seen; the six `pro-*` were not. The two
  calibration analyze evidence IDs repeat the pilot IDs
  (`ev_2b29a1dd…`, `ev_391dbfe6…`).
- Entry table counts: 4881 (calib-esbuild 0.25.12), 2302 (notesmd-cli),
  4411 (esbuild 0.21.5), 6115 (aether) Go types and 7200 Go strings (aether)
  match the bound logs; the aether `EOFException` is at
  `runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log:177`, failure at `:97`,
  and the entry labels the cause UNKNOWN.
- Source leg: `corpus/README.md:35` gained the entry; `w2/measure-head.json`
  has 95/95 mapped, no missing/dangling; `SOURCES.md` S003/S023/S024/S025/
  S026/S029 are `mined`, S028 `rejected`, and the used-by cells include the
  entry; `scripts/sources-census.sh validate --today 2026-10-20 --root
  /home/vgpnk/Projects/shokunin kaidoku` -> `kaidoku ok`, exit 0.
- C1(a): `temporal-sweep.py --rev da64646 --sites-rev b563c79` -> `sites 4,
  corrected 4, unqualified 0`; at baseline `sites 4, corrected 0,
  unqualified 4`; the four sites are LOG.md:2012, round-16.md:154,
  round-16/verification.json:419, r16 knowledge:95; corrections are in
  `LOG.md:2059-2062` and the lesson. `pins.py --selftest` -> 7 cases clean,
  red case names the mutated path.
- QUALITY: #19/#20 present (`QUALITY.md:29-30`); #19 cites
  `round-16-verifier-spotcheck.md:183` (R16-PROVENANCE); rows 1-18 are
  byte-identical (`w2/controls.json` `quality_admission_rows`), added rows
  `["19","20"]`.
- Controls: 94 old knowledge files byte-identical, four prior verifier files
  unchanged, LOG old prefix preserved, `w2/controls.json` old-knowledge
  94/94; no dangling map entries.
- r16 outside sample: the three sampled r16 decisions all `agree`
  (`round-16-verifier-spotcheck.md:143-145`); the two routed defects are at
  `:183-184`. Round 17 has no equivalent non-author sample.
- Citation-drift at HEAD: `w2/citation-drift-head.json` exit 0,
  `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.

## Residual risk and verification gaps

- This is a pre-final revision. F1-F5 are all fixable before the L1's final
  measured pass; the verdicts above are what the artifacts support **now**, and
  the smallest fixes would change the admissible verdicts.
- The mid-run pin checks are code-real but unretained. The absence of
  `pins_changed_during_run` in the receipts is evidence only of "no detected
  change at an unrecorded instant"; it is not a pre/mid/post measurement.
- `receipt-validate.py --selftest` is green with a list fixture, so it cannot
  catch the dict-shape producer it is paired with. Any fix must be exercised on
  a real receipt, not only the selftest.
- The outside closure's r17 admit/reject sample is the only thing that can make
  `discernment: improved` honest; w1/w2 seats are the lane, and the round's
  Gate says so.
- `.ufo/waves/round-17/verification.json` (the promised measured-records file)
  is absent at the revision; the LOG's "measured values follow" is a draft,
  and the SCORECARD round-17 section (with the trend verdict line) is not yet
  written. No round-17 trend line was found landed at `da64646`; the only
  round-17 trend text is the slot skeleton `w1/draft-scorecard.md:64` and
  `w1/draft-report.md:50-56`.
