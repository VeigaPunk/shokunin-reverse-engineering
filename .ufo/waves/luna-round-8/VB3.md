## CLAIM
Receipts `leg-6.md`–`leg-8.md` and `leg-6/7/8-RV3-replay.md` are internally consistent, hash-faithful, and match the three frozen L6–L8 TYPED-REFUSAL predictions.

## METHOD
Read-only recompute at HEAD `6e2ee8f`: sha256 of MANIFEST-covered files; extraction of every `text` stdout/stderr block with SHA-256 (trailing-newline convention); byte comparison against the raw survivor `/tmp/luna-round-8-ex7-run/mcp.stdout|.stderr`; carrier hashing (`/usr/bin/true`, `/usr/bin/jq`, pnpm `index.db`, `/tmp/luna-round-8-leg-6.sqlite`) plus read-only sqlite read; fixed-string greps of the refused verbs in the 170-line `leg-2-tools.txt`. No probes, no tracked-file writes.

## FINDINGS
- All six displayed stdout blocks hash-match their claimed digests exactly (with trailing `\n`): leg-6 `5bc135e0…`, leg-6-RV3 `c7997ada…`, leg-7 `866f8b58…`, leg-7-RV3 `7481ffaf…`, leg-8 and leg-8-RV3 both `65d740cf…` (626 B, matching the claimed byte count).
- leg-7 has an independent raw capture byte-identical to its displayed stdout (1075 B) and stderr (384 B) blocks. The leg-6 sqlite fixture (8192 B, `03c5ec9e…`) contains exactly the claimed DDL and row. All carriers match claimed size+hash: `true` 43320/`8bc9a73a…`, `jq` 30800/`e8156675…`, `index.db` 16384/`3701a7e3…`.
- Predictions match: every initialize reports rea `6.4.0`; each refused call is `-32602` `Tool <name> not found`; the three verbs occur 0× in `leg-2-tools.txt` (170 lines), so refusal is consistent with list absence. RV3's claim that canonical receipts predate the replays holds (mtimes 20:53–20:54 vs 20:57:41).
- MANIFEST recompute: legs 1–9 OK, **`leg-10.md` FAILS** (actual `6cd389e9…` vs claimed `c89eea7a…`; mtime 21:14:02, after MANIFEST 21:02:41 and CA6 census 21:07:37). Its appended EX10 sections are self-consistent (`61450b92…`, `6abdf805…` match their displayed blocks), so this reads as a post-census append rather than corruption — but CA6's "all hashes recompute" is time-bounded.

## THREATS
For leg-6, leg-8 and all three replays no raw capture survives, so digest-vs-display agreement is self-consistency, not independent replay; only leg-7 has a raw file. Exit codes, process sweeps, and run ordering are unverifiable now. Replay receipts carry no MANIFEST digest. I did not re-probe REA (not authorized) and did not audit legs 1–5 or 9–10 content.

## VERDICT
CLEAN for the assigned legs 6–8 + RV3 replays; cross-range flag: `leg-10.md` no longer matches `MANIFEST.txt`.
