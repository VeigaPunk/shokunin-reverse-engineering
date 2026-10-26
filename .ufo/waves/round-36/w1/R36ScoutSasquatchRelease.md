# R36ScoutSasquatchRelease — onekey-sec/sasquatch `sasquatch-v4.5.1-6`

Advisory, read-only. No VCS mutation, no tool installed (nothing needed beyond curl/ar/tar/sha256sum already on host; `dpkg-deb` absent, so the deb was unpacked with `ar x` + `tar -xf`). Scratch removed at the end.

## Observed facts

Access UTC: **2026-10-26T04:26:58Z–04:26:59Z** (`date -u` before/after the two fetches). Both `curl` calls returned HTTP 200:
- API `https://api.github.com/repos/onekey-sec/sasquatch/releases/tags/sasquatch-v4.5.1-6`
- page `https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6`
- asset list also read from `https://github.com/onekey-sec/sasquatch/releases/expanded_assets/sasquatch-v4.5.1-6` (page loads assets lazily, so the main page HTML does not itself contain the assets or digests; the expanded_assets fragment repeats the API digests).

Release: `tag_name`/`name` = `sasquatch-v4.5.1-6`; `published_at` **2026-01-27T11:57:51Z**; `created_at` 2026-01-27T11:54:41Z; draft=false, prerelease=false; `target_commitish` = `main` (a branch name, not a commit sha; the tag commit sha was not fetched).

Body (verbatim, CRLF stripped): "## What's Changed" with three PRs — `CI: fix build-nix` (#33, @qkaiser), `unsquashfs: fix prototypes for C23` (#32, @whispersofthedawn), `fix: remove unnecessary magic checks` (#34, @jstucke) — plus New Contributors and a compare link `sasquatch-v4.5.1-5...sasquatch-v4.5.1-6`. The body does not mention unblob, recursion, or the Debian-package contents.

Assets (name, bytes, GitHub `digest`, updated_at):

| asset | size | digest |
|---|---|---|
| sasquatch-dbgsym_1.0_amd64.deb | 323896 | sha256:73d44ca506e3273784091f3092839e8e8c162a81bb7d5af757201b0b1d41c54e |
| sasquatch-dbgsym_1.0_arm64.deb | 327784 | sha256:7891831a7cd7111d7d2380ef2df3dcb32295ea5093eff5ceec15e407e7be49c4 |
| sasquatch-dbgsym_1.0_armhf.deb | 319048 | sha256:9d82e6d4320957e2491603aa00f9c55fd816770a5f8926eaf7c454e98e74686a |
| sasquatch_1.0_amd64.deb | 187244 | sha256:efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95 |
| sasquatch_1.0_arm64.deb | 170080 | sha256:28e57a4ff545da32a65c3e061ff8a51e5ebaa5d170985c49f0b3eef08923476e |
| sasquatch_1.0_armhf.deb | 164428 | sha256:29c721598df93dcdf3c876b61d9941764f40af8f0ec4f0f8ac3d2fe75b8f1c22 |

amd64 files updated 2026-01-27T11:59:44Z; arm64/armhf 12:07:28–29Z.

## Comparison with installed `~/.local/bin/sasquatch`

- Re-downloaded `sasquatch_1.0_amd64.deb`: 187244 bytes, sha256 `efbc92bd…ade95` — **equals the GitHub digest**.
- `ar x` → `data.tar.xz` contents: `usr/bin/sasquatch` (382824 B, sha256 `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`), `usr/bin/sasquatch-v4be` (436232 B, sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`), `usr/share/doc/sasquatch/{changelog.gz,copyright}`. Member mtimes inside the deb: 2022-02-26.
- Installed `~/.local/bin/sasquatch`: sha256 `ad02d27a…4754`, 382824 B — **byte-identical to the deb's `usr/bin/sasquatch`**. Installed `~/.local/bin/sasquatch-v4be` sha256 `fac88740…14c6` — identical to the deb's.
- `~/.local/bin/sasquatch -version` → `unsquashfs version 4.5.1 (2022/03/17)` (also for `-v4be`). ELF x86-64 PIE, dynamic; `ldd` resolved libpthread/libz/liblzma/liblzo2 from `/usr/lib`.

Interpretation: the installed binary is exactly the release-asset binary. [INFERENCE] The release is a re-publish of a package whose binaries are dated 2022-02-26 and report 4.5.1 (2022/03/17); the release body's three changes (C23 prototypes, magic-check removal, CI) are not shown by this check to alter the binary — only the deb digest and byte-equality are verified, not source-to-binary provenance.

## Located quote (≤25 words)

Release page / API body, "What's Changed" list: "fix: remove unnecessary magic checks by @jstucke in #34" (9 words; present in page HTML 3 times and in API `body`).

## Draft SOURCES.md row (11 cells; no `|` inside any cell; format matches S106; S107 absent from corpus/SOURCES.md at 2026-10-26, last row S106)

```
| S107 | onekey-sec/sasquatch release sasquatch-v4.5.1-6 — https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6 | code | A | The official sasquatch 4.5.1 Debian-package release: asset set, published date and amd64 package digest; not unblob recursion behavior, not any carrier or verdict | Opened 2026-10-26; published 2026-01-27T11:57:51Z; API digest of sasquatch_1.0_amd64.deb (187244 bytes) sha256 efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95, its usr/bin/sasquatch sha256 ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754; body quote fix: remove unnecessary magic checks | Names the provenance of the sasquatch binary that REA extract-firmware needs for squashfs recursion: official onekey-sec release, digest-checked, prebuilt for amd64, arm64 and armhf. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
```

Notes for L1: kind `code` and tier `A` copy S106's convention (release assets of a primary vendor repo); change to `tool` if preferred (S001/S002 use `tool`). The `fix: …` quote contains `:` but no `|`. Row ends without a trailing `|`-after-used-by gap beyond the table pattern used by S100–S106 (`… | used-by |`) — add the closing `|` exactly as S106 does when appending.

## Limits
- Tag commit sha, release-asset signatures/attestations, and the sasquatch source were not examined.
- Release page rendering was read as served HTML (no JS); assets come from the API and the expanded_assets fragment.
