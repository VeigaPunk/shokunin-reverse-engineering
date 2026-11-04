# ExecCounter — round 81 frozen-counter audit

Axes: **calibration + depth**; no domain coverage or promotion claim.

## Scope and provenance

Read the plan and counter at frozen commit `abdcfd3c28d98288a3dc6b4e98c88d115ed42b53` using read-only `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show`. Base is `5b59ae615a2ab68e3b421820d1c72751e1185385`. Retained exact frozen bytes in `frozen-plan.md` and `frozen-counter.py`; counter SHA-256 `52c829c604a5aac9306458cc6291b8cc648d3999ccf2eec0348666e582d524d6`. No frozen/production file changed.

Executed only the assigned base control once and nine bounded classifier fixtures. `audit.py` is the retained reproducer, not an integrated test runner. All command argv, exits, stdout and stderr are in `commands.json`; individual receipts retain both arms. The classifier fixtures are intentionally synthetic output producers, **not** candidate selftests or evidence of real binder integration.

## AST anchor and actual kill rule

`omit_commit` selects the first top-level synchronous `FunctionDef` named `make_fixture_repo`, then walks it for expression statements whose value is a call and whose descendants contain the exact string constant `commit`. Exactly one expression is required. It replaces that expression's complete source-line span with an indented `pass`, leaving other lines intact. Base anchor: lines 111–113, indentation 4; `anchor.json` retains its exact source. It is the fixture git commit subprocess call. The base fixture checks `git rev-parse --show-toplevel` before adding/committing and uses an absolute `git -C` root.

This is a structural anchor, not a semantic proof of git invocation: any expression-call containing the constant qualifies; assigned calls, async definitions or computed `commit` strings do not have the same anchor. The synthetic probes deliberately exploit only that documented structural shape. Do not change it after scoring.

Actual kill conjunction (frozen counter lines 75–78): pristine exit 0 and any parsed summary; mutant any parsed summary and exit 1; exactly one JSON case row named `record-fixture-committed-clean`, with `pass is False`. JSON cases come only from stdout; last regex-matching `SELFTEST cases=N failures=N` is used. No check re-derives summary counts, requires the pristine declared case, inspects stderr, or proves real binder execution.

## Retained results

| Receipt basename | Counter exit | Pristine summary | Mutant summary | killed / survivors |
|---|---:|---|---|---|
| `base-control.json` | 1 | 9/0 | 9/0 | 0 / 1 |
| `declared-failure.json` | 0 | 11/0 | 11/1 | 1 / 0 |
| `absent-case.json` | 1 | 11/0 | 11/1 | 0 / 1 |
| `wrong-case.json` | 1 | 11/0 | 11/1 | 0 / 1 |
| `crash.json` | 1 | 11/0 | absent | 0 / 1 |
| `no-summary.json` | 1 | 11/0 | absent | 0 / 1 |
| `duplicate-case.json` | 1 | 11/0 | 11/1 | 0 / 1 |
| `undersized-pristine.json` | 0 | **1/0** | 11/1 | **1 / 0** |
| `dirty-pristine-summary.json` | 0 | **11/3** | 11/1 | **1 / 0** |
| `extra-wrong-case-failure.json` | 0 | 11/0 | 11/2 | 1 / 0 |

Base control reproduces the frozen before-value: removing the commit leaves all nine old FakeModule cases passing. Absent case, wrong case, crash before summary, no summary, and duplicate declared rows are not kills. The extra unrelated failing case does not prevent a kill when the unique named detector also fails; do not describe the counter as enforcing exclusive failure.

**Concrete predicate gap:** the last two pristine-summary probes violate the frozen plan's explicit pristine >=11 cases / zero failures requirement yet produce counter `ok: true`. Therefore a green counter receipt alone does not establish the full predicate. L1 must independently inspect pristine summary and the real integration implementation. I notified KaidokuR81 of these exact receipts. The two-condition `future-counter-hardening.patch` is an unapplied advisory for a future freeze only; it must not replace/amend this round's scored counter or predicate. It addresses those two numeric gaps, not output authenticity or semantic binder execution.

[INFERENCE, not exercised] A crash after printing a failing declared case and matching summary can satisfy the same exit-1 conjunction because stderr and exception origin are not classified. The exercised crash is specifically pre-summary; no general crash-proofness claim follows from it. Likewise synthetic cases advertising 11 while emitting one case illustrate that summary text is trusted, not independently enumerated.

## Printed counting commands

`printed-commands.json` retains both exact frozen sh blocks and the round-76 helper's static assessment. Both have zero placeholder/metacharacter defects and use the recognized `$REV` / `$OUT` (plus C2 `$WORK`) substitutions. As shell commands they require execution from the lane, bound variables, and paths without whitespace because the variables are unquoted. No initial variable bindings are printed. C2 includes required `--work`; C1 has no work parameter.

Both are refused by `tools/round-76/plan-command.py` because `SAFE_SCRIPT_PREFIX` is literally `tools/round-76/`, not because their round-71/round-81 script syntax is inherently unexecutable. The helper checks prefix before spawning either command. This is the named generalization debt, **not a third claim**. No helper or frozen command was modified. C1 was not executed by this seat; C2's base-control argv uses absolute paths, the required target override, explicit work and TMPDIR, and emits its expected exit-1 receipt.

## Opened source admit/rejection and reuse

Opened Python documentation on 2026-11-04, page title Python 3.15.2:

- **Admit for the scoped AST explanation:** https://docs.python.org/3/library/ast.html#ast.AST — `lineno` and `end_lineno` are documented as first/last source lines, 1-indexed; this grounds why `[lineno-1:end_lineno]` replaces the entire anchor span. The docs also identify `col_offset` as UTF-8 byte offset; the actual anchor has ASCII spaces. This source does not prove that the counter selects the intended subprocess semantically.
- **Opened and rejected as an alternative code parser:** https://docs.python.org/3/library/ast.html#ast.literal_eval — located entry lines 2341–2360 says it evaluates only literals/container displays, with no name lookups or ability to call out; it cannot parse a function definition and does not justify arbitrary-source safety. Flip only if the input contract becomes literal-only data; that is not this round's source-code contract.

Both URLs canonicalize to the existing source URL in `corpus/SOURCES.md` **S291** (line 207). Reuse S291 with these distinct scope notes; no SOURCE row was created or duplicated. Existing S291 rejects literal_eval for annotation grammar, which is compatible with the rejection above, not an endorsement of this counter. Source-open tool output retained in this session: AST node-location section; literal_eval located excerpt. No new source snapshot/hash is claimed.

## Boundaries, cleanup and handoff

Only this seat directory was written. The only fixture git writes were inside `/fast/scratch/hyaku/kaidoku-r81/ExecCounter/classification-repo`; `commands.json` records init, absolute-root verification, add and one fixture commit. Base battery's fixture writes stayed under the same seat scratch via the counter's explicit work/TMPDIR. `cleanup.json` records scratch removal after receipts were retained. No tools installed; no client configs, credentials, environment values, lane git writes, builds, lint, formatters or repository test sweeps were accessed/run. No LSP device was exposed in the mounted device inventory; semantic navigation was unavailable, so AST and exact source inspection were used without claiming LSP results.

The report is inside the explicitly authorized seat directory rather than the conflicting shorter trailer path outside it. L1 owns the integrated measurement and manual checks of >=11/0, preservation of the nine cases, and real clean/duplicate committed binder integration. No admission vote is supplied.

Self-evaluation: accuracy 4 (crash-after-summary limit explicitly inferred, not exercised); completeness 4 (integrated candidate verification belongs to L1); clarity 4 (long audit, compact result table); actionability 5 (receipts and future-only minimal patch); conciseness 4 (provenance retained explicitly). Average 4.2. Highest-impact improvement is L1's independent pristine-summary and integration inspection; do not infer those from `ok` alone.

Report: .ufo/waves/round-81/w1/ExecCounter/ExecCounter.md
