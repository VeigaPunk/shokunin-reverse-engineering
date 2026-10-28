# ScoutWaves — round-47 score-receipt house, and the set round 48 must commit

Axes: coverage of every file under `.ufo/waves/round-47/l1/scores/` and of which document cites it; depth of the two receipt schemas and of `quote_value`; calibration of the quoted numbers against those files, and of the minimum set the landing revision has to contain.

Pinned revision for every `git show` and for `record2.score`: `663f30ee751694fb0970e7de68fe88356e680822`. `tools/round-48/record2.py` at that revision is blob `1188f43fa00abf9fa7bafb120158f335c26fb30c`, the same blob as at `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873` and as the worktree file (`git hash-object`). No tool was installed. `scripts/hyaku/disk-guard.sh check` exited 0 (`/fast/scratch/hyaku` 33%).

Receipt of the quote-binding run: `.ufo/waves/round-48/w1/ScoutWaves/receipts/quote-binding.out` (driver exit 0, stdout sha256 `b9b0b5ed14d6d4805aecd2826c35d4c66a45252893070850c8287d3663f35412`, UTC `2026-10-28T18:57:59Z`). The driver calls `record2.score` in process with `battery=None`. The `record2.py` CLI (`--freeze` / `--rev` / `freeze_state`) was not run.

## What the round report cites

`LOG.md` `### Round 47` cites two files, in the short form `l1/scores/<file>`:

| cited file | what the paragraph says | what the file holds |
|---|---|---|
| `l1/scores/c1-at-A4.json` | exit 0, `rule_blocks 24`, `rows 4`, `refs 8`, battery `4/4/0/1/0` | `met_target true`, those four counts, battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0`, `rev=freeze=1e2c3102952dc636650095643c1963c833859019` |
| `l1/scores/c2-at-A4.json` | exit 0, `atoms 50`, `mismatches []`, `corrections 2`, battery `3/0` | `atoms 50`, `mismatches` length 0, `corrections 2`, `battery.correction_forgeries 3`, `forgeries_green 0`, `exempted` length 2 |

Those two sentences match those two files. The short form does not match `record2.RECEIPT` (`\.ufo/waves/round-[0-9]+/l1/scores/[A-Za-z0-9._-]+\.json`), so the LOG citations are invisible to the round-48 counter. `LOG.md` does not cite `c1-at-A7.json` or `c2-at-A7.json`.

`SCORECARD.md` `## Round 47` is the section `record2` reads. It cites two full paths, and the same two names again without the `.ufo/waves/round-47/` prefix in the paragraph above the table:

- `.ufo/waves/round-47/l1/scores/c1-at-A7.json`
- `.ufo/waves/round-47/l1/scores/c2-at-A7.json`

The `## Owned axes` calibration cell also cites the full `c2-at-A7.json` path, and the coverage and depth cells cite the directory `.ufo/waves/round-47/l1/scores/`. The directory has no filename, so it misses `RECEIPT`. The owned-axes block sits outside `## Round 47`, so the path collector and the quote scanner both skip it.

`corpus/lessons/round-47.md` cites short names only: `c1-at-L1.json`, `c1-at-A2.json`, `c1-at-A4.json`, `c1-at-A6.json`, `c1-at-A7.json`, `c2-at-L1.json`, `c2-at-R1.json`, `c2-at-A5.json`, `c2-at-A7.json`. Same invisibility to `RECEIPT` and to `record.py`'s `WAVE_DIR`.

## The directory

22 tracked files, `c{1,2}-at-{label}.json`. Labels present: `L1`, `R1`, `R2`, `R3`, `R4`, `A2`, `A4`, `A5`, `A6`, `A7`, `FINAL`. No `A1`, no `A3`. History on the path runs from `caafeffa` (2026-10-28 14:55 -0300, both counters' receipts) through `b1a058f3` (`round-47: final receipts at the tip`).

Round 46 has the same house at a smaller scale: `SCORECARD.md` `## Round 46` cites `.ufo/waves/round-46/l1/scores/c1-at-F4.json` and `c2-at-F4.json`, and `git ls-files .ufo/waves/round-46/l1/scores` lists 12 files.

### Schema

C1 files (`counter` `round-47-c1`, 30 keys) are `exact.py` receipts: `rule_blocks`, `rows`, `refs`, `met_target`, `failing`, `rev`, `freeze`, `profile`, pin fields, and `battery` with `forgeries_total`, `v2_green`, `v3_green`, `genuine_green`, `crash`. They have none of `atoms`, `exempted`, `corrections`, `mismatches`.

C2 files (`counter` `round-47-c2`, 13 keys) are `record.py` receipts. The four quote keys sit at the top level. `quote_value` returns the int for `atoms` and `corrections`, and the list length for `exempted` and `mismatches`. Every c2 file has `corrections` 2 and `mismatches` length 0. `exempted` is a list of `{class, key}` objects.

A `record2.py` receipt is a third shape, observed on `.ufo/waves/round-48/controls/ctl-c2-0-do-nothing.json` and on the in-memory object in the receipt: `corrections` at the top level is the count of `## Record corrections — round 48` lines; `atoms`, `exempted`, `mismatches`, and the oracle's own `corrections` sit under `oracle`. `quote_value` does not look under `oracle`.

### Each file

C1, `exact.py`. Battery scalars `4/4/0/1/0` mean `forgeries_total / v2_green / v3_green / genuine_green / crash`.

| file | rev (measured) | freeze | met | what it holds |
|---|---|---|---|---|
| `c1-at-L1.json` | `e856beb55208` | `9018c53b1650` | false | `refs 8`. `failing[0]` starts `arm cells not exact vocabulary tokens`. Battery skipped. Lessons M47-5. |
| `c1-at-A2.json` | `62e33f7dd75c` | same | true | `refs 8`, battery `4/4/0/1/0`. Lessons M47-5. |
| `c1-at-A4.json` | `1e2c3102952d` | same | true | same verdict as A2. The LOG citation. Lessons M47-5. |
| `c1-at-A5.json` | `07d2894eabe8` | same | true | same verdict as A2. Uncited. |
| `c1-at-R1.json` | `caafeffa330a` | `1e2c3102952d` | true | `refs 8`, battery `4/4/0/1/0`. Uncited. |
| `c1-at-R2.json` | `a631bba01633` | `07d2894eabe8` | true | `refs 8`, battery `4/4/0/1/0`. Uncited. |
| `c1-at-A6.json` | `f54b3b6de908` | same | false | `refs 9`. `failing`: `interpreter sha256 pin does not match the bytes at rev`. Battery skipped. Lessons M47-7. |
| `c1-at-R3.json` | `04469ee8f30b` | `07d2894eabe8` | false | `refs 9`. `failing`: `battery v2_green 0 != 4`, `battery genuine_green 0 != 1`. All four fixtures have `v2_exit 1` with `unresolved or unvalidated citations: 1`. Uncited. |
| `c1-at-A7.json` | `a07537869cf3` | `f54b3b6de908` | true | `refs 9`, battery `4/4/0/1/0`, 2513 bytes. The scorecard citation. |
| `c1-at-R4.json` | `31b092d17e77` | `f54b3b6de908` | true | same verdict as A7, later rev. Uncited. |
| `c1-at-FINAL.json` | `6f9fd7f8f001` | `f54b3b6de908` | true | same verdict as A7, tip remeasure. Uncited. |

C2, `record.py`. `forgeries_green` is `battery.forgeries_green` against `correction_forgeries 3`.

| file | rev | met | atoms | exempted length | exemptions | forgeries_green | cited by |
|---|---|---|---|---|---|---|---|
| `c2-at-L1.json` | `e856beb55208` | false | 50 | 2 | seats/45, window/46 | 1 | lessons M47-2 |
| `c2-at-A2.json` | `62e33f7dd75c` | true | 50 | 2 | seats/45, window/46 | 0 | nobody |
| `c2-at-A4.json` | `1e2c3102952d` | true | 50 | 2 | seats/45, window/46 | 0 | LOG |
| `c2-at-R1.json` | `caafeffa330a` | false | 41 | 1 | window/46 | 1 | lessons M47-2 |
| `c2-at-A5.json` | `07d2894eabe8` | true | 41 | 1 | window/46 | 0 | lessons M47-2 |
| `c2-at-A6.json` | `f54b3b6de908` | true | 42 | 1 | window/46 | 0 | nobody |
| `c2-at-A7.json` | `a07537869cf3` | true | 42 | 1 | window/46 | 0 | scorecard section, owned-axes cell, lessons M47-9 |
| `c2-at-R2.json` | `a631bba01633` | true | 42 | 1 | window/46 | 0 | nobody |
| `c2-at-R3.json` | `04469ee8f30b` | true | 42 | 1 | window/46 | 0 | nobody |
| `c2-at-R4.json` | `31b092d17e77` | true | 44 | 1 | window/46 | 0 | nobody |
| `c2-at-FINAL.json` | `6f9fd7f8f001` | true | 44 | 1 | window/46 | 0 | nobody |

`atoms_by_class` at the three counts the prose argues about: A4 is `{axes:2, path:12, rev:33, seats:2, window:1}` (50). A7 is `{axes:2, path:8, rev:29, seats:1, window:2}` (42). FINAL and R4 are `{axes:2, path:8, rev:31, seats:1, window:2}` (44).

## Calibration of the quoted numbers

Inside `## Round 47` the quote regex finds exactly three tokens: `atoms 42`, `corrections 2`, `exempted 2`. `## Round 46` finds none. `mismatches []` does not match the regex (it wants a digit after the word).

At the pin, `record2.score` on the committed card (`battery=None`) returns exit 1 with `quotes_checked 2`, `quotes_bad [{round-47, exempted 2}]`, oracle `met_target true`, `mismatches` length 0, `atoms 44`. `c1-at-A7.json` has no quote keys. `c2-at-A7.json` backs `atoms 42` and `corrections 2`. Its `exempted` list has length 1, so `exempted 2` matches nothing that section cites.

The fresh oracle count 44 equals `c2-at-FINAL.json` and `c2-at-R4.json`. The section quotes 42, and that quote is backed by the older cited file. The clause reads the cited file's top-level cell.

The scorecard table's measured-at cell is `1e2c310295`, which is A4's `rev`. Both A7 receipts record `rev` `a07537869cf37963dff559fc75271dfa8fbb2542`. The paragraph above the table names `a0753786`. That cell is outside the quote regex.

The owned-axes calibration row says `exempted 1` next to `c2-at-A7.json`, which matches that file's list length. Lessons M47-9 says the cells now read 42 and 1; that sentence is true of the owned-axes row. The round table still says `exempted 2`.

`c1-at-A7.json` is still required. Hiding it from `files()` leaves `quotes_checked 2` (the c2 file still backs the two passing quotes) and makes the oracle report one path mismatch on `.ufo/waves/round-47/l1/scores/c1-at-A7.json`. `WAVE_DIR` turns every `.ufo/waves/round-N/...` token in the last two round sections into a path atom that must exist. The round-47 section currently has four such tokens, all present at the pin:

- `.ufo/waves/round-47/controls/ctl-c1-0-do-nothing.json` (458 bytes)
- `.ufo/waves/round-47/controls/ctl-c2-0-do-nothing.json` (1409 bytes)
- `.ufo/waves/round-47/l1/scores/c1-at-A7.json` (2513 bytes)
- `.ufo/waves/round-47/l1/scores/c2-at-A7.json` (1016 bytes)

`ctl-c1-2-freeze-battery-absent.json` appears in the section as a bare filename, so it is not one of those atoms.

## The quote clause accepts a second receipt

Frozen clause 4 binds each `atoms|exempted|corrections|mismatches N` to any cited receipt in the section whose top-level cell equals N. The check is `any(quote_value(r, key) == int(val) for _, r in recs)` over `RECEIPT.findall(section_text)`.

Command (driver above; the mutation is `section.replace` of the A7 path with the A7 path plus `` `, `.ufo/waves/round-47/l1/scores/c2-at-A4.json ``, once, inside `## Round 47` only):

`python3 .ufo/waves/round-48/w1/ScoutWaves/receipts/quote_binding.py`

Differing value, same prose (`exempted 2` unchanged):

| run | quotes_checked | quotes_bad | oracle atoms | oracle mismatches |
|---|---|---|---|---|
| committed card | 2 | `exempted 2` against A7 and c1-A7 | 44 | 0 |
| section also cites `c2-at-A4.json` | 3 | `[]` | 45 | 0 |

A4's `exempted` list has length 2 (seats/45 and window/46). A7's has length 1 (window/46). The oracle stays `met_target true` because the added path exists. Exit of `score()` stays 1 on both cards for the two clauses that are still open on this tree: round 47 has no seat atom and no seats correction, and `## Record corrections — round 48` is absent. The quote failure is the one that clears.

So a landing that keeps the words `exempted 2` and also names `c2-at-A4.json` anywhere in `## Round 47` satisfies clause 4 without a `quote` correction. The correction path is the one the claims file's landing requirement describes; this citation path also satisfies the frozen sentence.

## What a round-48 receipt can back

Fixture object, not written into the lane, returned only from `files()` for `.ufo/waves/round-48/l1/scores/c2-at-LANDING.json`:

```json
{"counter":"round-48-c2","corrections":2,"oracle":{"atoms":44,"corrections":2,"exempted":[{}],"mismatches":[]}}
```

Appended section text: `` exit 0, `atoms 44`, `exempted 1`, `corrections 2`, `mismatches 0` (`<that path>`). ``

`quote_value` on that object: `atoms` None, `exempted` None, `mismatches` None, `corrections` 2. On `oracle` directly, `atoms` is 44. The quote scan then marks `atoms 44`, `exempted 1`, and `mismatches 0` bad, and counts `corrections 2` checked. A `quote` correction cannot repair the three misses: `_quote_correction` uses the same top-level `quote_value`, and a receipt that lacks the key does not back the correction's true value.

`ctl-c1-0-do-nothing.json` (`counter` `round-48-c1`) also lacks all four keys.

Numbers that do bind today, if a round-48 section cites that existing file:

| cited c2 file | atoms | exempted | corrections | mismatches |
|---|---|---|---|---|
| `c2-at-A4.json` (and A2, L1) | 50 | 2 | 2 | 0 |
| `c2-at-A7.json` (and A6, R2, R3) | 42 | 1 | 2 | 0 |
| `c2-at-FINAL.json` (and R4) | 44 | 1 | 2 | 0 |
| a `record2.py` emission with two correction lines | none | none | 2 (the line count) | none |

`corrections 2` on a record2 emission is the number of parsed round-48 correction lines. `corrections 2` on `c2-at-A7.json` is the round-47 oracle's correction count. The same digit satisfies either citation. The landing requirement asks for two round-48 lines (a seats correction for round 47, a quote correction for round 47's exempted cell), which makes the record2 top-level count 2 as well.

## Minimum set round 48 must commit

Already committed, and still required once `## Round 48` is appended (the window becomes round 47 and round 48; round 47's path atoms stay):

1. `.ufo/waves/round-47/l1/scores/c1-at-A7.json` — path atom. No quote keys.
2. `.ufo/waves/round-47/l1/scores/c2-at-A7.json` — path atom, and the backer for `atoms 42`, `corrections 2`, and a `quote` correction that states `exempted 1`.
3. The two control paths named in the same section (above). They are not under `l1/scores/`.

New files: every `.ufo/waves/round-…/…` token the new `## Round 48` section writes. The scorecard-section house is one full path per claim, `c1-at-<label>.json` and `c2-at-<label>.json` under `.ufo/waves/round-48/l1/scores/`. Those two files are the counter-minimum landing pair. The 22-file series is the archive round 47 kept; twelve of those files are cited by none of LOG, the scorecard, or the lesson, and the counter does not require them.

If the new section quotes `atoms`, `exempted`, or `mismatches` followed by a digit, the cited file has to be a `record.py`-shaped receipt (top-level keys) whose cell equals that digit. A `record2.py` JSON backs `corrections <line count>` and does not back the other three. Citing `c2-at-FINAL.json` or `c2-at-R4.json` backs `atoms 44`, which is the live oracle count at this pin. Citing `c2-at-A7.json` backs `atoms 42`. Citing `c2-at-A4.json` backs `atoms 50` and `exempted 2`, which is the demonstrated way to clear the current `exempted 2` failure.
