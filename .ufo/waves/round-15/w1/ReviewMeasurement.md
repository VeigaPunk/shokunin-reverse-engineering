# Round 15 — ReviewMeasurement (planned counts as bounded presence/range proxies)

- Lane: `KaidokuR15.ReviewMeasurement` (leaf; no subagent dispatch)
- Scope: planned round-15 counts; old measure script `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measure.py` (read only). New half-written scripts (round-15 `measure.py`, `snapshot-inventory.py`) were not present/inspected.
- Baseline: `9719dd232687f5ee78a4ed323b37f8810e833d10` (HEAD, `round-14 verifier spot-check`), confirmed by `git cat-file -t` = commit.
- Worktree observed (uncommitted, other seats): `M corpus/QUALITY.md` (+1), `M corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` (+11), `M corpus/lessons/round-14.md` (+17), `?? .ufo/waves/round-15/`. Numstat deletions are 0 for all three files.
- Executed: read-only git object reads (`git show`, `git ls-tree`, `git cat-file`, `git diff --numstat`/`--quiet`), grep/awk field counts, `sha256sum` of three pinned files. NOT executed: `measure.py`, selftest, quote-fidelity gate, census validator, snapshot inventory, any test/build/lint.
- Tools installed or upgraded: none. Used pre-existing git, grep, awk, sha256sum.

## 1. Findings by severity

### High

**H1 — The "after" state is unmeasurable until a commit exists; reusing HEAD silently reports no change.**
The old `measure.py` (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measure.py:10-15`) reads only `git rev-parse <rev>`, `git show <rev>:path`, and `git ls-tree <rev>`. It has no worktree mode. The baseline is currently HEAD, and all round-15 edits are uncommitted. Since the contract forbids commits for seats, an un-committed after would measure `9719dd2` again and show before=after everywhere. Proposed: L1 commits the lane work once, then measures that work commit. If a records-only commit follows (as in round 14: `3e99fbd` measured, `9d4e511` recorded), measure the work commit and prove the corpus tree is unchanged between them.

**H2 — Reusing the round-14 script or the round-14 `before.json` gives a false before. Baseline is already saturated for the old checks.**
Observed at `9719dd2` (not `767adaf`, the revision behind `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/before.json`):
- `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` is in the tree, so the old C1 check (hard-coded `:22`) returns 1. Round-14 before was 0.
- `.ufo/waves/round-14/tools/quote-fidelity.py` is in the tree, so the old C2-instrument check (`:23`) returns 1.
- `grep -c quote-fidelity` on `corpus/QUALITY.md` at `9719dd2` = 1, so the old C2-criterion substring check (`:24`) returns 1.
Consequence: a reused script reports 1→1 for every old observable, which is a non-change. The round-15 before values must be recomputed at `9719dd2`, and the round-15 checks must use round-15 names. The old script's hard-coded round-14 paths cannot be reused.

**H3 — Coverage-map integration gap: a new knowledge file lowers the coverage proxy unless a map token is added.**
The old script counts `mapped` only from the `## Coverage map` section (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md:11-69`). The `## Knowledge` section (`:70-154`) does not count. Round-15 adds one knowledge file, so `knowledge_files` goes 92→93 (observed 92 at baseline). Unless a token for `2026-10-20-r15-go-snapshot-inventory` is added inside lines 11–69, the result is `missing=[2026-10-20-r15-go-snapshot-inventory]` and `coverage_score = round(10*92/93, 2) = 9.89` (recipe A, `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SCORECARD.md:118-121`). That drop is an index-integrity artifact, not a domain regression. No seat owns `corpus/README.md` (spec contract: corpus not assigned), so L1 must add the row. Mentioning the file only in the Knowledge section is not enough for this measure.

**H4 — No score inflation is available, and no numeric proxy can express C1 or C2. Treat "tie at 10" as zero headroom, not evidence.**
- `depth_score` = `10*resolved/rule_blocks` over SKILL.md craft rules only (`SCORECARD.md:103-122`). Observed 17/17 at `767adaf` and `3e99fbd` (round-14 before/after); SKILL.md is not in the worktree diff. So depth stays 10.00 by construction. C1 (a new knowledge entry) cannot move this proxy.
- `coverage_score` stays 10.00 only if the new file is mapped (H3).
- `calibration` is the frozen rubric recipe B (`SCORECARD.md:126-142`), which round 15 does not run. Its only numeric value is the historical `0 → 10` (`SCORECARD.md:25`). C2 (quote-gate criterion, marker) cannot move it.
- All three are clamped at 10.0 by the formula, so no count can raise them. The claim "three owned proxies tie at 10; calibration worked" is a statement about saturation. It is not a ranking, and the choice of "lowest axis" is arbitrary.
Required report wording: "numeric proxies unchanged at 10.0 (presence-only, saturated); C1/C2 evidence = named presence/range observables below." Do not edit SCORECARD numbers.

### Medium

**M1 — C1 "tool existence" is not "one reproducible inventory".**
`snapshot-inventory.py` existence (planned 0→1) proves a file, not a result. The C1 claim requires one reproducible inventory. Independently checkable: (a) the inventory JSON output is committed as an artifact (count 0→1; currently no such file), and (b) two invocations on the same installed root produce identical `sha256sum` output. Neither is in the planned counts; L1 must add both or narrow the claim to "tool present, output not yet captured."

**M2 — C2 presence check is whole-file and cannot see supersession or dangling citations.**
Observed:
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:27` (row 17) contains `must not be submitted`. Baseline `git show 9719dd2:corpus/QUALITY.md | grep -c "must not be submitted"` = 0. Worktree = 1. Only row 17 matches, so this observable is correctly 0→1 as a whole-file count. The old code's `in` test is case-sensitive; the spec says case-insensitive, so use a case-insensitive check.
- Row 16 (`:26`) is byte-identical to baseline (numstat 0 deletions). Row 17 says "Supersedes #16's ambiguous manual-only boundary", but row 16 still states the boundary. Supersession is textual only; the count cannot detect contradiction.
- Row 17's evidence cell cites `corpus/lessons/round-15.md`. At `9719dd2`, `git cat-file -e` finds no such file (observed absent). No planned count checks this path resolves. It must exist at the measured commit.
- Row 17 documents exit behavior: a rendered quote "may return exit 1 `quote_not_contiguous`, not exit 2" (observed text). That is the documented limit the spec asks for. Gate code is unchanged (H-gate pins below). The presence count does not prove the documentation matches the gate's behavior; that needs the gate's existing selftest result, which the lane does not run.

**M3 — Correction marker presence (0→1) does not measure adequacy of "qualify the advisory pointer".**
- Exact heading `## Round-15 correction — virtual-dispatch advisory` at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md:144`. Baseline count = 0 (observed); worktree exact-line count = 1 (observed). Byte-exact: the separator is U+2014 em dash; an ASCII hyphen would fail silently.
- The knowledge entry also mentions the marker (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:116`), and a qualifier was appended at `:110`. A whole-file substring count of the marker would count both, so count headings per file.
- Routed defect 1 asks to "qualify the advisory pointer". Round-14 lesson pointers to `ReviewGoInference.md` remain unqualified inline at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-14.md:18` and `:76` (observed; numstat 0 deletions, so these lines are byte-identical to baseline). The correction is appended at `:144`, not beside the pointers. Count: qualified-inline pointers in the lesson = 0 of 2. L1 must decide whether an appended correction satisfies "qualify the pointer" (lane intent says append-only). The count cannot decide this.
- Filed advisory bytes: `git diff --quiet 9719dd2 -- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/ReviewGoInference.md` passes (observed "unchanged"). This is an exact, independent check and should be part of the after measure.

**M4 — Gate-unchanged is measurable by pins; the old script does not check it.**
Observed at `9719dd2` and in the worktree (identical):
- `.ufo/waves/round-14/tools/quote-fidelity.py` `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8`
- `.ufo/waves/round-14/fixtures/expected.json` `ef3714bbb77df1f03db0de325f6c49ea1a8bbf66a1fdeecdd2e8bb3d5474cadf`
- `.ufo/waves/round-14/measure.py` `ee546111cb19e70eae63634f0795325465d58d3f3d0e098cbafc1fdb0c4dd2ab`
These match `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/measurement-pins.json`. Independent after-check: `git diff --quiet <baseline> <after> -- .ufo/waves/round-14/tools .ufo/waves/round-14/fixtures .ufo/waves/round-14/measure.py` plus the three sha pins. The old count `tool in paths` cannot detect edits to the file.

**M5 — The range/citation proxy regex does not cover the new citations; a reused regex passes vacuously.**
SCORECARD recipe A resolves only `corpus/knowledge/<name>.md:<range>` (`SCORECARD.md:105`). The round-15 correction and QUALITY row 17 cite `corpus/lessons/...`, `.ufo/waves/round-14/w1/...:57-61`, and `corpus/README.md`-style paths. Recipe A would count those as zero citations. A range-resolution count is only meaningful if its path pattern is fixed before measurement. Proposed pattern, defined in advance: any token matching `(corpus|\.ufo)/[A-Za-z0-9._/-]+\.(md|json|py)(:\d+(-\d+)?)?`, resolved against the measured commit (path exists; `1 <= first <= last <= line_count`). Report N cited / N resolved; this is a range-existence proxy, not semantic support.

**M6 — Old script structure: fragile and not reusable.**
- `ROOT = Path(__file__).resolve().parents[3]` (`measure.py:9`) requires the script to live at depth `<kaidoku>/.ufo/waves/<round>/measure.py`. Correct for round-15 placement; breaks if copied elsewhere.
- `sys.argv[1]` required; no before/after pairing, no pins, and no input hashes in its output (only the revision).
- Hard-coded round-14 names (`:22-24`).
- `ls-tree` without `-z`: git quotes unusual paths. Observed: 0 quoted paths in the tracked tree at baseline (`grep -c '"'` = 0), and 0 non-`[A-Za-z0-9./_-]` names under `corpus/knowledge`. Low current risk; use `-z` anyway.

### Low

**L1 — `mapped` is lexical.** Any mention of a token inside the coverage-map section counts as mapped, including prose (e.g., the r14 entry is mentioned twice at baseline, lines 35 and 140 of `corpus/README.md`). "Mapped" therefore proves index mention, not row correctness. Already stated as a limit in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-14/w1/BaselineMeasures.md` §7.

**L2 — Column indices are correct now, but fragile.** `r[4]` = tier and `r[8]` = status (split on `|`, leading empty field). Observed: all 22 `^| S\d{3,}` rows have 13 awk fields (11 cells + 2 empty), so no cell contains `|`. Any future `|` in a cell silently shifts columns. Count rows with the expected field count and assert.

**L3 — Craft hash is boundary-sensitive.** The lesson records a sha of the extracted craft text; its reviewer got a different hash with a different extraction boundary. Do not use it as a before/after identity check.

**L4 — Sources.** No `SOURCES.md` change in the worktree (observed). Round 14 changed six `used-by` cells only (lesson `round-14-verifier-spotcheck.md`). A "rows/tiers/statuses unchanged" check must exclude column 11 (`used-by`), or it will fail on permitted edits and pass on non-permitted ones if the excluded column is not compared separately.

## 2. Observed values (read-only)

| Observable | Baseline `9719dd2` | Worktree (uncommitted) | Command / limit |
|---|---:|---:|---|
| Knowledge `.md` in tree | 92 (observed) | not counted | `git ls-tree -r --name-only 9719dd2 -- corpus/knowledge \| grep -c '\.md$'`; mapping not re-counted here |
| r15 knowledge entry present | 0 | 0 | not created yet |
| Round-14 knowledge entry present | 1 | 1 | presence only |
| `quote-fidelity` substring in QUALITY | 1 | 1 | old check; saturated, cannot register round 15 |
| `must not be submitted` in QUALITY (whole file) | 0 | 1 | row 17 only; not row-scoped |
| `## Round-15 correction — virtual-dispatch advisory` heading in `corpus/lessons/round-14.md` | 0 | 1 | exact heading line; em dash U+2014 |
| Marker substring in knowledge entry | 0 | 1 | reference only, not heading |
| Numstat deletions (QUALITY / lesson r14 / knowledge r14) | — | 0 / 0 / 0 | append-only evidence |
| ReviewGoInference filed bytes | unchanged | unchanged | `git diff --quiet` |
| Gate pins (3 files) | match `measurement-pins.json` | match | sha256 |
| SOURCES rows (ID shape, 13 awk fields) | 22 | 22 (not modified) | `^\| S[0-9]{3,}` |
| Tiers / statuses (historical, 767adaf) | A20/B1/C1; mined21/rejected1 | not recomputed | from `before.json`/`after.json`; not re-derived at 9719dd2 here |
| SCORECARD coverage / depth | 10.0 / 10.0 | 10.0 / 10.0 | recipe A; historical (round-14 measure at `3e99fbd`) |
| Coverage-map tokens of r14 entry | 2 lines (35, 140) | not changed | lexical presence |
| Round-15 lesson path cited by QUALITY row 17 | absent | absent | dangling until L1 writes it |

## 3. Proposed before/after (independently checkable; L1 runs, I did not)

| # | Observable | Before (rev `9719dd2`) | After (L1 work commit) | Pass condition | Limit |
|---|---|---|---|---|---|
| 1 | R15 knowledge entry present | 0 | 1 | `git cat-file -e <after>:corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md` | presence only |
| 2 | Knowledge files / mapped / missing / dangling | 92 / [BASE-MAP] / [] / [] | 93 / 93 / [] / [] | README coverage-map section contains the new token | lexical; row not checked |
| 3 | `coverage_score` (recipe A) | 10.0 | 10.0 | equals 10*mapped/files | saturated; a drop to 9.89 = H3 failure |
| 4 | `depth_score` (recipe A) | 10.0 | 10.0 | SKILL.md unchanged at after (`git diff --quiet`) | C1 not measurable by this proxy |
| 5 | Snapshot inventory tool present | 0 | 1 | file exists at `.ufo/waves/round-15/snapshot-inventory.py` | presence only |
| 6 | Inventory output artifact committed | 0 | 1 | committed JSON; two runs have identical sha256 | M1 — required for C1's "reproducible inventory" |
| 7 | QUALITY row 17 contains `must not be submitted` (case-insensitive, row-scoped) | 0 | 1 | row whose first cell is `17` matches | presence only; no supersession proof |
| 8 | QUALITY row 16 unchanged | identical | identical | `git show <after>:corpus/QUALITY.md` row 16 == baseline row 16 | textual |
| 9 | Correction heading count in `corpus/lessons/round-14.md` | 0 | 1 | exact line `## Round-15 correction — virtual-dispatch advisory` | U+2014 byte-exact |
| 10 | ReviewGoInference filed bytes | baseline | identical | `git diff --quiet 9719dd2 <after> -- .ufo/waves/round-14/w1/ReviewGoInference.md` | exact |
| 11 | Gate pins unchanged | 3 pins | 3 pins | sha256 equal; `git diff --quiet` on `.ufo/waves/round-14/{tools,fixtures}` and `measure.py` | exact |
| 12 | Append-only (3 edited corpus files) | — | 0 deletions | `git diff --numstat 9719dd2 <after> -- corpus/QUALITY.md corpus/lessons/round-14.md corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` | rule is append-only by lane intent; still permits textual change inside appended text |
| 13 | Registry rows / tiers / statuses | 22 / A20 B1 C1 / mined21 rejected1 | identical | rows ID set equal; cols 4 and 8 equal; col 11 differences listed separately | counts only |
| 14 | Citation range-resolution (new artifacts) | — | N/N | M5 pattern, all paths exist at after and ranges in bounds | range existence, not support |
| 15 | QUALITY row 17 evidence path `corpus/lessons/round-15.md` | absent | present | `git cat-file -e <after>:corpus/lessons/round-15.md` | exists only |

## 4. Predicted after values

- [INFERENCE] Knowledge 93, mapped 93, missing [], dangling [] — only if L1 adds the README token (H3). Without it: 92/93, missing 1, coverage 9.89.
- [INFERENCE] Tiers A20/B1/C1, statuses mined21/rejected1 — no new rows.
- [INFERENCE] Numeric proxies 10.0 / 10.0 / (calibration not recomputed). Report "unchanged, presence-only."
- Observed (worktree) presence deltas: QUALITY row 17 +1; correction heading +1; knowledge marker mention +1 (reference); no deletions anywhere.

## 5. Limits of this review

- Presence/range proxies only. None of these counts establishes semantic correctness of the entry, the row, or the correction. Source-anchor reading of the substance (S003 `GoRttiMapper.java:380-386`, `GoTypeManager.java:405-455`, the Go snapshot path) belongs to the VirtualLookup/PatchLookup/BaseLookup lanes, not this one.
- I did not run `measure.py`, the quote-fidelity selftest or gate, the census validator, or any inventory. Hash and count observations were read-only inventory; L1 must confirm them.
- The baseline `[BASE-MAP]` value (mapped count at `9719dd2`) was not re-counted here; it is [INFERENCE] from round-14 `after.json` at `3e99fbd` plus the unchanged knowledge tree.
- The baseline tier and status values are historical (round-14 `before.json`/`after.json`), not recomputed at `9719dd2`.
- Worktree observations are a snapshot at review time; other seats may still edit these files.

## 6. Proposed L1 checks (named only; not executed)

1. Commit lane work (no seat commits). Record the work SHA and any records-only SHA; prove corpus tree equality between them.
2. `python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/measure.py <baseline>` and `... <after>`; both before and after must be from the commit, not the worktree. Do not reuse round-14 `before.json`.
3. Add the README coverage-map token for the r15 entry inside `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/README.md:11-69`; confirm missing=[] and dangling=[].
4. Run `snapshot-inventory.py` twice against the installed Ghidra root; compare sha256; commit output.
5. Row-scoped QUALITY check for row 17 (case-insensitive); row 16 byte-identity; `corpus/lessons/round-15.md` exists.
6. Heading-count check for the correction marker; decide whether appended correction satisfies "qualify the advisory pointer" (M3).
7. Pin checks: three sha256 values in `measurement-pins.json`; `git diff --quiet` for `.ufo/waves/round-14/{tools,fixtures}`, `measure.py`, and `ReviewGoInference.md`.
8. Numstat append-only check for the three corpus files.
9. Registry check: rows/IDs equal; cols 4 and 8 equal; col 11 diffs listed.
10. Range-resolution count with the M5 pattern, on the new entry and correction.
11. Scores: report 10.0 / 10.0 / calibration unchanged; do not edit SCORECARD.md numbers.

## 7. Verdict

Planned counts are usable only as bounded presence/range observables measured at committed revisions with round-15 names. They cannot show score improvement (all proxies saturate at 10.0), and reusing round-14 numbers or the old script would report a false before and an unmeasurable after. Blocking items for L1: H1 (commit before measuring), H3 (README map token), and M1 (inventory output must exist before C1 is claimed as "reproducible inventory").
