# R45W1RevS150 — re-verification of the round-44 quarantine refusal (the round-45 assimilation gate)

Seat `R45W1RevS150`, leaf, lane `kaidoku-shokunin`, round 45 wave 1, 2026-10-28.
Read-only on the lane tree; every write is under
`.ufo/waves/round-45/w1/R45W1RevS150/` (this report, `artifacts/`, `helpers/`, `manifest.tsv`).
Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1RevS150` removed after the artifacts were copied.
No install, no VCS mutation, no commit.

**Verdict: AGREE with the round-44 refusal — five for five.** The staged register's S150 row is a
fabrication-class refuse and the quoted heading is byte-absent from every one of five independent
captures, from Zenn's own article API and from all six articles of the series the row claims to sit
in. S113/S136/S147 are present-with-caveat and S117 is unverifiable exactly as round 44 recorded.
The five-row slice is still byte-identical to rounds 43 and 44.

Two things in the round-44 record are wrong or insufficient and are reported here rather than
"fixed": its S147 caveat (b) has the pin comparison inverted (§4 F3), and both its page-hash
receipt and its "body sha256 is not stable" note describe a mechanism it did not identify — the
instability is a fixed-length per-response CSP nonce, which means a served-page sha256 **cannot**
be a durable receipt for this host at all (§4 F1/F2).

## 1. Provenance

| what | value | how |
|---|---|---|
| lane root | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` | prompt §Context |
| base | `149133d47aa7e90796f96047afe6d251a3e65b2c` | `plans/round-45-claims.md` |
| freeze | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | `git log --format=%H -1 -- plans/round-45-claims.md` |
| frozen file set at the freeze | `plans/round-45-claims.md`, `tools/round-45/{c1-counter.py,c2-counter.py,frozen-path-preflight.py,registry-scope.json}` | `git ls-tree -r --name-only f762b72 -- tools/round-45/ plans/round-45-claims.md` |
| lane HEAD while working | `faa875bc` | `git rev-parse HEAD` |
| frozen paths touched in `FREEZE..HEAD` | **0 commits** (`lines=0`) | C26 |
| staged register | 83,621 B, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, mtime 2026-10-24T08:37:00-03 | C01, C02 |

Read first, per the assignment: `plans/round-45-claims.md` (both predicates),
`corpus/lessons/round-44.md` `## Gate` (S150 / S113 / S136 / S147 / S117, and the
`## Routed defects` rows that point at them), `corpus/lessons/round-45.md` `## Gate`,
`.ufo/waves/round-44/w1/R44Quarantine.md` (§§2–4, 7), and the staged register row itself
(`…/absent-defect-register.md:82`):

```
| `kaidoku` | round5 | S150 | `payload-absent` | https://zenn.dev/yasu01/articles/7370bd5d414ec4 | `シンボルがない場合のヒント` | cited source, companion URLs and local artifacts were all checked; the quote is in none of them |
```

The lane registry is *not* the register: the staged ids live in the register's id space. There is
no lane `S150` row (C28: `rows=141 max=S141 s150_hits=0`), so this seat's S150 is the staged row
and nothing else.

## 2. Five-row verdict table — measured, not restated

`agree?` = does my live re-measurement support the round-44 verdict?

| staged row | round-44 verdict | what I measured 2026-10-28 | agree? |
|---|---|---|---|
| S150 | FABRICATION-CLASS (REFUSE) | HTTP 200, **174,088 B**, three fetches, three different sha256 (`c8f7d83c…`, `e88b1808…`, `5cba850e…`); quote **0** in raw / html-unescaped / NFKC; `ヒント` **0**; 8 real `<h2>`, none containing `ヒント`; **0** in the Zenn API `body_html` (39,937 chars) and **0** in the Zenn-authored TOC; **0** across all six series articles | **agree** |
| S113 | PRESENT (adoptable with anchor; count correction stands) | HTTP 200, **368,120 B** bare / **368,116 B** for the cited `?hl=en` form; `hreflang` unique **22** = 21 locales + `x-default` in **both** forms; narrow `[a-z-]*` pattern **18**; `tools/adb?hl=ja` = 1. The staged row is **locator-only** — it carries no quote and no count; the "17 locales" figure lives in the lane's own round-35 record and was corrected in round 36 (see F6) | **agree** (on the locale correction), with the attribution corrected |
| S117 | UNVERIFIABLE (not fabrication) | DOI **302** → `ieeexplore.ieee.org/document/9833799/` → **202, 0 bytes** (sha `e3b0c442…b855`); Crossref **200, 16,543 B**, sha `dbd9ee61…88593`, identical to round 44; title/container/issued match | **agree** |
| S136 | PRESENT (adopt-with-anchor) | lane locator 12,897 B, sha `26eeaf6f…26bf`, line 8 carries `2 of 24 verbs are`, count 1 — byte-identical to round 44 | **agree** |
| S147 | PRESENT (adopt-with-anchor; two caveats) | locator 3,386 B, sha `ab36b310…58fe`; line 41 `- REA release: \`rea-agents@6.7.0\`, skill v42, 207 tools.`; `207 tools` count 1; real headings at L39/L46 as stated | **agree on the anchor and caveat (a); caveat (b) is inverted — see F3** |

Slice identity (the gate's premise, re-derived from the register read-only):

```
awk -F'|' -v l='kaidoku' '$2 ~ l && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' <register>
→ 5 rows, sha256 7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a
diff vs round-43 artifact → exit 0, empty        (C04)
diff vs round-44 artifact → exit 0, empty        (C05)
```

So the r38 = r39 = r40 = r41 = r42 = r43 = r44 = r45 chain holds, and the register itself is
unchanged since 2026-10-24T08:37-03 (the same mtime and sha round 44 recorded).

## 3. S150 — five independent evidence routes, and a sixth that did not evaluate

| # | route | result | receipt |
|---|---|---|---|
| A | live `curl` of the cited URL, ×3 | 200 / 174,088 B each; three distinct sha256 | C06, C07 |
| B | the two archived captures (round-44, round-39), re-counted here | r44: 174,088 B, sha `17fedf14…c3f61`, quote 0; r39: 174,088 B, sha `5712fd9b…` masked `549dbd23…`, quote 0 | C12, C11 |
| C | **Zenn's article API** — the publisher's own `body_html` and the author-facing TOC | `body_html` 39,937 chars (7,833 letters), quote 0, `ヒント` 0; TOC = the real 8 `<h2>`; neither contains the quote | C13 |
| D | **the whole series the row places itself in** (all 6 articles, API bodies) | `quote+hint` total **0** across 第1回…第6回 | C14, C15 |
| E | escaped / normalised / transcription variants | `\uXXXX` forms absent, 0 escaped-CJK sequences, `bodyMarkdown` absent, NFKC identical, zero for `シンボルが無い場合のヒント`, `シンボルのない場合のヒント`, `場合のヒント`; `コツ` = 6 (the real tips heading) | C08, C10 |
| F | Wayback snapshot 20260727061433 | **not evaluable** — the 40,015 B capture contains no article body (`h2` 0, `llvm-objdump` 0, no `zenn` token). It is not evidence of absence and I do not use it as such | — |

Real heading outline (C09), which is what a re-anchor must target:

```
h2 (8): はじめに / 道具の準備 / 実例：小さなプログラムを逆アセンブルする / パターン認識のコツ /
        AArch64 で同じバイナリを読む / 読み進めるためのワークフロー / まとめ / シリーズを終えて
h3 (13): objdump, llvm-objdump, readelf / ソースコードと準備, Step 1–4 /
        関数の境界, 文字列参照, 分岐の構造, ライブラリ関数の特定 / Discussion
any heading containing ヒント: False
```

### 3.1 The row's other defects (carried, re-measured)

- **Part number is wrong.** The row's anchor line says "part 4 of a 6-part series". The cited
  article is **第6回** (`第6回` ×2 on the page, C14); `第4回` on that page is a *different*
  article (`3efeb9d6054eed`, "システムコールの裏側"). Round 39 recorded this; it is still true.
- **The second named anchor is also not a heading.** The row names `§「逆アセンブル」` and
  `§「シンボルがない場合のヒント」`; neither is in the heading set — `逆アセンブル` occurs 18×
  as body/title text but as no heading (round 36 recorded the same).
- **The row's substantive quote spans are real.** The two contiguous sentences the row actually
  quotes are byte-present: `GNU Binutils に含まれる逆アセンブラ。ほぼすべての Linux 環境に入っています。`
  and `strip されていても PLT のシンボルは残る場合があるので、ここが最初の手がかりになりました`
  each `body_html=1`, page=2 (C34). The fabrication is therefore **confined to the section
  anchor**, not to the row's teachable content — which is why "refuse the row, re-anchor and
  re-open" (round 35's flip) is the correct remedy and a blanket "the row is invented" would
  overstate it. Byte-present replacement anchors: `パターン認識のコツ` (body_html 1, page 4) or
  the title `実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む` (page 4).

### 3.2 Where the fabricated heading came from (mechanism, not motive)

The article title is `実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む`. On the
page `シンボルなし` occurs **4×** and every one is a copy of that title — `<title>`,
`og:title`, the `<h1>`, and the embedded `__NEXT_DATA__` title; in the API `body_html` it
occurs **0×**. The form the fabricator used, `シンボルがない`, occurs **0×** on the entire page
and **0×** in the body (C32, C34). So the invented span `シンボルがない場合のヒント` is a
paraphrase of the *title's* topic (`シンボルなし` → `シンボルがない`, plus a "tips" noun the body
never uses: `ヒント` = 0 in 7,833 letters) — and the paraphrase is exactly what makes a string
that is otherwise nowhere in the document look like it came from it. That is the signature of a **topic-derived heading** generated
from metadata rather than read from text — the reason the string looks plausible to a reviewer,
and the reason "it is a heading I would expect" is not evidence.

## 4. Calibration findings (the wave-1 payload)

**F1 — a served-page sha256 cannot be a durable receipt for this host.** Every response carries a
per-request CSP nonce echoed at **44** `nonce="…"` sites plus **1** `<noscript data-n-css="…">`
copy, each **44 characters** (C11, C36). The variable region is a fixed 1,980 bytes, so the
**byte count is stable by construction** (five captures, five times exactly 174,088) while the
**sha256 differs on every fetch** (`c8f7d83c…`, `e88b1808…`, `5cba850e…` in one minute). Masking
`nonce="…"` **and** `data-n-css="…"` makes the three same-day captures identical
(`masked_sha=379ac19f863d0171`), which is the reproducible form. Round 44's §7 note ("fetch-body
sha256 is not stable across fetches … dynamic markup/escape sequences") is correct but
under-specified: it is not escaping, and it will never stabilise.

*Corroboration and delta.* While this seat was working, another wave-1 seat landed
`R45-CL12` in `corpus/lessons/round-45.md`, reaching the same class independently for a
`github.com` page ("per-request nonce and request-id", two fetches 667 bytes apart). My measurement
adds three things that lesson does not yet carry: (a) the nonce is **fixed-length**, so the
**byte count is a false comfort** — identical 174,088 every time — (b) the reproducible form is
the **nonce-masked** hash, demonstrated identical across three fetches, and (c) on this host the
sha churn is *only* the nonce: the field-level diff shows the body is invariant (§F2). Together
those turn "an HTML digest is not identity" into "use a masked digest or a named content
counter", which is the actionable form.

**F2 — cross-round instability is not content drift either.** Field-level diff of the embedded
`__NEXT_DATA__` JSON between captures:

| pair | changed fields | values |
|---|---|---|
| r44 capture → r45 live (C31) | **1** | `.props.pageProps.topics[0].taggingsCount` 2780 → 2784 |
| r39 capture → r44 capture (C33) | **2** | `.buildId` `d0GeNpgx…` → `FaqphhRY…`; `.props.pageProps.topics[0].taggingsCount` 2766 → 2780 |

Between 2026-10-26 and 2026-10-28 the article body is unchanged; the only deltas are a Next.js
build id and a public tag-follower counter. A byte count is too coarse to see that, a raw sha is
too noisy to carry it, and a whole-page "occurrence count" would see the taggingsCount change.
The durable receipt is a **named content counter on a named field** (`body_html` from the API),
which is why route C, not route A, settles this row.

**F3 — round 44's S147 caveat (b) is inverted.** `R44Quarantine.md` §4 says the quoted
`rea-agents@6.7.0` "disagrees with the lane-pinned `rea-agents@6.5.0`". `PROVINCE.md:9` says the
lane's client pins — Devin, OMP, Kimi — are **6.7.0**, and `PROVINCE.md:12` says the **round
carrier runs** pin the superseded 6.5.0 (`tools/round-28/c1-heldout-naming.py:59` confirms the
carrier argv). So the document **agrees** with the lane's configured pins and disagrees only with
the carrier CLI pin. A caveat copied forward in this form would attach a false drift claim to an
adoptable row; the corrected form is "matches the client pins; the carrier runs pin 6.5.0".

**F4 — the staged-id namespace note understates the collisions.** Round 44 recorded only the lane
`S136` collision. Measured (C37): lane rows exist for `S113`, `S117`, `S136` (unrelated subjects —
unblob fixtures, unblob README, sasquatch releases API) and do **not** exist for `S147`, `S150`.
With the lane at `S141` and minting ~2 rows a round, `S147`/`S150` are future lane ids as well
[INFERENCE: projection from the observed 139→141 rate, not a measurement]. Consequence: a bare
`S150` in a lane file is ambiguous now (register vs lane) and contradictory soon. Every reference
should be written `staged S150` / `register S150`, and the 0–3-space id-collision guard must run at
append time, not at adoption-design time.

**F5 — line pointers into `corpus/SOURCES.md` are revision-scoped.** Round 44 cites the S117 lead
at `SOURCES.md:232`; it is at **:237** now, because rounds 44 and 45 appended four rows. Same
class as R44-CL9. A pointer into a growing table needs its revision stated or a quoted-string
locator, or it silently rots.

**F6 — S113: the "17 locales" claim is the lane's, not the staged row's; and the cited URL form is
not the bare form.** (a) *Attribution.* The register's kaidoku S113 row
(`absent-defect-register.md:315`) sits in the never-checked table (`| lane | round | id | cause |
locator |`), cause *the cited source could not be fetched, so no quote was checked*, locator
`https://developer.android.com/tools/adb?hl=en`. It states no quote and no count. "17 locales plus
`x-default`" is the **lane's own** round-35 Gate sentence (`corpus/lessons/round-35.md:21`),
already corrected to 21 + `x-default` in round 36 (`corpus/lessons/round-36.md:48`). Round 44's
compressed "S113's '17 locales' is really 21 + `x-default`" reads as a defect of the staged row;
it is a defect the lane fixed itself, and the register row carries no such claim. (b) *Form.* The
register cites `?hl=en`; round 44 measured the bare path. They are different resources:
**368,116 B** (cited) vs **368,120 B** (bare), differing in exactly one token — whether devsite
module id `116` is present in the `app_loader.js` id list — with an identical 22-entry `hreflang`
set and otherwise identical content (C38). The id appears and disappears in both directions
across captures (r44 bare: absent; r45 bare: present; r45 `?hl=en`: absent), so it is edge/build
variance, not growth, and the byte count is not a content measure here either. Two receipts this
seat produced differ by that token purely because of URL form (C16 vs C38); a receiver comparing
them would otherwise report a phantom change. Fetch the **cited** form and cite a content counter.

**F7 — the page-hash form is sound for static hosts; only nonce hosts break it.** Round 45's own
Gate cites page sha256 for its two sources. Re-fetched twice each: `https://git-scm.com/docs/git-status`
→ **byte-identical**, 99,934 B, sha `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`
— exactly the lesson's value; `https://git-scm.com/docs/git-diff-tree` → byte-identical, 256,810 B,
sha `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640` — exactly the lesson's value
(C39, C42). So those receipts are reproducible and F1 does not touch them: the defect is
host-specific (a per-response CSP nonce), not "page hashes are useless". That is what makes the
fix cheap — mask where the nonce exists, keep the digest where it does not.

Two method notes for whoever wires quote-lint to these rows. (i) Both S140 segments are
byte-present under **proper** text extraction (`<script>` removed, tags replaced by a *space*,
entities unescaped), with "This makes it" elided between them and marked by `…` (C41). (ii) The
S141 sentence is present, but the page writes spaces before the commas (`When --raw , --numstat ,
--name-only …`), so the lesson's comma-normalised form matches only under whitespace folding —
three characters that a byte-exact checker would flag. Neither is a fabrication; both are
strictness facts about the round's own source receipts.

**Method trap, recorded because it manufactures false verdicts.** C40 shows the naive extraction
(`re.sub(r'<[^>]+>','',html)`) reporting both S140 segments as **absent** — removing tags to the
empty string merges adjacent words, so a real quote reads as fabricated. This is the same failure
mode that would let a bad checker "confirm" a fabrication. It cannot explain the S150 result:
that row is refuted twice over by inputs with no tags at all — the Zenn API `body_html` (a JSON
string) and the one-token count `ヒント` = 0, which is immune to boundary merging (§3).

## 5. Assimilation-line audit (why the gate is still closed)

| check | result | receipt |
|---|---|---|
| staged subjects in `corpus/knowledge/` | **0 files** (grep exit 1) | C24 |
| staged-subject additions in `corpus/SOURCES.md` since the r44 close | **0 lines** (grep exit 1) | C35 |
| new `SOURCES.md` rows since the r44 close | exactly `S138`, `S139` (r44) and `S140`, `S141` (r45) — none a staged subject | C35 + diff |
| `.ufo/waves/round-45/assimilation/` | **absent** | C25 context |
| corpus/PROVINCE working tree | clean for `corpus/ PROVINCE.md` | C25 |
| commits touching `corpus/ PROVINCE.md` since the r44 close | 17, all lane r44/r45 record landings; none adds a staged row | C25 |

So round 45's `Assimilation: none` is supported by measurement, not by inheritance: the refusal
stands **and** nothing staged has slipped in while it stood. `considerthese/` is still absent in
this lane (round 44's finding; not re-run here — see §8).

## 6. Separability / freeze cross-checks

- The frozen round-45 instruments never read the staged register: `grep -rn
  'S150\|quarantine\|absent-defect\|shokuknow' tools/round-45/` → **no match** (C27). The
  assimilation line and both frozen predicates are disjoint, so a defect in one cannot move the
  other's score — the claims file's causal-separability sentence holds on this pair.
- No commit in `FREEZE..HEAD` touches a frozen path (C26, `lines=0`), including the post-freeze
  amendment `1f4b27f8`. The directory freeze's own arm (`--pathspec tools/round-45/`) was not
  re-scored here; other wave-1 seats own that score.
- Cited round-44 anchors resolve (C29): `round-44.md:18` (M44-2), `:63` (R44-CL1), `:88`
  (R44-CL10), `round-44-verifier-spotcheck.md:89` (restore-arm limit), `:166` (no registry rows).

## 7. Receipts

42 checks, `artifacts/receipts.tsv` (one row per check: id, exit, **full stdout sha256**, UTC
start/end, description, first stdout line, exact command). Captured stdout for each is
`artifacts/C<nn>.txt`; `.stderr.txt` exists only where a command wrote stderr. Exit semantics
used: 0 = ran and the condition held, 1 = the searched-for negative (`C24`, `C27`, `C35` all
exit 1 = zero matches), 2 = could-not-evaluate (**none**). No check returned 2, and nothing here
counts toward a C1/C2 target.

| id | exit | stdout sha256 (full) | UTC | check |
|---|---|---|---|---|
| C01 | 0 | `d277a02b6acdcfdafaaebe0fb5e7d459d803a55c50288240650b3e35424ace02` | 15:45:57Z | register sha256 `5afe1810…bad833` |
| C02 | 0 | `1635885f0f7b8d4ea959b1c92300d52ea9a1d5822b0692a9f6ab1fc1d03f94a3` | 15:45:57Z | register 83,621 B, mtime 2026-10-24T08:37-03 |
| C03 | 0 | `4b32d148bd91810f5ff908f8a90da6233ddeec49e77a1f7283ca12600927f216` | 15:45:57Z | slice re-derivation, sha `7383a90e…28e6a` |
| C04 | 0 | `1e00073b48fe3b36fc839da3b74b515bbecc9def677e059553835bb86bde8c55` | 15:45:57Z | diff vs r43 slice → `IDENTICAL` |
| C05 | 0 | `1e00073b48fe3b36fc839da3b74b515bbecc9def677e059553835bb86bde8c55` | 15:45:57Z | diff vs r44 slice → `IDENTICAL` |
| C06 | 0 | `2a51907bb419a694a287079044eacd36792bcf3281af8a52e880d998aa5494ea` | 15:45:57Z | S150 live: 200 / 174,088 B |
| C07 | 0 | `34ceb2a03b048c41f91369d4bd3c61967834d7835458c3ed62ff0f6213a879f1` | 15:45:58Z | two refetches, three distinct sha256 |
| C08 | 0 | `f9999bfa8c9f001fe10d59cc806dc8eed97b06142af3cf9c7d95ed5140056f0d` | 15:46:00Z | quote 0 raw/unesc/NFKC; `ヒント` 0; variants 0 |
| C09 | 0 | `6a01007927ae570dd8e94b30e753ba53675dae8770a0bdf5fb72b935b660deaa` | 15:46:00Z | 8 h2, 13 h3, none contains `ヒント` |
| C10 | 0 | `469d84e67c4dfa9c58b0522551ff5918eaa377fea3d9bdf59ba59e5ddc4f4544` | 15:46:00Z | no `\uXXXX` form, 0 escaped CJK |
| C11 | 0 | `0d3ffab3b97cefdbb47461bbb7b97c546ed14ae18416398150ca5bb9e9c3c81b` | 15:46:00Z | masked identity: same-day true, cross-round false |
| C12 | 0 | `ddb5ca4ab361781421356baecb7a585a3062c7c7e34a1481ebba5006d26e36a4` | 15:46:00Z | r44 capture `17fedf14…c3f61`, quote 0 |
| C13 | 0 | `425f158f6fde0f188ef028dcc225de13f473f5594c61dc6e9de6d88c89d9e909` | 15:46:00Z | API `body_html` + TOC: quote 0, `ヒント` 0 |
| C14 | 0 | `7ce7de6c40184d57fc76f1df238a73b0637313017f0724ca3ca79293a7b5f483` | 15:46:01Z | 6 series rows; `第6回` ×2; `llvm-objdump` 6 lines / 16 occ |
| C15 | 0 | `2a3d42ba43919b099a0db203639d9407c68388794848169dc192a7d7f30ec0c8` | 15:46:01Z | series sweep: quote+hint total **0** |
| C16 | 0 | `d4a2513fbc0f1816a52cd64af3642feb6c326b44cfda4d8f08ffe1013ad83b56` | 15:46:11Z | S113 200 / 368,120 B; 22 hreflang = 21 + x-default |
| C17 | 0 | `135baef50e3b70e00e182fcc658e62ff7c1b64fe61ea85fd47d93c626f11e443` | 15:46:12Z | S113 +4 B = devsite asset-id list |
| C18 | 0 | `9d5eb808815781f004a26571cff25d9821744d66313dae35ae92c1f72abe2d97` | 15:46:12Z | DOI 302 → ieeexplore |
| C19 | 0 | `41dce1b39349de4b9dbfb7fe4682b5e1c6806fa6f28bdfe41da0f02ba32e6bc3` | 15:46:12Z | publisher 202, 0 B, `e3b0c442…b855` |
| C20 | 0 | `95f30fe2f44c349ead8eb4563f69d39e19edc635d0cf37e861145da814a1d3ee` | 15:46:12Z | Crossref 200 / 16,543 B, `dbd9ee61…88593` |
| C21 | 0 | `ca3750634c19cabceb6daab0cd43957ebbc0412e805362997f4e1a2890039a24` | 15:46:12Z | S136 locator + line 8 quote |
| C22 | 0 | `f89cc35820f29ad8ca5eed248046e6e806e1619b0345a0b022cb0c738ae4e1ac` | 15:46:12Z | S147 locator + line 41 + headings |
| C23 | 0 | `e455fa1dc51804fd452e709efea203061756d72315e51b792c44396827ddba79` | 15:46:12Z | PROVINCE pins: 6.7.0 client, 6.5.0 carrier |
| C24 | 0 | `ca0f7afbf703dbe007eee4d7dd506129c01fb33ab345c9a10d262b0e7cbf2ad1` | 15:46:12Z | knowledge grep → `grep_exit=1` (0 files) |
| C25 | 0 | `90322bbbaa29c7dd13a23e94dfd0356be07e34c6ceb86b8d09279ed895f33ee7` | 15:46:12Z | 17 corpus commits since r44; tree clean |
| C26 | 0 | `1d6fd9a10f66b5e08cd5bdabac14aaeecb192ae6a2900201af53f016d297f085` | 15:46:12Z | frozen-path touches `lines=0` |
| C27 | 0 | `ca0f7afbf703dbe007eee4d7dd506129c01fb33ab345c9a10d262b0e7cbf2ad1` | 15:46:12Z | instruments never read the register |
| C28 | 0 | `5fe1856fecbfce4eab3da15f390794e66c6a7ea413f987742c61ebfe090b4c7f` | 15:46:12Z | lane `rows=141 max=S141 s150_hits=0` |
| C29 | 0 | `8805dffced9ccd7ab07a46fc8c76e7a4aa4c0941e9befe3af6870b63ea2af701` | 15:46:12Z | 5 cited round-44 lines resolve |
| C30 | 0 | `02b284b7769c08a7d4349522abde6d40b48fdbebdd51030cc5933eda95667059` | 15:46:12Z | r44 5-row verdict table re-read |
| C31 | 0 | `e411073bbedd8d20618b12f0e408d9639ba572d68a9d857556c11ea92e2d8adc` | 15:46:32Z | r44→r45: 1 field (`taggingsCount`) |
| C32 | 0 | `947c8dffddb0dd0aaf1f4d89ac65643de7a943178aa73517f3ede1ed5623a1f5` | 15:46:32Z | title carries `シンボルなし`; body carries neither |
| C33 | 0 | `503aa9ebe9a7d8943b86ffa862bc9f35a54e6b2a5593f169fbc67791c1b1031b` | 15:46:39Z | r39→r44: 2 fields (`buildId`, `taggingsCount`) |
| C34 | 0 | `fad339c94c5b6c2e831f668def5187f09c89dae502615f95b4f5a2abdab28c59` | 15:46:53Z | both substantive quote spans present |
| C35 | 1 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 15:47:41Z | 0 staged-subject additions in SOURCES (empty output) |
| C36 | 0 | `2aed24d33d03fd74b6d48df72a27072540d93a0041a85adea438c63a48ba6365` | 15:47:41Z | 44 nonce sites @44 chars + 1 data-n-css |
| C37 | 0 | `3129e5574d9fbec1f6891588e5628bb0372fb6191d0e38c3a0d9e993456136ee` | 15:47:41Z | lane rows for S113/S117/S136; none for S147/S150 |
| C38 | 0 | `4f32e4e08e172d0e0ad2607f7385b69b0c176129245f5951c97283b566721be1` | 15:50:35Z | cited `?hl=en` vs bare URL: 1 token (devsite id `116`), same 22 hreflang |
| C39 | 0 | `6e9915e893de1cb8432c95ad7623234b3446c2220abf4299f6776eef06301e79` | 15:51:59Z | git-status ×2 byte-identical, sha = the lesson's cited value |
| C40 | 0 | `91825a506f21fd727974b195f900fabc571213c32e0288f966239bcfc1de038f` | 15:51:59Z | naive tag-strip undercounts S140's segments (method trap) |
| C41 | 0 | `1aaba6918ad9f1fb27a910aa70490aca8b7d936dcfe3f8d9b7f32fe7aaa87fe3` | 15:51:59Z | proper extraction: both S140 segments + the S141 segment present |
| C42 | 0 | `7563876bcb40159fca362d4bb919c6f3965abdba3cf834e7a656bee67e5bc194` | 15:51:59Z | git-diff-tree ×2 byte-identical, sha = the lesson's cited value |

(C35's empty output is the finding — the sha is the sha256 of the empty string, and `C35.txt` is
0 bytes. C36/C37 shas are transcribed from `artifacts/receipts.tsv`; that file is the authority if
this table and it ever disagree.)

## 8. Residual risk and what I did not run

- **Zenn's article revision history is not public.** `body_updated_at` is 2026-06-04T03:18+09; the
  row was authored later in the campaign (round 5, after the 2026-10-19 lane base), so the body
  the row quotes did not contain the heading *at authoring time* — but I cannot inspect a
  pre-2026-06-04 revision. The only Wayback snapshot (20260727061433) carries no body and was not
  used as evidence of absence. If a revision ever held that heading, the class would become
  "drifted", not "fabricated"; nothing observed supports that, and the 2026-06-04 date predates
  every round that checked the row.
- **S117's abstract-level quantities stay unchecked** ("four LLVM IR lifters; 252,063
  executables"). Publisher body is 0 bytes; verdict remains identity-only, as in rounds 38–44.
- **`considerthese/` was not re-run** this seat (round 44 found it absent lane-wide and in the
  sibling campaign root). Inherited, not measured here.
- **A concurrent non-author write was observed and not caused by this seat.**
  `git status --porcelain` at 15:54Z showed ` M corpus/lessons/round-45.md`
  (mtime 2026-10-28T15:49:02Z, +55/−6 lines, adding routed defects `R45-CL6`…`R45-CL12`
  attributed to other wave-1 seats). I read that file at 15:39Z and never wrote it; its
  `## Gate` S150 sentence and its `Assimilation: none` bullet are **not** inside the diff
  hunks, so the quotes in this report still hold. The path is not frozen, so the freeze arm is
  unaffected — but this is the M45-1 shape (a file in the lane tree changing under a reader)
  occurring while the round's own record was being written, and it is worth the L1's eye.
- **Not run:** the frozen counters (`c1-counter.py`, `c2-counter.py`), `frozen-path-preflight.py`
  — other wave-1 seats own those scores; no C1/C2 value appears in this report. No REA/unblob run.
  No install (nothing needed installing; therefore no install record).
- **Scope of the series sweep:** the six articles the page itself links. The author's other
  articles were not enumerated — absence across the cited series is what the row's own framing
  makes relevant.
- **C31–C42 were appended outside the driver** (which writes C01–C30); their rows carry the exact
  command text in `receipts.tsv` and their captured stdout files are beside it, but they were not
  re-executed under the driver's capture wrapper.

## 9. What the L1 can land from this

1. The refusal is **re-affirmed with stronger evidence than round 44 had**: cite the Zenn API
   `body_html` + TOC (route C) and the six-article series sweep (route D), not the page byte
   count. A page-only check cannot distinguish fabrication from drift; routes C and D can, and
   both are cheap.
2. Write the gate's S150 as **`staged S150`** and keep the register id out of lane id space (F4).
3. If S147 is ever adopted, **replace caveat (b)** with the measured form (F3).
4. Any future receipt that cites a served-page sha256 for `zenn.dev` should cite the
   **nonce-masked** sha or, better, a named content counter (F1/F2). The form is *not* generally
   broken: S140/S141's `git-scm.com` page digests reproduce exactly (F7, C39/C42), so this is a
   per-host caveat, not a reason to distrust the round's own source receipts.
5. If quote-lint is wired to the round's Gate rows, fold whitespace for S141 (`--raw ,` in the
   served page) and allow the `…` elision in S140 — and never strip tags to the empty string,
   which turns both S140 segments into false "absent" verdicts (C40/F7).
6. Round 35's flip is still executable and now has byte-present anchors: re-anchor the row to
   `パターン認識のコツ` (or the title) and re-open; the row's two substantive quotes are real
   (C34), so the fabrication is the anchor, not the content.

## 10. Axes touched

- **Calibration** — the primary gain: five corrections to what this lane's records can claim —
  F1 (page-sha non-reproducibility, with the nonce mechanism and the masked-hash fix), F3 (the
  inverted S147 caveat), F4 (the id namespace), F6 (an attribution error: "17 locales" is the
  lane's own round-35 sentence, not a claim of the staged row, and the cited `?hl=en` form is a
  different resource from the bare path), F7 (the page-hash form is sound on static hosts, so the
  caveat is per-host) — each with a receipt.
- **Depth** — the S150 verdict moves from "the heading is not on the page" to a five-route
  demonstration with a mechanism and a scoped remedy (anchor fabricated, content real).
- **Coverage** — unchanged; this seat adds no domain surface.

Artifacts: `.ufo/waves/round-45/w1/R45W1RevS150/` — `report.md`, `manifest.tsv` (sha256 + bytes per
artifact), `artifacts/` (42 captured stdout files + `receipts.tsv` + the six raw captures:
`s150-live.html`, `s150-refetch-1.html`, `zenn-api.json`, `api-<id>.json` ×6, `s113-adb.html`,
`s117-crossref.json`, `s117-ieee.html` (0 B), `s113-hlen.html`, `series-rows.json`, `doi-head.txt`),
`helpers/` (`driver.py` plus 14 probe scripts, so every number above is re-derivable).
