# W2C2Sources — S147 / S148 / S149 and the round-49 snapshots

**Verdict: falsified on two landed locators.** Byte pins, HTTP 200, and stated sizes hold for all three rows. The live pages today are byte-identical to the snapshots at `29883d4ec35a31a8393c4ffb220888c44c0bb022`. S149 places its quote under `DESCRIPTION`; the quote is under the `ERRORS` anchor. S147’s 9-word quote is a cross-clause cut, and it is not the clause S145 quoted. `c2-mismatch.py`: not run. No counter patch.

Axes checked: coverage (every quote, stated word count, HTTP status, byte count, sha256), depth (the element above each quote), calibration (only commands recorded below).

Landing revision read with `git show` / `git cat-file`. Worktree not used. Counters not patched.

## Findings

1. **S149 locator is the previous section.** `corpus/SOURCES.md:155` (blob `0e02bdeca1cae1a7117dbd555dacea800c222693`) names `` `DESCRIPTION` `` immediately before `"EX_USAGE (64) The command was used incorrectly"`. In `corpus/evidence/round-49/c2/freebsd-sysexits.html` the quote follows `<a id="ERRORS" href="#end"><b>ERRORS</b></a>`. The `DESCRIPTION` anchor ends at “Its use is discouraged.” The page has no `h1`–`h6`. Lesson line 25 does not name `DESCRIPTION`; its HTTP 200, 59,251 B, sha256, and 7-word quote hold. C2’s predicate reads S145–S148, so this row cannot turn A6/A7 red. Landed-text miss, not a counter defect.

2. **S147’s second quote crosses a clause boundary and is not S145’s clause.** Both S147 quotes sit under h2 `2. Backdrop to Popper’s Thought` (U+2019), and the next h2 is `3. The Problem of Demarcation`. That heading claim holds. The 9-word quote is the substring `it is consistent with all possible observations, is unscientific` inside one sentence whose main subject is “a theory which is compatible with all such observations” and whose “it” is the psychoanalytic-theories because-clause. S145’s 22-word clause (`if a theory is incompatible … all such observations`, normalised index 12362) starts inside the 21-word quote and runs past it through “conversely, a theory which is compatible with all such observations”, ending before the 9-word quote. It equals neither S147 quote. The teaches cell on line 153 says “the same clauses as S145”. Quote presence after `html_norm`, the 21-word quote, the heading, and the word counts hold. The frozen counter judges quote-in-snapshot and h2/h3 text, not clause boundaries (plan: prose is not judged). Not run here.

3. **S148’s teaches cell names `sysexits(3)`.** That string occurs 0 times on the Linux page. The title and footline are `sysexits.h(3head)`. The SYNOPSIS quote, `EX_USAGE` 64, the 9-word count, Linux man-pages 6.19 / 2025-09-21, and “HTML rendering created 2026-09-09” hold. The h2 text after the counter’s whitespace collapse is `SYNOPSIS top` (the in-heading link). The section id is `SYNOPSIS`.

## Per-row table

Normalisation is the counter’s `html_norm` (`tools/round-49/c2-mismatch.py`: drop script/style, mark `h2`/`h3`, strip tags, unescape, collapse whitespace). Word count is `len(quote.split())`.

| row | stated HTTP / bytes / sha256 | observed | quotes (stated words → split) | heading above the quote | snapshot vs live |
|---|---|---|---|---|---|
| S147 `SOURCES.md:153`; lesson `:23` | 200; 118,135; `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`; snapshot `corpus/evidence/round-49/c2/popper.html` | 200; 118135; same sha256. Git blob `70ca6f044383ac2952ea2ddcd4d38cf75b0b8017` size 118135. Pubinfo: `substantive revision Fri Jul 31, 2026` | Q1 21→21, one hit, norm index 12288. Q2 9→9, one hit, index 12674. Both raw-contiguous hits = 0 (`<em>falsifiability</em>`, newlines). Q1 is a faithful span ending at “it is scientific”. Q2 is finding 2 | h2 at norm offset 8874: `2. Backdrop to Popper’s Thought`. Next h2 at 12990: `3. The Problem of Demarcation`. Both S147 quotes and the S145 clause lie between those two h2 markers. Heading codepoints match the row (U+2019) | equal, including cache-bypass |
| S148 `SOURCES.md:154`; lesson `:24` | 200; 12,725; `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340`; snapshot `corpus/evidence/round-49/c2/sysexits.html` | 200; 12725; same sha256. Git blob `c78fe5f133f87c523e5d1046236ca87569d9824a` size 12725. Footline `Linux man-pages 6.19` / `2025-09-21`. Colophon `HTML rendering created 2026-09-09`. Response `Last-Modified: Wed, 28 Oct 2026 18:28:41 GMT` (body stamps unchanged) | `"#define EX_USAGE 64 /* command line usage error */"` 9→9 (`#define`, `EX_USAGE`, `64`, `/*`, `command`, `line`, `usage`, `error`, `*/`). One norm hit, index 511. Raw hit 0: `<b>#define EX_USAGE 64 </b>/* command line usage error */` | h2 id `SYNOPSIS`. Normalised h2 text `SYNOPSIS top`. Row names `SYNOPSIS`. Define is before h2 `DESCRIPTION top` | equal, including cache-bypass |
| S149 `SOURCES.md:155`; lesson `:25` | 200; 59,251; `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`; snapshot `corpus/evidence/round-49/c2/freebsd-sysexits.html` | 200; 59251; same sha256. Git blob `0fe0b09fd19ceebb20a9a7fe24d184c52451280a` size 59251. `<title>sysexits(3) - FreeBSD 15.1-RELEASE and Ports.quarterly Manual Pages</title>`. h1–h6 count 0 | `"EX_USAGE (64) The command was used incorrectly"` 7→7. One norm hit, index 11050. Raw hit 0: `<b>EX_USAGE</b> (64)` plus tabs and doubled spaces (`was  used  incorrectly`). Sentence continues “, e.g., …” | `<a id="ERRORS" href="#end"><b>ERRORS</b></a>` then the list. `DESCRIPTION` is the previous anchor. `html_norm` h2/h3 above the quote: none | equal. First response `X-Cache: HIT` `Age: 1291`. Cache-bypass `X-Cache: MISS` `Age: 0`. Same sha256 |

Search-log line 244 says the FreeBSD fetch was HTTP 200 and that the three pages were pinned under `corpus/evidence/round-49/c2/`. Those two statements hold. Identified/screened/included counts on that line: not re-counted.

## Commands

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Revision: `29883d4ec35a31a8393c4ffb220888c44c0bb022`. Scratch was `/fast/scratch/hyaku/kaidoku-r49/W2C2Sources` (`TMPDIR` set there). Disk guard before the pass: `/fast/scratch/hyaku` 37% used, 511.4G free (`scripts/hyaku/disk-guard.sh status`; the consumer listing was still running when this seat moved on). `GIT_NO_REPLACE_OBJECTS` was not required for these read-only object reads.

Git (exit 0), UTC with the cache-bypass pass `2026-10-28T22:40:56Z`:

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse 29883d4ec35a31a8393c4ffb220888c44c0bb022
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin cat-file -s 29883d4ec35a31a8393c4ffb220888c44c0bb022:<path>
```

Stdout of `rev-parse` is the revision above. Blob sizes: popper 118135, sysexits 12725, freebsd 59251, `corpus/SOURCES.md` 169518, `corpus/lessons/round-49.md` 12948. Lesson blob `eeaf1225bdb0bdef4591d225fddd4e67be430db4`. Recorded in `git-blobs.txt`.

First fetch, shell exit 0, `2026-10-28T22:38:50Z`–`22:38:53Z`. Per-curl exit code: not recorded. `-w` and the status line both say 200. Zero redirects.

```
curl -sS -L --max-redirs 5 --retry 2 --retry-delay 1 \
  -A 'kaidoku-r49-w2-W2C2Sources/1.0 (source re-fetch; research)' \
  -D <hdr> -o <body> \
  -w '%{http_code} %{size_download} %{url_effective} %{num_redirects} %{content_type}' \
  --max-time 60 <url>
```

| url | `-w` stdout | bytes | sha256 |
|---|---|---|---|
| `https://plato.stanford.edu/entries/popper/` | `200 118135 https://plato.stanford.edu/entries/popper/ 0 text/html` | 118135 | `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207` |
| `https://man7.org/linux/man-pages/man3/sysexits.h.3head.html` | `200 12725 https://man7.org/linux/man-pages/man3/sysexits.h.3head.html 0 text/html` | 12725 | `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` |
| `https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3` | `200 59251 https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 0 text/html` | 59251 | `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` |

Cache-bypass refetch, each curl exit 0, `2026-10-28T22:40:54Z`–`22:40:57Z`. Bodies byte-equal to the first fetch and to `git show` of the three snapshots.

```
curl -sS -L --http1.1 --max-redirs 5 \
  -A 'kaidoku-r49-w2-W2C2Sources/1.0' \
  -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
  -D <hdr> -o <body> -w '%{http_code} %{size_download} %{num_redirects}\n' \
  --max-time 60 <url>
```

| page | exit | start–end | `-w` stdout | stdout sha256 | body sha256 |
|---|---|---|---|---|---|
| popper | 0 | `22:40:54Z`–`22:40:55Z` | `200 118135 0` | `2bb0911d964a552dc88d4ac78eef27ac49ad1a2ae40a89a9286f6e94fc0a89fc` | `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207` |
| sysexits | 0 | `22:40:55Z`–`22:40:56Z` | `200 12725 0` | `372da6161ec1835c5c6cd6ee9af32379fd22de68bc1beb6bd42eb233139f9a68` | `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` |
| freebsd | 0 | `22:40:56Z`–`22:40:57Z` | `200 59251 0` | `1a3ae5126569d951039b179368d7d258a41637c91717b0cef79bdf6602bf487d` | `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf` |

Receipts and response headers: `.ufo/waves/round-49/w2/W2C2Sources/`. `artifact-sha256.txt` hashes those files.

Quote location was a local Python replay of `html_norm` / `section_of` over the fetched bodies. Exit 0. That replay is not `c2-mismatch.py`.

## What held

- All three snapshot sha256 values in the rows and the lesson match the git blobs and both live fetches.
- Stated sizes 118,135 / 12,725 / 59,251 match the body lengths.
- Each quote occurs once after `html_norm`. Stated word counts 21, 9, 9, and 7 match `split()`.
- S147’s 21-word quote and the heading `2. Backdrop to Popper’s Thought`, including the claim that both quotes precede `3. The Problem of Demarcation`.
- S148’s define sits in SYNOPSIS and states `EX_USAGE` 64. The rendering dates in the row match the page body.

## Not run

`python3 -I -B tools/round-49/c2-mismatch.py` (with or without `--battery`). No install. No mutating git.
