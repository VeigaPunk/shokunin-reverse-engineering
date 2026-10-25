# R35Audit18 — Verify release API page tags (r35 w1, executor)

**Item:** Verify release API page tags. Read-only / private /tmp only; no lane writes beyond this report.

**Scope:** prep captures `.ufo/waves/round-35/prep/jsc-sources/releases-page1.json` and `releases-page7.json` (GitHub releases API for `xqy2006/jsc2js`) feeding C1/S129 (.jsc → source mapping, release inventory).

## Commands / method (evidence)

1. Parse captures as JSON; extract per-release `tag_name`, `name`, `html_url`, `id`, `created_at`, `draft`, `prerelease`, assets.
2. Live re-fetch (2026-10-25 ~16:17Z, unauthenticated API):
   - `curl -sH "Accept: application/vnd.github+json" "https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page=1|2|7|8"` → `/tmp/r35audit18/live-page{1,2,7,8}.json`
   - `urllib` fetch of pages 3–6 → `/tmp/r35audit18/live-page{3,4,5,6}.json`
3. `git ls-remote --tags https://github.com/xqy2006/jsc2js.git` (1354 ref lines → 677 distinct tag names).

## Findings

- **Captures are byte-identical to live API:** `live-page1.json == releases-page1.json` and `live-page7.json == releases-page7.json` (exact JSON-equality; same 100 and 77 records, same `(id, tag_name)` pairs; no only-live / only-capture diffs).
- **Complete inventory:** total 677 releases over exactly 7 pages (100×6 + 77); page 8 → `[]`. All 677 ids unique; all 677 `tag_name` unique, non-empty, dotted-numeric (regex `\d+(\.\d+)+`); 0 drafts, 0 prereleases.
- **Tag-field consistency:** in both captured pages, `name == tag_name` for all 177 releases and `html_url` ends `/releases/tag/<tag_name>` (0 mismatches).
- **Git-tag correspondence (1:1):** all 677 release `tag_name`s exist as distinct git tags; 0 git tags lack a release; 0 release tag_names missing from git tags.
- **Pagination contiguity:** consecutive pages connect with no gap/duplicate (created_at strictly descending across page boundaries: 2026-08-14T13:11:13Z → … → 2025-08-24T03:19:15Z). Within-page order is not strictly sorted by any single field (minor server-side order quirks: 5 created_at inversions on page 1; harmless).
- **Assets:** every release carries exactly 2 assets named `d8-<tag>-linux.tar.gz` / `d8-<tag>-windows.zip`. Note: readme quick-start mentions `d8-linux` / `d8-windows.exe` — descriptive names, not literal asset names (cosmetic doc-vs-data nuance).

## Falsifications

- None found: no authentication/tampering issue, no tag anomalies, no missing/extra tags, no drafts/prereleases, page set complete.

## Status

- Verdict: PASS — captured release API pages are authentic, internally consistent, and fully backed by git tags.

## Limits

- Live comparison reflects GitHub state at fetch time (2026-10-25 ~16:17Z); unauthenticated API (~60 req/hr) — no further enumeration.
- Pages 2–6 were not part of prep captures; fetched live for completeness only (not stored in lane).
- Claim scoring is the counters' job; this report is advisory evidence for C1/S129.
