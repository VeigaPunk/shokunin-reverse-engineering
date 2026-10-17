## CLAIM
Legs 3–5 verify hash-correct as stored. The flagged L3 defect is a superseded on-disk state, not a current one: `5c682099…a569` matches the receipt's displayed block *and* the raw stdout byte-for-byte; RE1's `ac7470f9…2223` matches the pre-20:59:03 file. The exact repair is: **do not edit `leg-3.md`**.

## METHOD
Byte-exact extraction in Python (bytes between the final ```` ```text ```` newline and the closing fence; receipt files are LF-only) with SHA-256, plus `stat -c '%y %s'` and `sha256sum`. Cross-checks against `receipts/MANIFEST.txt`, `receipts/census-pre.txt:97`, `RE1.md:9`, `/tmp` artifacts, and a live `sha256sum /usr/lib/signal-desktop/signal-desktop`.

## FINDINGS
- L3: displayed block (`leg-3.md:21-22`) = 623 B = `5c682099…a569` = claimed hash, byte-equal to `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout` (623 B, mtime 20:53:24). Current file = 1448 B / `1be7e4f9…e33e1b` = `MANIFEST.txt:3` = CA6, mtime 20:59:03.
- RE1's hash resolves exactly: current bytes with `"prompts":{"listChanged":true}` → `"prompts":{}` = 605 B block / `ac7470f9…2223`, 1430 B file / `d641e3d3c4e7985d…` — identical to `census-pre.txt:97`'s leg-3 entry (1430 B / `d641e3d3…`). So the corruption was persisted to disk (a census script read those bytes), not display-only; it was replaced at 20:59:03. No file now contains `"prompts":{}` (grep over repo + /tmp: none).
- L4: block 625 B = `0fbd3bd0…0d5f` = claim; file = MANIFEST. Census saw an earlier 1233 B form (`8f04ac26…`); no L4 raw stdout survives, so only self-consistency is provable.
- L5: block 628 B = `adfb7370…b115` = claim; file = MANIFEST = census. Carrier re-verified live: 223513856 B, SHA-256 `f7a9b441…85a` = `leg-5.md:5` claim.
- L3's stderr block (209 B npm notice) has no leg-3-owned artifact: `/tmp/…leg-3.stderr` and `…leg-3-mcp.stderr` are both 0 B. Identical text appears in other seats' captures (`/tmp/kaidoku-luna-round8-rv1/leg1.stderr`, `/tmp/luna-round-8-ex7-run/mcp.stderr`); attribution plausible, unproven.
- Cross-seat flag: `leg-10.md` now hashes `6cd389e9…` (40401 B, mtime 21:14) ≠ MANIFEST/CA6 `c89eea7a…`; its internal blocks still self-verify.

## THREATS
Receipt hashes prove content, not execution. Census timing is inferred from mtimes (leg-9/replays 20:57 ≤ census < leg-4's 20:58:39 rewrite); `census-pre.txt` records no clock. I changed nothing (read-only; write scoped to this file).

## VERDICT
FINDING: legs 3–5 are hash-correct as stored; L3's reported defect is the superseded pre-20:59:03 bytes, so the exact repair is no edit to `leg-3.md` — annotate `RE1.md:9` as stale and keep the defect out of the consolidated entry.
