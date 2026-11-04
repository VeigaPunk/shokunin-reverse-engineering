# ExecControls — round 71 frozen controls

Axes: coverage (C1 runtime evidence), calibration (C2 lying-field discrimination), operability (C3 registry drift). No implementation changes; frozen bytes remained unchanged.

## Execution and provenance

Freeze: `b827a8b5d54f2885ec9be7786389f356c59226ce`. All five working-tree instrument hashes matched both the freeze blobs and claims-container pins before execution (`execution-provenance.json`). Python `/usr/bin/python`, 3.14.8. No tools installed or upgraded. LSP was unavailable in this seat's exposed tools; source inspection and Python AST were used, with no symbol refactoring.

The requested frozen controls command exited **0**, `arms_passed=6`, `target=6`, `failed=[]`: `controls-at-freeze.json`, `controls.stdout`, `controls.stderr`, and exact `controls-command.json` retained here. Execution used bwrap with the host filesystem read-only, seat scratch/findings writable, and the historical round-70 landing path namespace-bound to seat scratch. This was necessary because unmodified controls.py:89–91 recreates a historical pinned packer outside the assigned scope. No host historical path was modified. The sandbox changed filesystem visibility, not frozen instrument bytes or receipt contents.

The independently repeated controls used byte-identical freeze copies of the counters in seat scratch, independent descriptive-ID fixtures, and the same read-only isolation. `independent-controls.json` retains full argv, stdout, stderr and exit code for every execution. Per-control stdout/stderr files are also retained.

## Six observations and shortcut coverage

| Control | Frozen run and independent observation | Shortcut needed to reach target; does control catch it? |
|---|---|---|
| c1-base-world | rc 1, 7/10; only A8_child_env_observed, A9_concurrent_collision, A10_run_binding false, in both runs | Reuse the unchanged round-70 route and call seven arms ten. Caught: runtime probe still names all three missing capabilities. This does not independently establish that a new route earns 10/10. |
| c1-constant-probe | rc 1; ten `no observation` defects. Independent fixture uses the actual ten descriptive arm IDs and receives ten corresponding defects. | Assert ten true arms with empty observations. Caught. Nonempty fabricated observations are outside this narrow control's demonstrated coverage; structural validation is not runtime authenticity. |
| c2-do-nothing | Committed round-70 battery: ten base-world shapes, two landing-world shapes, no lying_shapes key. Independently re-derived, actual total 12. | Re-label the old receipt as the eighteen-row battery without exercising six lying fields. Caught by the missing lying rows and unchanged baseline counts. The frozen control's displayed forged_total/target are misleading; see EC-1. |
| c2-constant-battery | rc 1; all six lying rows rejected for rc pair not (0,1). Independently constructed six named classes likewise rejected. | Report (first_cut_rc,superseded_rc)=(0,0) as discrimination success. Caught. Merely fabricating a (0,1) pair is not ruled out by this structural control alone; genuine execution evidence remains necessary. |
| c3-base-nonconformant | rc 1, 88 rows, six nonconformant round-70 rows. Independent full output names packed-elf, mutation-check, contract-probe, seam-probe, forged-receipts, controls, each with exactly ['pinned-empty']. | Do nothing to the malformed registry and claim clean census. Caught. The baseline does not show the repaired registry is clean. |
| c3-junk-row | rc 1; five-cell missing-path row has exactly cells<6, pinned-empty, path-absent. Independent one-row fixture reproduces all three. | Treat the row as tolerable grammar or silently ignore it. Caught for this fixture. Not evidence that every possible malformed row is rejected. |

## Independent committed do-nothing checks

`independent-committed-baselines.json` records revision identities, SHA256s and exact derived values. The retained committed source artifacts are `round70-battery-committed.json`, `round70-landing-committed.json`, and `round70-probe-committed.py`.

1. Battery receipt at freeze: `shapes=10`, `landing_probe_shapes=2`, `lying_shapes` absent. Total is **12**, not 16 or 18. The receipt is not present at measured commit 7c155617 (git show returned 128); it was read from freeze committed bytes, not assumed present at its measured revision.
2. Landing receipt at freeze: no top-level `run_root`, `child_env_observed`, or `run_nonce` key.
3. Probe source at `7c155617bb42dadf1725b88a06fe3f235c364f0a`: **eight syntactic arm() calls but seven distinct runtime arms**. A2_threaded_path has separate mutually exclusive if/else calls. Remaining IDs are A1 and A3–A7. Thus seven-arm baseline is correct; a literal seven-call assertion is not.

## Defects and limitations

**EC-1 — control receipt count labeling:** controls.py:130–138 computes `forged_total=shapes+lying` (10) while separately showing two landing-world rows, and emits `target=16`. Its docstring says 12 baseline rows and target 18, matching the overall C2 predicate. The predicate actually used by this arm remains correct (10 base, 2 landing, 0 lying), so this is an evidence-precision defect rather than a failed six-control run. Interpret 16 only as base+lying subset target, never the declared overall eighteen-row target; the output does not label that subset.

**EC-2 — scope-unsafe historical fixture recreation:** controls.py:89–91 writes the round-70 receipt's historical absolute packer path. A direct unsandboxed run violates this seat's write bounds and can collide with other seats. Namespace isolation allowed the frozen command to run without modifying that host path. Route this finding; no repair was made.

Controls are negative/shortcut checks, not substitutes for the three positive claim receipts. The plan's post-freeze and positive-runtime kill rules remain parent-owned. No full build, lint, formatter or unrelated tests were run. Only explicitly assigned controls and independent rechecks were executed. Prior round spot-check disagreements/routed items were read as input; unrelated bookkeeping repairs were not made by this seat.

All scratch fixtures and copied tools were removed after retaining evidence. Scratch/provenance paths nested inside receipts are run pointers, not evidence; the files retained in this findings directory are evidence. The requested outside-directory trailer report was intentionally not written because the binding write scope permits this directory only.

## Self-evaluation

Accuracy 4/5: raw committed and executed evidence retained; sandboxed execution rather than unrestricted host execution is explicitly disclosed. Completeness 4/5: all six controls and three baselines rechecked; positive claim verification intentionally belongs to other seats. Clarity 4/5: count-label and literal-call disagreements separated from behavioral results. Actionability 4/5: EC-1/EC-2 have exact lines and consequences; fixes cannot be landed by this seat. Conciseness 4/5: one observation table plus retained raw artifacts avoids repeating full stdout. Overall 4.0/5. Improvements: label subset counts explicitly and replace historical-path fixture writes in a disclosed future instrument revision. Would the user agree? Evidence supports the six-control result without implying all three claims pass.

VERDICT: met — six frozen controls and independent baseline rechecks; defects EC-1 count labeling and EC-2 out-of-scope historical fixture write named.
