# CritC1Predicate — R47-C1 predicate falsification (round 47, wave 1)

**Verdict: predicate too weak, here is what closes it.** A block that teaches nothing reaches
`exit 0` with the *same* battery receipt as the landed block. The predicate is a schema
check: it reads the table's grammar and the two pins, never the matrix's content.

Measured against `tools/round-47/exact.py@62e33f7d` — sha256
`dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`, the bytes the landed
block pins — and re-checked against the tip bytes at `a0753786` (sha256 `01a4bca7…`).
`git diff 62e33f7d a0753786 -- tools/round-47/exact.py` touches only `_fixture_files` (A6,
fixture completeness); clauses 1–9 are byte-identical, so none of this is about a superseded
draft.

## 1. The counterexample (sharpest form)

590 characters, no prose, title `24. Shopping list.`, empty `v2 hole` column, arms permuted
against their routed ids, one citation repeated three times
(full text: `blocks/vE-titleless-nonsense.block.txt`, block sha256
`6eef64fe6c48…`):

```
- **24. Shopping list.** <!-- exactness-table v3 --> `tools/round-47/exact.py`
  interpreter_sha256:dcef54f1…c412c mutations_sha256:19a2166e…a112 names
  substring-arm, duplicate-routed-id, stale-mutations-digest, flag-order-drift.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 |  | order | 1 |
| R46-CL3 |  | symbol | 1 |
| R46-CL4 |  | once | 1 |
| R46-CL6 |  | digest | 1 |

  Refs: `corpus/lessons/round-46.md:1`, `plans/round-47-claims.md:1`, `tools/round-47/exact.py`
```

Command (fixture repo built from the lane's own bytes at `62e33f7d`, freezes == rev, so the
freeze guard is satisfied by construction — see §5 for why that is the only reachable
configuration):

```
python3 -I -B tools/round-47/exact.py --root <fixture> --freeze <fixture-rev> --rev <fixture-rev>
```

Result: **exit 0**, `failing == []`, `battery {forgeries_total 4, v2_green 4, v3_green 0,
genuine_green 1, crash 0}` — the same receipt as the genuine landed block
(`control-genuine`, 2121 chars, also exit 0, same battery). The matrix's semantics are
inverted (`R46-CL2` claims the `order` arm, `R46-CL6` the `digest` arm) and nothing notices.

## 2. Evidence — ten fixtures, two counters

Every fixture is a one-commit git repo under my scratch, built from `git show 62e33f7d:<path>`
for `SKILL.md`, `plans/round-47-claims.md`, `tools/round-47/exact.py`,
`tools/round-46/gate.py`, `corpus/lessons/round-46.md`, `corpus/lessons/round-45.md`; only
`SKILL.md` block 24 differs. Drivers: `receipts/attack.py`, `receipts/attack2.py`. Machine
receipts: `receipts/runs.json` (frozen vs proposed), `receipts/runs-at-a0753786.json`,
`receipts/scores.json`, `receipts/scores2.json`.

| variant | what it changes vs. the landed block | chars | frozen exit | tip (A6) exit | battery |
|---|---|---|---|---|---|
| `control-genuine` | nothing (the landed block) | 2121 | 0 | 0 | 4/4/0/1/0 |
| `vE-titleless-nonsense` | title subject, all hole cells, arm order, all prose | 590 | **0** | **0** | 4/4/0/1/0 |
| `vA-junk-holes-permuted-arms` | hole cells `n/a`, arms permuted, exits all `0` | 635 | **0** | **0** | 4/4/0/1/0 |
| `vB-empty-holes` | hole cells empty, arms permuted, exits all `2` | 620 | **0** | **0** | 4/4/0/1/0 |
| `vC-repeated-refs` | one citation repeated three times | 639 | **0** | **0** | 4/4/0/1/0 |
| `vD-same-arm-four-times` | all four arm cells `symbol` | 636 | **0** | **0** | 4/4/0/1/0 |
| `vF-block23-relabelled` | block 23's table relabelled `24. ` (claims' own kill rule) | 4334 | 1 | 1 | — |
| `vG-hole-column-n-a` | **only** the `v2 hole` column → `n/a` | 1879 | **0** | **0** | 4/4/0/1/0 |
| `vH-arms-swapped` | **only** two arm cells swapped (`symbol` ↔ `digest`) | 2120 | **0** | **0** | 4/4/0/1/0 |
| `vI-minimal-after-fix` | correct arms+exits, every prose cell empty | 602 | **0** | **0** | 4/4/0/1/0 |

`vG`/`vH` are single-variable: one column changes and the verdict does not move. `vF`
confirms the claims file's kill rule holds (a block-23 copy fails clauses 2–6), so the
predicate is not vacuous *about its own kill rules* — it is vacuous about teaching.

Fixture revs and block sha256: `receipts/fixtures-meta.json`.

## 3. What each clause actually binds

| clause | binds | does **not** bind |
|---|---|---|
| 1 | marker count, title prefix `24. `, block is last | the title's subject (`24. Shopping list.` passes) |
| 2–3 | header cells, 4 rows × 4 cells, exit ∈ {0,1,2} | which exit belongs to which row |
| 4 | each `R46-CL<n>` appears once, in the trigger cell | that the row addresses the id it names |
| 5 | the arm cell is *one of* four tokens | that the token is **that row's** clause; no distinctness (vD); no set coverage |
| 6 | pin matches the counter's own list; the four names appear *somewhere* | that the names map to rows, or that the prose describes them |
| 7 | `gate.py`'s literal appears once, reversed zero | — (this one is exact) |
| 8 | ≥3 `path:line` occurrences resolve; `round-46.md` among them | distinct loci (vC: one selector × 3), or that any citation supports any row |
| 9 | the counter discriminates four *token*-level forgeries | anything about the block's content: all vacuous variants score the identical battery |

The `v2 hole` column — the only column that states *why* each v2 binding was loose, i.e. the
block's teaching content — is never read (vG). The arm column's semantics are never read
(vH). Between them that is all of the block's depth.

## 4. Is `exactness` the right axis and the right surface?

- **Axis (`depth`).** The attribution is conventional, not a category error: rounds 45/46
  scored blocks 22/23 the same way, and the landed block *does* teach (its hole cells name
  the mechanisms and its refs resolve). But the predicate cannot see that. What it measures
  is *schema conformance of a table plus the counter's sensitivity to four token mutations* —
  a coverage/instrument property, not depth. Charging `depth` for it overstates the claim by
  exactly the amount vG/vH demonstrate.
- **Surface (`tools/round-47/exact.py`).** Right place for the measurement; the loss is that
  clauses 1–8 are a grammar and clause 9 is monotone in that grammar. An artefact that
  conforms and says nothing is indistinguishable from one that conforms and teaches.
- **Consequence for the landing.** The claim's Target (`failing == []`) is true of the
  landed block *and* of a shopping list. Post-landing the record cannot cite R47-C1 as
  evidence of depth without this being the first thing a hostile reader finds.

**The weakness is in the frozen claim, not only in the code.** Predicate clauses 5 and 8 as
written ("is one of `symbol`/`once`/`digest`/`order`", "at least three citations carry a line
selector") admit vD and vC on their face: no row-map, no distinctness, no occurrence-vs-locus
distinction. Patching `exact.py` alone would make the counter stricter than the claim it
implements — so closing this needs a claims amendment *and* a re-pinned
`interpreter_sha256` in block 24, i.e. one more entry in the A-series, which is exactly the
tension §6 measures.

## 5. Smallest safe correction (measured, not proposed on faith)

Two clauses and one text change; prototype in `receipts/exact_fix.proposed.py`, applied to a
**copy** — frozen bytes untouched.

```python
ROUTED_ARM = {"R46-CL2": "symbol", "R46-CL3": "once",
              "R46-CL4": "digest", "R46-CL6": "order"}
MUT_FOR_ID = {"R46-CL2": "substring-arm", "R46-CL3": "duplicate-routed-id",
              "R46-CL4": "stale-mutations-digest", "R46-CL6": "flag-order-drift"}
# clause 5': the arm cell must equal the clause of ITS OWN routed id
wrong = [(per_row[i][0], arm[i]) for i in range(len(rows))
         if len(per_row[i]) == 1 and arm[i] != ROUTED_ARM[per_row[i][0]]]
# clause 9': the exit cell must equal the v3 exit that row's forgery actually returns
#           (re-derived from the battery, never a literal)
out["exit_cells_match"] = all(str(f["v3_exit"]) == row_exit[MUT_ID[f["name"]]] ...)
```

| variant | frozen | proposed |
|---|---|---|
| `control-genuine` | 0 | **0** (kept green — no SKILL.md edit needed) |
| `vA` `vB` `vD` `vE` `vH` | 0 | **1** (`arm tokens name another row's clause`) |
| `vC` | 0 | **1** (`battery exit_cells_match 0 != 1`) |
| `vF` | 1 | 1 |
| `vG` (hole column) | 0 | **0 — residual** |
| `vI` (602 chars, correct arms/exits, empty prose) | 0 | **0 — residual** |

**Third binding, needed for the residual:** require each row to carry its own resolving
`path:line` selector and the four selectors to be distinct. That is a *text* change to the
landed block (its citations sit in one trailing `Refs:` line), so it is the L1's call:
either land it with per-row refs and add the clause, or state plainly that the predicate
binds provenance, not teaching. **Hard limit, stated honestly:** no static predicate can
prove a citation *supports* its row — a determined forger cites arbitrary resolvable lines.
The three bindings move the cost from "copy the header" to "reproduce the counter's per-row
measurement and point at four distinct loci"; that is the strongest mechanical closure
available, and it should be named as such rather than sold as depth.

## 6. Secondary finding — the documented counting command cannot return 0

`plans/round-47-claims.md` says the freeze is the commit that first holds it and
`tools/round-47/` (= `5017e1f7`), and A1 re-declares it as "the commit that carries this
paragraph" (= `9018c53b`). Every amendment after that touches the frozen directory
(`git log --name-status 13a9e9e1..HEAD -- plans/round-47-claims.md tools/round-47/`:
`62e33f7d`, `2e4ae434`, `1e2c3102`, `07d2894e`, `a0753786` all modify `tools/round-47/`), and
`gate.freeze_state` returns 2 `frozen_path_changed` for both declared freezes.

Measured at tip `a0753786` (`receipts/freeze-series-at-tip.json`):

| `--freeze` | exit | reason |
|---|---|---|
| `5017e1f7` (claims: first commit holding the file) | 2 | `frozen_path_changed` |
| `9018c53b` (claims: A1, the declared freeze) | 2 | `frozen_path_changed` |
| `e856beb5` landing | 2 | `frozen_path_changed` |
| `62e33f7d` A2 / `2e4ae434` A3 / `1e2c3102` A4 / `07d2894e` A5 | 2 | `frozen_path_changed` |

At `caafeffa` (pinned, `receipts/freeze-series-pinned.json`) A4 → 0 and A5's predecessor → 0,
so the guard is not structurally void — but the freeze the *claims file* names is stale by
five amendments, and the directory keeps being touched. As long as the exactness counter
keeps being amended, the only `--freeze` that scores is one at or after the last touch, i.e.
the amendment series itself is now the freeze. Either declare A6 as the freeze in a further
amendment and stop touching `tools/round-47/`, or state that the guard is void for this
claim. Exit 2 never counts toward a target, so today R47-C1 is unscoreable via the documented
command at the tip.

## 7. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r47/CritC1Predicate; export TMPDIR="$S" HYAKU_SCRATCH="$S"
python3 -I -B "$S/attack.py"  62e33f7d     # vA..vE + control-genuine
python3 -I -B "$S/attack2.py" 62e33f7d     # vF, vG, vH (single-variable)
# each prints {"variant":…, "fixture": <dir>, "rev": <sha>}; then
python3 -I -B tools/round-47/exact.py --root <dir> --freeze <rev> --rev <rev>
```

Scratch `$S` is removed after this report; the drivers, the ten block texts
(`blocks/*.block.txt`, each with its sha256 in `receipts/fixtures-meta.json`) and every
stdout receipt are preserved under
`.ufo/waves/round-47/w1/CritC1Predicate/receipts/`, so every fixture is rebuildable from
`62e33f7d` alone.

## 8. Not run / out of scope

- `tools/round-47/record.py` (R47-C2) — not measured here; other seats hold it.
- The lane's own selftests (`exact.py --selftest`, `record.py --selftest`) — verification is
  the main agent's job; I ran only the clause path under test.
- No installs; no tool used outside `python3`/`git`. Nothing written outside this seat's
  report dir and its scratch; all git work in throwaway one-commit repos under `$S` with
  `git -C "$D" rev-parse --show-toplevel == $D` asserted before each commit.
