# RV-12 — advisory patch text: fragility mitigations for the arc3-era entries

Author: seat RV-12 (c3, reviewer) · wave arc3-loop1-round3 · **advisory only**.

Status of the real target: `.ufo/gates/citation-drift/pointer-table.json` was landed
by EX-41 at sha256 `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7`
(57 entries / 4 quoted; expected.json re-pinned to the same digest). RV-12 did **not**
write it, does not propose editing it this round, and does not dispute the landing:
the round's acceptance test (the census) is met and the probe is clean 0 in both modes.
The items below are for the **next** extension or for a maintainer who reworks a
citation, in the order RV-12 would rank them.

## 1. Version-named instrument path (highest measured likelihood)

`.ufo/gates/c1-census-v10.py` is pinned by three new extracted entries
(`census-cites-sc-e22-debt` :7, `census-cites-sc-round4-range` :27,
`census-cites-sc-laundering-refusal` :33). The path carries its version, and the
lane's own history shows the bump (`c1-census-v10.py` replaced v9 at `265e1aa`;
r1 evidence keeps `c1-census-v9-recovered.py`). A future v11 normally lands as a
**new path**, at which point all three entries read `citation_file_absent` on a
tree whose citations were honestly updated.

Options (any one closes it):
- grade the three citations from the SCORECARD side (an `extracted` entry whose
  citing line is the SCORECARD row that names the census path), or
- add a coupled entry pinned to the SCORECARD row + keep the instrument pin only
  as a note, or
- drop the version out of the file name at the next version bump.

## 2. Anchor-form reform (the doctrine's own prescribed form)

All 14 new `extracted` entries fire `citation_dead` when a citing pointer is
honestly reformed from `` `path:line` `` into the anchor form — the form the
table itself pins as durable (`mcpreg-errata-anchor-form`,
`r416-errata-durable-anchor`). Measured: 25 entries on the landed table, 14 of
them new.

Nothing in the probe can express "either the number or the anchor form", so the
only in-scope mitigation is the coupling duty, stated where the maintainer will
see it: **a commit that reforms a citation must re-form its table entry in the
same commit** (the frozen-run guard makes the half-done edit loud, exit 2, never
silent). If a future round adds an alternative-pattern capability to the probe,
these entries are its first customers.

## 3. Prose/form pins on mutable files

`sc-arc3r1-section-key` (SCORECARD.md:1338) and `sc-arc3r2-section-key`
(SCORECARD.md:1419) pin a line number in an operator-mutable file. Measured cost:
0 insert-above events in 41 revisions for the arc3 region (tail-append-stable), so
the real-world likelihood is low today; the class is the one rule #11 names. If the
arc3 sections ever stop being tail-append (a connector revision, a re-order), both
entries and `sc-arc3r2-cites-shonen` (:1435) shift together. Preferred form when
they are next touched: keep the `exact` pin for the section *key* but add the
section-key wording to the entry's `note` so the maintainer sees the intent.

## 4. Cross-chain coupling (open at review time)

Four new anchors target `.ufo/gates/custody-pair/README.md`
(`custody-readme-v2-fieldset`, `-rewrite-identity`, `-precedence`,
`-scratch-never-tmp`) — the file C2 rewrites this same round. RV-12 measured the
four tokens present at review time (occurrences 2/1/1/1) and the probe clean;
if C2's landed text drops any of those phrasings the probe goes RED on the
integration commit. Recommended: the parent's landing check re-runs the probe
**after** C2's README lands, before the records commit.

## 5. Renames (total-impact, zero base rate)

95 commits, 0 renames. If one ever happens, the entries fire
`citation_file_absent` / `citation_dead` even when every citing line was updated
(measured: SCORECARD rename → 5 entries, README rename → 3, r7 entry → 4,
r1 EVM entry → 2). Cheapest guard is the same coupling duty as §2; no code change
is worth it at a 0/95 base rate.