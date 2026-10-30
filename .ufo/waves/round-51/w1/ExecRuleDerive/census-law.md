# R51-C1 device accounting derivation

## Class census from committed nonregular oracle tables

The oracle TSV contains directory, symlink and device rows. Device census is derived per carrier (not inferred from a representative unit):

| Class | Carrier | char-device rows | Device detail |
|---|---|---:|---|
| Cable | c6430 | 1 | `dev/led` `247:0` |
| Cable | c6490 | 1 | `dev/led` `247:0` |
| FRITZ!Box | g7581 | 13 | `dev/led` `247:0`; `dev/pts/0`…`dev/pts/7` `136:0`…`136:7`; `dev/tiatm` `230:0`; `dev/ttyp0`…`dev/ttyp2` `3:0`…`3:2` |
| FRITZ!Box | g7582 | 13 | same thirteen paths and major/minor values as g7581 |

All four tables contain no block-device, fifo, or socket row. Directory entries are published as directories (not regular-file paths); for symlinks the receipts record unpublished-entry gaps. Each receipt has 1 structural `depth-limited` gap and 19 path-resolved unpublished-entry gaps. Their `unpublished_entries_by_kind` counts symlinks as c6430=567, c6490=612, g7581=636, g7582=636. All four receipts record zero diagnostics (therefore no removal diagnostic disposition in these runs). No receipt reports a char-device, fifo, socket or block-device gap; no such path is recorded among published regular files. Thus every oracle device entry in all four carriers has **no disposition at all** (not a gap and not a removal), in both classes.

This is an entry-by-entry classification: the class table above explicitly lists all device rows; for the remaining nonregular rows, each `dir` is represented as a directory, each `symlink` is a `unpublished-entry` gap where such a receipt record exists, or, if it has neither a matching gap nor diagnostic, is an unreported symlink disposition. The v1 counter's disposition checker requires a disposition only for kinds with `required[kind]` true; an allowed gap kind by itself defaults required, but explicit `required.char-device=false` exempts device rows. `MaliciousSymlinkRemoved` diagnostic rows, if present, are exclusive symlink removals; none appear in these four receipts. Full path-by-path disposition assignment for symlinks is not reconstructed by this class census; rely on the frozen counter's exact path resolution when scoring.

## Law check against claims text

The claims sentence is: “the extraction producer (REA 6.5.0 `extract-firmware`, handler `squashfs_v4_le`, unblob 26.6.4 → sasquatch `-le`) materialises regular files and directories and re-creates symlinks (with a `MaliciousSymlinkRemoved` diagnostic when it refuses one), but it creates **no device nodes, fifos or sockets** — an unprivileged extraction cannot `mknod` — and it emits **no gap record for them**: a char-device/fifo/socket oracle entry is expected to carry **no disposition at all**.”

The carrier census agrees for char devices across both classes: 1/1/13/13 rows, all have no gap/removal/published regular-file disposition in the committed receipts. This supports the claims' stated model for these observed char devices, but does not independently prove producer behavior for fifo/socket because none occur in any of the four oracle tables. It likewise does not establish the syscall premise generally: the synthetic bounded probe below grounds only unsquashfs 4.7.5's non-root behavior.

## Rule encoding

`gap-rule-v2.json` retains path-resolved unpublished-entry allowances for symlink/char-device/fifo/socket, makes char-device non-required, removes the per-detail silent exception entirely, and retains symlink-removal semantics and structural allowances. There is no device-detail whitelist: Cable/FRITZ!Box are distinct only in their census, not the rule. Important counter-semantic caution: if a kind is not required, allowed gaps for it need not appear; this is the v1 checker behavior. Accordingly this encoding expresses the no-disposition law for device kinds, not “all devices must have unpublished-entry gaps.”
