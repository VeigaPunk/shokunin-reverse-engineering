<!-- candidate — kaidoku-shokunin round 14 (2026-10-20), claim C1 (axis: depth, per claims-review.json). Draft only: L1 owns integration, the corpus/README index row, and any append-only correction to the older entry. Staging evidence: this file and `.ufo/waves/round-14/w1/GoEntryDraft.md`. -->

# Go RTTI bootstrap failure on Ghidra 12.1.4 — the missing JSON snapshot edge class, not a version-gate refusal

source: installed REA skill v42 `/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` (SHA-256 `c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0`, Go route at `:167-169`); installed Ghidra 12.1.4 source archive `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` (SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`), members `ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java` (`2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95`), `GoApiSnapshot.java` (`765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d`), `structmapping/DataTypeMapper.java` (`53ff4eb578371102a5296015b872f6a3896af837122bbf15b0973794c12c66ff`), `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java` (`b9b70998570b18d4619de28e41e99beb17f9c04e0197d4888b0688b66054ab80`), `ghidra/app/util/bin/format/golang/GoBuildInfo.java` (`43f799b9660f6a02077e91d389d87f04b3c4dfe11e7064af3196d4966ee37101`); upstream commit `385e8cd923d09f10b1a7874108e71748875fa174` at `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174`; installed `Ghidra 12.1.4 Change History` `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` (SHA-256 `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`, `# Ghidra 12.0 Change History` `### Improvements` at lines 564/582/585); retained observation `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:29,34,64-74`; fleet K1 trace `.ufo/waves/round-14/w1/InstalledGoGate.md`.

verified-at: 2026-10-20

recheck: (1) `sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` → expect `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`. (2) `unzip -p <zip> 'ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java' | nl -ba | sed -n '79p;114,125p;170,177p;331p;354,365p'` → expect the `1.15-1.25` range, the `Untested Go version` log, the `super(program, null)` call, and the two distinct bootstrap messages. (3) `unzip -p <zip> 'ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java' | nl -ba | sed -n '115p;122,126p;148,166p;205,239p;503,505p'` → expect `return GoApiSnapshot.EMPTY;`, the base-version lookup, the same-minor patch fallback, the arch filter, and `isInvalid()` = `arches.isEmpty()`. (4) `ls …/typeinfo/golang/go*.json | wc -l` → expect `11`; `find …/typeinfo/golang -name '*1.26*' | wc -l` → expect `0`; `ls …/typeinfo/golang/patchverdiffs | wc -l` → expect `123`; `ls …/patchverdiffs | grep -c '^go1\.25'` → expect `0`; `ls …/typeinfo/golang/*.gdt | wc -l` → expect `9`. (5) `unzip -q <zip> -d <tmp> && grep -rn 'golang_' <tmp> | wc -l` → expect `0` over the full Base source extraction. (6) `sed -n '564p;582p;585p' /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` → expect the 12.0 release heading, `### Improvements`, and the JSON-instead-of-gdt line. (7) `curl -sS -H 'Accept: application/vnd.github+json' https://api.github.com/repos/NationalSecurityAgency/ghidra/commits/385e8cd923d09f10b1a7874108e71748875fa174` → expect title `GP-6528 add support for golang 1.26`, 10 files, `go1.26.0.json` added. All steps are read-only; none invokes REA, Ghidra analysis, or a target.

Scope: this entry is a **source-conditional differential diagnosis of one edge class** — a Go binary whose Ghidra symbol recovery collapses because the Go RTTI bootstrap never completes. It deepens the held cross-version Go symptom in `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md`; it does **not** claim a new domain, a target run, or a held recovery capability. Axis attribution is `depth`, not coverage (`claims-review.json`).

## New diagnostic question (round 14)

> When a Go binary's Ghidra symbol recovery is collapsed, which **source-visible** gate can be named without executing anything, and what does each observed signal actually prove?

The answer this entry defends: on stock 12.1.4 a `go1.26.x` build reaches the RTTI bootstrap with an **empty API snapshot**, and the `Missing Go bootstrap type info` message marks that bootstrap branch — **not** a version-range refusal and not, by itself, a parser-layout verdict.

## Evidence layers — keep them separate

| layer | artifact | exact anchor | what it decides |
|---|---|---|---|
| L1 build version | the binary's `.go.buildinfo` version string (`go1.26.8`, …) | `GoBuildInfo.java:44-46` names the section; `:188-201` defines the `Go version fallback` option | which snapshot filename is requested |
| L2 declared range | installed `GoRttiMapper.java:79` | `"1.15-1.25"` | only an `Untested Go version` **log line** |
| L3 snapshot resolution | `GoApiSnapshot.java` | base `major.minor`, same-minor patch diffs, `EMPTY` on a miss | whether any snapshot data exists at all |
| L4 bootstrap struct mapping | `GoRttiMapper.initStructMappings` + `DataTypeMapper.registerStructure` | throws when mapped structs are missing | whether RTTI extraction starts |
| L5 upstream fix | commit `385e8cd9…` | adds `go1.26.0.json`, bumps the range, and also changes downstream layout handling | what a future release would change; **not** a host capability |
| L6 parser layout | pcHeader/moduledata mapping | reached only after L4 succeeds | irrelevant when L4 aborts |

## Observations

### L2 — the declared range is diagnostic, not a refusal

- `OBSERVATION` — `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` at `GoRttiMapper.java:79`.
- `OBSERVATION` — out-of-range handling is one log call inside `if (!SUPPORTED_VERSIONS.contains(goVer) ) {` (`:170`): `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));` (`:171`). There is no `return` and no throw on this branch; `:176` immediately calls `GoApiSnapshot.get(goVer, buildInfo.getGOARCH(program),` / `buildInfo.getGOOS(program), monitor);`.
- `INFERENCE` — a log line `Untested Go version [1.26.x]` proves only that L1 exceeded L2. It does not stop the analyzer and does not explain a collapse. Writing "the version gate rejects Go 1.26" contradicts `:171`.

### L3 — missing JSON resolves to EMPTY, and there is no cross-minor fallback

- `OBSERVATION` — `GoApiSnapshot.get` returns `return GoApiSnapshot.EMPTY;` at `GoApiSnapshot.java:115` when `getApiSnapshotJsonFile` yields no provider; `EMPTY` is `public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());` at `:242`.
- `OBSERVATION` — the lookup uses `GoVer baseVer = goVer.withPatch(0);` (`:122`) and requests `"typeinfo/golang/%sgo%s.json%s"` (`:171`); a missing base file returns null (`:124-126`).
- `OBSERVATION` — the patch-diff fallback in `getPatchVerDiffFile` walks only patch numbers of the same major.minor (`:148-166`). It cannot fall from 1.26 to 1.25.
- `OBSERVATION` — installed data: **11 — `ls …/typeinfo/golang/go*.json | wc -l` (2026-10-20)** base snapshots (`go1.15.0`–`go1.25.0`); **0 — `find …/typeinfo/golang -name '*1.26*' | wc -l` (2026-10-20)**; **123 — `ls …/patchverdiffs | wc -l` (2026-10-20)** patch diffs, with **0 — `ls …/patchverdiffs | grep -c '^go1\.25'` (2026-10-20)** for the 1.25 minor; **9 — `ls …/typeinfo/golang/*.gdt | wc -l` (2026-10-20)** legacy `.gdt` archives (`golang_1.15_anybit_any` through `golang_1.23_anybit_any`).
- `INFERENCE` — for any `go1.26.x` build on stock 12.1.4, the base-file miss is unconditional and version-driven; it does not depend on GOOS/GOARCH, because the file check precedes the arch filter.

### L3 — the GDT archives are not a fallback on this code path

- `OBSERVATION` — `GoRttiMapper` constructs its superclass with no archive: `super(program, null);` at `GoRttiMapper.java:331`.
- `OBSERVATION` — `DataTypeMapper.getType` searches the program DTM first, consults `archiveDTM` only `if (dataType == null && archiveDTM != null)` (`DataTypeMapper.java:282-289`), then falls back to built-in types; the constructor leaves `archiveDTM` null (`DataTypeMapper.java:88-93`).
- `OBSERVATION` — the shipped `.gdt` archives predate the JSON switch: the installed 12.1.4 change record says `Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.` — `ChangeHistory.md:585`, under `# Ghidra 12.0 Change History (December 2025)` (`:564`), `### Improvements` (`:582`). A source-wide text sweep finds **0 — `unzip -q <zip> -d <tmp> && grep -rn 'golang_' <tmp> | wc -l` (full 12.1.4 Base source extraction, 2026-10-20)** references.
- `INFERENCE` — on a freshly imported program, the JSON snapshot is the only bootstrap-struct source for this analyzer; the 9 `.gdt` files are inert legacy data, and none covers 1.26.
- `UNKNOWN` — a program whose DTM already contains Go structures from another source (manual archive attach, prior analysis state) could behave differently; that is outside the fresh-import path examined here.

### L4 — missing structs become the bootstrap exception, which aborts the analyzer

- `OBSERVATION` — `registerStructure` calls `getType(structNames, Structure.class)` and, when null, throws `Missing struct definition for class %s, structure name: [%s]` (`DataTypeMapper.java:172-181`).
- `OBSERVATION` — `initStructMappings` catches that `IOException`; only when `apiSnapshot.isInvalid()` (`GoRttiMapper.java:356`) does it throw `"Missing Go bootstrap type info, unable to extract Go RTTI info."` (`:359`). With a valid snapshot and a mapping failure it throws the different message `Invalid Go bootstrap struct mapping info: %s` (`:363-365`).
- `OBSERVATION` — `getSharedGoBinary` catches the bootstrap exception (`:114`), warns, and returns null (`:125`); `GolangSymbolAnalyzer` then logs `Go symbol analyzer error: unable to get GoRttiMapper` and returns false (`GolangSymbolAnalyzer.java:133-137`).
- `INFERENCE` — with `EMPTY`, `isInvalid()` is true and the first path is taken; the analyzer does not reach moduledata/pcHeader parsing. This is the **bootstrap edge class**: functions may still be created by ordinary analyzers, but Go names, types, and signatures are never applied.
- `OBSERVATION` — `isInvalid()` is `arches.isEmpty()` (`GoApiSnapshot.java:503-505`), and `read` keeps only arch names matching `goOS-goArch`, `goOS`, `unix`, `goArch`, `all` (`:108-109,205-239`). So the **same message** can also arise from a present snapshot whose arch list matches nothing.
- `INFERENCE` — the message identifies the *invalid-snapshot* branch, not the *version* cause. Quoted without the binary's version and the data-file state, it is not version proof.

### L5 — the upstream fix adds the snapshot, but is not a host capability

- `OBSERVATION (upstream)` — commit `385e8cd923d09f10b1a7874108e71748875fa174`, author date 2026-03-03, title `GP-6528 add support for golang 1.26`, touches 10 files (**10 — GitHub commit `files` array, 2026-10-20**), including: adds `Ghidra/Features/Base/data/typeinfo/golang/go1.26.0.json`; changes the range line to `GoVerRange.parse("1.15-1.26")`; and also changes pcHeader `textStart` presence (`1.18+` → `1.18-1.25`), the moduledata locator (prefer a `go.module` section), and the build-id read.
- `INFERENCE` — the commit confirms that 12.x's bootstrap is snapshot-driven and that 1.26 needed snapshot data plus downstream layout edits. It is master history, **not** an installed release; the entry claims no release contains it and no recovery result from it.
- `UNKNOWN` — whether any released Ghidra after 12.1.4 contains GP-6528; not opened.

### Path boundary — the Ghidra RTTI gate is not all REA Go handling

- `OBSERVATION` — the installed REA skill routes embedded Go metadata to a built-in parser: `inspect_go_binary` with the explicit local file; `This built-in target-free inspection requires no Go installation or disassembler.` (`SKILL.md:167-169`; the sentence wraps across lines 168–169).
- `OBSERVATION (retained)` — `corpus/knowledge/2026-10-16-l7-01-inspect-go-binary.md:1-8` records a successful `inspect_go_binary` read of `/usr/bin/docker` (`go1.26.5-X:nodwarf5`, module `github.com/docker/cli/cmd/docker`, SHA-256 `70f68a77…`). That path parses build metadata; it does not run the Ghidra Go analyzer.
- `INFERENCE` — a `go1.26` metadata read succeeding and a Ghidra RTTI bootstrap failing are compatible, because they are different parsers. A Ghidra log observation must not be generalized to "REA cannot handle Go 1.26".

### Retained op-pair record and the K1 trace

- `OBSERVATION (retained)` — `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:29,34` records 33,060 procedures on the go1.25.7 build vs 11,595 on the go1.26.8 build; `:64-74` records 11,588 `FUN_*`/`thunk_FUN_*` names and `entry` as the only real name on the latter, plus a transient `Missing Go bootstrap type info, unable to extract Go RTTI info` line from a log directory later deleted.
- `CREDIT` — fleet seat K1 (`KaidokuR14.InstalledGoGate`) independently traced the same source anchors (`.ufo/waves/round-14/w1/InstalledGoGate.md` §2–§4); this draft re-derived them from the archive before reading that report.
- `INFERENCE (conditional)` — **if** that message came from the go1.26.8 session, the source path says the analyzer aborted at L4 with an EMPTY snapshot before L6. The exact causal attribution for the 11,595-procedure outcome is **not proven**: the message text is recalled from a deleted log, the same message also covers the OS/arch-exclusion case, and no run was repeated in round 14.

## Differential decision table

Use the first row whose signal is actually present; a later row is not implied by an earlier one.

| # | signal actually observed | source-supported layer | what it explains | what it does **not** establish | next discriminating check |
|---|---|---|---|---|---|
| 1 | log `Untested Go version [1.26.x]` | L1/L2 | the declared range was exceeded | any recovery failure; the branch only logs | look for the bootstrap message separately |
| 2 | log `Missing Go bootstrap type info, unable to extract Go RTTI info.` | L3→L4 invalid snapshot | RTTI struct mapping never started | that the cause was the Go **version**: a present snapshot with no matching OS/arch also yields this (`GoApiSnapshot.java:503-505`) | check the requested base file *and* the binary's GOOS/GOARCH |
| 3 | no `go1.26.0.json` in installed data | L3 | on stock 12.1.4, a `go1.26.x` build cannot obtain any snapshot; `EMPTY` is unconditional for that minor | that a newer release also lacks it, or that adding one file is sufficient (L5 changes more) | `ls …/typeinfo/golang/go1.26.0.json`; compare a release containing GP-6528 |
| 4 | many `FUN_*` procedures, no Go names, default `entry` | consequence | symbol recovery never applied or aborted | which gate fired, and whether any layout was attempted | row 2's message plus the install/version state; a rerun would be needed for certainty |
| 5 | Go build metadata readable via `inspect_go_binary` while Ghidra names are absent | separate REA built-in parser | the two routes are independent | any statement about the other parser's coverage limits | name the tool/provider behind each record |
| 6 | "the Go 1.26 pclntab is unparseable" | L6 | nothing on stock 12.1.4: L4 aborts before L6 | that layout is the cause of this collapse | only a run with a valid snapshot could reach L6; none exists here |

Two shortcuts this table forbids:

- **Do not** write "Ghidra 12.1.4 rejects Go 1.26 because the supported range ends at 1.25." The range branch logs (`:170-172`); the abort is the empty snapshot (`:356-359`).
- **Do not** write "the missing-bootstrap message proves the Go version caused the collapse." The same message is emitted for an invalid snapshot from any cause, including an OS/arch mismatch; the version link needs the absent `go1.26.0.json` as a separate observation.

## Relation to the retained op-pair entry (no rewrite)

`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:69-73` attributes the collapse to a Go 1.26 moduledata/pclntab layout that the analyzer cannot parse. That mechanism sentence has no parser-source anchor in the old entry and is not supported by the installed source as written: on stock 12.1.4 the bootstrap aborts before any moduledata/pcHeader read *when the snapshot is invalid*. This entry records the source-conditional path and leaves the original cause `UNKNOWN`; it does not edit the old file. L1 owns any append-only correction, and the round-4 operational conclusion — pair cross-toolchain functions by ELF role/address, not symbol name — remains valid and unaffected.

## Bounded scope and unknowns

- Installed release only: Ghidra **12.1.4** (archive hash above). The upstream commit is master history; no released post-12.1.4 binary or source was opened.
- No REA call, no Ghidra import/analysis, and no target execution were performed. The round-4 figures are a retained record, not a reproduction.
- `UNKNOWN` — the actual cause of the retained op-pair collapse. The log artifact is gone, the same message is not version-unique, and no rerun exists. The source path is conditional, not a causal proof.
- `UNKNOWN` — whether 12.1.4 plus a dropped-in `go1.26.0.json` would recover names; GP-6528 also changes downstream layout handling, and no run was made.
- `UNKNOWN` — whether any release after 12.1.4 contains GP-6528, and whether it recovers this pair.
- `UNKNOWN` — non-fresh-import programs that already carry Go data types; the GDT conclusion assumes a fresh import.
- `UNKNOWN` — architectures other than the retained linux/amd64 pair: the file-absence path is version-driven, but the arch-filter path was not exercised.
- No author-side admission is claimed; L1 owns integration and an outside check remains outside this lane.

## Sources reopened for this entry (2026-10-20)

| id | source | location used | limitation |
|---|---|---|---|
| S001 | installed REA skill v42 `SKILL.md` | `:167-169` | documents the target-free metadata route; no execution |
| S003 | installed Ghidra 12.1.4 `Base-src.zip` | `GoRttiMapper.java:79,114-125,170-177,331,354-365`; `GoApiSnapshot.java:115,122-126,148-166,205-239,503-505`; `DataTypeMapper.java:88-93,172-181,282-289`; `GolangSymbolAnalyzer.java:133-137` | shipped source archive, not a compiled-binary disassembly |
| S004 | GitHub commit `385e8cd9…` | title, date, `files` array | master, not a release; `go1.26.0.json` body not opened |
| S007 | installed `ChangeHistory.md` | `:564`, `:582`, `:585` | installed release's own record; a short excerpt is not a full compatibility statement |
| — | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` | `:29,34,64-74` | retained round-4 measurement; scratch deleted, not rerun |
| — | `.ufo/waves/round-14/w1/InstalledGoGate.md` | §2–§4 | concurrent fleet K1 trace; author-side, credited not treated as independent admission |

The GoReSym and BSim sources are deliberately **not** cited: their documented parser/layout and similarity scopes do not bear on this bootstrap edge class, and using them here would be scope padding.
