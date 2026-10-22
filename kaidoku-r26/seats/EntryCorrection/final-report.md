# Round 26 wave 1 — EntryCorrection (scribe): routed defect 4, "138 responses per selector"

Seat: KaidokuR26.EntryCorrection. Read-only on the lane; nothing in the lane was edited except this
report. No REA call, no web source, no tool install, no git/jj write.

Target: routed defect 4 in `corpus/lessons/round-25-verifier-spotcheck.md:193-195`. The entry
`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` says "one complete 4byte.directory
page and one openchain `filter=false` response per selector", but the 138 saved responses are 2 per
carrier-selector row (69 rows), not per distinct selector (43). This seat re-derives 69, 43 and 138
from committed round-25 evidence and drafts the append-only correction; it does not apply the edit
(`corpus/` is read-only here, and the defect asks the lane to land it "in a new commit").

## The old phrase and where it sits

`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`, **line 41** (the phrase wraps onto
line 42). Same line number at the frozen revision `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`, at
lane base `a0639d8e61e486e2a716ff94cddd89a73200a02c` and in the worktree.

```
41:carrier; 138 saved lookup responses (one complete 4byte.directory page and one
42:openchain `filter=false` response per selector, all HTTP 200, every sha256
43:re-checked equal to its manifest). `tools/round-25/a2/resolve-selectors.py`
```

`git blame -L 41,42` attributes both lines to `dc31f9c4` (2026-10-22 06:31:23 -0300).
`git grep -n "one complete 4byte" HEAD -- '*.md'` (exit 0) gives two hits: this entry at line 41 and
the lesson quoting it at `corpus/lessons/round-25-verifier-spotcheck.md:193`. `corpus/README.md:164`
and `LOG.md:2956` state the bare total 138 and are not affected.

## Re-derivation

Read-only, run 2026-10-22T12:17Z–12:19Z UTC. `L` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Every command below exits 0.

**138 = 2 x 69 carrier-selector rows** (all at 2026-10-22T12:18:07Z):

```
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/*' -name '*.json' ! -name 'manifest.json' | wc -l   -> 138
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' | wc -l                                ->  69
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/openchain-*.json' | wc -l                            ->  69
python3 -c "import json,glob;print(sum(len(json.load(open(f))) for f in glob.glob('$L/corpus/evidence/round-25/a2/c2/*/db/manifest.json')))"  -> 138
```

The six per-carrier `db/manifest.json` files hold 16 + 30 + 12 + 10 + 44 + 26 = 138 entries, matching
the six `fetch.txt` receipts (`{"fetched": 16}`, `30`, `12`, `10`, `44`, `26`). All 138 manifest entries
were re-checked: file present, `sha256` equal to the manifest value, `status` 200. Mismatches: 0.

**69 carrier-selector rows.** Each carrier's `db/` directory holds exactly one 4byte page plus one
openchain response per selector of that carrier: carrierb 8+8, carrierv 15+15, kdxtoken 6+6,
rv2token 5+5, stewardtoken 22+22, vaultb-opt200 13+13. 8+15+6+5+22+13 = 69 rows, 138 responses. The
same 69 is carried by the committed offline replay `corpus/evidence/round-25/a3/c2/analyze/<carrier>.json`
(rows per carrier: 8, 15, 6, 5, 22, 13) and by `corpus/evidence/round-25/a3/c2/analyze/tally.json`
(`per_carrier_rows.selector_rows` = 69).

**43 distinct selectors** (2026-10-22T12:18:07Z):

```
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' -printf '%f\n' \
  | sed -E 's/^4byte-(.*)-p[0-9]+\.json$/\1/' | sort -u | wc -l                                        -> 43
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/openchain-*.json' -printf '%f\n' \
  | sed -E 's/^openchain-(.*)\.json$/\1/' | sort -u | wc -l                                            -> 43
```

43 also comes from the committed replay output: the 69 rows carry 43 distinct selector hexes, and
`tally.json` `distinct_selectors.selector_rows` = 43.

**Why 138 is not "per selector".** Per kind, 69 saved responses cover 43 distinct selectors: 16
selectors were fetched for more than one carrier, giving 26 extra copies per kind (69 - 43 = 26). All
copies of a shared selector are byte-identical across carriers (16 of 16, both kinds), so the 138 files
hold 43 distinct 4byte bodies and 43 distinct openchain bodies. The later `filter=true` pass in
`corpus/evidence/round-25/a3/c2/filter-true/` did fetch once per distinct selector (manifest: 43
entries, 43 distinct selectors); the two passes used different units, which is how the round-25 phrase
came to be written loosely. The other half of the old phrase holds: all 69 saved 4byte responses have
`next: null`, so the single saved page per selector is the complete page. **Recheck.**
`python3 -I -B tools/round-25/a3/tally-resolution.py --root $L` → exit 0, stdout JSON-identical to
`corpus/evidence/round-25/a3/c2/analyze/tally.json` (69 rows, 43 distinct). All of the above is
observation.

## Drafted append-only correction (for the lane to land in a new commit)

Append a new section at the end of
`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` (after `## Limits`). Nothing above
is edited; the old sentence stays as history and the new section supersedes it.

```markdown
## Correction (round 26 wave 1): the 138 saved responses are per carrier-selector row

The sentence in "The measured procedure" (line 41) — "138 saved lookup responses (one complete
4byte.directory page and one openchain `filter=false` response per selector, all HTTP 200, every
sha256 re-checked equal to its manifest)" — is wrong in one word: "per selector". It reads as one
pair of responses per distinct selector, which would be 86. The 138 responses are two per
carrier-selector row, and there are 69 such rows over the six carriers; the six carriers use 43
distinct selectors. A selector shared by three carriers therefore contributes six saved responses,
not two.

Command (read-only, committed evidence under `corpus/evidence/round-25/a2/c2/`):

    find corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' | wc -l        # 69
    find corpus/evidence/round-25/a2/c2 -path '*/db/openchain-*.json' | wc -l    # 69
    find corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' -printf '%f\n' \
      | sed -E 's/^4byte-(.*)-p[0-9]+\.json$/\1/' | sort -u | wc -l            # 43

69 rows x 2 responses = 138 saved responses; 138 = 2 x 69 carrier-selector rows, not 2 x 43
distinct selectors. Per kind, 16 of the 43 selectors were fetched for more than one carrier
(26 extra copies); those copies are byte-identical across carriers, so the 138 files hold 43
distinct 4byte bodies and 43 distinct openchain bodies. All 138 manifest entries still re-check
equal to their manifest `sha256` with `status` 200. `corpus/evidence/round-25/a3/c2/analyze/
tally.json` carries the same pair: `per_carrier_rows.selector_rows` = 69 and
`distinct_selectors.selector_rows` = 43. Nothing else in the entry changes: the rule scores are per
carrier row (69) and per distinct selector (43) as stated, and the `filter=true` re-fetch under
"Limits" was already once per distinct selector (43 responses in
`corpus/evidence/round-25/a3/c2/filter-true/manifest.json`).
```
Quoted from `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md:41-42`.

## Out of scope, and one adjacent observation

Applying the edit to `corpus/knowledge/…` (read-only for this seat; the lane owns the commit);
`corpus/README.md:164` and `LOG.md:2956` (bare total 138, correct as written); the other routed
defects (1, 2, 3, 5, 6, 7); REA replay and live lookups (none needed). Adjacent (not part of the
defect): the entry's `recheck:` line claims the tool's output "equals
`corpus/evidence/round-25/a3/c2/analyze/tally.json`", but the tool prints a trailing newline while the
committed file has none, so stdout is JSON-identical but not byte-identical (8325 vs 8324 bytes, sha256
`7e02dbbe…` vs `479bc13e…`); a byte-comparing recheck would report a false mismatch.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/EntryCorrection/)

derive-counts.py 1726e40ee2f43f42ad5d438e112886d563654b0f2e2c585603abb01349a0a218;
derive-counts.out 804d0b545ae2ec833f19b0a9ea38288a3caa7d3ccc965108354122f821e43c80 (stdout, exit 0,
2026-10-22T12:17:19Z); per-selector-copies.txt 164116f9e7e1d3a5a031499562e71a668d8081ce71b64eabfba26f1b40205266.
Tool installs: none. Sources opened: none (all evidence is local committed bytes).
