# R36W2ScoutS107 — re-open of SOURCES.md S107 (row at corpus/SOURCES.md:113, tip 01a44dbf)

Method (2026-10-26, ~04:59Z local session): `gh api repos/onekey-sec/sasquatch/releases/tags/sasquatch-v4.5.1-6` (unauthenticated curl was rate-limited; gh is logged in, no repo write), `curl -L` of the amd64 deb from the release's browser_download_url, `sha256sum`/`stat`, `ar x` + `tar -xf data.tar.xz`, `sha256sum ~/.local/bin/sasquatch*`. Scratch removed. No tools installed.

## Per-value verdicts
| Cell value | Re-measured | Verdict |
|---|---|---|
| published 2026-01-27T11:57:51Z | API `published_at` = 2026-01-27T11:57:51Z (created_at 11:54:41Z; draft=false, prerelease=false); HTML page `datetime="2026-01-27T11:57:51Z"` | AGREE |
| sasquatch_1.0_amd64.deb 187244 bytes | API `size` 187244; downloaded file `stat -c %s` = 187244 | AGREE |
| deb sha256 efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95 | API `digest` sha256:efbc92bd…ade95; `sha256sum a.deb` identical | AGREE |
| member usr/bin/sasquatch sha256 ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754 | `sha256sum` of extracted ./usr/bin/sasquatch (382824 B) identical; also equals ~/.local/bin/sasquatch | AGREE |
| member usr/bin/sasquatch-v4be sha256 fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6 | extracted ./usr/bin/sasquatch-v4be (436232 B) identical; also equals ~/.local/bin/sasquatch-v4be | AGREE |
| quote "fix: remove unnecessary magic checks by @jstucke in #34" | Rendered release page text (HTML, tags stripped): `unnecessary magic checks by @jstucke in #34` → AGREE with the web view. Release-body *source* (API `body`, which is what S107's "API asset digest" provenance implies) reads `* fix: remove unnecessary magic checks by @jstucke in https://github.com/onekey-sec/sasquatch/pull/34`. | AGREE on rendered page; DISAGREE as a verbatim API-body string: ` in #34` is GitHub's display rewrite of the full PR URL. Minor; word count 9 holds either way (with URL it is 9 words too, URL counted as one). |

## Scope-cell checks
- "asset set": the cell claims scope "asset set, publish date and the amd64 package digest" but the anchor cell never enumerates the asset set. API shows 6 assets: sasquatch_1.0_{amd64 187244 sha256 efbc92bd…, arm64 170080 28e57a4f…476e, armhf 164428 29c72159…1c22}.deb and sasquatch-dbgsym_1.0_{amd64 323896 73d44ca5…c54e, arm64 327784 78918317…49c4, armhf 319048 9d82e6d4…686a}.deb. DISAGREE (gap, not error): scope promises an asset set the row does not record; only the amd64 deb is recorded. [INFERENCE] harmless to claims since only amd64 is used, but the stated scope overreaches the anchor.
- Release page HTML lazy-loads assets, so the asset set is verifiable only via API/expanded-assets, not the tag page alone.
- Observation (no disagreement): deb tar member mtimes are 2022-02-26, i.e. the packaged binaries predate the 2026-01-27 release by ~4 years; consistent with a build-in-CI-from-old-staging, not a contradiction of any S107 value. Release also contains the changelog "fix: remove unnecessary magic checks" (PR #34) plus PR #33, #32 (C23 prototypes); body lists those three.
- Lesson line (corpus/lessons/round-36.md:27) repeats the quote and digest equalities: "installed binaries equal the deb members" — AGREE (both hashes match ~/.local/bin).
- Knowledge file header (corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md:1) restates size/digest/date: AGREE.

## Bottom line
All numeric/digest/date values AGREE. Two disagreements: (1) quote is the rendered form, not API-body-verbatim (`#34` vs full PR URL); (2) scope cell says "asset set" but records only 1 of 6 assets.
