# C2 entry numbers — verification (KaidokuR25a3.C2EntryNumbers, round 25 attempt 3, wave 1)

Target: every number in `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`.
Sources used: `corpus/evidence/round-25/a3/c2/analyze/tally.json`, the saved
`corpus/evidence/round-25/a2/c2/<carrier>/db/` files, and the resolver selftest.
Verified 2026-10-22, window ending 10:45:12Z.

## Number-by-number verdicts

| # | Number in entry | Source checked | Match |
|---|---|---|---|
| 1 | 69 selector rows | `tally.json` `.per_carrier_rows.selector_rows` = 69; disk: lookup pairs per carrier 5+6+13+8+22+15 = 69 | yes |
| 2 | 43 distinct selectors | `tally.json` `.distinct_selectors.selector_rows` = 43; independent union of selector hex in saved `openchain-*.json` filenames = 43 | yes |
| 3 | 138 saved responses | 138 response JSONs on disk (10+12+26+16+44+30, manifest excluded); 138 manifest entries | yes |
| 4 | table row 1: 59 / 33 / 26 / 10 | `.per_carrier_rows.rules.fourbyte_first` = named 59, right 33, wrong 26, no_name 10 | yes |
| 5 | table row 2: 48 / 47 / 1 / 21 | `.fourbyte_sole_args_consistent` = 48 / 47 / 1 / 21 | yes |
| 6 | table row 3: 62 / 61 / 1 / 7 | `.openchain_first` = 62 / 61 / 1 / 7 | yes |
| 7 | table row 4: 55 / 54 / 1 / 14 | `.openchain_sole_unfiltered` = 55 / 54 / 1 / 14 | yes |
| 8 | table row 5: 49 / 49 / 0 / 20 | `.openchain_sole_unfiltered_args_consistent` = 49 / 49 / 0 / 20 | yes |
| 9 | 6 distinct selectors without candidates | `.distinct_selectors.no_candidate_in_either_database` = 6; `.no_candidate_selectors` has 6 entries | yes |
| 10 | 7 rows without candidates | `.per_carrier_rows.no_candidate_in_either_database` = 7 | yes |
| 11 | 0 keccak mismatches | `.per_carrier_rows.keccak_mismatch_candidates` = 0 and `.distinct_selectors…` = 0; reproduced by recheck run | yes |
| 12 | 9/9 selftest checks | `resolve-selectors.py selftest`: 9 checks, all `"ok": true`, top-level `"ok": true` | yes |

## Producing commands, excerpts, exit codes (all 2026-10-22, ≤ 10:45:12Z)

1. Selftest — `TMPDIR=…/C2EntryNumbers/tmp python3 -I -B tools/round-25/a2/resolve-selectors.py selftest`, exit 0.
   Excerpt: 9 check objects, e.g. `"check": "negative control: hashlib.sha3_256 is not Keccak-256", "got": "4b40e901", "want": "not a9059cbb", "ok": true`; last check `"known collision is labelled args-mismatch" … "ok": true`.
2. Recheck — `python3 -I -B tools/round-25/a3/tally-resolution.py --root <lane>` (no `--out`, so it writes nothing; script docstring lines 6–8 confirm), exit 0, stdout saved to
   `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2EntryNumbers/recheck-tally.json`
   (sha256 7e02dbbe048da684b217b5c535423db41938c41a9b4767d5f13359fb628ca2b7).
   `diff <(python3 -m json.tool recheck-tally.json) <(python3 -m json.tool tally.json)` → empty, `DIFF=CLEAN`. Observation: the committed tally is exactly reproducible offline from saved envelopes, saved lookups and compiler ABIs, which transitively re-verifies counts 1–2 and 4–11.
3. File counts — `find …/a2/c2/*/db -name '*.json' ! -name manifest.json`, exit 0:
   `rv2token 10, kdxtoken 12, vaultb-opt200 26, carrierb 16, stewardtoken 44, carrierv 30, TOTAL=138`.
4. Distinct selectors — union of hex in `openchain-*.json` filenames: `43`, exit 0.
5. Integrity — python re-hash of all 138 files against their manifests, exit 0:
   `manifest_entries=138 sha_ok=138 sha_bad=0 status200=138` → confirms "all HTTP 200, every sha256 re-checked equal to its manifest".

## Internal consistency of the table (observation)

named + no_name = 69 for all five rules (59+10, 48+21, 62+7, 55+14, 49+20); right + wrong = named for all five (33+26, 47+1, 61+1, 54+1, 49+0). Entry prose "named 49 of 69 rows with 0 wrong … 20 rows got no name" and "26 of its 59 names were wrong" match rows 8 and 4. `.wrong_names` length = 29 = 26+1+1+1+0 across rules. The two no-candidate examples the entry names, `fee_of(uint256,uint256)` (`0c751377`) and `note(bytes32,uint256)` (`3efdef66`), are the first two entries of `.no_candidate_selectors`.

## Verdict

Every number checked holds (12/12, with each verified against at least one source beyond the entry itself). No counterexample found.

## Residual risk and verification gaps

- All counts derive from the same saved snapshot (2026-10-22T08:28Z–08:30Z); the entry itself flags that later lookups can change them. I did not re-query either database.
- The distinct-selector count is corroborated by filenames (independent of tally code) but the 69-row cut (per-carrier duplication) was verified via tally.json plus the file-count sum, not by an independent ABI re-derivation; the recheck rerun exercises the tally script itself, so a shared bug in resolver `analyze` would not be caught by either. The 9/9 selftest and the Keccak/arg labels partially bound that.
- `find` printed one benign error for the glob `c2/*/db` matching the file `carriers.tsv` (not a directory); all six `db/` directories were still enumerated.

## Seat artifacts

- `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2EntryNumbers/recheck-tally.json` — sha256 7e02dbbe048da684b217b5c535423db41938c41a9b4767d5f13359fb628ca2b7
- `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2EntryNumbers/tmp/` — TMPDIR for isolated runs (empty after runs)
- No tools were installed or upgraded. No lane files were mutated; all lane access read-only.
