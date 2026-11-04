# R68-V1 — the round-68 knowledge entry's missing line-start provenance trio

## Live state: landed and committed at `5ee94c56` — do not append this block

The landing commit `5ee94c56ce7490938ee38c2e5c10930a1fd1330a` (2026-11-03 23:44:58 -0300, "round-69
landing: … the six r68 repairs …") carries a correction block at
`corpus/knowledge/2026-11-03-r68-packed-elf-route.md:82-101` (entry sha256
`6fe62359de3361ee3c9a2b0491667cf67df355181da7bf638847c2a6460d9612`, 101 lines; the live worktree bytes
are identical), opened
`## Correction — round 69 (appended 2026-11-03; the filed text above is not rewritten)`. It supplies
the trio in the shape `QUALITY.md` #101/#112 require, as three backticked list items:

```
$ grep -cE '^- `(source|verified-at|recheck):`' corpus/knowledge/2026-11-03-r68-packed-elf-route.md
3
```

So R68-V1's structural requirement is met in the worktree. **Do not append the block below** — a
second correction section would duplicate the heading and the trio. The block is retained here as
(a) the exact text this seat drafted before the landing, (b) the fuller variant if the L1 decides the
landed `verified-at:` / `recheck:` cells are too thin (the landed ones name only the landing commit and
"the two frozen counters", not the carrier pins), and (c) the record of the check design
(`evidence/v1-trio.txt`).

Two precision notes on the landed block: its three fields are list items, so the *backticked* grep above
counts 3 while the unanchored occurrence count is higher (`grep -c 'recheck:'` = 4) and the line-start
field grep stays 0 — that is the QUALITY #101 distinction ("a receipt that checks such a field greps
unanchored and states that the count is occurrence-based, not line-anchored"), not a defect. And the
landed paragraph at lines 99-101 additionally states that S269 is *not* superseded — that claim is the
branch conflict reported in `v5-supersede-row.md`; if the L1 lands the S271 row, that paragraph needs
its own appended correction, because it would be false.

## The original target (before the landing)

Target: `corpus/knowledge/2026-11-03-r68-packed-elf-route.md`, HEAD bytes
sha256 `00f1a03a7074b3507cbd1f40e31e9ed2a10b8bf07bb388f87d066c04943c5696`, 80 lines
(`git show HEAD:corpus/knowledge/2026-11-03-r68-packed-elf-route.md | sha256sum`; HEAD =
`3f3d20fc065b5be62f676028b9a38d316ddfe8fd`). The live worktree has since gained the landed
correction block and now hashes `6fe62359…` at 101 lines.

## Why the block, not an edit

`QUALITY.md` #112 (and #101 for the correction shape) and `CORPUS.md` §"Rules added from the kaika campaign" (first bullet) make the
provenance trio a property of a new entry's opening lines; a filed entry is corrected by an appended
block, never by rewriting its opening. The shipped precedent is
`corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md:49`
(`## Correction — 2026-11-03, round 68 (appended, never an in-place rewrite; QUALITY #65 and #100)`),
and `corpus/knowledge/2026-10-31-r53-triage-v6-reader-census.md:102-119` shows the same shape for a
missing `verified-at:`/`recheck:` pair.

## Insertion point

Append at end of file, after line 80, separated by exactly one blank line. Nothing above line 80 is
touched. After the append the file has 1 added section and 0 changed lines.

## Exact block (paste verbatim)

~~~markdown
## Correction — round 69

This block is appended, not an in-place rewrite: the bold `**Source:**` prose at line 3 stays as filed
(QUALITY #112; #101 for shape). It records the repair of routed defect R68-V1 in
`corpus/lessons/round-68-verifier-spotcheck.md` §5. The entry opened without the line-start provenance
trio `source:` / `verified-at:` / `recheck:`, so `CORPUS.md` §"Rules added from the kaika campaign"
(first bullet) and the corpus freshness sweep could not read it: `grep -nE
'^(source|verified-at|recheck):'` on the filed entry returns no line.

- `source:` S269 — UPX 5.2.0 documentation, `doc/upx-doc.txt` at tag `v5.2.0`,
  https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt; re-fetched 2026-11-03 for this
  block: HTTP 200, 37 208 B, sha256
  `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`, equal to S269's pin. Anchor:
  `NOTES FOR LINUX/ELF386` (heading at fetched-bytes line 433), quote at lines 441-442. Secondary
  locators as filed: the general Linux section at lines 383-384, `--exact` at lines 101-106.
- `verified-at:` 2026-11-03 (round 68) — [observation] `jq` over
  `.ufo/waves/round-68/l1/scores/c2-at-landing.json` reads `rev
  978436bdc5331ec50d8683eebf55457badfade0a`, `instrument.sha256
  48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e`, `carriers_matched 2`,
  `target 2`, `control_ok true`, `failing []`, `met_target true`, and both carrier pins
  `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` and
  `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` occur in its bytes.
  [observation] The round-68 closure records that it re-derived the two carrier pins, the two packed
  sha256 values and the byte-identical round trip on 2026-11-04
  (`corpus/lessons/round-68-verifier-spotcheck.md` §2, "re-measured"). The entry's claim numbers are
  the receipt's; this block adds no new measurement.
- `recheck:` 180d (S269's cadence) — re-run `python3 -I -B tools/round-68/packed-elf.py --selftest`
  (expect 13 cases, exit 0), re-hash `/usr/bin/jq` and `/usr/bin/xxd` against the two pins above, and
  re-fetch the pinned manual requiring sha256
  `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42`.

The quote's word-count label is corrected separately by S271, whose `teaches` opens
`supersedes S269 — ` (round-68 closure R68-V5).
~~~

## Checks behind the block

- trio absent: `grep -nE '^(source|verified-at|recheck):' corpus/knowledge/2026-11-03-r68-packed-elf-route.md` → no output (exit 1).
- source re-derivation: `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/doc/upx-doc.txt` → HTTP 200, 37 208 B, sha256 `4dc547ed…`; lines 433/441/442 as quoted (`evidence/word-count.txt`).
- receipt fields: `jq` select over `.ufo/waves/round-68/l1/scores/c2-at-landing.json` as listed; both full pins occur in the receipt's bytes (`evidence/revisions.txt`, `evidence/word-count.txt`).
- The `- source:` / `- verified-at:` / `- recheck:` items are line-start list items, so the sweep
  `grep -rlE '^[-* ]*recheck *:'` matches this file after the append.
- Unrun here: the corpus census (`scripts/sources-census.sh validate`) — the L1 owns the gate; this
  block adds no SOURCES row.
