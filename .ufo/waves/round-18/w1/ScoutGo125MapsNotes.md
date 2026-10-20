# ScoutGo125MapsNotes — does Go 1.25 still support `GOEXPERIMENT=noswissmap`?

Seat: `KaidokuR18.ScoutGo125MapsNotes` (author-side advisory). Read-only; no lane file edited.
Network used only for the two hosts named in the item (`go.dev`, `raw.githubusercontent.com`). No tool installed.
Labeling: **[OBS]** = command output or quoted bytes read this session; **[INF]** = inference from those bytes.

## Verdict

**[OBS]** Yes. Go 1.25.0 still supports `GOEXPERIMENT=noswissmap`. It is a first-class `goexperiment.Flags`
field (baseline `true`, so `no`-prefix clears it), the old map implementation survives as a complete
build-tagged tree (12 negative-tagged files, including a 1891-line `runtime/map_noswiss.go`), and the
installed go1.25.0 toolchain accepts the flag, recompiles the standard-library imports under the new
configuration, links and runs a map program, recording `X:noswissmap` in build-info.

**[OBS]** The **1.25 release notes do not mention it at all** (0 occurrences of `swiss`), so the 1.25 notes
page is *not* a source for this claim; the 1.25 source tree plus the 1.24 notes sentence are.

## Anchors and quotes (all ≤25 words, contiguous)

| # | Path:line (go1.25.0) | Quote | Kind |
|---|---|---|---|
| 1 | `src/internal/buildcfg/exp.go:85` | `SwissMap:        true,` (inside `baseline := goexperiment.Flags{` at `:81`) | code |
| 2 | `src/internal/buildcfg/exp.go:101` | `names := make(map[string]func(bool))` | code |
| 3 | `src/internal/buildcfg/exp.go:106` | `names[strings.ToLower(rt.Field(i).Name)] = field.SetBool` | code |
| 4 | `src/internal/buildcfg/exp.go:131-132` | `if strings.HasPrefix(f, "no") {` / `f, val = f[2:], false` | code |
| 5 | `src/internal/buildcfg/exp.go:134-136` | `set, ok := names[f]` … `unknown GOEXPERIMENT %s` | code |
| 6 | `src/internal/buildcfg/exp.go:187` | `list = append(list, "no"+name)` | code |
| 7 | `src/internal/goexperiment/flags.go:115-116` | `// SwissMap enables the SwissTable-based map implementation.` `SwissMap bool` | code |
| 8 | `src/internal/goexperiment/exp_swissmap_on.go:7-8` | `const SwissMap = true` / `const SwissMapInt = 1` | code |
| 9 | `src/internal/goexperiment/exp_swissmap_off.go:7-8` | `const SwissMap = false` / `const SwissMapInt = 0` | code |
| 10 | `src/internal/abi/map_select_noswiss.go:5,10` | `//go:build !goexperiment.swissmap` … `type mapType = OldMapType` | code |
| 11 | `src/runtime/map_noswiss.go:5` | `//go:build !goexperiment.swissmap` (file is 1891 lines) | code |
| 12 | `src/cmd/compile/internal/reflectdata/reflect.go:775-779` | `if buildcfg.Experiment.SwissMap { rt = rttype.SwissMapType } else { rt = rttype.OldMapType }` | code |
| 13 | `src/cmd/compile/internal/reflectdata/reflect.go:879-883` | `if buildcfg.Experiment.SwissMap { writeSwissMapType` … `writeOldMapType` | code |
| 14 | go1.24 notes, HTML line 572 (first `noswissmap` occurrence) | `may be disabled by setting GOEXPERIMENT=noswissmap` | docs |
| 15 | `src/internal/abi/map_swiss.go:32-43` | `type SwissMapType struct {` … `GroupSize`, `SlotSize`, `ElemOff` | code |

Mechanism, read directly: `:101-106` turns **every** `Flags` field into a settable lower-case name;
`:131-132` strips a leading `no` and sets the field `false`; the baseline at `:85` is `true`, so
`noswissmap` is exactly the intended spelling; `:187` re-emits it as `"no"+name`. `exp.go` upstream bytes
are identical to the installed copy (`sha256 db71987c0caabdb6173fbd2a945a0c8b44dcbb526eae9a8ec95e14f4c3fb393c`),
so installed line numbers are go1.25.0 line numbers.

## Commands and exit codes

Fetches (all HTTP 200, exit 0):

```
curl -sS https://go.dev/doc/go1.25 -> 71574 bytes, HTTP:200, EXIT:0
  sha256 c9d872d374a3d52bbd5e1fad7d99b9eb44a7dac45d7032314d8cacd0702d38fd   # == digest recorded in SOURCES S031
curl -sS https://go.dev/doc/go1.24 -> 82634 bytes, HTTP:200, EXIT:0
  sha256 d35c2d52a864b3474451e28fb89bae013edba4adcc1fa7164796267c0e4ec4e7
curl raw .../go1.25.0/src/internal/buildcfg/exp.go -> 6303 bytes, HTTP:200, EXIT:0
  sha256 == installed db71987c…; diff -u installed upstream -> DIFFEXIT:0
curl raw .../go1.25.0/src/runtime/map_noswiss.go -> 58975 bytes, HTTP:200, EXIT:0
  sha256 == installed 3e2aa723… (whole-file cmp, no diff)
curl raw for reflect.go, map_select_noswiss.go, flags.go, map_swiss.go -> all HTTP:200, EXIT:0, all IDENTICAL:
  reflect.go db3f307175228e7f5781d3dc1777f2bdfb5f7457e74c60c9362072c3f581be4b
  map_select_noswiss.go b8a433106c57585b8da857321f48bbeae4cc18050c1c02ee9b0700e2103b974f
  flags.go 818253f229fe504d6f066e2820efa5bc5d9ef325b231d99b25012eba51bb8877
  map_swiss.go f97713fa86ada07e992c69b021732a7c09f2ac6bdbfa6980a0f6538875c4d29b
```

Release-note searches (**the negative result is the point**):

```
grep -c -i swiss go125.html                      -> 0        (grep exits 1 on zero matches)
grep -o -i '\bmap\b' go125.html | wc -l          -> 1        (unicode "CategoryAliases map provides…")
grep -o -i 'goexperiment[^<]{0,80}' go125.html   -> greenteagc, nodwarf5, synctest, jsonv2  (no swissmap)
grep -c -i swiss go1.26.html / go1.27.html       -> 0 / 0    (HTTP 200 each; combined EXIT:1 from the last grep -c)
```

Toolchain, installed go1.25.0 (`/home/vgpnk/.local/opt/go-1.25.0`, `VERSION` = `go1.25.0`, time 2025-08-08T19:33:32Z):

```
go version                                            -> go version go1.25.0 linux/amd64      EXIT:0
go env GOEXPERIMENT                                   -> (empty)                              EXIT:0
GOEXPERIMENT=noswissmap go env GOEXPERIMENT           -> noswissmap                           EXIT:0
GOEXPERIMENT=noswissmap go tool compile -p main m.go  -> (no output)                          EXIT:0
go tool compile -p main m.go                          -> (no output)                          EXIT:0
  # objects differ: 5d9756a0… (noswiss) vs 0b8b2be7… (default)
GOEXPERIMENT=noswissmap go build -o probe_noswiss .   -> real 1.675s (user 27.5s; fresh GOCACHE, dependency graph recompiled) EXIT:0
go build -o probe_swiss .                             -> real 1.526s                          EXIT:0
./probe_noswiss                                       -> 2 3                                  EXIT:0
go version -m probe_noswiss                           -> go1.25.0 X:noswissmap
go version -m probe_swiss                             -> go1.25.0            (no X: token)
GOEXPERIMENT=noswissmap go build (twice, same env)     -> det_a == det_b, sha256 613207ec…, cmp EXIT:0
```

File selection, i.e. the observable that separates the pair:

```
go list -f '{{join .GoFiles " "}}' runtime | grep map
  default   -> map_fast32_swiss.go map_fast64_swiss.go map_faststr_swiss.go map_swiss.go mbitmap.go tracemap.go
  noswissmap-> map_fast32_noswiss.go map_fast64_noswiss.go map_faststr_noswiss.go map_noswiss.go …   (both EXIT:0)
go list -f … internal/abi | grep map
  default    -> map_noswiss.go map_select_swiss.go map_swiss.go
  noswissmap -> map_noswiss.go map_select_noswiss.go map_swiss.go
tag census: 18 files `//go:build goexperiment.swissmap`, 12 files `//go:build !goexperiment.swissmap`
```

Runtime fingerprint of the two linked binaries (`go tool nm`):

```
internal/runtime/maps.* symbols      : swiss 36   noswiss 5  (only mapKeyError2, typeString, unhashableTypeError + itab)
runtime.mapaccess*/mapassign* symbols: swiss 12   noswiss 13
internal/abi.OldMapType/SwissMapType type symbols: 0 in both
```

Control toolchain, clean re-run (`GOTOOLCHAIN=local`, cwd `/tmp`):

```
go1.24.6 go version                              -> go version go1.24.6 linux/amd64   EXIT:0
GOTOOLCHAIN=local GOEXPERIMENT=noswissmap go env GOEXPERIMENT GOVERSION -> noswissmap / go1.24.6  EXIT:0
GOTOOLCHAIN=local go env GOEXPERIMENT            -> (empty)                           EXIT:0
1.24.6 src/runtime/map_noswiss.go:5              -> //go:build !goexperiment.swissmap
1.24.6 exp.go:76,81                              -> baseline := goexperiment.Flags{ … SwissMap: true
```

## Calibration notes for the round (each with the observation it rests on)

1. **Release-notes silence is verified, not assumed.** `grep -c -i swiss` on the 1.25 page is `0`; its only
   `\bmap\b` is the unicode `CategoryAliases map`. The 1.25 page bytes are the same snapshot already
   registered as S031 (`sha256 c9d872d3…`), so S031's page cannot ground a swiss/map claim — only DWARF 5.
   **[INF]** The claim "1.25 still supports noswissmap" must be anchored on the 1.25 *tree* (+ the 1.24
   notes sentence), never on the 1.25 notes.
2. **`OldMapType` is byte-identical between go1.24.6 and go1.25.0.** `internal/abi/map_noswiss.go` whole-file
   `diff` is empty (`DIFFEXIT:0`); `OldMapType` fields at `:25-36` are `Type, Key, Elem, Bucket, Hasher,
   KeySize, ValueSize, BucketSize, Flags` in both. **[INF]** In the 8-carrier matrix the two `noswiss` rows
   are layout-matched across compiler versions; a difference between `s1246-noswiss-*` and `s1250-noswiss-*`
   is a compiler-emission effect, not a map-layout effect.
3. **Name presence is not a discriminator.** `go list` shows `internal/abi` compiles *both* `map_noswiss.go`
   and `map_swiss.go` in *both* configurations (`map_swiss.go:5` has no build tag); only the alias file
   (`map_select_{swiss,noswiss}.go`) is tagged. **[INF]** Any `swiss-misread.py`/symbol heuristic that infers
   "true kind" from whether `OldMapType`/`SwissMapType` *names* exist would be wrong; the correct witnesses are
   the map-type descriptor that `reflect.go:879-883` writes for `TMAP` and the runtime symbol set in the
   `go tool nm` rows above (36 vs 5 `internal/runtime/maps.*`).
4. **Build-info token matches the S026 rule.** `go version -m` on the noswiss build prints
   `go1.25.0 X:noswissmap` (space separator, no dash because the version has no prerelease suffix); the swiss
   build prints plain `go1.25.0`. **[INF]** This is a free, receipt-grade discriminator for the C3 labels, and
   a check that a carrier was really built with the intended setting.
5. **Rebuilds are byte-deterministic** under `GOEXPERIMENT=noswissmap` with `-trimpath -buildvcs=false` and a
   stable env: two builds gave the identical sha256 `613207ec…` (`cmp` exit 0). A *different* pair of builds
   did differ, but only because flags/env differed (`-trimpath -buildvcs=false` and distinct GOCACHE/GOPATH);
   **[INF]** that is not evidence against the recipe's determinism.
6. **Toolchain-identity hazard (self-inflicted, worth a lesson).** Running
   `/home/vgpnk/.local/opt/go-1.24.6/bin/go env GOEXPERIMENT` with cwd inside
   `/home/vgpnk/.local/opt/go-1.25.0/src` printed `go: downloading go1.25.0 (linux/amd64)` and answered with
   **go1.25.0**, because that directory's `src/go.mod` says `go 1.25` and `GOTOOLCHAIN` defaults to `auto`.
   **[OBS]** The C3 recipe is already immune: `carriers/build.sh:19` passes `GOTOOLCHAIN=local`, `GOENV=off`,
   `GOFLAGS=`, `CGO_ENABLED=0`, `GOOS/GOARCH/GOAMD64`, and `GOEXPERIMENT="$exp"` under `env -i`. **[INF]**
   Any ad-hoc toolchain probe should set `GOTOOLCHAIN=local` or run outside a module, else version identity is
   silently wrong — exactly the confusion this item is about.

## Draft source row (only if the L1 wants a new row)

**[INF]** A row *is* warranted for the support question, but it must **not** duplicate the two sibling scribe
items: `ScoutGo124NotesSwiss`/`DraftGoNotesRow` own the 1.24-notes docs row, and `DraftAbiRow` owns a code row
for the `SwissMapType`/`OldMapType` descriptor layouts. The unowned surface is the **selection mechanism**
(buildcfg name parsing + tagged file swap + compiler emission). Next free id is `S033`; if `DraftAbiRow` takes
it, renumber this to `S034`. 11 columns, matching `corpus/SOURCES.md`:

```
| S033 | Go 1.25.0 source tree, map-experiment selection — https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/buildcfg/exp.go; `src/cmd/compile/internal/reflectdata/reflect.go`; `src/internal/abi/map_select_noswiss.go`; `src/runtime/map_noswiss.go` | code | A | Whether Go 1.25 still honours `GOEXPERIMENT=noswissmap`, and how a build's map implementation and map-type descriptor are selected | go1.25.0 `exp.go:81-85` baseline `SwissMap: true`; `:101-106` every `Flags` field becomes a settable name; `:131-132` leading `no` clears it; `:187` `"no"+name`; `reflect.go:775-779` and `:879-883` choose `rttype.OldMapType`/`writeOldMapType`; `map_select_noswiss.go:5,10` `//go:build !goexperiment.swissmap` and `type mapType = OldMapType`; `runtime/map_noswiss.go:5` same tag, 1891 lines. Upstream bytes equal installed bytes (sha256 `db71987c…`, `db3f3071…`, `b8a43310…`, `3e2aa723…`) | The opt-out survives 1.25 as a first-class experiment: it clears a baseline-true flag, swaps in the build-tagged old implementation, and makes the compiler emit the `OldMapType` descriptor; the installed go1.25.0 rebuilds `std`, links and runs with it, and records `X:noswissmap`. | mined | 2026-10-20 | on-release | .ufo/waves/round-18/w1/ScoutGo125MapsNotes.md |
```

Gate-style quote line (≤25 words, located): `SwissMap:        true,` — `go1.25.0 src/internal/buildcfg/exp.go:85`.

## Limits / remaining unknowns

- **[OBS]** I did not fetch the 75 MB go1.25.0 tarball or re-check its digest; installed-tree provenance rests on
  `VERSION` (`go1.25.0`, `2025-08-08T19:33:32Z`) plus byte-identity of the six cited files to
  `raw.githubusercontent.com/golang/go/go1.25.0`. The tarball digest claim in `build.sh` was not re-verified here.
- **[OBS]** No `cmd/go` rejection path was probed beyond the end-to-end acceptance above; acceptance is proven
  empirically, rejection semantics were not exercised.
- **[OBS]** No carrier was built or executed, no REA/Ghidra run was made; the symbol counts come from my own
  two throwaway binaries built in `/tmp` from a 5-line map program.
- **[INF]** Whether Go 1.25's `noswissmap` builds are *semantically* identical to go1.24.6's is not shown by
  layout equality alone; the pair remains a compiler-version comparison, which is what the 8-carrier design
  wants.
