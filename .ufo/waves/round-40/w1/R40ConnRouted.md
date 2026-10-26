# R40ConnRouted — round-40 routed-defect ledger (pre-freeze)

**Verdict: DONE.** Ledger produced for the round-40 lesson: all routed defects carried into round 40 are connected to the draft `plans/round-40-claims.md`; the draft binds/claims 6 of 6 open R39 defects (CL1–CL6, one partially); **5 carried items are silently dropped by the draft (M39-2 class)** and are flagged for the freeze: R36-CL5, the `heldout-gen.py` `corruption_bad_minor` docstring erratum, loose SOURCES anchors S118/S121, surviving interpreter/counter mutants, and the non-exit-code parts of R39-CL6 (cross-domain-evidence line, seat status).

## 1. Method and evidence base

Read (all at lane base, `HEAD = fa6a8a3f85ec65946b3a54d37c0ddd1d6748664f` = the assignment's base; verified with `git rev-parse HEAD` and `git log --oneline -5`):

- `plans/round-40-claims.md` (the DRAFT; lines cited below refer to it);
- `corpus/lessons/round-39-verifier-spotcheck.md` §5 (R39-CL1..CL6 + "Still open" list);
- `corpus/lessons/round-39.md` `## Routed defects` ledger (states of R38-CL1..4, R36-CL2..6);
- `corpus/lessons/round-36-verifier-spotcheck.md` §Routed defects (R36-CL1..CL6 definitions);
- `corpus/lessons/round-38-verifier-spotcheck.md` §5 (R38-CL1..CL4 definitions);
- `SCORECARD.md` `## Round 39` last bullets (`:3432`): " (a) a counter clause that binds a C1 receipt to an in-round re-run … (b) an out-of-set envelope the triage table must label `unclassified` … Second choice: coverage on the AVM-BE branch" — the draft's line 12-13 takes (a) as a binding inside R40-C1 and (b) as part of R40-C2, and works the AVM branch as the coverage surface;
- `corpus/SOURCES.md` S112–S122 rows (S114 = Freetz AVM-BE format note; S118/S121 anchor gaps confirmed present);
- `.ufo/waves/round-39/w2/R39W2TriageMutants.md`, `R39W2C2Mutants.md` (exist; the-round-39 lesson records 18/39 interpreter mutants and 9 counter mutants surviving);
- w2 findings D1/F3 (`R39W2C2Shortcut.md`, `R39W2ScribeScorecard.md`) for the `corruption_bad_minor` erratum (`tools/round-39/heldout-gen.py:218`).

No REA/unblob run, no downloads, no installs (nothing installed/updated this session; no tools written), no scratch used (pure reads + one lane-internal write). Bounds respected: only this report is written, inside the lane.

## 2. Ledger (for the round-40 lesson)

State at round start = at base `fa6a8a3f` (round-39 closure landed). Action vocabulary: claim / binding / hygiene / none. "silently dropped" = no mention anywhere in the draft.

### 2a. Closed (state at round start: fixed/superseded) — round-40 action: none

| id | source | state at round start | round-40 action | evidence the closure can check |
|---|---|---|---|---|
| R38-CL1 (false absence sweep) | r38 spotcheck §5 | fixed in round 39 (QUALITY 82; `absence-sweep.py`) | none | r39 lesson corrections; `absence-sweep.py --selftest` 18 cases; exit 0 ABSENT at fleet root, exit 1 PRESENT adding shokuknow root |
| R38-CL2 (unregistered gates) | r38 spotcheck §5 | fixed in round 39 (selftest modes; registry rows) | none | SKILL.md `### Round-35/37/38/39 instrument registry` rows; `--selftest` on `freeze-drift.py`/`intended-doc.py`/`registry-immutable.sh` |
| R38-CL3 (overstatement "turned C1 green") | r38 spotcheck §5 | fixed (correction recorded) | none | r39 lesson correction: "carrier-green" wording |
| R38-CL4 (gate redness vs ships_freeze_bytes) | r38 spotcheck §5 | fixed in round 39 (freeze-integrity rule) | none (rule carried) | r39 claims `## Freeze-integrity rule`; counters exit 2 `frozen_path_changed`; draft :15-20 inherits |
| R36-CL1 (untracked w2 stamp) | r36 spotcheck | fixed (`e059ca93`) | none | `git log` on `w2.ready.dispatched` |
| R36-CL2 (frontier pointer names missing) | r36 spotcheck | fixed in round 39 (PROVINCE `:384` names the r36 entry stem) | none | PROVINCE.md:384 supersession note |
| R36-CL3 (counter blind spots) | r36 spotcheck | superseded in round 39 | partial: its C1 F1 arm (re-hashed envelope) is re-routed as R39-CL5 → claimed by R40-C1; its C2 A1–A6 (shadow rows/decoys) → covered by R40-C2 v2 unique labels + scored action + kill controls; the mutant/skip-control parts remain unbound (see 2b flags) | r39 lesson ledger; draft :42-45, :61-65, :79-82, :95-97 |
| R36-CL4 (freeze had no map) | r36 spotcheck | fixed for round 39 | none (inherited) | r39 claims freeze path list; `carriers.json` pins |
| R36-CL6 (subject.local_path into deleted scratch) | r36 spotcheck | fixed for round 39 (`subject.digest.sha256` binding) | none | C1 `subject_pin_ok`; draft :42 subject digest = carrier pin |

### 2b. Open — routed into the round-40 draft

| id | source | state at round start | round-40 action | evidence the closure can check |
|---|---|---|---|---|
| R39-CL1 (no domain guard; non-firmware envelopes labelled) | r39 spotcheck §5 | open | **binding** — R40-C2: domain-guard columns `operation`/`provider`; non-`extract_firmware`/non-`unblob` envelopes fall through to `unclassified` (planned (b)) | draft :75-76, :94 class `out-of-domain`; kill control catch-all (:96); predicate P40-C2 assigns (label, action) for all held-out envelopes |
| R39-CL2 (v1 block lacks mixed-symlink caveat; K5/K6 action contradicts their in-tree gaps) | r39 spotcheck §5 | open | **binding** — R40-C2: `mixed-symlinks` row ahead of the escaping row | draft :77, :92 class `mixed-symlinks`; row order testable in v2 table bytes |
| R39-CL3 (rows 5/8 exclude measured outcomes; cause→action unscored; 20 = 9 decisions) | r39 spotcheck §5 | open | **binding** — R40-C2: `partial-body-failure` (P>0) row with published files; `clean-empty` zero-files row; scored closed-vocabulary `action` column; unique labels per row; held-out replicates differ in a non-decision feature; counter reports number of distinct row decisions | draft :78-82, :91-93 classes, :96 kill controls `label-right/action-wrong`; predicate "number of distinct row decisions" and per-envelope (label, action) equality |
| R39-CL4 (kill-control `.formatfix` inputs landed after the freeze; CTL-C2-5/6 unevaluable) | r39 spotcheck §5 | open | **binding** — freeze-integrity rule: control tables and control receipts' inputs committed and format-validated in the freeze commit itself | draft :19-20 "(routed R39-CL4)"; closure checks control inputs exist in the freeze commit and validate |
| R39-CL5 (C1 counter cannot refuse a re-minted fabricated receipt) | r39 spotcheck §5 + `w2/R39W2C1Fabricate.md` | open | **claim** — R40-C1: the counter re-runs REA itself at scoring time on each carrier (scratch outdir) and compares a frozen semantic projection with the committed receipt; kill control "a receipt fabricated from the oracle with a re-minted evidence id (must now fail the rerun binding)" | draft :42-45, :62; predicate P40-C1 rerun clause; closure runs CTL-C1 fabricated-oracle control and expects exit 1 / no `met_target` |
| R39-CL6 (no exit codes in receipts; no cross-domain-evidence line; seat status null) | r39 spotcheck §5 | open (partial) | **binding** only for the exit-code part: "every score receipt records the counter's exit code (R39-CL6)" (draft :20). The cross-domain-evidence line and per-seat status are **not addressed** → see flag below | closure reads `l1/scores/*.json` for a non-null `exit_code` field |

### 2c. Open — silently dropped by the draft (M39-2 class, must be carried)

| id | source | state at round start | round-40 action | evidence the closure can check |
|---|---|---|---|---|
| R36-CL5 (instruments still fail QUALITY rows 33, 39, 45, 58, 60, 68) | r36 spotcheck §Routed defects; carried in r39 lesson ledger ("open") | open since round 36 | **none in draft — silently dropped.** Action: hygiene — either bind a QUALITY-conformance clause in a claim (preferred for the new counters) or record "still open" in the round-40 lesson | no draft mention; closure greps the draft for "QUALITY 33/39/45/58/60/68"; checks the new tools against the rows |
| `heldout-gen.py` `corruption_bad_minor` docstring erratum | r39 spotcheck §5 last bullet; `w2/R39W2C2Shortcut.md` D1; `R39W2ScribeScorecard.md` F3 | open (frozen round-39 bytes, erratum only) | **none in draft — silently dropped.** Action: hygiene — record the erratum in the round-40 lesson (bytes stay frozen; `frozen_path_changed` must not trip) | no draft mention; closure reads `tools/round-39/heldout-gen.py:218` vs measured class (handler `squashfs_v4_be`, `extraction_failed` true, gap `extractor-failure`) |
| Surviving interpreter mutants (18/39) | `w2/R39W2TriageMutants.md` | open | none in draft (v2 table/interpreter rewrite supersedes the v1 surface, but no mutant binding or kill control). Action: hygiene — mutate the v2 interpreter/table before the freeze, red-before/green-after | draft kill-control list (:95-97) has no mutant control; closure runs the v2 mutation sweep |
| Surviving counter mutants (9) | `w2/R39W2C2Mutants.md` | open | none in draft (new C1 rerun counter and C2 counter are new code). Action: hygiene — fresh mutation sweep + selftest red/green on both new counters before the freeze | draft has no counter-mutant control; closure runs the sweeps |
| Loose quote anchors S118 (scope omits second report site, lines 58-65) and S121 (`debian/rules` URL+sha unrecorded) | r39 spotcheck §3 | open | **none in draft — silently dropped.** Action: hygiene — either amend the SOURCES rows (append-only per CORPUS rule 2: add the anchor facts) or record as open in the lesson | no draft mention; closure re-opens S118/S121 at the pinned tags and compares anchors |

## 3. Draft-coverage matrix (defect → draft line → wave item)

| defect | draft anchor | wave item |
|---|---|---|
| R39-CL5 | :42-45 (predicate rerun), :62 (kill control) | R40-C1 (coverage, claim) |
| R39-CL1 | :75-76, :94, :96 | R40-C2 (depth, binding) |
| R39-CL2 | :77, :92 | R40-C2 (depth, binding) |
| R39-CL3 | :78-82, :91-93, :96 | R40-C2 (depth, binding) |
| R39-CL4 | :19-20 | freeze-integrity rule (binding, both claims) |
| R39-CL6 (exit-code part) | :20 | freeze-integrity rule (binding, both claims) |
| R36-CL3 (F1 arm) | :42-45, :62 | re-routed as R39-CL5 → R40-C1 |
| R36-CL3 (A1–A6 arm) | :79-82, :95-97 | R40-C2 (depth, binding) |
| R36-CL4 / R38-CL4 | :15-20 | freeze-integrity rule (inherited) |

The planned row mapping (SCORECARD `:3432` → draft :12-13) is faithful: (a) fabrication-limit → R40-C1 binding, (b) out-of-set envelope → R40-C2 `unclassified`, AVM-BE branch → R40-C1 coverage surface.

## 4. Flags for the freeze (M39-2 class — "routed defects dropped between rounds instead of carried with a state")

1. **R36-CL5 — silently dropped** (open since round 36; carried explicitly in the round-39 lesson ledger, absent from the round-40 draft).
2. **`heldout-gen.py` `corruption_bad_minor` docstring erratum — silently dropped** (open, frozen bytes).
3. **Loose SOURCES anchors S118/S121 — silently dropped** (open).
4. **Surviving interpreter mutants (18/39) and counter mutants (9) — unbound**: the new v2 interpreter and both new counters are fresh code with no mutation or red-before selftest requirement in the draft; recommend a "mutant sweep + selftest red cases fail on their own clause" binding for the new tools, or an explicit lesson entry.
5. **R39-CL6 remainder — partially dropped**: only the exit-code half is bound (:20); the cross-domain-evidence report line and per-seat status (wave ledgers) have no round-40 action. These are report/ledger hygiene — put them in the L1 or gate checklist, not silently dropped.

Prevention (M39-2 fix, as in round 39): the round-40 lesson must carry this ledger with every id and its state; the freeze commit should include it. All ids above are re-usable as-is; the four unnamed carried items (erratum, two mutant classes, S118/S121 anchors) are tracked above by description and should be given ids (e.g. R39-CL7..CL10 or R40-CL1..CL4) at the freeze, or they will be re-dropped next round.

## 5. Risks noted (not defects, for the L1)

- R40-C1's rerun binding (CL5) assumes REA runs are deterministic on the pinned carriers; the frozen semantic projection must be defined narrowly enough that benign nondeterminism (ordering of `files[]`, diagnostic text) cannot falsify a real run. The draft fixes "projection fields fixed in the freeze" (:44) — good, but the L1 should also freeze a normalization rule for the projection.
- R39-CL3's "replicates differ in a non-decision feature" is only meaningful if the generator's seed (freeze hash) is bound before data — the draft binds it (:87). Verify the two replicates per class really differ only in non-decision bytes (wave-1 recon should confirm).
- The `unclassified` fallthrough (CL1) must be reached by a **distinct row decision** — with unique labels and the scored action column, `unclassified` must be a label+action pair, not an absence of match, or a catch-all kill control could pass trivially.

## 6. Installs / scratch

Nothing installed or updated (no tool/version/channel/reason entry). No scratch created, no downloads, no REA/unblob/sasquatch runs; the only filesystem write is this report.

Report: .ufo/waves/round-40/w1/R40ConnRouted.md
