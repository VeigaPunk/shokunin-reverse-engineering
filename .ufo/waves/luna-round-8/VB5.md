# VB5 — MANIFEST verifier

## CLAIM
`receipts/MANIFEST.txt` recomputes against current bytes for all 10 legs. (Resolved path: `.ufo/waves/luna-round-8/receipts/` — no `receipts/` exists at repo root.)

## METHOD
- Read-only. Repo at HEAD `6e2ee8f`; no tracked files touched; no live probes.
- `cd .ufo/waves/luna-round-8/receipts && sha256sum leg-{1..10}.md`, compared line-by-line with MANIFEST.txt (format is `name hash`, so plain `sha256sum -c` refuses it; reordered via `awk '{print $2"  "$1}' MANIFEST.txt > /tmp/vb5-manifest-gnu.txt && sha256sum -c`).
- Timeline: `stat -c '%y %n'` on MANIFEST vs leg files; `grep -rl c89eea7a…` across round-8; prefix hash `head -n 59 leg-10.md | sha256sum`; /tmp leg10 artifacts hashed.

## FINDINGS
- **9/10 recompute exactly**: leg-1..leg-8, leg-9 all `OK`. leg-3 is `OK` — current bytes hash `1be7e4f9…e33e1b`, so the known display-layer corruption does not affect its MANIFEST entry.
- **leg-10.md FAILED**: MANIFEST claims `c89eea7a368c780ffe4ab6026e883300fa9f612484b1cf79ac75871cebd32d7b`; current bytes give `6cd389e99f9a5f9b7957fe1021b1007bfec7eb345ed58cf9f982e1d9595e1ec4` (40401 B).
- Cause is append-only supersession, not fabrication: `head -n 59 leg-10.md | sha256sum` = `c89eea7a…` (27655 B). leg-10.md mtime `21:14:02` vs MANIFEST `21:02:41`; `CA6.md:10` (21:07) cites the old hash. Lines 60–84 (`## EX10 lane A inspect_binary_layout fallback` section) were appended at 21:14, after both manifest and census. The pre-append bytes are exactly recoverable as `head -n 59`.
- Manifest is otherwise self-consistent: 10 lines, 10 unique names, 10 unique hashes.
- `c89eea7a…` matches no /tmp artifact; /tmp `kaidoku-luna-round-8-leg10.stdout`/`-summary.stdout` hash `23e94d0b…`/`61450b92…`, matching the hashes cited inside current leg-10.md.

## THREATS
- Timestamp reasoning uses filesystem mtimes only; no independent clock source.
- Prefix-hash test is at a line boundary; it establishes append semantics for this file but not byte provenance of the appended section (content verification belongs to L10 seats).
- I verified hashes only, not receipt content claims; manifest cannot be consumed by stock `sha256sum -c` without reformatting.

## VERDICT
FINDING: leg-10.md stale-by-append — MANIFEST hash `c89eea7a…` = pre-21:14 version (head-59); current bytes `6cd389e9…`; other 9 legs CLEAN.
