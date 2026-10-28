# R45W1SrcGitStatus — S140 opened, verified, row + Gate block cut

Seat: `R45W1SrcGitStatus` (leaf, no dispatch). Round 45, wave 1, lane `kaidoku-shokunin`.
Scope of this seat: open SOURCES candidate **S140** (`https://git-scm.com/docs/git-status`) live,
locate the two required passages, record a ≤25-word located quote, cut the 11-column registry row
and its 3-line Gate block, and prove the quote byte-present on the saved copy.

Read-only on the lane tree; all writes land in
`.ufo/waves/round-45/w1/R45W1SrcGitStatus/`. No commit, no stage, no mutating git, no sibling lane,
no `.ufo/state/`. No tool installed or updated (nothing was needed).

## 1. Behaviour — what was done and observed

Fetched the page twice from the live origin, independently:

| attempt | UTC | HTTP | bytes | sha256 | note |
|---|---|---|---|---|---|
| 1 | `2026-10-28T15:38:50Z` | 200 | 99934 | `903e31c5…59ad9` | saved to scratch |
| 2 | `2026-10-28T15:41:04Z` | 200 | 99934 | `903e31c5…59ad9` | `cmp` exit 0, identical to attempt 1 |

Full sha256 `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`.
Response headers (`receipt-headers.txt`): `HTTP/2 200`, `content-type: text/html; charset=utf-8`,
`server: cloudflare`, `via: 1.1 varnish`, `last-modified: Mon, 26 Oct 2026 14:52:03 GMT`,
`etag: W/"6adf6913-1865e"`. The etag's hex length field `0x1865e` = **99934**, matching the
byte count — an independent consistency check that the saved bytes are the served entity.

**Both passages located** (HTML `<p>` indices from `receipt-quote-presence.txt`):

- **Porcelain Format Version 1** — `id="_porcelain_format_version_1"` at raw byte offset **76125**,
  paragraph index **62**. The paragraph states the guarantee *and* the script-parsing rationale:
  "Version 1 porcelain format is similar to the short format, but is guaranteed not to change in a
  backwards-incompatible way between Git versions or based on user configuration. This makes it
  ideal for parsing by scripts. …"
- **`-z` machine parsing** — same section, paragraph index **65**: "There is also an alternate -z
  format recommended for machine parsing.… Second, a NUL (ASCII 0) follows each filename, replacing
  space as a field separator and the terminating newline …". Corroborated by the dedicated
  section `id="_pathname_format_notes_and_z"` at offset **90511** (paragraph 102): "… lines are
  terminated with a NUL (ASCII 0x00) byte."

**Located quote recorded (≤25 words).** 24 words, verbatim-contiguous:

> "guaranteed not to change in a backwards-incompatible way between Git versions or based on user
> configuration. This makes it ideal for parsing by scripts."

Byte-presence verification (receipt exit 0, `RESULT: PASS`): this span occurs **once** in the
saved page's whitespace-collapsed raw HTML (`raw_html_whitespace_collapsed_hits=1`) and once in
the extracted text. Quote sha256 `d1d0a42a48373f4f8ee9a9a237c33b3b5b4840c422cf4d51054274b4fa1daaa9`.

Honest caveat: the two `-z` quotes (11 and 18 words) are verbatim in the **rendered text** but not
raw-HTML contiguous, because the page wraps `-z` in `<code>` and `NUL` in `<em>`. The receipt prints
both metrics per quote rather than only the favourable one.

## 2. Row and Gate block (ready to land)

Row, 11 columns, validated: `columns 11`, no empty cell, `used-by` exactly
`corpus/lessons/round-45.md`. File: `row.md` (sha256 `cbce9a9ceed2d38d5f0b0e5a75545f99506e298537958bae155ccee216fe9fad`).

| S140 | git-status documentation — https://git-scm.com/docs/git-status | docs | A | Git's Version 1 porcelain status format and its `-z` variant — the form a gate parses to read worktree state; not porcelain v2, not diff/diff-tree output (S141), not the 44 prose mentions in `corpus/**.md` nor the 10 older tool call sites that run `--porcelain` without `-z` | anchors `#_porcelain_format_version_1` (HTML byte offset 76125) and `#_pathname_format_notes_and_z` (90511); page fetched 2026-10-28T15:41:04Z, HTTP 200, 99,934 B, sha256 `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`; quoted paragraphs are `<p>` index 62 (v1 stability) and 65 (`-z` machine parsing) | The v1 porcelain format is guaranteed not to change backwards-incompatibly between Git versions or based on user configuration and is ideal for parsing by scripts; `-z` is recommended for machine parsing, ends each filename with NUL (ASCII 0), reverses rename pairs to `to` then `from`, and quotes nothing — which is exactly what the dirty arm reads (`tools/round-45/frozen-path-preflight.py:137`). | mined | 2026-10-28 | on-release | corpus/lessons/round-45.md |

Gate block, exactly three lines:

```
URL: https://git-scm.com/docs/git-status
Accessed: 2026-10-28T15:41:04Z — HTTP 200, 99934 bytes, sha256 903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9
Quote: "guaranteed not to change in a backwards-incompatible way between Git versions or based on user configuration. This makes it ideal for parsing by scripts." (anchor #_porcelain_format_version_1, 24 words)
```

## 3. Gates run (exact command, exit, receipt)

| gate | command | exit | receipt |
|---|---|---|---|
| fetch | `curl -sS -o page2.html -w 'http_code=… size_download=…' -L -A 'Mozilla/5.0 …' https://git-scm.com/docs/git-status && sha256sum page2.html && wc -c page2.html && cmp page2.html git-status.html` | 0 | `receipt-fetch.txt` |
| headers | `curl -sSI … https://git-scm.com/docs/git-status \| tr -d '\r' \| grep -iE '^(HTTP/\|server\|…\|etag\|…)'` | 0 | `receipt-headers.txt` |
| quote presence | `python3 - "$PWD/git-status.html"` — per-`<p>` text extraction + whitespace-collapsed raw-HTML count per quote; exit 1 if any quote is not in exactly one paragraph | 0 (`PASS`, 4/4) | `receipt-quote-presence.txt` |
| row schema | `awk -F'\|' '/^\| S140 /{print NF-2}' corpus/SOURCES.md` (landed row) + header at `corpus/SOURCES.md:5` | 0, `11 columns` | `receipt-schema.txt` |
| v1 semantics | git 2.56.0 fixture under `$TMPDIR`, `git -C "$D"` only, `rev-parse --show-toplevel` = `$D` before the commit | 0 | `receipt-v1-semantics.txt` |
| instrument binding | `sed -n '25,35p'` + `awk 'NR>=133&&NR<=141'` on `tools/round-45/frozen-path-preflight.py`; `grep -rn -- '--porcelain' tools/round-45/` | 0 | `receipt-instrument-binding.txt` |

Every receipt carries command, cwd, `utc_start`/`utc_end`, exit, `stdout_bytes`, `stdout_sha256`.

**Semantics check — the page's claims, observed on git 2.56.0** (`receipt-v1-semantics.txt`):
`-z` gave 72 B / 5 NUL / 0 LF; rename printed `R  renamed.txt\0plain.txt\0` while non-`-z` printed
`R  plain.txt -> renamed.txt`; `with space.txt` emitted raw under `-z` and `"with space.txt"` without
it; `-c color.status=always` produced **0** ESC bytes; from a subdir with
`-c status.relativePaths=true` the path still printed repository-root-relative (` M sub/nested.txt`).
All five documented properties hold.

## 4. Findings

**F1 — S140 was already landed, and it is not false (informational; no action).**
`corpus/SOURCES.md:146` carries S140 in commit `e715263cb51b713c342ab992d527fe9d61d6f8ff`
("round-45: land SKILL rule block 22 … S140/S141; the lesson"). That commit is **not** an ancestor
of the freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (`git merge-base --is-ancestor` exit 1), and
`git show f762b727:corpus/SOURCES.md | grep -c S140` = **0**: the row is post-freeze record, which is
permitted because `SOURCES.md` is not a frozen path. Independently re-measured, every landed cell is
true — same sha256, same 99,934 bytes, `docs`/`A`/`mined`/`2026-10-28`/`on-release`/`corpus/lessons/round-45.md`
all in-vocabulary (`on-release` 92×, `Nd` 49×; `docs` 47×; `mined` 136×).

**F2 — two landed cells are under-specified, not wrong (calibration; sharper wording offered).**
(a) `scope` names only "Version 1 porcelain status format"; the instrument runs
`git status --porcelain -z`, so `-z` is the variant in scope and the omission makes the row read as
if `-z` were out of scope. (b) `anchor` identifies the passages in prose ("`Porcelain Format
Version 1`", "the `-z` machine-parsing paragraph") rather than by resolvable `id=`
(`#_porcelain_format_version_1`, `#_pathname_format_notes_and_z`). Both are fixable in place; the
row above supplies the tighter cells.

**F3 — the lesson Gate quote is an elided quote, so a byte-grep of it misses (calibration).**
`corpus/lessons/round-45.md:25` quotes 21 words with `…`: "guaranteed not to change … between Git
versions or based on user configuration … ideal for parsing by scripts". The stated word count is
correct (22 tokens incl. the ellipsis, 21 words without), and the meaning is faithful, but the
elision drops "This makes it", so `byte_contiguous_on_page` is **False** for that string. The 24-word
Q1 span above is contiguous in both rendered text and raw HTML; if the Gate block is re-cut, use Q1.

**F4 — the dirty arm counts a rename as two elements (precision note on C1, not a defect).**
`frozen-path-preflight.py:137-140` builds `dirty` as `[e for e in st.stdout.split("\x00") if e.strip()]`.
Under v1 `-z` a rename occupies **two** NUL-terminated fields (`R  <to>\0<from>\0`); the fixture's
4 dirty paths produced **5** list elements, one of which is a bare `<from>` path with no status
prefix. The arm's only use is the boolean `not dirty`, which stays correct; but the receipt's `dirty`
array is not one-entry-per-path whenever a rename is present, so any future consumer that reads
`receipt["dirty"][i][:2]` as a status code would misparse. Cheap hardening for a later round: pair
`R`/`C` entries (consume the next field) instead of splitting flatly.

**F5 — scope boundary of the row, and ten older call sites that predate S140 (coverage).**
Measured with include filters *before* `--` (`grep -rn -I --include='*.py' --include='*.sh'
--include='*.mjs' -- '--porcelain'`): prose mentions in `corpus/**.md` = **44** (39 files, 41 of them
in `corpus/lessons/`); code mentions in `tools/` excluding `round-45/` = **13 lines in 9 files**, of
which **3 lines mention `-z` and 10 do not**, spread over **8 files**:
`tools/round-29/prefile-check.sh:20`, `tools/round-30/settle-gate.py:8` (docstring),
`tools/round-40/c2-counter.py:1335`, `tools/round-41/c2-counter.py:2469`,
`tools/round-42/c2-counter.py:2996`, `tools/round-42/prefile-gate.py:354`,
`tools/round-43/c1-counter.py:4079`, `tools/round-43/c2-score-r43.py:114`.
Those ten parse porcelain **without** `-z`, i.e. they inherit the quote/munge hazard S140 warns
about (a path with a space prints `"with space.txt"` in non-`-z` output — observed in
`receipt-v1-semantics.txt`). They are **out of this round's registry scope** (`c2-counter.py`'s
scope is the six paths named by `plans/round-44-claims.md` and `plans/round-45-claims.md`, which does
not include rounds 40–43), so this is not a C2 failure; it is a standing hazard and a candidate for a
later round. The only executing consumer of S140's contract today is
`tools/round-45/frozen-path-preflight.py:137`. The row's `scope` claims the instrument family, not
the 44 prose mentions and not `-z`-safety for the ten older sites.

## 5. Claim-predicate contact (R45-C1, clauses 4–5)

- Clause 5 ("the block cites `S140` and `tools/round-45/frozen-path-preflight.py`"): the docstring at
  `frozen-path-preflight.py:30-31` already cites S140 by URL and states the v1 guarantee and the `-z`
  machine-parsing recommendation. Verified by `receipt-instrument-binding.txt`.
- Clause 5's other half ("the interpreter is present at `--rev`") is not this seat's measurement and
  was not run; the receipt only shows the file at the working tree.
- Clause 4 (citations resolve) is not this seat's measurement. No counter was run and no
  `met_target` is claimed. This seat scores nothing.

## 6. Conflicts to reconcile verbatim

None between seats. Two internal tensions the canonical judge should see as stated, not resolved:

1. `SOURCES.md:146` `anchor` = "anchors `Porcelain Format Version 1` and the `-z` machine-parsing
   paragraph" **vs** the resolvable slugs `#_porcelain_format_version_1`,
   `#_pathname_format_notes_and_z` measured here. Same passages, different addressing.
2. `corpus/lessons/round-45.md:25` quote string is **not** byte-present (elision of "This makes it")
   while `row.md` Q1 is. Both are on the same page and say the same thing.

## 7. Out of scope / not run

- No counter (`c1-counter.py`, `c2-counter.py`, `frozen-path-preflight.py`) executed; no exit 0/1/2
  claimed for any predicate. Clause 5's `--rev` presence and clause 4's citation resolution unmeasured.
- No SKILL.md row, block, or lesson edited — landing is L1's.
- One access window only (two fetches, same day); no second-day recheck of the page.
- Behaviour evidence is git 2.56.0 alone; a forward-compatibility guarantee cannot be falsified by a
  single version.

## 8. Artifacts (all under `.ufo/waves/round-45/w1/R45W1SrcGitStatus/`)

| file | bytes | sha256 |
|---|---|---|
| `row.md` | 10152 | `cbce9a9ceed2d38d5f0b0e5a75545f99506e298537958bae155ccee216fe9fad` |
| `git-status.html` (saved page) | 99934 | `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9` |
| `git-status.txt` (extracted text) | 21043 | `fd785b552795b940133da0b7a3807e6da3a40218b45ff39803311a03568ec1ac` |
| `receipt-fetch.txt` | 858 | `14f085edf376ea04b04e1696802fc34c988f3cf69fccf21855f663a4a707bc7d` |
| `receipt-headers.txt` | 723 | `8fb041742260d416ebfc1866e27b787366a3415e97b1fa533857aa518f610d16` |
| `receipt-quote-presence.txt` | 2633 | `f674a16c95dee7078d47bca603dff9413a432e71c9bca600cc8ba27ccf1d204a` |
| `receipt-v1-semantics.txt` | 3099 | `17d32354f319b8d578b0801f1f159f3fcbbbe2d5441a4a4448cd3611337b26c8` |
| `receipt-instrument-binding.txt` | 1911 | `9dd90ffb77a10328dc79d6d9eb5f2b5cd406f57db5ed909953344a5edcdcdbda` |
| `receipt-schema.txt` | 1505 | `72708b7f0326695d9ef325c4bdecfca765ac88342e00a5dae470959961b4966d` |

Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W1SrcGitStatus` removed before yield; the saved page
and every receipt above were copied out first. Nothing was written under `/tmp`.
