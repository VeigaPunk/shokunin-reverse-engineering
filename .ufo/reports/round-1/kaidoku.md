# kaidoku — operator-steered round 1, interactive recovery

Status: **blocked, not a verified completed round**. Work commit: `23c0fd5f2e5838da737341ac468edabca1784da7`.
Inherited source commit: `c265db9bd3c0883fbaf4487f839559c85a736826`.
Baseline: `6645585873c4e66372b15687c47000abf8d91978`.
This local report is written after the work commit; it does not modify any
historical fleet report or ledger. No push.

## Work performed

- Reconciled the interrupted worker's commit with its absent result/report;
  preserved its frozen rubric, baseline, old native Evidence, historical r1–14,
  and all session files. Initial status had only untracked `.ufo/` material.
  Evidence: `LOG.md:486-500`; saved WWKD plan in `.ufo/rounds/interactive-r1/`.
- Continued the existing calibration move, not a new numbered round or a
  completed historical integration. Fresh immutable-source measurements and
  L1-author review arguments now back the missing result. Evidence:
  `evidence/round-1-2026-10-15/result.json`, `source-measurements.json`.
- Validated exactly 32 distinct advisory scopes with the canonical renderer,
  exit 0; refused unauthorized dispatch. Existing overrides/cards do not
  realize the required content, audit or connector aliases/fallback. Evidence:
  `wave-spec.json`, full `wave-validation.json`, `routing-observation.json`.
  **Spawned 0; settled 0.** No second L1, background orchestration, routing
  overlay, per-dispatch model pin or global config mutation.
- Ran actual bounded libjq static inspection through the current REA 6.5.0 /
  Ghidra 12.1.4 surface, exported complete Evidence and closed the owned session.
  Independent `sha256sum` and bounded `objdump` matched digest and ENDBR64 bytes,
  process exit 0. Evidence: fresh `rea-bundle.json`, recovery lesson.
- Reproduced the missing-result evidence failure before repair, then exercised
  the new local gate and isolated-fixture self-invocation. Admission remains
  could-not-evaluate. Full lines and exit codes appear below and in
  `gate-before.json` / `gate-results.json`.
- Inspected only selected launch/pane/Sighting metadata: run/session IDs and
  an argv launch exist, applicable task-receipt authority does not. No mint,
  validate or complete operation was attempted. Evidence:
  `receipt-binding-observation.json`. The real interactive pane remained live:
  `tmux display-message -p -t %14 '#{pane_id} #{pane_current_command} dead=#{pane_dead}'`
  returned `%14 node dead=0`, exit 0. No pane was replaced or made a log watcher.

## Landed changes

All work below is in `23c0fd5f2e5838da737341ac468edabca1784da7`, authored as
`kaidoku-shokunin <kaidoku@shokunin.local>`; motivated and recorded by
`LOG.md:486-567`.

- Restored `evidence/round-1-2026-10-15/result.json` with measured source
  revision, individual C1–C9 source arguments, author-only attribution,
  `admitted:false` and `verified_round_increment:0`.
- Added `.ufo/rounds/interactive-r1/`: plan, 32-scope wave, complete validation,
  fresh source measurement/native bundle, shape-only route/receipt blockers,
  digest-pinned expectations, runnable gate and full before/after verdicts.
- Appended the current SCORECARD admission correction and LOG evidence;
  registered the sealed recovery gate in SKILL. Added a new correction lesson
  and its corpus index row rather than rewriting historical corpus claims.
- Left inherited rubric/baseline/bundle, SHONEN, PROVINCE, native session
  material, sibling repos, source trees, global config and shared fleet files
  unchanged. No package/host remediation or external live-target research.

## Before → after measurements

Commands: SCORECARD recipes A (Git objects at the two revisions) and B
(`/usr/bin/jq --slurpfile r evidence/round-1-2026-10-15/result.json ...`).
Full remeasurement: `.ufo/rounds/interactive-r1/source-measurements.json`.
The result supplies source review arguments; automatic counts are not semantic
proof. The result itself is a later bookkeeping artifact, not falsely claimed
present in its measured source commit.

| Axis / observable | Baseline `6645585...` | Inherited work `c265db9...`, freshly checked | Author verdict |
|---|---:|---:|---|
| calibration, selected reviewed alignment | 0/9 | 9/9 | improved within the frozen failure-selected rubric |
| coverage, mapped knowledge files | 70/72 | 70/72 | unchanged; r14 pair still unmapped |
| depth, resolvable cited rule blocks | 9/9 | 9/9 | unchanged; structural only |

Recovery durability improved from missing result to a locally consistent pinned
package, but this is not another scored axis move. Learning trends: expansion
**unchanged**, quality **improved** for this assessment chain only, discernment
**unchanged**. No native Pareto verdict, promotion or domain saturation is claimed.

## SHONEN

- [~] Decision tables / error patterns / checklists: `SHONEN.md:5-6`, `SKILL.md:38-75,77-210`; author assertion only, no outside verifier.
- [~] End-to-end domain task: owned libjq open → instruction decode → export → close; `.ufo/rounds/interactive-r1/rea-bundle.json`; no outside verifier.
- [~] Executable instructions: source recipes and recovery gate exercised; `gate-results.json`; no outside verifier or broad recipe revalidation.
- [~] Province boundary: `PROVINCE.md:88-109`; current version alignment remains contested as named in SCORECARD; no outside verifier.

A same-lane subagent would not be an outside verifier. In this recovery no
specialists were dispatched at all.

## Full local verdicts and process exits

Before result repair:

```text
RECOVERY_EVIDENCE: COULD_NOT_EVALUATE finding=missing_result exit=2
PROCESS_EXIT: 2
```

### after

Command: `python3 .ufo/rounds/interactive-r1/verify-recovery.py`

```text
RECOVERY_EVIDENCE: CLEAN finding=pinned_package_consistent author_review=9/9 coverage=70/72 citation_rules=9/9 admitted=false verified_round_increment=0
PROCESS_EXIT: 0
```

### selftest

Command: `python3 .ufo/rounds/interactive-r1/verify-recovery.py --selftest`

```text
SELFTEST_CASE: CLEAN case=clean exit=0 expected=0 finding=pinned_package_consistent
SELFTEST_CASE: CLEAN case=missing_result exit=2 expected=2 finding=missing_result
SELFTEST_CASE: CLEAN case=snapshot_tampered exit=2 expected=2 finding=snapshot_tampered
SELFTEST_CASE: CLEAN case=wrong_revision exit=1 expected=1 finding=revision_mismatch
SELFTEST_CASE: CLEAN case=omitted_obligation exit=1 expected=1 finding=obligation_set_mismatch
SELFTEST_CASE: CLEAN case=duplicate_obligation exit=1 expected=1 finding=obligation_set_mismatch
SELFTEST_CASE: CLEAN case=wrong_subject exit=1 expected=1 finding=subject_mismatch
SELFTEST_CASE: CLEAN case=unearned_admission exit=1 expected=1 finding=unearned_admission
SELFTEST_CASE: CLEAN case=blocked_admission exit=2 expected=2 finding=required_alias_bindings_missing+applicable_receipt_binding_missing
RECOVERY_SELFTEST: CLEAN cases=9 exit=0
PROCESS_EXIT: 0
```

### admission

Command: `python3 .ufo/rounds/interactive-r1/verify-recovery.py --admission`

```text
ROUND_ADMISSION: COULD_NOT_EVALUATE finding=required_alias_bindings_missing+applicable_receipt_binding_missing exit=2
PROCESS_EXIT: 2
```


Canonical wave validation: `WAVE_VALIDATION: CLEAN exit=0`, counts
`spawn=32 resume=0 total=32`. This validates spec shape, not route health or
native dispatch. Complete canonical JSON stdout/stderr/argv is committed in
`wave-validation.json`; no native `task` payload was submitted.

Native smoke: subject `/usr/lib/libjq.so.1.0.4`, SHA-256
`7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b`;
`0x117070` → `f30f1efa`, ENDBR64, length 4, observed/shipped-artifact.
Evidence `ev_f5e5da50ea8ff88ca9b26a97cebe1ac440c41414e0effd9bfe1943f464780481`.
MCP export returned records=1, bytes=18991; close returned `result:null`.
MCP success is reported as tool outcome, not an invented process exit code.
This was static decoding, not target execution or a safety/trust verdict.

## Debt, cross-domain boundaries and exact unblock

1. **Routing authority:** required executor/scribe `@m_composer`; observed
   `@m_mid`/`@m_fast`. Required reviewer/critic `@m_grok`; observed
   `@m_mid`/`@m_strong`. Required connector `@m_antigravity` with `@m_zfl`
   fallback; observed `@m_mid`, named antigravity fallback list empty. Existing
   agent cards carry no alternate model binding. Operator must provide these
   authorized existing bindings; this lane must not change global config.
2. **Applicable receipt:** launch and selected Sighting record contain no
   taskKey, dispatcher prompt/config digests or result/receipt path binding.
   Operator/integrator must supply applicable dispatch authority. Do not mint
   a schema-shaped receipt with invented taskKey or locally substituted hashes.
3. **Incomplete wave:** shape validation is not dispatch or settled output.
   After routing is authorized, recover this round in one fresh interactive L1
   session and use one complete native 32-member batch from the renderer.
   Do not rerun recorded Phase-0 contract-sync or self-iter failures merely to
   confirm them; this recovery did not run them or claim native judgment.
4. **Historical/fleet closure:** LOG records ten old goal-era rounds, but this
   pass did not revalidate all historical rounds or resolve their fleet-only
   report/ledger gaps. Shared ledger closure remains integrator-owned. The
   verified historical total under the current dispatch contract is not
   established here, not fabricated as zero or ten.
5. **Retained domain debt:** version-pinned surface/name reconciliation;
   family-specific Evidence-ID law versus universal old summaries; two unmapped
   r14 files; stale frontier/fix-count summaries; old safety-label scope bleed;
   device/provider/scale limits. Sources/unblock directions remain in SCORECARD,
   Open gaps. No unrelated fixes were absorbed.
6. **Outside discernment/promotion:** no non-author admit/reject spot-check.
   An eligible outside verifier must review at least one admit and reject;
   author assertions and same-lane reviews cannot close promotion boxes.

## Continuation and integrator handoff

**Verified-round increment: 0. Current round: 1, blocked recovery.** Target:
at least 100 verified rounds; not replaced by the launch counter or historical
quota. No arbitrary session-budget stop or saturation claim.

Fresh-session-per-round continuation is preserved: this process does not run
round 2. `.ufo/continuation/kaidoku-interactive-r1.json` and `.md` identify this
work commit and unblock actions. Preserve mission
`m_645cfa32b5284aaab568431141665df8` / pane `%14` until authorized cutover;
Sighting is not marked complete. Only the fleet integrator updates shared
ledgers. Commit/report durability is complete locally; round admission is not.

## Erratum — evidence-derived admission diagnostic, same round 1

Correction work commit: `a3f2e1be58ceaaba1c57ba996698bd86b36123e6`.
This appendix was written after that commit; the original report above
retains its filed bytes.

The original admission exit 2 recorded the known blockers unconditionally.
It was not verification of the routing/receipt observation contents. This
supersedes that interpretation of the earlier Full local verdicts section,
not its historical output. The corrected gate cross-checks recorded aliases
against the canonical wave preflight and persisted required routes, requires
zero dispatch/settlement across observations and result, and validates the
receipt-absence fields against the argv-launch metadata shape.

Three new isolated fixtures reject contradictory routing status, settlement
without dispatch and contradictory receipt absence. They re-pin only the
isolated fixture inputs so that semantic checks, rather than the digest guard,
must reject them. Full output and process exit codes:
`.ufo/rounds/interactive-r1/gate-correction-results.json`.

Commands: `python3 .ufo/rounds/interactive-r1/verify-recovery.py`, followed by
the same entry with `--selftest` and `--admission`.

```text
RECOVERY_EVIDENCE: CLEAN finding=pinned_package_consistent author_review=9/9 coverage=70/72 citation_rules=9/9 admitted=false verified_round_increment=0
PROCESS_EXIT: 0
SELFTEST_CASE: CLEAN case=clean exit=0 expected=0 finding=pinned_package_consistent
SELFTEST_CASE: CLEAN case=missing_result exit=2 expected=2 finding=missing_result
SELFTEST_CASE: CLEAN case=snapshot_tampered exit=2 expected=2 finding=snapshot_tampered
SELFTEST_CASE: CLEAN case=wrong_revision exit=1 expected=1 finding=revision_mismatch
SELFTEST_CASE: CLEAN case=omitted_obligation exit=1 expected=1 finding=obligation_set_mismatch
SELFTEST_CASE: CLEAN case=duplicate_obligation exit=1 expected=1 finding=obligation_set_mismatch
SELFTEST_CASE: CLEAN case=wrong_subject exit=1 expected=1 finding=subject_mismatch
SELFTEST_CASE: CLEAN case=unearned_admission exit=1 expected=1 finding=unearned_admission
SELFTEST_CASE: CLEAN case=routing_status_contradiction exit=1 expected=1 finding=routing_observation_mismatch
SELFTEST_CASE: CLEAN case=settled_without_dispatch exit=1 expected=1 finding=undispatched_wave_observation_mismatch
SELFTEST_CASE: CLEAN case=receipt_presence_contradiction exit=1 expected=1 finding=receipt_observation_mismatch
SELFTEST_CASE: CLEAN case=blocked_admission exit=2 expected=2 finding=required_alias_bindings_missing+applicable_receipt_binding_missing
RECOVERY_SELFTEST: CLEAN cases=12 exit=0
PROCESS_EXIT: 0
ROUND_ADMISSION: COULD_NOT_EVALUATE finding=required_alias_bindings_missing+applicable_receipt_binding_missing exit=2
PROCESS_EXIT: 2
```

This is consistency verification of the pinned recorded state, not a fresh
route-health probe, native judgment or receipt acceptance. Axes, learning
trends, four author-only SHONEN assertions and unblock actions remain unchanged.
No new round, wave dispatch, receipt or Sighting completion occurred.
Verified-round increment remains **0**. Updated machine handoff:
`.ufo/continuation/kaidoku-interactive-r1-admission-correction.json`.
