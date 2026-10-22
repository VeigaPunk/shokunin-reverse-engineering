# C2 version sensitivity — REA 6.7.0 vs the committed 6.5.0 envelopes (KaidokuR25a3.C2Rea67)

Target: does REA 6.7.0 change any selector, `inferred_arguments` or `inferred_state_mutability` on the six C2 carriers, and would any naming-rule outcome in `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` change? Lane access read-only; the only lane file written is this report. Work window 2026-10-22, 10:43:41Z–10:49:07Z.

## Verdict

- **Holds.** On all six carriers REA 6.7.0 returns the same 69 function rows as REA 6.5.0: same selector set, same `inferred_arguments`, same `inferred_state_mutability`, same `bytecode_offset` and `dispatch`. Zero differing fields (69/69 rows, six carriers); `raw_result` and `normalized_result` are identical objects under both versions.
- **No naming-rule outcome changes.** Re-running the lane's own resolver and tally over the 6.7.0 envelopes against the *same* saved 4byte.directory and openchain lookups reproduces the committed `corpus/evidence/round-25/a3/c2/analyze/tally.json` exactly: all five rule rows equal, `wrong_names` equal, `no_candidate_selectors` equal.
- **stewardtoken `0xa9059cbb` is unchanged and still wrong.** 6.7.0 still infers `uint256,uint256` for `transfer(address,uint256)`, so the entry's "wrong REA arguments pick the wrong name" error pattern stands verbatim under 6.7.0.
- **One version-sensitive detail, not a naming outcome:** the envelope `evidence_id` differs between 6.5.0 and 6.7.0 for every carrier although the analysis content is identical. Cause (observation, source-read): REA 6.7.0 changed `semanticProjection` in `dist/domain/evidence.js` so `relationship_coverage` is always in the hashed projection, while 6.5.0 omitted the key when it was `null`. Recomputing `sha256(canonical(semanticProjection))` under each rule reproduces both ids for all six carriers exactly. Consequence for the entry: its `verified-at` claim that "REA `rea-agents@6.5.0` envelopes replayed byte-equal" holds only for 6.5.0; a 6.7.0 replay is *not* byte-equal, but every analysis field and every naming outcome is.

## Per-carrier diff table

`args` = `inferred_arguments`, `mut` = `inferred_state_mutability`, `off` = `bytecode_offset`. "diff" = rows where any of args/mut/off/dispatch differ between 6.5.0 and 6.7.0. `evidence_id` truncated to 16 hex chars; full values are in the seat artifacts.

| carrier | rows 6.5.0 | rows 6.7.0 | selectors added/removed | args diff | mut diff | off/dispatch diff | `raw_result` identical | `evidence_id` 6.5.0 | `evidence_id` 6.7.0 |
|---|---|---|---|---|---|---|---|---|---|
| rv2token | 5 | 5 | none | 0 | 0 | 0 | yes | `ev_78769b9b5a7b901` | `ev_19d7d3cb29183523` |
| kdxtoken | 6 | 6 | none | 0 | 0 | 0 | yes | `ev_dbccef49e8903f3a` | `ev_e0f0c9185c3b7b7b` |
| vaultb-opt200 | 13 | 13 | none | 0 | 0 | 0 | yes | `ev_b58d82e0f563a5fe` | `ev_ae5aaee0b8ad1b9d` |
| carrierb | 8 | 8 | none | 0 | 0 | 0 | yes | `ev_61b29a8609cd791d` | `ev_861873b06acdcac7` |
| stewardtoken | 22 | 22 | none | 0 | 0 | 0 | yes | `ev_94dd707922226822` | `ev_b07b89717568e40b` |
| carrierv | 15 | 15 | none | 0 | 0 | 0 | yes | `ev_026e6cfaf2a67197` | `ev_62e1b9e6e4d254f3` |

Full 69-row value-by-value listing: `per-carrier-diff.txt` (sha256 `6f06cd98107de9b50a882c8e75400417414188ba7fbe935d601dbfce46eb0891`).

## The stewardtoken focus row (unchanged)

`0xa9059cbb` in both versions: `args` = `uint256,uint256`, `mut` = `payable`, `off` = 806, `dispatch` = `abi`. ABI truth `transfer(address,uint256)`. Rule outputs identical under 6.5.0 and 6.7.0: `fourbyte_first` → `workMyDirefulOwner(uint256,uint256)` (wrong), `fourbyte_sole_args_consistent` → `workMyDirefulOwner(uint256,uint256)` (wrong), `openchain_first` → `transfer(address,uint256)` (right), `openchain_sole_unfiltered` → `transfer(address,uint256)` (right), `openchain_sole_unfiltered_args_consistent` → `null` (no name). The entry's decision rule 2 still yields no leading candidate here, and the entry's "wrong REA arguments pick the wrong name" paragraph is unchanged under 6.7.0.

## Naming-rule tally under 6.7.0 (identical to the committed 6.5.0 table)

| naming rule | named | right | wrong | no name |
|---|---|---|---|---|
| first 4byte.directory result | 59 | 33 | 26 | 10 |
| the only 4byte candidate whose parameter list matches REA | 48 | 47 | 1 | 21 |
| first openchain result (`filter=false` order) | 62 | 61 | 1 | 7 |
| the only openchain candidate with `filtered=false` | 55 | 54 | 1 | 14 |
| the only `filtered=false` openchain candidate whose parameter list matches REA | 49 | 49 | 0 | 20 |

Per-carrier rows 69, distinct selectors 43, `no_candidate_in_either_database` 7 rows / 6 distinct, `keccak_mismatch_candidates` 0 — all identical to the committed `corpus/evidence/round-25/a3/c2/analyze/tally.json` (parsed comparison returned `True` for `per_carrier_rows`, `distinct_selectors`, `wrong_names`, `no_candidate_selectors`).

## Evidence

- `TMPDIR=<seat>/tmp npx -y rea-agents@6.7.0 inspect-evm-interface <carrier runtime.hex> hex --format json` — six runs, exit 0, UTC 10:43:47Z (stewardtoken) and 10:43:54Z (the other five), stderr empty (sha256 `e3b0c442…`, zero bytes). `npx -y rea-agents@6.7.0 --version` → `6.7.0`, exit 0.
- Same command with `rea-agents@6.5.0` — six runs, exit 0, UTC 10:44:01Z–10:44:03Z. Every 6.5.0 output is **byte-identical** to the committed lane envelope (`corpus/evidence/round-25/a2/c2/<carrier>/envelope.json`, sha256 equal for all six), so the comparison arm is anchored on the committed evidence, not on a fresh baseline.
- Determinism control: two further runs per version on stewardtoken (UTC 10:44:35Z / 10:44:36Z) gave identical sha256 within each version (6.7.0 `0ee7dfc9…`, 6.5.0 `1de20e96…`), so the `evidence_id` change is version-bound, not run noise.
- `python3 -I -B compare-rules.py --envelopes out67 --out out --tag rea670-final` and the same with `out65` — exit 0, UTC 10:49:06Z–10:49:07Z. Row-by-row comparison of the two 69-row rule tables: `total differing rows: 0`.
- End-to-end with the lane's own instrument: sandbox clone `git clone -q <lane> <seat>/clone` (HEAD `08c7a729`), the six envelopes replaced by the 6.7.0 outputs, then `python3 -I -B tools/round-25/a3/tally-resolution.py --root <clone> --out <seat>/out/tally-670-clone` — exit 0; its `tally.json` equals the committed tally on every compared section.
- Cause of the id change, source-read: `diff -u` of `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js` (6.5.0) against `~/.npm/_npx/a1722018f28f9df2/…` (6.7.0) shows the 6.7.0 projection always emitting `relationship_coverage`, 6.5.0 emitting it only when non-null. Recomputation: `sha256(canonical(projection_without_rc))` equals the 6.5.0 id and `sha256(canonical(projection_with_rc))` equals the 6.7.0 id for all six carriers (`match65: True`, `match67omit: False`, `match67inc: True` on every carrier).
- Version notes: `npm view rea-agents versions` (exit 0) ends `…, 6.3.0, 6.3.1, 6.4.0, 6.5.0, 6.7.0` (no 6.6.0, so 6.7.0 is the immediate successor). Both `rea-agents@6.5.0` and `rea-agents@6.7.0` pin `evmole` to exactly `0.9.3` (`npm view rea-agents@6.5.0|6.7.0 dependencies.evmole` → `0.9.3` for both; installed `node_modules/rea-agents/package.json` shows `evmole 0.9.3` in each), and both envelopes report `"provider":{"id":"evmole-interface","version":"evmole@0.9.3"}`. Consistent with the sibling finding that EVMole 0.9.4 exists upstream but no published REA carries it, so the Vyper argument inference is unchanged by construction.

## Limits and risks

- Coverage is the six C2 carriers only (69 rows, 43 distinct selectors). REA 6.7.0 could still differ on bytecode shapes not represented here; the claim is bounded to these carriers.
- The naming-rule comparison reuses the **saved** 2026-10-22T08:28Z–08:30Z lookups. This seat made no fresh database request, so it measures the effect of the REA version on the inference step only, not on the databases' current content.
- No live network lookups were made, so no 1-second-per-host pacing was needed and the 120-request seat cap was not approached (0 external lookups).
- The `evidence_id` change is a REA hashing-policy change, not an analysis change. The entry names 6.5.0 explicitly, so it stays accurate as written; if the L1 wants to claim version insensitivity it should say "analysis content identical under REA 6.7.0; the envelope `evidence_id` differs because REA changed its semantic-projection rule", not "byte-equal under 6.7.0".
- Tooling: no package installed or upgraded by this seat. `npx` fetched `rea-agents@6.7.0` and `rea-agents@6.5.0` from the public npm registry into the existing `~/.npm/_npx` cache (Node v24.21.0, npm 11.19.0). No pacman transaction, no service restart.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2Rea67/`)

sha256, one per line (`file` `sha256`):

```
out67/rv2token.json 12e5d171396354065979df8a0f109beb41598e5fe33cf6490a4e46f6e85076fb
out67/kdxtoken.json 4a82b31d2b14c9b145ac69731c2b6396ba53f456929f1105f2fda19f2338018f
out67/vaultb-opt200.json 8336351fe65ad48695b67c33b8012a2a0a9cbbdea2ff39209a9e33a8198fb214
out67/carrierb.json 47418c8f67170d5d7250efe87e459c79fcd20370ccbec838ff9d8fd674d7c374
out67/stewardtoken.json 0ee7dfc990aafb02a2556006b13d3ef093aa624d20c066948a46e27705d68359
out67/carrierv.json 0d7171ed8a0ea0beca90fb3d32c54ac20a9bfbf1f7b89ce275999fe3a1ea7c75
out65/rv2token.json ed4a1118dfc7a180fac794541371019ce8bc2272908860bc1fd4bf99ad2cbf50
out65/kdxtoken.json 1bc65b6f3f396f9efea242a2ca25317c90c1c85e9c79798a16bba43ee8274462
out65/vaultb-opt200.json 506c9101ab85e2c45d221054b923d850923a740792789de378b8fb1ce5d4aeba
out65/carrierb.json 95e86017fc1ee8f75b616cbe62e0d878302af1e30d367aa1bb769fc5966ec0d6
out65/stewardtoken.json 1de20e9604885579649a6486306518a906c1aac6c4961a818e53d3cdd82b642a
out65/carrierv.json a2e7ba7b27a9fece86842d641462cd6ad7fffe219feffd40b583b2c4d1e8b8e4
compare-rules.py 02d6214a55fa31cad3ebd5e630db92b5332332c0dc3585014578122ac4a0d305
out/per-carrier-diff.txt 6f06cd98107de9b50a882c8e75400417414188ba7fbe935d601dbfce46eb0891
out/tally-rea670.json e54809ba0850201897d038822ac95d60032f2592744588aaa79123a8224e25aa
out/tally-rea650.json a653ca08725c5dd616a2efda23910a09efc391e2a0034c96d51658354e5f1362
out/tally-rea670-final.json 89a6433a49f34649d061e829d18ee0afcd0116f1fe39dd2e78965520624ea032
out/tally-rea650-final.json 7d9322411e0b24ea9885d0ca1f771c8bfac34f562b3665e3bc721415c94a6439
out/tally-670-clone/tally.json 479bc13ea4c2139289808a54c47321c83c3daafffaad5de4b06c00ac840b40dc
out/tally-670-clone.stdout 7e02dbbe048da684b217b5c535423db41938c41a9b4767d5f13359fb628ca2b7
```

All `out67/*.err` and `out65/*.err` are empty (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
