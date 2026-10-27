# R43W2AssimCitations — independent source-citation attack

Measured revision: `5856614ac4bf7f2363bbcd1956644474a82108e5` (lane HEAD, 2026-10-27). Freeze: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`. Scope: `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`, its S136/S137 citations, cited source anchors, page/API boundary, and recheck. Read-only lane; no shokuknow access/write, extractor execution, or VCS mutation. Scratch removed before yield. No installation.

## Results

**API matrix and projection: reproduced.** Fresh API response `https://api.github.com/repos/onekey-sec/sasquatch/releases`: HTTP 200, 107313 bytes, SHA-256 `5ada6ccc52b5062f6226a25e1e19ed252e2edcb180cf7dadbbcb4e368f87c3bf` (11:33:15Z response date). The prescribed jq projection exited 0 and returned `[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]`. All eight tags/publish times and all listed asset sizes agree with the entry. The newest release has the six stated `sha256:` digests; amd64 digest matches S107. Body lengths were 645, 560, 0, 0, 0, 38, 0, 0; standalone `1.0` token scan found 0/8. `v4.5.1-1` body is exactly “Rebased on top of squashfs-tools 4.5.1”; `v4.5.1-6` body includes the cited C23 line and Full Changelog URL. `grep -c 'sasquatch-v4.5.1-6' api.json` returned 12. The staged draft’s actual `recheck:` (R42Assim draft entry-A line 17) is instead the Python release/asset-count projection; that projection reproduced on this response too.

Field-level comparison against the committed R42 API receipt (`.ufo/waves/round-42/w1/artifacts/R42Assim/receipts/rel.json`, 87700 B, SHA-256 `57a19513ca266c10a310504fc33fa16f15e04f92f0be6840c2eb4e6c56a499db`) found identical keys and only seven `download_count` differences. The seven values progressed from 23694 to 23790 for the noted amd64 asset among the changed counters; this current fetch is later than the entry’s cited 23773. Comparison to R43AssimGround’s retained API JSON found six differing objects, all only `download_count`. Fresh compact JSON was 87701 bytes including newline, consistent with the entry’s serialization caveat. The response digest differs from the cited response digest, as disclosed and expected for mutable counts.

**Rendered-page boundary: reproduced.** Fresh page fetch HTTP 200, 349274 bytes, SHA-256 `fe4f248cf78556063b84b81c323c8c2ff025bd0e578dadcef1bed952a83f31b6`. Extracted 8 distinct release-tag hrefs. Counts for `sasquatch_1.0_amd64.deb`, arm64, armhf, and dbgsym amd64 were all zero. The page’s length/digest differ from retained fetches, as disclosed. Fresh page `grep -c 'sasquatch-v4.5.1-6'` is 13; this is not the entry’s API grep recheck. Retained R43 scribe and ground page captures also yield 13. Entry’s two page-capture hashes/lengths were directly corroborated by `R43ScribeAssim/receipts/page-probe.txt` (first capture) and `page-fetch2.txt` (second); the S137 registry row independently records R43AssimGround fetch hashes, so distinct fetches are being cited, not inconsistent source payload claims.

**Citation wording discrepancy (finding).** Landed entry’s final paragraph says “The staged entry’s own `recheck:` — `grep -c 'sasquatch-v4.5.1-6'` → `12` — reproduces.” But the staged draft at `.ufo/waves/round-42/w1/artifacts/R42Assim/drafts/entry-A-sasquatch-release-matrix.md:17` has a Python API projection as its `recheck:`; it contains no grep. The `grep -c` → 12 is separately documented in `R42Assim.md:87` and `artifacts/R42Assim/sources-reopened.md:12` as the review/row recheck, and currently reproduces on API bytes (12). Thus the outcome is true, but “staged entry’s own recheck” misattributes which command was staged. The row’s current jq projection is independently valid and reproduces; this is a provenance/wording calibration issue, not a false matrix result.

**Rows and anchors.** SOURCES header has 11 columns; S136 and S137 each have 11 cells, kind/tier/status/date/recheck/used-by fields are structurally present, and registry IDs are unique (137/137). S136 is dataset/A; S137 docs/A; both mined, opened 2026-10-27, recheck 180d, and used by the landed entry. S135 LICENSE was independently fetched: 1068 bytes, SHA-256 `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`; cited permission line is line 5. Other cited anchors checked: `PROVINCE.md:156-157` contains the sasquatch Frontier bullet; `corpus/lessons/round-36.md:42` has the staged refusal; round-42 `R42Assim.md:28` records the ADMIT verdict; `corpus/evidence/round-36/c1/K1/after-run.json:10` records `unsquashfs version 4.5.1 (2022/03/17)`; `~/.local/bin/sasquatch` hash is `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`. Tags API reports 19 tags, including exactly the eight sasquatch-v* tags. Releases `?per_page=100&page=2` returned `{"n":0,"tags":[]}`.

**Plan numstat discrepancy.** FREEZE→REV SOURCES diff is empty; blob hashes at FREEZE and REV both `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c`. BASE→REV `git diff --numstat` is `4 0`, not the plan’s “exactly 3 insertions and 0 deletions”: the diff adds S135/S136/S137 plus a blank line. The three data rows themselves are the only row additions. No existing content changed.

## Commands and outputs (exit status)

- `git -C <lane> rev-parse HEAD`; `git log --oneline -5`; status inspection: HEAD as above; no mutation performed.
- `df -h /fast/scratch /home/vgpnk/Projects/shokunin`: /fast 506G available, /home 590G available. Network probe API HTTP 200.
- `curl -fsSL -D api.headers -o api.json https://api.github.com/repos/onekey-sec/sasquatch/releases`; exit 0; `wc -c` 107313; `sha256sum` as above.
- `curl -fsSL -o page.html https://github.com/onekey-sec/sasquatch/releases`; exit 0; `wc -c` 349274; `sha256sum` as above.
- `jq -c '[length, (map(.assets|length)), (map([.assets[]|select(.digest)]|length))]' api.json`: exit 0; exact projection above.
- `jq -r` projections of tags/published_at, all asset name/size pairs, newest digests, and body lengths: exit 0; values described above.
- Python field-level comparisons to R42 `rel.json` and R43AssimGround `rel-r43-assimground.json`: exit 0; respectively 7 download_count field changes, and six objects with only download_count differences.
- `jq -c . api.json | wc -c`: 87701; same for R43AssimGround raw response: 87701.
- Page href extraction via `grep -o ... | sort -u`: 8 distinct links; four filename `grep -c` checks: each 0; page tag-string grep count 13.
- `grep -c 'sasquatch-v4.5.1-6' api.json`: 12. Python body token scan: 0/8. Body line grep: C23 line and compare URL present.
- `curl -fsSL ...releases?per_page=100&page=2 | jq -c '{n:length,tags:[.[].tag_name]}'`: `{"n":0,"tags":[]}`. `curl .../tags?per_page=100 | jq`: 19 tags.
- `sha256sum ~/.local/bin/sasquatch`; receipt/anchor reads; S135 curl, `wc -c`, `sha256sum`: values above.
- `git diff --numstat BASE..HEAD -- corpus/SOURCES.md`: `4 0`; `git diff FREEZE..HEAD -- corpus/SOURCES.md`: empty; `git show` blob hashes identical.

Limitations: The live API/page are mutable; this report evaluates the exact fetches above and retained committed captures, not future responses. No asset packages were downloaded or executed. All fresh network files were under the seat scratch directory and removed before yield.

Report: .ufo/waves/round-43/w2/R43W2AssimCitations.md
