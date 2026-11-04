# ExecControls — independent finite oracle

Author-side evidence only; not outside admission. Axes: positive-attribution correctness, control discrimination, committed-byte reproducibility.

## Result

Explicit bounded probe completed at exit 0 under Python 3.14.8. Exactly eight declaration-frozen cases were evaluated, including both committed real-entry cases; every output and expectation was boolean.

| Evaluator | Total mismatches | Real mismatches | Mismatching cases |
|---|---:|---:|---|
| Independent delimiter/ASCII oracle | 0 | 0 | none |
| Actual committed legacy `entry_cites` | 3 | 1 | real-withdrawn, commentary-only, withdrawn-head |
| Refuse everything | 3 | 1 | real-primary, plain-positive, multi-positive |
| Accept everything | 5 | 1 | real-withdrawn, commentary-only, withdrawn-head, absent-source, embedded-id |

Neither constant control nor the legacy lexical function reaches the zero-mismatch target. On the two real cases the oracle gives S286=true, S299=false; legacy gives both true. The actual committed first line positively leads with S286 and ends `duplicate S299 withdrawn in-round`. The retained round82 lexical result therefore does not demonstrate positive attribution of S299.

## Reproduction and retained evidence

All artifacts below are relative to `.ufo/waves/round-83/w1/ExecControls/`:

- `probe.py`: independently implemented parser; extracts only committed legacy `entry_cites` (lines 257–261) through AST with `re`, never executes its CLI. No imports or reads of the round83 counter or candidate.
- `receipt.json`: per-case expectations, outputs, mismatch booleans, positive ids, real-case counts, exact source line, revisions, runtime and SHA-256 provenance.
- `legacy-committed.py`: full read-only snapshot from BASE `650344bc37ca303fb9487c1174192057af499b9b`, SHA-256 `88b1dff2385547e1bdb2ecf802d667c38eabe929747075c27ae88f0c5c061487`.
- `entry-committed.md`: actual round82 entry from BASE, SHA-256 `c14b43393b85cc64275f06c00a9195fd03d0e54c4e78c01f897649096b5089ee`.
- `cases-declaration.json`: unmodified frozen fixture bytes from declaration `de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e`, SHA-256 `2066da67577812070fb93bc004bc8818b7f92b761d79fff29f2713189add441f`.

Probe SHA-256: `8a5cf96d206e2357f6d4c7ac112883189c9c7ad5b746d896db11342a5425931f`.

Exact bounded invocation (after creating the empty seat scratch directory):

```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r83/ExecControls python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-83/w1/ExecControls/probe.py
```

The script reads only pinned Git objects and rewrites only its own retained snapshots/receipt. Its exit 0 requires measured oracle=0, legacy=3, refuse=3, accept=5 and one real mismatch for each failing control. Scratch was removed with successful `rmdir` after receipts were retained. No clone or tool installation occurred. No builds, linters, formatters, production edits, frozen-file edits, or Git mutations were performed.

## Limits and integration

This is the declared eight-case calibration, not universal citation parsing, candidate verification, counter authenticity, or outside admission. The independent parser is delimiter/ASCII based rather than the counter implementation; duplicate source fields are refused and the unique source header must occur in the first twelve lines. No LSP device is exposed in this seat; function selection used Python AST, not a cold LSP response. No blockers. L1 owns candidate integration and the frozen counter's prescribed post-integration gate.

## Self-assessment

Accuracy 4/5: exact committed bytes and boolean results retained; no external admission measured. Completeness 5/5: all eight cases, both constant controls and real mismatch counts measured. Clarity 4/5: per-case details require opening the receipt. Actionability 5/5: reproducible isolated command and pinned input snapshots retained. Conciseness 4/5: report includes provenance repetition for auditability. Overall 4.4/5. Improvements: L1 should attach this receipt to its integration evidence; consult per-case receipt rows rather than interpreting aggregate totals as wider coverage. Would the user agree? The explicit finite-scope caveat is intended to prevent overclaiming.
