# ConnSourcesPaths — round 18 `## Paths` proposal and search-log skeleton

Seat: `KaidokuR18.ConnSourcesPaths` (leaf, advisory; L1 integrates). Read-only on lane files; this report is the only write. No REA/Ghidra/carrier execution, no network, no `jj`/git writes, no installs. Peer w1 reports written this round were read as data.

Axes: calibration (C1), operability (C2), depth (C3).

## Bottom line

1. **Row allocation: S033 PR revision, S034 Go 1.24 notes, S035 one `internal/abi` map-layout row covering both tags, S036 jj 0.45.1 docs.** This resolves a real four-way `S034` collision in the w1 drafts (below); `ScoutAbiSwissLayout.md:98-102` independently recommends exactly S034-notes / S035-one-map-row.
2. **`## Paths`:** replace the current route bullet (`corpus/SOURCES.md:44`) so it ends at S030, insert a Swiss-map replay bullet `S034 → S035 → S023 → S033`, and insert a jj bullet `S036`. Verbatim text below.
3. **Search log:** two prose entries (Go/Swiss, jj/git) with named count placeholders and a ledger that counts *candidate rows* separately from *supporting sources*, fixing the round-17 count defect class (`ReviewSourcesRows.md:43-45`).

## Evidence (observation unless marked INFERENCE)

- `corpus/SOURCES.md` has 32 data rows; sections: Registry `:3`, Paths `:40`, Search log `:51`, Leads `:61`. S032 is the last row `:38`; the current route path `:44` ends `S032`. [OBS]
- `claims.json:14` fixes S033 as the C1 source (`supersedes S032`); `:21` sources C2 to the jj docs row; `:28` sources C3 to the Go 1.24-notes and `internal/abi` rows. [OBS]
- `contract.md:44-45` requires S033's `teaches` to start `supersedes S032 —` and its anchor to contain `fetch-time`. [OBS]
- `wave1-spec.json:283,288,293,298` orders the four row drafts (S033Row, GoNotesRow, AbiRow, JjRow); `:8` sets the report dir. [OBS]
- Draft IDs collide: `DraftS033Row.md:10` S033; `DraftGoNotesRow.md:11` S034; `DraftAbiRow.md:10` S034; `DraftJjRow.md:41` S034; `ScoutJjColocation.md:74` S034; `ScoutGitRevParseDocs.md:6` proposes S035; `ScoutGo125MapsNotes.md:155` offers an optional new row. Four drafts explicitly claim S034 (`DraftGoNotesRow`, `DraftAbiRow`, `DraftJjRow`, `ScoutJjColocation`); two more (`ScoutAbiSwissLayout`, `ScoutGo125MapsNotes`) number themselves against it. [OBS]
- `ScoutAbiSwissLayout.md:98-102` recommends S034 = 1.24 notes, S035 = one map-layout row subsuming `DraftAbiRow`, and says not to register both map rows. [OBS]
- Installed `go1.25.0.json`: `runtime.maptype` = alias → `internal/abi.OldMapType`, Position `$GOROOT/runtime/map_noswiss.go:68:6`; `go1.24.0.json`: same target, Position `:67:6` (read with Python stdlib JSON). [OBS]
- Local go1.25.0: `src/runtime/map_swiss.go:5` `//go:build goexperiment.swissmap`, `:22` `type maptype = abi.SwissMapType`; `src/runtime/map_noswiss.go:5` `!goexperiment.swissmap`, `:68` `type maptype = abi.OldMapType` (go1.24.6: `:67`). [OBS]
- `src/internal/abi/map_select_swiss.go:5,22` / `map_select_noswiss.go:5,10` select `mapType`; `type.go:321` is `Uncommon`, `:358-363` is the `case Map` that places uncommon data after `mapType`. [OBS]
- `map_swiss.go` and `map_noswiss.go` are byte-identical between go1.24.6 and go1.25.0 (sha256 pairs equal; `diff -q` exit 0) and carry no build tag (`grep -c 'go:build'` = 0, grep exit 1). Both `exp.go` baselines set `SwissMap: true` (1.25.0 `:85`, 1.24.6 `:81`). [OBS]
- `ScoutAbiSwissLayout.md:58-65` measures amd64 `SwissMapType` 112 bytes / `OldMapType` 88 bytes; `:76-83` derives the 24-byte uncommon-offset shift. [OBS from that report]
- `ScoutGo125MapsNotes.md:15,67-70`: the 1.25/1.26/1.27 release notes contain 0 `swiss` matches; the 1.25.0 toolchain accepts `noswissmap` and records `X:noswissmap`. [OBS]
- `ScoutJjColocation.md:9-11`: the `v0.45.1` page says `jj` commands "will usually put the Git repo in a `"detached HEAD"` state"; the working-copy-parent wording is a recipe comment (`:10`, `docs/git-compatibility.md:208`), not prose; `latest` is 0.46.0 content and must not be cited for 0.45.1. [OBS]
- `ScoutGitRevParseDocs.md:6` recommends one git-grammar row; its §2.1-2.3 shows `--verify` takes one argument, `^{commit}` does not prove attachment, bare names can resolve to tags, and `@{u}` fails on a detached HEAD. [OBS]
- [INFERENCE] The canonical IDs are S034/S035/S036 by spec order plus the abi-scout recommendation. If the L1 admits the optional git or 1.25-selection rows, they take S037/S038; substitution rules are given below.

## Proposed `## Paths` text (verbatim, integration-ready)

Replace current line 44 with this bullet:

```
- Go carrier route diagnosis — S024 → S026 → S031 → S025 → S003 → S023 → S029 → S030: read the stdlib build-info decoder, decode the `X:` experiment suffix and its DWARF 5 opt-out, date the toolchain, then the installed selector and its 1.25 base, then upstream Ghidra and GoReSym release status. These sources predict the logged bootstrap and snapshot routes; they do not establish patched-content correctness or recovery quality.
```

Insert immediately after it, as the next two bullets:

```
- Swiss-map layout replay (aether EOF) — S034 → S035 → S023 → S033: read the Go 1.24 note that names the Swiss Tables map implementation and the build-time `noswissmap` opt-out, then the 1.24.6/1.25.0 `internal/abi` descriptor structs and the experiment alias that selects one (112-byte `SwissMapType`, 88-byte `OldMapType` on amd64, byte-identical across the two tags), then the installed `go1.25.0.json` snapshot's single `runtime.maptype` → `OldMapType` binding, and end at the PR revision (supersedes S032) that names the old-vs-Swiss misread; the chain grounds the mechanism, not an instrumented replay or correct map-type layout.
- jj colocated revision pins — S036: read that jj commands usually leave Git HEAD detached and that the conversion recipe points it at the working-copy commit's parent, so a pin resolves `refs/heads/<branch>` and compares it with `HEAD` instead of treating `HEAD` as the branch tip; the row is the `v0.45.1` tag, and the parent statement is recipe commentary, not a general rule.
```

### Conditional variants (pick exactly one branch per extra row)

- **If S037 (git grammar) is admitted:** replace the jj bullet with:
  ```
  - jj colocated revision pins — S037 → S036: read the git grammar first (one-argument `--verify`, `^{commit}` peels but does not prove attachment, bare names may resolve to tags, `@{u}` needs an attached branch), then what jj does to HEAD in a colocated workspace (commands usually leave it detached; the conversion recipe names the working-copy commit's parent), so a pin resolves `refs/heads/<branch>` and compares it with `HEAD`; the jj row is the `v0.45.1` tag, not the moving `latest` page.
  ```
- **If S038 (1.25 map-selection source) is admitted:** change the replay arrow to `S034 → S038 → S035 → S023 → S033` and add after the 1.24-note clause: "then the 1.25 build-config/reflectdata gate that still honours `noswissmap`,".
- **If a Ghidra map-class-binding row is admitted by `ScoutGhidraGoStructMapping`:** insert it between `S023` and `S033`; if not, keep S003 out of this path — S003's scope is the version gate/bootstrap, not map-class binding, so citing it for the binding would stretch the row.

Placement rationale: the route path now predicts routes only (S032 did not predict a route; it explained a post-bootstrap failure), and the replay path makes the C3 mechanism a first-class ordered read. S032 leaves the *path* (not the registry) because S033 supersedes its unreproducible digest; the replay prose still names the supersession.

## Row-ID allocation (for the registry append)

| id | row | draft source | note |
|---|---|---|---|
| S033 | PR #9348 revision, head `a214355…`, state OPEN, digest fetch-time only | `DraftS033Row.md:10` | required by `contract.md:44-45` |
| S034 | Go 1.24 Release Notes, `#runtime` | `DraftGoNotesRow.md:11`; `ScoutGo124NotesSwiss.md:60` | drafts disagree on status (`DraftGoNotesRow.md:11` says `mined`, `ScoutGo124NotesSwiss.md:60` says `queued`); the C3 citation decides, and the transition is logged old→new |
| S035 | go1.24.6 + go1.25.0 `internal/abi` map descriptors and alias, compiled amd64 layout | `ScoutAbiSwissLayout.md:102` | **one** row; subsumes `DraftAbiRow.md:10`; do not register both |
| S036 | jj 0.45.1 Git compatibility (`docs.jj-vcs.dev/v0.45.1/...`) | `ScoutJjColocation.md:74` | prefer this over `DraftJjRow.md:41` (`latest` = 0.46.0) |
| S037 (optional) | git-rev-parse + gitrevisions 2.56.0 | `ScoutGitRevParseDocs.md:253` | strengthens C2; one row for both pages |
| S038 (optional) | go1.25.0 map-experiment selection (`buildcfg/exp.go`, `reflectdata`, `map_select_*`) | `ScoutGo125MapsNotes.md:155` | only if L1 wants source grounding for the 1.25 `noswissmap` half |

Every primary row (S033-S036) appears in exactly one path above, so none is registered `mined` without a path citation. S032 stays a registry row with its round-17 `used-by`; no row text is edited by this proposal.

## Search-log entry skeleton (verbatim; fill placeholders from scout reports)

```
- 2026-10-20 round 18 — Question: which official Go sources ground the Swiss/old map-descriptor distinction and the `noswissmap` opt-out that C3's minimal pair and the aether EOF inference depend on, and what stable identity can the S032 lead carry? Where searched: https://go.dev/doc/go1.24 (`#runtime`, lines 560-573); https://go.dev/doc/go1.25, /1.26, /1.27 (a case-insensitive `swiss` search returned 0 matches on each page); the installed go1.24.6 and go1.25.0 trees (`src/internal/abi/{map_swiss,map_noswiss,map_select_swiss,map_select_noswiss,type}.go`, `src/internal/buildcfg/exp.go`, `src/internal/goexperiment/flags.go`, `src/cmd/compile/internal/reflectdata/{reflect,map_swiss,map_noswiss}.go`, `src/runtime/{map_swiss,map_noswiss,type}.go`); the installed Ghidra `go1.24.0.json` and `go1.25.0.json` (`runtime.maptype`), plus Base-src.zip (`ScoutGhidraGoStructMapping`, report pending); GitHub PR #9348 (page, API JSON, `gh pr view`; multiple fetches, HTML digest not reproducible). Identified {I-go} candidate rows: S033 (PR revision), S034 (1.24 notes), S035 (one map-layout row covering both tags){, S038 if the 1.25 selection row is admitted}; screened {S-go}; included {INC-go}; excluded {EXC-go}: the 1.25 notes page (0 `swiss` matches; S031 already rows it for DWARF), the 1.26/1.27 notes pages (outside the claim), and the second map-layout draft (folded into S035 per ScoutAbiSwissLayout.md:98-102). Separately {SUP-go} supporting sources were opened and are not row candidates: {go.dev pages, both toolchain trees, installed JSONs, PR HTML/API}. Negative denominators: 0 `swiss` matches on each of the 1.25/1.26/1.27 notes pages (ScoutGo125MapsNotes.md:67-70); {Gh tags}/{GoReSym releases} only if ScoutGoReSymSwiss re-swept them. Stop: the 1.24 note, both descriptor layouts with their alias gate, the installed alias and the PR revision answer the mechanism question; Go 1.26/1.27 are C3's stated non-goal.
```

```
- 2026-10-20 round 18 — Question: in a jj-colocated workspace, what does Git HEAD name, and what must a branch-tip pin resolve instead? Where searched: jj git-compatibility at tag v0.45.1 (`docs.jj-vcs.dev/v0.45.1` and raw `docs/git-compatibility.md`; v0.45.0 bytes identical, `latest` is 0.46.0 content), jj revsets/bookmarks (`trunk()`, `name@remote`) and config (`snapshot.auto-track`, 1 MiB default), local `jj help` topics (`git-compatibility` is not a topic), git-rev-parse/gitrevisions at 2.56.0, and throwaway colocated sandboxes under mkdtemp. Identified {I-jj} candidate rows: S036 (jj docs) and the git grammar row recommended by ScoutGitRevParseDocs.md:6 (S037 if admitted); screened {S-jj}; included {INC-jj}; excluded {EXC-jj}: revsets/bookmarks and snapshot config as operational leads only, and the `latest`/0.46.0 pages because they are not the host's 0.45.1. Stop: one tag-anchored jj statement, plus the git grammar row if admitted, bound the pin; deeper jj model detail is operational, not corpus.
```

### Count ledger (how to fill the placeholders)

| placeholder | definition | fill source |
|---|---|---|
| `I-go` | distinct candidate **row families** considered, not URLs | S033 (`DraftS033Row.md`), S034 (`DraftGoNotesRow.md`, `ScoutGo124NotesSwiss.md`), S035 (`ScoutAbiSwissLayout.md`, subsumes `DraftAbiRow.md`), optional 1.25 row (`ScoutGo125MapsNotes.md:155`) |
| `S-go` | candidate families actually opened and checked | the same reports |
| `INC-go` | rows admitted | final registry; primary 3 |
| `EXC-go` | opened candidate families not admitted, each with a reason | 1.25 notes page, 1.26/1.27 pages, duplicate map draft, optional 1.25 row if not admitted |
| `SUP-go` | supporting sources opened that were never row candidates | the "Where searched" list; do not add these to `I-go` |
| `I-jj`/`S-jj`/`INC-jj`/`EXC-jj` | same rules for the jj/git question | `ScoutJjColocation.md`, `DraftJjRow.md`, `ScoutGitRevParseDocs.md`, `ScoutJjRevsetsTrunk.md` |
| negative denominators | count behind each "0 matches"/"no release" | `ScoutGo125MapsNotes.md:67-70`; `ScoutGoReSymSwiss.md` if it re-swept tags/releases |

This split is deliberate: the round-17 verifier found that row-level counts hid sources the round actually opened (`ReviewSourcesRows.md:43-45`), and that universal negatives lacked denominators.

## Axis effects and no-harm

- **Calibration:** resolves the S034 collision (five drafts, one ID) before integration; prevents a second map-layout row; stops the route path from conflating route prediction with mechanism explanation; separates candidate-row counts from supporting-source counts; keeps S003 inside its scoped row.
- **Operability:** the three bullets are paste-ready; the ID table and conditional variants make renumbering mechanical; placeholders name the exact report that fills each count.
- **Depth:** the replay chain carries the concrete 112/88 layout and the build-tag alias gate, then the installed snapshot's single-branch alias, ending at the PR revision that names the misread; the jj bullet is tag-anchored and distinguishes prose from recipe commentary.
- **No-harm:** `## Paths` is not a registry row, so the `W18/controls.py` row comparison (S001-S032 unchanged except status/recheck/used-by) is untouched. S032 remains in the registry; only the path anchor moves to S033. No claim of an instrumented Ghidra replay, map-layout correctness, or recovery quality is added.

## Risks / decisions for the L1

1. **Integrate the both-tags S035, not `DraftAbiRow`'s 1.25-only row.** If the 1.25-only draft is used, drop the "1.24.6/1.25.0" and "byte-identical" clauses from the replay bullet.
2. **Integrate `ScoutJjColocation`'s `v0.45.1` row, not `DraftJjRow`'s `latest` row.** If the latter is used, the "row is the `v0.45.1` tag" clause must be removed or the anchor replaced (latest is 0.46.0 content).
3. **S023's source is the `go1.25.0.json` snapshot only**; the replay bullet names that JSON, not the 1.24 JSON, even though the 1.24 JSON was also observed to bind `OldMapType`.
4. **Ghidra map-class binding:** if `ScoutGhidraGoStructMapping` recommends a scoped row, insert it before S033; otherwise the reader binding stays a C3 tool-basis citation, not a path row. Do not cite S003 outside its version-gate/bootstrap scope.
5. **Counts:** `ScoutGhidraGoStructMapping`, `ScoutInstalledJsonMaps`, `ScoutGoReSymSwiss`, and `ScoutPr9348Reopen` had no report at my read time; finalize `{I-go}`, `{SUP-go}` and the sweep denominators from their reports at integration.

## Commands and exit codes (read-only; no network)

```
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
G=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
A124=/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi
A125=/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi
R125=/home/vgpnk/.local/opt/go-1.25.0/src/runtime

$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$L/corpus/SOURCES.md"
32                                                              exit 0
$ grep -nE '^(## (Registry|Paths|Search log|Leads)|# SOURCES)' "$L/corpus/SOURCES.md"
1:# SOURCES  3:## Registry  40:## Paths  51:## Search log  61:## Leads   exit 0
$ awk 'NR==38 || NR==40 || NR==44 {printf "%d: %s\n", NR, substr($0,1,80)}' "$L/corpus/SOURCES.md"
38: | S032 ...  40: ## Paths  44: - Go carrier route diagnosis ... S032  exit 0
$ python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["all"]["Types"]["runtime.maptype"])' "$G/go1.25.0.json"
{'Kind': 'alias', 'Target': 'internal/abi.OldMapType', 'Position': '$GOROOT/runtime/map_noswiss.go:68:6'}  exit 0
$ python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["all"]["Types"]["runtime.maptype"])' "$G/go1.24.0.json"
{'Kind': 'alias', 'Target': 'internal/abi.OldMapType', 'Position': '$GOROOT/runtime/map_noswiss.go:67:6'}  exit 0
$ grep -n "type mapType" "$A125"/map_select_*.go "$A124"/map_select_*.go
map_select_noswiss.go:10 / map_select_swiss.go:22 in both trees   exit 0
$ grep -n "go:build\|type maptype" "$R125"/map_swiss.go "$R125"/map_noswiss.go
5://go:build goexperiment.swissmap  22:type maptype = abi.SwissMapType
5://go:build !goexperiment.swissmap  68:type maptype = abi.OldMapType   exit 0
$ grep -c 'go:build' "$A124"/map_swiss.go "$A124"/map_noswiss.go "$A125"/map_swiss.go "$A125"/map_noswiss.go
0 for each file (grep exit 1: no matches)                      exit 1
$ sha256sum "$A124"/map_swiss.go "$A125"/map_swiss.go "$A124"/map_noswiss.go "$A125"/map_noswiss.go
0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383 (both)
03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291 (both)  exit 0
$ diff -q "$A124"/map_swiss.go "$A125"/map_swiss.go; diff -q "$A124"/map_noswiss.go "$A125"/map_noswiss.go
(no output, no output)                                         exit 0
$ grep -n "SwissMap:" /home/vgpnk/.local/opt/go-1.25.0/src/internal/buildcfg/exp.go /home/vgpnk/.local/opt/go-1.24.6/src/internal/buildcfg/exp.go
1.25.0:85 / 1.24.6:81                                          exit 0
$ grep -n "S033\|R17-S032-DIGEST" "$L/.ufo/waves/round-18/claims.json" "$L/.ufo/waves/round-18/contract.md"
claims.json:14 ; contract.md:44-45                             exit 0
$ grep -n '"DraftS033Row"\|"DraftGoNotesRow"\|"DraftAbiRow"\|"DraftJjRow"' "$L/.ufo/waves/round-18/wave1-spec.json"
283 / 288 / 293 / 298                                          exit 0
```

An earlier `grep -rn "goexperiment" map_swiss.go map_noswiss.go` returned exit 1 (no matches) — itself the observation that the two struct files carry no experiment tag; selection lives in `map_select_*.go`.

## Tooling record

No installs or upgrades. No network. Used `grep`, `awk`, `sed`, `sha256sum`, `diff`, and Python 3 stdlib JSON reads only. No REA, Ghidra, carrier execution, `jj`, or git write; lane files other than this report were not touched.

## Limits

- Counts are a skeleton, not final numbers: four source-related scout reports had not landed at read time (see risk 5). The schema and ledger are the deliverable; fill at integration.
- The proposed text assumes the canonical S034-S036 allocation and the both-tags abi row. If either changes, use the substitution rules; the arrow order is independent of the numbers.
- The jj parent clause is explicitly recipe commentary (`ScoutJjColocation.md:10`); the path says so. The lane's own detached-HEAD state is an observation from that report, not a general claim about all jj versions.
- No verdict on whether C3's carriers reproduce the aether mechanism; this report only orders the sources and fixes the counts' shape.
