# R29 independent selector-preseen audit

## Verdict

- **R29-C1 — “none of the 152 selectors appears anywhere in the lane at base”: HOLDS.** Whole-blob search found **0/152** selectors in any searched spelling or raw-byte form.
- **R29-C2 — “none of the 178 selectors has an OpenChain response at base”: HOLDS.** There are **0/178** matches among `result.function` keys and no matching `openchain-<selector>.json` filenames. No C2 selector spelling/raw-byte match occurs in any of the 529 response-shaped JSON blobs.
- Do not interpret C2’s response-specific `overlap=0` as global selector absence: whole-tree search found **26/178** C2 selectors in **937 selector/path/spelling rows** outside response-shaped JSON. The full rows are in the hit artifact below. Thus the response claim holds; a stronger C2 “appears nowhere” claim would not.

## Method and counts

Used the C1 inventory at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-29/c1/heldout.tsv` (152 unique selectors; SHA-256 `2db9e658d5076771ee249f9d027938103edb7933201abb4b391f1053323dca23`) and the C2 inventory at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-29/c2/selectors.tsv` (178 unique selectors; SHA-256 `3a93f7837accb9acd66874707922317d9a8e0f8afb0c9cd87ee79f3d9fa15b5d`). The audit did not read or execute `tools/round-29/preseen.py`.

For base `bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47`, the audit enumerated the complete recursive Git tree using `git ls-tree -r -z --full-tree`, then read **all 20,664 blob objects** through `git cat-file --batch`. It searched blob bytes without file-type filtering, so binary blobs were included. Per selector, the needles were bare lowercase hex, bare uppercase hex, `0x` + lowercase hex, `0x` + uppercase hex, and the four raw bytes from the hex value. Identical lower/upper needles are grouped in the output. JSON detection parsed every blob as UTF-8 JSON where possible and selected an object-shaped `result.function`; it separately enumerated every basename matching `openchain-*.json` or `4byte-*.json`.

| Set | Selectors | Any whole-blob text/raw hits | No whole-blob hit | OpenChain `result.function` key overlap | `openchain-<selector>.json` filename overlap |
|---|---:|---:|---:|---:|---:|
| C1 | 152 | 0 | 152 | — | — |
| C2 | 178 | 26 | 152 | 0 | 0 |

The C2 whole-blob hit selectors are: `01ffc9a7`, `081812fc`, `09b81346`, `0d0f30c6`, `0dfe1681`, `1a686502`, `3644e515`, `39509351`, `415565b0`, `41973cd9`, `5f575529`, `60806040`, `60a06040`, `60c06040`, `60e06040`, `61010060`, `7c025200`, `89035730`, `8abf6077`, `9a2b8115`, `a457c2d7`, `c45a0155`, `d55ec697`, `e7acab24`, `fc6f7865`, `fd9f1e10`. Every hit’s selector, absolute path, spelling, occurrence count, offsets, Git object ID and mode is in `hits.jsonl` (937 rows). Example rows:

- `01ffc9a7` — `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c1/CR-1/evidence/Cr1Sample.sol` — `0x-prefixed lowercase hex`
- `01ffc9a7` — same path — `bare lowercase hex`

The tree contains 5,610 parseable JSON blobs, of which **529** have the `result.function` object shape. The filename scan found **529** `openchain-*.json` files and **256** `4byte-*.json` files (**785 total**); the 529 response-shape paths exactly equal the 529 OpenChain-named paths. The complete absolute-path lists and `result.function` keys are in `summary.json`.

## Evidence record

1. **Producing command:** `python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPreseenIndependent/audit.py` (internally ran the two read-only Git commands stated above). **UTC:** `2026-10-22T20:22:20+00:00` through `2026-10-22T20:24:30+00:00`. **Exit:** `0` **[INFERENCE]** — the background runner did not expose a numeric status, but the script emitted its complete summary and output path with no exception/error; its normal return is zero. Exact summary excerpt:

   ```json
   "blobs_cat_file_read": 20664,
   "matching_counts": {
     "C1": {"distinct_selectors_with_any_spelling_or_raw_hit": 0, "distinct_selectors_without_hits": 152, "selector_set_size": 152},
     "C2": {"distinct_selectors_with_any_spelling_or_raw_hit": 26, "distinct_selectors_without_hits": 152, "selector_path_spelling_rows": 937, "selector_set_size": 178}
   },
   "C2_result_function_selector_key_hits": 0,
   "openchain_response_shape_json_blobs_count": 529,
   "openchain_or_4byte_named_json_blobs_count": 785
   ```

2. **OpenChain filename cross-check:** Python post-processing of `summary.json` plus the C2 TSV compared all 178 normalized selector IDs to every OpenChain filename and recorded the response-key list. **UTC:** `2026-10-22T20:28:35+00:00`. Exact output: `{"C2_result_function_key_hits": [], "C2_selector_count": 178, "openchain_filename_selector_hits": [], "openchain_named_json_file_count": 529}`. **Exit:** `0` **[INFERENCE]** (normal completion, no error).

3. **Path materialization:** `python3 /fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPreseenIndependent/materialize-absolute-paths.py; status=$?; printf 'exit_code=%d\\n' "$status"; exit "$status"`. **UTC:** `2026-10-22T20:27:49+00:00`. Exact output included `"openchain_response_shape_json_blobs": 529`, `"openchain_named_json_files": 529`, `"openchain_shape_paths_equal_names": true`, `"4byte_named_json_files": 256`, `"C2_selector_spelling_or_raw_hit_rows_in_openchain_response_shape_blobs": 0`, and `exit_code=0` (**observed**).

4. **Artifact hashes:** `sha256sum` output recorded at `2026-10-22T20:27:55Z`; the command completed normally (exit `0` **[INFERENCE]**):
   - `3dfd484416331cb4722afa2d65759a46b4692f047d5f2f07cc94675848252785` — `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPreseenIndependent/audit.py`
   - `ef3ddcc70ef95d16e093ba96467af5658272a77eb89b76e7c5eef0ac1cefd63d` — `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPreseenIndependent/materialize-absolute-paths.py`
   - `fcd5290cae65bd44f4018c176724fa40909fbac64af974707e0bedc7fcee791d` — `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPreseenIndependent/summary.json`
   - `e21827b656dfb6dd5a3df002fc1fbcfe8de04ade16543b6f278d8067eaed32fd` — `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ExecPreseenIndependent/hits.jsonl` (**937 rows**)

## Risks and blockers

- The 26 C2 broad-search hits mean only the response-specific C2 claim is supported; they contradict a broader claim of no C2 selector value anywhere in the lane.
- Results are scoped to blobs committed in the specified base tree and the supplied C1/C2 selector inventories. No external sources, network lookups, REA, or tool installs were used. No blocker encountered.
