# routed-r18.py — scoped review

## Scope and observed version

**Observation.** At review time `refs/heads/main` was `279e8b19c51658bfd05b9e31a1c0894ab2e70537`. The target also had an uncommitted worktree modification (`M`, 86 insertions / 27 deletions relative to that tip). Findings below distinguish the current worktree variant from behavior in the committed tip; no production files were edited. Mutation tests ran only in private clones detached at the observed tip, with the current worktree script copied into those clones where noted.

Axes checked: Git-object vs live-ref scoping; execution/import isolation; temporary-directory cleanup and location; false-red/false-green test oracles.

## Findings (severity order)

### High — code loaded from REV can rewrite the counter and forge an all-green result

**Observation.** `load_module()` executes the supplied module in the caller's interpreter (`.ufo/waves/round-19/tools/routed-r18.py:84-92`). The MIDMAP check imports `REV`'s `receipt-validate.py` and `pins.py` (`:97-104`); the validator-digest check separately imports `REV`'s `routed-defects.py` (`:129-138`). `evaluate()` subsequently dispatches every check through the shared module-level `SUBSTANCE` mapping (`:352-376`). Thus the object under evaluation executes with write access to the evaluator's Python state, not merely as an isolated subject.

**Observed mutation.** In a private clone at the observed tip, I copied the current worktree version of `routed-r18.py`, committed a test `receipt-validate.py` whose import-time code replaced `__main__.SUBSTANCE` entries with `(True, "poisoned at REV import")`, and whose `validate_receipt()` satisfied the MIDMAP fixtures. At test revision `b07c22e0a98d1569ba606e7220bb9aa0fe0c4380`, this command:

```sh
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py \
  --root "$PWD" --rev b07c22e0a98d1569ba606e7220bb9aa0fe0c4380 --strict
```

returned **exit 0**, `open_count=0`, `substance_open=0`; six check explanations literally said `poisoned at REV import`. The mutation changed only the validator blob at the evaluated revision, not the named corrections. This is a demonstrated false-clean: the checker imports the revision's code and that code can replace the checker that decides its result.

**Inference.** The same-process `measure.py` caller materializes and imports revision tools (`.ufo/waves/round-19/measure.py:24-26, 272-289`), so a malicious revision module can also affect that caller's interpreter; the direct-CLI mutation above is the exercised reproduction. Isolate revision code from the evaluator (or otherwise make its result unable to mutate the evaluator) before treating this as an integrity check.

### Medium — a full-hash measurement still depends on the live `refs/heads/main`

**Observation.** The tool's contract says the live checks read Git objects of REV plus the fixed A18 revision (`routed-r18.py:14-16`). But `s_head_aliases()` invokes the extracted probe with `--rev refs/heads/main` (`:241-265`), which resolves that ref in the current root rather than the requested full-hash `rev`.

**Observed mutation.** In a private clone, using the current worktree script and the same requested revision `279e8b19c51658bfd05b9e31a1c0894ab2e70537`:

```sh
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py \
  --root "$PWD" --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
```

returned **exit 0**, `open_count=0` while `refs/heads/main` existed. Then, in that clone only, `git update-ref -d refs/heads/main` succeeded; rerunning the identical counter command for the same full hash returned **exit 1**, `open_count=1`, with `R18-HEAD-ALIASES` false and `refs/heads/main also refused (always-red)`. Other checks still evaluated the explicit commit. This makes the result depend on a mutable live ref, contrary to the stated revision-only input scope.

**Inference.** A missing or invalid local branch can create an apparent open defect at an otherwise identical immutable REV. The positive control should be tested against an isolated/pinned branch or otherwise made independent of the caller's live ref state.

### Low — temporary directories are hard-coded to the documented exhausted path

**Observation.** `evaluate()` allocates each check directory with `tempfile.mkdtemp(..., dir="/tmp")` before entering its `try/finally` (`routed-r18.py:371-380`); `selftest()` does the same (`:388-452`). The repository's host scratch guidance says “never `/tmp`” and records it as quota-exhausted with `EDQUOT` (`.ufo/gates/custody-pair/README.md:45-47`).

**Inference.** If that documented quota condition is encountered, `mkdtemp()` raises before the cleanup/error-handling block and the command emits no normal JSON or documented exit classification. The successful runs below left no `kr19-routed-*`/`kr19-routed-selftest-*` residue, so cleanup after successful allocation was observed to work; the issue is the forced scratch location and uncaught allocation failure, not a demonstrated cleanup leak.

### Low — the declared fixed-input scope omits another pinned commit

**Observation.** The module docstring names only A18 as the fixed extra revision (`routed-r18.py:14-16`). The current `s_deadseat()` also reads `.ufo/waves/round-19/w1/DeadSeatHistoryR18.md` from the separate hard-coded commit `4f6c73f81ae8d31de18377d7ff57e4e10140ce48` (`:292-303`). This is an immutable Git-object input, not a working-tree read, but it is omitted from the declared measurement inputs.

**Inference.** The scope description and any measurement provenance based on it are incomplete until this additional evidence revision is named. This is a disclosure/calibration issue; the pin itself is not mutable.

## Verified behavior / issues not retained against the current worktree variant

- `python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --selftest` → **exit 0**, `SELFTEST: CLEAN cases=13`.
- Against B `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`, current worktree tool with `--root . --strict` → **exit 1**, `open_count=7`, `substance_open=7`.
- Against tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537`, current worktree tool with `--root . --strict` → **exit 0**, `open_count=0`, `substance_open=0`.
- The current worktree variant canonicalizes `root` (`:49-55`), scrubs Git/JJ environment variables (`:44-46`), pins the strict-baseline producer to A18 before reading its tool blob (`:210-218`), and refuses aliases including `ORIG_HEAD` (`:473-479`). `--rev ORIG_HEAD` returned **exit 2**. These changes address the relative-root false red, empty-`tool_rev` index fallback, inherited Git environment, and pseudo-ref acceptance present in the earlier committed version; those are not reported as current-worktree findings. The committed tip remains older than this uncommitted worktree variant.
- The current `--root .` run at the tip passed, and normal `finally` cleanup was observed: `ls -d /tmp/kr19-routed-* /tmp/kr19-routed-selftest-* 2>/dev/null` produced no matches (**ls exit 2**, no residue).
- `s_head_aliases()` treats any subprocess **exit 2** as alias refusal (`:251-260`) rather than checking for the specific `rev_moving_state` finding. The live-ref positive control catches a globally unusable probe, but the oracle can still conflate other per-alias could-not-evaluate causes with policy refusal. No current false-clean from this path was demonstrated; retain as residual test-oracle risk.

## Verification gaps

- No LSP device/server was available in the mounted tool inventory; therefore no LSP status, references, definition, or diagnostics results are claimed. Source anchors are from `read` snapshots; grep was used only for literal line-location checks.
- No build, broad suite, linter, formatter, or REA/Ghidra runtime was run. Mutation tests were confined to private clones, then those clones and scratch artifacts were removed.
- The direct poison test was exercised against the current worktree tool. The `measure.py` propagation is labelled inference, not an observed harness result.

Report: .ufo/waves/round-19/w2/ToolCounterScope.md
