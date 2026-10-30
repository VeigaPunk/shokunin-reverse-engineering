## Round-51 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-marker little-endian SquashFS v4 (`hsqs`, v4.0 xz, `mkfs_time == bytes_used`) members of four public FRITZ!OS images (7581/7582 07.18, 6490 Cable 07.57, 6430 Cable 07.30 x86 members) — handler `squashfs_v4_le` | no new REA key — unblob 26.6.4 runs plain `sasquatch -le` for every LE v4 chunk (S245 :53-54; the AVM marker test exists only in the BE branch, :48); `REA_UNBLOB_COMMAND` = unblob 26.6.4; `extract-firmware --max-depth 1` with the frozen `rea_parameters` budgets | `extract-firmware` (rea-agents 6.5.0) on the four chain-pinned vendor carriers, re-run under the round-51 law-derived device-accounting rule (`tools/round-51/gap-rule.json`) and scored by `tools/round-51/c1-counter.py` at the freeze `<<FREEZE_COMMIT>>` | entry `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` (S243, S244, S245, S249, <<R51_SOURCE_ROWS>>); carriers chain-pinned by `tools/round-51/fetch-vendor.py`, never committed; fresh receipts `corpus/evidence/round-51/c1/<<ID>>/{run.json,after.json}` (`<<ID>>` = g7581, g7582, c6490, c6430); the counting command's score `<<.ufo/waves/round-51/l1/scores/c1-after.json>>` reports `carriers_matched <<4>>`, exit `<<0>>`, `gaps_ok` true on every carrier, `frozen_path_changed []`; the before-arm is the committed round-50 receipt `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (`carriers_matched 2`, exit 1) |

The device-accounting law this row stands on (derived in round 51, stated before the freeze): the
extraction producer (REA 6.5.0 `extract-firmware`, handler `squashfs_v4_le`, unblob 26.6.4 →
`sasquatch -le`) materialises regular files and directories and re-creates symlinks (with a
`MaliciousSymlinkRemoved` diagnostic when it refuses one), but it creates **no device nodes, fifos
or sockets** — an unprivileged extraction cannot `mknod` — and it emits **no gap record for them**:
a char-device/fifo/socket oracle entry is expected to carry **no disposition at all**. The
round-50 frozen rule's `removed.silent.char-device: ["247:0"]` generalised one Cable-carrier
detail into a class-wide whitelist and left the FRITZ!Box class's other twelve char-devices with
neither a matching gap nor a removal (M50-7); that is why that freeze matched 2 of 4.

The per-class census the rule is derived from (measured from the committed oracle tables
`tools/round-50/oracle/<id>.nonregular.tsv`, sha256 in the round-51 report):

| carrier class | carriers | char-devices per carrier | symlinks | dirs | non-regular entries | other kinds |
|---|---|---|---|---|---|---|
| Cable | `c6430`, `c6490` | 1 (`dev/led` 247:0) | 568 / 613 | 255 / 300 | 824 / 914 | none |
| FRITZ!Box | `g7581`, `g7582` | 13 (`dev/led` 247:0; `dev/pts/0-7` 136:0-7; `dev/tiatm` 230:0; `dev/ttyp0-2` 3:0-2) | 639 / 639 | 349 / 349 | 1001 / 1001 | none |

No fifo, socket or block-device entry occurs in any of the four tables (the kinds present are
`symlink`, `dir`, `char-device` only). The class distinction is a property of the carriers' device
census, not of the rule.

The row above supersedes the status of the block `## Round-50 measured, not promoted (R50-C1 honest
stop)` above for the LE AVM members only: that block's `measured, not promoted` status came from
the frozen rule's Cable-class generalisation, not from the carriers. The block stays as the
round-50 measurement record; its receipts and oracle tables are re-used as the round-51 pre-freeze
controls (CTL-OLD over the same receipts stays red at `carriers_matched 2`).

Honest scope: the promoted surface is the four pinned vendor members under the law-derived
accounting rule — not every LE AVM image, and not "REA recognises AVM": the AVM marker
(`mkfs_time == bytes_used`) is a constant of the pinned bytes (unblob 26.6.4 tests it only in its
big-endian branch, S245 :48), so a standard LE body with the marker patched in produces the same
projection. Still Frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box
7530/7590, observed), AVM kernels, nested sub-images below depth 1, other vendor-mangled images,
v4 Broadcom, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies,
`squashfs_v2_nonstandard`, v2.1 images.

Round-51 frontier note, 2026-10-30: LE AVM members (`hsqs`) moved Frontier → Core with `2026-10-30-r51-avm-le-squashfs-core` (four chain-pinned FRITZ!OS members re-run under the device-accounting law derived per carrier class; `carriers_matched <<4>>`, exit `<<0>>`, `gaps_ok` true on every carrier, `frozen_path_changed []`). This note supersedes the LE-AVM clause of the round-40/41/42/44/49/50 notes' Still-Frontier lists, and the LE-members clause of the `## Round-50 measured, not promoted (R50-C1 honest stop)` block, and nothing else: the round-50 miss was a rule-generalisation defect (one char-device `247:0` allowance generalised from the Cable-carrier class), not a carrier defect. Still Frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed), AVM kernels, nested sub-images below depth 1, other vendor-mangled images, v4 Broadcom, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, `squashfs_v2_nonstandard`, v2.1 images.
