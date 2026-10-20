PARTIAL

# SimplifyR17Edits: YAGNI review of the in-place round-17 tool edits (B→REV)

Seat: KaidokuR18.SimplifyR17Edits (simplifier, author-side advisory, read-only). B = `9011581d84527ba34c675f9cf912e54d2e72d470`, REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, F = `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Scope: `git diff B REV -- .ufo/waves/round-17/tools/`, which touches 4 files (+614/−14). Every `path:line` below is a `git show REV:<path>` line. The lane has HEAD = refs/heads/main = REV and the scoped worktree is clean, so the worktree bytes are the REV bytes.

**Question:** is any branch added B→REV left unexercised by both its selftest and every run?
**Answer:** yes, in 2 of the 4 files.
- `compare.py` and `log-extract.py` hold: no added production line goes unexecuted.
- `receipt-validate.py` has 12 branch arms (37 lines) that no selftest and no run reaches.
- `carrier-run.py` has 1 such branch (2 lines).

Of the unexercised arms, five are redundant, plus one redundant token in compare.py. These are deletion candidates D1–D5. Each remaining arm is the only finding for its failure shape, so it needs a red selftest, not deletion.

## 1. Coverage (observation)
**Method.** I traced each tool's own selftest line by line with stdlib `trace`, in process (harness `/tmp/cov_lines.py`). compare.py's selftest shells out to itself for every case, so those calls are routed back in process.

**Runs.** For receipt-validate.py I added real-input CLI runs, also traced (`/tmp/cov_cli.py`): 15 r18 receipts with `--require-mid-maps`, and 8 r17 receipts both with and without the flag. For carrier-run.py the run evidence is the 15 retained REV receipts, because the REA runs cannot be replayed here.

| tool | + lines | added executable | not executed by selftest | not executed by selftest ∪ runs |
|---|---|---|---|---|
| carrier-run.py | 76 | 54 | 513, 516 (+715, the selftest failure arm) | 513, 516. Runs: 22/22 `pin_checks` carry `map_path`+`map_sha256`, 0 carry `map_error` |
| compare.py | 59 | 54 | 0 | 0 (one sub-line arm, D5) |
| log-extract.py | 173 | 69 | no production lines (113-115 run at import; 521/545/572/596/617 are selftest `return False, err` arms) | 0 |
| receipt-validate.py | 306 | 243 | 41 (not counting def lines 453/589/617) | 37. CLI lines 1020-1021 and 1038-1039 are reached only by the real-input runs |

The runs used the REV tool bytes:
- `git diff --stat F REV -- .ufo/waves/round-17/tools/` is empty.
- 15/15 `runs/*/producer.json` `tool_sha256` values equal the REV blobs for all four tools.

## 2. Added branches never exercised (trace = observation; classification = repro on a /tmp copy of `runs/calib-notesmd-cli`, `/tmp/repro_dup.py` variants V0–V10)
V0 is the unmodified copy: 0 findings with and without the flag. The table covers the `receipt-validate.py` function `verify_mid_maps`.

| unexecuted REV lines (exact trace output) | arm | only finding for its shape? | class |
|---|---|---|---|
| 475, 478 | skip a non-dict step / check | crash guard; check_binding :194-195 skips non-dict steps and :201-203 flags non-dict checks | keep |
| 490-492 | `mid_map_write_error` | yes without the flag (V7: n=1; with the flag, +`mid_map_missing`) | keep, untested |
| 503-506 | `mid_map_incomplete` | yes (V8: sha absent gives n=1; `walk_pairs` needs both values to be str) | keep, untested |
| 509-511 | `mid_map_missing` (file gone) | **no**: the generic `missing_file` at `…pin_checks[0].map` fires too (V2) | D1 |
| 527-530 | `mid_map_unparseable` (non-object) | yes (V9: n=1) | keep, untested |
| 534-537 | `mid_map_taken_at_mismatch` | yes (V6: re-dated map with a consistent digest gives n=1) | keep, untested |
| 541-544 | `mid_map_entries_mismatch` | **no**: fires together with `mid_map_compare_mismatch` (V3) or `mid_run_pin_drift` (V4) | D2 |
| 546-549 | `mid_map_no_pre` | **no**: fires together with `missing_field $.pins_pre/pins_post` (V5) | D3 |
| 553-557 | `pins_compare_error` | yes (V10: `entries="junk"` gives n=1) | keep, untested |
| 576-578 | flag with list-shaped `steps` | nothing produces list-shaped steps | D4 |
| 580 | flag with `steps` neither dict nor list | fail-closed default | keep |

**carrier-run.py:513-516** (`except OSError` → `map_error`). The repro (`/tmp/repro_unexercised.py`) makes `out_dir/pins` a regular file, so `os.makedirs` raises FileExistsError. Result: `map_error` is recorded, no `map_path` is written, and carrier-run **exits 0**. The failure is caught only downstream, by receipt-validate's `mid_map_write_error` (V7). The branch is unique and needed, but no test covers it.

## 3. Deletion candidates (none made; this seat is read-only)
- **D1** receipt-validate.py:509-510 (keep the `continue` at :511, because `sha256_file` at :512 would raise on a missing file). The finding duplicates `walk_pairs`:
  - its `<stem>_path`/`<stem>_sha256` convention at :316-326 covers `map_path`/`map_sha256`;
  - PIN_KEYS at :84 skips only `pins_pre`/`pins_post`, so `pin_checks` entries are walked;
  - `verify_file` then reports `missing_file` (:216-224). Shown by V2.
- **D2** receipt-validate.py:538-544. Why it is redundant (INFERENCE by case analysis, illustrated by V3/V4): let e = recorded entries, N = |pins_pre.entries|, m = |map.entries|.
  - If e≠N, `mid_entries_mismatch` (:483-488) fires.
  - If e=N≠m, the key sets differ, so `pins.compare` returns missing≠[] and equal=false.
  - Then a recorded equal=true trips `mid_map_compare_mismatch`, and any other recorded value trips `mid_run_pin_drift` (:201-203).
  - So the receipt's validity never depends on D2.
- **D3** receipt-validate.py:546-548 (keep the skip at :549). `rerun_pins_compare` runs under the same `pins is not None` guard (:597-600) and already flags an absent `pins_pre` (:414-419). Shown by V5.
- **D4** receipt-validate.py:576-578. Nothing produces list-shaped steps:
  - carrier-run writes dict steps (:313, :353);
  - all 15 REV receipts have dict steps;
  - the only tracked JSON at REV with `"steps": [` is `evidence/jj-red-before.json`, which is not a receipt.
  - The list arm also follows a second rule: it accepts *any* step with checks, while the dict arm requires `analyze` to have them. After deletion, the fail-closed `else` (:579-580) remains. The verdict would change only for list-shaped receipts that carry `pin_checks`, and no producer emits those.
- **D5** compare.py:205: the `isinstance(extra["analyzer_errors_empty"], bool) and` token. The `is` test at :206 already compares against the bool singletons, so the guard adds nothing: 0 of 24 cases differ (`/tmp/repro_small.py` (a): 12 JSON values × both error-list states). All 15 frozen predictions use bools, so the guarded arm never runs.

**Tradeoff for D1–D3 and D5:** the receipt verdict is unchanged on every reproduced shape. What is lost is the mid-map-specific diagnostic name.

## 4. Duplicates pinned elsewhere (stop here: deleting them would harm an axis)
- **S1** receipt-validate.py:512-517 `mid_map_sha256_mismatch` duplicates the generic `sha256_mismatch` at `…pin_checks[0].map` (V1), and the tool's own docstring (:467-469) says so.
  - It *is* exercised, by selftest case 4e.
  - It is pinned by `round-18/tools/routed-defects.py:282-283`, which runs `all(n in code for n in need)` over non-comment code as part of the C1 R17-PINMAP substance check. Deleting S1 would reopen that C1 defect.
  - INFERENCE: that check only tests that the identifier exists, not that the behaviour happens.
- **S2** log-extract.py `symbol_analysis_failures` (:172, :198-199, :303).
  - It is exercised: by the selftest, and it is non-empty in 3 runs.
  - No program consumes it at REV: `git grep` over `*.py`/`*.sh` finds only task text in gen-wave1.py:97.
  - In 15/15 observations it equals `[e for e in analyzer_errors if "Go analysis failure" in e]`. Analyzer errors are collected at :243-244, and the decision rule reads `analyzer_errors`.
  - It is required by contract.md:123-125, so stop.

## 5. Not dead (correcting my own first suspicion)
carrier-run.py:445 `mid_map_counter=None` and the guard at :499 look unused, because the only call inside the tool passes the counter (:377-378). But the retained historical script `round-17/w2/stopgroup-attack.py:126-128` calls `_run_polled` without it. `/tmp/repro_small.py` (b) uses that exact call shape: 1 pin check with keys {changed, entries, equal, missing, taken_at_utc}, no `pins/` directory, exit 0. The default keeps that script rerunnable, so keep it.

The caller check is a literal `git grep`, not semantic: reading `xd://lsp` returned "No such tool", so no LSP was available.

## 6. Leftovers from the in-place edits (observation)
- log-extract.py:20-35: the round-18 paragraph was inserted mid-sentence. At B, lines 19-21 read as one sentence; at REV it is split across :20-21, the inserted paragraph :23-34, and :35. Check with `git show B:.ufo/waves/round-17/tools/log-extract.py | sed -n 19,21p` against `git show REV:… | sed -n 20,35p`.
- log-extract.py:10-15: the "Emits JSON" key list leaves out `invalid_index_reads`, which the tool emits at :302.

## 7. Adjacent operability gap
The selftest never reaches `--require-mid-maps` (receipt-validate.py:1020-1021, 1038-1039), because it calls `validate_paths(…, require_mid_maps=True)` directly. `round-18/verify.py:201` runs receipt-validate without the flag, although `predictions/decision-rule.json:2` says the binding gate requires it. My runs reproduce the claims in w1/CarrierRunMidMaps.md:166, LOG.md:2148-2149 and corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:68:

| receipts | flag | exit | findings |
|---|---|---|---|
| 15 r18 | yes | 0 | valid 15/15, 0 findings (input: 22 map-bearing `pin_checks`) |
| 8 r17 | yes | 1 | `mid_map_missing` ×8 |
| 8 r17 | no | 0 | none |

## Commands (exit codes observed)
REV tool bytes were extracted with `git archive REV .ufo/waves/round-17/tools/ | tar -x -C /tmp/revtools` (exit 0). In the list below, T = `/tmp/revtools/.ufo/waves/round-17/tools`.
1. `git diff --stat B REV -- .ufo/waves/round-17/tools/` → 0
2. `git diff --stat F REV -- .ufo/waves/round-17/tools/` → 0 (empty)
3. Selftests in T, each `python3 -I -B <tool> --selftest` → 0:
   - compare.py: `cases=23`
   - log-extract.py: `cases=13`
   - receipt-validate.py: `cases=18`
   - carrier-run.py: `cases=3`
4. `python3 -I -B /tmp/cov_lines.py T/<tool>.py /tmp/cov/<tool>.json`, run for each of the 4 tools → 0. Each reports selftest CLEAN, except log-extract, whose `_selftest` returns `(True, 13)`.
5. `python3 -I -B /tmp/unexercised_added.py` → 0 (selftest-only column of §1)
6. `python3 -I -B /tmp/cov_cli.py T/receipt-validate.py /tmp/cov/rv-cli-r18-flag.json -- --require-mid-maps $(git ls-tree -r --name-only REV .ufo/waves/round-18/runs/ | grep /receipt.json$)` → wrapper 0, tool exit 0
7. The same with the 8 r17 receipts (`.ufo/waves/round-17/runs/`), once with the flag (tool exit 1) and once without (tool exit 0) → wrapper 0 both times
8. `python3 -I -B /tmp/unexercised_union.py` → 0 (37 lines never exercised; 4 lines reached by CLI runs only)
9. `python3 -I -B /tmp/repro_dup.py` → 0 (V0–V10 as cited)
10. `python3 -I -B /tmp/repro_small.py` → 0 ((a) 0/24 differences; (b) None arm)
11. `python3 -I -B /tmp/repro_unexercised.py` → 0, 13/13 branches reached
12. Inline python over `git show REV:` receipts/producers/observations → 0 each:
    - 15 receipts, all with dict steps; 22 pin_checks; 0 `map_error`
    - 15/15 producer hashes equal the REV blobs
    - 15/15 `symbol_analysis_failures` equal the filtered `analyzer_errors`
13. `git grep -n "_run_polled\|mid_map_counter" REV -- . ':!*.md'` → 0; `git grep -l -E '"steps": *\[' REV -- '*.json'` → 0 (only jj-red-before.json)

Failed attempts, disclosed (none affects the findings):
- `python3 -m trace --count … carrier-run.py --selftest` → 1. The selftest itself printed `CLEAN cases=3`; trace then crashed writing results for the deleted temp `pins.py`. Replaced by the in-process harness.
- The first run of `/tmp/repro_unexercised.py` → 1, because my `_DoneProc` replica lacked `wait()`. Fixed and rerun → 0.
- `ls .ufo/waves/round-18/runs/*/receipt.json` → 2, because of a non-directory entry `run-log.txt`. Replaced by `git ls-tree`.
- The extra_expectations loop over `git ls-tree F predictions/` → 1, on non-prediction members. All 15 label rows were still printed.

Harness sha256 (all under /tmp):

| script | sha256 |
|---|---|
| cov_lines.py | `0ed46e1269cb31b5dabcf727151d0294684b21d23827028834f9213a4887ffa1` |
| cov_cli.py | `79cad12987d0111522f2eaf44ff399280ae48ebec115cb63a3fd22464851f859` |
| unexercised_added.py | `76d9a1d8f42caa91de5359cd27fb95d9f74c76ea8e43b81519f48114cd11f8e0` |
| unexercised_union.py | `dd29c01f08b89b45dfa7dd1beff20edfb791abc289625ce134347f5a5821e07f` |
| repro_dup.py | `03b9afe4ff7ac5373cf1944605552483ca23067178e5492f38146f5daa753429` |
| repro_small.py | `27bd666a4d7db1dd73f553a96cd0ab3a7467f2a2fc7214441c02ab5bcabfb6c9` |
| repro_unexercised.py | `7c6bfd9e71bf91e12993480650927f378561a4dc51301432bcffda13e09f1202` |

## Hygiene
- **Lane writes:** this report only. `git --no-optional-locks status --porcelain -- .ufo/waves/round-17 .ufo/waves/round-18/runs .ufo/waves/round-18/predictions` printed nothing (exit 0), and HEAD = refs/heads/main = REV.
- **Git:** one early `git status --porcelain` ran without `--no-optional-locks`. It may refresh the `.git/index` stat cache but changes no content. No jj and no git write commands were used.
- **Execution:** no REA/npx, no Ghidra, and no carrier binary was run. The carrier-run repro's "carrier" is a 17-byte fake in /tmp that nothing executes, and its child processes are python only.
- **Installs:** none.
- **Writes outside the lane:** `/tmp/revtools`, `/tmp/cov`, `/tmp/r18copy`, `/tmp/{repro-,dup-,nonearm-,carrier-run-selftest-}*`, and the harness scripts above.
