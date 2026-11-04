# CriticClaims — round 71 frozen predicates

Axes: coverage (C1), calibration (C2), operability (C3). Read the round-70 non-author spot-check first; its seven routed inputs are acknowledged, especially the six previously unreceipted lying fields. No instrument edits, git mutations, installations, or alternate judging runtime. All executed instrument copies came from `git show b827a8b5d54f2885ec9be7786389f356c59226ce:<path>`; their SHA256s are recorded in `shortcuts.json` and match the four relevant container pins. No full 10-arm or 18-row battery success is claimed here.

Evidence: `shortcuts.json` records exact CLI argv, exit, stdout and stderr for actual process tests; preserved forged inputs and registry fixtures are siblings. Scratch paths in argv identify historical runs, not surviving evidence.

## C1 — coverage

### Forged observation log: reachable arm, trust-boundary limitation and a containment defect

Shortest shortcut: write three JSONL records naming upx/node/readelf, assert exactly HOME/LANG/PATH/TMPDIR, and return the matching observed summary. The unmodified frozen A8 block evaluates true. The fixture used HOME/TMPDIR `run_root + '-outside/home|tmp'`, which are NOT descendants, but pass `startswith(run_root)`.

Method disclosure: this is execution of the unchanged A8 AST statements from the frozen probe with a counterfeit `invoke` process boundary; not the full probe CLI and not evidence that the frozen route actually forges logs. `shortcuts.json:C1.forged_A8_A9_boundary` records the resulting observations. The caller-supplied log path alone is not an exploit: the probe creates a fresh unpredictable a8 directory and passes its own log filename. The frozen launcher really appends environment records before exec. Thus fabrication requires control of the producer/process boundary or concurrent filesystem interference, not merely supplying an ordinary receipt.

Classification: **(b)** raw-log provenance is producer trust, not independent attestation; **(a)** textual prefix is not filesystem containment, contradicting the explicit “under its own root” condition. Smallest correction: use normalized `commonpath`/relative containment, consistently in route summaries and probe A8/A9. Test the sibling-prefix counterexample.

### Pre-created roots: reachable A9 expression, not a full-route collision exploit

Shortest shortcut: return three distinct pre-created battery paths and three distinct pre-created route roots with one fabricated env record each. Frozen A9 statements evaluate true, even when that record names only `invented-child`, has only HOME/TMPDIR, and points at sibling-prefix outside paths. Route log files are outside the reported roots (under the shared a9 parent), yet acceptance is true.

Method: unchanged A9 AST block, explicit fake Popen boundary; no alternate instrument bytes were run. Actual probe Popen calls start three batteries, then three routes concurrently; pre-creating arbitrary directories cannot redirect frozen route mkdtemp by itself.

Classification: pre-created identity alone **(b)**, not fresh-creation attestation; prefix containment **(a)** as above. The predicate says “each env log under its own root”, but A9 never checks log-path containment and itself chooses logs at the shared parent. That is a concrete **(a)** implementation/predicate mismatch. Smallest correction: create/write each log inside its returned run root and check that association, rather than accepting unrelated caller-owned logs. Do not claim six-way battery+route overlap: these are two separate concurrent batches.

### Published nonce and receipt transplantation: actual checker exit 0

Shortest shortcut: copy the genuine round-70 landing receipt, relabel revision/instrument to frozen round 71, add a 64-character nonce, invent a non-existent run_root and green observation summary, and compute `sha256(nonce + ':' + instrument_sha + ':' + ','.join(sorted(packed_pins)))`. Frozen `packed-elf.py --check-receipt ... --nonce-commitment sha256(nonce)` exits **0**, `met:true`, `failing:[]`; `run_root_exists:false`. Preserved input: `transplanted.json`.

Classification: **(a)** if “rejects a transplanted or altered receipt” means producer-authenticated new run evidence; **(b)** only for the narrower explicitly enumerated A10 tests (unchanged round-70 receipt, nonce flip without recomputation, broken binding). A10 does not bind run_root, env observations, argv, counts, or revision into its digest. Even fields included in the digest can be rebound after the receipt publishes the nonce. An independently precommitted hash prevents choosing a different nonce before disclosure; after the genuine receipt reveals that nonce, no secret prevents relabelling old evidence and recomputing the binding. This attack used a known demonstration nonce/commitment, not the lane's secret preimage; the same formula works with any disclosed genuine nonce. It is not a demonstrated full A1..A10 success without runtime execution.

Smallest safe correction: distinguish challenge consistency from authenticated run provenance in the claim; if provenance is required, retain a verifier-controlled run transcript/artifact association or authentication authority unavailable to the receipt fabricator. Adding another public hash alone does not provide it. This is an authority tradeoff, not grounds for a critic to admit or reject the claim.

## C2 — calibration

### Asserted reader exits: structural validator reachable, full predicate not bypassed

A fabricated receipt with six `(first_cut_rc:0, superseded_rc:1, clause_found:true)` rows, an invented base shape, and a nonempty invented genuine object passes frozen `forged-receipts.py --validate` with exit **0**. Input `asserted-battery.json`; exact invocation/output in `shortcuts.json:C2.asserted_validate`.

Classification **(b)**: validator describes structural honesty, not subprocess provenance. The actual frozen counting path cannot obtain its six exits by assertion: lines 343–358 extract and execute both committed readers for every shape. It checks rc and parsed first-cut `met`, plus named superseded failure. Treating --validate as equivalent to the frozen counting command would be a separate false-authority error.

### Unrelated-clause rejection shortcut: not reproduced

Executed all six frozen `forge_lying` outputs against actual first-cut and superseded reader blobs, with `--rev` set to the first-cut world in BOTH commands. Every first-cut exit **0**; every superseded exit **1**. Failures are exclusively the requested changed fields:

- L1: `unpacked_counts != orig_counts`;
- L2: `packed_sha256 != declared`;
- L3: `section_count != 0` and `upx_list_rc != 0`;
- L4: `runs.pack.argv ... lacks --best`;
- L5: `refusal.packed_rc 0`;
- L6: `format != readelf of the pinned source`.

No instrument/revision mismatch masks these six local tests. Classification **(c)**: no counterexample to C2's six reader comparisons. This is not a rerun of the whole 18-row battery; unchanged surrounding arms remain other seats' evidence. Smallest correction: none for the six comparisons; preserve distinction between structural validation and counted execution.

## C3 — operability

### New malformed multicell row accepted: actual CLI exit 0

Fixture `new-eight-cell-SKILL.md` contains a fabricated registry with one existing dummy `tools/a.py` and eight cells: `tool,purpose,verdict,selftest,pin,surplus,write,owner`. Frozen census `--root <fixture> --rev WORKTREE` exits **0**, rows=paths=1, nonconformant=[], duplicates=[], multicell_rows=1. The row is NOT one of the four filed round-69 exceptions.

Classification **(a)**: contradicts the frozen kill rule “a new malformed row (not one of the four filed multicell rows) accepted”. Parser unconditionally joins every row's surplus cells. Smallest correction: scope bare-pipe joining to the four exact filed historical row identities (preferably frozen row bytes), rejecting new non-seven-cell rows; keep escaped pipes as ordinary seven-cell rows. Add this precise negative test. If arbitrary multicell grammar is intentional, that is a claim/kill-rule tradeoff, not permission to silently broaden the contract.

### Empty owner and fabricated block: actual CLI exit 0

`empty-owner-SKILL.md` has seven cells, nonempty pinned value and empty owner; accepted **0**. A fully fabricated one-row good-looking block is also accepted **0**. Classification **(b)** under the declared grammar: conformance only requires path existence and nonempty pinned, not semantic correctness, complete registry inventory, owner truth, or executable tool content. These are not demonstrations that the entire frozen C3 predicate is met: it additionally names the four historical rows and six repaired round-70 rows. Smallest correction: name the grammar-only limit; do not describe this as completeness or semantic validation. If owner completeness is required independently, make it a tested clause.

### Empty pinned / absent path / duplicate: rejected

Actual frozen CLI exits: seven-cell empty pinned **1** (`pinned-empty`), absent registered path **1** (`path-absent`), duplicate tool path **1** (`DUPLICATE`). Classification **(c)**. Exact commands and JSON findings are preserved.

## Integration boundary

No target is honestly shown fully met without its work: C1's runtime full command was not bypassed, C2's frozen counting path executes real readers, and fabricated C3 inventories do not satisfy the claim's named historical rows. However, the C1 provenance wording exceeds its public digest, A8/A9 containment is false-green for sibling prefixes, A9 log-under-root is not implemented, and C3 accepts new malformed multicell rows despite its kill rule. These are concrete correction candidates, not an admission decision.

VERDICT: defects named — C1 A8/A9 containment and log association plus public-nonce provenance limit; C3 new malformed multicell acceptance; C2 six reader comparisons resisted the shortcut.
