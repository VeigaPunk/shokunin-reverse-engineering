PARTIAL — 3/6 mutants are killed by shipped selftests; the strict S timestamp clean oracle kills a fourth. Both C2 binding mutants survive selftest plus real measurement.

# MutateGuardsAndLint — author-side FALSIFY

Axes: **calibration** (do not count an already-red baseline as a kill), **coverage** (which promised checks reject regressions), **depth** (separate exit/count agreement from accepted evidence identity).

## Scope and provenance

- Attacks: **C1/D3** carrier check mode/ctime invariants; **C1/D2** committer-time and JSON coverage; **C2** `bound_evidence` operation/refusal conjuncts. No contract or production-source changes delivered.
- B = `14f0260ad319ecc26994381b2415d5a999003375`; F = `808cbb31a1e24656da5ba4967497e602fbca7415`; measured S = `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`.
- Own `tempfile.mkdtemp()` clone: `/tmp/kr20w2-MutateGuardsAndLint-lh0tqjlb`. Local `git clone -q --no-hardlinks`, detached checkout S, and `rev-parse HEAD` each exited **0**; observed HEAD was exactly S. The three starting source files were byte-compared with successful `git -C LANE show S:<path>` reads, not assumed from the working tree.
- Evidence saved from the clock at `2026-10-21T07:12:38.316781+00:00`. All **35** detector runs retain actual argv, start/end times, exit, stdout and stderr in `/tmp/kr20w2-MutateGuardsAndLint-evidence-eyeln1ka/probe-results.json` (387021 bytes; SHA-256 `5998bb8c7172b8619e3cb51a190fe29853d75d951461f3bbc842119d2c94d197`). This scratch evidence is not a committed lane artifact.
- Independent file families ran concurrently; each file had only one active mutant, followed by exact restoration and the same detector commands. First restoration measurements also provide pristine bytes before the second mutant. All selftest fixtures lived outside the clone in system-temp mkdtemp directories.

## Commands and detector results

Below, `R` is the clone above, `P=.ufo/waves/round-20/tools`, and `G=/tmp/kr20w2-MutateGuardsAndLint-evidence-eyeln1ka/guard-record`. G contains the exact `arm.json` blob read at S. Exit triples are **pristine → mutant → restored**; original S/B data remain pinned while the selected Python implementation is mutated.

| ID | Command (all actual exits appear in the mutant table) |
|---|---|
| ST(x) | `python3 -I -B "$R/$P/x" --selftest` |
| GS | `python3 -I -B "$R/$P/carrier-guard.py" check --manifest "$R/.ufo/waves/round-20/predictions/carriers.tsv" --record "$G"` |
| TS | `python3 -I -B "$R/$P/evidence-timestamps.py" --root "$R" --rev 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 --path .ufo/waves/round-20 --strict` |
| TB | `python3 -I -B "$R/$P/evidence-timestamps.py" --root "$R" --rev 14f0260ad319ecc26994381b2415d5a999003375 --path .ufo/waves/round-19 --strict` |
| VS | `python3 -I -B "$R/$P/verb-coverage.py" --root "$R" --rev 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` |

Source anchors below are **at S**, with paths relative to the lane. `tools/` abbreviates `.ufo/waves/round-20/tools/`.

| Mutant → attacked point | Expected detector/finding | Observed output and exits | Verdict |
|---|---|---|---|
| **G-mode** — `tools/carrier-guard.py:403`, replace execute-bit predicate with `False` | ST must require `mode_restored` in `mode_restored_and_content_changed` (`:552-569`). | ST **0→1→0**; mutant: `check missed expected findings: ['content_changed', 'ctime_changed']`; `SELFTEST: FAILED cases=4 fails=1`. GS **1→1→1**: 40→20→40 findings, with all 20 `mode_restored` findings absent only in mutant. | **KILLED by selftest**; GS baseline red, therefore inconclusive as a kill oracle. |
| **G-ctime** — `tools/carrier-guard.py:408`, replace ctime predicate with `False` | Same ST must require `ctime_changed` (`:568`). | ST **0→1→0**; mutant: `check missed expected findings: ['content_changed', 'mode_restored']`; `SELFTEST: FAILED cases=4 fails=1`. GS **1→1→1**: 40→20→40 findings, with all 20 `ctime_changed` findings absent only in mutant. | **KILLED by selftest**; GS independently inconclusive. |
| **T-author** — `tools/evidence-timestamps.py:159`, read `author-time` instead of `committer-time` | TS must remain clean for the real S round-20 tree under the introducing-committer contract. A distinct-author/committer fixture should expose the substitution, but is absent. | ST **0→0→0**, always `SELFTEST: CLEAN cases=4`. TS **0→1→0**, future findings **0→184→0**, with unchanged 883 scanned/20 skipped. TB **1→1→1**, future findings **1→808→1**. | **KILLED by TS clean oracle; SURVIVED shipped selftest**. Merely checking TB's exit 1 does not kill it. |
| **T-json** — insert `if display.endswith(".json"): continue` at `tools/evidence-timestamps.py:214` | `future_line_flagged`, `zulu_and_offset_parsed`, and `later_commit_line_uses_own_time` must still inspect their JSON fixtures; TB must retain `future_dated claims.json:36`. | ST **0→1→0**; all three named cases fail with `strict exit=0`; `SELFTEST: FAILED cases=4 fails=3`. TS **0→0→0**, but scanned **883→511→883**, skipped **20→19→20**. TB **1→0→1**, findings **1→0→1**. | **KILLED by selftest and TB positive-control oracle**; clean-only TS does not reject the omission. |
| **V-operation** — `tools/verb-coverage.py:163`, remove `all(t in blob for t in tokens)` while retaining refusal filter | Operation-mismatched retained evidence must not bind. A negative operation-binding fixture should fail. | ST **0→0→0**, always `SELFTEST: CLEAN cases=8`. VS **0→0→0**, always **133/153** mentioned and **5/5** targets exercised. JSON is **not** identical: mutant accepts wrong-operation evidence (example below); restored JSON equals pristine. | **SURVIVED** the shipped tests and measurement acceptance, despite observable bound-pair corruption. |
| **V-refusal** — `tools/verb-coverage.py:163`, remove `not any(t in blob for t in REFUSAL_TOKENS)` while retaining operation filter | A retained operation-matching refusal must not count as exercised. A refusal fixture should fail. | ST **0→0→0**, always `SELFTEST: CLEAN cases=8`. VS **0→0→0**, **133/153**, **5/5**. Complete parsed VS JSON is identical to pristine in mutant and restoration. | **SURVIVED**; no distinguishing exercised refusal case in these detectors. |

Pristine and every restored selftest report `SELFTEST: CLEAN cases=4` for guard/timestamps and `SELFTEST: CLEAN cases=8` for coverage. Neither guard defect is masked by the combined tamper fixture: it explicitly requires all three finding kinds, not merely a nonzero finding count.

## Observations versus inference

1. **Observed — real guard check is already red, not a killed mutant.** All pristine/restored GS runs report 20 carriers checked, 20 `mode_restored` and 20 `ctime_changed`. At S, `.ufo/waves/round-20/evidence/carrier-guard/disarm.json` records 20 carriers restored to `0o755` at `2026-10-21T05:57:43.966074Z`. I ran only **check** against those host paths: no Go carrier was executed, armed, disarmed or chmodded. Mode/ctime kills above come solely from clean→failed→clean selftests on temporary `/usr/bin/true` copies.
2. **Observed — timestamp selftests cannot distinguish author from committer.** `tools/evidence-timestamps.py:303-304` assigns both fixture dates from the same `when`. The T-author mutant survives all four cases. Real S does distinguish them: `.ufo/waves/round-20/evidence/c2/harmony/fa-json/receipt.json:18` contains `2026-10-20T20:52:08.478Z`; Git blame attributes it to F with author time `20:43:06Z` but committer time `21:01:54Z`. It is not future-dated under the actual contract. The mutant falsely labels it `future_dated ...:18` and still calls the emitted field `committer_time`.
3. **Observed — operation removal changes accepted identities without changing coverage.** For `compare-wasm-interfaces`, V-operation returns ID `ev_16a0be885adf3dee8f857604b91d409f4113a97e198b5875e0416f678e356d89` bound to `.ufo/waves/round-20/evidence/c2/wasm-inspect/evmole-repeat/receipt.json`. At S that receipt's `:7` names **inspect-wasm-artifact** and its bytes contain no `compare_wasm_interfaces`. This pair is absent from pristine/restored bound lists. The return value is capped at five pairs (`tools/verb-coverage.py:231`), so these are returned-list observations, not exhaustive bound cardinalities.
4. **Inference, grounded in observed survival — negative binding coverage is missing.** `tools/verb-coverage.py:250-304` tests absent/forged IDs, path existence and same-entry citation, but neither operation mismatch nor a matching-operation refusal. The forged-ID case cannot catch removal of either conjunct because its forged ID never occurs in retained bytes. V-refusal's survival does **not** establish that a real refused run is currently counted; it establishes that this regression was not caught.
5. **Limit:** these are direct tool measurements over Git objects at S, not a rerun of the entire `measure.py`/`routed-r19.py` claim pipeline. Those wrappers re-extract code from the named revision, so uncommitted implementation mutations would not propagate through an invocation still pinned to S. GS is necessarily a live read-only byte/mode check using the S manifest/arm record. No C1/C2 admission decision is made here; survivors are coverage findings, not permission to relax the contract.

## Exact-byte restoration

Common pristine **and restored** SHA-256 values (also verified by direct byte equality with the source fetched from S):

| Alias | File | Before = after each restoration |
|---|---|---|
| G | `tools/carrier-guard.py` | `62ab550c433741c343cd7f0c5c5e877a01e052f6babc25d0c067895db5eace6b` |
| T | `tools/evidence-timestamps.py` | `2c4fe4d554a4a74b4d7c653ef1157fc91e26796fc8c36b6716abbfdb4febf3a8` |
| V | `tools/verb-coverage.py` | `cfbf1880c4fb2bba80e3c2e40e236165a67c03bf51cced4983b469cfe315b26f` |

| Mutant | Before → mutated SHA-256 → restored |
|---|---|
| G-mode | G → `eb4a8eb028ef9b09b6708f42c14d2cf7c579dadfe13f483551e7c2f0c91f3145` → G |
| G-ctime | G → `b9ca4f384ee73c9d6391e06765d411c55410195b29e0fb80589ec19c321801ba` → G |
| T-author | T → `5d2bb0c53d44b721277d60834474e14b2cbe767622d4cbec1301472dd59e8e9b` → T |
| T-json | T → `d52124546ecc256db14fe998f6af6e68277d947639fb1c8e2901867a57f7e96c` → T |
| V-operation | V → `b058de76fc90a39f0daf36a23f1334dbb3d11b2efe1d87b2487e99d512b1f867` → V |
| V-refusal | V → `709a6e304f027f9a102798d2f1d90e169d7c6556a6d5723f86335abbd10a5344` → V |

All six restoration byte-equality checks were **true**, with the same detectors rerun on restored bytes. Only this report was written in the lane. No installs/upgrades, REA analysis, Ghidra, Go toolchain executions, lane Git writes, client-config edits, or sibling-source edits.
