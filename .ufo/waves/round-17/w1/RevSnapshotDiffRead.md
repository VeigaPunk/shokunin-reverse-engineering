# RevSnapshotDiffRead — does retained evidence identify the 1.23.12 patch diff actually applied?

Scope: Ghidra 12.1.4 `GoApiSnapshot.java` in the installed `Base-src.zip`, the round-17 pilot
Ghidra log for esbuild 0.25.12, and every other artifact the pilot retained. Read-only; no REA
analyze/search/decompile, no Ghidra invocation, no carrier execution, no installs.

## Verdict

**No retained line or artifact names the diff file, its path, or its digest.** The only diff-related
line is `pilot/esbuild-0.25.12-log/ghidra.log:63`, which names a *version* (`1.23.12`), not a file.

**But the retained log already determines the path**, by code semantics: `INFO (GoApiSnapshot)` is
emitted only when the selector found the diff at the requested patch (or patch is 0). For patch 12
the only file the lookup can have opened is
`<ghidra>/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/go1.23.12.json.diff`
(111 215 bytes, SHA-256 `e1fdbc7e690cf6a1bb7c56969c2308ecc51a532daf6b1c7e8cd4dab3b7a99c53`).
What the run did **not** retain is the byte identity of that file at run time. The smallest addition
that closes that gap: **pin that one already-computed path (sha256/size/mtime, pre and post) in the
existing `pins.py` receipt — one path entry, no Ghidra edit, no copied bytes.** Details in §6.

## 1. What the installed source logs (observation)

Source archive identity: `Base-src.zip` SHA-256
`f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`; member `GoApiSnapshot.java`
SHA-256 `765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d`.

| Anchor (member `Base-src.zip:ghidra/app/util/bin/format/golang/...`) | Content |
|---|---|
| `rtti/GoApiSnapshot.java:102-116` | `get()`; returns `GoApiSnapshot.EMPTY` at `:115` when no provider. |
| `rtti/GoApiSnapshot.java:122-126` | base is `goVer.withPatch(0)`; null base short-circuits before any diff lookup. |
| `rtti/GoApiSnapshot.java:128-131` | `patchDiffFile == null` → plain base provider (no diff applied). |
| `rtti/GoApiSnapshot.java:133-145` | diff path → `getDerivedByteProviderPush`; derived name `"go%s.json"` (`:135`); monitor message `"Patching Go API snapshot %s -> %s"` (`:138-139`, a `TaskMonitor` message, not a `Msg` log). |
| `rtti/GoApiSnapshot.java:148-166` | `getPatchVerDiffFile`: downward loop `:153-156`; `Msg.warn("Falling back from %s to %s ...")` `:158-161`; `Msg.info("Using Go API snapshot for %s")` `:162-164`. |
| `rtti/GoApiSnapshot.java:168-178` | filename construction `typeinfo/golang/%sgo%s.json%s` (`:170-171`) with subdir `patchverdiffs/` and suffix `.diff` (from `:154`). |
| `rtti/GoRttiMapper.java:165-181` | `goVer` from build info; range check `:170-172`; `GoApiSnapshot.get(...)` `:176-177`; `Msg.info("Using Go API snapshot for version %s")` `:178-180` prints `apiSnapshot.getVer()`, i.e. the **requested** version (passed to `read` at `:111`), never the selected patch file. |

There is **no** log call in `GoApiSnapshot` that prints a filename, path, size, or hash. The two
messages above are the complete vocabulary. The `:138-139` progress string is not written to
`ghidra.log` (absent from the retained log; compare `FileCacheMaintenanceDaemon` messages, which do
appear at `ghidra.log:11`).

Path resolution is deterministic for a release install: `Application.getModuleDataFile` (`:954-963`)
uses the caller's module (`getMyModuleRootDirectory` `:560-564` + `ReflectionUtilities.java:228-274`,
which drops frames through `Application`), so the caller `GoApiSnapshot` yields module **Base**;
`getDataFileInModule` prepends `data/` (`Application.java:53,354-375`) and `GModule.findModuleFile`
probes the module roots (`GModule.java:147-155`). Installed layout confirms a plain file (not a
jar-copied resource), and the log itself names the install root at `ghidra.log:1`
(`.../Ghidra/Framework/Generic/lib/Generic.jar!/generic.log4j.xml`).

Version normalization: `GoBuildInfo.java:488-490` strips the `go` prefix; `getGoVer()` parses at
`:237-238`; `GoVer.parse` splits and keeps the patch at `GoVer.java:62-75` (suffix stripped at
`:65`). Hence the log label `1.23.12` is `GoVer(1,23,12)` with patch 12 — not 0.

## 2. What the pilot log actually contains (observation)

`pilot/esbuild-0.25.12-log/ghidra.log` has 123 lines (retained; `pilot/SHA256SUMS:1` gives
`f6b6115297915e7eaba5e6dc1165241166fb6c09ae521c7268095aeeda5d89a7`).

| Log line | Text |
|---|---|
| `:1` | `Using log config file: jar:file:/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Framework/Generic/lib/Generic.jar!/generic.log4j.xml` → install root. |
| `:11` | `Starting cache cleanup: /tmp/rea-ghidra-r9xmGu/cache/vgpnk-ghidra/fscache2` → per-run FileSystemService cache root (inside REA's runtime root, deleted at close). |
| `:62` | `INFO (GoRttiMapper) Reading Go binary info: target-bab29b2ca7a9.bin` |
| `:63` | `INFO (GoApiSnapshot) Using Go API snapshot for 1.23.12` ← the only GoApiSnapshot line |
| `:64` | `INFO (GoRttiMapper) Using Go API snapshot for version 1.23.12` (requested version, per §1) |
| `:67` | `INFO (GolangSymbolAnalyzer) Go version 1.23.12` |

Targeted search of that file for `.diff`, `go1.23`, `typeinfo`, `Caching`, `derived`, `Patching`
returned **no matches**; there is no `Falling back from ...` line either. So the retained log
contains one `GoApiSnapshot` message and no path/hash of any snapshot input.

## 3. What that line proves, and what it does not (inference from source, calibrated)

- **Path is fixed.** With patch 12 > 0, the `:162-164` INFO branch is reachable only when the
  `:153-156` loop stopped at the requested patch with a non-null file; a null diff at patch 12 would
  have produced the `:158-161` WARN with `1.23.12 → 1.23.0`. The loop stops at the first present
  candidate, so the file is exactly `patchverdiffs/go1.23.12.json.diff`. (Caveat: at patch 0 the
  same INFO text appears with no diff; the inference is label-dependent and holds here because the
  label is `1.23.12`.)
- **The label asymmetry matters.** A WARN does *not* establish "a lower diff was applied" — the same
  WARN fires when no diff exists in the minor at all (r16 knowledge
  `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:23`). The INFO line is the discriminating
  signal; a version-shaped log alone is not (r15 knowledge
  `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:21`).
- **Application completed.** `JsonPatchApplier.applySection`/`findParent` throw `IOException` on an
  unresolvable path or unsupported section (`JsonPatchApplier.java:75,118,122-158`), the pusher's exception
  propagates through `getDerivedByteProviderPush` and `GoApiSnapshot.get`, and `GoRttiMapper` catches
  only `CancelledException` (`GoRttiMapper.java:183-185`). Analysis succeeded with no such error, so
  the diff parsed and applied over the base without exception. This still does not yield a digest.
- **Not a fingerprint.** `GoTypeManager "Found 4881 Go types"` counts `typeOffsetIndex.size()`
  (`GoTypeManager.java:144`) — target-derived, not snapshot content; do not use it to identify the
  diff.

## 4. The installed candidate, and why it is not yet run-bound (observation)

`Ghidra/Features/Base/data/typeinfo/golang/` holds 11 bases and 123 diffs; `go1.23` has 12. Exact
name match is unique:

| File | Size | SHA-256 | mtime |
|---|---|---|---|
| `patchverdiffs/go1.23.12.json.diff` | 111 215 | `e1fdbc7e690cf6a1bb7c56969c2308ecc51a532daf6b1c7e8cd4dab3b7a99c53` | 2026-09-21 16:37:26 -0300 |
| `go1.23.0.json` (base) | 9 368 866 | `3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692` | 2026-09-21 16:37:26 -0300 |

The sibling scout output `w1/selection-1.23.12.json` independently reports `status: exact_diff`,
the same size/SHA-256, `patch_applied: false`, `evidence_class: source_model` — filename selection
only, no application. Both files predate the run by a month and share the install-extraction mtime,
so present-day hashing is consistent with, but not proof of, the bytes read on 2026-10-20 10:18.

## 5. Retained-artifact inventory (what else could have carried the identity)

- `pilot/SHA256SUMS` — 6 entries only: the two `ghidra.log`, two `script.log`, and two REA JSON
  files. No data-dir file is covered.
- `pilot/esb.json` — `analysis_profile` pins the provider as Ghidra 12.1.4 and `subject.digest` as
  the esbuild SHA-256; `environment` is `null`, `raw_result` is `null`. No diff path/digest.
- `pilot/README.txt:4-6` — the log was captured by 1 s polling and "pre/post carrier pins were NOT
  recorded in the pilot".
- `pilot/` is untracked at baseline `b563c799d97774aae4351276fe43cb897311e349`
  (`git status` shows `?? .ufo/waves/round-17/pilot/`), so these artifacts live only in the working
  tree.
- REA package (`~/.npm/_npx/.../rea-agents`): no file matched `patchverdiffs`, `typeinfo/golang`, or
  `GoApiSnapshot`; the config surface references `GHIDRA_INSTALL_DIR` for provider launch. No
  retained REA output field carries the diff path or digest (see `esb.json` above).

## 6. Smallest retained-evidence addition (no Ghidra edit)

**Add one path to the existing `pins.py` pre/post snapshot, and one derived receipt field.**

1. Path: `<golang-root>/patchverdiffs/go<normalized-label>.json.diff`, where the relative path is
   already produced by `predict.py`'s `selection.selected_diff.path` (see
   `w1/selection-1.23.12.json`), i.e. `os.path.join(golang_root, selected_diff["path"])`. Pin it
   pre-run and post-run with the contracted `pins.py` fields `{sha256, size, mtime_ns}`.
2. Receipt/log-extract field: `applied_diff {branch: exact|fallback, label, path, pin_sha256}`,
   derived from the `:162-164` INFO / `:158-161` WARN lines. An INFO label different from the
   prediction, or a WARN, is already a reportable prediction mismatch.

Why this is minimal and sufficient: it is one path (~250 B of receipt JSON), no bytes copied, no
Ghidra or REA change; `pins.compare` turns "this file hashes X today" into "same bytes at two
instants around the run", and the INFO branch binds that path to the applied diff. The known limit
is `pins.py`'s own: same bytes at two instants, not immutability throughout. Pin the base
`go1.23.0.json` only if the *effective patched JSON* must be reproducible (one more entry).

Stronger but not smallest: poll-copy the FileSystemService derived snapshot. It is the exact
post-patch JSON the analyzer parsed, written on disk because it exceeds the 2 MiB in-memory
threshold (`FileCache.java:59,135`) at
`/tmp/rea-ghidra-*/cache/<user>-ghidra/fscache2/<md5[0:2]>/<md5>` (`FileCache.java:275-279`), but the
bytes are XOR-obfuscated (`ObfuscatedOutputStream.java:51-62`, mask at
`ObfuscatedFileByteProvider.java:32-40`) and the name index is in-memory only
(`FileCacheNameIndex.java:32`), so discovery requires a new-file scan plus deobfuscation; ~9 MB and
a race with REA deleting its runtime root.

## 7. Bounded search log

- Full reads of `Base-src.zip` members: `GoApiSnapshot`, `GoRttiMapper`, `GoVer`, `GoBuildInfo`,
  `JsonPatch`, `JsonPatchApplier`, `GoTypeManager`, `FileSystemService`, `FileCache`,
  `FileCacheNameIndex`, `ObfuscatedOutputStream`, `ObfuscatedFileByteProvider`; `Application`,
  `GModule`, `ReflectionUtilities` from `Generic-src.zip` / `Utility-src.zip`.
- Pilot log read in full (123 lines) plus targeted greps (`.diff|go1.23|typeinfo|Caching|derived|
  Patching`, and `Go API snapshot|patchverdiffs|Patching Go|Falling back`).
- Lane-wide grep for `patchverdiffs|GoApiSnapshot|getPatchVerDiffFile` over `*.md/*.json/*.py/*.txt`
  (hits only in held knowledge/lessons and the r16 selection outputs).
- REA dist grep for `patchverdiffs|typeinfo/golang|GoApiSnapshot`.
- No REA analyze/search/decompile, no Ghidra/analyzeHeadless, no carrier execution, no tool
  installs/upgrades.

## 8. Recheck (for L1)

```
sha256sum /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip
# expect f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804
unzip -p <Base-src.zip> ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java | nl -ba | sed -n '111p;115p;122,131p;148,171p'
# expect: read(...,goVer); EMPTY; withPatch(0); patchverdiffs/ + .diff; WARN at 159-160; INFO at 163
grep -n 'Go API snapshot\|Falling back' <pilot>/esbuild-0.25.12-log/ghidra.log
# expect only :63 GoApiSnapshot 1.23.12 and :64 GoRttiMapper "version 1.23.12"
sha256sum <golang>/patchverdiffs/go1.23.12.json.diff
# expect e1fdbc7e690cf6a1bb7c56969c2308ecc51a532daf6b1c7e8cd4dab3b7a99c53
```
