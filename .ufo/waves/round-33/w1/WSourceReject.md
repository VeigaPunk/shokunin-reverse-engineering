# WSourceReject

Decision: **S100 rejection retained.** No changed finding. No flip. This is not a new source row, not loader behavior, and not a replacement for stopped R33-C1.

Question: does the Microsoft PE Format specification document `CHPEMetadataPointer` at PE32+ offset 200/`0xC8`, and numeric code-map tag bit meanings?

## Surfaces

| surface | role this seat | identity |
|---|---|---|
| fresh served Markdown | live reopen | `https://learn.microsoft.com/en-us/windows/win32/debug/pe-format?accept=text/markdown` |
| retained served Markdown | same bytes as the fresh body | `corpus/evidence/round-33/sources/pe-format.md` |
| retained docs Markdown | S100 representation, not re-fetched | `corpus/evidence/round-32/sources/pe-format.md` |
| retained HTML | S100 representation, not re-fetched | `corpus/evidence/round-32/sources/pe-format.html` |

Fresh fetch: HTTP 200, `content-type: text/markdown; charset=utf-8`, `content-length: 183798`, response `Date: Fri, 23 Oct 2026 09:30:11 GMT`, `last-modified: Thu, 10 Sep 2026 16:04:34 GMT`. Body front matter: `ms.date: 2026-09-10T00:00:00.0000000Z`, `git_commit_id: 55e845e9f3a6a3261f59a2f460f61edc25ffcdd5`. That git blob was not fetched. The live docs-branch tip and live HTML were not re-fetched; the assignment allowed retained source only.

| file | sha256 | bytes |
|---|---|---|
| fresh `pe-format-learn.md` | `563f2dd952e16ca836036189ee82e46f1dbde29d716ee4ea5d2277e9562609d8` | 183798 |
| retained round-33 `pe-format.md` | `563f2dd952e16ca836036189ee82e46f1dbde29d716ee4ea5d2277e9562609d8` | 183798 |
| retained round-32 `pe-format.md` | `b17271a341f9b6e3204cf3f04ed905c25c03fd4cadb7a57bd4aaf38cf56a2fe0` | 335441 |
| retained round-32 `pe-format.html` | `d0c584f14a3a464c45f3544d35cd0146cc6bf480aeb2e47ce5c3fcab42a6f0b1` | 282123 |

The fresh body is byte-identical to the round-33 capture (`source-pins.json` / S102 hash). The two round-32 hashes equal the S100 registry pins.

## Census

Same absence on all four files. Counts are case-sensitive except where noted. L1 pattern `CHPE|CHPEMetadataPointer|0[xX][cC]8|code.?map` is 0 matches on each file. Census finished 2026-10-23T09:31:07Z.

| token | fresh / r33 md | r32 md | r32 html |
|---|---|---|---|
| `CHPEMetadataPointer` | 0 | 0 | 0 |
| `CHPE` / `chpe` | 0 | 0 | 0 |
| `MetadataPointer` | 0 | 0 | 0 |
| `CodeMap`, `code map`, `code-map` | 0 | 0 | 0 |
| `0xC8` / `0xc8` | 0 | 0 | 0 |
| `range type`, `range-tag`, `StartOffset` | 0 | 0 | 0 |
| `DynamicValueReloc` | 0 | 0 | 0 |

Present, and not the rejected claim:

| token | fresh / r33 | r32 md | r32 html |
|---|---|---|---|
| `ARM64EC` | 166, 167 | 130, 131 | 962, 969 |
| `ARM64X` | 167 | 131 | 967 |
| `GuardLongJumpTargetCount` | 1682 | 1961 | 5409 |
| `low 2 bits` | 570 | 560 | 2340 |
| `HYBRIDMAP` | 1856 | 2183 | 5756 |

## Located quote

Contiguous cell text, 16 words, under the 25-word limit. It documents the ARM64X machine value, not a load-config offset or a code-map tag.

Fresh and retained round-33 Markdown, line 167, value `0xA64E`:

> Binary format that allows both native ARM64 and ARM64EC code to coexist in the same file.

Same sentence: retained docs Markdown line 131; retained HTML line 969, one `td` (value cell line 968 is `0xA64E`).

Load Configuration Layout, fresh/r33 line 1649 (14 words): “The load configuration structure has the following layout for 32-bit and 64-bit PE files:” The last row, line 1682, is separate cells `116/184`, `4/8`, `GuardLongJumpTargetCount`. Line 1684 starts GuardFlags prose. No later layout row. Retained docs Markdown ends the same table at line 1961 with those cells. No `CHPEMetadataPointer` row and no offset cell `200` or `0xC8` in that table.

## Near misses (not a flip)

- Decimal `200` in the fresh/r33 body is the optional-header data directory: line 365 `184/200` Bound Import; line 367 `200/216` Delay Import Descriptor; line 1100 “optional header data directories list (offset 200)” for that Delay Import slot. Line 172 `0x200` is `IMAGE_FILE_MACHINE_IA64`. None is a load-config CHPE field.
- Line 1691 `0x00000200` is `IMAGE_GUARD_CFW_INSTRUMENTED`. It is not `0xC8`.
- Line 570, the only “low 2 bits” hit: “The low 2 bits of the displacement are zero and are not stored.” (13 words), on `IMAGE_REL_THUMB_BLX23`. Not a code-map tag.
- Line 1856 `IMAGE_ARCHIVE_HYBRIDMAP_MEMBER` / `/<HYBRIDMAP>/` is an archive member name. Not a code map.

## Flip

Unchanged from the S100 row in `corpus/SOURCES.md`: later versions of **both** representations explicitly document the CHPE field at PE32+ offset 200/`0xC8` **and** numeric range-tag bit meanings. One conjunct, or a different page, does not flip it.

Neither conjunct is in the fresh served Markdown or in either retained S100 representation. S102’s header scope is untouched. No source-registry write.

## Limits

Live HTML and the live `MicrosoftDocs/win32` docs Markdown tip were not re-fetched. Their retained bytes still match the S100 pins and still omit both conjuncts; a later change on those two URLs is unchecked here. `winnt.h` was not opened. Nothing here is Windows loader behavior. No tool was installed. Original claim R33-C1 stays stopped.

## Argv

```
date -u +%Y-%m-%dT%H:%M:%SZ
# 2026-10-23T09:30:11Z
mkdir -p /fast/scratch/hyaku/kaidoku-r33/w1/WSourceReject
curl -fsSL --retry 3 --retry-delay 2 -A 'kaidoku-r33-w1/WSourceReject' \
  -D pe-format-learn.headers -o pe-format-learn.md \
  -w 'learn_md http=%{http_code} size=%{size_download} type=%{content_type} url=%{url_effective} time=%{time_total}\n' \
  'https://learn.microsoft.com/en-us/windows/win32/debug/pe-format?accept=text/markdown'
# learn_md http=200 size=183798 type=text/markdown; charset=utf-8 url=https://learn.microsoft.com/en-us/windows/win32/debug/pe-format?accept=text/markdown time=0.321864
# end 2026-10-23T09:30:11Z
sha256sum pe-format-learn.md \
  corpus/evidence/round-33/sources/pe-format.md \
  corpus/evidence/round-32/sources/pe-format.md \
  corpus/evidence/round-32/sources/pe-format.html
# hashes in the table above; exit 0
```

Token counts are a stdlib Python scan of those four files, exit 0, finished 2026-10-23T09:31:07Z. Scratch copy: `/fast/scratch/hyaku/kaidoku-r33/w1/WSourceReject/pe-format-learn.md`.

Report: `.ufo/waves/round-33/w1/WSourceReject.md`
