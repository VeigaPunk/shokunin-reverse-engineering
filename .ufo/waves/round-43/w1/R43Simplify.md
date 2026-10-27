# R43Simplify — YAGNI review of what the round-43 C1 port inherits

**DONE** — 165 of the inherited depth counter's 3026 lines (5.3 %) are outside P43-C1 and their deletion is
behaviour-identical on the narrow existing check (selftest 74/74 after pruning the 5 cases that only tested the
deleted code; round-42 data still scores n = 78, matched = 78, same single false binding, same `decision_pairs`;
`probe.diff` = 165 deletions / 4 insertions). The generator's three non-default action vocabularies are not merely
unused but **unreachable** (each misses 3 of the 16 recipe labels and exits at the loud missing-label check). The
scoring chain needs **no network and no REA**: `strace -f -e trace=network` over a full scoring run records 820
lines, all `SIGCHLD`, and `grep -c 'connect('` = 0. Two inherited pieces are not merely dead but *wrong* for round
43: `fixture_scope()` is vacuous (it reads a top-level `fixtures` key the generator never writes, so the fixture
directory P43-C1 freezes is unfrozen today — proved red/green below), and the generator-identity bindings are
structurally impossible for a post-freeze generator (`generator_absent_at_freeze` at every revision). Calibration
finding: P43-C1's "the lookup control scores strictly fewer than half" clause, bound literally, contradicts the
round-42 measurement of the same control on the same generator family (19/24 = 79 %, reported and deliberately
*not* bound in round 42); the draft's own parenthetical names a different quantity (`combo_unseen_majority`).

Seat bounds honoured: nothing in the lane was written except this report and `artifacts/R43Simplify/`; no VCS
mutation; scratch removed; no tool installed or upgraded (python3 3.14.8, git 2.56.0, strace 7.2 — pre-existing).

## 1. Subjects, base bytes, method

| Subject | Path at base `6b9e64fe7e0de202d9383baad5792fbfe039a743` | Lines | sha256 |
|---|---|---|---|
| depth counter (port target of `tools/round-43/c1-counter.py`) | `tools/round-42/c2-counter.py` | 3026 | `f108916713b38d860acdd60d78dd1d1a541b9feccb1bd1979742dd8dd952cb59` |
| held-out generator (port target of `heldout-gen-v4r43.py`) | `tools/round-42/heldout-gen-v4.py` | 3419 | `c2b1641ad6beec0d8eead002520174fb596c574efe44220c4a440917be03a5e1` |

Method: read the draft (`plans/round-43-claims.md`, unchanged for C1 by the L1 amendment `1ed29de2`), mapped every
P43-C1 clause onto the 35 inherited bindings (21 claim + 14 instrument), then did two empirical runs rather than
reading only — (a) the base counter against the round-42 held-out data at the round-42 freeze
(`d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b`) to fix the retained contract, (b) a probe copy with the candidate
deletions applied (`artifacts/R43Simplify/yagni-probe/c2-counter.py`, 2865 lines) run through the same two checks
plus a frozen-path red test. All runs in scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43Simplify` with
`HYAKU_SCRATCH`/`TMPDIR` set there; the sandbox clone was asserted with `git -C <clone> rev-parse --show-toplevel`
before its fixture-identity commit.

Baseline (retained contract, this is what a deletion must not move):

```
$ python3 -I -B c2-counter.py --root <LANE> --rev 6b9e64fe... --freeze d1681696...
{"bindings_false": ["observed_features_match_declared"], "matched": 78, "matched_classes": 54,
 "matched_combos": 24, "n": 78, "exit_code": 1}            # exit 1; 1.59 s; materialised_files 68
$ python3 -I -B c2-counter.py --selftest
{"selftest": "c2-counter r42 (v4)", "cases": 79, "pass": 79, "fail": 0}   # 47.3 s
```

The single false binding is exactly the round-42 stop (`C02`, `gap_kinds`: declared
`{extractor-failure, unpublished-entry}`, observed +`depth-limited`) — reproduced here as the reference point, not
re-litigated.

## 2. P43-C1 clause → inherited binding map

Status vocabulary: **ok** (inherited and needs only path re-pointing), **wrong-shape** (cannot hold for a
post-freeze generator), **vacuous** (present but reads nothing), **missing**.

| P43-C1 clause | Inherited binding(s) | Status |
|---|---|---|
| v4 table region byte-identical to `d1681696` | `v4_block_identical`, `v4_block_present` (anchored freeze↔REV only) | wrong-shape (no `d1681696` anchor) |
| interpreter + evaluator byte-identical at `d1681696`, freeze, REV | `frozen_units`, `frozen_drift` over `FROZEN_PATHS`+writer scope | wrong-shape (no `d1681696` anchor) |
| held-out set from the `--seed/--out/--run/--scratch` command, first add after the freeze, 27×2+24 | `seed_matches_freeze`, `manifest_after_freeze`, `manifest_before_envelopes`, `classes_two_each`, `n_equals_twice_classes`, `combo_family_wellformed` | ok (nothing binds that `--run` happened — see §8.4) |
| every observed six-field tuple equals its declared tuple | `observed_features_match_declared` (+ `declared_features` report) | ok |
| manifest records `generator.tuple_check`, all equal; refusal red/green in controls | — | **missing** |
| interpreter pair == evaluator pair on every envelope | `matched == n`, `evaluator_covers_all`, `decisions_reported`, `row_decisions_consistent` | ok |
| CTL-C2-7 lookup scores strictly < half of the combos | `lookup_control_identical` (identity only); the score is `binding: false` | **missing** (reported, not bound) |
| round-41 C1 receipts + round-42 dev envelopes get the evaluator's pair | `real_receipts_depth_limited`, `legacy_dev_envelopes` | ok |
| carriers regenerate byte-identically from the seed | `carriers_regenerated`, `regenerated_seed_matches_freeze`, `writer_matches_manifest` | ok |
| seed == freeze | `seed_matches_freeze` | ok |
| subject digest == carrier sha256 | `envelopes_valid`, `carriers_committed` | ok |
| fixtures are the pinned unblob 26.6.4 MIT fixtures; basis cited by S135 | `fixture_scope` (→ `FROZEN_PATHS`) | **vacuous** + S135 **missing** |
| no frozen C1 path changed after the freeze | `frozen_drift`, `skill_block_drift` | hole over the fixture dir (§4) |

The counter's own CLI is already minimal — `--root --rev --freeze --json-out --selftest`, all five used. The unused
option weight is entirely generator-side.

## 3. Removal list, ranked by safety

Each item: what goes, why no R43-C1 clause needs it, what it could weaken. Line counts are measured off
`probe.diff` (items A1–A3 are applied in the probe) or off the source span (B-items, not applied — the generator
port is the L1's to author).

| # | Removal | Lines | Why P43-C1 does not need it | Risk (clause weakened) |
|---|---|---|---|---|
| **A1** | `fixture_scope()` → one `FROZEN_PATHS` entry for `corpus/evidence/round-42/c2/fixtures` | −25 / +2 | the manifest carries `generator.fixtures` (metadata), never a top-level `fixtures`, so the helper always returned `{}` | **none — strengthens** "no frozen C1 path changed": the fixture dir becomes actually frozen (red/green in §4) |
| **A2** | CTL-C2-7b fallback block, `LOOKUP_7B`, its frozen unit, the `GREEN_CHECK` assertion | −44 | P43-C1 names only `CTL-C2-7-lookup.md`; the 7b control was `binding: false` | none in P43-C1; loses an unbound second anti-enumeration witness |
| **A3** | `legacy_chunks_not_no_squashfs`, `new_legacy_label_exercised`, `handler_families_exercised` + their blocks, 5 selftest cases, 2 stub modes, `LEGACY_LABEL`, `V4_HANDLER_PREFIX`, `row_cells`, `class_families` | −87 | these are the round-42 **C1-carrier** family bindings; P43-C1 never reads them, and the table is byte-frozen so their content assertions cannot change | low: they are the only guards on *table content* (no-squashfs handler cell, legacy-failure row) if the L1 ever re-anchors the table elsewhere |
| **A4** | `res['table']['v3_marker_at_rev'/'v3_marker_at_freeze']` | −2 | reported only, no binding reads them (`MARKER_V3` itself stays for the selftest's v3 refusal fixture) | none |
| **B1** | generator `ACTION_SETS` entries `tabledraft`, `interp`, `actionreview` + the `--actions-set` choice list | −48 | 16 recipe labels; each set has 13 rows and misses `container-depth-limited`, `legacy-body-failure`, `unknown-residue` → `main()` exits at the missing-label check before building | none: unreachable, not merely unused |
| **B2** | `--fetch` + urllib plumbing in `fixture_bytes()` | −24 | all 14 pins have committed copies; the counter never passes `--fetch`; P43-C1 forbids nothing here but needs nothing either | none; removes the only URL call site in the scoring chain |
| **B3** | `--allow-unseen-minority`, `ALLOW_UNSEEN_MINORITY`, the gate override (`heldout-gen-v4.py:2802-2809`) | −10 | it is an escape hatch around the very quantity P43-C1 binds | none; makes the generator fail closed at build time |
| **B4** | `--ood-op`, `--gzip`, `--keep-extraction` + plumbing | −18 | the round-43 data command passes `--seed --out --run --scratch` only; no `*.gz` exists under the round-42 held-out set, so `--gzip` was never used | low: `--gzip` is the only size lever if round-43 envelopes are committed compressed |
| **B5** | generator `verify()`, `regen_check()`, `feature_diff()`, `expected_for()`, its `observed_features()`, `--verify` | −132 | the counter already re-runs the generator from the freeze and compares bytes, digests and tuples (`carriers_regenerated`, `envelopes_valid`, `observed_features_match_declared`, 78/78 in 1.6 s) | low: `regen_check` is the only place `tree.json` byte-identity is compared |
| **C1** | stub-only generator options in the counter's `STUB_GEN` (`--arm`, `--combos`) | — | the real generator's argparse has neither; the selftest's dev arm is the sole caller | none while the manifest keeps `arm` |

Total applied in the probe (A1–A4 ≈ 158 net) + B-items ≈ 232 further lines available on the generator side.

Verification of A1–A4 (`artifacts/R43Simplify/probe.diff`, sha256 `00e5b8a1…`):

```
$ python3 -I -B yagni-probe/c2-counter.py --selftest
{"cases": 74, "pass": 74, "fail": 0}                         # 43.3 s; 5 cases deleted with their code
$ python3 -I -B yagni-probe/c2-counter.py --root <LANE> --rev 6b9e64fe... --freeze d1681696... --json-out probe-r42.json
{"bindings_false": ["observed_features_match_declared"], "matched": 78, "n": 78, "exit_code": 1}   # 1.64 s
base vs probe: bindings 35 → 32; decision_pairs identical (True); combo_unseen_majority identical (True);
               (id, label, action) triples identical for all 78 carriers (True)
```

## 4. Dead code that looks like protection: the fixture freeze

`fixture_scope()` reads `man.get('fixtures')`; the manifest's only `fixtures` key is `generator.fixtures`, a metadata
dict (`pins`, `pins_sha256`, `project`, `commit`, `url_base`, `license`, `count`, `resolution`, `damage_recipe`) with
no per-file `path`, so the function returns `{}` and contributes no frozen path — confirmed in the live receipt
(`"fixture_scope": {}` while `generator.fixtures.count == 14`).

Red/green in a sandbox clone (`git clone -q --shared`, toplevel asserted, fixture-identity commit at REV
`62534188b1528ac1855522ce31395deee62df87e`) with a one-byte edit to the *unreferenced* pin
`corpus/evidence/round-42/c2/fixtures/v3-le--squashfs_v3_le.bin`:

```
base  counter: exit 1, frozen_paths_changed [], bindings_false ["observed_features_match_declared"]   # blind
probe counter: exit 2, unevaluable "frozen_path_changed",
               frozen_paths_changed ["corpus/evidence/round-42/c2/fixtures"]                          # caught
```

So P43-C1's "no frozen C1 path changed after the freeze" currently has a hole over exactly the directory the
claim freezes, and the cheapest fix is a deletion: 25 lines out, 1 path in. Note the port must add a selftest case
for it (the probe's fix is covered by this live test, not by the selftest, which builds no fixture tree).

Related, smaller: 4 of the 14 pins are unreferenced by the round-42 manifest (`v3-le`, `v3ddwrt-be`, `v3ns-be`,
`v3ns-le`) — they are frozen inputs either way once A1 lands, so no action needed; recorded so nobody "cleans up"
the fixture directory.

## 5. Must-change, not removable (repairs the port cannot skip)

1. **Generator identity.** `GEN = 'tools/round-42/heldout-gen-v4.py'` and `show(root, freeze, GEN)` do not exist for
   a generator first added after the freeze: the inherited code raises `Unevaluable('generator_absent_at_freeze')` at
   *every* revision. `generator_sha_matches_freeze` / `manifest_generator_path` must be re-pointed at the data
   commit (or the freeze must name the generator path explicitly), not deleted and forgotten.
2. **A `d1681696` anchor.** Both the table region and the interpreter/evaluator identity clauses name
   `d1681696`, while the inherited bindings anchor freeze↔REV. One extra `REF` constant plus a unit hash.
3. **`generator.tuple_check`, read not recomputed.** The new binding must read the recorded per-carrier
   observed/declared verdicts out of the manifest. Recomputing them means invoking the generator with `--run` →
   78 `npx -y rea-agents@6.5.0` calls at scoring time (§6). This is the one place where the inherited code makes
   the wrong implementation look natural.
4. **S135.** Nothing in the counter reads `corpus/SOURCES.md`; P43-C1 cites S135 for the fixtures' license basis.
5. **The lookup score** must be bound (inherited: `binding: false`) or the clause reworded — see §8.1 before
   freezing, because it is the likeliest way for a green table to fail the round.

## 6. Does the round-43 counter need any network or REA access at scoring time?

**No, and the inherited chain already satisfies this.** Named evidence:

- counter imports: `json os re shlex shutil subprocess sys tempfile` — no `urllib`, `requests`, `socket`, `http`.
- every `subprocess.run` target is `git` or `sys.executable` on a local file: `git` (show/cat-file/rev-parse/
  merge-base/log/ls-tree), the materialised generator, the materialised `indep-eval-v4.py`, the materialised
  `sqfs-triage-v4.py`.
- the generator is invoked as `python -I -B <gen> --seed <FREEZE> --out <outdir>` with `cwd` = the materialised
  freeze tree and `KAIDOKU_GEN_SQUASHFS`/`KAIDOKU_FIXTURES` pointing into that tree — **no `--run`, no `--fetch`**.
- `strace -f -e trace=network` over a complete scoring run: 820 traced lines, every one a `SIGCHLD` child-exit
  record; `grep -c 'connect(' net.log` = **0**; no `socket(`, `sendto(`. (`unshare -n` was refused by the host —
  "Operation not permitted" — so the syscall audit replaces the namespace proof.)
- the generator's only URL call site is `urllib.request.urlopen` inside `fixture_bytes(..., fetch)`, gated on
  `fetch`; `fixture_bytes(entry, None, <empty cache>, fetch=False)` raises
  `FixturePinError: fixture 'v1-be' found in neither (no --fixtures-dir) nor <cache>. Pass --fetch to download …`
  — fail-closed, not silent-fallback.
- the only REA entry points are `run_rea()` / `out_of_domain_run()` (`cmd = ['npx', '-y', 'rea-agents@6.5.0', …]`,
  `REA_UNBLOB_COMMAND` set to `~/.local/bin/unblob`), both reachable only under `--run`.

Inherited calls that would break the property if a port keeps them in a *scoring* path: none today; the two
temptations are `--fetch` (delete: B2) and verifying tuples by `--run` (do not: §5.3).

## 7. Preserved contract / tradeoff

- Preserved: the 32 surviving bindings, their failure vocabulary (`Unevaluable` reasons and exit codes 0/1/2),
  `counter_sha256` + `counter_sha256_at_freeze`, the `--json-out` receipt shape, the interpreter/evaluator interface
  probing (deliberately kept — the frozen tools' CLI is what made round-42 green; trimming interface tolerance
  trades weight for post-freeze repair risk).
- Tradeoff of A3: the counter stops asserting *table content* (that the `no-squashfs-chunk` row's handler cell is
  `none`, that a legacy-failure row exists). That content is frozen by byte identity at `d1681696`, so the
  assertions can only restate a constant — but if the L1 re-anchors the table, they must come back.
- Not done: I did not implement the round-43 port (only a deletion probe), did not touch `corpus/`, `tools/`,
  `plans/`, `SKILL.md` or any VCS, and ran no extractor on any published firmware image.

## 8. Draft-attack notes (calibration)

1. **The lookup clause is the round's likeliest green-table kill.** P43-C1 binds "the frozen lookup control run
   through the frozen interpreter scores strictly fewer than half of the held-out combos" and parenthesises it as
   "`combo_unseen_majority` ≥ 12 of 24" — two different quantities. Measured on the round-42 held-out set with the
   same generator family: lookup score **19/24**, `combo_unseen_majority` **19/24**, intersection 16. The lookup
   table's rows (`depth-limited → depth-*`, `partial-body-failure → partial-*`, `clean`) catch 7
   `container-depth-limited`, 5 `partial-body-failure`, 4 `dep-missing-le` combos — i.e. the score is driven by the
   combo factor mix, not by the table under test. Round 42 measured this and froze it as `binding: false` with a
   recorded reason. [INFERENCE] A fresh seed with the same class structure will land in the same regime, so binding
   the literal threshold hands the kill to the factor draw; if the parenthetical is what the L1 means, reword the
   clause to bind `combo_unseen_majority` only.
2. **Provenance of "produced by `--run`".** Each round-42 carrier ships `run.json`, and the counter never reads it
   (`grep -c run.json tools/round-42/c2-counter.py` = 0). What the counter proves is that an envelope exists whose
   subject digest equals the carrier's sha256 — reproducible by construction, not by an REA run. The new
   `generator.tuple_check` record is also self-reported. If turn-1 wants that clause to bite, bind the `run.json`
   digests too (cheap: one more frozen-path-style check), otherwise the clause measures self-consistency.
3. **`declared_extras` is write-only.** The generator emits `declared_extras` (`extraction_failed`, `max_depth`) per
   carrier; the counter's `REQUIRED_FEATURES` is six and `declared_extras` appears 0 times in the counter. The round-42
   mistake was a declared-vs-observed gap set; `max_depth` is the same class of claim (`container-depth-limited`
   depends on it) and is unbound. Either bind the extras in the tuple check or stop emitting them.
4. **A 7th feature field.** `FEATURE_KEYS` carries `extraction_failed` beyond the six-field tuple P43-C1 names; the
   real manifest never declares it, so it is compared only on the selftest stub's 7-field declared tuples. Harmless,
   but it means "six-field tuple" and the counter's vocabulary differ — keep it (deleting it means editing the stub
   declarations) and say "six declared fields" in the port's docstring.
5. **Stub surface drift.** `STUB_GEN` implements `--arm`/`--combos`, which the real generator lacks; a round-43
   generator that changes the manifest's per-carrier records must update the stub in the same commit or the selftest
   green is fiction.

## 9. Artifacts

All under `.ufo/waves/round-43/w1/artifacts/R43Simplify/` (1.1 MB total, nothing above the 5 MB bound):

| File | sha256 | What |
|---|---|---|
| `yagni-probe/c2-counter.py` | `626bd3df10ec7e4dfeaf8a526320798cbab28b878c702a6bdd104d55cd074ebf` | the 2865-line probe: A1–A4 applied, 32 bindings, selftest 74/74 |
| `yagni-probe/heldout-gen-v4.py` | `c2b1641ad6beec0d8eead002520174fb596c574efe44220c4a440917be03a5e1` | unmodified copy of the generator the spans refer to |
| `probe.diff` | `00e5b8a1f7c126a24276c1f0ccbdbfd2ab25e3b32a6b43b518835d8e4a2c1386` | unified diff base→probe, 165 deletions / 4 insertions |
| `base-r42.json` | `d53b70512944c06f14e63634c83ebe377e9be6695d65080d9f3d4d72a4182522` | base counter receipt at `6b9e64fe` / freeze `d1681696` |
| `probe-r42.json` | `12fd52d1791a016573c0a3ead3133a381458cd7dd21cbf54751e443324c3970e` | probe receipt, same revision/freeze |
| `fx-base.json` | `ce54778033e6a062698c518b3c51d0728d2c25095f79a6caddd817913dbeb0da` | base counter on the fixture-mutated clone (blind: exit 1) |
| `fx-probe.json` | `0a7659aa35ab81afce5b797c3f73c29da5fb6371aa615590bbe3beba477569f7` | probe on the same clone (exit 2 `frozen_path_changed`) |
| `strace-network-audit.txt` | `6ef44acded74913e3a3df07b49d5824387188d7b1dd5605c2a27afe82d43b1e3` | the network audit: command, counts, fail-closed fixture evidence |
| `removal-ledger.json` | `bfefc3b9ff19f6641b707bf631b7d66ac2350fa32bb0e1de40e601e5ab6bb9aa` | machine-readable removals, clause map, repairs, network answer |

Reproduction (scratch, from the lane): the two counter runs are the commands quoted in §1 and §3 verbatim; the
fixture red test needs `git clone -q --shared <LANE> "$D/lane"`, a one-byte edit to
`corpus/evidence/round-42/c2/fixtures/v3-le--squashfs_v3_le.bin`, and a `-c user.name=fx -c user.email=fx@fx`
commit inside the clone.

Report: .ufo/waves/round-43/w1/R43Simplify.md
