# Round 16 · w1 · ReviewMinorIsolation — no fallback across major/minor

Scope: source contract (S003) and installed data at `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`. Read-only: `unzip -p`, `cat -n`, `ls`, `grep`. No Java/Python executed, no builds, tests, or checks run. No candidate `selection.py` exists under `.ufo/waves/round-16/` (checked), so this review covers the source contract and proposed failure modes.

Axes: depth (source-anchor and data-overlap evidence), calibration (each claim labelled by evidence strength).

## Verdict on the target

Source shows **no cross-major/minor fallback in the snapshot path**. Isolation is enforced by filename construction plus a same-minor patch walk. Real risk sits in (a) a `selection.py` port that naively uses "nearest lower diff" across minors, (b) lenient version parsing, and (c) the applier's lack of base-identity checks, which turns any mis-selection into silent corruption rather than an error.

## Source anchors (verified by reading shipped source)

Snapshot path (`GoApiSnapshot.java`, extracted from `Base-src.zip`):

- `GoApiSnapshot.java:118-126` `getApiSnapshotJsonFile`: base is `goVer.withPatch(0)` (L122) resolved by `getApiFile(baseVer,"","")` (L123). If the base is missing, returns `null` (L124-126) before any diff is consulted. A diff can never be applied to a different minor's base.
- `GoApiSnapshot.java:115` `get`: null base → `EMPTY`. So `missing_base` yields no snapshot, not a neighbour's.
- `GoApiSnapshot.java:148-166` `getPatchVerDiffFile`: loop `while patch>0 && (diff = lookup(patchVer)) == null → patchVer = patchVer.prevPatch()`. Only the patch number changes; the walk stays inside one major.minor.
- `GoVer.java:134-136` `prevPatch()` returns `new GoVer(major, minor, patch>0 ? patch-1 : 0)`. Major and minor are preserved.
- `GoApiSnapshot.java:168-178` `getApiSnapshotFile` builds `typeinfo/golang/%sgo%s.json%s` from `goVer.toString()` (`GoVer.java:155-158`, `"%d.%d.%d"`). Names are canonical integers, not echoed request text.
- `GoApiSnapshot.java:159-161` warns `"Falling back from %s to %s"` for same-minor patch fallback, including the patch-0 base-only result. Base-only is logged as a patch fallback, not as a distinct unpatched state.
- `GoApiSnapshot.java:183-192` `getApiFile` tries `go%d.%d.%d.json`, and only when patch is 0 (L187) falls back to `go%d.%d.json` (L188). Grep of the whole `Base-src.zip` finds no caller besides its definition, so it is dead in this snapshot. Forbidden by contract; must not be ported.
- `GoVer.java:46-48,62-81` `parse` defaults a missing patch to 0 and accepts several non-strict forms (see F4).

Caller and version source (`Base-src.zip` lines):

- `GoRttiMapper.getGoBinary` `397471-397491`: `buildInfo == null || goVer invalid` (L397474) → `GoBuildInfo.fromFallbackInfo` (L397475-397477) substitutes a version string. `SUPPORTED_VERSIONS = 1.15-1.25` (L397399, checked at L397490); out-of-range only logs `Msg.error` (L397491) and continues. No automatic minor substitution.
- `GoBuildInfo.fromFallbackInfo` `391762-391772`: returns a build info with the stored fallback version string when that string parses valid.
- Fallback is user-set via analyzer option `Fallback Go Version` (`Base-src.zip` L71986-72003, L72020; set at L70805 `GoBuildInfo.setFallbackVersion`). This is the **only** cross-minor path in the tree, and it is an explicit user override, not an automatic fallback (F5).

Applier (`JsonPatchApplier.java`, `JsonPatch.java`):

- `JsonPatchApplier.java:83-94`: REMOVE for object keys is `parentObj.remove(targetName)` (L87-90) with no comparison to the old value. The array branch (L99-101) removes by index without checking the old value.
- `JsonPatch.java:183-189`: section header is only `@ <json path>`. No base or target version identity is present in the diff format. `lineFromJson` (L172-181) requires a value only for ADD.

## Installed data inventory (verified by `ls`)

- Bases (11): `go1.15.0.json` … `go1.25.0.json`. All are `X.0`.
- Patch diffs (123): per minor 1.15:15, 1.16:15, 1.17:13, 1.18:10, 1.19:13, 1.20:14, 1.21:13, 1.22:12, 1.23:12, 1.24:6, **1.25:0**. Each minor's patches are contiguous from 1. Every diff's base exists (no orphan diffs).
- `golang_1.15…1.23_anybit_any.gdt` (9 files) cover 1.15–1.23 only. Not consulted by `GoApiSnapshot`; noted as scope boundary.

## Findings

### F1 — Source has no cross-minor fallback (confirmed, informational)
Anchors: `GoApiSnapshot.java:118-126, 148-166`; `GoVer.java:134-136`. Missing base → `EMPTY`; missing patch diffs → base-only at same minor. Calibration: high (direct source reading).

### F2 — Nearest-lower across minors would be wrong on present data (proposed failure; high-impact for the port)
A "nearest present diff ≤ request" search that ignores minor boundaries selects wrong patches. Concrete counterexamples from the inventory:

- Request `1.25.N` (N≥1): no 1.25 diffs exist. Source walks to `1.25.0` and returns base-only (`GoApiSnapshot.java:148-166`). A cross-minor port selects `go1.24.6.json.diff` (the highest 1.24 diff) onto `go1.25.0.json`. Wrong.
- Request `1.16.0`: base only. Cross-minor port selects `go1.15.15.json.diff`. Wrong.
- Request `1.17.0`: base only. Cross-minor port selects `go1.16.15.json.diff`. Wrong.
- Request `1.26.x`, `1.14.x`, `2.0.0`: must report `missing_base`, not borrow `go1.25.0.json`/`go1.15.0.json`.

Required fixtures (for the planner): each of the above, plus `1.24.7` (same-minor nearest lower → `1.24.6`, allowed) to check that same-minor fallback still works. Calibration: high for the inventory and the source contract; the "wrong" verdict is by source-law (`getPatchVerDiffFile` loop), not by executing an applier.

### F3 — Applier has no base-identity check; mis-selection is silent (defect risk, medium-high)
`JsonPatchApplier.java:87-90` removes keys without comparing values, and the diff carries no version header (`JsonPatch.java:183-189`). Minor isolation therefore rests entirely on file naming, and a wrong pairing never errors.

Data-overlap evidence (line-level `grep -F` of REMOVE lines, substring-level, approximate):

- `go1.15.15.json.diff`: 773 distinct REMOVE lines. Present in `go1.15.0.json`: **761/773**. In `go1.16.0.json`: **84/773**. In `go1.25.0.json`: 31/773.
- `go1.24.6.json.diff`: 832 distinct REMOVE lines. In `go1.24.0.json`: **825/832**. In `go1.25.0.json`: 86/832. In `go1.23.0.json`: 112/832.
- `go1.16.1.json.diff`: 10 distinct REMOVE lines. In `go1.15.0.json`: 10/10. In `go1.16.0.json`: 10/10. In `go1.17.0.json`: 0/10.

Reading: text-identity is a weak minor discriminator (1.15 and 1.16 share the `xml.go:1988` line, `go1.16.1` case), but a 1.15.15 diff onto a 1.16.0 base shows roughly 89% REMOVE-value mismatch. The applier would still succeed silently. Implication for the port: `selection.py` as a preview does not apply patches (`patch_applied:false`), so its impact is limited to the labelled selection. Any future consumer that applies the selection must add an explicit base/target identity check. Calibration: medium (grep-based overlap; applier not executed).

### F4 — Lenient parsing would silently remap versions (proposed failure, medium)
If `selection.py` ports `GoVer.parse`, these inputs are accepted rather than rejected with exit 2:

- `1.25` → `1.25.0` (`GoVer.java:46-48, 66-75`).
- `1.25.3rc1` → `1.25.3` (suffix strip `GoVer.java:64-65`).
- `1.25.3.9` → `1.25.3` (only first three parts used, `GoVer.java:72-74`).
- `1.024.0` → `1.24.0` (`Integer.parseInt` accepts leading zeros, `GoVer.java:70-71`).

Python-specific hazards for a strict parser: `re` `\d` matches Unicode digits unless `re.ASCII`; `int()` accepts underscores and leading `+`; `$` matches before a trailing newline (use `fullmatch` or `\Z`). Required: ASCII-only canonical `^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$` with fullmatch, and filenames built from integers. Calibration: high for the Java behaviour (direct reading); the Python hazards are general knowledge, not observed here.

### F5 — Explicit user cross-minor override exists (informational)
`GoBuildInfo.fromFallbackInfo` (`Base-src.zip` 391762-391772) and the analyzer option `Fallback Go Version` (L71986-72020, L70805) let a user supply a version that the snapshot then uses when the binary's build info is absent or invalid (`GoRttiMapper.getGoBinary` L397474-397477). This is the one place a different minor can drive selection. It is user-chosen and not automatic, and `selection.py` takes `--request` explicitly, so it is outside the contract. Any future preview claiming "selected from binary" must label fallback-origin versions. Calibration: high.

### F6 — Dead minor-only filename fallback (hazard, low)
`GoApiSnapshot.java:183-192` `getApiFile` tries `go%d.%d.%d.json`, and only when patch is 0 (L187) falls back to `go%d.%d.json` (L188). No callers in `Base-src.zip`, and no `go1.M.json` names are installed, so no current effect. The contract forbids it; the port must not reproduce it. Calibration: high (grep of shipped source found no call sites).

### F7 — Log wording labels base-only as a patch fallback (informational)
`GoApiSnapshot.java:159-161` logs `Falling back from 1.25.3 to 1.25.0` for a case where no diff is applied at all, i.e. base-only. The selection preview must label base-only explicitly (contract already requires `unpatched preview`). Calibration: high.

## Residual risk and verification gaps

- No candidate `selection.py` exists; findings F2/F4 are proposed failures derived from the source contract, not observed outputs.
- Overlap counts are substring-level `grep -F` on REMOVE lines, not applier execution. They show value-mismatch magnitude, not an observed corrupt merge.
- Diff semantics (cumulative against base vs incremental) are the sibling lane `ReviewLowerDiff`'s scope; this review assumes base-relative application only because the source does so (`getApiSnapshotJsonFile` applies one diff to base).
- Not checked: whether `go1.25.0.json` internal structure matches its filename (no parsing performed).

## Tooling

No installs or updates performed by this review. No `pacman`, `uv`, `npm`, or `cargo` invoked.
