# ScoutSources — round 66, wave w1

Seat: one opened source, one drafted registry row, one rejected alternative, the registry before-state. No source
was edited and `corpus/SOURCES.md` was not touched; the only writes are the three files in
`.ufo/waves/round-66/w1/ScoutSources/` and this report.

## Behavior

- Fetched **once** into scratch:
  `curl -fsSL -o sys.html -w 'HTTP=%{http_code}\nSIZE=%{size_download}\n' https://docs.python.org/3/library/sys.html`
  → **HTTP 200, 280617 bytes**, exit 0, captured **2026-11-04T00:16:22Z UTC** (access date **2026-11-03** local,
  UTC−3). sha256 `572c354eb01e5121f7beb3084408fc7ecbc465accf3a3335f1182c7df3648f7e`; 3071 lines, LF only, no BOM.
  Document title pins the served version: `sys — System-specific parameters and functions — Python 3.15.2
  documentation` (raw line 20). Response headers were not captured (single body fetch, no `-D`; no second request was
  made), so **no** `etag`/`last-modified` is recorded and no byte-stability claim is made.
- Located `sys.dont_write_bytecode`: `<dt class="sig sig-object py" id="sys.dont_write_bytecode">` at **raw line
  585** (byte 49551, one occurrence); its `<dd><p>` spans **raw lines 587-591**, bytes 49838-50767.
- Nearest preceding `<h1>`-`<h6>` heading: **h1** `sys — System-specific parameters and functions`
  (`#module-sys`, **raw line 206**, byte 10286). The page has **zero** `<h2>`; all eight `<h3>`/`<h4>` in the file are
  page chrome (`This page`, `Navigation`, `Previous topic`, `Next topic`), four before the h1 (103, 108, 127, 145) and
  four after the article (2945, 2950, 2969, 2990). So the module h1 is the entry's only containing heading — the page
  defines no section for this data attribute.
- The sentence that names the environment variable, verbatim, **32 words** (over the Gate cap, so quoted as
  context only):

  > This value is initially set to True or False depending on the -B command line option and the PYTHONDONTWRITEBYTECODE environment variable, but you can set it yourself to control bytecode file generation.

  The attribute sentence, verbatim, **17 words**:

  > If this is true, Python won’t try to write .pyc files on the import of source modules.

- **Gate quote**, 18 words, raw lines 588-590, bytes 50024-50697, one occurrence in the rendered page, labelled
  **`composite`** because the words cross `<code>`/`<a>` markup (True, False, `-B`, `PYTHONDONTWRITEBYTECODE`):

  > initially set to True or False depending on the -B command line option and the PYTHONDONTWRITEBYTECODE environment variable

  Apostrophe in the attribute sentence is U+2019. A re-check that greps the plain sentence in raw bytes will report
  a false mismatch: the fragment is contiguous only after tag-stripping and entity-unescaping.

## Row decision

Drafted in `row.md`, 11-column shape, pipe-free cells (`awk -F'|'` → `NF=13`, 12 pipes):

- `id` **S267** (free: 0 occurrences in `corpus/SOURCES.md`; S266 is the highest present id).
- `kind` **docs**; `tier` **A** under the fleet `CORPUS.md` tier category *official docs* — "primary or authoritative
  for that scope (spec, official docs, source code, original paper, maintainer statement, the lane's own re-runnable
  gate output)"; `community` would be barred from A and this is not that kind. Coverage-map ground served:
  `.jsc` route under a complete closure (round 65), `corpus/README.md:76`, whose R66-C1 closure counter runs this
  interpreter.
- `scope` is exactly what the page states about the flag and the variable: no attempt to write `.pyc` on import of
  source modules; an initial value set from `-B` **and** `PYTHONDONTWRITEBYTECODE`; the value may be set by the
  program itself. It is **not** "the interpreter writes no bytecode", not cache content, not an emptiness guarantee.
- `teaches`: one grounded benefit — read the attribute as a statement about an *attempt*, not about a directory, so a
  cache-free probe pins one lever and still censuses the tree.
- `recheck` **90d** (`docs.python.org/3/` serves a floating minor; the row's anchor is a dated snapshot).
- `status` **queued**, `used-by` **—**: the C1 knowledge entry that will cite the row does not exist at this base, and
  the census checks `used-by` only for `mined` rows, so `mined` here would create a missing-path finding. Flip is
  specified in `gate.md` § Status note (append-only, logged old→new in `corpus/lessons/round-66.md`).

## Second candidate — rejected, with flip

`https://docs.python.org/3/using/cmdline.html` was fetched in the same run: 171073 bytes, HTTP 200, sha256
`96f87232f979982bd2aa268510c9c89b57186f0f3802840aafa7de1a7537810f` — **identical bytes at the two named instants**
to S266's pin (r65 recorded the same sha256 at 2026-11-03T23:26:03Z; this fetch at 2026-11-04T00:16:22Z). No
continuity between the instants is claimed.

- `-B` definition at `#cmdoption-B`, raw line 472 (`<dd><p>` 474-475), section h3 `1.1.3. Miscellaneous options`
  (`#using-on-misc-options`, raw line 451).
- `PYTHONDONTWRITEBYTECODE` at `#envvar-PYTHONDONTWRITEBYTECODE`, raw line 1131 (`<dd><p>` 1133-1135), section h2
  `1.2. Environment variables` (`#using-on-envvars`, raw line 987), with "This is equivalent to specifying the `-B`
  option." at raw line 1135.

**Why it is not the row:** round 65 already holds **S266** for that page and for the switch's own effect, and S266's
`scope` cell explicitly excludes both the environment variable's page and the `sys` attribute's page. A second row on
one page for one switch duplicates a row, and the switch definition cannot carry the attribute's initial-value and
settable semantics — which is what R66-C1's probe arms turn on. **Flip:** S266 rejected or superseded, or a claim
resting on the equivalence sentence (raw line 1135) or on a section-level statement of the variable itself — then open
the variable's row at `#envvar-PYTHONDONTWRITEBYTECODE` (raw line 1131) instead of reusing either existing row.

This is a **scope split, not a reversal** of round 65's recorded rejection of `sys.html`; traceability is stated in
`gate.md` § Traceability (QUALITY #35/#36) with the r65 pointer by file and bullet, in case the landing judge reads it
as a reversal.

## Registry before-state

| measure | value | command |
|---|---|---|
| rows | **173** | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` |
| malformed (`NF!=13`) | **0** | the `CORPUS.md` malformed-row one-liner |
| duplicate ids | **0** | `awk -F'\|' … \| sort \| uniq -d` |
| next free id | **S267** | highest present S266; `grep -c 'S267'` → 0 |
| tier histogram | `A=159 B=9 C=5` | tier one-liner |
| status histogram | `mined=164 rejected=9` (zero `queued`) | status one-liner |
| enum / tier-inflation violations | **none printed** | enum one-liner, exit 0 |
| `mined` rows with a missing `used-by` path | **none printed** | used-by one-liner |
| `considerthese/` | **absent** | `ls considerthese` → exit 2, `No such file or directory` |

Disk guard before the pass: `/fast/scratch/hyaku` 55 % used, 368.8 G free; `/tmp` 26 % used, 95.8 G free. Scratch
(`/fast/scratch/hyaku/kaidoku-r66/ScoutSources`, 444 K) was created with `mkdir -p` and deleted
(`SCRATCH_REMOVED`); nothing was written into the toolchain tree, and the interpreter was only invoked with `-I -B`.

## Assimilation status (read-only)

`ls /home/vgpnk/Projects/shokuknow/merge/kaidoku/` →
`MERGE-REPORT.json`, `MERGE-REPORT.md`, `SOURCES.append.md`, `knowledge/`.

`MERGE-REPORT.md` heading list, quoted (grep `^#{1,6} `):

```
1:# Merge package — kaidoku
11:## What gets appended to `corpus/SOURCES.md`
15:## Knowledge files to add
97:## Rows no entry rests on (status forced to `queued`)
106:## `used-by` pointers corrected at packaging time
118:## Adopt checklist
```

Its own header states: 132 proposed rows accepted, 77 proposed knowledge entries, "lane registry currently holds
**105** rows; first staged id is **S106**", and "**Nothing was written into the lane repo.**"

Measured assimilation at this base:

| measure | value | command |
|---|---|---|
| staged rows / staged knowledge files | **132 / 77** | row-header grep + `os.listdir` over `knowledge/corpus/knowledge` |
| staged knowledge files present in `corpus/knowledge/` | **2 of 77** (`jsc-mapper-cli-contract.md`, `jsc-mapper-release-inventory.md` — round 64, `corpus/README.md:75`) | `os.path.exists` per staged name |
| staged ids that also exist in the registry | **44**, but **0 of 44** share the staged `source` cell | per-id compare of the row's `source` cell |

The 44 id collisions are **not** assimilation: the package was staged when the lane held 105 rows and allocated
S106+, while the lane has since allocated S106+ for its own rows (e.g. lane `S106` = binutils readelf version-needs,
staged `S106` = unblob README). Appending `SOURCES.append.md` as-is would produce 44 duplicate ids; any future
adoption must renumber. Conclusion for this round: **no remaining staged theme fits these two counter repairs** (the
jsc theme was the only one adopted, in round 64), and `considerthese/` remains absent — matching the plan's
"Assimilation: none this round", now with the measurement behind it.

## Gates

Full record with commands in `gate.md`; summary: id free (`S267` 0 occurrences), schema shape (`NF=13`), Gate quote
18 words ≤ 25 with `composite` label, one rendered occurrence, locator = module h1 (raw line 206) with body h2 count
0, definition at raw line 585, registry census clean on all five one-liners, `fetch.json` loads and reports 18 words.
Hard boundary recorded there: the page says nothing about cache contents, so no arm that requires an *empty* cache may
cite this row.

## Findings

1. The page's own words are about an **attempt** ("won't try to write"), the **source of the initial value** (`-B`
   and the variable), and **assignability** ("you can set it yourself"). R66-C1's a1/a2 arms need an empty cache and
   a `.pyc` path respectively: the `.pyc`-path arm (a2) is consistent with this page, the empty-cache arm (a1) is
   **not** — an empty tree must come from the counter's own census, not from the flag.
2. Page-local scope matters here: the sentence that makes the variable and `-B` equivalent lives on `cmdline.html`
   (raw line 1135), i.e. S266's page. The sys page only says the initial value depends on both. A row that merged the
   two would misstate its locator; keeping them split is what lets this row exist without duplicating S266.
3. The entry has no section of its own — only the module h1 — which is precisely the ground on which round 65
   declined it for the S266 anchor. That is not a defect in this row's locator (it is the nearest heading and it is
   named), but it does mean the anchor must carry the raw line and byte offsets, which it does.
4. Byte identity across rounds is available and cheap: the `cmdline.html` snapshot this seat fetched is the same
   sha256 that S266 pinned, at two named instants. That supports reading S266's quote against current bytes; it is
   not evidence of stability over any interval.
5. Registry hygiene is clean at the base, but the lane holds **zero** `queued` rows, so a drafted `queued` row is the
   only one of its kind; if the landing prefers `mined`, the citing knowledge entry must exist first or the used-by
   census will print a `missing:` line exactly as it did in round 65.

## Limits

- **One fetch, no headers.** No `etag`/`last-modified`/`content-encoding` header was captured, and no second body
  request was made; nothing here shows the page's bytes are stable between instants, only what the one snapshot holds.
- **Version skew stated, not resolved.** The page is 3.15.2 documentation; the lane interpreter measured 3.15.0. The
  row anchors the snapshot it opened, not "Python 3".
- **No runtime claim.** The single observation `python -I -B -c '…sys.dont_write_bytecode'` → `True` shows only that
  invocation, with `-B` supplied by this seat. Nothing was imported, no cache was observed, no directory was
  inspected, and the environment variable was not exercised.
- **Page scope only.** The source establishes nothing about V8, Node, Electron, `.jsc` files or code caches; nothing
  about `PYTHONPYCACHEPREFIX`/`-X pycache_prefix`; nothing about whether an existing `.pyc` is still read when writing
  is suppressed; nothing about child processes or embedded interpreters; nothing about the filesystem outcome of a
  refused write.
- **Merge package read-only, not audited.** Counts above come from filenames and row headers; this seat did not verify
  the staged rows' own sources and does not vouch for them.

## Touched surfaces

Written (only these, all under the seat directory):

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-66/w1/ScoutSources/row.md` — 3943 bytes,
  sha256 `777fd83b07900da777e161ee02d0b0817d293796aeac6d72aea808e91fe24c2e`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-66/w1/ScoutSources/gate.md` — 7107 bytes,
  sha256 `1ba691bc97ecec05f0227494ae8db329c3137ac24fbbe77d91da7792bceb3170`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-66/w1/ScoutSources/fetch.json` — 4860 bytes,
  sha256 `b204e53722a6f00c67c4e27ae3e8e11601e1625fc4e6a022446c59eff3b1846c`
- this report.

Read-only reads: lane `corpus/SOURCES.md`, `corpus/README.md`, `corpus/QUALITY.md`, `corpus/knowledge/`
(r65 note's `source:` line, two jsc notes' headers), `plans/round-66-claims.md:104-116`,
`.ufo/waves/round-65/w1/ScribeSources.md`, fleet-root `CORPUS.md:80-150`, `/home/vgpnk/Projects/shokuknow/merge/kaidoku/`.
No tool was installed, upgraded or removed; `pacman` was not run.
