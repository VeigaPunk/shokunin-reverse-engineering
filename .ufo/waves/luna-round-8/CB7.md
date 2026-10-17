## CLAIM
Byte-check whether the planned leg-3 repair (replace displayed stdout block with the raw `/tmp` bytes) corrupts any other recorded field; pin the byte-exact repair.

## METHOD
Read `receipts/leg-3.md`; hashed `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`; extracted the fenced block (lines 21-22 + trailing LF) and `cmp`'d it to raw; reconstructed the pre-repair file by deleting the 18-byte field; `stat` mtime/ctime of leg-3.md and dependents; recomputed `MANIFEST.txt:3`, `CA6.md:10`, `census-pre.txt:97`, and legs 1-10 block-vs-claim. Untracked dir, no probes; only this file written.

## FINDINGS
- **Repair already applied on disk.** `leg-3.md:21-22` block == raw file, 623 B, sha256 `5c68209953fb9d1444209e286ee7de0a67661ae087f222977165d30f76d5a569` == claim at `:6`; whole file 1448 B sha256 `1be7e4f92c9de9c76edb156addee15114ebc3cd04abce4505ffa0ac877e33e1b` == `MANIFEST.txt:3` and `CA6.md:10`; mtime=ctime=20:59:03.685 — untouched since.
- **Pre-repair bytes pinned.** Deleting `"listChanged":true` (18 B) from the unique `"prompts":{...}` in line 21 yields 1430 B, sha256 `d641e3d3…ca11091` (= `census-pre.txt:97`) and block sha256 `ac7470f9…` (= `RE1.md:9`). So the defect was exactly a lost 18-byte field; RE1/census-pre measured it before the 20:59:03 fix (stale-read artifact; raw captured 20:53:24).
- **Byte-exact repair:** in line 21 insert `"listChanged":true` after the `{` of the unique `"prompts":{`; equivalently replace the fenced content with the raw bytes. Postconditions: size 1448; file sha `1be7e4f9…e33e1b`; block sha `5c68…`; `cmp` block /tmp raw → identical; fences (lines 20, 23) and all other bytes unchanged; LF only.
- **No other field is byte-implicated.** Block replacement is local; `MANIFEST.txt:3`, `CA6.md:10`, `VB5.md:12`, `VB7.md:9,18` expect exactly `1be7e4f9…` — an idempotent verify preserves them; dropping the block's trailing LF or touching fences breaks all four. `census-pre.txt:97` leg-3 (`d641e3d3…`) can never recompute (pre-final snapshot); same for its leg-4 entry (1233 B/`8f04ac26…` vs current 1200 B/`aa4aa7a3…`, mtime 20:58:39). All other census entries recompute.
- **Unattested:** stderr block (`leg-3.md:10-14`, npm notices) has no surviving raw — both leg-3 `/tmp` stderr captures are 0 B. Unaffected by the repair.

## THREATS
No direct observation of who wrote the 20:59:03 bytes; RE1's report (21:01:04) and census-pre data predate the flip. Extraction convention matters: block without trailing LF hashes `225d67cc…`, not the claim. The parent must not assert census-pre recomputes for legs 3-4.

## VERDICT
FINDING: repair target is already on disk — apply idempotent verify-only (block==`5c68…`, file `1be7e4f9…`); byte-exact edit if ever needed = insert 18 B `"listChanged":true`; `census-pre.txt:97` legs 3-4 are pre-final snapshots; stderr block unattested.
