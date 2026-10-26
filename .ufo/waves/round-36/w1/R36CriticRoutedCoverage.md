# R36 critic — inherited outside verdicts: routed-defect coverage

Seat `R36CriticRoutedCoverage`, leaf. Round 36, wave 1. Measured at lane HEAD
`d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` (base `cab59f22`), 2026-10-26.
Sources read in full: `corpus/lessons/round-35-verifier-spotcheck.md` (121 lines),
`round-34-verifier-spotcheck.md` (169), `round-33-verifier-spotcheck.md` (141),
`plans/round-36-claims.md` (104), `tools/round-36/c1-counter.py` (372), `c2-counter.py` (340).

Method: committed bytes only. No lane counter, gate or selftest was executed (PROTOCOL §Gate
standard, the same limit every prior closure accepted). Read-only git (`log`, `show`,
`diff --name-only`, `ls-files`, `cat-file`) plus `python3` over committed blobs. No scratch
directory was created (no clone, download or fixture was needed); no tool was installed or
upgraded; no VCS mutation; nothing outside this file written.

## Verdict in one paragraph

The round handles the *shape* of the inherited criticisms well — the two inherited design defects
that were actually methodological (substring-anywhere doc checks, frozen-C2 coupling) are fixed in
the frozen instruments — but it does not handle the *ledger*. Sixteen routed items and
disagreements from r33/r34/r35 have neither a landed fix nor an observable in the plan, and the plan
asserts at
`plans/round-36-claims.md:103-104` that the routed set is "landed as appended corrections" when no
such correction exists at HEAD (`git diff --name-only cab59f22 HEAD` touches none of
`LOG.md`, `corpus/lessons/`, `corpus/knowledge/`, `corpus/QUALITY.md`, `SKILL.md`, `PROVINCE.md`,
`corpus/SOURCES.md`, `corpus/README.md` — the grep exits 1 on an empty set). Two frozen instruments
also admit a green result while the surfaces the claims name as moved/stated stay false. Both are
reportable; neither requires touching a frozen predicate.

## Counterexample 1 — R36-C1 can be met while both named surfaces still say the capability is missing

- The claim's surface is explicit: `plans/round-36-claims.md:14-17` names `PROVINCE.md`
  `### Round-4 frontier (post-unlock)` bullet **sasquatch** and `corpus/README.md` **Firmware row**
  ("AppImage SquashFS carved but recursion blocked by missing sasquatch"), and the title says the
  surface *moves* from Frontier to Core.
- The frozen predicate (`:22-30`) and the counter require only: a round-36 **Core** section row
  (`c1-counter.py:199-202`, scans `section(prov, '## Round-36 additions to Core')` only), the entry
  file, one SOURCES row with exact-cell `used-by` (`:215-224`), and one `## Coverage map` README row
  *containing the stem lexically* (`:226-229`).
- At HEAD the named surfaces are still unretired: `PROVINCE.md:149`
  ("**sasquatch** — unblob's squashfs recursion extractor (AUR-only); 7z fallback covers today") and
  `corpus/README.md:44` ("AppImage SquashFS carved but recursion blocked by missing sasquatch"),
  with `README.md:227` repeating "sasquatch (AUR) … 7z fallback covers today".
- Nothing in the counter reads the frontier bullet or the "recursion blocked" clause. A revision that
  adds a Core row + entry + SOURCES row + one coverage-map row and leaves `PROVINCE.md:149` and
  `README.md:44` byte-identical scores `carriers_matched 4`, all five bindings true, `met_target`.
- This is not hypothetical distance: the committed after receipt at `3310d8fa` already has
  `carriers_matched: 4`, `carriers_unchanged: true`, and all five bindings false
  (`.ufo/waves/round-36/interim/c1-after-receipts-only.json`). The whole remaining delta of R36-C1 is
  documentary, and the documentary clause does not cover the retirement the claim asserts.
- Severity judgement: **fixable defect, not a tradeoff to accept**. A coverage credit that says a
  frontier surface moved while the frontier bullet still says "AUR-only" is exactly the class the r35
  closure refused ("no PROVINCE/README edit", `round-35-verifier-spotcheck.md:76`).

Secondary trap in the same clause (low severity, pre-data): the frozen heading literal is
`## Round-36 additions to Core` with no suffix, but the lane's own last two Core headings carry one —
`PROVINCE.md:343` `## Round-31 additions to Core (verified 2026-10-23)`, `:353`
`## Round-32 additions to Core (verified 2026-10-23)`. `section()` uses `lines.index(heading)`, an
exact match, so house style would make `province_core_section` false and C1 unreachable. The lane
must write the frozen literal and disclose the deviation.

## Counterexample 2 — R36-C2 is green while every inherited disagreement stands

- C2 is genuinely honest at its own landing: `.ufo/waves/round-36/c2/after-at-d2e46ef5.json` gives
  `mismatches 0`, `guards_ok true`, `met_target true`, `base_unresolved` = `receipts-B` and
  `ScoutSkillPlacement.md`, `guards.base_pointers 34`. Base 3 mismatches reconcile with
  `plans/round-36-claims.md:79-82`.
- But its unit set (`c2-counter.py:57-86`, `units()`) is only `SCORECARD ## Owned axes`,
  `SCORECARD ## Capabilities`, `SHONEN.md` boxes — i.e. `plans/round-36-claims.md:67-70`. At the same
  revision, these are all still true:
  - the r35 self-grade `quality: improved` (fleet `.ufo/reports/round-35/kaidoku.md:46`) remains
    contradicted by the outside verdict (`round-35-verifier-spotcheck.md:102` "Disagree with the
    self-grade");
  - `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:3-6` still carries
    `author/status/sources/revisions` and no `source:`/`verified-at:`/`recheck:` (R34-D3);
  - `SKILL.md:998,1042,1213` still declare `| tool | purpose | command | exit codes | selftest |`
    (R34-D4, five columns against PROTOCOL §Gate's eight);
  - `.ufo/waves/round-35/w1-settle.json` is still `{"spawned": 2, "settled": 2, "dead": 0,
    "spawned": 7}` and `w1-results.json` still carries 64 seats with `output: null` (R35-D2).
- Therefore "calibration met" and "no inherited disagreement remains" are different propositions, and
  the plan nowhere separates them. The lane has the right precedent in its own file: `SCORECARD.md:3382`
  ("Round-35 trend verdicts are not inferred from claim counters alone"). Round 36 does not restate
  it, so a green C2 will read as closing R35-D1 unless the record says otherwise.

## Enumeration — every disagreement and routed defect

Legend: **plan?** = does `plans/round-36-claims.md` state an observable/ordering for it; **landed?** =
is it discharged by a commit at or before HEAD; **owed** last column.

### Round-33 spot-check (`round-33-verifier-spotcheck.md`)

| id | source | item | plan? | landed? | owed |
|---|---|---|---|---|---|
| R33-1 | `:127` | report:8 claimed `SKILL.md` unchanged (it gained 72 lines) → append a correction in the next LOG/lesson | n/a (already discharged) | **yes** — `LOG.md:3084` carries the appended correction with the `72 0` per-file diff and the "filed report is not rewritten" rule; class also encoded as `QUALITY 65` (`corpus/QUALITY.md:75`) | none |
| R33-2 | `:128` | R33-C1 unprovable, no revival, any future depth claim needs an independently authored manifest frozen pre-data | no | no depth claim exists (`plan:8-9`: C1 coverage, C2 calibration), and no revival: no CHPE/jsc work in the r36 diff | **stated reason** (one line: no depth claim, R33-C1 stays stopped) |
| R33-3a | `:130` | seven empty/malformed freeze maps falsely CLEAN → claims-schema validation | no | partly: `tools/round-34/freeze-integrity.py` + `LOG.md:3088` ("all seven old false-CLEAN map cases as exit 3"); **not applied to r36** — r36 uses no claims container and its receipts carry no counter digest and no UTC instant, so nothing verifies that the frozen counter bytes are the ones that scored | **stated reason** + a digest/UTC pin (QUALITY 73 says a receipt states argv, reader digest, commit, UTC *or declares `caller_asserted`*) |
| R33-3b | `:131` | parser count-limit `>`→`>=` mutant survives | no | no (`LOG.md:3088` "old count-boundary mutant survives") | **stated reason** (not an admission dependency of P36-C1/C2) or bound it |
| R33-3c | `:132` | metadata-span mutation inconclusive after EAGAIN | no | **yes** — `LOG.md:3088` "span is now killed" | none (r36 does not restate; acceptable) |
| R33-3d | `:133` | tag mutant detected only via an error | no | no (`LOG.md:3088` "tag detection remains detector-error-only") | **stated reason** |
| R33-3e | `:134` | scanner lexical blind spots | no | no (disclosed, not repaired) | **stated reason** |
| R33-4 | `:136` | five round-32 wrapper mutants + archived secondary-gate gaps (`pe_own_compare`, `verify_quotes`, `independent-pe`) | no | no — `LOG.md:3068` and `SKILL.md:1190` leave them open, and `SKILL.md:1190`'s non-dependency statement is scoped to **P34** only | **stated reason** restated for P36 (or a fix) |
| R33-5 | `:137` | parser pin forward pointer | n/a | **yes** — `.ufo/waves/round-33/prep/R33ChpeParser-independent.json:51-58` carries `path`/`superseded_pin`/`reason` and keeps the old digest | none |
| R33-N1 | `:27-29` | the dispatched prompt did not carry the literal `/fast/scratch` `du`/`find` restriction (flagged orchestrator-side); `QUALITY 60` requires it in every wave context | no | **recurs** — `.ufo/waves/round-36/w1-spec.json` `context` contains `Scratch` once and `du `, `find`, `disk` **zero** times; the per-item prompts carry it zero times | **QUALITY 60 conformance** for the next wave + disclose that the r36 wave was dispatched without it |
| R33-N2 | `:115-123` | SHONEN box 2 (end-to-end task) and box 3 (executable without oral context) not checkable | partly | partly — C2 checks box pointers/one count/one range only | **stated reason**: what C2 certifies about SHONEN, and what it does not |

### Round-34 spot-check — "Routed defects — kaidoku must fix next round"

| id | source | item | plan? | landed? | owed |
|---|---|---|---|---|---|
| R34-D1 | `:122-129` | start census must be captured in its own file before the first registry edit, and the observed count reported | yes (`plan:96-97`, "exit 0, 9 W04") | **yes, substantively** — `.ufo/waves/round-36/census-start.txt` added in `790561d4` (the first r36 commit), names `rev=cab59f22` (the base), carries a UTC stamp and `EXIT=0`, and it is *not* interchangeable with an end census because no SOURCES edit has landed (`corpus/SOURCES.md` last row is still `S106`) | residual only: the receipt records no row count (106); put it in the end census/report |
| R34-D2 | `:130-134` | seat accounting must match the record (r34: 31/32, not 32/32) | names it only inside "hygiene" (`plan:103`) — no observable, no ordering, no artifact | **no**, and the class is *recurring now*: `.ufo/waves/round-36/w1-spec.json` has **43** items, `.ufo/waves/round-36/w1/` holds **13** seat reports, and `w1/swarm-registry.json` lists every member with `agentId: null, item: null` | **fix**: commit `w1-results.json`/`w1-settle.json` with real per-seat status, and compare settled count against the 43-item spec (QUALITY 76) before the report |
| R34-D3 | `:135-140` | entry provenance trio (`source:`/`verified-at:`/`recheck:`) for the r34b entry, appended not rewritten | names it (`plan:103-104`) | **no** — verified at HEAD: the file's only header fields are lines 3-6 `author/status/sources/revisions` | **fix** (appended block; cheap, independently doable, owed since r34) |
| R34-D4 | `:141-145` | PROTOCOL §Gate registry rows need `gate|probe`, verdict map, self-test + spelling, pinned-value path, write scope, owner | no | **no** — `SKILL.md:998`, `:1042`, `:1213` still five-column; r36 adds two counters and a harness and the plan has no field list for their registry rows | **fix** (8-field rows when the r36 registry section lands) or a stated reason + QUALITY criterion |
| R34-D5 | `:146-150` | protocol lane: no per-attempt report filename / erratum rule for re-dispatched rounds | no | out of lane; still relevant because r36's base `cab59f22` is exactly that artifact — commit message: "hyaku run 7 interrupted: in-flight snapshot committed by the orchestrator (not a landing)", and its 14 added files are the closed round-35 wave artifacts | **stated reason** ("protocol lane") named in the r36 record, so the ledger closes |
| R34-N1 | `:160` | SHONEN box 2 (end-to-end domain task) not checkable | no | no — C2 checks box 2's pointer only | **stated reason** (see R33-N2) |

### Round-35 spot-check — "Routed defects (lane fixes next round)"

| id | source | item | plan? | landed? | owed |
|---|---|---|---|---|---|
| R35-D1 | `:107`, disagreement at `:102`, `:34(5)` | self-graded `quality: improved` without a LEARNING.md observable | no (implicitly swept into "hygiene") | **no** — no LOG/lesson/QUALITY change landed in r36; the false grade is at fleet `.ufo/reports/round-35/kaidoku.md:46` and the outside verdict says `unchanged` | **fix**: appended correction naming `round-35-verifier-spotcheck.md:102` (class already covered by `QUALITY 65`) |
| R35-D2 | `:108`, `:34(1)(2)(3)` | seat accounting not derivable; commit the 14 artifacts **or** say why; file a correction naming the supersession of the report's "not yet verified" accounting | no | **partly** — the 14 artifacts were committed at `cab59f22` (by the orchestrator, not the lane), and seat-name coverage is now derivable: 64 spec names == 64 `w1/*.md`, no missing/extra. **Still not derivable:** `w1-results.json` = 64 × `output: null` (with prose notes) and `w1-settle.json` is malformed with a duplicated `spawned` key (JSON parsers take the last, giving spawned 7 vs 2 keys); no supersession correction exists | **fix** + correction |
| R35-D3 | `:109` | new C2 must be severable from C1 and token-exact; D-4 heading/table shape reconciled | **yes** (`plan:89-91` separability; the S-id/substring class is gone) | **yes in design** — `c2-counter.py:26` anchors the pointer token (`^…$`), there is no S-id element to substring-match, and the d2e46ef5 receipt is green with C1's entry not yet landed | residual: C2 takes no `--freeze` and no digest pin, so "no counter change after this commit" is asserted (plan kill rule) not instrumented — the r35 `INSTRUMENT_REVISED` class (`.ufo/waves/round-35/freeze-status.md`) | **stated reason** or an appended digest pin |
| R35-D4 | `:110` | C1 package staged but unadopted; reattempt with a **table-scoped** PROVINCE/README check | yes (predicate `:22-30`) | **method yes** — `c1-counter.py:199-202` scopes PROVINCE to the Core section, requires a word-boundary `sasquatch` in the **first cell** and the entry path in the row; `:215-224` requires exact-cell `used-by`; selftest reds cover row-outside-section, first-cell, row-absent, `S1070`, opened-earlier, used-by, stem-absent (`:318-324`) | residuals: (a) the README binding is still lexical (`STEM in l`, `:229`), not an exact-stem cell — the R35-D4 class is narrowed at that one site, not eliminated; (b) the staged jsc2js package has no disposition — `S125`/`S129` were never registered (`corpus/SOURCES.md` ends at `S106`) and `PROVINCE.md:147` still carries the `.jsc → source mapping` frontier bullet; (c) see Counterexample 1 | **fix/disclose**: (a) quote the actual coverage-map row in the report; (b) one disposition line for the staged package |
| R35-D5 | `:111`, `:34(1)` | report filed before the final lane commit; late artifacts as erratum, never rewrite | no | **no** — no prefile gate and no erratum convention in the plan; `QUALITY 47` requires `tools/round-29/prefile-check.sh <LANE>` exit 0 immediately before the report commit and that script exists (`tools/round-29/prefile-check.sh`, 2305 bytes) | **fix**: name the prefile gate in the plan/lesson and run it; **stated reason** for the erratum rule |
| R35-N1 | `:34(4)`, `:113` | SHONEN boxes are `[~]` author assertions, not checkable by a non-author | partly | partly (see R33-N2) | **stated reason** |
| R35-O1 | `:67` | observation: r34's D-2/D-3 were doable without the C1 dependency and were not attempted | no | **recurs** — r36 again defers the whole routed set to "hygiene" with no gate, no ordering and no artifact, so it is again sequenced behind the claims | **fix**: a committed disposition ledger (see below) |
| R35-V1 | `:83` | verdict `rejected-honest-stop`, admitted=false | **yes** (`plan:4` cites all three rejections) | n/a | none |

Tally over the 25 enumerated rows: **4 discharged by a landed commit** (R33-1, R33-3c, R33-5, R34-D1),
**3 discharged in design by the frozen instruments** (R35-D3, R35-D4-method, R35-D2-first-half),
**1 out-of-lane** (R34-D5), **1 acknowledged** (R35-V1) — leaving **16 with neither a landed fix nor a
plan observable**, most of them only a one-line "stated reason" away from being closed.

## What the round got right (calibration of this review)

Not everything is open, and saying so matters for the reviewer's own calibration:

- The r35 class that produced the worst defect — *substring-anywhere* doc checks — is genuinely fixed at
  the PROVINCE and SOURCES sites, with red selftests that name the precise failure. The `S1070` case
  (`c1-counter.py:321`) is the direct answer to the r35 `S1060` critic finding.
- C2's severability answer (`plan:89-91`: measured at its own landing commit, then re-stated at the tip;
  C1 reads none of SCORECARD/SHONEN) is the right shape and is already exercised — the d2e46ef5 receipt
  predates the entry.
- The census fix (R34-D1) is real: the receipt names `rev=cab59f22`, which is what made the r34 pair
  indistinguishable.
- The plan's stated selftest tallies match the code: C1 has 14 cases (1 green + 13 red — the plan's
  "oracle or carriers changed" is two cases, which is why the enumeration looks one short) and C2 has
  13 (1 green + 12 red). No overclaim there.
- Counters are byte-stable since the freeze: `git diff --stat 790561d4 HEAD -- tools/round-36/` is empty.

## Impacted axes

| axis | impact | why |
|---|---|---|
| calibration | **at risk (primary)** | C2 can report 0 mismatches while every inherited disagreement (R35-D1, R34-D3, R34-D4, R35-D2) stands; `plan:103-104` asserts they are "landed" when they are not. Crediting calibration from C2 alone would repeat the r35 rejection reason |
| coverage | **at risk** | R36-C1's `met_target` does not require the frontier bullet (`PROVINCE.md:149`) or the README Firmware clause (`README.md:44`) to be retired, so coverage could be credited for "Frontier → Core" with both surfaces still false; R35-D4's jsc2js surface also remains unadopted and undisposed |
| freshness | degraded (small) | R34-D3 is the freshness sweep's input field trio; leaving it absent keeps one entry invisible to sweeps |
| depth | unaffected | no depth claim this round; R33-2 correctly dormant |
| operability | unaffected | no claim; `R34-D4` is a documentation-shape gap, not a runnability one |
| adjacency | unaffected | not claimed |

## Smallest safe corrections (none touches a frozen predicate, counter, carrier or oracle)

1. **Correct the plan's provenance sentence (append-only erratum, pre-report).** `plan:103-104` must stop
   saying "landed as appended corrections". Either name each artifact and its commit, or say "to be
   appended before the report" and add the ledger in (2). This is the false-provenance item; it is the
   cheapest and the one most likely to be quoted by a closure.
2. **Add a disposition ledger** (`.ufo/waves/round-36/routed-defects.md`) with one row per item above:
   id, source line, state (`discharged` / `fix owed` / `stated reason`), and the anchor. The ledger is the
   observable the plan currently lacks; without it "hygiene" is unfalsifiable.
3. **Separate the two propositions in the record.** State that `P36-C2` certifies the three enumerated
   SCORECARD/SHONEN surfaces only, and that trend grades and seat accounting are certified by the outside
   closure, following the `SCORECARD.md:3382` precedent. Then R35-D1 needs its own appended correction.
4. **Retire the two named C1 surfaces outside the counter** and show the diff in the report: strike or
   re-point the `PROVINCE.md:149` frontier bullet and the `README.md:44` "recursion blocked" clause at
   the same revision the Core row lands. Keep `met_target` as evidence of the Core addition only.
5. **Close the r34 trio and registry shape** (R34-D3, R34-D4) as appended edits; both are minutes of work
   and both are cited by a closure, not by the claim.
6. **Commit the wave's own accounting before the report** (R34-D2/R35-D2/R35-D5): real `w1-settle.json`
   (no duplicate keys), a `w1-results.json` whose entries are not all `null`, the 9 currently untracked
   wave paths, and `tools/round-29/prefile-check.sh` exit 0 in the report.
7. **Add the literal scratch restriction to the next wave's context** (`QUALITY 60`) and record that the
   r36 wave was dispatched without it (R33-N1 recurrence).
8. **Write the Core heading exactly as frozen** (`## Round-36 additions to Core`) and disclose that it
   departs from `PROVINCE.md:343/353` style, which would fail `province_core_section`.

## Limits of this review

- Lane counters, gates and selftests were not executed (PROTOCOL §Gate standard; consistent with the
  r33/r34/r35 closures). Every number above is read from committed receipts (`interim/…`,
  `c2/after-at-d2e46ef5.json`, `controls/*.json`) or from a read-only git/python recomputation over blobs.
- Wave state (43 spec items, 13 reports, 9 untracked paths) is a snapshot at HEAD `d2e46ef5`; a settlement
  after that instant would change R34-D2/R35-D2's status but not the plan-level gap.
- The `met_target`-with-stale-surfaces construction (Counterexample 1) is [INFERENCE] from the counter's
  read set (`c1-counter.py:199-229`); it was not executed as a lane run, and the frozen counter was not
  modified to demonstrate it. It is falsifiable in one command by anyone holding a scratch fixture.
- No claim is made about the correctness of the C1 carriers, oracle or evidence-id recomputation; other
  seats hold that scope.
