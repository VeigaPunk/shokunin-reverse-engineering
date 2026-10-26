# R42C2Mutants — mutation sweep of the round-41 C2 tooling round 42 keeps (base `c4a38ea`)

**Verdict: CONFIRMED.** All 19 round-41 survivors re-derive on the base-commit bytes
(`c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`): 10 counter survivors are selftest-blind
(70/70 pass on every mutant) and the headline M05 still flips the real score to **MET**
(exit 0, 52/52, `bindings_false []`); the 9 interpreter/evaluator survivors survive
selftest **and** the 52 held-out pairs, with 7 of 9 re-verified against their round-41
killing envelopes (I10/E07 are pair-blind by apparatus design, as documented). The v4
counter/interpreter/evaluator selftests must add the 21 killing cases specified in §3–§4
— every one verified by execution: it passes a correct implementation and fails its
mutant. §5 (`## A1 delta`) adds **17 new mutants** on the A1 v4 additions (container row
order/predicate, HF-vs-F, residue-before-depth, L-family globs, membership deps, single
declared key, lookup/majority combo bindings, counter_sha256), all killed by named cases.

Attacked sources (base bytes, sha256 — identical to the round-41 frozen/measured
digests, so every documented mutant re-applies byte-identically):

| file | sha256 |
|---|---|
| `tools/round-41/c2-counter.py` | `c6c1ea64f07884a3b160a7e52268d295d54c8ef3bc2005704d5fae3398720af8` |
| `tools/round-41/sqfs-triage-v3.py` | `6ad2b4e1638a2b5f883d7bed14f8863ad5396dbc1af64b7cd521720ea42b6aa4` |
| `tools/round-41/indep-eval-v3.py` | `26178d71c0f7634c3f1371ad5c4c7de3b59c49636cdf1b61bf8b2e461c75dce1` |
| `SKILL.md` (v3 block carrier) | `94d13b445701609f110ca6512e99f87afbdc00ccee3123b817853107f3cd725c` |

## Detector (bounded, identical on pristine / mutated / restored bytes)

- **D1 — selftest:** `HYAKU_SCRATCH=<S>/hs TMPDIR=<S> python3 -I -B <tool> --selftest`
- **D2 — real score (counter only):** `python3 -I -B <counter> --root <LANE> --rev e9a24d07… --freeze d764389e… --json-out <receipt>`
- **D3 — pairs (interp/eval):** the 52 held-out envelopes of
  `corpus/evidence/round-41/c2/heldout/` fed exactly as `c2-counter.py` feeds them
  (interpreter: `--skill SKILL.md <52 envelope paths>`; evaluator: `--envelopes <flat dir>`),
  compared to the pristine baseline.
- **D4 — killing case (survivors):** the round-41 killing envelope run against pristine
  and mutant binaries; the flip must be observed, not predicted.

Scratch `S=/fast/scratch/hyaku/kaidoku-r42/R42C2Mutants` (removed at the end). Mutants
are scratch copies (`<S>/muts/`); every patch anchor is asserted to occur exactly once.
The lane tree was never modified: the counter only issues read-only `git -C <LANE>`
commands; the selftest's fixture commits happen inside its own `mkdtemp` fixture repos
(toplevel-asserted). No sandbox clone was needed.

## Baseline (pristine, base bytes)

- Counter D1: `{"selftest": "c2-counter r41 (v3)", "cases": 70, "green": 20, "red": 50, "pass": 70, "fail": 0}`, exit 0, 33.8 s.
- Counter D2: exit 1; `matched 52/52 (matched_classes 40, matched_combos 12), distinct_decisions 13, met_target false, bindings_false ["observed_features_match_declared"]`; receipt 93 429 B, sha256 `1702bda590131f990331629564a4e568047b1ecef57d87d38eeb9966f138f722` (artifact `BASELINE.receipt.json`; byte-different from the round-41 receipt only because the lane tip moved — all semantic fields identical).
- Interpreter D1: exit 0, 69 cases. Evaluator D1: exit 0, 46 cases.
- D3: 52 pairs each, cross-agreement 52/52, disagree [].

## §1 Counter survivors re-derived (`c2-counter.py`, 10/10)

Patch provenance: `artifacts/R41W2C2CounterMut/driver.py`, applied verbatim; mutant
sha256 in `counter-rederive-summary.jsonl` (all rows). Selftest = D1, real = D2 at
`e9a24d07`/`d764389e`.

| id | mutation (one point) | selftest | real @ e9a24d07 | verdict |
|----|----------------------|----------|-----------------|---------|
| M05 | lookup chain + `declared` key | 70/70 pass (blind) | **exit 0, MET, 52/52, bindings []** | **survivor, verdict-flipping** (reproduces at base bytes; mutant sha `897cc8b3…` = round-41's) |
| M02 | pair match ignores action | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M03 | pair match ignores label | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M14 | seed compared on first 8 hex chars | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M15 | `regenerated_seed_matches_freeze` := True | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M18 | `v3_block_identical` drops byte equality | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M21 | drift scan ignores deletions (`D`) | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M37 | `ids_unique` := True | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M46 | committed bytes compared to regen sha, not the manifest pin | 70/70 pass (blind) | exit 1 unchanged | survivor |
| M47 | regen check drops class/arm equality | 70/70 pass (blind) | exit 1 unchanged | survivor |

## §2 Interpreter/evaluator survivors re-derived (9/9)

Patch provenance: `artifacts/R41W2C2InterpMut/tools/mutdrive.py` (edits verbatim);
kill-check = selftest **and** 52 held-out pairs unchanged (D1+D3); D4 = the round-41
killing envelope (`kill/K*.json`), pristine pair → mutant pair.

| id | tool | mutation | selftest | pairs vs baseline | killing envelope (D4) | verdict |
|----|------|----------|----------|-------------------|------------------------|---------|
| I08 | interp | SR diagnostics key `__typename__` → `type` | exit 0 | 0 changed | K12: `escaping-symlink-removed` → `clean` | SURVIVED |
| I10 | interp | P collapsed to 0/1 | exit 0 | 0 changed | K11: pair unchanged (`clean`/`none` both) — P 5→1 invisible to the pair oracle | SURVIVED |
| I11 | interp | files absent reads P=1 | exit 0 | 0 changed | K2: `clean-empty` → `clean` | SURVIVED |
| I14 | interp | `squashfs` H-filter dropped | exit 0 | 0 changed | K3: `no-squashfs-chunk` → `unclassified` | SURVIVED |
| E01 | eval | `-be` token test → substring test | exit 0 | 0 changed | K1: `avm-marker-be-dropped` → `body-extractor-failure` | SURVIVED |
| E04 | eval | stdout SR fallback removed | exit 0 | 0 changed | K8: `escaping-symlink-removed` → `clean` | SURVIVED |
| E05 | eval | diag-level holder dropped (report-only) | exit 0 | 0 changed | K9: `escaping-symlink-removed` → `clean` | SURVIVED |
| E07 | eval | P collapsed to 0/1 | exit 0 | 0 changed | K11: pair unchanged (as I10) | SURVIVED |
| E08 | eval | step 3 moved after step 4 | exit 0 | 0 changed | K5: `dep-missing-be` → `partial-body-failure` | SURVIVED |

## §3 Killing cases the v4 counter selftest must add

Implemented and verified in `killing-cases-counter.py`: 11 cases + their fixture muts
appended to the base counter's selftest (scenario tuples in the harness's own
`(name, params, want_exit, want_false, want_true)` vocabulary). Probe results
(`killing-cases-counter.json`): **pristine+cases = 79/81**, the only failing new case
being the v4-only manifest-level case (see NM-C6 below); **every mutant+cases probe
fails exactly its expected case on top of that baseline-only failure and nothing else
(12/12 match)**.

| killing case (exact) | fixture | expected | kills |
|---|---|---|---|
| `green: tuples declared under the single key declared_features` | `muts={'declare_via_declared_features'}` (every carrier's tuple moved to `declared_features`; `class_expected.features`/`features` removed) | exit 0, `observed_features_match_declared` true | **NM-C1** (single key not read) |
| `red: tuples only under the legacy declared key stay a lookup failure` | `muts={'declare_via_legacy_declared'}` (tuples moved to legacy `declared`) | exit 1, binding false, missing = all ids | **M05** (mutant reads `declared` → binding true → exit 0) |
| `red: a manifest-level tuple map is not the declared key` | `muts={'manifest_level_tuples'}` (carrier tuples stripped; manifest gains `feature_tuples` map) | **v4-only:** exit 1, binding false, missing = all ids | **NM-C6** (v3's manifest-level `decl_key` scan retained). On the v3 counter this case fails by design (pristine exits 0, binding true — the R41-CL1 mechanism family, documented); it belongs in the v4 selftest only |
| `red: seed shares the freeze prefix but differs` | `seed='prefix8'` (seed = `freeze[:8] + 'a'*56`) | exit 1, `seed_matches_freeze` false | **M14** |
| `red: the frozen generator stamps a drifted seed into the regenerated manifest` | `muts={'gen_seed_drift'}` (the frozen stub generator writes `seed = seed + '-drift'`) | exit 1, `regenerated_seed_matches_freeze` false, `seed_matches_freeze` true | **M15** |
| `red: two carriers share one id` | `muts={'dup_id'}` (H02.id = 'H01') | exit 1, `ids_unique` false | **M37** |
| `red: committed bytes match regeneration but the manifest pin points elsewhere` | `muts={'pin_wrong'}` (H01 manifest `sha256` **and** envelope subject digest = `'f'*64`; committed/regenerated bytes unchanged) | exit 1, `carriers_committed` false | **M46** |
| `red: a regenerated carrier ships the wrong arm` | `muts={'arm_swap'}` (H01 `arm='before'`, regeneration says `after`) | exit 1, `carriers_regenerated` false | **M47** |
| `red: the evaluator rotates the action on one whole class` | `emode='disagree_action2'` (stub evaluator flips the action to `none` for the **whole** `clean-empty` class, H05+H06 — a single-envelope flip trips `row_decisions_consistent` and is invisible to the pair halves) | exit 1, `row_decisions_consistent` true, `evaluator_covers_all` true | **M02** (mutant: matched 52 → exit 0) |
| `red: the evaluator rotates the label on one whole class` | `emode='disagree_label2'` (label `clean` for the whole `clean-empty` class) | exit 1, same want_true | **M03** |
| `frozen: a frozen path is deleted by a later commit` | `claim='delete_frozen'` (after the claim commit: `git rm -q tools/round-41/c2-counter.py` + commit) | exit 2 (`frozen_path_changed`) | **M21** (mutant ignores `D` → exit 0) |

**M18 has no counter-level killing case** (re-verified: `M18+cases` = 79/81, unchanged):
a block-bytes difference at REV is always accompanied by a SKILL-touching commit, so the
drift scan (exit 2) masks the binding; the byte-equality conjunct is reachable-false only
via the absent-block case, which M18 preserves. The v4 selftest must therefore pin the
comparison as a **pure function**: `v4_block_identical(b, b) is True`, `(None, b) is
False`, `(a, b≠a) is False` — implementable only if the v4 counter factors the
freeze-vs-rev block comparison out of the drift scan. [INFERENCE] With CTL-C2-0b (the v3
table transcribed under the v4 marker) the v4 counter reads two blocks, so this
comparison becomes genuinely load-bearing and deserves the unit pin.

## §4 Killing cases the v4 interpreter/evaluator selftests must add

`ref-v4.py` is a precedence-derived reference of the **A1** text (steps 1–15, features
H/F/L/G/D/HF/BE/SR/P transcribed from `plans/round-42-claims.md:66-136`) — a private
mutation-test harness, **not** a deliverable and not an oracle for other seats. Its
selftest = 37 cases (28 pair cases + 6 feature cases + boundary variants), pristine
37/37. Each round-41 survivor has an execution-verified killer on A1 semantics:

| survivor | v4 selftest case (input → expected) | verified killer (ref mutant) |
|---|---|---|
| I08 | `s11-mixed`/`s12-escaping`/`s12b-diag-level-holder`: SR token on a `diagnostics[]` holder (report-nested or diag-level) → `mixed-symlinks`/`escaping-symlink-removed` | NM-I16 (`__typename__`→`type`) fails all three |
| I10, E07 | `f-p-counts-every-file`: 5 files → features `P == 5` (pair stays `clean`/`none` — the pair oracle is magnitude-blind by design) | NM-I14 (P collapse) fails |
| I11 | `f-p-absent-is-zero` + `s14c-files-absent`: in-domain envelope without `files` → `P == 0`, pair `clean-empty`/`confirm-empty` | NM-I19 (absent→1) fails |
| I14 | `s3-no-squashfs`: only chunk `handler='gzip'` → `no-squashfs-chunk`/`inspect-input` | NM-I20 (F prefix dropped) fails |
| E01 | `f-be-token-not-substring`: child argv token `-be=1` → `BE == 'no'` (pair `avm-marker-be-dropped`) | NM-I17 (substring test) fails |
| E04 | **A1 changes the semantics**: SR = yes *iff* a `MaliciousSymlinkRemoved` report is in `diagnostics` — the round-41 K8 stdout-only envelope is no longer a counterexample. v4 case: `s12c-stdout-only-sr` (token only in `raw_result.execution.stdout.text`) → `clean`/`none`, pinning the IFF | NM-I12 (stdout fallback added) fails |
| E05 | `s12b-diag-level-holder`: `__typename__` directly on `diagnostics[]` → `escaping-symlink-removed` | NM-I13 (diag holder dropped) fails |
| E08 | `s4e-dep-plus-partial`: `missing-extractor-dependency` + `extractor-failure`, P=3 → `dep-missing-be`/`install-extractor-be` (step 4 first) | NM-I15 (steps 4/5 swapped) fails |

## §5 A1 delta — 17 new mutants on what v4 adds

All verified by execution: pristine reference passes, each mutant fails its named case
(`ref-mutants.json`, `binding-mutants.json`).

**Interpreter-side (11, on `ref-v4.py`):**

| id | defect | killing case (expected per A1) |
|---|---|---|
| NM-I1 | container row (step 2) placed after step 3 | `s2-container-trx`, `s2b-container-gzip`: F=∅ + `depth-limited`∈G → `container-depth-limited`/`raise-depth`, not `no-squashfs-chunk` |
| NM-I2 | step 2 predicate `and` → `or` | `s10-depth`: F={squashfs_v4_be} + `depth-limited` → `depth-limited`, not container |
| NM-I3 | step 2 additionally requires a `tar_*` handler | `s2-container-trx`: H={trx_v1} (A1's own example) → container |
| NM-I4 | step 6 tests `squashfs_v4_be ∈ F` instead of HF | `s6c-hf-trx`: ef gap names `trx_v1`, chunk `squashfs_v4_be`, P=0, BE=no → `body-extractor-failure`, not `avm-marker-be-dropped` |
| NM-I5 | L = exact names {v1,v2,v3} instead of the `squashfs_v1*/v2*/v3*` globs | `s7-legacy-ddwrt` (+`s7b-legacy-le`, `s7c-legacy-gap-handler`, `f-legacy-family-glob`): `squashfs_v3_ddwrt` → `legacy-body-failure`, not `body-extractor-failure` |
| NM-I6 | L too wide (`squashfs_v*`, matches v4) | `s8-v4le-body`: `squashfs_v4_le`, ef, P=0, BE=no → `body-extractor-failure`, not `legacy-body-failure` |
| NM-I7 | residue row (step 9) after depth row (step 10) | `s9-residue-plus-depth`: G={`unknown-chunk-handler`,`depth-limited`} → `unknown-residue`/`isolate-residue`, not `depth-limited` |
| NM-I8 | H built from chunks only (gap handlers dropped) | `s7c-legacy-gap-handler`: no chunks, ef gap handler `squashfs_v3_le` → `legacy-body-failure`, not `no-squashfs-chunk` |
| NM-I9 | step 4 dependency test exact-set instead of membership ("D holds") | `s4c-dep-membership-le` (+`s4d`): D={sasquatch,unsquashfs} → `dep-missing-le`, not `unclassified` |
| NM-I10 | step 2 keys on H=∅ instead of F=∅ | `s2-container-trx` (+`s2b`): H={gzip} nonempty, F=∅ → container |
| NM-I11 | legacy glob match with pattern/args swapped (`fnmatchcase(p, h)`) | `s7-legacy-ddwrt` (+`s7b`, `s7c`, `f-legacy-family-glob`) |

**Counter-side (6):** NM-C1 (single declared key not read — on the base counter, killed
by the §3 green case), NM-C2 (`lookup_combo_below_half` uses `<=` — killed by
`lookup-4-of-8-exactly-half`: exactly half must NOT pass), NM-C3 (lookup denominator =
the control output's own list length instead of the held-out total — killed by
`lookup-3-matched-of-12-heldout`: 3 matched of 12 held-out must be TRUE), NM-C4
(`combo_unseen_majority` uses `>` instead of `>=` — killed by `unseen-6-of-12-exactly-half`:
exactly half unseen must pass), NM-C5 (`counter_sha256` hashes the argv string instead of
the file bytes — killed by `sha-self-is-file-bytes`), NM-C6 (pin compared on an 8-char
prefix — killed by `sha-pin-full-equality`; plus the §3 manifest-level case). NM-C2…C6
verified on `binding-ref.py`, a micro-reference of the three A1 bindings (D4 + the two
combo bindings) with boundary-pinned selftest.

## Bounds compliance, tooling, restoration evidence

- Writes: this report, `artifacts/R42C2Mutants/`, seat scratch (removed at the end). No
  corpus/, tools/, plans/, PROVINCE/SCORECARD/SKILL/LOG writes; no fleet-repo or
  shokuknow writes; no VCS mutation anywhere (mutants ran on scratch copies; the
  selftest's fixture commits happen inside its own mkdtemp repos with the toplevel
  assertion); no subagents, no background jobs launched (four long commands were
  auto-backgrounded by the harness; their outputs are the recorded rows).
- Tooling authorization: **nothing installed or upgraded** — preinstalled `python3` and
  `git` only; sasquatch/sasquatch-v4be/unblob/unsquashfs/7z untouched; no pacman
  transactions.
- Lane restoration evidence: `git status --porcelain -- tools/round-41 tools/round-42
  SKILL.md corpus/evidence/round-41 corpus/lessons` → empty (the one dirty lane path,
  `plans/round-42-claims.md`, is L1's own uncommitted A1 amendment); lane
  `tools/round-41/c2-counter.py` sha256 `c6c1ea64…` unchanged; every mutant was a fresh
  scratch copy, pristine bytes never mutated; base extraction hashes equal the round-41
  frozen digests (§ header table).
- Runtime: counter selftest ≈ 34–36 s per probe (13 probes ≈ 8 min per sweep, two sweeps
  after two harness fixes: a `gen_seed_drift` patch that rebound `gen_src` after
  `tool_tree` captured it, and a failure-name parser that split on the case names' own
  `': '`); interp/eval + ref sweeps seconds.

## Artifacts (this dir: `.ufo/waves/round-42/w1/artifacts/R42C2Mutants/`)

| file | sha256 | note |
|---|---|---|
| `BASELINE.receipt.json` | `1702bda590131f990331629564a4e568047b1ecef57d87d38eeb9966f138f722` | pristine D2 receipt (93 429 B) |
| `M05.receipt.json` | `2fe9fec8008d6d44c39cb2a0cfb63ee3fdb640136b927cd186fd49991c48ec2b` | the verdict-flipping survivor's D2 receipt (exit 0, MET) |
| `baseline-counter-selftest.txt` / `baseline-d2.txt` | `f3db407a…` / `6440bf58…` | pristine D1/D2 outputs |
| `baseline-interp-selftest.txt` / `baseline-eval-selftest.txt` | `57342801…` / `a82b2978…` | pristine D1 (69 / 46 cases) |
| `baseline-interp-pairs.tsv` / `baseline-eval-pairs.json` | `1786de7d…` / `412b3881…` | pristine D3 (52 pairs each) |
| `counter-rederive-summary.jsonl` | `34c829cc…` | all 10 counter survivor rows: patch provenance, mutant sha256, D1+D2 outputs |
| `rederive-interp.py` / `rederive-interp.json` | `b0479b1a…` / `b087c2e4…` | §2 sweep driver + results |
| `killing-cases-counter.py` / `killing-cases-counter.json` | `ca03efa5…` / `87303a14…` | §3 case implementation + 12-probe verification |
| `ref-v4.py` / `ref-mutants.py` / `ref-mutants.json` | `23341c65…` / `66e2d116…` / `59699951…` | A1 reference harness (37 cases), 20-mutant sweep, results |
| `binding-ref.py` / `binding-mutants.json` | `dd1d0702…` / `e3745b6a…` | counter-binding micro-reference + 5-mutant sweep |

## Limits

- The counter killing cases were verified against the **v3** counter (the v4 counter is
  wave-2 work); they are specified in the harness's own scenario vocabulary so the v4
  port can adopt them verbatim. The manifest-level case is v4-only by contract and
  documents the v3 behavior it must replace.
- `ref-v4.py` implements the A1 precedence text only (no SKILL-table parser, no REA
  envelope quirks beyond the shapes the cases exercise); its role is to prove case
  sensitivity, not to be the v4 interpreter or evaluator.
- I10/E07 remain unkillable by any (label, action) oracle; their cases are
  feature-level (`P == len(files)`), which the v4 counter's `declared_features` binding
  also needs (it compares `published` as `nonzero`/`zero` — magnitude-blind like v3
  unless v4 widens it; A1 does not).
- D2 receipts are byte-different from round-41's because the lane tip moved between
  rounds; all semantic fields reproduce.
