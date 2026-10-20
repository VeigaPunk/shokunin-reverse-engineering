# Round-19 SKILL registry rows — wave-2 review

**Axes:** calibration, freshness, depth.

**Scope / evidence point.** Reviewed the seven new rows `routed-r18` through `round19-verify` at `SKILL.md:594-600` against the observed main tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`). The scope is the new registry rows and their direct command contracts; no production edits. LSP is unavailable in the mounted tools (`read xd://lsp` returned “No such tool”), so no references/definition/diagnostics result is claimed. I read the exact source and exercised commands; grep was only used to locate parser declarations, not as semantic proof.

## Findings

### High — the documented carrier timeout envelope is not a bound

**Observation.** The new `go-carrier-run-r19` row says `TIMEOUT_S` is a per-step timeout (`SKILL.md:598`). The underlying driver states `TIMEOUT_S=1200` per step, then claims “a 9-row wave cannot stall longer than 3 h” (`.ufo/waves/round-19/run-carriers.sh:22-32`). It invokes `carrier-run.py` with `--timeout 1200` but no `--search` argument (`run-carriers.sh:317-321`). The called runner executes `inspect-go-binary` and then `analyze`; only explicit repeatable `--search` arguments add more timed steps (`.ufo/waves/round-17/tools/carrier-run.py:352-390,731-750`). The current TSV has 8 labels (`.ufo/waves/round-19/predictions/carriers.tsv:1-8`).

**Inference.** Two separate 1200-second REA steps per label allow nearly 40 minutes per label; nine labels permit about 6 hours of capped REA-step waits (the present eight-label set about 5 h 20 min), before non-REA overhead. The “cannot stall longer than 3 h” statement is therefore not supported by the configured per-step timeout. The registry correctly calls it per-step, but the adjacent saturation assurance is materially too strong.

### Medium — the advertised `SHA256SUMS` is not the carrier-run integrity oracle

**Observation.** `SKILL.md:598` lists both `predictions/carriers.tsv` and `predictions/SHA256SUMS` as pinned values. The driver itself says the TSV sha256 column is the only carrier-integrity source and that no `SHA256SUMS` store is read (`run-carriers.sh:7-10`). Its preflight and hash comparison use the TSV column (`run-carriers.sh:232-251,284-289`); no runtime check consults the manifest.

**Inference.** The registry overstates the runner’s enforced pin set. An operator could reasonably expect a mismatch against `SHA256SUMS` to refuse the run, but the runner does not compare against it. Scope the registry’s runner-pin claim to the TSV column, or separately describe the manifest as evidence not consumed by this command.

### Medium — an unknown carrier label is a silent successful no-op

**Observation.** The script treats the first argument as a label selector and skips every nonmatching TSV row, then exits `overall` (initially 0) (`run-carriers.sh:262-267,331-334`). In the isolated clone, `bash .../run-carriers.sh no-such-label` returned **0 with no output**. `bash .../run-carriers.sh --help` also returned **0 with no output**: there is no help branch; `--help` is treated as a label. The row documents `[LABEL]` but not this behavior (`SKILL.md:598`).

**Inference.** A typo or help request can look green without running a carrier or comparison. The row’s “0 every run and compare exited 0” map is vacuously satisfied when zero rows match. This weakens the observable success contract; document/refuse an unknown selector rather than treating it as a clean run.

### Medium — write-scope entries omit replacement/deletion behavior

**Observation.** The runner validates its output location, then does `rm -rf "$outabs"; mkdir -p "$outabs"` before writing run records (`run-carriers.sh:268-276`). Thus a normal repeat at `W19/runs/<label>` deletes the previous label directory, not just appends new outputs. The row names that directory but does not say it is replaced (`SKILL.md:598`). Also, `wave-outcomes.py` creates parent directories, writes a temporary sibling and `os.replace`s the requested `--out`; its docstring explicitly says it may overwrite (`wave-outcomes.py:34-47,356-373`). `rea-catalog.py --out` similarly creates parents and atomically replaces the target (`rea-catalog.py:253-263`), while the rows say “`--out` only” / “stdout or `--out` only” (`SKILL.md:596-597`).

**Inference.** The registry names the broad destinations but does not expose whether existing evidence is discarded/replaced, nor the temp-file/parent-directory effects. The runner’s default output is especially destructive. State that the selected label directory is removed/recreated; qualify the `--out` entries as atomic replacement that can overwrite an existing file.

### Low — exit maps and selftest limits are incomplete in three rows

**Observation.** `round19-measure` only promises JSON with C1/C2/C3 fields (`SKILL.md:599`), but its actual contract is exit 0 after emitting a report even when a claim is unevaluable, and exit 2 only when revision/tree resolution fails (`measure.py:32-45,1319-1347`). `round19-verify` lists only 0/1 (`SKILL.md:600`), but usage errors and preflight refusals (unresolvable baseline, missing branch/source pin, etc.) return 2 (`verify.py:399-452,760-767`). Its `--selftest` is only a two-command runner-mechanics fixture, not the full verification pass (`verify.py:36-42,265-328`). `rea-catalog` likewise has no row exit map (`SKILL.md:596`): without `--strict`, findings still exit 0; `--strict` makes findings exit 1; refusal is 2 (`rea-catalog.py:24-25,214-263`).

**Inference.** Registry users cannot distinguish “reported but unevaluable” from a clean pass for `measure`, or unusable/preflight refusal from a verification failure for `verify`; the `verify` selftest also does not prove the expected-exit table against the full plan. Add these bounded exit and selftest limitations to the rows. `verify.py --help` was observed to print only its usage and exit 2; it does not implement an argparse help option.

## Observations that checked out

- `routed-r18` constants and status map matched direct checks: at baseline `--strict`, 7 open / exit 1; at observed tip `--strict`, 0 open / exit 0. Its `--selftest` says token-only evidence leaves the seven substantive defects open; it passed 13 cases.
- `province-pins` flags/strict behavior and the row’s time-dependence were consistent. At the observed tip, strict comparison reported mismatch_count 0 / exit 0; all three live configs reported `rea-agents@6.7.0`. This is a point-in-time reading, not continuity.
- `rea-catalog` evidence matched the observed cache probe: both versions report 153 CLI commands / 207 MCP tools; 6.7.0 hash `af39310c…` and 6.5.0 hash `805433f1…` are distinct identities. The carrier runner itself pins `REA_VERSION=6.5.0` and passes it explicitly (`run-carriers.sh:17-20,53,317-321`; `carrier-run.py:352`), consistent with the round-19 contract (`contract.md:35-38`). The catalog’s two-version inventory is not evidence that these are the same runtime or a runtime reroute.
- `measure.py` does remove the temporary materialization after tool evaluation (`measure.py:664-672`); the row’s removed-`mkdtemp` write claim is accurate.

## Commands and verification

Observed source tip command: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main` → `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (exit 0). A no-hardlinks clone was made under `/tmp/kr19-w2-SkillRegistryNew.b8MhkM`, detached at that observed tip for the mutation/selftest commands below, then removed. No install, build, broad suite, carrier execution, Ghidra run, or full `verify.py BASELINE_REV` pass was performed.

Seven help probes:

```text
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/routed-r18.py --help -> exit 0; flags: --root, --rev, --strict, --selftest
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/province-pins.py --help -> exit 0; flags: --root, --rev, --strict, --selftest
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/rea-catalog.py --help -> exit 0; flags: --npx-root, repeatable --version, --out, --strict, --selftest
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/wave-outcomes.py --help -> exit 0; flags: --registration, --report-dir, --causes, --out, --selftest
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/measure.py --help -> exit 0; positional revision, --root, --selftest
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/verify.py --help -> exit 2; usage only, no help
bash /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/run-carriers.sh --help -> exit 0; no output, treated as selector
```
The first six help probes used the lane files; the runner help probe used the isolated clone.

Seven targeted selftests, all in the isolated clone at the observed tip, passed:

```text
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/routed-r18.py --selftest       -> SELFTEST: CLEAN cases=13; exit 0
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/province-pins.py --selftest    -> SELFTEST: CLEAN cases=35; exit 0
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/rea-catalog.py --selftest       -> SELFTEST: CLEAN cases=7; exit 0
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/wave-outcomes.py --selftest    -> SELFTEST: CLEAN cases=33; exit 0
bash /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/run-carriers.sh --selftest                         -> SELFTEST: CLEAN cases=26; exit 0
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/measure.py --selftest                  -> SELFTEST: CLEAN cases=118; exit 0
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/verify.py --selftest                   -> SELFTEST: CLEAN cases=2; exit 0
```
Additional read-only behavior probes in the isolated clone:

```text
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-SkillRegistryNew.b8MhkM --rev 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --strict -> exit 1 / open_count 7
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-SkillRegistryNew.b8MhkM --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict -> exit 0 / open_count 0
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/province-pins.py --root /tmp/kr19-w2-SkillRegistryNew.b8MhkM --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict -> exit 0 / mismatch_count 0
python3 -I -B /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/tools/rea-catalog.py --npx-root /home/vgpnk/.npm/_npx --version 6.7.0 --version 6.5.0 -> exit 0; matched retained catalog values
bash /tmp/kr19-w2-SkillRegistryNew.b8MhkM/.ufo/waves/round-19/run-carriers.sh no-such-label -> exit 0; no output
```

**Residual risk / verification gaps.** Targeted selftests are local fixture checks; the carrier runner selftest uses stubs and does not validate a live REA/Ghidra run. I intentionally did not run the normal carrier driver or full verifier because they write round evidence and/or invoke the REA pipeline. The runner’s delete/recreate behavior and the source-level per-step calculations are observed; no actual long-duration saturation run was performed.