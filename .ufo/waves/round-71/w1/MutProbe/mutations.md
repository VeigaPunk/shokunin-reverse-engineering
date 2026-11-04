# MutProbe — frozen counter attacks

Axes: coverage (C1), calibration (C2), operability (C3). Frozen instruments extracted from b827a8b5d54f2885ec9be7786389f356c59226ce; all five initially matched claims.json. All executions used those isolated copies, not the changing working tree. No installation, git mutation, or source repair performed.

Evidence in this directory: census-results.json, validate-results.json, mutant-l1-results.json, restoration.json; fixture registries in fixtures/; representative input receipts in receipts/. Nested scratch paths in results are historical run pointers, not evidence locations. Attack drivers retained as execution-source records, not standalone packages.

| Mutant/input | Expected detector | Observed output | Verdict |
|---|---|---|---|
| C3: seven cells, empty pinned | exit 1, NONCONFORMANT/pinned-empty | exit 1; pinned-empty | killed |
| C3: two rows, one path | exit 1, DUPLICATE | exit 1; DUPLICATE tools/a.py | killed |
| C3: absent path | exit 1, NONCONFORMANT/path-absent | exit 1; path-absent | killed |
| C3: marker typo | exit 2, unevaluable | exit 2; missing or duplicate registry markers | killed, loud |
| C3: no data rows | exit 2, unevaluable | exit 2; empty registry | killed, loud |
| C3: conformant two-row registry | exit 0 | exit 0, findings [] | positive control met |
| C3: empty owner cell | probe missing-owner detection | exit 0, findings [] | survived: nonempty owner is not checked |
| C3: novel nine-cell row | probe extra-cell acceptance | exit 0, findings []; multicell_rows 1, legacy_rows cells 9 | accepted under declared join grammar; not itself proof of claim failure |
| C1 validate: ten true arms, empty observations | exit 1 | exit 1; A1..A10 each no observation | killed |
| C1 validate: arms_passed contradicts rows | exit 1 | exit 1; arms_passed disagrees with the arm rows | killed |
| C1 validate: failed contradicts rows | exit 1 | exit 1; failed disagrees with the arm rows | killed |
| C1 validate: ten fabricated observations {x:1} | probe evidentiary validity | exit 0, defects [] | survived: structural validator does not authenticate observations |
| C1 validate: fabricated arm ID | probe inventory enforcement | exit 0, defects [] | survived: inventory not checked |
| C1 validate: ten duplicate A1 IDs | probe uniqueness enforcement | exit 0, defects [] | survived: uniqueness not checked |
| C1 validate: broken JSON | exit 2 | exit 2, JSON decode unevaluable | killed, loud |
| C1 validate: empty arms | exit 1 | exit 1, arms absent or empty | killed |
| C1 bind_producer: matching identity | no defects | defects [] | positive control met |
| C1 bind_producer: transplanted round-70 identity | named rejection | path, sha256, rev mismatch defects | killed |
| C2 validate: six lying rows rc (0,0) | exit 1 | exit 1; six lying rc pair not (0,1) defects | killed |
| C2 validate: five lying rows | exit 1 | exit 1; lying_shapes present but not six rows | killed |
| C2 validate: genuine missing | exit 1 | exit 1; genuine arm absent | killed |
| C2 validate: base shapes clause_found false, rc (0,1) | probe named-clause enforcement | exit 0, defects [] | survived: named clause unchecked for base shapes |
| C2 validate: lying clause_found false, rc (0,1) | exit 1 | exit 1; six clause not found defects | killed; establishes asymmetry with base shapes |
| C2 validate: base shapes rc (0,0) | exit 1 | exit 1; ten rc pair defects | killed |
| M-L1: drop unpacked_counts clause from superseded reader copy | battery L1 acceptance must flip from true to false | first cut rc 0/met true; pristine superseded rc 1 naming unpacked_counts; mutant rc 0/met true; L1 row true -> false | killed by the L1 row predicate |
| M-L1 restored exact bytes | same reader detector as pristine | rc 1, same unpacked_counts rejection; exact_restoration true | restoration confirmed |

## M-L1 method and restoration

Removed only the unpacked_counts comparison/append block (superseded reader lines 509–511), replacing it with a mutant-identifying comment. Forged L1 through the frozen battery's write_lying_shape(), then executed its actual first-cut and superseded-reader commands. The bounded detector was the L1 row condition in check(): first_cut_rc=0, first_cut_met=true, superseded_rc=1, declared clause present. This is a bounded replay of that real row, **not a full check() battery invocation**. Baseline row passed; mutated row failed; restoring the same reader path to exact original bytes restored the original rejection. Thus this was not a baseline-failure/inconclusive kill.

Hashes:
- First-cut reader: 1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880.
- Superseded pristine and restored: 417b116803fbf78b44220d4a2caeb30d1261030353bc1b1c81d22c3b0146048a.
- Mutant: 9772614588eadf65497275de0da42b141ab0b2efe1a645ed6b3f44ce2e6ae001.

## Scope of surviving inputs

Survivors are coverage findings, not permission to change the contract. Seam --validate promises structural honesty; filler observations and wrong IDs pass it, so it cannot independently prove C1. Battery --validate does not require lying_shapes at all, and does not inspect base-shape clause_found (the actual check() does require named clauses). The empty-owner census input passes its explicitly declared grammar, which requires an existing backticked path and nonempty pinned value, not nonempty owner. The novel nine-cell input is surfaced in legacy_rows/multicell_rows but not rejected. These results do not establish that actual measured claim receipts are false.

## Concurrent tree drift observation

At extraction, live forged-receipts.py matched its frozen pin 50bb190b3c0b91870bfcce74c9898167f961102c8381d1a2b0c70fe7df115c7f. At final source hashing its working-tree hash was 44b973f1edad28ed409fcd41f487c75e804d06ee6d24e3d7699e50c121cac1d5; read-only git status reported it modified and diffstat was 7 insertions/6 deletions. Other four round-71 tools and the round-70 reader remained at their pins. I did not change these files; all results above used freeze-extracted copies. L1 must reconcile the observed working-tree edit with the frozen kill rule/disclosure process; this report neither reverts nor integrates sibling work.

VERDICT: assigned negative controls met and M-L1 killed/restored; structural-validator/owner coverage gaps named; concurrent pinned-instrument tree drift requires L1 reconciliation.
