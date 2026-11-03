# ExecControlArms — R64-C1 four control arms

Seat: ExecControlArms (leaf). No 18-cell matrix run performed here (that is ExecMatrixRun's job).
Instrument: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-64/jsc-route-matrix.py
sha256 29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb — equal to the frozen pin (verified before any arm).
Real d8 binaries were hashed only; no real d8 was executed by this seat.
Scratch: /fast/scratch/hyaku/kaidoku-r64/ExecControlArms (deleted on exit). Report dir: .ufo/waves/round-64/w1/ExecControlArms/.
disk-guard before the pass: /fast/scratch/hyaku 50% used, 404.5G free.

Counting-command arguments used for arms C and D (identical to the counting command except the arm-specified override):

    --typora /home/vgpnk/.local/share/kaidoku-jsc/inputs/atom.compiled.dist.jsc \
    --d8-neighbour /home/vgpnk/.local/share/kaidoku-jsc/d8-14.8.178.1 \
    --d8-cross /home/vgpnk/.local/share/kaidoku-jsc/d8-14.7.173 \
    --view8-dir /home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src/View8 \
    --python /home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python --node node

Input pins re-checked by hand before the arms: probe a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710,
typora 6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9 — both equal to PINS.

| arm | command (essential) | exit | observed key line | verdict |
|---|---|---|---|---|
| A selftest | `python3 .../jsc-route-matrix.py --selftest` | **0** | `SELFTEST CLEAN cases=22 failures=0` (22 PASS lines, none FAIL) | as predicted |
| B do-nothing | `python3 .../jsc-route-matrix.py --skip-run --out .../w1/ExecControlArms/donothing.json` | **1** | JSON: `skip_run true, exit 1, runs_matching 0, runs_total 18, verified false, mismatches 18, receipts 0` | as predicted |
| C flipped probe | counting args, `--probe <scratch>/flip.jsc --work <scratch>/work-c --out .../armC.json` | **2** | stderr: `tools/round-64/jsc-route-matrix.py: pin mismatch probe: /fast/scratch/hyaku/kaidoku-r64/ExecControlArms/flip.jsc`; stdout empty | as predicted |
| D fake-green d8 | counting args, `--d8-match <scratch>/fakeD1 --work <scratch>/work-d --out .../armD.json` | **2** | stderr: `tools/round-64/jsc-route-matrix.py: pin mismatch d8 D1: /fast/scratch/hyaku/kaidoku-r64/ExecControlArms/fakeD1/d8`; stdout empty | as predicted |

## Arm A — selftest

- 22 cases, all PASS: dump-ok / dump-empty-rc0 / dump-sigabrt (134) / dump-sigsegv (139) / dump-exit-1 /
  dump-timeout / view8-ok / view8-empty / view8-exit-1 / node-pass / node-fail / compose-full /
  compose-skipped / verdict-all-match / verdict-do-nothing-exit / verdict-do-nothing-count /
  verdict-one-mismatch-exit / verdict-one-mismatch-count / verdict-fake-green-count /
  pin-probe-mismatch / pin-probe-missing / pin-typora-missing-after-probe.
- Exit 0, no writes (in-memory fixtures only). Receipt: selftest.txt.

## Arm B — do-nothing control

- Exit 1 (claim-not-verified class), every cell recorded `not-run`; sample mismatch:
  `{"cell": ["probe","D1"], "rep": 1, "observed": "not-run", "predicted": "dump-ok|view8-ok|node-fail"}`.
- `cmp .../w1/ExecControlArms/donothing.json .../l1/c1-before-donothing.json` → **exit 0 (byte-identical)**;
  both files sha256 `c60dbadc291569c7271d7c22b74113573a165234e2c5855e4699dd690f1ff16d`.
  The L1 pre-freeze do-nothing receipt therefore reproduces exactly from the post-freeze instrument.
- stderr empty (0 bytes). Receipt: donothing.json, donothing.stderr.txt.

## Arm C — pin refusal on a one-byte-flipped probe

- flip: byte 100 `0x08` → `0xF7` (xor 0xFF); flipped file sha256
  `6ae4f65c0185fce522cac08cbc2cc166e649cbbce38d14f8418c49bb30c41e70` (probe pin a86f6ea0… unchanged).
- Refused before any run: `check_pins` precedes `work_root.mkdir` (instrument lines 178–184), so
  **work-c does not exist** (`ls: cannot access 'work-c': No such file or directory`) — stronger than
  "empty dir": no cell directory, no dump, no d8 process.
- `armC.json` **absent**: `emit()` is never reached on the pin-refusal path, so the arm leaves no JSON receipt.
  Evidence for this arm is exit 2 + the stderr line (captured in armC.stderr.txt). Receipts: armC.stderr.txt (113 B), armC.stdout.txt (0 B).

## Arm D — fake-green d8 refused by the binary pin

- fake d8: `/bin/sh` script, 45 bytes, mode 0755, body prints `[SharedFunctionInfo]` and `exit 0`;
  `snapshot_blob.bin` and `icudtl.dat` copied from the real D1 build (they were never reached: the d8
  binary check runs first, instrument lines 150–157).
- fake d8 sha256 `7911777c299c89134baf701dc9a080c4c169713ba6ab1390d2337546d8feb1ea` ≠ D1 pin
  `bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331` → exit 2, `pin mismatch d8 D1`.
- Fake-green demonstration (classifier on a scratch copy of the instrument, no real d8):
  `classify_dump(0, b'[SharedFunctionInfo]\n') = dump-ok`; composed label `dump-ok|view8-skipped|node-skipped`.
  So the sha256 pin, not the label classifier, is what refuses a fake-green route — the control exercises
  the defence that matters.
- `work-d` absent; `armD.json` absent (same pre-emit refusal path). Receipts: armD.stderr.txt (114 B), armD.stdout.txt (0 B).

## Notes / risks

- Both refusal arms (C, D) exit 2 with an empty stdout and no `--out` file; a reviewer must read stderr+exit,
  not the JSON, to see these controls. Not a defect for R64-C1 (the predicate concerns the full 18-cell run),
  but worth stating so no one reads "no JSON" as "arm not run".
- The instrument was never edited; the frozen PREDICTED/PINS tables were read only. No tool installs were needed.
