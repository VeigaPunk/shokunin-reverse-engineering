# arc3-loop1-round5 — kaidoku-shokunin — round report

**Schedule slot:** R5 — 64 seats, `openai-codex/gpt-6-luna-max`.
**Executed as:** the scheduled provider, no fallback. All 64 seat reports
delivered (16 c1 + 16 c2 + 16 c3 + 12 verdicts; the 4 TB seats map to c1).
**Work commit:** `58c3db7`. **Records commit:** this commit.
**Round type:** the arc's scheduled correctness sweep — a wave dispatched
specifically to re-derive rounds 1–4 and disposition the arc2 carried debt.

## Work performed

- **Aggregated the three claim reports** the frozen claim required and no seat
  wrote: `claims/c1/sweep-report.md`, `claims/c2/audit.md`,
  `claims/c3/disposition.md` — each consolidated from the seat artifacts with
  per-row seat pointers.
- **Landed the corpus corrections the audit caught**, append-only:
  - `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md` — erratum: the
    `:17` initcode-absence sentence (runtimes byte-embedded at +20/+24/+27 —
    parsed-and-empty is the probe result, not byte absence), the `:21`
    CODECOPY wording (2-byte entry, not the 26-byte table), the `:30`
    "no Core promotion" sentence (superseded by `40de383`'s own PROVINCE
    `Core, arc3-r4` wording), and the `Ex09Vault` input-text provenance
    (recorded UNVERIFIABLE, not a runtime-digest defect).
  - `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md` — erratum:
    the `:24` initcode wording (same class; offsets measured) + the
    matrix-only roster rows recorded UNVERIFIABLE (evidence not retained).
  - `corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md` — erratum: the
    `:15` Smoke digest domain (685 B decoded ↔ `08299f31…`; `530efc7b…` is
    the 1,370 B ASCII-hex file's digest).
- **Fixed the records the sweep flagged:** SCORECARD "all nine stale literals
  cleared" → "eight cleared + one adjudicated NO-CHANGE (`JEB (unprobed)`
  survives at :88 by design)". The custody counting command's correct
  invocation is the positional `selftest` (the `--selftest` flag exits 2).

## Landed changes

- `58c3db7` — work commit: the three append-only corpus errata, the SCORECARD
  wording fix, and the committed wave tree `.ufo/waves/arc3-loop1-round5/`
  (64 seat artifacts + the three aggregates).
- This records commit — SCORECARD section, LOG entry, this report.

## Before → after measurements

| claim | before | after | evidence |
|---|---|---|---|
| C1 calibration | arc3 r1–r4 numbers recorded but not independently re-derived | every scoped number reproduced (command A 82→84 at 7 revisions; census PASS; drift 0/0; custody 28/28; PROVINCE 162; Vyper 15/15 + sha) with **5 named discrepancies corrected** | `claims/c1/sweep-report.md` discrepancy ledger |
| C2 coverage | 3 dated entries landed, not per-claim audited | per-claim audit done: selectors/identities/shapes VERIFIED; **2 real defects + 2 domain fixes landed append-only**; matrix-only rows + Carrier-3 offsets recorded UNVERIFIABLE | `claims/c2/audit.md` + the three errata |
| C3 freshness | 3 arc2 debt items open | 3 rulings recorded: mid-leg STOPPED (operator-gated), r10 deficit DISCHARGED-BY-PRECEDENT (corrected set), census CARRIED-forward | `claims/c3/disposition.md` |

Instruments at `58c3db7`: command A 84/84 mapped, 14/14 rules, coverage/depth
10.0/10.0; `c1-census-v10.py` PASS; citation-drift `findings=0` both modes;
custody selftest `CLEAN 28/28`; `PROVINCE.md` 162 lines.

## Axis verdicts (per-axis, no scalar)

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | sweep reproduced the numbers + corrected 5 discrepancies |
| coverage | **improved** | audit verified the corpus + landed 4 append-only fixes |
| freshness | **improved** | 3 debt rulings recorded; arc2 administrative debt discharged |
| depth | unchanged | 10.0 → 10.0 |
| operability | unchanged | custody 28/28, probe 0/0 |
| adjacency | unchanged | PROVINCE boundary untouched; no cross-lane writes |

Admission: all three claims verified — the sweep produced its report, the
audit produced its table + corrections, the debt produced its three rulings —
and no axis harmed → **admitted**.

## The sweep's yield (why this round was worth a provider slot)

A 64-seat wave dispatched *only to find errors* found five: a genuine
initcode-absence defect carried by both the r3 and r4 entries (the probe
parses empty but the runtime bytes are present verbatim — exactly the
parsed-and-empty-vs-absence distinction `corpus/QUALITY.md:21` codifies), a
Core-promotion scope sentence contradicted by its own landing commit, a
CODECOPY wording error, a digest-domain mismatch, and a records
overstatement. This is the discipline the arc exists to train: the wave
measured first, reported the discrepancies with corrected values, and the
corrections landed append-only — never rewrites.

## Carried debt (named, not smoothed)

1. **Mid-leg faithful retest stays open, operator-gated** — the one
   substantive arc2 item; it discharges only on operator authorization of the
   ~20 GiB host cost.
2. Census Frontier blind spot (R1) + `ptr_check` pinned-clause blind spot (R2).
3. r3 matrix-only roster rows + r3-07 Carrier-3 offsets: UNVERIFIABLE,
   evidence not retained (recorded, not corrected).
4. `.ufo/waves/arc2-loop1-round10/C3.md` still dirty; `/tmp` quota standing.

## SHONEN

- `[~]` SKILL.md real decision tables / cited sources — asserted
  `SKILL.md:81-255`; this round added no rule blocks; no named non-author
  verifier.
- `[~]` end-to-end domain task executed and logged — the sweep itself is the
  logged task (re-derivation → discrepancy → append-only correction).
- `[~]` instructions executable without oral context — the sweep recipe +
  discrepancy ledger + correction procedure are recorded in the three
  aggregate reports.
- `[~]` no cross-domain bleed — PROVINCE boundary untouched; corrections are
  corpus-internal and append-only.
