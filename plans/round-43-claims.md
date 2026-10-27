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
tuple (the round-42 stop binding, now expected true); the manifest records the generator's own tuple check
(`generator.tuple_check`: per-carrier observed/declared verdicts, all equal) and the refusal rule is demonstrated
red/green in the committed controls; the frozen interpreter gives every held-out envelope the same (label, action)
pair as the frozen evaluator; the combo-unseen-majority binding scores at least half of the held-out `combo`
envelopes outside the union of the named classes' declared tuples (`combo_unseen_majority` ≥ 12 of 24 — the
round-42 binding kept verbatim; the frozen lookup control
`.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` is run through the frozen interpreter and its score
reported, not bound — round 42 measured 19/24 on the same generator family, so a literal
"strictly fewer than half" threshold would hand the kill to the factor draw); the round-41 C1 receipts and the
evaluator's pair; every carrier regenerates byte-identically from the seed; the seed equals the freeze commit hash;
every envelope's subject digest equals its carrier's sha256; the fixtures the carriers embed are the pinned unblob
26.6.4 MIT fixtures (`tools/round-42/fixtures.json`), whose license basis is cited by the new SOURCES row S135
opened this round; no frozen C1 path changed after the freeze.

- The generator change (QUALITY 85 / R42-CL1): in `heldout-gen-v4r43.py` (a port of `tools/round-42/heldout-gen-v4.py`),
the manifest write moves behind the REA run (the frozen generator finalizes `manifest.json` before the first REA
process — the inversion M42-2 lived in): build carriers, run REA, then for each carrier compare
`observed_features(envelope)` (the same extraction the round-42 dev proof uses) against the tuple about to be
declared; any difference refuses the manifest (exit 3 `declared_tuple_unobserved`, no manifest write, per-carrier
diff list on stdout); on all-equal the manifest is written with `generator.tuple_check` appended (per-carrier
verdicts, `all_equal: true`). The predictor itself is corrected, not only guarded (R43RevRevenger D1): in
`combo_declared` the `published` block moves above the depth block and `reached` derives from it
(`reached = (not dep_effective) and published == 'nonzero'`), because a damaged v4 chunk's partial output still
reaches the ceiling — without this the generator would refuse on ~42 % of seeds. A non-`--run` invocation builds
carriers and `tree.json` only under `--carriers-only` (no manifest, exit 0 — the counter's regeneration arm uses
it); plain `--seed --out` exits 4 having written nothing, and a standalone `--tuple-check DIR` re-runs the
refusal against a committed directory (exit 3 on the round-42 held-out set at C02). If the seed's draw includes
the C02 shape (a damaged single root chunk whose partial output reaches the depth ceiling — measured 42.2 % of
seeds), the manifest declares what was observed, including `depth-limited`; the unconditional demonstration is
the CTL-C1-2 red arm on the committed round-42 set.
- Target: `matched == n` (n = 78), every claim binding of `tools/round-43/c1-counter.py` true,
`observed_features_match_declared` true, exit 0.
- Counting command: `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>`.
- Data procedure (after the freeze, never before): the generator command above, run by the L1; seats never run it.
- Kill rule: a control meeting the target stops C1 before held-out generation. Controls scored at the freeze
  (`.ufo/waves/round-43/controls/c1/`):
  - CTL-C1-0 do-nothing: counter at the freeze exits 2 `no_manifest_at_rev`;
  - CTL-C1-1 the round-42 held-out manifest copied to the round-43 path: the counter exits non-zero (seed ≠ freeze;
    manifest not first-added after the freeze);
  - CTL-C1-2 red/green of the refusal: `heldout-gen-v4r43.py --tuple-check corpus/evidence/round-42/c2/heldout`
    on the committed round-42 set exits 3 and writes nothing (red receipt: `REFUSE C02 … depth-limited`);
    a green arm — the same check on a directory whose manifest declares the observed tuples — exits 0;
  - CTL-C1-3 the round-42 shortcut controls re-scored by the frozen round-43 counter on the frozen dev arm stay
    below the target (the r42 control receipts are reproduced, none reaches 78).
- Disclosed limits: as round 42 — agreement with an independent evaluator cannot tell this table from any other
  table labelling the same envelopes the same way; the claim measures that the frozen table implements the frozen
  precedence on real REA envelopes under a generator that cannot declare the unobserved, not that the precedence is
  the best triage. The C02 shape is a property of REA 6.5.0's gap minting beside a failing chunk at the depth
  ceiling; the observed tuple is authoritative, whatever it is. The tuple check is vacuous for the two
  out-of-domain carriers (H25/H26 class `out-of-domain`: empty envelope, declared tuple empty — effective
  n = 76 for the refusal), and the check is generator-self-reported, so the counter additionally binds the
  per-carrier `run.json` digests and the `declared_extras` fields (eight-field match, not six).

## R43-C2 — coverage: the 18 host-local SOURCES rows become resolvable from in-lane copies

Surface moved: `corpus/SOURCES.md` holds 18 rows (S001 S002 S003 S006 S007 S023 S035 S040 S048 S056 S066 S070 S079
S081 S082 S083 S090 S092) whose URL cell names a host-local path outside the lane; at the base
`python3 -I -B tools/round-41/local-source-gate.py --root <LANE> --rev <REV>` exits 1 with those 18 rows in
`rows_failed` (`local-source-gate.py --help`: a sidecar map `corpus/evidence/local-sources.json` binds each
out-of-lane path to an in-lane copy digest). After the move the gate exits 0 at the measured revision with
`rows_failed` empty and 17 in-lane copies plus the preserved S126 entry committed under
`corpus/evidence/round-42/local-sources/` (the destination the prepared map pins; byte copies, one lossless
`gzip -9 -n`, deterministic member/directory tars — the exact dispositions the round-42 wave-1 `R42LocalSrc` seat
proved green in a sandbox clone, this round re-verified against the live host objects). Command that shows it unmoved: the gate at the freeze revision exits 1
with `rows_failed` length 18.

**Predicate P43-C2.** At the measured revision, in a clean `--shared` clone checked out at REV (worktree
`git status --porcelain` empty — the gate reads the map and the copies from the worktree, not from REV, so the
clean-clone form is part of the predicate): `corpus/evidence/local-sources.json` binds every out-of-lane path
named by a `corpus/SOURCES.md` URL cell to exactly one in-lane copy that is a regular file — not a symlink at
its own path or at any component above it (the frozen gate's `isfile` follows links, so the scoring wrapper adds
a `find -type l`/lstat check over `corpus/evidence/round-42/local-sources/` and
`corpus/evidence/round-41/s126/`); each entry's copy sha256 field equals its copy's sha256; each row-pinned
digest (where the URL cell pins one) equals the entry or its source digest; `python3 -I -B
tools/round-41/local-source-gate.py --root <CLONE> --rev <REV> --json` exits 0 with `rows_failed` empty and no
`--sources`/`--map` overrides; the gate tool itself is byte-identical to the round-41 committed bytes
(`cafe232a…` since `d764389e`); no committed copy exceeds the 5 MiB bound and none of the 18 mapped copy paths
carries third-party firmware bytes; and the copies are re-derived byte-exactly from the objects they stand for,
per their dispositions (byte copy ⇒ copy digest == host digest; `gzip -9 -n` ⇒ decompressed digest == host
digest; member/directory tars ⇒ every cited member digest == the host object's member digest), checked by
`verify-copies-r43.py` (the hardened port in `.ufo/waves/round-43/w1/artifacts/R43RevLocalsrc/` — the pack's own
`verify-copies.py` crashes on absent hosts and is not re-used) run by two independent seats this round against
the exact committed bytes at REV: 15 of 18 entries re-verify against the live host object, and the three
host-absent entries (S035 `go-1.24.6`/`go-1.25.0` `src/internal/abi`, S081 `rea-agents` 6.7.0 npx cache) are
proven against upstream bytes (the Go tarballs' members byte-equal `raw.githubusercontent.com/golang/go@…`
fetches; S081's members byte-equal the pinned `rea-agents-6.7.0.tgz`, sha256 `20958a66…`). The
`corpus/SOURCES.md` registry keeps its host-path rows byte-identical to the base plus exactly the appended
round-43 rows (S135, S136, S137) — the map, not the registry, carries the resolution.

- Target: gate exit 0, `rows_failed` empty, `rows_checked == 19`, `rows_total` = the post-append row count
  (136 with S135–S137), receipt committed at the measured revision.
- Counting command: in a clean `--shared` clone at REV,
  `python3 -I -B tools/round-41/local-source-gate.py --root <CLONE> --rev <REV> --json` (exit 0, and
  `jq '.rows_failed | length' <receipt>` prints 0); the receipt additionally records `counter_sha256`,
  `map_sha256`, the resolved REV and the worktree cleanliness line.
- Controls scored at the freeze (before the copies land): CTL-C2-0 the do-nothing gate run at the freeze revision
  (exit 1, 18 rows failed — committed receipt); CTL-C2-1 a sandbox-clone control proving a map entry whose copy is
  absent or digest-mismatched keeps the gate red (the round-38 lesson); CTL-C2-2 a symlink copy replacing a real
  one keeps the claim's structural check red (the frozen gate greens it — measured T2, so the wrapper's
  `find -type l` clause is what catches it); CTL-C2-3 a worktree-shadow (copies present uncommitted or absent at
  REV) is caught by the clean-clone form. Gate receipts carry argv, the gate tool's sha256, the resolved
  revision and the exit code (R43SentProv receipt shape).
- Kill rule: a control reaching exit 0 while satisfying every P43-C2 clause stops C2 before the copies land.
- Disclosed limits: the copies bind this checkout's row pins; they do not re-verify the upstream sources' content
  claims (that is each row's own recheck cell); a `source_sha256` entry where the host object still exists
  hard-fails the gate on drift (the drifted path re-reds the row AND flips the exit on hosts that hold it —
  deliberate property); a duplicate map key is last-wins under `json.load` (non-binding footnote — the landing
  lint rejects duplicates outright); the gate's consistency check does not prove provenance for URL-unpinned
  rows, which is why the landing carries the `verify-copies-r43.py` audit in the predicate.

## Separability

C1 reads `SKILL.md`, the round-42 frozen v4 tools and fixtures, the round-43 held-out evidence, and the S135 row.
C2 reads `corpus/SOURCES.md`, `corpus/evidence/local-sources.json`, `corpus/evidence/round-42/local-sources/`, and
the round-41 gate tool. Neither reads the other's data; the shared file is this plan. S135 is a C1 citation only;
C2's evidence cites existing rows.

## Wave-1 amendments (recorded before the freeze — attack findings folded back into the draft)

1. **C1 generator** (R43RevRevenger D1/D2/D3/D6 + demonstration): the manifest write moves behind the run;
   `--carriers-only` preserves the counter's regeneration arm; the `combo_declared` predictor's `reached` clause
   is corrected (reordered to derive from `published`); the C02-shape sentence is conditional; `manifest_before_envelopes`
   is kept and `generator.tuple_check.all_equal` is bound by the counter; the standalone `--tuple-check DIR` mode
   is the CTL-C1-2 arm.
2. **C1 lookup clause** (R43Simplify §8.1): "strictly fewer than half" on the lookup control contradicted the
   round-42 measurement (19/24); reworded to bind `combo_unseen_majority` only, lookup score reported.
3. **C1 counter port inherits the R43Simplify removals**: `fixture_scope` becomes a real `FROZEN_PATHS` entry for
   `corpus/evidence/round-42/c2/fixtures` (the fixture dir becomes actually frozen — red/green proved); the three
   wrong-shape generator-identity bindings for a post-freeze generator are replaced by
   `generator_absent_at_freeze`-equivalents plus `tuple_check` presence; the round-42 C1-carrier family bindings
   and CTL-C2-7b stay unported (−165 lines, behaviour-identical on the r42 set at 74/74 selftest).
4. **C2 SOURCES clause** (R43SentProv defect): the byte-identity clause now says "identical except the appended
   round-43 rows" (S135/S136/S137) — the original wording was falsified by the round's own S135 append.
5. **C2 live-object clause** (R43SentProv host-audit): 15/18 live-equal, 3 host-absent — wording now binds
   "re-verifies where the host object still exists; the prepared copy is the record for the absent three".
6. **C2 landing path** (L1 amendment `1ed29de2`): the prepared map's pinned destination
   `corpus/evidence/round-42/local-sources/` stands — the copies keep round-42 provenance; do NOT rename.
7. **R42-V2 remedy recorded**: the L1 runs `tools/round-42/prefile-gate.py --round 43` after wave 2 settles and
   commits `.ufo/waves/round-43/l1/prefile-gate.json` with the report-filing commit.
8. **R42-V3 SKILL status markers**: the status sentences land as appended text on existing prose lines (end of
   the line before each marker — marker line numbers and both rule-block regions byte-identical).
9. **OOD vacuity + self-report limits** (R43RevRevenger D5, R43Simplify §8.2/§8.3): disclosed; counter binds
   `run.json` digests and `declared_extras` (eight-field match).
10. **SKILL.md status-marker placement** (R43ScoutTable + counter `rule_block` semantics): appended to existing
    lines, never a new line inside a `rule_block` span and never a new `- **` bullet — `rule_blocks` stays 21,
    marker stays `:521`/`:438`.


## Frontier step (this round, inside the claim cap)

- Sources: S135 (unblob 26.6.4 LICENSE, opened by the L1 at 2026-10-27T08:08Z, HTTP 200, 1068 B, sha256
  `67303bbd…`) is appended as the round's one new registry row, cited by P43-C1's fixtures clause and by the round's
  v4-scored knowledge entry. Assimilation (§10): one theme, one admitted entry
  (`sasquatch-prebuilt-package-inventory`, re-grounded in-round per the round-42 `R42Assim` review's ADMIT verdict),
  its cited staged rows appended in fleet schema with the scratch collision/quarantine checks; ≥1 reject stays on
  record. Quarantine slice (5 rows) hand-checked. `considerthese/`: no such directory — report line.

## Frozen paths and landing paths

Byte-frozen (the counter's `frozen_path_changed`/`skill_block_drift` watch them): this file;
`tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c1-controls-r43.py}`; the round-42 frozen tools
`tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,fixtures.json}` and the lookup control
`.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md`; the SKILL v4 table region (the `rule_block` span —
status text appends to the prose line above the marker, never inside a region); the fixtures under
`corpus/evidence/round-42/c2/fixtures/` (a real `FROZEN_PATHS` entry this round — the round-42 `fixture_scope`
read a top-level manifest key the generator never wrote and was vacuous); the round-42 dev arm
`corpus/evidence/round-42/c2/dev/`; the round-41 C1 receipts
`corpus/evidence/round-41/c1/{V3,V4,L3,L4}/after.json`; `tools/round-41/local-source-gate.py`;
`corpus/evidence/round-41/s126/` (the preserved S126 copy).

First-added after the freeze, digest-pinned here (exempt from the no-touch rule, exactly like the heldout dir):
`corpus/evidence/local-sources.json` — the prepared pack's map verbatim, sha256
`2671850b5d57748557def5b8a67592bb656793e2a0143429b23c5097ff3ec49a`; the 17 copies under
`corpus/evidence/round-42/local-sources/` — the prepared pack's tree verbatim, sorted-paths sha256-manifest hash
`72768b7b03917f784636833a2b3fd0445ec8194c077b3532cd03f359bc9d2ea0`; the held-out set
`corpus/evidence/round-43/c1/heldout/` plus controls, data and score receipts under `.ufo/waves/round-43/`.

## Changes from the draft
(recorded in `## Wave-1 amendments` above — ten items folded back before the freeze)
Updates since item 1–10 (folded before the freeze): 11. **C2 predicate hardened per R43CritC2 P-1..P-10** —
regular-file/no-symlink clause, clean-clone counting form (the gate reads the worktree, not REV), receipt
`counter_sha256`/`map_sha256` fields, symlink/worktree-shadow controls, kill rule conditioned on every clause,
`verify-copies-r43.py` adopted as the landing lint (the pack's own verifier crashes on absent hosts), upstream
fallback proofs for the three host-absent entries named verbatim. 12. **R43C1Regress routing note** — the
round-42 C1 `projection_ok` clause cannot be re-run by a seat (reserved inputs); its re-derivation is an L1
control step. 13. **R43ConnPattern hits adopted** — `combo_count`/`fixtures` read-unwritten keys fixed in the
port spec (the real keys are bound); `c1-counter.py` records `counter_sha256_at_freeze` on every exit path;
the counter honours `TMPDIR`/`--scratch` and never hardcodes `kaidoku-r42`.
