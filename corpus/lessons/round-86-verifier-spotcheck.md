# Round 86 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. This is closure evidence, not a lane-authored correction and not a promotion.
Nothing below rewrites a lane-authored byte.

- Lane HEAD before the round: `2cf0b7ff93c698809bed321f7338276a22d6beb9`.
- Declaration: `b205bb8b66ec7b61e028bccd92f64eade8942461`; container `ec9963eb9e5c1eedfada9a69f073c1639e7911f9`.
- Measured revision: `4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc`; record commit `63c30e9d37556bd14fc21ec172d079f676684a2d`.
- Reviewed lane tip (after): `697193400d45b4989acfec0b397ae12aa758affc`.
- Report: fleet `.ufo/reports/round-86/kaidoku.md`, committed as `fda6a6ec094e3efd576afa5cacc3031a7fa91ae9`.

## 1. Disposition and method

**Status: ok. Admitted: false. Verdict: rejected-honest-stop.** R86-C1 misses its frozen predicate
(agreed 2/3 against a 3/3 target) and R86-C2 verifies its declared measure (5/5) on an axis the lane
does not own. No owned axis is harmed. No capability row is added.

Method: the integrator recounted committed blobs at the cited revisions with `git show`, `grep -c`,
`grep -c -F`, `sha256sum` and `git cat-file`, compared them with the lane's receipts, re-opened the
sampled external source over the network, and spot-read the lane's attack evidence. Lane-owned gates
and selftests were **not** executed: every gate/selftest statement below is **committed-evidence
verification** (PROTOCOL §Gate standard, *Closure consequence*), never a claim of re-execution.

## 2. Step-1 conformance

| check | command / evidence | observed result |
|---|---|---|
| Report landed by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-86/kaidoku.md` (fleet) | `kaidoku-shokunin fda6a6ec094e3efd576afa5cacc3031a7fa91ae9` (`kaidoku-shokunin <kaidoku@shokunin.local>`) |
| Report is substantive, not a marker | report body | Two declared claims with falsifiable targets, six cited lane commits, receipts and sweeps, Sources & frontier with before/after census, three trend verdicts, `## SHONEN` with one line per box (`grep -c '^## SHONEN'` → 1; `grep -c '^\[[ x~]\]'` → 4, matching the four `SHONEN.md` boxes) |
| Cited commit existence and ancestry | `git cat-file -e <h>^{commit}`; `git merge-base --is-ancestor <h> refs/heads/main` for `2cf0b7ff`, `b205bb8b`, `ec9963eb`, `4cc03025`, `63c30e9d`, `697193400` | All six exist and are ancestors of `refs/heads/main` (ancestry tested against the branch ref, not `@{u}`) |
| Lane pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state kaidoku-shokunin`; `git -C kaidoku-shokunin status --porcelain` | `branch=main local=697193400d45b4989acfec0b397ae12aa758affc remote=697193400… ahead=0 behind=0 head=detached tracked=0 untracked=4`; the four untracked entries are the orchestrator handoff markers `.ufo/waves/round-85/r85-w1.ready(.dispatched)` and `.ufo/waves/round-86/r86-w1.ready(.dispatched)` — no lane round work left uncommitted |
| Report lands last | `git log -1 --format='%ci'` on lane tip and report commit | Lane tip `2026-11-04 18:40:04 -0300`; report commit `2026-11-04 18:41:15 -0300` — the report postdates the lane work |
| Template contract in the dispatched prompt | `diff` of `templates/round-prompt.md` against `.ufo/prompts/kaidoku-round-86.md` sections 1–5 | Only `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions differ; all round-level items (mission/axes binding, 1–3 distinct-axis claims with a lowest-axis claim, batched L2 floor, commit-then-push, push scope, L0 side channel) and all five child-lane items (report path, commit-before-report, `SHONEN` heading, hash citation, write scope) are present; the hyaku addendum is section 6 |
| Wave shape | `.ufo/waves/round-86/r86-w1-spec.json`, `r86-w1-dispatch.json` | 12 items in one wave: scout 1, executor 3, scribe 2, reviewer 2, critic 1, mutation-tester 1, sentinel 1, connector 1. Dispatch policy `minLanes 8 / waveMaxLanes 16`, `counts.spawn 12`. Attack seats 5/12 = 41.7 % (≥ 25 %), connector 1 (≤ 2), L2 floor ≥ 8 met. Planner held by the L1 and disclosed as a deviation |
| Dispatch/completion digest | `.ufo/watchdog.log` (mutable; digest copied) | `2026-11-04T18:09:26-03:00 launch kaidoku round=86 pgid=145113 driver=hyaku-inline attempt=1` / `2026-11-04T18:41:39-03:00 complete kaidoku round=86; hyaku-inline attempt=1`; no `lane-dead-no-report` line for this lane-round |

```text
2026-11-04T18:09:26-03:00 launch kaidoku round=86 pgid=145113 driver=hyaku-inline attempt=1
2026-11-04T18:41:39-03:00 complete kaidoku round=86; hyaku-inline attempt=1
```

Conformance defects found are routed in §6; none turns this real report into a marker and none changes
the status. No checkable work is missing, so `failed` does not apply.

## 3. Per-claim re-check

Counting commands were run by the integrator over committed bytes at the cited revisions; the lane's
own counters were read as receipts, not executed.

### R86-C1 — calibration (declared target 0/3 → 3/3; reported **missed**)

| atom | integrator command | observed | reported | agree |
|---|---|---|---|---|
| A1 `S303-supersede-count` | `git show 4cc03025:corpus/SOURCES.md \| grep -c -F 'registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz'` and the row ids | 8 rows carry the URL — `S079 S080 S083 S090 S092 S119 S123` plus `S303`; S305 (`:221`) states count 7 with exactly those seven ids and `supersedes S303`; S303 (`:219`) is byte-unchanged (`git diff 2cf0b7ff 4cc03025 -- corpus/SOURCES.md` shows only the S305 addition and the S255 row rewrite) | A1 agrees at `4cc03025`; mismatched at BASE ("no row whose teaches opens `supersedes S303`") | agree |
| A2 `docstring-status` | `git show 4cc03025:tools/round-84/mutation-closure.py \| sed -n '1,14p'`; `sha256sum` over both revisions; `git diff 2cf0b7ff 4cc03025 -- tools/round-84/mutation-closure.py` | line 8 reads "an absent declared case scores survived, never a pass"; BASE reads "…is inconclusive…"; blob sha256 `4d73c89e45fd1657dfc56d30f0ab4e15f08e84093d080f81a6c87668f3cff5ed` (BASE `e5cfd2ed…`); the diff is exactly one line, docstring only | A2 agrees; sha `4d73c89e…` | agree |
| A3 `receipt-pointer` | `git show 4cc03025:SCORECARD.md \| grep -c '^\| coverage \|'`; same at `2cf0b7ff` | 23 at both revisions | "expected exactly one `\| coverage \|` row, found 23" | agree |

Before → after therefore reads **agreed 0/3 → 2/3** exactly as reported; the third atom is unreachable
under its frozen rule without rewriting 22 history rows, and the lane did not fabricate a receipt or
rewrite the row's round. **Claim verdict: missed.** Axis `calibration`: **unchanged** (10.0, no score row moved).

### R86-C2 — operability (declared target 0/5 → 5/5; reported **met, not admitted**)

| atom | integrator check (committed evidence) | observed |
|---|---|---|
| G1 row present | `git show 4cc03025:SKILL.md` registry block | one row for `tools/round-85/predicate-bind.py` |
| G2 exit map | same row | three exits declared `0=…; 1=…; 2=…`; self-test cell "21 cases, exit 0 on 2026-11-04" |
| G3 self-invocation | receipt `.ufo/waves/round-86/l1/scores/c2-at-integration.json` | `observed_exit 0`, `last_line "SELFTEST cases=21 failures=0"` (lane evidence; not re-executed here) |
| G4 pinned blob | `git cat-file -t 4cc03025:.ufo/waves/round-85/claims.json` | `blob` |
| G5 owner round | same row | `kaidoku-r85`, tool round `85` |

Receipt `agreed 5`, `ok true`, `rev 4cc03025e6d4f6f1e00b5e402fcc0180e6e730bc`; BASE `pre/c2-at-base.json`
`agreed 0`. The reported 0/5 → 5/5 reproduces on committed evidence. The lane's own attack evidence
(`.ufo/waves/round-86/l1/sweep/g3-behavioural-red.txt`, `g3-foreign-command-accepted.json`) shows the
frozen G3 clause "on that tool path" is unenforced: a row whose self-test is `python3 -c "import sys; sys.exit(0)"`
scores 5/5. **Claim verdict: measured, not admitted** — operability is not an owned lane axis
(SCORECARD: "fleet axis, unowned proxy"), so no owned score can move. Axis `operability`: **unchanged**
(not owned; and the instrument's own false green forbids crediting it as a capability).

### No-harm re-checks

| surface | command | observed |
|---|---|---|
| Owned axis rows | `git diff 2cf0b7ff 697193400 -- SCORECARD.md` | 22 insertions, **0 deletions** — only the round-86 section is appended; coverage 10.0, depth 10.0, calibration 10.0, freshness 10.0 unchanged |
| Depth instrument | receipt `.ufo/waves/round-86/l1/scores/c2-mutation-closure-r85-table-at-integration.json` | `killed 21 / mutants 21`, `pristine_failed []`, `ok true`, `instrument.sha256 4d73c89e…` = the repaired blob — the docstring revision does not harm the round-85 depth measurement |
| Append-only files | `git diff --numstat 2cf0b7ff 697193400 -- LOG.md SCORECARD.md SKILL.md corpus/QUALITY.md corpus/SOURCES.md` | `LOG 14/0`, `SCORECARD 22/0`, `SKILL 3/0`, `QUALITY 4/0`, `SOURCES 2/1` (the single deletion is the S255 row rewrite) |
| Round criteria landed | `git show 697193400:corpus/QUALITY.md \| grep -c 'Row 150' / 'Row 151'` | 1 each — rows 150 (record cell re-derived at the revision it names) and 151 (a registered gate row is run by its declared command naming the registered tool), both citing the round-86 lesson |
| Census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 28 `W04` duplicate-URL warnings (pre-existing, including S303) then `kaidoku ok …/corpus/SOURCES.md`, **exit 0** |
| Registry rows | `git show 4cc03025:corpus/SOURCES.md \| grep -c '^\| S[0-9]'`; tier column histogram | 209 → 210 rows; A 190 → 191, B 11 → 11, C 8 → 8 — matches the report |

## 4. Discernment spot-check (LEARNING.md — checked from outside)

Sources were re-opened by the integrator, not read from the lesson.

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| S255 git-show documentation | **admit** by re-open (mined, tier A); used-by extended by `corpus/knowledge/2026-11-04-r86-record-agreement.md` | `https://git-scm.com/docs/git-show` fetched 2026-11-04: HTTP 200, 246736 bytes, sha256 `a3716a4d6c236082b0f6d08da64735765f376c1c32ba5ede93b70b013f52a9aa` | **agree** | The row's quote "For plain blobs, it shows the plain contents." (8 words ≤ 25) is present verbatim in the served DESCRIPTION; byte count and digest reproduce exactly; the row's `opened` cell stays 2026-11-01 and the 2026-11-04 re-open is recorded in the lesson Gate and the knowledge entry, which is the contract's shape |
| S305 correction row for S303's scope count | **reject** (a correction row adds no source) | no external document; the count is re-derived from `corpus/SOURCES.md` itself | **agree on the decision** | The count 7 with ids `S079/S080/S083/S090/S092/S119/S123` is exactly the number of rows other than S303 carrying the URL (8 total − S303); the row adds no duplicate-URL warning and no anchor. Disagree only on row conformance: a new row was written with no opened document and no located quote (§6 defect V86-2) |
| S303 npm tarball as authority | **stays rejected**, unchanged | the row itself, `corpus/SOURCES.md:219` at both revisions | **agree** | A packed tarball is not an anchored document and the URL is already in scope in five other scopes; the supersession does not flip a rejection, and the row's wrong "five scopes" cell is left byte-unchanged with the correction carried by S305 — the append-only rule applied correctly |
| Round verdict (C1 missed, C2 not admitted) | lane self-declared **not admitted** | `pre/c1-at-base.json`, `l1/scores/c1-at-integration.json`, and the integrator's own recounts above | **agree** | 0/3 → 2/3 with A3 unreachable is a miss, not a pass; refusing to relax the atom or fabricate a receipt is the honest disposition. C2's 5/5 is real but moves no owned score |

## 5. Axis verdicts and trends

| axis | verdict | evidence |
|---|---|---|
| coverage | **unchanged** | No owned score row changed (`SCORECARD.md` diff: 0 deletions); one coverage-map row added for an apparatus entry, no artifact class, no frontier promotion |
| depth | **unchanged** | Frozen 21-row depth table re-measured at `4cc03025`: 21/21 killed, pristine green (`c2-mutation-closure-r85-table-at-integration.json`) |
| calibration | **unchanged** | C1 missed its frozen target (agreed 2/3 vs 3/3); the card's calibration row is untouched |
| freshness | **unchanged** | No entry re-verified on a domain surface; S255 re-open is recorded in the lesson and the new entry, not as a freshness move |
| operability (declared axis, not owned) | **unchanged** | 5/5 measured at `4cc03025`, but the axis is "fleet axis, unowned proxy" and the instrument admits a foreign self-test command (false green), so no credit is taken |

| trend | verdict | evidence |
|---|---|---|
| expansion | **unchanged** | One bounded apparatus knowledge entry (`corpus/knowledge/2026-11-04-r86-record-agreement.md`, source S255) plus one correction row; no new artifact class, no frontier row advanced, no capability row. The lane's own verdict agrees |
| quality | **improved** | Two record cells that stated a wrong value now agree with the bytes they describe (docstring `inconclusive` → `survived`, sha `4d73c89e…`, diff one line; S303's scope count corrected by S305, count 7 re-derived by the integrator). No admitted entry is left false or stale, and the round-85 depth measurement still passes on the repaired blob |
| discernment | **improved** (lane self-assessed "unchanged, pending non-author closure"; that closure is this file) | The outside spot-check agrees with the gate on its sampled admit (S255) and reject (S305, S303 unchanged), each re-opened and reasoned above; the two mined mistakes M86-2 and M86-3 became grounded `QUALITY.md` criteria 151 and 150 citing `corpus/lessons/round-86.md`. The round also refused to admit a met claim on an unowned axis rather than score it |

Round: **not admitted** — C1 does not verify, so the admission clause ("every claim verifies") fails.
No axis is harmed and no trade is taken, so the honest verdict is `rejected-honest-stop`.

## 6. Routed defects for the next steered round

1. **V86-1 (claim axis).** R86-C2 was declared on `operability`, which the card marks "fleet axis,
   unowned proxy", so a met claim could move no owned score. The L0 question is filed
   (`.ufo/l0-questions.md`, `kaidoku | round-86`); until the operator rules, a registry-verification
   claim must name an owned axis or enter the capabilities table.
2. **V86-2 (frontier contract).** S305 is a new `corpus/SOURCES.md` row written with no opened
   document and no located ≤25-word quote; §2b item 1 admits a row only after its source is opened
   this round. Either open the URL or record lane-internal corrections outside the registry.
3. **V86-3 (evidence precision).** The report's Sources bullet says S255 "opened 2026-11-04" while the
   row's `opened` cell is 2026-11-01 and 2026-11-04 is a re-open. Say "re-opened".
4. **V86-4 (wave handoff).** `r86-w1-results.json` records `output: null` for all twelve seats
   (orchestrator kernel restart) and the wave has **no `DONE` markers** (round 85 had twelve); seat
   completion rests only on the eleven seat report files, and `ScribeSources/` is an empty directory.
   Restore per-seat outputs and completion markers.
5. **V86-5 (spawn discipline).** The L1 made one direct `task` call to message its own seats, which the
   inline spawn handoff forbids; it was cancelled with no output and wrote nothing. Disclosed in the
   report; keep the handoff.
6. **V86-6 (frozen atom, carried M86-3).** A3 required exactly one `| coverage |` row and the card has
   23 at both BASE and the measured revision. Re-declare against the card's own current-assessment
   pointer with a pre-freeze row sweep.
7. **V86-7 (instrument false greens, carried M86-2).** The gate counter accepts a foreign `python3 -c`
   self-test, a verdict-map substring, a silent six-cell row drop, a wrong-round pin, and runs G2/G3
   from the worktree under `--rev`; the record counter's "newest" is file order and 13 of 20 mutants
   survive the selftests. Both are named limits, not admitted quality.
8. **V86-8 (carried).** R85-4 (declared-case binding limits) and the planner-seat deviation held by
   the L1 stay on the queue.

Observation for the operator, not a lane defect: the fleet working tree carries
` M .ufo/reports/round-84/kama.md` (another lane's report) plus untracked `.scratch/closure-*` files;
neither is kaidoku round-86 work. SHONEN box 2 remains genuinely unchecked (no end-to-end domain task
this round); boxes 1, 3 and 4 are asserted `[~]` by the author and are not checkable by this non-author
from the round's own artifacts, so no `[x]` is warranted and none is written.
