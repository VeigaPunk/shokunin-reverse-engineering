# C2EntryOverreach — overreach attack on the R25-C2 entry's decision rule

Target: `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` at lane tip 08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76.
Seat: KaidokuR25a3.C2EntryOverreach (critic, read-only on the lane). Scratch: /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2EntryOverreach/.
Overall: the counts reproduce exactly. The decision rule and its "0 wrong" framing overreach. Every defect below can be fixed by rewording; none needs new data.

## Baseline (observation)
- `python3 -I -B tools/round-25/a3/tally-resolution.py --root <lane> --out <scratch>/analyze` exited 0 at 2026-10-22T10:43:19Z. Its `tally.json` and all six `<carrier>.json` files are byte-equal (`cmp`) to `corpus/evidence/round-25/a3/c2/analyze/`.
- Every probe below runs offline on those saved outputs with the lane's own resolver and `rule_outputs`. Each exited 0.

## Ranked overclaims

1. **"0 wrong" is a score on the same data the rule was picked from, presented as reliability.** Verdict: fails.
   - Observation: the tally scores five rules on the same 69 rows. The entry adopts the one with 0 wrong. The rule, `tally-resolution.py` and the entry were all added in one commit, 08c7a729 (2026-10-22T09:31:23Z, `git log --diff-filter=A`). `.ufo/waves/round-25/a2/claims.json` freezes only the counter, not a rule. Inference: the rule was chosen after its score was seen.
   - Observation: 49 named rows are only 31 distinct selectors. The other 18 rows reuse the same saved lookup, so they are not independent trials. `contest.py` prints `0 wrong of 31: 0.0921` and `0 wrong of 49: 0.0593` (one-sided 95% upper bounds), and those bounds hold only within this sample.
   - Observation: the rule had no choice to make for 21 of the 31: `sole openchain candidate (no choice): 21; with competitors: 10`. More than one unfiltered candidate existed only once: `['d0e30db0']`. The precondition for a wrong name (truth absent from both databases, some candidate present) occurred once: `[('6e8efde2', 'fee_quote(uint256)')]`.
   - Fix (rule 2): "On these six carriers the rule named 31 of 43 distinct selectors (49 of 69 rows) and none was wrong. The rule was chosen on this same data. Only two selectors exercised its checks: one choice between unfiltered candidates and one wrong sole candidate rejected. The result bounds nothing outside this sample; with 0 of 31 the 95% upper bound is 9%, even in-sample."

2. **The parameter-list check is presented as the safeguard, but REA's arguments were often wrong. On wrong-argument rows only the `filtered` flag stood between the rule and a wrong name.** Verdict: fails.
   - Observation: `probe.py` prints `REA inferred_arguments != ABI params: 12 of 69 rows`. Eleven are on the two Vyper carriers, where `address` was inferred as `uint256` (stewardtoken 8 of 22 rows, carrierv 3 of 15). One is solc: carrierb `note(bytes32,uint256)` was inferred as `uint256,uint256`.
   - Observation: the check rejected the true name on 9 rows (approve, transferFrom, mint, balanceOf, transfer and allowance on stewardtoken; is_owner, balances and balance_of on carrierv). It rejected a wrong name on 1 row (0x6e8efde2).
   - Observation (mutation, `flip.py`, 2026-10-22T10:45:44Z, exit 0): a scratch copy of stewardtoken's lookups had `filtered=false` set on the one junk match. Output: `flipped: ... rea_args=uint256,uint256 abi=transfer(address,uint256) leading_candidate=workMyDirefulOwner(uint256,uint256) right=False`. Saved data gives `leading_candidate=None`. One flag bit separates the sample from a wrong "leading candidate" on the most common selector there is.
   - Fix: in error pattern 3 and the rule, replace "the parameter-list check is what caught it" with: "REA's argument types were wrong on 12 of 69 rows (11 of them on the two Vyper carriers, address read as uint256). There the check rejected the true name 9 times and a wrong name once. When REA's arguments are wrong, only openchain's `filtered` flag prevents a wrong name. Add to rule 2: the label requires that REA's argument types are not known to be unreliable for the compiler (for example Vyper address parameters)."

3. **Selection bias: every name the rule found is an old, common public name, so the sample barely tests the case that fails.** Verdict: fails (the Limits section understates it).
   - Observation: `created.py` lists 4byte `created_at` for every ABI-true text present. The newest is `is_owner(address) ... created_at=2022-04-22`; most date from 2016 to 2018. All 31 rule-named names are generic identifiers (totalSupply, owner, pause, deposit, fund, tag, rate, ...).
   - Observation: no sign of lane contamination. No ABI-true text was added during the lane's lifetime.
   - Observation: the carrier description is wrong. "one Vyper token" should be two Vyper carriers: stewardtoken (`EX-03/token.vy`) and carrierv (`EX-04/src/CarrierV.vy`, built by `compile-carrier.sh` with vyper), plus four solc carriers.
   - Inference: on deployed contracts the error rate is driven by how often the true name is absent while a collider is present. Here that happened on 1 of 43 selectors, so the sample says almost nothing about it.
   - Fix (Limits): "All 31 named selectors carry common names that 4byte had recorded since 2016–2022. The truth was absent while a candidate was present on 1 of 43 selectors, so the rule's behaviour when a contract uses an unpublished name is essentially unmeasured." Fix the inputs line to "four solc carriers and two Vyper carriers".

4. **"Leading candidate" is evaluative wording that the evidence does not earn.** Verdict: fails, but a wording fix is safe.
   - Inference: "leading" implies a ranking or likelihood. The rule is a uniqueness filter on one database snapshot, and its checks were exercised twice (items 1 and 2). Readers will treat a "leading candidate" as probably right, including on Vyper bytecode, where the mutation shows it can be junk.
   - Fix: use a descriptive label instead, such as "sole unfiltered argument-consistent openchain candidate (snapshot <UTC>)". Always print it with rule 1's full candidate list and with REA's argument types marked as inferred. If an evaluative word is kept, add "not a likelihood; untested on contracts with unpublished names".

5. **The error patterns are incomplete. They omit junk that passes the `filtered` flag, the systematic Vyper argument error, and a flag that does not discriminate.** Verdict: fails (not representative).
   - Observation: `contest.py` prints `unfiltered openchain candidates 40, of which not the ABI name 4`: OwnerTransferV7b711143(uint256), cat642998653(address,uint256), hasStreamed(address) and X19B3C29E(string). So `filtered=false` is not a junk-free label (4 of 40 distinct).
   - Observation: the entry shows the Vyper argument error as one row. It is 11 rows across two carriers (item 2).
   - Observation: `probe.py` prints `(hasVerifiedContract, is_truth) ... (True, False): 92`. The flag is true on 92 wrong candidates and on all 61 right ones, so rule 1's "with its flags" invites misreading it as verification.
   - Fix: add patterns "unfiltered junk next to the true name (4 of 40 distinct unfiltered candidates)" and "systematic Vyper address-as-uint256 inference". Add to rule 1: "`hasVerifiedContract` was true on 92 wrong candidates here; it does not verify a name."

6. **Headline counts are per-carrier rows, which inflates the rates through repeated ERC-20 selectors.** Verdict: fails mildly; the direction still holds.
   - Observation (`tally.json` `distinct_selectors`): first 4byte result is 12 wrong of 34 named, against the per-row 26 of 59. The openchain rule is 31 of 31 right, against 49 of 49. The 4byte parameter rule is 0 wrong of 29 distinct, against 1 wrong of 48 per row.
   - Fix: lead the table and rules 2 and 3 with distinct-selector counts and give rows second. Example for rule 3: "12 of its 34 distinct-selector names (26 of 59 rows) were wrong."

7. **The compiler ABI as ground truth.** Verdict: holds.
   - Observation: `probe.py` prints `ABI functions REA did not recover: {... all []}` and `rows with no ABI truth: []`. REA's selector set equals the ABI's set on all six carriers.
   - Observation (script text, not a run): `compile-carrier.sh` writes abi.json and runtime.hex from one vyper invocation.
   - The ABI is the right truth for "the source's function name". Its limit is the lane-chosen names, which is item 3, not a truth defect. Fix: none beyond the existing Limits line.

## Smallest safe correction
Reword rule 2 and drop the "0 wrong" reliability framing (items 1 and 4). Add the Vyper argument and `filtered`-only caveats (item 2). Correct the carrier composition and the Limits text (item 3). Add the two missing error patterns and the `hasVerifiedContract` note (item 5). Lead with distinct-selector counts (item 6). All of these are fixable defects, not tradeoffs that would force rejecting the entry. Without items 1, 2 and 4, rule 2 claims a reliability that the evidence cannot support.

## Impacted axes
Coverage (R25-C2 entry content) and calibration (the entry's self-assessment of reliability). The C2 counter is unaffected because it checks presence and linkage only.

## Artifacts (sha256)
- probe.py d6368eb2231bb303f35878adffe991efb84ab309b02fff4c7edf9bec1ee8b6b3; probe-out.txt 71a6e63e2311b6ee75c9d2b71e72c4407c01d55416aa287ec79a8f7cbafa45c6
- created.py c0d11ed04f84d73ba9ac0962b58b0ba5bc4a077edeedf1a1bfc4f44f679ef19c; created-out.txt a45f09b7f30e4739f2c8aff9ed1dd84281f012c75aa8f35343d11538d969d939
- contest.py 4b32208b1e79a880522e77154edb2780254da4b59be07499be5dd6fc00cb228c; contest-out.txt 25dbe1e9088b3fe2690f6557b3fb7e50c22b8e04e3fcf8618ca740c3973c6e9f
- flip.py 5a2d28c9378b261840a6afbe0f5f9c78c24928538bec1d87809bcaae6fde8270; flip-out.txt 6b6951573ac8c9419eadb7ffe63456a29571858063c82f6bed5099bd38655a6a; flip-db/openchain-a9059cbb.json (mutated) 34856e98aad179258a1f957fabaf36bc28885fe60118e3c23f3f56307260b6b2
- tally-stdout.json 7e02dbbe048da684b217b5c535423db41938c41a9b4767d5f13359fb628ca2b7; analyze/tally.json 479bc13ea4c2139289808a54c47321c83c3daafffaad5de4b06c00ac840b40dc

## Not done
No REA run, no web lookups, no source pages opened (none were needed for this attack). No tools installed or updated. No lane file edited except this report.
