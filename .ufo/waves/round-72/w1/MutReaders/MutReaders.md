# MutReaders — frozen round-72 reader mutations

Axes: behavioral discrimination, current selftest coverage, exact restoration, isolation.

All seven defects were applied separately to isolated copies of operative-freeze bytes. Each stage ran the same bounded detector (90-second subprocess timeout), with a caller canary and caller HOME outside the checker run root. No production sources changed. No tool installation.

| Mutant | Binding case | Selftest | Behavioral fixture | Exact restoration |
|---|---|---|---|---|
| a | git-reader-allowlisted-exec | survived | killed | True |
| b | checker-readelf-allowlisted-exec | survived | killed | True |
| c | implicit-capsule-polluted-raw-log | survived | killed | True |
| d | summary-canary-contradiction | killed | killed | True |
| e | sibling-prefix-escaped-HOME | killed | killed | True |
| f | summary-record-count-mismatch | killed | killed | True |
| g | forged-present-binding | killed | killed | True |

## Actual outputs and restoration

Full argv, rc, stdout/stderr and pristine/mutated/restored SHA-256 values are in results.json and a.json–g.json. Unified defect patches are a.patch–g.patch. A nonzero pristine or restored detector is inconclusive, never counted as a kill.

Pristine/restored detectors returned 0 for every mutant. Mutated behavioral detectors returned 1 for all seven; mutated selftests returned 0 for a/b/c and 1 for d/e/f/g. Named selftest failures: d `summary-canary-lie`; e `containment-sibling`; f `records-mismatch`, `shape-records-rejected`; g `nonce-verdict-agrees`.

Important capture distinction: a/b produced empty captured child environments, not leaked caller environments. With capture enabled, `run()` uses `dict(env or {})`; removing the environment therefore loses the four required keys. Without capture it passes None through to subprocess, which would inherit the caller; that latter branch was not exercised. b still returned checker rc=0; c likewise falsely returned checker rc=0 over its polluted implicit capsule.

Restored packed-elf SHA-256: `973d504b415c58c1cc84896057322ce99c2db2762551de3b13f0c87f17ffefe7`. Restored capsule_audit SHA-256: `d3b189152cb052bc5f178f9ffc16a0d186de2cd7d1a7340eef4ba4e1e1ab0c72`. Every corresponding before hash is identical.

## Current test boundary

See results.json for observed selftest survivors. The new allowlisted-exec fixtures directly execute the git reader and checker readelf with raw child-environment capture; they are not part of current --selftest. The implicit-capsule fixture omits the explicit capsule argument, names an absolute observed.log, and supplies a clean claimed key set over a polluted raw record. Other cases isolate a contradictory claimed canary, sibling-prefix HOME escape, count lie, and forged present binding.

## Scope and risks

Only the assigned selftests and new targeted behavioral fixtures were exercised. No full seam-probe/battery claim about all current integration tests is made. Existing A11 is a separate behavioral integration detector; whether it detects environment mutants is not inferred from selftest survival. Receipt fixtures reuse retained route evidence, replacing rev and producer digest with the frozen git blob solely to isolate checker clauses. Scratch is removed in finally before return.

## Self-evaluation

Accuracy 4: exact outputs retained, but no full integration detector run. Completeness 4: seven requested defects and three-stage detectors; boundary limited to assigned probes. Clarity 4: table plus full machine receipts; large raw environment output is relegated to JSON. Actionability 4: named missing binding cases and exact patches; not integrated into production tests. Conciseness 4: summarized here, full receipts separate. Overall 4.0. Highest-impact improvement: add executable git/readelf environment and implicit-capsule cases to current selftest. User agreement check: results distinguish local selftest coverage from full integration coverage.

Report: .ufo/waves/round-72/w1/MutReaders/MutReaders.md
