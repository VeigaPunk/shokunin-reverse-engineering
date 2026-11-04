<!-- counting-command: r75 -->
```sh
python3 -I -B tools/round-75/probe-mutation.py --root . --rev 538b8b81 --tool tools/round-75/seam-probe.py --patch-set r75probe --expect-survivors 0 --expect-target-sha256 1fc1c8fc… --expect-sole b-drop-canary-field
```
<!-- /counting-command -->

Verbatim from `.ufo/reports/round-75/kaidoku.md` "Before → after measurements"
(R75-C1, after arm), line breaks joined. The abbreviated digest carries a
Unicode ellipsis, so the block is refused before execution.
