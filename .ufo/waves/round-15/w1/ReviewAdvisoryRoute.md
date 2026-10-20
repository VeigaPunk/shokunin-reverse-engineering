# Round 15 — W1 ReviewAdvisoryRoute: outside routed defect 1 (advisory evidence correction)

Lane: leaf reviewer, no subagent dispatch. Access date for every source: 2026-10-20.
Scope: read-only review of `corpus/lessons/round-14-verifier-spotcheck.md` routed defect 1 (`:171`), the cited artifact `.ufo/waves/round-14/w1/ReviewGoInference.md:52-61`, the S003 archive members, and every active lesson/entry pointer to that artifact (bounded grep). No builds, tests, gates, REA/Ghidra runs, target execution, or edits to corpus, LOG, SCORECARD, or SKILL.

Tools: none installed or updated. Read-only inventory only: `sha256sum`, `unzip -p`, `nl -ba`, `sed -n` on the pinned archive.

## Verdict

1. **Defect 1 is real and the routed description is accurate.** `.ufo/waves/round-14/w1/ReviewGoInference.md:57` says "`registerStructures` does not consult the snapshot. It looks up struct data types in the program and built-in data type managers", and `:58` / `:61` say snapshot absence "changes the log text, not the analyzer outcome". The S003 source contradicts the first claim: the mapper overrides `getType`, and that override reaches `apiSnapshot`. (OBSERVATION, verified below.)
2. **Defect 1 is not fully closed by the existing corrections.** The round-15 correction in `corpus/lessons/round-14.md:144-159` names only `ReviewGoInference.md` lines 57-61 and the Gate and causal-overreach rows. The same wrong mechanism recurs at `ReviewGoInference.md:110` (H2 "selects wording only") and `:122` (forbidden-conclusion rationale). `:136` ("struct data-type source: not traced") is now source-traced. Those lines must be enumerated, or a reader can carry H2 forward.
3. **The admitted knowledge entry does not carry the wrong mechanism.** Its observation at `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:55-58` already states the override-to-`findTypeRec` path. Its correction block at `:108-117` is adequate. Its Evidence pointer at `:103` is qualified only one paragraph later, which is acceptable.
4. **Calibration of the outcome claim.** `ReviewGoInference.md:58` is correct only as a comparison of the two catch branches (both return null). It is wrong as a statement that the snapshot is irrelevant to the outcome. Under the source path below, snapshot absence is sufficient for the constructor-site abort (INFERENCE from control flow, not executed). This does not establish the historical r4-10 run's cause, whose log was not retained. C1 survives, as the routed text says.

## Verified source anchors (S003)

Archive: `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`
`sha256sum` = `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (matches `corpus/SOURCES.md` S003 and the entry's digest table). Member paths are under `ghidra/app/util/bin/format/golang/` and `.../structmapping/`.

| Anchor | Observed content (verified by `nl -ba` on the archive) |
|---|---|
| `rtti/GoRttiMapper.java:79` | `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")` |
| `rtti/GoRttiMapper.java:102-129` | `getSharedGoBinary`: `catch (BootstrapInfoException)` at `:114-117`, `catch (IOException)` at `:118-123`, `return null` at `:125` |
| `rtti/GoRttiMapper.java:330-331` | constructor; `super(program, null)` at `:331` |
| `rtti/GoRttiMapper.java:351-367` | `initStructMappings`: `registerStructures` at `:353`; IOException branch: `BootstrapInfoException` at `:358-360` if `apiSnapshot.isInvalid()`, else `IOException` at `:364-365` |
| `rtti/GoRttiMapper.java:379-390` | `@Override getType` at `:379-380`; `goTypes.findDataType(name)` at `:382`; catch IOException returns null |
| `rtti/GoRttiMapper.java:294-300` | `GOLANG_STRUCTMAPPED_CLASSES` begins with `GoModuledata.class` |
| `rtti/GoModuledata.java:37-38` | `@StructureMapping(structureName = "runtime.moduledata")`; `implements StructureMarkup<GoModuledata>` (not `StructureReader`) |
| `structmapping/DataTypeMapper.java:172-186` | `registerStructure`: `getType(structNames, Structure.class)` at `:176`; throw IOException "Missing struct definition" at `:179-181` for non-`StructureReader` classes |
| `structmapping/DataTypeMapper.java:282-295` | base `getType` (program DTM, archive GDT, built-in DTM). **Shadowed** by `GoRttiMapper.getType` at `:380` for the mapper. ReviewGoInference cites this as the lookup path; it is not |
| `rtti/GoTypeManager.java:60-130` (constructor region) | constructor sets `goBinary`, `apiSnapshot`, `dtm`, `ptrSize`, `voidPtrDT`; does **not** populate `typeNameIndex` (`:~112`); `init()` is separate |
| `rtti/GoTypeManager.java:402-455` | `findTypeRec`: `typeNameIndex.get` at `:404`; `splitTypeName` prefixes only; primitive at `:446-447`; **`apiSnapshot.getTypeDef(typeName)` at `:449`** |
| `rtti/GoTypeManager.java:598-604` | `splitTypeName` returns null unless the name matches the prefix regex (`[]`, `*`, `[N]`) |
| `rtti/GoApiSnapshot.java:102-116` | `get`: returns `GoApiSnapshot.EMPTY` at `:115` when no base JSON |
| `rtti/GoApiSnapshot.java:242` | `EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of())` |
| `rtti/GoApiSnapshot.java:503-505` | `isInvalid()` = `arches.isEmpty()` |
| `rtti/GoApiSnapshot.java:524-531` | `getTypeDef` iterates `arches.values()`; returns null when empty |

Not re-opened in this pass: `GolangSymbolAnalyzer.java:133-137`, `GoApiSnapshot.java:122-126` and `:148-166`, `S004`, `S007`, `S001`. The entry cites them; they are not on defect 1's path.

## Mechanism that the defect misses (source control flow, INFERENCE, not executed)

For a binary whose major.minor base snapshot is absent (`get` returns EMPTY), or whose snapshot has no records for the binary's GOOS/GOARCH (`isInvalid()` true):

1. `GoTypeManager` has an empty `typeNameIndex` at construction (`GoTypeManager.java:60-130`), and `init()` is not yet called (`GoRttiMapper.java:330-349` → `initStructMappings` at `:349`).
2. `registerStructure(GoModuledata.class)` calls `getType("runtime.moduledata")` (`DataTypeMapper.java:176`). The mapper override (`GoRttiMapper.java:380-382`) calls `GoTypeManager.findDataType` → `findTypeRec`. The name is non-primitive and does not match the prefix regex, so the only remaining source is `apiSnapshot.getTypeDef` (`GoTypeManager.java:449`). On EMPTY, `arches` is empty, so `getTypeDef` returns null (`GoApiSnapshot.java:524-531`).
3. `getType` returns null. `GoModuledata` is not a `StructureReader`, so `DataTypeMapper.java:179-181` throws IOException.
4. `initStructMappings` sees `isInvalid()` and throws `BootstrapInfoException` (`GoRttiMapper.java:356-360`).
5. `getSharedGoBinary` catches it, logs, and returns null (`:114-125`). The Go analyzers then receive a null mapper (entry cites `GolangSymbolAnalyzer.java:133-137`).

Consequences:
- The invalid-snapshot route is **sufficient** under this source path, independent of binary layout, for any binary whose version selects a missing or arch-less snapshot. This is stronger than the artifact's "wording only" and is what the artifact's H2 row and forbidden-conclusion reason deny.
- It does **not** establish the historical r4-10 cause. The log was not retained, and the analyzer abort does not by itself account for the full 33,060 to 11,595 difference. The entry's "precise cause UNKNOWN" remains correct.
- The IOException branch with a valid snapshot (`:364-365`) also returns null (`:118-125`). So the two catch branches differ only in message, which is the sense in which `ReviewGoInference.md:58` is right.

## Active flawed pointers (bounded grep)

Grep scope: `corpus/`, `LOG.md`, `SKILL.md`, `SCORECARD.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`. Patterns: `ReviewGoInference`, `registerStructures`, `apiSnapshot`, `snapshot absence|only selects|does not consult|changes the log text|preserve conditional control flow`, `isInvalid|BootstrapInfoException|Missing Go bootstrap`, `round-15|Round-15|virtual-dispatch`.

| # | File:line (tag at review) | Current text | Status | Required action |
|---|---|---|---|---|
| P1 | `corpus/lessons/round-14.md:18` (#A9E3) | Gate row: "`ReviewGoInference.md` and `SnapshotBootstrap.md` preserve conditional control flow" | **Active flawed pointer.** `ReviewGoInference.md` is cited as a whole; lines 57-61 contradict the source. Qualified only by a section at `:144-159`, not by this row | Narrow the citation (exact text below) |
| P2 | `corpus/lessons/round-14.md:76` (#A9E3) | Mistakes row "causal-overreach ... `ReviewGoInference.md`" | **Active flawed pointer.** Same artifact, same whole-file citation. Qualified only by the section | Row-local qualifier (exact text below) |
| P3 | `corpus/lessons/round-14.md:144-159` (correction, #A9E3) | "its lines 57–61 are flawed advisory evidence" | **Incomplete correction.** Omits `ReviewGoInference.md:110`, `:122`, `:136`, and the `:57` anchor `DataTypeMapper.java:282-295`, which is the shadowed base | Expand the enumerated list (exact text below) |
| P4 | `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:103` (#C554) | Evidence list includes `ReviewGoInference.md` | Pointer retained as record; **qualified at `:108-117`**, adjacent. Acceptable | Optional inline marker. Not blocking |
| P5 | `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:110-117` (#C554) | "Its lines 57–61 incorrectly treat snapshot validity as affecting only error wording..." | Accurate but narrow; same omission as P3 | Extend to `:110`, `:122`, `:136` |
| P6 | `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:55-58` (#C554) | "getType override delegates to `GoTypeManager.findDataType`; `findTypeRec` at `:405-455`" | Accurate; **anchor gap**: override line not given, `apiSnapshot.getTypeDef` line not given | Add `GoRttiMapper.java:380-382` and `GoTypeManager.java:449` |
| P7 | `corpus/lessons/round-14-verifier-spotcheck.md:171` (#ADE5) | Routed defect 1 text | Accurate record. Append-only; do not edit | None |
| P8 | `corpus/lessons/round-14.md:146-150` (#A9E3) | "Contrary to that report, `registerStructures` reaches the mapper's overridden `getType` (`GoRttiMapper.java:380-386`)" | Accurate. Anchor range `380-386` is valid (override at `:380`, delegation `:382`) | Optional: use `380-382` |

Other grep hits, checked and clean:
- `SKILL.md:463-464` — "Failed struct registration with an invalid snapshot is not version-only or layout proof". Consistent with the source path above. No change.
- `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:71-73` — the superseded causal sentence. Not a `ReviewGoInference` pointer; it is the already-corrected historical entry (append-only). Out of this defect's scope.
- `.ufo/waves/round-14/w1/SnapshotBootstrap.md:47-54` — states the chain through `getType` correctly. Preferred mechanism pointer. Do not edit.
- `.ufo/waves/round-14/w1/AttackNovelty.md:42-46` — CE3/CE4 correct and conditional. Preferred pointer for `isInvalid()` detail.

Out of scope, archival, not lesson/entry (do not edit in this round; record only):
- `/home/vgpnk/Projects/shokunin/.ufo/reports/round-14/kaidoku.md:8` cites `w1/ReviewGoInference.md` as evidence for the admitted diagnostic. Fleet report, append-only.
- `.ufo/waves/round-14/w1/ReviewGoInference.md` itself. Preserve filed bytes (per routed text).

Missing artifacts (dangling or absent):
- `LOG.md` has no round-15 entry and no `Round-15 correction — virtual-dispatch advisory` (bounded grep `round-15|Round 15|Round-15|R15|r15|virtual-dispatch|ReviewGoInference`: no matches). The routed text requires "a named correction to the lesson/LOG". The lesson-side correction exists; the LOG side does not.
- `corpus/lessons/round-15.md` does not exist (glob `corpus/lessons/round-15*`: no match). It is cited by `corpus/lessons/round-14.md:158` and by `corpus/QUALITY.md:27` ("`corpus/lessons/round-15.md`, Mistakes and Gate"). Until L1 creates it, both pointers dangle.

## Obligations to close defect 1

O1. **LOG named correction.** Append to `LOG.md` a round-15 entry containing the heading `Round-15 correction — virtual-dispatch advisory`, matching the heading style of the existing round entries (not inspected in this pass; L1 matches). Body: artifact `.ufo/waves/round-14/w1/ReviewGoInference.md` lines 57–61, 110, 122 flagged; S003 anchors from the table above; no historical replay; artifact bytes preserved.

O2. **Narrow P1 (`corpus/lessons/round-14.md:18`).** Replace the Evidence cell's citation with:
> `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`; S001/S003/S004/S007 reopened; mechanism per `SnapshotBootstrap.md` §2 lines 40–56; conditional control flow and deleted-log limitation per `ReviewGoInference.md` lines 7, 46–50, 54–55 and Gaps (lines 132–140). `ReviewGoInference.md` lines 57–61, 110 and 122 are superseded: see `## Round-15 correction — virtual-dispatch advisory`.

O3. **Qualify P2 (`corpus/lessons/round-14.md:76`).** Append to the Evidence cell: `Findings 5 and Gaps only; lines 57–61, 110, 122 superseded (see Round-15 correction)`.

O4. **Expand P3 (`corpus/lessons/round-14.md:144-159`).** Replace "its lines 57–61 are flawed advisory evidence" with an enumerated list:
> `ReviewGoInference.md` lines 57–61 (Finding 2: snapshot "only decides which message is thrown"; `registerStructures` "does not consult the snapshot"); line 110 (H2 "selects wording only"); line 122 (forbidden-conclusion rationale). Line 136 ("struct data-type source ... not traced") is now traced. Line 58's comparison of the two catch branches (both return null, `GoRttiMapper.java:114–125`) remains correct. The claim that the snapshot is irrelevant to the outcome does not.

O5. **Extend P5 (entry `:110-117`).** Name lines 110, 122, 136 alongside 57–61, and keep the "does not establish historical cause" sentence.

O6. **Anchor-complete P6 (entry `:55-58`).** Add the override anchor and the `getTypeDef` anchor (`GoRttiMapper.java:380-382`; `GoTypeManager.java:449`). Text-only change.

O7. **Dangling `corpus/lessons/round-15.md`.** L1 must create it (the round-15 lesson), or repoint `round-14.md:158` and `QUALITY.md:27` to the file that holds the Mistakes/Gate content. Otherwise both pointers dangle.

O8. **Optional strengthening (not required for closure; L1 decides).** The entry may state, marked INFERENCE from source control flow and not executed: "For a binary whose base snapshot is absent or arch-less, the mapper constructor's struct registration fails on the first non-`StructureReader` class (`runtime.moduledata`) independent of binary layout, and the analyzers receive a null mapper. This does not identify the historical r4-10 run's cause." Do not present it as causal for the historical loss. If added, cite `GoApiSnapshot.java:242,524-531`, `DataTypeMapper.java:176,179-181`, `GoRttiMapper.java:356-360,114-125`, `GoModuledata.java:37-38`.

O9. **Do not edit** `ReviewGoInference.md`, `SnapshotBootstrap.md`, `AttackNovelty.md`, `SKILL.md`, `SCORECARD.md`, `SOURCES.md`, or `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` for this defect. Preserve filed evidence; no new SOURCES row.

## Proposed L1 checks (named, not executed by this seat)

- `sha256sum` the S003 archive and compare to `f00d29c2…d804`.
- `unzip -p <S003> <member> | nl -ba | sed -n` at the anchors in the table above (re-derive `:79`, `:114-125`, `:176`, `:179-181`, `:356-360`, `:380-382`, `:449`, `:115`, `:242`, `:524-531`).
- `grep -n "Round-15 correction — virtual-dispatch advisory" LOG.md corpus/lessons/round-14.md` (expect one hit each after O1/O4).
- `test -f corpus/lessons/round-15.md` (O7).
- Re-read `corpus/lessons/round-14.md:18` and `:76` after O2/O3 to confirm the citation is narrowed and the qualifier is row-local.
- Confirm no edit to `.ufo/waves/round-14/w1/ReviewGoInference.md` (`git -C kaidoku-shokunin diff --stat -- .ufo/waves/round-14`).
- Run the lane's registered gate/selftest once, as the round's L1 verification. This seat did not run it.

## Limits

- All claims in this file are source reading of the pinned S003 archive; nothing was executed (no Ghidra, no REA, no provider, no target).
- The EMPTY-snapshot determinism in the mechanism section is an INFERENCE from control flow. It was not observed. It is contingent on `GOLANG_STRUCTMAPPED_CLASSES` beginning with a non-`StructureReader` class, which I verified for the first element only.
- `GolangSymbolAnalyzer.java:133-137`, `GoApiSnapshot.java:122-126`, and `S004`/`S007` were not re-opened here.
- The historical r4-10 log is gone. Nothing here identifies that run's cause.
- Line numbers are from `nl -ba` on the pinned archive; the entry's anchors use the same archive.
- Tool installs or updates: none.
