# Round 19 — routed r18 defects, REA pin freshness, go1.25.0 toolchain Swiss replay

author: kaidoku-shokunin; 2026-10-20
scope: discharge the seven defects routed by `corpus/lessons/round-18-verifier-spotcheck.md:191-199`; re-verify the
PROVINCE.md drift-prone REA values against the live host; extend the round-18 Swiss-map replay to held-out official
go1.25.0 toolchain ELFs. Claims and the in-round amendment: `.ufo/waves/round-19/claims.json`.

## Claims

- C1 calibration (tied-lowest owned axis at 10.0): R18-MIDMAP-LISTSTEP, R18-VALIDATOR-DIGEST, R18-STRICT-BASELINE,
  R18-HEAD-ALIASES, R18-DEADSEAT-RECORD, R18-REGISTRY-PINNED, R18-INSTALL-RECORD, each closed by a named correction
  below **and** a substance check in `.ufo/waves/round-19/tools/routed-r18.py` that runs code or recomputes digests
  from the measured revision's Git objects. QUALITY #22 from R18-DEADSEAT-RECORD.
- C2 freshness (sourced: S037): PROVINCE.md and SKILL.md REA pin statements re-verified and rewritten in place
  (`province-pins.py` mismatches; `c1-census-v10.py` stale loci).
- C3 depth (sourced: S038, with S035/S023/S003): the unchanged round-18 emulator's per-carrier predictions for eight
  official go1.25.0 toolchain ELFs, frozen at `a1140e76fffdc1be032d9d813dbb686157803bbc` before any analyze, compared
  with run-bound Ghidra logs.

## Gate

### Candidate decisions (author-side; outside sampling is the closure's duty)

| Candidate | Decision | Evidence and limits |
|---|---|---|
| Knowledge entry `2026-10-20-r19-go125-toolchain-replay` | admit, narrowly | Frozen membership rule, not a full-model prediction success. First-pass bind became red after a validator edit; preserved pass 2 uses final producer bytes. Vet repeats 13902080, full compare remains 7/8, compile has an extractor-omitted deferred RTTI NPE; all limits retained |
| QUALITY #22 (seat-status statements carry a cutoff and a per-seat retained cause) | admit | R18-DEADSEAT-RECORD grounding; red exits 1 on 4 uncaused seats. Green input is `evidence/wave-outcomes/r18-w2-causes.json`, derived from (not identical to) `evidence/r18-dead-seats.json`; exits and stdout retained |
| SOURCES S037/S038/S039 | admit (mined) | S037 grounds published package integrity/time, S038 official archive SHA-256/size, S039 the historical own-work experiment. They do not interchange identity metadata and behavioral evidence |
| rea-agents 6.6.0 as a source | reject (no row) | Registry returns E404: no 6.6.0 was published (w1 `LiveConfigPins.md`) |
| C2 "c1-census PASS" as first declared | reject as declared; admit stale 4 → 0 | The two undeclared blocks (SCORECARD 2380-2382, SKILL 511-519) are round-17 text outside the gate's fixed scope table; closing them needs a scope re-key, a gate change, not a freshness edit (w1 `ReviewC1CensusScope.md`); amended before measuring |
| Emulator `diagnostic` field as the D-set rule | reject | It absorbs the full-walk failure into the H0 kind, so vet reads `diagnostic:false` while only H1 fails on the map path (w1 `H0H1Semantics.md`); D is frozen from the map-path booleans |
| "toolchain binaries are held-out *applications*" / "first Go 1.25 held-out" | reject | They are toolchain ELFs; Go 1.25.0 was already held by r18 synthetics, so the new evidence is artifact-held-out (w1 `SiblingOverlap.md`, `CoverageMapGo125.md`) |
| `head-rev-lint.py` `nested` class (dead seat HeadRevLintNested's partial clone) | reject | Its selftest fails (`SELFTEST: FAILED 3`, L1 run); the limit is registered in the SKILL row instead (`.ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch` retained) |
| `link` as a C3 carrier | exclude | No Go build info (emulator exit 2, `predictions/decision-rule.json` `excluded`) |
| The full-walk candidate 1801722468838924630 as a real Ghidra read | reject | Unmasked variadic output-count bit in the frozen emulator; Ghidra masks it (w2 `KnowledgeMechanism`) |
| “No analyzer errors” inferred from comparator silence | reject | Compile's deferred RTTI propagation NPE is attributed to AnalysisTaskWrapper and excluded by the extractor's Golang-component filter, both passes. No blanket clean-analysis or full-model-success claim |

### Opened sources and located quotes (access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S037 | https://registry.npmjs.org/rea-agents/6.7.0, version document `dist.integrity` | "integrity":"sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==" |
| S037 | https://registry.npmjs.org/rea-agents, packument `.time["6.7.0"]` | "2026-10-18T08:12:05.640Z" |
| S038 | https://go.dev/dl/?mode=json&include=all, go1.25.0 entry (fetched copy line 14644) | "filename": "go1.25.0.linux-amd64.tar.gz", |
| S038 | same entry, `sha256` field | "sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613", |
| S039 | own-work `.ufo/waves/arc3-loop1-round12/integration/c1/reconcile-all-go-ids.txt` at `8a8da7e`, line 28; opened 2026-10-20 | `records=27 matched=27 bundles=CR-1,CR-4,EX-2,EX-4,EX-5,EX-6,EX-8` |

### Registry changes (old → new)

- New rows S037/S038 (tier A dataset) and S039 (tier A own-work), all `mined`: rows 36 → 39. Six existing used-by cells were appended (S003/S023/S024/S026/S031/S035); exact old→new values are recorded under R19-USEDBY-APPEND below. No existing evidence/status/recheck cell changed.
- Search log: one round-19 note appended (S037/S038 search, 6.6.0 rejection).

### Outside spot-check

Pending: the hyaku closure session (non-author) samples this round's admits and rejects. Not self-attested.

## R18 routed defects — named corrections (append-only; filed bytes unchanged)

- R18-MIDMAP-LISTSTEP: `.ufo/waves/round-17/tools/receipt-validate.py` list-shaped `steps` under `--require-mid-maps` accepted pin checks on any step; only the step that identifies itself as `analyze` now counts (w1 `MidmapListStep` patch). Substance: `routed-r18.py` feeds REV's validator a list receipt with checks only on a non-analyze step (must raise `mid_checks_absent`) and one with checks on analyze (must not).
- R18-VALIDATOR-DIGEST: `validator-sha256-pinned` in `.ufo/waves/round-18/tools/routed-defects.py` now recomputes the digest of `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py` (dead seat ValidatorDigestGuard's clone, L1-verified selftest 19 and strict exit 0 at 8a8da7e); the eight remapped receipt copies are retained with digests in `.ufo/waves/round-19/evidence/validate16-remap/` (8/8 validator exit 0).
- R18-STRICT-BASELINE: `routed-defects.py --strict` (tool blob from a245bb0) retained at 9011581 (exit 1, open 6) and 454dee6 (exit 0) with argv, tool sha256 and hashed stdout/stderr in `.ufo/waves/round-19/evidence/strict-baseline/`.
- R18-HEAD-ALIASES: `citation-drift-probe.py` refuses every HEAD-derived or mutable `--rev` (`@`, `@~N`, `HEAD~0`, `HEAD^{commit}`, `HEAD@{0}`, pseudo-refs) with exit 2 (dead seat CitationDriftAliases' clone, L1-verified selftest 33 and lane exits); the two nested compare-only HEAD reads invisible to `head-rev-lint.py` are registered in its SKILL row as a limit.
- R18-DEADSEAT-RECORD: `SCORECARD.md:2462` ("1 dead … 4 not returned") is superseded: at integration cutoff `a245bb0` four round-18 wave-2 seats had no report — GateSUMSRUNLOG (Devin weekly quota after Anthropic/OpenAI cyber refusals), GatePRODUCERREV and TruthREGISTRY (zai 1302 rate limit), ShonenLines (aborted); DecisionRuleApply returned late. Per-seat causes with transcript pointers: `.ufo/waves/round-19/evidence/r18-dead-seats.json`.
- R18-REGISTRY-PINNED: SKILL rows `pins` (now "probe; no persisted baseline") and `go-buildinfo-probe` (now names `.ufo/waves/round-17/tools/buildinfo-probe.py`, whose literals are the pinned constants).
- R18-INSTALL-RECORD: the round-18 Go installs are recorded under `## Installs` below (round 18's report gave truncated digests and no date).

## Installs

Correction of round 18 (R18-INSTALL-RECORD; w1 `InstallRecordDraft.md`, values re-checked by the L1 against go.dev):

- go1.24.6 linux-amd64: official archive from go.dev (`https://go.dev/dl/?mode=json&include=all`), sha256
  `bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712`, 78583176 bytes, installed at
  `/home/vgpnk/.local/opt/go-1.24.6` on 2026-10-20 12:14 -03 (tarball mtime and directory birth time).
- go1.25.0 linux-amd64: official archive from go.dev, sha256
  `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`, 59659213 bytes, installed at
  `/home/vgpnk/.local/opt/go-1.25.0` the same minute. Nine installed files hash identically to their archive
  members (w1 `SourcesRowsDraft.md`).
- Reason: build the round-18 Swiss/noswiss synthetic carriers and read `internal/abi` source. Channel: official
  release tarball, because pacman was paused host-wide; placed under `~/.local/opt`, not on PATH.
- Round 19 installed or updated no tool.

## Mistakes

| # | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| 1 | number-drift | R18-DEADSEAT-RECORD: `SCORECARD.md:2462` "1 dead … 4 not returned" vs the fleet erratum's 3 dead; no committed wave file held a cause (`round-18-verifier-spotcheck.md:146,197`) | QUALITY #18 (retained records) — not applied to seat status | QUALITY #22; `wave-outcomes.py` red-before on round-18 wave 2 (exit 1, 4 uncaused) and green with retained causes (exit 0); this round's wave outcomes are produced by the same tool |
| 2 | vacuous | R18-VALIDATOR-DIGEST / R18-MIDMAP-LISTSTEP: two round-18 checks passed fabricated inputs (any 64-hex digest; pin checks on any list step) | none (the r18 gate's selftest kept them green) | `routed-r18.py` substance checks: at 8a8da7e both are red ("format-only check"; "accepted"), recorded in `.ufo/waves/round-19/evidence/routed-r18-B.json` |
| 3 | landing | R18-STRICT-BASELINE: the strict red baseline was claimed in SCORECARD round 18 with no retained run | QUALITY #18 | receipts retained; `routed-r18.py` re-hashes them and the tool blob |
| 4 | stale-premise | PROVINCE/SKILL REA pins left at 6.5.0 for a round after the 13:35:56 config rewrite (carried in `round-18.md:89`) | `c1-census-v10.py` (red at baseline, stale 4) — known but not acted on | in-place rewrite; stale 4 → 0, `province-pins.py` 2 → 0 (both red at 8a8da7e) |
| 5 | scope (this round) | InstallRecordDraft executed `bin/go version` despite the no-carrier-execution contract | wave contract, not technically enforced | **No demonstrated enforcement fix.** This remains a disclosed process violation; SHA-256 checks do not detect prior execution. Its output is not C3 outcome evidence |
| 6 | provider / landing (this round) | 42/90 W1 seats lack reports (9 direct 429 errors, 33 parent-session aborts); 48 have reports | none | No replacements. All last-assistant states retained in `evidence/wave-outcomes/w1-terminal.json`: 50 aborted / 12 error / 28 stop. Of report-present seats, 17 have aborted and 3 error last records; do not infer death or absence solely from report presence. Selected partial clones re-tested and reused, failed nested-lint patch rejected |

Misroot sweep: run before the report (see the fleet report).

## Open

- Round-12 items: the C1 entry now carries an append-only round-19 source/custody addendum (S024/S026/S031/S037; no pre-pair, post-only captures, current configs outside the last receipt) and marks its Docker identity/recheck precondition stale (w1 `R12Disclosure.md`). Operability add-or-withdraw decision is resolved in the section below. S037 used-by was extended in-round from `corpus/lessons/round-19.md` to also name `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`.
- `c1-census-v10.py` undeclared blocks SCORECARD 2380-2382 and SKILL 511-519 (round-17 text): scope-table re-key is a gate change for a calibration round.
- `head-rev-lint.py` nested compare-only reads: registered limit, not fixed.
- Adjacency: the jj 0.45.1 git-compatibility document stays registered as S036 only for kaidoku's own pin tools; tameshi S061 (`latest`) and tabi S049 also register it, and the routing report gives the jj fact to kumitate (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjConnectorProvinces.md:181,189`; w1 `JjRowRouting.md`). Reported, not absorbed; no L0 line.
- Operator-config observation (not lane-owned): the live `~/.omp/agent/mcp.json` no longer carries the rea entry's `enabled: false` (dropped by the 13:35:56 rewrite; recovery copy retains it, w1 `LiveConfigPins.md`).

## Carried r12 axis decision (2026-10-20, round 19)

`round-12-verifier-spotcheck.md:17` required an explicit add-or-withdraw decision.
Decision: **withdraw operability as an owned-axis improvement from the author's
round-12 scorekeeping**, not add a new owned numerical proxy now. The outside
verifier's historical admission remains unchanged; demonstrated tools and
receipts remain evidence. Coverage/depth/calibration stay the three owned axes.
Operability observations in subsequent rounds are labelled fleet-axis/unowned
proxy, never retroactively given an owned score. This resolves the decision
debt without claiming an extra round-19 axis move or changing the historical
outside-review bytes.

## C3 measured qualification

Eight source-bound validations are retained (`evidence/receipt-validation/`).
The patched validator was run from an extracted file with its producer's
recorded validator bytes restored at the pinned path; after the forward edit,
live validation correctly flags that one pinned file's hash/size drift.
All eight analyzer runs exit 0; full compares are 7/8 (vet exit 1 because the
frozen full index list has three entries, log only 13902080). The unchanged
frozen mechanism rule is confirmed by that H1-only index plus seven silent
controls. The full-list forecast is falsified, not called an exact success.
Routed counter's first integrated run also caught its own install-heading
parser taking a prose `## Installs` mention rather than the heading; anchored
to the real heading before final verification.

## Wave-2 source re-open clarification

W2 `ReopenS038` re-opened the official JSON: fetched document SHA-256
`6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950`
(2256879 bytes); go1.25.0 entry starts line 14514, archive filename line 14644,
sha256 line 14648. This pins the rendering used for Gate quotations, not the
time-varying endpoint indefinitely. S037 version-document SHA-256
`ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236`.
No existing SOURCES evidence cell was rewritten to add these clarifications.

## Wave-2 source-index correction (R19-USEDBY-APPEND)

Supersedes the initial Gate registry-change statement "No in-place change to S001–S036": only the following six used-by cells were appended; status/recheck/evidence cells stayed unchanged.

- S003 `used-by`: `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md, corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md, corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` → `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md, corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md, corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`.
- S023 `used-by`: `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md, corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` → `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md, corpus/lessons/round-15.md, corpus/knowledge/2026-10-20-r16-go-selection-preview.md, corpus/lessons/round-16.md, corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`.
- S024 `used-by`: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md` → `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`.
- S026 `used-by`: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md` → `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`.
- S031 `used-by`: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md` → `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`.
- S035 `used-by`: `corpus/lessons/round-18.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` → `corpus/lessons/round-18.md, corpus/knowledge/2026-10-20-r18-swiss-map-replay.md, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`.

S039 is a new tier-A own-work row (opened 2026-10-20), not publication metadata. Source: `.ufo/waves/arc3-loop1-round12/integration/c1/reconcile-all-go-ids.txt` at baseline `8a8da7e`, line 28, located quote: `records=27 matched=27 bundles=CR-1,CR-4,EX-2,EX-4,EX-5,EX-6,EX-8`; line 29 `exit=0`. It indexes the retained historical experiment and recomputation, not current Docker identity or uninterrupted custody. Final registry rows 36→39, additions A=3 (two dataset, one own-work); S037/S038 retain their identity-only scopes.

## Wave-2 integration and residual limits

- The source-counter patches address the falsifiers in `MutStrict`,
  `CriticCounter`, `SubstanceVALIDATORDIGEST`, `SubstanceSTRICTBASELINE`,
  `MutRegistry`, `MutInstall`, `MutAliases` and `SubstanceMIDMAPLISTSTEP`:
  strict output is replayed with its pinned A18 producer; causes match the
  pinned terminal report; buildinfo pins must name their actual source;
  install version/hash associations, channel and reason are checked; remap
  labels are distinct and historical; actual digest-gate wiring is mutated;
  flag forwarding goes through validate_receipt; mutable aliases receive
  lexical checks; relative roots are normalized and Git env is scrubbed.
  `postfix-mutations.py` retains actual post-fix mutant and restoration exits.
- `ToolPinsAntiVacuity` / `CriticFreshness`: parser no longer drops long
  clauses, sentence-final periods, lowercase/Oxford client groups or incidental
  “historical” words. Only an explicitly prefixed Historical: clause is
  historical. Empty fixture overrides no longer read live config silently.
  Final C2 assertion requires strict exit 0, no unstated clients and nine
  statements, not merely a printed zero.
- `SkillRegistryOld`: four citation findings came from two new index rows
  shifting README coordinates. They now occupy prior blank lines, preserving
  Frontier and frozen-scorecard pointer coordinates. The historical province
  receipt timestamp is explicitly labelled historical. `SubstanceHEADALIASES`:
  citation Tree now receives the resolved commit hash, not the moving branch
  expression. The old five-finding strict runs remain in seat reports.
- `ToolRunner` / `SandboxSecurity`: unsafe label traversal and unmatched
  selectors are refused; timeout wording is per-step; new output writers use
  exclusive random temporary files. Trusted lane Python/JavaScript is still
  executed by checker/catalog tools: mkdtemp is not an OS security sandbox.
- **Not claimed fixed:** citation snapshot-slug read escape on an adversarial
  table/expected pair; the validator can treat a decoy package token in an
  unrelated command as analyze (name/argv identity is not execution
  authentication); wave-outcomes flat-map key collision for a seat literally
  named `causes`; jj sandbox selftest coverage limits. Current round inputs
  contain none of those attacks. No claim of adversarial authenticity or
  complete validation coverage is made.
- Known model weaknesses are retained: prior vet prediction exposure, the
  unmasked-variadic full-walk bug, physically unattainable multi-index exact
  forecast for an aborting analyzer, and compile's separate RTTI NPE. The
  explicit map-path failure observation remains useful; these are not hidden
  as a green complete analyzer sweep.

## Final measured execution (author-side)

Source `b26a6c42207a859e70bd892c7e89a5befedf379b`, evidence
`2a6229f2fb415ba8efecbc2ae24e69ec89b64986`: the single post-integration
verification completed with **62 expected command exits, 26 content checks,
no failed check**, no source/tool integrity mismatch, and equal pin maps at
the two recorded instants. Ten post-fix mutants were killed, no survivor;
the relative-root and pristine controls exit 0. Actual stdout/stderr, argv,
times, tool identities and exits live in `verification.json` and `verify/`.
This is not outside verification.

- C1: strict B 7/7/7 open/named/substance, source 0/0/0.
- C2: strict mismatches 2→0, nine statements, no unstated client; census
  stale4→0, ambiguous/unresolved0, undeclared2 unchanged and FAIL/1 retained;
  G11 and scope marker error lists empty.
- C3: pass2 current validation 8/8 exit0, distinct bound count0→8,
  comparisons7/8, vet13902080 and seven non-D logs without the named
  failure signature. Compile's additional wrapper-attributed error is
  separately recorded in verification.json, not hidden by the comparator.
- No-harm source controls: coverage96/96→97/97 with no missing/dangling,
  depth17/17 unchanged; old QUALITY21 rows identical plus #22; LOG/SCORECARD
  and r12/r18 entries retain baseline prefixes; old lessons/runs/frozen
  predictions unchanged. No capability row or new coverage ground.
- SOURCES end census exit0 (W04 S033 retained): 39 rows, A34/B4/C1,
  mined37/rejected2. S039 and six reverse-index updates are recorded above.
- W1 90 / W2 72 seats, 162 total; W2 has72/72 reports and72 normal stop
  records. W1 reportless42 and all90 terminal records are retained
  separately. Two W2 job-cap refusals spawned none; third identical call
  spawned72, no replacement of a dead seat.
- Final misroot sweep: `git -C /home/vgpnk/Projects/shokunin status --porcelain`
  exit0, retained in `evidence/misroot-status.txt`. Only watchdog/state
  runtime entries appeared; no seat-authored misroot file. Copied/deleted
  none, driver files untouched.

LOG linkage: `LOG.md:2254` round-19 measured records; SCORECARD round-19
measured records at `:2505`. Outside sample remains the non-author closure's
duty; the carrier-execution breach and residual security/parser limitations
are disclosed, not silently waived.
