# R38W2Quarantine — quarantine slice re-derivation and the five verdicts (round-38 w2)

Seat `R38W2Quarantine` (critic, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
HEAD `0fc6113376a156fddc3ec385386d71c3a4a9f690` at read time. Axes: coverage, calibration.
Milestone: round-38 attempt 2 — falsify the landing. Nothing here changes a frozen predicate, counter,
carrier, oracle or the register; the register and every campaign file were opened read-only.

**Verdict: CONFIRMED** — the committed quarantine slice is byte-identical to a fresh addendum-§10
derivation, every line carries an S-id, and all five verdicts in `corpus/lessons/round-38.md`
`### Quarantine slice` hold against live sources. Three defects found, none of which flips a verdict:
S150's refusal is **understated** (the row carries a second false provenance cell the lesson does not
record — it is part **6**, not part 4), the "17 locales" lineage is proven to be a **regex artifact**
(and the round-35 lesson still asserts it, unrouted), and the section's ids are **campaign ids** that
collide with lane ids for S113.

---

## 1. Slice re-derivation — identical, 5 rows, provenance intact

Register identity (unchanged since wave 1's cited hash): `sha256sum
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` =
`5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines.

The addendum's awk, run verbatim
(`/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-38.md`, item "Quarantine — payload-absent rows"):

```
awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

```
 S150   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S117`   the cited source could not be fetched, so no quote was checked
 S136`   the gate block named no locator, so no quote was checked
 S147`   the gate block named no locator, so no quote was checked
```

- `diff -u .ufo/waves/round-38/assimilation/quarantine-slice <derived>` → **exit 0** (byte-identical).
- Both sides hash `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`.
- Provenance: the file enters history in `3b960fe5f9a7f1dfa22819f98dc0fa983f4260a8` and is identical at
  `0fc61133` (both `git show` hashes equal).
- Completeness: the register holds exactly **6** kaidoku-bearing lines — 5 data rows (82, 315-318) plus
  the `## By lane` summary row (254, excluded by the `round[0-9]+` predicate). No kaidoku row is
  written with a different round spelling, so nothing is missed.
- The 5-row count and the register's own kaidoku payload-absent total (`1`) agree; the lesson's
  "kaidoku data rows: 5" is correct.
- Caveat, cosmetic: the never-checked table has one fewer column, so those four lines carry a stray
  backtick in `$4` and a **reason** (not a class) in `$5`. Ids stay unambiguous.

Evidence: `.ufo/waves/round-38/w2/artifacts/R38W2Quarantine/slice-derivation.txt`.

## 2. S150 — refusal CONFIRMED, and the row is worse than the lesson records

Live re-fetch of `https://zenn.dev/yasu01/articles/7370bd5d414ec4` (2026-10-26): HTTP 200,
**174,088 B** on two independent fetches — the size the lesson quotes.

| probe | raw HTML | `\uXXXX`-unescaped body |
|---|---|---|
| `シンボルがない場合のヒント` (the registered span) | **0** | **0** |
| `ヒント` | 0 | 0 |
| `シンボルがない` | 0 | 0 |
| `パターン認識のコツ` | 4 | 4 |

The unescape matters: zenn serves the body twice (rendered HTML and a `\u003c`-escaped `bodyHtml`
JSON), so a raw-only count could miss an escaped heading. It does not — zero both ways.

Real H2s: はじめに / 道具の準備 / 実例：小さなプログラムを逆アセンブルする / パターン認識のコツ /
AArch64 で同じバイナリを読む / 読み進めるためのワークフロー / まとめ / シリーズを終えて. There is no
hint section and no heading named 「逆アセンブル」 (the closest is 「実例：小さなプログラムを逆アセンブルする」).

**Not a mis-citation rescue.** The article's own series table maps all six parts; I fetched the five
siblings (145,135-208,459 B each) and the span occurs **0 times in every part**:

| part | slug | title |
|---|---|---|
| 第1回 | 0350f265dc880c | 同じ処理、3つの命令セット |
| 第2回 | 274cf708c13ded | Cコンパイラの出力を読む |
| 第3回 | 1f92df34f54c31 | スタックフレームを図解する |
| 第4回 | 3efeb9d6054eed | システムコールの裏側 |
| 第5回 | 13d6ac052137ae | SIMD命令を読む |
| **第6回** | **7370bd5d414ec4** | **リバースリーディング** (the cited article) |

**Disagreement (understatement).** The row (`.ufo/…/round5/SOURCES-PROPOSED.md:21`,
`merge/kaidoku/SOURCES.append.md:51`) also claims "part 4 of a 6-part series". The article's own table
puts it at **第6回**; 第4回 is `3efeb9d6054eed`. So the row carries **two** false provenance cells (the
absent heading, the series position) plus a non-heading § name. The lesson records only the heading.
The refusal verdict is right and, if anything, over-determined; the article itself is genuine and its
PLT/`objdump` substance does resolve (H3 `objdump`, the `strcmp@plt` sentence), so the row is
fabrication-class on its citation cells, not a fabricated document.

**Smallest safe correction:** extend the lesson's S150 bullet with "and the row's 'part 4 of a 6-part
series' is false — the article is 第6回; §『逆アセンブル』 is not a heading". No register edit.

Evidence: `…/artifacts/R38W2Quarantine/zenn-s150.txt`.

## 3. S113 (staged adb page) — the count is CONFIRMED, and "17" is now explained

Two fetches of `https://developer.android.com/tools/adb?hl=en` (2026-10-26): HTTP 200, 368,059 B and
368,063 B; both carry **22** `hreflang` tags = **21 locales + `x-default`** (ar bn de en es-419 fa fr
he hi id it ja ko pl pt-BR ru th tr vi zh-Hans zh-Hant). The lesson's "21 locales + `x-default`, not
17" is correct.

New evidence — the 17 does not come from a different page state, it comes from a narrower extractor:

| pattern | count |
|---|---|
| `hreflang="[a-z]*"` | **17** |
| `hreflang="[a-z][a-z]"` | **17** |
| `hreflang="[a-z-]*"` | 18 |
| `hreflang="[^"]*"`, distinct | 22 |
| `grep -c hreflang` (lines) | 21 |

The `[a-z]*` pattern silently drops exactly five tags — `es-419`, `pt-BR`, `x-default`, `zh-Hans`,
`zh-Hant` — and the 17 survivors are `ar bn de en fa fr he hi id it ja ko pl ru th tr vi`. So the
row's "17 locales" is an under-counting artifact, not a historical locale matrix.

**Un-routed defect.** `corpus/lessons/round-35.md:21` still asserts "17 `hreflang` locales plus
x-default … 368,063 bytes" — a byte size I reproduce today on a page that carries 21 locales. The
round-38 lesson corrects the number but never routes the round-35 line, so the lane keeps a live false
count one round back.

**Smallest safe correction:** add "17 = a `[a-z]*`-only extractor dropping the five hyphenated tags;
`round-35.md:21` superseded" to the S113 bullet, and list `round-35.md:21` under routed defects for the
next closure. No register edit — the row is not appended and no admitted entry cites the adb page.

Evidence: `…/artifacts/R38W2Quarantine/s113-hreflang.txt`.

## 4. S117 — CONFIRMED `unverifiable (not fabrication)`

`https://doi.org/10.1109/SP46214.2022.9833799` → 302 → `ieeexplore.ieee.org/document/9833799/`
**HTTP 202, 0-byte body** (reproduced). Semantic Scholar graph API **HTTP 429** again (second round).
Crossref DOI-keyed **HTTP 200**: title `SoK: Demystifying Binary Lifters Through the Lens of Downstream
Applications`, container `2022 IEEE Symposium on Security and Privacy (SP)`, page `1100-1119`. The paper
exists; the abstract-level claims (e.g. 252,063 executables) stay unchecked. The addendum's rule that a
prose "could not be fetched" cell is `unreachable`, never fabrication, is what the lesson applied.

## 5. S136 — CONFIRMED `adopt-with-anchor`

`corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` is 12,897 B; the row's named heading is the H1 at
**line 3** (`# kaidoku-r4u / 06 — ADB surface: client present, zero devices`), and the quote the row's
recheck targets, "2 of 24 verbs are", occurs **once**, at **line 8**. The lesson cites line 8; both
lines resolve, so the verdict is right. Precision note only: the row named a *heading* (line 3) while
the lesson anchors the *recheck sentence* (line 8) — for a repaired locator, naming both is cheaper
than letting a reader think the heading moved.

## 6. S147 — CONFIRMED line 41; "the heading names are wrong" is imprecise

`/home/vgpnk/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`, 3,386 B. Line 41 is
`- REA release: \`rea-agents@6.7.0\`, skill v42, 207 tools.`; `grep -c '207 tools'` = 1. Real headings:
`## State as of this writing` (39), `## Expected \`doctor\` output on this host` (46).

**Disagreement (calibration).** Of the row's two named locators, `§ "Expected doctor output"`
**does** resolve (line 46, modulo backticks); only `§ "REA release"` fails — it is a bullet at line 41
under `## State as of this writing`. "The heading names in the row are wrong" overstates by one. The
lesson also drops the path (bare `HOST-CONTRACT.md`) on a row whose cited source is
`agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`; that is exactly the kind of locator
weakening this lane has been burning rounds on.

**Smallest safe correction:** "line 41 resolves; `§ 'REA release'` is a bullet under
`## State as of this writing` (39), and `§ 'Expected doctor output'` resolves to line 46 — cite
`~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md:41`".

## 7. "No admitted entry cites any of the five" — true by document, ambiguous by id

Verified true as written, in document terms:

- base `77091b49`..HEAD `0fc61133` adds only `S110` (cell edit), `S112`, `S113`, `S114`, `S115`, `S116`
  to `corpus/SOURCES.md` — no row for the zenn article, the adb page, the DOI, `r4u-06` or
  `HOST-CONTRACT`.
- The two admitted entries' `source:` lines cite S112/S113/S114 and S116/S110 (S110 = same document as
  staged S106).
- Corpus-wide, the five documents appear only in lessons and in `corpus/SOURCES.md:210`, an
  **unopened-lead prose line present at base** (not a row, not created this round).

**Disagreement (labelling).** The sentence sits in a section whose ids are **campaign** ids, but the
same ids are live in the lane: lane `S113` is unblob's `squashfs_v4_be/__input__` fixtures
(`corpus/SOURCES.md:119`), it is **admitted at `round-38.md:29`**, and its row was appended in
`3b960fe5`. So "no admitted entry cites S113" is false at id level, and `round-38.md` uses `S113` for
both documents (line 29 = fixtures, line 76 = staged adb, line 88 = fixtures). The parenthetical
"(staged)" disambiguates the verdict row but not the closing sentence. Lane ids stop at `S116`, so
S136/S147/S117/S150 cannot collide.

**Smallest safe correction:** rewrite line 81 as "No admitted entry cites these five *documents*
(zenn S150, staged-S113 adb, S117 DOI, S136 `r4u-06`, S147 `HOST-CONTRACT`), so none is appended."

## 8. Limits of this check

- The drift branch ("did the adb page really have 17 locales on 2026-10-23?") could not be closed
  historically: the Wayback availability API returned **HTTP 429** for both URLs. The regex result
  makes drift an unnecessary hypothesis — 17 is reproducible *today* from the same bytes that show 21.
- Semantic Scholar is rate-limited (429, second round), so S117's abstract-level claims stay unchecked.
- I ran no campaign tool in `/home/vgpnk/Projects/shokuknow` (`absent-defect-register.py`,
  `renumber-staged.py`, `quote-lint.py` untouched; register read-only), wrote nothing outside this
  report and `…/w2/artifacts/R38W2Quarantine/`, and used read-only git (`show`, `diff`, `log`) only.
- No tool installed or updated; nothing needed (pacman paused host-wide, `sasquatch*` untouched).
- Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2Quarantine` removed before this report was yielded;
  every cited byte count, hash and count is quoted above or captured in the artifacts.

## Axes and corrections, one line each

| item | verdict | axis | smallest safe correction |
|---|---|---|---|
| slice vs addendum awk | identical (diff 0, sha `7383a90e…`) | coverage | none |
| S150 refuse | confirmed, understated (part **6**, not 4) | coverage | record the second false cell; future re-anchor must fix it too |
| S113 count 21 + x-default | confirmed; "17" = `[a-z]*` artifact | calibration | state the artifact; route `round-35.md:21` |
| S117 unverifiable | confirmed (202/0 B; Crossref 200) | calibration | none |
| S136 adopt-with-anchor | confirmed (heading line 3, quote line 8) | calibration | name both lines |
| S147 line 41 | confirmed; "heading names wrong" overstates | calibration | one of two named § resolves; keep the path |
| "no admitted entry cites" | true by document, false by id | coverage | name the five documents, not bare ids |
