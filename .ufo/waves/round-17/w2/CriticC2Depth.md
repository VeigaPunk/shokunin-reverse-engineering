# CriticC2Depth: is the 8-carrier prediction/observation table new depth?

Seat: `KaidokuR17.CriticC2Depth`, an author-side advisory critic. This seat is read-only except for this file. It ran no REA analyze/search/decompile, no Ghidra, and no carrier; scratch files are under `/tmp/c2d`. Installs: none.
Revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`. All paths are relative to `kaidoku-shokunin/`, and `W` = `.ufo/waves/round-17`.
Axes: **depth** and **calibration**.

## Verdict

C2 adds real depth, but most of it is **not in the 8/8 compare tally**. The depth is in:
- the first retained, run-bound provider logs;
- the runtime request echo after a fallback;
- the uncached bootstrap retry seen twice;
- the no-build-info log signature;
- the unpredicted aether EOF.

Of the 40 field comparisons, 36 are reproduced by a naive model that uses only the version string and the `1.15-1.25` constant. The remaining 4 come from two carriers in one route class (`base_only` fallback). A deliberately wrong selector that never falls back to a lower patch diff also scores 40/40. The r16 selector's nontrivial branch, `fallback_diff`, has **zero** runtime observations. The `pro-esbuild-0.27.7` compare cannot fail on a log with no Go lines at all. The knowledge entry's recheck command fails on all 8 receipts, and its second step deletes the retained run it is supposed to compare against.

## Findings

### F1 — HIGH (calibration). The `pro-esbuild-0.27.7` compare passes on an empty or truncated log
- Target: `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:83` ("The hand prediction matched"), and `:47` ("all eight runs: … compare exit 0").
- Counterexample: the retained log is cut just before its first `Reading Go binary info` line (line 63), so the cut log contains zero Go lines.
  ```
  head -n 62 runs/pro-esbuild-0.27.7/logs/rea-ghidra-DjvEp2/ghidra.log > /tmp/c2d/trunc.log
  python3 -I -B tools/log-extract.py --log /tmp/c2d/trunc.log > /tmp/c2d/trunc.obs.json   # extract=0
  python3 -I -B tools/compare.py --prediction predictions/pro-esbuild-0.27.7.prediction.json --observation /tmp/c2d/trunc.obs.json   # compare=0
  → all_match True; untested_version/snapshot_label/missing_bootstrap/snapshot_route/fallback_to all True
  → observation: classification no_go_analysis, bootstrap_attempts 0, analyzer_errors [], go_lines 0
  ```
- Cause:
  - The discriminating expectations sit in `predictions/pro-esbuild-0.27.7.prediction.json` `extra_expectations`: `bootstrap_attempts_at_least: 1` and `analyzer_errors_contain: "unable to get GoRttiMapper"`.
  - `tools/compare.py:39,43` compares only `FIELDS` + `ROUTE_FIELDS`. For this carrier, all five predicted values are null/false/`none`, which is the all-absent state.
  - Sibling `DraftLessonEvidence.md:55-58` reports the unchecked extras. This finding adds the stronger point: the compare that was run cannot fail on a log with no Go analysis.
- Observation: the real log does satisfy the extras. Lines 63 and 68 are `Reading Go binary info`, lines 64 and 69 are `unable to get GoRttiMapper`, and `observation.json` has `bootstrap_attempts: 2`. So the claim is true by inspection, but no tool verifies it.
- Smallest fix: make `compare.py` evaluate `extra_expectations`, or at least `classification != no_go_analysis` and `bootstrap_attempts >= 1`, then re-run compare on the 8 retained observations. Until then, `:83` should read "matched by inspection; compare.py fields are non-discriminating for this route".

### F2 — HIGH (depth/calibration). The r16 selector's `fallback_diff` branch was never exercised; a wrong selector scores 40/40
- Target: decision-table row `knowledge …r17….md:103` ("a lower patch (or the base) was used"), `SKILL.md` round-17 table "Lower patch data used", and C2's claimed comparison against "GoApiSnapshot base/diff selection via r16 selection.py" (`W/claims.json` C2).
- Evidence, from the frozen `selection.status` in the predictions:
  - `pro-aether` = `base_only` 0
  - `pro-notesmd-cli` = `base_only` 0
  - `pro-esbuild-0.21.5` = `exact_diff` 12
  - `calib-esbuild-0.25.12` = `exact_diff` 12
  - The rest are `missing_base` or have no version.
  - No `fallback_diff` row exists. No lower 1.25 diff exists either: `os.listdir(patchverdiffs)` filtered to `go1.25.` gives `[]` for both 1.25.8 and 1.25.14.
- Counterexample model (`python3 -I -B /tmp/c2d/wrongsel.py`): info iff an exact diff exists or patch is 0; otherwise **always** fall back to `X.Y.0`. That contradicts the downward search at `GoApiSnapshot.java:153-156`.
  ```
  N1 wrong-selector (base-only fallback): 40/40
  lower-patch diffs below each fallback request: {'1.25.8': [], '1.25.14': []}
  ```
- Host scan: a read-only `\xff Go buildinf:` header scan of `/usr/bin`, `~/.local/bin`, `~/go/bin` and the kimi-code pnpm esbuild dirs found 26 Go binaries. None is a `fallback_diff` candidate (1.24.≥7, or any patch above the installed diff maximum). This agrees with w1 `CriticC2Novelty.md` N3. The gap is therefore a sampling limit, not a selection error. It is still undisclosed: `grep -n "fallback_diff|base_only|lower patch"` on the knowledge entry finds only `:103`.
- Smallest fix:
  - Qualify `:103` as "observed only as base fallback (1.25.x → 1.25.0); lower-patch-diff fallback (r16 `fallback_diff`, e.g. 1.24.7→1.24.6) is source-only, no runtime observation".
  - Add one line to "Not examined" (`:122-133`).
  - Qualify row `:102` "or patch 0" the same way, because no `X.Y.0` carrier was run.

### F3 — MEDIUM (depth). The 8/8 tally overstates independent tests; 36/40 matches need no selector
- Target: `SKILL.md:515` ("Eight of eight matched, including six prospective carriers"), `LOG.md:2047`, and `corpus/lessons/round-17.md:26`.
- Naive baseline N0 (`python3 -I -B /tmp/c2d/naive.py`): `untested` iff the minor is outside 15..25; `missing_bootstrap` iff untested; route `info` if in range, else `none`; no fallback.
  ```
  N0 naive baseline: 36/40 field matches; predictor: 40/40
  N0 miss ('pro-aether', 'snapshot_route', 'info', 'fallback')
  N0 miss ('pro-aether', 'fallback_to', None, ['1.25.0'])
  N0 miss ('pro-notesmd-cli', 'snapshot_route', 'info', 'fallback')
  N0 miss ('pro-notesmd-cli', 'fallback_to', None, ['1.25.0'])
  ```
- Per-field classification:
  - `snapshot_label` is tautological by construction. It is honestly labelled in the `compare.json` rules ("non-discriminating: request echo").
  - `untested_version` is tautological. It is the same `GoVer.parse` plus range test on the same string (`GoRttiMapper.java:170-171`). Its only non-trivial input, the `-X:nodwarf5` suffix, was already pilot-observed (w1 `CriticC2Novelty.md` V2).
  - `missing_bootstrap` is collinear with `untested_version` on this host. The knowledge entry itself admits this at `:111-113`, yet the tally counts both fields.
  - Discriminating rows: `snapshot_route` and `fallback_to` on 2 carriers.
- Per-row ledger (O = observed; prior = the earlier corpus row that already predicted it):

  | row | role | route class | already predicted in corpus | beats N0? | new depth |
  |---|---|---|---|---|---|
  | calib-shfmt | calibration | missing_base | r14 `:75,77`; pilot log | no | none (pilot repeat) |
  | calib-esbuild-0.25.12 | calibration | exact_diff | pilot log | no | none (pilot repeat; ID repeat `:92-96`) |
  | pro-notesmd-cli | prospective | base_only fallback | r16 class row `1.25.7 base_only` (`r16…md:71`), source only | **yes** | first runtime fallback WARN plus request echo (O) |
  | pro-aether | prospective | base_only fallback | same class | **yes** (same class) | unpredicted EOF after bootstrap (O) |
  | pro-esbuild-0.21.5 | prospective | exact_diff | same class as calib-esbuild | no | replicate |
  | pro-containerd-shim | prospective | missing_base, `X:` suffix | same class and suffix as calib-shfmt | no | replicate |
  | pro-op | prospective | missing_base 1.26.8 | literal r16 row `1.26.8 … missing_base` (`r16…md:72`) | no | replicate (correctly not cited as r4-10, `:117-120`) |
  | pro-esbuild-0.27.7 | prospective, hand | no build info | new | n/a | new route signature (O); compare vacuous (F1) |

- Net: six prospective carriers make **two** independent new route-class tests. One of them (no build info) is not machine-checked.
- Smallest fix: qualify `SKILL.md:515` as "8/8 matched; 4 of 40 field matches discriminate beyond the version/range constant (two 1.25.x base fallbacks); `fallback_diff` unobserved". The knowledge entry's honesty note at `:37-40` is accurate about calibration versus prospective but silent on this.

### F4 — HIGH (calibration). The knowledge recheck fails on every receipt, and its second step destroys the comparand
- Target: `knowledge …r17….md:3` and the SKILL `go-carrier-run` row (`SKILL.md:532`).
- (a) `receipt-validate.py` rejects all 8 retained receipts:
  ```
  for l in runs/*/; do python3 -I -B tools/receipt-validate.py $l/receipt.json; done  → rv=1 ×8
  findings: [{"code":"unrecognized_shape","detail":"receipt matches neither retain nor carrier shape","where":"$"}]
  ```
  - Cause: `tools/receipt-validate.py:98-101` requires `steps` to be a list, but `carrier-run.py` writes a dict keyed `inspect-go-binary` / `analyze`.
  - This blocks the C2 capability condition "+1 only if … its receipt validates" (`W/claims.json` C2; `corpus/lessons/round-17.md:17-18`).
  - Siblings `DraftLessonEvidence.md:25` and `RunProaether.md:19` report the same failure. Listed here because it makes `:3` false as written.
- (b) `W/run-carriers.sh` does `rm -rf "$out"` with `out="${RUNS_DIR:-runs}/$label"`. Following `:3` literally ("rerun one carrier with `bash …/run-carriers.sh <label>` and compare `observation.json` fields") deletes the retained `runs/<label>` first. The comparison then reads the new run against itself.
- Smallest fix:
  - Make `receipt-validate` accept dict `steps`, re-run it on all 8 receipts, and retain the outputs.
  - Change `:3` and `SKILL.md:532` to `RUNS_DIR=/tmp/<dir> bash …/run-carriers.sh <label>`, then diff `/tmp/<dir>/<label>/observation.json` against `runs/<label>/observation.json`.

### F5 — LOW (depth, cheap gain). An in-sample control already bounds the aether EOF; the knowledge entry does not use it
- Target: `knowledge …r17….md:84-91` ("Cause: **UNKNOWN**. This run does not show that the 1.25.0 fallback data caused it.")
- Observation: `pro-notesmd-cli` took the **same** fallback (`Falling back from 1.25.8 to 1.25.0`, log line 68). Symbol markup then completed: log lines 77-78 `Fixed 1657 … / Fixed 761 Go function signatures`, line 82 `RTTI callsite fixup … 2253/2210/3`, and no `Go analysis failure`. So 1.25.0 fallback data is **not sufficient** for the failure on every 1.25.x carrier. A patch-specific (1.25.8 vs 1.25.14) or carrier-specific cause stays open.
- Observation: `MemoryByteProvider.java:310-312` formats `Unable to read past EOF: <index>, <length>`. The aether request length is 111,938,854 bytes; `stat` gives the carrier as 20,694,888 bytes, so the request is 5.4× the whole file.
- INFERENCE: the length is a mis-decoded field rather than a short section.
- Smallest fix: add one OBSERVATION sentence citing notesmd log lines 68 and 77-82. Optionally add the length-versus-file-size fact as INFERENCE.

### F6 — LOW (calibration). The "every 30 s during" pin checks leave no positive record
- Target: `knowledge …r17….md:26-30` ("hashed … every 30 s during … no mid-run check differed").
- Observation: `tools/carrier-run.py:422-433` writes `pins_changed_during_run` only when a check differs. The number of mid-run checks and their times are never recorded. `receipt.json` keys contain no `mid` or `during` key in any of the 8 receipts.
- `last_pin_check = 0.0` (`:412`) makes the first check fire immediately. Analyze durations: shfmt 30.6 s, notesmd 38.1 s, op 248.8 s.
- "No mid-run check differed" is therefore evidenced only by an absent key.
- Smallest fix: record `pin_checks: [{taken_at_utc, equal}]`, or reword `:28-29` to "mid-run checks record only differences; none recorded".

### F7 — LOW (provenance). `runs/run-log.txt` omits `calib-shfmt`
- Observation: the committed `runs/run-log.txt` (`git show da64646:…/run-log.txt | head -2`) starts at `calib-esbuild-0.25.12 start 10:47:42-03:00`. `runs/calib-shfmt/receipt.json` shows `pins_pre` at 13:47:05Z and analyze ending at 13:47:37Z, 5 s before the esbuild start.
- The receipt and the `.exit` files (`0` / `0`) exist, so the run is evidenced, but the runner log is incomplete.
- Fix: add a note that the first label is absent from `run-log.txt`; the receipt is authoritative.

## Bounded no-findings (checked, held)
- **Freeze integrity:**
  - Predictions were committed at `2716747` (10:46:45-03 = 13:46:45Z), before the first run (13:47:05Z).
  - `git diff --stat 2716747 da64646` over `predictions/` and `tools/` shows no changes to predictions, `compare.py`, `log-extract.py` or `predict.py`.
  - `sha256sum -c predictions/SHA256SUMS`: all OK.
- **No pre-freeze observation of the `pro-*` carriers:** `grep -rn` of `w1`/`pilot` finds `Falling back from 1.25.(8|14)` only as source predictions (`CriticC2Novelty`, `CriticSampleSize`, `CriticC2Confound`). There is no analyze of any `pro-*` carrier and no matching type or string counts.
- **Table cells against logs:**
  - fallback WARN plus request echo: notesmd 68-69, aether 92-93;
  - INFO on exact diff: 0.21.5 lines 62-63, 0.25.12 lines 63-64;
  - untested plus missing bootstrap ×2: shfmt, containerd, op;
  - 0.27.7 lines 63 and 68;
  - type counts 4881/2302/6115/4411; aether strings 7200.

  All match the retained logs. The analyze evidence IDs for `calib-*` equal the pilot IDs (`pilot/shfmt.json`, `pilot/esb.json`).
- **Source anchors**, re-read from `Base-src.zip`: `GoRttiMapper.java:79,170-172,179-180`; `GoApiSnapshot.java:122-126,153-164`; `GoBuildInfo.java:488-489`; `GoVer.java:62-81`; `TransientProgramProperties.java:107-110`. All say what the entry claims.
- **Honesty that held:**
  - Calibration versus prospective is stated (`:37-40`).
  - aether's cause stays UNKNOWN.
  - op is not cited as r4-10 (`:117-120`).
  - The range/base confound is labelled INFERENCE (`:111-116`).
  - The lessons reject the general "8/8 proves predictor" reading (`round-17.md:36`).

## Commands run (all read-only; scratch in /tmp/c2d)
- `log-extract.py` and `compare.py` (round-17 tools) on a truncated copy of a retained log.
- `/tmp/c2d/naive.py` and `/tmp/c2d/wrongsel.py`: stdlib scoring of the retained `compare.json` files.
- `/tmp/c2d/scan.py`: build-info header byte reads; no execution.
- `receipt-validate.py` on the 8 receipts.
- `unzip -p` of the Base-src members.
- `git show`/`diff`/`log`, `sha256sum -c`, `stat`.
