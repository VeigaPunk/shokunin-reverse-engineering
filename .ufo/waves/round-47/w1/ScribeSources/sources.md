# Round 47 wave 1 — `corpus/SOURCES.md` drafts (seat ScribeSources)

Rule: `plans/round-47-claims.md`. Base `13a9e9e1`, first freeze `5017e1f7`; the lane had advanced to a
six-commit freeze series (A1 `9018c53b` … A6 `f54b3b6d`) by the time these rows were measured, while
the claims file discloses two (findings F4/F5 in `../ScribeSources.md`).
Nothing here is written into `corpus/SOURCES.md` — this seat is read-only on the lane tree; every row
below is ready to paste.

## Registry-first checks (done before opening anything)

| check | command | result |
|---|---|---|
| current census | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | `144` rows, ids `S001`…`S144` |
| next free id | `grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md \| tail -3` | `S142`, `S143`, `S144` → next free `S145` |
| maximum at the first freeze | `git show 5017e1f:corpus/SOURCES.md` | `S142` (the S143 row arrived in `e856beb5`) |
| `--diff-merges` already registered? | `grep -n 'diff-merges' corpus/SOURCES.md` | `S142` — do not duplicate |
| `re.fullmatch` already registered? | `grep -n 'docs.python.org' corpus/SOURCES.md` | `S050` (json), `S143` (`re`, landed in `e856beb5`) |
| Python CLI / hashlib registered? | `grep -cn 'hashlib\|cmdline\|isolated' corpus/SOURCES.md` | `0` — both unoccupied |

## Admitted (new ids)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S145 | Python command-line and environment documentation — https://docs.python.org/3/using/cmdline.html | docs | A | the `-I` isolated-mode guarantee the round-47 counting command depends on (implies `-E`, `-P` and `-s`; every PYTHON* variable ignored; neither the script's directory nor the user's site-packages on `sys.path`) and `-B`'s bytecode-write suppression; not the rest of the CLI, not the CPython binary's identity, not the `-X` options | Page fetched 2026-10-28T17:53:30Z (HTTP 200, 171,073 B, sha256 `c19141f2030687e14e00e73fff1ed482c3608813dfdc66a0b0931b92bb2902ac`); anchor `-I`, sentence "Run Python in isolated mode. This also implies -E, -P and -s options."; the version-pinned `https://docs.python.org/3.14/using/cmdline.html` copy (160,951 B, sha256 `a1ebda77fb59415d6701f38a08e4e83c0c6766023048b775cff94cf5e7a9667d`) carries the same passage byte for byte | `-I` and `-B` are both load-bearing and neither implies the other: `-I` strips the script's directory from `sys.path` (which is why both counters re-insert their own directory at `exact.py:23-24` and `record.py:28-29`) and ignores PYTHON* variables, while only `-B` stops a `.pyc` being written into the frozen directory. | mined | 2026-10-28 | on-release | corpus/lessons/round-47.md |
| S146 | Python hashlib documentation — https://docs.python.org/3/library/hashlib.html | docs | A | the digest interface's stated subject — the concatenation of the bytes fed — and the `hexdigest()` output form; not the OpenSSL provider choice, `usedforsecurity`, `file_digest`, or any lane pin | Page fetched 2026-10-28T17:53:30Z (HTTP 200, 121,928 B, sha256 `fc778efd702a9324aa999577997ac2231c84567f79f134ba6a3cb252127be6c1`); anchor `Constructor methods`, sentence "ask it for the digest of the concatenation of the data fed to it so far" | A digest covers the concatenation of the bytes fed and records no boundary between them, so `mutations_sha256` pins a join convention rather than a structure: the pin cannot be inverted to recover the four mutation names, which is why clause 6 also requires the block to name them. | mined | 2026-10-28 | on-release | corpus/lessons/round-47.md |

### Why each earns a row

- **S145** — the counting command in the claims file is literally `python3 -I -B tools/round-47/exact.py …`
  and no registry row explains either flag. Both counters manipulate `sys.path` *because* of `-I`
  (verified by reading `exact.py:23-24`, `record.py:28-29`), and `tools/round-47/__pycache__/` holds two
  `.pyc` files, so a run without `-B` plainly already happened in the frozen directory. The row is the
  only place a reader learns which failure each flag prevents.
- **S146** — clause 6 requires the digest *and* the four names; the doc's "digest of the concatenation"
  is the reason the second half is not redundant. It also grounds the lesson's R47-CL4 (the pin binds
  names, not mutation bodies).

## Already landed, independently verified (no new id)

| row | verdict | independent measurement |
|---|---|---|
| S143 `re` — https://docs.python.org/3/library/re.html | **sound, keep** | HTTP 200, 257,706 B, sha256 `f169ed065bf6e6ad779dd7049e6e4ce4ac1081c10eb3f40cd079b0a1f9d11f6a` — reproduces the landed pin exactly on two separate fetches; `id="re.fullmatch"` present (`grep -c` → 1); located quote "If the whole string matches the regular expression pattern, return a corresponding Match." (14 words) |
| S144 regex HOWTO — https://docs.python.org/3/howto/regex.html | **sound, keep** | HTTP 200, 165,172 B, sha256 `5e205f7d5a4e3c66f9d044625d170059a16f979cf996b6ccaa1ba37f7da7f9be`, equal to the landed pin; its claim "the token `fullmatch` occurs 0 times in the rendered text" is true (`grep -c fullmatch regex.html` → 0; 0 in tag-stripped text too); abstract: "This document is an introductory tutorial to using regular expressions in Python with the re module." (17 words) |

### One recommended repair to S143's scope (optional, L1's call)

`/3/` is a moving alias: it served **Python 3.15 development** docs at fetch time (every
`Python 3.1[0-9]` hit on the page reads `3.15`), while the counting command's interpreter is
**3.14.8** (`python3 -V`). The teaching is not version-sensitive — the `re.fullmatch` passage
extracts **byte for byte identically** from `/3/` and from `/3.14/` (both extractions sha256
`58c6c5854e67…`), and the same holds for the `-I` passage (both `a46120cb6617…`) — but the URL
should say so. Append to S143's anchor cell:

> the `/3/` alias served 3.15 development docs at fetch time while the counting command runs 3.14.8;
> the version-pinned `https://docs.python.org/3.14/library/re.html` copy (250,047 B, sha256
> `755a744674c17bdfa46b2753508b89e3e2431b1621a1f481290af521819cec7e`) carries the `re.fullmatch`
> passage byte for byte

## Not admitted

| candidate | outcome | reason | flip condition |
|---|---|---|---|
| git-log `--diff-merges` entry — https://git-scm.com/docs/git-log | **no row — duplicate of S142** | `S142` already binds exactly this source and anchor for the flag-order arm. Re-fetched 2026-10-28T17:53:30Z: HTTP 200, 375,834 B, sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`, identical to S142's pin, so the registered row is accurate and a second id would be redundant. | none needed; re-open only if `--diff-merges` gains a format the arm would have to distinguish |
| Python Regular Expression HOWTO — https://docs.python.org/3/howto/regex.html | already carried as **S144 (rejected)** by the landing | This seat reached the same source and the same verdict independently before reading the landed row; the round's single reject is therefore already registered and this seat adds no second rejected id. | as stated in S144: an edition that documents `fullmatch` beside `search` with its return semantics |

## Landing conditions for these rows

1. Census moves `142 → 146` in `corpus/lessons/round-47.md` (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
   reads `144` now, `146` after S145/S146).
2. The lesson's "Sources opened this round" table needs the two lines below, or `used-by` is false:

   | row | URL | opened | located quote (≤25 words) |
   |---|---|---|---|
   | S145 | https://docs.python.org/3/using/cmdline.html | 2026-10-28T17:53:30Z, HTTP 200, 171,073 B, page sha256 `c19141f2…`; anchor `-I` | "Run Python in isolated mode. This also implies -E, -P and -s options." (13 words) |
   | S146 | https://docs.python.org/3/library/hashlib.html | 2026-10-28T17:53:30Z, HTTP 200, 121,928 B, page sha256 `fc778efd…`; anchor `Constructor methods` | "ask it for the digest of the concatenation of the data fed to it so far" (15 words) |

   and the "Admission and rejection" list needs two `**Admit**` lines.
3. If S145/S146 are not landed, nothing else in this file changes — S143/S144 need no edit beyond the
   optional scope note above.

## Receipts

`receipts.jsonl`, `receipts2.jsonl`, `pins.json` in this directory. Every line carries the exact argv,
exit code, stdout sha256, stdout bytes and UTC time. Discarded measurements are named in
`../ScribeSources.md` § Gates.
