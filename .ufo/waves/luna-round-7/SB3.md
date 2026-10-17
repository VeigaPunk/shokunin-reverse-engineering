# SB3 — sentinel hygiene (lane B, deepseek-v4.1-flash)

## CLAIM
Round-7 no-probe discipline held on my surfaces (20:09–20:15): zero probe/MCP processes beyond session infra, zero config drift, no tracked-file modifications; SB3 wrote only this receipt. `/tmp` carries inherited round-6 litter plus fresh round-7 seat scratch, none held open by any process. Verdict FINDING applies to the `/tmp` surface only.

## METHOD
Read-only; no probes, no cleanup. Three `sha256sum` captures (20:09:14 / 20:11:58 / 20:14:04) of the four operator configs; `ps` + pgrep filter `rea-agents|\.bin/rea|rea mcp`; `ss -tlnp`; deleted-exe scan (`readlink /proc/*/exe`); `/proc/*/cwd` + `/proc/*/fd` scans vs `/tmp`; `ls -la /tmp`; label census `ls -1 /tmp | grep -Ei '^(bb|bc|cb|cc|qa|rb|rea-|tb|xb|sb[0-9]|kaidoku|vb[0-9])'`; `du -sc`; `find /tmp -maxdepth 1 -newermt '2026-10-16 19:56:00' -printf '%T+ %f\n'`; `git -C kaidoku rev-parse HEAD`, `status --porcelain=v1`, `diff --quiet HEAD`; repo mtime walk excluding `.ufo`/`.git`.

## FINDINGS
- Configs: all three captures identical — devin `16f496e6…263a4`, OMP `38d2a1d0…926b`, Kimi `4af27747…2707`, `.bashrc` `7d2ca28a…6598` — equal to round-6 finals (`.ufo/waves/luna-round-6/SE2.md:9-12`; `SB2.md:9-12`, 19:00:22); mtimes ≤13:54:22 today, unchanged.
- Processes (20:14:52): pgrep exit 1 (none); sole MCP = infra `cli-agents-mcp` PID 3018 (since 18:47:58); no deleted-exe holders; listeners = host shims 8787-8793 + system (631/53/5355); 6 defunct uwsm-app/systemctl = host noise; no lane `/tmp` path referenced by any cwd/fd (only chromium deleted temp handles).
- `/tmp` (20:14:52): 59 label-matched top-level entries, `du -sc` total 1,265,988 KB ≈1.21 GiB (two 336 MB npm caches frozen at 19:00:38/49; rea-cb6 173 MB). Since SB1's round-6 19:21 sweep (`luna-round-6/SB1.md:13,25`): +7 late round-6 writes (bc1-mani.txt, bc4-*, bc5-block.txt, rea-bc2 19:49:58) and 12 round-7 top-level entries since 19:56 (rb7-readme.md 20:09:46; tb1-r7 20:10:11 with command-A recipe output 72/72 @ 411175e; vb1/vb2 leg/`.raw` dumps; rb5-sim; cb3-sim; pb2-r7 20:14:27).
- Repo: HEAD `411175e337c0`; `git -C kaidoku diff --quiet HEAD` exit 0; status clean outside untracked `.ufo/`; in-repo mtimes since 19:53 only `.git` (my index refreshes) — LOG.md/SCORECARD.md 19:52:35 belong to 411175e (committed 19:53:26).

## THREATS
Point-in-time: seats wrote `/tmp` mid-pass (pb2-r7 at 20:14:27) — counts are floors. Label regex ≠ SB1's classification, so 43→59 drift is approximate. A sub-second probe leaving no process, cache, or `/tmp` trace cannot be fully excluded. Hash/mtime checks cannot exclude backdated touches. Cleanup not performed (out of scope).

## VERDICT
FINDING: process/config surfaces CLEAN (zero probe residue, zero drift), but `/tmp` holds ~1.21 GiB inherited round-6 litter plus live round-7 scratch, unreferenced by any process.
