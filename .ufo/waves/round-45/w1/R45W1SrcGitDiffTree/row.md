# S141 — git-diff-tree documentation: registry row, Gate block, proof

Seat `R45W1SrcGitDiffTree`, round 45 wave 1. Read-only on the lane tree; nothing below was
written into `corpus/SOURCES.md` or `corpus/lessons/round-45.md`.

## 1. Live open (source S141)

| field | value |
|---|---|
| URL | `https://git-scm.com/docs/git-diff-tree` |
| command | `curl -sS -L --max-time 60 -o s141.html -w '%{http_code}\n' https://git-scm.com/docs/git-diff-tree` |
| UTC (pre-command) | 2026-10-28T15:38:50Z |
| HTTP status | `200` |
| bytes | `256810` |
| sha256 | `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640` |
| curl exit | `0` (stderr empty) |
| saved copy | `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/s141-git-diff-tree.html` (same sha256) |
| tool versions | curl 8.23.0, git 2.56.0, python 3.14.8 |

The sha256 measured by this seat is byte-identical to the `opened` cell already drafted in
`corpus/SOURCES.md:147` (a fetch ~7 min earlier), so the page bytes are reproducible across
two independent fetches and seats.

## 2. The two located statements the assignment names

Both live in the page's own HTML; locators are **raw `<p>`/`<dt>` line numbers of the saved
copy**, and anchors are the `id` attributes present at those lines.

### A. `--name-status` + `-z`: NUL field terminators, pathnames not munged

- Section: `OPTIONS` → `<dt>` for `-z`
- Anchor: `Documentation/git-diff-tree.txt--z` (also `#Documentation/git-diff-tree.txt--z`), raw line **3644**
- Text locator: raw lines **3646-3647** (sentence begins `When --raw, --numstat, --name-only …`)
- Located quote (20 words):

> "When --raw, --numstat, --name-only or --name-status has been given, do not munge pathnames and use NULs as output field terminators."

- Shorter cell-safe form (11 words): *"do not munge pathnames and use NULs as output field terminators."*
- Neighbouring anchor for the same option family: `Documentation/git-diff-tree.txt---name-status`, raw line **3661**.
- The sentence is scoped to `--raw`, `--numstat`, `--name-only` **or** `--name-status` — i.e. it
  licenses all four machine forms, which matters because the frozen counter's freeze arm uses
  `--name-only` (`tools/round-45/c1-counter.py:53`) and its preflight uses `--name-status`
  (`tools/round-45/frozen-path-preflight.py:93`).

### B. Raw output format: a tab — or a NUL with `-z` — separates the fields

- Section: `Raw output format`
- Anchor: `_raw_output_format`, `<h2>` at raw line **5369**
- Field list introduced at raw line **5418** (`That is, from the left to the right:`), after the
  sample block at **5405** (`An output line is formatted this way:`)
- Field order confirmed at these raw lines:

| raw line | `<li>` text |
|---|---|
| 5450 | `status, followed by optional "score" number.` |
| 5453 | `a tab or a NUL when -z option is used.` |
| 5459 | `a tab or a NUL when -z option is used; only exists for C or R.` |
| 5465 | `an LF or a NUL when -z option is used, to terminate the record.` |

- Located quote (16 words, ≤25):

> "a tab or a NUL when -z option is used; only exists for C or R."

- Record-terminator quote (14 words): *"an LF or a NUL when -z option is used, to terminate the record."*
- Why the C/R line is the load-bearing one: it is the only place the page states a **second**
  pathname field exists for a copy/rename record, which is the framing a commit-touching gate
  must handle (see §4, receipt B: `R100\0old.txt\0new.txt\0` is three NUL-terminated fields).

## 3. 11-column registry row (candidate, verbatim 11 cells)

This row is **already present** at `corpus/SOURCES.md:147` at HEAD `faa875bc0eb839d15b83c4afa6078819e5a7b381`
(landed by `e715263cb51b713c342ab992d527fe9d61d6f8ff`, "round-45: land SKILL rule block 22 …"); the
`S1xx` census moved 40 → 42 rows across that commit. Reproduced here after live verification so the
L1 can compare rather than append a duplicate:

```markdown
| S141 | git-diff-tree documentation — https://git-scm.com/docs/git-diff-tree | docs | A | git diff-tree raw and name-status output, used to enumerate the paths a commit touched | Page fetched 2026-10-28 (HTTP 200, 256,810 bytes, sha256 `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`); anchors `-z` and the raw output format section | With --name-status and -z the fields are NUL-terminated and pathnames are not munged, so a gate can read touched paths without quoting ambiguity. | mined | 2026-10-28 | on-release | corpus/lessons/round-45.md |
```

Column audit (11 cells, header order `id | source | kind | tier | scope | anchor | teaches |
status | opened | recheck | used-by`):

| # | column | cell value | verified against |
|---|---|---|---|
| 1 | id | `S141` | unique: `grep -c '^| S141 ' corpus/SOURCES.md` → 1 |
| 2 | source | `git-diff-tree documentation — https://git-scm.com/docs/git-diff-tree` | live fetch §1 |
| 3 | kind | `docs` | page is the rendered Git reference documentation |
| 4 | tier | `A` | primary upstream documentation of the cited behavior |
| 5 | scope | `git diff-tree raw and name-status output, used to enumerate the paths a commit touched` | §2 A and B both inside this scope |
| 6 | anchor | `Page fetched 2026-10-28 (HTTP 200, 256,810 bytes, sha256 …); anchors -z and the raw output format section` | all three match §1; anchors resolve to raw 3644 and 5369 |
| 7 | teaches | `With --name-status and -z the fields are NUL-terminated and pathnames are not munged …` | documented statement A; empirically receipted in §4 |
| 8 | status | `mined` | claim cites it; the instrument behavior is receipted here |
| 9 | opened | `2026-10-28` | §1 UTC |
| 10 | recheck | `on-release` | docs page tracks the git release train |
| 11 | used-by | `corpus/lessons/round-45.md` | assignment; matches the landed cell |

Registry acceptance (read-only): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
→ exit **0**, last line `kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`,
**no** `S141` line (neither error nor `W04`); `grep -c W04` → 14; `grep -c 'git-scm.com/docs/git-diff-tree'`
→ 1 (URL unique in this lane's scope). Receipt stdout sha256 `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19`, UTC 2026-10-28T15:41:58Z.

## 4. Gate block rows (drop-in for `corpus/lessons/round-45.md` `## Gate`)

The landed Gate row for S141 carries quote A only, and its word count is wrong (finding F2).
Suggested replacement / addition, one table row per located statement:

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S141 | https://git-scm.com/docs/git-diff-tree | 2026-10-28T15:38:50Z, HTTP 200, 256,810 bytes, page sha256 `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`; anchor `Documentation/git-diff-tree.txt--z`, raw lines 3646-3647 | "When --raw, --numstat, --name-only or --name-status has been given, do not munge pathnames and use NULs as output field terminators." (20 words) |
| S141 | https://git-scm.com/docs/git-diff-tree | same fetch; anchor `_raw_output_format`, raw line 5459 (field list from 5418; siblings 5450, 5453, 5465) | "a tab or a NUL when -z option is used; only exists for C or R." (16 words) |

Only the row in §3 has 11 cells; the two rows above have 4 cells and belong to the Gate table
(`row | URL | opened | located quote`), so a `^| S141 |` grep over this file returns three lines
and only the 11-cell one is a registry row.

If the L1 keeps one row, the 20-word quote A plus the §2 B locator is enough; the C/R
sentence is the one that justifies parsing **two** paths from one record.

## 5. Proof that the quotes are in the saved copy

Verifier `prove.py` (saved beside this file): strips HTML tags, unescapes `&lt;`/`&gt;`/`&amp;`,
collapses whitespace, then requires each quote as a substring; exits 1 if any is absent.

```
python3 -I -B prove.py .ufo/waves/round-45/w1/R45W1SrcGitDiffTree/s141-git-diff-tree.html
```

| quote | words | present in saved copy | first raw line |
|---|---|---|---|
| A `When --raw, --numstat, --name-only or --name-status … field terminators.` | 20 | true | 3646 |
| B `a tab or a NUL when -z option is used; only exists for C or R.` | 16 | true | 5459 |
| C `status, followed by optional "score" number.` | 6 | true | 5450 |
| D `an LF or a NUL when -z option is used, to terminate the record.` | 14 | true | 5465 |

- exit `0`, UTC 2026-10-28T15:40:17Z, `prove.json` sha256 `aaf83dca1c7004b278249ca12eb52cffb4c834802ac219794af96c4c15b62a59`
- the verifier reads the **saved** 256,810-byte copy whose sha256 is `f81c1e31…` (§1), not the network

Raw-HTML locator (independent of the text extraction): `grep -n 'do not munge pathnames' s141.html`
→ `3647`, and `grep -n 'a tab or a NUL when' s141.html` → `5453`, `5459`, `5465`.

## 6. Empirical check of the documented framing (git 2.56.0, scratch fixtures)

Fixture protocol honoured: `S=/fast/scratch/hyaku/kaidoku-r45/R45W1SrcGitDiffTree`,
`D=$(mktemp -d -p "$S" …) && git -C "$D" init -q`, `git -C "$D" rev-parse --show-toplevel`
asserted equal to `$D` before the first commit, all later calls `git -C "$D"`, throwaway
identity only inside `$D`.

**Receipt B** (`fixture_receipts.sh`, stdout `fixture-transcript.txt` sha256 `8823a38b4a1cc8d4775789973e3a24d0b8a9ccf04f8048332c51e7d73e2ac18b`, exit 0, UTC 2026-10-28T15:40:49Z):
one commit adds `old.txt`, `é.txt`, and a path containing a literal tab, then renames `old.txt`
→ `new.txt`.

`git diff-tree -r -M --name-status --no-commit-id <C>` (no `-z`):

```
R100	old.txt	new.txt
M	"tab\there.txt"
M	"\303\251.txt"
```

`git diff-tree -r -M --name-status --no-commit-id -z <C> | od -c`:

```
0000000   R   1   0   0  \0   o   l   d   .   t   x   t  \0   n   e   w
0000020   .   t   x   t  \0   M  \0   t   a   b  \t   h   e   r   e   .
0000040   t   x   t  \0   M  \0 303 251   .   t   x   t  \0
```

NUL count over that stream: **7** = 3 (rename: `R100`, src, dst) + 2 (tab file: `M`, path) +
2 (`é` file: `M`, path). Reading:
- without `-z` the pathnames **are** munged — tab is C-escaped to `\t`, the UTF-8 byte becomes
  `\303\251`, and both are wrapped in quotes; a pathname containing a tab would collide with the
  field separator if it were not quoted;
- with `-z` every field is NUL-terminated and the pathname bytes are raw (including the literal
  TAB byte at offset 0000031), exactly statement A;
- with `-z` the status and the pathname are **separate** NUL-terminated fields, so a record is
  `STATUS\0PATH\0` — a parser must not assume "status then tab".

**Receipt C** (`raw-transcript.txt` sha256 `3971806849303142da11f3bb8a65b31565563a6d28ae72b8f420fbd47a988f95`, exit 0, UTC 2026-10-28T15:40:55Z):
`git diff-tree -r -M --raw --no-commit-id -z <C> | od -c` shows the raw record as
`:<mode> <mode> <sha> <sha> R100 \0 old.txt \0 new.txt \0` — the score field then NUL, then src,
then NUL, then dst, then NUL, i.e. statement B's field list with NUL separators. Note the header
fields before the status remain space-separated; only the status/score and path fields switch to
NUL under `-z`.

**Receipt D** (`log-transcript.txt` sha256 `0179ac749dfcc11cc6a04f5c7dfa3cc698d91c084e527ab6e4c62445525e1097`, exit 0, UTC 2026-10-28T15:41:14Z):
the exact frozen-preflight invocation, `git log -m --diff-merges=first-parent --name-status --format=%x00%H -1 <C>`:

```
\0 12b56e7c…f1 \n\n R100 \t old.txt \t new.txt \n M \t "tab\there.txt" \n M \t "\303\251.txt" \n
```

i.e. with **no** `-z` this form returns quoted pathnames — see finding F3.

## 7. Findings (report, never "fix")

**F1 — the drafted Gate row for S141 carries only quote A.** The instrument it justifies
(`frozen-path-preflight.py`) parses `--name-status` records whose rename arm has **two** paths;
that is statement B (raw line 5459 / 5453 / 5465), which the Gate block does not yet cite. Row
added in §4. Severity: depth of the landing evidence, no predicate effect.

**F2 — word-count defect in the landed Gate row.** `corpus/lessons/round-45.md` `## Gate` says the
S141 quote is "(23 words)". Measured: `printf '%s\n' '<quote A>' | wc -w` → **20**, and the same
count from `prove.py` (`"words": 20`). The cell over-states by 3; the ≤25 bound still holds either
way. No counter reads this cell.

**F3 — the frozen preflight cites S141 for `-z` but its commit arm does not pass `-z`.**
`tools/round-45/frozen-path-preflight.py:32` (docstring) says "with --name-status, `-z` terminates
fields with NUL instead of munging pathnames", while line 93 runs
`git log -m --diff-merges=first-parent --name-status --format=%x00%H <base>..<tip>` with no `-z`,
and lines 99-107 split on `"\t"`. `tools/round-45/c1-counter.py:53` likewise runs
`git log --name-only --format=` with no `-z`.
Consequence, measured (receipt D): the paths the gate compares are git's **C-quoted** forms
(`"\303\251.txt"`), not raw pathnames. For the current frozen paths — `plans/round-45-claims.md`
and the ASCII `tools/round-45/` tree (`FROZEN` at `c1-counter.py:32`) — quoted and raw coincide,
so no verdict changes; the arms' quoted `ls-tree --name-only` output is quoted the same way and
`ok = not touched and not blob_changed and not restored and not dirty` (line 142) never
cross-compares representations. Status: docstring/justification is stronger than the code, not a
predicate failure. The repair that would make the sentence true is `-z` plus `\x00` splitting
(receipt B), which this seat did not apply: the instrument is frozen.

**F4 — no selftest case covers pathname quoting.** The preflight's 11 cases
(`frozen-path-preflight.py:265-275`) are `green-clean`, `red-touched`, `red-restored`, `red-dirty`,
`green-dirty-without-arm`, `red-dirfreeze-no-pathspec`, `green-dirfreeze-pathspec`,
`red-unknown-freeze`, `red-nonancestor`, `red-bulk-sweep`, `green-empty-range`;
`grep -n 'quotePath\|quote\|nonascii\|non-ascii\|munged' frozen-path-preflight.py` → no match. So
F3's behavior is untested in either direction; `cases >= 11` (claim C1 clause 6) is met at 11.

**F5 — census count differs from the drafted lesson sentence.** `corpus/lessons/round-45.md`
`## Gate` `### Admission and rejection` says the round-end census yields "exit 0, 16 W04
warnings"; measured at HEAD `faa875bc` with the documented command: exit **0**, `kaidoku ok`,
**14** `W04` lines, no S141 line. `W04` is a *cross-scope* duplicate-URL class, so the count can
move with other lanes' registries; this is a recorded value, not an asserted defect.

## 8. Receipts inventory (all under `.ufo/waves/round-45/w1/R45W1SrcGitDiffTree/`)

| file | sha256 | exit | UTC |
|---|---|---|---|
| `s141-git-diff-tree.html` | `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640` | curl 0 (HTTP 200) | 2026-10-28T15:38:50Z |
| `prove.py` | `4d0859cae508c657ca5190179c321e89980a9a2f39400ea585db3220ed88ce96` | — | — |
| `prove.json` | `aaf83dca1c7004b278249ca12eb52cffb4c834802ac219794af96c4c15b62a59` | 0 | 2026-10-28T15:40:17Z |
| `fixture_receipts.sh` | `089f52aa072aa8564ba04aa1b792812495165d66d9151d27e02ac3f42267b60a` | — | — |
| `fixture-transcript.txt` | `8823a38b4a1cc8d4775789973e3a24d0b8a9ccf04f8048332c51e7d73e2ac18b` | 0 | 2026-10-28T15:40:49Z |
| `raw-transcript.txt` | `3971806849303142da11f3bb8a65b31565563a6d28ae72b8f420fbd47a988f95` | 0 | 2026-10-28T15:40:55Z |
| `log-transcript.txt` | `0179ac749dfcc11cc6a04f5c7dfa3cc698d91c084e527ab6e4c62445525e1097` | 0 | 2026-10-28T15:41:14Z |
| `census.out` | `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19` | 0 | 2026-10-28T15:41:58Z |

The `census.out` receipt lives in this directory (copied out of scratch before teardown), so it
stays citable; the scratch tree that produced it is removed.

