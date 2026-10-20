# Round 17 — retained Go carrier diagnostics and routed provenance/invocation defects

author: kaidoku-shokunin; 2026-10-20
scope: eight real, pinned x86-64 Linux Go carriers analysed by REA 6.5.0 (Ghidra 12.1.4) in two passes, with retained, run-bound analyzer logs compared against routes predicted from installed source and frozen in Git before the measured runs; append-only corrections for the two routed r16 outside defects. No carrier is executed, and no recovery quality or patched-content correctness is claimed.

This file was first committed mid-round at `da64646adcb19c1ede7537b799b8c7d283fe43da`. The falsify wave (w2) then attacked it. This version revises it before round close, and every revision is listed under "In-round revisions". The same applies to the round-17 knowledge entry, SOURCES rows S024–S030 and QUALITY rows 19–20, all of which were added this round.

## Claims

- C1 calibration (tied-lowest owned axis at 10.0): discharge routed defects
  R16-PROVENANCE and R16-INVOCATION
  (`corpus/lessons/round-16-verifier-spotcheck.md:183-184`).
  - Each in-lane temporal-stability site gets a named, line-exact
    correction.
  - A pinning tool whose failure is demonstrated replaces bare booleans.
  - Every SKILL registry row's command matches an argv that was exercised and
    retained.
  - QUALITY #19 is added.
- C2 depth, with capability acquisition: real-carrier analyzer diagnostics
  discriminate the Go snapshot routes (none / info / fallback / no
  build-info) against frozen predictions. QUALITY #20 is added. The
  capability row is entered only after the receipts validate.

## Gate

### Candidate decisions (author-side; outside sampling remains the closure's duty)

| Candidate | Decision | Evidence and limits |
|---|---|---|
| Knowledge entry `2026-10-20-r17-go-carrier-diagnostics` with route decision table | admit | Two passes, each with 8 receipts. Every receipt has one session bound by whole log records plus the full carrier MD5. Second-pass pins are equal at every retained instant. Predictions were committed at `271167473d87ef710f07ecdd98caf0ce12091686` before the first measured run. 8/8 compare exit 0 in both passes. 3 of the 6 prospective carriers tested routes unseen at freeze |
| QUALITY #19 (temporal records) and #20 (bound provider logs) | admit | #19 from R16-PROVENANCE, plus this round's own recurrence (Mistakes row 10). #20 from this round's attribution and echo findings (Mistakes rows 6–7) |
| SOURCES S024–S027, S029–S032 | admit (mined) | Opened 2026-10-20; quotes below. Each is cited by the entry or by this lesson. S032 is a tier-B community lead, never sole support |
| SOURCES S028 Go 1.27 release notes | reject (row kept) | No `dwarf` text in the 1.27 notes. S026 source and S031 ground the `nodwarf5` token instead |
| "The 1.15–1.25 range check stops Go analysis" | reject | `GoRttiMapper.java:170-172` only logs. On this host, out-of-range always co-occurs with a missing base, so the runs cannot separate the two; the source can |
| "Go 1.26/1.27 layout changes break recovery" | reject | The failure occurs in the constructor, before any moduledata is read. Layout is neither shown nor excluded |
| "`GoRttiMapper` `…for version X` proves the selected data" | reject | notesmd-cli and aether logged `Falling back from X to 1.25.0` and then `…for version X` |
| "aether's symbol-markup EOF is caused by the 1.25.0 patch fallback" | reject | The failing binding is the base `go1.25.0.json` alias `runtime.maptype → OldMapType`, which the fallback does not change. notesmd-cli has no map types with method info, so it is not a control (w2 `CriticAetherUnknown`). Kept as a labelled INFERENCE, not an observation |
| "Historical op 2.40.0 route is now observed" | reject | r4-10 recorded go1.26.8, which by version falls in the missing-base class. Its log was never retained and the package is gone |
| "The pilot runs demonstrate the capability" | reject | The pilot had no pins, no binding and no receipt (`.ufo/waves/round-17/pilot/README.txt`) |
| "8/8 matches prove the predictor generally" | reject | One host, x86-64 ELF, Ghidra 12.1.4, two passes. Two carriers are calibration (pilot-seen) and three more repeat pilot-seen routes |
| "Retained log = complete log" | reject | REA kills the post-script analysis pass on close (w1 `RevReaLifecycle.md`), so the capture is a prefix. All 16 retained logs reach `REPORT: Analysis succeeded` before the bridge script |
| "Analyze Evidence IDs replicate across passes" (frozen in `predictions/replicate-expectations.json`) | reject for aether, admit for 7/8 | aether `string_count` 29118 → 29117 changed its id (`ev_ae9f7086…` → `ev_247261e8…`). The other seven ids, every route, every bootstrap count and the aether EOF pair `17645861, 111938854` replicated |

### Opened sources and located quotes (access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S024 | https://go.dev/src/debug/buildinfo/buildinfo.go, line 58 (go1.27.3) | `var buildInfoMagic = []byte("\xff Go buildinf:")` |
| S024 | same, line 97 | `bi.GoVersion = vers` |
| S024 | same, line 411 | `return 0, errNotGoExe` |
| S025 | https://go.dev/doc/devel/release, `#go1.27.0` | go1.27.0 (released 2026-08-19) |
| S025 | same, `#go1.27.3` | go1.27.3 (released 2026-10-19) |
| S026 | https://go.dev/src/cmd/link/internal/ld/main.go, line 197 (go1.27.3) | `buildVersion += sep + "X:" + goexperiment` |
| S026 | https://go.dev/src/internal/buildcfg/exp.go, line 158 (go1.27.3) | (Experiments in the same state as in the baseline are elided.) |
| S027 | https://github.com/golang/go/issues/75953, dmitshur comment 2025-10-17 | A simple change might be to replace the space with a dash, like "go1.25.3-X:nodwarf5". |
| S028 | https://go.dev/doc/go1.27, "Faster memory allocation" | You may set GOEXPERIMENT=nosizespecializedmalloc at build time to disable |
| S029 | https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/Ghidra_12.1.4_build/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java, line 79 | public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25"); |
| S029 | master HEAD `b8e9917e4c01959fe97ba94954731ed8cf2d201c`, same file, line 79 | public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.26"); |
| S030 | https://github.com/mandiant/GoReSym/releases/tag/v3.3, release body | Add 1.26 support |
| S031 | https://go.dev/doc/go1.25#dwarf5-support, page lines 628-629 (rendered text spans a `<code>` element) | DWARF 5 generation can be disabled by setting the environment variable GOEXPERIMENT=nodwarf5 at build time |
| S032 | https://github.com/NationalSecurityAgency/ghidra/pull/9348, page title | Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries |

These are code, issue-thread and HTML sources, so they were checked manually
under QUALITY #1/#17. None is a machine-gradeable raw-prose submission. W1
seats opened and quoted them. The L1 reopened S031 and S032 itself. W2 seats
`ReopenS024`–`ReopenS030` re-opened each row's quotes on 2026-10-20 and found
them exact. All of these seats are author-side; the outside closure should
reopen a sample.

### Registry transitions (old → new)

- S003 `used-by` old: `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md, corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md` → new: the same list plus `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md`.
- S023 `used-by` old: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md` → new: the same plus `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`. The 1.25.x fallback carriers loaded this base.
- S024–S032 are new rows. Existing rows had no status or recheck changes and no tier changes.
- Leads: the GoReSym-releases lead is resolved by S030 and narrowed to "type recovery on a 1.26 carrier". The "Ghidra release notes after 12.1.4" lead is resolved by S029. The IDA/Hopper/JEB references remain unopened.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| vacuous / number-drift — R16-PROVENANCE | `.ufo/waves/round-16/verification.json:419` boolean with one hash map; in-lane sites `LOG.md:2012`, `corpus/lessons/round-16.md:154`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`, verification.json:419. The fleet report `.ufo/reports/round-16/kaidoku.md:60` is out of lane and is corrected in this round's report | none: QUALITY #18 requires producer and inputs, not instants (w2 `ConnProvenanceRoutes`) | `tools/pins.py`, and `carrier-run.py` retaining every pin check with its instant; QUALITY #19; line-exact corrections below. Able to fail: `pins.py --selftest` red case (mutated file → compare exit 1 naming the path), and `receipt-validate.py --selftest` case `carrier_mid_run_drift_red` |
| survivor / reference-drift — R16-INVOCATION | At baseline `b563c79`, `invocation-audit.py` classes `SKILL.md:448` (citation-drift) and `:449` (custody-pair) as `unlabelled_variant` (2 of 7) | QUALITY #18 | Both rows now advertise the isolated absolute argv that the round-17 verification pass exercised (`.ufo/waves/round-17/verification.json`, labels `citation-strict` and `custody-capture`). Able to fail: the baseline audit run shows 2 variants |
| scope — L1 contract undercount | The w1 `contract.md` temporal-sweep site list and regex found 2 of 4 lane sites (w1 `CriticC1Vacuity`, `ScoutTemporalWording`) | rule (author-side critics this round) | The sweep covers `corpus/knowledge/` and `corpus/lessons/`, joins wrapped lines and uses run/execution-scoped phrases. A correction needs the marker, the exact `file:line` and the required phrase, and sites are read at the baseline (`--sites-rev`). Able to fail: selftest cases 2, 3 and 3b |
| stale-premise — L1 contract law | `contract.md` named a nonexistent `GoVer.fromVersionString` and equated missing bootstrap with missing base (w1 `ReviewContract`). Amended as-built at the end of `contract.md` | rule (author-side review) | `predict.py` strips `go` per `GoBuildInfo.java:488-489` before `GoVer.parse`; the missing-base proxy is labelled. Able to fail: the 366-string Java differential (`.ufo/waves/round-17/w2/predict-java-diff/`) showed 27 disagreements before and 0 after |
| landing — bytecode written into frozen dirs | `.ufo/waves/round-16/__pycache__/` (10:32 and again 11:08) and `.ufo/gates/citation-drift/__pycache__/`, written by imports under `python3 -I` without `-B` (w1 `CriticNoHarm`, w2 `CriticNoHarm2` F2). Gitignored, so Git-object controls could not see them | none | Removed. `predict.py`, `carrier-run.py`, `receipt-validate.py` and `retain.py` set `sys.dont_write_bytecode`; predict's selftest child uses `-B`; `verify.py` fails if any `__pycache__` exists under `.ufo`. Able to fail: `python3 -I` import of `selection.py` without the guard recreates it |
| vacuous — non-discriminating compare field | The `snapshot_label` request echo (`GoRttiMapper.java:179-180`) matches on exact and fallback runs alike (w1 `CriticC2Novelty` V1) | none | `snapshot_route`/`fallback_to` are read from the `GoApiSnapshot` component, and a hand prediction's `extra_expectations` are compared. Able to fail: verification labels `compare-route-red` (forced `info` → exit 1) and `compare-three-fields` (exit 0) |
| attribution — unbound and forgeable session logs | The w1 contract polled every new `/tmp/rea-ghidra-*` while a live REA MCP server and sibling lanes share `/tmp` (w1 `SentinelPollRace`). The first binding was substring-based with a 12-hex prefix (w2 `BindingFuzz` b04–b07) | none | Private `TMPDIR`, allowlisted environment, and binding by whole log records plus the loader's full `?MD5=`. Able to fail: `receipt-validate.py --selftest` red cases (foreign prefix, MD5 collision, stack-trace needles) |
| vacuous / survivor — validator green on the wrong shape | At `da64646`, `receipt-validate.py` rejected all 8 producer receipts with `unrecognized_shape` (list-vs-object `steps`), while its own selftest passed on a list fixture (w2, 17 seats independently) | none: neither selftest exercised the other tool's real output | Accepts the producer shape; its fixture now uses the producer's object shape; all 16 receipts were validated. Able to fail: the `da64646` validator on any `runs/*/receipt.json` → exit 1 |
| number-drift — unresolvable commit token | `2716747` in the knowledge entry and `run-carriers.sh:2` (w2, 9 seats). The real prefix is `2711674` | none | Both now carry the full hash. Able to fail: `git rev-parse --verify 2716747^{commit}` → fatal |
| vacuous — R16-PROVENANCE recurring inside round 17 | The `da64646` knowledge entry and lesson said "pins equal pre/mid/post" and "no mid-run check differed", but first-pass receipts kept only pre/post maps; mid checks were recorded only on drift (w2 `CriticC1Admission` F1 and 6 more seats) | QUALITY #18 (did not catch it); #19 now does | Every mid-run check is retained with its instant (second pass: 2–8 per run, all equal); the entry states identical bytes at those instants only; `receipt-validate.py` fails on recorded drift. Able to fail: `carrier_mid_run_drift_red` |
| provider — dispatch refusals and dead seats | `wave1-dispatch-attempts.json`: two whole-wave refusals at the host background-job cap (L1-observed text "Background job limit reached (100)"), then 78 spawned on attempt 3. W2: `PinsAttack` and `TemporalSweepAttack` died on an m_swe free-tier rate limit (`resource_exhausted`) | host, not a lane gate | The same payload was retried every 180 s and never split. Dead seats stay dead; the L1 covered their targets with the mutation-tester reports and its own selftest additions |
| scope — routed site list | `round-16-verifier-spotcheck.md:183` names SCORECARD (0 matching lines at `b563c79`) and omits the knowledge entry | the outside closure's route, against this lane's search | Sites are found by search at the pinned baseline, not copied from a prose list. No SCORECARD correction is invented |

### R16-PROVENANCE named corrections (append-only; filed bytes unchanged)

- R16-PROVENANCE: `LOG.md:2012` map matches committed source-revision blobs; temporal stability not evidenced.
- R16-PROVENANCE: `corpus/lessons/round-16.md:154` map matches committed source-revision blobs; temporal stability not evidenced.
- R16-PROVENANCE: `.ufo/waves/round-16/verification.json:419` map matches committed source-revision blobs; temporal stability not evidenced.
- R16-PROVENANCE: `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` map matches committed source-revision blobs; temporal stability not evidenced.
- The fleet report site `.ufo/reports/round-16/kaidoku.md:60` is outside this lane. Its correction is carried by this round's fleet report.

### In-round revisions (all added this round, revised before round close after w2)

- Knowledge entry:
  - The frozen hash was corrected.
  - The mid-run statement now cites retained second-pass checks.
  - The recheck command is non-destructive.
  - Evidence-ID locations were corrected.
  - The decision table now covers normalization, the request echo, invalid versions and the component that reports the failure.
  - The aether cause was raised from UNKNOWN to a labelled INFERENCE; S032 is a lead.
  - The op inference was corrected using r4-10's recorded go1.26.8.
  - The prospective accounting was split three plus three.
  - S024/S025/S026/S029/S031 are now used in the body.
- SOURCES rows:
  - S024 anchor gained `searchMagic`/`errNotGoExe`.
  - S026 `teaches` rephrased: the token records a link-time experiment configuration.
  - S027 "chosen" changed to "proposed".
  - S028 tier changed C→A (official docs) and its flip was scoped to 1.27+.
  - S029 gained the master HEAD and file sha256.
  - S031 and S032 were added.
- QUALITY #19: reworded so that only "identical bytes at the named instants" is admitted (w2 `CriticC1Admission` F7). #20: the `why` cell now cites Mistakes rows 6–7, and `supersedes` dropped #9 (w2 `ReviewQuality1920`).
- Tools: every change after `da64646` is listed in the as-built section of `contract.md` and in the LOG measured entry. The first-pass receipts at `da64646` were produced by the pre-hardening `carrier-run.py`. The second pass started at `95e34db`. During it, `carrier-run.py` gained a bytecode guard and a group stop and exit on timeout; both paths stayed unexercised because no run timed out. The binding check was then made MD5-anchored and line-anchored. All 16 receipts pass the final validator (verification pass).

## Integration boundaries

The initial lane state was clean at `b563c799d97774aae4351276fe43cb897311e349`.
The bounded watchdog search for `lane-dead-no-report kaidoku round=17`
returned nothing (exit 1). There are no inherited leftovers. The prior outside
verifier files are unchanged. No `corpus/lessons/operator-*` file exists. The
L1 holds the canonical planner seat. W1 had 78 seats, all completed. W2 had 69
seats: 67 completed and 2 died on a provider rate limit. The pilot
(10:17–10:19) is calibration only. It ran before `claims.json` was written and
before the predictions were frozen.

Tool installs/updates: none by the L1. Seat `DraftSourcesRows` (w1) installed
Go 1.27.3 linux/amd64 from the official go.dev tarball into
`~/.local/opt/go-1.27.3`, not on PATH; its sha256 matched
`go.dev/dl/?mode=json`. The verification pass uses that toolchain's
`go version -m`, which reads files only. Seat `ScoutReaLogKnob` (w2)
materialized `rea-agents@6.7.0` for read-only inspection. No pacman
transaction was run.
