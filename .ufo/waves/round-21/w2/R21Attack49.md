# R21Attack49 — t1246-test2json retrospective C2 compatibility

**Axes:** C1 / calibration; C2 / depth. **Scope:** only retained R20 label `t1246-test2json`; retrospective compatibility, not a fresh forecast.

## Artifact identity

The binding `.ufo/waves/round-20/runs/t1246-test2json/comparison-log-binding.json` names `.ufo/waves/round-20/runs/t1246-test2json/logs/rea-ghidra-tU5R8R/ghidra.log`, records SHA-256 `6a4de93b3e571d45276eafb028be099f045f8da6731b5adec0be4bcfc2933481`, and has `verified: true`. The hash command returned the same digest.

The frozen prediction `.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-test2json.json` has `first_failure.h0: null` and `first_failure.h1: null`.

## Verification record

Hash invocation (the submitted bash command also printed the command status and listed the bound log directory):

```text
hash argv: sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-test2json/logs/rea-ghidra-tU5R8R/ghidra.log
hash stdout: 6a4de93b3e571d45276eafb028be099f045f8da6731b5adec0be4bcfc2933481  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-test2json/logs/rea-ghidra-tU5R8R/ghidra.log
hash stderr: (no stderr text observed)
hash exit: 0 (the wrapper printed EXIT=0 immediately after sha256sum)
```

The actual bash command also emitted `total 28`, directory entries `.` (40 bytes), `..` (34 bytes), `ghidra.log` (22,788 bytes), and `script.log` (105 bytes) from its trailing `ls -la` read-only listing.

Assigned comparator, using the original R20 extractor:

```text
Python argv: python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py --prediction /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/t1246-test2json.json --log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/t1246-test2json/logs/rea-ghidra-tU5R8R/ghidra.log --extractor /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py
Bash wrapper: python3 -I -B [the argv above]; status=$?; printf 'EXIT=%s\\n' "$status"; exit 0
stdout: {"finding": "failure_match", "last_line": 191, "match": true, "observed": null, "predicted": null}
EXIT=0
stderr: (no stderr text observed)
Python comparator exit: 0
```

## Result and limits

For this exact bound log/prediction pair, the comparator returns `failure_match`: both predicted and observed first failures are null, and the null observation is bounded through log line 191. This confirms one retrospective match only. The log contains `GoTypeManager` subtype warnings at lines 138–140; they are not qualifying first-failure records for the R20 extractor. The comparison does not verify overall analyzer correctness or success: it compares the first-failure observation, ignores the extractor's separate `other_errors` inventory, and unrelated analyzer errors or warnings do not establish success. The log's line 185 `Analysis succeeded` status is likewise outside the comparison predicate.

**Actionable findings:** none for this exact artifact pair. **Residual risk / verification gaps:** this does not exercise malformed or missing observations, asymmetric nulls, distinct failure kinds/indices, or the remaining retained R20 labels; it cannot substantiate C2's broader compatibility claim by itself.

No production files were edited. No REA tool or native carrier was run; no installs, builds, formatters, broad test suites, or outside verifier were run. The hash shell invocation included an additional read-only directory listing (recorded above).