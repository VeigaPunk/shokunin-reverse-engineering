# SB1 — sentinel /tmp sweep (luna-round-8)

## CLAIM
Sweep /tmp for luna-round-8 residue: verify the leg-3 raw-stdout corroborator against its claimed hash, detect leaked REA servers, and note litter without deleting other seats' files.

## METHOD
Read-only, 21:18-21:22 local. `ls -la /tmp`; `find /tmp -maxdepth 1 -newermt '2026-10-16 20:00'`; `sha256sum` + `cmp` of `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` vs `receipts/leg-3.md:21-22`; `sed`-extracted block variants; `pgrep -af 'rea-agents|kaidoku'`; `pgrep -af node`; `ss -ltnp`; `du -sh`. No probes, no servers started, no deletions; sole write is this report.

## FINDINGS
- Corroborator intact: `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B) sha256 `5c682099…f76d5a569` equals the claim at `receipts/leg-3.md:6`, and `cmp` exit 0 shows it byte-identical to leg-3.md's display block (623 B, same hash). The KNOWN DEFECT does not reproduce on current disk; block variants hash differently (lines 20-23 with fences `08576144…`, no-trailing-newline `225d67cc…`), and other seats probed the same at 21:17 (`/tmp/zb3-*`, `/tmp/qb3-leg3-display.bin`).
- No leaked servers: `pgrep -af 'rea-agents|kaidoku'` → none; no REA/node listener (`ss -ltnp`; :8787-8793 are host shims pid 1590-1595, age 2h30m). `luna-round-8-leg-6.sqlite` (8192 B) has no `-wal`/`-shm`.
- Litter, not deleted: 14 round-8-named entries — 10 files ~2.2 MB (`leg10.stdout` 2127950 B etc.) + sqlite + three npx caches ≈469 MB (`kaidoku-luna-round-8-npm-cache` 156M, `kaidoku-luna-round8-rv1` 158M, `luna-round-8-ex7-run` 156M). 63 /tmp entries newer than 20:00; seat prefixes bb2/bb3, cb3/cb7, hb2, pb2-r7, qb3, rb5/rb7/rb8, tb1-r7, vb1/vb2/vb5, xb1, zb3; unattributed `arms-rum-preload.cjs` (344 B Electron ArmsEventBridge), `znr-*.sock`, `scoped_dirA8Dw8D`, `hsperfdata_vgpnk`.
- Incidental (outside /tmp): `receipts/leg-10.md` now `6cd389e9…` (mtime 21:14) vs MANIFEST.txt:10 and CA6.md:10 `c89eea7a…` — post-census edit; legs 1-9 equal MANIFEST exactly. `census-pre.txt` leg-3 `d641e3d3…` (1430 B) / leg-4 `8f04ac26…` (1233 B) are a superseded older snapshot (`CE1.md:8-11`).

## THREATS
Point-in-time snapshot: other seats wrote /tmp during the sweep (21:17-21:19). Authorship of litter items unproven. Round-6/7 litter also present, not fully inventoried.

## VERDICT
CLEAN: no leaked REA servers; leg-3 corroborator matches the claim and the on-disk block is byte-identical; ~469 MB caches + files noted in place, nothing deleted. Incidental, non-scope: leg-10.md differs from MANIFEST since the 21:14 edit.
