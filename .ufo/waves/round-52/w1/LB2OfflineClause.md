# LB2OfflineClause — round 52 wave 1

**Verdict: hypothesis supported; no stop-the-round mismatch.** An independent scratch implementation of the three-family committed-data disposition semantics gives the expected 2/4 under the round-50 rule and 4/4 under the r52 device-accounting law.

| Carrier | R50 disposition | R52 law disposition | Detail |
|---|---:|---:|---|
| c6430 | pass | pass | 824 nonregular rows; 567 path gaps; 1 structural depth gap; 1 removal |
| c6490 | pass | pass | 914 nonregular rows; 612 path gaps; 1 structural depth gap; 1 removal |
| g7581 | fail | pass | R50 has exactly 12 undisposed required device rows; R52 has 1001 rows, 636 path gaps, 1 structural depth gap, 3 removals |
| g7582 | fail | pass | R50 has exactly 12 undisposed required device rows; R52 has 1001 rows, 636 path gaps, 1 structural depth gap, 3 removals |

The two R50 failures are specifically `dev/pts/0-7`, `dev/tiatm`, and `dev/ttyp0-2`, matching the claims' twelve-row expectation. The R52 model is built in-memory from the committed R50 rule with the claimed law change: `allowed.char-device=[]`, `required.char-device=false`, and no silent char-device details. It does not import or execute the production counter or another seat's output. It reads the four committed `after.json` envelopes and corresponding nonregular TSV oracle tables; no REA/data-run, network, or vendor bytes used.

**Evidence:** `LB2OfflineClause/probe.py` is the standalone implementation; `LB2OfflineClause/stdout.json` is captured command stdout; `LB2OfflineClause/receipt.json` records exact command, exit code, stdout SHA-256 and UTC. Final command exited 0, stdout SHA-256 `a4dbc0a67b41886f008f0087a3e63c897b8f17e8ef70f8f3fde970685fbe670d`, UTC `2026-10-30T10:49:42Z`.

**Scope/risks:** This tests only rule-scoped disposition expectations, not byte-dependent counter clauses, carrier pins, frozen bindings, projection, controls, or the post-freeze data run. One earlier probe iteration exposed and corrected an implementation error resolving removals from diagnostic `input_path` rather than `report.link`; the final implementation follows the counter's documented path mapping and reports the expected rows. No tools installed. No blockers.