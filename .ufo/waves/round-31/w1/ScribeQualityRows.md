# Round 31 wave 1 — Quality row draft

## Behavior and touched surfaces
Drafted three admission criteria for `corpus/QUALITY.md`, continuing after row 51 with rows 52–54 and matching its `# | criterion | why (lesson) | supersedes` table. `corpus/QUALITY.md` was read only and is unchanged. The only file written is this scoped report.

## Draft rows

| # | criterion | why (lesson) | supersedes |
|---|---|---|---|
| 52 | A report cites a gate result only when a committed receipt shows that result; otherwise it cites only committed runs. For round 31, the cited-runs gate is `tools/round-31/cited-runs-gate.py`. | `corpus/lessons/round-30-verifier-spotcheck.md:144` (routed defect 1); round-31 gate receipt: `<receipt path>` | — |
| 53 | A counter's committed-record check compares the full envelope, including code and message, never only `ok`; retain the copied-predictions control showing that an `ok`-only comparison fails. | `corpus/lessons/round-30-verifier-spotcheck.md:145` (M30-3); round-31 copied-predictions control: `<receipt path>` | — |
| 54 | A Core-admission check verifies that a table row is placed under a Core heading (or in the round's Core-addition table); token co-occurrence alone is insufficient. | `corpus/lessons/round-30-verifier-spotcheck.md:149` (routed defect 6); round-31 placement control: `<receipt path>` | — |

## Findings and provenance

- **Observation — row format and numbering.** Producer: `functions.read(path="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:-100")`. The returned table uses the stated four columns and ends at row 51. Tool result has no shell exit code or per-call UTC timestamp. Review timestamp recorded immediately after reads: `2026-10-23T04:10:06Z`.
- **Observation — lesson sources.** Producer: `functions.read(path="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-30-verifier-spotcheck.md:142-151")`. Exact excerpts: line 144, “Commit the receipts of the runs a report cites, or cite only committed runs”; line 145, “The next C2-family counter must compare the full refusal envelope (code plus message), and show that it fails on the copied-predictions control”; line 149, “A future Core-admission counter should check placement under `## Core` (or the round's Core-addition table), not only co-occurrence.” Tool result has no shell exit code or per-call UTC timestamp; see review timestamp above.
- **Unknown / not independently exercised.** No round-31 gate, counter, or control was run or inspected for an execution result. The row-to-control mapping follows the assignment; the `<receipt path>` placeholders are intentionally left for the L1 to fill. No install was performed.

## Gates, limits, and out-of-scope

No gate or test result is reported. `tools/round-31/cited-runs-gate.py`, the copied-predictions control, and the placement control were not executed in this scribe task. No product or lane files were changed; in particular, this task did not edit `corpus/QUALITY.md` or independently verify the controls. External sources: none opened.

## Artifact path

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/w1/ScribeQualityRows.md`
