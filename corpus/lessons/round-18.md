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
| Knowledge entry `2026-10-20-r18-swiss-map-replay` | admit | Predictions and decision rule committed at `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` (16:23:55Z, pushed 16:23:57Z) before the first run step (16:24:07Z); 15/15 compare exit 0; 15/15 `receipt-validate.py --require-mid-maps` exit 0; both held-out diagnostic carriers (both Go 1.24.x) failed with the exact predicted index. One Ghidra release, one pass, x86-64 ELF; the Go 1.25 half rests on the calibration carrier |
| "named map types *with methods* trigger the misread" (the round's first design) | reject | Every named type has an uncommon block; the trigger is a Swiss named map whose `SlotSize` offset lands on a name with a pkgPath (w1 `CriticC3.md`, `RevNotesmdMaps.md`); methods/nomethods carriers were predicted and observed silent (8/8) |
| "aether's EOF is caused by the 1.25.14→1.25.0 patch fallback" | reject (re-confirmed) | s1246-swiss-nethttp fails on an exact-diff INFO route (no fallback) |
| "Go 1.25.0 Swiss carriers are safe" | reject | s1250-swiss-nethttp is silent only because the name at `types+40` has no pkgPath; the misread itself is present (H1 `PkgPath`=40, `Mcount`=0) |
| "aether's failure is on the map path" | admit (revised after w2 `AetherDualPath.md`; wave 1 had rejected it) | The retained stack's innermost frames are `GoType.getUncommonType` → `GoUncommonType.getPkgPath` on GoName `0x954048`, reached through address-ordered container markup (struct/interface frames); w1 `RevGhidraMapTypeRead.md` read the outer frames as a second route. The map type's identity (`http.Header`) is a byte-decode INFERENCE |
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
| S035 | go1.25.0 `src/internal/abi/type.go:358-362` | case Map: type u struct { mapType u UncommonType } |
| S036 | https://raw.githubusercontent.com/jj-vcs/jj/v0.45.1/docs/git-compatibility.md, lines 114-116 | `jj` commands will usually put the Git repo in a "detached HEAD" state, since in `jj` there is not concept of a "currently tracked branch". |

### Registry changes (old → new)

- S032 `status` mined → mined, `used-by` unchanged: kept as the superseded row; S033's teaches opens `supersedes S032 —`. No in-place S001–S032 evidence cell changed.
- New rows S033–S036 (3 tier A, 1 tier B community). Rows 32 → 36.
- `used-by` old → new (wave-2 integration, w2 `UsedByResolve.md`): S003 `…, corpus/lessons/round-17.md` → `…, corpus/lessons/round-17.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`; S023 `…, corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` → `…, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` appended; S033 `corpus/lessons/round-18.md` → `corpus/lessons/round-18.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`.
- S034 revised in-round before closure (w2 `ReopenS034.md` F1): its teaches cell said "not from the Go release number", which is wrong (a default Swiss build records no marker); the scope now says "no Go 1.25 map claim" and the anchor adds raw lines 567-568.
- Census at round end: `sources-census.sh validate` exits 0 with one warning, `W04 S033 duplicate url … across scopes` — the expected result of a superseding row with a narrower scope (w2 `CensusRerun.md`).

### Outside spot-check

Pending: the hyaku closure session (non-author) samples this round's admits and rejects. Not self-attested.

## R17 routed defects — named corrections (append-only; filed bytes unchanged)

- R17-PINMAP: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32` and `SCORECARD.md:2374` — mid-run instants retain the comparator verdict against the retained pre map, not the map (29/29 second-pass checks); corrections appended to the entry and to SCORECARD round 18. Also `corpus/lessons/round-17.md:90` ("the entry states identical bytes at those instants only") inherits the same overstatement (w1 `ScoutPinmapSites.md`).
- R17-VALIDATE16: `SCORECARD.md:2364` and `corpus/lessons/round-17.md:88,122` ("all 16") — 8 validations were retained in `verification.json`; the 8 first-pass receipts at `da64646` now validate 8/8 exit 0 under the `9011581` validator via a path-prefix-remapped copy (`.ufo/waves/round-18/evidence/validate16/summary.json`); an in-place replay is red 8/8 because the pass-1 log directories no longer exist (`missing_file`, then `binding_mismatch`) and pass 2 rewrote pro-aether's `analyze.json` (w1 `RevValidatorPaths.md`, corrected per w2 `ValidateRemapAttack.md`).
- R17-PRODUCER-REV: pass 1 produced by `271167473d87ef710f07ecdd98caf0ce12091686`, pass 2 by `95e34db62f2693c455d7ee4dfef24b8f3ebc007d`; `d0ab299` is the verification revision (w1 `RevProducerRev.md`). Round-18 runs record `producer.json` (branch tip + tool digests).
- R17-SUMS-RUNLOG: the `carriers.tsv` line dropped at `95e34db` is restored byte-exact in `.ufo/waves/round-17/predictions/SHA256SUMS` (the one in-place edit to round-17 *run evidence*; five round-17 tools and `verify.py` were also edited in place under the contract); the `da64646` pass-1 `run-log.txt` lists 7/8 carriers (calib-shfmt missing; its receipt exists, `.ufo/waves/round-18/evidence/sums-runlog.json`) and has no final aggregate exit line — the 8 per-carrier `carrier-run.exit`/`compare.exit` files (all 0) stand in for it; the retained pass-2 log is 8/8. The restore makes the SHA256SUMS digest pinned in round-17 `verification.json` stale by design.
- R17-REGISTRY: `SKILL.md` rows go-route-compare, receipt-validate, pins, go-buildinfo-probe carry pinned values and write scope; citation-drift is `gate`; pins kind `tool` → `probe`.
- R17-S032-DIGEST: S033 anchors on title, state, head `a214355…` and a byte-stable `.patch` digest; page digests are fetch-time only (three L1 fetches, three digests, `.ufo/waves/round-18/evidence/s032-digests.json`).

## Mistakes

| # | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| 1 | vacuous | R17-PINMAP: r17 entry said each mid-run pin map was retained; receipts kept a verdict (`round-17-verifier-spotcheck.md:108,137`); `9011581:.ufo/waves/round-17/tools/carrier-run.py:475` even tagged "(QUALITY #19)" | QUALITY #19 by text; not applied (the tag was self-attestation) | QUALITY #21. Red-before at `9011581`: `git show 9011581:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md \| grep -cE 'R17-PINMAP\|comparator verdict'` → 0 (exit 1); 29/29 mid checks carry only the five verdict keys; a forged verdict-only entry (`entries` 7, 1970 timestamp) is accepted, exit 0 (w1 `CriticDiscernment.md`, reproduced w2 `QualityRowsIntact.md`). Fix: `carrier-run.py` writes `pins/mid-<n>.json` + `map_sha256`; `receipt-validate.py --require-mid-maps` exits 1 `mid_map_missing` on all 8 r17 receipts and 0 on all 15 r18 receipts; forged `entries` → `mid_entries_mismatch` |
| 2 | number-drift | R17-VALIDATE16: "all 16 receipts validated" vs 8 retained runs | QUALITY #18 | remapped validation 8/8 retained; `routed-defects.py` derives k/8 from the summary, now with every entry's stdout hash-bound and an exact (digit-bounded) fraction (red at `9011581`) |
| 3 | attribution | R17-PRODUCER-REV: second-pass receipts cited under the verification revision | QUALITY #18 | per-run `producer.json` (branch tip + 7 tool digests) — recorded, but no gate reads it (w2 `ProducerJson.md` L3), so it is a record, not a fix shown able to fail; routed-defects checks both producer hashes are named and are ancestors (red at `9011581`); the tool cannot check which pass each hash is attributed to (w2 `TruthPRODUCERREV.md` F1) |
| 4 | landing | R17-SUMS-RUNLOG: frozen manifest lost a line when a file was added | none | restored line; routed-defects compares every `2711674` manifest line byte-exact (red at `9011581`) |
| 5 | reference-drift | R17-REGISTRY and R17-S032-DIGEST | none (PROTOCOL row fields) / QUALITY #4 | rows fixed; routed-defects requires `Pinned values:` plus a non-empty write scope with resolvable paths, `--strict` in the citation-drift gate entry, and a 40-hex head plus ≥2 recorded page digests (red at `9011581`) |
| 6 | vacuous (this round, recurred) | C1 counter as first contracted: substring checks closable by tokens (w1 `CriticC1.md`). The amended "substance" checks were still closable by fabrication: one honest receipt whitewashed 14 (w2 `GatePINMAP.md`), deleted stdout files and an all-zero validator digest passed (w2 `GateVALIDATE16.md`, `ValidateRemapAttack.md`), `18/8` matched `8/8`, deleted `Pinned values:` passed (w2 `GateREGISTRY.md`), a fake 40-hex head passed (w2 `GateS032.md`) | none | wave-2 hardening: every r18 receipt checked, stdout hash-binding, digit-bounded fraction, `Pinned values:` and `--strict` required; selftest CLEAN 17 with token-only fixtures open. Still open: the validator digest is format-only, S033's head and PRODUCER-REV pass attribution are not resolvable offline — so `open_count 0` is reported together with the w2 Truth* re-derivations, not alone |
| 7 | number-drift (this round) | C2 "3 → 0" declared in `claims.json` before the lint existed, copied from audit prose; the first contracted rule gives 8 (w1 `CriticC2.md`) | CORPUS "a count carries its command" | amended scope rule written before measuring; baseline is the tool's output (3 live, 8 fixture, excluded files listed). Limit: two compare-only HEAD reads through nested wrappers (`round-17/verify.py:83`, `revpin.py:108`) are invisible to the lint (w2 `LintBlindSpots.md`), so "0 live" is a lint-rule count |
| 8 | stale-premise (this round) | C3 first design (methods vs nomethods) predicted non-diagnostic by three seats before any run | none | nethttp carriers and a real carrier added; diagnostic set D and the verdict rule frozen with the predictions (`predictions/decision-rule.json`) |
| 9 | landing (this round) | `routed-defects.py` amended after the freeze (finding ids) without updating its selftest fixture: `--selftest` exited 1 at `b2aad08` while this lesson said "CLEAN 17" (w2 `TruthVALIDATE16.md` F2, `LessonGateAudit.md` F1) | the round's own `verify.py` (expects every selftest 0) — not yet run | fixture updated; the post-integration `verify.py` pass records the selftest exit |
| 10 | scope (this round) | "frozen before any REA run": the wave-1 census had run REA `inspect-go-binary` on three label carriers before the freeze (w2 `FreezeBeforeRun.md`); `claims.json` amendment time 13:25:00 is after its own commit (13:23:55) | none | wording narrowed to "before any `analyze`" in the entry; the build-info call is a prediction input, not the measured outcome |

Misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain` found no untracked file naming kaidoku or round-18 at wave-1 close (w1 `ScoutMisrootFleet.md`) and wave-2 close (w2 `MisrootSweep.md`); re-run before the report.

## In-round revisions (after the wave-2 falsify pass, before closure)

- Knowledge entry `2026-10-20-r18-swiss-map-replay`: title and decision table scoped to Go 1.24 held-out / 1.25 calibration; H1 abort conditions widened; `http.Header` removed from the synthetic carriers' list; recipe audit attributed (w1 8, w2 12); kimi-webbridge described as the only *application* ELF found; D defined by failure kind; walk-channel merge and false positives disclosed; timestamps corrected; recheck line narrowed (re-hash, not recompute), `<GOLANG_DIR>` defined, retained-key print command added; row 4 of the decision table corrected (go1.24.6 vs go1.25.0, layout cause); Evidence-ID explanation corrected (w2 `KnowledgeEntryReview.md`, `KnowledgeDecisionTable.md`, `TrendVerdicts.md`, `S1250NethttpSilent.md`, `EmulatorSourceCheck.md`, `FreezeBeforeRun.md`).
- SKILL.md: r17 fallback row qualified (intermediate fallback now observed); jj pushed row (ancestry vs equality, `landed <hash>` only, HEAD-alias limit); registry rows receipt-validate, revpin, jj-red-before, swiss-misread, go-carrier-run-r18, r18-prediction-freeze given their limits.
- Tools: `routed-defects.py` fixture and hardening (row 6, 9); `custody-pair.py` git reads use `--no-optional-locks` and tolerate a shallow copy path (w2 `CustodyReview.md` F1/F2); round-17 `verify.py` derives `LANE` from its own path (w2 `Verify17Review.md` F1); round-18 `verify.py` validates with `--require-mid-maps` and adds revpin, runner selftest, emulator and census-count commands (w2 `Verify18Review.md`).
- SOURCES: S034 teaches revised; used-by appended (above); search-log correction line.
- Capability table: no row entered; `swiss-misread.py` is C3's depth instrument (w2 `CapabilityCandidate.md`).

## Open (routed earlier or found this round, still open)

- Round-12 routed items (w1 `ScoutOperatorLessons.md`): the r12 C1 entry `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` has no `S###` row and no custody-leg disclosure; the r12 operability axis "add or withdraw" decision was never recorded (w2 `OpenRoutedQueue.md`). Carried.
- PROVINCE.md pin drift (w2 `ProvinceAccuracy.md`): all three client configs now pin `rea-agents@6.7.0` (Devin/OMP files rewritten 2026-10-20 13:35:56 -03, outside the lane), the 6.4.0 npx cache is gone, and `PROVINCE.md:8-26,44` still states 6.5.0/6.4.0; `c1-census-v10.py` fails at baseline and now. Freshness debt, not fixed this round; round-18 runs pinned `rea-agents@6.5.0` explicitly.
- citation-drift refuses only the literal `--rev HEAD` (`@`, `HEAD~0`, `HEAD^{commit}` pass, w2 `CitationDriftReview.md` F1); custody-pair `repo-root` records the `--repo` argument, not the top level (w2 `CustodyReview.md` F4); jj-red-before selftest env scrub and pointer-table path guard (w2 `JjSandboxSafety.md` F1/F2).
- `invocation-audit.py` at `b2aad08` counts 9 unlabelled new registry rows (w2 `OpenRoutedQueue.md`, `AxisHarmCheck.md`); rows not exercised by the verification pass are now labelled unexercised variants; the measured count after the pass is in SCORECARD round 18.
- Adjacency (w2 `SiblingOverlap2.md`): the jj 0.45.1 git-compatibility document is registered three times (kaidoku S036 at the v0.45.1 tag, tameshi S061 at `latest`, tabi S049 at v0.45.1); the jj routing report gives the jj fact to kumitate (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjConnectorProvinces.md:181,189`). Reported, not absorbed: kaidoku keeps S036 only as the source for its own pin tools. `revpin.py:6` says HEAD sits on the working-copy commit; it is the working-copy parent (`@-`) — wording fix carried to round 19. Revenger's records still list Ghidra as absent on this host while it is installed (revenger-owned).
