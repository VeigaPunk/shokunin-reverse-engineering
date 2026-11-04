# SentinelR87 (round 87, sentinel): hostile-input review of upx-magic-repair.py

Full findings, repro commands and timings: `.ufo/waves/round-87/w1/SentinelR87/findings.md`.

1. **MEDIUM**: a decoy sentinel steers the resume scan (first match wins). A 25-byte decoy in the loader stub makes
   the repair exit rc 0 while it writes the wrong window. The real end-of-chain magic stays tampered, and `upx -t`
   fails (jq, dinit). On an intact packed file with a decoy, the tool mutates 4 loader bytes, which breaks N3-style
   idempotence. This does not affect the frozen magic-only population or its 8/8 score. It bounds the promotion to
   "magic-only tamper". Fix: keep the candidate whose sentinel is nearest the PackHeader, or refuse when candidates
   are ambiguous.
2. **LOW-MEDIUM**: CPU DoS from a quadratic resume scan. An 832 KB crafted input runs longer than the counter's
   300 s repair timeout, while RSS stays flat at about 16 MB. Fix: memoize walk ends per offset, or bound the
   resume window.
3. **LOW**: `/dev/zero` and FIFO inputs give an unbounded read or block forever. I/O errors exit rc 1 with a
   traceback instead of the documented rc 2.
4. **LOW/INFO**: `--out` follows symlinks and writes non-atomically. A refusal writes nothing (verified).
5. **INFO/calibration**: jq and xxd carry a fourth `UPX!` in the stub that the tool does not restore, so the
   repaired bytes differ from the packed bytes in 4 of 8 cases. `upx -t` and `-d` still pass, so the frozen arms
   are unaffected.
6. **INFO**: verified safe. The tool makes no execve besides python itself and opens only `--out` for writing.
   Under `-I`, nothing is imported from the cwd, the script dir or PYTHONPATH. Without `-I`, stdlib shadows in the
   script dir are imported.
