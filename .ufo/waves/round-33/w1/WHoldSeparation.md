# WHoldSeparation — Builder-dependent artifact absence, import hygiene, and residual-dependency flags for R33-C1

Reviewer/leaf seat, round 33 w1. Scope: verify that every builder-dependent artifact listed in `quarantine-record.json` is absent from the committed tree, that no retained (admitted) module imports or loads them, and that no residual held-data dependency remains in reachable lane material. Read-only lane; only this report was written in lane. No subagents, no background jobs, no builds/tests/linters/formatters, no runs of the retained modules (only their existing selftest receipts were read), no carrier execution, no git/jj writes, no installs (no tooling updates — nothing installed).

## 0. Observed revision and evidence basis

- Lane HEAD == pinned admissible revision: `d7076120e4f00c6d18aa77b8764d14861e820eb2` (commit; verified `git rev-parse HEAD` and `git cat-file -t`).
- Base `428315a8f5674b952def862910af6e07a6c2224b` exists as an object.
- Only permitted hold metadata was consulted: `safety-holds.json`, `quarantine-record.json` (provider-error metadata and excluded path list). The quarantine directory `/fast/scratch/hyaku/kaidoku-r33/quarantine-cyber-policy-20261023T091126Z`, the held item `U064N008Hf47eb933`, and the held seat's output/transcript findings were NOT opened.
- `lsp` device: not available (mounted devices are only `ast_edit`, `debug`); caller/import/diagnostics checks therefore used literal text `git grep`/`grep` as the fallback, recorded here per tool policy.

## 1. Excluded builder-dependent artifacts — absent from committed tree AND working tree

`quarantine-record.json` lists 8 excluded paths. Each was checked against `HEAD` (`git cat-file -e HEAD:<path>`) and against the working tree (`test -e`):

| Excluded path | In committed tree | On disk |
|---|---|---|
| `tools/round-33/chpe_fixture_gen.py` | ABSENT | GONE |
| `tools/round-33/chpe_predict.py` | ABSENT | GONE |
| `tools/round-33/chpe_driver_manifest.py` | ABSENT | GONE |
| `.ufo/waves/round-33/frozen` | ABSENT | GONE |
| `.ufo/waves/round-33/prefreeze-controls` | ABSENT | GONE |
| `.ufo/waves/round-33/prep/R33FixtureBuilder.md` | ABSENT | GONE |
| `.ufo/waves/round-33/prep/R33ChpeParser.md` | ABSENT | GONE |
| `.ufo/waves/round-33/prep/builder-count-erratum.txt` | ABSENT | GONE |

Independent corroboration: `git ls-tree -r --name-only HEAD` contains **no** path matching `chpe_fixture_gen`, `chpe_predict`, `chpe_driver_manifest`, `round-33/frozen`, `prefreeze-controls`, `R33FixtureBuilder`, `R33ChpeParser.md`, or `builder-count-erratum`. The committed `round-33` set contains only the retained artifacts: `tools/round-33/{chpe_profile, selftest_pegen, measure_driver, r32_oracle_adapter, disk-command-audit, freeze-integrity}.py`, `tools/round-33/timestamps/*`, and `.ufo/waves/round-33/` metadata/recs (including `prep/R33ChpeParser-independent.json` — the retained *independent* variant, distinct from the excluded mixed report). Working-tree `git status --porcelain` shows only the untracked w1-dispatch/record/spawn/spec/submitted JSONs and the untracked `w1/` report directory; no excluded path is untracked or modified.

## 2. No independent tool imports/loads the excluded artifacts

Static load-surface review of every retained round-33 module (full reads of all four admitted modules; load-site grep across the retained `tools/round-33` set; committed-content `git grep` across `tools/round-33`, `.ufo/waves/round-33`, and round-33 corpus files for every excluded artifact name and quarantine path):

- `chpe_profile.py`: stdlib imports only (`hashlib,json,os,struct,subprocess,sys,tempfile`). Runtime reads only (a) its CLI input byte path (`argv[0]`), (b) in `selftest()` its own file re-invoked as subprocess and synthetic bytes. `selftest_pegen` is imported lazily inside `selftest()` only. No excluded path, no `frozen`, no `prefreeze`, no quarantine string anywhere.
- `selftest_pegen.py`: imports only `struct`; builds synthetic PE32+ bytes; reads nothing. No dependence on or reference to held code/data.
- `measure_driver.py`: stdlib + optional `git` subprocess. Reads classifier bytes, manifest, document-spec and row paths via `Source` (worktree absolute paths or `git cat-file` at a given rev). No excluded path constants; no builder references.
- `r32_oracle_adapter.py`: stdlib + `load_oracle()` which hash-guards (`ORACLE_SHA256 = 17eea1f9…`) and `exec`s the committed `tools/round-32/arm64x_oracle.py` (verified committed; on-disk sha256 matches the pin). The round-32 oracle is a retained, unfiltered instrument — not held data, not a builder output, and not a carrier fixture. `selftest_pegen`/`measure_driver` imports are lazy inside `selftest()`.
- Retained toolset files (`disk-command-audit.py`, `freeze-integrity.py`, `timestamps/run-gate-hashed.py`, `build-hashed-fixture.sh`, `run-hashed-selftest.sh`): load sites are stdlib, own re-invocation, or the retained `evidence-timestamps.py` (round-20) / git fixture repos under `/fast/scratch/hyaku/kaidoku-r33/…`; none touch excluded artifacts. `freeze-integrity`/`run-gate-hashed` operate on synthetic fixture repos (round 99 / plan-vs-actual clones), not on held data.

Lane-wide committed-content grep for `chpe_fixture_gen|chpe_predict|chpe_driver_manifest|prefreeze-controls|R33FixtureBuilder|builder-count-erratum|quarantine-cyber-policy` returns matches **only** in `quarantine-record.json`'s `excluded_paths` metadata (the sole permitted reference) and in the wave dispatch/spec/submitted/spawn record texts (assignment text). No retained module, receipt, prep file, knowledge file, or source capture carries any of them.

The independent record `prep/R33ChpeParser-independent.json` declares `no_held_fixture_use: true` and pins the four module digests; the three retained selftest receipts (`selftest-chpe_profile.json`, `selftest-measure_driver.json`, `selftest-r32_oracle_adapter.json`) all report `pass: true` and are instrument evidence only. Module sha256 values (verified on disk) match `parser-pins.json` and the independent record bit-for-bit.

## 3. Residual held-data dependency flags (found; reported, NOT repaired/rerouted)

1. `prep-settle.json:435` and `prep-provenance-final.json:159` reference the held seat name `R33FixtureBuilder` and `prep-settle.json:435` names the excluded report path `prep/R33FixtureBuilder.md`. These lines are **metadata only** (seat name/status/report path in the spawn ledger) and contain no held findings; they are permitted as hold metadata. No action taken — the reference is record-keeping, not a loaded dependency.
2. `prep/R33FixtureDesign.md` is a committed, retained prep document that documents carrier-geometry design facts for the stopped claim (e.g. k01/k04/k12 section/offset/byte-span constants, read-only opens of `/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll` at 2026-10-23T08:11:25Z). It is not in the quarantine exclusion list and contains no builder *output*; its design constants are carrier-geometry facts (the exemption's `k01/k02/k08 derivative` bar applies to builder-derivative use, and this document is a design prep from the pre-hold phase). It is flagged as the closest committed neighbor to held-adjacent material and is NOT imported/loaded by any retained module — no code path reads it.
3. `prep/R33ClaimAttack.md:21,123` cites `corpus/evidence/round-32/independent-pe/readobj-k04.txt:106-155` and `a2audit/A2CHPEBits.md` retained captures (kept reader captures, not direct carrier bytes). These are round-32 retained evidence, not held builder data; flagged for completeness only.
4. No committed file other than `quarantine-record.json` references the scratch quarantine path. No committed file references `U064N008Hf47eb933` except policy/containment sentences (prep-contract, prep docs, lessons) that explicitly forbid inspection — no dependency, but the identifier is present as exclusion text.

## 4. Verification gaps

- Static-only separation: import/path/metadata analysis does not prove runtime-environment isolation beyond the modules' own fixed paths and pinned hashes (e.g. a hypothetical runtime read of a held path by something else was not observed, because nothing was executed).
- `selftest_pegen.py` has no standalone selftest receipt; it is exercised only indirectly through the `chpe_profile` and `r32_oracle_adapter` selftest receipts (also noted by WDataflow §7).
- The retained selftest receipts were not rerun in this wave (not assigned; verification rests on receipt content plus hash equality to pinned module bytes).

## 5. Findings summary

- No finding at blocker severity. All 8 excluded builder-dependent artifacts are absent from both the committed tree and the working tree; no retained module imports, loads, or references any of them; the only lane occurrences of excluded names are the permitted hold-metadata records and wave assignment text.
- Residual flags (§3) are record-keeping or design-prep references; none is a loaded held-data dependency. Per assignment, they are reported and not repaired/rerouted.
- Nothing here modifies the stopped claim: R33-C1 remains `unprovable; honest stop` (`claim-stop.json`); these checks are separation evidence, not a replacement admission benchmark or a revived carrier claim.

## 6. Tooling

No installs or updates performed (nothing needed; no pacman transaction, no uv/npx binary install). Tools used: `read`, `glob`, `grep`, `bash` (`git rev-parse`/`cat-file`/`ls-tree`/`grep`, `sha256sum`, `test -e`, `grep` literals — all read-only), `write` for this report only. `git`/`jj`: no lane/fleet writes performed. All paths observed under the lane or the retained scratch roots; no `du`/`find` walked over scratch.
