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
| Knowledge entry `2026-10-20-r19-go125-toolchain-replay` | admit | See the entry; predictions frozen at `a1140e7` before the first analyze (run log starts 15:57:51 -03, freeze pushed 15:57:47); C3 outcome per the frozen rule |
| QUALITY #22 (seat-status statements carry a cutoff and a per-seat retained cause) | admit | Grounded in R18-DEADSEAT-RECORD (`round-18-verifier-spotcheck.md:146,197`); red-before: `wave-outcomes.py` on round-18 wave 2 with no causes exits 1 naming 4 uncaused seats, green with `r18-dead-seats.json` causes exits 0 (`.ufo/waves/round-19/evidence/wave-outcomes/`) |
| SOURCES S037 (npm registry rea-agents 6.7.0), S038 (go.dev JSON go1.25.0 archive) | admit (mined) | Opened 2026-10-20 by w1 `SourcesRowsDraft` and re-opened by the L1 the same day (integrity, publish time, sha256 and size reproduced); each scoped to identity/provenance only (w1 `CriticSourced.md`: metadata grounds identity sub-claims, not outcomes) |
| rea-agents 6.6.0 as a source | reject (no row) | Registry returns E404: no 6.6.0 was published (w1 `LiveConfigPins.md`) |
| C2 "c1-census PASS" as first declared | reject as declared; admit stale 4 → 0 | The two undeclared blocks (SCORECARD 2380-2382, SKILL 511-519) are round-17 text outside the gate's fixed scope table; closing them needs a scope re-key, a gate change, not a freshness edit (w1 `ReviewC1CensusScope.md`); amended before measuring |
| Emulator `diagnostic` field as the D-set rule | reject | It absorbs the full-walk failure into the H0 kind, so vet reads `diagnostic:false` while only H1 fails on the map path (w1 `H0H1Semantics.md`); D is frozen from the map-path booleans |
| "toolchain binaries are held-out *applications*" / "first Go 1.25 held-out" | reject | They are toolchain ELFs; Go 1.25.0 was already held by r18 synthetics, so the new evidence is artifact-held-out (w1 `SiblingOverlap.md`, `CoverageMapGo125.md`) |
| `head-rev-lint.py` `nested` class (dead seat HeadRevLintNested's partial clone) | reject | Its selftest fails (`SELFTEST: FAILED 3`, L1 run); the limit is registered in the SKILL row instead (`.ufo/waves/round-19/w1/inherited/HeadRevLintNested.patch` retained) |
| `link` as a C3 carrier | exclude | No Go build info (emulator exit 2, `predictions/decision-rule.json` `excluded`) |

### Opened sources and located quotes (access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S037 | https://registry.npmjs.org/rea-agents/6.7.0, version document `dist.integrity` | "integrity":"sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==" |
| S037 | https://registry.npmjs.org/rea-agents, packument `.time["6.7.0"]` | "2026-10-18T08:12:05.640Z" |
| S038 | https://go.dev/dl/?mode=json&include=all, go1.25.0 entry (fetched copy line 14644) | "filename": "go1.25.0.linux-amd64.tar.gz", |
| S038 | same entry, `sha256` field | "sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613", |

### Registry changes (old → new)

- New rows S037 (tier A, dataset) and S038 (tier A, dataset), both `mined`. Rows 36 → 38. No in-place change to S001–S036.
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
| 5 | scope (this round) | w1 `InstallRecordDraft` ran `go version` with the go1.24.6/go1.25.0 `bin/go`, a C3 carrier, although the contract forbids executing carriers (`.ufo/waves/round-19/contract.md`, REA section) | the wave contract — not enforced by any tool | the install record above cites archive digests, not the executed output; no C3 measurement uses it; carriers' sha256 was re-checked at run time against the frozen `carriers.tsv` |
| 6 | provider / landing (this round) | 42 of 90 wave-1 seats left no report: 9 died on Anthropic 429s (~9400 s retry-after; critics, sentinels, two scribes) and 33 were aborted when the L1 session exited on an Anthropic 429 (`.ufo/waves/round-19/wave1-outcomes.json`, causes with transcript pointers in `evidence/wave-outcomes/w1-causes.json`); 3 more seats wrote their report before their final message hit a 429 | none | dead seats were not replaced; their partial clones were reused only where the L1 re-ran their selftests (ValidatorDigestGuard, CitationDriftAliases, JjRedBeforeSafety, ProvincePinsTool, RunCarriersR19) and rejected otherwise (HeadRevLintNested); each kept as a dead seat in `wave1-outcomes.json` |

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
