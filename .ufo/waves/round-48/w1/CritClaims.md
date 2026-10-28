# CritClaims — round 48 frozen-claim attack

## Axes and scope

Reviewed depth (C1), calibration (C2), and whether apparent gains are rescoring. The frozen rule is `plans/round-48-claims.md` at lines 39–108. Read-only review only; no frozen bytes modified and no claim counter was run. Verification receipts are therefore **not run**.

## Counterexample and evidence

**Freeze identity discrepancy:** the prompt declares `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`, but the claims file says the freeze is the commit first containing the file and `tools/round-48/` (lines 6–12), and A1/A2 specify the commit carrying the amendments (lines 133–158). `git log --format=%H -1 -- plans/round-48-claims.md` returned `ac02a79ff84133220d01ce3b59a4789b7004dbc5`, not the declared hash. Thus the stated path-only derivation does not establish the claimed freeze: it identifies the latest commit touching the claims file, not the first commit that jointly contains all three required pathspecs. This is a potentially material freeze-provenance ambiguity; resolve by checking the joint pathspec at the declared commit and deriving the first joint commit, then use only that exact freeze. I did not run either counter, so cannot claim a counter exit code or classify this as a verified frozen-path failure.

**Depth:** C1 is not merely the established citation-resolution recipe. It adds new predicate content: routed-id-keyed arm semantics, mutations/interpreter source pins, lesson+knowledge citations, and digit-to-meaning classification for every census row (`plans/round-48-claims.md:44-68`). This is a meaningful extension to depth rather than simple re-scoring, although no before/after measurement was run. A directly evidenced design risk is token-substring classification: `meanings.py` defines regex token classes `SUCCESS`, `NOTMET`, `UNEVAL` at lines 57–61, while legitimate prose can contain a term such as “refusal” in explanatory context (the A2 false-red is disclosed at claims lines 147–158). The frozen amendment addresses one concrete false positive, but regex classification remains context-insensitive; the strongest required attack is to mutate text with class tokens in non-verdict clauses and demonstrate exact outputs. Not run here.

**Calibration:** C2 adds a real completeness floor and re-derives quotes/corrections/score cells, but its floor is structural, not a completeness proof of the record. The implemented predicate visible in `record2.py` requires per-section one seat/path/rev atom and a claim id, at least two axes atoms, correction validity, and quote binding (lines 80 onward; specifically floor logic in the inspected body). A section can still satisfy a minimum count with a true but unrepresentative atom and a claim id unrelated to the work; that is an explicit bounded proxy, not evidence that the whole record is complete. The five forgery battery tests named cases, not the full adversarial space. No evidence establishes the after-state score as a single closure-reproducible value yet; the claimed command requires a chosen `--rev` and a valid freeze, and acceptance must include its battery. Not run.

**Re-scoring:** The card currently shows coverage and depth already at 10/10 in `SCORECARD.md` lines 23–25, and calibration already at 10 with round-47 measurement text. C1 targets a new semantic depth instrument, not the old 24/24 citation count; C2 targets a new record instrument, not the old round-47 consistency-only metric. These can represent new measurement capability, but they do not demonstrate numerical axis improvement when the scores are already saturated. Claims correctly disclose all owned axes tied at 10 and no coverage claim (`plans/round-48-claims.md:14-22`). Any reporting must distinguish “instrument/predicate improved” from “axis score increased.”

## Smallest safe correction / landing guidance

1. Reconcile the declared freeze with the claims file's first-joint-commit definition; cite the joint pathspec evidence rather than relying only on the claims path log.
2. Preserve C1's new depth surface, but attack context-insensitive meaning tokens with valid verdict prose containing cross-class words outside the verdict segment; reject only if a concrete v3-green forgery occurs.
3. Describe C2 as calibration-instrument hardening and disclose the structural floor's bounded nature; do not claim comprehensive record completeness or a score increase absent measured evidence.
4. L1 should run both frozen counters against the actual landing revision and include exact command, exit, stdout hash, timestamp, and battery outputs before asserting closure.

## Commands exercised

Exact command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format=%H -1 -- plans/round-48-claims.md`
Exit: 0. Stdout: `ac02a79ff84133220d01ce3b59a4789b7004dbc5`.
SHA-256 of stdout payload (without trailing newline): not computed. UTC timestamp: not captured. This is an incomplete receipt under the assignment's receipt format; do not treat it as a formal counter receipt.

Exact command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain`
Exit: 0. It showed extensive pre-existing user changes in sibling wave paths; none were modified by this seat. Stdout hash and UTC timestamp: not captured.
