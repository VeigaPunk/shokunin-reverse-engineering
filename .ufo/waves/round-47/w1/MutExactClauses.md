# MutExactClauses — clause-deletion probe on `tools/round-47/exact.py` (R47-C1)

Seat `MutExactClauses`, round 47 wave 1, mutation-tester role. Read-only on the lane: every
mutant is a *scratch copy*. No install, no `pacman`, no new tool.

Instrument under test: `tools/round-47/exact.py`, sha256
`01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5` at lane HEAD
`31b092d17e77f5064c919383a9bc1e6cbfd2d1ff`. The file did **not** change during the probe
(lane hash before == after, see §7). HEAD advanced twice mid-wave (A5/A6, then the pin
follow-through); the probe was rebuilt from the newest bytes and every number below is
measured on `01a4bca7`, not on the pre-A6 `dcef54f1`.

## 1. What was measured

Seventeen behaviour-bearing checks inside `score()` — the nine predicate clauses of
`plans/round-47-claims.md` R47-C1, resolved into the independent checks the code actually
contains — were deleted one at a time from a scratch copy, and three detectors
were run on every variant:

- **D1 selftest** — `python3 -I -B <variant>/tools/round-47/exact.py --root <variant>
  --freeze selftest --rev selftest --selftest` (16 cases; pristine: exit 0, 0 failures,
  stdout sha256 `0249b80f58085f0d…`). A case "goes red" when its `ok` flips True→False.
- **D2 battery** — the variant's own `run_battery()` over the synthetic block-24 fixture
  (4 forgeries). A forgery "goes red" when its `v3_exit` flips 1→0 (the forgery survives).
- **D3 probes** — 23 artefact-level fixtures, each tripping one clause, scored with
  `battery=None`. Needed because D1/D2 leave part of the code unexercised; a probe flipping
  1→0 is the only evidence a deletion was noticed at all.

Command (harness runs all 29 variants, ~13 s):

```sh
cd /fast/scratch/hyaku/kaidoku-r47/MutExactClauses && \
HYAKU_SCRATCH=$PWD/tmp TMPDIR=$PWD/tmp python3 -I -B harness.py
```

Receipts: `.ufo/waves/round-47/w1/MutExactClauses/receipts/{results.json,harness.py,harness.log}`.

## 2. Baseline (pristine copy, no deletion)

- selftest: exit 0, `cases=16 failures=0`.
- battery: `forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0`.
- real counter at the tip, `--freeze <tip> --rev <tip>`: **exit 0**, `failing []`, `refs 9`,
  both pins match — measured at `31b092d1` (`receipts/base-tip-battery.json`, stdout sha256
  `918a12a8…`) and re-measured at the later tip `f7d6e58d` with `SKILL.md` byte-identical
  (`894e2864…`): exit 0 again, same battery (`receipts/base-tip-battery-2.json`, stdout
  sha256 `1fae3f70…`).

A baseline failure would have made every mutant inconclusive; there is none.

## 3. Mutation table

`st` = selftest exit on the variant. "newly red" = cases/forgeries/probes that changed
relative to pristine. Clause numbers are the R47-C1 predicate's.

| # | deleted clause (mutant) | exact.py sha256[:12] | st | selftest cases newly red | battery v3_green | probes newly green | verdict |
|---|---|---|---|---|---|---|---|
| C1 | 1a marker-uniqueness + 1b block-is-last + 1c `24. ` title | `e3548321a904` | 1 | `red-title-unnumbered`, `red-two-markers` | 0 | `1b-block-is-last`, `1c-title-24`, `1-stray-marker` | **killed** (D1) |
| C2 | 2 header cells exact | `a2678eb2c395` | 1 | `red-header-inexact` | 0 | `2-header` | **killed** (D1) |
| C3 | 3a row count + 3b four cells + 3c exit cell | `d7add85f7ab7` | **0** | — | 0 | `3b-row-cells`, `3c-exit-cell` | **survived** D1+D2; killed by D3 only |
| C4 | 4 v3 routed-id cardinality | `46c8b8336a12` | **0** | — | 0 | `4-multi-id-row` | **survived** D1+D2; killed by D3 only |
| C5 | 5 exact arm token | `c8a3648ff1d6` | 1 | `battery-discriminates`, `red-arm-substring`, `red-battery-green-forgery` | **1** (`substring-arm` survives) | `5-arm-token` | **killed** (D1+D2) |
| C6 | 6a digest pin + 6b mutation names | `18307d8416dd` | 1 | `battery-discriminates`, `red-digest-stale` | **1** (`stale-mutations-digest` survives) | `6a-digest-pin`, `6b-mutation-names` | **killed** (D1+D2) |
| C7 | 7 flag-order literal | `47b50e57259e` | 1 | `battery-discriminates`, `red-flag-order-swapped` | **1** (`flag-order-drift` survives) | `7-flag-order` | **killed** (D1+D2) |
| C8 | 8a refs≥3 + 8b resolve + 8c must-cite + 8d interpreter pin | `26674b885bae` | 1 | `red-pin-mismatch`, `red-ref-no-selector`, `red-ref-outside-allowlist` | 0 | `8a-floor-1real`, `8a-floor-2real-noself`, `8b-refs-resolve`, `8c-must-cite`, `8d-interpreter-pin` | **killed** (D1) |
| C9 | 9 battery thresholds | `b8f7b19527d2` | **0** | — | 0 | `9-battery-thresholds` | **survived** D1+D2; killed by D3 only |

Sub-clause resolution (same detectors, one check each):

| sub-mutant | st | selftest cases newly red | probes newly green | verdict |
|---|---|---|---|---|
| 1a marker-uniqueness | 1 | `red-two-markers` | — (`red-marker-missing` survives D1 already; v2 `if not marked` masks it) | killed |
| 1b block-is-last | **0** | — | `1b-block-is-last` | survived D1+D2 |
| 1c `24. ` title | 1 | `red-title-unnumbered` | `1c-title-24` | killed |
| 2 header | 1 | `red-header-inexact` | `2-header` | killed |
| 3a rows==4 | **0** | — | **none — undeletable by any artefact** | **dead weight** (implied by clause 4) |
| 3b four cells | **0** | — | `3b-row-cells` | survived D1+D2 |
| 3c exit cell ∈{0,1,2} | **0** | — | `3c-exit-cell` | survived D1+D2 |
| 4 v3 cardinality | **0** | — | `4-multi-id-row` | survived D1+D2 |
| 4 both profiles (v3+v2 id checks) | 1 | `red-duplicate-routed-id` | `4-multi-id-row`, `4-routed-ids` | killed |
| 5 arm token | 1 | 3 cases | `5-arm-token` | killed |
| 6a digest pin | 1 | `battery-discriminates`, `red-digest-stale` | `6a-digest-pin` | killed |
| 6b mutation names | **0** | — | `6b-mutation-names` | survived D1+D2 |
| 7 flag order | 1 | `battery-discriminates`, `red-flag-order-swapped` | `7-flag-order` | killed |
| 8a refs≥3 | **0** | — | `8a-floor-1real`, `8a-floor-2real-noself` | survived D1+D2 |
| 8b refs resolve/allowlist | 1 | `red-ref-no-selector`, `red-ref-outside-allowlist` | `8b-refs-resolve` | killed |
| 8c must-cite round-46.md | **0** | — | `8c-must-cite` | survived D1+D2 |
| 8d interpreter pin | 1 | `red-pin-mismatch` | `8d-interpreter-pin` | killed |
| 9 battery thresholds | **0** | — | `9-battery-thresholds` | survived D1+D2 |
| 3a+4 removed together | 1 | `battery-discriminates`, `red-duplicate-routed-id`, `red-rows-not-four` | `3a-rows-count`, `4-multi-id-row`, `4-routed-ids` | killed (only as a pair) |

**Nine of seventeen checks and three of nine clauses can be deleted with the shipped
detectors still green.** None of them is a broken mutant: each variant parses, imports,
runs, and its selftest exits 0 with `failures=0`.

## 4. Findings

### F1 (highest value) — the battery's `once` forgery does not test the `once` arm

`duplicate-routed-id` inserts a **fifth** row. At the tip the forgery is killed by clause 3
first, and only then by clause 4:

```
duplicate-routed-id  v2 0  v3 1  ['rows 5 != 4',
  "routed cardinality {'R46-CL2': 2, 'R46-CL3': 1, 'R46-CL4': 1, 'R46-CL6': 1} != each of [...] exactly once"]
```

Delete clause 4's cardinality arm (mutant `46c8b8336a12`): the battery still reports
`v3_green 0`, `forgeries_total 4`, and the selftest still exits 0. **The `once` arm of block
24 is defended by no red case at all** — `red-duplicate-routed-id` uses the same 5-row shape,
which the retained at-least-once check also kills.

The only shape that isolates the arm is a 4-row table where all four ids appear once and one
row names two of them. Measured on the pristine counter:

```python
rows = [("R46-CL2 R46-CL3", "...", "symbol", "1"), G[2], G[3], ("R46-CL2", "...", "once", "1")]
# pristine: exit 1  ['rows naming != 1 routed id: [0]',
#                    "routed cardinality {'R46-CL2': 2, ...} != each of [...] exactly once"]
# mutant C4: exit 0  (survivor)
```

Fix (L1's call, not mine — the bytes are frozen): make the `duplicate-routed-id` forgery that
4-row shape, or add it as a fifth forgery; a one-row-per-id 5-row insertion must not be
allowed to stand in for the cardinality arm.

### F2 — clause 3a (`rows != 4`) is dead weight

No artefact rejects under clause 3a that is not already rejected by clause 4's four checks:
with fewer than 4 rows an id is missing (v2 arm fires), with more than 4 rows an id repeats
or a row names none (`multi`/`counts` fire). Measured: `3a` mutant → selftest 0 failures,
battery unchanged, and the targeted `3a-rows-count` probe is *still* exit 1 (clause 4 catches
it). Removing 3a together with all routed-id checks is the first time the 3-row fixture
passes (`3a+4-removed` → `3a-rows-count` exit 0). Clause 3's 3b/3c are load-bearing but
likewise have no red case.

### F3 — clause 8's `refs >= 3` floor is satisfied by the block's own self-reference

`HARD_REF` matches the block's `` `tools/round-47/exact.py` `` mention, and `check_refs`
exempts that path from the line-selector rule. Measured on the pristine counter:

| block's Refs line | `refs` | exit |
|---|---|---|
| one citation (`round-46.md:10-30`) | 2 | 1 `refs 2 < 3` |
| **two** citations (`round-46.md:10-30`, `round-47-claims.md:20`) | **3** | **0** |
| the same two, self mention stripped | 2 | 1 `refs 2 < 3` |
| **two** ranges on the **same** path | **3** | **0** |

So two selected citations pass, and the count is an occurrence count, not a count of
distinct citations. The claims' landed-surface prose says "at least three citations carry a
line selector"; the code's floor is three *matches* + self, which is 2. Deleting 8a is
invisible to D1/D2 (`red-ref-no-selector` survives because the selector rule, not the floor,
kills it). Fixture: `probes["8a-floor-2real"]`, `["8a-floor-2same"]`.

### F4 — clause 9's thresholds are the only artefact-level use of the battery, and nothing tests them

`battery-discriminates` computes its own `ok` from the aggregate dict instead of scoring an
artefact through `score(..., battery=...)`, so it cannot see clause 9 at all. Deleting clause
9 → selftest exit 0, `failures=0`, battery identical. A counter with no threshold clause
would still print `met_target` on an artefact whose battery showed `v3_green 1` — measured
directly by passing `{"forgeries_total":4,"v2_green":4,"v3_green":1,"genuine_green":1,"crash":0}`
to `score()`: pristine exit 1, mutant exit 0. That is the single most dangerous survivor,
because it silently removes the check that turns a surviving forgery into a red verdict.

### F5 — clause 1 counts the marker over the whole document (over-strict, not vacuous)

A correct block plus one later prose line quoting `<!-- exactness-table v3 -->` gives
`marker_occurrences 2 != 1`, exit 1 (`probe 1-stray-marker`). `blocks_of()` scopes the marked
block to the craft section but `skill.count(MARKER)` does not. Harmless for this landing
(block 24 is the only mention) but a trap for any future prose that quotes the marker.

### F6 — `6b` (mutation names), `8c` (must-cite) and `1b` (block-is-last) are live but unguarded

Each flips exactly one purpose-built probe and no selftest case (`probe 6b-mutation-names`
→ `mutation names not stated in the block: ['stale-mutations-digest']`; `8c` → cites
`round-45.md` only; `1b` → `marker block is not the last craft block`). A one-line case per
check would close them.

## 5. Calibration — the freeze series does not survive as declared

R47-C1's counting command takes `--freeze <FREEZE> --rev <REV>`. Measured at
rev `31b092d1` (`receipts/freeze-*.json`):

| FREEZE | exit | reason |
|---|---|---|
| `5017e1f7` (first freeze) | **2** | `frozen_path_changed`: `plans/round-47-claims.md`, `tools/round-47/`, `…/exact.py`, `…/record.py` |
| `62e33f7d` (A2, the second declared freeze) | **2** | `frozen_path_changed`: `tools/round-47/`, `…/exact.py`, `…/record.py` |
| `31b092d1` (= rev) | 0 | clean |
| `f7d6e58d` (= the later rev), re-run | 0 | clean |

The claims file declares the freeze as "a series of two" (A1, A2). A3–A6 and the A6
pin follow-through all touched frozen bytes, so **neither declared freeze scores at the
tip**, and the only admissible freeze is the measured revision itself — the freeze is a
measurement-time constant, not a pinned commit. This is not a mutant of mine and I did not
touch frozen bytes; it is a receipt L1 must reconcile before the landing is scored.

## 6. What the claim does and does not hold

At `01a4bca7` the instrument does what the predicate says: exit 0 at
`--freeze 31b092d1 --rev 31b092d1`, all nine clauses pass, `refs 9`, both pins match, and the
battery measures the four holes at `v2_green 4 / v3_green 0`. The claim is **met as written**.
The defect is in the *guard*, not the verdict: three of the nine clauses (and nine of the
seventeen checks) can be deleted with `--selftest` exiting 0 and the battery unchanged, so a
later edit that quietly drops the `once` arm, the exit-cell arm or the battery thresholds
would keep both instruments green. A surviving mutant is a coverage finding, not permission
to change the contract — I changed no lane bytes.

## 7. Restoration evidence

- Originals are never written. `results.json._meta` records
  `src_sha256 == src_sha256_after == 01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5`,
  and every variant lives under `/fast/scratch/hyaku/kaidoku-r47/MutExactClauses/v/<name>/`.
- Lane re-checked after the run: `sha256sum tools/round-47/exact.py` = `01a4bca7…`;
  `git status --porcelain -- tools/round-47 SKILL.md plans/round-47-claims.md` empty.
- Scratch removed after receipts were copied (§8). No `git` mutation was run anywhere; the
  fixture repos were created by `exact.py`'s own `_repo()` (`git -C <d> init`) under the
  seat scratch, and each asserts `rev-parse --show-toplevel == d`.

## 8. Receipts and tooling

`.ufo/waves/round-47/w1/MutExactClauses/receipts/`:

| file | sha256 |
|---|---|
| `results.json` (29 variants, all exits, all probe codes) | `7b215ba6f0b2…` |
| `harness.py` (the deletion edits, verbatim) | `d09b60a59972…` |
| `harness.log` (per-variant one-liners) | `49931b8fbc…` |
| `base-tip-battery.json` (pristine counter at `31b092d1`, exit 0) | `918a12a8f991…` |
| `base-tip-battery-2.json` (the same at `f7d6e58d`, exit 0) | `1fae3f701bdd…` |
| `freeze-A1freeze.json`, `freeze-A2freeze.json`, `freeze-tip.json` | `f55cd2fd…`, `688f7a8c…`, `3f351726…` |

No tool was installed (no `pacman` transaction, no `uv`/`npx`/binary). Python 3.14.8 stdlib
only.

## 9. Sources

- `plans/round-47-claims.md:45-113` (the R47-C1 predicate and its nine clauses, read in full).
- `tools/round-47/exact.py@01a4bca7` (`score()`, `MUTATIONS`, `check_refs`, `run_battery`,
  `selftest` — the whole file, not excerpts).
- `tools/round-46/gate.py:144-195` (`freeze_state`, the source of the F-calibration exits).
- `SKILL.md` block 24 at `31b092d1` (the landed artefact the battery is scored against).
