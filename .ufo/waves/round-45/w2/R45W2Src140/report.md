# R45W2Src140 — S140 (`git-status`) adversarial re-open

Seat `R45W2Src140` (scribe), round 45 wave 2, lane `kaidoku`. Leaf member: no subagent
dispatch. Read-only on the lane tree; every write below is under
`.ufo/waves/round-45/w2/R45W2Src140/`. No tool was installed (git 2.56.0, python 3.14.8,
curl 8.23.0 were already present). Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W2Src140`
was removed after its receipts were copied here.

Revisions named by the ticket: freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, landing
`e715263cb51b713c342ab992d527fe9d61d6f8ff`, measured revision A1
`1f4b27f82353d6544dc0c8048b3cfdadd8525d12`. Lane HEAD at run time:
`0ee50aaff516571aa607769bbbdf19a3db90dfa5`.

Target: the S140 row at `corpus/SOURCES.md:146` and the S140 Gate row at
`corpus/lessons/round-45.md:26`, plus the claim that `SKILL.md` block 22's dirty arm reads
`git status --porcelain -z` because S140 says that is the machine form. The frozen claims
file `plans/round-45-claims.md` and `tools/round-45/` are byte-frozen; this seat never wrote
to them (receipt R07: worktree hash equals the freeze blob; `git diff FREEZE..A1` over both
frozen paths is empty; `git status --porcelain` for them is empty).

## 1. What was attacked

| # | attack | artefact under test |
|---|---|---|
| A1 | page identity: live re-fetch, HTTP, bytes, sha256, stability | S140 row `anchor` cell; lesson `## Gate` row |
| A2 | the 21-word quote: raw-byte contiguity, normalized-text presence, word count, elision | lesson `## Gate` quote cell |
| A3 | both named anchors resolve and locate the quoted paragraphs | row `anchor` cell |
| A4 | the registry row is the contract's 11-column shape, none empty | `corpus/SOURCES.md:146` vs header `:5` |
| A5 | `used-by` names the row's consumers | row `used-by` cell |
| A6 | S140 actually supports the dirty arm's `--porcelain -z` reading | `SKILL.md` block 22; `frozen-path-preflight.py:137` |
| A7 | the dirty arm can read every `-z` output S140 sanctions (special filenames) | `frozen-path-preflight.py:47,137,140` |
| A8 | the row's teaching cell `-z` makes the **fields** NUL-terminated | `corpus/SOURCES.md:146` cell 7 vs the page |
| A9 | the recorded open time `2026-10-28T15:31Z` is reproducible | lesson `## Gate`; w1 receipts |
| A10 | the recorded word count (21) is right at the measured revision | lesson `## Gate`, `1f4b27f8` |
| A11 | S140/S141 add no duplicate-URL warning and the W04 count is 14 at both ends | lesson `## Gate` admission paragraph |

## 2. Verdicts

| # | verdict | one-line reason |
|---|---|---|
| A1 | **holds** | two fresh fetches at 16:05:56Z: HTTP 200, 99,934 B, `sha256 903e31c5…59ad9`, `cmp` identical; the same hash as wave 1's two fetches (15:38:50Z / 15:41:04Z). Not stale. |
| A2 | **holds (modulo HTML markup and the explicit elision)**; raw-byte grep fails | both fragments are in the whitespace-normalized page; raw contiguous = false (HTML line wraps + the printed `…`); 21 words excluding `…` is exactly right. |
| A3 | **holds** | `Porcelain Format Version 1` (h3) and the `-z` machine-parsing paragraph both resolve; anchor `id`s present once each. |
| A4 | **holds** | header 11 cells, row 11 cells; all cells non-empty; `used-by` is cell 11. |
| A5 | **falsified (minor, incomplete)** | `used-by` = `corpus/lessons/round-45.md` only; `SKILL.md` cites S140 twice, the gate docstring cites it, and `plans/round-45-claims.md` cites it; registry precedent lists multiple consumers. |
| A6 | **holds** | the page's `-z` option text says "Terminate entries with NUL … implies `--porcelain=v1`"; v1's `-z` paragraph says a NUL follows each filename and special filenames are unquoted; the arm runs exactly `git status --porcelain -z` and splits on NUL. |
| A7 | **falsified (instrument; new)** | a non-UTF-8 filename (explicitly sanctioned by S140) makes `git status --porcelain -z` succeed but the arm's `text=True` decode raise `UnicodeDecodeError`; the gate exits **1** with empty stdout, not 2 with a receipt. Reproducer in R09. |
| A8 | **falsified (wording only)** | source says NUL follows each **filename** / entries are NUL-terminated, and "a space still separates the status field from the first filename"; "fields" is too broad. No detection impact. |
| A9 | **not verified (no receipt)** | 15:31Z appears only in the lesson text (and a wave-2 peer's copy of it); wave 1's retained fetches are 15:38:50Z and 15:41:04Z, both after the 15:33:03Z landing. |
| A10 | **holds** | measured 21 words excluding the elision; A1's `(21 words)` and HEAD's `(21 words, excluding the elision marker)` are both true. |
| A11 | **holds** | `sources-census.sh validate` exit 0, 14 W04 + `kaidoku ok`, sha `9f32a8a8…`; same sha as the round-44 end receipt per `R45W1CensusDupClass`; rows 139→141; diff FREEZE→A1 is exactly the two added rows; both new URLs unique. |

Count: 7 holds (A2 holds with the stated caveat), 3 falsified (A5 minor, A7 instrument,
A8 wording), 1 not verified (A9).

## 3. Detail

### A1 — page identity: holds, and the page is stable

`curl -sS -o git-status.html https://git-scm.com/docs/git-status` at **2026-10-28T16:05:56Z**:

```
http_code=200 size_download=99934 url_effective=https://git-scm.com/docs/git-status
903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9  git-status.html
99934
```

A second fetch wrote a second file; `cmp` identical, same sha256 (R02). That is **four**
independent fetches of the same bytes (wave 1 at 15:38:50Z and 15:41:04Z, both recorded in
`.ufo/waves/round-45/w1/R45W1SrcGitStatus/receipt-fetch.txt`; this seat's two at 16:05:56Z),
all `903e31c5…`. The recorded row and lesson cell are current, not stale.

Contrast with the S138 lesson (`corpus/lessons/round-45.md` R45-CL12): a github.com HTML digest
carried a per-request nonce. `git-scm.com` serves an ETag'd static page
(`etag: W/"6adf6913-1865e" = 0x1865e = 99,934`, per wave 1's receipt); its HTML digest is a
stable identity over this window. The row is not exposed to the S138 defect.

### A2 — the 21-word quote: holds modulo markup/elision; raw-byte grep misses

Receipt R03, exact values:

```
raw_html_contiguous_q1: False
raw_html_contiguous_q2: True
raw_html_contiguous_full21: False
normalized_text_contiguous_q1: True
normalized_text_contiguous_q2: True
tokens_including_elision: 22
words_excluding_elision: 21
source_between_fragments: 'based on user configuration. This makes it '
```

The page's sentence (raw lines 2757-2759) is:

> Version 1 porcelain format is similar to the short format, but is guaranteed
> not to change in a backwards-incompatible way between Git versions or
> based on user configuration. This makes it ideal for parsing by scripts.

The lesson's quote starts at "guaranteed" (mid-sentence, lowercased), elides with `…`, and
resumes at "ideal for parsing by scripts". The elision covers the sentence period and exactly
three words (`This makes it`; receipt R03's `source_between_fragments` prints
`based on user configuration. This makes it `), so 24 source words − 3 elided = **21**, which
is the stated count. The elision is marked; the claim is faithful.

The raw 99,934-byte HTML does not contain the 21-word string: asciidoc wraps the line after
`guaranteed` and after `or`, and the `…` is editorial. Fragment Q1 (`… configuration`) is
present only after whitespace normalization; fragment Q2 (`ideal for parsing by scripts`) is
raw-contiguous. Wave 1's own row.md already recorded `byte_contiguous_on_page: False` and
recommended the 24-word Q1 span as the byte-normalized alternative; the landed lesson did not
carry that caveat, only the word count. A mechanical byte-grep of the Gate quote will miss;
a rendered-text check will not.

### A3 — anchors: holds

Receipt R04 (one `grep -c` per line): `Porcelain Format Version 1` = 1;
`recommended for machine parsing` = 1; `Terminate entries with` = 1;
`pathnames are printed as is` = 1; `id="_porcelain_format_version_1"` = 1;
`id="_pathname_format_notes_and_z"` = 1.

Byte offsets in the fetched file: v1 heading id 76,199; the `-z` machine-parsing paragraph
77,109; the `-z` option definition 57,070; the `Pathname Format Notes and -z` h4 90,585.
Wave 1's `row.md` calls 76,125 / 90,511 "HTML byte offset"; those are **character** offsets
(the file has multi-byte UTF-8 before both points; byte − char = 74 for both). The landed
row names its anchors in prose and carries no offsets, so this is a wave-1 record defect
only (F5).

The landed anchor phrase "the `-z` machine-parsing paragraph" resolves to the paragraph at
77,109, inside the v1 section. The stronger dedicated h4 at 90,585 ("pathnames are printed as
is … lines are terminated with a NUL … byte") is not named by the row but supports it.

### A4 — 11-column shape: holds

Receipt R05 (`awk -F'|'` on the header and row):

```
header_cells=11
row_cells=11
cell1=[S140] … cell11=[corpus/lessons/round-45.md]
used_by=[corpus/lessons/round-45.md]
```

The row has no embedded `|`; all 11 cells are non-empty (`mined`, `2026-10-28`,
`on-release`). The census's E01 (`NF != 13`, i.e. not 11 columns plus the two edge pipes) did
not fire (R06). Holds.

### A5 — `used-by`: falsified (minor)

The cell is `corpus/lessons/round-45.md`. The file exists, cites S140 four times, and the
census E11 check is clean. But the row has more consumers:

- `SKILL.md:559` ("S140 guarantees stable for scripts and whose `-z` form is the machine one")
  and `SKILL.md:589` (block 22's dirty row "…, S140");
- `tools/round-45/frozen-path-preflight.py:30-32` (the docstring's source list);
- `plans/round-45-claims.md:165` and the claims' "Sources" paragraph.

Registry precedent for multi-consumer rows exists: S036's used-by is
`corpus/lessons/round-18.md, SKILL.md`; S081's is
`tools/round-27/xpin-attribute.mjs, corpus/lessons/round-27.md`. The S141 wave-2 seat reached
the same verdict for its row (`falsified (minor)`). Fix: list at least
`corpus/lessons/round-45.md, SKILL.md, tools/round-45/frozen-path-preflight.py`. S140 is a new
row (not present at BASE), so the value can be corrected without touching a base row.

### A6 — does S140 support the dirty arm's reading? Yes

Arm code (`tools/round-45/frozen-path-preflight.py`, blob
`633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`, identical at FREEZE and
in the worktree):

| line | code |
|---|---|
| 30-32 | docstring: "S140 https://git-scm.com/docs/git-status — porcelain v1 is guaranteed not to change backwards-incompatibly; `-z` is recommended for machine parsing." |
| 47 | `return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)` |
| 137 | `st = git(root, "status", "--porcelain", "-z", *dscope)` |
| 140 | `dirty = [e for e in st.stdout.split("\x00") if e.strip()]` |
| 135 | `scope_paths = dirty_pathspecs or pathspecs` (the R45-CL15 scope replacement; not S140's claim) |

The page says (line numbers in the 99,934-byte file):

- `--porcelain[=<version>]` (2295-2303): "Give the output in an easy-to-parse format for
  scripts. This is similar to the short output, but will remain stable across Git versions
  and regardless of user configuration"; the version "defaults to the original version `v1`
  format".
- `-z` option (2446-2449): "Terminate entries with **NUL**, instead of **LF**. This implies
  the `--porcelain=v1` output format if no other format is given."
- v1 `-z` alternate (2776-2783): "recommended for machine parsing"; "a **NUL** (ASCII 0)
  follows each filename, replacing space as a field separator and the terminating newline
  (but a space still separates the status field from the first filename)"; "filenames
  containing special characters are not specially formatted; no quoting or
  backslash-escaping is performed".
- `Pathname Format Notes and -z` (3086-3091): "When the `-z` option is given, pathnames are
  printed as is and without any quoting and lines are terminated with a **NUL** (ASCII 0x00)
  byte."

So yes: `git status --porcelain -z` is exactly the documented machine form, `-z` implies v1
when no other version is named, and NUL is the record terminator the arm splits on. The
source supports the reading; the defects are in the arm's **decoder** (A7) and in the row's
word "fields" (A8), not in the citation.

Rename nuance, measured (R08): `R  b.txt\0a.txt\0`. The arm's list becomes
`["R  b.txt", "a.txt"]` — one status-prefixed entry plus a bare old path. Detection is
correct (`not dirty` is false); the receipt is not one-element-per-path for renames. Wave 1
recorded the same shape; it is a receipt-shape note, not a detection defect.

### A7 — the dirty arm cannot read every `-z` output S140 licenses: falsified

Input (R09, git 2.56.0, fixture `$S/utf8fix3`): a clean commit, then one untracked file whose
name is `bad\xffname` (raw byte 0xFF, not valid UTF-8). S140's v1 `-z` paragraph explicitly
licenses this: special filenames are printed as-is, with "no quoting or backslash-escaping".

Observed:

```
git_status_exit 0
git_status_stdout_hex 3f3f20626164ff6e616d6500      # "?? bad\xffname\0"
preflight_exit 1
preflight_stdout_hex                                 # empty
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 6: invalid start byte
  File ".../frozen-path-preflight.py", line 137, in evaluate
    st = git(root, "status", "--porcelain", "-z", *dscope)
  File ".../frozen-path-preflight.py", line 47, in git
    return subprocess.run([...], capture_output=True, text=True)
```

Differing value: the source sanctions raw bytes; the arm decodes as strict UTF-8. Worse, the
uncaught exception exits **1** with no JSON, so a caller reads "frozen path changed" (the
violation code) for a state the gate never evaluated; the gate's own contract reserves 2 for
could-not-evaluate. The selftest has no case for this (no `surrogate`, `xff`, or non-UTF-8
fixture in the file). The lane's frozen paths are ASCII, so this round's score is unaffected;
it is a general gate defect and a second path to a false red.

Fix (round-46 refreeze; the blob is frozen now): capture bytes
(`subprocess.run(..., text=False)`), split `st.stdout.split(b"\x00")`, compare bytes; decode
only for display with `errors="surrogateescape"`; wrap the reader in `try/except
(OSError, UnicodeError)` and return `2, {"reason": "git output decode failed"}` with a
receipt. Apply the same to the `ls-tree`, `log` and `rev-parse` reads in `git()`.

### A8 — "fields NUL-terminated": falsified as wording only

Row cell 7: "The v1 porcelain format is guaranteed not to change backwards-incompatibly and
is the form a script should parse; `-z` makes the **fields** NUL-terminated, which is what the
dirty arm reads."

The page's own qualification (2779-2781) is "a NUL … follows each filename … (but a space
still separates the status field from the first filename)", and the option text (2448) says
"Terminate **entries** with NUL". The status field is not NUL-terminated; filenames/entries
are. The arm is unaffected because it only tests whether any NUL-delimited chunk is non-empty.
Fix: "`-z` terminates each entry with NUL (a NUL follows each filename; the status field
remains space-separated), which is what the dirty arm reads." Materiality: none for
detection; the teaching sentence is simply broader than the source.

### A9 — the recorded open time is not reproducible: not verified

Lesson Gate cell: `2026-10-28T15:31Z, HTTP 200, 99,934 bytes, page sha256
903e31c5…`. The bytes and hash are correct (A1). The **time** has no retained receipt:

| evidence | UTC |
|---|---|
| lesson Gate row (S140 and S141, same second) | 15:31Z |
| freeze commit `f762b727` (committer; author 15:18:55Z) | 15:27:20Z |
| landing commit `e715263c` | 15:33:03Z |
| A1 commit `1f4b27f8` | 15:34:20Z |
| wave-1 seat `R45W1SrcGitStatus` first / second fetch | 15:38:50Z / 15:41:04Z |
| this seat's two fetches | 16:05:56Z |

`grep -rn '15:31' .ufo/waves/round-45` finds only the S140/S141 lesson text quoted in
`R45W2Src141/probe.json` (a peer's copy of the Gate row) — no fetch receipt, no `utc_start`
line, no file mtime. The landing commit already carried the cell two minutes after 15:31Z, so
an unrecorded L1 fetch at 15:31Z is plausible; but on the retained record the first open of
S140 is wave 1's 15:38:50Z, **after** both the freeze (15:27:20Z) and the landing (15:33:03Z).
The frozen claims file at 15:27:20Z already cites S140 and S141. If the lane requires a source
to be open before the claim that cites it is frozen, this is an ordering violation of the
M45-2 class; if it does not, the cell is an unsupported timestamp. Either way the row's
`opened` **date** (`2026-10-28`) is true. Verdict: cannot confirm the time; retain the L1
fetch receipt or change the cell to the retained 15:38:50Z.

### A10 — word count: holds

The Gate quote's tokens: 22 including `…`, 21 excluding it (R03). At the measured revision A1
the cell said `(21 words)`; at HEAD amendment A2 changed it to `(21 words, excluding the
elision marker)`. Both are true; the A2 wording is the better one. (The S141 seat found its
own count wrong at A1 — 23 stated vs 20 measured — and fixed at HEAD; S140 was right at A1.)

### A11 — duplicate-URL census: holds

R06 runs the lane's own validator:

```
kaidoku  W04  … (14 lines) …
kaidoku  ok   /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit 0
```

14 W04 warnings and `kaidoku ok`; stdout sha256 `9f32a8a8…` is the same value
`R45W1CensusDupClass` records and the same value it says the round-44 end receipt carries, so
"14 at both ends" holds. S140 is not among the 14; `grep -c
'git-scm.com/docs/git-status' corpus/SOURCES.md` = 1 and the S141 URL also occurs once. The
FREEZE→A1 diff of `corpus/SOURCES.md` is exactly two added lines (`+2`, no changed rows), and
rows go 139 → 141, so the two new rows add no W04. Holds.

## 4. Gates / receipts

Every row: command, exit, stdout sha256, UTC. Full argv and raw stdout/stderr are in
`receipts/receipts.json` and `receipts/<id>.out|.err`.

| id | UTC | command (abridged; exact argv in receipts.json) | exit | stdout sha256 | bytes |
|---|---|---|---|---|---|
| R01-fetch1 | 2026-10-28T16:05:56Z | `curl -sS -o git-status.html -w … https://git-scm.com/docs/git-status && sha256sum && wc -c && date -u` | 0 | `003b933938360ee777f3276b53b21493a126a46cc64861b4cec52556003f6f91` | 190 |
| R02-fetch2 | 2026-10-28T16:05:56Z | second `curl`, `sha256sum` both, `cmp` | 0 | `5139a3ee1bfc2876e07f63f84a5b87ac635e6b38133305b1bfe05a9ee1bf933d` | 214 |
| R03-quote | 2026-10-28T16:05:56Z | `python3 quotecheck.py git-status.html` | 0 | `921bafee8367d66623814e4a9ab73f5c0dadbe7efb588277463814c4bdfa4a75` | 565 |
| R04-anchors | 2026-10-28T16:05:56Z | `grep -c` ×6 + byte/char offsets | 0 | `f25040a426013b0e9a17b1b328e4bf9a4584fe24d041232ed1846bbed71f19b4` | 97 |
| R05-row-shape | 2026-10-28T16:05:56Z | `awk -F'\|'` header/row cell counts + cells + row sha | 0 | `4027f89df64cad698a99135175f458f9401ac63a063603640f772eb06ffea443` | 861 |
| R06-census | 2026-10-28T16:05:56Z | `scripts/sources-census.sh validate --root … kaidoku` | 0 | `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19` | 1518 |
| R07-revisions | 2026-10-28T16:05:56Z | `git show` S140 counts at FREEZE/LANDING/A1; lesson presence; frozen blob hashes; frozen diff; `git status` | 0 | `99350debfd6f2974902f3ba1f5c00038ca66067db90b32d79f04962e0822d2af` | 425 |
| R08-dirty-rename | 2026-10-28T16:05:56Z | rename fixture; `git status --porcelain -z \| od -c`; preflight `--check-dirty` | outer 0; inner preflight **1** | `8493c02c53bc15ceba6fbbaaf5ff1a2148540233182e0636564306b56c11d2ba` | 578 |
| R09-dirty-nonutf8 | 2026-10-28T16:05:56Z | fixture with `bad\xffname`; `git status` exit 0; preflight `--check-dirty` | outer 0; inner preflight **1** (crash) | `d423121033796fd8755a4a97107ed2a7a0c7088e2545827b8fed7a7bdbf876bc` | 2302 |
| R10-timestamp | 2026-10-28T16:05:56Z | `grep -rn '15:31' .ufo/waves/round-45`; commit times; wave-1 fetch receipt | 0 | `5f2a8c50e2797dec5856f1cf6926f72cd01680f50b58c397ea5d61c40dc41187` | 1228 |

R07 values, verbatim: S140 row count at FREEZE = `0`, at LANDING = `1`, at A1 = `1`; S140
`SOURCES.md` row sha at A1 = `82fea81f…` = worktree; lesson Gate row sha at A1 =
`0fa37405…` (HEAD `dd6810b6…`: A2's wording only); lesson absent at FREEZE (git show exit
128); preflight worktree sha = `633ebc05…` = FREEZE blob; frozen `git diff --stat` empty;
`git status --porcelain` empty.

## 5. Findings to route

- **F1 (new, MEDIUM; instrument).** The dirty arm's `text=True` reader crashes on a
  non-UTF-8 path that S140 explicitly permits, exiting 1 with empty stdout. Reproducer R09.
  Fix as in A7; add a `--selftest` case. This is distinct from R45-CL15 (dirty-scope
  replacement) and from the S141 seat's plain-form quoting finding (commit arm).
- **F2 (record, MEDIUM).** The lesson Gate's `opened 2026-10-28T15:31Z` has no retained
  receipt; the only dated fetches are wave 1's 15:38:50Z/15:41:04Z, after the freeze and the
  landing. Retain the L1 receipt or change the cell. The row's `opened` date is true.
- **F3 (record, MINOR).** S140 `used-by` lists only `corpus/lessons/round-45.md`; `SKILL.md`
  (twice), the gate docstring, and `plans/round-45-claims.md` cite it. Same class as the
  S141 seat's A6; registry precedent S036/S081.
- **F4 (record, LOW).** S140 cell 7's "fields NUL-terminated" is broader than the source
  (entries/filenames are NUL-terminated; the status field stays space-separated).
- **F5 (wave-1 record, LOW).** `R45W1SrcGitStatus/row.md` labels 76,125/90,511 "HTML byte
  offset"; they are character offsets (bytes 76,199/90,585; the file has 74 more bytes than
  characters before both points). The landed row carries no offsets, so no landed defect.
- **F6 (quote, LOW).** The 21-word Gate quote is not a raw byte substring (HTML wraps plus the
  printed `…`); a byte-grep misses it. The 24-word Q1 span is the normalized-contiguous
  alternative; the lesson's "excluding the elision marker" is honest but should also say the
  quote is whitespace-normalized if it is meant to be greppable.
- **F7 (positive).** S140's page receipt is live and stable: four fetches across two seats and
  ~27 minutes, one hash. It is not affected by the S138/github nonce defect (R45-CL12).

## 6. Out of scope / not run

- **The doc's forward-compatibility guarantee** is a statement about future Git versions; a
  single host (`git 2.56.0`) cannot falsify it. Wave 1 exercised the current-version behavior
  table (`receipt-v1-semantics.txt`); this seat did not repeat it.
- **Browser-rendered text** was not used (no browser); all quote checks are on the fetched
  HTML, raw and whitespace-normalized.
- **The `--dirty-pathspec` scope replacement** (R45-CL15) and the **merge-commit freeze arm**
  (R45-CL6) are other instruments/other seats; not re-run here. The arm's line 135 is cited
  only to distinguish it from the S140 claim.
- **The 11-case preflight selftest** was not re-run (the c1 counter and wave 1 cover it; this
  seat's scope is S140 and the dirty arm). No `2` verdict was produced by this seat's checks;
  every S140 value was evaluable except A9.

## 7. Artifacts

- `report.md` (this file) and the trailer copy `../R45W2Src140.md`.
- `receipts/receipts.json` — full argv, cwd, UTC, exit, stdout/stderr sha256 and bytes for
  R01–R10.
- `receipts/R01-fetch1.out` … `R10-timestamp.out|.err` — raw streams.
- Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W2Src140` was removed after the copy; no lane
  file outside this directory was written; no commit, push, stage, stash, or mutating git/jj
  command was run.
