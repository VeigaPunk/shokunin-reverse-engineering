## CLAIM
Lane-B independent ledger for luna rounds 1–3: every debt/defect named in the three round reports traced to later evidence; records-commit rewrite-vs-append adjudicated.

## METHOD
Read `.ufo/reports/luna-round-{1,2,3}/kaidoku.md`, `LOG.md:625-714`, `SCORECARD.md:237-373,561-613`, round-4/5/9 reports, `SHONEN.md`, `.ufo/waves/luna-round-9/{F3,GB5}.md`. Git-object only: `git show --numstat <records> -- LOG.md SCORECARD.md` for all nine records commits; `git rev-parse --short HEAD` → `c343939` — one commit past the briefed `6e83a20` (operator-amendment commit); tracked worktree clean. No probes, network, `/tmp`, or writes outside this seat file.

## FINDINGS
- **Rewrite table (records-commit deletions):** r1 `a4bd355` SCORECARD 40/**4**; r2 `a9580eb` 60/**8**; r3 `0772d54` 55/**7**; r4 `cfc84c2` 46/**1**; r7 `6e2ee8f` 32/**1**; r5/r6/r8/r9 SCORECARD 0 deletions; LOG 0 deletions in all nine. → Five rewrite rounds, not four: **round 1 rewrote the living coverage row and Coverage-map gap bullet** (4 deleted lines), absent from lane A's W1/W2/W3/R8 set. Rounds 2/3 rewrote the calibration/depth rows + Version-drift/Authority-contradiction bullets.
- **Closed later:** 12 V-seat map drift + README drift → round-4 drain (14 repairs, 5 adjudications; `.ufo/reports/luna-round-4/kaidoku.md:10-46`); asar framing, README nits, r9-02, r5-02, r12-01 → round-5 seven dispositions (`.ufo/reports/luna-round-5/kaidoku.md:11-39`); r3 C7 request-byte pin landed — `PROVINCE.md:33`.
- **Carried, no closure found through r9:** R4 no-peeking (r1:66-67), S2 pointer-style (r1:67-68), four untracked `.ufo/interactive-sessions/` files (r1:68-69; still 4 untracked on disk), r14-01/02 content debt (r1:18-20; GB5:13), B2 stale L7 hash (r2:65; F3:12), misnamed `R2-reviewer-readme.md` (r3:65; file still so named), C4 unpersisted census (r3:66-68), `/tmp/probe*.log` (r3:68; GB5:12).
- **SHONEN** 4×`[~]` current (`SHONEN.md:5-12`); seat counts r1 64/64, r2 58+6 backfill, r3 64/64 (disk counts match reports).
- **MANIFEST:** luna-rounds 1–3 rows (`MANIFEST.json:2750,2763,2776`) carry exact enums — `jq` scan finds 6 prose-decorated fields in luna rows 8,9,10,12×2,13, plus 4 in historical rows 1–4.

## THREATS
Reports are bounded evidence; "no closure cited" ≠ proven open. `/tmp` not inspected; command A not rerun; old probes not revalidated. D1 (lane A) covered these rounds before me — this pass is independent (adds round-1 rewrite; confirms carried set).

## VERDICT
FINDING: round 1's records commit also rewrote SCORECARD (lane A flagged only 2/3/4/7); eight rounds-1–3 debt items lack closure evidence through round 9.
