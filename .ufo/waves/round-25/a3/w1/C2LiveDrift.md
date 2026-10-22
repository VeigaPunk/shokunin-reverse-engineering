# R25 a3 wave 1 — C2 live drift of the saved lookups (seat C2LiveDrift)

Date: 2026-10-22. Lane: /home/vgpnk/Projects/shokunin/kaidoku-shokunin, HEAD `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` (`git rev-parse HEAD`, exit 0). Lane read-only: this seat wrote no lane file except this report; the modified lane files shown by `git status --porcelain` (`SCORECARD.md`, `corpus/SOURCES.md`, `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`, `corpus/lessons/round-25.md`) pre-date this seat's work and are not mine.

## Verdict

| Attack | Result |
|---|---|
| Re-query of the 15 assigned selectors: candidate sets drifted? | **holds (no drift)** — 0 of 15 changed, byte-identical responses |
| Re-query of all 43 distinct saved selectors (superset): candidate sets drifted? | **holds (no drift)** — 0 of 43 changed |
| Any of the five naming rules in the entry changes today? | **holds (no change)** — replay of the lane's own tally over fresh lookups reproduces every number |

## Method

`tools/round-25/a2/resolve-selectors.py fetch` logic re-implemented in the seat's own script (`live-drift.py`, stdlib only) so the fetch is independent of the lane tool: 4byte.directory `GET /api/v1/signatures/?hex_signature=0x<sel>` with all pages followed via `next`, and openchain `GET /signature-database/v1/lookup?function=0x<sel>&filter=false`, both with the same User-Agent as the lane fetch. Raw bodies saved byte-for-byte with UTC time and sha256 in `fresh/manifest.json`.

Assigned 15 (all present in the saved `db/` dirs, as required): `a9059cbb`, `6e8efde2`, `2e1a7d4d`, `0c751377`, `3efdef66`, `095ea7b3`, `23b872dd`, `70a08231`, `18160ddd`, `313ce567`, `dd62ed3e`, `06fdde03`, `40c10f19`, `d0e30db0`, `9c421eb5`. Because the acceptance asks whether *any rule outcome* changes, and the entry's rules are scored over all 69 carrier rows / 43 distinct selectors, I extended the same fetch to the remaining 28 distinct selectors (all 43 covered). Host politeness: 1.1 s between requests to one host; 90 requests total to lookup hosts, under the 120-per-seat cap.

## Per-selector drift table

`fb` = 4byte.directory candidate count, `oc` = openchain candidate count, `unf` = openchain candidates with `filtered=false`. "saved" = 2026-10-22T08:28Z–08:30Z snapshot in the lane; "live" = 2026-10-22T10:43:44Z–10:48:21Z re-query. "identical" means the full ordered candidate list is equal, which for every row below also means the raw HTTP body is byte-identical.

| selector | set | carrier(s) | fb saved→live | oc saved→live | unf saved→live | first 4byte saved→live | first openchain saved→live | drift |
|---|---|---|---|---|---|---|---|---|
| a9059cbb | A15 | kdxtoken,rv2token,stewardtoken | 6→6 | 13→13 | 1→1 | workMyDirefulOwner(uint256,uint256) → same | transfer(address,uint256) → same | none |
| 6e8efde2 | A15 | carrierv | 0→0 | 1→1 | 1→1 | (none) | hasStreamed(address) → same | none |
| 2e1a7d4d | A15 | carrierv,vaultb-opt200 | 2→2 | 2→2 | 2→2 | OwnerTransferV7b711143(uint256) → same | withdraw(uint256) → same | none |
| 0c751377 | A15 | carrierv,stewardtoken | 0→0 | 0→0 | 0→0 | (none) | (none) | none |
| 3efdef66 | A15 | carrierb | 0→0 | 0→0 | 0→0 | (none) | (none) | none |
| 095ea7b3 | A15 | kdxtoken,rv2token,stewardtoken | 4→4 | 8→8 | 1→1 | _SIMONdotBLACK_(int8[],int224[],int256,int64,uint248[]) → same | approve(address,uint256) → same | none |
| 23b872dd | A15 | kdxtoken,rv2token,stewardtoken | 5→5 | 10→10 | 1→1 | func_nZHTch(...) → same | transferFrom(address,address,uint256) → same | none |
| 70a08231 | A15 | kdxtoken,rv2token,stewardtoken | 4→4 | 13→13 | 1→1 | watch_tg_invmru_119a5a98(...) → same | balanceOf(address) → same | none |
| 18160ddd | A15 | kdxtoken,rv2token,stewardtoken | 3→3 | 4→4 | 1→1 | watch_tg_invmru_ae5c248(...) → same | totalSupply() → same | none |
| 313ce567 | A15 | stewardtoken | 5→5 | 6→6 | 1→1 | watch_tg_invmru_5c94e13(bool) → same | decimals() → same | none |
| dd62ed3e | A15 | stewardtoken | 4→4 | 5→5 | 1→1 | join_tg_invmru_haha_5911067(...) → same | allowance(address,address) → same | none |
| 06fdde03 | A15 | stewardtoken | 3→3 | 4→4 | 1→1 | transfer_attention_tg_invmru_6e7aa58(...) → same | name() → same | none |
| 40c10f19 | A15 | kdxtoken,stewardtoken | 2→2 | 2→2 | 2→2 | cat642998653(address,uint256) → same | mint(address,uint256) → same | none |
| d0e30db0 | A15 | carrierv,stewardtoken,vaultb-opt200 | 1→1 | 2→2 | 2→2 | deposit() → same | deposit() → same | none |
| 9c421eb5 | A15 | vaultb-opt200 | 0→0 | 1→1 | 1→1 | (none) | feeOn(uint256) → same | none |
| 0776076f,1aa02d59,24a9d853,27e235e3,3d96e276,3f4ba83a,410673e5,4643c56b,48a3ef5c,51f91066,5c975abb,637eea19,69fe0e2d,6ea056a9,7d882097,8456cb59,875194ac,8da5cb5b,95d89b41,b144adfb,ca1d209d,cbf9fe5f,cee38a15,d5d44d80,d869f754,db006a75,e0749a6a,e7ee6ad6 | extra 28 | (all six carriers) | unchanged | unchanged | unchanged | unchanged | unchanged | none |

Full machine-readable table (all 43 selectors, both candidate lists verbatim) in `diff.json`; per-file sha256 comparison in `sha-compare-all.json`.

## Raw-response evidence

- Fetch command: `TMPDIR=$PWD/tmp python3 -I -B live-drift.py fetch` then `… fetchmissing`; each `get()` records HTTP status, UTC and sha256 of the raw body in `fresh/manifest.json` (86 entries, all status 200, UTC 2026-10-22T10:43:44Z–10:48:21Z). Exit 0 for both runs.
- Fresh manifest self-consistency: recomputed sha256 of every saved body equals its manifest entry — `True` (exit 0).
- Saved manifest self-consistency (lane, re-checked): every one of the 138 saved response files hashes to its lane manifest entry — mismatches `[]` (exit 0).
- Byte comparison saved vs live: **138 saved-file/live-file pairs compared, 138 byte-identical, 0 differing.** Independent spot check with `cmp` (exit 0, no output): `openchain-a9059cbb.json`, `4byte-a9059cbb-p0.json`, `openchain-0c751377.json`.
- Pagination: no 4byte page returned a `next` link in either snapshot, so the one-page saved files are complete candidate sets (not a truncation) — `4byte pages with next (pagination): []`.
- Liveness proof the lookups were really served now, not cached locally: a repeat `GET` of the openchain `0xa9059cbb` lookup returned HTTP 200 with header `Date: Thu, 22 Oct 2026 10:45:57 GMT` (host clock agrees with the seat's `date -u` = `2026-10-22T10:45:58Z`) and body sha256 `f20961e3…302bd43`, equal to the fresh manifest's sha256 for that file. The 4byte repeat returned `Date: Thu, 22 Oct 2026 10:45:58 GMT`, body sha256 `12aefaec…79ba9bce6`, also equal to the fresh manifest.
- Opened pages (plain HTTP, 2026-10-22): `https://www.4byte.directory/api/v1/signatures/?hex_signature=0xa9059cbb` — section "results[0]": quote "workMyDirefulOwner(uint256,uint256)". `https://api.openchain.xyz/signature-database/v1/lookup?function=0xa9059cbb&filter=false` — section "result.function.0xa9059cbb[0]": quote "transfer(address,uint256)". `https://docs.openchain.xyz/signature-database/api-endpoints` — **unopened**: connect timed out (URLError, exit 1), so it supports nothing here and the entry's S076 wording is untested by this seat.
- The live openchain body for the collision case `0x6e8efde2` is still exactly `{"name": "hasStreamed(address)", "filtered": false, "hasVerifiedContract": true}` — the wrong-but-sole candidate the entry describes is unchanged.

## Do any rule outcomes in the entry change today?

**No (observation, exit 0).** Replay: `tools/round-25/a3/tally-resolution.py --root <staged root with fresh db dirs> --out analyze-fresh`, where the staged root (`mergedroot/`) symlinks the lane `tools/` and `.ufo/` (compiler ABIs) and carries per-carrier `db/` dirs in which the fresh responses replace the saved ones for all 43 selectors. Every selector has a fresh body, so the whole 69-row tally runs on live data only. Comparison against the same tool run over the untouched lane (`--root <lane>`, `analyze-saved/`):

| tally section | saved vs live |
|---|---|
| `per_carrier_rows` (69 rows) | identical (True) |
| `distinct_selectors` (43) | identical (True) |
| `no_candidate_selectors` | identical (True) |
| `wrong_names` (every wrong rule hit, with carrier/selector/rule/returned/abi) | identical (True) |
| per-row analysis of all 6 carriers, 69 rows | 0 differing rows, 0 differing summaries |

Live per-row rule counts (same as saved and as the entry's table): fourbyte_first 59 named / 33 right / 26 wrong; fourbyte_sole_args_consistent 48 / 47 / 1; openchain_first 62 / 61 / 1; openchain_sole_unfiltered 55 / 54 / 1; openchain_sole_unfiltered_args_consistent 49 / 49 / 0; `no_candidate_in_either_database` 7 rows; `keccak_mismatch_candidates` 0.

Entry claims re-checked against live data and still true (observation): the 6 distinct selectors with no candidate in either database are still exactly `0c751377` (fee_of), `3efdef66` (note), `875194ac`, `cee38a15`, `d869f754`, `e0749a6a`; `0x6e8efde2` is still a real collision whose only openchain candidate is the wrong `hasStreamed(address)`; `0x2e1a7d4d` still returns two unfiltered names with identical parameter lists, so the rule gives no name; `0xa9059cbb` still has `workMyDirefulOwner(uint256,uint256)` as the first 4byte result and still makes the 4byte parameter-list rule pick the junk name on the Vyper row; 4byte still lists higher ids first (ids 1111734, 844280, 313067, 161159, 31780, 145 for `0xa9059cbb`).

## Limits and residual risk

- The drift window measured is the ~2 h 15 min between the saved snapshot (08:28Z–08:30Z) and this re-query (10:43Z–10:48Z) on 2026-10-22. Both databases take public submissions, so drift at a later hour or after new submissions is not excluded; the entry's own "one snapshot" limit still stands.
- The entry's `no_candidate` list (6 selectors) was re-derived from the fresh data and matches; but 4 of those 6 selectors were outside my assigned 15 and are covered only by the extension fetch.
- The freshness check is a repeat of two URLs, not of all 86; the per-file `Date` header was captured only for those two, so "the responses were served today" rests on the manifest UTC plus those two live headers.
- `docs.openchain.xyz` was unreachable from this host (timeout), so no independent re-read of the openchain filter/flag documentation was possible; the `filtered` and `hasVerifiedContract` semantics are used exactly as the lane's saved data and the entry define them.
- The rule-outcome replay reuses the lane's own `tally-resolution.py` and `resolve-selectors.py`; a bug shared by both the saved tally and my replay would not show up as drift. The independent check on the database side is the byte comparison, which is tool-independent.

## Artifacts (scratch, sha256)

- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/live-drift.py — `f6a2f38fbe56dfe7913ae369888c56d04610708f054b9323985dfe37cff40a7a`
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/fresh/manifest.json — `adf75227ea0ca770b5ef2bef3690beb4be6ff65869fe7b5684e7ea0f2faf89f8` (86 raw bodies, each hashed, live in `fresh/`)
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/diff.json — `060146cbd15f0b4ce994d216e46e832c0bc23195df84b47a2e7910731a4b1c68`
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/sha-compare-all.json — `4eb595e25ead715b174659be58307a5ea1c68a134d282b182334cb96fa4cc67d`
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/analyze-fresh/tally.json — `479bc13ea4c2139289808a54c47321c83c3daafffaad5de4b06c00ac840b40dc`
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/analyze-fresh/carrierv.json — `bbcf5f83ed0773acef528e0c34b9cf20b9d1a46ca7c5681f9bd6395c0c9bb187`
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/analyze-fresh/kdxtoken.json — `233f1260115766dde6818a88eb102a8e427badfc10c783b0079693d46aff2f8b`
- /fast/scratch/hyaku/kaidoku-r25-a3/seats/C2LiveDrift/analyze-saved/tally.json — replay of the untouched lane (baseline for the comparison)

Tooling: none installed or upgraded. Existing `python3` 3.14.8 used; no pacman, `uv`, `npx` or REA invocation (no REA needed — this seat measures the lookup databases, not REA inference). No git writes, no `jj` command, no lane mutation.

Report: .ufo/waves/round-25/a3/w1/C2LiveDrift.md
