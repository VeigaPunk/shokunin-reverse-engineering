# R45W2Waves — attack on the round shape (round 45, wave 2)

Seat: `R45W2Waves`. Attacked artefact: the round's own seat accounting — `w1-dispatch.json`,
`r45-w1-results.json`, `w2-dispatch.json`, `r45-w2-results.json` (absent), both swarm registries,
the `.ready.dispatched` handshake markers, and the seat-count sentences the record derives from
them (`LOG.md:3273`, `SCORECARD.md:3527-3528`). Read-only on the lane and the fleet: the only bytes
written are this directory and the report copy `.ufo/waves/round-45/w2/R45W2Waves.md` that this
seat's `Report:` trailer names. Every number below is reproduced by
`python3 .ufo/waves/round-45/w2/R45W2Waves/check_shape.py <out>` (exit **1**, 9 of 28 checks fail);
commands, exit codes, sha256s and UTC times are in `receipts.md`.

## 1. Verdicts

| # | attack (what it attacks) | verdict | evidence |
|---|---|---|---|
| V1 | w1 dispatch seat set == w1 ledger seat set | **holds** | `diff` of the two sorted name lists: empty, 40/40 (R2) |
| V2 | w1 spec items == registry members == dispatch tasks | **holds** | 40/40/40 identical names (R5) |
| V3 | w2 spec items == registry members == dispatch tasks == ready ids | **holds** | 36/36/36/36 identical names (R3, R5, R16) |
| V4 | wave 1 has 40 seats *delivered* (as `SCORECARD.md:3527` and `LOG.md:3273` read) | **falsified** | 25 delivered: 25 non-null `output`s, 25 report `.md` + 25 seat dirs, 15 `output:null` + note (R7). True number of *initiated* seats: 40 |
| V5 | wave 2 has 32 seats (`LOG.md:3273`, `SCORECARD.md:3527`) | **falsified** | `w2-spec.json`, `w2-dispatch.json`, `w2/swarm-registry.json`, `w2.ready.dispatched` all carry **36**. The spec was already 36 at `faa875bc` (12:37:11), the commit that introduced it; `abfeda50` (12:35:26), which wrote "wave 2: 32 seats", predates the spec and the number was never corrected at A2, A3 or `1d04c6af` (R9, R10) |
| V6 | `SCORECARD.md:3527-3528` sources both counts from `{r45-w1,r45-w2}-results.json` | **falsified** | `r45-w2-results.json` is absent in the worktree (`ls` exit 1) **and at HEAD** (`git cat-file -e HEAD:…` exit 128; `git log --all --` on the path is empty, so no commit ever carried it). The w1 half is sourced correctly but is the wrong quantity (V4) |
| V7 | each wave is 32–64 seats | **holds on dispatched** (40, 36) · **falsified on delivered** (25) · w2 delivered **not run** | R3 vs R7; `r45-w2-results.json` absent → exit 2 by construction |
| V8 | the two waves sum to 64–128 | **holds on dispatched** (76) · **not run on delivered** (25 + unknown) | R3; exit 2 for the delivered basis, not a pass |
| V9 | attack share ≥25 % (addendum §2, roles reviewer/critic/mutation-tester/labrat) | **holds** | w1 dispatched 11/40 = 0.275, w1 delivered 8/25 = 0.32, w2 dispatched 19/36 = 0.5278 (R1) |
| V10 | few connector seats | **holds** | exactly 1 per wave (R1) |
| V11 | role histogram as recorded / recordable | **holds as measured**, see §2 | R1, R4 |
| V12 | dead seats carry their last error text | **not run** | the ledger schema has no `status` field (`keys = agent,name,note,output`) and no writer produces error text; 15 identical notes, `output:null` (R1, R13) |
| V13 | `r45-w1-results.json` is orchestrator output | **falsified** (exit 1): the committed dispatcher cannot produce these bytes; **exit 2** on who wrote them | `scripts/hyaku/inline-dispatcher.py:295` is the only dead-seat note string and differs; `:262` refuses `.dispatched`/finalize unless every seat spawned; `grep` over `scripts/` finds no emitter of the ledger's string (R13, R14) |
| V14 | the wave-2 dispatch names the round's measured revision | **falsified** | shared `context` says "amendment A1 `1f4b27f8` (the measured revision)"; `LOG.md:3315` and `SCORECARD.md:3589-3591` say A3 `f59565b7` is the measured revision; only 12/36 seat prompts name A3, 1 names only the landing, 23 name no sha (R16) |
| V15 | the dispatch `policy` block is a committed policy | **holds for v1, with a rule conflict below** | all fields equal `scripts/hyaku/ufo-wave-policy.json` (32–64 band, `maxLanes` 256, `minLanes` 16, ramp 5/700 ms, ceiling 1056, `hardCeiling` 256). Policy **v2** (64–128) has been used by **0 of 47** committed wave dispatches, rounds 16–45 (R11) |
| V16 | the `.ready.dispatched` handshake conforms to its writer | w2 **holds**; w1 **falsified** | w1 marker is a bare epoch `1793201921.739129` (= 2026-10-28T15:38:41Z); every committed dispatcher version writes an ISO line, plus the id map since `216cfd36` (R14, R15) |

## 2. Numbers (measured, no interpolation)

```
wave 1: dispatched 40 (spawn 40, resume 0) | ledger results 40 | ledger "seats" 40
        delivered 25 | dead 15 | report files 25 | attacked-as-met 25/40
wave 2: dispatched 36 (spawn 36, resume 0) | spec 36 | registry 36 | ready ids 36
        results ledger ABSENT -> delivered unknown, exit 2
round : dispatched 76 | delivered 25 + unknown
```

Role histogram — dispatched → delivered:

| role | w1 disp | w1 deliv | w2 disp |
|---|---|---|---|
| connector | 1 | 0 | 1 |
| critic | 4 | 2 | 5 |
| executor | 17 | 12 | 8 |
| mutation-tester | 3 | 3 | 4 |
| revenger | 1 | 0 | 1 |
| reviewer | 4 | 3 | 10 |
| scout | 5 | 3 | 1 |
| scribe | 3 | 2 | 2 |
| sentinel | 1 | 0 | 3 |
| simplifier | 1 | 0 | 1 |
| **total** | **40** | **25** | **36** |

Four roles contributed **zero** delivered reports in wave 1: `connector`, `revenger`, `sentinel`,
`simplifier`. The sentinel role — the one whose job is to catch a lane going off-contract — has
0/1 delivered in w1 and 3 dispatched in w2.

## 3. Dead seats (15) and their "last error text"

Every one of the 15 carries `output: null` and the *same* note string, verbatim:

> `never spawned: host job-cap refusal during wave fill; wave completed without it (partial-fill loss recorded by L1)`

| # | seat | role |
|---|---|---|
| 1 | `R45W1CritSweepClass` | critic |
| 2 | `R45W1RevControls` | reviewer |
| 3 | `R45W1SentDeepRead` | sentinel |
| 4 | `R45W1ProbeTmp` | executor |
| 5 | `R45W1InhSweepEvidence` | scout |
| 6 | `R45W1InhTipCounters` | executor |
| 7 | `R45W1InhQualityRows` | executor |
| 8 | `R45W1InhCommandA` | executor |
| 9 | `R45W1InhBlockCount` | executor |
| 10 | `R45W1InhSkillTail` | scout |
| 11 | `R45W1ConnFleetOwnership` | connector |
| 12 | `R45W1SimplDedupe` | simplifier |
| 13 | `R45W1RevengerSweepPath` | revenger |
| 14 | `R45W1ScribeLessonDraft` | scribe |
| 15 | `R45W1DistillPredicates` | critic |

There is **no per-seat error text anywhere**: no `status`, no `id`, no exit code, no stderr. The
only text is the one sentence above, and `scripts/hyaku/inline-dispatcher.py:290-296` shows why —
the ledger schema is `{name, agent, output, note}` and its only note is the kernel-restart
sentence. "Last error text" is therefore **not run (exit 2)**: the artefact class does not carry it.

The claim in that sentence is *plausible* but unverified: the lane had 25 seats running against a
host that carries ~40 live siblings and 379 parked agents, and
`scripts/hyaku/lane-addendum.md:80-82` documents tranche filling with a ~100-running-agent cap, so
a fill cap is the expected failure mode. I could not verify it: the refusal log lives in
`.ufo/state/` and `.ufo/watchdog.log`, both out of bounds for this seat. Marked `[INFERENCE]`.

## 4. Findings with fixes

**F1 — the record's wave-2 seat count is wrong by 4 and was wrong when written.**
`LOG.md:3273` ("wave 1 40 seats and wave 2 32 seats") and `SCORECARD.md:3527` ("wave 1: 40 seats;
wave 2: 32 seats") against `w2-spec.json` / `w2-dispatch.json` / `w2/swarm-registry.json` /
`w2.ready.dispatched` = 36. `git show abfeda50:…/w2-spec.json` exits 128 (the file did not exist
when the sentence was written) and the spec has carried 36 since `faa875bc`. Fix: 36, total 76, at
both sites, with the same "dispatched" qualifier as F2.

**F2 — the record reports initiated seats as if they were seats.** `SCORECARD.md:3527` and
`LOG.md:3273` say 40 for wave 1; the ledger's `seats` field is 40 (it is `len(results)` over the
*dispatch* names — `inline-dispatcher.py:296`), while 25 seats produced anything. Nothing in
`LOG.md` or `SCORECARD.md` states 25. Fix: state both quantities — "40 dispatched / 25 delivered
(15 never spawned)" — and add `produced`/`dead` counts to the ledger summary so a reader cannot
read `seats` as delivery.

**F3 — the SCORECARD names a ledger that does not exist.** `SCORECARD.md:3527-3528` sources the
counts from `{r45-w1,r45-w2}-results.json`; `r45-w2-results.json` is absent at HEAD (exit 1 on
`ls`). Fix: either land the wave-2 ledger, or cite the dispatch/registry for the wave-2 number and
say the ledger is expected.

**F4 — the wave-1 ledger is not the committed driver's output.** Three independent measurements:
(a) the only dead-seat note the committed dispatcher emits is
`orchestrator kernel restarted mid-wave; seat output was delivered to the orchestrator session but
not retained …` (`inline-dispatcher.py:295`) — round 35's ledger carries it 64 times (R12), round
45's carries it zero times; (b) no file under `/home/vgpnk/Projects/shokunin/scripts/` contains the
round-45 sentence (`grep` exit 1); (c) the dispatcher writes `.dispatched` and registers the wave
only when *every* seat spawned (`:262-265`), so a wave that never filled 15 seats never reaches
`finalize()` — and if the wave did fill and the seats died later, the note would be (a). Fix: keep
the machine note and add a separate `l1_note` field (or record the rewrite in `LOG.md`); a hand
sentence in the handoff file is the one thing a falsification wave cannot check.

**F5 — the wave-1 dispatch marker does not match its writer either.** `w1.ready.dispatched`
contains the bare epoch `1793201921.739129` (2026-10-28T15:38:41Z); every committed dispatcher
version writes an ISO timestamp line and, since `216cfd36`, an id map on line 2. `w2.ready.dispatched`
conforms. Same fix as F4, plus: if the running orchestrator is newer than `scripts/hyaku/inline-dispatcher.py`,
commit it — otherwise the wave's provenance is unverifiable from the repo. I cannot tell which:
the loaded driver is not observable → the *actor* claim stays exit 2.

**F6 — the wave-2 dispatch attacks the wrong "measured revision".** Its shared `context` line says
`amendment A1 1f4b27f8 (the measured revision)`; the record (`LOG.md:3309-3316`,
`SCORECARD.md:3583-3591`) says A3 `f59565b7` is the measured revision. Only 12/36 seat prompts were
updated to A3 when the dispatch was regenerated at `1d04c6af` (12:56:22); 1 names only the landing
`e715263c`; 23 name no sha. This matters because A3 changed exactly the two surfaces wave 2 attacks
(the `c1-run.sh` registry row and block 22's limit text). Fix: regenerate the context with A3, or say
"A3 measured; identical values at A1" and name A3 in every prompt that reads a landed file.

**F7 — the band test is only partly falsifiable because its rule contradicts itself.** The seat
contract and `lane-addendum.md:77-78` say round total 64–128; `lane-addendum.md:195` says "each
round is 32–128 seats in total". A 40-seat round would pass one and fail the other. Separately,
policy **v2** (`waveMinLanes 64`, `waveMaxLanes 128`) has been used by 0 of 47 committed dispatches
(rounds 16–45: `(64,100)`×16, `(32,64)`×30, `(32,256)`×1). Round 45's 40/36 is therefore *correct
under v1*, the declared shape ("two v1 waves"), and below v2's floor — both readings are defensible,
which is the defect. Fix: state which policy the round validates under in the round record (round 45
does not), and reconcile the 64–128 vs 32–128 totals in the addendum.

**F8 — a wave-2 seat id was taken before it spawned.** The ready marker maps
`R45W2Trends -> R45W2Trends-2`, i.e. an agent id `R45W2Trends` already existed when the dispatcher
spawned the seat. The ledger keys by seat *name*, so no join breaks; but this is the signature of a
duplicate spawn, and wave 2 is still running. Watch: if two `R45W2Trends` reports land, one seat is
double-counted. Cause unverified (exit 2) — the earlier agent's identity is only in `.ufo/state/`.

## 5. What this does to the round

- The round is **inside its declared band on dispatched seats** (76 total; 40 and 36) and
  **outside it on delivered seats for wave 1** (25 < 32). It is not a "40+36 round" in any
  delivered sense; it is a 25-delivered + pending round, and the record never says so.
- The loss is concentrated in verification roles: 4 of 10 role classes delivered nothing in wave 1,
  including the only sentinel. The claim-carrying seats (counters, registry rows, mutation-testers)
  all delivered, which is why the round's C1/C2 verdicts are not in question here — only the
  breadth of independent attack is.
- Two of the wave's own handoff artefacts (`r45-w1-results.json`, `w1.ready.dispatched`) cannot be
  produced by the committed fleet driver, so "the counts come from `*-results.json`" is an appeal to
  a file whose authorship is not established. That is the finding I would route first, ahead of the
  off-by-four.

## 6. Not run

| item | why |
|---|---|
| wave-2 delivered counts, wave-2 delivered band, wave-2 delivered attack share | `r45-w2-results.json` absent at 2026-10-28T16:01Z (exit 2, never a pass) |
| per-seat last error text for the 15 dead seats | no `status`/`id`/stderr field exists in the ledger schema; not observable in-repo |
| verification of "host job-cap refusal" | the refusal log is in `.ufo/state/` and `.ufo/watchdog.log`, out of bounds |
| m_flash ≥50 % of every wave (addendum run-7 block) | the ledger and registry carry no model field |
| whether the *running* orchestrator is the committed `inline-dispatcher.py` | the loaded driver is unobservable; only the repo copy can be read |

Install record: none. Tool inventory unchanged; portage/pacman untouched.
