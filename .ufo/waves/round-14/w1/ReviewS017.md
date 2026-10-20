# ReviewS017 — independent reopen of S017 (View8 README)

Lane: `KaidokuR14.ReviewS017`, leaf reviewer, scope S017 only. No builds, tests, linters, REA target execution, or subagent dispatch. No shared files, registry, lesson, SKILL, or gate code was edited. Access date: 2026-10-20.

## Verdict

1. The round-13 S017 Gate quote is a splice and is **not** a substring of the pinned README bytes. Confirmed.
2. The corrected sentence from the round-13 errata is a contiguous, exact substring of the pinned bytes. Confirmed. Its location is `Usage` → `Command-Line Arguments` → `--normalize` row, raw line 40. The registry anchor `Deterministic Function Names and Mapping CSV` (raw lines 81–107) does **not** contain it.
3. Blocker for C2 (calibration gate): the pinned file has **zero** Markdown `#` headings. Every heading is HTML (`<h1>`–`<h3>`). The gate contract's section rule ("exact Markdown heading text including #") cannot name the section that contains the corrected quote. A passing located case for S017 is therefore not expressible under the current contract without a decision by L1 or the gate owner. I did not decide this.

## Sources opened

| id | location | access | bytes / identity | notes |
|---|---|---|---|---|
| S017 pinned raw README | https://raw.githubusercontent.com/suleram/View8/ef39099b4f5076042173f9113382ebeb0630a56d/README.md | 2026-10-20, `curl` HTTP 200 | 13242 bytes, 283 lines, sha256 `191621cd0f87eb3c7f54d18e0ca128f2d7fffd997b11f83d5b3761c5cc01619b` | Full snapshot NOT retained (custody: public-repo README redistribution, F2). Identity is pinned by URL and sha256 only; short quotes and heading tokens are cited in this report. The read tool's reader view of the same URL showed identical text. |
| S017 commit metadata | https://api.github.com/repos/suleram/View8/commits/ef39099b4f5076042173f9113382ebeb0630a56d | 2026-10-20 | `sha` matches; committer date 2026-07-28T00:34:41Z; message "[FEATURE] While normalizing functions names, produce a mapping file (CSV)" | Only commit metadata; the rest of the tree was not inspected. |
| Registry row S017 | `corpus/SOURCES.md` line 23 | local | — | Anchor: `Requirements`, `Deterministic Function Names and Mapping CSV`, pickle warning. |
| Round-13 Gate and errata | `corpus/lessons/round-13.md` line 44 (Gate row), lines 63–65 (errata), Mistakes row 3 | local | — | Original quote and corrected quote. |
| Round-13 spot-check | `corpus/lessons/round-13-verifier-spotcheck.md` line 13 | local | — | States the reviewer found the S017 splice. |
| Wave contract | `.ufo/waves/round-14/claims.json` | local | — | C2 is calibration; limits say local captured excerpts only. |

Tools: no installs or upgrades. Used system `curl`, `sha256sum`, `grep -F`, `wc`, `file`. The scratch copy in `/tmp` and the draft copy under `w1/ReviewS017-source/` were both removed; no full README copy remains in the repository.

## Raw heading map (pinned file)

| raw line | element | section span used for location |
|---|---|---|
| 5 | `<h2>Requirements</h2>` | 5–17 |
| 18 | `<h2>Usage</h2>` | 18–… |
| 20 | `<h3>Command-Line Arguments</h3>` | 20–65 (next h3 at 66) |
| 66 | `<h3>Basic Usage</h3>` | — |
| 81 | `<h3>Deterministic Function Names and Mapping CSV</h3>` | 81–107 (next h3 at 108) |
| 108 | `<h3>Creating and Processing Serialized Files</h3>` | 108–117 |

## Quote comparison

| item | round-13 Gate quote (as printed) | pinned-bytes result | corrected quote (errata) | pinned-bytes result |
|---|---|---|---|---|
| sentence | "Use --normalize to replace address-derived function names with deterministic names based on parse order." (14 words) | `grep -F`: NOT FOUND in the whole file | "Replace address-derived function identifiers with deterministic names based on parse order." (11 words) | `grep -F`: found once, line 40 |
| raw context | — | Nearest match is line 82: `<p>Use <code>--normalize</code> to replace address-derived function names with deterministic identifiers. To preserve …` | — | Line 40: `<li><code>--normalize</code>: Replace address-derived function identifiers with deterministic names based on parse order.</li>` |
| section of the located text | Registry anchor `Deterministic Function Names and Mapping CSV` | Line 82 is inside that section, but its wording differs after "deterministic" | Errata: `Usage` → `Command-Line Arguments` → `--normalize` row | Line 40 is inside lines 20–65, not inside 81–107 |

Splice mechanics, verified by byte inspection: the round-13 quote's first half ("Use --normalize to replace address-derived function names with deterministic") comes from line 82 in the Deterministic section. Its second half ("names based on parse order.") comes from line 40 in the CLI table. Neither line alone contains the round-13 quote.

Tag-stripping check: if a gate strips HTML tags before matching, line 82 becomes "Use --normalize to replace address-derived function names with deterministic identifiers." The round-13 quote still does not match, because it requires "names based on parse order." So the red result does not depend on the tag policy.

Corrected quote tag check: the quoted span on line 40 contains no tags, so the match is the same with or without tag stripping.

Pickle warning (registry anchor "pickle warning"): "Unpickling data from untrusted sources can execute arbitrary code." is a contiguous substring at raw line 112, section 108–117. Verified by `grep -F`.

## Red-before case (stable)

Use these as the frozen red/green inputs for the gate. The results below are **expected verdicts derived from byte inspection**. The gate was not run.

| case id | source | quote | section | expected verdict |
|---|---|---|---|---|
| S017-R13-SPLICE (red-before) | pinned bytes, sha256 `191621cd…1619b` | round-13 sentence, 14 words | `Deterministic Function Names and Mapping CSV` | `quote_not_contiguous` (text absent from entire file; stable under tag stripping) |
| S017-CORR-WRONG-SECTION (red) | same | corrected sentence, 11 words | `Deterministic Function Names and Mapping CSV` | `quote_location_mismatch` (contiguous, but not inside that section) |
| S017-CORR-LOCATED (green candidate) | same | corrected sentence, 11 words | `<h3>Command-Line Arguments</h3>` | Not expressible under the current contract, because the section rule requires Markdown `#` headings. Blocked until L1 or the gate owner decides the heading grammar. |

Finding IDs were not supplied to me, so none are asserted here.

## Other S017 registry claims checked

- `Requirements` (raw lines 5–17) lists disassembler versions 9.4.146.24, 10.2.154.26, and 11.3.244.8. Nothing in the file mentions V8 14.8. This supports the registry's "does not establish compatibility with V8 14.8" limit.
- The registry phrase "bundled V8 maps" is a paraphrase. The README says "Available versions" (line 13) and says disassemblers are searched for in a `Bin` folder (line 71–72). It does not use the word "bundled". Minor wording issue, not a quote defect.
- The registry phrase "function names repeatable" matches the `--normalize` row (line 40) and the Deterministic section (lines 81–107).

## Residual risk and limits

- Only S017 was reopened. S018 and the other registry rows were not reopened here.
- The commit metadata confirms the pinned SHA and date. The tree and other files at that commit were not inspected.
- The file is HTML-in-`.md`. Any gate that assumes Markdown `#` headings must either support HTML headings or pin a different, documented excerpt form. A normalized copy would not match the pinned bytes, so it cannot replace the raw sha256.
- Expected verdicts above come from `grep -F` on exact bytes. They are not gate output.

## Checks for L1 (not run by me)

- Run `quote-fidelity.py --selftest`, then the frozen S017 manifest with the three cases above, and compare each verdict with the expected verdict in the table.
- Decide the heading grammar for HTML headings before the green S017 case is admitted.
