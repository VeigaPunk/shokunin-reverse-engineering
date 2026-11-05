# ExecCandidate (executor) — R91-C1 reproduction and cheap-rule controls

Lane: `kaidoku-shokunin`, round 91, attempt 1. Declaration commit `deb2765a55fef0e4e81500a027dfe59951b69e87`; base `2135f6e1d3f69a259b32cc5167c52ccb1a261c24`. Frozen counters and claims were not edited; no lane file was modified. Scratch was removed before yield.

## 1. Reproduction of the frozen counter

| arm | command (abridged) | exit | label | refused | unsafe | silent | intact | met |
|---|---|---|---|---|---|---|---|---|
| declaration | `python3 -I -B tools/round-91/stop-boundary-battery.py --root <lane> --repair-cmd tools/round-91/upx-stop-boundary-repair.py --rev deb2765… --expect "refused 8 of 8; unsafe 0; intact 4 of 4"` | 0 | refused 8 of 8; unsafe 0; intact 4 of 4 | 8 | 0 | 0 | 4 | True |
| base | same counter, `--repair-cmd tools/round-90/upx-break-repair.py --rev 2135f6e1…` | 1 | refused 0 of 8; unsafe 2; intact 4 of 4 | 0 | 2 | 6 | 4 | False |

Receipts: `.ufo/waves/round-91/w1/ExecCandidate/c1-at-declaration-repro.json`, `.ufo/waves/round-91/w1/ExecCandidate/c1-base-repro.json`.

Comparisons:
- Declaration vs the L1's `l1/scores/c1-at-declaration.json`: label, counts, met, revision, repair sha256 (`473bb3a9…`), counter sha256 (`5998b6bd…`), and all eight cell classes are identical.
- Base vs `.ufo/waves/round-91/pre/c1-base-round90-repair.json`: label, counts, and all eight cell classes are identical.
- Base per cell: `jq −7` unsafe (out-of-window `10094–10097`), `libz −7` unsafe (out-of-window `60124–60127`); the other six cells silent (rc 0).
- Declaration per cell: all eight refused (rc 2, no output); all four intact carriers identity, rc 0.

## 2. Cheap-rule controls (scratch variants, one change each)

Variants are copies of `tools/round-91/upx-stop-boundary-repair.py` inside a scratch clone at `deb2765`. Each is a single inserted line after `cls = classify(...)`, so `ROOT` resolves to the clone's round-87/88/90 modules. Sources and diffs are in `.ufo/waves/round-91/w1/ExecCandidate/variants/` (`SHA256SUMS` included).

- **blanket** (`variant-blanket.py`): `if cls is not None and len(cls[0]) >= 2: raise Refused(...)`.
- **geometry** (`variant-geometry.py`, as specified: "otherwise behave as the candidate"): `if cls is not None and cls[3] and cls[4] < cls[2]["u_len"]: raise Refused(...)`.
- **geometry-pure** (`variant-geometry-pure.py`, added by me): the geometry refusal, plus the round-90 fall-through replacing the `upx -t` branch. Added because the geometry arm as specified keeps the candidate's `upx -t` fallback, so it cannot isolate the prediction's mechanism.

Scoring command: `python3 -I -B <clone>/tools/round-91/stop-boundary-battery.py --root <clone> --repair-cmd <absolute variant path> --work <scratch> --rev deb2765… --expect "refused 8 of 8; unsafe 0; intact 4 of 4" --json-out …`

| arm | exit | label | refused | unsafe | silent | intact | met |
|---|---|---|---|---|---|---|---|
| base (round-90 repair) | 1 | refused 0 of 8; unsafe 2; intact 4 of 4 | 0 | 2 | 6 | 4 | False |
| declaration (candidate) | 0 | refused 8 of 8; unsafe 0; intact 4 of 4 | 8 | 0 | 0 | 4 | True |
| blanket | 1 | refused 8 of 8; unsafe 0; **intact 0 of 4** | 8 | 0 | 0 | 0 | False |
| geometry (as specified) | 1 | refused 8 of 8; unsafe 0; **intact 3 of 4** | 8 | 0 | 0 | 3 | False |
| geometry-pure | 1 | refused 3 of 8; unsafe 0; **intact 3 of 4** | 3 | 0 | 5 | 3 | False |

Receipts: `c1-variant-blanket.json`, `c1-variant-geometry.json`, `c1-variant-geometry-pure.json` (same directory).

Per-cell classes (carrier, delta):

| cell | base | declaration | blanket | geometry (spec) | geometry-pure | stored total vs `u_len` |
|---|---|---|---|---|---|---|
| jq −7 | unsafe | refused | refused | refused (geometry) | refused | 22585 < 30800 |
| jq +7 | silent | refused | refused | refused (upx -t) | silent | 30800 = 30800 |
| xxd −7 | silent | refused | refused | refused (upx -t) | silent | 38928 = 38928 |
| xxd +7 | silent | refused | refused | refused (upx -t) | silent | 38928 = 38928 |
| libz −7 | unsafe | refused | refused | refused (geometry) | refused | 87421 < 108560 |
| libz +7 | silent | refused | refused | refused (geometry) | refused | 98592 < 108560 |
| dinit −7 | silent | refused | refused | refused (upx -t) | silent | 851288 = 851288 |
| dinit +7 | silent | refused | refused | refused (upx -t) | silent | 851288 = 851288 |
| intact jq | identity | identity | **rc 2** | identity | identity | — |
| intact xxd | identity | identity | **rc 2** | identity | identity | — |
| intact libz | identity | identity | **rc 2** | **rc 2** | **rc 2** | not logged; refused by the geometry rule (geometry-pure has no `upx -t` fallback) |
| intact dinit | identity | identity | **rc 2** | identity | identity | — |

## 3. Disagreements with the predicted outcome

1. **Geometry arm (as specified): cell count disagrees; label verdict holds.** The prediction said geometry-only "does not refuse all eight cells". The measured arm refuses 8 of 8, because the variant keeps the candidate's `upx -t` branch for every cell the geometry rule passes (jq +7, xxd ±7, dinit ±7). It still fails the frozen label through `intact 3 of 4` (intact libz refused, as predicted). Cells: the table above, columns "geometry (spec)" and "intact libz".
2. **Geometry-pure: matches the predicted mechanism.** It refuses 3 of 8 (jq −7, libz −7, libz +7) and refuses intact libz. It fails the label (refused 3 of 8, intact 3 of 4).
3. **The predicted reason is only partly right.** The prediction says the walked total "cannot see a +7 tamper (its total still equals u_len)". True for jq +7, xxd +7, dinit +7, but: (a) libz +7 is refused by geometry (total 98592 < 108560), and (b) a −7 tamper is also invisible to the walked total on xxd (total 38928 = u_len) and dinit. So geometry sees some +7 and some −7 cells, and misses some of each. The label-level verdict (fails) is unchanged.
4. **Blanket: matches the prediction exactly** (`refused 8 of 8`, `intact 0 of 4`, fails).

## 4. Regression arm (round-90 battery; informative, not scored as a claim)

Command: `python3 -I -B tools/round-90/upx-later-block-battery.py --root <clone> --rev deb2765… --repair-cmd <repair> --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <scratch> --expect "P1 6 of 6; P2 4 of 4; P3 4 of 4" --json-out …`

| repair | exit | label | controls |
|---|---|---|---|
| candidate (`upx-stop-boundary-repair.py`) | 0 | P1 6 of 6; P2 4 of 4; P3 4 of 4 | all true (met) |
| round-90 baseline (`upx-break-repair.py`) | 0 | P1 6 of 6; P2 4 of 4; P3 4 of 4 | all true (met) |
| blanket | 1 | P1 0 of 6; P2 4 of 4; P3 4 of 4 | N3, carrier_blind, rea false |
| geometry (spec) | 1 | P1 0 of 6; P2 0 of 4; P3 4 of 4 | N3, carrier_blind, rea false |
| geometry-pure | 1 | P1 0 of 6; P2 0 of 4; P3 4 of 4 | N3, carrier_blind, rea false |

The variant control failures are downstream of the P1/P2 refusals [INFERENCE]; I did not trace them per cell. Receipts: `reg-candidate-rerun.json`, `reg-base-round90-repair.json`, `reg-variant-blanket.json`, `reg-variant-geometry.json`, `reg-variant-geometry-pure.json`.

## 5. Deviations and host notes

- **REA package path.** The counter's default `--pkg ~/.local/share/rea-agents/6.5.0` does not exist on this host; the default run returns `unevaluable: rea_pin` (exit 2). `~/.local/share/rea/package.json` is rea-agents 6.7.0, sha `910651a4…`, not the pin. I used `--pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`: rea-agents 6.5.0, package.json sha `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, equal to the pin (`REA_PKGJSON_SHA256`). This is the same path the L1's regression receipt recorded as `rea_pkg`. The counter was not edited.
- **Invocation error, corrected.** My first candidate regression run passed a relative `--repair-cmd` and returned `unevaluable: missing_repair` (exit 2). The rerun uses the absolute path; that receipt is `reg-candidate-rerun.json`.
- **Base run repair path.** The base battery run uses `--root <lane>` at HEAD `fe1913d90`. `git diff --stat deb2765… HEAD -- tools/round-87 … round-91` is empty, so the instrument bytes equal those at declaration.

## 6. Tools installed or upgraded

None. No pacman; no package installs.

## 7. Files written

Seat directory `.ufo/waves/round-91/w1/ExecCandidate/`:
- `c1-at-declaration-repro.json`, `c1-base-repro.json`
- `c1-variant-blanket.json`, `c1-variant-geometry.json`, `c1-variant-geometry-pure.json`
- `reg-candidate-rerun.json`, `reg-base-round90-repair.json`, `reg-variant-blanket.json`, `reg-variant-geometry.json`, `reg-variant-geometry-pure.json`
- `variants/variant-blanket.py`, `variants/variant-geometry.py`, `variants/variant-geometry-pure.py`, `variants/*.diff`, `variants/SHA256SUMS`
- this report: `.ufo/waves/round-91/w1/ExecCandidate.md`

Scratch `/fast/scratch/hyaku/kaidoku-r91/ExecCandidate` removed.

## 8. Checks for the main agent

- Reproduction (exit 0 at declaration, exit 1 at base) and the candidate regression arm (exit 0) are the frozen checks. The main agent should re-run them against its own receipts; I only reproduced.
- The variant results are not claim evidence: the frozen label fails for all three, which is the kill condition for the cheap-rule controls.
