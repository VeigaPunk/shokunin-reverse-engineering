# SOURCES.md cells for the round-80 entry (draft; the L1 lands them)

Entry path the `used-by` cells must name: `corpus/knowledge/2026-11-04-r80-four-bindings.md`.

## S297 — the round's new row (Python `re`, `\b`); disposition `append`

- `used-by`: append `corpus/knowledge/2026-11-04-r80-four-bindings.md`.
- `tier` (trust grade): `A` — the vendor's own reference for the interpreter's `\b` semantics; it
  grounds the boundary *shape*, not this lane's ASCII alphabet.
- `scope`: the zero-width assertion that a match sits at the beginning or end of a word, where a word
  is a run of `\w` characters; grounds the delimited-token vocabulary R80-C1's binder uses, not the
  frozen alphabet itself (the frozen token characters add `.` and `-` to `\w`) and not `re.fullmatch`
  (S143).

## S049 — the held row the duplicate-cell rule cites; no cell change but `used-by`

- `used-by`: append `corpus/knowledge/2026-11-04-r80-four-bindings.md` (current value:
  `corpus/lessons/round-21.md`).
- `tier` (trust grade): `A` — unchanged; RFC 8259 section 4, page 6.
- `scope`: unchanged — "JSON object member identity and duplicate-name interoperability; not REA
  Evidence authenticity or a requirement that every application accept every JSON value". The round-80
  entry relies on exactly this cell, which already names duplicate-name interoperability; a second
  RFC 8259 row for the same section would duplicate it.

## S143 — cited for equality-over-containment; `used-by` append only

- `used-by`: append `corpus/knowledge/2026-11-04-r80-four-bindings.md` (current value:
  `corpus/lessons/round-47.md`).
- `tier` (trust grade): `A` — unchanged.
- `scope`: unchanged — "the exact-match primitive, `re.fullmatch`, which is the equality a token
  clause needs rather than the containment `re.search` gives". The entry cites it for the principle
  and explicitly does *not* claim `fullmatch` can bind a token inside a longer line.

## S298 — withheld (no row, no `used-by`)

The sources seat's `receipt.json` records `disposition: "withhold"` for the RFC 8259 section 4
candidate: the `.txt` URL is already held by S289 with byte-identical bytes (`28 360 B`,
`sha256 61a5378f4255c720…`) and the section-4 anchor is already carried by S049. The id stays
reserved and must not be consumed; no `used-by` value is written for it.
