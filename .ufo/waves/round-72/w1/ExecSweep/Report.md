# ExecSweep — round-72 w1 instrument sweep (seat ExecSweep, 2026-11-04)

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. All commands run with `cwd` = the lane
(the seat shell starts at the fleet root; every command below was executed from the lane).
Receipts (verbatim stdout/stderr/rc per command, plus `sweep.json`) are in this directory.
Scratch `/fast/scratch/hyaku/kaidoku-r72/ExecSweep/` was created once and deleted before yield.

Godspeed axes: evidence coverage (all six assigned commands + one bonus operability run),
verdict precision (each anomaly judged against the routed-defect criteria), zero out-of-bounds
writes (lane-only), receipts retained in-lane.

## 0. Lane state at start (read-only git)

`git status --porcelain` rc=0 — untracked only, no tracked file modified:

| path | judgment |
|---|---|
| `.ufo/waves/round-72/l1/pre/receipt-r72-lying.json` | untracked file inside the otherwise-tracked frozen `l1/pre/` receipt set (its round-71 sibling `receipt-r71-lying.json` IS tracked). Plausibly in-flight L1 work; **freeze-hygiene flag for the L1** — not touched. |
| `.ufo/waves/round-72/l1/scores/c1-at-landing.json` | appeared between my first status and the sweep run — live L1 scoring in flight; expected wave artifact. |
| `.ufo/waves/round-72/r72-w1.ready`, `.ready.dispatched` | wave dispatch markers; expected. |
| `.ufo/waves/round-72/w1/` | seat output directory (includes these files); expected. |

HEAD at sweep time: `6375afe687bc03603eab8387f2defc4fa1248054` ("round-72 supersession: the
probe's scratch blob copy carries the route's sibling module (capsule_audit.py), so a black-box
invocation can import it"). The bonus battery run (item 7) pins that rev explicitly.

## 1. Command / rc / verdict table

| # | command (cwd = lane) | rc | verdict |
|---|---|---|---|
| 1 | `git status --porcelain` | 0 | Untracked paths per §0; no tracked modification. |
| 2 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 (0 required ✓) | Final line `ok .../corpus/SOURCES.md`. **Warnings: 22**, all `W04 duplicate url … across scopes` (S138, S142, S245–S248, S271–S273 in the visible tail; full list in `sources-census.out`). Non-blocking cross-scope duplicate-url notes. |
| 3 | `python3 -I -B tools/round-71/registry-census.py --root . --rev 56241b1c8baff95862730c008f1ae5132b03388e --generate --out <scratch>/registry.json` | 0 | `ok: true`; **rows 93, nonconformant 0, duplicates 0**, findings 0, legacy/multicell rows 4 (the four r69 8-cell rows; grammar v2 joins cells 4:-2). Copy retained as `registry.json`. |
| 4a | `python3 -I -B tools/round-72/packed-elf.py --selftest` | 0 | cases 35, `failed: []` — green. |
| 4b | `python3 -I -B tools/round-72/seam-probe.py --selftest` | 0 | cases 10, `failures: []` — green. |
| 4c | `python3 -I -B tools/round-72/mutation-check.py --selftest` | 2 | **No `--selftest` mode** (argparse: unrecognized argument). By design: this battery *consumes* the target instrument's `--selftest` (docstring; `run_selftest()`). Self-equivalent executed for real — item 7, rc 0. |
| 4d | `python3 -I -B tools/round-72/capsule-audit.py --selftest` | 0 | cases 13, `failed: []` — green. |
| 4e | `python3 -I -B tools/round-72/capsule_audit.py --selftest` | 0 (empty output) | Pure **library module** (no argparse, no `__main__`): imports and exits silently. Exercised via `capsule-audit.py` (sys.path insert + `import capsule_audit`) and the battery's sibling-copy logic. Not a defect. |
| 4f | `python3 -I -B tools/round-72/controls.py --selftest` | 2 | **No `--selftest` mode**; requires `--root/--base-rev/--decl-rev/--receipt/--commitment/--expect-upx/--work`. Operability at the declaration is already evidenced by the pre-existing receipt `.ufo/waves/round-72/l1/pre/controls-at-declaration.json`; not re-run here to avoid duplicating the scoring seats' command. |
| 4g | `python3 -I -B tools/round-71/registry-census.py --selftest` | 0 | cases 14, `failures: []`; all 14 named sub-cases true — green. |
| 5 | no-/tmp scan of `tools/round-72/*.py` | — | 12 literal `/tmp` occurrences in 3 of 6 files (capsule-audit 1, packed-elf 6, seam-probe 5; capsule_audit/controls/mutation-check 0). **All 12 judged not defects** — see §2. No hardcoded scratch root → no routed defect. |
| 6 | `python3 -I -B tools/round-70/packed-elf.py --check-receipt .ufo/waves/round-72/l1/pre/route-at-declaration.json --root . --rev 6316c1053f927a1a1cdc3e0960b70acab5f56381` | 1 | **Expected producer-binding rejection, labeled — not a defect.** Check R70-C3, `met: false`, `failing` names exactly: (a) `instrument.path tools/round-72/packed-elf.py != tools/round-70/packed-elf.py`; (b) `instrument.sha256 973d504b… != blob at 6316c105… (417b1168…)`. The round-70 checker otherwise consumes the receipt structurally (`carriers_matched: 4`, per-carrier ceilings emitted). The round-72 receipt is correctly bound to the round-72 producer; the round-70 checker refuses it by design. |
| 7 | BONUS `python3 -I -B tools/round-72/mutation-check.py --root . --rev 6375afe687bc03603eab8387f2defc4fa1248054 --tool tools/round-72/seam-probe.py --patch-set r72 --work <scratch>/mc-work --json-out <scratch>/mutation-check-r72.json` | 0 | `ok: true`; pristine selftest 10/10 green; the r72 patch set's `A10_binding_force_true` applied and **KILLED naming `a10-binding-from-checker`**; survivors 0; `killed_wrong_case` 0; `target_pin.matched: true`; target sha256 `d1811680…`. The round-71 survivor dies on the round-72 probe — sweep-side (non-scoring) operability + calibration evidence for R72-C2. |

## 2. no-/tmp scan — every literal occurrence, judged

| file:line | text | judgment |
|---|---|---|
| capsule-audit.py:21 | docstring "…never /tmp; the instrument writes nothing beside its inputs" | documented non-fallback note |
| packed-elf.py:28 | docstring "HOME and TMPDIR inside --work, never /tmp" | documented non-fallback note |
| packed-elf.py:164 | comment "never fall back to /tmp (round-69 M69-11)" | documented non-fallback note |
| packed-elf.py:214 | docstring "never a /tmp fallback, round-69 M69-11" | documented non-fallback note |
| packed-elf.py:1151 | selftest comment "…no /tmp" | comment |
| packed-elf.py:1158 | `not ce["HOME"].startswith("/tmp") and not ce["TMPDIR"].startswith("/tmp")` | negative assertions (×2 occurrences) |
| seam-probe.py:29 | docstring A6 "…back to /tmp: the receipt's child_env HOME lives" | documented non-fallback note |
| seam-probe.py:30 | docstring "inside --work, and the blob carries no /tmp HOME" | documented non-fallback note |
| seam-probe.py:84 | `TMP_FALLBACK_PATTERN = 'os.environ.get("HOME", "/tmp")'` | detection needle — the forbidden pattern's literal, used to assert its ABSENCE in the audited blob (A6) |
| seam-probe.py:429 | comment "…never falls back to /tmp" | comment |
| seam-probe.py:435 | `str(cenv.get("home", "")) != "/tmp"` | negative assertion |

Verified occurrence counts per file (independent string count): capsule-audit.py 1,
capsule_audit.py 0, controls.py 0, mutation-check.py 0, packed-elf.py 6, seam-probe.py 5.
**Zero hardcoded scratch roots; zero `/tmp` fallbacks in code paths.**

## 3. Findings and risks

- **F1** `mutation-check.py` and `controls.py` expose no `--selftest`; the standing duty's
  "--selftest for all six" is only partially satisfiable as written. Recorded honestly; their
  self-equivalents are the full battery run (item 7, rc 0) and the declaration-time controls
  receipt, respectively. No action taken beyond recording (duty = sweep; not authorized to add
  modes to frozen instruments).
- **F2** `capsule_audit.py` is silent under any argv (library). A validator that expects JSON on
  stdout from every instrument would misread rc 0 + empty output as a vacuous pass — worth a
  clause in the freeze-gate notes. Recorded, not modified.
- **R1** Untracked `l1/pre/receipt-r72-lying.json` in the frozen receipt dir (§0) — L1 decision;
  untouched.
- **R2** Lane was live during the sweep (L1 landing `l1/scores/c1-at-landing.json` mid-sweep).
  My commands read only frozen declaration-state receipts; no interference observed.
- No tool installs or upgrades performed (python3 present; host pacman pause respected; nothing
  to record under the operator 2026-10-19 tooling authorization).

## Receipts (this directory)

`sweep.json` (argv + rc + full stdout/stderr for items 1–6), per-command `*.out` / `*.err` /
`*.rc`, `registry.json` (item 3 output), `mutation-check-r72.{json,out,err,rc}` (item 7).
Report trailer path: `.ufo/waves/round-72/w1/ExecSweep.md`.

Report: .ufo/waves/round-72/w1/ExecSweep.md
