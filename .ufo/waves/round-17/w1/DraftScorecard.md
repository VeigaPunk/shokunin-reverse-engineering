# DraftScorecard — w1 report (author-side advisory seat `KaidokuR17.DraftScorecard-3`)

Deliverable: `.ufo/waves/round-17/w1/draft-scorecard.md` (new file, slots only for numbers and outcome verdicts). Only this report and that draft were written. No `SCORECARD.md`, `LOG.md`, `QUALITY`, `SKILL`, lesson, knowledge, or verifier file was edited. No commit, no push. No REA analyze/search/decompile, no Ghidra, no carrier execution. No tools installed or updated. `git status` at baseline: only `?? .ufo/waves/round-17/`.

## Axes and lane
- Claims (`.ufo/waves/round-17/claims.json`): C1 calibration (R16-PROVENANCE, R16-INVOCATION, QUALITY #19); C2 depth (Go carrier diagnostics, capability acquisition).
- Calibration is tied-lowest (`claims.json` C1 `why_this_axis`). Capability entry requires a demonstrated run (`AXES.md:57-63`).

## Findings (observation unless marked [INFERENCE])

1. **The r16 scorecard section does not contain the R16-PROVENANCE wording.** `SCORECARD.md:2294-2348` (baseline) has no "unchanged during", "stable throughout", or equivalent. Repo grep for the sweep phrases and their variants found the sentences only in `corpus/lessons/round-16.md:154`, `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95`, `LOG.md:2012` ("remain unchanged across execution"), and the boolean at `.ufo/waves/round-16/verification.json:419`. The spotcheck's claim that "the scorecard say[s]" the same thing (`corpus/lessons/round-16-verifier-spotcheck.md:183`) is therefore not matched at baseline. The draft records this negative rather than inventing a scorecard correction. L1 must decide whether a negative record is acceptable for the "r16 scorecard wording" item in the claim.

2. **`temporal-sweep.py` as specified will under-count.** `contract.md:90-96` restricts sites to LOG.md, SCORECARD.md, `corpus/lessons/round-16.md`, SKILL.md and `verification.json`, and the regex at `contract.md:93` misses the LOG phrasing at `LOG.md:2012`. Against the baseline, the regex yields 2 in-scope sites (`lessons/round-16.md:154`, `verification.json:419`). The true in-scope count is 3, and the knowledge sentence at `corpus/knowledge/2026-10-20-r16-go-selection-preview.md:95` is outside scope entirely. [INFERENCE from regex and scope reading; not executed — the tool does not exist yet.] Recommend L1 add `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` and the "across execution" variant to the sweep before C1's "every statement" claim can be checked.

3. **Self-match hazard for the correction.** Any site file (SCORECARD.md, LOG.md) that quotes the sweep phrases verbatim creates a new unqualified site. The draft paraphrases and never quotes the regex strings or the boolean key. Only the path-bearing `R16-PROVENANCE:` lines name the sites, which is what `contract.md:94` requires for `corrected`. [INFERENCE: the sweep's "corrected" rule is line-based and path-based.]

4. **Verification facts behind the correction.** `verification.json` has one timestamp, `executed_at_utc` at `:4` (`2026-10-20T08:36:33Z`); `producer_and_fixture_sha256` at `:397` has 20 entries (counted); `pins_unchanged_during_run: true` at `:419`. There are no before/after maps and no per-command hashes, which matches the spotcheck's description at `corpus/lessons/round-16-verifier-spotcheck.md:183`.

5. **Capability table count is ambiguous.** The claim's "capability rows 4 (+r13/r14 appended)" (`claims.json` C2 `falsifiable_before_after`) is not literally true of the main table. The main `## Capabilities` table has 4 rows at `SCORECARD.md:617-622`. The round-13 row is in a round sub-table at `SCORECARD.md:2135`, and the round-14 row at `SCORECARD.md:2207`. Neither appears in the main table. L1 must decide whether r13/r14 are appended to the main table (a move outside this claim) or the baseline count is reported as "4 main + 2 sub-table". The draft uses a slot.

6. **Stagnation counter is not recorded through r16.** The last explicit counter is "Round 3 … (3/10)" at `SCORECARD.md:1500`. `SCORECARD.md:2315` says the window "remains 10" without a count. The draft leaves `{{stagnation_before}}` as a slot. L1 must reconstruct it from the full history before C2 can claim a reset.

7. **SKILL registry variant.** `SKILL.md:448` (citation-drift row) shows `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . …` without `-I`, and the row does not carry "unexercised". This matches the spotcheck's R16-INVOCATION route at `corpus/lessons/round-16-verifier-spotcheck.md:184`. [Observation of the baseline text; the audit's classification is not run.]

8. **QUALITY row.** `corpus/QUALITY.md` has criteria 1–18 (row 18 at `:28`); no row 19 exists yet. Presence 0→1 is the right supplemental for C1(c).

9. **Draft shape.** The draft follows the r16 shape exactly: heading, baseline, measured revision, pointers, the claim/axis table with proxy / supplemental / verdict columns, the coverage/operability/freshness/adjacency rows, the "not expertise scores" line, the named correction, the executed-controls list, the learning-trend line and the planned line. The capability row is conditional and marked not entered.

## Limits
- Nothing was measured. Every number is a slot. The sweep, invocation audit, pin tool, and `measure.py` do not exist at baseline; the draft references them by contract name only.
- Verdict words are slots as well, because the outcome is unknown until the runs complete.
- `AXES.md` lines were read at `/home/vgpnk/Projects/shokunin/AXES.md:57-72`; the fleet-root `SCORECARD.md` was grepped by mistake once (wrong root), and its results were discarded. Every anchor in this report was re-checked against `kaidoku-shokunin/`.
- Peers were running concurrently (`LOG` scribe, other reviewers). Any L1 integration must re-verify anchors at the integration baseline.

## Tooling record
None. No install, update, or upgrade was performed by this seat.

## Artifacts
- `.ufo/waves/round-17/w1/draft-scorecard.md` (draft)
- `.ufo/waves/round-17/w1/DraftScorecard.md` (this report)

Routing: nothing routed to KaidokuR17 beyond this report; no blockers.
