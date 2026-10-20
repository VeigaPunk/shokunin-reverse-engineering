BROKEN

# Routed selftest mutation probe — author-side advisory

Revision: `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Target/citation prefix **P** = `.ufo/waves/round-18/tools/routed-defects.py`; every P:line below refers to the blob obtained by `git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/routed-defects.py`, not moving working-tree bytes. Axes: **calibration** (do not count baseline failures as kills), **operability** (bounded reproducible detector), **depth** (one substantive mutation for each of six defects). This is a detector report, not a round-admission judgment.

## Result

- **[OBSERVATION] Pristine selftest is red:** exit **1**. The closed fixture supplies only `mid_map_mismatch` (P:914-916), while the production substance check explicitly requires `mid_map_sha256_mismatch` and `mid_map_compare_mismatch` and says the placeholder was never an ID (P:277-284). The closed-fixture expectations at P:1045-1065 consequently fail.
- **[OBSERVATION] Raw green-mutant list: M01 only.** Regressing the required-ID tuple to the obsolete placeholder changes the same selftest to exit **0**, `SELFTEST: CLEAN cases=17`. Exact restoration returns exit **1** and the original diagnostics.
- **[OBSERVATION] Six single-point probes completed**, one per defect, each pristine → mutated → exact-restored. M02–M06 return the identical red diagnostics at all three stages. All stderr streams are empty.
- **Formal mutation verdict: 6 inconclusive; 0 established kills; 0 established survivors.** The failed pristine detector prevents a valid killed/survived classification. M01 is an observed green-under-regression anomaly, not a clean-baseline survival claim. The other five nonzero exits are **not** kills.
- **[INFERENCE]** The positive fixture is stale relative to the amended PINMAP requirement. Its repair is outside this read-only assignment; no fixture or lane source was repaired to make mutation scoring look conclusive. No inference about whether the real six remediations are truthful is made.

## Mutants and expected detector

The detector for every row is exactly `python3 -I -B SUBJECT --selftest`, bounded at 120 seconds, with TMPDIR inside the isolated clone. With a green pristine selftest, an intentional substantive regression should be rejected by exit 1; the prerequisite was not met here. Each row changes only the indicated expression on one line; there are no combined mutants and no selftest edits.

| ID / defect | Exact anchor at REV | Original → mutation | Property the detector should protect | Exit pristine / mutant / restored | Formal verdict |
|---|---|---|---|---|---|
| M01 / R17-PINMAP | `.ufo/waves/round-18/tools/routed-defects.py:282` | `need = ("mid_map_sha256_mismatch", "mid_map_compare_mismatch")` → `need = ("mid_map_mismatch",)` | Reject the obsolete placeholder; require both as-built finding IDs. | 1 / 0 / 1 | Inconclusive: pristine red |
| M02 / R17-VALIDATE16 | `.ufo/waves/round-18/tools/routed-defects.py:459` | `len(vs) == 64` → `len(vs) >= 1` | Require a 64-character validator digest, not any nonempty hex string. | 1 / 1 / 1 | Inconclusive: pristine red |
| M03 / R17-PRODUCER-REV | `.ufo/waves/round-18/tools/routed-defects.py:517` | `"R17-PRODUCER-REV", *PRODUCER_REVS)` → `"R17-PRODUCER-REV", *PRODUCER_REVS[:1])` | Require both pinned producer revisions in each correction line. | 1 / 1 / 1 | Inconclusive: pristine red |
| M04 / R17-SUMS-RUNLOG | `.ufo/waves/round-18/tools/routed-defects.py:587` | `carriers == hist_tsv` → `carriers.splitlines()[0] == hist_tsv.splitlines()[0]` | Compare complete historical TSV bytes, not just the header. | 1 / 1 / 1 | Inconclusive: pristine red |
| M05 / R17-REGISTRY | `.ufo/waves/round-18/tools/routed-defects.py:642` | `if not _exists(root, rev, t):` → `if False:` | Reject a scope path absent at the evaluated revision. | 1 / 1 / 1 | Inconclusive: pristine red |
| M06 / R17-S032-DIGEST | `.ufo/waves/round-18/tools/routed-defects.py:774` | `len(digests) >= 2` → `len(digests) >= 1` | Require two distinct evidence digests rather than one. | 1 / 1 / 1 | Inconclusive: pristine red |

[OBSERVATION] The existing token-only assertion checks the aggregate target flags rather than individually requiring each broken substance finding (P:1239-1243). For example, the registry negative fixture simultaneously has a too-short scope and a missing path (P:1209-1212); the S032 negative fixture removes the entire evidence file (P:1222-1224). **[INFERENCE]** Such compound negatives can mask single-check regressions; the observed red baseline means this probe cannot upgrade that concern into an established coverage-survival result.

## Commands and actual output

Scope/setup commands below all exited 0. `git show` outputs were captured, not redirected into the lane. New scratch subjects were created with the file-write tool from the exact exported bytes, mutated with the surgical-edit tool, and restored in a finally block from those bytes. The lane received only this report.

| Command (cwd when relevant) | Exit | Observed result |
|---|---:|---|
| `git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/routed-defects.py` (cwd `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`) | 0 | Pinned source printed |
| `mktemp -d /tmp/r18-routed-selftest-mut.XXXXXX` | 0 | `/tmp/r18-routed-selftest-mut.5lVBjd` |
| `git clone --no-checkout --no-local /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/r18-routed-selftest-mut.5lVBjd/repo` | 0 | Clone created |
| `git -C /tmp/r18-routed-selftest-mut.5lVBjd/repo remote remove origin` | 0 | Empty stdout/stderr; done before scratch subject writes |
| `git -C /tmp/r18-routed-selftest-mut.5lVBjd/repo show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/tools/routed-defects.py` | 0 | 60,194 source bytes captured |
| `python3 -I -B --version` | 0 | `Python 3.14.8` |
| `git --version` | 0 | `git version 2.56.0` |

The following is the complete behavioral command log, with identical outputs deduplicated as **F0** / **C0** below. Rows within each subject were executed in the stated order; independent subjects ran concurrently. To reproduce a mutant, export P from the pinned revision into an isolated /tmp clone with origin removed, create the named subject from that export, apply exactly its one replacement above, and invoke its command. Recreate pristine bytes before the restored invocation. The retained subject paths currently contain **restored**, not mutated bytes.

| Subject | Stage | Exact command | Exit | stdout |
|---|---|---|---:|---|
| Initial | initial-pristine | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/routed-defects.py --selftest` | 1 | F0 |
| M01 | pristine | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m01-pinmap.py --selftest` | 1 | F0 |
| M01 | mutated | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m01-pinmap.py --selftest` | 0 | C0 |
| M01 | restored | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m01-pinmap.py --selftest` | 1 | F0 |
| M02 | pristine | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m02-validate16.py --selftest` | 1 | F0 |
| M02 | mutated | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m02-validate16.py --selftest` | 1 | F0 |
| M02 | restored | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m02-validate16.py --selftest` | 1 | F0 |
| M03 | pristine | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m03-producer-rev.py --selftest` | 1 | F0 |
| M03 | mutated | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m03-producer-rev.py --selftest` | 1 | F0 |
| M03 | restored | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m03-producer-rev.py --selftest` | 1 | F0 |
| M04 | pristine | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m04-sums-runlog.py --selftest` | 1 | F0 |
| M04 | mutated | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m04-sums-runlog.py --selftest` | 1 | F0 |
| M04 | restored | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m04-sums-runlog.py --selftest` | 1 | F0 |
| M05 | pristine | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m05-registry.py --selftest` | 1 | F0 |
| M05 | mutated | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m05-registry.py --selftest` | 1 | F0 |
| M05 | restored | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m05-registry.py --selftest` | 1 | F0 |
| M06 | pristine | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m06-s032-digest.py --selftest` | 1 | F0 |
| M06 | mutated | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m06-s032-digest.py --selftest` | 1 | F0 |
| M06 | restored | `TMPDIR=/tmp/r18-routed-selftest-mut.5lVBjd/repo python3 -I -B /tmp/r18-routed-selftest-mut.5lVBjd/repo/m06-s032-digest.py --selftest` | 1 | F0 |

**F0 — actual stdout (one line; trailing newline):**

```text
SELFTEST: FAILED closed-fixture-cli: rc=0 opened=['R17-PINMAP', 'R17-PRODUCER-REV'] broken=['receipt-validate-mid-finding', 'producer-revs-are-ancestors']; closed-fixture-inprocess: open_count=1 broken=['receipt-validate-mid-finding']; token-only-R17-VALIDATE16: rc=0 target=(True, False, True) extra_open=['R17-PINMAP']; token-only-R17-PRODUCER-REV: rc=0 target=(True, False, True) extra_open=['R17-PINMAP']; token-only-R17-SUMS-RUNLOG: rc=0 target=(True, False, True) extra_open=['R17-PINMAP']; token-only-R17-REGISTRY: rc=0 target=(True, False, True) extra_open=['R17-PINMAP']; token-only-R17-S032-DIGEST: rc=0 target=(True, False, True) extra_open=['R17-PINMAP']
```

**C0 — actual stdout:**

```text
SELFTEST: CLEAN cases=17
```

For the green-under-regression finding, the concrete reproduction is the M01 replacement at P:282 followed by the exact M01 mutated command above (observed exit 0 / C0); unmodified and restored invocations are also recorded (exit 1 / F0). The tuple replacement and pinned source are sufficient to reproduce without relying on retained /tmp state.

## Hashes and restoration

**H = SHA-256 `034f5ead5af0bb1844f9d71c5460e9684b75f6550e820f8c2bf1d46e4de584b2`** is the exported REV blob and every pristine/restored subject. All six restored files are 60,194 bytes; direct byte comparison with the exported blob returned true for every subject, in addition to matching SHA-256. The restored detector outputs also match their pristine outputs exactly.

| Subject | Before SHA-256 | Mutated SHA-256 | After SHA-256 | Byte-identical restoration |
|---|---|---|---|---|
| M01 | H | `b5323cef47c4c51468ccd89363a7520b6cdf86809a0d2310e61491b442d39c31` | H | true |
| M02 | H | `1239d4e9a064a80709fb95ff34fa404ad9bd0043a13d4423f9b4cbd5571ed3a5` | H | true |
| M03 | H | `157ca76c5d3e5f2230d55fb0a2b7119b40639579d9dad34033476b7b17699c27` | H | true |
| M04 | H | `46029e95332bb6be1c5faf0c36119f8581aa9509f462cfdde5d9feb74fcf483d` | H | true |
| M05 | H | `cae50cc2e760364a4690edc5a47e1874721ccb7311cd1607caffd6f205c31de7` | H | true |
| M06 | H | `abdb96c91d2cc923679b5384c55e830e7e75e97a1dd5a9125917d8cf62d9e347` | H | true |

No tools installed or updated. No REA/Ghidra analysis, carrier execution, jj invocation, lane Git writes, or sibling-source edits. Only existing Python 3.14.8 and Git 2.56.0 were used for the detector. Probe complete; scratch subjects restored, no fix integrated.
