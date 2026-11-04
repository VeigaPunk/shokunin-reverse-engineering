# Registry rows — draft for `corpus/SOURCES.md` (round 80, ScribeSources)

Draft only. The L1 lands them. Highest id held at `84d68e90` is `S296`
(`grep -oE 'S[0-9]{3,}' corpus/SOURCES.md | sort -u | tail -5` → S292 S293 S294 S295 S296).

## Row 1 — proposed `S297`: append

Source: Python `re` documentation, `\b` entry, anchor `#re-syntax-special-word-boundary`
(fetched 2026-11-04, HTTP 200, 257 722 B, sha256 `24ef5ff0…`, snapshot kept at
`.ufo/waves/round-80/w1/ScribeSources/re.html`).

```
| S297 | Python `re` documentation, `\b` word-boundary assertion — https://docs.python.org/3/library/re.html#re-syntax-special-word-boundary (snapshot `re.html`, 257 722 B, sha256 `24ef5ff00f937cee65b83d527638fe1c1fc573578851e296f4bca0c4da3828a6`, in `.ufo/waves/round-80/w1/ScribeSources/`) | docs | A | the zero-width assertion that a match sits at the beginning or end of a word, where a word is a run of `\w` characters; it grounds the delimited-token vocabulary R80-C1's binder uses, not the frozen alphabet itself (the frozen token characters add `.` and `-` to `\w`, and `\w` on str patterns is Unicode-aware while that alphabet is ASCII-only) and not `re.fullmatch` (S143) | `\b` entry, section id `b`, span id `re-syntax-special-word-boundary`, raw HTML line 746, first sentence at line 747 | `\b` matches only at a boundary between a word character and a non-word character or the string ends, so a declared pin is checked as a delimited token rather than a substring; `.` and `-` are not word characters, so `\b` still bounds inside `rea-agents@6.7.0-rc1` and the frozen rule is deliberately stricter | mined | 2026-11-04 | on-release | .ufo/waves/round-80/w1/ScribeSources/receipt.json |
```

Cell check: 11 cells, no literal or escaped column separator inside a cell.

## Row 2 — proposed `S298`: withhold (refused reuse)

Source: RFC 8259 section 4 Objects, duplicate-names sentence
(fetched 2026-11-04, HTTP 200, 28 360 B, sha256 `61a5378f…` — byte-identical to S289's snapshot;
the requested anchor is already carried by S049).

```
| S298 | RFC 8259 section 4 Objects, duplicate names — https://www.rfc-editor.org/rfc/rfc8259.txt (snapshot `rfc8259.txt`, 28 360 B, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`, in `.ufo/waves/round-80/w1/ScribeSources/`) | spec | A | the object grammar's duplicate-name sentence and the interoperability paragraph that follows it: unique names are a SHOULD, and receivers of a non-unique object behave unpredictably, so the lane's duplicate-cell refusal is its own stricter policy and not an RFC requirement | section 4 Objects, raw line 322 (`grep -n` numbering; splitlines reports 327), interoperability paragraph at raw lines 329-344 | The names within an object SHOULD be unique, and where they are not, receivers disagree (last-wins in many, error or all-pairs in others), so a record declaring the same client cell twice is ambiguous on the sender's side and must be reported as a duplicate rather than collapsed last-wins | mined | 2026-11-04 | 365d | — |
```

Do **not** append this row and do **not** consume an id for it unless the L1 overrules the reuse
verdict; `S298` is then free for the rejected-status row below, which would move from `S299` to `S298`. The ground already exists twice:

- `corpus/SOURCES.md:205` — S289, `https://www.rfc-editor.org/rfc/rfc8259.txt`, same 28 360 B,
  same digest prefix `61a5378f4255c720` that S289 records.
- `corpus/SOURCES.md:55` — S049, `https://www.rfc-editor.org/rfc/rfc8259`, anchor "section 4
  Objects", scope "JSON object member identity and duplicate-name interoperability".

The action that adds value instead: append this receipt path to S049's `used-by` cell, so
R80-C1's duplicate-cell rule is visibly grounded on the row that already carries section 4.

## Optional extra — rejection row (lane precedent S144, S291, S294)

Not one of the two drafted rows; the L1 decides whether the rejection becomes a registry row or
stays in the receipt only. Its id is left unassigned on purpose: assign the next free id at landing (`S298` if the withheld RFC row is
not landed, otherwise `S299`), so the registry keeps no gap.

```
| — | Stack Overflow question 21 802 701, duplicate JSON keys — https://stackoverflow.com/questions/21832701 (content opened through the Stack Exchange API 2.3, snapshots `so-api.json` 1 387 B sha256 79f61b33… and `so-answers.json` 21 102 B sha256 e086dc8b…; the rendered page returned HTTP 403, 5 753 B) | community | C | duplicate JSON names as a Q&A sees them; not the grammar and not a requirement | top answer, score 226: 'Yes but is not recommended' followed by a quotation of RFC 8259 and of BCP 14's SHOULD | REJECTED: the normative sentence is the RFC's, reproduced by quotation, and the page's own contribution is vote-ordered interpretation that drifts without notice. Flip: the claim becomes about observed implementer practice rather than the grammar, and the row then pins the answer's `last_edit_date` and the API snapshot digest. | rejected | 2026-11-04 | 180d | — |
```

## Optional log line (SOURCES.md "Log" section)

```
- 2026-11-04 round 80 — Question: which texts ground R80-C1's two rules, a duplicate-cell refusal and an exact-token delimited match? Where searched: the two known official URLs (rfc-editor.org `rfc8259.txt`, docs.python.org `re.html`), one GET each (HTTP 200; 28 360 and 257 722 bytes), plus one Q&A reached through the Stack Exchange API because its rendered page returned HTTP 403. Identified 3, screened 3, included 1 (S297 `\b`), reused 1 (S049 for the section 4 duplicate-name sentence; S289 already holds the same RFC bytes), excluded 1 (the Q&A, community commentary that quotes the RFC). Stop: the grammar and boundary questions are answered by a primary text each, and the remaining duplicate-key material is a paraphrase of the sentence S049 already carries.
```
