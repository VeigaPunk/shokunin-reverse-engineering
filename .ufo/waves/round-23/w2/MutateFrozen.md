# R23 MutateFrozen — one-newline frozen-fixture probe

## Scope and axes

- Candidate: `2838351450ff1ee4baa620c962a1153450d53311`; frozen baseline: `aa1450b82f9ede35aada63efe8a34e01c6e02f72`.
- **Coverage:** challenge the frozen-input byte-integrity gate, not the six-verb counting result.
- **Calibration:** distinguish a killed newline mutant from a full clean selftest or coverage/admission evidence.
- **Isolation/restoration:** one private local clone, one fixture-only byte edit, exact restoration, then clone removal.
- This is author-side R23-C1 falsification only; not independent outside admission. No claim is made about the observed cumulative T1 count or completeness.

## Findings

### Mutant and expected detector

**Mutant:** append exactly one LF byte (`0a`) after the existing final LF in `.ufo/waves/round-23/frozen/fixture.json` (83-line pristine file; a new blank line 84). This preserves the JSON data while changing its byte snapshot. Only this file was edited, only inside `.ufo/waves/round-23/runtime/MutateFrozen/clone`.

**Expected detector:** the exact candidate counter's `--selftest` must exit **2**, emit `finding=unevaluable`, and identify `snapshot_tampered: .ufo/waves/round-23/frozen/fixture.json`.

Pinned source evidence, read with `git show 2838351450ff1ee4baa620c962a1153450d53311:PATH` rather than the moving worktree:

- `.ufo/waves/round-23/tools/count-c1.py:135-146`: `selftest` validates the hard-coded manifest digest, then every manifest input SHA256, before loading the fixture runner. Input mismatch raises `ValueError('snapshot_tampered: '+rel)` at lines 142–144.
- `.ufo/waves/round-23/tools/count-c1.py:167-169`: that exception becomes JSON `finding=unevaluable` and exit 2.
- `.ufo/waves/round-23/frozen/expected-v2.json:5`: pins the pristine fixture to `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b`.

### Actual bounded detector outputs

The **same bounded manifest/input SHA256 predicate** was applied to pristine, mutated and restored bytes. This was the integrity predicate only, not three full CLI selftests.

| Stage | Fixture bytes | Fixture SHA256 | Bounded outcome |
| --- | ---: | --- | --- |
| Pristine | 2394 | `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` | `snapshot_intact`; all input digests match |
| Mutated | 2395 | `e8fff600c84acaae59f285b515a71bdccce6be23a9c074d6a5efd0e882c2c9c0` | `snapshot_tampered`; only the fixture digest mismatches |
| Restored | 2394 | `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` | `snapshot_intact`; all input digests match |

A direct bytes comparison also established `mutated == pristine + b'\n'` and `restored == pristine`. The pristine integrity baseline succeeded; it was not an inconclusive baseline failure.

### Exact candidate invocation and output

Executed **once**, with the fixture mutated:

```text
cwd: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/runtime/MutateFrozen/clone
argv: ["python3", "-I", "-B", ".ufo/waves/round-23/tools/count-c1.py", "--root", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/runtime/MutateFrozen/clone", "--selftest"]
exit: 2
stdout: {"error": "snapshot_tampered: .ufo/waves/round-23/frozen/fixture.json", "finding": "unevaluable"}
stderr: <empty>
```

Stdout ended in one LF. The retained JSON stores the exact argv, stdout, stderr and exit, plus clone/checkout/removal command records and the exact pinned `git show` outputs.

**Verdict: KILLED.** The one-newline mutant was rejected with precisely the assigned error and exit status. This confirms the fixture-byte tampering detector for this one input/mutation only. No full green suite was run or claimed; pristine/restored checks were SHA256 integrity checks. `RunSelftest` retains ownership of the full clean-suite result.

## Source/input hashes and restoration evidence

All four hashes below matched candidate `git show` bytes in the pristine clone. After restoration, all four again matched; the counter, helper and manifest were unchanged throughout the mutation.

| Pinned path | Bytes | SHA256 before / after restoration |
| --- | ---: | --- |
| `.ufo/waves/round-23/tools/count-c1.py` | 8382 | `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2` |
| `.ufo/waves/round-23/tools/counter-fixtures.py` | 6560 | `f2990b35d113b5e44317e7f00e6ca5157baae1efb5ee1a1b8e4995d0ace1a97f` |
| `.ufo/waves/round-23/frozen/expected-v2.json` | 2389 | `458b30d5a6420c1b37874c3364d3ae3b22529d6c3560b5241848a21eec97096f` |
| `.ufo/waves/round-23/frozen/fixture.json` | 2394 | `a1f5aff8ebb5e5d327522031b74ed91283708907af0fc4a6df24812479bfef4b` |

Restoration ran in a `finally` block before clone removal. Then `rm -rf -- /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/runtime/MutateFrozen/clone` exited 0 with empty stdout/stderr; path existence was false afterward. The private clone is removed. Production sources, production Git/index, peer reports and operator configuration were not modified. The only retained writes are this scoped report and the own-seat receipt under the ignored runtime root.

## Produced files and hashes

- `.ufo/waves/round-23/runtime/MutateFrozen/probe.json` — full commands/outputs, pinned source bytes, input/source hashes, all three bounded detector observations, exact mutation/restoration evidence, verdict and clone-removal evidence. **SHA256:** `e3dcdfb4427199dce82c2dff19cdec031df3ecd9292b262040411746d539cd2a`; **bytes:** 31982.
- `.ufo/waves/round-23/w2/MutateFrozen.md` — this report; its SHA256 is supplied in the final handoff (not embedded recursively).
- No private clone, generated source, temporary runner or mutation remains.

## Installs

None. No package transactions, host-service actions, global installs or configuration edits.

## Open risks / limits

- The full clean selftest and all six T1 behaviors were not exercised by this seat; no green-suite, count, source relevance, authentication or ownership-admission conclusion follows from this mutation probe.
- This single killed mutant does not establish rejection of every possible tamper or changing snapshot manifests/constants together.
- The retained runtime receipt lives under the ignored own-seat runtime directory; retain it with the wave evidence if ignored runtime cleanup is later performed.

Report: .ufo/waves/round-23/w2/MutateFrozen.md
