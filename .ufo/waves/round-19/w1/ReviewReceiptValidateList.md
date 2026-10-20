# Receipt validator list-step review

## Finding — Medium: `--require-mid-maps` can accept checks on a non-analyze list step

**Observation.** The validator documents that the flag requires every `pin_checks` entry to have retained map fields *and* requires the `analyze` step to have a check (`.ufo/waves/round-17/tools/receipt-validate.py:33-36,465-468`). The object arm correctly selects `steps["analyze"]`, but the list arm accepts any dict with a truthy `pin_checks` (`:570-585`, especially `:573-578`). Thus a list with checks only on `inspect-go-binary` and an absent/empty analyze check satisfies the presence test; retained-map validation of that other check does not establish that analyze was checked. `_iter_steps` exposes list positions, not a contractual step identity (`:125-128`).

The producer uses an object keyed by step name (`.ufo/waves/round-17/tools/carrier-run.py:307-314,352-353,355-358,380-388`); the source itself says list support exists because the original selftest used a list (`receipt-validate.py:112-119`). The introduced `--require-mid-maps` branch is present in the `d0ab2992149a38794e5ef2474ba5d4ef5ee1e905` → `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` diff.

**Inference — exact fix.** In the strict-mode check, make the list arm fail closed (`ok = False`) rather than treating any list element's `pin_checks` as proof of an analyze check. The accepted list shape has no documented analyze-name binding, so it cannot prove the contract; keep legacy list classification/validation unchanged when `--require-mid-maps` is off. If named list entries are ever made a supported receipt schema, require an explicit `name == "analyze"` and a nonempty `pin_checks`, not an index or any-step match.

**Red regression fixture.** Add a selftest derived from `_carrier_receipt` and the existing valid retained-map setup at `:937-957`: make a real snapshot/map and a matching check (same `taken_at_utc`, `equal`, `changed`, `missing`, `entries`, `map_path`, and `map_sha256` fields as case 4h); place that check only in a list entry named `inspect-go-binary`; include an `analyze` entry with `pin_checks: []` (or omit it). Invoke `validate_paths(..., require_mid_maps=True)` and assert exit 1 plus `mid_checks_absent` at `$.steps.analyze.pin_checks`. The current list arm returns `ok=True` for that shape, so the regression assertion is red on the current implementation; with the fix it rejects the unprovable analyze check. The valid retained map isolates the analyze-presence contract rather than a missing-map finding.

## Residual risk

The defect is confined to list-shaped `steps` under the strict flag. The producer emits object-shaped steps, and the round-18 spot-check records that its real receipts were object-shaped (`corpus/lessons/round-18-verifier-spotcheck.md:191-194`); those runs are not implicated. Rejecting list shape only in strict mode is conservative until an explicit named-list schema exists.

## Verification gaps and commands

No code, tests, or carrier runtime were executed; the fixture is a regression-test recommendation, not an observed run. No LSP device is mounted: `read xd://lsp` returned `No such tool: xd://lsp`. Literal search was only a locator; the finding is based on the source, producer, and contract lines cited above plus the read-only Git diffs.

Commands run (all read-only; exit codes observed):

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format='%H %s' -S'elif isinstance(steps, list)' refs/heads/main -- .ufo/waves/round-17/tools/receipt-validate.py
exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --format='%H %s' refs/heads/main -- .ufo/waves/round-17/tools/receipt-validate.py
exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 -- .ufo/waves/round-17/tools/receipt-validate.py
exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --unified=2 271167473d87ef710f07ecdd98caf0ce12091686 d0ab2992149a38794e5ef2474ba5d4ef5ee1e905 -- .ufo/waves/round-17/tools/receipt-validate.py
exit 0
```
