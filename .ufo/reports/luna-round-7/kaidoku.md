# kaidoku luna-round-7 — coverage: six 6.5.0-verb knowledge entries

Date: 2026-10-16. Axis: **coverage**. Third 128-seat two-lane wave
(64 luna + 59 commissioned deepseek + 5-seat backfill).

## Work performed

- Six knowledge entries drafted from luna-round-6's cross-lane receipts,
  with per-verb evidence verifiers, drafters, second-opinion drafters,
  convergence seats, QUALITY gates, and adversaries. The integration
  seat compiled FINAL-MANIFEST.md with every wave correction applied
  (see Landed changes).
- Instrument catch with fleet-wide value: the original filename plan used
  verb names with underscores, which command A's map-token regex
  (`[a-z0-9-]+`) truncates — three independent simulations showed
  mapped=72/coverage 9.23; hyphenated slugs yield 78/78. Parent ruling:
  hyphenated filenames, verb names verbatim inside entry bodies.

## Landed changes

- `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md` …
  `l7-06-inspect-with-objdump.md` — six entries, all carrying
  source:/verified-at:/recheck: metadata, observation/inference/unknown
  labels, carrier path+SHA-256, receipt citations, and RESULT-class-only
  claims. Notable wave rulings: entry 2 keeps the lane-A Signal `.node`
  and lane-B `/usr/bin/rg` carriers as distinct observations; entry 4
  admits only lane-B's hash-pinned pnpm-index result (lane A's synthetic
  fixture excluded per QUALITY criterion 12); entry 3 transcribes the
  provider's exact fuse names, resource bounds, and four limitations.
- `corpus/README.md` — six 3-cell map rows after r14-02 + six 4-cell
  Knowledge rows at the table end — commits `1cfd2a3` (six files) +
  `3395b6d` (twelve rows), both lane identity.
- Bookkeeping commit (below).

## Before → after measurements

Command A at `3395b6d`: `{"citation_resolved_rules": 9, "coverage_score":
10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 78,
"mapped": 78, "missing": [], "rule_blocks": 9}`. Prior-72 byte identity:
`git diff --name-only 411175e 3395b6d -- corpus/knowledge | grep -v l7-0 | wc -l` → 0.

## Findings & named debt

- E4V/S1's "round-6 receipts untracked" claims were FALSE — 26 receipt
  files are tracked at `bc91424` (parent re-verified; VB4 conceded). Seat
  misread class recorded.
- Q1–Q6 graded absence (drafts landed after their reads) — their criteria
  were re-applied by the QUALITY-gate and integration seats; recorded as
  timing artifacts, not content failures.
- BB1 composed entries 3 and 5 without a prior gate pass on those exact
  bytes (disclosed in FINAL-MANIFEST THREATS); both were reviewed by
  QB3/QB5 gates + the wave's adversaries.
- Knowledge table now 79 rows for 78 files (the lessons-only row
  precedent, confirmed by RB7).
- SC1–SC6 scout reports remain untracked auxiliaries (receipts are the
  tracked anchors) — fleet convention question for the integrator.

## SHONEN

- [~] ×4 unchanged (SH1): entries strengthen box 1's evidence but the
  named-non-author verifier bar stands; no promotion claimed.

## Verdicts

- coverage: **improved** — six exercised verbs became admitted,
  quality-gated knowledge at denominator 78 (index completeness held).
- depth / calibration / freshness / operability: **unchanged** (measured
  where applicable).
- Learning: expansion improved; quality improved (QUALITY-12 enforced,
  metadata now standard); discernment unchanged.
- Admitted: yes — one axis improved, none harmed.
