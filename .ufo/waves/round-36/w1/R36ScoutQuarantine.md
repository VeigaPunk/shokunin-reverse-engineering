# R36ScoutQuarantine — kaidoku round 36 quarantine re-check (5 rows)

Date of checks: 2026-10-26 (host clock; fetch `date:` header 04:28 GMT). Advisory only; no lane file other than this one was written; no VCS mutation; no tool installed; no REA/campaign tool run in shokuknow.

Inputs read: `.ufo/waves/round-36/assimilation/quarantine-slice` (5 lines: S150, S113, S117, S136, S147); `.ufo/waves/round-35/assimilation/quarantine-verdicts.md`; staged rows in `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` (rows at lines 14, 18, 37, 48, 51; the file marks them `*`).

## Verdict table

| row | register class | today's check (2026-10-26) | verdict | vs round 35 |
|---|---|---|---|---|
| S150 | payload-absent | Cited quote `§「シンボルがない場合のヒント」` is **not** in the article. Details below. | **fabrication-class REFUSE** (the quoted section anchor); the row's *teaches* is otherwise supported | **agrees** (REFUSE). One extra finding: the other cited anchor `§「逆アセンブル」` is also not a heading (only a substring of one) |
| S113 | unreachable | Page fetches (200, 368,063 B). Row's own recheck reproduces (`grep -c 'tools/adb?hl=ja'` → 1). But the row's *teaches* count "17 locales" is **false against live bytes**: 22 `hreflang` alternates = 21 locales + `x-default` | **locatable** (anchor + recheck) with a **teaches-count defect** (17 vs 21) | agrees on "verifiable-now", **disagrees on the number**: round 35 recorded "17 locales plus x-default". Same byte size (368,063) as round 35 [INFERENCE: same bytes, so round 35 miscounted or counted a subset; today's count is mechanically reproducible below] |
| S117 | unreachable | `doi.org` → 302 → ieeexplore; IEEE final fetch HTTP **202, empty body** (same as round 35); `ieeexplore.ieee.org/document/9833799/` 200 but 16,543 B JS shell with no abstract. Semantic Scholar (the row's own recheck source) HTTP **429** twice. **But** OpenAlex mirror of the IEEE abstract (HTTP 200) contains the row's quote: "We study four popular static and dynamic LLVM IR lifters … from a total of 252,063 executables". HKUST repository mirror: captcha redirect loop | **unverifiable at the cited source** (publisher wall; `§ I Introduction` not checkable by anyone today); abstract-level claim **locatable only at a third-party mirror** (OpenAlex) | partly **differs**: round 35 said plain unverifiable. Today the abstract content is checkable via OpenAlex, the row's cited location (IEEE) is still not. Not fabrication either way |
| S136 | named no locator | Own-work. `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` exists (12,897 B); `grep -c '2 of 24 verbs are'` → 1; line 3 is `# kaidoku-r4u / 06 — ADB surface: client present, zero devices` | **locatable** (locator supplied by the row's own text; the "named no locator" class was a gate-block extraction miss, not a row defect) | agrees |
| S147 | named no locator | Own-work. `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` exists (3,386 B, mtime 2026-10-22). Headings present: `## State as of this writing` (line 39) and `## Expected \`doctor\` output on this host` (line 46); line 41 `REA release: rea-agents@6.7.0, skill v42, 207 tools`; line 23 `Do **not** run rea-agents setup --client`. `npx -y rea-agents@6.7.0 --version` → `6.7.0`. | **locatable**, with a **heading mismatch**: the row cites `§ "REA release"`, but no heading by that name exists; `REA release:` is a bullet under `## State as of this writing` | agrees on "locatable". Round 35 did not note the heading mismatch |

Verdict count today: 1 refuse (S150); 3 locatable (S113 with count defect, S136, S147 with heading mismatch); 1 unverifiable-at-source (S117).

## S150 — evidence

Commands (scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36ScoutQuarantine`, removed at end):

```
curl -sL -A 'Mozilla/5.0' -o zenn.html https://zenn.dev/yasu01/articles/7370bd5d414ec4   # 200, 174088 B (identical size to round 35)
grep -c 'シンボルがない場合のヒント' zenn.html     # 0
grep -o 'ヒント' zenn.html | wc -l                  # 0
curl -sL https://zenn.dev/api/articles/7370bd5d414ec4                # 200, 69896 B JSON; body_html 39,937 chars
```

Zenn API: title 「実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む」, published_at 2026-05-23, body_updated_at 2026-06-04 (both before the 2026-10-23 "as fetched" date, so no post-fetch edit explains the absence). `'ヒント' in body_html` → False; `'シンボルがない場合' in body_html` → False. Live heading outline (HTML `<h2>/<h3>`, 20 headings): はじめに / 道具の準備 (objdump, llvm-objdump, readelf) / 実例：小さなプログラムを逆アセンブルする (ソースコードと準備, Step 1–4) / パターン認識のコツ (関数の境界, 文字列参照, 分岐の構造, ライブラリ関数の特定) / AArch64 で同じバイナリを読む / 読み進めるためのワークフロー / まとめ / シリーズを終えて. **No heading `シンボルがない場合のヒント` and no heading exactly `逆アセンブル`.**

What the article *does* support (so the row's teaches is not invented, only its anchor): under 「ライブラリ関数の特定」 it says `PLT のエントリを見ると strcmp@plt、printf@plt、puts@plt といったシンボルが残っていることがあります。strip されていても PLT のシンボルは残る場合があるので、ここが最初の手がかりになりました。` (matches "PLT symbols can survive stripping and are the first clue"); it has an `strip greet # シンボルを削除` walkthrough; `objdump` appears 42 times; the AArch64 section exists. The row's recheck `grep -c 'llvm-objdump'` → 6 reproduces (line count).

Class: the quoted heading is absent from both served HTML and the Zenn API body → a fabricated/guessed section anchor. A teaches built on real content under a non-existent quoted section name is still a quote-anchor failure. Flip condition (same as round 35): re-anchor to a real contiguous quote, e.g. 「ライブラリ関数の特定」 with the `strip されていても PLT のシンボルは残る場合があるので` sentence, and re-open; do not repair in place by editing only the heading.

## S113 — evidence and locale-count defect

```
curl -sL -A 'Mozilla/5.0' -o adb.html 'https://developer.android.com/tools/adb?hl=en'    # 200, 368063 B
grep -c 'tools/adb?hl=ja' adb.html            # 1   (row's recheck: reproduces)
```
`<link rel="alternate" hreflang=…>` tags parsed with Python `re` over `<link[^>]*rel="alternate"[^>]*>` (attributes can span lines, so a one-line grep under-counts): 22 tags, set = ar, bn, de, en, es-419, fa, fr, he, hi, id, it, ja, ko, pl, pt-BR, ru, th, tr, vi, zh-Hans, zh-Hant (21 locales) + x-default. The row says "served in 17 locales"; round 35 wrote "17 locales plus x-default". Both disagree with today's count (21 + x-default). Consequence: if S113's row or its entry (`adb-locale-pinned-reference.md`) is ever adopted, the "17" must be corrected to 21 or re-measured; the anchor/recheck themselves are fine. The staged entry `adb-locale-pinned-reference.md` was not adopted and is not part of the sasquatch theme.

## S117 — evidence

```
curl -sL -D hdr -o doi.html https://doi.org/10.1109/SP46214.2022.9833799   # 302 → ieeexplore.ieee.org/document/9833799/ → HTTP 202, 0 B (final)
curl -sL https://ieeexplore.ieee.org/document/9833799/                      # 200, 16543 B, no abstract text
curl -sL https://api.semanticscholar.org/graph/v1/paper/DOI:10.1109/SP46214.2022.9833799?fields=…   # 429 (twice, 5 s apart)
curl -sL https://api.crossref.org/works/10.1109/SP46214.2022.9833799        # 200: title/venue/2022-05 only, no abstract
curl -sL https://api.openalex.org/works/doi:10.1109/SP46214.2022.9833799    # 200, 19347 B
```
OpenAlex `abstract_inverted_index` reconstructed: "… We study four popular static and dynamic LLVM IR lifters that were developed by the industry or academia from a total of 252,063 executables generated by various compilers and optimizations and on different architectures." Both row numbers (four lifters, 252,063) present; venue `IEEE Symposium on Security and Privacy`, year 2022. The row's `§ I Introduction` cannot be checked (no full text reached). The row's own recheck command (Semantic Scholar) is rate-limited today. OpenAlex is a reconstructed secondary index, not the cited source, so the honest verdict is unverifiable-at-source, mirror-consistent. This is a calibration difference from round 35, not a contradiction.

## Sasquatch-theme entry citation check (the "will any admitted entry cite these rows" question)

**No.** Evidence:

- Staged sasquatch/unblob entries in `/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/`: `unblob-sasquatch-dependency.md` (sources S106, S107), `sasquatch-prebuilt-package-inventory.md` (S107, S130), `sasquatch-unblob-compatibility.md` (S183–S186), plus `sasquatch-unblob-compatibility-precondition.md`, `sasquatch-unblob-avm-branch.md`, `unblob-format-matrix.md` and the `avm-*` entries. `grep -rlE '\bS(113|117|136|147|150)\b'` over `knowledge/` lists only: `adb-locale-pinned-reference.md`, `japanese-native-literature-shape.md`, `offline-lifter-survey-scope.md`, `adb-host-vs-device-verbs.md`, `adb-verb-classification-join.md`, `chinese-oem-native-adb-reference.md`, `rea-catalogue-version-join.md`, `japanese-native-adb-command-reference.md`, `japanese-no-symbols-reading-workflow.md`, `japanese-dynamic-analysis-command-set.md`, `binary-lifter-sok-access-routes.md`. **None** of these is a sasquatch/unblob/avm entry; none of the sasquatch-theme files contains any of the five ids.
- Row `used-by` pointers (staged rows): S113 → `adb-locale-pinned-reference.md`; S117 → `offline-lifter-survey-scope.md`; S136 → `adb-verb-classification-join.md`; S147 → `rea-catalogue-version-join.md`; S150 → `japanese-no-symbols-reading-workflow.md`. All ADB / lifter / Japanese-literature / REA-catalogue entries, not sasquatch.
- Lane side: `corpus/knowledge/` has no round-36 entry yet (`ls … | grep -E 'r36|sasquatch'` empty; the planned path in `plans/round-36-claims.md` is `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`, not yet written at check time). The six round-36 scout reports under `.ufo/waves/round-36/w1/` cite S036/S081/S094/S106/S107/S109–S112 etc.; `grep -E 'S(113|117|136|147|150)\b'` over them → no hit.
- Round-36 frozen claim text (`plans/round-36-claims.md` lines ~98–102) names the sasquatch/unblob assimilation theme as `unblob-sasquatch-dependency`, `sasquatch-prebuilt-package-inventory`, `sasquatch-unblob-compatibility`, i.e. sources S106/S107/S130/S183–S186; none of the five quarantine ids.

So: none of the five rows is adopted this round unless an entry outside the sasquatch theme is admitted, and none is; adoption stays closed. Consistent with round 35 ("No row is appended").

## Cross-cutting notes for the integrator

1. S150 is the only fabrication-class row; keep it refused. Do not append the other four either (not cited by any admitted entry; append guard is the id-collision check, not this slice).
2. If S113 is ever lifted out of quarantine, fix "17" → 21 (+ x-default) first; the count in round-35's verdict table is itself wrong.
3. If S147 is lifted, change `§ "REA release"` to `§ "State as of this writing"` (bullet `REA release:`) so the quoted section name exists.
4. Limits: S117 `§ I Introduction` unchecked; OpenAlex mirror is secondary; Semantic Scholar recheck blocked by 429; one HKUST mirror request looped on a captcha redirect (a background curl may still be spinning on it; it holds nothing).

## Tooling / scratch

No tools installed or updated. Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScoutQuarantine` removed before finishing. No `agent://` messages sent.
