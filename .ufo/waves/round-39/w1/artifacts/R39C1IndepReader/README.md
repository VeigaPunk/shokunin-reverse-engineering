# R39C1IndepReader — independent SquashFS 4.0 oracle reader (wave-1 artifact)

Seat: `R39C1IndepReader` (round 39, wave 1, pre-freeze). Everything here is a
development artifact; nothing is a frozen carrier and nothing was run through
REA. The lane is not mutated: this directory and the report are the only
outputs.

## Deliverable

`sqfs-list.py` — pure-stdlib SquashFS 4.0 reader, LE (`hsqs`) and BE (`sqsh`),
gzip (id 1) and LZMA/XZ (ids 2, 4), fragments and sparse blocks.
sha256 `1808c3f54205448761e27ffe8a82de59fe87300eb4c49ec406324800d148be7f`.

    python3 -I -B sqfs-list.py IMAGE --files OUT.tsv --symlinks OUT.tsv [--inspect]

Exit 0 ok, 2 unreadable/unsupported. `--inspect` writes a JSON summary
(superblock, counts, `symlink_reasons`, `decode_paths`) to stdout.

## Reproduction

    S=$(mktemp -d)
    A=<this directory>

    # 1. four committed oracles (read-only on the corpus)
    python3 "$A/check-oracles.py" --root <LANE> --artifacts "$A"
    #    -> oracle-check.txt, K1..K4.{files.tsv,symlinks.tsv,inspect.json}

    # 2. development fixtures + scoring
    python3 "$A/build-and-check.py" --work "$S/work" --artifacts "$A" \
        --gen <LANE>/tools/round-37/gen-squashfs.py
    #    -> A/B/C/L/B-be-*, D/S tables, build-and-check.txt

    # 3. extractor cross-checks (unsquashfs, sasquatch-v4be, unblob)
    python3 "$A/extractor-probes.py" --work "$S/work" --artifacts "$A" --lane <LANE>
    #    -> extractor-probes.txt

    # 4. measured limits of the lane generator (needs the fixtures from 2.)
    python3 "$A/generator-probes.py" --work "$S/work" --artifacts "$A" --lane-root <LANE>
    #    -> generator-probes.txt

## Files

| path | what |
|---|---|
| `sqfs-list.py` | the reader (deliverable) |
| `check-oracles.py`, `oracle-check.txt` | K1–K4 vs the committed `oracle.tsv`, byte-identical after a C-locale sort |
| `build-and-check.py`, `build-and-check.txt` | LE fixtures built with the lane generator and with `mksquashfs` 4.7.5, scored against their source trees and hand-derived symlink tables |
| `extractor-probes.py`, `extractor-probes.txt` | `unsquashfs` 4.7.5, `sasquatch-v4be` 4.5.1 and `unblob` 26.6.4 on the carriers and fixtures, plus a chain/cycle fixture (`chains-le-gzip`) whose symlink classes are compared with unblob's kept/removed outcomes |
| `generator-probes.py`, `generator-probes.txt` | four measured limits of `tools/round-37/gen-squashfs.py` (P1–P4) |
| `K*.files.tsv`, `K*.symlinks.tsv`, `K*.inspect.json` | per-carrier tables for K1–K4 |
| `<fixture>.*` | the same three tables for every development fixture |
| `images/*.sqsh` | the fixture images as built (the `mksquashfs`-built ones — `D*`, `S*`, `chains-le-gzip` — are not byte-reproducible: `mksquashfs` stamps the build time) |
| `sources/squashfs_fs.h.v6.12` | the on-disk layout authority, Linux v6.12 `fs/squashfs/squashfs_fs.h` as fetched |
| `sha256sums.txt` | hashes of every script, image and the header |
