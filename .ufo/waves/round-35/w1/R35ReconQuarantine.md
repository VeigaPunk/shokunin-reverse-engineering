# R35ReconQuarantine — round 35 wave 1, quarantine slice: derivation + hand-check

Seat: `R35ReconQuarantine` (scout, leaf — no subagent dispatch).
Item: "Derive and hand-check quarantine slice."
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Only lane write: this report (`.ufo/waves/round-35/w1/R35ReconQuarantine.md`). No lane
production file, corpus, counter, plan, claims file, SCORECARD, LOG, VCS/index/jj state,
fleet/sibling repo or `/home/vgpnk/Projects/shokuknow` was written. No commit, no checkout,
no branch, no index mutation. No builds, no tests, no linters, no formatters, no counter
runs (counters are other seats' instruments). No pacman transaction. Private capture
root (not in the lane): `/fast/scratch/hyaku/kaidoku-r35/w1/R35ReconQuarantine/`.

`lsp` device: **not available** in this session (mounted devices are `ast_edit`, `debug`
and the MCP routes only). Caller/definition tracing was therefore done with literal text
search (`grep`, `git log -S`), recorded here per tool policy; grep output is presented as
literal-match evidence, not as semantic proof.

---

## 0. What the slice is (object under test)

Committed lane artifact under test: `.ufo/waves/round-35/assimilation/quarantine-verdicts.md`
(tracked since `d2729cba`, the round-35 instruments-first prep commit). It names a source
register in the sibling fleet repo and one extraction command, then a five-row
hand-check table with one verdict per row.

Named source register (read-only):

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
sha256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833
375 lines; mtime 2026-10-24; clean in shokuknow at commit
d4ab45f281572ecb353dd3c9b71eee0e9213558b ("Name the rows the census never reached,
instead of leaving them implied", 2026-10-24 08:37 -0300)
```

Generator of that register: `absent-defect-register.py`
(sha256 `5947600639eea70360f051cecebfdc8b2bc9247b7a26ce645c320704bd559257`), reading the
quote census `quote-lint-full-v5.json`
(sha256 `403769e369393d6f5f4e1f461f54a9555f8c15c053ccc700071c46f7b368f0b3`).

---

## 1. Derivation — reproduced, and the slice is complete

Command copied verbatim from the committed verdict file:

```bash
A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-35/assimilation
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
  {print $4, $5}' "$R"
```

Observed output (5 rows; `$4`=id cell, `$5`=class/why cell):

```
 S150   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S117`   the cited source could not be fetched, so no quote was checked
 S136`   the gate block named no locator, so no quote was checked
 S147`   the gate block named no locator, so no quote was checked
```

**Completeness (independent of the awk).** The register has two data tables — "Rows"
(header at line 28, 194 data rows, all class `payload-absent`) and "Rows whose quotes
were NEVER CHECKED" (header at line 266, 109 data rows: 78 fetch-failed, 31 no-locator)
— plus a "## By lane" summary table (line 235) that the awk correctly skips (its `$3` is a
count, not `roundN`). `grep -n 'kaidoku'` over the whole register returns exactly **6**
lines: 82 (table 1), 254 (the By-lane summary row), 315, 316, 317, 318 (table 2).
So kaidoku owns 1 + 4 = **5** data rows — the committed "Slice rows: 5" is correct and
no kaidoku row is missed by the filter.

**The By-lane summary is stale, but its kaidoku cell is not.** Measured table-1 lane
histogram: `tabi 37, revenger 24, chousa 20, kotodama 18, tameshi 14, game-dev-2d 13,
kake 9, audio 8, kagi 8, kama 7, kotoba 7, souji 7, mado 6, kumitate 5, game-dev-3d 4,
kasegi 2, kengaku 2, tsukuroi 2, kaidoku 1` = 194 rows over **19** lanes. The summary
table lists only **10** lanes (124 rows) — it omits 9 lanes outright. The kaidoku cell
(`| kaidoku | 1 |`) is nevertheless exactly right for table 1. The verdict file's note
"(header and `## By lane` summary totals are stale; slice derived from data rows only)"
is therefore correct but understated: the omission is lanes, not only totals.

**Namespace (important for the C1 id-guard).** The five slice ids do **not** exist in
kaidoku's committed registry: `corpus/SOURCES.md` has exactly 106 rows, `S001`…`S106`
(`grep -c '^| S[0-9]'` → 106), and `git log --all -S 'S150' -- corpus/SOURCES.md` /
`-S 'S136'` return nothing — the ids never existed in any commit of this lane. They are
*campaign-staged* ids: the round-4 lane message states "CONTINUE the S-id space: the first
new row id is **S136** (the lane registry ends at S135 counting every row staged so far)"
(`shokuknow/.ufo/waves/corpus-expansion-1/wave4-messages/ScoutKaidoku.md:19`). The lane's
own `.ufo/waves/round-35/assimilation/staged-ids` is the contiguous pool `S106`…`S237`
and already contains S113/S117/S136/S147/S150 **and** C1's S125/S129 — so the five
quarantined ids are occupied and must never be re-allocated.

---

## 2. Hand-check of the five rows — all five re-derived independently

Staged rows and gate blocks read from the campaign lane tree
(`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round{4,5}/SOURCES-PROPOSED.md`).

| id | staged source (row cell 1 / anchor cell 5) | gate-block quote | gate-block "also" | location named |
|---|---|---|---|---|
| S136 | own-work `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` | `Answer: the adb surface is **bound and partially live** — 2 of 24 verbs are` | `the other 22 all demand a \`<serial>\`` | file + heading 「kaidoku-r4u / 06 — ADB surface: client present, zero devices」 |
| S147 | `agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` | `207 tools` | ``Do not run `rea-agents setup --client …` `` | § "REA release" and § "Expected doctor output" |
| S150 | zenn.dev/yasu01/articles/7370bd5d414ec4 | `GNU Binutils に含まれる逆アセンブラ。ほぼすべての Linux 環境に入っています。` | `strip されていても PLT のシンボルは残る場合があるので、ここが最初の手がかりになりました` | §「逆アセンブル」 and §「シンボルがない場合のヒント」 |

### S150 — live fetch 2026-10-25 (the REFUSE row)

```
curl -sS -L -o s150-zenn.html -w 'http=%{http_code} size=%{size_download}' \
     'https://zenn.dev/yasu01/articles/7370bd5d414ec4'
http=200 size=174088                       # byte count matches the committed verdict exactly
sha256 s150-zenn.html = 6d1b2137fd3cbf2908be97cfeefb253bca63c090758b1b6a16a1ae94f43845ed
```

Measured in the served bytes:

- `ヒント` → **0** occurrences; `シンボルがない場合のヒント` → **0** occurrences.
- `<title>`, `og:title` and `<h1>` all equal
  `実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む` (exact match to the verdict).
- Full heading inventory (h1–h4): はじめに / 道具の準備 / objdump / llvm-objdump /
  readelf / 実例：小さなプログラムを逆アセンブルする / Step 1…Step 4 / パターン認識のコツ
  (関数の境界, 文字列参照, 分岐の構造, ライブラリ関数の特定) / AArch64 で同じバイナリを読む /
  読み進めるためのワークフロー / まとめ / シリーズを終えて. **No heading contains ヒント**,
  and **no heading is 逆アセンブル** (the two sections named in the row's anchor are both
  absent as headings).
- `<p data-line="69" class="code-line"><code>strip</code> でシンボル…` — the "strip
  walkthrough at data-line 69" detail of the verdict is **confirmed**.
- **The row's own quoted payload IS present**: gate quote → 2 occurrences; gate "also"
  quote → 2 occurrences. `https://zenn.dev/api/articles/7370bd5d414ec4` (HTTP 200,
  69,896 B) reports `published_at 2026-05-23`, `body_updated_at 2026-06-04` — the article
  has not changed since the row was opened (2026-10-23), so the missing heading is not a
  post-staging edit.

### S113 — live fetch 2026-10-25

```
curl -sS -L -o s113-adb.html 'https://developer.android.com/tools/adb?hl=en'
http=200 size=368063                      # byte count matches the committed verdict exactly
sha256 s113-adb.html = ec42553f5ece0128683b6ac9e57ecb3fcbab98269fc52f5f9bf5093cf7438b50
```

- 22 `<link rel="alternate" hreflang=…>` entries: `en`, `x-default`, and 20 locale codes
  (`ar bn zh-Hans zh-Hant fa fr de he hi id it ja ko pl pt-BR ru es-419 th tr vi`).
- `tools/adb?hl=ja` alternate present, count **1** (verdict confirmed).

### S117 — live fetch 2026-10-25

```
curl -sS -L -o s117-doi.bin -w 'http=%{http_code} size=%{download_size}' \
     'https://doi.org/10.1109/SP46214.2022.9833799'
http=202 size=0   url_effective=https://ieeexplore.ieee.org/document/9833799/
sha256 s117-doi.bin = e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The digest is the sha256 of the empty string — the 202/empty-body verdict is **confirmed
exactly**.

### S136 — own-work artifact (lane tree)

```
corpus/knowledge/2026-10-13-r4u-06-adb-surface.md   12,897 B
sha256 26eeaf6f91eee756e962b9259e1f600f45819c653a659a86a8dacf1e87aa26bf
line 3  : # kaidoku-r4u / 06 — ADB surface: client present, zero devices   # heading exact
line 8  : Answer: the adb surface is **bound and partially live** — 2 of 24 verbs are
line 9  : device-free and now return real evidence; the other 22 all demand a `<serial>`
grep -c '2 of 24 verbs are' → 1
```

Gate quote, gate "also" and the heading all reproduce verbatim — **confirmed**.

### S147 — own-work artifact (host tree)

```
~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md   3,386 B
sha256 ab36b310b285c0278bef2a62ccdc5effe9cdc2d232e4e684452c17be264b58fe
line 41 : - REA release: `rea-agents@6.7.0`, skill v42, 207 tools.      # § "REA release"
line 46 : ## Expected `doctor` output on this host                     # § "Expected doctor output"
line 23 : - Do **not** run `rea-agents setup --client <client>` …      # the "also" quote
```

`207 tools` → present (line 41); the "also" quote is present modulo markdown bold and the
`<client>` placeholder. **Confirmed** (with the locator precision caveat in F4).

---

## 3. First falsifications

### F1 (material) — the S150 "REFUSE (fabrication class)" is overstated; the ABSENT was raised against a mis-extracted span

The census did **not** check the row's quoted evidence. Its finding for S150 is:

```json
{"lane":"kaidoku","round":"round5","id":"S150","verdict":"ABSENT",
 "quote":"シンボルがない場合のヒント",
 "line":"- anchor: article §「逆アセンブル」 and §「シンボルがない場合のヒント」, part 4 of a 6-part series",
 "url":"https://zenn.dev/yasu01/articles/7370bd5d414ec4","binding":"id"}
```

The extracted "quote" is the **anchor's section name**, harvested because
`quote-lint.py:73` `QUOTE_SPAN_RE` treats `「」` (and `『』`, `“”`) as quote delimiters.
The gate block's real quoted sentence is plain prose with no delimiters, so the checker
never tested it. The register then wrote the class note "cited source, companion URLs and
local artifacts were all checked; the quote is in none of them" — which is false for this
row: the row's quote was never checked.

Live evidence (above): the row's gate quote and its "also" quote are both present verbatim
in the served bytes (2 occurrences each), and the article is unchanged since staging. So
the correct disposition is **"the anchor names two sections that do not exist → re-anchor
and re-open"**, which is exactly the repair the register's own class definition prescribes
("the fabrication class: verify by hand, then correct the quote or refuse the row"). A
refusal should be reserved for a row whose quoted payload is genuinely absent; S150's is
present. `quote-lint.py`'s own docstring already names the phenomenon as distinct from
fabrication: *"two whose anchor named a section the quote was not in"*.

Blast radius: the overstatement lives only in the committed prep artifact
`quarantine-verdicts.md`. It does **not** touch C1 or C2 (see §4) and no registry row was
appended for S150, so nothing in the corpus asserts the fabrication.

### F2 (minor) — S113's "17 locales plus x-default" does not match the served bytes

The served page carries **22** hreflang alternates = `en` + `x-default` + **20** locale
codes (`ar bn zh-Hans zh-Hant fa fr de he hi id it ja ko pl pt-BR ru es-419 th tr vi`).
No counting rule that is stated anywhere yields 17 (20 locales; 22 entries; 16 if the four
region-qualified codes are dropped; 17 only if three of those four are dropped
arbitrarily). The rest of the S113 verdict (HTTP 200, 368,063 B, `?hl=ja` alternate
count 1) is confirmed. Confidence: high (byte count matches the committed capture exactly,
so the verdict author saw the same bytes).

### F3 (attribution) — "the gate block named no locator" is a checker blind spot, not a defect of the gate blocks

`quote-lint.py:348-374` (`local_locator`) resolves a gate block's evidence path only if
`pathlib.Path(raw).exists()` **or** `lane_dir / raw` exists, where `lane_dir` is
`shokuknow/lanes/kaidoku`. S136's evidence lives in the *lane repo*
(`kaidoku-shokunin/corpus/knowledge/…`) and S147's under `$HOME`
(`~/.agents/skills/…`); neither path resolves from `lane_dir`, so the checker emitted
`no-locator` and left both rows unchecked. Both gate blocks **do** carry a `- URL:` line
naming a local artifact, and both quotes verify (measured above). The tool's own comment
says so: *"A row that names such an artifact was checked by NOBODY when this tool
reported it as `no-locator` … Reporting the row as `no-locator` leaves it unchecked."*
The committed verdict's phrase "the location is now supplied" should read "the checker's
locator resolver could not open a lane-repo or `$HOME` path; the location was always in
the gate block".

### F4 (precision) — S147's line citations 18/41/53 do not all carry the named tokens

`rea-agents@6.7.0` → line 18 ✓ (also 32, 33, 41, 60); `skill v42` → line 41 only;
`207 tools` → line 41 only; line 53 carries a bare `6.7.0` digest string
(`Pristine 6.7.0 digest is …`) and no `rea-agents@` prefix, no `v42`, no `207`. So two of
the three cited lines support the sentence; the third supports a different token.

### F5 (reproducibility) — the slice is not reproducible from lane bytes alone

The committed verdict records the extraction **command** but not its **output**: the
artifact the command writes (`$A/quarantine-slice`) is neither tracked
(`git ls-files .ufo/waves/round-35/assimilation/` lists only `census-start.txt`,
`collisions`, `id-guard-proof/*`, `quarantine-verdicts.md`, `reg-ids`, `staged-ids`) nor
present on disk. In addition the register itself is a **sibling-repo** file whose digest is
recorded nowhere in the lane (`claims-canonical.json` pins only
`.ufo/waves/round-35/assimilation/census-start.txt`), and the register is regenerated
periodically upstream. Pinning the digest + commit (currently
`5afe1810…` @ `d4ab45f2…`) and committing the slice output would make the slice
re-derivable.

---

## 4. Scope check — the slice is outside both frozen claims

Neither counter mentions the quarantine slice, the register or the verdicts file:
`grep -n 'quarantin|absent-defect|register|verdicts' tools/round-35/c1-coverage-counter.py
tools/round-35/c2-calibration-counter.py` → **no matches**. C1's constants are the two
target entry paths ↔ `S125`/`S129` only; C2's constants are D-1…D-4 only. The quarantine
slice is therefore prep/assimilation evidence, cannot satisfy either predicate, and its
verdicts cannot be used as claim data. Consistent with the verdict file's own closing
line ("No row is appended; adoption stays closed to the admitted jsc2js entries").

Registry state that supports "no adoption happened": `corpus/SOURCES.md` = 106 rows
(S001–S106) — none of S113/S117/S136/S147/S150 present, and S125/S129 not yet present
(they land with C1 data). `git log --all -S` finds no trace of the five quarantined ids
in `corpus/SOURCES.md` in any commit.

---

## 5. Advisory (not applied — no lane production file may be written by this seat)

1. **Append a correction** to the committed `quarantine-verdicts.md` (executor/scribe
   seat): S150's disposition is "anchor misnamed / repairable", not fabrication-class
   refusal, and the S113 hreflang count is 22 (20 locales + `en` + `x-default`). This is
   an append to a prep record; it does not require re-freezing C1/C2, whose predicates
   and counters do not read it.
2. **Pin and commit** the derivation: register digest + shokuknow commit in the prep file,
   and the `quarantine-slice` output the documented command produces.
3. **Keep the five ids retired** in any future S-id allocation (they are already inside
   the lane's `staged-ids` pool S106–S237); C1's S125/S129 do not collide with them.
4. If the lane wants the register's `no-locator` class to mean what it says, the fix
   belongs to the checker's resolver (lane-repo and `$HOME` path roots), not to the rows.

## 6. Limits / unresolved

- `lsp` device unavailable → symbol/caller tracing done by literal text search
  (`grep`, `git log -S`); grep matches are literal, not semantic, evidence.
- Network observations are as of 2026-10-25 (this session). The zenn article is stable
  since 2026-06-04; the Android page and the IEEE redirect are live-time dependent, and
  the `?hl=ja`/hreflang inventory can change upstream.
- I read the campaign's `quote-lint.py`, `absent-defect-register.py`, `locator.py`,
  `quote-lint-full-v5.json` and the four kaidoku lane files; I did **not** open the
  `.qcache` HTML cache or re-run the census (that would be a re-measurement of other
  lanes' rows and is out of scope).
- I did not run either counter, did not modify any lane file other than this report, did
  not touch VCS/index/jj state, did not write to `/home/vgpnk/Projects/shokuknow`, and
  installed nothing.

## 7. Captured evidence (private, outside the lane)

```
/fast/scratch/hyaku/kaidoku-r35/w1/R35ReconQuarantine/
  s150-zenn.html  174,088 B  sha256 6d1b2137fd3cbf2908be97cfeefb253bca63c090758b1b6a16a1ae94f43845ed
  s150-api.json    69,896 B  sha256 c0129e418bee1c073afe75c9f6dd58980a346ea418ae90c977c1e4e5d3ecba05
  s113-adb.html   368,063 B  sha256 ec42553f5ece0128683b6ac9e57ecb3fcbab98269fc52f5f9bf5093cf7438b50
  s117-doi.bin         0 B  sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```
