# kaidoku round 17 — fleet report draft (W2, author-side, not the final report)

Target report: `.ufo/reports/round-17/kaidoku.md` (L1 integrates; this draft is not final).
Baseline: `b563c799d97774aae4351276fe43cb897311e349`. Integrated source revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`. Freeze of predictions: `2711674` (= `271167473d87ef710f07ecdd98caf0ce12091686`).
Axes: calibration (C1), depth (C2). Claims: `.ufo/waves/round-17/claims.json`.
Slot syntax: `{{SLOT: …}}` = value L1 fills from its own final run or commit. Numbers below marked *measured* were re-run by this seat against `da64646` (read-only tools, git objects, retained files). Every *measured* value is a tool output, not a claim from a prior seat.

## Work performed

- **C1 — calibration: discharge R16-PROVENANCE and R16-INVOCATION** (claims.json C1; contract.md:12, :80, :90).
  - Temporal-stability sites: *measured* `temporal-sweep.py --root . --rev da64646 --sites-rev b563c79` → sites 4, corrected 0, unqualified 4 at baseline; at `da64646` corrected 4, unqualified 0. The tool regex (`tools/temporal-sweep.py:55-57`) is wider than contract.md:93; the count is bounded to the tool's file scope (see Sources & frontier).
  - Registry variants: *measured* `invocation-audit.py --rev b563c79` → 7 rows, 5 exercised_match, 0 labelled_unexercised, 2 unlabelled_variant. At `da64646` → 17 rows, 6 exercised_match, 0 labelled_unexercised, **11 unlabelled_variant**. Target was 0.
  - QUALITY row 19 presence: *measured* 0 → 1 (`measure.py`, `C1_quality_row19`). QUALITY rows 18 → 20 (row 20 is not in claims.json; see Landed changes).
- **C2 — depth: Go bootstrap discrimination with retained Ghidra analyzer log** (claims.json C2; contract.md:31, :51, :62, :75).
  - Eight pinned carriers run through REA 6.5.0 `analyze` with `carrier-run.py`; 8/8 carrier-run exit 0; 8/8 compare exit 0 (two calibration carriers seen in the pilot, six prospective).
  - Retained receipts: 8 (`runs/*/receipt.json`). `receipt-validate.py` on these receipts: **0/8 valid** (see Before → after).
  - Tool work: 11 round-17 tools present (`measure.py` `tools_present` 0 → 11). Selftests were run by their executor seats; this seat ran `pins.py --selftest` (CLEAN cases=7) and `receipt-validate.py --selftest` (CLEAN cases=5).
  - Pilot (not measured runs): `.ufo/waves/round-17/pilot/README.txt`; `pilot/SHA256SUMS` verifies from the pilot directory.

## Landed changes

- Work commit: `da64646adcb19c1ede7537b799b8c7d283fe43da` (126 files, 33393 insertions, 94 deletions vs `b563c79`). Records commit: {{SLOT: hash of the post-measurement record commit}}.
- Knowledge entry `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (C2): landed (`measure.py` `C2_knowledge_entry` 0 → 1). Its prediction-freeze hash is printed as `2716747` at line 37; the correct short hash is `2711674` — {{SLOT: L1 corrects in the knowledge file before admission}}.
- QUALITY rows 19 and 20 (`corpus/QUALITY.md:29-30`). Row 19 is the C1 requirement. Row 20 is not in claims.json; its source cites the round-17 knowledge entry it sharpens. {{SLOT: admission decision for row 20}}.
- Append-only corrections for round-16 temporal assertions: `LOG.md:2059-2062` name `LOG.md:2012`, `corpus/lessons/round-16.md:154`, `.ufo/waves/round-16/verification.json:419`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`. `temporal-sweep.py` marks all four `corrected: true`.
- SOURCES: rows S024–S030 added (S028 rejected); S003 and S023 used-by extended in place.
- SKILL.md: round-17 registry section appended (`SKILL.md:509-540`); citation-drift and custody-pair rows aligned in place (`SKILL.md:448-449`).
- SCORECARD capability row `retained REA Ghidra-session log`: **not landed** at `da64646` (`measure.py` `scorecard_capability_rows_matching` 0). {{SLOT: landed in record commit, or withheld with rule applied}}.
- SHONEN.md: **not changed** (`git diff b563c79 da64646 -- SHONEN.md` is empty).

## Before → after measurements

| claim | before (`b563c79`) | after (`da64646`) | evidence | measured by |
|---|---|---|---|---|
| C1a temporal sites, unqualified | 4 unqualified | 0 unqualified (4 corrected) | `temporal-sweep.py --rev da64646 --sites-rev b563c79` | this seat |
| C1b registry rows, unlabelled_variant | 2 of 7 | **11 of 17** (target 0) | `invocation-audit.py --rev da64646` | this seat |
| C1b citation-drift re-exercised in round 17 | not retained | **not retained** (matched receipt is `.ufo/waves/round-16/verification.json`) | `invocation-audit.py` output | this seat |
| C1c QUALITY row 19 | 0 | 1 | `measure.py` | this seat |
| C2 retained Go carrier runs (carrier + evidence id + log sha256 + prediction) | 0 | 8 retained; 6 prospective + 2 calibration | `runs/*/receipt.json`, `runs/*/compare.json` | this seat |
| C2 receipts that pass `receipt-validate.py` | n/a | **0 of 8** | `receipt-validate.py runs/<label>/receipt.json` exit 1, `unrecognized_shape` | this seat |
| C2 capability rows matching "retained REA Ghidra-session log" | 0 | 0 (target +1 only if capture runs and receipt validates) | `measure.py` | this seat |
| Sources registry rows | 23 | 30 (mined 22 → 28; rejected 1 → 2; tier A 21 → 26, B 1 → 2, C 1 → 2) | `measure.py` | this seat |
| Knowledge files | 94 | 95 | `measure.py` | this seat |
| QUALITY rows (1–18 byte-identical) | 18 | 20 (violations {}) | `controls.py b563c79 da64646` | this seat |

Carrier table (eight runs; full digests in receipts). Analyze and inspect Evidence IDs are in `runs/<label>/receipt.json`.

| label | carrier sha256 (`carrier.sha256_post` = `_pre`) | build-info Go | predicted route | observed GoApiSnapshot line | bootstrap | pins pre/post |
|---|---|---|---|---|---|---|
| calib-shfmt | `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459` | go1.27.0-X:nodwarf5 | none, untested 1.27.0 | none; `Untested` ×2 log lines | missing (×2) | equal, 146 paths |
| calib-esbuild-0.25.12 | `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014` | go1.23.12 | info | info | loaded (1 attempt) | equal, 146 paths |
| pro-notesmd-cli | `412dc532d278b9e4aaf502891ea1f7b5c60e7572fb82935778ebdb728000802d` | go1.25.8 | fallback → 1.25.0 | fallback (WARN ×1) | loaded | equal, 146 paths |
| pro-aether | `06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e` | go1.25.14 | fallback → 1.25.0 | fallback (WARN ×1) | loaded; 6115 types; then analyzer EOF | equal, 146 paths |
| pro-esbuild-0.21.5 | `b567f467fdac92c606717c86ea5cd1d6c30145c616776c0f2ff5429ad48586ba` | go1.20.12 | info | info | loaded | equal, 146 paths |
| pro-containerd-shim | `d3aa80d720b80f70721a3e66997fcfc72fdfc4d5ef304094e0173e829dbf370d` | go1.27.2-X:nodwarf5 | none, untested 1.27.2 | none | missing (×2) | equal, 146 paths |
| pro-op | `f4ac474fd0202c73e93cec7ff35e5c7a0b46df593b8717c92a262ecd4d77f818` | go1.26.8 | none, untested 1.26.8 | none | missing (×2) | equal, 146 paths |
| pro-esbuild-0.27.7 | `c638273fcf95573ca74af586677800b4dd874c55f8f945adb54316d6902ba14b` | none (no build-info) | hand: none, no version lines | none; analyzer `unable to get GoRttiMapper` ×2 | no mapper | equal, 146 paths |

- Prediction mismatches (reported, not hidden): 0 mechanical mismatches on the five compared fields. Unpredicted: aether `Go analysis failure … EOFException` after a successful fallback bootstrap (`runs/pro-aether/logs/*/ghidra.log:97,177`); cause UNKNOWN.
- Evidence ID repeat: calib-shfmt `ev_2b29a1ddfaead9d13a3d8923a2edc176dbe8ebda0ac776707625c6c1de3c5be3` and calib-esbuild `ev_391dbfe69769673c3af0bb7575e730e311f6f8bd273d848126d8f5addc22b03f` match the pilot IDs (one repetition, not a determinism proof).
- Retained-log capture: 8/8 receipts show one bound session and zero unbound; polling copy with `log_capture_limit` set.
- Pilot observation (not measured): `pilot/shfmt-log/ghidra.log:83` `Untested Go version [1.27.0]`; `pilot/esbuild-0.25.12-log/ghidra.log:64` `Using Go API snapshot for version 1.23.12`.

## Sources & frontier

- Go source anchors (installed `Base-src.zip`): `GoRttiMapper.java:79` declared range `1.15-1.25`; `:171` `Untested Go version`; `:359` missing bootstrap message; `GoVer.java:46` `parse`. Reopened: S003, S023.
- New SOURCES rows: S024 (Go `debug/buildinfo`), S025 (Go release history), S026 (Go linker `X:` suffix), S027 (golang/go issue #75953, rationale only), S028 (Go 1.27 release notes, rejected), S029 (Ghidra upstream range, tag vs master), S030 (GoReSym v3.3 release). Measured: 30 rows.
- Bounded scope: the temporal N→0 holds only for the tool's file scope (LOG, SCORECARD, lessons/round-16, SKILL, round-16 verification.json, plus the knowledge file). Lane-wide sites outside that scope remain: {{SLOT: list from the repo-wide grep; see DraftReportR17.md F5}}.
- Frontier (open, not claimed): Go 1.27 symbol recovery is an expected bootstrap failure, not a target (claims.json non_claims). Aether analyzer EOF: cause unknown. GoReSym v3.3 recovery on a 1.26 carrier: not opened.

## Trend verdicts

Per-axis (no scalar). Fill from measured before/after only.

| axis | verdict | evidence |
|---|---|---|
| calibration | {{SLOT: improved / unchanged / harmed}} | C1a 4→0 unqualified in tool scope; C1b unlabelled 2→11 (target 0 not met); receipt validation 0/8 |
| depth | {{SLOT: improved / unchanged / harmed}} | 0→8 retained carrier runs; 8/8 compare exit 0; capability row not landed; receipts not validated |
| coverage | {{SLOT}} | 8 carriers, 4 Go-version classes (1.20, 1.23, 1.25, 1.26/1.27) |
| operability | {{SLOT}} | `carrier-run.py` single-command path; `receipt-validate.py` rejects its receipts |
| freshness | {{SLOT}} | predictions frozen at `2711674` before runs |
| adjacency | {{SLOT}} | {{SLOT}} |

Admission: {{SLOT: admitted | withheld, with the rule applied. Recommended: knowledge entry admitted only after the `2716747`→`2711674` correction; capability row withheld until a receipt validates.}}

## SHONEN

Promotion checklist (`SHONEN.md`, unchanged at `da64646`). This round does not authorize any `[x]`; boxes stay `[~]` unless an independent non-author verifier establishes them.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SHONEN.md:5`. Delta: round-17 section appended (`SKILL.md:509-540`); 11 registry rows unlabelled at `da64646`.
- [~] At least one end-to-end domain task executed and logged in LOG.md — `SHONEN.md:7`. Delta: eight retained carrier runs logged (`LOG.md:2044-2066`); no outside verifier.
- [~] Instructions executable by an agent without oral context — `SHONEN.md:9`. Delta: `run-carriers.sh` and `carrier-run.py` run from the lane; receipt-validate does not accept the receipts it is meant to check.
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `SHONEN.md:11`. Delta: `PROVINCE.md` line 52 qualified in place; PROVINCE otherwise untouched.

## Stale-lane

Stale-lane: {{SLOT: output of the bounded watchdog sweep `(lane-dead-no-report kaidoku round=17|launch kaidoku round=17|complete kaidoku round=17)` run at record time}}. Observed at `da64646`: the round-17 LOG entry (`LOG.md:2032-2066`) contains no stale-lane line; the round-16 precedent (`corpus/lessons/round-16.md:69-71`) did.

## Tool installs/updates

- **Go toolchain go1.27.3 linux/amd64** — seat `DraftSourcesRows` (w1). Channel: official `go.dev/dl` tarball, sha256 verified against `go.dev/dl/?mode=json` (seat record: `65efbc80…b40`; not re-verified by this seat). Location: `~/.local/opt/go-1.27.3`, not on PATH. Reason: read stdlib `debug/buildinfo` and run `go version <file>` (reads bytes; no carrier execution). Verified present: `go version` → `go1.27.3 linux/amd64`. Deviation to record: operator directive names `~/.local/bin` for official binaries; this is a tree under `~/.local/opt`.
- This seat (DraftReportR17): no installs, no upgrades, no pacman operation.
- Lane tooling: no `pacman` transaction. Read-only `pacman -Qo` used for carrier owners (four of five owned; `notesmd-cli` unowned).
- {{SLOT: any further seat-level installs, each as tool, version, channel, reason}}

## Cross-domain evidence

- Carrier provenance: `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@{0.21.5,0.25.12,0.27.7}` (esbuild, from another project's pnpm store; read-only); `/usr/bin/shfmt` 3.14.1-1; `/usr/bin/aether` 4.32.0-2; `/usr/bin/op` 1password-cli 2.41.0-1; `/usr/bin/containerd-shim-runc-v2` containerd 2.4.2-1; `~/.local/bin/notesmd-cli` (no package owner). Carrier installs are outside the kaidoku lane.
- Routed outside defects: `corpus/lessons/round-16-verifier-spotcheck.md:183-184` (R16-PROVENANCE, R16-INVOCATION). Disposition: {{SLOT: discharged in part; C1b open per Before → after}}.
- No sibling gate, agent database, credential/auth file, client routing or host service accessed by this seat. {{SLOT: L1 confirms for the lane}}.

## Wave stats

Observed from the dispatch artifacts (not measured outcomes):

- Wave 1: 78 spec items (`wave1-spec.json`); role histogram scout 20, executor 14, reviewer 12, scribe 10, connector 8, critic 6, revenger 4, sentinel 2, simplifier 2. Dispatch attempts: 1 refused 78, 2 refused 78, 3 refused 0 (`wave1-dispatch-attempts.json`; the file records no cause). Registry: 78 members, all `kind: spawn`.
- Wave 2 (falsify): 69 spec items (`wave2-spec.json`); role histogram reviewer 18, executor 16, scout 9, critic 8, scribe 5, mutation-tester 4, connector 3, revenger 3, sentinel 2, simplifier 1. Dispatch: 1 attempt, 0 refused, 69 spawned (`wave2-result.txt`).
- Seat outcomes (wave 1): {{SLOT: delivered / failed / substantive count}}
- Failed seats not counted as substantive: {{SLOT}}
- Wave 2 outcomes: {{SLOT: delivered / failed / substantive count}}
