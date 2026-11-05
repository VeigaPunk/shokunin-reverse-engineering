# ConnectorOverlap — round 99, cross-lane and frontier-consistency scan

Lane: kaidoku-shokunin at Bk `c19d57cd2e65a036478b9e78f6c5397dedfb2bcb` (scratch clone, detached, `rev-parse --show-toplevel` verified). Read-only; no lane or fleet write.
Receipts: `.ufo/waves/round-99/w1/ConnectorOverlap/overlap-check.sh` (line-cited, `exit=0`, output `overlap-check.out`) and `.ufo/waves/round-99/w1/ConnectorOverlap/sibling-scan.txt`.

## 1. Sibling-lane overlap (part 1)

Scanned 20 sibling repos (kaidoku excluded) with grep for the R99-C1 counter, the R99-C2 battery/repair, the S326 rule and UPX PE terms.

- **No sibling overlap with the frozen claims.** `checkOverlay`, `OverlayException`, `canUnpack0`, `PackHeader`, `self-assessment-audit`, `pe-upx-trunc`, `upx-pe-repair`, `upx-chain-repair`, `upx-magic-repair`: zero hits in sibling `corpus/**/*.md`, `*.md`, `tools/**/*.py` (Q3, Q4 in `sibling-scan.txt`).
- Incidental byte overlap, not knowledge: `tameshi-shokunin/.ufo/waves/round-32/w1/CtlRegionDiff.md:276` and `:744` contain `UPX!` inside a binary-dump bytes literal.
- Vocabulary-only overlap with the coverage ledger: `audio-shokunin/SCORECARD.md:1059-1060` and `audio-shokunin/corpus/lessons/round-101.md:65` use "coverage-map rows" and calibration C1 ledger prose. Different lane, different counters, no shared file or tool. Not a conflict.
- Nothing in a sibling changes the R99-C1 mismatch count or the R99-C2 predicate.

## 2. Round-99 frontier note versus round-98, 76/77, 92 (part 2a)

Check: no item both Core and Frontier in `corpus/README.md` `## Frontier` / round-N frontier notes (lines 326-407). Each Core claim below is paired with the unsuperseded Frontier clause that still names the same class.

**F1 (medium) — "packed PE/Mach-O" is still Frontier in five notes that round 98 did not supersede.**
Round 98 (`corpus/README.md:405`) says it supersedes the PE half of the round-92 clause and "packed PE/Mach-O in the round-76/77 notes" only. Round-76/77 are at `:389` and `:391` and are correctly superseded. The following Frontier lists still name packed PE as Frontier with no supersession:
- `corpus/README.md:349` (round-68): "Still Frontier: … packed PE/Mach-O, packed libraries and static binaries"
- `corpus/README.md:351` (round-87): "… big-endian ELF, packed PE/Mach-O, carriers outside the four …"
- `corpus/README.md:382` (round-70): "Still Frontier: any other packer, anti-UPX stubs, packed PE/Mach-O …"
- `corpus/README.md:384` (round-72): "… anti-UPX stubs, packed PE/Mach-O and semantic inventory equality"
- `corpus/README.md:387` (round-73): "… anti-UPX stubs, packed PE/Mach-O, semantic inventory equality"
Against Core claims at `:405` (round-98 PE magic/section repair, six carriers) and `:407` (round-99 PE truncation refusal, ten carriers) and rows `:140`, `:141`. Fix: append a supersession clause at `:405` or `:407` naming `:349`, `:351`, `:382`, `:384`, `:387` as narrowed for win32/pe and win64/pep (round-98/99 scope), or cut the PE words from those lines.

**F2 (low-medium) — round-99 Core class is wider than its own Frontier exclusion.**
`corpus/README.md:407` states Core for "UPX 5.2.0 `--best` win32/pe and win64/pep packs, exe and DLL, on the ten carriers pinned …" and in the same line Still Frontier: "PE DLLs outside the pinned set". Row `:141` repeats "(exe or DLL)" as a class phrase. The class statement is wider than the population measured. Fix: "exe and DLL on the ten pinned carriers" as the Core scope, with DLLs outside the pinned set in Frontier.

**F3 (low) — round-98 Frontier list is contradicted by round-99 for offsets, but only by a later narrowing sentence.**
`corpus/README.md:405` Still Frontier includes "PE DLLs", "PackHeader offsets other than 992 (all frozen carriers share it)" and "truncated payloads (reported `ok intact`)". Round 99 (`:407`) narrows these in one sentence ("narrows its … items to the four pinned DLLs (one PackHeader at offset 517 …)"; "supersedes … for length truncation only"). The narrowing is explicit, so this is not a Core/Frontier overlap, but a reader of `:405` alone reaches the wrong statement. Suggest an inline "superseded at :407" marker on `:405`, as the file already does for round 38/44/50 lines.

**F4 (low) — ambiguous "PE" in round-88/89/90/91 frontier lists.**
`:395`, `:397`, `:399`, `:401` list "big-endian/PE/32-bit carriers" as Frontier for the packed-ELF `b_info` classes. Round 98/99 Core is a different class (PackHeader magic, section names, truncation). Not a direct contradiction, because no `b_info` tamper on PE was measured. The unqualified "PE" still reads as overlapping. Suggest "PE `b_info` tampers" in those lines.

**Consistent (checked):** round-76 (`:389`) and round-77 (`:391`) PE Frontier clauses are explicitly superseded by round 98 (`:405`). Round-92 (`:403`) "PE and Mach-O packed inputs" is explicitly superseded for the PE half by `:405`. Round-98 "truncated payloads (reported `ok intact`)" is explicitly narrowed by `:407` ("for length truncation only"). Mach-O remains Frontier everywhere, which is consistent.

## 3. Coverage-map rows r93–r97 versus SCORECARD and lessons (part 2b)

Verdicts recorded at Bk:

| round | SCORECARD header (line) | lesson verdict (line) | coverage row (`corpus/README.md`) | match |
|---|---|---|---|---|
| r93 C1 calibration | `SCORECARD.md:6622` NOT verified | `round-93-verifier-spotcheck.md:21` NOT VERIFIED | `:135` "NOT verified at its closure" | yes |
| r93 C2 depth | `:6622` verified | `:31` verified | `:134` "verified on the frozen predicate" | yes |
| r94 C1 calibration | `:6644` verified | `round-94-verifier-spotcheck.md:29` evidence-verified | `:136` "verified" | yes |
| r94 C2 depth | `:6644` verified | `:54` (heading, no verdict word) | not stated | **F5** |
| r95 C1 calibration | `:6666` verified, named limits | `round-95-verifier-spotcheck.md:45` evidence-verified | `:137` "verified … named limits" | yes |
| r95 C2 depth | `:6666` verified | `:79` evidence-verified | not stated | **F5** |
| r96 C1 calibration | `:6687` verified | `round-96-verifier-spotcheck.md:21` evidence-verified | `:138` "verified" | yes |
| r96 C2 depth | `:6687` verified | `:34` heading "(measured)"; verdict at `:40` "improved on the frozen predicate" | not stated | **F5, F6** |
| r97 C1 calibration | `:6711` NOT admitted, harmed | `round-97-verifier-spotcheck.md:24` NOT ADMITTED | `:139` "not admitted … harmed the public path" | yes |
| r97 C2 depth | `:6711` verified | `:35` verified | not stated | **F5** |

- **F5 (medium, completeness) — rows `:136`, `:137`, `:138`, `:139` state only the calibration verdict.** SCORECARD and the lessons record a depth verdict for each (verified in all four cases). The coverage map is therefore a partial statement of "each round's verdict". Row `:134` covers r93 C2 and row `:135` covers r93 C1, so r93 is complete; r94–r97 are not.
- **F6 (low, wording) — `round-96-verifier-spotcheck.md:34`** heading "R96-C2 — depth (measured)" names no verdict; the verdict is at `:40`, and SCORECARD `:6687` says "verified on the frozen predicate". Align the heading.
- **F7 (informational) — lessons index.** `corpus/README.md:288-295` `## Lessons` lists round-92, 91, 83, 82, 81 only. Round-93–98 lesson files exist (`corpus/lessons/round-9{3..8}.md` and `-verifier-spotcheck.md`) and are not indexed there. The table is selective by design, so this is not a contradiction; flagging only because the round-99 coverage rows point readers at these files.

Checks passed: all six new rows `:134-139` exist, each cites the knowledge basename, and each basename resolves to a file (`corpus/knowledge/2026-11-05-r9{3..7}-*.md`). Row `:134` (r93 C2) and row `:135` (r93 C1 NOT verified) match their SCORECARD and lesson verdicts exactly.

## 4. Findings

Count: 7 (F1–F7). Severity: F1, F5 medium; F2 low-medium; F3, F4, F6 low; F7 informational. No finding changes the frozen R99-C1 or R99-C2 predicate.

## 5. Installs / updates

None. Read-only grep/sed/git; scratch clone trap-deleted on exit.

## 6. Verdict line

ConnectorOverlap: 0 sibling overlaps with the frozen claims; 7 frontier/coverage-row inconsistencies (F1 and F5 medium; F1 is the Core/Frontier overlap on packed PE at `corpus/README.md:349,351,382,384,387` against `:405,:407`).
