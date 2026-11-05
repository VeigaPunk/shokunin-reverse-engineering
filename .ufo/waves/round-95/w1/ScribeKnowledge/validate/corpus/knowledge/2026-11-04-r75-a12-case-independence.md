# A12 case independence: a witness may carry several samples, and a mutant has one detector

source: S284 — Python 3 standard library, `os.path.commonpath`, "Return the longest common sub-path of each pathname in the iterable paths." (opened 2026-11-04, https://docs.python.org/3/library/os.path.html#os.path.commonpath, located anchor: `os.path.commonpath` entry, snapshot lines 291–296, sha256 `c33538739c8f63d5d0e677f4fa8c7265cae81f8ff9b02856b61e4d220ef94850`) — the containment predicate `under()` that decides `home_under`/`tmpdir_under` in every witness sample. The grammar half rests on S143 (`re.fullmatch`, opened round 47; reused, not re-registered: a round-75 attempt to append the same page was withdrawn as a duplicate). The argv-as-claim half rests on S277 (`proc_pid_cmdline(5)`, opened round 73; its `used-by` gains this entry this round) and S278 (the read-permission gate). Rows: `corpus/SOURCES.md`.
verified-at: 2026-11-04 — measured at the round-75 declaration `8dff07b9ac7dfc3f099c97d98ee97cc5f69efb3a` (each receipt's `rev` field); the freeze `ec149dc497b4de53ccb3e7a125baa226a66daaa7` pins the instruments. Receipts: `.ufo/waves/round-75/pre/c1-base-arm.json` (patch set `r75base` on the landed round-74 probe: 10 killed, 4 survivors, pristine 20 green, `b-drop-canary-field` failing two cases), `.ufo/waves/round-75/pre/c1-post-at-declaration.json` (patch set `r75probe` on `tools/round-75/seam-probe.py`: 15 killed, 0 survivors, pristine 25 green, canary field sole), `.ufo/waves/round-75/l1/scores/c1-at-landing.json` (the landing re-run).
recheck: re-run the two frozen R75-C1 predicate commands from `plans/round-75-claims.md` — `python3 -I -B tools/round-75/probe-mutation.py --root . --rev <measured> --tool tools/round-75/seam-probe.py --patch-set r75probe --work <scratch> --expect-survivors 0 --expect-target-sha256 1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d --expect-sole b-drop-canary-field --json-out <receipt>` and the same battery with `--tool tools/round-74/seam-probe.py --patch-set r75base --expect-survivors 4` — then read `survivor_count`, `sole_detector` and `target_pin` in the receipts.

## What round 74's wave found

The round-74 battery scored ten defect classes on the round-74 probe and reported
zero survivors — but the wave demonstrated three further defects **outside that
frozen ten** and one cross-binding:

| finding | what the code did | why the selftest was green |
|---|---|---|
| `home_under` / `tmpdir_under` identity | `s.get("home_under") is True` | every fixture fed a real `bool`, never `1` or `"true"` |
| witness name collision | `_name_samples` kept one sample per shim name | a second launch of the same shim was dropped, so first-wins or last-wins could hide a dirty one |
| `lie_clean` key test | `sorted(keys) == allow` | no fixture fed a **superset** of the allowlist |
| cross-binding | deleting the `canary_present` field also failed `a12-kernel-multiple-samples` | that case read `canary_present`, so the canary-field case was not the sole detector |

## What the round-75 probe changes

- **A witness name carries every sample.** `_name_samples` returns
  `name -> [samples]`, and `a12_verdict` reads them through `_samples`, which
  flattens both the list form and the single-dict form (so the selftest's
  synthetic dicts still work). A duplicated shim launch is therefore visible:
  the case `a12-sample-name-merge` feeds dirty-then-clean **and**
  clean-then-dirty and requires detection in both orders. A last-wins or a
  first-wins mutation now fails one of the two orders.
- **The multi-sample case is canary-free.** It asserts count, pids and the argv
  basename only. Deleting the `canary_present` field no longer touches it, so
  `a12-kernel-canary-field` is the *sole* detector of that mutant — the
  battery records `sole: failed == [expect_case]` per mutant.
- **Identity is identity.** `a12-genuine-field-identity` feeds `home_under: 1`,
  `tmpdir_under: 1` and `home_under: "true"`; a truthiness mutation accepts all
  three and is now killed.
- **The lie's key list is exact.** `a12-lie-clean-keys-exact` feeds a forged
  shim whose keys are the allowlist plus one extra, with a dirty forged kernel
  (so `forged_detected` is true and the only reason to fail is `lie_clean`); a
  superset test turns `ok` true and is killed.

## Why argv is a claim, not evidence

The A12 arm exists because a producer can write a clean child-side dump while
its kernel environment is dirty. S277 states the same asymmetry for argv: the
process may override the memory region and "break assumptions about the contents
or format" of `/proc/pid/cmdline`, and a zombie read returns zero characters —
so an argv read is the process's **claim**, never authentication. S278 adds the
read-permission gate: an unreadable environ is a permission outcome and must be
omitted, not read as empty. The two boundaries together are why the witness
keeps field names, presence and containment booleans instead of values, and why
an unreadable sample is dropped rather than defaulted.

## The transferable rule

A mutation closure is only as strong as its **detector grammar**. A case that
feeds a value "close enough" to the sensitive one (a boolean for an identity
check, one sample for a name, an exact list for a containment test) cannot see
the mutation it is supposed to kill. The two questions to ask of every case:
*what input distinguishes the correct code from the plausible mutation?* and
*is the declared case the only detector, or does another case also read that
field?* The first question found the identity and key-list survivors; the second
found the cross-binding. Round 75 makes both mechanical: the extended patch set
and the `sole_detector` field.
