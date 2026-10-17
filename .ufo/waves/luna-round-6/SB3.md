# SB3 — sentinel processes (lane B, deepseek-v4.1-flash)

## CLAIM
After lane B's 10-leg battery (receipts-B completed 10/10 + MANIFEST by 19:06), no stray MCP or probe processes remain on the host; every REA MCP observed was terminated by its owning seat.

## METHOD
- Host date 2026-10-16; HEAD f0e8cdecb216d71cf7df974675c0f6b16ba4f82f, `git status --porcelain=v1` → only untracked `.ufo/` (no tracked writes).
- `/proc` census (cmdline, cwd, exe, lstart) snapshots 19:00:32, 19:01:20, 19:03:38, 19:05:01, 19:06:35.
- 150s watch loop 19:00:58→19:03:31, 5s interval, logging first-seen of any cmdline matching `npx|mcp|node|rea`.
- Stray criterion: probe process alive after its owning seat harness exited. Verification by PID; zombie scan (`stat Z`), deleted-exe scan (`readlink /proc/*/exe`), TCP listeners (`ss -tlnp`). Read-only: no kills, no config edits.

## FINDINGS
- Watch captured 9 lane-B seats' probe trees, all rooted in /tmp: CC7 19:01:08, CC8 19:01:17/19:01:51/19:02:49, BB5 19:01:28, BB9 19:01:29, BB3 19:01:45, BB6 19:01:18, CC6 19:01:58, CC3 19:02:15, CB4-ICE 19:03:23. Pattern: `npm exec rea-agents@6.5.0 [--]mcp` → `node ~/.npm/_npx/.../.bin/rea mcp` (CC3/CC6 used /tmp/kaidoku-luna-round-6-npm-cache).
- Every re-checked probe PID group was gone after its harness exited. Longest-lived: CC3 tree 43034→43035(probe2.py)→43036→43048, alive 19:02:15–19:05:01 (harness alive, MCP up ~2m46s); all four GONE at 19:06:35 = terminated, not stray.
- At 19:06:35: zero `rea-agents`/probe node processes; no probe TCP listeners (only session shims on 127.0.0.1:8787-8793); no deleted-exe holders.
- Live MCP at final state: two `cli-agents-mcp` servers, PID 3018 (started 18:47:58, session stack) and PID 23615 (19:01:15, later kimi session) — harness infrastructure (python, cwd /home/vgpnk/Projects/shokunin, no probe cmdline), not battery residue. Flagged per assignment; classified infra.
- 4 defunct `uwsm-app` zombies (parents mako/waybar/fcitx5/swaybg, started 18:47:47) — boot noise, not battery.

## THREATS
- Point-in-time samples could miss a probe shorter than 5s; mitigated by watch-loop first-seen logging.
- CC3 held an MCP ~3 min with its harness still alive; termination verified only by tree-gone-at-sample, not by a shutdown log.
- Any literal `ps | grep mcp` will see the two infra `cli-agents-mcp` instances as "live MCP" — false-positive risk; they predate/postdate probe runs without probe lineage.
- Lane B seats were active during the window; "stray" was defined as outliving the owning harness, not "alive mid-run".

## VERDICT
CLEAN: zero stray/orphan MCP or probe processes; all observed REA MCP sessions terminated with their owning seats.
