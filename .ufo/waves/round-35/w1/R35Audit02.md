# R35Audit02 — S129 release page and pagination audit

- Role: executor (fleet wave w1, round 35)
- Item: Verify S129 release page and pagination
- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Date: 2026-10-25; all reads read-only; only this report written inside the lane; VCS untouched.

## 1. Scope / claim context

Frozen claim C1 (plans/round-35-claims.md, claims-canonical.json) requires `corpus/SOURCES.md` row **S129**
(`status=mined`, `opened=2026-10-25`, `used-by` = `corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md`)
as the source for the jsc2js release-inventory entry. **S129 does not exist yet** — grep for `S129|S125` in
`corpus/SOURCES.md` returns no match (pre-data state is expected at freeze). The prep captures in
`.ufo/waves/round-35/prep/jsc-sources/` are the evidence base for that row; this audit verifies the source
side (release page + pagination) against the live upstream.

## 2. Captured evidence (prep)

| file | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-35/prep/jsc-sources/releases-page1.json` | 631043 | `4a5199ddf709ec41b6a1109b5d5598356892d6a4aad227dc873fe3869a0f813c` |
| `.ufo/waves/round-35/prep/jsc-sources/releases-page7.json` | 487166 | `499e2b227a6eb2c3053a8df280e52dc7dd5c597d50a1cdbabc1ff98a20e199fc` |
| `.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md` | 8996 | `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3` |

Both JSON files are raw GitHub REST release listings (arrays, no wrapper/headers) for repo
`xqy2006/jsc2js` (`https://api.github.com/repos/xqy2006/jsc2js/releases`, repo id 1042605456).

## 3. Verification performed

Commands (all read-only; nothing written to lane except this report; tmp files under /tmp):

```
curl -sS -D /tmp/gh-h{1,6,7}.txt -o /tmp/gh-p{1,6,7}.json \
  "https://api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page={1,6,7}"
curl -sS "https://github.com/xqy2006/jsc2js/releases?page=1"   # HTML pager
curl -sS "https://github.com/xqy2006/jsc2js/releases?page=68"  # HTML pager tail
python3 -c 'json.load(...)'  # full structural comparisons (see findings)
```

### 3.1 API pagination (per_page=100)

- `Link` headers on live page 1: `rel="next"` → page 2, `rel="last"` → **page 7**. Page 7 has no `next`.
- Page sizes live: 100, 100, 100, 100, 100, 100, 77 → **total 677 releases**.
- Captured page 1 == live page 1 (full JSON equality), captured page 7 == live page 7 (full JSON equality).
- All 7 live pages: 677 distinct release ids, zero overlap across every adjacent-page boundary
  (all 6 boundary overlaps = 0), so the listing is gap-free and duplicate-free.
- Boundary pairs are adjacent listings (e.g. p6 tail `12.9.202.28` → p7 head `12.9.202.26`; p1 tail
  `11.1.111` → p2 head `11.0.226.9`).

### 3.2 Within-page ordering nuance (not a capture artifact)

The server order is not strictly release-id monotonic: 5 positions per page (identical in capture and live)
have an id increase vs the previous row, e.g. page1 idx35: `11.8.172.2` (id 370808938, created
2026-08-14T20:30Z) immediately followed by `11.8.172.18` (id 370866840, created
2026-08-14T23:17Z). This is GitHub's own ordering for this repo (CI interleaves per-version release
builds), not a capture/reorder artifact — verified byte-identical in the live response (page1: 0 relative
order violations across all 100 shared items; page7 matches exactly).

### 3.3 HTML release page (UI)

- `https://github.com/xqy2006/jsc2js/releases` (HTTP 200) paginates at **10 per page → 68 pages**
  (pager aria-labels on page 1 and page 7 include "Page 68"; 677/10 → ceil = 68).
- UI page 1 lists newest tag `15.6.75.19`; UI page 68 lists oldest tail (`12.0.157`, …), matching the
  API order. Both UI and API pager structures are consistent with the 677-release total.

### 3.4 Release inventory facts (advisory content for the future S129 row)

- Total 677 releases; **min tag `5.1.281.65`**, **max tag `15.6.75.19`**; 101 distinct `major.minor`
  version families; earliest `published_at` 2025-08-24T03:19:17Z, latest 2026-10-21T08:33:45Z.
- 0 drafts, 0 prereleases; every release has exactly 2 assets: `d8-<tag>-linux.tar.gz` +
  `d8-<tag>-windows.zip` (Linux/Windows d8 per README).
- Range claim in the captured README (V8 5.1+; 5.1 is the lower bound) is consistent with the actual tag
  span (min tag exactly 5.1.281.65).

## 4. Findings

1. **S129 row is not yet authored** in `corpus/SOURCES.md` — expected pre-data; nothing to falsify in the
   row itself yet.
2. **Release page verified**: endpoint live, HTTP 200, correct repo, captures byte-identical to the current
   live listing (page 1 and page 7) as of 2026-10-25.
3. **Pagination verified**: API pagination 7 pages @ per_page=100 (rel="last" = page 7), 677 total,
   gap-free/duplicate-free; UI pagination 68 pages @ 10/page; both consistent. Captured page 7 is the
   true final page (77 < 100 items), so the prep snapshot covers the newest and oldest endpoints of the
   full 677-release timeline.
4. **No falsification found** against the claim's source basis. One advisory limit: prep captures only
   pages 1 and 7 (middle pages 2–6 were not stored in prep); this audit re-fetched all 7 live pages and
   confirmed contiguity, so the S129 row can cite the full range with confidence, and a future frozen
   counter should not depend on the absent middle-page captures.

## 5. Recommended S129 row shape (advisory for the authoring seat)

`| S129 | GitHub releases API/UI for xqy2006/jsc2js — https://api.github.com/repos/xqy2006/jsc2js/releases (per_page=100, 7 pages, 677 releases; UI https://github.com/xqy2006/jsc2js/releases, 68 pages) | dataset | A | ... | snapshot 2026-10-25; page1 sha256 4a5199…, page7 sha256 499e2b…; min tag 5.1.281.65, max tag 15.6.75.19 | ... | mined | 2026-10-25 | on-release | corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md |`

## 6. Limits

- Unauthenticated GitHub API rate limit 60/hr (39 used during this audit; no retry pressure).
- The middle pages 2–6 were not captured in prep; verified live only (see finding 4).
- No lane writes other than this report; no VCS mutation; no subagent dispatch.
