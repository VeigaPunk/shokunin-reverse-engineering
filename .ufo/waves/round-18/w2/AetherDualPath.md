BROKEN — the INFERENCE at `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:101-106` says the aether bad read "is reachable from more than the map path". The retained stack it cites is the map path. The stack has 12 markup levels. The last three are: a func-param type → `GoType.getUncommonType` → `GoUncommonType.getPkgPath` → GoName `0x954048`. The struct/interface frames are the container route that Ghidra's address-sorted markup took to reach the map. They are not a second route to the read. The INFERENCE's supporting facts hold: the frame lines, `0x954048` as the misread `PkgPath` of three 40-slot maps, and the two emulator channels. "The frozen prediction used the map path" holds in effect: on 15/15 labels the frozen lists equal the map-only lists.

# AetherDualPath — aether retained stack vs the r18 map-path INFERENCE (round 18, wave 2, falsify)

Seat `KaidokuR18.AetherDualPath` (revenger). This is an author-side advisory seat, not outside review.
- **Revisions.** REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` = `refs/heads/main` (C1).
- **Anchors.** Lane anchors are `git show REV:path` lines, and every cited tracked file is byte-identical in the working tree (C2). The exception is w2 sibling reports (`w2/*.md`), which are untracked; those are cited at their working-tree lines as read on 2026-10-20. Ghidra anchors are members of the installed `Base-src.zip` (sha256 `f00d29c2…a8d804`, S003, C4).
- **Labels.** **O** = observation; **I** = inference.
- **Scope.** Read-only: no REA or Ghidra run, no carrier executed (`/usr/bin/aether` bytes were only read), nothing installed. This file is the only write.
- **Abbreviations.**
  - LOG = `.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log` (sha256 `bb3d2e16…f78e65e`, REV = working tree, 244 lines).
  - KE = the knowledge entry.
  - SM = `.ufo/waves/round-18/tools/swiss-misread.py`.

## Answer: which path does Ghidra's markup order reach first?

The container path reaches the read first, and that path ends in the map path. There is one route, not two.

1. **O (source).** Markup order:
   - The analyzer creates a fresh `MarkupSession` and calls `markupGoTypes` as its first markup step (`GolangSymbolAnalyzer.java:142-146`). firstmoduledata is marked up after that (`:148-152`).
   - `markupGoTypes` marks every type in ascending unsigned address order (`GoTypeManager.java:151-153,263-269`).
   - The first `IOException` aborts the whole analyzer (`GolangSymbolAnalyzer.java:181-183`). LOG has exactly one `Go analysis failure` (LOG:97; C16).
2. **O (log + source).** LOG:98-154 segments into 12 markup levels (C5, table below). The outermost level (L0) is a top-level type from the address loop (LOG:154 `GoTypeManager.java:153`). The innermost (L11) is the GoName whose `pkgPath` field reference throws (LOG:100-102, 196, 177).
3. **I (high).** Identity of the levels: L0 = `*options.App` `0x9857C0` → … → L9 = `http.Header` `0xA350A0`.
   - The frames carry no addresses, so this cannot be read from LOG.
   - It rests on three things: the emulator's `walk.h1.path` (rerun byte-identical, C11); my own byte decode along the same 12-level shape (C8); and the order checks below (C9, C10).
4. **O (bytes) + I.** `0x9857C0` is below the lowest 40-slot map (`textproto.MIMEHeader` `0xA1C7A0`). So the container route came first, and no 40-slot map was ever marked at its own turn in the loop.

## Level map (C5 frame segmentation; classes from source; identities I, bytes C8)

| L | LOG line of `markup:127` | entered by | leaves by | class (how known) | identity (I) and bytes (O) |
|---|---|---|---|---|---|
| 0 | 153 | `markupGoTypes:153` loop | class `@Markup` getter | getter returns a struct: ptr/slice/array/chan/map elem (I: `GoPointerType.getElement`, `GoPointerType.java:44-47`) | `*options.App` `0x9857C0`, tflag `0x08` (no uncommon) |
| 1 | 149 | getter result | `GoStructType.additionalMarkup:94` (LOG:147) | GoStructType (O) | `options.App` `0xA515C0`, uncommon mcount 0 |
| 2 | 144 | slice element | getter | GoStructField (O, `GoStructType.java:94`) → `getType` `GoStructField.java:68-71` | field[15] `AssetsHandler` |
| 3 | 140 | getter result | `GoInterfaceType.additionalMarkup:77` (LOG:138) | GoInterfaceType (O) | `http.Handler` `0x9CBA40` |
| 4 | 135 | slice element | getter | GoIMethod (O, `GoInterfaceType.java:77`) → `getType` `GoIMethod.java:56-60` | `ServeHTTP` |
| 5 | 131 | getter result | getter that returns a List | GoFuncType (O, see ①) | `func(http.ResponseWriter, *http.Request)` `0x9A98C0` |
| 6 | 126 | List element | `GoInterfaceType.additionalMarkup:77` (LOG:124) | GoInterfaceType (O) | `http.ResponseWriter` `0x9DAF00` (param[0]) |
| 7 | 121 | slice element | getter | GoIMethod (O) | `Header` |
| 8 | 117 | getter result | getter that returns a List | GoFuncType (O, ①) | `func() http.Header` `0x99D420` |
| 9 | 112 | List element | class getter | GoType whose getter returned L10; that getter is `getUncommonType` (O, ②) | `http.Header` `0xA350A0`, kind 21, tflag `0x07`, SlotSize 40 |
| 10 | 108 | getter result | getter | GoUncommonType (O, ②) → `getPkgPath` `GoUncommonType.java:56-59` | read at T+88 = `0xA350F8`: PkgPath `0x28`, Mcount 0 (true uncommon at +112: `net/http`, Mcount 13) |
| 11 | 104 | getter result | field ref `@MarkupReference("getPkgPath")` (`GoName.java:88-89`, LOG:100-102) | GoName (O, LOG:196 `GoName.getPkgPath:124`) | `0x954048`: `6e 00 01 61 00 01 78 00`, pkgPath `0x780100` → `0x10D4120` (flags `0xf6`) → A=17645861, B=111938854 = LOG:177 |

How each transition maps to source (O):
- `markup:105` marks Collection elements; `markup:127` → `markupStructure` (`MarkupSession.java:103-106,127`).
- Within `markupStructure`, the order is fields (`:336-341`, `:339`), then class `@Markup` getters (`:348-350`, `:349`), then `additionalMarkup` (`:326-328`, `:327`).
- Getter results are marked with `nested=false` (`StructureMappingInfo.java:394-399`), and so are deduped (`MarkupSession.java:295-297`).
- Slice elements are marked with `nested=true` (`GoSlice.java:349-358`).

**① L5/L8 are func types (O).** L6 and L9 are entered as elements of a List returned by a getter (LOG:127, 113: `markup:105` under `createMarkupFuncFromGetter:398`). The golang package has 29 `@Markup` sites (C6). Only two return a List: `GoFuncType.getParamTypes` (`GoFuncType.java:106-111`) and `GoModuledata.getItabs`. Of those, only `getParamTypes` is reachable from `GoIMethod.getType`.

**② L10 is a misread uncommon (O + one w1 premise).** L11's getter target was read at `0x10D4120` = types + `0x780100`, so L11 is a GoName whose pkgPath is `0x780100`. Two scans pin it down:
- **Scan A (C9).** Exactly one start in `[types, etypes)` parses with HAS_PKGPATH and pkgPath `0x780100`: `0x954048`.
- **Scan C (C9).** `0x954048` is the `n` byte inside the genuine 3-byte record at `0x954046`. Records run `0x954040, …43, …46, …49, …`. So no genuine name offset points at it.

L10's getter returned that GoName. The candidates for L10 are:
- **A GoStructType/GoInterfaceType** via `getPkgPath`. These getters are pointer-based (`GoStructType.java:49-52`, `GoInterfaceType.java:52-55`). Scan B found no 8-byte pointer to `0x954048` anywhere in the file, which rules this out.
- **A GoName** via `GoName.getPkgPath` (`GoName.java:122-125`). L9 would then have returned that GoName through a pointer-based `getPkgPath`. 72 positions parse with pkgPath `0x28`, but none is the target of any pointer (Scan D). Ruled out.
- **A GoBaseType** via `getGoName`. A GoBaseType is only marked as the nested `typ` field (`GoType.java:72-75` → `FieldMappingInfo.java:151-158,280-283`). That would put `FieldMappingInfo.markupNestedStructure` on the stack, and LOG has no such frame (C16: count 0; the only `FieldMappingInfo` frames are l.100-101). Ruled out.
- **A GoUncommonType** with PkgPath `0x28`. This is the only candidate left. A correctly read uncommon cannot hold `0x28` (Scan C), so this one is misread.

Only map types are bound with the wrong length: `OldMapType` is 88 bytes and Swiss is 112 (w1 `RevGhidraMapTypeRead.md` §3; I did not re-derive this). A Swiss map's T+88 is `SlotSize`. The three 40-slot named maps (`0xA1C7A0`, `0xA229A0`, `0xA350A0`) each read PkgPath `0x28` (C8). `getUncommonType` is L9's first class getter, because getters are collected superclass-first (`ReflectionHelper.java:362-365`, `StructureMappingInfo.java:90-94`; `GoMapType extends GoType`, `GoMapType.java:35`, `GoType.java:143-150`).

**Why the first throw is at L9→L10 and not deeper inside L9.**
- **O, ptrToThis is marked first.** Before L9's class getters run, its `typ` field marks `getGoName`/`getPtrToThis` (`GoBaseType.java:108-128`). For `http.Header` that marks `*http.Header` `0xA2E4E0` (C9).
- **O, three methods resolve to null.** `*http.Header` has 13 methods. Three have `mtyp` −1: `sortedKeyValues`, `write`, `writeSubset`. `resolveTypeOff` returns null for −1 (`GoTypeManager.java:702-705`).
- **O signatures, I closure.** The 10 reachable signatures (C10) name no other 40-slot map. `Clone` → `func() http.Header` = L8, which is already marked. I infer that the closures of the remaining types (`io.Writer`, `error`, `map[string]bool`, `string`, `[]string`) contain no named map.
- **O, go1.25.0 source.** `write` and `writeSubset` take `*httptrace.ClientTrace` (`net/http/header.go:89,190`). `ClientTrace.Got1xxResponse` is `func(code int, header textproto.MIMEHeader) error` (`httptrace/trace.go:115`).
- **I, counterfactual.** Without those −1 entries, the deepest frames would end at `textproto.MIMEHeader` (one of the 40-slot maps) by way of `*http.Header`'s methods, not at L9's own uncommon.

## The INFERENCE, clause by clause (KE:101-106)

| Clause | Status | Evidence |
|---|---|---|
| "the bad read is reachable from more than the map path" | **BROKEN** | L9–L11 are the map path. Scans A–D find no non-map producer of the `0x954048` → `0x780100` chain. Read as "reached through containers, not only at the map's own turn", the sentence is true, but then it describes the same path. The two-route meaning is the one the lineage intended: `RevGhidraMapTypeRead.md:315-329` → `SwissMisreadTool.md:101-102,121` → `lessons/round-18.md:22`. |
| "retained stack runs through struct/interface markup (`GoStructType.additionalMarkup:94` → `GoInterfaceType.additionalMarkup:77`" | HOLDS, incomplete | O: LOG:147, 138, 124. There are two interface frames. The clause leaves out L5–L11. |
| cites w1 `RevGhidraMapTypeRead.md` for that | **premise BROKEN** | `RevGhidraMapTypeRead.md:315-320` reads L4 → "GoIMethod name `@MarkupReference` → GoName markup → pkgPath" with "no GoMapType/GoUncommonType frame". That reading would put one level after the imethod. LOG has seven (L5–L11). Class-name frames are absent by construction: the getter has already returned (`StructureMappingInfo.java:397`) when `session.markup` runs (`:398`). C15: 0 `GoMapType`/`GoUncommonType` frames. |
| "the same GoName at `0x954048` is the misread `PkgPath` of three 40-slot maps (w1 `RevAetherReplay.md`)" | HOLDS | O: C8 bytes. The cited report itself concludes that the logged chain *is* the `http.Header` map path (`RevAetherReplay.md:14-34,181-224`). |
| "The emulator reports both channels" | HOLDS | O: `predictions/swiss-misread/calib-aether.json:27-46` (map path, 3 failing maps) and `:2632-2684` (walk). `walk.h1.path` (`:2665-2673`) ends at `func.param[0]`, the map. So the walk also reaches the read through the map. Rerun is byte-identical (C11). |
| "the frozen prediction used the map path" | HOLDS in effect | O: on all 15 labels the frozen `eof_reads`/`invalid_index_reads` equal the map-only lists (C12). The code does merge walk reads, though (SM:1441-1460; the kind is derived from the merged lists, SM:1479-1480; frozen at `gen-predictions.py:51-59`). This matches w2 `KnowledgeEntryReview.md` F7. |

## Divergences to route (recommendations; I edited nothing)

1. **KE:101-106.** Suggested replacement:
   > OBSERVATION (frames + source): the aether stack is the map path, reached through containers. Its 12 markup levels end in func param → `GoType.getUncommonType` → `GoUncommonType.getPkgPath` → GoName `0x954048` (ghidra.log:104-121). Types are marked in address order (`GoTypeManager.java:151-153,263-269`), so a container (I: `*options.App` `0x9857C0` → `AssetsHandler` → `ServeHTTP` → `ResponseWriter.Header`) reaches `http.Header` before any 40-slot map's own turn. INFERENCE: the identities (no addresses are logged). Frozen lists equal map-only lists on 15/15; the code also merges walk reads (`swiss-misread.py:1441-1460`).
2. **`corpus/lessons/round-18.md:22`.** The row rejects "aether's failure is on the map path" "as stated", on the same premise. It also credits `RevAetherReplay.md` with "the map path is a second route". That phrase does not appear in `RevAetherReplay.md` (C14). It comes from `SwissMisreadTool.md:121`. On this evidence the candidate should be admitted, with the limit "reached through container markup; identity inferred".
3. **KE:117-118.** "walk … was never used as a prediction" is true in effect but not in code: SM:1445-1447 and 1454-1456 add walk reads to the frozen lists. In the 15 frozen labels this added nothing (C12).
4. **Siblings (disagree).** w2 `CapabilityCandidate.md:71` says the frames "cannot show whether that route enters a misread map type". w2 `KnowledgeDecisionTable.md:81` says "The map path is never visible in a stack trace". The map path is not visible by class name. It is visible by shape, as L9–L11 (C5).
5. **Out of scope, O.** The same segmentation of s1246-swiss-nethttp (4 levels) and real-kimi-webbridge (24 levels) ends in the same tail `… → getter → getter → field ref` (C13). I did not check their identities.

## Limits and confidence

- **High (O, source + log):** the frame semantics and the 12-level shape.
- **High (O, bytes):** the decoded chain and Scans A–D. Scans A and D look back at most 48 bytes from each 4-byte match, so a longer apparent name+tag is not covered.
- **INFERENCE (high):** the identities of L0–L9.
- **INFERENCE, emulator only:** "fields 0–14 of `options.App` and all types below `0x9857C0` reach no 40-slot map". The emulator index is 5924 types, against Ghidra's 5927 + 188 unindexed (`SwissMisreadTool.md:123-128`). So 191 Ghidra types are absent from the walk. I did not re-derive this.
- **INFERENCE:** that `OldMapType` is the only wrong-length binding (w1). The go1.25.0 signatures are taken as standing for go1.25.14.
- One Ghidra release (12.1.4), one retained log.

## Commands (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless `cd` shown; R = REV)

- **C1** — exit 0 / 0 / 0:
  - `git -C …/kaidoku-shokunin cat-file -t b2aad08…` → `commit`
  - `git … rev-parse refs/heads/main` → `b2aad08…`
  - `git … ls-tree -r --name-only R -- …calib-aether …/tools …/predictions KE` → 57 paths, including LOG.
- **C2** — exit 0:
  - `git show R:LOG | sha256sum` and `sha256sum LOG` → both `bb3d2e1653a6d4e2114d8a3a7c7791922b09b3010ddc5f6f2070f1245e78f65e`; `wc -l` → 244.
  - A loop of `git show R:$p | sha256sum` vs `sha256sum $p` over SM, `gen-predictions.py`, the aether prediction/emulator JSON, KE and three w1 reports → REV = working tree for all 8.
- **C3** — exit 0,0: `git show R:LOG | grep -nE 'GoStructType|GoInterfaceType|…|Caused by'` → matched l.94-95 (GoTypeManager INFO lines), 100-154, 172, 176-177, 188, 194, 196, 198. The only `FieldMappingInfo` frames are l.100-101 (`addRefToFieldWithGetter:296`, `makeMarkupReferenceFunc:290`); see C16 for the `markupNestedStructure` count.
- **C4** — exit 0: `sha256sum …/Base-src.zip` → `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`. Source lines were printed with `python3 -I -B -c "import zipfile…show(member,a,b)"`, exit 0 for each call. Members: MarkupSession 80-360; GoTypeManager 90-160, 263-275, 702-714; StructureMappingInfo 70-100, 360-420; GoSlice 335-360; FieldMappingInfo 230-305 plus usages 151-183; ReflectionHelper 310-335, 352-395; GolangSymbolAnalyzer 118-186; and the type classes cited above.
- **C5** — exit 0,0. Verbatim:
```
git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log | python3 -I -B -c "
import sys,re
L=sys.stdin.read().splitlines()
fr=[(i+1,re.search(r'at \S+\.(\w+\.[\w\$]+)\((\w+\.java:\d+)\)',L[i])) for i in range(97,154)]
fr=[(n,m.group(1),m.group(2)) for n,m in fr if m]
fr=fr[::-1]
lv=[];cur=None
for k,(n,meth,loc) in enumerate(fr):
    if loc=='MarkupSession.java:127':
        prev=fr[k-1]; pp=fr[k-2] if k>=2 else None
        how={'GoTypeManager.java:153':'top-level (markupGoTypes loop)','StructureMappingInfo.java:398':'class @Markup getter result','MarkupSession.java:105':'Collection element'}.get(prev[2],prev[2])
        if prev[2]=='MarkupSession.java:105':
            how+=' of '+{'StructureMappingInfo.java:398':'a getter-returned List','GoSlice.java:356':'GoSlice.markupArrayElements'}.get(pp[2],pp[2])
        cur={'line':n,'entered':how,'exit':None}; lv.append(cur)
    elif cur is not None and loc in ('MarkupSession.java:339','MarkupSession.java:349','MarkupSession.java:327') and cur['exit'] is None:
        cur['exit']={'MarkupSession.java:339':'field @MarkupReference getter (markupFields:339)','MarkupSession.java:349':'class @Markup getter (markupFields:349)','MarkupSession.java:327':'additionalMarkup (markupStructure:327)'}[loc]
    elif cur is not None and cur['exit'] and 'additionalMarkup' in cur['exit'] and 'additionalMarkup' in meth:
        cur['exit']+=' -> '+meth+':'+loc.split(':')[1]
for j,v in enumerate(lv): print('L%-2d log:%d  entered=%-55s exit=%s'%(j,v['line'],v['entered'],v['exit']))
print('levels',len(lv))
"
```
  → `levels 12`; per-level lines as in the table (L0 log:153 … L11 log:104 `field @MarkupReference getter`).
- **C6** — exit 0: a python zipfile census of every line equal to `@Markup` under `ghidra/app/util/bin/format/golang/` → `total @Markup sites 29`. The only List returns are `GoFuncType.java:106->107` and `GoModuledata.java:360->361`.
- **C7** — exit 0,0: `git show R:KE | awk 'NR>=99 && NR<=108'` → the INFERENCE text at :101-106. With `NR>=110 && NR<=121` → :117-119. `git show R:…/SwissMisreadTool.md | awk '…99-102, 120-122'` → the reconcile text.
- **C8** — exit 0: `python3 -I -B -c "import struct; d=open('/usr/bin/aether','rb').read(); …"`. It parses ELF PT_LOADs, sets T=`0x954020`, and walks P11 `0x9857c0` → elem → fields[15] → imethod[0] → param[0] → imethod[0] → param[0]. Then it decodes SlotSize/uncommon at +88 and +112, N0 and the target LEB, and prints the three 40-slot maps. Output (abridged, values verbatim):
  - `maxOffset 0x17ffd9f`
  - `0x9857c0 kind=22 tflag=0x08 '*options.App'`
  - `0xa515c0 kind=25 'options.App'`, fields len=42, field[15]=`'AssetsHandler'`
  - `0x9cba40 'http.Handler'`, [0]=`'ServeHTTP'`
  - `0x9a98c0 'func(http.ResponseWriter, *http.Request)'`
  - `0x9daf00 'http.ResponseWriter'`, [0]=`'Header'`
  - `0x99d420 'func() http.Header'`
  - `0xa350a0 kind=21 tflag=0x07 'http.Header'`, GroupSize=328, SlotSize=40, ElemOff=16
  - Ghidra uncommon@+88: PkgPath=0x28 Mcount=0 Moff=16; true uncommon@+112: `'net/http'` Mcount=13 Xcount=8
  - `N0 … 0x954048 bytes=6e 00 01 61 00 01 78 00 01 79 flags=0x6e … pkgPath=0x780100`
  - `target … 0x10d4120 flags=0xf6 -> A=17645861 B=111938854 ; B-1 > maxOffset-A: True`
  - `P11 0x9857c0 < … 0xa1c7a0: True`
  - the three maps `0xa1c7a0/0xa229a0/0xa350a0`, each SlotSize=40, misread PkgPath=0x28 → 0x954048
- **C9** — exit 0: one `python3 -I -B -c` script over `/usr/bin/aether` with the same loader. Output:
  - Scan A (starts with HAS_PKGPATH and pkgPath==0x780100) → `[('0x954048', '0x6e', 0)]`
  - Scan B (8-byte pointer 0x954048, whole file) → `[]`
  - Scan C, bytes `0x954040..57` → `00 01 64 00 01 75 00 01 6e 00 01 61 00 01 78 …`, giving records at 0x954046/49/4c/4f/52/55
  - `http.Header PtrToThis=0xda4c0 -> 0xa2e4e0 kind=22`; `*http.Header uncommon mcount=13 xcount=8`; methods 10–12 `mtyp=-1`
  - `options.App uncommon mcount=0`; F1/F2 PtrToThis=0x0
  - Scan D (a separate run, exit 0): `GoName parses with HAS_PKGPATH and pkgPath==0x28: 72`; `targets of any 8-byte pointer: {}`
- **C10** — exit 0: python decode of `*http.Header` methods. Output: `Add func(string, string)`, `Clone func() http.Header` (`0x99d420`), `Del`, `Get`, `Set`, `Values func(string) []string`, `Write func(io.Writer) error`, `WriteSubset func(io.Writer, map[string]bool) error`, `get`, `has func(string) bool`, and `sortedKeyValues`/`write`/`writeSubset mtyp=-1`. Both `http.Handler` and `http.ResponseWriter` have uncommon mcount=0. Go source lines came from the session grep tool on `/home/vgpnk/.local/opt/go-1.25.0/src/net/http/{header.go,httptrace/trace.go}` → header.go:89,167,190 and trace.go:115.
- **C11** — exit 0,0:
  - Command: `python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier /usr/bin/aether --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang | python3 -I -B -c "…compare with git show R:…/swiss-misread/calib-aether.json…"`.
  - Result: `whole-json identical True`.
  - `walk.h1.path ['type@0x9857c0', 'elem', 'struct.field[15].typ', 'interface.imethod[0].typ', 'func.param[0]', 'interface.imethod[0].typ', 'func.param[0]'] type 0x9857c0 eof [17645861, 111938854]`.
- **C12** — exit 0: `python3 -I -B -c "…for each of 15 labels: map-only eof/invalid from per_type[].h1 vs prediction.extra_expectations…"` → `frozen==map-only True` ×15.
  - walk.h1 for aether: past_eof, the same pair.
  - For s1246-swiss-nethttp: invalid_index 22386945, the same.
  - For notesmd-cli and kimi: `unmapped 8`, not merged.
  - Other labels: none.
- **C13** — exit 0,0 ×3: the segmentation loop over `calib-aether`, `s1246-swiss-nethttp` and `real-kimi-webbridge` logs at R → `levels 12 / 4 / 24`. The last three are `[('elem(List)','getter'),('getter','getter'),('getter','fieldref')]` for aether and kimi, and `[('getter','getter'),('getter','getter'),('getter','fieldref')]` for s1246.
- **C14** — exit 0,0 / 0 / 0:
  - `git show R:corpus/lessons/round-18.md | awk 'NR>=14 && NR<=26'` → :22 row.
  - `git grep -n -E 'map path|struct/interface|more than the map|second.*route|two routes|not the map-specific' R -- corpus SKILL.md .ufo/waves/round-18/*.md` → relevant hits only KE:101,102,106 and lessons:22. The other hits (SOURCES.md:11, `2026-10-13-r5-01-riscv-bypass.md:78`, lessons:64) are unrelated text that matched `second.*route`.
  - `git show R:…/w1/RevAetherReplay.md | grep -nE '^## |…|second route|…'` → headings :14, :181; `INFER (high)` :223; no `second route` line.
- **C15** — exit 1: `git show R:LOG | grep -cE 'GoMapType|GoUncommonType'` → `0` (exit 1 = no match).
- w1 lineage — exit 0 except where stated: `for f in RevGhidraMapTypeRead RevAetherReplay SwissMisreadTool CriticC3 ConnC3Prediction RevNotesmdMaps; do git show R:…/w1/$f.md | grep -nE 'GoStructType|…|two interface'; done` → relevant hits RevGhidraMapTypeRead.md:316-317, RevAetherReplay.md:34,183-184,202,216 and SwissMisreadTool.md:99-102,120-122. The other hits are unrelated uses of "walk". ConnC3Prediction and RevNotesmdMaps returned no match (exit 1).
- **C16** — exit 1 / 0 / 0:
  - `git show R:LOG | grep -c 'markupNestedStructure'` → `0` (exit 1).
  - `git show R:LOG | grep -c 'Go analysis failure'` → `1`.
  - `git show R:LOG | grep -n 'FieldMappingInfo'` → l.100, l.101 only.

No tools were installed or updated.

Report: .ufo/waves/round-18/w2/AetherDualPath.md
