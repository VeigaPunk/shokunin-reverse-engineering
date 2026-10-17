# SB3 — sentinel hygiene 2: /tmp + processes + configs (lane B, deepseek-v4.1-flash)

## CLAIM
Read-only audit at HEAD a280e07 (2026-10-16 21:56–22:00 -03) finds: operator configs frozen (zero drift vs r6/r7 finals), no stray probe process (the one live rea MCP died with its interactive harness), and `/tmp` carrying ~1.59 GiB of inherited litter while live round-9 seats write scratch into it mid-audit. FINDING applies to the `/tmp` surface only.

## METHOD
Read-only; no probes/network/deletions. `sha256sum`+`stat` on the four operator configs; `ps -eo pid,ppid,lstart,stat,comm,args`; zombie + deleted-exe scans (`readlink /proc/*/exe`); `ss -tlnp`; `/proc/*/cwd` and `/proc/*/fd` sweep vs `/tmp`; `ls -1 /tmp` label census + `du -sc`; `find /tmp -maxdepth 1 -newermt '2026-10-16 21:44:34'` (wave start = earliest wave artifact, `A1.md` 21:44:34); lineage walk of PID 678880; `git rev-parse HEAD`; `git status --porcelain=v1 | grep -v '^??' | wc -l` → 0.

## FINDINGS
- **Configs CLEAN:** all four hashes equal r6/r7 finals (devin `16f496e6…263a4`, omp `38d2a1d0…926b`, kimi `4af27747…2707`, `.bashrc` `7d2ca28a…6598`); mtimes ≤2026-10-16 13:54; no `~/.npmrc`.
- **Processes CLEAN:** only rea MCP seen = PID 678868→678880 (`npm exec rea-agents@6.5.0 mcp`, from 21:48:47), child of interactive omp→bash→alacritty (cwd `/home/vgpnk/tmp`, `npm_config_cache=/home/vgpnk/.npm`); alive 21:58:31, gone with harness by 22:00 — not stray by r6 criterion. No deleted-exe holders; 5 defunct zombies (host noise); listeners normal (shims 8787–8793, omp:3847, system/steam).
- **/tmp FINDING:** 155 top-level entries; label census 99→102 during the pass; `du -sc` 1,666,484 KB ≈1.59 GiB (r6 npm caches ~336 MB each; r8-era ~480 MB). Six round-9 scratch items appeared live 21:58:59–22:00:17: `sb4r9-frame-*` ×3, `sb4r9-now.txt`, `pb1-r9/`, `gb2-readme-693009.txt`. No process cwd under `/tmp`; only `/tmp` fds are host apps' deleted temps (steam/chromium).
- **Proposal (no unilateral deletions):** PROTOCOL.md:341-343 — tmpfs paths are not evidence; durable receipts belong in `.ufo/waves/<round>/receipts/`. Post-wave, operator reviews an explicit-path inventory; no glob/age/prefix deletion (labels collide across rounds, e.g. `rea-cb5` mtime 21:35:41; unlabelled `m*.log`, `reltest`, `/tmp/tmp/` unattributable — filenames≠ownership).

## THREATS
Moving target: census grew 99→102 entries, ~+28 MB, during the pass; mtimes lower-bound usage only. Hash/mtime checks cannot exclude backdated edits. The interactive omp probe's task was not inspected. Command A/battery not rerun (outside this seat).

## VERDICT
FINDING: /tmp holds ~1.59 GiB inherited litter plus live round-9 scratch — delete nothing now; hygiene is operator-owned, post-wave, explicit-path. Process and config surfaces CLEAN.
