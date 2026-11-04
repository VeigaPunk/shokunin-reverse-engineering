# ScoutSources — gate record for S267 (round 66, wave w1)

Source: `https://docs.python.org/3/library/sys.html`, entry `sys.dont_write_bytecode`.
Snapshot: 280617 bytes, 3071 lines, LF only, no BOM, sha256
`572c354eb01e5121f7beb3084408fc7ecbc465accf3a3335f1182c7df3648f7e`, HTTP 200, captured
2026-11-04T00:16:22Z UTC (= access date 2026-11-03 local). One body fetch; no second request was made.

## Gates

| gate | result | evidence |
|---|---|---|
| Row id free | `S267` occurs 0 times in `corpus/SOURCES.md`; highest present id `S266` | `grep -c 'S267' corpus/SOURCES.md` → 0; `grep -oE '^\|[[:space:]]*S[0-9]{3,}'` sorted → … S265, S266 |
| Schema shape | drafted line parses to **11 cells** | `awk -F'\|' '/^\| S267/' row.md` → `NF=13`; 12 pipes (leading, 10 separators, trailing); no cell holds a pipe |
| Quote length | Gate quote **18 words** ≤ 25 | rendered fragment split → 18 |
| Quote contiguity / label | contiguous rendered run, written **`composite`**: the 673 raw bytes 50024-50697 carry `<code>`/`<a>` markup inside the words (True, False, `-B`, `PYTHONDONTWRITEBYTECODE`), so it is not a single raw-byte substring | `re.sub('<[^>]+>','',raw)` unescaped equals the quote; `grep`-style byte search of the plain sentence fails in the raw bytes |
| Quote occurrence | 1 in the page's rendered text (whole-document tag-strip) | `text.count(fragment)` → 1 |
| Locator | nearest preceding heading is **h1** `sys — System-specific parameters and functions` (`#module-sys`, raw line 206, byte 10286); body h2 count **0**; all eight h3/h4 are page chrome — four before the h1 (raw lines 103, 108, 127, 145) and four after the article (2945, 2950, 2969, 2990) | heading scan with `<h[1-6][^>]*>` over the file |
| Definition located | `<dt class="sig sig-object py" id="sys.dont_write_bytecode">` raw line 585 (byte 49551), one occurrence; `<dd><p>` raw lines 587-591, bytes 49838-50767 | byte offsets from the decoded snapshot |
| Sentence word counts | attribute sentence 17 words; naming sentence 32 words (over the Gate cap, so quoted as context); Gate fragment 18 words | split on the rendered strings |
| Registry census at the base | rows **173**, malformed **0**, duplicate ids **0**, enum/tier violations **0**, `mined` rows with a missing `used-by` path **0**; tier histogram `A=159 B=9 C=5`; status histogram `mined=164 rejected=9` (zero `queued`) | the five `CORPUS.md` census one-liners, run read-only from the lane root |
| `considerthese/` | absent | `ls considerthese` → exit 2, `No such file or directory` |
| `fetch.json` valid | `json.load` ok; `row_decision.id` = `S267`, `sentences.gate_quote.words` = 18 | `python -c "import json;json.load(open('fetch.json'))"` |

## Scope the page does and does not support

Stated by the page (observation of served bytes):

- the attribute's effect is on **an attempt**: "won't try to write `.pyc` files on the import of source modules";
- its initial value is set from the `-B` command line option **and** the `PYTHONDONTWRITEBYTECODE` environment
  variable;
- a program "can set it yourself to control bytecode file generation" — the value is assignable at runtime;
- the page is the module page; it defines no section for this entry beyond the module h1.

Not stated by the page (so nothing in the row may rest on it):

- nothing about cache **contents**: no sentence says a tree stays empty, so it cannot ground an "empty cache" arm;
- nothing about `PYTHONPYCACHEPREFIX` or `-X pycache_prefix` redirection (different entries, not read here);
- nothing about whether an existing `.pyc` is still *read* when writing is suppressed;
- nothing about child processes, embedded interpreters, V8, Node, Electron, `.jsc` files or code caches;
- nothing about atomicity, permissions failures, or the filesystem result of a refused write.

## Version scope

The page served is **3.15.2** (document title, raw line 20). The lane's dedicated interpreter is **Python 3.15.0**
(`/home/vgpnk/.local/share/kaidoku-jsc/venv/bin/python -I -B -V`, exit 0), same minor line. Observation at that
instant: `python -I -B -c 'import sys;print(sys.dont_write_bytecode)'` printed `True` — consistent with the page's
"-B sets the initial value" statement for this one invocation; it is not a test of the environment variable, of the
no-flag default, or of any write.

## Traceability against round 65 (QUALITY #35 / #36)

Round 65's `ScribeSources.md` recorded `sys.html` as a **rejected alternative** for its own row, with the stated
reason "its nearest heading is only the module-level h1, and it defines the attribute as *derived from* `-B`". That
decision was scoped to the `-B` switch row (S266), whose `scope` cell explicitly ends "not the environment variable's
page and not the `sys` attribute's page". This round's row takes exactly the carved-out scope, so it is a **scope
split, not a reversal** of a source decision; the row's `scope` cell names the earlier rejection, and the round-66
lesson must name `S267` for the reverse pointer. If the landing judge reads it as a reversal instead, the admitting
lesson owes the rejected decision by path and line
(`.ufo/waves/round-65/w1/ScribeSources.md`, "Behavior" bullet 4) — this file supplies that pointer.

## Rejected alternative

`https://docs.python.org/3/using/cmdline.html` — snapshot 171073 bytes, sha256
`96f87232f979982bd2aa268510c9c89b57186f0f3802840aafa7de1a7537810f`, fetched in this same run
(2026-11-04T00:16:22Z), **byte-identical at the two named instants** to S266's pin (r65 recorded the same sha256 at
2026-11-03T23:26:03Z); no continuity claim.

- `-B` definition: `<dt id="cmdoption-B">` raw line 472, `<dd><p>` 474-475, under h3
  `1.1.3. Miscellaneous options` (`#using-on-misc-options`, raw line 451).
- `PYTHONDONTWRITEBYTECODE`: `<dt id="envvar-PYTHONDONTWRITEBYTECODE">` raw line 1131, `<dd><p>` 1133-1135, under
  h2 `1.2. Environment variables` (`#using-on-envvars`, raw line 987); its sentence "This is equivalent to
  specifying the `-B` option." is at raw line 1135.

Why it is not the row: round 65 already holds **S266** for this page and for the switch's own effect, and S266's
scope cell excludes both the variable's page and the attribute's page. A second row on the same page for the same
switch would duplicate a row, and the switch definition cannot carry the attribute's initial-value and
settable-at-runtime semantics, which is what R66-C1's probe arms turn on.

Flip condition: S266 rejected or superseded, or a claim resting on the *equivalence* sentence (raw line 1135) or on
a section-level statement of the variable itself — then open the variable's row at `#envvar-PYTHONDONTWRITEBYTECODE`
(raw line 1131) rather than reusing either existing row.

## Status note

Drafted `queued` / `used-by —`. The registry holds zero `queued` rows today, and the census checks `used-by` only for
`mined`, so this draft cannot create a missing-path finding at the base. Flip to `mined` with the C1 knowledge entry's
path — logged old→new in `corpus/lessons/round-66.md`, append-only — once that entry's `source:` line cites `S267`.
