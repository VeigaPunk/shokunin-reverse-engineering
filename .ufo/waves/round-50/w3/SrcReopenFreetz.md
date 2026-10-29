# SrcReopenFreetz — round-50 attempt-2, wave 3, seat report (2026-10-29)

## Verdict

**MET (exit 0).** The Freetz AVM_LE/AVM_BE symbols-only patch (planned SOURCES row **S243**) re-opens clean: HTTP 200 at `2026-10-29T20:32:26Z`, **1,153 B**, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707` — byte-identical to the attempt-1 record (1,153 B, `e28b3341…`, opened 2026-10-28T23:31:54Z; `cmp` exit 0 against the lane snapshot `.ufo/waves/round-50/w1/C1SrcFreetz/sources/`). **The row can be registered this round as planned** (tier B, kind code, scope "AVM LE/BE symbol definitions", teaches "supersedes nothing; new row"): both attempt-1 Gate quotes still locate at exactly the cited lines, and the source has now been observed byte-identical across three fetches over four days (R42 2026-10-26, R50-w1 2026-10-28, this re-open 2026-10-29).

## Findings

| # | Check | Exact command | Exit | Observed |
|---|-------|---------------|------|----------|
| 1 | Host capacity before the pass | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | 0 | `/fast/scratch/hyaku` 39% use, 495.7 G free — no pressure |
| 2 | Fetch S243 source | `curl -sS -o $S/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch -w 'http_code=%{http_code} size_download=%{size_download}\n' https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch; echo curl_exit=$?` | 0 | `http_code=200 size_download=1153` at UTC `2026-10-29T20:32:26Z` |
| 3 | Hash / size / line count | `sha256sum <out>`; `stat -c 'bytes=%s' <out>`; `wc -l <out>` | 0 | `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`; 1153 B; 27 lines (attempt-1 said "27 lines" — matches) |
| 4 | Byte-identity vs attempt-1 | `cmp $S/101-…patch /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/w1/C1SrcFreetz/sources/101-…patch && echo cmp_exit=0_identical` (with `sha256sum` on both) | 0 | identical; both hash `e28b3341…c707` |
| 5 | Gate quote, line 7 | numbered grep `AVM_LE` on the fetched body | 0 | `7\|+#define AVM_LE 2` — locates exactly as cited |
| 6 | Gate quote, lines 17-18 | same grep | 0 | `17\|+#if   defined(TARGET_FORMAT) && (TARGET_FORMAT == SQUASHFS4_LE \|\| TARGET_FORMAT == AVM_LE)` / `18\| #define TARGET_FORMAT_BYTE_ORDER __LITTLE_ENDIAN` — the byte-order condition names **both** `SQUASHFS4_LE` and `AVM_LE` and selects `__LITTLE_ENDIAN`, exactly as cited |
| 7 | Seat-dir copy | `cp $S/101-…patch <seat>/ && sha256sum <seat>/101-…patch` | 0 | copy hashes identical, 1153 B |

## Registration statement

Row S243 is registration-ready this round as planned:
- **Unchanged source**: HTTP 200, 1,153 B, `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707` — identical to the attempt-1 receipt cited by the entry text (`re-read 2026-10-28 (1,153 B, sha256 e28b3341…)` in `tools/`-side landing drafts and to all prior round-39/40/42 receipts), so no landing text needs a hash/date update beyond the re-open date itself.
- **Quotes locate**: `:7` `+#define AVM_LE 2` and `:17`-`:18` the byte-order condition naming `SQUASHFS4_LE` or `AVM_LE` selecting `__LITTLE_ENDIAN` — both verified on today's bytes, line-for-line.
- **Row content supported**: under its symbols-only name the patch adds the `AVM_LE`/`AVM_BE` define values and maps `AVM_LE` to little-endian byte order — and nothing else (no marker write, no layout text, no id-table change; the marker writer is patch 550, a different file). Tier B, kind code, scope "AVM LE/BE symbol definitions", teaches "supersedes nothing; new row" all hold against today's body.
- The id **S243** is the one already minted for this source in `plans/round-50-attempt2-claims.md` (opened 2026-10-28, "re-opened 2026-10-29 this attempt"; S150–S242 skipped as never-registered staged ids) — the w1 draft's provisional S150 label was already resolved; no collision remains. This report plus the receipt provide the fresh 2026-10-29 re-open evidence the claims file calls for.

## Artifacts (seat dir `.ufo/waves/round-50/w3/SrcReopenFreetz/`)

- `101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch` — verbatim fetched body, 1153 B, sha256 `e28b3341…c707`
- `copy-receipt.md` — command, exit code, sha256, UTC time, byte-identity result
- (this file is the seat report `SrcReopenFreetz.md`)

## Notes and limits

- No REA invoked; no mutating git command run; nothing written outside the seat dir, the seat report, and scratch. Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenFreetz` removed after copying receipts.
- Attempt-1 Gate-quote provenance: the R42 (2026-10-26) and R50-w1 (2026-10-28) receipts in the lane already recorded the same body (`AVM_BE_AVM_LE` 0 hits in body; defines at body lines 7-8); this seat re-derived those line locations from today's fetch rather than trusting them.
- `.ufo/waves/round-50/l1/srcs-attempt2/` does not exist yet (checked; L1 creates it at landing) — no conflict; my receipts are independent.

## Tool installs / updates

None. No tool install or upgrade was needed for this seat; pacman untouched (guard respected).
