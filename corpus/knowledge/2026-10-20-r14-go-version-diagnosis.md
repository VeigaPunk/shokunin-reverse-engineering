source: S001, S003, S004, S007 in `corpus/SOURCES.md`; installed REA skill `/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md`; installed Ghidra Base source archive `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`; upstream https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174; installed `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md`.
verified-at: 2026-10-20 — source reading only; round-14 author-side review, not a fresh target execution.
recheck: `sha256sum /home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md`; compare the expected digests below, then reopen the named archive members and upstream diff at their anchors.

# Go RTTI bootstrap diagnosis: a range warning is not a parser refusal

## Question and provenance

The held cross-version task already recorded different Go-symbol recovery on
`1password-cli` packages `2.34.1-1` and `2.40.0-2` (x86_64). What it lacked
was a source-backed distinction between the declared version range, missing
bootstrap metadata, and a downstream layout failure. This entry deepens that
existing holding; it does not claim new domain coverage or recovered Go symbols.

Expected SHA-256 values from this round's `sha256sum` command:

| Source | SHA-256 |
|---|---|
| S001 installed REA skill | `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0` |
| S003 Base source archive | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` |
| S007 installed change history | `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4` |

Archive member anchors below bind to S003, not to an arbitrary checkout of
Ghidra master. `GoRttiMapper.java`, `GoApiSnapshot.java`, and
`GoTypeManager.java` are under `ghidra/app/util/bin/format/golang/rtti/`.
`GolangSymbolAnalyzer.java` is under `ghidra/app/plugin/core/analysis/`.
`DataTypeMapper.java` is under `ghidra/app/util/bin/format/golang/structmapping/`.

## Source observations and derived control flow

- **OBSERVATION — advisory range.** `GoRttiMapper.java:79` declares
  `GoVerRange.parse("1.15-1.25")`. At `:170-172`, an out-of-range version
  causes `Msg.error` with `Untested Go version [%s]`; there is no throw or
  return on that branch. Snapshot lookup follows at `:176`.
- **OBSERVATION — separate snapshot lookup.** `GoApiSnapshot.java:122-126`
  first requests the same major/minor at patch zero. A missing base file
  returns null, and `get` returns `GoApiSnapshot.EMPTY` at `:115`.
  The patch-diff search at `:148-166` does not fall back to an earlier minor.
- **OBSERVATION — bootstrap failure is conditional.** `DataTypeMapper.java:172-181`
  throws when a required mapped structure cannot be found.
  `GoRttiMapper.java:353-365` first calls `registerStructures`; only in its
  IOException handler does an invalid snapshot select the message
  `Missing Go bootstrap type info, unable to extract Go RTTI info.`
  A valid snapshot with failed mapping selects a different message.
- **INFERENCE FROM SOURCE — not a direct version stop.** The missing-bootstrap
  message identifies failed struct registration with an invalid snapshot,
  not the advisory range check. `GoRttiMapper.java:114-125` catches this
  bootstrap exception and returns null; `GolangSymbolAnalyzer.java:133-137`
  then returns false. This is source control-flow reasoning, not observed
  execution of the current provider.
- **OBSERVATION — the same message has another cause.** `GoApiSnapshot.java:205-239`
  selects OS/architecture-specific and generic records; `isInvalid()` at
  `:503-505` tests `arches.isEmpty()`. A present file without applicable
  records can therefore reach the same invalid-snapshot branch.
- **OBSERVATION — no legacy-archive shortcut on this path.** The mapper calls
  `super(program, null)` at `:331`. Its `getType` override delegates to
  `GoTypeManager.findDataType`; the latter's `findTypeRec` at `:405-455`
  obtains non-primitive definitions from `apiSnapshot`, not a legacy GDT
  archive. S007, `Ghidra 12.0 Change History` → `Improvements`, line 585,
  explicitly records the switch to JSON snapshots instead of GDT files.
- **OBSERVATION — upstream support is a bundle.** S004 changes the range to
  `1.15-1.26`, adds `go1.26.0.json`, and also changes the moduledata locator,
  pcHeader field presence, and map/type handling. It is not evidence that
  editing only the range string, or adding only a snapshot, repairs this host.
- **OBSERVATION — different REA route.** S001's `Route the target first` says
  `inspect_go_binary` is a built-in target-free metadata inspection requiring
  no Go installation or disassembler. A successful build-info read says
  nothing about Ghidra RTTI recovery. The retained Docker example is
  `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:1-8`.

## Differential decision table

| Signal available | Supported conclusion | Do not conclude | Next discriminating evidence |
|---|---|---|---|
| `Untested Go version` | Declared range exceeded; the inspected branch continues | The range check aborted recovery | Separate bootstrap diagnostic or retained analyzer log |
| Missing base JSON for the binary's major/minor | Source lookup yields EMPTY on that installation | Layout is unparseable, or another installation has the same files | Pin installed data and binary build version |
| `Missing Go bootstrap type info` | Struct registration failed with an invalid snapshot | The version alone caused it | Distinguish absent base file from OS/architecture exclusion |
| Many `FUN_*` names, or missing `main.main` in an inventory | Recovery/inventory is incomplete for the requested names | Those functions/strings do not exist in the binary | Retained analyzer diagnostics and an appropriately scoped search |
| Upstream GP-6528 exists | A concrete support-change bundle can be studied | This installed release contains it, or a repaired run has succeeded | Explicit installed/released bytes and a separately authorized carrier run |

## Correction and limits

**Supersedes the causal inference, not the historical measurements**, in
`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69-73`: that text
attributes the outcome to an unparseable Go moduledata/pclntab layout.
Its transient log was not retained. The bootstrap explanation above is a
source-supported diagnostic route, but the original run's precise cause is
**UNKNOWN**. No controlled rerun, provider execution, or target execution
was performed in round 14. Downstream layout incompatibilities are neither
proved absent nor identified as the cause of that old run.

The historical instruction to avoid name-only pairing remains useful. Match
by explicit evidence and ELF role/address with appropriate uncertainty; a
matching role/address is not itself proof of semantic equivalence.

The source companion archive was inspected, not authenticated against the
compiled provider's executing classes. No release after the named installed
version was checked, and no Go recovery capability is added. GoReSym and BSim
were opened as study routes but are not support for this bootstrap diagnosis.

Evidence: `.ufo/waves/round-14/w1/GoEntryDraft.md`,
`.ufo/waves/round-14/w1/SnapshotBootstrap.md`,
`.ufo/waves/round-14/w1/ReviewGoInference.md`, and
`.ufo/waves/round-14/w1/AttackNovelty.md`.
The original study lead is fleet `.ufo/waves/kaika-w1/kaidoku-art.md`, K1;
round-14 seats re-opened the sources rather than treating that draft as proof.
