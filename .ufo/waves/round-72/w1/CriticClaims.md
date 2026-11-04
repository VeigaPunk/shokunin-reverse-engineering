# CriticClaims — round-72 frozen-claim attacks

## Scope and axes

Axes: C1 coverage/completeness of observed checker children; C2 calibration and fail-closed verdict consistency; C3 operability, byte integrity versus producer authenticity; denominator honesty. No production instruments, claims, or plan were edited. No admission or canonical judgment is made here.

**Per frozen claim verdict:** C1 intact against these attacks; C2 intact against these attacks; C3 intact against these attacks. These are deliberately narrow verdicts: the attacks demonstrate false-green component counters, but do not demonstrate the entire frozen conjunction green at the prescribed pinned tool/revision while its literal predicate is false. Do not promote these verdicts into landing verification.

## Exact reproduction command (all attacks and arithmetic)

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-72/w1/CriticClaims/replay.py
```

The retained driver fetches `seam-probe.py` and `capsule_audit.py` using read-only `git show 34fe7aa70b627d92e2d27dbce308d9f5bebda63d:tools/round-72/<name>`, writes fixtures only in `/fast/scratch/hyaku/kaidoku-r72/CriticClaims`, copies result JSON and the generated wrapper to the designated lane receipt directory, and removes scratch in `finally`. Final invocation exited 0. Earlier driver attempts failed with `StopIteration` on a line-number AST selector; fixed by structural selection. The first exploratory invocation imported the live working tree; its result is not frozen evidence. All final receipts use freeze blobs. No tools installed.

## C1 — wrapper can forge both witnesses; census is not complete

**Counterexample.** The fake checker invokes allowlisted git/readelf decoys, overwrites their writable `<log-dir>/<name>.environ` files with clean four-key NUL-separated records, writes a clean checker JSONL, emits clean `checker_child_env`, and then executes `/usr/bin/env -0` with `env=os.environ`. Its actual child receives the caller canary.

**Observed:** `CriticClaims/c1-wrapper.json`: A11 `ok=true`, rc 0, both shim key sets exact, `observed_ok=true`, but `real_child_canary_present=true`; actual child keys include `KAIDOKU_ENV_CANARY`. Generated wrapper retained as `CriticClaims/fake-checker.py`.

The unmodified frozen `checker_env_arm` is executed, not a reimplemented assertion. The frozen shim uses a shell plus `cat /proc/self/environ`; before explicit overwrite the decoy run failed A11 because shell-added `PWD`, `SHLVL`, `_` appeared. That false negative is a separate portability defect: it observes the cat process after shell processing, not necessarily the target exec environment. The final green needs explicit forged records and makes no claim to defeat an external immutable witness.

**Limit / frozen verdict: intact.** This reproduces a false-green A11 against an adversarial replacement wrapper, not a complete 11/11 frozen probe against the prescribed pinned packed-elf tool. The other ten arms and producer-pin constraints were not bypassed. The frozen claim is exposed if its measured-route observation is advertised as complete or adversary-independent child coverage; it cannot establish either. Two names present is a minimum census, not proof of no unobserved children.

**Smallest safe correction:** retain the measured-route trust boundary explicitly; fix shell witness distortion with a native exec-boundary witness. To claim hostile-wrapper completeness requires a parent-owned process/exec census and records inaccessible to the target, rather than another target-writable summary. Do not silently amend the frozen predicate.

## C2 — absent clauses fail closed; contradictory checker output does not

**Counterexample.** A fake checker emits rc 0, `met=false`, a nonempty `failing`, and both binding clauses true for the genuine input. Wrong-nonce and broken-binding copies return rc 1 and the corresponding clause false.

**Execution:** the driver structurally extracts and executes the actual frozen A10 branch, stopping before A11, using the real frozen `invoke`, `bind_producer`, `binding_verdict`, and `arm` functions. Receipt instrument path/hash/revision agree with this fixture wrapper; `defects=[]`. This is not a full-probe run.

**Observed:** `CriticClaims/c2-verdict.json`: contradictory A10 `ok=true`, genuine verdict all true, expected negative clauses false. Direct `binding_verdict({met:false, clauses:{run_nonce:true, run_binding:true}})` returns all true. Empty clause object yields nonce/binding false and A10 false. Completely absent clause object yields `present=false`, both verdicts false. Thus missing clauses do fail closed; no absent-clause false green was found.

**Limit / frozen verdict: intact.** Frozen C2 requires the two named checker clauses, the specific mutant killed in its named case, and landing observations; it does not explicitly require interpreting `met`. The contradiction falsifies a broader interpretation that A10 proves coherent checker acceptance, but not the literal clause-only predicate. No evidence here defeats the frozen self-mutant conjunction.

**Smallest safe correction:** add a separate consistency assertion requiring genuine checker `met is true` and `failing == []`, alongside rc and the two clauses; give the contradiction its own selftest case. Do not make `binding_verdict` require global `met` for negative inputs: unrelated failure must not erase the specific nonce/binding clause diagnosis.

## C3 — forged clean capsule accepted, with or without matching digest

**Counterexample.** Invent two clean records, fabricate an agreeing count/census/run root, omit the digest, then audit; repeat with a computed digest. No producer ever emitted these records.

**Observed:** `CriticClaims/c3-capsule.json`: wholly invented clean capsule accepted (`ok=true`, failures empty), with `clauses.log_sha256=null` when omitted; accepted again with matching fabricated digest. Polluting the actual capsule with a canary while retaining a clean summary (digest omitted) is rejected: `keys` and `canary` fail. The genuine committed capsule was accepted with 46 records and all seven clauses true.

**Limit / frozen verdict: intact.** Audit proves internal consistency and raw-record properties, not execution provenance. Rewriting both capsule and claim consistently defeats authenticity regardless of digest. Frozen A4 explicitly marks omitted digest not evaluated, and the round-71 summary explicitly says digest is integrity accounting, not producer authentication. The frozen C3 tamper battery keeps the genuine summary fixed and its lying-receipt test retains polluted raw bytes; neither promises rejection of an entirely forged clean pair. `ok=true` must not be presented as “every clause true” when one is null.

**Smallest safe correction:** distinguish structural `ok` from all-clauses-evaluated status and retain null explicitly. Require an independently retained digest if a byte-integrity claim is being made. Execution authenticity would require a trusted external capture/attestation boundary; merely requiring a supplied digest is insufficient.

## Denominator arithmetic against retained receipts

`CriticClaims/denominators.json` records the extraction:

- C1 pre receipt: 9/11; exactly A10 and A11 false. Controls agree. The declared after denominator is 11, not 10. No landing 11/11 receipt was present when initially inspected; none is claimed verified here.
- C2 pre survivor receipt: one survivor out of one named mutant. Fixed pre receipt: zero survivors and one named kill; pristine ten cases. One mutant is not eleven probe arms: denominators are distinct.
- C3: 46 nonempty capsule records; census sums `1+16+8+21=46`. Seven tamper shapes are seven negative cases, not the 46-record denominator. Controls' polluted record count 47 is deliberate insertion, not a contradictory genuine count.
- Declared wave seats: `5+3+2+2+1+1+1+1=16`; attack seats `2+2+1=5`; `5/16=31.25%`. “31%” is whole-percent rounding, not exact arithmetic. No arithmetic defect found. These role numbers validate the declared roster arithmetic only, not actual live worker identities.

## Review limitations and self-check

No full route, landing battery, canonical judge, or unrelated runtime was invoked. Component false-green receipts must not be cited as complete frozen-predicate falsification. Scratch cleanup is performed by the executed driver even on exceptions. All retained files are scoped review evidence.

Self-evaluation: accuracy 4 (component/frozen distinction explicit; no full conjunction exercised), completeness 4 (all four assigned attack areas exercised, no full route replay), clarity 4 (trust limits separated from observations), actionability 4 (driver and minimal corrections retained), conciseness 4 (one report covers distinct caveats). Mean 4.0. Highest-impact improvement for integration is an external child census if hostile producer coverage is intended. User should agree this is evidence of component limits, not permission to change frozen claims.
