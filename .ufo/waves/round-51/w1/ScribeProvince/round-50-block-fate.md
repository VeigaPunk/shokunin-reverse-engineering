# R51-C1 — the fate of the round-50 `measured, not promoted` block

**Answer: it stays, as history, with a dated pointer to the round-51 section.** Nothing is
deleted and the round-50 measurement record is not rewritten. This is the lane's own precedent,
applied twice in this file:

- **Round 41** (`042b8769`): the block `## Round-40 measured, not promoted (R40-C1 honest stop)`
  was left in place verbatim, and the round-41 landing added its own section *below* it plus
  the paragraph "The row above supersedes the status of the block below for the genuine AVM layout
  only: the layout was correctly measured in round 40, and the block's own status line was a
  counter false negative." The round-40 heading was not renamed.
- **Round 49** (`3847f393`): the block `## Round-44 measured, not promoted (R44-C1 honest stop)`
  was left in place verbatim, and the round-49 frontier note says "This note supersedes the
  SquashFS v1/v2 status of the `## Round-44 measured, not promoted (R44-C1 honest stop)` section
  and of the round-44 frontier note above (`measured, not promoted`)".

So the round-51 landing mirrors that: the round-50 block stays, and the supersession is carried by
(a) a paragraph inside the new `## Round-51 additions to Core` section and (b) the round-51 frontier
note. Both are in `province-r51-section.md`.

## Why the block cannot simply be deleted or renamed

1. **It is the round-50 receipt's own subject.** The committed miss receipt
   `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` reports `carriers_matched 2`, `target 4`,
   `met_target false`, `exit_code 1`, `failing ["g7581:gaps_ok", "g7581:projection_ok",
   "g7582:gaps_ok"]`. The PROVINCE block is where that decision is stated in prose. Deleting it
   would remove the record of a decided miss.
2. **Its two Core-promotion bindings were false.** The same receipt reports
   `province_core_section false` and `province_core_row false` — the round-50 landing wrote a
   *measured-not-promoted* block instead of a `## Round-50 additions to Core` section, so the
   round-50 counter's own documentation bindings correctly reported "nothing was promoted". The
   round-51 draft must not inherit that shape: it adds a real `## Round-51 additions to Core`
   section with the LE-members row (verified: `province_core_section true`,
   `province_core_row true`, `frontier_note true`, exit 0 — see `receipts.md` R3).
3. **The miss was a rule defect, not a carrier defect.** REA published every frozen-oracle regular
   file on all four carriers; only the frozen rule's `removed.silent.char-device: ["247:0"]`
   generalisation failed. The round-50 block is the record of *that* defect, and it stays accurate
   as long as its forward-looking clause ("the repair … waits for a new freeze") is marked
   discharged.

## The three in-place edits (E7, E8, E9 in `frontier-note-edits.md`)

The block is **not** edited to change its status — it is edited only so that no sentence in it is
*false* after the round-51 freeze:

- **E7 — the status paragraph (`PROVINCE.md:442`).** Its closing clause "the repair (a re-frozen
  rule that states the device-accounting law per carrier class) waits for a new freeze" is
  forward-looking and becomes false at the round-51 freeze. A dated bracket
  (`[2026-10-30: that repair landed — …]`) marks it discharged and points at the new section.
  Every measurement clause in the paragraph is unchanged.
- **E8 — the table row (`PROVINCE.md:446`).** The row's parenthetical "nothing was promoted"
  describes the round-50 landing and stays true of it, but a reader scanning for the current
  status of LE AVM members would find it without a date. A dated bracket scopes it to round 50
  and names the round-51 successor.
- **E9 — the round-50 frontier note (`PROVINCE.md:448`).** "Still Frontier: LE AVM members
  (`hsqs`)" is the most recent statement of the LE-members status and would be false after the
  promotion. A dated bracket supersedes **only that clause**; the other clauses of the list (the
  ~13k-file rootfs under REA's 120 s limit, AVM kernels, nested sub-images below depth 1) stand
  and are carried forward verbatim by the round-51 note.

This is exactly the shape the lane used in `b98fd2d0` (round-50 falsify corrections), which
appended a dated bracket to this same status paragraph to correct an overstatement.

**Do not** touch the block's heading (`## Round-50 measured, not promoted (R50-C1 honest stop)`),
the round-50 table's other cells, the `Round-50 frontier note` marker, or the round-50 stem
`2026-10-28-r50-avm-le-squashfs-core`: the round-50 counter's own `frontier_note` binding searches
for the marker and the stem **on a single line**, and removing either would break that counter's
frozen binding for no gain.

## What the round-51 note supersedes, exactly

The round-51 frontier note names eight prior sources of the LE-members clause and nothing else:

1. the round-40 frontier note's Still-Frontier list (`LE AVM members (\`hsqs\`)`),
2. the round-41 prose block's closing sentence ("LE AVM members (`hsqs`) … stay Frontier"),
3. the round-41 frontier note's Still-Frontier list,
4. the round-42 frontier note's Still-Frontier list ("LE AVM members" — no backticks in that one),
5. the round-44 frontier note's Still-Frontier list,
6. the round-49 frontier note's Still-Frontier list,
7. the round-50 frontier note's Still-Frontier list,
8. the round-50 block's LE-members clause (the paragraph and the table row — items E7 and E8).

The round-50 note names its own scope as "the LE-AVM clause of the round-40/41/42/44/49 notes'
Still-Frontier lists"; the round-51 note adds the round-50 note and the round-50 block to that
enumeration, because the round-50 note is the most recent statement of the LE-members status.

**Not superseded by the round-51 note:** the `- **sasquatch** — …` bullet
(`PROVINCE.md:156-157`). Its LE clause was superseded in round 36 and its big-endian AVM clause in
round 41; the round-50 note does not name it. See E10 in `frontier-note-edits.md`.

Every other clause of every one of those lists is unchanged and restated in the round-51 note, so
no residual is silently dropped.
