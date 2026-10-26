PROVINCE.md — R41-C1 landing text (draft; L1 applies it at the freeze)
=====================================================================

Placement (three edits, all in PROVINCE.md):

1. Append the section below at the END of PROVINCE.md, after the current last block
   `## Round-40 measured, not promoted (R40-C1 honest stop)` and its `Round-40 frontier note` line.
   Do not rewrite the round-40 block; it stays as history.
2. Do not renumber or move anything above it.
3. Nothing else in PROVINCE.md changes for R41-C1.

Binding requirements this text satisfies (round-41 ports, measured from the seat artifacts):
`tools/round-41/c1-counter.py` requires the exact heading string, a row in that section whose FIRST cell
names `squashfs_v4_be` and whose line also carries `AVM[-_ ]layout` and the entry path, and a line starting
`Round-41 frontier note` that names the heading, the entry stem and the AVM-layout token
(`.ufo/waves/round-41/w1/artifacts/R41C1Counter/c1-counter.py:220-256, 1250-1275`).
The supplementary gate `tools/round-41/c1-extra.py` additionally requires the SAME one line to contain a
supersede verb AND the phrase `measured, not promoted`, so the round-40 honest-stop record cannot be
mistaken for superseded by silence (`…/R41C1Extra/c1-extra.py:131-155`).

---------------------------------------------------------------------------------------------------
SECTION TO APPEND (verbatim; the single line marked NOTE must stay one physical line)
---------------------------------------------------------------------------------------------------

## Round-41 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| genuine AVM-layout big-endian SquashFS v4 (`squashfs_v4_be`) | no new REA key — unblob 26.6.4 appends `-be` to `sasquatch-v4be` only when the AVM marker `mkfs_time == bytes_used` is false (S112 lines 44-50), so a genuine AVM body runs `sasquatch-v4be` WITHOUT `-be` (S121 lines 664-669, 4389-4400); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); `sasquatch-v4be` 4.5.1; `extract-firmware --max-depth 1` (a vendor member exceeds the 10 000-entry staging budget at the default depth) | `extract-firmware` (rea-agents 6.5.0) on four frozen carriers no extractor touched before the freeze — V3 FRITZ!Box 5490 FRITZ!OS 07.31 member `./var/tmp/filesystem.image`, V4 FRITZ!Box 5491 FRITZ!OS 07.31 {FILL:V4 carrier = the nested filesystem_core.squashfs carved to its own bytes_used, or the wrapper member if the nested image does not fit the staging budget}, L3 lane-built AVM layout xz and L4 lane-built AVM layout gzip (both carrying in-tree and absolute symlinks and both-direction path collisions) — against the frozen reader oracle; vendor bytes fetched by `tools/round-41/fetch-vendor.py` (url -> image sha256 -> member sha256 -> carve -> pin), never committed | entry `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md`; every oracle regular file published at its exact path relative to the chunk extract root with the same sha256 {FILL:V3 8/8, V4 6349/6349, L3 13/13, L4 14/14}, no regular file at a non-regular entry's exact path, gaps one `unpublished-entry` per retained symlink plus one `depth-limited`, no failed chunk, `plus-extractor` projection reproduced by the counter's own rerun; counter `tools/round-41/c1-counter.py` `carriers_matched {FILL:carriers_matched 4}` exit {FILL:exit code 0} at `{FILL:measured revision}`; receipts `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json` |

The row above supersedes the status of the block below for the genuine AVM layout only: the layout was
correctly measured in round 40, and the block's own status line was a counter false negative. A standard
big-endian body whose AVM marker was stripped stays governed by `## Round-39 additions to Core`, and
LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1 and other vendor-mangled
images stay Frontier.

The frontier-note line below must stay ONE physical line, must begin at column 0 with the marker, and must
not be reflowed by any formatter. Do not wrap it:

Round-41 frontier note, 2026-10-26: for the genuine AVM layout the block `## Round-40 measured, not promoted (R40-C1 honest stop)` above is superseded by `## Round-41 additions to Core` (`2026-10-26-r41-avm-be-squashfs-core`); its `measured, not promoted` status came from a counter suffix false negative (R40-CL1), not from the images, and this note also supersedes the AVM sentence of the round-39 note. Still Frontier: LE AVM members (`hsqs`), AVM kernel images, nested `filesystem_core` images below depth 1, other vendor-mangled images.

---------------------------------------------------------------------------------------------------
END OF SECTION
---------------------------------------------------------------------------------------------------

Notes for the integrator
------------------------
- The heading line, the word `squashfs_v4_be`, the token `AVM-layout`, the entry path, and the frontier
  note's start `Round-41 frontier note` are all load-bearing tokens; a miscased heading or a reflowed
  note line fails the gate (`…/R41C1Extra/red-cases-detail.json` cases `note-miscases-heading`,
  `round_40_note_only`, `note-omits-r40-record`, `presence_only`).
- Every FILL token is a number that exists only after the freeze runs; the fill ledger
  `artifacts/R41C1EntryDraft/fill-ledger.tsv` names the artifact each one comes from.
- If R41-C1 lands as an honest stop instead, this section must NOT be added; append a
  `## Round-41 measured, not promoted (R41-C1 honest stop)` block instead and keep the counter's
  `province_core_section` binding red (exit 1, never `met`).
