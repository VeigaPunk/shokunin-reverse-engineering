# ReviewerC1 — adversarial review of R84-C1 (calibration: a claim names its counter)

Seat: reviewer. Lane: `kaidoku-shokunin`, round 84, wave `r84-w1`. Scope: R84-C1 only.
Frozen inputs read, never edited: `plans/round-84-claims.md`, `.ufo/waves/round-84/claims.json`
(blob at `a5663ddedd157bb9113928f5fe80509d6f3fc7a1` = `3e3f75ce…`),
`.ufo/waves/round-83/claims.json` (blob `30b864cf…`, identical at its freeze `af20aff3`),
`tools/round-84/freeze-precheck.py` (blob `602239f5…` at both `e0de2088` and `a5663dde`),
`tools/round-29/freeze-gate.py` (blob `25b54339…` at BASE/`af20aff3`/`e0de2088`/`a5663dde`/HEAD).
No production edits, no git/jj mutations, no deletions, no `task` spawns.
No tool installs were needed.

## Verdict

- **The R84-C1 measurement is SOUND at the measured revision.** The exact command, run against
  the pinned blob `602239f5…`, returns exit 0 with `mismatches []`, `refused_expected 1`,
  `accepted_expected 1`, `met true`, round-83 `FLAGGED` with exactly
  `CLAIM_NO_COUNTER_PATH:R83-C1` and round-84 `CLEAN` with no findings, each equal to its
  declared `--expect`. I re-derived the expectation from the containers before running and it
  matches the plan. The maintained gate at the same revision reports round-84 CLEAN and exits 0.
- **The gate is UNSOUND as the general property in its title** ("a claim names its counter").
  Two demonstrated false-accept paths are high severity: a counter path anywhere in the claim
  object (including `kill_rule`, `id`, `axis`, or a negated sentence) satisfies it (H1), and the
  pin is compared against the measured revision rather than the freeze revision, so an
  undisclosed re-pin passes (H2).
- **The evidence chain is not admissible as it stands** (H3, process/provenance): the pinned
  counter's working-tree copy was modified at 16:46:03 during this wave (digest `4aae3f26…`,
  uncommitted `M`) while the counting command executes the working-tree path, not the git blob.
  `.ufo/waves/round-84/l1/scores/c1-at-container.json` (16:46:07) was produced 4 s later from
  those unpinned bytes. The frozen blob still reproduces the claim exactly; the fix is to
  regenerate the receipt from the pinned blob, or commit the change and re-freeze
  container+pin+declaration. I did not revert or edit anything.

## 1. Independent re-run (exact command, frozen bytes)

Command as assigned. Receipts: `w1/ReviewerC1/precheck-exact.json` (run before the 16:46 edit),
`precheck-exact-frozen.json` (executed from the a5663 blob copied to scratch, identical bytes to
the first run, `cmp` equal), `precheck-exact-worktree.json` (current working tree).

| Field | Frozen blob `602239f5…` | Current working tree `4aae3f26…` |
|---|---|---|
| exit | 0 | 0 |
| round-83 verdict/findings | `FLAGGED` / `[CLAIM_NO_COUNTER_PATH:R83-C1]` | identical |
| round-84 verdict/findings | `CLEAN` / `[]` | identical |
| mismatches | `[]` | `[]` |
| refused/accepted | 1/1 | 1/1 |
| met | true | true |
| control | `{accepted:true, rule:instruments-only}` | `{accepted:true, container:round-84, expected:CLEAN}` plus `controls[]` (both containers) and `control_fired:true` |

The two versions differ only in control accounting; `check_container` is unchanged, so the
verdicts/findings are version-independent.

## 2. Expectation re-derived (not read off the plan)

At `a5663dde`:

- Round-83 container: one claim `R83-C1`; its four strings (`id`, `axis`, `predicate`,
  `kill_rule`) contain no `tools|corpus|.ufo` + `.py/.sh/.mjs/.js` token →
  `named = []` → exactly one `CLAIM_NO_COUNTER_PATH:R83-C1`. The container's top-level pin is
  `tools/round-83/attribution-audit.py = 386e7891…`, which does match the blob at the rev, but
  the code `continue`s on the empty-path branch (line 91), so no blob/pin finding can follow.
  Verified identical text at freeze `af20aff3` (`30b864cf…`), so the finding is not a revision
  artifact.
- Round-84 container: three claims, each naming exactly its own counter and nothing else —
  C1 → `tools/round-84/freeze-precheck.py`, C2 → `tools/round-84/mutation-closure.py`,
  C3 → `tools/round-84/nested-sqfs.py`. All three are blobs at the rev (digests `602239f5…`,
  `fd8aee39…`, `08353f36…`, identical at `e0de2088`) and all three are pinned at those exact
  digests in `instruments` → `CLEAN`. The `fixtures` block is not a pin source and no claim
  string names a fixture path, which is why no phantom-path finding fires (see M1).

## 3. Every reason the gate can fire, and benign false refusals

Exhaustive from the frozen source (line anchors in `tools/round-84/freeze-precheck.py`):

| # | Code / exit | Trigger | Can it refuse a *valid* container for a benign reason? |
|---|---|---|---|
| 1 | `CONTAINER_UNPARSABLE:<err>` | container blob is not JSON | Only for a genuinely invalid file; but a UTF-8 decode with `errors=replace` can turn a corrupt blob into a JSON error, which is the right answer anyway. |
| 2 | `CONTAINER_NO_CLAIMS` | `claims` missing, empty, or not a list | Yes, coarsely: a dict `claims` (a plausible authoring slip) is reported as "no claims" with `claims: 0` rather than a schema error. |
| 3 | `CLAIM_NO_COUNTER_PATH:<id>` | no script token in *any* string of the claim object | Yes: a counter that is not `.py/.sh/.mjs/.js` (JSON receipt, notebook, Makefile, binary) or not under `tools|corpus|.ufo`; a counter written as an absolute path or `./tools/...` (leading `/`/`.` fails the lookbehind); a bare filename; a claim that legitimately delegates measurement to a data file. Measured: absolute → `CLAIM_NO_COUNTER_PATH:X`; `./tools/...` → same; `bin/counter.py` → same. |
| 4 | `COUNTER_BLOB_ABSENT:<path>` | named path not readable by `git show rev:path` | Yes, via misparse: the regex has no trailing boundary, so **any `.json` path is captured as `.js`**. Measured: `.ufo/waves/round-84/mutants.json` → `COUNTER_BLOB_ABSENT:.ufo/waves/round-84/mutants.js`; `tools/round-84/claims.json` → `tools/round-84/claims.js`. A container that cites its frozen fixture (exactly the metadata this plan asks for) is refused over a path nobody wrote. Round-84 escapes only by keeping fixture paths out of claim strings. |
| 5 | `COUNTER_PATH_NOT_PINNED:<path>` | named path not in `instruments`/`loaded_by_counter`/`producers_not_counters` | Yes: a pin carried inside the claim object (`counter: {path: digest}`) → refused. Also any additional named producer/target script (e.g. naming `mutation-closure.py` as a target inside C1) forces a pin; resolvable, but it conflates producers with counters. |
| 6 | `COUNTER_PIN_MISMATCH:<path>` | pin ≠ sha256(blob at `--rev`) | Yes across revisions: the gate has no `instrument_supersessions` concept, so a container pinned at its freeze is refused at any later rev where the counter changed. The maintained gate treats the same state as `INSTRUMENT_REVISED` with a disclosure path. |
| 7 | `UNREADABLE` + `CONTAINER_BLOB_ABSENT`, exit 2 | container path not a blob at `--rev` | Correct refusal; note `git_blob` does not check object type (L1). |
| 8 | exit 1 with `met false` | any verdict ≠ expect (or FLAGGED without expect), or no `refused≥1`/`accepted≥1` pair, or recorded control not accepted | Yes structurally: a lone FLAGGED container with the correct `--expect` has `mismatches []`, `refused 1`, `accepted 0` → `met false`, exit 1 (measured; also the BASE receipt's shape). The gate cannot green-light a single correctly-refused container. |

## 4. Soundness attacks (false accepts), measured against the frozen blob

| ID | Attack | Measured result |
|---|---|---|
| H1 | Move the counter path out of the predicate: append it to `kill_rule`, or put it in `id`, or in `axis`, or mention it negated ("does not run tools/...") | All four return `CLEAN` on the round-83 container. The exact routed requirement — the *predicate sentence* must name the counter — is not enforced: `strings(claim)` spans the whole claim dict (line 52/89). One non-predicate sentence defeats the round-83 finding. |
| H1b | Any pinned script satisfies any claim | `CLEAN` for a calibration claim whose text names `nested-sqfs.py`; a bare-string claim (not a dict) naming a pinned path also returns `CLEAN`. The gate binds a name to a pin, never the claim to the script's measurement. |
| H2 | Silent re-pin after a post-freeze counter edit | Round-73's committed container is `CLEAN` at `a5663dde`; it stays `CLEAN` with `instrument_supersessions` stripped, although four named counters changed between its freeze `8b928422` and the rev (1–2 commits each). The gate compares `pinned[path]` to `sha256(blob(path) at --rev)` (lines 94–102), never to the freeze blob, so disclosure is optional. C1's kill rule says "not pinned at its frozen digest"; the instrument does not test that. |
| M2 | Extension truncation | `tools/round-84/freeze-precheck.python` and `....pyc` both return `CLEAN` as if they named the real `.py` (no `(?![A-Za-z0-9_-])`). The maintained gate flags the same text `INSTRUMENT_NONE`, so the two gates disagree and the new one accepts a non-existent path. |
| M3 | Pin shadowing | `instruments = {path: 0*64}` plus `producers_not_counters = {path: correct}` → `CLEAN`: `pins()` merges keys in order and the last write wins. The maintained gate shares this merge order. |
| L2 | No container schema/id checks | Wrong `schema`, `round: 3`, duplicate claim ids, and a `claims` list of bare strings all pass as long as the token+pin shape is met. |

## 5. Control analysis

- **Does it fire?** Yes, as a shape predicate: `cheap_rule(round-83)` = `accepted true` (measured
  standalone and via `--container round-83 --control`), because `instruments` is a non-empty dict.
- **Would a file-shaped container pass it?** Yes: `{"instruments": {"x": "y"}}` with zero claims →
  `accepted true`, while `check_container` refuses it with `CONTAINER_NO_CLAIMS`. The control
  therefore proves the cheap rule cannot reach the verdicts, which is its purpose.
- **Does the C1 receipt evidence the round-83 acceptance?** No, on the frozen bytes: `main()`
  overwrites `receipt["control"]` for each `--container` (lines 244–250), so with the C1 order the
  single `control` field belongs to the round-84 container. Measured with a third, no-instruments
  container last: `control.accepted false` even though round-83's own control is `true`. The
  property is true; the frozen receipt does not attribute it. The 16:46 working-tree edit adds
  `controls[]` per container and `control_fired`, which fixes this — on unpinned bytes (H3).
- **Control absence is green:** running the exact command without `--control` gives
  `control: null`, `met: true`, exit 0 (measured; `precheck-no-control.json`). The kill rule's
  "a control that does not fire" is enforced by the caller, not the instrument. ExecGateForge's
  `combined.json` (16:41:51, frozen bytes) is exactly this shape — `control: null`, `met true` —
  and its report calls it "the C1 counting-command shape"; it is not, because the C1 command
  passes `--control instruments-only`.

## 6. Maintained gate `tools/round-29/freeze-gate.py` at the same revision

`--rev a5663ddedd157bb9113928f5fe80509d6f3fc7a1 --require-clean round-84`
(receipt `w1/ReviewerC1/freeze-gate-r84.json`): exit **0**, `audited 59`, `clean 32`,
`required_failed []`, round-84 `CLEAN`, findings `[]`, instruments the three tools, freeze
`a5663dde`; round-83 `FLAGGED` with the single finding `INSTRUMENT_NONE`. At HEAD the same
command is also exit 0 with round-84 CLEAN (`freeze-gate-head.json`). The round-84 predicate text
is sufficient for the maintained gate at this revision.

With `--disclosures corpus/claim-freezes-v2.tsv` the same rev exits **1**: 58/59 rows exact,
`missing: ["round-84"]` (`freeze-gate-ledger-a5663.json`). At BASE it exits **0** with 58/58 exact
(`freeze-gate-ledger-base.json`), matching the plan's "Before" sentence and the pre receipt.
So "exits 0 on the disclosed ledger" is true of BASE today, not yet of `a5663dde`; the round-84
ledger row is still an open standing duty. This is a state note, not a predicate kill.

The "stays byte-unchanged" claim holds: `freeze-gate.py` is `25b54339…` at BASE, `af20aff3`,
`e0de2088`, `a5663dde` and HEAD.

## 7. Is the round-83 finding exactly `CLAIM_NO_COUNTER_PATH:R83-C1`, not a cascade?

Yes. Exactly one finding. By control flow, not luck: the claim has no script token, so the loop
`continue`s before `COUNTER_BLOB_ABSENT`/`COUNTER_PATH_NOT_PINNED`/`COUNTER_PIN_MISMATCH` can be
reached; the container's top-level pin is never consulted for a claim with no path. The
container text is identical at its freeze (`af20aff3`) and the measured rev (`30b864cf…`), so no
revision artifact contributes. The pin that *is* present is correct (`386e7891…`), so a repaired
predicate would be CLEAN; the single finding is precisely the predicate defect.

## 8. Kill-rule audit for R84-C1 (at `a5663dde`, pinned blob)

| Kill-rule clause | Status | Evidence |
|---|---|---|
| any verdict/expectation mismatch | not triggered | `mismatches []` |
| round-84 not CLEAN | not triggered | `CLEAN`, `[]` |
| round-83 not FLAGGED with that exact finding | not triggered | exactly `CLAIM_NO_COUNTER_PATH:R83-C1` |
| control fails to accept round-83 | not triggered factually | `cheap_rule(round-83).accepted true`; frozen receipt does not attribute it (M5) |
| control reaches target without per-claim check | not triggered | `check_container` ran on both containers |
| changed predicate or container set | not triggered | container blob at `a5663dde` equals the declared one; unchanged at HEAD |
| named counter not a blob at measured rev / not pinned at frozen digest | not triggered | all three blobs at `a5663dde` and `e0de2088`, pins match (`602239f5…`, `fd8aee39…`, `08353f36…`) |
| maintained gate byte-unchanged | not triggered | `25b54339…` at five revisions |

Caveat: the last clause is true of this container, not something the instrument verifies (H2).

## 9. Live working-tree changes observed during the review (not mine)

| Path | State | Evidence |
|---|---|---|
| `tools/round-84/freeze-precheck.py` | `M`, mtime 16:46:03, digest `4aae3f26…` vs pin `602239f5…` | diff adds per-container `controls[]`, `control_fired`, one selftest case (10 → 11 cases, both selftests 0 failures); verdict logic unchanged |
| `tools/round-84/nested-sqfs.py` | `M`, mtime 16:48:09, digest `e0364dde…` vs pin `08353f36…` | adjacent C3 exposure, outside this review's scope |
| `PROVINCE.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/lessons/round-83.md` | `M` | other seats' standing-duty work |
| `.ufo/waves/round-84/l1/scores/c1-at-container.json` | mtime 16:46:07, new schema (`controls`, `control_fired:true`) | C1 receipt produced from the edited, unpinned working tree |

I made no edits and ran no mutating git/jj. The frozen blob is intact in git and reproduces the
claim; the working-tree edit is what breaks pin→execution binding for receipts produced after
16:46:03. Recommended integrator action (not performed here): either restore the frozen bytes
for the C1 measurement, or commit the change and re-freeze the container/pin/declaration so the
receipt and the pin name the same bytes.

## 10. Residual risk

- A future container can pass with the counter named only in `kill_rule`/`id`/`axis` or in a
  negation (H1); the gate would report CLEAN for metadata the round-83 review explicitly routed
  against.
- A post-freeze counter edit with an updated pin passes without disclosure (H2, round-73 proof).
- `CLEAN` never proves the named script is the one that measured the claim (H1b).
- The control is a shape check; its acceptance is evidence about the cheap rule, not correctness.
- Working-tree edits to pinned counters are invisible to the gate (it reads git only), so
  pin-to-executable binding depends on process, not on the instrument.
- `met` is true when `--control` is omitted, so a re-run can look green while skipping the
  control the claim's kill rule requires (M4).

## 11. Verification gaps

- No `lsp` device is mounted in this seat's toolset; caller/definition checks were done by
  full-source read plus execution of the frozen blob (`frozen-blob-602239f5-freeze-precheck.py`,
  digest verified), not by grep as semantic proof.
- The tree-typed-blob concern (L1) is code reading only; there is no tree named in a claim at
  `a5663dde` to exercise.
- I did not review C2/C3 counters or their evidence; the `nested-sqfs.py` working-tree change is
  noted, not adjudicated.
- I did not establish who made the uncommitted production edits.

## Receipts

All under `.ufo/waves/round-84/w1/ReviewerC1/`: `precheck-exact.json`,
`precheck-exact-frozen.json`, `precheck-exact-worktree.json`, `precheck-no-control.json`,
`precheck-r83-only-control.json`, `precheck-control-lastwins.json`, `freeze-gate-r84.json`,
`freeze-gate-head.json`, `freeze-gate-ledger-a5663.json`, `freeze-gate-ledger-base.json`,
`selftest-frozen.json`, `selftest-wt.json`, `probe.out`, `probe2.out`, `probe3.out`,
`stripped.out`, `probe.py`, `probe2.py`, `frozen-blob-602239f5-freeze-precheck.py`.
Scratch `/fast/scratch/hyaku/kaidoku-r84/ReviewerC1/` was copied here and removed before yield.
