## CLAIM
Provenance grade per round-5 erratum: correctable-by-text vs needs-live-reprobe; flag any text correction silently upgraded into a re-verification claim.

## METHOD
Read-only primaries at HEAD cfc84c2 (worktree=HEAD): asar-surface.md:14-19; r4u-01:41,49; PROVINCE.md:28-33; README.md:122,131,160,163; r9-02:7-8,50-55,82-84,146-169,215-216,294-309,326-335; r5-02:18-19,150-155; r12-01:40-42,99-104; LOG.md:389-401; Lane A seats D1-D7, V1/V3/V5/V7, C5/C7, G3/G4, X1. Hex math via python3. No probes, no tracked edits.

## FINDINGS
1. ASAR framing: text-only. Consolidates held r2/r3 findings (r3-renderer-asar.md:31-37: 45 `ipcMain` = 44 `on` + 1 `handle`; :79-85: `index.js` not-found); D1/V1 disclaim fresh verification.
2. `.fwimage` decimals: text-only arithmetic — 0x1c01dc8→29,367,752; 0x505b000→84,258,816; in-entry corroboration at :49 (carve extent ≈29,367,752); D2 hedges "no new readelf result claimed".
3. PROVINCE pin: text-only, family-scoped. FLAG: V3/G3's unscoped "does not authenticate module attribution" and X1's PIN gate (tokens only `when module identity matters`+`pin request bytes`) admit a general rule built from an `analyze_function`-only counterexample — D3/C7's qualifier is required.
4. README: text-only (:131 via LOG.md:389-401; :163 via map rows :47/:53/:56). Residual: :122 still asserts "all four statuses live…unsupported" — same defect as item 5, outside the recorded span.
5. r9-02 statuses: text-only when record-scoped ("no recorded run reports `inferred`"). FLAG: "never observed" would need durable receipts or reprobe; D5/V5 correctly says "unobserved in this record".
6. r5-02: text-only from recorded census (284 call+2 jmp; 3 probed; 281+2 unprobed). Keep "recorded counts imply"; the census receipt (/tmp) is non-durable.
7. r12-01: text-only supersession. FLAG: existing :99-104 already upgrades to "held==lane==audit holds" plus 4 sites/7 values whose supporting /tmp envelopes are absent (V7) — any round-5 append must stay "the record reports…" and not re-verify; D7's "no new erratum" conflicts with X1's census expecting an r12-01 append.

## THREATS
Grading draft provenance, not run truth; no reprobe performed. Lane B sibling reports were not visible at write time. Items 2/6/7 receipts are non-durable; the corrected ga10x decimal rests on recorded hex alone.

## VERDICT
FINDING: all 7 are text-correctable as scoped; three silent-upgrade hazards flagged (items 3, 5, 7); none requires a live reprobe for its text-scoped correction.
