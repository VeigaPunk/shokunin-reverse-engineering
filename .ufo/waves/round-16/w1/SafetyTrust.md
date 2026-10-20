# SafetyTrust — what source-model output cannot authenticate (r16 w1, sentinel)

Axes: depth, calibration. Read-only static review. I did not execute `selection.py`, `selfcheck.py`, Ghidra, Java classes, a patch engine or any target. Static reads were `unzip -p`/`unzip -l`, `sha256sum`, and `javap` disassembly (JDK `javap` 21.0.12.1, `/usr/bin/javap`) of jar members extracted to scratch `/tmp/sentinel_src`, which has been removed. Tool installs/updates: **none**. No pass, score or target capability is claimed.

Artifacts reviewed are pinned by SHA-256 at review time. Several were still being edited.

| Artifact | SHA-256 |
|---|---|
| `.ufo/waves/round-16/selection.py` | `97a9a8b381287cfbd536b92f20a122c01cf867f24a205a2e320c7592a73abc24` |
| `.ufo/waves/round-16/selection-fixtures.json` | `ff2483d88ad77a39ef5fb2f6ad7310ba6d940094debe03dc6daa0e8b802fcaaa` |
| `.ufo/waves/round-16/negative-fixtures.json` | `d4a4c2036be00fa00819ff251e84a3816aa25f48fbe56984c894b7a285dac92b` |
| `.ufo/waves/round-16/w1/EntryDraft.candidate.md` | `cd6dfab4d6db885c852433c454ed413e38fbcae19c076d3fbe91bad2c420b786` |
| S003 `Base-src.zip` | `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` |
| `Base.jar` | `5ce4a06970f6d0a5c1458d627443a4e474742e06208e8f9c001679bd17f0b7bf` |
| `Base.jar` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.class` (CRC `37c3a9cc`) | `78f1f789f08e318ae7af83d437d2bf833a469a35ac73e72937a05f75e3d29976` |

## F1 — Medium: the entry draft drops the "companion source ≠ executing class" limit

**Evidence.**
- `EntryDraft.candidate.md:10` asks what "the shipped Ghidra source" would select. `:32` says "Source law (S003, shipped member; line numbers as shipped)".
- Limits `:102-116` never say that S003 is unauthenticated against the class Ghidra loads, and `Base.jar` is never mentioned.
- The integrated r15 entry states this limit explicitly (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:13`: "The source companion archive is not authenticated against executing compiled classes"). Round-15 `SnapshotEntry.md:121` also kept it. Leaving it out of r16 is a calibration regression.
- `selection.py` never opens `Base-src.zip` or `Base.jar`. Its fidelity to S003 comes from human transcription. Its fixtures were hand-derived from the same source reading, so a fixture pass shows model-versus-author agreement, not source or class authentication.

**Exploit path.** Once integrated, the entry is cited as "Ghidra 12.1.4 selects X for request R." Two gaps make that claim unsupported:
- The runtime class can differ. `Ghidra/patch/README.txt:1-4,6-9` says classes or jars placed there load *before* the release jars. Today the directory holds only `README.txt`, but that is a point-in-time `ls`. No launch classpath was retained.
- An r15 seat already made the stronger form of this overclaim. `round-15/w1/InstalledLayout.md:162` says one constant string is "proving the installed binary matches the S003 companion source".

**Narrower evidence available (static, this seat).** `javap -c -p -l -constants` on the jar member above is consistent with S003 for exactly these units:
- `get`: LineNumberTable 105–115. The concat recipe `\u0001-\u0001` is applied to `goOS` then `goArch`. `"unix"`/`""` is chosen via `IS_GOOS_UNIX.contains(goOS)`, then `goArch` and `"all"`.
- `getApiSnapshotJsonFile`: lines 120–145. It calls `withPatch(0)` and returns null on a null base. Only then does it call `getPatchVerDiffFile`. The derived name is `go%s.json` of the *requested* `goVer`.
- `getPatchVerDiffFile`: lines 151–165. The loop runs while `getPatch() > 0` and the probe is null, using `"patchverdiffs/"` and `".diff"`. It warns or logs info by comparing patch numbers.
- `getApiSnapshotFile`: lines 170–176. It formats `typeinfo/golang/%sgo%s.json%s`, calls `Application.getModuleDataFile` and `getFile(true)`, and maps `IOException` to null.
- `<clinit>` line 180: the 12-string `IS_GOOS_UNIX`.
- `GoVer.class`: `toString` is `%d.%d.%d`, or `%d.%d` when patch is −1. `prevPatch` clamps at 0.

This consistency was judged by reading. It is not a mechanical equivalence check. It says nothing about the loaded class, `GoVer.parse`, `GoBuildInfo` or `JsonPatchApplier`.

**Smallest remediation.** Add one limit line to the entry: "S003 is the companion source; the preview opens neither `Base.jar` nor the runtime classpath, and `Ghidra/patch` can override release classes." The javap consistency may be recorded as a separate, narrower observation only if its argv and digests are retained. Do not upgrade the wording to "Ghidra 12.1.4 selects."

## F2 — Medium: the target tuple (version, GOOS, GOARCH) is caller-supplied; Ghidra derives it differently

**Evidence (S003).**
- `GoRttiMapper.java:165-177`: `goVer = buildInfo.getGoVer()`, then `GoApiSnapshot.get(goVer, buildInfo.getGOARCH(program), buildInfo.getGOOS(program), …)`.
- `GoBuildInfo.java:272-275,283-297`: the `GOOS` build setting is used if present. Otherwise GOOS comes from the loader:
  - ELF maps to `"linux"` (source comments at `:284,:287`: "TODO: this mapping needs more logic");
  - PE maps to `"windows"`, Mach-O to `"darwin"`;
  - anything else gives `"unknown"`.
- `GoBuildInfo.java:306-329`: GOARCH comes from the `GOARCH` build setting, otherwise from a 6-entry language map, otherwise `"unknown"`. Little-endian mips/mips64/ppc64 get an `le` suffix.
- Version (`GoBuildInfo.java:488-490`): the leading `go` is stripped from the buildinfo string.
- Fallback version (`GoRttiMapper.java:153-159` with `GoBuildInfo.java:192-201`): taken from the program option `Go version fallback`.
- `GoVer.parse` is lenient (`GoVer.java:62-81`).

**Exploit path.** Take a FreeBSD Go ELF whose buildinfo lacks a `GOOS` build line:
- Ghidra searches `[linux-amd64, linux, unix, amd64, all]`.
- A preview run with `--goos freebsd` reports `[freebsd-amd64, freebsd, unix, amd64, all]` and different `base_matching_buckets`.

[INFERENCE, not verified here] Go added `build` setting lines in 1.18, so 1.15–1.17 binaries would always take the loader fallback. Another case: a `devel …` version string parses INVALID, and `GoRttiMapper.java:166-169` throws before `get`. The preview has no such state.

**Impact.** No preview row can be attached to a target or a historical run without target-derived evidence of Ghidra's own tuple. The entry's linux/amd64, windows/amd64, darwin/arm64 and linux/riscv64 rows (`EntryDraft.candidate.md:68-84`) are caller assumptions.

**Smallest remediation.** Add one limit to the entry: "request/GOOS/GOARCH are caller-supplied. Ghidra derives them from `GoBuildInfo`, using loader/language fallbacks, the fallback-version option, and lenient parse (anchors above). Mapping a target requires retained target evidence, e.g. the program-info properties written at `GoBuildInfo.java:352,365-367`." No code change is required.

## F3 — Medium: negative fixtures misstate source behavior

- **`invalid-request-v-prefix`.** The note says `GoVer.java:65` "strips the leading 'v' … so source accepts". That is false.
  - `replaceAll("[^.0-9].*$", "")` deletes from the *first* character outside `[.0-9]` to the end of the string. For `v1.21.0` that is the whole string.
  - The result is `""`, which splits to length 1, so `GoVer.java:66-68` returns `INVALID`.
  - Source and model both reject this input, so the note invents a strictness divergence. The `RequestError` expectation itself is fine.
- **`unreadable-base-json-array`.** The note says `beginObject` throws `JsonSyntaxException`.
  - Installed `Ghidra/Framework/Generic/lib/gson-2.13.2.jar` has `JsonReader.beginObject`, which calls `unexpectedTokenError` and throws `new IllegalStateException` (javap).
  - [INFERENCE] That exception is unchecked, so it bypasses the "IOException if error parsing json" contract of `get`. Propagation beyond `get` was not traced.
- **`missing-base-empty-root`.** The note cites "returns null at :171". The null return is the `catch` at `GoApiSnapshot.java:175-176`.
- **`missing-base-two-part-name-no-fallback`.** The note calls `getApiFile` "legacy external-API only". That is an uncited characterization. I found no caller in the extracted `golang/` or `gfilesystem/` packages, and that is the only claim the evidence supports.

**Smallest remediation.** Rewrite these four notes. Expectations are unchanged.

## F4 — Low: preview stdout carries no root or installation identity

`selection.py:131-133` reports `path` relative to `--root` ("stable across roots", `:118`). The emitted JSON has no root and no Ghidra identity. Ghidra's identity is `application.properties` 12.1.4, revision `8b6bbb857accdfa20dc5b2f5dea471178c2e9fbc`. Digests identify the bytes, not their installation. Retained stdout alone could come from a fixture tree or another install with the same names.

**Remediation.** Always cite stdout together with its retained argv, which QUALITY 18 in the working tree already requires. Optionally emit the resolved `--root`. Do not claim installed-tree provenance from stdout alone.

## F5 — Low: the preview's digests cannot be matched to bytes Ghidra consumes on diff paths

- `FileSystemService.java:462-489` caches the derived provider under the key `containerMD5 + "_" + derivedName`, where the derived name is `go<requested>.json` (`FileCacheNameIndex.get/add`). The index is an in-memory soft `ReferenceMap`.
- The selected diff's identity is not part of the key.
- The resulting FSRL MD5 is of the *patched output* (`:486-488`).

**Impact.** Any Ghidra-side MD5 or FSRL for an `exact_diff`/`fallback_diff` case is incomparable with the preview's base/diff SHA-256. Within one session, changing the diff without changing the base could reuse stale derived bytes. That is an inference from source and was not exercised.

**Remediation.** Add a limit line only.

## F6 — Low: model-only "unreadable" outcomes are not source outcomes

`_top_level_keys` (`selection.py:145-150`) uses `json.load`, which rejects trailing data after the top-level object. Ghidra's `read` calls `reader.endObject()` and closes without checking for end of document (`GoApiSnapshot.java:214-226`). The model's exit 2 therefore means "the model could not evaluate", not "Ghidra could not read". This is not reachable on the installed bases, all 11 of which round-15 parsed.

**Remediation.** Make the CLI and entry wording say so.

## Cross-reference (other lanes own this; included for readiness honesty)

At the pinned digests, `selection.py:254` emits `selected_patch: 0` on `base_only`, and `:106-112` drops `""` from `arch_search_order`. Meanwhile `selection-fixtures.json` expects `null` in five `base_only` cases and keeps `""` in `windows_omission`. No "selfcheck passes" statement is attainable until these are reconciled.

## Non-defects confirmed

- The `selection.py` docstring and `w1/SelectorModel.md:80-91` correctly disclaim patch application, the module-data search path and provider parity.
- EntryDraft limits 2–7 correctly separate log lines from selection, the requested label from data, a single root from a multi-root layout, and strict parsing from lenient parsing.
- Duplicates avoided: patched-content facts are covered by `AttackHonesty.md`; path joins, FIFOs and roots by `SafetyPaths.md`.
