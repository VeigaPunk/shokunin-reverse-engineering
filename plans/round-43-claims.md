# kaidoku round 43 — frozen claims

Base `6b9e64fe7e0de202d9383baad5792fbfe039a743` (lane `main` at round start; the round-42 verifier spot-check
`corpus/lessons/round-42-verifier-spotcheck.md` sits on tip `af50af81751bbb02316c9bc9a0459ca96707b0c0`,
ancestor of the base). L1 `KaidokuR43` holds the §3 planner seat (orchestrator ruling 2026-10-19: the validator
rejects `planner` as a swarm role; the L1 is the canonical planner and bounded planning data-walks ride scouts,
connectors and revengers — recorded here per the round contract). Fresh-start round (run-10 directive): the L1 read
the last three rejected closures (rounds 40, 41, 42 verifier spot-checks) before declaring; both claims below are
ones a do-nothing control cannot reach (§9), each with its control scored before any claim data.

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis is a lowest axis.
R43-C1 works calibration (generator honesty/self-assessment now refuses declarations unsupported by its own
observation); R43-C2 works coverage. Both are routed follow-throughs named by prior closures:
R43-C1 lands routed defect R42-CL1 (= QUALITY 85, M42-2: the round-42 held-out generator declared a feature tuple
its own run did not observe, combo C02, and the round stopped on that binding); R43-C2 lands routed defects
R41-CL3/R42-CL3 (the round-42 wave-1 `R42LocalSrc` seat prepared, and proved green in a sandbox clone, in-lane
copies for the 18 `corpus/SOURCES.md` rows the `local-source-gate.py` reds at the base, and the landing was never
committed). Routed defect R42-CL2 (no wave 2 attacked the round-42 landing) is discharged by this round's wave 2,
which includes re-running the round-42 C1 counter against a fresh carrier cache; it is a round-shape item, not a claim.

## Freeze-integrity rule (both claims; carried from rounds 39–42)

A score at `REV` is admissible only if `FREEZE` is an ancestor of `REV`, no commit in `FREEZE..REV` touches a frozen
path of that claim, and each frozen regular-file blob at FREEZE equals the blob at REV; a later restore does not
un-block (exit 2 `frozen_path_changed`, never `met_target`). The path walk includes merge diffs (`-m
--diff-merges=first-parent`); M/D/R/T/U are changes, and A is a change whenever the path existed at FREEZE (so a
rewrite/re-add cannot hide as a creation). SKILL rule-block extraction is compared at every commit in the range
with merge commits included; the tree-level blob comparison is an independent backstop. These requirements close
the round-42 default-`git log` merge-diff and rewrite/re-add holes demonstrated in
`.ufo/waves/round-43/w1/R43RevFreeze.md` §2. Control tables and their development inputs are committed in the
freeze. Every score receipt records the scorer's exit code and `counter_sha256` (the sha256 of the counter file it
ran) plus `counter_sha256_at_freeze` (round-41 closure D4), and sha256 of every post-freeze control receipt it
cites. QUALITY 84: both counters are dry-run end to end, as frozen, with data produced by the frozen generators
in a dev arm, before the freeze, and the dry-run receipts show every binding evaluated.

## R43-C1 — calibration: the v4 SquashFS triage table scored on a fresh held-out set under a generator that refuses unobserved declarations

Surface moved: `SKILL.md` `## Queue-drain craft` rule block 21 (`<!-- sqfs-triage-table v4 -->`) stopped unscored
at round 42 — it matched its independent evaluator 78/78 but the round stopped on `observed_features_match_declared`
because the generator declared a gap set for combo C02 that its own REA run did not observe. This claim does not
change one table byte: it re-freezes the frozen table (bytes proven equal to the round-42 freeze `d1681696` at the
table region), regenerates the held-out set from a NEW seed, and replaces the generator's declared-tuple predictor
with a measured one (QUALITY 85): the generator's declared tuple stays the predictor's tuple — a pure pre-run
function of (class, drawn factors, fixture pins) — with its predictor amended to model REA 6.5.0's
depth-limited minting beside a failing chunk at the depth ceiling (the C02 fix); after the `--run` it extracts
the observed six-field tuple from each envelope it produced (the same extraction algorithm as the frozen
counter's `observed_features`) and REFUSES to write the manifest unless every observed tuple equals the
predictor's tuple (exit 3 `declared_tuple_unobserved`, per-carrier diff list, no manifest write). The counter
additionally binds the manifest's own record of that check. Command that shows it unmoved: the round-43 C1 counter at the freeze exits 2
(`no_manifest_at_rev`), and the round-42 stop receipt stays byte-committed at
`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`.

**Predicate P43-C1** (implemented by `tools/round-43/c1-counter.py`; its docstring's clause list is the full text).
At the measured revision: the v4 table region of `SKILL.md` (from the line containing `<!-- sqfs-triage-table v4 -->`
through the end of the first markdown table after it) is byte-identical to the same region at `d1681696`, at the
freeze and at the measured revision (sha256 `92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2`
under the counter's `rule_block` extraction — 13 856 bytes, equal at `d1681696` and the base);
`corpus/SOURCES.md` carries row S135 naming the unblob 26.6.4 LICENSE at its pinned URL with its committed
digest; the
frozen interpreter `tools/round-42/sqfs-triage-v4.py` and the frozen evaluator `tools/round-42/indep-eval-v4.py`
are byte-identical at `d1681696`, at the freeze, and at the measured revision (no commit in
`d1681696..REV` touches them); the held-out set is `corpus/evidence/round-43/c1/heldout/` produced by
`python3 -I -B tools/round-43/heldout-gen-v4r43.py --seed <FREEZE> --out corpus/evidence/round-43/c1/heldout --run --scratch <scratch under /fast/scratch/hyaku/kaidoku-r43/>`, first added in a commit descending from the freeze,
with the same class structure as round 42 (27 named classes × 2 plus 24 combo carriers, n = 78) and the same
`declared_features` single-key contract (R41-CL1); every envelope's observed six-field tuple equals its declared
tuple (the round-42 stop binding, now expected true); the manifest records the generator's own tuple check
(`generator.tuple_check`: per-carrier observed/declared verdicts, all equal) and the refusal rule is demonstrated
red/green in the committed controls; the frozen interpreter gives every held-out envelope the same (label, action)
pair as the frozen evaluator; `combo_unseen_majority` binds exactly as the frozen round-42 counter computes it
(`len(unseen) >= ceil(n_combos/2)` where UNSEEN = the combo's observed six-field tuple outside the union of the
named-class declared tuples in the frozen round-42 dev-arm manifest `corpus/evidence/round-42/c2/dev/manifest.json`,
canonicalized — the round-43 set's own named tuples are NOT the union); the frozen lookup control
`.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` is byte-identical to its frozen bytes
(`lookup_control_identical`) and its held-out combo score is reported, not bound — round 42 measured it 19/24
with `below_half: false` on identical class structure, so a `< half` binding is unreachable on this family; the
round-41 C1 receipts and the round-42 dev-arm envelopes get the evaluator's pair; every carrier regenerates
byte-identically from the seed; the seed equals the freeze commit hash;
every envelope's subject digest equals its carrier's sha256; the fixtures the carriers embed are the pinned unblob
26.6.4 MIT fixtures (`tools/round-42/fixtures.json`), whose license basis is cited by the new SOURCES row S135
opened this round; no frozen C1 path changed after the freeze.

- The generator change (QUALITY 85 / R42-CL1): in `heldout-gen-v4r43.py` (a port of `tools/round-42/heldout-gen-v4.py`),
the manifest write moves behind the REA run (the frozen generator finalizes `manifest.json` before the first REA
process — the inversion M42-2 lived in): build carriers, run REA, then for each carrier compare
`observed_features(envelope)` (the same extraction the round-42 dev proof uses) against the tuple about to be
declared; any difference refuses the manifest (exit 3 `declared_tuple_unobserved`, no manifest write, per-carrier
diff list on stdout); on all-equal the manifest is written with `generator.tuple_check` appended (per-carrier
verdicts, `all_equal: true`). The predictor itself is corrected, not only guarded (R43RevRevenger D1 + L1 dry-run
D8): at `max_depth == 1`, `depth-limited` is predicted only when REA ran and a recursive extraction output directory
exists (`extraction_output = capped or bool(factors['body_v4']) or not damage_effective`;
`reached = (not dep_effective) and extraction_output`). The C05 dry-run falsifier showed why `published != zero`
is not the predicate: a damaged legacy chunk can publish a residue FILE while producing no extraction directory,
so adding depth-limited there would repeat M42-2 with the sign flipped. The measured predicate distinguishes that
from a damaged v4 chunk's earlier files and a tar/member or second-chunk output directory; the generator refuses
on any remaining mismatch rather than smoothing it. A non-`--run` invocation builds carriers and `tree.json` only
under `--carriers-only` (no manifest, exit 0 — the counter's regeneration arm uses it); plain `--seed --out`
exits 4 having written nothing, and a standalone `--tuple-check DIR` re-runs the refusal against a committed
directory (exit 3 on the round-42 held-out set at C02). If the seed's draw includes the C02 shape (a damaged
single root v4 chunk whose output directory reached the depth ceiling), the manifest declares what was observed,
including `depth-limited`; the unconditional demonstration is the CTL-C1-2 red arm on the committed round-42 set.
- Target: `matched == n` (n = 78), every claim binding of `tools/round-43/c1-counter.py` true,
`observed_features_match_declared` true, exit 0.
- Counting command: `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>`.
- Data procedure (after the freeze, never before): the generator command above, run by the L1; seats never run it.
- Kill rule: any counterfactual baseline that omits the claimed work (do-nothing, stale-manifest, shortcut, or
  hand-edited-manifest; CTL-C1-0/1/3/4) reaching the full target stops C1 before held-out generation. The
  explicit reference witness and CTL-C1-2's tuple-check green arm are not counterfactual table-score controls.
  Controls scored at the freeze (`.ufo/waves/round-43/controls/c1/`):
  - CTL-C1-0 do-nothing: counter at the freeze exits 2 `no_manifest_at_rev`;
  - CTL-C1-1 the round-42 held-out manifest copied to the round-43 path: the counter exits non-zero
    (`seed_matches_freeze` false — the copy declares the round-42 freeze seed — plus
    `manifest_after_freeze`/`carriers_regenerated` false);
  - CTL-C1-2 red/green of the refusal: `heldout-gen-v4r43.py --tuple-check corpus/evidence/round-42/c2/heldout`
    on the committed round-42 set exits 3 and writes nothing (red receipt: `REFUSE C02 … depth-limited`);
    a green arm — the same check on a directory whose manifest declares the observed tuples — exits 0;
  - CTL-C1-3 the round-42 shortcut controls re-scored by the frozen round-43 counter on the frozen dev arm stay
    below the target (the r42 control receipts are reproduced, none reaches 78);
  - CTL-C1-4 counter-side hand-edit rejection: a dev-arm manifest with one carrier's `declared_features`
    edited to a value its committed envelope does not observe, scored by the frozen round-43 counter, exits
    non-zero with `observed_features_match_declared` false — the counter computes the observed tuple from
    envelope bytes, never from the manifest's `generator.tuple_check` record.
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
carries third-party firmware bytes; each copy's source/anchor derivation is independently re-derived by disposition:
byte copies equal source bytes; gzip copies decompress to the row-pinned source digest; cited archive members match
their row pins byte-for-byte; source/container digests match `source_sha256` where present. The gate's URL-cell pin
clause is an empty conjunction for these 18 rows (none has a URL-cell digest), so the gate alone is not the content
proof; the mandatory structural/content linter is `tools/round-43/verify-copies-r43.py` (hardened port in
`.ufo/waves/round-43/w1/artifacts/R43RevLocalsrc/`; the pack's own `verify-copies.py` crashes on absent hosts).
The amended pack was re-derived by R43C2Land (133 checks, 0 failures) and its row-pinned members independently
audited by R43C2Pin; 35 of 41 anchor-cell digest slots are carried as bytes, the remaining six are source/container
or package-field digests structurally represented by `source_sha256`/copied metadata. S048's 28-member tar extends
the 23-member pack to add the five previously missing anchor-pinned members `domain/pcap/pcapAnalysis.js`,
`pcap/PcapProvider.js`, `pcap/PcapNativeBound.js`, `ghidra/GhidraTargetSnapshot.js`, and
`bridge/ghidra/ReaGhidraBridge.java` (four dist-relative plus the package-root Java member). S082's package digests
remain textual pins in copied `desc`/`mtree`; absent-host S035/S081 are checked against upstream Go tag/API bytes
and the pinned 6.7.0 tarball, not a live path.
- Target: `tools/round-43/c2-score-r43.py` exits 0, gate `rows_failed []`, `rows_checked == 19`,
  `rows_total == 137`, and the copy/provenance verifier reports 136 checks / 0 failures; its committed receipt
  binds both child receipts, the resolved REV, map/SOURCES digests, BASE→REV numstat and S126 preservation.
- Counting command (one invocation, internally scores the gate and the content verifier in a clean `--shared` clone):
  `python3 -I -B tools/round-43/c2-score-r43.py --root <LANE> --rev <REV> --freeze <FREEZE> --scratch <S> --upstream-dir <GO-TREES> --tarball-67 <rea-agents-6.7.0.tgz> --tarball-65 <rea-agents-6.5.0.tgz> --json-out <OUT>`
  (exit 0; `<OUT>` is `.ufo/waves/round-43/l1/scores/c2-at-<REV>.json`). The gate invocation has no
  `--sources`/`--map` overrides. Upstream inputs are digest-pinned (Go tags; npm tarballs S081/S090/S092)
  and live in scratch, never the repository. The verifier binds the imported EXPECT table at FREEZE and REV;
  that source is `.ufo/waves/round-42/w1/artifacts/R42LocalSrc/build/verify-copies.py`.
- Controls scored at the freeze (before the copies land): CTL-C2-0 the do-nothing gate run at FREEZE
  (exit 1, 18 rows failed); CTL-C2-1 a sandbox-clone control proving a map entry whose copy is absent or
  digest-mismatched keeps the gate red; CTL-C2-2 the symlink attack is the deliberate gate false-green
  (gate exit 0) but `verify-copies-r43.py` `copy-regular` red; CTL-C2-3 a worktree-shadow (copies present
  uncommitted or absent at REV) is caught by the clean-clone receipt (`git status --porcelain` must be empty).
  Gate and copy-audit receipts carry argv, tool sha256, resolved revision, tool-at-REV digest and exit code;
  the copy-audit receipt additionally records the imported EXPECT-table digest at FREEZE and REV.
- Kill rule: any counterfactual no-copy/invalid/worktree-shadow control (CTL-C2-0/1/2/3) that satisfies the clean-clone,
  content/provenance, map, and gate clauses at exit 0 stops C2. The valid prepared-pack baseline in the CTL-C2-2
  symlink test is a positive witness for the verifier, not a kill arm.
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

1. **C1 generator** (R43RevRevenger D1/D2/D3/D6 + L1 dry-run D8): the manifest write moves behind the run;
   `--carriers-only` preserves the counter's regeneration arm; the `combo_declared` predictor's `reached` clause
   is based on recursive extraction-output existence, not any nonzero published file
   (`extraction_output = capped or bool(body_v4) or not damage_effective`; `reached = not dep_effective and
   extraction_output`). The dry-run's C05 residue-only file falsified `published != zero` as a proxy; C05 is now
   predicted without `depth-limited`, while damaged v4/clean/wrapped/sibling output cases remain measured.
   The C02-shape sentence is conditional; `manifest_before_envelopes` stays bound; `generator.tuple_check.all_equal`
   is bound by the counter; standalone `--tuple-check DIR` is the CTL-C1-2 arm.
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
8. **R42-V3 SKILL status markers** (R43SkillMark): two status paragraphs are inserted immediately before markers
   v3/v4 (v3 marker moves 438→440, v4 521→525); the v3 and v4 decision-table regions stay byte-identical to the
   round-42 freeze and command A remains 21/21. The status prose and the whole `SKILL.md` file are frozen at FREEZE.
9. **OOD vacuity + self-report limits** (R43RevRevenger D5, R43Simplify §8.2/§8.3): disclosed; counter binds
   `run.json` digests and `declared_extras` (eight-field match).
10. **SKILL.md status-marker placement** (R43ScoutTable + counter `rule_block` semantics): indented continuation
    paragraphs before the markers, not inside either `rule_block` span and never new `- **` bullets — rule_blocks
    stays 21, the v4 table region hash stays unchanged.
11. **Freeze-integrity hardening** (R43RevFreeze + R43C1Counter): ancestor check, merge-aware path walk, A-as-change
    for frozen blobs, tree-level blob backstop and SKILL-status prose frozen as part of `SKILL.md`; counter selftest
    90/90.
12. **C05 predictor falsifier** (R43DryRun D8): `published` was too broad because a residue FILE can be published
    without a recursive output directory; the extraction-output predicate above replaces it. The L1 dry-run
    receipt at `.ufo/waves/round-43/l1/dry-run-C05-refusal/` preserves the pre-fix failure. Before freeze the
    corrected generator passed the same forced seed `b8201bf474ab85c8f2af5010eb3191f084a63e8a` (G1–G7 all true,
    45/45 bindings evaluated) and a 6-draw predictor sweep (6/6 accepted); full `--run --verify` on 78 carriers
    at that seed also passed tuple_check and regeneration (R43C1Gen receipts).



## Frontier step (this round, inside the claim cap)

- Sources: S135 (unblob 26.6.4 LICENSE, opened by the L1 at 2026-10-27T08:08Z, HTTP 200, 1068 B, sha256
  `67303bbd…`), S136 (the onekey-sec/sasquatch releases API endpoint
  `api.github.com/repos/onekey-sec/sasquatch/releases`, `dataset` — the release matrix's machine-readable source)
  and S137 (the rendered releases page, `docs`, cited for the negative: it carries no asset filename) are appended
  as the round's three new registry rows; S135 is cited by P43-C1's fixtures clause and the v4-scored knowledge
  entry, S136/S137 by the admitted assimilation entry. Assimilation (§10): one theme, one admitted entry
  (`sasquatch-prebuilt-package-inventory`, re-grounded in-round per the round-42 `R42Assim` review's ADMIT verdict
  as `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`), its cited rows appended in fleet schema with the
  scratch collision/quarantine checks; ≥1 reject stays on record (the r42 `sasquatch-unblob-compatibility` REJECT).
  Quarantine slice (5 rows) hand-checked. `considerthese/`: no such directory — report line.

## Frozen paths and landing paths

Byte-frozen (the counter's `frozen_path_changed`/`skill_block_drift` watch them): this file;
`tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py,c2-score-r43.py,receipt-wrap.py,verify-copies-r43.py,build-copies-r43.py}`; the round-42 frozen tools
`tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,fixtures.json}` plus the SquashFS writer the manifest names
`tools/round-39/gen-squashfs.py`; the lookup control `.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` and the
other round-42 CTL files the CTL-C1-3 driver re-scores under `.ufo/waves/round-42/controls/c2/` including its
receipts `c2-counter-at-freeze.json`/`dev-scores-prefreeze.json`; the whole `SKILL.md` file (status paragraphs are
included in the freeze; v3/v4 table regions additionally checked by `rule_block` extraction); the fixtures under
`corpus/evidence/round-42/c2/fixtures/` (a real `FROZEN_PATHS` entry this round — the round-42 `fixture_scope`
read a top-level manifest key the generator never wrote and was vacuous); the round-42 dev arm
`corpus/evidence/round-42/c2/dev/` and the round-42 held-out manifest
`corpus/evidence/round-42/c2/heldout/manifest.json` plus the C02 envelope files the CTL-C1-2 arm reads
(`corpus/evidence/round-42/c2/heldout/C02/{envelope.json,rea-full.json}`); the stop receipt
`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`; the round-41 C1 receipts
`corpus/SOURCES.md` as a whole (S135/S136/S137 are appended before the freeze; the whole file is byte-identical
from FREEZE to REV, while BASE→REV numstat is exactly 3 insertions and 0 deletions); `tools/round-41/local-source-gate.py`;
`.ufo/waves/round-42/w1/artifacts/R42LocalSrc/build/verify-copies.py` (the EXPECT table the hardened verifier imports);
`corpus/evidence/round-41/s126/` (the preserved S126 copy). No round-43 tool imports a `tools/round-42` module
at runtime (ports vendor, not import).

First-added after the freeze, digest-pinned here (exempt from no-touch, like heldout data):

`corpus/evidence/local-sources.json` (a landing path — its 17 new entries land in the landing commits; its final
bytes equal the corrected prepared pack's map verbatim, sha256
`3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e`; the pre-existing S126 entry is preserved
JSON-value-equal to the base entry); the 17 copies under `corpus/evidence/round-42/local-sources/` — the
corrected prepared pack's tree verbatim, sorted-paths sha256-manifest hash
`62fcdf31834687899de0f99e275426b66e67c822bb09f6280eaa9bd8f8519dbb`; the held-out set
`corpus/evidence/round-43/c1/heldout/` plus controls, data and score receipts under `.ufo/waves/round-43/`.
For C2 the landing commits may add map entries and copies and change nothing else: the gate tool, this file, the
S126 entry, and `corpus/SOURCES.md` rows other than the appended round-43 rows are untouched in FREEZE..REV — the
C2 receipt additionally records `git diff --numstat <BASE>..<REV> -- corpus/SOURCES.md` (exactly the appended
round-43 rows, zero deletions) and the S126-preservation check (`jq -cS` on the map's `sources` object at BASE
vs REV).

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
14. **C2 one-command closure** (R43CritC2 / R43RevLocalsrc): `tools/round-43/c2-score-r43.py` is the single count
    command that runs the gate and the 136-check content verifier on the same clean clone/revision, records gate,
    linter, map/SOURCES digests and S126/numstat bindings, and refuses on any failed clause.
