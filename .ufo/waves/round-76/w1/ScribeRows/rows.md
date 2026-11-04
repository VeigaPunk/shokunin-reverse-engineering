# ScribeRows — round-76 source-row drafts: S286 shlex.split, S287 argparse, S288 sh(1) reject

Seat: ScribeRows (scribe). Date of work: 2026-11-04. Scope: fetch the three frozen pages
once each, draft the three registry rows in the 11-cell grammar, locate every quote in its
pinned snapshot, and check the drafts mechanically. `corpus/SOURCES.md` was NOT written.

## 1. Fresh-fetch facts

One content GET per URL, exactly as the seat spec names them:

```text
$ curl -sS -o <scratch>/shlex.html     -w '%{http_code} %{size_download}\n' 'https://docs.python.org/3/library/shlex.html#shlex.split'
200 66497
$ curl -sS -o <scratch>/argparse.html  -w '%{http_code} %{size_download}\n' 'https://docs.python.org/3/library/argparse.html'
200 334994
$ curl -sS -o <scratch>/sh1.html       -w '%{http_code} %{size_download}\n' 'https://man7.org/linux/man-pages/man1/sh.1.html'
404 196
```

Follow-up status-only probes (no body saved), disclosed because they repeat one URL:

```text
$ curl -sSI -o /dev/null -w '%{http_code} %{url_effective}\n' 'https://man7.org/linux/man-pages/man1/sh.1.html'
404 https://man7.org/linux/man-pages/man1/sh.1.html
$ curl -sSI -o /dev/null -w '%{http_code} %{url_effective}\n' 'https://man7.org/linux/man-pages/man1/sh.1p.html'
200 https://man7.org/linux/man-pages/man1/sh.1p.html
```

| page | HTTP | bytes | sha256 |
|---|---|---|---|
| shlex.html | 200 | 66 497 | `4c1f8bf65662ed0a4cde315df6602cde5c103b34a1ede6ae2552c227fb745ee5` |
| argparse.html | 200 | 334 994 | `14d33eea5257a16d679b390d6ecb2cb5529da1c2dd2b1ad15517a2f7f5784fb2` |
| sh1.html (404 body) | 404 | 196 | `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880` |

Both Python pages are the 3.15.2 documentation build and contain no `nonce` token
(`grep -c -i nonce` prints 0 for each), so a single-hash claim is sound for these bytes.

Independent corroboration: the L1 snapshots in `.ufo/waves/round-76/l1/sources/` are
byte-identical for `shlex.html` (`4c1f8bf6…`) and `argparse.html` (`14d33eea…`), so the two
digests rest on two independent GETs. That directory instead carries `bash.1.html`
(497 852 B, `e35fa296…`), consistent with the 404 recorded here.

## 2. Draft rows (verbatim)

```text
| S286 | `shlex.split`, Python 3 standard library — https://docs.python.org/3/library/shlex.html#shlex.split (snapshot and digest in `.ufo/waves/round-76/w1/ScribeRows/`) | docs | A | argv tokenisation without a shell: `shlex.split` splits a printed command into argv tokens using shell-like quoting, the parse the round-76 gate performs instead of handing the string to a shell; the page grounds the tokenisation contract, the no-shell property is the instrument's static grammar plus the consumer's `shell=True` count of 0; not the `shlex` class's stream configuration and not a claim that shell quoting equals shell semantics | Python 3.15.2 documentation snapshot; fetched 2026-11-04, HTTP 200, 66 497 bytes, sha256 `4c1f8bf65662ed0a4cde315df6602cde5c103b34a1ede6ae2552c227fb745ee5`; `shlex — Simple lexical analysis` (h1, line 218), `shlex.split` entry `dt` at lines 227-228, prose `dd` at line 229; located quote at line 229: "Split the string s using shell-like syntax." (7 words, composite: the served bytes read `Split the string <em>s</em> using shell-like syntax.`) | Grounds the gate's no-shell argv parse: the block is tokenised by `shlex.split`, so a shell metacharacter is a static refusal rather than an interpretation; the absent shell is checked, not assumed (`grep -c 'shell=True' tools/round-76/plan-command.py` prints 0). | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r76-plan-command-executability.md |
| S287 | `argparse`, Python 3 standard library — https://docs.python.org/3/library/argparse.html (snapshot and digest in `.ufo/waves/round-76/w1/ScribeRows/`) | docs | A | exit status 2 on a parser error: `ArgumentParser.error` prints a usage message including its message to `sys.stderr` and terminates with status 2, the documented outcome the round-75 printed command produced when a required argument was missing; not help (exits 0), not every failure path, and not shell exit-status translation | Python 3.15.2 documentation snapshot; fetched 2026-11-04, HTTP 200, 334 994 bytes, sha256 `14d33eea5257a16d679b390d6ecb2cb5529da1c2dd2b1ad15517a2f7f5784fb2`; `Exiting methods` (h3, line 2398), `ArgumentParser.error` entry `dt` at lines 2415-2416, prose `dd` at lines 2417-2418; located quote at lines 2417-2418: "This method prints a usage message, including the message, to sys.stderr and terminates the program with a status code of 2." (21 words, composite: `message` sits in an `em` span and `sys.stderr` in an `a` span; `ArgumentParser.exit(status=0, message=None)` at line 2400 is the exit primitive it routes through) | A missing required argument is a parser error, so rc 2 with `missing required arguments: work` is the documented outcome the C2 r75-argv arm expects, not an instrument quirk. | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r76-plan-command-executability.md |
| S288 | `sh(1)` shell manual — https://man7.org/linux/man-pages/man1/sh.1.html (the URL returns HTTP 404; snapshot in `.ufo/waves/round-76/w1/ScribeRows/`) | docs | C | The shell's word splitting, pathname expansion and pipelines — the semantics a no-shell executor must not inherit; not the gate's argv tokenisation (S286) and not its parser-error status (S287) | Requested content GET 2026-11-04 returned HTTP 404, 196 bytes, sha256 `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`; the saved body is the server's `404 Not Found` page, whose only sentence is at snapshot line 6: "The requested URL was not found on this server." (9 words); no `SYNOPSIS` or `DESCRIPTION` exists to locate; a later HEAD status probe of `man1/sh.1p.html` returned HTTP 200, but that different page was not fetched or screened | REJECTED: the whole point of the executability claim is the shell the gate refuses to invoke, so a shell manual cannot ground it, and at the named URL nothing is served (HTTP 404, 196 bytes); the operative shell-free fact is the instrument's static grammar plus the consumer search `grep -c 'shell=True' tools/round-76/plan-command.py`, which prints 0. Flip: the consumer acquires a shell dependency whose semantics it must cite (a `shell=True` occurrence), or a claim is made about shell word-splitting, quoting or exit-status semantics. | rejected | 2026-11-04 | on-release | — |
```

## 3. Located quotes and line spans

All line numbers are 1-based in the copied snapshot; each quote is a contiguous run in the
rendered text of the named lines. Quotes whose words cross inline tags are labelled
`composite` per QUALITY #42 at the point of writing, and the raw span is given.

- S286 — `shlex.html`, heading `shlex — Simple lexical analysis` (h1, line 218), entry
  `shlex.split` (`<dt>` lines 227-228), prose `<dd><p>` line 229. Quote at line 229:
  "Split the string s using shell-like syntax." (7 words; composite — the served bytes are
  `Split the string <em>s</em> using shell-like syntax.`).
- S287 — `argparse.html`, heading `Exiting methods` (h3, line 2398), entry
  `ArgumentParser.error` (`<dt>` lines 2415-2416), prose `<dd><p>` lines 2417-2418. Quote at
  lines 2417-2418: "This method prints a usage message, including the message, to sys.stderr
  and terminates the program with a status code of 2." (21 words; composite — `message` is in
  an `<em>` span, `sys.stderr` in an `<a>` span). The `ArgumentParser.exit(status=0,
  message=None)` entry (`<dt>` line 2400, prose lines 2402-2403) is the exit primitive the
  error path routes through; the status-2 sentence is on `error`.
- S288 — `sh1.html`, the 404 body: `<title>404 Not Found</title>` line 3, `<h1>Not Found</h1>`
  line 5, and the only sentence at line 6: "The requested URL was not found on this server."
  (9 words). The body has no `SYNOPSIS` or `DESCRIPTION`; there is nothing else to locate.

## 4. Mechanical checks (no production file touched)

`check-rows.py` (scratch) reported `FAILURES: 0` over: three rows present; 11 cells each;
no literal or escaped pipe in any cell; id/kind/tier/status/opened/recheck enums; each quote
contiguous in the rendered bytes of its stated lines; word counts 7 / 21 / 9, all <= 25; the
stated heading at the stated line; the pinned digest and byte count inside each anchor cell;
the entry `<dt>` at its stated line; the reject's `REJECTED: … Flip: …` with reason and flip
at least three words each and the consumer search named. Output: `check-rows.txt`.

Standing parser, run read-only against scratch fixtures (`validate --today 2026-11-04`):

| fixture | rc | findings |
|---|---|---|
| `HEAD:corpus/SOURCES.md` (no S286-S288) | 0 | 24 W04 warnings |
| same + these three drafts | 0 | 24 W04 warnings, no E-finding |
| worktree `corpus/SOURCES.md` (uncommitted S286-S288) | 0 | 24 W04 warnings |
| same + these three drafts | 1 | `E03 S286 duplicate id`, `E03 S287 duplicate id`, `E03 S288 duplicate id` (+ W04 for the two shared URLs) |

So the drafts are grammar-clean against the committed registry and cannot be appended beside
the uncommitted rows: the ids collide (section 6, conflict 1).

The consumer search required by the seat spec, verbatim (`consumer-search.txt`):

```text
$ grep -c 'shell=True' tools/round-76/plan-command.py
0
grep-exit=1

$ grep -n 'shlex.split' tools/round-76/plan-command.py
13:no shell (shlex.split) under a four-key child environment, and compares the
107:    argv = shlex.split(joined)

$ grep -n 'required=True' tools/round-76/plan-command.py
333:    ap.add_argument("--rev", required=True)
340:    ap.add_argument("--work", required=True)

$ grep -n 'subprocess.run' tools/round-76/plan-command.py
67:    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
162:    proc = subprocess.run(argv, cwd=root, env=env, capture_output=True,
321:        subprocess.run(["rm", "-rf", "--", work])
```

## 5. Draft Gate rows (for the round-76 lesson `## Gate`)

| source / decision | URL | accessed | located quote (<=25 words) | digestion |
|---|---|---|---|---|
| S286, `shlex.split`, admit (mined) | https://docs.python.org/3/library/shlex.html#shlex.split | 2026-11-04 | "Split the string s using shell-like syntax." (7 words; `shlex.split` entry, snapshot line 229; composite — `s` sits in an `em` span) | Grounds the gate's no-shell argv tokenisation: `tools/round-76/plan-command.py` builds argv with `shlex.split` (line 107) and refuses shell metacharacters statically; the consumer search `grep -c 'shell=True' tools/round-76/plan-command.py` prints 0 (grep exit 1). |
| S287, `argparse`, admit (mined) | https://docs.python.org/3/library/argparse.html | 2026-11-04 | "This method prints a usage message, including the message, to sys.stderr and terminates the program with a status code of 2." (21 words; `Exiting methods` h3 line 2398, `ArgumentParser.error` entry, snapshot lines 2417-2418; composite) | A missing required argument is a parser error, so the C2 r75-argv arm's rc 2 with `missing required arguments: work` is the documented contract; the consumer declares `--rev` and `--work` required (lines 333, 340). |
| S288, `sh(1)`, reject | https://man7.org/linux/man-pages/man1/sh.1.html (HTTP 404) | 2026-11-04 | "The requested URL was not found on this server." (9 words; 404 body line 6 — no `SYNOPSIS`/`DESCRIPTION` exists) | REJECTED: the executability claim's whole point is the shell the gate refuses to invoke, so a shell manual cannot ground it, and the frozen URL serves nothing (HTTP 404, 196 B). The operative shell-free fact is the instrument's static grammar plus the consumer search `grep -c 'shell=True' tools/round-76/plan-command.py`, which prints 0. Flip: the consumer acquires a shell dependency whose semantics it must cite (a `shell=True` occurrence), or a claim is made about shell word-splitting, quoting or exit-status semantics. |

## 6. Conflicts and findings (reported, not resolved)

1. **The frozen ids are already occupied in the worktree.** At HEAD
   `201df797d555d324ee2eb5e3c4b9bbe4fb77d85a` the registry's highest id is S285; the worktree
   (` M corpus/SOURCES.md`, sha256 `dde75e6e…`, 225 314 B) adds three uncommitted rows,
   `git blame` = "Not Committed Yet", at lines 202-204: S286 `shlex.split` (mined), S287
   `argparse` (mined), S288 `bash(1)` (rejected). This seat's drafts use the frozen ids and
   therefore cannot be appended without `E03`; the mechanical proof is
   `census-worktree-diff.txt`. The two mined rows and this seat's drafts agree on URL, tier,
   status, `opened`, `recheck` and `used-by`.
2. **S288 source substitution.** The frozen seat spec names
   `https://man7.org/linux/man-pages/man1/sh.1.html`; the uncommitted row instead rejects
   `bash(1)` at `https://man7.org/linux/man-pages/man1/bash.1.html` (497 852 B, sha256
   `e35fa2966c44a4e9ee519760160f1aba14c670451a463177968ed2c4710bf846`), noting "the round plan
   named `sh(1)`, which 404s on this host". Both rows reject for the same reason; only the
   source URL and quote differ, and only one may land under S288. This seat kept the frozen
   URL and records the 404 as the page's disposition, with the same flip.
3. **Tag name in the uncommitted S286 anchor.** It says "the word `s` sits inside a `<var>`
   tag". The served byte at line 229 is `<em>s</em>`; there is no `<var>` on that line or in
   the entry. This draft names `em`.
4. **S287 quote span.** The uncommitted row quotes "terminates the program with a status code
   of 2." at "snapshot line 2418" — a contiguous mid-sentence fragment. This draft quotes the
   whole sentence across lines 2417-2418, so the subject and the `sys.stderr` destination are
   inside the quote.
5. **Rejected-row cadence.** The uncommitted S288 uses `180d`; this draft uses `on-release`
   (the round-75 rejected-row convention). Both pass E09; the difference is a convention
   choice for the landing, not a defect.

## 7. Evidence inventory (under `ScribeRows/`)

- `shlex.html` — 66 497 B, `4c1f8bf6…`
- `argparse.html` — 334 994 B, `14d33eea…`
- `sh1.html` — 196 B, `80c3fe2a…` (the 404 body)
- `sha256sums.txt`, `http-status` facts in section 1
- `rows-draft.md` — the three rows verbatim (the file the draft block above is generated from)
- `consumer-search.txt` — the required grep and the corroborating line numbers, verbatim
- `check-rows.txt` — the row checker, `FAILURES: 0`
- `check-rows.py`, `run-census.sh` — the drivers that produced the transcripts; both carry
  the now-deleted scratch path and are kept for re-derivation
- `census-head-baseline.txt`, `census-head-with-rows.txt`, `census-head-diff.txt`
- `census-worktree-baseline.txt`, `census-worktree-with-rows.txt`, `census-worktree-diff.txt`,
  `census-e03.txt`, `census-exits.txt`
- `receipt.json` — digests, quote-to-snapshot line mapping, check results
- `rows.md` — this file

## Limits

- One content GET per URL; the `sh(1)` URL also received one status-only HEAD (disclosed).
  The 404 is a host/URL observation on 2026-11-04, not a negative about `sh(1)` elsewhere.
  `man1/sh.1p.html` answered a HEAD with 200 but was not fetched or screened.
- The Python pages may drift between documentation builds; only the pinned bytes are claimed.
  No per-request nonce is present in either page.
- The census was run against scratch fixtures that symlink the lane's trees; the fleet census
  over the real lane is the L1's step. No production file was edited.
- The uncommitted worktree rows are another seat's in-flight work; this report records them
  but does not modify or republish them.
