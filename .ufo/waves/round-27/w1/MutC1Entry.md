# R27-C1 wave 1 — seat MutC1Entry — mutation test of the counter's entry_ok gate

Scope: I attacked only the `entry_ok` gate of the pinned R27-C1 counter
`tools/round-27/c1-rename-identity.py` (commit `a4f674b3`, byte sha256
`e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7`). I made no REA call, changed no
carrier, and did not touch the row-computation rules. All work is in the sandbox clone
`/fast/scratch/hyaku/kaidoku-r27/seats/MutC1Entry/clone` (a clone of the lane at `a4f674b3`); the lane
working tree was read only, no lane git write, no jj command, no package installed.

## Detector

    python3 -I -B tools/round-27/c1-rename-identity.py --root <clone> --rev HEAD --base <base>

`killed` = the counter exits 1 with `entry_ok=0` (the gate noticed). `survived` = the counter still exits 0
with `entry_ok=1` (the gate did not notice). The 16 table rows stayed complete in every run, so every
verdict below comes from the entry gate alone. `entry md` is
`corpus/knowledge/2026-10-22-r27-renamed-copy-evidence-id-identity.md`, `SOURCES` is `corpus/SOURCES.md`,
`lesson` is `corpus/lessons/round-27.md`.

## Green fixture and baseline

The fixture is built by `build_fixture.py` from the counter's own pinned helpers (`_envelope`, `_write`,
`argv_for`), so the envelope bytes are synthetic counter-generated envelopes, not REA runs. Two commits:
docs `7e8f440b` (SOURCES gains the S900 row, the lesson gains a `## Gate` section, the knowledge entry is
added) and evidence `054ac6b5` (48 envelopes, runs.tsv, table.tsv). Synthetic commit and run timestamps
(15:50Z and 16:00Z) sit after the counter's own commit time (2026-10-22T14:51Z) so the "run after the
counter commit" rule holds; the entry gate reads no timestamp, so this dating cannot affect any verdict here.

Baseline on pristine bytes, 2026-10-22T14:55Z, exit 0:

    entry: sourced by S900
    rows_complete=16/16 entry_ok=1 rev=054ac6b5c9082a908357ac64c210b7c616a8f8e9

## Mutants (14 probes, one commit each, counter run after each commit)

| mutant | file sha256 before → after | expected | counter output (entry line) | exit | verdict |
|---|---|---|---|---|---|
| m01 second `source:` line added after the real one | entry md `cef3209abedb`→`84551331ab05` | gate still passes | `sourced by S900` | 0 | survived |
| m02 decoy `source:` line placed before the real one | entry md `cef3209abedb`→`07517478925c` | gate rejects | `source: line does not name corpus/evidence/round-27/c1/table.tsv` | 1 | killed |
| m03 S id only in prose, not on the `source:` line | entry md `cef3209abedb`→`1807ebeeeca3` | gate rejects | `source: line names no S### that is new since base, mined, opened 2026-10-22 and in ## Gate` | 1 | killed |
| m04 SOURCES S900 row with 10 columns | SOURCES `9187d066f493`→`769e74833f10` | gate rejects | same "names no S###" line | 1 | killed |
| m05 status cell `mined ` with trailing space | SOURCES `9187d066f493`→`221f13d1b139` | gate rejects (if strict) | `sourced by S900` | 0 | survived |
| m06 opened cell `2026-10-21` | SOURCES `9187d066f493`→`e9d3b468e6d7` | gate rejects | same "names no S###" line | 1 | killed |
| m07 lesson heading `## Gate (sources)` | lesson `ce222c667ac9`→`6a2c30324c3d` | gate rejects | same "names no S###" line | 1 | killed |
| m08 S id moved to the second cell of the Gate row | lesson `ce222c667ac9`→`d51e00cf3d79` | gate rejects | same "names no S###" line | 1 | killed |
| m09 entry file renamed to another name | entry md `cef3209abedb`→absent, alt file `cef3209abedb` | gate rejects | `entry absent` | 1 | killed |
| m10 cited S row already present in the base SOURCES | no tree change, `--base 7e8f440b` | gate rejects | same "names no S###" line | 1 | killed |
| m11 status cell `MINED` | SOURCES `9187d066f493`→`8e2b21b2512f` | gate rejects | same "names no S###" line | 1 | killed |
| m12 opened cell `2026-10-22 ` with trailing space | SOURCES `9187d066f493`→`8a1b6d9f144f` | gate rejects (if strict) | `sourced by S900` | 0 | survived |
| m13 source line names `S900 S901`, S901 has no SOURCES row | entry md `cef3209abedb`→`eb7851ad09d5` | gate rejects (if strict) | `sourced by S900` | 0 | survived |
| m14 SOURCES S900 row with 12 columns | SOURCES `9187d066f493`→`396919a78bb4` | gate rejects (if strict) | `sourced by S900` | 0 | survived |

m10 needs the "new since base" clause, so that one run used `--base 7e8f440b` (the fixture's docs commit,
where S900 already exists in SOURCES); every other run used the lane base `cd32264f`. Cell counts were
checked directly before the runs: m04 produced 10 fields, m14 produced 12, the green row has 11; m05 left
the raw cell `mined ` (two spaces before the pipe) and m12 left `2026-10-22 `.

## Verdict on the invariant

**The entry_ok gate holds for every requirement the statement names.** It rejects an entry whose source
line does not name the table, an S id that appears only in prose, a SOURCES row with fewer than 11 cells,
a wrong opened date, a status that is not exactly `mined`, a lesson heading that is not exactly `## Gate`,
a Gate row whose S id is not the first cell, a missing or renamed entry file, and a cited row that already
existed at the base. Nine of fourteen probes were killed; the five survivors are tolerance edges, not
holes in the named requirements.

## Do the survivors matter to the statement

- m01, m05, m12 — do not matter. A second `source:` line, `mined ` and `2026-10-22 ` still say mined and
  still say 2026-10-22, so the entry continues to satisfy the statement. Coverage note only: the counter
  reads only the first `source:` line.
- m14 — does not matter to the statement. The statement fixes the status and the opened date, not the
  column count; a 12-cell row still carries both in the checked positions.
- m13 — matters mildly, and only as written. The gate passes when at least one cited S id qualifies, so an
  entry that cites a good row and also a wrong or missing row is not flagged. The statement says the entry
  cites *a* SOURCES row, so the counter matches the statement as written; if the round wants every cited id
  checked, that is a statement change, not a counter defect. Observation, not a counter change.

## One over-strict edge (m02), worth telling the L1

The counter takes the first line starting with `source:` and ignores the rest. An entry whose first
`source:` line is anything else is rejected even when a later line cites the table and the qualifying S id
(m02, exit 1, `source: line does not name corpus/evidence/round-27/c1/table.tsv`), although such an entry
still "cites the table and a SOURCES row" under the statement's wording. Recommendation: the round-27
knowledge entry must carry exactly one `source:` line, and that line must carry the table path and the S id.
This is an authoring constraint, not a change to the pinned counter.

## Restoration evidence

After every mutant the clone was reset to the green commit `054ac6b5` and cleaned; the sha256 of the three
touched files matched the pristine values exactly (`restore check: identical`). After the last restore the
counter was run again on the restored bytes, 2026-10-22T14:56Z, exit 0:

    entry: sourced by S900
    rows_complete=16/16 entry_ok=1 rev=054ac6b5c9082a908357ac64c210b7c616a8f8e9

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/MutC1Entry/)

| path | sha256 |
|---|---|
| `build_fixture.py` | `44546b4a5067b43e5212eb0109e701fb25f946a2ab2739ae36c1c15785d66f74` |
| `run_mutants.py` | `4cef7910d82e80d45e9add9582dfe3548e8576a146f4b6765b9c325d6d1b1163` |
| `mutants.json` (per-mutant exit, output and hashes) | `f8d5bd23b0e41014d30065a4180949aa357ea02d59bda1942b1206dda8f84e7c` |
| `clone/` (sandbox clone; HEAD `054ac6b5`, docs commit `7e8f440b`) | directory, not hashed |

Tools installed: none. The pinned counter and `tools/round-26/recompute-ids.py` were used as committed.

Labels: every table row is an observation from a run I executed. The judgement that the survivors do not
weaken the statement is an inference from the statement text and the counter source.

Report: .ufo/waves/round-27/w1/MutC1Entry.md
