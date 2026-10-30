# ScribeProvince — R51-C1 PROVINCE.md bindings (round 51, wave 1, attempt 1)

Seat: ScribeProvince (scribe, leaf member — no dispatch). Lane:
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.

## What I produced (all drafts, all under `.ufo/waves/round-51/w1/ScribeProvince/`)

| file | content |
|---|---|
| `province-r51-section.md` | the drop-in `## Round-51 additions to Core` section: Core row, device-accounting-law paragraph, per-class census table, round-50 supersession paragraph, honest-scope paragraph, and the single-line `Round-51 frontier note, 2026-10-30:` paragraph |
| `frontier-note-edits.md` | the patch-style edit list E1–E12: exact OLD lines quoted verbatim, exact NEW lines, and why each is edited, not edited, or superseded |
| `round-50-block-fate.md` | the fate of `## Round-50 measured, not promoted (R50-C1 honest stop)`: **stays as history**, with three dated-bracket in-place corrections (E7/E8/E9) and a dated pointer to the round-51 section |
| `receipts.md` | every command, exit code, stdout sha256, UTC time, and the explicit "not run" list |
| `census.txt`, `binding-selfcheck.py`, `binding-selfcheck.json` | the measured per-class census output, the offline binding harness, and its result |

## Verdict

**The three PROVINCE documentation bindings of the round-50 counter are satisfiable with the
drafted section, and I have measured that they are.** Running the round-50 counter's own three
documentation-binding predicates (ported offline with the round-51 constants from
`plans/round-51-claims.md`) against the drafted section: `province_core_section true`,
`province_core_row true`, `frontier_note true`, exit 0. Seven mutants show the check
discriminates: a renamed heading, the BE handler in the row's first cell, a row citing the
round-50 entry, a removed frontier note, a frontier note without an LE token, and a row with no
AVM-marker anywhere are all red (exit 1).

**This is not the claim.** `carriers_matched 4` is a placeholder: no REA run, no data run, no
fetch happened by this seat. The section asserts the promotion only in the future tense of its
placeholder cells, and the L1 must fill them from the after-receipt.

## The three most important findings

1. **The round-50 miss was a rule-generalisation defect, and the file already says so.** The
   frozen rule's `removed.silent.char-device: ["247:0"]` took one Cable-carrier detail
   (`dev/led` 247:0) as a class-wide whitelist. I re-derived the per-class census from the
   committed oracle tables (`tools/round-50/oracle/<id>.nonregular.tsv`, sha256 in `receipts.md`
   R1): Cable class `c6430`/`c6490` carry **1** char-device each; FRITZ!Box class `g7581`/`g7582`
   carry **13** each (`dev/led` 247:0; `dev/pts/0-7` 136:0-7; `dev/tiatm` 230:0; `dev/ttyp0-2`
   3:0-2). No fifo/socket/block-device row occurs in any of the four tables (kinds present:
   `symlink`, `dir`, `char-device` only). The per-carrier non-regular totals 824 / 914 / 1001 /
   1001 agree with the round-50 entry's Results table. The law-derived rule must key on the
   class's census, not on a detail whitelist — that is the input the rule-derivation seat needs.

2. **The round-50 counter's AVM-marker binding is weaker than its handler binding, and the
   round-51 counter should tighten it.** `province_core_row` requires the handler in the row's
   **first cell** (`HANDLER_RE` on `cells(r)[0]`) but the AVM-marker in the **whole row**
   (`AVM_MARKER_RE.search(r.replace(ENTRY, ''))`). Measured: a row whose first cell drops
   "AVM-marker" but whose second cell still says "the AVM marker test exists only in the BE
   branch" stays **green** (mutant M3); only a row with the phrase removed everywhere goes red
   (M7). The drafted row names `AVM-marker` in its first cell, so it satisfies the intended
   reading either way — but the round-51 counter should bind the marker to the first cell too.

3. **The frontier-note binding is line-based, so the round-51 note must be one physical line.**
   `frontier_note` searches **one line at a time** for `Round-51 frontier note`, the stem
   `2026-10-30-r51-avm-le-squashfs-core`, and an LE-AVM token **outside** the stem (the stem
   itself spells `avm-le` and would otherwise satisfy the token on its own — the counter strips
   it). The drafted note is written as a single line for exactly this reason. Corollary for the
   L1: do not strip the `Round-50 frontier note` marker or the round-50 stem out of the file —
   the round-50 counter's frozen binding keys on them.

## What the L1 should know about the shape of the landing

- **Precedent is append-and-supersede, not rewrite.** The round-41, round-42 and round-49
  landings each left the earlier `measured, not promoted` block verbatim and added a dated
  supersession from below; the only in-place edits the lane has made to an existing frontier note
  are factual corrections to the round's own just-written text (`b98fd2d0`). This draft follows
  that: E1–E6 (the round-40/41/42/44/49 notes and the round-41 prose block) are left untouched
  and superseded by name from the round-51 note; only E7/E8/E9 (the round-50 block's own three
  sentences that would become *false*) carry dated brackets.
- **Nothing in `## Frontier` proper (lines 73-96) loses the LE-members clause** — that list holds
  PE subtypes, recorded crashes, alternate providers, macOS-only surfaces and EVM bytecode, and
  no LE-AVM bullet. The LE-members clause lives entirely in the dated notes.
- **I withdrew my own first draft of E10.** I had proposed a dated addition to the
  `- **sasquatch** — …` bullet (lines 156-157). On re-reading the file, that bullet's LE clause
  was already superseded in round 36 ("superseded for LE SquashFS v4") and its big-endian AVM
  clause in round 41, and the round-50 note does not name it — so a round-51 marker there would
  claim a supersession that had already happened. E10 is now a **no-edit** with the reasoning
  recorded; an optional variant is quoted for the L1 to decide.
- **The honest scope is narrower than "LE AVM members".** The draft promotes the four pinned
  vendor members under the law-derived accounting rule, and says explicitly that the AVM marker
  (`mkfs_time == bytes_used`) is a constant of the pinned bytes (unblob 26.6.4 tests it only in
  its big-endian branch, S245 :48), not "REA recognises AVM". Still Frontier: the ~13k-file LE AVM
  rootfs under REA's 120 s limit, AVM kernels, nested sub-images below depth 1, the other
  vendor-mangled images, v4 Broadcom, `squashfs_v3_broadcom`/`_nonstandard`, gzip v3 bodies,
  `squashfs_v2_nonstandard`, v2.1 images.
- **Fill the placeholders only after the data run**: `<<FREEZE_COMMIT>>`, `<<R51_SOURCE_ROWS>>`,
  `<<.ufo/waves/round-51/l1/scores/c1-after.json>>`, `carriers_matched <<4>>`, `exit <<0>>`. A
  Core row asserting 4/4 before it is measured is the round-50 defect class. **The frontier-note
  paragraph's counts are placeholders too** — I set `carriers_matched <<4>>` and `exit <<0>>`
  there as well, so no landed sentence asserts a measured 4/4 unless the L1 fills it from the
  after-receipt. The binding is unaffected: `frontier_note` needs the mark, the stem and an
  LE-AVM token, not the counts (re-verified, exit 0, after the change).

## Out of scope for this seat (not done, by design)

- The round-51 counter, the law-derived `tools/round-51/gap-rule.json`, the controls, the fetcher
  and the triage v6 port belong to other seats. `binding-selfcheck.py` is an **offline port of the
  round-50 binding predicates** kept in this seat's directory as a cross-check for the L1; it is
  not a lane instrument, is not registered, and does not run REA.
- No REA invocation, no `--data-run`, no download, no mutation of the lane tree, the fleet repo,
  `.ufo/state/`, or any sibling lane. The only writes were this seat's directory and the scratch
  `/fast/scratch/hyaku/kaidoku-r51/w1-ScribeProvince` (removed after the copies above).
- `corpus/README.md`, `corpus/SOURCES.md`, the knowledge entry and the SCORECARD row are other
  seats' surfaces; the claims file's landing bindings list them separately.

## Honest limits of this draft

- The promotion text is **unmeasured**: every count that depends on the fresh run is a
  placeholder, and the draft says `carriers_matched 4` in the frontier note's parenthetical —
  the L1 must either keep that cell placeholder-honest in the landed note or land the note only
  after the data run reports 4/4. I flag this as the single largest risk in the draft.
- The binding self-check ports the round-50 counter's **three documentation** predicates only. It
  does not port the per-carrier clauses, the freeze-drift binding or the gap-rule evaluation, so
  it cannot and does not establish the claim.
- The census is a re-count of the **committed** oracle tables; it is not a fresh `unsquashfs`
  read of the carrier bytes, and the counter still re-derives those tables at scoring time.
