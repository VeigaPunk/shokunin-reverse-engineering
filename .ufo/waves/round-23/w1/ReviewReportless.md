# ReviewReportless — R22 QUALITY22 cutoff and causes

## Findings

### Historical causal overstatement — corrected; no active contradiction in the final R22 record

- **Observed — current rule:** `corpus/QUALITY.md:32` (criterion #22) requires a wave-status claim to name its observation cutoff, distinguish terminal failures from seats not yet returned, and retain per-seat causes with error/transcript/result evidence or `cause unknown` plus what was tried. Later reclassification must be appended with its own cutoff; a headline count alone is inadmissible.
- **Observed — superseded assertion:** `.ufo/waves/round-22/wave1-terminal.json:3-4` and `.ufo/waves/round-22/recovery-authority.json:3-8` originally attribute all 93 W1 children to automatic termination with the coordinator after its Anthropic429. That is not the operative account: `.ufo/waves/round-22/wave1-terminal-correction.json:2-16` explicitly supersedes the causal assertion, states children do not necessarily die with a parent, and records the per-child cause as unknown. The correction retains the checks performed (empty inherited-agent reads, W1 directory containing only the registry, and a parent process check) and requires any late report to be counted and reclassified, not discarded.
- **Observed — corrected cutoff:** `.ufo/waves/round-22/final-wave-outcomes.json:1-18` sets the final observation cutoff to **2026-10-21T13:58:56.949274+00:00**. At that cutoff W1 had 93 seats, zero reports, and 93 not-live observations; the aggregate cause says per-child unknown, with the parent Anthropic429 observed but automatic parent-child cancellation unestablished. The retained `.wave1.members[]` records mark the individual W1 causes `unknown; parent provider error is not per-child terminal proof` and list the attempted checks; a grouped read of all 93 member causes returned that same unknown cause for all 93. The recorded final W1 sweep contains only `swarm-registry.json` (`:8-18`). Thus the evidence establishes W1’s reportless/not-live status at that cutoff, **not** that parent death automatically cancelled the children or why each child lacked a report.
- **Observed — known causes are separate:** W2 had 64 seats, 55 reports, and nine terminal provider failures (`final-wave-outcomes.json:1139-1153`, per-seat details in `.wave2.members[]`; R22 report `.ufo/reports/round-22/kaidoku.md:26-29`). The retained failures group as 3 Codex capacity / `turn_rate_limit_exceeded`, 1 Haiku 429, 3 Cursor `RESOURCE_EXHAUSTED`, and 2 Devin `resource_exhausted`/free-model-limit outcomes. One W2 scribe’s retained record notes a second same-identity Haiku429 after a steering race; it was not an additional seat or replacement. These known W2 provider failures do not establish W1 child causes.
- **Observed — R23 inheritance is calibrated:** `round-23/claims.json:63` carries forward “102 reportless seats remain per-seat unknown where unknown; not replaced or explained by conjecture.” The count is 93 W1 unknowns plus nine W2 known terminal failures, not 102 uniformly unknown causes. The retained total is 157 seats with zero replacements (`final-wave-outcomes.json:1778-1786`).
- **Conclusion:** Reject the automatic R22 parent-death cancellation explanation as an established cause. The coordinator’s Anthropic429 is observed; W1 per-child causes remain unknown. The original statement remains useful only as preserved, superseded history. The corrected final record applies the relevant QUALITY22 cutoff/cause distinctions; no additional or redundant quality criterion is indicated by this boundary review.

## Residual risk

- The superseded universal-cancellation wording remains in `wave1-terminal.json` and `recovery-authority.json`; readers must follow `wave1-terminal-correction.json` and the final outcomes rather than reusing the earlier attribution.
- This result is bounded by the recorded cutoff. No fresh post-cutoff process or report check was performed here. A later W1 report would require the correction’s appended reclassification treatment.
- W1’s per-child causes remain unresolved; no inference about provider behavior or child lifecycle is made from the coordinator failure or absence of reports.

## Verification gaps

- This is an author-side, read-only review of retained documents and JSON records, not independent admission or live process verification.
- No shell/REA probe, build, test, or other execution was run; therefore no command exit is claimed. The source evidence was read directly, including grouped JSON queries for W1 causes and W2 terminal-failure causes.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewReportless.md` — final SHA-256 is reported in the delivery message (a file cannot embed its own unchanged digest).

## Installs

- None.
