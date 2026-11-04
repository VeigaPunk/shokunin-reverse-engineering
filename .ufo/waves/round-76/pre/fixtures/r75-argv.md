<!-- counting-command: r75 -->
```sh
python3 -I -B tools/round-75/probe-mutation.py --root . --rev 538b8b81 --tool tools/round-75/seam-probe.py --patch-set r75probe --expect-survivors 0 --expect-target-sha256 1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d --expect-sole b-drop-canary-field
```
<!-- /counting-command -->

The same printed command with the digest bound and nothing else changed: it
still carries no `--work`, so the instrument refuses it at its own preflight
(`{"unevaluable": "missing required arguments: work"}`, exit 2).
