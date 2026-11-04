# ExecControls — R66-C1 do-nothing controls + three fail-ability arms

Frozen inputs read-only throughout; pins re-checked before running:

- `tools/round-66/closure-boundary.py` sha256 `3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b`
- `tools/round-66/coverage-selfcheck.py` sha256 `1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa`

Scratch: `/fast/scratch/hyaku/kaidoku-r66/ExecControls` (deleted before yield). Receipts:
`.ufo/waves/round-66/w1/ExecControls/`. Interpreter: `python3 -I -B` (system), fixture/toolchain
probe interpreter `/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python` as the counter defaults.

## 1. Committed C1 do-nothing control — reproduced

Command:

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r66/ExecControls python3 -I -B \
  .ufo/waves/round-66/l1/controls/c1-do-nothing.py \
  --repo /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --out .ufo/waves/round-66/w1/ExecControls/c1-do-nothing.json
```

Exit 0 (control semantics: nonzero only if the control meets the target, which would indict the
counter). Rerun receipt is JSON-equal to the committed
`.ufo/waves/round-66/l1/controls/c1-do-nothing.json`: `passed 1 / arms_total 5`, `ok false`.
Only `a1-guarded-fixture-green` passes; a2/a3/a4/a5 fail on the r65-order defects (pre-probe cache
scan, unasserted count, synthetic skip-run closure). Receipt sha256
`bbcc70c4674256a7320e126dba80c55762ec2946514086b770e2053a65284850`.

## 2. Committed C2 do-nothing control — reproduced

Command:

```
TMPDIR=/fast/scratch/hyaku/kaidoku-r66/ExecControls python3 -I -B \
  .ufo/waves/round-66/l1/controls/c2-do-nothing.py \
  --repo /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev 311079d869f068bc083a8d180977e49634120fdf \
  --out .ufo/waves/round-66/w1/ExecControls/c2-do-nothing.json
```

Exit 0. Rerun receipt is JSON-equal to the committed
`.ufo/waves/round-66/l1/controls/c2-do-nothing.json`: `passed 0 / conditions_total 3`, `ok false`.
Receipt sha256 `f4599e1b840e951f28a535b6f5197f066742ccb1d36f1f56e0aa2c51f0c8ec24`.

## Baseline (same harness, unmutated counter)

```
TMPDIR=$S python3 -I -B tools/round-66/closure-boundary.py --verify \
  --repo /home/vgpnk/Projects/shokunin/kaidoku-shokunin --work $S/work-base \
  --out .ufo/waves/round-66/w1/ExecControls/base-verify.json
```

Exit 0, `passed 5 / 5`, `ok true` (`base-verify.json`). This is the positive control for the three
mutants below: same interpreter, same flags, same scratch root.

## 3. Arm-mutation A — the count assertion must be load-bearing

Mutation: copy of the counter with `COUNT = 30` → `COUNT = 29`; r65 pin load untouched.
Mutant sha256 `ad121361f68705c209f76ce62d8a1c20a636a273c01764ec68b309a1aa65939d`.

```
TMPDIR=$S python3 -I -B $S/m1.py --verify --repo <lane> --work $S/work-m1 \
  --out .ufo/waves/round-66/w1/ExecControls/m1-verify.json
```

Exit **1**, `passed 3 / 5`, `ok false`. **Flipped: `a3-real-manifest-count-green` and
`a4-truncated-manifest-red`.**

- a3: `entries 30 != 29`, `count_ok false`, `ok false` → arm fails.
- a4: `entries 29`, `count_ok true`, `ok true`, findings empty → the truncated manifest silently
  greens, exactly the r65 C1-F2 defect the repaired arm exists to catch → arm fails.

Verdict: the `COUNT` assertion is load-bearing for both count arms; a count-blind counter loses
2/5 and cannot pass the predicate. Receipt sha256
`fcf105dc69e6d9a7228220b63c8ddc22ec018f122a6a3e886e17a6e499d86540`.

## 4. Arm-mutation B — the ordering must be load-bearing

Mutation: second copy with `post_cache = mod.cache_entries(root)` moved before
`probe_ok, probe_msg = probe_fn()`; the `ok` expression uses the moved value. Mutant sha256
`d779dd42db7dc1f2072bf9267d97e55234a0efacc4f5d67c8dac0743c8756114`.

```
TMPDIR=$S python3 -I -B $S/m2.py --verify --repo <lane> --work $S/work-m2 \
  --out .ufo/waves/round-66/w1/ExecControls/m2-verify.json
```

Exit **1**, `passed 4 / 5`, `ok false`. **Flipped: `a2-unguarded-fixture-red`.**

- a2 detail: `ok true`, `cache_present []`, `findings []`, probe ok — the unguarded probe's
  `__pycache__/fixture_mod.cpython-315.pyc` is written after the (moved) scan and is invisible, so
  the arm cannot fail. a1/a3/a4/a5 still pass, isolating the flip to the ordering.

Verdict: the post-probe cache scan is load-bearing; a pre-probe scan reproduces the r65 C1-F1
ordering defect and loses a2. Receipt sha256
`df97ec43bed8b696e1c7e4d0175e200e4292d858b5bb25db31711c00c1b3a8d5`.

## 5. Arm-mutation C — skip-run must stay honest

Mutation: third copy whose `skip_run_receipt` returns
`"closure": {"ok": True, "entries": 30}, "closure_claimed": True` with the other keys unchanged
(`verified: false`, `exit: 1` untouched). Mutant sha256
`933052f6f67b711b8dd56607ae4383a4d3c6a94becc84fe3e34c137c9d917bb8`.

```
TMPDIR=$S python3 -I -B $S/m3.py --skip-run --repo <lane> \
  --out .ufo/waves/round-66/w1/ExecControls/m3-skiprun.json      # exit 1
TMPDIR=$S python3 -I -B $S/m3.py --verify --repo <lane> --work $S/work-m3 \
  --out .ufo/waves/round-66/w1/ExecControls/m3-verify.json       # exit 1
```

`--skip-run` emits `"closure": {"entries": 30, "ok": true}` and `"closure_claimed": true` — a
closure object claiming ok that no run evaluated. `--verify` exits **1**, `passed 4 / 5`.
**Flipped: `a5-skip-run-no-closure`** (detail `{"closure": {"entries": 30, "ok": true},
"closure_claimed": true}`); a1–a4 still pass.

Verdict: a5 is load-bearing on the emitted closure object and claim flag; the dishonest claim is
caught by `--verify` even though the mutant leaves the untouched `exit: 1` key nonzero.
Receipts sha256 `c91ccced563cc169ddf8b900b88eed57612fd112e529e896533fc2dbd257c9a2` (skip-run) and
`774ef6b8c575bed7b64c9a98d63a3dbf41c502d105bc30ae5979842ef15afe70` (verify).

## Summary

| arm | mutation that must flip it | flipped? | mutant score |
|---|---|---|---|
| a3-real-manifest-count-green | A (`COUNT=29`) | yes | 3/5, exit 1 |
| a4-truncated-manifest-red | A (`COUNT=29`) | yes | 3/5, exit 1 |
| a2-unguarded-fixture-red | B (pre-probe cache scan) | yes | 4/5, exit 1 |
| a5-skip-run-no-closure | C (skip-run claims closure) | yes | 4/5, exit 1 |
| a1-guarded-fixture-green | none applied | n/a (stays green) | — |

All three mutations flipped their target arm(s); none stayed green. **A mutation that does NOT flip
its arm is a counter defect to report, not to fix** — no such defect was observed on this axis, and
no counter file was modified (the frozen `tools/round-66/*` and `tools/round-65/*` bytes were used
only as the copy source).
