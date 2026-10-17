## CLAIM
Over-reach audit of all D*/DB* drafts, both lanes: Lane A D1–D7, Lane B DB1–DB7 (all present by 16:43). Hunt: assertions exceeding cited or available evidence.

## METHOD
Read all 14 drafts; re-verified load-bearing claims against HEAD cfc84c2 (`git show`), live `readelf -S`/`sha256sum` on the four GSP blobs (no REA), worktree `hash-object`, a repo-wide PROVINCE-citation census (`git grep`), and `stat` mtimes. Read-only; no tracked writes.

## FINDINGS
1. **D7 (r12-01) over-reaches.** D7.md:2,21 closes the debt ("CLEAN"; "existing append-only correction resolves the recorded debt"; "V27 independently records") though D7.md:18 concedes presence-only checking. V7.md:2,9–10 finds the erratum's count unsupported; DB7.md:4,12 with VB7.md:11–15 (source-level) confirms four sites but adds residual staleness both missed — `r4-16-frontier-rescan.md:750–754` still states the two-value account (verified at HEAD) — and "7 values" is not re-derivable. V27.md:15 disclaims independent byte verification.
2. **D2/D3 false-absent inputs.** D2.md:5 "Fleet-root `**/V2.md` glob returned no match"; V2.md mtime 16:23:58 predates D2.md 16:27:29. D3.md:19 "V3.md is absent"; V3.md 16:24:32, 18 s before D3.md 16:24:50 (R4.md:11 flags it). Only consistent if their globs skipped hidden `.ufo/`. D1/D7 timing is consistent (V1 16:28:49 > D1 16:24:18; V7 16:26:00 > D7 16:25:40).
3. **DB3.** (a) Keeps "pin the exact request bytes", failing the PIN gate's literal `pin request bytes` (C4.md:25 assert; X1.md:32 matcher — both verified); VB3.md:9–11 reworks it. (b) "Line 33 grows 42→~190 chars" (DB3.md:12): the quoted 290-char sentence yields ≈333 (42 verified at HEAD). (c) Its stale-citation list omits ≥4 tracked sources: r12-02 ledger :141/:183/:297 and r4-16:849 (→PROVINCE:117), `.ufo/reports/round-1/kaidoku.md:84` (→:88–109), r14-02:80/:91/:92 (→:130/:75–86/:69–73). Its offsets 2885/2961, line-49=865, F3 reproduction, README:170: exact.
4. **DB4.md:8** labels 6a71cd5 "= HEAD"; HEAD is cfc84c2 (its parent); README byte-identical across, so positions hold. Label slip only.
Spot-verified clean: D1, D4 (LOG:389–401 exact), D5 (V5.md:12–13 verbatim), D6 (284−3=281), DB1, DB2 (":47→:49" fix right; live sha256/readelf match), DB5, DB6 (SB2 pin = HEAD blob sha).

## THREATS
Hidden-dir glob-skip inferred, not proven; census regex undercounts chained refs (the four omissions are first-position, solid); DB* writes after 16:43 unaudited; draft-order process claims unverifiable.

## VERDICT
FINDING: D7's closure contradicts V7/DB7 and misses r4-16:750–754; D2/D3 rely on false-absent inputs; DB3's wording fails the PIN gate and its growth/drift numbers are off; DB4 mislabels HEAD; nine drafts spot-verify clean.
