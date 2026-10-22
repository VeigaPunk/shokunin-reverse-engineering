# R25 a3 wave 1 — C2IndependentTally (KaidokuR25a3.C2IndependentTally)

Seat `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2IndependentTally/`. Target: the five naming-rule counts in `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`. Method: a second, independent scorer (`independent_tally.py`) written from scratch — own Keccak-256 (FIPS-202 permutation, 0x01 padding), own ABI type canonicalisation, own rule code — reading only the saved REA envelopes, the saved 4byte.directory/openchain responses, the `db/manifest.json` files and the six compiler ABI JSONs. It never reads `tools/round-25/a2/resolve-selectors.py` nor `tools/round-25/a3/tally-resolution.py`. No lane file was edited (bounds): the §1 table is paste-ready for the L1 to place beside the entry's table. All times UTC 2026-10-22.

## 1. My table beside the entry's table — all ten numbers hold

Command: `python3 -I -B independent_tally.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --out out` (exit 0, 10:51:44Z). Selftest first: `python3 -I -B independent_tally.py --root <lane> --selftest` → `selftest: PASS` (exit 0, 10:51:44Z); it checks keccak256 of `""`/`"abc"`/`"testing"`, the selectors of `transfer(address,uint256)`=`a9059cbb`, `balanceOf(address)`=`70a08231`, `totalSupply()`=`18160ddd`, `approve(address,uint256)`=`095ea7b3`, `transferFrom(address,address,uint256)`=`23b872dd`, a SHA3-256 negative control and four canonicalisation cases. The entry's working-tree table (mtime 07:55:05Z at my last check) reads "the first number is per carrier row (69 rows); the number in brackets is per distinct selector (43)". My numbers, both scopes:

| naming rule | named | right | wrong | no name | entry (69 rows / 43 distinct) |
|---|---|---|---|---|---|
| first 4byte.directory result | 59 | 33 | 26 | 10 | 59 (34) / 33 (22) / 26 (12) / 10 (9) |
| the only 4byte candidate whose parameter list matches REA | 48 | 47 | 1 | 21 | 48 (29) / 47 (29) / 1 (0) / 21 (14) |
| first openchain result (`filter=false` order) | 62 | 61 | 1 | 7 | 62 (37) / 61 (36) / 1 (1) / 7 (6) |
| the only openchain candidate with `filtered=false` | 55 | 54 | 1 | 14 | 55 (34) / 54 (33) / 1 (1) / 14 (9) |
| the only `filtered=false` openchain candidate whose parameter list matches REA | 49 | 49 | 0 | 20 | 49 (31) / 49 (31) / 0 (0) / 20 (12) |

**Verdict: holds — ten of ten published numbers reproduce exactly** (observation). Zero count differences against the committed `corpus/evidence/round-25/a3/c2/analyze/tally.json` (`count_diffs: []`). Final gate (10:58:46Z, after the L1's wave-1 correction commit `dc31f9c4`): a parser re-read the entry's current table and compared all 40 published cells (both scopes) with my output — `FINAL: entry table matches independent scorer exactly: True`.

## 2. Cross-checks run by the same scorer

- **Row-level diff vs the published analyze files — holds.** `python3 -I -B compare.py --root <lane> --mine out/my-tally.json --out out` (exit 0, 10:51:44Z) compares, for all 69 rows, candidate lists **and their order**, per-candidate labels, openchain `filtered` flags, REA `inferred_arguments` and the ABI ground truth: `rows_checked: 69, count_diffs: 0, row_diffs: 0, abi_diffs: 0`, `wrong_names only mine: 0 only published: 0`, `no_candidate_selectors_match: True`. My 29 wrong-name rows are identical to the published ones, cell for cell (observation).
- **Canonicalisation (tuples, arrays) is provably inert here — holds.** The scorer labels every candidate twice, canonicalised vs raw string equality: `canonicalisation_label_differences: 0` over **344** labelled candidates. No ABI has a tuple or array input (`tuple_inputs=0 array_inputs=0` for all six carriers; 69 ABI functions, one per REA row); REA's inferred vocabulary is only `{address: 16, uint256: 44}` plus empty; no candidate uses an alias spelling (`uint`, `int`, `byte`, `address payable`: 0 of 344) or spaces. 18 candidates carry inline tuples and 32 carry arrays, but both sides of every comparison are elementary types, so canonicalisation cannot change a verdict; the counts do not depend on the resolver's string-equality shortcut (observation). Side effect: my canonical ABI signature hashes (own Keccak) to exactly the REA selector on all 69 rows (`rows_without_abi_signature: 0`), so the ABI↔REA linkage is confirmed, not assumed.
- **Saved-response integrity — holds.** Re-hashing every file listed in each `db/manifest.json`: 138 listed responses, 138 sha256 equal, 0 mismatching, 0 missing, 0 unlisted files in the six `db/` directories, 0 non-200 statuses; every 4byte page has `next: null` and `count == len(results)` (69/69), so no pagination was truncated; every openchain response has `ok: true` (69/69); `filtered` values are `False` 69 / `True` 147 (none missing) (observation).
- **Why the "no name" buckets have their size.** Consistent 4byte candidates per row: 0 on 18 rows, 1 on 48, 2 on 3 → rule 2 names 48, leaves 21 (18 with none, 3 ambiguous). Unfiltered openchain candidates: 0 on 7 rows (the 7 rows with no candidate at all), 1 on 55, 2 on 7 → rule 4 names 55, leaves 14. Unfiltered **and** consistent: 0 on 17, 1 on 49, 2 on 3 → rule 5 names 49, leaves 20. Every row with any openchain candidate has ≥1 unfiltered candidate, so rule 3 never names a filtered candidate (observation).

## 3. Other numeric claims in the entry, re-derived independently — all hold

Command: `python3 -I -B extra_checks.py out/my-tally.json` (exit 0, 10:56Z), same rows.

| entry claim | my number | verdict |
|---|---|---|
| REA inferred arguments differ from the ABI on 12 of 69 rows (11 Vyper, 1 carrierb `note`) | 12 of 69 (stewardtoken 8, carrierv 3, carrierb 1: `3efdef66` `uint256,uint256` vs `note(bytes32,uint256)`) | holds |
| 21 of the 31 distinct rule-5 names had openchain return a single candidate | 21 of 31 (30 of 31 had exactly one *unfiltered* candidate) | holds |
| `filtered=false` let through 4 wrong candidates out of 40 distinct unfiltered ones | 40 unfiltered candidates over 43 distinct selectors, 4 wrong (`40c10f19`, `2e1a7d4d`, `d0e30db0`, `6e8efde2`) | holds |
| `hasVerifiedContract` true on 92 candidate rows that are not the ABI name | 153 rows with the flag true, 92 not the ABI name | holds |
| a rule also requiring `hasVerifiedContract=true` scored 52 of 69 named, none wrong | 52 named, 52 right, 0 wrong (sole unfiltered + argument-consistent + flag true) | holds |

## 4. The one caveat: the bracketed (43-selector) numbers are dedup-order dependent

The published distinct-selector numbers come from first-occurrence dedup in `carriers.tsv` order. My scorer also computes a carrier-agnostic ("unanimous") variant; exactly one cell moves.

| naming rule (43 distinct) | published / first-occurrence | unanimous across carriers |
|---|---|---|
| first 4byte.directory result | 34 / 22 / 12 / 9 | 34 / 22 / 12 / 9 |
| the only 4byte candidate whose parameter list matches REA | 29 / 29 / 0 / 14 | **29 / 28 / 1 / 14** |
| first openchain result | 37 / 36 / 1 / 6 | 37 / 36 / 1 / 6 |
| the only openchain candidate with `filtered=false` | 34 / 33 / 1 / 9 | 34 / 33 / 1 / 9 |
| the only `filtered=false` candidate whose parameter list matches REA | 31 / 31 / 0 / 12 | 31 / 31 / 0 / 12 |

Cause (observation): 10 (selector, rule) pairs differ across carriers — `095ea7b3`, `23b872dd`, `70a08231`, `a9059cbb`, `27e235e3` — because REA's inferred argument list differs per carrier and the two argument-dependent rules depend on it. Example `a9059cbb`: rv2token and kdxtoken infer `address,uint256` → `transfer(address,uint256)` (right); stewardtoken (Vyper) infers `uint256,uint256` → `workMyDirefulOwner(uint256,uint256)` (wrong); the published `wrong: 0` keeps rv2token's row. The 32 selector+database copies present in more than one carrier directory are **byte-identical** across carriers (0 of 32 differ), so the difference comes only from REA's inference, never from a different snapshot. **Verdict: could-not-evaluate as stated** — a per-selector "right/wrong" for the argument-dependent rules is not scope-free while one selector has different REA inferences per carrier; the published number is a true reading of one defined scope, but the entry does not name that scope. Recommendation: label the bracketed column "first occurrence".

## 5. Entry error-pattern examples, re-derived — all confirmed

From `out/my-tally.json` (observation): `carrierv/6e8efde2` — sole openchain candidate `hasStreamed(address)`, `filtered=false`, args-mismatch against REA `uint256` → rules 3 and 4 name it (wrong), rule 5 gives no name. `carrierv` and `vaultb-opt200` `2e1a7d4d` — two unfiltered consistent candidates `withdraw(uint256)` and `OwnerTransferV7b711143(uint256)` → rules 4 and 5 give no name, rule 3 names `withdraw(uint256)` (right). `stewardtoken/a9059cbb` — REA inferred `uint256,uint256` → the 4byte parameter-list rule returns `workMyDirefulOwner(uint256,uint256)` (wrong) and the openchain rule returns nothing (its only unfiltered candidate `transfer(address,uint256)` is args-mismatch). 6 distinct selectors / 7 rows have no candidate in either database, including `fee_of(uint256,uint256)` (`0c751377`) and `note(bytes32,uint256)` (`3efdef66`).

## Result summary

| attack | verdict |
|---|---|
| five naming-rule counts, 69-row and 43-distinct scopes | **holds** — exact match on both |
| row-level labels / candidate order / flags / ABI truth vs published analyze files | **holds** — 0 differences over 69 rows |
| own Keccak + own ABI canonicalisation | **holds** — 0 label differences over 344 candidates |
| saved-response integrity (138 responses) | **holds** |
| five further numeric claims in the entry (§3), and the three error-pattern examples | **holds** |
| 43-selector table read without a dedup rule | **could-not-evaluate** — one cell moves (29/29/0 → 29/28/1); published number is first-occurrence-specific |

## Files changed

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-25/a3/w1/C2IndependentTally.md` (new). No lane corpus, tool, Git index or jj state touched; the entry's Markdown was not edited (lane bounds), so §1's table is offered for the L1 to place beside the entry's table.

## Artifacts (seat dir, sha256)

- `independent_tally.py` `524b4bb952f52212a13674791ae1c401c437fbf7e1f6ce968e07b4b79df3b621` (the scorer), `compare.py` `8568a678b4b94ea64ce6fa7364b600a419c75986bce03be72e20077530e07cfa` (diff vs published evidence), `extra_checks.py` `37f7a54903f40976ba3a08f103818de2aeda85ee64104e68955a1ba5accda076` (§3 re-derivations).
- `out/my-tally.json` `c92bbf457419f7dbfd0670f763c2b2fd1cafd5ebae84b3314a6ba9d6f0922275` (69 rows, every candidate, label and rule output), `out/my-table.md` `aba9df42b8c6ce3fd701eb721b7626f3d6179098455dbbcd1cba606b12ed82ac` (the tables above), `out/compare.json` `91695c5f64f4043530eb5c820181ee34cbf8d7dfdc4963050fc06f0b3c5f19e8` (machine diff).
- `out/stdout.json` `c3f66e36a0c99058245aabfff541bdf7eacc80810d1fb31be0f068ba85bce5d8`, `out/selftest.txt` `a6880dcb865bafe0799884e38503b897b59fb265b2dde3bf73c4f5c3d10233f2`, `out/compare-stdout.txt` `8408e934acc1bbf91b83f9b77309efa476bdfb55046204bdf88c543014245b55`, `out/extra_checks.txt` `248536e65faf678b6abfff40f22d5b65253c086953c93f82acadc6217473520b` — captured stdout. No tools installed or upgraded (python3 stdlib only; this seat made no network calls).

## Risks, limits, blockers

- The lane's per-lookup evidence is a 2026-10-22 snapshot; my verdicts cover that snapshot only. My scorer trusts the saved responses as "what the servers returned"; it cannot verify the servers.
- The entry was edited in the working tree during this wave (mtime 07:55:05Z at my last check); §1 compares against that text and the 10:58Z gate re-parsed it. If the table changes again, rerun `independent_tally.py` (deterministic, offline).
- The distinct-selector ambiguity in §4 is a scope question for the L1, not a numeric error.
- No blockers. Every command above ran in this seat and every number quoted is from its output.
