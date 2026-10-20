# QualityLineage — author-side advisory

Axes: **calibration**, **freshness**, **depth**.

## Finding

- **Observation:** QUALITY #18 requires execution evidence to retain the producing argv/snippet, measured revision, stdout/stderr and exit; #21 limits retention/compliance claims to keys actually retained and validator fields actually recomputed (`corpus/QUALITY.md:28,31`). The R18 strict-baseline defect is therefore already covered by #18: the missing strict/red receipt is missing execution evidence, not a new admission-rule gap (`corpus/lessons/round-18-verifier-spotcheck.md:195`).
- **Observation:** QUALITY #8 already requires capability claims to pin tool/provider versions and their source, while round-19 C2 explicitly plans a live-config comparison probe for PROVINCE's stated pins (`corpus/QUALITY.md:18`; `.ufo/waves/round-19/claims.json:17-20`). The PROVINCE drift belongs to that freshness correction, not a separate #22 (`corpus/lessons/round-18.md:88`).
- **Observation:** The R18 routed list also contains receipt-validator, alias-guard, registry, and install-record defects (`corpus/lessons/round-18-verifier-spotcheck.md:193-199`). These are concrete tool/record corrections; folding them into one broad admission criterion would duplicate the routed fixes rather than identify a shared bar gap (`corpus/lessons/round-18-verifier-spotcheck.md:193-199`).
- **Observation:** The seat-status issue is distinct: SCORECARD records one dead and four not returned “at integration” (`SCORECARD.md:2462`); the filed report records two dead and two not returned at integration, with other seats returning late (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:84`); its appended erratum says TruthREGISTRY then died and ShonenLines had not returned when the erratum was written (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:99-101`). The spot-check says committed W2 records lack failure text and routes the discrepancy (`corpus/lessons/round-18-verifier-spotcheck.md:146,197`).
- **Inference:** #18's execution-evidence rule and #21's producer-output retention rule do not explicitly require a round-status claim to name its cutoff or to preserve each seat's disposition and cause (`corpus/QUALITY.md:28,31`). A count difference across cutoffs is not itself proof that one snapshot is wrong; a new row should require explicit cutoffs rather than flattening distinct snapshots (`SCORECARD.md:2462`; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:84,99-101`).

## Draft

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 22 | A round-seat status claim names its observation cutoff, distinguishes terminal failures from seats not yet returned at that cutoff, and is reproducible from retained per-seat dispositions; each terminal failure cites its retained cause or is explicitly marked unknown, and later reclassifications are appended with their new cutoff rather than silently rewriting the earlier snapshot. | `corpus/lessons/round-18-verifier-spotcheck.md:146,197` (R18-DEADSEAT-RECORD) | — |

## Effects and risks

- **Calibration (improves):** avoids treating “not returned at integration” as a final dead-seat disposition and requires the count to match the retained per-seat record (`SCORECARD.md:2462`; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:84,99-101`).
- **Freshness (improves):** explicit cutoffs distinguish an integration snapshot from a later erratum instead of making stale and updated statuses look simultaneous (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-18/kaidoku.md:84,99-101`).
- **Depth (improves):** retaining a cause or explicitly unknown disposition preserves failure information beyond a headline count (`corpus/lessons/round-18-verifier-spotcheck.md:146,197`).
- **Risk (inference):** an overly broad version could pull fleet orchestration into artifact-analysis admission; keep the row scoped to claims about round-seat status and allow an explicit unknown cause rather than requiring unsupported attribution (`corpus/QUALITY.md:1-4`; `corpus/lessons/round-18-verifier-spotcheck.md:146,197`).

## Verification

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin --no-optional-locks diff --exit-code 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- corpus/QUALITY.md` returned exit 0; #1–#21 remain as read in `corpus/QUALITY.md:9-31` (command result; current main includes the round-19 dispatch commit).
- Read-only review only; no tests, builds, validators, or tools were run. No tool was installed or updated.