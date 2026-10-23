# MutFreezeIntegrity — round 31, wave 2

## Result and boundary

- **[OBSERVATION] Pristine gate: holds for all five assigned fixtures.** Clean is accepted; an edited frozen input, an edit followed by an exact-byte revert, a deleted instrument, and a changed input with a post-freeze digest re-pin are rejected.
- **[OBSERVATION] Ten single-point mutants: 7 killed, 3 survived, 0 inconclusive.** This is a mutation result for the five-fixture accept/reject detector below, not a claim of exhaustive coverage or a defect in the pristine gate.
- **[OBSERVATION] Restoration:** after every mutant the active gate returned to SHA-256 `8c836cfe246605487ddf413f7e0dbde1608b91c60e1e622e9ac2e1b297590f66`; all 50 restored-fixture runs matched their expected outcomes.
- **[OBSERVATION]** 105 gate invocations total: 5 baseline, 50 mutant, 50 restored. No REA, carrier/mutant modification, package installation, agent dispatch, lane Git write, or lane source edit was performed. The only lane write is this report. All started commands completed synchronously; no service or background process was started.

Axes exercised: byte integrity, touched-after-freeze history, frozen pin provenance, both pin groups, missing-path handling, failure aggregation, and exit-code integrity.

## Isolation and detector

Source: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/freeze-integrity.py` (70 lines; original SHA-256 above).

Active mutation copy: `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/freeze-integrity.py`.

Sandbox: `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone`, cloned from the lane and checked out at `1288285eed81395e6af7c279a173b117b2c2eaa3` before fixture construction. Creation commands completed with exit 0:

```text
timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone checkout -q -B ctl 1288285eed81395e6af7c279a173b117b2c2eaa3
```

Fixture commits used `git -c user.name=ctl -c user.email=ctl@local -c commit.gpgsign=false commit` in this clone only. Every Git invocation had `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed from its environment. Git was 2.56.0; Python was 3.14.8. No tools were installed or updated.

The unchanged detector command for every phase was:

```text
timeout 300 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/lab.py phase <phase-name>
```

Each phase invokes the following gate command once per fixture, substituting the full revision from the table below:

```text
timeout 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/freeze-integrity.py --root /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone --round 31 --rev <fixture-revision>
```

**Expected detector:** compare `(process exit, final summary status)` with the fixture oracle: a = `(0, CLEAN)`; b–e = `(1, FAIL)`. A mismatch kills a mutant only if pristine and restored phases pass. Pin counts and per-path diagnostic hashes are retained verbatim but are not independent kill criteria. Thus a survivor may have incorrect diagnostics while preserving all five accept/reject outcomes. All phase-wrapper commands exited 0; individual gate exits are reported below.

Exact expanded commands, complete stdout/stderr, UTC start/end, expectations, gate hashes, and misjudgment flags for all 105 runs are in `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/detector-evidence.txt` and the per-phase JSON artifacts. The pristine detector ran at `2026-10-23T04:33:35.705192Z`–`04:33:35.916566Z`; there was no baseline failure.

## Fixture commits and pristine outcomes

The freeze resolved to `35ba7c522dba55f9be27eb161d4254eacaa24330` throughout.

| Fixture | Full commit | Construction | Pristine exit/status | UTC start, 2026-10-23 |
|---|---|---|---|---|
| a | `b22f0fa8fe738dfd28ce3f006b203f6115207430` | Empty clean commit, parent = assigned tip | 0 / CLEAN | 04:33:35.705192Z |
| b | `14f17a184ba4a298e2344d539ba92fbc258390e5` | Parent a; first prediction's row-limit argument changed from 5 to 6 | 1 / FAIL | 04:33:35.748010Z |
| c | `93de8fb5003bc2209c551bbb61f256d2d681ff08` | Parent b; that argument restored from 6 to 5, in a separate commit | 1 / FAIL | 04:33:35.790208Z |
| d | `b24e2c6fad4143f47db432bbc52ccf12ed3f9bb3` | Parent a; pinned C1 instrument deleted | 1 / FAIL | 04:33:35.832057Z |
| e | `3a35da9fed72b28b0e1525083df8a939a4c546d8` | Parent a; same input edit as b, plus its digest re-pinned in claims.json | 1 / FAIL | 04:33:35.875877Z |

Input under test in the clone: `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone/corpus/evidence/round-31/c2/predictions.tsv`.

- Original and c SHA-256: `acac45e3a6f0b266af56028b86b999172586fef1cbb82b8afa050c2eaf0262f8`.
- b and e SHA-256: `8579b343b7793db15fffa34235e787efd5b8fdb03bf7a362407e8db22146a585`.
- The e digest was written into `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone/.ufo/waves/round-31/claims.json` before committing.
- Deleted instrument in d: `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone/tools/round-31/c1-sqlite-positive.py`, frozen SHA-256 `048020881b0a2732b870634101338161e086225a334d841bb6f35a723eb540a0`.

Exact pristine stdout summary lines, in fixture order:

```text
freeze-integrity: CLEAN pins=5 freeze=35ba7c522dba rev=b22f0fa8fe738dfd28ce3f006b203f6115207430
freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=14f17a184ba4a298e2344d539ba92fbc258390e5
freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=93de8fb5003bc2209c551bbb61f256d2d681ff08
freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=b24e2c6fad4143f47db432bbc52ccf12ed3f9bb3
freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=3a35da9fed72b28b0e1525083df8a939a4c546d8
```

Exact distinguishing pristine stdout excerpts (b, c, d, e respectively; each process exited 1):

```text
FAIL	corpus/evidence/round-31/c2/predictions.tsv	sha=8579b343b779	commits_after_freeze=14f17a18
FAIL	corpus/evidence/round-31/c2/predictions.tsv	sha=acac45e3a6f0	commits_after_freeze=93de8fb5,14f17a18
FAIL	tools/round-31/c1-sqlite-positive.py	sha=absent	commits_after_freeze=b24e2c6f
FAIL	corpus/evidence/round-31/c2/predictions.tsv	sha=8579b343b779	commits_after_freeze=3a35da9f
```

These show that c is not just another byte-mismatch fixture: its bytes equal the original, but both post-freeze commits remain visible.

## Single-point mutants and killed/survived table

Every mutant changes exactly one source line of the isolated active gate, relative to pristine. Each was run separately, restored, and the same five-fixture detector rerun before proceeding. Source line numbers below refer to the pristine gate.

Notation: `C0` = final summary CLEAN, exit 0; `F1` = FAIL, exit 1; `F0` = FAIL, exit 0. Bold entries misjudge the fixture. UTC is the first fixture invocation of that mutant, on 2026-10-23.

| Phase name / mutant | Single-point change | UTC start | a | b | c | d | e | Misjudged fixtures | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| m01-drop-touched | L58: remove `and not touched` | 04:34:00.698000Z | C0 | F1 | **C0** | F1 | F1 | c | killed |
| m02-pins-at-rev | L48: read claims at `a.rev`, not `freeze` | 04:34:30.937787Z | C0 | F1 | F1 | F1 | F1 | none | survived |
| m03-skip-frozen-inputs | L50: iterate only `("instruments",)` | 04:34:57.241782Z | C0 | **C0** | **C0** | F1 | **C0** | b, c, e | killed |
| m04-skip-instruments | L50: iterate only `("frozen_inputs",)` | 04:35:24.483785Z | C0 | F1 | F1 | **C0** | F1 | d | killed |
| m05-or-not-and | L58: replace `and` with `or` | 04:36:02.524192Z | C0 | F1 | **C0** | F1 | F1 | c | killed |
| m06-blobs-at-freeze | L54: read pinned blob at `freeze`, not `a.rev` | 04:36:28.887270Z | C0 | F1 | F1 | F1 | F1 | none | survived |
| m07-reversed-touch-range | L56: replace `freeze..rev` with `rev..freeze` | 04:36:58.918203Z | C0 | F1 | **C0** | F1 | F1 | c | killed |
| m08-reset-failure-count | L59: replace `bad += not ok` with `bad = not ok` | 04:37:31.386315Z | C0 | **C0** | **C0** | **C0** | **C0** | b, c, d, e | killed |
| m09-missing-uses-pin | L55: use `digest`, not `"absent"`, on failed blob read | 04:38:01.421129Z | C0 | F1 | F1 | F1 | F1 | none | survived |
| m10-fail-exits-zero | L64: return 0, not 1, on failure | 04:38:31.840724Z | C0 | **F0** | **F0** | **F0** | **F0** | b, c, d, e | killed |

Producing command for each row is the phase command above with that exact phase name. Verbatim representative stdout excerpts, in row order:

```text
m01 / c: freeze-integrity: CLEAN pins=5 freeze=35ba7c522dba rev=93de8fb5003bc2209c551bbb61f256d2d681ff08
m02 / e: freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=3a35da9fed72b28b0e1525083df8a939a4c546d8
m03 / b: freeze-integrity: CLEAN pins=3 freeze=35ba7c522dba rev=14f17a184ba4a298e2344d539ba92fbc258390e5
m04 / d: freeze-integrity: CLEAN pins=2 freeze=35ba7c522dba rev=b24e2c6fad4143f47db432bbc52ccf12ed3f9bb3
m05 / c: freeze-integrity: CLEAN pins=5 freeze=35ba7c522dba rev=93de8fb5003bc2209c551bbb61f256d2d681ff08
m06 / d: freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=b24e2c6fad4143f47db432bbc52ccf12ed3f9bb3
m07 / c: freeze-integrity: CLEAN pins=5 freeze=35ba7c522dba rev=93de8fb5003bc2209c551bbb61f256d2d681ff08
m08 / b: freeze-integrity: CLEAN pins=5 freeze=35ba7c522dba rev=14f17a184ba4a298e2344d539ba92fbc258390e5
m09 / d: freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=b24e2c6fad4143f47db432bbc52ccf12ed3f9bb3
m10 / b: freeze-integrity: FAIL pins=5 changed=1 freeze=35ba7c522dba rev=14f17a184ba4a298e2344d539ba92fbc258390e5
```

The `mNN / fixture:` labels above identify excerpts; the text beginning `freeze-integrity:` is the exact gate stdout line. Gate exit codes are in the table; importantly m10/b exited **0**, despite its FAIL summary.

### Survivor interpretation

- **[OBSERVATION] m02 survived even e.** It reads the changed digest from the later claims, but the input's post-freeze touching commit still causes rejection.
- **[OBSERVATION] m06 survived.** It reports frozen bytes instead of current/deleted bytes, but the history check still rejects b–e.
- **[OBSERVATION] m09 survived d.** It substitutes the correct pinned digest for the missing blob, but the deletion commit still causes rejection.
- **[INFERENCE]** These three are blind spots of this five-fixture decision detector: its rejection cases exercise the untouched-after-freeze condition at the same time as digest or absence checks. Their survival is not evidence that the mutated code is contract-correct and does not authorize removing either defense.
- **[UNKNOWN / not exercised]** Broader histories, merge simplification, malformed freezes, pin removal from later claims, missing freeze commits, and Git-command failures. No universal equivalence or exhaustive gate correctness is claimed.

## Mutation hashes and restoration evidence

All ten probes had pristine before-state and restored after-state SHA-256:

```text
8c836cfe246605487ddf413f7e0dbde1608b91c60e1e622e9ac2e1b297590f66
```

Each mutant's actual SHA-256 (same immediately before/after its detector run) is below. Every restored detector produced the baseline decision vector `C0 F1 F1 F1 F1`, and its before/after SHA-256 equaled the pristine value. First restoration started `2026-10-23T04:34:14.573735Z`; final restored phase metadata was recorded at `2026-10-23T04:38:45.163969Z`. Full timing and bytes are retained per phase.

| Mutant snapshot | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m01-drop-touched.py` | `03887ecc9ac6322209d8e7fceca7e26324480417cc99730f04f11bddcc470140` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m02-pins-at-rev.py` | `60e1c23c4103f15e92fec8f0154ed5d30ab448c62988602a0ff8ca7ab7684842` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m03-skip-frozen-inputs.py` | `0ec4b4a10ca3e825c868211473be1266ca06eef8b512dd16c5be1b4a89cc2cb0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m04-skip-instruments.py` | `c925f0786841a7b5ca6f0e56d910e01c2c94a1d06105899b4f092e975abfe8aa` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m05-or-not-and.py` | `ecdfd4a3914060c44b0e73af554c6173627bcd6a25bafbbb6a52decef787863e` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m06-blobs-at-freeze.py` | `4d61149f84ccee429e74e0904c58787a1a71e4894bdc64c11702cbfe6634b276` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m07-reversed-touch-range.py` | `b74d11fc610a08549b7b43342566ee2fffba9e585f304af802df7a3d97cbf8ea` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m08-reset-failure-count.py` | `e1e29a47da1fd9fb1531723fde708ba48343a8830e2b133b44f9958781b3bd0a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m09-missing-uses-pin.py` | `65ed9848669a3c6eb5658c98a4cf1df4dc725a765f20ab59f36e67dff2e255b0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/m10-fail-exits-zero.py` | `7fc7c22fcb11d9a2ab9df2c5e3917a4b91dea4e660ffb84dd9f673839de062a5` |

A final `timeout 30 sha256sum` command on the active copy and lane source returned the same pristine digest for both (exit 0; UTC recorded immediately after at `2026-10-23T04:39:13Z`). The lane source also had this hash at the initial measurement (`2026-10-23T04:29:55Z`). The intentionally dirty fixture *histories* remain preserved in the clone; the active gate itself is restored.

## Artifact inventory

The complete, per-file SHA-256 inventory—including every file of the sandbox clone, every mutant/restored source snapshot, and every phase JSON—is `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/artifact-sha256.tsv` (21,759 listed files; the manifest excludes itself). Its SHA-256 is `b0c82cb4da292d7b2fa41e4e73a183bb618f64aa769e518cae973054fa9a9db7`. This inventory is the exhaustive artifact list accompanying this report; central deliverables are also named directly here:

| Absolute artifact | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/freeze-integrity.py` | `8c836cfe246605487ddf413f7e0dbde1608b91c60e1e622e9ac2e1b297590f66` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/lab.py` | `8cd6910fe34e37a90252578767ebf801c1fa57f8c076aed18dd0ee86f95d9cdb` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/render-evidence.py` | `33b5842dc0e268094192d2ee25a0ac5e0af2ad032ef554553864a89da4a1d043` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/fixtures.json` | `993e2df23d358218daa838e7055e78ddcb7f88190c77a3e3d8f5cd29bb5da649` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/fixtures.bundle` | `2f0a920e33e7ea679c6532b429fdd31370e85c1e567c10d4a9f7ef78ac5d3999` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/commands.jsonl` | `516a539de3f631cf3addb33353cd2f2895e6a6ef6120d62cdcf8dfea47e783b0` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/detector-evidence.txt` | `3166a71eb7109abc22b3b9d53df74bddefe3e0057603429ceaa340311cfe1d5a` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/outcomes.tsv` | `02a09cca7d8ad00c6310afb24674725400ea3558e2abc53f9dffab56c8816365` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/summary.json` | `6c4d8ac4230ad4acc8ea923e245a17619898b4692273c325f6716fe5d6546fae` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/sources.tsv` | `8c7985b3be2578efd112d6d29f1a0de925e3d3aae33701dd2f3477f9ba6abced` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/baseline.json` | `3f6863e732686c71c1f1f68f20d618d439512ebd68706ce53f1577cdcb6cc057` |
| `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/results/restored-m10-fail-exits-zero.json` | `1bdd3eb1a7c7bf3f391779f8ce7011271f1a8a4d162b18f854c1cdbc4d362392` |

The fixture bundle preserves branches `ctl` (c, with b and a ancestors), `fixture-d`, and `fixture-e`. Its producing command was:

```text
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/clone bundle create /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/fixtures.bundle ctl fixture-d fixture-e
```

Exit 0; stdout/stderr empty; UTC completion receipt `2026-10-23T04:40:08Z`. Bundle restoration was not exercised.

Recorded-output renderer command:

```text
timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/render-evidence.py
```

Exit 0; exact first stdout line: `phases=21 gate_invocations=105 baseline_failures=0 restored_failures=0`. This renders saved results only; it does not rerun the gate.

## Primary-source receipts

Only ordinary local-file reads were used. Access date for all entries is **2026-10-23**; URLs, full-file SHA-256 values, and located quotes of at most 25 contiguous words are recorded in `/fast/scratch/hyaku/kaidoku-r31/seats/w2/MutFreezeIntegrity/sources.tsv`.

The central contract source is `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/freeze-integrity.py`, SHA-256 `8c836cfe246605487ddf413f7e0dbde1608b91c60e1e622e9ac2e1b297590f66`, lines 12–13: “and requires every pinned path at --rev to hash to that digest and to have no commit touching it in freeze..rev.”

**[INFERENCE, scoped verdict]** The specified five-fixture invariant holds for the pristine bytes tested. The detector kills seven plausible one-line regressions; its three survivors remain explicitly recorded coverage limitations, not changes to the freeze contract.
