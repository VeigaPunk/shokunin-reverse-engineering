# Scout — Go RE parsers and Swiss map types

Item: does any other Go RE parser handle Swiss map types (GoReSym v3.4.1 release notes/changelog,
redress, Ghidra master after 12.1.4)? Read-only source census; no carrier was run, no REA/Ghidra analysis
was invoked, no parser was executed.

Accessed 2026-10-20T15:30Z. Primary sources: GitHub releases, tags, commits, PR state, raw file bytes,
and Go source at release tags. `gh` is authenticated; unauthenticated `api.github.com` was 60/hr-exhausted
(HTTP 403, `x-ratelimit-remaining: 0`), so `gh api` carried every API read.

## Bottom line

| parser | Swiss map types? | Evidence class |
|---|---|---|
| **redress v1.2.98 via gore v0.14.7** | **Yes, explicit** — detection, dedicated 64/32-bit layout parsers, and a test that asserts key/elem kinds and one method on a named map type | Observed source; not run on a carrier |
| **GoReSym v3.4.1** | **No explicit handling** — no `swiss` string anywhere, no version/experiment gate, no method recovery; its map case reads only key/elem/third-pointer, offsets that coincide with Swiss `Key`/`Elem`/`Group` | Observed source + inferred offset equivalence |
| **Ghidra master after 12.1.4** (`b8e9917e4c01`) | **Partial: Go 1.26+ only** — master's `GoMapType` gains `group` for `1.26-` and drops old fields for `≥1.26`; for Go 1.24/1.25 the class still binds `runtime.maptype`→`OldMapType`. No release contains this (12.1.4 is latest and is `1.15-1.25`); PR #9348 (1.24/1.25 Swiss) remains open | Observed source + snapshot data |

Consequence for C3: the lane's carriers are go1.24.6 / go1.25.0, so **Ghidra master would still take the
old-map path on them**. Master's added Swiss branch is gated at the Go 1.26 ABI rename, not at the
`goexperiment.swissmap` experiment. Neither GoReSym nor gore validates the aether mechanism; gore only
shows the descriptor split is recoverable.

## Evidence

### 1. The ABI hinge (defines "Swiss map type" in this round)

- [OBS] Go 1.24.6 and Go 1.25.0 `runtime/map_swiss.go:5` `//go:build goexperiment.swissmap`,
  `:22` `type maptype = abi.SwissMapType`; `runtime/map_noswiss.go:5` `//go:build !goexperiment.swissmap`,
  `:68` `type maptype = abi.OldMapType`
  (`https://raw.githubusercontent.com/golang/go/go1.25.0/src/runtime/map_swiss.go`).
- [OBS] Go 1.25.0 `internal/abi/map_swiss.go:32-43` `SwissMapType{Type; Key,Elem,Group *Type; Hasher;
  GroupSize,SlotSize,ElemOff uintptr; Flags uint32}`.
- [OBS] Go 1.26.0 has no `internal/abi/map_swiss.go` or `map_noswiss.go` (both HTTP 404);
  `internal/abi/map.go:32-43` defines `type MapType struct` with the same Swiss fields, and
  `type.go:408` returns `*MapType`. So in 1.26 the ABI name is `MapType`, and Go 1.26 has no old-map
  alternative.
- [OBS] Go 1.24 release notes: "a new builtin map implementation based on Swiss Tables … may be disabled by
  setting `GOEXPERIMENT=noswissmap`" (`https://go.dev/doc/go1.24`, Runtime section).

### 2. redress v1.2.98 → gore v0.14.7: explicit support (the "yes")

- [OBS] `redress` `go.mod:8` pins `github.com/goretk/gore v0.14.7`; `type.go:153` calls `f.GetTypes()`;
  `type.go:209-215` prints every type (and `typ.Methods` with `-m`) for `types all`.
  Release `v1.2.98` published `2026-10-20T12:50:16Z`; it is the latest.
- [OBS] gore `type2.go:108-115`:
  ```
  func usesSwissMapTypeLayout(goversion string, typesData []byte) bool {
      if GoVersionCompare(goversion, "go1.26rc1") >= 0 { return true }
      return bytes.Contains(typesData, []byte("internal/runtime/maps")) ||
          bytes.Contains(typesData, []byte("SwissMapType"))
  }
  ```
- [OBS] gore `type2.go:47-61`/`:72-86` select `mapTypeParseFuncSwiss64`/`Swiss32` when that returns true;
  `:862-877` maps `Group` into the parser's `Bucket` slot and reads `Hasher`/`Flags`:
  ```
  return mapType{ Key: resolvePointer(... typ.Key ...), Elem: ... typ.Elem ...,
      Bucket: resolvePointer(p.resolver, typ.Group, fileAddr+16), Hasher: ..., Flags: typ.Flags }
  ```
- [OBS] gore `type2.go:1322-1332` `mapTypeSwiss64{Key,Elem,Group,Hasher,GroupSize,SlotSize,ElemOff,Flags}`;
  `:1334-1343` the 32-bit form; `:1345-1374` an additional Go 1.27 layout.
- [OBS] gore `slow_test.go:305-329` `TestSwissMapTypes` builds `go126SwissMapTestSrc`
  (`type namedMap map[string]int` with `func (m namedMap) Touch() int`), then asserts
  `typ.Key.Kind == reflect.String`, `typ.Element.Kind == reflect.Int`,
  `require.Len(t, typ.Methods, 1)`, `typ.Methods[0].Name == "Touch"`.
- [OBS] Provenance: commit `754807d2e43c05b6574c2d4098c61c739f7b6b4d`, "feat: add swiss map type parsing
  support", 2026-05-17, `slow_test.go` 73 and `type2.go` 128 changed lines (174 insertions, 27 deletions
  total); `git describe --contains` →
  `v0.13.29~1`, and every tag `v0.13.29` … `v0.14.7` contains it.
- [OBS] gore type methods are parsed generically from `uncommon` data at `type.go:758`
  (`typ.Methods = parseMethods(...)`) and `type2.go:1170` `uncommonTypeParseFunc64`; map dispatch is
  `type2.go:367-374`.
- [INF] The `usesSwissMapTypeLayout` heuristic for 1.24/1.25 depends on `internal/runtime/maps` or
  `SwissMapType` appearing in the types-region bytes. The test fixture is written against a 1.26 toolchain
  and only skips `< go1.24`, so the repo demonstrates the 1.26 path; the 1.24/1.25 string path is code-present
  but not proven here (no carrier run).

### 3. GoReSym v3.4.1: no Swiss awareness

- [OBS] `v3.4.1` release body (published `2026-09-14T17:08:29Z`):
  > "Improve handling of 1.20+ layouts when version info cannot be recovered by trying runtime versions
  > 1.20 - 1.26 which all share the same layout  version but have fields shifted in 1.26+"
  > https://github.com/mandiant/GoReSym/pull/102 @mlhaigh
  The single commit is `722897e0a80da0a06c00c5e40591a253a551f04e`, `objfile: fallback to modern moduledata
  layouts when runtimeVersion is unknown (#102)`, one file `objfile/objfile.go` (+124/−115). The added
  lines are moduledata (`Go 1.26 introduced epclntab, shifting textsectmap and subsequent fields`), not map
  descriptors. Master HEAD == `v3.4.1` (`git ls-remote`: both `722897e0a80d`); no newer release.
- [OBS] `grep -rni swiss --include='*.go' --include='*.md'` in the v3.4.1 tree: **no matches** (exit 1).
- [OBS] `objfile/objfile.go:1023-1058` `case Map:` carries the old comment (`bucket *rtype`,
  `keysize/valuesize/bucketsize`) but reads only three pointers at `baseSize+0/+ptr/+2ptr` and recurses;
  `hasher`, sizes, and flags are never read. `tflagUncommon` is consumed only to skip 16 bytes in the
  **func** case (`:796-798`), and `Type` (`objfile/internals.go:136-147`) has no method field. So GoReSym
  recovers no method sets for named map types at all.
- [INF] Because `SwissMapType` places `Key`, `Elem`, `Group` at the same three pointer offsets as
  `OldMapType`'s `Key`, `Elem`, `Bucket`, GoReSym's three reads land on valid `*Type` values under Swiss; it
  labels `Group` "bucket" but does not follow the fields that diverge (`GroupSize/SlotSize/ElemOff` vs
  `KeySize/ValueSize/BucketSize`). This is derived from the two struct layouts, not from a run.
- [OBS] No GoReSym issue/PR mentions Swiss: `search/issues?q=swiss repo:mandiant/GoReSym` → `total_count 0`;
  the only map-related PR is closed and about `ModuleDataTable` offset maps (#71).

### 4. Ghidra master after 12.1.4: 1.26-only split, 1.24/1.25 unchanged

- [OBS] `Ghidra_12.1.4_build` = `8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc`, committer date
  `2026-09-11T10:14:59Z`; latest release is 12.1.4 (`2026-09-21T17:38:59Z`). Installed
  `GoRttiMapper.java:79` is `GoVerRange.parse("1.15-1.25")` (extracted from
  `Ghidra/Features/Base/lib/Base-src.zip`).
- [OBS] Master HEAD `b8e9917e4c01959fe97ba94954731ed8cf2d201c` (2026-10-20T08:14:31-04:00) has
  `GoRttiMapper.java:79` `GoVerRange.parse("1.15-1.26")` and `go1.26.0.json`.
- [OBS] Master `rtti/types/GoMapType.java:32-34` maps the same three names
  `{ "runtime.maptype", "internal/abi.MapType", "internal/abi.OldMapType" }`; no Java file in the golang
  tree contains `SwissMapType` (grep over the sparse checkout: none). `:45-63`:
  ```
  @FieldMapping(presentWhen = "-1.25") private long bucket;
  @FieldMapping(presentWhen = "1.26-") private long group;   // ptr to group type
  @FieldMapping(presentWhen = "-1.25") private int keysize;
  @FieldMapping(fieldName = { "elemsize", "ValueSize" }, presentWhen = "-1.25") private int elemsize;
  @FieldMapping(presentWhen = "-1.25") private int bucketsize;
  @FieldMapping private int flags;
  ```
  `GoRttiMapper.java:399-413` applies `GoVerSet.parse(presentWhen).contains(goVer)`; `GoVerRange.java:33-52`
  documents `"-1.5"`, `"1.2-"`, `"1.2+"` forms, so `-1.25` = ≤1.25 and `1.26-` = ≥1.26.
- [OBS] Installed 12.1.4 `GoMapType.java` (same sha256 as the tag raw file and the installed zip member:
  `6f8786a0f50d8f21f1e079062e6bce373c4724422f8297634642c3f5ea7c33ca`) has `bucket`, `hasher`, `keysize`,
  `elemsize`, `bucketsize`, `flags` with **no version gates**, and `getBucket()` with no null guard
  (`:45-59`, `:96-99`). Master's sha256 is
  `566f4369b5d37ff40824128c4277cf954289d58c56c576ee3760ca22dd454c22`.
- [OBS] The change is GP-6528 `385e8cd923d0` "add support for golang 1.26" (author 2026-03-03), which also
  added `go1.26.0.json` and touched `GoMapType.java` (+20/−5). `compare/Ghidra_12.1.4_build...385e8cd` →
  `diverged`, `ahead_by 1`, `behind_by 559`: the commit is **not** an ancestor of the 12.1.4 tag. The same
  commit also adds the `getBucket`/`getGroup` null guards; a later `ed77fbc07b16` (GP-6871) adds
  `isValidSize` only.
- [OBS] Snapshot contents (master and installed copies agree for 1.24/1.25):
  - `go1.24.0.json` / `go1.25.0.json`: `internal/abi.OldMapType` (Bucket, KeySize, ValueSize, BucketSize,
    Flags) and `internal/abi.SwissMapType` (Group, GroupSize, SlotSize, ElemOff, Flags) both exist, but
    `runtime.maptype` is `{"Kind":"alias","Target":"internal/abi.OldMapType"}` (Position
    `$GOROOT/runtime/map_noswiss.go:67:6` / `:68:6`).
  - `go1.26.0.json`: only `internal/abi.MapType` (Group, GroupSize, SlotSize, ElemOff, Flags); no
    `runtime.maptype`, no `OldMapType`, no `SwissMapType`.
- [INF] Therefore master's `1.26-` branch is the first branch that reads a Swiss descriptor, and it is keyed
  to the Go 1.26 rename. For the lane's 1.24.6/1.25.0 Swiss carriers master still binds the old field set:
  `keysize`@32 reads `GroupSize`'s low 4 bytes, `elemsize`@36 its high 4, `bucketsize`@40 `SlotSize`'s low
  16, `flags`@44 the rest of `SlotSize` — the same class of misread the C3 emulator targets, not a fixed
  path.
- [OBS] Upstream PR #9348 (external, `kubrickfr`) is still `state: OPEN`, `mergedAt: null`, title
  "Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries", updated 2026-08-31.
- [OBS] No post-12.1.4 golang-package commit adds Swiss handling: path-filtered commits since 2026-09-11
  return only `ff5d7a12d612` (committer 2026-09-14, a `DataTypeManagers/Archives` refactor touching Debug
  files); the newest golang-package commit by author date is `0f5a0e592bd5` 2026-08-05.

## Observation vs inference

- **Observed**: every code quote, file hash, tag/commit/PR state, snapshot alias, and release body above,
  at the stated tag/commit.
- **Inference**: (a) GoReSym's three pointer reads are layout-compatible with Swiss Key/Elem/Group
  (struct-offset comparison only); (b) gore's 1.24/1.25 string heuristic works on real map-using binaries
  (not exercised); (c) Ghidra master's ≤1.25 path remains misaligned on Swiss fields (from field order and
  snapshot alias, no run).
- **Not claimed**: that gore or GoReSym produces correct recovery quality; that Ghidra 12.1.4's aether EOF
  is caused by this specific field read (C3 owns that); that any release beyond 12.1.4 exists.

## Commands run (verbatim, with exit)

| command | exit |
|---|---|
| `gh release view v3.4.1 -R mandiant/GoReSym --json tagName,publishedAt,targetCommitish,name,body` | 0 |
| `gh api repos/mandiant/GoReSym/commits/722897e0a80d --jq '{msg:...,files:...}'` | 0 |
| `git ls-remote https://github.com/mandiant/GoReSym refs/heads/master refs/tags/v3.4.1` | 0 |
| `git clone -q --depth 1 --branch v3.4.1 https://github.com/mandiant/GoReSym /tmp/gore-v341` | 0 |
| `grep -rni "swiss" --include='*.go' --include='*.md' .` (in `/tmp/gore-v341`) | 1 (no match) |
| `grep -rn "tflagUncommon" --include='*.go' .` (in `/tmp/gore-v341`) | 0 |
| `gh api "repos/mandiant/GoReSym/pulls?state=all&per_page=100" --jq '...test("map\|swiss")...'` | 0 |
| `git clone -q --depth 1 --branch v0.14.7 https://github.com/goretk/gore /tmp/gore-v0147` | 0 |
| `git clone -q --filter=blob:none https://github.com/goretk/gore /tmp/gore-full` | 0 |
| `git describe --contains 754807d2e43c` (in `/tmp/gore-full`) | 0 → `v0.13.29~1` |
| `gh api "repos/goretk/gore/commits?path=type2.go&per_page=15"` | 0 |
| `git clone -q --depth 1 --branch v1.2.98 https://github.com/goretk/redress /tmp/redress-v1298` | 0 |
| `gh release list -R goretk/redress --limit 10` | 0 |
| `gh release view v1.2.98 -R goretk/redress --json publishedAt,body` | 0 |
| `curl -sS https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/master/.../GoMapType.java` | 0 (HTTP 200, 5383 B) |
| `curl -sS https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/Ghidra_12.1.4_build/.../GoMapType.java` | 0 (HTTP 200, 4696 B) |
| `sha256sum /tmp/GoMapType-master.java /tmp/GoMapType-1214.java` | 0 (digests differ) |
| `unzip -o .../Base-src.zip 'ghidra/.../types/GoMapType.java' -d /tmp/ghidra1214src` | 0 |
| `sha256sum /tmp/ghidra1214src/.../GoMapType.java /tmp/GoMapType-1214.java` | 0 (equal) |
| `unzip -p .../Base-src.zip '*/GoRttiMapper.java' \| grep -n '"1.15'` | 0 → `79: "1.15-1.25"` |
| `git clone -q --depth 1 --filter=blob:none --sparse https://github.com/NationalSecurityAgency/ghidra /tmp/ghidra-sparse` | 0 |
| `grep -n "SUPPORTED_VERSIONS" .../rtti/GoRttiMapper.java` (master) | 0 → `79: "1.15-1.26"` |
| `grep -rn "SwissMapType" .../src/main/java/ghidra/app/util/bin/format/golang` (master) | 1 (no match) |
| `gh api "repos/.../commits?path=.../GoMapType.java&per_page=20"` | 0 |
| `gh api "repos/.../compare/Ghidra_12.1.4_build...385e8cd923d0"` | 0 → `diverged 1 559` |
| `gh release list -R NationalSecurityAgency/ghidra --limit 5` | 0 |
| `gh pr view 9348 -R NationalSecurityAgency/ghidra --json state,title,createdAt,updatedAt,mergedAt,...` | 0 → OPEN |
| `python3` snapshot walk over installed `go1.24.0.json` / `go1.25.0.json` / master `go1.26.0.json` | 0 |
| `curl -sS https://raw.githubusercontent.com/golang/go/go1.25.0/src/runtime/map_swiss.go` (and `map_noswiss.go`, go1.24.6, go1.26.0 `map.go`; go1.26.0 `map_swiss.go`/`map_noswiss.go` → 404) | 0 |
| `curl -sS https://go.dev/doc/go1.24` | 0 (HTTP 200) |
| `gh api repos/gnzlbg/redress` (probe) | 1 (404 — wrong slug; corrected to `goretk/redress`) |
| `curl -sS https://api.github.com/repos/mandiant/GoReSym/releases/latest` (probe) | 0 but HTTP 403, rate-limited |

No tool was installed or upgraded. `gh` 2.x (authenticated), `git`, `curl`, `python3` were already present.

## Proposed SOURCES row (one; L1 may instead fold it as a lead line)

Next free id after C1's S033 is **S034**.

```
| S034 | goretk/gore Swiss map descriptor parser (the parser behind redress v1.2.98) — https://github.com/goretk/gore/blob/v0.14.7/type2.go | code | A | Explicit Swiss-map type-descriptor parsing: detection plus 64/32-bit layouts, reached by redress through gore | Tag `v0.14.7`; `type2.go:108-115` `usesSwissMapTypeLayout`; `:862-877` `mapTypeParseFuncSwiss64` maps `Group` into the `Bucket` slot; `:1322-1332` `mapTypeSwiss64`; commit `754807d2e43c05b6574c2d4098c61c739f7b6b4d`, 2026-05-17, first tag `v0.13.29`; `slow_test.go:305-329` | A second Go RE parser treats `SwissMapType` as a distinct layout and tests key/elem kinds plus one method on a named map type; redress reaches it via `go.mod:8` `gore v0.14.7` and `type.go:153` `GetTypes`. The old/Swiss split is therefore a parser-layout choice, not a limit of Go metadata; it does not test Ghidra or this lane's carriers. | mined | 2026-10-20 | on-release | corpus/knowledge/2026-10-20-r18-swiss-parser-census.md (proposed) |
```

## Remaining unknowns

- gore/redress were not run against `/usr/bin/aether` or any C3 carrier (analysis is L1's single sequential
  pass), so the 1.24/1.25 detection-string path and any recovery-quality claim are untested here.
- Ghidra master was read at `b8e9917e4c01`; a later commit could change `GoMapType`, though no golang-package
  commit exists after 2026-08-05 as of access.
- PR #9348's diff was not opened (S032 and a sibling scout own it); only state/title/date were verified.
- GoReSym has no post-v3.4.1 commits or releases, so "v3.4.1" is also "current master".
