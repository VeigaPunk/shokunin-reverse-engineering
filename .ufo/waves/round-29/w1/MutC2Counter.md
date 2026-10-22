# Round 29 C2 counter mutation probe

## Scope and detector

**Observation.** Mutated only `tools/round-29/c2-filtered-unseen.py` in the isolated clone at `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutC2Counter/clone`; the lane remained read-only. Each mutant started from pristine bytes, ran the same detector, was restored from the byte-for-byte backup, and ran the detector again.

Detector command, from the clone root:

```text
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -I -B tools/round-29/c2-filtered-unseen.py --selftest
```

**Observation.** Pristine run at `2026-10-22T20:21:38Z`: exit `0`; output ended `selftest cases=19 failures=0`. Pristine SHA-256: `00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801`. Thus the baseline passed; mutant failures below are killed mutants, not baseline failures.

## Mutants

| Mutant | Mutated bytes SHA-256 | UTC | Actual detector output excerpt | Detector exit | Verdict |
|---|---|---|---|---:|---|
| Removed `predicted_false >= 1` from the success gate | `440377a485e1b26b442db6053cc38ccb1c182eb94be02cca416db089410c76f3` | `2026-10-22T20:22:06Z` | `FAIL red-no-false-branch exit=0 want=1`; `selftest cases=19 failures=1` | 1 | **Killed** |
| Removed claim-row validation in `check_entry` | `b74fe03612eb737afdc904583ebd6ca39d6969df0393fdfc753ee91216137353` | `2026-10-22T20:22:25Z` | `FAIL red-entry-old-row exit=0 want=1`; `FAIL red-row-not-in-gate exit=0 want=1`; `FAIL red-row-status exit=0 want=1`; `FAIL red-cites-other-new-row exit=0 want=1`; `selftest cases=19 failures=4` | 1 | **Killed** |
| Flipped the missing-canonical-signature fallback to predict `True` (filtered) | `16d422899ae315d93cf496d1920a7861edb1e8da0979b97424d0250164490fc5` | `2026-10-22T20:22:48Z` | `FAIL green-both-branches exit=1 want=0`; `FAIL red-flag-on-non-canonical exit=0 want=1`; `selftest cases=19 failures=2` | 1 | **Killed** |
| Compared names with `.casefold()` | `7dbc934a1d4e1769244de06745a0cf73bf6a84774f59d7a98008d5030d9a0430` | `2026-10-22T20:23:00Z` | `selftest cases=19 failures=0` | 0 | **Survived — coverage finding** |
| Replaced strict boolean identity (`is not`) with equality (`!=`) | `3c8305ec86bbfbc75ce6f87244def47d79b09487043b2069b035e2e00a50789d` | `2026-10-22T20:23:17Z` | `FAIL red-flag-not-boolean exit=0 want=1`; `selftest cases=19 failures=1` | 1 | **Killed** |
| Removed the timestamp ordering test `t <= ctime` | `842494ea271c3f187fbca8d83394f6a4f5c7a026be0f3d5a2ca4e5eaa69d3bcb` | `2026-10-22T20:23:32Z` | `FAIL red-early-fetch exit=0 want=1`; `selftest cases=19 failures=1` | 1 | **Killed** |
| Removed the response SHA-256 comparison | `e3bc79882cb37ccfac8059e98f2e78aad35821977b1ebfa85085dd553e3d750b` | `2026-10-22T20:23:43Z` | `FAIL red-sha exit=0 want=1`; `selftest cases=19 failures=1` | 1 | **Killed** |

**Observation — missing-signature branch.** The prompt's “treat a key with no signature as unfiltered” describes the current rule (`pred` is false when `c is None`), so that literal change would be behavior-equivalent, not a meaningful mutant. I tested its plausible faulty inverse instead. The selftest's `11111111` response has no canonical-signature entry and `filtered: false`; flipping that fallback is detected by both the green case and `red-flag-on-non-canonical`. **Conclusion: the magic/missing-signature branch is tested.**

**Inference — surviving casefold mutant.** The test suite does not distinguish exact from case-insensitive comparison: its signature/name fixtures contain no case-only difference. The casefold mutant therefore survives, indicating a coverage gap for names that differ only by case; this is not a change to the contract.

## Restoration evidence

**Observation.** After each mutant, the clone target was restored from `pristine.py`; every recorded post-restore target hash was `00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801`. Each of the seven restored selftests exited `0` and printed `selftest cases=19 failures=0` (UTC starts: `20:22:06Z`, `20:22:25Z`, `20:22:48Z`, `20:23:01Z`, `20:23:17Z`, `20:23:32Z`, `20:23:44Z`). The pristine and all restored stdout files have SHA-256 `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a`.

## Scratch evidence artifact SHA-256

All listed paths are under `/fast/scratch/hyaku/kaidoku-r29/seats/w1/MutC2Counter/` unless shown otherwise.

| Artifact | SHA-256 |
|---|---|
| `pristine.py` | `00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801` |
| `pristine-selftest.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `mut-casefold.py` | `7dbc934a1d4e1769244de06745a0cf73bf6a84774f59d7a98008d5030d9a0430` |
| `mut-casefold.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `mut-drop-claim-row.py` | `b74fe03612eb737afdc904583ebd6ca39d6969df0393fdfc753ee91216137353` |
| `mut-drop-claim-row.txt` | `3ac4e8e16ad51546fd06dc6cc25cbfade4f284dc575a28b72e5cd5d999f36bd4` |
| `mut-drop-predicted-false.py` | `440377a485e1b26b442db6053cc38ccb1c182eb94be02cca416db089410c76f3` |
| `mut-drop-predicted-false.txt` | `2efefffcb11c703950c10cf7a3f305d612cf0894e9885673f24df366e66acc27` |
| `mut-drop-sha.py` | `e3bc79882cb37ccfac8059e98f2e78aad35821977b1ebfa85085dd553e3d750b` |
| `mut-drop-sha.txt` | `0e103f291ad3b8762a7c6e22071a86408d77d2ed424421a98c80c068c85d0ac3` |
| `mut-early-fetch.py` | `842494ea271c3f187fbca8d83394f6a4f5c7a026be0f3d5a2ca4e5eaa69d3bcb` |
| `mut-early-fetch.txt` | `2e94269d0eff89c1897a90180d22e2f7439b1881eca4aa80bde38c6e972ee593` |
| `mut-missing-signature-filtered.py` | `16d422899ae315d93cf496d1920a7861edb1e8da0979b97424d0250164490fc5` |
| `mut-missing-signature-filtered.txt` | `b05a286a6f6d3d186d17b5f9fdb8f74fc4fd5196d30a309dbf96404f1cc655fa` |
| `mut-nonboolean-flag.py` | `3c8305ec86bbfbc75ce6f87244def47d79b09487043b2069b035e2e00a50789d` |
| `mut-nonboolean-flag.txt` | `ffbdbe6b9fb99f34a43aeffa8d0c1a6b5376b0db902472979f343f3d3f2688cb` |
| `restore-casefold.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `restore-drop-claim-row.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `restore-drop-predicted-false.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `restore-drop-sha.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `restore-early-fetch.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `restore-missing-signature-filtered.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `restore-nonboolean-flag.txt` | `3e3d5926afec89d77fefb11add5b0f1cb2bef1eaad502e1c0dc5f140418fa06a` |
| `clone/tools/round-29/c2-filtered-unseen.py` | `00ca0a3d72515c2636c63f39785d799924dd6530f67cc8787b2a632817c5a801` |

No tools were installed or updated.