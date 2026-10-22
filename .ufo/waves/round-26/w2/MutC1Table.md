# MutC1Table — mutation test of the R26-C1 counter's table checks

Seat `KaidokuR26.MutC1Table` (critic, leaf). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Frozen rules `.ufo/waves/round-26/claims.json`, claim `R26-C1` `rules`, frozen at `c27f445e70cedbaf5300b2fd0a53e821d9b659a9`. The L1 landed the R26-C1 evidence at `ebe2cb4a` and the counter at `bd0c84bc`; wave-1 seat `CounterC1` reported the instrument. This seat attacks the instrument's **table checks** only.

**Verdict: the counter's table checks kill every mutant the frozen rules make a defect; two table shapes survive that the frozen `row_complete` rule does not name.** 13 of 21 mutants killed, 8 survived. No survivor changes the claim's meaning: the landed table at `ebe2cb4a` is unmodified and still reads 8 of 8 and `entry_ok` 1.

## Setup and bounds

- Sandbox clone `/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Table/clone` (`git clone -q` of the lane). The lane was never written to; no lane Git write, no `jj`.
- Base commit `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb` (the R26-C1 landing). Pristine table sha256 `89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df`, identical at lane HEAD (read-only `git show`).
- Detector: committed instrument bytes copied out with `git show bd0c84bc:tools/round-26/c1-id-identity.py`, sha256 `11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa` (the same blob at lane HEAD), run as the frozen counting command `python3 -I -B <detector> --root <clone> --rev <REV>`.
- Kill criterion: the frozen gate triple (exit, `rows_complete`, `entry_ok`) differs from the pristine baseline (0, 8, 1). The counter's non-gating `table` echo is reported separately, not used as the verdict.
- Each mutant is a commit on top of the base inside the clone. After each mutant the clone is reset to the base, the table bytes re-hashed and the detector re-run at the base; the restored stdout must be byte-identical to the baseline stdout. All 21 restores matched on both counts.

## Baseline (2026-10-22T13:03:51Z)

```
python3 -I -B c1-id-identity.py --root <clone> --rev ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb
exit 0  rows_complete 8  entry_ok 1  table_reasons []
stdout sha256 76141980e4553c7091a4c67d9b1390dc06bcc43cfe66b8e76d7d92c8bebe552a
```

That stdout hash equals the wave-1 seat's own after-receipt hash for the same revision (`out/real-landing-ebe2cb4a.json`, sha256 `76141980…`), so the detector copy and the lane run agree byte for byte. **Observation.**

## Results (21 mutants; `gate` is exit, `rows_complete`, `entry_ok`)

| # | mutant | gate | verdict | reason (detector output) |
|---|---|---|---|---|
| M1 | wrong id cell (analyze `base_id` → `ev_000…`) | (1,7,1) | KILLED | `analyze: id_cell_mismatch:base` |
| M2 | wrong verdict (analyze → `path-sensitive`) | (1,7,1) | KILLED | `analyze: verdict_mismatch:analyze:table=path-sensitive:derived=content-keyed` |
| M3 | duplicate row (xrefs twice) | (1,7,1) | KILLED | `xrefs: duplicate_verb_row`; `data_rows 9` |
| M4 | unknown verb (instructions → `frobnicate`) | (1,7,1) | KILLED | `table.reasons ["unknown_verb_row:frobnicate"]`; `instructions: row_missing` |
| M5 | missing row (function deleted) | (1,7,1) | KILLED | `function: row_missing`; `data_rows 7` |
| M6 | extra column (`note` in header + every row) | (0,8,1) | SURVIVED | no reason; `header_ok true` |
| M7 | extra column, header only | (0,8,1) | SURVIVED | no reason; `header_ok true` |
| M8 | extra cell in one row only | (0,8,1) | SURVIVED | no reason; payload identical to baseline apart from `rev` |
| M9 | extra column mid-table (header + rows) | (0,8,1) | SURVIVED | no reason; `header_ok true` |
| M10 | reordered header (header + rows, consistently) | (0,8,1) | SURVIVED | no reason; `header_ok true` |
| M11 | reordered header, rows untouched | (1,0,1) | KILLED | all 8 rows `row_missing`; `unknown_verb_row:content-keyed,…` |
| M12 | extra column mid-table, header only | (1,0,1) | KILLED | all 8 rows `id_cell_mismatch:copy` (ibl: `repeat`+`copy`) |
| M13 | header names `base_id`/`repeat_id` swapped | (0,8,1) | SURVIVED | no reason; every landed verb has base == repeat |
| M14 | header names `base_id`/`copy_id` swapped | (1,7,1) | KILLED | `inspect-binary-layout: id_cell_mismatch:base; id_cell_mismatch:copy` |
| M15 | empty `subject_sha256` cell | (0,8,1) | SURVIVED | no reason (empty cell is not a mismatch) |
| M16 | wrong `subject_sha256` cell | (1,7,1) | KILLED | `analyze: table_subject_sha256_mismatch:analyze:table=000…0` |
| M17 | empty verdict cell | (1,7,1) | KILLED | `analyze: verdict_mismatch:analyze:table=:derived=content-keyed` |
| M18 | `subject_sha256` column dropped | (1,0,1) | KILLED | all 8 rows `table_header_invalid` |
| M19 | `base_id` renamed to `base` | (1,0,1) | KILLED | all 8 rows `table_header_invalid` |
| M20 | row truncated to 5 cells (subject cell gone) | (0,8,1) | SURVIVED | no reason |
| M21 | row truncated to 3 cells | (1,7,1) | KILLED | `xrefs: id_cell_mismatch:repeat; id_cell_mismatch:copy` |

The five assignment-named mutants — wrong id cell (M1), wrong verdict (M2), duplicate row (M3), unknown verb (M4), missing row (M5) — are **all five killed**. The two assignment-named shape mutants — extra column (M6/M7/M9) and reordered header (M10) — **both survived**.

## Why the survivors survive, against the frozen rule

The frozen `rules.inputs` names the table "tab-separated, header verb, verdict, base_id, repeat_id, copy_id, subject_sha256", and `rules.row_complete` binds: the verb is one of the 8 frozen verbs; all three envelopes exist and parse; each `ok` is true; each subject sha256 equals the carrier; the three id cells equal the envelopes' `.data.evidence_id` values; the verdict equals the derived verdict. **None of these binds the column count, the column order or the row width.** The counter reads by header name, so the survivors are the shapes the frozen text does not forbid:

- **M6, M7, M9 (extra column) and M10 (reordered header).** The counter maps `col[name] = header.index(name)`, so a surplus named column or a consistent reordering leaves every cell it reads at the right value. The table's content still is one row per frozen verb, three id cells equal to the envelopes' ids and the verdict equal to the derived verdict, so the frozen `row_complete` test is still met. A coverage finding about the counter's strictness, not a defect in the landed table. **Observation** (mechanism at `tools/round-26/c1-id-identity.py:396-419` of the file at `bd0c84bc`); **inference** that the frozen rule permits it.
- **M13 (`base_id`/`repeat_id` header names swapped).** Every one of the eight landed verbs has base id == repeat id, so swapping those two column names cannot change any cell the counter reads. M14 (swapping `base_id`/`copy_id`) *is* killed, because `inspect-binary-layout` has base != copy. The counter's id-column checking is real but its discriminating power is bounded by the landed data, in which seven of eight verbs are content-keyed. **Observation.**
- **M15 and M20 (empty `subject_sha256` cell, by cell clearing and by row truncation).** The counter compares the table's own `subject_sha256` cell only when it is non-empty (`if table_subject and table_subject != CARRIER_SHA256`); a truncated row leaves that cell empty. The frozen `row_complete` text binds the three *envelopes'* subject digests and does not name the table cell, so an empty cell is the literal reading — wave-1 seat `CounterC1` disclosed this as defect D2. This seat reproduces it by mutation. **Observation**, consistent with that disclosure.

M8 (a stray seventh cell on one row, header unchanged) survives with a payload byte-identical to the baseline apart from the `rev` field: the extra cell sits at an index the counter never reads. **Observation.**

## Counter-examples to the counter (none)

No mutant produced a reading that understates the claim: every killed mutant lowered `rows_complete` and raised the exit code, and none lowered `rows_complete` in a way that made a worse table read better. The counter's cap on surplus rows (`rows_complete = min(rows_complete, 8 - len(extra_rows))`) lowered M4's count as intended. **Observation.**

## Restoration evidence

For all 21 mutants the clone was reset to the base after the mutant measurement, the table blob re-hashed to `89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df` (matches pristine) and the detector re-run at the base produced stdout sha256 `76141980e4553c7091a4c67d9b1390dc06bcc43cfe66b8e76d7d92c8bebe552a` (identical to the baseline): 21 of 21 restores byte-exact, no lane file touched at any point. The clone ends at the base commit with the pristine table blob; `restore_ok` is true for every record in `out/summary.json`.

## Independent re-read

The instrument's own `--mutants` harness was run over the 21 mutant revisions with an expectation file naming `entry_ok=1` for each (table mutants never touch the entry): 21 cases, 0 failures, exit 0. **Observation.** It confirms the mutants are entry-neutral; it does not re-test the table gate, which the `--root/--rev` runs above did.

## Artifacts (seat scratch, sha256)

`mutate.py` `ef522bffd1ae7fd3a863e98a91a304182a387517f3ecc55ac21fa1b3fa6d1a25` · `c1-id-identity.py` `11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa` · `table.pristine.tsv` `89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df` · `out/run.log` `2fb4b5fe1b0cefc7fe70f9d2c06af94793a7317c13bd0da5c70405080fcb0b1a` · `out/summary.json` `4a3201a7a938168bb3c11eae8f2d03f2bb3923276d450338ad1762adfc8fb130` · `out/baseline.json` `62d399ac2a7014231f1dc04aac5da1de88a883eff11fad193173a7f162aebf20` · `out/final_table.json` `d44a2e34b55148e823387fec3d0b291fc7e9c21bac5819c2f705f797d79d27c0` · `out/mutants_harness.json` `49ca90dabfb975c6bcda15e266a669d5ae8e870d7965f4d15d7494ca9dcceeca` · `out/mutants_harness.err` (empty) `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` · per-mutant payloads `out/M<n>-*.json`, full records `out/M<n>-*.full.json`.

No tool was installed or upgraded by this seat; `git`, `python3` (standard library only) and `sha256sum` were already present.

## Reproduce

```
cd /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Table
python3 mutate.py                      # 21 mutants, baseline, restore check
python3 -I -B c1-id-identity.py --root ./clone --mutants out/final_table.json
```
