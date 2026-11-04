# ReviewerC1 — round 81 / C1

Axes: calibration and depth; no domain-coverage, mastery, saturation or promotion claim.

## Findings by severity

No actionable C1 defect remains in the inspected final ExecRegistry candidate. This is a scoped review, not an admission vote.

**High, base-only, repaired by candidate:** the do-nothing base cannot meet C1. Independent parsing of committed SKILL.md at `5b59ae615a2ab68e3b421820d1c72751e1185385` yields 129 rows and 129 distinct existing paths; 118 seven-cell, ten eight-cell, one six-cell; no duplicates. Six eight-cell rows are outside the four frozen exceptions; the six-cell row has no positional pinned cell. Thus seven defects persist without changes. Receipt: `independent-base.json`; independent parser imports no census code. Frozen control receipt independently agrees and records exit 1; I did not rerun it.

| Base SKILL.md line | Tool | Independent defect / semantic requirement |
|---|---|---|
| 1908 | tools/round-77/verdict-bind.py | 8 cells: merge output and read-only qualifiers into WRITE, not PINNED; preserve kaidoku-r77 |
| 1909 | tools/round-77/prefile-receipt.py | 8 cells: merge clone/work/filing/json-out output descriptions into WRITE; preserve inputs and owner |
| 1910 | tools/round-77/gen-controls.py | 8 cells: merge out-dir/copies/json-out scope; preserve both pinned instruments and owner |
| 1911 | tools/round-78/attack-gate.py | 8 cells: two unescaped purpose pipes; missing WRITE and OWNER. Escaping alone leaves SIX cells, still defective |
| 1912 | tools/round-78/surface-recheck.py | 6 cells: disclosure text occupies positional OWNER; preserve provider/disclosure content, supply actual output scope and kaidoku-r78 |
| 1913 | tools/round-79/gate-mutation.py | 8 cells: merge scratch/output/read-only scope; preserve target/digest pin and owner |
| 1914 | tools/round-79/pointer-bind.py | 8 cells: merge receipt-output/read-only scope; preserve PROVINCE/live-input pin and owner |

These are absolute file line numbers; frozen control line numbers 129–135 are registry-block-relative.

## Candidate actually inspected

Candidate: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRegistry/SKILL.candidate.md`.
SHA256: `1380d3c963cbd85764a67f88ad766cd202b89228a9f13b0c96a867e976ff3a4d`.

`candidate-edits.json` reconstructs this candidate exactly from base using ten unique old/new anchors. Seven edits repair C1; three change round-80 printed case tallies (D2, not claimed as C1). All 129 registry paths are preserved exactly, not merely replaced to satisfy a population floor. Independent candidate parse: 125 seven-cell rows and exactly four eight-cell rows; each of the seven target rows now has seven cells. No duplicate path or deletion. Each preserved path exists in the measured base tree.

The four legitimate exceptions remain byte-identical: `tools/round-69/packed-elf.py`, `tools/round-69/mutation-check.py`, `tools/round-69/contract-probe.py`, `tools/round-69/controls.py`. No new exception or general eight-cell acceptance was introduced. ExecRegistry's frozen counter copy matches the base counter SHA256 `b85b4d7922ab571af04f633e415a4fe91859e440c9a609d4182a46aec61bb380`.

Field review: the five excess output/read-only columns merge into WRITE, retaining their original PINNED inputs and final round owners. `verdict-bind` explicitly qualifies “none” as no lane-input writes, not no receipt output. The attack purpose now contains exactly `base-only\|all-refuse\|no-fixtures`; unescaping yields all three original alternatives inside PURPOSE, restoring verdict/selftest positions. Its fixture/tool inputs and receipt disclosure remain PINNED; WRITE names json-out plus work fixtures and OWNER is kaidoku-r78. Surface providers and never-env/token disclosure remain PINNED; WRITE states receipt-only/live-read-only and OWNER is kaidoku-r78. No configuration was opened.

Definition/diagnostic access: `xd://lsp` returned “No such tool”; semantic status/references/definition/diagnostics were unavailable. Literal fallback inspection located `verdict-bind.py:601–622`, `surface-recheck.py:397–423`, and `attack-gate.py:993–1023`, grounding receipt/work output descriptions. Literal matches are not semantic caller proof. No executable behavior or callers change in this Markdown-only C1 candidate.

## Opened source screening

**Admitted sourced claim (reuse S258/S273, no new SOURCE row):** https://github.github.com/gfm/#tables-extension- — opened GFM §4.10, Example 200: “Include a pipe in a cell’s content by escaping it, including inside other inline spans.” This directly grounds escaping the two purpose pipes even inside backticks. Flip: reject this authority for a consumer whose contract explicitly uses a different table grammar.

**Rejected inference, with flip:** the same opened source says excess body cells are ignored and missing cells end-padded. That rendering tolerance does NOT establish the frozen registry's stricter positional seven-cell contract, and cannot justify broadening its grammar. Flip: admit tolerance only for a Markdown-rendering question, not C1 census acceptance. Also opened https://docs.python.org/3/library/tempfile.html#tempfile.mkdtemp (existing S274/S276 URL): reject it as registry-grammar evidence because its creation/permissions/cleanup contract says nothing about registry cells; flip if the question becomes temporary-directory lifecycle. No SOURCE rows added or duplicated.

## Residual risks and verification gaps

- This is candidate-byte review, not committed integration verification. L1 must measure the integrated revision with the frozen base counter and confirm unchanged counter bytes, exit 0, rows >=129, nonconformant [], duplicates [], multicell_rows 4, exact exception set, and green frozen selftest.
- Independently compare the complete path multiset: rows >=129 alone cannot detect deleting one path and adding another. This candidate preserves it exactly.
- Independent regex parser is deliberately bounded, not a general GFM renderer. Consecutive-backslash edge cases are not proven generally; actual changed attack text has one backslash per pipe and was inspected directly.
- Census syntax cannot prove all field meanings. This review examined all seven repaired rows and actual diff; historical pins/claims beyond those fields and the three D2 tally corrections are not independently re-executed here.
- ExecRegistry reports one frozen selftest run, 14 cases, zero failures; that is executor-reported evidence, not a reviewer-run check. No broad tests, builds, product-runtime invocation, client configuration reads, fixture git mutation, tool installation or production edit occurred.
- Canonical-runtime/rerouting/resume-continuity behavior is untouched and outside this C1 data-only slice; no claim of exercising those contracts.

Evidence in this directory: `independent_parse.py`, `independent-base.json`, `independent-candidate.json`, `shortcut-analysis.json`, `candidate.diff`. Scratch: only `/fast/scratch/hyaku/kaidoku-r81/ReviewerC1/`; TMPDIR and --work explicitly supplied to the bounded parse, no fixture commits. Scratch removed after retaining receipts.

Self-evaluation: accuracy 4 (candidate-byte findings, not integrated measurement); completeness 4 (all seven rows/four exceptions covered; integrated selftest belongs to L1); clarity 4 (base/candidate/source screening distinguished); actionability 4 (exact final checks specified); conciseness 4 (field matrix retained for audit). Overall 4.0. Improvement: bind this review's candidate digest to L1's integrated receipt; user should agree with the stated integration limit.
