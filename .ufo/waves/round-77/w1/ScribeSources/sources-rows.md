# ScribeSources — round-77 source-row drafts: S289 RFC 8259 §3, S290 Bash §3.7.5, S291 `ast.literal_eval` reject

Seat: ScribeSources (scribe). Date of work: 2026-11-04. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Measured HEAD at the start of this read: `509c105140e90f7299b024796914e2639c206cb9` (base `188562d4…`, declaration
`819cf30e…`, freeze `6767a879…`, all ancestors of HEAD). `corpus/SOURCES.md` was **not** written by this seat: the
three rows were already committed at `fd0b95bd` while this seat was reading; these drafts are the byte-verified
replacement text, and every difference from the committed rows is listed in section 6.

## 1. Byte-exact quote verification (the three committed snapshots)

All three snapshots are the ones committed in `.ufo/waves/round-77/l1/sources/`; no fetch was repeated. Each
quote is asserted byte-exactly inside the stated 1-based line (`bytes_verified: true` in `receipt.json`), and each
occurs once in its file (`data.count(quote) == 1`). Line endings are LF; the RFC text is plain ASCII and the two
HTML pages are UTF-8.

```text
$ sha256sum .ufo/waves/round-77/l1/sources/{rfc8259.txt,page-721dd237.html,page-298eb5f5.html}
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  rfc8259.txt            (28 360 B)
78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b  page-721dd237.html     (1 040 954 B)
8cacd731a2e0af73fe025a7223d53036b09f6405b98755d4253a6bb9d2d8dcb2  page-298eb5f5.html     (362 493 B)

$ grep -n 'A JSON value MUST be an object' rfc8259.txt
298:   A JSON value MUST be an object, array, number, or string, or one of

$ grep -n 'Bash itself returns the exit status of the last command' page-721dd237.html
4435:<p>Bash itself returns the exit status of the last command

$ grep -n 'Evaluate an expression node or a string containing only a Python literal or' page-298eb5f5.html
2760:<dd><p>Evaluate an expression node or a string containing only a Python literal or
```

Located context:

- **RFC 8259** — publication date `December 2017` (line 9, `Obsoletes: 7159`), section heading `3.  Values` at
  line 296, quote at line 298 (14 words). The sentence continues at line 299 (`the following three literal names:`)
  and the three literal names are at lines 301-303 (`false`, `null`, `true`); line 305-306 states
  `The literal names MUST be lowercase.` The quote is contiguous plain text, not composite.
- **Bash** — `This is Edition 5.3, last updated 18 May 2025,` at line 9 (plain-text mirror at line 84), section
  heading `3.7.5 Exit Status` at line 4392, quote at line 4435 (10 words). The sentence continues at lines
  4436-4437: `executed, unless a syntax error occurs, in which case it exits with a non-zero value.` The quote is
  contiguous rendered text (the `<p>` opener precedes it on the same line); no tag falls inside the quoted words.
- **`ast.literal_eval`** — `<title>` (line 20) names `Python 3.15.2 documentation`; the entry `<dt>` is at lines
  2758-2759; the quote is the first rendered sentence at line 2760 (13 words), continuing on line 2761
  (`container display.`). Lines 2761-2763 give the accepted Python structures: `strings, bytes, numbers, tuples,
  lists, dicts, sets, booleans, None and Ellipsis`.

## 2. Draft rows (verbatim, 11 cells each, no literal or escaped pipe)

```text
| S289 | RFC 8259 section 3 Values (JSON), December 2017 — https://www.rfc-editor.org/rfc/rfc8259.txt (snapshot `rfc8259.txt`, 28 360 B, in `.ufo/waves/round-77/l1/sources/`) | spec | A | JSON value taxonomy: `false`, `null` and `true` are literal names distinct from numbers, and the literal names MUST be lowercase; grounds the type-strict comparison of a claimed verdict against a receipt field, not schema conformance and not REA Evidence authority | December 2017 (line 9); section 3 Values heading line 296; located quote line 298 (14 words), the sentence continuing to line 301; the three literal names at lines 301-303; sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`; opened 2026-11-04 | A receipt's `true` and `1` are different JSON values, so an annotation claiming one cannot satisfy a field holding the other; `tools/round-77/verdict-bind.py` compares types (line 187) because Python's `True == 1` would otherwise accept a boolean where the record holds an integer. | mined | 2026-11-04 | 90d | corpus/knowledge/2026-11-04-r77-verdict-binding.md |
| S290 | GNU Bash Reference Manual, Edition 5.3 (last updated 18 May 2025) — https://www.gnu.org/software/bash/manual/bash.html (snapshot `page-721dd237.html`, 1 040 954 B, in `.ufo/waves/round-77/l1/sources/`) | docs | A | Shell exit-status semantics: a shell process returns the exit status of the last command executed, a syntax error being the documented exception; grounds recording a child gate's exit in a receipt, not a claim that the gate's verdict is correct | Edition 5.3 (line 9, last updated 18 May 2025); section 3.7.5 Exit Status heading line 4392; located quote line 4435 (10 words), the sentence continuing to line 4437 with the syntax-error exception; sha256 `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b`; opened 2026-11-04 | The wrapper records a child's exit because a shell returns the last command's status; `tools/round-77/prefile-receipt.py` stores the child's `returncode` as `exit` (line 114), so the field is the gate's own verdict, never a re-derivation of its checks. | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r77-prefile-receipt.md |
| S291 | `ast.literal_eval`, Python 3.15.2 standard library — https://docs.python.org/3/library/ast.html (snapshot `page-298eb5f5.html`, 362 493 B, in `.ufo/waves/round-77/l1/sources/`) | docs | C | AST literal evaluation; refused as the grammar for the verdict annotations the receipts carry | Python 3.15.2 documentation (title line 20); `ast.literal_eval` entry `<dt>` lines 2758-2759; located quote line 2760 (13 words); sha256 `8cacd731a2e0af73fe025a7223d53036b09f6405b98755d4253a6bb9d2d8dcb2`; opened 2026-11-04 | REJECTED: the annotation grammar is JSON's literal vocabulary, not Python's; `literal_eval` also accepts `True`, `None`, `Ellipsis` and container displays (tuples, sets, bytes) that the records never use, so it would widen the grammar past the JSON literals the receipts hold. Flip: the annotation grammar becomes a Python literal grammar. Consumer search: `grep -c 'literal_eval' tools/round-77/verdict-bind.py` prints 0 (grep exit 1, no match), so no consumer needs the page. | rejected | 2026-11-04 | 180d | — |
```

## 3. Mechanical checks (no production file touched)

`check-rows.py` reported `failures: []` (`check-rows.json`) over: three rows; 11 cells each; no literal or
escaped pipe in any cell; `kind` / `tier` / `status` / `opened` / `recheck` enums; the first URL token normalizes
to the expected host+path; the full sha256 and the byte count present in the anchor cell; each quote byte-exact
on its stated line and occurring exactly once; the recomputed word counts 14 / 10 / 13 equal to the counts the
draft states; the reject's `Flip:` and consumer search present.

Standing parser (`scripts/sources-census.sh`, read-only; `--file`/lane args below, `TMPDIR` in scratch):

| run | rc | findings |
|---|---|---|
| `validate --file corpus/SOURCES.md` (live registry, HEAD `509c1051`) | 0 | 23 W04, `ok`, no E-code |
| `census --file corpus/SOURCES.md` | 0 | 197 rows (tier A 181, B 9, C 7; mined 179, rejected 18) |
| scratch lane `fix-r77repl-shokunin`: committed S289-S291 **replaced** by these drafts | 0 | 23 W04, `ok`, no E-code |
| scratch lane `fix-r77app-shokunin`: these drafts **appended** beside the committed rows | 1 | `E03 S289`, `E03 S290`, `E03 S291` duplicate id, plus 3 W04 (the reworded scopes) |

The two scratch lanes symlink the lane's other top-level entries and `corpus/` children, so `E11` resolves; the
first attempt with `--file` into a bare scratch dir produced spurious `E11` findings and is not evidence.

## 4. Id collision check (read from the registry, not assumed)

- At the freeze tip the registry's highest id is `S288`; the next free numbers are `S289`, `S290`, `S291`.
- The committed lesson (`corpus/lessons/round-77.md`, `## Gate`) and the round's landing commit `fd0b95bd`
  already pin those three ids to exactly these three sources, so a different numbering would contradict the
  committed record.
- HEAD `509c1051` carries `S289`/`S290`/`S291` once each in `corpus/SOURCES.md` (`git grep -c` → 1) and twice in
  the lesson. The drafts therefore **replace** the committed rows; appending them yields `E03` (section 3).
- If the L1 instead keeps the committed rows, the next free ids are `S292`, `S293`, `S294`; they are unused at
  HEAD.

## 5. Duplicate URLs and the W04 class

`url_of()` (`scripts/sources-census.sh:600`) takes the first `https?://…` token, strips the fragment and a
trailing slash, and lowercases only the host; duplicates are exact normalized-string matches, `W04` when the
`(url, scope)` pair is new and `E04` when the same URL repeats inside one scope without `supersedes S…`.

- The RFC 8259 URL is already held by **S049** as `https://www.rfc-editor.org/rfc/rfc8259` (scope: JSON object
  member identity and duplicate-name interoperability). The `…/rfc8259.txt` path is a different normalized
  string, so S289 does not collide; a row citing the HTML URL would print
  `W04 <id> duplicate url www.rfc-editor.org/rfc/rfc8259 across scopes`.
- The JSON URL is already held by **S050** as `https://docs.python.org/3/library/json.html` (Python JSON library
  decoder behavior); no row here cites it.
- The Bash manual URL (`www.gnu.org/software/bash/manual/bash.html`) and the `ast` URL
  (`docs.python.org/3/library/ast.html`) are new; the nearest neighbours are S288 (`man7.org/…/bash.1.html`,
  rejected) and S050 (different page).
- **W04 is a warning by contract**: `scripts/sources-census.sh:33` and its selftest
  (`W04-does-not-fail-validation`) fix that warnings never change a clean lane's exit; only `E04` is an error.
  Empirically the replace fixture keeps the baseline 23 W04 and exits 0.

## 6. Differences from the three committed rows (`fd0b95bd`), reported not edited

1. **S289 anchor** — committed: `December 2017, section 3 Values, line 298`, with the digest only as a 16-hex
   prefix in the source cell. Draft: full sha256, and the section heading (296), the sentence end (301) and the
   literal-name lines (301-303) named.
2. **S290 anchor** — committed: `Bash 5.x manual`. The snapshot's own line 9 reads `This is Edition 5.3, last
   updated 18 May 2025`, so the draft names Edition 5.3; the draft's `scope` also carries the syntax-error
   exception the sentence states at lines 4436-4437, which the committed scope omits.
3. **S291 source/anchor** — committed: `Python 3 standard library` and `line 2760`; the page's `<title>` names
   Python 3.15.2, so the draft pins that build. Full sha256 in the draft anchor.
4. **Consumer-search citation** — the committed S291 `teaches` cell and the lesson Gate both write
   `(QUALITY row 36)`. QUALITY row 36 is the source-decision reversal-traceability rule; it contains no
   consumer-search clause, and no QUALITY row does. The draft drops the citation and states the search itself,
   which follows the round-76 S288 precedent.
5. **Gate word counts** — the committed lesson Gate states 16 / 11 / 15 words for the three quotes; `wc -w` on the
   quoted strings gives **14 / 10 / 13**. All six numbers are under the QUALITY #42 ceiling of 25, so this is a
   count error, not an over-length quote. The drafts state the recomputed counts.
6. **Unretained HTTP 200** — the lesson Gate and the rows say `HTTP 200` for all three GETs, and the lesson says
   "one GET each", but no fetch transcript (status, `size_download`, timestamp) is retained anywhere under
   `.ufo/waves/round-77/`. This seat verified the retained bytes and digests only; the HTTP status is carried from
   the lesson, not re-observed here.

## 7. Consumer search for the reject (verbatim)

```text
$ grep -c 'literal_eval' tools/round-77/verdict-bind.py
0
grep-exit=1
```

`grep -c` prints `0` and exits 1 (no match). The row is not needed: `verdict-bind.py` compares against JSON
decoded values (`json.loads`, line 126; `type(claimed) is type(actual)`, line 187), never against Python literal
syntax.

## Limits

- No fetch was repeated; the snapshots are the committed ones, and their digests are recomputed from the bytes on
  disk. A live-page drift is outside this draft.
- The committed rows are another hand's landing, committed mid-seat; this report records them but does not modify
  or republish them. `corpus/SOURCES.md`, the lesson and the knowledge entries were not written by this seat.
- The census was run against scratch lanes that symlink the real trees; the fleet census over the real lane is the
  L1's step.
