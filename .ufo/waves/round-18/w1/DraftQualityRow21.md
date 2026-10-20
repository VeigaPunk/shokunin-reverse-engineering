# DraftQualityRow21 — QUALITY.md admission row #21 (draft, read-only lane)

Author-side advisory draft. No lane file was edited. The L1 (KaidokuR18) integrates.

## Draft

Placement: insert after `corpus/QUALITY.md:30` (row 20), before the blank line at `:31` and `## Signals of weak material` at `:32`. Table shape copied from `corpus/QUALITY.md:9-10` (header `| # | criterion | why (lesson) | supersedes |`, separator row) and four cells per row, as in `:29-30`.

```text
| 21 | A retention claim names each field the producing tool retains (for a pin check: `taken_at_utc`, the per-path map with SHA-256 and size, and the comparator verdict) and states a field is absent when the tool does not retain it; a comparator verdict (`equal`, `changed`, `missing`, an entry count) is never described as the compared object (the map, the bytes, the file) | `corpus/lessons/round-17-verifier-spotcheck.md` R17-PINMAP (`:108`, `:137`: mid-run `pin_checks` keep `{taken_at_utc, equal, entries, changed, missing}`, not the map; `carrier-run.py:481-486`); `corpus/lessons/round-18.md` | sharpens 19 |
```

## Evidence (path:line or command source)

- Partial outside disagreement: `corpus/lessons/round-17-verifier-spotcheck.md:108` marks the knowledge pin sentence "partial disagree", because "mid-run instants keep a comparator verdict and count, not the per-path map QUALITY #19 itself requires".
- Routed defect R17-PINMAP: `corpus/lessons/round-17-verifier-spotcheck.md:137` names the same gap and cites `carrier-run.py:481-486`.
- Producer fields: `.ufo/waves/round-17/tools/carrier-run.py:481-486` appends exactly `taken_at_utc`, `equal`, `entries` (`len(mid["entries"])`), `changed`, `missing`. The map itself is not appended. The comment at `:475` reads "Every check is retained with its instant (QUALITY #19), not only drift."
- Observed record: read of `.ufo/waves/round-17/runs/pro-aether/receipt.json?q=.steps.analyze.pin_checks&compact=true` returned three entries, each with keys `changed`, `entries` (146), `equal` (true), `missing`, `taken_at_utc`. No per-path map field is present.
- Absence of a map on disk: `grep` pattern `map_sha256|pin_checks|pins/mid` over `.ufo/waves/round-17/tools` matched only `pin_checks` lines (`carrier-run.py:481`, `receipt-validate.py:187,696`). No `map_sha256` and no `pins/mid` hit.
- Overstatement the row targets: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:28-33` says "each pin map is retained with its UTC instant … All maps are equal." `SCORECARD.md:2374` says the log "carries pre/mid/post pin maps with instants."
- Existing rule the row sharpens: `corpus/QUALITY.md:29` (row 19) already requires the producing tool to keep "each pin map (per-path SHA-256 and size) with its UTC timestamp and the comparison verdict, including mid-run checks." Row 21 does not restate that rule; it adds (a) an explicit field list for any retention claim and (b) the verdict-versus-object separation that the R17 disagreement exposed.
- Dependency: `corpus/lessons/round-18.md` does not exist yet (read of that path returned "not found"). The why-cell cites it, so the lesson must land (with a Mistakes entry for R17-PINMAP) before row 21 is admitted. The lesson skeleton is peer-owned (`KaidokuR18.DraftLessonSkeleton`); this report does not write it.
- Validator compatibility: `.ufo/waves/round-18/contract.md:29-32` (C1 R17-PINMAP check c) requires an admission-table data row whose why-cell contains `round-17-verifier-spotcheck.md` and `R17-PINMAP`. The draft row's why-cell contains both literal strings.
- Claims: `.ufo/waves/round-18/claims.json` C1 requires "QUALITY data rows 20 -> 21 with rows 1-20 byte-identical." The draft only appends after `:30`.

## Supersedes choice

`sharpens 19` is chosen over `—`. Reason: row 19 sets the pin-map requirement that the R17 sentence violated; row 21 narrows what a retention claim may name. If the L1 reads row 21 as a new rule rather than a narrowing, the cell may be `—` without other edits; the row text does not change.

## Limits and calibration

- Observation: the receipt and code lines above were read; no REA analyze, search, decompile, Ghidra run, or carrier execution was performed (contract forbids it for this seat).
- Inference: that the R17 sentence is a retention claim rather than a temporal claim. Row 19 covers temporal wording; row 21 covers retention wording in any form, so both can apply to the same sentence.
- Not verified: the round-18 `routed-defects.py` output (C1 tool, peer-owned, not run here). The why-cell's lesson link is unverified until `corpus/lessons/round-18.md` exists.
- Tools installed or updated by this seat: none.
