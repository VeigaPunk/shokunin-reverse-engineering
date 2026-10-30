# Draft — the exact Frontier-note line edits for round 52 (R52-C1)

`PROVINCE.md` sha256 before these edits: `b0cb62abd63df687451e0f73d2e71684a20e2933b47dfd4f84e92edec79872a8`
(448 lines). The seven LE-AVM lines below are the **only** places in `PROVINCE.md` that carry
an "LE AVM members" Frontier clause (grep `LE AVM members` → lines 394, 405, 408, 416, 430,
438, 448; receipt `province-le-avm-lines`). The `## Frontier` bullet list itself (lines
73–127) carries **no** LE-AVM clause — the clause lives only in the dated round notes and in
the round-41 section's status paragraph. There is therefore **no** top-level Frontier bullet
to delete; the work is on the dated notes.

Every old line is quoted verbatim (from the `:raw` read of the file at the sha above).

---

## Variant 1 — RECOMMENDED: append-only dated supersession (the lane's house style)

**Do not touch lines 394, 405, 408, 416, 430, 438, 448.** Land the new section
(`province-r52-core-section.md`, Branch A) and let its single `Round-52 frontier note` line
carry the supersession, in the same style as the round-41, round-42 and round-49 notes
("This note supersedes the … clause of the round-N frontier note, and nothing else").

Why this is the recommendation, not a stylistic preference: those seven lines are **dated
history** of rounds 40–50. The round-49 note establishes the precedent explicitly —
"This note supersedes the SquashFS v1/v2 status of the `## Round-44 measured, not promoted`
section and of the round-44 frontier note above …, and nothing else" — i.e. the lane
supersedes **by reference from a newer dated note**, never by rewriting an older dated note.
Rewriting line 394 (dated 2026-10-26) in 2026-10-30 would leave a round-40 note that no
longer says what round 40 concluded.

The single line to land (it satisfies the counter's `frontier_note` binding: the line carries
the mark `Round-52 frontier note`, the stem `2026-10-30-r52-avm-le-squashfs-core`, and an
independent LE-AVM token `LE AVM` outside the stem):

```markdown
Round-52 frontier note, 2026-10-30: LE AVM members (`hsqs`) moved Frontier → Core with `2026-10-30-r52-avm-le-squashfs-core` (four chain-pinned FRITZ!OS members re-measured under the device-accounting law frozen at `tools/round-52/gap-rule.json`; `carriers_matched <PLACEHOLDER — L1: 4> of 4`). This note supersedes the LE-AVM clause of the round-40, round-41, round-42, round-44, round-49 and round-50 frontier notes and of the round-41 section's status paragraph, and nothing else. Still Frontier: AVM kernel images, nested sub-images below depth 1, LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed), and the fifo, socket and block-device kinds of the device-accounting law, which the corpus does not exercise.
```

Placement: inside the new `## Round-52 additions to Core` section, after the scope
paragraphs, as the section's last line (so the section ends at the next `## ` heading).

---

## Variant 2 — only if the L1 chooses in-place clause removal

**Not recommended** (it rewrites dated history), but given here so the L1 can apply it
mechanically if it decides to. Each replacement below is the **old line with the LE-AVM
clause removed and a dated cross-reference added in its place**. Each is byte-exact against
the quoted old line except for the marked edit.

### 2.1 `PROVINCE.md:394` (round-40 frontier note)

Old (verbatim):

> Round-40 frontier note, 2026-10-26: AVM-BE is **measured, not promoted** — the genuine AVM layout extracted with every oracle file on two vendor members and two lane-built images (`2026-10-26-r40-avm-be-squashfs-core`), but R40-C1 stopped at 3/4 on a counter false negative, so the round-39 note's AVM sentence still stands until a re-frozen counter scores it. Still Frontier: AVM-BE bodies (this measurement included), LE AVM members (`hsqs`), nested `filesystem_core` images below depth 1, other vendor-mangled images.

Replacement (the clause `, LE AVM members (`hsqs`)` is dropped; a dated cross-reference is
appended at the end of the sentence — the note's AVM-BE half is untouched):

> Round-40 frontier note, 2026-10-26: AVM-BE is **measured, not promoted** — the genuine AVM layout extracted with every oracle file on two vendor members and two lane-built images (`2026-10-26-r40-avm-be-squashfs-core`), but R40-C1 stopped at 3/4 on a counter false negative, so the round-39 note's AVM sentence still stands until a re-frozen counter scores it. Still Frontier: AVM-BE bodies (this measurement included), nested `filesystem_core` images below depth 1, other vendor-mangled images. [2026-10-30: the LE AVM members clause of this note is superseded by the Round-52 frontier note — LE AVM members (`hsqs`) moved to Core.]

### 2.2 `PROVINCE.md:403-406` (the round-41 section's status paragraph — three lines)

Old (verbatim, lines 403–406):

> The row above supersedes the status of the block below for the genuine AVM layout only: the layout was
> correctly measured in round 40, and the block's own status line was a counter false negative. A standard
> big-endian body whose AVM marker was stripped stays governed by `## Round-39 additions to Core`, and
> LE AVM members (`hsqs`), AVM kernel images, nested sub-images below depth 1 and other vendor-mangled
> images stay Frontier.

Replacement (line 405's LE-AVM clause is dropped; the rest of the paragraph, including its
line breaks, is untouched):

> The row above supersedes the status of the block below for the genuine AVM layout only: the layout was
> correctly measured in round 40, and the block's own status line was a counter false negative. A standard
> big-endian body whose AVM marker was stripped stays governed by `## Round-39 additions to Core`, and
> AVM kernel images, nested sub-images below depth 1 and other vendor-mangled
> images stay Frontier. [2026-10-30: LE AVM members (`hsqs`) moved to Core — see the Round-52 frontier note.]

### 2.3 `PROVINCE.md:408` (round-41 frontier note)

Old (verbatim):

> Round-41 frontier note, 2026-10-26: for the genuine AVM layout the block `## Round-40 measured, not promoted (R40-C1 honest stop)` above is superseded by `## Round-41 additions to Core` (`2026-10-26-r41-avm-be-squashfs-core`); its `measured, not promoted` status came from a counter suffix false negative (R40-CL1), not from the images, and this note also supersedes the AVM sentence of the round-39 note. Still Frontier: LE AVM members (`hsqs`), AVM kernel images, nested `filesystem_core` images below depth 1, other vendor-mangled images.

Replacement:

> Round-41 frontier note, 2026-10-26: for the genuine AVM layout the block `## Round-40 measured, not promoted (R40-C1 honest stop)` above is superseded by `## Round-41 additions to Core` (`2026-10-26-r41-avm-be-squashfs-core`); its `measured, not promoted` status came from a counter suffix false negative (R40-CL1), not from the images, and this note also supersedes the AVM sentence of the round-39 note. Still Frontier: AVM kernel images, nested `filesystem_core` images below depth 1, other vendor-mangled images. [2026-10-30: the LE AVM members clause of this note is superseded by the Round-52 frontier note — LE AVM members (`hsqs`) moved to Core.]

### 2.4 `PROVINCE.md:416` (round-42 frontier note)

Old (verbatim):

> Round-42 frontier note, 2026-10-26: SquashFS v3 (`squashfs_v3`, `squashfs_v3_ddwrt`) moved Frontier → Core with `2026-10-26-r42-squashfs-v3-core`; the producer statement `2026-10-26-unblob-format-matrix` stays as written. Still Frontier: SquashFS v1/v2, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom, LE AVM members, AVM kernels, nested sub-images below depth 1.

Replacement (the clause `, LE AVM members` is dropped — note this line spells the clause
without backticks and without `hsqs`):

> Round-42 frontier note, 2026-10-26: SquashFS v3 (`squashfs_v3`, `squashfs_v3_ddwrt`) moved Frontier → Core with `2026-10-26-r42-squashfs-v3-core`; the producer statement `2026-10-26-unblob-format-matrix` stays as written. Still Frontier: SquashFS v1/v2, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom, AVM kernels, nested sub-images below depth 1. [2026-10-30: the LE AVM members clause of this note is superseded by the Round-52 frontier note — LE AVM members (`hsqs`) moved to Core.]

### 2.5 `PROVINCE.md:430` (round-44 frontier note)

Old (verbatim):

> Round-44 frontier note, 2026-10-28: SquashFS v1/v2 were measured on four standard fixtures (`squashfs_v1`, `squashfs_v2`; counter 4/4), but R44-C1 is not promoted: the frozen claim's output-directory clause disagreed with the counter's `/kaidoku-r44/` provenance binding. SquashFS v1/v2 remain Frontier pending a new pre-data freeze that aligns the predicate and instrument. Still Frontier: `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom, LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1.

Replacement:

> Round-44 frontier note, 2026-10-28: SquashFS v1/v2 were measured on four standard fixtures (`squashfs_v1`, `squashfs_v2`; counter 4/4), but R44-C1 is not promoted: the frozen claim's output-directory clause disagreed with the counter's `/kaidoku-r44/` provenance binding. SquashFS v1/v2 remain Frontier pending a new pre-data freeze that aligns the predicate and instrument. Still Frontier: `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom, AVM kernels and nested sub-images below depth 1. [2026-10-30: the LE AVM members clause of this note is superseded by the Round-52 frontier note — LE AVM members (`hsqs`) moved to Core.]

### 2.6 `PROVINCE.md:438` (round-49 frontier note)

Old (verbatim):

> Round-49 frontier note, 2026-10-28: SquashFS v1/v2 moved Frontier → Core with `2026-10-28-r49-squashfs-v1v2-core` (`squashfs_v1` and `squashfs_v2`, both byte orders, rea-agents 6.5.0 `extract-firmware` on four committed unblob 26.6.4 fixtures, v1.0 and v2.0 only; second reader `/usr/bin/unsquashfs` 4.7.5 plus the unblob `__output__` expected trees). This note supersedes the SquashFS v1/v2 status of the `## Round-44 measured, not promoted (R44-C1 honest stop)` section and of the round-44 frontier note above (`measured, not promoted`), and the v1/v2 clause of the round-42 frontier note, and nothing else: `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3 bodies, v4 Broadcom, v2.1 images (the handler pattern admits `s_minor` 1; nothing measured), LE AVM members (`hsqs`), AVM kernels and nested sub-images below depth 1 stay Frontier.

Replacement:

> Round-49 frontier note, 2026-10-28: SquashFS v1/v2 moved Frontier → Core with `2026-10-28-r49-squashfs-v1v2-core` (`squashfs_v1` and `squashfs_v2`, both byte orders, rea-agents 6.5.0 `extract-firmware` on four committed unblob 26.6.4 fixtures, v1.0 and v2.0 only; second reader `/usr/bin/unsquashfs` 4.7.5 plus the unblob `__output__` expected trees). This note supersedes the SquashFS v1/v2 status of the `## Round-44 measured, not promoted (R44-C1 honest stop)` section and of the round-44 frontier note above (`measured, not promoted`), and the v1/v2 clause of the round-42 frontier note, and nothing else: `squashfs_v2_nonstandard` (`v2ns-*`; no independent reader), `squashfs_v3_broadcom`, `squashfs_v3_nonstandard` (and the DD-WRT no-pad/4k-pad v3 images), gzip v3 bodies, v4 Broadcom, v2.1 images (the handler pattern admits `s_minor` 1; nothing measured), AVM kernels and nested sub-images below depth 1 stay Frontier. [2026-10-30: the LE AVM members clause of this note is superseded by the Round-52 frontier note — LE AVM members (`hsqs`) moved to Core.]

### 2.7 `PROVINCE.md:448` (round-50 frontier note — the round-50 section's own note)

Old (verbatim):

> Round-50 frontier note, 2026-10-29: the LE-AVM clause of the round-40/41/42/44/49 notes' Still-Frontier lists is unchanged by this round — `LE AVM members (hsqs)` stays Frontier after the measured attempt (`2026-10-28-r50-avm-le-squashfs-core`; 2/4 under the frozen gap-accounting rule). Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed), AVM kernels, nested sub-images below depth 1.

Replacement (this one is a **status** line, so the replacement states the new status rather
than only dropping a clause — but it still keeps the round-50 measurement in the sentence, as
a dated history):

> Round-50 frontier note, 2026-10-29: the LE-AVM clause of the round-40/41/42/44/49 notes' Still-Frontier lists is unchanged by **this** round — `LE AVM members (hsqs)` stayed Frontier after the measured attempt (`2026-10-28-r50-avm-le-squashfs-core`; 2/4 under the frozen gap-accounting rule). [2026-10-30: the LE AVM members clause of this note is superseded by the Round-52 frontier note — LE AVM members (`hsqs`) moved to Core.] Still Frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed), AVM kernels, nested sub-images below depth 1.

---

## Out of my seat's file scope, but the L1 must not miss it

`corpus/README.md:303` carries a **parallel** LE-AVM Frontier note with the same Still-Frontier
clause (sha256 `aad0c5907483f38fc0fcf82cb66f63d0b15a6554c3ad2d0d6d85c6a60b5da5db`, 303 lines):

> Round-50 frontier note, 2026-10-29: LE AVM members (`hsqs`) were measured on four chain-pinned vendor carriers (`2026-10-28-r50-avm-le-squashfs-core`; REA published every oracle regular file on all four) and **stay Frontier** — R50-C1 measured 2 of 4 under the frozen gap-accounting rule (twelve `char-device` entries per FRITZ!Box carrier with no disposition; the rule was generalised from the Cable-carrier class). Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit, AVM kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom. This note adds the round-50 measurement to the LE-AVM clause of the round-49 note and supersedes nothing…

The README also needs its `## Coverage map` row for the new entry stem
`2026-10-30-r52-avm-le-squashfs-core` (the counter's `coverage_map_row` binding requires a
`|` line inside `## Coverage map` containing the stem) and its `## Knowledge` index row.
I do not own `corpus/README.md`; the L1 (or the README seat) must land those, and the same
Still-Frontier clause there needs the same dated supersession.
