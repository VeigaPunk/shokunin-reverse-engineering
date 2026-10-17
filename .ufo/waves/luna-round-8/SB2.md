# SB2 — sentinel configs (lane B, deepseek-v4.1-flash)

## CLAIM
All four sentinel config paths are byte-identical to lane-A SE2 (round 8) and to the round-6 baseline; no config drift was observed.

## METHOD
Read-only; no probes, no cleanup, no writes beyond this file. Three captures at `2026-10-16T21:17:04`, `21:17:14`, `21:19:31 (-03:00)` running `date -Is && sha256sum <4 paths> && stat -c '%y  %s bytes  %n' <4 paths`. Digests compared as sorted 64-hex sets against `.ufo/waves/luna-round-8/SE2.md:9-12` and `.ufo/waves/luna-round-6/SE2.md:9-12` (round-6 baseline), corroborated at `.ufo/waves/luna-round-6/SB2.md:9-12`, `.ufo/waves/luna-round-7/S3.md`, `.ufo/waves/luna-round-7/SB3.md:10`, `.ufo/waves/luna-round-2/S2.md:8-10`, and `.ufo/waves/luna-round-8/receipts/census-pre.txt:98-100`.

## FINDINGS
- Three captures identical; 4/4 match vs round-8 SE2 and 4/4 vs the round-6 baseline:
  - `/home/vgpnk/.config/devin/mcp_config.json` `16f496e663d0c91252d17dcb8094d141a8feb713466e2fb4f14267bf744263a4` (406 B)
  - `/home/vgpnk/.omp/agent/mcp.json` `38d2a1d0e5e67da09266c4611b34ab32b394371063f307c5104b6cb0de1b926b` (429 B)
  - `/home/vgpnk/.kimi-code/config.toml` `4af27747eb93244fcd343fc15552dc7b3ae689fcd7d00f2dea46faca1ca42707` (46 513 B)
  - `/home/vgpnk/.bashrc` `7d2ca28a245c44a1f5458921f0dff54823aa1e74ffa02eac2013b486e6a26598` (3 601 B)
- Lineage: rounds 2/6/7/8 all record these digests; `census-pre.txt:98-100` independently re-hashes devin/omp/kimi to the same values (`.bashrc` not in that census).
- Sizes and mtimes unchanged across the three captures: devin/omp `2026-10-14 17:53:20`, kimi `2026-10-16 13:54:22`, `.bashrc` `13:33:16` — all ≥6h56m before round-8 `receipts/leg-1.md` (20:52:40).

## THREATS
No round-8 pre-battery config capture exists (earliest: SE2 at 20:53:26, 46 s after leg-1); a write-then-revert inside the round-8 window is not excluded by hashing, and mtimes are owner-forgeable. Scope is exactly these four paths; no other config surface sampled. Scope-adjacent observation: `census-pre.txt:97` records leg-3 and leg-4 with bytes that no longer recompute (leg-3 1430 B/`d641e3d3…` vs current 1448 B/`1be7e4f9…`; leg-4 1233 B/`8f04ac26…` vs current 1200 B/`aa4aa7a3…`), while the other 11 entries recompute — the census preserves those two legs' pre-replacement bytes. Current leg-3 stdout block hashes to its claimed `5c682099…` (equal to `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`); current leg-4 likewise to `0fbd3bd0…`.

## VERDICT
CLEAN: 4/4 sentinel hashes match SE2 and the round-6 baseline across three captures; no config drift observed.
