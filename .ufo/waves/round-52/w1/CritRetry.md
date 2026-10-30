# CritRetry — round 52 wave 1 report

Verdict: the projection retry policy in `plans/round-52-claims.md:105-114` is not admissible as written.

Findings (full text, severity, and demanded controls: `.ufo/waves/round-52/w1/CritRetry/findings.md`):
1. CRITICAL — the retried ENOENT is a REA-side `readlink` (`FirmwareFiles.js:184`) racing unblob's `unlink`/`symlink_to` (`extractor.py:89-91`) on absolute-target symlinks. Not the host-load `provider_timeout` class; not proven transient. The r51 disposition is quoted with an invented qualifier ("without proof able to fail"); r51 says unconditionally "no new retry policy is admitted" (`plans/round-51-claims.md:351-352`).
2. CRITICAL — the deterministic-ENOENT control proves only that the policy can exhaust, not that the real failure recovers. The inherited exhausted-ENOENT branch yields exit 2, not red (probe2: 3 invocations, RerunEnvError).
3. HIGH — the frozen projection drops `link_target` (`c1-counter.py:1839-1843`), so a retry can turn a visible red into a green over a differently-rewritten symlink.
4. HIGH — the success path drops `attempts` and the failing diagnostic; the failure capture truncates at 300 chars and drops `retryable:false`.
5. HIGH — the budget (2 for ENOENT) has no evidence; the only lane evidence for timeout is two exhausted dev-arm probes on non-carrier ids.
6. MEDIUM — exit-code semantics for exhaustion are unstated; the harness retry policy diverges from the counter's.

Method and limits: no REA run and no installs. Probes used a local stub `.mjs` package and the inherited counter code (`probe*.py`). The REA package was read, not executed. Receipts with exact commands, exit codes, stdout sha256 and UTC: `.ufo/waves/round-52/w1/CritRetry/receipts.json`. Status: `.ufo/waves/round-52/w1/CritRetry/status.json`. Scratch `/fast/scratch/hyaku/kaidoku-r52/w1-CritRetry` removed after copy.
