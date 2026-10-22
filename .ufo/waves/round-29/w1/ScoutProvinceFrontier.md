# Scout — PROVINCE.md EVM core and Frontier text for round 29

**Question.** At `18be864a528873b2b70d8c94e31f880290249e90`, what do the EVM lines in `PROVINCE.md` (Core and the Frontier bullet "EVM bytecode (extended)", round-28 annotation near `:94`) say, and what would a one-line round-29 annotation have to say to be accurate given the two round-29 entries?

**Scope.** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md` at the measured tip: blob `4fdab20bf8612567016d637c4f4c6ca9b816efde`, content sha256 `bc153a5c89f5fae5892fb6b1900fe373cc48da3ecffa3a87e7f30ae2d8300748`, 327 lines. `PROVINCE.md` is byte-identical at base `bacbe9cc` (`git diff --stat` empty), so every line below is both the tip and the base text. No lane file was written except this report. Read-only git only; no REA, no network lookup, no 4byte/openchain request. Scratch: `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScoutProvinceFrontier/`.

## 1. What the current text says

### 1.1 Core — line 54 (the only EVM row in the Core table)

```
54: | EVM interface | `rea inspect-evm-interface <file> <raw|hex>` — encoding is POSITIONAL (no `--encoding` flag despite schema); bundled EVMole 0.9.3/WASM | synthetic hex carrier → selector extraction | hand-assembled 81-byte dispatcher recovered all 3 planted ERC-20 selectors; `dispatch:"abi"` (r3-07) |
```

It says, cell by cell: the verb is `rea inspect-evm-interface <file> <raw|hex>` and the encoding argument is positional (no `--encoding` flag despite the schema); the provider is bundled EVMole 0.9.3/WASM; the readiness probe used is a synthetic hex carrier for selector extraction; the verified evidence is the r3-07 hand-assembled 81-byte dispatcher, which recovered all 3 planted ERC-20 selectors with `dispatch:"abi"`. The table header (`PROVINCE.md:40`) dates the table's verification to 2026-10-13.

### 1.2 Frontier — lines 91–94, bullet "EVM bytecode (extended)"

```
91: - **EVM bytecode (extended)** — selectors held on synthetic dispatcher
92:   (Core, r3-07), real solc-0.8.37 carriers (Core, arc3-r1/r3) and a vyper-0.4.3
93:   carrier (arc3-r4); names are labelled candidates from saved signature-DB lookups, never verified (`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`).
94:   Round 28 (claim R28-C1 missed, 60 of 61 runs; Frontier status unchanged): on 187 held-out selectors the round-25 primary naming rule was observed at named 137, right 137, wrong 0 (`corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md`). openchain's `filtered` flag is set only for selectors on Sourcify's 36-key canonical list; it was re-observed on 10 of those keys, the deployed revision is not identified, and the test is not held out (`corpus/knowledge/2026-10-22-r28-openchain-filtered-flag.md`).
```

Line 95 is blank; `## Adjacent` is line 96.

It says: `:91-93` states what is held (synthetic dispatcher, r3-07; real solc-0.8.37 carriers, arc3-r1/r3; a vyper-0.4.3 carrier, arc3-r4) and the bullet's reservation — names are labelled candidates from saved signature-DB lookups, never verified. `:94` is the round-28 dated annotation: R28-C1 missed its target (60 of 61 runs), Frontier status unchanged; on 187 held-out selectors the round-25 primary rule was observed at named 137, right 137, wrong 0; openchain's `filtered` flag is set only for selectors on Sourcify's 36-key canonical list, was re-observed on 10 of those keys, the deployed revision is not identified, and the test is not held out.

Related, not part of the bullet: `:310` (round-27 dated section) says "the Frontier list (PE subtypes, recorded crashes above 32 MiB, alternate providers, macOS-only surfaces, EVM bytecode extended) is unchanged by this round". That is a dated statement about round 27, not a current status (precedent: the round-24 section at `:278-281` supersedes an earlier placement "without rewriting that table").

## 2. What the two round-29 entries establish (frozen at the tip)

R29-C1 (`corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`, tip blob `bdd3922efff6…`, content sha256 `9233ac85b2c9…`; target met as measured): 16 fresh solcjs-0.8.37 stub carriers, hex-screened 16/16; 152 selectors held out of the lane at the base (none in round 25's 43 or round 28's 187, none present as an 8-hex word at the base; pre-seen overlap 0); all 152 held-out selectors recovered by REA (`recovered_by_rea 152`); the unchanged round-25 primary rule `openchain_sole_unfiltered_args_consistent` scored **named 122, right 122, wrong 0, no name 30**, against each carrier's compiler ABI. 30 abstentions: 24 `bytes32` inferred `uint256`, 3 `string` inferred `bytes`, 3 spam ties. Only 15 of the 16 carriers contribute held-out rows (n09/WETH9 keeps a run but no row); only n04's interface list is sourced (S088).

R29-C2 (`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md`, tip blob `a9a8b8d03d15…`, content sha256 `3a66ee2f927f…`; target met as measured): 178 selectors with no openchain response in the lane at the base (26 unanswered canonical keys + the 152 C1 selectors), 178/178 responses fetched after the freeze; 252 candidate entries, **mismatches 0**, 38 predicted and observed `true`, 214 `false`. The 53 canonical-set entries split 38 true / 15 false; all 38 true entries fall on 19 of the 26 canonical keys (4 keys returned no candidate; 2 of the 5 signature-less `system:magic` keys and 5 of the 6 mis-keyed keys returned candidates). The deployed revision is assumed, not identified. The entry's own check (not a counter output) finds 6 of the 31 kept signatures do not hash to their key: `0x0d0f30c6`→`token1()`, `0x1a686502`→`uniswapV3SwapCallback(...)`, `0x89035730`→`flash(...)`, `0xc45a0155`→`mint(...)`, `0xfc6f7865`→`uniswapV3MintCallback(...)`, `0x8abf6077`→`proxyOwner()`.

In-flight note (observation, not current state): while this scout ran, the working tree (HEAD still `18be864a`) acquired uncommitted edits to `LOG.md`, `SCORECARD.md`, both round-29 entries and `tools/round-29/prefile-check.sh` (`git status --porcelain` at 20:33:35Z). The revised entries keep the same headline numbers (C1 122/122/0/30; C2 0 of 252, 38/214, 6 of 31) but add wave-1 wording: C1's limits now say the names are author-selected public names and some name strings were already in the lane; C2 adds a branch decomposition (37 entries under 15 keys with the kept signature present, 22 true/15 false; 16 entries under 7 keys — 2 magic, 5 mis-keyed — filtered because the key is listed at all, all true). `PROVINCE.md` itself is unchanged (`working=tip=4fdab20b…`). A single working-tree `LOG.md` round-29 section exists at line 2997 but does not claim a Frontier→Core move. This report's proposed text is written to fit both the tip entries and the revised wording.

## 3. What round 29 falsifies or sharpens in the current text

- **Falsified (exactly one clause):** `:94` "and the test is not held out". Round 29 is the held-out test of the same rule: 178 selectors with no openchain response anywhere in the lane at the base, screened before the freeze (`preseen.py --kind flag` → `overlap=0`), with both branches present on data never fetched. Leaving `:94` unannotated makes PROVINCE carry a current falsehood.
- **Not falsified — `:91-93`:** the carriers are still compiled stubs and the names are still not verified on a deployed artifact; "right 122" is measured against the compiler ABI of an L1-written stub, so `:93`'s "never verified" stands. C1's selectors are held out; its names are public and author-selected (revised entry's Limits), which the annotation must not blur.
- **Confirmed and sharpened — `:94` first clause:** C1's own lookups show 0 of the 199 non-canonical entries marked `filtered`, so the flag is inert outside the 36 keys; round 29 adds that every candidate under a signature-less key is filtered and that 6 kept signatures are mis-keyed (entry's own check).
- **Not falsified — `:54`:** round 29 re-exercises the same verb with the same positional `hex` argv at `rea-agents@6.5.0` on 16/16 fresh carriers, provider `evmole@0.9.3`. Nothing in the row's text or its r3-07 evidence changes.
- **Dated, not current — `:310`:** it remains true for round 27 and needs no edit, even if the bullet later moves (the document keeps dated supersessions).

## 4. Proposed annotation (primary)

Insert as a new paragraph line after `:94` (two-space indent, one physical line, same shape as the round-28 paragraph):

```
  Round 29 (claims R29-C1 and R29-C2 met as measured — C1 16/16 runs, 152/152 rows; C2 178/178 responses; Frontier status unchanged): on 152 selectors absent from the lane at the base, drawn from 15 of the 16 fresh solcjs-0.8.37 stub carriers holding published function lists, the unchanged round-25 primary rule scored named 122, right 122, wrong 0, no name 30 against each carrier's compiler ABI rather than a deployed contract (`corpus/knowledge/2026-10-22-r29-evm-fresh-selector-naming.md`); the Sourcify `filtered` rule then held out of sample at 0 mismatches of 252 entries on 178 never-fetched selectors (26 canonical keys + the 152), 38 predicted and observed `true` — all on 19 of the 26 canonical keys — and 214 `false`, superseding the round-28 clause "the test is not held out" while the deployed revision is still not identified (`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md`).
```

Exact scratch copies: `annotation-A.txt` (sha256 `c5c02ad8f09f…`), `PROVINCE-proposed.md` (`c318b6cf9fc4…`), `province-annotation.diff` (`6d15ac008c92…`, `diff` exit 1 as expected for a difference). Placement precedent: commit `2832c5b3` inserted the round-28 paragraph after `:93` (`PROVINCE.md | 1 +`), and `071270b5` corrected its wording (`1 insertion(+), 1 deletion(-)`). Inserting after `:94` shifts every later PROVINCE line by +1 (`## Adjacent` 96→97); citations to earlier baselines are governed by `SCORECARD.md:16-17` ("Line citations to pre-existing lane files refer to the baseline revision unless explicitly marked current").

### 4.1 Why each clause is required

| Clause | Required because | Failure if omitted |
|---|---|---|
| "claims R29-C1 and R29-C2 met as measured — C1 16/16 runs, 152/152 rows; C2 178/178 responses" | `:94` records the prior round's miss and run count; C1's frozen target is completeness (`runs_ok`, `rows_complete`, `tally_equal`, `entry_ok`) and C2's includes `responses_complete 178/178` | A reader cannot tell round 29 apart from round 28's honest stop, or whether the triple came from a complete run set |
| "152 selectors absent from the lane at the base" | The selector screen is C1's only held-out property (`preseen.py --kind name` → `overlap=0`) | "122 right" would read as a blind test on arbitrary selectors |
| "drawn from 15 of the 16 fresh solcjs-0.8.37 stub carriers" | `heldout.tsv` has 152 rows with 15 distinct carrier ids; n09 keeps a run but no held-out row (entry, Result) | "152 on 16 carriers" — the entry's own table heading — overstates; PROVINCE should be exact |
| "holding published function lists" | The carrier class (entry intro: "16 new carriers that hold published function lists") | The carriers could be mistaken for collected or deployed contracts |
| "the unchanged round-25 primary rule" | The claim tests the same rule, not a newly fitted one (`primary_rule` in `claims.json`) | A reader would think a new rule was chosen on these rows |
| "named 122, right 122, wrong 0, no name 30" | The learning, including the 20% abstention that keeps the wrong count at 0 | Reporting only "right 122" hides that recall is bought by abstention |
| "against each carrier's compiler ABI rather than a deployed contract" | Entry Limits ("not deployed contracts"; "the ground truth for every row is still the compiler ABI") and `:93`'s "never verified" | "right 122" would contradict `:93` or claim deployed-name verification |
| "the Sourcify `filtered` rule then held out of sample" | C2 is the first held-out test of the rule; round 28's was a re-observation (M28-4) | The annotation would repeat round 28's stale "not held out" state |
| "0 mismatches of 252 entries on 178 never-fetched selectors (26 canonical keys + the 152)" | C2's counted result and exact set composition (26 + 152 = 178) | A reader may think all 36 canonical keys were fetched; "never-fetched" is the held-out property |
| "38 predicted and observed `true` — all on 19 of the 26 canonical keys — and 214 `false`" | Both branches present, and the true branch is confined to canonical keys (0 of 199 c1 entries filtered) | "38 true" alone invites the false reading that non-canonical selectors produce filtered entries |
| "superseding the round-28 clause 'the test is not held out'" | The only current PROVINCE sentence round 29 falsifies; dated supersession is this document's convention (`:278-281`) | PROVINCE would carry a false current statement |
| "while the deployed revision is still not identified" | C2 Limits ("The deployed revision behind `api.openchain.xyz` is assumed") | A reader may think round 29 matched the live service revision |
| "Frontier status unchanged" | Promotion rule `:75-76`; no round-29 `LOG.md` entry at the measured tip; the bullet's `:93` reservation is not discharged | A reader may think the bullet moved to Core, or that the round changed nothing |

## 5. Optional expansions

**B — edge cases the flag now carries** (append to A, or use instead of the last clause if space allows; scratch `annotation-B-extra.txt`, sha256 `3e25b442277b…`):

```
  The entry's own reading of the pinned list, not a counter output, makes every candidate under the 5 signature-less keys filtered and finds 6 of the 31 kept signatures that do not hash to their key, so `filtered` can hide the true name (`corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md`).
```

Why optional rather than mandatory: it is the entry's post-fetch reading (not a counter output), and the two entries' pointers already lead to it. Why it is still worth having: without it, `:94`'s "filtered is set only for selectors on [the list]" invites using the flag as a spam filter, which is wrong on the 5 magic keys and the 6 mis-keyed keys.

**Core — optional dated re-exercise note** (scratch `annotation-core-optional.txt`, sha256 `aa55ab5398a1…`):

```
  Round 29 re-exercise (dated; the Core table above remains the 2026-10-13 record): `inspect-evm-interface <runtime> hex --format json` at `rea-agents@6.5.0` exited 0 on 16 of 16 fresh solcjs-0.8.37 runtime files, provider `evmole@0.9.3`, recovering all 152 held-out selectors (`corpus/evidence/round-29/c1/runs.tsv`; envelopes `corpus/evidence/round-29/c1/envelopes/`).
```

Recommendation: **no Core edit is required.** Nothing in `:54` is falsified; the row is the 2026-10-13 surface record (`:40`), and the document's convention for later additions is a dated section that does not rewrite the table (`:306-310`). If the L1 wants the second-pin liveness datum in PROVINCE, put the line above in a new dated section at the end, not in the table cell, and do not claim "WASM" (the envelope exposes `provider.version = evmole@0.9.3`, not the packaging).

## 6. Frontier status: unchanged (recommendation with reasons)

`PROVINCE.md:75-76` makes promotion mechanical: a Frontier bullet "moves to Core by a `LOG.md` entry citing the corpus entries that earned it." At the measured tip, `LOG.md` contains no round-29 material at all (`git show …:LOG.md | grep -icE 'round.?29|r29'` → `0`, grep exit 1; the last header is round 28 at `:2985`). The uncommitted working-tree LOG section does not claim a move either. Independently, the bullet's stated reservation (`:93` "names are … never verified") is not discharged: C1's ground truth is the compiler ABI of stubs the L1 wrote from published standards (only n04 sourced, S088), and C2's deployed revision is assumed. Both round-29 items are learning claims about a rule, not a held capability to name a shipped artifact. Hence the annotation says "Frontier status unchanged".

**If the L1 decides the bullet is earned anyway:** do not write this annotation. The correct edit is the Frontier→Core move the rule describes — prune the bullet and add a dated Core section carrying the C1/C2 results and the residual (deployed-artifact name verification) as what remains Frontier — and the phrase "Frontier status unchanged" must not appear.

## 7. What an accurate annotation must not say

- "152 selectors on 16 carriers" without the 15-of-16 qualifier (n09 has no held-out row).
- "held out" applied to C1's names: author-selected public names; the held-out object is the selector set (revised entry's Limits).
- "names verified" or "verified names": C1 scores a rule against stub compiler ABIs.
- "deployed revision identified": C2 assumes it.
- "moved to Core", "Frontier held", "bullet retired": no LOG entry exists.
- "38 true on unseen non-canonical selectors": all 38 are canonical-key entries; 0 of 199 c1 entries are filtered.
- "6 of 31" (or "5 magic keys") as a counter output: the entry computes these after the fetch, over the pinned list.
- "REA recovered 152/152 names": it recovered 152/152 selectors (`recovered_by_rea 152`); names come from the database rule.

## 8. Evidence

All commands read-only; lane `HEAD = 18be864a528873b2b70d8c94e31f880290249e90`. Exit codes and UTC from the receipts in scratch (`logs/`).

| UTC | Command (abbreviated) | Exit | Exact excerpt |
|---|---|---|---|
| 20:28:26Z | `git rev-parse 18be864a^{commit}`; `git rev-parse 18be864a:PROVINCE.md`; sha256 of `git show 18be864a:PROVINCE.md` | 0 | `rev_parse 0 18be864a…`; `province_blob 0 4fdab20bf8612567016d637c4f4c6ca9b816efde`; `province_sha256 bc153a5c89f5… bytes 36450` |
| 20:28:26Z | `git diff --stat bacbe9cc 18be864a -- PROVINCE.md` | 0 | `province_diff_base_tip exit 0 out= ''` |
| 20:28:26Z | read `corpus/evidence/round-29/c1/{runs.tsv,tally.json,heldout.tsv,carriers.tsv}` + envelope provider versions | 0 | `c1_runs 16 exits ['0'] pkgs ['6.5.0']`; `c1_envelopes 16 providers {'evmole@0.9.3': 16}`; `c1_tally selector_rows 152 recovered_by_rea 152 primary {… 'named': 122, 'right': 122, 'wrong': 0, 'no_name': 30}`; `c1_heldout_rows 152 carrier_rows 16` |
| 20:28:26Z | recount `corpus/evidence/round-29/c2/db/openchain-*.json` (178 files) + `selectors.tsv` + `canonical-signatures.json` | 0 | `c2_selectors 178 sets {'c1': 152, 'canonical': 26}`; `c2_files 178 entries 252 filtered 38 per_set[…] {'canonical': [26, 53, 38], 'c1': [152, 199, 0]} nonbool 0 empty ['0d0f30c6','60c06040','60e06040','61010060']`; `canonical_keys 36 with_signature 31 no_signature 5 ['0x60806040',…]`; `mis_keyed 6` + the six rows |
| 20:28:35Z | `git show 18be864a:<entry>` + sha256 | 0 | C1 `git_show_exit 0 sha256 9233ac85b2c9…`; C2 `git_show_exit 0 sha256 3a66ee2f927f…` |
| 20:36:54Z | corrected set check: bare selectors vs the 36 canonical keys (an earlier scratch check at 20:28:35Z double-prefixed `0x`, so its 36-key line is superseded by this receipt) | 0 | `keys_36 36 c1_n 152 canon_n 26`; `c1_vs_36keys 0 canon_subset_of_36 True c1_vs_canon 0` |
| 20:34:39Z | own decomposition of canonical entries (independent of both counters) | 0 | `heldout_rows 152 distinct_carriers 15`; `canonical_keys 26 entries 53 true 38 false 15 keys_with_true 19 empty 4`; `magic_keys_with_candidates 2 miskeyed_keys_with_candidates 5` |
| 20:33:35Z | `git status --porcelain` (relevant paths); working-vs-tip `git hash-object`/`rev-parse`; `git show 18be864a:LOG.md \| grep -icE 'round.?29\|r29'`; `git show --stat 2832c5b3/071270b5 -- PROVINCE.md` | 0 (grep 1) | `M LOG.md`, `M SCORECARD.md`, `M corpus/knowledge/…r29-…` (both), `M tools/round-29/prefile-check.sh`; `PROVINCE.md working=4fdab20b… tip=4fdab20b… SAME`; `0` round-29 lines in tip LOG (exit 1); `PROVINCE.md \| 1 +`; `PROVINCE.md \| 2 +-` |

Recounts were done from committed bytes only. The only deviations: the numeric clauses were re-derived with an independent keccak-256 (pycryptodome) and independent parsing, never by re-running a lane counter; the working-tree drift row is an observation of concurrent work, not a measurement input.

## 9. Conclusion

- **Observation.** Core has one EVM row (`:54`): verb, positional encoding, EVMole 0.9.3/WASM, synthetic probe, r3-07 evidence. The Frontier bullet (`:91-94`) holds selectors on three carrier classes and reserves name verification; its round-28 annotation records a missed C1 and a non-held-out C2.
- **Observation.** Round 29 falsifies exactly one PROVINCE clause — `:94` "the test is not held out" — and falsifies nothing in Core. It confirms `:54`'s positional encoding and provider version on 16 fresh carriers and confirms the flag's inertness outside the canonical list.
- **Inference (high confidence, grounded in `:75-76`, the tip LOG, and the entries' Limits).** The accurate one-line annotation is the text in §4: both claims met as measured, C1's exact triple with its compiler-ABI qualifier, C2's held-out 0-of-252 result with its set composition and width, an explicit supersession of the round-28 clause, the assumed deployed revision, and "Frontier status unchanged".
- **Unknowns.** (1) The outside verdict on round 29 is not in the tip (SCORECARD and LOG round-29 sections exist only as uncommitted working-tree text); "met as measured" mirrors the in-flight SCORECARD wording and the counter receipts. (2) Whether the L1 integrates the revised entries/LOG/SCORECARD as they stand or further edits them; the annotation's numbers are identical in both entry versions, but the revised C1 limits add "author-selected public names". (3) Whether a later LOG entry will claim the Frontier→Core move; if so, §6's second branch applies and this annotation must be replaced, not appended.

**Confidence.** High for the line readings, the falsification set, and every number in the proposed text (each independently recounted at the tip). Medium-high for "Frontier status unchanged", which is a policy judgment grounded in the document's own promotion rule, the absence of a round-29 LOG entry, and the entries' stated limits.

## 10. Scratch artifacts (all under `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ScoutProvinceFrontier/`)

| Artifact | sha256 |
|---|---|
| `PROVINCE-tip.md` (`git show 18be864a:PROVINCE.md`) | `bc153a5c89f5fae5892fb6b1900fe373cc48da3ecffa3a87e7f30ae2d8300748` |
| `annotation-A.txt` | `c5c02ad8f09f7b6ce2666e057bb44290c839944db805d708a6c905def35f2f5e` |
| `annotation-B-extra.txt` | `3e25b442277b982a58b0a6ab710c391d041f4e7ea20069be5088248e5bc670d0` |
| `annotation-core-optional.txt` | `aa55ab53998a1495c8bb6cc495d1e19ca1395ef3d86e92ce120f85c367009d85` |
| `PROVINCE-proposed.md` | `c318b6cf9fc48d6bd64c1a65cf184dd129a9fc6f247da83e27db89167abcae48` |
| `province-annotation.diff` | `6d15ac008c92c04429e979507b930a274ee8650f859e5d8caa9c7453d2258108` |
| `verify-facts.py` | `ed45cf7c4566352ea6a0b48fa217e3592289af0108bd1b80b147b44c5dbba142` |
| `verify-sets.py` | `5de690a4e830de367c069d73ca1fe1dd813c53c476a05d040a2a4b9acf5c3ba1` |
| `logs/verify-facts.txt` | `21704216f1273f05ef6b61052b2a103257abc4b68b1cb576873d2770f44d5757` |
| `logs/verify-sets.txt` | `5a60de915e41f231888fff011681c0d996fa8069ef4c7097b2f9f7b739f6fc43` (its 36-key overlap line double-prefixed `0x`; superseded by `verify-sets2.txt`) |
| `logs/verify-sets2.txt` | `58cb8b5010daa2cc8c7695ed7af19339f0449d08f8d3fecb0388a6b6c68ee589` |
| `logs/verify-drift.txt` | `e9e460aca290fccfc9786700694465d40d5c927bd0a1c2ee07fc0b8d62b6e32e` |
| `logs/verify-counts2.txt` | `7868dc260238ba842b0bddab135f37c011503d095d5b20197a2e43b47bd83289` |

**Tool install (recorded per operator directive):** `pycryptodome 4.1.0` installed 2026-10-22 ~20:27Z into a scratch `uv venv` (`.venv`) via `uv pip install --python .venv/bin/python pycryptodome`; official PyPI channel; reason: an independent keccak-256 to check the "6 of the 31 kept signatures do not hash to their key" clause before citing it. No pacman transaction, no host service touched, no other install or update.
