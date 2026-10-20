# DraftLessonSkeleton — round-18 lesson draft (w1, advisory, read-only)

Seat: KaidokuR18.DraftLessonSkeleton (leaf; no subagent dispatch). Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Baseline B = 9011581d84527ba34c675f9cf912e54d2e72d470 (`.ufo/waves/round-18/claims.json:4`).

Assignment: draft the `corpus/lessons/round-18.md` skeleton in the shape of `corpus/lessons/round-17.md` (`## Gate`, `## Mistakes` with rows R17-VALIDATE16, R17-PINMAP, R17-SUMS-RUNLOG), using the facts in `corpus/lessons/round-17-verifier-spotcheck.md`. No lane file was edited. The draft is in the `## Draft` section below; the L1 integrates it.

## Findings (calibration of the spot-check anchors, read-only)

Method: `read`, and read-only `git show` / `git diff` / `git log` / `git rev-parse` in the lane (no `jj`, no git writes, no REA, no carrier execution). Each anchor the spot-check cites was re-opened at the revision named below.

- F1 R17-PINMAP anchor holds. `.ufo/waves/round-17/tools/carrier-run.py:481-487` appends `{taken_at_utc, equal, entries: len(mid["entries"]), changed, missing}` and no map. The string `map_sha256` is not in that block (`carrier-run.py:475-487`, read in the working tree). This matches `corpus/lessons/round-17-verifier-spotcheck.md:137`.
- F2 The knowledge pin sentence sits at `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:29-32` ("each pin map is retained with its UTC instant … All maps are equal"). The spot-check cites `:30-32` (`round-17-verifier-spotcheck.md:108`, `:137`). The draft cites `:29-32`. Minor anchor offset.
- F3 `SCORECARD.md:2364` ("all 16 receipts `receipt-validate.py` exit 0") and `:2374` ("carries pre/mid/post pin maps with instants") hold at B: `git show 9011581:SCORECARD.md | grep -c 'all 16 receipts'` → 1; the `:2374` row is read from the working tree SCORECARD.md.
- F4 The "round-17.md:122" cited at `round-17-verifier-spotcheck.md:138` is ambiguous as written. `.ufo/waves/round-17/round-17.md` does not exist (`_grep` skipped path). The file meant is `corpus/lessons/round-17.md:122` ("All 16 receipts pass the final validator"), read in full. The L1 should cite the full path when the defect is closed.
- F5 Candidate un-routed instance of the R17-PINMAP wording: `LOG.md:2097-2100` (at B) says "Mid-run pin checks retained: 2–8 per run, all equal." The spot-check routes only `SCORECARD.md:2374` and the knowledge entry (`round-17-verifier-spotcheck.md:137`). "all equal" is literally true of the `equal` verdict field; the overstatement is the word "retained". Classified here as a candidate to check, not a confirmed defect.
- F6 R17-VALIDATE16 evidence confirmed. At `b31975de62de5413a6f2d244f2690eaeb3d18c25` (evidence revision), `.ufo/waves/round-17/verification.json` contains 8 `"label": "receipt-validate-<carrier>"` entries (all on `runs/<label>/receipt.json`, A receipts) and 0 references to `da64646` (`git show b31975de…:.ufo/waves/round-17/verification.json | grep -c …`). `da64646` has no `verification.json` at all (`git show da64646:… → fatal: path … exists on disk, but not in 'da64646…'`). So no validator run over the 8 da64646 receipts exists in the retained evidence. This matches `round-17-verifier-spotcheck.md:71` and `:138`.
- F7 R17-SUMS-RUNLOG, the loss is narrower than the spot-check range. `predictions/SHA256SUMS` contains a `predictions/carriers.tsv` line at `2711674` and at `da64646` (1 line each), and none at `de6c721` (A) or `9011581` (B). `git diff 2711674 9011581 -- .ufo/waves/round-17/predictions/SHA256SUMS` is a 1-line deletion (`8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv`) plus a 1-line insertion (`f5ce3d6ba0da04749a65f63295540f82610e13adfe931fb39c67be75b7cb72d5  predictions/replicate-expectations.json`). `git log -- …/SHA256SUMS` lists only `2711674` and `95e34db` (`2026-10-20 11:27:35 -0300`, "w2-hardened tools and frozen replicate expectations (pre-rerun)"). So the line was replaced in place at `95e34db`, not dropped in a generic window. The carriers.tsv blob is `e232bf2bdcc607bcb577d1fb788b785cc6821188` at 2711674, de6c721 and 9011581 (unchanged, as `round-17-verifier-spotcheck.md:141` says), and `sha256sum` of that blob is `8ac38afe…d3eb5`, equal to the removed line's sha. The fix can restore that exact line.
- F8 R17-SUMS-RUNLOG "7/8" is a `da64646` statement only. `git show da64646:.ufo/waves/round-17/runs/run-log.txt` lists 7 labels (calib-shfmt absent) and ends at `== pro-op end … carrier-run=0 compare=0`, with no `run-carriers exit=` line. This matches `round-17-verifier-spotcheck.md:142`. The second-pass working-tree `.ufo/waves/round-17/runs/run-log.txt:2-18` lists 8 labels and ends `run-carriers exit=0`. The LOG.md check in `contract.md:40` ("7/8") must name the `da64646` revision, or it will be misread against the second pass.
- F9 Operability: `contract.md:33-35` requires the validate16 summary at `da64646` with exactly 8 receipts, each with an int `exit`. The spot-check's "retain the validator run over `git show da64646:…/runs/*/receipt.json`" option (`round-17-verifier-spotcheck.md:138`) is therefore the one the contract's check admits; the "correct the count to 8" option would fail `contract.md:33-35`. The L1 should pick the retain option.

Overall calibration: the three Mistakes rows are supported by the spot-check's own anchors; F1, F3, F6, F7 and F8 are confirmed at pinned revisions. The draft keeps the spot-check's routing and does not add facts beyond them except as labelled in this Findings section.

## Draft

The draft is verbatim below. Fields that depend on round-18 results are written as `filled at integration`.

```markdown
# Round 18 — kaidoku: routed round-17 defects, jj-safe revision pins, Swiss-map minimal pair

author: kaidoku-shokunin; 2026-10-20
scope: round-18 draft skeleton. Baseline `9011581d84527ba34c675f9cf912e54d2e72d470` (`.ufo/waves/round-18/claims.json:4`). Shape follows `corpus/lessons/round-17.md:1-8` and `:24-` (Gate, Mistakes). Every field whose value depends on round-18 results reads `filled at integration`.

## Claims

- C1 calibration (routed round-17 defects): discharge the six defects routed at `corpus/lessons/round-17-verifier-spotcheck.md:137-147` (R17-PINMAP, R17-VALIDATE16, R17-PRODUCER-REV, R17-SUMS-RUNLOG, R17-REGISTRY, R17-S032-DIGEST) and turn the one partial outside disagreement into a lesson-backed QUALITY criterion (`.ufo/waves/round-18/claims.json:12`; `corpus/lessons/round-17-verifier-spotcheck.md:108`). Falsifiable: open routed defects 6 at `9011581` → 0 at the delivered revision (`.ufo/waves/round-18/claims.json:13`).
- C2 operability (jj-safe pins): the three HEAD-keyed revision sites read the branch tip (`.ufo/waves/round-18/claims.json:18-19`). Falsifiable: live HEAD-as-revision call sites 3 → 0 (`.ufo/waves/round-18/claims.json:20`).
- C3 depth (Swiss-map minimal pair): eight deterministic synthetic carriers, frozen predictions, retained run-bound logs (`.ufo/waves/round-18/claims.json:26-27`). The round-17 aether mechanism stays an INFERENCE until replayed (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:145-164`).

## Gate

### Candidate decisions (author-side; outside sampling remains the closure's duty)

| Candidate | Decision | Evidence and limits |
|---|---|---|
| C1 — R17-PINMAP: named correction or retained mid maps | filled at integration | Routed at `corpus/lessons/round-17-verifier-spotcheck.md:137`; checks at `.ufo/waves/round-18/contract.md:29-32` |
| C1 — R17-VALIDATE16: retained validator run over the 8 `da64646` receipts, or count corrected to 8 | filled at integration | Routed at `corpus/lessons/round-17-verifier-spotcheck.md:138`; summary check at `.ufo/waves/round-18/contract.md:33-35` |
| C1 — R17-PRODUCER-REV: name the producing revision per pass | filled at integration | Routed at `corpus/lessons/round-17-verifier-spotcheck.md:139`; check at `.ufo/waves/round-18/contract.md:36-37` |
| C1 — R17-SUMS-RUNLOG: restore the `carriers.tsv` line; qualify the `7/8` run-log statement | filled at integration | Routed at `corpus/lessons/round-17-verifier-spotcheck.md:140-143`; check at `.ufo/waves/round-18/contract.md:38-40` |
| C1 — R17-REGISTRY and R17-S032-DIGEST | filled at integration | Routed at `corpus/lessons/round-17-verifier-spotcheck.md:144-147`; checks at `.ufo/waves/round-18/contract.md:41-45` |
| C1 — open routed defects, `routed-defects.py --strict` | filled at integration | `.ufo/waves/round-18/contract.md:26-47`; baseline value `6` per `.ufo/waves/round-18/claims.json:13` |
| C2 — jj-safe pins (`head-rev-lint.py`, `revpin.py`, `jj-red-before.py`, in-place fixes) | filled at integration | `.ufo/waves/round-18/contract.md:51-98`; baseline live sites `3` per `.ufo/waves/round-18/claims.json:20` |
| C3 — Swiss-map minimal pair, eight carriers | filled at integration | `.ufo/waves/round-18/contract.md:100-120`; `.ufo/waves/round-18/claims.json:26-27` |
| QUALITY row 21 (C1 criterion) | filled at integration | `.ufo/waves/round-18/claims.json:13` |

Admitted: filled at integration. Rejected: filled at integration.

### Outside spot-check

Pending non-author closure. This lesson does not record an outside decision. The round-17 closure's sample is at `corpus/lessons/round-17-verifier-spotcheck.md:96-109`; its one partial disagreement (the pin-map sentence) is at `:108` and is routed at `:137`. The round-18 closure's sample: filled at integration.

### Registry transitions

filled at integration.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| number-drift — R17-VALIDATE16 | `SCORECARD.md:2364` says "all 16 receipts `receipt-validate.py` exit 0" and `corpus/lessons/round-17.md:122` says "All 16 receipts pass the final validator" (both as cited at `corpus/lessons/round-17-verifier-spotcheck.md:138`). Only 8 of the "all 16" validations are retained (`corpus/lessons/round-17-verifier-spotcheck.md:71`); `verification.json` retains 8 `receipt-validate-*` runs, all on the A receipts; the 8 `da64646` receipts have only w2 seat prose (`corpus/lessons/round-17-verifier-spotcheck.md:138`) | outside closure (`corpus/lessons/round-17-verifier-spotcheck.md:71`, `:138`); the spot-check records no lane-side capture | Retain the validator run over `da64646:…/runs/*/receipt.json`, or correct the count to 8 (`corpus/lessons/round-17-verifier-spotcheck.md:138`). Acceptance: `.ufo/waves/round-18/evidence/validate16/summary.json` with `rev` = `da64646adcb19c1ede7537b799b8c7d283fe43da` and 8 receipts each with an int `exit` (`.ufo/waves/round-18/contract.md:33-35`). Result: filled at integration |
| overstatement — R17-PINMAP | `carrier-run.py` records each mid-run pin check as `{taken_at_utc, equal, entries, changed, missing}`, not a per-path map (`.ufo/waves/round-17/tools/carrier-run.py:481-487`; `corpus/lessons/round-17-verifier-spotcheck.md:137`). The knowledge entry says "each pin map is retained … All maps are equal" (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:29-32`) and `SCORECARD.md:2374` says "pre/mid/post pin maps with instants" (`corpus/lessons/round-17-verifier-spotcheck.md:137`). QUALITY #19 requires the map (`corpus/lessons/round-17-verifier-spotcheck.md:137`) | outside closure discernment sample, partial disagreement (`corpus/lessons/round-17-verifier-spotcheck.md:108`); the spot-check records no lane-side capture | Either retain mid maps (or their digest), or append a named correction: "mid-run instants retain the comparator verdict against the retained pre map, not the map" (`corpus/lessons/round-17-verifier-spotcheck.md:137`). Acceptance: `.ufo/waves/round-18/contract.md:29-32` (knowledge line with `R17-PINMAP` and `comparator verdict`; SCORECARD line; QUALITY row whose why-cell cites the spot-check and `R17-PINMAP`; `carrier-run.py` contains `map_sha256`). Result: filled at integration |
| landing / reference-drift — R17-SUMS-RUNLOG | `predictions/SHA256SUMS` lost its `carriers.tsv` line between `2711674` and the A revision; the file is unchanged, but the frozen manifest no longer covers it (`corpus/lessons/round-17-verifier-spotcheck.md:141`; also `:75`). The pass-1 `runs/run-log.txt` at `da64646` lists 7/8 carriers and has no final exit line (`corpus/lessons/round-17-verifier-spotcheck.md:142`) | outside closure (`corpus/lessons/round-17-verifier-spotcheck.md:74-75`, routed at `:140-143`); the spot-check records no lane-side capture | Restore coverage and append the correction (`corpus/lessons/round-17-verifier-spotcheck.md:143`). Acceptance: `.ufo/waves/round-17/predictions/SHA256SUMS` has `<sha>  predictions/carriers.tsv` equal to the blob sha at REV, and `LOG.md` has a line containing `R17-SUMS-RUNLOG` and `7/8` (`.ufo/waves/round-18/contract.md:38-40`). The `7/8` statement names revision `da64646`. Result: filled at integration |

## Integration boundaries

filled at integration.
```

## Commands run (read-only; no installs)

- `git rev-parse --verify 9011581d84527ba34c675f9cf912e54d2e72d470^{commit}`, `… da64646adcb19c1ede7537b799b8c7d283fe43da^{commit}`, `… 2711674^{commit}`, `… de6c721^{commit}`, `… b31975de62de5413a6f2d244f2690eaeb3d18c25^{commit}` (all resolve).
- `git show da64646:.ufo/waves/round-17/runs/run-log.txt`.
- `git show <r>:.ufo/waves/round-17/predictions/SHA256SUMS | grep -c 'predictions/carriers.tsv'` for `2711674`, `da64646`, `de6c721`, `9011581` → 1, 1, 0, 0.
- `git rev-parse <r>:.ufo/waves/round-17/predictions/carriers.tsv` for `2711674`, `de6c721`, `9011581` → `e232bf2bdcc607bcb577d1fb788b785cc6821188` (all three); `git show 2711674:…carriers.tsv | sha256sum` → `8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5`.
- `git diff 2711674 9011581 -- .ufo/waves/round-17/predictions/SHA256SUMS` (1 deletion, 1 insertion); `git log --format=… -- .ufo/waves/round-17/predictions/SHA256SUMS` → `95e34db`, `2711674`.
- `git show b31975de62de5413a6f2d244f2690eaeb3d18c25:.ufo/waves/round-17/verification.json | grep -c '"label": "receipt-validate-'` → 8; `… | grep -c da64646` → 0; `git show da64646:…verification.json` → fatal (not in `da64646`).
- `git show 9011581:SCORECARD.md | grep -c 'all 16 receipts'` → 1.
- `read` of `.ufo/waves/round-17/tools/carrier-run.py:475-493`, `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`, `corpus/lessons/round-17.md`, `corpus/lessons/round-17-verifier-spotcheck.md`, `.ufo/waves/round-17/predictions/SHA256SUMS`, `.ufo/waves/round-17/runs/run-log.txt`, `SCORECARD.md`, `.ufo/waves/round-17/verification.json`, `.ufo/waves/round-18/{claims.json,contract.md}`.

## Tools

No tools installed or updated. No REA, Ghidra, carrier, `jj` or git write was run. No file in the lane was edited except this report.

## Open for the L1

- Choose the R17-PINMAP fix: retain mid maps, or the named correction (`corpus/lessons/round-17-verifier-spotcheck.md:137`).
- Choose the R17-VALIDATE16 fix: the contract's summary check (`.ufo/waves/round-18/contract.md:33-35`) admits the retain option only.
- Decide whether `LOG.md:2097-2100` (F5) joins the R17-PINMAP routing.
- Cite `corpus/lessons/round-17.md:122` by full path; `.ufo/waves/round-17/round-17.md` does not exist (F4).
