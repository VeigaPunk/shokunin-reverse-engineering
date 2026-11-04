# Round 84 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Subject: kaidoku round 84, lane HEAD `1598ee68943807845f04f52d057e01be6b5ddfe4` (base
`043b89a25241710a68b45526c3287fb3c8d907c3`). Report `.ufo/reports/round-84/kaidoku.md` (fleet
commit `be33e97dc7663746355ed4b6fa973f5025f40ef1`, lane identity `kaidoku-shokunin`). Dispatch digest
(`.ufo/watchdog.log`, copied at closure): `2026-11-04T16:23:22-03:00 launch kaidoku round=84
pgid=2142648 driver=hyaku-inline attempt=1`; `2026-11-04T17:12:17-03:00 complete kaidoku round=84;
hyaku-inline attempt=1`. Method: plain measurement over committed bytes (`git show`, `git cat-file`,
`jq`, `grep -c`, `sha256sum`, `curl`). Per PROTOCOL §Gate standard, the lane's three tools were
**not executed**; their committed receipts were verified against the revision they name and the
container's pinned digests. Reviewer statements below are my own re-measurements, not seat reports.

## 1. Step-1 conformance

| check | observed | result |
|---|---|---|
| report author | `git log -- .ufo/reports/round-84/kaidoku.md` → `kaidoku-shokunin <kaidoku@shokunin.local>`, `be33e97d…` | ok (lane identity) |
| report after cited work | `1598ee68` committed 17:09:34-03:00; report committed 17:10:36-03:00 | ok |
| `SHONEN` heading, one line per box | `## SHONEN` with 4 lines; `SHONEN.md` has 4 boxes | ok |
| required sections | Work performed, Landed changes, Before→after, Sources & frontier, Trend verdicts, SHONEN present, in order | ok |
| cited commits (9) exist and are ancestors of `main` | `e0de2088 a5663edd b15d8083 4a8362be 8ae9c8ee 26f4e1ba 4419abf6 16be078a 1598ee68` — `merge-base --is-ancestor … main` all OK | ok |
| base ancestry | `043b89a2` is an ancestor of `main` | ok |
| lane state | `jj-lane.sh state …kaidoku-shokunin` → `branch=main local=1598ee68 remote=1598ee68 ahead=0 behind=0`, exit 0 | ok, pushed |
| lane leftovers | `git status --porcelain` in the lane: empty | ok |
| `ls-remote origin refs/heads/main` | `1598ee68943807845f04f52d057e01be6b5ddfe4` | ok |
| dispatched prompt carries the template contract | `.ufo/prompts/kaidoku-round-84.md` §4 report contract, §5 commit/push scope, L0 side channel, §2b frontier step, §6 campaign addendum present | ok; L2 route map in §6 not reconciled line-by-line against `MISSION.md` (not checked here) |
| L2 floor (≥8 in one batched swarm) | one v1 wave, 14 seats (5 executor, 2 scribe, 1 scout, 2 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 connector) | ok |
| attack share / connector cap | 4/14 = 28.6 % attack; 1 connector | ok (run-15 band 8–16) |
| planner seat | none dispatched; L1 holds the planner seat | **conformance defect, status-neutral**: the report names the deviation (validator excludes planner); MANIFEST `kaidoku` notes already asked for it |
| frontier step | census before/after (§3); mined mistakes M84-1…M84-7; sourced claim via S301/S302 in the knowledge entry | ok |
| marker rule | report is substantive (work, pointers, commits) | not a marker → `ok` |

## 2. Claims — re-derivation

Claims are declared in `plans/round-84-claims.md` (frozen at `e0de2088`) and the container
`.ufo/waves/round-84/claims.json`. Pinned instrument digests in that container equal the HEAD blobs:

```
4aae3f26…  tools/round-84/freeze-precheck.py   (container pin = HEAD blob)
e5cfd2ed…  tools/round-84/mutation-closure.py  (container pin = HEAD blob)
c79dc9b2…  tools/round-84/nested-sqfs.py       (container pin = HEAD blob)
dbb6d4c9…  .ufo/waves/round-84/mutants.json    (table_identity.matches = true)
```

`git diff 16be078a 1598ee68 -- tools` is empty: the measured final revision and HEAD bytes are identical for all tools.

### R84-C1 — calibration: maintained audit vs. prefreeze refusal — **verified (measured)**

- Before (`pre/c1-maintained-gate-base.json`): `audited 58`, `flagged` includes `round-83`; the maintained audit exits 0 on the defective container.
- Before, new gate at BASE (`pre/c1-precheck-at-base.json`): `refused_expected 0`, `accepted_expected 0`, `met false`.
- After, landing `l1/scores/c1-at-landing.json` (rev `4a8362be`) and final `c1-at-final.json` (rev `16be078a`): both `met true`, `refused_expected 1`, `accepted_expected 1`, `mismatches []`, `control_fired true`; round-83 → `FLAGGED` with exactly `CLAIM_NO_COUNTER_PATH:R83-C1`; round-84 → `CLEAN`.
- Re-measured: round-83 `claims.json` has one claim, `R83-C1`, keys `axis,id,kill_rule,predicate`, no counter field. Round-84 predicates name `tools/round-84/freeze-precheck.py`, `…mutation-closure.py`, `…nested-sqfs.py`.
- Limit (lane-disclosed, confirmed by reading the claim text): a naming/pinning lint; a counter path in `kill_rule` or negated prose also satisfies it.
- Evidence basis: receipts re-read and pin digests matched by plain `sha256sum`; tool not executed.

### R84-C2 — depth: frozen mutant table, BASE vs. after — **verified (measured, name-level kill)**

- Before (`pre/c2-base.json`, rev `043b89a2`): `killed 4`, `ok false`; survivors `pin-call, static-refusal, source-mined, source-date, source-base, source-plan, source-entry, sb-header-position, sb-duplicate-last`.
- After (`l1/scores/c2-at-final.json`, rev `16be078a`; landing `c2-at-landing.json` at `4a8362be`): `killed 13`, `ok true`, `survivors` none, `inconclusive` none, `pristine_failed` none, table identity matched.
- Re-measured by `grep -c -F`: `jq -r '.mutants[] | .declared_case'` (13 rows) — **all 13 declared case names occur in their target's committed bytes at HEAD** (`floor-refused` 1, `failures-refused` 1, `binder-refused` 1, `bare-name-refused` 2, and one each for the other nine). At BASE, nine of the thirteen declared case names have 0 occurrences in their target (`runtime-pin-mismatch-refused`, `static-defect-no-execution`, `sourced-row-*`, `sourced-plan-missing`, `sourced-entry-uncited`, `late-single-header`, `duplicate-target-second`).
- Spot-read of one body (`tools/round-82/printed-command.py` L675-700): `sourced_case` calls the production `sourced_arm` (L678), not a re-typed expression, consistent with the lesson's claim.
- Limit (lane-disclosed, confirmed): a kill binds a case name to a failing run. A fabricated case that asserts the declared token would also score green. Not re-proved here; not executed.
- Revision note: the landing receipt (`4a8362be`) and the final receipt (`16be078a`) differ in one docstring hunk of `mutation-closure.py` (`git diff 4a8362be 16be078a`: 5 insertions, 3 deletions, docstring only). Behaviour identical; the container pins the final digest.

### R84-C3 — coverage (capability acquisition): nested container chain — **verified (measured, bounded class)**

- Before: `git cat-file -e 043b89a2:tools/round-84/nested-sqfs.py` fails (file absent at base); `PROVINCE.md:407` and `corpus/README.md` list "nested sub-images below depth 1" as open Frontier. The before is therefore *counter absent*, not a measured zero, and is stated as such by the lane.
- After: `c3-at-landing.json` (rev `4a8362be`) and `c3-at-final-with-provider.json` (rev `16be078a`): `met true`, arms A1–A9 all `true`, `instrument.sha256 c79dc9b2…` (= HEAD blob), fixture pins `a e82c5995…`, `b 7d2dd0e7…`, `c f68b42fa…` (match the lesson text byte-for-byte), `control.fires true`.
- Non-zero exit retained: `c3-at-final.json` / `.execution.json` (exit 1, all arms false) lacks the unblob provider in the Eval environment; the lane kept it and the rerun with `REA_UNBLOB_COMMAND` set (`env_overrides` recorded) exits 0. Accepted as recorded.
- Limit (lane-disclosed): `analysis_depth` is the provider's own field; the before/control are not independent of the pilot; A3 is a suffix match; A9 does not pin the `sasquatch` child. Not re-executed (gate rule).
- Frontier evidence: the new knowledge entry `corpus/knowledge/2026-11-04-r84-nested-container-chain.md` cites S301 and S302 by `source:`; `PROVINCE.md:362` and `corpus/README.md:125,260` carry the round-84 Core note for the bounded class only.

## 3. Sources census and rows

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → terminal `kaidoku ok …/corpus/SOURCES.md`, **exit 0**, 27 W04 duplicate-URL warnings (report says 26 → 27 with S303; matches).
- Measured with `grep -c` over `corpus/SOURCES.md`: base `rows 205 / mined 184 / rejected 21 / tier A 187`; HEAD `rows 208 / mined 186 / rejected 22 / tier A 190`. Matches the report and the lesson census line.
- New row S301 quote: live `curl -sL https://man.archlinux.org/man/mksquashfs.1.en` → HTTP 200, 57 790 bytes, sha256 `3ea8c1a1…` identical to the committed snapshot `.ufo/waves/round-84/l1/sources/mksquashfs.1.en.html`. Located quote present after tag-stripping; word count of the quoted sentence = **24** (≤25, ok).
- New row S302 quote: installed `rea-agents` 6.5.0 file `dist/firmware/FirmwarePublication.js` at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/…` sha256 `bb4f3246…` (matches the row); line 17 `"depth-limited": "Rerun extract_firmware with a higher max_depth (up to 10) and a fresh output_directory to descend into this path."`; quote word count = **18** (≤25, ok). Pointer is a npx cache path, not a committed snapshot (routed R1 below).

## 4. Discernment spot-check (LEARNING.md)

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| S301 mksquashfs(1) `-repro-time` | admit (A, mined) | live URL + committed snapshot (sha equal) | **agree** | Quote is verbatim in the live page and the snapshot; it grounds fixture reproducibility and says nothing about extraction, as the row states. |
| S302 rea-agents 6.5.0 `depth-limited` remedy | admit (A, mined) | installed package file, line 17, sha256 equal | **agree** | The provider's own remedy text is the anchored authority for the gap kind; row's flip-scope ("does not establish how deep vendor images nest") is correct. Pointer hygiene routed (R1). |
| S303 npm tarball as gap-taxonomy authority | reject (A-tier label, status rejected) | `registry.npmjs.org/…/rea-agents-6.5.0.tgz` → HTTP 200 | **agree on the decision; disagree with one reason fact** | A tarball is not an anchored document and S302 is the anchored source; the flip is stated. **Factual error in the reason**: the reason says the URL is held "in five scopes (S083/S090/S092/S119/S123)". `grep -F` finds the identical URL in **seven** prior rows: S079, S080, S083, S090, S092, S119, S123 (routed R2). |

Spot-check result: admits 2 (agree 2), rejects 1 (agree 1). Discernment decision-level agreement on the sample; reason-level defect routed.

## 5. Mistakes (sweep of the lesson `## Mistakes`)

- M84-1, M84-2, M84-3, M84-7: pointers resolve (`.ufo/waves/round-84/l1/mistakes/*`, `l1/archive/c1-at-container.json` under `.ufo/waves/round-84/`).
- M84-6: `w1/ReviewerC3/verify.json` resolves under `.ufo/waves/round-84/`.
- **M84-5: pointer prefix wrong.** The lesson cites `l1/waves/round-84/w1/SentinelScope/esc-receipt.json`; that path does not exist. The file is `.ufo/waves/round-84/w1/SentinelScope/esc-receipt.json` (routed R3).
- **M84-4: no evidence pointer file.** The row's evidence is prose ("the first `score_envelope()` returned `met = all(arms)`"); there is no receipt or diff pointer to resolve (routed R4).

## 6. Per-axis verdicts (owned axes in SCORECARD)

| axis | verdict | basis |
|---|---|---|
| coverage | improved | C3 verified: a previously absent measured class (bounded three-level LE SquashFS v4 chain) moved to measured Core with a capability row. Score 10.0 unchanged (saturated proxy); no score change claimed. |
| depth | improved | C2 verified: 4 → 13 killed on the frozen 13-row table, 9 declared cases now present in committed target bytes. Name-level kill limit disclosed; not treated as semantic certification. |
| calibration | improved | C1 verified: refusal arm 0 → 1 with control firing; round-83 defect now refused. Naming-lint limit disclosed. Score 10 unchanged (saturated). |
| freshness | unchanged | Not a claim this round; SCORECARD freshness row unchanged (diff touches only the coverage row among axis rows). |

No axis is harmed: the SCORECARD diff against base changes only the coverage row among axis rows (text refreshed, score 10.0 kept).

## 7. Trend verdicts (evidence)

- **expansion: improved.** One measured nested-container class admitted as Core for its bounded scope, with its knowledge entry citing S301/S302, three capability rows added and verified (`## Capabilities`), census 205→208.
- **quality: improved.** C2 closes the declared 13 classes by behaviour-bearing cases (spot-read confirmed); QUALITY 144–147 and the round-83 quote-count correction appended without rewriting history.
- **discernment: improved.** Non-author spot-check agrees with the gate on 2 admits and 1 reject (table §4). Reason-level defects routed, not hidden.

## 8. Admission

Every declared claim verifies on its finite predicate at the measured revision, and no owned axis is harmed. **Admitted: true.** Whole-round or broader interpretations are not asserted by this check (consistent with the lane's own CriticClaims limit).

## 9. Routed defects for the lane's next round

- **R1 (S302 pointer).** Commit a snapshot of `FirmwarePublication.js` (or cite a reproducible `npm pack rea-agents@6.5.0` command with the digest) under `.ufo/waves/round-84/l1/sources/`, as S301 has. The npx cache path is not durable evidence.
- **R2 (S303 reason).** Correct "five scopes" to the seven prior rows (S079, S080, S083, S090, S092, S119, S123) by an appended correction, not an in-place rewrite.
- **R3 (M84-5 pointer).** Correct `l1/waves/round-84/…` to `.ufo/waves/round-84/w1/SentinelScope/esc-receipt.json` (and the `-abs` variant) by an appended correction.
- **R4 (M84-4 pointer).** Add a resolvable pointer (receipt or diff commit) for the removed `met = all(arms)` field.
- **R5 (planner seat).** Either dispatch the planner seat or keep the stated deviation in the wave record each round.
- **R6 (C2 semantics, carried).** Make the kill binding semantic as the lane's own `planned (a)` says; the name-level kill is a known gap.
- **R7 (C1 and C3 limits, carried).** Predicate-field binding for C1; C3 fixture-pin enforcement against a frozen constant, A3 exact root match, A9 `sasquatch` pin.

## 10. SHONEN

The four boxes remain `[~]` in the report. A non-author can check box 2 (the end-to-end domain task) from committed artifacts (LOG `round84` entry, C3 receipts re-read here). Promotion is operator-owned; no `[x]` is written by this closure.
