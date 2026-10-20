# ScoutGo1273Exposure — Go 1.27.3 tree: installer, archive identity, carrier suitability

Written 2026-10-20T17:51:19-03:00 (clock read immediately before this write, command 20).
Seat: KaidokuR20.ScoutGo1273Exposure-2 (leaf, read-only). Baseline `14f0260ad319ecc26994381b2415d5a999003375`.
Nothing installed, no Go toolchain ELF executed, no REA analyze/search/decompile, no Ghidra
analyzeHeadless. Scratch: one 70,588,678-byte official tarball download and one `Base-src.zip`
member extraction, both under `tempfile.mkdtemp()` and removed (commands 8, 20). Lane writes: this
report only.

Labels: **[O]** observation from a command/path below; **[I]** inference from source or timing.

## 1. Who installed it — [O]

Seat `DraftSourcesRows` of round 17, wave 1, installed the tree mid-round-17. Anchors:

- `corpus/lessons/round-17.md:135-141` — "Tool installs/updates: none by the L1. Seat `DraftSourcesRows`
  (w1) installed Go 1.27.3 linux/amd64 from the official go.dev tarball into `~/.local/opt/go-1.27.3`,
  not on PATH; its sha256 matched `go.dev/dl/?mode=json`."
- `.ufo/waves/round-17/w1/DraftSourcesRows.md:10` — "sha256 `65efbc80…b40` matched against
  `go.dev/dl/?mode=json`; extracted to `~/.local/opt/go-1.27.3`"; `:42` — channel/version/location/reason
  and "No pacman operation performed"; `:43` — "the downloaded tarball was removed".
- `.ufo/waves/round-17/w2/DraftReportR17.md:83-84` — F17: location `~/.local/opt` deviates from the
  operator channel order's `~/.local/bin`; recorded as not a defect of the artifacts.
- `.ufo/waves/round-18/w1/ScoutMistakeSweep.md:122` — the record does not say why pacman was bypassed
  (open "host/operator" item; unrelated to this seat).
- `.ufo/waves/round-19/w1/InstallRecordDraft.md:34` — dir birth `10:32:19.468`, mtime `10:32:19.948`
  (-0300). `SpotcheckAnchors.md:166-167` and `ToolchainIdentity.md:122` restate the install.
- Primary command trace, `history://KaidokuR17.DraftSourcesRows-3`: `:84` fetched
  `https://go.dev/dl/?mode=json` and parsed it; `:88` downloaded
  `https://go.dev/dl/go1.27.3.linux-amd64.tar.gz` and echoed its sha256 (`65e…` in the transcript's
  abridged view); `:101` unzipped `Base-src.zip` into `/tmp/kr17-src` in the same minute.

Install instant [O]: directory birth **2026-10-20 10:32:19.468 -0300** (`stat`, command 5). Contents
carry **2026-10-19 19:20:36 -0300 = 22:20:36Z**, which equals `VERSION`'s `time 2026-10-19T22:20:36Z`
(the archive's build stamp), so content mtimes are archive-preserved and must not be read as install
times [O, from the equality; inference that tar restored them]. Bracket: the round-17 w1 commit
`271167473d87…` is dated 2026-10-20 10:46:45 -0300 (command 4), i.e. 14 minutes after the directory
birth. The `/tmp` burst at 10:32:12–10:32:49 contains two seats' artifacts (command 18): the
installer's `buildinfo-go1.27.3.go` / `rtdbg-go1.27.3.go` and `kr17-src` extraction [I from transcript
timestamps], plus `ScoutGoExperimentSuffix`'s 1.27.2 source tarball/tree (§6) [O: its transcript and
lane row name the hash].

## 2. Is it an official archive — yes, re-verified end to end [O]

The extracted tarball was deleted (`DraftSourcesRows.md:43`), so archive identity was re-established
from the official source rather than from the install record:

1. Fresh `https://go.dev/dl/?mode=json&include=all` (command 7): document sha256
   `6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950`; entry `go1.27.3`,
   `stable: true`, `go1.27.3.linux-amd64.tar.gz`, sha256
   `65efbc80fdc1fa2cd2631cad5b481777a68e8725f34e89f50fc6ac714e379b40`, size `70588678`. This equals
   the full value whose prefix the round-17 record carries.
2. Re-downloaded that exact URL into mkdtemp and hashed it (command 8): sha256 identical, size
   identical.
3. Extracted it and ran `diff -r --no-dereference <extracted>/go /home/vgpnk/.local/opt/go-1.27.3`
   (command 8): **exit 0, zero differing lines**. Every file in the installed tree is byte-identical
   to the official archive; total tree size 244,139,206 bytes (command 15).

So it is the official linux/amd64 **binary** release archive, not a source build [O]. Trust is
TLS + published sha256; no GPG/signature check was made [gap]. `/home/vgpnk/.local/opt/go-1.27.3/VERSION`
= `go1.27.3` / `time 2026-10-19T22:20:36Z` (command 2), matching the 2026-10-19 release date recorded
at `corpus/SOURCES.md:31` (S025).

## 3. Lane records mentioning 1.27.3 — [O]

`git grep -n "1\.27\.3" 14f0260…` (command 3): **176 matching lines across 51 files**; `git grep -l`
list at command 19. Load-bearing anchors beyond §1:

- `corpus/SOURCES.md:30` (S024, `debug/buildinfo` at go1.27.3) and `:32` (S026, linker `X:` suffix at
  go1.27.3); `SKILL.md:545`; `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:102`.
- `.ufo/waves/round-17/verify.py:162` and `verification.json:391,523,…` — the verification pass invoked
  `…/go-1.27.3/bin/go version -m <file>` (file-reading oracle; historical execution).
- Round 20: `contract.md:88-92` names 1.27.3 **only** in the never-execute clause (`:90`); claims.json
  has no 1.27.3 mention; no W20 evidence references it as a carrier. So 1.27.3 is out of round-20's
  declared carrier set [O].
- Do not confuse `.ufo/waves/round-16/w1/CraftDraft.candidate.md:40` ("`go1.27.3.json.diff`"): that is
  synthetic tool-test fixture text, not evidence that Ghidra ships a 1.27 snapshot (§4 shows it does not).

## 4. Carrier suitability under Ghidra 12.1.4 — the answers differ by purpose

### 4a. Snapshot coverage — [O]

`Ghidra/Features/Base/data/typeinfo/golang/` holds 11 JSON snapshots `go1.15.0.json` … `go1.25.0.json`
and 9 `golang_1.15…1.23_anybit_any.gdt` (command 16; `*.json` count in command 22's batch). There is
**no 1.26 or 1.27 file and no `patchverdiffs/go1.27.*`**. `docs/ChangeHistory.md:585` says 12.1.4 added "support for Golang 1.24 and
1.25" and switched bootstrapping from gdt to JSON snapshots. Declared range: `GoRttiMapper.java:79`
`SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`.

### 4b. What 1.27.3 actually does — source-traced, not run [O source / I outcome]

Ordered path inside `Ghidra/Features/Base/lib/Base-src.zip`:

1. Build info parses fine; `go_version` is exactly `go1.27.3` (no `X:` token), `flags 2`, modinfo
   `path cmd/go|cmd/compile|cmd/gofmt|…` (commands 11, 12; all 10 ELFs agree).
2. Out-of-range is **not** an abort: `GoRttiMapper.java:170-172` only
   `Msg.error(…, "Untested Go version [%s]")`.
3. Snapshot lookup uses the exact major.minor with patch zeroed: `GoApiSnapshot.java:122-126` opens
   `typeinfo/golang/go1.27.0.json` for linux-amd64 (name built at `:168-178`; `withPatch(0)` and
   `toString()` = `1.27.0`, `GoVer.java:138-140,155-158`); patch fallback (`:148-166`) walks
   `patchverdiffs/go1.27.3.json.diff` down to `go1.27.0.json.diff`, none exist.
   Missing base file returns `null` → `GoApiSnapshot.EMPTY` (`:242`, `isInvalid()` = empty arches,
   `:503-505`). There is **no fallback to an earlier minor's snapshot** (only patch-level within the
   same minor). `EMPTY.getTypeDef` returns null (`:524-531`).
4. Constructor: `initStructMappings()` → `registerStructures(GOLANG_STRUCTMAPPED_CLASSES)`
   (`GoRttiMapper.java:348-353`, list at `:294-300`). First class is `GoModuledata`
   (`@StructureMapping(structureName = "runtime.moduledata")`, `GoModuledata.java:37`). With an empty
   snapshot `GoTypeManager.findTypeRec` finds no type def (`GoTypeManager.java:449`), so
   `DataTypeMapper.java:180-181` throws `IOException("Missing struct definition for class GoModuledata,
   structure name: [runtime.moduledata]")`.
5. `initStructMappings` catches it; because `apiSnapshot.isInvalid()` it throws
   `BootstrapInfoException("Missing Go bootstrap type info, unable to extract Go RTTI info.")`
   (`GoRttiMapper.java:356-360`). `BootstrapInfoException extends IOException`
   (`BootstrapInfoException.java:20`); `getSharedGoBinary` catches it, logs it to the analyzer message
   log and returns null (`GoRttiMapper.java:110-124`); `GolangSymbolAnalyzer.java:133-137` then
   `Msg.error("Go symbol analyzer error: unable to get GoRttiMapper")` and returns false.

**Predicted first failure** [I, from the above source chain; not executed]: fatal bootstrap refusal,
`{"kind": "missing_bootstrap_type_info", "phase": "initStructMappings", "va": null, "index": null}` —
before any RTTI/pclntab/moduledata scan. **Calibration hazard for C3:** the first `Msg.error` line in a
bound log will be `Untested Go version [1.27.3]`, which is a range warning, not the failure; the failure
is the message-log/warn line above. A `first-failure-extract` that keys on the first `error` token will
misreport [I]. Also, the `BootstrapInfoException` path is a `Msg.warn`, so there is **no exception stack
trace** to parse; the analyzer's later `unable to get GoRttiMapper` error is the second marker.

### 4c. Verdict

- **Suitable as "later carriers"** for the out-of-range/EMPTY-snapshot path: they deterministically
  exercise the version gate, the missing-snapshot branch and a clean refusal [I]. Good provenance
  (official archive), good ELF shape (below), no `X:` experiment token to complicate version parsing.
- **Not suitable for a successful RTTI mapping** on Ghidra 12.1.4, and equally not on the master state
  recorded in round 17 (range 1.15-1.26, `.ufo/waves/round-17/w1/DraftSourcesRows.md:27`; carried, not
  re-verified live). A positive-path carrier set must stay ≤1.25.
- ELF shape otherwise ideal [O]: 10 ELF carriers, `ELF 64-bit LSB executable, x86-64, statically linked,
  not stripped`; `.gopclntab`, `.symtab`, `.go.buildinfo` present; `runtime.firstmoduledata` is a
  GLOBAL OBJECT at `0x1ac91a0` in `compile`; `.gopclntab` starts `f1ffffff` (magic `0xfffffff1`,
  Go ≥1.20). Sizes 2.3 MB-28.3 MB (manifest below).

## 5. Exposure: the tree is executable and outside the D3 guard — [O]

- 10 ELF carriers and 44 helper scripts carry an exec bit; all ELF modes are `0755` (command 14).
  `go-1.24.6/bin/go` is `0644`; `go-1.25.0/bin/go` is `0755`.
- `W20/evidence/carrier-guard/manual-arm.json` (command 17): `action` manual-arm, `taken_at_utc`
  `2026-10-20T20:37:00+00:00`, **20 carriers, all under `/opt/go-1.24.6/`**, `mode_after 0o644`,
  `exec_probe` = `PermissionError` errno 13. No 1.27.3 (or 1.25.0) entry exists.
- `command -v go` → exit 1 and `~/.local/bin/go` absent (exit 2), so the tree is not PATH-reachable
  (command 13). The only current control over 1.27.3 execution is the prose rule at
  `contract.md:90`; if D3 is meant to enforce "never execute any Go toolchain binary", the guard does
  not yet cover two of the three trees [O].
- Advisory (not applied; host mutation outside this seat): add these 10 paths to a carrier-guard
  manifest, or clear their exec bits. D3's own declared limits still apply (loader-mapped exec and
  root are not prevented).

Manifest-ready rows (mode 0755, from `sha256sum`, command 12):

| path | size | sha256 |
|---|---|---|
| bin/go | 17164222 | 5f5eb6d0b2fb6aa0bb5d5f8c5f1c944e0de955c925f0111af92a9d8f79680b5b |
| bin/gofmt | 3144728 | fd464d1c9098a6714d06bd3fcd2a1fedcdd291e710241160ebb663bf99adf2f8 |
| pkg/tool/linux_amd64/asm | 5435657 | fdcf20e7e2d9a602979b96ced85e6ba6529551ae23a38edcd80181df4566b7a9 |
| pkg/tool/linux_amd64/cgo | 4475043 | 9f67e42d7910067eb5857e5321e1d04aaaa2d22b8ff6d8e1c63bb4365b651049 |
| pkg/tool/linux_amd64/compile | 28267981 | c331d8fc6c4ae9dbe20e8198435db0455f2a5ca55d2d02fc6d7337c906be8283 |
| pkg/tool/linux_amd64/cover | 5820112 | 02d4e5525baf6f7ab661430549dc1137321fc9e27b6ba71797123c305355b46d |
| pkg/tool/linux_amd64/fix | 9536304 | ae0e0eafb4e2e03ff53947e4aae5b1985b197bd196fc7bb75022620c9bb629ad |
| pkg/tool/linux_amd64/link | 7289158 | c9990b939ed48a77ca9a29b33d408d44b56fc4950a28e3d3533025a8dc08b2fe |
| pkg/tool/linux_amd64/preprofile | 2379482 | 75cf4cecf37908adab3c352779bbd4b23fb85b352918711e8cf8fba95ca6d969 |
| pkg/tool/linux_amd64/vet | 9247161 | 4c459358f5fc720f74fc53dd0fc032655e038e2461d8230f1667d0931661ff6c |

## 6. Residue from round 17 in /tmp — [O], two seats

`/tmp` still holds the 10:32 downloads/unpacks (command 18), and they split by seat:

- **`ScoutGoExperimentSuffix`** (round-17 w1): `go1.27.2.src.tar.gz` (35,134,614 B, sha256
  `03495da2ba64894d40f5c4992e49454fa78b50690604ff92b6a…`), extracted tree `/tmp/go1272` (187 MB,
  15,636 files, no `bin/`/`pkg/`), plus `buildinfo-go1.27.2.go`. Its transcript shows
  `history://KaidokuR17.ScoutGoExperimentSuffix-3:69` downloading that URL and `:73` extracting it into
  `/tmp/go1272 --strip-components=1`; its lane row `w1/ScoutGoExperimentSuffix.md:103` records the same
  size/hash. The tarball hash equals the official `go.dev` JSON entry for `go1.27.2.src.tar.gz`
  (command 25), so the residue is an official **source** archive, not a binary install.
- **`DraftSourcesRows`**: `buildinfo-go1.27.3.go` (10:32:30) and the `kr17-src` Base-src extraction;
  the 1.27.3 binary tarball itself was removed (`DraftSourcesRows.md:43`, true).

`/tmp/go1272/VERSION` = `go1.27.2` / `time 2026-10-02T20:28:03Z`. Not lane- or Git-resident, so not a
D1 residue; but it is a second, stale Go source tree (a different patch level than the pinned 1.27.3
tree). `/tmp/go1272/api/go1.27.txt` is byte-identical to the 1.27.3 copy (sha256 `d3315088…`,
command 18), so that file cannot distinguish the trees.

## 7. Commands and exits (all pasted exits are the shell's)

| # | command (abridged) | exit |
|---|---|---|
| 1 | `ls -la --time-style=full-iso /home/vgpnk/.local/opt/go-1.27.3/` | 0 |
| 2 | `cat …/go-1.27.3/VERSION` | 0 |
| 3 | `git grep -n "1\.27\.3" 14f0260… -- .` | 0 |
| 4 | `git log --format='%H %ci %s' 14f0260… -- .ufo/waves/round-17/w1/DraftSourcesRows.md` | 0 |
| 5 | `stat -c '%n\|%w\|%y\|%s\|%A' …/go-1.27.3 …/bin/go …/compile …/go-1.24.6/bin/go …/go-1.25.0/bin/go` | 0 |
| 6 | `find …/go-1.27.3 -type f -perm /111 -printf …`; `… \| wc -l`; `du -sb` | 0 / 0 / 0 |
| 7 | `curl -fsSL -m 45 -o /tmp/kr20go-dl.json 'https://go.dev/dl/?mode=json&include=all'`; `sha256sum`; python entry select | 0 / 0 / 0 |
| 8 | `curl … go1.27.3.linux-amd64.tar.gz` + `sha256sum` + `tar -xzf` + `diff -r` (mkdtemp, removed) | 0 / 0 / 0 / 0 |
| 9 | `file …/bin/go …/compile` | 0 |
| 10 | `readelf -h` / `-S` on `compile` | 0 / 0 |
| 11 | `python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py …/bin/go` | 0 |
| 12 | loop: buildinfo-probe over the 10 ELFs (all `go1.27.3`) | 0 |
| 13 | `command -v go`; `ls -l ~/.local/bin/go` | 1; 2 |
| 14 | `find … -perm /111` (54 files, all 0755) | 0 |
| 15 | `sha256sum` on the 10 ELFs | 0 |
| 16 | `unzip -l Base-src.zip \| grep Go…`; `ls typeinfo/golang/*.json \| wc -l` (11) | 0; 0 |
| 17 | python read of `manual-arm.json` (20 carriers, 1 tree, taken_at) | 0 |
| 18 | `ls -la /tmp/…`; `du -sh /tmp/go1272`; `find … \| wc -l`; `tar -xOf …src.tar.gz go/VERSION`; `sha256sum` api files | 0 |
| 19 | `git grep -l "1\.27\.3" 14f0260… \| wc -l` (51) | 0 |
| 20 | `date -Iseconds`; `rm -rf /tmp/kr20-gsrc-tS6iek`; `test -e …` | 0; 0; 1 |
| 21 | `readelf -sW compile \| grep firstmoduledata` | 0 |
| 22 | `readelf -x .gopclntab compile`; `awk 'NR>=84&&NR<=92' .ufo/waves/round-20/contract.md`; `ls typeinfo/golang/*.json \| wc -l` (11) | 0; 0; 0 |
| 23 | `unzip -p Base-src.zip <member> \| awk/grep` for GoRttiMapper, GoApiSnapshot, GoTypeManager, DataTypeMapper, GoModuledata, GoKind, GoBuildInfo, BootstrapInfoException, GolangSymbolAnalyzer | 0 |
| 24 | `grep -n -E 'go1\.27\|1\.27\.2\|src\.tar' history://KaidokuR17.DraftSourcesRows-3` and `…ScoutGoExperimentSuffix-3` | 0; 0 |
| 25 | `sha256sum /tmp/go1.27.2.src.tar.gz`; python compare with `go1.27.2.src.tar.gz` entry in `/tmp/kr20go-dl.json` | 0; 0 |

## 8. Limits and remaining unknowns

- Never executed: the Ghidra failure in §4b is a source-traced prediction [I]; the L1 must run it after
  freezing predictions. No REA/Ghidra tool was run on this tree by this seat.
- Ghidra master's live snapshot inventory was not re-fetched; the 1.15-1.26 master range is carried
  from round-17 (`DraftSourcesRows.md:27`), not re-verified here.
- `/tmp` residue attribution rests on agent transcripts plus lane rows, not on lane Git objects (the
  files are outside the lane); the residue tarball's bytes are still verified against `go.dev` (§6).
- The transcript view is abridged (`…`), so `:88`'s echoed sha256 was not read in full; the full value
  comes from the lane record and this seat's re-download (§2).
- Archive trust is TLS + published sha256 only; no cryptographic signature check.
- No install/update was performed by this seat (operator directive: nothing to record).

Report: .ufo/waves/round-20/w1/ScoutGo1273Exposure.md
