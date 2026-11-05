# SentinelWrite — scoped findings (round 95, R95-C1 receipt write path)

Full evidence: `.ufo/waves/round-95/w1/SentinelWrite/security.md`. Frozen commit `4bda1d1d`. Lane not patched.

- **(a) symlinked receipt parent dir — NONE (residual).** The temp file and receipt land in the directory the operator named, via its symlink target. Parent-dir swap is out of stated scope. `exp_symlink.py` case A, exit 0.
- **(b) pre-created symlink at receipt path — NONE.** `os.replace` replaces the link; victim unchanged. Probe leg `victim_intact true`. `exp_symlink.py` cases B and B2, exit 0.
- **(c) mkstemp name and O_EXCL — NONE.** Strace shows `O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0600. A forced name collision with a planted symlink raises `FileExistsError` and leaves the victim intact. `exp_symlink.py` case C-excl, exit 0.
- **(d) writes outside `--work` / `--json-out` on the honest v5 run — NONE.** Run rc 0, `selfverify ok=True reasons=0`, met True. 0 write-flag opens or renames outside `work/`, `out/`, `tmp/` (excluding `/dev/null`). `strace -f -qq -e trace=openat,rename,renameat,renameat2,unlink,unlinkat`.
- **(e) secrets in receipts — NONE.** `grep -ci` for `PATH=`, `HOME=`, token, key, secret, password, session, cookie: 0 each. Positive control `grep -c sha256` = 22. Premise mismatch: at `4bda1d1d` the `l1/scores/*.json` receipts are untracked in the lane, not committed; only the two s320 HTML fetches are committed.
- **(f) probe write scope — LOW.** The probe's victim, `.tmp` symlink and writer legs stay under `--work` (0 writes outside). Its own `--json-out` uses `open(..., "w")` and follows a planted symlink (victim overwritten, exit 0). Remediation: route the probe's receipt through the same mkstemp + `os.replace` writer.
- **Additional — LOW [INFERENCE].** `verify_receipt` re-opens the path after the replace instead of reading the written fd, so self-verification is not a boundary against a writer with access to the output dir.

No HIGH or MED findings.

Named files written: `.ufo/waves/round-95/w1/SentinelWrite/security.md`, `.ufo/waves/round-95/w1/SentinelWrite/exp_symlink.py`, `.ufo/waves/round-95/w1/SentinelWrite/exp-symlink-output.txt`, `.ufo/waves/round-95/w1/SentinelWrite/honest.stdout`, `.ufo/waves/round-95/w1/SentinelWrite/honest.stderr`, `.ufo/waves/round-95/w1/SentinelWrite/honest.rc`, `.ufo/waves/round-95/w1/SentinelWrite/honest-receipt.json`, `.ufo/waves/round-95/w1/SentinelWrite/strace-honest.txt`, `.ufo/waves/round-95/w1/SentinelWrite/probe.stdout`, `.ufo/waves/round-95/w1/SentinelWrite/probe.stderr`, `.ufo/waves/round-95/w1/SentinelWrite/c1-symlink-v5.json`, `.ufo/waves/round-95/w1/SentinelWrite/strace-probe.txt`, `.ufo/waves/round-95/w1/SentinelWrite/probe-jsonout-symlink-victim-after.txt`, and this report `.ufo/waves/round-95/w1/SentinelWrite.md`. Scratch removed. No tooling installed (strace already at `/usr/bin/strace`).
