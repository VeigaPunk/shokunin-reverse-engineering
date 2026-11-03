# S266 gate — CPython `-B` option

| field | value |
|---|---|
| URL opened | https://docs.python.org/3/using/cmdline.html |
| access date | 2026-11-03 |
| fetch time (UTC) | 2026-11-03T23:26:03Z (response `date` header, identical to local clock read) |
| HTTP status / protocol | 200, HTTP/2 |
| document title | `1. Command line and environment — Python 3.15.2 documentation` (raw line 20) |
| bytes | 171073 |
| sha256 | `96f87232f979982bd2aa268510c9c89b57186f0f3802840aafa7de1a7537810f` |
| lines | 1922, LF only, no BOM, no Content-Encoding (body bytes == Content-Length) |
| repeatability aids | `last-modified: Tue, 03 Nov 2026 17:54:14 GMT`, `etag: "6aea1fc6-29c41"` |

## Exact quote

> If given, Python won’t try to write .pyc files on the import of source modules.

- 15 words, one sentence, one contiguous passage.
- Line: **raw line 474** (sentence continues on raw line 475). Raw byte span 36131–36287.
- The apostrophe is U+2019 (`\xe2\x80\x99`) in the fetched bytes, not ASCII `'`.
- Raw-markup note: the rendered sentence is contiguous, but the raw bytes wrap `.pyc` in
  `<code class="docutils literal notranslate"><span class="pre">.pyc</span></code>` (four inline tags), so the quote is not a
  single raw-byte substring. Recorded so a re-check compares rendered text, not raw splicing.
- Nearest heading containing it: **h3 `1.1.3. Miscellaneous options`** (id `using-on-misc-options`, raw line 451); the
  option definition itself is `<dt ... id="cmdoption-B">` at raw line 472. Containing chain: h2 `1.1. Command line`
  (line 233) in h1 `Command line and environment` (line 225).

## Page choice

Both named pages were fetched in the same run. `sys.html` (200, 280617 bytes,
sha256 `572c354eb01e5121f7beb3084408fc7ecbc465accf3a3335f1182c7df3648f7e`) documents `sys.dont_write_bytecode` at raw
line 585 with the same core sentence, but its nearest containing heading is only the module-level h1 `sys —
System-specific parameters and functions` (line 206), and its text defines the attribute as *initially set* from `-B`
and `PYTHONDONTWRITEBYTECODE` — a derived setting, not the switch. `cmdline.html` was chosen because the quoted
passage is the switch's own definition and sits under a named section heading, giving a clearer anchor. The rejected
page is recorded in `fetch.json` (`rejected_alternative`) rather than discarded.

## Admissibility (tier A, status mined)

- First-party CPython documentation on the official `docs.python.org` host, `content-type: text/html`, no redirect to
  a third party; version-pinned in the title (`Python 3.15.2`).
- Scope declared is the switch's stated effect only. The quote is used for exactly one proposition: with `-B`, the
  interpreter does not try to write `.pyc` files on import of source modules.
- 15 words, `<= 25`; contiguous; located by raw line and byte span; heading named.
- No `|` in any row cell; row written with 11 columns per the header at `CORPUS.md:86` into the lane registry
  `kaidoku-shokunin/corpus/SOURCES.md` (the fleet-root `CORPUS.md` is contract text and was not written).
- Row shape checked against the lane's own census: on a scratch copy of `corpus/SOURCES.md` with this row appended,
  `NF!=13` malformed rows print 0 and duplicate ids print nothing. The `used-by` census prints exactly one
  `missing:` line, because the cited knowledge note does not exist yet — recorded, not hidden (see report finding 5).

## Limit — what the page does NOT establish

- Nothing about V8, Node, Electron, `.jsc` files or code caches. V8 code caches are a different mechanism from CPython
  `.pyc` files; this page cannot ground any claim about View8's output, its determinism, or whether View8/Python
  wrappers around it write caches.
- Nothing about whether a *child* process inherits `-B`: it documents the switch, not propagation. A cache-free claim
  therefore needs per-invocation evidence for each interpreter actually spawned.
- Nothing about writes performed by non-Python tools or by an embedded interpreter whose start-up is not the
  documented command line (e.g. `Py_Initialize` embedding, where `sys.dont_write_bytecode` is the lever, not `-B`).
- Nothing about the filesystem: no statement that a cache is absent — only that the interpreter will not try to
  write one. Absence remains an observation to be taken (the closure matrix's own census), not an inference from
  this page.
- Wording is version-agnostic in substance but the snapshot is 3.15.2; recheck at 90d or on a docs release, since the
  page ships with the documentation version.

## Provenance of this gate

Commands run (scratch `/fast/scratch/hyaku/kaidoku-r65/ScribeSources`, deleted after writing these files):

```
curl -sS -D h1.txt -o cmdline.html -w '%{http_code} %{size_download}\n' --max-time 60 https://docs.python.org/3/using/cmdline.html
curl -sS -D h2.txt -o sys.html     -w '%{http_code} %{size_download}\n' --max-time 60 https://docs.python.org/3/library/sys.html
sha256sum cmdline.html sys.html
```

Exit code 0 for both; reported sizes 171073 and 280617 match `wc -c` and `content-length`. No second fetch was made, so
byte stability across fetches is **not** claimed; `etag`/`last-modified` are given so a later re-check can detect drift.
