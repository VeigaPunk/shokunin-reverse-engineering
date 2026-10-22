# MutQualityRow38 — mutation test of QUALITY row 38 (instrument committed before data)

Seat `KaidokuR28a2.MutQualityRow38`, round 28 attempt 2, wave a2w. Target: routed defect 8 of
`corpus/lessons/round-27-verifier-spotcheck.md` — give QUALITY rows 38–40 the mutation test the
dead seats did not run. This seat covers row 38 only.

**Verdict: the row-38 check HOLDS behaviourally, but the counters' own `--selftest` does not
cover it.** 4 of 10 mutations die on the shipped selftest; **6 survive it** while demonstrably
accepting data committed before the instrument. That is a coverage finding about the selftest,
not a defect in the row-38 contract, and this seat does not change the contract.

Claims below are **observations** unless labelled inference. No lane file was written except
this report; the lane working tree is unchanged by this seat.

## 1. The gate that enforces row 38

Row 38 (`corpus/QUALITY.md:38`) requires the instrument to be committed before the data it
counts, and to "refuse any run that started, and any evidence file that was first committed,
earlier than that commit". No separate row-38 gate script exists; both round-28 counters
implement the refusal themselves:

| id | file:line (pristine) | what it refuses |
|---|---|---|
| E1 | `c1-heldout-naming.py:97-102` | `first_commit_time()` = git first **add** commit (`--diff-filter=A`, `out[-1]`) |
| E2 | `c1-heldout-naming.py:177` | run whose `utc_start` is not after the instrument commit (`t <= counter_time`) |
| E3 | `c1-heldout-naming.py:186-188` | envelope first committed before the instrument (`added < counter_time`) |
| E4 | `c1-heldout-naming.py:241-243` | lookup response file first committed before the instrument |
| E5 | `c1-heldout-naming.py:237` | lookup fetched (`manifest.utc`) not after the instrument commit |
| E6 | `c1-heldout-naming.py:353` | `counter_time` = the instrument's own first commit time (the reference point) |
| E7 | `c2-filtered-flag.py:67-70` | `first_commit_time()`, same helper shape as E1 |
| E8 | `c2-filtered-flag.py:162-164` | response fetched not after the instrument commit (`t <= ctime`) |
| E9 | `c2-filtered-flag.py:167-169` | response file first committed before the instrument (`added < ctime`) |
| E10 | `c2-filtered-flag.py:142` | `ctime` = the instrument's own first commit time |

Both files are under `tools/round-28/` in the lane.

On the real lane bytes at tip `a2673116` both counters pass every row-38 clause, with no
row-38 refusal message in either output (§5). Instrument commits `87d3dfb6` (C1, 14:17:16-03:00)
and `86fa8526` (C2, 14:21:55-03:00) precede the data commits `ca4069a4` (14:22:32),
`cb8d495e` (14:25:49) and `a2673116` (14:45:05). Row 38's ordering holds for round 28.

## 2. Method

Sandbox clone of the lane at `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow38/clone`
(HEAD `a2673116`, tree clean; clone bytes byte-identical to the lane: sha256
`29c2b571ac97…eeb27c` C1, `4fdf7db81c5e…fd60ef` C2). Two detectors, each run against
**pristine, mutated and restored** bytes:

* **D1 — the counter's own `--selftest`**, the detector named in the assignment. Baseline:
  C1 `selftest cases=21 failures=0` exit 0; C2 `selftest cases=17 failures=0` exit 0.
* **D2 — a behavioural probe** (`scenario.py`) that rebuilds the counter's own selftest fixture
  then moves the evidence *before* the instrument in git history, keeping every byte and every
  sha256 identical. Four modes: `early-data` (evidence added 10:30Z, instrument 11:00Z),
  `touch-after` (added 10:30Z, mode-only touch 12:00Z), `readd-after` (added 10:30Z, removed
  11:45Z, re-added 12:00Z, identical bytes), `same-second` (evidence committed normally after
  the instrument, run/fetch timestamp set to exactly the instrument's commit second). All four
  refuse on pristine bytes (C1 `row38_refusals=5`/2, C2 `3`), so a baseline failure would be
  inconclusive.

After each mutation the file was restored from the pristine copy; the restoration is proved by
sha256 plus an empty `git -C clone status --porcelain -- <file>`. Final clone tree clean, both
counter sha256 values equal the lane's.

## 3. Mutations (diff = pristine → mutant, against the clone file)

| id | counter | diff | weakens | selftest (D1) | killed by (D2) |
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

**Selftest summary: 4 killed (M4, M6, M9, M10), 6 survived (M1, M2, M3, M5, M7, M8).**

## 4. The surviving mutants are real (coverage finding)

A survivor only counts if it changes behaviour. Each does, and D2 shows the change. Exact
output, from `out/M*.scn-*.txt`. M2 (C1, envelope grace) under `early-data`:

```
pristine: runs_ok=0/2 rows_complete=0/3 tally_equal=0 entry_ok=0   row38_refusals=5
          REFUSED: FAIL k1: envelope first committed before the counter
mutant:   runs_ok=2/2 rows_complete=0/3 tally_equal=1 entry_ok=1   row38_refusals=3
          REFUSED: FAIL row 5c36b186: 4byte-5c36b186-p0.json first committed before the counter; …
```

The mutant **accepts** envelopes committed before the instrument (`runs_ok` 0/2 → 2/2); only
the lookup-side clause still refuses. M1 (C1, `out[-1]` → `out[0]`) under `readd-after`, where
the file is added before the instrument and re-added after it with identical bytes:

```
pristine: runs_ok=0/2 rows_complete=0/3 … row38_refusals=5   (refuses "envelope first committed before the counter")
mutant:   runs_ok=2/2 rows_complete=3/3 tally_equal=1 entry_ok=1   row38_refusals=0   exit=0
```

M8 (C1, guard deleted), M3 and M5 show the same shape; M7 (C2) goes under `readd-after` from
`responses_complete=0/3` to `responses_complete=3/3`, `row38_refusals=0`.

**Inference (well supported):** the shipped selftest exercises the *timestamp* clauses
(E2, E5, E8 — M4, M6, M9 die) but has **no case at all** for the *commit-order* clauses
(E1, E3, E4, E7, E9 — M1, M2, M3, M5, M7, M8 survive). `red-early-run` and `red-lookup-early`
move a *timestamp* earlier; no selftest case ever commits an envelope or response file
**before** the instrument's commit. That is why M8 — deleting the refusal outright — still
leaves the selftest green. This is a coverage finding about the selftest, not a weakness in
the row-38 contract.

## 5. Commands and evidence

All outputs are in `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow38/out/`.

| step | command | result |
|---|---|---|
| clone | `git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin …/clone` | HEAD `a2673116`, tree clean |
| baseline D1 | `python3 clone/tools/round-28/c1-heldout-naming.py --selftest` | exit 0, `selftest cases=21 failures=0` |
| baseline D1 | `python3 clone/tools/round-28/c2-filtered-flag.py --selftest` | exit 0, `selftest cases=17 failures=0` |
| baseline D2 | `python3 scenario.py clone/tools/round-28/<counter> <c1\|c2> <mode>` | 8 pristine probes all refuse, exit 1 |
| per mutation | `bash run-mut.sh <M#> <file> <c1\|c2>` → diff, selftest, 4 probes, restore | §3 |
| restore proof | `sha256sum clone/tools/round-28/<file>` + `git -C clone status --porcelain -- <file>` | C1 `29c2b571ac97…eeb27c`, C2 `4fdf7db81c5e…fd60ef`, status empty |
| real lane | `python3 tools/round-28/c1-heldout-naming.py --root . --rev a2673116 --base 935c366` | exit 0, `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=0` |
| real lane | `python3 tools/round-28/c2-filtered-flag.py --root . --rev a2673116 --base 935c366` | exit 0, `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=0` |

UTC starts (2026-10-22, `out/RUN-LOG.md`): M1 18:42:23Z, M2 18:42:58Z, M3 18:43:11Z,
M4 18:43:19Z, M5 18:43:33Z, M6 18:43:41Z, M7 18:43:47Z, M8 18:43:53Z, M9 18:44:08Z, M10 18:44:15Z.

## 6. Artifacts (all under `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutQualityRow38/`)

| path | sha256 |
|---|---|
| `scenario.py` (probe harness, 4 modes) | `e0444ab54fc21edc433cd763f5eb5da5f8a2859ff59da8c8e03496d74b06e262` |
| `run-mut.sh` (diff → selftest → 4 probes → restore → sha256 proof) | `ede18cd568bfadd4bfc299ab7612ec0ac0f3e8a9db682997079ae1d5b633f30f` |
| `pristine/c1-heldout-naming.py` | `29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c` |
| `pristine/c2-filtered-flag.py` | `4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef` |
| `out/RUN-LOG.md` (UTC per mutation) | `9a80bf229b635f0c8f96db41f7459c3239f2de9544758c2a78a7e6cf9ee6f855` |
| `out/M{1..10}.diff`, `out/M{1..10}.selftest.txt`, `out/M{1..10}.scn-<mode>.txt`, `out/PRISTINE-c{1,2}-<mode>.txt` | 72 files in `out/` |
| `clone/` | sandbox clone, tree clean |

## 7. What this seat does not claim

* It does not claim row 38 is violated for round 28: on the real lane bytes both counters
  refuse nothing row-38-related, and the instrument commits precede the data commits (§1).
* It does not change the row-38 contract or any lane file. The recommendation is that a future
  round's selftest gain a red case that commits an envelope/response file **before** the
  instrument — the case M8 shows is missing. This seat proposes; the L1 decides.
* Tooling: no installs, no upgrades, no pacman transactions; Python 3 and git were already
  present.
