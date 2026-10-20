# SourceWabtRelease — WABT 1.0.42 release identity (round 20, w1)

Seat: `KaidokuR20.SourceWabtRelease-2` (read-only scribe). Written 2026-10-20T17:47:48-03:00.
Scope: identity of the WABT binaries that REA `inspect-wasm-artifact` runs (`wasm-validate`, `wasm-objdump`, `wasm2wat`).

## Sources opened

| # | URL | Access (write-time clock) | Document sha256 | Notes |
|---|---|---|---|---|
| 1 | https://github.com/WebAssembly/wabt/releases/tag/1.0.42 | 2026-10-20T17:47:01-03:00 (curl, HTTP 200, 255156 B) | `14692be371041c0794d358bc3180b8f235bae861852ea9ce186d2b2c45912cac` | Release HTML; body text read via `gh api repos/WebAssembly/wabt/releases/tags/1.0.42` (9976 B, sha256 `7d28358b…`) |
| 2 | `gh release view 1.0.42 -R WebAssembly/wabt --json assets` (GitHub API) | 2026-10-20 | n/a | Asset metadata: digests and sizes below |
| 3 | https://github.com/WebAssembly/wabt/releases/download/1.0.42/wabt-1.0.42-linux-x64.tar.gz.sha256 | 2026-10-20 (curl HTTP 200) | n/a | Content: `84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131  wabt-1.0.42-linux-x64.tar.gz` |
| 4 | https://github.com/WebAssembly/wabt/releases/download/1.0.42/wabt-1.0.42-linux-x64.tar.gz | 2026-10-20 (curl) | `84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131` | 4761911 B; `sha256sum -c` OK against the .sha256 asset |
| 5 | `gh api repos/WebAssembly/wabt/git/refs/tags/1.0.42` | 2026-10-20 | n/a | Tag object type `commit`, sha `ff0ef7e0009402740c805a9744c09b05be063e48` |
| 6 | `CMakeLists.txt` at `ff0ef7e0009402740c805a9744c09b05be063e48` (`gh api …/contents`) | 2026-10-20 | n/a | Line 18: `project(WABT LANGUAGES C CXX VERSION 1.0.42)` |
| 7 | rea-agents@6.5.0 npm tarball (`npm pack`), `rea/package/third_party/wabt/README.md` | 2026-10-20 | n/a | REA's own pin text: admitted release, source commit, runtime tools |

Asset digests (GitHub API, `digest` field): linux-x64 tarball `sha256:84895407…ab131`, size 4761911; linux-x64 `.sha256` `sha256:359dac13…9c88f`, size 95; linux-arm64 `a7632c1c…13ea8` (4817547 B); macos-arm64 `3f654779…1e240` (3695890 B).

Release metadata: name `1.0.42`, `isPrerelease=false`, `isDraft=false`, `publishedAt=2026-09-15T20:34:46Z`, `targetCommitish=main`, tag commit `ff0ef7e0009402740c805a9744c09b05be063e48`. Linux-x64 asset `createdAt=2026-09-15T20:36:45Z`.

## Quote (one contiguous, <=25 words)

> "Bump version to 1.0.42 by @sbc100 in https://github.com/WebAssembly/wabt/pull/2859"

Located: release body (`gh api repos/WebAssembly/wabt/releases/tags/1.0.42 -q .body`), section `## What's Changed`, line 79; the same entry appears in the tag page HTML under the Release 1.0.42 block (tag page text line ~545). Eight words.

Corroboration (not the quoted source): `CMakeLists.txt:18` at `ff0ef7e…` reads `project(WABT LANGUAGES C CXX VERSION 1.0.42)`.

## Observations (executed, scratch only)

- Extracted `wabt-1.0.42-linux-x64.tar.gz` into `/tmp/wabt-src-wqd2oo/wabt-1.0.42/` (system temp; not in lane). Tarball layout: `wabt-1.0.42/{bin,include,lib,share}`.
- `bin/wasm-validate --version` → `1.0.42`, sha256 `6b722ed0df68204cfc7a8effdf1fc2ddeac2d184bd211cdf7fdfa5f9d49d3eb5`.
- `bin/wasm-objdump --version` → `1.0.42`, sha256 `dad264def1a3b7755859c5bf48227f01259a95fa82b7c38358b12b9e70b27a41`.
- `bin/wasm2wat --version` → `1.0.42`, sha256 `4322d652f650c1ee117b549c9722f42fc93eb4676ff046d60ba033b5639697a5`.
- `bin/wat2wasm --version` → `1.0.42` (verification-fixture compiler only), sha256 `9e9ec8f737c890553951defcb1ee7f82de99fcafa32bef54990de27413794e7f`.
- Only upstream-released WABT binaries were executed (`--version` banners). No Go toolchain, no REA analyze/search/decompile, no Ghidra run.

## Installs / updates

None. Tools used were already present: `gh`, `curl`, `npm`, `tar`, `sha256sum`, `base64`. `npm pack rea-agents@6.5.0` wrote its tarball into the scratch dir only.

## Draft

SOURCES.md row (11-column registry shape; id placeholder `S0NN`, assigned at integration; target file `corpus/SOURCES.md`):

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | WABT 1.0.42 release — https://github.com/WebAssembly/wabt/releases/tag/1.0.42 (asset `wabt-1.0.42-linux-x64.tar.gz`, `.sha256` asset) | docs | A | Release identity of the upstream WABT 1.0.42 linux-x64 asset and its tag commit, which REA's `inspect-wasm-artifact` tools (`wasm-validate`, `wasm-objdump`, `wasm2wat`) are expected to come from; not operator-tool provenance and not runtime authenticity of any local copy | Release 1.0.42, tag commit `ff0ef7e0009402740c805a9744c09b05be063e48` (`CMakeLists.txt:18` `VERSION 1.0.42`); asset sha256 `84895407a6bbb80e918f33b16b2fb2206021c150b6bc9ff6f761263a745ab131`, 4761911 B; `.sha256` asset content matches; release body `What's Changed` line 79; fetched 2026-10-20 (tag page sha256 `14692be3…2cac`) | Lets a verifier tie a local `wasm-*` banner `1.0.42` and tarball hash to the published release asset, so the identity claim is checkable against upstream metadata rather than the adapter's own pin. | queued | 2026-10-20 | on-release | — |

Notes on the row: the release page supports identity of the published asset and tag; it does not authenticate any operator-supplied directory (REA's own `third_party/wabt/README.md` says the same: "Version admission ... does not certify publisher authenticity"). Keep the scope column so it is not read as a trust claim.

## Findings

1. Supported. The release page, the `.sha256` asset, the GitHub asset digest, and my local `sha256sum -c` all agree on `84895407…ab131` for the linux-x64 tarball (4761911 B). The tag `1.0.42` resolves to commit `ff0ef7e…`, which REA's README also names as the source commit.
2. Supported. The extracted `wasm-validate`, `wasm-objdump`, `wasm2wat` each print exactly `1.0.42`, matching the banner REA requires (`cli.js` `WABT_PROVIDER_IDENTITY.version = "wabt@1.0.42"`; README: "every version banner to report `1.0.42`").
3. Limit (not a finding against the source): the README's verification archive is the macOS arm64 asset (`3f654779…1e240`); this report did not run the macOS build. Linux-x64 identity rests on the GitHub asset digest plus the published `.sha256`, not on a reproducible rebuild from `ff0ef7e…`.
4. Limit: the release metadata shows `targetCommitish=main`; I did not verify the tag-to-main ancestry or rebuild the tarball from source.
5. Calibration: the release page alone is enough for the release-identity scope. Publisher authenticity is out of scope and the row says so.

## Residual unknowns

- No checksum from an independent channel (e.g., signed release) was located on the release page; only GitHub-hosted `.sha256` and API digests were observed.
- `rea-agents@6.5.0` runtime code path that actually invokes these binaries was not traced here (out of seat scope).
