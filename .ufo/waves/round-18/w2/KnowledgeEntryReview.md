PARTIAL

# KnowledgeEntryReview — round 18 wave 2 (falsify)

**Seat and scope**
- Seat: `KaidokuR18.KnowledgeEntryReview`. Author-side advisory critic, leaf. Not outside review.
- Target: `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Below it is written `KE:<line>`, meaning `git show REV:<that path>` line N.
- Freeze commit: `eb6c2668…`. Baseline: `9011581…`.
- The worktree equals REV (`git diff b2aad08… --stat | wc -l` → `0`).

**What I did not do**
- No REA run and no Ghidra run.
- No carrier was executed.
- No lane file was edited.
- No tool was installed or upgraded.

**Scratch writes**
- One `/tmp` mkdtemp rebuild, since removed (`rm -rf` exit 0).
- One `/tmp` page fetch, since removed.

**Shorthand used in commands below**
- `L` = the lane directory.
- `REV` = the full REV hash.
- `G` = `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`.
- Every command ran with cwd `L` and literal values.

**Labels and exit codes**
- `[O]` = observation; `[I]` = inference.
- An exit code marked `0†` means the harness reported success but the shell did not echo the code.

## Verdict

The frozen-rule verdict **confirmed** survives everything I tried. I re-derived every number the target lists, and all of them hold.

Several statements still overreach the evidence:
- "the only … ELF on the host" is false by the entry's own source (F1).
- The Go 1.25 generalization has no held-out loud 1.25 case (F2).
- The QUALITY #21 wording on mid-run maps is off (F3).
- The recheck cannot be run as written (F4).

So the verdict is PARTIAL, not BROKEN. Every defect can be fixed by appending a named correction.

## Holds — re-derived at REV

| Claim (KE line) | Command | Exit | Result |
|---|---|---|---|
| 15 labels; 15/15 `receipt-validate.py --require-mid-maps` (KE:68) | `for d in .ufo/waves/round-18/runs/*/; do python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps "$d/receipt.json"; echo $?; done` | 0 ×15 | [O] 15/15 exit 0. 15 run directories plus `run-log.txt`. |
| 22 mid-run maps (KE:68) | Python count of `steps.*.pin_checks[].map_path` per receipt | 0† | [O] 3+2+2+1+2+1+1+1+1+1+2+1+1+2+1 = **22**. There are 22 `pins/mid-*.json` files in `git ls-tree -r REV`. |
| 15/15 compare exit 0 (KE:83) | `python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction predictions/<l>.prediction.json --observation runs/<l>/observation.json` ×15 | 0 ×15 | [O] `all_match: true` ×15, with 3 `extra.*` fields each. compare.py:245 exits 0 only when all fields match. Retained `compare.exit` = 0 ×15. `run-log.txt:3-31` shows `compare=0` ×15. |
| Ghidra log lines 97/177, 408/451, 73/206 (KE:74,76,81) | `grep -nE 'Go analysis failure\|Invalid index\|read past EOF' runs/<l>/logs/*/ghidra.log` | 0 | [O] Exact match. Lines 97 and 177 (aether); 408 and 451 (s1246-swiss-nethttp); 73 and 206 (kimi-webbridge). Values `17645861, 111938854`, `22386945`, `15606016`. |
| Only 3 logs fail; 11 non-D synthetic labels and 6 noswiss labels do not (KE:87,95) | Same grep with `-l`, per label | 0† | [O] Failing logs are calib-aether, s1246-swiss-nethttp and real-kimi-webbridge only. Synthetic labels: 12 − 1 (D) = 11 non-D. Noswiss labels: 6. |
| Routes INFO/WARN (KE:74-81) | `grep -hE 'Using Go API snapshot\|Falling back' …/ghidra.log` | 0† | [O] As tabled. kimi: `WARN (GoApiSnapshot) Falling back from 1.24.13 to 1.24.6`. |
| Evidence IDs (KE:74,76-78,81) | `grep -ho 'ev_[0-9a-f]\{64\}' runs/<l>/analyze.json` | 0† | [O] All 5 tabled IDs equal the retained IDs. Each ID is also in `receipt.json` (1 line). |
| Carrier identity and binding | `sha256sum` of the 3 real carriers; Python check that prediction sha = receipt `sha256_pre` = `sha256_post` = log `target-<12>` | 0† | [O] `06c91f55…`, `412dc532…` and `71067480…f8ad35d` match KE:49-52. Binding holds 15/15. |
| Carrier bytes | `sha256sum -c` against `REV:carriers/SHA256SUMS` in `~/.local/share/kaidoku-r18/carriers` | 0 | [O] 12/12 OK. |
| Predictions frozen before the run, unchanged at REV (KE:1,83) | `git diff --stat eb6c266 REV -- .ufo/waves/round-18/predictions/ tools/swiss-misread.py gen-predictions.py carriers/` and `git diff --stat eb6c266 REV -- .ufo/waves/round-17/tools/` | 0 / 0 | [O] Empty diffs. Emulator sha256 `14924bd6…` equals the frozen `c3.emulator_sha256`. All 15 `producer.json` record `branch_tip eb6c2668e5cb`. |
| Held-out values not seen before the freeze | `git log --all -S15606016` and `-S22386945`; grep of the fleet repo (gitignore off) | 0† | [O] The values first appear in the same-second commits `5397f9f`/`13b6a5c`/`eb6c266`, only in `predictions/*` and in w1 `ConnC3Prediction.md` / `SwissMisreadTool.md` as emulator **predictions**. No pre-freeze Ghidra log contains them. |
| Emulator re-derivation (KE:3) | `python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier <path> --golang-root $G` ×15, diffed against `predictions/swiss-misread/<l>.json` | 0 ×15 | [O] 33/33 keys identical for all 15 labels (`diff=[]`). |
| Decision rule (KE:60-64) | `git show REV:.ufo/waves/round-18/predictions/decision-rule.json` | 0† | [O] D = {calib-aether, s1246-swiss-nethttp, real-kimi-webbridge}. Held-out = the last two. Per-label table equals KE:74-81. |
| S035 (KE:1,18-19) | `sed -n` of `~/.local/opt/go-1.25.0/src/internal/abi/{map_swiss.go:32,map_noswiss.go:25,map_select_swiss.go:5,22,type.go:358-363}`; `cmp` against go-1.24.6 | 0† | [O] All anchors hold. Files are identical across 1.24.6 and 1.25.0. Sizes: `Type` 48 + 5×8 puts `SlotSize` at +88. Swiss is 108 bytes, aligned to **112**. Old is 48+32+8 = **88**. |
| S003 (KE:22,28-32) | `unzip -p Base-src.zip …` at the cited lines; zip sha256 `f00d29c2…` matches the row | 0† | [O] `GoMapType.java:33` lists `{runtime.maptype, internal/abi.MapType, internal/abi.OldMapType}` (no Swiss). `GoType.java:144-147` reads uncommon at `getStructureEnd()`. `GoName.java:94/95/124`. `GoRttiMapper.java:1053-1075` has no range check on `off`. `MemoryByteProvider.java:302` is `Invalid index`; `:312` is `Unable to read past EOF`. |
| S023 alias in both snapshots (KE:20-21) | Python walk of `$G/go1.2{4,5}.0.json` | 0† | [O] `all/Types/runtime.maptype` = alias → `internal/abi.OldMapType` in both. go1.25.0.json sha `54d10162…` matches S023. |
| S034 lines 571-573 (KE:1) | `curl -sS https://go.dev/doc/go1.24 \| sha256sum`; `sed -n '560p;571,573p'` | 0 | [O] Page sha `d35c2d52…` equals the row. `<h2 id="runtime">` at line 560. The `GOEXPERIMENT=noswissmap` sentence is at 571-573. |
| Provenance trio comes first (QUALITY, `/home/vgpnk/Projects/shokunin/CORPUS.md:18,163-165`) | `git show REV:KE \| grep -n ''` | 0† | [O] Lines 1-3 are `source:`, `verified-at:`, `recheck:`. |
| REA 6.5.0 / Ghidra 12.1.4, one pass 16:24–16:32Z (KE:2) | grep for `rea-agents@` in receipt/producer and `ghidra_*_PUBLIC` in logs; `run-log.txt` | 0† | [O] Each run records `rea-agents@6.5.0` and `ghidra_12.1.4_PUBLIC`. `run-log.txt:2,31` spans 13:24:07–13:32:10-03:00. |
| Absence claims bounded (QUALITY #20) | `grep -c 'Golang Symbols'` and `grep -c 'REPORT: Analysis succeeded'` per log | 0† | [O] Both counts are 1 in all 15 logs. Absence of a failure line is therefore bounded past the analyzer. |
| w1 citations exist (KE:36,47,53,103-105,119) | `git cat-file -e REV:.ufo/waves/round-18/w1/<7 files>` | 0 ×7 | [O] All 7 exist. `RevAetherReplay.md:26,131` gives `types+0x28 = 0x954048`. `SwissMisreadTool.md:155` gives "5924 vs 5927", i.e. 3 of ~5927. |
| Aether ID equals the r17 second-pass ID (KE:87-88) | `grep -rl ev_247261e8… .ufo/waves/round-17/runs/`; `REV:r17 entry:119` | 0† | [O] Found in `round-17/runs/pro-aether/{analyze,receipt}.json`. r17:119 names it as the second-pass ID. (See F9 for the stated reason.) |

## Findings

### F1 — "the only non-r17 Go 1.24/1.25 ELF on the host" is false (KE:52-53)

Axes: calibration, depth (premature saturation).

**Counterexample.** The entry's own source lists two upstream toolchain installs (`RealCarrierCensus.md:48-50`). The census itself only claims kimi-webbridge is "the only real non-carrier **application**" (`:46-47`).

**Reproduction.**
- Command: `for f in $(find ~/.local/opt/go-1.24.6 ~/.local/opt/go-1.25.0 -type f -perm -u+x -size +4k \( -path '*/bin/*' -o -path '*/pkg/tool/*' \)); do python3 -I -B .ufo/waves/round-17/tools/buildinfo-probe.py "$f"; done`
- Exit: 0 per file.
- [O] **29** real ELFs: 20 report `go1.24.6` and 9 report `go1.25.0`.
- None is in r17 `carriers.tsv` (`grep -c '.local/opt'` → 0).

**Unused held-out candidates** [I: emulator output only, no REA run]
- Command: `swiss-misread.py --carrier <each> --golang-root $G`.
- Exit: 0 for 27 files. Both `link` binaries are `unparseable`.
- `diagnostic=true` H1 `invalid_index` predictions on **7 go1.24.6 tools**:

  | Tool | Predicted index |
  |---|---|
  | `go` | 35082496 |
  | `addr2line` | 22078465 |
  | `compile` | 36421889 |
  | `nm` | 22070273 (`*dwarf.abbrevTable`, slot 40) |
  | `objdump` | 13816064 |
  | `pprof` | 27091201 |
  | `trace` | 25696001 |

- go1.25.0 `vet` predicts H1 `invalid_index 13902080` (`*types.valueMap`, slot 40). Its `diagnostic` is false only because H0's walk channel also predicts `invalid_index` (1801722468838924630).

**Smallest correction.** Replace with: "the only real non-carrier *application* … in the census roots; the two upstream toolchain installs (29 ELFs) were not used". Name them under "Not examined".

### F2 — The Go 1.25 arm has no held-out loud case, and this is not stated

KE:5, 10, 94; Limit at KE:94; Not examined at KE:110-119. Axes: calibration (QUALITY #5, #7).

**What was observed** [O]
- Both held-out loud confirmations are 1.24.x: s1246 is go1.24.6; kimi is go1.24.13 with base go1.24.0 + .6 diff.
- On 1.25.x, the only loud observation is the **calibration** carrier, aether.
- Every held-out 1.25 label has H1 = H0 = `none`, so none of them is diagnostic. This covers s1250-* and notesmd-cli. Source: the `decision-rule.json` table.
- w1 already warned of this: `ConnC3Prediction.md:13`, "cannot confirm the aether 1.25.x case".

**Inference** [I] Extending the mechanism to 1.25 is a sound inference from source. S035 files are identical across versions, and S023 has the same alias in both snapshots. But it is inference, not held-out observation.

**Smallest correction.** Add to Limit: "both held-out loud cases are go1.24.x; 1.25.x rests on the calibration carrier plus source identity (INFERENCE)". Add a "no held-out loud 1.25.x carrier" bullet under "Not examined".

### F3 — QUALITY #21: "every retained mid-run map recomputed" / "22 mid-run maps recomputed" (KE:3, 68)

Axes: calibration, operability.

**Evidence** [O]
- The validator recomputes the following. Source: `receipt-validate.py:456-468` (docstring); code at `:512` (digest), `:552` (verdict) and `:566` (mismatch finding).
  - the map **file** SHA-256 against `map_sha256`
  - a parse of the map
  - `taken_at_utc` and the entry counts
  - the `equal`/`changed`/`missing` **verdict**, via `pins.compare(pins_pre, mid_map)`
- It does not and cannot recompute the map's per-path entries at the mid-run instant.
- QUALITY #21 (`REV:corpus/QUALITY.md:31`) has two relevant rules:
  - An exit 0 "is described only by the fields it recomputes". A verdict is never described as "the map".
  - A retention statement — here KE:66-67, "retained as `pins/mid-<n>.json` with `map_sha256`" — needs a recheck that prints the retained keys.
- The recheck's validator prints only `counts`, `checks_performed` and `findings`.

**Key-printing recheck that satisfies #21.**
- Command: `python3 -I -B -c` loading `runs/calib-aether/receipt.json` `steps.analyze.pin_checks[0]` and its `map_path`.
- Exit: 0.
- `pin_checks` keys: `[changed, entries, equal, map_path, map_sha256, missing, taken_at_utc]`.
- Map keys: `[entries, monotonic_ns, taken_at_utc]`.
- Entry keys: `[mtime_ns, sha256, size]`.

**Smallest correction.** Reword to: "22 retained mid-run map files: SHA-256 re-hashed against `map_sha256`, `equal/changed/missing` recomputed from `pins_pre`". Add the key-printing command.

### F4 — The recheck (KE:3) does not run as written

Axis: operability.

**(a) `<GOLANG_DIR>` is never defined.**
- It appears only as a placeholder: `REV:SKILL.md:539,590` and KE:3. There is no definition anywhere at REV (repo grep finds none).
- The natural guess, the Go toolchain root that S035 names, fails:
  - Command: `python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier /usr/bin/aether --golang-root ~/.local/opt/go-1.25.0`
  - Exit: **2**.
  - Output: `{"error": "no snapshot base go1.25.0.json under /home/vgpnk/.local/opt/go-1.25.0", "status": "unparseable"}`
- The correct value is `$G`. It is discoverable only from `REV:.ufo/waves/round-17/final-recheck/invocation-audit-final.receipt.json.stdout:110` or from the frozen `snapshot_file`.

**(b) The keys are compared against the wrong file.**
- The recheck says to compare `predicted_failure_kind_h1` / `predicted_*_reads_h1` with `predictions/<label>.prediction.json`.
  - `grep -c predicted_failure_kind_h1 predictions/s1246-swiss-nethttp.prediction.json` → `0`, exit **1**.
  - `grep -c predicted_failure_kind_h1 predictions/swiss-misread/s1246-swiss-nethttp.json` → `1`, exit 0.
- `.prediction.json` holds the same facts under different names: `c3.h1_kind` and `extra_expectations.*`.

**Smallest correction.** Define `GOLANG_DIR=$G`. Point the comparison at `predictions/swiss-misread/<label>.json`. With both fixes, all 15 labels re-derive with zero differing keys.

### F5 — The synthetic nethttp carriers do not contain `http.Header` (KE:39)

Axis: calibration (accuracy).

**Evidence** [O]
- The emulator's uncommon map types per carrier (Python over `predictions/swiss-misread/<l>.json` `per_type[uncommon]`, exit 0†):

  | Carriers | Named map types |
  |---|---|
  | 4 synthetic nethttp | `*textproto.MIMEHeader`, `*url.Values` (slot 40) only |
  | kimi-webbridge, aether | `*http.Header` as well |

- `carriers/src/nethttp/main.go:2,16` intends all three.
- w1 `ConnC3Prediction.md:12,39` also says two.

[I] The linker likely omitted the `http.Header` descriptor.

**Smallest correction.** Name "two of these (`textproto.MIMEHeader`, `url.Values`)".

### F6 — The KE:80 reason fits only 2 of the 8 labels it covers

Axis: calibration (accuracy).

**Evidence** [O] The frozen `c3` blocks give:

| Labels | uncommon | misread | Why H1 predicts `none` |
|---|---|---|---|
| swiss-methods (×2) | 1 | 1 | `*main.Counts` slot 24 is silent; the KE:80 reason applies |
| swiss-nomethods (×2) | 0 | 0 | No named map. This is the unnamed control, `ConnC3Prediction.md:113` |
| noswiss (×4) | — | 0 | True layout is read |

**Smallest correction.** Split the row, or reword the reason as above.

### F7 — The walk channel "was never used as a prediction" (KE:117-118; also KE:106)

Axis: calibration (accuracy).

**Evidence** [O]
- `swiss-misread.py:1441-1456` appends the walk's first failure into the read lists whenever it is `eof` or `invalid_index`.
- Those lists feed:
  - `predicted_*_reads_h1/_h0`
  - `predicted_failure_kind` (defined `:1468`, called `:1479`)
  - `diagnostic` (`:1531`)
- In the frozen labels this changed no value:
  - aether and s1246-swiss-nethttp: walk equals map path.
  - notesmd-cli and **kimi-webbridge**: walk = `unmapped@8`, which is not merged. Check via the frozen `walk.h1` / `walk.h0` fields (exit 0†).
- kimi-webbridge is therefore a second walk false positive, under both H1 and H0. It is not disclosed; only notesmd-cli is.

**Smallest correction.** "Walk eof/invalid_index first-failures are merged (`swiss-misread.py:1441-1456`); in the 15 frozen labels they equal the map path or are `unmapped` (notesmd-cli, kimi-webbridge) and not merged."

### F8 — The definition of D in KE:60-61 does not match the code

Axis: calibration.

**Evidence** [O]
- KE says "H1 and H0 differ on a logged field".
- The code compares **kinds**: `swiss-misread.py:1531` (`predicted_kind_h1 != predicted_kind_h0`) and `gen-predictions.py:77`.
- The two agree on all 15 labels, because H0 = `none` everywhere.
- They diverge on go1.25.0 `vet`: same kind, different index (F1).

**Smallest correction.** "differ on predicted failure kind".

### F9 — The reason given for Evidence-ID equality is incomplete (KE:88)

Axis: calibration (QUALITY #14/#15).

**Evidence** [O]
- KE says "(same carrier bytes and params)".
- `REV:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:116-122` records that the same bytes gave a different aether ID in r17 pass 1 (`ev_ae9f7086…`), because `string_count` was 29118 instead of 29117.
- Regex over both `analyze.json` files (exit 0†): r18 and r17 pass 2 both record `string_count` **29117**.

**Smallest correction.** Append: "and the same `string_count` 29117; r17 pass 1 (same bytes) had 29118 and a different id".

### F10 — "no failure" sits next to thousands of ERROR lines; synthetic carriers carry DWARF (KE:75-80, 86-87)

Axes: calibration, depth.

**Evidence** [O]
- Command: per-log counts of `grep -c 'ERROR (GoFuncData)'` and `grep -c DWARF`. Exit 0†.
- 11 non-failing synthetic logs contain 5,448–10,240 lines of `ERROR (GoFuncData) Failed to add source file mapping: new entry would overlap entry /DWARF_DEFAULT_COMP_DIR/…`, plus 5.5k–10.4k DWARF lines.
- The 3 real carriers have 0 GoFuncData lines and 3 DWARF lines each.
- `analyzer_errors` counts only ERRORs from components starting `Golang` (`.ufo/waves/round-17/tools/log-extract.py:243-244`).
- The failing D label s1246-swiss-nethttp has **0** GoFuncData lines. Its noswiss sibling has 9,779.
  - [I] The abort skipped function-data markup. This is a corroborating consequence the entry does not claim.

**Smallest correction.**
- Write "no `Golang*` ERROR / `Go analysis failure` line".
- Add to Not examined: "synthetic carriers are unstripped (DWARF); real carriers are not".

### F11 — Provenance timestamps (KE:1)

Axis: calibration. Severity: minor; the ordering still holds.

**Evidence** [O]
- KE says "pushed 16:23:55Z". That is the committer time.
  - `git reflog show --date=iso-strict refs/remotes/origin/main` (exit 0†): `eb6c266 …@{2026-10-20T13:23:57-03:00}: update by push`, i.e. **16:23:57Z**.
- KE says "first run step (16:24:08Z)". That is the `analyze` step.
  - The first recorded step is `inspect-go-binary` at 16:24:07.220Z; `pins_pre` is at 16:24:07.202Z (`runs/calib-aether/receipt.json`).

**Smallest correction.** "pushed 16:23:57Z (remote-tracking reflog), before the first step (16:24:07.2Z)".

### F12 — Floating citation and SOURCES registry gaps

Axis: calibration (provenance).

**(a) KE:12 cites "`SKILL.md` round-17 table, last row" as the INFERENCE record.** [O]
- At REV, `SKILL.md:528` now reads "Round 18: replayed and confirmed…".
- The INFERENCE text exists only at `9011581:SKILL.md:528`.
- Fix: pin it as `9011581:SKILL.md:528`.

**(b) `used-by` omits this entry.** [O]
- `REV:corpus/SOURCES.md` rows S003, S023 and S033 do not list the entry, though it cites them (`grep -c r18-swiss-map-replay` → 0 ×3). S034 and S035 do list it.
- This breaks the `used-by` rule, `/home/vgpnk/Projects/shokunin/CORPUS.md:107`.

**(c) `go1.24.0.json` has no SOURCES row.** [O]
- `grep -c go1.24.0.json` → 0.
- Both held-out confirmations load this snapshot, yet KE:21 attributes it to S023, whose scope is go1.25.0.json.
- [O] `patchverdiffs/go1.24.6.json.diff` contains no map/uncommon edits (`grep -ci maptype` → 0), so not applying it is harmless.

**(d) S033 in the `source:` line has no URL** (CORPUS.md:163-165).

**(e) The determinism citation covers only 8 of the 12 carriers.**
- KE:47-48 cites `CarrierRecipeAudit.md` for 12 builds. The audit covers **8**: 0 `nethttp` mentions, and `:11` says "all 8 carriers".
- The substance still holds. I rebuilt everything once:
  - Command: `T=$(mktemp -d /tmp/ker18-rebuild.XXXXXX) && OUT=$T/bin bash .ufo/waves/round-18/carriers/build.sh`
  - Exit: 0.
  - `diff` against `REV:carriers/SHA256SUMS`: exit 0, 12 lines.
  - All 12 carriers are byte-identical, including the 4 nethttp builds.
- Fix: cite a 12-carrier rebuild.

## Side observation (outside this entry)

[O] The amendment timestamp in `claims.json` is wrong, not the order of events.
- The amendment says `"at": "2026-10-20T13:25:00-03:00 (… before any round-18 REA run)"`.
- That time is after the commit containing it: `eb6c266`, committed 13:23:55-03:00 (`git show eb6c266:.ufo/waves/round-18/claims.json | grep -n 13:25:00` → line 35).
- It is also after the first run start: 13:24:07-03:00 (`run-log.txt:2`).

## Stack shapes (supports the entry; not claimed in it)

[O] From `grep -nE` over the retained logs:
- s1246-swiss-nethttp, lines 408-468. The held-out stack has no GoMapType, GoStructType or GoInterfaceType frame. The chain is:
  1. `GoTypeManager.markupGoTypes:153`
  2. four nested `MarkupSession.markup`
  3. `GoName.getPkgPath:124`
  4. `resolveNameOff:1063`
  5. `getGoName:1074`
  6. `GoName.readStructure:94` → `ensureBounds:302`
- aether and kimi stacks pass through `GoStructType.java:94` and `GoInterfaceType.java:77`.

[I] The read is consistent with H1 in all three. KE:101-106 discusses aether only.

## Tools

No installs or upgrades.

Tools used:
- lane tools under `python3 -I -B`: `receipt-validate.py`, `compare.py`, `swiss-misread.py`, `buildinfo-probe.py`
- the lane `build.sh`, run with the installed go1.24.6/1.25.0 toolchains into /tmp
- `curl`, `git` (read-only), `unzip -p`, `sha256sum`
