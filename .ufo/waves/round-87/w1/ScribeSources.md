# ScribeSources — round-87 SOURCES rows (R87-C1, UPX magic-tamper repair)

Seat: ScribeSources (scribe, leaf). Date: 2026-11-04. Candidates only; `corpus/SOURCES.md` not edited.

## Delivered
- `.ufo/waves/round-87/w1/ScribeSources/rows.md`: three candidate rows, S306, S307, S308, each 11 cells, no `|` inside any cell (checked by field count), status `mined`, opened 2026-11-04, recheck `180d`, used-by `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`.
- `.ufo/waves/round-87/w1/ScribeSources/gate.md`: 12 gate rows (quote, URL, access date, scoped use, absent -> mined), a p_unix.cpp non-admission note, and copy-ready gate lines.
- `.ufo/waves/round-87/w1/ScribeSources/notes.md`: fetch receipts (HTTP status, bytes, sha256, ETag, second-fetch equality), registry schema and id check, decisions, findings.
- `.ufo/waves/round-87/w1/ScribeSources/receipts/`: `verify_quotes.py` and `verify_quotes.out` (23 located strings, `bad= 0`), `fetch_sha256.txt`, `refetch_headers.txt`.

## Fetches (v5.2.0, live 2026-11-04, all HTTP 200, second fetch byte-identical)

| file | bytes | sha256 |
|---|---|---|
| src/stub/src/include/linux.h | 19689 | 5de99480d6cfdc5df463dfb21153cee4ed3ac2509bbf0d3558855d1655a03ea9 |
| src/p_lx_elf.cpp | 373743 | 551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc |
| src/packhead.cpp | 13236 | 41b4a51ba4d78429241e2c970565402287fd79360445013f955e2b4cf137f37a |
| src/p_unix.cpp (extra, not admitted) | 24181 | bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e |

## Registry
- Highest existing id: S305. Next ids: S306, S307, S308.
- Lane plan named two ids; a third (S308) is used because packhead.cpp is kept. Re-check the highest id at append time.

## Decisions
- S306 `linux.h`: admit. Quotes: `UPX_MAGIC_LE32` 0x21585055 at line 540; `struct l_info` line 579 with `l_magic` at 582; `b_info` `sz_cpr` at 572.
- S307 `p_lx_elf.cpp`: admit. Linux ELF unpack overrides at 7755 and 9023; trailer magic checks at 7778 and 9046; EOF check `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` at 8065 and 9310; loader-variance comment at 7993 and 9239.
- S308 `packhead.cpp`: admit, narrow scope. The checksum (`get_packheader_checksum`, lines 62-72) starts summing at byte 4 (`buf += 4;` line 65), so it never reads the `UPX!` magic. Not redundant with the other two. Scope limit: the Linux ELF header write path (`PackUnix::pack4` p_unix.cpp:278 → `writePackHeader` p_unix.cpp:97 → `patchPackHeader`, line 110) is not resolved in the fetched files, so whether an ELF header carries this checksum is unverified.
- p_unix.cpp: not admitted as a row. The same EOF line is at p_unix.cpp:671, inside base `PackUnix::unpack` (line 609). The Linux ELF classes define their own `unpack` in p_lx_elf.cpp; base `PackLinuxElf::unpack` (line 9334) throws `internal error`.

## Findings for L1 (reported, not repaired in frozen files)
1. Sibling entry candidate (`.ufo/waves/round-87/w1/ScribeEntry/candidate/corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`) cites S307 as `src/p_unix.cpp`. Its quoted line exists there only as the base-class copy (p_unix.cpp:671); the ELF-operative check and the "Getting past the loader" comment are in `src/p_lx_elf.cpp`. Recommend re-pointing S307's locator to p_lx_elf.cpp lines 8065 and 9310.
2. The entry must not assert that the Linux ELF PackHeader checksum covers or excludes the magic until `patchPackHeader` is located.
3. Scoped fact: a change to only the first four bytes of a PackHeader does not alter its checksum (packhead.cpp:65). That bears on the claim's tamper class only if finding 2 resolves to "ELF headers carry the checksum".
4. Scoped fact: a mismatched loader-trailer magic (p_lx_elf.cpp 7778) takes a blank-record re-read workaround (7780-7787) before `throwCantUnpack("l_info corrupted")`; the other branch (from 7788) was not read. The entry must not claim the mismatch path always refuses.
5. The sibling S306/S307 usage (linux.h; p_unix.cpp) is otherwise consistent with the rows; ids must be reconciled at append.

## Out of scope / not done
- The 2026-11-04 knowledge entry, the lesson `## Gate` section in the round file, and the SOURCES append itself: not written (L1).
- No tool installs. No git/jj mutation. No write to production paths, fleet root, `.ufo/state/`, MANIFEST.

Report: `.ufo/waves/round-87/w1/ScribeSources.md` (this file). Seat DONE marker: `.ufo/waves/round-87/w1/ScribeSources/DONE`.
