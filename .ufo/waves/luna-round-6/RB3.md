## CLAIM
Are RE1–RE4's protocol verdicts supported by the artifacts they cite and the timeline in which they looked?

## METHOD
Read RE1–RE4; recomputed sha256 of every receipt's primary stdout block vs its recorded digest (in-file convention: joined lines + final LF); compared `stat` mtimes of seat reports vs receipts to test each "at inspection" claim; verified leg-1.md file hash vs MANIFEST; checked cited lines (EX1, XG2, SC2–SC5, SHONEN, SKILL, PROTOCOL, PS4); `ps -C node` + `pgrep` at ~19:05.

## FINDINGS
- All ten primary stdout digests recompute MATCH — including L6 `9a1445b4…` and L8 `e0b2d505…`; leg-1.md file hash = MANIFEST `24bfd90f…`. Only L9's raw-process digest `1ff84c06…` is not reconstructible from the receipt.
- RE2/RE3/RE4 snapshot verdicts supported: leg-2.md mtime 18:19:00; MANIFEST (18:18:38) lists leg-1 only; PS3.md 18:23. Their citations hold: RE2 `leg-1.md:3-11`; RE3 `EX1.md:10-11` and `printf '6.5.0\n'|sha256sum`→`3eb8e06c…`; RE4 `XG2.md:7-10` and SC/SHONEN/SKILL/PROTOCOL refs. RE4's "Glob showed only leg-1" at 18:19:20 is consistent but unreproducible (leg-2 landed 18:19:00).
- RE1 (18:27:31) is only partly auditable: it read leg-6/8/9 revisions replaced at 18:27:56–18:28:04 (mtimes > report mtime), so refs (`leg-6.md:12`, `:15-19`) resolve only against unpreserved revisions. Its L6 defect is corroborated by RV3.md:5 ("L6 was repeated once to repair receipt capture"); final L6 reconciles.
- RE1 items reproducing: L2/L3/L4 metadata documents no 240 s bound (their "240" strings sit inside echoed tools/list JSON; L4 has none); all eight reviewed receipts record /tmp; L2 `:19`, L3 `:219-221`, L4 `:37-41` closures match. Item failing: "L8 does not document a 240-second bound / records provider output not full MCP stdout" — final L8 documents 240 s (`leg-8.md:3`) and ships full MCP stdout (`:16-20`), having been rewritten after RE1. L9 `:47` likewise points to a replaced revision (final 13 lines).

## THREATS
Superseded leg-6/8/9 revisions are unpreserved; mtimes prove last, not first write, so RE1's L8 items can be neither confirmed nor refuted. No host/config audit; lane-B probes were live under /tmp at my check, so no global-cleanup claim.

## VERDICT
FINDING: RE2–RE4 verdicts supported; RE1's L6 finding corroborated and its L1–L5 claims reproduce, but its L8/line-ref claims describe revisions replaced after its review and are unverifiable against the final receipts.
