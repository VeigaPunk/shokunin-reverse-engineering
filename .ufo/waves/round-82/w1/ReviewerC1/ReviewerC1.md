# ReviewerC1 — round 82 C1

Recommendation: correct the receipt-level acceptance defects below before describing this as general full-conjunction record-integrity enforcement. The frozen three-state battery itself passes; no admission/promotion judgment is made.

## Scope and axes

Axes: verdict/record agreement; typed numeric fields; population/summary agreement; original-case identity/uniqueness; structured error reporting. Bounded forged states and outer CLI demonstrations only. No production edits, predicate changes, dispatch, repository sweeps or lane commits.

Reviewed snapshot: `eb227c4694e16cb8fae74df0eea2f07643b46124`, gate SHA256 `6155a1ffa7564acffc755caeafbe450f5b080d00526edf4bef247444ad04e1af`. Evidence paths below are relative to this report's `evidence/` directory. The exact reviewed instrument is retained as `conjunction-gate-reviewed.py`; line references refer to that snapshot, not subsequent worktree edits.

LSP unavailable: `read xd://lsp` returned “No such tool”; references/definition/diagnostics could not be requested. Source inspection and executable demonstrations are the evidence, not semantic-search proof.

## Findings by severity

### High — reported `killed` is not enforced (declared conjunction gap)

`tools/round-82/conjunction-gate.py:101-134` checks rederived `frozen_killed`, `survivors` and `mutants`, but never the receipt's recorded `killed` or `ok`. Starting from the genuine landing receipt, changing only `killed=0` and `ok=false` still gives `conjunction_ok=true`, `frozen_killed=true`, `defects=[]`. Recorded counts are impossible: killed 0 + survivors 0 != mutants 1. This directly conflicts with the plan's stated “killed 1” conjunct if that means the receipt's reported count.

Evidence: `ce5-killed-field.input.json`, CE5 in `c1-forged-states.json`, and the `undersized` arm in `c1-battery-ce5-killed-field.json`. Counter definition: `tools/round-81/record-integration.py:73-80` constructs recorded killed/survivors/ok together from the Boolean kill calculation; the gate does not enforce that invariant on forged records.

Negative control CE5b: recorded killed 1 with mutant exit 0 is correctly refused through `frozen_rule_not_killed`. Thus rederivation protects against false reported kills in that direction; the finding is unflagged record inconsistency, not acceptance of that negative control.

### Medium — case population is padable; original presence is not uniqueness

At gate lines 120-132, the floor counts every list entry; original checks use membership only. Replacing the pristine `record-fixture-committed-duplicate` row with a duplicate `green-validate-consistent` row leaves 11 entries but only 10 distinct names; all nine original names remain present. The conjunction accepts with no defects. Replacing that row instead with `{"pass":true}` also passes: only 10 named case records remain, and an unnamed dictionary supplies the eleventh floor entry.

Evidence: `ce3-dup-original.input.json`, `ce4-caseless-padding.input.json`, CE3/CE4 in `c1-forged-states.json`, and accepted `undersized` arm in `c1-battery-ce3-dup-original.json`. These expose record-integrity/population gaps beyond the literal nine-name-presence requirement; uniqueness itself was not explicitly declared in the frozen plan.

Negative controls: removing an original name is refused (`original_cases_absent`, plus floor); duplicate mutant detector rows are refused (`frozen_rule_not_killed`, `detector_absent_or_passing`).

### Medium — numeric Boolean substitution passes

Gate lines 111-128 use equality against 0/1 and `isinstance(v,int)`, which includes Python Booleans. The exact forged state sets pristine exit `false`, summary `[11,false]`, survivors `false`, mutants `true`. It is accepted with `defects=[]`. These are not the integer fields produced by the pinned counter.

Evidence: `ce1-bool-int.input.json`, CE1 in `c1-forged-states.json`; the actual CLI `dirty` arm in `c1-battery-ce1-bool-int.json` reports `conjunction_ok=true`, `frozen_killed=true`, no defects. This is a type-integrity gap, not proof of an additional failed semantic case.

### Medium — summary population never agrees with emitted population

Gate lines 114-121 validate the summary shape and failures but never use summary[0]. Changing the genuine pristine summary to `[1,0]` or `[0,0]`, leaving 11 emitted rows, is accepted with `defects=[]` and frozen kill true.

Evidence: `ce2a-summary-one.input.json`, `ce2b-summary-zero.input.json`, CE2a/CE2b in `c1-forged-states.json`. This is an internal record-consistency gap. The frozen wording does not explicitly require summary/list equality; it must not be represented as a demonstrated failure of the three declared fixture arms.

### Low — malformed retained receipt gives traceback, no structured receipt

`load_receipt` at line 71 decodes JSON; the calls through `arm` at lines 143/184 are outside the battery's pin-read exception handler. A committed input containing `{ "pristine": [ truncated` gives uncaught `JSONDecodeError`, rc 1, and does not create `--json-out`. That rc is also used for evaluated refusal, so exit code alone cannot distinguish the two.

Evidence: `malformed.input.json`, `c1-battery-malformed.stdout.txt`. Observed json-out absent. This is error-reporting weakness, not a false green.

## Outer CLI receipts and controls

- Pinned canonical gate, lane root, measured rev: rc 0; forged_total 3, refused 3, reasons exactly binder_digest_mismatch/pristine_cases_below_floor/pristine_failures_nonzero, genuine_ok true, frozen_rule_accepts_forged 3, both pins true, validate defects empty. Evidence: `c1-battery-head-pinned.json` and stdout.
- Selftest observed rc 0, 21 cases, zero failures (`c1-selftest.txt`); this run used the concurrently edited worktree, not the retained HEAD copy.
- Private fixture control battery: rc 0 (`c1-battery-fixture-control.json`); counter and binder bytes copied from measured revision with matching frozen digests. `fixture-control.json` retains source hashes.
- CE1/CE3/CE5 outer CLI batteries: rc 1 overall, **not false-green whole-battery exits**. Forged arms are accepted by the conjunction, so their expected refusal reasons disappear; the enclosing battery correctly fails its fixed reason/count checks. Their validate sections remain clean because aggregate receipts consistently report that failure. Variant history is cumulative: CE5 and CE3 fixture commits also retain CE1 in the dirty path; interpret each cited arm independently.
- A worktree gate run with `--rev 9cc8fbbc893d4f76ced1ac8cf66a6239cde91770` also returns the canonical green (`c1-battery-base.json`). Targeted tree read confirms tools/round-82 absent at base. This is not historical execution of a nonexistent gate: it runs newer instrument bytes against historical retained inputs, which the interface permits. Do not use it as red-before proof or as an independent defect. Internal landing receipt rev is `047d18ff49d3f41d8199fadfb545e2d4cbf475e1`, not the evaluation rev; these are deliberately historical receipts.

## Residual risk and verification gaps

The working-tree instrument changed during the review: initial/measured SHA 6155a1ff..., CLI worktree receipts recorded b2dffc42..., and a later targeted digest observed c0b40379.... These are concurrent edits, not evidence of misconduct or a defect by themselves. Remaining demonstrations were explicitly run from the retained measured-revision bytes. Findings apply only to that reviewed snapshot; newer candidate fixes were not assessed.

The literal frozen predicate passes. The findings do not establish whole-battery acceptance of additional forged arms; they establish weaker receipt-level acceptance and bounded error-path behavior. No general saturation, runtime-routing, resume-continuity or domain-capability claim was investigated or established. No repository build/lint/test sweeps were run. No changes to counter/binder pins or frozen predicate were made.

Reproduction materials retained: exact reviewed gate, exact forged inputs, forge driver, fixture builder/variant driver, result table, canonical/variant CLI receipts and tracebacks. Fixture git mutations were confined to the private scratch repository; absolute `git -C` and toplevel assertions preceded commits. TMPDIR was explicitly the seat's scratch work directory. Scratch is removed after retaining named evidence.

Tooling: existing Python 3.14.8 and Git 2.56.0; no installs/updates or package-manager transactions. RULES.md read first with the initial authorization batch. No configs, secrets, PATH directories, production files, fleet-root files or sibling evidence were written.

Report: `.ufo/waves/round-82/w1/ReviewerC1/ReviewerC1.md` (the explicit assigned-slice path inside the mandatory seat-only write boundary; the shorter outside-directory trailer was not duplicated).
