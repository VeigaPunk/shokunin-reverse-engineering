# ReviewSpotcheckRouting: coverage of the 8 routed defects in round 28

Seat: KaidokuR28a2.ReviewSpotcheckRouting (reviewer, leaf). Run 2026-10-22, ~18:35Z-18:49Z.
Basis: `corpus/lessons/round-27-verifier-spotcheck.md` lines 150-159 (the 8 defects), the claim
files `.ufo/waves/round-28/claims.json` and `claims-c2.json`, the a2w wave spec/dispatch
(`.ufo/waves/round-28/a2w-spec.json`, `a2w-dispatch.json`; the 73-seat a2 wave was withdrawn),
and lane tip `cae73c49` (main). The L1 has already landed the round-28 section in
`SCORECARD.md:3135-3157`, the round-28 lesson `corpus/lessons/round-28.md`, QUALITY rows 41-44,
and SOURCES rows S084-S086.

## Per defect

1. Corrections sweep (r26 entry pointer + QUALITY row superseding 37). **Addressed, landed.**
   `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md:137-145` has
   `## Pointer appended in round 28` naming the `analyze`/`inspect` rows and `## Use` and stating
   the snapshot-suffix condition (S083). `corpus/QUALITY.md:51` is row 41 superseding row 37 for
   those verbs, citing the r27 entry, the spot-check (`:112`, `:152`) and S083. Committed in
   `2832c5b3`. Also covered by seats ScribeR26Pointer (drafted) and ReviewQuality37 (a2w).

2. Red round-27 C2 selftest. **Partly (still red at tip; fix in flight).** Observation: sandbox
   clone `git clone -q <lane> clone` at `cae73c49`, then
   `python3 -I -B tools/round-27/c2-xpin-check.py --selftest` exits **1** at 18:39Z with
   `FAIL correct-stub: exit 0, expects 'r26_rows_ok=24/24 red_ok=3/3' | r26_rows_ok=24/24
   red_ok=3/3 capability_row=1 source_row=1 (S081)`; 6 cases, 1 failure. The fixture still
   demands the pre-`97358f75` output. Seat ExecR27SelftestFix (a2w, running) owns the fixture
   re-anchor and green receipt. Remaining: land that fix and its green receipt; the defect
   stays open until then. `SCORECARD.md:3151` points at "the wave findings below".

3. SKILL.md registry rows for the r27 counters. **Partly (drafted, not landed).** Observation:
   `grep -n 'c1-rename-identity\|c2-xpin-check' SKILL.md` prints nothing at tip. Seat
   ScribeRegistryRows (a2w, running) drafts one block covering both r27 tools plus both r28
   tools; a2w/ScribeRegistryRows.md not yet filed. Remaining: L1 integrates the drafted block.

4. Pinning (every file a counter loads pinned; freeze wording exact). **Addressed, landed.**
   `claims.json` `loaded_by_counter` pins `tools/round-25/a2/resolve-selectors.py`,
   `carriers.tsv`, `heldout.tsv` by sha256, with `pin_note` naming exactly what is pinned
   versus counted (lines 10-15); `claims-c2.json` `loaded_by_counter` pins `selectors.tsv`
   and `canonical-signatures.json` (lines 8-11). Both counters exit 2 on pin mismatch:
   selftest receipts `.ufo/waves/round-28/before/c1-selftest.txt` and `c2-selftest.txt` show
   `red-pin-refusal exit=2 want=2`, `failures=0` (21 and 17 cases). Committed at the freezes
   `87d3dfb6` / `86fa8526`; confirmed by `SCORECARD.md:3153`.

5. Duplicate-bytes gate (M27-2 / QUALITY row 40). **Addressed in substance; the standalone
   repaired-gate claim is deferred, not owed this round.** Observation: the r27 counter's
   cross-run byte comparison does not exist in the r28 C1 counter — per-run binding by carrier
   key, subject digest and envelope sha256 instead (`claims.json` `identical_outputs`,
   `tools/round-28/c1-heldout-naming.py:184-196`), and its freeze ships the green look-alike
   selftest case `green-identical-4byte-bodies-across-selectors` (exit 0 in the before
   receipt). SCORECARD:3121 already offered this as the "second choice" plan and SCORECARD:3154
   records r27 C1 stays a miss, never re-scored. Remaining: nothing required; a dedicated
   repaired-gate claim may still be a future round's claim if the lane wants the exact r27 gate
   shape re-tested. MutQualityRow40 (a2w) mutation-tests this row's enforcement.

6. Gate quotes from rendered HTML. **Addressed, landed.** QUALITY row 42
   (`corpus/QUALITY.md:52`) now codifies contiguous served bytes <=25 words and the `composite`
   label for rendered-HTML quotes. The round-28 Gate quotes are all from raw text files
   (raw.githubusercontent.com .ts, .json, .rst; `corpus/lessons/round-28.md` Gate table
   S084-S086). Residual minor: CriticSourceRows (a2w/CriticSourceRows.md, admit with fixes)
   flags the S085 quote `"0xd55ec697": {` as grounding neither "36 keys" nor the signature,
   and S084's "filtered: false" half resting on unanchored `:90`/`:262` — lesson-level
   corrections already appended at round-28.md Gate notes, not a defect-6 problem.

7. SCORECARD :3125/:3130 clarification. **Addressed, landed.** `SCORECARD.md:3156` states
   lines 16-17 are this file's own baseline-citation rule, not AXES lines, and that "the
   current planned field" at :3125 and :3130 means the field at :3128, superseding :3121.
   Placement is inside the appended round-28 section rather than beside the original lines;
   consistent with the lane's append-only convention.

8. Mutation tests (QUALITY rows 38-40, xpin-attribute.mjs). **Partly (planned and dispatched;
   nothing landed yet).** The a2w dispatch (`a2w-dispatch.json`, 36 spawns, registry all
   `spawn`) includes four defect-8 seats whose task texts are complete mutation plans:
   MutQualityRow38 (>=3 mutations to the instrument-before-data ordering in both r28 counters),
   MutQualityRow39 (>=3 mutations to pkg_version/pkg_json_sha256 enforcement), MutQualityRow40
   (>=3 mutations to the green look-alike/refusal gate), MutXpinTool (>=4 mutations to
   `tools/round-27/xpin-attribute.mjs`, compared against the committed r26-attribution receipt
   using the installed 6.5.0 and 6.7.0 package roots). Two extras beyond the defect:
   MutC2Counter (5 mutations to `c2-filtered-flag.py`) and MutLessonGate (entry_ok source-row
   checks). My assignment states the mutation-tester route is down this round; the live roster
   shows all six seats running, so the route-down premise may be stale. If the seats die as in
   round 27, the L1 must run the same procedures itself in one sandbox clone per target: apply
   each numbered mutation from the four seat task texts (plus the two extras if it wants them),
   re-run `python3 -I -B <counter> --selftest` (or the xpin tool on the 24 r26 envelopes with
   `--pkg65`/`--pkg67`) after each, revert, and record diff + killed/survived per mutant —
   i.e. re-execute the a2w task texts verbatim, they are self-contained. Remaining: land the
   six reports and fill the "wave findings" pointers at `SCORECARD.md:3151-3152,3157`.

## Residual risk and gaps

- The SCORECARD items 2, 3 and 8 point at wave findings that do not exist yet; if a2w seats die
  the pointers dangle. Defects 1, 4, 6, 7 are fully closed at tip `cae73c49`.
- The 73-seat a2 wave carried two defect-adjacent seats the 36-seat a2w wave dropped:
  ScribeScorecardClarify (defect 7) and ScribeQualityHtmlQuote (defect 6). Both defects were
  answered by the L1's own edits instead, so coverage did not regress.
- I did not re-run the r28 counters or the xpin tool; the r27 selftest red state was re-run by
  me in a scratch clone (receipt below). Everything else is read-only observation of committed
  bytes at `cae73c49`.

## Artifacts (under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewSpotcheckRouting/)

- `r27-selftest.txt` sha256 `f676450df0870907cdf1866b08fb6eac0709963aab1025b087e5b0f2bd708b99`
  — `c2-xpin-check.py --selftest` output, exit 1, `cae73c49` clone, 18:39Z.
- `clone/` — sandbox clone used for the selftest (transient, listed for reproduction).

No tool installs or updates. No 4byte/openchain requests, no REA runs. No lane file written
other than this report.
Report: .ufo/waves/round-28/a2w/ReviewSpotcheckRouting.md
