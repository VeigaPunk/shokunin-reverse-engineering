HOLDS

# KimiWebbridgeDerive — independent H1 byte derivation

Axes: **calibration** (conditional attribution), **operability** (complete read-only reproducer), **depth** (ELF → moduledata → named maps → nested GoName).

**Result:** exactly three named map descriptors produce the requested index under H1: **textproto.MIMEHeader, url.Values, and http.Header**. This is a static, conditional derivation, not a new Ghidra run or proof that a map frame caused the retained run's first exception.

All repository citations below are to **REV b2aad08ceeee8dd125ce0d316056d8bd766c7f94**, obtained with the explicit `git show REV:path` commands in section 5. The scoped C3 amendment is `.ufo/waves/round-18/claims.json:33-40`. No overall C3 verdict is made here.

## 1. Reconstructed contract and byte observations

**[OBSERVATION — independent parser, exit 0]** Target `/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge`: 10,031,288 bytes, ELF64 little-endian, inline build version `go1.24.13`, SHA-256 `71067480bd99c2ba0f6d76df50a17e4911917cec8878320c107105066f8ad35d`. This equals the pinned identity at `.ufo/waves/round-18/predictions/swiss-misread/real-kimi-webbridge.json:21-24`.

The parser found the unique consistent moduledata from the `.gopclntab` pointer and five pcHeader/slice relationships, rather than assuming a types address from the prediction:

| Item | Independently decoded value |
|---|---|
| pclntab VA / magic / pointer size | `0xa663e0 / 0xfffffff1 / 8` |
| moduledata VA / file offset | `0xd3d2e0 / 0x93d2e0` |
| types VA / file offset | `0x882000 / 0x482000` |
| etypes (exclusive) | `0xa620e1` |
| typelinks VA / entries | `0xa62100 / 3194` |
| ELF maximum PT_LOAD end, inclusive | `0xdc7b4f` |
| Maximum SHF_ALLOC section end, inclusive | `0xdc7b4f` |

The moduledata fields are words 37/38 (types/etypes) and 44/45 (typelink pointer/count), independently checked against `.rodata` and `.typelink`. The byte-derived values equal the frozen module fields at `.ufo/waves/round-18/predictions/swiss-misread/real-kimi-webbridge.json:65-74`.

**[SOURCE-DERIVED CONTRACT]** H1 uses an 88-byte OldMapType, while the true Swiss descriptor occupies 112 bytes; thus uncommon starts at `T+0x58` rather than `T+0x70`. This is the declared hypothesis at `.ufo/waves/round-18/w1/SwissMisreadTool.md:11-15`, not an independently observed Ghidra configuration in this seat. Installed source corroborates the read law (section 4).

At `T+0x58`, a Swiss descriptor contains `SlotSize`; H1 instead reads its low 32 bits as `PkgPath`, and its zero upper bits as `Mcount/Xcount`. `Moff` becomes the low 32 bits of `ElemOff` (16 here). Resolving that false PkgPath reads a GoName at `types+SlotSize`.

## 2. Which named maps, and the exact failing chain

**[OBSERVATION]** Following all 3,194 typelinks and their type references produced 5,512 distinct type descriptors, no rejected reference, 184 map descriptors, and **five** uncommon map descriptors. An independent 8-byte-aligned scan of the entire types interval, validating the map header, key/element/group types and group size, found the **same 184 map addresses**, with no scan-only or graph-only entry. This is bounded metadata coverage, not reconstruction of Ghidra's discovery/markup order.

All five named maps have kind byte `0x35` (low five bits = map, 21) and tflag `0x07` (Uncommon, ExtraStar, Named). The raw GoName strings in the frozen JSON start with `*`; **ExtraStar means strip that extraneous prefix**, not that these map descriptors are pointer-kind descriptors.

| Go type (raw stored GoName has leading `*`) | Type VA | File offset | SlotSize | H1 uncommon VA | Outcome |
|---|---:|---:|---:|---:|---|
| config.DomainRealm | `0x9031c0` | `0x5031c0` | 32 | `0x903218` | no nested pkgPath / no requested index |
| sarama.BalanceStrategyPlan | `0x91ea60` | `0x51ea60` | 24 | `0x91eab8` | no nested pkgPath / no requested index |
| **textproto.MIMEHeader** | `0x944e80` | `0x544e80` | **40** | `0x944ed8` | **Invalid index: 15606016** |
| **url.Values** | `0x94b780` | `0x54b780` | **40** | `0x94b7d8` | **Invalid index: 15606016** |
| **http.Header** | `0x95f5a0` | `0x55f5a0` | **40** | `0x95f5f8` | **Invalid index: 15606016** |

The three failing rows agree with the frozen per-type claims at `.ufo/waves/round-18/predictions/swiss-misread/real-kimi-webbridge.json:2996-3081`; the two silent rows agree with `.ufo/waves/round-18/predictions/swiss-misread/real-kimi-webbridge.json:2940-2994`. In particular, **five misread maps does not mean five failing maps**.

For each slot-40 map, H1's tuple is `(PkgPath, Mcount, Moff) = (40, 0, 16)`. All three therefore read the same false GoName G1:

`G1 = types + 40 = 0x882028` (file offset `0x482028`). The eight bytes are:

`67 00 01 73 00 01 66 00`

| VA | Interpretation under GoName.readStructure |
|---|---|
| `0x882028` | flags `0x67`: HAS_TAG (2) and HAS_PKGPATH (4) set |
| `0x882029` | ULEB128 name length 0; empty name |
| `0x88202a` | ULEB128 tag length 1 |
| `0x88202b` | tag byte `0x73`, i.e. `s` |
| `0x88202c..0x88202f` | little-endian pkgPath `00 01 66 00` = **`0x00660100`** |

**[SOURCE-DERIVED INFERENCE]** The markup getter resolves G1's pkgPath to a second GoName:

`G2 = 0x00882000 + 0x00660100 = 0x00ee2100 = 15606016`.

G2 is beyond both ELF mapped maxima `0x00dc7b4f`. With the source's address-space-minimum provider base, reading G2's **first flags byte** fails the start-index check. It is therefore **Invalid index**, not an in-range start plus an oversized byte-array read (the distinct “Unable to read past EOF” branch). The carrier ELF maxima are directly observed; this seat did not obtain a live Ghidra memory map.

The other landings do not recurse: `types+32 = 0x882020` has bytes `00 01 78` (flags 0, name `x`), and `types+24 = 0x882018` has flags 1 and name length 110. Neither has HAS_PKGPATH. Unnamed map descriptors, even if slot 40, do not enter this uncommon path.

**Correct-layout invariant:** real uncommon data lies 24 bytes later. For the three maps its package/method pairs are respectively `(56292,5)` → `net/textproto`, `(16696,6)` → `net/url`, `(20036,13)` → `net/http`, at `0x944ef0 / 0x94b7f0 / 0x95f610`. H1 replaces those meaningful package offsets with 40. Its Mcount is **zero**, so this particular index comes from the **false package-name chain**, not from reading a mis-sized method array.

## 3. Evidence chain, divergences, confidence

- **[OBSERVATION]** The independently derived index is exactly the pinned expectation `.ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json:37-42`; the frozen H1/map counts are at `.ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json:15-24`.
- **[OBSERVATION — retained evidence only]** `.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:206-220` records `java.io.EOFException: Invalid index: 15606016`, `MemoryByteProvider.ensureBounds:302`, and `GoName.readStructure:94` via `GoName.getPkgPath:124`. That is the predicted first-byte/read-site taxonomy, not an executed experiment by this seat.
- **[CALIBRATION LIMIT]** The retained trace also contains interface/struct markup frames at `.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:100,114,123,136,149,162,176`. The static map derivation establishes three sufficient routes under H1; the shared numerical result does **not** establish which route the logged traversal reached first, nor that all three map getters executed. The frozen report already distinguishes map and full-walk channels (`.ufo/waves/round-18/w1/SwissMisreadTool.md:17-21,119-122`).
- **Divergences:** none found in the scoped byte-level H1 prediction. Do not inflate this into unconditional causality or an overall mechanism verdict. The apparent leading-star naming difference is raw-name storage, resolved by tflag, not an additional pointer map type.
- **Confidence:** high for the exact three descriptors and `0xee2100` arithmetic under H1; conditional for source-to-import bounds; actual first-path attribution remains unproved here.

## 4. Source/provenance and safety

Read-only source-text corroboration (installed files, **not** Git-versioned lane evidence):

- `~/.local/opt/go-1.24.6/src/runtime/symtab.go:394-419`: moduledata field order/typelinks relative to types.
- `~/.local/opt/go-1.24.6/src/internal/abi/type.go:20-44,107-116,235-241`: common header, Uncommon/ExtraStar/Named flags, uncommon fields.
- `~/.local/opt/go-1.24.6/src/internal/abi/map_swiss.go:32-43`: SwissMapType fields; SlotSize at +88 on amd64.
- `~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` members:
  - `ghidra/app/util/bin/format/golang/rtti/types/GoType.java:143-149`: uncommon at mapped structure end.
  - `ghidra/app/util/bin/format/golang/rtti/types/GoMapType.java:32-62`: OldMapType mapping and unconditional fields.
  - `ghidra/app/util/bin/format/golang/rtti/types/GoUncommonType.java:38-58`: package offset markup getter.
  - `ghidra/app/util/bin/format/golang/rtti/GoName.java:43-47,92-101,123-125`: flags, eager fields, nested pkgPath getter.
  - `ghidra/app/util/bin/format/golang/rtti/GoVarlenString.java:65-71`: ULEB128 then byte array.
  - `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:1053-1074`: types + offset, no pre-read range restriction.
  - `ghidra/app/util/bin/format/golang/structmapping/DataTypeMapper.java:503-513`: reader based at image address space minimum; indices/address offsets synonymous.
  - `ghidra/app/util/bin/MemoryByteProvider.java:153-159,289-313,334-350`: max index construction and distinct exception branches.

Semantic navigation availability: `read xd://lsp` returned **“No such tool”**; no LSP server/device was available to query. These are literal source reads plus independently decoded bytes, not grep asserted as semantic reference proof. Initial source searches are only navigation aids.

No installs/upgrades (none needed). Python used: **3.14.8**, stdlib only, all subprocess invocations `python3 -I -B`. No REA CLI/device invocation, Ghidra invocation, carrier execution, git write, jj command, clone, or file modification other than this report. The lane emulator was **not executed or imported**. The first preparatory PATH query found no `go`; the existing toolchain sources were then read without running Go.

## 5. Reproducing commands and exits

The following Git commands ran from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; each exited **0**, with empty stderr. Line-numbered excerpts above were selected from their complete captured stdout, not from the working tree.

```sh
'git' 'show' 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/predictions/real-kimi-webbridge.prediction.json'  # exit 0
'git' 'show' 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/predictions/swiss-misread/real-kimi-webbridge.json'  # exit 0
'git' 'show' 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log'  # exit 0
'git' 'show' 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/w1/SwissMisreadTool.md'  # exit 0
'git' 'show' 'b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/claims.json'  # exit 0
```

### Independent ELF probe — exit 0

The quoted -c argument below is the complete executed code; no script file is required. It reports the sections/program headers, all candidate pclntab pointers, moduledata words, mapped maxima, digest and inline version bytes. It does not import any lane tool.

```sh
python3 -I -B -c "import struct, pathlib, hashlib, sys
b=pathlib.Path('/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge').read_bytes()
print('python',sys.version.split()[0], 'sha256',hashlib.sha256(b).hexdigest(),'size',len(b))
assert b[:6]==b'\\x7fELF\\x02\\x01'
u=lambda f,o:struct.unpack_from('<'+f,b,o)[0]
phoff,shoff=u('Q',32),u('Q',40)
phsz,phnum,shsz,shnum,shstr=(u('H',x) for x in (54,56,58,60,62))
sh=[struct.unpack_from('<IIQQQQIIQQ',b,shoff+i*shsz) for i in range(shnum)]
st=b[sh[shstr][4]:sh[shstr][4]+sh[shstr][5]]
sections={st[s[0]:st.index(0,s[0])].decode():s for s in sh}
for n,s in sections.items():
 if s[2]&2:print('section',n,'va',hex(s[3]),'off',hex(s[4]),'size',hex(s[5]),'type',s[1])
load=[]
for i in range(phnum):
 p=struct.unpack_from('<IIQQQQQQ',b,phoff+i*phsz)
 if p[0]==1:
  load.append(p);print('PT_LOAD','va',hex(p[3]),'off',hex(p[2]),'filesz',hex(p[5]),'memsz',hex(p[6]),'end',hex(p[3]+p[6]-1))
pcl=sections['.gopclntab'];pva=pcl[3]
print('pclntab','va',hex(pva),'header',b[pcl[4]:pcl[4]+72].hex(' '))
def voff(a):
 for p in load:
  if p[3]<=a<p[3]+p[5]:return p[2]+a-p[3]
 raise ValueError(hex(a))
needle=struct.pack('<Q',pva);at=0
while True:
 at=b.find(needle,at)
 if at<0:break
 va=next((p[3]+at-p[2] for p in load if p[2]<=at<p[2]+p[5]),None)
 print('pclntab_pointer','file',hex(at),'va',hex(va) if va is not None else None)
 if at%8==0 and at+400<=len(b):
  w=struct.unpack_from('<50Q',b,at)
  print('module_candidate_fields',[(i,hex(w[i])) for i in (1,4,7,10,13,16,20,21,22,23,37,38,39,40,41,42,43,44,45,46)])
 at+=1
print('max_PT_LOAD',hex(max(p[3]+p[6]-1 for p in load)))
print('max_SHF_ALLOC',hex(max(s[3]+s[5]-1 for s in sh if s[2]&2)))
bi=sections['.go.buildinfo'];o=bi[4];print('buildinfo_prefix',b[o:o+80].hex(' '))
"
# exit 0
```

### Independent full derivation — exit 0

This separate stdlib parser determines its own moduledata, walks the type graph, cross-checks the map census by an aligned scan, and emits the GoName chain for each observed slot size. Its reference walk uses the true Swiss layout; only the specified uncommon read is reinterpreted under H1. No expected carrier-specific address or index is an input.

```sh
python3 -I -B -c "import struct, pathlib, hashlib, collections, sys
b=pathlib.Path('/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge').read_bytes()
u=lambda f,o:struct.unpack_from('<'+f,b,o)[0]
assert b[:6]==b'\\x7fELF\\x02\\x01'
ph=[struct.unpack_from('<IIQQQQQQ',b,u('Q',32)+i*u('H',54)) for i in range(u('H',56))]
loads=[p for p in ph if p[0]==1]
sh=[struct.unpack_from('<IIQQQQIIQQ',b,u('Q',40)+i*u('H',58)) for i in range(u('H',60))]
st=sh[u('H',62)];strings=b[st[4]:st[4]+st[5]]
s={strings[x[0]:strings.index(0,x[0])].decode():x for x in sh}
def off(a,n=1):
 for p in loads:
  if p[3]<=a and a+n<=p[3]+p[5]:return p[2]+a-p[3]
 raise ValueError('not file backed: '+hex(a))
def v(f,a):return u(f,off(a,struct.calcsize('<'+f)))
def bs(a,n):return b[off(a,n):off(a,n)+n]
def leb(a):
 value=shift=0
 while True:
  c=v('B',a);a+=1;value|=(c&127)<<shift
  if c<128:return value,a
  shift+=7
  if shift>=63:raise ValueError('long LEB128')
def gname(a):
 start=a;flags=v('B',a);n,a=leb(a+1);name=bs(a,n);a+=n;tag=None
 if flags&2:n,a=leb(a);tag=bs(a,n);a+=n
 po=a if flags&4 else None;pkg=v('I',a) if po is not None else 0
 return dict(addr=hex(start),flags=hex(flags),name=repr(name),tag=repr(tag),pkg_at=hex(po) if po else None,pkg=hex(pkg),length=a+4-start if po else a-start),name,pkg
pcl=s['.gopclntab'];pva=pcl[3];h=pcl[4]
assert u('I',h)==0xfffffff1 and b[h+7]==8
mods=[];at=0
while True:
 at=b.find(struct.pack('<Q',pva),at)
 if at<0:break
 if at%8==0 and at+376<=len(b):
  w=struct.unpack_from('<47Q',b,at)
  if all(w[i]==pva+u('Q',h+j) for i,j in ((1,32),(4,40),(7,48),(10,56),(13,64))) and w[44]==s['.typelink'][3] and w[45]*4==s['.typelink'][5]:mods.append((at,w))
 at+=1
assert len(mods)==1
md,w=mods[0];types,etypes=w[37:39];tl,n=w[44:46]
assert (types,etypes)==(s['.rodata'][3],s['.rodata'][3]+s['.rodata'][5])
maxva=max(p[3]+p[6]-1 for p in loads)
print('identity',sys.version.split()[0],len(b),hashlib.sha256(b).hexdigest())
print('moduledata file',hex(md),'VA',hex(next(p[3]+md-p[2] for p in loads if p[2]<=md<p[2]+p[5])))
print('types',hex(types),'etypes',hex(etypes),'typelinks',hex(tl),'count',n,'maxva',hex(maxva))
bi=s['.go.buildinfo'][4];verlen,vi=leb(s['.go.buildinfo'][3]+32)
print('version',bs(vi,verlen).decode())
def header(a):
 assert types<=a and a+48<=etypes
 size,ptr=v('Q',a),v('Q',a+8);tflag,align,field,kind=bs(a+20,4)
 assert ptr<=size and align in (1,2,4,8) and field in (1,2,4,8) and 1<=kind&31<=26
 no=v('i',a+40);assert 0<no<etypes-types
 gn,raw,pkg=gname(types+no)
 return kind&31,tflag,raw[1:] if tflag&2 and raw.startswith(b'*') else raw,raw,no
roots={types+v('i',tl+i*4) for i in range(n)}
seen=set();queue=list(roots);bad=[]
while queue:
 a=queue.pop()
 if a in seen:continue
 seen.add(a)
 try:
  k,f,name,raw,no=header(a);refs=[];core=48
  pt=v('i',a+44)
  if pt>0:refs.append(types+pt)
  if k in (17,18,22,23):
   refs.append(v('Q',a+48));core={17:72,18:64,22:56,23:56}[k]
   if k==17:refs.append(v('Q',a+56))
  elif k==21:
   refs.extend(v('Q',a+x) for x in (48,56,64));core=112
  elif k==19:
   core=56;inc,out=v('H',a+48),v('H',a+50)&32767
   refs.extend(v('Q',a+core+(16 if f&1 else 0)+8*i) for i in range(inc+out))
  elif k in (20,25):
   core=80;data,num=v('Q',a+56),v('Q',a+64)
   if k==20:refs.extend(types+v('i',data+i*8+4) for i in range(num))
   else:refs.extend(v('Q',data+i*24+8) for i in range(num))
  if f&1:
   ut=a+core;cnt,moff=v('H',ut+4),v('I',ut+8)
   refs.extend(types+mt for i in range(cnt) if (mt:=v('i',ut+moff+i*16+4))>0)
  queue.extend(r for r in refs if r not in seen and r)
 except (AssertionError,ValueError,struct.error) as e:bad.append((hex(a),str(e)))
maps={a for a in seen if types<=a<a+48<=etypes and v('B',a+23)&31==21}
named=sorted(a for a in maps if v('B',a+20)&1)
print('graph roots',len(roots),'visited',len(seen),'bad',bad,'maps',len(maps),'uncommon',len(named))
scan=set()
for a in range(types,etypes-112+1,8):
 if v('B',a+23)&31!=21 or v('Q',a)!=8 or v('Q',a+8)!=8:continue
 try:
  k,f,name,raw,no=header(a)
  for x in (48,56,64):header(v('Q',a+x))
  if v('Q',a+80)!=v('Q',v('Q',a+64)):continue
  scan.add(a)
 except (AssertionError,ValueError,struct.error):pass
print('aligned validated scan maps',len(scan),'only_scan',[hex(a) for a in sorted(scan-maps)],'only_graph',[hex(a) for a in sorted(maps-scan)])
for slot in sorted({v('Q',a+88) for a in named}):
 a=types+slot;d,raw,pkg=gname(a)
 print('H1_GoName slot',slot,'file',hex(off(a)),'bytes',bs(a,d['length']).hex(' '),d,'G2',hex(types+pkg) if pkg else None)
for a in named:
 k,f,name,raw,no=header(a);slot=v('Q',a+88);d,raw1,pkg=gname(types+slot)
 g2=types+pkg if pkg else None;h1=v('I',a+88),v('H',a+92),v('I',a+96)
 ut=a+112;h0=v('I',ut),v('H',ut+4),v('I',ut+8);p0=gname(types+h0[0])[1]
 print('MAP',hex(a),'file',hex(off(a)),'kind',hex(v('B',a+23)),'tflag',hex(f),'nameOff',hex(no),'raw',repr(raw),'Go',name.decode(),'slot',slot,'H1',h1,'H0',h0,'real_pkg',repr(p0),'G2',hex(g2) if g2 else None,'result',('Invalid index: '+str(g2)) if g2 and g2>maxva else 'no invalid index')
"
# exit 0
```

Selected exact stdout (the slot-24 garbage-name byte dump is omitted here):

```text
identity 3.14.8 10031288 71067480bd99c2ba0f6d76df50a17e4911917cec8878320c107105066f8ad35d
moduledata file 0x93d2e0 VA 0xd3d2e0
types 0x882000 etypes 0xa620e1 typelinks 0xa62100 count 3194 maxva 0xdc7b4f
version go1.24.13
graph roots 3194 visited 5512 bad [] maps 184 uncommon 5
aligned validated scan maps 184 only_scan [] only_graph []
H1_GoName slot 40 file 0x482028 bytes 67 00 01 73 00 01 66 00 {'addr': '0x882028', 'flags': '0x67', 'name': "b''", 'tag': "b's'", 'pkg_at': '0x88202c', 'pkg': '0x660100', 'length': 8} G2 0xee2100
MAP 0x9031c0 file 0x5031c0 kind 0x35 tflag 0x7 nameOff 0x17bfc raw b'*config.DomainRealm' Go config.DomainRealm slot 32 H1 (32, 0, 16) H0 (154643, 0, 16) real_pkg b'github.com/jcmturner/gokrb5/v8/config' G2 None result no invalid index
MAP 0x91ea60 file 0x51ea60 kind 0x35 tflag 0x7 nameOff 0x1f960 raw b'*sarama.BalanceStrategyPlan' Go sarama.BalanceStrategyPlan slot 24 H1 (24, 0, 16) H0 (122639, 1, 16) real_pkg b'github.com/Shopify/sarama' G2 None result no invalid index
MAP 0x944e80 file 0x544e80 kind 0x35 tflag 0x7 nameOff 0x19c94 raw b'*textproto.MIMEHeader' Go textproto.MIMEHeader slot 40 H1 (40, 0, 16) H0 (56292, 5, 16) real_pkg b'net/textproto' G2 0xee2100 result Invalid index: 15606016
MAP 0x94b780 file 0x54b780 kind 0x35 tflag 0x7 nameOff 0xa359 raw b'*url.Values' Go url.Values slot 40 H1 (40, 0, 16) H0 (16696, 6, 16) real_pkg b'net/url' G2 0xee2100 result Invalid index: 15606016
MAP 0x95f5a0 file 0x55f5a0 kind 0x35 tflag 0x7 nameOff 0xb631 raw b'*http.Header' Go http.Header slot 40 H1 (40, 0, 16) H0 (20036, 13, 16) real_pkg b'net/http' G2 0xee2100 result Invalid index: 15606016
```

<details>
<summary>Preparatory command ledger (overall shell exit 0 for each; not the independent derivation)</summary>

These initial shell/pipeline invocations are retained for transparency. Overall group success does not imply every intermediate command succeeded: in particular, the `go` PATH/version probe reported command-not-found; the final source-zip listing succeeded. Subsequent semantic/source navigation used the specialized read/grep tools. No preparatory result is substituted for the independent parser evidence.

```sh
file /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge; ls -la /home/vgpnk/.kimi-webbridge/bin/; sha256sum /home/vgpnk/.kimi-webbridge/bin/kimi-webbridge
# overall exit 0

which go python3 unzip readelf objdump nm xxd 2>&1; go version 2>&1 | head -2; ls -la /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip 2>&1
# overall exit 0

cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib && unzip -p Base-src.zip ghidra/app/util/bin/MemoryByteProvider.java | cat -n | sed -n '1,120p'
# overall exit 0

cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib && unzip -p Base-src.zip ghidra/app/util/bin/MemoryByteProvider.java | cat -n | sed -n '120,330p'
# overall exit 0

cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib && unzip -p Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoName.java | cat -n | sed -n '55,140p'
# overall exit 0

cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib && unzip -p Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | cat -n | sed -n '1040,1085p' && unzip -p Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoVarlenString.java | cat -n | sed -n '55,90p'
# overall exit 0

cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib && unzip -p Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoName.java | cat -n | sed -n '1,55p' && echo ===== && unzip -p Base-src.zip ghidra/app/util/bin/MemoryByteProvider.java | cat -n | sed -n '330,365p'
# overall exit 0

cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib && unzip -p Base-src.zip ghidra/app/util/bin/format/golang/rtti/types/GoType.java | cat -n | sed -n '100,160p' && echo ==GoUncommonType== && unzip -p Base-src.zip ghidra/app/util/bin/format/golang/rtti/types/GoUncommonType.java | cat -n | sed -n '30,110p'
# overall exit 0

ls /home/vgpnk/.local/opt/ 2>/dev/null | head -20; ls /home/vgpnk/.local/opt/go-1.24.6/src/internal/abi/ 2>/dev/null; ls /home/vgpnk/.local/opt/go-1.25.0/src/internal/abi/ 2>/dev/null
# overall exit 0

cd /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib && unzip -l Base-src.zip | grep -E "golang.*(GoRttiMapper|GoTypeManager|DataTypeMapper|MarkupSession|StructureContext)\.java" && unzip -p Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | grep -n "ByteProvider\|getTypesOffset\|getMaxOffset" | head -20
# overall exit 0
```
</details>

Report: .ufo/waves/round-18/w2/KimiWebbridgeDerive.md
