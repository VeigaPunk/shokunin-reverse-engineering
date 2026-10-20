# ScoutTemporalWording — R16-PROVENANCE wording sweep (read-only)

Scope: the six files named in the assignment, at lane HEAD `b563c79`. Question: every statement asserting
pins/files stayed unchanged/stable **during the r16 run**. No edits outside this file; no REA/analyze, no
Ghidra, no carrier execution, no installs. Methods used: shell `grep -nE`, Python 3 stdlib JSON reads, and
read-only `git show` of committed blobs. Labels: **observed** = tool output quoted here; **[INFERENCE]** =
my reading.

## Grep commands and result counts (observed)

1. Contract's proposed pattern (see `.ufo/waves/round-17/contract.md`, `temporal-sweep.py`):
   ```
   grep -nEi 'unchanged during|remained unchanged during|stable throughout|pins_unchanged_during_run' \
     LOG.md SCORECARD.md SKILL.md corpus/lessons/round-16.md \
     .ufo/waves/round-16/verification.json \
     /home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md
   ```
   → **3 hits**: `corpus/lessons/round-16.md:154`, `.ufo/waves/round-16/verification.json:419`,
   fleet report `:60`.
2. Widened time-adverbial sweep (23 matches, 4 relevant):
   ```
   grep -nEi '(unchanged|stable|identical|held|match(es|ed)?|drift|preserved|not modified|no change)[^.]{0,70}(during|throughout|across|execution|window|run)|(during|throughout|across)[^.]{0,50}(unchanged|stable|identical|held|preserved)' \
     LOG.md SCORECARD.md SKILL.md corpus/lessons/round-16.md \
     /home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md
   ```
   → adds `LOG.md:2012`; all other hits are earlier-round custody/invocation lines or axis verdicts.
3. Precise recovery regex — returns exactly the four core sites, no false positives:
   ```
   grep -nEi 'unchanged (during|across|throughout)|pins_unchanged_during_run' \
     LOG.md SCORECARD.md SKILL.md corpus/lessons/round-16.md \
     .ufo/waves/round-16/verification.json \
     /home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md
   ```

## Core findings — four sites assert during-run stability (observed)

| # | Site | Exact text | Assertion type |
|---|---|---|---|
| 1 | `corpus/lessons/round-16.md:154` | `All producer/fixture pins remained unchanged during execution.` | Strongest prose form; "All" + "during execution" |
| 2 | `.ufo/waves/round-16/verification.json:419` | `"pins_unchanged_during_run": true,` | Machine-readable boolean keyed to during-run stability |
| 3 | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60` | second sentence: `Producer/input hashes stayed unchanged during execution.` | Prose, same claim |
| 4 | `LOG.md:2012` | `parameter. Producer/fixture hashes remain unchanged across execution.` | Prose variant ("across", not "during") |

Site 2's supporting map is `producer_and_fixture_sha256` at `verification.json:397-418`; the boolean is
`:419`. Sites 1/3/4 refer to that same 20-entry map.

## Evidence shape at that revision (observed)

- Top-level JSON keys are exactly `baseline`, `commands`, `evidence_scope`, `executed_at_utc`,
  `pins_unchanged_during_run`, `producer_and_fixture_sha256`, `source_revision`.
- `executed_at_utc` is a **single** instant: `2026-10-20T08:36:33Z` (`verification.json:4`).
- The hash map has **20 entries** (`:397-418`); the `commands` array has **22 records** (`:5-396`) whose
  key union is `argv, cwd, exit, label, stderr, stdout` — **no per-command hash, no second timestamp**.
- There are **no** keys containing `before`, `after`, `pre`, or `post`.
- Read-only check: for all 20 map paths, `sha256(git show 27b8fc13…:<path>)` equals the recorded value —
  **20/20 match, 0 mismatches**. So the route's replacement clause "map matches committed
  source-revision blobs" is observed true; what is absent is any second observation bracketing the run.
  The boolean therefore asserts more than the receipt can show; it is an assertion, not a measurement.

## Delta from the route anchor (`corpus/lessons/round-16-verifier-spotcheck.md:183`)

- The route says "The report, lesson, LOG and scorecard say pins stayed unchanged during execution."
  Observed: report (:60), lesson (:154) and LOG (:2012) do; **SCORECARD does not**. Its r16 section
  (`SCORECARD.md:2280-2348`) contains only change-scope or two-revision wording:
  `:2322-2323` "four outside verifier files unchanged, 126/126 pre-existing frozen/evidence blobs
  byte-identical"; `:2328` "QUALITY rows1–17 unchanged"; `:2330` "tiersA21/B1/C1 unchanged".
  **[INFERENCE]** the route's enumeration is imprecise by one document; no temporal correction belongs on
  SCORECARD, and inventing one would add an unsupported "corrected" site.
- **LOG.md:2012 is missed by the contract's proposed regex** (it says "unchanged **across** execution").
  With the contract pattern the sweep reports 3 sites, leaving the LOG overstatement unqualified and the
  count short by one. Recommended substitute pattern in "Integration notes" below.
- The fleet report is outside `--root LANE` and outside the contract's site list, so a Git-objects-based
  `temporal-sweep.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin` can neither scan nor mark
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/kaidoku.md:60`. That site must be named separately
  (its filed bytes must not be rewritten, per the route).

## Adjacent wording — similar words, different claim class; do not "correct" as temporal

- `corpus/lessons/round-16.md:65` and fleet report `:15`: "Outside verifier files remain unchanged." —
  lane-start state audit (clean baseline), no time adverbial.
- `corpus/lessons/round-16.md:142`: "pointer table/expected pins unchanged." — change scope: the README
  integration did not alter them.
- `LOG.md:1944`: "original tool and pinned inputs unchanged." — route-2 change scope.
- `corpus/lessons/round-16.md:145-146`, `LOG.md:2007`, fleet report `:59`, `SCORECARD.md:2323`:
  "126/126 pre-existing frozen/evidence blobs byte-identical." — a two-named-revision comparison produced
  by `controls.py BASELINE SOURCE` with retained argv; pair-of-instants evidence, correctly scoped, not a
  throughout-run claim.
- `LOG.md:1989`: "producer/input hashes retained in `verification.json`." — retention claim; true (map
  exists). It is the setup sentence whose companion at `:2012` overstates.
- `SCORECARD.md:2328/:2330`, fleet report `:41-42/:76`: row/tier/axis "unchanged" — counting or verdicts.
Correction rule applied: only a predicate that ties unchanged/stable to an execution window (during,
across, throughout) or the literal `pins_unchanged_during_run` is in scope; byte equality between two
named revisions is a different, supported claim.

## Bounded no-findings (what was searched, and what was absent)

- `SKILL.md`: zero matches under all three patterns; no r16-scoped pin-stability sentence. Nearest hits
  are generic pin guidance (`SKILL.md:37,:139,:294-296,:407-415`) and registry "Pinned values" cells.
- `SCORECARD.md`: zero during-run statements in the r16 section (`:2280-2348`), as detailed above.
- First r16 LOG entry (`LOG.md:1924-1976`): no temporal pin claim; only change-scope `:1944`.
- Fleet report outside `:60` (lines 1-43, 84-99): no other pin/file stability sentence; `:41-42` are axis
  verdicts.
- Repo-wide widened search found only other lanes/rounds (e.g. `.ufo/reports/round-13/tabi.md:12`,
  `.ufo/reports/round-21/kake.md:57`, `.ufo/waves/round-10/seats/sweep-window.md:575`) and fleet
  `.ufo/MANIFEST.json:7837`, which *quotes the route* rather than asserting stability — all outside the
  kaidoku r16 scope.

## Integration notes for L1 (author-side advice)

1. Append-only named corrections; never rewrite the filed report/LOG/verification bytes (route rule).
   A round-17 lesson/LOG/SCORECARD line containing `R16-PROVENANCE` plus the repo-relative paths
   `LOG.md`, `corpus/lessons/round-16.md`, `.ufo/waves/round-16/verification.json` satisfies the
   contract's `corrected` predicate for all three lane sites at once.
2. Replacement clause per the route: "map matches committed source-revision blobs (20/20 at 27b8fc1);
   temporal stability not evidenced." For the JSON key, add that the boolean is an assertion: no pre/post
   snapshot, no per-command hash, one `executed_at_utc` only.
3. Widen the sweep to `(?i)(unchanged (during|across|throughout)|pins_unchanged_during_run)`. Do **not**
   use bare `remain unchanged`: it adds the change-scope false positive at `round-16.md:65`.
4. Report the fleet-report site explicitly ("plus one filed fleet-report sentence, not machine-counted")
   or add an `--extra-site` input; the lane-root Git sweep cannot see it.
5. If the sweep is ever widened beyond the five lane files, exclude the route/MANIFEST text, which
   contains the literal `pins_unchanged_during_run` and would self-match.

## Remaining unknowns

- Whether uncommitted or seat-local pre/post evidence exists anywhere else was not searched beyond the six
  targets; none is referenced from the four sites. **[INFERENCE]** none exists in committed form.
- Whether the operator/aggregator will mirror the correction onto the filed fleet report is outside lane
  authority.
- The route's intended referent for "scorecard" is unresolved; the reading above (imprecise enumeration)
  is **[INFERENCE]** from the absence of any during-run predicate in `SCORECARD.md`.

Confidence: **high** on the four sites, the regex-coverage gap, and the 20/20 map match (directly observed);
**medium** only on the route's intent regarding SCORECARD.
