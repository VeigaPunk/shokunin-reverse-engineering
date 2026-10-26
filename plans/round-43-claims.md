# kaidoku round 43 — frozen claims

Base `6b9e64fe7e0de202d9383baad5792fbfe039a743` (lane `main` at round start; the round-42 verifier spot-check
`corpus/lessons/round-42-verifier-spotcheck.md` sits on tip `af50af81751bbb02316c9bc9a0459ca96707b0c0`,
ancestor of the base). L1 `KaidokuR43` holds the §3 planner seat (orchestrator ruling 2026-10-19: the validator
rejects `planner` as a swarm role; the L1 is the canonical planner and bounded planning data-walks ride scouts,
connectors and revengers — recorded here per the round contract). Fresh-start round (run-10 directive): the L1 read
the last three rejected closures (rounds 40, 41, 42 verifier spot-checks) before declaring; both claims below are
ones a do-nothing control cannot reach (§9), each with its control scored before any claim data.

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis is a lowest axis.
R43-C1 works depth, R43-C2 works coverage. Both are routed follow-throughs named by prior closures:
R43-C1 lands routed defect R42-CL1 (= QUALITY 85, M42-2: the round-42 held-out generator declared a feature tuple
its own run did not observe, combo C02, and the round stopped on that binding); R43-C2 lands routed defects
R41-CL3/R42-CL3 (the round-42 wave-1 `R42LocalSrc` seat prepared, and proved green in a sandbox clone, in-lane
copies for the 18 `corpus/SOURCES.md` rows the `local-source-gate.py` reds at the base, and the landing was never
committed). Routed defect R42-CL2 (no wave 2 attacked the round-42 landing) is discharged by this round's wave 2,
which includes re-running the round-42 C1 counter against a fresh carrier cache; it is a round-shape item, not a claim.

## Freeze-integrity rule (both claims; carried from rounds 39–42)

A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path of that claim; a later
restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`). Control tables and their development
inputs are committed in the freeze. Every score receipt records the scorer's exit code and `counter_sha256` (the
sha256 of the counter file it ran) plus `counter_sha256_at_freeze` (round-41 closure D4). QUALITY 84: both counters
are dry-run end to end, as frozen, with data produced by the frozen generators in a dev arm, before the freeze, and
the dry-run receipts show every binding evaluated.

## R43-C1 — depth: the v4 SquashFS triage table scored on a fresh held-out set under a generator that refuses unobserved declarations

Surface moved: `SKILL.md` `## Queue-drain craft` rule block 21 (`<!-- sqfs-triage-table v4 -->`) stopped unscored
at round 42 — it matched its independent evaluator 78/78 but the round stopped on `observed_features_match_declared`
because the generator declared a gap set for combo C02 that its own REA run did not observe. This claim does not
change one table byte: it re-freezes the frozen table (bytes proven equal to the round-42 freeze `d1681696` at the
table region), regenerates the held-out set from a NEW seed, and replaces the generator's declared-tuple predictor
with a measured one (QUALITY 85): the generator runs REA on every carrier, extracts the observed six-field feature
tuple from each envelope it produced, and REFUSES to write the manifest unless every observed tuple equals the tuple
the manifest would declare; on refusal it exits non-zero and writes no manifest. The counter additionally binds the
manifest's own record of that check. Command that shows it unmoved: the round-43 C1 counter at the freeze exits 2
(`no_manifest_at_rev`), and the round-42 stop receipt stays byte-committed at
`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`.

**Predicate P43-C1** (implemented by `tools/round-43/c1-counter.py`; its docstring's clause list is the full text).
At the measured revision: the v4 table region of `SKILL.md` (from the line containing `<!-- sqfs-triage-table v4 -->`
through the end of the first markdown table after it) is byte-identical to the same region at `d1681696`; the
frozen interpreter `tools/round-42/sqfs-triage-v4.py` and the frozen evaluator `tools/round-42/indep-eval-v4.py`
are byte-identical at `d1681696`, at the freeze, and at the measured revision (no commit in
`d1681696..REV` touches them); the held-out set is `corpus/evidence/round-43/c1/heldout/` produced by
`python3 -I -B tools/round-43/heldout-gen-v4r43.py --seed <FREEZE> --out corpus/evidence/round-43/c1/heldout --run --scratch <scratch under /fast/scratch/hyaku/kaidoku-r43/>`, first added in a commit descending from the freeze,
with the same class structure as round 42 (27 named classes × 2 plus 24 combo carriers, n = 78) and the same
`declared_features` single-key contract (R41-CL1); every envelope's observed six-field tuple equals its declared
tuple (the round-42 stop binding, now expected true); the manifest records the generator's own tuple check
(`generator.tuple_check`: per-carrier observed/declared verdicts, all equal) and the refusal rule is demonstrated
red/green in the committed controls; the frozen interpreter gives every held-out envelope the same (label, action)
pair as the frozen evaluator; the frozen lookup control `.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` run
through the frozen interpreter scores strictly fewer than half of the held-out `combo` envelopes
(`combo_unseen_majority` ≥ 12 of 24); the round-41 C1 receipts and the round-42 dev-arm envelopes get the
evaluator's pair; every carrier regenerates byte-identically from the seed; the seed equals the freeze commit hash;
every envelope's subject digest equals its carrier's sha256; the fixtures the carriers embed are the pinned unblob
26.6.4 MIT fixtures (`tools/round-42/fixtures.json`), whose license basis is cited by the new SOURCES row S135
opened this round; no frozen C1 path changed after the freeze.

- The generator change (QUALITY 85 / R42-CL1): in `heldout-gen-v4r43.py` (a port of `tools/round-42/heldout-gen-v4.py`),
manifest finalization is preceded by a tuple check: for each carrier, `observed_features(envelope)` (the same
extraction the round-42 dev proof uses) is compared with the tuple about to be declared; any difference refuses the
manifest (exit 3 `declared_tuple_unobserved`, no manifest write, per-carrier diff list on stdout). Combo C02's
round-42 shape (a failing chunk beside a sibling extraction that reaches the depth ceiling) must appear among the
new seed's combos with the manifest declaring what was observed, including `depth-limited`.
- Target: `matched == n` (n = 78), every claim binding of `tools/round-43/c1-counter.py` true,
`observed_features_match_declared` true, exit 0.
- Counting command: `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>`.
- Data procedure (after the freeze, never before): the generator command above, run by the L1; seats never run it.
- Kill rule: a control meeting the target stops C1 before held-out generation. Controls scored at the freeze
  (`.ufo/waves/round-43/controls/c1/`):
  - CTL-C1-0 do-nothing: counter at the freeze exits 2 `no_manifest_at_rev`;
  - CTL-C1-1 the round-42 held-out manifest copied to the round-43 path: the counter exits non-zero (seed ≠ freeze;
    manifest not first-added after the freeze);
  - CTL-C1-2 red/green of the refusal: the round-42 C02 manifest (declared {extractor-failure, unpublished-entry})
    fed to the frozen generator's tuple check exits 3 and writes no manifest (red receipt); a manifest the check
    passes is the green the data run itself must produce;
  - CTL-C1-3 the round-42 shortcut controls re-scored by the frozen round-43 counter on the frozen dev arm stay
    below the target (the r42 control receipts are reproduced, none reaches 78).
- Disclosed limits: as round 42 — agreement with an independent evaluator cannot tell this table from any other
  table labelling the same envelopes the same way; the claim measures that the frozen table implements the frozen
  precedence on real REA envelopes under a generator that cannot declare the unobserved, not that the precedence is
  the best triage. The C02 shape is a property of REA 6.5.0's gap minting beside a failing chunk at the depth
  ceiling; the observed tuple is authoritative, whatever it is.

## R43-C2 — coverage: the 18 host-local SOURCES rows become resolvable from in-lane copies

Surface moved: `corpus/SOURCES.md` holds 18 rows (S001 S002 S003 S006 S007 S023 S035 S040 S048 S056 S066 S070 S079
S081 S082 S083 S090 S092) whose URL cell names a host-local path outside the lane; at the base
`python3 -I -B tools/round-41/local-source-gate.py --root <LANE> --rev <REV>` exits 1 with those 18 rows in
`rows_failed` (`local-source-gate.py --help`: a sidecar map `corpus/evidence/local-sources.json` binds each
out-of-lane path to an in-lane copy digest). After the move the gate exits 0 at the measured revision with
`rows_failed` empty and 17 in-lane copies plus the preserved S126 entry committed under
`corpus/evidence/round-43/local-sources/` (byte copies, one lossless `gzip -9 -n`, deterministic member/directory
tars — the exact dispositions the round-42 wave-1 `R42LocalSrc` seat proved green in a sandbox clone, this round
re-verified against the live host objects). Command that shows it unmoved: the gate at the freeze revision exits 1
with `rows_failed` length 18.

**Predicate P43-C2.** At the measured revision: `corpus/evidence/local-sources.json` binds every out-of-lane path
named by a `corpus/SOURCES.md` URL cell to exactly one in-lane regular-file copy under
`corpus/evidence/round-43/local-sources/`, each entry digest equals its copy's sha256, each row-pinned digest (where
the URL cell pins one) equals the entry or its source digest, and `local-source-gate.py --root <LANE> --rev <REV>`
exits 0; the gate tool itself is byte-identical to the round-41 committed bytes; no committed copy exceeds the
5 MiB bound and no third-party firmware image is among them; every copy's digest re-verifies against the live host
object it copies (fresh row-pin audit, this round); the `corpus/SOURCES.md` table itself is byte-identical to the
base except nothing — the rows keep their host paths (the map, not the registry, carries the resolution).

- Target: gate exit 0, `rows_failed` empty, `rows_total` ≥ 129, receipt committed at the measured revision.
- Counting command: `python3 -I -B tools/round-41/local-source-gate.py --root <LANE> --rev <REV>` (exit 0, and
  `jq '.rows_failed | length' <receipt>` prints 0).
- Controls scored at the freeze (before the copies land): CTL-C2-0 the do-nothing gate run at the freeze revision
  (exit 1, 18 rows failed — committed receipt); CTL-C2-1 a sandbox-clone control proving a map entry whose copy is
  absent or digest-mismatched keeps the gate red (the round-38 lesson: a counter must not green on a stub at the
  old path — the gate's vocabulary binds copies under the map, and the receipt names the map version).
- Kill rule: a control reaching exit 0 stops C2 before the copies land.
- Disclosed limits: the copies bind this checkout's row pins; they do not re-verify the upstream sources' content
  claims (that is each row's own recheck cell); host paths that drift later re-red the row in the gate's advisory
  output without changing its exit while the copy stands.

## Separability

C1 reads `SKILL.md`, the round-42 frozen v4 tools and fixtures, the round-43 held-out evidence, and the S135 row.
C2 reads `corpus/SOURCES.md`, `corpus/evidence/local-sources.json`, `corpus/evidence/round-43/local-sources/`, and
the round-41 gate tool. Neither reads the other's data; the shared file is this plan. S135 is a C1 citation only;
C2's evidence cites existing rows.

## Frontier step (this round, inside the claim cap)

- Sources: S135 (unblob 26.6.4 LICENSE, opened by the L1 at 2026-10-27T08:08Z, HTTP 200, 1068 B, sha256
  `67303bbd…`) is appended as the round's one new registry row, cited by P43-C1's fixtures clause and by the round's
  v4-scored knowledge entry. Assimilation (§10): one theme, one admitted entry
  (`sasquatch-prebuilt-package-inventory`, re-grounded in-round per the round-42 `R42Assim` review's ADMIT verdict),
  its cited staged rows appended in fleet schema with the scratch collision/quarantine checks; ≥1 reject stays on
  record. Quarantine slice (5 rows) hand-checked. `considerthese/`: no such directory — report line.

## Frozen paths

C1: this file; `tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py}`; the round-42 frozen tools
`tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,fixtures.json}` and the lookup control
`.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md`; the SKILL v4 table region; the fixtures under
`corpus/evidence/round-42/c2/fixtures/`; the round-42 dev arm `corpus/evidence/round-42/c2/dev/`; the round-41 C1
receipts `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json`. C2: this file;
`tools/round-41/local-source-gate.py`; `corpus/evidence/local-sources.json`; the copies under
`corpus/evidence/round-43/local-sources/` (added after the freeze — landing paths, not pre-landing bytes).

## Changes from the draft

(none yet — this file is the draft wave 1 attacks; every change is recorded here before the freeze)
