# R36W2ScoutS109 — re-open of SOURCES row S109 (neovim v0.12.6 release)

Observed 2026-10-26 ~05:00Z. Lane HEAD at observation `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` (`git rev-parse HEAD`). Row under test: `corpus/SOURCES.md:115`. No lane file edited; scratch removed. Tools installed: none (used the existing `gh` in `~/.local/bin`, `curl`, `jq`, `sha256sum`).

## Method
- Unauthenticated `curl https://api.github.com/repos/neovim/neovim/releases/tags/v0.12.6` → HTTP 403 (rate limit, 179.218.13.209). Switched to the authenticated `gh api` (account VeigaPunk) for all API reads. Same JSON as the public endpoint.
- Re-downloaded both assets with `curl -sSL` from the exact `url` fields in `carriers.json` (HTTP 200) and hashed them myself.
- Fetched the release page `https://github.com/neovim/neovim/releases/tag/v0.12.6` (HTTP 200, 207659 B) and `.../releases/expanded_assets/v0.12.6` (HTTP 200, 52427 B).

## Per-value verdict

| Value in the row | My observation | Verdict |
|---|---|---|
| tag `v0.12.6` | `rel.json`: `tag_name v0.12.6`, `draft false`, `prerelease false` | agree |
| commit `779c36969e31080503be2dfccbcc3f999e289606` | `releases/tags/v0.12.6` `.target_commitish` = that sha; `git/ref/tags/v0.12.6` points to an **annotated tag object** `022946c802832f938398dfae34b3f277ca9509d4`; `git/tags/022946c8…` `.object` = `{sha 779c3696…, type commit}`; `commits/v0.12.6 --jq .sha` = `779c3696…`; page HTML contains `779c36969e31080503be2dfccbcc3f999e289606` ×3. The row says "tag v0.12.6 (commit 779c…)" — that is the peeled commit, not the tag-object sha. Commit date 2026-10-09T15:05:39Z, tagger date 2026-10-09T15:06:21Z | agree (commit is the peeled target; tag-object sha is a different id and is not claimed) |
| published `2026-10-09T15:43:25Z` | `.published_at` = `2026-10-09T15:43:25Z`; page `<relative-time datetime="2026-10-09T15:43:25Z">`. (`created_at` is 15:06:21Z; the asset `updated_at` stamps are 15:43:22/23Z; a page `Verified 2026-10-09 15:30:00 UTC` is a commit-signature stamp, not the publish time.) | agree |
| `nvim-linux-x86_64.appimage` 11454968 bytes | API asset `size` 11454968; my download `size_download` 11454968, `stat -c %s` 11454968; `HEAD` `content-length: 11454968` | agree |
| `nvim-linux-arm64.appimage` 11356680 bytes | API `size` 11356680; download and `stat` 11356680 | agree |
| x86_64 sha256 `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb` | API `digest` `sha256:b644d034…29fb`; **my own `sha256sum` of the downloaded bytes** = same; `carriers.json` K3 = same; `expanded_assets` HTML contains `sha256:b644d034…` | agree (published digest == frozen K3 == bytes) |
| arm64 sha256 `8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2` | API `digest` same; `sha256sum` of downloaded bytes same; `carriers.json` K4 same; `expanded_assets` contains it | agree |
| quote `page install step "Download nvim-linux-x86_64.appimage"` | Release body (API) lines 48-50: `#### AppImage` / `1. Download **nvim-linux-x86_64.appimage**` under `### Linux (x86_64)`. Page raw HTML: `<li>Download <strong>nvim-linux-x86_64.appimage</strong></li>`. The quoted string is therefore the *rendered* text; it is not a contiguous byte substring of the markdown (has `**`) nor of the raw HTML (has `<strong>`). `grep -o 'Download nvim-linux-x86_64.appimage' page.html` → no match | agree on content/location (rendered text, correct section); **minor disagree on literal-substring fidelity** — a byte-level grep of either source misses it |
| "API assets digest" wording (digests came from the API) | true, and the same digests also appear on the page family: `page.html` itself has 0 `sha256:` strings (`grep -c` = 0); the digests are in the lazily loaded `expanded_assets/v0.12.6` fragment (24 occurrences, both carrier digests present, 12 distinct digests for 12 assets, `assets|length` = 12) | agree; the row's wording is the precise one |
| kind `dataset`, tier `A`, status `mined`, opened `2026-10-26`, recheck `on-release`, used-by `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` | `awk -F'|'` on line 115 → NF=13 = 11 cells, no `|` in a cell. `sources-census.sh validate --file corpus/SOURCES.md --today 2026-10-26` → no finding naming S109; only pre-existing W04 duplicate-url warnings on S054/S062/S069/S083/S090/S092/S102; last line `file ok …/SOURCES.md` (the pipeline's `rc=0` printed there is `tail`'s, not validate's) | agree |

## Disagreements found (all outside the S109 row itself)
1. **`corpus/lessons/round-36.md:29` — "Quote (3 words): "Download nvim-linux-x86_64.appimage""**. `echo -n 'Download nvim-linux-x86_64.appimage' | wc -w` → **2**. `R36ScribeSources.md:49` (wave 1) said "(2 words)". The word count in the committed lesson is wrong (still ≤25, so the gate's limit is unaffected; but the "3 words" figure is a stated measured fact that does not reproduce). `R36ReviewerQualityBar.md` row 16/17/42 also repeats "S109 3 words" as "met" — same miscount, not independently checked. Severity: low (cosmetic count), calibration.
2. **Quote literalness** (above): the quote is rendered-page text; the lesson gives no note that the source markdown bolds the filename. Same low severity.

## Things I checked and found nothing wrong
- Row sizes, digests, publish time, commit: all agree with live API, page, and bytes I hashed.
- The `carriers.json` frozen digests for K3/K4 equal both the published digests and my own re-hash.
- `corpus/evidence/round-36/c1/K3|K4/before.json` `published_bytes` 11454968 / 11356680 equal the row's sizes. (The `after.json` `published_bytes` values 51122564 / 51792724 are the extracted-payload totals, a different quantity; the entry's line 65 says the "before" figures are "the whole carrier" — consistent.)
- Release is not draft/prerelease; assets state `uploaded`.

## Limits
- The API digest is GitHub's computed asset digest, not a publisher-signed checksum (the release also lists `.zsync`/`shasum` assets; `shasum.txt` was not opened by me). The row's wording "GitHub-published digests" is accurate; "vendor-published" in the teaches cell is slightly stronger than GitHub-computed-on-upload. [INFERENCE] about publisher vs GitHub provenance; I did not verify how the digest is computed.
- Observation is a point in time (2026-10-26 ~05:00Z); an asset replaced later would change both digest and bytes, which is what `recheck: on-release` does not cover for in-place re-uploads.
