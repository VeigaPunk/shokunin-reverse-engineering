# ScoutSources — R99-C2 source attack (kaidoku round 99, wave w1)

Item: independently fetch UPX v5.2.0 `packer.cpp`/`pefile.cpp`, compare with S326/S324 rows
at Bk and the pre/ copies, verify the quoted lines and the refusal rule, map earlier
short-file checks, and draft one further primary source or a rejection.
Scratch: /fast/scratch/hyaku/kaidoku-r99/ScoutSources (deleted after receipt copy).
Receipts: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-99/w1/ScoutSources/
(receipts-sha256.txt + fetched files + issue-search JSONs). Tooling: no installs needed
(curl, git, GitHub REST API only); pacman untouched; lane touched read-only.

## Commands run (exact, all rc=0 unless noted)

1. `curl -fsSL -o $S/packer-v5.2.0.cpp https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packer.cpp` and `-o pefile-v5.2.0.cpp .../pefile.cpp` — rc 0.
2. `sha256sum` + `wc -c` on fetched and on lane copies `.ufo/waves/round-99/pre/s326-packer-v5.2.0.cpp`, `.ufo/waves/round-98/pre/s324-pefile-v5.2.0.cpp` — rc 0.
3. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show c19d57cd2e65a036478b9e78f6c5397dedfb2bcb:corpus/SOURCES.md` → $S/SOURCES-at-Bk.md — rc 0, 366 lines (read-only git).
4. `curl .../api.github.com/repos/upx/upx/contents/src?ref=v5.2.0` — rc 0; fetched `pefile.h`, `p_w64pe_amd64.cpp`, `p_w32pe_i386.cpp`, `packhead.cpp`, `packmast.cpp`, `upx-doc.txt`; `peheader.h` → rc 22 HTTP 404 (no such file at v5.2.0; `pe_section_t` lives in pefile.h).
5. GitHub issues search API: `q=repo:upx/upx+"invalid+overlay+size"` rc 0 total_count 0; `q=repo:upx/upx+"overlay+size"` rc 0 total_count 2; `q=repo:upx/upx+overlay+truncated+in:title,body+type:issue` rc 0 total_count 0.

## Findings

F1. Fetch is byte-identical to both registered rows and their lane copies.
    packer.cpp: 44586 bytes, sha256 `ab274d672d0985fa92d83e8c9c867d62ff30a1f31d2fb0b919e6d8826b03e040` — equals S326 row at Bk and the pre/ copy. pefile.cpp: 127340 bytes, sha256 `6783a926f339b8fa5051c3c0c105c078655513d96ca4bb0f94c74315911379fa` — equals S324 row at Bk and the pre/ copy. No drift between Bk text and upstream tag.

F2. Quoted lines located verbatim.
    packer.cpp 431 `void Packer::checkOverlay(unsigned overlay) {`, 432 `if ((int) overlay < 0 || overlay > file_size_u)`, 433 `throw OverlayException("invalid overlay size; file is possibly corrupt");` — matches S326's anchor. pefile.cpp 3041-3049 = `handleStub(fi, fo, pe_offset);` (3041), `if (ih.filealign == 0) throwCantUnpack(...)` (3042-3043), then 3045-3049:
    `const unsigned iobjs = ih.objects;` / `const unsigned overlay =` / `file_size_u -` / `ALIGN_UP(isection[iobjs - 1].rawdataptr + isection[iobjs - 1].size, ih.filealign);` / `checkOverlay(overlay);` — matches the cited window.

F3. The entry's rule is what the source computes. VERDICT: CONFIRMED.
    unpack0 (pefile.cpp 3045-3049) computes overlay = file_size_u − ALIGN_UP(last-table-row rawdataptr + last-table-row size, filealign); checkOverlay (packer.cpp 431-433) throws when `(int) overlay < 0` — which for realistic sizes (both terms < 2^31) is exactly file_size_u < ALIGN_UP(...) after unsigned wrap [INFERENCE on the two's-complement cast, standard for this codebase's `unsigned` arithmetic] — or `overlay > file_size_u`. "Last section in table order" is literal: `isection[iobjs - 1]`; the table is read verbatim in canUnpack0 (pefile.cpp 3164-3166 `fi->readx(isection, sizeof(pe_section_t) * objs)`) and never sorted. Field mapping (pefile.h 189-197): `name[8]; vsize; vaddr; size; rawdataptr; _[12]; flags` → `.size` = SizeOfRawData, `.rawdataptr` = PointerToRawData. Note the pack-side twin is different: `readSections` (pefile.cpp 2273-2275) computes overlaystart as the MAX over all table rows, and `pack0` (2379-2382) clamps `overlay >= file_size_u` to 0 — the table-order qualifier in the entry is load-bearing and correct for the unpack path.

F4. Earlier checks on a short file, in order, unpack path.
    Dispatch: `PackMaster::visitAllPackers` (packmast.cpp 141-173) tries PE packers (`PackW64PeAmd64`, `PackW32PeI386`, ...) via `try_can_unpack` (115-130) → `pb->canUnpack()` BEFORE the winner's `unpack()` runs. So, in order:
    (a) `PeFile32/64::canUnpack` (3262/3312) → `canPack()` = readFileHeader + readPeHeader — header-region reads; pass for tail truncation; `readPeHeader`'s `fi->readx(&ih, sizeof(ih))` (3238/3293) fails only for files cut before the optional header.
    (b) `canUnpack0` (3157): section-table `readx` (3166) throws EOF ("unexpected end of file") if truncation reaches `pe_offset + ih_size + 40*objs`; then the PackHeader probe at `isection[1].rawdataptr - 64` + `readPackHeader(1024)` (3169-3170, S324's anchor 3167-3174) — a truncation cutting into/below the UPX1 head region leaves no magic → found_ph false → canUnpack returns false → refusal ("not packed by UPX" class) BEFORE any overlay check.
    (c) Inside `unpack0` itself, nothing length-dependent precedes 3045-3049: handleStub only fails on pre-header truncation and the `filealign == 0` test is header-only; `checkOverlay` IS the first length-dependent refusal in unpack0. After it, the `ph.c_len` `readx` (3051-3053) can still EOF, but only when file_size ≥ section end, outside the truncation class.
    `readSections` is pack-path only (its only caller is `pack0` at 2379), so it cannot fail before the overlay check on `upx -d`.
    Net: for the battery's fixture class — tail truncation that keeps headers, section table and the PackHeader window intact — the first failing check is exactly the F3 rule; deeper truncations (section table or pack-header window cut) are refused earlier by (a)/(b) with different errors.

F5. Application to C2's refusal rule: the repair tool's predicate (refuse when file < ALIGN_UP(last section rawdataptr + SizeOfRawData, FileAlignment), last section in table order) is the exact unpack0 condition, and no unpack-path check contradicts or precedes it for tail truncations. [INFERENCE from source order only — this seat ran no fixtures; battery numbers belong to the executor/replay seats.]

F6. Further primary source: NONE EXISTS in the required class → rejection drafted (draft-s327-candidate-rejection.md in receipts dir). GitHub issues: `"invalid overlay size"` 0 hits; `"overlay size"` 2 hits ("Datatype of overlay_offset in p_mac.cpp", "v3.95") neither on this behaviour; `overlay truncated` 0 hits. upx-doc.txt sha256 `4dc547edc7201f205ce904f373518b6fcaef608d5aafd8a4a7564d42993b8c42` is already S269/S271; its overlay section (143-164) documents copy/strip/skip only and the word "invalid" never occurs. Third-party writeups (0xdf Flare-On 2020 "garbage"; hardlyprogramming = S325) are outside the issue-tracker/docs class. No S-id consumed; a reusable 11-column row shape is held in the draft file.

## Gaps

- upx/upx Discussions were not searched (GraphQL only; REST issue search is issue/PR-scoped). Low risk: the message string has 0 issue hits and originates in packer.cpp (S326).
- F3's `(int)` wrap analysis is inference from the code text, not executed C++; semantics of unsigned wrap → signed cast are standard.

## Verdict

Source attack confirms R99-C2's frozen rule: pefile.cpp 3045-3049 + packer.cpp 431-433 refuse exactly `file < ALIGN_UP(last-table-row rawdataptr + SizeOfRawData, FileAlignment)`; only deeper truncations (section table / PackHeader window) fail earlier in canUnpack0, and no further primary source exists (rejection drafted).

Receipts: .ufo/waves/round-99/w1/ScoutSources/{receipts-sha256.txt, packer-v5.2.0.cpp, pefile-v5.2.0.cpp, pefile.h, p_w64pe_amd64.cpp, p_w32pe_i386.cpp, packhead.cpp, packmast.cpp, upx-doc.txt, gh-issues.json, gh-issues2.json, gh-issues3.json, SOURCES-at-Bk.md, draft-s327-candidate-rejection.md}

Report: .ufo/waves/round-99/w1/ScoutSources.md
