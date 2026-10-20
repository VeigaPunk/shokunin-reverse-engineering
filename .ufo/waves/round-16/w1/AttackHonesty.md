# AttackHonesty — evidence-boundary review

**Axes:** depth; calibration. Advisory only; no judgment, admission, numeric score, or target-capability claim.

## 1. Concrete counterexample: selected files are not an applied snapshot

For request **1.24.6**, the inspected source selects `go1.24.0.json` plus the installed `patchverdiffs/go1.24.6.json.diff`. The base's JSON path `all.Types["runtime.m"].Fields` has no `allpSnapshot`; the diff at **1855–1858** inserts `{"DataType":"[]*runtime.p","Name":"allpSnapshot"}` between `traceback` and `ncgocall`. These are substantive different type representations, not merely different filename labels.

Evidence opened:
- S003, `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`, **getApiSnapshotJsonFile:119–145**: after selecting the diff, the Java path calls `JsonPatch.read`, constructs `JsonPatchApplier`, applies it, and serializes derived JSON. **get:108–111** then passes those bytes into `read`; **read:205–239** builds the ordered bucket map.
- Installed data root `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/`: direct JSON query of `go1.24.0.json` using `.all.Types["runtime.m"].Fields | {has_allpSnapshot:any(.Name == "allpSnapshot"),adjacent:.[32:36]}` returned `false`; direct read of `patchverdiffs/go1.24.6.json.diff:1855-1858` supplies the insertion above. No patch was applied.

**Counterexample implication:** even an executed Python preview reporting `exact_diff`, matching `all`, file hashes, and exit 0 would not establish the patched `runtime.m` representation, successful Java deserialization, or target type recovery. `[SOURCE INFERENCE]` successful application would add that field; successful application itself was not observed.

**Impacted axes:** depth if base-only bucket facts are presented as patched-content facts; calibration if a Python-model run is described as Ghidra/provider/target execution.

**Smallest safe correction:** preserve `evidence_class: "source_model"`, `patch_applied: false`, and the explicit **unpatched base preview** label whenever a diff is selected. Describe an exercised CLI, if L1 records one, as “Python source-model executed against installed data,” not “Ghidra snapshot/recovery executed.” This counterexample does **not** contradict C1's deliberately narrow wording at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/claims.json:6`; it constrains stronger downstream wording. No additional runtime is needed for that narrow claim.

## 2. Concrete counterexample: a documentation green would not prove a producer ran

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/documentation-red.json:6` defines `producing_command_retained` as **`bool(co) and 'argv' in co`**, where `co` is the source text of `controls.py`. `[SOURCE INFERENCE]` an unexecuted script containing `argv` satisfies this predicate. Therefore this documentary assertion cannot establish a producing invocation or its results. The retained artifact actually records exit **1** and all assertions false at the named baseline (`:8-11`); this review claims no green execution.

**Impacted axes:** calibration; depth of command provenance.

**Smallest safe correction:** retain this as a documentation-presence control, not an execution witness. Any statement that controls were actually produced must point to the producer's recorded argv, measured revision/input identity, exit, stdout/stderr, and emitted artifact. Otherwise label it an unexecuted reproducible recipe. This is a fixable evidence-label distinction, not a reason to add another gate.

## Boundaries that should survive integration

- Source reading, installed-byte reading, Python-model execution, compiled Ghidra execution, and target recovery remain separate propositions. A digest establishes byte identity, not execution or successful use.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md:13` already discloses shared installation origin and that the companion source archive is not authenticated against executing compiled classes. Multiple readers of those same bytes do not repair that missing link.
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/CorrectionDraft.candidate.md:7-27` correctly separates the retained `python3 -I` absolute-path invocation from the unexecuted relative/non-isolated spelling. The historical producing record is `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-15/verification.json:28-41`; it is not evidence of a round-16 model run.
- No target was selected. Compiled-source correspondence, an actual Ghidra invocation/result, and target identity/recovery evidence remain outside this review. The reviewed claims do not supply those facts and should not be promoted to them.

**Limits:** reviewed the declared approach and cited source/data/draft records, not a completed selector implementation. Read-only review; no checks, builds, tests, patch engines, providers, targets, or other runtimes executed. No tools installed or updated. Only this report written.
