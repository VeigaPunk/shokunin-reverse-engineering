# ConnSiblings — round-31 sibling-overlap scan

Seat: `KaidokuR31.ConnSiblings` (connector, leaf). Item: sibling-overlap scan for round 31
(SQLite database inspection, REA `inspect_sqlite_database` / CLI `inspect-sqlite-database`).
Lane base `c369242fee9f559f895e3f7956b1242076c7b1be`; freeze `35ba7c522dba55f9be27eb161d4254eacaa24330`.
Timezone UTC, 2026-10-23. Read-only everywhere: no git/jj write, no REA run, no install, no lane
write except this file; the fleet repo and all 20 sibling lanes were only read.

## 0. Answer

- **No sibling lane holds knowledge of REA's SQLite reader.** `inspect_sqlite_database` and
  `inspect-sqlite-database` have **0 hits** in every tracked and untracked non-ignored file of all
  20 sibling lanes, in either spelling (`git grep` working tree, 04:18:37–04:19:11Z; committed HEAD,
  04:25:32–04:25:39Z). No sibling file is named for the verb; two working-tree names contain
  "sqlite" (kumitate's WAL-source scout report and a vendored `@types/node/sqlite.d.ts` inside a
  kagi sandbox), neither is REA ground.
- **Six lanes hold adjacent SQLite ground worth cross-referencing** (kagi, kumitate, tameshi,
  kengaku, tsukuroi; plus tabi as the lane-boundary witness). None of it duplicates or contradicts
  what round 31 will claim *about REA*, because all of it is about the host `sqlite3` CLI, the
  SQLite file format/WAL docs, or another lane's own gate.
- **No sibling conflict.** The one contradiction found is *inside kaidoku*: R31-C1's surface prose
  "a verb the lane has never run or named" is false at the base — the lane ran and named it on
  2026-10-16 (`corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md`, live 6.5.0 call,
  Evidence `ev_7572e622…`). A sibling artifact (tabi round-17 `AdjRow2.md:52`) cites that same
  base entry, which is how the scan surfaced it; the in-wave critics already report the same
  contradiction (`CriticAxisFitC1.md:15`, `CriticAxisFitC2.md:63-79`). This scan adds the
  cross-lane witness and the sibling-boundary consequence, not a new defect.
- **Two grep collisions to expect:** "Chinook" in kotodama is *Chinook Jargon* (a contact language);
  "GeoPackage" in kotoba is the MIME token `application/geopackage+sqlite3` inside an OMP strings
  dump, not GeoPackage work.

## 1. Method and coverage

Lanes scanned (20, kaidoku excluded): audio, chousa, game-dev-2d, game-dev-3d, kagi, kake, kama,
kasegi, kengaku, kotoba, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi,
tsukuroi — all `*-shokunin` directories under `/home/vgpnk/Projects/shokunin`.

| # | Command (abridged) | Result | Exit | UTC |
|---|---|---|---:|---|
| M1 | `grep -rIl -i --include=*.md sqlite /home/vgpnk/Projects/shokunin/*-shokunin/corpus 2>/dev/null \| grep -v kaidoku \| head -50` | **39 files** | 0 | 04:19:57 |
| M2 | `grep -rIn -i --include=*.md -E 'sqlite\|inspect[-_]sqlite[-_]database\|proj\.db\|geopackage\|chinook' …/corpus \| grep -v '^./kaidoku'` | **113 lines / 42 files** | 0 | 04:19:57 |
| M3 | per lane: `git -C <lane> grep -I -i -l --untracked -E 'inspect[-_]sqlite[-_]database\|proj\.db\|geopackage\|chinook'` | only kotoba 1, kotodama 3, tabi 1; 17 lanes 0 | 0/1 | 04:18:37–04:19:11 |
| M4 | per lane: same pattern, committed `HEAD` | same set (tabi 1, kotoba 1, kotodama 3) | 0/1 | 04:25:32–04:25:39 |
| M5 | per lane: `git grep -i sqlite HEAD -- PROVINCE.md SKILL.md SCORECARD.md README.md` | kagi 7, kotoba 1, kumitate 1, tameshi 1; 16 lanes 0 | 0/1 | 04:23:1x |
| M6 | per lane: `git ls-files \| grep -ci sqlite` | 1 committed name: `kumitate-shokunin/.ufo/waves/round-44/controls/ScoutSqliteWal.md` | 0 | 04:23:16 |
| M7 | per lane: `{ git ls-files; git ls-files --others --exclude-standard; } \| grep -i sqlite` | 2 working-tree names: kumitate `ScoutSqliteWal.md`; kagi `.ufo/waves/round-28/sandboxes/SrcNodeSemver/node_modules/@types/node/sqlite.d.ts` | 0 | 04:25:32–04:25:39 |

Two unbounded recursive greps over the whole sibling trees were launched before M3/M4 and **timed
out at the 300 s cap** (jobs `bg_5853`, `bg_5854`, `bg_6101`); they were replaced by the per-lane
`git grep` pair, which covers every tracked file plus untracked non-ignored files in each working
tree. Gitignored files were not scanned. No external source was opened; every quote below is from
a local file at a stated line.

## 2. Hit list

### 2.1 Corpus (sibling `corpus/` at working tree; line numbers from M2)

Format: `path: lines — gloss`.

**kagi (11 files, 45 lines) — the one lane with real SQLite read-path ground**
- `kagi-shokunin/corpus/knowledge/surface-census.md: 5,7,66,67,91,114,116,117,131,135,231,260,261,278,304` — census contract: `SQLite format 3` magic (16 bytes, NUL-exact), mode/table/row floors, fail-closed `UNVERIFIED` on missing `sqlite3`, snapshot read via `file:…?mode=ro` on a copy (a read-only open of the live file still touches `-shm`), two-pass `sqlite_master` then counts, selftest cases incl. prefix-without-NUL.
- `kagi-shokunin/corpus/knowledge/handler-on-disk-state.md: 8,31,77,186,211,213,214,215,217,218` — transcript DB (`opencode.db`), §"Read-side gotcha": any `sqlite3` open (even `?mode=ro`) creates the 0600 `-wal`/`-shm` siblings; mtime not part of the bound.
- `kagi-shokunin/corpus/knowledge/transcript-hygiene.md: 4,87,104,146,147` — `file:…?immutable=1` read gate; plain `sqlite3`/`-readonly` mutates sidecars; credential-table count.
- `kagi-shokunin/corpus/knowledge/control-plane-hardening.md: 142,144,145` — `sqlite3 -readonly` row/`PRAGMA table_info(session)` probes.
- `kagi-shokunin/corpus/knowledge/claim-ledger.md: 99` — "a sqlite row floor" as a ledger-row example.
- `kagi-shokunin/corpus/lessons/round-10.md: 26,45,63,105`; `round-8.md: 33`; `round-21.md: 13`; `round-8-aggregator-box3-coldrun.md: 22`; `round-11.md: 160` (deny-list word removal: "`sqlite3`/`timeout` dropped from the [list]") — census lessons, fail-closed arm, read-side drift.
- `kagi-shokunin/corpus/README.md: 42,48,50` — index rows for the census contract and DB introspection.

**kumitate (6 files, 20 lines) — SQLite sidecar lifecycle**
- `kumitate-shokunin/corpus/knowledge/omp-agent-root.md: 1,22,44,45,53` — §"SQLite sidecars": `-wal`/`-shm` exist while open and are normally deleted on last close; `-journal` is a rollback journal and is *not* declared.
- `kumitate-shokunin/corpus/SOURCES.md: 67,68,69,71` — S054 `sqlite.ts`, S055 credential store, S056 sqlite.org/wal.html (pinned, quote), S058 incident.
- `kumitate-shokunin/corpus/lessons/round-44.md: 17,64,66,68,69,76`; `round-44-verifier-spotcheck.md: 151,152`; `README.md: 92` — source admission of S056 (WAL doc, sha256 `f3467b53…`), census gate.
- `kumitate-shokunin/corpus/knowledge/route-probe-cluster.md: 100,500` — "never reads SQLite" comment pin.

**kotoba (13 files, 28 lines) — host `sqlite3 -readonly` as a measurement tool**
- `kotoba-shokunin/corpus/knowledge/opencode-offer-trace-round8.md: 4,95,100,103,105,107,111,113,115,119` — `.tables` and count queries on `opencode.db`.
- `claim-census-round12.md: 79,97,99`; `claim-scope-audit-round9.md: 72`; `harness-router-models-round9.md: 19,95`; `skill-activation-telemetry.md: 52,70`; `trigger-miss-proxy-round6.md: 5`; `render-mechanism-round7.md: 93`; `harness-independent-round37.md: 8`; `harness-verifier-round10.md: 11`; `checklist-execution-round15.md: 160`; `lessons/round-5-aggregator-audit.md: 39`; `round-6-aggregator-audit.md: 32,38`; `round-8-aggregator-box3-coldrun.md: 11,22` — all CLI reads/counts, no schema parse, no REA.

**tameshi (3 files, 10 lines) — verification craft over kagi's SQLite gate**
- `tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md: 73,92,134,203,268` — B7 `sqlite-unavailable` exact-count kill, B6 magic-length NUL probe, floor-boundary semantics, U5 host/toolchain dependence.
- `tameshi-shokunin/corpus/knowledge/arm-class-matrix.md: 117,292` — the "cannot measure" species is `sqlite-unavailable` → exit 1 `SHAPE UNVERIFIED`.
- `tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md: 214,218,305` — `SQLITE3_BIN` override and sqlite-backed fixtures.

**kengaku (4 files, 4 lines) — method, not SQLite content**
- `kengaku-shokunin/corpus/evidence/round11-fleet/r11-connector.md: 59` — duplicate-construction ruling; explicitly notes kagi's checkpoint keyword hit is SQLite WAL/checkpoint handling, not model generation.
- `round10-fleet/r10-connector.md: 41` — kagi `transcript-scan.sh` connector row.
- `round12-fleet/r12-endpoint-freshness.md: 526` — grok `index.sqlite` endpoint artifact.
- `knowledge/bench-arena-round7-noise-n25.md: 24` — `sqlite3.OperationalError` in a failed run.

**tsukuroi (2 files, 3 lines) — package/substrate only**
- `tsukuroi-shokunin/corpus/knowledge/aur-risk-plane.md: 180` — `depends=(sqlite)` in an AUR entry.
- `update-safety-note.md: 38,304` — sqlite listed among packages that can break rebuilds.

**kotodama (3 files, 3 lines) — collision only**
- `kotodama-shokunin/corpus/knowledge/civilizations/pacific-northwest.md: 50` — "Chinook Jargon/Chinuk Wawa is a contact language".
- `linguistics/morphological-typology.md: 79`; `lessons/round-1-triage/L4.md: 18` — same contact-language material.

### 2.2 Non-corpus material hits (outside `corpus/`)

| Path:line | What it holds | Relation to round 31 |
|---|---|---|
| `kagi-shokunin/SKILL.md:44` | Decision-table refuse: "`sqlite3` without `file:…?immutable=1` (mutates `-wal`/`-shm` in the live dir)" | Cross-reference for the `wal` field and journal family; the general hazard. |
| `kagi-shokunin/SKILL.md:506-508` | "Querying the transcript DB with plain `sqlite3 <db>` or `-readonly` — it creates/updates 0600 `-wal`/`-shm` siblings"; use `immutable=1` or a copy | Same. |
| `kotoba-shokunin/.ufo/round-21/scouts/F1.md:123` | "`/tmp/f1probe/db_copy.db-shm` / `-wal` sidecars created by sqlite stayed in `/tmp`" | Independent corroboration that a SQLite open creates sidecars. |
| `kumitate-shokunin/.ufo/waves/round-44/controls/ScoutSqliteWal.md:1-48` | WAL/tempfiles docs pinned by HTTP 200 + sha256 (`wal.html` `f3467b53…`, `tempfiles.html` `b9c7f358…`); quotes on sidecar lifetime | Source record for `-wal`/`-shm` lifetime if the entry explains the `wal` field. |
| `tsukuroi-shokunin/.ufo/waves/round-24/w1/ExecMirrorTimestamps/host-core-pkglist.txt:268-271` | `sqlite 3.54.0-1`, `sqlite-analyzer`, `sqlite-doc`, `sqlite-tcl` | Matches C1's stated oracle substrate (system libsqlite3 3.54.0). |
| `tabi-shokunin/.ufo/waves/round-17/w2/AdjRow2.md:52` | Cites kaidoku `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:14` ("forensic recovery …") | The cross-lane witness to the in-lane prior art; see §4. |
| `tameshi-shokunin/.ufo/evidence/kaika-round-1/coldread/B-control.txt:9-11` | `ok-case 08 sqlite-magic`, `09 sqlite-magic-prefix-only`, `10 sqlite-unavailable` | Prior test-craft for the same edge classes (magic, prefix-only, no reader). |
| `mado-shokunin/.ufo/waves/round-17/w1/reports/SiblingOverlap.md:92,189-191` | Its own per-sibling disposition table ("do not absorb") | Format precedent for this report, not SQLite knowledge. |
| `kotoba-shokunin/.ufo/round-44/evidence/omp-live-18.12.2-strings.txt:160980` | MIME token `application/geopackage+sqlite3` in an OMP strings dump | Grep collision, not GeoPackage work. |
| `souji-shokunin/census/round-4/seat-02.json:5,61,116,203` | Third-party `obsidian-cli-inspector` (Rust/SQLite) and its `vault.db` | A different inspector, not REA; no overlap. |

Incidental, no knowledge bearing: `kama` `.ufo/waves/round-15/*` lists `sqlite` among blocked paths;
`game-dev-2d` `reports/round-103/mutations/r103-ver8-review.py:59` lists `sqlite3` as a blocked
module; `mori` `.ufo/waves/round-24/w2/CriticC1Admission.md:171` used `/usr/bin/sqlite3` read-only;
`kumitate` `.ufo/pins/anchor-truth.json:5783` is the word "SQLite" in a route-probe comment;
`kengaku` `.ufo/waves/round-28/scratch/**` are sandbox replicas of its own corpus.

## 3. Overlap verdict per sibling

`none` = no knowledge this round would duplicate or contradict and nothing to cross-reference;
`cross-reference` = the lane holds ground the round's entries should name; `conflict` = the lane
asserts something the round would contradict (or vice versa). No lane earns `conflict`.

| Sibling | Corpus files/lines | Verdict | Detail |
|---|---|---|---|
| audio | 0 / 0 | none | no SQLite surface. |
| chousa | 0 / 0 | none | research method only; no SQLite content. |
| game-dev-2d | 0 / 1* | none | one blocked-module list contains the string `sqlite3`. |
| game-dev-3d | 0 / 0 | none | no hits. |
| **kagi** | **11 / 45** | **cross-reference** | The fleet's only SQLite read-path ground: 16-byte NUL-exact magic, read-only open mutates `-wal`/`-shm`, `immutable=1` blind window, two-pass catalog read, fail-closed `UNVERIFIED`. Cite it for the `wal` field, magic edge and "no reader" species; it is a host CLI gate, not REA, so it neither duplicates nor contradicts the REA claim. |
| kake | 0 / 0 | none | no hits. |
| kama | 0 / 3* | none | safety advice lists `sqlite` among blocked paths; no SQLite knowledge. |
| kasegi | 0 / 0 | none | no hits. |
| kengaku | 4 / 4 | cross-reference (method) | `r11-connector.md:59` is the duplicate-construction ruling this scan imitates, and it records that kagi's checkpoint hit is SQLite WAL handling; `r12:526` mentions a grok `index.sqlite`. No REA or schema ground. |
| kotoba | 13 / 28 | none | Uses `sqlite3 -readonly` as a measurement tool on two host DBs; no schema parse, no REA, no L1 work. Its `F1.md:123` sidecar observation corroborates kagi but is not a citation target for the entries. |
| kotodama | 3 / 3 | none | "Chinook" is Chinook Jargon; no database material. Naming caution only. |
| **kumitate** | **6 / 20** | **cross-reference** | `omp-agent-root.md:53-58` + `SOURCES.md:69` (S056) is the fleet's pinned ground for `-wal`/`-shm` lifetime and for `-journal` being a *distinct* rollback journal. Cite it if the entry explains the `wal` field or the journal family; do not merge WAL and rollback-journal semantics. |
| lore | 0 / 0 | none | no hits. |
| mado | 0 / 9* | none | Its round-17 `SiblingOverlap.md` is a format/method precedent, not SQLite knowledge. |
| mori | 0 / 3* | none | one round used `/usr/bin/sqlite3` read-only for table listing; incidental. |
| revenger | 0 / 0 | none | No SQLite ground. Named only as a co-route in tabi's refusal. |
| souji | 0 / 63* | none | `obsidian-cli-inspector` is a third-party SQLite-backed tool; different inspector and subject. |
| **tabi** | 0 / 1* | **cross-reference** | `AdjRow2.md:52` cites kaidoku's l7-04 and `PROVINCE.md:15` refuses "reverse engineering as forensics (→ revenger/kaidoku)". Boundary for the entries: offline and bounded, never "forensic recovery". |
| **tameshi** | **3 / 10** | **cross-reference** | Mutation case over kagi's census pins the exact edge classes round 31 predicts: NUL-magic length (B6), symlink arm (B4), `sqlite-unavailable` as an exit-1 verdict (B7/case 10). Cite as prior test-craft; the round's mutants are data mutants, not code mutations, so no method duplication. |
| **tsukuroi** | 2 / 3 | **cross-reference (substrate)** | Host package record `sqlite 3.54.0-1` corroborates C1's "system libsqlite3 3.54.0" limit; otherwise package/update-safety only. |

`*` = non-corpus hits only, counted in M3/M5; they do not enter the corpus totals.

## 4. The one contradiction (lane-internal, witnessed by a sibling)

**Claim vs base.** R31-C1's `surface` says the operation is "a verb the lane has never run or
named". At base `c369242f`, `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md` records a
live `rea-agents@6.5.0` call with `inspect_sqlite_database({"path":…})` on a hash-pinned pnpm index
copy, Evidence `ev_7572e622b7b3c5c281d3eae0d48282690c6f0b78ab8aae5a550bda07f93d6f9a`, and the
result `wal:null`, one `package_index` table, `rows:null` (`:5,9,11`). It is indexed in
`corpus/README.md:65` (and `:163`), and its limitations line already says "forensic recovery …
outside scope" (`:14`). `2026-10-16-l8-01-6p4-symmetry-battery.md:12` names the tool in the 6.4.0
"Tool not found" battery.

**Exact base counts (both spellings).**

```
$ git grep -I -c 'inspect_sqlite_database' c369242f -- corpus
c369242f:corpus/README.md:2
c369242f:corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:3
c369242f:corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md:1
$ git grep -I -l 'inspect-sqlite-database' c369242f -- PROVINCE.md SKILL.md corpus/knowledge
(no output, exit 1)
$ git grep -I -c -i 'sqlite' c369242f -- PROVINCE.md SKILL.md
(no output, exit 1)
```

So the frozen `unmoved_command` is literally true only for the **hyphenated CLI spelling in three
paths**; the lane's corpus names and ran the **tool spelling** before the base. `PROVINCE.md` and
`SKILL.md` were and are clean (0 `sqlite` lines), which is the honest coverage delta: first
PROVINCE Core row plus first CLI use, not first contact.

**Sibling witness.** tabi's round-17 adjacency audit re-pinned kaidoku `PROVINCE.md:3` and quoted
the lane's own sqlite entry in its issue I1:

```
tabi-shokunin/.ufo/waves/round-17/w2/AdjRow2.md:52:
  not forensic"; `corpus/knowledge/2026-10-16-l7-04-inspect-sqlite-database.md:14` "forensic recovery …
```

`tabi-shokunin/PROVINCE.md:15`: `**Refuses:** reverse engineering as forensics (→ revenger/kaidoku),`.
No other sibling cites l7-04 (per-lane `git grep 'l7-04' HEAD` at 04:23:1x: only tabi, 1 line).

**Status.** Already reported in this wave by `CriticAxisFitC1.md:15` ("fails … names and runs
`inspect_sqlite_database`") and `CriticAxisFitC2.md:63-79` ("prose miss, frozen command intact"),
with the smallest safe correction. This seat does not re-open it as a blocker; it records that the
prior authority is **in-lane, not sibling**, and that the sibling record (tabi) is a boundary
citation, not an ownership claim.

## 5. Proposed move (bounded, one block per entry)

Add to both round-31 entries a short **"Fleet prior art and lane boundary"** block (prose only; no
counter, prediction, carrier, envelope or frozen target changes; keep the required S096/S092
citations intact):

1. **Name the in-lane prior art and state the delta.** C1: l7-04 ran the same operation at the same
   pin by MCP on one carrier (`wal:null`, inventory without columns, `rows:null`); round 31 adds the
   CLI verb with `--schema-scope database`, 12 published carriers (PROJ/Chinook/GeoPackage), column
   completeness and index/view/trigger rows, plus the PROVINCE Core placement. C2: l7-04's own
   unknowns (`:13` "changing databases, WAL inputs, encrypted/corrupt files") are exactly the 20
   refusal rows; l8-01 supplies the 6.4.0 name-absence control.
2. **Quote the lane boundary.** tabi `PROVINCE.md:15` refuses "reverse engineering as forensics
   (→ revenger/kaidoku)" and its `AdjRow2.md:52` quotes l7-04's "forensic recovery … outside scope".
   The entries should say *offline, bounded inspection*, never forensic recovery or integrity
   verification.
3. **Distinguish WAL from rollback journal once.** Cite kumitate `omp-agent-root.md:53-58` / S056 for
   `-wal`/`-shm` lifetime and for `-journal` being a separate rollback journal. Pair kagi's
   read-side hazard (`SKILL.md:44,506-508`; `handler-on-disk-state.md:77`) with this wave's
   `SentinelContainment.md:96` observation (REA captures into a private snapshot root and opens
   sources `O_RDONLY|O_NOFOLLOW`), so the general `sqlite3` sidecar rule is not misread as an open
   risk to the committed==live full-envelope rule.
4. **Record the two grep collisions in one line** (kotodama "Chinook Jargon"; kotoba MIME
   `application/geopackage+sqlite3`) so a later fleet-wide search does not read them as prior art.

**Affected axes.** depth ↑ (the journal/WAL distinction and the 23-row delta are grounded in prior
art); calibration ↑/protected (the entries stop implying first contact and match what the frozen
command actually measures); coverage **neutral** (no carrier, request, envelope or target line
changes — the coverage target is measured by the counter, not by prose). No axis is harmed.

**Risks.** (a) The block must not delete or displace S096/S092, or `entry_ok` can flip; add prose,
keep the required citation strings. (b) Cross-lane citations are boundary/prior-art statements, not
evidence for REA behavior — do not let a sibling quote stand in for a live run. (c) Quoting kagi's
sidecar rule without the Sentinel answer invites a false open-risk reading. (d) Do not merge WAL
(`-wal`/`-shm`) with rollback-journal (`-journal`) semantics: C2's hot/short/empty/zeroed mutants
are rollback-journal cases. (e) Tabi's adjacency pin is kaidoku `PROVINCE.md:3`; this round must not
rewrite that line (it does not).

**Verification (main agent, after entries land).**
- `git grep -n 'l7-04' -- corpus/knowledge/2026-10-23-r31-*.md` returns both entries; `git grep -n
  'forensic' -- corpus/knowledge/2026-10-23-r31-*.md` shows only the negated boundary phrasing.
- `git grep -c 'S096'` / `'S092'` in the respective entries unchanged (entry gate intact).
- Both counters unchanged at the measured revision: C1 `carriers=12 pass=12 target=12 entry_ok=1
  province_ok=1`, C2 `requests=23 matches=23 target=23 entry_ok=1 skill_ok=1`, each exit 0.
- Re-run the sibling scan: `git -C <each sibling> grep -I -i -l 'inspect_sqlite_database'` stays 0.

## 6. Evidence ledger

| # | Finding | Command (abridged) | Excerpt | Exit | UTC |
|---|---|---|---|---:|---|
| E1 | 39 sibling corpus files contain `sqlite`; 113 pattern lines over 42 files | M1, M2 (§1) | `files=39`, `lines=113` | 0 | 04:19:57 |
| E2 | Only kotoba/kotodama/tabi have non-corpus four-string hits; 17 lanes zero | M3 per-lane `git grep --untracked` | `kotoba … files=1`, `kotodama … files=3`, `tabi … files=1`; all others `rc=1 files=0` | 0/1 | 04:18:37–04:19:11 |
| E3 | Zero sibling hits for either verb spelling | M3/M4 | no `inspect_sqlite_database` line in any lane | 1 (per lane) | 04:18:37–04:19:11 / 04:25:32–04:25:39 |
| E4 | SQLite-named sibling working-tree files | M6, M7 | committed: `kumitate …/ScoutSqliteWal.md`; working tree adds `kagi …/@types/node/sqlite.d.ts` | 0 | 04:23:16 / 04:25:32–04:25:39 |
| E5 | kagi read-side rule | `grep -n 'immutable=1' kagi-shokunin/SKILL.md` | ``44:… printing matched text; `sqlite3` without `file:…?immutable=1` (mutates `-wal`/`-shm` in the live dir)`` | 0 | 04:24:08 |
| E6 | kagi sidecar creation | `grep -n 'creates the 0600' …/handler-on-disk-state.md` | ``77:Any `sqlite3` open of that path **creates the 0600 `-wal`/`-shm` siblings**,`` | 0 | 04:24:08 |
| E7 | kagi live-file read touches `-shm`; magic NUL-exact; two-pass | `grep -n` on `surface-census.md` | `66: first 16 bytes compared byte-exact including the terminating NUL`; `131: A read-only open of the *live* file still`; `135: Two sqlite passes` | 0 | 04:24:08 |
| E8 | kumitate sidecar/WAL ground | `grep -n '^## SQLite sidecars' omp-agent-root.md`; `grep -n 'Usually, the WAL file' SOURCES.md` | `53:## SQLite sidecars`; `69:| S056 | … sqlite.org/wal.html` | 0 | 04:24:08 |
| E9 | tameshi prior test-craft | `grep -n 'sqlite-magic\|sqlite-unavailable' …/B-control.txt` | `9:ok-case 08 sqlite-magic`, `10:…prefix-only`, `11:…sqlite-unavailable … unverified=3` | 0 | 04:24:08 |
| E10 | kengaku duplicate-construction ruling | `grep -n 'Duplicate-construction ruling' r11-connector.md` | `59: … no round-10/11 sibling artifact already measures this design` | 0 | 04:24:08 |
| E11 | kotodama collision | `grep -n 'Chinook Jargon' pacific-northwest.md` | `50:| Contact | Chinook Jargon/Chinuk Wawa is a contact language` | 0 | 04:24:08 |
| E12 | kotoba sidecar observation / MIME collision | `grep -n 'sidecars created by sqlite' F1.md`; `grep -n 'geopackage+sqlite3' …strings.txt` | `123:…sidecars created by sqlite stayed in`; `160980:…application/geopackage+sqlite3…` | 0 | 04:24:08 |
| E13 | tsukuroi host sqlite 3.54.0-1 | `grep -n '^sqlite 3.54.0-1' host-core-pkglist.txt` | `268:sqlite 3.54.0-1` | 0 | 04:24:08 |
| E14 | tabi boundary/citation | `grep -n 'l7-04' AdjRow2.md`; `git show HEAD:PROVINCE.md` | `52: … l7-04-inspect-sqlite-database.md:14 "forensic recovery …`; `15:**Refuses:** reverse engineering as forensics (→ revenger/kaidoku),` | 0 | 04:24:08 / 04:23:1x |
| E15 | Base contradiction counts | `git grep -I -c 'inspect_sqlite_database' c369242f -- corpus`; hyphen grep over three paths | `README.md:2`, `l7-04…:3`, `l8-01…:1`; hyphen no output | 0 / 1 | 04:23:17 |
| E16 | No prior PROVINCE/SKILL SQLite surface | `git grep -I -c -i 'sqlite' c369242f -- PROVINCE.md SKILL.md` | no output | 1 | 04:23:17 |

Boundary evidence for E15/E16 is the base commit itself (`git show c369242f:…`); the entry's live
call and evidence ID are quoted from l7-04 `:5,9,11`, not re-run by this seat.

## 7. Scratch artifacts and hygiene

All under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/ConnSiblings/`:

| File | sha256 |
|---|---|
| `corpus-files.txt` (39 sqlite corpus files) | `d2a96a277cda79f248fce7cbb6d2f05d2cabe2d3f39ec9a0a465d1bc2b37c9ed` |
| `corpus-hits.txt` (113 pattern lines) | `5e17f83f8aebf1b466ea33c1a9157a9e49f0e9efd0fa1b8f0a250525e23e42e6` |
| `evidence.log` (M1–M3 log; cancelled at its slow `find` step) | `0f64fcb6f4474fbd1439f00e323a6f1c74a6cad20e3e7e26c71234d530226f36` |
| `evidence2.log` (names, base counts, l7-04 citations) | `b5d9215df583895fd3b369eb681544ac5ab0a2da0c2c09ee497155e183e44ed1` |
| `evidence3.log` (quote verification) | `e8103b1f34f6ad9514efdaf9e9567f4726061ab62e1859d9979b7f1842a7b682` |
| `evidence4.log` (committed HEAD rerun, working-tree names, match-token check) | `7d77c04312c9658abfd4697730bf3b3ba55672ada57824c51222e37fc43653d9` |

No installs or updates (tooling directive satisfied by doing nothing). No REA run. No git or jj
write in any lane or in the fleet repo; every `git` command above is read-only (`grep`, `show`,
`ls-files`, `ls-tree`, `merge-base --is-ancestor`, `log`). The recursive jobs started before the
per-lane scans (`bg_5853`, `bg_5854`, `bg_6101`, `bg_6276`) were capped at 300 s; `bg_6276` was
cancelled after it had finished the needed M1–M3 steps.
