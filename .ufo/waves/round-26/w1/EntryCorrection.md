# Round 26 wave 1 - EntryCorrection (scribe): routed defect 4, "138 responses per selector"

Seat: KaidokuR26.EntryCorrection. Read-only on the lane; only this report was written. No REA
call, no web source, no tool install, no git/jj write.

Target: routed defect 4 in `corpus/lessons/round-25-verifier-spotcheck.md:193-195`. The entry
`corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md` says "one complete 4byte.directory
page and one openchain `filter=false` response per selector", but the 138 saved responses are 2 per
carrier-selector row (69 rows), not per distinct selector (43). This seat re-derives 69, 43 and 138
from committed round-25 evidence and drafts the append-only correction; it does not apply the edit
(`corpus/` is read-only here; the defect asks the lane to land it "in a new commit").

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
and `LOG.md:2956` state the bare total 138 and are unaffected.

## Re-derivation

Read-only, run 2026-10-22T12:17Z-12:19Z UTC. `L` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Every command below exits 0.

**138 = 2 x 69 carrier-selector rows** (all at 2026-10-22T12:18:07Z):

```
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/*' -name '*.json' ! -name 'manifest.json' | wc -l   -> 138
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' | wc -l                                ->  69
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/openchain-*.json' | wc -l                            ->  69
python3 -c "import json,glob;print(sum(len(json.load(open(f))) for f in glob.glob('$L/corpus/evidence/round-25/a2/c2/*/db/manifest.json')))"  -> 138
```

The six per-carrier `db/manifest.json` files hold 16 + 30 + 12 + 10 + 44 + 26 = 138 entries, matching
the six `fetch.txt` receipts (`{"fetched": 16}`, `30`, `12`, `10`, `44`, `26`); all 138 manifest entries
were re-checked (file present, `sha256` equal to the manifest value, `status` 200), mismatches 0.

**69 carrier-selector rows.** Each carrier's `db/` directory holds exactly one 4byte page plus one
openchain response per selector of that carrier: carrierb 8+8, carrierv 15+15, kdxtoken 6+6,
rv2token 5+5, stewardtoken 22+22, vaultb-opt200 13+13. 8+15+6+5+22+13 = 69 rows, 138 responses. The
committed offline replay `corpus/evidence/round-25/a3/c2/analyze/<carrier>.json` and `analyze/tally.json`
agree (rows per carrier 8, 15, 6, 5, 22, 13; `per_carrier_rows.selector_rows` = 69).

**43 distinct selectors** (2026-10-22T12:18:07Z); the committed replay agrees (69 rows, 43 distinct selector hexes; `tally.json` `distinct_selectors.selector_rows` = 43):

```
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' -printf '%f\n' \
  | sed -E 's/^4byte-(.*)-p[0-9]+\.json$/\1/' | sort -u | wc -l                                        -> 43
find $L/corpus/evidence/round-25/a2/c2 -path '*/db/openchain-*.json' -printf '%f\n' \
  | sed -E 's/^openchain-(.*)\.json$/\1/' | sort -u | wc -l                                            -> 43
```

**Why 138 is not "per selector".** 16 of the 43 selectors were fetched for more than one carrier
(26 extra copies per kind); the correction block below gives the full arithmetic. All 69 saved 4byte
responses have `next: null`, so each page is complete. **Recheck.** `python3 -I -B
tools/round-25/a3/tally-resolution.py --root $L` exits 0, stdout JSON-identical to
`corpus/evidence/round-25/a3/c2/analyze/tally.json` (69 rows, 43 distinct); all of the above is
observation.

## Drafted append-only correction (for the lane to land in a new commit)

Append a new section at the end of `corpus/knowledge/2026-10-22-r25-evm-selector-name-resolution.md`
(after `## Limits`); nothing above is edited and the new section supersedes it.

```markdown
## Correction (round 26 wave 1): the 138 saved responses are per carrier-selector row

The sentence in "The measured procedure" (line 41) — "138 saved lookup responses (one complete
4byte.directory page and one openchain `filter=false` response per selector, all HTTP 200, every
sha256 re-checked equal to its manifest)" — is wrong in one word: "per selector". It reads as one
pair of responses per distinct selector, which would be 86. The 138 responses are two per
carrier-selector row: there are 69 such rows over the six carriers, which use 43 distinct
selectors, so a selector shared by three carriers contributes six saved responses, not two.

Command (read-only, committed evidence under `corpus/evidence/round-25/a2/c2/`):

    find corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' | wc -l        # 69
    find corpus/evidence/round-25/a2/c2 -path '*/db/openchain-*.json' | wc -l    # 69
    find corpus/evidence/round-25/a2/c2 -path '*/db/4byte-*.json' -printf '%f\n' \
      | sed -E 's/^4byte-(.*)-p[0-9]+\.json$/\1/' | sort -u | wc -l            # 43

138 = 2 x 69 carrier-selector rows, not 2 x 43 distinct selectors: 16 of the 43 selectors were fetched
for more than one carrier (26 extra copies per kind), byte-identical across carriers, so the 138 files
hold 35 distinct 4byte bodies (43 - 9 + 1: nine selectors return the same empty 4byte page) and 43
distinct openchain bodies. All 138 manifest entries still re-check equal to their manifest `sha256`
with `status` 200, and `corpus/evidence/round-25/a3/c2/analyze/tally.json` carries the same pair:
`per_carrier_rows.selector_rows` = 69 and `distinct_selectors.selector_rows` = 43. Nothing else in the
entry changes: the rule scores are per carrier row (69) and per distinct selector (43) as stated.
```

## Out of scope, and one adjacent observation

**Finding against the landed text at HEAD (`c3277726`).** It says the 138 files hold "43 distinct
4byte bodies and 43 distinct openchain bodies". The 4byte half is wrong: the 69 saved 4byte files
carry 43 distinct selectors but only **35** distinct bodies, because the nine selectors with no
candidate all return the same empty page `{"count":0,"next":null,"previous":null,"results":[]}`
(sha256 `0595424161ea8638…`); 43 - 9 + 1 = 35. The openchain half is right (43). Command:
`python3 -c "import glob,hashlib;print(len({hashlib.sha256(open(f,'rb').read()).hexdigest() for f in glob.glob('corpus/evidence/round-25/a2/c2/*/db/4byte-*.json')}))"`
→ 35 (exit 0, 2026-10-22T12:56Z). A one-word fix ("43" → "35"); the 69 / 43 / 138 counts are
unaffected, and I did not apply it: `corpus/` is read-only for this seat.

Applying the edit to `corpus/knowledge/…` (read-only for this seat; the lane owns the commit);
`corpus/README.md:164` and `LOG.md:2956` (bare total 138, correct as written); the other routed
defects (1, 2, 3, 5, 6, 7); REA replay and live lookups (none needed). Adjacent (not part of it): the entry's
`recheck:` line claims the tool's output "equals
`corpus/evidence/round-25/a3/c2/analyze/tally.json`", but the tool prints a trailing newline while
the committed file has none, so stdout is JSON-identical but not byte-identical (8325 vs 8324 bytes, sha256
`7e02dbbe…` vs `479bc13e…`); a byte-comparing recheck reports a false mismatch.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/EntryCorrection/)

derive-counts.py 1726e40ee2f43f42ad5d438e112886d563654b0f2e2c585603abb01349a0a218;
derive-counts.out 804d0b545ae2ec833f19b0a9ea38288a3caa7d3ccc965108354122f821e43c80 (stdout, exit 0,
2026-10-22T12:17:19Z); per-selector-copies.txt 164116f9e7e1d3a5a031499562e71a668d8081ce71b64eabfba26f1b40205266;
build_report.py c32557faba00aca571bf52248c93b32518a8d18b05576c98cd1e46f045164048 (assembles this file).
No tool installs; no sources opened (local committed bytes only).