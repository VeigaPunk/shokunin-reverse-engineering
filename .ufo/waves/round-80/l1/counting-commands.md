# Round-80 counting commands — the block text printed in the report, copied verbatim
Each block below is byte-identical to the corresponding block in
`.ufo/reports/round-80/kaidoku.md`; `tools/round-76/plan-command.py` reads this committed copy
because it reads a plan from the lane at `--rev`, not a fleet file.

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-80/strictness-battery.py --root $ROOT --impl tools/round-80/pointer-bind.py --control-impl tools/round-79/pointer-bind.py --work $WORK --json-out $OUT
```
<!-- /counting-command -->

<!-- counting-command: C2 -->
```sh
python3 -I -B tools/round-80/receipt-provenance.py --root $ROOT --rev $REV --from-round 60 --to-round 79 --json-out $OUT
```
<!-- /counting-command -->

<!-- counting-command: C3 -->
```sh
python3 -I -B tools/round-80/guard-battery.py --root $ROOT --rev $REV --expect-sha256 df6fb85670549ff1a03f925a3bed456cc3b64a311ae8681754c8efcc567149d6 --work $WORK --json-out $OUT
```
<!-- /counting-command -->

