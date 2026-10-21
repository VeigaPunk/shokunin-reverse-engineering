# Round 20 — routed round-19 defects, first-held static tool verbs, first-failure Go forecasts

author: kaidoku-shokunin; 2026-10-20
scope: discharge the six defects routed by `corpus/lessons/round-19-verifier-spotcheck.md:178-190` (D1-D6, eleven items);
admit knowledge for REA CLI verbs the corpus did not hold; replace the round-18/19 whole-walk emulator forecast with a
masked-variadic first-failure forecast frozen before held-out go1.24.6 toolchain runs. Claims: `.ufo/waves/round-20/claims.json`
(declaration `d1d981d2cc041dda4656c5b01d2c8445d8d17124`); freeze `808cbb31a1e24656da5ba4967497e602fbca7415`.

## Claims

- C1 calibration (tied-lowest owned axis, 10.0): eleven routed items closed by named `- R19-<ITEM>:` corrections plus
  substance checks in `.ufo/waves/round-20/tools/routed-r19.py`; census `c1-census-v10.py` FAIL/1 → PASS/0 at the delivered
  tip; QUALITY #23-#25.
- C2 coverage (sourced: S041-S046, S040): first-held `inspect-wasm-artifact`, `compare-wasm-interfaces`,
  `execute-rizin-command`, `list-objdump-architectures`, `project-harmony-application-graph`
  (`.ufo/waves/round-20/tools/verb-coverage.py`).
- C3 depth (sourced: S047 carrier provenance; S003/S023/S035 mechanism as round 19): `tools/swiss-misread-v2.py`
  first-failure forecasts for 19 go1.24.6 toolchain ELFs, frozen and pushed at `808cbb3` before the first analyze.

## Gate

### Candidate decisions (author-side; outside sampling is the closure's duty)

| Candidate | Decision | Evidence and limits |
|---|---|---|
| Knowledge `2026-10-20-r20-wasm-interfaces` | admit | Four shipped modules + three compare pairs retained under `evidence/c2/wasm-*`; the only `changed` verdict comes from a recipe-retained synthetic pair (QUALITY #12); no same-module version pair exists on the host |
| Knowledge `2026-10-20-r20-rizin-command-observation` | admit | ELF (jq, libjq) and PE legs retained; shell-capable surface stated; a seat's unretained claim that `;` does not chain is rejected against the retained `06-semicolon-chain` record |
| Knowledge `2026-10-20-r20-objdump-architecture-list` | admit, narrowly | `list-objdump-architectures` has `subject: null` by construction; its output equals host `objdump -i`; the subject-bearing companion run is `inspect-with-objdump disassemble` on jq |
| Knowledge `2026-10-20-r20-harmony-application-graph` | admit, narrowly | Synthetic Stage/FA HAPs only (recipe retained); the projection's Stage/FA hint is a path test (`harmonyApplication.js:110-117`); no real HarmonyOS package, signing or runtime |
| `pe-surface` erratum (rizin/radare2 absent) | admit as appended erratum | 2026-10-13 sweep is stale; re-run 2026-10-20 resolves all six tools; original text kept |
| QUALITY #23 / #24 / #25 | admit | grounded below (Mistakes 1-2, D3, Mistake 4) |
| Census re-key as DATED for SCORECARD 2374-2382 and SKILL 511-519 | admit | round-17 capability/registry records; flipping them CURRENT fails ambiguous=2 (wave-1 `ReviewCensusGate.md`); DATED shelter of a future planted pin inside those rows is a declared residual (wave-1 `CriticCensusRekey.md`) |
| `final-census.py` as a separate tool | admit | wave-1 `SimplifyC1Tools.md` proposed merging into verify.py; kept separate because routed-r19 D5 checks its record shape and the record must be the last lane write |
| bwrap-based revexec | reject for this round | contract claimed bwrap absent (false, Mistake 3); the systemd-run sandbox was built and passes its selftest; bwrap port left as an option |
| go1.27.3 toolchain as C3 carriers | reject | Ghidra 12.1.4 has no go1.27 snapshot → bootstrap failure, not a map-path test (wave-1 `ScoutGo1273Exposure.md`) |
| `link` as a C3 carrier | exclude before freeze | v2 emulator exit 2 (first-hit decoy build-info magic); recorded in `predictions/decision-rule.json` `excluded` |
| Retro v2 8/8 on round-19 logs as prediction evidence | reject | outcomes were public before v2 existed (wave-1 `CriticC3.md`, `SimplifyC3Pipeline.md`); retained only as a consistency check (`evidence/retro-v2/`) |

### Opened sources and located quotes (access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S040 | installed `rea-agents@6.5.0` `dist/domain/harmony/harmonyApplication.js:111` | `const stage = manifests.some(({ path }) => /(?:^|\/)module\.json$/iu.test(path));` |
| S041 | https://github.com/WebAssembly/wabt/releases/tag/1.0.42, release body `What's Changed` | "Bump version to 1.0.42 by @sbc100 in https://github.com/WebAssembly/wabt/pull/2859" |
| S042 | https://webassembly.github.io/spec/core/binary/modules.html, Indices (reST `modules.rst:48`) | "External indices are encoded by a distiguishing byte followed by an encoding of their respective value." |
| S043 | https://github.com/rizinorg/rizin/tree/v0.8.2 `librz/main/rizin.c:128` | "Do not load user settings and scripts" |
| S044 | https://book.rizin.re/ §7 Shell Command-line Options, `-q` line | "Quiet mode (no prompt) and quit after -i and -c" |
| S045 | https://sourceware.org/binutils/docs/binutils/objdump.html, `-i`/`--info` | "Display a list showing all architectures and object formats available for specification with -b or -m." |
| S046 | https://gitee.com/openharmony/docs, `application-configuration-file-overview-stage.md:12` | "there are two types of configuration files: one app.json5 file and one or more module.json5 files" |
| S047 | https://go.dev/dl/?mode=json&include=all, go1.24.6 entry, line 19268 | "sha256": "bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712", |

Quote sources: wave-1 seat reports `SourceWabtRelease.md`, `SourceWasmSpec.md`, `SourceRizinDocs.md`, `SourceObjdumpDocs.md`,
`SourceHarmonyDocs.md`, `SourceGo1246.md`, `HarmonyLeg.md`; S040 re-read by the L1 (`sed -n 110,117p`).

### Registry changes (old → new)

- New rows S040-S047 (rows 39 → 47). S040 was proposed by seat HarmonyLeg as kind `tool`; integrated as kind `code`
  (installed compiled source) before its first commit. All eight rows `mined`. No existing row's status/recheck/used-by cell
  changed. Paths: one appended study sequence; Search log: two round-20 notes (Harmony projection; static tool sources).
- Census W04 for S047 (same go.dev index URL as S038, distinct scope) is expected, like the carried S033 W04.

### Outside spot-check

Pending: the hyaku closure session (non-author) samples this round's admits and rejects. Not self-attested.

## R19 routed defects — named corrections (append-only; filed bytes unchanged)

- R19-D1: `.ufo/gates/custody-pair/custody-pair.py selftest` now refuses a scratch inside any Git worktree (exit 2,
  `scratch_inside_worktree`) and removes its selftest dir in `finally`; the two untracked nested repos were recorded
  (`.ufo/waves/round-20/evidence/d1-residue-before.txt`) and removed; round-20 `verify.py` uses mkdtemp scratch outside the lane.
- R19-D2: `.ufo/waves/round-20/tools/evidence-timestamps.py` compares every zoned timestamp with its line's introducing
  committer time; at baseline it flags round-19 `claims.json:36` (+643 s) and the never-routed round-18 `claims.json:35` (+65 s).
  Filed bytes are not rewritten; the round-20 wave tree must be clean under `--strict`.
- R19-D3: `.ufo/waves/round-20/tools/carrier-guard.py` arm/check/disarm; exec bits of all go-1.24.6 (20), go-1.25.0 (9)
  and go-1.27.3 (10) toolchain ELFs cleared during the round; per-label checks before each run; QUALITY #24 states the bypasses.
- R19-D4: `c1-census-v10.py` declares SCORECARD 2374-2382 and SKILL 511-519 (stable text anchors) as DATED round-17 records.
- R19-D5: `.ufo/waves/round-20/tools/final-census.py` records the final census at the delivered tip in `verify/final-census.json`.
- R19-D6a: `head-rev-lint.py` reports `nested` HEAD reads (round-17 `verify.py:83`, round-18 `revpin.py:113`).
- R19-D6b: `.ufo/waves/round-20/tools/revexec.py` runs revision-extracted Python in a `systemd-run --user` unit with
  `PrivateNetwork=yes` and a read-only view except the work dir; routed-r19 executes REV tools through it.
- R19-D6c: `citation-drift-probe.py` refuses unsafe `@<slug>` snapshot targets (`slug_unsafe`, realpath containment).
- R19-D6d: `receipt-validate.py` authenticates an analyze step only by `analyze` directly after the `rea-agents@<v>` token.
- R19-D6e: `wave-outcomes.py` no longer confuses a seat named `causes` with the wrapper key.
- R19-D6f: `jj-red-before.py` selftest gains `jj_relative_traversal_refused` and `jj_tmpdir_scrubbed` (9 → 11 cases).

## Installs

- WABT 1.0.42 linux-x64: official GitHub release asset `wabt-1.0.42-linux-x64.tar.gz`, sha256
  `84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131` (verified against the release `.sha256` asset with
  `sha256sum -c`), 4761911 bytes, extracted to `/home/vgpnk/.local/opt/wabt-1.0.42` (not on PATH) by the L1 at
  2026-10-20T17:31:52-03:00. Reason: REA 6.5.0 `inspect-wasm-artifact` requires WABT exactly 1.0.42 via
  `REA_WABT_BIN_DIRECTORY`. Channel: official release binary (pacman paused host-wide).
- Mode changes (not installs): exec bits cleared on the go-1.24.6, go-1.25.0 and go-1.27.3 toolchain ELFs for the round
  (`evidence/carrier-guard*/arm.json`); restored at round end (`disarm.json`).

## Mistakes

| # | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| 1 | scope | R19-D1: round-19 `verify.py:537-539` passed a lane path as custody-pair selftest scratch; two nested fixture repos stayed untracked (`round-19-verifier-spotcheck.md:29,33-35`; `.ufo/waves/round-20/evidence/d1-residue-before.txt`) | none | custody-pair refuses in-worktree scratch (exit 2) and cleans up; baseline tool left 136 files / 2 nested `.git` under an outside scratch (wave-1 `ScoutLaneScratchWriters.md`, `CustodySelftestFix.md`); patched tool leaves 0 entries; routed-r19 D1 red at baseline |
| 2 | number-drift | R19-D2 and a second, never-routed instance: round-18 `claims.json:35` asserts 13:25:00-03:00 in commit `eb6c266` committed 13:23:55 (+65 s), disclosed in `round-18.md` but not caught by the round-19 check | PROTOCOL §Evidence standard (prose only) | `evidence-timestamps.py --strict` exit 1 at baseline over round-18 and round-19 (two findings, wave-1 `ScoutTimestampOracle.md` independent oracle agrees: 2 of 2280 zoned timestamps); QUALITY #23 |
| 3 | stale-premise (this round) | `contract.md` §Interfaces D6b said "bwrap is NOT installed"; `/usr/bin/bwrap` 0.13.1 exists (wave-1 `ScoutSandboxPrimitives.md`, `ConnSandboxPatterns.md`, `SentinelRevexec.md`). Cause: the L1's `which bwrap` ran in a persistent shell left in `set -e` by the WABT install command, so the probe aborted silently | none | **no demonstrated fix**; revexec was built on systemd-run and passes its own selftest, so no claim depends on the false clause. Practice: never leave `set -e` in the persistent shell; a presence claim needs a printed probe result |
| 4 | vacuous (this round) | C2 `exercised` predicate accepted any `ev_`+64-hex string plus any existing evidence path in the same entry (wave-1 `CriticC2.md`, `ReviewClaimsC2.md`) | none | `verb-coverage.py` `bound_evidence`: the id must occur inside a retained file under `evidence/c2/` whose bytes carry the verb's operation token and no refusal code; new selftest case `forged_id_not_in_retained_bytes`; the pre-fix fixture case went red under the new predicate (`SELFTEST: FAILED evidence_id_and_existing_path_exercise`) before the fixture was made honest; QUALITY #25 |
| 5 | reference-drift (this round) | `first-failure-extract.py` prints an envelope `{log_path, last_line, first_failure, …}`; `compare-first-failure.py` expected the bare object, so the L1's first retro run returned `unevaluable` exit 2 for all 8 labels | none (both selftests used their own stub shapes, wave-1 `SimplifyC3Pipeline.md`) | comparator unwraps the envelope (before the freeze commit); retro then 8/8 `yes` (`evidence/retro-v2/retro-v2.csv`) |
| 6 | reference-drift (this round) | `run-carriers.sh` compare step passed `predictions/<label>.prediction.json`, whose `first_failure` holds the H1 object directly, to a comparator that requires `first_failure.h1`; every in-run compare exited 2 (`runs/*/compare.json`: "prediction: missing first_failure.h1") | none | compare re-run after the runs with the unchanged frozen comparator on the frozen emulator outputs `predictions/swiss-misread-v2/<label>.json`, whose `first_failure.h1` equals each prediction's `first_failure` for 19/19 labels (checked before re-running); both records retained |
| 7 | landing (this round) | seat HeadRevNested's patch file embedded a read-tool truncation banner (`git apply`: corrupt patch at line 302) | none | patch regenerated from the seat's clone (`w1/patches/HeadRevNested-2.regenerated.patch`); selftest CLEAN 5 after apply |
| 8 | scope (this round) | seats wrote overlapping `corpus/SOURCES.md`/`README.md` edits and both proposed id S040 (HarmonyLeg, RizinPeLeg) | contract `Writers` (patches) — not specific about shared registry files | L1 integrated SOURCES/README itself; RizinPeLeg applied with `--exclude` for those two files; README insertion that would shift pinned Frontier coordinates (`:175`, `:180`) was replaced by a row on a former blank line |
| 9 | reference-drift (this round; found by the recovery coordinator) | routed-r19 `_s_d5` required `argv` as a flat string list and read the census stdout at the record's named rev, while `final-census.py` writes `argv` as a list of argv lists and the stdout lands only in the record commit; `_s_d3` demanded a fresh armed `check` even after the round's required disarm | none (each tool's selftest used its own fixture shape) | `_s_d5` accepts argv lists and reads stdout at REV; `_s_d3` accepts a disarm record later than every retained check. Red/green on one fixture commit (clone of `5c0b46c` + a real final-census record commit): the 7a1e0df counter blob reports D3 `no exit-0 check record…` and D5 `argv is absent or malformed` (exit 1), the fixed counter closes both (exit 0) — `.ufo/waves/round-20/verify/recovery/d3-d5-redgreen.txt` |
| 10 | environment (this round) | revexec's sandbox made host `/tmp` read-only and HOME empty, so revision tools that hard-code `/tmp` (round-18 `jj-red-before.py`), refuse `/tmp` scratch (custody-pair, EDQUOT rule) or read client anchors under HOME (census) failed under the patched counter although their fixes existed: at `aad0869` D1 `outside-workdir selftest exit 1`, D4 `ANCHOR-FAIL`, D6f `Read-only file system at /tmp/…` (`.ufo/waves/round-20/w1/RoutedR19Tool.md` `## Integration fix`, item lines) | none | revexec work base moved to `/fast/scratch` (refused under /tmp or /var/tmp), `PrivateTmp=yes`, opt-in `--host-home` (read-only) used only for the live census; new selftest cases `private_tmp`, `host_home_passthrough`; at `81c2021` D1/D4/D6f substance true (`verify/recovery/routed-81c2021-live-strict.json`; the unpatched-counter measurement at `7a1e0df` is `verify/recovery/routed-7a1e0df-live-strict.json`) |
| 11 | landing (this round) | attempt 1's coordinator stopped at 18:45 -03 after provider 429/quota/cyber-flag errors, before the SCORECARD/LOG rows, wave 2 and report; its last integration fix (`w1/patches/RoutedR19Fix.patch`) and the C3 entry survived only in checkpoint commits `aa78b0d`/`7a1e0df` marked "admission pending" | watchdog `lane-dead-no-report kaidoku round=20` (`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:544`) | recovery coordinator re-ran every counter before reuse (`## Recovery attempt 2`); practice: land SCORECARD/LOG claim rows right after integration so a dead coordinator leaves named state, not only checkpoints. No demonstrated gate fix |

Misroot sweep: run before the report (see the fleet report).

## Open

- DATED shelter (census): a live pin planted inside a DATED range reads historical (wave-1 `CriticCensusRekey.md`); scope-diff's
  "to EOF" flag is unimplemented and same-line "(historical)" laundering lowers counts (wave-1 `ReviewCensusGate.md` F1/F2).
- Carrier guard: mode bits stop direct `execve` only; copy+exec, memfd+`fexecve`, in-process loaders and same-owner chmod
  between instants are not prevented or detected (wave-1 `CriticGuardSufficiency.md`, `ScoutCarrierExecPaths.md`).
- revexec: same uid, AF_UNIX sockets (`/run/systemd/resolve`, user bus, docker) remain reachable (wave-1
  `ScoutSandboxPrimitives.md`); not a security boundary.
- Adjacency: revenger-shokunin's PROVINCE still claims the REA toolset while its own routing assigns the live surface to
  kaidoku (wave-1 `ConnSiblingRizin.md`); reported, not absorbed; no L0 line.

## C3 measured outcome (author-side)

Freeze `808cbb31a1e24656da5ba4967497e602fbca7415` (committer 18:01:54 -03, helper `landed` before the runner); runs
18:02:05–18:17:55 -03, 19 labels, carrier guard checked clean before each. First-failure comparison (frozen comparator and
extractor bytes, frozen emulator outputs): **19/19 match** — 8 exact predicted `Invalid index` values, 11 silent.
objdump's REA analyze ended `execution_failure` (Java heap OOM after the Go failure); receipts 19/19 valid under
`--require-mid-maps`. Entry: `corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md`. The retro 8/8 on round-19
go1.25.0 logs is a consistency check, not prediction evidence.

## Registry used-by appends (R20-USEDBY-APPEND, old → new)

For S003, S023 and S035 the `used-by` cell at `14f0260ad319ecc26994381b2415d5a999003375` is a byte prefix of the new cell;
the only change is the appended suffix `, corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md`
(old cells end `…, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`). S040 (new this round) gained
`corpus/lessons/round-20.md` before its first commit; S047 (new) gained the C3 entry. No status or recheck cell changed.

## Recovery attempt 2 (operator-authorized recovery coordinator, 2026-10-21)

Attempt 1 (coordinator `KaidokuR20`) dispatched W1 once (100 spawn seats after one job-cap refusal that spawned none,
`.ufo/waves/round-20/wave1-dispatch-attempts.json`; members and agent ids in `wave1-registry.json`; `w1/swarm-registry.json`
is the validator's pre-record copy with 0 assigned). Role mix: executor 28, scout 22, reviewer 16, scribe 10, connector 8,
critic 8, revenger 4, sentinel 2, simplifier 2. Reports: 98 under `w1/`; ConnSiblingHarmony and ConnJjSelftests have no
report: each transcript's only assistant message stopped `aborted` ("Request was aborted", 17:46:51 -03) and the
session ended `session_exit` reason `dispose` at 18:29:58 -03 with a pending `bash` call (no 429 text). RoutedR19Fix
is not a separate seat: it is a resumed RoutedR19Tool-2 turn (same identity). Attempt-1 seats count toward the round total;
none was respawned.

Reused after re-verification (each re-run by the recovery coordinator, not trusted from text):
- landed commits `d1d981d`…`aad0869` (claims, freeze, integrations): C2 `verb-coverage.py` at B 128/153, 0/5 exercised →
  at `7a1e0df` 133/153, 5/5 bound; C3 `measure.py main --freeze 808cbb3` first_failure_bound 19, matched 19, receipts 19/19;
  census PASS at `81c2021` (via routed-r19 D4 archive run).
- checkpoint `aa78b0d`: `w1/patches/RoutedR19Fix.patch` applied unchanged (`git apply --check` clean) and extended
  (Mistakes 9-10); the C3 knowledge entry, SOURCES used-by appends and README row (re-read; challenged in W2).
- checkpoint `7a1e0df`: three >1 MiB generated Wasm seat patches retained as seat evidence only; no claim rests on them.

Discarded (not relied on): attempt-1 prose stating D1-D6f closed (replaced by the measured counter); the in-run
`runs/*/compare.json` records (Mistake 6; superseded by the retained re-run); the routed-r19 blob at `7a1e0df` (superseded).

Recovery commits: `81c2021` (RoutedR19Fix applied; revexec work base/private /tmp/host-home; D5 shape; SCORECARD/LOG rows),
`5c0b46c` (final guard checks and disarm of all three guards, modes restored to 0755; D3 disarm rule; W2 generator).

## Recovery attempt 3 — integration of 169 reports, 2026-10-21

Attempt 2 (coordinator `KaidokuR20Recovery`) ended on the Devin weekly quota before it filed a report; its own last commits are
`81c2021` and `5c0b46c`. Attempt 3 was dispatched under the operator-authorized failed-coordinator recovery, with **no new seat
spawned**: the round total stays 171 (wave 1: 100 spawned, 98 reports; wave 2: 71 spawned after two all-refused job-cap attempts,
71 reports). All 169 reports are integrated; the two reportless wave-1 seats carry retained causes in
`.ufo/waves/round-20/evidence/wave-outcomes/w1-causes.json` (both `session_exit` reason `dispose` at 2026-10-20T21:29:58Z, cancelled
after 50/25 requests with a pending tool call; raw transcript paths cited) and the wave-outcomes record reads
`seats=100 reports=98 missing=2 uncaused=0`, exit 0. W2 outcomes read `seats=71 reports=71 missing=0`, exit 0.

Reused after re-verification (not trusted from attempt-2 prose): the attempt-1 commits `d1d981d`…`aad0869`; the wave-1 reports and
retained C2/C3 evidence; the W2 reports; `verify/recovery/routed-{7a1e0df,81c2021}-live-strict.json` and `d3-d5-redgreen.txt`.
Discarded: attempt-2 text that treated D1–D6f as closed before the required final-census record existed; the in-run
`runs/*/compare.json` records (Mistake 6, superseded); the routed-r19 blob at `7a1e0df` (superseded by the fixed counter).

### Wave-2 integration — code and evidence changes

- `receipt-validate.py`: `_is_analyze_step` now requires `npx`, optional `-y/--yes`, then the pinned package operand and `analyze`;
  second-package and non-npx decoys are refused. Selftest gains `argv_second_package_decoy`, `argv_non_npx_decoy`,
  `argv_latest_refused` (w2 `AttackD6d.md`).
- `wave-outcomes.py`: wrapper detection disambiguates a registered seat named `causes` from a wrapper map by value shape; the old
  no-`wave` wrapper fixture is restored alongside `seat_named_causes` (w2 `AttackD6e.md`, `CriticNoHarmS.md`).
- `evidence-timestamps.py`: the text-size skip is removed (only binary blobs are skipped and reported); the timestamp grammar accepts
  compact `T±HHMM` and space+`Z`/offset forms. Selftest re-run in the final suite (w2 `AttackD2.md`).
- `routed-r19.py`: D5 requires the record's `rev` to be REV's single direct parent, the fixed stdout path, the exact two-command argv,
  `worktree_clean`, and both validators' success markers; D3 also accepts a disarm record later than every retained check and verifies
  restored modes; D6d's fixture records the npx form (w2 `AttackD5.md`, `AttackD3Disarm.md`).
- Evidence committed with this recovery: `w2/` (71 reports), `wave2-{assignments,registry,spec,dispatch,dispatch-attempts}.json`,
  `wave2-result-attempt{1,2,3}.txt`, `verify/recovery/`, `verify/receipt-validation/`, `evidence/wave-outcomes/`.
- Corrections: SOURCES **S048** (installed non-Harmony REA CLI/service source) and errata in the WASM, Rizin, objdump and Harmony
  entries; QUALITY corrections for #23–#25; SKILL registry rows split and completed; this lesson's corrections below.

### Corrections to this lesson's earlier claims

- **Mistake 1 (D1):** the strict-red counter output was not retained (w1 recorded the baseline counter *without* `--strict`, exit 0,
  `open_count=11`); the demonstrated red artifact is the residue sweep (136 files / two nested `.git` trees left by the baseline
  selftest). C1's counting command must carry `--live`; without it the counter can read closed while untracked residue remains.
- **Mistake 2 (D2):** the strict `exit 1` is not in the cited w1 report; the findings are (`claims.json:35` +65 s, `:36` +643 s) and the
  independent oracle agrees. The strict run is demonstrated by the final suite, not by the w1 text.
- **Mistake 4:** the quoted `SELFTEST: FAILED not_mentioned_is_zero,substring_trap_rejected,evidence_id_and_existing_path_exercise`
  output is the pre-fix *positive* fixture set, not `forged_id_not_in_retained_bytes`. The new anti-forgery case exists and passes, but
  no retained output shows it red before the predicate fix. The claim is the predicate change plus the passing case, not a retained
  red-before for that case.
- **C2 falsifier floor:** `claims.json` falsifies below three target verbs; the round measured 5/5. The claim is narrowed here to
  mention-level coverage (128→133/153) plus the five exercised targets; `list-objdump-architectures` is pathless (`subject: null`) and
  is not carrier-bound.
- **C3 model errors:** the naive "stop on any ReadError" emulator forecast 5/8; the masked-variadic v2 forecasts 8/8 (19/19 with the
  silent labels). The residual predicate/vacuity limits (continue-set, trail cleanup, empty-D refusal) are named in `## Open`.
- **Mistake 8** is a coordination incident (overlapping SOURCES/README edits), not a demonstrated test red-before.

## Mistakes — wave-2 additions (2026-10-21)

| # | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| 12 | acceptance without authentication | R19-D6d decoy: second package-looking token + `analyze` passed; non-npx `/usr/bin/true rea-agents@6.5.0 analyze` passed (w2 `AttackD6d.md`) | none (the D6d text required npx but the predicate scanned every index) | `_is_analyze_step` anchors npx+package+subcommand; three named selftest decoys (red before the change, green after) |
| 13 | fix regressed an accepted input | S's wave-outcomes required `wave` in a wrapper, so the previously accepted no-`wave` wrapper exited 2 `causes_unknown_seat` (w2 `CriticNoHarmS.md`) | QUALITY #16/#21 old-fixture retention, not enforced for tools | wrapper/seat disambiguation by registration membership; the old no-`wave` fixture restored beside `seat_named_causes` |
| 14 | closure without its witness | D5's final-census record absent at S; D5's old check accepted a non-parent record and any argv shape (w2 `CriticAdmitC1.md`, `AttackD5.md`) | the contract's D5 wording, not the counter | counter now binds parent/argv/markers; the final record commit is the last lane write (this recovery) |
| 15 | source mis-scope | S040 (Harmony) cited for WASM/Rizin/objdump implementations (w2 `EntryWasmClaims.md`, `EntryRizinClaims.md`, `EntryObjdumpClaims.md`) | SOURCES used-by/scope rule | S048 row + entry errata; S040 used-by unchanged |
| 16 | registry rows not gate-conformant | `final-census` as a gate with no map/pinned path; three tools merged in one row; `carrier-guard adopt` syntax wrong (w2 `ReviewSkillRowsR20.md`) | PROTOCOL §Gate standard | rows split/rewritten with per-tool verdict maps, pinned paths and correct `adopt --from` form |
| 17 | seat accounting without causes | two W1 seats had no retained cause record (w2 `ReviewWaveRecords.md`) | QUALITY #22 | `w1-causes.json` with transcript pointers + `w1-outcomes.json` exit 0 (`seats=100 reports=98 uncaused=0`) |

## Gate addendum — S048 quote (opened 2026-10-21)

| Row | URL / location | Accessed | Quote (location) |
|---|---|---|---|
| S048 | retained installed-source extract `.ufo/waves/round-20/evidence/c2/rizin-pe/rea-cli-source-notes.md:8` (package `rea-agents@6.5.0`, `dist/application/reverse/ReverseEngineeringService.js:150-168`) | 2026-10-21 (re-read) | "non-access-denied, non-timeout digest failures become `AnalysisInputError`" (source note line 8) |

## Claim bounds stated at integration

- **C1:** eleven routed items; 10 are substance-closed by the counter at the work tip; D5 closes by the final-census record commit
  (the record's `rev` is that commit's parent, and the counter verifies parent, argv, markers and the two-path tree diff). Final numbers
  are in the SCORECARD measured-record section and the fleet report.
- **C2:** mention-level 128/153 → 133/153; five targets `exercised` under the counter's ID/path/operation-token rule; pathless
  `list-objdump-architectures` is `subject: null` and not carrier-bound; Harmony is synthetic path-hint only.
- **C3:** 19/19 first-failure matches (8 exact `Invalid index`, 11 silent through the retained log end) for the 19 frozen go1.24.6
  toolchain ELFs. "Held out" means held out from prior Ghidra first-failure outcomes for these exact artifacts, not version-held-out;
  the R18 synthetic `22386945` result and the pprof candidate lead were known before the freeze. The comparator checks `kind` and
  `index` only; `t1246-link` was excluded; `t1246-objdump` ended on a later Java heap OOM.

### Residual limits accepted (not fixed this round)

C1/C3 share the receipt validator as a verification authority (claim separability attack, w2 `CriticSeparabilityS.md`); D6a's
duplicate-name nested-read limitation; D6b exposes a read-only host HOME (including `.ssh` names) under `--host-home`; QUALITY #23
still skips binary blobs; QUALITY #25 remains a token check; the census DATED shelter and same-line laundering; carrier-guard
loader-mapped execution; the C3 predicate/vacuity residuals; census W04 for S033/S047; S041/S045/S046 quotes are rendered text, and
S043's `-c` anchors (`rizin.c:111,586-588`) remain unadded; no real HarmonyOS package, device or runtime was exercised.

