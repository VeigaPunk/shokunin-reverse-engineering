# C2Oracle — oracle sourcing experiment

Axes: depth (oracle provenance), calibration (actual v3 verdict).

## Exact measurement

Freeze and revision both `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`.

Command (exit 1):
```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C2Oracle python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out .ufo/waves/round-48/w1/C2Oracle/receipt.json
```
UTC `2026-10-28T18:47:56Z`; stdout SHA-256 (identical to receipt file): `f0bf3d66c54b8d954b6f6e0bec2916d31b1afccde806da2ce20ae2260c1ab6be`. Receipt: `receipt.json`. Frozen paths unchanged. Oracle reports `met_target=true`, `mismatches=[]`, atoms 44, corrections 2. Overall v3 `met_target=false`; failing: round-47 lacks seat atom/re-derived seats correction; no correction line re-derived; unbacked quote `exempted 2`. Floor shows round-46 seats=1, round-47 seats absent; both have path/rev/claim IDs. Axis score cells read coverage 9.72→10.0 for 138/138, depth 10→10 for 24/24. Battery skipped because structural clause fails.

## Stub attack

Copied lane to `/fast/scratch/hyaku/kaidoku-r48/C2Oracle/copy`, replaced only COPY's `tools/round-47/record.py` with a two-line `print("GREEN STUB")` script, then invoked:
```sh
python3 -I -B /fast/scratch/hyaku/kaidoku-r48/C2Oracle/copy/tools/round-48/record2.py --root /fast/scratch/hyaku/kaidoku-r48/C2Oracle/copy --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out /fast/scratch/hyaku/kaidoku-r48/C2Oracle/copy/.ufo/waves/round-48/w1/C2Oracle/stub-receipt.json
```
Exit 1, same JSON stdout byte-for-byte as the direct run (SHA-256 `f0bf3d66c54b8d954b6f6e0bec2916d31b1afccde806da2ce20ae2260c1ab6be`). This demonstrates the replaced helper has no effect on the result. The attempted initially-outside-root JSON path was refused (exit 2, `--json-out outside the lane root`); retry used an in-lane path.

## Provenance boundary

`record2.py` line 35 adds its own directory and `../round-46` to `sys.path`; line 37 imports `gate` from the worktree. Its `oracle(root,rev)` calls `gate.show(root,rev,ORACLE)`, then compiles/executes those returned committed bytes (lines 62–73). Thus the round-47 `record.py` worktree replacement is irrelevant, but the gate implementation is not revision-pinned. Current `tools/round-46/gate.py` SHA-256: `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` (captured at measurement time). This lane's worktree was already dirty before the experiment, including `tools/round-48/meanings.py`; I did not alter lane source files. Bound: the observed evidence establishes only that the present gate returns committed oracle bytes in this execution; it does not establish historical gate integrity or resist a modified gate that falsifies `show` results. The stub test itself ran a copied counter and gate, not a deliberately malicious gate; such tampering was not measured.

No installs. No build, lint, or tests run. No freeze/landing recommendation beyond this measured provenance boundary.
