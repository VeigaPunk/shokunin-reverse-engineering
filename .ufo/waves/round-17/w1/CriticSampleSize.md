# CriticSampleSize — C2 carrier selection (round 17, w1, author-side advisory critic)

Scope: C2 rests on 2 pilot carriers from one host and one session (`pilot/README.txt:1`, runs 10:17–10:19 −03). Which minimum carrier set supports which bounded statement, and which generalizations the knowledge entry must forbid. Judged axes: calibration, depth. Read-only. No REA analyze/search/decompile, no Ghidra, and no carrier was run.

Method (all OBSERVATION unless labelled): I read `claims.json`, `contract.md`, `pilot/*`, and `w1/draft-knowledge-r17.md`. I extracted the S003 Go members from `Base-src.zip` into a `/tmp` scratch dir and read them. I listed the installed `typeinfo/golang` data. I statically read ELF bytes on the host: the build-info magic `\xff Go buildinf:` at 16-byte alignment, the inline uvarint version/modinfo strings, and `PT_INTERP`/`PT_DYNAMIC` from the program headers. The census covered `/usr/bin`, `/usr/lib`, `/usr/local`, `/opt`, `~/.local/bin`, `~/go`, `~/.cargo/bin`, `~/Projects`, `~/.npm`, and `~/.cache`, plus the Go members of 7 cached pacman packages read through `tar -xO` into scratch. I also ran `pacman -Qo`/`-Q` (queries only). The scratch was removed afterwards. Installs: none.

## Finding 1: the pilot logs were seen before the predictions were written, so the 2-carrier table is not a test (calibration, high)

- Counterexample: every value in the draft's prediction table (`w1/draft-knowledge-r17.md:42-45`) agrees with a log the authors had already read. The pilot ran 10:17–10:19 (`pilot/shfmt-log/ghidra.log:1`, `pilot/esbuild-0.25.12-log/ghidra.log:124`). README mtime is 10:20:47, claims 10:21:53 (declared `claims.json:5` 10:25), contract 10:22:46. The contract already encodes observed log shapes: `contract.md:54` quotes both snapshot-label forms, and `contract.md:60` reads "Line format observed". The final runs of the same two carriers (same SHA-256) can only reproduce the pilot.
- Impacted axes: calibration. A "prediction matched" claim on these two carriers is a post-hoc consistency check, not a falsification. Depth: the claim's discrimination goal (`claims.json:20`) is not reached by re-running carriers that were already observed.
- Smallest safe correction: in the entry, label shfmt and esbuild-0.25.12 as the derivation/calibration set. Freeze the `predict.py` outputs for at least one held-out carrier whose log nobody has read: record the sha256 and a UTC time before its `carrier-run.py` starts, and cite both. Only held-out rows may carry the word "predicted" without qualification.

## Finding 2: the claimed third carrier adds a run but no new branch (depth, high)

- Branch map from source (OBSERVATION of S003):
  - `GoApiSnapshot.java:122-126`: no base `goM.m.0.json` → `:115` EMPTY. The log has no GoApiSnapshot line.
  - `:148-166`: the diff search. Exact diff → INFO `Using Go API snapshot for X` (`:163`). Patch > 0 with no diff at or below it → WARN `Falling back from X to Y` (`:159-160`).
  - `GoRttiMapper.java:170-172`: an independent range ERROR.
  - `:179-180`: the label uses the **requested** version, because `read(...)` is passed the requested `goVer` (`GoApiSnapshot.java:111,239`).
  - `GoRttiMapper.java:154-163`: no buildinfo (and no fallback option set) → `return null`, so no version diagnostics at all.
- Installed data (OBSERVATION): base JSONs exist for 1.15–1.25. Patch diffs reach 1.23.12 and 1.24.6. **None exist for 1.25.x.** No base exists for 1.26 or 1.27.
- The claim's set `claims.json:21` covers {1.27.x shfmt, 1.23.12 esbuild, 1.20.12 esbuild}. Both esbuild builds hit the same branch (r16 `exact_diff`; `patchverdiffs/go1.20.12.json.diff` and `go1.23.12.json.diff` both installed). They also share the same distributor and build settings: `-buildmode=exe -trimpath=true CGO_ENABLED=0 GOAMD64=v1` (modinfo of both). The run count goes from 2 to 3 (`claims.json:22`), but branch coverage stays at 2 of the 5 reachable branches. This is premature saturation.
- Branches left unexercised by the claim, with host carriers that exercise them (OBSERVATION, census):

| branch (source) | r16 `selection.py` status | predicted Go log signature (INFERENCE from source) | host carrier (sha256 prefix, size) |
|---|---|---|---|
| in range, base present, patch > 0, no diff | `base_only` (patch 0) | WARN `Falling back from 1.25.8 to 1.25.0 for Go API snapshot`, INFO `Using Go API snapshot for version 1.25.8`, no Untested, no Missing bootstrap | `~/.local/bin/notesmd-cli` go1.25.8, `412dc532d278b9e4`, 4.8 MB, exe, CGO=0, goreleaser. Alternate: `/usr/bin/aether` go1.25.14, `06c91f55df4117e5`, 20.7 MB, exe, CGO=1, `PT_INTERP` |
| buildinfo magic absent | n/a (`predict.py` exits 2, `contract.md:73`) | no GoRttiMapper version lines; possibly no Go analysis at all (`GoRttiMapper.java:160-163`; fallback only if `FALLBACK_GOVER_OPTION` is set, `GoBuildInfo.java:192-197`) | `.../@esbuild+linux-x64@0.27.7/.../esbuild`, sha256 `c638273fcf95573ca74af586677800b4dd874c55f8f945adb54316d6902ba14b`. It has a `.go.buildinfo` name in shstrtab, no magic anywhere, and the string `go1.25.7` at file offset 7701896. That the string is the toolchain version is an INFERENCE. |

- Smallest safe correction: replace or supplement esbuild 0.21.5 with notesmd-cli. It is the cheapest carrier (4.8 MB), held out, and the only one that tests the fallback WARN and the "label ≠ selected bytes" path that r15/r16 described (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:40`). Keep esbuild 0.21.5 only as a labelled replicate.

## Finding 3: version is confounded with build mode, packaging and strip state in the out-of-range cell (calibration, medium)

- The two pilot carriers differ on every axis at once (OBSERVATION, modinfo plus phdrs):
  - shfmt (`pacman -Qo`: shfmt 3.14.1-1): go1.27.0, `-X:nodwarf5`, `-buildmode=pie`, `-linkmode=external`, CGO=1, `PT_INTERP`, has an external debug link (`pilot/shfmt-log/ghidra.log:79`).
  - esbuild: go1.23.12, upstream release, exe, CGO=0, static, `.gosymtab` size 0 (`pilot/esbuild-0.25.12-log/ghidra.log:56`).
- Source resolves the cause: struct types come only from the snapshot (`GoTypeManager.java:443-451`). Missing-bootstrap requires `apiSnapshot.isInvalid()` (`GoRttiMapper.java:356-360`), which is `arches.isEmpty()` (`GoApiSnapshot.java:503-505`). The observations alone do not.
- Host carriers that vary build mode with the version held:

| purpose | carrier | Go | build |
|---|---|---|---|
| vary PIE/cgo/strip, keep Arch toolchain and nodwarf5 (cheap) | `/usr/bin/containerd-shim-runc-v2` (containerd 2.4.2-1), `d3aa80d720b80f70`, 9.3 MB | go1.27.2-X:nodwarf5 | exe, CGO=0, no `PT_INTERP`, `.symtab` present |
| same program and version, different toolchain distribution (costly) | `~/.local/bin/gh` `7469124f70694413`, 42 MB, versus `/usr/bin/gh` `fa4ea7647350b0a3` (github-cli 2.102.0-1) | both go1.27.1 | upstream: exe, CGO=0, `-s -w`, no GOEXPERIMENT; Arch: PIE, CGO=1, nodwarf5 |

- Empty cell (OBSERVATION): no in-range PIE/external-link Go binary exists on this host. All seven cached Arch package members I opened are go1.26.5–1.27.0, all PIE: fzf 0.74.3, gum 2.0.0, runc 1.5.1, lazygit 0.65.0, docker 29.7.2, github-cli 2.100.0, plus containerd 2.3.5 (exe). The "in range + PIE + nodwarf5" combination therefore cannot be observed here.
- Smallest safe correction: add containerd-shim-runc-v2 as an out-of-range held-out run, and state the empty cell as a limit.

## Finding 4: the draft offers a second cause for an invalid snapshot that installed data cannot produce (calibration, low)

- `w1/draft-knowledge-r17.md:117` says the message "can also come from a present file with no applicable records". However, `archSearchOrder` always ends in `"all"` (`GoApiSnapshot.java:108-109`), and every installed base has `all` (`corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:63`). On this installation, an invalid snapshot therefore implies a missing base, for any GOOS/GOARCH.
- That is an INFERENCE. Two things are not checked: diff application preserving `all`, and Gson parse failure. A Gson parse failure throws IOException rather than producing an empty snapshot.
- Correction: scope the alternative cause as "not reachable with the installed bases unless diff application removes `all`; untested".

## Finding 5: the pin and environment gaps let the prediction's inputs drift silently (calibration, medium)

- `contract.md:34` explicitly does not pin the Go data directory, yet every prediction is a function of that listing (base present or absent, diff present or absent).
- The receipt fields at `contract.md:44-47` omit the `REA_GHIDRA_*` environment. The pilot README names `LANGUAGE_ID`, `COMPILER_SPEC_ID` and `DISABLED_ANALYZERS` (`pilot/README.txt:4-5`). Any of these can remove the `golang` cspec or the Golang analyzers, which yields `no_go_analysis` without any version cause.
- Correction:
  - Have `carrier-run.py` pin the exact files that `predict.py` reported. The r16 `selection` dict already carries the base and diff sha256 and size.
  - Pin a digest of the `typeinfo/golang` listing (absence of `go1.26.0.json`/`go1.27.0.json` is itself a premise).
  - Record `{k: v for k in os.environ if k.startswith("REA_")}` in the receipt.

## Finding 6: the compared fields are blind to the branch that distinguishes the models (depth, medium)

- `compare.py` scores only `untested_version`, `snapshot_label` and `missing_bootstrap` (`contract.md:76-78`).
- For a fallback carrier (Finding 2), all three match whether or not the WARN `Falling back` line appears. The label is the requested version in both cases (`GoApiSnapshot.java:111,239`).
- r16 calls this `base_only` (`r16-go-selection-preview.md:40,71`), but Ghidra logs a WARN fallback for patch > 0. A reader of "base_only matched" would wrongly infer "no fallback warning".
- Correction: add a fourth field, `snapshot_route` ∈ {none, exact_info, fallback_warn, patch0_info}, predicted from (`status`, `requested patch`, `selected_patch`) and observed from GoApiSnapshot lines. Alternatively, state in the entry that the fallback signature is outside the scored fields.

## Minimum set and the statement each supports

The set is cost-ordered, all linux/amd64 ELF, analyzed once each under Ghidra 12.1.4, REA 6.5.0 and the `ghidra-default` preset (`pilot/shfmt.json` `analyzer_preset`).

| # | carrier | branch | role | bounded statement it licenses |
|---|---|---|---|---|
| 1 | shfmt go1.27.0 PIE (pilot) | `missing_base` | calibration | For this sha256, the retained log shows Untested + Missing bootstrap, once per Go analyzer (2×, `:82-89`). |
| 2 | esbuild 0.25.12 go1.23.12 (pilot) | `exact_diff` | calibration | For this sha256, the snapshot INFO lines report label 1.23.12 and no bootstrap error. |
| 3 | notesmd-cli go1.25.8 | `base_only`, patch > 0 (fallback WARN) | **held-out** | The installed source model's prediction for an in-range carrier with no patch diff did or did not match a log nobody had seen. This is the only predictive row. |
| 4 | containerd-shim-runc-v2 go1.27.2 exe CGO=0 | `missing_base` | held-out control | The out-of-range signature recurs on a static non-PIE Arch build. Version-not-buildmode is then supported by source plus 2 observations, not proven. |
| opt | esbuild 0.27.7 (no buildinfo magic) | outside `predict.py` | negative control | The absence of version diagnostics is not evidence of an in-range or out-of-range version. |
| opt | esbuild 0.21.5 go1.20.12 | `exact_diff` replicate | replicate | Second base JSON on the same branch; adds no branch. |

Without rows 3 and 4, the entry supports only "two named carriers produced logs consistent with a source reading written after seeing them".

## Generalizations the knowledge entry must forbid

1. Version scope. "Ghidra 12.1.4 / REA fails on Go 1.27 (or ≥ 1.26) binaries." Observed: 1 carrier at 1.27.0 (2 with row 4). A sourced, labelled statement may say: "Source predicts EMPTY for any major.minor without an installed base JSON." It must not be presented as observed coverage.
2. Mechanism. "The Untested ERROR causes the bootstrap failure." These are separate mechanisms that co-occur only because this release's range (`GoRttiMapper.java:79`) equals its JSON set. r14 already rejected the version-alone reading (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:77`; `corpus/lessons/round-14.md:19`).
3. In-range success. "In-range Go binaries bootstrap successfully." Exercised: 1 exe/CGO=0 distributor. Not exercised: PIE in range (no host carrier), patch-0 INFO, fallback WARN (until row 3), and in-range cgo/dynamic (aether only).
4. Platform. Any arch, OS or format statement. Only x86_64 ELF linux carriers exist in the scanned roots, and the language was `x86:LE:64:default:golang` in both logs (`:48`). GOARCH changes bucket order (r16 entry :74-76) and register info (`GoRttiMapper.java:333-334`).
5. Tool version. Anything about other Ghidra or REA versions. S004 moves the range to 1.26 upstream, and `REA_GHIDRA_*` environment overrides were not recorded.
6. Determinism. "The log is deterministic or stable." There is n = 1 run per carrier and no repeat, and capture is by polling (`contract.md:46-47`).
7. Absence claims beyond the capture. Absence claims past the last captured line are forbidden: neither pilot log has a session-end line (`shfmt :126`, `esbuild :124`).
8. Label meaning. "Logged snapshot label = selected bytes." The label is the requested version (`GoApiSnapshot.java:239`). This matches r15 (`r15-go-snapshot-inventory.md:5`).
9. Version from log absence. "No version diagnostic implies a non-Go or in-range binary." esbuild 0.27.7 has no buildinfo magic, so the source path returns before any version check (`GoRttiMapper.java:160-163`).
10. Historical replay. "r4-10's observed-not-cited line is now confirmed." The r4-10 carrier, op 2.40.0 sha `8d029d2c…` (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:19`), is gone: `/tmp/rea-r4` is absent and the pacman cache holds only `1password-cli-2.41.0`. Current `/usr/bin/op` is a different sha (`f4ac474fd0202c73`, also go1.26.8).
11. Recovery counts. `procedure_count`/`string_count` (2581/7813, 8109/17573) and Go type or string counts (`:65-66`, `:83`) are single-run, carrier-specific values, not recovery rates.

## Notes and limits

- "Same day" matters less than "same installation". Predictions depend on the installed data and preset, not on the date. That is why Finding 5's pins carry more weight than temporal spread.
- Why each failing run appears twice: `getSharedGoBinary` returns null on BootstrapInfoException (`GoRttiMapper.java:114-125`). INFERENCE: a null result is not cached, so each Go analyzer re-enters (`TransientProgramProperties` was not read). This resolves the draft's UNKNOWN at `draft-knowledge-r17.md:118` only as a labelled inference.
- Search bound: the census covers only the roots listed under Method. It found no non-x86_64 Go ELF and no pre-1.18 (pointer-format) build-info, so the low out-of-range side (< 1.15) and the BootstrapInfoException "Invalid Go version string" path (`GoRttiMapper.java:166-168`) have no host carriers.
