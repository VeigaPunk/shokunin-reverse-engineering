# ConnRouted — sibling-overlap scan over `tools/round-4[1-8]` clause vocabulary

Seat: ConnRouted (connector, leaf). Scope: which lane counters share the clause
vocabulary `met_target` / `failing` / exit-2 "could-not-evaluate" /
`frozen_path_changed`, and where each sibling's semantics disagrees with the
round-48 predicates. Lane read-only; all mutation was on scratch copies.
Measured freeze for probes: `ac02a79ff84133220d01ce3b59a4789b7004dbc5` (see
"Freeze-id contradiction" below).

## 0. Freeze-id contradiction (state, not smooth)

- This prompt pins the declared freeze as `dc73587a…` (A1).
- `plans/round-48-claims.md` is the rule and says (line 156–158): **"The declared
  freeze is the commit that carries this paragraph"** — the A2 paragraph.
  `git log -1 -- plans/round-48-claims.md` and `-- tools/round-48/` both return
  `ac02a79f`. The A1→A2 delta is 1 line of `meanings.py` (the NOTMET guard in the
  exit-0 classifier) + 13 lines of claims text. `record2.py` is byte-identical.
- Consequence: a `--freeze A1 --rev A1` run executes the **A2 worktree** counter
  (counters grade committed bytes but execute from the worktree — the R47-CL1
  hole, still open for the counters themselves; `meanings.py` is pinned only
  *inside* its own scored block via `interpreter_sha256`, nothing pins the
  runner's `sys.executable` byte-source). C2Floor's receipt used `--freeze dc73587a
  --rev dc73587a`; `gate.freeze_state` returned clean because the range is empty.
  For the L1's re-measure, pass `--rev` at the landing commit — the frozen-set
  union (gate.py:152–167) means the declared claims file at A2 is what matters.

## 1. Vocabulary-sharing map (who shares the four terms)

| file | `met_target` | `failing` | exit-2 = could-not-evaluate | `frozen_path_changed` |
|---|---|---|---|---|
| round-41 c1/c2-counter.py | yes (conjunction over `bindings`) | **no** — receipt uses `bindings`, `unevaluable`, `met_target`, `exit_code` | yes, `Unevaluable` exception (`c1-counter.py:329–342`) | yes, `FrozenPathChanged` (`c1-counter.py:333–338`) |
| round-42 c1/c2-counter.py | yes | **no** (same `Unevaluable` family) | yes | yes |
| round-43 c1-counter.py | yes | no | yes, docstring lines 100–102 | yes, `Unevaluable('frozen_path_changed')` line 1484 |
| round-43 c2-score-r43.py / c2-controls-r43.py | n/a | n/a | n/a — controls, not counters | n/a |
| round-44 c1-counter.py | yes | no | yes | yes (`c1-counter.py:372–377`) |
| round-44 c2-counter.py | yes — **weakened by `enforce_freeze`** | no — `mismatches` + `unevaluable` lists | yes (`EXIT_CANT`) | yes — **conditional** (D1) |
| round-44 c2-rubric.json | data | data | data | data (rubric declares its own frozen set; `c2-rubric.json:178` note — `corpus/README.md` deliberately NOT byte-frozen) |
| round-45 c1/c2-counter.py | yes (`met_target: not reasons`) | **yes — first appearance** (`c1-counter.py:200`) | yes (`c1-counter.py:127`) | yes — inline `FROZEN` const, `git log` walk (`c1-counter.py:32,52–56`) |
| round-45 frozen-path-preflight.py | n/a | no | exit 2 reserved for unknown rev / git failure | **same token, exit 1** (D2) |
| round-46 gate.py / attest.py / registry.py | yes | yes | yes (gate.py:238–243 `main_guard`) | yes — canonical (`gate.py:144–195`) |
| round-47 exact.py | yes | yes | yes (`exact.py:171`) | yes, via `gate.freeze_state` (`exact.py:400`) |
| round-47 record.py | yes | yes | yes (`record.py:311`) | **ABSENT** (D4) |
| round-48 meanings.py / record2.py | yes | yes | yes | yes, via `gate.freeze_state` (`meanings.py:534`, `record2.py:477`) |

Also sharing the *family* but not these exact keys: `round-41/{indep-eval-v3,
sqfs-triage-v3}.py`, `round-42/{c2-controls,heldout-gen-v4,indep-eval-v4,
prefile-gate,sqfs-triage-v4}.py`, `round-43/heldout-gen-v4r43.py`,
`round-44/c1-controls.py` use `failing` for internal reasons without a claim
receipt shape — same word, different object (vocabulary seam, not a conflict).

## 2. Disagreements with the round-48 predicates — named, file:line

### D1 — `met_target true` is reachable with `frozen_path_changed` non-empty (r44-c2)
`tools/round-44/c2-counter.py:1046–1049`:
`met_target = not mismatches and not unevaluable and (not frozen_path_changed
**or not enforce_freeze**) and entries_evaluated > 0` — under `--pre-freeze`
(`score(..., pre_freeze)` → `finalize(..., enforce_freeze=not pre_freeze)`,
lines 1199–1308) a receipt can carry `met_target: true` **and**
`frozen_path_changed: […]` simultaneously; only `claim_gate.
usable_as_claim_score` (lines 1062–1070) is strict. Round-48's vocabulary has
no such mode: `gate.freeze_state` exit 2s before scoring (gate.py:187–195). A
reader porting r44-c2's `met_target` would accept a claim score r48 rejects.
*Status:* intended per-round mode, but a real semantic fork of `met_target`.

### D2 — `frozen_path_changed` maps to exit **1**, not exit 2 (r45 preflight)
`tools/round-45/frozen-path-preflight.py:142–155`: `verdict:
"frozen_path_changed"` returns `(0 if ok else 1)` — the same token the round-46
gate and every r46+ counter reserves exit 2 for. The r48 claims file line 12
stipulates `frozen_path_changed` ⇒ **exit 2** ("a change makes both counters
exit 2 `frozen_path_changed`"). The preflight is a red-before-commit probe, so
exit 1 is self-consistent there, but it is the only lane instrument where the
token means "not met" instead of "unevaluable."

### D3 — r45's frozen walk is claims-blind, worktree-blind, and merge-blind
`tools/round-45/c1-counter.py:32` `FROZEN = [CLAIMS, "tools/round-45"]`;
`frozen_path_changed()` (lines 52–56) is `git log --name-only` over that
hardcoded pair — no `## Frozen paths` parsing (a claims file declaring more is
invisible), no `git status` union (a dirty worktree frozen tool scores clean —
the hole `gate.dirty`/`frozen_worktree_dirty` at gate.py:173–191 closes), and
no `-m --diff-merges=first-parent` (a merge-resolution edit to a frozen path is
invisible — gate.py:94–95 names this R45-CL6). `round-45/c2-counter.py:30,63–78`
is identical shape. r48 inherits the gate semantics; r45's are strictly weaker.

### D4 — round-47 `record.py` has no freeze gate at all
`tools/round-47/record.py:456` `evaluate(root, rev, with_battery)` — the only
claim counter whose CLI has no `--freeze` and can never emit
`frozen_path_changed`. Its round-48 successor restores it via `gate.freeze_state`
(`record2.py:477–495`). Disagreement by absence: r47-record grades committed
bytes yet is unexaminable under the shared vocabulary term.

### D5 — the corrections grammar silently drops `axes` and `quote` (R47-CL14)
`tools/round-47/record.py:50` `CORR = …(seats|window|path|rev)` vs
`tools/round-48/record2.py:44` `…(seats|window|path|rev|axes|quote)`.
**Probe P2** (receipt `p2-corr-grammar`, sha 497f41fd…):
`- corrects axes coverage: 5/7` → r47 match **False**, r48 match **True**.
`record.py`'s own `derive`/`corrects` carry `axes` arms (lines 223, 280–292)
that are unreachable from its grammar — dead code by grammar hole; and the
`axes`-correction parse exists only as an *exemption* path, never validated
against `axis_pairs`. r48 parses the classes and re-derives them.

### D6 — completeness is pooled in r47, floored per-section in r48 (R47-CL10 C2)
`tools/round-47/record.py:377–379`: `missing_classes` is computed over
`atoms_by_class` **pooled across both `## Round N` sections** — one fat section
masks an empty sibling (exactly the "measures consistency, never completeness"
defect). `record2.py:214–231` floors each section independently (seats-or-
correction, path, rev, claim id) plus claim-id uniqueness across sections
(lines 232–239) and a ≥2 `axes` atom head requirement (240–243).

### D7 — no quoted-receipt binding in r47 (R47-CL13)
`record.py` has **no** `QUOTE`/`RECEIPT`/`quote_value` machinery — a number the
record quotes from its own receipt is unbound. `record2.py:46–47,114–137,274–301`
adds `QUOTE`, `RECEIPT` (`\.ufo/waves/round-[0-9]+/l1/scores/…json`), per-key
`quote_value` (digging `["receipt"][key]` → top-level), and a `quote` correction
re-derivation that must name a receipt-true value *and* fix a wrong quote
(`_quote_correction`, lines 159–177).

### D8 — the `axes` class binds the fraction, never the score cell (R47-CL2)
`tools/round-47/record.py:39–40,178–183`: the `axes` atom captures only
`FRAC.search(m.group(2))` — `n/d`; the `→ score` cell beside it is never bound.
`tools/round-48/record2.py:48–49,140–156` parses `SCORE_CELL` from `cell[0]` (the
A1 fix) and `FRAC` from `cell[1:]`, then clause 5 requires
`score == round(10*n/d, 2)` (lines 303–315).

### D9 — arm cells are multiset-bound in r47, keyed by routed id in r48 (R47-CL10 C1)
`tools/round-47/exact.py:236–243` checks only that every arm cell ∈ VOCAB and
counts ids as a multiset (218–229): permuting the *arm* values across the *ids*
is green under r47 semantics — the "permutation hole" the claims file names.
`tools/round-48/meanings.py:46,358–370` adds `EXPECTED_ARM = {R46-CL7: meaning,
R47-CL10: floor}` keyed per routed id; the `permuted-arm` mutation is one of its
own four forgeries.

### D10 — r46's registry check binds digits, not meanings (R46-CL7)
`tools/round-46/registry.py:46` `EXITMAP = re.compile(r"\b([012])\s*[=:]")` and
`thin` at lines 194–198 requires only `keys == {"0","1","2"}`; the r45 fallback
(lines 199–202) accepts **bare digits** ("0 rows, 1 column, 2 bytes" binds
nothing but passes the lenient profile).
**Probe P1** (receipt `p1-meaning-classes`, sha b092168b…):
`0=banana; 1=nope; 2=whatever` → r46 `thin`-check **PASS**, r48
`meaning_classes` → `{'error': 'verdict map names no meaning class
(placeholder text)'}`. The swapped-meaning cell → `exit 0 segment names no
success meaning` (the A2 guard-drop is load-bearing: swapping is still caught
via the exit-0 segment carrying the exit-2 text). A tautological
`0=pass; 1=fail; 2=usage error` **passes** r48 — the classifier binds meaning
*classes*, not falsifiability; that is by design (the claim binds meaning, not
proof).

### D11 — census scope ends at round 46 in the r46 instrument
`tools/round-46/census.py:26–27` `CLAIMS`/`TOOL` bound `round-4[1-6]`;
`tools/round-48/census2.py:27–28` bound `round-4[1-8]` (docstring lines 9–12
states the reason). Disagreement: the committed `census2.json` has **42 paths**;
an artefact whose registry rows are exactly the r46 census fails r48 clause 8 on
`registry_missing` (the two missing rows today are exactly the new counters —
see §3). Note `census2.census_text` uses `read(p) is not None` where `census.py`
used `gate.blob` — same membership semantics, different null source; not a
disagreement.

### D12 — profile numbering shifted: `v2` was strict, now it is lenient
`tools/round-46/attest.py:153` and `registry.py:141`: `hard = profile == "v2"`;
r46's battery keys are `v1_green` (lenient accepts all) / `v2_green == 0`
(strict rejects all) — `registry.py:216–217`. In r47/r48 (`exact.py:167`,
`meanings.py:304`, `record2.py:181`) `hard = profile == "v3"` and the same key
`v2_green` flips sign: r48 wants `v2_green == {4|5}` (lenient accepts every
forgery), `v3_green == 0`. Same vocabulary, opposite end of the leniency axis —
a reader porting r46 expectations misreads every r48 battery receipt.

### D13 — `failing` as the false-clause list is a round-45+ invention
r41–r44 receipts name failures through `bindings`/`mismatches`/`unevaluable`
(e.g. `round-41/c1-counter.py:1790–1798`, `round-44/c2-counter.py:1150–1154`);
the `failing: […]` list of false clause strings first appears
`round-45/c1-counter.py:200` and is uniform r46→r48. Not a defect — but "naming
each false clause in `failing`" is unsatisfiable in a pre-r45 receipt schema,
so the vocabulary is only *claimed* for r45+ instruments.

### D14 — the r48 meaning classifiers reject the lane's own `met_target` phrasing
`tools/round-48/meanings.py:58` `SUCCESS = …\b(met|clean|ok|…)\b` does **not**
match `met_target` (`\b` fails inside a word). **Probe P4** (receipt
`p4-registry-audit`, sha in receipt; cell dump `p4-registry-cells.txt`):
**16 of 40 committed registry rows fail `meaning_classes`**, all on this
vocabulary seam:
- `0=met_target true …` (round-43/c1-counter.py) — `met_target` unread as success;
- `0=all three bindings true…`, `0=every … resolved`, `0=no control reaches n/n`,
  `0=ok, both carriers built`, `0=clean, both arms agree` — accurate prose with
  no token from SUCCESS (`met_target`, "resolved", "agree", "matched",
  "produced", "computed" are all outside the regexes);
- `1=never a verdict`, `1=not a verdict` (mk-l-carriers, c1-run.sh, gate.py) —
  honest "this tool never emits a not-met verdict" prose that trips the
  not-met-class check because it is *not* a not-met meaning;
- `2=…` for `heldout-gen-v4.py` — unevaluable phrased without a UNEVAL token.
This is *not* a counter bug — it is the exact registry repair the frozen
landing requirement names ("repairs every verdict map that does not carry its
meaning class"), but the L1 must reword 16 cells without losing the row's own
semantics (e.g. `gate.py`'s `1=not a verdict` row must become a not-met *class*
or be re-marked). The row text for `gate.py` is the sharpest: its real exit-1
meaning is "not a verdict — running gate.py as a script prints usage", which
the current prose already says; it fails only on token surface.

### D15 — `:` is not a segment separator in r48
`meanings.py:57` `SEG` accepts `0=` only; `registry.py:46` `EXITMAP` accepts
`0=` **or `0:`**. A registry row written `0: met; 1: not met; 2: error` passes
r46's thin check and is unparseable (`"does not parse as 0=;1=;2="`) under r48.
Minor, but it means r48 narrows the surface grammar of verdict maps; any future
row must use `=`.

## 3. Landing-evidence delta for the L1 (from the same audit)

- Registry rows in worktree `SKILL.md`: **40**; census2 paths at A2: **42**.
  Missing rows: `tools/round-48/meanings.py`, `tools/round-48/record2.py`.
  `extra`: none. `census_rederived_equal`: not re-measured here (the frozen
  counter checks it; `named_but_absent []` at A2).
- Craft section: 24 blocks, last is block 24; marker
  `<!-- verdict-meaning-table v1 -->` absent in worktree — block 25 is unlanded,
  consistent with a pre-landing measurement.
- `record2.py` floor on the frozen card (C2Floor's receipt, corroborating):
  exit 1 — round-47 section lacks a seat atom/re-derived seats correction,
  the `## Record corrections — round 48` section is absent, quote
  `exempted 2` unbacked. The landing requirement's named corrections
  (a `seats` correction for round 47, a `quote` correction for round 47's
  `exempted` cell) are exactly what the floor demands.

## 4. Stale `.pyc` contamination (search trap, not a defect)

`tools/round-47/__pycache__/record.cpython-314.pyc` and
`exact.cpython-314.pyc` still contain the string `frozen_path_changed` that the
sources lack — vocabulary greps that include bytecode files misreport
`record.py`/`exact.py` as freeze-gated. Excluded from the map above.

## 5. Probes run (receipts in `./receipts/`)

| probe | claim demonstrated | receipt |
|---|---|---|
| P1 meaning_classes vs EXITMAP | D10 + D14 (banana/swapped/met_target/not-a-verdict cells) | `p1-meaning-classes.json` sha b092168b… exit 0 |
| P2 CORR grammar | D5 (axes/quote inert in r47) | `p2-corr-grammar.json` sha 497f41fd… exit 0 |
| P3 digest scope | name-only vs name+body pin (r47 `exact.py:96` vs `meanings.py:129–138`) | `p3-digest-scope.json` sha e0a2e3f7… exit 0 |
| P4 registry audit | 42-census vs 40 rows, 16 meaning failures | `p4-registry-audit.json`, `p4-registry-cells.txt` sha 81d0e601… exit 0 |

The r48 `meanings.py` was executed **from the frozen bytes** materialized to
scratch (`git show ac02a79f:tools/round-48/meanings.py`), with only the
round-46 `gate` import path pre-seeded — matching how the counters exec their
oracles. No counter's `main()` was run against the lane; this was a vocabulary
and predicate-semantics scan, not a re-score.

## 6. Not run

- No `meanings.py`/`record2.py --root … --freeze … --rev …` claim scores (siblings
  own the measured runs; this seat's brief was the overlap scan).
- No mutation battery, no fixture `git init`, no selftest.
- No installs (none needed: system python 3.14 sufficed).

## 7. Risk notes for the L1

- The 16-cell meaning repair must preserve each row's own claim semantics:
  `0=no control reaches n/n so the kill rule does not fire` is a *success* class
  phrased negatively — forcing a `met` token in would read wrongly. Prefer
  appending a canonical class token (`0=ok — …`, `1=not met — …`,
  `2=could-not-evaluate — …`) over rewriting prose.
- `--freeze` arguments in receipts from other seats should use `ac02a79f` per the
  claims file's own re-derivation rule (`git log --format=%H -1 --
  plans/round-48-claims.md`); A1 receipts are still internally consistent but
  measure the pre-amendment counter source if the worktree were rolled back.
- `SEG` order-sensitivity (D15) and the missing `:` separator mean the two new
  rows for the r48 counters must use `0=…; 1=…; 2=…` with `=` only, digits in
  order.
