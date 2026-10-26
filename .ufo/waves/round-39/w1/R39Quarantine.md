# R39Quarantine — quarantine slice re-derivation, AVM-theme join, five verdicts (round 39 wave 1)

**Verdict: CONFIRMED (slice) / DEFECTS FOUND (AVM-theme entries).** The kaidoku slice is byte-identical to round 38's and has 5 rows, all with verdicts already; none of the five staged ids is cited by any AVM-theme entry, so the hand-check set (slice ∩ AVM-cited ∩ no verdict) is **empty**. Hand-checking was therefore carried out as a live re-open of all five sources (all five verdicts hold) plus a first-ever quote/claim check of the AVM-theme entries' sources, which found two defects.

Seat `R39Quarantine` (leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on `/home/vgpnk/Projects/shokuknow`. No REA, no carrier, no tool install, no VCS mutation. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39Quarantine` (removed at end). All cited evidence is in `.ufo/waves/round-39/w1/artifacts/R39Quarantine/`.

## 1. Slice derivation (identical)

```
awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```
Output = `artifacts/R39Quarantine/quarantine-slice` (5 lines: S150, S113, S117, S136, S147). `cmp` against `.ufo/waves/round-38/assimilation/quarantine-slice` → identical (exit 0); sha256 `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a` (same as round-38 w2). Register sha256 `5afe1810…d833`, 375 lines, unchanged since round 38; 6 kaidoku-bearing lines (5 data + 1 summary row).

## 2. AVM-theme join (the item's selection rule)

AVM-theme entries: the five `merge/kaidoku/knowledge/corpus/knowledge/avm-*.md`. Cited source ids (`artifacts/…/avm-citation-join.tsv`):

| entry | cited ids |
|---|---|
| avm-firmware-image-unblob | S216 S217 S218 S219 S220 S223 |
| avm-image-build-blocker | S197 S198 S199 |
| avm-image-extraction | S200 S201 |
| avm-le-image-genuine-marker | S212 S213 S214 |
| avm-le-variant-reachability | S206 S207 |

Intersection with {S150, S113, S117, S136, S147}: **∅** (`slice-in-avm-entries.tsv`: 0 hits each). The slice ids live in non-AVM entries (adb-*, japanese-*, offline-lifter-survey-scope, rea-catalogue-version-join). The AVM entries' ids S197–S223 do not appear in the register at all for kaidoku (register hits for S200/S201/S202/S206 belong to other lanes `kama`, `mado`, `kake` — campaign ids are lane-local, harmless but easy to misread).

## 3. Verdict table (`artifacts/…/verdict-table.tsv`)

| staged id | AVM-cited | prior verdict (round 38) | live check 2026-10-26 | round-39 verdict |
|---|---|---|---|---|
| S150 | no | refuse (fabrication) | zenn.dev HTTP 200, 174,088 B; `シンボルがない場合のヒント` count **0**; `第6回` ×2 (row says "part 4") | **refuse** |
| S113 | no | adopt-with-anchor, count corrected | adb page HTTP 200, 368,063 B; **22** distinct hreflang = 21 locales + `x-default`; the `hreflang="[a-z]*"` regex yields 17 (the artifact) | **adopt-with-anchor** (21 + x-default) |
| S117 | no | unverifiable | `doi.org -L` → ieeexplore HTTP 202, 0 B body; Crossref 200: "SoK: Demystifying Binary Lifters…", 2022 IEEE S&P, 2022-05 | **unverifiable** (paper exists) |
| S136 | no | adopt-with-anchor | `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` present; line 8 "2 of 24 verbs are device-free" | **adopt-with-anchor** |
| S147 | no | adopt-with-anchor + conflict | `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` 3,386 B, sha256 `ab36b310…58fe` (unchanged); line 41 "REA release: `rea-agents@6.7.0`, skill v42, 207 tools"; lane pins 6.5.0 | **adopt-with-anchor**, conflict stays |

No verdict changed; no admitted entry cites any of the five, so nothing to append to the lane. Evidence: `live-recheck.txt`.

## 4. Extra check — AVM-theme entries' own sources (not slice rows, no prior verdict; done because the slice join was empty)

External sources, live 2026-10-26:
- S198 tags API: 200, 7,787 B, 18 tags, **no 4.3** (4.4, 4.4-git.1, 4.5, 4.5.1, 4.6, 4.6.1, 4.7–4.7.5, CVE-2021-41072, squashfs-tools-4.6, squashfs-tools-4.6.1, 3.1, 3.2, 3.2-r2). Entry's list omits 3.1 and `squashfs-tools-4.6.1`; the claim "no 4.3" holds.
- S206 patch 101: `#define AVM_LE 2`, `#define AVM_BE 3`; `AVM_BE_AVM_LE` 0 hits in body. Holds.
- S214 patch 613 (pinned commit): hunks @109, @4462, @4971 present; `-no-mkfs-time` sets `use_standard_mkfs_time = FALSE` → `mkfs_time = bytes_used`. Holds.
- S216 index: `FRITZ.Box_6490_Cable-07.57.image`, 39741440 B, 04-Sep-2023. S217: `Product: FRITZ!Box 6490 Cable`, `Version: FRITZ!OS 7.57`, `Release date: 04.09.2023`. Hold.
- S220 README line 674: "AVM-LE … some cable boxes, e.g. 6490, 6590 (x86 core only) … mkfs_time … equal to the bytes_used field." Holds verbatim.
- Lane-internal TSVs (S197, S200, S207, S212, S218, S219 under `shokuknow/lanes/kaidoku/round*/work/`) exist; S218/S219 numbers match the firmware entry (28,200,029 = 28,200,029; 5,442,392 = 5,442,392; 6,912 + 2,942 = 9,854 per row sum? the TSV lists total 9,877 — see D3).

### Defects (routed to L1)

- **D1 — failing recheck command.** `avm-le-variant-reachability.md:7`: `grep -c -F 'handler=squashfs_v4_le' lanes/kaidoku/round12/work/lead2-avm-le.tsv` → entry says 1; run from the shokuknow root it returns **0**. The TSV's row 7 is `unblob_handler<TAB>squashfs_v4_le` (`grep -c -F 'squashfs_v4_le'` → 1); the literal `handler=squashfs_v4_le` exists only in the round-12 logs (`lanes/kaidoku/round12/work/avmle.log`, `avmle2.log`) — the recheck names the wrong file/string. I ran all 8 recheck commands of the 5 `avm-*` + 3 `sasquatch-unblob-*` entries from `/home/vgpnk/Projects/shokuknow`: 7 return the stated count, this one returns 0. Fix: `grep -c -F 'squashfs_v4_le' lanes/kaidoku/round12/work/lead2-avm-le.tsv` → 1.
- **D2 — "marker invisible to unblob" overstated.** `avm-firmware-image-unblob.md:16,75` and `avm-le-image-genuine-marker.md:30` say unblob never notices the AVM marker. unblob 26.6.4 `handlers/filesystem/squashfs.py:47-50` does: for big-endian v4 it computes `is_avm = header.bytes_used == header.mkfs_time` and appends `-be` only when false (AVM → bare `sasquatch-v4be -no-exit-code -f -d`). The entries' own BE command (no `-be`) is that branch firing. True only for handler selection and the LE path (always `-le`). The sibling entry `sasquatch-unblob-avm-branch.md` (S189) states the rule correctly, so the corpus contradicts itself. Smallest correction: "unblob's handler selection ignores the marker; its BE extractor reads it to drop `-be`; the LE extractor never does."
- **D3 — minor arithmetic.** S219 TSV: `le_files_extracted 6912`, `be_files_extracted 2942`, `total_files_extracted 9877`; 6,912 + 2,942 = 9,854 (23 short). The LE top-level listing includes `var.tar` and `var.tar_extract`, so the 23 is probably a nested extraction counted only in the total [INFERENCE]. The entry repeats "9 877 files in all" as if it were the sum of the two table rows.

## 5. Limits
Own-work TSVs were checked for existence, recheck strings and the quoted numbers I could see, not regenerated (the builds are not retained per the entries' own caveats). No source in the AVM set was unreachable. Zenn S150 sibling-part check was not repeated (round 38 w2 did it, 0 in all six parts).

Artifacts: `quarantine-slice`, `verdict-table.tsv`, `avm-citation-join.tsv`, `slice-in-avm-entries.tsv`, `live-recheck.txt`, `s198…`, `s206…`, `s214…`, `s216…`, `s217…`, `s220…`.
