# QA2 — evidence-discipline sample 2 (lane B)

## CLAIM
Sampled 8 lane-B seat reports by arrival order (frozen ~19:02): XA, BB1, SB2, CC1, PB0, TB1, BB10, SB4. Seven pass structure and citation checks under read-only recomputation; XA carries two non-resolving citations.

## METHOD
Sample rule: top-level `.ufo/waves/luna-round-6/*.md`, mtime >= 18:55 (lane A's last artifact `EX7.md` 18:53:13; lane B's first `XA.md` 18:58:07), eight smallest mtimes at freeze (range 18:58:07-19:01:34). Read all 8 in full; scripted heading/word/verdict scan. Re-ran cited commands read-only: `printf '6.5.0\n' | sha256sum`/`xxd`; `sha256sum` of receipts and SB2's four config paths; `sha256sum -c MANIFEST.txt`; recipe A extracted verbatim from `SCORECARD.md:92-123` with `REV=f0e8cde`; `sed`/`grep` line checks; `stat`; `git rev-parse HEAD`; `git status --porcelain`. Lane-A reads: verification only. No MCP server, no config edit, no repo write outside this file.

## FINDINGS
- Structure: 8/8 exactly the five headings, 223-362 words; verdicts CLEAN (7) / FINDING (XA).
- Reproduced: BB1/CC1 L1 digest `3eb8e06c…` at `receipts-B/leg-1.md:26` = `receipts/leg-1.md:11`, re-derived from `printf '6.5.0\n'`; CC1's 271/864 B sizes and `24bfd90f…` at `MANIFEST.txt:1`; `sha256sum -c MANIFEST.txt` fails exactly as CC1 states (exit 1, "no properly formatted checksum lines"); SB2's four hashes equal `SE2.md:9-12` and my recomputation (zero drift persists), quoted mtimes match `stat`; TB1's recipe-A stdout sha256 `258dc869…` and JSON (72/72, 9/9, 10.0/10.0) reproduced exactly, HEAD `f0e8cde`, 0 tracked changes; BB10's `e4cf0833…` sits in both leg-10 receipts, exit 0, two `level:40` stderr lines; `receipts/leg-2.md` holds 207 `"inputSchema"` and all ten battery tool names (corroborates PB0).
- FINDING (XA): `RV2.md:6` is blank, `:10` is the L5 bullet, `grep 'L10\|Harmony' RV2.md` = 0 matches; the described L10 Harmony route is at `RV4.md:6,10`. `EX8.md:10` is blank; EX8.md is an L8/objdump report holding no L6 text. Both files' mtimes (18:21:55, 18:22:32) predate `XA.md` (18:58:07) — citation error, not snapshot drift; PB0 independently reports the same non-resolution. XA's substance otherwise checks: `MANIFEST.txt:1` lists only leg-1, `leg-9.md:12` raw-process digest has no bytes, `RV2.md:9` resolves, lane-A heading containment holds (53/53; PR2 adds an extra `## luna-round-6…` heading).

## THREATS
Lane membership rests on the mtime window plus seat markers; if `EX7.md` were lane B the sample shifts. Spot-verification only: XA's L1-L8/L10 digest recomputations and live-process orphan checks were not repeated (concurrent seats' probe processes were live during my checks).

## VERDICT
FINDING: 7/8 sampled lane-B reports reproduce under read-only recomputation; XA's citations `RV2.md:6,10` and `EX8.md:10` do not resolve (material at `RV4.md:6,10`; EX8 has no L6 text).
