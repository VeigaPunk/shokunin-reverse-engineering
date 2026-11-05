# SquashFS `extract-firmware` outcome triage v2: a domain guard, three outcomes v1 could not label, and an action scored with every label (round 40)

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` lines 24-70 (AVM branch 44-50) — as read 2026-10-26
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `fix_symlink` lines 50-92 — as read 2026-10-26
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `dist/firmware/FirmwarePublication.js:68-75,239-307` — as read 2026-10-26
source: S120 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py — `report.py:91-98` — as read 2026-10-26
source: S123 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — where `operation` and `provider.id` are set; `extract_firmware`→`unblob`, `inspect_firmware_regions`→`binwalk` — opened 2026-10-26 (round-40 wave 1, `.ufo/waves/round-40/w1/R40SrcReaOps.md`)
verified-at: 2026-10-26
recheck: 180d — `python3 -I -B tools/round-40/sqfs-triage-v2.py --skill SKILL.md --table-only` -> 11 rules, exit 0

**What v2 adds.** Rule block 19 in `SKILL.md` `## Queue-drain craft` holds table v2 after the marker
`<!-- sqfs-triage-table v2 -->`, read by `tools/round-40/sqfs-triage-v2.py`. It keeps the six v1 features
(`H` squashfs chunk handlers, `G` gap kinds, `D` gap dependencies, `BE` a recorded standalone `-be`,
`SR` a `MaliciousSymlinkRemoved` report, `P` the published file count) and adds two domain features read
first: `OP` = `data.operation` and `PV` = `data.provider.id`. Each row also carries one `action` token from
the closed vocabulary on the `<!-- sqfs-triage-actions: … -->` line; labels are unique, so a label is a row
decision, and the scored answer is the (label, action) pair. No match is (`unclassified`, `none`).

**Domain guard (routed R39-CL1).** Every v2 row requires `operation` = `extract_firmware` and `provider` =
`unblob`. REA 6.5.0 sets both per operation (S123); of 33 operations run on a bare SquashFS carrier only
`inspect-firmware-regions` returns an `ok` envelope with a `normalized_result`, and it is
`inspect_firmware_regions` / `binwalk` (`.ufo/waves/round-40/w1/R40C2ReconDomain.md` §2). The v1 table
labels that envelope `no-squashfs-chunk`, a SquashFS verdict on a region scan, because its v1 feature vector
equals a genuine empty `extract-firmware` envelope; only the two domain columns separate them. In the
held-out set the operation and provider change together, so the provider cell is not tested on its own.

**Three outcomes v1 could not label.** (1) `mixed-symlinks` (routed R39-CL2): an image holding both an
escaping and an in-tree link records `G = {unpublished-entry}` and `SR = yes`; v1's escaping row matched on
`SR` alone and told the reader to ignore the in-tree gaps, which round-39 Core carriers K5 and K6 carry
(S118 lines 50-92 remove the escaping link and report it; S119 `FirmwarePublication.js:68-75` records the
kept link as one gap). v2 puts the mixed row first. (2) `partial-body-failure` (R39-CL3 D1): a damaged
body that still publishes files records `extractor-failure` with `P > 0`; v1's body row demanded `P = 0`.
(3) `clean-empty` (R39-CL3 D2): a clean extraction of a tree with no regular file records no gap and
`P = 0`; v1's clean row demanded `P > 0`. Recon: `.ufo/waves/round-40/w1/R40C2ReconMixed.md`,
`R40C2ReconPartial.md`, `R40C2ReconEmpty.md`.

**The AVM-marker row, stated against the genuine AVM layout.** unblob omits `-be` exactly when
`mkfs_time == bytes_used` (S112 lines 44-50). On a standard big-endian body with that marker set,
`sasquatch-v4be` then reads the body in the wrong byte order and fails: row `avm-marker-be-dropped`,
action `wrap-extractor-be`. A genuine AVM-layout body (big-endian fields, little-endian 2-byte metadata
block-length headers) extracts without `-be` and publishes its files, so it never reaches this row; its
failure would be damage. The envelope cannot see block-length endianness, so the row's cause tells the
reader to walk the inode-table metadata headers little-endian before wrapping (round-40 C1 entry
`2026-10-26-r40-avm-be-squashfs-core`).

**Scoring.** Held-out carriers come from `tools/round-40/heldout-gen-v2.py` with seed = the round-40
freeze commit hash: 13 classes × 2 replicates that differ in endianness, compression or tree, each
assigned its (label, action) pair before any REA run. On the 26 development envelopes (seed
`sha256("dev40")`) the round-39 v1 table agrees with 18 of 26 classes; the eight misses are exactly the
mixed, partial, clean-empty and out-of-domain classes (`.ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/v1-table-on-v2-dev-set.txt`).

**Limits.** A table with one load-bearing cell per label can also score every envelope of a closed class
set (`.ufo/waves/round-40/w1/R40C2AxisFit.md` (c)); the score shows the table decides these classes, not
that every cell is necessary. The `cause` column is prose and is not scored; the action token is. Not
covered: genuine AVM-layout outcomes (that is the C1 surface), `unknown-chunk-handler`, `encrypted-chunk`
and `depth-limited` envelopes, and anything about extracted programs.
