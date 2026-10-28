# R44Quarantine — round 44 wave 1, quarantine slice re-derivation, 5-row hand-check, adoption audit

**Verdict: CONFIRMED** — the kaidoku-package quarantine slice re-derived from the staged register
this round is **byte-identical** to the round-43 committed slice (5 rows, sha256
`7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a`), the staged register is
unchanged since round 43 (sha256 `5afe1810…bad833`, mtime 2026-10-24), and **no staged row has
been adopted into the lane corpus since round 43**: zero commits touching `corpus/` in
`c29360e3..HEAD`, clean `git status`, and zero occurrences of every staged subject in
`corpus/knowledge/`. A live re-open of all five sources on 2026-10-28 reproduces the five standing
verdicts: **1 fabrication-class refuse (S150), 3 present-with-anchor (S113 count-corrected, S136,
S147), 1 unverifiable-not-fabrication (S117)**. Nothing is appended from the slice.

Seat `R44Quarantine`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base
`c29360e3ba5381a5ab69e372d0d9577970f85018`; lane HEAD at work `fc5eb54a` (round-44 draft claims,
`plans/` only). Lane writes: this report and `artifacts/R44Quarantine/` only. No corpus/C1/C2/tool
file, no register, no VCS mutation, no install.

## 1. Inputs read

- DRAFT claims `plans/round-44-claims.md` (fresh-start posture; `## Separability`; the §10
  assimilation line at `plans/round-44-claims.md:193-196`).
- Staged register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
  (read-only; 83,621 B, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833` —
  unchanged from round 43's recorded hash and from round 38's).
- Round-43 slice artifacts `.ufo/waves/round-43/w1/artifacts/R43Quarantine/{quarantine-slice,
  quarantine-slice.sha256,quarantine-verdicts.tsv,fetch-receipts.tsv}` and report
  `.ufo/waves/round-43/w1/R43Quarantine.md`.
- Lesson `corpus/lessons/round-43.md` `### Admission and rejection` (line 25 records the S150
  reject and the S113/S136/S147/S117 dispositions).
- Round-44 assimilation state: `.ufo/waves/round-44/assimilation/` — **empty** (0 entries);
  `.ufo/quarantine/` — **absent**.

## 2. Slice re-derivation and byte comparison

Command (register read-only; same adapted form round 38 recorded and round 43 used):

```
awk -F'|' -v l='kaidoku' '$2 ~ l && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Output (artifact `quarantine-slice`), 5 lines, every line S-id-bearing:

```
 S150   `payload-absent`
 S113`   the cited source could not be fetched, so no quote was checked
 S117`   the cited source could not be fetched, so no quote was checked
 S136`   the gate block named no locator, so no quote was checked
 S147`   the gate block named no locator, so no quote was checked
```

```
sha256sum quarantine-slice
7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a  quarantine-slice
diff quarantine-slice .ufo/waves/round-43/w1/artifacts/R43Quarantine/quarantine-slice   # exit 0, empty
```

Byte-identical to round 43 and to its stored `.sha256`. The chain r38 = r39 = r40 = r41 = r42 =
r43 = r44 holds. Carried notes, re-verified: (a) the four never-checked ids carry a stray trailing
backtick in `$4` because that register table has one fewer column — ids unambiguous; (b) the
register's per-lane totals row for kaidoku is `1` (payload-absent), agreeing with the slice's one
fabrication-class row plus four never-checked rows.

## 3. Adoption audit since round 43 (git log + ls)

| check | command | result |
|---|---|---|
| commits touching corpus since r43 close | `git log --oneline c29360e3..HEAD -- corpus/ PROVINCE.md` | **empty** (`fc5eb54a` is `plans/` only) — Q04 |
| working tree | `git status --porcelain -- corpus/ PROVINCE.md SCORECARD.md SHONEN.md` | only `?? corpus/evidence/round-44/` — a **sibling C1 seat's** pre-freeze oracle trees (23 files under `oracle/squashfs_v{1,2}/{little,big}_endian` + `manifest.json`), not an adoption — Q05 |
| newest knowledge entries | `ls -t corpus/knowledge/*.md` | 2026-10-27 `r43-sqfs-triage-v4-scored` and `sasquatch-release-matrix`; **no 2026-10-28 file** (137 `*.md` total) — Q07 |
| knowledge additions (last 20) | `git log --diff-filter=A --name-only -20 -- corpus/knowledge/` | last additions are the two 2026-10-27 round-43 entries — Q11 |
| staged subjects in `corpus/knowledge/` | `grep -rlE '7370bd5d414ec4\|9833799\|developer\.android\.com/tools/adb\|207 tools\|hreflang' corpus/knowledge/` | **0 files**, exit 1 — Q06 |
| staged subjects in SOURCES/PROVINCE/SCORECARD/SHONEN/README | same pattern plus `HOST-CONTRACT` | 2 hits, both **not adoptions** (below) — Q12 |
| staged register identity | `sha256sum absent-defect-register.md` | `5afe1810…bad833`, unchanged — Q03 |

The two `corpus/SOURCES.md` / `PROVINCE.md` hits are **not** adoption of a staged row, and are
recorded so they are not mistaken for one:

- `corpus/SOURCES.md:232` — the staged S117 identifier (DOI `10.1109/SP46214.2022.9833799`) appears
  under `## Leads (unopened)`, not in the SOURCES row table: "*only Crossref metadata was returned;
  the primary paper and an anchorable quote remain unopened.*" `git blame` = `5ac78607`,
  2026-10-19, i.e. **before** the staged register existed. It is an unopened lead and states the
  unverifiable status; it is not the staged row admitted.
- `PROVINCE.md:24` — "Installed shared REA skill is v42/207 tools" is the lane's own independent
  host measurement, not a citation of the staged S147 document (no `HOST-CONTRACT` reference
  anywhere in the lane). S147's subject is the host contract file; S147 itself is not cited.

## 4. Verdict table (live re-open 2026-10-28)

`status` = re-derived class; `adopted?` = is this staged row now present in the lane corpus.

| row | status | adopted? |
|---|---|---|
| S150 | FABRICATION-CLASS (REFUSE) | no |
| S113 | PRESENT (adoptable with anchor; count correction stands) | no |
| S117 | UNVERIFIABLE (not fabrication) | no (unopened lead at `SOURCES.md:232`, not a SOURCES row) |
| S136 | PRESENT (adopt-with-anchor) | no |
| S147 | PRESENT (adopt-with-anchor; two standing caveats) | no |

### S150 (round5, `payload-absent`) → FABRICATION-CLASS (REFUSE)

`curl -sSL` → **HTTP 200, 174,088 B**, sha256 `17fedf14…c3f61` (artifact `s150-zenn.html`). On the
html-unescaped body: `シンボルがない場合のヒント` = **0**, `ヒント` = **0**, `シンボルがない` = **0**.
The real `<h2>` set is はじめに / 道具の準備 / 実例：小さなプログラムを逆アセンブルする /
パターン認識のコツ / AArch64 で同じバイナリを読む / 読み進めるためのワークフロー / まとめ /
シリーズを終えて — the quoted heading is in none of them, and the register row's own note says
"the quote is in none of them". Row recheck: `grep -c llvm-objdump` = **6** (matches the r43
reading; note `grep -o | wc -l` = 16 **occurrences** — line count vs occurrence count differ and
the register/r43 recheck is the line count). **Verdict: FABRICATION-CLASS, stays refused.**

### S113 (round1, fetch-failed prose class cell) → PRESENT (adoptable with anchor)

`curl -sSL` → **HTTP 200, 368,116 B**, sha256 `ee2ce264…51c835` (artifact `s113-adb.html`).
Honest drift note: round-43 measured 368,063 B; this fetch is **+53 B**, and every content counter
is unchanged — `hreflang="[^"]*"` unique = **22** = 21 locales + `x-default` (`ar bn de en es-419
fa fr he hi id it ja ko pl pt-BR ru th tr vi zh-Hans zh-Hant`), the narrow `[a-z-]*` pattern
undercounts at 18 because of `es-419`/`pt-BR`/`zh-Hans`/`zh-Hant`, and `tools/adb?hl=ja` = 1. The
row's "served in 17 locales" remains **not reproducible**; the correct statement is 21 locales +
`x-default`. **Verdict: PRESENT, adoptable later with anchor and the re-stated count.**

### S117 (round1, fetch-failed prose class cell) → UNVERIFIABLE (not fabrication)

`https://doi.org/10.1109/SP46214.2022.9833799` → **302** →
`https://ieeexplore.ieee.org/document/9833799/` → **HTTP 202, 0-byte body**
(`e3b0c442…b855`), byte-for-byte the r43 result. Crossref
`https://api.crossref.org/works/10.1109/SP46214.2022.9833799` → **HTTP 200**, 16,543 B, sha256
`dbd9ee61…88593` (identical to r43): title "SoK: Demystifying Binary Lifters Through the Lens of
Downstream Applications", container "2022 IEEE Symposium on Security and Privacy (SP)",
published 2022-05. The citation is real; the publisher serves nothing fetchable. **Verdict:
UNVERIFIABLE** — unreachable is not fabrication; abstract-level quantities stay unchecked.

### S136 (round4, no-locator) → PRESENT (adopt-with-anchor)

Locator `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md` — **12,897 B**, sha256
`26eeaf6f…26bf` (both unchanged). Quote `2 of 24 verbs are` = **1**, line **8**. **Verdict:
PRESENT.** Namespace note (carried): the lane registry also carries a **lane** S136
(`2026-10-27-sasquatch-release-matrix.md`, sasquatch release API) — different subject,
names-only collision.

### S147 (round5, no-locator) → PRESENT (adopt-with-anchor; two caveats)

Locator `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` — **3,386 B**, sha256
`ab36b310…58fe` (unchanged). Line **41** `- REA release: \`rea-agents@6.7.0\`, skill v42, 207
tools.` — `207 tools` = 1. Caveats unchanged: (a) the row names headings that do not exist; the
real anchors are `## State as of this writing` (L39) and `## Expected \`doctor\` output on this
host` (L46); (b) drift — the quoted `rea-agents@6.7.0` disagrees with the lane-pinned
`rea-agents@6.5.0`. The document is an anchor for what the host contract said on 2026-10-23, not a
statement of the package this round measures.

## 5. Assimilation

Assimilation: none

No staged entry exists for round 44 (`.ufo/waves/round-44/assimilation/` empty), the five
quarantine rows are cited by no admitted or staged entry, and all five carry `adopted? = no`
above. The slice therefore adds nothing to the corpus this round.

`considerthese/`: **absent** — `find` over the lane and the sibling campaign root
(`/home/vgpnk/Projects/shokuknow`, depth 4) returns no `considerthese*` entry (Q08, empty).

## 6. Receipts

All receipts carry seat `R44Quarantine`, the exact command, exit code, sha256 of captured stdout,
and wall time. `q`-series = structure/adoption checks (`checks-receipts.tsv`), `Q13..Q23` = live
re-open checks (`fetch-receipts.tsv`). Both are artifacts.

| id | exit | stdout sha256 (first 16) | wall | check |
|---|---|---|---|---|
| Q01 | 0 | `7383a90e7c04c723` | 1 ms | slice re-derivation (5 rows; file sha256 `7383a90e…28e6a`) |
| Q02 | 0 | `e3b0c44298fc1c14` | 1 ms | diff vs round-43 slice (empty output = byte-identical) |
| Q03 | 0 | `d277a02b6acdcfda` | 1 ms | `sha256sum` staged register (`5afe1810…bad833`) |
| Q04 | 0 | `e3b0c44298fc1c14` | 1 ms | `git log c29360e3..HEAD -- corpus/ PROVINCE.md` (empty) |
| Q05 | 0 | `e3c057e989115f0b` | 11 ms | `git status --porcelain` (only untracked `corpus/evidence/round-44/`) |
| Q06 | 1 | `e3b0c44298fc1c14` | 3 ms | staged-subject grep in `corpus/knowledge/` (exit 1 = 0 files) |
| Q07 | 0 | `1f53039da78fa65e` | 2 ms | `ls -t corpus/knowledge/*.md` (newest 2026-10-27) |
| Q08 | 0 | `e3b0c44298fc1c14` | 7 ms | `find … -name 'considerthese*'` (empty) |
| Q09 | 0 | `f1c044df0eb899fa` | 2 ms | `ls -la .ufo/waves/round-44/assimilation` (empty) |
| Q10 | 1 | `e3b0c44298fc1c14` | 0 ms | `test -d .ufo/quarantine` (absent) |
| Q11 | 0 | `654adb4698a11d65` | 3 ms | knowledge-additions log (last = 2026-10-27) |
| Q12 | 0 | `5a435c6a3976426b` | 2 ms | staged-subject grep in SOURCES/PROVINCE/SCORECARD/SHONEN/README (2 non-adoption hits) |
| Q13 | 0 | `d6375201ce3518ef` | 626 ms | `curl -sSL -o s150.html -w http/bytes/url` → `http=200 bytes=174088` |
| Q14 | 0 | `db4ee0e7106e2fcb` | 13 ms | S150 quote counters (`0/0/0`; occurrences `llvm-objdump`) |
| Q15 | 0 | `662e57423d6195a9` | 13 ms | S150 `<h2>` heading texts |
| Q16 | 0 | `38aa863e4c076898` | 925 ms | `curl -sSL -o s113.html` → `http=200 bytes=368116` |
| Q17 | 0 | `5a20b6496876b8ee` | 5 ms | hreflang census (`unique=22 narrow=18 hlja=1`) |
| Q18 | 0 | `cb0b0556f9e2e3ce` | 338 ms | DOI chain → `302` → `202`, 0 B |
| Q19 | 0 | `ed8f86316dbae733` | 718 ms | Crossref identity (200, 16543 B) |
| Q20 | 0 | `0101b8d43daea102` | 3 ms | S136 locator size/sha |
| Q21 | 0 | `c35439f8f8f566bb` | 1 ms | S136 quote at line 8 |
| Q22 | 0 | `560aaa39b2c7ee4f` | 3 ms | S147 locator size/sha |
| Q23 | 0 | `2adf40f78e4c78ea` | 2 ms | S147 quote at line 41 + real headings |

Exit-code semantics: 0 = check ran and its condition held/clean output; 1 = the searched-for
negative (`Q06` zero staged subjects in knowledge, `Q10` no quarantine dir). No check returned 2
(could-not-evaluate); nothing here counts toward a C1/C2 target.

## 7. Limits

- Fetch-body sha256 is **not stable across fetches** for S150 and S113 (dynamic markup/escape
  sequences): two S150 fetches minutes apart gave `ea6721ec…` and `17fedf14…` at identical
  174,088 B. The durable evidence is the content counters and the per-fetch captures stored as
  artifacts, not a single sha.
- S113 grew 368,063 → 368,116 B since round 43 (+53 B) with every content counter unchanged; the
  `17 locales` under-count in the staged row is the only substantive defect and it is not repaired
  here (no adoption by this seat).
- S117's abstract-level quantities ("four … LLVM IR lifters; 252,063 executables") remain
  unchecked — the publisher body is empty; the verdict is identity-only, as in rounds 38–43.
- The adoption audit reads `corpus/knowledge/` at HEAD plus the working tree; the untracked
  `corpus/evidence/round-44/` belongs to a sibling C1 seat and was inspected read-only (no staged
  identifier present) and otherwise left untouched.
- Nothing was adopted into any corpus file by this seat; adoption is the L1's call.
- No REA/unblob/squashfs run, no `tools/round-44/c1-run.sh`, no install, no VCS mutation, no
  shokuknow write. Scratch `/fast/scratch/hyaku/kaidoku-r44/w1-R44Quarantine` holds the raw
  outputs and both receipt TSVs.

Artifacts: `.ufo/waves/round-44/w1/artifacts/R44Quarantine/` — `quarantine-slice` (+ `.sha256`),
`quarantine-verdicts.tsv`, `checks-receipts.tsv`, `fetch-receipts.tsv`, `adoption-git-log-since-r43.txt`,
`adoption-git-status.txt`, `adoption-staged-subject-grep-knowledge.txt`,
`adoption-staged-subject-grep-sources.txt`, `knowledge-additions-log.txt`, `s150-zenn.html`
(174,088 B), `s150-quote-counters.txt`, `s150-h2-headings.txt`, `s113-adb.html` (368,116 B),
`s113-hreflang-census.txt`, `s117-doi-chain.txt`, `s117-crossref.json`.
