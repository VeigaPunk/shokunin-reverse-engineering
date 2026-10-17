# HB1 — hex/hash spot-check (5 recorded sha256s)

## CLAIM
Independently recompute 5 recorded sha256s from `.ufo/waves/luna-round-8/receipts/`; report match/mismatch with exact commands. Read-only; no live probes; no tracked files modified (`git status --porcelain` shows no tracked changes).

## METHOD
`sha256sum` on receipt files and /tmp captures; `sed -n` block extraction; `cmp`/`diff` byte comparison; `printf '6.4.0\n' | sha256sum` for literal L1 stdout; `head -n 59 | sha256sum` prefix test for leg-10.

## FINDINGS
1. MANIFEST.txt:1 claims leg-1.md `af959f64…` → recompute `af959f64…` ✓ (271 B).
2. MANIFEST.txt:3 claims leg-3.md `1be7e4f9…` → recompute `1be7e4f9…` ✓ (1448 B).
3. MANIFEST.txt:10 claims leg-10.md `c89eea7a…` → recompute `6cd389e9…` ✗ (40401 B; file mtime 21:14:02 > MANIFEST 21:02:41). `head -n 59 receipts/leg-10.md | sha256sum` = `c89eea7a…` (27655 B): append-only supersession (12746 B EX10 fallback tail appended). Stale entry, no byte loss.
4. leg-1.md:11 stdout `3754366908ac…` → `printf '6.4.0\n' | sha256sum` = `3754366908ac…` ✓ (6 B).
5. leg-3.md:6 stdout `5c682099…` → `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B) = `5c682099…` ✓; displayed block leg-3.md:21-22 is byte-identical (`cmp` exit 0, both 623 B). The briefed display-layer defect does not reproduce at the current revision.

Supplementary: full MANIFEST sweep — all 10 entries recomputed, 9/10 match; only leg-10 fails (per #3). census-pre.txt:81/102 self-hash `128006b1…` recomputes from lines 83-100 ✓ (2525 B), but its per-file list is a pre-rewrite snapshot: leg-3.md recorded 1430 B/`d641e3d3…` and leg-4.md 1233 B/`8f04ac26…` vs current 1448 B/`1be7e4f9…` and 1200 B/`aa4aa7a3…`; 11/13 census entries match current files. VB5.md:13-16 / ZB2.md:9 reached the same #3 adjudication independently.

## THREATS
- No raw /tmp capture exists for leg-1 stdout; verified only against the receipt's literal content.
- /tmp leg-3 capture provenance inferred from filename/mtime; not regenerable without a live probe (out of scope).
- census-pre.txt mtime (21:06) postdates the revisions it records, so its mtime does not date its content.
- leg-10 adjudication rests on prefix-hash equality — strong, but full byte history is not provable from disk alone.

## VERDICT
FINDING: MANIFEST.txt:10 leg-10.md stale (claimed `c89eea7a…` = head-59 prefix; current `6cd389e9…`); remaining 4/5 spot-checks clean; leg-3.md display defect not reproducible at current revision.
