source: S084 Sourcify 4byte service filterResponse code (commit 189cd726); S085 Sourcify canonical-signatures.json (same commit); S078 Sourcify 2025 Recap (openchain lookups answered by Sourcify); S076 Sourcify 4byte OpenAPI (`filter` parameter)
verified-at: 2026-10-22, round 28 (R28-C2); 230 openchain `filter=false` responses fetched 2026-10-22T17:22:05Z–17:25:57Z, after the counter froze at lane commit 86fa8526 (17:21:55Z); manifest with sha256 per response in `corpus/evidence/round-28/c2/db/manifest.json`
recheck: python3 -I -B tools/round-28/c2-filtered-flag.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> (offline over committed bytes; expected `responses_complete=230/230 entries=246 mismatches=0 predicted_true=59`)

# openchain's `filtered` flag marks only non-canonical names of 36 canonical selectors

The round-25 naming rules (`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`)
use openchain's `filtered` flag as a filter step, but the round-25 entry only observed the flag.
It did not say what sets it. This entry states the rule from the service's own code and tests it
on fresh responses.

## Rule (code, S084 + S085)

At Sourcify commit `189cd726f7ed8fb3d2f503402d5c133e0f50e1fd`, `services/4byte/src/api/handlers.ts`
`filterResponse` (`:39-66`) loops over every selector in a lookup result. When the selector is a
key of `services/4byte/src/utils/canonical-signatures.json` (36 keys, S085), it sets each
candidate's `filtered` to `name !== canonical signature` (`:47-48`). It never touches any other
selector, so those candidates keep the `filtered: false` they were built with. With `filter=true`,
the service then drops the candidates marked `filtered`.

So `filtered` is not a spam score. It is true exactly when the selector is one of the 36 canonical
keys and the candidate's name differs from that key's kept signature. Five of the 36 keys
(`0x60806040`, `0x60a06040`, `0x60c06040`, `0x60e06040`, `0x61010060`, source `system:magic`) have
no `signature` field, so every candidate for them is marked (seat `SourceFilterCode`). None of
them is among the tested selectors.

## Test (R28-C2, live service, one fetch instant)

- Selectors: 230 (`corpus/evidence/round-28/c2/selectors.tsv`): the 43 round-25 selectors plus
  the 187 round-28 held-out selectors. Of these, 10 are canonical keys, all from round 25. None of
  the 187 held-out selectors is a canonical key.
- Responses: 230 of 230 committed (`corpus/evidence/round-28/c2/db/`). 48 have no candidate.
- Candidate entries: 246, of which 69 belong to the 10 canonical selectors.
- Result: **mismatches 0 of 246 entries**. The code rule predicts the live flag on every entry.
  It predicts `filtered: true` for 59 entries, and all 59 are true in the responses
  (predicted_true 59). The other 187 entries are predicted false, and all are false. Of those,
  10 are the canonical names themselves and 177 belong to non-canonical selectors.
- Counter: `tools/round-28/c2-filtered-flag.py` (sha256 `4fdf7db8…60ef`, frozen in
  `.ufo/waves/round-28/claims-c2.json`, 17 selftest cases), and its pinned inputs.

## What this means for the round-25 rules
- On a non-canonical selector, `filtered` is always false, so `openchain_sole_unfiltered` names
  exactly what "the only openchain candidate" would name. The filter step only acts on the 36
  canonical selectors. The 59 flagged entries sit there; one example is
  `__$$____$_$___$_$_$_$_$__$$___()` under `0x06fdde03` `name()`.
- A selector with two or more real-looking candidates that is not on the list stays ambiguous.
  The flag does not resolve it.
- On the round-28 held-out rows the filter step therefore changed nothing. The difference between
  `openchain_first` (named 145) and the primary rule (named 137) comes from the sole-candidate and
  argument checks (`corpus/evidence/round-28/c1/tally.json`).

## Limits

- The test does not identify the deployed revision. The service behind `api.openchain.xyz` is
  assumed, not shown, to run this commit. The frozen claim's `limits` say that a different deployed
  list "would show up as mismatches". That is wrong. The seat `CriticC2Width` found that the 35-key
  list at the service's first commit `5fc5ebc3` also gives 0 mismatches here, and so does any list
  that differs only on the 26 keys outside these selectors.
- One fetch instant, one host. The test covers only the 10 canonical keys among these selectors (9
  ERC-20 selectors and `owner()`), not all 36. In all 10 responses the canonical name was listed
  first, so "canonical key and not first in the list" fits the data equally well
  (`CriticC2Width`).
- Says nothing about result order or `hasVerifiedContract`.
- Pre-registration was weakened (seat `CriticC2PreFreeze`, `.ufo/waves/round-28/a2w/CriticC2PreFreeze.md`;
  mistake M28-4). Before the freeze (`86fa8526`, 17:21:55Z) the L1 ran this rule on the 69
  committed round-25 openchain responses (216 entries, 0 mismatches). The probe time recorded in
  `claims-c2.json`, "17:24Z", is later than the freeze commit, so it is wrong, and the true time
  is unknown. By then the L1 had also fetched 125 of the 187 held-out openchain `filter=false`
  responses for R28-C1. In all, 168 of the 230 test selectors already had a response in the lane
  before the freeze (`tools/round-28/preseen-overlap.py`, exit 1). The seat found that the fresh
  responses repeat those (name, filtered) pairs, and all 59 predicted-true entries come from the 10
  round-25 canonical selectors that were probed. So the test is a re-observation, at a second
  instant, of a rule read from code, not a held-out prediction. 26 of the 36 canonical keys stay
  untested. A held-out test would freeze a list built from those 26 keys before fetching anything.

## Use

- Read `filtered: true` as "not the canonical name for one of 36 well-known selectors". It is not
  a general spam verdict.
- Do not treat `filtered: false` as evidence that a name is right. For a non-canonical selector it
  is the default.
- When the canonical list changes (S085 recheck `on-release`), re-run the counter over a fresh
  fetch before relying on this entry.

## Pointer appended in round 29

Round 29 tested this rule on 178 selectors with no prior openchain response in the lane,
including the 26 canonical keys this entry did not fetch: mismatches 0 of 252 entries
(`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md`). It also found that 6 of the 31
kept signatures in the list do not hash to their own key (for example `0xc45a0155` keeps
`mint(address,int24,int24,uint128,bytes)`, which is `0x3c8a7d8d`), so under those keys every
candidate is filtered, the true name included. Read the title and the Use gloss above ("not the
canonical name") as "differs from the string the list keeps", which for those 6 keys belongs to
another selector; and S085's "the signature it keeps for each" does not hold for 11 of the 36 keys
(5 keep none, 6 keep another selector's). The "not first" alternative in the Limits is also
contradicted on fresh data: under `0xc45a0155` the first candidate is filtered, and on the c1 set
non-first spam candidates are unfiltered (round-29 wave-1 seat `ScoutCorrectionSites`).
