# RevFetchGuards — reviewer

**Final executor disclosure:** `ExecFetchVendor.md:3–8` now explicitly reports blocked/partial: required guard-deleted fixtures were not completed, existing selftest does not prove guard deletions red, and no tests were run. Therefore routed defect 4 is **unfulfilled**, not merely awaiting receipt inspection. Do not freeze this draft as a completed guard repair.

Recommendation: do not approve the in-flight fetcher without its final offline guard/deletion receipts.

1. Initial draft #592E broke every frozen carrier by comparing padded member length instead of carving; nested-reader APIs and chain tests also regressed. Executor acknowledged and replacement #03AC restores original chain code/tests. This is caught-and-reworked evidence, not an unresolved allegation against final bytes.
2. Initial guard selftest would reach the real network when initial guards were deleted; redirect probes used req=None and would crash on guard removal. Executor notified; replacement witnesses were not yet delivered. Four independent scheme/host deletion sites require offline, non-crash evidence.
3. Guard list pins URL scheme/hostname, not strict origin port or proxy socket. Original permits same-host HTTPS redirects. File/data schemes, relative redirects, authority confusion, transport wiring, and target-file symlinks deserve explicit boundaries/tests rather than blanket safety claims.

Full numbered findings, network inventory, source locations, residual risks and verification gaps: `.ufo/waves/round-52/w1/RevFetchGuards/findings.md`.

Static review only; runtime/selftests/mutants/REA/downloads not run. LSP device unavailable; literal source fallback used. No installs or scratch files; only assigned report/status paths written. Final integration owner must inspect final draft and command/exit/stdout-sha256/UTC receipts; no final-byte approval asserted.
