# Round 15 — AdvisoryCorrection candidate (append-only paragraphs)

Seat: `KaidokuR15.AdvisoryCorrection`. Drafted 2026-10-20. No corpus, LOG,
QUALITY, gate, fixture, or script file was edited by this seat; this file is
the only artifact written besides the sibling report
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/AdvisoryCorrection.md`.

Purpose: supply the C2 advisory duty text for three append-only targets.
Evidence is read-only S003 source inspection; nothing was executed. Baseline
`git rev-parse HEAD` at draft time:
`9719dd232687f5ee78a4ed323b37f8810e833d10`.

Targets (append only; never rewrite or delete existing bytes):

1. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md`
   — append after HEAD line 142 / current EOF.
2. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`
   — append after HEAD line 106 / current EOF.
3. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md`
   — append after line 1831 / current EOF.

Reconciliation note: at draft time the working tree already contained
uncommitted `Round-15 correction — virtual-dispatch advisory` sections in
targets 1 and 2 (mtimes 2026-10-20 03:55:10, not written by this seat), and an
uncommitted `QUALITY.md` #17 row. LOG had no round-15 change. L1 must choose
one text per target: either keep the existing uncommitted section or replace
it with the candidate below before committing. Do not append both; the two
texts are alternatives, not additive corrections.

---

## BEGIN Candidate A — lesson round-14 append

## Round-15 correction — virtual-dispatch advisory

The Gate's first candidate row cites
`.ufo/waves/round-14/w1/ReviewGoInference.md` as preserving conditional
control flow. That pointer is retained only as a flawed advisory, not as
mechanism support. Its lines 57–61 (under the `:52` heading) — especially
“`registerStructures` does
not consult the snapshot” and “snapshot absence changes the log text, not the
analyzer outcome” — ignore the virtual dispatch from
`DataTypeMapper.registerStructure` (`:176`) through `getType(List, Class)`
(`:310-320`) to `GoRttiMapper`'s `@Override getType(String, Class)`
(`GoRttiMapper.java:379-396`). That override calls
`GoTypeManager.findDataType` (`:355-358`), whose `findTypeRec` (`:402-455`)
resolves a non-primitive name only through `apiSnapshot.getTypeDef` (`:449`);
`GoApiSnapshot.EMPTY` carries no arch maps (`GoApiSnapshot.java:242`) and its
`getTypeDef` returns null (`:524-531`). `runtime.moduledata` is non-primitive
(`GoKind.java:58-61,76-83`) and is not a splice, pointer, or sized-array name
(`GoTypeManager.java:598-604`), so with no installed `go1.26*` snapshot the
first mapped class `GoModuledata` (`GoRttiMapper.java:294-295`;
`GoModuledata.java:37-38`), which is not a `StructureReader`, fails at
`DataTypeMapper.java:179-181` and reaches the `initStructMappings` handler
(`GoRttiMapper.java:355-360`) that emits the observed bootstrap message.
For this installation and a go1.26 binary, snapshot absence is therefore a
sufficient source-level cause of that failure, not merely a selector of its
wording.

This correction does not invalidate the admitted round-14 conclusion. The
installed range check remains advisory and is still not the stop; the
historical `op` run's precise cause remains UNKNOWN because its log was not
retained; and a snapshot-only or range-only edit is still not established as
a repair, because S004's support change remains a bundle. The advisory
artifact stays appended evidence with its filed bytes intact; neither it nor
this paragraph claims target, provider, or compiled-provider execution.

## END Candidate A

---

## BEGIN Candidate B — prior Go entry append

## Round-15 advisory-pointer correction

The `ReviewGoInference.md` pointer in the Evidence paragraph above is retained
as an author-side review record only; its lines 57–61 (under the `:52`
heading) are wrong on mechanism.
`registerStructures` does reach the snapshot, through the mapper's `getType`
override (`GoRttiMapper.java:379-396`) and `GoTypeManager.findTypeRec`
(`:402-455`, snapshot lookup at `:449`). On this install a go1.26 binary gets
`GoApiSnapshot.EMPTY` (no `go1.26.0.json`; `GoApiSnapshot.java:242,503-505`),
so the first mapped class's `runtime.moduledata` structure cannot resolve and
`registerStructure` throws (`DataTypeMapper.java:179-181`), which is the
`IOException` path that produces the observed bootstrap message
(`GoRttiMapper.java:355-360`). Snapshot absence is therefore a possible cause
of that failure, not merely a selector of its wording.

This paragraph qualifies the pointer only. The observations and conclusion
above stand: the `1.15-1.25` range check is advisory and not a stop, the
historical `op` run's precise cause is UNKNOWN without its retained log, and
a snapshot or range edit alone is not established as a repair. S003 was
reopened read-only on 2026-10-20; outside finding:
`corpus/lessons/round-14-verifier-spotcheck.md`, routed defect 1. No
execution was performed for this correction.

## END Candidate B

---

## BEGIN Candidate C — LOG append

## 2026-10-20 — round-15 — advisory correction (no gate change)

- `.ufo/waves/round-14/w1/ReviewGoInference.md` stays filed, but its lines
  57–61 are a flawed advisory: virtual `getType` dispatch
  (`GoRttiMapper.java:379-396`) reaches `GoTypeManager.findTypeRec`
  (`:402-455`) and the API snapshot, so snapshot absence can cause the
  bootstrap struct-registration failure, not only select its wording. The
  named correction and pointer qualification are appended to
  `corpus/lessons/round-14.md` and
  `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`; no existing
  lesson or entry byte is rewritten.
- The admitted round-14 conclusion is unchanged: the `1.15-1.25` range check
  remains advisory, the historical `op` run's cause remains UNKNOWN, and no
  Go recovery or repair capability is claimed. S003
  (`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`,
  SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`)
  was reopened read-only.
- This advisory duty changes no quote-gate implementation, fixture, or
  expected value, and performed no target/provider execution and no tool
  installation or update.

## END Candidate C

---

## Anchor basis used by all three paragraphs

All line numbers are for installed S003 archive members as extracted
read-only from the pinned zip above. Verbatim anchors:

| Member:line | Text / role |
|---|---|
| `structmapping/DataTypeMapper.java:176` | `Structure structDT = getType(structNames, Structure.class);` |
| `structmapping/DataTypeMapper.java:179-181` | throws `Missing struct definition for class %s, structure name: [%s]` when the class is not a `StructureReader` |
| `structmapping/DataTypeMapper.java:310-313` | list overload calls `getType(dtName, clazz)` — virtual dispatch point |
| `rtti/GoRttiMapper.java:294-295` | `GOLANG_STRUCTMAPPED_CLASSES = List.of(GoModuledata.class, ...)` |
| `rtti/GoRttiMapper.java:331` | `super(program, null);` — no archive DTM |
| `rtti/GoRttiMapper.java:353` | `registerStructures(GOLANG_STRUCTMAPPED_CLASSES, this);` |
| `rtti/GoRttiMapper.java:355-360` | `catch (IOException e)` → `apiSnapshot.isInvalid()` → `BootstrapInfoException("Missing Go bootstrap type info, ...")` |
| `rtti/GoRttiMapper.java:379-396` | `@Override getType(String, Class)` → `goTypes.findDataType(name)`; `pcHeader` fallback only |
| `rtti/GoModuledata.java:37-38` | `@StructureMapping(structureName = "runtime.moduledata")`; not a `StructureReader` |
| `rtti/GoTypeManager.java:355-358` | `findDataType(String)` → `findTypeRec` |
| `rtti/GoTypeManager.java:402-455` | `findTypeRec`; non-primitive branch at `:443-451` |
| `rtti/GoTypeManager.java:449` | `apiSnapshot.getTypeDef(typeName)` — the only non-primitive definition source |
| `rtti/GoTypeManager.java:598-604` | `splitTypeName` matches only leading `*`, `[]`, `[N]` |
| `rtti/types/GoKind.java:58-61` | primitive kind set |
| `rtti/types/GoKind.java:76-83` | `parseTypename` returns `invalid` for unrecognized names |
| `rtti/GoApiSnapshot.java:242` | `EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of())` |
| `rtti/GoApiSnapshot.java:503-505` | `isInvalid()` == `arches.isEmpty()` |
| `rtti/GoApiSnapshot.java:524-531` | `getTypeDef` iterates retained arch `Types` maps, returns null when empty |

Installed-data inventory facts (read-only): the 12.1.4 install contains base
JSON `go1.15.0` … `go1.25.0` only; `find … -name 'go1.26*'` returns count 0.
`go1.25.0.json` SHA-256 is
`54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`;
its `all.Types` map has 3741 entries and contains both `runtime.moduledata`
and `runtime.pcHeader`. That shows the lookup key exists in the snapshot
schema, not that a 1.26 snapshot is present or sufficient.
