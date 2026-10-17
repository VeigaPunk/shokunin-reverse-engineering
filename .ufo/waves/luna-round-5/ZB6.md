## CLAIM
Item 6 converges substantively across both lanes (281 call sites + 2 jump sites remain; append-only erratum due). The open divergence is lexical: the two proposed post-integration gates — C4's token check and X1's regex check — cannot both pass on any erratum wording drafted so far, so integration must harmonize the erratum text with the retained gate.

## METHOD
Primary-source pass first (Lane A unread): `git show HEAD:corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md`, nl-selected `:18-19,59-70,152-155`; arithmetic 284−3=281 calls, +2 jmp = 283 remaining GOT-indirect sites. Then read all 15 wave files containing 281/283 (C4,C5,C7,D6,F6,G6,P0,P1,P2,R2,R3,S2,V6,X1) plus Lane B artifacts SB2/SB4/TB1/CB10/VB2. No probes; no tracked edits.

## FINDINGS
1. Substance unanimous: census 286 = 284 call + 2 jmp (`:18`), 3 probed (`:59-70`), so `:153` "remaining ~283 call sites" mislabels the 283-site residual as calls. Fix: append-only erratum at EOF (file is 194 lines; repo-wide max r5-02 citation = `:194`, nothing stranded). My derivation matches D6/F6/V6/G6/R3/P0/P2/R2/C5/C7.
2. Wording vs gates (reproduced Python sim): C4 (`C4.md:14`) needs lowercase substrings `284 call sites`, `3 probed`, `281 remaining call sites`, `2 jmp` — every drafted text FAILS. X1 (`X1.md:38`) needs `281.calls|281.call.sites` + `(?:2|two).jumps` + unprobed — passes only where "2 jumps" appears verbatim (V6 erratum, G6 finding prose; G6's quoted suggestion "2 jump sites" would fail X1). Sim: D6 FAIL/FAIL, V6 FAIL/PASS, F6 FAIL/FAIL, G6 FAIL/PASS, P2 FAIL/FAIL; none passes both. Verified dual-gate body: "The census records 284 call sites + 2 jmp; 3 probed call sites leave 281 remaining call sites, i.e. 281 call sites and 2 jumps remain unprobed (283 GOT-indirect sites total)." → PASS/PASS.
3. Broken pointer: `R2.md:9` cites `.ufo/waves/luna-round-5/V2.md:10-11` for the 281+2 arithmetic; V2.md is the firmware seat — 21 lines, zero r5-02/281/283 content, `:10-11` = blank + `## FINDINGS`. Intended: `.ufo/waves/luna-round-4/V10a.md:11` (as F6/V6/G6 cite).
4. Baseline pins verified exactly: S2 tail-15 `:180-194` = 5ffef2c8…766fe; SB2 tail-12 = cc9beb31…5144a; full blob 7387e01c…38689; 194 lines / 12634 B; worktree hash = HEAD a5f2f7d3…. SB2's r5-02 last-line quote is truncated ("…reference e" vs "…reference entry.") — hashes unaffected; don't copy the quote.

## THREATS
No recount of `/tmp/r5-jq.disasm.txt` (absent; probes prohibited): arithmetic is conditional on the recorded counts. Gate simulation is lexical, not semantic, covering only item-6 predicates of C4/X1 — their full census scripts were not run.

## VERDICT
FINDING: harmonize the r5-02 erratum wording with the retained gate (or dual-phrase as shown) and fix R2's V2→V10a pointer; item 6's substance converged.
