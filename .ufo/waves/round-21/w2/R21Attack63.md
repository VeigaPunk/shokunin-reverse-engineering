# R21Attack63 — cross-claim separation and R20-SEP control

## Axes

- **R21-C1 — calibration:** binding a cited Evidence ID to the operation in that same successful record, with refusal/negative controls; C1 does not claim cryptographic authentication (`claims.json:8`).
- **R21-C2 — depth:** distinguish malformed/absent observations from bounded silence while retaining kind/index/null semantics (`claims.json:9`).

## Evidence from the frozen round cache

The frozen contract declares 12 C1 and 20 C2 cases, explicitly says each claim's cases must not load the other successor, and keeps the 19 R20 artifact pairs retrospective (`fixture-contract.json:5-42`). `battery.py` selects only the requested case in its loop and materializes that case's validator (`battery.py:70-109`); C1 plus `--regression` is rejected (`:50-51`), while regression is separately dispatched through the C2 comparator/extractor (`:117-140`). This is source-level path evidence, not an import-trace claim.


The following selected JSON fields are copied from **cached verification records, not commands I reran**; their files preserve complete stdout/stderr. Exact extracted output:

| Arm | Exit (expected) | Output fields |
|---|---:|---|
| C1 baseline `2dd430cb6bcad60ff4db720c052074f1f75eecbc` | 1 (1) | `source_path=.ufo/waves/round-20/tools/verb-coverage.py`; `total=12`, `passed=3`, `violations=9`, `false_clean=9` |
| C1 candidate `a75c3c67e4e658a232e1842ab1aceb383b711269` | 0 (0) | `source_path=.ufo/waves/round-21/tools/verb-coverage.py`; `total=12`, `passed=12`, `violations=0`, `false_clean=0`, `undeclared_crashes=0` |
| C2 baseline `2dd430cb6bcad60ff4db720c052074f1f75eecbc` | 1 (1) | `source_path=.ufo/waves/round-20/tools/compare-first-failure.py`; `total=20`, `passed=14`, `violations=6`, `false_clean=5`, `undeclared_crashes=1` |
| C2 candidate `a75c3c67e4e658a232e1842ab1aceb383b711269` | 0 (0) | `source_path=.ufo/waves/round-21/tools/compare-first-failure.py`; `total=20`, `passed=20`, `violations=0`, `false_clean=0`, `undeclared_crashes=0`; all 19 regression rows have `exit=0`, `log_sha_equal=true` |

Exact recorded argv:

```text
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/battery.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 2dd430cb6bcad60ff4db720c052074f1f75eecbc --claim C1
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/battery.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev a75c3c67e4e658a232e1842ab1aceb383b711269 --claim C1
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/battery.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 2dd430cb6bcad60ff4db720c052074f1f75eecbc --claim C2
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/battery.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev a75c3c67e4e658a232e1842ab1aceb383b711269 --claim C2 --regression
```

The records are `verify/before-C1.json`, `after-C1.json`, `before-C2.json`, and `after-C2.json`. Candidate stdout identifies selected source hashes `77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc` (C1) and `990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c` (C2). Thus the nominal C1 and C2 invocations are separable in dispatcher source and cached per-case results. The C2 19/19 is compatibility against retained R20 inputs, not new R21 predictions.

The fixture source and contract are pinned to `d93c85887d9ae77d224c82c8f56bc8cca86d1a75` and `53166ab0aae495c964d956050ca0ca3a4f29014a`; their byte hashes are checked by `battery.py` against `fixtures/expected.json`. This controls input drift across the baseline/candidate arms, but shared, frozen inputs alone do **not** establish causal attribution or independent authorship. One specific C1 duplicate-member guard mutation is separately shown to fail its fixed negative while preserving its positive (`w2/R21Attack66.md:46-75`); that result is local to that mutation and is not C2 mutation evidence.

## R20-SEP boundary and contradiction

R20's historical `_s_d6d` aggregate passed a decoy and the retained C3 receipt at `runs/t1246-addr2line/receipt.json` to the R17 v2 validator and required that receipt to validate (`round-20/tools/routed-r19.py:937-962`). R21's `tools/isolated-control.py` instead creates synthetic receipt metadata and a decoy, then invokes the pinned R17 v2 validator (`round-21/tools/isolated-control.py:18-55`). The cached `verify/isolated-without-C3.json` records this exact argv: `/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/isolated-control.py --root /tmp/kaidoku-r21-verify-vepj60uy`, exit 0. Its stored stdout has `independent_positive` exit 0/valid and `independent_decoy` exit 1 with `analyze_step_unauthenticated`; the helper's reported limit says no C3 forecast/run file was read. This is separate cached evidence, not part of either battery result.

A residual calibration weakness is visible in the helper itself: it builds its positive with `module._carrier_receipt(...)` from the same imported validator that it then tests (`isolated-control.py:18-23,33-42`). The decoy is usefully derived by changing its recorded argv, but the positive is not an independent receipt fixture. Also, the C1 battery does not dispatch `isolated-control.py` (`battery.py:70-109`), so a green C1 battery by itself cannot stand in for the R20-SEP control. The separate no-C3 cache record covers the helper as currently measured, but the two limbs should remain visibly distinct. These are limitations on what the respective outputs prove, not evidence that the cached observations are false.

## One bounded proposal

**Make the R20-SEP positive control an independently authored frozen inert receipt, and keep it as a separately reported C1 control limb.** Replace only the runtime call to `_carrier_receipt` used to manufacture the positive with a small, immutable synthetic receipt fixture authored independently of the validator; retain the paired one-field decoy, no-C3 scratch root, and never execute recorded argv. Record/hash both the selected `receipt-validate-v2.py` and its adjacent `pins.py` (the current helper reports only the validator digest). Keep this result separate from the 12 C1 case denominator and from the 19 historical R20 comparisons; do not fold R20 history into C2 or a shared aggregate score. This combines the round's separate-control and per-case/round-qualified reporting proposals without adding a C2 dependency or changing either frozen denominator.

**Precise falsifier:** with only the pinned validator and `pins.py` in the isolated root and no C3 receipt/run input, the independent fixed positive must validate with exit 0 and the otherwise identical unauthorized-analyze decoy must exit 1 with `analyze_step_unauthenticated`. The proposal fails if the positive is still generated by validator code, either exit/finding changes, the result needs any C3 input, or a C1-only invocation starts loading C2 successor code. For claim isolation, preserve the currently observed selected-tool identity and all 12/20 per-case expectations; keep the historical 19 rows individually marked retrospective.

**Affected axes / risks:** directly strengthens C1 calibration by removing the self-generated positive oracle; no C2 behavior or fixture population changes, so the two C2 depth comparisons remain intact. Risks are stale pinned schema/pin data or accidentally making the new fixture depend on environmental paths; freeze the inert fixture bytes and expected digest, and retain the explicit non-authentication limit. Shared fixture bytes remain a controlled input, not causal proof.

## Verification and bounds

Evidence read: frozen claims/contract, dispatcher and validators, baseline/candidate result records, no-C3 record, and R20's historical caller. Cached checks are reported above; I ran no command, test, build, provider, carrier, or mutation. No source, fixture, Git/jj/index state, or sibling report was changed. No tool installed or updated.

Report: `.ufo/waves/round-21/w2/R21Attack63.md`
