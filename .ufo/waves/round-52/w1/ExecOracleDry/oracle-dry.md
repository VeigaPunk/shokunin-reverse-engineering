# Oracle dry run — synthetic SquashFS

Fixture: two regular files (`a.txt`, `sub/b.txt`), one symlink (`sub/link -> ../a.txt`), one FIFO (`pipe`). `mknod <path> p` succeeded unprivileged (`fifo-result.txt`). `mksquashfs` produced little-endian v4 xz; its superblock is non-AVM (`avm_marker: false`).

All three producers ran: pure-Python `sqfs-list.py --layout auto` (harness additionally ran `auto` and `le`), `/usr/bin/unsquashfs -no-xattrs -f -no-exit-code` plus `-lln`, and `sasquatch -le -f -no-exit-code -n`. Each extracted/reported two regular files with the same sorted `relpath<TAB>sha256<TAB>size` rows. `unsquashfs -lln` recorded the FIFO; Python reported nonregular entries `pipe` as `fifo`, `sub` as `dir`, and `sub/link` as `symlink` with target `../a.txt`.

**Mismatch:** harness crosscheck `all_equal=false`, mismatch_count 2: `pipe` was an `unexpected-special-in-tree` against both extraction trees. Both extractors created the FIFO in the extraction tree, while the harness comparison expects special entries only in the `-lln` listing (the contract notes that unprivileged extraction cannot create them). The regular-file data agree; whole-oracle verification did not pass. Harness returned 3. This fixture exposed a synthetic-special-file assumption mismatch, not disagreement in regular-file contents. The L1 should decide whether to adapt the fixture (omit FIFO) for clean positive harness agreement or amend the intended extractor behavior/check; do not represent this as a clean harness pass.

Harness was run with `C1_ALLOW_NONAVM=1` (the documented waiver for control carriers), `C1_ALLOW_PIN_DRIFT=1`, and `C1_ALLOW_FOREIGN_SCRATCH=1` (required because the task scratch does not include the R50 provenance segment). It accepted and recorded the non-AVM waiver and `run_provenance_segment_ok:false`. Installed unsquashfs was 4.7.5. The first harness attempt returned 2 because the foreign scratch segment was not waived; retry used the allowed waiver.

An initial direct extraction attempt was also invalid: destination parents were missing, causing unsquashfs failure and empty extracted tables. Created both roots and reran successfully. This initial attempt is retained in scratch-derived stdout capture and not used in the comparison.

## Predictive limit

The positive component evidence covers small LE/xz regular files, a directory, symlink and FIFO. The harness-level negative is relevant: its declared behavior conflicts with a locally extractable FIFO. This does not establish behavior on AVM vendor images, large images, device nodes/socket, alternate block layouts or the four target carriers. The L1's post-freeze vendor oracle run remains necessary; resolve the FIFO comparison expectation before treating special-entry crosschecks as validated.

## Evidence

`receipts.json` records exact invocations, exit codes, stdout SHA-256 and UTC capture time; `harness/oracle-run.json` contains tool pins, producer results, tables and crosscheck. Individual tables/logs and the FIFO creation result are retained. No REA or vendor download was run.
