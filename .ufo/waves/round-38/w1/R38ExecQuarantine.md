# R38ExecQuarantine — round-38 w1, quarantine slice hand-check (kaidoku)

Seat: `R38ExecQuarantine` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
(HEAD `cb4326b2aa4c2024af0651fe6115b82d0c4de3df` at read time). Axes: coverage, calibration.
Milestone: round-38 build drafts and first falsifiers. This seat's move: derive the kaidoku
quarantine slice from the **absent-defect-register (read-only)** and hand-check every row
against its cited source. No counter, carrier, oracle or frozen predicate was touched.

## 1. Inputs read

| input | role |
|---|---|
| `plans/round-38-claims.md` | frozen claims R38-C1 (coverage: BE SquashFS v4 → Core), R38-C2 (calibration: self-assessment surfaces) |
| `corpus/lessons/round-37-verifier-spotcheck.md` | routed defects R37-CL1..CL3, R36-CL1..CL6 carried into this round |
| `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | read-only source of the slice; sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines |
| `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/quote-lint-full-v5.json` | per-row quote/verdict records (see §2 note) |
| `/home/vgpnk/Projects/shokuknow/lanes/kaidoku{/round4,/round5}/SOURCES-PROPOSED.md` | the five registry rows named by the slice (read-only) |
| lane `corpus/SOURCES.md`, `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md`, `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` | anchor targets for S136 / S147 |

## 2. Slice derivation (exact command, 5 rows, every line carries an S-id)

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

Output — **count = 5**:

```
 S150   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S117`   the cited source could not be fetched, so no quote was checked
 S136`   the gate block named no locator, so no quote was checked
 S147`   the gate block named no locator, so no quote was checked
```

Register lines: 82 (S150), 315 (S113), 316 (S117), 317 (S136), 318 (S147). Line 254
(`| `kaidoku` | 1 |`, the per-lane total) is excluded by the `round[0-9]+` predicate. The
per-lane totals row says kaidoku has **1** payload-absent row, which agrees with the slice:
exactly one fabrication-class row (S150) and four never-checked rows.

Note on the trailing backtick in `S113``…`S147``: the register's *"Rows whose quotes were NEVER
CHECKED"* table has one fewer column, so `$4` carries the id together with a stray backtick and
`$5` carries the reason instead of a class. The ids are still unambiguous.

The quoted data in `quote-lint-full-v5.json` for these five ids is: S150 `verdict=ABSENT`
with the quote string; S113, S117 `verdict=fetch-failed`; S136, S147 `verdict=no-locator`. The
three never-checked ids carry **no quote string at all** in that JSON, so for those rows the
hand-check was done against the registry row's own `anchor`/`teaches`/`recheck` columns and its
own reproducible recheck command (`lanes/kaidoku{/round4,/round5}/SOURCES-PROPOSED.md`), not
against a lint quote. That is stated per row below; it is not a substitution of an easier test.

Slice file: `artifacts/R38ExecQuarantine/quarantine-slice` (5 lines, every line S-id-bearing).
The path the assignment names, `.ufo/waves/round-38/assimilation/quarantine-slice`, **already
existed before this seat ran** and is **byte-identical** to the derived slice:

```
$ diff -u .ufo/waves/round-38/assimilation/quarantine-slice \
          .ufo/waves/round-38/w1/artifacts/R38ExecQuarantine/quarantine-slice && echo SLICE-IDENTICAL
SLICE-IDENTICAL
$ sha256sum .ufo/waves/round-38/assimilation/quarantine-slice
7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a  .ufo/waves/round-38/assimilation/quarantine-slice
```

Deviation, deliberate: this seat did **not** write into `.ufo/waves/round-38/assimilation/`
(the binding Bounds allow only this report and `w1/artifacts/<seat>/`). The pre-existing file is
identical, so the L1 has the slice at the required path without any write from here.

## 3. Verdicts (hand-check, live 2026-10-26)

Full text with exact anchors: `artifacts/R38ExecQuarantine/quarantine-verdicts.txt`.

| id | round | register class | verdict | evidence (exact) |
|---|---|---|---|---|
| S150 | round5 | `payload-absent` | **REFUSE (fabrication class)** | zenn.dev/yasu01/articles/7370bd5d414ec4 → HTTP 200, 174,088 B, sha256 `42d59c48…766e34`; `シンボルがない場合のヒント` = **0**, `ヒント` = **0**, `シンボルがない` = **0**; real H2s listed below; `パターン認識のコツ` = 4 (real `<h2 id="…パターン認識のコツ">`); row's own recheck `grep -c llvm-objdump` → **6** (matches the row) |
| S113 | round1 | never-checked (fetch failed) | **ADOPT-WITH-ANCHOR, count must be re-stated** | developer.android.com/tools/adb?hl=en → HTTP 200, 368,063 B, sha256 `e6d50f92…769198`; **22** `hreflang` = **21 locales + `x-default`**; `grep -c 'tools/adb?hl=ja'` → **1** (row's recheck). Row scope says "served in **17** locales" — not reproducible from live bytes |
| S117 | round1 | never-checked (fetch failed) | **UNVERIFIABLE (not fabrication)** | DOI → 302 → `ieeexplore.ieee.org/document/9833799/` HTTP **202**, **0-byte** body; Semantic Scholar graph API HTTP **429** on two attempts 20 s apart; dblp returns a bot-challenge page (HTTP 202). Crossref (DOI-keyed, HTTP 200): title `SoK: Demystifying Binary Lifters Through the Lens of Downstream Applications`, *2022 IEEE Symposium on Security and Privacy (SP)*, pp. 1100-1119 — paper exists, abstract text unchecked |
| S136 | round4 | no-locator | **ADOPT-WITH-ANCHOR** | `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md`, 12,897 B; heading line **3** `# kaidoku-r4u / 06 — ADB surface: client present, zero devices`; `2 of 24 verbs are` occurs **1×**, line **8**; row recheck `grep -c` → **1** |
| S147 | round5 | no-locator | **ADOPT-WITH-ANCHOR**, locator heading names approximate | `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`, 3,386 B; `grep -c '207 tools'` → **1**, line **41** `- REA release: \`rea-agents@6.7.0\`, skill v42, 207 tools.`; real headings are `## State as of this writing` (39) and `## Expected \`doctor\` output on this host` (46) — there is no "REA release" heading |

Tally: 3 adopt-with-anchor (S113 with a count correction, S136, S147), 1 refuse
(fabrication class, S150), 1 unverifiable (S117). Nothing was adopted into any corpus file by
this seat; adoption is the L1's call.

### 3.1 S150 — the fabrication is one section heading, not the row's substance

Live page (single fetch, body stable with the round-35/36 captures at 174,088 B):

```
h1 実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む
h2 はじめに / 道具の準備 / 実例：小さなプログラムを逆アセンブルする / パターン認識のコツ /
   AArch64 で同じバイナリを読む / 読み進めるためのワークフロー / まとめ / シリーズを終えて
```

Neither section the row's anchor names exists: there is no `シンボルがない場合のヒント`
heading (0 occurrences of `ヒント` anywhere in the served bytes) and no `逆アセンブル` heading
(the string only occurs 18× as body text / inside `実例：小さなプログラムを逆アセンブルする`).
The article is genuinely about reading symbol-less binaries (`strip` 14×, `PLT` 8×,
`AArch64` 6×, `objdump` 42×), and the row's own recheck still passes, so the correct disposition
is **re-anchor, not delete**. Flip condition: re-anchor to a real contiguous span (the H2
`パターン認識のコツ`, or the `strip` walkthrough at `data-line="154"`) and re-open.

### 3.2 S113 — mechanism present, number wrong

```
$ curl -fsSL 'https://developer.android.com/tools/adb?hl=en' | grep -c 'tools/adb?hl=ja'
1
$ grep -o 'hreflang="[^"]*"' adb.html | wc -l
22
$ grep -o 'hreflang="[^"]*"' adb.html | sed 's/.*="//;s/"//' | sort -u | tr '\n' ' '
ar bn de en es-419 fa fr he hi id it ja ko pl pt-BR ru th tr vi x-default zh-Hans zh-Hant
```

21 language tags + `x-default` = 22 `hreflang` links. The row's load-bearing inference ("one
document rendered into many locales, so an adb citation must pin `?hl=`") is true and
locatable; the numeral **17** is not. This is a calibration defect in the row's scope prose, not
a fabricated source, and it matters now because round-38's C2 predicate is a
zero-mismatch predicate over stated counts: any successor surface that quotes "17 locales" from
this row would carry a false count into a claim.

### 3.3 S117 — publisher serves nothing; identity confirmed elsewhere

`https://doi.org/10.1109/SP46214.2022.9833799` → `302` → `https://ieeexplore.ieee.org/document/9833799/`
→ `HTTP 202`, `size_download=0`. Semantic Scholar graph API (the row's own recheck target)
returned `429 Too Many Requests` twice; dblp returned an anti-bot HTML page. Crossref resolved
the DOI and returned the exact title, venue and page range, so the citation is real; the
abstract-level quantities the row states ("four … LLVM IR lifters; 252,063 executables") remain
**unchecked and uncheckable today** — `unverifiable`, explicitly not the fabrication class.

### 3.4 S136 / S147 — no-locator rows are now locatable

Both rows were class `no-locator` (the gate block named no source), so the hand-check consisted
of supplying the locator and locating the quote:

- S136: own-work file, quote at line 8, one occurrence, matching the row's recheck. Adoptable.
- S147: quote at line 41, one occurrence. Two caveats. (a) The row names sections that do not
  exist under those names; the real anchors are line 41 under `## State as of this writing` and
  `## Expected \`doctor\` output on this host`. (b) **Drift**: the round's frozen counting
  command pins `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, whose
  `package.json` reads `"version": "6.5.0"`, while the contract sentence the row quotes says
  `rea-agents@6.7.0`. The document is usable as an anchor for "what the host contract said on
  2026-10-23"; it is no longer a true statement of the package this round measures.

## 4. Secondary observations (advisory, no writes)

1. Every `used-by` target named by these five rows exists only as a proposal heading in
   `/home/vgpnk/Projects/shokuknow/lanes/kaidoku{/round4,/round5}/KNOWLEDGE-PROPOSED.md`;
   none exists under the lane's `corpus/knowledge/`. So `used-by` here means "proposed entry",
   and a reader must not read it as a landed file. Defect only if a row is treated as landed.
2. `HOST-CONTRACT.md` (S147) and this round's pinned package disagree on the REA version
   (6.7.0 vs 6.5.0). This seat did not change either; the L1 should not let an S147-shaped row
   carry "6.7.0" into a round-38 claim.
3. R37-CL3 asks for a `## Gate` block recording decisions. This seat's slice outcome is one
   clean reject (S150), one unverifiable (S117), three anchor-supplied (S113, S136, S147) — a
   ready-made `## Gate` input for the L1, including the refusal.
4. None of these five rows is cited by an admitted entry in the lane, which is why no append
   was attempted: quarantine disposition is not admission.

## 5. Evidence retained

- `artifacts/R38ExecQuarantine/quarantine-slice` — the 5-row slice (derived by the assignment's
  awk; identical to the pre-existing assimilation copy).
- `artifacts/R38ExecQuarantine/quarantine-verdicts.txt` — per-row verdict, anchors, exact
  counts, flip conditions, auxiliary observations.
- Hashes cited above are of live bodies fetched into this seat's scratch; the scratch is
  removed at hand-off, so the byte counts, sha256 values, HTTP codes and grep counts are
  reproduced verbatim in the two artifact files rather than referenced by scratch path.
- Lane status after the seat (`git status --porcelain`, read-only): only untracked
  `.ufo/waves/round-38/assimilation/`, `.ufo/waves/round-38/w1.ready`, `.ufo/waves/round-38/w1/`
  — the last two are wave scaffolding, and this seat's writes are confined to
  `.ufo/waves/round-38/w1/artifacts/R38ExecQuarantine/` plus this report.

## 6. Tooling, scratch, limits

- No tool installed, upgraded or removed (pacman paused host-wide; nothing needed `uv`/`npx`
  beyond the already-present `curl`, `python3`, `git`). No host service touched.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38ExecQuarantine` (fetched bodies only, all well
  under 1 MB); removed before hand-off.
- No VCS mutation, no subagents, no background jobs, no `agent://all` message.
- Limits: one fetch per live source (no stability sweep beyond the body size matching the
  round-35/36 captures for zenn and adb); the S117 body is unobtainable by design of the
  publisher, so that row stays open; three of the five rows carry no lint quote at all, so the
  hand-check used each row's registry anchor and its own recheck command — [INFERENCE] where a
  row's `teaches` prose outruns what its checkable command proves (S113's numeral, S117's
  abstract counts).
