# R34b w1 — LabratSeedSensitivity: 100-seed probe of the frozen shortcut gate

Seat: `L1Kaidoku34-2.LabratSeedSensitivity` (leaf executor item, no lane writes).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` @ frozen `c79bbe7b0959132b9873ff3431cf5eb313b58b33`.
Claim under test: **R34-C2** (`.ufo/waves/round-34/r34b/claims.json`, declared `2026-10-25T07:11:52Z`).
Scratch (all harness code and raw receipts): `/fast/scratch/hyaku/kaidoku-r34b/w1/LabratSeedSensitivity/`.
Machine: `python3 = /usr/bin/python3` = `Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1]` (evidence: this session, `-VV`). No tool installs or upgrades were made; pacman/uv/npx untouched.

## 1. Hypothesis tested

**H** — across 100 distinct `--seed` values, no *registered* shortcut class reaches the green target of 8 matches
(`tools/round-34/mini-fix/mini-counter.py`, `TARGET = 8`).

Registered classes are exactly the seven `shortcuts[]` entries of `tools/round-34/gate-config-mini.json`
(`tools/round-34/gate-config-mini.json:12-20`): `all-false`, `size-keyed`, `fixed-slice`, `digest-keyed`,
`string-scan`, `record-order-replay`, `label-memorization`. `readers/structural.py` is the gate's
`positive_control`, not a shortcut; `readers/label_keyed.py` is pinned in `claims.json` but is **not**
registered (see §8).

## 2. Instruments verified before use

Read-only `sha256sum` of every path in `claims.json:claims[0].pins`, compared against the frozen pins:
26/26 matches, 0 mismatches. Verifier output: `/fast/scratch/hyaku/kaidoku-r34b/w1/LabratSeedSensitivity/out/bounds.json`
(companion printout captured in the same cell) and the `sha256sum` transcript of `2026-10-25T07:18:42Z`.
Key digests confirmed: `mini-counter.py 43ef669f…`, `expected.json 5ebb5349…`, all eight fixtures,
all nine readers (`all_false e1a509b0…`, `digest_keyed 87577e18…`, `fixed_slice 8a1d1ce5…`,
`label_keyed f727c152…`, `label_replay_full c772227e…`, `record_order_replay 11d655af…`,
`size_keyed 740a7f7e…`, `string_scan 4a46f5e2…`, `structural 2f399cab…`).
Nothing under the lane was written; every `--root` was the lane and the counter only reads it.

One-run calibration before the sweep (`--seed 0 --control-reader …/size_keyed.py`, `2026-10-25T07:18:45Z`):
exit 1, `matched=1`, `finding=records_mismatch`, 131 ms → one counter invocation scores all eight fixtures.

## 3. Method (700 assigned runs)

Harness: `…/LabratSeedSensitivity/sweep.py` (runs the *pinned* counter as a subprocess, 4 threads, seeds
`"0"…"99"` passed verbatim, `PATH=/usr/bin:/bin`, 200-char stderr capture; nothing but `out/results.jsonl`
and `out/summary.json` written).

```
cd /fast/scratch/hyaku/kaidoku-r34b/w1/LabratSeedSensitivity
/usr/bin/python3 sweep.py > out/sweep-stdout.txt 2> out/sweep-stderr.txt      # exit 0
```
Start `2026-10-25T07:18:54Z`, end `2026-10-25T07:19:18Z`, `wall_ms=23718`, **700/700 runs recorded**
(`out/results.jsonl`, 700 lines), per-run elapsed min 120 / median 133 / p95 147 / max 215 ms, **no timeout,
no non-empty stderr, every run exit 1** (exit 1 is the counter's honest "below target" return).
Raw: `out/results.jsonl`, `out/summary.json`, `out/sweep-start.txt`, `out/sweep-end.txt`.

## 4. Result: max matched per registered class (100 seeds each)

| class | reader | distinct `matched` | **max** | argmax seeds | fixtures ever matched |
|---|---|---|---|---|---|
| all-false | `all_false.py` | {0} | **0** | all 100 | — |
| size-keyed | `size_keyed.py` | {1} | **1** | all 100 | `alpha.mrec` (100/100) |
| fixed-slice | `fixed_slice.py` | {0} | **0** | all 100 | — |
| digest-keyed | `digest_keyed.py` | {0} | **0** | all 100 | — |
| string-scan | `string_scan.py` | {0} | **0** | all 100 | — |
| record-order-replay | `record_order_replay.py` | {0,1} | **1** | **88** | `beta.mrec` (1/100) |
| label-memorization | `label_replay_full.py` | {0} | **0** | all 100 | — |

No class reached 8; no run carried `met_target=true`. Target never approached beyond **1/8**.
Per-fixture match counts (same evidence): `out/summary.json` + the per-fixture counter printed in the
verification cell of `2026-10-25T07:21:58Z`.

## 5. Why the seeds move (the probe is not a no-op)

Seeds genuinely re-permute: distinct transformed fixtures over seeds 0–99 = 100/100 for
alpha, delta, eta, gamma, theta, zeta; 91/100 beta; 94/100 epsilon
(`out/extension-stdout.txt`, `distinct_transforms_per_fixture_over_100_seeds`).

Seed sensitivity exists **only** for `record-order-replay`, and only through one coincidence. `permute()`
(`mini-counter.py:57-76`) splits the whole 488-byte tail on NUL, so the 475 padding NULs are shuffled as
empty strings; the single beta name therefore lands at pool byte offset `k ∈ 0..475`, and the reader
(`readers/record_order_replay.py`) maps `name_off = k` through its memorized `NAMES` list when `k < 8`.
`NAMES[3] == "libcrypto.so.3"` = beta's only name ⇒ beta matches **iff k = 3**, probability ≈ 1/476.
Independent re-derivation over seeds 0–99: `k = 3` at **seed 88 only**, and only beta is ever emitted as a
match (`out/bounds.json` → `record_order_per_seed`, `record_order_argmax_seeds = ["88"]`).
`epsilon` (the other single-name fixture) can never match: `ld-linux-x86-64.so.2` is absent from `NAMES`.

## 6. Positive control under the same seeds (the target stays reachable)

`…/positive.py` = the same harness with `CLASSES = [("structural-honest", "structural.py")]`:

```
/usr/bin/python3 positive.py > out/positive-stdout.txt 2> out/positive-stderr.txt   # exit 0
```
start `2026-10-25T07:20:09Z`, `wall_ms=3295`, 100/100 runs `matched=8`, `met_target=true`, exit 0,
`seeds_below_target=[]` (`out/results-structural.summary.json`, `out/results-structural.jsonl`).
So the 8-target is not vacuous at any of the 100 seeds — the permutation preserves decodable content.

## 7. Class ceilings derived independently, and a 1000-seed extension

`…/bounds.py` (exit 0, `2026-10-25T07:20:1x Z`, `out/bounds.json`) re-derives each class's emission from
first principles against `expected.json`:

* all same size (8 × 512) ⇒ `size-keyed` emits alpha's template for every fixture ⇒ ceiling **1** (alpha), seed-invariant.
* `string-scan` emits only `flags=0, value=0` records; `fixtures_all_zero_flat = []` (gamma carries `flags=2`/value 2912, theta carries 0x0B03) ⇒ ceiling **0**.
* `fixed-slice` emits `flags=0, value ∈ {64,96,…,480}`; every expected value is 0, 2819, 2912 or a payload constant ⇒ `fixed_slice_possible_fixtures = []` ⇒ ceiling **0**.
* `digest-keyed` template is alpha's first record only; no 1-record expected list equals it ⇒ ceiling **0** (plus the 8-hex-digit prefix was never hit in 800 permutations).
* `label-memorization` keys on basenames; the counter writes `opaque-<sha256[:20]>.data` ⇒ ceiling **0**.
* `record-order-replay`: two in-range offsets must differ by < 8 bytes, but every pool name is ≥ 10 chars + NUL, so any multi-name fixture must drop records and fall short of its expected length; epsilon's name is not in `NAMES`; beta matches iff `NAMES[3]` ⇒ **ceiling 1**, seed-dependent. Matches the measured `record_order_bounds` block.

**Extension** (`…/extension.py`, exit 0, start `2026-10-25T07:20:21Z`, 900-run leg `wall_ms=31038`, end
`07:20:53Z` per `out/extension-summary.json` mtime):
`record-order-replay` over seeds 100–999 → the only match in 900 runs is **seed 410 / beta.mrec**;
`distinct_matched=[0,1]`, `any_reaches_target=false` (`out/results-record-order-100-999.jsonl`,
`out/extension-summary.json`). Combined 1000 seeds for that class: 2 hits, max 1 — the 1/476 coincidence rate
predicted in §5 (0.2 % observed). Extrapolating those bounds to arbitrary seeds, no registered class can
reach 8 at *any* seed; 8 is above every class's structural ceiling.

**Falsification verdict on H: NOT FALSIFIED.** Max matched over 700 assigned runs = 1
(`size-keyed` at every seed, `record-order-replay` at seed 88); target 8 is unreachable by every registered
class on both the empirical and the analytic bound. The gate's default-seed verdict is therefore
seed-robust for the registered seven.

## 8. Adjacent finding (out of assignment, advisory): the green surface is reachable by an unregistered class

Running the same pinned counter and gate, the perturbation is **narrower than the predicate implies**:
`permute()` changes only `name_off` values; count, record order, `flags`, `value` and total size are fixed.
A memorized-answer reader keyed on `(count, tuple(flags,value) sequence)` therefore survives every seed
without ever reading a name.

Probe reader (scratch only, never in the lane): `…/LabratSeedSensitivity/payload_keyed.py` — parses the
header and record array, then answers from a hardcoded table; it never touches the name pool.

```
cd kaidoku-shokunin && for s in 0 17 88 410 999; do
  /usr/bin/python3 -I -B tools/round-34/mini-fix/mini-counter.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --control-reader /fast/scratch/hyaku/kaidoku-r34b/w1/LabratSeedSensitivity/payload_keyed.py --seed "$s"; done
```
→ 5/5 runs exit **0**, `matched=8`, `met_target=true`, `finding=records_match`
(`2026-10-25T07:21:50Z`; full stdout in the transcript of that cell).

Decisive name-blindness check (`…/out/pool-erasure.json`, `2026-10-25T07:22:16Z`): with the entire name
region of each fixture overwritten by NUL (`data[names_off:] = 0`), `payload_keyed.py` still reproduces
**8/8** expected record lists while `structural.py` reproduces **0/8** (`payload_keyed_matches=8`,
`structural_matches=0`).

Gate behaviour with that class registered (config copied to scratch, no lane mutation):

```
cd kaidoku-shokunin && /usr/bin/python3 -I -B tools/round-34/replay-gate.py --root . \
  --config /fast/scratch/hyaku/kaidoku-r34b/w1/LabratSeedSensitivity/out/gate-config-mini-plus-payload.json
# exit 2 -> REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_over_target=payload-keyed-probe   (2026-10-25T07:22:22Z)
```
and the frozen config at its default seed reproduces the claim's green row
(`REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-`,
exit 0, `2026-10-25T07:22:15Z`, `out/gate-default-seed.txt`).

Interpretation: the gate **mechanism** discriminates correctly; its frozen **class set** is incomplete for
the name-blind memorization family that the predicate sentence names
("only record-array traversal associates a name with its record", `mini-counter.py:8-10`, `claims.json`
`predicate_identity`). This is not a defect of the seed and not a break of the frozen literal target
("every *registered* shortcut class stays below target" still holds), but it means R34-C2's evidence does
**not** generalize to "no structure-blind shortcut passes". The frozen pins and the kill rule forbid
changing the predicate or dropping/adding classes this round; no lane edit is proposed by me.

Draft for the L1 (advisory, not applied): record in the claim's residual-risk text that the counter
perturbs only `name_off`, so a payload-keyed memorization reader reaches the green target at every seed with
the name pool erased (evidence above), and that a future freeze should register that class (the gate accepts
it unchanged: `REPLAY_GATE_REFUSED` demonstrated above).

## 9. Instrument observations (no action taken)

1. `permute()`'s docstring says "Reorder the name pool"; it actually shuffles NUL **padding** as empty
   strings, so names are relocated across the whole 488-byte tail and `name_off` becomes ~uniform over
   0..475 instead of small pool offsets. Harmless for structural decoding (100/100 seeds 8/8) but it is
   what creates the 1/476 `record-order-replay` coincidence at seeds 88 and 410.
2. `label_keyed.py` is pinned in `claims.json` but absent from `gate-config-mini.json` `shortcuts[]`; the
   gate never scores it. Paid: one run at `2026-10-25T07:21:58Z`, exit 1, `matched=0` — dead weight in the
   pin set, not in the gate.
3. The gate passes no `--seed`, so the frozen verdict rests on the single default seed
   `kaidoku-r34-mini-v1`; §4/§7 show that seed is not load-bearing for any registered class.

## 10. Budget, commands, exit codes, UTC

| step | command (cwd as noted) | exit | UTC |
|---|---|---|---|
| instrument hashes | `sha256sum` over the 26 pins, cwd=scratch | 0 | 07:18:42 |
| calibration run | `mini-counter.py … --seed 0` (size-keyed) | 1 (expected) | 07:18:45 |
| 700-run sweep | `/usr/bin/python3 sweep.py` (700 counter invocations, 4 threads) | 0 | 07:18:54 → 07:19:18 |
| positive control | `/usr/bin/python3 positive.py` (100 structural runs) | 0 | 07:20:09 → 07:20:13 (`results-structural.summary.json` mtime 07:20:13Z) |
| bounds analysis | `/usr/bin/python3 bounds.py` | 0 | 07:20:09 (`out/bounds.json` mtime 07:20:09Z) |
| 900-seed extension | `/usr/bin/python3 extension.py` | 0 | 07:20:21 → 07:20:53 (`out/extension-summary.json` mtime) |
| gate, frozen config | `replay-gate.py --root . --config tools/round-34/gate-config-mini.json` | 0 (`REPLAY_GATE_CLEAN`) | 07:22:15 |
| gate + payload class | same, scratch config | 2 (`REPLAY_GATE_REFUSED`) | 07:22:22 |
| pool erasure | inline python, scratch | 0 | 07:22:16 |

Total probe window ≈ 4 min (07:18:42 → 07:22:22), inside the 10-minute cap. No build, lint or test suite was
run; no ELF carrier, fixture or reader was executed as a program of interest (fixtures are static bytes read
by Python readers; readers ran only under `/usr/bin/python3 -I -B`). No lane VCS command, no lane file
written besides this report.

## 11. Verdict

**H holds and is not falsified**: over 100 distinct seeds × the seven registered classes (700 runs, plus a
900-seed extension on the only seed-sensitive class), the maximum green-surface match for any registered
shortcut is **1 of 8** — `size-keyed` at every seed via the alpha template, `record-order-replay` at seed 88
only — with the honest structural positive control at 8/8 on all 100 seeds; no registered class reaches the
target and no seed flips the gate. **Adjacent, advisory:** the same green surface is reached 8/8 at every
seed by a name-blind payload-keyed memorization reader (unregistered, demonstrated with the name pool
erased), so R34-C2's literal registered-class target stands but its "only record-array traversal associates
a name with its record" generalization is falsified; the gate refuses that class the moment it is registered.
