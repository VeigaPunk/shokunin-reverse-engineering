## CLAIM
Verify CB5's census covers: 10 receipts hashed; 10/10 predictions; leg-9 exact; zero drift; Command A + token set unchanged at the integration commit.

## METHOD
Read-only at HEAD `6e2ee8f`, 21:16–21:31 ART. Looked up `CB5.md` (three checks) and swept the repo for any CB5-named artifact; read `MANIFEST.txt`, legs 1–10, `census-pre.txt`, CA6, XB1, VB2/VB5, `census-laneB-pre.txt`. Independently recomputed: leg sha256s (two snapshots ~10 min apart), six leg-9 fixed-string greps, `sha256("6.4.0\n")`, tool-list count/uniqueness, Command A verbatim at `6e2ee8f`, coverage-map token digest, `git diff 3395b6d 6e2ee8f`, `git status`, three host-config hashes. Python via stdin; no probes; only write is this file.

## FINDINGS
- CB5's census has no on-disk artifact: `ls .ufo/waves/luna-round-8/CB5.md` → exit 2 at 21:16, 21:26, 21:31; repo-wide `find -name 'CB5*'` returns only rounds 5–7. `XB1.md:5,16` and `receipts/census-laneB-pre.txt` independently record the same (`WAVE_REPORTS_EXIST_CB5=False`). Coverage by CB5 is unverifiable.
- Criteria, against artifacts that exist: **10 hashed** — MANIFEST holds 10 unique leg names/hashes; recompute 9/10: leg-10 stale-by-append (claim `c89eea7a…` = `head -n 59`, 27655 B; current `6cd389e9…`, 40401 B; `CA6.md:10` cites the stale value). leg-3 now self-verifies (1448 B, `1be7e4f9…` = MANIFEST; displayed block + LF = `5c682099…` = claim = `/tmp/kaidoku-luna-round-8-leg-3-mcp.stdout`, 623 B); the defective 1430-B state survives only in `census-pre.txt:97`. **10/10** — L1 `6.4.0` (`3754366908…`); L2 170 unique; L3–L8 each `-32602 Tool … not found`; L9 six greps rc=1/empty; L10 RESULT `inspect_binary_layout` on jq (`ev_9befd8…`). **leg-9 exact** — six whole-word greps rc=1, empty stdout `e3b0c442…`. **zero drift** — `git status -uno` empty, `git diff --quiet HEAD` clean, configs equal CE1's 21:06 hashes, receipt bytes identical across my two snapshots. **Command A/tokens** — 78/78, 9/9, 10.0/10.0, missing/dangling `[]`; 78 tokens, digest `c6c025f3…` = digest at `3395b6d` (README byte-identical `1cf5b769…`, 0 knowledge blobs changed).

## THREATS
Drift window is 21:06→21:31 only; no pre-round-8 capture. XB1's fallback census is the nearest lane-B census but is not CB5's. If CB5 files later, re-run required.

## VERDICT
FINDING: CB5's census is absent from disk, so its coverage of the five criteria is unverifiable; independently they hold for existing artifacts except MANIFEST's leg-10 hash (stale-by-append).
