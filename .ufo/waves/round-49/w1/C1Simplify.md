# R49 wave 1 — C1Simplify (YAGNI on the draft instrument set)

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Draft bytes read-only; every mutation was made in
scratch (`/fast/scratch/hyaku/kaidoku-r49/C1Simplify`, a `mkclone.sh` clone with dev freeze
`c5a0eb3a76c346d932b5912958225d3a91de4762` and `c2-after.py` fixture `a9781385c8641a6c8134b15a6786c554500b9f6b`).
Artifacts: `.ufo/waves/round-49/w1/C1Simplify/` (variant diffs, receipts, `SHA256SUMS`).
Tools: no installs. Used the already-present `coverage` 7.17.0 (`~/.local/bin/coverage`), `unblob`,
`sasquatch`, `npx`. Lane: read-only git and my own `w1/` directory only.

## Verdict

**Not minimal, and one route must go before the freeze.** Removing the items below changes no verdict
(proven on the green fixture, table rows R1–R7). One exit-0 route is a false positive for the counter
(F1): `c1-counter.py --dev-arm` accepts the CTL-C1-2 fabricated oracle-only envelopes. Delete `--dev-arm`
before FREEZE. `c1-oracle.py` is evidence, not a score-time instrument; it is not the producer of the frozen
oracle block. Its own selftest passes, but it is not named by the plan.

## Findings (exact commands, exit codes, sha256)

| # | Finding | Command (scratch paths; `$S`=C1Simplify, `$CL`=clone) | Exit | Evidence (sha256 / path) | Effect on verdict |
|---|---|---|---|---|---|
| F1 | **`--dev-arm` exit 0 on fabricated envelopes.** Dev arm calls `measure(root, rev, rev, dev_arm=True)` (freeze==rev, so the freeze check is vacuous) and sets `receipt_fresh`/`projection_ok` to exempt (c1-counter.py ~L2085–2131, L2485). Envelopes are the CTL-C1-2 sandbox's `after.json` (oracle-only, fabricated). | `python3 -I -B $CL/tools/round-49/c1-counter.py --dev-arm --root $CL --rev a9781385… --pkg65 $PKG --arm-dir $S/devarm --work $S/devarm-work --json-out $S/devarm.json` | **0** (`dev_matched` 4/4) | `devarm.json` sha256 `5e8c97d6b608ba6820435fb99f90a34aff61f80f1bc63665f7a43dcfe860fdb0` (`receipts/devarm.json`). Same bytes through the real counter at the c2 sandbox: exit **1**, `projection_ok` false (`receipts/c1-counter-counterfactual-c2.json`). | Not a claim path, but the counter's own docstring calls dev-arm "the positive development control". Citing it as positive-control evidence would be a false green. **Delete.** |
| F2 | **Data runner writes into the committed evidence root on `--fake-rea`.** The refusal guard (c1-run.py ~L835–845) keys only on `--data-run`/env, not on `--fake-rea`. | `python3 -I -B $CL/tools/round-49/c1-run.py --lane-root $CL --carrier v1le --freeze a9781385… --scratch $S/fakeScratch --data-run --fake-rea 'echo {}'` | **1** (`receipt False`) | Wrote `clone/corpus/evidence/round-49/c1/v1le/{envelope.json,provenance.json,run.json,…}`; `receipts/fake.out`, `fake.err`. Not accepted (the counter rejects a synthetic receipt), but a dev-only flag reaches the committed root. | None (red either way). **Delete `--fake-rea`** from the data runner, or refuse it when `writing_committed`. |
| F2b | `--rea-outdir-mode evidence` (c1-run.py L799–806, L344) makes REA write into the evidence dir; the counter's `provenance_ok` (c1-counter.py ~L1177–1184) requires the `/kaidoku-r49/` scratch segment. | code read; not executed end-to-end | not run | — | Red either way (counter). **Delete.** |
| F2c | `--include-exploratory` writes v21le/v21be into the committed root; the counter never reads `scope.exploratory_ids` (0 hits in `c1-counter.py`); plan says v2.1 is not a carrier. Also `--carrier` filter, dev-only. | code read (`grep -c exploratory c1-counter.py` = 0) | not run | — | None. **Delete**. |
| F3 | **Freeze-time control path is untested in the draft, and the fixtures are not in the draft tree.** Default controls run writes fixtures to `<root>/tools/round-49/control-fixtures` (c1-controls.py L88, L91–110, L1420). The plan's freeze score is `--from-fixtures`; that branch (L1399–1420) and `load_fixtures` (L113–133) never ran in the default run (coverage, `receipts/c1-controls-full-devafter.json`). | (a) `cd $CL && python3 -I -B tools/round-49/c1-controls.py --root $CL --freeze a9781385… --counter $CL/tools/round-49/c1-counter.py --pkg65 $PKG --work … --out … --json-out … --doc-dir $S/docs` ; (b) `… --controls pos --from-fixtures --fixtures-root $CL/tools/round-49/control-fixtures` | (a) **0**, 7/7 as expected; (b) **0** | (a) `c1-controls-full-devafter.json`; (b) `c1-controls-pos-fromfixtures.json`. Fixtures: 39 untracked files in clone. | Freeze ordering must be: build fixtures → commit them → FREEZE → `--from-fixtures` score. `mkclone.sh` does not include them. **Fix before FREEZE.** Also `run-ctl.sh` defaults `--freeze` to `git rev-parse HEAD` (not the freeze); pass it explicitly. |
| F3b | Controls "landing" blocks (`--doc-dir`) pass the counter. | `…--controls pos…` as in F3 | 0 | `c1-controls-pos-run1-summary.json`; POS score `c1-score-pos-base.json` → `carriers_matched 4`, `met_target true` | Positive: the draft landing blocks satisfy the counter's landing bindings. |
| F4 | **`c1-oracle.py` is not score-time and is not the producer of the frozen oracle.** Counter/controls/run reference it 0 times; plan does not name it. `carriers.json` is "the round-44 table carried over with its oracle data" (plan L52–53). Its emitted doc does not contain the top-level `oracle` keys (`tool_version_line`, `member_command`, `expected_tree_source`, `independence`, `pkg` → 0 hits in c1-oracle.py) that `oracle_tool_ok` reads (`doc.get('tool')`, c1-counter.py L2222–2234). Dead: `import errno` (L79), `EXPLORATORY_IDS` (L187). | `python3 -I -B tools/round-49/c1-oracle.py --selftest` | **0** (24 cases, `failures []`) | `oracle-selftest.out` sha256 `19bb2b24bad7d1d3339a7893bd05d4dd14d0ac40fcbbc125dfb9fe847d5f9053` | None at score time. **Move out of the frozen directory (evidence) or delete**; drop the two dead lines either way. |
| F5 | Counter dead defs: `HANDLER_RE` (L326), `legacy_same_rel` (L1393), selftest `spec_plants`, `mk_same_runner` (+`run`), `runner_for` — zero callers. | Variant `cA` (24 lines removed, `w1/C1Simplify/variants/c1-counter.cA.diff`): `python3 -I -B $CL/tools/round-49/var-cA.py --root $SB --rev 741418e1… --freeze a9781385… --pkg65 $PKG --work … --json-out …` and `--selftest` | score **0**; selftest **0** | score normalized sha `870e8e910b19f431…` identical to base; selftest `cases 47, red_ok 46` identical (`receipts/c1-score-pos-cA.json`, `c1-selftest-cA.out`) | **None (R1).** |
| F6 | `--dev-arm` path: `dev_arm()` (L2408–2514, 107 lines) + dispatch + flags `--dev-arm --arm-dir --arm-ids --run-rea`. Never executed in 8 counter runs. | Variant `cB` (116 lines, `c1-counter.cB.diff`), same two commands | score **0**; selftest **0** | identical (`c1-score-pos-cB.json`, `c1-selftest-cB.out`) | **None (R2).** Delete (also fixes F1). |
| F7 | `--verify-receipt` (L2335–2355) and `--no-rerun` (L2360–2366, always exits 2). Neither is in the plan's counting command; `--verify-receipt` never executed; no caller in controls or run. | Variant `cC` (27 lines, `c1-counter.cC.diff`) | score **0**; selftest **0** | identical (`c1-score-pos-cC.json`, `c1-selftest-cC.out`) | **None (R3).** Delete. |
| F8 | Silent-admit branch: `silent_detail_matches` (L1477–1487) and gate `allowed_details = (removed.get('silent') …)` (L1557–1558). `removed` comes from the rule model (L640–708), never set on the four carriers; never executed in 8 runs. | Variant `cD` (15 lines, `c1-counter.cD.diff`) | score **0**; selftest **0** | identical (`c1-score-pos-cD.json`, `c1-selftest-cD.out`) | **None (R4).** Delete. |
| F9 | Controls-driver `selftest` (c1-controls.py L1151–1248, dispatch L1299–1302, flag L1284; 103 lines), never executed in the default run. | Variant `var-ctl.py` (`c1-controls.selftest-removed.diff`): `… --controls pos --from-fixtures --fixtures-root …` for both | **0** both | Verdict maps identical (`CTL-C1-POS as_expected`, kill false, failures []); `c1-controls-pos-fromfixtures-{orig,selftest-removed}.json` | **None for POS (R5).** Not re-run for the 7-control set. |
| F10 | C2 `Overlay.ls` (c2-mismatch.py L130–136, 7 lines). The battery applies no overlay to a W1 path, so the filter never bites; coverage shows the lines run but change nothing. | Variant `c2-noOverlayLs.py`: `python3 -I -B … c2-noOverlayLs.py --root $CL --rev a9781385… --freeze c5a0eb3a… --battery` | **0** | Battery JSON identical to base except counter fields (`c2-battery.json` sha `579788d3…`; `c2-noOverlayLs.json`). `mismatches 0`, 11/11, do-nothing 9 red. | **None (R6).** Delete. |
| F10b | `Overlay.__getattr__` is **needed**: without it the battery turns red (`c2-noGetattr`). | `… c2-noGetattr.py … --battery` | **1** (battery red, `mismatches 0`, `failing` lists all 11 mutations) | `c2-noGetattr.json` | Keep. |
| F11 | C2 battery: 57 of 476 statements not executed (coverage, `--battery`): all are error-message branches for atoms A1–A9 (e.g. A2 L266–274, A4 L312–327, A5 L339–349, freeze L503–511). No function is unexecuted. The plan fixes eleven mutations, so these cannot be added without a plan change. | `coverage run --branch -m` style run on `c2-mismatch.py --battery` | 0 | `c2-cov` report (82.4%) | Depth gap, not a removal. Disclose. |
| F12 | C2 freeze integrity probe: touch a frozen file (`tools/round-49/c2-mismatch.py`), commit, restore to freeze blob, commit. | `python3 -I -B $CL/tools/round-49/c2-mismatch.py --root $CL --rev <touched|restored> --freeze c5a0eb3a…` | **2** both (`frozen_path_changed`) | `probe-*.json` | Works as the plan states (a restore does not un-block). C1's merge-aware walk was **not run** by me. |
| F13 | Top-level `carriers.json` keys `round` and `toolchain` are read by no tool (0 hits in all three). | `grep -c "'round'\|'toolchain'"` on counter/run/controls | — | — | None. Removing them changes frozen bytes; low priority. |
| F14 | Counter baseline coverage: score + selftest + six counterfactuals execute 1575 of 2107 statements (69.8%). Never executed in any of the 8 runs: `dev_arm`, `find_rea_pkg` (L532, the `--pkg65` fallback; plan always passes `--pkg65`; removal not run), `trusted_run_root` (L1185, reached only through `diagnostic_rel` with `report.link`; reachable but unexercised, **keep unless the L1 decides**), `silent_detail_matches`, `legacy_same_rel`, selftest helpers. | `coverage combine` over `cov-cscore`, `cov-cselftest`, `cov-c0..c5` | — | `all.json` (not copied) | See R1–R4. |
| F15 | Counterfactuals on the green fixture, each exit 1 for a distinct reason: c0 do-nothing `carriers_matched 0`; c1 `subject_pin_ok`…; c2 `projection_ok` ×4; c3 sasquatch absent; c4 `run_provenance_ok`; c5 mutated superblock. | `c1-counter.py --root <sandbox-cN> --rev <rev> --freeze a9781385… --pkg65 $PKG` | **1** ×6 | `receipts/c1-counter-counterfactual-c{0..5}.json` | Confirms the controls behave as the plan states. |

Positive reference: POS arm `CTL-C1-POS` through the counter on sandbox rev `741418e1cd4ba9725ab274ce558a5e51b1a0cb60`
→ exit **0**, `carriers_matched 4`, `met_target true` (`receipts/c1-score-pos-base.json`).
Freeze-integrity: the counter's `frozen_path_changed` check passes at the dev commits (`bindings`/`frozen_path_changed []`).

## Removal list (each proven verdict-neutral unless marked)

| ID | Remove | Lines | Proof | Verdict change |
|---|---|---|---|---|
| R1 | `HANDLER_RE`, `legacy_same_rel`, selftest `spec_plants`, `mk_same_runner`, `runner_for` (c1-counter) | 24 | F5 | none |
| R2 | `--dev-arm` path (`dev_arm()`, dispatch, 4 flags) | 116 | F6 (and F1 is the reason) | none on the claim; removes a false-green route |
| R3 | `--verify-receipt`, `--no-rerun` (c1-counter) | 27 | F7 | none |
| R4 | silent-admit branch (`silent_detail_matches`, `allowed_details` gate) | 15 | F8 | none |
| R5 | controls-driver `selftest` + flag | 103 | F9 (POS arm only) | none on POS |
| R6 | C2 `Overlay.ls` | 7 | F10 | none (battery JSON identical) |
| R7 | c1-oracle.py out of `tools/round-49/` (or delete), dead `errno` and `EXPLORATORY_IDS` | file | F4 | none at score time |
| R8 | c1-run.py: `--fake-rea`, `--rea-outdir-mode evidence`, `--include-exploratory`, `--carrier` | code read | F2, F2b, F2c | none (red either way); F2 is a real guard gap |
| R9 | controls-driver `--rehearsal-table-freeze`, `--dev-arm-carriers`, `--capture-only` | code read (not run; L1317–1349, L1357–1376) | coverage: never executed in default run | none on the default path; not run |

Keep (proven needed or on the freeze path): `c1-counter.py` core; `carriers.json` (frozen table); `c1-run.py` + `c1-run.sh` (data procedure, named in the counter's FROZEN_PATHS); `c1-controls.py` default, `--build-only`, `--from-fixtures`, `load_fixtures` (executed green in F3b); C2 except `Overlay.ls`, including `Overlay.__getattr__` (F10b).

## Plan-vs-draft notes for L1

- Control fixtures (`tools/round-49/control-fixtures/**`) are missing from the draft; they must be built, committed before FREEZE, then scored with `--from-fixtures` (F3).
- `run-ctl.sh` takes `--freeze` from `HEAD`; pass the freeze explicitly.
- `plans/round-49-claims.md` is absent at base (expected; it lands with FREEZE). The other plan-frozen paths exist at base: `tools/round-42/{fixtures.json,c1-counter.py,prior-pins.json,rea-pkg.json}`, `tools/round-39/gen-squashfs.py`, `tools/round-27/xpin-attribute.mjs`, `corpus/evidence/round-44/oracle/`, and the four carrier bytes under `corpus/evidence/round-42/c2/fixtures/`.
- Freeze-time receipts must be created after the dev freeze; the counter's `receipt_fresh` check depends on that.

## Draft tool sha256 (as read)

| file | sha256 |
|---|---|
| c1-controls.py | 209f0f4ad0568a6e845b72dcd8ca5102caa13423884391dd9a92398e26d087a4 |
| c1-counter.py | d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779 |
| c1-oracle.py | 80f8212d892cca1c75edf101233a48a8b8dcebc4c5583654b7ed0e45fe16cc47 |
| c1-run.py | f9161ff3afa2ded9553ea77dc31432add67ca6f6a02e98b3eb22c74da33a46fb |
| c1-run.sh | 5ebb453f6197a8d2fc7790e80ae3d357e0053e8bf9191cdb95d946ee78c0d366 |
| c2-mismatch.py | 90fa4722c960a8c21dd3166f115f721fa097115cc576703478c7a55c7d15243f |
| carriers.json | 829e339286611d2abacb1041261e13637e9a0e0f9ce060ed9288a8a4ed0a56b3 |

Per-receipt sha256 values: `.ufo/waves/round-49/w1/C1Simplify/receipts/SHA256SUMS`.

## Limits and not-run items

- Timestamps: no per-command UTC stamp was recorded. The run window was about 21:10–22:00 UTC on 2026-10-28.
- Removal proofs were run on the scratch dev freeze, not the lane. Only POS was re-run for the controls removal (F9). Not run: C1 freeze-integrity merge walk; `find_rea_pkg` removal; R8 and R9 (code read only).
- Scratch `$S` removed after receipts were copied. The clone's alternates pointed at the lane's object store (read only); nothing was pushed or committed to the lane or fleet repo.
