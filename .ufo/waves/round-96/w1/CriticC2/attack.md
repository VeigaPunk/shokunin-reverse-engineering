# CriticC2 — adversarial attack on R96-C2 (depth) + round-95 planned (c) non-author check of block 34

Seat: CriticC2 (critic), kaidoku round 96, attempt 1. Lane tip measured: `3baac2ef4`
(disclosed supersession commit). Block 35 absent at tip (`grep -c kill-rule-gate-coverage SKILL.md` → 0);
`corpus/QUALITY.md` ends at Row 192 (329 lines). All work in scratch clone
`/fast/scratch/hyaku/kaidoku-r96/CriticC2/clone` (`git clone --shared` of the lane); between
variants the clone's `SKILL.md`/`corpus/QUALITY.md` were `cp`-reset to tip bytes. Lane repo
untouched except this SEAT dir and the report file.

## 0. Instrument sanity (all green)

- Pins: sha256 of `craft-citation-semantic.py`, `depth-blocks-v2.py`, `depth-blocks-v3.py`
  in the clone = `34cf6579…`, `359f15e1…`, `bcf6c4ea…` — byte-identical to
  `.ufo/waves/round-96/pins.sha256`.
- `python3 -I -B tools/round-93/craft-citation-semantic.py --selftest --work <scratch>` → rc 0.
- Before-side reproduced at tip bytes: `depth-blocks-v2.py --root CL --worktree
  --expect-blocks 35` → rc 1, `blocks 34 resolved 34 expect 35`; `depth-blocks-v3.py …
  --shape-from 35` → rc 1 (receipts `receipts/tip-v2.json`, `receipts/tip-v3.json`).
- Junk control reproduced on the faithful draft: rc 1 on the four keyword atoms (below).

## 1. Draft basis (faithful control)

Because the landing has not happened, I drafted in the clone: block 35 carrying the frozen
marker `kill-rule-gate-coverage v1`, a 4-body-row/4-cell decision table whose first cells
contain the manifest's `row_snippet`s exactly, criteria citing QUALITY 193/193/193/194; plus
draft QUALITY Rows 193/194 containing exactly the atoms the frozen predicate requires (193:
`instrumented count`, `survives every exit-code diff`, `main()-level negative control`,
`receipt-content consistency check`; 194: `--json-out is mandatory`, `skipped
self-verification`). Drafts: scratch `drafts/block35-*.md`, `drafts/quality-*.md` (scratch
removed after; every draft is reproducible from this file).

## 2. Attack table (checker = `craft-citation-semantic.py --root CL --manifest M --block 35 --worktree`)

| id | draft | manifest | expected | measured rc | verdict | receipt |
|---|---|---|---|---|---|---|
| control | faithful | block35-after.json | 0 (control is checker-valid) | **0**, ok, shape true | draft valid — any later red is attributable to the attack, not the draft | `receipts/control-after.json` |
| control-junk | faithful | block35-junk.json | 1 (junk control fires) | **1**, four keyword atoms missing | command-4 semantics reproduced | `receipts/control-junk.json` |
| **A** (item a) | criteria state the OPPOSITE rule ("durability is advisory…", "a quiet green exit without any receipt is acceptable…") | block35-after.json | 0 — named limit | **0**, ok | **CONFIRMED false green**: every criterion asserts the rule the row refutes; the checker never reads the criterion text | `receipts/a-different-rule.json` |
| **B** (item b) | rule-free criteria `see (QUALITY 193/194)` | block35-after.json | 0 — junk the junk control does not catch | **0**, ok | **CONFIRMED**: a criterion that states nothing passes; the junk manifest only catches swapped keywords | `receipts/b-rule-free.json` |
| **C** (item c, disjoint vocab) | 194-row criterion cites QUALITY 193 | block35-after.json | 1 | **1**, `QUALITY 193 lacks ['--json-out is mandatory', 'skipped self-verification']` | caught **only because** 193's text lacks 194's atoms | `receipts/c-wrong-row.json` |
| **C2** (item c, overlap) | same wrong-row block; draft 193 also mentions `--json-out is mandatory` and `skipped self-verification` | block35-after.json | 0 — residual | **0**, ok | **CONFIRMED A5 residual**: the citation number itself is never validated; keyword containment in the cited row is the only rule — any vocabulary overlap defeats it | `receipts/c2-wrong-row-overlap.json` |
| **D** (item d) | 3-row table (4th row dropped) | block35-after.json | 1 via manifest; 0 via depth counters | checker **1** `row not found: 'green without a receipt'` (shape atom **true**); v2 **0** `blocks 35 resolved 35`; v3 **0** `required-shaped 1/1` | **the 4th row is load-bearing only through the frozen manifest; the ≥3-row floor alone admits the 3-row table** | `receipts/d-three-rows.json`, `receipts/d-v2-wt.json`, `receipts/d-v3-wt.json` |
| **E** (item d, shape floor) | decoy 3-row 4-cell table + only 2 real decision rows | block35-after.json | 1 via manifest; v3 0 | checker **1** (`row not found` ×2, shape atom **true**); v3 **0** `required-shaped 1/1` | **shape floor is padded by any table's rows** (`_table_rows` merges all `|` lines of the block); the frozen manifest blocks the false green for block 35 | `receipts/e-decoy-table.json`, `receipts/e-v3-wt.json` |
| F (rigidity) | each criterion cites two rows (`QUALITY 193 and QUALITY 194`) | block35-after.json | 1 (exact-one rule) | **1**, four `names 2 QUALITY citations, expected 1` | tradeoff, not a claim defect: a criterion legitimately citing two rows is refused; the block author must split criteria | `receipts/f-two-citations.json` |

Mechanism (from the pinned bytes): for each manifest row the checker finds exactly one body
row whose first cell contains `row_snippet`, regexes `QUALITY (\d+)` in the LAST cell
(exactly one), reads that QUALITY row's text, and requires every keyword verbatim **in the
cited QUALITY row's text**. The criterion cell's own words are never semantic inputs.

Transfer argument to the landing bytes: A and B are false greens for ANY rows that carry the
frozen atoms — the frozen predicate guarantees QUALITY 193/194 will carry them, so these two
demonstrations hold at the landing without further measurement. C2 transfers only if the real
landing Row 193 happens to mention 194's atoms (conditional; the real bytes do not exist yet).

## 3. Round-95 planned (c) — block 34 non-author check (lane tip bytes, no drafts)

Craft block 34 (`receipt-world-binding v1`, SKILL.md `:788`), criteria at tip: QUALITY 191
(line 327), 192 (line 329). Checker vocabulary re-run at tip bytes:
`--manifest .ufo/waves/round-95/manifests/block34-after.json --block 34 --worktree` → rc 0
(`receipts/b34-r95-manifest-tip.json`).

| block-34 row | cites | verdict | reason | atoms (row-line count / file `grep -c`) |
|---|---|---|---|---|
| consistent label rewrite | QUALITY 191 | **AGREE** | 191 states the exact rule: "when met_target is true the receipt's label must be bound to the frozen expect label the run was invoked with" | `bound to the frozen expect label` 1/1; `when met_target is true` 1/1 |
| counts that do not recompute the label | QUALITY 191 | **AGREE** | 191: "the label must recompute the label from its own counts … a label that outruns the counts it records is refused rather than believed" | `recompute the label from its own counts` 1/1 |
| revision field not the measured tree | QUALITY 192 | **AGREE** | 192: "the full measured revision resolved by git rev-parse … a short or truncated `--rev` never passes as that tree's identity" | `full measured revision` 2/1; `git rev-parse` 2/1 |
| temp-file symlink escape | QUALITY 192 | **AGREE** | 192: "unique temporary name created with mkstemp … a planted symlink standing at that name is neither read nor followed" | `unique temporary name` 2/1; `planted` 3/1 |

4 of 4 AGREE — block 34's cited criteria state the rules their rows assert; the vocabulary
green and the semantic reading agree. This is the check the checker itself cannot do (A/B are
its counterexamples), and it comes out clean for the round that built it.

## 4. Impacted axes and smallest safe correction

- coverage: the vocabulary gate (QUALITY 188 residual, disclosed as C2's named limit) is now
  demonstrated with two concrete false-green classes (A: opposite rule; B: no rule) plus the
  overlap-citation case (C2). No new undisclosed defect: the claim's named limit states
  exactly this, and the frozen junk manifest catches only the keyword-swap class.
- depth: block 34 = clean (4/4); block 35's 4th row is manifest-load-bearing, not
  counter-load-bearing; the shape floor is pad-able (E). Both are bounded by the frozen
  manifest — the manifest is the actual defense, the shape floor is decoration for this class.
- calibration: every attack has a measured rc and a receipt; nothing is claimed unrun.
- freshness: all measurements at tip bytes `3baac2ef4` (+ splices confined to the scratch clone).

Smallest safe correction (for a successor instrument, not this round — the checker is pinned
and the C2 kill rule does not require semantic checks): require the criterion cell to restate
at least one keyword atom of its own manifest row (kills A and B), and have `table_shape`
count only the table that carries the row snippets (kills E). Neither blocks the frozen
predicate; both are discernment work the wave already routes as the named limit.

## 5. Bounds compliance

Lane writes: this SEAT dir (`receipts/*.json`, this file) and `.ufo/waves/round-96/w1/CriticC2.md`
only. No git mutations anywhere (fixture rule respected; clone reset by `cp` from
scratch-preserved tip bytes). No host changes, no tool installs (none needed). Scratch
`/fast/scratch/hyaku/kaidoku-r96/CriticC2` removed after receipt copy.
