# ReopenS035 — SOURCES row S035 re-open (round 18, wave 2)

HOLDS

Seat: KaidokuR18.ReopenS035. REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, baseline `9011581d84527ba34c675f9cf912e54d2e72d470`. This was a read-only check; this report is the only file I wrote. I ran every command on 2026-10-20. In the working tree, both cited corpus files match REV byte for byte (check 1), so working-tree line numbers are the same as REV line numbers. `G=/home/vgpnk/.local/opt/go-1.25.0/src` and `A=/home/vgpnk/.local/opt/go-1.24.6/src` below.

## Verdict

HOLDS. Every field of SOURCES row S035 checks out at REV:
- all three sha256 digests match both the local tree and upstream tag `go1.25.0`;
- the published tarball digest matches;
- `map_swiss.go` and `map_noswiss.go` are byte-identical between go1.24.6 and go1.25.0;
- all four anchor groups sit on exactly the stated lines;
- tier, kind, scope, teaches, status and used-by are all consistent.

I agree with the decision "admit (mined)" at `corpus/lessons/round-18.md:24`.

Findings: one minor citation-precision defect in the lessons Gate quote table (F1), plus two notes (F2, F3). None of them touches what the row claims, and none changes the verdict.

## Row under test

OBSERVATION. The row is `corpus/SOURCES.md:41` at REV. The column header is at `:5`: `id|source|kind|tier|scope|anchor|teaches|status|opened|recheck|used-by`.
- source: Go 1.24.6 and 1.25.0 `internal/abi` map type descriptors, at `/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/`. The row says `map_swiss.go`/`map_noswiss.go` are byte-identical in `…/go-1.24.6/src/internal/abi/`, and gives upstream `https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/`.
- kind `code`, tier `A`.
- scope: the toolchains' own `SwissMapType`/`OldMapType` structs, the build-tag alias that selects `mapType`, and where `Type.Uncommon()` places uncommon data for a map. Excluded: Ghidra's reader and 32-bit layouts.
- anchor: "go1.25.0 official tarball". sha256 of `map_swiss.go` is `0e2fedbe…76c383`, of `map_noswiss.go` is `03db5a82…5a7291`, of `map_select_swiss.go` is `c16b55b8…af799718`. Line anchors: `map_swiss.go:32`, `map_noswiss.go:25`, `map_select_swiss.go:5,22`, `type.go:358-363`.
- teaches: "On amd64 the Swiss descriptor is 112 bytes and the old one 88, and a map's uncommon block follows its own descriptor, so a reader bound to the 88-byte struct looks for uncommon data 24 bytes early on a Swiss binary."
- status `mined`, opened `2026-10-20`, recheck `on-release`. used-by: `corpus/lessons/round-18.md`, `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`.

## Checks (each command → its exit code → result)

### 1. Row exists at REV; working tree matches REV

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git rev-parse HEAD
b2aad08ceeee8dd125ce0d316056d8bd766c7f94                                   # exit 0
$ git status --porcelain -- corpus/SOURCES.md corpus/lessons/round-18.md    # (empty) exit 0
$ git diff HEAD --stat -- corpus/SOURCES.md corpus/lessons/round-18.md      # (empty) exit 0
$ git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:corpus/SOURCES.md | grep -n "S035"
41:| S035 | Go 1.24.6 and 1.25.0 `internal/abi` map type descriptors — …
49:- Swiss-map replay — S034 → S035 → S023 → S003 → S033: …                # exit 0
```

### 2. Anchor digests match, locally and upstream

```
$ sha256sum $G/internal/abi/map_swiss.go $G/internal/abi/map_noswiss.go $G/internal/abi/map_select_swiss.go $G/internal/abi/map_select_noswiss.go
0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383  …/map_swiss.go
03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291  …/map_noswiss.go
c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718  …/map_select_swiss.go
b8a433106c57585b8da857321f48bbeae4cc18050c1c02ee9b0700e2103b974f  …/map_select_noswiss.go   # exit 0
$ curl -s --max-time 20 https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/map_select_swiss.go | sha256sum
c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718  -        # exit 0
$ for f in map_swiss.go map_noswiss.go; do curl -s --max-time 20 "https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/$f" | sha256sum | sed "s/-/$f/"; done
0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383  map_swiss.go
03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291  map_noswiss.go       # exit 0
$ curl -s --max-time 20 https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/type.go | sha256sum
6f3e3d720b4ba23750593d77dcc8e844fdfa18581a17e045e21b68c7f6cc603c  -        # exit 0 (== local $G/internal/abi/type.go, check 4)
```

OBSERVATION: the three digests in the row match both the local tree and upstream tag `go1.25.0`. Upstream `type.go`, which holds the `:358-363` anchor, also matches the local file.

### 3. "go1.25.0 official tarball" provenance

```
$ sha256sum /tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz
2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  …        # exit 0
$ python3 -I -B -c "import json; d=json.load(open('/tmp/kr18-dl/dl.json')); [print(f['filename'], f['sha256'], f.get('size')) for rel in d for f in rel.get('files',[]) if f.get('filename')=='go1.25.0.linux-amd64.tar.gz']"
go1.25.0.linux-amd64.tar.gz 2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613 59659213   # exit 0
$ cat /home/vgpnk/.local/opt/go-1.25.0/VERSION
go1.25.0
time 2025-08-08T19:33:32Z                                                  # exit 0
```

The same two commands for go1.24.6 give `bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712` in both places (size 78583176, both exit 0).

OBSERVATION: the tarball on disk has the digest that go.dev/dl publishes. `dl.json` is the copy L1 fetched, still in `/tmp/kr18-dl/`. This matches the w1 record at `.ufo/waves/round-18/w1/SentinelReaEnv.md:73-77`. Check 2 adds that the extracted files match the upstream tag files.

### 4. Byte-identity across the two toolchains

```
$ sha256sum $A/internal/abi/map_swiss.go $A/internal/abi/map_noswiss.go
0e2fedbe…76c383  map_swiss.go    03db5a82…5a7291  map_noswiss.go           # exit 0 (== go1.25.0)
$ for f in map_swiss.go map_noswiss.go type.go; do curl -s --max-time 20 "https://raw.githubusercontent.com/golang/go/go1.24.6/src/internal/abi/$f" | sha256sum | sed "s/-/go1.24.6:$f/"; done
0e2fedbe…76c383  go1.24.6:map_swiss.go   03db5a82…5a7291  go1.24.6:map_noswiss.go
44ee183a5a3567f6c1e3cc7ca813cbaabcb3834516442ce447ecb5631aa5a2a9  go1.24.6:type.go   # exit 0
$ sha256sum $A/internal/abi/map_select_swiss.go $A/internal/abi/map_select_noswiss.go $G/internal/abi/map_select_noswiss.go
c16b55b8…af799718  b8a43310…b974f  b8a43310…b974f                          # exit 0
$ sha256sum $A/internal/abi/type.go $G/internal/abi/type.go $A/internal/abi/compiletype.go $G/internal/abi/compiletype.go
44ee183a…a5a2a9  6f3e3d72…6cc603c  0988077c…223f10  0988077c…223f10        # exit 0
```

OBSERVATION: the row's byte-identity claim holds for the two files it names, both locally and against upstream tag `go1.24.6`. Two more files that the row does not mention are also identical across the toolchains: `map_select_*.go` and `compiletype.go`. `type.go` is not identical (see F3).

### 5. Anchor line numbers (go1.25.0 tree)

```
$ awk 'NR==32 {printf "%d: %s\n", NR, $0}' $G/internal/abi/map_swiss.go
32: type SwissMapType struct {                                              # exit 0
$ awk 'NR==25 {printf "%d: %s\n", NR, $0}' $G/internal/abi/map_noswiss.go
25: type OldMapType struct {                                                # exit 0
$ awk 'NR==5 || NR==22 {printf "%d: %s\n", NR, $0}' $G/internal/abi/map_select_swiss.go
5: //go:build goexperiment.swissmap
22: type mapType = SwissMapType                                             # exit 0
$ awk 'NR>=358 && NR<=363 {printf "%d: %s\n", NR, $0}' $G/internal/abi/type.go
358: 	case Map:
359: 		type u struct {
360: 			mapType
361: 			u UncommonType
362: 		}
363: 		return &(*u)(unsafe.Pointer(t)).u                               # exit 0
$ awk 'NR>=321 && NR<=324 {printf "%d: %s\n", NR, $0}' $G/internal/abi/type.go
321: func (t *Type) Uncommon() *UncommonType {
322: 	if t.TFlag&TFlagUncommon == 0 {
323: 		return nil
324: 	}                                                                   # exit 0
```

OBSERVATION: all four anchor groups land exactly. The Map case at 358-363 is inside the switch of `Uncommon()` (`:321`). That supports the scope phrase "where `Type.Uncommon()` places uncommon data".

### 6. Teaches: 112 / 88 / 24 bytes early

```
$ grep -n "func CommonSize\|func UncommonSize" $G/internal/abi/compiletype.go
15:func CommonSize(ptrSize int) int { return 4*ptrSize + 8 + 8 }
22:func UncommonSize() uint64 { return 4 + 2 + 2 + 4 + 4 }                  # exit 0
$ grep -n "func commonsize" $G/cmd/link/internal/ld/decodesym.go
35:func commonsize(arch *sys.Arch) int      { return abi.CommonSize(arch.PtrSize) }      // runtime._type   # exit 0
$ awk 'NR>=562 && NR<=570 {printf "%d: %s\n", NR, $0}' $G/cmd/link/internal/ld/deadcode.go
562: 	case abi.Map:
563: 		if buildcfg.Experiment.SwissMap {
564: 			off += 7*arch.PtrSize + 4 // internal/abi.SwissMapType
565: 			if arch.PtrSize == 8 {
566: 				off += 4 // padding for final uint32 field (Flags).
567: 			}
568: 		} else {
569: 			off += 4*arch.PtrSize + 8 // internal/abi.OldMapType
570: 		}                                                               # exit 0
$ grep -n "internal/abi.SwissMapType\|internal/abi.OldMapType" $A/cmd/link/internal/ld/deadcode.go
564:			off += 7*arch.PtrSize + 4 // internal/abi.SwissMapType
569:			off += 4*arch.PtrSize + 8 // internal/abi.OldMapType            # exit 0
```

- Arithmetic from the source:
  - `Type` is `CommonSize(8)` = 48 bytes. Per `type.go:20-45`: four pointer-width fields, then 8 bytes of hash/flags/kind, then 8 bytes of Str/PtrToThis.
  - `SwissMapType` (`map_swiss.go:32-43`) adds 7 pointer-width fields and a uint32: 48+56+4 = 108, padded to **112**.
  - `OldMapType` (`map_noswiss.go:25-36`) adds 4 pointer-width fields plus 1+1+2+4 bytes: 48+32+8 = **88**.
- The linker's own `decodetypeMethods` (`deadcode.go:562-570`, the same lines in go1.24.6) computes a map type's uncommon offset with exactly these numbers. It even comments on the amd64 Flags padding. This is an independent upstream statement of +112 for Swiss and +88 for old. Neither the row nor w1 `DraftAbiRow.md` cites this site; I found it during this re-open.
- w1 measured the same sizes with a mirror probe: amd64 112/88, 386 64/56 (`.ufo/waves/round-18/w1/DraftAbiRow.md`, "Measurement"). The 386 result is consistent with the row excluding "32-bit layouts".

INFERENCE: 112 − 88 = 24. A reader that looks for uncommon data at descriptor+88 on a Swiss binary therefore reads 24 bytes early and lands on `SlotSize`, which is at offset 88 in `SwissMapType` (`map_swiss.go:40`). This row grounds the abi-source half of the teaches sentence. The reader half (Ghidra binds `OldMapType`) belongs to S023/S003 and C3, which this row's scope excludes.

### 7. Lessons Gate: decision and quotes

```
$ grep -n "S035" corpus/lessons/round-18.md
10:- C3 depth (the filed sourced claim, S034/S035, with S023/S003/S033): …
24:| SOURCES S033 (supersedes S032), S034, S035, S036 | admit (mined) | Opened 2026-10-20; quotes below |
36:| S035 | go1.25.0 `src/internal/abi/map_select_swiss.go:22` | type mapType = SwissMapType |
37:| S035 | go1.25.0 `src/internal/abi/type.go:358-361` | case Map: type u struct { mapType u UncommonType } |   # exit 0
$ grep -n "Rows 32 → 36\|^## Gate\|^### Registry changes" corpus/lessons/round-18.md
12:## Gate   40:### Registry changes (old → new)   43:- New rows S033–S036 (3 tier A, 1 tier B community). Rows 32 → 36.   # exit 0
$ git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:corpus/SOURCES.md | grep -c "^| S0"     # 36, exit 0
$ git show 9011581d84527ba34c675f9cf912e54d2e72d470:corpus/SOURCES.md | grep -c "^| S0"     # 32, exit 0
```

- Decision (`:24`, under `## Gate` at `:12`): "admit (mined)". This agrees with the row's status `mined` and opened date 2026-10-20. The registry bullet at `:43` ("Rows 32 → 36") matches the counts at REV and baseline.
- Quote 1 (`:36`): "type mapType = SwissMapType", 4 tokens. It matches `map_select_swiss.go:22` byte for byte.
- Quote 2 (`:37`): "case Map: type u struct { mapType u UncommonType }", 10 tokens. It is the contiguous source with whitespace flattened. Both quotes are under the 25-word cap. The cited line range is off by one (F1).
- Used-by: the knowledge entry cites S035 with the same anchors and the 112 B / 88 B figures (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:1,18`). `.ufo/waves/round-18/claims.json` `amendments[0].sourced` reads "C3 S034/S035 … C3 is the filed sourced claim". Both agree with the row.

## Findings

### F1: minor citation-precision defect in the lessons Gate quote table (not in the SOURCES row)

OBSERVATION: `corpus/lessons/round-18.md:37` anchors its quote at `type.go:358-361`. The quote ends with `}`, which is line 362 (check 5). Flattened, lines 358-361 stop at "…u UncommonType" with no closing brace.

Every other artifact cites the wider range:
- the SOURCES row itself (`corpus/SOURCES.md:41`, `358-363`);
- w1 `DraftAbiRow.md:14,29`;
- w1 `ConnSourcesPaths.md:23`;
- the knowledge entry (`:1`).

The other S0xx quotes follow the convention that the range covers the whole quote. For example, S034's quote is exactly raw lines 571-573 of go.dev/doc/go1.24: `curl -s --max-time 25 https://go.dev/doc/go1.24 | sed -n '571,573p'`, exit 0.

Reproduce:
- `awk 'NR>=358 && NR<=363' $G/internal/abi/type.go` (check 5);
- `grep -rn "358-361" corpus/ .ufo/waves/round-18/w1/` (exit 0). Its only hit is `corpus/lessons/round-18.md:37`. The scope leaves out `w2/` because this report quotes the string. An earlier unscoped run over `.ufo/waves/round-18/ corpus/`, made before this report existed, also hit only `:37`.

Severity: minor. The quote text is verbatim and within the cap, the row's own anchor is correct, and no decision depends on this label. Smallest fix: relabel `:37` as `type.go:358-362`.

### F2: note on anchor-column completeness (no defect)

OBSERVATION: the anchor column cites only the Swiss-side alias (`map_select_swiss.go:5,22`) and gives three digests. The counterpart alias, `type mapType = OldMapType` under `//go:build !goexperiment.swissmap`, is at `map_select_noswiss.go:5,10`. That file's sha256 is `b8a43310…b974f`, the same in both toolchains (checks 2 and 4). The Swiss side alone shows the alias mechanism that the scope names, and the knowledge entry and w1 draft cover the noswiss side, so the row overclaims nothing. I record the fourth file's identity here for whoever next edits the row.

### F3: note on the version scope of the `type.go` anchor (no defect)

OBSERVATION: `type.go:358-363` is a line number in the go1.25.0 tree. In go1.24.6, `type.go` differs (sha256 `44ee183a…` vs `6f3e3d72…`, check 4), and the same Map case sits at `:362-367`:

```
$ awk 'NR>=325 && NR<=329 || NR>=362 && NR<=367 {printf "%d: %s\n", NR, $0}' $A/internal/abi/type.go
325: func (t *Type) Uncommon() *UncommonType { … 362: 	case Map: … 364: 			mapType … 365: 			u UncommonType … 367: 		return &(*u)(unsafe.Pointer(t)).u   # exit 0
$ diff -u $A/internal/abi/type.go $G/internal/abi/type.go
@@ -187,11 +187,7 @@ TypeFor body (5 lines → 1)   @@ -487,7 +483,7 @@ comment "funcType"→"FuncType"   # exit 1 (differences: exactly these two hunks)
```

The only differences are the `TypeFor` body and one comment. Neither the `Type` struct nor the Map case changes, so the teaches sentence holds for both toolchains. The row is accurate: its byte-identity claim names only `map_swiss.go`/`map_noswiss.go`, and its anchors belong to the go1.25.0 location. Someone applying `:358-363` to the go1.24.6 tree would land 4 lines early.

## Verdict rationale

Every field of row S035 is confirmed by a reproducing command:
- digests: local, upstream for both tags, and the published tarball;
- byte-identity across the two toolchains;
- all four anchor groups;
- tier, kind, status and used-by;
- the teaches arithmetic, which now has three independent sources, including a linker site that neither the row nor w1 cited.

The Gate's "admit (mined)" decision is supported. F1 is a one-line range label in the lessons quote table and does not affect the row. F2 and F3 are notes for completeness.

## Installs

None. I installed and updated nothing; `sha256sum`, `curl`, `awk`, `grep`, `diff` and `python3` were already present.
