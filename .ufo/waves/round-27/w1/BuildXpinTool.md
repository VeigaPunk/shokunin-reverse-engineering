# BuildXpinTool — R27-C2 capability tool build

Seat: `KaidokuR27.BuildXpinTool`. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Round 27, attempt 1, wave 1. Runs on 2026-10-22 UTC. Lane files touched: only this report.

## Tool delivered
- Seat path: `/fast/scratch/hyaku/kaidoku-r27/seats/BuildXpinTool/xpin-attribute.mjs`
- sha256: `8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708`; full source line count: 267
- Node ESM, no runtime dependencies; node v24.21.0.

## Contract behavior
`node xpin-attribute.mjs --pkg65 <root> --pkg67 <root> ENVELOPE...` prints one tab-separated line per
envelope: `<path as given> TAB <stored id> TAB <id65> TAB <id67> TAB <6.5.0|6.7.0|both|none>`.
Exit 0 on success; exit 2 on unreadable input with a stderr message. Evidence record read from `.data`.

Per pin: (1) `digestCanonicalValue` imported from that package's `dist/domain/canonicalDigest.js`;
(2) `semanticProjection` obtained from that package's own `dist/domain/evidence.js` source text — never
retyped; (3) id = `'ev_' + digestCanonicalValue(semanticProjection(record), 'Evidence')`.

`--parse` mode (L1 addition): per envelope prints
`<path> TAB <parseEvidence-6.5.0 accept|reject:<first error message>> TAB <parseEvidence-6.7.0 ...>`,
using each package's exported `parseEvidence`.

## Projection extraction (exact method)

No regex. A character scanner finds the first `const semanticProjection` in `evidence.js`, advances from
the first `=` after it, tracks nesting of `( [ {` / `) ] }` while skipping strings, `//` and `/* */`
comments, ends at the first `;` at depth 0 and returns that whole source span, then evaluates it with
`new Function` returning `semanticProjection`. If the text is not found: `InputError`
(`6.5.0: no "const semanticProjection" definition in evidence.js`) → stderr, exit 2. Same exit-2 path
for unreadable package root, unreadable/unparseable envelope, missing `.data`, projection/digest failure
(all verified).

Extracted statements are the live definitions: 6.5.0 `evidence.js` line 156 (null-coverage spread
`...(evidence.relationship_coverage === null ? {} : {...})`); 6.7.0 `evidence.js` line 159
(unconditional `relationship_coverage: evidence.relationship_coverage`).

## Checker run

```
python3 -I -B tools/round-27/c2-xpin-check.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --rev main --tool-cmd 'node /fast/scratch/hyaku/kaidoku-r27/seats/BuildXpinTool/xpin-attribute.mjs'
```

Output (2026-10-22T15:13:39Z, exit 1):
```
checker attribution of the round-26 envelopes: 6.5.0=21 6.7.0=0 both=3 none=0
r26_rows_ok=24/24 red_ok=3/3 capability_row=0 source_row=1 (S081) rev=c6d619a3c50e39dbb830de28146362e360d170d7
```
- r26_rows_ok=24/24 and red_ok=3/3: targets met.
- exit 1 because capability_row=0 (the SCORECARD `## Capabilities` row naming the tool is the L1's
  later integration step; none exists at current main).
- source_row=1 (S081) at current main: the SOURCES row was committed during the wave; the earlier
  pre-integration main (9dca26df) gave source_row=0 as the card predicted.

## Direct run on the 24 round-26 envelopes

`node ... xpin-attribute.mjs --pkg65 ... --pkg67 ... *.json` in
`corpus/evidence/round-26/c1/envelopes/` (2026-10-22T15:13:46Z, exit 0), saved to
`/fast/scratch/hyaku/kaidoku-r27/seats/BuildXpinTool/r26-direct.tsv`
(sha256 `8ac00521ab63e0e78a6eb2def7998235cc7b053f87258c8b203f8ede5e2012a3`).

Attribution counts (exactly the checker's expected counts): both = 3 (function-base/copy/repeat,
relationship_coverage set); 6.5.0 = 21 (relationship_coverage null); 6.7.0 = 0; none = 0.

`--parse` mode on the same 24 (r26-parse.tsv, sha256
`5b56e1c83b84eae6f7410e4692dde54ffd5757797861109c63b4d1c0692c9b68`): 6.5.0 = 24 accept;
6.7.0 = 3 accept (coverage-set rows), 21 reject with
`Evidence semantic identifier does not match its record` (6.7.0 always includes relationship_coverage,
so null-coverage ids cannot match stored 6.5.0 ids).

## Lane records lacking relationship_coverage (6.4.0-era)

Discovery (read-only git, 2026-10-22T15:07Z):
`git grep -L relationship_coverage main -- 'corpus/**/*.json' 'evidence/**/*.json' '.ufo/**/*.json'`,
filtered to JSON whose `data` has `evidence_id` → 37 files
(`/fast/scratch/hyaku/kaidoku-r27/seats/BuildXpinTool/keyless-main-list.txt`,
sha256 `f426c918b323207b35511319bcc737bb4a4c5f0f538851b9e794e6bdba334930`).

Default mode on the 37 (keyless-default.tsv, sha256
`ccb42b03f6b9e6024d6b102c7d3e7939b05fc19e38664e857e62f29001df8ec0`, exit 0): 37 `both`
(stored == id65 == id67). This follows each package's own JS semantics: the extracted 6.7.0 projection
yields `relationship_coverage: undefined` when the key is absent, and both packages' canonical digest
skips undefined-valued object keys, so both rules equal the stored 6.4.0 id. The tool does not insert null.

`--parse` mode on the 37 (keyless-parse.tsv, sha256
`e44ba85836c57b9a04aac6cd2d683d10fb2e15fc2972c5555dafa380b7b9104f`, exit 0):
6.5.0 = 37 accept (schema `.nullable().default(null)` fills null); 6.7.0 = 37 reject, first error
message `Invalid input: expected object, received undefined` (6.7.0 schema line 116 has no default).

Note: the checker's Python recompute inserts `relationship_coverage=null` for id67, which differs from
6.7.0's own JS on keyless records; the checker exercises only the 24 round-26 envelopes plus 3 red
envelopes (all with the key present), so no conflict. The tool deliberately follows package semantics per
the L1 instruction.

## Committed-form validation (sandbox clone)

Sandbox clone at `/fast/scratch/hyaku/kaidoku-r27/seats/BuildXpinTool/clone2`, tool committed at
`tools/round-27/xpin-attribute.mjs`, checker with default path (no `--tool-cmd`) gave
`r26_rows_ok=24/24 red_ok=3/3` (2026-10-22T15:12:01Z). After the L1 commits the seat copy to
`tools/round-27/xpin-attribute.mjs`, the checker's default tool path works.

## Artifacts (seat dir, sha256)

- `xpin-attribute.mjs` 8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708
- `r26-direct.tsv` 8ac00521ab63e0e78a6eb2def7998235cc7b053f87258c8b203f8ede5e2012a3
- `r26-parse.tsv` 5b56e1c83b84eae6f7410e4692dde54ffd5757797861109c63b4d1c0692c9b68
- `keyless-default.tsv` ccb42b03f6b9e6024d6b102c7d3e7939b05fc19e38664e857e62f29001df8ec0
- `keyless-parse.tsv` e44ba85836c57b9a04aac6cd2d683d10fb2e15fc2972c5555dafa380b7b9104f
- `keyless-main-list.txt` f426c918b323207b35511319bcc737bb4a4c5f0f538851b9e794e6bdba334930

No tooling installs, upgrades or REA runs were made.

## Risks / notes

- 6.7.0 parse rejections of null-coverage round-26 envelopes are expected (6.7.0 rule includes
  relationship_coverage unconditionally).
- Checker exit stays 1 until the capability row and committed tool path at REV exist (L1 integration).
- Envelope paths are printed exactly as given (the checker keys rows on that).
