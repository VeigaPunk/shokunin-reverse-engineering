# R46W1RegC — command receipt (round 46, wave 1, tag reg-c)

Freeze parsed from the seat spec: `31820472784284727546808acc31b3ea1e73919b`.
All instruments were read and run from Git blobs at that commit, except where the row says
so; the lane working tree was being edited by sibling seats during this wave, so a
working-tree run is never cited as a revision result (see `probe-dirty-worktree` below).
Scratch `S=/fast/scratch/hyaku/kaidoku-r46/R46W1RegC` (removed after these receipts were
copied here). No tool was installed; nothing needed installing.

## A. Row-claim probes (each row's claim verified by a command actually run)

| # | exact command | exit | stdout sha256 | UTC | note |
|---|---|---|---|---|---|
| a1 | `bash /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/c1-run.sh` | **2** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:52:30Z | usage on stderr (sha `d9509fc272b314f2ea634d68ce5fba9985c21d270b411eaead78b9a9f505bf5`); proves cell-3 `2=usage` |
| a2 | `bash …/tools/round-41/c1-run.sh bogus carrier out` | **2** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:52:30Z | byte-identical usage on stderr; a wrong mode is a usage refusal, not a verdict |
| a3 | `python3 -I -B …/tools/round-42/c2-controls.py` | **2** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:52:30Z | argparse: `error: the following arguments are required: --root, --dev, --out, --json-out` (stderr sha `5c374a56bce6cf301f46f2966c3fa5b0352485f88783260587586f4ddf80739a`) |
| a4 | `python3 -I -B …/tools/round-42/c2-controls.py --root S/probe/lane --dev S/probe/dev-empty --out S/probe/out2 --json-out S/probe/out2/j.json` | **1** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:52:39Z | stderr `no envelopes under [...]` — **an unevaluable run returns 1** |
| a5 | `python3 -I -B …/tools/round-42/c2-controls.py --root S/probe/lane --dev S/probe/dev1 --out S/probe/out3 --json-out S/probe/out3/j.json` | **1** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:52:39Z | stderr `evaluator failed on … (exit 2): … preview-precedence.py: No such file` — **second unevaluable path returning 1** |
| a6 | `python3 -I -B …/tools/round-44/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work S/w-selftest` | **0** | `fbe23fefc21c12358232a8146947a3da39e96fc1d359fa9f61ec36178310da1c` | 2026-10-28T16:52:39Z | stdout `{"cases": 47, "failures": [], …}`; **byte-identical to the round-45 receipt's sha** in `.ufo/waves/round-45/w1/R45W1RegR44C1Counter/receipt.md` |

Not exercised (say-so recorded, not passed): the exit-0 paths of `c1-run.sh` (needs REA,
unblob and a carrier) and of `c2-controls.py` (needs DEV envelopes plus the
`v4-check-interp.py` / `preview-precedence.py` replicas, which **do not exist** at the
freeze — `git ls-tree -r 3182047 tools/round-42` has no match for `interp|precedence`).
Exit 0 for `c2-controls.py` is read from source line 601 (`return 1 if full else 0`).

## B. Exit codes outside {0,1,2}

- `tools/round-41/c1-run.sh` exits **3** on tool failure (`fail()` at line 94; `exit 3` at
  line 604). Header states `Exit: 0 ok, 2 usage/environment error, 3 tool failure`. It has
  no designed exit 1: under `set -euo pipefail` only an unguarded command failure can
  surface status 1. The row's cell 3 says so without naming 3, per the seat rule.
- `tools/round-42/c2-controls.py` exits **1** for both "a control reached full score" and
  the unevaluable `SystemExit(<str>)` diagnostics (measured, a4/a5). That is a calibration
  defect in the instrument, not a row-format issue.
- `tools/round-44/c1-counter.py` uses exactly {0,1,2} in its designed contract, but a
  `SystemExit(<str>)` inside `--selftest` (missing/unusable `--pkg65`) also lands on 1.

## C. Rows checked against the frozen counter

| # | exact command | exit | stdout sha256 | UTC | result |
|---|---|---|---|---|---|
| c1 | static check: 7 cells, cell 1 exactly the backticked path, EXITMAP `\b([012])\s*[=:]` keys `{0,1,2}`, zero backticks outside cell 1 (frozen regexes) | — | — | 2026-10-28T16:53:25Z | 3/3 rows pass all four |
| c2 | `python3 -I -B <fixture>/tools/round-46/registry.py --root <fixture> --freeze HEAD --rev HEAD --no-battery --json-out <fixture>/.ufo/fx-a-out.json` | **0** | `0aa9bbd63b393758398877e7ba5a1d13f5a17f7472de0a6162edeae35314288c` | 2026-10-28T16:53:30Z | `scope_size 3`, `registered` = my three paths, `unregistered []`, `thin []`, `absent_at_rev []`, `met_target true`, `failing []` (receipt `fixtures/fx-a-rows-only.json`) |
| c3 | same, section = the **round-45** row for `tools/round-44/c1-counter.py` only | **1** | `1bc554160ff862e8ddd7ea2bbae640ca04cd7db1cd6f9334f03281017b799cdf` | 2026-10-28T16:53:46Z | `thin ["tools/round-44/c1-counter.py"]` — the landed round-45 row is thin under v2 (receipt `fixtures/fx-c-old-row-only.json`) |
| c4 | same, **old row first, my row appended** | **1** | `554610f1153093e2dc8b04e5eb6d23edea6b373f7a07d9af6f0a71cb3b8601e6` | 2026-10-28T16:53:46Z | `thin ["tools/round-44/c1-counter.py"]` — `by_path.setdefault` is first-wins, so **appending cannot repair a thin row** (receipt `fixtures/fx-d-old-then-new.json`) |
| c5 | same, **my row first, old row after** | **0** | `270e4c6419b2fa274df1db69c9118b3fb362464628fee2d55995ff545064c611` | 2026-10-28T16:53:46Z | `thin []`, `met_target true` (receipt `fixtures/fx-e-new-then-old.json`) |

Fixture construction: `git -C "$D" init -q`, `rev-parse --show-toplevel` asserted equal to
`$D` before the first commit, one commit `fixture` per repo with a throwaway
`GIT_AUTHOR_*`/`GIT_COMMITTER_*` identity inside that repo only. `SKILL.md`, the claims
file, the three registered tools and `tools/round-46/{registry.py,gate.py}` were written
from `git show 3182047:<path>`; `census.json` was filtered to my three paths; my section is
the house header, separator and the three rows.

## D. The frozen instruments themselves (wave 1 context, same lane, read-only)

| # | exact command | exit | stdout sha256 | UTC | result |
|---|---|---|---|---|---|
| d1 | `python3 -I -B …/tools/round-46/registry.py --selftest` (the literal command the claims' preflight names) | **2** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T16:54:09Z | argparse: `--root, --freeze, --rev` are required even for `--selftest`; the preflight sentence does not run |
| d2 | `python3 -I -B <3182047 blob>/tools/round-46/registry.py --selftest --root /nonexistent --freeze HEAD --rev HEAD` | **0** | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | 2026-10-28T16:55:17Z | `REGISTRY_SELFTEST: cases=12 failures=0` — the claims say **cases=11** |
| d3 | `python3 -I -B <3182047 blob>/tools/round-46/attest.py --selftest --root /nonexistent --freeze HEAD --rev HEAD` | **0** | `ac22e9c7acb4bb6fc66b98bdb203190dc64f18bb7121e686f02fa195810e8ddb` | 2026-10-28T16:55:17Z | `ATTEST_SELFTEST: cases=15 failures=0` (arms written as `case(...)` call sites; matches the claims only in the count) |
| d4 | `python3 -I -B <65678df0 blob>/tools/round-46/attest.py --selftest --root /nonexistent --freeze HEAD --rev HEAD` | **0** | `0bf8f4c6ae0e46a0c4f00b9eb8b573afd7c10b0bbb6bf7e2ce58e7c2c5296dd8` | 2026-10-28T16:55:43Z | `cases=16 failures=0`; repeated 3× from the blob copy and 2× via the lane path, byte-identical sha each time |
| d5 | `python3 -I -B <65678df0 blob>/tools/round-46/registry.py --selftest --root /nonexistent --freeze HEAD --rev HEAD` | **0** | `0fa8c31a6419905fcb1971cb32631862be682014339a9e390634d360fd11872e` | 2026-10-28T16:55:44Z | `cases=12 failures=0` |
| d6 | `python3 -I -B <3182047 blob>/tools/round-46/registry.py --root <lane> --freeze 3182047… --rev 3182047… --no-battery` | **1** | `d89e522fc10b4cc87f71b096f47ff25de52d7c2d071e7e75600172695505d95d` | 2026-10-28T16:55:36Z | `failing: ["markers: 0 open, 0 close", "header != house schema (7 cells)", "unregistered: 38 of 38"]`, `scope_size 38` — the true "Before" for R46-C2 at the freeze |
| d7 | `python3 -I -B <3182047 blob>/tools/round-46/registry.py --root <lane> --freeze 3182047… --rev 6e018068… --no-battery` | **2** | `9c3f8f953bf6189977b467a83be80c6f2e40be38c10d7620244ff0c1a9d4a019` | 2026-10-28T16:55:36Z | `reason: frozen_path_changed`, `frozen_path_changed: ["tools/round-46/", "tools/round-46/attest.py", "tools/round-46/gate.py", "tools/round-46/registry.py"]`, `restored` = the three files |
| d8 | `probe-dirty-worktree`: `python3 -I -B <lane>/tools/round-46/attest.py --selftest --root /nonexistent --freeze HEAD --rev HEAD` | **1** | `ca384eb960d97e1dc2c388c1fa7781e0e92d73cb084bda08c702b13a6b6a6a3e` | 2026-10-28T16:54:25Z | `cases=16 failures=1`, failing case `green-with-battery: battery v1_green 5 != 9`. The same file bytes (sha `e6c44d2d…`) run five times at d4 returned `failures=0`; the shared working tree was dirty at 16:54:2x, so this run is **not attributable to any commit** and is retained only as evidence that a working-tree run is not a revision result |
| d9 | inline read-only audit of `.ufo/waves/round-46/l1/registry-section.md` with the frozen v2 rule (7 cells, `EXITMAP` keys `{0,1,2}`) | **0** | `1e7c011cbda23bd5bf94566a7eb3d46d3d0d375748403a7d258971e3fc0a6420` | 2026-10-28T16:58:26Z | `rows=38 thin=3 unregistered_placeholders=3`; thin = the `UNREGISTERED` placeholders for `tools/round-41/sqfs-list.py`, `tools/round-43/c1-counter.py`, `tools/round-46/registry.py` |

## E. Files written

- `.ufo/waves/round-46/w1/R46W1RegC/rows.md` — the three rows, verbatim for the L1.
- `.ufo/waves/round-46/w1/R46W1RegC/receipt.md` — this file.
- `.ufo/waves/round-46/w1/R46W1RegC/fixtures/{fx-a-rows-only,fx-c-old-row-only,fx-d-old-then-new,fx-e-new-then-old}.json`
  — the frozen counter's own receipts for c2–c5.
- `.ufo/waves/round-46/w1/R46W1RegC.md` — the report.
