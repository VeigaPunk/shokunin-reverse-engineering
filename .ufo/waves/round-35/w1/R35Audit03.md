# R35Audit03 — seat report (w1, executor item)

Item: inspect release page 7 and total limitations. Read-only inspection; only this report written. No VCS/claims/counters touched.

## Evidence A — `prep/jsc-sources/releases-page7.json` capture (valid, complete)

- Valid JSON array, len=77; every release carries full GitHub release payload (id, tag_name, name, body, published_at, created_at, html_url, assets, draft, prerelease).
- No drafts, no prereleases, no empty bodies. Each release has exactly 2 assets: `d8-<tag>-linux.tar.gz` + `d8-<tag>-windows.zip` (177/177 releases across pages 1+7).
- Body pattern: `Patched d8 for V8 <ver> (v2 patch, includes d8 + snapshot_blob.bin).`
- Range: tag `12.9.202.26` published 2025-08-25T00:32:29Z → tag `12.0.157` published 2025-08-24T03:19:17Z. Ids and tags disjoint from page 1 (no overlap). Page-7 newest created (2025-08-25T13:30:17Z) is older than page-1 oldest created (2026-08-14T13:12:00Z) → the two captures are non-overlapping segments of the same list.

## Evidence B — totals and limitations (live API probe)

- `GET https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100` → `Link:` header: `rel="next"` page=2, `rel="last"` page=7. Page 8 returns `[]` (HTTP 200, 5 bytes).
- Total releases = 677 (pages 1–6 × 100 + page 7 × 77). Page 7 IS the last page.
- Limitation (local): the lane captures only page 1 and page 7; pages 2–6 (~500 releases, created 2025-08-25 → 2026-08-14) are NOT captured locally. The S129 release-inventory entry can therefore enumerate only the 177 captured samples; any total/coverage claim must cite the 677 total and the missing middle pages, or re-fetch pages 2–6 before writing the inventory.
- Limitation (API): per_page cap 100; unauthenticated core rate limit 60/hr (probe saw 31 remaining after existing usage; reset 1792957347). Not scoring-relevant — c1 counter reads git objects only.

## Evidence C — ordering nuance (do not infer chronology from page order/tags)

- Neither page is monotonic by `created_at`, `published_at`, or tag. Tags are backfilled (e.g., `11.1.111` published 2026-08-14 on page 1 sits next to `15.x` tags; page 7 holds `12.x` tags published 2025-08). For the inventory, only the tag strings are authoritative for V8 version coverage; page position and dates must not be used as a version ordering.

## Evidence D — instrument pin integrity at HEAD `3ecf4298`

- `sha256sum` working tree == HEAD blob == canonical pins: `tools/round-35/c1-coverage-counter.py` = `e28792c7…`, `c2-calibration-counter.py` = `576c14dd…`, `plans/round-35-claims.md` = `45b644a4…`.
- `.ufo/waves/round-35/assimilation/census-start.txt` sha256 = `b6ce2b17…` == `frozen_inputs` pin. Content matches D-1 predicates: rows=106, EXIT=0, exactly 9 W04 warnings (S033/S047/S054/S062/S069/S083/S090/S092/S102).
- `freeze-status.md` INSTRUMENT_REVISED debt refers to the pre-canonical discovery revision; the canonical pins already hold the final hashes (as that note itself states), and those pins match the actual instrument bytes today.

## Evidence E — first falsifications (current HEAD = do-nothing state for C1)

- At HEAD 3ecf4298: no `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md`, no `…release-inventory.md`; no S125/S129 rows in `corpus/SOURCES.md`; no PROVINCE.md/README coverage-map rows. These are exactly the 8 failing checks listed in `controls/c1-do-nothing.json` (entry_missing ×2, registry_row_missing ×2, province_missing ×2, readme_missing ×2) — i.e., C1 currently fails as the fresh-start control expects. The c1 counter cannot pass until the writing wave lands those artifacts.
- Instrument checks are structurally sound: `ENTRIES` maps mapper-contract→S125 and release-inventory→S129; S125 = README raw URL (`raw.githubusercontent.com/xqy2006/jsc2js/main/README.md`), S129 = releases page URL; no pre-existing SOURCES row collides (grep `jsc2js` in `corpus/SOURCES.md` = 0 matches); append safety: only IDs from S107 up, never re-add S106.

## Evidence F — content facts for the entries (advisory)

- S129/release-inventory: README advertises `d8-linux` / `d8-windows.exe` per release; actual asset names are version-prefixed archives (`d8-<ver>-linux.tar.gz`, `d8-<ver>-windows.zip`) and bodies state `includes d8 + snapshot_blob.bin` — the entry should record the real asset naming.
- S125/mapper-contract: README limitations to carry — (1) Node-compiled `.jsc` may not decompile (no Node env; Electron works); (2) reconstruction is approximate (names/control flow/constant folding not fully recoverable); (3) V8 version must match the producing d8; (4) V8 5.1 lower bound, 369 legacy tags / 57 modern failed-tag handling.

## Limits

- Read-only throughout; the only lane write is this report. Live probes: 2 unauthenticated GitHub API GETs (page 8 + page 2), ~31/60 core requests remaining; no scoring run, no git mutation.
