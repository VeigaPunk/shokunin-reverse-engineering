# What the round-42 C1 entry supersedes, and how (dated pointers, no edits)

Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`. Line numbers below are base line numbers; every quote
was read from the base blob with `git show <base>:<path>`, not from the working tree.

Mechanism, identical to rounds 36-41: **no old text is edited**. The new entry, the PROVINCE frontier
note and the README `## Frontier` line carry a dated pointer that names the old text, quotes the phrase
it supersedes, and says what still stands. A reader who finds the old sentence finds the pointer from the
Frontier line and from the entry; a reader who finds the new row sees which old status it replaces.

## 1. Superseded as a *status*: the format-matrix "coverage claim only" row

| where | text at the base | superseded for | what still stands |
|---|---|---|---|
| `corpus/README.md:92` (coverage map, row `2026-10-26-unblob-format-matrix`) | "held as producer coverage statement — unblob.org lists 97 handler sections including `SquashFS (v4-BE)` and the vendor-mangled SquashFS variants; … **coverage claim only, never an extraction outcome**; …" | the SquashFS v3 handlers measured in round 42 (and only those) | everything else in the cell: the 97 sections, the v4-BE section, the "more than 30" vs "78+" count conflict, the assimilated provenance |
| `corpus/knowledge/2026-10-26-unblob-format-matrix.md:38` (Caveats) | "**A support matrix claims coverage, never an outcome**: "Fully supported" says nothing about whether a given image extracts." | nothing about that document's own subject — the sentence is about the vendor site's matrix and remains true | the sentence; the lane's v3 status is a different object, and the new entry is what changes it |

The pointer text is in `province-round42-additions.md` (the `Round-42 frontier note` line) and in
`readme-r42-rows.md` EDIT 3. The README row at :92 keeps its bytes; the round-42 coverage-map row is
inserted *after* it (base line 99), so a reader scrolls from the old status into the new row.

Why this is a supersession and not a contradiction: the old cell describes what the producer's matrix
claims. Round 42 adds a lane *outcome* on third-party v3 bytes. The two are different objects; the cell's
phrase "never an extraction outcome" was accurate for the lane's state at round 38 and is now history for
the handlers listed in the new row.

## 2. Partially superseded: the round-36 "vendor-mangled images" frontier sentence

| where | text at the base | superseded for | what still stands |
|---|---|---|---|
| `corpus/README.md:254` (the round-36 `sasquatch` dated note) | "Still frontier: big-endian/AVM (`sasquatch-v4be`) and **vendor-mangled images**." | the v3 vendor/format magics (`squashfs_v3_ddwrt` `tqsh`, `squashfs_v3_broadcom` `qshs`, `squashfs_v3_nonstandard` `sqlz`) **only if** one of the four frozen carriers carries that magic; the entry's handler matrix is a source reading, not a per-variant measurement | "vendor-mangled" for v4 Broadcom, AVM kernels, LE AVM `hsqs`, and every variant no frozen carrier carries |

The round-42 README frontier line is keyed on `sasquatch` (not `sasquatch-v4be`) precisely because this
surface is the plain binary's `-le`/`-be` leg, and it does not repeat or re-supersede the v4 chain
(:254-258).

## 3. Named, deliberately NOT superseded: the triage v3 table's legacy-chunk cause

| where | text at the base | round-42 disposition |
|---|---|---|
| `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:22-24` | "a chunk whose only SquashFS handler is v1-v3 therefore matches no row and is `unclassified` here, where the precedence's step 2 says `no-squashfs-chunk` — a disclosed divergence the generator never produces" | unchanged. C1 adds an extraction outcome; it labels no envelope, so it cannot supersede a label-precedence cell (Separability: C1 does not read SKILL.md, C2 does not read C1's data) |
| `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:108-110` | "Clause 2 labels an image whose only SquashFS chunk is v1-v3 `no-squashfs-chunk`; the name is the precedence text's, the cause cell says what happened." | unchanged, same reason |

The document that could replace that cell is R42-C2's `SKILL.md` rule block 21
(`<!-- sqfs-triage-table v4 -->`) plus `corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md`, and its
supersession sentence belongs in **that** entry and in block 20's supersession line, not here. The
round-42 PROVINCE note names the cell and says it is not superseded, so a reader cannot mistake the v3
coverage row for a relabelling.

Related but not corpus text: `plans/round-42-claims.md` § R42-C1 says "no REA run on a v3 chunk is in
the corpus". That is a pre-round description of `corpus/evidence/`; the round-42 receipts are what make it
false, and the claims file records it in its own freeze commit (`## Changes from the draft` / the frozen
R42-C1 text). No corpus file is edited for it.

## 4. Not superseded at all

- `2026-10-26-r39-be-squashfs-v4-core`, `2026-10-26-r41-avm-be-squashfs-core` and their PROVINCE rows:
  they concern SquashFS v4, a different handler family, extractor binary and argv branch.
- `2026-10-26-r36-sasquatch-squashfs-recursion`: LE v4; untouched.
- The round-41 triage v2/v3 entries' label semantics: untouched by C1.
