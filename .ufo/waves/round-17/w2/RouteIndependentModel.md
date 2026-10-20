# RouteIndependentModel — independent route reimplementation vs predict.py (wave 2 falsify)

Scope: reimplement `GoApiSnapshot.getApiSnapshotJsonFile` /
`getPatchVerDiffFile` route logic from
`Base-src.zip:ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:118-166`
without importing r16 `selection.py` or r17 `predict.py`; sweep all
`1.m.p` for m in 13..28, p in 0..20 over the installed dir; diff against
`predict.py` `expected.snapshot_route`/`expected.fallback_to`; attack
predict.py's route model.

## Verdict

**Bounded no-finding on the central claim.** 336/336 versions agree on
(route, fallback_to); the internal countdown↔listing cross-check inside
my own model agrees everywhere; all 7 retained real-Ghidra ground-truth
log lines match predict's route fields; 7/7 synthetic fixture roots and
8/8 version-string edge cases also agree. Below: the residuals found —
one citation imprecision and two genuine model-fidelity divergences
outside the sweep grid.

## Artifacts

- `.ufo/waves/round-17/w2/route-model.py` — independent model + sweep
  runner. `--selftest` = CLEAN cases=10 (all four route classes plus
  directory-decoy, non-canonical-name, missing-base cases).
- `.ufo/waves/round-17/w2/route-diff.json` — full 336-row comparison,
  sha256 `f2305ca9d64d316b4d33dfdf0a5e7b2fd08c17cfd06adb8834aa44e8c30d602e`.

Run: `python3 -I -B route-model.py --out route-diff.json` (2.8 s,
16 predict subprocesses in a ThreadPoolExecutor).

## Model (observation, anchors verified this session)

- `GoApiSnapshot.java:122-123` — base is always `goVer.withPatch(0)`
  → `go<M.m.0>.json`; `:124-126` null → EMPTY, **before** the diff
  search. Route `none`.
- `:153-156` — literal while-loop probes `patchverdiffs/go<M.m.p>.json.diff`
  for p = req, req−1, … until found or p==0 (`GoVer.prevPatch`,
  `GoVer.java:127-131` clamps at 0).
- `:157-165` — `patchVer.patch != goVer.patch` → WARN "Falling back from
  <req> to <patchVer>" (route `fallback`, `fallback_to =
  patchVer.toString()`); else INFO "Using Go API snapshot for <req>"
  (route `info`). Note: WARN also fires when `patchDiffFile` ends null —
  `go1.25.7` logs `Falling back from 1.25.7 to 1.25.0`, confirmed live.
- `Application.java:354-374` — `getDataFileInModule` throws
  `FileNotFoundException` when the path is absent **or a directory**;
  `getApiSnapshotFile` (`:168-177`) catches → null. Presence = "regular
  file exists". `getModuleDataFile(relative)` is scoped to the caller's
  module (Base) — `find` over the install tree confirms a single
  `typeinfo/golang` root.

## Sweep result

```
minor 13,14,26,27,28: nnnnnnnnnnnnnnnnnnnnn   (no base → none)
15: iiiiiiiiiiiiiiiifffff   (diffs 1..15; p16..20 fallback→1.15.15)
16: iiiiiiiiiiiiiiiifffff   (diffs 1..15)
17: iiiiiiiiiiiiiifffffff   (diffs 1..13)
18: iiiiiiiiiiiffffffffff   (diffs 1..10)
19: iiiiiiiiiiiiiifffffff   (diffs 1..13)
20: iiiiiiiiiiiiiiiffffff   (diffs 1..14)
21: iiiiiiiiiiiiiifffffff   (diffs 1..13)
22: iiiiiiiiiiiiiffffffff   (diffs 1..12)
23: iiiiiiiiiiiiffffffff    (diffs 1..11)
24: iiiiiiiffffffffffffff   (diffs 1..6)
25: iffffffffffffffffffff   (base only; p1..20 fallback→1.25.0)
```

`agree: 336 / disagree: 0`. Route counts: info 134, fallback 97, none 105.

## Ground-truth anchor (observation — retained runs/)

| retained line | predict fields | match |
|---|---|---|
| `runs/calib-esbuild-0.25.12/logs/rea-ghidra-NnYFT2/ghidra.log` INFO `Using Go API snapshot for 1.23.12` | info / null | ✓ |
| `runs/pro-esbuild-0.21.5/logs/rea-ghidra-kS1Ie7/ghidra.log` INFO `... for 1.20.12` | info / null | ✓ |
| `runs/pro-notesmd-cli/logs/rea-ghidra-eK7Drd/ghidra.log` WARN `Falling back from 1.25.8 to 1.25.0` | fallback / `1.25.0` | ✓ |
| `runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log` WARN `Falling back from 1.25.14 to 1.25.0` | fallback / `1.25.0` | ✓ |
| `runs/calib-shfmt/logs/rea-ghidra-kc2RG0/ghidra.log`: no GoApiSnapshot line; GoRttiMapper `Untested [1.27.0]` + `Missing Go bootstrap` | none / null, missing_bootstrap true | ✓ |
| `runs/pro-containerd-shim/.../ghidra.log` same for 1.27.2 | none / null | ✓ |
| `runs/pro-op/.../ghidra.log` same for 1.26.8 | none / null | ✓ |

`runs/pro-esbuild-0.27.7` is untestable for route: its `inspect-go.json`
has `build_info: null` (no version; predict exits 2 on empty input —
consistent with the route being unreachable, not a defect).

## Fixture attacks (7/7 agree)

Under `/tmp/routefix`: diff-gap both directions (`diffs {2,7}`: req 5→`fallback 1.9.2`, req 1→`fallback 1.9.0` — **diffs above the request are ignored**, the sharpest direction risk), decoy directory named `go1.9.7.json.diff` (skipped → `1.9.3`), valid + dangling symlinks, base-as-directory → `none`. All agree with predict via selection.py.

## Version-parse edge cases (8/8 agree)

`go1.24`→patch 0; `go1.24.07`→1.24.7 → `fallback 1.24.6` (Java `parseInt`
accepts leading zeros, probes the canonical name); `go1.24.6X`→exact
1.24.6; `go1.25.99`→`fallback 1.25.0`; `go1.24.-1`→1.24.0 info;
`go1.24.2147483648`→exit 2 (int overflow); `go0.0.5`→exit 2 (INVALID
sentinel); `go1.24.`→1.24.0.

## Residuals (real but outside the sweep's discriminating surface)

1. **Citation imprecision** — `predict.py:185` BASIS cites
   `GoApiSnapshot.java:111` for "getVer is requested goVer"; `getVer()`
   is defined at `GoApiSnapshot.java:499`. The claim is true, but the
   operative anchor is `:111` (the `read(is, archSearchOrder, goVer)`
   call site) — correct line, wrong symbol name. Cosmetic; worth a
   one-word basis fix, not a behavioral defect.
2. **Unparseable/corrupt base divergence** — a present-but-bad-JSON
   `go<M.m.0>.json` makes `selection.py:_top_level_keys` raise → predict
   exits 2 with no route. Ghidra's route *decision* is file-presence
   only: it would still emit INFO/WARN and only fail later in
   `read()`/`JsonPatch` (propagated `IOException` → analyzer error).
   predict.py cannot emit a route for a case Ghidra does route. Latent;
   unreachable on the installed data set (all 11 bases parse).
3. **O(request_patch) probing unmodelled** — `go1.24.2147483647`
   (max int, parseable) makes Java's while-loop issue ~2×10⁹ filesystem
   probes: effectively a hang, i.e. an upstream DoS-shaped edge.
   predict.py answers `fallback 1.24.6` instantly — the *decision* is
   right, the timing side is invisible to the model. Inference flagged:
   Java loop bound is plain from `GoApiSnapshot.java:153-156`; probe
   cost is an assumption.

## Also checked, no divergence

- `snapshot_label` echoes the *request* under fallback — confirmed by
  the 1.25.x WARN followed by INFO `version 1.25.14` in
  `pro-aether/.../ghidra.log:93`; predict's docstring marks it
  NON-DISCRIMINATING, and the separate `fallback_to` field carries the
  discriminating signal. No defect.
- Only the caller's module is searched (`Application.getModuleDataFile`,
  Application.java:954-963 → `getDataFileInModule`), so `--golang-root`
  as the single lookup dir is faithful. `find` over
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` shows exactly one
  `typeinfo/golang` root.
- My listing-vs-countdown cross-check initially "disagreed" on
  `go1.3.04.json.diff` (leading zero): it matched my `\d+` regex but can
  never match Java's literal formatted-name probe — and r16
  `_DIFF_NAME_RE` correctly rejects it too. Both the Java loop and
  predict are immune to non-canonical diff names.
- Contract & route shape: `none` (no log line), `info` (INFO),
  `fallback` (WARN) corresponds 1:1 with observed `Msg` calls; the
  WARN-fires-with-null-diff corner (fallback→patch 0) is correctly
  `fallback`/`M.m.0` in predict (`predict.py:211-219`).

## Commands

```
python3 -I -B .ufo/waves/round-17/w2/route-model.py --selftest   # CLEAN cases=10
python3 -I -B .ufo/waves/round-17/w2/route-model.py --out .ufo/waves/round-17/w2/route-diff.json  # 336 agree
python3 -I -B .ufo/waves/round-17/tools/predict.py --go-version go1.25.14 \
  --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
# → snapshot_route "fallback", fallback_to "1.25.0"  (== retained WARN)
```

No installs. No files outside `.ufo/waves/round-17/w2/` touched;
fixtures lived under `/tmp/routefix` (removed-able scratch).
