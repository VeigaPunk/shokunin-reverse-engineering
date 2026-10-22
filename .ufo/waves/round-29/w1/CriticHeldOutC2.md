# CriticHeldOutC2: is R29-C2 a held-out test or a re-observation?

Seat: KaidokuR29.CriticHeldOutC2 (critic, wave 1). Lane tip 18be864a528873b2b70d8c94e31f880290249e90, base
bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47, freeze dbd87cfa. Read-only on the lane. No git writes, no network, no REA.

Attacked: whether R29-C2 is held out (claims.json R29-C2 `kind`/`separation`; entry
`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md`, especially `## Separation`, line 18 and lines 74-80;
counter `tools/round-29/c2-filtered-unseen.py`; data `corpus/evidence/round-29/c2/`).

## Verdict

- **Held-out test vs re-observation: HOLDS as a held-out test.** It is not a re-observation (observation plus
  inference, details below). At the base the lane held no openchain response and no candidate list for any of the
  178 selectors. Reading the canonical list tells you what the rule predicts once you know the candidate names. It
  does not tell you the observed flags, and the observed flags are the only thing that can produce a mismatch. A
  real way to fail existed: see 0x09b81346 below.
- **The strength of the test is overstated: FAILS on three wording points, all fixable.** None changes the
  counter result, which is still `mismatches=0`, exit 0.

## Strongest objection

The claim is "0 mismatches of 252 entries", and the separation section says it separates rival rules. Most of that
number does not test the part of the rule that matters:

1. **c1 set, 199 of 252 entries.** These are all in the "not a canonical key, so false" branch. Their predictions
   are identical to an "always false off the list" baseline. Round 28 already tested that branch on held-out
   selectors: base `.ufo/waves/round-28/a2w/CriticC2Width.md:44` says "0 of the 187 held-out selectors are
   canonical keys, so for all 147 held-out entries the rule only predicts `false`." The 152 responses are also
   byte-identical to R29-C1's own openchain `filter=false` lookups, fetched in an overlapping window. So this is a
   second copy of shared evidence, not an independent observation.
2. **Canonical set, 26 keys and 53 entries.** Only 15 keys (37 entries: 22 predicted true, 15 predicted false)
   actually exercise the comparison `name !== signature` against a string that appears among the candidates.
   - 4 keys returned no candidate, so they test nothing.
   - 7 keys (2 `system:magic`, 5 mis-keyed; 16 entries) are filtered entirely because the key is on the list.
     Every candidate is true whatever the kept string is.
3. **The separation sentence is false as written for 11 of the 26 keys.** Entry lines 78-79 and claims.json line
   61 say: "a list whose kept signature differs on any of the 26 keys would have shown mismatches there". On the 4
   empty keys nothing can mismatch. On the 7 all-filtered keys, a deployed list with a different kept string that
   also matches no candidate gives the same flags. Only a list that keeps one of the returned names, or drops the
   key, is caught there.

On top of these, there is false provenance at entry line 18: "Three consequences the round-28 entry did not
state". The first of the three (a key with no `signature` filters every candidate) is stated in the round-28 entry
at the base, line 24: "no `signature` field, so every candidate for them is marked (seat `SourceFilterCode`)". That
consequence was a pre-registered prediction that this round tested for the first time. It is not a new finding.

## Answers to the assigned questions

**Could the outcome have been known? Inference: largely expected, but not known.**
- Observation: the freeze-time screen gives `preseen --kind flag` overlap=0
  (`.ufo/waves/round-29/before/preseen-c2-flag.txt`, quoted in claims.json line 10).
- Observation: I widened that screen. I searched the base for each of the 26 canonical keys as a whole word, in any
  file and any format. The screen only looks at openchain-shaped JSON, so this also covers markdown and TSV
  quotations. The only hits are:
  - copies of the list itself;
  - round-28 seat reports about the code and the list (ReviewC2Counter, SourceCanonicalList, SourceFilterCode,
    CriticSourceRows, ReviewSpotcheckRouting, CriticC2Width);
  - arc3 compiler and prologue artifacts (`^60806040`, `0x01ffc9a7` in Cr1Sample.sol and solc drift JSON);
  - the r3 and r28 knowledge entries.

  None of them quotes an openchain or 4byte candidate list or a `filtered` value for any of the 26 keys.
- Inference: the chance of 0 mismatches was high before the fetch. Round 28 got 0 mismatches live on 10 canonical
  keys, and `filterResponse` hashes the same at every revision from d5a8f035 to 189cd726 (base CriticC2Width.md:37).
  That makes this a low-surprise held-out test, not a re-observation. A high prior does not make a test
  re-observed. Seeing the answer before the freeze would, and that did not happen.
- Observation, a real way to fail: base CriticC2Width.md:37 says the canonical list "added `0x09b81346`" in commit
  56c6b336 (2025-10-29). A deployment on an older list would have returned `filtered: false` for 0x09b81346's
  non-kept candidate. The fetch shows 1 entry predicted true and observed true there. Mismatches were possible, and
  none occurred.

**Is `predicted_true >= 1` a real risk or a certainty? It is not a test of the rule at all.**
- Observation: the counter computes `pred = c is not None and it.get("name") != c.get("signature")`
  (counter line 198). It uses only the candidate names and the pinned list, never the observed flag. So
  `predicted_true` cannot fail because of what openchain says about filtering. It can only fail if the database
  holds no non-kept name under any of the 26 keys.
- Inference: given the list read before the freeze, that failure was close to impossible. The 5 signature-less
  magic keys make any candidate under them a true prediction. Round 28's 10 ERC-20 and Ownable keys alone had
  produced 59 true predictions (base CriticC2Width.md:10). Observed this round: 38 true predictions from 15 keys.
  It is a coverage guard that makes sure the true branch has data, which is useful. It should not be read as a
  falsification risk. The only number that can falsify the rule is `mismatches`.

**Does the c1 set add a test or pad the count? Both.**
- It adds a test (observation): it separates two named rivals on unseen data.
  - A `hasVerifiedContract` rule: 44 c1 entries have `hasVerifiedContract: false`, and all 44 are
    `filtered: false`.
  - A "mark every non-first candidate" rule: 36 of the 152 selectors have more than one candidate, which gives 47
    non-first entries, all `filtered: false`.
- It pads the count (observation): it cannot tell the rule apart from "always false off the list". It repeats the
  branch round 28 already tested on held-out data. Its bytes are R29-C1's lookup responses again
  (152/152 byte-identical). It raises the headline from 53 entries to 252.
- Note (observation): the canonical set separates the `hasVerifiedContract` rival by itself. On canonical
  entries, `filtered == !hasVerifiedContract` holds for 38 and fails for 15. The rival "canonical key and
  non-first" is not separated by the 15 string-comparison keys, because the kept signature is first in all 15. It
  is separated only by the 7 all-filtered keys, where the first candidate is also filtered.

**Separation section of the C2 entry.**
- What holds: c1 separates the `hasVerifiedContract` and non-first rivals.
- What fails: the "list differs on any of the 26 keys" sentence (the counterexample is point 3 above). The final
  caveat about the other 10 keys is correct but incomplete, because it leaves out the 11 weak keys.

## Impacted axes

- Depth (R29-C2's axis): the learning is real but narrower than stated. The string comparison was tested on 15
  keys, not 26.
- Provenance/honesty of the entry: the line 18 attribution is wrong.
- Duplicate authority (minor): the same openchain bytes back both R29-C1 and the c1 half of R29-C2.

These are fixable wording defects, not a tradeoff that the judge would have to reject. The claim statement's
target (178/178, mismatches 0, both branches present, entry_ok 1) is still met.

## Smallest safe correction (for the L1; I edited nothing)

1. Entry line 18: change it to "Two consequences the round-28 entry did not state, plus one it stated (line 24,
   from seat SourceFilterCode) and this round tests for the first time:"
2. Entry lines 78-80 and claims.json `separation`: replace the 26-key sentence with:

   > A deployed list whose kept signature differs on any of the 15 keys whose kept signature was returned would
   > have shown a mismatch there. On the 7 keys where every candidate is filtered, only a list that keeps one of
   > the returned names, or drops the key, is separated. The 4 keys that returned nothing separate nothing.

3. Entry `## Test`: add one line splitting the 0 mismatches by branch:
   - string comparison: 15 keys, 37 entries;
   - key membership only: 7 keys, 16 entries;
   - empty: 4 keys;
   - default branch: 199 c1 entries, which separate the `hasVerifiedContract` and non-first rivals but not
     "always false off the list", and are byte-identical to R29-C1's openchain lookups.
4. Lesson or QUALITY: state that `predicted_true >= 1` is a coverage guard computed from names, not a risk on the
   flag.

## Evidence (all observation unless labelled)

| UTC | command | exit | excerpt |
|---|---|---|---|
| 20:21:46Z | `python3 -I -B tools/round-29/c2-filtered-unseen.py --root <LANE> --rev 18be864a` | 0 | `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1` |
| 20:21:45Z | `venv/bin/python analyze.py <LANE> 18be864a` (scratch; reads via `git show`) | 0 | `string-compare both outcomes [12, 34, 22, 12]` / `kept-sig only (false only) [3, 3, 0, 3]` / `empty [4, 0, 0, 0]` / `miskeyed(all-true, no string compare) [5, 6, 6, 0]` / `magic(all-true, no string compare) [2, 10, 10, 0]` / `c1 set: {"sel": 152, "entries": 199, "multi": 36, "hvc_false": 44, "nonfirst": 47, "obs_true": 0, "empty": 0}` |
| 20:22:14Z | `git grep -l -i -w -E "(0x)?<key>" bacbe9cc -- .` for each of the 26 keys | 0 | e.g. `0dfe1681 files=1 corpus/evidence/round-28/c2/canonical-signatures.json`; `60806040 files=10 .ufo/waves/arc3-loop1-round3/...prologues.py ...` |
| 20:23:31Z | the same search with line content for 60806040, d55ec697, 01ffc9a7, 60a06040 and 09b81346 | 0 | only list, code-review, compiler-artifact and knowledge-entry lines; no candidate or `filtered` value |
| 20:22:17Z | python over the c1 and c2 manifests | 0 | `openchain 152 ['2026-10-22T20:03:40Z'] ['2026-10-22T20:08:52Z'] ['filter=false']`; `c2 178 2026-10-22T20:03:21Z 2026-10-22T20:06:17Z` |
| 20:22:53Z | python comparing c1/db and c2/db openchain bytes for the 152 c1 selectors | 0 | `byte_identical=152 bytes_differ=0 name_flag_sets_differ=0 missing_in_c1=0` |
| 20:22:48Z | `sha256sum` of the r29 list and `git show bacbe9cc:corpus/evidence/round-28/c2/canonical-signatures.json` | 0 | both `5572beb5…b3e2` (identical list held before the freeze) |
| 20:23:35Z | python over the canonical responses | 0 | `canonical keys with kept sig first=15 not_first=0; canonical entries where filtered==!hasVerifiedContract: 38, differ: 15` |
| 20:23:43Z | `git show bacbe9cc:corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`, lines 18-30 | 0 | line 24: "no `signature` field, so every candidate for them is marked (seat `SourceFilterCode`). None of" |

Sources opened (local lane files, read 2026-10-22, plain file read or `git show`):

| file | sha256 of bytes read | quote (line) |
|---|---|---|
| corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md (tip, clean) | 3a66ee2f927ff19b9e001de174c3dc4eeb0c496137cb068ba81a57ff152fdc4d | "Three consequences the round-28 entry did not state:" (18) |
| .ufo/waves/round-29/claims.json (tip) | 76bc0d8f556019763157bbb74cd43b9983b9e7cf77ad9d92cae898365a60cf79 | "a service that applies a list other than the pinned one would give mismatches on any of the 26 canonical keys" (61) |
| tools/round-29/c2-filtered-unseen.py (tip, equals pin) | 00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801 | `pred = c is not None and it.get("name") != c.get("signature")` (198) |
| tools/round-29/preseen.py (tip) | 073381ca213573b8809a130cf3d958e0b253b4d56a7ce34079ef2f2b0c89d167 | "every selector with a tracked openchain response at --rev" (10) |
| corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md @ bacbe9cc | 964e19bac43d089447945df13492af154bbc05cc09954502c0fe8aa66c5be9bd | "no `signature` field, so every candidate for them is marked" (24) |
| .ufo/waves/round-28/a2w/CriticC2Width.md @ bacbe9cc | 5e2a35ca9beac9e9f0d1c3d1eb23d420c2392939356597e2be2465bf54bb0561 | "0 of the 187 held-out selectors are canonical keys, so for all 147 held-out entries the rule only predicts `false`" (44) |
| .ufo/waves/round-28/a2w/SourceFilterCode.md @ bacbe9cc | 94af52641e20fb981bf042e8373c3c1d8e39c5233c21486e01ef39ddd205b5b2 | "`name !== undefined`, so every candidate is marked." (64) |
| corpus/evidence/round-29/c2/db/manifest.json (tip) | 098d02bbef8a5f722b37b8dc021deaa2846646beef0f2b589bb14abe7dad6c02 | utc range 20:03:21Z-20:06:17Z (computed) |
| corpus/evidence/round-29/c1/db/manifest.json (tip) | 16172f2fd994eb9a37c0d5ba3332b745426c93eda785fea51b0f76e357d6640e | openchain utc range 20:03:40Z-20:08:52Z, `filter=false` (computed) |

Unknown: whether the L1 knew openchain's candidate sets for these keys from outside the lane before the freeze.
Nothing in the lane shows it. Even if the L1 did, that would only affect `predicted_true`, not `mismatches`.

## Scratch artifacts (/fast/scratch/hyaku/kaidoku-r29/seats/w1/CriticHeldOutC2/)

- `analyze.py`: sha256 a9e6761e66042dbb6fa62552a8f8528263366528f034707c615c97b354bc66dd
- `analyze-out.txt`: sha256 88197fc9f23b53d80704a176930d653204df209393dbce55da16ffdf6977bb73
- `venv/`: a scratch virtual environment, not evidence

## Tooling

One install: pycryptodome 4.1.0, installed with `uv venv` + `uv pip` into the scratch `venv/`. I needed it for
keccak-256, to check which kept signatures hash to their own key. No pacman. No network lookups to 4byte or
openchain. No REA.
