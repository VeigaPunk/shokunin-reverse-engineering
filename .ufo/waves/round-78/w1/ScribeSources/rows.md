# Round-78 SOURCES rows — S292, S293 (mined), S294 (rejected)

Registry schema (11 columns): `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.
Access date **2026-11-04**. Snapshots: `.ufo/waves/round-78/l1/sources/`. Every byte count and sha256
below was re-measured by this seat from the committed blobs at HEAD
`ffcb47d13f0340f88397af6c8d2707a9554abab3`; every quote is a literal contiguous excerpt with its
`grep -n` snapshot line (`shots.txt`). `HTTP 200` inside an anchor cell is the landing's recorded fetch
status, not a re-fetch by this seat.

## 1. The two mined rows (ready to append)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S292 | `Numeric Types — int, float, complex`, Python 3 standard library — https://docs.python.org/3/library/stdtypes.html (snapshot `stdtypes.html`, 814 496 B, sha256 `16f072e19fed1d1ab8ed34468cd6365fad7b7d2013eccd0e298cc6f43797acf1`, in `.ufo/waves/round-78/l1/sources/`) | docs | A | Booleans are a subtype of integers; grounds the type-strict receipt guard (`isinstance(x, int) and not isinstance(x, bool)`) the two receipt contracts need, not a claim about JSON's own taxonomy (S289) or about a receipt's schema | Numeric Types, snapshot lines 440-441; located quote at line 441: "In addition, Booleans are a subtype of integers" (8 words); Python 3.15.2 docs, fetched 2026-11-04, HTTP 200 | A boolean is an int to `isinstance`, so an integer field must exclude it explicitly; the guard is `check_receipt_like` in `tools/round-78/attack-gate.py` and `check_receipt` in `tools/round-77/prefile-receipt.py` | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r78-attack-gate.md |
| S293 | `tomllib — Parse TOML files`, Python 3 standard library — https://docs.python.org/3/library/tomllib.html (snapshot `tomllib.html`, 34 923 B, sha256 `d98e62f75b3a673e6977b4f1fe48eb6b518f77242f434148177e1679d701d53a`, in `.ufo/waves/round-78/l1/sources/`) | docs | A | A read-only TOML parser: `load`/`loads` parse TOML 1.1.0 and the module does not write; grounds reading the Kimi config's `rea` entry instead of grepping its text | Module introduction, snapshot lines 221-223; located quote at line 221: "This module provides an interface for parsing TOML 1.1.0 … This module does not support writing TOML." (17 tokens incl. the ellipsis); Python 3.15.2 docs, fetched 2026-11-04, HTTP 200 | The Kimi pin is read with `tomllib.loads` and `mcp_servers.rea.args`; a parse failure is an unparsed id, never a pass, and the file is never written | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r78-surface-recheck.md |

Both rows are already present in the working tree at `corpus/SOURCES.md:209-210`. The text above is the
pinned replacement, and it differs from that copy only in the anchor cell: the located span is
`lines 440-441` for S292 (the landed cell says `line 441`) and `lines 221-223` for S293 (the landed cell
says `line 221`), because the quoted sentence starts on the earlier line. Every other cell is verbatim
the landed text.

`used-by` is exactly the one admitted knowledge entry that cites each row, checked at its front matter:

```
corpus/knowledge/2026-11-04-r78-attack-gate.md:1:source: S292 — https://docs.python.org/3/library/stdtypes.html — Python 3.15.2 docs, Numeric Types, line 441; opened 2026-11-04
corpus/knowledge/2026-11-04-r78-surface-recheck.md:1:source: S293 — https://docs.python.org/3/library/tomllib.html — Python 3.15.2 docs, module introduction, line 221; opened 2026-11-04
```

## 2. The third slot (S294) — the plan's source is blocked by S143

The frozen plan (`plans/round-78-claims.md:132-133`) names `re.html` for S294:

> Sources: three new rows opened this round (S292 `stdtypes.html`, S293 `tomllib.html`, both mined;
> S294 `re.html`, rejected).

Measured facts:

- `re.html` is committed at the declaration commit and at HEAD: 257 722 B, sha256
  `24ef5ff00f937cee65b83d527638fe1c1fc573578851e296f4bca0c4da3828a6`; located quote at line 283.
- Its URL is already S143's (`corpus/SOURCES.md:149`, mined for `re.fullmatch`). The census reports a
  repeated URL as W04, and the round-75 lesson withdrew S283 for exactly this ground — same page, same
  exact-match scope, "ids are not reused, so S283 stays a gap"
  (`corpus/lessons/round-75.md:24,38`).
- In the working tree at `2026-11-04T09:10Z` the `re.html` snapshot is deleted (uncommitted; still
  committed at HEAD) and S294 is occupied by a different rejected source, the GnuPG handbook.

### 2a. Draft of the plan's row (not appendable as things stand)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S294 | `re — Regular expression operations`, Python 3 standard library — https://docs.python.org/3/library/re.html (snapshot `re.html`, 257 722 B, sha256 `24ef5ff00f937cee65b83d527638fe1c1fc573578851e296f4bca0c4da3828a6`, in `.ufo/waves/round-78/l1/sources/`) | docs | C | Regular-expression syntax and matching semantics, screened as the authority for the record's verdict grammar and refused: the frozen grammar defines what the record admits | Regular expression syntax, snapshot line 283: "A regular expression (or RE) specifies a set of strings that matches it" (13 words); Python 3.15.2 docs, fetched 2026-11-04, HTTP 200 | REJECTED: the page defines what a pattern matches, not what the record's grammar admits; citing it would license "the regex decides the record" when the frozen grammar (`QUALIFIED_ATOM_RE`, the rule table) does. The URL also duplicates S143, which already mines `re.fullmatch` for the exact-match scope, so a second row adds a duplicate URL, not a second meaning. Flip: a claim needs an `re` fact S143's anchor does not cover and the frozen grammar cannot settle (a documented syntax restriction that changes an admitted atom), or a re-open shows S143's anchor no longer holds. | rejected | 2026-11-04 | 180d | — |

Blockers, in order: (i) S294 is occupied in the working tree by the GnuPG row; (ii) the URL duplicates
S143, so appending draws a W04 duplicate-URL warning and adds no second meaning; (iii) the snapshot is
currently deleted from the working tree (committed at HEAD, absent on disk).

### 2b. The row that currently occupies S294 (verified, not drafted by this seat)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S294 | `The GNU Privacy Handbook`, GnuPG — https://www.gnupg.org/gph/en/manual.html (snapshot `gnupg-manual.html`, 113 892 B, sha256 `6d8e63bd2ece3f6f2f7d222c9bd9c06a166e1de5fdc0b44d8cc1ead109abb8f6`, in `.ufo/waves/round-78/l1/sources/`) | docs | C | Digital-signature semantics, screened as the authority for signed receipts (the round-78 Still-Frontier item) | Digital signatures, snapshot line 1017: "A signature is created using the private key of the signer" (12 words); fetched 2026-11-04, HTTP 200 | REJECTED: a signature authenticates possession of a private key, not the receipt's field contents; the lane holds no signing key, has no signer identity to record, and its in-round binding (`rev` + `instrument.sha256` re-derived from the blob) is provenance of the producing bytes, which this row cannot upgrade. Flip: an operator-owned signing key exists and the lane records its fingerprint and a verification command | rejected | 2026-11-04 | 180d | - |

Verification: 113 892 B and sha256 `6d8e63bd…` match the snapshot; the quote sits at line 1017; the
reason and the flip are both present. Two cosmetic deviations from the registry's own conventions: the
`used-by` cell is `-` where S291 (rejected) uses `—`, and the anchor's word count says 12 while the
quoted string has 11 words (`shots.txt` §7, `report.json`).

## 3. Resolution (the L1 decides; this seat wrote no lane file)

Two admissible outcomes, with their consequences:

1. **Keep the landing.** S294 stays the GnuPG reject; `re.html` is recorded in the lesson's Gate block
   as *screened and withheld* for S143's duplicate URL (S283 precedent; no id consumed). The plan's
   sentence at `plans/round-78-claims.md:132-133` then functions as a screening record, and the lesson
   must not claim that a `re.html` row entered.
2. **Keep the plan's letter.** S294 becomes the `re.html` reject and the GnuPG row moves to S295. This
   is only still possible because the working tree is uncommitted; once landed, ids are not reused. The
   S143 duplicate-URL warning remains either way and must be stated in the Gate block.

No third option exists: appending a second row for the same URL violates the withdrawal precedent, and
reusing a committed id is forbidden by the same convention.
