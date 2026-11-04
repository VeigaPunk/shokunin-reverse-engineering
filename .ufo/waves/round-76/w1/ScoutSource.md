# ScoutSource — r76/w1: the three source decisions behind the printed-command executor

Seat: ScoutSource (scout, leaf). Lane `kaidoku-shokunin`. Read-only: no registry, instrument or
corpus byte was edited by this seat.

Scope: per-page reconnaissance on (1) `shlex.split`, (2) `argparse`, (3) `sh(1)`; plus the
near-duplicate scan for their registry ids. Date 2026-11-04. One fresh GET per URL; bytes
retained under `.ufo/waves/round-76/w1/ScoutSource/`, digests in `receipt.json`.

**Verdict summary.**

| page | independent fetch | row state at audit | verdict |
|---|---|---|---|
| `shlex.split` (S286) | HTTP 200, 66 497 B, sha256 `4c1f8bf6…` | S286, `mined` | **BLOCKING**: `teaches` credits the page with the instrument's metacharacter refusal; `scope` asserts three negatives the page never states. Anchor quote and digest are correct. |
| `argparse` (S287) | HTTP 200, 334 994 B, sha256 `14d33eea…` | S287, `mined` | **BLOCKING**: the row grounds the before-arm's rc 2 in `error()`, but that rc 2 came from the round-75 probe's own `return 2`, not from argparse. Anchor quote and digest are correct. |
| `sh(1)` (S288) | **HTTP 404**, 196 B, sha256 `80c3fe2a…` | S288 re-scoped to `bash(1)`, `rejected` | **BLOCKING**: the located quote is a sentence that says the opposite ("do not undergo word splitting and pathname expansion") and is not in EXPANSION. The reject is right, for a different reason than the row gives. |

Both included rows reproduce byte-for-byte against my independent GET (same bytes, same sha256),
and the three snapshots in `.ufo/waves/round-76/l1/sources/` hash equal to mine. The defects are in
*wording and attribution*, not provenance.

---

## 1. `shlex.split` — https://docs.python.org/3/library/shlex.html#shlex.split

Snapshot: `shlex.html`, HTTP 200, 66 497 B, sha256
`4c1f8bf65662ed0a4cde315df6602cde5c103b34a1ede6ae2552c227fb745ee5`. Rendered-page line numbers.

### Located passages

| # | line(s) | exact text |
|---|---|---|
| X1 | 218 | `shlex — Simple lexical analysis` |
| X2 | 221-224 | "The shlex class makes it easy to write lexical analyzers for simple syntaxes resembling that of the Unix shell.  This will often be useful for writing minilanguages, (for example, in run control files for Python applications) or for parsing quoted strings." |
| X3 | 228 | `shlex.split(s, comments=False, posix=True)` (signature line of the entry) |
| X4 | 229 | "Split the string s using shell-like syntax." (the word `s` is `<em>s</em>`; composite, as S286 discloses) |
| X5 | 229-234 | "If comments is False (the default), the parsing of comments in the given string will be disabled (setting the commenters attribute of the shlex instance to the empty string).  This function operates in POSIX mode by default, but uses non-POSIX mode if the posix argument is false." |
| X6 | 236-237 | "Changed in version 3.12: Passing None for s argument now raises an exception, rather than reading sys.stdin." |
| X7 | 265-272 | Warning, under `quote()`: "The shlex module is only designed for Unix shells. The quote() function is not guaranteed to be correct on non-POSIX compliant shells or shells from other operating systems such as Windows. Executing commands quoted by this module on such shells can open up the possibility of a command injection vulnerability. Consider using functions that pass command arguments with lists such as subprocess.run() with shell=False." |
| X8 | 291 | "The quoting is compatible with UNIX shells and with split():" — under `quote()`, about *quoting* |
| X9 | 551-553 | "Runs of punctuation characters will be returned as a single token. However, note that no semantic validity checking will be performed: for example, ‘>>>’ could be returned as a token, even though it may not be recognised as such by shells." |
| X10 | 628-629 | "Of course, tokens will be returned which are not valid for shells, and you’ll need to implement your own error checks on the returned tokens." |
| X11 | 645-649 | example: input `'~/a && b-c --color=auto || d *.py?'` → `['~/a', '&&', 'b-c', '--color=auto', '||', 'd', '*.py?']` (tilde and glob text survive as literal tokens) |
| X12 | 658-659 | "(Note that posix=False is the default for shlex.)" — the **class** default, not `split`'s |

### What the gate actually relies on

`tools/round-76/plan-command.py:107` calls `shlex.split(joined)` with **no keyword arguments**, so
the gate relies on the documented defaults `comments=False, posix=True` (X3, X5). Two consequences
the page does state: comments are not parsed, so a `#` is data; POSIX mode governs quote and
backslash handling. The rest of the gate's safety is *not* shlex:

- `METACHARS = (";", "|", "&", "$(", "`", ">", "<")` and `UNBOUND_RE`/`VAR_RE` are checked in
  `static_defects` **before** the split (`plan-command.py:44, 84-103`), and `$REV/$WORK/$OUT/$ROOT`
  are substituted **after** the split (`:107-112`) — which is exactly why unbound variables are
  refused.
- The `\`-newline join is the instrument's own `command.replace("\\\n", " ")` (`:106`); the page
  says nothing about backslash-newline continuation for `split`.
- Execution is `subprocess.run(argv, cwd=root, env=env, ...)` with a list argv and the four-key
  child env (`:45, :162`); there is no shell object anywhere.

### What the row may claim

- The function's contract is `split(s, comments=False, posix=True)`; it splits a string into tokens
  "using shell-like syntax"; POSIX mode and comment suppression are the defaults (X3-X5).
- The module is a lexical analyser for "simple syntaxes resembling that of the Unix shell" (X2),
  and the page itself warns its tokens can be "not valid for shells" (X10) and that the module is
  "only designed for Unix shells" (X7).
- The page's own recommended execution shape is a **list argv with `shell=False`** (X7, 271-272).
  This is the strongest page-grounded sentence for a no-shell design — it is inside the `quote()`
  Warning, so the row must name it as such.
- By **example** (X11), `~` and `*` text is returned unexpanded by the tokeniser. Mark it as an
  example, not as a stated property.

### What the row may NOT claim (any of these is BLOCKING)

1. That `shlex.split` implements a shell grammar, or that its output is a shell command. The page
   says "shell-like" and explicitly disclaims shell validity (X4, X9, X10).
2. **That the page states it "performs no expansion, substitution or execution"** — the current
   `scope` cell. On the snapshot: `substitut` **0** hits, `glob` **0** hits, `expand` 1 hit (page
   chrome, line 71 `aria-expanded`), `exec` 2 hits, both in the `quote()` warning (269, 277). No
   sentence asserts those negatives.
3. **"so no shell metacharacter is ever interpreted"** — the current `teaches` cell. The page never
   uses "metacharacter"; the refusal is `static_defects`/`METACHARS` in the instrument. Credit the
   instrument, not S286.
4. That `shlex.split` handles the printed block's `\`-newline continuations (X-none; instrument
   does it).
5. That `posix=False` is the split default. X12 says `posix=False` is the default for the **class**
   `shlex.shlex`; `split`'s default is `posix=True` (X3). Citing X12 for `split` would invert the
   row.
6. That line 291 makes `split` "compatible with UNIX shells" — 291 is about `quote()` and about
   *quoting*; it even demonstrates `split` only as the inverse operation.

**Suggested repair (no page re-open needed):** keep X4 as the located quote; extend `anchor` with
X3 + X5 defaults and add "Consider using functions that pass command arguments with lists such as
subprocess.run() with shell=False." (271-272, `quote()` Warning); narrow `scope` to "shell-like
tokeniser, not a shell grammar; POSIX mode and comment suppression are the documented defaults";
replace the `teaches` clause with the list-argv/`shell=False` recommendation and attribute the
metacharacter refusal to `static_defects`.

---

## 2. `argparse` — https://docs.python.org/3/library/argparse.html

Snapshot: `argparse.html`, HTTP 200, 334 994 B, sha256
`14d33eea5257a16d679b390d6ecb2cb5529da1c2dd2b1ad15517a2f7f5784fb2`. Rendered-page line numbers.
The snapshot is the **Python 3.15.2** documentation (lines 20, 237); the lane's instrument runs on
Python 3.14.8 on this host.

### Located passages

| # | line(s) | exact text |
|---|---|---|
| A1 | 2401-2403 | `ArgumentParser.exit(status=0, message=None)` — "This method terminates the program, exiting with the specified status and, if given, it prints a message to sys.stderr before that." |
| A2 | 2404-2409 | "The user can override this method to handle these steps differently:" + `ErrorCatchingArgumentParser` example overriding `exit` |
| A3 | 2416-2418 | `ArgumentParser.error(message)` — "This method prints a usage message, including the message, to sys.stderr and terminates the program with a status code of 2." |
| A4 | 931-933 | `>>> parser.parse_args(['--foo', 'FOO'])` → `usage: PROG [-h] [-f FOO] bar` / `PROG: error: the following arguments are required: bar` |
| A5 | 1169-1171 | `parse_args([])` with `nargs='+'` → `PROG: error: the following arguments are required: foo` |
| A6 | 1374-1379 | `add_argument('--foo', required=True)`; `parse_args([])` → `: error: the following arguments are required: --foo` |
| A7 | 1382-1384 | "As the example shows, if an option is marked as required, parse_args() will report an error if that option is not present at the command line." |
| A8 | 1729-1736 | "The parse_args() method attempts to give errors whenever the user has clearly made a mistake…" (negatives are positionals, not options) |

### What the page documents, and what it only composes

- Documented in one sentence: **`error()` → status 2** (A3), and **`exit()` defaults to status 0**
  (A1), both overridable (A2). The page never prints the process exit status of any example.
- Documented per-hop: missing required option ⇒ `parse_args` "will report an error" (A7), and the
  examples show the report in `PROG: error: ...` form (A4-A6).
- **Not documented as one sentence:** "a missing required argument makes `parse_args` exit 2". That
  is a composition of A7 + A4-A6 + A3. It is defensible *if labelled as a composition*; it is not
  a quoted contract.
- The page's missing-argument text is **"the following arguments are required: …"** (A4-A6). It
  does not contain the string "missing required arguments".

### The before-arm's rc 2 does not come from argparse

Frozen receipt `.ufo/waves/round-76/pre/r75-printed-exec.txt`:

```
$ python3 -I -B tools/round-75/probe-mutation.py --root . --rev 538b8b81 --tool ... --expect-sole b-drop-canary-field
{"unevaluable": "missing required arguments: work"}
exit=2
```

`tools/round-75/probe-mutation.py:447-452` is the source of both the line and the status:

```
    missing = [name for name in ("rev", "tool", "patch_set", "work")
               if not getattr(args, name)]
    if missing:
        print(json.dumps({"unevaluable": "missing required arguments: "
                                          + ", ".join(missing)}))
        return 2
```

All probe options are optional (`--work` at `:433`, no `required=True` anywhere in `:429-441`), so
`argparse` accepted the invocation; there was no `error()` call and no argparse exit. Independent
host check (Python 3.14.8, in-memory, no files): a required positional produces exit **2** with
`PROG: error: the following arguments are required: work` — i.e. the documented wording, not the
receipt's wording.

So the row's `scope` tail ("the exit the round-75 printed command produced") and its `teaches`
cell ("Grounds the before-arm's observed exit … rc 2 is the documented outcome, not an instrument
quirk") are **factually wrong**: the receipt's rc 2 *is* an instrument quirk — the probe's own
`return 2`.

### What the row may claim

- `ArgumentParser.error(message)` prints a usage message plus message to stderr and terminates with
  status 2 (A3); `exit()` defaults to 0 (A1) and both are overridable (A2).
- `parse_args` reports an error for a missing required option (A7), shown in `PROG: error: the
  following arguments are required: …` form (A4-A6).
- **Composition, labelled as such:** a missing required argument takes the usage-error path, and
  that path's documented status is 2 (A4-A6 + A3).

### What the row may NOT claim (BLOCKING)

1. That the before-arm's rc 2 is argparse's documented exit. It is `probe-mutation.py:452`.
2. That "an invalid invocation" exits 2 without qualification: `exit(status=0)` is the default, and
   `-h` exits 0.
3. That the page documents the receipt's string "missing required arguments: work". That string is
   `probe-mutation.py:450`; the page's string is "the following arguments are required".
4. That the page's 3.15.2 wording is the 3.14.8 behaviour the instrument exhibits (version note
   needed, in the style of S266/S267's "Python 3.15.2" cells).

**Suggested repair:** keep A3 as the located quote; scope → "`ArgumentParser.error()` prints usage
and terminates with status 2 (default; overridable); `exit()` defaults to 0"; teaches → "grounds the
status-2 contract a usage error takes (`parse_args` reports required-argument errors, A7/A4-A6); not
the round-75 probe's rc 2, which is the probe's own `return 2`." Add the doc version.

---

## 3. `sh(1)` — https://man7.org/linux/man-pages/man1/sh.1.html

### The frozen URL does not exist

- HTTP **404**, 196 B, sha256 `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`.
  Body: `<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN"> … <h1>Not Found</h1> <p>The requested
  URL was not found on this server.</p>`.
- Reproduced with a browser User-Agent (same 404, 196 B), so it is not UA filtering.
- Nearest live pages, checked this round:

| URL | status | bytes | what it contains |
|---|---|---|---|
| `man1/sh.1p.html` (POSIX.1 `sh`, snapshot `sh1p.html`) | 200 | 78 700 | utility page only; `grep -c 'field splitting'` → **0**; expansions are cross-references to "Section 2.6.1/2.6.2/2.6.6" (lines 230, 284, 583) and "Chapter 2, Shell Command Language" (92, 404) |
| `man1/bash.1.html` (S288's substitute) | 200 | 497 852 | full bash semantics, incl. EXPANSION and Pipelines |
| `pubs.opengroup.org/…/utilities/sh.html` | 200 | 75 412 | POSIX utility page (same delegation to Chapter 2; not retained) |

Consequence: even a corrected `sh.1p` row could not quote word splitting or pipelines from that
page; the text lives in Chapter 2 (`V3_chap02.html`), a different page not opened this round.

### The S288 row's quote is inverted

S288 currently anchors on "EXPANSION, snapshot line 477; located quote: 'word splitting and
pathname expansion.  The shell'". In `bash.1.html`:

- EXPANSION **begins at line 1931**, not 477.
- Line 477 is inside the `[[ expression ]]` item of the compound-command list, and its sentence is:

```
477:              undergo word splitting and pathname expansion.  The shell
478:              performs tilde expansion, parameter and variable expansion,
479:              arithmetic expansion, command substitution, process
480:              substitution, and quote removal on those words.
```

with line 476 reading "The words between the [[ and ]] do not undergo …". The quoted fragment drops
both the subject and the negation, so the quote asserts the opposite of its sentence and of the
row's scope. **BLOCKING** as an anchor.

The scope the row declares *is* on the page, elsewhere:

| # | line(s) | exact text |
|---|---|---|
| B1 | 1932-1936 | "Expansion is performed on the command line after it has been split into words.  The shell performs these expansions: brace expansion, tilde expansion, parameter and variable expansion, command substitution, arithmetic expansion, word splitting, pathname expansion, and quote removal." |
| B2 | 1938-1941 | "The order of expansions is: brace expansion; tilde expansion, parameter and variable expansion, arithmetic expansion, and command substitution (done in a left-to-right fashion); word splitting; pathname expansion; and quote removal." |
| B3 | 350-352 | "A pipeline is a sequence of one or more commands separated by one of the control operators | or |&." |
| B4 | 476-480 | "The words between the [[ and ]] do not undergo word splitting and pathname expansion.  The shell performs tilde expansion, parameter and variable expansion, arithmetic expansion, command substitution, process substitution, and quote removal on those words." |

### Why the reject row is right, and what would flip it

Right, for these reasons (the row's stated reason — "the page cannot support the row's scope" — is
the wrong reason; the page does document the scope):

- The gate has **no shell consumer**: `grep -c 'shell=True' tools/round-76/plan-command.py` → 0;
  execution is a list-argv `subprocess.run(argv, cwd=root, env=env, ...)` (`:162`); the command is
  pre-screened against `; | & $( ` > <` (`:44, 84-103`); and the shlex page itself recommends
  `subprocess.run()` with `shell=False` (S286 X7). A shell manual therefore grounds nothing the
  gate does — only semantics it refuses.
- The plan's named page is a 404, so the row cannot be opened as written; the bash(1) substitute is
  a *different* shell's semantics, and bash is not POSIX `sh`.
- Its only legitimate use is as a counter-source naming the excluded semantics, which the lane
  already records better from the instrument side.

Flip (both clauses required):

1. the gate gains a shell path — a `/bin/sh -c` call or a shell fragment in the printed block — or
   a claim is made about shell word-splitting semantics; **and**
2. the anchor is re-pointed to B1/B2/B3 (and, for POSIX `sh`, to the Open Group Chapter 2 page,
   not bash(1)) with the 476-480 exemption kept as the counter-example.

---

## 4. Near-duplicate scan

Commands and results, run against the current `corpus/SOURCES.md` (318 lines before the concurrent
row write, 323 after):

```
$ grep -n 'shlex\|argparse\|man1/sh' corpus/SOURCES.md
202:| S286 | `shlex.split`, Python 3 standard library — https://docs.python.org/3/library/shlex.html#shlex.split …
203:| S287 | `argparse`, Python 3 standard library — https://docs.python.org/3/library/argparse.html …
$ grep -n 'man1/bash\|bash\.1' corpus/SOURCES.md
204:| S288 | `bash(1)`, Linux man-pages — https://man7.org/linux/man-pages/man1/bash.1.html …
$ grep -n 'S286\|S287\|S288' corpus/SOURCES.md
202, 203, 204                     # ids unique, one row each
$ grep -c 'docs\.python\.org' corpus/SOURCES.md
16                                # none of the other 14 is shlex or argparse
$ grep -n 'man-pages/man1' corpus/SOURCES.md
(no output)                       # no other section-1 man page is registered
```

Timing note for the L1: my first scan (before the rows landed) returned **no** hits for any of the
three ids or URLs; S286-S288 appeared concurrently at 06:44 while this seat was reading. So: no
collision existed before, and no duplicate exists now. The three rows are the only rows for these
pages; no sibling URL (`subprocess`, `os.path`, `re`) duplicates their scope.

## 5. Provenance

| artifact | HTTP | bytes | sha256 |
|---|---|---|---|
| `shlex.html` | 200 | 66 497 | `4c1f8bf65662ed0a4cde315df6602cde5c103b34a1ede6ae2552c227fb745ee5` |
| `argparse.html` | 200 | 334 994 | `14d33eea5257a16d679b390d6ecb2cb5529da1c2dd2b1ad15517a2f7f5784fb2` |
| `bash1.html` | 200 | 497 852 | `e35fa2966c44a4e9ee519760160f1aba14c670451a463177968ed2c4710bf846` |
| `sh1.html` | 404 | 196 | `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880` |
| `sh1p.html` | 200 | 78 700 | `f9a6d7d00b940e23e29b85fbbca9fbf8494c275eeed320c32e8cb694d3c7c583` |

The three snapshots already committed at `.ufo/waves/round-76/l1/sources/` hash to the same three
values as my independent GETs (`sha256sum` over that directory). The round-76 search-log entry
(line 233) records the `sh(1)` 404 as "196 B" and the bash(1) substitution — both reproduced.

## 6. Open unknowns

- The doc snapshots are Python **3.15.2** while the host instrument runs **3.14.8**. The page does
  not enumerate per-version exit-status changes; whether 3.14.8's `error()` path is byte-identical
  to the 3.15.2 page is inferred from the host probe, not from the page.
- The `sh(1)` 404 is observed from this host at this time (two UAs). Whether man7.org ever hosted
  `man1/sh.1.html` is not established; only that it does not now.
- The plan's own counting-command block and the C2 battery replay are out of this seat's scope
  (separate seats own them).
