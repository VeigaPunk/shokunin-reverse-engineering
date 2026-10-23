# A2SourceReject

UTC evidence window: 2026-10-23T06:45:36Z through 2026-10-23T06:47:47Z.
Decision subject: Microsoft PE Format specification only.
Registry: not written. No `corpus/SOURCES.md` edit. No S-id assigned.

## Decision

REJECT for this scope: the opened PE Format specification does not document `CHPEMetadataPointer` at offset `0xC8`, and it does not document CHPE code-map bit types.

Not a page rejection. The same bytes do document COFF machine `IMAGE_FILE_MACHINE_ARM64EC` = `0xA641` and `IMAGE_FILE_MACHINE_ARM64X` = `0xA64E`. Those sentences are not the offset and not the bit types.

Search target, lane instrument, not this spec (`tools/round-32/arm64x_oracle.py`, read this session): line 7 "range type in its low 2 bits: 0 ARM64, 1 ARM64EC, 2 AMD64" (13 words); line 86 reads a qword at `lc + 0xC8`. Those lines name what was searched for. They are not Microsoft text.

## Flip

Admit these two facts from this specification only if a later fetch of both URLs below contains both of the following in that file:

1. A Load Configuration Layout row whose field cell is `CHPEMetadataPointer` and whose offset cell states the 64-bit/PE32+ offset as `200` or `0xC8` (the cell text, not a sum inferred past the last row).
2. A definition of CHPE or ARM64EC code-map range tags: the bit position and the numeric values for the ARM64, ARM64EC, and x64/AMD64 kinds.

One conjunct does not flip. Another URL (Arm64X article, winnt.h, LLVM, a blog) does not flip this decision; that is a different source. The winnt.h page opened below names the field and still fails both conjuncts.

## What was opened

| bytes | sha256 | size | identity |
|---|---|---|---|
| scratch `pe-format.html` | `d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1` | 282123 | `https://learn.microsoft.com/en-us/windows/win32/debug/pe-format` HTTP 200 at 2026-10-23T06:45:57Z |
| scratch `pe-format.md` | `b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0` | 335441 | `https://raw.githubusercontent.com/MicrosoftDocs/win32/docs/desktop-src/Debug/pe-format.md` HTTP 200 at 2026-10-23T06:45:57Z |
| git blob of that md | git sha1 `9d81b6b3ee7a65f171981a698984be200b9fa37a` | 335441 | same sha as GitHub contents API `desktop-src/Debug/pe-format.md` on `MicrosoftDocs/win32` ref `docs` (API file size 335441) |
| scratch `load-config64.md` | `27c3fdea2939abd3aabc0ef24234484fb2a823b92c44328f8f4e3ac690acea20` | 7164 | winnt.h API page, not the PE spec. Raw `MicrosoftDocs/sdk-api` `docs` `sdk-api-src/content/winnt/ns-winnt-image_load_config_directory64.md` HTTP 200 |

HTML meta, observed in `pe-format.html`: `ms.date` `2026-09-10T00:00:00Z`; `updated_at` `2026-09-10T15:41:00Z`; `git_commit_id` `55e845e9f3a6a3261f59a2f460f61edc25ffcdd5`; `original_content_git_url` `https://github.com/MicrosoftDocs/win32-pr/blob/live/desktop-src/Debug/pe-format.md`.

Docs-branch commits for that path (API HTTP 200): `ca8274decead49403d70ceeed4af8d4ca74eaf11` `2026-10-08T15:26:36Z` "Clarify optional header descriptions in pe-format.md (#2227)"; then `8a9c5d8f32001411f5e572a17e6d736d6fcc055f` `2026-07-16T16:54:38Z`; then `856f63ffa7273a9c617c83833ec91cf73d5f20ab` `2026-06-04T14:54:09Z`. The searched markdown is the `docs` tip of that path, later than the live page meta date.

`MicrosoftDocs/win32-pr` contents API and raw URL for commit `55e845e9f3a6a3261f59a2f460f61edc25ffcdd5` both HTTP 404 (body `Not Found`). That commit was not hashed. The served HTML was searched instead.

GitHub code search `CHPEMetadataPointer repo:MicrosoftDocs/win32` and `repo:MicrosoftDocs/sdk-api` both HTTP 401. Not used as absence evidence.

Debug directory listing `https://api.github.com/repos/MicrosoftDocs/win32/contents/desktop-src/Debug?ref=docs` HTTP 200, 122 entries. Name filter `pe|coff|load|arm|chpe|hybrid` returned symbol-loading pages plus `pe-format.md` only. No second PE-spec file in that listing.

Scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourceReject`. `df -h /fast` at 2026-10-23T06:45:36Z: 243G avail, 70% used. No lane clone. No tool install. No carrier execution. No Git write.

## Search counts

Same counts on `pe-format.md` and `pe-format.html` (census 2026-10-23T06:47:11Z):

| token | pe-format.md | pe-format.html | load-config64.md |
|---|---|---|---|
| CHPEMetadataPointer | 0 | 0 | 1 |
| CHPE / chpe | 0 | 0 | 1 |
| MetadataPointer | 0 | 0 | 2 |
| CodeMap | 0 | 0 | 0 |
| code map | 0 | 0 | 0 |
| code-map | 0 | 0 | 0 |
| 0xC8 / 0xc8 | 0 | 0 | 0 |
| 0xC0 / 0xc0 | 0 | 0 | 0 |
| ARM64EC | 2 | 2 | 0 |
| ARM64X | 1 | 1 | 0 |
| hybrid | 2 | 2 | 0 |
| HYBRIDMAP | 2 | 2 | 0 |
| DynamicValueReloc | 0 | 0 | 3 |
| GuardLongJumpTargetCount | 1 | 1 | 1 |
| range type | 0 | 0 | 0 |
| low 2 bits | 1 | 1 | 0 |
| IMAGE_ARM64EC | 0 | 0 | 0 |
| arm64x-pe | 0 | 0 | 0 |

`116/184` occurs once in `pe-format.md` (line 1961). `GuardLongJumpTargetCount` occurs once (line 1961).

## Quotes

Re-opened against `pe-format.md` sha256 `b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0` unless noted. Each quote is one contiguous run, at most 25 words.

- Line 130, Machine Types: "ABI that enables interoperability between native ARM64 and emulated x64 code." (11). HTML line 964, one `td`.
- Line 131: "Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file." (16). HTML line 969, one `td`, value cell on line 968 is `0xA64E`.
- Line 1926, Load Configuration Layout: "The load configuration structure has the following layout for 32-bit and 64-bit PE files:" (14).
- Line 1961, last row of that table, separate cells, not one spliced sentence: offset `116/184`; size `4/8`; field `GuardLongJumpTargetCount`. HTML lines 5407-5411, then `</table>` at 5413. No later layout row.
- Line 560, only "low 2 bits" hit: "The low 2 bits of the displacement are zero and are not stored." (13). Same line names `IMAGE_REL_THUMB_BLX23`. Not a code-map type.
- Line 2174 and 2183, Archive File Signature: "The Windows SDK winnt.h header defines the following macros:" (9) and the macro `IMAGE_ARCHIVE_HYBRIDMAP_MEMBER` with replacement `"/<HYBRIDMAP>/   "`. Both `hybrid` hits are these two `HYBRIDMAP` spellings on line 2183.

`load-config64.md` line 9: `ms.date: 12/05/2018`. Line 58: "Contains the load configuration data of an image." (7). Lines 163-167 are consecutive headings `DynamicValueRelocTable`, then `CHPEMetadataPointer`, then `GuardRFFailureRoutine`, with blank lines only between them. The embedded struct in that file ends at `SEHandlerCount` (lines 193-215) and has no `CHPEMetadataPointer` member.

## Inference

The load-config table header on line 1930 says `Offset`, not `Offset (PE32/PE32+)`. Other tables in the same file use the slash form under the header "Offset (PE32/PE32+)" (line 201). If that convention applies, the last field starts at PE32+ offset 184 with size 8, so the documented bytes end at 192 (`0xC0`). `0xC8` is 200. That sum is not in the spec. The reject does not depend on it: the field name, `0xC8`, and code-map type tags are absent as strings.

Decimal `200` does occur elsewhere. Data-directory line 329 is `184/200` for Bound Import, not a load-config CHPE row.

## Argv and exits

```
date -u +%Y-%m-%dT%H:%M:%SZ
# 2026-10-23T06:45:36Z
df -h /fast
# /dev/nvme1n1p2  804G  561G  243G  70% /fast
mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2SourceReject
```

```
curl -fsSL --retry 3 --retry-delay 2 -A 'kaidoku-a2audit/1.0' -o pe-format.html -w 'learn_html http=%{http_code} size=%{size_download} url=%{url_effective}\n' 'https://learn.microsoft.com/en-us/windows/win32/debug/pe-format'
# learn_html http=200 size=282123 url=https://learn.microsoft.com/en-us/windows/win32/debug/pe-format
curl -fsSL --retry 3 --retry-delay 2 -A 'kaidoku-a2audit/1.0' -o pe-format.md -w 'raw_md http=%{http_code} size=%{size_download}\n' 'https://raw.githubusercontent.com/MicrosoftDocs/win32/docs/desktop-src/Debug/pe-format.md'
# raw_md http=200 size=335441
curl -fsSL --retry 3 --retry-delay 2 -A 'kaidoku-a2audit/1.0' -o debug-dir.json -w 'api_dir http=%{http_code} size=%{size_download}\n' 'https://api.github.com/repos/MicrosoftDocs/win32/contents/desktop-src/Debug?ref=docs'
# api_dir http=200 size=119090
curl -fsSL --retry 3 --retry-delay 2 -A 'kaidoku-a2audit/1.0' -o load-config64.md -w 'winnt_md http=%{http_code} size=%{size_download}\n' 'https://raw.githubusercontent.com/MicrosoftDocs/sdk-api/docs/sdk-api-src/content/winnt/ns-winnt-image_load_config_directory64.md'
# winnt_md http=200 size=7164
sha256sum pe-format.html pe-format.md debug-dir.json load-config64.md
# d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1  pe-format.html
# b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0  pe-format.md
# 8903ad762fac04b57a97e5ef7d4f3ff16f9272768e3e47153b74e94f5f424810  debug-dir.json
# 27c3fdea2939abd3aabc0ef24234484fb2a823b92c44328f8f4e3ac690acea20  load-config64.md
# date after sha256sum: 2026-10-23T06:45:57Z
```

```
curl -fsSL --retry 3 -A 'kaidoku-a2audit/1.0' -o pe-format-commits.json -w 'commits http=%{http_code} size=%{size_download}\n' 'https://api.github.com/repos/MicrosoftDocs/win32/commits?path=desktop-src/Debug/pe-format.md&sha=docs&per_page=3'
# commits http=200 size=14124
curl -fsSL -G --retry 3 -A 'kaidoku-a2audit/1.0' --data-urlencode 'q=CHPEMetadataPointer repo:MicrosoftDocs/win32' -o gh-chpe.json -w 'gh_chpe http=%{http_code} size=%{size_download}\n' 'https://api.github.com/search/code'
# curl: (22) The requested URL returned error: 401
# gh_chpe http=401 size=0
curl -fsSL -G --retry 3 -A 'kaidoku-a2audit/1.0' --data-urlencode 'q=CHPEMetadataPointer repo:MicrosoftDocs/sdk-api' -o gh-chpe-sdk.json -w 'gh_sdk http=%{http_code} size=%{size_download}\n' 'https://api.github.com/search/code'
# curl: (22) The requested URL returned error: 401
# gh_sdk http=401 size=0
```

```
curl -fsSL --retry 3 --retry-delay 2 -A 'kaidoku-a2audit/1.0' -o pe-format-55e845e9.md -w 'live_blob http=%{http_code} size=%{size_download} url=%{url_effective}\n' 'https://raw.githubusercontent.com/MicrosoftDocs/win32-pr/55e845e9f3a6a3261f59a2f460f61edc25ffcdd5/desktop-src/Debug/pe-format.md'
# curl: (22) The requested URL returned error: 404
# live_blob http=404 size=0 url=https://raw.githubusercontent.com/MicrosoftDocs/win32-pr/55e845e9f3a6a3261f59a2f460f61edc25ffcdd5/desktop-src/Debug/pe-format.md
curl -sS -A 'kaidoku-a2audit/1.0' -o win32pr-contents.json -w 'api http=%{http_code} size=%{size_download}\n' 'https://api.github.com/repos/MicrosoftDocs/win32-pr/contents/desktop-src/Debug/pe-format.md?ref=55e845e9f3a6a3261f59a2f460f61edc25ffcdd5'
# api http=404 size=127
curl -sS -A 'kaidoku-a2audit/1.0' -o win32pr-repo.json -w 'repo http=%{http_code} size=%{size_download}\n' 'https://api.github.com/repos/MicrosoftDocs/win32-pr'
# repo http=404 size=118
```

Token census and quote reopen were Python 3 stdlib over those saved files (no package install), exits 0, at 2026-10-23T06:47:11Z, 2026-10-23T06:47:28Z, and 2026-10-23T06:47:47Z. Counts and quote line hits are the tables above. `git_blob_sha1 9d81b6b3ee7a65f171981a698984be200b9fa37a` computed as SHA1 of `blob <len>\0` plus `pe-format.md` bytes.

Tools installed: none.

.ufo/waves/round-32/a2audit/A2SourceReject.md
