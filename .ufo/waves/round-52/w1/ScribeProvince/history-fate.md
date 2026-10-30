# Draft — the fate of the round-50 / round-51 LE-AVM records (R52-C1, PROVINCE side)

Three records are in scope. None of them is deleted, none of them is rewritten in place;
each gets a dated cross-reference from the round-52 landing.

---

## 1. `## Round-50 measured, not promoted (R50-C1 honest stop)` — KEEP, as history

`PROVINCE.md:440-448`. **Keep the block byte-identical**, including its status line, its
row and its `Round-50 frontier note` line. Reasons:

- It is the **committed before-state** of R52-C1: the claims file names its receipt
  (`.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`, `carriers_matched 2`, exit 1) as
  the "Before (measured, already committed)" of the claim. A round-52 rewrite of that block
  would erase the very measurement the claim is scored against.
- The lane's own precedent (the round-41 note) is that a later round **supersedes a status
  by reference** — "for the genuine AVM layout the block `## Round-40 measured, not promoted
  (R40-C1 honest stop)` above is superseded by `## Round-41 additions to Core` … its
  `measured, not promoted` status came from a counter suffix false negative (R40-CL1), not
  from the images" — and it leaves the old block in place.

**Recommended addition** (one dated line; it makes the round-52 supersession visible from
inside the old block, which the round-41 precedent does too). Insert it **after**
`PROVINCE.md:448` (the round-50 frontier note line) and **before** the new
`## Round-52 additions to Core` section:

```markdown
Round-52 note, 2026-10-30: the LE-AVM status of this block is superseded by `## Round-52 additions to Core` (`2026-10-30-r52-avm-le-squashfs-core`) — the same four chain-pinned carriers re-measured under the device-accounting law frozen at `tools/round-52/gap-rule.json`, `carriers_matched <PLACEHOLDER — L1: 4> of 4`. This block stays as the round-50 measurement record (2 of 4 under the frozen gap-accounting rule) and is not rewritten; its `Round-50 frontier note` line is history and is superseded only in its LE-AVM clause by the Round-52 frontier note.
```

If the L1 prefers to touch nothing inside the round-50 block, the same cross-reference
already exists in the new section's closing paragraph (drafted in
`province-r52-core-section.md`), and the two options are equivalent for the bindings. The
L1 should pick one, not both.

**What must NOT happen** to that block: no deletion; no retitling; no edit of `2 of 4`, of
`exit 1`, of the twelve undisposed device rows, of the receipt path, or of the
`Round-50 frontier note` line's own dated statement; no promotion language inside it.

---

## 2. The round-51 NOT-promoted entry pointer — KEEP, as history

The round-51 record is a **landed file**:

- `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` — title
  `# LE AVM accounting prerequisites — NOT promoted (round 51 honest stop)`; its status
  paragraph reads "**Status:** the filename was declared before the build wave; it is not a
  Core claim. R51-C1's four-carrier measurement was not completed. LE AVM members (`hsqs`)
  remain Frontier."; it cites S250/S251.
- `corpus/README.md:107` — coverage-map row: "SquashFS device and padding boundaries (round
  51) | `2026-10-30-r51-avm-le-squashfs-core` | source correction only, not promoted — …".
- `corpus/README.md:230` — knowledge index row: "`2026-10-30-r51-avm-le-squashfs-core` |
  source-grounded accounting prerequisites; filename is the declared slot, not Core promotion".
- `SCORECARD.md:3838` — the R51-C1 row: "**unverified** — no R51 data receipt or Core
  section; no promotion".

**Fate: keep all four byte-identical.** The round-51 statement was true when written and
remains a true record of round 51; the round-52 promotion does not make it false, and
rewriting it would delete the correction the round-52 entry rests on (the `-nopad` spelling,
the char/block-vs-fifo/socket mechanism distinction). The round-52 entry supersedes it **by
reference**, and the round-52 entry's text should say so in one sentence: that it supersedes
the round-51 entry's LE-AVM status while keeping the round-51 source corrections (S250/S251)
as its own citations.

### 2.1 Stem-collision hazard (concrete, must not happen)

The round-51 **wave draft** `.ufo/waves/round-51/w1/ScribeEntryC1/entry.md` was written for
the stem `2026-10-30-r51-avm-le-squashfs-core` — the **same stem** the L1 later used for the
landed "prerequisites — NOT promoted" file. Two consequences for round 52:

1. **The wave draft must never be landed.** Copying it to `corpus/knowledge/` would
   overwrite the landed round-51 entry with a different document under the same stem (and
   would import its own `<PLACEHOLDER>` set). It stays a wave artifact under
   `.ufo/waves/round-51/w1/ScribeEntryC1/`.
2. The round-52 entry is a **different stem**: `2026-10-30-r52-avm-le-squashfs-core`
   (`corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`). No collision with the landed
   round-51 file.

---

## 3. The conflict the L1 must resolve before the freeze (reported verbatim)

The claims text (`plans/round-52-claims.md`, sha256
`bce512c4867df91e8d3a93d203b67867e7a4f62e2fab1a80ee7c5c89eeca623a`) says, in the *Width*
paragraph of R52-C1:

> "**Width:** for the four measured LE AVM carriers, every char-device row of the independent
> census carries no extraction gap and no published path (28 of 28 rows); the generalisation to
> fifo/socket/block rests on the source ground and the corpus does not yet exercise it — no
> fifo, socket or block-device row exists in any measured carrier (F5 width statement,
> unchanged)."

The lane's **landed** round-51 entry (same file as above, S250 at tag 4.7.5) says:

> "FIFO (`:1328`) and socket (`:1349`) creation call `mknod` outside this root test. Thus the
> proposed explanation "an unprivileged extraction cannot mknod, so
> char-device/fifo/socket rows all disappear" is rejected. The source does not prove those two
> kinds disappear. The lane must distinguish the mechanisms and observe the operative extractor
> before assigning a disposition to an untested kind."

and the round-52 claims' own source row S252 is the kernel-side `mknod(2)` **CAP_MKNOD**
ground — a capability that gates **device files**, not FIFOs or sockets.

**Reading.** For char/block devices the mechanism is source-grounded (unsquashfs gates
`mknod` for `S_IFCHR`/`S_IFBLK` behind `if(root_process)`, and the kernel gates device files
behind CAP_MKNOD). For **fifo and socket** the mechanism is *not* the same and the source
does not support the "they disappear" generalisation; it is also not exercised by the corpus
(no such row exists on any of the four carriers — kinds present: `symlink`, `dir`,
`char-device`; receipt `census-kinds`).

**What the PROVINCE draft therefore does.** The drafted scope text states the law's measured
width as **char-device only (28 of 28)**, names the fifo/socket/block kinds as **not
exercised**, and explicitly warns the reader not to restate the fifo/socket generalisation as
source-grounded (the drafted `Round-52 frontier note` lists those kinds as still Frontier).
This keeps the landed text consistent with the lane's own round-51 correction.

**For the canonical judge.** Whether the r52 claims' *Width* sentence needs an amendment in
the freeze commit (it is the round-52 claims file, not a PROVINCE file) is **not mine to
decide** — it is the L1's amendment surface, and the claims file explicitly lists the
"## Wave-1 amendment record" for exactly this. Two amendment options, both honest:

- **A1 (recommended).** Amend the *Width* sentence to "the generalisation to **block-device**
  rests on the source ground (S250/S252); the fifo/socket part is **not** source-grounded per
  the round-51 correction and **not** exercised by the corpus", and keep the scope list
  unchanged.
- **A2.** Keep the claims sentence as written and let the round-52 entry's own text carry the
  narrowing (the entry's "the law's width" paragraph). This leaves the claims file and the
  lane's landed correction in visible tension; the entry's wording must then be explicit
  about which reading it takes.

I did not amend anything: `plans/round-52-claims.md` is the L1's file and the lane's
read-only rule forbids me from writing it.

---

## 4. SCORECARD (the L1's rows — I do not write `SCORECARD.md`)

Measured head, for the L1's coverage row (receipt `knowledge-file-count`, exit 0): the lane
holds **141** knowledge files today (`git ls-tree -r --name-only HEAD corpus/knowledge |
grep -c '\.md$'`), and the round-52 entry `2026-10-30-r52-avm-le-squashfs-core` would be the
map's **142nd** file. The claims require the coverage head to name **141/141 → 142/142**.

History that stays as history in `SCORECARD.md`:

- `SCORECARD.md:23` — the coverage head, last change round 51 ("Round-51 index integrity:
  141/141 knowledge files mapped; no Frontier→Core promotion"). The round-52 row updates the
  count and records the promotion; the round-51 sentence about the 141st file stays reachable
  in the round-51 section.
- `SCORECARD.md:3774-3815` — the round-50 section (the honest stop, `carriers_matched 2`).
- `SCORECARD.md:3838-3839` — the R51-C1 / R51-C2 rows ("unverified … no promotion").

The round-52 SCORECARD row must state, for C1: the before (the committed round-50 receipt,
2 of 4, exit 1), the after (the fresh counter score at the landing revision), and the
counting command (the claims' predicate command) — and, if the claim is missed, "honest stop,
no narrowing, no amendment", with the LE-AVM members staying Frontier and **no** Core row
landed.
