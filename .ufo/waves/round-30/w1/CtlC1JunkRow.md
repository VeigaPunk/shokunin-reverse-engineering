# R30-C1 pre-data control: junk-row

CONTROL junk-row met_target=no

**Attack verdict: holds.** The committed junk entry, PROVINCE marker and S089 registry row satisfied both auxiliary gates, but the measured control passed **0/16** carriers and exited **1**. The first attempt was PIN-blocked and is not counted as a successful negative-control measurement.

Axes: frozen C1 coverage; evidence/provenance integrity; resistance to keyword/registry-only saturation. This report is a control receipt, not collected claim evidence or a canonical judgment.

## Construction

Sandbox: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone`.

The clone command exited 0 with no stdout:

```sh
timeout 10 mkdir -p /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow && timeout 90 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone
```

**Observation:** at `2026-10-23T02:42:16Z`, `timeout 10 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD refs/heads/main`, run in the sandbox, exited 0 and printed:

```text
4ee65c6771058284aa947a266475839d196ed4d4
4ee65c6771058284aa947a266475839d196ed4d4
```

Using the edit/write tools, made precisely these sandbox changes:

- Appended line 329 to `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/PROVINCE.md`:
  `JUNK inspect-rust-binary corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`
- Created `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` with these complete, newline-terminated contents:

  ```text
  source: S089
  junk
  ```

- Appended line 178 to `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/SOURCES.md`:
  `| S089 | junk |`

S089 here is deliberately junk, not a provenance claim. No envelopes were created or committed. Neither counter invocation used `--write-evidence`.

Executed these commands, with Git environment variables unset:

```sh
timeout 10 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone add -- /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/PROVINCE.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/SOURCES.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: R30-C1 junk-row without envelopes'
timeout 10 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone rev-parse HEAD
```

**Observation:** the construction pipeline exited 0 during `2026-10-23T02:43:17Z`–`2026-10-23T02:43:18Z`. Exact commit output:

```text
[main d6840942] control: R30-C1 junk-row without envelopes
 3 files changed, 4 insertions(+)
 create mode 100644 corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md
d68409425d39ab582c061c679e6f468592d5458f
```

**Sandbox commit:** `d68409425d39ab582c061c679e6f468592d5458f`, on `main`, unchanged between measurements. Complete construction commands and tool-edit contents are retained in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/construction.txt`.

An untouched-state counter comparison was unnecessary: the assigned question is whether this committed junk-only control reaches the frozen target.

## Exact counter command

Working directory: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow`.

```sh
timeout 900 python3 -I -B clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone --rev main
```

Both runs used this exact argv. The capture wrapper removed `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` from the inherited environment, and set `TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/tmp`. Its capture deadline did not fire in either run. It kills its spawned process group on completion; no persistent service was started.

Capture commands:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/run-control.py
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/run-control.py rerun
```

The wrapper was amended between runs only to allow a separate output-file prefix, preserving the initial receipt.

## Run 1: PIN-blocked

**Observation:** `2026-10-23T02:43:46Z`–`2026-10-23T02:43:47Z`; counter exit **2**. Full counter stdout:

```text
PIN carrier elf-x86_64-uv absent or altered at /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uv
```

Full counter stderr: empty (0 bytes).

**Conclusion — observation:** this run did not reach measurement and cannot establish whether the junk-row attack is rejected by P1.

L1 subsequently reported restoring four altered shared carriers and making all 16 immutable, and explicitly requested a rerun. That restoration and writer attribution are L1-reported, not independently established by this seat. **This seat was not the writer:** it never wrote a shared carrier or mutant, changed their permissions/flags, or executed any carrier/mutant. Carrier interactions were read-only counter inspection plus `stat`/`sha256sum` diagnostics.

## Run 2: measured negative control

**Observation:** `2026-10-23T02:44:52Z`–`2026-10-23T02:45:07Z`; counter exit **1**. Full counter stdout:

```text
elf-x86_64-uv	P1-fail	committed envelope absent or not added after the freeze
elf-x86_64-uvx	P1-fail	committed envelope absent or not added after the freeze
elf-aarch64-uv	P1-fail	committed envelope absent or not added after the freeze
elf-aarch64-uvx	P1-fail	committed envelope absent or not added after the freeze
elf-riscv64-uv	P1-fail	committed envelope absent or not added after the freeze
elf-riscv64-uvx	P1-fail	committed envelope absent or not added after the freeze
pe-x86_64-uv	P1-fail	committed envelope absent or not added after the freeze
pe-x86_64-uvx	P1-fail	committed envelope absent or not added after the freeze
pe-x86_64-uvw	P1-fail	committed envelope absent or not added after the freeze
pe-arm64-uv	P1-fail	committed envelope absent or not added after the freeze
pe-arm64-uvx	P1-fail	committed envelope absent or not added after the freeze
pe-arm64-uvw	P1-fail	committed envelope absent or not added after the freeze
macho-x86_64-uv	P1-fail	committed envelope absent or not added after the freeze
macho-x86_64-uvx	P1-fail	committed envelope absent or not added after the freeze
macho-arm64-uv	P1-fail	committed envelope absent or not added after the freeze
macho-arm64-uvx	P1-fail	committed envelope absent or not added after the freeze
carriers=16 pass=0 target=16 entry_ok=1 (ok) province_ok=1 (ok)
```

Full counter stderr: empty (0 bytes).

Frozen target: `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1`, exit 0. **NOT MET.**

## Counterexample, impacted axes, smallest safe correction

- **Counterexample attempted:** a committed, semantically empty entry plus keyword/path marker and junk S089 row, with no envelopes. The measured stdout above is the producing evidence (same exact command, exit 1, UTC interval above).
- **Observation:** both `entry_ok=1 (ok)` and `province_ok=1 (ok)` accept this junk. They are syntactic gates, not independent proof of learned coverage or valid provenance.
- **Inference from that stdout and counter lines 182–204, 241–250:** the mandatory post-freeze committed-envelope clause prevented false saturation. Every carrier was downgraded for `committed envelope absent or not added after the freeze`. The code emits that reason only after a live run passes the live/oracle checks; raw live envelopes were intentionally not retained as claim data.
- **Impacted axes:** coverage would be falsely saturated if marker/registry checks were treated as sufficient; evidence integrity remains protected by the full P1 conjunction in this tested control.
- **Smallest safe correction:** none to the frozen counter for this attack. Preserve the mandatory committed-envelope check; do not promote the two auxiliary booleans into a standalone success criterion. No predicate clause let the control reach the full target. This receipt makes no claim about other controls or the semantic quality of a future evidence-backed entry.

## Retained artifacts and SHA-256

Hashes were produced with `timeout 30 sha256sum` over the absolute paths below; exit 0 at `2026-10-23T02:45:50Z` for capture/construction artifacts and at `2026-10-23T02:44:05Z` for the three constructed clone files. The sandbox clone itself is identified by the full commit above; inherited repository files are not new seat artifacts. Incidental Node compile-cache files under the private temporary directory were removed (cleanup exit 0).

| Absolute path | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/construction.txt` | `f1c4da87ffd88242f74520cd7741aedc416d8376a1b36c5b632b2bbf03dd1b4d` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/run-control.py` | `cf4af924d1b5eb12364f79df69e814754902904f12b5404fa55b72d46aff343a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/counter.stdout` | `7ae1b93ea7d012ac3b6b5b607982198119a610c5b3de8c8c30077116278bd0d6` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/counter.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/counter.receipt.json` | `9e969fd87a95a895fccea0d6e0d76c3ae703437b024f02d62de9927c8815ba47` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/rerun.stdout` | `5a623e1198986fbc5d5f9443dfdeeecb66fc8cccfcb0752adf9fe3632823a239` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/rerun.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/rerun.receipt.json` | `a0b0420118e82627cdd8d59bf03f71c255bc4462edc29f2032a719bd3e20b3cb` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/PROVINCE.md` | `b0ab34d984ad7fce7e325281bc723d197c8e9594fb30164c0b37e28e9214f069` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/SOURCES.md` | `96a85ae6b9422046107d75dbd56582ba9e5108f3a1e6fa3de297fb8019e5c863` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` | `cdcd81f2e1ac61fd35b3dc34cd4adbff9632103cc8ac3c2ac41adcd0bd281113` |

## Opened primary/local evidence sources

All accessed **2026-10-23**, by ordinary local file reads; hashes identify complete file bytes. No external source page was opened. Each quote is at most 25 contiguous words.

| URL | SHA-256 | Located quote |
|---|---|---|
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/tools/round-30/c1-rust-positive.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | L187: `return False, "committed envelope absent or not added after the freeze"` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/.ufo/waves/round-30/claims.json` | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | L16: `"target": "carriers=16 pass=16 target=16 entry_ok=1 province_ok=1, exit 0",` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/evidence/round-30/c1/carriers.tsv` | `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b` | L2: `elf-x86_64-uv` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/PROVINCE.md` | `b0ab34d984ad7fce7e325281bc723d197c8e9594fb30164c0b37e28e9214f069` | L329: `JUNK inspect-rust-binary corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/SOURCES.md` | `96a85ae6b9422046107d75dbd56582ba9e5108f3a1e6fa3de297fb8019e5c863` | L178: `\| S089 \| junk \|` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1JunkRow/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` | `cdcd81f2e1ac61fd35b3dc34cd4adbff9632103cc8ac3c2ac41adcd0bd281113` | L1: `source: S089` |

Operational instructions also opened, same access date:

| URL | SHA-256 | Located quote |
|---|---|---|
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | L2: `name: godspeed` |
| `file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | L2: `name: reverse-engineer-anything` |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | L1: `# Tooling directive — operator, 2026-10-19 (always on, every agent)` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/AGENTS.md` | `9536078c8b28917ca2ec9ae55a6396d53fa24056b46606803d80b22463d87730` | L1: `# kaidoku-shokunin operating rules` |

Tool installs/updates: no install/update command was issued by this seat. The counter invoked its prescribed `npx -y rea-agents@6.5.0` CLI. No extra REA run, carrier execution, subagent, lane/index write, fleet mutation, or unrelated verification was performed. The only lane file written by this seat is this scoped report.
