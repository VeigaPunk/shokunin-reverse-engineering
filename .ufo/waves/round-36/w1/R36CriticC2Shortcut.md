# R36CriticC2Shortcut — P36-C2 shortcut falsifiers (round 36, wave 1)

Seat: critic (leaf). Assigned question: find an edit to `SCORECARD.md`/`SHONEN.md` that drives
`c2-counter.py` to `met_target` **without** making the self-assessment match observed state.

**Result: P36-C2 is falsified as implemented.** Six shortcut classes reach `met_target: true` on
fixture repos while the frozen surfaces still carry the base's false statements; one of them (A1) is a
three-line append to `SCORECARD.md` + `SHONEN.md` and leaves `116/116 knowledge files mapped`,
`` `receipts-B/` `` and `` `ScoutSkillPlacement.md` `` in the scored files untouched. Nothing in the
lane was modified except this report — no counter, claim, carrier or surface was edited.

## Frozen inputs (verified, read-only)

| Item | Value |
|---|---|
| Claim file | `plans/round-36-claims.md` (freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`) |
| Base | `cab59f221fe19726b5692bfa4d9a9679e96b8a73` |
| Counter | `tools/round-36/c2-counter.py`, sha256 `f079aff11a3d65429b40cac62671f7bde6ee7f94ba2497d11a9c561f9c9b078f` — identical at freeze `790561d4`, at the control commit `6a870b92`, and at lane HEAD (`git show <rev>:tools/round-36/c2-counter.py \| sha256sum`) |
| Controls compared against | `.ufo/waves/round-36/controls/ctl-c2-{0,1,2,3}-*.{json,out}` |
| Measured region | `units()`: `## Owned axes` rows, `## Capabilities` table rows, SHONEN `- [ ]` boxes |

## Method

```
S=/fast/scratch/hyaku/kaidoku-r36/R36CriticC2Shortcut ; export TMPDIR="$S"
D=$S/fx ; git -C "$D" init -q
git -C <lane> archive cab59f221fe19726b5692bfa4d9a9679e96b8a73 | tar -x -C "$D"   # rc 0, 23168 files
git -C "$D" add -A && git -C "$D" commit -qm base        # BASE = fixture commit of the same tree
python3 -I -B <lane>/tools/round-36/c2-counter.py --root "$D" --rev <cand> --base <BASE> --json-out "$S/<tag>.json"
```
Each candidate = `git checkout -f BASE && git clean -fd`, apply one edit, commit, run the counter.
`git -C "$D" rev-parse --show-toplevel` = `$D` (checked before the first commit).

**Fixture fidelity.** At `BASE` the counter reproduces the frozen do-nothing control exactly:
exit 1, `{"mismatches":3,"guards_ok":false,"met_target":false,"pointers":34}`, unresolved
`[["cap:pre-registered two-lane live battery on REA 6.5.0","receipts-B/"],["shonen:No cross-domain bleed (PROVINCE.md still accurate)","ScoutSkillPlacement.md"]]`,
`base_pointers=34`, `base_unresolved` = the same two, observed
`command_a {mapped:122, knowledge_files:122, resolved_rules:17, rule_blocks:17}`,
`command_b [9,9]`, `craft_range [81,314]`, `adjacent_range [97,118]` — field-for-field identical to
`ctl-c2-0-do-nothing.json` (only the fixture commit id differs).

Counter selftest in the same scratch (`HYAKU_SCRATCH=$S python3 -I -B c2-counter.py --selftest`):
exit 0, `{"cases":13,"green_ok":1,"red_ok":12,"failures":[]}`. **None of the 13 cases exercises any
class below**, so the selftest certifies the counter against a shortcut set that excludes all of them.

## Scored candidates

| # | class | edit | exit | `met_target` | mismatches | guards_ok | pointers |
|---|---|---|---|---|---|---|---|
| V0 | honest control | restate count 122/122 + repoint both base-broken pointers to the same-basename documents | 0 | **true** | 0 | true | 34/34 |
| V1 | A4 decoy repair | V0 + cite two planted same-basename decoys instead | 0 | **true** | 0 | true | 34/34 |
| V2 | A1 duplicate-unit shadow | base rows/box untouched; append duplicate `coverage` row, duplicate capability row, duplicate box title carrying the corrections | 0 | **true** | 0 | true | 34/34 |
| V3 | A2 extra box, false count | V0 + append box `SKILL.md contains real decision tables, split detail` asserting `3/3 rule blocks` | 0 | **true** | 0 | true | 35/34 |
| V4 | A2 extra row, false count | V0 + append own-axes row `coverage (map) … 116/116 knowledge files mapped` | 0 | **true** | 0 | true | 35/34 |
| V5 | A3 second conflicting range | V0 + second `PROVINCE.md:95-116` beside the correct `PROVINCE.md:97-118` | 0 | **true** | 0 | true | 35/34 |
| V6 | A5 population degradation | keep `116/116`; repair pointers; delete 6 mapped, uncited knowledge files | 0 | **true** | 0 | true | 34/34 |
| V7 | rejected: repair shape | V0 but cap cites `.ufo/waves/luna-round-6/receipts-B/leg-1.md:1-1` | 1 | false | 0 | false (`unrepaired`=cap) | 34/34 |
| V8 | A6 pointer identity swap | V0 with `.ufo/waves/round-31/w1/ScribeScorecardRows.md` → `corpus/README.md:1-2` | 0 | **true** | 0 | true | 34/34 |
| V12 | rejected: count wording escape | V0 with `122 of 122 knowledge files in the map` | 1 | false | 1 (`O1 stated:null`) | true | 34/34 |
| V13 | rejected: box rename | V0 with box 4 title `No cross-domain bleed` | 1 | false | 0 | false (`missing_units`) | 34/34 |
| V14 | A3 second conflicting count | V0 + `(older claim \`SKILL.md:1-999\`)` and `; older map says 999/999 knowledge files mapped` | 0 | **true** | 0 | true | 35/34 |
| V15 | rejected: out-of-file range | V0 + `\`SKILL.md:1-2000\`` (file is 1221 lines) | 1 | false | 1 (`unresolved` depth) | true | 35/34 |

## Accepted classes

### A1 — duplicate unit keys shadow the real row/box (strongest; `SCORECARD.md` + `SHONEN.md` only)

`units()` builds `{unit_key: text}` with plain assignment (`u['owned:'+first_cell(l)] = l`,
`u['cap:'+…] = l`, `u['shonen:'+title] = l`). A later row/box with the same first cell (or the same
box title) overwrites the earlier text: the earlier statement is not count-checked **and its pointers
are never resolved**. The shadow text is what satisfies the base-repair guard.

Edit (V2, `-U0` shows three added lines and no removals):
- after the `| coverage |` row: `| coverage | 9.72 → 10.0 | 122/122 knowledge files mapped at \`corpus/README.md:1-5\` (round-36 recount) | \`corpus/README.md\`; \`corpus/README.md:3\` | round 36 |`
- after the `| pre-registered two-lane live battery on REA 6.5.0 |` row: same first cell, evidence cell now names `.ufo/waves/luna-round-6/receipts-B/`
- at EOF of `SHONEN.md`: a box with the byte-identical title `- [~] No cross-domain bleed (PROVINCE.md still accurate)` asserting `PROVINCE.md:97-118` and `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`

Counter: `{"assertion_mismatches":[],"guards_ok":true,"met_target":true,"mismatches":0,"pointers":34}`, exit 0.
Surface state at that revision (checked with the counter's own `show()`): `116/116 knowledge files mapped`
present ×1 in `SCORECARD.md`, `` `receipts-B/` `` present ×1 in `SCORECARD.md`, `` `ScoutSkillPlacement.md` ``
present ×1 in `SHONEN.md`. The predicate sentence — "the SCORECARD `## Owned axes` rows, the SCORECARD
`## Capabilities` table rows and the SHONEN.md boxes — carry zero mismatches" — is therefore false at a
revision the counter scores `met_target`.

### A2 — a statement is validated by unit identity, not by occurrence

`O1..O4` look up fixed keys (`U.get('owned:coverage')`, `sh1 = next(… startswith('shonen:'+BOX1))`).
A statement of the same fact under any other key is unvalidated.
- V4: `| coverage (map) | 10 | 116/116 knowledge files mapped | … |` in `## Owned axes` → green, observed 122/122. The false count sits inside the scored section.
- V3: extra box titled `SKILL.md contains real decision tables, split detail` with `3/3 rule blocks` → green; `next()` returns the base box (first insertion order) and the split box's count is never compared. With an *identical* title the earlier box is dropped altogether (A1).

### A3 — `re.search` validates only the first statement per unit

`stated()` uses `re.search`, so a second, contradictory statement in the same unit is invisible once the
first matches observed.
- V5: box 4 carries `PROVINCE.md:97-118` (observed) **and** `PROVINCE.md:95-116` → green.
- V14: coverage row carries `122/122 … knowledge files mapped` **and** `999/999 knowledge files mapped`; depth row carries `SKILL.md:81-314` **and** `SKILL.md:1-999` → green.

Boundary: a secondary range that does not resolve is caught at pointer level (V15 red), so this class is
"resolvable but wrong", which is exactly how a contradictory self-assessment reads.

### A4 — the repair test cannot distinguish documents (`V0` output ≡ `V1` output)

`unrepaired` accepts any pointer `p2` that resolves and satisfies `p2 == path or p2.endswith('/'+path)`,
i.e. a basename-suffix test. V0 (correct documents) and V1 (planted decoys
`.ufo/waves/round-36/w1/receipts-B/junk.txt`, `.ufo/waves/round-36/w1/ScoutSkillPlacement.md`) are
field-identical: `mismatches`, `unresolved`, `assertion_mismatches`, `guards`, `guards_ok`,
`met_target`, `pointers`, `observed` all equal.

This is *not* a rejection of the run: both base twins are in fact the plausible intended documents
(`.ufo/waves/round-30/w1/ScoutSkillPlacement.md` is the placement note that discusses the SHONEN box-4
pointer; `.ufo/waves/luna-round-6/receipts-B/MANIFEST.txt` is the 10-leg B lane) and V0 is the honest
repair. The finding is that a green C2 provides **no evidence** for the predicate's "same document"
clause — the freeze names no intended document, so the clause is unimplementable and the counter
substitutes a test any twin passes. The existing controls do not cover it: CTL-C2-3 substitutes
`corpus/README.md`, which the suffix test happens to reject.

### A5 — the counts are relative, so shrinking the population greens them (outside the assigned surface)

`O1/O2` compare the stated numbers against command A **at the same revision**. V6 leaves the `116/116`
row untouched and deletes six knowledge files that are mapped and not cited by any
`## Queue-drain craft` rule (`2026-10-13-asar-surface.md`, `-crash-evidence.md`, `-doctor-taxonomy.md`,
`-elf-observation-jq.md`, `-ghidra-install.md`, `-java-runtime.md`): observed becomes `(116,116)`,
matching the stale row → `met_target: true`, exit 0, `guards_ok: true`, pointers 34/34.
No guard bounds `knowledge_files`, `mapped` or `rule_blocks` below the base values, so a green C2 is
compatible with the lane losing six corpus entries. This edit is not SCORECARD/SHONEN-only; it is
reported because it defeats the claim's separability/guard text, not because it is a tempting surface move.

### A6 — the pointer guard is a count, not an identity

`guards_ok` requires `total >= base_total`. V8 replaces the coverage row's
`.ufo/waves/round-31/w1/ScribeScorecardRows.md` citation with `corpus/README.md:1-2` and stays green at
34/34: a real citation disappears at zero cost.

## Rejected classes (negative results — the counter is not uniformly weak)

- V7: citing a **file inside** the correct-basename directory (`.ufo/waves/luna-round-6/receipts-B/leg-1.md:1-1`) is rejected — `unrepaired` = `[cap:…, receipts-B]`. The guard matches the pointer path, not its ancestors.
- V12: dropping the count phrase (`122 of 122 knowledge files in the map`) is rejected — `stated: null` → `O1` mismatch. "Absent but not counted" is caught.
- V13: renaming a base box title is rejected — `missing_units` non-empty. A split must be an *addition* (A2) or an exact-title duplicate (A1).
- V15: a second *unresolvable* range is rejected — `unresolved: [owned:depth, SKILL.md:1-2000]`.
- Frozen controls CTL-C2-0/1/2/3 reproduced on the fixture: base 3 mismatches / junk count red / deletion red / non-basename substitution red.

## Impacted axes

- **calibration** (C2's own axis): all six classes produce `met_target: true` on a miscalibrated surface, so the axis reading would be false. A1 is reachable in good faith — a scribe restating the count by appending a row instead of editing the existing one produces exactly V2.
- **coverage**: A5 is a coverage regression (six mapped knowledge files gone); A1/A6 let stale coverage citations survive behind a shadow row.
- **depth**: A3/A2 shapes apply directly to the depth row's `SKILL.md:81-314` and `17/17` statements.
- **Kill rule / controls**: the frozen control set covers deletion, junk counts and suffix-visible substitution only. Running CTL-C2-0..3 does not measure any of A1/A2/A3/A5/A6, so a green C2 at the measured revision would not establish that the self-assessment matches observed state.

## Smallest safe corrections (advisory — nothing here was edited)

1. **Freeze-time, before any data:** P36-C2 must name the two intended documents by full lane-relative
   path (`.ufo/waves/luna-round-6/receipts-B/`, `.ufo/waves/round-30/w1/ScoutSkillPlacement.md`) and the
   counter must compare exact paths (base path, or a relocation named in the claim) instead of a basename
   suffix. Closes A4. Without it the "same document" clause is not measurable.
2. **Counter, one change:** validate by statement shape over the *whole* surface set — collect every
   `(\d+)/(\d+) knowledge files mapped`, `… queue-drain rule blocks`, `… preselected reconciliation
   obligations`, `SKILL.md:(\d+)-(\d+)` and `PROVINCE.md:(\d+)-(\d+)` occurrence in the three surfaces with
   `findall` and require *every* occurrence to equal the observed value. Closes A2, A3, V14; with (3) closes A1.
3. **Counter, one change:** stop collapsing duplicate unit keys — keep every row/box (`f'{key}#{n}'` or a
   list per key) and resolve pointers over all of them. Closes A1 (both the hidden count and the hidden
   unresolved pointers).
4. **Guard:** populations must not regress against the base (`knowledge_files`, `mapped`, `rule_blocks`,
   `resolved_rules` ≥ base) and no knowledge file may be removed by the claim's diff. Closes A5.
5. **Guard:** pointer identity instead of pointer count — every `(unit, path, range)` present at the base
   must still be present or explicitly repaired. Closes A6.

## Limits / inference

- Fixtures copy the base tree into an independent repo; revs are fixture commits, not lane commits. All
  counter arguments, exit codes and the six-key stdout line are quoted above; JSON receipts existed only
  in scratch and are not cited as evidence.
- `[INFERENCE]`: whether a lane would actually produce A1–A3 in good faith is not measured; only that the
  counter scores them green. Severity ordering (A1 > A3 > A2 > A4 > A6 > A5) is my judgement.
- V14's `SKILL.md:1-999` is inside the 1221-line file, so it passes the range check; the class is
  "resolvable but contradictory", not "out of range" (that case is V15, rejected).
- No tools installed; `pacman` untouched. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36CriticC2Shortcut`
  removed after the run.
