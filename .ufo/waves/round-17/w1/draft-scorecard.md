# Draft — SCORECARD.md `## Round 17` (author-side, not integrated)

Status: DRAFT for L1 integration. Not an admission. Not for paste until every slot is filled by a retained measured run.
Slot rule: `{{…}}` marks a number or an outcome verdict that is unknown until measured. No number or verdict is pre-filled. Prose outside slots states only what the baseline already shows, with anchors in `DraftScorecard.md`.

---

## Round 17 — calibration correction and Go carrier diagnostics, 2026-10-20

Baseline: `b563c799d97774aae4351276fe43cb897311e349` (`.ufo/waves/round-17/claims.json` `baseline`).
Measured source revision, committed and pushed before checks: `{{REV}}`.
Full producer argv/cwd/stdout/stderr/exits/input hashes: `.ufo/waves/round-17/verification.json`; motivating evidence and admit/reject decisions: LOG round-17 and `corpus/lessons/round-17.md`.

| Claim / axis | Existing numeric proxy | Falsifiable supplemental before→after, command and measured revision | Author-side verdict / limits |
|---|---|---|---|
| C1 calibration | {{proxy_before}}→{{proxy_after}}, delta {{delta}}; three owned finite proxies tie at 10.0 at baseline | `pins.py` selftest red case exit {{pins_red_exit}} (mutated temp file named); `temporal-sweep.py --rev {{REV}}` sites {{sites_before}}→{{sites_after}}, unqualified {{unq_before}}→{{unq_after}}; `invocation-audit.py --rev {{REV}}` unlabelled-variant rows {{M_before}}→{{M_after}}; QUALITY row 19 presence 0→{{q19}}; `python3 -I .ufo/waves/round-17/measure.py {{REV}}` on baseline and measured revision | {{verdict_C1}}. Limit: `pins.py` proves same bytes at two instants, never unchanged throughout. Sweep scope excludes `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` unless passed via `--extra` (see correction below). |
| C2 depth | {{depth_proxy_before}}→{{depth_proxy_after}}; capability rows {{cap_before}}→{{cap_after}} | Retained carrier runs with pinned carrier, REA evidence id, retained log sha256 and prediction comparison: runs with all three {{runs_before}}→{{runs_after}} (target ≥3); prediction mismatches reported: {{mismatches}}; `compare.py` exits {{compare_exit}} | {{verdict_C2}}. Limit: polling copy of `ghidra.log`/`script.log`; lines after the final poll may be missing. No Go 1.27 recovery is promised. |
| coverage | {{cov_before}}→{{cov_after}} | {{cov_command_result}} | {{verdict_coverage}} |
| operability | {{op_before}}→{{op_after}} | `controls.py` and selftests exit {{op_exits}} | {{verdict_operability}} |
| freshness | {{fresh_before}}→{{fresh_after}} | installed-data and carrier pins recorded pre/post | {{verdict_freshness}} |
| adjacency | no owned numeric proxy | local source-model/data and documentation evidence only | {{verdict_adjacency}} |

The supplemental counts are not expertise scores or unbiased calibration measures. The lowest-axis tie is worked through calibration; no proxy is retired or relabeled.

### Named correction — R16-PROVENANCE (append-only; no r16 bytes rewritten)

The r16 section (`SCORECARD.md:2294-2348`) contains no temporal-stability sentence at the baseline. The attribution to the scorecard in `corpus/lessons/round-16-verifier-spotcheck.md:183` is therefore not matched here, and this section records that negative instead of correcting a sentence that is absent.

Map matches committed source-revision blobs; temporal stability is not evidenced for any statement below. Each site is listed on its own line with its path:

R16-PROVENANCE: `corpus/lessons/round-16.md:154` — producer/fixture pin stability sentence in the round-16 metadata bullet. Map matches committed source-revision blobs; temporal stability not evidenced.
R16-PROVENANCE: `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` — producer/fixture pin stability sentence. Map matches committed source-revision blobs; temporal stability not evidenced. (Outside the current temporal-sweep site list.)
R16-PROVENANCE: `LOG.md:2012` — producer/fixture hash stability sentence in the round-16 measured-records entry. Map matches committed source-revision blobs; temporal stability not evidenced.
R16-PROVENANCE: `.ufo/waves/round-16/verification.json:419` — boolean field `true` backed only by the 20-entry map at `:397`; `executed_at_utc` at `:4` is the only timestamp. Map matches committed source-revision blobs; temporal stability not evidenced. The boolean is not a measurement.

R16-INVOCATION: `SKILL.md:448` citation-drift registry row — {{invocation_correction_status}}; receipt `{{receipt_path}}`.

### Capability row — conditional draft, NOT entered unless the demonstration runs

Target: main `## Capabilities` table, `SCORECARD.md:617-622` (4 rows at baseline). Round-13 and round-14 capability rows sit in round-section sub-tables (`SCORECARD.md:2135`, `:2207`) and are not in the main table.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| retained REA Ghidra-session log capture for caller-selected Go carriers | For a carrier pinned by path+SHA-256, runs REA {{rea_version}} analyze with per-poll copies of the new session's `ghidra.log`/`script.log`, extracts Go analyzer diagnostics and compares them with source-derived predictions; polling copy, final-poll lines may be missing | `.ufo/waves/round-17/runs/{{label}}/receipt.json` sha256 `{{receipt_sha256}}`; `receipt-validate.py` exit {{validate_exit}}; `python3 -I .ufo/waves/round-17/tools/carrier-run.py --carrier {{CARRIER}} --label {{label}} --out-dir {{DIR}}` | 17 |

Entry condition: `receipt-validate.py` exit 0 on a retained run receipt. Otherwise no row is added and the stagnation counter does not reset.

Prediction vs observation (per carrier; fields are not pre-filled):

| Carrier (path, SHA-256) | Go version (`inspect-go-binary`) | Predicted untested / snapshot / bootstrap | Observed untested / snapshot / bootstrap | Match |
|---|---|---|---|---|
| {{CARRIER_1}} | {{GO_1}} | {{PRED_1}} | {{OBS_1}} | {{MATCH_1}} |
| {{CARRIER_2}} | {{GO_2}} | {{PRED_2}} | {{OBS_2}} | {{MATCH_2}} |

Stagnation: {{stagnation_before}}/10 → {{stagnation_after}}/10. Note: the last explicit counter in the baseline is `3/10` at `SCORECARD.md:1500`; `:2315` says the window "remains 10" without a count. `{{stagnation_before}}` must be decided by L1 from the full history.

### Executed controls and frontier

- Controls: `controls.py {{BASELINE}} {{REV}}` exit {{controls_exit}}; prior lesson and knowledge prefixes retained {{prefix_counts}}; pre-existing `.ufo/waves/**` and `evidence/**` blobs byte-identical {{blob_counts}}; QUALITY rows 1–18 unchanged {{quality_unchanged}}.
- Metadata: `{{metadata_command}}` exit {{metadata_exit}}.
- Sources: {{sources_before}}→{{sources_after}}; tiers {{tiers}}; mined {{mined}}; rejected {{rejected}}.
- Swarm: W1 {{w1_seats}} seats, completed {{w1_done}} / failed {{w1_failed}}. Credit or capacity failures are retained, not replaced or called passes. L1 holds the canonical planner seat; author seats are not outside reviewers.

Learning trends: expansion {{v_expansion}}; quality {{v_quality}}; discernment {{v_discernment}}.

Planned: {{planned_next}}. SHONEN stays `[~]`. No promotion, no `[x]`, no outside verification by author seats, no following round started here.
