# PriorOutsideDebt — R22 verifier lesson, current operator teaching, and new routed duties

Scope: locate and read the R22 outside-verifier lesson and any current operator teaching, then
enumerate only duties actually routed into round 23. Read-only except this report. Baseline for all
absence checks: `a3c92eb6bc70984e90ae5b895412de978840b2c5`.

Labels: `[OBS]` = command output or fetched bytes; `[INF]` = inference from those bytes; `[UNKNOWN]` =
not established by this seat.

## Findings

### 1. R22 verifier lesson — no corpus lesson file; the verification record is the MANIFEST closure entry

`[OBS]` There is no `corpus/lessons/round-22-verifier-spotcheck.md` at the R23 baseline and none in
any ref:

| command (cwd = lane) | result | exit |
|---|---|---|
| `git cat-file -e a3c92eb6bc70984e90ae5b895412de978840b2c5:corpus/lessons/round-22-verifier-spotcheck.md` | `fatal: path ... does not exist` | 128 |
| `git ls-tree -r --name-only a3c92eb -- corpus/lessons/ \| grep -E 'verifier\|operator'` | nine files, rounds 12–20 only; no 21/22/23, no `operator-*` | 0 |
| `git log --all --pretty=format: --name-only --diff-filter=ADMR -- 'corpus/lessons/round-2[23]-verifier-spotcheck.md' \| sort -u` | empty | 0 |

`[OBS]` The lane itself already recorded that the prior round's outside lesson was likewise absent:
`corpus/lessons/round-22.md:38` — “No round-21-verifier-spotcheck.md existed in the lesson inventory
at replacement start”; same statement at `.ufo/reports/round-22/kaidoku.md:95`.

`[OBS]` The R22 non-author verification was instead recorded in the fleet `MANIFEST.json` closure
entry, `MANIFEST.json:11169-11209` (0-based `rounds[415]`; file sha256
`61c29fb49277fd789acb4ebfb371f15c3de83639acbe73d3d70830558e30b844`):

- `:11198` commit `kaidoku-shokunin@aa1450b82f9ede35aada63efe8a34e01c6e02f72`; `:11199` closed
  `2026-10-21T14:29:48.942821Z`.
- `:11204` reviewer `CloseKaidoku22 (fresh non-author closure integrator), independent ReviewC1 and
  ReviewC2Sources slices`.
- `:11205` spotcheck: **agree** S055 original Saber envelope admit (`ok true`,
  `identify_flutter_build`, `flutter_detected true`, coverage partial); **agree** Godot
  parsed-negative admit (`ok true`, `flutter_detected false`); **agree** `inspect-dart-aot` Saber
  `unsupported_target` reject (producer `ok false`, four absent dynamic symbols); S051 quote
  `Debugging information is stripped out.` matches, while the docs do not establish APK build mode,
  runtime/source recovery or Dart SDK mapping.
- `:11206` rechecks: independent read-only runs at B `7787fea4`, V `e9db7e2`, H `aa1450b8`:
  C1 exits 1/1/1, held 0/1/1 of 6; C2 exits 1/0/0, accounted 0/14/14; claim-only separation;
  auxiliary gates evidence-verified, 18/18 producer-envelope pairs, 1135 prior files unchanged,
  sources 50→57, census exit 0.
- `:11208` notes: admitted only for the frozen finite coverage and calibration moves; C1
  `c1_incomplete` exit 1 is disclosed five-verb incompleteness; `/usr/bin/false` ADB controls prove
  only chosen-client refusal; Frida enumeration succeeds and impossible-PID refusal is not provider
  absence; W1 93 members/0 reports with per-child causes unknown; W2 64/55/9 provider failures;
  157 total, no replacements; all 102 reportless seats uncredited; **“Existing
  SOURCE/TIME/LINT-SANDBOX/CENSUS-GUARD/ADJACENCY residuals remain open.”**; no lane/report edits,
  promotion, redispatch, target execution or installs; ReviewC1 found no actionable defect and
  ReviewC2Sources no blocking finding.

`[INF]` The R22 verifier “lesson” therefore contains **no disagreement and no routed defect** to
convert into a QUALITY criterion. Its operative content is (a) three admits/one source reopen
agreeing with the lane, (b) the admission-scope limits, and (c) the open-residual list.

`[OBS]` Timeline: `corpus/lessons/round-22.md` mtime `2026-10-21 11:02 -03` and the fleet report
`2026-10-21 11:05 -03` both predate the closure at `11:29:48 -03`; round 23 is the first round that
can reflect the closure. No R22 closure seat report was located in the lane or the searched fleet
paths; the spotcheck text says it is “Recorded here under no-lane-write closure scope”
(`MANIFEST.json:11205`).

### 2. Current operator teaching — no operator lesson file exists at the R23 baseline or in history

`[OBS]` `git cat-file -e a3c92eb:corpus/lessons/operator-teaching.md` → absent, exit 128. Broader
checks:

| command (cwd = lane) | result | exit |
|---|---|---|
| `ls corpus/lessons/operator-*` | `No such file or directory` | 2 |
| `git ls-tree -r --name-only a3c92eb -- 'corpus/lessons/operator-*'` | 0 lines | 0 |
| `git log --all --pretty=format: --name-only --diff-filter=ADMR -- 'corpus/lessons/operator-*' \| sort -u` | empty | 0 |
| `find . -iname 'operator-*.md' -not -path './.git/*'` | none in the lane, tracked or untracked | 0 |

`[OBS]` This matches the independent R20 scout, which measured the set empty and never existing on
any ref: `.ufo/waves/round-20/w1/ScoutOperatorLessons.md:5-6,22-39`; the R18 scout reported the same
(`.ufo/waves/round-18/w1/ScoutOperatorLessons.md`, section 1).

`[OBS]` The current binding operator words are not a corpus teaching; they are the round-23 prompt's
verbatim campaign addendum: `.ufo/prompts/kaidoku-round-23.md:143-157` (operator directives of
2026-10-20: train to round 100, 64–100 subagents, route table, `jj` as git manager, commit/push each
round) and `:386` (all pacman transactions paused host-wide). The prompt's own teaching duty is
conditional at `:376-379`: read `round-22-verifier-spotcheck.md` **if it exists**, and “honor any
`corpus/lessons/operator-*.md` teaching not yet reflected.”

`[OBS]` The operator-directive block is unchanged between the two rounds:
`diff <(sed -n '141,158p' .ufo/prompts/kaidoku-round-22.md) <(sed -n '141,158p' .ufo/prompts/kaidoku-round-23.md)`
exits 0; the full prompt diff contains only round-number and attempt-label substitutions. `[INF]` No
new operator teaching text was introduced for round 23; the only new teaching-related duty is the
conditional check above.

`[INF]` No operator-teaching duty materializes for round 23: there is no file to read or reflect.
Inventing a teaching, or adding a QUALITY row attributed to one, would fabricate lineage.

`[UNKNOWN]` Whether an operator teaching exists outside the repository refs/worktree (e.g. an
unpersisted session message) is not established; this seat only establishes repo absence.

### 3. New routed duties actually in force (no assumed reports)

Only duties with a routing anchor are listed. “New” means introduced for round 23 by the frozen
declaration or the current prompt; “carried” means an explicit R22 closure obligation, not a new
deliverable.

| # | Duty | Routed by | Kind | Observable acceptance |
|---|---|---|---|---|
| D1 | State in the round report why no verifier-disagreement QUALITY row/fix was added | `.ufo/prompts/kaidoku-round-23.md:376-378`; absence evidence above | new (conditional; absence makes it not-applicable) | Round report states why not; this seat's evidence supplies the basis; it must not claim a spotcheck file exists |
| D2 | Carry SOURCE, TIME, LINT-SANDBOX, CENSUS-GUARD and kaidoku/revenger ADJACENCY residuals as **open** | `MANIFEST.json:11208`; `corpus/lessons/round-22.md:38` | carried | No round-23 text claims these closed; any change cites its own evidence |
| D3 | Keep R22 admission scope: finite moves only; no completeness/mastery, cryptographic authentication, provider availability, device absence, dynamic-analysis ownership or capability claim | `MANIFEST.json:11208`; `claims.json:46-52` (`not_claimed`) | carried | Round-23 wording matches; `no mastery` already in `claims.json:11,26` |
| D4 | Keep the 102 R22 reportless seats per-seat unknown; do not replace or explain by conjecture | `claims.json:63`; `MANIFEST.json:11208`; counts observed in `.ufo/waves/round-22/final-wave-outcomes.json` (W1 93 all `reportless_no_live_seat`; W2 55 reports/9 reportless) | carried | Report repeats per-seat unknown; no causal closure |
| D5 | R23-C1 cumulative sourced held count from 1/6 to **k/6 with k>=2**, exact k, no mastery | `claims.json:24-26` | new | `count-c1.py` at two revisions; exact k printed; exit/profile retained |
| D6 | New knowledge cites opened/mined **S058+** with exact `used-by`; preserve historical R22 witnesses; new evidence only under `round-23/evidence/c1` | `claims.json:28` | new | Registry rows and knowledge citations resolve; no inherited witness rewritten |
| D7 | Respect the no-execution boundary: no debugger/Frida live execution, no process attach/device/carrier execution; signals offline only; `inspect-dart-aot` static parsing only | `claims.json:29`; wave context | new | Retained argv plus absence of execution artifacts; adjacent ownership stays unresolved |
| D8 | Apply the seven C1 falsifiers (refusal, erased parent refusal, mention-only, lost inherited identify, double count, absent source linkage, unsupported relevance/ownership) | `claims.json:30-38` | new | Each falsifier has an exercised control or is named unevaluated |
| D9 | Frontier step: census before→after with exit 0; mine one mistake or paste the finding sweep; at least one claim sourced from a row opened this round | `.ufo/prompts/kaidoku-round-23.md:42,54-66,68-72,73-75` | new | Committed census outputs; round-23 `## Mistakes`; citation to an S058+ row |
| D10 | Resolve inherited uncommitted lane leftovers; never edit foreign files (`operator` sweeps, `round-*-aggregator-*`, `round-*-verifier-spotcheck.md`); name both in the report | `.ufo/prompts/kaidoku-round-23.md:373-375` | new | Report names the untracked `round-23/` wave tree and any resolution |
| D11 | Report extras: Trend verdicts, `Stale-lane`, tool installs | `.ufo/prompts/kaidoku-round-23.md:380-382` | new | Present in the fleet report |
| D12 | Operator campaign mechanics: 64–100 seats per wave, host route table, `jj` lane commits, pacman paused (install only via uv/npx/official binary, or L0) | `.ufo/prompts/kaidoku-round-23.md:143-157,182,386` | carried/current | Wave records show counts; no pacman transaction; installs recorded |

`[OBS]` The R22 no-harm floor that round 23 inherits is `claims.json:55-62`: prior knowledge/source
rows unchanged, LOG/SCORECARD prefixes preserved, prior admission criteria unchanged, R22 C1=1/6 and
C2=14/14 at final, map integrity and citation rules preserved, source census exit 0.

### 4. Explicitly not assumed (no report exists merely because a duty names it)

`[OBS]` The following are absent, not pending deliverables of this seat:

- `corpus/lessons/round-22-verifier-spotcheck.md` — absent at `a3c92eb`, exit 128.
- `corpus/lessons/round-23-verifier-spotcheck.md` — absent; history empty.
- `corpus/lessons/operator-*.md` — absent at every ref; untracked search empty.
- Any persisted R22 closure seat report (`ReviewC1`, `ReviewC2Sources`) — not found in the lane
  tree, `.ufo/reports/round-22/`, or the searched fleet `.ufo` paths (maxdepth 3); the closure
  record at `MANIFEST.json:11203-11208` is where the content was found, and the underlying seat
  reports were not located.
- Any R22 W1 seat report — `final-wave-outcomes.json` records 93/93 `reportless_no_live_seat`.

`[UNKNOWN]` Per-child W1 terminal cause; whether any unpersisted operator teaching exists; provider
availability over time; device absence; dynamic debugger/Frida ownership; independent non-author
admission of round 23. None is resolved here.

## Produced files

| path (absolute) | sha256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/PriorOutsideDebt.md` | final digest carried in this seat's result message |

An in-file digest names bytes that any later edit would change, so the final value is reported with
the seat result rather than embedded here. No other file was written by this seat.

## Installs

None. No package manager, `uv`, `npx`, binary download, config edit or host service change was used.
REA was not invoked; no MCP device was used; no target, device or carrier was executed.

## Open risks

- The R22 closure-only record can be lost to a MANIFEST rewrite; the lane has no R22 verifier
  lesson, so the entry quoted here is the only located account.
- Absence of a verifier spotcheck file is not absence of an outside opinion; the R22 closure entry is
  the only located persisted account.
- The 102-reportless figure depends on `final-wave-outcomes.json`'s per-seat statuses; it is not an
  independent re-observation of each seat.
- The prompt's conditional teaching duty is easy to misread as “must add a QUALITY row”; with no
  source file, adding one would fabricate lineage.
- Round-23 duties D5–D8 remain unexecuted by this seat; this report routes them, it does not verify
  them.
