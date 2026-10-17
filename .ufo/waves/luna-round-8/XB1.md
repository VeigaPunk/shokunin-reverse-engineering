## CLAIM
Lane B seat XB1 (census runner): pre-state census of the luna-round-8 evidence set executed read-only at HEAD `6e2ee8f`; receipt `.ufo/waves/luna-round-8/receipts/census-laneB-pre.txt` (sha256 `0920d6f555be0f87c552560f45bba097410bde5abd2a7459b1f987782204a7a4`). The assigned design source "CB5's census" had no on-disk artifact at run time; the census ran on the documented fallback, disclosed in the receipt.

## METHOD
Lookup `ls .ufo/waves/luna-round-8/CB5.md` → exit 2 (absent; `WAVE_REPORTS_EXIST_CB5=False`). Fallback per round-6 XB1 / round-7 PB2 precedent: Recipe A extracted verbatim from the pinned `SCORECARD.md` Git blob (fence sha256 `2cc0f1c0…`), coverage-map token census, knowledge blob aggregate, plus lane-B additions: receipt inventory with MANIFEST cross-check, 6.4.0 tool-list control, three host-config fingerprints. Script `/tmp/xb1-r8/census.py` (`a0fc12ef…`), run three times, embedded whole in the receipt with all run hashes. No probes, MCP, network, config edits, or tracked writes. Exposure: lane-A `census-pre.txt`/`CA6.md` and lane-B leg-10 analyses were read during recon; every value independently recomputed (non-blind, disclosed).

## FINDINGS
- Controls: HEAD match, tracked-dirty 0, `git diff --quiet HEAD` exit 0; Recipe A exit 0 — 78/78 mapped, 9/9 rules, 10.0/10.0, stdout sha256 `5885833a…` (= TB1's independent lane-B run).
- Tokens 78/78 unique, digest `c6c025f3…`, set-equal to the 78 file stems, missing/dangling `[]`; knowledge aggregate `00891de8…` (78 files).
- Inventory (16 files, every sha256 recorded): MANIFEST 9/10 exact; leg-10 append-superseded — claimed `c89eea7a…` = `head -n 59` (27655 B) of current 40401 B `6cd389e9…` (agrees with VB3/VB5/VB6/ZB2).
- leg-3: current file sha `1be7e4f9…` = MANIFEST; displayed stdout block + LF = `5c682099…` = its claim = `/tmp/…-leg-3-mcp.stdout` bytes → the known display defect does not reproduce in current bytes (pre-repair 1430-B state survives only in `census-pre.txt:97`).
- Tool list: 170/170 unique; all six 6.5-only verbs absent, rc=1 each (inventory-level L2/L9 support); sorted digest `5612d104…` (new pin).
- Config fingerprints equal CE1's 21:06 snapshot; runs differ only in the concurrency-labelled `WAVE_REPORT_COUNT` line (74→76→81).

## THREATS
"CB5's census" is unresolvable from disk at this snapshot (21:22–21:25 ART); if CB5 later defines a different census, a re-run is required. Lane B was filing concurrently — the receipt records a point-in-time state. The census is mechanical: it records the leg-10 mismatch and `census-pre.txt`'s pre-repair 13-file list without adjudicating them, and makes no battery-outcome claim.

## VERDICT
CLEAN — pre-state census reproduced at `6e2ee8f` (78/78 · 9/9 · 10.0; tokens `c6c025f3…`; 78-file `00891de8…`; 170-tool list, six verbs absent); receipt filed (`0920d6f5…`).
