# MutationTester-4 — round-77 w1 mutation scoring

Seat: MutationTester-4 · Lane: kaidoku-shokunin · Base: `188562d43e3cc58b217ad7aa763fb296c5b8a0b7`
Receipt: `.ufo/waves/round-77/w1/MutationTester-4/mutation-receipt.json`
Raw detector outputs: `.ufo/waves/round-77/w1/MutationTester-4/pristine-{c1,c2}.selftest.json`, `mut-<name>.selftest.json` (10 files)

## Method

Both instruments were copied to the seat scratch `/fast/scratch/hyaku/kaidoku-r77/MutationTester-4/`
(now deleted). Each mutant is a single exact byte replacement (anchor asserted `count == 1`)
on a scratch copy; the detector is `python3 -I -B <instrument> --selftest` against pristine,
mutant, and lane bytes. Survivors were additionally probed behaviorally to demonstrate the
hole the selftest cannot see. Lane instruments were only ever read.

## Pristine baseline

| Instrument | SHA-256 (pristine = lane) | Selftest | Result |
|---|---|---|---|
| `tools/round-77/verdict-bind.py` | `45280392ff6c59e4c96041544720f055952a11a088769e24cb04207db932a9e7` | 15 cases | 0 failures, exit 0 |
| `tools/round-77/prefile-receipt.py` | `174eedb56369414f5e4310afa9fe5ee6400e5145e4801452c9d21a7abac2d3fd` | 13 cases | 0 failures, exit 0 |

## Scoreboard — 10 mutants, 8 killed, 2 survivors

| # | Instrument | Mutant | One decision changed | killed_by | sole_detector | Verdict |
|---|---|---|---|---|---|---|
| 1 | C1 | `c1-drop-typed-check` | `typed_equal` drops `type()` strictness → `True == 1` binds | `red-type-mismatch` | `red-type-mismatch` | killed |
| 2 | C1 | `c1-drop-atom-lookup` | atom-id fields never resolve via `receipt.atoms` | `red-false-annotation`, `green-same-cell-true` | both (unique) | killed |
| 3 | C1 | `c1-rev-show-to-worktree` | `show()` reads the working tree instead of `git show <rev>:<path>` | — | — | **SURVIVOR** |
| 4 | C1 | `c1-of-ignore-total` | `N of M` ignores the `<field>_total` half | `red-of-total` | `red-of-total` | killed |
| 5 | C1 | `c1-unknown-field-pass` | unknown field scores as bound pass instead of unbound | `unbound-unknown-field` | `unbound-unknown-field` | killed |
| 6 | C1 | `c1-absent-receipt-clean` | missing named receipt skips silently, no `absent_receipt` | `red-absent-receipt` | `red-absent-receipt` | killed |
| 7 | C2 | `c2-nonint-exit-accepted` | `check_receipt` accepts a str/bool `exit` | — | — | **SURVIVOR** |
| 8 | C2 | `c2-skip-stdout-digest` | `stdout_sha256` never re-derived from `stdout` | `red-digest` | `red-digest` | killed |
| 9 | C2 | `c2-verdict-exit-disagreement-ok` | `passed`/verdict-vs-`exit` agreement check disabled | `red-verdict` | `red-verdict` | killed |
| 10 | C2 | `c2-skip-env-keys-check` | `env_keys` not compared to the four-key allowlist | `red-env` | `red-env` | killed |

`survivor_count: 2` · `sole_detector_conflict: []` (no killed_by set is shared, every killed
mutant owns at least one killing case no other mutant is killed by; no survivor shared).

## Survivors (coverage findings — record only; no contract or production file touched)

### S1 · C1 `c1-rev-show-to-worktree`

Change (in `show()`):

```diff
-    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
-                          capture_output=True)
-    if proc.returncode != 0:
-        return None
-    return proc.stdout.decode("utf-8", "replace")
+    try:
+        return pathlib.Path(root, path).read_text(encoding="utf-8")
+    except OSError:
+        return None
```

Selftest under mutant: `cases 15, failures [], exit 0` (`mut-c1-rev-show-to-worktree.selftest.json`).
The selftest scores the grammar through a fake resolver (`cell_case`) and never exercises the
`--rev` byte-access path, so a swap of frozen-revision reads for working-tree reads is invisible
to all 15 cases — precisely the forgery surface the claim ("re-derived at the measured revision")
depends on.

Behavioral probe (scratch fixture repo, `rev-parse --show-toplevel` asserted equal to the
fixture before commit):

- pristine `show(fixture, "HEAD", "probe.txt")` → `committed-bytes\n`
- mutant `show(fixture, "HEAD", "probe.txt")` → `working-tree-bytes\n`

### S2 · C2 `c2-nonint-exit-accepted`

Change (in `check_receipt`):

```diff
     exit_code = receipt.get("exit")
-    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
-        defects.append(f"exit is not an integer: {exit_code!r}")
-        return defects
```

Selftest under mutant: `cases 13, failures [], exit 0` (`mut-c2-nonint-exit-accepted.selftest.json`).
All 13 cases either remove the `exit` key (caught earlier by the `missing key exit` loop) or
keep it an `int`; no case feeds a present-but-non-integer `exit`.

Behavioral probe: a receipt with `"exit": "1"` (string), `passed false`, a `prefile: FAIL`
verdict and consistent digest/argv/env_keys —

- pristine `check_receipt` → `["exit is not an integer: '1'"]`
- mutant `check_receipt` → `[]` (forgery accepted)

## Restoration evidence

| Bytes | before | after | equal |
|---|---|---|---|
| lane `tools/round-77/verdict-bind.py` | `45280392…db932a9e7` | `45280392…db932a9e7` | yes |
| lane `tools/round-77/prefile-receipt.py` | `174eedb5…7abac2d3fd` | `174eedb5…7abac2d3fd` | yes |

All mutants ran on scratch copies; `lane_bytes_restored: true` in the receipt. Scratch
`/fast/scratch/hyaku/kaidoku-r77/MutationTester-4/` deleted via `trap … EXIT` after receipts
were copied here. No git writes anywhere; the only `git init/commit` was inside the scratch
fixture with `rev-parse --show-toplevel` asserted first. No tool was installed or upgraded
(nothing beyond the stock `python3`/`git` was needed).

## Findings for the record (routed to L1; this seat changed nothing)

1. **C1 selftest gap:** no case pins `--rev` byte resolution to `git show`; add a red fixture
   whose working tree disagrees with the measured revision (e.g. score the grammar against a
   resolver backed by a fixture repo where `HEAD:path` ≠ worktree `path`).
2. **C2 selftest gap:** no red fixture carries a non-integer `exit` (string `"1"` / bool /
   `null` with the key present); the typed-`exit` decision is enforced but untested — suggest
   `red-exit-string` alongside the existing `red-no-exit`.
3. Eight of the ten one-decision mutants are each killed by a distinct named case, so the two
   selftests carry genuinely independent red fixtures per failure shape (matches the frozen
   claim sentences' "one red fixture per failure shape" wording for the shapes they cover).
