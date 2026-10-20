# Round 15 w1 — AttackManualBoundary (critic, leaf)

seat: KaidokuR15.AttackManualBoundary
date: 2026-10-20
axes: calibration (primary), depth (do the docs describe the real gate control flow?)
repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin (HEAD `9719dd232687f5ee78a4ed323b37f8810e833d10`; worktree has an uncommitted QUALITY row 17)
execution: none. I did not run the gate, selftest, frozen run, measure, census, or any test. I did run non-verdict checks: `git status`/`diff`/`show`, `sha256sum`, an awk column listing, and one in-memory Python check. That check applied the gate's two heading regexes (copied from `quote-fidelity.py:75-76`) to sample lines and tested plain `in` substring membership. It is not gate output.
tool installs/updates: none.
writes: this file only.

## Target under attack

1. Landed worktree row: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:27` (row 17, supersedes cell `16`). Absent at HEAD: `git show HEAD:corpus/QUALITY.md | grep -c '^| 17 |'` → 0.
2. Unchanged registry row `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md:450`.
3. Sibling proposals feeding L1:
   - `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/ReviewManualRoute.md` §4.1 and §5.
   - `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/w1/BoundaryFixtures.md:10-12`.
4. Gate source: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/tools/quote-fidelity.py`. Read at `:1-123` and `:173-298`, plus grep. Not modified.

## Ground truth: what a manual-only input actually gets (code-read, not executed)

The gate has no representation field and no classifier. `parse_manifest` accepts only `id/source/section/quote` strings (`:194-208`). For each quote, `grade_quote` checks in this order:

| step | anchor | condition | finding | exit |
|---|---|---|---|---|
| pre | `:286-288` | source digest ≠ pin | `source_tampered` | 2 |
| pre | `:289-293` | source not valid UTF-8 | `invalid_manifest` "source is not valid UTF-8" | 2 |
| 1 | `:252-254` | >25 whitespace words | `quote_too_long` | 1 |
| 2 | `:256-258` | quote bytes absent from whole source | `quote_not_contiguous` | 1 |
| 3 | `:261-263` | selector matches >1 heading | `invalid_manifest` "duplicate exact heading" | 2 |
| 4 | `:264-266` | no heading matches | `quote_location_mismatch` "section not found" | 1 |
| 5 | `:267-268` | quote outside that section body | `quote_location_mismatch` | 1 |
| 6 | — | otherwise | none | **0** |

Exit is decided per manifest, not per quote (`:97-100`): any CNE finding wins.

Heading recognition (`:75`) is `^(#{1,6})[ \t]+(.+?)[ \t]*\Z`. In-memory regex check (my reproduction, not gate output):

- Matches: `# TODO: handle error` (True), `# define X 1` (True).
- Does not match: `#include <stdio.h>` (False), a setext `Title`/`=====` pair (False/False), a two-line `<h2>\nIntro</h2>` (False).
- So shell, Python, YAML, and TOML comment lines become "sections". Setext and multi-line HTML headings do not exist for the gate.

Substring checks:

- `'Use raw bytes.' in '## Intro\n\n<img alt="Use raw bytes." src="x.png">\nUse <em>raw</em> bytes.\n'` → **True**.
- The same check on the round-15 fixture bytes → False.
- `'a – b' in 'x a &#8211; b'` → False.

## Counterexamples (strongest first)

### X1 — HIGH, calibration: row 17 asserts a false negative guarantee ("not exit 2")

Row 17 says: "a submitted rendered quote may return exit 1 `quote_not_contiguous`, not exit 2."

- The "not exit 2" half reads as a guarantee. It is false for the classes row 17 itself lists.
  - **Code member.** Take a Python source with two `# TODO` comment lines and a quote copied raw from it, section `# TODO`. Step 2 passes, and step 3 returns `invalid_manifest`, exit 2 (`:261-263`).
  - **Commit object.** A raw zlib git object is not UTF-8, so it gets exit 2 at `:289-293`. This is conditional on the carrier; `git cat-file -p` text would not trigger it.
  - **Rendered quote.** Exit 2 can coexist with any quote whenever the same manifest trips a pre-check. Exit is per manifest (`:97-100`, `:279-293`).
- Row 17 names one outcome and leaves out the rest:
  - **Exit 0 (false green).** In the alt-attribute case above, a rendered markup-spanning quote also occurs raw in the same section, so the gate returns clean. The green is about a different occurrence.
  - **Exit 1 `quote_location_mismatch` "section not found".** This is the usual outcome for Java members, JSON, and most command output, because they have no ATX lines (`:264-266`). It is not `quote_not_contiguous`.
  - **Exit 0 for a code member.** A Python line under a `# comment` heading grades clean.
- Impact: calibration. A reader learns a wrong outcome map for the exact inputs the row is about.
- **Smallest safe correction:** make the row outcome-agnostic (wording below).

### X2 — HIGH, calibration/hidden regression: supersedes cell `16` silently drops row 16's still-valid obligations

Lane convention:

- `QUALITY.md:4-5`: "A criterion is replaced by a new row naming the row it supersedes."
- `awk` column listing: row 15's cell is `14`, a full replacement (#14's universal was disproved). Row 10's cell is `sharpens 8`, a partial one.
- So a bare `16` reads as full replacement of #16.

Row 16 obligations missing from row 17:

| row 16 obligation | in row 17? |
|---|---|
| "never splice wording" | no |
| "[never] reuse a locator from a different rendering" (the S018 lesson) | no |
| "retain the registered `quote-fidelity` manifest and verdict" | no |
| "an absent or misplaced quote is rejected" | no |
| "exit 2 is unevaluable, never clean" | no |

Row 17 says "still require contiguous located passages", which covers splicing only implicitly. Row 16 is the only home of the other four rules. Under full-replacement reading they lapse.

- Impact: calibration (a weaker admission bar). Depth also suffers: the S018 wrong-rendering locator lesson is lost.
- **Correction:** change the cell to `sharpens 16`, the row-10 precedent. Or carry the five clauses into row 17. Option 1 is smaller.

### X3 — MEDIUM, calibration: no disposition when the policy is violated

"must not be submitted" is discipline only, with no enforcement point (concurs with ReviewManualRoute F5). Row 17 never says what a verdict on such a submission means.

- Exit 1 on a faithful rendered quote is not evidence the quote is wrong. `BoundaryFixtures.md:114-115` concedes it is indistinguishable from a splice.
- Exit 0 on a code member is not admission evidence.
- "Green raw checks prove only…" covers only half of this.
- **Correction:** add one clause: the verdict on such an input "is void as admission or rejection evidence; only the manual check under #1 counts".

### X4 — MEDIUM, depth: "heading-structured" is not tied to the gate's parser

The gate recognizes only ATX and single-line HTML h1–h6 (`:24-32`, `:75-76`). As shown above, code comment lines count as headings and setext or multi-line HTML headings do not.

- "heading-structured raw UTF-8" therefore admits a Python file by accident.
- It also misdescribes a setext Markdown capture as gradeable; every selector would hit "section not found".
- **Correction:** "Markdown ATX or single-line HTML h1–h6 headings as defined in the script docstring".

### X5 — MEDIUM, calibration: "spanning markup" misses entities and is ambiguous for raw-tag quotes

- **Entities.** `&#8211;` renders as `–` and raw membership is False. Round-14 `w1/AttackQuoteGate.md:35` records the real S018 heading `Appendix &#8211; A`. Character references are not "markup" in ordinary reading.
- **Raw-tag quotes.** A raw-copied quote that contains tags literally "spans markup", yet it is the gate's supported positive case. Examples: `raw-accepted.json` in the round-15 fixtures, and ReviewManualRoute F3.
- **Correction:** "rendered quotations whose raw bytes contain markup or character references" (this classifies by the form submitted).

### X6 — MEDIUM, calibration: sibling proposals would enforce the false guarantee or contradict themselves

- **False guarantee.** ReviewManualRoute draft row (§4.1 item 2 and the quoted draft) says "exit 2 is never produced for them". Its A4 acceptance check requires that phrase "or equivalent exit-2 negation".
  - Its own F4 (`ReviewManualRoute.md:73`) says code with `# ` lines can produce duplicate-heading `invalid_manifest` exit 2.
  - So the acceptance check would certify a statement its own finding refutes. Drop the negation from A4.
- **Self-contradiction.** Its A4 also requires `grep -c "does not grade" corpus/QUALITY.md` → 0. Its A3 requires row 16 to stay byte-identical, and row 16 contains "does not grade" (`QUALITY.md:26`). Both cannot pass. Scope A4 to row 17 only.
- **Overgeneralization.** `BoundaryFixtures.md:10-12` says a rendered sentence "is rejected even when it is the correct reading". That holds only when the rendered form does not also occur raw (see X1's exit-0 case).
  - The synthetic fixture itself is honest: `raw-source.md` sha256 `2e80083b7567beaf119463cee31eb617a02d3ab7887bce8441baf43150118270` contains no raw `Use raw bytes.`.
  - Generalizing from it must say "in this fixture".

### X7 — LOW, calibration: registry row still reads as if exit 2 covers "invalid input" broadly

`SKILL.md:450` describes the exits as "1 failed (quote absent/mislocated/too long), 2 could-not-evaluate (invalid input or source digest mismatch)".

- "invalid input" can be read as covering unsupported representations.
- The registry row carries no manual-only pointer.
- The non-UTF-8 trigger is absent from the docstring FINDINGS list (`:42` lists only malformed manifest, duplicate heading, unsafe path), so row 17's "documented malformed/tampered inputs" is only partly documented.
- Pin check: `pointer-table.json` pins SKILL rows by content anchor only (`:108-111`, `:440-450`), and no anchor needle is on the quote-fidelity row. A same-line edit is therefore pin-neutral (this is an [INFERENCE] about the probe, not a probe run).
- **Correction (optional, same line):**
  - Change "invalid input" to "malformed manifest, unsafe path, non-UTF-8 source, duplicate selected heading".
  - Append: "no representation classifier; manual-only inputs per QUALITY #17 are never submitted".

### X8 — LANDING PRECONDITION: row 17's "why" cell does not resolve yet

Row 17 cites `corpus/lessons/round-15.md`, "Mistakes and Gate". That file does not exist in the worktree: the `ls corpus/lessons` filter shows only `round-14*.md`.

Unless L1 lands it, with those headings, in the same commit, row 17 violates QUALITY #1 on arrival. This is the same class as round-14 `w1/AttackNoHarm.md:47` (A5).

## Not attacked / survives

- **No exit-2 classifier is claimed.** Row 17's sentences "The script does not detect unsupported representation" and "Exit 2 … never a general manual-review classifier" are correct (`:78`, `:97-100`, `:194-208`).
- **No implementation change.** Gate bytes are untouched (worktree diff lists only `corpus/QUALITY.md`, the r14 knowledge entry, and `corpus/lessons/round-14.md`).
- **Fixture expectations are consistent with the code path.** BoundaryFixtures' derived raw 0 / rendered 1 `quote_not_contiguous@rendered-text` matches `:252-258`. The fixture sha256 values I computed match `BoundaryFixtures.md:20-22`.
- **measure.py stays satisfied.** `measure.py:25-26,93-95` needs `^| 17 |` plus "must not be submitted" (case-insensitive). Every correction below keeps both.

## Recommended honest row 17 (drop-in, keeps measure markers)

> | 17 | New REA research Gate quotations still require contiguous located passages. Only a captured raw UTF-8 excerpt with Markdown ATX or single-line HTML h1–h6 headings (script docstring), quoted byte-for-byte, may be submitted as machine-gradeable to `quote-fidelity`. Code members, commit objects, JSON, command output, and rendered quotations whose raw bytes carry markup or character references must not be submitted as machine-gradeable; they require the appropriate manual source check under #1. The script has no representation classifier. If such an input is submitted anyway, it gets whatever the raw rules yield: exit 0; exit 1 (`quote_not_contiguous`, `quote_location_mismatch` or `quote_too_long`); or exit 2, only through the script's ordinary `invalid_manifest`/`source_tampered` conditions. That verdict is void as admission or rejection evidence. Green raw checks prove only pinned substring/section consistency, not authenticity, completeness, meaning, or held capability. | `corpus/lessons/round-15.md`, Mistakes and Gate; routed defect 2 in `corpus/lessons/round-14-verifier-spotcheck.md` | sharpens 16 |

If L1 keeps a bare `16` in the supersedes cell, it must carry forward these #16 clauses:

- "never splice wording or reuse a locator from a different rendering"
- "retain the registered manifest and verdict"
- "exit 2 is unevaluable, never clean"

## Proposed L1 checks (none run here)

1. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff 9719dd232687f5ee78a4ed323b37f8810e833d10 -- corpus/QUALITY.md`: exactly one added `| 17 |` line, and row 16 byte-identical.
2. Row 17 text check:
   - Must not contain: `not exit 2`, `never produced`, `does not grade`, `detects`.
   - Must contain: `must not be submitted`, `no representation classifier` (or equivalent), and a void-verdict clause.
3. Row 17 supersedes cell is `sharpens 16`. Otherwise, grep row 17 for `splice`, `different rendering`, and `never clean`.
4. `test -f /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-15.md`, and confirm it has `Mistakes` and `Gate` headings in the same commit as row 17.
5. Gate and fixture pins unchanged:
   - `sha256sum .ufo/waves/round-14/tools/quote-fidelity.py` → `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`
   - `sha256sum .ufo/waves/round-14/fixtures/expected.json` → `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf`
6. Boundary controls, run once:
   - `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --manifest "$PWD/.ufo/waves/round-15/boundary-fixtures/raw-accepted.json"` → exit 0.
   - The same with `rendered-rejected.json` → exit 1, `quote_not_contiguous@rendered-text`.
   - Record these as "this fixture", not "rendered quotes fail".
7. Optional discriminator for X1, under `/var/tmp` (non-committed, deleted after). Each case would refute X1 if its result differed:
   - Alt-attribute duplicate source, rendered quote → expect exit 0.
   - Python source with two `# TODO` lines, quote copied raw from it, section `# TODO` → expect exit 2 `invalid_manifest`.
   - JSON source, raw quote → expect exit 1 `quote_location_mismatch`.
8. Existing `--selftest` (28/28) and `--frozen` (7 matched), plus `measure.py <after-rev>`, which should give `C2_quality_row17_manual_only_wording=1` and `C2_round14_lesson_correction_marker=1`.

## Limits

- All outcome claims are derived from reading the gate's control flow, plus regex and substring checks I reproduced in memory. None is gate output.
- Gate lines `:299-836` were read only through grep hits, apart from the ranges listed above.
- The X1 commit-object exit-2 path depends on the carrier (raw zlib object versus `cat-file -p` text).
- The X7 pin neutrality is an inference from the pointer-table entries, not a probe run.
- The "full vs partial supersession" convention in X2 is inferred from the two in-file precedents (rows 10 and 15); it is not a stated rule.
