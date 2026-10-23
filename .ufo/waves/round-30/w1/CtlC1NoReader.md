# R30-C1 — CtlC1NoReader

CONTROL CtlC1NoReader met_target=no

- **Observation:** the assigned oracle-only fabrication did not meet the frozen C1 target. At sandbox commit `ed7ff19dc178872c0b1c5f842d4fd39b1badb1c6`, the unmodified counter printed `carriers=16 pass=0 target=16 entry_ok=1 (ok) province_ok=1 (ok)` and exited **1**, 2026-10-23T02:46:14Z–02:46:28Z.
- **Attack verdict: holds for this assigned control.** All 16 fabricated evidence IDs were rejected against the corresponding live REA IDs. No predicate clause let the control through. The enforcing clause is P1's requirement that the committed envelope carry the **same evidence_id** as the live run; its implementation is the equality check at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py:190-193`.
- **Mutation-testing verdict: inconclusive, not killed.** The pristine freeze revision itself exits 1 because it deliberately has no collected envelopes or entry. A failing baseline cannot establish a killed mutant. The narrower, directly observed negative-control result above is still `met_target=no`.
- **Unknown:** this single construction does not establish a general authenticity property for every possible fabricated envelope. No second mutation or contract change was attempted.

## Mutant, expected detector, and construction

Axes: frozen-detector fidelity, sandbox isolation, oracle-only construction provenance, exact byte restoration.

The sole mutation was replacing absent C1 evidence with 16 oracle-fabricated success envelopes, plus the required syntactic documentation gates. Neither counter nor oracle was edited. Sandbox only:

`/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone`

The clone initially resolved main to freeze commit `4ee65c6771058284aa947a266475839d196ed4d4`, tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2` (also captured in the pristine run receipts).

Construction commands, all successful (exit 0):

```sh
timeout 30 mkdir -p /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/tmp
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone
timeout 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/record-sources.py
timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/build-control.py
```

The constructor ran at **2026-10-23T02:45:34Z**. Its complete per-carrier receipt is `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/construction.json`. The script first verified every carrier against its frozen SHA-256, imported only the cloned independent oracle, and used `oracle.read_file()` for each carrier. It neither invoked REA nor read any detector output. For every oracle package, absent `kind`, `dependencies`, and `root` became `null`, `[]`, and `false`, respectively; package order and dependency indices were retained. Each envelope was exactly the requested shape:

```text
{ok:true,data:{operation:'inspect_rust_binary',evidence_id:'ev_'+sha256(carrier_id),subject:{digest:{sha256:frozen_sha}},normalized_result:{auditable_metadata:{packages:normalized_oracle_packages,file_offset:oracle_offset,compressed_bytes:oracle_size}}}}
```

The entry `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` began with `source: S089` and named all 16 fabricated IDs. Surgical tool edits added:

- A clearly marked junk S089 registry row in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/SOURCES.md`.
- A negative-control-only line naming `inspect-rust-binary` and the entry in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/PROVINCE.md`.
- A sandbox-control log entry in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/LOG.md`, honoring that clone's contribution rule.

All inserted prose explicitly identified the fabrication as a negative control, not domain knowledge. The exact edits and all envelopes are preserved in `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/no-reader-control.patch`.

```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone add -- /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/PROVINCE.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/LOG.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/SOURCES.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone -c user.name=ctl -c user.email=ctl@sandbox commit -m 'Control R30-C1: fabricate oracle-only no-reader envelopes'
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone log -1 --format='%H%n%T%n%cI' main
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone diff 4ee65c6771058284aa947a266475839d196ed4d4 main --output=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/no-reader-control.patch
```

Actual commit/log excerpt:

```text
[main ed7ff19d] Control R30-C1: fabricate oracle-only no-reader envelopes
 20 files changed, 130446 insertions(+)
ed7ff19dc178872c0b1c5f842d4fd39b1badb1c6
4bb70ecafd8b0b1732bd074e9de0dc344a403226
2026-10-22T23:46:05-03:00
```

Thus the control commit time was **2026-10-23T02:46:05Z**, after the freeze. **Expected detector:** reject at the committed/live evidence-ID equality check, despite syntactically valid entry/province gates and oracle-correct package contents.

## Exact counter and run records

Every invocation used this identical detector command, with cwd `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader`, TMPDIR `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/tmp`, and GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset:

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone --rev main
```

The recorder command was:

```sh
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/tmp python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/run-counter.py LABEL
```

`LABEL` was, in order, `pristine`, `pristine-ready`, `mutated`, and `restored`. These are recorder labels, not detector arguments. The recorder preserves the actual counter exit code separately; its own successful recording exit was 0. It bounds the entire process group, has an unused 880-second emergency cleanup deadline inside the 900-second command bound, and records before/after file hashes. None of these short runs reached a timeout. All four counter stderr files were empty.

### Initial untouched-clone run: PIN-blocked

**Observation, 2026-10-23T02:43:31Z–02:43:31Z; counter exit 2.** Full counter stdout:

```text
PIN carrier elf-x86_64-uv absent or altered at /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uv
```

This run was inconclusive and did not reach REA. The blocker was reported to L1. **I did not alter any shared carrier.** L1 subsequently reported restoring four altered shared carriers from verified wheel members and applying immutable protection. The identity of that writer is **unknown to this seat**. The successful pin phase of the following runs, not an assumption about the restoration, is the basis for their interpretation.

### Untouched-clone rerun after the shared-input repair

**Observation, 2026-10-23T02:45:05Z–02:45:18Z; counter exit 1.** Revision `4ee65c6771058284aa947a266475839d196ed4d4`. Full counter stdout:

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
carriers=16 pass=0 target=16 entry_ok=0 (entry absent at rev) province_ok=0 (no PROVINCE line names inspect-rust-binary with the entry)
```

### Mutated, committed no-reader control

**Observation, 2026-10-23T02:46:14Z–02:46:28Z; counter exit 1.** Revision `ed7ff19dc178872c0b1c5f842d4fd39b1badb1c6`. Full counter stdout:

```text
elf-x86_64-uv	P1-fail	committed evidence_id 'ev_b4d17e4c30c3de7d6e14cb71a9af05c2dacbf24251ff88a84428a349f85b021b' != live 'ev_ef18bd88be10acda35b48cd1675299c0e27b643c5e24acbd0a2700ea3f6a0b33'
elf-x86_64-uvx	P1-fail	committed evidence_id 'ev_5feaa6b3be12bf1de57c66e248bb74c7847a312b3283611cf1bbbe31135b11f2' != live 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e'
elf-aarch64-uv	P1-fail	committed evidence_id 'ev_5d93090a6e4f39150eb3fc1509aa0582e5ea4d5e64b9d84f5a332c9519cdc551' != live 'ev_1506350fdcaad3573291668df01a30fb30dbdba545c2a20ad4d09ec927c8d40e'
elf-aarch64-uvx	P1-fail	committed evidence_id 'ev_b048cf03556e95a247f27c8963b5f6227036e92f81449b574585af4e5eaf6e8e' != live 'ev_5aa17b13d4b1dbdcc4ff03b7abacef14203776cfc504c64fb252473c1e2c38d8'
elf-riscv64-uv	P1-fail	committed evidence_id 'ev_c84856c365595673abc91f7231b6e1c3075777c148be572dacc33ff73a053d27' != live 'ev_6fb2c5354740d93ceb96e5c98b807d84bd02bbace617b93e88498eda90e7a371'
elf-riscv64-uvx	P1-fail	committed evidence_id 'ev_136054e9fa4d6ff3ee99df49b651bb98824678b71321cd6b537a84907ce286e6' != live 'ev_3b6453525097133d138ae225eee86e46af8403b17648dfda4f70abc045ff80bc'
pe-x86_64-uv	P1-fail	committed evidence_id 'ev_a0d7c04d77acf1917529e6d3e3325289eb0845cbed70b452ada546978ba3337b' != live 'ev_3cb29ace54adb615cf4cf9495ae753a12fd8240fd6b82b5cdc34e57c85449943'
pe-x86_64-uvx	P1-fail	committed evidence_id 'ev_64f5d29ce9984d33723cf6d442702da99b921f7a44185cc617e92ae709b15a97' != live 'ev_eaf76ad92d83fa393039570cb113b16120e3369332b6444f39e9f79540351863'
pe-x86_64-uvw	P1-fail	committed evidence_id 'ev_12b32b7c6c099c22da7b371756e5d7f91eaea35eee45e9f6e1a7d79c94b5966a' != live 'ev_ab1b78ca69fdcd71cb69faed3557e2f5794c94e37b8f33aea5c35728713288b2'
pe-arm64-uv	P1-fail	committed evidence_id 'ev_f874c628fddb9f821e5b9232bfb508e834c2a653bce3171e929b000ed8318e07' != live 'ev_58d8e1f477c5dff8801fe1a2d6f6b81a9c26d69b1f09d0c4904c59d3ef86697e'
pe-arm64-uvx	P1-fail	committed evidence_id 'ev_e1b76075526e01dfeaad368213299a0ac8b60651ce70b3d5138319f74fd5f1d8' != live 'ev_ae58e67e96e716244041cb0292221bdeab86ef5731f890ad25b2bab9177ab7dc'
pe-arm64-uvw	P1-fail	committed evidence_id 'ev_bc7943a0c40947fa1c1ea0d80bf3ab95b4d7cabaef99db8e6a993c133ff3828b' != live 'ev_6f00915a36c933a68fa819f36977f7085b980b7b2ffec1997a5bea93c51defc9'
macho-x86_64-uv	P1-fail	committed evidence_id 'ev_b332b23e5a2549e76ece845281fad1227e4d4a9adf0f3ab55a550a68a13c378d' != live 'ev_1c3ef6996f8f62f1eeffda94f2b5892763eda8b2f4a333c01311a11bf0c6af10'
macho-x86_64-uvx	P1-fail	committed evidence_id 'ev_43bf696f1036ce885ae7f5a365d4aecd7e32b0f3e79fadc6ef1085466d2154a8' != live 'ev_02fb9f95c9b82c4a6ade2ea299e4fe85e193f821d406fa76feb0cfec709177b0'
macho-arm64-uv	P1-fail	committed evidence_id 'ev_88ab3131d98e7e8a5b7b639515d2a74785c3a1158a9f17d0e3d7aa469917d84e' != live 'ev_7f9ac67aa01cc62f2a0a8d0d4bd50f34fd195523eaf73a6560ceb4b313b9b35d'
macho-arm64-uvx	P1-fail	committed evidence_id 'ev_30e04c854cfe542d7b8711be75b4d5df3ea054d762ffaaa9af543c7126a50157' != live 'ev_6fcab3d46593ceb4056e5b67c540119f6fbdd113a79661462819e5317e3687f7'
carriers=16 pass=0 target=16 entry_ok=1 (ok) province_ok=1 (ok)
```

**Inference from the observed reasons and the unchanged counter's control flow:** the live first-half metadata checks succeeded for all 16 carriers; only then does it call the committed-record check. The junk source row and negative-control province line satisfied the two syntactic gates, but could not compensate for the evidence-ID mismatches. This is not a green mutation baseline.

### Restored-byte run

Restoration command, exit 0, **2026-10-23T02:46:41Z**:

```sh
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone -c user.name=ctl -c user.email=ctl@sandbox revert --no-edit ed7ff19dc178872c0b1c5f842d4fd39b1badb1c6
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone log -1 --format='%H%n%T%n%cI' main
```

Actual output excerpt:

```text
[main 511cb2a6] Revert "Control R30-C1: fabricate oracle-only no-reader envelopes"
 20 files changed, 130446 deletions(-)
511cb2a6d0971e9bafd64edecdc0eef5f17906be
ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2
2026-10-22T23:46:41-03:00
```

**Observation, 2026-10-23T02:46:45Z–02:46:59Z; counter exit 1.** Same detector command, restored tree. Full counter stdout:

```text
elf-x86_64-uv	P1-fail	committed envelope not ok
elf-x86_64-uvx	P1-fail	committed envelope not ok
elf-aarch64-uv	P1-fail	committed envelope not ok
elf-aarch64-uvx	P1-fail	committed envelope not ok
elf-riscv64-uv	P1-fail	committed envelope not ok
elf-riscv64-uvx	P1-fail	committed envelope not ok
pe-x86_64-uv	P1-fail	committed envelope not ok
pe-x86_64-uvx	P1-fail	committed envelope not ok
pe-x86_64-uvw	P1-fail	committed envelope not ok
pe-arm64-uv	P1-fail	committed envelope not ok
pe-arm64-uvx	P1-fail	committed envelope not ok
pe-arm64-uvw	P1-fail	committed envelope not ok
macho-x86_64-uv	P1-fail	committed envelope not ok
macho-x86_64-uvx	P1-fail	committed envelope not ok
macho-arm64-uv	P1-fail	committed envelope not ok
macho-arm64-uvx	P1-fail	committed envelope not ok
carriers=16 pass=0 target=16 entry_ok=0 (entry absent at rev) province_ok=0 (no PROVINCE line names inspect-rust-binary with the entry)
```

**Observation:** bytes were restored exactly, but Git history retains the control and its revert. **Inference:** that retained add-history explains why the restored run reaches `committed envelope not ok`, rather than the pristine run's earlier add-time failure. No assertion of identical Git history is made.

## Before/mutated/restored hashes

The recorder captured these file hashes before and after each run. The pristine and restored tree IDs are both `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`; the control tree was `4bb70ecafd8b0b1732bd074e9de0dc344a403226`.

| Absolute sandbox file | Pristine SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/PROVINCE.md` | `4f94007f80be8b87fb4645b366a6e4a695f330da96bdf2dc058ab046db9d1e32` | `4610d694d14c2d378c86ac090af8ac29e661e84496a13929a94ecd09b2d0c5d3` | `4f94007f80be8b87fb4645b366a6e4a695f330da96bdf2dc058ab046db9d1e32` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/LOG.md` | `fe337ccb6688b03657405c377c704d6aa354c3975b3176fef9e9e4c678177f32` | `6b8e79b09c0c9e76da963ca7bdf8b1116158349b37cfe3dab72cf2e41595c0d3` | `fe337ccb6688b03657405c377c704d6aa354c3975b3176fef9e9e4c678177f32` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/SOURCES.md` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` | `151b69721ee0f8f395a0c8917be1f60a7ab985c201ee8487fe2b1688f085e8ad` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` | absent | `29e57eac7d3ab5cc33d08170ab5b1aab489ff5218dd1afc8e62528561bc543f1` | absent |

All 16 envelope paths below were **absent before and absent after restoration**. Their mutated-byte SHA-256 values are retained in the construction receipt, mutant-run receipt and complete patch:

| Absolute envelope path at control commit | Mutated SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uv.json` | `3901ce5503cea02a37cab642f67978ab92dcc1a4d7efc4f10023b3985605fb95` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uvx.json` | `a7c353efdce391131b8e67454534a2a3a540c61426912d718a8fa1ec17640311` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uv.json` | `e9a214a161d27f4d7b50bbe67f434ef41cf6d043eece155bce9b7514ee2a8d55` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uvx.json` | `2f949cff91eb56509d2b3c7994469db8629c3bff203e3a9f2babf41cd6d6a31c` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uv.json` | `1e1cf78b2246690cf7c6b77863092bc2a09e81ad158cfcd8800ea790346aa6c8` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uvx.json` | `6a814532325bf46b21733c198475514f1ebbd2905b18cd71260380ee647b0134` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uv.json` | `82bad6a9c1787cca362addda1a1dcf05642f5f2d6d5b8d55b6a90b6d0bf7e09d` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvx.json` | `b7d8e98124b68963148db5101500cd298a862f9d9378fabb9938a466f31c9b46` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvw.json` | `b91c43cdb78445801897872e6218760a7701849586f45d53eb3f41adc00a3f72` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uv.json` | `755d7f5a6207d0058f21b37377449fd8cfadbfde2b425ba86c80c2a0e36fa8bd` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvx.json` | `847065c646382f790d1f9e684e1b666adb5ec1023828a15fe6006e1e8f7f98d0` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvw.json` | `f1f7a97d3e733caf492b0f61dd681db11870fab962a6b86304ce037c62001aee` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uv.json` | `2ce5a84147aa5749f94882453288084fe51099adfb7609c018f9c84adf3ae02f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uvx.json` | `f461f35ead32c122b4a64e97f10880f4eacdd502b7b6564c6cf5ffc29494014d` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uv.json` | `a6c284305d90ebe4cc86f1db219c2e5ff2ec5605f781211bb63c5c600538d358` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uvx.json` | `1f4a90867e3dd0ad358c698b896c6fedd0dfd102775df3df1f0e47e00926b2b8` |

The counter, oracle, carrier TSV and claims-file hashes were unchanged in every before/after snapshot. Their hashes appear in the receipts and source registry below. No lane Git/index/jj write occurred; only this report was written inside the lane. No carrier or mutant was executed, and no C2 measure-mode counter was run.

## Opened sources

Ordinary local reads only; **access date 2026-10-23** for every row. Quotes are at most 25 contiguous words. `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/sources.json` was produced at 2026-10-23T02:45:34Z and preserves these URLs, byte hashes and located quotations. Binary carrier input hashes are separately recorded for all 16 members in the construction receipt and frozen TSV; no external source URL embedded in the pre-existing source registry was fetched.

| Source URL | SHA-256 | Located quote |
|---|---|---|
| `file:///home/vgpnk/.agents/skills/godspeed/SKILL.md` | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | line 2: `name: godspeed` |
| `file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md` | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | line 2: `name: reverse-engineer-anything` |
| `file:///home/vgpnk/.omp/agent/RULES.md` | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | line 3: `Any agent — main session or subagent, any lane, any wave — installs or updates any tool that` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py` | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | line 193: `committed evidence_id %r != live %r` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py` | `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d` | line 3: `Shares no code with REA. It parses the container section tables itself` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json` | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | line 16: `carriers=16 pass=16 target=16 entry_ok=1 province_ok=1, exit 0` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv` | `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b` | line 2: `elf-x86_64-uv` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/AGENTS.md` | `9536078c8b28917ca2ec9ae55a6396d53fa24056b46606803d80b22463d87730` | line 5: `Never fabricate domain knowledge: cite a file, a command output, or a source.` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/corpus/SOURCES.md` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` | line 3: `## Registry` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/PROVINCE.md` | `4f94007f80be8b87fb4645b366a6e4a695f330da96bdf2dc058ab046db9d1e32` | line 38: `## Core` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/clone/LOG.md` | `fe337ccb6688b03657405c377c704d6aa354c3975b3176fef9e9e4c678177f32` | line 1: `# kaidoku-shokunin — Iteration Log` |

## Retained artifact inventory

SHA-256 values below were produced by a bounded `timeout 30 sha256sum` command over the listed absolute files. The control patch preserves every changed byte; the clone retains the control commit and its restoration commit. Only the seat's disposable Node compile cache was removed, not any raw output or control evidence.

| Absolute artifact | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/run-counter.py` | `cee966cf47531b5e9fbe360158b2409dcdcef3c86627af98aaf94098fd229730` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/build-control.py` | `319bd2d24314bc46f145726ee1c86d320925000d2dc163ef6aa315e0053d72bd` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/record-sources.py` | `d49637025f577719121760ccde5242a1755cfebd8cb03f47e9527fd597984d30` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/sources.json` | `b8b3629ab2ed00318ea26c7df211b48659b401cd60e49ca0896c0c26db5ac87a` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/construction.json` | `4d40149e14b57f4cd2c5add6f652b24798c8bca624443b16854ebe1e407c2f89` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/no-reader-control.patch` | `db2e3e7acb3e317412dd4ebf83cd546b98aa4b163907772febcadc22c1032e42` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/pristine.stdout` | `7ae1b93ea7d012ac3b6b5b607982198119a610c5b3de8c8c30077116278bd0d6` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/pristine.receipt.json` | `372adf6b37f675dde7fdb2c78c89b4aa38f7e229a8b614df2a4b4ce50b76884e` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/pristine-ready.stdout` | `afa4cc794aad76161a1570f46fde93e024585c61a98b441dbf216124bceba98b` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/pristine-ready.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/pristine-ready.receipt.json` | `81e22e1b32bb596af102a4e6392c92641d9038f2ca1989d19328717b6aea661f` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/mutated.stdout` | `f4fa88b0261c4ff893725eca503f4de75bf20181cb3c5c923d18adf288072b77` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/mutated.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/mutated.receipt.json` | `49ac0309b8e53b8b42a0960a38766f75195bbc903c4f515a40389b160f6107b4` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/restored.stdout` | `06e640bd4b5f511bcfb33fe02ab89226cbd43aeabe3aae6636304d8ee308bd04` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1NoReader/restored.receipt.json` | `d907bfa67d4c294256f7ffc3945f41a1a24201e8d60e56539f3761e321627de8` |

**Tooling/process observations:** no installation or update was performed by this seat; the assigned counter used the existing pinned `rea-agents@6.5.0` npx installation. No pacman transaction, service, MCP device, alternate REA version, or subagent was used. All four recorder receipts report `cleanup: process group absent`; no started process tree remained after a run. Only the prescribed bounded detectors were exercised; no build, formatter, unrelated test, integration, or shipping action was performed.

Report: .ufo/waves/round-30/w1/CtlC1NoReader.md
