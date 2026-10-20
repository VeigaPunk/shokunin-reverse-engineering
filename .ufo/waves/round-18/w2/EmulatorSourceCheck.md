HOLDS

# EmulatorSourceCheck: H1 read chain for s1246-swiss-nethttp (round 18, w2 falsify)

Seat `KaidokuR18.EmulatorSourceCheck` (revenger, author-side advisory, not an outside reviewer).
Lane REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (HEAD = refs/heads/main = REV, C1). C3 freeze
`eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Ghidra source: `Base-src.zip` sha256 `f00d29c2…a8d804` (C2).
Carrier sha256 `5c9faf239ed2c68304666992a8d2c1dc40c36e90f8021c62fef4cc4453f201b6`. Both copies match,
and so does `carriers/SHA256SUMS:5` at REV (C3). The carrier was never executed. I ran no REA, Ghidra or jj,
and no git write. I installed and updated no tools. The only file I wrote is this report.

## Result

- **N = 22386945 (0x1559901), computed from the carrier bytes by my own parser (C8).** It equals
  types `0x553000` plus the pkgPath `0x01006901` decoded from the GoName that H1 makes Ghidra read at
  types+0x28. [observation]
- **Equal to the frozen prediction:** `predictions/swiss-misread/s1246-swiss-nethttp.json:660,668,714-720`
  and `predictions/s1246-swiss-nethttp.prediction.json:40-42`. The blobs are identical at eb6c266 and at REV
  (C13), and the freeze precedes the run (13:23:55-03:00 < `runs/run-log.txt:22` 13:28:55-03:00).
  [observation]
- **Equal to the observed log:** `runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log:451`
  `Caused by: java.io.EOFException: Invalid index: 22386945`, after `:408` `Go analysis failure`. The log's
  sha256 `05ea153e…` equals `runs/s1246-swiss-nethttp/receipt.json:1901`, and the log imports
  `target-5c9faf239ed2.bin` (`:46`). [observation]
- **The error is "Invalid index", not past-EOF.** The failing read is the 1-byte GoName flags read at
  index 22386945.
  - `MemoryByteProvider.java:301-302` throws `Invalid index` when `index > maxOffset`.
  - Past-EOF (`:307-312`) needs `index ≤ maxOffset` and an overrun.
  - Here maxOffset is the highest ram address. From the ELF it is 0x7461af = 7627183. That value is an
    inference about Ghidra's block list, but it isn't needed: the observed message already proves
    index > maxOffset.
  - The chain's earlier reads are the 88-byte descriptor at 0x58b0a0, the 16-byte uncommon block at
    0x58b0f8 and 6 bytes of name1 at 0x553028. All are far below maxOffset.
  - The log contains 0 `Unable to read past EOF` lines (C12).
- **The observed N picks out H1's 88-byte map descriptor and no other.** I swept the uncommon offset over
  the 8-aligned candidates 48..112 on both named maps (C10):
  - Only +88 (the `OldMapType` length) yields 22386945.
  - The true Swiss +112 (H0) is silent. So are +80, +96 and +104.
  - +48..+72 fail with other N values.

## Evidence chain (installed Ghidra 12.1.4 source applied to the carrier bytes)

| # | Step | Base-src.zip member:line | Carrier value (C8) |
|---|---|---|---|
| 1 | GoMapType binds the first resolvable name of `runtime.maptype`, `internal/abi.MapType`, `internal/abi.OldMapType` | GoMapType.java:32-34; DataTypeMapper.java:172-176, 310-319; GoRttiMapper.java:380-396 (`clazz.isInstance` filter); GoTypeManager.java:549-555 (alias → TypedefDataType) | `go1.24.0.json` `all`: `runtime.maptype` is an alias of `internal/abi.OldMapType` (`map_noswiss.go:67:6`). No `internal/abi.MapType` in any linux-amd64 search bucket. OldMapType fields sum to 88 B. The 1.24.6 diff touches none of these (0 matching lines, C7). Whether the alias is skipped as a non-Structure [inference] or resolved, the bound type is OldMapType. |
| 2 | Uncommon block read at structure end | GoType.java:143-150; StructureContext.java:190-204; GoBaseType.java:100-102 (TFlag bit 0) | `textproto.MIMEHeader` map @0x58b0a0, tflag 0x07, SlotSize 40. Uncommon read @0x58b0f8 (+88): PkgPath 40 (low half of SlotSize), Mcount 0, Moff 16. |
| 3 | The uncommon pkgpath is marked up | GoUncommonType.java:38-41 (`@MarkupReference`), 56-59 (`@Markup getPkgPath`) | `resolveNameOff(0x58b0f8, 40)` |
| 4 | `resolveNameOff` checks that the referrer is in [types, etypes); the target is not range-checked | GoRttiMapper.java:581-588, 1053-1064, 1073-1075 | types 0x553000, etypes 0x5e8821 (symtab, equal to `firstmoduledata+296/+304`) → name1 @0x553028 |
| 5 | GoName is read eagerly | GoName.java:93-102; GoVarlenString.java:65-72 | Bytes `6d 00 01 69 00 01`: flags 0x6d (HAS_PKGPATH set, HAS_TAG clear), LEB length 0, pkgPath u32 0x01006901. This is misaligned into 3-byte name records (`00 01 6d`, `00 01 69`, …). |
| 6 | Marking up name1 runs its field-reference getter first | MarkupSession.java:292-297, 324, 336-341 (field funcs), then 348-350 (getter funcs); FieldMappingInfo.java:285-305; GoName.java:88-90, 122-125 | `resolveNameOff(0x553028, 0x01006901)` → name2 @0x1559901 |
| 7 | The flags read hits the bounds check | GoName.java:94; BinaryReader.java:393-407, 987-989; MemoryByteProvider.java:252-261, 289-314. The provider is `MemoryByteProvider(memory, imageBase space)` (DataTypeMapper.java:510-514), so maxOffset is the highest address in that space (MemoryByteProvider.java:112-142, 334-351). | 22386945 > 7627183 → `EOFException: Invalid index: 22386945` |
| H0 | True layout, uncommon at +112 | none | MIMEHeader uncommon @0x58b110: PkgPath 20885 → `net/textproto`, flags 0x00, chain ends. url.Values: PkgPath 7227 → `net/url`, chain ends. Both silent. |

`url.Values` (@0x58dc60, SlotSize 40, H1 uncommon @0x58dcb8) reaches the same name1, so it gives the same N.
A brute-force byte scan, independent of the emulator's discovery, finds 38 map descriptors, 2 of them with
uncommon blocks. That matches `predictions/swiss-misread/s1246-swiss-nethttp.json:59,728`. The emulator's
per-type H1/H0 uncommon reads (`:651-656, 662-667, 680-685, 691-696`) equal mine field for field.

## The observed stack follows this source chain

The exception chain is at `ghidra.log:409-428,451-465`:

- `GoName.readStructure` (`GoName.java:94`), called from `getGoName` (`GoRttiMapper.java:1074`), called from
  `resolveNameOff` (`:1063`), called from `GoName.getPkgPath` (`:124`).
- That call comes from `FieldMappingInfo.addRefToFieldWithGetter` (`:296`) inside `markupFields` (`:339`).
- Above it are three `createMarkupFuncFromGetter` (`:398`) hops, which start at `GoTypeManager.markupGoTypes`
  (`:153`).

I checked each of these frames against the source and every line holds that call, as do
`MemoryByteProvider:254,302`, `BinaryReader:394,406,988` and `DataTypeMapper:413,449`. I did not check the
`ReflectionHelper` or `StructureMappingInfo:156` frames. [observation]

The three getter hops fit this path: T0 marks up the map, the map's `getUncommonType` returns the uncommon
block, its `GoUncommonType.getPkgPath` returns name1, and name1's field-reference getter reads name2. T0 decodes
as the pointer type `*textproto.MIMEHeader` @0x580fa0 (kind 22, elem 0x58b0a0; `GoPointerType.java:44-47` is
the `@Markup getElement`). The emulator's walk names the same type
(`swiss-misread/s1246-swiss-nethttp.json:735-746`). [inference: the log does not print T0.]

## Side findings (none of them refutes this label)

1. **The emulator reports a module-containment failure as `invalid_index`.**
   - `swiss-misread.py:816-818` assigns that kind, and `:1402-1405` renders it as `Invalid index: <referrer>`.
   - Ghidra throws `Unable to find containing module for structure at 0x…` in that case
     (`GoRttiMapper.java:1058-1061`).
   - The depth sentinel (`MAX_NAME_DEPTH` = 8) and the cycle sentinel are also reported as `invalid_index`
     (`:54, :786-790`). Ghidra has no depth cap.
   - C15 reproduces this: a containment failure prints `Invalid index: 7168000`. That index is below
     maxOffset, where Ghidra's provider can never report `Invalid index`.
   - Not triggered in R18: no frozen prediction carries a sentinel detail. Both frozen invalid indices
     (22386945; kimi 15606016) are above their PT_LOAD max (C16), which rules out containment sentinels. I did
     not examine whether the kimi value could be a depth sentinel.
2. **`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:28-33` overstates two points.** It says "no range
   check (`GoRttiMapper.java:1053-1075`)" and "anything else is a silent misread".
   - There is a referrer containment check (`GoRttiMapper.java:1057-1061`).
   - Reads that land in a gap or an uninitialized block abort with `IOException(e.getMessage())`
     (`MemoryByteProvider.java:256-260`).
   - A varint above 2^31-1 aborts with `InvalidDataException` (`BinaryReader.java:1334-1339`).
   - None of these is exercised by this label. To reproduce: `unzip -p` those members (C4).
3. **The emulator's gap scan diverges from Ghidra's.**
   - Emulator: `walk.unindexed_types` is 0/0 (`swiss-misread/s1246-swiss-nethttp.json:751-754`, reproduced by
     C11).
   - Ghidra: `Discovered 39 unindexed Go types` and `Found 1713 Go types` (`ghidra.log:182-183`).
   - The emulator's H1 indexed count is 1674 = 1713 − 39. So discovery matches and only the gap scan differs.
     That affects `walk` only, not the map path or N.
   - Separately, H0 indexed 1602 < H1 indexed 1674. I can't explain this and did not investigate it.
4. Nit: `swiss-misread.py:31` cites `structmapping/MemoryByteProvider.java`. The member is
   `ghidra/app/util/bin/MemoryByteProvider.java`, which `:1565` cites correctly.

**Concordance with wave 1.** `w1/ConnC3Prediction.md:39` and `w1/RevNotesmdMaps.md:134` found the same hop
(0x553028 → 0x1559901). This check did not use their scripts or the emulator: it has its own ELF/GoName parser
and reads the source directly. In addition, rerunning the REV emulator reproduces the frozen JSON byte for byte
(C11).

## Commands (exit codes)

The lane path `L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin` and the variables
`R=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, `F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`,
`Z=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` and
`C=/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp` are shorthand for readability. I typed
the commands with literal paths.

- **C1.** `git -C $L rev-parse HEAD refs/heads/main` → exit 0 (both REV). `git -C $L cat-file -t $R` →
  `commit`, exit 0.
- **C2.** `sha256sum $Z` → `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`, exit 0.
- **C3.** `sha256sum $C $L/.ufo/waves/round-18/carriers/bin/s1246-swiss-nethttp` → both `5c9faf23…`, exit 0.
  `git show $R:.ufo/waves/round-18/carriers/SHA256SUMS | cat -n` → line 5 is the same hash, exit 0.
- **C4.** Several invocations of `unzip -p "$Z" <member> | cat -n | sed -n '<range>p'`, each exit 0. Members:
  GoMapType, GoUncommonType, GoName, GoVarlenString, GoType, GoPointerType, GoBaseType, MemoryByteProvider,
  BinaryReader, GoRttiMapper, GoTypeManager, DataTypeMapper, StructureContext, MarkupSession,
  FieldMappingInfo, StructureMappingInfo, GolangSymbolAnalyzer. The ranges are the ones cited above.
- **C5.** `readelf -W -l -S $C` → exit 0. Last alloc section `.noptrbss` is [0x738c00,0x7461b0), and
  PT_LOAD[2] ends at 0x7461b0.
- **C6.** `readelf -W -s $C | grep -E ' (runtime\.types|runtime\.etypes|runtime\.firstmoduledata|type:net/textproto\.MIMEHeader|type:net/url\.Values|type:\*net/textproto\.MIMEHeader|type:\*net/url\.Values)$| UND '`
  → exit 0/0. Only symbol 0 is UND. `type:*` symbols are absent from .symtab, so I located the maps by byte
  scan.
- **C7.** In `…/data/typeinfo/golang`, `sha256sum go1.24.0.json patchverdiffs/go1.24.6.json.diff` →
  `aab28c8f…`, `e169e8dd…`. A `python3 -I -B -c` dump of the `runtime.maptype`, `internal/abi.MapType`,
  `internal/abi.OldMapType`, `internal/abi.SwissMapType`, `internal/abi.UncommonType` and `internal/abi.Type`
  definitions over the linux-amd64, linux, unix, amd64 and all buckets → exit 0.
  `grep -cE 'maptype|MapType|UncommonType|NameOff' patchverdiffs/go1.24.6.json.diff` → `0`, exit 1.
- **C8.** Appendix A → exit 0 (prints the chain shown above).
- **C9.** Appendix B → exit 0 (T0 = kind 22, elem 0x58b0a0).
- **C10.** Appendix C → exit 0 (offset sweep).
- **C11.** Rerun the REV emulator on the carrier and compare with the frozen JSON → `rerun == frozen: True`,
  `diff keys: []`, exit 0 0 0. The tool's sha256 is `14924bd6…` at both F and R, equal to
  `s1246-swiss-nethttp.prediction.json:18`.

  ```
  git show $R:.ufo/waves/round-18/tools/swiss-misread.py | python3 -I -B - --carrier $C --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang | python3 -I -B -c 'import json,subprocess,sys; a=json.load(sys.stdin); b=json.loads(subprocess.check_output(["git","show","b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/predictions/swiss-misread/s1246-swiss-nethttp.json"])); print("rerun == frozen:", a == b); print("diff keys:", sorted(k for k in set(a)|set(b) if a.get(k)!=b.get(k)))'
  ```

  (The last stage as run also printed the H1/H0 kinds. Run from `cd $L`.)
- **C12.** On the retained log (`$R:.ufo/waves/round-18/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log`):
  - `git show <log> | grep -cE 'Unable to read past EOF'` → `0`, exit 1.
  - `git show <log> | grep -nE 'Invalid index|Unable to find containing module|Go analysis failure'` →
    lines 408 and 451, exit 0.
- **C13.** Freeze ordering and blob identity:
  - `git log -1 --format='%H %cI %s' $F` → `2026-10-20T13:23:55-03:00 … frozen C3 predictions …`, exit 0.
  - `git merge-base --is-ancestor $F $R` → exit 0.
  - `git diff --stat $F $R -- <prediction json ×2, decision-rule.json, swiss-misread.py>` → empty, exit 0.
  - `git rev-parse` of each prediction blob at F and at R → `ec00c310…` and `8f2a745d…` respectively, the same
    at both commits, exit 0.
- **C14.** `git show <log> | sha256sum` → `05ea153e…`, equal to `receipt.json:1901`.
  `receipt.json:8-9` (sha256 pre/post) equals the carrier hash. `run-log.txt:22-23` shows start 13:28:55,
  end 13:29:24, `carrier-run=0 compare=0`. All exit 0.
- **C15.** Appendix D → exit 0 0 (`kind=invalid_index index=7168000 detail='no containing module for 0x6d6000'`).
- **C16.** Appendix E → exit 0. Both frozen invalid indices are above their PT_LOAD max.

## Confidence

High (≈0.95) that the H1 chain gives `Invalid index: 22386945` (not past-EOF) on this carrier:

- N is computed from the bytes.
- Every step is tied to the installed source.
- The observed message and the frame lines I checked match.
- The offset sweep excludes every other 8-aligned descriptor length from 48 to 112.

Residual risks:

- Ghidra's exact memory-block list (maxOffset) is inferred from the ELF. This isn't load-bearing because the
  observed message implies index > maxOffset.
- T0's identity is inferred.
- I did not read `ReflectionHelper` or `GoTypeManager.findDataType` in full.

## Appendix A: independent chain computation (C8, verbatim)

```
python3 -I -B - /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp <<'PY'
import struct, sys, hashlib
P = sys.argv[1]; d = open(P, 'rb').read()
print('carrier sha256', hashlib.sha256(d).hexdigest(), 'size', len(d))
phoff, shoff = struct.unpack_from('<QQ', d, 0x20)
phes, phn, shes, shn, shx = struct.unpack_from('<HHHHH', d, 0x36)
loads = [(va, off, fs, ms) for t, fl, off, va, pa, fs, ms, al in
         (struct.unpack_from('<IIQQQQQQ', d, phoff + i*phes) for i in range(phn)) if t == 1]
S = [struct.unpack_from('<IIQQQQIIQQ', d, shoff + i*shes) for i in range(shn)]
cstr = lambda o: d[o:d.index(b'\0', o)].decode()
sec = {cstr(S[shx][4] + s[0]): s for s in S}
blocks = sorted((s[3], s[3] + s[5], s[1], n) for n, s in sec.items() if s[2] & 2 and s[5])
maxv = max([a + m for a, _, _, m in loads] + [b for _, b, _, _ in blocks]) - 1
print('ram blocks (alloc sections):', ', '.join('%s[0x%x,0x%x)' % (n, a, b) for a, b, _, n in blocks))
print('maxOffset (highest ram address, inclusive) = %d (0x%x)' % (maxv, maxv))
st = sec['.symtab']; strt = S[st[6]][4]; syms = {}
for i in range(st[5] // 24):
    nm, info, oth, shndx, val, size = struct.unpack_from('<IBBHQQ', d, st[4] + i*24)
    if nm: syms.setdefault(cstr(strt + nm), val)
def foff(va):
    for v, o, fs, ms in loads:
        if v <= va < v + fs: return o + va - v
types, etypes, md = syms['runtime.types'], syms['runtime.etypes'], syms['runtime.firstmoduledata']
mt, me = struct.unpack_from('<QQ', d, foff(md + 296))
print('symtab runtime.types=0x%x etypes=0x%x; firstmoduledata@0x%x +296 types=0x%x +304 etypes=0x%x' % (types, etypes, md, mt, me))
assert (mt, me) == (types, etypes)
class RE(Exception): pass
def readb(idx, n):  # MemoryByteProvider.ensureBounds + block lookup
    if n < 0 or n > 0x7fffffff: raise RE('Unable to read more than Integer.MAX_VALUE bytes in one operation: %d' % n)
    if idx > maxv: raise RE('EOFException: Invalid index: %d' % idx)
    if n and n - 1 > maxv - idx: raise RE('EOFException: Unable to read past EOF: %d, %d' % (idx, n))
    out = bytearray()
    for k in range(n):
        o = foff(idx + k)
        if o is None or not any(a <= idx + k < b and t != 8 for a, b, t, _ in blocks):
            raise RE('unmapped/uninitialized read at 0x%x' % (idx + k))
        out.append(d[o])
    return bytes(out)
def leb(p):
    v = sh = n = 0
    while True:
        b = readb(p + n, 1)[0]; n += 1; v |= (b & 0x7f) << sh; sh += 7
        if not b & 0x80: break
    if v > 0x7fffffff: raise RE('InvalidDataException: Value out of range for positive java 32 bit unsigned int: %d' % v)
    return v, n
def goname(va):  # GoName.readStructure (GoName.java:93-102)
    flags = readb(va, 1)[0]; L, n = leb(va + 1); p = va + 1 + n
    name = readb(p, L); p += L; tag = None; pkg = 0
    if flags & 2: TL, tn = leb(p); p += tn; tag = readb(p, TL); p += TL
    if flags & 4: pkg = struct.unpack('<I', readb(p, 4))[0]
    return flags, name, tag, pkg
def chain(ptr, off, label):  # GoRttiMapper.resolveNameOff (1053-1064), recursive pkgPath
    seen = set(); k = 0
    while True:
        if off == 0: print('  %s step%d: nameOff 0 -> null, chain ends' % (label, k)); return None
        if not (types <= ptr < etypes):
            m = 'IOException: Unable to find containing module for structure at 0x%x' % ptr
            print('  %s step%d: %s' % (label, k, m)); return m
        va = types + off
        try: flags, name, tag, pkg = goname(va)
        except RE as e: print('  %s step%d: read GoName @ types+0x%x = %d (0x%x) -> %s' % (label, k, off, va, va, e)); return str(e)
        print('  %s step%d: GoName @0x%x = types+0x%x flags=0x%02x tag?%d pkg?%d namelen=%d name=%r tag=%r pkgPath=0x%x' % (label, k, va, off, flags, flags >> 1 & 1, flags >> 2 & 1, len(name), name[:40], (tag or b'')[:24], pkg))
        if va in seen: print('  cycle'); return 'cycle'
        seen.add(va); ptr, off = va, pkg; k += 1
print('raw bytes types+0x28..+0x48:', d[foff(types + 0x28):foff(types + 0x48)].hex(' '))
# brute-force map type scan (not the emulator's discovery): Size_=8, Kind&0x1f=21, Key/Elem/Group in types range
maps = []
for A in range(types, etypes - 112, 8):
    o = foff(A)
    sz, pb, h, tf, al, fal, kind, eq, gc, s, ptt = struct.unpack_from('<QQIBBBBQQii', d, o)
    if sz != 8 or kind & 0x1f != 21 or not (0 < s < etypes - types): continue
    key, elem, grp = struct.unpack_from('<QQQ', d, o + 48)
    if not all(types <= x < etypes for x in (key, elem, grp)): continue
    try: nm = goname(types + s)[1]
    except RE: continue
    maps.append((A, tf, nm))
print('map type descriptors found by scan: %d; with TFlag uncommon: %d' % (len(maps), sum(1 for m in maps if m[1] & 1)))
for A, tf, nm in maps:
    if not tf & 1: continue
    o = foff(A)
    gs, slot, eoff = struct.unpack_from('<QQQ', d, o + 80)
    print('named map %r @%d (0x%x) tflag=0x%02x Swiss GroupSize=%d SlotSize=%d ElemOff=%d' % (nm, A, A, tf, gs, slot, eoff))
    for label, U in (('H1 OldMapType(88)', A + 88), ('H0 SwissMapType(112)', A + 112)):
        pk, mc, xc, mo = struct.unpack_from('<iHHI', d, foff(U))
        print(' %s: uncommon @0x%x PkgPath=%d Mcount=%d Xcount=%d Moff=%d' % (label, U, pk, mc, xc, mo))
        chain(U, pk, label.split()[0])
PY
echo "exit=$?"
```

Output (observation, abridged to the load-bearing lines):

```
carrier sha256 5c9faf239ed2c68304666992a8d2c1dc40c36e90f8021c62fef4cc4453f201b6 size 4785233
maxOffset (highest ram address, inclusive) = 7627183 (0x7461af)
symtab runtime.types=0x553000 etypes=0x5e8821; firstmoduledata@0x6d8460 +296 types=0x553000 +304 etypes=0x5e8821
raw bytes types+0x28..+0x48: 6d 00 01 69 00 01 71 00 01 74 01 01 52 00 01 64 01 01 4e 00 01 75 00 01 78 00 01 61 00 01 79 00
map type descriptors found by scan: 38; with TFlag uncommon: 2
named map b'*textproto.MIMEHeader' @5812384 (0x58b0a0) tflag=0x07 Swiss GroupSize=328 SlotSize=40 ElemOff=16
 H1 OldMapType(88): uncommon @0x58b0f8 PkgPath=40 Mcount=0 Xcount=0 Moff=16
  H1 step0: GoName @0x553028 = types+0x28 flags=0x6d tag?0 pkg?1 namelen=0 name=b'' tag=b'' pkgPath=0x1006901
  H1 step1: read GoName @ types+0x1006901 = 22386945 (0x1559901) -> EOFException: Invalid index: 22386945
 H0 SwissMapType(112): uncommon @0x58b110 PkgPath=20885 Mcount=5 Xcount=5 Moff=16
  H0 step0: GoName @0x558195 = types+0x5195 flags=0x00 tag?0 pkg?0 namelen=13 name=b'net/textproto' tag=b'' pkgPath=0x0
  H0 step1: nameOff 0 -> null, chain ends
named map b'*url.Values' @5823584 (0x58dc60) tflag=0x07 Swiss GroupSize=328 SlotSize=40 ElemOff=16
 H1 OldMapType(88): uncommon @0x58dcb8 PkgPath=40 Mcount=0 Xcount=0 Moff=16
  H1 step1: read GoName @ types+0x1006901 = 22386945 (0x1559901) -> EOFException: Invalid index: 22386945
 H0 SwissMapType(112): uncommon @0x58dcd0 PkgPath=7227 Mcount=6 Xcount=6 Moff=16
  H0 step0: GoName @0x554c3b = types+0x1c3b flags=0x00 ... name=b'net/url' ... pkgPath=0x0
exit=0
```

## Appendix B: T0 decode (C9, verbatim)

```
python3 -I -B - /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp <<'PY'
import struct, sys
d = open(sys.argv[1], 'rb').read()
loads = [(0x400000, 0x0, 0x152971), (0x553000, 0x153000, 0x182220), (0x6d6000, 0x2d6000, 0x41480)]  # PT_LOAD (vaddr, off, filesz) from readelf -l
def foff(va):
    for v, o, fs in loads:
        if v <= va < v + fs: return o + va - v
types = 0x553000
def name(off):
    p = foff(types + off); fl = d[p]; L = d[p+1]
    return fl, d[p+2:p+2+L]
for A in (0x580fa0, 0x58b0a0, 0x58dc60):
    o = foff(A)
    sz, pb, h, tf, al, fal, kind, eq, gc, s, ptt = struct.unpack_from('<QQIBBBBQQii', d, o)
    p48 = struct.unpack_from('<Q', d, o + 48)[0]
    print('type 0x%x kind=%d tflag=0x%02x size=%d str=%r +48ptr=0x%x' % (A, kind & 0x1f, tf, sz, name(s)[1], p48))
PY
echo "exit=$?"
```

Output: `type 0x580fa0 kind=22 tflag=0x09 size=8 str=b'*textproto.MIMEHeader' +48ptr=0x58b0a0`. The two maps print
kind 21. exit=0.

## Appendix C: uncommon-offset sweep (C10, verbatim)

```
python3 -I -B - /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp <<'PY'
import struct, sys
d = open(sys.argv[1], 'rb').read()
loads = [(0x400000, 0x0, 0x152971), (0x553000, 0x153000, 0x182220), (0x6d6000, 0x2d6000, 0x41480)]
types, etypes, maxv = 0x553000, 0x5e8821, 0x7461af
def foff(va):
    for v, o, fs in loads:
        if v <= va < v + fs: return o + va - v
def b(va):
    if va > maxv: raise IndexError('Invalid index: %d' % va)
    o = foff(va)
    if o is None: raise IndexError('unmapped 0x%x' % va)
    return d[o]
def leb(p):
    v = sh = n = 0
    while True:
        c = b(p + n); n += 1; v |= (c & 0x7f) << sh; sh += 7
        if not c & 0x80: return v, n
def chain(ptr, off):
    seen = set()
    while off:
        if not types <= ptr < etypes: return 'no containing module @0x%x' % ptr
        va = types + off
        if va in seen: return 'cycle'
        seen.add(va)
        try:
            fl = b(va); L, n = leb(va + 1); p = va + 1 + n
            if p + L - 1 > maxv: return 'Unable to read past EOF: %d, %d' % (p, L)
            p += L
            if fl & 2:
                TL, tn = leb(p); p += tn + TL
            off = struct.unpack('<I', bytes(b(p + k) for k in range(4)))[0] if fl & 4 else 0
            ptr = va
        except IndexError as e:
            return str(e)
    return 'silent'
for A in (0x58b0a0, 0x58dc60):
    print('map 0x%x:' % A, '; '.join('+%d -> %s' % (k, chain(A + k, struct.unpack_from('<i', d, foff(A + k))[0])) for k in range(48, 113, 8)))
PY
echo "exit=$?"
```

Output, the same for both maps:
`+48 -> Invalid index: 11242016; +56 -> Invalid index: 11234464; +64 -> Invalid index: 11318848; +72 -> Invalid index: 11545760; +80 -> silent; +88 -> Invalid index: 22386945; +96 -> silent; +104 -> silent; +112 -> silent`.
exit=0.

## Appendix D: emulator containment-sentinel demo (C15, verbatim; run from `$L`)

```
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/swiss-misread.py | python3 -I -B -c '
import sys
ns = {"__name__": "swiss_misread"}
exec(compile(sys.stdin.read(), "swiss-misread.py", "exec"), ns)
m = ns["Machine"].__new__(ns["Machine"])
m.types, m.etypes = 0x553000, 0x5e8821
try:
    m.resolve_name_off(0x6d6000, 40)   # ptr outside [types, etypes)
except ns["ReadError"] as exc:
    print("kind=%s index=%d detail=%r" % (exc.kind, exc.index, exc.detail))
    print("per_type rendering (lines 1402-1405):", "Invalid index: %d" % exc.index)
'; echo "exit=${PIPESTATUS[*]}"
```

Output: `kind=invalid_index index=7168000 detail='no containing module for 0x6d6000'`, then
`per_type rendering (lines 1402-1405): Invalid index: 7168000`. exit=0 0.

## Appendix E: frozen invalid indices vs PT_LOAD max (C16, verbatim; run from `$L`)

```
R=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; for f in $(git ls-tree --name-only $R .ufo/waves/round-18/predictions/swiss-misread/); do git show $R:$f | python3 -I -B -c '
import json, sys, subprocess
j = json.load(sys.stdin)
v = j.get("predicted_invalid_index_reads_h1", []) + j.get("predicted_invalid_index_reads_h0", [])
if not v: sys.exit(0)
out = subprocess.check_output(["readelf", "-W", "-l", j["carrier"]["path"]], text=True)
mx = max(int(l.split()[2], 16) + int(l.split()[5], 16) for l in out.splitlines() if l.split()[:1] == ["LOAD"]) - 1
print(sys.argv[1], "invalid_index values", v, "PT_LOAD max 0x%x" % mx, "all > max:", all(x > mx for x in v))
' "$f"; done; echo "exit=$?"
```

Output: `real-kimi-webbridge.json … [15606016] PT_LOAD max 0xdc7b4f all > max: True` and
`s1246-swiss-nethttp.json … [22386945] PT_LOAD max 0x7461af all > max: True`. exit=0.
