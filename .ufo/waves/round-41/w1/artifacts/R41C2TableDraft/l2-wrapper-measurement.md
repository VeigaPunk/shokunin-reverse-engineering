# The `-be` PATH wrapper through REA 6.5.0 — measured 2026-10-26 (closes the round-39 L2 / round-40 L2 `[INFERENCE]`)

Seat `R41C2TableDraft`. This is development recon on a carrier this seat built from its own fresh
tree: no reserved image, no vendor byte, no lane carrier was read or run. It retires the one
carried-forward `[INFERENCE]` in the triage table — that a PATH executable named `sasquatch-v4be`
is what unblob actually executes under REA, and that appending `-be` is a delivery mechanism, not a
prose guess.

## What was built

```
tree:  alpha.txt ("alpha\n"), blob.bin (40 KiB from /dev/urandom), sub/beta.txt ("beta\n")
cmd:   python3 -I -B tools/round-40/gen-squashfs.py tree marked-be.sqsh --endian avm --comp gzip
out:   wrote marked-be.sqsh 41377 bytes, inodes 5 mode avm   (gen exit 0)
super: magic b'sqsh', mkfs_time 41377, bytes_used 41377, marker mkfs_time == bytes_used
sha256 marked-be.sqsh = ec65e7711da30d15306d95711fa3ef29932af69b5b3fc2122ab868675b8ea7e2
```

`--endian avm` is the round-40 "marker-only standard-BE body" mode: standard big-endian layout with
`mkfs_time := bytes_used`, which makes unblob's `is_avm` branch omit `-be` (S112 :48-50). Rebuild the
carrier from the three files above; the bytes are not copied into the lane (the tree is trivially
reproducible, the digest pins it).

## The three runs

Every run: `cd <fresh dir> && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0
extract-firmware --format json --full-output <carrier> <fresh outdir>`, exit 0 each time.

| # | PATH | envelope | receipt |
|---|---|---|---|
| 1 | unchanged | `H={squashfs_v4_be}`, `G={extractor-failure}`, `BE=no`, `P=0`, `extraction_failed: true`; recorded command `sasquatch-v4be -no-exit-code -f -d …`, stderr `SquashFS version [1024.0] / inode count [83886080] suggests a SquashFS image of a different endianess` … `FATAL ERROR: File system corruption detected`, exit_code 1 | `l2-env-baseline.json` (sha256 `3deb947b…`) |
| 2 | `wrap/` prepended, `sasquatch-v4be` = marker + `exec real -be "$@"` | `G=∅`, `P=4`: `WRAPPER-MARKER` (21 B) plus `alpha.txt`, `blob.bin`, `sub/beta.txt` with **sha256 equal to the tree's files** (`b6a98d9c…`, `1c8b22e6…`, `f2c82dec…`) | `l2-env-wrapper.json` (sha256 `449fca4c…`), wrapper text `l2-wrapper-sasquatch-v4be.sh` (`5bce229e…`) |
| 3 | `decoy/` prepended, `sasquatch-v4be` = writes `DECOY-MARKER` into the `-d` dir and exits 0 | `G=∅`, `P=1`: `DECOY-MARKER` | `l2-decoy-sasquatch-v4be.sh` (`9e683c9e…`) |

Repeat of run 1 (no wrapper, second attempt): identical failure, `P=0`, `G={extractor-failure}` — the
baseline is deterministic, not a race.

## What this establishes

1. unblob 26.6.4 inside REA 6.5.0 resolves the extractor **through PATH**: a `sasquatch-v4be` earlier
   on PATH is the binary that runs (run 3 publishes the decoy's own file; nothing else could).
2. Appending `-be` to that call flips the marker-doctored standard-BE carrier from
   `extractor-failure`/`P=0`/`BE=no` to a complete extraction whose three files are sha256-identical
   to the tree — i.e. row 5's `wrap-extractor-be` action is deliverable through REA exactly as its
   cause says, with no REA flag passthrough.
3. The wrapper **must be removed afterwards**: a leftover `sasquatch-v4be` that always appends `-be`
   re-adds `-be` on every later run, including genuine AVM-layout bodies, where `-be` is the wrong
   reading (round-39 D5b). The action token already says "then remove it".

## Observed and not explained (recorded, not claimed)

A wrapper that writes a side file **outside the extraction directory** (to the scratch tree or to
`/tmp`) leaves no trace, while the same wrapper's write **inside** the `-d` directory lands (run 2's
`WRAPPER-MARKER`, run 3's `DECOY-MARKER`, both mode `0600`, owner uid 1000 = this shell). `/fast` and
`/tmp` are both `xfs rw` and the child's uid is mine, so permissions and mounts do not explain it, and
the rea-agents 6.5.0 tree carries no `landlock`/`unshare`/`chroot` code path for the provider (only a
`PrivateRuntimeRoot` = `mkdtemp`). I did not find the mechanism and I am not claiming one. Consequence
for the lane: a wrapper used inside REA should prove itself with a marker file inside the extraction
directory, never with a side log — which is how the runs above are evidenced.

Rebuild everything: `gen-squashfs.py` line above, then the three REA commands with the two wrapper
scripts in `PATH`. No tool was installed; `unblob 26.6.4`, `rea-agents 6.5.0`, `sasquatch-v4be 4.5.1`
as already installed. Scratch removed at the end; the two envelopes and the two wrapper texts are the
retained receipts.
