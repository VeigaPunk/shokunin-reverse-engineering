# ExecC1Repro — independent reproduction of R94-C1 at dd4524916a0332bb65f83525532da1c1b8d709de

Seat: ExecC1Repro (executor). Lane: kaidoku, round 94, attempt 1. Item: read-only, independent
non-author reproduction of the four frozen v4 runs, the agreement counter, and the v4 selftest.
No lane file was edited; all work ran in a `git clone --shared` at the declaration commit.

## Setup and pins (verified before any run)

- Clone: `git clone --shared -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin $S/clone && git -C $S/clone checkout -q dd4524916a0332bb65f83525532da1c1b8d709de`
  (`S=/fast/scratch/hyaku/kaidoku-r94/ExecC1Repro`). `git -C $S/clone rev-parse HEAD` = `dd4524916a0332bb65f83525532da1c1b8d709de`.
- sha256 (full) of the pinned files at the clone, all match `claims.json`:
  - v4 `stop-boundary-repair-battery-v4.py` `c41d54d72257ad41db7da5c42bea9e8ebc66fea88257660edc6e20c147266272` ✓
  - agreement `c1-receipt-agreement.py` `dc384a4464c2cb045dea491d56855685e8058dc5567a6c3b6d6dc899875836c9` ✓
  - v3 `round-93/stop-boundary-repair-battery-v3.py` `60026511e54cdc1df71233c491392fafcc89705808fa5c187d96a85862cbd4e3` ✓
  - round-92 `stop-boundary-repair-battery.py` `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc` ✓
  - round-92 `stop-boundary-battery-v2.py` `f6ddb48b4d9cbd460002db68d834f909955e2c7d4e60d7ad85325ef4e66f1874` ✓
- Repair tool `tools/round-92/upx-stop-boundary-search-repair.py` `ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1` (unchanged from round 92 per the claim).
- Controls (no pin in claims.json; hashes recorded for the record):
  - `table5-window.py` `3271c1ca07cdd43b144781740e6615d8886f6537606e137e9b8aac7c2e83c65b`
  - `carrierread5.py` `cc6a07c74a7fbca7cb9d8947ff2f6adce65e0a42bcabc4ea8fbb31204e836e23`
  - `identity_noop.py` `518422b560156da6d16396e69439cfa5012b393d896408939c042dca3b719337`
- **upx binary observed:** `/usr/bin/upx`, sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`.
  Prefix `cf2f6e7c6846a7c9` matches the pin. ✓
- Python: `python3 -V` = 3.14.8.

## Runs (exact command shape; `python3 -I -B`, `TMPDIR=$S/tmp`, `--work $S/work`)

Each run: `python3 -I -B tools/round-94/stop-boundary-repair-battery-v4.py --root . --repair-cmd <cmd> --work $S/work --rev dd4524916a0332bb65f83525532da1c1b8d709de --expect 'repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2' --json-out <seat>/r94-repro-<name>.json > <seat>/r94-repro-<name>.stdout 2> <seat>/r94-repro-<name>.stderr; echo $? > <seat>/r94-repro-<name>.rc`

The four runs were run sequentially, not in parallel: `--work` holds fixed-path state (`fresh-src.bin`), so parallel runs sharing one work dir would race. Driver: `$S/run-four.sh` (scratch, not a deliverable).

| run | repair cmd | rc | stdout line (verbatim) | predicted |
|---|---|---|---|---|
| pos | `tools/round-92/upx-stop-boundary-search-repair.py` | 0 | `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0` | met True exit 0 ✓ |
| F1 | `.ufo/waves/round-93/controls/table5-window.py` | 1 | `repaired 10 of 12; wrong 0; unsafe 0; intact 5 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2 met False exit 1` | met False exit 1 ✓ |
| F2 | `.ufo/waves/round-93/controls/carrierread5.py` | 1 | `repaired 10 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2 met False exit 1` | met False exit 1 ✓ |
| F3 | `.ufo/waves/round-93/controls/identity_noop.py` | 1 | `repaired 0 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 0 of 12; fresh-roundtrip 0 of 2 met False exit 1` | met False exit 1 ✓ |

All four stderr files are 0 bytes. All four `.json` receipts parse as JSON (dict). Each stdout is one line.

Receipt paths (seat dir): `r94-repro-{pos,F1,F2,F3}.{json,stdout,stderr,rc}`.

Honest-case encoding check: `r94-repro-pos.json` carries `"output": {"bytes": 34436, "sha256": "81f74a27fb70c62d4bd8fb454d59dc7dbf3714c47c0fc6fe3de59174d7e6bcfc"}` (the bytes-as-length-and-sha256 writer path ran on the honest case, where v3 raised TypeError). No `*.tmp` leftover in the seat dir.

Stdout-vs-receipt label equality: for each of the four runs, the stdout line equals
`receipt.label + " met " + receipt.met_target + " exit " + receipt.exit` exactly (checked in Python, `EQUAL`, one stdout line each).

## Agreement counter

Command: `python3 tools/round-94/c1-receipt-agreement.py --dir <seat> --prefix r94-repro` (driver `$S/run-agreement.sh`), rc **0**.

Output `counts_of_4`: `{"valid": 4, "agree": 4, "predicted": 4}`, `"met": true`. Per-row `valid`, `agree`, `predicted` all true for pos, F1, F2, F3.
Saved stdout: `r94-repro-agreement.stdout` (rc in `r94-repro-agreement.rc`).

Frozen target (`counts_of_4` valid 4, agree 4, predicted 4; met true; exit 0): **met**.

## v4 selftest

Command: `python3 -I -B tools/round-94/stop-boundary-repair-battery-v4.py --selftest --work $S/work-selftest` (driver `$S/run-selftest.sh`), rc **0**.

```
selftest bytes-encoded: ok
selftest bytes-receipt-reparses: ok
selftest unknown-type-raises: ok
SELFTEST cases=3 failures=0
```
Saved in `r94-repro-selftest.stdout`, rc in `r94-repro-selftest.rc`.

As the claim states, the selftest only exercises writer helpers. It is not counted as evidence for C1; the four public-CLI runs above are.

## Verdict on the item

- Four exit codes: pos 0, F1 1, F2 1, F3 1. Match predictions.
- Agreement counts: valid 4, agree 4, predicted 4; exit 0. Match the frozen target.
- Stdout lines equal the receipts' labels (and met/exit): yes, all four.
- upx sha256 prefix observed: `cf2f6e7c6846a7c9` (matches pin).
- Kill-rule checks I could observe: positive met True (no kill); no forgery met True (no kill); all receipts valid JSON (no kill); no stdout/receipt disagreement (no kill); all pinned sha256 match (no kill); upx prefix matches (no kill).

Independent reproduction: **C1 reproduces at dd45249** (R94-C1 measured target met in this non-author run).

## Not done / limits

- I did not run R94-C2 (not assigned to this seat).
- Controls F1–F3 have no pins in `claims.json`; their hashes are recorded above but not checked against any frozen value.
- Only one host (this workstation), one run of each command. No repeat-run variance measured.

## Tooling

No tools installed, upgraded or removed. No pacman, no `~/.local/bin` writes, no host state changes. `/usr/bin/upx` was read-only inspected (sha256 only), not invoked directly by me; it was invoked only through the frozen counter.

## Files written

- `.ufo/waves/round-94/w1/ExecC1Repro/ExecC1Repro.md` (this report; also written at the Report trailer path)
- `.ufo/waves/round-94/w1/ExecC1Repro/r94-repro-{pos,F1,F2,F3}.{json,stdout,stderr,rc}`
- `.ufo/waves/round-94/w1/ExecC1Repro/r94-repro-agreement.{stdout,stderr,rc}`
- `.ufo/waves/round-94/w1/ExecC1Repro/r94-repro-selftest.{stdout,stderr,rc}`

Scratch `/fast/scratch/hyaku/kaidoku-r94/ExecC1Repro` (clone, work dirs, driver scripts) is removed before yield.
