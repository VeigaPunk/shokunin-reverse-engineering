# ExecControls — round-75 w1: independent control re-derivation (seat report)

Seat: ExecControls. Date: 2026-11-04. Lane repo: kaidoku-shokunin.
Revisions: base `3c15a156`, freeze `ec149dc`, lane HEAD at report time `e1944b65`.
All runs from the lane root with `python3 -I -B`, own scratch as `--work`
(`/fast/scratch/hyaku/kaidoku-r75/ExecControls`, deleted after the run).

## Frozen run (the assigned command)

```
python3 -I -B tools/round-75/controls.py --root . --base-rev 3c15a156 \
  --work <scratch>/work --json-out <scratch>/controls-frozen.json
```

Exit **0**, `ok: true`, all four arms met — receipt at
`.ufo/waves/round-75/w1/ExecControls/receipt.json` (verbatim copy of the run's
`--json-out`).

A second run executed the **frozen bytes only**: the five instruments extracted
from the freeze blobs (`git cat-file blob ec149dc:tools/round-75/...`, sha256s
re-verified against `claims.json.instruments`), invoked with
`--after-rev ec149dc` so every executed detector/audit byte is a frozen blob.
Exit **0** (`frzexit.txt`), observations identical to the receipt below.

## Independent re-derivation, arm by arm (from each arm's own observed block)

- **c1_base_world** — `survivors` is exactly, and only, the four claimed
  base-world survivors `d-home-under-truthy, d-tmpdir-under-truthy,
  d-name-samples-last-wins, d-lie-clean-superset`; `pristine_cases` 20 (full
  base selftest); `canary_failed` is exactly two cases,
  `a12-kernel-multiple-samples` and `a12-kernel-canary-field`, with
  `canary_sole: false` — the canary is cross-bound, not sole, in the base
  world. Matches R75-C1's before-world.
- **c1_no_declared_cases** — `killed: []` (no mutant killed under renamed case
  names); `wrong_case` is exactly the seven-name closed set
  (`b-first-sample-only, b-drop-canary-field, d-home-under-truthy,
  d-tmpdir-under-truthy, d-name-samples-last-wins, d-name-samples-first-wins,
  d-lie-clean-superset`) — satisfies both the frozen `>= 6` binding and the
  post-`0465f251` exact-set binding; `pristine_rc: 0` and
  `renamed_pristine_ok: true`, so the reds come from the case-name binding,
  not broken code. The case names, not merely a red selftest, are what binds.
- **c2_do_nothing** — `mismatch_count` 8 equals the eight frozen atoms;
  `mismatches` is exactly `D16…D23` in frozen order; `rc: 1`, empty stderr. A
  do-nothing round cannot reach zero.
- **c2_red_fixtures** — all nine grammar cases true (`d9` ×3, `d10` ×2,
  `d11` ×2, `d12` ×2): every strengthened grammar rejects its red fixture and
  accepts its good fixture in-process.

## Negative control (my own; the shown-able-to-fail proof)

One assertion changed in a scratch copy of `controls.py` (expect 3 survivors):

```
-    base_ok = (base_scored["pristine_ok"] and survivors == sorted(BASE_SURVIVORS)
+    base_ok = (base_scored["pristine_ok"] and survivors == sorted(BASE_SURVIVORS[:3])
```

Re-run (same base rev, own work dir): **exit 1** (`negexit.txt`,
`NEG_EXIT=1`), `ok: false`, arm `c1_base_world` red — the only red arm — with
the observed four survivors preserved in its observation block; the other
three arms stay green. Receipt: `neg-receipt.json`. Reproduced twice with
identical observations. The control can fail, and names the changed arm.

## Consistency vs the frozen instruments' own output

My four arms match `.ufo/waves/round-75/pre/controls-at-declaration.json` and
`.ufo/waves/round-75/l1/scores/controls-at-landing.json` on **every observed
value** (the only diffs are per-run `renamed_path` work paths and the landing
receipt's `after_rev`). **No arm observation is inconsistent** with the frozen
instruments' own output. That is three-plus independent executions (frozen
declaration receipt, L1 landing receipt, my two runs, frozen-blob rerun)
agreeing on every survivor, case, count and grammar boolean.

## Integrity observations (no action taken; disclosure only)

- Current on-disk `tools/round-75/{controls,probe-mutation,record-audit}.py`
  hash `22bb4be9…, d7757ae2…, b81d037d…`, which differs from the
  declaration/freeze blobs (`f9db96a2…, ec089411…, bba8b8cd…`) that do match
  `claims.json.instruments`. `freeze-pins.py` and `seam-probe.py` are
  unchanged at `f80ad407…` and `1fc1c8fc…`.
- The delta is a disclosed post-freeze supersession chain, not silent drift:
  `ad53c1e1` (probe-mutation runner binding) + `13d1498f` (disclosure),
  `0465f251` (controls exact-set binding) + `13d1498f`, `4e93c1a5` and
  `7edb005e` (record-audit D21/D20 extensions) + `9817d41a`/`142e78c4`
  (disclosures), each paired with re-taken receipts. Both instrument
  generations produce identical arm observations on this seat's runs.
- `git ls-files -v` shows plain `H` on all five instruments (no
  skip-worktree/assume-unchanged masks); `git status` clean at `e1944b65`.

## Files written by this seat

- `.ufo/waves/round-75/w1/ExecControls/receipt.json` — frozen-run receipt (exit 0)
- `.ufo/waves/round-75/w1/ExecControls/neg-receipt.json` — negative control (exit 1)
- `.ufo/waves/round-75/w1/ExecControls/frzexit.txt`, `negexit.txt` — measured exit codes
- `.ufo/waves/round-75/w1/ExecControls/post-freeze-log.txt` — commit→file map since the freeze
- `.ufo/waves/round-75/w1/ExecControls.md` — this report

No lane file outside `w1/ExecControls/` was written. Scratch dir removed.
