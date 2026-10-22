# EntryNumbers — attack of the routed-defect-4 correction numbers (kaidoku round 26, wave 1)

Seat: KaidokuR26.EntryNumbers (reviewer leaf). Date 2026-10-22. Lane
/home/vgpnk/Projects/shokunin/kaidoku-shokunin, HEAD `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`,
entry working tree clean (`git status --porcelain` on the entry: empty, exit 0).
Target attacked: the routed-defect-4 correction statement in
`corpus/lessons/round-25-verifier-spotcheck.md:193-195` — "the 138 responses are 2 per
carrier-selector row (69 rows), not per distinct selector (43)" — against the committed
evidence under `corpus/evidence/round-25/`. Lane untouched; no REA run was needed for this
item. No tools installed.

## Verdict

**Holds.** All three numbers reproduce from the committed bytes with independent commands
(the lane tally tool was not reused): 69 carrier-selector rows, 43 distinct selectors,
138 saved responses, and the 138 are exactly 2 per row (one `4byte-<sel>-p0.json` plus one
`openchain-<sel>.json` per carrier-selector row), not 2 per distinct selector (which would
be 86). One adjacent defect found in the same sentence that carries the 69/43 explanation:
"shared ERC-20 selectors appear in up to four carriers" overstates the measured maximum,
which is three.

## Number 1 — 69 carrier-selector rows (observation)

Command: `python3 /fast/scratch/hyaku/kaidoku-r26/seats/EntryNumbers/derive_counts.py`
(own script; parses each of the six committed envelopes' `normalized_result.functions`,
selector normalized by lowercasing and stripping `0x`; cross-checks `raw_result.functions`;
checks no duplicate selector inside a carrier). Run 2026-10-22T12:16:20Z, exit 0.

```
carrier rv2token: 5 functions ... kdxtoken: 6 ... vaultb-opt200: 13 ... carrierb: 8
... stewardtoken: 22 ... carrierv: 15
ROWS (carrier,selector): 69
```

5+6+13+8+22+15 = 69; no in-carrier duplicates; raw and normalized function lists agree on
all six carriers. Per-carrier order taken from `a2/c2/carriers.tsv`.

## Number 2 — 43 distinct selectors (observation)

Same run, same command:

```
DISTINCT selectors: 43
selector -> number-of-carriers histogram: {1: 27, 2: 6, 3: 10}
```

27 + 6·2 + 10·3 = 69 rows — internally consistent. Independent corroboration (second
command, run 2026-10-22T12:18:27Z, exit 0): the 43 `openchain-*.json` files in
`corpus/evidence/round-25/a3/c2/filter-true/` (the later `filter=true` re-fetch of all
distinct selectors) have exactly the same selector set as the 43 derived from the
envelopes (`filter-true openchain files: 43; set == 43 distinct envelope selectors: True`).

## Number 3 — 138 saved responses (observation)

Same run, same command; counts files in the six `a2/c2/<carrier>/db/` directories
(excluding `manifest.json`), recomputes sha256 of every file against its manifest entry,
and checks that every row has both expected files:

```
carrier rv2token: manifest entries 10, response files 10 ... kdxtoken 12/12,
vaultb-opt200 26/26, carrierb 16/16, stewardtoken 44/44, carrierv 30/30
RESPONSE FILES total: 138 (manifest entries 138)
sha256: every response file matches its manifest entry
per-row files: every (carrier,selector) row has both 4byte-<sel>-p0.json and openchain-<sel>.json
cross-check 2 x rows = responses: 138 vs 138
```

All 4byte files are `-p0` (no second pages); file set equals manifest set per carrier;
no unexpected files. So 138 = 2 × 69 rows. Note: only 86 distinct file names exist
(43 selectors × 2 databases) — the per-row duplication is what makes 138.

## Verdict on the spot-check's statement (holds, with one adjacent defect)

- The defect it names is real and still present at HEAD: entry lines 41-42 read
  "138 saved lookup responses (one complete 4byte.directory page and one openchain
  `filter=false` response per selector, all HTTP 200, ...)" (read at
  `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md:40-43`; identical bytes
  at `cce7504a`, `git show ... | grep` exit 0). Read as "per distinct selector" that
  predicts 2 × 43 = 86 responses; the evidence holds 138. [observation]
- The correction's numbers are exact: 69 rows, 43 distinct, 138 responses, 2 per row. [observation]
- Adjacent defect, same sentence family (entry lines 49-54): "The first number is per
  carrier row (69 rows); the number in brackets is per distinct selector (43), because
  shared ERC-20 selectors appear in up to four carriers." Measured sharing maximum is
  **three** carriers, not four (histogram `{1: 27, 2: 6, 3: 10}`; none of the 43 selectors
  appears on four carriers; e.g. `095ea7b3`: rv2token, kdxtoken, stewardtoken — 3). As a
  statement of the observed maximum the word "four" is wrong; it is only defensible as a
  loose upper bound, which does not fit the entry's count-reporting style. Recommend the
  correction commit change "four" to "three" together with lines 41-42. [observation;
  author's intent otherwise unknown]

## Other locations of the wording

Grep patterns used: `per selector|per distinct selector` and
`138 (saved|lookup|response|responses|lookups)|response per selector`, over the entry,
`corpus/README.md`, the corpus tree and the lane top-level registers, plus a full read of
the entry, its README rows and the `r25-evm-selector-name-resolution` references
(`grep -rln` over CORPUS.md LEARNING.md PROVINCE.md SOURCES.md QUALITY.md LOG.md
SCORECARD.md SHONEN.md corpus/README.md corpus/knowledge/ corpus/lessons/ → hits only in
PROVINCE.md, SCORECARD.md, README.md, the spot-check lesson; run 2026-10-22T12:2xZ, exit 0).

1. `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md:41-42` — the defective
   sentence itself ("... response per selector ..."). This is the one place to fix.
2. Same entry, lines 50-51 — "per carrier row (69 rows); ... per distinct selector (43)":
   correct senses, numbers verified above; only the "four carriers" clause is wrong (above).
3. `corpus/lessons/round-25-verifier-spotcheck.md:193-195` — quotes the wording as the
   routed defect; historical record, quote must stay as-is.
4. `corpus/README.md:74` — "six lane-compiled carriers (69 selector rows)": carrier-row
   sense, 69 verified; no change needed.
5. `corpus/README.md:164` — "138 saved lookups with sha256": number only, 138 verified;
   no per-selector claim; no change needed.
6. `LOG.md:2956` — "saved 138 signature-database lookups": number only, verified; no change.
7. `PROVINCE.md:93` and `SCORECARD.md:3055` — reference the entry with no counts; nothing to fix.
8. No other sentence in the entry or `corpus/README.md` repeats the per-selector wording.
9. Outside corpus (frozen wave records, listed for completeness, out of correction scope):
   `.ufo/waves/round-25/a3/w1/` seat reports (C2EntryNumbers, C2AbiTruth, EvidenceIntegrity,
   Sentinel, C2FilterTrue, C2LiveDrift, C2HasVerified, C2IndependentKeccak,
   C2IndependentTally all state 138; SourcesOverlap.md:85 "69 of the 138 saved lookups")
   and the wave dispatch/spec JSONs — all use the number correctly or as task text; none
   asserts the per-distinct-selector reading.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/EntryNumbers/)

- `derive_counts.py` sha256 `3e30422855438460a9e6ad7198305988232fe7716373d102cc27a35528558a0b`
- `derive_counts.out` sha256 `c7b4f18f2f578a2c74f0a9a157dcf54323fa97039b69e77b7d58341a71a4edb0`
- `wording_checks.out` sha256 `77e16e86760f4e646ee7e523bbd33bd5d2a0747d13e1108834ddbfeb94f9c703`

## Residual risk and verification gaps

- Rows are defined by the committed REA envelopes; envelope-vs-ABI selector consistency was
  not re-derived here (r25 EvidenceIntegrity seat covered it; not re-attested by me).
- My integrity check verified sha256-vs-manifest for all 138 and per-row file presence; it
  did not re-check manifest URL shape or the `status: 200` fields (r25 seats did).
- The lane-wide wording search is pattern-based (`per selector`, `138 ...`); a paraphrase
  without those tokens outside the entry and README would not be caught. Within the entry
  and README the check is complete by full read.
- Whether "up to four carriers" was meant as a loose bound (author intent) is unknown;
  the measured maximum is three.
