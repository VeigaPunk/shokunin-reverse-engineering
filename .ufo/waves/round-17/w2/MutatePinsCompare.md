# MutatePinsCompare — round 17, wave 2

**Axes:** calibration; depth. **Observation:** 12 independent one-line mutants: **8 survived, 4 killed, 0 inconclusive** by the assigned `--selftest` detector. All pristine and restored selftests passed. A separate, independent witness for each mutation returned **0 / 1 / 0** on pristine / mutated / restored bytes, confirming every mutant changed observable behavior. These are bounded selftest-coverage findings, not defects alleged to exist in the pristine implementation.

## Scope and detector

- Source: Git objects at `da64646adcb19c1ede7537b799b8c7d283fe43da`, extracted using `git show da64646adcb19c1ede7537b799b8c7d283fe43da:.ufo/waves/round-17/tools/<file>`; current lane source hashes matched those objects. All source anchors below are relative to the lane at that revision.
- Each ID had its own directory under `/tmp/r17-MutatePinsCompare-xmr2hy`, containing both original scripts. Only the named target line was mutated; the sibling import remained pristine.
- Same primary command before mutation, during mutation, and after exact restoration: `python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/<ID>/<target> --selftest`. Python: **3.14.8**; cwd and TMPDIR: `/tmp/r17-MutatePinsCompare-xmr2hy`; each command bounded to 30 seconds. Expected mutation detector: exit 1 / `SELFTEST: FAILED`, conditional on pristine/restored exit 0.
- Same independent witness command across all three states: `python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/<ID>/<target> <ID>`. It imports only these Python tools, uses temporary data files, computes reference digests with stdlib hashlib, and expects exit 0 when the invariant holds. Witness counts below are lengths of the returned path lists, not altered tool return values.
- Ran **36 selftest commands + 36 witness commands**. No carrier execution, REA, Ghidra, judge, other orchestration runtime, installation, commit, or source-tree edit. The only lane write is this report.

## Mutation results

P = pristine, M = mutated, R = restored. The replacement column is the entire changed source line, without indentation.

| ID | Original source anchor | Exact replacement | Selftest P/M/R | Verdict |
|---|---|---|---|---|
| P01 | `.ufo/waves/round-17/tools/pins.py:96` | `elif a.get("size") != b.get("size"):` | 0/0/0 | survived |
| P02 | `.ufo/waves/round-17/tools/pins.py:96` | `elif a.get("sha256") != b.get("sha256"):` | 0/0/0 | survived |
| P03 | `.ufo/waves/round-17/tools/pins.py:82` | `for path in sorted(set(pre_entries) & set(post_entries)):` | 0/0/0 | survived |
| P04 | `.ufo/waves/round-17/tools/pins.py:98` | `equal = not changed and not missing` | 0/1/0 | killed |
| P05 | `.ufo/waves/round-17/tools/pins.py:98` | `equal = not changed and not errors` | 0/1/0 | killed |
| P06 | `.ufo/waves/round-17/tools/pins.py:96` | `elif a.get("sha256") != b.get("sha256") and a.get("size") != b.get("size"):` | 0/0/0 | survived |
| R01 | `.ufo/waves/round-17/tools/receipt-validate.py:337` | `for field in ("changed", "missing", "errors"):` | 0/0/0 | survived |
| R02 | `.ufo/waves/round-17/tools/receipt-validate.py:337` | `for field in ("equal", "changed", "missing"):` | 0/0/0 | survived |
| R03 | `.ufo/waves/round-17/tools/receipt-validate.py:337` | `for field in ("equal", "missing", "errors"):` | 0/1/0 | killed |
| R04 | `.ufo/waves/round-17/tools/receipt-validate.py:127` | `actual = expected_sha` | 0/0/0 | survived |
| R05 | `.ufo/waves/round-17/tools/receipt-validate.py:80` | `digest.update(b"")` | 0/1/0 | killed |
| R06 | `.ufo/waves/round-17/tools/receipt-validate.py:79` | `for chunk in [handle.read(1 << 20)]:` | 0/0/0 | survived |

All six pin baselines/restorations ended with the actual stdout line `SELFTEST: CLEAN cases=7`; all six receipt baselines/restorations printed `SELFTEST: CLEAN cases=5`. Stderr was empty for every primary and independent-witness invocation.

The four killed controls failed the intended assertions: **P04** `api-error`; **P05** `api-missing`; **R03** `pins_compare_forged_red` (exit 0, expected 1); **R05** `retain_green` and `carrier_green` (exit 1, expected 0). Full unabridged stdout for all three states is retained in the evidence JSON below.

## Missing cases demonstrated by survivors

1. **P01/P06 — equal-size changed bytes.** At `.ufo/waves/round-17/tools/pins.py:192-199` and `:233-245`, both red fixtures change digest **and** length. Removing SHA comparison, or changing OR to AND, still passes all seven cases. Independent witness: snapshot `b"alpha"`, overwrite with `b"omega"`, snapshot, compare; the mutants incorrectly return equal.
2. **P02 — size differs with digest held fixed.** A copied snapshot with only its recorded size incremented exercises the other disjunct at `.ufo/waves/round-17/tools/pins.py:96`. This is a synthetic recorded-metadata case, **not** evidence of a SHA collision or naturally generated same-digest/different-size files. It verifies the explicit size comparison contract.
3. **P03 — one-sided path sets, in both directions.** At `.ufo/waves/round-17/tools/pins.py:201-207`, the deleted-file fixture still has the same entry key on both sides, with an error entry after deletion. It cannot distinguish union from intersection at `:82`. Comparing a populated snapshot against an empty snapshot, then reversing the arguments, does.
4. **R01/R02 — independently forge each comparison field.** The only receipt comparison forgery at `.ufo/waves/round-17/tools/receipt-validate.py:545-553` changes `changed`; omission of `changed` is killed (R03), but omission of `equal` or `errors` at `:337` survives. The witnesses change exactly one recorded field and otherwise leave recomputation consistent. The `missing` field was not separately mutated in this probe.
5. **R04 — digest recomputation without size fallback.** At `.ufo/waves/round-17/tools/receipt-validate.py:536-543`, `b"pinned bytes\n"` (13 bytes) becomes `b"tampered bytes\n"` (15 bytes). Replacing the digest read at `:127` with the expected digest still passes the suite: the red case is rescued by size mismatch. Despite the comment, that case mutates only the pinned file, not stdout/stderr. The independent same-size `alpha`→`omega` witness returns no findings under R04. An independent digest-only red case for each pinned/captured/log commitment is absent from this suite.
6. **R06 — hashing beyond the first chunk.** The selftest files at `.ufo/waves/round-17/tools/receipt-validate.py:518-525` are all small. Hashing only the first read at `:79` passes. A 1,048,577-byte known-answer fixture, `b"a" * (1 << 20) + b"z"`, produces the wrong digest under R06. The independent reference hashes the entire payload, not the function under mutation.

**Calibration:** the original implementations passed every independent witness. Survival means the existing selftest does not detect that injected defect; it does not authorize changing the contract or establish the defect in shipped bytes. The depth result is the isolated distinction between digest-vs-size detection, path-set-vs-filesystem disappearance, and full-vs-first-chunk hashing.

## Exact survivor commands and observed output

Commands below ran against mutant bytes before restoration. For each ID, both the pristine and restored independent witness exited 0; the mutant witness exited 1. Primary mutant selftests exited 0 despite that independently observed violation.

### P01

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/P01/pins.py --selftest
red case observed: compare exit 1 names /tmp/r17-MutatePinsCompare-xmr2hy/pins-selftest-emlm84r1/a.txt
SELFTEST: CLEAN cases=7
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/P01/pins.py P01
{"case": "P01", "expected": {"changed": 1, "equal": false, "errors": 0, "missing": 0}, "observed": {"changed": 0, "equal": true, "errors": 0, "missing": 0}, "pass": false}
[exit 1; stderr empty]
```

### P02

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/P02/pins.py --selftest
red case observed: compare exit 1 names /tmp/r17-MutatePinsCompare-xmr2hy/pins-selftest-z7js3diz/a.txt
SELFTEST: CLEAN cases=7
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/P02/pins.py P02
{"case": "P02", "expected": {"changed": 1, "equal": false, "errors": 0, "missing": 0}, "observed": {"changed": 0, "equal": true, "errors": 0, "missing": 0}, "pass": false}
[exit 1; stderr empty]
```

### P03

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/P03/pins.py --selftest
red case observed: compare exit 1 names /tmp/r17-MutatePinsCompare-xmr2hy/pins-selftest-p4mi_eq8/a.txt
SELFTEST: CLEAN cases=7
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/P03/pins.py P03
{"case": "P03", "expected": [{"changed": 0, "equal": false, "errors": 0, "missing": 1}, {"changed": 0, "equal": false, "errors": 0, "missing": 1}], "observed": [{"changed": 0, "equal": true, "errors": 0, "missing": 0}, {"changed": 0, "equal": true, "errors": 0, "missing": 0}], "pass": false}
[exit 1; stderr empty]
```

### P06

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/P06/pins.py --selftest
red case observed: compare exit 1 names /tmp/r17-MutatePinsCompare-xmr2hy/pins-selftest-22nysyfk/a.txt
SELFTEST: CLEAN cases=7
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/P06/pins.py P06
{"case": "P06", "expected": {"changed": 1, "equal": false, "errors": 0, "missing": 0}, "observed": {"changed": 0, "equal": true, "errors": 0, "missing": 0}, "pass": false}
[exit 1; stderr empty]
```

### R01

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/R01/receipt-validate.py --selftest
SELFTEST: CLEAN cases=5
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/R01/receipt-validate.py R01
{"case": "R01", "expected": [{"code": "pins_compare_mismatch", "where": "$.pins_compare.equal"}], "observed": [], "pass": false}
[exit 1; stderr empty]
```

### R02

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/R02/receipt-validate.py --selftest
SELFTEST: CLEAN cases=5
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/R02/receipt-validate.py R02
{"case": "R02", "expected": [{"code": "pins_compare_mismatch", "where": "$.pins_compare.errors"}], "observed": [], "pass": false}
[exit 1; stderr empty]
```

### R04

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/R04/receipt-validate.py --selftest
SELFTEST: CLEAN cases=5
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/R04/receipt-validate.py R04
{"case": "R04", "expected": ["sha256_mismatch"], "observed": [], "pass": false}
[exit 1; stderr empty]
```

### R06

```text
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/R06/receipt-validate.py --selftest
SELFTEST: CLEAN cases=5
[exit 0; stderr empty]
$ python3 -B -I /tmp/r17-MutatePinsCompare-xmr2hy/witness.py /tmp/r17-MutatePinsCompare-xmr2hy/R06/receipt-validate.py R06
{"case": "R06", "expected": "03a3a055d5c33cdcaa15f945b5bca4450a3f3d374ebac452b7f119871342ca95", "observed": "9bc1b2a288b26af7257a36277ae3816a7d4f16e89c1e7e77d0a5c48bad62b360", "pass": false}
[exit 1; stderr empty]
```

## Restoration and hashes

Exact-byte restoration was performed in a finally block for every isolated pair before restored detectors ran. Both copied files were hashed before mutation, during mutation, and after restoration. In all 12 directories the entire two-file before/after `sha256sum` output matched exactly; only the designated target digest changed during mutation.

Before = restored SHA-256 (also unchanged lane-source SHA-256 before/after):

- **P** (pins.py): `9e9c72507de429c913891c65ffeafda9a686fee532d6a9dcfcd42b8092639fe0`
- **R** (receipt-validate.py): `53a5f0964e7787f59268c7f5e22415e4f6cb7ab7a6d2dbf7665e3cfdeee27cc7`

| ID | Before/restored target hash | Actual mutant SHA-256 |
|---|---|---|
| P01 | P / same | `b22cf882280dcf3f412af840ae9f2b936d1ba4b89d140a36522bf25a2c024f64` |
| P02 | P / same | `a171ccb5b9e697cb1435f7000bdb88256f6287c89d639ebb77c5980fd0f4ae91` |
| P03 | P / same | `8188b5e1dd7e627314ab75007d27623982d745174122058cb5ddcbac6f7aacc4` |
| P04 | P / same | `e497d33b727696c8432d898d9fcff05e99159d3bdf2d1f7beec496194e581641` |
| P05 | P / same | `3d96dd312b1c3361bcdcfd794e4de575ce7edbc169483231ff72ba5fa71a0201` |
| P06 | P / same | `d1cdb13429d30d0c6280f85fe4599823390a5fb41a1a22f425228466aabfdeb9` |
| R01 | R / same | `38a96b095cd76f5dc8402781ca73280ab51b4b4905748aa789654e17683e55e0` |
| R02 | R / same | `5b468a3253c3aaa0a2f66ae870266355231cf3d5c33fd78324f35268b2b4673f` |
| R03 | R / same | `8edbc7e97d68a507052377a251fd6cce1f5cfc96a2185889725a3c9d0053baa0` |
| R04 | R / same | `c7b620cf701b23feab14561ac937691b26cdaeb510c322400cde6aa92e8155bb` |
| R05 | R / same | `b96108ff3965e9812e586b4022f8f9c1bd08b04dd3ed92fa30118ca0df42cf2b` |
| R06 | R / same | `fba4bd0d53b230c25a9756621ffd97ac003e82e5c2a560757501709bce1a4e7d` |

Supplemental scratch evidence (no lane artifacts other than this report):

- `/tmp/r17-MutatePinsCompare-xmr2hy/results.json`: exact argv, return codes, full stdout/stderr, before/mutant/restored hashes, and restoration flags for every probe and both detectors.
- `/tmp/r17-MutatePinsCompare-xmr2hy/witness.py`: complete independent bounded detector, retained for reproduction; temporary fixture subdirectories were removed.

Actual evidence hashes:

```text
3cbc2f579776d0e9593bc64f1025528dbb45c8c2e233e50a80c6e23290058409  /tmp/r17-MutatePinsCompare-xmr2hy/results.json
7d51ea398fa44ee3d1c2797691a2e0afcb03aa5076e31295d35aa1e81255684c  /tmp/r17-MutatePinsCompare-xmr2hy/witness.py
```

No tools installed or updated. No production fix or integration performed.
