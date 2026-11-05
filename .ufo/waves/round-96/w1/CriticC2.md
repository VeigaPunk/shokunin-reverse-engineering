# CriticC2 — R96-C2 attack + block-34 non-author check (evidence summary)

Seat report; full detail in `.ufo/waves/round-96/w1/CriticC2/attack.md` (same dir holds 17
receipt JSONs). Lane tip measured: `3baac2ef4`. Pins verified: checker
`34cf6579d7d0614336add1710912877492c68517331736fa5e4021ffedf05340`, depth v2
`359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f`, depth v3
`bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f` — all match
`.ufo/waves/round-96/pins.sha256`. Checker `--selftest` rc 0. Block 35 absent at tip
(`grep -c kill-rule-gate-coverage SKILL.md` → 0), QUALITY ends at Row 192 — attacks therefore
ran against a draft faithful to the frozen predicate, spliced into a `git clone --shared`
scratch clone, `cp`-reset to tip bytes between variants.

## Method

Driver: python script in scratch ran, per variant:
`python3 -I -B <clone>/tools/round-93/craft-citation-semantic.py --root <clone> --manifest <M> --block 35 --worktree --json-out .ufo/waves/round-96/w1/CriticC2/receipts/<label>.json`
(depth counters analogously with `--worktree --expect-blocks 35 [--shape-from 35]`).
Drafts: block 35 with frozen marker + 4-row table (snippets exact, criteria 193/193/193/194)
+ draft QUALITY Rows 193/194 carrying exactly the frozen atoms. Scratch removed after copy.

## Attack results (all measured)

- control faithful draft vs `block35-after.json` → **rc 0** (`control-after.json`); junk
  manifest → **rc 1** on four keyword atoms (`control-junk.json`) — command-4 reproduced.
- **(a) opposite-rule criteria → rc 0** (`a-different-rule.json`): the checker never reads the
  criterion text; keywords bind only the cited QUALITY row. Named limit confirmed.
- **(b) rule-free criteria `see (QUALITY 193)` → rc 0** (`b-rule-free.json`): junk class the
  junk control cannot catch (it only catches keyword swaps).
- **(c) 194-row citing QUALITY 193 → rc 1** while vocabularies are disjoint
  (`c-wrong-row.json`), **rc 0** once the cited row also carries the 194 atoms
  (`c2-wrong-row-overlap.json`) — A5 residual confirmed as vocabulary-containment-only; the
  citation number is never validated directly. A/B transfer to the landing bytes (the frozen
  predicate guarantees the atoms); C2 transfers only if real Row 193 mentions 194's atoms.
- **(d) 3-row table → checker rc 1** (`row not found: 'green without a receipt'`, shape atom
  still true, `d-three-rows.json`) but **v2 rc 0 / v3 rc 0** (`required-shaped 1/1`,
  `d-v2-wt.json`/`d-v3-wt.json`): the 4th row is load-bearing through the frozen manifest
  only; the ≥3-row floor alone admits 3 rows. Decoy-table padding also passes v3 shape
  (`e-decoy-table.json` shape true + rc 1 via manifest; `e-v3-wt.json` rc 0) — `_table_rows`
  merges every `|` line of the block.
- rigidity: a criterion citing two rows is refused (rc 1, `names 2 QUALITY citations`,
  `f-two-citations.json`) — tradeoff, not a claim defect.
- tip before-side reproduced: v2/v3 `--expect-blocks 35` → rc 1 `blocks 34 resolved 34`
  (`tip-v2.json`, `tip-v3.json`).

## Round-95 planned (c): block 34 non-author check — 4 of 4 AGREE

At tip bytes: vocabulary re-run rc 0 (`b34-r95-manifest-tip.json`). Semantic verdicts:
`consistent label rewrite`→191 AGREE; `counts that do not recompute the label`→191 AGREE;
`revision field not the measured tree`→192 AGREE; `temp-file symlink escape`→192 AGREE —
each cited criterion's text states the rule its row asserts (reasons per row in attack.md §3).
Atom re-derivation (`grep -c -F`, file/row): `bound to the frozen expect label` 1/1;
`when met_target is true` 1/1; `recompute the label from its own counts` 1/1;
`full measured revision` 1 line (2 in-row); `git rev-parse` 1/2; `unique temporary name` 1/2;
`planted` 1/3.

## Verdict

No defect in the frozen R96-C2 claim: the vocabulary-plus-junk-control land is exactly what
measures, the named limit is real (now demonstrated with two concrete false-green classes +
the overlap case), block 34 passes the non-author check cleanly, no pins differ, no counter
bytes changed, no hidden regression found. Smallest safe successor correction (not this
round): make the checker require the criterion cell to restate ≥1 of its own row's keywords
(kills a and b) and make `table_shape` count only the snippet-carrying table (kills the
padding class).

## Files written (complete list)

Lane (allowed writes only): `.ufo/waves/round-96/w1/CriticC2/attack.md`;
`.ufo/waves/round-96/w1/CriticC2/receipts/{tip-v2,tip-v3,control-after,control-junk,control-v2-wt,control-v3-wt,a-different-rule,b-rule-free,c-wrong-row,c2-wrong-row-overlap,d-three-rows,d-v2-wt,d-v3-wt,e-decoy-table,e-v3-wt,f-two-citations,b34-r95-manifest-tip}.json` (17);
this report `.ufo/waves/round-96/w1/CriticC2.md`. Tracked lane files untouched
(`git diff --stat HEAD -- SKILL.md corpus/QUALITY.md tools/` empty). Scratch
`/fast/scratch/hyaku/kaidoku-r96/CriticC2` removed. No tools installed (none needed); no host
state changed; no mutating git command anywhere.
