# Round 19 wave 2 — SOURCES gate audit (KaidokuR19.SourcesGate-3)

Scope: SOURCES gate shape; status/recheck/used-by/opened changes old→new; census before/after; quotes of new rows; freshness of the two new rows (S037, S038). Read-only in LANE. No production edits. Mutations only in my own mkdtemp clones. No delegation, no installs, no builds, no broad suite.

Observed bases:
- Baseline B = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (contract.md).
- Main tip at my start = `5e364bd5e6016f030a04b4b8c81830477ebdaf51`. Main moved to `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (16:10:41 -0300, "round-19: wave-two assignment records and verification expected-red safeguards") during my run. `corpus/SOURCES.md` blob is `c7bacb0bc60731a6e34d8a531e50c392697ede0a` at both tips, so all SOURCES results below hold for either. The knowledge file blob `f163243…` is also identical at both tips.
- Lane working tree: `git status` shows `M corpus/lessons/round-19.md`, `M .ufo/waves/round-19/verify.py`, and (observed later) `M corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` (+7 lines, uncommitted, not analysed). `corpus/SOURCES.md` in the working tree is identical to `refs/heads/main` (`git diff --quiet` exit 0).

Labels: **[OBS]** = observed by a command in this report. **[INF]** = inference from observations.

Mkdtemp root: `/tmp/kr19-w2-SourcesGate.RxjSPx` (clones `c-8a8da7e`, `c-5e364bd`, `c-prop`; fetched copies `npm/`, `go/`).

---

## 1. Verdict

1. **Gate result: clean on both bases.** Census, validate and overdue exit 0 at baseline and at tip. Only pre-existing warning: `W04 S033` (same pull/9348 URL as S032 across scopes), unchanged since round 18.
2. **Row mutations: none to S001–S036.** `status`, `opened`, `recheck`, `used-by`, `tier`, `scope` are byte-identical for all 36 pre-existing rows (row-level join, §3.2). Two rows added: S037, S038.
3. **Defect (depth/traceability, not caught by the gate): the `used-by` reverse index is missing six round-19 citations.** The round-19 Go 1.25 knowledge entry cites S003, S023, S035 but none lists it. The round-12 addendum's grounding rows S024, S026, S031 do not list it either. Round 18 did append used-by in place for its citations (S003, S023, S035 list `2026-10-20-r18-swiss-map-replay.md`). The lesson line `round-19.md:47` ("No in-place change to S001–S036") is literally true but hides this gap. The gate cannot see it: E11 checks only that a used-by path exists on disk, and validate passes at tip (§4.3). Exact correction in §5; proven clean on a mutant clone in §6.
4. **Freshness of the new rows: verified live.** S037 (npm rea-agents@6.7.0) and S038 (go.dev go1.25.0 archive, plus all nine carrier digests) reproduce exactly; details in §7.

---

## 2. Gate shape (what the gate checks)

Gate = `scripts/sources-census.sh` in the fleet repo, `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (806 lines, sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, last commit `6a1dd8c`). Header states SOURCES-CONTRACT-v1: one registry table, 11 columns (NF=13 after splitting on `|`), statuses `queued|mined|rejected`, community never tier A. Read-only, stdout only.

Modes and codes (script header lines 2–38; checks at `row_pass` lines 574–694 and `usedby_findings` lines 538–571):

| Code | Check | Source line |
|---|---|---|
| E01 | NF != 13 | sources-census.sh:635 |
| E02 | id not `S[0-9]{3,}` | :637, :640 |
| E03 | duplicate id | :641 |
| E04 | duplicate URL within scope (not rejected; no `supersedes`) | :646–649 |
| E05 | kind enum | :655 |
| E06 | tier enum `A|B|C` | :657 |
| E07 | status enum | :658 |
| E08 | opened not past/present ISO date | :660–662 |
| E09 | recheck not ISO date, `NNd`, or symbolic | :663–667 |
| E10 | community at tier A | :668 |
| E11 | **used-by path missing on disk** (existence only) | :566–567 |
| E12 | row-shaped source outside `## Registry` | :619–621 |
| W01–W04 | tier-C mined with used-by; thin reject; mined unused; same URL across scopes | :669–674, :645 |

Blind spot **[OBS]**: no check compares a source's used-by against the files that actually cite it. E11 only checks existence. Confirmed by §4.3 (validate exit 0 at tip with six missing reverse links).

Selftest: `bash scripts/sources-census.sh selftest` → exit 0, `selftest ok`, 96 `killed`, 0 `SURVIVED` (1.18 s). **[OBS]**

Invocations used (all read-only):
- `bash scripts/sources-census.sh census --file <clone>/corpus/SOURCES.md --today 2026-10-20` → exit 0 (base and tip).
- `bash scripts/sources-census.sh validate --file <clone>/corpus/SOURCES.md --today 2026-10-20` → exit 0 (base and tip).
- `bash scripts/sources-census.sh overdue --file <clone>/corpus/SOURCES.md --today 2026-10-20` → exit 0 (base: 36 cadence lines, 0 overdue; tip: 38 cadence lines, 0 overdue).
- Canonical lane invocation, lane working tree: `cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh census kaidoku --root /home/vgpnk/Projects/shokunin --today 2026-10-20` → exit 0; `validate kaidoku …` → exit 0 (`kaidoku ok …/corpus/SOURCES.md`).

`--file` is used for revision pins because the script's `--file` mode resolves `dirname/..` as the lane root, so used-by paths resolve inside the clone.

---

## 3. Status / recheck / used-by / opened changes, old → new

### 3.1 Census before/after

| Metric | Base `8a8da7e` | Tip `5e364bd` (= `d0690fd` for SOURCES) | Δ |
|---|---|---|---|
| rows | 36 | 38 | +2 (S037, S038) |
| tier A / B / C | 31 / 4 / 1 | 33 / 4 / 1 | +2 A |
| status mined / rejected / queued | 34 / 2 / 0 | 36 / 2 / 0 | +2 mined |
| W-codes | W04 S033 | W04 S033 | none new |
| E-codes | none | none | none |
| missing registry | 0 | 0 | — |
| census / validate / overdue exit | 0 / 0 / 0 | 0 / 0 / 0 | — |

Commands: `git clone -q --no-hardlinks <lane> <clone>` then `git checkout -q --detach <rev>` for each base; exit codes above. Lesson claim "Rows 36 → 38" (`corpus/lessons/round-19.md:47`) matches. Claims.json `frontier_step` ("36 rows, W04 S033") matches [OBS].

### 3.2 Row-level comparison, all 36 pre-existing rows

Method: extract `| S### |` rows from both revisions, join on id, compare cells 5 (tier), 6 (scope), 9 (status), 10 (opened), 11 (recheck), 12 (used-by). Output: `base rows=36 tip rows=38`; `unchanged_rows=36`; the only differences are the two new rows (`MISSING` on the base side). Also `git diff --stat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 5e364bd5e6016f030a04b4b8c81830477ebdaf51 -- corpus/SOURCES.md` → `corpus/SOURCES.md | 3 +++`, 1 file changed, 3 insertions, 0 deletions (hunks `@@ -40,6 +40,8 @@` (+2 rows) and `@@ -68,0 +71 @@` (+1 search-log line)). An earlier `git diff --numstat` attempt used a mistyped baseline hash and exited 128; it is not evidence.

Conclusion **[OBS]**: no status, recheck, used-by, opened, tier or scope change to any of S001–S036. Only additions.

### 3.3 New rows

| id | status | opened | recheck | tier | kind | used-by (as filed) |
|---|---|---|---|---|---|---|
| S037 | mined | 2026-10-20 | on-release | A | dataset | `corpus/lessons/round-19.md`, `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` |
| S038 | mined | 2026-10-20 | 180d | A | dataset | `corpus/lessons/round-19.md`, `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` |

Search-log entry `corpus/SOURCES.md:71` (round 19) matches the rows: "Identified 4, screened 4, included 2 (S037, S038), excluded 2 as separate rows … Rejected: rea-agents 6.6.0 (registry E404)". **[OBS]** `GET https://registry.npmjs.org/rea-agents/6.6.0` → HTTP 404 (§7.1).

Paths/Leads: S037 and S038 appear in no `## Paths` route (`corpus/SOURCES.md:46–57`) and no Leads entry (`:73–81`). **[INF]** Not a gate requirement; S038 is provenance-only, so omission is defensible. Optional, no correction proposed.

### 3.4 used-by reverse-index check (round-19 citing files)

Grounding determined by reading the citing text, not by regex. Regex over-matched; the arc3 addendum explicitly names S001, S002, S003, S023 as *not* bearing (`corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md:48`) and S025 as *not grounded* (`:46`).

| Citing file (round 19) | Grounding rows (cited as grounding) | Row used-by lists the file? |
|---|---|---|
| `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` (header line 1: "source: S038 …, S035 …, S023 …, S003 …") | S038, S035, S023, S003 | S038 yes; **S035 no, S023 no, S003 no** |
| `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` round-19 addendum (`:36` "Grounded by existing rows": S024 `:40`, S026 `:41`, S031 `:42`; S037 `:71`) | S024, S026, S031, S037 | S037 yes; **S024 no, S026 no, S031 no** |
| `corpus/lessons/round-19.md` (Gate table `:28`; quotes `:40–43`) | S037, S038 | yes for both (S037, S038 used-by list the lesson) |

Precedent **[OBS]**: round 18 appended the r18 knowledge file to used-by of S003, S023 and S035 (`git show 5e364bd:corpus/SOURCES.md` lines 9, 29, 41 each end `…2026-10-20-r18-swiss-map-replay.md`). Round 14 did the same for S003 and S004 (tip lines 9–10 both list `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`). Round 19 deviated without a recorded decision.

Not missing (correctly excluded): S001, S002, S003 (for the arc3 file), S023 (for the arc3 file), S025 (addendum `:46` "not grounded").

---

## 4. Gate behaviour on the tip (the blind spot)

- 4.1 Tip validate exit 0 (§2) with the six reverse links absent. **[OBS]**
- 4.2 Canonical lane validate exit 0 (§2). **[OBS]**
- 4.3 Negative control on a copy with one used-by path typo: `validate --file <neg>/corpus/SOURCES.md` → exit 1, `E11 S003 missing used-by corpus/knowledge/2026-10-20-r19-go125-toolchain-replya.md`. **[OBS]** So E11 is live for existing paths, not for missing reverse links.

---

## 5. Exact corrections (proposed; none applied to LANE)

### 5.1 SOURCES.md — append used-by entries in place (6 rows, 6 cells)

Rule: append to the existing used-by cell (comma-separated, keep order), touch no other cell. Line numbers at tip `5e364bd`; identical blob at `d0690fd`.

| Line | Row | Current last used-by entry | Append |
|---|---|---|---|
| 9 | S003 | `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` | `, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` |
| 29 | S023 | `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` | `, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` |
| 30 | S024 | `corpus/lessons/round-17.md` | `, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` |
| 32 | S026 | `corpus/lessons/round-17.md` | `, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` |
| 37 | S031 | `corpus/lessons/round-17.md` | `, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` |
| 41 | S035 | `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` | `, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` |

Do **not** add the arc3 file to S025 (addendum `:46` says not grounded), S001, S002, S003 or S023 for that file (addendum `:48` says not bearing). Do **not** add the r19 file to S024, S026, S031 (it does not cite them).

Gate effect (proven in §6): status/tier/opened/recheck unchanged; census still 38 rows, A33/B4/C1, mined36/rej2; validate exit 0; no new codes.

### 5.2 round-19 lesson — correct the registry-change statement

`corpus/lessons/round-19.md:47` (tip `5e364bd`; `d0690fd` same line number, since the lesson's added lines are later in the file):

Current: `- New rows S037 (tier A, dataset) and S038 (tier A, dataset), both \`mined\`. Rows 36 → 38. No in-place change to S001–S036.`

Proposed: `- New rows S037 (tier A, dataset) and S038 (tier A, dataset), both \`mined\`. Rows 36 → 38. No status, opened, recheck, tier or scope change to S001–S036. used-by appended in place for S003, S023, S035 (round-19 Go 1.25 replay entry) and S024, S026, S031 (round-12 addendum source rows); named correction R19-USEDBY-APPEND.`

### 5.3 Optional (no correction required)

- `corpus/SOURCES.md` `## Paths` (`:46–57`): S037/S038 have no route line. Optional one-liner if the L1 wants them findable: `- Package and carrier identity — S037 (rea-agents@6.7.0 publish identity), S038 (go1.25.0 archive digest): identity and provenance only; they do not establish runtime behaviour or recovery quality.`
- `PROVINCE.md:9,16–20,44–45` and `SKILL.md:19–20` carry the 6.7.0 pin statements (C2 rewrites). None of them cites S037 (`git grep -c S037 5e364bd -- PROVINCE.md SKILL.md` → exit 1, no match). The pins are backed by config files and the npx cache (`PROVINCE.md:19–20`), not the registry. **[INF]** Adding PROVINCE/SKILL to S037 used-by is only needed if the L1 wants S037 to back those statements. Not required.
- S038 recheck `180d` vs S037 `on-release`: **[INF]** a policy choice; the archive digest is immutable, so either is defensible. No change proposed.
- `.ufo/waves/round-19/claims.json:28` (C3 sourced) names `S034/S035/S023`; the amendment at `:41` corrects it to `S035/S023/S003`. The r19 knowledge header (line 1) is consistent with the amendment. S034 is not cited by the r19 entry. Append-only record; no action.

---

## 6. Mutation test (own clone, observed base `5e364bd`)

Clone: `c-prop` (`git clone --no-hardlinks <lane>`; `git checkout -q --detach 5e364bd…`; HEAD verified). Applied §5.1 (six cells) with a scripted, asserted replacement in the scratch clone only (asserts each row's last used-by entry before appending; asserts the new path absent beforehand).

| Step | Result |
|---|---|
| apply | `mutant applied rows: ['S003', 'S023', 'S024', 'S026', 'S031', 'S035']`, exit 0 |
| `git diff --stat` | `corpus/SOURCES.md | 12 ++++++------`, 6 insertions / 6 deletions, one file |
| census | rows 38, A33 B4 C1, mined 36, rejected 2; exit 0 |
| validate | `W04 S033` (pre-existing) + `ok`; exit 0 |
| overdue | 0 overdue; exit 0 |
| reverse-index (§3.4) after mutant | S003, S023, S024, S026, S031, S035 each list the r19 or arc3 file |

Negative control (`c-neg`, copy of `c-prop` with one typo in an appended path): validate exit 1 with `E11`, as in §4.3. `c-neg` removed.

Scope check: a validate-level gate that compared used-by to citing files would flag the tip; the current gate does not (§4.1). No gate change is proposed here (out of scope for a freshness/depth seat; the lane owner decides).

---

## 7. Freshness of new rows (live, fetched 2026-10-20T19:16:36Z)

### 7.1 S037 — `rea-agents@6.7.0` npm registry

Commands (all in `$T/npm/`; `curl -fsS` exit 0 each): `GET https://registry.npmjs.org/rea-agents/6.7.0` (exit 0), `GET https://registry.npmjs.org/rea-agents` (packument, exit 0), `GET https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0` (exit 0), tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz` (6,276,963 bytes, exit 0).

| Claim (S037 row / lesson) | Observed | Result |
|---|---|---|
| `dist.integrity` `sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==` | same string; recomputed sha512 of the tarball equals it | match |
| `dist.shasum` (lesson does not quote) | `11f23ba377303a5c28b3162180cf2bf3f3643708`; recomputed sha1 equal | match |
| packument `time["6.7.0"]` `2026-10-18T08:12:05.640Z` | same; substring present verbatim in packument | match |
| `dist-tags.latest` = 6.7.0 | `{'latest': '6.7.0'}` | match |
| `6.6.0` not published | not in `versions`; `GET …/rea-agents/6.6.0` → HTTP 404 | match |
| SLSA predicate `https://slsa.dev/provenance/v1` | present (also an `npm publish v0.1` predicate, empty resolvedDependencies) | match (row cites SLSA only) |
| `resolvedDependencies[0].digest.gitCommit` `27dc42d10249f0410904a75c0997842eb03b931c` | same; URI `git+https://github.com/morluto/rea@refs/heads/release/6.7.0` | match |
| S037 `teaches`: "release-workflow commit" | `externalParameters.workflow.path` = `.github/workflows/release.yml`, `ref` = `refs/heads/release/6.7.0`, builder `https://github.com/actions/runner/github-hosted` | match |
| subject sha512 | attestation subject sha512 `ca1231da…a117` (not recomputed; row does not claim it) | not checked |

Scope statement ("not the package's runtime behaviour") is correct. The row claims identity and provenance only.

### 7.2 S038 — go1.25.0 linux-amd64 archive and carriers

Commands: `GET https://go.dev/dl/?mode=json&include=all` → `dl.json` (82,604 lines, pretty-printed; exit 0). `GET https://go.dev/dl/go1.25.0.linux-amd64.tar.gz` (59,659,213 bytes; exit 0). `tar -tzf` / `tar -xzf` for the nine carrier members (exit 0).

| Claim | Observed | Result |
|---|---|---|
| go1.25.0 `stable` true; file `go1.25.0.linux-amd64.tar.gz`; sha256 `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`; size 59659213; kind archive | same, one go1.25.0 entry; filename at `dl.json:14644`, sha256 at `:14648` | match (lesson "line 14644" matches) |
| `curl …tar.gz` re-hashes to the same sha256 | `sha256sum` = `2852af0c…b613`; `stat` 59,659,213 bytes | match |
| nine carrier binaries hash identically to archive members | 9/9 MATCH: `bin/go` `b93cdfdbc72f1afc3f21498c80bf3d155a44a9b95e2d690c940511051574bc25`, `bin/gofmt` `2aa4122abbd1593ee7c9e184366feef7cb06e52ce790b5ef2119e8aee8640a80`, `pkg/tool/linux_amd64/{asm,cgo,compile,cover,link,preprofile,vet}` (all MATCH; digests printed by the `sha256sum` loop) | match |

Carriers were hashed (read-only `sha256sum`) and never executed. **[OBS]**

Scope statement ("not the Go 1.26 or 1.27 release train") is correct.

### 7.3 Lesson quotes (`corpus/lessons/round-19.md:40–43`)

- `"integrity":"sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw=="` — verbatim in fetched version doc. **match**
- `"2026-10-18T08:12:05.640Z"` — verbatim at `"6.7.0":"2026-10-18T08:12:05.640Z"` in packument. **match**
- `"filename": "go1.25.0.linux-amd64.tar.gz",` — my copy `dl.json:14644`. **match**
- `"sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613",` — my copy `dl.json:14648`. **match**

Knowledge file `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:15` ("W1 `SourcesRowsDraft.md` re-downloaded it and matched all nine listed binary members") is reproduced by §7.2. **match**

---

## 8. Quotes of the new rows (tip `5e364bd`, `corpus/SOURCES.md:43–44`)

Full cells, each on its own line, as filed:

S037 — source: `rea-agents 6.7.0 npm registry record — https://registry.npmjs.org/rea-agents/6.7.0 (tarball https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz; packument https://registry.npmjs.org/rea-agents)`
S037 — kind `dataset`; tier `A`; scope `Publish identity and integrity of rea-agents@6.7.0 as served by the npm registry, with its SLSA provenance source commit; not the package's runtime behaviour`
S037 — anchor `Version document dist.integrity, dist.shasum, dist.attestations; packument time["6.7.0"], dist-tags.latest; attestation https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0, predicate https://slsa.dev/provenance/v1, resolvedDependencies[0].digest.gitCommit 27dc42d10249f0410904a75c0997842eb03b931c; fetched 2026-10-20`
S037 — teaches `Pins the 6.7.0 tarball by its sha512 and release-workflow commit, so a client pin can be checked against the registry's own digest before any package code runs.`
S037 — status `mined`; opened `2026-10-20`; recheck `on-release`; used-by `corpus/lessons/round-19.md, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`

S038 — source: `Go release list JSON, https://go.dev/dl/?mode=json&include=all, entry go1.25.0 linux-amd64 archive`
S038 — kind `dataset`; tier `A`; scope `The official go1.25.0 linux-amd64 archive digest and size, against which the installed 1.25.0 carrier binaries are matched; not the Go 1.26 or 1.27 release train`
S038 — anchor `Endpoint JSON, version go1.25.0 with stable true, file go1.25.0.linux-amd64.tar.gz sha256 2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613 size 59659213; fetched 2026-10-20; curl -fsSL https://go.dev/dl/go1.25.0.linux-amd64.tar.gz re-hashed to the same sha256`
S038 — teaches `Gives an independent digest for the toolchain: nine carrier binaries under /home/vgpnk/.local/opt/go-1.25.0 hash identically to the same members extracted from that archive.`
S038 — status `mined`; opened `2026-10-20`; recheck `180d`; used-by `corpus/lessons/round-19.md, corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`

Both rows: 13 fields after `|` split (NF=13, §2 E01 clean).

---

## 9. Findings list (ordered)

1. **F1 (depth/traceability, medium): used-by missing six round-19 citations** (S003, S023, S035 ← r19 Go 1.25 entry; S024, S026, S031 ← r12 addendum). Exact fix §5.1; proven §6. Gate-invisible (§4). Root cause: the round-19 lesson's "no in-place change" wording (`round-19.md:47`) was applied to status/recheck/opened without checking the used-by reverse index.
2. **F2 (gate blind spot, low): E11 checks existence only.** Not fixed here. Note for the L1: any future round can repeat F1 with validate exit 0.
3. **F3 (calibration, none): new rows are scoped tightly and reproduce.** S037 and S038 match live registry and go.dev data; the nine carriers match archive bytes. No overclaim found in the rows or the lesson quotes.
4. **F4 (optional): S037/S038 not in `## Paths`; PROVINCE/SKILL pin statements do not cite S037.** No correction required (§5.3).
5. **F5 (process): main moved 5e364bd → d0690fd during this audit**; SOURCES blob unchanged; lesson `round-19.md` changed (+27/−1) but not its registry paragraph. Re-check §5.2 against the lesson's current text before applying.
6. **F6 (process): uncommitted lane edit** to `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` (+7 lines: vet `analyze.json` binding paragraph). Not analysed; does not change any registry cell or source header line. Note the L1 should re-check used-by after it commits.

---

## 10. Commands run (exit codes)

| Command | Exit |
|---|---|
| `git rev-parse refs/heads/main` (start) | 0 (`5e364bd…`) |
| `git clone -q --no-hardlinks <lane> <clone>`; `git checkout -q --detach <rev>` (×2, base and tip) | 0, 0 (HEAD verified) |
| `sha256sum scripts/sources-census.sh` | 0 (`3fb72615…`) |
| `sources-census.sh census|validate|overdue --file <clone>/corpus/SOURCES.md --today 2026-10-20` (base, tip) | 0 each |
| `git diff --no-ext-diff -U0 8a8da7e 5e364bd -- corpus/SOURCES.md` | 0 |
| row-level join (base vs tip) | 0 (`unchanged_rows=36`) |
| `sources-census.sh selftest` | 0 (`selftest ok`, 96 killed, 0 survived) |
| canonical `census kaidoku --root …` / `validate kaidoku --root …` (lane working tree) | 0, 0 |
| `git -C <lane> status --short -- corpus/` | 0 |
| `git -C <lane> diff --quiet refs/heads/main -- corpus/SOURCES.md` | 0 (identical) |
| `GET rea-agents/6.7.0`, packument, attestation, tarball | 0 each |
| `GET rea-agents/6.6.0` | HTTP 404 |
| `GET go.dev/dl/?mode=json&include=all`; `GET go1.25.0.linux-amd64.tar.gz` | 0, 0 |
| `tar -tzf`/`tar -xzf` nine carrier members; `sha256sum` ×9 installed + ×9 archive | 0; 9/9 MATCH |
| mutant apply (`c-prop`) + census/validate/overdue | 0, 0, 0 |
| negative control (`c-neg`) validate | 1 (E11 expected) |
| `git grep -c S037 5e364bd -- PROVINCE.md SKILL.md` | 1 (no match) |

Installs/updates: **none** (curl, python3 stdlib, tar, sha256sum, git, bash were already present). Scratch files in `/tmp/kr19-w2-SourcesGate.RxjSPx` only.

No LANE writes beyond this report. No git writes in LANE. No REA/Ghidra use. No carrier executed.
