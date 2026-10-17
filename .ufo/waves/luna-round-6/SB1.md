# SB1 — luna-round-6 LANE B | /tmp sentinel, post-run sweep

## CLAIM
Post-run /tmp sweep: lane-B probing left 43 round-labelled entries (~1.2 GB) with no live reference — litter by lane-A precedent (SE1.md:2) — and zero orphaned probe/MCP processes; SB1 footprint nil. Verdict: FINDING.

## METHOD
- Read-only; no SB1 /tmp writes: no new top-level entry after 19:11 except seat-owned mtime bumps (`find /tmp -maxdepth 1 -newermt '2026-10-16 19:11:00'`).
- Baseline proven: `find /tmp -maxdepth 2 ! -newermt '2026-10-16 18:47:00' -not -path /tmp` → 0 entries (tmpfs, boot 18:47) ⇒ everything present is post-boot.
- 16 quiescence polls 19:02:14–19:19:36 (`ls /tmp`, `ps` rea/npm/mcp greps, `/proc/*/cwd`, receipts-B count); inventory 19:15–19:21 (`ls -la` mtime/size ledger, per-entry `du`, `file` scan, >1 MB find, `/proc/*/fd`, python3 REA-signature walk: 32,740 paths, 7 root-only permission errors).
- Completion anchor: receipts-B/leg-1..10.md + MANIFEST.txt present by 19:11.

## FINDINGS
- 43 entries at 19:21 = 27 seat dirs + 13 scratch files + 3 runtime caches ≈ 1.2 GB (scratch 536 MB + caches 675 MB). Largest: round npm caches `kaidoku-luna-round-6[-B]-npm-cache` 336 MB each; `cc6-leg6` 339 MB (nested npm cache incl. 39 MB frida prebuild tar); `rea-cb6` 173 MB (still live); `cc3-luna6` 8.9 MB; `cc2-compare` 6 MB. SQLite fixtures `cc6-leg6.sqlite`, `bb6-leg-6/sc4-index.db` match leg-6 probe scope.
- Abandoned-seat proof: `rea-bb1` mtime 18:59:48 unchanged through 19:19 — 16+ min after BB1 completed (BB1.md, receipts-B/leg-1.md); bb6-leg-6, bb10-l10, rea-cc* likewise idle.
- Zero orphans: observed probe PIDs (17579/92, 28409–11, 43036, 70528/9) all exited with their seats; final samples 19:19:36/19:21 show no rea/npm/mcp process, no listener, no fd into /tmp. Live PID 3018 is host session infra (cli-agents-mcp, since 18:47), not a probe.
- No binaries: `file` scan found text/JSON/sqlite only ("Dyalog APL transfer" hits are `file` false positives on receipts).
- Host, not round, excluded: org.chromium.Chromium.HKmsX5 (user browser 19:10), hsperfdata_vgpnk, node-compile-cache v24 subdir (18:47).

## THREATS
- Snapshot, not close-state: seat CB6 still writing at 19:20 (mtime 19:20:15) — re-sweep at wave close advised.
- Attribution = tmpfs-fresh baseline + name/mtime/ownership; 7 root-only dirs unverified.
- Deletion deliberately not performed (own-scope only; evidence preservation; some dirs live).
- If wave norms accept seat scratch as benign, re-classify (round-5 SB3 precedent); round-6 lane A called remaining labelled artifacts a hygiene FINDING.

## VERDICT
FINDING: 43 lane-B-labelled /tmp entries (~1.2 GB; incl. 2×336 MB npm caches) remain uncleaned at the 19:21 post-battery sweep; no orphan probe/MCP processes; SB1 footprint zero.
