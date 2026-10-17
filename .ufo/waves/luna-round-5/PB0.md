## CLAIM
Lane-B verifies the 7 recorded debts from primaries only; Z-seats converge by item-ID diff with primary-source adjudication.

## METHOD
Read at HEAD cfc84c2: the five knowledge files, PROVINCE.md:31-32,58, README.md, LOG.md:395-401, SCORECARD.md:92-123; hex via python3. Enumeration drafted from primaries, then cross-checked P0.md (no V/DB read).

## FINDINGS
Seven items (A = append-only erratum, C = current-surface edit; locate by quoted text — line numbers drift):
1. A — asar-surface.md:14-16 "app.asar IS the main-process bundle": r3-renderer-asar:31-37,107 proves obsidian.asar holds the privileged main.js (45 ipcMain) and app.asar is a thin launcher; reconcile r2-asar-deep-obsidian:23-29.
2. A — r4u-01:41-49,103: 0x1c01dc8 = 29,367,752 (text says 29,358,536); 0x505b000 = 84,258,816 (text says 84,242,432). python3-verified; append corrections, no rewrite.
3. C — PROVINCE.md:31-32,58: conditional request-byte pin for module-identity probes (`subject` unauthenticated; ids verb-family-specific). Authority r9-02:146-169.
4. C — README.md:131,163: :163 lists held process/managed/call-target ops as frontier (reconcile :47,:53,:125); :131 "4 nits fixed" vs LOG.md:395-401 (2 fixes, 1 pre-land self-correction, 1 accepted). Subchecks 4a/4b.
5. A — r9-02: :215-216 "four statuses … complete" vs `inferred:0` :82-84 and live examples :106-124 (verified/contradicted only); reconcile toward README:53.
6. A — r5-02: after 3 probes remaining = 281 calls + 2 jmp*, not "~283 call sites" (:152-153; census :18-19; probes :59-70).
7. A — r12-01 L197 (frontier-table line): main :13,:40-44 "two values" vs erratum :99-104 (4 sites/7 values); verify erratum adequacy, else append pointer.

Lane-B independence: pre-draft inputs = assignment pointers + primaries + git objects only; do not open luna-round-5 V*/D* (Lane-A verdict outputs) until your verdict's evidence is fixed. Post-draft reading allowed; never revise to match — log the divergence. No tracked-file edits (LOG included); propose text in-seat.

Z convergence-diff: per item 1-7, extract every A/B verdict + evidence pointers; classify CONVERGENT / DIVERGENT (adjudicate from primaries, cite path:line) / UNILATERAL (flag one-lane gap) / UNPROVABLE. Diff by item ID, locate by text. Z reads all outputs; verdicts rest on primaries — agreeing lanes are not evidence. Post-edit: rerun Command A (SCORECARD.md:92-123) → 72/72 files, 9/9 rules, 10.0/10.0; README map token set == 72 baseline.

## THREATS
Textual-only; no artifacts replayed; hex by arithmetic. Pointer drift is systemic (items 4,6,7). P0 cross-read occurred post-draft.

## VERDICT
CLEAN — 7 items enumerated, independence rules and Z protocol assigned; no scope additions.
