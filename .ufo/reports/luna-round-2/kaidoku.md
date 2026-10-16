# kaidoku luna-round-2 — per-client REA surface calibration

Date: 2026-10-16. Axis: **calibration** (the SCORECARD's registered 'planned'
move; taken on a three-way proxy tie at 10.0 by the most-falsifiable-next-claim
rule). One axis-move. Wave: 64 seats total on
`openai-codex/gpt-6-luna-max` — 58 + 6 backfill (see Process defects).

## Work performed

- Live substrate probed read-only 2026-10-16; receipts at
  `.ufo/waves/luna-round-2/receipts/` (hashed, replay-verified):
  - Devin `~/.config/devin/mcp_config.json:7` + OMP `~/.omp/agent/mcp.json:8`
    pin `rea-agents@6.5.0`: 207 MCP tools (tools/list, two independent runs
    L7/L15), 153 CLI (`--help`, L6), catalog `805433f17bb4…` (L12), installed
    skill v42, doctor `aligned` (l10-doctor-6.5.0, exit 1, live_server unknown).
  - Kimi `~/.kimi-code/config.toml:1478` pins `rea-agents@6.4.0`: 170 tools
    (L8/L15), 127 CLI (L5), catalog `25802f6d…` (L12), expects skill v37,
    doctor `stale` (l10-doctor-6.4.0).
  - Ghidra 12.1.4 (build 2026-Sep-21) and JDK 21.0.12.1 re-verified (L11).
  - Operator configs hash-identical before/after the wave (S2/S5).
- Boundary adjudication (conflicting seats resolved by parent): Core-table
  probe cells are dated 2026-10-13 records — kept byte-identical (E4, A6);
  the Core row's present-tense "all spawn `rea-agents@6.4.0`" config clause
  was current-surface and is reconciled per-client (P0, B5). Coverage-map
  evidence cells and LOG/lessons untouched.
- Guards: F1 availability→holding guard list applied; G3 point-in-time pass
  CLEAN; F7 final pass CLEAN (no wrong-client pairing, no running-process
  implication); G9 receipt fidelity confirmed all E-draft numbers (one stale
  hash in B2 — named debt, not in the edit path); B5 completeness check found
  no missed current-surface claims outside the declared union.
- Integration: 7 edits across PROVINCE.md (surface summary, drift-prone
  values, Core spawn clause) and SKILL.md (Domain sentence marked historical,
  dated per-client inventory paragraph, two checklist rewordings). Work commit
  `75af886a` under lane identity.

## Landed changes

- `PROVINCE.md` + `SKILL.md` — commit `75af886a` (lane identity).
- `LOG.md` + `SCORECARD.md` + this report — bookkeeping commit (below).
- Historical records (Core probe cells, coverage-map evidence cells, LOG,
  lessons) byte-identical; operator configs untouched.

## Before → after measurements

Receipt-backed census (the acceptance evidence): every number in the new text
resolves to a hashed 2026-10-16 receipt (G9). Token census (F2 command,
guard only): PROVINCE surface {6.4.0} → {6.4.0, 6.5.0}; drift-prone
{6.4.0, skill:v37} → {6.4.0, 6.5.0×2}; SKILL domain {6.4.0×2} →
{6.4.0×2, 6.5.0}. Side-harm check, command A at `75af886a`: mapped 72,
missing [], dangling [], coverage 10.0, depth 10.0 (9/9 rules). Limit
declared up front: receipts prove configured pins and package inventories —
both doctor runs exit 1 with `live_server: unknown`; no running-client
process identity and no tool *holding* is claimed anywhere.

## Process defects (recorded, not hidden)

- Parent dispatched 58 seats, not the contracted 64; caught at wave close,
  repaired with a 6-seat backfill (R9, G9, F7, L15, S5, B5) before any
  integration. Round seat total: 64 across two batches.
- Mid-round: the first drift-prone heading draft broke F2's census anchor;
  caught by running the census; heading + work commit amended before records.
- Seat-level: G1 found L1's claimed stdout hash omits a trailing LF (receipt
  content verified correct by replay); D3 (round 1) class of miscount guarded
  by direct parent measurement this round; B2 cites a stale L7 receipt hash
  (named debt for its owning round); G9 notes E-draft dates derive from the
  wave date rather than receipt bytes (attested by wave dir + this report).
- R8/G8: SHONEN remains 4×[~] — parent-dispatched seats do not satisfy the
  fleet's named non-author verifier bar.

## SHONEN

- [~] decision tables/citations: unchanged (no semantic SKILL audit).
- [~] e2e task executed: unchanged (no new e2e; live probes were inventory
  censuses, logged with receipts).
- [~] executable without oral context: unchanged (recipes replayed by
  multiple seats; no box-specific verifier).
- [~] no cross-domain bleed: unchanged (K1 recorded tsukuroi/kama/mori
  boundaries; configs read-only).

## Verdicts

- calibration: **improved** (current surface reconciled to receipted live
  inventory; no inference beyond receipts).
- coverage: **unchanged** (10.0 measured at the round commit).
- depth: **unchanged** (10.0, 9/9 rules measured at the round commit).
- Learning: expansion unchanged; quality improved (surface now matches
  receipts; 6.5-only name set recorded as inventory); discernment unchanged
  (attacks ran, none survived).
- Admitted: yes — one axis improved, none harmed.
