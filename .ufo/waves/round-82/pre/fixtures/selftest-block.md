Fixture: a runnable block that invokes this instrument's own --selftest.
Proves the instrument itself executes as a pinned script without
self-recursion (the battery never executes its own --battery block).

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-82/printed-command.py --selftest --root . --json-out $OUT
```
<!-- /counting-command -->
