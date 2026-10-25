# MutCounterClauses — five clause mutants of the R34-C2 shortcut-gate counter

Seat: `L1Kaidoku34-2.MutCounterClauses` (mutation-tester, leaf; no subagent dispatch).
Claim under attack: **R34-C2** (capability acquisition, axis depth), pre-freeze structure-blind
shortcut-replay gate, frozen at `c79bbe7b0959132b9873ff3431cf5eb313b58b33`
(`.ufo/waves/round-34/r34b/claims.json`, claim `claims[0]`).
Lane VCS: **not written** (no git/jj command of any kind was run). R34-C1: **not re-opened**
(`tools/round-34/elf-version-needs.py` and `version-needs-counter.py` were never executed; no
carrier, fixture or reader was executed as a program of interest; readers ran only as `python3`
children of the gate/counter, as the instrument itself does).
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w1/MutCounterClauses/` (1.1 MiB, all writes here).
Clock: all times UTC. Tools installed/upgraded: **none** — `/usr/bin/python3` 3.14.8, `sha256sum`,
`diff`, `xargs`; no network used.

## 0. Axes named (Godspeed)

| axis | proxy used here | preferred direction |
|---|---|---|
| A1 kill power | does a committed control's `GATE_COUNTER_*` result flip from MISS/UNEVALUABLE to `OK`? | an admitted control = clause proven load-bearing |
| A2 clause reach | which of the six frozen clauses can a control receipt make false *alone*? | more sole-clause coverage = better |
| A3 harm pole | does the mutant ever emit `GATE_COUNTER_OK` for a gate that the frozen predicate rejects? | false pass is the harmful pole |
| A4 evidence integrity | does the mutant still record what the gate actually said (line vs receipt fields)? | preserved evidence = better |
| A5 restoration | do pristine bytes survive byte-for-byte, with hashes before and after? | exact |

A3 is the severity axis. On this corpus **no mutant reaches A3**: no committed control is admitted.
The interesting result is on A2 — the corpus pins 4 of 6 clauses, two of them only jointly.

## 1. Baseline reproduced from pinned bytes (A0)

Scratch root built read-only from the lane (2026-10-25T07:19:07Z, exit 0):

```
S=/fast/scratch/hyaku/kaidoku-r34b/w1/MutCounterClauses
cp -a <LANE>/tools/round-34             $S/root/tools/round-34
cp -a <LANE>/.ufo/waves/round-34/r34b/controls/gates  $S/root/.ufo/waves/round-34/r34b/controls/gates
```

Copy bytes equal the lane and the `claims.json` pins (read-only `sha256sum`, 2026-10-25T07:24:20Z):

```
41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72  tools/round-34/c2-shortcut-gate-counter.py
8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558  tools/round-34/replay-gate.py
72b1294171b58ecb276ce84edcff0698c750d9f5e4490a60253e9385086b1428  tools/round-34/gate-config-naive.json
4483f3852429b4390656a1d8235e1d0a676e4da1e7d7841f20bd2b575c12ac9c  tools/round-34/gate-config-mini.json
fbb2eca683852f68997f5e9671bdeb8c16d886747a1e76e232757e81bb48dfce  controls/gates/gate-always-clean.py
777013c22dd096f308afebe93327c2f8f653088aef57b95d672d87110f748255  controls/gates/gate-junk-clean.py
d0b03f1b40ba94f2a373dfc4b63976a0df8ebbd6f37a9e1573723a65191e341e  controls/gates/gate-no-positive-check.py
0646a3dffb1e54ad4f63c1d9f1ec7b0688c0757778f9f18f99bbd542d06e78a8  controls/gates/gate-vacuous-no-floor.py
```

Baseline run of the **pinned** counter against all five committed controls
(`$S/run_matrix.sh`, 2026-10-25T07:19:17Z → 07:19:25Z; loop status 0, while each cell's exit is the
counter's own, below):

| control | counter exit | failing clauses | line |
|---|---|---|---|
| do-nothing | 2 | (gate_absent) | `GATE_COUNTER_UNEVALUABLE finding=gate_absent …` |
| gate-always-clean.py | 1 | red_refused, selftest_clean | `… selftest_failures=2 mutants_killed=3 red=REPLAY_GATE_CLEAN green=REPLAY_GATE_CLEAN …` |
| gate-junk-clean.py | 1 | red_refused | `… red=REPLAY_GATE_CLEAN … clauses_failed=red_refused` |
| gate-no-positive-check.py | 1 | mutants_killed, selftest_clean | `… mutants_killed=2 red=REPLAY_GATE_REFUSED …` |
| gate-vacuous-no-floor.py | 1 | selftest_clean | `… selftest_failures=1 red=REPLAY_GATE_REFUSED …` |

**Independent reproduction:** all ten committed control artefacts diff byte-identically to my
re-runs — `diff -q $S/out/baseline/<name>.json <LANE>/.ufo/waves/round-34/r34b/controls/<name>.json`
→ identical for `do-nothing`, `gate-always-clean.py`, `gate-junk-clean.py`,
`gate-no-positive-check.py`, `gate-vacuous-no-floor.py` (both `.json` and `.txt`, 10/10). The five
`gate_path` values also match, so my invocation shape
(`python3 -I -B c2-shortcut-gate-counter.py --root <root> --rev c79bbe7b… --gate <gate> --json-out <f>`)
is the same one that produced the committed receipts.

## 2. Method

`$S/mutate.py` (exit 0, 2026-10-25T07:19:54Z) copies the pristine counter once per mutant and
applies **one** exact-string replacement (anchor occurrence asserted `== 1`); mutants are separate
files, the pristine scratch copy is never edited. Each cell is one counter invocation over the
scratch root with `--gate` pointing at the control, `--json-out` capturing the receipt:

```
$S/run_one.sh <counter.py> out/<series> <tag> <gate-rel-path>
xargs -P 8 -L 1 ./run_one.sh < 66 invocations   # GATE_COUNTER exits: 0 OK / 1 MISS / 2 UNEVALUABLE
```

66 invocations, 2026-10-25T07:20:29Z → 07:20:36Z, `xargs` exit 0. A mutant is **killed by a
control** only when that control's counter exit becomes 0 (`GATE_COUNTER_OK`); a baseline failure
does not count.

## 3. The five assigned mutants (one clause each)

| id | mutation (single anchor) | sha256 | Δ |
|---|---|---|---|
| a | `red_refused`: `receipt["red"]["exit"] == 2` → `in (1, 2)` | `aa3e82f6…cd94` | +5 B |
| b | delete clause `"green_positive_meets_target": …positive_matched"] == 8,` | `500e61d9…d5a` | −82 B |
| c | delete clause `"mutants_killed": receipt["mutants_killed"] == TARGET["mutants_killed"],` | `21a2c96b…ca4` | −81 B |
| d | `red`/`green` `verdict` read from the **printed line** first token instead of the JSON payload | `11722f6f…7fa` | −6 B |
| e | `red`/`green` `verdict` hardcoded to `TARGET["red_verdict"]` / `TARGET["green_verdict"]` | `14b659c0…0ce` | −32 B |
| a′ (extra reading of "accept exit 1") | `red_refused`: `== 2` → `== 1` | `19603281…ac2` | ±0 |

Full unified diffs: `$S/mut/*.py` vs `$S/root/tools/round-34/c2-shortcut-gate-counter.py`; each
diff is exactly the anchor above and nothing else (verified by `diff -u`, one hunk per file).

## 4. Mutant × committed control matrix (A1/A3)

Cells are counter exits: `0` = OK (admitted), `1` = MISS, `2` = UNEVALUABLE.
Raw: `$S/matrix_raw.txt`, receipts `$S/out/controls/<mutant>/<control>.json`.

| mutant | do-nothing | always-clean | junk-clean | no-positive-check | vacuous-no-floor | controls wrongly admitted |
|---|---|---|---|---|---|---|
| a | 2 | 1 | 1 | 1 | 1 | **0** |
| b | 2 | 1 | 1 | 1 | 1 | **0** |
| c | 2 | 1 | 1 | 1 | 1 | **0** |
| d | 2 | 1 | 1 | 1 | 1 | **0** |
| e | 2 | 1 | 1 | 1 | 1 | **0** |
| a′ | 2 | 1 | 1 | 1 | 1 | **0** (but see F7) |

**Result: 0/30 cells flip.** No assigned mutant admits any committed control.

Two mutants are even *behaviourally equivalent* to the pinned counter on this corpus: for (a) and
(d) all five receipts — including `do-nothing`'s early-return path — are **byte-identical** to the
pinned receipts (`diff -q out/baseline/<c>.py.json out/controls/a…/<c>.json` → 5/5, likewise `d…`).
(a) is equivalent because no control returns exit 1; (d) is equivalent because for every committed
gate the printed line's first token equals the payload verdict. For (b) and (c) the only receipt
difference is the deleted clause key itself (one `-` line: `"green_positive_meets_target": true` /
`"mutants_killed": true`); for (e) it is the one `verdict` field (F6).

## 5. Why — clause coverage of the committed corpus (A2)

Derived from the five committed receipts, and confirmed against the gate diffs
(`diff -u tools/round-34/replay-gate.py controls/gates/<control>.py`):

| frozen clause | false in which committed receipt | sole discriminator? |
|---|---|---|
| `gate_present` | do-nothing | **yes** |
| `selftest_clean` | always-clean, no-positive-check, vacuous | yes (vacuous) |
| `mutants_killed` | no-positive-check (`mutants_killed=2`) | **no** — same receipt also has `selftest_failures=2` |
| `red_refused` | always-clean (paired with selftest_clean), junk-clean | yes (junk-clean) |
| `green_clean` | **none** — all five controls print `REPLAY_GATE_CLEAN` on the green case | — never exercised |
| `green_positive_meets_target` | **none** — all five report `green_positive_matched=8` | — never exercised |

Control mechanics behind that table (each control is the pinned gate with one branch disabled):

* `gate-always-clean`: `if over:` → `if False:` (line 124). Red case returns CLEAN/exit 0 →
  `red_refused` false; its selftest also fails `red-one`,`red-two`.
* `gate-no-positive-check`: `if not positive["met_target"]:` → `if False:`. Runtime on both pinned
  configs is unchanged (both have `structural=8`), so the gate still prints REFUSED/CLEAN; only its
  **selftest** (`positive-below`, `no-positive-check-anchor-missing`) and `mutants_killed=2` move.
* `gate-vacuous-no-floor`: drops `len(shortcuts) < MIN_SHORTCUTS`. The two pinned configs have 8
  shortcuts, so runtime is unchanged; only the selftest case `two-shortcuts-unevaluable` fails.
* `gate-junk-clean`: 11-line stub that prints fixed CLEAN lines and forges
  `failures=0, mutants_killed=3, rows=[structural matched 8]`. Caught only by `red_refused`.

This is the whole explanation of section 4: (b) has nothing to kill it; (c) is always paired with
`selftest_clean`; (a) and (d) are invisible because the corpus never produces exit 1 or a
line/payload disagreement.

## 6. Isolation probes — are the clauses load-bearing at all? (A2/A3, supplementary)

Seven scratch-only gates (`$S/root/.ufo/…/controls/gates/iso-*.py`, mode 0644) each answer
`--selftest`, red and green with **target-shaped** receipts and deviate in exactly one observable.
They are **not committed controls** and I claim nothing about them beyond clause discrimination.
Sanity anchor: `iso-control-ok.py` (all observables at target) is admitted by the pinned counter
(`GATE_COUNTER_OK`, exit 0, 2026-10-25T07:20:3xZ), so any rejection below is attributable to the
deviation.

| probe (sha256 prefix) | pinned counter | a | b | c | d | e |
|---|---|---|---|---|---|---|
| iso-control-ok `0b0606` | **OK 0** | OK | OK | OK | OK | OK |
| iso-red-exit1 (red refuses, exit 1) `cdd7e9` | MISS 1 (`red_refused`) | **OK 0** | MISS | MISS | MISS | MISS |
| iso-positive-below (structural 5/8) `c5c23f` | MISS 1 (`green_positive_meets_target`) | MISS | **OK 0** | MISS | MISS | MISS |
| iso-mutants2 (`failures=0`, `killed=2`) `732558` | MISS 1 (`mutants_killed`) | MISS | MISS | **OK 0** | MISS | MISS |
| iso-line-json-split (line=target, payload=opposite) `26cd00` | MISS 1 (`red_refused,green_clean`) | MISS | MISS | MISS | **OK 0** | **OK 0** |
| iso-forged-verdict (both verdicts `REPLAY_GATE_ALLOWED`, line=payload) `d669a4` | MISS 1 (`red_refused,green_clean`) | MISS | MISS | MISS | MISS | **OK 0** |
| iso-payload-wins (payload=target, line=opposite) `0945c1` | **OK 0** | OK | OK | OK | MISS 1 | OK |

Raw: `$S/out/iso/<tag>/<probe>.json|.txt`; 36 + 6 invocations, 2026-10-25T07:20:36Z and
07:22:2xZ, each exit recorded in `$S/matrix_raw.txt` / transcript.

**Every assigned clause is load-bearing**: each mutant is admitted by the probe that deviates in
exactly its clause, and by no other probe except the two documented overlaps in F4/F6.

## 7. Findings

**F1 (High, coverage) — `green_clean` and `green_positive_meets_target` are unpinned.**
All five committed controls print `REPLAY_GATE_CLEAN` on the green case and report
`green_positive_matched=8`. Mutant (b), which deletes the positive clause outright, is
indistinguishable from the pinned counter on the corpus (0 admissions, all receipts identical
except the missing clause key), and no control would notice a green-clearing defect.
Evidence: `$S/out/baseline/*.json` (`green` blocks), `$S/out/controls/b_drop_green_positive/*.json`.

**F2 (High, coverage) — `mutants_killed` is never a sole discriminator.**
Its only witness (`gate-no-positive-check`, `mutants_killed=2`) also fails `selftest_clean`
(`failures=2`). Mutant (c) therefore leaves that control at MISS with
`clauses_failed=selftest_clean` (`$S/out/controls/c_drop_mutant_kill/gate-no-positive-check.json`):
the kill clause contributes nothing to the corpus verdict. It is not redundant *in principle* —
`iso-mutants2` (failures 0, killed 2) is admitted by (c) and rejected by the pinned counter.

**F3 (Medium) — exit 1 is unmodelled: widening survives; strictness is unwitnessed.**
The pinned gate's protocol is `{0 CLEAN, 2 REFUSED, 3 UNEVALUABLE}` (`replay-gate.py:14-16,120-128`);
1 is the *counter's* own MISS code, not a gate verdict. No control refuses with exit 1, so mutant
(a) is byte-equivalent to the pinned counter on the corpus, while `iso-red-exit1` shows the clause
does its work off-corpus. The mirror mutant a′ (`== 1`) is rejected by a conforming gate
(`iso-control-ok` → MISS `red_refused`) yet still passes the whole corpus (0 admissions), because
**the corpus contains no control that a correct counter must admit**.

**F4 (Medium) — the evidence-authority direction is unpinned.**
For every committed gate the printed line and the JSON payload agree, so (d) is byte-equivalent to
pinned on the corpus, and the pinned counter never asserts agreement: `iso-payload-wins` (stdout
says `REPLAY_GATE_CLEAN` on the red case, payload says `REPLAY_GATE_REFUSED`) is admitted
`GATE_COUNTER_OK` by the pinned counter. A gate whose digest line lies about its own verdict is
scored from the JSON and reported as OK, and only (d) notices — in the opposite direction.

**F5 (Medium, plan-vs-measurement) — two `control_plan` entries do not describe what the committed
receipts measure.** `claims.json claims[0].control_plan` says
`"vacuous gate without the shortcut floor -> UNEVALUABLE, MISS"` but the measured receipt is
`red=REPLAY_GATE_REFUSED` (exit 2), MISS solely via `selftest_clean`; and
`"gate whose positive control is all-false -> green clause fails, MISS"` but the measured receipt
has `green_clean=true`, `green_positive_matched=8`, MISS via `mutants_killed,selftest_clean`.
F1 and F2 are the direct consequence: the intended green-side exercise was implemented inside the
gate's selftest, not against the counter's green clauses. I make no claim that this invalidates the
predicate — the controls still refuse/MISS for the predicate's reasons — only that the registered
clause coverage is narrower than the plan text asserts.

**F6 (Low, evidence integrity) — (e) falsifies its own receipt.** With hardcoded verdicts,
`gate-always-clean` and `gate-junk-clean` receipts record `red.verdict=REPLAY_GATE_REFUSED` beside
`red.line="REPLAY_GATE_CLEAN …"` while `red_refused` stays false (exit/class still bind). No
clause compares the two fields, so the contradiction is only visible to a human reader.

**F7 (Low, corpus asymmetry) — no admission-direction control exists.** All five committed controls
are gates the counter must reject; over-strict mutants (a′) survive all 30 cells. Corollary for
L1: a "must be admitted" gate control is missing from the control set (my `iso-control-ok` is a
scratch stand-in, not a substitute).

## 8. Lane hygiene observation (reported, not caused by me)

`<LANE>/tools/round-34/mini-fix/__pycache__/mini-counter.cpython-314.pyc`
(10 625 B, sha256 `c6f49a4e6b577d9a91909d712ed8b7979739398ecba6162d39993d467c6f4b1a`,
mtime `2026-10-25 04:19:33.095 -0300` = **07:19:33Z**) exists in the frozen instrument tree.
It is not mine: every invocation I made used `-I -B` and `--root $S/root`, and my scratch
`root/tools/round-34/mini-fix/` contains **no** `__pycache__` (verified: `find root -name
__pycache__ -o -name '*.pyc'` → empty). It post-dates my read-only copy (07:19:07Z) and is
consistent with another seat running a counter against the lane root without `-B`. Flagged for
L1: a bytecode artefact inside a frozen instrument directory changes the tree the freeze covers.

## 9. Restoration and no-harm evidence

* The pristine scratch counter was never edited: mutants are separate files. Hash before the matrix
  and after (`2026-10-25T07:22:38Z`) is identical, and equals both the lane file and the
  `claims.json` pin: `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72` (3/3).
* Mutant hashes are stable across the whole exercise (section 3 values re-measured at 07:22:38Z).
* No lane file was written: every lane path I touched was opened read-only (`cp -a` out,
  `sha256sum`, `diff`, `cat`, `find -newermt`). Lane instrument mtimes remain 2026-10-25
  04:07–04:13 local, i.e. pre-dating this seat; the only later lane mtime is the foreign
  `__pycache__` of section 8.
* No VCS command (git or jj) was run in the lane; no `pacman`, no service change, no network.
* The only lane file this seat writes is this report.

## 10. Limits / non-claims

* The seven `iso-*` probes are synthetic receipt emitters built in scratch; they discriminate
  clauses, they are not controls and must not be landed as controls without L1's decision.
* I did not re-score the claim, edit any doc, or judge whether the frozen predicate should be
  amended. Section 7's F1/F2/F7 are coverage findings, not evidence that a defective gate passes.
* No claim is made about the gate's own five-branch mutant set beyond the shipped `--selftest`
  numbers it reported through the counter (`mutants_killed`, `selftest_failures`).
* R34-C1 was not opened, executed or scored at any point.

## Verdict

`MUT_COUNTER_CLAUSES: 5/5 assigned mutants SURVIVED the five committed controls (0/30 cells flip; 0 controls wrongly admitted); 5/5 clauses KILLED by dedicated scratch isolation probes (a→red-exit1, b→positive-below, c→mutants-killed, d→line/payload split, e→forged verdict). Committed control corpus pins 4/6 clauses and only 2 of them solely (gate_present, red_refused); green_clean and green_positive_meets_target are exercised by no control, mutants_killed never alone, exit-1 and line-vs-payload authority not at all. Severity: coverage gap, no false pass. Restoration: pristine 41d59703… intact 3/3, mutants isolated, lane unwritten.`
