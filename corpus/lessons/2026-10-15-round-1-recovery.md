# 2026-10-15 — round 1 recovery: a landed assessment is not a verified round

source: `LOG.md`, Interactive round-1 recovery; `c265db9bd3c0883fbaf4487f839559c85a736826`; `.ufo/rounds/interactive-r1/`
verified-at: 2026-10-15; recovery evidence only, round admission blocked
recheck: `python3 .ufo/rounds/interactive-r1/verify-recovery.py`; `--selftest`; `--admission`; source-count recipes A/B in SCORECARD

## Trigger and correction

The interrupted worker landed the calibration assessment at `c265db9`, but
its scorecard, lesson and log cited an absent `result.json`. The interactive
successor found the inherited rubric, baseline and native bundle, no local
round report, and only untracked native-session material. Preserve those
artifacts and the historical r1–14 labels; do not infer a completed round from
the old launch counter or commit subject. This is recovery of the existing
2026-10-15 round 1, not another round and not the next version-expansion move.

This entry supersedes the closure promises in
`corpus/lessons/2026-10-15-round-1.md:140-143,154-160` and `LOG.md:480-484`:
the local result is now restored, but no fleet report reassessment was written
and no specialist/outside-review attribution was reconstructed from transcripts.
Only this repository is writable. The new result's C1–C9 reviews are explicitly
**L1-author** reviews, not proof that the interrupted worker finished those reviews.

## Fresh observations

- Immutable Git-object measurement for baseline `6645585873c4e66372b15687c47000abf8d91978`
  and work commit `c265db9bd3c0883fbaf4487f839559c85a736826` reproduced **70/72**
  map coverage and **9/9** resolvable rule blocks at both revisions. Counting
  recipe A is in SCORECARD; fresh outputs are
  `.ufo/rounds/interactive-r1/source-measurements.json`. These remain structural
  proxies, not coverage of the whole domain or semantic correctness.
- Counting recipe B, executed with `/usr/bin/jq --slurpfile r
  evidence/round-1-2026-10-15/result.json ...
  evidence/round-1-2026-10-15/rubric.json`, returned baseline **0/9, score 0**
  and after **9/9, score 10**, measured against those two source commits.
  The result records each source-review argument; counting flags does not
  prove their truth. Failure-selected completeness is not unbiased accuracy.
- The current live REA status reported a closed target, package **6.5.0**,
  **207** MCP tools, **153** CLI commands, skill **42**, catalog digest
  `805433f17bb4f709558ff20c04f96fe561fca2938fd0f459b1f8cc0f6b438ded`.
  These are catalog/status facts, not 207 held verbs. No host config,
  package or provider remediation was performed.
- Actual smoke: pin `/usr/lib/libjq.so.1.0.4` at SHA-256
  `7e8bccc6df37a55fb90703c9069b3770f5cdc502e96959c866d2f30fbf5e8b6b`;
  `open_binary` with Ghidra; `inspect_native_instruction {"address":"0x117070"}`
  decoded `f30f1efa` / `ENDBR64`, length 4, observed/shipped-artifact, provider
  **12.1.4**. Exported the complete fresh bundle to
  `.ufo/rounds/interactive-r1/rea-bundle.json`, then closed only that owned
  session (`result:null`). Evidence
  `ev_f5e5da50ea8ff88ca9b26a97cebe1ac440c41414e0effd9bfe1943f464780481`.
  `sha256sum /usr/lib/libjq.so.1.0.4 && objdump -d --start-address=0x17070
  --stop-address=0x17074 /usr/lib/libjq.so.1.0.4` independently matched digest
  and bytes, exit 0. This is static decoding, not target execution or safety.

## Gate

- **Candidates considered:** restore the missing assessment result and local
  handoff; start the next round immediately; dispatch through whichever aliases
  happen to work; count historical quota or a clean evidence gate as 100-round
  progress; manufacture a receipt from local prompt hashes.
- **Admitted to this recovery lesson:** only source-backed chronology,
  reproducible measurements, a bounded static smoke, and truthful blockers.
  No new `knowledge/` surface is admitted; no complete round is admitted.
- **Rejected:** unauthorized alias substitution, invented worker/outside review,
  numeric mastery, silent renumbering, availability-to-holding inference,
  receipt fabrication and Sighting completion without applicable authority.
- **Local checks:** before the repair, the recovery gate returned
  `COULD_NOT_EVALUATE finding=missing_result`, exit **2**. After the repair,
  `RECOVERY_EVIDENCE: CLEAN ... admitted=false verified_round_increment=0`,
  exit **0**; isolated self-invocation tested **9** exit/finding pairs and
  returned `RECOVERY_SELFTEST: CLEAN cases=9 exit=0`. Full output, commands
  and process exit codes are in `.ufo/rounds/interactive-r1/gate-before.json`
  and `gate-results.json`. The gate pins every input snapshot digest; it
  checks package integrity and cross-references, not review semantics.
- **Admission check:** `--admission` returned
  `ROUND_ADMISSION: COULD_NOT_EVALUATE finding=required_alias_bindings_missing+applicable_receipt_binding_missing exit=2`.
  This negative prerequisite verdict is not canonical native judgment.
- **Spot-check:** no outside admit/reject review occurred. Planned specialists
  were not dispatched; author review is not discernment or promotion evidence.

## Exact blockers and unblock actions

The canonical `ufo-swarm-wave.mjs plan --spec <saved-wave-spec> --route-families`
accepted **32** distinct scopes, width **32**, exit **0**. The full validation
output is saved locally. It did not dispatch or establish route health.

| Binding | Required | Observed in global taxonomy overrides |
|---|---|---|
| executor / scribe | `@m_composer` | `@m_mid` / `@m_fast` |
| reviewer / critic | `@m_grok` | `@m_mid` / `@m_strong` |
| connector | `@m_antigravity`, fallback `@m_zfl` | `@m_mid`; named antigravity chain is empty |

A model-binding sweep of existing global agent cards found no alternate
binding. No wave was dispatched, no new L1 was spawned, and no pins, routing
overlays or global config changes were used. Operator/integrator action:
provide the required existing role bindings and connector fallback before
redispatching the saved scopes through one complete native task batch.

The selected launch and Sighting metadata identifies run/session
`shk-kaidoku-interactive-20261015T050057Z`, mission
`m_645cfa32b5284aaab568431141665df8`, pane `%14`, with an `argv` dispatch.
It supplies no taskKey, dispatcher prompt/config digests or receipt/result
binding. `.ufo/rounds/interactive-r1/receipt-binding-observation.json` records
only metadata shape. Operator/integrator action: issue an applicable
receipt-bound dispatch; local arbitrary hashes cannot substitute for it.
No receipt mint/validation or Sighting completion is claimed.

## Verdict and continuation

For the inherited source move: calibration **improved** within its nine-item
selected rubric; coverage/depth **unchanged**. Recovery itself repairs evidence
durability, not another scored round. Trends: expansion **unchanged**,
quality **improved** only for this assessment evidence chain, discernment
**unchanged**. Retain all named provider, identity-law, map, scope and fleet
history debt. No saturation, promotion or harmed-axis trade is asserted.

**Verified-round increment: 0.** Recover round 1 in a fresh authorized session
when the bindings are supplied; do not advance to round 2 or run an in-session
loop. Historical quotas and the goal of at least 100 verified rounds remain
separate from actual applicable completion evidence.
