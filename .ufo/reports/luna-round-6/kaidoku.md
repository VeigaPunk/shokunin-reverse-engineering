# kaidoku luna-round-6 — operability: pre-registered 6.5.0 battery

Date: 2026-10-16. Axis: **operability** (fleet axis, unowned proxy). Second
128-seat two-lane wave; first with live substrate probes since luna-round-2.
Predictions frozen by the parent in the dispatch brief before any execution.

## Work performed

- **Battery (10 legs)** on the live REA 6.5.0 surface: L1 version probe
  (exact 6.5.0), L2 tools/list (exact 207), L3-L8 RESULT-class legs
  (inspect_go_binary / inspect_rust_binary / inspect_electron_fuses /
  inspect_sqlite_database / search_bytes / inspect_with_objdump on real
  host carriers scouted by 6 scout seats), L9-L10 TYPED-REFUSAL-class legs
  (identify_flutter_build on jq; wasm/harmony route).
- Lane A (luna) executed with receipts `receipts/leg-1..10.md`; lane B
  (deepseek-v4.1-flash) re-ran all ten independently into
  `receipts-B/leg-1..10.md`; CC seats compared per leg; adversaries ran
  forgery, carrier-substitution, copy-vs-run, and availability-to-holding
  attacks; replay seats re-executed legs across lanes.
- Carriers scouted read-only on-host (Go/Rust/Electron/sqlite/small-ELF);
  zero operator-config drift (hashes before/after); no live MCP residue.

## Landed changes

- `.ufo/waves/luna-round-6/receipts/` + `receipts-B/` + both census
  transcripts — committed TRACKED at `bc91424` (lane identity). Durability
  deviation from the untracked-wave convention, disclosed: the round-5
  r12-01 erratum had to *attribute* a numeral because /tmp receipts were
  gone; battery receipts now survive in-repo.
- No map/PROVINCE/SKILL changes (measurement-only round).
- Bookkeeping commit (below).

## Before → after measurements

- Lane A score **10/10** (AC1 synthesis; PS1-PS4, RE2 independent reads).
- Lane B score **10/10** (BC1 independent recount with digest verification:
  all 10 receipt digests recompute; L2 frame re-parsed to 207 unique tools).
- Cross-lane agreement 10/10 at outcome-class level; byte-identical stdout
  on L1/L2/L7/L10 (BC1/BC5; CC seats).
- Frozen census `CENSUS RESULT: PASS` executed twice with byte-identical
  transcripts (AC3 lane A, BC4 lane B): 20/20 receipts hashed, zero drift,
  command A + token set unchanged.
- Command A at the round commit: 72/72, 9/9, 10.0/10.0 (AC8).

## Defects & adjudications (recorded, none hidden)

- Parent short-counted lane A (53/64) — **fourth occurrence** of the
  dispatch-arithmetic defect; the wave's 128th slot was additionally lost
  to a double-counted EX7 across an interrupted re-dispatch. Distinct-seat
  census: 127 (BC6, from the session wire). Counting self-check continues
  to be applied and continues to miss; the fleet ledger now carries four
  instances — a process defect the operator may want to gate.
- RV5's lane-A `MANIFEST.txt` lists L1 only (the 10 receipt files
  themselves hash-match).
- BB7/BB8's original lane-B receipts were overwritten by CC7/CC8 compare
  seats (custody defect; current bytes hash-match; BB reports remain
  class-valid).
- L10 route deviation: both lanes refused at `inspect_wasm_artifact`
  (WABT absent); the frozen `project_harmony_application_graph` fallback
  never executed. Outcome class matched the freeze; route recorded.
- L9 lane-B evidence is class-level (pretty-printed frame), not
  byte-level. L3/L9 "byte-identical" claims exist only in compare-seat
  prose (BC5 correction).
- ~1.2 GB of /tmp battery litter left in place (other live sessions share
  /tmp; removal is operator hygiene, not lane debt).
- AC2 carried open: EX6's raw transcript chronology (replacement receipt
  authored by RV3).

## SHONEN

- [~] ×4 unchanged (AC5 final): the battery is exactly the kind of evidence
  box 3 wants, but the fleet rule requires a named non-author verifier
  outside the lane's dispatched seats; cross-lane replay seats are still
  lane-dispatched. No advance.

## Verdicts

- operability: **improved** (first live-process evidence: 20 hashed,
  cross-lane-verified receipts; 10/10 + 10/10 vs frozen classes).
- coverage / depth / calibration: **unchanged** (measured).
- Learning: expansion deferred to round 7; quality improved (durable
  receipts + custody lessons); discernment improved (forgery/copy-vs-run
  attacks exercised).
- Admitted: yes — one axis improved, none harmed.
