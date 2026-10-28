# R49-C1 pre-freeze attack — C1CounterMut (mutation test of the DRAFT `c1-counter.py`)

Seat: C1CounterMut (leaf, offline). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`.
Artifacts: `.ufo/waves/round-49/w1/C1CounterMut/` (harness, mutant sources, per-control receipts, probes, `table-full.md`, SHA256 manifests).
Scratch (removed after receipts were copied): `/fast/scratch/hyaku/kaidoku-r49/C1CounterMut`. Nothing written in the lane tree, the draft tree, git history or `~/.local/bin`. No tools installed or upgraded (python 3.14.8, git, node v24.21.0 from fnm were used as found).

## Verdict

**NOT freeze-ready as drafted.** The draft counter passes its own selftest unmodified (exit 0, 47 cases, `failures []`) and the seven draft controls pass at base (exit 0, `kill_rule_fires false`). But the instruments do not witness what the plan says they witness:

- **35 of 75** single-point mutants of the draft counter **survive `--selftest`** (exit 0).
- Of the 35 selftest survivors, **34 survive all seven controls** (`CTL-C1-0..5`, `POS`). The one caught survivor (M29) is caught only by the positive arm, not by a red control.
- **CTL-C1-5 is vacuous.** With the superblock probe forced to `ok` for every input (M49), all seven controls still behave as expected.
- Plan predicate clause `unpublished_entries == []` is **not enforced** by any counter clause (probe P7).
- The freeze walk **does not catch files added** under `tools/round-49/` after the freeze, while the plan says "no commit touches `tools/round-49` (directory)" (probes P1, P2).
- Frozen tools (`c1-run.py`, `c1-controls.py`) quote a plan sentence that is not in the plan (plan says the committed evidence path is *not* the output directory). See F6.

Findings to fold in before the freeze are F1–F8 below. Nothing here was patched in the drafts.

## What was run (exact)

| step | command (abbreviated) | exit | receipt |
|---|---|---|---|
| clone at base with draft tools as dev freeze | `draft/mkclone.sh /fast/scratch/hyaku/kaidoku-r49/C1CounterMut/base` | 0 | `DEV_FREEZE=7a064950c13ca311a47d2effba811ef527c778ad` (identity `r49-dev` set in the clone only; toplevel asserted) |
| draft counter sha | `sha256sum draft/tools/round-49/c1-counter.py` | — | `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779` |
| baseline selftest | `TMPDIR=$S HYAKU_SCRATCH=/fast/scratch/hyaku python3 -I -B <clone>/tools/round-49/c1-counter.py --selftest --pkg65 <rea 6.5.0> --work $S/base-run` | 0 | stdout sha256 `f575d310f1bdd2067ef7298aef70393ce5bc1fdd89a8f96ec1d07751112f572b` (`baseline/base-selftest.out`); 11 s; `cases 47, failures []` |
| baseline controls | `draft/run-ctl.sh <clone> $S/ctl-base` | 0 | `baseline/ctl-base.json` sha256 `b2c37b7f405aebc98f7d4dd64cf8726b083ec735c386819ed9b8380dbd3f9629`; CTL-C1-0..5 `as_expected` (exit 1), POS `as_expected` (exit 0), `kill_rule_fires false`; 1m53s |
| mutation sweep | `python3 harness.py` (75 mutants, 4 workers) | — | `harness/mut-results.json` sha256 `f8f244e907f4c9460c026a720f7380618e9cee9be6e7ced80d79d8fed63197f2`; 40 KILLED, 35 SURVIVED, 0 CRASH, 0 PATTERN-MISS |
| controls on survivors | per mutant: `reflink` clone of base (`cp -a --reflink=always`), mutated counter written and committed as its dev freeze (identity in clone only; toplevel asserted), then `draft/run-ctl.sh <clone> <work>` | 0 each | 37 runs; `harness/ctl-runs.json`, per-run `ctl/<id>/ctl.json` + `run-ctl.txt` |

Harness method. Each mutant is one replacement (or one CLAUSES tuple element removed), each asserted to match exactly its expected number of times, then compiled, then selftested with `C1_SELFTEST_DETAIL=1`. Selftest exit 0 = SURVIVED; exit 1 with the selftest JSON line = KILLED; anything else = CRASH. The 75 mutants are 22 `CLAUSES` drops (`D-*`) and 53 source edits (`M01`–`M55`). The source of every mutant is in `mutants.py`; the mutant bytes for the 37 control-run mutants are in `mutants/*.py` with `mutants/SHA256SUMS`.

Control-run check. The controls really ran the mutant. For `M22-s-minor-off` the control receipts record `counter_sha256 029d63914e44d6a9747fc55cee65df5c8469c227309a6a45ef263f6b4f790e50`, which equals the mutant's sha256 in `harness/table-full.md`.

## Mutation table (summary; full hashes in `harness/table-full.md`)

Survived selftest and not caught by any control (34): D-carrier_present, D-carrier_pin_ok, D-carrier_size_ok, D-carrier_fresh_ok, D-oracle_ok, D-operation_ok, D-chunks_ok, D-nonregular_unpublished_ok, M01 handler any-of, M03 oracle sha ignored, M04 oracle size ignored, M10 freeze prefixes off, M11 freeze A ignored, M12 freeze blob backstop off, M13 used-by off, M16 frontier stem off, M17 frontier token off, M22 s_minor off, M24 layout handler off, M27 compression off, M31 receipt-fresh add-only, M32 is_ancestor off, M33 carrier_fresh off, M34 envelope exit_code key off, M35 operation off, M36 provenance absolute-path off, M40 nonregular unpublished off, M43 chunks off, M44 carrier pin off, M45 carrier size off, M46 starts_sane off, M53 gap kind any, M54 removal not exclusive, M55 disposition required off.

Survived selftest, caught by a control (1): M29 chunk-end without zero-pad rounding, caught only by `CTL-C1-POS` (`expected exit 0, got 1`).

Killed by selftest but missed by all seven controls (2): M49 layout probe verdict constant `ok` (superblock probe off); M50 freeze walk returns `[]`. These are the CTL-C1-5 vacuity proof (M49) and the freeze-walk proof (M50): no control plants a post-freeze change to a frozen path.

Killed by selftest (38, plus M49 and M50 above, total 40): D-layout_ok, D-carve_ok, D-tree_ok, D-receipt_present, D-receipt_fresh, D-evidence_envelope_ok, D-subject_pin_ok, D-handler_ok, D-oracle_hits_ok, D-gaps_ok, D-path_shape_ok, D-run_provenance_ok, D-evidence_id_ok, D-projection_ok, M02, M05, M06, M07, M08, M09, M14, M15, M18, M19, M20, M21, M23, M25, M26, M28, M30, M37, M38, M39, M41, M42, M47, M48. Selftest kills of these are real witnesses, but for several the kill is by a case that checks a different clause than its name (e.g., `M07` is killed by the rerun cases, not by `handler_ok`). Not a finding by itself.

## Classification of the 35 selftest survivors

Equivalent on the frozen carrier set (no finding, but they are not witnessed either):
- D-carrier_size_ok, M45 — the frozen pin already fixes the size.
- D-nonregular_unpublished_ok, M40, M53, M54, M55 — all four carriers have zero non-regular rows (`GAP_RULE` comment), so any path-bearing gap already fails `disposition_check`.
- M12 — the endpoint blob comparison is subsumed by `git log` for the paths it covers.
- M24 — the layout `handler_ok` branch duplicates the `carriers_spec_ok` binding, which fails anyway.
- M46 — `starts_sane` is mostly subsumed by `meta_chain_lands`.
- M34 — every counter-written receipt carries `counter_sha256`, so the `exit_code` key is redundant for real score receipts; a forged receipt carrying only `exit_code` is still accepted (real hole, low severity; see F5).

Real witness holes (the clause can break and nothing notices):
- Carrier custody: D-carrier_pin_ok, D-carrier_present, D-carrier_fresh_ok. A pin mismatch cannot be produced in a control because any byte change at a frozen path is first a drift (exit 2). Only an in-counter case with a wrong `sha256` in carriers.json would witness it.
- Oracle: D-oracle_ok, M03 (sha not compared), M04 (size not compared). No selftest case or control publishes a file whose path matches but whose sha differs while the projection is satisfied; CTL-C1-2 and CTL-C1-4 use the oracle's own sha.
- Receipt shape: D-operation_ok, D-chunks_ok (no `extraction_failed` case), M01 (any-of handler), M43, M35.
- Layout: M22 (s_minor), M27 (compression class), M46 (starts). Only CTL-C1-5 could witness the layout probe; it does not (F1).
- Documentation: M13 (used-by), M16 (frontier stem), M17 (frontier token). Selftest has only the absence case; no control has a wrong-stem note.
- Freshness: M31 (add only), M32 (is_ancestor), M33 (carrier_fresh, not in the plan; F7).
- Freeze walk: M10 (`FROZEN_PREFIXES` off), M11 (`A` not counted), M12. Selftest has only explicit-path cases; no control changes a frozen path.
- Provenance: M36 (relative `output_directory` accepted because the absolute test was removed). Low severity: REA always emits absolute paths, but nothing tests it.

## Findings for the fold-in (ordered by severity)

**F1 — CTL-C1-5 cannot fail.** `c1-controls.py` control_c5 plants the mutated superbytes at `corpus/evidence/round-49/c1/superbyte-mutation/<id>/<arm>.bin`, which the counter never reads (it reads `corpus/evidence/round-44/carriers/*.bin` and `corpus/evidence/round-49/c1/<id>/after.json`). Its expectation is only `exit non-zero, carriers_matched 0` (plus `probe_reds_every_mutation: True`, a key that the judge never reads: `grep -n probe_reds_every_mutation c1-controls.py` → only line 854). With no receipts, the counter exits 1 whatever the probe does. Proof: M49 (probe returns `ok` for every input) → `CTL-C1-5 as_expected 1 behaved as the claim states`, `surv-ctl/M49-layout-ok-constant/ctl.json` sha256 `0aa50d4583bc9a92…`. Fix: call the counter's `layout_probe` in-process on each arm, and judge `ok is False` per arm and per carrier. The byte deltas the control already records are the right inputs.

**F2 — The controls witness almost nothing the selftest does not.** 34 of 35 selftest survivors pass all 7 controls; only M29 is caught (by POS). The counter's clause-level guarantees therefore rest on the selftest alone (47 cases; most of the 22 `CLAUSES` entries have no case that breaks them in isolation). Each gap in the classification above needs a selftest case with the named fixture, e.g.: (a) carriers.json with a wrong pin while bytes match the frozen pin; (b) published sha altered with path and size intact; (c) `extraction_failed: true` on one chunk; (d) `operation` = `unblob` with `extract_firmware` misspelt; (e) `used-by` without the entry; (f) frontier note with another stem; (g) s_minor flipped in a carrier with the pin recomputed; (h) lzma-labelled carrier whose observed class is gzip; (i) receipt first added on a branch that does not descend from the freeze; (j) new file added under `tools/round-49/` (see F4).

**F3 — `unpublished_entries == []` is not enforced (plan clause missing from the counter).** `grep -n unpublished_entries c1-counter.py` shows reads only in `receipt_paths` (line 1244), `projection` (line 1776), and the selftest fixture builders (lines 2639, 2697); no clause reads it. Probe P7 (`probe_unpub.py`, `probes/probe_unpub.out`): a receipt with `normalized_result.unpublished_entries` set to one symlink row, `gaps []`, all other fields as the green fixture, gives `gaps_ok true`, `nonregular_unpublished_ok true`, `run_provenance_ok true`, `subject_pin_ok true`, `operation_ok true` (every clause the evaluator computes is true). The counter-time rerun would reproduce the same `unpublished_entries` in its projection, so projection_ok would also be true. Fix: add `unpublished_entries_ok` (empty list) to `evaluate_carrier` and to `CLAUSES`, with a selftest case.

**F4 — The freeze walk misses added files under `tools/round-49/`.** `frozen_drift` treats an `A` (add) as a change only when the path existed at the freeze (`existed_cache`), so a new file under a frozen prefix is never a touch. Probes (`probes/probes.out`): P1 `tools/round-49/zz-new-helper.py` added after the freeze → `frozen_drift == []`; P2 `tools/round-49/control-fixtures/ctl-x/extra.bin` added → `[]`. The plan says: "no commit in FREEZE..REV touches `tools/round-49` (directory)". Edits to existing unlisted files *are* caught via the prefix (P6, `probes/probe_prefix_edit.out`: `tools/round-49/c1-controls.py` edited → `['tools/round-49/c1-controls.py']`). Fix: for paths under the directory prefixes, any `A`/`M`/`D`/`R`/`T`/`U` counts; keep the existed-at-freeze rule only for explicit single-file entries if the plan keeps it. M50 (freeze walk returns `[]`) is caught by selftest but not by any control (F2).

**F5 — Forgeable receipt shapes accepted.** (a) `evidence_envelope_ok` tests `{'counter_sha256','exit_code'} & set(env)`; a receipt carrying only `exit_code` passes (M34 survives). (b) `provenance_ok` tests `'/kaidoku-r49/' in output_directory` as a substring (M36 survives for relative paths; the absolute test is in the same function). Probe P4 (`probes/probes.out`): `provenance_ok('/tmp/kaidoku-r49/x') == True`, `'/home/x/kaidoku-r49/run' == True`, `'/fast/scratch/hyaku/kaidoku-r42/x/kaidoku-r49/y' == True`. The plan requires "an absolute path inside the `/kaidoku-r49/` scratch segment"; the substring test is literal, but the contract forbids citing anything under `/tmp`. Suggested fix: require the prefix `$HYAKU_SCRATCH/kaidoku-r49/` (or `/fast/scratch/hyaku/kaidoku-r49/`) and `os.path.isabs`. Low–medium severity.

**F6 — Plan misquote in frozen tools; the provenance mechanism is described two ways.** The plan's sentence (line 79) says `output_directory` is "an absolute path inside the `/kaidoku-r49/` scratch segment"; it also says the committed evidence path is not the output directory. The plan contains no sentence that "names a corpus/evidence/round-49/c1 path". Three frozen tool files say it does:
- `tools/round-49/c1-run.py` lines 337–342 (comment on `build_plan`) quotes "the binding the frozen claims text states … names a corpus/evidence/round-49/c1/ path". `build_plan(... outdir_mode='evidence')` makes that the default in the function signature, while the CLI default (line 800) is `scratch`. The `evidence` mode yields a receipt that `run_provenance_ok` rejects, so the function default is a trap.
- `tools/round-49/c1-controls.py` docstring lines 41–42 (CTL-C1-4 "provenance binding refuses … not under corpus/evidence/round-49/c1") and lines 945–946 (CTL-C1-POS "names the round-49 evidence path, which is what the provenance binding reads"). The counter actually reads the scratch segment; the verdicts are right, the stated mechanism is wrong.
- `tools/round-49/c1-controls.py` line 796 (CTL-C1-4 note) repeats it.
Fix: change the three comments and the `build_plan` default to the plan's sentence; delete the `evidence` mode or mark it as never valid.

**F7 — `carrier_fresh_ok` is outside the plan and does not see the round-44 measurement.** The plan's predicate has no freshness clause. The counter has one (`carrier_fresh_ok`, checked against `tools/round-42/prior-pins.json`, which lists rounds 38–41 only). `carriers.json` pins are not in that file (checked: all four `False`). The plan's disclosed limit says these bytes were "already measured once in round 44". So the clause passes for bytes the plan says were already measured, and nothing witnesses it (M33 survives). Fix: either name the clause in the plan and cover round 44 in the prior-pins list, or drop it and state the reuse in the disclosed limits.

**F8 — Plan and counter disagree on what is enforced.** `carrier_size_ok`, `carve_ok`, `oracle_ok`, `carrier_fresh_ok`, the `receipt_fresh` ancestry check, and the `frozen_tables_valid` binding are not sentences of the plan's predicate, although the plan says "The counter is that sentence". Conversely the plan's "`target` frozen in carriers.json" has no referent (no `target` key in the table; see Also noted). Either extend the plan sentence to name the extra clauses or remove them; they are currently unwitnessed (F2).

Also noted: `carriers.json` has **no `target` key** (its keys: `carriers, claim, note, oracle, round, schema, scope, superblock_layout, toolchain`), although the plan says "`target` frozen in carriers.json". `carriers_spec` skips its target cross-check when the key is absent (`if 'target' in spec and …`), so the target is enforced only by the constant `TARGET = 4` and `len(ids) == 4`. Fix: either add `"target": 4` to the frozen table or reword the plan sentence (see F8).

## Probes (no draft edits; all in a throwaway fixture repo, identity `probe` in that repo only, toplevel asserted)

| id | command | result |
|---|---|---|
| P1 | `probes.py`: freeze `F`, then commit `tools/round-49/zz-new-helper.py`, `frozen_drift(D,F,R1,spec)` | `[]` (expected: touch of `tools/round-49`) |
| P2 | same, add `tools/round-49/control-fixtures/ctl-x/extra.bin` | `[]` |
| P3 | edit the file that P1 added | `['tools/round-49/zz-new-helper.py']`: the later `M` is seen, the `A` that created it is not (the asymmetry behind F4) |
| P4 | `provenance_ok` on `/tmp/kaidoku-r49/x`, `/home/x/kaidoku-r49/run`, nested `…/kaidoku-r42/…/kaidoku-r49/y` | all `True` |
| P5 | `under_root` segment probes | correct (`x_extract/a` owned, `x_extract2/…` not) |
| P6 | `probe_prefix_edit.py`: edit an existing unlisted file under `tools/round-49/` | detected |
| P7 | `probe_unpub.py`: green-shape receipt with `unpublished_entries` set | every clause true (F3) |

Exit codes: each probe ran `python3 -I -B`, exit 0. Output in `probes/`.

## Not run / limits

- Not run: `c1-run.sh --data-run` (prohibited for seats); the REA data procedure; `c2-mismatch.py`; wave-2 work. No `corpus/`, `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `PROVINCE.md`, `plans/`, `tools/`, `SKILL.md` edited; no git mutation in the lane or fleet repo.
- The controls are real REA runs (each control run about two minutes); their verdicts are the controls' own, not re-derived.
- Mutation coverage is 75 single-point edits. It is not an exhaustive proof: a surviving mutant is a witness gap, and a killed one only shows that one case fails under that edit.
- The carriers are the four round-44 fixtures (4 KiB, no non-regular members); the non-regular clauses are therefore equivalent on this set (see classification), not tested.

## Receipt index

- `harness/table-full.md` — the 75-row table with full sha256s and control verdicts.
- `harness/mut-results.json` (sha256 `f8f244e9…`), `harness/ctl-runs.json`, `harness/harness.py` (sha256 `099ce146…`), `harness/mutants.py` (sha256 `1f394fb2…`), `harness/survivors.txt`, `harness/full-run2.txt`, `harness/surv-one.sh`.
- `mutants/*.py` (37 mutant counters), `mutants/SHA256SUMS`.
- `ctl/<id>/ctl.json` and `ctl/<id>/run-ctl.txt` (37 control runs).
- `baseline/base-selftest.out`, `baseline/ctl-base.json`, `baseline/ctl-base.time`, `baseline/ctl-base.out`.
- `probes/probes.py`/`probes.out`, `probes/probe_unpub.py`/`.out`, `probes/probe_prefix_edit.py`/`.out`.
- `draft-sha256.txt` — draft tool and plan hashes read by this seat (hashes read at seat end; `c1-counter.py` `d6d70cb7…` equals the value recorded when the clone was made, `plans/round-49-claims.md` `984e1026…`, `carriers.json` `829e3392…`, `c1-controls.py` `209f0f4a…`, `c1-run.py` `f9161ff3…`).
- `SHA256SUMS.artifacts` — sums of the json/out artifacts.

## Disclosure

One `git status --porcelain` was run in the lane root by mistake (intended read-only). It is not on the allowed read-only list and can refresh `.git/index` stat data. It was interrupted by a 300 s command timeout. Nothing was staged, committed, stashed or written by this seat; no other git command touched the lane.

## Suggested witnesses for L1 (folded into the freeze if accepted)

1. Layout: CTL-C1-5 calls the counter's `layout_probe` in-process per arm and judges `ok is False`; selftest adds s_minor, compression-class, and starts cases.
2. Oracle: selftest case (published sha differs, path/size intact) → `oracle_hits_ok` red.
3. Receipt shape: selftest cases for `chunks_ok` (one `extraction_failed`), `operation_ok`, `unpublished_entries` (F3), `exit_code`-only envelope (F5).
4. Documentation: selftest cases for `used-by` missing the entry, frontier note with another stem, frontier note without token.
5. Freshness: selftest case where the first add sits on a branch not descending from the freeze.
6. Freeze walk: selftest cases adding a file under `tools/round-49/` after freeze (P1/P2) and a control that commits one.
7. Provenance: reject `/tmp` and any prefix other than the scratch base (F5).
