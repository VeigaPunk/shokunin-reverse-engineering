# SentinelWrite — adversarial security review, round 91

Scope: `tools/round-91/upx-stop-boundary-repair.py` and `tools/round-91/stop-boundary-battery.py`
at declaration commit `deb2765a55fef0e4e81500a027dfe59951b69e87` (base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`).
Read-only on the lane. All runs in a scratch clone (`git clone --shared` + `checkout deb2765`), scratch removed.
Pins verified before any run: worktree = declaration commit (`git diff --stat` empty); sha256 repair
`473bb3a9…` and battery `5998b6bd…` match `claims.json`; `/usr/bin/upx` `cf2f6e7c…`, upx 5.2.0.
Tools used: `strace` (already at `/usr/bin/strace`), `/home/vgpnk/.local/bin/time` (already present). No installs. Receipts: `w1/SentinelWrite/receipts/`.

## Verdict

No HIGH finding. Two MED (availability of the refusal path; a contract violation in `--info`), five LOW.
No path executes a shell, injects an option into `upx`, follows a symlink target on write, or writes into
the lane. The frozen C1 counter reproduces in the clone (`refused 8 of 8; unsafe 0; intact 4 of 4`, met true, exit 0).

## Findings (ranked)

### MED-1 — crafted input drives quadratic CPU and ~11x memory before the refusal
Mechanism (read from code, measured): `classify` → `chain_ok` → `find_sentinel` loops over every byte offset
from the stop to the PackHeader in Python (`struct.unpack_from` per offset) and builds a per-call `memo`
dict with one entry per chain node. `derive_break` then, for every plausible successor header in its
window (`derived <= su_p`), does `bytearray(d)` + `bytes(dd)` (two full copies) and a fresh `chain_ok`
(another full `find_sentinel` pass). Per-candidate cost is therefore a full-input pass; the number of
candidates scales with input size, so total cost is ~quadratic in N. The refusal is reached only after this work.

Reproduction (input from `w1/SentinelWrite/craft-input.py`, which is byte-identical to the measured inputs):
```
python3 -B w1/SentinelWrite/craft-input.py 67108864 27 $S/craft-64M-C0.bin      # C = 0 successors
python3 -B w1/SentinelWrite/craft-input.py 67108864 208 $S/craft-64M-C10.bin    # C = 10 (su_p = 28+20*(10-1))
TMPDIR=$S/tmp HOME=$S/home PATH=/usr/bin:/bin LANG=C \
  /usr/bin/time -f 'MAXRSS_KB=%M WALL_S=%e' python3 -I -B tools/round-91/upx-stop-boundary-repair.py --in $S/craft-64M-C10.bin --out $S/o.bin
```
Observed (all rc 2, refused `stop-boundary`):

| input | C | rc | wall | max RSS |
|---|---|---|---|---|
| 8 MiB | 0 / 3 / 6 | 2 / 2 / 2 | 1.78 s / 4.24 s / 6.77 s | — |
| 64 MiB | 0 | 2 | 14.11 s | — |
| 64 MiB | 10 | 2 | 94.96 s | — |
| 256 MiB (cap) | 0 | 2 | 59.00 s | **2,843,664 KB** |

Per-candidate cost ≈ 0.83 s at 8 MiB and ≈ 8.1 s at 64 MiB (linear in N per candidate). The 256 MiB RSS is
dominated by the `find_sentinel` memo (about N/20 entries) plus the input [INFERENCE on attribution; the
total is measured]. Extrapolation: a 256 MiB input with ~N/20 ≈ 13.4 M successors would run for days to
years [INFERENCE]. On a host with less memory than ~3 GB, the process is OOM-killed, so no typed refusal
is produced (rc would be a signal, not 2) [INFERENCE].
Impact: local resource exhaustion from a crafted artifact processed by the lane; no integrity loss; the
cap (256 MiB) bounds size only, not work. Suggested remediation: compute the chain once and bound the candidate
count; do not copy the input per candidate (patch and undo in place, or pass the derived value as an argument);
replace the per-byte Python scan with a bounded walk.

### MED-2 — `--info` failure after a successful `--out` write returns rc 2 with the output on disk
`main()` writes `--out` first, then `write_atomic(args.info, …)`. If the info path is refused, the `Refused`
handler returns rc 2 ("refused") while the output file already exists. The documented contract is
"rc 2 = typed refusal, no output written".
Reproduction (`$S/inputs/xxd.packed` = `upx --best` of `/usr/bin/xxd`, intact):
```
python3 -I -B tools/round-91/upx-stop-boundary-repair.py --in $S/inputs/xxd.packed --out $S/t/ok.bin --info $S/t/nodir/x.json
```
Observed: rc 2, stdout `…"refused": "--out parent is not a directory: …/nodir"`, and `$S/t/ok.bin` exists with bytes
identical to the input. Frozen battery is unaffected (it passes no `--info`), but any caller that trusts rc 2 to
mean "nothing written" is wrong. Fix: validate and write all outputs before the first `os.replace`, or report
the partial write in the rc-2 message.

### LOW-1 — `--out` symlink guard checks only the immediate parent
`checked_target` refuses when `os.path.islink(parent)` (immediate parent only). A symlinked ancestor is followed.
- `--out link/out.bin` (immediate parent is the symlink): rc 2, `--out parent is a symlink` (T1, verified).
- `--out link/sub/out.bin` where `link -> real`, `real/sub` exists: rc 0; `real/sub/out.bin` created through the link (T2, verified).
Operator-chosen path, so this needs attacker write access to the output tree; TOCTOU between `checked_target` and
`mkstemp(dir=…)` is the same class (theoretical, not reproduced deterministically). Fix: `os.path.realpath(parent)`
under an expected root, or refuse any symlink component.

### LOW-2 — battery receipt does not bind the upstream modules it loads
The receipt keys are `carriers, cells, class, counter_sha256, counts, exit, expect, intact, label, met_target,
repair, repair_sha256, revision, tool`. `repair` loads round-87/88/89/90 modules with no runtime sha check (the
round-90 sha is only recorded in `info`). `claims.json` pins them, but nothing enforces the pins.
Mutant (clone only): appended a comment to `tools/round-88/upx-chain-repair.py`
(sha `59ee51b0…` → `3b52c973…`). Battery re-run: rc 0, label `refused 8 of 8; unsafe 0; intact 4 of 4`,
`repair_sha256` and `counter_sha256` identical to the unmodified receipt. Behaviour-changing mutants would change
cells, but the receipt would still name the same repair and counter. Receipts: `receipts/big-and-mutant.json`,
`receipts/battery-mut.json`. Fix: record and check the upstream shas in the counter.

### LOW-3 — tool invoked through a symlink fails with rc 1
`ROOT` is derived from `os.path.abspath(__file__)` (no realpath), so a symlinked copy looks for siblings
next to the link. Reproduced: `ln -s …/upx-stop-boundary-repair.py $S/bin/upx-link.py`, run it →
rc 1, `FileNotFoundError: …/kaidoku-r91/tools/round-87/upx-magic-repair.py`. Functional, typed as an internal error.

### LOW-4 — output file mode is 0600, not the umask default
`write_atomic` uses `mkstemp` (0600) and `os.replace` keeps it. Reproduced: `stat -c %a` on the T2 output → `600`.
Functional for shared artifacts; not a confidentiality defect for the operator's own run.

### LOW-5 — file descriptor leak in `upx_test` if `os.fdopen` raises
`fd, path = mkstemp(...)`; if `os.fdopen(fd, "wb")` raises (simulated ENOSPC), the fd is not closed. The
`finally` removes the file (verified: no leftover), but the fd leaks once per failure.

### LOW-6 — `upx_test` copies the whole input into the temp directory
`upx_test` writes the full input (up to 256 MiB) to `tempfile.gettempdir()` before `upx -t`. This is the only
write outside the output directory (besides `--info`). strace of the crafted run shows `openat(…/tmp/.r91-test-*,
O_RDWR|O_CREAT|O_EXCL|O_NOFOLLOW, 0600)` then `unlink`. Disk amplification of up to 256 MiB per call; by design.

## Checks that found nothing

Each check ran; the evidence is the cited command or receipt.

1. **Shell use.** `grep` of both files: `subprocess.run` takes an argv list at all three call sites (`upx -t`, `upx --best`, the battery's `run`); no `shell=True`, `os.system`, `popen`, `eval`, `exec`.
2. **Environment reduction.** Repair `upx` child env = `{PATH, LANG=C, HOME=gettempdir()}`. Hostile env run: `UPX=-d UPX_DEBUG_DISABLE_DOCTEST=1 LD_PRELOAD=/nonexistent.so` on the intact carrier → repair rc 0, class `intact`, output written (T14). Control: direct `/usr/bin/upx -t -q` under the same env → rc 1, `illegal option in environment variable 'UPX'`. So the inherited `UPX` option would have changed the verdict, and the reduced env prevents it.
3. **Relative/option-looking TMPDIR.** `TMPDIR=-V` (existing dir): `gettempdir()` returns the absolute `…/rel/-V`, so argv never starts with `-`. Control: `upx -t -q "-V/.r91-test-x"` rc 1, invalid option. No injection.
4. **Temp name predictability.** `mkstemp` (random 8-char, `O_EXCL|O_NOFOLLOW`) for `.r91-write-*` and `.r91-test-*`; battery uses `mkdtemp`. Strace shows `O_EXCL|O_NOFOLLOW` on the test file. Pre-created names cannot be reused.
5. **`upx_test` cleanup on every path.** In-process spy (`$S/upx-test-cleanup.json`): normal return → no leftover; `subprocess.run` raising → propagated, file removed; `TimeoutExpired` → propagated, file removed; `os.fdopen` raising → propagated, file removed. Argv is `["/usr/bin/upx","-t","<tmp>"]`, `shell=False`.
6. **`--out` as a symlink to a victim.** `--out victim-link` → rc 0, victim content unchanged (`VICTIM`), link replaced by a regular file (T3). `os.replace` does not follow.
7. **`--out` dangling symlink.** Ghost target not created; link replaced (T4).
8. **`--out` existing directory.** rc 2, `--out is a directory` (T5).
9. **`..` in `--out`.** rc 2; `x.bin` not created (T6).
10. **`--out` parent is a regular file.** rc 2 (T7).
11. **`--info` symlink to a victim.** Victim unchanged, link replaced (T9).
12. **`--out /dev/null`.** rc 1 `PermissionError` on `/dev/.r91-write-*`; no write (T10).
13. **Input cap.** Sparse 256 MiB + 1 → rc 2, `input exceeds 268435456 bytes`, 0.03 s (T12). Exactly 256 MiB → passes the cap, refused `not a little-endian ELF`, 0.22 s (T12b).
14. **Input type.** Symlink and FIFO inputs → rc 2 `input is not a regular file` (T13a/b); `lstat` before `open`.
15. **Battery writes.** strace of the battery (`receipts/wr.txt`, 96 write-class events): all under `--work` or its `tmp/`, except the operator-given `--json-out`. Zero writes under the lane.
16. **Battery frozen label, independent reproduction.** Scratch clone at `deb2765`: `label refused 8 of 8; unsafe 0; intact 4 of 4`, met true, exit 0, counts `{refused 8, unsafe 0, intact 4, silent 0, recovered 0}` (`receipts/battery.json`). The regression arm (P1–P3) was not in my item and was not run.
17. **Repair selftest.** `--selftest` → `SELFTEST cases=4 failures=0`, rc 0.
18. **Symlink/option tricks on the counter.** Battery calls the repair with `sys.executable -I -B` and a box dir from `mkdtemp`; carriers are pinned by sha256 before use.

## Not checked (scope)

- Round-90 regression arm and the other classes; not in my item.
- Race conditions beyond the theoretical TOCTOU notes (LOW-1, LOW-6); I did not build a deterministic race harness.
- Host memory limits for MED-1 under OOM; the 256 MiB case was measured on this host only.
