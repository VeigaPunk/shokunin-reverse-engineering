# kaidoku luna-round-9 — freshness: carried-spill queue

Date: 2026-10-16. Axis: **freshness** (fleet axis, unowned proxy). Fifth
two-lane wave (128 seats). Four carried items, each with full
verifier/drafter/adversary/reviewer chains and dual lane-B gates.

## Work performed

- **Item 1 — r4-16 L197 cross-reference:** the file's r12-01 erratum block
  still summarized the old two-site account; landed an EOF erratum pointing
  to r12-01's corrected four-site account (:99-104) + round-5 erratum
  (:110-120), with "7 values" explicitly attributed (receipts gone).
- **Item 2 — census instrument limits:** documented in this SCORECARD
  section as ADJUDICATED-not-PASS with pointers to both adjudicated
  instances (round-5 SIZES comma-token; round-4 F18 replacement-encoding;
  round-5 opener-detector) and a retest trigger. Home ruling: SCORECARD
  (instrument debt already lives here); corpus/QUALITY.md rejected as
  admission doctrine.
- **Item 3 — /tmp dependence audit:** NO current lane instruction, gate, or
  landed recheck requires pre-existing /tmp contents; historical
  verify-recipes citing /tmp outputs are labeled archival debt; L7-01
  cold-cache untested; ~1.2 GB litter remains operator hygiene — no
  deletion authorized or performed (RB3: "no freshness-improvement claim
  from item 3 alone" — the round's improvement rests on items 1/2/4).
- **Item 4 — jq-shadow safety-verdict scope:** all four "benign" loci
  named and qualified — historical wording asserting only recorded
  byte-identity + agent-initiated provenance, explicitly not a
  safety/trust/reuse verdict per PROVINCE.md:114-116. Qualification
  chosen over retraction (D3's argument overruled: qualification preserves
  the byte-identity finding).

## Landed changes

- Two append-only knowledge errata — commit `40162fc` (lane identity),
  prefix-identity verified against base blobs.
- SCORECARD: this round's section (known-limits + /tmp audit).
- Bookkeeping commit (below).

## Before → after measurements

Command A at `40162fc`: 79/79 mapped, 9/9 rules, 10.0/10.0, missing []
dangling []; both appended files byte-prefix-identical to their a280e07
blobs; PROVINCE byte-identical (8a1cec88); zero deletions; changed paths ⊆
{the two knowledge files, SCORECARD.md, LOG.md}.

## Findings & carried debt

- Steer drift corrected in-wave: PROVINCE safety refusal is at :114-116
  (not the steered :107-109); two stale :107-109 pointers survive at
  SCORECARD.md:79 (inside the frozen 2026-10-15 reconciliation table —
  untouchable by design) and lessons/2026-10-15-round-1.md:152-153
  (historical) — named debt.
- r3-jq-provenance companion bleed (:60,:136) — named debt for a future
  round (out of this round's four-item scope).
- Lane-B stragglers: VB3 absent (no third-seat review for item 3 — RB3's
  findings stand on A-chain + C-gates).

## SHONEN

- [~] ×4 unchanged (X1/RB8).

## Verdicts

- freshness: **improved** (items 1/2/4 landed; item 3 dispositioned with
  no improvement claim).
- coverage / depth / calibration / operability: **unchanged** (measured).
- Learning: expansion unchanged; quality improved (instrument limits +
  safety-scope enforced); discernment unchanged.
- Admitted: yes — one axis improved, none harmed.
