# MutC1Judge — C1 judge/normalizer selftest mutation probe

## Result and scope

**Observation: 14 of 14 single-clause mutants killed; 0 survived; 0 inconclusive.** All 11 requested defect classes were exercised in `judge()`, plus three direct field-loss mutants in `rea_tuples()`. Each isolated copy received its own pristine, mutated and byte-restored run of the same `--selftest` detector: 42 detector executions, 25 cases per execution.

**Observation:** every pristine and restored execution exited 0 with `selftest cases=25 failures=0`; every mutated execution exited 1 with an actual assertion failure, not an import error, exception or timeout. All stderr strings were empty. Full stdout/stderr, command arguments, UTC intervals, exit codes and hashes are retained in the three phase receipts below.

**Survivor findings:** none. No missing selftest case was exposed by this finite mutant set. **Unknown:** completeness against other defects and live P1/carrier behavior; this probe did not measure either. The frozen counter/selftest was not edited, no REA was invoked, and no carrier or C2 mutant was opened or executed. No claim is made that R30-C1 itself passes.

Axes: single-clause isolation, behavioral kill discrimination, exact-byte restoration. Four concurrent detector subprocesses at most; no agents spawned. Python reported `Python 3.14.8` from `timeout 10 python3 --version`. No tools were installed or updated.

## Detector and execution receipts

Each following exact detector command was run three times on the same path, once per phase. The `timeout` wrapper bounds the otherwise unchanged requested `python3 -I -B <copy> --selftest` detector.

```sh
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M01/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M02/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M03/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M04/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M05/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M06/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M07/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M08/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M09/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M10/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M11/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M12/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M13/c1-rust-positive.py --selftest
timeout -k 5 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M14/c1-rust-positive.py --selftest
```

Producing orchestration commands, all completed successfully:

```sh
timeout -k 5 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/probe.py pristine
timeout -k 5 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/probe.py mutated
timeout -k 5 180 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/probe.py restored
```

| Phase | UTC interval, 2026-10-23 | Detector exits | Exact summary output |
| --- | --- | --- | --- |
| Pristine | 02:43:55.081934–02:43:55.218968Z | 14 × 0 | `selftest cases=25 failures=0` on every copy |
| Mutated | 02:44:23.133518–02:44:23.266344Z | 14 × 1 | `selftest cases=25 failures=1` for M01–M11; `selftest cases=25 failures=3` for M12–M14 |
| Restored | 02:44:42.474882–02:44:42.600622Z | 14 × 0 | `selftest cases=25 failures=0` on every copy |

## Mutants and killing cases

All row verdicts are **observations**. Line numbers refer to pristine source. Every mutation touched one guard/comparison/extraction clause only; selftest bytes were unchanged.

| Mutant / single-clause change | Killed-or-survived | Killing case(s) | Mutated UTC start, 2026-10-23 | Exit |
| --- | --- | --- | --- | --- |
| M01: remove nonzero-exit guard, lines 96–97 | killed | `red-nonzero-exit` | 02:44:23.133518Z | 1 |
| M02: omit `ok is True` clause at line 98, retain dict-shape guard | killed | `red-not-ok` | 02:44:23.133744Z | 1 |
| M03: remove operation guard, lines 101–102 | killed | `red-other-operation` | 02:44:23.134007Z | 1 |
| M04: remove subject digest guard, lines 104–105 | killed | `red-subject-mismatch` | 02:44:23.133899Z | 1 |
| M05: line 116 compares `set(got)` with `set(oracle_tuples)` | killed | `red-duplicate-package` | 02:44:23.167871Z | 1 |
| M06: line 116 compares `t[:5]` projections, omitting dependency tuples | killed | `red-edge-dropped` | 02:44:23.168910Z | 1 |
| M07: line 116 compares `t[:3] + t[4:]` projections, omitting kind | killed | `red-kind-dropped` | 02:44:23.168880Z | 1 |
| M08: line 116 compares `t[:4] + t[5:]` projections, omitting root | killed | `red-root-dropped` | 02:44:23.169500Z | 1 |
| M09: remove offset guard, lines 118–119 | killed | `red-offset-differs` | 02:44:23.201399Z | 1 |
| M10: remove compressed-size guard, lines 120–121 | killed | `red-size-differs` | 02:44:23.202289Z | 1 |
| M11: remove nonempty-oracle guard, lines 110–111 | killed | `red-empty-oracle` | 02:44:23.202350Z | 1 |
| M12: `rea_tuples()` line 89 sets `deps = ()` | killed | `green-exact`, `green-reordered-indices`, `green-committed-agrees` | 02:44:23.206643Z | 1 |
| M13: `rea_tuples()` line 90 emits `None` instead of extracted kind | killed | `green-exact`, `green-reordered-indices`, `green-committed-agrees` | 02:44:23.233587Z | 1 |
| M14: `rea_tuples()` line 90 emits `False` instead of extracted root | killed | `green-exact`, `green-reordered-indices`, `green-committed-agrees` | 02:44:23.234160Z | 1 |

Exact killing stdout excerpts, in M01–M11 order (each line belongs to its corresponding command above):

```text
FAIL red-nonzero-exit got=P1-pass (packages=2 edges=1)
FAIL red-not-ok got=P1-pass (packages=2 edges=1)
FAIL red-other-operation got=P1-pass (packages=2 edges=1)
FAIL red-subject-mismatch got=P1-pass (packages=2 edges=1)
FAIL red-duplicate-package got=P1-pass (packages=3 edges=1)
FAIL red-edge-dropped got=P1-pass (packages=2 edges=0)
FAIL red-kind-dropped got=P1-pass (packages=2 edges=1)
FAIL red-root-dropped got=P1-pass (packages=2 edges=1)
FAIL red-offset-differs got=P1-pass (packages=2 edges=1)
FAIL red-size-differs got=P1-pass (packages=2 edges=1)
FAIL red-empty-oracle got=P1-pass (packages=0 edges=0)
```

Each of M12, M13 and M14 separately emitted this exact excerpt:

```text
FAIL green-exact got=P1-fail (package multiset differs (rea 2, oracle 2))
FAIL green-reordered-indices got=P1-fail (package multiset differs (rea 2, oracle 2))
FAIL green-committed-agrees got=False (committed package multiset differs)
selftest cases=25 failures=3
```

**Inference limited to these probes:** the requested acceptance-weakening defects are detected by their intended negative cases (M01–M11). Direct normalizer field-loss defects are detected by positive/committed-agreement cases (M12–M14); those three were not credited to the negative field-loss cases.

## Restoration and bounds evidence

**Observation:** the original lane tool, untouched pristine snapshot, all 14 copies before mutation, and all 14 copies after restoration have SHA-256:

```text
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a
```

Each mutant's intervening hash is listed with its preserved mutant snapshot in the inventory below and in its mutated receipt. Every receipt also records identical before/after hashes for the detector itself, so the detector did not modify the tested bytes. Restoration used the inverse surgical edit at the same clause; exact original hashes and successful restored detector runs establish byte restoration, not merely equivalent behavior. Preserved `c1-rust-positive.mutant.py` files are inert evidence copies, not the restored tested paths.

All subprocesses were bounded with a 30-second timeout and 5-second kill grace, were collected to exit by the driver, and recorded `forced_process_group_kill=false`. No background job or service was started. No Git/jj writes, source integration or changes to sibling files occurred. The sole lane write is this assigned report.

## Opened sources

Access date for all entries: **2026-10-23**. Local sources were opened with ordinary file reads; hashes are of complete file bytes. Quotes are contiguous excerpts of at most 25 words. The oracle was read for context only; `--selftest` does not load it.

| URL | SHA-256 | Located quote |
| --- | --- | --- |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | line 94: `def judge(env, carrier_sha, oracle_sec, oracle_tuples, exit_code):` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py` | `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` | line 3: `Shares no code with REA. It parses the container section tables itself` |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | line 14: `Record every install or update — tool, version, channel, reason — in your report or handoff.` |
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | line 10: `You are a Godspeed-enabled subagent.` |
| `file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | line 14: `complete source repository, use normal repository tools and do not run REA` |

## Retained artifact inventory

The following lists every retained scratch file with its SHA-256. Phase JSON files contain full detector stdout/stderr and before/after hashes, not only excerpts. Hashes were produced using bounded `timeout 30 sha256sum` commands over these absolute paths.

```text
9639ecdb8cd3fa35beeb3a65ebfd9dfa90c8e2e7f7efd3b803a98dfc86a928ea  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/probe.py
ba814ba0c4be5d8cebf7681c98223583ec65707f7516deeb9d625f7debce8cf8  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/manifest.json
f4ad16505220a7f3fdd2321b2d7ce5bf079d7c2eb57735d1d90817955f1a005d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/pristine.json
6683fa4a5031e746fda057d53dc69cc3a4f658288bf588b29a176795b8c59c59  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/mutated.json
744802ffd4da652b6fa49eed3712403a1bb978b89643f0016f54022bf99f7bab  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/restored.json
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/pristine/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M01/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M02/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M03/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M04/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M05/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M06/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M07/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M08/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M09/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M10/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M11/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M12/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M13/c1-rust-positive.py
e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M14/c1-rust-positive.py
69b6790c6e97ef267f7e9c48252abcfb14e8ad3bfc9a64367031e0a503deb4d8  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M01/c1-rust-positive.mutant.py
448f619ed091682920ae82e35425ed6d435160dd4fd2b36f219fa61e9f43e75b  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M02/c1-rust-positive.mutant.py
9f2b1db37ec075026efb9ae2ad62bf17080fed3e6345d173bbb92937bbaf0c3d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M03/c1-rust-positive.mutant.py
7d35693d090b9ae0796898c6c5ae15f0af5e8ba7bb9cb6c9910f7dab5999f230  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M04/c1-rust-positive.mutant.py
2d94756417576de61ef7de2a10df250fce13a70b65b232c7975b6317699f185c  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M05/c1-rust-positive.mutant.py
63792652e98e8691438725f7a683e84b51f0441650d8eda83592aea1681ace73  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M06/c1-rust-positive.mutant.py
05ca9fa737deccfc8fcc3931a159f44e98df651f531a3d8d359c076e385479ee  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M07/c1-rust-positive.mutant.py
6eef99780bee7b9d264c8d2f5fb85cd8bbaacc5e7be8a2b1fd138aa176772b8a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M08/c1-rust-positive.mutant.py
dba9f23f9da42364cddc98c8b221f3cf899b8d5efe9fc27f11c65a2dabd4c09b  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M09/c1-rust-positive.mutant.py
4aa29d7537bac226af869daf735298fc6b62611bf041cfc944adbad2d3ac755d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M10/c1-rust-positive.mutant.py
5fa0437aa2a8606b62790d92ae2a8613539b00e0f8b76daa2a41b89e8bdefcd1  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M11/c1-rust-positive.mutant.py
6e7218048c283788a345ab677828d9f2626d95926a60f2a500b78215692c30d6  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M12/c1-rust-positive.mutant.py
2b5e1b707e0a5a7f049cc64a6d31ad022be834825175fc1c5714fa76a767bd20  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M13/c1-rust-positive.mutant.py
47c2c4de45e7ee970b367f626aaee4b899f7ef2c1050695e7c23cfca9399f543  /fast/scratch/hyaku/kaidoku-r30/seats/w1/MutC1Judge/M14/c1-rust-positive.mutant.py
```
