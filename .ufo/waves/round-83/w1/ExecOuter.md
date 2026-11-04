# ExecOuter — R83-C1 outer CLI driver

## Files

- `ExecOuter/candidates/outer-cli-fixtures.py` (relative to this report's directory): executable integration candidate supporting required `--root --rev --freeze --work --json-out`.
- `ExecOuter/receipts/legacy-inspect.json`: frozen counter's actual legacy receipt.
- `ExecOuter/receipts/legacy-inspect.meta.json`: exact invocation, actual exit, hashes.
- `ExecOuter/receipts/syntax-check.json`: historical parse receipt for the initial draft only, superseded by the final comparison correction below. Not evidence for the final artifact.

## Behavior

Mirrors round82's CLI-fixtures pattern: one shared private clone, detached committed revision, clean child environment, isolated entry file, subprocess receipts and cleanup. Baseline lane git reads only; checkout affects only the private clone. No candidate implementation fabricated.

Four cases:

1. Frozen audit on legacy target at BASE `650344bc37ca303fb9487c1174192057af499b9b`, same freeze: require rc1 and `real-withdrawn` in mismatches.
2. Frozen audit on `tools/round-83/source-bind.py` at `--rev`: require rc0 and empty mismatches.
3. Candidate CLI on committed BASE entry, S286: require rc0, attributed.
4. Same entry, S299: require rc1, not_attributed.

The CLI output is retained under `output`. Both CLI cases require matching exit and typed JSON fields: schema `kaidoku-r83-source-bind-v1`, requested `sid`, boolean `cites` (true for S286, false for S299), and `status` (`attributed` / `not-attributed`). These fields were read from the available ExecCandidate candidate, not invented. No unavailable-path claim.

Final comparison correction compares against `clean` for the candidate audit and `attributed`/`not_attributed` for CLI case labels; subject JSON status uses its actual hyphenated spelling. Relative root/work paths are resolved before child execution, and clone toplevel is asserted before checkout. No final-driver execution performed.

## Measured evidence

Only the requested legacy audit was executed. Instrument materialized from declaration `de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e`; BASE target and declaration fixtures read through absolute-path read-only git commands.

Actual exit **1**; **8 cases, 2 real, 3 mismatches**: `real-withdrawn`, `commentary-only`, `withdrawn-head`. Matches the declared legacy expectation. Exact counter result and digests retained in receipts. Candidate-green, subject CLI cases, refuse-everything and full driver were not run here; no green claim.

Initial draft syntax parse was performed, but is superseded by the final comparison correction. Parent owns final verification. No builds, linters or formatters executed.

## Integration

After candidate is committed, run with absolute root/work/output paths:

```sh
python3 -I -B .ufo/waves/round-83/w1/ExecOuter/candidates/outer-cli-fixtures.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev COMMITTED_REV \
  --freeze de4e58b2c22bf4376dc81bd32dfe0b9ac605e17e \
  --work ABSOLUTE_PRIVATE_SCRATCH --json-out ABSOLUTE_RECEIPT
```

Expected after integration: all four cases pass. Not yet measured. Driver uses committed candidate bytes, not working-tree edits.

## Risks and hygiene

Use absolute path arguments. Clone/setup failures propagate after cleanup without a result receipt, following the prior driver pattern. Constants mirror the frozen audit. Child timeout is 300 seconds. Cleanup uses best-effort removal.

Scratch `/fast/scratch/hyaku/kaidoku-r83/ExecOuter/` removed after copying receipt, absence observed. No tools installed; existing Python 3.14.8 and git 2.56.0 used. No production/counter/fixture changes, fleet-root writes, commits, pushes or orchestration. All written files are this report and the owned seat directory. Findings are author-side evidence only.
