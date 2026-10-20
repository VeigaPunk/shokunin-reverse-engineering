# Round-17 scout — prior Go-recovery statements vs. the retained pilot logs

Lane: kaidoku-shokunin, round 17 (author-side advisory scout). Read-only: no REA
`analyze`/`search`/`decompile`, no Ghidra, no carrier execution, no writes outside this file.
Allowed `rea inspect-go-binary` was run twice (ids below); installed Base-src.zip members and
installed `typeinfo/golang` JSON were read.

## Abbreviations

| Tag | Absolute path |
|---|---|
| K40 | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md` |
| K14 | `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` |
| K15 | `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` |
| K16 | `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` |
| PS | `.ufo/waves/round-17/pilot/shfmt-log/ghidra.log` |
| PE | `.ufo/waves/round-17/pilot/esbuild-0.25.12-log/ghidra.log` |
| PSJ / PEJ | `pilot/shfmt.json` / `pilot/esb.json` (`binary_overview` evidence from the same runs) |

Verdicts: **CONFIRM** = the retained line directly supports the statement; **PARTIAL** = the line
bears but does not settle it (analogy or missing counterpart); **REFINE** = the line shows the
wording needs qualification; **NOT TESTED** = no pilot carrier/line bears; **COND-REFUTE** =
log + source contradict the stated attribution under the stated condition.

## Pilot material actually available (OBSERVATION)

- `sha256sum -c pilot/SHA256SUMS` → 6/6 OK (both `ghidra.log`, both `script.log`, both analyze
  JSONs). Logs are retained, content-addressed, and quotable.
- Carrier binding is inside the logs: `PS:64,82` say `target-58f765638eed.bin`;
  `PE:55,62` say `target-bab29b2ca7a9.bin`. Those are the first 12 hex of the carrier SHA-256
  (`PSJ` subject `58f76563…ab459`, `PEJ` subject `bab29b2c…d7014`). The binding is a 12-hex
  prefix, not a full digest; pre/post pins were **not** recorded in the pilot (README.txt).
- Build versions confirmed this session with the allowed verb:
  `/usr/bin/shfmt` → `go1.27.0-X:nodwarf5`, `ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`;
  esbuild 0.25.12 → `go1.23.12`, `ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626`.
  Both match `pilot/README.txt`.
- The two carriers give a clean negative/positive pair inside one provider build: shfmt
  (out-of-range, no base) recovers nothing; esbuild (in-range, exact patch diff) recovers.

### The two decisive log sequences (OBSERVATION, verbatim message text)

```
PS:82 INFO  (GoRttiMapper) Reading Go binary info: target-58f765638eed.bin
PS:83 ERROR (GoRttiMapper) Untested Go version [1.27.0]
PS:84 WARN  (GoRttiMapper) Missing Go bootstrap type info, unable to extract Go RTTI info.
PS:85 ERROR (GolangSymbolAnalyzer) Go symbol analyzer error: unable to get GoRttiMapper
PS:86 INFO  (GoRttiMapper) Reading Go binary info: target-58f765638eed.bin
PS:87 ERROR (GoRttiMapper) Untested Go version [1.27.0]
PS:88 WARN  (GoRttiMapper) Missing Go bootstrap type info, unable to extract Go RTTI info.
PS:89 ERROR (GolangStringAnalyzer) Go string analyzer error: unable to get GoRttiMapper
```
```
PE:62 INFO  (GoRttiMapper) Reading Go binary info: target-bab29b2ca7a9.bin
PE:63 INFO  (GoApiSnapshot) Using Go API snapshot for 1.23.12
PE:64 INFO  (GoRttiMapper) Using Go API snapshot for version 1.23.12
PE:66 INFO  (GoTypeManager) Found 4881 Go types
PE:67 INFO  (GolangSymbolAnalyzer) Go version 1.23.12
PE:72 INFO  (GolangSymbolAnalyzer) Fixed 2248 Go function signatures from runtime snapshot signatures
PE:73 INFO  (GolangSymbolAnalyzer) Fixed 2055 Go function signatures from method info
PE:80 INFO  (PropagateRttiBackgroundCommand) Go RTTI callsite fixup info (total/updated/skipped): 9908/9798/2
PE:85 INFO  (GoRttiMapper) Go missing type names: 19
```
`PS` contains **no** `Using Go API snapshot` line at all (grep: none). Source rules below make that
absence informative, not just missing text.

## Claim → bearing line

### A. K40 (r4-10)

| # | Claim (anchor) | Pilot line(s) that bear | Verdict |
|---|---|---|---|
| A1 | `K40:66-68` — go1.25.7 build: full pclntab-name recovery, 33,060 procedures, ~32,933 namespaced | None. Pilot's only in-range carrier is go1.23.12 (`PE:63-67`; `PEJ` procedure_count 8109). No 1.25.7 log. | NOT TESTED |
| A2 | `K40:69-70` — go1.26.8 build: 11,595 procedures, 11,588 `FUN_*` | None. No 1.26.8 carrier in the pilot (README lists only 1.27.0 and 1.23.12). | NOT TESTED |
| A3 | `K40:70-73` — "cannot parse the Go 1.26 moduledata/pclntab layout"; message seen transiently, observed-not-cited | `PS:84` and `PS:88` cite the identical message for **go1.27.0**, retained with a digest. `PS:83` shows `Untested Go version [1.27.0]`. Installed data has no 1.26 or 1.27 base (listing below). Source: `GoRttiMapper.java:353-365` emits this message only in `initStructMappings`'s IOException handler when `apiSnapshot.isInvalid()`, i.e. **before** any moduledata/pclntab parsing; `GoApiSnapshot.java:115` returns `EMPTY` (INVALID at `:242`). | **COND-REFUTE** of the causal clause. If K40's report that the message appeared is accurate, that message itself places the failure at bootstrap struct registration with an invalid snapshot, not at layout parsing; on this installation no 1.26 base exists (`K15:68`). The 1.26.8 inventory numbers are still NOT TESTED, and the old log is still unretained (`K40:198-202`). The pilot is a new, different-version instance, not a replay. |
| A4 | `K40:74-78` — `main.main` hit vs empty; entry name `_rt0_amd64_linux` vs `entry`; `compare_functions` mismatched | None: pilot has no `search`, inventory, or function dossier. | NOT TESTED |
| A5 | `K40:102-106` — candidate restating A1/A2 | As A1/A2; `PE:63-73` shows in-range recovery works at 1.23.12 but says nothing about 1.25.7/1.26.8. | NOT TESTED |
| A6 | `K40:187-188` — a toolchain bump "silently collapses provider symbol recovery" | `PS:83-89` is a loud ERROR/WARN diagnostic, not silence; the CLI still exits 0 (`pilot/shfmt.exit`) and returns 2581 procedures (`PSJ`). | REFINE: the collapse is silent in the overview/exit status, not in the analyzer log. |

### B. K14 (decision table and source observations)

| # | Claim (anchor) | Pilot line(s) that bear | Verdict |
|---|---|---|---|
| B1 | `K14:31-34` — range 1.15-1.25; out-of-range logs `Msg.error "Untested Go version [%s]"`; no throw/return; snapshot lookup follows | `PS:83` exact text at ERROR from `(GoRttiMapper)`; the next event is `PS:84`, not a stop. Source levels/order: `GoRttiMapper.java:170-171` (Msg.error), `:176-181` (snapshot lookup). | CONFIRM |
| B2 | `K14:35-38` — missing base → null → `EMPTY` at `:115`; no earlier-minor fallback | `PS` has no `Using Go API snapshot` line. Source: mapper prints that line only if `getVer()` is valid (`GoRttiMapper.java:178-181`); `EMPTY` carries INVALID (`GoApiSnapshot.java:242`). So absence = no snapshot returned, not merely a lost line. Data listing: no `go1.27.0.json`; latest base is `go1.25.0.json`. | CONFIRM (EMPTY outcome). PARTIAL on cross-minor fallback: not exercised by this carrier. |
| B3 | `K14:39-44` — message only in the IOException handler with invalid snapshot; valid snapshot + failed mapping selects a different message | `PS:84` exact message at WARN; neither log contains `Invalid Go bootstrap struct mapping info`. Source `:353-365`. | CONFIRM (invalid-snapshot branch); alternate branch NOT TESTED |
| B4 | `K14:45-50` — INFERENCE: message = failed registration with invalid snapshot, not the range check; mapper returns null; analyzer returns false | `PS:84` WARN immediately followed by `PS:85` ERROR "Go symbol analyzer error: unable to get GoRttiMapper"; second pair `PS:88-89` from `GolangStringAnalyzer` (`GolangStringAnalyzer.java:103-105`). Catch/null at `GoRttiMapper.java:114-115`; analyzer error at `GolangSymbolAnalyzer.java:135-136`. | **CONFIRM** for 1.27.0 — this is the observation the corpus labelled "not observed execution". It does not settle 1.26.8. |
| B5 | `K14:51-55` — same message can come from a present file with no applicable OS/arch records | No such case: no 1.27 file exists at all. | NOT TESTED |
| B6 | `K14:65-69` — a successful build-info read says nothing about Ghidra RTTI recovery | shfmt build-info reads `go1.27.0-X:nodwarf5` (`ev_f8ef…f4a42a`, this session) while `PS:83-89` shows zero Go symbol/string recovery. | CONFIRM (direct) |
| B7 | `K14:75` — `Untested Go version` row; next evidence "separate bootstrap diagnostic or retained analyzer log" | `PS:83` (the version line) + `PS:84` (the separate bootstrap diagnostic) + `PS:85/89` (branch terminates). The requested next evidence now exists. | CONFIRM |
| B8 | `K14:76` — missing base → EMPTY; next evidence "pin installed data and binary build version" | Build version is pinned (inspect-go id above); installed data is **not** pinned by any pilot artifact, and the planned `W/tools/carrier-run.py` contract pins carrier + `selection.py` but not the Go data dir. Fresh listing (this report) is the only data-side anchor. | PARTIAL — half the requested evidence is unretained; see Finding 4 |
| B9 | `K14:77` — message row; next evidence "distinguish absent base file from OS/architecture exclusion" | No `go1.27.0.json` exists, so OS/arch exclusion cannot explain the shfmt failure; absent base is the only applicable branch. | CONFIRM (absent-base branch); OS/arch branch NOT TESTED |
| B10 | `K14:78` — many `FUN_*`/missing `main.main` means incomplete recovery; next evidence "retained analyzer diagnostics and an appropriately scoped search" | Retained diagnostics now exist (`PS:85,89`); no procedure-name search was run, so `FUN_*` prevalence is not measured. `PSJ` 2581 procedures vs `PEJ` 8109 is not comparable (different binaries). | PARTIAL |
| B11 | `K14:79` — GP-6528 row | None. | NOT TESTED |
| B12 | `K14:84-89` — old `op` cause remains UNKNOWN, not reproduced | Pilot does not analyze 1.26.8; `PS` is a 1.27.0 instance. | CONFIRM (status unchanged) |
| B13 | `K14:121-127` — present-file/no-applicable-architecture path is a source-level possibility, not an observed failure | No present-file case in either pilot carrier. | NOT TESTED |

### C. K15 (inventory)

| # | Claim (anchor) | Pilot line(s) that bear | Verdict |
|---|---|---|---|
| C1 | `K15:5,21` — requested patch labels are not selected data bytes; mapper info can name the requested patch while bytes come from a lower fallback | `PE:63` is `(GoApiSnapshot)` INFO for 1.23.12 and `PE:64` is `(GoRttiMapper)` INFO for 1.23.12; no `Falling back` WARN. Source: `GoApiSnapshot.java:158-163` emits INFO only on the exact-patch branch, WARN `Falling back from %s to %s` otherwise. | **REFINE** — the label is not byte identity, but the log is not content-blind: level + component discriminate exact diff from fallback; only the *mapper* line (`PE:64`) is ambiguous. `log-extract.py` must keep that distinction. |
| C2 | `K15:17` — mandatory same-minor base; missing base yields `EMPTY` | `PS` no snapshot line + bootstrap failure = EMPTY (see B2). | CONFIRM (missing-base shape) |
| C3 | `K15:19` — one selected diff, backward search; inventory does not apply it | `PE:63` shows the exact 1.23.12 diff was found/selected; Java applies it (`GoApiSnapshot.java:128-145`). `PE:66` "Found 4881 Go types" is `typeOffsetIndex.size()` (`GoTypeManager.java:144`), built from the target's moduledata type list (`:100-143`) — a recovered-target count, not a snapshot record count. | PARTIAL/CONFIRM source law; inventory non-application not tested |
| C4 | `K15:15` — generic definitions prove schema content, not successful registration/recovery | Positive: `PE:65-67,72-73`; negative: `PS:84-89`. | CONFIRM as a control pair; sentence unchanged |
| C5 | `K15:66` — 1.25.7: `base_only`, no minor diff, `all` 29,041 funcs / 3,741 types | No 1.25.7 carrier. Fresh read of `go1.25.0.json` reproduces 29,041/3,741 and sha256 `54d10162…f16252` (matches `K15:11`). | NOT TESTED by pilot; inventory value re-observed |
| C6 | `K15:68` — 1.26.8: same-minor base absent | No 1.26.8 carrier; 1.27.0 has the same missing-base shape (`PS:83-84`). Fresh listing has no 1.26/1.27 base. | PARTIAL (analogous version only) |
| C7 | `K15:21` — do not treat a version-shaped log as a content hash | `PE:63-64,67` carry version labels only; no filename or digest appears in either log. | CONFIRM (negative) |
| C8 | `K15:29-35` decision-table rows | Rows 29 (base absent), 30 (exact diff present) are borne by `PS`/`PE`; row 31 (fallback diff), 32 (no diff), 33 (platform key), 35 (snapshot-only replacement) are not exercised. | PARTIAL |
| C9 | `K15:39,46` — virtual `getType` participates in the lookup chain; snapshot validity is not only wording | `PE:68-70` shows three `GoTypeManager` `Failed to get subtype …` warnings during a successful in-range run (`GoTypeManager.java:417`), i.e. type lookup does fail at the edges. This does not demonstrate the virtual-dispatch correction, only that lookup failures occur inside a recovered run. | PARTIAL / adjacent |

### D. K16 (selection preview)

| # | Claim (anchor) | Pilot line(s) that bear | Verdict |
|---|---|---|---|
| D1 | `K16:19` — same-minor base missing → `missing_base`, no diff search; a nearby minor does not rescue | `PS` missing-base outcome for 1.27.0; `selection.py` was not run by the pilot. | PARTIAL |
| D2 | `K16:21` — exact diff exists → filename selection only; preview has not applied it | `PE:63` indicates the exact 1.23.12 file was found; the Java provider applies it (`GoApiSnapshot.java:128-145`) and `PE:65-66` is the downstream result. The preview's non-application is untouched. | REFINE: Java-side application is now observed; the preview limitation is a model boundary, not a property of the run. |
| D3 | `K16:40` — `exact_diff` means exact filename, never a computed snapshot-content digest | No digest in either log. | CONFIRM (negative) |
| D4 | `K16:62-76` — executed source-model table | Pilot adds two executed rows absent from the table: 1.23.12 exact-diff observed success, 1.27.0 missing-base observed failure. The table's 1.25.7 and 1.26.8 rows remain source-model-only. | EXTENDS (no contradiction) |
| D5 | `K16:71` — 1.25.7 `base_only` | No carrier. | NOT TESTED |
| D6 | `K16:72` — 1.26.8 `missing_base` | Analogous 1.27.0 only. | PARTIAL |
| D7 | `K16:9,78-81` — 1.24.5 `exact_diff` despite installed patch 6 | No carrier. | NOT TESTED |
| D8 | `K16:24-26` — requested echo / arch order / base buckets | `PE:63` exercises the linux/amd64 order indirectly (base present, exact diff, snapshot valid); no platform-exclusion case. | PARTIAL (order not directly observable in the log) |

### E. Corpus lessons that restate the same claims

| Claim (anchor) | Pilot bearing | Verdict |
|---|---|---|
| `corpus/lessons/round-14.md:19` — `SUPPORTED_VERSIONS` logs and continues; it does not reject | `PS:83-85` (logs, continues to bootstrap failure) | CONFIRM for 1.27.0 |
| `corpus/lessons/round-15.md:19` — requested version ≠ bytes; no-diff or lower-diff cases can occur | `PE` is the exact-diff case only; the no-diff/lower-diff cases are not exercised | PARTIAL |
| `corpus/lessons/round-16.md:36` — GoVer `toString` formats numeric triples; the model accepts narrower input | `PS:83` shows `1.27.0` for build string `go1.27.0-X:nodwarf5`; `PE:63-67` shows `1.23.12` | CONFIRM (normalization observed) |
| `corpus/lessons/round-16-verifier-spotcheck.md:145` — requested label is not selected input identity; digests remain distinct | No digest in logs; `PE:63` INFO vs a would-be WARN is the only selection discriminator | REFINE (see C1) |

## Calibration findings for L1 / C2

1. **Prediction rows are now fully determined for both pilot carriers.** Using the source rules
   above and the r16 selector law: shfmt → normalized `1.27.0`, `missing_base`, predicted
   `untested_version="1.27.0"`, `snapshot_label=null`, `missing_bootstrap=true`; observed
   `PS:83` / no snapshot line / `PS:84` → 3/3. esbuild → normalized `1.23.12`, `exact_diff`,
   predicted `untested_version=null`, `snapshot_label="1.23.12"`, `missing_bootstrap=false`;
   observed no `Untested` line / `PE:63-64` / no bootstrap failure → 3/3. (INFERENCE from source
   rules; `predict.py` was not run by this seat.)
2. **Normalization datum for `predict.py`.** `go1.27.0-X:nodwarf5` becomes `1.27.0` in the log
   (`PS:83`). Source: `GoBuildInfo.java:488-490` drops the `go` prefix; `GoVer.java:62-65` strips
   at the first non-`[.0-9]` character. `predict.py`'s `normalized`/`untested_version` must emit
   `1.27.0`, not the raw build string. The contract's `go1.27.2-X:nodwarf5` example has the same
   shape.
3. **`log-extract.py` field shape.** Capture `(component, level, version, fallback_from,
   fallback_to)`, not a flat `snapshot_labels` list. The exact/fallback discriminator lives in
   `GoApiSnapshot` INFO vs WARN (`GoApiSnapshot.java:158-163`). Also dedupe the two
   `Reading Go binary info` attempts (`PS:82/86`) and attribute each `unable to get GoRttiMapper`
   error to its analyzer (`GolangSymbolAnalyzer` vs `GolangStringAnalyzer`).
4. **Data-dir pin gap (C2 acceptance risk).** `K14:76` explicitly asks to pin installed data, but
   neither the pilot nor the planned `carrier-run.py` pins
   `Ghidra/Features/Base/data/typeinfo/golang/`. A missing-base claim then rests on unpinned
   installation state. Recommend a manifest pin of the 11 base JSONs + 123 diffs (or at least the
   11 bases) in the receipt; `pins.py` can hash a directory listing.
5. **Log↔carrier binding.** `target-<sha256[:12]>.bin` appears in both logs (`PS:64,82`,
   `PE:55,62`) and matches the carrier digests. Use this in `receipt-validate.py` as a cheap
   binding check, and state that it is a 12-hex prefix, not a full digest.
6. **Exit code is not recovery evidence.** Both analyze runs exit 0 (`pilot/shfmt.exit`,
   `pilot/esb.exit`); shfmt still recovers zero Go symbols. C2 must compare log diagnostics and
   inventories, never REA exit status.
7. **Type-count semantics.** `PE:66` "Found 4881 Go types" is `typeOffsetIndex.size()`
   (`GoTypeManager.java:144`), populated from the target's moduledata type list (`:100-143`). It is
   not K15's 3,741 `all` snapshot types and not a procedure count. Keep those in separate columns.
8. **Fresh installed-data observations (this seat).** 11 bases `go1.15.0.json`…`go1.25.0.json`;
   no 1.26/1.27 base. Diff histogram `1.15:15, 1.16:15, 1.17:13, 1.18:10, 1.19:13, 1.20:14,
   1.21:13, 1.22:12, 1.23:12, 1.24:6`, none for 1.25/1.26/1.27 — matches `K15:64`.
   `go1.23.0.json` sha256 `3b1d795f2e017c17ad15119bd8083e16ccaffb66cd3d504065fe06aea0f63692`
   (all: 27,192 funcs / 3,532 types); `go1.25.0.json` sha256 `54d10162…f16252` (all: 29,041 /
   3,741). `patchverdiffs/go1.23.12.json.diff` exists, so the exact-diff branch was available to
   the esbuild run.
9. **Cost (context only).** shfmt (3.6 MB) analyzed 10:17:30→10:17:54 (~24 s analysis, ~27 s
   total); esbuild (10.4 MB) 10:18:20→10:19:53 (~93 s). K40's ~6 min/call figure is for 41-43 MB
   and is not contradicted.

## What the pilot cannot settle (bounded unknowns)

- The 1.26.8 inventory (`K40:69-70`) and its cause: no 1.26.8 carrier; the old log is deleted; the
  pilot's 1.27.0 instance is not a replay (`K40:198-202`).
- The 1.25.7 `base_only` row (`K15:66`, `K16:71`) and the fallback-WARN branch (`K15:31`).
- The OS/architecture-exclusion branch (`K14:77`, `K15:33`) — no present-file/zero-applicable-keys
  case.
- Whether polled log copies missed lines after the final poll (README limitation; PS ends at
  10:17:56 and PE at 10:19:53 with a normal completion report, so no truncation is visible, but
  that is not proof).
- Installed-data identity during the pilot runs (no data-dir pin).
- Whether the applied 1.23.12 diff was semantically correct; the log shows it was selected and
  applied, not that the patched content matches the binary.

## Recheck commands used (read-only, this seat)

```sh
sha256sum -c /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/pilot/SHA256SUMS
npx -y rea-agents@6.5.0 inspect-go-binary /usr/bin/shfmt --format json
npx -y rea-agents@6.5.0 inspect-go-binary /home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild --format json
ls /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/
unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java
```

Source anchors are archive members of S003 (`Base-src.zip`); the `/tmp/gr17src` extraction used
only to read them and is not evidence. No installs were made. No target executed.
