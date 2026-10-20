# RevContractC3 — C3 `swiss-misread.py` vs Ghidra 12.1.4 source and Go ABI

Scope: `.ufo/waves/round-18/contract.md:109-120` (C3 tool spec) and
`.ufo/waves/round-18/claims.json:24-27` (C3 claim). Read-only review; no REA analyze/search/decompile, no
Ghidra, no carrier execution. All commands are quoted with exit codes. `[O]` observation, `[I]` inference.

**Verdict.** The layout predicate is correct for the contract's eight synthetic carriers (and for the four
`nethttp` additions now on disk), official 1.24.6/1.25.0, linux/amd64, but wrong as stated in general, and
the mechanism the claim names ("method-carrying map types misread their uncommon/method data") cannot occur
in the emulated layout: the misread `Mcount` is `bits 32..47 of SlotSize`, i.e. 0. `predicted_failure` is
not well-defined, and the aether acceptance pair is a fit to a retained log, not a derivable prediction —
the emulator as specified is unfalsifiable on its only calibration case.

## 1. True-layout rule (calibration)

`[O]` Go 1.24.6 and 1.25.0 both default `SwissMap: true`
(`~/.local/opt/go-1.24.6/src/internal/buildcfg/exp.go:81`, `go-1.25.0/.../exp.go:85`), and both keep the
`noswissmap` off-switch (`exp_swissmap_on.go` / `exp_swissmap_off.go`, `flags.go:119-120` resp. `:115-116`).
The compiler chooses the descriptor by that experiment
(`go-1.25.0/src/cmd/compile/internal/reflectdata/reflect.go:775-780`, `:879-884`), and the two layouts are
`internal/abi.OldMapType` (88 B) and `internal/abi.SwissMapType` (112 B)
(`/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/map_swiss.go:32-42`,
`/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/map_noswiss.go:25-36`; `runtime.maptype` =
`abi.SwissMapType` at `runtime/map_swiss.go:22`, = `abi.OldMapType` at `runtime/map_noswiss.go:68` for 1.25
and `:67` for 1.24.6).

`[O]` All carriers agree with the rule: `go version -m` (read-only) reports
`go1.24.6` / `go1.24.6 X:noswissmap` and `go1.25.0` / `go1.25.0 X:noswissmap`, with
`build GOEXPERIMENT=noswissmap` on the noswiss arms and no `GOEXPERIMENT` setting on the swiss arms
(`.ufo/waves/round-18/carriers/build.sh:17-27`; the four `nethttp` arms were added after this contract was
written — see §8). The ` X:` suffix is the linker's record of the effective non-default experiment set
(`go-1.25.0/src/cmd/link/internal/ld/main.go:188-192`), and the build-info setting is
`cfg.RawGOEXPERIMENT`, which includes the toolchain's embedded default
(`cmd/go/internal/cfg/cfg.go:289-290`, `cmd/go/internal/load/pkg.go:2474`).

`[O]` As a general predicate the rule has at least three holes:

1. **`GOEXPERIMENT=none`.** The parser zeroes *all* flags, including `SwissMap`
   (`go-1.25.0/src/internal/buildcfg/exp.go:123-129`; 1.24.6 `:119-125`), so a `none` build is old-layout
   while "lacks `noswissmap`" is true. The rule needs the effective set, not a substring test.
2. It ignores the `X:` record. Both records are initialized from the same
   `envOr("GOEXPERIMENT", defaultGOEXPERIMENT)` (`internal/buildcfg/exp.go:31-37`; build info
   `load/pkg.go:2474`), so they agree here — but `GOEXPERIMENT=none` makes the build setting literally lack
   `noswissmap` while the `X:` list records it, because `Experiment.String()` lists every flag that differs
   from baseline. The faithful predicate is: token-split the build setting, treat `none` as all-off, and
   cross-check the `X:` tokens.
3. The rule says "Go ≥ 1.24" without saying *which* version. The carriers' `go.mod` is `go 1.24`
   (`.ufo/waves/round-18/carriers/src/{methods,nomethods}/go.mod:1`) while two arms are built by 1.25.0;
   the layout follows the *build* toolchain, not the language version. `--go-version` precedence is
   undefined.

`[O]` Snapshot selection is also looser than Ghidra: the r16 law never merges the patch diff
(`.ufo/waves/round-16/selection.py` docstring; `--request 1.24.6` returns `status: exact_diff`,
`patch_applied: false`, exit 0), while `GoApiSnapshot.getApiSnapshotJsonFile` merges it
(`Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:122-146`). For this pair it is
harmless: `patchverdiffs/go1.24.6.json.diff` contains zero occurrences of `OldMapType`, `SwissMapType` or
`UncommonType` (only two `internal/abi.Type` occurrences, both inside function signatures). The spec should
still say "base file only, no merge" or require the merge.

## 2. What Ghidra actually maps (calibration)

`[O]` `GoMapType` binds only `runtime.maptype`, `internal/abi.MapType`, `internal/abi.OldMapType`
(`Base-src.zip:ghidra/app/util/bin/format/golang/rtti/types/GoMapType.java:32-34`); there is no
`SwissMapType` binding. In both `go1.24.0.json` and `go1.25.0.json`, `runtime.maptype` is an *alias* to
`internal/abi.OldMapType` and `internal/abi.MapType` is absent; `internal/abi.SwissMapType` exists but is
never selected. Because `registerStructure` resolves the name list with `Structure.class` and an alias is
registered as a `TypedefDataType`
(`.../structmapping/DataTypeMapper.java:177-179`, `:299-301`, `:314-324`;
`.../rtti/GoTypeManager.java:549-556`), the registered structure is the concrete
`internal/abi.OldMapType`, length 0x58.

`[O]` `GoType.getUncommonType()` reads `GoUncommonType` at `context.getStructureEnd()`
(`.../types/GoType.java:144-148`), i.e. at descriptor + 0x58, not + 0x70. Applying Go's layout rules:
`abi.Type` = 0x30, `OldMapType` = 0x30+0x20+0x08 = 0x58, `SwissMapType` = 0x30+0x20+0x18+0x04 → 0x70.
So for a Swiss descriptor Ghidra's `GoUncommonType` fields read from the real
`SlotSize` (0x58), `ElemOff` (0x60), `Flags` (0x68) as:

| Ghidra field | true Swiss source | value |
|---|---|---|
| `PkgPath` (u32 @ +0x58) | low 32 bits of `SlotSize` | small (e.g. 24) |
| `Mcount` (u16 @ +0x5C) | bits 32..47 of `SlotSize` | **0** |
| `Xcount` (u16 @ +0x5E) | bits 48..63 of `SlotSize` | 0 |
| `Moff` (u32 @ +0x60) | low 32 bits of `ElemOff` | e.g. 8/16 |

(`GoUncommonType.java:39-50`, `:57-58`, `:74`; layout `abi/type.go:231-237`; `Mcount` is `uint16`, and
`FieldMappingInfo` reads the *structure component's* length, not the Java field type —
`.../structmapping/FieldMappingInfo.java:236-246`.)

`[I]` Therefore the C3 claim's mechanism is wrong: a Swiss map type's misread uncommon has `Mcount = 0`, so
`getMethodsSlice`/`getMethods` walk no method records and "misread their ... method data" cannot happen.
The observable misread is confined to `PkgPath` (a small `SlotSize` NameOff) and `Moff`/size fields. This
also makes `misread_map_types` ("method-carrying") the wrong cardinality; the affected set is map types
whose `TFlagUncommon` is set, which by `reflectdata/uncommonSize` is every *named* map type, with or
without methods (`go-1.25.0/src/cmd/compile/internal/reflectdata/reflect.go:60-65`, `:462-464`).

## 3. `predicted_failure` is not well-defined (operability)

`[O]` Problems, in the order an implementer hits them:

- **Circular truth condition.** "true iff the emulated reads raise the same EOF Ghidra's reader would"
  (`contract.md:118`) uses Ghidra's actual reader as the oracle, but the declared model only lays out
  structures; no reader, traversal order, or bounds rule is specified.
- **No tie to the list.** Nothing says `predicted_failure == (predicted_eof_reads != [])`, or whether any
  EOF at any address counts, or only the specific pair. The two output fields can disagree.
- **Reader/address space undefined.** Four providers raise this message (`ByteProviderWrapper.java:129`,
  `FileByteProvider.java:275`, `MemoryByteProvider.java:312`, `RangeMappedByteProvider.java:227`), and the
  numbers are provider-relative `(index, length)`. The Go analyzer uses
  `createProgramReader()` → `MemoryByteProvider(program.getMemory(), imageBase address space)`
  (`DataTypeMapper.java:510-514`) with the address-space minimum as base, so `index` is the absolute
  program address (aether: `0x10D4A25` = 17645861, inside `.rodata` 0x954000-0x13B4C40). None of this is in
  the contract; a PIE or non-default image base would change it.
- **Off-by-five trap.** For `GoVarlenString`, `index` is the *payload* address after the flags byte and the
  uvarint length (`GoName.java:99-100`, `GoVarlenString.java:66-73`): for aether the name record starts at
  0x10D4120, the length varint encodes 111938854, and the failing read index is 0x10D4125. An implementer
  that emits the name-record start gets 17645856 and fails acceptance.
- **Type discovery is unspecified.** `map_types`, `uncommon_map_types`, `misread_map_types` require walking
  the binary's type table (moduledata/typelinks, `GoModuledata.java:99-100`, `:398-404`); the contract never
  names that step, yet the counts feed `predicted_failure`.
- **Version plumbing.** The build version of four carriers is `go1.24.6 X:noswissmap` (likewise 1.25.0).
  The r16 selection law rejects that string: exit 2 `invalid request version '1.24.6 X:noswissmap'` (run
  below), because `parse_request` accepts only strict `M.m.p` (`selection.py` docstring). Ghidra itself
  accepts it — `GoVer.parse` strips at the first non-`[.0-9]` character
  (`GoVer.java:62-81`). The spec is stricter than the behavior it emulates, and `--go-version` is optional
  with no stated precedence over the build info. `[I]` 4 of the contract's 8 synthetic carriers (6 of the
  12 now on disk) exit 2 if the version is passed through unchanged.

## 4. The aether calibration pair is a fit, not a derivation (depth)

`[O]` The retained log's failure is a name-resolution EOF, not a map markup:

- `ghidra.log:97` `Go analysis failure`; `:177` `Caused by: java.io.EOFException: Unable to read past EOF:
  17645861, 111938854`; stack `GoName.getPkgPath:124` → `GoRttiMapper.resolveNameOff:1063` →
  `getGoName:1074` → `GoName.readStructure` → `GoVarlenString.readFrom:71`, under
  `GoStructType.additionalMarkup:94` → `GoInterfaceType.additionalMarkup:77` →
  `GoSlice.markupArrayElements:356`.
- There is **no map-type frame** in the trace. A misread map uncommon would call
  `GoUncommonType.getPkgPath` (`GoUncommonType.java:57-58`), a different method from
  `GoName.getPkgPath` (`GoName.java:123-124`).
- `[O]` The pair is byte-verifiable: at vaddr 0x10D4120 (file offset 0xCD4120) the bytes are
  `f6 a6 9a b0 35 ...`; flags 0xf6 (HAS_TAG|HAS_PKGPATH plus undefined high bits), uvarint `a6 9a b0 35` =
  111938854, payload at 0x10D4125 = 17645861. So the *numbers* are exactly reproducible from the carrier
  bytes at a fixed address.
- `[I]` But the address 0x10D4120 = `moduledata.types + off`; nothing in the declared map-layout model
  yields that `off`. A Swiss map's misread `PkgPath` is `SlotSize` (tens of bytes), so the derivation would
  need `typesBase ≈ 0x10D4100`, which the spec neither requires nor computes. The r17 knowledge itself
  admits "The exact invoking record is unresolved."
  (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:159-160`).
- `[I]` The 40-byte-slot arm supplies the quantitative link: for `map[string][]string`
  (`http.Header`, `url.Values`, `textproto.MIMEHeader`) `SlotSize` = 40, so the aether address implies
  `typesBase = 0x10D4120 - 40 = 0x10D40F8`. That is checkable only if the emulator emits `typesBase` and
  the offending `NameOff`; the contract requires neither, and an implementer can hit the acceptance pair
  without ever computing it (see §3 and §8).

`[I]` Consequence: a map-layout emulator cannot derive the pair; it can only copy it, scan for it, or
hard-code the aether sha256. The acceptance is `contains` (`contract.md:119`), and nothing forbids
sha256-specific branches or a constant list; a constant-return emulator passes both acceptance lines
(aether pair present, notesmd false). That is the unfalsifiability: the calibration case does not exercise
the mechanism, and the only negative case is a boolean on a binary that, per the r17 seat trace, has no map
type reaching the path — not an independent check of the layout model.

`[O]` The pair also does not discriminate the layout: aether is go1.25.14 and notesmd-cli go1.25.8, both
with no `GOEXPERIMENT` setting (default Swiss), both falling back to the same `go1.25.0.json` base. The
difference between them is program content, not layout.

## 5. Minimal-pair design (calibration)

`[O]` The "nomethods" arm is not a named map type without methods: it uses the unnamed `map[string]int`
(`.ufo/waves/round-18/carriers/src/nomethods/main.go:1-6`, `:12-20`), while "methods" declares
`type Counts map[string]int` with two methods (`.../methods/main.go:1-17`). By `uncommonSize` the unnamed
map has no uncommon at all (`reflect.go:60-65`), so the pair confounds (a) uncommon presence / namedness
with (b) methods. `[I]` Given `Mcount = 0` under the misread, a named map *without* methods would behave
like the methods arm in Ghidra; the variable that matters is `TFlagUncommon` (pkgpath read), not methods.
A clean pair is named-map-with-methods vs named-map-without-methods, plus a noswiss arm of the same named
type as a same-shape control. The wave-1 recipe already added a third `nethttp` arm for exactly this
reason (`carriers/build.sh:5-7`: "the methods/nomethods pair is predicted non-diagnostic"), and the TSV
now carries those four rows; the contract text still lists only the two arms — see §8.

## 6. Smallest required fixes

1. Define the true layout from the *effective* experiment set: token-split the `GOEXPERIMENT` setting,
   handle `none`, and cross-check the `X:` suffix; record which source was used. Keep the go.mod language
   version out of it.
2. Define the EOF pair space explicitly: program address in the default address space as Ghidra imports
   the image, and the length requested; state that the index is the post-uvarint payload address.
3. Tie `predicted_failure` to a stated predicate (e.g. `predicted_eof_reads != []`) and require the
   emulator to emit its derivation inputs (`types_base`, the offending `NameOff`, the decoded length) so a
   reviewer can check the pair rather than accept a constant.
4. Specify type discovery, or drop `map_types`/`uncommon_map_types`/`misread_map_types` from the claim.
   Define `misread_map_types` as `TFlagUncommon` set and `ghidra_size != true_size`, not "methods".
5. Either make the aether pair calibration-only (observed vs derived, both reported) or remove it from
   acceptance. As written it certifies a fit.
6. Normalize the version string for the r16 law (`go` prefix and ` X:...` suffix) and state precedence for
   `--go-version`; state whether the patch diff is applied.
7. Define `ghidra_maptype` and `true_kind` vocabularies (`internal/abi.OldMapType` / `SwissMapType` is the
   natural pair) and make `basis` checkable (member:line existence).

## 7. Verification gaps / residual risk

- `[O]` I did not run REA or Ghidra. The exact `moduledata.types` base of aether is not established here;
  `typesBase + SlotSize = 0x10D4120` is a plausible but unverified hypothesis. The r17 knowledge's byte
  trace is confirmed for the pair and address, not for its causal attribution.
- `[O]` Carrier digests match the r17 receipts: `/usr/bin/aether` = `06c91f55df41…8006e` (receipt
  `runs/pro-aether/receipt.json`), notesmd-cli = `412dc532d278…802d`.
- `[O]` `patchverdiffs/` has no 1.25.* entry (last is `go1.24.6.json.diff`), so every 1.25.0-built carrier
  uses the 1.25.0 base; this matches the log's fallback (`ghidra.log:92-93`).
- `[O]` Tool installs/upgrades: none. No lane writes outside this report; `Base-src.zip` members were
  extracted read-only to `/tmp/r18c3` for reading, and no carrier was executed.

## 8. Live-artifact divergence (wave-1 state at review time)

`[O]` The label file was extended while this review ran. At the latest read,
`.ufo/waves/round-18/predictions/carriers.tsv` has 15 rows: 2 calibration, 8 `synthetic-minimal-pair`,
4 `synthetic-nethttp`, and 1 `real-go1.24.13` (`real-kimi-webbridge` →
`/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge`, 10031288 bytes, `go version -m` = `go1.24.13`). The
contract and the C3 claim still describe eight `{methods,nomethods}` carriers
(`contract.md:101-120`, `claims.json:26`), and `build.sh` builds 12.

| artifact | synthetic count |
|---|---|
| `contract.md:101-120`, `claims.json:26` | 8 (`methods`,`nomethods`) |
| `carriers/build.sh:5-7`, `:22` | 12 (`methods`,`nomethods`,`nethttp`) |
| `carriers/SHA256SUMS`, `/home/vgpnk/.local/share/kaidoku-r18/carriers/` | 12 |
| `predictions/carriers.tsv` | 12 synthetic + 2 calibration + 1 real |

`[O]` `run-carriers.sh:24,148` iterates the whole TSV. The `nethttp` arm (the one `build.sh:5-7` calls
diagnostic) is now included, so that hazard is resolved; the uncovered row is now `real-kimi-webbridge`.
Its `go1.24.13` has no exact base: Ghidra's patch fallback would pick `go1.24.0.json` plus
`patchverdiffs/go1.24.6.json.diff` (`GoApiSnapshot.java:148-166`), and the r16 preview reports
`fallback_diff` without merging. If the row stays, `--go-version 1.24.13` and the fallback must be in the
emulator's stated selection rule; if it is dropped, `run-carriers.sh` needs a filter or the TSV must be
split. Either way, reconcile the contract text, the claim count ("0 -> 8"), the TSV and `SHA256SUMS` before
predictions are frozen — the wave is live, so this is a gating hazard, not a final state.

`[O]` `W18/tools/swiss-misread.py` did not exist at any listing taken during this review
(`head-rev-lint.py`, `jj-red-before.py`, `revpin.py`, `routed-defects.py`); this review is of the contract
text and the source it names.

## Commands (exact, exit codes)

```
$ unzip -l /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip | grep -Ei 'golang|GoMapType|GoType'
# exit 0 (member list)
$ cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang && python3 -I -B -c '
import json
for fn in ("go1.24.0.json","go1.25.0.json"):
    t=json.load(open(fn))["all"]["Types"]
    print(fn, "maptype->", t["runtime.maptype"]["Target"], "MapType?", "internal/abi.MapType" in t, "Swiss?", "internal/abi.SwissMapType" in t)
'
# exit 0; maptype-> internal/abi.OldMapType, MapType? False, Swiss? True (both versions)
$ python3 -I -B -c '
f=open("/usr/bin/aether","rb"); f.seek(0xcd4120); b=f.read(8)
i=1; sh=0; v=0
while True:
    c=b[i]; v|=(c&0x7f)<<sh; i+=1
    if not c&0x80: break
    sh+=7
print("flags=%#x len=%d payload=%#x(%d)" % (b[0], v, 0x10d4120+i, 0x10d4120+i))
'
# exit 0; flags=0xf6 len=111938854 payload=0x10d4125(17645861)
$ python3 -I -B .ufo/waves/round-16/selection.py --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang --request '1.24.6 X:noswissmap' --goos linux --goarch amd64
# exit 2; error: invalid request version '1.24.6 X:noswissmap': expected stable M.m.p
$ python3 -I -B .ufo/waves/round-16/selection.py --root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang --request '1.24.6' --goos linux --goarch amd64
# exit 0; status exact_diff, selected_diff patchverdiffs/go1.24.6.json.diff, patch_applied false
$ sha256sum /usr/bin/aether /home/vgpnk/.local/bin/notesmd-cli
# exit 0; 06c91f55…8006e aether, 412dc532…802d notesmd-cli
$ for f in /home/vgpnk/.local/share/kaidoku-r18/carriers/s* /usr/bin/aether /home/vgpnk/.local/bin/notesmd-cli; do /home/vgpnk/.local/opt/go-1.25.0/bin/go version -m "$f" 2>&1 | grep -E '^/|GOEXPERIMENT'; done
# exit 0; versions and GOEXPERIMENT settings quoted in §1/§8
$ readelf -SW /usr/bin/aether | grep -E '\] \.'
# exit 0; .rodata 0000000000954000 size a60c40
$ grep -c 'OldMapType\|SwissMapType\|UncommonType' /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/go1.24.6.json.diff
# exit 1; 0 (no matches)
$ grep -rn -E 'Unable to read past EOF|Go analysis failure' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log
# exit 0; :97 Go analysis failure, :177 EOF pair
```
