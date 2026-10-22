# MutQualityRow38 — mutation test of QUALITY row 38 in the round-28 counters

Seat `KaidokuR28a2.MutQualityRow38`. Scope: routed defect 8 of `corpus/lessons/round-27-verifier-spotcheck.md`, QUALITY row 38 only. Lane read-only; all mutation work in the sandbox clone `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow38/clone` (`git clone` of the lane at `a2673116`). Times are UTC, 2026-10-22. Installs: none.

## Verdict

- **The row-38 check holds behaviourally.** On pristine bytes both counters refuse every piece of evidence committed before the instrument, and on the real lane bytes at tip `a2673116` neither counter emits a row-38 refusal. Observation.
- **The shipped selftest does not cover the commit-order half of row 38.** 4 of 10 mutants die on `--selftest`; **6 survive it** while demonstrably accepting data committed before the instrument. Observation.
- **The gap is exact.** The selftest exercises the *timestamp* clauses (E2, E5, E8) and has no case for the *commit-order* clauses (E1, E3, E4, E7, E9): `red-early-run` and `red-lookup-early` move a timestamp earlier, and no case ever commits an envelope or response file before the instrument. M8 deletes the refusal outright and the selftest stays green (21 cases, 0 failures). Inference, well supported by the mutant table and the probe outputs.

## Where the rule lives

No separate row-38 gate script exists. Both round-28 counters implement the refusal themselves, at ten sites:

- `tools/round-28/c1-heldout-naming.py` — E1 `:97-102` `first_commit_time()` = git first **add** commit (`--diff-filter=A`, `out[-1]`); E2 `:177` run `utc_start` not after the instrument commit (`t <= counter_time`); E3 `:186-188` envelope first committed before the instrument (`added < counter_time`); E4 `:241-243` lookup response file first committed before the instrument; E5 `:237` lookup fetched not after the instrument commit; E6 `:353` `counter_time` = the instrument's own first commit time.
- `tools/round-28/c2-filtered-flag.py` — E7 `:67-70` the same `first_commit_time()` helper; E8 `:162-164` response fetched not after the instrument commit (`t <= ctime`); E9 `:167-169` response file first committed before the instrument (`added < ctime`); E10 `:142` `ctime` = the instrument's own first commit time.

Lane commits: instruments `87d3dfb6` (C1, 14:17:16-03:00) and `86fa8526` (C2, 14:21:55-03:00) precede the data `ca4069a4` (14:22:32), `cb8d495e` (14:25:49), `a2673116` (14:45:05).

## Method

Detector D1 is the counter's own `--selftest`, run in the clone with `TMPDIR=…/tmp`: baseline on pristine bytes C1 `selftest cases=21 failures=0` exit 0, C2 `selftest cases=17 failures=0` exit 0. Each mutant was applied to the clone's copy, measured, then the file restored from `pristine/`.

Detector D2 is a behavioural probe (`scenario.py`) that rebuilds the counter's own selftest fixture and then moves the evidence *before* the instrument in git history, keeping every byte and every sha256 identical: `early-data` (evidence added 10:30Z, instrument 11:00Z), `touch-after` (added 10:30Z, mode-only touch 12:00Z), `readd-after` (added 10:30Z, removed 11:45Z, re-added 12:00Z, identical bytes), `same-second` (evidence committed normally after the instrument, run/fetch timestamp set to exactly the instrument's commit second). On pristine bytes all eight probes refuse (C1 `row38_refusals=5`/2, C2 `3`), so no baseline is failing and every verdict below is attributable.

## Mutants

Diff = pristine → mutant, against the clone file. "Selftest" is D1, "probe" is D2.

| id | ctr | diff | weakens | selftest | killed by |
|---|---|---|---|---|---|
| M1 | C1 | `first_commit_time`: `return int(out[-1]) if out else None` → `return int(out[0]) if out else None` | E1: newest add commit instead of first, so a re-added file looks committed after the instrument | **SURVIVED** 21 cases / 0 failures | probe `readd-after` |
| M2 | C1 | envelope: `added < counter_time` → `added < counter_time - 86400` | E3: allows an envelope committed up to a day before the instrument | **SURVIVED** 21 / 0 | probe `early-data`, `touch-after`, `readd-after` |
| M3 | C1 | lookup: `added < counter_time` → `added < counter_time - 86400` | E4: allows a response file committed up to a day before | **SURVIVED** 21 / 0 | probe `early-data`, `touch-after`, `readd-after` |
| M4 | C1 | run: `t <= counter_time` → `t <= counter_time - 86400` | E2: allows a run started up to a day before | **KILLED** | `red-early-run` (`exit=0 want=1`) |
| M5 | C2 | response: `added < ctime` → `added < ctime - 86400` | E9: allows a response committed up to a day before | **SURVIVED** 17 / 0 | probe `early-data`, `touch-after`, `readd-after` |
| M6 | C2 | fetch: `t <= ctime` → `t <= ctime - 86400` | E8: allows a fetch up to a day before | **KILLED** | `red-early-fetch` (`exit=0 want=1`) |
| M7 | C2 | `first_commit_time`: `out[-1]` → `out[0]` | E7: same as M1, C2 side | **SURVIVED** 17 / 0 | probe `readd-after` |
| M8 | C1 | envelope guard → `if False:` | E3: deletes the envelope commit-order refusal outright | **SURVIVED** 21 / 0 | probe `early-data`, `touch-after`, `readd-after` |
| M9 | C1 | lookup fetch: `t <= counter_time` → `t <= counter_time - 86400` | E5: allows a lookup fetched up to a day before | **KILLED** | `red-lookup-early` (`exit=0 want=1`) |
| M10 | C1 | `count()`: added `counter_time = 0  # MUTANT: …` | E6: the instrument's commit time stops being the reference, so comparisons are against 0 | **KILLED** (2 cases) | `red-early-run` **and** `red-lookup-early` |

**Selftest: 4 killed (M4, M6, M9, M10), 6 survived (M1, M2, M3, M5, M7, M8).**

## The survivors are real, not equivalent mutants

A survivor only counts if behaviour changes, and D2 shows it. Exact output, from `out/M*.scn-*.txt`.

M2 (C1, envelope grace) under `early-data`: pristine `runs_ok=0/2 rows_complete=0/3 tally_equal=0 entry_ok=0`, `row38_refusals=5`, refusing with `FAIL k1: envelope first committed before the counter`; the mutant gives `runs_ok=2/2 rows_complete=0/3 tally_equal=1 entry_ok=1`, `row38_refusals=3` — it **accepts** envelopes committed before the instrument (`runs_ok` 0/2 → 2/2) and only the lookup-side clause still refuses.

M1 (C1, `out[-1]` → `out[0]`) under `readd-after`, where the file is added before the instrument and re-added after it with identical bytes: pristine `runs_ok=0/2 rows_complete=0/3`, `row38_refusals=5`; mutant `runs_ok=2/2 rows_complete=3/3 tally_equal=1 entry_ok=1`, `row38_refusals=0`, `exit=0`.

M8 (C1, guard deleted), M3 and M5 show the same shape; M7 (C2) goes under `readd-after` from `responses_complete=0/3` to `responses_complete=3/3`, `row38_refusals=0`.

## Commands, evidence, artifacts

Baseline D1 `python3 clone/tools/round-28/c1-heldout-naming.py --selftest` → exit 0, `selftest cases=21 failures=0`; `…/c2-filtered-flag.py --selftest` → exit 0, `selftest cases=17 failures=0`. Baseline D2 `python3 scenario.py clone/tools/round-28/<counter> <c1|c2> <mode>` → all 8 pristine probes refuse, exit 1. Per mutant `bash run-mut.sh <M#> <file> <c1|c2>` → diff, selftest, 4 probes, restore. UTC starts: M1 18:42:23Z, M2 18:42:58Z, M3 18:43:11Z, M4 18:43:19Z, M5 18:43:33Z, M6 18:43:41Z, M7 18:43:47Z, M8 18:43:53Z, M9 18:44:08Z, M10 18:44:15Z. On the real lane `python3 tools/round-28/c1-heldout-naming.py --root . --rev a2673116 --base 935c366` → exit 0, `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=0`; `python3 tools/round-28/c2-filtered-flag.py --root . --rev a2673116 --base 935c366` → exit 0, `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=0`.

Artifacts under `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow38/` (72 files in `out/`): `scenario.py` `e0444ab54fc21edc433cd763f5eb5da5f8a2859ff59da8c8e03496d74b06e262` · `run-mut.sh` `ede18cd568bfadd4bfc299ab7612ec0ac0f3e8a9db682997079ae1d5b633f30f` · `pristine/c1-heldout-naming.py` `29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c` · `pristine/c2-filtered-flag.py` `4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef` · `out/RUN-LOG.md` `9a80bf229b635f0c8f96db41f7459c3239f2de9544758c2a78a7e6cf9ee6f855` · `out/M{1..10}.diff`, `out/M{1..10}.selftest.txt`, `out/M{1..10}.scn-<mode>.txt`, `out/PRISTINE-c{1,2}-<mode>.txt`.

## Restoration and lane state

- Clone files restored byte-exact: after the last restore `sha256sum` gave `29c2b571…eeb27c` (C1) and `4fdf7db8…fd60ef` (C2), equal to the pristine copies and to the lane's own bytes; `git -C clone status --porcelain` is empty for the whole tree.
- The lane was written only by this report. The lane's two counters still hash `29c2b571…` and `4fdf7db8…`. No git write, no jj command, no REA call, no network request was made.
- This seat changed no counter and did not change the row-38 contract; whether the L1 turns the coverage gap into a counter selftest case (a fixture that commits an envelope/response file before the instrument) is the L1's decision.
