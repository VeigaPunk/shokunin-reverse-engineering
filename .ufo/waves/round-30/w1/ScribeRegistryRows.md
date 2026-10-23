# Round-30 measurement-registry rows — draft

## Scope and disposition

**[Observation]** This report drafts three `SKILL.md` registry rows in the existing five-column format. `SKILL.md` and the tool files were not edited. No carrier or mutant was executed, and no live REA measurement was run. Only `--selftest` was run for C1/C2; the oracle `--selftest` attempt was a no-op, not a test. No tools were installed.

**Static provenance:** registry shape read from `SKILL.md:948-963`; counter behavior from `tools/round-30/c1-rust-positive.py:16-25,207-267,270-351` and `tools/round-30/c2-rust-refusals.py:19-27,289-317,320-383,386-452`; oracle API from `tools/round-30/rust_dep_oracle.py:1-15,99-135`; frozen instrument hashes from `.ufo/waves/round-30/claims.json`. The selftest code paths are synthetic judgment/record fixtures; they are not evidence of a live REA run.

## Proposed row text

| Name | Kind / owner | Entry / verdict map | Self-invocation | Pinned values / write scope |
|---|---|---|---|---|
| round30-C1 | gate / kaidoku | `python3 -I -B tools/round-30/c1-rust-positive.py --root <LANE> --rev <REV>`; runs REA 6.5.0 `inspect-rust-binary` on the 16 frozen positive carriers and compares each live result with the independent `.dep-v0` oracle reading and (unless collecting evidence) the committed record. 0 iff `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`; 1 if measured but any target/entry/province/committed-record condition fails; 2 if a pinned carrier list/carrier/package input is absent or altered (including REA package version other than 6.5.0). Optional `--write-evidence` writes envelopes, stderr files and `runs.tsv`; default mode reads committed envelopes. | `python3 -I -B tools/round-30/c1-rust-positive.py --selftest`: 25 cases (17 live-envelope judge cases + 8 committed-record cases); 0 all pass, 1 any failure. Observed `selftest cases=25 failures=0`, exit 0 (2026-10-23T02:42:21Z; full output `c1-selftest.txt`). | Counter sha256 `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a`; oracle sha256 `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d`; `carriers.tsv` sha256 `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b`. C1 target covers ELF, PE and thin Mach-O carriers. Evidence collection writes under the lane's C1 evidence tree; selftest uses in-memory fixtures. |
| round30-C2 | gate / kaidoku | `python3 -I -B tools/round-30/c2-rust-refusals.py --root <LANE> --rev <REV>`; rebuilds the 19 deterministic mutants from `elf-x86_64-uvx`, runs REA 6.5.0 `inspect-rust-binary` on each and checks the frozen predictions plus the entry and SKILL row. 0 iff `mutants=19 matches=19 target=19 entry_ok=1 skill_ok=1`; 1 if measured but any target/entry/skill condition fails; 2 if mutant build/prediction/package pins fail (including REA package version other than 6.5.0). `--write-evidence` writes envelopes, stderr files and `runs.tsv`; `--build` rebuilds only. **Measure mode rewrites the shared mutants at `/fast/scratch/hyaku/kaidoku-r30/mutants` every run; only the authorized measure seat may invoke it.** | `python3 -I -B tools/round-30/c2-rust-refusals.py --selftest`: 16 cases (10 envelope-judge cases + 6 committed-record cases); 0 all pass, 1 any failure. Observed `selftest cases=16 failures=0`, exit 0 (2026-10-23T02:42:21Z; full output `c2-selftest.txt`). | Counter sha256 `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b`; `predictions.tsv` sha256 `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315`; base id `elf-x86_64-uvx` with code's SHA prefix `2e9105ad94813196`; 19 predictions frozen. Measure writes mutants to the shared scratch path even without `--write-evidence`; evidence collection additionally writes to the lane's C2 evidence tree. |
| round30-rust-dep-oracle | helper / kaidoku | No standalone measurement command or score/exit map: imported dynamically by the two counters through `load_oracle()`. API `read_file(path)` locates a single `.dep-v0` section, inflates/parses its JSON, and returns section metadata and document; `locate`, `decode` and `normalize` are the component operations. Supports ELF32/ELF64 little-endian, PE/COFF and thin 64-bit Mach-O. | No implemented `--selftest` or test-case count. The attempted command `python3 -I -B tools/round-30/rust_dep_oracle.py --selftest` exits 0 with empty stdout/stderr because this module defines no CLI/main; it runs no cases (attempt output `oracle-selftest-attempt.txt`). Oracle parse failures are raised as `OracleError` to the importing counter. | Oracle sha256 `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` (frozen in claims); module itself writes no files. |

## Selftest evidence

Each counter command below was run through `timeout 900` at the stated UTC start. Outputs are reproduced in full; process exit codes are printed by the wrapper and captured in the evidence artifacts.

### C1

Command: `timeout 900 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py --selftest`

Started: `2026-10-23T02:42:21Z`; exit: `0`.

```text
ok green-exact got=P1-pass (packages=2 edges=1)
ok green-reordered-indices got=P1-pass (packages=2 edges=1)
ok red-do-nothing got=P1-fail (envelope not ok)
ok red-nonzero-exit got=P1-fail (exit 1)
ok red-not-ok got=P1-fail (envelope not ok)
ok red-other-operation got=P1-fail (operation 'inspect_go_binary')
ok red-subject-mismatch got=P1-fail (subject sha256 'x')
ok red-null-metadata got=P1-fail (auditable_metadata count 1 or null)
ok red-empty-packages got=P1-fail (package multiset differs (rea 0, oracle 2))
ok red-empty-oracle got=P1-fail (oracle list empty)
ok red-version-differs got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-edge-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-kind-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-root-dropped got=P1-fail (package multiset differs (rea 2, oracle 2))
ok red-duplicate-package got=P1-fail (package multiset differs (rea 3, oracle 2))
ok red-offset-differs got=P1-fail (file_offset 101 != 100)
ok red-size-differs got=P1-fail (compressed_bytes 49 != 50)
ok green-committed-agrees got=True (ok)
ok red-committed-absent got=False (committed envelope absent or not added after the freeze)
ok red-committed-before-freeze got=False (committed envelope absent or not added after the freeze)
ok red-committed-same-commit-as-freeze got=False (committed envelope absent or not added after the freeze)
ok red-no-freeze-commit got=False (no freeze commit)
ok red-committed-id-differs got=False (committed evidence_id 'ev_2' != live 'ev_1')
ok red-committed-packages-differ got=False (committed metadata shape)
ok red-entry-lacks-id got=False (entry does not name ev_1)
selftest cases=25 failures=0
```

### C2

Command: `timeout 900 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py --selftest`

Started: `2026-10-23T02:42:21Z`; exit: `0`.

```text
ok green-refusal-matches got=P2-match (refused with predicted message)
ok green-acceptance-matches got=P2-match (accepted, packages=1)
ok red-do-nothing got=P2-miss (predicted message absent)
ok red-accepted-when-refusal-predicted got=P2-miss (accepted, refusal predicted)
ok red-other-message got=P2-miss (predicted message absent)
ok red-empty-predicted-message got=P2-miss (predicted message absent)
ok red-refused-when-acceptance-predicted got=P2-miss (not accepted (exit 1))
ok red-accept-wrong-packages got=P2-miss (package multiset differs)
ok red-accept-wrong-offset got=P2-miss (offset/size differ)
ok red-accept-wrong-subject got=P2-miss (subject sha256)
ok green-committed-agrees got=True (ok)
ok green-committed-refusal-agrees got=True (ok)
ok red-committed-absent got=False (committed envelope absent or not added after the freeze)
ok red-committed-before-freeze got=False (committed envelope absent or not added after the freeze)
ok red-committed-ok-differs got=False (committed ok False != live ok True)
ok red-committed-id-differs got=False (committed evidence_id differs)
selftest cases=16 failures=0
```

### Oracle `--selftest` attempt

Command: `timeout 900 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py --selftest`

Started: `2026-10-23T02:42:21Z`; stdout empty; stderr empty; exit `0`. This is **not** a passing selftest: the module has no command-line entry point or selftest implementation, so no cases ran.

## Evidence, limits, and artifacts

**[Observation]** The selftest outcomes above are the only executions. No REA CLI measurement, carrier/mutant read through the counters, or C2 measure/build invocation occurred. Thus no live C1/C2 target outcome is claimed. C2 measurement was intentionally not invoked because its default measure path rewrites shared mutant files and this item was not authorized to perform that measurement.

**[Inference, static source]** The proposed exit maps and write descriptions follow the counter source branches cited above; they were not established by a live measurement. The oracle has no native selftest. The no-op direct-execution outcome is recorded separately from the C1/C2 case counts.

The current tool and manifest hashes were observed with a `sha256sum` pass at `2026-10-23T02:42:56Z`; values used in the rows: C1 `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a`, C2 `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b`, oracle `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d`, C1 carriers `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b`, and C2 predictions `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315`. The claims file pins the three tool hashes; the manifest hashes are local-file observations.

Artifacts under `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScribeRegistryRows/` (sha256):

- `registry-rows-draft.md` — `f8dc00ac3822a8585020c5cf13af434e6f09d0ab94af75812a8629d8ef7f0b63`
- `c1-selftest.txt` — `0d54e59ab4390636bdd34f06811aeeda73b3524a5c935301afb0ce8a8adc4861`
- `c2-selftest.txt` — `a7939e151952520eb15fe6ff44d78699975ab9037f35be9f6ff41053272c82c5`
- `oracle-selftest-attempt.txt` — `2987cf1076706b5c633f07e44bd0df71a6cf82538c3cd252a9ade4ea9293be13`

No other lane file was written by this item. The sole in-lane output is this report; the SKILL registry remains unchanged for L1 integration.
