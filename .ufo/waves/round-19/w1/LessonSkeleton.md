# LessonSkeleton — round-19 lesson skeleton, verification and draft

Seat: `KaidokuR19.LessonSkeleton` (leaf, author-side advisory; no subagents dispatched; no lane file edited except this report).
Baseline: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` = `refs/heads/main` (`git rev-parse refs/heads/main`, output `8a8da7e…`) [observation].
Tool installs/updates: none. Read-only network calls: `curl` of `go.dev/dl/?mode=json&include=all`, `curl` of the npm tarball `rea-agents-6.7.0.tgz`, `npm view rea-agents` (dist-tags and metadata). No Go carrier was executed; no REA/Ghidra call was run on any carrier.
Exit codes: the census and c1-census outputs are read from retained files (their `exit=` lines are quoted). Ad-hoc shell commands below were run without a captured exit code; their output is shown instead.

## 1. Axes and what was checked

| Axis | Claim (from claims.json) | What this seat verified |
|---|---|---|
| calibration (C1) | Discharge seven routed R18 defects | Each of the seven is still open at baseline (section 3). |
| freshness (C2) | Rewrite stale PROVINCE REA pins; pin-drift probe | Live pins read, npm 6.7.0 identity checked, stale statements located (section 4). |
| depth (C3) | Held-out Go 1.25.0 carriers, frozen predictions | Prescan records read; one calibration flag found on `vet` (section 5). |

## 2. Observations about the lane baseline

- `claims.json:7` names the lowest axis as coverage/depth/calibration tied at 10.0; `claims.json:12`, `:19`, `:26` are C1/C2/C3; `claims.json:31-32` are frontier_step and carried_open.
- `contract.md:4` fixes baseline B = 8a8da7e…; `contract.md:41-42` names the C3 carriers `go` and `gofmt` plus the eight `pkg/tool` binaries.
- Census before: `.ufo/waves/round-19/evidence/census-before.txt` shows `exit=0`, a `W04 S033 duplicate url` warning, and `kaidoku ok …/corpus/SOURCES.md`.
- SOURCES row count: `grep -c '^| S[0-9]' corpus/SOURCES.md` = 36 (rows S001–S036; S033–S036 at `corpus/SOURCES.md:38-42`).
- Census C1 v10 before: `.ufo/waves/round-19/evidence/c1-census-v10-before.txt` ends `VERDICT: FAIL  (stale=4 ambiguous=0 undeclared=2 unresolved=0)` and `exit=1`.

## 3. Routed R18 defects — status at 8a8da7e (observation)

Source list: `corpus/lessons/round-18-verifier-spotcheck.md:191-199` (seven items). Carried items: `:201-206`.

1. **R18-MIDMAP-LISTSTEP — open.** `.ufo/waves/round-17/tools/receipt-validate.py:576-578` is the list branch: `elif isinstance(steps, list): ok = any(isinstance(s, dict) and s.get("pin_checks") for s in steps)`. The `analyze` step is not required there (`:570-578`, sed output).
2. **R18-VALIDATOR-DIGEST — open.** `.ufo/waves/round-18/tools/routed-defects.py:466-467` check is labelled `validator_sha256=… (format only; see limits)`; `:491` is the failure branch. `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum` = `618448829ba6c5d743ef10c5b686b9f4e09a3ae09f2da0aa5d0e50e3d239126f`, the value the item quotes (`round-18-verifier-spotcheck.md:194`).
3. **R18-STRICT-BASELINE — open.** `ls .ufo/waves/round-18/evidence` lists `carrier-buildinfo.json jj-red-before.json real-carrier-census.json s032-digests.json sums-runlog.json validate16`. No retained `routed-defects --strict` receipt. `grep -rl -- '--strict' .ufo/waves/round-18/evidence` matches only `jj-red-before.json`, a different tool.
4. **R18-HEAD-ALIASES — open.** `.ufo/gates/citation-drift/citation-drift-probe.py:329` is `if rev == "HEAD":` (exact-string refusal; `@`, `HEAD~0`, `HEAD^{commit}` pass). The two nested compare-only reads are `.ufo/waves/round-17/verify.py:83` (`rev-parse --verify HEAD^{commit}`, with `head-rev-lint: compare-only` at `:82`) and `.ufo/waves/round-18/tools/revpin.py:108` (`_resolve(lane, "HEAD^{commit}")`). Note: the item cites `revpin.py:108` without a directory; the file is under `round-18/tools/`, not `round-17/`.
5. **R18-DEADSEAT-RECORD — open.** `SCORECARD.md:2462` reads "1 dead (GateSUMSRUNLOG, provider usage-policy refusal), 4 not returned at integration (GatePRODUCERREV, TruthREGISTRY, DecisionRuleApply, ShonenLines)". The "3 dead" erratum named in the item was not found: `grep -rn '3 dead\|three dead'` over `.ufo/waves/round-18`, `.ufo/waves/round-19` and repo `*.md` returned nothing. The erratum sits outside the lane and is not verifiable here.
6. **R18-REGISTRY-PINNED — open.** `SKILL.md:542` (pins): "Pinned values: none (no expected digests; …)" with no path. `SKILL.md:545` (go-buildinfo-probe): "Pinned values: the build-info magic and header constants of go1.25.0 `debug/buildinfo`" — constants named, no file path, no "no persisted baseline" statement.
7. **R18-INSTALL-RECORD — open.** `corpus/lessons/round-18.md` has no tool-install block (`grep -n -i 'tool install\|installs/updates\|go1.24.6'` returns no install record). The round-17 precedent is `corpus/lessons/round-17.md:135-137` ("Tool installs/updates: none by the L1. Seat `DraftSourcesRows` … installed `~/.local/opt/go-1.27.3`"). Install facts for the round-19 record are in section 5.

## 4. Freshness (C2) — observations

- Live client pins (grep of config files, rea-agents lines only): `~/.config/devin/mcp_config.json:7` = `rea-agents@6.7.0`; `~/.omp/agent/mcp.json:8` = `rea-agents@6.7.0`; `~/.kimi-code/config.toml:4126` = `rea-agents@6.7.0`.
- Stated pins: `PROVINCE.md:16` (Devin `rea-agents@6.5.0`), `PROVINCE.md:17` (OMP `rea-agents@6.5.0`), `SKILL.md:19` (devin=6.5.0, omp=6.5.0). Stated-vs-live mismatches = 2 (Devin, OMP), matching `claims.json:20` expectation.
- `c1-census-v10` reports STALE at `PROVINCE.md:9,16,17,44`, `SKILL.md:19` and UNDECLARED at `SCORECARD.md:2380-2381`, `SKILL.md:512` (`c1-census-v10-before.txt`).
- npm registry: `npm view rea-agents dist-tags` → `latest: 6.7.0`; `npm view rea-agents@6.7.0 time` → `"6.7.0": "2026-10-18T08:12:05.640Z"`; `dist.integrity = sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==`. Downloaded tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz` (6276963 bytes) hashes to the same sha512 (observation).
- npx cache: `.npm/_npx/a1722018f28f9df2/package.json` and `.npm/_npx/ad9a3fdbcad992c6/package.json` name rea-agents (6.7.0 and 6.5.0 per `PROVINCE.md:19-21`); no 6.4.0 cache found (census UNRESOLVED at `c1-census-v10-before.txt`).

## 5. Depth (C3) — observations and one flag

- Go archive identity: `https://go.dev/dl/?mode=json&include=all` (fetched 2026-10-20) lists `go1.25.0.linux-amd64.tar.gz` sha256 `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`, size 59659213; `go1.24.6.linux-amd64.tar.gz` sha256 `bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712`, size 78583176. Local archives `/tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz` and `/tmp/kr18-dl/go1.24.6.linux-amd64.tar.gz` (`sha256sum`) match both values.
- Installed tree: `/home/vgpnk/.local/opt/go-1.25.0/VERSION` reads `go1.25.0` / `time 2025-08-08T19:33:32Z`; `sha256sum` of `bin/go` = `b93cdfdbc72f1afc3f21498c80bf3d155a44a9b95e2d690c940511051574bc25` (file hash only; binary not executed).
- Prescan (`.ufo/waves/round-19/evidence/prescan/kr19-sm-*.json`, nine files): `link` = `status: unparseable`, `error: no Go build info in …/pkg/tool/linux_amd64/link`. `asm`, `cgo`, `compile`, `cover`, `go`, `gofmt`, `preprofile` = `predicted_failure_kind_h0 none`, `predicted_failure_kind_h1 none`.
- **Flag (calibration, for L1 before freeze).** `kr19-sm-vet.json`: `predicted_failure_h1: true`, `predicted_failure_kind_h1: invalid_index`, but also `predicted_failure_kind_h0: invalid_index` with `predicted_invalid_index_reads_h0: [1801722468838924630]` and `predicted_failure_h0: false`. The top-level `diagnostic` is `false`. The emulator defines `diagnostic = predicted_kind_h1 != predicted_kind_h0` (`.ufo/waves/round-18/tools/swiss-misread.py:1531`), and the frozen rule defines D as labels "whose H1 and H0 failure kinds differ" (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:68-69`). Under that rule `vet` is not in D, while `claims.json:27` and the spot-check text assume a vet H1 `invalid_index` prediction. The H0 kind is computed from `h0_invalid` (`swiss-misread.py:1481-1482`) while the H0 failure flag comes from `h0_fail` (`:1466`), so the two fields disagree. INFERENCE: the H0 read at `1801722468838924630` is an out-of-range sentinel, so the vet discriminator may be an artifact of that value. Not resolved here; L1 decides before freeze.

## Draft

Verbatim draft for L1 integration (not yet decided; `[pending]` marks L1-owned decisions):

```
# Round 19 — routed R18 defects discharged, rea-agents pin freshness, Go 1.25.0 held-out replay

author: kaidoku-shokunin; 2026-10-20
scope: discharge the seven defects routed by `corpus/lessons/round-18-verifier-spotcheck.md:191-199`; re-verify PROVINCE.md REA pins against the live client configs and the npm registry (`corpus/lessons/round-18.md` Open, :88-89); extend the Swiss-map replay to held-out Go 1.25.0 application ELFs with frozen predictions.

## Claims

- C1 calibration (tied-lowest owned axis at 10.0; `.ufo/waves/round-19/claims.json:7`): R18-MIDMAP-LISTSTEP, R18-VALIDATOR-DIGEST, R18-STRICT-BASELINE, R18-HEAD-ALIASES, R18-DEADSEAT-RECORD, R18-REGISTRY-PINNED, R18-INSTALL-RECORD each closed by a named correction and a substance check (`.ufo/waves/round-19/claims.json:12-13`). [pending: counts after integration]
- C2 freshness: stated-vs-live client pin mismatches 2 at 8a8da7e (Devin, OMP; `PROVINCE.md:16-17`, `SKILL.md:19`; live `~/.config/devin/mcp_config.json:7`, `~/.omp/agent/mcp.json:8`) and `c1-census-v10` VERDICT FAIL stale=4 undeclared=2, exit 1 (`.ufo/waves/round-19/evidence/c1-census-v10-before.txt`). New source row: npm registry metadata for rea-agents 6.7.0 (`claims.json:21`). [pending: post-fix values]
- C3 depth: held-out go1.25.0 carriers (`contract.md:41-42`) with frozen predictions. Prescan: link unparseable; seven predicted silent; vet flagged (see Gate). [pending: L1 decision on vet]

## Gate

### Candidate decisions (author-side; outside sampling remains the closure's duty)

| Candidate | Decision | Evidence and limits |
|---|---|---|
| SOURCES S037 — npm registry metadata, rea-agents@6.7.0 | proposed admit [pending L1] | `npm view rea-agents@6.7.0 time` → 6.7.0 `2026-10-18T08:12:05.640Z`; tarball sha512 matches `dist.integrity` (observed by LessonSkeleton, `.ufo/waves/round-19/w1/LessonSkeleton.md` §4). Limit: registry metadata, not the installed tree |
| SOURCES S038 — go.dev/dl JSON, go1.25.0 linux-amd64 archive | proposed admit [pending L1] | sha256 `2852af0c…b613`, 59659213 bytes; matches the local archive `/tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz` (§5). Limit: archive-level identity; the installed `bin/go` hash is not a release identity |
| Prescan `vet` (H1 invalid_index; H0 kind also invalid_index) | [pending L1] | `kr19-sm-vet.json`; `swiss-misread.py:1531`; `…r18-swiss-map-replay.md:68-69` (§5) |

### Opened sources and located quotes (access date 2026-10-20)

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S037 (candidate) | https://registry.npmjs.org/rea-agents (`npm view`), version 6.7.0 | `"latest": "6.7.0"` (dist-tags) and `"6.7.0": "2026-10-18T08:12:05.640Z"` (time) |
| S038 (candidate) | https://go.dev/dl/?mode=json&include=all, entry `go1.25.0` | `go1.25.0.linux-amd64.tar.gz` … `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613` |

### Registry changes (old → new)

- Proposed: new rows S037 and S038 (rows 36 → 38). No in-place S001–S036 evidence cell changed.
- `used-by`: [pending L1 — assigned to the corpus/knowledge entry that cites them, if admitted].
- Census: `scripts/sources-census.sh validate` at round start printed `W04 S033 duplicate url … across scopes` and exit 0 (`.ufo/waves/round-19/evidence/census-before.txt`). [pending: census at round end]

### Outside spot-check

Pending: the hyaku closure session (non-author) samples this round's admits and rejects. Not self-attested.

## R18 routed defects — named corrections (append-only; filed bytes unchanged)

- R18-MIDMAP-LISTSTEP: open at 8a8da7e (`.ufo/waves/round-17/tools/receipt-validate.py:576-578`). Named correction: [pending]. Substance fix: require the `analyze` step in the list branch; red fixture [pending].
- R18-VALIDATOR-DIGEST: open at 8a8da7e (`.ufo/waves/round-18/tools/routed-defects.py:466-467` format-only). Named correction: [pending]. Substance fix: compare to `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum` (= `618448829ba6…126f`) and retain per-copy digests in `validate16/summary.json` [pending].
- R18-STRICT-BASELINE: open at 8a8da7e (no `routed-defects --strict` receipt under `.ufo/waves/round-18/evidence/`). Named correction: [pending]. Substance fix: retain the strict run [pending].
- R18-HEAD-ALIASES: open at 8a8da7e (`.ufo/gates/citation-drift/citation-drift-probe.py:329`; `.ufo/waves/round-17/verify.py:83`; `.ufo/waves/round-18/tools/revpin.py:108`). Named correction: [pending]. Substance fix or registered limits [pending].
- R18-DEADSEAT-RECORD: open at 8a8da7e (`SCORECARD.md:2462`); the "3 dead" erratum is outside the lane. Named correction: [pending]. Substance fix: append the failure causes [pending].
- R18-REGISTRY-PINNED: open at 8a8da7e (`SKILL.md:542` "Pinned values: none"; `SKILL.md:545` constants with no path). Named correction: [pending]. Substance fix: name the path or state "no persisted baseline" [pending].
- R18-INSTALL-RECORD: open at 8a8da7e (`corpus/lessons/round-18.md` has no tool-install block; precedent `round-17.md:135-137`). Named correction: [pending]. Substance fix: add the Go 1.24.6 / 1.25.0 record (tool `go`, version, channel = official go.dev tarball, sha256 `bbca37cc…8712` / `2852af0c…b613`, reason = Swiss-map carriers) [pending].

## Mistakes

| # | class | evidence | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| 11 (candidate) | stale-premise (freeze) | `kr19-sm-vet.json`: H0 and H1 kinds both `invalid_index`, so `diagnostic: false` under `swiss-misread.py:1531` and the frozen D rule (`…r18-swiss-map-replay.md:68-69`) | [pending L1] | [pending L1] |
| 12 (candidate) | vacuous / stale-premise | R18-DEADSEAT-RECORD: `SCORECARD.md:2462` counts 1 dead + 4 not returned; the erratum with "3 dead" is outside the lane | [pending] | [pending] |

## Open

- Carried (`round-18-verifier-spotcheck.md:201-206`; `round-18.md:88-92`): the r12 C1 entry lacks an `S###` row and a custody-leg disclosure (`round-18.md:88`); the r12 operability add/withdraw decision (`:88`); PROVINCE REA-pin drift (client configs now `rea-agents@6.7.0`; `PROVINCE.md:16-17` still 6.5.0; `round-18.md:89`) — C2 scope; citation-drift literal-HEAD refusal (`round-18.md:90`) — R18-HEAD-ALIASES; custody-pair `repo-root` records the argument (`round-18.md:90`); jj-red-before env scrub and path guard (`round-18.md:90`); `revpin.py:6` `@-` wording (`round-18.md:92`; observed at `.ufo/waves/round-18/tools/revpin.py:6`); the jj 0.45.1 doc triple registration (`round-18.md:92`; routed to kumitate).
- Operator/protocol: the §3 `1× planner` vs the hyaku §6 L1 planner seat (`round-18-verifier-spotcheck.md:208`).
```

## 6. Items this seat could not verify

- The `3 dead` erratum (R18-DEADSEAT-RECORD) is not in the lane (section 3, item 5).
- The `validate16/summary.json` per-copy digests and the `routed-defects --strict` baseline were not reproduced (no run performed; read-only seat).
- The round-17 `receipt-validate.py` red fixture and the `routed-defects.py` selftest were not run (assignment forbids verification runs).

## 7. Temp files outside the lane

`/tmp/kr19-godl.json` (go.dev JSON, fetched), `/tmp/kr19-rea-agents-6.7.0.tgz` (npm tarball). No lane file was written except this report.
