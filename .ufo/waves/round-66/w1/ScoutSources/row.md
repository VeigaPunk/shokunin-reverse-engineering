# S267 — drafted registry row (round 66, not landed)

Eleven-column shape of `corpus/SOURCES.md`; no cell holds a pipe. Drafted, not appended: this seat writes only
inside its own report directory.

| S267 | CPython 3 documentation, The Python Standard Library, `sys.dont_write_bytecode` (Python 3.15.2) — https://docs.python.org/3/library/sys.html | docs | A | The `sys.dont_write_bytecode` attribute's own stated semantics — no attempt to write `.pyc` files on the import of source modules, an initial value set from the `-B` command line option and the `PYTHONDONTWRITEBYTECODE` environment variable, and a value a program may set itself; the page round 65 recorded as a rejected alternative for the S266 switch anchor, opened here under its own scope; not cache content and not an emptiness guarantee | `sys.dont_write_bytecode` `<dt>` raw line 585; definition `<dd><p>` raw lines 587-591 (bytes 49838-50767); quote bytes 50024-50697; nearest preceding heading h1 `sys — System-specific parameters and functions` (`#module-sys`, raw line 206); snapshot sha256 `572c354eb01e5121f7beb3084408fc7ecbc465accf3a3335f1182c7df3648f7e`, 280617 bytes, opened 2026-11-03 | Read the attribute as a statement about an attempt, not about a directory — its initial value comes from `-B` or the environment variable and a program may assign it, so a cache-free probe pins one lever and still censuses the tree instead of inferring emptiness from the flag | queued | 2026-11-03 | 90d | — |

## Gate

- **URL**: `https://docs.python.org/3/library/sys.html`
- **Access date**: 2026-11-03 (local); captured instant `2026-11-04T00:16:22Z` UTC. One body fetch, `curl -fsSL -o`,
  HTTP 200, 280617 bytes, sha256 `572c354eb01e5121f7beb3084408fc7ecbc465accf3a3335f1182c7df3648f7e`.
  Document title pins the served version: `sys — System-specific parameters and functions — Python 3.15.2 documentation`
  (raw line 20).
- **Locator**: nearest preceding heading is **h1** `sys — System-specific parameters and functions`
  (`#module-sys`, raw line 206, byte 10286). The page body carries no h2; the eight h3/h4 in the file are page
  chrome (`Navigation`, `This page`, `Previous topic`, `Next topic`), four before the h1 (raw lines 103-145) and four
  after the article (raw lines 2945-2990).
  The definition is `<dt class="sig sig-object py" id="sys.dont_write_bytecode">` at raw line 585 (byte 49551);
  its `<dd><p>` runs raw lines 587-591, bytes 49838-50767.
- **Quote (Gate, 18 words, contiguous rendered text, `composite` — words cross `<code>`/`<a>` markup on raw lines
  588-590; bytes 50024-50697; one occurrence in the page's rendered text)**:

  > initially set to True or False depending on the -B command line option and the PYTHONDONTWRITEBYTECODE environment variable

- **Source sentence naming the variable, 32 words verbatim (context only — over the 25-word Gate cap)**:

  > This value is initially set to True or False depending on the -B command line option and the PYTHONDONTWRITEBYTECODE environment variable, but you can set it yourself to control bytecode file generation.

- **Attribute sentence, 17 words verbatim**:

  > If this is true, Python won’t try to write .pyc files on the import of source modules.

- **Kind / tier**: `docs`; tier **A** under the fleet `CORPUS.md` tier category *official docs* — "primary or
  authoritative for that scope (spec, official docs, source code, original paper, maintainer statement, the lane's own
  re-runnable gate output)". Coverage-map ground served: `.jsc` route under a complete closure (round 65)
  (`corpus/README.md:76`), whose R66-C1 counter runs this interpreter.
- **Status note (not a cell)**: drafted `queued` with `used-by —` so the census is clean at the base, where the C1
  knowledge entry does not exist yet. Flip to `mined` — logged old→new in `corpus/lessons/round-66.md`, append-only —
  when that entry cites `S267` in its `source:` line.
