# ExecAttr — round 82, outside round-81 defect 6

## Scope and candidate

Axes: attribution correctness, scoring preservation, bounded reproducibility. Candidate only; no production file, lane Git/JJ state, configuration, MANIFEST, commit or push changed. L1 owns integration and admission.

`producer-path.patch` changes exactly one line in `tools/round-81/strictness-battery.py:383`: receipt `instrument.path` becomes `tools/round-81/strictness-battery.py`. The complete proposed file is `strictness-battery.candidate.py`.

The independent defect is specifically the producer path, as recorded in `corpus/lessons/round-81-verifier-spotcheck.md:126`. Preserve inherited `ROUND=80`, schema, base, fixtures and binder defaults: they describe the inherited scoring contract. Renaming them would widen this repair beyond the routed finding. No scoring logic or validator changes.

## Observed before → after

Inputs exported directly from container freeze `2d63e1a7d04d4dcff45c3908bb51be787a2f22e1` into one private checkout directory; `input-pins.json` retains all five source digests. This was a selective committed-byte checkout/export, not a clone with lane history or configuration.

| Finding | Before | After |
|---|---|---|
| Actual scoring exit | 0 | 0 |
| Red / green population | 4 / 2 | 4 / 2 |
| Candidate false greens / green refusals | 0 / 0 | 0 / 0 |
| Control false greens / green refusals | 4 / 0 | 4 / 0 |
| Internal validation defects | [] | [] |
| Label resolves to recorded producer digest | false | true |

Before: receipt labels `tools/round-80/strictness-battery.py`, whose digest is `f2aa8422f4d5ac93d1e3ed2823eb72869694b46682e90d8e1e908c0555da2a0a`, but records actual round-81 producer digest `6bffdbc1c2f027c7b70cadfb70aabdf5ec6a9e3a6067484886d3560fad3efe3c`. Thus a genuine successful scoring receipt is a counterexample to sound producer attribution. Its existing validator reports no defect despite that path mismatch.

After: receipt labels the round-81 path and records candidate digest `1f7f3910ae7185be1811d88f4c807542a880867b3b41efcc0732a1fad630fae9`; that path resolves to the same bytes. All receipt fields except `instrument` and `checked_at` compare equal (`comparison.json`). This is attribution red→green, not a claim that the scorer's exit changed.

## Execution and isolation

`before.execution.json` and `after.execution.json` retain exact argv, cwd, explicit child environment and exits. Both ran the real scoring CLI, not `--selftest` or a fabricated receipt, through retained `scoring-launcher.py`. The launcher uses `runpy` without replacing any binder function. `--work` and TMPDIR were explicitly below `/fast/scratch/hyaku/kaidoku-r82/ExecAttr/`.

The scoring implementation normally attempts live configuration reads during duplicate-record cases. A pre-I/O audit hook rejected every host-home file open; each arm refused 22 attempts. Consequently no live client/configuration content was read. Missing live objects are handled by the real binders' existing OSError path. This does not establish live pointer freshness or successful live object binding; it establishes the frozen red/green scoring and producer metadata under the disclosed no-host-read condition. Bind-only controls consume the frozen fixture lines directly.

The scorer itself creates private Git fixture repositories, checks `rev-parse --show-toplevel` against their absolute paths before add/commit, and uses absolute `git -C` paths. Child HOME was private; system/global Git configuration was disabled explicitly. No lane Git mutation occurred. Scratch was removed only after evidence/candidate retention; `cleanup.json` records removal. No scratch inventory was performed.

## Supersession requirement for L1

Landing this one-line fix changes round-81 instrument bytes and digest. Append a disclosed instrument supersession to the round-81 container/history, with old→new target identity, exact integrated revision and reason; preserve old pins/receipts as historical evidence rather than rewriting them. Re-observe/rebind any active evidence that is intended to describe the repaired producer at its new committed revision. In particular, an old record-integration receipt's target digest describes the old subject and must not be presented as certification of the changed subject. The old C2 evidence exercised selftest output, not this faulty scoring mode, so this finding does not retroactively refute the demonstrated C2 claim. Do not modify the frozen predicate or original counter to make old evidence appear newly produced. This seat grants no supersession or promotion authority.

## Retained artifacts and limits

All artifacts are relative to this report's directory:
- `producer-path.patch`, `strictness-battery.candidate.py`: minimal proposed repair.
- `input-pins.json`: freeze and exact inputs.
- `before.json`, `after.json`: genuine complete scoring receipts.
- `before.stdout`, `after.stdout`, `before.stderr`, `after.stderr`: actual process output (stderr empty).
- `before.execution.json`, `after.execution.json`: exact process receipts.
- `scoring-launcher.py`: safety wrapper used for both demonstrations.
- `comparison.json`: observed digest mismatch→match and unchanged scoring payload.
- `cleanup.json`: private scratch removal.

Only the assigned two scoring demonstrations ran; no build, lint, formatter, repository test sweep, selftest or sibling gate ran. No installed/updated tooling: existing Python 3.14.8 and Git 2.56.0 sufficed (no install channel applicable). RULES.md read before tooling; pacman remained paused. No LSP tool is mounted in this seat; supported-symbol lookup was unavailable, and the change is a literal metadata path rather than a symbol refactor.

Process limitation: initial discovery used unnecessarily broad repository grep and shell directory/search/paging commands before narrowing to the cited defect and exact source ranges. Those were read-only but not the preferred scoped discovery method; no such output is used as provenance evidence here.

Self-evaluation (not an expertise/admission score): accuracy 4 (two genuine runs, but host reads intentionally refused); completeness 4 (candidate and receipts complete, integration/supersession explicitly L1-owned); clarity 4 (distinguishes scoring success from attribution failure); actionability 4 (one-line patch plus retained full candidate, committed rerun belongs to L1); conciseness 4 (isolation details are necessary to bound the result). Overall 4.0. Highest-impact improvement: L1 should bind the repaired instrument at its actual integrated revision, not reuse this private candidate's receipts as a committed landing certificate.
