# Round 17 — retained Go carrier diagnostics and routed provenance/invocation defects

author: kaidoku-shokunin; 2026-10-20
scope: eight real, pinned x86-64 Linux Go carriers analysed by REA 6.5.0 (Ghidra 12.1.4) with retained, run-bound analyzer logs, compared with routes predicted from installed source and frozen in Git first; append-only corrections for the two routed r16 outside defects. No carrier is executed, and no recovery quality or patched-content correctness is claimed.

## Claims

- C1 calibration (tied-lowest owned axis at 10.0): discharge routed defects
  R16-PROVENANCE and R16-INVOCATION
  (`corpus/lessons/round-16-verifier-spotcheck.md:183-184`). Each
  temporal-stability site gets a named, line-exact correction, and a pinning
  tool whose failure is demonstrated replaces bare booleans. Every SKILL
  registry row's command matches an exercised retained argv; this needs the
  two unlabelled variants re-exercised. QUALITY #19 is added.
- C2 depth, with capability acquisition: real-carrier analyzer diagnostics
  discriminate the Go snapshot routes (none / info / fallback / no build-info)
  against frozen predictions. QUALITY #20 is added, and the capability row is
  entered only after receipts validate.

## Gate

### Candidate decisions (author-side; outside sampling remains the closure's duty)

| Candidate | Decision | Evidence and limits |
|---|---|---|
| Knowledge entry `2026-10-20-r17-go-carrier-diagnostics` with route decision table | admit | 8 receipts with one bound session each and pins equal pre/mid/post; predictions committed at `271167473d87ef710f07ecdd98caf0ce12091686` before the first run; 8/8 compare exit 0 (6 prospective) |
| QUALITY #19 temporal records / #20 bound provider logs | admit | #19 from R16-PROVENANCE; #20 from this round's attribution and echo findings (Mistakes rows 3, 6) |
| SOURCES S024, S025, S026, S027, S029, S030 | admit (mined) | Opened 2026-10-20; quotes below; each cited by the entry or this lesson |
| SOURCES S028 Go 1.27 release notes | reject (row kept) | No `nodwarf5`/dwarf text; S026 source grounds the token instead |
| "The 1.15–1.25 range check stops Go analysis" | reject | `GoRttiMapper.java:170-172` only logs. On this host, out-of-range co-occurs with a missing base, so the runs cannot separate the two; source can |
| "Go 1.26/1.27 layout changes break recovery" | reject | Failure is in the constructor before any moduledata read; layout is neither shown nor excluded |
| "`GoRttiMapper` `…for version X` proves the selected data" | reject | notesmd-cli and aether logged `Falling back from X to 1.25.0` and then `…for version X` |
| "aether's symbol-markup EOF is caused by 1.25.0 fallback data" | reject | Unpredicted; no control separates fallback data from carrier layout; recorded UNKNOWN |
| "Historical op 2.40.0 cause is now established" | reject | That package is gone; current op 2.41.0-1 (go1.26.8) is a different binary |
| "The pilot runs demonstrate the capability" | reject | Pilot had no pins, no binding, and no receipt (`.ufo/waves/round-17/pilot/README.txt`) |
| "8/8 matches prove the predictor generally" | reject | One host, x86-64 ELF, one run per carrier, Ghidra 12.1.4 only; two carriers were calibration (pilot-seen) |
| "Retained log = complete log" | reject | REA kills the post-script analysis pass on close (w1 `RevReaLifecycle.md`); the capture is a prefix. Every Go line precedes the bridge script |

### Opened sources and located quotes (access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S024 | https://go.dev/src/debug/buildinfo/buildinfo.go, line 58 (go1.27.3) | `var buildInfoMagic = []byte("\xff Go buildinf:")` |
| S024 | same, line 97 | `bi.GoVersion = vers` |
| S025 | https://go.dev/doc/devel/release, `#go1.27.0` | go1.27.0 (released 2026-08-19) |
| S025 | same, Release Policy | Each major Go release is supported until there are two newer major releases. |
| S026 | https://go.dev/src/cmd/link/internal/ld/main.go, line 197 (go1.27.3) | `buildVersion += sep + "X:" + goexperiment` |
| S026 | https://go.dev/src/internal/buildcfg/exp.go, line 158 (go1.27.3) | (Experiments in the same state as in the baseline are elided.) |
| S027 | https://github.com/golang/go/issues/75953, dmitshur comment 2025-10-17 | A simple change might be to replace the space with a dash, like "go1.25.3-X:nodwarf5". |
| S028 | https://go.dev/doc/go1.27, "Faster memory allocation" | You may set GOEXPERIMENT=nosizespecializedmalloc at build time to disable |
| S029 | https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/Ghidra_12.1.4_build/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java, line 79 | public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25"); |
| S029 | https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174.patch, patch line 151 | `+	public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26");` |
| S030 | https://github.com/mandiant/GoReSym/releases/tag/v3.3, release body | Add 1.26 support |

These are code, issue-thread and HTML sources, so they were checked manually
under QUALITY #1/#17. None is a machine-gradeable raw-prose submission. The
quotes were taken by w1 seats (`ScoutGoBuildinfoDocs`, `ScoutGoReleaseHistory`,
`ScoutGoExperimentSuffix`, `DraftSourcesRows`, `ScoutGhidraUpstreamGo`,
`ScoutGoReSymReleases`), which are author-side. The outside closure should
reopen a sample.

### Registry transitions (old → new)

- S003 `used-by` old: `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md, corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md` → new: the same list plus `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md`.
- S023 `used-by` old: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md` → new: the same plus `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`. The 1.25.x fallback carriers loaded this base.
- S024–S030 are new rows. No status or recheck changes on existing rows, and no tier changes.
- Leads: the GoReSym-releases lead is resolved by S030. The "Ghidra release notes after 12.1.4" half of the last lead is resolved by S029. The IDA/Hopper/JEB references remain unopened.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| vacuous / number-drift — R16-PROVENANCE | `.ufo/waves/round-16/verification.json:419` boolean with one hash map; sites `LOG.md:2012`, `corpus/lessons/round-16.md:154`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`, verification.json:419 (fleet report `.ufo/reports/round-16/kaidoku.md:60` is out of lane) | none — QUALITY #18 asks for producer and inputs, not instants (w1 `ConnProvenanceRoutes.md`) | `tools/pins.py` (pre, 30 s mid-run and post maps with timestamps) used by `carrier-run.py`; QUALITY #19; line-exact corrections below. Able to fail: `pins.py --selftest` red case (mutated file → compare exit 1 naming the path) |
| survivor / reference-drift — R16-INVOCATION | `SKILL.md:448` (citation-drift) and `:449` (custody-pair) at baseline `b563c79`: `invocation-audit.py` classes them `unlabelled_variant` (2 of 7 rows) | QUALITY #18 in prose, applied only to the named r15 instances | Both rows now advertise the exercised isolated absolute argv, re-exercised this round with retained argv. The audit counts the whole registry. Able to fail: the baseline run shows 2 variants |
| scope — L1 contract undercount | `contract.md` temporal-sweep site list and regex found 2 of 4 lane sites (missed the `across execution` phrasing and the knowledge entry). w1 `CriticC1Vacuity`, `ScoutTemporalWording`, `ReviewContract` F5 | author-side critics this round | Sweep widened to `corpus/knowledge/` with wrapped-line joining and run/execution-scoped phrases. A correction needs marker + exact `file:line` + "temporal stability not evidenced", and sites are read at the baseline (`--sites-rev`). Able to fail: selftest cases 2–3 (path-only marker and deleted site stay unqualified) |
| stale-premise — L1 contract law | `contract.md` named a nonexistent `GoVer.fromVersionString` and equated missing bootstrap with missing base. w1 `ReviewContract`, `ScoutGoVer`, `ScoutGoRttiMapper` | author-side review | `predict.py` strips `go` per `GoBuildInfo.java:488-489` before `GoVer.parse`. The missing-base proxy is labelled as a proxy of the stronger source condition (`GoRttiMapper.java:351-361`) |
| landing — write into a frozen dir | `.ufo/waves/round-16/__pycache__/selection.cpython-314.pyc` created 10:32 by a w1 seat importing r16 `selection.py` under `python3 -I` (w1 `CriticNoHarm.md`); gitignored, so Git-object controls could not see it | none | Removed before commit. Every r17 tool invocation uses `-B`, and predict/carrier-run import with bytecode writes disabled. Able to fail: `python3 -I` without `-B` recreates the file |
| vacuous — non-discriminating compare field | `contract.md` compare fields; the requested-label echo (`GoRttiMapper.java:179-180`) matches on exact and fallback runs alike (w1 `CriticC2Novelty` V1, `ConnRequestedLabel`) | none | `snapshot_route`/`fallback_to` read from the `GoApiSnapshot` component, predicted from `GoApiSnapshot.java:148-166`. Able to fail: the notesmd-cli prediction with its route forced to `info` makes compare exit 1, while the three contract fields alone exit 0 (retained in verification) |
| attribution — unbound session logs | contract polled every new `/tmp/rea-ghidra-*`; a live REA MCP server and sibling lanes share `/tmp` (w1 `SentinelPollRace`, `SentinelCarrierSafety` F1) | none | Private `TMPDIR` per run, plus binding from the log's own `Using log file:` and `IMPORTING:` lines; exit 2 unless exactly one bound session. QUALITY #20. All eight receipts: bound 1, unbound 0 |
| scope — routed site list | `round-16-verifier-spotcheck.md:183` names SCORECARD (0 matching lines at `b563c79`) and omits the knowledge entry | outside closure (route) vs this lane's search | Sites are found by search at the pinned baseline, not copied from a prose list. No SCORECARD correction is invented |
| provider — dispatch refusals | `.ufo/waves/round-17/wave1-dispatch-attempts.json`: two whole-wave refusals (job cap 100), then 78 spawned on attempt 3 | host job cap, not a lane gate | Same payload retried every 180 s, never split |

### R16-PROVENANCE named corrections (append-only; filed bytes unchanged)

- R16-PROVENANCE: `LOG.md:2012` map matches committed source-revision blobs; temporal stability not evidenced.
- R16-PROVENANCE: `corpus/lessons/round-16.md:154` map matches committed source-revision blobs; temporal stability not evidenced.
- R16-PROVENANCE: `.ufo/waves/round-16/verification.json:419` map matches committed source-revision blobs; temporal stability not evidenced.
- R16-PROVENANCE: `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` map matches committed source-revision blobs; temporal stability not evidenced.
- The fleet report site `.ufo/reports/round-16/kaidoku.md:60` is outside this lane; its correction is carried by this round's fleet report.

## Integration boundaries

The initial lane state was clean at `b563c799d97774aae4351276fe43cb897311e349`.
The bounded watchdog search for `lane-dead-no-report kaidoku round=17`
returned nothing (exit 1). There are no inherited leftovers. The four prior
outside verifier files are unchanged. No `corpus/lessons/operator-*` file
exists. The L1 holds the canonical planner seat. W1 was 78 seats, all
completed. The pilot (10:17–10:19) is retained as calibration only, before
`claims.json` (10:25) and the frozen predictions.

Tool installs/updates: none by the L1. Seat `DraftSourcesRows` installed Go
1.27.3 linux/amd64 from the official go.dev tarball (sha256 matched
`go.dev/dl/?mode=json`) into `~/.local/opt/go-1.27.3`, not on PATH, to read
the toolchain source. No pacman transaction was run.
