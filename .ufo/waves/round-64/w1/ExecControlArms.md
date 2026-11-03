# ExecControlArms — R64-C1 control arms (scoped result)

Seat: ExecControlArms (leaf, w1). Ran the four control arms only. **No 18-cell matrix run, no real d8 execution**
(real d8 trees were hashed, never invoked). Instrument not edited.

Instrument under test: `tools/round-64/jsc-route-matrix.py`
sha256 `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb` — equals the frozen pin.

## Results

| arm | exit | observed | verdict |
|---|---|---|---|
| A selftest | 0 | `SELFTEST CLEAN cases=22 failures=0` | as predicted |
| B do-nothing | 1 | `runs_matching 0, runs_total 18, verified false, mismatches 18, receipts 0`; byte-identical to `l1/c1-before-donothing.json` (`cmp` exit 0, both sha256 `c60dbadc291569c7271d7c22b74113573a165234e2c5855e4699dd690f1ff16d`) | as predicted |
| C flipped probe (byte 100 `0x08`→`0xF7`, sha256 `6ae4f65c0185fce522cac08cbc2cc166e649cbbce38d14f8418c49bb30c41e70`) | 2 | stderr `pin mismatch probe: .../flip.jsc`; stdout empty; work dir never created | as predicted |
| D fake-green d8 (sh script printing `[SharedFunctionInfo]`, exit 0; sha256 `7911777c…` vs pin `bc70d3c0…`) | 2 | stderr `pin mismatch d8 D1: .../fakeD1/d8`; stdout empty; work dir never created | as predicted |

Extra evidence for D: the label classifier alone accepts the fake (`classify_dump(0, b'[SharedFunctionInfo]\n') = dump-ok`,
label `dump-ok|view8-skipped|node-skipped`), so the sha256 pin — not the classifier — is the effective barrier.

Both refusal arms exit before `emit()`, so armC.json / armD.json do not exist by design; evidence is exit+stderr.

## Files written (all inside the seat's assigned paths)

- `.ufo/waves/round-64/w1/ExecControlArms/findings.md` (5,650 B)
- `.ufo/waves/round-64/w1/ExecControlArms/selftest.txt` (1,307 B)
- `.ufo/waves/round-64/w1/ExecControlArms/donothing.json` (3,285 B, sha256 `c60dbadc…`)
- `.ufo/waves/round-64/w1/ExecControlArms/donothing.stderr.txt` (0 B)
- `.ufo/waves/round-64/w1/ExecControlArms/armC.stderr.txt` (113 B) / `armC.stdout.txt` (0 B)
- `.ufo/waves/round-64/w1/ExecControlArms/armD.stderr.txt` (114 B) / `armD.stdout.txt` (0 B)
- this report

Scratch `/fast/scratch/hyaku/kaidoku-r64/ExecControlArms` deleted after the arms. No tool installs. No git mutation.

## Risks

- Control arms C and D produce no `--out` JSON; a reader expecting a receipt file there would wrongly read
  "missing file" as "not run". Use stderr + exit (captured above).
- Nothing found that requires an edit to the instrument or the claims file.
