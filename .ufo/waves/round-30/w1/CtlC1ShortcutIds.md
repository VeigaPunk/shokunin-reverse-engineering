# R30-C1 pre-data control — shortcut keyed on ids

CONTROL CtlC1ShortcutIds met_target=no

**Attack:** copy one genuine REA envelope unchanged under all 16 frozen carrier ids, then satisfy the entry/source/PROVINCE existence gates.

**Verdict: holds.** The frozen counter rejects the clean shortcut: `carriers=16 pass=1 target=16 entry_ok=1 (ok) province_ok=1 (ok)`, exit 1. This is a control observation, not a canonical claim judgment or admission.

**Impacted axes:** C1 coverage; evidence identity/provenance integrity. C2 depth was not exercised.

## Construction and boundaries

[Observation] The isolated clone began at `4ee65c6771058284aa947a266475839d196ed4d4`, on main. The `clone_initial` command below returned exactly:

```text
4ee65c6771058284aa947a266475839d196ed4d4
2026-10-22T23:35:13-03:00
HEAD -> main, origin/main, origin/HEAD
```

The clone was created with:

```sh
timeout 900 mkdir -p /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/tmp && timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone
```

[Observation] Construction performed only these sandbox content changes:

- The construction scripts copied the complete, unmodified CLI stdout bytes to all 16 envelope filenames from the frozen carrier list. They did not fabricate metadata, change evidence ids or rewrite subject hashes.
- Created /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md, first line exactly `source: S089`, naming only the single seed evidence id.
- Inserted the following PROVINCE control row in /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/PROVINCE.md:

```text
| inspect-rust-binary (CONTROL ONLY) | One envelope copied under all 16 carrier ids | Deliberately insufficient sandbox shortcut | corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md |
```

- Inserted the following deliberately junk source row in /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/SOURCES.md; it is not a primary authority:

```text
| S089 | junk shortcut control row; no primary authority | control | none | adversarial sandbox only | none | no source claim | control | 2026-10-23 | never | corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md |
```

Relative names inside those literal test rows are the counter's required repository-relative strings, not additional filesystem destinations.

[Observation] Sandbox commits, from the commit commands' actual stdout:

```text
[main f795e1dc20f4eecd4866466d600f1d8f59835ac4] control: reuse one Rust envelope under all carrier ids
[main b35e673e0471439ae0e9522bf0580b5df3904a08] control: seed shortcut ids from restored frozen carrier
```

Both commits used `user.name=ctl`, `user.email=ctl@sandbox`; no lane/fleet Git or jj writes were performed. No carrier or mutant was executed. **I did not alter any carrier.** All generated evidence and scripts are in the assigned scratch directory; the only lane write is this report. No standalone baseline counter was needed or run.

## Contamination and its completed correction

[Observation] The original allowed seed call ran at 2026-10-23T02:42:42Z–02:42:43Z, exit 0. Its actual envelope had:

```text
"evidence_id": "ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33"
"sha256": "9f41e2d43ca085f1200cd52f1856fa3e821a05942a90d8084122a9ad9ef903a1"
```

The independent `carrier_sha` command at 2026-10-23T02:43:47Z, exit 0, returned exactly:

```text
9f41e2d43ca085f1200cd52f1856fa3e821a05942a90d8084122a9ad9ef903a1  /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

That differs from the frozen source digest `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d`. The first construction attempt consequently stopped with `AssertionError` (2026-10-23T02:43:18Z, exit 1) before creating any envelope file. The subsequent construction retained and explicitly recorded the discrepancy, copied the genuine output without modification, and committed the contaminated control as f795e1dc20f4eecd4866466d600f1d8f59835ac4.

[Observation of L1 instruction] L1 reported carrier restoration and immutability, and explicitly authorized **one additional standalone REA call** on the restored source, rebuilding, recommitting and recounting. The writer responsible for the earlier carrier alteration remains [Unknown]; this seat did not investigate its identity.

[Observation] The contaminated control counter run passed the pinned-input checks and measured all 16 carriers, but rejected all 16 committed evidence ids. It was not a PIN-blocked run. No pre-restoration/PIN-blocked counter was run by this seat, so no such stdout or exit code is invented below.

[Observation] The authorized clean seed call at 2026-10-23T02:46:06Z, exit 0, produced evidence id `ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e` with subject SHA-256 exactly equal to the frozen source digest. Its raw stdout SHA-256 is `847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a`. The clean builder copied those exact bytes under all 16 ids and changed the entry's single named id accordingly. The clean sandbox commit is b35e673e0471439ae0e9522bf0580b5df3904a08.

## Exact commands and execution receipts

[Observation] Commands below were run from /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds. The receipt runner sets `TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/tmp` and unsets GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE for every child (including the counter's Git children). UTC times and exit codes are captured in the named JSON receipts. Both counter runs used the unchanged frozen instrument, in measure mode, without `--write-evidence`.

### clone_initial

UTC 2026-10-23T02:42:42+00:00–2026-10-23T02:42:42+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py clone_initial timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone show -s --format=%H%n%cI%n%D main
```

### rea_once

UTC 2026-10-23T02:42:42+00:00–2026-10-23T02:42:43+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py rea_once timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx --format json --full-output
```

### construction

UTC 2026-10-23T02:43:18+00:00–2026-10-23T02:43:18+00:00; exit **1**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py construction timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/build_control.py
```

### carrier_sha

UTC 2026-10-23T02:43:47+00:00–2026-10-23T02:43:47+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py carrier_sha timeout 60 sha256sum /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

### construction_ok

UTC 2026-10-23T02:43:47+00:00–2026-10-23T02:43:47+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py construction_ok timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/build_control.py
```

### git_stage

UTC 2026-10-23T02:44:23+00:00–2026-10-23T02:44:23+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py git_stage timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone add -- PROVINCE.md corpus/SOURCES.md corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md corpus/evidence/round-30/c1/envelopes
```

### git_commit

UTC 2026-10-23T02:44:23+00:00–2026-10-23T02:44:23+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py git_commit timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone -c user.name=ctl -c user.email=ctl@sandbox -c core.abbrev=40 commit --no-gpg-sign -m 'control: reuse one Rust envelope under all carrier ids'
```

### source_inventory

UTC 2026-10-23T02:44:58+00:00–2026-10-23T02:44:58+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py source_inventory timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/source_inventory.py
```

### c1_after_restore

UTC 2026-10-23T02:44:58+00:00–2026-10-23T02:45:12+00:00; exit **1**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py c1_after_restore timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone --rev main
```

### rea_clean

UTC 2026-10-23T02:46:06+00:00–2026-10-23T02:46:06+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py rea_clean timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx --format json --full-output
```

### construction_clean

UTC 2026-10-23T02:46:19+00:00–2026-10-23T02:46:19+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py construction_clean timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/build_clean_control.py
```

### git_stage_clean

UTC 2026-10-23T02:46:31+00:00–2026-10-23T02:46:31+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py git_stage_clean timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone add -- corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md corpus/evidence/round-30/c1/envelopes
```

### git_commit_clean

UTC 2026-10-23T02:46:31+00:00–2026-10-23T02:46:31+00:00; exit **0**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py git_commit_clean timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone -c user.name=ctl -c user.email=ctl@sandbox -c core.abbrev=40 commit --no-gpg-sign -m 'control: seed shortcut ids from restored frozen carrier'
```

### c1_clean

UTC 2026-10-23T02:46:48+00:00–2026-10-23T02:47:02+00:00; exit **1**.

```sh
timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py c1_clean timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone --rev main
```

## Full counter stdout — contaminated seed

Measured revision: f795e1dc20f4eecd4866466d600f1d8f59835ac4 (`main` at that run). UTC 2026-10-23T02:44:58Z–02:45:12Z. Exit **1**; stderr empty; target **not met**.

```text
elf-x86_64-uv	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_ef18bd88be10acda35b48cd1675299c0e27b643c5e24acbd0a2700ea3f6a0b33'
elf-x86_64-uvx	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e'
elf-aarch64-uv	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_1506350fdcaad3573291668df01a30fb30dbdba545c2a20ad4d09ec927c8d40e'
elf-aarch64-uvx	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_5aa17b13d4b1dbdcc4ff03b7abacef14203776cfc504c64fb252473c1e2c38d8'
elf-riscv64-uv	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_6fb2c5354740d93ceb96e5c98b807d84bd02bbace617b93e88498eda90e7a371'
elf-riscv64-uvx	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_3b6453525097133d138ae225eee86e46af8403b17648dfda4f70abc045ff80bc'
pe-x86_64-uv	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_3cb29ace54adb615cf4cf9495ae753a12fd8240fd6b82b5cdc34e57c85449943'
pe-x86_64-uvx	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_eaf76ad92d83fa393039570cb113b16120e3369332b6444f39e9f79540351863'
pe-x86_64-uvw	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_ab1b78ca69fdcd71cb69faed3557e2f5794c94e37b8f33aea5c35728713288b2'
pe-arm64-uv	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_58d8e1f477c5dff8801fe1a2d6f6b81a9c26d69b1f09d0c4904c59d3ef86697e'
pe-arm64-uvx	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_ae58e67e96e716244041cb0292221bdeab86ef5731f890ad25b2bab9177ab7dc'
pe-arm64-uvw	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_6f00915a36c933a68fa819f36977f7085b980b7b2ffec1997a5bea93c51defc9'
macho-x86_64-uv	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_1c3ef6996f8f62f1eeffda94f2b5892763eda8b2f4a333c01311a11bf0c6af10'
macho-x86_64-uvx	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_02fb9f95c9b82c4a6ade2ea299e4fe85e193f821d406fa76feb0cfec709177b0'
macho-arm64-uv	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_7f9ac67aa01cc62f2a0a8d0d4bd50f34fd195523eaf73a6560ceb4b313b9b35d'
macho-arm64-uvx	P1-fail	committed evidence_id 'ev_bc3cec5edbeba76cd0fa2a307ed56e897c31d14198b97e747a4610e62fc47c33' != live 'ev_6fcab3d46593ceb4056e5b67c540119f6fbdd113a79661462819e5317e3687f7'
carriers=16 pass=0 target=16 entry_ok=1 (ok) province_ok=1 (ok)
```

## Full counter stdout — clean seed

Measured revision: b35e673e0471439ae0e9522bf0580b5df3904a08 (`main` at that run). UTC 2026-10-23T02:46:48Z–02:47:02Z. Exit **1**; stderr empty; target **not met**.

```text
elf-x86_64-uv	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_ef18bd88be10acda35b48cd1675299c0e27b643c5e24acbd0a2700ea3f6a0b33'
elf-x86_64-uvx	P1-pass	packages=584 edges=3041
elf-aarch64-uv	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_1506350fdcaad3573291668df01a30fb30dbdba545c2a20ad4d09ec927c8d40e'
elf-aarch64-uvx	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_5aa17b13d4b1dbdcc4ff03b7abacef14203776cfc504c64fb252473c1e2c38d8'
elf-riscv64-uv	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_6fb2c5354740d93ceb96e5c98b807d84bd02bbace617b93e88498eda90e7a371'
elf-riscv64-uvx	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_3b6453525097133d138ae225eee86e46af8403b17648dfda4f70abc045ff80bc'
pe-x86_64-uv	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_3cb29ace54adb615cf4cf9495ae753a12fd8240fd6b82b5cdc34e57c85449943'
pe-x86_64-uvx	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_eaf76ad92d83fa393039570cb113b16120e3369332b6444f39e9f79540351863'
pe-x86_64-uvw	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_ab1b78ca69fdcd71cb69faed3557e2f5794c94e37b8f33aea5c35728713288b2'
pe-arm64-uv	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_58d8e1f477c5dff8801fe1a2d6f6b81a9c26d69b1f09d0c4904c59d3ef86697e'
pe-arm64-uvx	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_ae58e67e96e716244041cb0292221bdeab86ef5731f890ad25b2bab9177ab7dc'
pe-arm64-uvw	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_6f00915a36c933a68fa819f36977f7085b980b7b2ffec1997a5bea93c51defc9'
macho-x86_64-uv	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_1c3ef6996f8f62f1eeffda94f2b5892763eda8b2f4a333c01311a11bf0c6af10'
macho-x86_64-uvx	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_02fb9f95c9b82c4a6ade2ea299e4fe85e193f821d406fa76feb0cfec709177b0'
macho-arm64-uv	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_7f9ac67aa01cc62f2a0a8d0d4bd50f34fd195523eaf73a6560ceb4b313b9b35d'
macho-arm64-uvx	P1-fail	committed evidence_id 'ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e' != live 'ev_6fcab3d46593ceb4056e5b67c540119f6fbdd113a79661462819e5317e3687f7'
carriers=16 pass=1 target=16 entry_ok=1 (ok) province_ok=1 (ok)
```

## Counterexample, interpretation and smallest safe correction

[Observation; clean counter command and receipt above] The correctly seeded `elf-x86_64-uvx` slot passes (`packages=584 edges=3041`), while each other slot fails on **committed evidence_id != live evidence_id**. Both superficial document gates pass. Thus rejection is not an absent entry/source/PROVINCE row or a uniformly invalid seed.

[Observation; clean stdout lines 1–2] The strongest local pair is same-wheel `elf-x86_64-uv` versus `elf-x86_64-uvx`: the former live id is `ev_ef18bd88be10acda35b48cd1675299c0e27b643c5e24acbd0a2700ea3f6a0b33`, and the genuine seed/live uvx id is `ev_f277bd376a7cd0fb449fa3ad69a2c92737c07bde25b9f98ff4eef1470927ab1e`. The frozen claims' limits state that uv and uvx from one wheel carry the same dependency document. Even that near-identical metadata case does not let relabeling pass.

[Inference from clean stdout and frozen counter lines 182–204, 241–250] The binding clause — the committed envelope must carry the **same evidence_id as that carrier's live run** — blocks the shortcut. Fifteen wrong-slot copies fail that clause; the one genuine source slot correctly survives. No predicate clause let the complete control meet the frozen target. This demonstrates resistance to this tested shortcut, not every conceivable provenance forgery or a C2 result.

**Smallest safe correction:** none to the frozen predicate or instrument is indicated by this control. The fixable first-seed contamination was corrected in the sandbox by L1-authorized recollection from the restored source. A real positive submission must instead commit the matching live envelope for each carrier and name each matching id; it cannot repair provenance by renaming copies. Do not rescale the 16/16 target or count the contaminated 0/16 as the clean shortcut result.

No canonical Rust judge, build, linter, formatter, selftest or C2 counter was invoked. Only the assigned C1 live counter measurements were run. No tool install/update command was issued; the explicit CLI pin was the already-available rea-agents 6.5.0. The transient Node compile cache generated under the assigned scratch TMPDIR was removed after all REA processes exited. All started commands have returned; no service or process was left running.

## Opened primary/local sources

Access date for every source: **2026-10-23**. Ordinary local byte reads only; no external HTTP source or browser was used. The source-inventory command above exited 0 at 2026-10-23T02:44:58Z and retained these full-byte hashes and located quotes (each at most 25 words). The dummy S089 row was not used as authority.

- URL: file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json
  - SHA-256: `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a`
  - Line 6: "This file is the round-30 freeze"

- URL: file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py
  - SHA-256: `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a`
  - Line 193: "committed evidence_id"

- URL: file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/rust_dep_oracle.py
  - SHA-256: `f0b144c6f489b5a78970bcd837cdf3d31ac52e3851bdd574f4f24dda4be9d81d`
  - Line 3: "Shares no code with REA."

- URL: file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv
  - SHA-256: `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b`
  - Line 1: "id\tformat\tarch"

- URL: file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md
  - SHA-256: `4f94007f80be8b87fb4645b366a6e4a695f330da96bdf2dc058ab046db9d1e32`
  - Line 31: "ground moves to Core only after an end-to-end probe lands a"

- URL: file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
  - SHA-256: `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed`
  - Line 5: "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |"

## Artifact SHA-256 inventory

Hashes below cover every retained script, command receipt, raw stdout/stderr, construction/source manifest and current sandbox construction file. The sandbox itself is identified by the two commit hashes above; unchanged inherited checkout files and Git-internal storage are not new control evidence. The historical contaminated copies are recoverable from f795e1dc20f4eecd4866466d600f1d8f59835ac4 and are byte-identical to the retained original seed stdout (hash 5eafec93f5acb3a170040959bffdf8fe5872dc2709daa8b1a448b09fac165fb3). The current 16 copies are the clean seed bytes. No temporary runtime cache is retained.

```text

20f08b042cb31ae51add2e12286c4d6ff391af78621395c0e834638ba2a31b96  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/run_receipted.py
d7d7b89aea56fc1d60a5f5ccc5b10aa557d531eec8951bfc254e2e7a0a4d7d40  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/build_control.py
a8e4726d2ea1706cb1c77e04c7691d3f21b74ee71addcc97adfe98bf03b743d9  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/build_clean_control.py
a694018239a271c3e88abe560e86d13bc02f306467216cd52a8ddf7ca54a4a2e  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/source_inventory.py
3cb9b8d791bd750817bfb140098f61b0fced8aeb275e12c06536111afd01b4ad  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/sources.json
ddf8b72c1227593b31acd633d47e909c8155832062555fb21a02dd2dd0ef247b  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction.json
4e5db2411812706861432f640ba1f55bf59314fff68893adb854de7de0aefb01  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction_clean.json
5cc5e9c0102b6cf0daec8d2eb0889f8be79d2ea0dd93af67b2d3f825335abef0  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone_initial.receipt.json
81c27b5d00cb5a6c05643e98a71a0180b4b5fc5024a03edaef97f37ce88026ce  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone_initial.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone_initial.stderr
8c44819f604d38d50d0edcb63ba4e8676db2bd5a80091a4161d11e6e8ec43f2e  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/rea_once.receipt.json
5eafec93f5acb3a170040959bffdf8fe5872dc2709daa8b1a448b09fac165fb3  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/rea_once.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/rea_once.stderr
e509117b53bf119d5c11af1c7feecfa2d4440796ba80dc331e62311bb550dfa2  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction.receipt.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction.stdout
61e4266f4275c2e87d2fcb9efd78517e8721c10d82c6dd0138d441ca5b854a5a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction.stderr
f7ed0c1692d3439a49cef2e026570efb838cfbc6dbd2a2a5abab0a99d403aab3  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/carrier_sha.receipt.json
070800a0d6a7aaaff1e07661c65c765b2f866235665aadb953ba70a939b90b27  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/carrier_sha.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/carrier_sha.stderr
04e7f98aeca3ccc6bc099c79e74732488fcc9124cab8fa98fc92719768fe21f4  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction_ok.receipt.json
ddf8b72c1227593b31acd633d47e909c8155832062555fb21a02dd2dd0ef247b  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction_ok.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction_ok.stderr
e70d0c87483a8ee0527a5b07fffebdedb0933a6ce8671d3a71e57f489df23266  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_stage.receipt.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_stage.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_stage.stderr
7dbbcacf17fc4ee06541b31f1d015b46e019d01ee30d583dd99c6a9b76361b5b  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_commit.receipt.json
9c7bd7856c954bb647825774ec9637b7ba3f42269c6f8b0b96192fbf6d46b443  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_commit.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_commit.stderr
29f1500b751823dbcbd586efdad9146f02b15a54aba97611ce21e6b394b1cf10  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/source_inventory.receipt.json
3cb9b8d791bd750817bfb140098f61b0fced8aeb275e12c06536111afd01b4ad  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/source_inventory.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/source_inventory.stderr
fe158250ef0da82bcc802efbda8b8c42fbc62dddd47d562603628381987c4c30  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/c1_after_restore.receipt.json
ee0297980f6ae3403142a320bbd78447deaad8ecc783168f7a155ffb67656dd3  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/c1_after_restore.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/c1_after_restore.stderr
8e855e3292ad3994f924c73557cf6beb2b3a9c5ee4d9d5470681db230d34b9c0  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/rea_clean.receipt.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/rea_clean.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/rea_clean.stderr
e33b00775959007eaa472e53beff27c479bb20cdfc7de34a51eee2cb6dd5fb00  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction_clean.receipt.json
4e5db2411812706861432f640ba1f55bf59314fff68893adb854de7de0aefb01  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction_clean.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/construction_clean.stderr
ce4c0af911cfb8056c90f7a887b5faf5ed540c78d8e1eeadfa220d464e8ccbfb  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_stage_clean.receipt.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_stage_clean.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_stage_clean.stderr
af06e335b84f463ea89468838a0e5a3b1c6cb238726ff9020c5abb904a7bd8a2  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_commit_clean.receipt.json
9fb778ec89b07ce5a04d8ea8fe6014e27388c724429d11c699b14b844a64599d  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_commit_clean.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/git_commit_clean.stderr
e78458f0c29f33900731813c6b15af9b4bc030b95bd836c839470df9243cee65  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/c1_clean.receipt.json
5e04a9b087412586051d36fb3c20973ab58759ecf7bdf38fdcdf90db4be960e4  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/c1_clean.stdout
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/c1_clean.stderr
30a8cb6693868c275f94f8da67624aff5b069a956fd54f8c3f7d0d4a7fe71ded  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/PROVINCE.md
a21334679c281908bfb1cbe6c1587856dd4ff6144ca23f49c2c0aebbf1320e4e  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/SOURCES.md
f2ad9880864f5585a880d29fb918467cc56e275ca7b619272e63c93bfc8d5faf  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uv.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uvx.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uv.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uvx.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uv.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uvx.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uv.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvx.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvw.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uv.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvx.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvw.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uv.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uvx.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uv.json
847a680d7df682d5557ecd400cea8f5dfe82b8ecf95687542b6efc7cc628c34a  /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1ShortcutIds/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uvx.json
```

CONTROL CtlC1ShortcutIds met_target=no
