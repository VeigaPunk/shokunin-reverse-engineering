# RevGrammarOffline — settled

Verdict: CTL-OLD expectation confirmed, 2/4; CTL-NEW expectation confirmed, 4/4. No claims-expectation defect found.

- R50: c6430/c6490 PASS, g7581/g7582 FAIL (twelve undisposed required device rows each). Law: all PASS. `nonregular_unpublished_ok` true for all four.
- Harness `run.json` gap-detail arrays are truncated to 20; full `after.json` envelopes are required. Verified all four envelope SHA-256 values against harness receipts. Claims already prescribe complete envelopes correctly.
- Offline derivation process exited 0 and agreed with canonical `disposition_check` for all eight pairs; execution receipt includes exact argv, UTC and stdout SHA-256. No REA/full-counter/network run. LSP device unavailable. No tools installed.

Detailed table, JSON paths, source references, residual risks and self-evaluation: `RevGrammarOffline/verdict.md`. Raw computation: `RevGrammarOffline/derivation.json`; reproducible probe: `RevGrammarOffline/derive.py`; execution receipt: `RevGrammarOffline/execution.json`.

ExecGrammar/LB2OfflineClause reports were unavailable after independent derivation; comparison not run. This is a review recommendation, not freeze admission.
