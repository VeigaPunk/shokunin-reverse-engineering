source: S003 installed Ghidra 12.1.4 Base source archive `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`, SHA-256 `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`; S007 installed `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md`, SHA-256 `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4`; S023 installed `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go1.25.0.json`, SHA-256 `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`; prior entry `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`; registry `corpus/SOURCES.md`.
verified-at: 2026-10-20 — source reading of the named S003 archive members and S007, plus the S023 file identity hash and a targeted bucket-placement query for two type names in that file. No Ghidra analyzer, REA provider, or target execution. Installed coverage counts and the full key census belong to this round's companion inventory record, not to this record.
recheck: `sha256sum` the three absolute paths above and compare with the pins; reopen `Base-src.zip` members at the cited line numbers and `docs/ChangeHistory.md:585`; re-run the two-name `all`-versus-other-bucket query against the pinned JSON.

# Go JSON snapshot selection: base, patch diff, and OS/architecture applicability are three decisions

## Question and scope

The installed Go RTTI path asks three separable questions, and an analyst log
usually answers only the last one: which JSON file is opened, which definitions
are retained from it, and which required bootstrap structure then failed to map.
Source reading below separates those questions. It does not reconstruct any
historical target run and does not claim that snapshot selection alone explains
recovered or missing Go symbols.

S007 records the transition at `Ghidra 12.0 Change History` → `Improvements`,
line 585: "Changed method of bootstrapping Go type info to use json Go snapshot
files instead of gdt files." That statement names the mechanism; it does not
describe selection, fallback, or applicability.

## Prerequisites the selector consumes

- **OBSERVATION — version input.** `GoBuildInfo` strips a leading `go` from the
  build-info version string (`GoBuildInfo.java:488-490`). `GoVer.parse` then
  keeps only the leading `[0-9.]` run, defaults a missing patch to `0`, and
  returns `GoVer.INVALID` when fewer than two fields parse (`GoVer.java:62-79`).
  A suffix such as ` X:rangefunc` or an `rc` marker is discarded by that
  pattern, so it cannot select a different snapshot.
- **OBSERVATION — advisory range.** `SUPPORTED_VERSIONS` is
  `GoVerRange.parse("1.15-1.25")` (`GoRttiMapper.java:79`); both bounds use
  wildcard patch (`GoVerRange.java:42-55`), so the comparison ignores patch
  (`GoVerRange.java:83-87`). An out-of-range but parseable version only logs
  `Untested Go version` and continues (`GoRttiMapper.java:170-172`). An
  unparseable version is a separate `BootstrapInfoException`
  (`GoRttiMapper.java:165-169`).
- **OBSERVATION — OS/architecture strings.** `getGOOS`/`getGOARCH` prefer
  build settings and otherwise map the loader/language
  (`GoBuildInfo.java:272-327`); unmapped values become `unknown`, and
  little-endian `mips`/`mips64`/`ppc64` gain an `le` suffix
  (`GoBuildInfo.java:65-73`). These two strings, not the file name, drive
  applicability.
- **OBSERVATION — data root is module-relative.** The snapshot path is resolved
  with `Application.getModuleDataFile` from the calling class's module
  (`GoApiSnapshot.java:168-178`; `Application.java:954-963`). That prepends
  `data/` and searches the module root, a `build/` directory when present, and
  shadow modules (`Application.java:354-375`; `GModule.java:47-58,147-155`).
  The installation path seen in practice is an instance of that resolution, not
  a hard-coded constant.

## Decision 1 — which file is opened, and what the label means

Base lookup precedes every other consideration: `goVer.withPatch(0)` names
`go<major>.<minor>.0.json`, and a null result returns before any diff is
examined (`GoApiSnapshot.java:118-131`). That forced patch of `0` also means the
two-segment `toString` branch is unreachable here; the requested name always has
three segments (`GoVer.java:138-140,155-159`). The IOException that signals a
missing file is caught inside `getApiSnapshotFile` (`:168-178`), so the absence
itself is silent. The patch-diff name is
`typeinfo/golang/patchverdiffs/go<major>.<minor>.<patch>.json.diff`
(`GoApiSnapshot.java:148-166,168-178`), and the search decrements only the patch
within the same minor. `getApiFile` has a two-segment `go<major>.<minor>.json`
fallback, but no Java member of this archive calls it and it is not the live path
(`GoApiSnapshot.java:183-192`).

| ID | Source-visible condition | Bytes returned | `snapshot.getVer()` | Selector log | Do not conclude |
|---|---|---|---|---|---|
| A1 | `go<M>.<m>.0.json` absent | none; `EMPTY` (`:115,242`) | `GoVer.INVALID` | none from the selector; the mapper info line is skipped too (`GoRttiMapper.java:178-181`) | That a diff was tried, or that another installation lacks the file |
| A2 | base present, requested patch 0 | base raw (`:129-131`) | `M.m.0` | `info` "Using Go API snapshot for M.m.0" (`:162-164`) | That base definitions match the real compiler minor's runtime |
| A3 | base present, requested patch `k`, exact diff `k` present | base + diff `k` (`:133-145`) | `M.m.k` | `info`, no warn | That the diff is authentic or content-checked; no version or digest verification appears on this path |
| A4 | base present, patch `k`, exact diff absent, lower `j` (1≤`j`<`k`) present | base + diff `j` | `M.m.k` | `warn` "Falling back from M.m.k to M.m.j" (`:158-160`) | That the content is patch `k`; only the warn says otherwise |
| A5 | base present, patch `k`, no diff in that minor | base raw | `M.m.k` | `warn` to `M.m.0` | That content and label agree; this is the same substitution with `j=0` |

**OBSERVATION — label and content diverge.** `read` is called with the requested
version, not the diff that was found: `GoApiSnapshot.read(is, archSearchOrder,
goVer)` (`GoApiSnapshot.java:108-111`), and the constructor stores that value
(`:494-501`). The derived provider is also named for the requested version
(`:135`). Consequently `getVer()` and the later mapper info line report the
requested patch even when A4 or A5 supplied lower-patch bytes. The version label
is not byte provenance.

**INFERENCE FROM SOURCE — failure to apply a diff is not a silent fallback.** A
patch parse/apply error is thrown from the derived provider's callback
(`:135-144`) and reaches `getGoBinary`'s caller, which catches `IOException`
separately from `BootstrapInfoException` and logs `Failed to read Go info`
(`GoRttiMapper.java:102-128`). `JsonPatchApplier` fails typed on an unsupported
section or a path miss (`:118`, `:151`, `:158`), and its own contract is use "against
the exact original value" (`:31-34`). Whether any installed diff actually fails
is not asserted here.

## Decision 2 — which definitions are visible

`archSearchOrder` is built as `[goOS-goArch, goOS, unix|"", goArch, "all"]`
(`GoApiSnapshot.java:108-109`), where `unix` is inserted only for a fixed
unix-like `goOS` set (`:180-181`). Reading keeps only keys present in that list,
in that priority order (`:205-240`), and lookups iterate the retained order and
return the first non-null definition (`:514-530`). There is no merge across
keys.

| ID | Condition | Effect in source | Do not conclude |
|---|---|---|---|
| B1 | OS and arch resolve normally | Most specific existing key wins; `linux` outranks `unix`, which outranks bare `amd64`; `all` is last (`:108-109,205-240`) | That all five keys exist or contain that type |
| B2 | an `all` object key is present | `arches` is non-empty, so `isInvalid()` is false (`:242,503-505`) | That the OS/arch-specific definition was found |
| B3 | no listed key yields a retained object in a present file | `arches` empty, `isInvalid()` true, but `getVer()` is valid, so the info line can still print (`:111`; `GoRttiMapper.java:178-181`) | That the file was absent; this is the present-file empty case |
| B4 | a type exists in two retained keys | The more specific definition shadows the broader one; field lists are not merged, though each field's type name is resolved separately through the same lookup (`GoTypeManager.java:582`) | That field-level differences are reconciled |
| B5 | a type exists only under a non-retained key | Lookup misses and may fall back to structural construction (`GoTypeManager.java:402-455`) or fail | That the type is absent from the binary |

**OBSERVATION — the generic bucket carries the bootstrap structs.** In the
pinned installed base, `all.Types` contains `runtime.moduledata` and
`runtime.pcHeader` as `struct`; `runtime.moduledata.Fields[1]` is `pcHeader`
typed `*runtime.pcHeader` (S023 anchor). A targeted query of that file found no
copy of either name in any other bucket's `Types` map. `all` is last in the search
order and is present in this file, so those names remain visible for any
OS/arch string; a platform-specific key is not required to see them. That does
not show every required name resolves, nor that structure registration succeeds.

**OBSERVATION — `*-cgo` keys are never requested.** The documented key family
includes names such as `linux-amd64-cgo` (`GoApiSnapshot.java:51-81`), but the
constructed list contains no `-cgo` suffix (`:108-109`) and the fallback
GOARCH map never produces one (`GoBuildInfo.java:65-73`). Any definition that
exists only under a cgo key is therefore outside the retained set. **INFERENCE**:
whether any needed type is cgo-only in the installed files was not measured.

**OBSERVATION — two different invalidities share one word.** `GoApiSnapshot.isInvalid()`
tests `arches.isEmpty()` (`GoApiSnapshot.java:503-505`), while the mapper's
info-line guard tests `GoVer.isInvalid()` (`major == 0 && minor == 0`,
`GoVer.java:105-107`; `GoRttiMapper.java:178-181`). Only the former selects the
missing-bootstrap branch (`GoRttiMapper.java:351-367`).

## Decision 3 — reading the diagnostic instead of guessing

| Retained signal | Source path it supports | What it does not establish |
|---|---|---|
| No "Using Go API snapshot" info line, then `Missing Go bootstrap type info` | A1 (`EMPTY`, ver invalid) — provided the log retained `Msg.info` and no snapshot IOException occurred | Which installation was consulted, or why the base was absent |
| Info line present, then `Missing Go bootstrap type info` | B3 (present file, no listed key) | That applicability matched the target's OS/arch |
| `Falling back from M.m.k to M.m.j` before the info line | A4 or A5; bytes are at `j` or at `.0` | That the target's patch level differs in any particular type |
| `Failed to read Go info` with a stack trace | IOException on the snapshot path, including patch parse/apply failure (A3/A4) | Which file threw without the exception text |
| `Invalid Go bootstrap struct mapping info` | Snapshot non-invalid, but a required structure mapping failed (B2/B4/B5 or missing mapped definitions) | That the snapshot was absent or the version unsupported |

**OBSERVATION — the missing-bootstrap message carries no version.**
`GoRttiMapper.java:359-360` calls `.formatted(goVer)` on a literal with no
placeholder, so the emitted text omits the version. Do not read a version out of
that message.

**OBSERVATION — the range warning changes no selection.** `SUPPORTED_VERSIONS`
is minor-granular, so every `1.15.N` through `1.25.N` is "tested" and the
advisory error cannot discriminate patch levels (`GoRttiMapper.java:79,170-172`).

## Relation to the round-14 entry

This record **qualifies** two statements in
`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, without changing its
historical conclusion:

- `:51-54` says a present file without applicable records can reach the same
  invalid-snapshot branch. Source permits it only when none of the listed keys,
  including `all`, is present (B3). With an `all` object in the file, the
  snapshot is non-invalid (B2), and OS/arch exclusion becomes a per-type miss,
  not `isInvalid()`.
- The table row at `:77` pairs the missing-bootstrap message with
  "distinguish absent base file from OS/architecture exclusion." On installed
  bases carrying an `all` object, that message cannot arise from OS/arch
  exclusion; the discriminating signals are the presence or absence of the info
  line and the separate `Invalid Go bootstrap struct mapping info` message. The
  round-15 inventory supplies the key-presence observation; this record supplies
  only the source rule.

The old run's precise cause remains **UNKNOWN**; no retained analyzer log,
provider run, or target execution is added by this record.

## Limits and non-claims

- No inventory counts, filename ranges, or coverage ratios are asserted here;
  they belong to this round's pinned inventory record. S023 pins one installed
  base file's identity and its `all` bucket placement, not the whole set.
- S003 is the installed source companion. It is not the executing bytecode of
  `Base.jar`; a bytecode-level check is a separate observation and is not
  claimed here.
- No Ghidra analyzer run, REA provider call, or Go binary inspection was
  performed. A3/A4/A5 describe selector behavior, not decompiler success or
  symbol recovery.
- `JsonPatchApplier` and `GModule` are cited from their archive members only;
  the installed diff files were not replayed here.
- `GoArch.Funcs`/`Types` have no null guard (`GoApiSnapshot.java:445-447`), and
  the type deserializer returns `null` for an unknown `Kind` (`:450-465`). A
  malformed arch section could therefore surface as a null dereference or a
  missing definition; the installed files' well-formedness is not asserted.
- The advisory round-14 artifact pointer and any tool-install records are out of
  scope for this entry.

Evidence: `.ufo/waves/round-15/w1/BaseLookup.md`,
`.ufo/waves/round-15/w1/PatchLookup.md`,
`.ufo/waves/round-15/w1/ArchLookup.md`,
`.ufo/waves/round-15/w1/InstalledLayout.md`, and
`.ufo/waves/round-15/w1/ReviewPatchCases.md`. Those seats re-opened the sources;
this entry states the selection law rather than treating any of them as proof.
