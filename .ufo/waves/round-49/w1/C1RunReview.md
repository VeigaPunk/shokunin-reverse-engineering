# R49-C1 run-procedure review (seat C1RunReview, wave 1, pre-freeze)

Base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`. Dev clone via `mkclone.sh` at `DEV_FREEZE=72a100b11f467a1e654785f476ba7ddd8a9b12c8` (scratch, removed). Lane tree not written. `--data-run` not run. Freeze-bound draft bytes read-only.

## Verdict

**REVISE before freeze.** The fail-closed paths work: the default committed root is refused without `--data-run`; a pin mismatch never reaches REA; an occupied output directory without `--force` exits 2 and leaves the receipt unchanged. But the data run can write outside `corpus/evidence/round-49/c1/` and the scratch segment through ordinary arguments, the counter's `run_provenance_ok` accepts paths outside `$HYAKU_SCRATCH/kaidoku-r49/` (including `/tmp` and lane-internal paths), and the runner's own comments quote a plan sentence that does not exist.

## Top findings

1. **The data-run guard protects one path only.** `--evidence-root` takes any directory. A real dev run with `--evidence-root <clone>/corpus/evidence/round-44/oracle --carrier v1le` exited 0 and overwrote the tracked frozen file `corpus/evidence/round-44/oracle/manifest.json` (git: ` M`), plus created `corpus/evidence/round-44/oracle/v1le/`. The plan freezes `corpus/evidence/round-44/oracle/**`.
2. **`provenance_ok` is a substring test.** `c1-counter.py:1176-1182` checks `'/kaidoku-r49/' in output_directory`. Imported and called from the draft counter: `/tmp/kaidoku-r49/probe/rea-out` → True; `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/kaidoku-r49/x/rea-out` (lane-internal) → True; `/kaidoku-r49/x` (relative root) → True. The plan says "inside the `/kaidoku-r49/` scratch segment" and the contract says nothing under `/tmp` is citable. Only `/fast/scratch/hyaku/kaidoku-r49/…` should pass.
3. **Provenance and manifest are not counter-bound, and some provenance fields are constants.** The counter never opens `provenance.json`, `run.json`, `manifest.json`, `extract-env.json` or `extract-tree.tsv` (grep of `c1-counter.py`: only `run_provenance_ok` and comments). `c1-run.py:682` writes `'evidence_outdir_under_evidence_root': True` (constant); `:690` writes `'rewritten': False` (constant); `:684` writes `round_evidence_segment` (constant). The plan's parenthetical ("the runner copies … and records provenance.json; … that sentence is the one the counter implements") reads as if provenance were checked. It is not.
4. **Freeze arming is a bare flag.** `--data-run` / `KAIDOKU_C1_DATA_RUN=1` assert nothing: `--freeze deadbeef --data-run --fake-rea true --carrier v1le` on the default root passed the guard and wrote `corpus/evidence/round-49/c1/manifest.json` with `freeze: "deadbeef"`, `mode: "data-run"`, `rea_command: ["true"]` (exit 1, carrier failed). No check that FREEZE is an ancestor of HEAD or that `tools/round-49` and `plans/round-49-claims.md` are unchanged.
5. **Runner comments misquote the plan.** `c1-run.py:338-341` says the plan states "the receipt's parameters.output_directory names a corpus/evidence/round-49/c1/ path" and calls `--rea-outdir-mode evidence` "the binding the frozen claims text states". `grep -c "names a corpus/evidence/round-49/c1/" plans/round-49-claims.md` → `0`. The plan (line 79-82) says the output directory is inside `/kaidoku-r49/` and the committed path is NOT the output directory. The module docstring (`c1-run.py:27-31`) also presents as a quotation text that is not in the plan. This is the round-44 failure shape (plan text vs counter disagree about provenance); fix the comments to the plan sentence.

## Findings table

Commands are run from a dev clone `$C` = `mkclone.sh /fast/scratch/hyaku/kaidoku-r49/<seat>/clone` (remade from the base; `--lane-root "$C"`). `rc` = observed exit. sha256 = stdout/stderr file under `w1/C1RunReview/logs/` or the draft file. Severity: H/M/L.

| # | Sev | Finding | Command (exact) | rc | Evidence / sha256 |
|---|---|---|---|---|---|
| F1 | H | `--evidence-root` unrestricted; real write into frozen oracle dir | `c1-run.sh --lane-root "$C" --evidence-root "$C/corpus/evidence/round-44/oracle" --carrier v1le` | 0 | `git status`: ` M corpus/evidence/round-44/oracle/manifest.json`, `?? …/oracle/v1le/`. stdout `logs/x5r.out`. Dry form: `x5.out` sha256 `0e8b27823925683eebe96ae90fe603c1c790d1d4651fc7cd184c2a40d4638c51` |
| F2 | H | `--scratch` and `HYAKU_SCRATCH` unconfined | `c1-run.sh --lane-root "$C" --scratch "$C" --carrier v1le --dry-run` ; `HYAKU_SCRATCH=/tmp c1-run.sh --lane-root "$C" --carrier v1le --dry-run` | 0 | `--scratch $C` → run dir `$C/kaidoku-r49/probe-R49C1Run/…` (dry-run output, not kept as a file); `HYAKU_SCRATCH=/tmp` → `/tmp/kaidoku-r49/probe-R49C1Run/c1-run.v1le.<pid>/rea-out` (`d3.out` sha256 `c6a7b61d5a74be5b1024d987bb71ef7aba872747a90ad04deb61ee6f849e8bd8`). Code: `c1-run.py:837-841` creates `<base>/kaidoku-r49` with no check. |
| F3 | H | `provenance_ok` substring: accepts `/tmp/…`, lane-internal, relative `/kaidoku-r49/` | python: `importlib` load draft `c1-counter.py` (`-I -B`), call `provenance_ok(s)` | — | True for `/tmp/kaidoku-r49/probe/rea-out`, `<lane>/kaidoku-r49/x/rea-out`, `/kaidoku-r49/x`; False for `/fast/scratch/hyaku/kaidoku-r42/x`, `…/kaidoku-r49x/rea-out`, `…/kaidoku-r49/../kaidoku-r42/x`. Counter sha256 `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`. Fix: prefix match on `/fast/scratch/hyaku/kaidoku-r49/` (or the frozen `HYAKU_SCRATCH`), reject `..`, reject lane paths. |
| F4 | M | provenance/manifest/run/extract-env/tree never counter-read; hardcoded provenance fields | `grep -n "provenance.json\|extract-tree\|run.json\|manifest.json\|extract_env" c1-counter.py` | — | `c1-run.py:682,684,690` constants; counter has no reader. `provenance.json` in dev run: `evidence_outdir_under_evidence_root: true`, `rewritten: false` regardless of inputs. Fix: compute those fields and have the counter verify `extract-tree.tsv` against the committed files and `provenance.json.evidence_outdir`/`rea_output_directory`, or state in the plan that these files are documentary. |
| F5 | M | `--data-run`/env flag is the only arm; `--fake-rea` accepted on committed root; FREEZE not verified | `c1-run.sh --lane-root "$C" --data-run --freeze deadbeef --fake-rea true --carrier v1le` (on the clone's default root) | 1 | `logs/g5.err` sha256 `e1ed9673ca97fa20a39d08c9f529e7a91abacde00211e9c8c88ed8be7f0dc80e`; manifest `freeze: "deadbeef"`, `rea_command: ["true"]`. Fix: refuse `--fake-rea` on the default root; on data run require `--freeze`, `git merge-base --is-ancestor <FREEZE> HEAD`, and `git diff --quiet <FREEZE> -- tools/round-49 plans/round-49-claims.md`. KAIDOKU_C1_DATA_RUN=1 alone is equivalent by `c1-run.py:827` (not executed). |
| F6 | M | Exit 2 mid-run leaves partial committed tree and no manifest | make `$S/ev3/v2be/SENTINEL`; `c1-run.sh --lane-root "$C" --evidence-root "$S/ev3" --timeout 600` | 2 | v1be, v1le, v2le receipts written; `v2be` sentinel kept; no `manifest.json` (`logs/f2.err` sha256 `4a07eb1eda08e6dfa2d5c8656e3f32900e9e8108ce7fc24bfedae9cb13165602`). Fix: preflight `clear_outdir` checks for every plan before the first REA call. |
| F7 | M | Dangling symlink at outdir: REA runs, then uncaught `FileExistsError`, exit 1 not 2 | `ln -s $S/nonexistent ev6/v1le`; `c1-run.sh --lane-root "$C" --evidence-root "$S/ev6" --carrier v1le` | 1 | `logs/f4.err` sha256 `c264a7a448060ec96eb8b32462ae0e7f89c22cf8207db2e35adec8039f809a34`. `clear_outdir` uses `os.path.exists` (false for dangling); crash at `c1-run.py:587` after REA at `:570`. Fix: `os.path.lexists`. |
| F8 | L | `--include-exploratory` is a dead flag; v21 ids have no carrier entries | `c1-run.sh --lane-root "$C" --include-exploratory --dry-run` ; `--carrier v21le --dry-run` | 2 | `logs/x6.err` sha256 `491351b89c8a3736c994f85beacd173ce372c891e79ded3ea8ed7badf7f4f6b5` ("scope names ids with no carrier entry: v21be,v21le"); `--carrier v21le` → "no carrier matches". `carriers.json` scope note says "measured and retained" but has no entries. |
| F9 | L | Comments misquote plan (see top finding 5) | `grep -c "names a corpus/evidence/round-49/c1/" plans/round-49-claims.md` | — | `0`. `c1-run.py:27-31, 338-343`. |
| F10 | L | `--rea-outdir-mode evidence` writes receipts the counter rejects | `c1-run.sh --lane-root "$C" --evidence-root "$S/ev" --rea-outdir-mode evidence --dry-run` | 0 | `x3.out`: REA output_directory = evidence path (no `/kaidoku-r49/` segment → `provenance_ok` False). Refuse on data run. |
| F11 | L | npm side effects outside the segment on each REA call (not evidence; disclose) | `strace -f -qq -e trace=file … c1-run.sh --evidence-root "$S/ev" …` (dev run, 4 carriers) | 0 | Outside scratch: `~/.npm/_logs` 4 new logs + 4 unlinks of older logs; `~/.npm/_cacache/tmp` + `index-v5` 4 writes + 4 renames; `~/.npm/_npx/ad9a3fdbcad992c6/concurrency.lock` 4 mkdir + 4 rmdir. Full list: `strace-outside-writes.txt`; raw trace gz `logs/strace-f-dev-run.txt.gz` (raw sha256 `971c768f10202ddc3a33a4f60e010ee6f161e7e2ec9e1c1365fd66a384ddd759`). REA/unblob themselves write only under `TMPDIR` and the output root (4567 writes inside the scratch segment/evidence). |
| F12 | I | Scratch run dirs are deleted after each run, so the committed `output_directory` names a path that no longer exists | — | — | `probe-R49C1Run/…/rea-out` removed at end of `run_carrier` (`c1-run.py:755-756`); counter-time rerun is the only re-check. |
| F13 | I | Manifest `carriers` paths relative to lane (`../ev/…` for an external root); `round_evidence_segment` constant | dev run manifest | 0 | cosmetic; see F4. |

## Confirmed good (coverage of the seat's asks)

- **Carriers (dry run):** `v1le v1be v2le v2be`, the only scored ids; `scope.target_ids` equals these four; each carrier `sha256` pin matches the fixture on disk (`b45925fa…`, `529e1077…`, `7c62dbe3…`, `79c0f388…`).
- **Output directory:** `/fast/scratch/hyaku/kaidoku-r49/probe-R49C1Run/c1-run.<id>.<pid>/rea-out` in default `--rea-outdir-mode scratch`; real `after.json` confirms `parameters.output_directory` equals this path. Inside the segment.
- **Evidence paths (default root, dry, `d1.out`):** `<lane>/corpus/evidence/round-49/c1/<id>/` and `…/c1/manifest.json`.
- **Guard (default root, no `--data-run`):** exit 2 with no directory created. Spelled three ways: plain (`g1.err` `98d5…`), trailing slash + `..` (`g2`), symlink (`g3`). `KAIDOKU_C1_DATA_RUN=1` is equivalent by code (`c1-run.py:827`), not executed.
- **Dry-run writes nothing:** with `HYAKU_SCRATCH=$S/hs0` the scratch base was not created; clone `git status --porcelain` empty after dry runs (`d2b.out`, not kept as a file; observed in-session).
- **Pin mismatch fails closed:** flipped one byte in the clone's `v1le` fixture (sha `1209f508…` ≠ pin `b45925fa…`): rc 1, `status: failed`, `pin mismatch` in manifest, no REA call, no outdir created.
- **`--force` semantics:** replaces an occupied outdir (rc 0, sentinel removed, `f3.out`); on a symlink-to-directory removes only the link (victim kept, `f5.out`). Without `--force`, occupied outdir → rc 2, manifest sha unchanged (`f1.err`; manifest sha256 before = after prefix `0a4bdb2b…`).
- **Real scratch dev run (not a data run; evidence root non-default so no guard):** `c1-run.sh --lane-root "$C" --evidence-root "$S/ev" --timeout 600` → rc 0; four carriers `exit 0, receipt True`; `firmware.bin_extract` regular-file counts v1le 3, v1be 3, v2le 4, v2be 4 (match `expected_regular`). `run.json` `rev_at_run` = dev freeze hash.
- **Write surface of the REA chain:** strace over the four-carrier run shows no write to the lane tree and no write under `$HOME` other than npm's cache/logs (F11).

## Ways the data run could write outside `corpus/evidence/round-49/c1/` or the scratch segment

1. `--evidence-root <any>` (F1): writes `<root>/<id>/…` and `<root>/manifest.json`; `--force` removes `<root>/<id>`. Proven on a frozen path.
2. `--scratch <any>` / `HYAKU_SCRATCH=<any>` (F2, F3): creates `<any>/kaidoku-r49/probe-R49C1Run/…` and TMPDIR there. Proven by dry run; creation by code.
3. `--data-run` plus `--fake-rea` on the default root (F5): writes committed root with a non-REA command. Inside the evidence root but not claim-valid.
4. npm's global cache and logs (F11): `~/.npm/_logs`, `~/.npm/_cacache`, `~/.npm/_npx/ad9a3fdbcad992c6/concurrency.lock`. Outside the segment; benign; disclose.
5. Partial committed output on exit 2 (F6, F7): not an outside write, but a non-atomic committed tree with no manifest.
6. `--include-exploratory` / `--carrier` for ids in `carriers.json`: currently only the four scored ids exist; a future Frontier entry would be written under `--carrier <id>` with no scope check (`c1-run.py:870`). No such entry exists today (X1, F8).

## Recommended fold-ins (for the draft before freeze; not applied)

- Confine `--evidence-root` for any non-dry run to `<lane>/corpus/evidence/round-49/c1` (realpath) or refuse exit 2; same for `--scratch`/`HYAKU_SCRATCH` to `/fast/scratch/hyaku/kaidoku-r49`. Refuse `--fake-rea` and `--rea-outdir-mode evidence` on data runs.
- Preflight every carrier's occupancy before the first REA call; use `os.path.lexists`.
- Require `--freeze` on data runs with ancestry and blob checks against `tools/round-49` and `plans/round-49-claims.md`.
- Tighten `provenance_ok` to the literal segment prefix and reject lane-internal and `/tmp` paths; add a mutation to the controls (`output_directory` under `/tmp/kaidoku-r49/`, under `<lane>/kaidoku-r49/`, and `/kaidoku-r49/x`) that must read red.
- Either have the counter verify `provenance.json` / `extract-tree.tsv` or state in the plan that they are documentary; drop constant fields or compute them.
- Correct `c1-run.py` comments at 27-31 and 338-343 to the plan sentence; drop the "binding the frozen claims text states" wording for evidence mode.
- Remove `--include-exploratory` or add the v21 entries the scope note describes.

## Verification gaps / not run

- `--data-run` not run (seat contract). No evidence written to the committed root by this seat.
- `KAIDOKU_C1_DATA_RUN=1` alone (no flag) not executed; equivalence by code only.
- Counter not run end-to-end on the dev receipts (outside this seat). F3 was checked by calling `provenance_ok` directly.
- REA run (dev arm) used the npx cache `rea-agents@6.5.0` under `~/.npm/_npx/ad9a3fdbcad992c6`. No package install occurred.

## Tooling

No installs or upgrades. Used existing `/usr/bin/strace` (version 7.2), `unblob` 26.6.4 at `~/.local/bin/unblob`, and `npx` on the fixed PATH. `pacman` not used. `disk-guard.sh status` rc 0 before the heavy pass.

## Artifacts

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/w1/C1RunReview/`: `SHA256SUMS.txt` (sha256 of every copied file), `strace-outside-writes.txt`, `logs/` (run, guard, flag and error captures; gzipped raw strace; the draft `c1-run.py` and `c1-run.sh` copies), `receipts-dev-run/` (the four dev-arm receipt trees, manifest, `after.json` files). Draft sha256: `c1-run.py` `f9161ff3afa2ded9553ea77dc31432add67ca6f6a02e98b3eb22c74da33a46fb`; `c1-run.sh` `5ebb453f6197a8d2fc7790e80ae3d357e0053e8bf9191cdb95d946ee78c0d366`; `c1-counter.py` `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779`.

Scratch `$S` removed after copying.
