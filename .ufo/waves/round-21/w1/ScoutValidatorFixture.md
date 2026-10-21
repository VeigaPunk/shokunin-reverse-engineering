# Scout — isolated `receipt-validate-v2.py` positive fixture

**Axes:** C1 calibration (the assigned fixture is supplemental D6d control evidence); C2 depth (no C2 implementation inspected or changed).

## Observed

- The R20 D6d aggregate check is explicitly coupled to the C3 run: `.ufo/waves/round-20/tools/routed-r19.py:908-962` builds a synthetic decoy, then passes `.ufo/waves/round-20/runs/t1246-addr2line/receipt.json` as the positive control at lines 941-944. The check is registered as `D6d` and called through `SUBSTANCE[item](ctx)` (`:1037-1068`). The R20 spotcheck identifies this exact dependency as R20-SEP (`corpus/lessons/round-20-verifier-spotcheck.md:134-138`).
- `receipt-validate-v2.py` already has useful synthetic fixture mechanics, but no standalone fixture-builder CLI. `_carrier_receipt` constructs a carrier-shaped base with real file paths/digests and bound-log metadata (`.ufo/waves/round-17/tools/receipt-validate-v2.py:768-809`); `selftest` creates temporary files and removes its temp directory (`:812-1003`, cleanup in `:1183-1199`). CLI options are only `--selftest`, `--require-mid-maps`, and receipt paths (`:1203-1230`). Thus the selftest is a source pattern, not a retained receipt artifact or directly reusable external builder.
- The built-in selftest demonstrates both relevant outcomes: the list-shaped analyze step becomes green when its own entry receives the map-bearing check (`:1072-1118`), while the post-package decoy is rejected with `analyze_step_unauthenticated` and `mid_checks_absent` (`:1142-1167`).
- A positive carrier receipt needs more than an accepted `argv`: carrier shape and required step fields are checked at `:113-132`, `:378-445`; `check_binding` additionally requires `bound_sessions`, at least one bound session, a matching retained `ghidra.log`, and a carrier digest present in `pins_pre` (`:169-243`). The log must contain line-anchored records naming its session path and `target-<sha256-prefix>.bin`; when the carrier is present, its logged MD5 must also match (`:204-239`).
- With `--require-mid-maps`, `steps.analyze` must be authenticated from the actual argv, and that analyze entry must carry a map check. Every `pin_checks` record needs `map_path` and `map_sha256`; the map bytes, entry count, timestamp and equal/changed/missing verdict are rechecked against `pins_pre` (`:491-654`). The validator accepts `npx`, optional `-y`/`--yes`, a pinned `rea-agents@<numeric-version>` package operand, then the immediate `analyze` subcommand (`:134-157`). `pins.snapshot` records absolute real paths and sha256/size/mtime; `pins.compare` recomputes equal/changed/missing/errors (`.ufo/waves/round-17/tools/pins.py:37-106`).
- The R21 frozen contract has twelve independent C1 Evidence-record cases (`.ufo/waves/round-21/fixture-contract.json:5-17`); these are not receipt-shape cases. The contract basis explicitly says “Independent local application contract, not JSON-spec required fields or Evidence authentication” (`:4`). The synthetic D6d receipt should therefore remain a supplementary compatibility control, not replace or count toward those twelve cases.

## Fixture design inference

A portable C1-owned positive can be built at runtime under the harness's isolated temporary directory, then passed as a receipt path to the existing validator CLI alongside the existing decoy. The retained artifact is the C1-owned builder/fixture definition; generated receipt paths and bytes should be fresh for each run rather than checked in with machine-specific absolute paths.

1. Write a synthetic carrier plus stdout/stderr and a synthetic Ghidra log. Put the carrier in real `pins.snapshot` pre/post snapshots, compute its SHA-256 and MD5 from those bytes, and set `pins_compare = pins.compare(pre, post)`.
2. Use a nonempty temporary session path in both `bound_sessions` and `retained_logs`; write the exact log records expected by `check_binding`, including that path, the carrier SHA-256 prefix, and the actual carrier MD5. Keep the retained log and step capture paths/digests consistent.
3. Use object-shaped `steps` with a single `analyze` key whose argv is `npx -y rea-agents@6.5.0 analyze ...`; provide required step fields and one `pin_checks` item on that same analyze step. Build/write the mid-map from the pre snapshot, then record its actual path, digest, timestamp, entry count, and matching compare verdict. Avoid placing map checks only on unrelated steps.
4. Preserve the current decoy negative in the same D6d check and inspect parsed per-receipt results: the synthetic positive must be `valid: true`, while the decoy must retain the expected unauthenticated-analyze refusal. Remove the `t1246-addr2line/receipt.json` path entirely from this control.

This is only local validator-acceptance evidence. The validator's own header limits the result to current-byte digest/pin checks and acknowledges that it cannot prove bytes were not changed and restored between observations (`receipt-validate-v2.py:1-42`). It is not Evidence authentication, target execution, or a security claim.

## Confidence and gaps

- **High confidence** in the required fixture shape and current dependency: direct source sections and the current D6d caller were read.
- **Inference, not observed implementation:** a new R21 builder can reuse this mechanism cleanly; no R21 `battery.py` or new C1 validator hookup was read or executed, so exact integration point is unresolved.
- The `lsp` device was unavailable (`read xd://lsp` returned “No such tool”); searches were textual and are not semantic proof. No external URL was opened or proposed; no source-row support is claimed.

## Parent checks (not run here)

- Run the frozen C1 battery after integration: `python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C1`; preserve all twelve contract cases, and verify the supplemental D6d positive is green while the decoy remains refused without a C3 receipt path.
- Run C2 separately with `--claim C2`; preserve its twenty frozen cases and keep it independent of the C1 fixture.
- Parent owns the stable changed-path smoke and final suite once. No tests, validator runs, builds, or other checks were run for this report; no files except this report were written.

Report: .ufo/waves/round-21/w1/ScoutValidatorFixture.md
