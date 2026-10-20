# AttackNoHarm: line-shift and harm attack on round-14 integration (critic)

- Seat: `KaidokuR14.AttackNoHarm` (critic, leaf). Judged on: coverage, calibration.
- Baseline: HEAD `767adafb97e2eef6980e2ad873d357e16721c467`. `git status --short` shows only `?? .ufo/waves/round-14/`, so reads of pinned surfaces match HEAD.
- Access date: 2026-10-20. Tools: none installed or upgraded. I used `git`, `sha256sum`, `wc`, `awk`, `sed` and Python file reads only.
- **I did not execute any gate.** I did not run the citation-drift probe, the census, Command A, `measure.py`, `sources-census.sh`, or any selftest. Every predicted finding below is an `[INFERENCE]` from reading the gate code. The measurements `BaselineMeasures.md` reports are that seat's numbers, not mine.

## Axes

- **Coverage:** C1 must land with a Command A map token, and without making another owned proxy worse.
- **Calibration:** C2 must make S017/S018 failable without over-claiming. Its verification must not be able to read clean falsely.
- **No-harm surfaces:** the citation-drift probe (`--strict` findings must stay 0), census v10 PASS, Command A (91/91 → 92/92, depth 17/17), `measure.py`, and the `sources-census` validate step.

## Pinned metadata (observed)

- **Pointer table:** `pointer-table.json` sha256 `7994eec7…789d1` equals `expected.json:12`. The table has 60 `entries`, 5 `quoted` and 8 `exempt`. `expected.json` sha256 is `05c251fb…ac52c`, and the probe's is `e2665074…a36a`.
- **Frozen run:** `expected.json:3-9` pins `frozen_run.revision` `679af5d…`. That is an immutable Git object, so no round-14 commit can change the frozen measurement.
- **Line-pinned (`exact`/`extracted`/`quoted`) citing lines:**
  - SKILL.md: 246, 248, 252, 254.
  - SCORECARD.md: 59, 60, 68, 69, 72, 270, 622, 699, 1338, 1419, 1435.
  - corpus/README.md: 22 (×2), 175 (×3).
  - SHONEN.md: 6, 12.
  - LOG.md: 1012, 1442.
  - PROVINCE.md: 18.
- **Line-pinned targets:**
  - corpus/README.md:138 (from SCORECARD.md:72).
  - corpus/README.md:180 (from SCORECARD.md:69).
  - SCORECARD.md:1216, 850-852, 856+, 908.
  - SKILL.md:81-255. Its needle is rule #13 at SKILL.md:233.
  - PROVINCE.md:88-116.
  - corpus/QUALITY.md:21, 24-25 and 25.
- **Census v10 SCOPE (`c1-census-v10.py:254-277`):**
  - SKILL.md 10-20.
  - SCORECARD.md up to the DATED row 1759-2122.
  - FRONTIER rows keyed by line at PROVINCE.md 75-162, plus an unregistered-bullet guard (`:467-469`).
- **Command A (`SCORECARD.md:101-104`):** counts map tokens **only inside `## Coverage map`**. Rule blocks are `- **` bullets in the craft section, and a rule resolves only through `corpus/knowledge/…md[:N[-M]]` refs.
- **`measure.py:22-24`:** requires the gate at exactly `.ufo/waves/round-14/tools/quote-fidelity.py` in `git ls-tree`. It also requires the literal `quote-fidelity` in QUALITY.md.

## Counterexamples (strongest first)

| # | Proposed or plausible addition | Evidence | Predicted harm `[INFERENCE]` | Axis | Fixable? |
|---|---|---|---|---|---|
| A1 | `SkillRuleDraft.candidate.md:2-3` places a new `## Go symbol-recovery…` section "after Error patterns … before Queue-drain craft", above SKILL.md:81. The draft body is 22 lines (`:9-30`); with a separator it is 23. | The probe reads the citing line at a fixed number and runs `re.search(pattern, citing_line)`. No match gives `citation_dead` (`citation-drift-probe.py:196,212-218`). | `skill-rule14-cr2-identity`, `-verdict-identities`, `-entry-recheck` and `-log-fresh-identity` all go `citation_dead`. At ≥23 lines, rule #13 moves 233→256, past `SHONEN.md:6`'s `SKILL.md:81-255`, which adds `shonen-skill-range`. That is 4–5 findings. SHONEN:14 "81-314" also goes stale. | no-harm, calibration | Yes. Place it after SKILL.md:318 (before `## Config custody`, which is outside the craft split, so rule_blocks stays 17) or at EOF. |
| A2 | Any README row insert for C1: a Coverage-map row (11-68), a Knowledge-table row (72-153), or a Lessons-index row for `round-14` (157-168). | This repeats round-12 mistake #9 exactly (`corpus/lessons/round-12.md:20`). | `sc69-readme-177` (target :180), `sc72-readme-nitrow` (target :138) and `readme175-sc1217/-r7range/-r8e2` (citing :175) go dead: 5 findings. An insert above :22 adds `readme22-r7range/-r8range`: 7 findings. SCORECARD:69/72 are append-only and cannot be re-pointed. | coverage (forces a revert), no-harm | Yes. Append the token on the same physical line of an existing Coverage-map row (precedent `SCORECARD.md:1042-1043`). No Knowledge-table or Lessons row: the README Knowledge table already has zero `2026-10-19` rows, so map-only is precedent. |
| A3 | Omitting the map token to avoid A2. | Command A's `files - mapped`. | 91/92 gives coverage 9.89 (<10.0). `measure.py` would show `missing:[2026-10-20-r14-go-version-diagnosis]`. | coverage | Yes, per the A2 fix. The stem matches `2026-10-\d{2}-[a-z0-9-]+`. |
| A4 | QUALITY row 16 as drafted (`QuoteCriterionDraft.candidate.md:12`): "A quote-bearing claim is admitted only when the registered `quote-fidelity` gate exits 0…". | The gate contract needs Markdown `#` headings (the dispatch `Gate interface`). C1's draft quotes Java members, a GitHub commit and README text (`GoEntryDraft.candidate.md:5,27-33`). The draft itself says View8 and Check Point have no Markdown headings (`:49`). | Under C2's own row, C1's quotes are not gradeable (exit 2 or no manifest), so **C1 becomes inadmissible**. It also applies to every future code, JSON or HTML quote. "Rendered line numbers are never a locator" can be read against the lane's line-anchored citation norm, which the probe enforces. | coverage, calibration | Yes. Scope the row to quotes from heading-structured prose captured as a pinned Markdown excerpt, or to SOURCES/lesson Gate quote tables. State that member/line-anchored code quotes stay under #1. |
| A5 | Row 16's "why" cites `.ufo/waves/kaika-w3/kaidoku-r13-review.md`. | `ls` shows it is absent in the lane repo and present only at `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/`. `git ls-files` does not match it. | A non-resolvable lesson citation inside QUALITY, which violates QUALITY #1 at the moment it lands. | calibration | Cite `corpus/lessons/round-13-verifier-spotcheck.md`, which is lane-resident and names that fleet file, or use the absolute fleet path. |
| A6 | A new craft rule (`- **…` inside SKILL.md 81-318) that cites only lessons, the gate or QUALITY. | Command A: `valid = bool(refs)` over `corpus/knowledge/` refs only (`SCORECARD.md:105-117`). | rule_blocks 17→18 with 17 resolved gives depth 10.0→9.44. SHONEN box-1 "17/17" goes stale. | depth (owned; harm) | Yes. Don't add a craft rule, or cite real `corpus/knowledge/…:N-M` support and co-land a SHONEN EOF correction (`SHONEN.md:14` precedent). |
| A7 | A records append to SCORECARD containing `REA 6.5.0`, `rea-agents@x.y.z`, or `/abs/…json:N`. | Census rule: appended text "must be locus-free in this instrument's unit" (`c1-census-v10.py:41-43`). The patterns are `PIN`/`VER`/`PTR` at `:315-317`. Declared SCOPE stops at 2122 and the file is 2175 lines. | An UNDECLARED locus makes census FAIL (exit 1). `go1.26.x` and `12.1.4` do not match `VER`. | no-harm | Keep the round-14 SCORECARD/LOG prose locus-free, using repo-relative paths. |
| A8 | Any edit to `pointer-table.json` (for example grading the C1 entry). | `run_check` compares the table sha against the pin before grading (`citation-drift-probe.py:294-308`). | Without a same-commit re-pin: `pointer_table_tampered`, exit 2. | no-harm | Leave the table unchanged. If L1 extends it, re-pin with the r12 serializer rule (`round-12.md:18`). |
| A9 | A new Go frontier bullet in PROVINCE.md. | FRONTIER rows are line-keyed, plus the unregistered-bullet guard. `prov18-*` pins :18 and SHONEN:12 pins 88-116. | FRONTIER-UNEVALUABLE or a shifted span gives census FAIL. | no-harm | Leave PROVINCE untouched; the claims do not name it. |
| A10 | Verifying before committing, or without `--strict`. | The probe reads `git show <rev>:path` (`:100-109`), so uncommitted edits are invisible. Non-strict mode returns CLEAN despite findings (`:86-87`). Command A and `measure.py` also read Git objects. | **False-clean**: the A1/A2 harms would read exit 0. | calibration | Commit first, then run `--strict --rev <commit>` and require `findings=0`. Run census with `--root` (`round-12.md:21`). |

## Append-only placement that harms no axis (recommended)

- **corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:** a new file. It is not pinned or census-scoped.
- **corpus/README.md:** append the C1 token on the same physical line of an existing Coverage-map row in 23-68.
  - `:35` (the `r4-10` Go-bump row) is the natural fit.
  - Never `:22`, and never a new row in any section. No Lessons-index row for round 14.
- **corpus/QUALITY.md:** append row 16 as the new line 26.
  - Pins at :21, :24-25 and :25 are unaffected. No live pin points at ≥26.
  - The only ≥26 reference is the historical `QUALITY.md:11-24,30-35` at `2026-10-14-r14-02-final-sweep.md:105`, which was already non-current before this round.
  - Apply the A4 and A5 corrections first. Keep the literal `quote-fidelity`. Never rewrite rows 1-15 (`QUALITY.md:4-5`).
- **SKILL.md registry:** insert the gate row between :449 and :450 so the table stays contiguous.
  - That shifts only :450-451, which carry no pins.
  - Keep :447-449 byte-identical; they are the anchor needles for three entries.
  - Use the repo-relative command `python3 .ufo/waves/round-14/tools/quote-fidelity.py`. The absolute main-checkout path in the dispatch would mis-measure worktrees.
  - Callsite: the intro at :440-441 enumerates exactly three tools and goes stale with a fourth. Edit it in place without changing its line count, or accept it as a named nit.
- **SKILL.md Go diagnosis table (A1):** if L1 lands it, place it after :318 or at EOF, never above :255.
- **SCORECARD.md, LOG.md:** append at EOF only, locus-free (A7).
- **SHONEN.md:** EOF correction only, and only if A6 adds a rule.
- **corpus/SOURCES.md:** the `RegistryDeltaDraft` same-line `used-by` cell appends cause no line shift, and SOURCES.md is not probe-pinned.
- **Untouched:** PROVINCE.md, root README.md, `pointer-table.json`, `expected.json`. Root README.md is unpinned and no instrument reads it.
- **Co-land in one commit:** the gate file at the exact `measure.py` path, its frozen manifests and expected verdicts, the SKILL registry row, and QUALITY row 16. Row 16 depends on the registered gate for its truth (SKILL rule #16, `SKILL.md:279`).

## Checks L1 should run after integration (none run here)

1. `citation-drift-probe.py --root . --rev <commit> … --strict`; expect `findings=0`.
2. `c1-census-v10.py --root <tree>`; expect PASS 0/0/0/0.
3. Command A at `<commit>`; expect 92/92, 17/17 (or 18/18 if A6 is done correctly).
4. `python3 .ufo/waves/round-14/measure.py <commit>`; expect C1=1, C2 instruments=1, criteria=1, `missing:[]`.
5. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`; expect ok.
6. The quote gate's `--selftest` and its frozen-manifest run.

## Sources opened (2026-10-20; contiguous ≤25-word quotes)

- `.ufo/gates/citation-drift/pointer-table.json`, entry `skill-registry-row` note: "a line number into a file the lane appends to is the defect class rule #11 names"
- `.ufo/gates/citation-drift/citation-drift-probe.py:86-87`: `if not strict: return CLEAN`
- `.ufo/gates/c1-census-v10.py:41-42`: "text appended past the declared bound must be locus-free in this instrument's unit"
- `corpus/lessons/round-12.md:20`: "Line-shifting insert into a pinned file: the work commit `4072ebb` added a lessons-index row inside `corpus/README.md` (above `## Frontier`)"
- `SCORECARD.md:1042-1043`: "line-neutral map-token append (E8's r4 form — same physical line, no row insert)"
- `SHONEN.md:14`: "appended at EOF so the pinned box lines keep their numbers"
- `corpus/QUALITY.md:4-5`: "A criterion is replaced by a new row naming the row it supersedes, never rewritten."
- Also read:
  - SCORECARD.md:56-73, 86-125 and 2118-2175
  - corpus/README.md (full), README.md (full), SKILL.md:240-320 and 436-451
  - corpus/lessons/round-13.md, corpus/lessons/round-13-verifier-spotcheck.md
  - the round-14 claims, `measure.py`, and drafts `SkillRuleDraft`, `QuoteCriterionDraft`, `GoEntryDraft` (:1-33), `RegistryDeltaDraft`, `CoverageGap`, `BaselineMeasures`

## Limitations

- Shift effects are derived from the probe, census and Command A source code, not from execution.
- The final texts of the C1 entry, row 16, and any SKILL addition belong to L1 and may differ from the drafts.
- The A1 count of 4 or 5 depends on the exact number of inserted lines.
- I did not re-verify `BaselineMeasures`' 91/91.
- I flagged A1 to `SkillRuleDraft` and A4/A5 to `QuoteCriterionDraft` by message. I did not edit their files.

## Addendum: A4/A5 re-check of the revised draft (2026-10-20)

I re-read the revised `QuoteCriterionDraft.candidate.md:12`.

- **A4 is resolved in the draft.** Row 16 now covers only "A source quote offered as Gate evidence … from a heading-structured document". It also states that code, commit, JSON and command-output Gate quotes "and all knowledge-entry quotes are outside this criterion and remain under #1". C1 is therefore no longer made inadmissible.
- **A5 is resolved in the draft.** The why-cell cites the lane-resident `corpus/lessons/round-13-verifier-spotcheck.md` and `corpus/lessons/round-13.md`. The fleet review now appears only as an absolute path (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika-w3/kaidoku-r13-review.md`), which resolves. That path ends in `.md`, so census `PTR` does not match it, and QUALITY.md is outside census SCOPE in any case.
- **Residual co-land dependency.** The why-cell still names the planned `corpus/lessons/round-14.md`. Row 16 must land in the same commit as that lesson, the committed gate and the SKILL registry row (SKILL rule #16).
- I ran no gate. The S017/S018 expected verdicts remain hypotheses until L1's frozen run.
