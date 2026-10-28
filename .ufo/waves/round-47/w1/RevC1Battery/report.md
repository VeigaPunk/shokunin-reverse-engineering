# RevC1Battery — attack on the R47-C1 battery (round 47, wave 1)

Seat `RevC1Battery`, lane `kaidoku` @ `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read-only on the lane tree: every run below either read committed objects or ran inside a
git fixture I created under `/fast/scratch/hyaku/kaidoku-r47/RevC1Battery/` (reaped after the
receipts were copied to `.ufo/waves/round-47/w1/RevC1Battery/receipts/`). Nothing was
installed (no pacman/uv/npx/official binary); all runs are `python3 -I -B`, stdlib only.

## 0. Verdict

1. **The four forgeries ARE built from the landed block.** Not hand-written: `run_battery`
   re-reads `SKILL.md` at `--rev` (`exact.py:334-337`), takes the marked block, and applies
   each mutation to it; the four fixture `SKILL.md` files are byte-identical to the landed
   file outside the block, and `flag-order-drift` changes zero SKILL.md lines (it mutates the
   fixture's `tools/round-46/gate.py` copy only). Provenance is clean — see §2.
2. **`forgeries_total == 4` is not a real denominator.** It is the number of loop iterations
   over `MUTATIONS` — *attempts*, not discriminating forgeries, and not four distinct defect
   classes. A neutered mutation body is counted as a *passing* forgery (F1), and four entries
   with three distinct names pass (F2/F3). See §3.
3. **Two frozen-clause defects and one over-claim.** F1 (the no-op branch launders a
   non-forgery), F2 (`duplicate-routed-id` is two defect classes at once, so the `once` arm's
   evidence is confounded and clause 4 can be deleted undetected), F3 (`order` arm deletable
   together with its mutation). F4 is a latent false red: clause 9's fixture file set is
   narrower than clause 8's allowlist. The landed counter's *direct* clause-4 and clause-7
   enforcement is correct (T6a, baseline receipt); what is lost is the battery's
   regression-detection value and clause 9's "one defect class at a time" claim.

## 1. Bytes tested

| artefact | revision | sha256 |
|---|---|---|
| `tools/round-47/exact.py` | identical at `5017e1f` (freeze) and `1e2c310` (tip) | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` |
| `SKILL.md` block 24 | `1e2c310:SKILL.md` | file `bf94d1b53a255d2e7bf50b0516ff679b3cd1e63e4e9b573d9fac5b54c3a3fae8` |
| draft snapshot used to build every fixture | `$S/draft-SKILL.md` | `bf94d1b5…` — **byte-identical to `1e2c310:SKILL.md`**, so every fixture below mutates the *landed* block |
| `plans/round-47-claims.md` C1 predicate | `1e2c310` | lines 106-110 unchanged since the freeze (`git diff 5017e1f..HEAD` removes no line) |

Revisions: original freeze `5017e1f7299c3a812e87e7950148f54313dd279e`, declared freeze after
A1 `9018c53b`, after A2 `62e33f7dd75c8e3285967b26419842c106f6c965`, landing `e856beb5`, tip at
measurement `1e2c3102952dc636650095643c1963c833859019`. The C1 instrument is unchanged by A1/A2
(`record.py` and the claims text only), so the attack applies to the frozen bytes.

Attack matrix (full receipts in `receipts/`, manifest in `manifest.md`):

| # | what the attacker changed | exit | battery forg/v2/v3/genuine/crash | verdict |
|---|---|---|---|---|
| T0 | nothing (control) | 0 | 4/4/0/1/0 | claim met |
| **T1** | one mutation **body** → `return block, {}` | **0** | **4/4/0/1/0** | **claim met with a non-forgery** |
| **T2** | drop `flag-order-drift`, add `substring-arm` twice | **0** | **4/4/0/1/0** | **claim met, 3 distinct classes** |
| **T2b** | T2 **+ clause 7 deleted from the counter** | **0** | **4/4/0/1/0** | **`order` arm unbound** |
| **T3** | clause 4 deleted from the counter | **0** | **4/4/0/1/0** | **`once` arm unbound** |
| T4 | `MUTATIONS` shrunk to 3, pin re-derived | 1 | 3/3/0/1/0 | caught: `forgeries_total 3 != 4` |
| T5 | block cites `corpus/knowledge/probe-r47.md:2` | 1 | 4/0/0/0/0 | false red (F4) |
| **T6a** | 4-row block, `R46-CL2` twice, `R46-CL3` dropped, **real counter** | **1** | n/a | clause 4 fires alone |
| **T6b** | same block, **T3's clause-4-deleted counter** | **0** | **4/4/0/1/0** | **battery certifies a blind counter** |
| T7 | a mutation raises | 2 | n/a | caught: could-not-evaluate |
| T8 | a mutation changes only non-graded prose | 1 | 4/4/1/1/0 | caught: `v3_green 1 != 0` |

The counter never sees `SCORECARD.md`; fixtures contain `SKILL.md`, `plans/round-47-claims.md`,
`tools/round-47/exact.py`, `tools/round-46/gate.py`, `corpus/lessons/round-46.md`,
`corpus/lessons/round-45.md`.

## 2. Q1 — are the four forgeries built from the landed block? YES

Method: I loaded the frozen `exact.py` in-process from the T0 lane, replaced `_repo` with a
spy that records the `files` dict it is handed, and ran the real `run_battery` at the T0 rev.
Then, for each fixture, I compared the forged `SKILL.md` against `git show <rev>:SKILL.md`:

```
substring-arm              outside_block_identical=True changed_lines=9   (4 table rows rewritten)
duplicate-routed-id        outside_block_identical=True changed_lines=2   (one inserted row)
stale-mutations-digest     outside_block_identical=True changed_lines=2   (digest hex only)
flag-order-drift           outside_block_identical=True changed_lines=0   (gate.py copy only)
forgeries_total 4  v2 4  v3 0
```

`text.startswith(pre) and text.endswith(post)` held for all four, where `(pre, post)` is the
landed file split around the marked block. The landed block is re-parsed from the rev
(`exact.py:334-337`), not synthesised; the only hand-written block in the tree is
`selftest`'s `good_block()`, which the claim does not measure.

Two caveats on provenance, neither exploited by the landing:

- the fixture is written with `skill.replace(block, text, 1)` (`exact.py:359`) — first
  occurrence. If the same block text ever appears earlier in `SKILL.md` (a quoted copy), the
  mutation would land on the quote and the graded block would stay genuine; the battery would
  then report `v3_green 1` and the claim would fail *red*, not green. Not a hole, a
  brittle failure.
- `_fixture_files` (`exact.py:322-328`) copies a fixed six-path set, not the union of cited
  paths — see F4.

## 3. Q2 — is `forgeries_total == 4` a real denominator? NO

It counts attempts. Two independent demonstrations:

**T1 — a mutation that mutates nothing is scored as a discriminating forgery.** Patch
(fixture `T1-noop-mutation-body`, recipe in `scripts/attack.py`):

```diff
 def _m_substring_arm(block, spec):
-    rows = [r[:2] + ["order-ish"] + r[3:] for r in _rows(block)]
-    return rewrite_rows(block, rows), {}
+    return block, {}
```

The name list and therefore `MUT_DIGEST` (`exact.py:96`, sha256 over *names* only) are
unchanged, so the block's `mutations_sha256` pin still matches. The no-op branch
(`exact.py:353-357`) then does `forgeries_total += 1` **and** `v2_green += 1`, and `continue`s
before `v3_green` is ever incremented:

```python
        if text == block and not overrides:
            out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
            out["forgeries_total"] += 1
            out["v2_green"] += 1          # <- counted as v2-discriminating ...
            continue                       # ... and never scored under v3
```

Receipt `receipts/T1-noop-mutation-body.json`: exit **0**, `met_target true`,
`battery 4/4/0/1/0`, and `fixtures[0] = {"name": "substring-arm", "error": "mutation was a
no-op"}` — a met claim carrying its own record that one of its four forgeries does not exist.
The asymmetric twin in the *same freeze* proves the intent was the opposite: `record.py:406-410`
(the C2 battery) records a no-op and increments `forgeries_green += 1`, i.e. red. C1's branch
increments the *green* counter and skips the red one. This is also the exact defect A2's
disclosure names for C2 ("the 'forgery' was a no-op"); in C1 it is silent.

**T2 / T2b — four entries, three distinct classes.** `MUTATIONS` becomes
`[substring-arm, duplicate-routed-id, stale-mutations-digest, substring-arm]` (the
`flag-order-drift` line replaced by a second `substring-arm`), with the block re-pinned to the
new names digest. Receipt `receipts/T2-dup-name-4-entries.json`: exit **0**, battery
**4/4/0/1/0**, fixture names `['substring-arm','duplicate-routed-id','stale-mutations-digest',
'substring-arm']`. The pin cannot see this: it is sha256 over the name *list*, and the block
still names all four strings (the prose keeps `flag-order-drift`), so clause 6's "names all
four mutation names" also passes.

T2b additionally deletes the whole clause-7 block from `score()` (the `gate_order_*` checks,
`exact.py:256-264`). Receipt `receipts/T2b-dup-name-clause7-deleted.json`: exit **0**,
battery 4/4/0/1/0, and the receipt carries **no** `gate_order_literal` key — the arm is gone
from the code and nothing in the claim notices.

## 4. Findings

### F1 (HIGH) — the battery's no-op branch makes a non-forgery count as a pass

- Fixture: `/fast/scratch/hyaku/kaidoku-r47/RevC1Battery/T1-noop-mutation-body` (rebuild:
  `scripts/attack.py`, case `T1-noop-mutation-body`), freeze `a1fbcce9dcaf`, rev `092a671bbe88`.
- Command:
  `HYAKU_SCRATCH=$S python3 -I -B tools/round-47/exact.py --root $S/T1-noop-mutation-body --freeze a1fbcce9dcaf --rev 092a671bbe88 --json-out $S/T1-noop-mutation-body/.ufo/receipts/T1-noop-mutation-body.json`
- Exit **0**, `"met_target": true`, `battery {"forgeries_total": 4, "v2_green": 4,
  "v3_green": 0, "genuine_green": 1, "crash": 0}`, `fixtures[0].error = "mutation was a no-op"`.
- Consequence: clause 9 is satisfiable by an instrument that never exercises the
  `substring-arm` hole. The digest pin cannot close this because it covers names, not bodies
  (`exact.py:96`).
- What the claim would have to say: either `forgeries_total` counts *discriminating* forgeries
  (a no-op must increment `v3_green` or `crash`, never `v2_green` — `record.py:409` shows the
  convention), or clause 9 must admit that it counts attempts. As frozen, clause 9 asserts a
  property the code does not enforce. **The bytes are frozen; this is a landing-time honesty
  item, not an edit request** (editing `exact.py` makes both counters exit 2
  `frozen_path_changed`).

### F2 (HIGH) — `duplicate-routed-id` is two defect classes; the `once` arm has no isolating evidence

- The forgery inserts a fifth row (`exact.py:76`: `rows.insert(2, ["R46-CL2", "a duplicate
  trigger cell", "order", "1"])`). The landed baseline receipt
  (`receipts/T0-baseline.json`) records two failing clauses for it:
  `["rows 5 != 4", "routed cardinality {'R46-CL2': 2, 'R46-CL3': 1, 'R46-CL4': 1,
  'R46-CL6': 1} != each of [...] exactly once"]`. Clause 9 says each forgery is scored "one
  defect class at a time" (`plans/round-47-claims.md:106-110`); this one violates the row-count
  clause **and** the cardinality clause, so its red is not evidence for the `once` arm.
- Consequence, demonstrated end-to-end: build a block that violates **only** clause 4 — four
  rows, every row naming exactly one id, `R46-CL2` twice and `R46-CL3` dropped — and score it
  with the real counter and with a counter that has clause 4 deleted
  (`exact.py:224-233` replaced by a comment; the v2 `else` removed too).
  - Fixture `T6a-dup-id-block-real-counter` (freeze `a58e416da115`, rev `3b9ad0a477d3`):
    exit **1**, `failing == ["routed cardinality {'R46-CL2': 2, 'R46-CL4': 1, 'R46-CL6': 1}
    != each of ['R46-CL2','R46-CL3','R46-CL4','R46-CL6'] exactly once"]` — clause 4 *does*
    work on the block.
  - Fixture `T6b-dup-id-block-clause4-deleted` (freeze `8a0510434f54`, rev `ffaa3f1d505b`):
    **exit 0**, battery **4/4/0/1/0**, `failing == []` — the battery certifies a counter that
    cannot see the `once` defect.
  - Fixture `T3-clause4-deleted` (freeze `eb94e09aa6c9`, rev `512f12cf9879`), genuine block:
    **exit 0**, battery 4/4/0/1/0. Nothing in the claim refers to clause 4's enforcement.
- What the claim would have to say: clause 9's "one defect class at a time" is false for
  `duplicate-routed-id`, and clause 4 has no binding evidence. Either the forgery substitutes
  an id inside four rows (the T6a shape), or clause 9 must not claim isolating evidence for
  the `once` arm.

### F3 (HIGH) — the `order` arm is contemporary with its mutation, so both can be removed together

- Fixtures `T2-dup-name-4-entries` (freeze `53224b71c85f`, rev `7ff8d959e59f`) and
  `T2b-dup-name-clause7-deleted` (freeze `6afd5e1fc176`, rev `2a5c1cf97638`); both exit **0**
  with battery 4/4/0/1/0.
- Consequence: clause 7 (`gate.py` flag order) and its forgery are not independent evidence:
  drop the mutation, duplicate another name to keep the count at four, delete clause 7, and
  the claim still reads met. The digest pin cannot see it (names, not bodies/distinctness) and
  the "names all four mutation names" check cannot see it (the prose still names
  `flag-order-drift`).
- What the claim would have to say: `forgeries_total == 4` needs a distinctness requirement
  over names (`len(set(names)) == 4`) or a body pin, otherwise it is an attempt counter.

### F4 (MEDIUM) — clause 9's fixture set is narrower than clause 8's allowlist (false red)

- Clause 8 accepts citations inside `corpus/lessons/`, `corpus/knowledge/`, `plans/`,
  `tools/round-47/` (`plans/round-47-claims.md:83`). `_fixture_files` (`exact.py:322-328`)
  copies only `SKILL.md`, `plans/round-47-claims.md`, `tools/round-47/exact.py`,
  `tools/round-46/gate.py`, `corpus/lessons/round-46.md`, `corpus/lessons/round-45.md`.
- Fixture `T5-citation-outside-fixture-set` (freeze `1e6002e22379`, rev `5683c03e00aa`): the
  block adds `corpus/knowledge/probe-r47.md:2` (file present at the rev in the fixture lane).
  The *real* score is green — `unresolved_citations []`, `refs 9`, `cited` includes
  `corpus/knowledge/probe-r47.md` — yet the run **exits 1** with
  `["battery v2_green 0 != 4", "battery genuine_green 0 != 1"]`, because every forged fixture
  is missing that file and so is the genuine fixture.
- Consequence: any legitimate block citing a `corpus/knowledge/` entry, `SCORECARD.md`-free
  but allowlisted, or any second `tools/round-47/*.py` (e.g. `record.py`) fails clause 9 while
  satisfying clause 8. The landed block cites only `round-46.md`/`claims.md`/`exact.py`, so
  the landing is unaffected — but the constraint is undisclosed, and any later re-pin of
  block 24's citations trips it.
- What the claim would have to say: clause 8 must state that citations are confined to the
  battery's six paths, or `_fixture_files` must fetch the union of cited paths.

### Honest negatives — what the battery does catch

- **T4** (`T4-shrunk-3-mutations`, freeze `daeb88e790e0`, rev `a7e5cce98cbd`): `MUTATIONS`
  reduced to three entries with the block's `mutations_sha256` re-derived by the attacker →
  exit **1**, `["battery forgeries_total 3 != 4", "battery v2_green 3 != 4"]`. A pure *shrink*
  is caught, by the count and by `v2_green`, even when the pin is re-derived.
- **T7** (`T7-mutation-raises`, freeze `4fe4fde36fa2`, rev `926ebbd87f59`): a mutation that
  raises → exit **2**, `unhandled RuntimeError: boom`; a crashing battery can never be
  laundered into a met claim.
- **T8** (`T8-cosmetic-change`, freeze `f63228bb6d8c`, rev `26cc35bb56f4`): a mutation that
  changes only non-graded prose → exit **1**, `["battery v3_green 1 != 0"]`. A change that
  does not break the block is correctly rejected; the F1 hole is narrow (block returned
  unchanged **and** no overrides) but real.

## 5. Landing state (as measured at `1e2c310`, 2026-10-28T~14:55Z)

- `python3 -I -B tools/round-47/exact.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin
  --freeze 1e2c310 --rev 1e2c310` → exit **0**, `failing []`, `met_target true`,
  `rows 4`, `rule_blocks 24`, battery **4/4/0/1/0**; stdout sha256
  `98ef390e1c1a3eaa1e0d2b9f3a9c635a4870c257b2cdebad4c4a87497616ea6d`
  (`receipts/landing-c1.json`). Every one of my nine fixture runs reproduces this shape on the
  same block bytes.
- **Freeze arm is vacuous in that measurement and every non-vacuous freeze exits 2.**
  `--freeze 5017e1f --rev 1e2c310` → exit **2** `frozen_path_changed`, `restored
  ["tools/round-47/record.py"]`, `touched ["plans/round-47-claims.md",
  "tools/round-47/record.py"]`. `--freeze 62e33f7d (A2) --rev 1e2c310` → exit **2**
  `frozen_path_changed` (`tools/round-47/record.py` restored). Only `freeze == rev` scores,
  and there `frozen_path_changed []`, `touched 0` are structural, not evidence that frozen
  bytes held. L1 should cite the amendment series (claims A1/A2) as the reason, and should not
  present `frozen_path_changed: []` at `freeze == rev` as a freeze integrity result.
- **Cross-instrument coupling through the frozen set.** `freeze_state` derives the set from
  the claims file's `## Frozen paths (exact)` (`plans/round-47-claims.md` + `tools/round-47/`),
  so an uncommitted or committed edit to **C2's** `record.py` makes **C1** exit 2
  (`frozen_worktree_dirty` / `frozen_path_changed`). The claims' "causal separability"
  paragraph is about *reads* and holds; landing order is still: commit both instruments, then
  measure. At the time of my first probe the worktree carried ` M tools/round-47/record.py`
  and C1's verdict was exit 2, not exit 1 — worth knowing before any seat reports "C1 red".

## 6. Residual risk and verification gaps

- **Not run:** a deep attack on the C2 battery (`record.py`). One cross-check only, by reading
  `record.py:399-416`: its no-op branch increments `forgeries_green` (red), the opposite of
  C1's, so F1 is C1-specific. C2's `wrong_total`/`non_empty` forgeries also return the card
  unchanged when their regex misses (`record.py:417-430`), which is a *false red* of the same
  family as F4 — unverified by execution, out of this seat's scope.
- **Not run:** the `skill.replace(block, text, 1)` first-occurrence hazard (§2) and a
  multi-table block (`_table_span` merges every `|` line in the block into one table).
- **Residual:** the `--freeze` argument is caller-supplied; `blob_changed`/`history_touched`
  only bind if the caller names a freeze distinct from `--rev`, and §5 shows no such pair
  scores in this round. The freeze integrity of C1 therefore rests on the claims file's
  disclosure of the A1/A2 series, not on an executed arm.
- **Residual:** F1–F3 are latent in the landed instrument (the four real mutations do
  discriminate; T0 shows 9/2/2/0 changed lines respectively). They degrade clause 9's
  *evidence*, not the block predicate: T6a, the baseline `gate_order_literal 1 / reversed 0`,
  the digest pin and the arm-token equality all fire correctly on the landed bytes.

## 7. Reproduction

Scratch `/fast/scratch/hyaku/kaidoku-r47/RevC1Battery` is reaped per contract; the fixtures
are rebuilt deterministically by `scripts/attack.py` (T0–T5), `scripts/t6.py` (the isolating
pair) and `scripts/t78.py` (the negatives) against
`$S/draft-SKILL.md` = `git show 1e2c310:SKILL.md` and
`$S/exact.py` = `git show 5017e1f:tools/round-47/exact.py`. Each lane is
`git archive <freeze> plans/round-47-claims.md tools/round-47 tools/round-46
corpus/lessons/round-46.md corpus/lessons/round-45.md SKILL.md | tar -x`, one poisoned
`exact.py`, one commit as freeze, `SKILL.md` with the block and its re-derived
`interpreter_sha256` as the second commit, `--show-toplevel` asserted equal to the lane,
`HYAKU_SCRATCH` set, then the counting command above with `--root <lane> --freeze <c1>
--rev <c2>`. Receipts: `receipts/*.json` (full counter receipt + exact argv + exit + UTC +
stdout sha256), index in `manifest.md`.

## 8. Sources

- `plans/round-47-claims.md:106-110` (C1 clause 9, "one defect class at a time"), `:83`
  (clause 8 allowlist).
- `tools/round-47/exact.py` @ `5017e1f`: `:96` (name-only digest), `:76` (row insertion),
  `:322-328` (`_fixture_files`), `:334-337` (block parsed from the rev), `:353-357` (no-op
  branch), `:359` (first-occurrence replace), `:224-233` (clause 4), `:256-264` (clause 7).
- `tools/round-47/record.py` @ `5017e1f`: `:399-416` (C2's no-op counts red).
- `tools/round-46/gate.py`: `:132-141` (`dirty`), :144-194 (`freeze_state`, `restored`).
- Lane commits: `5017e1f` freeze, `9018c53b` A1, `62e33f7d` A2, `e856beb5` landing,
  `1e2c310` tip at measurement.
