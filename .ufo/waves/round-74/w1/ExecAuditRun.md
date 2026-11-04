# ExecAuditRun — round-74 independent record audit

Axes: committed-byte fidelity, routed-defect coverage, receipt consistency. Instrument read-only; no implementation changes.

## Executed results

Command form: `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-74/record-audit.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <revision> --json-out <absolute evidence path>`.

| Revision | Exit | Atoms | Mismatches |
|---|---:|---:|---|
| base `04fdc2c4dbedbe5ee50a069af14310068393233e` | 1 | 16 | 11: D3, D6, D7b, D8, D9, D10, D11, D12, D13, D14, D15 |
| freeze `021914c0e638454e507087accfe41af1ab69f185` | 1 | 16 | 9: D3, D6, D7b, D8, D9, D10, D11, D12, D13 |

The executed instrument SHA256 is `5bcd1462ee25c3ab3ef92f5ff22eda43bfc15dbbca15750f4c678eb9b1a32c5c`, equal to the freeze pin. At base the receipt correctly has a null runner digest because this round's audit did not yet exist at that measured revision; the executing instrument is separately identified above.

Both revisions still fail D3 because `corpus/claim-freezes-v2.tsv` lacks a round-74 row, although the round-73 gate has empty `missing`/`stray` disclosures. Both fail D6 because SCORECARD lacks the round-74 lowest-axis declaration. The seven other remaining failures are explained below. D1, D2, D4, D5 and D7 are true at both revisions; D14 and D15 become true at freeze.

## Nine added atoms: exact committed evidence and routing

All cited line numbers refer to committed bytes retained with their blob digests and revision keys in `ExecAuditRun/committed-evidence.json`, not the concurrently edited working tree. B = base; F = freeze.

| Atom | B / F | Decisive committed bytes or absence | Mapping to plan / routed defect |
|---|---|---|---|
| D7b | false / false | `SCORECARD.md:5740` names both `pre/c1-at-base-r72probe.json` and `pre/c1-at-base.json` in R73-C1. Its round-73 section has no `**Before-arm selection (round 74 correction)**` block. | Matches planned (b), the D7 false-green and routed item 9. Both receipts resolve but their claim roles are not selected. Predicate weakness: presence of both strings in the block suffices; it does not parse a before-arm choice or each receipt's role. |
| D8 | false / false | `SCORECARD.md:615` opens `## Capabilities`; table ends with round-72 rows (including line 648 ending `| round 72 |`). Its final cells contain zero round-73 and zero round-74 entries. | Matches routed defect 1 (three missing round-73 rows), extended by the plan to two round-74 rows. The false reason includes the original defect. |
| D9 | false / false | `corpus/SOURCES.md:192`, S275 final cell is exactly `corpus/knowledge/2026-11-04-r72-checker-env-capsule.md, .ufo/waves/round-72/w1/ScoutSource.md`, omitting `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md`. | Matches routed defect 2 precisely. |
| D10 | false / false | `corpus/SOURCES.md:221` opens `## Search log`; line 223 begins `- 2026-11-04 round 72 — Question:`. That section contains neither `round 73` nor `round 74`; both receipt flags are false. | Matches routed defect 3, extended to this round. Predicate only checks the round strings and `Identified`, not question/where/counts/stop completeness. |
| D11 | false / false | No registry row with status cell `rejected` has any of `proc.5.html`, `proc_cmdline.5.html`, `proc_pid.5.html`, `index.html#_section_5` in its page cell: counts are exactly 0,0,0,0 at B and F (11 other rejected rows exist). | Matches routed defect 4's missing rows. Predicate does not inspect nonempty reason/flip cells despite its detail claiming those checks. |
| D12 | false / false | SCORECARD contains no heading beginning `## 2026-11-04 — round 74:` at either revision, hence no round-74 `census erratum` block mentioning `W04`, `24`, `23`. | Matches routed defect 5's missing named erratum. Predicate checks token co-presence, not the arithmetic or the roles of the numbers. |
| D13 | false / false | `corpus/README.md` last four decoded characters are exactly `ity.`; final byte is `2e`, not newline `0a`, at B and F. Last-byte hex/repr retained. | Matches routed defect 7 precisely. |
| D14 | false / true | B lacks `.ufo/waves/round-74/pre/c1-base-arm.json`. F has `runner.path = tools/round-74/probe-mutation.py` and `runner.sha256 = 156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b`, equal to that committed blob. | **Atom coverage defect: not routed defect 6's receipt.** The routed receipt is `.ufo/waves/round-73/pre/c1-at-base-r72probe.json`; its blob remains `57202996fc6ebc69b1da54a24e12bafa2ade624cb1bcd8973ea9103e254b89e2` at B and F, with no `runner` key. D14 turns green by binding a different round's receipt, leaving the named defect untouched. Evidence: `binding-evidence.json`. |
| D15 | false / true | B lacks `.ufo/waves/round-74/claims.json`. F introduces it at `021914c0e638454e507087accfe41af1ab69f185`; its five `instruments` and four `loaded_by_counter` hashes each equal the blob at that first-add commit. All nine exact pin/blob pairs are retained in `binding-evidence.json`. | Matches planned (d)'s new freeze-pin procedure, not repair of routed defect 8's permanently flagged round-73 freeze. **Coverage limitation:** D15 checks only round-74 pins; it cannot establish the routed obligation to keep the old standing debt visible. A claim that D15 closes defect 8 would therefore mismatch the routed defect. |

The underlying external mapping is retained verbatim from `corpus/lessons/round-73-verifier-spotcheck.md:120-130`. In particular, line 127 explicitly names the round-73 before receipt for defect 6, and line 129 calls the old freeze permanently FLAGGED and asks that the debt remain visible. Missing future round-74 artifacts explain D14/D15's base false verdicts; those false verdicts alone are not proof of binding the historical defect population.

## Receipt validation and inconsistent-atom attack

Executed `python3 -I -B <audit> --validate <absolute receipt path>` on each:

| Input | Exit | Observed defects |
|---|---:|---|
| `ExecAuditRun/base.json` | 0 | `[]` |
| `ExecAuditRun/freeze.json` | 0 | `[]` |
| `ExecAuditRun/flipped-atom.json` | 1 | `mismatches disagree with the atom rows`; `mismatch_count disagrees with the atom rows` |

The attack copied the valid freeze receipt and changed only D1's `ok` from true to false, leaving `mismatches`, `mismatch_count` and every other field untouched. The validator detects inconsistency; its defect text names the inconsistent aggregate fields, not the individual atom ID. Validation is internal-consistency validation, not independent truth validation of an atom's committed-byte evidence.

## Retained evidence / boundaries

Evidence directory: `.ufo/waves/round-74/w1/ExecAuditRun/`.
- `base.json`, `freeze.json`: requested `--json-out` receipts.
- `base-execution.json`, `freeze-execution.json`: exact subprocess exit/stdout/stderr.
- `base-validation.json`, `freeze-validation.json`, `flipped-atom-validation.json`: exact validator exit/stdout/stderr.
- `flipped-atom.json`: one-field inconsistent receipt.
- `committed-evidence.json`: selected committed source lines, absence records and blob digests for both revisions.
- `binding-evidence.json`: original round-73 runner absence, nine freeze pin/blob pairs, executing-instrument identity.

Only these evidence files and this exclusive report were written in the lane. No build/lint/formatter/selftest or other gates were run. No git mutations, fixtures, credentials reads or environment-value dumps. Scratch `/fast/scratch/hyaku/kaidoku-r74/ExecAuditRun/` was explicitly passed as TMPDIR during execution and deleted in `finally` before reporting. No tools installed. LSP unavailable in this seat's tool inventory; no symbol refactor attempted.

Risk: a future zero-mismatch score is not sufficient evidence of routed defect 6 closure or standing historical-debt visibility. Frozen atom semantics must not be silently amended; parent must distinguish declared predicate success from the observed coverage defects. No landing revision was requested or scored here.

Self-evaluation: accuracy 4 (executed exits and committed evidence; predicate weaknesses inspected, not separately mutation-tested), completeness 4 (all requested arms/table/attack retained; no landing claim), clarity 4 (explicit per-atom table, long source lines in JSON), actionability 4 (D14 substitution and D15 boundary identified; parent owns disposition), conciseness 4 (evidence wrappers duplicate stdout to retain exact execution). Mean 4.0. Improvements: prioritize the D14 coverage disposition, keep D15's historical-debt boundary explicit, and avoid treating parser token checks as semantic proof. User-agreement self-check: these limitations are explicit rather than hidden.
