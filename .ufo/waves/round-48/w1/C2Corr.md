# C2Corr — R48-C2 correction attack

## Scope and evidence
- Read frozen claims `plans/round-48-claims.md` in full. No frozen or lane implementation files were edited.
- Frozen counter command:
  `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/C2Corr/receipt.json`
- Exit 1. Receipt: `receipt.json`, SHA-256 `f0bf3d66c54b8d954b6f6e0bec2916d31b1afccde806da2ce20ae2260c1ab6be`. Freeze paths unchanged (`frozen_path_changed: []`); round-47 oracle clean (`mismatches: []`, `met_target: true`), but v3 is not met. Concrete failures: round-47 seat floor missing, no R48 correction lines, and `exempted 2` is unsupported by cited round-47 receipts. Battery skipped because structural clauses failed. The two axes score cells were actually examined (`coverage 138/138, 9.72→10.0`; `depth 24/24, 10.0→10.0`), `axis_score_bad: []`.
- Recorder invocation UTC: `2026-10-28T18:48:15Z`; command exit 1. The stdout stream was not separately persisted, so its SHA-256 is **not recorded**. Receipt-file digest above is not claimed as stdout digest.

## Correction probes (in-memory score() on frozen committed bytes)
Ran Python 3 `-I -B` importing `record2`, with `files(path)` resolving via `gate.show(root, freeze, path)`, and called `record2.score(card, files, root, freeze, profile)` on three appended-correction variants. No fixture or source bytes were changed. Probe output:

| Variant | profile | exit | finding |
|---|---|---:|---|
| `- corrects axes depth: 24/24 citation-resolved queue-drain rules.` | v3 | 1 | correction itself has `corrections_bad: []`; overall red for existing structural/quote failures |
| same correct axes line | v2 | 0 | green |
| change `24/24` to `999/999` | v3 | 1 | `corrections_bad` names the line; derived depth pair `[24,24]` |
| same forged axes line | v2 | 1 | red (oracle's old correction parser rejects the supplied correction section; therefore this probe does **not** establish the requested v2-green contrast) |
| `- corrects seats 47: Waves: 1 + 1 = 2 seats.` | v3 | 1 | correction rejected: expected `'<n> waves, <total> seats total'`; overall also red |
| same seats correction | v2 | 0 | green |

The v3/v2 probes use `score()` without battery; do not represent full `evaluate()`/battery acceptance. Axes clause behavior is isolated in v3 by `corrections_bad`: correct pair accepted, `999/999` rejected. However, the requested wrong-v3 / wrong-v2 green calibration was not achieved: v2 returned 1 for this malformed-for-oracle axes-line variant. This is a limitation of the probe fixture, not evidence that v2 catches the axes predicate; the counter's v2 profile returns before v3-specific correction validation.

Seats probe deliberately tests malformed correction grammar, and demonstrates v3 rejects it while v2 accepts it. It does not test a correctly formed but dispatch-total-disagreeing seats correction; not run.

## Risks / blockers
- The freeze card itself is red, so end-to-end battery was skipped and genuine/battery thresholds remain unevaluated at this revision.
- The two requested focused probes are incomplete: a v2-green *well-formed* forged axes correction and a well-formed seats correction with a total conflicting with dispatch are still needed. No implementation issue is inferred from the malformed seats probe.
- No install, build, lint, formatter, or tests run. No verification beyond commands and in-memory probes above.