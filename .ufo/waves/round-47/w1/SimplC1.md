# SimplC1 — YAGNI pass on `tools/round-47/exact.py` (R47-C1)

Seat `SimplC1`, wave `round-47/w1`, lane `kaidoku-shokunin`. Leaf seat: no subagent
dispatch. **No lane file was edited**; every mutation below was applied to a copy under
`/fast/scratch/hyaku/kaidoku-r47/SimplC1` (removed after the receipts were copied here).
No installs were needed (`python3` 3.14 stdlib only; no pacman, no `uv`, no `npx`).

Measured revision: `09a9f912f4a639b91bce7dcd3711d8f391969d4f`.
Operative freeze: `f54b3b6de9085d3db449ed5d0916296cb29c1f6d` (see Y1 — **not** the
`5017e1f7…` in my prompt).

Method: for every check in the counter, cut exactly that check in a copy and re-run
(a) the module's own `--selftest` and (b) the real counter at the measured revision.
A cut that leaves both green is a check with **no failing case**; a cut that reddens one
of them is load-bearing. Plus a forgery matrix (`attack/probe.py`, `attack/probe2.py`)
that feeds blocks designed to pass while violating a stated clause.

---

## 0. Verdict

* At the operative freeze the artefact is **green**: counter exit 0, `failing []`,
  battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`,
  selftest `cases=16 failures=0` (`receipts/R2-counter-freeze-f54b3b6d.out`,
  `receipts/R4-selftest-with-args.out`). Receipt values: `rule_blocks 24`,
  `marker_occurrences 1`, `rows 4`, `refs 9`, `gate_order_literal 1 / reversed 0`,
  `interpreter_sha256 == expected == 01a4bca7…bcd5`, `mutations_sha256 19a2166e…a112`.
* The counter is **not** decoration: 11 of the 25 clause checks are load-bearing against
  an existing case, and 4 more are load-bearing only through the battery. But **9 checks
  have no failing case at all**, and **3 of those 9 are also falsifiable by a forgery that
  scores green** (Y2, Y3, Y5).
* The two most valuable findings are Y1 (the freeze the prompt names cannot run the
  counter) and Y3 (the battery's `forgeries_total == 4` counts loop iterations, so a
  battery that forges nothing still scores `v2_green 4 / v3_green 0`).

---

## 1. Findings (falsifications first)

### Y1 — the prompt's freeze makes the counter exit 2, and `exact.py` changed after the freeze with no amendment paragraph

```sh
python3 -I -B tools/round-47/exact.py --root $PWD \
  --freeze 5017e1f7299c3a812e87e7950148f54313dd279e --rev HEAD
```
→ **exit 2**, `reason frozen_path_changed`,
`frozen_path_changed ["plans/round-47-claims.md", "tools/round-47/", "tools/round-47/exact.py", "tools/round-47/record.py"]`
(`receipts/R1-counter-freeze-5017.out`).

* `sha256(tools/round-47/exact.py @ 5017e1f7)` = `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`.
* `sha256(tools/round-47/exact.py @ f54b3b6d = HEAD)` = `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5`.
* `git log --format='%h %s' -- tools/round-47/exact.py` = `f54b3b6d A6 - the battery
  fixture carries every citation the landed block names` **on top of** the freeze commit.
* `plans/round-47-claims.md` discloses A1 and A2 only. There is **no A6 paragraph**:
  the claims file's last commit is `62e33f7d` (A2), and `f54b3b6d` touches only
  `tools/round-47/exact.py` (16 lines). The claims file's own rule — "Nothing in this
  file or in `tools/round-47/` changes after the freeze: a change makes both counters
  exit 2 `frozen_path_changed`" — is therefore **false of the landed tree** unless A6 is
  declared.
* A6 is load-bearing, not cosmetic: cutting its citation loop reddens the counter
  (`genuine_green 0`, `battery v2_green 0 != 4`) while the selftest stays 16/16
  (`receipts/R9-abl-mini.out`, `a6-fixture-citation-loop`). So the frozen bytes were
  wrong and the fix was necessary — but it is an **undisclosed third amendment**.
* Only one freeze satisfies the freeze arm for both counters: `f54b3b6d`
  (`git merge-base --is-ancestor 07d2894e f54b3b6d` → yes; at `f54b3b6d` the counter
  exits 0, `restored []`). `07d2894e` as freeze still reddens with
  `frozen_path_changed ["tools/round-47/", "tools/round-47/exact.py"]`.

**Action for L1 (no frozen edit by me):** declare A6 in the claims file as a disclosed
amendment, state the declared freeze as `f54b3b6d` (or whatever commit carries the A6
paragraph), and quote the counting command with that hash. Otherwise the R47-C1 target is
unreachable by the command the claims file itself prints.

### Y2 — clause 8 is weaker than its claim text: `refs >= 3` counts SELF mentions, and a block with **one** line-selected citation passes

Claims clause 8: "`refs >= 3`, every reference carries a line selector …". Code:
`receipt["refs"] = len(HARD_REF.findall(block))` counts *every* mention including the
`tools/round-47/exact.py` mention that the interpreter pin already requires, and
`check_refs` exempts SELF from the selector rule (`if name == SELF: continue`).

Forgery (`attack/probe.py`, case `refs-padded-with-self-mentions`): the genuine block with
`Refs:` reduced to `` `corpus/lessons/round-46.md:1-2`, `tools/round-47/exact.py` `` →
**exit 0**, `refs 3`, `cited` = {round-46.md, exact.py}: exactly **one** citation carries
a line selector. `one-selector-only` (same block, SELF mention removed) → exit 1
`refs 2 < 3`. So the only thing enforcing three selectors is a count that SELF inflates.

`receipts/R5-probe.out`. Minimal fix for a future counter: count selector-carrying,
non-SELF matches (`sum(1 for name, first, _, in HARD_REF.findall(block) if first and name != SELF)`)
and add the case above as `red-refs-count-padded` (expect 1). **Verified red today**
(`red-refs-count-padded` is not in the selftest; the probe shows the current code green).

### Y3 — clause 9's denominator counts loop iterations: a battery whose mutations forge **nothing** still scores `forgeries_total 4 / v2_green 4 / v3_green 0 / crash 0`

`run_battery`'s no-op branch books a dead mutation as a *successful v2 forgery*:

```python
if text == block and not overrides:
    out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
    out["forgeries_total"] += 1
    out["v2_green"] += 1          # <-- a forgery that forged nothing scores green
    continue
```

Ablations (`receipts/R6-ablate2.out`):
* `mutation-substring-is-noop` (one identity mutation) → counter **met True**, battery
  `4/4/0/1/0`, `noop_fixtures ["substring-arm"]`.
* `all-mutations-noop` (all four identity) → counter **met True**, battery `4/4/0/1/0`,
  `noop_fixtures` = all four. **Zero forgeries executed, clause 9 green.**

The only trace is the per-fixture `"error": "mutation was a no-op"` string, which no clause
reads. This is R46-CL4 (an unpinned denominator) re-entering through the battery: the name
digest pins *which* mutations exist, not that they mutate.

Fix proven on a copy (`receipts/R7-ablate3.out`): replace `out["v2_green"] += 1` in that
branch with `out["crash"] += 1` → baseline stays green (`noop-counts-as-crash`, met True),
all-noop reddens (`v2_green 0 != 4`, `crash 4 != 0`). One line, no other clause touched.
Case to add: `battery-noop-mutation` (a MUTATIONS list with an identity entry must exit 1).

### Y4 — the `duplicate-routed-id` forgery is killed by the row count, not by the `once` arm; and a single-defect, v2-green version of it is **impossible**

Shipped forgery inserts a fifth row (`rows.insert(2, …)`), so its v3 kill is
`rows 5 != 4` **and** the cardinality message (`receipts/R2…out` battery fixture 2).
Consequences:

* Cutting clause 4 entirely leaves the counter **met True** (`c4-v3-cardinality` in
  `receipts/R6-ablate2.out`): the battery cannot tell that the `once` arm is gone.
* Making the forgery single-defect (`rows[1] = ["R46-CL2", …]`, 4 rows) makes it
  **v2-red** (`v2_exit 1`), because v2's at-least-once check then misses `R46-CL3`
  (`dup-forgery-4row` in `receipts/R7-ablate3.out`, `v2_green 3`). In a four-row table the
  only id multiset that keeps every id present is "each exactly once", so a duplicate-id
  forgery that stays v2-green **must** add a row. The `once` arm therefore has **no
  attributable battery evidence**, by construction.
* The only attributable evidence for clause 4 is the selftest case
  `red-duplicate-routed-id` (4 rows, asserts red, no v2 requirement) — and that case does
  fail when clause 4 is cut (`failed=['red-duplicate-routed-id']`).

Verdict: **keep** clause 4; state in the report that its battery attribution is
co-located with clause 3, and that the selftest case is the real evidence. Do not change
the frozen forgery.

### Y5 — pin multiplicity is unchecked: a block carrying a correct pin *and* a wrong one passes

`MUT_PIN.search` / `SELF_PIN.search` take the **first** match only.
`second-pin-conflicts` (genuine block + `mutations_sha256:` + 64 zeros) → **exit 0**;
`second-interpreter-pin-conflicts` → **exit 0** (`receipts/R5-probe.out`). A block can
therefore "carry" a pin equal to the digest while also carrying a contradictory one.
Fix: assert `len(MUT_PIN.findall(block)) == 1` (and same for SELF_PIN); case
`red-second-pin` (expect 1).

### Y6 — `--selftest` is not runnable as documented: it exits 2 unless three unused arguments are supplied

```sh
python3 -I -B tools/round-47/exact.py --selftest      # exit 2
exact.py: error: the following arguments are required: --root, --freeze, --rev
```
(`receipts/R3-selftest-standalone.out`; with the three dummies: exit 0, 16/16,
`receipts/R4-selftest-with-args.out`.) `main()` handles `--selftest` before evaluating,
but `argparse` marks the three as `required=True`. Any receipt that quotes
`--selftest` alone is quoting a usage error, not a run. Fix: `required=False` on the three
(or default `--root .`), keep the 16 cases.

### Y7 — two receipt fields do not mean what they say

* `rev` is echoed, not resolved: the receipt of a run with `--rev HEAD` prints
  `"rev": "HEAD"` (`receipts/R2-counter-freeze-f54b3b6d.out`), although
  `fs["rev"]` holds the resolved SHA. `evaluate` merges `freeze`, `frozen_derived`, … but
  not `fs["rev"]`. A receipt whose job is to pin the measured revision does not.
* `restored` is wrong: at `--freeze 5017e1f7 --rev HEAD` the receipt lists
  `restored ["tools/round-47/exact.py", "tools/round-47/record.py"]` while the same
  receipt lists both in `frozen_path_changed` and `git diff 5017e1f7 HEAD --
  tools/round-47/exact.py` is non-empty (15 insertions). `gate.freeze_state` compares
  *file* paths in `touched` against *directory* entries in `changed`
  (`tools/round-47/`), so every touched file under a changed directory is reported
  "restored". The bug is in `tools/round-46/gate.py` (frozen infra, outside this claim's
  surface), but `exact.py` prints it as evidence: a reader concludes the frozen bytes are
  identical when they are not. Recommendation: drop `restored` from the C1 receipt or fix
  gate.py in a round that owns it; add `fs["rev"]` to the merge.

### Y8 — three clause checks are provably subsumed (redundant, not wrong)

| cut | observed | proof |
|---|---|---|
| `rows != 4` (v3) | counter **and** selftest stay green | with each row naming exactly one routed id and the multiset equal to the four distinct ids (clause 4), the row count is necessarily 4; a 3-row block is caught by clause 4's multiset, a 5-row block by its pigeonhole duplicate |
| `len(marked) != 1` (v3) | green | `occurrences == 1` ∧ `len(marked) != 1` ⟹ `marked == []` ⟹ the earlier `if not marked: return 1` fires |
| `len(r) != 4` per row | green | `bad_exit` already flags `len(r) < 4`, and a 5-cell row is flagged by `len(r) != 4` only — the *cell-count* check is the one piece with no case; `red-row-three-cells` is red today via `bad_exit` (`receipts/R8-probe2.out`) |

Keep them for clause fidelity; they buy no kill, so a future counter may drop them without
losing a forgery. Not a hole.

### Y9 — the selftest cannot see its own fixture regressions (the A6 class)

Cutting the A6 citation loop reddens the counter but leaves the selftest **16/16**
(`receipts/R9-abl-mini.out`). The selftest builds fixture file maps that already contain
every citation, so it cannot detect that `_fixture_files` fails to carry one. Add
`battery-fixture-carries-citations`: a block citing a file outside the hardcoded base list
must still score `genuine_green 1`.

---

## 2. Keep / cut table

Legend — *cut*: the check was removed (replaced by `pass`/`True`) in a scratch copy;
*catching case*: the selftest case that reddens when the check is cut, or the case that
would have to be added. "red today" means the case was verified to score 1 with the
current bytes (`receipts/R8-probe2.out`), so only its absence from the selftest is the gap.

### 2.1 Clause checks inside `score()`

| # | surface | claim clause | cut observed | catching case | verdict |
|---|---|---|---|---|---|
| 1 | `occurrences != 1` | cl.1 | selftest red | `red-two-markers` | **keep** |
| 2 | `len(marked) != 1` (v3) | cl.1 | nothing | — (subsumed, Y8) | keep for fidelity; redundant |
| 3 | `block_is_last` | cl.1 | nothing | **missing** — `red-block-not-last` (red today) | **keep + add case** |
| 4 | `block.startswith("24. ")` | cl.1 | selftest red | `red-title-unnumbered` | **keep** |
| 5 | `header == HEADER` (v3) | cl.2 | selftest red | `red-header-inexact` | **keep** |
| 6 | header substring test (v2) | v2 port | nothing (`v2-header-strict` still 4/4) | — | **cut-able** (no forgery depends on it) |
| 7 | `rows != 4` (v3) | cl.3 | nothing | — (subsumed by cl.4, Y8) | keep for fidelity; redundant |
| 8 | `len(r) != 4` | cl.3 | nothing | **missing** — `red-row-three-cells` (red today via `bad_exit`) | **keep + add case** |
| 9 | `bad_exit` ∈ {0,1,2} | cl.3 | nothing | **missing** — `red-exit-outside` (red today) | **keep + add case** |
| 10 | routed-id cardinality (v3) | cl.4 | selftest red, counter still green | `red-duplicate-routed-id` | **keep** (battery cannot attribute — Y4) |
| 11 | routed-id "some row" (v2) | v2 port | nothing | — | **cut-able** (documentation of the R46-CL3 hole only) |
| 12 | arm token equality (v3) | cl.5 | selftest **and** counter red (`v3_green 1`) | `red-arm-substring`, `red-battery-green-forgery`, `battery-discriminates` | **keep — most load-bearing check in the file** |
| 13 | arm substring (v2) | v2 port | counter red (`v2_green 3`) | `battery-discriminates` | **keep** |
| 14 | `mutations_sha256 == MUT_DIGEST` | cl.6 | selftest + counter red | `red-digest-stale` | **keep** |
| 15 | four mutation names stated | cl.6 | nothing | **missing** — `red-names-absent` (red today) | **keep + add case** |
| 16 | flag order in `gate.py` | cl.7 | selftest + counter red | `red-flag-order-swapped` | **keep** |
| 17 | `refs >= 3` | cl.8 | nothing, **and falsifiable** (Y2) | **missing** — `red-refs-count-padded` (green today ⇒ currently a hole) | **keep, fix the count** |
| 18 | SELF exempt from selector | cl.8 carve-out | selftest `green` breaks | `green` | keep (but it is Y2's mechanism) |
| 19 | every ref carries a selector | cl.8 | selftest red | `red-ref-no-selector` | **keep** |
| 20 | path allowlist | cl.8 | nothing (dangling check covers the test's path) | **missing** — case with `corpus/QUALITY.md:3` *present* in the fixture | keep; pairwise-redundant with 21 |
| 21 | citation absent at rev | cl.8 | nothing (allowlist covers the test's path) | **missing** — `red-ref-absent-at-rev` (red today) | keep; pairwise-redundant with 20 |
| 22 | range `1 <= a <= b <= n` | cl.8 | nothing | **missing** — `red-ref-range-inverted` (red today) | **keep + add case** |
| 23 | must-cite `round-46.md` | cl.8 | nothing | **missing** — `red-must-cite-absent` (red today) | **keep + add case** |
| 24 | `interpreter_sha256 == bytes at rev` | cl.8 | selftest red | `red-pin-mismatch` | **keep** |
| 25 | battery counters `4/4/0/1/0` | cl.9 | nothing | **missing** — `red-battery-counts` (red today) | **keep + add case** |

### 2.2 Battery machinery (`MUTATIONS`, `run_battery`, fixtures)

| surface | clause | evidence | verdict |
|---|---|---|---|
| `_m_substring_arm` | cl.9 `substring-arm` | the only forgery whose v3 kill is `arm cells not exact vocabulary tokens` | keep |
| `_m_duplicate_id` (`rows.insert`) | cl.9 `duplicate-routed-id` | two defects at once (Y4); single-defect version is v2-red | keep frozen; **document the non-attribution** |
| `_m_stale_digest` (`MUTATIONS[:3]`) | cl.9 `stale-mutations-digest` | produces a digest ≠ `MUT_DIGEST` | keep |
| `_m_flag_order` (`gate.py` copy) | cl.9 `flag-order-drift` | `0 correct, 1 reversed` | keep |
| `_table_span` + `rewrite_rows` | mutation plumbing | only caller of each other; two mutations need the table rewrite | keep |
| no-op branch `v2_green += 1` | cl.9 denominator | **all-noop battery scores green** (Y3) | **fix to `crash += 1`** (proven) |
| `_repo` toplevel assertion | fixture contract | matches the lane contract (`rev-parse --show-toplevel` == dir) | keep |
| `_fixture_files` hardcoded `corpus/lessons/round-45.md` | none | block 24 does not cite it; A6's loop already fetches citations; cutting it changes nothing (`R9`) | **cut** |
| `_fixture_files` A6 citation loop | cl.9 `genuine_green` | cutting it reddens the counter (`R9`) | **keep** — and declare it (Y1) |
| `out["mutations_sha256"] = MUT_DIGEST` | none | nothing reads it; already in the block and in `receipt.mutations_sha256_expected`; cutting it changes nothing (`R9`) | **cut** |
| `battery.get("crash")` counter | cl.9 | 0 in the genuine battery, so it only bites on a crash | keep |
| `evaluate` gating (`battery` only when `code == 0`) | cl.9 reachability | recorded by `controls/ctl-c1-2-freeze-battery-absent.json` (`battery.skipped`) | keep |

### 2.3 Parse helpers, constants, exit-2 path

| surface | clause | verdict |
|---|---|---|
| `craft_section` + `MALFORMED` + `Malformed` | cl.1, exit-2 contract | keep (`red-malformed-heading-is-exit-2`) |
| `blocks_of` (`^- \*\*` split) | cl.1 | keep |
| `table` / `_cells` / `_rows` | cl.2/cl.3 | keep (separator rows are skipped; an all-dash line in the body is not a row — verified `separator-line-in-body` exit 0, which is correct) |
| `line_count` | cl.8 | keep (sole caller `check_refs`) |
| `HEADER`, `ROUTED`, `VOCAB`, `ALLOW`, `MUST_CITE`, `ORDER`, `REVERSED`, `ID`, `HARD_REF`, `MUT_PIN`, `SELF_PIN`, `MARKER`, `CRAFT`, `SELF`, `CLAIMS`, `GATE46`, `MUT_DIGEST` | clauses 1–8 | keep, all read |
| `ID = r"R46-CL\d+"` on the trigger cell only | cl.4 | keep — an id named only in the v2-hole cell is ignored, which is what the claim says (`id-in-hole-cell-not-trigger` exit 0) |

### 2.4 CLI flags

| flag | consumer | verdict |
|---|---|---|
| `--root` | everything | keep |
| `--freeze` | `gate.freeze_state` (cl.9 of the freeze arm) | keep |
| `--rev` | `gate.show`, clause 8 resolution | keep; **record `fs["rev"]`** (Y7) |
| `--profile {v2,v3}` | v3 = the predicate; v2 = `controls/ctl-c1-1-v2-profile.json` and the battery's hole measurement | keep |
| `--no-battery` | consumed by `ctl-c1-1-v2-profile.json` (its receipt has no `battery` key) — note it makes that control blind to clause 9 | keep; state the blindness |
| `--selftest` | calibration | keep; **fix `required`** (Y6) |
| `--json-out` | every control and the landing receipt; refused inside graded surfaces by `gate.out_path` | keep |
| `main_guard` (gate) | exit-2-never-crash contract | keep |

### 2.5 Receipt fields

| field | read by | verdict |
|---|---|---|
| `rule_blocks`, `marker_occurrences`, `block_present`, `rows`, `header` | clauses 1–3 + human | keep |
| `block_is_last`, `block_title`, `header_ok` | clause 1/2 (read back through the receipt dict — a KeyError if removed, see `receipt-block-fields` ablation) | keep, but prefer locals |
| `routed_counts`, `arm_tokens` | diagnosis of clauses 4/5 | keep |
| `mutations_sha256` / `_expected`, `interpreter_sha256` / `_expected` | clause 6/8 diagnosis | keep |
| `gate_order_literal` / `gate_order_reversed` | clause 7 | keep |
| `refs`, `cited`, `unresolved_citations` | clause 8 | keep — but `refs` is the miscount in Y2 |
| `battery` | clause 9 | keep |
| `freeze`, `frozen_derived`, `frozen_path_changed`, `touched`, `dirty` | freeze arm | keep |
| `restored` | nobody | **cut or fix** (false at `5017e1f7..HEAD`, Y7) |
| `rev` | human | **fix** — currently echoes the argument (Y7) |

---

## 3. What I did **not** do

* No edit to `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, or the
  fleet repo; no git/jj mutation; no commit/stage/stash.
* No claim scored beyond R47-C1's instrument (R47-C2's `record.py` is another seat's
  surface); I only note that the *shared* freeze must be `f54b3b6d` for the C1 arm, which
  is also the newest commit touching `tools/round-47/`, so it is the earliest freeze that
  can be green for both counters.
* The prompt's freeze was **not** used for scoring, because it makes the counter exit 2;
  I measured at `f54b3b6d` and at the pinned rev `09a9f912`.

---

## 4. Receipts

All under `.ufo/waves/round-47/w1/SimplC1/`. Columns: name, exit, stdout sha256 (first 16),
UTC. Full stdout is `receipts/<name>.out`.

| name | exit | sha256[:16] | UTC |
|---|---|---|---|
| R1-counter-freeze-5017 | 2 | 3f16566aefc4c47b | 2026-10-28T18:04:29Z |
| R2-counter-freeze-f54b3b6d | 0 | 421031967d327b7b | 2026-10-28T18:04:29Z |
| R3-selftest-standalone | 2 | d7017b6eeacb82b8 | 2026-10-28T18:04:30Z |
| R4-selftest-with-args | 0 | 0249b80f58085f0d | 2026-10-28T18:04:30Z |
| R5-probe | 0 | 53f38c8d57ea3369 | 2026-10-28T18:04:30Z |
| R6-ablate2 (26 cuts) | 0 | 3d532fbbedb5ee9c | 2026-10-28T18:08:09Z |
| R7-ablate3 (8 targeted runs) | 0 | 3bea25a1b687a86c | 2026-10-28T18:08:12Z |
| R8-probe2 (8 candidate cases) | 0 | db2ad50ce7ec208a | 2026-10-28T18:12:06Z |
| R9-abl-mini (4 cuts) | 0 | d279e7cffcc32945 | 2026-10-28T18:13:43Z |

Commands (run from the lane root, `TMPDIR`/`HYAKU_SCRATCH` = the seat scratch):

```sh
python3 -I -B tools/round-47/exact.py --root $PWD --freeze 5017e1f7… --rev HEAD          # R1
python3 -I -B tools/round-47/exact.py --root $PWD --freeze f54b3b6d… --rev HEAD          # R2
python3 -I -B tools/round-47/exact.py --selftest                                         # R3
python3 -I -B tools/round-47/exact.py --root $PWD --freeze f54b3b6d… --rev HEAD --selftest # R4
python3 -I -B attack/probe.py  <scratch>/base/tools/round-47/exact.py                    # R5
python3 -I -B attack/probe2.py <scratch>/base/tools/round-47/exact.py                    # R8
python3 -I -B attack/ablate2.py                                                          # R6
python3 -I -B attack/ablate3.py                                                          # R7
python3 -I -B attack/abl_mini.py <scratch> $PWD 09a9f912…                                 # R9
```

`attack/` holds the four drivers (probe matrix, candidate-case matrix, two ablation
drivers, mini-ablation). Each driver copies `exact.py` into its own scratch tree with
`tools/round-46/gate.py` beside it, patches the copy only, and runs the real counter
against the lane root.

Scratch `/fast/scratch/hyaku/kaidoku-r47/SimplC1` was removed after these receipts were
copied here.
