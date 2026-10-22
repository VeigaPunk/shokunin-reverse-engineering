# MutC1Forgery: forged envelope sets against the R26-C1 counter

Seat KaidokuR26.MutC1Forgery (mutation tester), 2026-10-22. Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin, read only.
Tip commit judged: fe3eb4edf410244eff46151a148c8f754be1ce80 (tree 784215f955cca6bc678d98d35d9e845f269132df).
Verdict: the committed counter accepts three of the four forgeries named by wave-1 critic C1Sizing, and accepts the fourth only when the forged table is left incoherent. Two of the accepted forgeries change a verdict. This is a coverage finding about the counter, not a change to the frozen claim.

## Method (all commands below were run; exit codes and UTC times are recorded)

- Sandbox clone: `git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Forgery/clone`, at fe3eb4ed. No git write, no jj command, and no file change in the lane.
- Detector (the frozen counting command, instrument run from the lane work tree, sha256 11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa, equal to the blob at HEAD):
  `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-26/c1-id-identity.py --root /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Forgery/clone --rev <REV>`
- Mutants were built by `build-mutants.py` in the clone (one branch each, one commit each). Source of the forged bytes: the committed envelopes at the tip, and the L1 pre-freeze probe file /fast/scratch/hyaku/kaidoku-r26/l1/probe-ibl.json, sha256 689680863a6e3dbd8c5a442aee52042a4601fd37e0555aa6db66d3a8ab3b195a, which claims.json names as envelope_sha256 of the pre_freeze_probe.
- Baseline and restored runs of the detector on the pristine tip: exit 0, rows_complete 8, entry_ok 1. Raw outputs raw/pristine.json and raw/restored.json are byte identical (sha256 4a57e912a13433bb9500fbc6d8456ad7f903b9151416dd5a910158c98ef8d160).

## Mutant table

| mutant | forgery | rev | rows_complete | entry_ok | exit | verdict change | detector verdict |
|---|---|---|---|---|---|---|---|
| M1 | every copy envelope replaced by its base envelope, table cells and verdict made coherent | c3e69360 | 8 | 1 | 0 | inspect-binary-layout path-sensitive to content-keyed | false accept, verdict changing |
| M1n | same envelope swap, table left untouched | 26720342 | 7 | 1 | 1 | none | killed, only by table incoherence |
| M2 | one run used three times for every verb, table made coherent | ef395c24 | 8 | 1 | 0 | inspect-binary-layout path-sensitive to content-keyed | false accept, verdict changing |
| M3 | analyze and inspect envelope files swapped for all three runs | cb71a920 | 8 | 1 | 0 | none | false accept |
| M4 | L1 pre-freeze probe envelope reused as the inspect-binary-layout base | 3e3d96bf | 8 | 1 | 0 | none | false accept |

Runs at 2026-10-22T12:59:34Z (pristine, M1, M1n) and 12:59:35Z (M2, M3, M4, restored). Full JSON in raw/.

## What the counter saw and did not gate

- M1 and M2 (obs): the counter printed the path diagnostic for eight files each. For M1, `diagnostics_not_gating.tree_path_text` reports `text_contains_path: false` for analyze-copy, decompile-copy, function-copy, inspect-binary-layout-copy, inspect-copy, instructions-copy, read-bytes-copy and xrefs-copy, expected path /fast/scratch/hyaku/kaidoku-r26/carrier/alt/jq. The frozen rules place this diagnostic outside the gate, so the row still counted complete. The copy envelopes in both mutants are byte identical to their base envelopes (sha256 check, all 8 verbs, recorded in the run log).
- M1n (obs): the only reason the counter objected is `id_cell_mismatch:copy;verdict_mismatch:inspect-binary-layout:table=path-sensitive:derived=content-keyed`. The table was still the honest one. A forger who updates the table (M1) passes.
- M3 (obs): analyze and inspect envelopes share their `.data` exactly, so the ids are identical (`ev_14f9d92f41c6...`) and the swap moves no id. The swapped file analyze-base.json still carries `.meta.command` "inspect" and inspect-base.json carries "analyze"; the counter never reads `.meta.command`. Verdict unchanged, no diagnostic flagged.
- M4 (obs): the probe file and the committed inspect-binary-layout base differ only in `.meta.duration` ("192ms" against "194ms"); same `.data.evidence_id`, same subject sha256, `ok` true, same command and same path. The counter accepted it. The probe therefore becomes a table row, which claims.json says must never happen, and no rule can see it.
- The instrument's own `--mutants` harness compares only entry_ok (obs, source of tools/round-26/c1-id-identity.py). entry_ok is 1 in all five mutants, so that harness reports every forgery as unchanged.

## Secondary detectors, not part of the counter

- recompute-ids.py on the 24 committed envelopes of each mutant: exit 0, "recomputed ids: 24 match of 24 total" for pristine and for every mutant (work/*.recompute.txt). It does not catch any of the four forgeries, because the forged files carry genuine envelope bytes.
- Cross check of the committed runs.tsv `envelope_sha256` column against the sha256 of the committed envelope files: pristine 24 rows, 0 mismatches; M1 8 mismatches (all copy rows); M2 16 mismatches (all repeat and copy rows); M3 6 mismatches (all analyze and inspect rows); M4 1 mismatch (inspect-binary-layout-base, recorded 4a256cc73b54 against actual 689680863a6e). All four forgeries are caught by data already committed in the lane. The counter does not read runs.tsv.

## Restoration evidence

- Clone returned to fe3eb4edf410244eff46151a148c8f754be1ce80, tree 784215f955cca6bc678d98d35d9e845f269132df, identical to the tree before the mutants and to the lane tree at the same commit.
- table.tsv sha256 89eca1527564e383565d0535d04801e3e3837edbce6462a464c887d4ee79f5df before and after; clone work tree clean; detector rerun on the restored tip gives exit 0, 8 of 8, entry_ok 1.
- Lane HEAD is fe3eb4edf410244eff46151a148c8f754be1ce80 and the lane tree hash is unchanged. The only file this seat wrote inside the lane is this report.

## Reading for the judge (no contract change proposed here)

- The frozen rules verify id shape, subject sha, presence and table coherence. They do not verify run identity, run path, byte distinctness or provenance, so a table built from a single run, or from envelopes taken from another verb or from the pre-freeze probe, is counted as 8 of 8 with entry_ok 1 (obs).
- The claim statement says the verdicts re-derive from three committed envelopes (base, same-path repeat, byte-identical copy at the alternate path). M1 and M2 satisfy every frozen rule while breaking that clause, and they flip inspect-binary-layout from path-sensitive to content-keyed (obs). The counter therefore cannot carry that clause on its own.
- The cheapest coverage that uses only committed lane data is the runs.tsv envelope_sha256 cross check above, which is sensitive to M1, M2, M3 and M4 (obs). Whether to add it is a decision for the L1; this seat does not change the claim or the instrument.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Forgery/)

- build-mutants.py 5b87a25581bae9467fca0bbd5df5e4b5412ea3f9091bb3030be6fe0626f8e560
- run-counter.sh ff606c1856e6e7a115144f54c87e56abe3a5696bebc5612280b05fc99f5cda37
- secondary-checks.sh 7ac9291474330fdf83ac4ac64af48ffd56d62945787b4e9f11bc5417a6a54e11
- manifest.json 46bccedac48047e2b06b92f2d8558cfd6c05c22524284dbdc4739bae588f9b6a
- raw/pristine.json 4a57e912a13433bb9500fbc6d8456ad7f903b9151416dd5a910158c98ef8d160
- raw/restored.json 4a57e912a13433bb9500fbc6d8456ad7f903b9151416dd5a910158c98ef8d160
- raw/M1_copy_is_base_coherent.json acc6a78cd1d10f4e51352f4a64c420227edfd52df7dfd0f4c7fb0c0d3fb82206
- raw/M1n_copy_is_base_naive.json 09cc3c5407befc22d8848559eebce2665b9feb47273e8bfa8655f7f5660196ac
- raw/M2_one_run_three_times.json 2bca86e4b01880e0da9355b8f25bc969e546dbe0d5f46e35432fef8284c5e677
- raw/M3_swap_analyze_inspect.json a98fa9045e8460f76b89f42e5f9ebe3892a986f174fe2dd054d83a745b236639
- raw/M4_probe_as_ibl_base.json 533d6a747770aa439547ec68b0799fd797d64980bbc405897bf19c1d3ead2d8a
- work/pristine.recompute.txt 36bd25d15201ff00455bfa0eae03f4275497cade7671a935f70ab86fa973d5fb and one file per mutant in the same directory
- The clone itself is at /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Forgery/clone, branches m1-copy-is-base-coherent, m1n-copy-is-base-naive, m2-one-run-three-times, m3-swap-analyze-inspect, m4-probe-as-ibl-base.

Tools installed or updated: none. No REA run was needed for this seat; all evidence is local file bytes from the lane and from the L1 probe file.
