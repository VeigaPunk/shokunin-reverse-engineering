# RevAetherEOF — r17 W2 falsification: which getter read past EOF on /usr/bin/aether

Scope: read-only reverse engineering of the retained aether run. Artifacts are cited at lane
revision `da64646adcb19c1ede7537b799b8c7d283fe43da` (`git show REV:path`). The run dir was
re-executed during wave 2 (working tree HEAD `95e34db`; committed `logs/rea-ghidra-JpGezV/` is
deleted there and replaced by `logs/rea-ghidra-J5bcRT/`); I cite the committed revision for
anchors and the re-run only for reproduction. Carrier `/usr/bin/aether` sha256
`06c91f55df4117e58b478242df366145148b956c41c11a46cd1800f76178006e`, 20,694,888 B, ET_EXEC,
`go1.25.14` (`go version -m`; `runs/pro-aether/inspect-go.json`). No carrier execution, no REA
analyze/search/decompile, no Ghidra, no installs.

## F1 — (depth, high confidence) the getter is `GoName.getPkgPath`; the two numbers are (address, length)

Observation, `runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log` (sha256
`f39c329338a7fc2262eceaaa681a8ad9328feef05b61ebbaba4417e2a9f0b4ed`, 22,462 B, 244 lines):

- `:97` `ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException`
- `:100` `at ...FieldMappingInfo.addRefToFieldWithGetter(FieldMappingInfo.java:296)` → the throwing call is a field `@MarkupReference`, not a `@Markup` method.
- `:177` `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854`
- `:182` `at ...GoVarlenString.readFrom(GoVarlenString.java:71)`
- `:196` `at ...GoName.getPkgPath(GoName.java:124)` ← `:195` `resolveNameOff(...:1063)` ← `:194` `getGoName(...:1074)`

Installed source (Base-src.zip members): `GoName.java:88-90` (`@MarkupReference("getPkgPath")` on the
`pkgPath` field), `:93-101` (flags byte, `name` GoVarlenString, optional tag, optional 4-byte
`pkgPath`), `:122-125` (`getPkgPath` → `resolveNameOff(context.getStructureStart(), pkgPath)`);
`GoRttiMapper.java:1053-1064` (`nameStart = module.getTypesOffset() + off`), `:1073-1074`;
`GoVarlenString.java:65-71` (LEB128 strlen then `readNextByteArray`); `MemoryByteProvider.java:289-315`,
throw text at `:311-312` `"Unable to read past EOF: %s, %d"` with `Long.toUnsignedString(index)` first;
`DataTypeMapper.java:510-514` builds the provider over `program.getImageBase().getAddressSpace()`, whose
min address is 0, so **provider index == program address** (`MemoryByteProvider.java:138-176`).

Numeric proof that this is (offset, length), not (length, offset):

```
$ python3 -B -c "d=open('/usr/bin/aether','rb').read(); print(hex(0x10d4125), d[0xcd4121:0xcd4125].hex(' '), d[0xcd4125:0xcd4129].hex(' '))"
0x10d4125 a6 9a b0 35 1e 34 f6 41
```
LEB128-unsigned of `a6 9a b0 35` = `0x6AC0D26` = 111,938,854 = the second number, and the bytes sit
immediately before index 0x10D4125. Address→file mapping is vaddr−0x400000 (all LOADs here;
`readelf -lW`: LOAD #3 `Offset 0x554000 VirtAddr 0x954000 FileSiz 0xdabea8 R`; `readelf -SW`:
`.rodata` `Address 0x954000 Off 0x554000 Size 0xa60c40`). So:

- index `17645861` = `0x10D4125` = program address, file offset `0xCD4125`, `.rodata+0x780125`;
  inside LOAD #3 and `.rodata [0x954000,0x13B4C40)`, **not** in `.typelink` (0x13B4C40),
  `.itablink` (0x13B86C0) or `.gopclntab` (0x13B9580).
- The reverse reading is excluded: `111938854` as an address exceeds the provider max
  `0x17FFDA0` and would have thrown `Invalid index`, not `past EOF`
  (`MemoryByteProvider.java:301-302` vs `:311-312`).

Where the bad address comes from (observation + arithmetic): `runtime.moduledata` at vaddr
`0x172E400` (file `0x132E400`, `.noptrdata`) has `types=0x954020`, `etypes=0x13B4999`,
`rodata=0x954020`, `typelinks=0x13B4C40 len 3739` (=`.typelink` 0x3A6C/4), `itablinks=0x13B86C0
len 470` (=`.itablink` 0xEB0/8), `text=0x408EE0`, `etext=0x94FB10`:

```
$ python3 -B -c "import struct; d=open('/usr/bin/aether','rb').read(); b=0x132e400; print(*(hex(struct.unpack_from('<Q',d,b+o)[0]) for o in (0x128,0x130,0x160,0x168,0x178,0x180)))"
0x954020 0x13b4999 0x13b4c40 0xe9b 0x13b86c0 0x1d6
```

(Earlier fields at the same base give `text=0x408EE0`, `etext=0x94FB10`, matching `.text`.)
Fields are read with Ghidra's `runtime.moduledata` layout from
`Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json`; `GoModuledata.java:99-103,189-197`.
Therefore the resolved name record starts at `0x10D4120 = types + 0x780100`. `0x780100 <
etypes−types = 0xA60979`: the `pkgPath` nameOff was *in range* but points into non-name bytes of the
types blob (inference: the invoking GoName's `pkgPath` field is 0x780100; the observed fact is only
the read address).

Bytes at the resolved record: `f6 a6 9a b0 35 1e 34 f6 41 46 2a 78 ...`. Ghidra reads
`flags=0xF6` — bits 4–7 set, impossible for a genuine Go name (the Flag enum defines only four bits,
`GoName.java:44-47`); name LEB128 = 111,938,854. Remaining bytes to provider max = 7,519,355,
so `readNextByteArray(111938854)` throws.

Reproduction (observation): the wave-2 re-run `logs/rea-ghidra-J5bcRT/ghidra.log` (sha256
`5e6d8563050dea00507d0b8a75817bc6945cd56b33176ddc71aa48cd51dc2939`, 22,463 B) has the identical
`Unable to read past EOF: 17645861, 111938854` at line 177 and the same getter frames; carrier pins
pre/post equal (`receipt.json` in the same dir).

Severity: major for RE usefulness of this carrier — the exception aborts the Go type/RTTI markup
pass (`GolangSymbolAnalyzer.added`, caught/logged at `:97`), so the Go type and symbol enrichment for
this binary is lost; later analyzers still ran (Go strings found: 7200, "Analysis succeeded"). For
round 17 it is an **unpredicted in-range failure**: a base snapshot exists, but type markup still
aborts.

Smallest fix (analyzer side, one method): make `GoName.getPkgPath` tolerant — `catch (IOException e)
{ return null; }` around `resolveNameOff` (`GoName.java:122-125`); `pkgPath` is only an optional
label/string decoration, and this prevents one bad nameOff from aborting all Go type markup.
Sturdier variant: bound the name length by the containing module's `etypes − nameStart`
(`GoName.java:93-101`, `GoVarlenString.java:65-71`) and reject resolved flags with bits 4–7 set.
Anchor for the missing validation: Go's own `resolveNameOff` range-checks the resolved name against
`[md.types, md.etypes)` (`/home/vgpnk/.local/opt/go-1.27.3/src/runtime/type.go:300-304`); Ghidra's
does not (`GoRttiMapper.java:1053-1064`).

## F2 — (bounded no-finding) the *invoking* GoName cannot be identified from this image + log

Checked, all negative:

1. Enumerated every structurally valid in-range name record with `HAS_PKGPATH` (1571 records,
   printable names). All sampled resolutions are genuine package names — pkgPath `0xCDAB`→
   `regexp/syntax` @0x960DCB, `0x384E`→`reflect`, `0x87`→`os`, `0x10A8`→`bytes` — and **none** has
   value 0x780100 (so none resolves to 0x10D4120).
2. Whole-file search for LE `00 01 78 00`: 6 hits, 5 in the types blob (vaddrs 0x95404C, 0xA96105,
   0xDEAA86, 0xF566C7, 0xFB4C6F) and 1 in `.gopclntab` (0x14826C3). Only one admits any structural
   GoName parse ending at it: start 0x954048 (types+0x28), which is the mid-record `'n'` character of
   a run of one-character field-name records (`c f r w p S d u n a x y g s m`). Parsed from there:
   `flags=0x6E`, zero-length name, one-byte tag `a`, then the value 0x00780100. The genuine `'n'`
   record starts at 0x954046 (`00 01 6e`), and the four bytes at 0x95404C are really
   `[flags=00][len=1]['x']` for the next record — so no genuine record ends at any hit. Pre-1.17
   2-byte-BE name-length parses also fail at all 6 (3,000-byte window).
3. Alternate bases tested: `types` absolute (V=0x780100, 6 hits), base 0 (V=0x10D4120, 0 hits),
   image-base-relative (V=0xB80100, 7 hits); none has a structural GoName parse. So no evidence
   supports a different `types` base than the moduledata field above.

Conclusion (INFERENCE, not observed): the GoName that invoked `getPkgPath` was itself produced by an
earlier mis-resolution (a nameOff/uncommonType read that landed on bytes which merely parse as a
name). The logged cause chain stops at the first EOF, so the parent link is unobservable; a
GoType-specific structure length or an uncommonType read at a wrong address earlier in the same
markup chain is a candidate, not a finding. Smallest fix: none for the round (attribution would
require a provider-side fix plus a re-run, or a Go-type dump naming the failing structure — outside
this read-only lane).

## F3 — (low, derived-evidence gap) the observation JSON drops the exception cause chain

`runs/pro-aether/observation.json:2-4` records only
`"Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException"`.
`grep EOFException observation.json` = 0 hits; `:177`'s two numbers exist only in the retained raw
log (`:72-75` pins the log path and sha256, so nothing is lost, but the derived artifact cannot
answer the question this ticket asks). Cause: `tools/log-extract.py:193-194` appends only the
timestamped record message; continuation lines are intentionally skipped (`:145-147`;
contract-consistent).

Smallest fix: additive `analyzer_cause_lines: [{line, text}]` for each `Golang*` ERROR record,
collecting subsequent non-timestamped lines until the next record; no existing field or
classification changes.

## F4 — (medium for calibration) `compare.json` scores the unpredicted abort as a clean match

`runs/pro-aether/compare.json:2` = `"all_match": true`; the compared fields (`:3-37`) are exactly
`untested_version, snapshot_label, missing_bootstrap, snapshot_route, fallback_to`.
`tools/compare.py:39,43,121-142` never reads `observation["analyzer_errors"]`, and
`predictions/pro-aether.prediction.json:15-21` has no analysis-outcome key. The aether run was added
as a *fallback-branch* carrier (`w1/CriticC2Confound.md:57`) predicting only the two snapshot log
lines; it additionally aborted Go analysis, and that outcome is invisible in the verdict. C2's
"prediction mismatches are reported, never hidden" holds only for the fields that were predicted.

Smallest fix: add one expected field `analyzer_error: false` (in-range, base-only carriers) to
`predict.py`'s output and one equality rule in `compare.py` (`observed = len(analyzer_errors) > 0`).
`pro-aether` then reports a mismatch (predicted false / observed true), which is the honest score.

## Limits

- No Ghidra/REA run and no carrier execution; evidence is static. No installs.
- Go 1.25.14 vs `go1.25.0` snapshot layout deltas are untested (no 1.25 patch diffs installed in the
  Ghidra data dir); the GoName width itself is validated by resolving genuine names (F2.1), so a
  pkgPath-width mismatch is excluded, but other struct deltas are not.
- `.typelink` entries were used only to confirm section sizes and the types base; their per-entry
  target semantics were not fully resolved and are not needed for F1.
- The content type of the `.rodata` region at types+0x780100 is not established (high-entropy bytes;
  consistent with embedded data, unproven).
