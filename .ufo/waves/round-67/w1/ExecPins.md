# ExecPins — round 67 / w1: frozen pins, freeze order, selftests, R29 gate

Seat: ExecPins (leaf). Machine receipt: `.ufo/waves/round-67/w1/ExecPins/pins.json`
(`kaidoku-r67-execpins-v2`, with `observations` and `findings`). No tool installed, no git/jj
write, nothing written under `corpus/`, `tools/`, `PROVINCE.md` or any sibling lane.

**The lane moved eight commits under this seat.** The first pass ran while the freeze commit was
`HEAD` (21:52 -0300) and was clean. Between 21:57:02 and 22:05:19 the L1 landed eight commits that
edit the C1 counter three times, the gap rule once, the mutation battery once, and the claims
container three times. The receipt records **three epochs** (freeze / HEAD / worktree) and a
timestamped `observations` list; this report is anchored on the immutable one.

Snapshot: `HEAD = eadc2188e10598c27a51ddd222022243f8a42965` at `2026-11-04T01:05:48Z`.

## Headline

| statement | verdict |
|---|---|
| at the freeze `3663e6b2`: 7/7 pins == blobs, order intact, selftests green, gate `CLEAN` | **holds** |
| at HEAD `eadc2188`: 7/7 pins == blobs | holds |
| pins unchanged since the freeze | **fails** — 3 of 7 changed (counter, gap rule, battery) |
| container unamended since the freeze (A0, declaration pointer) | **fails** — 3 edits |
| both claims' kill rule ("a post-freeze instrument edit") | **triggered** — see F1 |

So the freeze commit is sound in itself; what a round-67 verdict cannot rely on is that the
instrument being scored is the instrument the freeze pinned. That is F1 and it is the L1's call,
not this seat's.

## 1. Pins — `sha256(git show <rev>:<path>)` vs the pin recorded in `claims.json` at that rev

| instrument | pin at freeze | blob at freeze | pin at HEAD | blob at HEAD | changed since freeze |
|---|---|---|---|---|---|
| `tools/round-67/avm-le-counter.py` | `f78ed365…` | `f78ed365…` | `5d6cc82a…` | `5d6cc82a…` | **yes** (3 edits) |
| `tools/round-67/mutation-battery.py` | `cabc0a0b…` | `cabc0a0b…` | `ecf55987…` | `ecf55987…` | **yes** (1 edit) |
| `tools/round-67/gap-rule-v2.json` | `e66ba022…` | `e66ba022…` | `b55d5e87…` | `b55d5e87…` | **yes** (1 edit) |
| `tools/round-67/c1-run.sh` | `00be5a87…` | `00be5a87…` | `00be5a87…` | `00be5a87…` | no |
| `tools/round-50/c1-counter.py` | `9820811b…` | `9820811b…` | `9820811b…` | `9820811b…` | no |
| `tools/round-66/closure-boundary.py` | `3c5cfb03…` | `3c5cfb03…` | `3c5cfb03…` | `3c5cfb03…` | no |
| `tools/round-66/coverage-selfcheck.py` | `1be9d046…` | `1be9d046…` | `1be9d046…` | `1be9d046…` | no |

Full 64-hex values are in `pins.json` → `instrument_table`. Every pin matched the blob at its own
epoch; none is a hash typo. All four files under `tools/round-67/` at the freeze are pinned —
no unpinned file in that directory. Embedded pins agree with the container:
`ENGINE_PIN 9820811b…`, `CLOSURE_PIN 3c5cfb03…`, `COVERAGE_PIN 1be9d046…`.

## 2. Freeze order

| check | result |
|---|---|
| `git log --diff-filter=A --format=%H -- .ufo/waves/round-67/claims.json` | still exactly one commit: `3663e6b2` |
| instruments commit `39a91a99` ancestor of the freeze | yes (rc 0) |
| base `a7a4ce69` ancestor of the instruments commit / of the freeze | yes / yes |
| carry-in `cf705c53` ("r66 non-author closure … QUALITY #34") ancestor of the freeze | yes (rc 0) |
| container unamended since the freeze | **no** (`6dcc447e`, `66389549`, `eadc2188`) |

Post-freeze commits at snapshot (`git log 3663e6b2..HEAD`):

```
a4c1d0fc 21:57:02  data run — four carrier receipts                         (+4 run.json)
1e7fe7b7 21:57:37  instrument correction — lane-relative gap-rule name       (counter, control-dryrun)
6dcc447e 21:57:44  freeze disclosure — supersession recorded                 (claims.json)
454071dd 22:01:47  data receipts — the four after.json envelopes             (+4 after.json)
ecc4de0e 22:01:48  instrument correction 2 — the REA package re-pin          (counter, control-dryrun)
66389549 22:02:06  freeze disclosure 2 — the REA re-pin recorded             (claims.json)
7cfe83e4 22:05:19  instrument repairs from wave 1 — rule silent row restored, clause set unchanged,
                   rule pinned, control receipt bound, battery kill test exact-set
7cfe83e4 22:05:19  (same commit) rule + battery + counter
eadc2188 22:05:19  freeze disclosure 3                                      (claims.json)
```

Positive: all four `after.json` and all four `run.json` receipts are committed at HEAD.

## 3. Selftests

Run at HEAD's bytes (the receipt records both epochs' results where they differ):

| instrument | command | result at HEAD | result at the freeze |
|---|---|---|---|
| `mutation-battery.py` | `--selftest --root <lane> --work <scratch>` | exit 0, `cases=10 failures=0` (adds `case-inventory`), equals the re-taken `l1/pre/selftest-c2.json` | exit 0, `cases=9 failures=0`, equalled the freeze-time receipt |
| `closure-boundary.py` | `--selftest` | exit 0, `cases=30 failures=0` | same (file unchanged) |
| `coverage-selfcheck.py` | `--selftest` | exit 0, `cases=26 failures=0` | same (file unchanged) |
| `c1-counter.py` | `--selftest` | exit 0, 169 cases, `green_ok 17`, `red_ok 152`, 57 probes, `failures []` | same run (engine blob identical at both revs) |

The 169-case run reproduces the committed `l1/pre/selftest-r50.txt` counters exactly; 2 of 57
probes differ only in the scratch path embedded in their `problems` string, not in verdict.

Supplementary, not the L1's after-arm: `mutation-battery.py --score --rev 3663e6b2` →
`survived_before 2, killed_before 0, killed_after 2, verified true, exit 0`, pristine `30/26`
green, failed cases `arm-false-bound` and `equiv-doctored-bound, equiv-doctored-diffs`. The battery
writes mutants only under `--work`; `git status -- tools/` stayed clean after it.

## 4. R29 freeze gate — round-67 entry (identical at `--rev 3663e6b2` and `--rev HEAD`)

```json
{"claims_file": ".ufo/waves/round-67/claims.json", "findings": [], "freeze": "3663e6b21dccf4c4957f459301156664d8b151d6", "instruments": ["tools/round-67/avm-le-counter.py", "tools/round-67/mutation-battery.py"], "verdict": "CLEAN"}
```

Aggregate `audited 42, clean 21, required_clean [], required_failed []`, exit 0. The gate anchors
on the first-add commit, so it reports the same entry at every HEAD and cannot see a supersession
(F6). Its `summary` counters (`INSTRUMENT_PIN_MISMATCH 2`, `INSTRUMENT_REVISED 17`, …) are
historical across 42 freezes, not this round. Round-67 is not in `flagged`.

## 5. Timeline observed by this seat

| observed (UTC) | HEAD | state |
|---|---|---|
| ~01:52 (first pass) | `3663e6b2` | HEAD == freeze, 7/7 pins, gate `CLEAN`, `tools/` clean |
| ~01:58 | `6dcc447e` | 7/7 at HEAD; counter pin `f78ed365 → 55decb51` |
| 01:03:50 | `66389549` | 7/7 at HEAD; counter pin `e44cacf5`; receipt snapshot |
| 01:05:18 | `66389549` | counter, rule, battery, `PROVINCE.md`, three C2 pre receipts dirty |
| 01:05:29 | `7cfe83e4` | **3 of 7 pins failed at HEAD** — artifacts repaired 30 s before the re-pin |
| 01:05:48 | `eadc2188` | 7/7 at HEAD; 3 pins changed since the freeze; gate still `CLEAN` |

## Findings

### F1 — BLOCKING: five instrument supersessions and three container edits against a freeze that defines itself as the first-add commit

- Instrument edits since the freeze: counter at `1e7fe7b7`, `ecc4de0e`, `7cfe83e4` (**3**);
  gap rule at `7cfe83e4` (**1**); battery at `7cfe83e4` (**1**). Container edits: `6dcc447e`,
  `66389549`, `eadc2188` (**3**).
- The container still defines the operative freeze as *the commit that first adds this file*
  (`3663e6b2`), A0 still says "no claim amendment after this file", and the declaration pointer
  still reads "(no amendments)".
- **Both** kill rules name `a post-freeze instrument edit` → "not verified, reported, never
  narrowed". R67-C1 is exposed by the counter and rule edits; R67-C2 by the battery edit.
- The edits are honestly disclosed (`instrument_supersessions`, five entries; A10, A11, A12) and
  the reasons reproduce: the patched `GAPRULE` was an absolute path while the engine reads its
  rule through `git show <rev>:<path>` (exit 2); the round-42 `package_lock_sha256` `d42d56f0` is
  no longer reproducible; the wave-1 repairs restored the silent row, kept the clause set whole,
  pinned the rule and bound the control receipt. Disclosure is not compliance with the kill rule:
  as written, **neither claim can be verified this round** unless the L1 redefines the freeze, and
  the container's own definition does not.

### F2 — BLOCKING: A4 still misstates the patch surface

A4 (unchanged) says the patched names are exactly `GAPRULE, AFTERDIR, ENTRY, STEM, CORE_HEADING,
FRONTIER_MARK, OPENED_DATES, PROV_BASE, PROV_SEGMENT, WORK_OVERRIDE and CLAUSES (dropping
carrier_fresh_ok)`. At HEAD the instrument assigns `…, WORK_OVERRIDE, rea_package_problems` and
**does not patch `CLAUSES`** (`DROPPED_CLAUSES` deleted at `7cfe83e4`; A12 states "the clause set
is unchanged (no dropped clause)"). The module docstring still says "patching exactly five things"
and its numbered list omits the rea-pkg patch. A4 and A12 also contradict each other on
`carrier_fresh_ok`.

### F3 — RESOLVED BY SUPERSESSION: `removed.silent` was absent at the freeze and restored at `7cfe83e4`

At the freeze the rule (`e66ba022`) had no `removed.silent`, while A5 and the docstring said
"`allowed`/`removed`/`structural` are unchanged" — false at that commit; measured effect was
silent `1 → 0` on `c6430`/`c6490` with `gaps_ok` unchanged. At HEAD (`b55d5e87`) the silent block
is back (`{"char-device": ["247:0"]}`), so `allowed`/`removed`/`structural` are now identical to
the round-50 rule and A5 is true. The repair is a post-freeze rule edit, i.e. another F1 instance;
the predicate itself was never affected (it counts `carriers_matched`/`gaps_ok` only, and the
before-arm receipts of both epochs record 2/4 and 4/4).

### F4 — BLOCKING: A0 cites a receipt that does not exist

A0: "…`git merge-base --is-ancestor <carry-in> <freeze>` exit 0, receipt
`l1/records/r67-order.txt`". That path is absent at `3663e6b2`, absent at HEAD (`git cat-file -e`
rc 128), absent on disk, and no `*r67-order*` exists anywhere. The order facts themselves are
**true** and were verified here independently (§2). Remedy is a commit of the receipt at the cited
path or a correction of A0 — outside this seat's write scope.

### F5 — INFO: the gap rule now fails closed (fixed at HEAD)

`RULE_V2_PIN = b55d5e87…`; `score()` raises on drift (exit 2) and records `rule.pin` and a
`control_receipt` binding (`control_ok true`, `gaps_ok_round50 2`). Before `7cfe83e4` the rule was
only recorded, never compared. The pin value itself postdates the freeze.

### F6 — INFO: the R29 gate is rev-local and scope-limited

Same `CLEAN` entry at `--rev 3663e6b2` and `--rev HEAD`; it did not flag the 3/7 pin-mismatch
window. It audits only the two `tools/round-67/` instruments — the five cross-round pins were
verified here directly.

### F7 — INFO: provenance substitution in the REA re-pin (for the critic)

`REA_PKG_R67` binds `rea-agents 6.5.0` by `package.json` `a5003023…` **and** the lock this host
resolves, `815c18f1…`, replacing the round-42 pin `d42d56f0…` whose bytes "no copy … survives".
`evidence_id_ok` stays required, but the oracle identity now depends on the local npx cache.

### F8 — INFO: pin and artifact should land atomically

At `7cfe83e4` the three repaired artifacts were committed 30 s before the container re-pin
(`eadc2188`); a seat sampling HEAD in that window saw 3/7 pins fail. Commit the artifacts and the
re-pin together.

## Supplementary checks

- R67-C1 `--control` re-run at the current bytes (`5d6cc82a`, rule `b55d5e87`): `gaps_ok_round50 2`,
  `gaps_ok_round67 4`, `exit 0`, `control_ok true`, `rule_problems` all `[]`, red controls
  `round67_rule_still_fails true`, `publication_check_names_it true` (`dev/led`),
  `junk_rule_would_pass true`. At the freeze the committed receipt recorded the same numbers with
  counter `f78ed365`.
- `tools/round-67/c1-run.sh` is a pure rename fork of `tools/round-50/c1-run.sh`: after
  `kaidoku-r50→kaidoku-r67`, `round-50→round-67`, `R50-C1→R67-C1` the bytes are identical
  (868 lines each).
- Predicates are byte-identical across `plans/round-67-claims.md` (unwrapped), `claims.json` and
  each instrument's `PREDICATE` (C1 310 bytes, C2 373 bytes).
- `tools/round-50/gap-rule.json` unchanged since its own freeze commit `435d41fd`
  (`sha256 43f7c8d7…`), which is also `rule_r50_sha256` in the control receipts.
- Carrier cache: the four files under `/fast/scratch/hyaku/kaidoku-r67/carriers/` hash to their
  names (4/4), matching `tools/round-50/carriers.json` (`g7581`, `g7582`, `c6490`, `c6430`).

## Not run by this seat

- R67-C1 `--score` (the four carrier data runs and the after-arm) — the L1's.
- R67-C2 after-arm `--score` at the record — the L1's (the freeze-rev supplementary run is labelled
  as such in `pins.json` and left no artifact in `corpus/`).

## Limits

- The lane was still being written at the snapshot; `PROVINCE.md` remains modified in the worktree
  (not this seat). Anything committed after `2026-11-04T01:05:48Z` is outside this receipt.
- `pins.json` embeds both epochs' pin tables and the six observations above; it is the authoritative
  machine record if this prose and the lane diverge later.
- Scratch `/fast/scratch/hyaku/kaidoku-r67/ExecPins` removed before yield.

Report: .ufo/waves/round-67/w1/ExecPins.md
