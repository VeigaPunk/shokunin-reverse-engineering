# R39W2Quarantine — falsify the lesson's quarantine sentence (round 39 wave 2)

**Verdict: CONFIRMED on the slice and the byte-identity claim; DEFECTS FOUND on "all five verdicts … held".** The slice re-derives byte-identically (5 rows, same sha256 as round 38). Re-opened live, S113, S117, S136 and S147 hold. S150's "refuse (fabrication)" holds only for the register's tested string (the anchor heading). The row's gate-block quote and "also" quote are present verbatim on the live page, so under the round-39 prompt's own quarantine rule ("absent → refuse; present → adopt with the anchor you located") the more defensible disposition is re-anchor, not refuse. Wave 1 never checked the gate quote. Two earlier seats (R35, R38W2) said the same and the round-39 corrections do not route it.

Seat `R39W2Quarantine` (leaf). Read-only on `/home/vgpnk/Projects/shokuknow`. No REA, no carrier, no tool install, no VCS mutation. Scratch `/fast/scratch/hyaku/kaidoku-r39/R39W2Quarantine` (removed at end). Evidence in `.ufo/waves/round-39/w2/artifacts/R39W2Quarantine/`.

Sentence attacked, `corpus/lessons/round-39.md:64-65`: "Quarantine slice: 5 rows, byte-identical to round 38, all five verdicts re-opened and held (`w1/R39Quarantine.md`)."

## 1. Slice re-derivation — CONFIRMED

Prompt: `/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-39.md:561-568`, the same awk as round 38.

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' $R > slice   # rc 0
```
- Register: sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines, mtime Oct 24 08:37, unchanged since round 38.
- The slice has 5 lines: S150, S113, S117, S136, S147. Each carries an S-id.
- `cmp slice .ufo/waves/round-39/w1/artifacts/R39Quarantine/quarantine-slice` → 0.
- `cmp slice .ufo/waves/round-38/assimilation/quarantine-slice` → 0.
- `sha256sum slice` = `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`, matching the wave-1 value.
- `grep -n kaidoku $R` returns 6 lines: 82 (S150, table 1), 254 (the By-lane summary row, which the awk skips), and 315-318 (S113, S117, S136, S147, table 2). So 5 data rows, none missed by the filter.
- Artifact: `quarantine-slice.rederived`.
- Deviation: the round-39 prompt (`:565`) tells the lane to write the slice to `.ufo/waves/round-39/assimilation/quarantine-slice`. That directory does not exist; the slice sits only in `w1/artifacts/R39Quarantine/`. The bytes are right, but the prompt's stated location is unused. Cosmetic.

## 2. Spot-check A — S150 (zenn.dev) — verdict holds on the register's string, but is overstated as "fabrication"

Live fetch 2026-10-26: `curl -sL https://zenn.dev/yasu01/articles/7370bd5d414ec4` → HTTP 200, 174,088 B (same size as rounds 35/36/38/39 wave 1). Artifacts `zenn-s150.html`, `zenn-s150-analysis.txt`.

| string | count |
|---|---|
| register quote `シンボルがない場合のヒント` | **0** (`ヒント` 0, `シンボルがない` 0) |
| gate quote `GNU Binutils に含まれる逆アセンブラ。ほぼすべての Linux 環境に入っています。` | **2** (once under H3 `objdump`; once in the embedded JSON blob) |
| gate "also" `strip されていても PLT のシンボルは残る場合があるので、ここが最初の手がかりになりました` | **2** (once under H3 `ライブラリ関数の特定`; once in the JSON blob) |

- Headings (live): H1 `実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む`. H2s: はじめに / 道具の準備 / 実例：小さなプログラムを逆アセンブルする / パターン認識のコツ / AArch64 で同じバイナリを読む / 読み進めるためのワークフロー / まとめ / シリーズを終えて. There is no `シンボルがない場合のヒント` heading and no `逆アセンブル` heading.
- Series: the `シリーズを終えて` table lists 第1回…第6回, and this is 第6回 (リバースリーディング); 第4回 is システムコール. The gate anchor's "part 4 of a 6-part series" is false.
- Gate block: `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round5/SOURCES-PROPOSED.md:68-73`. Anchor = §「逆アセンブル」 and §「シンボルがない場合のヒント」, part 4 of a 6-part series. Quote and "also" = the two sentences above.

**Defect D1 (material, carried, unrouted).** The register's `payload-absent` test ran on `シンボルがない場合のヒント`, the anchor's section name. The register's class note says "the quote is in none of them", and that is wrong for this row: the quote proper was never tested.

- R35 F1 (`.ufo/waves/round-35/w1/R35ReconQuarantine.md:189-218`) traced the extraction: `quote-lint.py:73` `QUOTE_SPAN_RE` treats `「」` as quote delimiters, so it harvested the heading. It concluded "refusal should be reserved for a row whose quoted payload is genuinely absent; S150's is present."
- R38ExecQuarantine §3.1 headed itself "the fabrication is one section heading, not the row's substance … correct disposition is re-anchor, not delete".
- R38W2Quarantine said the refusal is "fabrication-class on its citation cells, not a fabricated document", and asked for the S150 bullet to be extended with "part 6, not part 4".

The round-39 prompt (`kaidoku-round-39.md:570-572`) says: "locate the quote; absent → refuse the row (fabrication class …); present → adopt with the anchor you located." Applied to the gate quote, which is present under H3 `objdump` and H3 `ライブラリ関数の特定`, that gives **adopt-with-anchor, corrected anchors**: §`objdump` and §`ライブラリ関数の特定`, part 6.

Yet `corpus/lessons/round-38.md:117-118` still reads "S150: refuse (fabrication class) … heading occurs 0 times", `w1/R39Quarantine.md:33` carries "refuse" forward, and the round-39 `## Corrections to round 38` / `## Routed defects` sections contain no entry for it. Neither "part 6" nor the F1 reclassification appears in `corpus/lessons/round-3[89].md`: `grep -n 'part 6\|第6回\|part 4'` over round-38/39 returns nothing.

Consequence: the lesson sentence "all five verdicts … held" is true only if "held" means "refuse is a defensible decision for the staged row". The staged anchor (heading and part number) is false, so refusing the row as staged is consistent. It is not true that wave 1 re-opened the row's *claim*. Wave 1 checked the heading count and `第6回` ×2, not the gate quote. No admitted corpus entry cites S150, so there is no blast radius beyond the lesson text.

Smallest correction, append-only under `## Corrections to round 38`: "S150: the register's absent string is the anchor heading; gate quote and 'also' are present verbatim (2× each) under §objdump / §ライブラリ関数の特定 of 第6回; the row's anchor cells are false (no such heading; 第6回 not 第4回). Disposition: refuse the row **as staged**; the source is genuine (re-anchor if ever wanted)."

## 3. Spot-check B — adopt-with-anchor rows

**S113 (adb page).** `curl -sL 'https://developer.android.com/tools/adb?hl=en'` → HTTP 200, 368,063 B. `grep -o 'hreflang="[^"]*"' | sort -u | wc -l` = **22**: 21 locales + `x-default`. The 21 are ar bn de en es-419 fa fr he hi id it ja ko pl pt-BR ru th tr vi zh-Hans zh-Hant. Artifact `adb-hreflang.txt`. Holds: adopt-with-anchor, count 21 + `x-default`, not 17.
- Lineage note (not a verdict change): `corpus/lessons/round-35.md:21` still asserts "17 hreflang locales". Round 36 (`round-36.md:48`) called it false. Round 38 W2 called it a regex artifact. The round-35 text is uncorrected, which is allowed for a prior round's append-only text. No round-39 correction line names it, though; it is the same R38W2 item.

**S136 (own-work).** `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md:8-9` reads `Answer: the adb surface is **bound and partially live** — 2 of 24 verbs are` / `device-free and now return real evidence; the other 22 all demand a \`<serial>\``. Gate quote (`round4/SOURCES-PROPOSED.md:26-31`) = line 8, and its "also" is on line 9. Both reproduce. Holds.
- Minor: `w1/R39Quarantine.md:33` and `live-recheck.txt` cite `line 8 "2 of 24 verbs are device-free"`. "device-free" is on line 9; the phrase spans lines 8-9. It is a mis-cited line span, not a verdict flip. Artifact `s136-lines-8-9.txt`.

**S147 (host file).** `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` sha256 `ab36b310b285c0278bef2a62ccdc5effe9cdc2d232e4e684452c17be264b58fe`, unchanged. The gate quote `207 tools` is at line 41 (`- REA release: \`rea-agents@6.7.0\`, skill v42, 207 tools.`) under `## State as of this writing`. Artifact `s147-lines.txt`.
- The gate's anchor names § "REA release", but the file has no such heading. Its headings are `The rule`, `Do not`, `Do`, `State as of this writing`, `Expected \`doctor\` output on this host`.
- The gate "also" `Do not run \`rea-agents setup --client ...\` or re-enable the plugin`: the first half is at lines 23-24 (bolded, `<client>`). The literal "re-enable the plugin" appears **0** times; line 25 says `Do **not** run \`mcode plugin enable rea@official\``.
- The round-38 lesson's "one of the row's two heading names is wrong" is therefore correct and could say more precisely which. The conflict (6.7.0 vs the lane's pinned 6.5.0) stands.

**S117 (bonus).** `curl -sIL https://doi.org/10.1109/SP46214.2022.9833799` → final `https://ieeexplore.ieee.org/document/9833799/`, HTTP 202. Crossref → HTTP 200, title "SoK: Demystifying Binary Lifters Through the Lens of Downstream Applications", 2022 IEEE S&P, 2022-05. Holds: unverifiable, not fabrication.

## 4. Defect list

| id | severity | defect |
|---|---|---|
| D1 | material | Lesson `:64-65` "all five verdicts … held" is overbroad for S150. The gate quote and "also" are present, so the frozen prompt rule gives adopt-with-corrected-anchor. The R35 F1 / R38ExecQuarantine / R38W2 reclassification was never routed into the round-39 corrections or routed-defects table. The round-38 lesson S150 bullet still lacks "part 6". Wave 1 did not test the gate quote. |
| D2 | minor | S136 mis-cited line span (line 8 only, `device-free` is on line 9). |
| D3 | minor | S147 gate "also" `or re-enable the plugin` is not verbatim in the file, and § "REA release" is not a heading. The round-38 lesson says this vaguely. |
| D4 | cosmetic | The slice is not at the prompt's `round-39/assimilation/quarantine-slice`. |
| D5 | carried | `round-35.md:21` "17 hreflang locales" is uncorrected and not named in round-39 corrections. R36 and R38W2 raised it. |

Id caveat, still true: the staged ids are campaign-local. The lane's own SOURCES.md `S113` is the unblob BE fixtures URL (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md:4`), not the adb page. The lesson's "All ids below are staged campaign ids" caveat covers it; the round-39 sentence has no such caveat.

## 5. Limits
Live web state as of 2026-10-26, single fetch each. The zenn page was byte-stable at 174,088 B. The register and the campaign `SOURCES-PROPOSED.md` files were read-only. I did not re-run the AVM-theme join; wave 1 found the join empty, and that is a different claim. The sha256 of the fetched pages is in `sha256.txt`.
