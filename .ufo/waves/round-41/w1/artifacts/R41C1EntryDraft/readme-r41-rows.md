corpus/README.md — R41-C1 landing text (draft; L1 applies it at the freeze)
=======================================================================

Three edits. Edit 1 is scored (`coverage_map_row`); edit 3 is the Frontier update the claim names;
edit 2 is the practice round 40 followed and keeps the stem visible in the index.

EDIT 1 — `## Coverage map` table, append as the last row (after the
`| Genuine AVM-layout big-endian SquashFS v4 through REA (round 40) |` row, and still before the
`## Knowledge` heading; the counter searches only inside the `## Coverage map` section):

| Genuine AVM-layout big-endian SquashFS v4 through REA (round 41) | `2026-10-26-r41-avm-be-squashfs-core` | **Core** — `extract-firmware --max-depth 1` publishes every oracle regular file at its exact path relative to the chunk extract root (no suffix matching) on four frozen carriers (V3 FRITZ!Box 5490 07.31, V4 FRITZ!Box 5491 07.31, L3/L4 lane-built with both-direction path collisions); gaps one `unpublished-entry` per retained symlink plus one `depth-limited`; repairs round-40's suffix false negative (R40-CL1) and binds `member_sha256` in the vendor fetch chain (R40-CL6) {FILL:counter `carriers_matched 4/4`, exit 0}; LE AVM members and AVM kernels stay Frontier |

EDIT 2 — `## Knowledge` index, append as the last row:

| `2026-10-26-r41-avm-be-squashfs-core` | genuine AVM-layout BE SquashFS v4 via REA, Core: big-endian fields, little-endian metadata block lengths, no `-be`; exact extract-root path matching and the `member_sha256` fetch chain | S112, S114, S124, S121, S125, S127; receipts `corpus/evidence/round-41/c1/`; counter `tools/round-41/c1-counter.py` | 2026-10-26 |

EDIT 3 — `## Frontier`, the `sasquatch-v4be` lines. Keep both existing lines as dated history and append
one line after the round-40 line:

- sasquatch-v4be — 2026-10-26 round 41: the genuine AVM layout is **Core** (`2026-10-26-r41-avm-be-squashfs-core`), superseding the round-40 `measured, not promoted` line above; that stop was a counter suffix false negative (R40-CL1), not an image property. Still frontier: LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1, other vendor-mangled images.

Do not edit the round-38, round-39 or round-40 `sasquatch-v4be` lines themselves: the Frontier list is
append-only dated history, and the round-41 line names what it supersedes.

Boundary check before landing: `awk '/^## Coverage map/{f=1;next} /^## /{f=0} f' corpus/README.md | grep -c
'2026-10-26-r41-avm-be-squashfs-core'` must print `1`, and every `|` inside a cell must be absent (a pipe
inside a cell shifts the columns).
