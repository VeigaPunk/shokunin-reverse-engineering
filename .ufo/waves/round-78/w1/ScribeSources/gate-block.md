## Gate

Every source below was screened this round; the three Python pages were fetched by the landing on
**2026-11-04** (HTTP 200 as recorded in the rows) and the GnuPG page likewise. Byte counts and sha256s
were re-measured from the committed blobs at `ffcb47d1` and every quote is a literal contiguous
excerpt with its `grep -n` snapshot line (`.ufo/waves/round-78/w1/ScribeSources/shots.txt`). This seat
re-fetched nothing.

| source / decision | URL | accessed | located quote (≤25 words) | digestion |
|---|---|---|---|---|
| S292, `Numeric Types — int, float, complex`, admit (mined) | https://docs.python.org/3/library/stdtypes.html | 2026-11-04 (814 496 B, sha256 `16f072e19fed1d1ab8ed34468cd6365fad7b7d2013eccd0e298cc6f43797acf1`) | "In addition, Booleans are a subtype of integers" (8 words; snapshot lines 440-441, `grep -n "subtype of integers"` line 441) | `isinstance(True, int)` is true, so an integer receipt field must exclude booleans explicitly: the guards are `check_receipt` (`tools/round-77/prefile-receipt.py:134`) and `check_receipt_like` (`tools/round-78/attack-gate.py:538`). Grounds the guard, not JSON's value taxonomy (S289) and not a receipt schema. |
| S293, `tomllib — Parse TOML files`, admit (mined) | https://docs.python.org/3/library/tomllib.html | 2026-11-04 (34 923 B, sha256 `d98e62f75b3a673e6977b4f1fe48eb6b518f77242f434148177e1679d701d53a`) | "This module provides an interface for parsing TOML 1.1.0 … This module does not support writing TOML." (17 tokens incl. the ellipsis; snapshot lines 221-223, `grep -n` lines 221 and 223) | The Kimi pin is read with `tomllib.loads` (`tools/round-78/surface-recheck.py:148`) from `mcp_servers.rea.args`; a parse failure is an `unparsed` id, never a pass, and the file is never written. Grounds parse-not-grep reading of the live config, not the config's schema. |
| S294, `The GNU Privacy Handbook`, reject (screened for signed receipts) | https://www.gnupg.org/gph/en/manual.html | 2026-11-04 (113 892 B, sha256 `6d8e63bd2ece3f6f2f7d222c9bd9c06a166e1de5fdc0b44d8cc1ead109abb8f6`) | "A signature is created using the private key of the signer" (11 words; snapshot line 1017; the row's anchor cell states 12) | REJECTED: a signature authenticates possession of a private key, not the receipt's field contents; the lane holds no signing key and no signer identity, and its binding (`rev` + `instrument.sha256` re-derived from the blob) is provenance of the producing bytes, which this page cannot upgrade. Flip: an operator-owned signing key exists and the lane records its fingerprint and a verification command. |
| `re.html`, screened, withheld — no row (the frozen plan named it for S294) | https://docs.python.org/3/library/re.html | 2026-11-04 (257 722 B, sha256 `24ef5ff00f937cee65b83d527638fe1c1fc573578851e296f4bca0c4da3828a6`) | "A regular expression (or RE) specifies a set of strings that matches it" (13 words; snapshot line 283) | WITHHELD, not registered: S143 (`corpus/SOURCES.md:149`) already mines this exact URL for the exact-match scope (`re.fullmatch`), and the round-75 lesson withdrew S283 on the same ground — "ids are not reused, so S283 stays a gap" (`corpus/lessons/round-75.md:24,38`). The page defines what a pattern matches, not what the record's grammar admits. Flip: a claim needs an `re` fact S143's anchor does not cover and the frozen grammar cannot settle, or a re-open shows S143's anchor no longer holds. |

**Census.** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exits 0 with
23 W04 duplicate-URL warnings — the same count as the round-77 start — and no warning names S292,
S293, S294, `gnupg` or `re.html` (`grep -c` on the census output: 0). At HEAD the id scan returns 197
rows with S291 the highest; the working tree carries S292-S294 (200 ids, no duplicate id).

**Plan reconciliation.** The frozen plan (`plans/round-78-claims.md:132-133`) said "S294 `re.html`,
rejected"; the landing put a different reject in that slot (the GnuPG handbook) after the duplicate-URL
check saw S143 (`l1/pre-append-url-check.txt`). The third source is therefore a *withdrawal*, not a
row: `re.html` was opened, screened, and refused on authority and on the S143 duplicate. Row texts and
the collision evidence: `.ufo/waves/round-78/w1/ScribeSources/rows.md`.
