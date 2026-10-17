## CLAIM
Full-set recheck of RE5: no contradiction between round-7's 6.5.0-pinned entries and the 6.4.0 refusals; RE5's two unverified items (other five refusals, 170-tool inventory) now resolved.

## METHOD
Read-only recomputation: leg-2-tools.txt line/unique counts and exact-name absence; every leg-N.md sha256 vs MANIFEST.txt; every displayed stdout block vs its in-file claim; leg-2-tools/leg-1/3/4/5/9 vs census-pre.txt:97; round-7 `FINAL-MANIFEST.md:28-263`, the six landed entries `corpus/knowledge/2026-10-16-l7-01..06`, `corpus/README.md:62-67,146-151`, LOG/SCORECARD; CA6/VB5/VB7/RV2; `/tmp/kaidoku-luna-round-8-leg-3*`. No probes; no writes.

## FINDINGS
Substantive axis clean. leg-2-tools.txt: 170 lines, 170 unique; all six names absent by exact match (rc=1; near-misses only `read_bytes`/`search_procedures`/`search_strings`/`search_android_classes`). L3-L8: six `-32602` `Tool <name> not found`; L7's `open_binary` RESULT matches entry 5's 6.5.0 sequence; L1/L10 controls intact. All six entries pin `rea-agents@6.5.0` (l7-02:5 "other REA versions" untested); none claims 6.4.0 support, so no contradiction; jointly the results bound presence only across the two tested versions.
New record defect: `census-pre.txt:97` lists leg-3.md size=1430 sha256=`d641e3d3…` and leg-4.md size=1233 sha256=`8f04ac26…`; current bytes (matching MANIFEST.txt and CA6.md) are 1448 B/`1be7e4f9…` and 1200 B/`aa4aa7a3…`. Both mtimes (20:59:03/20:58:39) predate census-pre.txt (21:06:07), so those two lines are a stale ~20:58 snapshot; `d641e3d3…`/`8f04ac26…` appear nowhere else (grep) — possibly the only surviving trace of the known-defect-era leg-3.
Confirmed VB5: MANIFEST leg-10 hash `c89eea7a…` is stale after the 21:14:02 append (current `6cd389e9…`; `head -59` = `c89eea7a…`).
Known defect not reproducible: leg-3's displayed block (623 B, with trailing LF) recomputes to claimed `5c6820…`; without LF it is `225d67cc…`; /tmp capture matches.

## THREATS
mtime-based staleness inference assumes accurate mtimes; stale leg-3/4 bytes are unrecoverable, so the content delta cannot be assessed. Block hashes are self-consistent, not independently attested (only leg-3 has a /tmp raw witness). No re-probe (not assigned).

## VERDICT
FINDING: substantive cross-round consistency CLEAN, but `census-pre.txt:97`'s leg-3/leg-4 hash lines do not recompute against current bytes (stale snapshot) — treat census-pre's receipt block as pre-final for legs 3-4.
