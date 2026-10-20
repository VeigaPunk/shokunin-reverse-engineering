HOLDS

# S1250NethttpSilent: why s1250-swiss-nethttp is silent under H1 (round 18, wave 2, falsify)

This report comes from the author-side advisory seat `KaidokuR18.S1250NethttpSilent` (revenger). It was written at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. At read time, HEAD and `refs/heads/main` both pointed to REV.

- **What was read.** Carrier bytes, read with `xxd` and `python3 -I -B`, plus `git show REV:<path>` and Ghidra 12.1.4 `Base-src.zip` source (sha256 `f00d29c2…`).
- **What was not run.** I did not run REA or Ghidra, and I did not execute any carrier.
- **Freeze check.** `predictions/` and `tools/swiss-misread.py` have not changed between the freeze commit `eb6c2668…` and REV: `git diff --quiet` exits 0.
- **Installs.** No tools were installed or updated.

Labels: **O** means I observed it in bytes, a log, or source. **I** means I inferred it.

## Verdict on the claims under attack

| Claim at REV | Verdict |
|---|---|
| `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:78`: "none (name at types+40 has no pkgPath)" | HOLDS at the byte level |
| `corpus/lessons/round-18.md:21`: "silent only because the name at `types+40` has no pkgPath; the misread itself is present (H1 …)" | HOLDS under H1. For s1250's own run, "present" is an inference (see D3) |
| `…swiss-map-replay.md:96` and `SKILL.md:561`: "silent unless the name at `types+SlotSize` has a pkgPath" | Correct for s1250, but too narrow as a general rule (see D1) |

## Reconstructed contract: the H1 read chain, byte by byte (s1250 compared with s1246)

1. **O.** Both carriers have exactly two named Swiss map descriptors, meaning kind 21 with TFlagUncommon set. I found them with my own scan of `[runtime.types, runtime.etypes)`, without using the lane emulator.
   - s1250: `*textproto.MIMEHeader` at VA `0x58bb60` (file `0x18bb60`) and `*url.Values` at `0x58e480` (file `0x18e480`).
   - s1246: the same two types, at `0x58b0a0` and `0x58dc60`.
   - Neither carrier contains a `*http.Header` type name (`grep -c` gives 0). Aether and kimi-webbridge each have a third map, `*http.Header`.
2. **O (source).** Ghidra binds Go map types to the old 88-byte layout:
   - `GoMapType.java:32-34` maps to one of `{runtime.maptype, internal/abi.MapType, internal/abi.OldMapType}`. None of these is a Swiss type.
   - The installed `go1.25.0.json` (sha256 `54d10162…`) defines `runtime.maptype` as an alias of `internal/abi.OldMapType`, which is 88 bytes. `go1.24.0.json` does the same.
   - `GoType.java:143-147` reads `GoUncommonType` at `context.getStructureEnd()`, which is descriptor+88.
3. **O.** The 16 bytes at descriptor+88 are `28 00 00 00 | 00 00 | 00 00 | 10 00 00 00`, at VA `0x58bbb8` (file `0x18bbb8`) and at `0x58e4d8`.
   - Read as an UncommonType, this gives PkgPath=40, Mcount=0, Xcount=0, Moff=16. In the real Swiss layout these bytes are SlotSize=40 and the low half of ElemOff=16.
   - s1246 has the same bytes at `0x58b0f8` and `0x58dcb8`. **The input to the misread is identical in both carriers.**
   - The true UncommonType sits at +112: PkgPath `0x5210`=21008 (`net/textproto`, file `0x157210`) with Mcount 5, and PkgPath 7373 (`net/url`) with Mcount 6.
4. **O (source).** `GoUncommonType.java:57-58` passes the offset to `GoRttiMapper.resolveNameOff` (`:1053-1063`). That resolves to the GoName at `types + 40`:
   - In s1250, `types` = `runtime.types` = `0x552000` (`.rodata` at file `0x152000`), so the name is at `0x552028`.
   - In s1246, `types` = `0x553000`, so the name is at `0x553028`.
5. **O. This is where the two carriers differ.** The flags byte at that address decides the outcome (`GoName.java:43-47,93-101`):

| Carrier | Bytes at types+38 | Byte at types+40 | Flags decoded | Rest of the GoName read | Outcome |
|---|---|---|---|---|---|
| **s1250** | `00 01 62` (record "b") | `0x62` 'b' | HAS_TAG (0x02) set, **HAS_PKGPATH (0x04) clear** | Name varint `00` gives `""`. Tag varint `01` gives `"m"` (`0x6d` at `0x55202b`). pkgPath=0, so `resolveNameOff(off=0)` returns null (`GoRttiMapper.java:1054`). | No further read, **silent** |
| s1246 | `00 01 6d` (record "m") | `0x6d` 'm' | HAS_PKGPATH set | Name `""`. nameOff = u32 at `0x55302a` = `01 69 00 01` = `0x01006901`. `0x553000+0x01006901` = **22386945**, which is above the maximum mapped VA `0x7461af`. | `Invalid index: 22386945`: log l.451, stack l.457-465 (`GoName.readStructure:94` ← `getGoName:1074` ← `resolveNameOff:1063` ← `GoName.getPkgPath:124`) |

6. **O. Why the byte differs.** Here are the one-letter name records from `types+0` onward:
   - s1250: `'' _ v F r **w** C s f n p h c b m …`
   - s1246: `'' _ v F r C s f n p h c b m …`

   s1250 contains one extra 3-byte record, "w" (`00 01 77`), at types+14. Every later record shifts by +3. As a result, types+38 begins record "b" in s1250 and record "m" in s1246, and types+40 is that record's letter byte. `'b'`=`0x62` has bit 2 clear; `'m'`=`0x6d` has it set. This is a layout accident, as `…swiss-map-replay.md:97` says, not an effect of the Go version. **I:** which go1.25.0 struct field supplies the name "w" was not examined.
7. **O. My decoder reproduces every logged failing read from raw bytes.** I used the same decoder on the two held-out carriers and on the calibration carrier:
   - **aether:** types+40 = `0x954048` holds `6e 00 01 61 00 01 78 00`. That is flags 0x6e (TAG and PKGPATH), tag "a", nameOff `0x780100`, giving `0x10d4120`. At that address the flags are `0xf6` and the name length LEB128 is `a6 9a b0 35` = 111938854, with data starting at 17645861. This matches `Unable to read past EOF: 17645861, 111938854`.
   - **kimi-webbridge:** types+40 = `0x882028` holds `67 00 01 73 00 01 66 00`. That is flags 0x67, tag "s", nameOff `0x660100`, giving 15606016, which is above `0xdc7b4f`. This matches `Invalid index: 15606016`.

   In all three failing carriers the landing letter has bit 2 set (`m` 0x6d, `n` 0x6e, `g` 0x67). s1250's `b` (0x62) does not.
8. **O. The log shows that type markup completed.**
   - `GolangSymbolAnalyzer.java:146` (`markupGoTypes`) runs before `:155` (`markupGoFunctions`). s1246 aborted inside `:146` (log l.428-429).
   - s1250's log reaches the summary lines of the later `:155` phase (`runs/s1250-swiss-nethttp/logs/rea-ghidra-I0vJ0A/ghidra.log:10601-10606`). It has no `Go analysis failure`, `Invalid index`, or `read past EOF` lines, and ends with "Analysis succeeded" (l.10645).
   - `compare.json:2` has `all_match: true`, and `:43-53` show empty `eof_reads` and `invalid_index_reads`. The Evidence ID `ev_2b8b07d5…` matches `analyze.json`.
   - Rerunning REV `swiss-misread.py` (sha256 `14924bd6…`, the same as the frozen `emulator_sha256`) produces JSON identical to the frozen `predictions/swiss-misread/s1250-swiss-nethttp.json`. That file has H1 uncommon `{pkg_path 40, mcount 0}` at `:650-657` and `:678-685`, and predicted kind `none` at `:696-701`.

## Is the misread present but silent?

**Under H1, yes.** Ghidra reads the same bytes it reads in s1246, so it would get the package path wrong and drop the methods:
- **Package path:** both types get the GoName `{name "", tag "m"}`, which sits in the middle of a record at `0x552028`. The correct names are `net/textproto` and `net/url`.
- **Methods:** Mcount reads 0 instead of 5 and 6.

The scale of the loss is small. Raw method tables at `file 0x18bbe0` and `0x18e500` show that only one of the 11 method entries has live code: `url.Values.Encode` (Ifn=Tfn=text+`0xfb420`). The other 10 entries are `ffffffff`.

It is silent by construction. A conflict while applying markup becomes a program **bookmark**, not a log line (`MarkupSession.java:160-162,440-448`). Data creation uses `CLEAR_ALL_CONFLICT_DATA` (`:156-157`).

- **I:** Nothing points to `0x552028` itself (0 absolute-pointer hits). The real records "b" (`0x552026`, 1 pointer) and "m" (`0x552029`, 7 pointers) overlap the misread 4-byte GoName at `0x552028-0x55202b`. Depending on markup order, one may silently overwrite the other in the program database. That database was not retained and not inspected.

**Is there a witness in s1250's own run? No.** s1250 is a non-diagnostic label: `predictions/decision-rule.json:161-171` gives h0 = h1 = none. Its `analyze.json` holds only counts, and `carrier-run.stdout` is a binding receipt. So for this run, "present" is an inference drawn from four things: the source binding (O), the identical +88 bytes (O), the same code path producing the exact predicted index on s1246 and kimi (O), and the absence of any Swiss binding in 12.1.4 (O).

Two log signals look relevant but do not prove the misread:
- **Consistent, but not a witness of the +88 read.** "Found 1754" − "Discovered 34" = 1720 (log l.181-182), which equals the emulator's H1 index. The emulator's H0 model gives 1648, but it differs from H1 only because it does not follow the pointer at +64. In Ghidra that pointer is the OldMapType `bucket` field (`GoMapType.java:45-47`). The same identity (log Found − Discovered = emulator H1) holds for all four nethttp labels: 1720, 1673, 1674 and 1629.
- **Not attributable.** "Fixed … Go function signatures from method info" (counted per function, `GolangSymbolAnalyzer.java:283-285,330`) is 486 for swiss and 488 for noswiss (`s1250-noswiss-nethttp` log l.10468). H1 can remove at most one function here (Encode), so a difference of 2 is confounded by the different runtimes.

## Divergences (none changes the s1250 verdict)

- **D1 (calibration, minor).** `…swiss-map-replay.md:96`, `SKILL.md:561` and `corpus/lessons/round-18.md:21` shorten the rule to "silent unless the name at `types+SlotSize` has a pkgPath". The precise rule is the one stated at `…swiss-map-replay.md:27-33`:
  - A pkgPath bit is necessary for the chain to continue, but it is not sufficient to cause a failure.
  - The GoName at types+S reads its name length, and its tag length if HAS_TAG is set, before any pkgPath (`GoName.java:95-97`). An over-long length there would hit EOF (`MemoryByteProvider.java:312`) with no pkgPath involved.
  - s1250 is unaffected: its two lengths are 0 and 1.
  - Suggested wording: "silent unless the GoName chain from `types+SlotSize` reaches an out-of-range offset or an over-long length."
- **D2 (wave-1 evidence only).** `.ufo/waves/round-18/w1/ConnC3Prediction.md:49` says it "reads a zero-length tag". The bytes show a zero-length *name* and a one-byte tag `"m"`. `RevNotesmdMaps.md:135` has this right. The error did not reach the knowledge entry.
- **D3 (calibration).** `lessons/round-18.md:21` states "the misread itself is present" without the caveat that `…swiss-map-replay.md:96` keeps ("Silent case is INFERENCE"). For s1250 it is an inference from H1, not an observation.

## Commands run (exit codes as observed; `C=/home/vgpnk/.local/share/kaidoku-r18/carriers`, `L=kaidoku-shokunin`, `R=b2aad08…`)

```
git -C $L rev-parse HEAD refs/heads/main                       # exit 0 → both b2aad08ceeee…
git -C $L show $R:.ufo/waves/round-18/carriers/SHA256SUMS ; sha256sum $C/s1250-swiss-nethttp $C/s1246-swiss-nethttp   # exit 0; bd12f678…, 5c9faf23… match
git -C $L diff --quiet eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 $R -- .ufo/waves/round-18/predictions   # exit 0
nm $C/s1250-swiss-nethttp | grep -E ' runtime\.(types|etypes)$' ; readelf -SW $C/s1250-swiss-nethttp   # exit 0; types 0x552000, .rodata @0x152000
xxd -s 0x152026 -l 8 -g1 $C/s1250-swiss-nethttp   # exit 0 → 00 01 62 00 01 6d 00 01
xxd -s 0x153026 -l 8 -g1 $C/s1246-swiss-nethttp   # exit 0 → 00 01 6d 00 01 69 00 01
xxd -s 0x18bbb8 -l 32 -g1 $C/s1250-swiss-nethttp  # exit 0 → 28 00…|10 00…|01 00…|10 52 00 00 05 00 05 00
xxd -s 0x18e4d8 -l 32 -g1 $C/s1250-swiss-nethttp  # exit 0 → 28 00…|10 00…|01 00…|cd 1c 00 00 06 00 06 00
xxd -e -g4 -s 0x18e500 -l 96 $C/s1250-swiss-nethttp   # exit 0; only entry 2 has ifn=tfn=000fb420
xxd -s 0x554046 -l 10 -g1 /usr/bin/aether ; xxd -s 0xcd4120 -l 8 -g1 /usr/bin/aether   # exit 0 → 00 01 6e 00 01 61 00 01 78 00 ; f6 a6 9a b0 35 …
xxd -s 0x482026 -l 10 -g1 /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge   # exit 0 → 00 01 67 00 01 73 00 01 66 00
python3 -I -B -c '
import struct
for f,types,foff in (("s1250-swiss-nethttp",0x552000,0x152000),("s1246-swiss-nethttp",0x553000,0x153000)):
    d=open("/home/vgpnk/.local/share/kaidoku-r18/carriers/"+f,"rb").read(); o=foff+40; fl=d[o]; p=o+1; n=d[p]; p+=1+n; tag=None
    if fl&2: t=d[p]; tag=d[p+1:p+1+t]; p+=1+t
    pk=struct.unpack_from("<I",d,p)[0] if fl&4 else 0
    print(f,"flags=%#x HAS_TAG=%d HAS_PKGPATH=%d tag=%r pkgPath=%#x -> %s"%(fl,fl>>1&1,fl>>2&1,tag,pk,(types+pk) if pk else "null"))'
# exit 0 → s1250 flags=0x62 HAS_TAG=1 HAS_PKGPATH=0 tag=b'm' -> null ; s1246 flags=0x6d HAS_PKGPATH=1 pkgPath=0x1006901 -> 22386945
python3 -I -B <REV swiss-misread.py> --carrier $C/s1250-swiss-nethttp --golang-root ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang   # exit 0; JSON == frozen (True)
git -C $L show $R:.ufo/waves/round-18/runs/s1250-swiss-nethttp/logs/rea-ghidra-I0vJ0A/ghidra.log | grep -cE 'Go analysis failure|Invalid index|read past EOF'   # prints 0; grep exit 1 = no match (expected: silent)
git -C $L show $R:.ufo/waves/round-18/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log | grep -nE 'Go analysis failure|Invalid index'   # exit 0 → l.408, l.451 "Invalid index: 22386945"
git -C $L show $R:.ufo/waves/round-18/runs/<label>/logs/<dir>/ghidra.log | grep -nE 'unindexed Go types|Found [0-9]+ Go types|Fixed [0-9]+ Go function'   # exit 0 for s12{46,50}-{swiss,noswiss}-nethttp (dirs: I0vJ0A, Tikfv1, zHRS1l, PBi1r9)
```

Two scratch decoders were used outside the lane: `/tmp/s1250silent.aRyfdK/decode.py`, which does the full named-map scan and the GoName chain, and `methods.py`. Both exited 0 on s1250, s1246, aether and kimi. Their results are the rows above, and the `xxd` lines reproduce every byte they used.

## Confidence

- **High** for the byte-level explanation. My decoder, the frozen emulator and the Ghidra source agree, and the same decoder reproduces all three logged failing reads exactly.
- **Medium-high** that the silent misread actually ran inside s1250's Ghidra session. This is an inference: there is no witness in the program state, and the one supporting log count is only consistent with it.
