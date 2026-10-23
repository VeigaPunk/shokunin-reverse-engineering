# WSourceHeaders — S102 re-verification of the official served PE Format Markdown

Seat: KaidokuR33.WSourceHeaders (leaf, builder-free wave w1). Date: 2026-10-23.
Scope: re-open the official Microsoft PE Format served Markdown, verify S102 scoped
header/signature bounds and the exact line-133 quote (13 words), compare current capture
hash/location, confirm S100 stays a distinct CHPE-authority rejection (no source reversal),
and check the optional-header size / directory-count and 96-section statements as stated
spec text only — no Windows run is observed or inferred.
Relation to R33-C1: evidence only. The original claim remains STOPPED UNPROVABLE
(`.ufo/waves/round-33/claim-stop.json`); nothing here is a replacement benchmark or a
revived carrier claim.

## Result

VERIFIED on all four assigned points; no actionable defect found.

1. Capture custody (hash/location): byte-identical.
2. Line-133 quote: present, exact 13 words, at the pinned location.
3. S102 scoped bounds: every cited range contains the claimed statement; stated limits only.
4. S100 non-reversal: sweep regex finds zero matches in both the retained capture and the
   fresh live fetch; S100's row, status and flip are unchanged in `corpus/SOURCES.md:106`.

## 1. Capture re-open and hash/location comparison

Fresh fetch of the exact pinned URL
`https://learn.microsoft.com/en-us/windows/win32/debug/pe-format?accept=text/markdown`
at 2026-10-23T09:31:48Z (curl, argv in §5):

- HTTP/2 200; `content-type: text/markdown; charset=utf-8`; `content-length: 183798`.
- sha256 `563f2dd952e16ca836036189ee82e46f1dbde29d716ee4ea5d2277e9562609d8`, 183798 bytes.
- `cmp` retained lane capture vs live fetch: exit 0 (byte-identical).
- Response headers: `etag: "TBVhWHnP+RVfazzPbjGjDFZvjFc="`,
  `last-modified: Thu, 10 Sep 2026 16:04:34 GMT`,
  `akamai-cache-status: Miss from child, Hit from parent`, `date: Fri, 23 Oct 2026 09:31:48 GMT`.

Comparison against the recorded current capture:

| Record | Recorded sha256 / bytes | Observed | Match |
|---|---|---|---|
| `.ufo/waves/round-33/pe-source-capture.json` | 563f2dd9…2609d8 / 183798, accessed 2026-10-23T08:37:23Z | same hash and size on re-fetch 09:31:48Z | yes |
| `.ufo/waves/round-33/source-anchor-map.json` (pe-format.md) | 563f2dd9…2609d8 | same | yes |
| `.ufo/waves/round-33/document-spec.json` file_sha256 | 563f2dd9…2609d8 | same | yes |
| `corpus/SOURCES.md:108` S102 row | 563f2dd9…2609d8, opened 2026-10-23 | same | yes |

Location `corpus/evidence/round-33/sources/pe-format.md:133-141,222-224` (S102 row) verified
against the file: the cited ranges contain exactly the header/signature and probe-bound
content (§3). Upstream document has not changed since at least 2026-09-10 (last-modified)
and is byte-stable across the two same-day fetches (08:37:23Z, 09:31:48Z).

## 2. Line-133 quote (13 words)

Retained capture line 133 (232 chars) begins with exactly:

> At location 0x3c, the stub has the file offset to the PE signature.

- Word count of the quoted sentence: 13 (whitespace split), as pinned in
  `.ufo/waves/round-33/quote-manifest.json`.
- Verified as a prefix of line 133 in both the retained capture and the live fetch
  (byte-identical files, so location holds for both).
- Rest of line 133: "This information enables Windows to properly execute the image file,
  even though it has an MS-DOS stub. This file offset is placed at location 0x3c during
  linking." — consistent with the S102 scope (signature location via 0x3c), no CHPE content.
- `document-spec.json` `file_quote` check (path, line 133, quote) reproduces exactly.

## 3. S102 scoped header/signature bounds and stated limits

All statements below are read as documented spec text in the served Markdown. No Windows
loader or loader-family binary was run; no runtime behavior is claimed or inferred.

| Line(s) | Statement (verbatim, abridged where marked) | S102 scope element |
|---|---|---|
| 133 | "At location 0x3c, the stub has the file offset to the PE signature." | DOS/PE signature location |
| 135-137 | `### Signature (Image Only)`; 4-byte "PE\0\0" signature "at the file offset specified at offset 0x3c" | signature bound |
| 139-141 | `### COFF File Header (Object and Image)`; line 141: "Note that the Windows loader limits the number of sections to 96." | stated section-count limit (96) |
| 150 | COFF table row `16 / 2 / SizeOfOptionalHeader` — "The size of the optional header … required for executable files but not for object files … zero for an object file" | optional-header size field |
| 218-222 | `### Optional Header (Image Only)`; line 222: "the size of the optional header is not fixed. The **SizeOfOptionalHeader** field … must be used to validate that a probe into the file for a particular data directory does not go beyond **SizeOfOptionalHeader**." | optional-header probe bound |
| 224 | "The **NumberOfRvaAndSizes** field … should also be used to ensure that no probe for a particular data directory entry goes beyond the optional header." | directory probe bound |
| 290 | Windows-Specific table row `92/108 / 4 / NumberOfRvaAndSizes` — "The number of data-directory entries in the remainder of the optional header." | directory-count field |
| 335-348 | `#### Optional Header Data Directories (Image Only)`; 337: 8-byte data directory intro; line 348: "the number of directories is not fixed. Before looking for a specific directory, check the NumberOfRvaAndSizes field" | directory-count bound |
| 352-369 | Directory table: 16 entry rows (`96/112` Export Table … `216/232` Reserved), each size 8 | directory count = 16 as listed |

The S102 row's use note "Locate the PE signature via 0x3c and bound directory probes by the
declared optional-header size; no CHPE offset/tag definition is inferred" is exactly what
the cited lines support. The 96-limit is a stated loader limit in the spec text; it was not
exercised against any Windows system.

## 4. S100 remains a distinct CHPE-authority rejection — not reversed

- Sweep regex as recorded in `corpus/lessons/round-33.md`,
  `CHPE|CHPEMetadataPointer|0[xX][cC]8|code.?map`, case-sensitive, run over (a) the retained
  lane capture and (b) the fresh live fetch: **zero matches in both**. A stricter
  case-insensitive rerun of the same pattern also found zero matches.
- `corpus/SOURCES.md:106` (S100) is unchanged: status REJECTED, scope still "Candidate
  authority for CHPEMetadataPointer offset 0xC8 and code-map bit tags only", flip preserved
  ("later versions of both representations explicitly document the CHPE fiel[ds/tags]").
- S100's evidencing representations are distinct from S102's: S100 cites the round-32 served
  HTML (`d0c584f1…42a6f0b1`) and the GitHub Markdown (`b17271a3…56a2fe0`); S102 cites the
  served `text/markdown` capture (`563f2dd9…2609d8`). Today's byte-identical re-open of the
  third representation does not satisfy or approach S100's flip condition; S102 admits a
  different scope (header boundaries), so the rejection stands and no prior row's status,
  recheck or used-by changed.

## Findings by severity

- Critical / Major: none.
- Minor: none.
- Informational:
  - INF-1: The S102 registry row cites `pe-format.md:133-141,222-224`. Those ranges cover
    signature location, probe bounds and the 96-section statement. The 16-directory count
    and its "not fixed / check NumberOfRvaAndSizes" statement sit at lines 290 and 348-369,
    outside the cited ranges. Anyone later citing S102 for the directory count should cite
    those lines, not 222-224. This is a citation-hygiene note, not a defect in the row.
  - INF-2: S100's flip is worded over "both representations" (HTML, GitHub Markdown). The
    S102 capture is a third representation (served `text/markdown`). The flip predicate was
    not triggered on it today (zero CHPE matches), but a future flip evaluation should treat
    each representation explicitly.
  - INF-3: Both same-day fetches were served through Akamai edge caching (parent hit on the
    second). Bytes and etag were stable and `last-modified` predates both, so this does not
    weaken the comparison; it only means a later re-open could trail upstream edits briefly.

## Residual risk and verification gaps

- Re-open replication is two same-day fetches of one URL from one edge; a later content
  change would require re-pinning S102's sha/location (the row already carries the 90d
  recheck cadence). Not a defect today.
- S100's two round-32 representations were not re-opened in this seat (outside seat scope);
  only their unchanged registry row was read.
- The 96-section limit and directory count are verified as spec statements only; per
  assignment, no Windows run was performed, so no loader behavior is evidenced.
- No tool install or update was performed: system `curl`, `python3`, `awk`, `cmp`, `tee`
  were sufficient; pacman is host-paused and no channel upgrade was needed. Nothing was
  installed to record beyond this choice.

## Receipts (scratch: /fast/scratch/hyaku/kaidoku-r33/w1/WSourceHeaders/)

- `pe-format-live.md` — fresh fetch, sha256 563f2dd9…2609d8, 183798 bytes.
- `receipts/live-headers.txt` — full response headers of the 09:31:48Z fetch.
- `receipts/line-check-receipt.txt` — merged receipt: argv results, word count (13),
  line-133 prefix check (true, both files), sweep-adjacent line pins (141, 150, 222, 224,
  290, 348, 352-369), cmp exit 0, data-directories entry rows = 16; START/END UTC stamps
  2026-10-23T09:31:48Z (fetch), 09:34:39Z (quote/line checks), 09:35:13Z and 09:36:35Z
  (directory section). Executed commands: `curl -sS --max-time 60 -D …/live-headers.txt -o
  …/pe-format-live.md '<url>'`; `cmp -s <retained> <live>`; `sha256sum`/`wc -c` on both;
  `awk` line-range prints on the retained capture; python3 read-only scanners over both
  captures (no lane writes; single short-lived subprocesses, all exited, no process left
  running). No git/jj command touched the lane; no lane file was modified.
