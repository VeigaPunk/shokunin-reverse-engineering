# R43CritAssim — refetch analysis receipt (2026-10-27, UTC)

All commands run from scratch `S=/fast/scratch/hyaku/kaidoku-r43/w1-R43CritAssim` (TMPDIR=$S).
No REA, no unblob, no sasquatch run. Tools: curl 8.x, python3 (system). No install/upgrade.

## 1. Draft-A recheck command, verbatim (`.ufo/waves/round-42/w1/artifacts/R42Assim/drafts/entry-A-sasquatch-release-matrix.md` frontmatter)

```
curl -fsSL https://api.github.com/repos/onekey-sec/sasquatch/releases | python3 -c 'import json,sys;d=json.load(sys.stdin);print(len(d),[len(r["assets"]) for r in d])'
```

Output (2026-10-27T05:2xZ): `8 [6, 6, 6, 6, 6, 6, 6, 2]` — exit 0. REPRODUCES.

## 2. Staged entry's own recheck, verbatim (`merge/kaidoku/knowledge/corpus/knowledge/sasquatch-prebuilt-package-inventory.md`)

```
curl -fsSL 'https://api.github.com/repos/onekey-sec/sasquatch/releases' | grep -c 'sasquatch-v4.5.1-6'
```

Output (2026-10-27): `12` — exit 0. REPRODUCES.

## 3. Flip-condition refetch (the round-42 verdict's flip)

Fetch: `curl -sS -D rel.headers 'https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100' -o rel.json`
→ HTTP/2 200, 107313 B, sha256 `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0` (copy: `rel-2026-10-27.json`).

- Ninth release? **NO** — `len(d) == 8`, tags unchanged (v4.5.1-6, -5, -4, -3, -2, -1, v1.0.1, v1.0).
- Changed asset set / counts / sizes? **NO** — per-release asset-count vector `[6,6,6,6,6,6,6,2]`;
  every asset name and byte size byte-equal to the round-42 receipt, incl.
  v1.0: 2 assets (sasquatch_1.0_amd64.deb 185708 B, sasquatch-dbgsym_1.0_amd64.deb 321380 B);
  v1.0.1: 185724 / 168184 / 162288; v4.5.1-6: 187244 / 170080 / 164428 (+ dbgsym 323896/327784/319048).
- Digest asymmetry unchanged: 6 of 6 assets carry `digest` (sha256) on v4.5.1-6
  (amd64 deb `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95` — matches held S107),
  0 of 6 on every older release.
- Body stating a package/upstream version pair? **NO** — only three bodies are non-empty:
  v4.5.1-6 (645 B: three change lines incl. "unsquashfs: fix prototypes for C23" / PR 32, New
  Contributors, Full-Changelog URL), v4.5.1-5 (560 B), v1.0.1 (0 B), v4.5.1-1 (38 B: "Rebased on top
  of squashfs-tools 4.5.1" — upstream version only, no package-version pair). Regex scan
  `4\.5\.1[^\n]{0,60}1\.0|1\.0[^\n]{0,60}4\.5\.1` over all bodies: no hits.
  **The flip does NOT fire today (2026-10-27).**

## 4. Why the body sha256 differs from the round-42 pin (citation-durability evidence)

Round-42 receipt (`artifacts/R42Assim/receipts/rel.json`, 87700 B, sha256 `57a19513…`) vs today's
107313 B: field-level diff over all 8 releases' assets shows the ONLY changed JSON values are
`assets[].download_count` (7 counters, e.g. v4.5.1-6 amd64 deb 23694 → 23773). Every structural
field (`tag_name`, `published_at`, `assets[].name`, `assets[].size`, `assets[].digest`, `body`) is
byte-identical. Conclusion: the API body is volatile by `download_count`; a body-sha256 compare is
not a freshness check — the durable recheck is the structural one in §1. Point-in-time pin only.

## 5. Rendered page re-verification (S131's negative citation)

`curl -sS -o sasq-releases.html -w '%{http_code} %{size_download}' https://github.com/onekey-sec/sasquatch/releases`
→ `200 349250` (copy: `releases-page-2026-10-27.html`). All 8 tags present in the page bytes
(v4.5.1-6 ×13, v1.0.1, v1.0, the four middle tags). `grep -c 'sasquatch_1.0_amd64.deb'` → **0**
(exit 1). The page still carries no asset filename; asset facts remain the API's (S130's), not the
page's (S131's teaches holds on 2026-10-27 bytes).
