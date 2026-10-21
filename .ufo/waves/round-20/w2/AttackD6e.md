FALSIFIED — R19-D6e holds for scalar `causes` entries and the ordinary wrapped shape, but a valid flat object-form cause for seat `causes` is still mistaken for the wrapper when a `wave` seat is present; flat `seats` is also mistaken for a wrapper.

## Evidence (measured source S)

**Observed source.** Used `git show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-19/tools/wave-outcomes.py` (exit 0); blob `2890de84322d5c901b8ed2c134ae8adba078c52c`, SHA-256 `f925083c4f42c599bdf76f5c2b22402f03feb6f58c64d2c3c254dfcde466b6c8`. All probes ran this extracted file, not the working-tree copy. `load_causes` chooses a wrapper if `doc["causes"]` is a dict and any `wave` key exists (`:237-240`); otherwise any top-level `seats` selects the list wrapper (`:245-251`). Object causes are accepted (`:179-203`), and the chosen mapping is resolved into per-seat counts (`:254-290`, `:310-354`). The lesson's D6e statement is at `corpus/lessons/round-20.md:83`.

**Commands and observed results.** Source extraction: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-19/tools/wave-outcomes.py > /tmp/attack-d6e.tixqvk/wave-outcomes.py` → exit 0. For each invocation below, the shell captured the Python status with `rc=$?; printf 'SCRIPT_EXIT=%s\n' "$rc"; exit 0`.

```sh
python3 -I -B /tmp/attack-d6e.tixqvk/wave-outcomes.py --registration /tmp/attack-d6e.tixqvk/probes/flat-causes/registration.json --report-dir /tmp/attack-d6e.tixqvk/probes/flat-causes/reports --causes /tmp/attack-d6e.tixqvk/probes/flat-causes/causes.json --out /tmp/attack-d6e.tixqvk/probes/flat-causes/out.json
```
→ `SCRIPT_EXIT=0`; seats=1, causes_recorded=1, uncaused=0.

```sh
python3 -I -B /tmp/attack-d6e.tixqvk/wave-outcomes.py --registration /tmp/attack-d6e.tixqvk/probes/flat-wave/registration.json --report-dir /tmp/attack-d6e.tixqvk/probes/flat-wave/reports --causes /tmp/attack-d6e.tixqvk/probes/flat-wave/causes.json --out /tmp/attack-d6e.tixqvk/probes/flat-wave/out.json
```
→ `SCRIPT_EXIT=0`; seats=1, causes_recorded=1, uncaused=0.

```sh
python3 -I -B /tmp/attack-d6e.tixqvk/wave-outcomes.py --registration /tmp/attack-d6e.tixqvk/probes/flat-seats/registration.json --report-dir /tmp/attack-d6e.tixqvk/probes/flat-seats/reports --causes /tmp/attack-d6e.tixqvk/probes/flat-seats/causes.json --out /tmp/attack-d6e.tixqvk/probes/flat-seats/out.json
```
→ `SCRIPT_EXIT=2`; `REFUSED causes_invalid ... 'seats' is str, expected a list of rows`.

```sh
python3 -I -B /tmp/attack-d6e.tixqvk/wave-outcomes.py --registration /tmp/attack-d6e.tixqvk/probes/flat-all-reserved/registration.json --report-dir /tmp/attack-d6e.tixqvk/probes/flat-all-reserved/reports --causes /tmp/attack-d6e.tixqvk/probes/flat-all-reserved/causes.json --out /tmp/attack-d6e.tixqvk/probes/flat-all-reserved/out.json
```
→ `SCRIPT_EXIT=2`; same refusal for `seats`.

```sh
python3 -I -B /tmp/attack-d6e.tixqvk/wave-outcomes.py --registration /tmp/attack-d6e.tixqvk/probes/flat-causes-object-plus-wave/registration.json --report-dir /tmp/attack-d6e.tixqvk/probes/flat-causes-object-plus-wave/reports --causes /tmp/attack-d6e.tixqvk/probes/flat-causes-object-plus-wave/causes.json --out /tmp/attack-d6e.tixqvk/probes/flat-causes-object-plus-wave/out.json
```
→ `SCRIPT_EXIT=1`; seats=3, causes_recorded=1, uncaused=2. The input flat map is `{"causes":{"cause":"intended-for-causes"},"cause":"intended-for-cause","wave":"intended-for-wave"}`. `/tmp/attack-d6e.tixqvk/probes/flat-causes-object-plus-wave/out.json:9,15-50` shows `wave: "intended-for-wave"` and the cause intended for `causes` assigned to seat `cause`, while seats `causes` and `wave` have null causes.

```sh
python3 -I -B /tmp/attack-d6e.tixqvk/wave-outcomes.py --registration /tmp/attack-d6e.tixqvk/probes/wrapped-causes/registration.json --report-dir /tmp/attack-d6e.tixqvk/probes/wrapped-causes/reports --causes /tmp/attack-d6e.tixqvk/probes/wrapped-causes/causes.json --out /tmp/attack-d6e.tixqvk/probes/wrapped-causes/out.json
```
→ `SCRIPT_EXIT=0`; input `{"wave":"w2","causes":{"causes":"cause-for-causes"}}` yields seats=1, causes_recorded=1, uncaused=0, wave=`w2` (`/tmp/attack-d6e.tixqvk/probes/wrapped-causes/out.json:9,15-33`).

Fixture registration files contain the named member(s) with role `test`; report directories are empty.

## Assessment

**Observed:** Scalar flat maps for seats `causes` and `wave`, and a wrapper containing seat `causes`, are counted correctly in these probes. The valid flat map with an object cause plus a registered `wave` seat is misclassified: wrapper detection discards the outer entries and attributes the inner `cause` field to the registered seat `cause`. The flat `seats` form is refused rather than counted.

**Inference:** The wrapper detector relies on key/type shape alone and does not disambiguate wrapper keys against registered seat names. Therefore the specific D6e property is incomplete for object-form causes, in addition to the adjacent `seats` collision.

**Caller trace / limitation:** In this exact source, `main` calls `evaluate` (`:851`), which calls `load_causes` (`:310-311`); S's `verify.py:83` includes `wave-outcomes.py` in `REQUIRED_TOOLS`. The `lsp` device was unavailable (`xd://lsp` returned `No such tool`); literal grep located names only, not semantic proof. No installs were performed.