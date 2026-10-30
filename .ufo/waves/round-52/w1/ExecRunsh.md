# ExecRunsh — R52-W1

Verdict: settled. Drafted `c1-run.sh` by porting the round-50 harness into the seat artifact directory.

- Changed only round segment/prefix, evidence segment, default OUTDIR, and C1 claim/schema labels; retained pinned versions (REA 6.5.0, unblob 26.6.4, sasquatch 4.5.1, unsquashfs 4.7.5), fixed PATH, data-run guard, provider-timeout retry, superblock precondition, and three-producer oracle from source.
- `bash -n` and an `oracle --dry-run` executed from a scratch copy each exited 0; dry-run created no output directory. Exact commands, UTC, stdout hashes, and dry-run stdout are in `ExecRunsh/validation.md`.
- Diff lines: `ExecRunsh/deltas.md`. No tools installed. No REA/data run performed.
- Risks: no full extraction/oracle run was performed (intentionally); landing L1 should review the port diff. Scratch cleanup completed after preserving receipts.

Files: `.ufo/waves/round-52/w1/ExecRunsh/c1-run.sh`, `deltas.md`, `validation.md`, `status.json`.
