# Companion rows — NOT one of the three named blocks (routed to L1; add only if the L1 wants
# corpus/README.md consistent with the PROVINCE blocks). Neither companion changes command A
# (its map leg reads the `## Coverage map` section only, so the `## Knowledge` row is inert
# there and the `## Frontier` bullet is outside it).

## Companion 1 — `corpus/README.md` `## Frontier`, append AFTER the last bullet
## ("- Blocked-on-operator: IDA …"), before `## Known gaps`:

- sasquatch — 2026-10-28 round 44: SquashFS v1/v2 is **Core** (`2026-10-28-r44-squashfs-v1v2-core`), superseding the `v1/v2` item of the round-42 line above and that item only. Still frontier there: `squashfs_v3_broadcom`/`_nonstandard`, gzip v3; `squashfs_v2_nonstandard` (`v2ns-*`) also stays frontier — no independent reader.

## Companion 2 — `corpus/README.md` `## Knowledge`, append AFTER the last row
## (`2026-10-27-sasquatch-release-matrix`), before `## Lessons`:

| `2026-10-28-r44-squashfs-v1v2-core` | SquashFS v1/v2 via REA `extract-firmware`, Core: `squashfs_v1`/`squashfs_v2` handler bound per carrier from the superblock (magic, `s_major`, endianness), four committed unblob 26.6.4 fixtures both byte orders, independent `unsquashfs` 4.7.5 oracle cross-checked against the `__output__` expected trees; v2ns stays Frontier (no independent reader) | S138, S139; receipts `corpus/evidence/round-44/c1/`; counter `tools/round-44/c1-counter.py` | 2026-10-28 |
