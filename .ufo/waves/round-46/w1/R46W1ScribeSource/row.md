# S142 — row and Gate block (seat R46W1ScribeSource)

Opened live 2026-10-28. Source: `https://git-scm.com/docs/git-log`. Everything below was
read from the saved copy at
`$S/git-log.html` (`S=/fast/scratch/hyaku/kaidoku-r46/R46W1ScribeSource`, removed after
the receipts were copied here). The page is **not** in the lane tree; the digest is the pin.

## Registry row (11 columns, paste-ready)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S142 | git-log documentation — https://git-scm.com/docs/git-log | docs | A | the `--diff-merges=<format>` format set of git-log, in particular the `first-parent` value, which is the diff arm a freeze gate needs to see a merge's own resolution edit | Page fetched 2026-10-28 (HTTP 200, 375,834 bytes, sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`, byte-identical on two fetches); anchors `#Documentation/git-log.txt---diff-mergesformat` (the format list) and `#Documentation/git-log.txt-first-parent` (the value) | `--diff-merges=first-parent` emits one diff per merge, taken with respect to the first parent in the same shape `--patch` gives a non-merge commit, so a gate can read a merge's resolution edit that a plain `git log --name-status` omits. | mined | 2026-10-28 | on-release | corpus/lessons/round-46.md |

Row line on its own, for a verbatim paste into `corpus/SOURCES.md`:

```
| S142 | git-log documentation — https://git-scm.com/docs/git-log | docs | A | the `--diff-merges=<format>` format set of git-log, in particular the `first-parent` value, which is the diff arm a freeze gate needs to see a merge's own resolution edit | Page fetched 2026-10-28 (HTTP 200, 375,834 bytes, sha256 `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`, byte-identical on two fetches); anchors `#Documentation/git-log.txt---diff-mergesformat` (the format list) and `#Documentation/git-log.txt-first-parent` (the value) | `--diff-merges=first-parent` emits one diff per merge, taken with respect to the first parent in the same shape `--patch` gives a non-merge commit, so a gate can read a merge's resolution edit that a plain `git log --name-status` omits. | mined | 2026-10-28 | on-release | corpus/lessons/round-46.md |
```

Cell count: 11 (checked mechanically, see R6 below).

## Gate block (3 lines)

- **URL**: https://git-scm.com/docs/git-log
- **Access**: 2026-10-28T16:58:01Z (HTTP 200, 375,834 bytes, sha256
  `0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`); re-fetched
  2026-10-28T16:59:05Z, HTTP 200, 375,834 bytes, same sha256, `cmp` exit 0.
- **Quote**: "Show full diff with respect to first parent. This is the same format as
  --patch produces for non-merge commits." — 19 whitespace-delimited words; anchor
  `--diff-merges=<format>` (`#Documentation/git-log.txt---diff-mergesformat`), value
  `first-parent` (`#Documentation/git-log.txt-first-parent`).

## Presence proof (the quote is in the saved copy)

The sentence is not contiguous in the raw HTML: it wraps after "same", and `--patch` sits
inside its own `<span>`. So the proof is (a) a raw-byte check of the first clause and (b) a
tag-stripped, whitespace-normalised literal-substring check of the whole quote.

```
$ grep -c 'Show full diff with respect to first parent\.' git-log.html
1
```

```
$ python3 - <<'PY'
import re,html
raw=open('git-log.html',encoding='utf-8').read()
flat=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',raw)))
q="Show full diff with respect to first parent. This is the same format as --patch produces for non-merge commits."
print(raw.count('\n',0,raw.find(q.split('. ')[0]))+1, len(q.split()), q in flat)
PY
6072 19 True
```

Raw offsets in the saved copy (byte offset, 1-based line):

| item | offset | line |
|---|---|---|
| `id="Documentation/git-log.txt---diff-mergesformat"` (the section) | 253596 | 6043 |
| `id="Documentation/git-log.txt-first-parent"` (the value anchor) | 255613 | 6069 |
| `Show full diff with respect to first parent.` | 256017 | 6072 |

Surrounding raw bytes, verbatim:

```
is\'><code>1</code></span> </dt>
<dd>
<p>Show full diff with respect to first parent. This is the same
format as <span class=\'synopsis\'><code>--patch</code></span> produces for non-merge commits.</p>
</dd>
```

## What the page actually supports — and what it does not

- The `--diff-merges=<format>` entry opens: "Specify diff format to be used for merge
  commits. Default is `off` unless `--first-parent` is in use, in which case `first-parent`
  is the default." The value list is `off`/`none`, `on`/`m`, `first-parent`/`1`,
  `separate`, `combined`/`c`, `dense-combined`/`cc`, `remerge`/`r`.
- `first-parent` and `1` share one definition (`<dt>` pair, one `<dd>`): the quoted
  sentence. So `1` is an accepted synonym.
- The page does **not** say "only". `first parent only` and `first-parent only` occur 0
  times in the page text; "only the first parent" occurs twice, both about the unrelated
  traversal option `--first-parent` ("When finding commits to include, follow only the
  first parent commit upon seeing a merge commit") and `--exclude-first-parent-only`. The
  "one diff, first-parent side" reading is **inference from the value name plus the
  `--patch`-shape sentence**, not a quotation. [INFERENCE]
- `-m` is documented as "similar to `--diff-merges=on`… will produce no output unless `-p`
  is given as well"; `on` resolves through `log.diffMerges`, whose documented default is
  `separate`. `--first-parent` (traversal) additionally "changes default diff format for
  merge commits to `first-parent`".

## Behaviour probe (fixture repo, one merge with a hand resolution)

`$S/arm_probe.sh` — fixture `git -C "$D" init`, toplevel asserted equal to `$D`; merge
`a05988037ecf09f016a042da887ac1dc7e405d15` (parents `3158ad31…`, `43750641…`) resolves
`f.txt` to bytes neither parent has. Exit 0, stdout sha256
`15fa2dc8f0a42aeddad5003241e5a73d0f4281f5f8d468e0ea9ce925ae369ed3`, 2026-10-28T17:00:00Z.

| arm | command tail | seen for the merge |
|---|---|---|
| plain | `git log --name-status -1` | no file entry at all |
| documented value | `--diff-merges=first-parent --name-status` | one entry, `M f.txt` |
| `-m` only | `-m --name-status` | **two** entries (default `separate`), `M f.txt` twice |
| reversed order | `--diff-merges=first-parent -m --name-status` | **two** entries — identical to `-m` only |
| gate.py's order | `-m --diff-merges=first-parent --name-status -z` | one block, `M \0 f.txt \0` |

Consequences, stated not claimed: the value does what the sentence says; `-m` alone does
not narrow to the first parent; **the last of the two options wins**, so the arm's meaning
depends on `-m` preceding `--diff-merges=first-parent`, which is the order in
`tools/round-46/gate.py:99`. Nothing in the frozen instrument pins that order.

## Receipts

| # | command | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| R1 | `curl -sS -o git-log.html -w 'http_status=%{http_code} bytes=%{size_download} time=%{time_total}\n' https://git-scm.com/docs/git-log` | 0 | not saved to a file; live output `http_status=200 bytes=375834 time=0.063435` | 2026-10-28T16:58:01Z |
| R2 | same `curl` into `git-log.2.html`; then `sha256sum` both and `cmp -s` | 0 | `7d013c4e07cc13dd58eede2af2fa8554a62236c8d5112f8a49892d81393fc365`; both files `0a73e33b…`, `cmp` 0 | 2026-10-28T16:59:05Z |
| R3 | tag-strip + whitespace-normalise substring check (python3, above) → `receipts/quote.out`; plus `grep -c 'Show full diff with respect to first parent\.' git-log.html` | 0 | `ee479bc315d7a85f9d2677d088632fdc6aaf488a8497fad0bf61e9ffbea5e266`; grep printed `1` (`5593c04e…`, R5) | 2026-10-28T16:59:05Z |
| R4 | `bash $S/arm_probe.sh $S` | 0 | `15fa2dc8f0a42aeddad5003241e5a73d0f4281f5f8d468e0ea9ce925ae369ed3` | 2026-10-28T17:00:00Z |
| R5 | `grep -c 'Show full diff with respect to first parent\.' git-log.html > receipts/grep_raw.out` | 0 | `5593c04ed7710e53821c84ed5d6badf85833649205d0369308d89af7066d246b` (prints `1`) | 2026-10-28T17:00:36Z |
| R6 | `awk -F'\|' '/^\| S142 \|/{print "cells="NF-2}' row.md` \| `sort -u` | 0 | `4a599f405a50cdd002e8de2c39dd5c75152da29f972659f0f74961aa644c1b97` (prints `cells=11`) | 2026-10-28T17:00:36Z |

Both fetched files hashed to
`0a73e33b235368af3021b6dc7dbca11ca4b513157ac651acf548d94e1a5c4a1a`, `cmp` exit 0 — two
independent fetches, identical bytes, so the size/sha256 pair in the row is reproducible
and not a single-sample artefact.

Raw captures for R2–R6 are retained beside this file in `receipts/` (`quote.out`,
`grep_raw.out`, `cells.out`, `fetch2.out`, `sha2.out`, `arm_probe.out`, `index.tsv`) with
`arm_probe.sh`, the script that built the fixture. The 375,834-byte page is deliberately
not retained: the digest is the pin, and a live re-fetch is the recheck.
