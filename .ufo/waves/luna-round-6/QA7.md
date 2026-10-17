# QA7 — server-termination evidence (leg-2-class receipts)

## CLAIM
Every leg-2-class receipt — a leg that ran an MCP stdio server — demonstrates termination (process check and/or clean exit). This lists which ones do, and in what form.

## METHOD
Read lane-A receipts `receipts/leg-1..10.md` (protocol/method reading per assignment) and lane-B `receipts-B/` present at audit close 19:02:17 (legs 1,2,7,8,9,10). Classified each leg's mode from its COMMAND line; extracted termination statements by direct read plus grep. No re-runs; this report is my only write.

## FINDINGS
Lane A, leg-2-class (server ran) = legs 2,3,4,6,7,8,9,10. All 8 demonstrate termination, all clean-exit form:
- `leg-2.md:18-19` — exit 0; "SERVER TERMINATION: stdin closed; process exited"
- `leg-3.md:219-220` — exit 0; "stdin closed; process exited normally"
- `leg-4.md:37,41` — exit 0; "MCP process was waited and exited 0 (not reused)"
- `leg-6.md:14`, `leg-7.md:15`, `leg-8.md:14` — "MCP SERVER EXIT CODE: 0 (stdin closed; server exited normally)"
- `leg-9.md:1,10` — "waited for normal server exit"; exit 0; timeout=false
- `leg-10.md:26,29` — "PROCESS EXIT CODE: 0"; stdin closed; server exited 0

Out of class, CLI-only (no server): `leg-1.md:3`; `leg-5.md:3`.

Lane B present at audit close: `receipts-B/leg-1.md:47` CLI, "nothing to terminate"; `leg-2.md:13-14` exit 0, stdin EOF, signal null, no SIGTERM/SIGKILL; `leg-7.md:4,59` exit 0 plus "`ps` check: no rea-agents processes remain"; `leg-8.md:4,13` exit 0, timeout=false, forced terminate: no; `leg-9.md:81,85` exit 0, no signal, graceful stdin-EOF, post-run node/npx scan for cwd `/tmp/rea-bb9`: none; `leg-10.md:67` stdin EOF, exited 0 by itself, no rea process left.

Process-check form exists only in lane B (`receipts-B/leg-7.md:59` ps; `leg-9.md:85` scoped scan + ownership analysis of broad pgrep hits). Lane-A receipts carry no pgrep/ps/lsof evidence; sweeps live only in seat reports (BB1.md:13; SE3.md:5-8; RV1.md:13; RE1.md:11).

## THREATS
Lane-A termination is probe-reported (exit status + stdin close), not an independent post-exit sweep. SE3.md:8 / RV1.md:13 saw peer EX8's server live mid-wave; EX8.md:7,15 later records its exit 0 (in-flight, not orphaned) — but no receipt proves a globally clean host, and leg-9.md:85 shows concurrent seats' rea processes visible in a broad pgrep during the wave.

## VERDICT
CLEAN — all 8 lane-A leg-2-class receipts (2,3,4,6,7,8,9,10) demonstrate termination via clean exit; legs 1/5 ran no server; lane B adds two explicit process checks (leg-7 ps, leg-9 scoped scan).
