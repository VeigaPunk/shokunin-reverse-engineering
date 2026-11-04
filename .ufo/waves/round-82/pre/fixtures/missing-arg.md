Fixture: a runnable argv whose trailing --json-out has no value; argparse
exits 2 and the block is scored EXECUTION_FAILED.

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-82/conjunction-gate.py --battery --root . --rev $REV --json-out
```
<!-- /counting-command -->
