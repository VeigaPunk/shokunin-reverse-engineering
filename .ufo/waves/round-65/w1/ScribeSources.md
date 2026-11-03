# ScribeSources — round 65, wave w1

Seat: one opened source, one registry row. No source was edited; the only writes are the three files in the seat
directory plus this report file.

## Behavior

- Opened **S266** = CPython 3 documentation, *Command line and environment*, the `-B` option,
  `https://docs.python.org/3/using/cmdline.html`. Access date 2026-11-03; response `date` 2026-11-03T23:26:03Z.
- Snapshot: **171 073 bytes**, 1 922 lines, LF only, no BOM, no `Content-Encoding` (body bytes == `Content-Length`),
  sha256 `96f87232f979982bd2aa268510c9c89b57186f0f3802840aafa7de1a7537810f`.
  Document title pins the version: `1. Command line and environment — Python 3.15.2 documentation` (raw line 20).
- Quote (15 words, one contiguous passage, rendered text):

  > If given, Python won’t try to write .pyc files on the import of source modules.

  Raw **line 474** (continues on 475), byte span 36131–36287, apostrophe U+2019. Nearest heading:
  h3 `1.1.3. Miscellaneous options` (`using-on-misc-options`, line 451); definition `<dt id="cmdoption-B">` at line 472.
- Second candidate `https://docs.python.org/3/library/sys.html` was fetched in the same run (200, 280 617 bytes,
  sha256 `572c354eb01e5121f7beb3084408fc7ecbc465accf3a3335f1182c7df3648f7e`) and **not used**: `sys.dont_write_bytecode`
  (line 585) repeats the sentence but its nearest heading is only the module-level h1, and it defines the attribute as
  *derived from* `-B`. Recorded as `rejected_alternative` in `fetch.json` rather than dropped.

## Gates

| gate | result | evidence |
|---|---|---|
| Registry id free | S265 is the highest present id; zero occurrences of an `S266` row header in `corpus/SOURCES.md` | `grep -oE '^[ ]*S[0-9]+'` over the registry, `sort -V`, `tail -3` → S263, S264, S265 |
| Schema shape | row parses to **11 cells**; the line splits into 13 pipe-fields incl. leading/trailing empties, so no cell contains a pipe | field count 13 with the registry's own field splitter; cell split → 11 |
| Quote length / contiguity | 15 words ≤ 25; contiguous rendered sentence | `re.sub('<[^>]+>','',raw[36131:36287])` |
| Quote fidelity in gate.md | U+2019 form present, count 1 | `grep -c $'won\u2019t try' gate.md` |
| fetch.json valid | `json.load` ok; `bytes`=171073, `quote.words`=15 | python json load, exit 0 |
| Lane census, scratch copy (`corpus/SOURCES.md` + this row) at 20:27 | rows 173, malformed 0, duplicate ids 0, enum/tier violations 0, **one** `used-by` miss — the cited note did not exist yet | the five `CORPUS.md:135-147` census one-liners, run in scratch |
| Lane census, live `corpus/SOURCES.md` at 20:30 (after the concurrent append and after the note landed) | rows 173, malformed 0, duplicate ids 0, `used-by` misses 0 — clean | same five one-liners against the real registry, read-only |

## Touched surfaces

Written (only these):

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ScribeSources/row.md` — 752 bytes,
  sha256 `4e8422184b2255020fcc577560f22fb7f424ce1bd02b9dc8efa857b3a30305eb`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ScribeSources/gate.md` — 5 245 bytes,
  sha256 `7cc6cc658170feee73565381666f1192a2702704c4f94f2db70ce8e446594050`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-65/w1/ScribeSources/fetch.json` — 2 642 bytes,
  sha256 `ded743858509f3aad5ed34eacad4b22566ee9aa4d81db1b96309fa905631f553`
- this report.

Read-only reads: `kaidoku-shokunin/corpus/SOURCES.md` (schema, ids), fleet-root `CORPUS.md` (layout contract; not
written). Scratch `/fast/scratch/hyaku/kaidoku-r65/ScribeSources` created with `mkdir -p`, deleted.

**Concurrent change, not mine.** The seat drafts the row; it did not land it. At 20:29:10 local (after `row.md` was
written at 20:27:17) `corpus/SOURCES.md` gained exactly one line (`git diff --stat`: 1 insertion, 0 deletions), the
S266 row, appended by another writer in this wave. It matches `row.md` except that the `teaches` cell lost its final
period. This seat issued no write to `corpus/SOURCES.md`; `git status` was only read. Recorded so a later re-check
does not read the difference as tampering.

## Findings

1. The `-B` sentence is a switch definition, not an absence guarantee. It states the interpreter *will not try* to
   write `.pyc` on import; it cannot carry any closure-matrix claim that a cache tree is empty. The matrix's own
   census remains the only evidence of absence. The row's `teaches` cell is worded to keep that split.
2. Version pin is real: `docs.python.org/3/` served **3.15.2** docs on 2026-11-03, not a floating "latest". The
   `-B` wording is stable across 3.x in substance, but a recheck reads a version-specific snapshot — hence `recheck 90d`.
3. The quote is not a single raw-byte substring: the raw HTML wraps `.pyc` in one `<code>` element (four tags,
   documented in `fetch.json.quote.raw_markup_inside`). A re-check must compare rendered text or it will report a
   false mismatch.
4. Page choice was decided by anchor precision, not convenience: `cmdline.html` offers a named h3 section and the
   switch's own definition; `sys.html` offers the same sentence with only the module h1 and a derived-setting
   framing.
5. **Contract conflict, observed resolved — not by this seat.** The seat fixed `status: mined` with `used-by
   corpus/knowledge/2026-11-03-r65-jsc-closure-matrix.md`, while `CORPUS.md:103` defines `mined` as "cited by ≥1 path
   in `used-by`" and its census one-liner (`CORPUS.md:146-147`) requires those paths to exist. At 20:27 that note was
   absent, so the census over a scratch copy printed exactly one line:
   `missing: corpus/knowledge/2026-11-03-r65-jsc-closure-matrix.md`. At 20:28 the note appeared (5 593 bytes,
   sha256 `ee5a00cc3dc5b60d69b612e9142aa16f0303d584f89e0b1a8ee5c1219cbf7644`, `source: S266` at line 3, quoting the
   switch at line 54) and the live census at 20:30 is clean on all five one-liners. The `mined` status therefore
   stands as drafted; nothing here needed a downgrade to `queued`.
6. **One transcription nit for the landing reviewer.** The knowledge note's inline quote at line 54 writes
   `won't` with ASCII `'` where the fetched bytes carry U+2019 (`\xe2\x80\x99`). Meaning is unchanged, and this seat did
   not edit the note; flagged only because the row's `anchor` claims an exact quote and a re-check compares bytes.
   The landed registry row also differs from `row.md` by one dropped final period in `teaches`.

## Limits

- **No byte-stability claim.** One fetch per URL; `etag` `"6aea1fc6-29c41"` and `last-modified`
  `Tue, 03 Nov 2026 17:54:14 GMT` are recorded so a later fetch can detect drift, but nothing here shows the page
  is stable across fetches.
- **Scope limit on the source itself:** the page establishes nothing about V8, Node, Electron, `.jsc` files or code
  caches; nothing about whether a child process inherits `-B`; nothing about embedded interpreters where
  `sys.dont_write_bytecode` is the lever; and no filesystem observation. Enumerated in `gate.md` § Limit.
- `used-by` names `corpus/knowledge/2026-11-03-r65-jsc-closure-matrix.md`, which was absent when this seat finished
  its fetch (checked with `ls`, ENOENT) and appeared at 20:28, authored by another seat. This seat verified only that
  the path exists, cites `S266` at line 3, and leaves every census one-liner clean; it did not read the note's
  arguments and does not vouch for them.
- Tier A is the fleet contract's own definition, read at `CORPUS.md:93-97` ("**A**: primary or authoritative for
  that scope (spec, official docs, …)"; "`community` is never A"), applied to `kind: docs` on official
  `docs.python.org`. The 11-column header is `CORPUS.md:86`; the lane registry that consumes it is
  `kaidoku-shokunin/corpus/SOURCES.md`. No tier was invented here.
