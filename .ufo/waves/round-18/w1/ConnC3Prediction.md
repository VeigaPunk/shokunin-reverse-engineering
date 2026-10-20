# ConnC3Prediction — does the C3 minimal pair separate the hypotheses?

Seat: `KaidokuR18.ConnC3Prediction` (leaf, advisory). Round 18, 2026-10-20.
Scope: `claims.json:24-28` (C3), `contract.md:100-125`, r17 knowledge `:145-166`.
Method: read-only LANE; static ELF/byte probes and `Base-src.zip` reads; scratch probes in `/tmp` (no installs, no REA/Ghidra run, no carrier executed, LANE unmodified). Observation vs inference is labelled `[OBS]` / `[INF]`.

## Verdict

The factor design is correct: 2 versions × 2 layouts × 2 type shapes, orthogonal, and the Swiss-map misread path **is** reached by Ghidra’s main analyzer (the named map descriptor is discovered through its typelinked pointer type, `GoPointerType.discoverGoTypes`, and marked up in `markupGoTypes`). The question is the landing.

- **The eight carriers named in `claims.json:26` / `contract.md:102-104` are a null experiment.** Every one predicts `predicted_failure: false`: the only uncommon map type is `main.Counts` (`map[string]int`, SlotSize 24); Ghidra’s misread `PkgPath` is 24; the `GoName` at `types+24` has flags `0x01`, length 115/116, and no HAS_TAG/HAS_PKGPATH, so the second name hop never happens. The predicted log is 8× “no `Go analysis failure`, no EOF”, which H1 (silent misread), H2 (no fallback involved) and H0 (no defect) all predict. **Unresolved by construction; not a refutation.**
- **The four `nethttp` carriers added at 12:36–12:37 (`carriers/build.sh:4-5`, `carriers/src/nethttp/main.go`) partially rescue the design.** `s1246-swiss-nethttp` carries two real 40-byte-slot named maps (`textproto.MIMEHeader`, `url.Values`); Ghidra’s `PkgPath` is 0x28, G1 at `types+0x28` has flags 0x6d (HAS_PKGPATH) and pkg `0x1006901`, so G2 lands at `0x1559901` > `maxOff 0x7461af` → **predicted failure, class `invalid_index`**. `s1250-swiss-nethttp` has the same two maps but its G1 has flags 0x62 (HAS_TAG only, no pkgpath) → **no failure**. The two `noswiss-nethttp` controls read the true uncommon and pass.
- **Net discriminating power:** a failure observed on `s1246-swiss-nethttp` matching `Invalid index: 22386945` would **refute H2** (that route has no fallback) and confirm the mechanism on the 1.24.6 Swiss carrier. It cannot confirm the aether **1.25.x** case, because the 1.25.0 nethttp arm is inert; it cannot separate H1 from a 1.24.6-specific effect. The claims’ “eight carriers” and “replayed-confirmed or replayed-refuted” are **not met by the current 12 built carriers**.
- **The A-nethttp positive control is exactly the case the contract’s log schema does not handle.** The predicted exception is `EOFException("Invalid index: X")`, not `EOFException("Unable to read past EOF: A, B")`. `log-extract.py`’s new `eof_reads` only parses the latter (`contract.md:123-125`); the tool’s `predicted_eof_reads: [[index, length]]` has no representation for the former. Freeze the control only after the schema distinguishes the two classes, or the compare will report a false mismatch.

Two mechanism corrections for the claim/lesson: the trigger is **TFlagUncommon (a named type)**, not method presence (`reflect.go:60-65`); and the misread fields are `PkgPath = low32(SlotSize)` and `Moff = low32(ElemOff)`, with `Mcount = high32(SlotSize) = 0` — the method array is **never read**, so “misread their uncommon/method data” (`claims.json:26`) is only half true.

## What the bytes say `[OBS]`

Calibration digests verified against W17 receipts: aether `06c91f55…8006e` (`runs/pro-aether/receipt.json:7-8`), notesmd-cli `412dc532…802d` (`runs/pro-notesmd-cli/receipt.json:7-8`). All 12 carrier digests equal `carriers/SHA256SUMS` (mtime 12:37).

**Contract 8** (`types` and `maxoff` from ELF; typelinks from `.typelink`; descriptors from `[runtime.types, runtime.etypes)`):

| label | types / maxoff | typelink maps (uncommon) | named map desc (map / typelinked `*T`) | true `PkgPath` | Ghidra `PkgPath@+0x58` | G1 at `types+N` | G1 flags / len / pkg |
|---|---|---|---|---|---|---|---|
| s1246-swiss-methods | 0x495000 / 0x584a9f | 11 (0) | 0x4aa4c0 / 0x4a32c0 | 0x240 | **0x18 (24)** | 0x495018 | 0x01 / 116 / 0 |
| s1246-swiss-nomethods | 0x494000 / 0x583a9f | 11 (0) | none | — | — | — | — |
| s1246-noswiss-methods | 0x494000 / 0x581abf | 11 (0) | 0x4a4fc0 / 0x4a22e0 | 0x243 | 0x243 (correct) | 0x494243 | 0x00 / 4 / 0 (`main`) |
| s1246-noswiss-nomethods | 0x494000 / 0x581abf | 11 (0) | none | — | — | — | — |
| s1250-swiss-methods | 0x49b000 / 0x5a443f | 11 (0) | 0x4b13e0 / 0x4a9cc0 | 0x22e | **0x18 (24)** | 0x49b018 | 0x01 / 115 / 0 |
| s1250-swiss-nomethods | 0x49b000 / 0x5a443f | 11 (0) | none | — | — | — | — |
| s1250-noswiss-methods | 0x49a000 / 0x5a143f | 11 (0) | 0x4ab9c0 / 0x4a8cc0 | 0x231 | 0x231 (correct) | 0x49a231 | 0x00 / 4 / 0 (`main`) |
| s1250-noswiss-nomethods | 0x49a000 / 0x5a143f | 11 (0) | none | — | — | — | — |

**Added `nethttp` 4** (not in `claims.json`/`contract.md`; present in `SHA256SUMS` and `build.sh`):

| label | types / maxoff | named maps (slot) | map / typelinked `*T` | Ghidra `PkgPath@+0x58` | G1 at `types+0x28` | predicted |
|---|---|---|---|---|---|---|
| s1246-swiss-nethttp | 0x553000 / 0x7461af | `*textproto.MIMEHeader`, `*url.Values` (40) | 0x58b0a0/0x580fa0, 0x58dc60/0x582de0 | 0x28 | flags 0x6d, len 0, pkg 0x1006901 → G2 `0x1559901` > max | **failure, invalid_index 22386945** |
| s1246-noswiss-nethttp | 0x553000 / 0x7411cf | same (40) | 0x5850c0/0x57d4c0, 0x588020/0x57f300 | true 0x517e / 0x1c0d | flags 0, len 13 / 7 (`net/textproto`, `net/url`) | no failure |
| s1250-swiss-nethttp | 0x552000 / 0x75bcdf | same (40) | 0x58bb60/0x580ec0, 0x58e480/0x582e20 | 0x28 | flags 0x62, len 0, **pkg 0** | no failure (no pkgpath bit) |
| s1250-noswiss-nethttp | 0x551000 / 0x755cdf | same (40) | 0x584500/0x57c360, 0x587760/0x57e2c0 | true 0x51f9 / 0x1c9f | flags 0, len 13 / 7 | no failure |

Other observations:

- **No map type in any carrier’s typelinks has TFlagUncommon.** All typelink map descriptors carry `tflag=0x02` (ExtraStar). Named maps are reachable only through their typelinked **pointer** types (kind 22, `tflag=0x9`, `Elem` = map descriptor), and `GoPointerType.discoverGoTypes` (`GoPointerType.java:61-70`) follows `Elem`, so the map is registered in `init` and marked up in `markupGoTypes` (`GoTypeManager.java:96-119,147-155`). The path is live; the landing is the variable.
- `http.Header` has no map descriptor in either nethttp carrier (one `http.Header` string, in the function-name table); the two real named maps are `textproto.MIMEHeader` and `url.Values`. This is a compiler/linker fact, not a source omission; the carrier still carries two 40-byte-slot named maps.
- The misread landing is the **name-table region** at the start of the types blob. `s1250-swiss` lands on flags 0x01/0x62 (benign); `s1246-swiss-nethttp` lands on flags 0x6d (HAS_PKGPATH) and a pkgpath beyond `maxOff`. The landing is a byte-layout lottery, deterministic per binary but not derivable from the source alone.
- `s1250-swiss-nethttp` G1 flags 0x62 = HAS_TAG, no HAS_PKGPATH; it reads a zero-length tag and stops. No second hop.

## Mechanism model used (source-grounded `[INF]`)

1. `GoMapType` maps `{"runtime.maptype","internal/abi.MapType","internal/abi.OldMapType"}` (`GoMapType.java:32-34`); both snapshots alias `runtime.maptype → internal/abi.OldMapType` (`go1.24.0.json:1`, `go1.25.0.json:1`, key path `all.Types`). `OldMapType` = 0x58; `SwissMapType` = 0x70; `UncommonType` = 0x10.
2. `GoType.getUncommonType()` reads at `context.getStructureEnd()` = map_start + 0x58 (`GoType.java:143-150`). On Swiss, +0x58 is `SlotSize`; `PkgPath = low32(SlotSize)`, `Mcount/Xcount = high32(SlotSize) = 0`, `Moff = low32(ElemOff)`.
3. `GoUncommonType.getPkgPath()` → `resolveNameOff(start, off)` → `typesOffset + off` (`GoUncommonType.java:55-59`, `GoRttiMapper.java:1053-1064`).
4. `GoName.readStructure` reads flags, LEB128 length, bytes, optional tag, optional pkgpath (`GoName.java:92-102`, `GoVarlenString.java:65-72`). `MemoryByteProvider.ensureBounds` throws `EOFException("Invalid index: X")` when the index is past `maxOffset`, and `EOFException("Unable to read past EOF: index, length")` when the length overflows (`MemoryByteProvider.java:289-314`).
5. Markup reaches this through recursive `@Markup` getters: `markupGoTypes` → `getUncommonType()` → `markup(ut)` → `ut.getPkgPath()` → `markup(G1)` → `G1.getPkgPath()` → G2 (`StructureMappingInfo.java:394-399`, `MarkupSession.java:332-352`). `GoType.getPackagePathString` swallows IOException (`GoType.java:110-117`), but the markup getter does not; `GolangSymbolAnalyzer`’s `catch (IOException)` logs `Go analysis failure` (`GolangSymbolAnalyzer.java:181-184`).

The model reproduces aether exactly: the three `map[string][]string` descriptors at `0xa1c7a0`, `0xa229a0`, `0xa350a0` (`SlotSize 40`, `PkgPath 0x28`) give G1 at `0x954048` (flags 0x6e, pkg `0x780100`), then G2 at `0x10d4120` with a 4-byte LEB128 `111938854` read at `17645861` — the logged pair (`r17 knowledge :149-152`, `CriticAetherUnknown.md:58-63`). notesmd-cli has 0 uncommon map types (`CriticAetherUnknown.md:117`), so `predicted_failure: false`.

## Frozen-ready outcome table

`observed` = the retained log’s `Go analysis failure` / `eof_reads` / `invalid_index` for that label; `match` = observed equals the predicted class (and, for `past_eof`, the exact pair). `†` = this seat’s static probe, to be replaced by `swiss-misread.py` before freezing.

### A. Contract 8

| label | go / exp | snapshot route | Ghidra / true maptype | uncommon maps | misread | PkgPath | G1 | predicted_failure | class | H1 | H2 | observed | match |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s1246-swiss-methods | 1.24.6 / — | base `go1.24.0.json` + diff `go1.24.6.json.diff`; INFO (`GoApiSnapshot.java:148-165`) | 0x58 / 0x70 | 1† | 1† | 0x18† | 0x01,116,0† | **false**† | none | false (silent) | false | | |
| s1246-swiss-nomethods | 1.24.6 / — | same | 0x58 / 0x70 | 0† | 0† | — | — | **false**† | none | false | false | | |
| s1246-noswiss-methods | 1.24.6 / noswissmap | same | 0x58 / 0x58 | 1† | 0† | 0x243 | 0x00,4,0† | **false**† | none | false | false | | |
| s1246-noswiss-nomethods | 1.24.6 / noswissmap | same | 0x58 / 0x58 | 0† | 0† | — | — | **false**† | none | false | false | | |
| s1250-swiss-methods | 1.25.0 / — | base `go1.25.0.json`; INFO (`GoApiSnapshot.java:122-131,162-163`) | 0x58 / 0x70 | 1† | 1† | 0x18† | 0x01,115,0† | **false**† | none | false (silent) | false | | |
| s1250-swiss-nomethods | 1.25.0 / — | same | 0x58 / 0x70 | 0† | 0† | — | — | **false**† | none | false | false | | |
| s1250-noswiss-methods | 1.25.0 / noswissmap | same | 0x58 / 0x58 | 1† | 0† | 0x231 | 0x00,4,0† | **false**† | none | false | false | | |
| s1250-noswiss-nomethods | 1.25.0 / noswissmap | same | 0x58 / 0x58 | 0† | 0† | — | — | **false**† | none | false | false | | |

### B. Added `nethttp` 4

| label | go / exp | snapshot route | Ghidra / true | named maps | misread | PkgPath | G1 | predicted_failure | class | H1 | H2 | observed | match |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s1246-swiss-nethttp | 1.24.6 / — | base 1.24.0 + diff .6; INFO | 0x58 / 0x70 | 2† | 2† | 0x28† | 0x6d,0,0x1006901† | **true**† | **invalid_index 22386945**† | true | **false → refuted if observed** | | |
| s1246-noswiss-nethttp | 1.24.6 / noswissmap | same | 0x58 / 0x58 | 2† | 0† | 0x517e/0x1c0d | 0x00,13/7,0† | **false**† | none | false | false | | |
| s1250-swiss-nethttp | 1.25.0 / — | base 1.25.0; INFO | 0x58 / 0x70 | 2† | 2† | 0x28† | 0x62,0,0† | **false**† | none (no pkgpath bit) | false | false | | |
| s1250-noswiss-nethttp | 1.25.0 / noswissmap | same | 0x58 / 0x58 | 2† | 0† | 0x51f9/0x1c9f | 0x00,13/7,0† | **false**† | none | false | false | | |

Notes: `map_types` (Ghidra discovery closure, `[INF]`) = 12 for `-methods` (11 typelink + `Counts`), 11 for `-nomethods`, 38 for nethttp (36 typelink + 2). The snapshot routes are `exact_diff` and `base_only` in `selection.py` terms; `patch_applied: false` in that preview only means the preview never merges (`selection.py:10-15,297`) — Ghidra merges base+diff at load (`GoApiSnapshot.java:128-144`).

## Outcome-pattern decision table

`✓` = the run-bound log shows the analyzer failure (and, for `past_eof`, the exact pair); `✗` = no failure. A/E are the Swiss 1.24.6/1.25.0 arms; C/G the noswiss arms; B/D/F/H the unnamed controls; `Aᵢ/Eᵢ` the nethttp 1.24.6/1.25.0 arms.

| pattern | inference |
|---|---|
| Aᵢ✓ with `Invalid index: 22386945`, Eᵢ✗, Cᵢ/Gᵢ✗ | **H1 confirmed on 1.24.6** (Swiss + named-uncommon + 40-byte slot is sufficient); **H2 refuted** (Aᵢ’s route is base+diff, no fallback). Does not confirm the aether 1.25.x case; still confounded with a 1.24.6-specific effect unless a 1.25.x arm also fails. |
| A✓ E✓ and B C D F G H ✗ | H1 confirmed on both contract methods arms; H2 refuted. **Impossible with the built methods carriers** (benign landings). |
| Aᵢ✓ and Eᵢ✓ | strongest available: H1 confirmed across both versions; H2 refuted twice. Requires a 1.25.x nethttp landing that is currently benign. |
| Aᵢ✓ and Cᵢ/Gᵢ✓ | layout is not the trigger (noswiss fails); **H1 refuted**, even though Aᵢ failed. |
| A✓ only (contract) | unresolved: 1.24.6 × layout interaction. |
| E✓ only | exact-base/layout correlated; H2 refuted, H1 version-confounded. |
| any of B D F H ✓ | H1 refuted for the “uncommon is required” condition. |
| any of C G ✓ | H1 refuted for the “layout is the trigger” condition. |
| all ✗ | unresolved: H1-silent, H2 and H0 all fit (the contract-8 prediction). |
| all ✓ | no discrimination (generic analyzer instability). |
| observed class/pair ≠ frozen prediction | the **model** is refuted (separate from H1). |

## Freeze gates (must hold before Git-freezing C3)

1. **Positive control.** With the nethttp addition, the gate is met only on `s1246-swiss-nethttp` (two `invalid_index` predictions). It is **not** met on `s1250-swiss-nethttp` or on any contract-8 carrier. Decide explicitly whether a 1.24.6-only control is sufficient for the claim, or iterate the 1.25.0 nethttp layout (add a named map type of a different SlotSize / change the import set) until the emulator predicts a 1.25.0 failure.
2. **EOF class taxonomy (now load-bearing).** The A-nethttp predicted exception is `Invalid index: 22386945`, **not** `Unable to read past EOF: A, B`; the contract’s `eof_reads` (`contract.md:123-125`) cannot represent it, and `predicted_eof_reads: [[index,length]]` has no length to report. Add `predicted_failure_kind` (`past_eof` | `invalid_index` | `max_int` | null) to `swiss-misread.py`, and `invalid_index_reads` to `log-extract.py`/`compare.py`; otherwise the A-nethttp control will show `Go analysis failure` with an empty `eof_reads` and a false mismatch.
3. **Carrier-set consistency.** `claims.json:26` and `contract.md:102-104` say eight carriers; `build.sh:4-5` and `SHA256SUMS` contain twelve. Either amend the claims/contract to name the nethttp arms (and their prediction fields) or keep the extra four outside the frozen claim. A frozen table that silently adds carriers is not revision-scoped.
4. **Route labels.** The pair’s version factor is “diff-patched base” vs “exact base”, not “fallback vs no fallback”. H2 is refuted by *any* failure on a non-fallback route (A-nethttp suffices), not by comparing 1.25.0 with 1.25.x: with no installed 1.25 diffs, both select the same `go1.25.0.json` and differ only in the WARN line.
5. **Definitions.** Replace “method-carrying map types misread their uncommon/method data” with “named map types (TFlagUncommon) have their uncommon read at +0x58; `PkgPath` = low32(`SlotSize`), `Moff` = low32(`ElemOff`)”; `Mcount` reads 0, the method array is never read. The `nomethods` arm is the *unnamed* control.

## Recommended single move (bounded)

Freeze the 12-carrier set with the nethttp arms named, but **only after** `swiss-misread.py` emits `predicted_failure_kind` and the compare/log-extract carry `invalid_index_reads`; then the single load-bearing observation is `s1246-swiss-nethttp` → `Go analysis failure` + `Invalid index: 22386945` (refutes H2, confirms the mechanism on 1.24.6). In parallel, try one layout shift for `s1250-swiss-nethttp` (add a second named map type with a different slot, e.g. `map[uint64]bool` (16) or `map[string]string` (32), or extend the import set) until the emulator predicts a 1.25.0 failure; if that succeeds, the pair confirms H1 on both versions and the aether 1.25.x case is replayed at the mechanism level. If it does not, state in the lesson that C3 confirms the mechanism on 1.24.6 only and that the 1.25.x landing is layout-lottery-dependent.

## Exact commands (exit codes)

| command | exit | key output |
|---|---|---|
| `sha256sum /usr/bin/aether ~/.local/bin/notesmd-cli` | 0 | `06c91f55…8006e`, `412dc532…802d` = W17 receipts |
| `python3 -I -B .ufo/waves/round-16/selection.py --root …/typeinfo/golang --request 1.24.6 --goos linux --goarch amd64` | 0 | `status=exact_diff`, base `aab28c8f…`, diff `e169e8dd…` |
| same, `--request 1.25.0` | 0 | `status=base_only`, base `54d10162…` |
| same, `--request 1.25.14` | 0 | `status=base_only` (WARN fallback at load; `GoApiSnapshot.java:148-165`) |
| `readelf -sW <carrier> \| grep -E 'runtime\.types\|runtime\.etypes\|firstmoduledata'` | 0 | types/etypes symbols present |
| `python3 -B /tmp/r18tl.py` | 0 | contract 8: 11 typelink maps, **0 map-uncommon** |
| `python3 -B /tmp/r18probe3.py` | 0 | Counts map/pointer per `-methods`; G1 flags 0x1, len 115/116, pkg 0 |
| `python3 -B /tmp/r18net2.py` | 0 | nethttp: Aᵢ flags 0x6d → `Invalid index 22386945`; Eᵢ flags 0x62 → pkg 0; controls read true `main`/`net/textproto`/`net/url` |
| `python3 -B /tmp/r18ae2.py` | 0 | aether 3 descriptors → `[(17645861, 111938854)]` (exact logged pair) |
| `grep -n 'Unable to read past EOF\|Go analysis failure' runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log` | 0 | lines 97, 177 |
| same against `runs/pro-notesmd-cli/logs/rea-ghidra-eK7Drd/ghidra.log` | 0 | no matches (only lines 68-69 fallback/snapshot) |
| `grep -c 'UncommonType\|"Types","internal/abi' patchverdiffs/go1.24.6.json.diff` | 1 | 0 — the 1.24.6 diff does not touch abi map/uncommon types |

## Limits / risks

- My probe is an independent seat model, not the C3 tool. Its aether replay is exact, which calibrates the read path, but the frozen predictions must come from `swiss-misread.py` with `--selftest`.
- The type blob’s name-table bytes are layout-sensitive: any source/import/link change shifts the landing. Never hardcode the hostile offset; re-emulate the final bytes. The nethttp Aᵢ/Eᵢ divergence is proof of this.
- “No failure” is not “correct markup”: the same misread silently corrupts `GroupSize`/`SlotSize` reads without a log line (r17 `CriticAetherUnknown.md:130-139`). The controls measure only the crash.
- If the typelinked `*T` pointer is removed by devirtualization, the map becomes callsite-only and the deferred `PropagateRttiBackgroundCommand` catches `IOException` into a bookmark (`GolangSymbolAnalyzer.java:1146-1170`), making the experiment silently null. Keep a `discovery_route` column in the frozen table.

Report: .ufo/waves/round-18/w1/ConnC3Prediction.md
