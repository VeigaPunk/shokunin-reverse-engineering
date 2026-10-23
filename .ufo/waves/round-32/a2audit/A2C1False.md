# A2C1False — full all-false C1 control rejected
UTC report: 2026-10-23T06:52:34+00:00

## Counterexample, axes, and bounded finding

Counterexample: twelve newly committed, full JSON error envelopes with `ok:false`, full error/remediation/details objects, `data.operation=binary_overview`, correct frozen carrier SHA-256, and every oracle-compared report field populated correctly. The entry cites S099 and lists all twelve synthetic evidence IDs; an ARM64X row under `## Core` names the entry. Synthetic provenance is explicitly labelled; these are not asserted to be live REA receipts.

Impacted axes: **coverage** (C1, ARM64X Frontier→Core). Calibration (C2) is not exercised.

Observed resolved-environment result: **12 P1-fail, pass=0/12, entry_ok=1, province_ok=1, exit 1**. Every reason is the committed-versus-live full-comparison mismatch. The target `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0, was **not** met; this control supplies no FALSIFIED shortcut.

Source-path interpretation [INFERENCE]: the unique mismatch reason at counter lines 121–122 is reached from lines 198–202 only after the live judge succeeds. Thus the resolved run exercised committed-envelope discrimination rather than merely missing provider readiness. The counter does not expose individual live envelope bodies or live stderr in measure mode; no claims about their unprinted contents go beyond that control-flow implication. Rejection of this synthetic envelope class does not prove discrimination for every possible false control, nor isolate one mismatching field.

Smallest safe correction: preserve the frozen counter, predicates, target and inputs. Carry the two explicit Ghidra/JDK environment keys in the scoring invocation. Retain the original provider-failure receipt as **unevaluable for committed-envelope discrimination**, not as a successful negative control. No counter repair is justified by this result.

## Sandbox and scope

- Clone: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone`
- Frozen parent: `f382e3b7978e6091a19ca93277c15a75c0016b43`; C1 remains at its `9a73680a` freeze; base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
- One and only one fixture commit: `1199091b68f39271ffeeec4bdfff72297659d4f5`.
- Author and committer: `ctl <ctl@local>`. Commit/tree/timestamps and exact command are recorded below.
- Fixture change: 14 files, 35 additions; twelve new envelopes, one new entry, one Core table row. No counter, frozen input, claim, label or target edits.
- Lane writes: only this Report. No fleet/sibling/lane source, documentation/index or Git/jj state writes. No delegation, carrier execution, routing/model change, held-item inspection, or `--write-evidence`.
- Before clone/fixture work, `df -h /fast` exited 0: `/dev/nvme1n1p2 804G 559G 245G 70% /fast`. No carrier rebuild was performed.
- New fixture file contents total 34863 bytes, plus one bounded Core row; full patch 39837 bytes. Each fixture and all captured evidence/report writes remain below 1 MiB.
- Fixture oracle/construction child address-space limit: 4 GiB. All launched test/score commands use `timeout 900`; Ghidra is exempt from that fixture memory cap. No unbounded recursion.
- Child environments remove `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`; every git invocation uses `git -C` with the absolute sandbox path (the initial clone destination is inside the same unique scratch). Hooks and signing were disabled per commit invocation, not by lane/global configuration.

## Original provider-failure receipt — not discrimination evidence

The exact inherited Eval subprocess environment had both `GHIDRA_INSTALL_DIR` and `JAVA_HOME` absent. The first score returned twelve live `exit 1 ok False` reasons before any committed check. Its suppressed inner provider error is unknown and is not fabricated here. Bash `printenv GHIDRA_INSTALL_DIR JAVA_HOME REA_GHIDRA_PATH REA_GHIDRA_INSTALL_DIR` printed the two configured paths, then exited 1 because the latter optional keys were absent.

```json
{
  "utc_start": "2026-10-23T06:47:55+00:00",
  "utc_end": "2026-10-23T06:48:04+00:00",
  "argv": [
    "timeout",
    "900",
    "python3",
    "-I",
    "-B",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone/tools/round-32/c1-arm64x-positive.py",
    "--root",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
    "--rev",
    "1199091b68f39271ffeeec4bdfff72297659d4f5"
  ],
  "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
  "exit": 1,
  "stdout": "k01\tP1-fail\texit 1 ok False\nk02\tP1-fail\texit 1 ok False\nk03\tP1-fail\texit 1 ok False\nk04\tP1-fail\texit 1 ok False\nk05\tP1-fail\texit 1 ok False\nk06\tP1-fail\texit 1 ok False\nk07\tP1-fail\texit 1 ok False\nk08\tP1-fail\texit 1 ok False\nk09\tP1-fail\texit 1 ok False\nk10\tP1-fail\texit 1 ok False\nk11\tP1-fail\texit 1 ok False\nk12\tP1-fail\texit 1 ok False\ncarriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)\n",
  "stderr": "",
  "process_group": 3285401,
  "process_group_cleanup": "SIGKILL attempted after completion; ESRCH accepted; no detached sessions launched",
  "git_environment": "GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE absent in child environment",
  "memory_policy": "Fixture construction capped at 4 GiB address space; live Ghidra child exempt as assigned",
  "write_evidence": false
}
```

## Resolved-environment scoring receipt — one changed-environment run

Parent direction explicitly authorized one run after resolving this real prerequisite difference. Only these keys changed: `GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` and `JAVA_HOME=/usr/lib/jvm/java-21-openjdk`. The revision, fixture, counter and inputs are unchanged. No safety refusal/model switch occurred.

```json
{
  "utc_start": "2026-10-23T06:49:15+00:00",
  "utc_end": "2026-10-23T06:51:03+00:00",
  "argv": [
    "timeout",
    "900",
    "env",
    "GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC",
    "JAVA_HOME=/usr/lib/jvm/java-21-openjdk",
    "python3",
    "-I",
    "-B",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone/tools/round-32/c1-arm64x-positive.py",
    "--root",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
    "--rev",
    "1199091b68f39271ffeeec4bdfff72297659d4f5"
  ],
  "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
  "exit": 1,
  "stdout": "k01\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk02\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk03\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk04\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk05\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk06\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk07\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk08\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk09\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk10\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk11\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\nk12\tP1-fail\tcommitted envelope differs from the live envelope (full comparison)\ncarriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)\n",
  "stderr": "",
  "process_group": 3551843,
  "process_group_cleanup": "SIGKILL attempted after completion; ESRCH accepted; no detached sessions launched",
  "git_environment": "GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE absent in inherited child environment",
  "resolved_environment": {
    "GHIDRA_INSTALL_DIR": "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC",
    "JAVA_HOME": "/usr/lib/jvm/java-21-openjdk"
  },
  "memory_policy": "Fixture construction capped at 4 GiB address space; live Ghidra child exempt as assigned",
  "write_evidence": false
}
```

Full relevant stdout, one line for each P1 and the final target:

```text
k01	P1-fail	committed envelope differs from the live envelope (full comparison)
k02	P1-fail	committed envelope differs from the live envelope (full comparison)
k03	P1-fail	committed envelope differs from the live envelope (full comparison)
k04	P1-fail	committed envelope differs from the live envelope (full comparison)
k05	P1-fail	committed envelope differs from the live envelope (full comparison)
k06	P1-fail	committed envelope differs from the live envelope (full comparison)
k07	P1-fail	committed envelope differs from the live envelope (full comparison)
k08	P1-fail	committed envelope differs from the live envelope (full comparison)
k09	P1-fail	committed envelope differs from the live envelope (full comparison)
k10	P1-fail	committed envelope differs from the live envelope (full comparison)
k11	P1-fail	committed envelope differs from the live envelope (full comparison)
k12	P1-fail	committed envelope differs from the live envelope (full comparison)
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

The child REA argv below are determined by frozen `run_rea` lines 95–100; they are not a separate replay or separately captured process trace. Counter children use `/tmp`, timeout 600, and the same resolved environment.

```json
[
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k02.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k03.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k04.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k05.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k06.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k07.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k08.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k09.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k10.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k11.dll",
    "--format",
    "json",
    "--full-output"
  ],
  [
    "npx",
    "-y",
    "rea-agents@6.5.0",
    "inspect",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k12.dll",
    "--format",
    "json",
    "--full-output"
  ]
]
```

## Frozen identities and source locations

Reopened actual source on 2026-10-23 UTC; no external-source quotation is relied on.

- `file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone/tools/round-32/c1-arm64x-positive.py`: lines 69–87 (live gate), 95–100 (argv/environment), 109–126 (committed gate), 190–205 (dispatch); SHA-256 below.
- `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/config/parseConfig.js`:45–46 maps the two environment keys; SHA-256 `ae30b2c75d6ce6c08bdf2f2f5dba8a3d67f13021d6d800d5300645d690a0d4a9`.
- `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/ghidra/GhidraInstallation.js`:242–257 requires a configured install directory; SHA-256 `0ff09f1350ade169db156c8d987cca0929a98d4b2337c78efc2bceba839a203a`.
- Installed REA package.json: name `rea-agents`, version `6.5.0`, SHA-256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`.
- Ghidra application.properties: version 12.1.4, java.min 21, SHA-256 `e84c26b08545eee63d24a1a8a4dd7905e4209538e2e7192093877c435c64eb67`.

Frozen source/input SHA-256 (observed with `sha256sum` before fixture writes):

```json
{
  "tools/round-32/c1-arm64x-positive.py": "7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a",
  "tools/round-32/arm64x_oracle.py": "17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686",
  "corpus/evidence/round-32/c1/carriers.tsv": "8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e",
  "corpus/evidence/round-32/c1/predictions.tsv": "fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b"
}
```

Committed fixture content SHA-256 (new-file bytes captured at construction; PROVINCE observed with `sha256sum`):

```json
{
  "corpus/evidence/round-32/c1/envelopes/k01.json": "fdbe10f3d29da1c2ad3881df1f50c9fab5f3cca45e5b7aa6226dcffea794216d",
  "corpus/evidence/round-32/c1/envelopes/k02.json": "df6751773b3dac73f293b866857d0f51f09fcad20206b43f368c4364c8110f6a",
  "corpus/evidence/round-32/c1/envelopes/k03.json": "ccd7cd8ad319c83a21f950c88661877c1ea217e20808fa422d492578c46d2d3a",
  "corpus/evidence/round-32/c1/envelopes/k04.json": "cf5deeac0e4f7608300d5ac01f74c6c9c7584d844afabb043d57761a7ce96b2f",
  "corpus/evidence/round-32/c1/envelopes/k05.json": "e712788e49aedb311cdb73083ec237759401ae43a6372c54717fb0853f3b42d7",
  "corpus/evidence/round-32/c1/envelopes/k06.json": "71fa0536898eaabe8800a39d8a9f8763f74bf0bf9c93a3802470672d109804d1",
  "corpus/evidence/round-32/c1/envelopes/k07.json": "794a0eafe9fb4616017e2cc6a403a172122e626fc42d5f9119d4bd4ac96363c3",
  "corpus/evidence/round-32/c1/envelopes/k08.json": "898c0cbf9e5366b3dce33b557344a7c497449670833d4779ee541aaf04f63ec1",
  "corpus/evidence/round-32/c1/envelopes/k09.json": "b1d0da9df6a6695296f03aa99b224a09c97973d29551a5ddf7256f9fec9a6e00",
  "corpus/evidence/round-32/c1/envelopes/k10.json": "5561dec86bb0bfb6f8f2eeff0fe80307ec8e87cf35faef6394a20cfc665d2ec9",
  "corpus/evidence/round-32/c1/envelopes/k11.json": "96a768580450cb0bc714e6bd71bcfe383808117ffff0e8a6e4cb2107ca616656",
  "corpus/evidence/round-32/c1/envelopes/k12.json": "d69f9cf99d4197818f79ae5d2a04fc5f14959ad67afcad805cb9621774a7866c",
  "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md": "5b1715b04009f589d51e5159a6bdb0f8d831f514f619083fb7f7bb3253b97049",
  "PROVINCE.md": "76207c5fda8e9503603711d45436fd18b7be290a8bd83b6d49b5f90fbf2b8e19"
}
```

Full fixture diff SHA-256: `d00d5c281d5c6a60ee560dbc40dde7512a48f229b47134c17f0af5fdf6648fee`.

## Construction command receipts

Initial clone argv, both exit 0, with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset and a 4 GiB address-space cap:

```text
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone checkout --detach f382e3b7
Cloning into '/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone'...
done.
HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) — anchored evidence and description, before receipts
```

```json
[
  {
    "utc_start": "2026-10-23T06:47:40+00:00",
    "utc_end": "2026-10-23T06:47:40+00:00",
    "argv": [
      "timeout",
      "900",
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
      "add",
      "--",
      "PROVINCE.md",
      "corpus/evidence/round-32/c1/envelopes/k01.json",
      "corpus/evidence/round-32/c1/envelopes/k02.json",
      "corpus/evidence/round-32/c1/envelopes/k03.json",
      "corpus/evidence/round-32/c1/envelopes/k04.json",
      "corpus/evidence/round-32/c1/envelopes/k05.json",
      "corpus/evidence/round-32/c1/envelopes/k06.json",
      "corpus/evidence/round-32/c1/envelopes/k07.json",
      "corpus/evidence/round-32/c1/envelopes/k08.json",
      "corpus/evidence/round-32/c1/envelopes/k09.json",
      "corpus/evidence/round-32/c1/envelopes/k10.json",
      "corpus/evidence/round-32/c1/envelopes/k11.json",
      "corpus/evidence/round-32/c1/envelopes/k12.json",
      "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
    ],
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "process_group": 3282298,
    "process_group_cleanup": "SIGKILL attempted after completion; ESRCH accepted; no detached sessions launched"
  },
  {
    "utc_start": "2026-10-23T06:47:40+00:00",
    "utc_end": "2026-10-23T06:47:40+00:00",
    "argv": [
      "timeout",
      "900",
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
      "-c",
      "core.hooksPath=/dev/null",
      "diff",
      "--cached",
      "--no-ext-diff",
      "--binary",
      "--",
      "PROVINCE.md",
      "corpus/evidence/round-32/c1/envelopes/k01.json",
      "corpus/evidence/round-32/c1/envelopes/k02.json",
      "corpus/evidence/round-32/c1/envelopes/k03.json",
      "corpus/evidence/round-32/c1/envelopes/k04.json",
      "corpus/evidence/round-32/c1/envelopes/k05.json",
      "corpus/evidence/round-32/c1/envelopes/k06.json",
      "corpus/evidence/round-32/c1/envelopes/k07.json",
      "corpus/evidence/round-32/c1/envelopes/k08.json",
      "corpus/evidence/round-32/c1/envelopes/k09.json",
      "corpus/evidence/round-32/c1/envelopes/k10.json",
      "corpus/evidence/round-32/c1/envelopes/k11.json",
      "corpus/evidence/round-32/c1/envelopes/k12.json",
      "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
    ],
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
    "exit": 0,
    "stdout": "Full, byte-for-byte stdout is the patch in the Control fixture diff section below.",
    "stderr": "",
    "process_group": 3282439,
    "process_group_cleanup": "SIGKILL attempted after completion; ESRCH accepted; no detached sessions launched"
  },
  {
    "utc_start": "2026-10-23T06:47:40+00:00",
    "utc_end": "2026-10-23T06:47:40+00:00",
    "argv": [
      "timeout",
      "900",
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
      "-c",
      "user.name=ctl",
      "-c",
      "user.email=ctl@local",
      "-c",
      "commit.gpgSign=false",
      "-c",
      "core.hooksPath=/dev/null",
      "commit",
      "-m",
      "control: A2C1False full all-false C1 envelopes"
    ],
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
    "exit": 0,
    "stdout": "[detached HEAD 1199091b] control: A2C1False full all-false C1 envelopes\n 14 files changed, 35 insertions(+)\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k01.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k02.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k03.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k04.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k05.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k06.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k07.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k08.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k09.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k10.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k11.json\n create mode 100644 corpus/evidence/round-32/c1/envelopes/k12.json\n create mode 100644 corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md\n",
    "stderr": "",
    "process_group": 3282444,
    "process_group_cleanup": "SIGKILL attempted after completion; ESRCH accepted; no detached sessions launched"
  },
  {
    "utc_start": "2026-10-23T06:47:40+00:00",
    "utc_end": "2026-10-23T06:47:40+00:00",
    "argv": [
      "timeout",
      "900",
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
      "show",
      "-s",
      "--format=%H%n%T%n%an <%ae>%n%cn <%ce>%n%aI%n%cI",
      "HEAD"
    ],
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
    "exit": 0,
    "stdout": "1199091b68f39271ffeeec4bdfff72297659d4f5\n804002b37f8dcf6904f9c383daa86a1ef741f4ce\nctl <ctl@local>\nctl <ctl@local>\n2026-10-23T03:47:40-03:00\n2026-10-23T03:47:40-03:00\n",
    "stderr": "",
    "process_group": 3282499,
    "process_group_cleanup": "SIGKILL attempted after completion; ESRCH accepted; no detached sessions launched"
  }
]
```

## Oracle construction receipt

The frozen oracle was run read-only to populate the strongest required full data fields; its entire relevant stdout follows, including hashes, hybrid classification, expected segments and counts. JSON envelopes were created with the write tool; only the Core row was edited. No generator or import-named marker/log was created.

```json
{
  "utc_start": "2026-10-23T06:46:54+00:00",
  "utc_end": "2026-10-23T06:46:54+00:00",
  "argv": [
    "timeout",
    "900",
    "python3",
    "-I",
    "-B",
    "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone/tools/round-32/arm64x_oracle.py",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k02.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k03.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k04.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k05.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k06.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k07.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k08.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k09.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k10.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k11.dll",
    "/fast/scratch/hyaku/kaidoku-r32/carriers/k12.dll"
  ],
  "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/clone",
  "memory_limit_bytes": 4294967296,
  "exit": 0,
  "stdout": "{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 16, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 92, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 16, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-2f386dde73a2.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 1, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll\", \"sha256\": \"2f386dde73a262a657cc385f16594afce9369e05121916a8fd44a6cc45630989\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 32, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 112, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 32, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-a16ba36205f5.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 2, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\", \"f2\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k02.dll\", \"sha256\": \"a16ba36205f584b0a1589895ed31feffcc36eda692b81e675cdfeadb819519d4\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 132, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 216, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 48, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-0291e17bd517.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 3, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\", \"f2\", \"f3\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k03.dll\", \"sha256\": \"0291e17bd517802b44984fb8e8fcc2cec0266b02ded1cb81bccea040a737b73d\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 64, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 92, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 16, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-3c783318ea3a.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 4, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\", \"f2\", \"f3\", \"f4\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k04.dll\", \"sha256\": \"3c783318ea3aea29033460edb17b4cade7b0eca675e0d5410d278672d2bfb386\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 16, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 152, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 64, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-cc5c644a515b.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 1, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k05.dll\", \"sha256\": \"cc5c644a515b4e9d65c1c5ae8455df1032f5c3d21bb77d034e8ded13c04060bf\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 220, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 312, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 80, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-6c45a3ce1c3e.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 5, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\", \"f2\", \"f3\", \"f4\", \"f5\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k06.dll\", \"sha256\": \"6c45a3ce1c3e9b91719a3ded213d995c35947af221145b14c06f0ca838247b3c\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 96, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 112, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 32, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-84a78b7894fa.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 6, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\", \"f2\", \"f3\", \"f4\", \"f5\", \"f6\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k07.dll\", \"sha256\": \"84a78b7894fa11f876734d2bd926d8e3e73f08be3f2a6f93b35925e3605afb6f\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 32, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 192, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 96, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-b158eaf7c741.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 2, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\", \"f2\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k08.dll\", \"sha256\": \"b158eaf7c7417400202f06acc0867013185260efdf296a6dbbe622e873e3215c\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 112, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 132, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 48, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-cf0148615fce.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 7, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"n1\", \"n2\", \"n3\", \"n4\", \"n5\", \"n6\", \"n7\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k09.dll\", \"sha256\": \"cf0148615fce4399e067715eb48554f63c4a30cf04a40c75776d58b1a2b82a87\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 132, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 408, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 112, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-a48499d2df92.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 3, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"n1\", \"n2\", \"n3\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k10.dll\", \"sha256\": \"a48499d2df92de871fd3e7c7d8cba63bbfbc019fd84ee312bdbdada632c766c7\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 128, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 232, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 128, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-b5e2af7f2b96.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 8, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004600\", \"image_base\": \"0x180000000\", \"length\": 1536, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"f1\", \"f2\", \"f3\", \"f4\", \"f5\", \"f6\", \"f7\", \"f8\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k11.dll\", \"sha256\": \"b5e2af7f2b96fd66f87ed0be99e576fa94b7f843d088bdb05e212ac67592d181\"}\n{\"class\": {\"arm64x\": true, \"code_map\": [{\"length\": 16, \"start\": 4096, \"type\": \"ARM64\"}, {\"length\": 112, \"start\": 8192, \"type\": \"ARM64EC\"}, {\"length\": 32, \"start\": 12288, \"type\": \"AMD64\"}], \"machine\": \"0xaa64\"}, \"expected\": {\"architecture\": \"arm64\", \"document\": \"target-8c852d075fab.dll\", \"format\": \"pe\", \"image_base\": \"0x180000000\", \"procedure_count\": 1, \"segment_count\": 8, \"segments\": [{\"address_space\": \"ram\", \"end\": \"0x180000400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \"Headers\", \"start\": \"0x180000000\"}, {\"address_space\": \"ram\", \"end\": \"0x180002200\", \"image_base\": \"0x180000000\", \"length\": 4608, \"name\": \".text\", \"start\": \"0x180001000\"}, {\"address_space\": \"ram\", \"end\": \"0x180003200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".hexpthk\", \"start\": \"0x180003000\"}, {\"address_space\": \"ram\", \"end\": \"0x180004400\", \"image_base\": \"0x180000000\", \"length\": 1024, \"name\": \".rdata\", \"start\": \"0x180004000\"}, {\"address_space\": \"ram\", \"end\": \"0x180005200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".data\", \"start\": \"0x180005000\"}, {\"address_space\": \"ram\", \"end\": \"0x180006200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".pdata\", \"start\": \"0x180006000\"}, {\"address_space\": \"ram\", \"end\": \"0x180007200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".a64xrm\", \"start\": \"0x180007000\"}, {\"address_space\": \"ram\", \"end\": \"0x180008200\", \"image_base\": \"0x180000000\", \"length\": 512, \"name\": \".reloc\", \"start\": \"0x180008000\"}]}, \"native_exports\": [\"n1\"], \"path\": \"/fast/scratch/hyaku/kaidoku-r32/carriers/k12.dll\", \"sha256\": \"8c852d075fab64aca5c165ff3b907507d62d409972bbfddb72543ef3efea04fa\"}\n",
  "stderr": "",
  "process_cleanup": "Owned process group SIGKILL attempted after communicate; ESRCH accepted."
}
```

## Control fixture diff — full replayable patch

This is the exact staged `git diff --cached --no-ext-diff --binary` stdout captured before the one fixture commit. It is control data, not instructions or production evidence.

```diff
diff --git c/PROVINCE.md i/PROVINCE.md
index d9d4cf4c..5be271ce 100644
--- c/PROVINCE.md
+++ i/PROVINCE.md
@@ -41,6 +41,7 @@ Surfaces owned now — each verified on this host 2026-10-13.
 
 | Surface | Ports / paths / config keys | Liveness / readiness probe | Verified evidence |
 |---|---|---|---|
+| ARM64X hybrid PE — synthetic all-false control | Twelve frozen carrier digests; no executable launch | Intentionally `ok:false` full `binary_overview` envelopes; sandbox negative fixture only | `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` (S099; not production coverage evidence) |
 | REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml` — config files pin `rea-agents` (Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary) with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` would inspect a running attached client; not exercised this round. CLI: `rea doctor` (6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing) | round-19 re-grepped pin/sha256 record `.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in `evidence/doctor/`; historical readiness probe 2026-10-13 |
 | `rea` CLI | npx cache `~/.npm/_npx/*/node_modules/rea-agents` — no `rea` on PATH; 153 commands on the 6.5.0/6.7.0 pins, 127 on 6.4.0 (historical) | `npx -y rea-agents@6.4.0 --version` → `6.4.0` (2026-10-13 receipt) | wave 01/02/03 catalogs |
 | Ghidra provider | `GHIDRA_INSTALL_DIR` (876 MB install); headless `support/analyzeHeadless`; native decompiler `Ghidra/Features/Decompiler/os/linux_x86_64/decompile`; 39 processor modules; 34 features incl. PyGhidra/BSim | `rea doctor` → providerInspections `ghidra: configured+available`, 8/8 checks | `application.version=12.1.4`, build 2026-09-21, rev 8b6bbb85 |
diff --git c/corpus/evidence/round-32/c1/envelopes/k01.json i/corpus/evidence/round-32/c1/envelopes/k01.json
new file mode 100644
index 00000000..83549d5e
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k01.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"2d1399f981cac3d17e9e867fef051b402b04df0a59317e06db35d78de978da89","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_de383a2ba43bfaefa2be3b635a7e75fe4e14cf62e933a55115bd56fa942c9e5a","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-2f386dde73a2.dll","image_base":"0x180000000","procedure_count":1,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004400","image_base":"0x180000000","length":1024,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"2f386dde73a262a657cc385f16594afce9369e05121916a8fd44a6cc45630989"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll","name":"k01.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k02.json i/corpus/evidence/round-32/c1/envelopes/k02.json
new file mode 100644
index 00000000..c5a507c5
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k02.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"b76e79cc649db8f3a446d1d301e0e14644e4b8dab70d513833c8af9b15c6398c","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_47cca0e2ee0305e21b6a6ea1420a7d3d23aa07d6124a886b4643aba6fbbc16a7","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-a16ba36205f5.dll","image_base":"0x180000000","procedure_count":2,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"a16ba36205f584b0a1589895ed31feffcc36eda692b81e675cdfeadb819519d4"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k02.dll","name":"k02.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k03.json i/corpus/evidence/round-32/c1/envelopes/k03.json
new file mode 100644
index 00000000..b137f52f
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k03.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"a1ecb7a36ece77157e4b795f9b32254fdf15b14c7a68c8a2bea1e7eb538fe5cd","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_276ceff5a65b78841b73aaa6ca49a69168b4e8463a85c2407f840c050a61f799","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-0291e17bd517.dll","image_base":"0x180000000","procedure_count":3,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"0291e17bd517802b44984fb8e8fcc2cec0266b02ded1cb81bccea040a737b73d"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k03.dll","name":"k03.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k04.json i/corpus/evidence/round-32/c1/envelopes/k04.json
new file mode 100644
index 00000000..09aca1f5
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k04.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"96aff8ffc22fd5b92aeec8ec8c9964caed4944f55b754a412a97f96d3b00e163","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_e0fffcd7365bf879acfaa66de1a62163c2466aa71e226f2190a66094a167df58","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-3c783318ea3a.dll","image_base":"0x180000000","procedure_count":4,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"3c783318ea3aea29033460edb17b4cade7b0eca675e0d5410d278672d2bfb386"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k04.dll","name":"k04.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k05.json i/corpus/evidence/round-32/c1/envelopes/k05.json
new file mode 100644
index 00000000..21e45108
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k05.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"0ecc6bd667b4584be786d6a719247c26d32e7c028305c4b98b0385e01671c06f","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_55d6bee4f60c0cee79ecb8559b1b66e0ade32db28ffd67cde780ce7229a50caf","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-cc5c644a515b.dll","image_base":"0x180000000","procedure_count":1,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"cc5c644a515b4e9d65c1c5ae8455df1032f5c3d21bb77d034e8ded13c04060bf"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k05.dll","name":"k05.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k06.json i/corpus/evidence/round-32/c1/envelopes/k06.json
new file mode 100644
index 00000000..bf34254f
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k06.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"bf4784298d7dc1beb897ba886f7beaf6dbec68bacedc37bf407351b51546f160","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_af4790ddcabfcf04868e4b19b6a1d1bf67c4208e907ddeb53fa7c18fbc73e275","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-6c45a3ce1c3e.dll","image_base":"0x180000000","procedure_count":5,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"6c45a3ce1c3e9b91719a3ded213d995c35947af221145b14c06f0ca838247b3c"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k06.dll","name":"k06.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k07.json i/corpus/evidence/round-32/c1/envelopes/k07.json
new file mode 100644
index 00000000..727415c7
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k07.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"335846234c44237e0500f8311bd7bb5f736423c0c4389c18cd4f6e4ac8cf6e03","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_6bb93d33b51ef0875ee17207d37f4b26869f16f35e43d1137cad1482179cf8a8","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-84a78b7894fa.dll","image_base":"0x180000000","procedure_count":6,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"84a78b7894fa11f876734d2bd926d8e3e73f08be3f2a6f93b35925e3605afb6f"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k07.dll","name":"k07.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k08.json i/corpus/evidence/round-32/c1/envelopes/k08.json
new file mode 100644
index 00000000..23475a95
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k08.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"c723d0dbbc19b3091c9e5fb02f83e324acbaa48375bcce03a8b25c6fd0fdb5a3","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_1e733a124b239056947f8817eef013918be737178ce64c6d3b349fd59fbfeaa4","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-b158eaf7c741.dll","image_base":"0x180000000","procedure_count":2,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"b158eaf7c7417400202f06acc0867013185260efdf296a6dbbe622e873e3215c"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k08.dll","name":"k08.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k09.json i/corpus/evidence/round-32/c1/envelopes/k09.json
new file mode 100644
index 00000000..a40a8394
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k09.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"c6083279f3439fb1396dc81dcdab827c984fdfa2cb99e53f7fdc0f10ee00bfed","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_cdc3e9747752c10c74a84210c1544de7ad269be676067bf808497e7c9d968a43","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-cf0148615fce.dll","image_base":"0x180000000","procedure_count":7,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"cf0148615fce4399e067715eb48554f63c4a30cf04a40c75776d58b1a2b82a87"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k09.dll","name":"k09.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k10.json i/corpus/evidence/round-32/c1/envelopes/k10.json
new file mode 100644
index 00000000..3e71dc9a
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k10.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"b408c6aab169cdb32ae011082cc535b58e3a884756ddff3903d94911bf24c8bf","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_b2f989fb0b026d8ae745b1b889200df8832907dfe872b2c4163bfc2cf0bc177b","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-a48499d2df92.dll","image_base":"0x180000000","procedure_count":3,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"a48499d2df92de871fd3e7c7d8cba63bbfbc019fd84ee312bdbdada632c766c7"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k10.dll","name":"k10.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k11.json i/corpus/evidence/round-32/c1/envelopes/k11.json
new file mode 100644
index 00000000..fc698221
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k11.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"0d98573c660083b8e8f245a439d09fc60462a7ec4743914cdfbff2a077fe7ae5","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_653856a0b67ed43204b605241a8639b2242ffed9f4bc03588a218c1ce6feb432","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-b5e2af7f2b96.dll","image_base":"0x180000000","procedure_count":8,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004600","image_base":"0x180000000","length":1536,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"b5e2af7f2b96fd66f87ed0be99e576fa94b7f843d088bdb05e212ac67592d181"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k11.dll","name":"k11.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/evidence/round-32/c1/envelopes/k12.json i/corpus/evidence/round-32/c1/envelopes/k12.json
new file mode 100644
index 00000000..a3fd522a
--- /dev/null
+++ i/corpus/evidence/round-32/c1/envelopes/k12.json
@@ -0,0 +1 @@
+{"data":{"analysis_profile":{"digest":"230d08335e79e937841e797126222f15abe239a27346b58fbcd67d03675d01c1","parameters":{"construction":"frozen-oracle expected fields; intentional ok:false"},"provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"}},"authority":"synthetic-negative-control","confidence":"derived","environment":null,"evidence_id":"ev_40fffd979ee6980123e6ad8247bc98502b1b1346154c61b3c8d1b3f8b169a4a7","evidence_links":[],"limitations":["Synthetic control, not a live REA receipt. Comparable fields are derived from the frozen PE oracle; ok is intentionally false."],"locations":[],"normalized_result":{"document":"target-8c852d075fab.dll","image_base":"0x180000000","procedure_count":1,"segment_count":8,"segments":[{"address_space":"ram","end":"0x180000400","image_base":"0x180000000","length":1024,"name":"Headers","start":"0x180000000"},{"address_space":"ram","end":"0x180002200","image_base":"0x180000000","length":4608,"name":".text","start":"0x180001000"},{"address_space":"ram","end":"0x180003200","image_base":"0x180000000","length":512,"name":".hexpthk","start":"0x180003000"},{"address_space":"ram","end":"0x180004400","image_base":"0x180000000","length":1024,"name":".rdata","start":"0x180004000"},{"address_space":"ram","end":"0x180005200","image_base":"0x180000000","length":512,"name":".data","start":"0x180005000"},{"address_space":"ram","end":"0x180006200","image_base":"0x180000000","length":512,"name":".pdata","start":"0x180006000"},{"address_space":"ram","end":"0x180007200","image_base":"0x180000000","length":512,"name":".a64xrm","start":"0x180007000"},{"address_space":"ram","end":"0x180008200","image_base":"0x180000000","length":512,"name":".reloc","start":"0x180008000"}],"string_count":0},"operation":"binary_overview","parameters":{},"predicate_type":"rea.analysis","provider":{"id":"a2c1false-control","name":"Synthetic negative control; not REA evidence","version":"1"},"raw_result":null,"relationship_coverage":null,"subject":{"architecture":"arm64","digest":{"sha256":"8c852d075fab64aca5c165ff3b907507d62d409972bbfddb72543ef3efea04fa"},"format":"pe","local_path":"/fast/scratch/hyaku/kaidoku-r32/carriers/k12.dll","name":"k12.dll"}},"error":{"category":"analysis","code":"analysis_failed","details":{"captured_output":{"stderr":"","stdout":"","truncated":false},"control":"A2C1False","operation":"binary_overview"},"message":"Synthetic all-false control: deliberately unsuccessful, despite populated binary_overview data.","remediation":{"action":"This is a negative fixture, not a runtime failure to repair."},"retryable":false},"meta":{"command":"inspect","control":"A2C1False synthetic full error envelope","duration":"0ms"},"ok":false}
diff --git c/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md i/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
new file mode 100644
index 00000000..6b638aae
--- /dev/null
+++ i/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
@@ -0,0 +1,22 @@
+# ARM64X synthetic all-false control
+
+This sandbox-only negative fixture cites S099 (Microsoft Learn, Arm64X PE files).
+It is not production evidence and makes no positive coverage claim.
+Every committed envelope is intentionally `ok:false`, with a full error object,
+`data.operation` set to `binary_overview`, the pinned carrier digest, and every
+frozen oracle comparable field populated. No carrier binary is executed.
+
+| Carrier | Synthetic evidence ID | Envelope |
+|---|---|---|
+| k01 | `ev_de383a2ba43bfaefa2be3b635a7e75fe4e14cf62e933a55115bd56fa942c9e5a` | `corpus/evidence/round-32/c1/envelopes/k01.json` |
+| k02 | `ev_47cca0e2ee0305e21b6a6ea1420a7d3d23aa07d6124a886b4643aba6fbbc16a7` | `corpus/evidence/round-32/c1/envelopes/k02.json` |
+| k03 | `ev_276ceff5a65b78841b73aaa6ca49a69168b4e8463a85c2407f840c050a61f799` | `corpus/evidence/round-32/c1/envelopes/k03.json` |
+| k04 | `ev_e0fffcd7365bf879acfaa66de1a62163c2466aa71e226f2190a66094a167df58` | `corpus/evidence/round-32/c1/envelopes/k04.json` |
+| k05 | `ev_55d6bee4f60c0cee79ecb8559b1b66e0ade32db28ffd67cde780ce7229a50caf` | `corpus/evidence/round-32/c1/envelopes/k05.json` |
+| k06 | `ev_af4790ddcabfcf04868e4b19b6a1d1bf67c4208e907ddeb53fa7c18fbc73e275` | `corpus/evidence/round-32/c1/envelopes/k06.json` |
+| k07 | `ev_6bb93d33b51ef0875ee17207d37f4b26869f16f35e43d1137cad1482179cf8a8` | `corpus/evidence/round-32/c1/envelopes/k07.json` |
+| k08 | `ev_1e733a124b239056947f8817eef013918be737178ce64c6d3b349fd59fbfeaa4` | `corpus/evidence/round-32/c1/envelopes/k08.json` |
+| k09 | `ev_cdc3e9747752c10c74a84210c1544de7ad269be676067bf808497e7c9d968a43` | `corpus/evidence/round-32/c1/envelopes/k09.json` |
+| k10 | `ev_b2f989fb0b026d8ae745b1b889200df8832907dfe872b2c4163bfc2cf0bc177b` | `corpus/evidence/round-32/c1/envelopes/k10.json` |
+| k11 | `ev_653856a0b67ed43204b605241a8639b2242ffed9f4bc03588a218c1ce6feb432` | `corpus/evidence/round-32/c1/envelopes/k11.json` |
+| k12 | `ev_40fffd979ee6980123e6ad8247bc98502b1b1346154c61b3c8d1b3f8b169a4a7` | `corpus/evidence/round-32/c1/envelopes/k12.json` |
```

## Cleanup and exercised checks

- Every owned subprocess was waited and its owned process group was SIGKILL-attempted on completion (ESRCH accepted).
- Post-score cleanup command: `ps -o pid,ppid,pgid,sid,stat,args --sid 3285401,3551843`; observed exit 1 with only `PID PPID PGID SID STAT COMMAND`, hence no remaining members in either scorer session. No services/watchers were started.
- Exercised only the fixture-construction oracle, the original failed-prerequisite frozen C1 score, the single explicitly resolved-environment frozen C1 score, exact required hashes/provenance, and owned-process cleanup. No unrelated verification.
- Tool versions observed: Python 3.14.8, Node v24.21.0, npm 11.19.0, git 2.56.0; REA cached pin 6.5.0. No tool installation/update by this seat; no pacman transaction.
- Full scratch evidence: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1False/A2C1False.fixture.patch`, `A2C1False.oracle.json`, `A2C1False.git.json`, `A2C1False.counter.json`, `A2C1False.resolved-counter.json`; their required receipt/diff content is embedded above so this Report is self-contained for pre-data integration.

Report: .ufo/waves/round-32/a2audit/A2C1False.md
