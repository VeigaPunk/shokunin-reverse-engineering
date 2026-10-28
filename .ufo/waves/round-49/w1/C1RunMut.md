# C1RunMut: R49-C1 runner-provenance mutation test (wave 1, pre-freeze)

Seat `C1RunMut`, leaf member, no subagents. Scope: the provenance part of `tools/round-49/c1-run.py` and the counter's provenance clause in `tools/round-49/c1-counter.py`, attacked together. Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Lane untouched (`git rev-parse HEAD` still `e4f2cfa5…`; the only status line is the orchestrator's untracked `.ufo/waves/round-49/`).

## Verdict

**NOT CLEAN. The counter scores 4/4 for receipts produced the wrong way.** I ran 21 mutation scenarios against the real runner and the real counter (real REA 6.5.0 runs, real counter reruns, scratch clones only). The counter accepted 14 of them with `carriers_matched 4`; 2 of those 14 are confounded by my seat path and are listed separately. The counter rejects a receipt only when the `output_directory` string or the evidence id is wrong. It reads none of the runner's provenance sidecars, so it cannot tell:

1. a run recorded at a pre-freeze revision whose receipts are first committed after the freeze (F1),
2. an earlier real run's saved envelope replayed through `--fake-rea` (F2),
3. a verbatim evidence tree that is tampered or deleted (F3),
4. a `provenance.json` that names the committed path (F3),
5. a forged `output_directory` string that matches the substring (F4).

The plan's freeze rule and its `run_provenance_ok` sentence are satisfied in each case; the runner's own text claims more than the counter checks. Round 44 failed on that same mismatch. Findings are for the L1 to fold in before the freeze; I did not patch any draft.

## Setup and reproduction

- Scratch: `S=/fast/scratch/hyaku/kaidoku-r49/C1RunMut` (removed after copying artifacts). Each scenario is a fresh `mkclone.sh` clone (throwaway identity, clone-only, toplevel asserted before every git call). Receipts are committed in that clone; the counter is scored there with `--freeze <DEV_FREEZE of that clone>`.
- Driver: `artifacts: driver/drive.py` (scenarios BASE, S1–S5, P1, P3–P15, CTRL), `driver/drive2.py` (P14, P15, CTRL), `driver/drive3-p2b.py` (P2b). P2 in `drive.py` is a **no-op** (its key `output_directory` does not exist at top level of `provenance.json`); it is superseded by P2b. Its row is kept in `results.json`, marked by the same name, and is not counted.
- Tools: `unblob` (`~/.local/bin/unblob` → uv tool), `sasquatch` (`~/.local/bin/sasquatch`), `npx` (fnm node v24.21.0 on the runner's fixed PATH), rea-agents 6.5.0 cache at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`. Installed nothing; no pacman, no upgrades.
- Runner invocation (baseline and scenarios): `bash <clone>/tools/round-49/c1-run.sh --lane-root <clone> --carriers <clone>/tools/round-49/carriers.json --freeze <F> --evidence-root <scratch ev dir> --scratch <scratch base> [extra]`. `--data-run` never used; the default committed evidence root never written.
- Counter invocation: `python3 -I -B <clone>/tools/round-49/c1-counter.py --root <clone> --rev <HEAD> --freeze <DEV_FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <W> --json-out <OUT>`.
- Counter exit is **1** in every scenario including BASE, not 0. This is expected in a clone with no landing text: `bindings` false are `province_core_section, province_core_row, frontier_note, entry_present, coverage_map_row, sourced`. The measure is `carriers_matched` and the per-carrier clauses.

Input hashes (`sha256sum`, draft bytes = clone bytes):
- `draft/tools/round-49/c1-counter.py` `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`
- `draft/tools/round-49/c1-run.py` `f9161ff3afa2ded9553ea77dc31432add67ca6f6a02e98b3eb22c74da33a46fb`
- `draft/tools/round-49/c1-run.sh` `5ebb453f6197a8d2fc7790e80ae3d357e0053e8bf9191cdb95d946ee78c0d366`
- `draft/tools/round-49/carriers.json` `829e339286611d2abacb1041261e13637e9a0e0f9ce060ed9288a8a4ed0a56b3`
- `draft/plans/round-49-claims.md` `984e1026234d66af94b3c6e250e65784dd05141f4c4c7db1f624bb7970a9f492`

Mutation-applied evidence: each scenario's committed tree differs from BASE (file counts 36–50; `git diff` shows the tampered `firmware.bin_extract/apple.txt` byte `a`→`` ` ``). `CTRL` is a freshness control (see F5).

## Findings table

Full table with all hashes: `w1/C1RunMut/results.md` (`results.json` for the raw record). Exit codes: counter 0 met / 1 not met / 2 unevaluable; the runner's exit is in `driver.log`.

| # | scenario | how the wrong-way receipt was made | counter exit | carriers_matched | failing clauses | verdict |
|---|---|---|---|---|---|---|
| BASE | real runner run, dev freeze | none | 1 (landing bindings absent) | 4 | — | positive arm, carrier clauses clean |
| S1 | real run, `--rea-outdir-mode evidence` | REA writes into evidence dir | 1 | 4 | — | **confounded** (seat path contains `/kaidoku-r49/`); see F4 |
| S2 | real run, `--scratch <base>/kaidoku-r44` | scratch base named r44 (nested `kaidoku-r49`) | 1 | 4 | — | **ACCEPTED** (F4) |
| S3 | real run, code copy `ROUND_SEGMENT='kaidoku-r44'` | segment changed in runner | 1 | 4 | — | **confounded** (seat path); clean equivalent P14 rejected |
| S4 | real run at lane `e4f2` (pre-freeze), receipts committed after the freeze | `run.json rev_at_run = e4f2…` | 1 | 4 | — | **ACCEPTED** (F1) |
| S5 | `--fake-rea python3 -I -B replay.py` (replays saved real stdout + tree) | after.json byte-identical to BASE (`c2885be5…`) | 1 | 4 | — | **ACCEPTED** (F2) |
| P1 | delete `provenance.json` | sidecar removed | 1 | 4 | — | **ACCEPTED** (F3) |
| P2 (no-op) | edit `output_directory` in provenance.json | key absent; no change | — | — | — | invalid, superseded by P2b |
| P2b | `provenance.json`: `rea_output_directory` = committed evidence path, mode `evidence` | provenance lies, after.json still scratch | 1 | 4 | — | **ACCEPTED** (F3) |
| P3 | `run.json rev_at_run` = 40 zeros | sidecar lies | 1 | 4 | — | **ACCEPTED** (F3) |
| P4 | delete `run.json` | sidecar removed | 1 | 4 | — | **ACCEPTED** (F3) |
| P5 | one byte tampered in verbatim `firmware.bin_extract/apple.txt` | copy not byte-identical | 1 | 4 | — | **ACCEPTED** (F3) |
| P6 | delete verbatim `firmware.bin_extract/` | copy missing | 1 | 4 | — | **ACCEPTED** (F3) |
| P7 | delete `extract-env.json`, `unblob.log` | sidecars removed | 1 | 4 | — | **ACCEPTED** (F3) |
| P8 | append bytes to `envelope.json`, `stdout.log` | copies tampered | 1 | 4 | — | **ACCEPTED** (F3) |
| P9 | after.json `output_directory` = lane evidence path, re-minted | REA-style evidence mode | 1 | **0** | `run_provenance_ok` ×4 | rejected (correct) |
| P10 | same, no re-mint | | 1 | **0** | `run_provenance_ok`, `evidence_id_ok` | rejected (correct) |
| P11 | `output_directory` = `/fast/scratch/hyaku/kaidoku-r49/forged/…`, re-minted | forged string | 1 | 4 | — | **ACCEPTED** (F4) |
| P12 | `output_directory` = `/tmp/c1-forged/kaidoku-r49/…`, re-minted (string only; no file under /tmp) | non-scratch prefix | 1 | 4 | — | **ACCEPTED** (F4) |
| P13 | `normalized_result.files[0].sha256` forged, re-minted | content forgery | 1 | 3 | v1le: `oracle_hits_ok`, `projection_ok` | rejected (correct) |
| P14 | `output_directory` = `/fast/scratch/hyaku/kaidoku-r44/…`, re-minted | round-44 segment | 1 | **0** | `run_provenance_ok` ×4 | rejected (correct) |
| P15 | `output_directory` = `/fast/scratch/hyaku/kaidoku-r44/kaidoku-r49/…`, re-minted | r49 segment nested under r44 | 1 | 4 | — | **ACCEPTED** (F4) |
| CTRL | `--freeze` := the receipts commit itself | freshness control | 1 | 0 | `receipt_fresh` ×4 | rejected (correct; the freshness check works at commit time) |

Key hashes (`sha256`):
- BASE counter stdout `8fa73e4cabdee31e4e9ae7d46311902824f0483ff4a0743cd39b7777f72f6474`
- S4 counter stdout `f8548bbc38d60948b7c5f44f560ced2ae4e280e0c663e973900ce5d93df973a4`
- S5 after.json (v1le) `c2885be52625164029fcff15e53eb4875460e9e6992b5157ce565831eeca998d` = BASE after.json (v1le)
- S4 after.json (v1le) `6d192cbdd0802552e7f323d6bb88925d6c0f7db8cb96b89b91032dbf21760f10`

## Findings

**F1, pre-freeze run committed after the freeze scores 4/4 (S4). HIGH.**
- Command: runner with `--lane-root <clone-base at e4f2>` and `--carriers <dev clone>/tools/round-49/carriers.json`, exit 0. `run.json rev_at_run = e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9` (verified). The receipts were committed in a later clone commit (`396730d5 receipts S4_…` after `23942e48 dev freeze`), and the counter scored `carriers_matched 4`.
- Cause: `receipt_fresh` is commit-time only (`first_add` of `after.json` + `is_ancestor(freeze, add)`, `c1-counter.py` ~2082). `rev_at_run` is never read (grep: no `rev_at_run` in `c1-counter.py`).
- Plan/runner mismatch: `c1-run.sh` lines 13–14 say "a pre-freeze receipt breaks the counter's receipt_fresh binding". That is false for a receipt that was produced pre-freeze and first committed post-freeze. This is the round-44 failure mode in a new form.

**F2, replayed envelope accepted via `--fake-rea` (S5). MEDIUM, partly disclosed.**
- Command: `c1-run.sh … --fake-rea "python3 -I -B <scratch>/mut/replay.py"`, exit 0. The replay script copies a saved earlier real run's `firmware.bin_extract` and prints its stdout. Result: after.json byte-identical to BASE (`c2885be5…`), `run.json rea.command_override` records the replay, counter 4/4.
- The plan discloses that the rerun "proves projection equality, not which process wrote". The runner's `--fake-rea` help says "a synthetic receipt fails the counter's evidence-id and rerun-projection bindings"; that is true only for content-changed receipts (P13 rejected), not for a faithful replay. `command_override` is recorded and never checked.

**F3, the sidecars and the on-disk verbatim tree are never read (P1, P2b, P3–P8). HIGH.**
- `c1-counter.py` reads only `git show REV:corpus/evidence/round-49/c1/<id>/after.json` plus carriers/oracle/PROVINCE/entry/SOURCES/README (`measure()` lines ~2070–2078). No reference to `provenance.json`, `run.json`, `extract-tree.tsv`, `extract-env.json`, `unblob.log`, `envelope.json` or `stdout.log`.
- Consequence: a tampered byte in the verbatim tree (P5), a deleted tree (P6), a provenance that names the committed evidence path (P2b), a `rev_at_run` of zeros (P3), and a missing `run.json` (P4) all score 4/4.
- Plan/runner mismatch: `c1-run.py` docstring says `provenance.json` "binds the two so the committed evidence carries the produced bytes exactly". The plan says the runner "records `provenance.json`", and the counter implements only the `output_directory` string check. The binding the runner describes is unverified.

**F4, `run_provenance_ok` is a substring test (S2, P11, P12, P15; S1 and S3 confounded). MEDIUM–HIGH.**
- Clause (`c1-counter.py` 1176–1182): absolute path, contains `/kaidoku-r49/`, no `..`. No prefix check, no check that the segment is the immediate parent of the probe directory.
- Accepted: `/tmp/…/kaidoku-r49/…` (P12), `/fast/scratch/hyaku/kaidoku-r44/kaidoku-r49/…` (P15), `…/kaidoku-r49/forged/…` (P11), and a real run with `--scratch …/kaidoku-r44` (S2).
- Rejected correctly: `/…/kaidoku-r44/…` alone (P14), and the lane evidence path (P9, P10).
- Re-mint is one call of the frozen rea xpin tool (`mint_many`, identical to the counter's own path), so "the evidence id is minted over that provenance" establishes only that the envelope was re-minted, not who minted it.
- Confounded, **not counted as evidence about the lane**: S1 (evidence mode) and S3 (`ROUND_SEGMENT` copy) were accepted only because this seat's scratch path (`/fast/scratch/hyaku/kaidoku-r49/C1RunMut/…`) contains `/kaidoku-r49/`. Their string-level equivalents are P9 (rejected) and P14 (rejected). The consequence is still real: a checkout whose directory is named `kaidoku-r49` would pass evidence mode.

**F5, the control set misses these classes; the kill rule would not fire for them. MEDIUM (calibration).**
- The plan's CTL-C1-0..5 + POS cover do-nothing, relabelled v3 receipts, oracle-only envelopes, PATH without sasquatch, last round's receipts planted, and mutated superblocks. None covers a pre-freeze run committed post-freeze (S4), a replayed envelope (S5), sidecar or tree tampering (P5/P6), or a provenance lie (P2b). Each of S4, S5, P2b, P5 reaches 4/4 on the carrier clauses, so with a landed tree the kill rule ("any counterfactual control reaching 4/4 stops C1") would fire.
- Positive arm holds: BASE (real runs at the dev freeze) reaches `carriers_matched 4`, so the carrier clauses are satisfiable by a genuine run.

## Recommendations for the L1 (pre-freeze; not applied)

R1. Add a run-binding clause reading `run.json` and `provenance.json` at REV: `provenance.rea_output_directory == after.parameters.output_directory`; `rea.command_override is null`; `is_ancestor(freeze, rev_at_run)` (makes S4 red; the data run after the freeze records `rev_at_run == freeze`).
R2. Add a tree-binding clause: parse `extract-tree.tsv` at REV, compare each row (relpath, sha256, size) against the blob at REV, and reject extra or missing files under `<id>/firmware.bin_extract/`. Catches P5 and P6.
R3. Tighten the segment clause: require the path component immediately before `probe-R49C1Run/` to equal `kaidoku-r49` and reject any path not under the frozen scratch root (`$HYAKU_SCRATCH/kaidoku-r49/`). Catches P12 and P15; P11 (forged path + re-mint) remains and must be a disclosed limit.
R4. Replay (F2) cannot be closed by the counter. Either disclose it explicitly in the plan's limits ("a replayed earlier envelope is accepted") or bind `stdout_sha256` of `stdout.log` to `run.json`, which detects sidecar tampering but not replay.
R5. Correct `c1-run.sh` lines 13–14: a pre-freeze receipt is not caught by `receipt_fresh`.
R6. Add controls for S4, S5, P2b, P5 to the control set (each must go red, or the claim must be narrowed to what is enforced before the freeze).

Whichever of R1–R4 the L1 chooses, the plan sentence and the counter must say the same thing: at present the plan says the receipt's provenance is bound, and the counter binds one string.

## Not run

- `c1-run.sh --data-run` and any write to the committed evidence root (not run; all runs used scratch evidence roots).
- `c1-controls.py` / `run-ctl.sh` and `c1-counter.py --selftest` (not in scope; not run).
- Landing text, C2, and any lane file write (not run).

## Tooling

No tools installed or upgraded. The C1 runner and counter were used as shipped in the draft. No pacman transaction.

## Artifacts

`w1/C1RunMut/`: `results.md` (table with full hashes), `results.json`, `driver.log`, `driver/` (`drive.py`, `drive2.py`, `drive3-p2b.py`, `replay.py`, `c1-run-seg44.py`), `counter-out/*.json` (23 counter outputs), `evidence/` (BASE and run evidence trees minus `firmware.bin_extract`, so `after.json`, `run.json`, `provenance.json` and `stdout.log` for every run), `SHA256SUMS`.
