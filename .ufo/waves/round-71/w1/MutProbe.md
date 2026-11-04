# MutProbe — round 71 w1

Axes: coverage / calibration / operability. Tested frozen b827a8b5 bytes, extracted independently from git; no source changes or tool installations.

Full table and evidence: [MutProbe/mutations.md](MutProbe/mutations.md).

- Registry: five assigned negative registries rejected (exits 1/1/1/2/2); clean registry accepted (0). Empty-owner row accepted; nine-cell row accepted but surfaced as multicell/legacy. These are grammar/coverage observations, not an invented stronger contract.
- Seam validate: empty observations, arms_passed contradiction, failed-list contradiction rejected (all exit 1). Filler observations, fabricated arm ID, duplicate IDs accepted (0): structural validation alone cannot establish the claim. Matching producer identity accepted; transplanted identity rejected with path/hash/revision defects.
- Forged battery validate: six (0,0) lying rows, five lying rows, missing genuine block rejected (all 1). Ten base shapes with clause_found=false accepted (0), whereas lying rows with that flag false rejected (1). This asymmetry is a validator coverage finding; actual check() requires the named clauses.
- M-L1: dropped unpacked_counts clause in an isolated superseded-reader copy. The frozen battery's actual L1 row commands and predicate were replayed, not the entire battery. First-cut accepts (0); pristine superseded rejects with unpacked_counts (1); weakened reader accepts (0), so the L1 row fails and detects the weakened reader. Exact-byte restoration reran the same reader detector and restored rc 1 plus the same clause. Pristine/restored SHA256 417b116803fbf78b44220d4a2caeb30d1261030353bc1b1c81d22c3b0146048a; mutant 9772614588eadf65497275de0da42b141ab0b2efe1a645ed6b3f44ce2e6ae001. Evidence: MutProbe/mutant-l1-results.json and MutProbe/restoration.json.

Concurrent observation: live tools/round-71/forged-receipts.py changed from pinned 50bb190b... to 44b973f1... during this probe; read-only status reported a working-tree modification, 7 insertions/6 deletions. No claim is made about its author or disclosure. All tests here used frozen copies; L1 must reconcile this with the freeze kill rule before integration. Other four round-71 tool hashes and round-70 reader remained pinned.

All evidence retained in MutProbe/; scratch provenance paths inside receipts are historical run pointers, not evidence. Scratch removed after copying evidence. No installs; no git mutations. No full runtime seam/battery run claimed.

VERDICT: assigned counter negatives met; weakened-reader M-L1 killed with exact restoration; false-green coverage surfaces and concurrent frozen-tool tree drift named.
