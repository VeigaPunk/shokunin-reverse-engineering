# R23 source census reconciliation

## Findings

- **Observed — current registry recount:** Parsed the `Registry` Markdown table in `corpus/SOURCES.md:3-6,7-63` with Python, selecting rows whose first cell is an `S`-number, splitting the table cells, and requiring 11 cells per source row. The result is **57 rows, S001–S057**, with no missing IDs. Histogram: **tier A 51, B 5, C 1**; **status mined 55, rejected 2**; cross-tab **A: 50 mined / 1 rejected; B: 5 mined / 0 rejected; C: 0 mined / 1 rejected**. The input file SHA-256 is `5ae5e7ed539d092d801d1c521cb3a0cfa6d89ff82e38b8d86c0c8d5b4f777ebd`.
- **Observed — R22 end-state agreement:** `.ufo/waves/round-22/verify/final/source-rows.json:2-22` reports `after: 57`, `old_rows_identical: true`, tiers A/B/C `51/5/1`, and statuses mined/rejected `55/2`. Those counts exactly match the independent Python recount of the current table. Its recorded SHA-256 is `b51d86baec577f35cd75143219cbb16932552a5a0db89ee73c633bb5af53fa9f`.
- **Observed — validation output and warning drift:** R23 `.ufo/waves/round-23/start-census.json:1-12` records `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`, exit **0**, and W04 warnings for S033, S047, and S054, followed by `ok` for the registry. R22 final `.ufo/waves/round-22/verify/final/sources-census.json:4-15` records exit **0** and the same three W04 warnings, including S054. R22's earlier `.ufo/waves/round-22/start-census.txt:1-4` records exit **0** but only the S033/S047 warnings. Thus current validation agrees with R22 final, while the R22 start snapshot omits a warning that appears in its final snapshot; this does not affect the exit or row-count/histogram comparison. R22 final census SHA-256: `ac54433ede3b4a358868e439ec28e553ebcf49fe47ada4e71671b579945bebce`; R22 start snapshot SHA-256: `c3b713b6dc708735047952201a58b0a8f41197b46102b89e95068b261f477513`; R23 start snapshot SHA-256: `26175deda5ae80c44403625cce0b68f069128a7c74a424a3b44348c2e7bba1e6`.
- **Observed — inherited/declaration boundary:** S052 and S054 are both mined A-tier rows for the Android NDK ABI guide (`corpus/SOURCES.md:58,60`); S054 explicitly says it supersedes S052 and narrows the cited interpretation. The registry validator emits W04 for the repeated URL across scopes, but the validation still exits 0. S053/S057 likewise remain separate mined A-tier rows: S057 explicitly supersedes S053 and cites the original envelope rather than only the extracted copy (`corpus/SOURCES.md:59,63`). These distinctions are present in the current 57-row count and in the R22 end-state histogram. **Inference:** W04 is a nonfatal duplicate-source warning, not evidence that either supersession was omitted from the table.
- **Conclusion:** No row-count or tier/status-histogram discrepancy from R22 final is observed. No new S058+ row is present in this registry snapshot; this is a count observation, not a conclusion about whether the round required a new source.

## Produced files

- This report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewSourceCensus.md` — SHA-256 is computed after writing and reported in the final handoff (self-hash is not embedded in this file).

## Installs

- None.

## Open risks

- This is a syntactic row recount and comparison to retained R22 outputs. It does not independently replay the R22 `old_rows_identical` comparison or establish source authenticity, source relevance, or knowledge ownership beyond what the registry and cited outputs record.
