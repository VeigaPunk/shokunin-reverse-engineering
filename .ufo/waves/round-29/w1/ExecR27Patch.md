# Round-27 C2 selftest repair re-verification

## Verdict

**[OBSERVATION] Holds — selftest-only revision, measurement unchanged** at the requested measured revision `97358f759a531f7ebc0354fb937d546da8d3b8bd`.

## Evidence

- **[OBSERVATION] Target SHA matches.** Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/clone rev-parse HEAD`; then `sha256sum tools/round-27/c2-xpin-check.py /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/old.py` from the clone. UTC `2026-10-22T20:22:50Z`; exit `0`. Exact output:
  ```text
  18be864a528873b2b70d8c94e31f880290249e90
  1c8259a8fe4f5823e30f067d549d19b75a5202096c5dbc5215785b785d636783  tools/round-27/c2-xpin-check.py
  d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3  /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/old.py
  ```
  The clone was pinned at the requested target commit. `old.py` is the checker extracted from `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`.

- **[OBSERVATION] Every byte outside `def selftest()` is identical to the frozen copy.** Command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/compare_nonselftest.py /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/old.py /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/new.py`. UTC `2026-10-22T20:22:16Z`; exit `0`. Exact output:
  ```text
  base_selftest_lines=298-335 total_lines=407
  tip_selftest_lines=298-345 total_lines=417
  prefix_equal=true sha256_base=8f92f7b68f7d1af3746279ff3fc387b5cd5559cb2069a89126593fd003043eff sha256_tip=8f92f7b68f7d1af3746279ff3fc387b5cd5559cb2069a89126593fd003043eff
  suffix_equal=true sha256_base=abd96aa8ef4200dd344a6aa918447a574d564c5cc659ae7b8c4fd900bc286de9 sha256_tip=abd96aa8ef4200dd344a6aa918447a574d564c5cc659ae7b8c4fd900bc286de9
  outside_selftest_identical=true
  ```
  The helper AST-locates the top-level `selftest()` and byte-compares both the prefix and suffix.

- **[OBSERVATION] The repair selftest passes.** Command: `python3 -I -B tools/round-27/c2-xpin-check.py --selftest` in the clone at `18be864a528873b2b70d8c94e31f880290249e90`. UTC `2026-10-22T20:22:16Z`; exit `0`. Exact summary and representative anchor output:
  ```text
  PASS correct-stub at 97358f75: exit 1, expects 'r26_rows_ok=24/24 red_ok=3/3' | r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=0 rev=97358f759a531f7ebc0354fb937d546da8d3b8bd
  PASS correct-stub at cd32264f: exit 1, expects 'r26_rows_ok=24/24 red_ok=3/3' | r26_rows_ok=24/24 red_ok=3/3 capability_row=0 source_row=0 rev=cd32264f7ee356a9c0f48bd8e3fcdac222db22a0
  selftest cases=6 failures=0
  exit=0
  ```

- **[OBSERVATION] Measurement pin came from the committed round-27 after receipt.** Command: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/clone show 18be864a528873b2b70d8c94e31f880290249e90:.ufo/waves/round-27/after/c2-at-97358f75.txt`. UTC `2026-10-22T20:22:50Z`; exit `0`. Receipt excerpt:
  ```text
  r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=97358f759a531f7ebc0354fb937d546da8d3b8bd
  exit=0
  ```

- **[OBSERVATION] New checker measurement.** Command: `python3 -I -B tools/round-27/c2-xpin-check.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/clone --rev 97358f759a531f7ebc0354fb937d546da8d3b8bd` in the clone. UTC `2026-10-22T20:22:16Z`; exit `0`. Exact output:
  ```text
  checker attribution of the round-26 envelopes: 6.5.0=21 6.7.0=0 both=3 none=0
  r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=97358f759a531f7ebc0354fb937d546da8d3b8bd
  exit=0
  ```

- **[OBSERVATION] Frozen checker measurement.** Command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/old.py --root /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/clone --rev 97358f759a531f7ebc0354fb937d546da8d3b8bd` in the same clone. UTC `2026-10-22T20:22:16Z`; exit `0`. Exact output:
  ```text
  checker attribution of the round-26 envelopes: 6.5.0=21 6.7.0=0 both=3 none=0
  r26_rows_ok=24/24 red_ok=3/3 capability_row=1 source_row=1 (S081) rev=97358f759a531f7ebc0354fb937d546da8d3b8bd
  exit=0
  ```

- **[OBSERVATION] The two measurement stdout outputs are identical.** Command: `python3 -I -B /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/compare_measurements.py /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/measurement-old.txt /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/measurement-new.txt`. UTC `2026-10-22T20:23:07Z`; exit `0`; exact comparison result: `measurement_outputs_identical=true`.

## Risks, blockers, and changes

- **[INFERENCE] Scope limitation:** the verdict covers the requested selftest and the single C2 measurement revision named by the after receipt; it does not establish behavior at other revisions.
- **[OBSERVATION] Blockers:** none for the assigned checks. No tools were installed or updated.
- **Files changed in the lane:** this report only; no lane source files were modified.

## Scratch evidence artifacts and SHA-256

All generated scripts and raw outputs are under `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecR27Patch/`.

| Artifact | SHA-256 |
|---|---|
| `old.py` (frozen checker copy) | `d8de667ff82a46d5c0c9a19d4fc2f5a3c36c12fa037f9a32287046a377209bd3` |
| `new.py` (target-commit checker copy) | `1c8259a8fe4f5823e30f067d549d19b75a5202096c5dbc5215785b785d636783` |
| `compare_nonselftest.py` | `f82733fee5aa067a389e61e43ec73051b7931c59855e147739c41fdc552c4b1d` |
| `nonselftest-comparison.txt` | `f77b4ea1be8ff8dab45cca8a6aca6cbd0654d80034adf6dd6082a97f5ec8eacf` |
| `selftest.txt` | `4d83e4a23c7fd7e45704148603dd108256a8f634577dd41f5adc86994bdb6cf7` |
| `measurement-old.txt` | `42824b2da14fdbeddd83ad339f8be5e3fa6b236c88403239ba3716449d159f61` |
| `measurement-new.txt` | `d3aa3a45c967776495bae6d009eed0a033cb3363e209f9632faeb8bc7efa2ff9` |
| `compare_measurements.py` | `a49f6b08b07b0dbec8de9c17c7a914381aea5d0d8c22e89cb2c336e78a3f0dd8` |
| `measurement-comparison.txt` | `382fca7b9053008270d3f3ea4e4a9330d1dce2cc00c4e313a1557eb18eb93038` |
| `pin-evidence.txt` | `76ba1879d06b5a5b3e32da2736dfd49e87d3ed25f164e5bbf592b524423b2f21` |
| `receipt-source.txt` | `9b2fa4c107dddb14e012335f298f638fbf47f2385ad643614d8c2376e633a32e` |
