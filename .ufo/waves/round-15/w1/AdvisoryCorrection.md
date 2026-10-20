# Round 15 — AdvisoryCorrection report

Seat: `KaidokuR15.AdvisoryCorrection` (leaf; no subagent dispatch used).
Date: 2026-10-20. Lane root:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Assignment: draft named append-only correction paragraphs for the round-14
lesson, the prior Go entry's evidence pointer, and
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md`, without touching
the corpus; correct
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/ReviewGoInference.md:57-61`
by reopening virtual `getType` and snapshot lookup in S003; qualify the
pointer as flawed advisory without invalidating the admitted conclusion.

## Files changed

| Path | Change |
|---|---|
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/AdvisoryCorrection.candidate.md` | Created. Candidate A (lesson append), Candidate B (entry append), Candidate C (LOG append), anchor basis. |
| `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/AdvisoryCorrection.md` | Created. This report. |

No corpus, LOG, QUALITY, SOURCES, SKILL, SCORECARD, gate, fixture, or script
file was written by this seat. No commit, build, test, linter, formatter,
gate, smoke run, or target/provider execution occurred. No tool was installed
or updated, so there is no install record to emit.

## Behavior / deliverable

`AdvisoryCorrection.candidate.md` contains three ready-to-append passages and
one reconciliation rule:

- **Candidate A** names `Round-15 correction — virtual-dispatch advisory`
  for
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md`.
  It qualifies the Gate row
  1 pointer to `ReviewGoInference.md`, states the actual dispatch chain with
  exact S003 anchors, and states that snapshot absence is a sufficient
  source-level cause of the observed bootstrap message on this install for a
  go1.26 binary.
- **Candidate B** names `Round-15 advisory-pointer correction` for
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`.
  It qualifies only
  the `Evidence:` pointer (HEAD lines 101–106), restates the corrected chain,
  and explicitly preserves the entry's observations and the UNKNOWN historical
  cause.
- **Candidate C** appends a
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md` entry: advisory correction, no gate
  implementation change, no capability claim, no execution, pinned S003
  digest.
- All three are append-only; none rewrites `ReviewGoInference.md` bytes or any
  admitted conclusion.

## Exact retained evidence

### Pinned artifact

```text
sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip
f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804  /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip
```

Members extracted read-only to `/var/tmp/kaidoku-r15-w1-src/`; member line
numbers below are from those extractions. No member was modified.

### Mechanism chain (observed in source)

1. `DataTypeMapper.registerStructure` calls
   `getType(structNames, Structure.class)` —
   `ghidra/app/util/bin/format/golang/structmapping/DataTypeMapper.java:176`.
2. The list overload calls `getType(dtName, clazz)`
   (`DataTypeMapper.java:310-313`), so Java virtual dispatch selects the
   subclass override.
3. `GoRttiMapper` overrides it:
   `@Override public <T extends DataType> T getType(String name, Class<T> clazz)`
   at `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java:379-396`; the
   body calls `goTypes.findDataType(name)` at `:382` and has only the
   `runtime.pcHeader` artificial-structure fallback at `:383-389`. The base
   `DataTypeMapper.getType` is therefore bypassed on this path, consistent
   with `super(program, null)` at `GoRttiMapper.java:331` (no archive DTM).
4. `GoTypeManager.findDataType(String)` calls `findTypeRec`
   (`rtti/GoTypeManager.java:355-358`). `findTypeRec` (`:402-455`) handles
   leading `*`/`[]`/`[N]` and `map[...]`, then tests primitive kind; the only
   non-primitive definition source is
   `apiSnapshot.getTypeDef(typeName)` at `:449`.
5. `GoApiSnapshot.EMPTY` is constructed with `Map.of()`
   (`rtti/GoApiSnapshot.java:242`); `isInvalid()` is `arches.isEmpty()`
   (`:503-505`); `getTypeDef` iterates the retained arch `Types` maps and
   returns null when none match (`:524-531`). `GoApiSnapshot.get` returns
   `EMPTY` when the base JSON is absent (`:115-126`).
6. `runtime.moduledata` is not primitive (`rtti/types/GoKind.java:58-61`,
   `parseTypename` at `:76-83` returns `invalid`) and is not matched by
   `splitTypeName` (`GoTypeManager.java:598-604`, which requires a leading
   `*`, `[]`, or `[N]`). It is mapped to `GoModuledata` (`GoModuledata.java:37-38`),
   which implements `StructureMarkup`, not `StructureReader`. It is first in
   `GOLANG_STRUCTMAPPED_CLASSES` (`GoRttiMapper.java:294-300`).
7. Therefore, on an EMPTY snapshot, the first registration lookup returns
   null and `registerStructure` throws
   `Missing struct definition for class ...` (`DataTypeMapper.java:179-181`).
   `initStructMappings` catches that IOException and, because
   `apiSnapshot.isInvalid()`, throws the observed
   `Missing Go bootstrap type info, unable to extract Go RTTI info.`
   (`GoRttiMapper.java:355-360`).

Consequence: for this install and a go1.26 binary, snapshot absence is a
sufficient cause of the message, not merely a selector of its wording. This
directly contradicts `ReviewGoInference.md:57` (“`registerStructures` does not
consult the snapshot … The snapshot only decides which message is thrown”),
`:58` (“changes the log text, not the analyzer outcome”), and the `:61`
support statement; `:59` (“struct data-type source was not traced”) is now
traced.

### Installed-data inventory used only for the missing-snapshot premise

```text
find /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC -name 'go1.26*' | wc -l
0
sha256sum .../Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json
54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252
```

Base snapshots present: `go1.15.0.json` through `go1.25.0.json` (11 files).
`go1.25.0.json` `all.Types` has 3741 entries and includes both
`runtime.moduledata` and `runtime.pcHeader`. That establishes the lookup key
in the schema; it does not establish that a 1.26 snapshot is present or that
adding one repairs the install. (The broader C1 pinned inventory belongs to
the C1 seats; this report uses the two facts above only for the C2 mechanism.)

### Working-tree observations at draft time

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD
9719dd232687f5ee78a4ed323b37f8810e833d10
git status --porcelain
 M corpus/QUALITY.md
 M corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md
 M corpus/lessons/round-14.md
 M corpus/SOURCES.md
?? .ufo/waves/round-15/
```

The uncommitted corpus edits are not this seat's. At draft time
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md`
and
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`
already contained uncommitted `Round-15 correction — virtual-dispatch
advisory` sections (mtime 03:55:10), and
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md` already had
a #17 row. `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md` was
unmodified. Candidate A/B are alternatives to those uncommitted sections, not
additions to them; L1 must select one text per file. Candidate C is absent
from the tree and can be appended as-is (subject to L1's merge with other
round-15 LOG duties).
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` gained 5/2
lines between my first and final status reads; I did not edit it.

## Calibration and limits

- This is source-control-flow reasoning over installed S003, not a Ghidra run
  and not a historical replay. The `runtime.moduledata`-first failure is
  deterministic in the read code for an EMPTY snapshot, but no analyzer log
  was produced or observed.
- The historical `op` 2.40.0 run's precise cause remains UNKNOWN because its
  transient log was not retained. Candidate A/B say this explicitly.
- The range check remains advisory (`GoRttiMapper.java:170-176` from the prior
  round, unchanged here). Nothing in the correction makes the range a stop.
- Snapshot absence is sufficient for the observed message on this install; it
  is not shown necessary (other registration failures select the different
  `Invalid Go bootstrap struct mapping info` message), and snapshot presence
  is not claimed sufficient for successful 1.26 analysis. S004's bundle
  (range, JSON, moduledata route, pcHeader/map/type-flag changes) remains the
  support-change reference, not an installed capability.
- Snapshot discovery scope beyond `Application.getModuleDataFile` was not
  re-enumerated this round; the `find` count 0 covers the install and the
  prior round covered `~/.ghidra`. If another module-data root supplied a
  1.26 JSON, the EMPTY premise would not hold; that is not observed here.
- No provider execution, target execution, installation, or configuration
  change occurred. No claim about Go symbol recovery is added.

## Proposed L1 checks (not executed by this seat)

Command arguments below are repo-relative to the `git -C
/home/vgpnk/Projects/shokunin/kaidoku-shokunin` root; the target files
themselves are named absolutely above and in the candidate.

1. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --numstat --
   corpus/lessons/round-14.md corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md LOG.md`
   — expect insertions only (no deletion column > 0) once the chosen text is
   applied; `LOG.md` is new append-only text.
2. `git -C … diff -- corpus/lessons/round-14.md corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`
   — confirm no context/existing line is removed, and that only one of
   {existing uncommitted section, Candidate A/B} is present per file.
3. Reopen the anchors:
   `unzip -p <S003> ghidra/app/util/bin/format/golang/structmapping/DataTypeMapper.java | nl -ba | sed -n '172,181p;310,320p'`
   and the same for `GoRttiMapper.java` (`294-300,331,353-360,379-396`),
   `GoTypeManager.java` (`355-358,402-455,598-604`), `GoApiSnapshot.java`
   (`242,503-505,524-531`), `GoKind.java` (`58-61,76-83`), `GoModuledata.java`
   (`37-38`). Compare to the anchor table.
4. `sha256sum <S003>` and `find /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC -name 'go1.26*' | wc -l`
   — expect the pinned digest and count 0.
5. C2 no-gate-change check:
   `git -C … status --porcelain .ufo/waves/round-14/tools/quote-fidelity.py .ufo/waves/round-14/fixtures`
   — expect empty; the QUALITY #17 row is the separate criterion duty, not a
   gate-code change.
6. Confirm `ReviewGoInference.md` bytes are unchanged:
   `git -C … status --porcelain .ufo/waves/round-14/w1/ReviewGoInference.md`
   — expect empty.

## Risks and blockers

- Duplicate-correction risk: applying Candidate A/B while keeping the existing
  uncommitted sections would create two named corrections in each file. L1
  must choose one. This is the only integration ambiguity.
- Over-promotion risk: the sufficient-cause finding must not be cited as
  proof of the historical run's cause or as a repair recipe. The candidate
  text states both limits, but downstream summaries could still strip them.
- Anchor drift: candidates pin S003 by digest and member line; a future
  Ghidra update invalidates the line anchors and requires a re-derivation.
- LOG merge risk: other round-15 duties (C1 inventory, QUALITY #17) may append
  their own LOG entry; L1 owns ordering and deduplication.
- No blockers. All required evidence was reachable read-only.
