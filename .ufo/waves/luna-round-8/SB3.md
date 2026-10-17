# SB3 — sentinel processes | stray MCP check (lane B, deepseek-v4.1-flash)

## CLAIM
After lane A's battery finished (receipts complete 21:14) and during lane-B verification, the host carries zero stray/orphan REA MCP or probe processes; every live MCP process is host infrastructure with a live owning process.

## METHOD
- Read-only; no live probes; sole write = this receipt. Host clock 21:17:04–21:21 (-03); HEAD 6e2ee8f untouched (`git status --porcelain=v1`: only `?? .ufo/...`).
- Static census 21:17:04: full `ps` with lstart/ppid; pgrep filters (`rea-agents`, `\.bin/rea`, `rea mcp`, `npx`, `timeout 240|120`); `/proc/*/exe` regex scan; `/proc/*/maps` grep (`rea-agents|kaidoku-luna|_npx`); deleted-exe scan; `ss -tlnp`; zombie scan; `/proc/*/cwd`+fd sweep vs `/tmp`.
- 150 s spawn watch 21:18:22→21:20:52, `ps` delta every 3 s, then final census + listener/zombie diff.
- Collateral hashes: `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`, `receipts/leg-3.md`.

## FINDINGS
- Zero REA/kaidoku processes in every sample; pgrep hits were only the pgrep shell's own wrapper cmdline (self-match, PIDs 350827/363075). No npx/rea exe, no maps hits, no deleted-exe holders, no probe listeners; zombies 7/7 unchanged across the window.
- Live MCP is infra only: `cli-agents-mcp` PID 3018 (parent kimi 2959, since 18:47:58) and the ZCode editor set under `zcode-cli` 212551←212482←ZCode 212226 (since 20:48:2x, pre-wave): godot-mcp ×2, mcp-for-blender ×1, zcode-node-repl-mcp ×1 at 21:17. At 21:20:23 `zcode-cli` spawned a duplicate godot-mcp tree (404824/404897→405172/405226) and blender tree (406082/406093→406133/406143) with originals still alive — owner-alive editor duplication, caught mid-watch, not battery residue.
- Watch caught only lane-B seat shells (RB5/CB5 waiters, /tmp hash sweeps); no probe spawns; no new listeners (ss diff empty).
- No process holds cwd/fd under `/tmp` (only chromium deleted-handle).
- `leg-3-mcp.stdout` still present (623 B, mtime 20:53:24): sha256 `5c682099…569` = hash claimed in `receipts/leg-3.md` and byte-identical to leg-3.md lines 21-22; leg-3.md sha256 = MANIFEST `1be7e4f9…`. Flagged defect is not reproducible on current bytes; fence-inclusive/no-final-newline extractions hash `08576144…`/`08155af6…`/`225d67cc…` if the parent's mismatch came from extraction boundaries.

## THREATS
3 s watch granularity could miss sub-3 s probes; ps-delta observes starts/stops only; ownership classified by live parent, not shutdown logs; ZCode duplicate MCP trees may grow further (editor-side, left untouched); any literal `pgrep mcp` now returns ~11 infra processes (false-positive risk, cf. round-6 SB3.md:22).

## VERDICT
CLEAN: zero stray/orphan REA MCP or probe processes; all live MCP owner-held host infra (kimi session + ZCode editor, incl. mid-watch ZCode duplication).
