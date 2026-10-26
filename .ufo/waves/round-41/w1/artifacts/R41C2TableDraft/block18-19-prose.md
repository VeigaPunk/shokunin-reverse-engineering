# Block 18 and block 19 prose — the two supersession sentences (draft)

Seat `R41C2TableDraft`. Two edits for the L1 to paste into `SKILL.md`. The first repairs R40-CL5 L1
(block 18's verb) and round-40 axis-fit F7 (its scope word); the second is the one supersession
sentence block 19 gains.

## 1. Block 18 (v1 table, round 39) — replace the last sentence of its bullet

Current text (backticked span is what changes):

> Rows are tried top to bottom; the first match wins, no match is `unclassified`
> (interpreter `tools/round-39/sqfs-triage.py`). **Superseded for routing by rule block 19 (table v2,
> round 40); this v1 table stays as the round-39 record and mislabels mixed-link images, partial
> failures, empty trees and non-firmware envelopes** (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:27-36`).

Replacement sentence:

> Superseded for routing **and for the action column** by rule block 19 (table v2, round 40), itself
> superseded by block 20 (table v3, round 41); this v1 table stays as the round-39 record and mislabels
> mixed-link images and non-firmware envelopes, **cannot label** partial failures or empty trees, and
> wraps `-be` unconditionally on its AVM-marker row without the layout check every later table carries
> (`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:27-36`, `corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:57-72`).

Why each clause is there, measured:

- **"mislabels" kept for two, "cannot label" for the other two.** The frozen round-40 v1 interpreter on
  the 26 round-40 held-out envelopes returns 18/26: mixed-symlinks → `escaping-symlink-removed` and
  out-of-domain → `no-squashfs-chunk` are *wrong labels*; partial-body-failure and clean-empty →
  `unclassified` are *no label at all*. Round-40's sentence used "mislabels" for all four
  (`w2/R40W2C2TableReview.md` L1; the v2 entry's own "Three outcomes v1 could not label",
  `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:27-36`, says it correctly).
- **"and for the action column".** Block 18 still carries per-row procedures (`install the
  sasquatch-v4be 4.5.1 binary on that PATH`, `rerun through a PATH wrapper`). A reader told only that
  routing is superseded may still take an action from it; the one that is now wrong is exactly the AVM
  wrapper, which v2 narrowed and v3 moved into the pre-check
  (`w2/R40W2C2AxisFit.md` F7).
- **the AVM clause.** v1's avm row wraps unconditionally ("do not treat it as damage"); no later table
  does, so the list of v1 defects was incomplete without it (F7's second half).

## 2. Block 19 (v2 table, round 40) — one sentence to append

Append after "…with the limits in `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md:46-56`
(interpreter `tools/round-40/sqfs-triage-v2.py`).":

> Superseded for routing and for the action column by rule block 20 (table v3, round 41): v3 matches
> the failure, depth and mixed rows by containment, where this table's exact-set cells send a partial
> failure that also carries a link gap into `escaping-symlink-removed`; it adds the `depth-limited` row
> this table lacks, so all four round-40 C1 carriers were `unclassified`; and its layout pre-check
> replaces this bullet's claim that "the AVM-marker row covers a doctored marker on a standard-BE body
> only", which the row's own signature and cause contradict
> (`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:36-72`).

All three claims in that sentence are measured or code-backed, not asserted:

- A partial failure carrying a link gap: `H11` plus one injected `extractor-failure` gap is labelled
  `escaping-symlink-removed` / `expect-link-absent` under v2's exact-set cells
  (`w2/R40W2C2AxisFit.md` F6); under v3 it is `partial-body-failure` / `salvage-partial`
  (`artifacts/R41C2TableDraft/c-combined.tsv`, case "partial + mixed symlinks"), and the
  `+`-stripped control reproduces the v2 refusal (`ctl-exact-c-combined.tsv`).
- The four round-40 C1 carriers are `{depth-limited, unpublished-entry}` and v2 returns
  `unclassified` for that set (disclosed in the v2 entry's Limits); v3 returns
  `depth-limited-nested` / `raise-depth` for all four (`artifacts/R41C2TableDraft/b-c1-4.tsv`).
- The "only" is contradicted by the row it introduces: v2's `avm-marker-be-dropped` signature
  (`handler be`, `extractor-failure`, `deps none`, `BE=no`, `P=0`) is also produced by a damaged
  genuine AVM-layout body, and its own cause routes that branch to "keep it"
  (`w2/R40W2C2TableReview.md` M3); the round-40 marker-stripped measurement shows the mirror case
  under `BE=yes` (`w1/R40MistakeHunt.md` MH-6). v3's pre-check names all four layout × `-be`
  combinations once, above the table.

## 3. Not drafted here

The block-18 v1 **table rows** and the block-19 v2 **table rows** stay byte-identical: both are the
round's historical record and a rewrite would break the freeze-integrity rule that a later score must
see the frozen bytes. Only the two supersession sentences move.
