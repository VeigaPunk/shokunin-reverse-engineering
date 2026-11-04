# Round 85 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. This is closure evidence, not a lane-authored correction and not a promotion.

- Lane HEAD before the round: `b3084c8c2036db966ce4750b4039bddaa84cc760`.
- Declaration: `91eeb72f6a7b13dc96e826117956f90ed89ae3f3`.
- Measured instrument revision: `5ed965638a5d053d13ba9a1a756b704be2cf994c`.
- Record / container revision: `01f2d5193421d9769097ddcd9483046632f3b70e`.
- Reviewed lane tip (after): `b9d45602a13bec61832456ec791afa939535530a`.
- Report: fleet `.ufo/reports/round-85/kaidoku.md`, committed as `c8653681faa3cb9967c6af88a914851fc484576a`.

## 1. Disposition and method

**Status: ok. Admitted: false. Verdict: rejected-honest-stop.** R85-C1 misses its frozen predicate;
R85-C2 verifies on its declared finite, name-bound measure. No axis is harmed. No capability is added.

Method: the integrator recounted committed JSON results, table rows, anchor occurrences, case-name
presence, source rows, instrument digests and coverage stems from git blobs at the cited revisions,
reopened the sampled external sources over the network, and spot-read the lane's own attack reports.
Lane-owned gates and selftests were **not** executed: every gate/selftest statement below is
**committed-evidence verification** (PROTOCOL §Gate standard, *Closure consequence*), not a claim of
re-execution. Nothing in this file rewrites a lane-authored byte.

## 2. Step-1 conformance

| check | command / evidence | observed result |
|---|---|---|
| Report landed by the lane identity | `git log --format='%an <%ae> %H %s' -- .ufo/reports/round-85/kaidoku.md` (fleet) | `kaidoku-shokunin <kaidoku@shokunin.local> c8653681faa3cb9967c6af88a914851fc484576a round-85: kaidoku report` |
| Report is substantive, not a marker | report body | Two falsifiable claims, six cited lane commits, receipts, Sources & frontier, trend verdicts, `## SHONEN` with four `[~]` lines for the four `SHONEN.md` boxes (`grep -c '^## SHONEN'` prints 1) |
| Cited commit existence and ancestry | `git cat-file -e <hash>^{commit}` and `git merge-base --is-ancestor <hash> refs/heads/main` for all six hashes | All six exist and are ancestors of `refs/heads/main`: `91eeb72f…`, `c7e2e8e1…`, `c1c81c7d…`, `5ed96563…`, `01f2d519…`, `b9d45602…` |
| Lane pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain` | `branch=main local=b9d45602a13bec61832456ec791afa939535530a remote=b9d45602a13bec61832456ec791afa939535530a ahead=0 behind=0 head=detached tracked=0 untracked=3`; `git ls-remote origin refs/heads/main` prints the same tip. The three untracked entries are the two reported orchestrator handoff markers (`.ufo/waves/round-85/r85-w1.ready`, `…ready.dispatched`) and this file before its own commit — no lane round work left uncommitted |
| Report lands last | `git show -s --format='%aI %cI'` on the lane tip and the report commit | Lane tip `b9d45602…` authored/committed `2026-11-04T17:54:22-03:00`; report commit authored `17:53:20`, committed `17:55:28-03:00`. Report commit postdates the lane tip |
| Durable dispatched prompt | fleet `git log -1 -- .ufo/prompts/kaidoku-round-85.md` | `74b9b44f382fec646916163256b807ba32c70ee7`, lane identity, `2026-11-04T17:25:55-03:00`, on `origin/main` |
| Template fidelity | `diff` of `templates/round-prompt.md:1-140` against the prompt's sections 1–5 | Only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions differ (42 diff lines, all substitutions). Round-level items (mission/axes binding, 1–3 distinct-axis claims with a lowest-axis claim, batched L2 floor, commit-then-push, push scope, L0) and all five child-lane items (report path, commit-before-report, `SHONEN` heading, hash-citation rule, write scope) are present verbatim; the hyaku addendum is section 6 |
| Wave shape and roles | committed `.ufo/waves/round-85/w1/` tree | 12 seats, 12 `DONE` files, registry `swarm-registry.json`; attack seats 4/12 (ReviewerC1, ReviewerC2, CriticClaims, MutationRemeasure = 33 % ≥ 25 %), connector 1 (≤ 2), L2 floor ≥ 8 met in one wave. Planner held by the L1 and disclosed as deviation, not counted as a seat |
| Dispatch/completion digest | `.ufo/watchdog.log` (mutable; digest copied) | `2026-11-04T17:26:17-03:00 launch kaidoku round=85 pgid=3329039 driver=hyaku-inline attempt=1` / `2026-11-04T17:55:52-03:00 complete kaidoku round=85; hyaku-inline attempt=1`; no `lane-dead-no-report` line for this lane-round |

```text
2026-11-04T17:26:17-03:00 launch kaidoku round=85 pgid=3329039 driver=hyaku-inline attempt=1
2026-11-04T17:55:52-03:00 complete kaidoku round=85; hyaku-inline attempt=1
```

Conformance defects and remaining duties are routed in §8; none turns this real report into a
failed marker.

## 3. Claims — independent rechecks and committed gate evidence

### R85-C1 — calibration: unprovable (frozen target missed)

Reopened `plans/round-85-claims.md` (C1 predicate and kill rule), `.ufo/waves/round-85/claims.json`
`.claims[0].predicate`, `.ufo/waves/round-85/w1-briefs/ExecPredBind.md`, and the committed counter
`tools/round-85/predicate-bind.py:20-23,76`. The plan's frozen sentence lists the negation tokens
`not, no, never, without, neither, nor, cannot, none`; the container's pinned predicate repeats the
same eight-token list; the counter's `NEGATION_RE` is
`\b(?:not|no|never|without|neither|nor|cannot)\b` with a comment excluding `none`.

Read-only receipt extraction over committed blobs at the reviewed tip:

```sh
git show b9d45602a13bec61832456ec791afa939535530a:.ufo/waves/round-85/c1/literal-none-predicate-bind.json |
  jq '{rev,refused_expected,accepted_expected,control_fired,mismatches,met}'
```

| retained receipt | revision measured | refused | accepted positive | control fired | met |
|---|---|---:|---:|---|---|
| `pre/c1/base-freeze-precheck.json` (unchanged r84 gate) | `91eeb72f…` | 0/2 | 1/1 | true | false |
| `c1/literal-none-predicate-bind.json` (frozen list, incl. `none`) | `5ed96563…` | 2/2 | 0/1 | true | false |
| `c1/variant-predicate-bind.json` (list without `none`) | `5ed96563…` | 2/2 | 1/1 | true | true |

The literal-list receipt flags F1 with `PB_NO_PREDICATE_PATH:R85-F1`, F2 with
`PB_PREDICATE_NEGATED:R85-F2`, and the required CLEAN round-84 control with
`PB_PREDICATE_NEGATED:R84-C1` and `PB_PREDICATE_NEGATED:R84-C2`; its `mismatches` is
`[".ufo/waves/round-84/claims.json:FLAGGED"]`.

**The frozen target is not merely missed, it is unsatisfiable as frozen.** The round-84 positive
control's predicates read "… with mismatches none …" and "… survivors none, inconclusive none,
pristine_failed none …" (`git show b9d45602:.ufo/waves/round-84/claims.json | jq -r '.claims[].predicate'`),
so any negation list containing `none` flags the very container the same predicate requires to be
CLEAN. The lane's `missed` recording is therefore correct and conservative: the variant that meets
the target is a different rule, and a rule changed after the seats scored is not the claim's rule.
The variant's green selftest (`w1/ExecPredBind/selftest.json`: 21 cases, `failures []`, including
`none-token-is-not-negation`) validates the variant, never the frozen claim.

Gate-standard defect: `predicate-bind.py` has no registry row — `git show b9d45602:SKILL.md | grep -c
'predicate-bind'` prints 0 (R85-2). **No calibration improvement is admitted.**

### R85-C2 — depth: improved (finite declared-case binding)

Independent committed-byte measurements (Python over `git show` blobs; no lane scorer imported or run):

- `mutants.json` sha256 is `ef031dbe3525ff8454b1b120ed18f88a8918c981c7a4726ab626430e72e1ec41` at the
  declaration, measured and reviewed tip; `.mutants` has **21** rows; `.excluded` names the three
  verdict-neutral rows the report declares dropped.
- For every row, `target_blob.count(row.find) == row.anchor_occurrences` at `91eeb72f`, `5ed96563`
  and `b9d45602`: **no mismatches** (anchors unique at all three revisions).
- Declared case names present in their final target: **21/21**; **17** are new, and the four that
  pre-existed are exactly `sourced-row-rejected-status`, `late-single-header`, `duplicate`,
  `genuine-synthetic-passes` — i.e. the re-registered case plus the three BASE kills.
- Container pins: `claims.json.instruments` (3 digests at `measured_revision`),
  `claims.json.frozen_instruments` (mutation-closure at `base`) and `target_instruments` (3 digests)
  all equal their git blobs; all six pinned tool paths are byte-identical from `5ed96563` to the tip.
- `claims.json` does **not** exist at `5ed96563` (`git cat-file -e` fails: "exists on disk, but not in
  that revision"). The container and the final receipts land at `01f2d519`. The result is therefore
  input-provenanced in two revisions, which the report states; it must not be represented as a single
  revision's inputs.

```sh
git show b9d45602a13bec61832456ec791afa939535530a:.ufo/waves/round-85/c2/after-21row.json |
  jq '{rev,killed,rows:(.results|length),survivors:(.survivors|length),inconclusive:(.inconclusive|length),pristine_failed,ok,table_identity}'
```

| committed receipt | revision measured | killed / rows | survivors | inconclusive | pristine failed | table pin | ok |
|---|---|---:|---:|---:|---|---|---|
| `pre/c2/base-mutation-closure.json` | `91eeb72f…` | 3/21 | 18 | 0 | `[]` | `null` (no container yet) | false |
| `c2/after-21row.json` | `5ed96563…` | 21/21 | 0 | 0 | `[]` | `matches true` | true |
| `pre/c2/base-frozen13-regression.json` | `91eeb72f…` | 13/13 | 0 | 0 | `[]` | `matches true` | true |
| `c2/after-frozen13-regression.json` | `5ed96563…` | 13/13 | 0 | 0 | `[]` | `matches true` | true |

Independent recount of `results[].status` reproduces 3 killed / 18 survived → 21 killed. For every
killed row in both table receipts `declared_case_present` is true and the declared case occurs in
`failures`: **zero bad bindings**. The frozen r84 table digest the regression receipt pins
(`dbb6d4c9…`) equals the committed `.ufo/waves/round-84/mutants.json`.

These are integrity checks of retained observations, not independent executions of the mutants. What
makes the kill substantive rather than name-level is the counter's scoring site
(`tools/round-84/mutation-closure.py:196-211`): the mutated tool is written to a scratch copy, its own
`--selftest` is run, and a row is `killed` only when the declared case actually fails in that run with
pristine green; an absent declared case is a survivor (QUALITY 138). The residual gap is that a
"case" could itself be a text tripwire — a reviewed property, not one the counter enforces.

Selftest evidence (committed): `c2/after-21row.json.targets` records printed-command **36 cases /
exit 0 / `failures []`**, conjunction-gate **22 / 0 / `[]`**, source-bind **exit 0 / `[]`** with **10**
`case_names` (its selftest prints no case counter). The unchanged frozen scorer's own tally is **10**
selftest checks (`.ufo/waves/round-84/w1/ScoutLoci.md:296-308`, `SELFTEST cases=10 failures=0`) with
the `absent-case-survives` fixture asserting the stable reason
`declared-case-absent-from-selftest`; its registry row is `SKILL.md:1928` (verdict exits 0/1/2, so it
is treated as a gate).

Harm spot-read: `git diff b3084c8c b9d45602 -- tools/round-84` is empty. The three targets change
additively — `git diff --numstat` gives printed-command 235/2, source-bind 30/1, conjunction-gate
17/0 — and the three deleted lines are one re-registration (`sourced-row-rejected-status` moved to
`r85a_sourced_row_rejected_status`, `printed-command.py:870-880`, which runs both the original queued
arm and a new rejected-status arm) and one loop header (`fixtures = FIXTURES + (…)` in source-bind,
FIXTURES tuples untouched). Spot-read `r85b_pipe_metachar_refused` and
`r85b_unbound_plan_variable_refused` (`printed-command.py:1002-1018`): both drive production
`static_defects()` and assert a typed refusal — semantic for the pinned token, single-token in scope.
This supports, but does not convert into universal semantic certification, the lane review's
**19 SOUND / 2 WEAK / 0 FABRICATED** verdict (`w1/ReviewerC2/attack.md:35-83`), whose rows 10 (`|`
only) and 12 (`PLAN` only) are the two family gaps.

## 4. Coverage and per-axis verdicts

`git diff b3084c8c b9d45602 -- SCORECARD.md` rewrites the coverage evidence text (score stays
9.72 → 10.0) and appends the round-85 record; no other axis row changes. An independent stem recount
over `git ls-tree -r --name-only <rev> -- corpus/knowledge` (`.md` stems; `.gitkeep` excluded) against
the backticked tokens of the committed `corpus/README.md` `## Coverage map` section gives
**167/167 mapped, `missing []`, `dangling []` at `b3084c8c` and `5ed96563` → 168/168 at `01f2d519`
and `b9d45602`**. That is map completeness at a larger denominator, not new domain ground.

| axis | verdict | basis |
|---|---|---|
| coverage | unchanged | Map stays complete (168/168, no missing, no dangling) and no new domain class or province promotion is claimed. |
| depth | improved | C2: 3/21 → 21/21 by declared case, frozen 13/13 preserved, anchors and pins re-derived from blobs; case bodies reviewed, residual family gaps named. |
| calibration | unprovable | C1's frozen predicate cannot be satisfied (its own positive control contains `none`) and the variant that meets it is not the frozen rule; no existing score is lowered or inflated. |
| freshness | unchanged | No freshness claim, no axis row change; the new knowledge entry carries `recheck: 180d`. |
| operability | unchanged | Green apparatus selftests add no separately claimed repertoire capability. |
| adjacency | unchanged | No province cutover or sibling-domain absorption (`PROVINCE.md` untouched). |

No axis is judged harmed. These exact verdicts are used in the closure entry.

## 5. Sources census and independently reopened sample

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

Observed terminal `kaidoku ok …/corpus/SOURCES.md`, **exit 0**, **27** `W04` duplicate-URL warnings.
Frozen manual census over committed blobs: rows **208 → 209**, malformed rows **0 → 0**, duplicate
ids **none**, tier `A=190 B=10 C=8 → A=190 B=11 C=8`, status `mined=186 rejected=22 →
mined=187 rejected=22` — the one-row delta the report claims, on the single new tier-B/mined row.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S304 Papadakis et al., *Mutation Testing Advances*, Adv. Computers 112 (2019) | admit (mined, tier B, scope `mutation-testing survey`) | `https://web.archive.org/web/20190429011957/http://orbilu.uni.lu/bitstream/10993/31612/1/survey.pdf` re-fetched 2026-11-04: HTTP 200, 1 129 278 B, sha256 `63b7bfca877cd4661cb24e93fbfe1757a2740b39fb65ee3a79eb17e36215f023`, `pdftotext -f 6 -l 6` | agree | The quoted definition is verbatim on PDF p. 6, the section anchor resolves, and the quote is 24 words (≤ 25). A survey is right for behavioural kill semantics and is correctly not used as authority for case-name semantics. |
| S303 npm tarball as extraction-gap-taxonomy authority | reject, carried unchanged from round 84 (no fresh rejection this round) | `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` re-fetched 2026-11-04: HTTP 200, 5 634 033 B, `application/octet-stream`, gzip tar | agree on the decision; disagree on the stored reason text | A tarball with no file/line anchor is not the anchored taxonomy authority, and S302 is; the decision holds. The row's anchor cell still says "five scopes (S083/S090/S092/S119/S123)" while `git show 91eeb72f:corpus/SOURCES.md \| grep -c -F 'rea-agents-6.5.0.tgz'` prints **8** (S079, S080, S083, S090, S092, S119, S123, S303 — 7 prior). C-R2 corrects the count in the lesson; the registry row is still uncorrected (R85-3). |

S304 quote checked against the new registry row and PDF p. 6:

> When a test distinguishes the behaviour of a mutant (from that of the original program) we say that the mutant is 'killed' or 'detected'

`len(quote.split())` = **24**. The row's `used-by` is `corpus/knowledge/2026-11-04-r85-mutant-kill-binding.md`,
which exists and carries the provenance trio (`source:` S304 + URL + anchor, `verified-at:`,
`recheck: 180d`). The committed text snapshot
`.ufo/waves/round-85/w1/ScribeSource/source-snapshot.txt` hashes to
`3452916192a447db89545cf9cdb4c0c7bfbd7f162b67482fb7582691e6bd7bee`, matching the report.

Round-84 routed item R1 also re-verified: the committed
`.ufo/waves/round-85/l1/sources/FirmwarePublication.rea-agents-6.5.0.js` hashes to
`bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029`, byte-equal to the installed
6.5.0 copy at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/firmware/FirmwarePublication.js`
(the second npx tree, `a1722018f28f9df2`, holds a different build, `d811922c…`, and is not the cited
one). R2, R3 and R4 verify as appended corrections in `corpus/lessons/round-85.md` §Corrections; the
`met = all(arms)` pickaxe still returns no commit under `tools/`.

## 6. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | One tier-B source (S304) and one knowledge entry, both on the lane's own mutation apparatus; the coverage map row marks it bounded apparatus knowledge with no artifact class or frontier promotion, and no capability row entered. Coverage stem count rises 167→168 but on already-mapped ground. |
| quality | improved | Three routed round-84 defects are discharged by appended corrections (C-R2 count 8 rows / 7 prior, C-R3 pointer resolves, C-R4 bounded receipt plus an explicit "no removal commit exists" inference), S302 gains a byte-equal committed snapshot, and two lesson-backed criteria land (QUALITY 148 cites M85-2 and the MISMATCH sweep, 149 cites M85-1 and the red-before/green-after pointer sweep). No admitted entry fails its re-check; the C1 fix and the S303 registry correction remain open debt. |
| discernment | improved | This non-author sample agrees with the gate on the one admit (S304) and on the carried reject (S303). The one disagreement found is reason-level — the stored "five scopes" count — and it is already learned, not denied: M85-1, C-R2 and QUALITY 149. The round's own report left discernment `unchanged` because this check was pending; the check now exists and supersedes that pending assessment only. It does not claim a fresh rejection occurred in round 85. |

## 7. Admission and SHONEN

C1 remains unprovable on its frozen target, so **admitted=false**, **rejected-honest-stop**, even
though C2 improves and no axis is harmed. The report is real, committed and pushed, so **status=ok**,
not a failed marker.

SHONEN stays author-asserted: four `[~]` lines, no `[x]`. This round's apparatus work alone does not
newly certify the end-to-end domain and promotion boxes, and a non-author may not write `[x]` on the
lane's behalf here. No `[x]`, promotion, mint or lane-authored file is changed by this closure;
promotion remains operator-owned. The four boxes now look mechanically checkable by a non-author
(box 1 against `SKILL.md` decision tables and their citations, box 3 against the committed plan and
wave briefs, box 4 against `PROVINCE.md` and the connector report); whether to run that review is an
operator decision, not a closure act.

## 8. Routed defects and carried duties for kaidoku's next steered round

- **R85-1 — frozen C1 agreement (M85-2).** Keep the missed result; do not retro-fit the variant. The
  next declaration must make the token list agree with the positive control it is scored against
  (a frozen list containing `none` flags "mismatches none"), and must land the plan↔brief↔counter
  agreement check as a declared, pre-data sweep that is shown able to refuse a mismatch.
- **R85-2 — missing new gate registration.** `SKILL.md` has no `predicate-bind.py` row. Register its
  entry command, gate classification, exit map, self-invocation spelling, pinned values, write scope
  and owner under PROTOCOL §Gate standard; the 21 green variant fixtures do not register it and do
  not validate the literal frozen list.
- **R85-3 — registry-specific S303 correction.** C-R2 satisfies the earlier request for an appended
  lesson correction, but `corpus/SOURCES.md` still carries "five scopes" in S303's anchor cell.
  SOURCES rule 2 requires a new row whose `teaches` opens `supersedes S303 —`, preserving the old
  row; do not rewrite the anchor in place.
- **R85-4 — C2 limits (carried r84 R6).** Preserve the declared-case-name versus case-semantics
  distinction and the absence of a removed/weakened-case detector; the tripwire and removed-case
  controls stay counterexamples to broader certification. Rows 10 and 12 need same-family siblings
  (`>`, `<`, `&`; widened allowlist names) under their own frozen predicates, not stronger
  retrospective wording.
- **R85-5 — frozen scorer description still inconsistent.** At the reviewed tip
  `tools/round-84/mutation-closure.py:8` still calls an absent declared case "inconclusive", while
  the code (`:200-205`), the selftest fixture and the `SKILL.md:1928` registry row all say survivor.
  Correct in a new disclosed revision; never rewrite old claims or receipts.
- **R85-6 — coverage receipt pointer.** The refreshed SCORECARD coverage row says the receipt carries
  its own `rev`, but no round-85 coverage receipt path is named or committed (`.ufo/waves/round-85/l1/`
  holds only `sources/` and `sweep/`). The independent stem recount corroborates 168/168, so this is
  evidence-pointer debt, not a failed coverage claim: name a persisted receipt in the next refresh
  and never backdate evidence.
- **Carried r84 R5 (planner seat) — open.** The L1-held planner deviation is disclosed, not resolved;
  dispatch the seat or keep recording the deviation.
- **Carried r84 R7 — partially open.** C1 predicate-field work landed as a tool but its claim missed;
  C3 fixture-pin enforcement, A3 exact-root match and A9 `sasquatch` pin remain deferred as the report
  states.
- **Observation, not a defect.** The frozen C1 predicate was unsatisfiable against its own positive
  control, so the miss is a planning defect rather than a counter weakness; a future claim on this
  surface should score the positive control and the negation list for compatibility before the wave.

The two untracked ready markers are orchestrator-owned operational leftovers, not files for this
verifier to sweep. All routed defects above are status-neutral: the rejection is caused by C1's
frozen target miss, not by conformance paperwork.

Tool installs/updates during closure: none.
