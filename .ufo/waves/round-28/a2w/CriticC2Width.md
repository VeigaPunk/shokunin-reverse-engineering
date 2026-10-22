# CriticC2Width — R28-C2 statement versus its counter (round 28, attempt 2)

Attacked: the R28-C2 statement in `.ufo/waves/round-28/claims-c2.json` (frozen at 86fa8526) against `tools/round-28/c2-filtered-flag.py` (sha256 `4fdf7db8…60ef`, equal on disk and at a2673116), plus the assumption that api.openchain.xyz runs Sourcify commit 189cd726.

Verdict: **holds narrowly, with two fixable defects.** The counter checks the per-entry rule both ways, and the data agree: 0 mismatches. But the result cannot tell Sourcify revision 189cd726 apart from any earlier revision. The canonical branch rests on 10 ERC-20 and Ownable keys that were already seen before the freeze. One sentence in the Limits wording fails against a concrete counterexample. The `entry_ok` check accepts an unrelated source row.

## Runs (all exit codes observed, UTC)
| command | UTC | exit | excerpt |
|---|---|---|---|
| `python3 -I -B tools/round-28/c2-filtered-flag.py --root <lane> --rev a2673116` | 18:23:15Z | 1 | `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=0`, `FAIL entry absent` |
| same counter, `--selftest` | 18:23:15Z | 0 | `selftest cases=17 failures=0` |
| same counter, `--rev 9db24c9e` (lane tip) | 18:25:49Z | 0 | `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59 entry_ok=1` |
| `python3 -I -B profile.py <lane> a2673116` (scratch) | 18:23:52Z | 0 | `r28-heldout selectors 187 canonical_keys 0 entries 147 ... filtered_true 0`; `rival canon key and not first in list  mismatches 0` |
| sandbox clone at 9db24c9e, entry `source:` line replaced by `source: S086 Solidity docs library linking placeholders`, committed, counter `--rev HEAD` | 18:26:00Z | 0 | `... entry_ok=1` |
| `gh api repos/argotorg/sourcify/compare/189cd726…master` | 18:24:26Z | 0 | `identical ahead=0 behind=0` |

## Phrase table
| statement phrase | counter code | status |
|---|---|---|
| "each of the 230 selectors in selectors.tsv" | `pinned()` sha pin, `TARGET 230` | checked |
| "(round 25's 43 and round 28's 187 held-out)" | not read (set column ignored) | unchecked by counter. I checked it by hand: 43 r25 and 187 r28-heldout rows, and the 187 equal c1/heldout.tsv (comm diff 0 lines). Observation |
| "one openchain filter=false response" | manifest `url == URL % s`, status 200, ok=true, key present | checked from the manifest only. No headers or host evidence are saved (`collect-c2.py` manifest keys: file, sha256, status, url, utc) |
| "fetched after this freeze" | manifest `utc` > counter first-commit time; file added no earlier | checked against the collector's own `utc` field. The real fetch instant is unknown |
| "is committed" | `git show REV:path`, sha equal | checked |
| "on every candidate entry" | loop over `items` | checked |
| "filtered is true exactly when key of pinned json and name differs" | `pred = c is not None and name != signature`; `filtered is not pred` counts as a mismatch | checked in both directions; non-boolean flags count as mismatches |
| "pinned canonical-signatures.json" = Sourcify's file at 189cd726 | local sha pin only | unchecked by counter. I fetched the raw file at 18:23:55Z and got sha256 `5572beb5…b3e2`, equal to the pin. Observation |
| rule "read from handlers.ts filterResponse" | rule hard-coded, handlers.ts not pinned | unchecked by counter. In the opened bytes (sha256 `30981efb…5a38`) `:47-48` read `signatureItem.filtered =` / `signatureItem.name !== expectedCanonical.signature;`. Observation |
| "(mismatches 0)" | `mism == 0` | checked |
| "with both branches present (predicted_true >= 1)" | `ptrue >= 1` only | half checked: nothing requires a predicted-false entry (lines 207-209). On these data 187 entries are predicted false, so the result is unaffected |
| "knowledge entry states 'mismatches M of N entries'" | phrase with recomputed values | checked |
| "cites a SOURCES row new since the base, opened, mined, in ## Gate" | any S### on line 1 that passes those tests | checked as written, but too wide: the S086-only mutation passes (exit 0). The counter does not tie the row to the filter code |
| kind: "rule at commit 189cd726 predicts the live flag" | none | unchecked (see the deployment attack below) |

## Attack: does api.openchain.xyz run 189cd726?
- Observation: 189cd726 is the `master` head, "Deploy latest to production (#3036)", committed 2026-10-21T12:56:36Z. S078's saved page (sha256 `9b5c4f9e…5b21`, line 54) reads "We implemented the exact openchain API and now Sourcify serves all signature requests to openchain.xyz as well." Neither shows which revision answered at 17:22Z.
- Observation: `filterResponse` has hashed the same (`c9fc3d89…`) at every handlers.ts revision from d5a8f035 (2025-10-16) to 189cd726. The two older revisions differ only in how they handle null responses and how they loop over types; none of the 10 canonical selectors returned null. canonical-signatures.json changed once after creation: commit 56c6b336 (2025-10-29) added `0x09b81346`, which is not among the 230 selectors (`rg -c` found 0).
- Inference: every Sourcify 4byte revision since the service was created (5fc5ebc3, 2025-10-08) predicts the same 246 flags. The test is blind to which revision is deployed. "At commit 189cd726" names a revision the data cannot confirm or refute.
- **Fails:** the claim's `limits` and the entry's Limits both say a different deployed list "shows as mismatches". Counterexample: the 35-key list at 5fc5ebc3, or any list that differs only on the 26 canonical keys outside the 230 selectors, gives exactly the same 0 mismatches.
- Unknown: whether a service other than Sourcify, with the same canonical-name semantics, answered. No response headers were captured.

## What a 0-mismatch result does not show
1. Which code revision is deployed (see above). Only "some service whose flags agree on these 230 selectors".
2. Anything about the canonical branch on held-out data. 0 of the 187 held-out selectors are canonical keys, so for all 147 held-out entries the rule only predicts `false`. That equals the constructor default (`filtered: false` at handlers.ts `:90`, `:262`); "always false" also scores 0 mismatches on them.
3. A fresh risk on the true branch. All 10 canonical keys (all 59 predicted-true entries) are round-25 selectors, and the pre-freeze probe had already scored them at 0 mismatches. The fresh fetch re-observes known selectors.
4. Coverage of the canonical list. Only 10 of 36 keys were tested, and they are 9 `standard:erc20` plus 1 `standard:ownable`. None of the uniswap, seaport, `system:magic`, proxy, 0x, 1inch or other families was tested.
5. That the flag depends on the name rather than on list position. The canonical name was the first candidate in all 10 canonical lists. "Canonical key and not first in the list" also gives 0 mismatches (rival-rule run).
6. Edge cases: a canonical key whose canonical name is missing (all candidates filtered), a canonical key with a null answer, or `filter=true` behaviour. None was fetched.
7. Stability over time or hosts: one fetch window (17:22:05Z to 17:25:57Z) from one host. `hasVerifiedContract` and result order are not covered, as the claim says.
8. That the bytes came from api.openchain.xyz, beyond the collector's manifest `url` field.

## Impacted axes
Depth (the learning claim is narrower than "the code predicts the live flag"). Provenance (the revision is attributed but not shown). Honesty of the Limits wording.

## Smallest safe correction
- Entry Limits (lane tip, `corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`): replace "A different deployed list would show up as mismatches, and none did on these 246 entries." with "A deployed list that differs only on keys outside these 230 selectors, or any Sourcify revision since 5fc5ebc3, gives the same result; the test does not identify the deployed revision." Add: "The 59 true predictions come from 10 round-25 ERC-20 and Ownable keys already probed before the freeze, and the canonical name was first in each list, so list position fits the data equally well."
- The frozen claim `limits` sentence has the same flaw. Report it in the round-28 lesson; do not edit the frozen file.
- Next counter (the frozen one stays unchanged): require S084 or S085 on the `source:` line, and require `entries - predicted_true >= 1`.

## Artifacts (/fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticC2Width/)
| file | sha256 |
|---|---|
| profile.py | 1a9291ff987bfee410f5ea539c9c22b34bc98bb724046f915be05a7be130cb30 |
| profile-a2673116.txt | 317aa091b17ea9dd7567d43495deb9212ddb1998bbe5ab1789fcedd6620d3631 |
| counter-a2673116.txt | a018cb84dd9217a22fe6e3554deadbf10ae0b55b71ef1df3cbb92fde22a64476 |
| counter-tip.txt | 5b7ac8512d038215dff2d89df00dd86e59814c436a331e255834632b5387cb31 |
| mut-s086.txt | 5b7ac8512d038215dff2d89df00dd86e59814c436a331e255834632b5387cb31 |
| selftest.txt | d6dd57b1a59bf465321d19b9852a5090a774e5d0ab0c1e39cf16a3051f0f12fb |
| handlers-189cd726….ts | 30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38 |
| canon-189cd726….json | 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2 |
| readme-4byte.md (line 5: "The API is backwards compatible with the openchain.xyz API.") | f73b1651d96107f9baa92d4f59f2acee2cd703b3327fcdec7b15a3627c9157d8 |
| canon-history.txt | b771bf75b123eb5a67e7f5066f00a604df689924b70335a9528eab237b3edfa6 |
| handlers-history.txt | 1322a93c92812e35b0c515035c3fcddd7825388c7796d5fa570f15adbc68b37f |
| master-head.txt | 48db252a473843114ea7d6ded672a95e508f1af721a726c56bc7b388df9b4235 |
| hist/ (seven older handlers.ts and the 5fc5ebc3 canonical list), hashes in hist-sha.txt | 76c0af2cd24b7f84ff792517e429828252c4f600ff633f6f0ccdea17b1cb84cc |
| clone/ (sandbox, one mutation commit) | n/a |

Sources opened 2026-10-22 over plain HTTPS or the GitHub API: the raw.githubusercontent.com files above at their commits. I made no requests to openchain or 4byte.directory and ran no REA. Installs: none.
