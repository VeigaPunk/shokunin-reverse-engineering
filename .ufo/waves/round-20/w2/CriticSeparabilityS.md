FALSIFIED — strict claim separability at S; this does not establish a changed numeric result.

Axes: calibration (C1) and depth (C3) have shared verification authorities; coverage (C2) is separable for its target-specific criterion.

Evidence (all revision-scoped reads were from Git objects at S; commands read-only):
```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --no-textconv 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-17/tools/receipt-validate.py  [exit 0]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/measure.py | nl -ba  [exit 0]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/tools/routed-r19.py | nl -ba  [exit 0]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/predictions/carriers.tsv | nl -ba  [exit 0]
set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/evidence/carrier-guard/arm.json | jq '.carriers|length'; printf 'exit=%s\n' "$?"  [exit 0; 20]
set -o pipefail; git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/predictions/carriers.tsv | wc -l; printf 'exit=%s\n' "$?"  [exit 0; 21 lines]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 808cbb31a1e24656da5ba4967497e602fbca7415 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/predictions/carriers.tsv  [exit 0]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -F 'inspect-go-binary' 14f0260ad319ecc26994381b2415d5a999003375 -- corpus/knowledge  [exit 0]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -w analyze 14f0260ad319ecc26994381b2415d5a999003375 -- corpus/knowledge  [exit 0]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -F 'rea-agents@6.5.0' 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/runs/t1246-go/receipt.json  [exit 0; lines 1960, 2029]
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -F '"analyze",' 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/runs/t1246-go/receipt.json  [exit 0; line 1961]
```

- **C1 — PARTIAL (calibration).** At S, `routed-r19.py:44,503-507` uses `predictions/carriers.tsv` as D3's expected carrier set when present. It is present unchanged from F; the S manifest has 20 rows and `arm.json:4-184` records 20 paths, including `link` (manifest `:13`, arm `:104-111`); the paths shown match. But if C3 is reverted with its TSV, the S checker takes `wanted = arm_paths` (`routed-r19.py:503-505`), making the set comparison self-referential. **Inference:** the D3 check remains runnable, but no longer independently establishes the intended set; an arm/check pair over a reduced self-selected set can meet its count tests (`:516-526`). This is a scope/provenance dependency, not proof the S D3 result is wrong. C1's “census at delivered tip” is likewise tip-scoped (`claims.json:17-18`) and must be rerun on any reverted tree.
- **C2 — HOLDS for the target-specific criterion (coverage).** `verb-coverage.py:209-231` scans every knowledge entry, but the C3 entry's explicit REA command names are `analyze` and `inspect-go-binary` (`corpus/knowledge/2026-10-20-r20-go1246-first-failure-forecast.md:3,16`), both already mentioned at B (commands above). Removing that C3 entry therefore does not change the mentioned-command set; C1 does not own C2 target entries/evidence. This is a source-level determination, not a rerun of the counterfactual.
- **C3 — PARTIAL (depth).** `measure.py:153-166` materializes `receipt-validate.py` and `pins.py` from the measured revision; `:276-332,379-445` uses that validator for each receipt. The B→S diff removes the no-package/declaration fallback for list-shaped analyze identity and adds explicit unauthenticated-step findings; S requires `analyze` immediately after the `rea-agents@<version>` token (`receipt-validate.py:134-165`). This is C1's D6d correction (`routed-r19.py:878-915`). Thus C3's *validation authority* depends on C1, and the C3 output does not report the validator blob identity. The observed `t1246-go` receipt has the direct package/analyze sequence at `:1960-1961`, so it does not show a result flip under the older rule; I did not test all receipts against B's validator. No claim that C3's 19/19 count changes is supported.

Smallest safe correction: either declare D6d and its exact validator blob as a C3 prerequisite (record that blob ID in C3 measurement), and declare a frozen, C1-owned guard manifest shared with D3; or, for true revert separability, make the C3 analyze-identity check C3-local and make D3 require its own expected manifest (remove the arm-self fallback). Re-run the tip census for any counterfactual tree.

Report: .ufo/waves/round-20/w2/CriticSeparabilityS.md
