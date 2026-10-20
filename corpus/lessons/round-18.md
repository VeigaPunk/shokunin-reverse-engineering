# Round 18 — routed r17 defects, jj-safe revision pins, Swiss-map replay

author: kaidoku-shokunin; 2026-10-20
scope: discharge the six defects routed by `corpus/lessons/round-17-verifier-spotcheck.md:137-147`; make the lane's live revision pins read the branch tip under jj (routed by `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md` §5); replay the round-17 aether INFERENCE on carriers the prediction was not calibrated on.

## Claims

- C1 calibration (tied-lowest owned axis at 10.0): R17-PINMAP, R17-VALIDATE16, R17-PRODUCER-REV, R17-SUMS-RUNLOG, R17-REGISTRY, R17-S032-DIGEST each closed by a named correction **and** a substance check (`.ufo/waves/round-18/tools/routed-defects.py`); QUALITY #21 from the one partial outside disagreement.
- C2 operability: the three live HEAD-keyed pins read `refs/heads/main` and refuse an off-branch HEAD (`head-rev-lint.py` live sites, `jj-red-before.py` sandbox receipt).
- C3 depth (the filed sourced claim, S034/S035, with S023/S003/S033): Ghidra 12.1.4's `OldMapType` binding for Go 1.24/1.25 Swiss named map types, predicted per carrier before any run and observed on 15 bound logs.

## Gate

### Candidate decisions (author-side; outside sampling remains the closure's duty)

| Candidate | Decision | Evidence and limits |
|---|---|---|
| Knowledge entry `2026-10-20-r18-swiss-map-replay` | admit | Predictions and decision rule committed at `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` (16:23:55Z) before the first run step (16:24:08Z); 15/15 compare exit 0; 15/15 `receipt-validate.py --require-mid-maps` exit 0; both held-out diagnostic carriers failed with the exact predicted index. One Ghidra release, one pass, x86-64 ELF |
| "named map types *with methods* trigger the misread" (the round's first design) | reject | Every named type has an uncommon block; the trigger is a Swiss named map whose `SlotSize` offset lands on a name with a pkgPath (w1 `CriticC3.md`, `RevNotesmdMaps.md`); methods/nomethods carriers were predicted and observed silent (8/8) |
| "aether's EOF is caused by the 1.25.14→1.25.0 patch fallback" | reject (re-confirmed) | s1246-swiss-nethttp fails on an exact-diff INFO route (no fallback) |
| "Go 1.25.0 Swiss carriers are safe" | reject | s1250-swiss-nethttp is silent only because the name at `types+40` has no pkgPath; the misread itself is present (H1 `PkgPath`=40, `Mcount`=0) |
| "aether's failure is on the map path" | reject as stated | The retained stack runs through struct/interface markup to the same GoName (w1 `RevGhidraMapTypeRead.md`); the map path is a second route to it (w1 `RevAetherReplay.md`). The entry says so |
| QUALITY #21 (retention claims name retained keys; verdict ≠ object) | admit | Grounded in R17-PINMAP (`round-17-verifier-spotcheck.md:108,137`) and Mistakes row 1; red-before below |
| SOURCES S033 (supersedes S032), S034, S035, S036 | admit (mined) | Opened 2026-10-20; quotes below |
| go1.25 release notes as a Swiss source | reject (no row) | 0 `swiss`/`noswissmap` matches; S031 already registers the page |
| jj `latest` docs as the S036 anchor | reject | Unversioned (0.46 content); the v0.45.1 tag file is the anchor |
| C2 baseline "3" as declared before the lint existed | reject as declared; admit as measured | The number came from the audit's prose (`JjAuditKaidoku.md` §5); critics showed the contract's first rule gives 8 (w1 `CriticC2.md`, `ConnSiblingOverlap.md`). The amended rule, written before measuring, yields 3 live / 8 fixture / 10 excluded files at `9011581` |
| C1 counter as first specified (token checks) | reject | A token-only commit closed all six (w1 `CriticC1.md`); the shipped tool requires substance checks and its selftest keeps token-only fixtures open |

### Opened sources and located quotes (access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S033 | https://github.com/NationalSecurityAgency/ghidra/pull/9348, `<title>` | Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries |
| S034 | https://go.dev/doc/go1.24, `<h2 id="runtime">`, raw lines 571-573 | The new builtin map implementation and new runtime-internal mutex may be disabled by setting GOEXPERIMENT=noswissmap and GOEXPERIMENT=nospinbitmutex at build time respectively. |
| S035 | go1.25.0 `src/internal/abi/map_select_swiss.go:22` | type mapType = SwissMapType |
| S035 | go1.25.0 `src/internal/abi/type.go:358-361` | case Map: type u struct { mapType u UncommonType } |
| S036 | https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md, lines 114-116 | `jj` commands will usually put the Git repo in a "detached HEAD" state, since in `jj` there is not concept of a "currently tracked branch". |

### Registry changes (old → new)

- S032 `status` mined → mined, `used-by` unchanged: kept as the superseded row; S033's teaches opens `supersedes S032 —`. No in-place S001–S032 cell changed.
- New rows S033–S036 (3 tier A, 1 tier B community). Rows 32 → 36.

### Outside spot-check

Pending: the hyaku closure session (non-author) samples this round's admits and rejects. Not self-attested.

## R17 routed defects — named corrections (append-only; filed bytes unchanged)

- R17-PINMAP: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32` and `SCORECARD.md:2374` — mid-run instants retain the comparator verdict against the retained pre map, not the map (29/29 second-pass checks); corrections appended to the entry and to SCORECARD round 18. Also `corpus/lessons/round-17.md:90` ("the entry states identical bytes at those instants only") inherits the same overstatement (w1 `ScoutPinmapSites.md`).
- R17-VALIDATE16: `SCORECARD.md:2364` and `corpus/lessons/round-17.md:88,122` ("all 16") — 8 validations were retained in `verification.json`; the 8 first-pass receipts at `da64646` now validate 8/8 exit 0 under the `9011581` validator via a path-prefix-remapped copy (`.ufo/waves/round-18/evidence/validate16/summary.json`); an in-place replay is red 8/8 because pass 2 replaced the logs at the same paths (w1 `RevValidatorPaths.md`).
- R17-PRODUCER-REV: pass 1 produced by `271167473d87ef710f07ecdd98caf0ce12091686`, pass 2 by `95e34db62f2693c455d7ee4dfef24b8f3ebc007d`; `d0ab299` is the verification revision (w1 `RevProducerRev.md`). Round-18 runs record `producer.json` (branch tip + tool digests).
- R17-SUMS-RUNLOG: the `carriers.tsv` line dropped at `95e34db` is restored byte-exact in `.ufo/waves/round-17/predictions/SHA256SUMS` (the one in-place edit to round-17 evidence; `controls.py` permits exactly it); the `da64646` pass-1 `run-log.txt` lists 7/8 carriers (calib-shfmt missing; its receipt exists, `.ufo/waves/round-18/evidence/sums-runlog.json`); the retained pass-2 log is 8/8.
- R17-REGISTRY: `SKILL.md` rows go-route-compare, receipt-validate, pins, go-buildinfo-probe carry pinned values and write scope; citation-drift is `gate`; pins kind `tool` → `probe`.
- R17-S032-DIGEST: S033 anchors on title, state, head `a214355…` and a byte-stable `.patch` digest; page digests are fetch-time only (three L1 fetches, three digests, `.ufo/waves/round-18/evidence/s032-digests.json`).

## Mistakes

| # | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| 1 | vacuous | R17-PINMAP: r17 entry said each mid-run pin map was retained; receipts kept a verdict (`round-17-verifier-spotcheck.md:108,137`); `carrier-run.py:475` even tagged "(QUALITY #19)" | QUALITY #19 by text; not applied (the tag was self-attestation) | QUALITY #21; `carrier-run.py` writes `pins/mid-<n>.json` + `map_sha256`; `receipt-validate.py --require-mid-maps` exits 1 `mid_map_missing` on all 8 r17 receipts (red) and 0 on all 15 r18 receipts (green); forged `entries` → `mid_entries_mismatch` (selftest) |
| 2 | number-drift | R17-VALIDATE16: "all 16 receipts validated" vs 8 retained runs | QUALITY #18 | remapped validation 8/8 retained; `routed-defects.py` substance check derives k/8 from the summary (red at `9011581`) |
| 3 | attribution | R17-PRODUCER-REV: second-pass receipts cited under the verification revision | QUALITY #18 | per-run `producer.json`; routed-defects checks both producer hashes are ancestors (red at `9011581`: no line names them) |
| 4 | landing | R17-SUMS-RUNLOG: frozen manifest lost a line when a file was added | none | restored line; routed-defects compares every `2711674` manifest line byte-exact (red at `9011581`) |
| 5 | reference-drift | R17-REGISTRY and R17-S032-DIGEST | none (PROTOCOL row fields) / QUALITY #4 | rows fixed; routed-defects requires a non-empty write scope with resolvable paths, and a 40-hex head plus ≥2 recorded page digests (red at `9011581`) |
| 6 | vacuous (this round) | C1 counter as first contracted: substring checks closable by tokens (w1 `CriticC1.md`, scratch token-only commit closed 6/6) | none | substance checks; selftest has six token-only fixtures that stay open (`routed-defects.py --selftest` CLEAN 17) |
| 7 | number-drift (this round) | C2 "3 → 0" declared in `claims.json` before the lint existed, copied from audit prose; the first contracted rule gives 8 (w1 `CriticC2.md`) | CORPUS "a count carries its command" | amended scope rule written before measuring; baseline is the tool's output (3 live, 8 fixture, excluded files listed), never typed by hand |
| 8 | stale-premise (this round) | C3 first design (methods vs nomethods) predicted non-diagnostic by three seats before any run | none | nethttp carriers and a real carrier added; diagnostic set D and the verdict rule frozen with the predictions (`predictions/decision-rule.json`) |

Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` at wave-1 close found no untracked file naming kaidoku or round-18 (w1 `ScoutMisrootFleet.md`); re-run before the report.

## Open (routed earlier, still open)

- Round-12 routed items (w1 `ScoutOperatorLessons.md`): the r12 C1 entry `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` has no `S###` row and no custody-leg disclosure. Not discharged this round; carried.
