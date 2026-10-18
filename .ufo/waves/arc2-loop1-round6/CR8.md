# CR8 — provenance attack: service stdout as decisive evidence (single-writer?)

**VERDICT: SINGLE-WRITER FAIL.** Live `/var/tmp/arc2-l6r6-pe/stdout.json` is not sealed decisive evidence. The bytes on disk at 2026-10-18T17:48:42-03 are one coherent CLI document consistent with invocation `31dc1c7f0a5e4f9db082dfc9da37b90d`, but the path is a same-uid-writable regular file, the journal holds none of the payload, and the artifact does not name the invocation. C1's big leg is not HELD on these bytes (`analyzer_preset`/`evidence_id` absent). Land the honest-negative only from a close copy whose inode, size, and sha256 match the snapshot below; a mismatch means the big leg is unverified, not a new outcome. Service was not signaled. Custody pair out of scope.

Axes: exclusivity (single writer / exclusive hold), binding (bytes ↔ invocation), durability (second copy), non-interference.

## Evidence

Observed 2026-10-18T17:48:42-03 (20:48:42Z). Read-only. No `systemctl kill|stop|restart`, no write to the evidence path.

```sh
systemctl --user cat arc2-r6-pe
# StandardOutput=file:/var/tmp/arc2-l6r6-pe/stdout.json
# StandardError=file:/var/tmp/arc2-l6r6-pe/stderr.log
# ExecStart=.../npx -y rea-agents@6.5.0 analyze .../windows_release_arm64.exe
systemctl --version | head -1
# systemd 261 (261.2-1-arch)
journalctl --user -u arc2-r6-pe --no-pager -o cat | wc -c
# 411
journalctl --user -u arc2-r6-pe --no-pager -o cat | rg -c 'Analysis failed|execution_failure|Decompiler Parallel' || true
# stdout_text_absent_from_journal
journalctl --user _PID=1992927 --no-pager -o cat; journalctl --user _PID=1993398 --no-pager -o cat
# both empty
stat -c '%a %U ino=%i size=%s mtime=%y ctime=%z' /var/tmp/arc2-l6r6-pe/stdout.json
# 644 vgpnk ino=2160272 size=16692 mtime=2026-10-18 17:41:06.513410314 -0300 ctime=same
sha256sum /var/tmp/arc2-l6r6-pe/stdout.json
# 4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7
stat -c '%a %U ino=%i mtime=%y ctime=%z' /run/user/1000/systemd/transient/arc2-r6-pe.service
# 644 vgpnk ino=6756 mtime=2026-10-18 17:40:58.990392417 -0300 ctime=same
lsattr /var/tmp/arc2-l6r6-pe/stdout.json
# ---------------------- (no immutable)
python3 -c "import os; p='/var/tmp/arc2-l6r6-pe/stdout.json'; print(os.access(p, os.W_OK), os.getuid())"
# True 1000
# /proc fd scan for inode 2160272: open_fds 0
```

Resolving pointers:

- `/run/user/1000/systemd/transient/arc2-r6-pe.service:8` — `StandardOutput=file:/var/tmp/arc2-l6r6-pe/stdout.json` (not `append:`, not `truncate:`, not `journal`). `:9` stderr is a different file. `:12` one `ExecStart`. Fragment mode 0644, ctime frozen at unit create (17:40:58.990), still owner-writable.
- `systemd.exec(5)` (local man, systemd 261) lines 3349–3362: `file:path` opens a regular file **for writing at the beginning, without truncating**. `append:path` is append; `truncate:path` truncates. A later shorter write at offset 0 leaves a stale tail. This unit uses `file:`.
- Journal (`journalctl --user -u arc2-r6-pe -o verbose`): 4 messages, all `_PID=1539` (user systemd). `USER_INVOCATION_ID=31dc1c7f0a5e4f9db082dfc9da37b90d`. Start `__REALTIME_TIMESTAMP=1792356058992872` (17:40:58.992872 -03); exit `1792356066546929` (17:41:06.546929 -03), `status=1/FAILURE`. No message contains the stdout path or the payload. `_PID=1992927` and `_PID=1993398` have no journal lines.
- `/var/tmp/arc2-l6r6-pe/stdout.json:1-5` — `error: Analysis failed` / `code: execution_failure` / `retryable: false`. Not JSON (`json.loads` fails at column 1; the `.json` name is false).
- `:13` `target_sha256: 7a2ccd688f6c3d53d2d67878bc98a96bebe8463bf97acf986b9c2c9e1ba9a292`; `:17` `run_id: 478b7a2f-778a-482e-85b4-1d56460f5f45`; `:23` `process_id: 1993398` (Ghidra child, not ExecMainPID 1992927).
- Byte counts in the 16692 bytes: `31dc1c7f0a5e4f9db082dfc9da37b90d`=0, `1992927`=0, `analyzer_preset`=0, `evidence_id`=0, `\ncode:`=1, `exit_code:`=1, `error:`=2 (line 1 plus embedded `Rust error:` inside `:31`, not a second document). 0 NUL bytes. Ends with newline and `:39` `failure_message: Ghidra exited before bridge startup`.
- File birth 17:40:59.004392450 -03 (stat `%W=1792356059`), ~11ms after journal start. mtime 17:41:06.513410314 is 33.5ms before the journal exit line. stderr.log birth matches, size 0. Directory listing: `node-compile-cache`, empty `stderr.log`, `stdout.json` only — `runtime_root` `:18` `/var/tmp/arc2-l6r6-pe/rea-ghidra-f5rC3Z` is gone, so `:21` `ghidra.log` and `:22` `script.log` are not a second copy.
- `/var/tmp` is 1777 sticky; the evidence dir is 0755 `vgpnk`. Other uids cannot write or unlink the file. uid 1000 can (`W_OK` true). The wave shares that uid, and the prompt published this `TMPDIR`. No flock holder.

Labels:

- **observation** — stdout is `StandardOutput=file:` not the journal; journal has 4 lifecycle lines and zero payload; file mode 0644, no immutable bit, open fds 0, inode 2160272, sha256 `4a3ebb82…`, invocation id and ExecMainPID absent from the bytes; unit fragment equally 0644 and unsealed; `file:path` does not truncate.
- **inference** — current bytes are one CLI document (Ghidra stdout is a quoted field at `:30-31`, not a raw second writer on fd 1), flushed at this invocation's exit. Correlation to the unit is circumstantial (path in the mutable fragment + timestamp overlap + target/argv match), not a seal. A same-uid rewrite or a reopen at offset 0 can change the decisive file without changing `ExecMainStatus`.
- **unknown** — whether any child inherited fd 1 and wrote during the 7.554s run (no NUL gap and one document argue against it; not proven). Whether the file remains inode 2160272 / that sha256 until parent close. Mid-rung 17.7MB leg.

## Verbatim-landable (parent lands; this seat does not edit corpus)

```markdown
Provenance rule, arc2-r6-pe stdout: do not treat `/var/tmp/arc2-l6r6-pe/stdout.json` as sealed decisive evidence. The unit's `StandardOutput=file:` (systemd 261 `file:path`: write at offset 0, no truncate, not journal) left a mode-0644 file any uid-1000 process can rewrite; `journalctl --user -u arc2-r6-pe` has four lifecycle lines and none of the payload; InvocationID `31dc1c7f0a5e4f9db082dfc9da37b90d` and ExecMainPID `1992927` are absent from the file. Snapshot 2026-10-18T17:48:42-03: inode 2160272, 16692 bytes, sha256 `4a3ebb82f1978d00342734127d68c18431411c1553a2a0b4484a687c3f3c82b7`, mtime=ctime 2026-10-18 17:41:06.513410314 -0300. Copy and re-hash at close. Match → the honest-negative may cite that copy (`code: execution_failure`, no `analyzer_preset`, no `evidence_id`). Mismatch → big leg unverified; do not interpret the mutated file.
```
