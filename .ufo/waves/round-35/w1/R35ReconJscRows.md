# R35ReconJscRows — S125/S129 rows and captured sources: evidence and first falsifications

Seat: `R35ReconJscRows` (scout, wave 1). Scope: inspect the S125/S129 rows and the captured
sources for claim C1. Read-only everywhere; the only lane write is this report. No VCS
mutation, no counter/predicate edit, no corpus/SOURCES/PROVINCE/README/lesson/SCORECARD/LOG
write, no delegation, no nested background work, no pacman install, no traversal under
`/fast/scratch`, no write outside the lane.

Milestone: **Build evidence and first falsifications**.

---

## 0. Bottom line

1. **S125 and S129 do not exist in this lane's registry.** `corpus/SOURCES.md` holds exactly
   106 rows, `S001`–`S106`, all `status=mined` (102) / `rejected` (4); there is no `S125`
   and no `S129`. Both ids exist only as *staged* rows in the sibling package
   `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` (lines 26 and 30) and in
   that lane's proposals (`lanes/kaidoku/round2/SOURCES-PROPOSED.md:21`,
   `lanes/kaidoku/round3/SOURCES-PROPOSED.md:15`).
2. **The sibling rows, copied verbatim, fail the frozen C1 counter** on two named checks
   (`registry_opened_not_this_round`, `registry_usedby_missing`) — measured, not inferred.
3. **The sibling rows are also structurally incompatible with this lane's registry parser**
   (escaped pipe in the `recheck` cell → 13 pipes → `E01 fields=12`; `E09 invalid recheck`;
   `E11` on the used-by path). They must be re-authored in lane shape, not copied.
4. **A lane-conformant S125/S129 pair turns C1 green** — counter exit 0 *and* census exit 0 —
   in a `/tmp` git fixture (recipe in §4).
5. **First falsification of the S129 claim text:** the sibling row says the 677 releases span
   "V8 majors 9, 11 and 15". They span **majors 5–15** (11 majors). The error is already
   visible in the lane's own two captures (page 7 is 100% V8 major 12).
6. **First falsification of the round-35 lesson's S125 quote:** the quoted sentence is not
   byte-present in the capture (the `**bold**` markers are dropped in the quote).

---

## 1. What S125/S129 are, and where they actually live

| artefact | path | state |
|---|---|---|
| lane registry | `kaidoku-shokunin/corpus/SOURCES.md` | 106 rows `S001`–`S106`; **no S125/S129** |
| staged package rows | `/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` lines 26 (S125), 30 (S129) | present, `mined`, `opened=2026-10-23` |
| sibling proposals | `shokuknow/lanes/kaidoku/round2/SOURCES-PROPOSED.md:21` (S125), `round3/SOURCES-PROPOSED.md:15` (S129) | present |
| sibling knowledge entries | `shokuknow/merge/kaidoku/knowledge/corpus/knowledge/jsc-mapper-cli-contract.md`, `…/jsc-mapper-release-inventory.md` | present; their `source:`/`verified-at:`/`recheck:` lines are on lines 4–6 |
| lane captures (this round) | `kaidoku-shokunin/.ufo/waves/round-35/prep/jsc-sources/{jsc2js-readme.md, releases-page1.json, releases-page7.json}` | tracked in commit `d2729cba895b8664f3ccb27196091494f3cda83b` (2026-10-25) |
| id reservation | `.ufo/waves/round-35/assimilation/{reg-ids,staged-ids,collisions}` | `reg-ids` = S001–S106; `staged-ids` = S106–S237; `collisions` = `S106` only |
| round-35 lesson | `corpus/lessons/round-35.md` §Gate | S125/S129 **admitted as sources, no row appended** ("No source row is appended by this lesson itself") |

Commands:

```
grep -oE "^\| S[0-9]+" corpus/SOURCES.md | tr -d '| '        # → S001 … S106 (106 ids)
grep -rn "S12[5-9]" --include=*.md --include=*.json .        # S125/S129 only in .ufo/waves/round-35/** and shokuknow
comm -12 <(sort .ufo/waves/round-35/assimilation/staged-ids) \
        <(sort .ufo/waves/round-35/assimilation/reg-ids)    # → S106 (single collision)
```

---

## 2. Captured sources — independently re-verified

### 2.1 S125 — jsc2js README (the `.jsc` mapper's own contract)

Capture: `.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md`, 8 996 B,
sha256 `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`.

| check | result |
|---|---|
| live re-fetch 2026-10-25 `raw.githubusercontent.com/xqy2006/jsc2js/main/README.md` | sha256 **identical** to the capture (`df85060f…`), 8 996 B |
| `grep -c 'loadjsc'` on capture **and** on live | **6** = the sibling row's recheck value → reproducible |
| § 项目简介 present / § 快速开始 present | yes (1× each) |
| sibling S125 quote `` `jsc2js` 用于将v8生成的 **JSC 字节码**逆向为可读的 JavaScript。 `` | present, 1× |
| `./d8 -e "loadjsc('path/to/xxx.jsc')" > xxx.txt` | present (2×, zh + en) |
| `python view8.py --disassembled ../xxx.txt ../xxx.js` | present (2×) |
| version-match warning `不同 V8 版本的 Bytecode 指令集…请务必使用 **匹配版本** 的 d8` | present (zh + en) |
| caveat `还原 JS 不能 100% 重建原始源码` / `JavaScript reconstruction cannot be 100% identical to the original` | present (zh + en) |
| lower-bound statements `V8 5.1 是当前 \`.jsc\` 路径的兼容下界` / `V8 5.1 is the compatibility lower bound` | present (zh + en) |
| README's own counts: `369` tags, `358`, `356`, `45`, `20`, `57` failed tags (14.7.84–15.3.25) | present; **these are the README's tag counts, not the release count — do not conflate** |

### 2.2 S129 — jsc2js Releases (the version index)

Captures: `releases-page1.json` (100 items, sha256 `4a5199ddf709ec41b6a1109b5d5598356892d6a4aad227dc873fe3869a0f813c`),
`releases-page7.json` (77 items, sha256 `499e2b227a6eb2c3059a8df280e52dc7dd5c597d50a1cdbabc1ff98a20e199fc`).

| check | result |
|---|---|
| live API page 1 sha256 vs capture page 1 sha256 | **identical** (`4a5199dd…`) → capture is not stale |
| live `Link` header, `per_page=1` | `rel="last" … page=677` → **677 releases total** |
| HTML pager `data-total-pages` | `"68"` → matches the sibling anchor's "68 pages at 10 per page" |
| full crawl of all 68 HTML pages | **677 distinct tags, 0 duplicates**, majors `{5:12, 6:18, 7:54, 8:79, 9:66, 10:55, 11:83, 12:78, 13:92, 14:90, 15:50}` |
| `grep -c 'Patched d8 for V8'` on captured page 1 | **100** = the sibling row's recheck value → reproducible, but see falsification F-3 |
| every captured release body contains `includes d8 + snapshot_blob.bin` | 177/177 |
| release assets | exactly 2 per release: `d8-<tag>-linux.tar.gz`, `d8-<tag>-windows.zip`; downloaded `15.6.75.19` linux asset (sha256 `3701563a0f1009577374a78f04b7d9de47b99a52280a543f0e49525742137776`) → tar lists `d8`, `snapshot_blob.bin` |
| page ordering | not strictly id/created_at monotonic (5 ascending violations per page, identical live and captured) — GitHub's own CI ordering, not a capture artifact |

### 2.3 Quoted-source hygiene

`corpus/SOURCES.md` today: **0 of 106 rows contain any CJK character** in the row
(`re.search(r'[一-鿿]', row)` → no hit). The sibling S125 scope claims "the lane's first
natively Chinese-authored tool documentation"; for *this* lane's registry that novelty holds
only once the row is written, and it must be re-derived from the row, not inherited.

---

## 3. First falsifications

**F-1 — verbatim sibling rows fail the frozen counter.** Built a `/tmp` git repo with the two
merge rows appended unchanged, the two entries, a PROVINCE row and a README row; ran the
frozen counter (`tools/round-35/c1-coverage-counter.py`, `--rev HEAD --freeze HEAD`):

```
C1_FAIL: registry_opened_not_this_round:S125=2026-10-23;
          registry_usedby_missing:S125:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md;
          registry_opened_not_this_round:S129=2026-10-23;
          registry_usedby_missing:S129:corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md
EXIT=1
```

Cause: the counter requires `cells[7].startswith("2026-10-25")` (this round's opening date)
and `cells[9]` (used-by) to contain the **lane** entry path `corpus/knowledge/2026-10-25-r35-jsc2js-*.md`.
The sibling rows carry `opened=2026-10-23` and `used-by=corpus/knowledge/jsc-mapper-cli-contract.md`
/ `…-release-inventory.md`. Both are correct for the sibling lane and wrong here. The lane's
own capture commit is dated 2026-10-25, so `opened=2026-10-25` is the honest value.

**F-2 — verbatim sibling rows break the lane's own census.** Feeding the same two rows to
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate`:

```
E01  S125 fields=12      # the recheck cell contains an escaped `\|` → 13 pipes → NF=14
E01  S129 fields=12
E11  S125 missing used-by grep -c 'loadjsc'` -> 6 (ran 2026-10-23)   # pipe shift corrupts the cell
E11  S129 missing used-by grep -c 'Patched d8 for V8'` -> 100 (ran 2026-10-23)
EXIT=1
```

A recheck cell of the shape `180d — \`curl … | grep -c …\`` also trips **E09 invalid recheck**.
This lane's own 106 rows use a bare cadence token in that cell — `on-release` 78, `180d` 12,
`90d` 10, `365d` 6, no long strings — so the recheck *command* belongs in the lesson §Gate
(where round-35 already puts it), not in the registry cell. **Do not copy the sibling rows.**

**F-3 — the S129 scope/teaches text is wrong about majors.** The sibling row states "677 V8
versions spanning V8 majors **9, 11 and 15**" (scope + teaches; the same sentence appears in
`lanes/kaidoku/round3/REJECTIONS.md:39` and `round3/KNOWLEDGE-PROPOSED.md`). Measured from the
68-page crawl: majors **5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15** — eleven majors; 12 majors'
worth of releases (5–8, 10, 12–14) are absent from that claim. The error is already visible
inside the lane's own captures: captured page 1 holds majors {9:3, 11:75, 15:22} and captured
page 7 is **100 % major 12** (77/77). Any adopted S129 row must state the true span (or the
measured per-major counts), and the sibling's `teaches` cell must not be inherited verbatim.
Note also that the sibling's recheck value `grep -c 'Patched d8 for V8'` → 100 counts **one
API page**, not the inventory; it cannot detect a change in the total.

**F-4 — the round-35 lesson's S125 quote is not byte-present.** `corpus/lessons/round-35.md`
§Gate quotes "choose the V8 version that is identical to the one that produced your target
`.jsc`". In the capture the bytes are
`choose the V8 version that is **identical to** the one that produced your target \`.jsc\``
(line 130). The quote as written (bold markers dropped) occurs **0 times**; the bold-inclusive
form occurs 1×. The quoted line *is* inside the cited range "captured lines 128-157", so only
the quoting is inexact.

**F-5 — id-allocation tension (advisory, not a counter failure).** `CORPUS.md` §Registry:
"`id` — `S` + 3 or more digits, **the next unused**; never reused." This lane's next unused
id is `S107`, so adopting `S125`/`S129` (as the frozen predicate demands) leaves `S107`–`S124`
permanently unused in this registry. `S125`/`S129` are inside the staged range and collide
with nothing (`collisions` = `S106` only, which is the pre-existing r34 binutils row vs the
staged unblob row — not ours). The gap must be acknowledged in the lesson when the rows land.

**F-6 — counter/census divergence (frozen counter; report only).** All measured in `/tmp`
fixtures with the frozen counter:

| mutation | counter | census |
|---|---|---|
| rows fully conformant (this lane's shape) | `C1_CLEAN`, exit 0 | `ok`, exit 0 |
| extra pipe appended at end of a row | `C1_CLEAN`, exit 0 | `E01 fields=12`, exit 1 |
| extra pipe inside the scope cell | exit 1 (`registry_status_not_mined` — the shift makes the *anchor* land in the status cell) | `E01` |
| S125 row placed **after** `## Paths` (outside `## Registry`) | `C1_CLEAN`, exit 0 | `E12 row outside Registry section`, exit 1 |
| `used-by` names a path that does not exist on disk | `C1_CLEAN`, exit 0 | `E11`, exit 1 |
| used-by written as a bare basename (no `corpus/knowledge/` prefix) | exit 1 (`registry_usedby_missing`) | — |
| provenance trio not at the top of the entry (prose first) | `C1_CLEAN`, exit 0 | — |
| PROVINCE/README hold the stem in **prose**, not in a table row | `C1_CLEAN`, exit 0 | — |

So the counter's PROVINCE/README checks are unbounded substring tests (already recorded in
`corpus/lessons/round-35.md`: "the frozen C1 counter has an unbounded semantic scope check"),
and a row can satisfy the counter while the lane census rejects it. The counter also never
validates that the entry's `source:` line names the right URL or that the entry says anything
true about the source.

**F-7 — README filename form is load-bearing.** The counter requires the **filename with the
`.md` extension** in `corpus/README.md` (`readme_missing:corpus/knowledge/….md`). Following
the lane's common README convention `` `knowledge/<stem>` `` (no extension) **fails**:
`C1_FAIL: readme_missing:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md`. In
PROVINCE.md either form passes (stem, or stem + `.md`).

---

## 4. Lane-conformant green recipe (measured, in `/tmp`, no lane writes)

Row shape (11 cells, no `|` inside any cell, bare cadence in `recheck`):

```
| S125 | jsc2js upstream README — https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md | docs | A |
  <scope> | README.md § "项目简介" and § "快速开始" (branch `main`; lane capture
  `.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md` sha256 `df85060f…`, re-fetched
  byte-identical 2026-10-25) | <teaches> | mined | 2026-10-25 | 180d |
  corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md |
```

Entry shape — the three lines must be `^source:` / `^verified-at:` / `^recheck:` and the
`source:` line must contain the row id (`S125` / `S129`):

```
source: S125 — https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md — § "项目简介" and § "快速开始", branch `main`, as fetched 2026-10-25
verified-at: 2026-10-25 (capture sha256 `df85060f…`)
recheck: 180d — `curl -fsSL … | grep -c 'loadjsc'` -> 6 (ran 2026-10-25)
```

PROVINCE.md: the stem (with or without `.md`); `corpus/README.md`: the **filename with `.md`**.

Measured result on that fixture:

```
python3 -I -B tools/round-35/c1-coverage-counter.py --root <fixture> --rev HEAD --freeze HEAD
  → C1_CLEAN revision=HEAD            EXIT=0
scripts/sources-census.sh validate --root <fixture> --today 2026-10-25 .
  → r35c1green  ok  …/corpus/SOURCES.md   EXIT=0
```

Counter run against the **lane's own** tree, for the record:

```
--rev HEAD (3ecf4298)  → C1_FAIL: entry_missing ×2, registry_row_missing:S125/S129,
                         province_missing ×2, readme_missing ×2        EXIT=1
--rev aa04633a (base) → identical failure set                       EXIT=1
```

(The committed do-nothing receipt `.ufo/waves/round-35/controls/c1-do-nothing.json` reports the
same eight failures at base.)

---

## 5. Limits / what this report does not establish

- **Read-only, advisory.** No row, entry, PROVINCE/README/lesson/SOURCES edit was made; no
  counter, predicate, claims or scope change; no VCS/index/jj state touched; nothing written
  outside `.ufo/waves/round-35/w1/`. All fixtures live in `/tmp`.
- **Nothing here scores C1 or C2.** The green recipe is a *fixture* result at an unreferenced
  `/tmp` repo, not a lane measurement and not a claim adjudication.
- **Live fetch was rate-limited** partway: unauthenticated GitHub API core budget (60/h) was
  exhausted after page 4, so pages 5–7 of the API were not re-fetched live in this session;
  the 68-page HTML crawl (which needs no API budget) supplied the complete 677-tag census and
  is the basis for F-3. Captured page 7 was not re-fetched live here; its identity to the live
  page 7 is asserted by `R35Audit02.md` (which reports full JSON equality), not by me.
- **The 677 figure is confirmed** (API `Link rel="last" page=677` and the 68-page crawl), but
  the *per-major* breakdown in F-3 comes from the HTML tag crawl; the API listing's own
  ordering is non-monotonic, so per-major counts from the API pages are a different cut.
- **Not verified:** that the d8 builds actually work on any carrier (no execution), that the
  mapper's output is correct for any V8 version, that the 14.8/Electron-42 pairing the lane
  still lists as an open lead is covered by a release (the crawl shows 18 `14.8.*` tags, but
  no d8 was run), and that any of the sibling's `teaches` prose about "the lane's first
  Chinese-authored tool documentation" transfers to this lane.
- **C2 interaction (not my item, flagged only):** appending two rows moves the registry from
  106 to 108 rows. C2 D-1 pins the census-start receipt (rows=106) to be committed before the
  first `corpus/SOURCES.md` change after base; any adoption seat must order the two commits
  accordingly and must not restate the base row count.
- No `find`/`du` under `/fast/scratch`; no pacman install; no nested delegation.

Report: `.ufo/waves/round-35/w1/R35ReconJscRows.md`
