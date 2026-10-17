# ZB1 — SUPERSEDED-verdict table compiled into round-report process-defect text

## CLAIM
VB6's ten-row superseded-verdict table (VB6.md landed 21:19:20) is row-verified and compiled into append-ready text for the round-8 report's process-defect section.

## METHOD
Read-only at HEAD 6e2ee8f; no probes; only this file written. Recomputed all citations: verdict lines; the nine `rea-agents@6.4.0` pins (leg-1:3,2:1,3:4,4:4,5:3,6:3,7:4,8:3,10:3); refusals (leg-3:22,4:13,5:9,6:11,7:13,8:10); leg-9:18-23; leg-10 (40401 B; fields :3/:12/:18/:23/:24; :26 `23e94d0b…`; `head -59 | sha256sum` = `c89eea7a…`; whole file `6cd389e9…`); leg-2-tools.txt (170 lines; 0 matches per name); 6.5 sweep 0 matches; CA6:8/10; MANIFEST:10; /tmp leg-3-mcp.stdout `5c682099…` (623 B), leg10.stdout `23e94d0b…`.

## FINDINGS
All ten rows verified. Compiled section text:

> **Superseded lane-A verdicts (recorded).** Ten lane-A seats read receipts before they landed and recorded absent/unscored verdicts; the late evidence supersedes each; no score rests on them.
>
> Seat | Stale verdict | Superseding evidence
> ---|---|---|---
> PS1 | `PS1.md:20` L1–L5 unscored | legs 1–5 landed; `leg-3.md:22` `-32602`; list 170 names
> PS2 | `PS2.md:14` L6–L10 unscorable | legs 6–10 landed; refusals `leg-6.md:11`, `7:13`, `8:10`; `leg-9.md:18-23`; leg-10 RESULT
> PS3 | `PS3.md:27` final N/10 unestablished | ten legs present; `CA6.md:8` N/10=10/10
> RE2 | `RE2.md:22` 1/10 confirmed matched | as PS3
> RV6 | `RV6.md:14` pins unverifiable | nine receipts pin `@6.4.0`; leg-9 carries none
> RV8 | `RV8.md:14` leg-10 missing | `leg-10.md` fields `:3,:12,:18,:23,:24`; 40401 B
> RV1 | `RV1.md:22` no preexisting L2 receipt | leg-2.md + 170-name list landed (RV1's own capture)
> CA7 | `CA7.md:14` leakage check unverifiable | 6.5 sweep over ten legs + list: 0 matches
> XG1 | `XG1.md:21` six classes unverifiable | raw `-32602` leg-3/4/5; 6.4.0 quoted leg-6/7/8
> RE6 | `RE6.md:25` L9 unverified | `leg-9.md:18-23` six ABSENT, exit 1, `e3b0c442…`
>
> **Follow-ups.** `MANIFEST.txt:10` and `CA6.md:10` cite leg-10 whole-file `c89eea7a…`, stale for current bytes `6cd389e9…`; bytes 0–27655 still hash `c89eea7a…` — post-census append, not corruption. leg-3's claimed `5c682099…` recomputes from the displayed block (trailing LF) and /tmp raw: the display-hash defect does not reproduce.

## THREATS
Single untracked snapshot. RV1's supersession is partial — the receipt is self-authored, so "no independent" still holds. leg-9 has no version pin. VB6 excluded class-adjacent pending-L10 verdicts (PR1:27, PR2:26, CA8:14, CA2:15, RE3:18); parent may fold in or leave out. Landing times are mtimes, not read times.

## VERDICT
CLEAN — ten rows verified and compiled; two citation fixes (RV8 field lines; leg-10 hash follow-up); no row failed.
