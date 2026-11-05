source: S322 (fsync(2), Linux man-pages, https://man7.org/linux/man-pages/man2/fsync.2.html; fetched 2026-11-05, sha256 f0a986d21500222ecb69580fc7a910f346c6b1ff1005ca515501fb05bb5d91f5, copy `.ufo/waves/round-97/pre/s322-fsync2-fetch.html`); lane instruments under `tools/round-97/` and `.ufo/waves/round-97/`
verified-at: 2026-11-05 (the landing revision of round 97; the freeze is commit `e859a88d78567c44bc1ecfd211afe123755ae1c7`)
recheck: `python3 -I -B tools/round-97/kill-rule-v3.py --root . --work <scratch> --mutants .ufo/waves/round-97/mutants.json --fixtures .ufo/waves/round-97/forgery --prefix forge --decl e859a88d78567c44bc1ecfd211afe123755ae1c7 --json-out <receipt>` (exit 0 required) and `python3 -I -B tools/round-97/depth-blocks-v4.py --root . --rev <landing> --expect-blocks 36 --shape-from 36` (exit 0 required)

# Receipts that name a revision must carry that revision's bytes, and a receipt write must reach the disk

A receipt is a claim that a counter measured a named revision. Round 96 showed the
claim could be false while every check passed: the counter's receipt named the clean
HEAD and carried the digest of a dirty working-tree counter, so the verifier compared the
receipt to the live files and found them equal. The pinned round-96 counter
`tools/round-96/stop-boundary-repair-battery-v6.py` exited 0 on exactly that dirty tree
(`.ufo/waves/round-97/pre/c1-dirty-v6-admits.json`, `v6_dirty_exit 0`).

## Observed

- **The byte binding.** A pin is bound to the named revision by reading the blob at that
  revision: `git cat-file blob <revision>:<path>` and its sha256. A pin that matches the live
  file and not the blob is `byte-pin-not-bound:<key>`. Measured: the v7 counter refuses a
  dirty clone's counter pin on the public path with `byte-pin-not-bound` where v6 exits 0
  (`.ufo/waves/round-97/l1/scores/` dirty-clone leg of the frozen kill rule).
- **The durability ordering.** A receipt write fsyncs the file before the atomic replace,
  then fsyncs the containing directory, because a rename durable in the page cache is not
  durable on disk until the directory entry is flushed. The fsync(2) page states the
  directory case directly: "Calling fsync() does not necessarily ensure that the entry in
  the directory containing the file has also reached disk. For that, fsync() on a file
  descriptor for the directory is also needed." (S322; located in the fetched copy.)
- **The typed booleans and the allow-list.** `met_target` must be a real boolean; a counts
  object must carry the nine label keys as integers and no other key. Each violation is a
  typed reason (`met-not-typed`, `counts-extra-key:<k>`), so a receipt that the pinned v6
  verifier accepted with an absent `met_target` is refused.

## Not established

- The byte binding proves which bytes a revision contains, not that the process that
  wrote the receipt was not replaced afterwards.
- The directory fsync is measured by an instrumented call count (`os.fsync` observed
  before and after `os.replace`), not by a power-loss test; the claim is the ordering the
  code issues, not a crash-consistency proof of the filesystem.
- The provenance of a wholly re-authored receipt that describes the honest world
  consistently remains unauthenticated (the same limit recorded in Row 191).
