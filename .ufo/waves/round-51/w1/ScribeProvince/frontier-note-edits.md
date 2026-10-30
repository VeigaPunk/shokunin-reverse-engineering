# R51-C1 — PROVINCE.md frontier-note edits (patch style)

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Base revision: `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab` (the round-51 claims-draft commit)
Target file: `PROVINCE.md` (448 lines at base)
Seat: ScribeProvince (draft only — the L1 integrates; nothing here is landed by this seat)

**Precedent for the shape.** Every prior promotion in this file appends a dated
`## Round-NN additions to Core` section plus a dated `Round-NN frontier note, <date>: …`
paragraph, and leaves the *earlier* dated notes in place as history (see the round-41 landing
`042b8769`, the round-42 landing `eb8215ac` and the round-49 landing `3847f393`). The only
in-place edits the lane has made to an existing frontier note are **factual corrections** to the
round's own just-written text (round-50 falsify corrections, `b98fd2d0`). This draft therefore
follows the append-and-supersede shape, and edits in place only the two places where the
round-50 text would otherwise be **factually wrong** after the promotion.

## Decision summary

| # | Old line | Fate | Kind |
|---|---|---|---|
| E1 | `PROVINCE.md:394` (Round-40 frontier note) | unchanged — history; superseded by the round-51 note | supersession |
| E2 | `PROVINCE.md:402-406` (Round-41 prose block) | unchanged — history | supersession |
| E3 | `PROVINCE.md:408` (Round-41 frontier note) | unchanged — history | supersession |
| E4 | `PROVINCE.md:416` (Round-42 frontier note) | unchanged — history | supersession |
| E5 | `PROVINCE.md:430` (Round-44 frontier note) | unchanged — history | supersession |
| E6 | `PROVINCE.md:438` (Round-49 frontier note) | unchanged — history | supersession |
| E7 | `PROVINCE.md:442` (Round-50 status paragraph) | **in-place edit** — its closing clause would be false after the promotion | factual correction |
| E8 | `PROVINCE.md:446` (Round-50 table row) | **in-place edit** — the row's own status clause would be false | factual correction |
| E9 | `PROVINCE.md:448` (Round-50 frontier note) | **in-place edit** — the note's own LE-AVM clause would be false | factual correction |
| E10 | `PROVINCE.md:156-157` (`- **sasquatch** — …` bullet) | **no edit** — its LE clause was already superseded in round 36; see the note below | none |
| E11 | `PROVINCE.md:73-96` (`## Frontier` top-level bullet list) | unchanged — it holds no LE-AVM bullet | none |
| E12 | append at EOF | new `## Round-51 additions to Core` section + round-51 frontier note | append |

The `## Frontier` section proper (lines 73-96) lists PE subtypes, recorded crashes, alternate
providers, macOS-only surfaces and EVM bytecode — it carries **no** LE-AVM bullet, so nothing in
it loses the LE-members clause. The LE-AVM "still Frontier" membership lives entirely in the
**dated frontier notes** (E1, E3, E4, E5, E6, E9) plus the Round-41 prose block (E2); the
round-51 note supersedes exactly those clauses and nothing else.

---

## E7 — `PROVINCE.md:442` (Round-50 status paragraph)

**OLD (exact, one line):**

```
Recorded 2026-10-29 after scoring: the frozen counter `tools/round-50/c1-counter.py` at the attempt-2 landing matched **2 of 4** carriers (exit 1). REA 6.5.0 `extract-firmware --max-depth 1` (unblob 26.6.4, `sasquatch` 4.5.1 on the child PATH) published every frozen-oracle regular file on all four carriers; the counter's REA rerun reproduced the projection on three carriers and failed on `g7581` (extractor-tree `ENOENT` on a `usr/www.myfritz` symlink), whose projection stays unverified — the miss does not depend on it: `gaps_ok` is computed from the committed receipt against the frozen oracle, and `gaps_ok` is false on `g7581`/`g7582`, whose oracle tables carry 13 `char-device` entries each against the Cable carriers' 1, while the frozen rule (`required char-device`, one silent allowance `247:0`) has no disposition for the other twelve (the `dev/*` gaps that do exist on those carriers are `symlink` paths, not char-device paths). The row below is a measurement record, not a Core promotion; the repair (a re-frozen rule that states the device-accounting law per carrier class) waits for a new freeze.
```

**NEW (exact, one line):**

```
Recorded 2026-10-29 after scoring: the frozen counter `tools/round-50/c1-counter.py` at the attempt-2 landing matched **2 of 4** carriers (exit 1). REA 6.5.0 `extract-firmware --max-depth 1` (unblob 26.6.4, `sasquatch` 4.5.1 on the child PATH) published every frozen-oracle regular file on all four carriers; the counter's REA rerun reproduced the projection on three carriers and failed on `g7581` (extractor-tree `ENOENT` on a `usr/www.myfritz` symlink), whose projection stays unverified — the miss does not depend on it: `gaps_ok` is computed from the committed receipt against the frozen oracle, and `gaps_ok` is false on `g7581`/`g7582`, whose oracle tables carry 13 `char-device` entries each against the Cable carriers' 1, while the frozen rule (`required char-device`, one silent allowance `247:0`) has no disposition for the other twelve (the `dev/*` gaps that do exist on those carriers are `symlink` paths, not char-device paths). The row below is a measurement record, not a Core promotion; the repair (a re-frozen rule that states the device-accounting law per carrier class) waits for a new freeze. [2026-10-30: that repair landed — the round-51 freeze re-derives the rule from the device-accounting law per carrier class and promotes LE AVM members (`hsqs`); see `## Round-51 additions to Core` below. This paragraph stays as the round-50 record.]
```

**Why in place:** the sentence "the repair … waits for a new freeze" is a forward-looking claim
about the lane's own state. After the round-51 freeze it is false. A dated bracket keeps the
round-50 measurement intact (every clause before the bracket is unchanged) and marks the one
forward-looking clause as discharged. This is the same shape as the round-50 falsify correction
(`b98fd2d0`), which appended a dated bracket to this same paragraph.

## E8 — `PROVINCE.md:446` (Round-50 table row)

**OLD (exact; only the tail after `carriers_matched 2 of 4` differs):**

```
… counter `tools/round-50/c1-counter.py` at the freeze `435d41fd` — carriers_matched 2 of 4, `frozen_path_changed []`, citation and map bindings true with the two Core-promotion bindings false (`province_core_section`, `province_core_row` — nothing was promoted), receipt `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`
```

**NEW (exact tail):**

```
… counter `tools/round-50/c1-counter.py` at the freeze `435d41fd` — carriers_matched 2 of 4, `frozen_path_changed []`, citation and map bindings true with the two Core-promotion bindings false (`province_core_section`, `province_core_row` — nothing was promoted), receipt `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`; [2026-10-30: superseded for the LE AVM members by `## Round-51 additions to Core` below — the round-50 miss was a rule-generalisation defect (one Cable-carrier detail generalised to the class), not a carrier defect; this row stays as the round-50 measurement record]
```

**Why in place:** the row's parenthetical "nothing was promoted" describes the round-50 landing,
and stays true of it — but a reader scanning the file for the current status of LE AVM members
would find "nothing was promoted" in a row about exactly that surface, with no date. The dated
bracket removes the ambiguity without touching the round-50 measurement.

## E9 — `PROVINCE.md:448` (Round-50 frontier note)

**OLD (exact, one line):**

```
Round-50 frontier note, 2026-10-29: the LE-AVM clause of the round-40/41/42/44/49 notes' Still-Frontier lists is unchanged by this round — `LE AVM members (hsqs)` stays Frontier after the measured attempt (`2026-10-28-r50-avm-le-squashfs-core`; 2/4 under the frozen gap-accounting rule). Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed), AVM kernels, nested sub-images below depth 1.
```

**NEW (exact, one line):**

```
Round-50 frontier note, 2026-10-29: the LE-AVM clause of the round-40/41/42/44/49 notes' Still-Frontier lists is unchanged by this round — `LE AVM members (hsqs)` stays Frontier after the measured attempt (`2026-10-28-r50-avm-le-squashfs-core`; 2/4 under the frozen gap-accounting rule). Still Frontier: LE AVM members (`hsqs`), LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590, observed), AVM kernels, nested sub-images below depth 1. [2026-10-30: superseded for LE AVM members (`hsqs`) by the round-51 frontier note below; the remaining clauses of this list stand.]
```

**Why in place:** "Still Frontier: LE AVM members (`hsqs`)" is the most recent statement of the
LE-members status and would be false after the promotion. The dated bracket confines the
supersession to the LE-members clause; every other clause of the list (the ~13k-file rootfs under
the 120 s limit, AVM kernels, nested sub-images below depth 1) is untouched and is carried forward
verbatim by the round-51 note.

**Binding caution (measured, not assumed):** the round-50 counter's `frontier_note` binding
searches **one line at a time** for `FRONTIER_MARK`, the stem and an LE-AVM token
(`LE_AVM_RE` on the line with the stem removed). It does **not** care which frontier note the line
belongs to. Two consequences for the L1:

1. The round-51 frontier note must be a **single physical line** containing `Round-51 frontier
   note`, the stem `2026-10-30-r51-avm-le-squashfs-core` and, *outside* the stem, the token
   `LE AVM` (or `AVM LE`). The draft in `province-r51-section.md` is written as one line for this
   reason.
2. The round-50 note keeps its `Round-50 frontier note` marker and the round-50 stem, so the
   round-50 counter run against the round-51 tree would still see its own binding satisfied; the
   round-51 counter keys on `Round-51 frontier note` and the round-51 stem. **Do not** edit the
   round-50 note's marker or stem out of the file.

## E10 — `PROVINCE.md:156-157` (`- **sasquatch** — …` bullet) — **no edit**

**OLD (exact, line 157), kept unchanged:**

```
  covers the carved-image path today. [2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to Core`; big-endian/AVM stays here. Round 38: standard BE v4 measured through `sasquatch-v4be` (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`), not promoted — R38-C1 honest stop, K2's in-tree symlink leaves an `unpublished-entry` gap. Round 39: standard BE v4 is Core — see `## Round-39 additions to Core` (`2026-10-26-r39-be-squashfs-v4-core`); AVM-BE and vendor-mangled stay here.]
```

**No edit, and the reason is precise.** The bullet's LE clause was superseded in **round 36**
("superseded for LE SquashFS v4 — see `## Round-36 additions to Core`"), and the LE AVM members
*are* little-endian SquashFS v4 (`hsqs`, v4.0 xz). Its closing clause "AVM-BE and vendor-mangled
stay here" is the **big-endian** AVM clause, which the round-41 note already superseded for the
genuine AVM layout ("this note also supersedes the AVM sentence of the round-39 note"). The
round-50 note, which is the most recent authority on the LE-members clause, enumerates its scope
as "the LE-AVM clause of the round-40/41/42/44/49 notes' Still-Frontier lists" and does **not**
name this bullet.

An earlier draft of this document proposed a dated addition here naming the round-51 promotion.
That was **withdrawn**: it would claim a supersession that the round-36 and round-41 notes had
already made, and it would put a round-51 marker inside a bullet whose LE clause was never the
thing that kept LE AVM members in Frontier. The LE-members clause that actually needed superseding
lives in the dated notes (E1, E3, E4, E5, E6, E9) and in the round-41 prose block (E2) — and the
round-51 note names all of them.

**If the L1 prefers belt-and-braces** (a reader scanning only `### Round-4 frontier (post-unlock)`
might not see the promotion), the optional addition is:

```
… AVM-BE and vendor-mangled stay here. Round 51: LE AVM members (`hsqs`) are Core — see `## Round-51 additions to Core` (`2026-10-30-r51-avm-le-squashfs-core`); AVM-BE, AVM kernels, nested sub-images below depth 1 and the other vendor-mangled images stay here.]
```

This is **optional, not required**, and it is recorded here so the L1 can decide; the
recommendation is to leave line 157 untouched.

---

## E12 — append at EOF (`PROVINCE.md:449` onwards)

The new section text is in **`province-r51-section.md`** (same directory). It is the drop-in
`## Round-51 additions to Core` section: the Core row (four columns, matching the round-39/41/42/49
shape), the device-accounting law paragraph, the per-class census table, the supersession
paragraph for the round-50 block, the honest-scope paragraph, and the single-line
`Round-51 frontier note, 2026-10-30: …` paragraph.

Placeholders the L1 fills at landing (all receipt-dependent):

| Placeholder | Filled from |
|---|---|
| `<<FREEZE_COMMIT>>` | the round-51 freeze commit sha |
| `<<R51_SOURCE_ROWS>>` | the round-51 SOURCES row ids the entry cites |
| `<<ID>>` | the four carrier ids (g7581, g7582, c6490, c6430) — already spelled out inline |
| `<<.ufo/waves/round-51/l1/scores/c1-after.json>>` | the after-receipt path |
| `carriers_matched <<4>>` / `exit <<0>>` | the after-receipt's measured fields |
| `gaps_ok` true on every carrier | the after-receipt's per-carrier clauses |

**Do not** fill the receipt-dependent cells before the L1's data run; a Core row asserting
`carriers_matched 4` before it is measured is exactly the round-50 defect class.

## Binding self-check (offline, run in this seat's scratch)

`binding-selfcheck.py` ports the round-50 counter's three documentation-binding predicates
(`tools/round-50/c1-counter.py:2443-2492`) with the round-51 constants named in
`plans/round-51-claims.md` and runs them against the candidate section text. Result on the draft:
`province_core_section true`, `province_core_row true`, `frontier_note true`, exit 0.

Six mutants were run to show the check discriminates (all red except the noted one):

| Mutant | Expected | Measured |
|---|---|---|
| M1 Core heading renamed to "measured, not promoted" | red | `province_core_section false`, `province_core_row false`, exit 1 |
| M2 row cell names `squashfs_v4_be` | red | `province_core_row false`, exit 1 |
| M3 "AVM-marker" dropped from the row's first cell | red | **green — see caveat below** |
| M4 row cites the round-50 entry | red | `province_core_row false`, exit 1 |
| M5 frontier note removed | red | `frontier_note false`, exit 1 |
| M6 frontier note without an LE token | red | `frontier_note false`, exit 1 |

**Caveat on M3 (finding for the L1, not a defect in the draft):** the counter's
`province_core_row` predicate requires the *row* to match `AVM_MARKER_RE` — it searches the whole
row string with the entry path removed, not only the first cell. The draft's row mentions
"AVM-marker" in the first cell **and** the census row above it is not part of the matched row,
but the phrase `AVM marker` also occurs elsewhere in the drafted table row's own text
(`the AVM marker test exists only in the BE branch, :48`), so M3 stayed green. The draft is
nonetheless stricter than the check: the first cell itself names `AVM-marker`, so the row satisfies
the predicate by its first cell alone. **Recommendation to the L1:** in the round-51 counter, bind
the AVM-marker to the **first cell** (as `HANDLER_RE` already is) rather than to the whole row, so
a row cannot satisfy the marker clause by an incidental mention elsewhere in the row. This is a
round-51 counter change, not a PROVINCE.md change.
