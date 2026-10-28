# round 47 — report draft: Work performed + Landed changes

Draft for the L1 (`KaidokuR47`). Generated from the seat directories of
`.ufo/waves/round-47/w1/` at lane tip `b1a058f3` (`round-47: final receipts at the tip`).

**Coverage at this draft: 58 of 75 work items have a `report.md`**; 17 are gaps (listed
after the bullets). Every bullet below quotes or paraphrases only what the named seat
wrote; a gap is never upgraded to a result. `w1-results.json`
was **absent** at generation time.

## Work performed

### C1 verification (executors)

- **C1Struct** (executor) — Clauses 1–3 are computable, non-vacuous on this surface, and satisfiable together with clauses 4–9: candidate B is a measured failing == []…
  Evidence: `.ufo/waves/round-47/w1/C1Struct/report.md`, `.ufo/waves/round-47/w1/C1Struct/receipt.json`.

- **C1Ids** (executor) — Clause 4 is implemented exactly as the claims file states it and it fires on every cardinality defect I could construct — three forgeries red with clause-4 messages, a block that satisfies it green, and a block that breaks only the clauses *after* it keeps cla…
  Evidence: `.ufo/waves/round-47/w1/C1Ids/report.md`, `.ufo/waves/round-47/w1/C1Ids/receipts/at-tip-a4-freeze.json`, `.ufo/waves/round-47/w1/C1Ids/receipts/freeze-run.json`.

- **C1Tokens** (executor) — §4. Attack matrix — clause 5 alone — Each variant rewrites the four arm cells of the verified block and re-scores it in a fresh one-commit fixture. v3/v2 are counter exit codes (0 met, 1 not met). Matrix in attack-matrix.json and attack-matrix-vacuity.json.
  Evidence: `.ufo/waves/round-47/w1/C1Tokens/report.md`.

- **C1Digest** (executor) — Met by the landed block, and falsifiable in the ways the clause promises. The pin at REV is mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112, which I re-derived twice from the frozen source (ast walk and re over the MUTATIONS l…
  Evidence: `.ufo/waves/round-47/w1/C1Digest/report.md`.

- **C1Order** (executor) — §1. The clause, quoted from both files — plans/round-47-claims.md:80-82 (predicate 7, measured at the freeze)
  Evidence: `.ufo/waves/round-47/w1/C1Order/report.md`, `.ufo/waves/round-47/w1/C1Order/receipt-freeze.json`.

- **C1Refs** (executor) — §5. Findings against the frozen clause (do not fix frozen bytes) — F1 — clause 8 is satisfiable by a content-free citation set. Three repeats of one line —  corpus/lessons/round-46.md:57, corpus/lessons/round-46.md:57, corpus/lessons/round-46.md:57  plus the two SELF mentions in the narrative — give refs 6 over two distinct p…
  Evidence: `.ufo/waves/round-47/w1/C1Refs/report.md`, `.ufo/waves/round-47/w1/C1Refs/receipt.json`.

- **C1Battery** (executor) — §1. Result — the four classes discriminate, under my mutations, not the counter's — One-commit fixture per class. Fixture SKILL.md = the candidate block-24 bytes sha256:bf94d1b5… inserted into SKILL.md; every other file taken from git show 5017e1f:. Every fixture is a fresh git init in scratch with git -C "$D" rev-parse --show-toplevel assert…
  Evidence: `.ufo/waves/round-47/w1/C1Battery/report.md`, `.ufo/waves/round-47/w1/C1Battery/attack.py`.

- **C1SelfTest** (executor) — Net: C1's *artefact* predicate is sound enough to fail a real block (the do-nothing control reproduces…
  Evidence: `.ufo/waves/round-47/w1/C1SelfTest/report.md`.

- **C1FreezeWindow** (executor) — §4. The frozen window and the claims file's own freeze derivation (seat headline) — Live, --freeze pinned at $F, --rev at the tip, using the claims file's own counting command (receipts/c1-at-tip-pinned-freeze.json, battery not run)
  Evidence: `.ufo/waves/round-47/w1/C1FreezeWindow/report.md`.

### C2 verification (executors)

- **C2Atoms** (executor) — 1. The atom layer is sound. 50 atom instances / 41 distinct (class,key,atom) triples at the base 13a9e9e1; my independent derivation (raw git show / cat-file / ls-tree / rev-parse / merge-base, no import of record.py) agrees with record.derive() on every atom,…
  Evidence: `.ufo/waves/round-47/w1/C2Atoms/report.md`, `.ufo/waves/round-47/w1/C2Atoms/receipt.json`.

- **C2Mismatch** (executor) — §3. Findings against the FROZEN C2 clause (attack, not repair) — Each finding has a runnable probe, the exact command, the differing value and a fixture path…
  Evidence: `.ufo/waves/round-47/w1/C2Mismatch/report.md`, `.ufo/waves/round-47/w1/C2Mismatch/receipt.json`.

- **C2Corrections** (executor) — corrections_bad [{line: "- corrects window round-46: empty in 332f4884..58eb04b6 …",
  Evidence: `.ufo/waves/round-47/w1/C2Corrections/report.md`, `.ufo/waves/round-47/w1/C2Corrections/receipt.json`.

- **C2Vacuity** (executor) — The mechanism is *not* vacuous against the do-nothing record and three of the five specified attack families stay red — but four constructions reach met_target: true with a materially false or unverifiable record (A6, A7, A13, A14)…
  Evidence: `.ufo/waves/round-47/w1/C2Vacuity/report.md`.

- **C2CorrGrammar** (executor) — §0. Method and the two counter states — Fixture: git clone of the lane into scratch, branch at 5017e1f7; each case rewrites SCORECARD.md, commits, and is scored twice with the same command
  Evidence: `.ufo/waves/round-47/w1/C2CorrGrammar/report.md`.

- **C2SelfTest** (executor) — record.py --selftest is green and honest about what it runs (10 cases, 0 failures), but it is not calibrated against its own predicate: of 41 single-clause deletions, 18 turn at least one case red and 23 do not…
  Evidence: `.ufo/waves/round-47/w1/C2SelfTest/report.md`.

### C1 review (attackers)

- **RevC1Before** (reviewer) — **GAP: no `report.md`** at draft time; 11 artifact(s) present: `at-HEAD-A1-freeze.json`, `at-HEAD-A6-freeze.json`, `at-HEAD-prompt-freeze.json`, `at-landing-A1-freeze.json`, `at-landing-e856beb5.json`, `at-landing-v2-profile.json`. Evidence: `.ufo/waves/round-47/w1/RevC1Before/`.
- **RevC1Ids** (reviewer) — **GAP: no `report.md`** at draft time; 5 artifact(s) present: `c1-battery-tip.json`, `c1-battery.json`, `c2-at-tip.json`, `c2-head.json`, `receipts`. Evidence: `.ufo/waves/round-47/w1/RevC1Ids/`.
- **RevC1Tokens** (reviewer) — Clause 5 is implemented as a real equality and is not satisfiable by a forged *cell* (only symbol, once, digest, order survive --profile v3), but it is satisfiable by a forged matrix: it does not bind the arm token to the routed id, does not require a permutat…
  Evidence: `.ufo/waves/round-47/w1/RevC1Tokens/report.md`.

- **RevC1Digest** (reviewer) — §0. Two facts that frame everything below — Freeze re-derivation returns the tip, not the first freeze. git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/ at 1e2c3102 → 1e2c3102952dc636650095643c1963c833859019 (i.e. HEAD, the A4 amendment commit). The claim's own re-derivation rule is "t…
  Evidence: `.ufo/waves/round-47/w1/RevC1Digest/report.md`.

- **RevC1Order** (reviewer) — **GAP: no `report.md`** at draft time; 1 artifact(s) present: `receipts`. Evidence: `.ufo/waves/round-47/w1/RevC1Order/`.
- **RevC1Refs** (reviewer) — Clause 8 is the loosest clause in the matrix: it asks whether a *string* resolves, never whether the citation *is evidence for the row it sits beside*…
  Evidence: `.ufo/waves/round-47/w1/RevC1Refs/report.md`.

- **RevC1Last** (reviewer) — Clause 1 (exact.py:191, enforced at :194-197) is a statement about a fence-unaware line splitter (craft_section :101-108 splits on the first \n## …
  Evidence: `.ufo/waves/round-47/w1/RevC1Last/report.md`, `.ufo/waves/round-47/w1/RevC1Last/cases-all.json`, `.ufo/waves/round-47/w1/RevC1Last/revc1last-attack.py`.

- **RevC1Battery** (reviewer) — 1. The four forgeries ARE built from the landed block. Not hand-written: run_battery re-reads SKILL.md at --rev (exact.py:334-337), takes the marked block, and applies each mutation to it; the four fixture SKILL.md files are byte-identical to the landed file o…
  Evidence: `.ufo/waves/round-47/w1/RevC1Battery/report.md`.

### C2 review (attackers)

- **RevC2Before** (reviewer) — §1. The before-state replicates, and each of its four atoms is independently confirmed — python3 -I -B tools/round-47/record.py --root <LANE> --rev 13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5 --json-out <OUT> → exit 1, atoms 50, verified 46, mismatches 4, corrections 0, atoms_by_class {axes 2, path 12, rev 33, seats 2, window 1}, stdout sha256 53d81a…
  Evidence: `.ufo/waves/round-47/w1/RevC2Before/report.md`.

- **RevC2Scope** (reviewer) — §0. Bytes evaluated (pinned) — All counters below were executed from a byte-frozen copy of those files materialised with git cat-file -p 5017e1f:<path> under /fast/scratch/hyaku/kaidoku-r47/RevC2Scope/frozen/tools/, never from the lane worktree…
  Evidence: `.ufo/waves/round-47/w1/RevC2Scope/report.md`.

- **RevC2Exempt** (reviewer) — report present (17734 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/RevC2Exempt/report.md`.

- **RevC2Window** (reviewer) — §1. The four mandated vectors — verdicts — The three detections in k05/k13/k14 are real but incidental: k05 fails because the arm drops the pathspec entirely and grades the whole range, and k13/k14 fail because git still prints the D/A side of the rename. None of them is a clause.
  Evidence: `.ufo/waves/round-47/w1/RevC2Window/report.md`, `.ufo/waves/round-47/w1/LabWindowProbe/receipts/evil-merge-transcript.txt`, `.ufo/waves/round-47/w1/LabWindowProbe/window-receipt.json`.

- **RevC2Axes** (reviewer) — §0. The measurement, pinned — The lane moved under this review: HEAD was 3186f69b at first read, the L1 landed e856beb5 → 07d2894e → a631bba0 → 04469ee8 → f54b3b6d → a0753786 → 31b092d1 → f7d6e58d → 09a9f912 (15 commits since the freeze) while I was measuring…
  Evidence: `.ufo/waves/round-47/w1/RevC2Axes/report.md`, `.ufo/waves/round-47/w1/ScribeShonen/receipts/commandA-at-A4.json`.

- **RevC2Dispatch** (reviewer) — **GAP: no `report.md`** at draft time; 14 artifact(s) present: `axes-correction.out`, `base-c2.json`, `c2-at-07d2894.json`, `c2-at-caafeffa.json`, `drive.py`, `ghost-order.out`. Evidence: `.ufo/waves/round-47/w1/RevC2Dispatch/`.
### critique (falsifiers)

- **CritC1Predicate** (critic) — A block that teaches nothing reaches exit 0 with the *same* battery receipt as the landed block. The predicate is a schema check: it reads the table's grammar and the two pins, never the matrix's content.
  Evidence: `.ufo/waves/round-47/w1/CritC1Predicate/report.md`.

- **CritC1Sizing** (critic) — the target holds at f7d6e58 — failing == [], exit 0, battery 4/4/0/1/0 — but the predicate is too weak in four measured ways (exit column is a digit set, not a meaning…
  Evidence: `.ufo/waves/round-47/w1/CritC1Sizing/report.md`, `.ufo/waves/round-47/w1/CritC1Sizing/receipts/final/c1-tip-full.json`.

- **CritC1Order** (critic) — §1. Objects measured, and their bytes — The freeze series is now 5017e1f7 → A1 9018c53b → A2 62e33f7d → A3 2e4ae43 → A4 1e2c310 → A5 07d2894e → A6 f54b3b6d…
  Evidence: `.ufo/waves/round-47/w1/CritC1Order/report.md`.

- **CritC2Calibration** (critic) — Predicate too weak. At the tip b1a058f3 (and at 09a9f912 before it) the counter's mismatches == [] rests on 39 of 44 atoms being token-resolvability (a backticked hex resolves, a .ufo/waves/… path exists); of the 5 claim-carrying atoms, 1 is exempted, 1 is the…
  Evidence: `.ufo/waves/round-47/w1/CritC2Calibration/report.md`, `.ufo/waves/round-47/w1/CritC2Calibration/fixtures/c2-attack.py`, `.ufo/waves/round-47/w1/CritC2Calibration/fixtures/command-a.py`, `.ufo/waves/round-47/w1/CritC2Calibration/fixtures/probes.py`.

- **CritC2Corrections** (critic) — R47-C2's exemption route does not have to be about the atom it exempts. Cheapest false-but-passing card: fixture $S/fx base 03ff8de444947739eee57d66137a7c2675c5847f, card commit deda0d5ca7a6fbbb9fba8211de7debd309e3fc6e
  Evidence: `.ufo/waves/round-47/w1/CritC2Corrections/report.md`.

- **CritC2Axes** (critic) — The axes atom is the first n/m in the row tail (record.py:39-40, :173-183); the score cell the axis is scored on is never read, so 138/138 coexists with 9.72 → 8.40 or 42.0 → 99.9. Today's 9.72 → 10.0 is true (70/72 at the card's baseline 6645585…, 138/138 and…
  Evidence: `.ufo/waves/round-47/w1/CritC2Axes/report.md`.

- **CritC2Scope** (critic) — Clause 5 (sections = the last two ## Round N headings) is a *scope choice*, not a check: the claimant picks the window, the window moves whenever a heading is added, and SCORECARD.md's heading parser counts duplicate, in-fence and non-round headings…
  Evidence: `.ufo/waves/round-47/w1/CritC2Scope/report.md`.

- **CritBattery** (critic) — report present (24239 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/CritBattery/report.md`, `.ufo/waves/round-47/w1/CritBattery/receipts/manifest.jsonl`.

- **CritDigest** (critic) — predicate too weak, here is what closes it.
  Evidence: `.ufo/waves/round-47/w1/CritDigest/report.md`, `.ufo/waves/round-47/w1/CritDigest/fx-a1b.recheck.json`.

- **CritGold** (critic) — Full findings, per-claim clause numbers and smallest safe corrections: ../CritGold.md. Receipts: receipts/. Reproduce: sh rebuild.sh.
  Evidence: `.ufo/waves/round-47/w1/CritGold/report.md`.

### mutation (clause deletion / artefact mutation)

- **MutExactClauses** (mutation-tester) — §1. What was measured — Seventeen behaviour-bearing checks inside score() — the nine predicate clauses of plans/round-47-claims.md R47-C1, resolved into the independent checks the code actually contains — were deleted one at a time from a scratch copy, and three detectors were run on…
  Evidence: `.ufo/waves/round-47/w1/MutExactClauses/report.md`.

- **MutRecordClauses** (mutation-tester) — **GAP: no `report.md`** at draft time; 1 artifact(s) present: `receipts`. Evidence: `.ufo/waves/round-47/w1/MutRecordClauses/`.
- **MutBlock24** (mutation-tester) — 1. The core discrimination table holds: 13/13 mutations killed by v3, 12/13 green under v2. Every category the seat names (token, id, cells, exit, title, marker, header, digest, pin, refs) has at least one mutation that v3 catches and v2 does not. 2. 11 of 27…
  Evidence: `.ufo/waves/round-47/w1/MutBlock24/report.md`, `.ufo/waves/round-47/w1/MutBlock24/mut13.py`, `.ufo/waves/round-47/w1/MutBlock24/receipts/mut13-at-landing.json`.

- **MutRecordAtoms** (mutation-tester) — Baseline at 07d2894e is green: record.py exit 0, atoms 41, verified 40, corrections 2, corrections_bad [], exempted 1, battery.forgeries_green 0, met_target true (receipts/M0-baseline.json)…
  Evidence: `.ufo/waves/round-47/w1/MutRecordAtoms/report.md`.

- **MutCorrections** (mutation-tester) — §0. Instrument and measured bytes — Counting command, every row below (both modes run from the clone so the detector and the bytes are the same revision)
  Evidence: `.ufo/waves/round-47/w1/MutCorrections/report.md`.

- **MutGate** (mutation-tester) — **GAP: no `report.md`** at draft time; 2 artifact(s) present: `mutate.py`, `receipts`. Evidence: `.ufo/waves/round-47/w1/MutGate/`.
- **MutScratch** (mutation-tester) — TMPDIR=/tmp → no counter writes under /tmp. C1 refuses at the call site before mkdtemp (exit 2, reason quoted above, 0 mkdir/mkdirat under /tmp in the strace); C2 has no scratch surface at all (P2–P4 byte-identical receipts, 0 /tmp syscalls). A "counter that w…
  Evidence: `.ufo/waves/round-47/w1/MutScratch/report.md`, `.ufo/waves/round-47/w1/MutScratch/c1-own-head.json`, `.ufo/waves/round-47/w1/MutScratch/nodir/x.json`.

- **MutExitCodes** (mutation-tester) — **GAP: no `report.md`** at draft time; 15 artifact(s) present: `drive.py`, `drive2.py`, `drive3.py`, `drive4.py`, `drive5.py`, `drive6.py`. Evidence: `.ufo/waves/round-47/w1/MutExitCodes/`.
### cross-seat connectors

- **ConnSeparability** (connector) — §1. The method — D=/fast/scratch/hyaku/kaidoku-r47/ConnSeparability/repo3 # full clone of the lane git -C "$D" rev-parse --show-toplevel # asserted == $D before every commit
  Evidence: `.ufo/waves/round-47/w1/ConnSeparability/report.md`.

- **ConnRouted** (connector) — §2. Five attacks on the frozen instruments — Each attack is a fixture, not an edit: the originals were read from git objects and the altered bytes were committed only inside a throwaway repo under my scratch root. Scripts and outputs are in this directory.
  Evidence: `.ufo/waves/round-47/w1/ConnRouted/report.md`.

- **ConnSiblings** (connector) — §1. What was measured — Both frozen instruments were executed at the revisions named, plus eight forgery fixtures built from git clone --no-hardlinks of the lane (toplevel asserted equal to the fixture dir before the first fixture commit, throwaway identity configured inside the fixt…
  Evidence: `.ufo/waves/round-47/w1/ConnSiblings/report.md`.

- **ConnCraft** (connector) — Block 24 is half a real move. Against the ancestor's own standard it closes three of the four holes it names — cardinality (once) genuinely new, the digest (digest) a real strengthening of a rule block 23 only stated weakly, and the arm-vocabulary equality (sy…
  Evidence: `.ufo/waves/round-47/w1/ConnCraft/report.md`.

### sentinels (scope / fixtures)

- **SentScope** (sentinel) — Headline: neither counter writes outside the lane root, and neither can be made to execute code by artefact content…
  Evidence: `.ufo/waves/round-47/w1/SentScope/report.md`.

- **SentFixtures** (sentinel) — **GAP: no `report.md`** at draft time; no artifacts. Evidence: `.ufo/waves/round-47/w1/SentFixtures/`.
### revengers (intent / history)

- **RevIntent** (revenger) — Clause 7 protects the spelling of the arm — "-m", "--diff-merges=first-parent" present once and its reverse absent, in gate.py's committed bytes at --rev — and it does protect that one thing correctly…
  Evidence: `.ufo/waves/round-47/w1/RevIntent/report.md`.

- **RevHistory** (revenger) — The two round-46 record atoms failed for different reasons at different times, and only one of them is a freeze case
  Evidence: `.ufo/waves/round-47/w1/RevHistory/report.md`.

### falsifiable probes

- **LabOrderProbe** (executor) — 1. The premise of clause 7 is TRUE and now measured. On a deterministic two-parent merge the argument order is semantic, not cosmetic: git lets the *last* diff-merges selector win, so -m --diff-merges=first-parent shows the merge once (24 bytes) and --diff-mer…
  Evidence: `.ufo/waves/round-47/w1/LabOrderProbe/report.md`.

- **LabWindowProbe** (executor) — Yes, exactly one non-degenerate candidate window is empty: 332f4884..58eb04b6 (0 bytes, rc 0, every arm)…
  Evidence: `.ufo/waves/round-47/w1/LabWindowProbe/report.md`.

### simplifiers (YAGNI)

- **SimplC1** (simplifier) — **GAP: no `report.md`** at draft time; 5 artifact(s) present: `attack`, `receipts`, `receipts.tsv`, `run-a6.json`, `run-head.json`. Evidence: `.ufo/waves/round-47/w1/SimplC1/`.
- **SimplC2** (simplifier) — Clause 2 *as implemented* is self-referential
  Evidence: `.ufo/waves/round-47/w1/SimplC2/report.md`.

### scouts (maps)

- **ScoutCraftTail** (scout) — report present (11077 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/ScoutCraftTail/report.md`.

- **ScoutSources** (scout) — report present (8225 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/ScoutSources/report.md`.

- **ScoutAxes** (scout) — report present (12971 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/ScoutAxes/report.md`, `.ufo/waves/round-47/w1/ScoutAxes/record-at-freeze.json`.

- **ScoutRounds** (scout) — Two Wave/Waves sentences carry seat counts. Round 46 Waves: 40 + 40 = 80 seats is verifiable and matches w1/w2 counts.spawn (40 and 40); there is no w3-dispatch.json. Round 45 Wave 1: 40 seats; wave 2: 32 seats is verifiable and false: dispatch spawn is 40 and…
  Evidence: `.ufo/waves/round-47/w1/ScoutRounds/report.md`.

- **ScoutDispatch** (scout) — report present (5000 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/ScoutDispatch/report.md`, `.ufo/waves/round-47/w1/ScoutDispatch/receipts/record-at-HEAD.json`, `.ufo/waves/round-47/w1/ScoutDispatch/receipts/record-at-freeze.json`.

- **ScoutCraftBlocks** (scout) — report present (6185 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/ScoutCraftBlocks/report.md`.

- **ScoutTools** (scout) — report present (17124 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/ScoutTools/report.md`.

- **ScoutState** (scout) — report present (44119 B); no verdict field in a recognisable form, so no result is asserted here.
  Evidence: `.ufo/waves/round-47/w1/ScoutState/report.md`, `.ufo/waves/round-47/w1/C1Battery/base-v3.json`, `.ufo/waves/round-47/w1/C1Digest/receipt.json`, `.ufo/waves/round-47/w1/C1Ids/receipt-head.json`, `.ufo/waves/round-47/w1/C1Ids/receipt.json`.

### drafting (scribes)

- **ScribeBlock24** (scribe) — **GAP: no `report.md`** at draft time; 4 artifact(s) present: `block24-passing.md`, `block24.md`, `landed-block24.md`, `receipts`. Evidence: `.ufo/waves/round-47/w1/ScribeBlock24/`.
- **ScribeCorrections** (scribe) — **GAP: no `report.md`** at draft time; 7 artifact(s) present: `c1-at-2e4ae434.json`, `c1-orig-freeze-at-HEAD.json`, `c2-at-2e4ae434.json`, `c2-at-3186f69b.json`, `c2-at-e856beb5.json`, `corrections.md`. Evidence: `.ufo/waves/round-47/w1/ScribeCorrections/`.
- **ScribeAxesRow** (scribe) — **GAP: no `report.md`** at draft time; 2 artifact(s) present: `axes.md`, `receipts`. Evidence: `.ufo/waves/round-47/w1/ScribeAxesRow/`.
- **ScribeLesson** (scribe) — **GAP: no `report.md`** at draft time; 5 artifact(s) present: `MANIFEST.txt`, `lesson.md`, `receipts`, `self-exact.txt`, `self-record.txt`. Evidence: `.ufo/waves/round-47/w1/ScribeLesson/`.
- **ScribeQuality** (scribe) — **GAP: no `report.md`** at draft time; 12 artifact(s) present: `c1-at-head-a1-freeze.json`, `c1-at-head-first-freeze.json`, `c1-at-head.json`, `c2-at-head.json`, `probe-axes-correction.py`, `probe-noop-mutation.py`. Evidence: `.ufo/waves/round-47/w1/ScribeQuality/`.
- **ScribeSources** (scribe) — **GAP: no `report.md`** at draft time; 9 artifact(s) present: `pins.json`, `receipts.jsonl`, `receipts.py`, `receipts2.jsonl`, `receipts2.py`, `receipts3.jsonl`. Evidence: `.ufo/waves/round-47/w1/ScribeSources/`.
- **ScribeShonen** (scribe) — **GAP: no `report.md`** at draft time; 2 artifact(s) present: `receipts`, `shonen.md`. Evidence: `.ufo/waves/round-47/w1/ScribeShonen/`.
- **ScribeReport** (scribe) — **GAP: no `report.md`** at draft time; 15 artifact(s) present: `a2-record-at-tip.json`, `compose.py`, `exact-atA6.json`, `exact-f1e2c310-r1e2c310.json`, `exact-f5017e1f-r1e2c310.json`, `exact-f62e33f7-r1e2c310.json`. Evidence: `.ufo/waves/round-47/w1/ScribeReport/`.
### Gaps (no report at draft time)

These seats have directories (and in most cases artifacts) but no `report.md`, so nothing they produced is stated as a result above:

`ScribeBlock24`, `ScribeCorrections`, `ScribeAxesRow`, `ScribeLesson`, `ScribeQuality`, `ScribeSources`, `ScribeReport`, `ScribeShonen`, `RevC1Before`, `RevC1Ids`, `RevC1Order`, `RevC2Dispatch`, `MutRecordClauses`, `MutGate`, `MutExitCodes`, `SentFixtures`, `SimplC1`

## Landed changes

Derived from git, not from a seat: `git log --format='<hash> <subject>' 13a9e9e1..b1a058f3`.

- `b1a058f3` (2026-10-28 15:05:56 -0300) — round-47: final receipts at the tip
  Files: `.ufo/waves/round-47/l1/scores/c1-at-FINAL.json`, `.ufo/waves/round-47/l1/scores/c2-at-FINAL.json`.

- `6f9fd7f8` (2026-10-28 15:01:44 -0300) — round-47: record quotes its own receipts (atoms 42, exempted 1); axes repaired in place; M47-8/M47-9 and CL12-CL14
  Files: `SCORECARD.md`, `corpus/lessons/round-47.md`.

- `09a9f912` (2026-10-28 15:00:37 -0300) — round-47: route the wave's two strongest findings (R47-CL10 gold forgery, R47-CL11 stale declared freeze)
  Files: `corpus/lessons/round-47.md`.

- `f7d6e58d` (2026-10-28 14:59:20 -0300) — round-47: route the wave's instrument findings (R47-CL6/CL7/CL9) and land the R4 receipts
  Files: `.ufo/waves/round-47/l1/scores/c1-at-R4.json`, `.ufo/waves/round-47/l1/scores/c2-at-R4.json`, `corpus/lessons/round-47.md`.

- `31b092d1` (2026-10-28 14:58:52 -0300) — round-47: record the A6 freeze and the A7 measurement; M47-7 and R47-CL8
  Files: `.ufo/waves/round-47/l1/scores/c1-at-A7.json`, `.ufo/waves/round-47/l1/scores/c2-at-A7.json`, `SCORECARD.md`, `corpus/lessons/round-47.md`.

- `a0753786` (2026-10-28 14:58:27 -0300) — round-47: block 24's interpreter pin follows A6; the v2-profile control
  Files: `.ufo/waves/round-47/controls/ctl-c1-1-v2-profile.json`, `.ufo/waves/round-47/l1/scores/c1-at-A6.json`, `.ufo/waves/round-47/l1/scores/c1-at-R3.json`, `.ufo/waves/round-47/l1/scores/c2-at-A6.json`, `.ufo/waves/round-47/l1/scores/c2-at-R3.json`, `SKILL.md`.

- `f54b3b6d` (2026-10-28 14:58:08 -0300) — round-47: A6 - the battery fixture carries every citation the landed block names
  Files: `tools/round-47/exact.py`.

- `04469ee8` (2026-10-28 14:57:00 -0300) — round-47: block 24 cites a knowledge entry (proxy harm repaired); calibration row head; M47-6
  Files: `.ufo/waves/round-47/l1/scores/c1-at-R2.json`, `.ufo/waves/round-47/l1/scores/c2-at-R2.json`, `SCORECARD.md`, `SKILL.md`, `corpus/lessons/round-47.md`.

- `a631bba0` (2026-10-28 14:56:04 -0300) — round-47: A5 in the record, the LOG and the lesson; both claims' A5 receipts
  Files: `.ufo/waves/round-47/l1/scores/c1-at-A5.json`, `.ufo/waves/round-47/l1/scores/c1-at-R1.json`, `.ufo/waves/round-47/l1/scores/c2-at-A5.json`, `.ufo/waves/round-47/l1/scores/c2-at-R1.json`, `SCORECARD.md`, `corpus/lessons/round-47.md`.

- `07d2894e` (2026-10-28 14:55:37 -0300) — round-47: A5 - the ghost-atom forgery lands inside the corrections section
  Files: `tools/round-47/record.py`.

- `caafeffa` (2026-10-28 14:53:05 -0300) — round-47: record - the round section, the LOG entry, the lesson with its gate, QUALITY row 78, S144, and both counters' receipts
  Files: `.ufo/waves/round-47/l1/scores/c1-at-A2.json`, `.ufo/waves/round-47/l1/scores/c1-at-A4.json`, `.ufo/waves/round-47/l1/scores/c1-at-L1.json`, `.ufo/waves/round-47/l1/scores/c2-at-A2.json`, `.ufo/waves/round-47/l1/scores/c2-at-A4.json`, `.ufo/waves/round-47/l1/scores/c2-at-L1.json`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-47.md`.

- `1e2c3102` (2026-10-28 14:52:38 -0300) — round-47: A4 - the historical-correction selftest fixture gets its round-3 dispatch
  Files: `tools/round-47/record.py`.

- `2e4ae434` (2026-10-28 14:51:50 -0300) — round-47: A3 - a seats/window correction for a round older than the window stays valid evidence
  Files: `tools/round-47/record.py`.

- `62e33f7d` (2026-10-28 14:51:02 -0300) — round-47: A2 - make the window forgery a real forgery; block 24 arm cells carry only the token
  Files: `SKILL.md`, `plans/round-47-claims.md`, `tools/round-47/record.py`.

- `e856beb5` (2026-10-28 14:50:37 -0300) — round-47: land craft block 24, the record corrections, the current axis heads and S143
  Files: `SCORECARD.md`, `SKILL.md`, `corpus/SOURCES.md`.

- `9018c53b` (2026-10-28 14:47:25 -0300) — round-47: freeze amendment A1 - drop the unreachable window-pair clause
  Files: `.ufo/waves/round-47/controls/ctl-c2-2-freeze-amendment.json`, `plans/round-47-claims.md`, `tools/round-47/record.py`.

- `3186f69b` (2026-10-28 14:45:08 -0300) — round-47: wave-1 spec, dispatch and freeze controls
  Files: `.ufo/waves/round-47/controls/ctl-c1-0-do-nothing.json`, `.../waves/round-47/controls/ctl-c1-2-freeze-battery-absent.json`, `.ufo/waves/round-47/controls/ctl-c2-0-do-nothing.json`, `.ufo/waves/round-47/gen-w1.py`, `.ufo/waves/round-47/w1-dispatch.json`, `.ufo/waves/round-47/w1-spec.json`, `.ufo/waves/round-47/w1/swarm-registry.json`.

- `5017e1f7` (2026-10-28 14:32:59 -0300) — round-47: freeze the exactness counter and the self-assessment re-derivation counter
  Files: `plans/round-47-claims.md`, `tools/round-47/exact.py`, `tools/round-47/record.py`.

### Draft notes for the L1 (not part of the report)

- Wave tree at generation: **31 paths tracked** at `b1a058f3`, **148 untracked**. Seat evidence cited above does not resolve at a rev until the wave tree is committed; `record.py`'s `path` atom class checks exactly that.
- C1's counter is green only at `--freeze == --rev` (task freeze `5017e1f7` and every declared amendment A1–A6 exit 2 `frozen_path_changed`). Cite the freeze as the literal measured rev and disclose the degenerate pairing — see `ScribeReport.md` F1.
- `record.py` has no freeze guard and its `CORR` regex cannot parse `axes` corrections (F3/F4): `corrections: 2` is two of the four lines the card carries.
- Every bullet above is a quote from the named seat's own `report.md`; a bullet is absent, not softened, where the seat had not reported at generation time.

