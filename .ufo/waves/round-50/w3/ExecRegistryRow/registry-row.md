# R50-C3 instrument-registry v2 row — draft for the L1

Seat: ExecRegistryRow (wave 3, build). Lane: `kaidoku-shokunin`.
Source of truth: `plans/round-50-attempt2-claims.md` section R50-C3 (the plan is the rule).

## 0. The one decision the L1 must take first: the path

**The instrument must land at `tools/round-50-c3/sqfs-triage-v5.py`, NOT
`tools/round-50/sqfs-triage-v5.py`.**

My seat prompt named the in-tree path. The plan names the out-of-tree path, and the plan is
right — measured, not asserted:

| landing path | C1 `frozen_drift` (freeze `435d41fd`) | C2 `freeze_check` (freeze `435d41fd`) | B9 census |
|---|---|---|---|
| `tools/round-50/sqfs-triage-v5.py` | `['tools/round-50/sqfs-triage-v5.py']` → **C1 exit 2** | `frozen_path_changed` → **C2 exit 2** | gains the path |
| `tools/round-50-c3/sqfs-triage-v5.py` | `[]` → **no drift** | `(None, None)` → **no drift** | unchanged (12 paths) |

Why: `tools/round-50/c1-counter.py` freezes the whole directory family
(`FROZEN_PREFIXES = ('tools/round-50/',)`, `tools/round-50/c1-counter.py:425`) and
`tools/round-50/c2-record.py` freezes `FROZEN = ('tools/round-50', 'plans/round-50-claims.md')`
(`tools/round-50/c2-record.py:123`). An `A` status under either frozen path is drift — the
C1 arm adds it on `A` under a frozen prefix, the C2 arm on any touched frozen path. The
in-tree path therefore makes **both** frozen counters exit 2 at the C3 landing revision, and
the C1 data run (the L1's later job) would be scored against a drifted freeze.

The plan's path rule (`plans/round-50-attempt2-claims.md:66-71`) already reached this
conclusion from a wave-3 seat measurement; my independent re-measurement reproduces it
exactly. **The row below is therefore for `tools/round-50-c3/sqfs-triage-v5.py`.**

## 1. The row (verbatim, one line, seven cells)

Paste this immediately before `<!-- /instrument-registry -->` in `SKILL.md`:

```
| `tools/round-50-c3/sqfs-triage-v5.py` | gate — R50-C3 depth: the SKILL rule block 22 triage table v5 scored against the frozen independent evaluator over the round-42 recon envelope corpus (table label and action against evaluator label and action, pair_mismatches, evaluator_missing, the committed mutation battery), run as `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root LANE --rev REV --freeze FREEZE --envelopes DIR --json-out OUT` | 0=met, every envelope's table label and action equal the evaluator's, pair_mismatches 0 and evaluator_missing 0 at --rev, and the committed mutation battery green; 1=not met, a named envelope pair mismatch or a false binding, the receipt still written; 2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, an absent envelopes directory or a refusal | python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest — the committed mutation battery; the case count and the exit code are recorded in the freeze receipt | .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/manifest.json (the R42C2ReconLegacy envelope manifest) and .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ (the frozen held-out envelope set) | --json-out and a private scratch under $HYAKU_SCRATCH/kaidoku-r50/c3; never the lane | kaidoku |
```

Machine-readable copy: `row-final.txt` in this directory (same bytes as the block above).

## 2. Cell-by-cell derivation against the house grammar

The twelve attempt-1 rows (`tools/round-49/*` six, `tools/round-50/*` six) use a fixed
seven-cell shape. The row above mirrors it:

| cell | house grammar (from the attempt-1 rows) | this row | check |
|---|---|---|---|
| 0 | the exact path, backticked, `cell-0` | `` `tools/round-50-c3/sqfs-triage-v5.py` `` | exact path equality, no duplicate in the region |
| 1 | `gate — <purpose>, run as \`<entry command>\`` | `gate — R50-C3 depth: …, run as \`python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --root LANE --rev REV --freeze FREEZE --envelopes DIR --json-out OUT\`` | opens `gate`, entry command names the path |
| 2 | `0=met, …; 1=not met, …; 2=could-not-evaluate, …` | the gate-flavor three-segment map | round-48 meaning rule: `0`→success, `1`→not-met, `2`→unevaluable; three distinct segments |
| 3 | `python3 -I -B <path> --selftest …` | `python3 -I -B tools/round-50-c3/sqfs-triage-v5.py --selftest — …` | the frozen B9 self-test spelling `<interpreter> <path> … --selftest` |
| 4 | the pinned-value path | the R42C2ReconLegacy envelope manifest + envelope dir | names a path that exists and is git-tracked |
| 5 | the write scope | `--json-out` and a private scratch under `$HYAKU_SCRATCH/kaidoku-r50/c3; never the lane` | no lane write |
| 6 | `kaidoku` | `kaidoku` | house owner token |

Note on cell 3: the attempt-1 rows state a concrete case count and date (e.g. "29 cases, exit 0
on 2026-10-28"). The v5 instrument does not exist yet, so this row deliberately states the
*spelling* and points at the freeze receipt for the count and exit code rather than inventing
numbers. The L1 should replace that clause with the measured values once the instrument's
selftest has actually run — and must not land the row with a fabricated count.

Note on cell 4: the pinned-value path is the **envelopes manifest**, per the seat brief. The
manifest (`sha256 1acd4ca21435477b5a7141f0edfef081212526ffb0280810dca4c0e72a20bbb9`) is
git-tracked and is the file that names the 135 corpus entries (126 of which have an
`envelopes/<run>/` directory; nine are manifest-only per `REBUILD.md`).

## 3. B9 coupling — the simulation

`tools/round-50/c2-record.py` atom B9 (docstring lines 77-84, implementation lines 852-893)
derives its census as:

```
pick(BASE='7c678ae6…', 'tools/round-49')  +  pick(REV, 'tools/round-50')
```

where `pick` keeps `.py`/`.sh` and drops `/control-fixtures/`. It then requires each census
path to be the **cell-0 path of exactly one row** of the marker-bound region, with a
`gate|probe` kind, an entry command naming the path, a 0/1/2 verdict map bound to meanings,
a self-test spelling, and a pinned-value path.

The future REV's `tools/round-50/**` set is the current six plus the new instrument, so the
census is 13 paths. With the out-of-tree path the census stays at **12** and B9 is green
without the new row; with the in-tree path the census becomes **13** and B9 *requires* the
new row.

Three arms, each run against the frozen `b9()` / `registry_region()` / `meaning_classes()`
in a scratch clone (`git clone --shared` of the lane, detached at `6f4aba63`):

| arm | landing | B9 verdict |
|---|---|---|
| A | file in-tree, **no** registry row | `tools/round-50/sqfs-triage-v5.py: no registry row` → **red** |
| B | file in-tree **+** candidate row | `b9_problems []` → **green** |
| C | registry row for the out-of-tree path, file out-of-tree | `b9_problems []` → **green**, census still 12 |

So the row is not optional bookkeeping: it is the only thing that keeps B9 green if the
instrument lands in-tree, and it is harmless if it lands out-of-tree. Either way it is the
right thing to land, and the out-of-tree path is the one that also keeps C1 and C2 green.

**Dangling paths: none.** Every `tools/round-50/**` `.py`/`.sh` path at the simulated future
REV is cell-0 of exactly one row:

```
tools/round-50/c1-controls.py      tools/round-50/c1-counter.py
tools/round-50/c1-run.sh           tools/round-50/c2-record.py
tools/round-50/fetch-vendor.py     tools/round-50/selftest-r49-c2.py
```
(the six attempt-1 rows) plus, with the in-tree path, `tools/round-50/sqfs-triage-v5.py`
covered by the new row. The `tools/round-50/oracle/**` and
`tools/round-50/control-fixtures/**` trees hold no `.py`/`.sh` and are outside the census by
the prefix rule. `tools/round-50-c3/**` is invisible to B9's census because `git ls-tree
-- tools/round-50` matches the `tools/round-50` directory only — verified, 0 hits.

**One coupling the L1 must respect:** `tools/round-50/` may receive **no** new `.py`/`.sh`
beyond the six already registered. The plan's C3 freeze adds only the instrument, the
registry row and the SKILL.md rule block 22. If the C3 build needs a second helper script, it
must live outside `tools/round-50/` or it will need its own registry row *and* will trip the
C1 freeze-drift arm.

## 4. Effects on the other registry gates (measured, not assumed)

| gate | at `6f4aba63` (HEAD) | at the simulated C3 landing rev (out-of-tree + row) | verdict |
|---|---|---|---|
| `tools/round-50/c2-record.py` (freeze `435d41fd`) | exit 0, 11/11 atoms green | **exit 0, 11/11 atoms green, `mismatches 0`** | unchanged, green |
| `tools/round-50/c2-record.py` (freeze = C3 landing) | — | exit 0, 11/11 green | green |
| `tools/round-50/c2-record.py` (freeze `435d41fd`, in-tree path) | — | **exit 2 `frozen_path_changed`** | the in-tree path is the only thing that breaks it |
| `tools/round-46/registry.py` | exit 0, `met_target true` | exit 0, `met_target true`, `failing []` | unchanged, green (its census is rounds 41-46; extra rows are not its failure mode) |
| `tools/round-45/c2-counter.py` | exit 0, `met_target true`, `scope_size 6` | — | unchanged, green (scope is rounds 44-45 only) |
| `tools/round-48/meanings.py` | exit 1, `registry_extra` = 12 rows | exit 1, `registry_extra` = 13 rows (the new row joins the existing 12) | **already red before this row; the row adds one to a pre-existing failure list** |
| `tools/round-49/c2-mismatch.py` | exit 1, A8 red (`rows 146 -> 149, derived 146 -> 152`) | exit 1, A8 red, **identical numbers** | unchanged — A8 counts SOURCES.md rows, not registry rows |

The R48 `registry_extra` failure is pre-existing and disclosed: the attempt-1 landing added
twelve rows outside `tools/round-48/census2.json` (which covers rounds 41-48 only), and
`plans/round-50-claims.md:34-38` already records that "added rows in the
`instrument-registry v2` block of `SKILL.md` are rows outside the frozen round-48
`census2.json`; both older counters were verified at their own revisions and are not
re-run as gates this round". The new row is one more of the same kind. **It is not a new
defect and does not need fixing**, but the L1 should know the R48 counter's `registry_extra`
list grows from 12 to 13.

## 5. What the L1 should do with this draft

1. Land the instrument at **`tools/round-50-c3/sqfs-triage-v5.py`** (not in-tree), with the
   row above in `SKILL.md` immediately before `<!-- /instrument-registry -->`.
2. Replace the cell-3 clause with the instrument's measured selftest count and exit code
   once the selftest has actually run. Do not invent them.
3. Keep every other new `.py`/`.sh` out of `tools/round-50/`.
4. If a C3 helper script is needed, either put it under `tools/round-50-c3/` (invisible to
   B9's census) or register it.
5. Re-run `python3 -I -B tools/round-50/c2-record.py --root <LANE> --rev <FINAL> --freeze
   435d41fd…` after the landing: it must stay exit 0 with `mismatches 0`. That is the
   coupling this row exists to protect.
6. **Do not freeze the 49-byte stub currently sitting at `tools/round-50-c3/sqfs-triage-v5.py`.**
   It is a do-nothing that exits 0 on `--selftest` (with empty stdout) and exits 0 on the
   full predicate command while writing **no receipt** — a fake green, exactly the
   do-nothing control the claim requires to be red. The real instrument is 90,837 bytes,
   sha256 `c444f7ee918234bfa0b286afd37739a3b9fa1e7b2cdd4455fd4b25862f66367f`, and with it
   plus this row the C2 counter is exit 0 / 11-of-11 green at freeze `435d41fd`. Copy it
   byte-identically, verify with `sha256sum` + `cmp`, and require the instrument's
   `--json-out` receipt to exist and parse — a zero exit alone is not evidence.
7. Prefer **this** row over the competing `ExecTriageV5` landing-draft row: that row's cell 3
   opens with a backtick, so it does not satisfy B9's frozen self-test spelling
   (`selftest_cell_ok = False` under the frozen regexes); this row passes. Both are 7 cells
   with a valid 0/1/2 meaning map — the difference is the self-test cell alone.

## 6. Honest limits of this draft

- The instrument did not exist when this draft was written, so cell 3's count and cell 1's
  purpose wording were the only parts that might need a later edit. Every check in section 2
  was run against the frozen derivations in `tools/round-50/c2-record.py` and
  `tools/round-48/meanings.py`; the row as written passes all of them. (The instrument now
  exists at 90,837 bytes, sha256 `c444f7ee…` — see section 5 item 6 for the stub that must
  not be frozen in its place.)
- I did not build the instrument, and this seat does not own it.
- I did not run any REA, and I ran no `--data-run`. Every counter invocation above is an
  offline, in-clone measurement of a frozen counter's own derivation or its whole scoring
  path with `--rev`/`--freeze` pointed at a scratch clone.
- The four `v2ns *_ddefault` rows the claim names are confirmed present and confirmed
  `clean`/`none` in the committed manifest (2.0-be, 2.0-le, 2.1-be, 2.1-le; all four have
  envelope directories). The two other no-reader families carry 7 and 8 `clean`/`none`
  `_ddefault` rows respectively, so the v5 rule's effect is wider than the four the claim
  names — worth a line in the C3 after-run receipt, not a change to this row.
- Re-derived from the committed manifest: the corpus holds **38** no-reader envelopes
  (19 `clean`/`none`, 19 `depth-limited`) and **zero** no-reader extractor-failure-with-0-files
  envelopes. The `no-reader-failure` row is therefore unexercised by the corpus, and the two
  mutations the sibling's controls receipt marks `corpus=VACUOUS` are genuinely vacuous
  there. That is a disclosed limit for the C3 after-run, not a defect in this row.
- The real instrument at the landed path was measured against this row: `--selftest` green
  (13 cases), the predicate command reproduces the claim's before-state (exit 1,
  `pair_mismatches 19`, all four `v2ns *_ddefault` rows among them), and the frozen C2
  counter is exit 0 / 11-of-11 atoms green at freeze `435d41fd` with both committed together.
