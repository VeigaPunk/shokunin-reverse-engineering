# C1DocCheck — doc-binding dry run of CTL-C1-POS (round 49 wave 1, pre-freeze)

Run 2026-10-28T21:09Z–21:3xZ UTC. Clone `mkclone.sh` DEV_FREEZE `660f6563b04f76c1b9db1528188ca0300789ffca`
(draft `c1-counter.py` sha256 `d6d70cb7…a95779`, `c1-controls.py` sha256 `209f0f4a…087a4`).
Receipts: `.ufo/waves/round-49/w1/C1DocCheck/receipts/<run>/{run.out,ctl.json,counter.json,receipt.json}`, doc diffs
`…/C1DocCheck/diffs/<mut>.diff`, drivers `mut.py runmut.sh runvar.sh controls-*.py`, table `summary.txt`.

## Verdict
**Baseline binds; the stated "each doc mutation flips exactly its own binding" holds for 4 of 6, and two doc bindings are
vacuous under the draft POS fixture and partly in the counter itself.**
- CTL-C1-POS exits 0, `carriers_matched 4`, `met_target true`, all six boolean doc bindings true (the driver docstring and
  the plan say "five"; the counter has SIX: `province_core_section, province_core_row, frontier_note, entry_present,
  sourced, coverage_map_row`), `opened_source_rows [S138,S139]`.
- Heading, entry path, frontier-note stem, S139 `source:` line, README row each turn red. **Heading removal flips TWO
  bindings** (section + row; the row is read from the section). **Dropping `squashfs_v2` from the row flips NOTHING.**

## Commands (all `cd /fast/scratch/hyaku/kaidoku-r49/C1DocCheck`, `TMPDIR` and `HYAKU_SCRATCH` exported)
Baseline: `…/draft/mkclone.sh $S/clone` (exit 0) then `…/draft/run-ctl.sh $S/clone $S/w0 --controls pos` (stdout sha256
`cdccdf8b…ad60`; POS verdict `as_expected`, ctl exit 0, 15.8 s). Mutation i: `./runmut.sh <m>` = `mut.py` copies the
`w1/artifacts` doc dir to `$S/doc-<m>`, applies ONE change, then `run-ctl.sh $S/clone $S/w-<m> --controls pos --doc-dir
$S/doc-<m>`. Note `run-ctl.sh` itself always exits 0 (its last command is the summary printer); the control exit is
`ctl.json controls.CTL-C1-POS.exit_code` and `ctl-out/pos/counter.json exit_code`. Counter sha256 identical in all runs.

| id | mutation (one change) | counter exit | red bindings | ctl verdict | counter.json sha256 |
|---|---|---|---|---|---|
| w0 | none | 0 | none (matched 4, met) | as_expected | 43a23369…e94ab |
| m1 | delete `## Round-49 additions to Core` line from block-a | 1 | `province_core_section` **and** `province_core_row` | misbehaved | e41f90cb…df74 |
| m2 | replace every `squashfs_v2` in block-a row | **0** | **none (stays green)** | as_expected | 39a67443…999c |
| m3 | replace the entry path in block-a row | 1 | `province_core_row` | misbehaved | 579283cd…ae2a |
| m4 | replace the stem in block-b | 1 | `frontier_note` | misbehaved | d4adda24…ca9 |
| m5 | delete `source: S139` line from entry | 1 | `sourced` | misbehaved | e0c03973…fe6 |
| m6 | block-c (README row) emptied | 1 | `coverage_map_row` | misbehaved | c01ea058…83f |
| m4b | extra: block-b `Round-49 frontier note`→`Round-49 note` | 1 | `frontier_note` | misbehaved | a8eafaa6…e95 |
| m5b | extra: delete `source: S138` line | 1 | `sourced` | misbehaved | 4fe67c2c…33f |
| m6b | extra: block-c stem replaced | 1 | `coverage_map_row` | misbehaved | ed52d3cc…831 |
| m2b | extra: block-a `squashfs_v2`→`squashfs_v2_nonstandard` | **0** | none | as_expected | 7e6c5584…bf6 |
| m3b | extra: remove all "SquashFS v1 and v2"/"SquashFS v1/v2" prose from row | **0** | none | as_expected | 225eb5e2…8e8 |
| m4c | extra: remove "SquashFS v1/v2" prose from block-b (stem kept) | **0** | none | as_expected | 50401839…383 |
| u0 | extra: controls copy with the S138/S139 used-by append disabled (`controls-nousedby.py`) | 1 | `sourced` (`opened_source_rows []`) | misbehaved | 77f1fd27…b4d |

Neutral-headline arm (`controls-neutral.py` = draft controls with the POS `headline` text stripped of every `squashfs`
token; runs `n0, n-m2, n-m2b, n-m3b, n-m4c`):

| id | mutation | exit | red | counter.json sha256 |
|---|---|---|---|---|
| n0 | none | 0 | none | ccc96105…6b2 |
| n-m2 | drop `squashfs_v2` from row | 1 | `province_core_row` | b4484f3b…553 |
| n-m2b | `squashfs_v2` → `squashfs_v2_nonstandard` | **0** | none | d741052e…d69 |
| n-m3b | drop SquashFS v1/v2 prose from row | **0** | none | 0ea33f17…33f |
| n-m4c | drop SquashFS v1/v2 prose from block-b | **0** | none | 446fce21…34f |

## Findings
1. **VACUOUS (control side): `province_core_row` cannot see `squashfs_v2` leaving the row.** `_doc_landing`
   (`c1-controls.py:890-895`) replaces `<AFTER-DATA:…>` with a headline that itself contains `` `squashfs_v1`/`squashfs_v2` ``,
   and the counter checks the whole row (`c1-counter.py:2156-2159`). m2 stays green; with the headline neutralised
   (n-m2) it goes red. Fix: make the POS headline free of handler tokens (or have the counter read only the Surface/Ports
   cells), else the "row names squashfs_v2" clause is not exercised by POS and the real landing's quoted receipt headline
   will also satisfy it.
2. **VACUOUS (counter side): `squashfs_v2` is a substring test** (`'squashfs_v2' in r`). A row naming only
   `squashfs_v2_nonstandard` — the handler the claim says stays Frontier — passes (m2b and n-m2b green, even with the
   neutral headline). Needs a token-boundary regex.
3. **VACUOUS: the "names SquashFS v1/v2" text clause is subsumed.** `SQFS12_TEXT_RE` (`squashfs[ _-]?v?1…`,
   `c1-counter.py:327`) matches `squashfs_v1` in the row and `squashfs-v1v2` inside the entry stem on the frontier-note
   line, so removing all SquashFS v1/v2 prose keeps both bindings green (m3b, m4c, n-m3b, n-m4c). The plan sentence "names
   SquashFS v1/v2" / "a SquashFS v1/v2 token" is not what the code checks.
4. **Heading removal is not single-binding**: m1 reds `province_core_section` and `province_core_row` (rows are taken from
   the section). Fine as design, but the L1 claim "each flips exactly its own binding" should say two for this one.
5. The six per-binding mutations the L1 asked for are otherwise clean: entry path→`province_core_row` only; stem→
   `frontier_note` only; S139 or S138 `source:` line→`sourced` only; README row or its stem→`coverage_map_row` only; the
   used-by append (u0)→`sourced` only. Headline: "five documentation bindings" in `c1-controls.py:864,985` is stale (six).
6. **Stale round-44 text in the landing drafts the counter does not read** (so it cannot catch it): the entry's `status:`
   (header lines 3-10) still cites freeze `c48f8a4b…`, counter sha `9f2cc140…`, `.ufo/waves/round-44/controls/…`; body line
   21 "Round 44 adds the `## Round-49 additions to Core` row"; lines 101 and 248 cite round-44 R44 artifacts; title says
   "(round 44, Core)"; README block-c label says "SquashFS v1/v2 through REA (round 44)". Round 44's claim stopped, so a
   landed entry quoting its receipts as the scored run would repeat the round-44/48 header defect.
7. `sourced` requires `opened == 2026-10-28`; S138/S139 already carry that date (round 44 opened them the same day), so
   the binding is satisfied before any round-49 re-open and does not prove one; only the used-by append is new.
8. `run-ctl.sh` exits 0 unconditionally (summary printer); callers must read `ctl.json`/verdict lines, not `$?`.

## Not run
Full c0-c5 controls (only `--controls pos`); `--from-fixtures`; any data run; mutation of SOURCES `opened`/used-by cells
other than the used-by append.
