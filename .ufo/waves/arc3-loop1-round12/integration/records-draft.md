# arc3-loop1-round12 — records draft for parent fold

Status: draft only, not a landing receipt. `<WORK>` = the round's work commit;
`<M:...>` = a value the integrating parent must measure at `<WORK>`. Nothing
below upgrades a seat's scratch projection into landed evidence.

Citation abbreviations: `R12` = `.ufo/waves/arc3-loop1-round12` (relative to
the lane worktree); `STATE` = `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/kaidoku-state.md`;
`AXES` = `/home/vgpnk/Projects/shokunin/AXES.md`; `SCONTRACT` =
`/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`;
`R12PROMPT` = `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/prompts/kaidoku-round-12.md`.
All other paths are lane-root relative.

# Block 1 — SCORECARD section

## arc3-loop1-round12 — coverage + depth + operability: <verdict>, 2026-10-19

Wave: 48 seats frozen pre-dispatch on `openai-codex/gpt-6-luna-max` — the
scheduled `antigravity/gemini-3.8-flash` slot, substituted at dispatch because
the antigravity lane is down (operator directive; `R12/claims-frozen.md:3-8`);
the roster is enumerated 12 + 12 + 12 + 12 = 48 (`R12/claims-frozen.md:8-9,65-70`).
47/48 seat reports were delivered — `c1` 12, `c2` 12, `c3` 12, `verdicts` 11:
`CN-1` is the named non-completion, present in the frozen roster
(`R12/claims-frozen.md:70`) and absent on disk (`ls R12/claims/*/*.md | wc -l`
→ 47; `ls R12/claims/verdicts/*.md | wc -l` → 11). Integration ran in session
2026-10-19 `kaika W2a` with a 10-member L2 swarm (session artifact: this file,
`R12/integration/records-draft.md:1`; no lane-repo session log exists). Claims
measured at work commit `<WORK>`.

- C1 coverage (owned) — the fourth verb family's `ev_` Evidence-ID formula
  **lands as closed**: `inspect_go_binary` (REA 6.7.0) derives `ev_` + SHA-256
  of the canonical semantic Evidence; the projection includes
  `parameters.path`, `normalized_result.artifact.path`, and
  `locations[0].path`, and excludes outer display `subject.name` /
  `local_path` (`R12/claims/verdicts/VZ-1.md:26-30`; integration draft
  `R12/claims/c1/CR-4.md:1-11`). All 27/27 stored IDs recomputed; each of the
  seven convergent bundles also had a stable same-path repeat, while
  byte-identical copies at different paths produced different IDs
  (`R12/claims/verdicts/VZ-1.md:26-28`). Entry destination:
  `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`; token on the
  Evidence-model row, not the Go metadata row
  (`R12/claims/verdicts/VZ-1.md:30`; `corpus/README.md:41`). Command A:
  knowledge_files 90 → `<M:knowledge_files_after>`, mapped 90 →
  `<M:mapped_after>`, missing `<M:missing_list>`, dangling `<M:dangling_list>`
  (`SCORECARD.md:88-124`; baseline `R12/claims/verdicts/VZ-1.md:18-19`).
  Scope guard: the path-free `search_bytes` candidate is held as a separate
  Unknown, not disproved (`R12/claims/verdicts/VZ-1.md:32-34`).
- C2 depth (owned) — queue-drain rule #17 **lands** in `SKILL.md` after rule
  #16 and before `## Config custody` (`SKILL.md:279-297`): evidence-ID field
  sensitivity is a property of the operation's measured semantic projection,
  never a constant of the `ev_` prefix — pin operation/version/call shape/
  bytes, recompute from full envelopes, isolate one field or field set, use
  outer display fields as the negative control, and bound the result to the
  measured call shape (`R12/claims/verdicts/VZ-1.md:38-42`;
  `R12/claims/c2/EX-16.md:6-8`). Citations are only the r7/r10/r11 entries:
  `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:11,17-22`;
  `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:13-15,19-22`;
  `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:11-15,19-23`
  — all six ranges resolve under command A's citation pattern
  (`R12/claims/verdicts/VZ-1.md:44`). Rule #17 does not cite the r12 C1 entry.
  Command A: rule_blocks 16 → `<M:rule_blocks_after>`,
  citation_resolved_rules 16 → `<M:citation_rules_after>`
  (`R12/claims/verdicts/VZ-1.md:44`; baseline `R12/claims/verdicts/VZ-1.md:18-19`).
- C3 operability (fleet) — the citation-drift pointer table **lands** with
  PL-4's exact three rows grading the r7/r10/r11 `recheck:` lines
  (`R12/claims/c3/PL-4.md:36-60`; graded lines:
  `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md:5`,
  `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:7`,
  `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md:7`)
  and the matching `expected.json` pin `<M:expected_pointer_table_sha256>` —
  candidate `7470c3f6e956ce37e024ea34ae1f37002ebb515dc5a90d53eb9ad7a915d734f2`
  (`R12/claims/c3/PL-4.md:62-67`; canonical serializer
  `json.dumps(table, indent=2) + "\n"`, ASCII-escaped,
  `R12/claims/verdicts/VZ-1.md:58`). Table entries 57 →
  `<M:pointer_entries_after>`; strict probe `<M:strict_probe_verdict>`; each
  one-line `recheck:` seed produced exactly one `citation_dead` and strict
  exit 1 (`R12/claims/verdicts/VZ-1.md:48-56`). The rows grade recorded text
  only; they do not execute the recheck recipes
  (`R12/claims/verdicts/VZ-1.md:56`). No row references the r12 C1 entry.

Instruments at `<WORK>` (every value re-measured at the work commit; all
pending): command A knowledge_files `<M:knowledge_files_after>` / mapped
`<M:mapped_after>`, rule_blocks `<M:rule_blocks_after>` /
citation_resolved_rules `<M:citation_rules_after>`,
`<M:coverage_score>`/`<M:depth_score>`; census `<M:census_verdict>` + G21 +
unregistered-bullet guard + ptr `<M:ptr_state>`; citation-drift probe
findings `<M:probe_findings>` both modes; custody `<M:custody_cases>`/28;
PROVINCE `<M:province_lines>` held (r11 form: `SCORECARD.md:1977-2027`).

| axis | evidence | verdict |
|---|---|---|
| coverage — C1 | fourth `ev_` family closed; corpus 90 → `<M:knowledge_files_after>`; one map token (`R12/claims/verdicts/VZ-1.md:24-34`) | `<verdict>` |
| depth — C2 | rule #17 landed; rules 16 → `<M:rule_blocks_after>`; citations 16 → `<M:citation_rules_after>` (`R12/claims/verdicts/VZ-1.md:36-44`) | `<verdict>` |
| operability — C3 | pointer entries 57 → `<M:pointer_entries_after>`; strict probe `<M:strict_probe_verdict>`; three seeded recheck faults → `citation_dead`, exit 1 (`R12/claims/verdicts/VZ-1.md:46-62`) | `<verdict>` |
| calibration | no calibration claim in the frozen axes; baseline 10.0 (`R12/claims-frozen.md:11-14`; `STATE:63-70`) | unchanged |
| freshness | no freshness claim in the frozen axes (`R12/claims-frozen.md:11-14`) | unchanged |
| adjacency | `PROVINCE.md` boundary untouched; no adjacent-domain claim (`R12/claims-frozen.md:11-14`) | unchanged |

Learning trends: the `ev_` domain now has four measured verb families — r7
EVM, r10 Rust, r11 inspect-artifact, r12 inspect_go_binary — each
path-sensitive through its own projection, not a universal formula
(`R12/claims/verdicts/VZ-1.md:26-30`; `corpus/README.md:41`). The round also
records a reproducibility discipline: a pinned digest is meaningful only with
its serializer named, and VZ-1's own `ensure_ascii=False` attempt is recorded
as corrected rather than silently replaced (`R12/claims/verdicts/VZ-1.md:58`).
Operability moves from a clean-but-partial probe verdict to graded `recheck:`
lines (`R12/claims/verdicts/VZ-1.md:48-56`).

Saturation note (append-only; `## Saturation` at `SCORECARD.md:626-635` is not
rewritten): the arc3 window opened at r1 (`SCORECARD.md:1340-1342`, 1/10) and
r12 is the twelfth lane-round in it; every owned proxy is at 10.0
(`STATE:63-72`) and no capability row has entered since
arc2-r7/r8 (`SCORECARD.md:617-622`), so `AXES:66-73`'s nudge condition is met.
Defect D3 is recorded at `STATE:198`.

Planned: arc3-loop1-round13 — a capability/frontier move (nudge active; D3).
Primary candidate: ARM64X hybrid-PE analysis via Ghidra — one real host
carrier with `evidence_id` + subject SHA-256 + procedure count > 0 + chosen
language id; one new capability row, 4 → `<M:capability_rows_after>`
(`STATE:258`; `PROVINCE.md:83`). Second slot only if it fits the 1–3-claim
cap: typora `.jsc` named-function recovery, 0 named →
`<M:named_functions_after>` (`STATE:259`; `corpus/README.md:170-181`).
Either way, create `corpus/SOURCES.md` per contract v1 — opened rows only,
honest tiers, `## Paths` and `## Search log`; its capability row enters only
if every census command runs clean (`SCONTRACT:1-40`; `R12PROMPT:147-149`).
This `Planned:` line also closes the missing contract field D2
(`STATE:197`).

Carried debt: the mid-leg retest (operator-gated); the ASAR host-wide count
bounded by the unreadable `/opt/containerd` subtree; the Kimi session
`unknown`/`config_drift`; `.ufo/waves/arc2-loop1-round10/C3.md` still dirty;
`/tmp` quota standing (`SCORECARD.md:2023-2027`). New this round: `CN-1`
named non-completion (`R12/claims-frozen.md:70`); three landed entries still
carry DRAFT headers (D7, `STATE:202`); the path-free `search_bytes` candidate
remains an open Unknown (`R12/claims/verdicts/VZ-1.md:32-34`); the pointer
rows grade recorded text only and do not execute the recheck recipes
(`R12/claims/verdicts/VZ-1.md:56`).

# Block 2 — LOG.md entry

## 2026-10-19 — arc3-loop1-round12 (work commit `<WORK>`; records this entry)

Round 12 of arc3 loop 1: 48 seats frozen pre-dispatch on
`openai-codex/gpt-6-luna-max` (the scheduled `antigravity/gemini-3.8-flash`
slot — antigravity lane down, operator directive; `R12/claims-frozen.md:3-8`).
47/48 reports delivered; `CN-1` is the named non-completion
(`R12/claims-frozen.md:70`; `R12/claims/verdicts/` holds 11 reports).
Integration ran in session 2026-10-19 `kaika W2a` with a 10-member L2 swarm;
the parent's measurement is recorded at `<WORK>` (session artifact:
`R12/integration/records-draft.md`).

- C1 coverage: fourth verb family's `ev_` formula CLOSED —
  `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`:
  `inspect_go_binary` is path-sensitive through `parameters.path`,
  `normalized_result.artifact.path`, and `locations[0].path`; outer display
  fields are excluded; 27/27 stored IDs recomputed and the seven bundles each
  had a stable same-path repeat (`R12/claims/verdicts/VZ-1.md:26-30`). Map token landed on the
  Evidence-model row (`corpus/README.md:41`); command A 90 →
  `<M:knowledge_files_after>`.
- C2 depth: rule #17 landed (projection-local field sensitivity): pin
  operation/version/call shape/bytes, recompute from full envelopes, isolate
  the field or field set, use display fields as the negative control
  (`R12/claims/verdicts/VZ-1.md:38-42`). `rule_blocks` 16 →
  `<M:rule_blocks_after>`, all `<M:citation_rules_after>` resolved.
- C3 operability: citation-drift pointer table extended to grade the three
  `recheck:` lines (`R12/claims/c3/PL-4.md:36-60`); entries 57 →
  `<M:pointer_entries_after>`; strict probe `<M:strict_probe_verdict>`; each
  seeded recheck-line fault → `citation_dead`, exit 1
  (`R12/claims/verdicts/VZ-1.md:50-54`).
- Instruments at `<WORK>`: command A `<M:knowledge_files_after>` /
  `<M:mapped_after>` + `<M:rule_blocks_after>` / `<M:citation_rules_after>`,
  `<M:coverage_score>`/`<M:depth_score>`; census `<M:census_verdict>` + G21 +
  guard + ptr `<M:ptr_state>`; probe findings `<M:probe_findings>` both
  modes; custody `<M:custody_cases>`/28; PROVINCE `<M:province_lines>`
  (`SCORECARD.md:1977-2027` form; `LOG.md:1664-1683` model).

# Block 3 — `## Mistakes` mini-ledger

Scope: only classes this round shows. Each row checks `corpus/QUALITY.md`
(15 criteria, `corpus/QUALITY.md:11-25`; six weak signals,
`corpus/QUALITY.md:27-36`) for a capturing criterion.

## Mistakes — arc3-loop1-round12

| class | evidence pointer | captured-by criterion | fix |
|---|---|---|---|
| Dispatch-counting: one seat of the frozen 48 produced no report (`CN-1`) | `R12/claims-frozen.md:65-70` (roster names `CN-1`); `ls R12/claims/*/*.md \| wc -l` → 47 (c1 12, c2 12, c3 12, verdicts 11); lesson `corpus/lessons/2026-10-18-wave-dispatch-counting.md:5-16`; `STATE:174` | `none` — `corpus/QUALITY.md:11-25` has 0 matches for `dispatch\|seat\|items array`; the class lives in the lesson only | Record `CN-1` as the named non-completion, never an inferred shortfall; the freeze roster is the count. Add QUALITY #16 with the state's wording (`STATE:174`) |
| Publication-state: landed entries still carry seat-draft headers, including this round's own integration draft | `corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:5`; `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md:5`; `corpus/knowledge/2026-10-19-arc3-r10-rust-evidence-id-domain.md:1`; `R12/claims/c1/CR-4.md:1`; D7 `STATE:202` | `none` — no publication/header criterion in `corpus/QUALITY.md:11-25`; the only case-insensitive match is the unrelated "wave 15 draft" at `corpus/QUALITY.md:14` | This round's entry avoids it by landing the CR-4 body (`R12/claims/c1/CR-4.md:3-11` onward) with line 1's seat comment removed and line 3's `Draft —` opener dropped; acceptance `grep -c 'DRAFT for parent integration' corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` → 0 and the first line is the dated title |
| Digest serialization: the first PL-4 hash attempt used `ensure_ascii=False` and produced `ec7636…`, which was not the candidate byte stream | `R12/claims/verdicts/VZ-1.md:58`; candidate pin `R12/claims/c3/PL-4.md:66` | `none` — the two matches in `corpus/QUALITY.md` are `QUALITY.md:15` (canonical reject) and `QUALITY.md:24` (#14 `subject.digest.sha256`), neither pins a serializer | Name the exact serializer and bytes whenever a table/file digest is pinned; use `7470c3f6…` with default ASCII-escaped `json.dumps(indent=2) + "\n"`, never `ec7636…` (`R12/claims/verdicts/VZ-1.md:58`) |
| Contract drift: the frozen r12 claim set ran non-capability claims while the stagnation-nudge condition was already met (all owned proxies 10.0; no capability row since arc2-r7/r8) | `R12/claims-frozen.md:11-16`; `SCORECARD.md:626-635`, `SCORECARD.md:1340-1342`, `SCORECARD.md:617-622`; `AXES:66-73`; D3 `STATE:198` | `none` — the two matches in `corpus/QUALITY.md` are `QUALITY.md:18` (#8) and `QUALITY.md:20` (#10), which govern capability claims, not the nudge obligation; the governing clause is `AXES:66-73` | The `Planned:` line in Block 1 names the r13 capability/frontier move (ARM64X via Ghidra; typora `.jsc` second slot; `SOURCES.md` contract v1); D3 discharges only when that capability demonstrates running |

Intended fold: the round's lesson `## Mistakes` section (the contract row
`R12PROMPT:155-158` names that section).
