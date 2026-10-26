# R38ScoutSasquatchReadme — sasquatch README big-endian statement + v4be digest provenance

Scope: read-only; no lane corpus edit; tools installed: none. Access UTC: README fetch 2026-10-26T06:16:46Z (HTTP 200); release API 2026-10-26T06:16:46Z (HTTP 200); deb download + onekey-sec repo reads 2026-10-26T06:17:10Z.

## Finding 1 — devttys0 README says nothing about big-endian (confidence high)
- `curl https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md` → 200, 1050 bytes, 30 lines, sha256 `f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef` (== S111's recorded digest/line count; unchanged).
- `grep -c -i -E 'big|endian|-be'` → **0**. No `-be`/`-le`/big-endian/AVM text anywhere in it. Contrary to the "big-endian usage" premise in the assignment: that README has no big-endian usage section.
- What it does say (<=25 words each): "a set of patches to the standard unsquashfs utility ... add support for as many hacked-up vendor-specific SquashFS implementations as possible." / "Very beta." / "The included `build.sh` script will download squashfs-tools v4.3, patch the source".
- Repo state: devttys0/sasquatch not archived, default branch master, last push 2023-05-23T14:22:35Z (API). [INFERENCE] it is the legacy upstream; the shipped packaging is onekey-sec's fork.
- Consequence for the C1 entry: do NOT cite S111 for any -be / big-endian / v4be statement; cite it only for the self-description (S111 row's own scope already says this). Big-endian tool statements must rest on S107 (package contents), S108 (unblob handler argv), and the binary's own `-help`.

## Finding 2 — release API sasquatch-v4.5.1-6 (confidence high)
- `GET https://api.github.com/repos/onekey-sec/sasquatch/releases/tags/sasquatch-v4.5.1-6` → 200; tag `sasquatch-v4.5.1-6`, published 2026-01-27T11:57:51Z, prerelease=false, draft=false.
- Body quote: "fix: remove unnecessary magic checks by @jstucke in" PR #34 (body lists PRs #33, #32, #34; nothing about big-endian).
- Six assets only; **no standalone v4be asset**: sasquatch_1.0_{amd64,arm64,armhf}.deb, sasquatch-dbgsym_1.0_{amd64,arm64,armhf}.deb. API digest for amd64 deb: sha256 `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95`, 187244 B (matches S107).

## Finding 3 — installed sasquatch-v4be == deb member (confidence high)
- Downloaded `https://github.com/onekey-sec/sasquatch/releases/download/sasquatch-v4.5.1-6/sasquatch_1.0_amd64.deb` → sha256 `efbc92bd...ade95` (== API digest).
- `ar x` + `tar xf data.tar.xz`; `sha256sum`:
  - `usr/bin/sasquatch` `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`
  - `usr/bin/sasquatch-v4be` `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`
- Installed: `sha256sum ~/.local/bin/sasquatch*` → `ad02d27a...4754` (382824 B), `fac88740...14c6` (436232 B), both regular files (not symlinks), mtime Oct 26 01:22. **Both byte-identical to the deb members** and to S107's recorded digests.
- `sasquatch-v4be -version` → `unsquashfs version 4.5.1 (2022/03/17)`; `-help` lines 79-80: "-be Treat the filesystem as big endian" / "-le Treat the filesystem as little endian" (the binary's own statement; usable for the C1 tool statement).
- Why two binaries (primary source, onekey-sec/sasquatch `main`, `debian/rules`): normal build installs `sasquatch`; then `CFLAGS=-DFIX_BE dh_auto_build` and `cp squashfs-tools/sasquatch .../usr/bin/sasquatch-v4be`. Quote: "CFLAGS=-DFIX_BE dh_auto_build". Not yet in SOURCES.md (S107 scope is asset set + digests only) — candidate row if the entry wants to explain v4be; fetched raw.githubusercontent.com/onekey-sec/sasquatch/main/debian/rules (HTTP 200, branch main, no commit pinned — pin before citing).
- onekey-sec `main` has no README.md (raw 404); its `README` file is old squashfs NEWS text (no endian content). default branch `main`, pushed 2026-04-13T11:44:49Z.

## Limits
- debian/rules read from branch `main` unpinned; the release tag's rules not fetched [INFERENCE: same logic at tag].
- Did not run the binary on carriers (out of scope). Scratch removed.
