# 2026-10-15 — round 1 admission diagnostic must inspect its evidence

source: `LOG.md`, Admission-diagnostic correction; `.ufo/rounds/interactive-r1/verify-recovery.py`; prior work `23c0fd5f2e5838da737341ac468edabca1784da7`
verified-at: 2026-10-15; local evidence consistency only
recheck: `python3 .ufo/rounds/interactive-r1/verify-recovery.py --selftest`; same command without flag and with `--admission`

## Correction

The original `--admission` branch unconditionally emitted the two known
blockers. Its exit 2 was a recorded diagnostic, not verification of the
routing/receipt observation contents. This corrects that interpretation in
SCORECARD, LOG, the recovery lesson and filed report; their original bytes and
full historical outputs remain preserved.

The gate now checks the routing observation against the canonical wave's
resolved role aliases and persisted required aliases, checks zero spawned and
settled counts against the result/no-dispatch record, and checks the missing
receipt fields against the selected argv-launch metadata shape. Contradictory
observations fail before the blocker diagnostic can be emitted.

## Gate

- **Candidate / admitted:** derive the local prerequisite diagnostic from the
  pinned observations. No new native capability or verified round is admitted.
- **Rejected:** equating an unconditional exit with evidence verification;
  equating locally consistent recorded blockers with live route health,
  canonical judgment or applicable receipt acceptance.
- **Check:** the real recovery package returned evidence exit 0 and admission
  exit 2. Twelve isolated subprocess cases returned the persisted expected
  exit/finding pairs, including routing-ready/blocked contradiction,
  settled-without-dispatch and contradictory receipt absence. Those three
  fixtures re-pin only isolated input snapshots so the semantic checks, not
  the digest guard, must detect the contradiction. Full output:
  `.ufo/rounds/interactive-r1/gate-correction-results.json`.
- **Spot-check:** author correction only; no outside admit/reject review.

No new round, score, specialist dispatch, host reconfiguration, receipt or
Sighting completion. Verified-round increment remains zero. The original
routing and receipt unblock actions remain applicable to the recorded state.
