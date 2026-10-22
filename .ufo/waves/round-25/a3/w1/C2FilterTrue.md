# C2 openchain `filter=true`: server-side filter vs the local `filtered=false` subset

Seat KaidokuR25a3.C2FilterTrue. Round 25 attempt 3, wave 1. Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin, read-only except this report. Network use: public signature-database lookups only (never a target).

## What I attacked

The entry's Limits bullet: "openchain responses were requested with `filter=false` and the rule reads the per-match `filtered` flag; a `filter=true` request was not saved, so its server-side behaviour is not measured here." Claim under test: a server-side `filter=true` request returns the same candidate set as the local `filtered=false` subset of the saved `filter=false` responses, so rules 4 and 5 keep their counts.

## Verdict

**holds (observation).** For all 43 distinct selectors, the `filter=true` response returned exactly the local `filtered=false` subset: same members, same order, same count, 0 differences. Rules 4 and 5 keep their counts exactly (per carrier rows 55/54/1/14 and 49/49/0/20; distinct selectors 34/33/1/9 and 31/31/0/12), and 0 of 69 carrier rows change the name either rule returns. The server filter removes only entries whose own `filtered` flag is true; it does not drop `hasVerifiedContract=false` entries.

## Method

`https://api.openchain.xyz/signature-database/v1/lookup?function=0x<sel>&filter=true`, one request per distinct selector found in `corpus/evidence/round-25/a2/c2/*/db/openchain-*.json`, 1.2 s apart, all HTTP 200, 2026-10-22T10:44:14Z to 10:45:19Z. Raw body, UTC time and sha256 saved in `<seat>/filtertrue/manifest.json`. Command `python3 -I -B <seat>/fetch_filtertrue.py`, exit 0, stdout `{"selectors": 43, "requests": 43, "out": ".../filtertrue"}`. Seat request budget: 48 to api.openchain.xyz (43 + 5 stability re-fetches), 1 to api.4byte.sourcify.dev; limit 120 per seat.

## Acceptance

1. **Selectors where server-side `filter=true` equals the local `filtered=false` subset: 43 of 43.** Set equality, order equality and unfiltered-count equality hold for every selector; `set_different`, `order_different` and `unfiltered_count_different` are all empty.
2. **Differences: none in the returned candidate set.** The only differences are in the *total* candidate count, and they are the point of the server filter: for 10 selectors the `filter=false` response held extra junk entries that `filter=true` removed (147 entries over the 69 lane copies): `06fdde03, 095ea7b3, 18160ddd, 23b872dd, 313ce567, 70a08231, 8da5cb5b, 95d89b41, a9059cbb, dd62ed3e`. Those 10 are exactly the selectors whose two bodies differ; the other 33 bodies are byte-identical between `filter=false` and `filter=true`. All 6 no-candidate selectors (`0c751377, 3efdef66, 875194ac, cee38a15, d869f754, e0749a6a`) answer with JSON `null` under both `filter=false` and `filter=true`, byte-identical.
3. **Would rule 4/5 counts change if computed from `filter=true` responses? No.** Per-row comparison over the 69 carrier rows: `rule_row_differences` and `row_level_set_mismatch` are both empty.

| scope | rule | from `filter=false` | from `filter=true` |
|---|---|---|---|
| 69 carrier rows | rule 4, sole `filtered=false` | named 55, right 54, wrong 1, no name 14 | named 55, right 54, wrong 1, no name 14 |
| 69 carrier rows | rule 5, sole `filtered=false` + args-consistent | named 49, right 49, wrong 0, no name 20 | named 49, right 49, wrong 0, no name 20 |
| 43 distinct selectors | rule 4 | named 34, right 33, wrong 1, no name 9 | named 34, right 33, wrong 1, no name 9 |
| 43 distinct selectors | rule 5 | named 31, right 31, wrong 0, no name 12 | named 31, right 31, wrong 0, no name 12 |

The `filter=false` column reproduces the committed `corpus/evidence/round-25/a3/c2/analyze/tally.json` (rule 4 55/54/1/14, rule 5 49/49/0/20, distinct 34/33/1/9 and 31/31/0/12), so both columns come from the same code path (the lane's own `tools/round-25/a2/resolve-selectors.py` `analyze` and `tools/round-25/a3/tally-resolution.py` rule semantics, imported unchanged) and differ only in the response directory.

## What the `filter=true` responses look like

- No `filter=true` response contained an entry with `filtered=true` (`filtertrue_has_filtered_true` is empty). Every returned match still carries `filtered:false` and a `hasVerifiedContract` flag.
- `filter=true` does **not** mean "verified only". The three selectors whose local unfiltered subset has a `hasVerifiedContract=false` member (`2e1a7d4d`, `40c10f19`, `d0e30db0`) returned both members under `filter=true`, e.g. `2e1a7d4d` -> `withdraw(uint256)` and `OwnerTransferV7b711143(uint256)`. [observation] The server filter is "drop the junk the database itself marks `filtered=true`", not a second, stricter filter. This is the same tie the sibling seat C2HasVerified breaks with the `hasVerifiedContract` flag.
- The first entry of the `filter=true` response equals the first entry of the `filter=false` response for all 69 rows, so the "first openchain result" row of the entry's table is also unchanged by the server filter (62/61/1/7 both ways).
- Stability: 5 selectors re-fetched later the same day returned byte-identical bodies (`70a08231`, `a9059cbb`, `2e1a7d4d`, `6e8efde2`, `3efdef66`).

## Source opened this round

- URL `https://api.4byte.sourcify.dev/api-docs/swagger.json`, accessed 2026-10-22, HTTP 200, sha256 `896d6a30b58d501f508f8d311da0c81cdd6d006ed66f3e371142794101fcc00b` (byte identical to the lane's saved copy `corpus/evidence/round-25/a3/sources/sourcify-4byte-swagger.json`, the copy cited by S076). Section `paths` > `/signature-database/v1/lookup` > `get` > `parameters` > `filter`: quote "Whether or not to filter out junk results". The same description appears for `/signature-database/v1/search` > `get` > `parameters` > `filter`.

## Limits and risks

- Measured on 43 distinct selectors of six lane-compiled carriers, one snapshot pair: `filter=false` at 08:28Z-08:30Z, `filter=true` at 10:44Z-10:45Z the same day. The two snapshots agree exactly on the unfiltered subset, so no drift was observed in that window; [inference] the equality is a property of the service's `filtered` flag, not a coincidence of one hour, but it is only measured on these 43 selectors.
- The junk the server removed was, on this corpus, exactly the set of entries carrying `filtered=true`. A selector whose rows mark a junk entry `filtered=false` would break the equality; none of the 43 does.
- **Nothing is committed to the lane corpus yet.** The `filter=true` bodies, the manifest and the comparison scripts live only in my seat directory, and the contract forbids me to write into `corpus/`. If the entry wants to claim the server-side behaviour, the L1 must integrate `<seat>/filtertrue/` (43 files + `manifest.json`) into the lane evidence and re-point the entry's Limits bullet at the saved `filter=true` responses. Until then the entry's existing wording stays true and this report is the only record.

## Commands and evidence (all exit 0, UTC 2026-10-22)

1. `10:44Z-10:45Z` `python3 -I -B <seat>/fetch_filtertrue.py`: 43 requests, 43 HTTP 200, exit 0.
2. `10:4xZ` `python3 -I -B <seat>/compare.py`: exit 0. Writes `<seat>/compare.json` and prints the integrity, difference and score blocks quoted above.
3. `10:4xZ` sha256 of all 138 saved lane `filter=false` responses against the six `db/manifest.json` files: 0 mismatches (`lane_filterfalse_sha256_mismatch` empty); sha256 of my 43 `filter=true` files against my manifest: 0 mismatches.
4. `10:5xZ` `curl` of the Sourcify OpenAPI file: HTTP 200, sha256 as quoted; stability re-fetch of 5 selectors: all HTTP 200, all byte-identical to the first fetch.

## Artifacts (seat dir /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2FilterTrue)

- `artifacts.sha256` 1f4c8da90fb0d3df1d98081f24d042912a1702829b35e8b1890c2ba788d48b20 (index of every file in the seat dir with its sha256 and size, 127 files: the 43 `filtertrue/openchain-*.json`, their `filtertrue/manifest.json`, the per-carrier `ft-<carrier>/` copies, the 5 `refetch/` bodies, `swagger.json`, the scripts and the JSON results)
- `fetch_filtertrue.py` a3b63f6a6c65952659ed292605339375458ccf2ae029e574079f44665ab86457
- `compare.py` 05ae238dbbf07fa063e25d994f04ea449680fc6f4b33ce8ef0458a92af42c96f
- `compare.json` e2be83f578565a809df36d2670853e544c612e5d3c46552fc2d2184ce317e194
- `selectors.tsv` 32da3b9948351ab60173c28e83a6a08429ebab4a797207a3f224739494aac916 (per-selector table: total candidates, local unfiltered, `filter=true` returned, set/order equality, junk removed, returned names)
- `filtertrue/manifest.json` a6eb0336f108b87e563b7fab95981c105936ce97365c216d9b5de481496fed88
- `swagger.json` 896d6a30b58d501f508f8d311da0c81cdd6d006ed66f3e371142794101fcc00b
- `fetch.stdout` d6320b8cc054e252030b259d584ed187d72ef4c5ffbc4e3377abeaac4d39842f, `fetch.stderr` e0d15b91a37f57716a7f7f72b1c79ad4f6bd5d5f0a47379ffd97d57190dfee91, `probe-70a08231.json` 2116b06d1609e2afec12862fe823db5962f8b6efb069e662655e491f410e1ad5 (pre-flight single request, byte-identical to the later fetch of the same selector)

Tooling: nothing installed; system `python3` 3.14.8 standard library only (`urllib.request`), plus `curl` and `sha256sum`. Report: .ufo/waves/round-25/a3/w1/C2FilterTrue.md
