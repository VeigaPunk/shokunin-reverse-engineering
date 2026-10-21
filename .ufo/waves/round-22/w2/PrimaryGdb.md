# PrimaryGdb — GDB/MI console semantics, primary source (round 22 W2 recovery)

Seat: `KaidokuR22R.PrimaryGdb-6`. Leaf scout, author-side only, not outside admission.
This is new evidence from W2, not a returned W1 seat. Lane files were read only; this report and `PrimaryGdb.json` are the only writes.

## Verdict

The source is **accessible**. It gives bounded primary-source support for what GDB/MI console *output semantics* are: `~` stream records carry the textual responses to CLI commands, and `-interpreter-exec console` is the documented MI way to run a CLI command.
It gives **no** support for kaidoku *ownership* of gdb or dynamic analysis. PROVINCE.md:103-105 keeps "Non-REA dynamic analysis — gdb scripting ... `(unowned)`. gdb stays a fallback reader for supplied cores, not a lane-run tracer", and claims.json `not_claimed` keeps "dynamic-analysis ownership (kaidoku/revenger overlap stays open)". Nothing on these pages changes either statement.

## Quote (one contiguous passage, 23 words)

> "The console output stream contains text that should be displayed in the CLI console window.  It contains the textual responses to CLI commands."

- Heading: **27.5.2 GDB/MI Stream Records** (under 27.5 GDB/MI Output Records, chapter 27 The GDB/MI Interface), *Debugging with GDB*, Tenth Edition, for GDB Version 19.0.50.20261021-git.
- URL: https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI-Stream-Records.html
- Date: HTTP `Last-Modified: Wed, 21 Oct 2026 02:07:24 GMT`. Fetched at `Date: Wed, 21 Oct 2026 13:03:12 GMT`.
- sha256 of the fetched page: `b1202500c0b9ed3bf42c614851fc8ceba436bde9d90b3d409e2f265afa6b113b` (5091 bytes).

The assigned URL, `GDB_002fMI.html` (chapter 27 top), returned 200 but is only a table of contents plus "Function and Purpose" and "Notation". It has **no console-semantics text**. The quote comes from the child node that page links to through 27.5. I record this so nobody cites the chapter-top URL as the anchor.

## Corroborating facts from the same manual (observed, paraphrased; not counted as the quote)

- **27.2.2 GDB/MI Output Syntax**: the grammar is `console-stream-output → "~" c-string nl`. The prose says console output "should be displayed as is in the console. It is the textual response to a CLI command." Output is zero or more out-of-band records, then an optional result record, ended by `(gdb)`.
- **27.5.2**: `@` is target output, "only present when GDB's event loop is truly asynchronous, which is currently only the case for remote targets". `&` is the log stream, which carries GDB-internal debugging messages.
- **27.3 GDB/MI Compatibility with CLI**: raw CLI input works in MI, "but there may be some unexpected behavior". Query commands auto-answer yes, breakpoint command lists are not executed, and `if`, `when` and `define` (verbatim page text) prompt with `>`, which is not valid MI. The page recommends `-interpreter-exec` (see the next item).
- **GDB/MI Miscellaneous Commands, "The -interpreter-exec Command"**: synopsis `-interpreter-exec interpreter command`, "Execute the specified command in the given interpreter". The example `-interpreter-exec console "break main"` emits `&` log lines, one `~"Breakpoint 1 at ..."` line and `^done`.
- **Chapter 27 top**: "GDB/MI is still under construction, so some of the features described below are incomplete and subject to change".

## Unsupported inferences (do not draw these from this source)

1. **Ownership or a coverage claim.** The manual describes GDB, not REA or kaidoku. It cannot move gdb or dynamic analysis from `(unowned)` to owned, and it cannot settle the kaidoku/revenger overlap.
2. **R22-C1 counting.** C1 counts a T1 verb only with executed, retained, bound REA Evidence. A documentation row is not Evidence for `debug-with-gdb`. It can only back the semantics sentence of a knowledge entry that separately cites such Evidence (the C1 `sourced` field needs an S### row opened in round 22, so this row MAY serve as that citation). It adds 0 to `t1_exercised_count` on its own.
3. **REA behavior.** REA 6.5.0's own text (`.ufo/waves/luna-round-2/receipts/L14-llms-6.5.0.txt:33`: "Run one unrestricted GDB console command in an ephemeral MI session") is REA's claim. GDB's manual does not confirm that REA uses `-interpreter-exec console`, how REA parses `~`/`&`/`@`, or REA's safety and detach behavior around the inferior TTY. Those need REA Evidence or REA source.
4. **Inferior stdout appears as console output.** This is not supported. `~` is GDB's CLI response text. Program output is `@`, and only on asynchronous remote targets, so local inferior output is not promised in any MI stream.
5. **Version applicability.** The page documents development GDB 19.0.50.20261021-git (`/current/` tracks trunk). The host has `GNU gdb (GDB) 18.1`. That 18.1 behaves identically is `[INFERENCE]`, unverified. The page's "under construction ... subject to change" caveat also limits durability.
6. **Completeness or exclusivity of console output.** The manual does not say that every CLI response goes only to `~`. The `-interpreter-exec` example itself shows `&` lines mixed in.

## Drafted registry row (candidate for L1; the source was accessible)

No `sourceware.org/gdb` row exists in `corpus/SOURCES.md`; the highest id at read time was S053. L1 assigns the id.

```
| S0NN | GDB manual, GDB/MI Stream Records — https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI-Stream-Records.html | docs | A | Documented GDB/MI console (`~`), target (`@`) and log (`&`) stream semantics and `-interpreter-exec console` as the recommended CLI path; not REA's parsing, not host gdb 18.1 behavior, not ownership of dynamic analysis | Debugging with GDB, Tenth Edition, GDB 19.0.50.20261021-git; 27.5.2 GDB/MI Stream Records (Last-Modified 2026-10-21T02:07:24Z, sha256 `b1202500c0b9ed3bf42c614851fc8ceba436bde9d90b3d409e2f265afa6b113b`); cross-ref 27.2.2 Output Syntax, 27.3 Compatibility with CLI, -interpreter-exec | Console stream records carry GDB's textual CLI responses; inferior output is a separate `@` stream present only on async remote targets, so a console-command result is not a capture of the program's output. | mined | 2026-10-21 | 90d | (L1 to fill) |
```

## Commands and observed exits (cwd `/tmp`, curl/python3/sha256sum; no installs)

| argv | exit | observed |
|---|---|---|
| `curl -sS -L -o gdbmi_top.html -w '%{http_code} %{size_download} %{url_effective}\n' https://sourceware.org/gdb/current/onlinedocs/gdb.html/GDB_002fMI.html` | 0 | `200 16162 <same url>`, stderr empty |
| `curl -sS -L -o gdbmi_<P>.html ... /<P>.html` for P in GDB_002fMI-Stream-Records, -Output-Records, -Compatibility-with-CLI, -Miscellaneous-Commands, -Output-Syntax, index | 0 each | 200 with 5091, 5224, 4426, 29083, 10263, 113565 bytes |
| `curl -sSI .../GDB_002fMI.html \| grep -iE 'last-modified\|date\|etag'` | 0 | `date: Wed, 21 Oct 2026 13:03:12 GMT`, `last-modified: Wed, 21 Oct 2026 02:07:24 GMT`, `etag: "3f22-65e5035408354"` |
| `curl -sSI .../GDB_002fMI-Stream-Records.html \| grep -iE 'last-modified\|^date'` | 0 | same date and Last-Modified |
| `python3` HTML-to-text extraction (inline heredoc) | 0 | text quoted above; index: "This is the Tenth Edition, for GDB (GDB) Version 19.0.50.20261021-git." |
| `sha256sum gdbmi_*.html` | 0 | see `PrimaryGdb.json` |
| `command -v gdb && gdb --version \| head -1` | 0 | `/usr/bin/gdb`, `GNU gdb (GDB) 18.1` (version string only; no target, no attach) |

Lane reads: `PROVINCE.md:62,103-105`, `claims.json` (whole file, 40 lines), `corpus/SOURCES.md` header and ids, `L14-llms-6.5.0.txt:33`.
Not done: REA invocations (none were needed), target execution, debug attach, account or config inspection, installs (tooling: none installed or updated), pacman.

## Blockers

None. The only caveat is that the assigned chapter-top URL lacks the semantics, so the anchor is its 27.5.2 child page.
