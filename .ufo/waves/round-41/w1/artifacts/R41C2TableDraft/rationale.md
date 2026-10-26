# R41-C2 table v3 — row-by-row rationale (draft, for the freeze)

Seat `R41C2TableDraft`, round 41 wave 1. Deliverables: `block20.md` (SKILL rule block 20),
`entry.md` (`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md`), `block18-19-prose.md` (the two
supersession sentences), this rationale, and the executables that prove the block parses and decides
(`v3-refparse.py`, `checks.py`, plus the `l2-wrapper-measurement.md` recon).

The table is **not** a new design. It is the numbered label precedence in
`plans/round-41-claims.md` § R41-C2 rendered into the v2 table grammar, one row per clause, with the
cells of each row carrying exactly the constraints that clause names.

## 1. Clause → row map, and why the composition is exact

| clause | row | label | condition cells as drafted | argument |
|---|---|---|---|---|
| 1 | — | `unclassified` | every row pins `extract_firmware` + `unblob`; no match is `(unclassified, none)` | clause 1 is the no-match default, not a row |
| 2 | 1 | `no-squashfs-chunk` | handler `none-v4` | "no `squashfs_v4_*` handler in H" — a v4-absence test, not an empty-H test |
| 3 | 2 | `dep-missing-be` | gap contains `missing-extractor-dependency`, deps contains `sasquatch-v4be` | first branch of clause 3 |
| 3 | 3 | `dep-missing-le` | same gap cell, deps contains `sasquatch` | second branch; row 2 above it makes "if D names sasquatch-v4be" win when both names are present |
| 4 | 4 | `partial-body-failure` | gap contains `extractor-failure`, files `>0` | "whatever other gaps or removed links accompany it" is containment |
| 5 | 5 | `avm-marker-be-dropped` | handler `squashfs_v4_be`, gap contains `extractor-failure`, `be no`, files `0` | clause 5's four conditions |
| 6 | 6 | `body-extractor-failure` | gap contains `extractor-failure`, files `0`, `be *` | clause 6 names no `-be` value, so the cell is `*`; row 5 above it takes the `be no` + BE-handler case |
| 7 | 7 | `depth-limited-nested` | gap contains `depth-limited` | "whatever symlink gaps accompany it" |
| 8 | 8 | `mixed-symlinks` | gap contains `unpublished-entry`, `sr yes` | clause 8 |
| 9 | 9 | `escaping-symlink-removed` | gap `none`, `sr yes` | clause 9's `G = ∅` is why this cell is `none` and not v2's `*` |
| 10 | 10 | `in-tree-symlink-metadata` | gap exact `unpublished-entry` | clause 10 is a set **equality**; the only exact-set row among the symlink rows |
| 11 | 11 | `clean` | gap `none`, files `>0` | clause 11 first half |
| 11 | 12 | `clean-empty` | gap `none`, files `0` | clause 11 second half |
| 12 | — | `unclassified` | no match | clause 12 is the default |

Two disciplines make the composition exact rather than approximate:

1. **Cells are never tighter than their clause.** Every feature a clause does not name is `*`
   (`be`, `sr`, `files` on the failure and dep rows; `sr` on the clean rows). A cell tighter than its
   clause would refuse an envelope the precedence labels — the failure direction that costs a score.
2. **Row order is clause order.** Clause numbers and row numbers are monotone (1:<2, 3:2-3, 4:4, 5:5,
   6:6, 7:7, 8:8, 9:9, 10:10, 11:11-12). Because every row is tried top to bottom and the first full
   match wins, the executable order is the precedence order. This is also the round-40 axis-fit finding
   that row order is load-bearing at two boundaries (AVM before body, mixed before escaping) made
   explicit: the table states the more-specific-above-more-general principle in its own bullet.

The one place the draft deliberately departs from v2's cells is the `handler` column of row 1: clause 2
says "no `squashfs_v4_*` handler", which an image whose only SquashFS chunk is v1-v3 satisfies. v2's
`none` (no squashfs handler at all) would return `unclassified` there, disagreeing with the precedence
text on an envelope a critic can build from JSON alone. Grammar delta D3 (`none-v4`) closes it and is
selftested (`none-v4 on v3 chunk`). If the L1 freezes the v2 handler grammar unchanged, row 1 must
revert to `none` **and** the entry's Limits must state the divergence for v1-v3 chunks — that is the
only place in this table where the executable form would then be narrower than the precedence.

## 2. Grammar deltas the v3 interpreter must implement

| id | delta | why it is needed | selftest |
|---|---|---|---|
| D1 | marker `<!-- sqfs-triage-table v3 -->`; a v1 or v2 marker in the section is exit 2 | the block must be distinguishable at the base and at v2 | `v2 marker only` |
| D2 | in `gap kinds` and `dependencies`, a single name with one trailing `+` is a **contains** test; every other non-`*` cell stays exact-set equality, `none` is the empty set, `a+b+` is malformed | clauses 4, 7 and 8 say "whatever else accompanies it"; clauses 3 and 10 say "names" and "equals". Both forms must coexist in one column | `contains on superset`, `exact refuses superset`, `exact singleton`, `dependency contains`, `two contains rejected` |
| D3 | handler cell `none-v4` = no handler matching `squashfs_v4_*` | clause 2's wording, and the v1-v3 chunk population | `none-v4 on empty H`, `none-v4 on v3 chunk`, `v4 chunk skips row 1` |

Everything else is frozen v2 grammar and is re-implemented verbatim in `v3-refparse.py`: the twelve
columns in order, the action vocabulary on the last non-blank line above the header (blank lines
tolerated, `R40C2ReconPartial.md` §7.2), first full match, unique labels, `unclassified` reserved for
the no-match pair, `cause` must contain `->` (the round-40 `R40C2Shortcuts.md` D1 trap — every drafted
cause cell contains one), non-empty `source`, malformed anything → exit 2. `none` stays a declared
vocabulary token because it is both the clean row's action and the no-match action: forcing it out
would invent a second word for "no action".

## 3. Row by row

`v2` = the frozen block 19 cells; `defect` = what the cell changes relative to it.

| # | label | action | v2 → v3 cell change | defect repaired | cause citation (in-cell) | residual |
|---|---|---|---|---|---|---|
| 1 | `no-squashfs-chunk` | `inspect-input` | handler `none` → `none-v4` | D3; clause 2 fidelity | S112 :102,:159,:245 (v1/v2/v3 handler names), :463,:522 (v4 magics), knowledge r39 entry :50-54 | label name says "no chunk" for a v1-v3 chunk; cause states it, entry Limits discloses |
| 2 | `dep-missing-be` | `install-extractor-be` | exact → contains (gap and deps); `be n/a` → `*`; source names REA | L3 (REA mints `missing-extractor-dependency`); clause 3 fidelity (`n/a` was narrower than the clause) | S112 :24,:68-69; S120 `report.py:118-122`, `command.py:70-72`; S119 `FirmwarePublication.js:161-186`, `firmwareAnalysis.js:85` | `D` redundant with `H` on every measured class (F4) — disclosed in Limits |
| 3 | `dep-missing-le` | `install-extractor-le` | same | L3; the "v4be alone does not satisfy" claim kept and now source-backed by the resolved-executable-only report | S112 :24,:68-69; S120 `command.py:70-72`; S119 `:186-201` | a dependency list naming both binaries resolves to row 2 (clause 3's first branch) — stated in the cell |
| 4 | `partial-body-failure` | `salvage-partial` | exact → contains; `be *` kept | **F6 / L5**: a partial failure carrying link or depth gaps no longer falls to a symlink row | S119 `:288-293`; `w2/R40W2C2IndepEval.md` §6 for the oracle-match half | L4's inference retired by that measurement (H21: 4 of 5 files match, the fifth truncated) |
| 5 | `avm-marker-be-dropped` | `wrap-extractor-be` | exact → contains; `sr *`; cause no longer routes its own damage branch, that branch moved to the pre-check | **M3**; L2 closed by measurement | S112 :44-50; S121 build; `l2-wrapper-measurement.md` (PATH wrapper honoured, `-be` flips P=0 → 3 files) | the wrapper must be removed after use (cell says so); L2's mechanism now has a run, not a guess |
| 6 | `body-extractor-failure` | `preserve-failure` | exact → contains; cause rewritten; `handler` widened `squashfs_v4_be` → `squashfs_v4_*` | **M2**: the old cause denied the endianness handshake for a population (marker-stripped genuine AVM body) that is exactly it | S120 `report.py:91-98`; S124 :35; S112 :44-50; `w1/R40MistakeHunt.md` MH-6 | a timed-out run records `cmd`, so `BE` reads `n/a` and lands here — stated in the block prose and Limits |
| 7 | `depth-limited-nested` | `raise-depth` | **new row** | the inherited ceiling: all four round-40 C1 carriers were `unclassified` under v2 | S119 `FirmwarePublication.js:23-29,:243-247,:294-299`, `FirmwareRelease.js:27-32` | the row labels an envelope; it does not descend the carve. `raise-depth` is a new token and must be in the vocabulary line (it is) |
| 8 | `mixed-symlinks` | `audit-symlinks` | exact → contains; `sr yes` kept | clause 8's "and `unpublished-entry` ∈ G" is membership, not equality | S118 :50-92; S122; S119 `:301-307`, `firmwareAnalysis.js:139` | a mixed envelope that also carries `extractor-failure` is clause 4 (partial), so the symlink audit is not its action — clause order, disclosed |
| 9 | `escaping-symlink-removed` | `expect-link-absent` | gap `*` → `none` | **L5 / F6**: the absorbing row is closed; a combined set can no longer land here | S118 :42-47,:58-65,:79-90; S122 | none measured |
| 10 | `in-tree-symlink-metadata` | `count-gap` | `sr no` → `*` (row 8 above supplies the `yes` case); gap stays the exact singleton | clause 10 is the only set equality, so it must not be loosened | S119 `:301-307`, `firmwareAnalysis.js:139` | a second gap kind falls to clause 12 (`unclassified`) — v2 also refused it; disclosed |
| 11 | `clean` | `none` | `sr no` → `*`; cause rewritten | **L6**: the row no longer claims no link was removed; unblob deletes an empty-target link with no report | S118 :67-69; S119 `:301-307` | `[INFERENCE]` on the population: no committed envelope carries an empty-target link |
| 12 | `clean-empty` | `confirm-empty` | unchanged cells; cause now cites the publication rule | clause 11; source honestly cited | S119 `:301-307`; R39-CL3 D2 | none |

Two cause cells cite by artifact rather than by S-row: row 5's `l2-wrapper-measurement.md` (own-work
measurement, this wave) and row 1's R39 knowledge entry. Every other cause names an S-id with a
`file:line`; the only `[INFERENCE]` marker in the block is row 11's population note. S121 is cited for
what `-be` does to the reader (`-DFIX_BE` build), inherited from the round-40 registry row — I did not
re-fetch that URL this wave, and the block does not add a line number to it.

## 4. What was measured on the draft (all read-only against the lane)

Commands (artifacts dir, scratch cwd):

```
python3 -I -B v3-refparse.py --selftest                                   -> cases=20 pass=20 fail=0, exit 0
python3 -I -B v3-refparse.py --skill fixture-SKILL.md --table-only        -> marker line 45, 12 rules, exit 0
python3 -I -B checks.py                                                   -> TOTAL 48/48, exit 0
```

`fixture-SKILL.md` wraps `block20.md` in a minimal `## Queue-drain craft` section, i.e. the block is
measured in the position it will occupy, which is the round-40 `R40C2Shortcuts.md` D1 lesson.

| group | set | expected labels come from | result |
|---|---|---|---|
| A | 26 committed round-40 held-out envelopes | `manifest.json:label_actions` (round-40 data, not this draft) | **26/26**, `a-heldout-26.tsv` |
| B | the four round-40 C1 `after.json` receipts | clause 7 by hand | **4/4** `depth-limited-nested`/`raise-depth` at row 7, `b-c1-4.tsv` |
| C | 18 combined-set envelopes built from committed ones by injecting gap kinds / resetting the file count | the clause number written next to each case in `checks.py` | **18/18**, `c-combined.tsv` |
| control | the same block with every `kind+` rewritten to an exact `kind` (v2's set grammar in v3 shape) | same | A 26/26, **B 0/4**, **C 7/18** (`ctl-exact-*.tsv`) |

How to read that: A shows the grammar extension changed nothing for the v2 classes (all their gap sets
are empty or singletons), so v3's 26/26 on that set is a *reproduction*, not new evidence. B and C are
where the draft earns its keep, and the control quantifies it — the contains form is the difference
between 4/4 + 18/18 and 0/4 + 7/18. C is a *composition self-check*: its expected labels come from the
same precedence text the table was written from, so it proves table-vs-text agreement, not label truth.
Label truth is what the frozen independent evaluator and the held-out envelopes are for, and the claims
already require a disagreement between that evaluator and the generator's class map to be reported and
to fail the claim.

## 5. The one measurement beyond the table (L2)

`l2-wrapper-measurement.md`: a fresh 41 377-byte marker-only standard-BE carrier
(`gen-squashfs.py --endian avm`, sha256 `ec65e771…`) run through REA 6.5.0 three ways — no wrapper
(`G={extractor-failure}`, `P=0`, `BE=no`), a `sasquatch-v4be` wrapper that appends `-be` (`G=∅`, `P=4`
including its own marker, the three tree files sha256-identical), and a publishing decoy that proves
unblob resolves the extractor through PATH. The carried `[INFERENCE]` on `wrap-extractor-be` is
therefore closed by a run, and row 5 now cites it. Observed but unexplained and recorded as such: a
wrapper's side writes *outside* the extraction directory do not appear, so a wrapper should prove
itself with a marker inside the `-d` directory.

## 6. Not done, and why

- **No carrier built or extracted for C1/C2** beyond the one dev tree above; C1's reserved carriers
  (V3, V4, L3, L4) and the vendor images were neither read nor run — they are another seat's data.
- **No round-41 interpreter, counter or held-out generator authored.** `v3-refparse.py` is a reference
  reader for this draft (bounded, selftested), not `tools/round-41/sqfs-triage-v3.py`; the freeze owns
  that file and the L1 integrates it.
- **No scorer run.** The claim's target is the held-out score at the measured revision; nothing here
  substitutes for it. This artifact measures the *draft's shape*, not the claim.
- **The 13 v2 labels' truth is not re-argued.** Round 40 scored them; this draft only had to avoid
  regressing them, which A measures.
- `block20.md` cites the v3 knowledge entry by line range (`:11-24`, `:36-56`, `:57-72`); those ranges
  are the drafted entry's, so if the L1 edits the entry the citations must be re-anchored before the
  freeze (round-40's stale-embedded-copy defect, M1, is exactly this class of drift).
