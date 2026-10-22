# MutC1Entry: mutation probe of the C1 counter's entry_ok rule

Seat KaidokuR26.MutC1Entry (mutation tester), 2026-10-22. Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin, read only.
Judged commits: ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb (the C1 landing commit) and 003de8cc38a86a914c0348ded674091d47d71fc1 (lane tip observed at 2026-10-22T13:05Z; the L1 committed it during this seat's run, so every mutant was also rebuilt on it).
Verdict: the entry_ok rule as implemented catches five of the six mutants this seat was asked to make. The sixth, a SOURCES row whose status is set to `rejected`, survives with entry_ok 1, because the frozen rule never mentions status. Nine further probes also survive. All of them are rule-faithful: the counter implements the frozen text literally, and the frozen text is weaker than the claim statement it is meant to carry. These are coverage findings about the rule, not grounds to change it, and no lane file was changed here.

## Method (every command below was run; exit codes and UTC times are recorded)

- Sandbox clone: `git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Entry/clone`. Every Git write happened in that clone, one branch and one commit per mutant. No Git write, no jj command, and no file change in the lane.
- Detector, run from a copy of the committed instrument (sha256 11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa, equal to the blob in the lane at both judged commits):
  `python3 -I -B /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Entry/c1-id-identity.py --root /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Entry/clone --rev <REV>`
- Baseline on pristine bytes at both judged commits: exit 0, rows_complete 8 of 8, entry_ok 1, cited_ids [S079, S080], gate_ids [S037, S079, S080], qualifying_ids [S079, S080]. Raw outputs out/baseline.json and out-tip/baseline.json; the restored runs are byte identical to them (sha256 1bcd7af6… for the ebe2cb4a pair, ee5f684a… for the tip pair).
- Instrument self test: `python3 -I -B c1-id-identity.py --selftest`, exit 0 at 2026-10-22T13:07:25Z, five cases PASS (entry_missing, entry_source_without_table, sources_row_other_date, gate_omits_id, usage_error_missing_rev).
- Mutants were built by mutate.py, one branch each (`mutant/<name>`), one commit each, each touching exactly one of the three files that entry_ok reads.

## Mutant table (judged on the lane tip 003de8cc; the ebe2cb4a run gave the same verdicts)

| mutant | change | rev | rows_complete | entry_ok | exit | detector verdict |
|---|---|---|---|---|---|---|
| M1 | entry source: line no longer names `corpus/evidence/round-26/c1/table.tsv` | 4512b239e3e2 | 8 | 0 | 1 | killed |
| M2 | S079 and S080 opened date changed to 2026-10-21 | de9f365d337f | 8 | 0 | 1 | killed |
| M3 | S079 and S080 removed from the `## Gate` section of the round-26 lesson | 863bad9acc4b | 8 | 0 | 1 | killed |
| M4 | entry source: line cites the older row S075 instead of S079/S080 | d678688bdfc1 | 8 | 0 | 1 | killed |
| M5 | S079 and S080 status cell set to `rejected` | 3ce2bbb75324 | 8 | 1 | 0 | survived, false accept |
| M6 | entry file renamed to `…-renamed.md` | 4205b628a7be | 8 | 0 | 1 | killed |
| M7 | source: line mentions the table only to deny citing it | b6f0d9d01577 | 8 | 1 | 0 | survived, false accept |
| M8 | S075 cited and named in the `## Gate` section only as prose, never as a gate row | 6b5dd5801f1c | 8 | 1 | 0 | survived, false accept |
| M9 | entry file reduced to its source: line, body removed | a437553dbb29 | 8 | 1 | 0 | survived, false accept |
| M10 | S079 used-by cell no longer names this entry | 84ebaffda770 | 8 | 1 | 0 | survived, false accept |
| M11 | S079 gate row keeps its id but its sha256 and located quote cells are emptied | ded379fae901 | 8 | 1 | 0 | survived, false accept |
| M12 | entry source line asserts its sources were opened on 2026-10-21 | 97a46b816dbf | 8 | 1 | 0 | survived, false accept |
| M13 | source: line names the table and the ids but states nothing is cited | b9971c0d2d6d | 8 | 1 | 0 | survived, false accept |
| M14 | source: line cites only S079, S080 dropped | 22ec776d142e | 8 | 1 | 0 | survived, rule-faithful |
| M2b | only S080's opened date changed, S079 still qualifies alone | 903f2de3d50b | 8 | 1 | 0 | survived, rule-faithful |

Runs at 2026-10-22T13:08:02Z to 13:08:06Z (tip base) and 2026-10-22T13:05:09Z to 13:05:12Z (ebe2cb4a base). The shipped `--mutants` harness, fed with an expectation file that says entry_ok=0 for every case, exits 1 and prints FAIL for exactly the ten survivors (out/harness.txt, out-tip/harness.txt). Full JSON per mutant in out/M*.json and out-tip/M*.json.

## What the counter saw, and what it cannot see

- M1, M3, M6 killed with the reasons `source_line_does_not_name_table`, `no_cited_source_row_opened_today_and_named_in_lesson_gate` and `entry_missing` (obs).
- M4 killed by the Gate check, not by the date check (obs): S075's opened cell is 2026-10-22 and the counter listed it under rows_opened_today, so it failed only because S075 is not named in the round-26 lesson's `## Gate` section.
- M5 survives because `parse_sources_rows` stores the status cell (`"status": cells[8]`, instrument line 193) and `evaluate_entry` never reads it; the qualifying test is opened equals 2026-10-22 plus membership in the Gate id set (instrument lines 254 to 268). The registry does have a status vocabulary: 78 rows are `mined` and 2 are `rejected` (S022, S028), and the round-13 lesson states that a rejected source "is not presented as evidence for a lane finding" (corpus/lessons/round-13.md:53). Under the lane's own convention an entry citing only a rejected row should not qualify, so M5 is a false accept against the lane convention while remaining true to the frozen rule, which names only the opened date and the Gate membership.
- M8 survives because the Gate id set is a plain token scan of the whole section (instrument line 251), not a scan of the Gate table rows. The pristine tree already shows this: baseline gate_ids is [S037, S079, S080] and S037 appears only in the Gate prose ("already row S037's family"), never as a gate row (obs). A row named anywhere in the section qualifies, so any same-day-opened row from an earlier round (S074 to S078 were all opened on 2026-10-22) becomes a valid citation for this entry with one prose sentence.
- M7 and M13 survive because the table check is a substring test on the source line (instrument line 242) and the id test is a regex over the same line (instrument line 246). A line that denies citing the table, or says nothing is cited while naming the ids, satisfies both.
- M9, M10, M11, M12 survive because the rule asks only that the entry file exist, that its source line name the table, and that one cited id be opened today and named in the Gate section. It never asks that the entry have a body, that the registry point back at the entry, that the Gate row carry a sha256 and a located quote, or that the entry's own "opened" text agree with the registry.
- M14 and M2b survive because the rule says "at least one" qualifying id. That is the frozen wording, so these are not counter defects.

## Reading for the judge (no contract change proposed here)

- The claim statement in .ufo/waves/round-26/claims.json says "A knowledge entry cites the table and a SOURCES row opened 2026-10-22 whose id appears in corpus/lessons/round-26.md under ## Gate". The counter verifies presence of a file, a path substring, one id token, one opened date and one token in the Gate section. It cannot verify that the entry cites the table (M7, M13), that the id is gated for this round rather than mentioned in passing (M8), that the cited row is admissible rather than rejected (M5), or that the entry says anything at all (M9, M12). The claim's "cites" and "appears under ## Gate" are stronger than the counter can carry.
- The cheapest coverage that uses only committed lane data and no new REA run: parse the Gate table rows rather than the whole section, so an id counts only when it heads a row that carries a sha256 and a located quote; require the qualifying SOURCES row to be `mined`; and require the entry's used-by cell to name the entry. Whether to add any of these is a decision for the L1. This seat did not change the claim or the instrument.

## Restoration evidence

- Clone returned to the judged commit, work tree clean, `git status --short` empty, HEAD detached at 003de8cc38a86a914c0348ded674091d47d71fc1 after the tip run and at ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb after the base run.
- The three files entry_ok reads have identical sha256 before and after the whole mutant cycle: entry 1ba5d5d909eecb2db638677388f9bcc0429b5263469905a936fc3c2a6185a941 and b03fcdc450869e65337a81b009ca0f67008c4864d32630dfd858da5e99143a20 (tip and base respectively), corpus/SOURCES.md 945900936762151ad8544c8a0f66179d5c119aefe562e82a067b1085f6ae4657, corpus/lessons/round-26.md 28f55b8fd0238ffbc3dd36b88b6071e0f8fd6fb1152fc7619ac4f19f1a9af6d3.
- The detector rerun on the restored bytes gives exit 0, 8 of 8, entry_ok 1, and its output is byte identical to the pristine baseline output.
- The lane was not written to. The only file this seat wrote inside the lane is this report. Lane HEAD observed at the end: 003de8cc38a86a914c0348ded674091d47d71fc1.

## Artifacts (/fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Entry/)

- mutate.py a1afb0950e738605879677b18c554bca995db77cc93b56aeaa91d0a8ee6bef79
- c1-id-identity.py 11c274220fb5df41ef4467f595cf20a02c8e24240e37c6639308e2816fa918fa (copy of the committed instrument)
- final_table.json e9d4f9074cd58ee2ea1729207dce0dd3fcf31c3728a7b95bb8d5d711d291de22 and final_table_tip.json 6027fcbb7ead1bfeaf5cf6fa32fc30224a8b6a27bbeb0aac3027e2fc392aaae4 (expectation files for the shipped harness)
- out/table.json b3487b56efb38434508474e2b3896d250ee05a9c78eb709324339f3781589959, out/baseline.json and out/restored.json 1bcd7af6b8588ba2f343d5e3256e5ec3f7e690ede1a7cf4c094a823a9fb2dc33, out/harness.txt 41d6f7756036318db9214be7d7089cb855e887e7128a65b4e1360624274764b5, out/selftest.txt 208a14f33b8c8872125c75a85735c8ec82a7aa24cec49796edeb22ef78ee882b, and one JSON per mutant out/M*.json
- out-tip/table.json ad809aa24b8904c3ab402e564fa6dc4d9e6c306129db98ac4b3f5cd64e3935d4, out-tip/baseline.json and out-tip/restored.json ee5f684aac4d0f05428ceb6ac167d4e89c41741bb0ee85006a20abaff4ab86f4, out-tip/harness.txt f5344966fc780015fbf6604df8e0e16939be9396453ab04904ebf2b07a7e9202, and one JSON per mutant out-tip/M*.json
- The clone is at /fast/scratch/hyaku/kaidoku-r26/seats/w2/MutC1Entry/clone, branches mutant/M1 to mutant/M14 and mutant/M2b_one_of_two_dates_changed.

Tools installed or updated: none. No REA run was needed for this seat; all evidence is local file bytes from the lane.

Report: `.ufo/waves/round-26/w2/MutC1Entry.md`
