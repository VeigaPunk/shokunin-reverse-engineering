# ScribeEntry — round 87 report (R87-C1 knowledge entry and Core/frontier text)

Behavior: drafted candidate record text for R87-C1; no production file, frozen file, counter, repair, or VCS state touched. Seat dir `.ufo/waves/round-87/w1/ScribeEntry/`.

Artifacts:
- `.ufo/waves/round-87/w1/ScribeEntry/candidate/corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`
- `.ufo/waves/round-87/w1/ScribeEntry/candidate/SKILL.md.decision-row.md`
- `.ufo/waves/round-87/w1/ScribeEntry/candidate/PROVINCE.md.round-87-block.md`
- `.ufo/waves/round-87/w1/ScribeEntry/candidate/corpus/README.md.frontier-and-rows.md`
- `.ufo/waves/round-87/w1/ScribeEntry/notes.md` (scratch observation table + commands)

Gates: none run (scribe). One scratch observation (T1 only, no REA, not the scored run): repair → `upx -t` rc 0 and `upx -d` == original on all four carriers; anchors and walk data in notes.md.

Findings:
1. F1 (limit confirmed, observed): jq and xxd each carry a fourth `UPX!` occurrence outside the three anchors (offsets 10971, 16499); the tamper overwrites it, the repair leaves it, so repaired packed bytes differ from pristine packed by 4 bytes; libz and docker-init differ by 0. The predicate's arms (windows_only, identity on unpacked bytes) are unaffected. "Loader `cmp` immediate" is [inference], not disassembled.
2. F2 (record scope): "anti-UPX" appears in six corpus/README.md frontier notes (lines 324, 355, 357, 360, 362, 364 — rounds 68/70/72/73/76/77) and seven PROVINCE.md places (466, 474, 537, 546, 556, 617, 642). The candidate notes name all of them as superseded for the magic-only class; the entry-altered half stays Frontier everywhere.
3. F3 (source gap, for L1): the repair's PackHeader checksum claim (sum of bytes 4..30 mod 251, excluding the magic) cites `packhead.cpp` in the repair docstring, but the frozen plan names only `linux.h` and `p_unix.cpp`. Unless ScribeSources opens a packhead.cpp row, the checksum anchor in the entry rests on the repair source and the measured outcome, not on a source row.
4. F4 (frozen-claim weakness, report only): the counter scores bytes, not provenance (declared in the plan); the no-pin rule is review-only. Repeated in every candidate's limits.

Placeholders: `<MEASURED…>` (receipt, rev, counts) and `<QUOTE…>` (S306/S307 anchors) — L1 fills and reconciles ids.

Out of scope: running the counter, REA, sources fetch, integration into production paths.

Tooling installed/updated: none. Scratch `/fast/scratch/hyaku/kaidoku-r87/ScribeEntry/` deleted.
