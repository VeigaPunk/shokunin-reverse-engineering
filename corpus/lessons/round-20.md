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
