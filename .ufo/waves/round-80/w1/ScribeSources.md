# ScribeSources — round 80, wave 1

Seat: `ScribeSources` (scribe, leaf member; no subagent dispatch).
Base `16dfa009bf143080dfcdfc5f9ec34bd359536d90`; lane head and declaration
`84d68e90f8a1ea3a3a7f94a208695c21023c0472` (`git rev-parse 84d68e90^` → `16dfa009…`, so head is one
commit above base and `git log -1 --format=%H -- plans/round-80-claims.md` is the same `84d68e90`).
No lane production file was edited. Everything below is a draft for the L1.

Evidence dir: `.ufo/waves/round-80/w1/ScribeSources/` — `receipt.json`, `rows-draft.md`, two primary
snapshots, two Q&A snapshots, one rendered-page 403 snapshot, one background article.

## 1. Snapshots (bytes kept, HTTP 200)

| file | URL | form | status | bytes | sha256 |
|---|---|---|---|---|---|
| `rfc8259.txt` | `https://www.rfc-editor.org/rfc/rfc8259.txt` | plain text | 200 | 28 360 | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |
| `re.html` | `https://docs.python.org/3/library/re.html` | HTML | 200 | 257 722 | `24ef5ff00f937cee65b83d527638fe1c1fc573578851e296f4bca0c4da3828a6` |

The RFC bytes are byte-identical to the snapshot S289 already holds (same 28 360 B, digest prefix
`61a5378f4255c720` — the exact 16 hex characters S289 records). The `re.html` bytes are **not** S143's:
S143 recorded 257 706 B / `f169ed06…` on 2026-10-28; today is 257 722 B / `24ef5ff0…`, +16 B.

## 2. Located quotes (both ≤ 25 words)

- RFC 8259 §4, raw line **322** (`grep -n`; `splitlines()` reports 327 because 5 of the file's 16 form
  feeds precede it): **"The names within an object SHOULD be unique."** — 8 words,
  line sha256 `4f3b9acc…`, sentence sha256 `7081c92b…`. Anchor: section 4 Objects (raw line 316), the
  sentence closing the paragraph at 318-322, then the object ABNF (324-327) and the interoperability
  paragraph (329-344: "the behavior of software that receives such an object is unpredictable… Many
  implementations report the last name/value pair only").
- Python `re`, raw HTML line **747**: **"Matches the empty string, but only at the beginning or end of
  a word."** — 14 words, line sha256 `af345fa4…`, sentence sha256 `2e383a44…`. Anchor: section id `b`,
  span id `re-syntax-special-word-boundary`, h4 carrying the `\b` spelling at raw line 746; the paragraph
  runs to line 755 and supplies the formal reading (boundary between `\w` and `\W`, or `\w` and a string
  end).

## 3. Duplicate check (run before drafting)

```
grep -n 'rfc-editor\.org' corpus/SOURCES.md                  -> 4 hits (lines 55, 171, 205, 278)
grep -n 'docs\.python\.org/3/library/re\.html' corpus/SOURCES.md -> 1 hit (line 149)
grep -n 'docs\.python\.org' corpus/SOURCES.md                -> 19 hits
grep -n 're-syntax\|#re-' corpus/SOURCES.md                  -> 0 hits
grep -nF '\b' corpus/SOURCES.md                              -> 0 hits
grep -n 'word boundary' corpus/SOURCES.md                    -> 0 hits
```

- **RFC 8259 → refused reuse, not a row.** Line 205 (S289) holds the `.txt` URL with the same bytes;
  line 55 (S049) holds the same document's **section 4** anchor and a scope cell naming
  "duplicate-name interoperability". A third RFC 8259 row would register one sentence twice over.
  Action: cite S049, and append this receipt to S049's `used-by`.
- **Python `re` `\b` → row.** Line 149 (S143) holds the page URL but anchors
  `re.fullmatch(pattern, string, flags=0)` — a whole-string equality primitive. The requested anchor is
  the zero-width word-boundary assertion, a different grammar element in the syntax section. Lane
  precedent treats a different fragment of a held page as a new row (S260 `subprocess.html` vs S272
  `subprocess.html#subprocess.Popen`; S274 vs S276), and the two anchors answer different questions:
  whether the whole string is equal, versus where a word ends.
- **Host alone is not a bar.** `docs.python.org` already carries 19 citing lines across ~13 distinct
  pages. The bar is the URL plus its anchor.

## 4. Rejection (one, actually opened)

`https://stackoverflow.com/questions/21832701/does-json-syntax-allow-duplicate-keys-in-an-object`.
The rendered page returned **HTTP 403**, 5 753 B, Cloudflare interstitial titled "Just a moment…"
(`so-dupkeys.html`, sha256 `d6404958…`), so the content was opened through the official **Stack
Exchange API 2.3**: question body 1 387 B (`so-api.json`, sha256 `79f61b33…`) and its 12 answers
21 102 B (`so-answers.json`, sha256 `e086dc8b…`), both HTTP 200. The score-226 answer opens "Yes but is
not recommended" and then quotes RFC 8259's sentence with the BCP 14 reading of SHOULD; the score-161
answer quotes ECMA-404 and notes that JSON itself specifies no behaviour.

Reason it is not a row: its normative sentence is the RFC's own, reproduced by quotation; the page's own
contribution is vote-ordered interpretation that drifts without notice. Flip condition: the claim becomes
about **observed implementer practice** rather than the grammar (e.g. "implementers report last-wins in
practice") — then it becomes a `community` tier-B row whose source cell pins the answer's own
`last_edit_date` and the API snapshot digest. A claim about what the grammar permits still cites S049.

Also fetched and **not** registered (`screened_not_registered`): `https://en.wikipedia.org/wiki/JSON`
(HTTP 200, 478 308 B, sha256 `b5d0c2cc…`, kept as `wiki-json.html`). It carries a duplicate-names bullet,
but it is a tertiary paraphrase of the RFC §4 interoperability paragraph with no normative text of its own
and no stable revision pin — neither the primary ground nor the blog/Q&A rejection this seat must record.

## 5. Rows draft (`rows-draft.md`, draft only)

Proposed `S297` — **append** (new anchor on a held page; 11 cells, no escaped separator):

```
| S297 | Python `re` documentation, `\b` word-boundary assertion — https://docs.python.org/3/library/re.html#re-syntax-special-word-boundary (snapshot `re.html`, 257 722 B, sha256 `24ef5ff00f937cee65b83d527638fe1c1fc573578851e296f4bca0c4da3828a6`, in `.ufo/waves/round-80/w1/ScribeSources/`) | docs | A | the zero-width assertion that a match sits at the beginning or end of a word, where a word is a run of `\w` characters; it grounds the delimited-token vocabulary R80-C1's binder uses, not the frozen alphabet itself (the frozen token characters add `.` and `-` to `\w`, and `\w` on str patterns is Unicode-aware while that alphabet is ASCII-only) and not `re.fullmatch` (S143) | `\b` entry, section id `b`, span id `re-syntax-special-word-boundary`, raw HTML line 746, first sentence at line 747 | `\b` matches only at a boundary between a word character and a non-word character or the string ends, so a declared pin is checked as a delimited token rather than a substring; `.` and `-` are not word characters, so `\b` still bounds inside `rea-agents@6.7.0-rc1` and the frozen rule is deliberately stricter | mined | 2026-11-04 | on-release | .ufo/waves/round-80/w1/ScribeSources/receipt.json |
```

Proposed `S298` — **withhold** (refused reuse; full row text is in `rows-draft.md` and
`receipt.json.rows_draft[1]`). No id is consumed by this draft. If the L1 overrules the verdict, the row
is ready to paste as `S298`; the recommended alternative is the S049 `used-by` append.

Optional, not one of the two rows: a `rejected`-status row for the Q&A, matching lane precedent
S144 / S291 / S294, with its id left unassigned — the L1 assigns the next free id at landing (`S298` if
the withheld RFC row is not landed, otherwise `S299`). Whether the rejection becomes a registry row or
stays in the receipt only is the L1's call.

Ids: highest held is `S296`, so `S297` is next assignable
(`grep -oE 'S[0-9]{3,}' corpus/SOURCES.md | sort -u | tail -5` → S292 S293 S294 S295 S296). Ids are this
seat's reading at `84d68e90`; re-read them at landing.

## 6. Gate block draft (`receipt.json.gate_block_draft`)

Pins the committed instrument and each pointer line's digest, never the pointed bytes of a live config:

```json
{"instrument":{"path":"corpus/SOURCES.md","blob":"27771e681c59b22ddfff03e035a8d7485fbf006c","sha256":"3b7f44f6878cf153d7ca321956b2edc4ba96748af7b90b7f0eb9870ffdd55364"},
 "rows":[{"id":"S297","append":true,"snapshot":{"bytes":257722,"sha256":"24ef5ff0…"},"pointer":{"line":747,"line_sha256":"af345fa4…","quote_sha256":"2e383a44…","words":14}},
         {"id":"S298","append":false,"reuse_of":["S049","S289"],"pointer":{"line":322,"line_sha256":"4f3b9acc…","quote_sha256":"7081c92b…","words":8}}],
 "expected":{"rows":1,"withheld":1,"cells_per_row":11}}
```

`instrument.sha256` is the **committed** blob digest at head (`git ls-tree HEAD corpus/SOURCES.md` →
`27771e68…`, and `git cat-file blob 27771e68… | sha256sum` equals the worktree digest). It is stale by
construction the moment the L1 appends, so it must be recomputed from the committed blob post-landing —
which is precisely R80-C2's rule.

## 7. Findings

1. **The RFC ground already exists twice.** S289 holds the identical `.txt` bytes; S049 holds §4 and the
   duplicate-name scope. R80-C1's duplicate-cell rule has a citable ground today without a new row.
2. **`re.html` drifted** (+16 B, digest changed since 2026-10-28). A row on a live page must pin its own
   snapshot; the pointed-line digest is what survives drift.
3. **`\b` is not the frozen alphabet, in both directions.** Verified: `\brea-agents@6\.7\.0\b` **matches**
   `args = [ "rea-agents@6.7.0-rc1" ]` (the character after the pin is `-`, a non-word character) while the
   frozen rule **refuses** it; conversely the same pattern **fails** on `x rea-agents@6.7.0é` because `\w`
   on `str` patterns is Unicode-aware, while the frozen ASCII alphabet treats `é` as a delimiter and
   accepts. So `\b` grounds the boundary vocabulary and cannot stand in for the rule.
4. **The frozen fixture set cannot tell a `\b`-only binder from the frozen rule.** rb01's continuation is
   `5` and rb02's is `0` — digits — so `\b` refuses both reds, and it binds both greens. A `\b`-only
   binder would score `candidate_false_greens 0` and `refusals 0` on the frozen six while still
   mis-binding a hyphen- or dot-continued superstring. A fifth red fixture (`rea-agents@6.7.0-rc1`) would
   separate the rules, but the fixture set is frozen by the guard commit — an amendment, not a scribe
   edit. Reported, not acted on.
5. **The Q&A's rendered page was blocked** (403 Cloudflare); its content was opened through the official
   API and is recorded as an API open, never as a rendered-page open.
6. **Only one registry action is recommended**: append `S297`, and add this receipt to S049's `used-by`.
   Everything else is withheld or optional.

## 8. Limits

- Ids `S297`/`S298` are provisional; another seat may claim ids concurrently.
- The RFC sentence is a **SHOULD**; the duplicate-cell refusal is the lane's stricter policy, and the
  drafted row says so in its scope cell.
- RFC line numbers are `grep -n` numbering; `splitlines()` differs by the 5 form feeds that precede line
  322.
- The `re.html` quote is plain text inside one `<p>`; a byte-exact checker should compare the sentence,
  not the surrounding tags.
- No tool was installed or upgraded: no pacman transaction, no `uv`, no `npx`. Tools used were the host
  `python3` 3.14.8 and `curl` 8.23.0. Network use was six GETs total (two primary pages, the blocked
  rendered Q&A, two API calls, one Wikipedia page).
- Scratch `/fast/scratch/hyaku/kaidoku-r80/ScribeSources/` was created with `mkdir -p`, used as the cwd
  and `TMPDIR` root for every fetch, then removed with `rm -rf` after copying each receipt into the
  evidence dir. Nothing in the receipt depends on it, and no `/tmp` path was written by this seat.

## 9. Files written

- `.ufo/waves/round-80/w1/ScribeSources/receipt.json` (20802 B) — acceptance fields `snapshots`,
  `quotes`, `duplicate_check`, `rejection`, `next_ids`, `rows_draft`, `gate_block_draft`, plus
  `screened_not_registered`, `rejection_row_draft`, `log_entry_draft`, `findings`, `limits`,
  `self_checks`.
- `.ufo/waves/round-80/w1/ScribeSources/rows-draft.md`
- `.ufo/waves/round-80/w1/ScribeSources/{rfc8259.txt,re.html,so-api.json,so-answers.json,so-dupkeys.html,wiki-json.html}`
- `.ufo/waves/round-80/w1/ScribeSources.md` (this report)
