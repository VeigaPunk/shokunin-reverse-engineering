# ExecCandidate — round83 source attribution candidate

## Deliverables

- Candidate: `.ufo/waves/round-83/w1/ExecCandidate/candidates/source-bind.py`
- Retained receipt: `.ufo/waves/round-83/w1/ExecCandidate/receipts/selftest.json`
- This report: `.ufo/waves/round-83/w1/ExecCandidate.md`

No production, legacy tool, frozen counter, cases, predicate, repository configuration or sibling files changed. No git/jj mutations, clones, installations, builds, linters or formatters.

## Behavior

`entry_cites(text, sid)` is self-contained except `re`: count all column-zero `source:` fields including malformed duplicates across the entry, require exactly one and require that sole field within the first twelve lines, parse complete leading ASCII source ids and literal space-em-dash-space, and compare exact ids. Commentary never contributes attribution. Multiple ids and longer numeric ids are supported without sid-specific branches. CLI uses that same function, not a second grammar implementation.

CLI: `python3 -I -B SOURCE --entry FILE --sid SNNN --json-out FILE`. Exit 0 means attributed, 1 means not attributed, 2 means unavailable (malformed sid, unreadable/non-UTF-8 entry or finding-output failure). Stable findings have no entry paths or timestamps. `--selftest` invokes the own CLI twice per private fixture, checks exit codes, exact expected findings and byte-identical outputs; it never changes cwd.

## Exercised evidence

Explicitly assigned probe only:

```sh
env TMPDIR=/fast/scratch/hyaku/kaidoku-r83/ExecCandidate python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-83/w1/ExecCandidate/candidates/source-bind.py --selftest --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-83/w1/ExecCandidate/receipts/selftest.json
```

Executed with cwd `/fast/scratch/hyaku/kaidoku-r83/ExecCandidate`. Observed command success and output:

```text
selftest positive: ok rc=[0, 0]
selftest withdrawn: ok rc=[1, 1]
selftest malformed: ok rc=[1, 1]
selftest duplicate: ok rc=[1, 1]
selftest duplicate-after-window: ok rc=[1, 1]
selftest unavailable: ok rc=[2, 2]
selftest: passed
```

Receipt records stable findings and working-root preservation. Private fixture directories are removed by selftest; scratch removal follows this report write.

## Axes and limitations

Axes: grammar fidelity, extraction independence, CLI observability, fixture isolation, implementation simplicity. Final function has no external constants/helpers; the initial draft's globals were corrected before the exercised selftest. MutationSubject independently flagged that initial issue and received the corrected location. ReviewerClaim and CriticClaim-2 also received the candidate path for independent read-only assessment.

ReviewerClaim observed the earlier candidate (SHA256 `fa08b06340eb49929ffc34d69ac789c4fde91e83b4714afaff20b020e940ed18`) accepted a line1 source field plus duplicate line13. KaidokuR83 explicitly resolved the scope: duplicates anywhere must reject, with the sole field required within first12. Candidate now implements that interpretation and the final selftest above includes a duplicate-after-window fixture. The initial five-case selftest passed before this finding; the final six-case receipt supersedes it. Frozen cases/counter remain untouched. Reviewer/mutation evidence for the earlier SHA does not independently verify these final bytes.

These are author-side findings, not outside admission or the frozen eight-case counter measurement. No claim of universal citation parsing, fixture authenticity, source novelty or closure of carried debt. L1 must integrate and execute the frozen counter against committed bytes; no counter pass or mismatch count is asserted here. No implementation blocker.

Self-assessment (1–5; overall 4.0): accuracy 4 (own CLI exercised; frozen AST/counter remains L1-owned); completeness 4 (requested candidate and selftest delivered; integration intentionally external); clarity 4 (stable boolean findings intentionally omit detailed malformed-header diagnostics); actionability 4 (exact candidate, receipt and command retained; L1 cutover remains); conciseness 4 (CLI selftest is longer than the small grammar function). Improvements: retain independent AST/counter evidence after integration; keep this finite calibration distinct from grammar-general correctness. Would the user agree? Expected yes for this scoped candidate, not an admission verdict.
