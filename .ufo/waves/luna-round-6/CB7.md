# CB7 — wrong-version hunter (lane B receipts)

## CLAIM

Every command recorded in receipts-B (leg-1.md … leg-10.md) names `rea-agents@6.5.0`. CLEAN if every package invocation is exactly pinned; FINDING if any command floats or pins another version.

## METHOD

- Polled `.ufo/waves/luna-round-6/receipts-B/` until all 10 legs existed and were stable (10/10 by 19:04; md5sum of names+sizes+mtimes unchanged through 19:05).
- Regex sweep of all 10 files for every `rea-agents` token: each must equal `rea-agents@6.5.0`. Also swept for floating specs (`@latest|next|beta|rc`), alternate names (`rea_agents`), and cache-path execution (`node|exec|spawn … node_modules/rea-agents`).
- Grepped the persisted `/tmp` harness scripts that spawn the server, for the spawn-time pin.
- Cross-checked resolved npx caches and scanned each receipt for any non-6.5.0 `"version"` string.

## FINDINGS

- 25 `rea-agents` tokens total: 20 exactly `@6.5.0`; the other 5 are prose-only process/cache mentions (leg-4:62, leg-5:56, leg-8:78, leg-9:22, leg-9:85) — not commands.
- Command forms, all pinned: `--version` (leg-1:9); `mcp` subcommand (leg-2:1, leg-6:10, leg-9:19, leg-10:9); `--mcp` flag (leg-3:36, leg-4:12, leg-5:16, leg-7:10); leg-6 preflight `timeout 230 npx -y rea-agents@6.5.0 --version` (leg-6:14); leg-8 pipeline runs under `timeout 240` (leg-8:26, 51).
- Harness spawns verified at source in /tmp: driver.js:12, probe-leg3.mjs:12, mcp_leg4.py:18, mcp_drive.py:18, cleanup_probe.py:12, drive_mcp.py:34, probe.mjs:8 — all `["npx","-y","rea-agents@6.5.0", …]`.
- Zero floating specs, zero alternate package names, zero cache-path executions.
- Independent: both npx caches (`~/.npm/_npx/ad9a3fdbcad992c6` and lane-B `/tmp/kaidoku-luna-round-6B-npm-cache`) hold package.json version 6.5.0; every leg's `serverInfo` reports `"version":"6.5.0"`. The only other version strings belong to non-rea components (clientInfo 0.1.0 leg-6:41; Ghidra 12.1.4 leg-7; Chromium 149 leg-2).

## THREATS

- Check covers recorded commands plus persisted artifacts; no probe was re-run (by rule). Cache/harness artifacts were still on disk at check time.
- Attested pre-run commands (leg-2:2 pre-probe) were not re-executed; their cache resolves to 6.5.0.
- stdout sha256 values were not recomputed (outside this assignment). leg-4:9 shows an outer `timeout 285` wrapper — noted, not adjudicated here.

## VERDICT

CLEAN — every receipts-B command names rea-agents@6.5.0; no wrong-version invocation found.
