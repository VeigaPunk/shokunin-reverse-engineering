# ConnCraft — craft-block lineage: 22 (round 45) → 23 (round 46) → 24 (round 47)

Seat `w1/ConnCraft`, round 47, lane `kaidoku`. Measured revision `f7d6e58d6e7f4e664bf443137c55ee08821de244`
(the last commit on which `SKILL.md`, `plans/round-47-claims.md` and `tools/round-47/` are byte-identical
to the tip I measured — `git diff --stat f7d6e58d HEAD -- SKILL.md tools/round-47/ plans/round-47-claims.md`
is empty at `09a9f912`). Declared freeze for the C1 counter: `f54b3b6d` (A6), not `5017e1f7`.
Lane tree read-only; every mutation was made on scratch copies. Receipts:
`.ufo/waves/round-47/w1/ConnCraft/receipts/` (`manifest.tsv` carries command, UTC, exit, stdout sha256).

## 1. What each block actually added

| block | round | surface | rows / cells | what it states | what it makes checkable | pins |
|---|---|---|---|---|---|---|
| 22 | 45 | `SKILL.md:547-611` (10 rows) | `trigger \| arm \| exit \| receipt` | the freeze gate's arms, and **the family's vacuity limit, disclosed**: "a table of structurally valid but empty rows would pass it" (`SKILL.md:605`); "the cases — not the registration — are the evidence" (`:601`) | nothing by itself — it is a statement of arms plus two disclosed limits | none |
| 23 | 46 | `SKILL.md:612-631` (13 rows) | `trigger \| v1 hole \| v2 arm \| exit` | each routed R45 defect, the v1 clause that let it pass, the v2 arm that fails it | `tools/round-46/attest.py` (the row→arm vocabulary, marker-scoped parsing, forgeries) | `attest.py` sha256 |
| 24 | 47 | `SKILL.md:632+` (4 rows) | `trigger \| v2 hole \| v3 arm \| exit` | four routed R46 defects, the loose v2 binding that passed a forgery, the v3 arm | `tools/round-47/exact.py` (9 clauses); battery 4 forgeries | `exact.py` sha256 + `mutations_sha256` |

Structural direction of the lineage: **10 rows → 13 rows → 4 rows** while the interpreter behind the block
grew from "arms stated" to a nine-clause predicate. Block 22 described an instrument; block 23 named the
holes in it; block 24 pinned the holes closed for four of them. The claimed surface (`SKILL.md` block 24)
is now a four-row pointer at a nine-clause counter: clauses 1–3 (marker/title, exact header, row/exit cells)
and clause 8 (line-selected citations, allow-list, sha pin) are enforced but **not disclosed in the block**;
block 23 did disclose its clause set, one row per routed defect.

## 2. Per-defect attribution (the seat's matrix)

| routed defect | first stated anywhere | first stated in a craft block | first made checkable | block 24 row | verdict |
|---|---|---|---|---|---|
| **R46-CL2** `blobberish` satisfies `blob` | `corpus/lessons/round-45.md:142-152` (R45-CL13(c): "header cells are substring tests (`"exit" in "no-exit-code"` passes)") — one round earlier, same class | block 23, `SKILL.md:620`: "every row names a routed id and an arm **from the fixed vocabulary**, so a garbage row fails" | block 24 / clause 5 (`a not in VOCAB`) + selftest `red-arm-substring` | row 1, `symbol` | **real move in the interpreter, dead weight in the block**: the row's text adds nothing to block 23's arm cell; the class is on its third statement (45-lesson → 23 → 24). Only the code changed (`in` over a lowercased cell → membership). |
| **R46-CL3** an id appears in *some* row | `corpus/lessons/round-46.md:60-62` | block 24 — block 23's text is per-row presence only (`SKILL.md:620`) and never states cardinality | block 24 / clause 4 (`len(ids) != 1`, `set(counts.values()) == {1}`) | row 2, `once` | **real move, prose and code.** The only row whose requirement has no ancestor statement in any block. |
| **R46-CL4** no digest over the mutation list | `corpus/lessons/round-46.md:21` (M46-2) | block 23, `SKILL.md:618` carries the weak form: "the mutation list **is named** in the claim" | block 24 / clause 6 (`MUT_DIGEST`) + clause 9 (`forgeries_total == 4` hardcoded) | row 3, `digest` | **real move — a strengthening of a stated-but-weak rule.** Partial: the digest covers names+order, not mutation bodies (already routed as R47-CL4). |
| **R46-CL6** one flag reorder blinds the history arm | `corpus/lessons/round-46.md:65-68` | block 24 — block 23's R45-CL6 row names the arm but never the order | block 24 / clause 7 (literal count in `tools/round-46/gate.py`) | row 4, `order` | **dead weight: guards a non-defect.** The stated harm does not reproduce (§3.1), and clause 7 is satisfiable by a source literal that the runtime never sends (§3.2). This is the only row in the table whose named defect cannot be shown to exist. |

Net: **one new requirement (`once`), one strengthening (`digest`), one restatement (`symbol`), one
non-defect (`order`).** Two of the four rows earn their place; one is bookkeeping; one is wrong.

## 3. Attack measurements (all on scratch copies; lane bytes unmodified)

Interpreter copy sha256 `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5`
(= block 24's `interpreter_sha256` pin at `f7d6e58d`); block copy `SKILL.md` sha256
`894e2864e5de8232fc0efe67c8b70169a0d858c6b36050ce9c275fce0ebffafd`. The driver imports
`score()` from that byte copy and feeds it the real bytes at the measured revision, so no clause is
re-implemented by hand.

### 3.1 The `order` row's harm does not exist (r6, r7)

Command: `python3 receipts/flagorder.py`, `python3 receipts/narrow.py` (both exit 0).
`gate.history_touched` is a **set union** over `git log --name-status -z --format=`; `-m` alone means
`--diff-merges=separate`, whose merge entry is the union of both parents' diffs, and
first-parent-diff ⊆ separate-diff. Reversal can therefore only **add** a path that some in-range commit
already names for a wide range, or that predates the range base for a narrow one — never lose one.

- `r6-flagorder-wide`: a conflicted merge whose first-parent and second-parent sides both differ;
  `correct_order == reversed_order == ["f.txt","g.txt"]`, `reversed_loses: []`.
- `r7-flagorder-narrow`: range base after the second parent's edit, resolution keeps the **first**
  parent's bytes; `correct_order ["z.txt"]`, `reversed_order ["h.txt","z.txt"]`,
  `reversed_adds ["h.txt"]`, `reversed_loses []`.

So block 24's row-4 hole cell — "prints a merge twice and **blinds the arm**", exit `1` — is false as
written for this counter: the reversed order over-reports (a fail-safe direction for a freeze gate) and
cannot produce the false clean the row claims to prevent. `R46-CL6`'s own text ("restores the very
blindness R45-CL6 was about") inherits the error: `-m` is not the fence-blind `--name-only` call that
R45-CL6 was about.

### 3.2 Clause 7 binds a literal, not the argv (r5, case 7)

`attack.py` case `clause7-literal-in-constant-runtime-reversed` edits the **gate.py copy** so that
`("-m", "--diff-merges=first-parent")` appears exactly once as a module constant and the call iterates
`*reversed(LOG_ORDER)`. Counts: `gate_order_literal 1`, `gate_order_reversed 0`; **v3 exit 0,
`failing []`** — while the executed argv is the reversed order. A clause that counts a byte pair over the
whole file cannot distinguish the constant from the call; this is the R46-CL7 class ("binds the digits,
not their meanings") reappearing inside the row that mints the `order` token.

### 3.3 Contentless rows pass both profiles (r5, cases 2–5) — confirms R47-CL10

| case | mutation of the landed block | v3 exit | v2 exit |
|---|---|---|---|
| `genuine-landed-block` | none | 0 | 0 |
| `hole-cells-contentless-dash` | every `v2 hole` cell → `` `-` `` | **0** | 0 |
| `hole-cells-empty` | every `v2 hole` cell → empty | **0** | 0 |
| `hole-echoes-arm-token` | every `v2 hole` cell → its own arm token | **0** | 0 |
| `hole-and-title-prose-contentless` | hole cells empty **and** the title's explanatory clause deleted | **0** | 0 |

Block 22 named exactly this at `SKILL.md:605` ("a table of structurally valid but empty rows would pass
it"), 27 lines above block 24. Block 23 converted that disclosure into a closure claim ("so a garbage row
fails"); block 24 does not restore it. Block 24 *does* disclose that it does not reach R46-CL7's registry
row (`corpus/lessons/round-46.md:89-95`, "this block does not reach it") — but the same class, applied to
its own four rows, is not disclosed and measures green. **The lineage lost a disclosed limit and never got
it back.** This is the round's calibration defect in craft terms: the block claims exactness for the cells
it binds and is silent about the ones it does not.

### 3.4 The denominator is pinned; the names are matched by containment (r5, case 6)

Clause 6's second half is `unnamed = [n for n in names if n not in block]` — a substring test over the
whole block, i.e. the R46-CL2 class the same block closes in clause 5. Case
`mutation-names-only-inside-cells` deletes the prose name list and leaves each name only inside a
`v2 hole` cell: **v3 exit 0**. Harmless in practice because `MUT_DIGEST` carries the real binding and
`forgeries_total == 4` is hardcoded, but it is a self-contradiction of the block's own title and it is the
same containment the block says it removed.

### 3.5 The battery's `once` forgery is arm-covering, not arm-isolating (r4)

`r4-c1-at-declared-freeze.json` (exit 0, `failing []`, battery 4/4/0/1/0) shows the shipped
`duplicate-routed-id` fixture failing on **two** clauses:
`rows 5 != 4` **and** `routed cardinality {...} != each ... exactly once`. The forgery inserts a fifth row,
so its red is jointly attributable to clause 3. A four-row duplicate (`attack.py` case
`duplicate-id-keeping-4-rows`) fails clause 4 **alone** — so the clause is isolated and only the *battery
case* is not. This is R45-CL15's "arm-covering but not arm-isolating" recurring one instrument later, in
the one place the round's own doctrine (block 22: "the cases — not the registration — are the evidence")
says to look.

## 4. Coverage of the routed set

Round 46 routed twelve defects (`corpus/lessons/round-46.md` `## Routed defects`). Block 24 addresses
four (CL2, CL3, CL4, CL6). Of the eight it does not address, three recur *inside the round-47 instrument*:

| routed defect not claimed | recurrence at `f7d6e58d` | receipt |
|---|---|---|
| R46-CL7 (HIGH) contentless row scores met | same class green on block 24's own rows (§3.3) | r5 |
| R46-CL8 bare `--selftest` exits 2 from argparse | `exact.py --selftest` → **exit 2**, usage error; with `--root/--freeze/--rev` → `cases=16 failures=0` | r2 / r1 |
| R46-CL1 (squash-invisible tamper) | unchanged, disclosed — no new evidence | — |
| R46-CL5 (registry `purpose` unchecked) | out of scope for this block | — |

The round lesson records R47-CL1..CL11; §3.1, §3.2 and §3.5 are not among them (CL6 is row→arm
permutation, CL7 is duplicate citations, CL10 is wrong-arm/`n/a`/exit-only). §3.3 confirms CL10
independently with different mutations (empty and echo cells, stripped title prose).

## 5. Contradictions stated, not smoothed

1. **Block 24's title vs clause 6.** "An instrument's binding is an equality, not a containment" — clause 5
   is an equality; clause 6's mutation-name check is a containment (§3.4). Both are in the same predicate.
2. **Block 22's disclosure vs block 24's scope.** Block 22 says this family's structural test passes empty
   rows; block 24 is that instrument and passes empty rows; block 24's text implies the four named holes
   are the residual risk. Both statements are in the same section, 27 lines apart.
3. **R46-CL6's harm vs the code.** The defect text says one reorder blinds the arm; measurement says the
   reorder widens the set. A craft block that carries a false `v2 hole` cell is worse than one that carries
   none, because the next round's `order` arm will be written against it.
4. **The freeze named in the brief vs the counter.** `--freeze 5017e1f7` exits 2 `frozen_path_changed`
   (`plans/round-47-claims.md`, `tools/round-47/`, `exact.py`, `record.py`); `--freeze f54b3b6d` exits 0.
   The C1 target is reachable only at the A6 freeze (already routed as R47-CL11; receipts r3/r4 confirm).

## 6. What the L1 should do with this (landing evidence, not a frozen-byte edit)

- **Cite the freeze that can be scored.** C1 landing evidence is `plans/round-47-claims.md@f54b3b6d`,
  `--rev f7d6e58d`, exit 0, `met_target true`, battery `4/4/0/1/0` (r4). Quoting `5017e1f7` as the
  measured freeze makes the counter exit 2 and no seat's claim can be admitted on it.
- **Do not rewrite block 24's bytes to fix §3.1/§3.3/§3.4.** Freeze discipline holds; the correct landing
  move is a *report-level* correction plus a round-48 route: (a) row 4's hole cell states a harm the code
  does not have, (b) the block does not disclose the contentlessness of its own rows that block 22 named,
  (c) clause 6's name check is containment. If the L1 prefers an amendment, it needs its own red-before
  receipts per the round's own rule (R47-CL5), and §3.1 is the receipt for (a).
- **The `symbol` row is safe to keep as-is** — it is the block's least informative row, but it is not
  false; the interpreter does what the row says. Do not spend an amendment on it.
- **Re-measure after any pin change.** `exact.py` has exactly two versions in the round (`git log --
  tools/round-47/exact.py`: `5017e1f7` `dcef54f1` → `f54b3b6d` `01a4bca7`), and the move invalidated the
  landed `interpreter_sha256` (M47-7). Any further amendment moves it again.

## 7. Verification run by this seat

All commands run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` under
`HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/ConnCraft`; every receipt is
`<stdout sha256> <exit> <UTC>` in `receipts/manifest.tsv`.

| id | command | exit | stdout sha256 |
|---|---|---|---|
| r1 | `python3 -I -B tools/round-47/exact.py --root <lane> --freeze f54b3b6d --rev f7d6e58d --selftest` | 0 | `0249b80f…` (`EXACT_SELFTEST: cases=16 failures=0`) |
| r2 | `python3 -I -B tools/round-47/exact.py --selftest` | 2 | `e3b0c442…` (argparse usage error) |
| r3 | `python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f7 --rev f7d6e58d --json-out …/r3-c1-at-first-freeze.json` | 2 | `e4d02214…` (`reason: frozen_path_changed`) |
| r4 | `… --freeze f54b3b6d --rev f7d6e58d --json-out …/r4-c1-at-declared-freeze.json` | 0 | `19891405…` (`met_target true`) |
| r5 | `python3 receipts/attack.py` (7 cases on scratch copies) | 0 | `0934990c…` |
| r6 | `python3 receipts/flagorder.py` | 0 | `c52d8c12…` |
| r7 | `python3 receipts/narrow.py` | 0 | `aa6fc68e…` |

Byte-copy identities: `exact.py` `01a4bca7…` (= block pin), `SKILL.md` `894e2864…`. No lane file was
written outside `.ufo/waves/round-47/w1/ConnCraft/`; no git mutation was run anywhere (fixture repos under
scratch only, each asserted with `git -C "$D" rev-parse --show-toplevel`); `/fast/scratch/hyaku/kaidoku-r47/ConnCraft`
was removed after the receipts were copied. Tool installs: none.

## 8. Verdict

Block 24 is **half a real move**. Against the ancestor's own standard it closes three of the four holes it
names — cardinality (`once`) genuinely new, the digest (`digest`) a real strengthening of a rule block 23
only stated weakly, and the arm-vocabulary equality (`symbol`) a real fix in code that restates block 23's
prose a third time. Its fourth row (`order`) guards a defect that does not exist, binds a source literal
instead of the argv, and inherits R46-CL6's false harm statement. And the block that was supposed to make
"a check exact" does not restore the one limit its own predecessor disclosed: a structurally valid but
empty row still scores exit 0 under both profiles. The lineage therefore gains exactness in the four
dimensions it enumerates and loses exactness-in-disclosure overall — which is the honest reading of a
depth claim that adds a matrix narrower than its interpreter.
