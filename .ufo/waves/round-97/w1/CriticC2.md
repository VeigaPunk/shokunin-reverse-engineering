# CriticC2 — adversarial attack on R97-C2 (craft block 36 and first-table depth)

Landing revision: 867ed98d85f45a18265441c1760386ef353b3d43 (clone under scratch, detached, toplevel verified).
Counters: `tools/round-97/craft-citation-v2.py` (craft, `--worktree --block 36 --manifest ...`) and
`tools/round-97/depth-blocks-v4.py` (depth, `--worktree --expect-blocks 36 --shape-from 36 --expect 'blocks 36, resolved 36, required-shaped 1/1'`).
Both were run with `python3 -I -B <absolute tool path>`, with `--json-out` into `.ufo/waves/round-97/w1/CriticC2/`.

Method: each variant is a copy of `SKILL.md` (block 36 altered only as named) in a scratch root with
`corpus/` symlinked to the clone; the manifest is the frozen `block36-after.json` unless the variant
rewrites it. Variants were built from the landing bytes, not from each other.

## Reproduction (C2 baseline)

| command | rc | label / verdict | agrees with L1 receipt |
|---|---|---|---|
| `craft-citation-v2.py --manifest block36-after.json --block 36 --rev 867ed98…` (frozen D) | 0 | ok | yes (`l1/scores/c2-block36-at-867ed98…json` exit 0) |
| `craft-citation-v2.py --manifest block36-junk.json --block 36 --rev 867ed98…` (frozen D, junk) | 1 | 4 rows criterion-not-restated | yes (`c2-block36-junk-…json` exit 1) |
| `depth-blocks-v4.py --rev 867ed98… --expect-blocks 36 --shape-from 36 --expect '…'` (frozen C) | 0 | blocks 36, resolved 36, required-shaped 1/1 | yes (`c2-depth-v4-…json`) |

Receipts: `.ufo/waves/round-97/w1/CriticC2/frozen/{D-after,D-junk,C}.json`. The L1 receipts were not overwritten.

## Variant table

rc columns are the exit codes of the two counters on the same variant. "pass" means both 0.

| variant | craft rc | depth rc | finding |
|---|---|---|---|
| base-after (landing, control) | 0 | 0 | reproduces frozen C and D |
| base-junkman (control) | 1 | 0 | craft refuses the junk manifest; depth never reads the manifest (expected: shape-only) |
| (a1) pins row criterion `QUALITY 196 (`byte-pin-not-bound`)`, frozen manifest | 1 | 0 | refused: `criterion-citation-mismatch:196!=195`. The frozen `expected_quality` defeats the wrong-rule citation. |
| (a2) every criterion cell bare `QUALITY 195/196`, no restated keyword | 0 | 0 | **PASS — hole.** Restatement is `k in "|".join(row)` over the whole row, so the signature/guard cells satisfy it. Criterion text is never checked beyond the `QUALITY N` number. The docstring's "criterion cell must restate" is not what runs. |
| (a3) no `expected_quality`, pins row cites 196 with its keyword | 1 | 0 | refused: `QUALITY 196 lacks ['git cat-file blob','byte-pin-not-bound']`. Keyword-in-cited-row is the real guard when expected is absent. |
| (a4) manifest row 0 keyword `met-not-typed` (a keyword of the neighbouring row 195 rule); criterion `QUALITY 195 (`met-not-typed`)` | 0 | 0 | **PASS — hole.** The keyword need only occur in the table row and in the cited QUALITY row; nothing requires it to belong to the snippet row's rule. "pins name bytes" is verified by a keyword of "met is not a real boolean". |
| (a5) manifest rewritten (`expected_quality` 196, keyword `uncaught exception`) for the pins row; criterion `QUALITY 196` | 0 | 0 | **PASS — depends on manifest custody.** `expected_quality` is authored in the same manifest, so an author who rewrites manifest and cell together passes both counters. Only `pins.sha256` (manifests pinned at lines 27-28) catches it, and neither counter reads pins. |
| (b1) four-cell junk table (`a | b | c` bodies, 3 rows) before the real table, prose lead-in between | 0 | 0 | **PASS — by design but content-blind.** Depth's first-table floor counts rows and cells, not content. Craft evaluates only the snippet table, so the decoy is ignored. A junk-first table satisfies `required-shaped 1/1`. |
| (b2) three-cell junk first table before the real table | 1 | 1 | refused by both (`table shape violated`; depth `resolved 35`). |
| (b3) four-cell junk first table with only 2 body rows, real table after | 0 | 1 | **disagreement.** Craft's shape reads all body rows across tables (>=3 total), depth reads the first table only (>=3). The pair refuses; a single counter would not. |
| (b4) separator-less pipe run `| x | y | z | w |` before the real table | 1 | 0 | **disagreement (reverse).** Craft's shape reads `tables[0]` and needs a separator; depth skips heads without a separator and reads the real table. The pair refuses. |
| (c0) prose only, no table (control) | 1 | 1 | refused by both; citations still resolve, shape absent |
| (c1) real table moved into a ```markdown fence after the Refs line (still block 36 to the parser) | 0 | 0 | **PASS — hole.** Both counters parse raw `|` lines inside code fences. A non-rendered table satisfies the rendered-table claim. Citation `corpus/knowledge/2026-11-05-r97-receipt-byte-binding.md:1` resolves. |
| (c2) same fence, but with a `- **37.` bullet inside it | 1 | 1 | refused: `blocks 37`, expect 36. The block boundary is enforced. |
| (d1) snippet `pins name bytes` duplicated as a fifth row of the same table | 2 | 0 | craft exit 2 (`row snippet matches 2 rows`). Exit 2 is not a pass for the frozen D gate. Depth does not consult snippets and passes. |
| (d2) same duplicate in a second table after the real table | 2 | 0 | same as d1: unevaluable path works; depth still passes. |

## Findings (ranked)

1. **Restatement is row-wide, not criterion-cell (a2).** `craft-citation-v2.py` line 195 tests
   `"|".join(row)`, which includes the class/signature/guard cells. The docstring's "criterion cell must
   restate" and the `criterion-not-restated` story are therefore untrue for a criterion cell that names
   only `QUALITY N`. Smallest correction: test `row[-1]` (the criterion cell) for keyword restatement.
   Evidence: `.ufo/waves/round-97/w1/CriticC2/a2-bare-citations.craft.json` (exit 0).
2. **Keywords are not bound to the snippet row's rule (a4).** Any keyword present in the table row and in the
   cited QUALITY row passes, including one from a neighbouring rule. Smallest correction: require the keyword
   to be in the snippet row's own cells (not the joined row) or pin `expected_quality` against the keyword's
   own QUALITY row. Evidence: `a4-foreign-keyword-cited-195.craft.json` (exit 0).
3. **Manifest custody is outside both counters (a5, c-class).** `expected_quality` is trusted from the
   manifest; the counters never verify `pins.sha256` for the manifest they read. A rewritten manifest with a
   matching cell passes. Smallest correction: have the counter refuse a manifest whose sha256 differs from
   the frozen pin, or keep the manifest in the claims freeze. Evidence: `a5-manifest-rebound-to-196.craft.json` (exit 0).
4. **Depth shape is content-blind for a first table (b1).** A four-cell junk table in front of the real
   table satisfies `required-shaped 1/1`. This matches the v4 design (first table only); the protection is
   the craft counter's snippet check, which the junk table does not touch. Not a regression, but the depth
   label alone does not prove a meaningful table. Evidence: `b1-junk4x3-before-real.depth.json` (exit 0).
5. **Rendered-table claim is not checked (c1).** A table inside a code fence counts for both counters.
   Smallest correction: skip `|` lines that sit inside a fenced block in `_tables`/`first_table`.
   Evidence: `c1-table-in-second-fence.depth.json` (exit 0).
6. **Counter disagreement on first-table shape (b3, b4).** Craft and depth read "first table" differently
   (craft: `tables[0]` with separator, depth: first header-with-separator). The joint gate refuses both, but
   they should agree before either is trusted alone.

Not a hole: wrong-rule citations under the frozen manifest (a1, a3), prose-only (c0), block-splitting fence (c2),
junk-cell count (b2), duplicate snippet (d1, d2 -> exit 2).

## Limits

- No subagents, no REA call, no edits to frozen paths. Variants were built in scratch and not committed.
- Each variant was run once; the counters are deterministic over the same bytes.
- Tools installed: none. Scratch removed on exit.
