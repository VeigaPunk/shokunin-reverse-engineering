"""At the measured revision REV, for each frozen carrier, the committed round-50 REA 6.5.0
`extract-firmware --max-depth 1` after-receipt (unblob 26.6.4, sasquatch 4.5.1 on the child
`PATH`, no `-be` binary needed), first added in a commit descending from the freeze, names the
`squashfs_v4_le` handler for the carrier's chunk with no failed chunk; publishes every regular
file of the frozen independent oracle (`unsquashfs` 4.7.5 listing + per-file sha256; a second
reader — the lane's pure-Python `tools/round-41/sqfs-list.py` `auto` layout — equals it) at its
exact path relative to the chunk extract root (equality after mapping into the root, never a
suffix) with the same sha256 and size, and no extra regular file; accounts for every non-regular
oracle entry by the frozen gap/removal rule (round-41 `gaps_ok` three-family disposition); has a
subject digest equal to the carrier pin and recomputes its evidence id; the carrier bytes hash to
the frozen pin and their superblock reads the frozen layout — **little-endian `hsqs`, v4.0,
compression id 4, `mkfs_time == bytes_used`** (the AVM marker); **and** a counter-time REA rerun
of the same bytes (scratch output directory, carriers fetched through the pinned chain or the
`--carrier-cache`) has the same semantic projection as the committed receipt; **and** the
receipt's `parameters.output_directory` starts with `/fast/scratch/hyaku/kaidoku-r50/` (prefix
test, no `..`); documentation bindings: `PROVINCE.md` holds a `## Round-50 additions to Core`
section whose row names `squashfs_v4_le` with the AVM marker and cites the entry path; one line
carries `Round-50 frontier note`, the entry stem and an LE-AVM token; the entry exists at REV and
its `source:` lines cite SOURCES rows opened `2026-10-28`..`2026-10-29` that list the entry in
`used-by`; `corpus/README.md` `## Coverage map` maps the entry stem; no frozen C1 path changed
after the freeze.
"""
