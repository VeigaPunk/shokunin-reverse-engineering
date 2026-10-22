# CounterC1 — R26-C1 counting instrument (round 26, wave 1)

Seat `KaidokuR26.CounterC1` (executor, leaf). Lane
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Frozen rules:
`.ufo/waves/round-26/claims.json`, claim `R26-C1` `rules`, frozen at
`c27f445e70cedbaf5300b2fd0a53e821d9b659a9` before any table REA run. The L1
committed the instrument at `bd0c84bc` and the R26-C1 landing at `ebe2cb4a`;
the script was not changed after that, and every known defect is listed below
rather than fixed, per the L1's instruction.

## Deliverable

`/fast/scratch/hyaku/kaidoku-r26/seats/CounterC1/c1-id-identity.py`, sha256
`11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa`
(byte-identical to `tools/round-26/c1-id-identity.py` in commit `bd0c84bc`).
Standard library only, runs under `python3 -I -B`. CLI `--root <LANE> --rev
<REV>`, plus `--selftest` and `--mutants <final_table.json>`. Exit 0 iff
`rows_complete == 8 and entry_ok == 1`, exit 1 otherwise, exit 2 on usage
error / unresolvable rev. Reads only Git objects (`git show REV:path`,
`git ls-tree`); never writes.

Artifacts under `seats/CounterC1/` (sha256): `out/selftest.txt` `208a14f3…ee882b`;
`out/real-a0639d8e…02c.json` `fcb49c34…5363bd`; `out/real-c27f445e…59a9.json`
`27906956…22cb74`; `out/real-landing-ebe2cb4a.json` `76141980…be552a`;
`out/mutants.json` `6089bf85…945ac0c`; `out/run-real-data.json` `3893fb6c…eea1e5b`;
`out/run-real-green.json` `75f8e6a6…13bb2b`. All four `.stderr` files are
empty (`e3b0c442…7852b855`).

## Evidence 1 — the two required real runs (2026-10-22T12:44:04Z)

`python3 -I -B c1-id-identity.py --root <lane> --rev <REV>`

```
--rev a0639d8e61e486e2a716ff94cddd89a73200a02c  -> exit 1
{"rev":"a0639d8e61e486e2a716ff94cddd89a73200a02c","rows_total":8,"rows_complete":0,"entry_ok":0,"exit":1}
--rev c27f445e70cedbaf5300b2fd0a53e821d9b659a9  -> exit 1
{"rev":"c27f445e70cedbaf5300b2fd0a53e821d9b659a9","rows_total":8,"rows_complete":0,"entry_ok":0,"exit":1}
```

Every row reason `table_missing`; entry reason `entry_missing`. Matches the
expected `rows_complete 0`, `entry_ok 0`, exit 1. **Observation.**

## Evidence 2 — selftest (exit 0, 16 cases, 0 failures; full output `out/selftest.txt`)

Each case builds a temp Git repo with synthetic fixtures, commits it and runs
the CLI against `HEAD`. `exit / rows_complete / entry_ok`, all PASS:

```
green 0/8/1 · missing_envelope 1/7/1 · envelope_ok_false 1/7/1
wrong_subject_sha256 1/7/1 · id_cell_mismatch 1/7/1 · wrong_verdict 1/7/1
unknown_verb 1/7/1 · duplicate_verb_row 1/7/1 · table_subject_sha256_mismatch 1/7/1
gzip_envelopes 0/8/1 · no_id_verdict 0/8/1 · entry_missing 1/8/0
entry_source_without_table 1/8/0 · sources_row_other_date 1/8/0 · gate_omits_id 1/8/0
usage_error_missing_rev 2
```

Every named failure mode is covered; `gzip_envelopes` and `no_id_verdict` are
extra (the `.json.gz` input form, the `no-id` verdict). **Observation.**

## Evidence 3 — external mutation fixtures (seat MutR25Coverage)

Fixtures under `seats/MutR25Coverage/fixtures/` (bundle sha256
`73a9a8c1…28320bf`, `revs.json` sha256 `766ba2f6…a265b431`, 19 patches) with
expectation file `out/final_table.json`. Replayed with `--mutants` against the
mutation seat's own clone → exit 0, 13 cases, 0 failures; measured `entry_ok`
matched their expectation for every mutant (N-M1 0, N-M2 1, N-M3 0, N-M4 1,
N-M5 0, N-M6 0, N-M7 1, N-M8 0, N-M9 1, N-M10 1, N-M11 1, N-M12 0, N0 1). The
mutation seat re-ran the committed instrument in a fresh clone and got the
same 13 of 13 (`out/xcheck_result.json` sha256 `7c888088…8b5ad62`).
**Observation.** The instrument catches N-M1/N-M3/N-M5/N-M6/N-M8/N-M12 and
reproduces the disclosed residuals. Nothing synthetic entered the lane.

## Evidence 4 — the 24 real envelopes and the landed revision

A scratch clone (since deleted) took the real envelopes from RunAnalyzeInspect,
RunDecompileFunction, RunReadBytesLayout and RunXrefsInstructions plus a table
derived by the frozen `derived_verdict` rule: `rows_complete 8, entry_ok 0,
exit 1`; adding a synthetic entry, SOURCES row and lesson `## Gate` gave
`rows_complete 8, entry_ok 1, exit 0`. All 24 envelopes carry subject sha256
`e8156675…f7806` via `.data.subject.digest.sha256`; the non-gating path
diagnostic is `text_contains_path: true` for all 24. Then the committed
instrument was run read-only against the L1's landed revision:

```
python3 -I -B c1-id-identity.py --root <lane> --rev ebe2cb4a   -> exit 0
{"rev":"ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb","rows_total":8,"rows_complete":8,"entry_ok":1,"exit":0}
```

All 8 rows complete, no reasons, no warnings; analyze, inspect, decompile,
xrefs, read-bytes, function, instructions = `content-keyed`,
inspect-binary-layout = `path-sensitive`. Entry: `names_table true`, cited
`S079`/`S080`, both `opened 2026-10-22`, both in the lesson `## Gate` (gate
ids `S037`, `S079`, `S080`), `qualifying_ids [S079, S080]`, reasons empty,
`table.extra_rows` empty. **Observations** (the first is sandbox, not lane
content). The counter reaches the frozen target on the real tree.

## Interpretations of the frozen rules

The frozen text binds; these are readings of places where it left a choice.

1. **What a "row" is.** `rows_total` is the constant 8 (the claim's `before`
   and `target` both say 8; the table is absent at base), so `rows_complete`
   counts the 8 frozen verbs, not table lines. A line whose verb is not one of
   the 8 is not a row of this claim; it is reported under `table.extra_rows`
   and caps `rows_complete` at `8 - surplus`, because the claim's statement is
   that the table "has one row for each of the 8 frozen verbs". Without the
   cap, 8 good rows plus a foreign ninth row would read 8 of 8.
2. **Duplicate verb rows.** `row_complete` is a per-verb predicate, so two
   rows for one verb make that row non-unique: counted incomplete with reason
   `duplicate_verb_row` rather than one arbitrarily winning.
3. **Subject sha256.** Read literally as "first present of
   `.data.subject.digest.sha256`, then `.data.normalized_result.artifact.sha256`":
   a key present with a null value counts as present and mismatches the
   carrier. `.ok` is read at the envelope top level, as the claim's own
   `pre_freeze_probe` records it.
4. **Carrier sha256.** The expected subject sha is the frozen constant
   `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`
   (claims.json `carrier.sha256`), not a value read from the tree. The table's
   own `subject_sha256` cell is also compared with it (a non-empty wrong value
   fails the row); an empty cell is not a mismatch, since the frozen rule
   binds the three envelopes' subject digests, not the table cell.
5. **Id cell equality.** "the table's three id cells equal the envelopes'
   `.data.evidence_id` values" is exact string equality. When an envelope
   carries no `.data.evidence_id`, the derived verdict is `no-id` and that id
   cell must be empty; the row can still be complete with verdict `no-id`
   (the frozen limits say any verdict counts as complete). The `ev_` prefix
   is required only for the derived verdict, so a non-`ev_` id is a row
   warning, not a reason.
6. **`entry_ok` source line.** "its `source:` line" is the first entry line
   whose text starts with `source:` (the `verified-at:` and `recheck:` lines
   are not sources). The named `S###` ids are those on that line, not
   anywhere in the entry body. N-M8 and N-M12 are therefore both caught.
7. **`entry_ok` SOURCES row.** "opened 2026-10-22" is read against the
   `opened` column only. The frozen rule does not require `status == mined`,
   so a `rejected` row with `opened 2026-10-22` still qualifies (N-M4
   survives), and `used-by` is not required to name the entry (N-M9 survives).
8. **`entry_ok` Gate section.** "the `## Gate` section" is read
   section-scoped: the block under the first heading line exactly equal to
   `## Gate`, ending before the next line starting with `## `. An `S###`
   mentioned only outside that section does not qualify (N-M5 is caught; the
   whole-file reading would let it survive).
9. **Missing inputs.** A missing table, entry, SOURCES file or lesson file
   give `rows_complete 0` / `entry_ok 0` with an explicit reason, not a crash.
   Exit 2 is reserved for usage errors and an unresolvable revision.
10. **Envelope naming.** `envelopes/<verb>-<run>.json` then `.json.gz`; a
    `.gz` file is gunzipped before parsing. Both forms are selftested.

## Known defects in the instrument (reported, not fixed)

- **D1 — `entry_ok` inherits the round-25 false accepts.** A never-fetched URL
  whose `opened` cell says 2026-10-22 (N-M10), a forged `opened` cell
  (N-M11), a Gate row with no URL and no quote (N-M2), a source line naming
  the table while the table file is absent (N-M7), a `rejected` SOURCES row
  (N-M4) and a `used-by` that does not name the entry (N-M9) all give
  `entry_ok 1` with an empty reason list — the empty list is the false accept
  itself. Properties of the frozen rule, not of the code; the rule binds and
  the instrument reproduces it exactly.
- **D2 — the table's `subject_sha256` cell is not gated when empty.** A
  non-empty wrong value fails the row; an empty cell passes. The frozen
  `row_complete` text binds the three envelopes' subject digests and does not
  name the table cell, so this is the literal reading, but an empty cell is
  then unverified carrier evidence.
- **D3 — the surplus-row cap is an interpretation.** Another reader could let
  a ninth foreign row pass. The cap only ever lowers the count, so it cannot
  turn a failing table green.
- **D4 — the entry `source:` line must be the first one.** An entry whose
  `source:` line is not first, or that has two `source:` lines with the table
  on the second, reads as naming no table. N-M8 and N-M12 are caught under
  this reading; a `source:`-anywhere reading would let them survive.
- **D5 — `## Gate` is section-scoped.** An `S###` named only outside the Gate
  block does not qualify (N-M5 caught); a whole-file reading would let N-M5
  survive.
- **D6 — the `opened` cell is self-reported.** The instrument cannot tell a
  genuinely opened source from a forged `opened` cell (N-M10, N-M11).
- **D7 — no gating check that a committed envelope names the path it was run
  on.** The non-gating path diagnostic reports it; per the frozen rule it
  does not gate, so a wrong path in a committed envelope would not fail the
  count.
- **D8 — the selftest carries no residual shape.** It covers the N-M1 and
  N-M3 shapes (`gate_omits_id`, `entry_source_without_table`) but none of the
  six residual shapes, because a residual cannot be a red selftest case
  without asserting `entry_ok 1` for a broken tree. The mutation seat's
  fixture revs are the material for such cases.

## Risks and blockers

- The six residual `entry_ok` false accepts (D1) are latent on the landed
  tree, not currently false: the landing's `S079` and `S080` are genuine
  opened sources and the Gate row carries a URL and a quote, so the empty
  `entry.reasons` list at `ebe2cb4a` reflects a well-formed tree.
- No tools were installed or upgraded by this seat.

## Reproduce

```
cd /fast/scratch/hyaku/kaidoku-r26/seats/CounterC1
python3 -I -B c1-id-identity.py --selftest
python3 -I -B c1-id-identity.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV>
python3 -I -B c1-id-identity.py --root /fast/scratch/hyaku/kaidoku-r26/seats/MutR25Coverage/clone --mutants /fast/scratch/hyaku/kaidoku-r26/seats/MutR25Coverage/out/final_table.json
```
