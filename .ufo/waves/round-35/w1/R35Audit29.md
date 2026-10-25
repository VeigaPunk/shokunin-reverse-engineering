# R35Audit29 — S136 own-work quote locator

**Result:** S136's named-own-work quote is locatable and present. This corroborates the narrow quote/locator check only; it does not admit S136 or alter frozen Round-35 claim scope.

## Evidence

- The lane registry row identifies S136 as a round-4 `own-work` record against `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md`; the row's `used-by` is empty. In the corpus file, the supplied locator is heading `# kaidoku-r4u / 06 — ADB surface: client present, zero devices` at line 3.
- The exact contiguous quote `2 of 24 verbs are` occurs once in that file, at line 8, as confirmed by literal grep count `1`. SHA-256 of the file: `26eeaf6f91eee756e962b9259e1f600f45819c653a659a86a8dacf1e87aa26bf`.
- The cited knowledge file is tracked (`git ls-files --error-unmatch` succeeded), and its introducing commit `999ce123` is an ancestor of observed lane HEAD `3ecf42981a0b63414de90ade643040d609dbb8a5`.
- The original quarantine verdict already states the heading and quote, labels the row **verifiable**, and notes it is not adopted because no admitted entry cites it. The upstream absent-defect register's S136 row records the original defect as a missing locator, not an absent quote. Round-4 scout context corroborates S136 as the lane's own measurement/registry row for adb verb classification.

## Commands and observed outcomes

Run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`:

```sh
grep -n "2 of 24 verbs are" corpus/knowledge/2026-10-13-r4u-06-adb-surface.md
# 8:Answer: the adb surface is **bound and partially live** — 2 of 24 verbs are

grep -c "2 of 24 verbs are" corpus/knowledge/2026-10-13-r4u-06-adb-surface.md
# 1

grep -n "kaidoku-r4u / 06 . ADB surface: client present, zero devices" corpus/knowledge/2026-10-13-r4u-06-adb-surface.md
# 3:# kaidoku-r4u / 06 — ADB surface: client present, zero devices

sha256sum corpus/knowledge/2026-10-13-r4u-06-adb-surface.md
# 26eeaf6f91eee756e962b9259e1f600f45819c653a659a86a8dacf1e87aa26bf  corpus/knowledge/2026-10-13-r4u-06-adb-surface.md

git ls-files --error-unmatch corpus/knowledge/2026-10-13-r4u-06-adb-surface.md
# corpus/knowledge/2026-10-13-r4u-06-adb-surface.md

git merge-base --is-ancestor 999ce123 HEAD && echo ANCESTOR
# ANCESTOR

git rev-parse HEAD
# 3ecf42981a0b63414de90ade643040d609dbb8a5
```

A recursive literal search found this phrase in the cited knowledge file and in the round-35 quarantine-verdicts report. The latter is a later repetition of the quote and does not undermine location in the source; it means global repository-wide uniqueness is not claimed. No gate/counter was run.

## Provenance and limits

Read-only inputs: lane `corpus/SOURCES.md`, the cited corpus entry, round-35 `.ufo/waves/round-35/assimilation/quarantine-verdicts.md`, round-34 staged IDs, and the upstream `/home/vgpnk/Projects/shokuknow/.ufo/scopes/corpus-expansion-4/ScoutKaidoku.md` plus absent-defect-register row. No source or production files were changed. This report is the sole write, under the assigned seat directory.

This is documentary validation of an existing committed file and its quote, not a rerun of the historical adb measurement, source authenticity proof, adoption decision, or C1/C2 execution evidence. Frozen Round-35 claims C1 (S125/S129 `.jsc` assimilation) and C2 (round-34 D1–D4 closure) were not scored or modified. No pacman installs, nested delegation, or background work.