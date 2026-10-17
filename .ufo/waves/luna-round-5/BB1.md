# BB1 — r12-01 item-7 adjudication (Lane B backfill)

## CLAIM
Item 7 (PB0.md:15, P0.md:16): does the r12-01 main text still contradict the landed erratum :99-104, and is any append needed? Disposition + exact text.

## METHOD
Read-only at HEAD cfc84c2: `git show` (108 lines; worktree==HEAD, blob `8768ce77…`, sha256 `0a794bc1…`); source re-check of the four sites (rea-agents@6.4.0 dist, unblob 26.6.4); gates X1:39-40/C4:15-19 traced; candidate append simulated (no writes); /tmp scratch absent; split spot-checked (VB7/D7/G7/R2 no-append, C5/FB append).

## FINDINGS
1. Erratum adequate: :99-104 — "two classes across FOUR sites … 7 values"; marks the main count understated, non-reproducing. Sites source-verified: `FirmwarePublication.js:46` (`path=join(tree.outputRoot,…)`), `:59` (`output_directory=tree.outputRoot`); `FirmwareReports.js:157` (`provider_id=parsed.id`), `:198` (`provider_blob_id=child.blob_id`); unblob `identifiers.py:8-17` (`pid:counter`).
2. Main text still carries the superseded account at :13, :38, :40, :42, :67 — adjudicated by the erratum, un-rewritten by design.
3. "7 values" is not re-derivable (envelopes gone): quote attributed only; P0:16's "four variance classes" contradicts the erratum; V7's weakening rejected (sites source-supported).
4. Append need: none for the record (ADJUDICATED, existing erratum). But the wave's checks are baseline-tail-scoped: a no-append commit makes X1:39-40 read R12-01 DEBT, and C4:15-19 demands a new `## Errata (round 5 freshness` heading. Keep-machinery: land the pointer below (simulated PASS; adds the stale-loci map + numeral caveat); else amend X1:39-40 to full-text and drop C4's r12-01 clause.
5. Exact append (EOF; prefix-preserving; gates simulated PASS):

```text
## Errata (round 5 freshness, 2026-10-16, append-only)

- **L197 — main text superseded.** The "exactly two" normalized-values
  account (:13, :38, :40, :42, :67) is superseded by the round-12-audit
  erratum above (:99-104); this erratum supersedes main text at those loci.
  The true variance is two classes across FOUR sites — `files[].path`,
  `output_directory`, `chunks[].provider_id`, `derivations[].provider_blob_id`
  ("7 values" as recorded there; numeral attributed, not re-derived — the
  /tmp receipts are gone). Sites re-verified at source: rea-agents@6.4.0
  `FirmwarePublication.js:46,:59`, `FirmwareReports.js:157,:198`; unblob
  `identifiers.py:8-17`. Main text left as-written (append-only).
```

6. Adjacent (DB7:12, verified): rescan `2026-10-13-r4-16-frontier-rescan.md:751-752` (its r12-01 erratum :728ff) still carries the two-value account; optional one-line append, parent-owned.

## THREATS
Envelope byte-identity unverifiable (envelopes gone): adequacy argued from provider source, not the runs. Numeral suspect yet quoted (gate literals). Landing edits invalidate line anchors.

## VERDICT
FINDING: item 7 ADJUDICATED — erratum :99-104 already carries the four-sites correction (source-verified), main text stale by design; a pointer append is forced only by the tail-scoped census/gates — exact text above.
