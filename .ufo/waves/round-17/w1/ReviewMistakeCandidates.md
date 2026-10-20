# ReviewMistakeCandidates — r17 lesson `## Mistakes`, author-side advisory

**Axes:** calibration (counting and class hygiene), depth (whether the r16 record supports the row).
**Baseline:** `b563c799d97774aae4351276fe43cb897311e349` (lane HEAD). Read-only; no sibling tool run; no REA/Ghidra/carrier execution; no installs. Every count below is my own reimplementation over committed Git objects, not a sibling receipt.

## Verdict

The six rows in `corpus/lessons/round-16.md:50-59` are class-correct for rows 1–4 and evidence-verified; rows 5–6 have fixes that **cannot be shown to fail**, which violates `CORPUS.md:179-182` (“A fix is shown able to fail before it counts”). For the r17 section, add four rows (provenance, invocation, provider, attribution/landing) and correct two counted fixes whose baseline universes under-count survivors:

- `temporal-sweep.py` as specified (`contract.md:91-93`) finds **2** sites at baseline but the lane has **4** in-lane statements; two survive any sanctioned invocation.
- `invocation-audit.py` baseline `unlabelled_variant` count is **2 (certain) to 3 (strict path equality)**, not the single citation-drift row the r16 route names.

## A. The r16 `Mistakes` table, row by row

| r16 row | Class / pointer | Verdict |
|---|---|---|
| `round-16.md:54` | reference-drift/invocation; `knowledge:3` vs r15 argv | **stands.** `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:3` is the relative no-`-I` recheck; exercised argv is `python3 -I /abs/...` at `.ufo/waves/round-15/verification.json` commands 2–3. Correction at the same file `:76-84` names the exact argv; `SKILL.md:487` matches an exercised argv. |
| `round-16.md:55` | reference-drift/registry; quote-fidelity pinned-values cell | **stands.** `SKILL.md:450` contains `.ufo/waves/round-15/boundary-fixtures/expected.json`; present at S and A; original `round-14/fixtures/expected.json` untouched. |
| `round-16.md:56` | number-drift/provenance; `no-harm-controls.json` lacks producer | **stands.** Recursive scan of `.ufo/waves/round-15/no-harm-controls.json` finds no `argv`/`command` key; its top-level keys are the two revisions plus four booleans (`unchanged_inputs`, `row16_unchanged`, `append_only`, `pins_match`). |
| `round-16.md:57` | stale-premise/attribution; SHONEN box 3 “this round” | **stands.** `git show 6235498:SHONEN.md` box 3 says “this round executed…”; `SHONEN.md:10` now says “historical 2026-10-15 operator-steered round 1”; four `[~]` retained. |
| `round-16.md:58` | vacuous/marker sufficiency; `w1/AttackRedBefore.md` | **class/evidence stand; fix is a label, not a check.** `AttackRedBefore.md:9` shows the red predicate `bool(co) and 'argv' in co` accepts a comment-only file; the r16 “fix” is “labelled marker/presence evidence only” and cannot fail. |
| `round-16.md:59` | provider; 14 scout/8 connector 402 credit failures | **class stands; fix cannot fail; evidence pointer imprecise.** “Dead seats stay dead” is an intention. “Immediate” has no timestamped artifact (`wave1-outcomes.json` records only `agent_id`, `status`, `error`), and the spotcheck itself declines the timing claim (`round-16-verifier-spotcheck.md:186`). “Other failure results retained separately” is wrong in the literal sense: the 6 capacity failures are in the same `failure_records` array (`wave1-outcomes.json:121-146`). |

Format defect: the `captured-by` column should name a `QUALITY.md` criterion or protocol rule, or `none` (`CORPUS.md:171-178`). Rows 5–6 say “Current author-side critic” / “Host task execution, not domain gate”, which are causes, not criteria; use `none` and move the detail into evidence.

## B. Candidate rows for `corpus/lessons/round-17.md ## Mistakes`

Classes use the `mistakes.md` §5 vocabulary (`CORPUS.md:174-176`). “Evidence” is a path:line; “captured-by” is the rule that should have caught it or `none`.

| # | class | evidence pointer | captured-by | fix (red-before in §C) |
|---|---|---|---|---|
| 1 | vacuous / number-drift | `.ufo/waves/round-16/verification.json:419` `pins_unchanged_during_run:true`; one 20-entry map at `:397-418`; one `executed_at_utc` at `:4`; statements at `corpus/lessons/round-16.md:154`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`, `LOG.md:2012`, out-of-lane `.ufo/reports/round-16/kaidoku.md:60`; routed `corpus/lessons/round-16-verifier-spotcheck.md:183` | `QUALITY #18` (“structural/no-harm tallies retain the producer and immutable inputs, not only unexplained booleans”) existed at S but was not applied to the same round’s `verification.json`; effective capture = r16 non-author spotcheck | Pre/post `pins.py` snapshots with timestamps + `compare`; named append-only correction at every statement site; sweep **derives** sites by search, not the 5-file list. I verified the 20 hashes equal committed S and A blobs 20/20 and that none changed S→A, so the honest wording is “map matches committed blobs; temporal stability not evidenced,” not “unchanged during.” |
| 2 | survivor / reference-drift | `SKILL.md:448` (citation-drift, relative, no `-I`); `SKILL.md:449` (custody-pair, **no exercised argv under the contract's receipt definition**); `SKILL.md:450` (quote-fidelity, relative path vs absolute exercised argv `.ufo/waves/round-14/verification.json`); routed `round-16-verifier-spotcheck.md:184` | `QUALITY #18` (`corpus/QUALITY.md:28`) already required “match the exercised isolation flags and paths or explicitly name an unexercised variant”; the class recurred on 2–3 rows | `invocation-audit.py` at `b563c79` reports 2–3 unlabelled rows; after alignment/labels 0. Re-exercise citation-drift with the isolated absolute argv **and** label or align custody-pair and quote-fidelity; otherwise `M→0` is unreachable (`claims.json:12` names only citation-drift). |
| 3 | provider | `.ufo/waves/round-16/wave1-outcomes.json:7-146`: 22 × 402 billing (`:9-117`) + 6 × capacity (`:121-146`); roles from `wave1-registration.json`: 14 scout/8 connector/6 critic; `round-16.md:59` “immediate”; `round-16-verifier-spotcheck.md:186` declines the timing claim | `none` (host execution; no QUALITY/protocol rule) | Drop “immediate” or record per-seat first-observed timestamps; add a committed identity check: `failed(w1) ∩ members(w2) = ∅` and `members(w1) ∩ members(w2) = ∅`. I verified the current facts (64/64, 32/32, intersection ∅, 28 failed all in w1, 0 in w2), so the check passes today and can fail on injection (§C). |
| 4 | number-drift | `corpus/lessons/round-16.md:159` “22 credit, 6 capacity”; the only committed producer (`verification.json` label `source-contract-wave-counts`) emits `waves[].registered` and roles but **no failure counts**; `:173-174` claims every number carries a command, then carves out dead-seat counts | CORPUS count-command rule (`CORPUS.md:171-178`), exception disclosed rather than produced | A count command over `wave1-outcomes.json` emitting `{failed, completed, classes:{billing, capacity}}`; red case in §C. Low severity because the exception is disclosed, but the r17 lesson should not repeat it. |
| 5 | attribution | `.ufo/waves/round-16/wave2-outcomes.json:2` “Follow-ups retained the same seat identities”; no follow-up ids anywhere in the file; the ambiguity produced a review contradiction adjudicated at `round-16-verifier-spotcheck.md:58` | `none` | Enumerate the follow-up ids (or delete the clause); a validator requires every claimed identity to be a dispatch-registry member. Red case: add `KaidokuR16.Ghost` → exit 1. |
| 6 | landing | `.ufo/waves/round-16/wave1-outcomes.json:2` “agent:// failed-task artifacts were empty; tool issue reported”; the 28-failure record is a session transcription, not a retained provider error text | `none` | Retain the raw task-result notification per failure (file + sha256) and validate one per record; red-before is 0/28 retained → exit 1 (§C). This is what makes the provider row independently checkable. |
| 7 | scope | `round-16-verifier-spotcheck.md:183` names “report, lesson, LOG and scorecard”; measured: fleet report `.ufo/reports/round-16/kaidoku.md:60` yes, `LOG.md:2012` yes via “across execution”, `SCORECARD.md` **0** hits, and `corpus/knowledge/...:95` is **unnamed** | `none` | Produce a per-surface `file:line` table by search; red case: a named surface with 0 hits, or an unnamed in-lane file with ≥1 hit, exits 1. This is the root cause of candidate 1’s under-count. |

Row 7 is the reason the r17 sweep inherits a wrong universe: the route list was copied from prose. Prefer “the fix derives its site list” over “the fix is given a site list.”

## C. Red-before states (each fix can fail)

All are read-only or temp-fixture checks; none executes a carrier. The r17 tools are contract deliverables (`contract.md:12-20`, `:80-97`); the commands below are the contract spelling.

1. **pins.py** — selftest red case mandated at `contract.md:18-19`: snapshot → mutate one temp file → snapshot → `compare` exits 1 naming that path. **Sweep:** at `2fc1d6f` the contract scope reports `unqualified=2` (`round-16.md:154`, `verification.json:419`); with the two missing sites it is 4. Delete one correction line from `round-17.md` → `unqualified=1`. This is the “same command, fix as only delta” shape `CORPUS.md:179-182` requires.
2. **invocation-audit** — at `b563c79`: `unlabelled=2` under token equality (`citation-drift`, `custody-pair`), `3` if relative paths are not absolutized (`+quote-fidelity`); the other four rows match an exercised argv. Revert `SKILL.md:448` to its advertised text → count returns ≥1. **Contract gap:** “normalized command” (`contract.md:83-88`) does not state whether relative↔absolute paths are equal; state it, or two honest implementations report different `M`.
3. **provider identity check** — current committed state passes: `members(w1)=64`, `members(w2)=32`, intersection ∅, `failed(w1)∩members(w2)=∅`. Red case: copy `wave2-dispatch.json` to a temp dir and rename one member to `KaidokuR16.BaseName` (a failed w1 id) → exit 1. This converts “Dead seats stay dead” into a check the artifacts can fail.
4. **count command** — on a temp copy of `wave1-outcomes.json` with one `402` error string changed to `capacity`, the command must report 21/7 against expected 22/6 → exit 1. A count that cannot move is a marker.
5. **follow-up validator** — insert an id not present in any dispatch registry → exit 1; currently no ids exist, so the validator must report `unverifiable` rather than pass.
6. **failure-retention validator** — require one retained error text per `failure_records` entry with matching sha256; at baseline 0/28 → exit 1. This is the red-before for “transcribed only.”
7. **surface-table check** — `grep -c` the pattern on each named surface: scorecard returns 0 → finding; `grep` the lane tree: knowledge file returns 1 but is unnamed → finding.

## D. Findings against the two counted fixes (details)

**N (temporal sites).** Contract scope (`contract.md:91-93`) yields exactly 2 sites. The real in-lane set is 4:

- `corpus/lessons/round-16.md:154` — “remained unchanged during execution” (in scope).
- `.ufo/waves/round-16/verification.json:419` — `pins_unchanged_during_run` (in scope).
- `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` — “were unchanged during the run” (**file not in scope**).
- `LOG.md:2012` — “remain unchanged across execution” (**regex does not match; no `--extra` invocation can find it**).

Out-of-lane: `.ufo/reports/round-16/kaidoku.md:60` (“stayed unchanged during execution”). The spotcheck quotation at `round-16-verifier-spotcheck.md:183` is meta and should not be counted. `SCORECARD.md` and `SKILL.md` have **0** hits, so including them in the scope is harmless but shows the list was not searched. Consequence: `N→0` is achievable with two in-lane statements live. Fix: `--extra corpus/knowledge/...` **and** widen the pattern to `(?i)(remain(ed|s)?|stay(ed|s)?|were|was) unchanged (during|across|throughout)`; assert the 4-site set against the file:line table in the lesson. Name the out-of-lane fleet report as uncorrectable-in-lane rather than silently dropping it.

**M (registry variants).** My reimplementation of `contract.md:80-88` over the 7 rows at `SKILL.md:447-450,487,506-507` and the 12 contract-defined receipts gives:

- `interactive-r1-recovery` → exercised_match (`.ufo/rounds/interactive-r1/gate-results.json`).
- `citation-drift` → unlabelled (advertised relative/no-`-I`; exercised `python3 -I /abs/...` at `round-16/verification.json` label `citation-strict`).
- `custody-pair` → unlabelled with **no exercised argv at all** under the receipt definition; only a label or a new retained run can clear it.
- `quote-fidelity` → unlabelled under token equality (relative vs absolute); clears only if the audit absolutizes against the repo root, which the contract does not state.
- `go-snapshot-inventory`, `go-selection-preview`, `round16-structural-controls` → exercised_match.

So `M` is 2 or 3, not 1. `claims.json:12` only promises to re-exercise citation-drift; the metric `M→0` therefore needs custody-pair and quote-fidelity handled too, or the claim’s before/after will not close. This is a `survivor` of the same class, not a new class.

## E. Residual risk and gaps

- I did not run any sibling tool, REA, Ghidra, or a carrier; `M`/`N` are my reimplementations over Git objects and may differ from the delivered tools at the edges named above. The divergence is itself the finding: the contract must pin the normalization and the site universe.
- `pins.py` proves same-bytes-at-two-instants only; it cannot prove “no write occurred between them.” The lesson must keep that limit.
- `wave1-outcomes.json` failure records cannot be independently reconstructed (source is a transcription), so the 22/6 split is a derived count, not a measurement; candidate 4 and 6 are the repairs.
- `wave2-outcomes.json` “follow-ups” has no named ids; I did not infer any.
- No files outside this report were written; no tool was installed or updated.
