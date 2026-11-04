# ConnectorScope — Round-84 Wave 1 Sibling-Overlap Scan & Connector Move

Seat: `ConnectorScope` (connector, round-84 wave `r84-w1`)  
Lane: `kaidoku-shokunin` · L1: `KaidokuR84`  
Base: `043b89a25241710a68b45526c3287fb3c8d907c3`  
Declaration: `e0de2088a7bddc16305357f90ac7e889fa0a0d11`  
First container: `a5663ddedd157bb9113928f5fe80509d6f3fc7a1`  
Milestone: Claim metadata, mutation closure, nested container chain  
Owned axes: Coverage, depth, calibration, freshness  

Receipt: `.ufo/waves/round-84/w1/ConnectorScope/sibling-scan.json` (sha256 checked, scratch cleaned)

---

## 1. Executive Summary

A comprehensive read-only scan across all 21 fleet lanes (`/home/vgpnk/Projects/shokunin/*-shokunin`, covering `corpus/QUALITY.md`, `tools/`, `plans/`) and `/home/vgpnk/Projects/shokunin/scripts/` determined that **no other lane in the fleet holds an instrument that round 84 duplicates or contradicts**. Specifically:

1. **Prefreeze claim-metadata gate (`tools/round-84/freeze-precheck.py`):** Other lanes possess prefreeze checks, but they either validate wave orchestration and prompt rendering (`chousa-shokunin`), replay command output on base trees (`kagi-shokunin`, `kasegi-shokunin`), evaluate git commit graph precedence (`mori-shokunin`), parse Markdown preregistration syntax (`souji-shokunin`), or audit post-hoc ledgers (`kotodama-shokunin`, `tameshi-shokunin`). None inspects JSON claim container strings for counter script paths or binds them mechanically to top-level pin digests with an `instruments-only` failable control.
2. **Mutation-closure counter scoring kills by declared case (`tools/round-84/mutation-closure.py`):** Multiple lanes enforce mutation testing policies, but none scores a frozen text-edit table against a target tool's own `--selftest` case inventory where a kill strictly requires the *declared* case to appear in the target's reported `failures` list (QUALITY Row 138).
3. **Nested-SquashFS depth measurement (`tools/round-84/nested-sqfs.py`):** No other lane in the fleet measures multi-level nested SquashFS container chains or REA/unblob depth-limiting behavior. `revenger-shokunin` recorded observations on REA 6.5.0 but explicitly documented that SquashFS and nested member extraction were unknown and untested.

In addition, five lanes maintain stricter freeze-gate or ledger conventions than Kaidoku's baseline `tools/round-29/freeze-gate.py` + `corpus/claim-freezes-v2.tsv`: `souji-shokunin` (git ancestry via `merge-base --is-ancestor`, `DISPATCH-BEFORE-FREEZE`, symlink bans), `mori-shokunin` (commit graph temporal ordering of frozen inputs vs implementation commits across `base..tip`), `kotodama-shokunin` (pure `git cat-file` plumbing without shell commands, full 40-hex commit hashes, drift/vacuity checks), `kagi-shokunin` (command execution under timeout with regex match on last line, `stamps.tsv` prune protection), and `chousa-shokunin` (cross-artifact digest embedding and `DIGEST_STRAY` prompt sanitization).

---

## 2. Sibling-Overlap Scan Results

### 2.1 Category 1: Prefreeze Claim-Metadata Gate

Kaidoku's `tools/round-84/freeze-precheck.py` evaluates `.ufo/waves/round-N/claims*.json` at `--rev` before the declaration commit. For each claim, it verifies that:
- The claim's strings name a lane-relative script path (`tools/`, `corpus/`, `.ufo/` + `.py`, `.sh`, `.mjs`, `.js`);
- The named script exists as a Git blob at `--rev` (`COUNTER_BLOB_ABSENT`);
- The path is recorded in `PIN_KEYS` (`instruments`, `loaded_by_counter`, `producers_not_counters`) (`COUNTER_PATH_NOT_PINNED`);
- The pinned SHA-256 matches the blob's actual digest at `--rev` (`COUNTER_PIN_MISMATCH`);
- The `--control instruments-only` rule demonstrates failable semantics by accepting defective containers that provide an instruments map without per-claim path binding.

#### Fleet Hits:
1. **`chousa-shokunin`: `tools/freeze-check.py`**
   - *What it does:* Pre-ready verification of wave spec, dispatch, and ready payloads against `plans/round-N.md`. Checks `CLAIMS_NONEMPTY`, `CONTEXT_DIGEST`, `DIGEST_STRAY`, `CONTEXT_SPEC_EQ`, `NAMES`, `BODY_RENDER`, `READY_DISPATCH`, and `READY_IDENT`.
   - *Disposition:* **Stay separate.**
   - *Reason:* Chousa's gate governs wave orchestration files and prompt template rendering consistency. It does not inspect JSON claim container objects, does not parse claim predicate strings for executable paths, and does not verify Git blob digests against container pins.
2. **`souji-shokunin`: `tools/souji-freeze-check.py`**
   - *What it does:* Pre-dispatch checklist reading Markdown preregistrations (`## C<digits>` syntax). Validates `Key: value` headers (`Counter: <path> sha256=<hex>`), checks that counters and populations are git blobs, enforces `git merge-base --is-ancestor <base> <freeze>`, and flags `DISPATCH-BEFORE-FREEZE`.
   - *Disposition:* **Stay separate.**
   - *Reason:* Souji validates text/Markdown preregistrations with a custom syntax, rather than JSON claim containers. It checks commit graph ancestry and dispatch timing, but does not extract script references embedded within claim prose sentences or evaluate an `instruments-only` control.
3. **`kasegi-shokunin`: `corpus/instruments/freeze-check.py`**
   - *What it does:* Replays every claim's `counter_cmd` against the base tree. Verifies that `expect_before` matches output, `expect_after` is absent, and the base tree remains unmutated.
   - *Disposition:* **Stay separate.**
   - *Reason:* Kasegi's tool is a dynamic execution replay harness for command strings; Kaidoku's `freeze-precheck.py` is a static metadata binding gate linking claim prose to Git blob pins.
4. **`kagi-shokunin`: `corpus/prefreeze-control.sh`**
   - *What it does:* Extracts the base revision into a scratch tree, runs declared counting commands from `plans/round-N.controls.tsv`, and asserts that stdout integers equal expected values.
   - *Disposition:* **Stay separate.**
   - *Reason:* Replays numeric counting commands from TSV controls; does not validate claim container schemas, prose script references, or digest pins.
5. **`mori-shokunin`: `tools/mori-freeze-order.py`**
   - *What it does:* Reads `mori-freeze-register-v1` JSON to assert that declared frozen files (`frozen: [...]`) predate implementation commits (`impl: [...]`) in the commit range `base..tip`.
   - *Disposition:* **Stay separate.**
   - *Reason:* Enforces commit ordering between specification and implementation; does not parse claim sentences for counter script paths or pin consistency.
6. **`kotodama-shokunin`: `tools/ledger-token-guard.py`**
   - *What it does:* Reads claim ledger pairs, re-running recorded observations via `git cat-file` against immutable 40-hex commit hashes to prevent observation drift and vacuity.
   - *Disposition:* **Stay separate.**
   - *Reason:* Post-hoc observation verifier for ledger pairs, not a prefreeze gate for claim container validation.
7. **`tameshi-shokunin`: `tools/coldread-precheck-portable.py`**
   - *What it does:* Replaces per-lookup `git` subprocess spawns in historical coldread ledger checkers with batch-cached `git cat-file` and `git ls-tree` operations.
   - *Disposition:* **Stay separate.**
   - *Reason:* Performance optimization for large historical git-blob lookups, not a claim-metadata gate.
8. **Fleet Scripts (`scripts/hyaku/hyaku.env`, `scripts/hyaku/lane-addendum.md`):**
   - *What they do:* Configuration and dispatch templates mentioning prefreeze protocol steps.
   - *Disposition:* **Stay separate.** No instrument implementation present.

---

### 2.2 Category 2: Mutation-Closure Counter Scoring Kills by Declared Case

Kaidoku's `tools/round-84/mutation-closure.py` evaluates `.ufo/waves/round-84/mutants.json` (13 single-behavior text changes across `tools/round-82/conjunction-gate.py`, `tools/round-82/printed-command.py`, and `tools/round-83/source-bind.py`). It applies each edit in private scratch, restores pristine bytes, runs the target's `--selftest`, and scores the mutant killed **only if the mutant's declared case appears in the selftest failing-case inventory** (QUALITY Row 138). If the declared case does not fail, the mutant survives; if the declared case is absent from the pristine selftest inventory or pristine is red, the result is inconclusive.

#### Fleet Hits:
1. **`kake-shokunin`: `corpus/QUALITY.md` (Round-80 criterion)**
   - *What it does:* Requires survivor mutants to be closed by isolated test fixtures that flip a single conjunct.
   - *Disposition:* **Stay separate.**
   - *Reason:* Kake evaluates external tool behavior against isolated fixture files, rather than scoring single-edit text mutations against a target tool's internal `--selftest` case failure list.
2. **`kengaku-shokunin`: `plans/mutant_direction_check.py` (QUALITY 29, 31, 33, 37)**
   - *What it does:* Checks kill direction (`rc-silence` vs `rc-mirror`) for frozen gate mutants and enforces mutant population floors.
   - *Disposition:* **Stay separate.**
   - *Reason:* Classifies gate mutant sensitivity directionally on whole-script exit codes, but does not match kills against declared selftest case names.
3. **`mori-shokunin`: `tools/mutate-c2.py` (QUALITY 165, 177)**
   - *What it does:* Asserts that a selftest arm added for a named mutant fails on that mutant and passes on pristine.
   - *Disposition:* **Stay separate.**
   - *Reason:* Evaluates arm labels and tallies without the structured `mutants.json` text-replacement table or declared-case failure parsing.
4. **`tameshi-shokunin`: `.ufo/waves/round-56/w1/T56W1MutGate-receipts/10-driver-mutate.py` (QUALITY 89)**
   - *What it does:* Generates single-edit mutants of gate scripts, asserting that each mutant exits non-zero and prints a line starting with `FAIL `.
   - *Disposition:* **Stay separate.**
   - *Reason:* Scores whole-process non-zero exit codes and generic `FAIL ` line prefixes, lacking granular attribution to declared selftest case identifiers.
5. **`tsukuroi-shokunin`: `tools/mutants-owed-statements-r29-v4shapes.py`, `tools/mutants-btrfs-space-r30.py`**
   - *What it does:* Bespoke AST and regex statement mutation harnesses testing whether administrative and census tools report discrepancies.
   - *Disposition:* **Stay separate.**
   - *Reason:* Domain-specific statement replacement scripts; no declared-case failure matching or restoration verification.
6. **`kama-shokunin`: `tools/round69-newest-closure-counter.py`**
   - *What it does:* Audits whether `SCORECARD.md` names the newest verifier-spotcheck file by date and round number.
   - *Disposition:* **Stay separate.**
   - *Reason:* Homonym match on "closure"; this tool performs spotcheck file dating, completely unrelated to mutation testing.

*Synthesis:* Kaidoku's mutation closure counter is the sole fleet instrument executing QUALITY Row 138, providing exact declared-case attribution with single-anchor verification and pristine byte restoration.

---

### 2.3 Category 3: Nested-SquashFS Depth Measurement

Kaidoku's `tools/round-84/nested-sqfs.py` measures nested sub-images below depth 1 on a reproducible three-level chain of little-endian SquashFS v4 images (`a.sqfs` outer, `b.sqfs` mid, `c.sqfs` leaf, built with `mksquashfs 4.7.5`, gzip, `-repro-time 1760000000`). It evaluates REA 6.5.0 `extract-firmware` across `--max-depth 3` and `--max-depth 4`, testing arms A1–A9:
- Both depth runs publish identical 8/8 oracle members with identical SHA-256 digests;
- Depth 3 reports `coverage: partial`, 1 depth-limited path (`inner-b.sqfs_extract/inner-c.sqfs_extract`), 1 `depth-limited` extraction gap, and level-3 files carry `analysis_depth: null`;
- Depth 4 reports `coverage: complete`, 0 depth-limited paths, 0 gaps, and level-3 files carry `analysis_depth: 3`;
- Unblob engine identity is invariant across runs;
- The file-count control proves that a naive counter checking only "published file count == oracle count" would falsely report depth 3 complete.

#### Fleet Hits:
1. **`revenger-shokunin`: `corpus/live/runs/round-63/LEDGER.md`**
   - *What it does:* Records observations of REA 6.5.0 on a 2048-byte synthetic firmware image. Lines 51–53 explicitly state under limitations:
     - `U1`: "Other signatures... squashfs... cannot show whether the route detects any other firmware signature family."
     - `U2`: "Extraction completeness. The record extracted nothing (`extractions = {}`)."
     - `U3`: "Scan depth inside member bytes... Unknown for the record."
     - Revenger has 0 tools in `tools/`, no SquashFS generator, and no depth measurement scripts.
   - *Disposition:* **Stay separate.**
   - *Reason:* Revenger documented the *absence* of SquashFS extraction and nested-depth capabilities; Kaidoku provides the active, reproducible multi-level SquashFS chain measurement.
2. **`game-dev-3d-shokunin`: `corpus/knowledge/rea.md`**
   - *What it does:* Mentions unblob as an underlying engine dependency for REA in documentation.
   - *Disposition:* **Stay separate.**
   - *Reason:* Pure documentation note; no measurement or firmware extraction tooling.

*Synthesis:* Kaidoku's `tools/round-84/nested-sqfs.py` is the only instrument in the fleet measuring multi-level nested container chains and engine depth-limiting behavior.

---

## 3. Fleet Freeze-Gate and Ledger Conventions Comparison

Kaidoku's baseline freeze-verification architecture consists of:
- **`tools/round-29/freeze-gate.py`**: A post-hoc maintained audit of all `.ufo/waves/round-*/claims*.json` files. For each claims file, it identifies its freeze commit (`log --diff-filter=A`), checks script paths inside claim strings, verifies blob existence and SHA-256 pins, and checks whether commits in `freeze..MEASURED` modified the script without being listed in `instrument_supersessions`.
- **`corpus/claim-freezes-v2.tsv`**: A TSV ledger with schema `round<TAB>verdict<TAB>findings<TAB>pointer`. Audited freezes must match the recorded verdict and findings exactly, with zero unrecorded freezes and zero stray rows.

### Stricter Shapes Identified Across the Fleet:

1. **`souji-shokunin` (`tools/souji-freeze-check.py`)**
   - *Git Ancestry Enforcement:* Requires `git merge-base --is-ancestor <base> <freeze>`, preventing disconnected base commits from passing validation.
   - *Wave Timing Isolation:* Flags `DISPATCH-BEFORE-FREEZE` if any wave file (`*-dispatch*`, `*.ready*`, `*-spec.json`, `*-results.json`) is committed at or before the freeze commit.
   - *Filesystem Strictness:* Rejects symlinks for counters, populations, and controls (`COUNTER-SYMLINK`, `POPULATION-SYMLINK`, `CONTROL-SYMLINK`).
   - *Syntax Strictness:* Forbids duplicate keys in claim blocks (`KEY-DUPLICATE`) and rejects malformed round values (`ROUND-MALFORMED`).

2. **`mori-shokunin` (`tools/mori-freeze-order.py`)**
   - *Commit Precedence Verification:* Validates via `git diff-tree` across `base..tip` that declared frozen inputs (`frozen: [...]`) predate implementation commits (`impl: [...]`), preventing post-hoc generation of "frozen" assets.
   - *Strict JSON Grammar:* Rejects duplicate dictionary keys and non-standard numeric constants during register parsing.

3. **`kotodama-shokunin` (`tools/ledger-token-guard.py`)**
   - *Plumbing-Only Isolation:* Re-runs claim ledger observations strictly through `git cat-file`, eliminating `bash` subprocess invocations, environment variable inheritance, and shell injection risks.
   - *Immutable Commit Pinning:* Requires full 40-hex commit hashes (`observe.rev`), rejecting mutable identifiers (HEAD, tags, branch names).
   - *Two-Sided Observation Verification:* Verifies that observed values match historical baselines while asserting non-vacuity (`stated_token != observed_token`).

4. **`kagi-shokunin` (`corpus/claim-ledger.sh` + `corpus/claim-ledger.tsv`)**
   - *Mechanical Execution Gate:* Executes every claim command under a timeout, requiring exact exit code match AND exact regex match against the last non-empty line of stdout.
   - *Ledger Prune Protection:* `corpus/stamps.tsv` (`path<TAB>sha256<TAB>lines<TAB>bytes`) forbids shrinking without an explicit `--prune` flag, preventing accidental dropping of tracked files.

5. **`chousa-shokunin` (`tools/freeze-check.py`)**
   - *Prompt Context Hygiene:* Verifies that the reference SHA-256 of `plans/round-N.md` is present in dispatch context (`CONTEXT_DIGEST`) and asserts that no unexpected 64-hex SHA-256 tokens appear in prompt bodies (`DIGEST_STRAY`), preventing cross-wave context leakage.

---

## 4. UFO-FSD Connector Move: Dual-Sided Supersession & Gate Audit Binding

### 4.1 Evidence and Cross-Seat Synthesis

The wave 1 seats provide complementary assets that interact across verification surfaces:
- **`ExecGateForge`** proved that `tools/round-84/freeze-precheck.py` is robust against 11 forgery attacks, and confirmed that solo `--expect FLAGGED` runs exit 1 because `met` requires `accepted_expected >= 1`. Exit 0 requires both an accepted container and a refused container (`combined.json`), exactly matching the C1 counting command.
- **`ExecPcDetectors`** provided candidate patch `printed-command-candidate.patch` extending `tools/round-82/printed-command.py` with 7 declared selftest cases, killing all 7 round-82 survivors (`pin-call`, `static-refusal`, `source-mined`, `source-date`, `source-base`, `source-plan`, `source-entry`). The candidate digest is `91a01190bed4e5cd957177b77e6633e2928ead2a6b8bac581ee5ab7193b92a9f` (frozen release pin at BASE is `88b1dff2385547e1bdb2ecf802d667c38eabe929747075c27ae88f0c5c061487`).
- **`ExecSbDetectors`** provided candidate patch `source-bind.patch` extending `tools/round-83/source-bind.py` with 2 declared selftest cases, killing both round-83 survivors (`sb-header-position`, `sb-duplicate-last`).
- **`ExecMutantBase`** verified the BASE arm of `tools/round-84/mutation-closure.py` (4 killed, 9 survived, exit 1).
- **`ExecNested`** independently reproduced `tools/round-84/nested-sqfs.py` end-to-end, confirming all 14 checks and file-count control behavior across `--max-depth 3` and `--max-depth 4`.

### 4.2 The Hidden Second-Order Contradiction

When L1 integrates the candidate detector patches to satisfy C2 (13 killed, 0 survivors), `tools/round-82/printed-command.py` is modified in the landing commit.

`printed-command.py` is a released tool frozen in `.ufo/waves/round-82/claims.json`. If L1 commits the detector patch without appending the landing commit to `instrument_supersessions` in `.ufo/waves/round-82/claims.json`:
1. The standing maintained gate (`tools/round-29/freeze-gate.py`) will audit all historical claims and flag `round-82` with `INSTRUMENT_REVISED` (`findings: ["INSTRUMENT_REVISED"]`), turning the fleet ledger check (`freeze-gate.py --disclosures corpus/claim-freezes-v2.tsv`) RED (exit 1).
2. R84-C2's own kill rule will be violated:
   *"a target digest differing from the frozen release pin without a disclosed `instrument_supersessions` entry."*
3. Conversely, `tools/round-83/source-bind.py` was introduced in commit `730ddc65` during round 83 but was never listed in `.ufo/waves/round-83/claims.json` (which pinned only `attribution-audit.py`). Modifying `source-bind.py` does not alter `round-83/claims.json` audit status, but modifying `printed-command.py` does.

### 4.3 Proposed Move

**Dual-Sided Supersession & Gate Audit Binding:**
At the landing commit `REV_LAND`:
1. **Landed Supersession Disclosure:** In `.ufo/waves/round-82/claims.json`, append an entry to `instrument_supersessions`:
   ```json
   {
     "path": "tools/round-82/printed-command.py",
     "commit": "<REV_LAND>",
     "reason": "Add seven declared selftest cases for R84-C2 mutation closure; parameterize sourced_arm while preserving frozen anchor counts"
   }
   ```
2. **Conjunction Gate Invariance:** Ensure `tools/round-82/conjunction-gate.py` remains 100% byte-untouched (`f009009993160ca40dd55d771f8c05ce1e32799c22450f5430cae2c6e0bf163a`), preserving its 4 BASE kills without triggering supersession.
3. **Simultaneous Dual-Gate Assertion:** The landing verification must invoke both gates in lockstep:
   - Prefreeze claim-metadata gate: `python3 -I -B tools/round-84/freeze-precheck.py ... --rev <REV_LAND>` (passes CLEAN, Refused=1, Accepted=1).
   - Historical freeze gate: `python3 -I -B tools/round-29/freeze-gate.py --disclosures corpus/claim-freezes-v2.tsv --rev <REV_LAND>` (passes CLEAN on all 59 containers, with round-82 verified CLEAN via the disclosed supersession).

### 4.4 Affected Axes

- **Calibration (+):** Mechanically closes the gap between C1's prefreeze gate and the fleet's post-hoc audit, preventing `INSTRUMENT_REVISED` ledger discrepancies and upholding C2's kill rule.
- **Depth (+):** Enables all 13 mutants to die by declared cases (13/13 killed) on the candidate detector targets while maintaining exact custody and pin provenance.
- **Coverage (0):** Unaffected; C3's nested container chain measurement operates independently on REA 6.5.0 and SquashFS fixtures.
- **Freshness (0):** Preserves standing disclosure consistency and ledger cleanliness.

### 4.5 Risks and Second-Order Effects

- *Risk:* If the supersession entry uses a short hash or placeholder commit rather than the exact landing commit SHA, `freeze-gate.py` will report `INSTRUMENT_REVISED`.
- *Mitigation:* L1 integrates the detector patches and claims disclosure within the atomic landing commit, or amends the disclosure commit immediately with the exact full commit hash.

### 4.6 Verification

Execute in sequence at the landing commit `REV_LAND`:
```sh
# 1. Verify R84-C1 prefreeze claim-metadata gate
python3 -I -B tools/round-84/freeze-precheck.py --root . --rev $REV_LAND \
  --container .ufo/waves/round-83/claims.json --expect .ufo/waves/round-83/claims.json=FLAGGED \
  --container .ufo/waves/round-84/claims.json --expect .ufo/waves/round-84/claims.json=CLEAN \
  --control instruments-only
# Expected: exit 0, mismatches [], refused_expected 1, accepted_expected 1, met true

# 2. Verify R84-C2 mutation closure on landed targets
python3 -I -B tools/round-84/mutation-closure.py --root . --rev $REV_LAND \
  --mutants .ufo/waves/round-84/mutants.json --work /fast/scratch/hyaku/kaidoku-r84/verify-c2/
# Expected: exit 0, killed 13, mutants 13, survivors [], inconclusive [], pristine_failed [], ok true

# 3. Verify fleet maintained freeze-gate ledger consistency
python3 -I -B tools/round-29/freeze-gate.py --disclosures corpus/claim-freezes-v2.tsv --rev $REV_LAND
# Expected: exit 0, all audited containers match ledger disclosures exactly
```

---

## 5. Scope and Tooling Statement

- **Write Scope:** Writes were strictly confined to `.ufo/waves/round-84/w1/ConnectorScope.md` and `.ufo/waves/round-84/w1/ConnectorScope/sibling-scan.json`. No production files, sibling-lane files, fleet-root files (`LOG.md`, `SCORECARD.md`), or frozen bytes were created or modified.
- **Git Mutation:** Read-only inspection only (`git log`, `git show`, `git cat-file`). Zero git mutations, commits, or pushes executed.
- **Scratch Lifecycle:** Scratch directory `/fast/scratch/hyaku/kaidoku-r84/ConnectorScope/` was used for intermediate scan processing, receipts copied to the wave directory, and the scratch directory completely removed prior to yielding.
- **Tooling Compliance:** Evaluated with existing host Python 3.14.8 and Git 2.56.0. No tools installed, upgraded, or removed.
