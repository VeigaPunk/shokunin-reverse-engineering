# ScoutS320 — independent non-author re-open of the S320 source (`open(2)`, man7.org)

Seat: `ScoutS320` (scout). Lane: `kaidoku`, round 95, attempt 1.
Declaration commit read: `4bda1d1dd3788973f10e61212b70df18b3b14ea0` (base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`).
Lane is READ-ONLY for this seat: nothing outside this seat directory was written. All work ran from
`/fast/scratch/hyaku/kaidoku-r95/ScoutS320` (scratch, deleted at end of seat).

Scope: (1) fetch the S320 page twice with `curl -fsSL -w '%{http_code}'` and record status/bytes/sha256;
(2) compare both fetches to the L1 fetch `.ufo/waves/round-95/l1/scores/s320-open2-fetch1.html`;
(3) tag-strip + whitespace-normalise and locate the frozen quote and its `O_NOFOLLOW` heading context;
(4) read the man-pages version string verbatim; (5) this table. No lane edits, no subagent dispatch (leaf seat).

---

## 1 — Fetch table (the required table)

| fetch index | HTTP status | bytes | sha256 | quote located | version string | discrepancy |
|---|---|---|---|---|---|---|
| 1 (this seat, `s320-open2-fetch1.html`) | `200` | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes (1 occurrence, normalised) | `Linux man-pages 6.19` | none |
| 2 (this seat, `s320-open2-fetch2.html`) | `200` | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes (1 occurrence, normalised) | `Linux man-pages 6.19` | none |
| L1 `l1/scores/s320-open2-fetch1.html` (reference) | n/a (committed file) | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes (1 occurrence, normalised) | `Linux man-pages 6.19` | none — **byte-identical to both this seat's fetches** |
| L1 `l1/scores/s320-open2-fetch2.html` (reference) | n/a (committed file) | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes (1 occurrence, normalised) | `Linux man-pages 6.19` | none — **byte-identical to both this seat's fetches** |

**The frozen sha256 in `plans/round-95-claims.md` / `.ufo/waves/round-95/claims.json`
(`d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`, 76506 bytes) is CONFIRMED** on two
independent fetches made 2026-11-05, and the two L1-committed fetch files hash to the same value. No page drift.

### Exact commands and exit codes

```
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScoutS320
for i in 1 2; do
  code=$(curl -fsSL -w '%{http_code}' -o "$SEAT/s320-open2-fetch$i.html" https://man7.org/linux/man-pages/man2/open.2.html)
  rc=$?
  echo "fetch$i rc=$rc http=$code bytes=$(stat -c%s "$SEAT/s320-open2-fetch$i.html") sha256=$(sha256sum "$SEAT/s320-open2-fetch$i.html" | cut -d' ' -f1)"
done
```

```
fetch1 rc=0 http=200 bytes=76506 sha256=d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789
fetch2 rc=0 http=200 bytes=76506 sha256=d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789
```

Both `curl` invocations exited **0**; `%{http_code}` was **200** for both. Byte comparison:

```
cmp "$SEAT/s320-open2-fetch1.html" .ufo/waves/round-95/l1/scores/s320-open2-fetch1.html   → IDENTICAL (exit 0)
cmp "$SEAT/s320-open2-fetch2.html" .ufo/waves/round-95/l1/scores/s320-open2-fetch2.html   → IDENTICAL (exit 0)
cmp "$SEAT/s320-open2-fetch1.html" "$SEAT/s320-open2-fetch2.html"                          → IDENTICAL (exit 0)
```

Response headers of a third, header-only fetch (`headers.txt`):

```
http=200 size=76506
Date: Thu, 05 Nov 2026 16:43:32 GMT
Server: Apache/2.4.58 (Ubuntu)
Last-Modified: Mon, 02 Nov 2026 20:20:30 GMT
ETag: "12ada-65f50e092bf80"
Content-Length: 76506
```

`Last-Modified` 2026-11-02 is the page's own timestamp (matches the man-pages 6.19 tarball date 2026-02-08 in
the colophon), not a re-render of the round-95 fetch.

---

## 2 — Quote location

Frozen quote (identical in `plans/round-95-claims.md` and `.ufo/waves/round-95/claims.json`):

> If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP

### 2.1 Not a raw contiguous byte substring

```
python3 scan.py  →  RAW_CONTIGUOUS_COUNT = 0
```

Reason (observed in the source bytes, `s320-open2-fetch1.html` lines 348–352): the sentence is line-wrapped and
`path` / `ELOOP` carry markup:

```html
       <b>O_NOFOLLOW</b>
              If the trailing component (i.e., basename) of <i>path</i> is a
              symbolic link, then the open fails, with the error <b>ELOOP</b>.
              Symbolic links in earlier components of the pathname will
              still be followed.  (Note that the <b>ELOOP </b>error that can
```

### 2.2 After tag-strip + whitespace normalisation it is EXACT, exactly once

Normaliser used (`scan.py`): remove `<script>`/`<style>` blocks, drop all `<…>` tags, `html.unescape`, then
collapse every whitespace run to a single space and strip.

```
NORMALIZED_LEN    43529
NORMALIZED_SHA256 8d8501c9820149256a76d411c3a083f212a57304d53cdb6324ec8a21d62b1f6c   (fetch 1)
NORMALIZED_SHA256 8d8501c9820149256a76d411c3a083f212a57304d53cdb6324ec8a21d62b1f6c   (fetch 2 — same)
QUOTE_EXACT_COUNT 1
```

**Ordinal occurrence: 1st (and only) occurrence** of the full sentence on the page.
`trailing component` occurs exactly **1** time on the whole page — unlike round 94's S319 sentence (2
occurrences), this one is unambiguous and needs no disambiguation.

### 2.3 Heading context and enclosing section

The man7 man-page HTML does **not** use `<dl>/<dt>/<dd>` for flags (counts on the page: `<dl>` 0, `<dt>` 0,
`<dd>` 0); the flag list lives in `<pre>` blocks with `<b>FLAG</b>` term labels. Therefore:

| field | value |
|---|---|
| enclosing section (nearest `<h2>`) | **`DESCRIPTION`** (h2 at raw offset 3956; next h2 `RETURN VALUE` at 32616) |
| heading context (flag term label) | **`<b>O_NOFOLLOW</b>`** at raw offset 18584, directly preceding the sentence at raw offset 18613 |
| preceding flag term | `<b>O_NOCTTY</b>` (so the sentence is the *first* line of the `O_NOFOLLOW` entry) |
| flag class | `O_NOFOLLOW` is a **file status flag** (the page lists `O_CLOEXEC, O_CREAT, O_DIRECTORY, O_EXCL, O_NOCTTY, O_NOFOLLOW, O_TMPFILE, O_TRUNC` as *file creation flags* and the rest as *file status flags*) |
| raw offsets | sentence at 18613 (fetch 1) |

Enclosing normalized context (immediately before the quote):

> `… the access time. O_NOCTTY If path refers to a terminal device—see tty(4) —it will not become the process's controlling terminal even if the process does not have one. O_NOFOLLOW ` **⟨quote⟩** ` . Symbolic links in earlier components of the pathname will still be followed. (Note that the ELOOP error that can occur in this case is indistinguishable from the case where an open fails because there are too many symbolic links found while resolving components in the path prefix of the pathname.) This flag is a FreeBSD extension, which was added in Linux 2.1.126, and has subsequently been standardized in POSIX.1-2008.`

Corroborating occurrence elsewhere on the same page (the `ERRORS` section, h2 at 33034) — a second, independent
statement of the same rule:

> `ELOOP Too many symbolic links were encountered in resolving path . ELOOP path was a symbolic link, and flags specified O_NOFOLLOW but not O_PATH .`

(The `O_PATH` qualifier is the page's own exception: `O_PATH|O_NOFOLLOW` does **not** fail with `ELOOP`. Worth
knowing before the knowledge entry generalises the rule.)

### 2.4 Word count

`WORDS 20 / CHARS 112` — the frozen quote is 20 words, inside the declared ≤25-word bound.

---

## 3 — Version string (verbatim)

From the page footer (`<span class="footline">`):

```
Linux man-pages 6.19            2026-02-08                        open(2)
```

**Version string, verbatim: `Linux man-pages 6.19`** — matches the frozen `page_version` in
`.ufo/waves/round-95/claims.json` and `plans/round-95-claims.md` exactly.

Corroborated by the colophon: *"This page was obtained from the tarball man-pages-6.19.tar.gz fetched from
⟨ https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/ ⟩ on 2026-09-09."*

---

## 4 — Discrepancies

**None on the bytes, the hash, the quote or the version string.** The two independent fetches, the two
L1-committed fetch files, the frozen sha256, the frozen 76506-byte size, the frozen quote wording and the frozen
`Linux man-pages 6.19` label all agree.

Two caveats a landing row / knowledge entry should state, both observed here:

1. **The quote is not a raw contiguous byte substring** (raw count 0). It is exact only after tag-stripping and
   whitespace normalisation, because `path` is `<i>path</i>` and `ELOOP` is `<b>ELOOP</b>`, and the sentence is
   line-wrapped. Same shape as the round-94 S319 finding.
2. **The `O_PATH` exception** in the `ERRORS` section: `ELOOP path was a symbolic link, and flags specified
   O_NOFOLLOW but not O_PATH`. The `O_NOFOLLOW` rule as quoted is unconditional in the `DESCRIPTION` flag entry but
   is qualified by `O_PATH` in the `ERRORS` list; a knowledge entry should not state it as absolute.

Registry fit (advisory for the L1/Scribe): `corpus/SOURCES.md` contains **no** row for
`https://man7.org/linux/man-pages/man2/open.2.html` (17 `man7.org` rows exist, none is this URL); the highest
existing id is `S319` and `grep -c -E '^\| S320 \|' corpus/SOURCES.md` → **0**, so the `S320` id is free.

---

## 5 — Files written by this seat

- `.ufo/waves/round-95/w1/ScoutS320/s320-recheck.md` (this file)
- `.ufo/waves/round-95/w1/ScoutS320/s320-open2-fetch1.html` — fetch 1 (76506 B, sha `d665489c…`)
- `.ufo/waves/round-95/w1/ScoutS320/s320-open2-fetch2.html` — fetch 2 (76506 B, sha `d665489c…`)
- `.ufo/waves/round-95/w1/ScoutS320/headers.txt` — response headers of the header-only fetch
- `.ufo/waves/round-95/w1/ScoutS320/scan.py` — tag-strip / normalise / locate script
- `.ufo/waves/round-95/w1/ScoutS320/scan2.py` — structural context script (headings, flag-term offsets)
- `.ufo/waves/round-95/w1/ScoutS320/words.py` — quote word/char counter
- `.ufo/waves/round-95/w1/ScoutS320/scan-fetch1.txt`, `scan-fetch2.txt`, `scan2-fetch1.txt` — script outputs

Scratch dir `/fast/scratch/hyaku/kaidoku-r95/ScoutS320` deleted after copying receipts into the seat directory.
No lane file outside this seat directory was created, edited or deleted; no mutating git/jj command was run in
the lane (`git rev-parse` / `git status` / `git ls-tree` only). No tool was installed or upgraded — `curl`,
`python3` and `sha256sum` were already present on this host.
