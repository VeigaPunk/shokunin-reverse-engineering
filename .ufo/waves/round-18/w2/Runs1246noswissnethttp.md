HOLDS

# w2 · Runs1246noswissnethttp: independent re-derivation of `s1246-noswiss-nethttp`

Seat: author-side advisory leaf, read-only. I wrote only this file. Lane REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (`git rev-parse HEAD` returned it, exit 0). Freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Paths are relative to `kaidoku-shokunin/` unless absolute.
Aliases:
- `L` = `REV:.ufo/waves/round-18/runs/s1246-noswiss-nethttp/logs/rea-ghidra-PBi1r9/ghidra.log` (10242 lines). The REV blob sha256 is `14c01725…eee1`. It is byte-identical to the worktree file, and `git status --porcelain --untracked-files=all` on the run dir is empty.
- `R` = `REV:…/s1246-noswiss-nethttp/receipt.json`.
- `P` = `eb6c266:.ufo/waves/round-18/predictions/s1246-noswiss-nethttp.prediction.json`. Its blob sha256 is `e1cfd424…746f` at both freeze and REV, matching `REV:predictions/SHA256SUMS:7`.

## Per-field verdict (raw lines vs frozen P)

| Field (P line) | Frozen | Raw-log observation | Verdict |
|---|---|---|---|
| `snapshot_route` (P:34) | `info` | The only GoApiSnapshot record in L is L:182 `INFO (GoApiSnapshot) Using Go API snapshot for 1.24.6`. There is no `Falling back` WARN. Source: this INFO fires only when the diff for the exact patch exists (`GoApiSnapshot.java:153-163`). `go1.24.6.json.diff` is on disk with sha `e169e8dd…` = P `selected_diff`. | HOLDS |
| `snapshot_label` (P:33) | `1.24.6` | L:182; corroborated by L:183 (GoRttiMapper) and L:408 (`Go version 1.24.6`) | HOLDS (label is a request echo, non-discriminating) |
| `untested_version` (P:35) | null | No `Untested Go version` anywhere. 1.24.6 is inside `SUPPORTED_VERSIONS "1.15-1.25"` (`GoRttiMapper.java:79,170-171`). | HOLDS |
| `fallback_to` (P:31) | null | No fallback line | HOLDS |
| `missing_bootstrap` (P:32) | false | No `bootstrap` substring in L (case-insensitive). L:181 `Reading Go binary info` ×1. | HOLDS |
| `analyzer_errors_empty` (P:38) | true | 0 ERROR records from a `Golang*` component. Caveat F2: 9779 `ERROR (GoFuncData)` records exist. | HOLDS under the frozen law (`log-extract.py:243-244`) |
| `eof_reads` (P:39) | `[]` | 0 `Unable to read past EOF:`, 0 `past EOF`/`EOFException`, `grep -c -i eof` = 0 | HOLDS |
| `invalid_index_reads` (P:40) | `[]` | 0 `Invalid index` (any case, unanchored) | HOLDS |
| `Go analysis failure` (C3 kind; P:19-20 `h0/h1_kind none`; `REV:predictions/decision-rule.json:150-160`) | none | 0 occurrences. Structural proof follows this table. | HOLDS |

Structural proof for the last row:
- L:10195-10197 are the three `scheduling …` INFO lines. They are emitted inside the `try` at `GolangSymbolAnalyzer.java:164-175`, after every throwing call (`:145-161`). The `catch` at `:181-182` therefore did not run on this pass.
- A re-entry is short-circuited by `:113-121`.
- Further evidence that the Go pass reached function markup (`:155` → `:256-259` → `GoFuncData.java:426-427`): the 9779 GoFuncData records. The failing swiss sibling has 0.

C3 role: this label is the noswiss sibling of held-out D label `s1246-swiss-nethttp`. It meets the `decision-rule.json:7` clause "every noswiss sibling … shows no Go analysis failure". It does not trigger `:19` "any noswiss synthetic label fails".

## Binding and carrier (decision-rule.json:2 gate): HOLDS
- **Session path.** L:2 `Using log file: /tmp/kr17-rea-j66kd__i/rea-ghidra-PBi1r9/ghidra.log` is consistent with all of:
  - R:2-3 `bound_sessions`
  - R:1911 and R:1969 `session_dir`
  - the retained dir name `rea-ghidra-PBi1r9`
  - R:1998 `unbound_sessions: []`
  - R:1916 `session_parent_leftovers: []`

  The /tmp dir is gone now (`ls` → No such file).
- **target-sha12.** L:46/65/175/181/10236/10242 all name `target-62f7581ceb06.bin`, which is the first 12 hex of the carrier sha256.
- **MD5.** L:65 `?MD5=f27441e4f726fa863312aaa9f2c253ce` matches my `md5sum` of the carrier and R:6 `md5_pre`.
- **Carrier sha256.** My recomputed `62f7581c…4332d` matches:
  - P:28
  - R:8-9 (pre = post)
  - `~/.local/share/kaidoku-r18/carriers/SHA256SUMS` (`sha256sum -c`: 12/12 OK)
  - `REV:.ufo/waves/round-18/carriers/SHA256SUMS:2`

  The build info bytes at file offset 2953249 read `go1.24.6 X:noswissmap` (Python byte read; the carrier was not executed).
- **Validator.** It re-derives L:2/46/65 line-anchored (`receipt-validate.py:131-192`) → R:1893-1895 all true.
- **Validator has teeth on this receipt.** In-memory mutations of R:
  - unmodified → valid
  - log path → swiss-sibling log → `binding_mismatch` (all three false), `sha256_mismatch`, `size_mismatch`
  - session dir renamed → `binding_mismatch`
  - carrier sha → sibling → `binding_mismatch`, `carrier_not_pinned`, `sha256_mismatch`
- **Mid maps.** sha256 of `pins/mid-1.json` = `0d1ac1a4…` (R:1938) and of `pins/mid-2.json` = `e20b01c0…` (R:1947). Both have `equal: true`. R:25 `mid_run_drift_steps: []`.

## Reproducibility (observation)
- `log-extract.py --log L` → output is byte-identical to `observation.json` (`cmp` exit 0).
- `compare.py` → byte-identical to `compare.json`. Against the frozen blob via `/dev/fd`, the only diff is the `prediction` path line.
- `swiss-misread.py --carrier … --debug` → JSON equals the frozen `predictions/swiss-misread/s1246-noswiss-nethttp.json` (`828e0bff…` = `SHA256SUMS:22`).
- Tool sha256 at FREEZE = REV = worktree = R `pins_pre`, for:
  - carrier-run `6665dc7a`
  - pins `9e9c7250`
  - log-extract `eb8f2c78`
  - compare `582a77f3`
  - receipt-validate `70672eb3`
  - swiss-misread `14924bd6`
  - selection `6917da09`
- `git diff --stat eb6c266 b2aad08 -- predictions/ round-17/tools/ round-18/tools/ round-16/selection.py` → only `round-18/tools/routed-defects.py` changed.

## Findings
**F1 · Low · emulator gap scan never fires (does not change any outcome).**
- Observation: `REV:.ufo/waves/round-18/tools/swiss-misread.py:1233-1237` tests the raw GoName against `startswith("struct { ")`. `read_go_name` (`:782-811`) does not strip ExtraStar. All 39 closure-struct names in the carrier are raw `*struct { F uintptr; …` (byte scan: 39/39 preceded by `*`).
- Ghidra strips that `*` (`GoBaseType.java:116-118`; `GoTypeFlag.java:30` ExtraStar = 1<<1) before `isAnonType` (`GoSymbolName.java:237-238`).
- Frozen `walk.unindexed_types` = 0 / indexed 1629. Ghidra logs L:184 `Discovered 39 unindexed Go types` and L:185 `Found 1668`.
- Counterfactual, in memory only: changing that one token to `name.lstrip("*")` gives 39 / 1668, exactly matching L:184-185. It also matches Ghidra's logged counts on all 15 round-18 labels (188/56/195/10×4/39×2/9×4/34×2).
- `predicted_failure_kind_h0/h1`, `invalid_index_reads_h1` and `eof_reads_h1` are unchanged on all 15 labels. This label stays none/none.
- Consequence: the module docstring claim (`:17-18`) that it runs "the unindexed-closure gap scan" overstates fidelity. No verdict changes.
- Repro: run the counterfactual block below.

**F2 · Info · the `analyzer_errors` law is narrower than its name.**
- L has 9843 ERROR records: 9779 `(GoFuncData) Failed to add source file mapping …`, 59 DWARFImportSummary, 5 DWARFDataTypeImporter.
- The GoFuncData records come from inside the Go symbol pass and are caught as non-fatal (`GoFuncData.java:426-427`).
- `log-extract.py:243-244` counts only ERROR records from components starting with `Golang`, so the field is empty.
- The docstring at `log-extract.py:17-18` ("starts with `Go`/`Golang`") disagrees with the code at `:122-130`. That drift already exists at baseline `9011581` (:17 vs :58,:108), so it predates round 18.
- Repro: `grep -c 'ERROR (GoFuncData)' <L>` → 9779.

## Residual risk / gaps
- **Captured log is a prefix.** Polling stopped at L:10242 `ANALYZING changes made by post scripts`. All 15 round-18 logs end on that same line, and R:24 admits it. The absence of `Go analysis failure` is proven structurally (see above). The absence of EOF / `Invalid index` lines is shown only for the captured prefix. [INFERENCE] Post-script analysis is unlikely to add them.
- Ghidra was not re-run (forbidden). Every field is derived from the retained log plus Base-src.zip source reads (`unzip -p`).
- F1 approximates `ExtraStar.isSet(tflag)` with `lstrip("*")`.
- I created one scratch file, `/dev/shm/kr18-w2-r1246nn-obs.json` (log-extract output for `cmp`), and deleted it. The emulator and validator experiments ran in memory, under `-B`. Lane status is clean.
- No installs or upgrades (python3, git, grep and unzip were already present).

## Commands (exit codes)
```
git rev-parse HEAD                                                     # b2aad08c…; 0
git show eb6c266…:.ufo/waves/round-18/predictions/s1246-noswiss-nethttp.prediction.json   # 0
grep -n "Using Go API snapshot" <L>                                    # 182 (GoApiSnapshot INFO), 183; 0
grep -n "Go analysis failure\|Invalid index:\|Unable to read past EOF:" <L>   # no output; 1
grep -n "GoApiSnapshot\|GoRttiMapper\|Untested\|bootstrap\|Bootstrap\|fallback\|Fallback" <L>  # 181,182,183,10202 only; 0
grep -c -i "eof" <L>                                                   # 0; 1
python3 -I -B - (own regex parse of L)   # GoApiSnapshot [(182,'INFO',…1.24.6)]; fallback/untested/bootstrap/failure/invalid_index/eof = []; ERROR: GoFuncData 9779, DWARFImportSummary 59, DWARFDataTypeImporter 5; WARN GoTypeManager 4; 0
sha256sum <carrier>; md5sum <carrier>                                  # 62f7581c…4332d / f27441e4…53ce; 0 / 0
(cd ~/.local/share/kaidoku-r18/carriers && sha256sum -c SHA256SUMS)    # 12 OK; 0
git show REV:<L> | sha256sum                                           # 14c01725…eee1
git status --porcelain -- .ufo/waves/round-18/runs/s1246-noswiss-nethttp/   # empty; 0
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/runs/s1246-noswiss-nethttp/receipt.json
                                                                       # valid 1/1, findings [], checks_performed 366; 0
python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log <abs L> > /dev/shm/…; cmp … observation.json   # 0 / 0
python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction <lane P> --observation <obs> | cmp - compare.json  # 0 0
diff <(compare.py --prediction <(git show eb6c266:P) …) compare.json   # only "prediction" path line; 1
git diff --stat eb6c266 b2aad08 -- .ufo/waves/round-18/predictions/   # empty; 0
python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier <carrier> --golang-root <ghidra>/…/typeinfo/golang --debug
                                                                       # 0; == frozen JSON; "DEBUG h1 index 1629 / unindexed 0"
python3 -I -B - (exec swiss-misread.py source in memory with gap-scan test → name.lstrip("*").startswith("struct { "))
                                                                       # "DEBUG h1 index 1668 / unindexed 39"; kinds none/none; 15-label table unchanged; 0
grep -H "Discovered .* unindexed Go types" .ufo/waves/round-18/runs/*/logs/*/ghidra.log   # 188,56,195,10,39,10,10,39,10,9,34,9,9,34,9; 0
python3 -I -B - (importlib receipt-validate.validate_receipt on deep-copied R; M0-M3)    # M0 valid; M1/M2/M3 binding_mismatch; 0
unzip -p <ghidra>/Ghidra/Features/Base/lib/Base-src.zip <member> | cat -n | sed -n …   # GoApiSnapshot/GolangSymbolAnalyzer/GoRttiMapper/GoTypeManager/GoBaseType/GoSymbolName/GoFuncData; 0
```
