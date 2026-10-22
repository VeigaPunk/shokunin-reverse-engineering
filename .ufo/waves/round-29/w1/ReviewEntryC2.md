# ReviewEntryC2 — statement-by-statement review of the R29-C2 knowledge entry

Reviewed: `corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md` against committed
bytes at `18be864a528873b2b70d8c94e31f880290249e90` (measured tip), all checks 2026-10-22 UTC.
Verdict: **holds, with one factual defect and one overclaim** — neither touches the claim's
counted result.

## Verification commands run

- `python3 -I -B tools/round-29/c2-filtered-unseen.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 18be864a528873b2b70d8c94e31f880290249e90`
  → `responses_complete=178/178 entries=252 mismatches=0 predicted_true=38 predicted_false=214 entry_ok=1`, exit 0 — identical to the entry's recheck expectation. (observation)
- `python3 tools/round-29/preseen.py --root <lane> --rev bacbe9cc… --check corpus/evidence/round-29/c2/selectors.tsv --kind flag`
  → `test_selectors=178 seen_set=230 overlap=0`, exit 0. (observation)
- Independent re-audit script (`audit.py`, sha256 `fc03b42c…`, scratch path below) replaying the
  rule over all 178 committed response bytes with `selector_of` imported from
  `tools/round-25/a2/resolve-selectors.py` (Keccak-256, self-test vectors pass).
- `curl` of `handlers.ts` and `canonical-signatures.json` at Sourcify `0966a3bc` (staging) and
  `189cd726` (master): all four fetches returned the recorded sha256s
  (`30981efb…` / `5572beb5…`); the lane's pinned `corpus/evidence/round-29/c2/canonical-signatures.json`
  is byte-equal to both upstream copies. `handlers.ts:39-66` is `filterResponse` and `:47-48` is
  `signatureItem.filtered = signatureItem.name !== expectedCanonical.signature;` — as cited. (observation)
- `git ls-tree`/log/show at base `bacbe9cc`, freeze `dbd87cfa` (committer 2026-10-22T20:03:06Z),
  data commit `4fcea978` (20:09:09Z): all 179 c2 db files first appear in `4fcea978`; manifest
  `utc` values span 2026-10-22T20:03:21Z–20:06:17Z, every `status=200`, `tries=1`. (observation)

## Statement-by-statement verdicts

### Header (lines 1–3)
- `source:` line cites S087; S087 is a SOURCES row new since base, status `mined`, opened
  2026-10-22, listed in the lesson's `## Gate`; `verified-at`/`recheck:` format and the expected
  counter string all match what the counter enforces. **Holds** (observation: counter `entry_ok=1`).
- Fetch window `20:03:21Z–20:06:17Z`, all HTTP 200 first try, frozen at `dbd87cfa`:
  manifest min/max confirms; freeze committer time 20:03:06Z precedes first fetch by 15s.
  **Holds** (observation). Provenance relies on git committer timestamps — noted, not a defect.

### Rule section (lines 15–34)
- `filterResponse` `:39-66`, assignment `:47-48`, identical at `0966a3bc` and `189cd726`:
  byte-identical confirmed by sha256. **Holds.**
- 5 `system:magic` keys (`0x60806040`, `0x60a06040`, `0x60c06040`, `0x60e06040`, `0x61010060`)
  carry no `signature`; 31 kept signatures; 36 keys total. **Holds.**
- `0x60806040` "the usual start of creation code": correct for the classic `PUSH1 0x80 PUSH1 0x40`
  prelude. **Holds.**
- **6 of 31 kept signatures do not hash to their own key** — recomputed with the round-25
  `selector_of` over the S087-byte-equal pinned list; all six pairs and all six claimed true
  selectors match exactly: `0x0d0f30c6`→`token1()`(`d21220a7`), `0x1a686502`→`uniswapV3SwapCallback(int256,int256,bytes)`(`fa461e33`),
  `0x89035730`→`flash(address,uint256,uint256,bytes)`(`490e6cbc`), `0xc45a0155`→`mint(address,int24,int24,uint128,bytes)`(`3c8a7d8d`),
  `0xfc6f7865`→`uniswapV3MintCallback(uint256,uint256,bytes)`(`d3487997`), `0x8abf6077`→`proxyOwner()`(`025313a2`).
  Exactly 6; no others mis-keyed. **Holds.**
- "Every stored candidate hashes to its selector (all 252 entries fetched here do)": recomputed
  over all 252 candidates — zero keccak mismatches. **Holds.**
- "Under these 6 keys no candidate can equal the kept signature and every candidate … is
  filtered": sound inference, and observed true (every candidate under the 5 non-empty mis-keyed
  keys has `filtered: true`; `0x0d0f30c6` is empty). **Holds** (inference + observation).

### Test section (lines 38–61)
- selectors.tsv: 178 rows = 26 `canonical` + 152 `c1`. The 26 are exactly the canonical keys
  absent from `flag_seen` at base (`preseen --kind flag` → overlap=0, exit 0); the other 10 keys
  (`06fdde03`, `095ea7b3`, `18160ddd`, `23b872dd`, `313ce567`, `70a08231`, `8da5cb5b`, `95d89b41`,
  `a9059cbb`, `dd62ed3e`) all have committed openchain responses at base under
  `corpus/evidence/round-25/` and `corpus/evidence/round-28/c2/db/` — "answered in rounds 25 and
  28" verified per-selector. **Holds.**
- The 152 `c1` rows equal `corpus/evidence/round-29/c1/heldout.tsv` first-column set exactly;
  none is a canonical key. **Holds.**
- Table numbers — canonical 26 sel / 53 entries / 38 predicted+observed filtered; c1 152 / 199 /
  0; all 178 / 252 / 38 / **0 mismatches** — independently recomputed from response bytes and
  agree with the counter. **Holds.**
- "4 canonical keys returned no candidate (`0x0d0f30c6`, `0x60c06040`, `0x60e06040`,
  `0x61010060`)": exact; those four bodies hold `[]`. **Holds.**
- `0x60806040`: 6 candidates all `filtered: true`; `0x60a06040`: 4 of 4. **Holds.** "spam-like"
  names (`slappychuck_emorxmvrbf`, `_SIMONdotBLACK_`, `atInversebrah`, …) is accurate.
- Mis-keyed live cases: `0x1a686502`→only candidate `liquidity()`; `0x89035730`→`parameters()`;
  `0x8abf6077`→`impl()`; `0xfc6f7865`→`collect((uint256,address,uint128,uint128))`;
  `0xc45a0155`→2 candidates including `factory()`; all `filtered: true`; `0x0d0f30c6` empty.
  "5 of the 6 returned candidates and every one was filtered" — exact. **Holds.**

### Round-28 characterization (lines 7–11)
- Round-28 entry confirms 230 selectors, 168 pre-answered, all predicted-true from probed
  selectors (its own M28-4 admission). **Holds.**

## Findings

### F1 — factual defect (minor): wrong carrier for `factory()`
Entry line 60: "`0xc45a0155` (2 candidates, one of them `factory()`, the function R29-C1 carrier
**n08** holds under that selector)". `keccak256("factory()")[:4]` is `c45a0155`, and `factory()`
is indeed a function on a round-29 carrier — but it is defined in
`corpus/evidence/round-29/c1/src/UniV2Pair.sol:17` / `UniV2Pair.abi.json`, which `carriers.tsv`
maps to **n06**, not n08. n08 is `UniV2Factory` (ABI: `allPairs`, `allPairsLength`, `createPair`,
`feeTo`, `feeToSetter`, `getPair`, `setFeeTo`, `setFeeToSetter`) and holds no `factory()`; the
Uni V3-style signature `factory()` on a pair, not a factory, was likely the source of the
confusion. `c45a0155` is not a heldout selector (correctly — it is a canonical key). Cosmetic:
the entry's substantive point — a filtered candidate can be the true name — is unaffected.
Severity: low.

### F2 — overclaim (minor): separation guarantee for the 26 keys
Entry line 78: "A service applying a list whose kept signature differs on any of the 26 keys
would have shown mismatches there." False as stated. The test detects a kept-signature change on
a key only when the key's response contains at least one candidate whose flag the change flips:
- the 4 keys that returned no candidates (`0x0d0f30c6`, `0x60c06040`, `0x60e06040`,
  `0x61010060`) cannot show any mismatch regardless of the list;
- on the 7 keys where every candidate is filtered (`1a686502`, `60806040`, `60a06040`,
  `89035730`, `8abf6077`, `c45a0155`, `fc6f7865`), an alternate signature is detected only if it
  names one of the stored candidates;
- only the 15 keys with an unfiltered candidate reliably expose any differing kept signature.
The next sentence ("a list equal … on these 26 keys but different on the other 10 is not
separated") shows the author understands the mechanism, making the unconditional wording an
overclaim rather than an error of reasoning. Severity: low; honest-fix is a one-clause qualifier.

### F3 — verified, not a defect
- Separation clauses about `hasVerifiedContract`-derived filtering and "every non-first
  candidate": hold — `0x7ecebe00` alone yields both counterexample shapes (first candidate
  `nonces(address)` has `hasVerifiedContract: true` yet `filtered: false`; the 2 non-first
  candidates are also `filtered: false`). "Several selectors have spam collisions" on c1: holds
  (many multi-candidate c1 rows carry junk names, e.g. `_$_$$_$__$$$$…`, `transfer_attention_tg_*`).
- "A list equal on these 26 keys but different on the other 10 is not separated": correct —
  the other 10 keys were excluded by construction.
- Limits section accurately reflects scope (deployed revision assumed; one fetch instant; the
  26 keys are the complete unanswered set, not a sample; the 6-of-31 count is an L1 list-reading,
  not a counter output — consistent with the Gate note).

## Residual risk / verification gaps

- Correctness of `filtered` was verified against the committed response bytes and the pinned
  upstream list; whether `api.openchain.xyz` currently runs `0966a3bc` remains an assumption the
  entry itself discloses.
- Response **order** and `hasVerifiedContract` were not checked against any rule (none exists);
  `hasVerifiedContract` values in the db were observed only as bycatch.
- Provenance ordering (freeze before fetch) rests on git committer timestamps plus manifest
  `utc` fields, consistent with the counter's own mechanism.

## Scratch artifacts (all under /fast/scratch/hyaku/kaidoku-r29/seats/w1/ReviewEntryC2/)

- `audit.py` — `fc03b42cfff28e909a141e9e292d257d205e172aad88294212ff4274b3a6c6c8` (independent re-count + keccak checks)
- `ten-keys.tsv` — `823c51d07ba8616aae369839d3cd75371ab77162af3704f8df596e8d7ebfc680` (preseen input for the 10 excluded keys)
- `handlers-0966a3bc….ts` / `handlers-189cd726….ts` — `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38` each
- `canonical-0966a3bc….json` / `canonical-189cd726….json` — `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` each

No tools installed; no lane writes. Network: 4 `curl` GETs to raw.githubusercontent.com only
(primary source, no bot challenge); zero requests to 4byte.directory or api.openchain.xyz.
