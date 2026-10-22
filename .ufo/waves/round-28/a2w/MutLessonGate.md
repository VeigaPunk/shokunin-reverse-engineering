# Round 28 a2w — mutation probe: the entry_ok source-row checks

Seat: MutLessonGate. UTC window 2026-10-22T18:20Z–18:27Z. Lane tip read: 2832c5b3e20d84729bbd7f1b30afc081de9557b5.

## What I attacked

The `entry_ok` check inside both round-28 counters:

- `tools/round-28/c1-heldout-naming.py` (`check_entry`, lines 316-345)
- `tools/round-28/c2-filtered-flag.py` (`check_entry`, lines 119-141)

Both use the same rule: the entry's `source:` line must name at least one `S###` id that is present in `corpus/SOURCES.md` at the reviewed revision, **absent** from `corpus/SOURCES.md` at `--base`, a row with at least 11 columns, status `mined`, opened `2026-10-22`, and named inside the `## Gate` section of `corpus/lessons/round-28.md`.

## Method (sandbox only, no lane writes except this report)

```
git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutLessonGate/clone
python3 /fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutLessonGate/mutate.py      # 2026-10-22T18:26:29Z
python3 tools/round-28/c1-heldout-naming.py --root <clone> --rev <rev> --base <base>
python3 tools/round-28/c2-filtered-flag.py  --root <clone> --rev <rev> --base <base>
```

Fixture written in the clone: one minimal entry per counter (each naming exactly **one** source row), two SOURCES rows `S901` (C1) and `S902` (C2), and a minimal lesson whose `## Gate` section lists both rows. Sandbox history: `B0` (lane-tip tree, neither row), `Bx` (only `S901`), `By` (only `S902`), `T` (both rows plus entries plus Gate). Each mutant is one commit on top of `T` changing one field, one row or one base. Baseline is asserted to pass; a failing baseline would have stopped the probe.

## Results — entry_ok per mutation

| # | mutation | counter | entry_ok | exit | verdict |
|---|---|---|---|---|---|
| 0 | baseline (fixture passes) | C1 / C2 | 1 / 1 | 1 / 0 | baseline holds |
| M1 | C1 row `S901` status `mined` -> `candidate` | C1 | **0** | 1 | killed |
| M2 | C1 row `S901` opened `2026-10-22` -> `2026-10-21` | C1 | **0** | 1 | killed |
| M3 | C1 row `S901` absent from `## Gate` | C1 | **0** | 1 | killed |
| M4 | C1 row `S901` also present at `--base` (`Bx`) | C1 | **0** | 1 | killed |
| M5 | C2 row `S902` status `mined` -> `candidate` | C2 | **0** | 1 | killed |
| M6 | C2 row `S902` opened `2026-10-22` -> `2026-10-21` | C2 | **0** | 1 | killed |
| M7 | C2 row `S902` absent from `## Gate` | C2 | **0** | 1 | killed |
| M8 | C2 row `S902` also present at `--base` (`By`) | C2 | **0** | 1 | killed |
| M9 | C1 row named only outside `## Gate` (in `## Mistakes`) | C1 | **0** | 1 | killed |
| M10 | C2 row named only outside `## Gate` (in `## Mistakes`) | C2 | **0** | 1 | killed |

Every mutant also produced the counter's own message, e.g. M1 output line
`FAIL source: line names no S### new since base, mined, opened 2026-10-22 and in ## Gate`.

Each mutation is isolated: the counter whose row was not touched kept `entry_ok=1` in every run (M1-M4 leave C2 at 1; M5-M10 leave C1 at 1).

## Surviving mutants

**None.** All ten mutants were killed; both `entry_ok` checks hold against the four requested mutations.

## Other observations (labels)

- Observation: C1 exits 1 in every run, baseline included, because carrier `h09` is refused by REA (`runs_ok=60/61`, `rows_complete=186/187`). The C1 exit code therefore cannot signal an entry failure, which is why `entry_ok` is the reported metric. C2 exits 0 when `entry_ok=1` and 1 when it is 0.
- Observation: at the live lane tip the real entries pass both checks: C1 `runs_ok=60/61 rows_complete=186/187 tally_equal=1 entry_ok=1` (exit 1, h09 only); C2 `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=1` (exit 0).
- Inference: the real C1 entry names eight ids (`S086, S084, S085, S075, S076, S077, S078, S021`) and the real C2 entry names four (`S084, S085, S078, S076`) on the `source:` line. The check accepts **any one** qualifying id, so a single-row mutation against the real entries would survive by design; my minimal fixture (one row per entry) is what makes each mutation decisive. This is a coverage note, not a defect.
- Observation: `gate_ids` is section-scoped; a row named only under `## Mistakes` does not qualify (M9, M10 killed).

## Restoration evidence

- The lane was never written. Its committed counter bytes are byte-identical to the sandbox copies: C1 sha256 `29c2b571ac97098ac90b6aefc2112306b8b816722fe25abb3d84e03f22eeb27c`, C2 sha256 `4fdf7db81c5e56b3dfe8232ae87b89e3094e047f979adb088550381095fd60ef`. The only lane file I created is this report.
- Every mutant lived in its own sandbox commit on its own branch (`mut/M1-...` .. `mut/M10-...`); the probe ends checked out on `mut/tip` at `T` (fixture bytes intact: SOURCES `ef5bf1a0d6e4b4db724a9271b85771659668ee1757667eb66deccd9b41f44c22`, lesson `28fd18a029fadac204470c761aa4b8ca24e2418b4053e30c83f3517453ea54ad`, entry C1 `f39ca1ea41e2448a03da2909e9cd70667562b6ecff6f06c708fe326e57f84bb9`, entry C2 `607ec8f9d7893ff1591f6d9e1a4dc2772cc31e77514e96ce487bd86f1d595ab9`). The pristine lane-tip tree is still reachable in the clone as `origin/main` (`2832c5b3`).
- The scratch clone (387 MB) is disposable and stays under `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutLessonGate/`.

## Artifacts (sha256)

- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutLessonGate/mutate.py` — `7adf534612e6c2232d8ddfd1662174d47142320f1cabea0bf2e8ba7c2d4f8741` (driver: builds the fixture, applies the mutants, runs both counters).
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutLessonGate/out/runs.json` — `0571b6703745b7e0f0fd3e3ac6fd1e023c1f8c2652615c8f36c4a52ac6e95158` (full stdout of every counter run, per scenario).
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/MutLessonGate/clone/` — sandbox clone at `2832c5b3` with branches `mut/base0`, `mut/base-c1`, `mut/base-c2`, `mut/tip`, `mut/M1-...`..`mut/M10-...`.

No tool was installed or upgraded for this seat (`python3` and `git` were already present).
