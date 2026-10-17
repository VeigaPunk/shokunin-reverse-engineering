## CLAIM
Second protocol review of the delivered receipt set: RE1's L3 finding no longer reproduces (repaired); RE1's timeout finding is upheld; two new integrity issues exist — `leg-10.md` was mutated after the 10/10 census, and `census-pre.txt` does not match the delivered bytes.

## METHOD
Recomputed SHA-256 for every displayed stdout fence and every surviving `/tmp` raw; byte-compared displays to raws (L1-L3, L10); reconstructed RE1's pre-repair L3 bytes; diffed receipt hashes against `census-pre.txt`, `MANIFEST.txt`, `CA6.md`; re-ran the RE1 process scan; checked HEAD/worktree. No REA probe.

## FINDINGS
1. RE1's L3 defect does not reproduce: `leg-3.md:21-22`+LF is byte-identical to `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B, sha `5c682099…a569` = claimed; file 1448 B, `1be7e4f9…`). RE1's `ac7470f9…2223` reproduces exactly by deleting `"listChanged":true` from `"prompts"`; that version equals census's `d641e3d3…`/1430 B. Real observation, superseded artifact.
2. New — post-freeze mutation: `leg-10.md` is `6cd389e9…`/40401 B, mtime 21:14:02; `MANIFEST.txt` (21:02:41) and `CA6.md` (21:07) record `c89eea7a…`. Appended EX10 sections (`leg-10.md:28-84`) self-verify (`61450b92…` = `/tmp/…-leg10-summary.stdout`; `6abdf805…` = fence+LF) but `6abdf805…` has no surviving raw, and no census covers current bytes.
3. New — `census-pre.txt` records leg-3/leg-4 pre-repair hashes (`d641e3d3`/1430, `8f04ac26`/1233 vs current `aa4aa7a3`/1200) and omits leg-10 (13 files). Those files' mtimes (20:59:03, 20:58:39) predate the census write (21:06:07) and RE1's 20:59:42 read, so mtimes cannot order receipt content versions; mtime-based evidence (`CA6.md:8` via SE2) is unsound.
4. RE1's timeout point upheld: only L1/L2/L3/L7 show a timeout-wrapped invocation; L4-L6, L8, L10 assert ceilings.
5. Confirmations: L1-L8, L10 displays recompute to their claims; L2 raw `0bbe6bc7…` matches `leg-2-tools.txt` order (170 unique; six frozen names absent); carriers `/usr/bin/true` `8bc9a73a…`, `/usr/bin/jq` `e8156675…`, leg-6 sqlite `03c5ec9e…` still match; no REA process; HEAD `6e2ee8f` clean.

## THREATS
Raws survive only for L1-L3 and L10; L4-L9 hashes self-refer to displays, so raw fidelity there is unverifiable. `/tmp` is shared and mutable. This seat ran no live probe.

## VERDICT
FINDING: `leg-10.md` changed after the 10/10 census (MANIFEST/CA6 hashes stale) and `census-pre.txt` mismatches delivered bytes; RE1's L3 defect is repaired and no longer reproduces.
