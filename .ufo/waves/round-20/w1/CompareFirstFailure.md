# Compare first failure (C3)

Axes: calibration / coverage / depth; this assignment targets depth (C3). **Observed:** the binding contract defines C3's H1 comparison and exit codes at `.ufo/waves/round-20/contract.md:76-81`; its Python/selftest convention is at `:28-32`.

## Implementation

- Added `.ufo/waves/round-20/tools/compare-first-failure.py`: validates the direct `first_failure.h1` object and extractor result, executes the caller-provided `--extractor` as `python3 -I -B EXTRACTOR LOG`, emits both objects and match/error JSON, and returns 0 match / 1 mismatch / 2 unevaluable (`:12-35`, `:37-94`, `:155-173`). Equality is exactly both null or equal `kind` and `index`; `va`/`phase` are retained but not compared.
- Added `.ufo/waves/round-20/tools/retro-v2.py`: scans `<label>.json` files, pairs each with the unique `ghidra.log` below the corresponding round-19 pass2 label directory, reuses the comparator, and emits the four-column CSV (`:35-121`, `:123-142`, `:211-258`). Missing/ambiguous logs or unusable records are marked `unevaluable`; exit is 2 for unevaluable rows, else 1 for mismatches, else 0.
- Both files include tempfile-backed `--selftest` cases (`compare-first-failure.py:97-153`; `retro-v2.py:145-209`). **Not run:** the wave executor rule says to skip all tests while this editing wave is in flight; therefore no selftest last-line/exit code or stub-retro table exists. Parent owns the post-integration gate. LSP is unavailable in the supplied tool inventory; no LSP operation was available.

## Retained evidence and limits

- **Observed:** round-19 generation freezes `c3.h1_kind` and aggregate `extra_expectations` rather than a `first_failure.h1` object (`.ufo/waves/round-19/gen-predictions.py:66-90`); the frozen vet example predicts `invalid_index` and lists indices (`.ufo/waves/round-19/predictions/t1250-vet.prediction.json:27-31,45-52`). The retained pass2 vet log contains `Invalid index: 13902080` at `.ufo/waves/round-19/runs/pass2/t1250-vet/logs/rea-ghidra-PEkTou/ghidra.log:229` (also consistent with that frozen list).
- **Inference:** adapting the older forecast fields to first-failure-shaped stub JSON can exercise only plumbing, not establish v2 calibration; no stub was built/run here because of the test ban. Extractor integration assumes its CLI prints one JSON object or `null` to stdout, as implied by `.ufo/waves/round-20/contract.md:79-81`; the extractor implementation was not part of this assignment.
- **Risk/blocker:** comparator and retrospective execution remain unverified until the parent runs the mandated post-integration checks, including the requested selftest and stub retro run. No tools were installed/updated.

## Patch and commands

Patch: `.ufo/waves/round-20/w1/patches/CompareFirstFailure-2.patch`. Clone base observed: `14f0260ad319ecc26994381b2415d5a999003375`. `git diff --cached --stat 14f0260` (exit 0):

```
.ufo/waves/round-20/tools/compare-first-failure.py | 173 ++++++++++++++
.ufo/waves/round-20/tools/retro-v2.py              | 258 +++++++++++++++++++++
2 files changed, 431 insertions(+)
```

Commands run (each exited 0):

```
test ! -e /tmp/kr20-CompareFirstFailure-2
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-CompareFirstFailure-2
git -C /tmp/kr20-CompareFirstFailure-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375
git -C /tmp/kr20-CompareFirstFailure-2 rev-parse HEAD
mkdir -p /tmp/kr20-CompareFirstFailure-2/.ufo/waves/round-20/tools
test ! -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/CompareFirstFailure-2.patch && test ! -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/CompareFirstFailure.md
mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches
git -C /tmp/kr20-CompareFirstFailure-2 add -A
git -C /tmp/kr20-CompareFirstFailure-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/CompareFirstFailure-2.patch
git -C /tmp/kr20-CompareFirstFailure-2 diff --cached --stat 14f0260
```

No Python/test/build/lint/formatter command was run.
