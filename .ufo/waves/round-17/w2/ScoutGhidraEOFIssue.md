# ScoutGhidraEOFIssue — upstream Ghidra search for the aether `Unable to read past EOF`

- Seat: `KaidokuR17.ScoutGhidraEOFIssue` (wave 2, leaf scout; no subagents, no edits outside this report).
- Lane revision: `da64646adcb19c1ede7537b799b8c7d283fe43da` (`git rev-parse HEAD` in the lane).
- Method: read-only. Network: github.com HTML (via `read`), `api.github.com/search/issues`, `raw.githubusercontent.com`. No REA analyze/search/decompile, no Ghidra, no carrier execution. Python run with `-B`; scratch under `/tmp/r17ghidra`. No tools installed.
- Labels: **[OBSERVED]** = reproduced from named file/command output; **[INFERENCE]** = follows from code/upstream but not directly observed for aether.

## Bottom line

1. **Exact signature: bounded no-finding.** No upstream issue or PR found by the queries below contains `Unable to read past EOF` together with `GoInterfaceType.additionalMarkup` / `ReflectionHelper.callGetter` (no commit-message search was attempted). The six issues matching the literal EOF phrase are import-file/PE reports **by title**; none mentions Go or these frames (titles in §Queries; bodies were not read after the API rate limit, so this is title-level, not body-level, exclusion).
2. **Mechanism: match.** Open PR **#9348** — “Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries” — documents the same defect class, the same stack frames (`GoInterfaceType.additionalMarkup:77` → `GoName.getPkgPath:124` → `GoRttiMapper.resolveNameOff`), and the same carrier population (stripped Go 1.25, Ghidra before the fix). URL: <https://github.com/NationalSecurityAgency/ghidra/pull/9348>, **opened 2026-07-05**, 3 commits (latest push **2026-08-31**), **still Open**; labels `Feature: Language/Go`, `Status: Triage`.
3. Upstream root cause [OBSERVED in PR body, corroborated locally]: `GoMapType`’s `@StructureMapping` candidate list lacks `internal/abi.SwissMapType`; for Go 1.24/1.25 default builds the 112-byte swiss map RTTI is therefore read as the 88-byte `internal/abi.OldMapType` (**24-byte under-read**), `findUnindexedClosureStructTypes()` indexes phantom types from the phantom gap, one phantom `pkgPath` name offset is garbage, and `GoName.readStructure()` throws; because `markupGoTypes()` runs before function naming under one `try/catch`, that exception aborts the whole Go pass (zero symbols).
4. The lane artifacts’ “cause UNKNOWN” (`SKILL.md:524`, knowledge `:90`, `lessons/round-17.md:33`, `LOG.md:2049-2050`) is therefore **falsified as unknown**: the cause is an upstream-documented open defect, absent from the installed 12.1.4 and still absent from upstream `master` (verified by raw fetch). It is **not** the 1.25.0 snapshot fallback (the installed 1.25.0 snapshot already contains `SwissMapType`; the mapping code simply never selects it).
5. **Calibration caveat that matters for any backport:** aether is a variant of the failure class documented by PR #9348. Its bogus `nameOff = 0x780100` lands **inside** the module’s `[types, etypes)` region, so PR #9348’s `resolveNameOff` bounds guard (commit `a94872c`) would **not** fire for this instance. Only the `SwissMapType` mapping fix (primary) and the per-type `try/catch` (graceful degradation) address aether’s failure.

## Failure chain, reconstructed locally

Log: `.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log` (sha256 `f39c329338a7fc2262eceaaa681a8ad9328feef05b61ebbaba4417e2a9f0b4ed`).

| Log line | Frame |
|---|---|
| 92-93 | `WARN Falling back from 1.25.14 to 1.25.0`; `INFO Using Go API snapshot for version 1.25.14` |
| 94-95 | `Discovered 188 unindexed Go types`; `Found 6115 Go types` |
| 97 | `ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException` |
| 98-99, 175 | `ReflectionHelper.callGetter` (330, 317, 323) |
| 100-101 | `FieldMappingInfo.addRefToFieldWithGetter:296` / `lambda$makeMarkupReferenceFunc$6:290` |
| 124, 138 | `GoInterfaceType.additionalMarkup(GoInterfaceType.java:77)` |
| 147 | `GoStructType.additionalMarkup(GoStructType.java:94)` |
| 154-155 | `GoTypeManager.markupGoTypes(GoTypeManager.java:153)`; `GolangSymbolAnalyzer.added(GolangSymbolAnalyzer.java:146)` |
| 177 | `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854` |
| 178-181 | `MemoryByteProvider.ensureBounds:312` → `readBytes:265` → `BinaryReader.readByteArray:1173` → `readNextByteArray:704` |
| 182-183 | `GoVarlenString.readFrom:71` / `readStructure:57` |
| 188 | `GoName.readStructure(GoName.java:95)` |
| 193-196 | `DataTypeMapper.readStructure:449` → `GoRttiMapper.getGoName:1074` → `resolveNameOff:1063` → `GoName.getPkgPath:124` |
| 207 | `INFO (GolangStringAnalyzer) Go strings found: 7200` |
| 238 | `REPORT: Analysis succeeded for file: ...` (the analyzer failure is caught; the import succeeds) |

### Byte-level reconstruction [OBSERVED]

`MemoryByteProvider` is built from `program.getImageBase().getAddressSpace()` (`DataTypeMapper.java:511-513`), whose base is the space minimum (0), so the EOF index is the **virtual address**. `ensureBounds` prints `index, length` (`MemoryByteProvider.java:311-312`).

```text
$ python3 -B - <<'PY'
import struct
b = open('/usr/bin/aether', 'rb').read()
print('pcHeader magic', b[0xfb9580:0xfb9590].hex(' '), 'u32', hex(struct.unpack_from('<I', b, 0xfb9580)[0]))
target = 0x13b9580
cands = []
for name, va, off, size in [('data', 0x17016e0, 0x13016e0, 0x22104),
                            ('noptrdata', 0x1723f40, 0x1323f40, 0x97ca1)]:
    d = b[off:off + size]
    needle = struct.pack('<Q', target)
    i = d.find(needle)
    while i != -1:
        cands.append((name, va + i, off + i))
        i = d.find(needle, i + 1)
print('ptr candidates', [(n, hex(a)) for n, a, o in cands])
for name, va, fo in cands:
    o = fo
    pc = struct.unpack_from('<Q', b, o)[0]
    fn = struct.unpack_from('<QQ', b, o + 8)
    pcln = struct.unpack_from('<QQ', b, o + 104)
    minpc, maxpc, text, etext = struct.unpack_from('<QQQQ', b, o + 160)
    types, etypes, rodata, gofunc = struct.unpack_from('<QQQQ', b, o + 296)
    end = struct.unpack_from('<Q', b, o + 272)[0]
    print('cand vaddr', hex(va), 'file', hex(fo))
    print('pcHeader', hex(pc), 'funcnametab', hex(fn[0]), fn[1], 'pclntable', hex(pcln[0]), pcln[1])
    print('minpc', hex(minpc), 'maxpc', hex(maxpc), 'text', hex(text), 'etext', hex(etext))
    print('types', hex(types), 'etypes', hex(etypes), 'rodata', hex(rodata), 'gofunc', hex(gofunc), 'end', hex(end))
    print('0x10d4120 in types range:', types <= 0x10d4120 < etypes,
          'off from types', hex(0x10d4120 - types))
foff = 0x10d4125 - 0x400000
start = foff - 4
v = 0; sh = 0
for c in b[start:foff]:
    v |= (c & 0x7f) << sh; sh += 7
print('LEB bytes', b[start:foff].hex(' '), 'value', v)
print('GoName flags byte', hex(b[start - 1]), 'undefined bits', hex(b[start - 1] & ~0x0f))
print('EOF index', 0x10d4125, 'length', 111938854, 'index+length-1', hex(0x10d4125 + 111938854 - 1))
PY
pcHeader magic f1 ff ff ff 00 00 01 08 e2 30 00 00 00 00 00 00 u32 0xfffffff1
ptr candidates [('noptrdata', '0x172e400')]
cand vaddr 0x172e400 file 0x132e400
pcHeader 0x13b9580 funcnametab 0x13b95e0 629344 pclntable 0x15e0160 1168872
minpc 0x408ee0 maxpc 0x94fb01 text 0x408ee0 etext 0x94fb10
types 0x954020 etypes 0x13b4999 rodata 0x954020 gofunc 0x12e8308 end 0x17ffda0
0x10d4120 in types range: True off from types 0x780100
LEB bytes a6 9a b0 35 value 111938854
GoName flags byte 0xf6 undefined bits 0xf0
EOF index 17645861 length 111938854 index+length-1 0x7b94e4a
```

`0x10d4120` is therefore the start of the bogus `GoName` that `resolveNameOff` reached:

- `0x10d4120` flags byte = `0xf6`; `GoName.Flag` defines only bits 0-3 (`GoName.java:26-30`), so bits `0xf0` are undefined and `HAS_PKGPATH` is spuriously set.
- `0x10d4121` starts the `name` varlen: bytes `a6 9a b0 35` (file offset `0xcd4121`, vaddr−0x400000) decode as LEB128 = **111938854 = 0x6ac0d26**.
- Reader pointer after the LEB = `0x10d4125` = **17645861**; `readNextByteArray(111938854)` then fails because `0x10d4125 + 0x6ac0d26 - 1 = 0x7b94e4a` exceeds the memory max `0x17ffda0`.

The log’s two numbers are reproduced exactly by the bytes at `0x10d4120`; no bracketing is needed. A real `GoName` cannot have flags `0xf6`, so the resolved offset is being parsed as a name spuriously.

### Why the PR’s bounds guard does not cover this instance [OBSERVED locally + INFERENCE from code]

- `resolveNameOff(structure, off)` computes `module.getTypesOffset() + off` and calls `getGoName` unconditionally (`GoRttiMapper.java:1053-1064`).
- aether: `types=0x954020`, `etypes=0x13b4999`, and the bogus target `0x10d4120` is **inside** that range at `+0x780100`. PR #9348 commit `a94872c` rejects only `nameStart < typesOffset || nameStart >= typesEndOffset`; it would return the same address here and `GoName.readStructure` would still throw. [INFERENCE: derived from the two code paths; the guard is not installed, so its behavior is not executed.]
- PR #9348’s reproducer comment gives an example garbage `pkgPath` of `0x30580201` in the reporter’s original binary, producing `Invalid index` at `GoName.java:94` (their logs: `Invalid index: 13209856`, `Invalid index: 818045441`) because the address is past the image. aether’s in-range garbage offset is why the retained signature differs (`Unable to read past EOF` in `GoVarlenString`). Same defect, different landing address.

### Installed 12.1.4 has the upstream defect [OBSERVED]

- `Ghidra/application.properties:17` → `application.version=12.1.4`; the run’s `analyze.json` records upstream Ghidra `12.1.4`.
- `GoMapType.java:33` candidate list: `{ "runtime.maptype", "internal/abi.MapType", "internal/abi.OldMapType" }` — **no `SwissMapType`** and **no `presentWhen` gating** in 12.1.4 (upstream master at least has the `presentWhen` gating; master still has the same candidate list, see below).
- Installed snapshot `Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json` (the base actually used after the fallback):
  - `internal/abi.SwissMapType` present: `Type, Key, Elem, Group, Hasher, GroupSize, SlotSize, ElemOff, Flags` → 48 + 7×8 + 4(+4 pad) = **112 bytes**.
  - `internal/abi.OldMapType` present: `Type, Key, Elem, Bucket, Hasher, KeySize, ValueSize, BucketSize, Flags` → 48 + 4×8 + 1+1+2 + 4 = **88 bytes**.
  - `runtime.maptype` is a **typedef/alias** `Target = internal/abi.OldMapType`; `internal/abi.MapType` is absent.
  - The PR’s precondition is therefore exactly reproduced from installed data: the candidate list skips the 112-byte layout and lands on the 88-byte one.
- Carrier corroboration: `/usr/bin/aether` contains the ASCII string `SwissMapType` 36 times and `OldMapType` 0 times; `go version -m` → `go1.25.14`, `buildmode=exe`; `readelf -SW` has **no `.symtab` and no `.strtab`** (stripped), matching the PR’s affected population. `SwissMapType` strings are also why a snapshot-regeneration theory is not needed: the 1.25.0 base already models the swiss layout.

### Consequence in this run [OBSERVED control flow + INFERENCE]

`GolangSymbolAnalyzer.added()` wraps `goTypes.markupGoTypes(...)` at line **146** and `markupGoFunctions(monitor)` at line **155** in one `try`; the `IOException` is caught at **181-182** (`Msg.error(this, "Go analysis failure", e);`) and the method returns false. Therefore `markupGoFunctions` **never ran** in this session: the retained `analyze.json` `procedure_count: 6445` is analysis output (function/procedure count), not a symbol-name count. Upstream’s table reports “3 named” for stock master on stripped Go 1.25; [INFERENCE] aether is in the same state (Go function names absent/FUN_*), while Go string recovery did run (7200, log:207). The lane’s knowledge entry already says “in-range bootstrap is not full recovery” (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:84-91`), so this is a sharpening, not a contradiction.

## Upstream artifacts (URLs + dates)

### Matching mechanism: PR #9348 (open, no released fix)

- <https://github.com/NationalSecurityAgency/ghidra/pull/9348> — “Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries”, author `kubrickfr`; **opened 2026-07-05**; assigned `dev747368` 2026-07-06; comments 2026-07-06/07/08/09; **3 commits pushed 2026-08-31**; **Open**, 3 commits, labels `Feature: Language/Go` + `Status: Triage`.
- PR body (quoted): swiss maps default since 1.24; `GoMapType` candidate list omits `internal/abi.SwissMapType`; `runtime.maptype` is a typedef “skipped by the `Structure`-typed lookup”; `internal/abi.MapType` absent from 1.24/1.25 snapshots; falls to 88-byte `OldMapType`; real struct 112 bytes; `findUnindexedClosureStructTypes()` scans the phantom gap; phantom `pkgPath` offset throws `EOFException`; `markupGoTypes()` runs before function naming under one try/catch → “that one exception rolls back the whole analyzer → zero symbols”.
- PR comment 2026-07-07 (reproducer, `origin/master@e6ee047`): stack includes `GoStructType.additionalMarkup:94`, `GoInterfaceType.additionalMarkup:77`, `GoTypeManager.markupGoTypes:168`, `GolangSymbolAnalyzer.added:146`, `Caused by: java.io.EOFException: Invalid index: 13209856`, `GoName.readStructure:94`, `resolveNameOff:1068`, `GoName.getPkgPath:124`. Same frames as aether except the EOF frame (in-range variant).
- Commits (all three in the PR diff):
  - `1aa79ff379c91d5057a04f9bd9d0be0372bc7bd4` — “Golang: don’t let one bad type abort all type markup” (`GoTypeManager.markupGoTypes` per-type `try/catch`).
  - `a94872c6b574b1b40cec00a7eb3fd0d279fa6b56` — “Golang: reject out-of-bounds rtti name offsets instead of throwing” (`GoRttiMapper.resolveNameOff` guard, diff hunk `@@ -1065,6 +1065,23 @@`; its inline comment names the observed population: “observed on stripped Go >= 1.25 binaries, where one rtti type’s pkgPath name offset reads as a large garbage value”; not sufficient for aether, §above).
  - `a214355498e84aa86280be0c31c955aaf94f2d12` — “Golang: resolve stripped 1.24/1.25 maps as SwissMapType” (primary fix; candidate list + layout gating).
- PR body notes a release backport branch `fix/golang-stripped-type-markup` based on `Ghidra_12.1.2_build` (not 12.1.4; clean application to the installed 12.1.4 is unverified).

### Related but different: issue #9219 (closed for Go 1.26)

- <https://github.com/NationalSecurityAgency/ghidra/issues/9219> — “GolangSymbolAnalyzer crashes on Go 1.26 binaries — EOFException in GoUncommonType”; opened 2026-05-24 by `CryptoJones`, **closed 2026-05-29 as completed in `c01cd470a586aa8038453db10926d18e601c5679`**, milestone **12.2**, assignee `dev747368`.
- Signature differs: `java.io.EOFException: Invalid index: 549696843` at `MemoryByteProvider.ensureBounds:302` → `GoName.readStructure:94` → `GoRttiMapper.getGoName:1079` → `resolveNameOff:1068` → `GoBaseType.getGoName:110`; suspected Go 1.26 `internal/abi.Type` layout change. The closing commit diff (`c01cd47.diff`, 256 lines; `GoTypeManager.init`, `GoArrayType`, `GoBaseType`, `GoChanType`, `GoFuncType`, `GoInterfaceType`, `GoMapType`, `GoPlainType`, `GoPointerType`, `GoSliceType`, `GoType`) has **no** `nameOff`/`pkgPath`/`typesEndOffset`/`Unable to read past EOF` hunk (`grep -n -i` over the diff returned nothing for those tokens). Not a fix for aether’s Go 1.25 defect.

### Release branch and master are still unfixed [OBSERVED, raw fetch 2026-10-20]

- Release branch `Ghidra_12.1.4_build` (HTTP 200 for all fetched files):
  - `GoMapType.java:33` has the same three-entry candidate list (`runtime.maptype`, `internal/abi.MapType`, `internal/abi.OldMapType`) — **no `SwissMapType`**.
  - `GoRttiMapper.java` and `GoTypeManager.java` are **byte-identical** to the installed 12.1.4 copies (`diff -q` empty); `grep "Ignoring out-of-bounds"` and `grep "Failed to markup Go type"` find nothing. The installed analyzer is therefore exactly the unfixed release branch, not a local variant.
  - `Ghidra_12.2_build` returns **HTTP 404** under that branch name (no claim beyond the missing branch).
- Master raw URLs fetched (each file): `https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/master/Ghidra/Features/Base/src/main/java/ghidra/app/util/bin/format/golang/rtti/<FILE>` for `GoName.java`, `GoVarlenString.java`, `GoRttiMapper.java`, `GoTypeManager.java`, and `types/GoMapType.java`:
  - `GoName.java` and `GoVarlenString.java`: `diff -u` against the installed 12.1.4 sources → **empty** (byte-identical).
- `master/GoRttiMapper.java`: `resolveNameOff` still `long nameStart = module.getTypesOffset() + off; return getGoName(nameStart);` (line 1067), **no bounds guard**; `grep "Ignoring out-of-bounds"` → no match.
- `master/GoTypeManager.java`: `markupGoTypes` (lines 162-170) still calls `markupSession.markup(goType, false)` with **no per-type try/catch**.
- `master/GoMapType.java:33`: candidate list still `{ "runtime.maptype", "internal/abi.MapType", "internal/abi.OldMapType" }` — **no `SwissMapType`**.
- Conclusion: the PR is unmerged; no released Ghidra contains the fix. 12.1.4 predates even the master changes that are present.

## Queries and bounded no-finding

All issue searches via `GET https://api.github.com/search/issues?q=<q>&per_page=N` on 2026-10-20 (local). The core REST API (issue/PR detail and comment endpoints) later returned HTTP 403 `API rate limit exceeded`; the search endpoint continued to return 200, and the results below are the successful responses.

| Exact query `q` | total | Hits |
|---|---|---|
| `repo:NationalSecurityAgency/ghidra "Unable to read past EOF"` | 6 | #6864 (closed 2024-08-29, import EOF), #8265 (closed 2025-06-17, PE import table), #7271 (closed 2024-12-09, Ghidra 11.2.1), #4733 (closed 2022-11-10), #5899 (closed 2023-10-21), #3911 (closed 2022-01-24) — **none Go** |
| `repo:NationalSecurityAgency/ghidra golang EOF` | 0 | — |
| `repo:NationalSecurityAgency/ghidra GoVarlenString` | 1 | #5847 (closed 2023-10-03, “Stackover flow while trying to map structs in golang”; not this signature) |
| `repo:NationalSecurityAgency/ghidra "Go analysis failure"` | 2 | #9348 (open 2026-07-05), #9219 (closed 2026-05-24) |
| `repo:NationalSecurityAgency/ghidra GoInterfaceType` | 1 | #9348 |
| `repo:NationalSecurityAgency/ghidra "AdditionalMarkup"` | 1 | #9348 |
| `repo:NationalSecurityAgency/ghidra resolveNameOff` | 3 | #9348, #9219, #5847 |
| `repo:NationalSecurityAgency/ghidra GoName EOFException` | 2 | #9348, #9219 |
| `repo:NationalSecurityAgency/ghidra SwissMapType` | 1 | #9348 (only artifact naming the primary fix) |

Non-API checks: `https://github.com/NationalSecurityAgency/ghidra/issues/9219` and `.../pull/9348` read as HTML (dates/status above); `.../pull/9348.diff` and `.../commit/c01cd47.diff` fetched as text. A `grep.app` code-search attempt returned **HTTP 429** (Vercel checkpoint) and is recorded as **unavailable**, not as absence.

No upstream artifact was found that contains the exact aether string pair. The no-finding is bounded to the issue/PR searches above, the raw `master` files named in this report, and two commit diffs; **no full commit-history walk was performed**. A future fix should most likely surface under one of the queries above, as a new commit/PR touching `GoMapType.java`/`GoRttiMapper.java`.

## Findings on the round-17 artifacts, severity, smallest fix

### F1 — “Cause UNKNOWN” for the aether EOF is now known (calibration, medium)

Targets (all at `da64646`):
- `SKILL.md:524` — “Cause unknown; strings may still be recovered”.
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:90` — “Cause: **UNKNOWN**.”
- `corpus/lessons/round-17.md:33` — “no control separates fallback data from carrier layout; recorded UNKNOWN”.
- `LOG.md:2049-2050` — “aether symbol-markup EOF after a successful fallback bootstrap (cause UNKNOWN).”

The cause is upstream-documented: `GoMapType` candidate-list omission of `internal/abi.SwissMapType` → 88-byte `OldMapType` under-read of the 112-byte swiss struct → phantom types → garbage `nameOff` → `GoName` EOF; fix is open PR #9348, not in installed 12.1.4 or master. The lane’s rejection of “1.25.0 fallback data caused it” (`knowledge:91`, `lessons:33`) is **correct and strengthened**: the fallback base snapshot already contains `SwissMapType`; the failure is code-side layout selection. No factual error is present in the retained observation: `observation.json` records the analyzer error, and `classification: snapshot_loaded` follows the round-17 contract rule (snapshot label present, no missing bootstrap); it is not a symbol-recovery claim. Only the UNKNOWN disposition is outdated.

**Smallest fix:** replace “cause UNKNOWN” in the four sites with one sentence + citation: “Known upstream open defect (GoMapType missing `internal/abi.SwissMapType`; PR #9348, 2026-07-05); affects stripped Go 1.24/1.25 binaries on installed 12.1.4 and current master (PR unmerged).” No tool change. Keep the existing “not the fallback data” hedge but cite the snapshot evidence.

### F2 — The obvious backport (bounds guard) would not fix aether’s variant (depth, medium)

Target: any future lane statement or backport that treats PR #9348’s `resolveNameOff` guard as sufficient. aether’s target `0x10d4120` is **inside** `[0x954020, 0x13b4999)` (`off 0x780100`), so `a94872c` would not fire; the `GoVarlenString` EOF would remain.

**Smallest fix:** if the lane ever backports, take all three commits and record that the primary is `a214355` (`SwissMapType` candidate), with `1aa79ff` (per-type catch) limiting blast radius; do not claim `a94872c` alone covers aether. Note that installed 12.1.4’s `GoMapType` also lacks the `Group`/`GroupSize`/`SlotSize`/`ElemOff` field mappings and the `presentWhen` gating present in the PR’s base, so a 12.1.4 backport is not a one-line candidate-list edit. If no backport, one caveat sentence in the knowledge entry suffices.

### F3 — “Symbol markup aborted” can be sharpened to “function naming never ran” (calibration, low)

Target: `SKILL.md:524` decision text and `knowledge:84-91`. Installed source shows the `GolangSymbolAnalyzer.added` `try` contains `markupGoTypes` (line 146) then `markupGoFunctions` (line 155); the `IOException` is caught at 181-182 and `markupGoFunctions` is skipped. The retained `analyze.json` `procedure_count: 6445` is not Go-naming evidence.

**Smallest fix:** change the decision text to “Go function naming skipped for the session (markupGoTypes threw); bootstrap/type discovery and Go strings still ran.” One line; source anchor `GolangSymbolAnalyzer.java:146,155,181-182`.

### F4 — Exact-signature no-finding (informational, low)

No upstream artifact contains the literal aether string pair; PR #9348’s reports use `Invalid index` at `GoName.readStructure:94` because their garbage offsets land outside the image, whereas aether’s lands in-range and fails later, in `GoVarlenString`. This is a variant distinction worth one sentence wherever the lane records the signature, so a future exact-string search does not read as “no match at all”.

**Smallest fix:** in the knowledge entry, record the normalized signature as “GoName pkgPath → out-of-range/garbage nameOff → EOF in GoName/GoVarlenString” with both observed variants; no new query tooling.

## Reproduction commands (exact)

```text
$ stat -c '%s bytes' /usr/bin/aether; sha256sum /usr/bin/aether; /home/vgpnk/.local/opt/go-1.27.3/bin/go version -m /usr/bin/aether | head -3; readelf -SW /usr/bin/aether | grep -c '\.symtab'
20694888 bytes
06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e  /usr/bin/aether
/usr/bin/aether: go1.25.14
	path	aether
	mod	aether	(devel)
0
```

```text
$ python3 -B -c "import json; T=json.load(open('/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json'))['all']['Types']; [print(k, [f['Name'] for f in T[k]['Fields']]) for k in ('internal/abi.SwissMapType','internal/abi.OldMapType')]; print('runtime.maptype:', T['runtime.maptype']); print('MapType present:', 'internal/abi.MapType' in T)"
internal/abi.SwissMapType ['Type', 'Key', 'Elem', 'Group', 'Hasher', 'GroupSize', 'SlotSize', 'ElemOff', 'Flags']
internal/abi.OldMapType ['Type', 'Key', 'Elem', 'Bucket', 'Hasher', 'KeySize', 'ValueSize', 'BucketSize', 'Flags']
runtime.maptype: {'Kind': 'alias', 'Target': 'internal/abi.OldMapType', 'Position': '$GOROOT/runtime/map_noswiss.go:68:6'}
MapType present: False
```

```text
$ cd /tmp/r17ghidra/src && grep -n 'structureName = { "runtime.maptype"' ghidra/app/util/bin/format/golang/rtti/types/GoMapType.java; grep -n 'markupSession.markup(goType' ghidra/app/util/bin/format/golang/rtti/GoTypeManager.java; grep -n 'markupGoTypes(markupSession\|markupGoFunctions(monitor)\|Go analysis failure' ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java; grep -n 'Unable to read past EOF' ghidra/app/util/bin/MemoryByteProvider.java
33:	structureName = { "runtime.maptype", "internal/abi.MapType", "internal/abi.OldMapType" }
153:			markupSession.markup(goType, false);
146:			goTypes.markupGoTypes(markupSession, monitor);
155:			markupGoFunctions(monitor);
182:			Msg.error(this, "Go analysis failure", e);
312:				"Unable to read past EOF: %s, %d".formatted(Long.toUnsignedString(index), length));
```

```text
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show da64646:SKILL.md | grep -n 'Cause unknown'; git show da64646:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -n 'Cause: \*\*UNKNOWN\*\*'; git show da64646:corpus/lessons/round-17.md | grep -n 'recorded UNKNOWN'; git show da64646:LOG.md | grep -n 'cause UNKNOWN'
524:| Bootstrap OK, then `Go analysis failure …` | Symbol markup aborted after bootstrap (aether 1.25.14) | Cause unknown; strings may still be recovered |
90:  Go string recovery still ran (`Go strings found: 7200`). Cause: **UNKNOWN**.
33:| "aether's symbol-markup EOF is caused by 1.25.0 fallback data" | reject | Unpredicted; no control separates fallback data from carrier layout; recorded UNKNOWN |
2050:  successful fallback bootstrap (cause UNKNOWN).
```

GitHub search (exact form used; the `q` values are the table in §Queries):

```text
$ curl -sS -m 25 -H 'Accept: application/vnd.github+json' 'https://api.github.com/search/issues?q=repo%3ANationalSecurityAgency%2Fghidra+%22Unable+to+read+past+EOF%22&per_page=30' -o /tmp/r17ghidra/gh_issues_eof.json -w 'HTTP %{http_code}\n'
HTTP 200
$ python3 -B -c "import json; d=json.load(open('/tmp/r17ghidra/gh_issues_eof.json')); print('total',d.get('total_count')); [print(it['number'], it['state'], it['created_at'][:10], it['title'], it['html_url']) for it in d['items']]"
total 6
6864 closed 2024-08-29 Unable to read past EOF exception when importing file https://github.com/NationalSecurityAgency/ghidra/issues/6864
8265 closed 2025-06-17 Fix PE Import Table Parsing EOF Error in Truncated/Packed Files https://github.com/NationalSecurityAgency/ghidra/pull/8265
7271 closed 2024-12-09 Unable to read past EOF - Ghidra 11.2.1 https://github.com/NationalSecurityAgency/ghidra/issues/7271
4733 closed 2022-11-10 Error importing file ("Cannot read past EOF") https://github.com/NationalSecurityAgency/ghidra/issues/4733
5899 closed 2023-10-21 error importing file ("Cannot read past EOF") https://github.com/NationalSecurityAgency/ghidra/issues/5899
3911 closed 2022-01-24 error importing file ("Cannot read past EOF") https://github.com/NationalSecurityAgency/ghidra/issues/3911
```

`https://grep.app/api/search?q=Unable%20to%20read%20past%20EOF%20GoVarlenString` → HTTP 429 (Vercel checkpoint), recorded as unavailable.

## Remaining unknowns

1. Whether the bogus `GoName` at `0x10d4120` is exactly one of the 188 “unindexed” phantom types produced by the map-gap scan. The stack, the `188 unindexed` count, the 112-vs-88 snapshot mismatch, and the PR’s chain make this high-probability, but the log does not print the phantom type’s address. **[INFERENCE]**
2. Whether the per-type `try/catch` alone would restore aether’s function naming without the `SwissMapType` mapping fix. PR #9348’s table calls the guards “defense in depth” and says the `GoMapType` change alone restores recovery; both were tested together upstream, not separately. **[INFERENCE]**
3. Whether the PR’s backport branch (base `Ghidra_12.1.2_build`) applies cleanly to the installed 12.1.4, whose `GoMapType.java` lacks the `presentWhen` gating present in the PR base/master. Not tested; no Ghidra execution allowed here.
4. Whether `GolangSymbolAnalyzer` is retried by a later analysis pass after returning false. The retained log shows one attempt and no second “Go analysis failure”/“Go version” line; the consequence (naming skipped) is supported by control flow, not by a name count in REA output.
