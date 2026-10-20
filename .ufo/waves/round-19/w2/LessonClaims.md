# Round 19 lesson Claims/Gate review

**Axes:** calibration, freshness, depth. Read-only review of `corpus/lessons/round-19.md`, the round-19 claim/rule records, retained wave evidence, and the current working diff. No production files were edited; this file is the sole write.

**Observed snapshot:** `refs/heads/main` = `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (exit 0). The worktree has uncommitted `M` entries for `.ufo/waves/round-19/tools/routed-r18.py`, `corpus/SOURCES.md`, and `corpus/lessons/round-19.md`, plus untracked `.ufo/waves/round-19/w2/` and `runs/pass2/` (status command exit 0). Thus observations below distinguish the committed tip from pending integration bytes.

## Findings by severity

### Blocker — the lesson still has an explicit pending outside-verification placeholder

**[OBS]** `corpus/lessons/round-19.md:51-53` says `Pending: the hyaku closure session (non-author) samples this round's admits and rejects. Not self-attested.` The candidate table at `:22-34` is explicitly author-side. No non-author sampling result is present among the round-19 W2 reports; `CriticAdmission.md:51-57` also records that the outside sample has not occurred. `SCORECARD.md:2479,2493,2499` still says final verification/verdict is to be appended and outside sampling belongs to closure.

**[INF]** The report correctly disclaims self-attestation, but the requested no-pending-standards acceptance is not met. The round cannot be marked closed until the outside sample has an actual disposition and the pending placeholder is replaced; author-side reports do not satisfy it.

### High — C3's latest binding requirement has no retained final validation result

**[OBS]** Frozen `predictions/decision-rule.json:3` counts a label only if `receipt-validate.py --require-mid-maps` exits 0 on its receipt. The second claims amendment `claims.json:46` expressly says final counts must require live receipt validation at the delivered source and not treat historical exit-0 records as current. Yet the retained eight validations in `evidence/receipt-validation/` are first-pass records; the current validator exits 1 on all eight because its own pinned bytes changed. This is documented per-label in `w2/OutcomeVet.md:31-43,210-273` and `w2/OutcomeGo.md:136-166`; the drift is exactly `sha256_mismatch` + `size_mismatch` on `receipt-validate.py`, not carrier or log drift.

The second pass now has all eight `compare.json` files and a complete `runs/pass2/run-log.txt:1-19`; pass-two vet again reports only the frozen H1-only index (`runs/pass2/t1250-vet/compare.json:50-60`, raw log `:186,:229`). But there is no pass-two validation evidence in `evidence/receipt-validation/` (that directory still has only `t1250-*.json` first-pass files), and `verify.py:560-575,669-683` still iterates top-level `runs/<label>` and the original retained validations rather than `runs/pass2/`. The final C3 count therefore has logs and comparisons but no recorded proof that the new receipts pass the live binding gate.

**[INF]** The raw-log mechanism pattern repeats, but C3's “confirmed” disposition is not yet demonstrated under the latest explicit live-binding rule. Do not count the first-pass eight as current after the amendment; keep the C3 admission unresolved until pass-two receipts have a retained live-validation result and the final verification records it.

### High — C1's `open 7 → 0` result is not admission-grade on the committed main tip

**[OBS]** `w2/CriticCounter.md:25-34,50-74` mutated one field at a time on the observed `d0690fd` tool: swapping the go1.24.6/go1.25.0 digests, substituting unknown or fabricated dead-seat causes/source pointers, using an unrelated existing registry path, and replacing the install correction with “declined” all still produced `open_count=0`. The `d0690fd..279e8b1` `routed-r18.py` diff only adds strict-baseline replay and expands/refactors alias checks; it does not change the dead-seat, registry, install, or named-correction checks that let those mutants pass. These false-green results therefore still apply to the committed 279e8b1 counter. The actual current records may be correct; the finding is that the claimed `0` does not establish the substance it purports to measure.

The working-tree `routed-r18.py` has additional uncommitted changes to those checks, but no post-change measurement is retained. The only structured integrated record, `evidence/routed-r18-integrated.json:40-49`, is pinned to `4f6c73f` and has `open_count: 1` for `R18-INSTALL-RECORD`; `ReportEvidence.md:34-39` reports a later `d0690fd` result, not a run of the current worktree version. `SCORECARD.md:2493` still labels the final C1 verdict “appended after verification.”

**[INF]** Neither the old structured output nor the unmeasured dirty counter supports final C1 closure. The counter needs its false-green cases killed and the resulting exact revision re-measured before the `open 0` claim is admitted.

### Medium — the C3 comparator misses a Go analysis-task failure in the “silent” compile control

**[OBS]** The second-pass raw compile log has `ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred) - element cannot be mapped to a null key java.lang.NullPointerException` at `runs/pass2/t1250-compile/logs/rea-ghidra-07WMDZ/ghidra.log:347`. Its `compare.json:2,37-40` nevertheless says `all_match: true` and `extra.analyzer_errors_empty` observed `[]`. The first-pass raw-log review reaches the same finding: `w2/OutcomeCompile.md:32,80-94` shows that `log-extract.py:243` only counts `ERROR` records whose component starts with `Golang`, so it drops this `AnalysisTaskWrapper` Go RTTI task error.

**[INF]** This does not refute the narrow map-path H1 discriminator: compile has no `Invalid index` and is non-D. It does falsify the unqualified “seven silent”/empty-analyzer-errors presentation in `claims.json:40` and `round-19.md:119-122`. Report compile as “no frozen `GolangSymbolAnalyzer` failure, but one unmodeled Go RTTI task ERROR,” not as wholly silent; the compare's 7/8 is extractor-scoped, not a complete raw-error census.

### Medium — S039 is declared mined/source-indexing complete without a Gate decision, and is not in the committed source registry

**[OBS]** The current working lesson lists S039 as a located quote at `corpus/lessons/round-19.md:44` and says all three rows are mined at `:48`; the latest amendment says R12 source indexing is completed by S039 at `claims.json:47`. But the author-side “Candidate decisions” table `round-19.md:24-34` has no S039 admit/reject row. `S039` is in the working-tree `corpus/SOURCES.md:45` (own-work, historical one-ELF/call-shape scope), while `refs/heads/main` still lacks it: `corpus/SOURCES.md` is an uncommitted change and the 279e8b1 commit diff from d069 has no SOURCES change. The quote itself is present at `.ufo/waves/arc3-loop1-round12/integration/c1/reconcile-all-go-ids.txt:28-29` (`records=27 matched=27`, `exit=0`); the S039 row limits it to historical evidence, not current Docker identity, continuous custody, or a universal rule. The R12 addendum states the same boundary at `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md:44-48`.

**[INF]** The local record supports its narrow historical scope, but the claimed completed source-index disposition is not in the delivered main tree and the lesson Gate leaves the new admission unreviewed. Add an explicit S039 decision with the row's limits and integrate the row before claiming source-index closure.

### Medium — the scorecard's C3 count command counts run files, not unique labels

**[OBS]** `SCORECARD.md:2495` counts `find .ufo/waves/round-19/runs -name compare.json | wc -l`. At this snapshot that command returns **16**, exit 0: 8 first-pass compare files plus 8 second-pass compare files. The first-pass directory has 8, the `pass2` directory has 8, and the eight labels repeat. The `decision-rule.json:6` count is *labels*, not attempts/files. The retained first-pass validation directory has 8 records, but none refers to `runs/pass2/`.

**[INF]** The reported `0 → 8` can still be the unique-label count, but the scorecard's stated command no longer computes that quantity. It must deduplicate by label and filter by the live binding condition; otherwise the count is 16 and includes unvalidated attempts.

### Low — the `link` exclusion overstates what the parser established

**[OBS]** `round-19.md:34` and `predictions/decision-rule.json:10-17` say “No Go build info” and cite emulator exit 2. `w1/CriticSourced.md:55` reports raw `\xff Go buildinf:` magic bytes in `link` at file offset 3461224, while explicitly noting that this does not prove a valid decodable record. The observed fact is that the frozen emulator cannot parse it (`exit 2`/`unparseable`), not that the artifact contains no build-info bytes.

**[INF]** Excluding `link` from this parser's run cohort is justified; the reason should be narrowed to “unparseable by the emulator / no decodable Go build info,” not an absolute absence claim.

### Low — the registered nested-read limit has one stale source locator

**[OBS]** The nested-patch rejection is supported: `w2/ToolAliasLintLimits.md:15-23,51-64` reproduces `SELFTEST: FAILED 3` in an isolated clone, while the baseline selftest is clean. The registered limitation is present in `SKILL.md:587`, but `ToolAliasLintLimits.md:7-13` shows its cited `revpin.py:108` now points at the `source: None` field; the `HEAD` read is at line 113.

**[INF]** The rejection itself is sound, and the nested limitation is documented; only the line citation is stale, weakening recheckability of the “registered limit” claim.

## Audited decisions with no separate falsifier

| Decision in `round-19.md` | Review result | Evidence / limit |
|---|---|---|
| QUALITY #22 admit (`:27`) | Supported | Red evidence records 4 missing / 4 uncaused and exit 1; green retains causes and exit 0 (`evidence/wave-outcomes/r18-w2-red.stdout:1-4`, `.exit` says `exit=1`; green `.stdout:1-4`, `.exit` says `exit=0`). `evidence/r18-dead-seats.json:4-7,11-70` carries the cutoff and per-seat cause/source pointers. The wave tool's green alone checks non-empty causes; the retained per-seat record supplies the stronger source evidence. |
| S037/S038 mined admit (`:28, :40-43`) | Supported within stated identity/provenance scope | `w2/ReopenS037.md:19-24,70-91` reproduces registry integrity/publish identity and 6.6.0 absence; `w2/ReopenS038.md:16-23,125-164,188-212` reproduces the go.dev archive digest and carrier-member identity. The current lesson pins the JSON rendering at `:128-134`. These rows do not prove C2 live pins or C3 Ghidra outcomes; the Gate itself states that limit. |
| Reject rea-agents 6.6.0 (`:29`) | Supported | Registry version map lacks 6.6.0 and the endpoint returns E404 (`w1/LiveConfigPins.md:107-110,134-135`; `w2/ReopenS037.md:83-91`). |
| Reject C2 census PASS; retain stale 4→0 (`:30`) | Correctly amended; no PASS claimed | Baseline retained census records stale=4 / undeclared=2 (`evidence/c1-census-v10-before.txt:6-14,38-45,110-113`); C2 amendment `claims.json:39` says FAIL remains. The later PROVINCE change adds `re-grepped` receipt wording at `PROVINCE.md:44`, which addresses the earlier W2 G11 finding; no final post-change census receipt is present, so the amended residual should still be verified once. |
| Reject emulator `diagnostic` as D-set rule (`:31`) | Supported | The emulator mixes full-walk failure into its kind but exposes map-path booleans separately; vet has H1 map-path failure true, H0 false, with a shared walk-only index (`w1/H0H1Semantics.md:5-19`; frozen rule `decision-rule.json:2,7-9`). |
| Reject “applications” / “first Go 1.25 held-out” (`:32`) | Supported after amendment | The current wording identifies toolchain ELFs and artifact-held-out evidence, not applications/version-held-out; R18 had Go 1.25 synthetics (`w1/SiblingOverlap.md:9,17-21`; `w1/CoverageMapGo125.md:15-19,28-32`; lesson `:16-18,32`). |
| Reject nested-lint patch (`:33`) | Supported for that candidate | Isolated selftest fails as claimed; canonical W18 lint remains unchanged and SKILL registers the limit (`w2/ToolAliasLintLimits.md:15-23,33-64`; `SKILL.md:587`). |
| Exclude `link` (`:34`) | Exclusion supported; reason needs narrowing | Emulator exit 2/unparseable is a valid cohort exclusion. Raw magic means “no Go build info” is stronger than the evidence supports (`w1/CriticSourced.md:55`). |

The first amendment's future timestamp is explicitly withdrawn by the later append-only correction at `claims.json:43-45`; the C3 predictions/rule remain frozen at `a1140e7` before first analysis. The first-pass vet result also honestly reports the falsified full read list (only `13902080` observed versus three predicted; lesson `:118-122`, `w2/OutcomeVet.md:22-30,148-161`).

## Commands, exits, and verification gaps

Read-only commands executed for this review:

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
→ 279e8b19c51658bfd05b9e31a1c0894ab2e70537 ; exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --short -- corpus/lessons/round-19.md corpus/SOURCES.md .ufo/waves/round-19/tools/routed-r18.py .ufo/waves/round-19/runs/pass2 .ufo/waves/round-19/w2
→ M routed-r18.py, M SOURCES.md, M round-19.md, ?? runs/pass2/, ?? w2/ ; exit 0

find .ufo/waves/round-19/runs -type f -name compare.json -print | wc -l
→ 16 ; exit 0
find .ufo/waves/round-19/runs -mindepth 2 -maxdepth 2 -type f -name compare.json -print | wc -l
→ 8 first-pass files ; exit 0
find .ufo/waves/round-19/runs/pass2 -mindepth 2 -maxdepth 2 -type f -name compare.json -print | wc -l
→ 8 second-pass files ; exit 0
find .ufo/waves/round-19/evidence/receipt-validation -maxdepth 1 -type f -name 't1250-*.json' -print | wc -l
→ 8 first-pass validation records ; exit 0
```

`read xd://lsp` returned “No such tool”; LSP status, references, definitions, and diagnostics were unavailable. Literal search was used only to locate report text and was not treated as semantic proof. No tests, builds, REA/Ghidra commands, carrier execution, installs, or mutations were run by this reviewer.

**Residual risk / closure gate:** current source/lesson changes, pass-two runs, and W2 reports are uncommitted. `verify/` has no retained final output at this snapshot; `SCORECARD.md:2479,2493` says the final C1 verdict/verification is still to be appended. Main must integrate the scoped edits, validate current pass-two receipts, re-measure C1/C2 at the delivered revision, correct the C3 error/denominator wording, add the S039 Gate decision, and replace the explicit pending outside-sample placeholder before the lesson can be called closed.