# ExecBattery (seat ExecBattery-2) — round-75 wave-1 findings

Scope: run the frozen mutation battery twice at the declaration revision from the lane
root with my own `--work`, validate and self-test, independently re-derive the JSON,
and prove the pin-before-execution clause. Target: `tools/round-75/probe-mutation.py`
and `.ufo/waves/round-75/w1/ExecBattery/`.

## Method

- Runner provenance: the working-tree runner at lane tip differs from the declaration
  revision's runner (tip commit `ad53c1e1` changed the runner binding). Per the
  assignment, both arms ran the **frozen declaration runner**:
  `git show 8dff07b9ac7dfc3f099c97d98ee97cc5f69efb3a:tools/round-75/probe-mutation.py`
  extracted to scratch, sha256 `ec089411b0a3a0feb2cede59af5156a2a53675fe121eeeb1191d0e4410f84204`
  (= `git show 8dff07b9:tools/round-75/probe-mutation.py | sha256sum`), executed with
  `python3 -I -B` (Python 3.14.8) from the lane root, one `--work` + `TMPDIR` dir per arm
  under `/fast/scratch/hyaku/kaidoku-r75/ExecBattery-2` (deleted after the run).
- Lane HEAD at run time: `6864a78039fadf3743304c8eb9ca38be5b2238b1`.

## Results (acceptance, item by item)

- **A** (`--rev 8dff07b9… --tool tools/round-75/seam-probe.py --patch-set r75probe
  --expect-survivors 0 --expect-target-sha256 1fc1c8…410d --expect-sole b-drop-canary-field`):
  exit **0**. Re-derived from `receipt-A-r75probe.json`: `ok` true; survivor_count **0**;
  15 mutants, all verdict `killed`, `killed_wrong_case` empty; every kill's `failed` list
  names the mutant's declared case; `b-drop-canary-field` `failed == ["a12-kernel-canary-field"]`
  and is the **sole** detector (`sole_detector` true); pristine run rc 0 with **25** cases,
  floor 25, `pristine_ok` true; `target_pin` = expect 1fc1c8…, matched true, pinned true,
  `pinned_before_exec` true; runner block `path=tools/round-75/probe-mutation.py`,
  `sha256=ec089411…` equal to `git show 8dff07b9:tools/round-75/probe-mutation.py | sha256sum`.
- **B** (`--rev 3c15a156… --tool tools/round-74/seam-probe.py --patch-set r75base
  --expect-survivors 4`): exit **0**. Re-derived from `receipt-B-r75base.json`: `ok` true;
  survivor_count **4** with names exactly `d-home-under-truthy`, `d-tmpdir-under-truthy`,
  `d-name-samples-last-wins`, `d-lie-clean-superset` (all rc 0, 20/20 cases, floor 20);
  `b-drop-canary-field` killed with `failed == ["a12-kernel-multiple-samples",
  "a12-kernel-canary-field"]` → `sole_detector` **false** (the round-74 cross-binding,
  reproducible at the base). Unpinned target records `matched: null` (no pin supplied).
- **`--validate`** on both receipts: exit **0**, `defects: []` each.
- **`--selftest`**: exit **0**, 9 cases, no failures.
- **Wrong-pin probe**: A rerun with `--expect-target-sha256 0000…0000` exited **2** with
  `{"unevaluable": "target pin mismatch before execution: expected 0000…0000, blob at
  8dff07b9…:tools/round-75/seam-probe.py is 1fc1c8…410d"}`; the fresh `--work` dir held
  **0** entries afterwards (0 `mut-text-*` dirs). No mutant executed before the pin
  comparison — SS74-2 confirmed.

## Cross-check against the frozen pre receipts

Compared all scored fields of both receipts against the committed pre receipts
(`.ufo/waves/round-75/pre/c1-post-at-declaration.json`, `c1-base-arm.json`): **identical
on every field** (patch set, rev, tool, target sha256, pristine, survivor lists, verdicts,
failed lists, sole map, multi_detected, pin, ok, mutant rows). The only difference is the
runner block: pre receipts bind `d7757ae2…` (the tip runner, post-`ad53c1e1`), my A binds
`ec089411…` (the frozen declaration runner, as the assignment's runner-sha clause
requires) and my B binds `null` — the frozen runner reads the round-75 runner at the
target revision via `git show`, which fails at the round-74 base (round-74 routed
defect 5, later fixed at the tip by binding `__file__`). This is recorded behavior of the
frozen code under test, not a defect in these results.

## Notes / observations (no action required)

- In arm A, `a-drop-lie-clean` is killed by a two-case failure
  (`a12-kernel-cases`, `a12-lie-clean-keys-exact`), so it is correctly reported as
  `sole: false` / `multi_detected`; the sole-detector acceptance applies to
  `b-drop-canary-field` only.
- Arm B targets the unpinned round-74 blob (`target_pin.pinned: false`,
  `matched: null`) — per the assignment, no target pin was passed for B.

## Files

- `.ufo/waves/round-75/w1/ExecBattery/receipt-A-r75probe.json` — battery arm A receipt (`--json-out`).
- `.ufo/waves/round-75/w1/ExecBattery/receipt-B-r75base.json` — battery arm B receipt (`--json-out`).
- `.ufo/waves/round-75/w1/ExecBattery/receipt.json` — consolidated seat receipt with re-derivations.
- No lane source files were modified. Scratch dir deleted.
