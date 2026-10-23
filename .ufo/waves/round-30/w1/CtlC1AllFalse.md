# R30-C1 pre-data all-false control

CONTROL CtlC1AllFalse met_target=no

**Observation — attack verdict: holds for this control (rejected).** The committed all-false control scored `carriers=16 pass=0 target=16 entry_ok=1 (ok) province_ok=1 (ok)`, exit 1. It did not meet the frozen C1 target. No predicate clause let the control through.

**Mutation classification: inconclusive, not a killed mutant.** The pristine frozen revision also failed the target because it intentionally contains no post-freeze evidence. The first pristine attempt additionally hit an altered shared-carrier PIN failure. The successful bounded measurement of this negative control establishes its rejection, not a passing-pristine-to-failing-mutant kill.

Axes: record authenticity, target rejection, exact-byte restoration, shared-state isolation.

## Construction and isolation

- Sandbox: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone`. Starting `main`: `4ee65c6771058284aa947a266475839d196ed4d4`; original tree `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2`.
- Control commit: `6f8c4de93a4c1b1ecf1e920f7e704ff41b7d8c6f` at 2026-10-23T02:45:15+00:00; commit exit 0. Output excerpt: `[main 6f8c4de9] control: R30-C1 all-false committed envelopes`; `19 files changed, 24 insertions(+)`.
- No counter/oracle, frozen manifest, claim, carrier, or mutant bytes were changed by this seat. No carrier or mutant was executed. REA was invoked only by the assigned counter and once directly on `/usr/bin/rg`, using the required 6.5.0 pin. No `--write-evidence` run occurred and no genuine carrier envelopes were committed.
- This seat was **not** the writer that altered the shared carriers. All writes except this assigned report were under the seat directory. No lane/fleet Git index or jj state was written.
- No tools were installed or updated. The pre-existing cached `rea-agents@6.5.0` package was invoked through npx. No pacman transaction or service operation occurred.
- Every process command was timeout-bounded at 900 seconds or less. The evidence runner terminates its started process group after each run; every run completed. Its own generated Node compile cache was removed after the final detector, exit 0 at 2026-10-23T02:46:39Z. No started process tree remains running.

Clone command (exit 0; clone identity subsequently recorded at 2026-10-23T02:42:59Z):

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone
```

New files were created with the specialized `write` tool (batched through `eval tool.write`), and the two existing documents received one-line insertions with `edit`. The exact construction is retained in the hashed construction JSON and archive below. Git staging and commit commands were:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 30 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone add -- /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/PROVINCE.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/SOURCES.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 45 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone -c user.name=ctl -c user.email=ctl@sandbox commit -m 'control: R30-C1 all-false committed envelopes'
```

Staging: 2026-10-23T02:44:29+00:00–2026-10-23T02:44:31+00:00, exit 0, empty stdout/stderr. The runner unset `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` for every sandbox Git command and every counter Git child.

### Eight refusal records

The first eight manifest IDs received exactly `{"ok":false}` plus one newline (13 bytes each):

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uv.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uvx.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uv.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uvx.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uv.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uvx.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uv.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvx.json`

Each refusal SHA-256: `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea`.

### Eight real null-metadata records

The remaining eight IDs received the **identical captured stdout bytes** from the single allowed non-carrier REA run; no JSON reserialization, subject rewrite, or evidence-ID rewrite was performed:

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvw.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uv.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvx.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvw.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uv.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uvx.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uv.json`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uvx.json`

The producing command, with cwd `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse`, was:

```sh
TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/tmp timeout 300 npx -y rea-agents@6.5.0 inspect-rust-binary /usr/bin/rg --format json --full-output
```

2026-10-23T02:42:59+00:00–2026-10-23T02:43:00+00:00; exit 0; empty stderr. Exact output excerpts from stdout line 1: `"ok":true`, `"operation":"inspect_rust_binary"`, `"auditable_metadata":null`, and `No .dep-v0 section was found.`

- Evidence ID: `ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2`.
- Subject `/usr/bin/rg` SHA-256: `d006acfe51619144af4709e85945fe3b5a6f05038d356c4d8f752a33b4ecae42`.
- Captured stdout and each of its eight copies SHA-256: `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c`. Full original JSON: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/rg-null.stdout`.

### Junk structural gates

New entry `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` names no evidence ID:

```markdown
# Round-30 junk all-false control

source: S089
verified-at: 2026-10-23

Junk control entry; no evidence.
```

The clone PROVINCE Core table received exactly:

```text
| inspect-rust-binary | junk | junk | corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md |
```

The clone source registry received exactly:

```text
| S089 | junk | junk | junk | junk | junk | junk | junk | 2026-10-23 | junk | corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md |
```

## Exact behavioral detector and all runs

All four executions used cwd `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse` and the same absolute-path equivalent of the assigned counter command:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/tmp timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone --rev main
```

The runner retained the real child exit code, stdout/stderr bytes, UTC endpoints and digests; its own wrapper completion is not substituted for the child result. Every counter stderr was empty.

| State | Revision read as main | UTC start → end | Counter exit |
|---|---|---|---|
| pristine | `4ee65c6771058284aa947a266475839d196ed4d4` | 2026-10-23T02:42:59+00:00 → 2026-10-23T02:42:59+00:00 | 2 |
| pristine-repaired | `4ee65c6771058284aa947a266475839d196ed4d4` | 2026-10-23T02:44:44+00:00 → 2026-10-23T02:44:58+00:00 | 1 |
| all-false | `6f8c4de93a4c1b1ecf1e920f7e704ff41b7d8c6f` | 2026-10-23T02:45:24+00:00 → 2026-10-23T02:45:37+00:00 | 1 |
| restored | `e31be5dbdf5dd2102a84f1a67d2366587f46bd3a` | 2026-10-23T02:46:04+00:00 → 2026-10-23T02:46:17+00:00 | 1 |

The repaired pristine measurement was run before the control commit: `main` still named the untouched freeze. Control files were already staged, but the counter reads entry, registry, province and envelopes through `git show main:...`; the worktree counter/oracle/manifest remained the frozen bytes.

### pristine: full counter stdout

```text
PIN carrier elf-x86_64-uvx absent or altered at /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

### pristine-repaired: full counter stdout

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

### all-false: full counter stdout

```text
elf-x86_64-uv	P1-fail	committed envelope not ok
elf-x86_64-uvx	P1-fail	committed envelope not ok
elf-aarch64-uv	P1-fail	committed envelope not ok
elf-aarch64-uvx	P1-fail	committed envelope not ok
elf-riscv64-uv	P1-fail	committed envelope not ok
elf-riscv64-uvx	P1-fail	committed envelope not ok
pe-x86_64-uv	P1-fail	committed envelope not ok
pe-x86_64-uvx	P1-fail	committed envelope not ok
pe-x86_64-uvw	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_ab1b78ca69fdcd71cb69faed3557e2f5794c94e37b8f33aea5c35728713288b2'
pe-arm64-uv	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_58d8e1f477c5dff8801fe1a2d6f6b81a9c26d69b1f09d0c4904c59d3ef86697e'
pe-arm64-uvx	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_ae58e67e96e716244041cb0292221bdeab86ef5731f890ad25b2bab9177ab7dc'
pe-arm64-uvw	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_6f00915a36c933a68fa819f36977f7085b980b7b2ffec1997a5bea93c51defc9'
macho-x86_64-uv	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_1c3ef6996f8f62f1eeffda94f2b5892763eda8b2f4a333c01311a11bf0c6af10'
macho-x86_64-uvx	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_02fb9f95c9b82c4a6ade2ea299e4fe85e193f821d406fa76feb0cfec709177b0'
macho-arm64-uv	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_7f9ac67aa01cc62f2a0a8d0d4bd50f34fd195523eaf73a6560ceb4b313b9b35d'
macho-arm64-uvx	P1-fail	committed evidence_id 'ev_9ea97685bf6313d1e1816a43ba644a25d68459d9ec37f06dfc1b39934eb1bff2' != live 'ev_6fcab3d46593ceb4056e5b67c540119f6fbdd113a79661462819e5317e3687f7'
carriers=16 pass=0 target=16 entry_ok=1 (ok) province_ok=1 (ok)
```

### restored: full counter stdout

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

## Observed rejection boundary

- **Observation:** Eight refusal records failed with exactly `committed envelope not ok`.
- **Observation:** The eight rg records failed with exactly `committed evidence_id ... != live ...`; the complete actual IDs are in the control stdout above.
- **Observation:** The junk entry, S089 row and PROVINCE line produced `entry_ok=1 (ok) province_ok=1 (ok)`, but none of the 16 carriers passed P1.
- **Inference from the counter control flow:** Each carrier reached `committed_check`, so its live positive-image checks had passed before its committed record was rejected. The null-metadata and entry-ID checks later in `committed_check` were not reached for the rg records: this probe must not be described as exercising those later gates.
- **Conclusion (observation):** The specified all-false control did not meet the frozen target. No contract, predicate, instrument, target, or carrier list was changed to obtain this result.

## Initial shared-input interference

The initial full counter stdout is preserved above, not discarded. It exited 2 before any carrier REA run because the pinned elf-x86_64-uvx bytes were altered. The separate diagnostic command was:

```sh
timeout 20 sha256sum /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

UTC 2026-10-23T02:43:35+00:00; exit 0; full stdout:

```text
9f41e2d43ca085f1200cd52f1856fa3e821a05942a90d8084122a9ad9ef903a1  /fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx
```

The frozen manifest expected `2e9105ad948131962cbe20502e406d571a22d11c2f9d62ec8c8b88798172890d`. **Observation (message received):** L1 reported restoration of four altered shared carriers from verified wheel members and setting all 16 immutable. **Observation:** the ensuing pristine/control/restored counters passed their PIN stage and measured all 16. **Unknown:** identity of the external writer. This seat performed no shared-carrier writes.

## Restoration and before/after evidence

After recording the control and archiving its exact changed/new files, the sandbox alone was restored with:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 45 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone -c user.name=ctl -c user.email=ctl@sandbox revert --no-edit 6f8c4de93a4c1b1ecf1e920f7e704ff41b7d8c6f
```

UTC 2026-10-23T02:45:56+00:00; exit 0. Output excerpt: `[main e31be5db] Revert "control: R30-C1 all-false committed envelopes"`; `19 files changed, 24 deletions(-)`. Restored main: `e31be5dbdf5dd2102a84f1a67d2366587f46bd3a`. The original control commit remains available in the sandbox history.

Snapshot producing command (run for pristine, control, restored; receipts record exact UTC and exit 0):

```sh
timeout 30 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/snapshot.py
```

| State | Git tree | SHA-256 of canonical affected/input path→SHA-or-null map |
|---|---|---|
| pristine | `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2` | `81eda3bffedba9d439f96799a9da84cd32bed7d50864ffb13dd579905ba0c278` |
| control | `30612519cec788c9c5eb827fd1d72e9c514b6b06` | `8092fc3fc9104e0566ab4eb2f638d4ad867b58976cfc227c0ea65941fab160a7` |
| restored | `ec1ae170932f89c3f8eab9b7f40a1c7c0a1cc7a2` | `81eda3bffedba9d439f96799a9da84cd32bed7d50864ffb13dd579905ba0c278` |

**Observation:** pristine and restored tree IDs and byte-state hashes are identical. PROVINCE.md and corpus/SOURCES.md are exact original bytes; all 16 added envelopes and the junk entry are absent again. The instrument/oracle/manifest/claim hashes are unchanged in all three snapshots.

**Inference:** restored per-row reasons differ from the first measured pristine run because the revert preserves historical envelope additions: `added_time` still finds those commits, while the current envelope is absent. This is a history-sensitive diagnostic difference, not a byte-restoration failure; both states score pass=0, entry_ok=0, province_ok=0.

| Affected sandbox file (absolute) | Before SHA-256 | Control SHA-256 | Restored SHA-256 |
|---|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/PROVINCE.md` | `4f94007f80be8b87fb4645b366a6e4a695f330da96bdf2dc058ab046db9d1e32` | `b72526bc4d6defda85091120ddf29ff06a9a927e8d7b890a1294df526ae95039` | `4f94007f80be8b87fb4645b366a6e4a695f330da96bdf2dc058ab046db9d1e32` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/SOURCES.md` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` | `037ec83e3a4b9b1c171500ef53a8d5c90ec4955cf3089deab5ad5755bb2417e6` | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uv.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-aarch64-uvx.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uv.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-riscv64-uvx.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uv.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/elf-x86_64-uvx.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uv.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-arm64-uvx.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uv.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/macho-x86_64-uvx.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uv.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvw.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-arm64-uvx.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uv.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvw.json` | `ABSENT` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/evidence/round-30/c1/envelopes/pe-x86_64-uvx.json` | `ABSENT` | `db8c4a0c90cdbbbda90af1d70d35adedce6ec6fb928a309e48992f548e425cea` | `ABSENT` |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md` | `ABSENT` | `5e47883f043a72e309084d766550085a13d42351b282958964335ed338cb7842` | `ABSENT` |

Exact control-record archive command (exit 0 at 2026-10-23T02:45:24+00:00):

```sh
timeout 30 git -C /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone archive --format=tar --output=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-tree.tar main PROVINCE.md corpus/SOURCES.md corpus/evidence/round-30/c1/envelopes corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md
```

## Opened primary/local sources

All accesses were ordinary local file reads; access date **2026-10-23**. Hashes identify complete served file bytes (the displayed quotations are located excerpts of at most 25 words). No external website, browser, CAPTCHA, or access-control bypass was used. Source identity hashes were produced by the command in the hashed source-hashes receipt, exit 0 at 2026-10-23T02:42:59Z. The rg binary identity is recorded separately above; the following rg-output source is the textual REA record.

| URL | SHA-256 | Located quote |
|---|---|---|
| file:///home/vgpnk/.omp/agent/RULES.md | `beb647d0d4bba504e918ae988335a43403c6cff7033e42e75a2577e9ca0999ed` | L5: `helps its task or is a strict upgrade, with full privilege, without asking first.` |
| file:///home/vgpnk/.agents/skills/godspeed/SKILL.md | `1d6167238784245e003d0c8d38197cc25824018545e31bc81de25edb38d5f83a` | L12: `1. **Name the axes.**` |
| file:///home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | L17: `## Run REA through the CLI — this host is CLI-first` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | L14: `and whose auditable_metadata package list equals` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c1-rust-positive.py | `e07563d6c0c27aafcf3996c363ec849951774ebd2fc4eda52e9f2384c323ed2a` | L188: `if not isinstance(committed, dict) or committed.get("ok") is not True:` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c1/carriers.tsv | `c968cd1e41bcda0e5f0714d659c7859febf90249415f2b6431f26203369e4e4b` | L3: `/fast/scratch/hyaku/kaidoku-r30/carriers/elf-x86_64-uvx` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/PROVINCE.md | `4f94007f80be8b87fb4645b366a6e4a695f330da96bdf2dc058ab046db9d1e32` | L38: `## Core` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md | `68d06a54d54ae13f04310f1d7e6fd1b451dcfcd17002ad411e606d171ed336ed` | L3: `## Registry` |
| file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-16-l7-02-inspect-rust-binary.md | `748525e9391a7104f35d81f566cb87389111893a94ce56c9c1b26c98bbbf7430` | L9: `Nulls are not evidence of missing dependencies or compilers;` |
| file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` | L4: `"version": "6.5.0",` |
| file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/rg-null.stdout | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | L1: `No .dep-v0 section was found.` |

## Retained artifact SHA-256 inventory

All paths below are absolute and under the assigned seat directory. The inherited sandbox repository is identified by commit/tree above; its 19 produced control files are individually hashed above and retained in the control archive after exact restoration. The temporary runtime cache was removed, not retained as evidence. This inventory includes every retained seat-produced script, recipe, raw output, receipt and archive outside the inherited clone.

| Artifact | SHA-256 | Bytes |
|---|---|---|
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/all-false.receipt.json` | `286d9f103f4d3f9a51556e2389af2141cbc1ce8c70041d2238697669191bbfa0` | 1036 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/all-false.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/all-false.stdout` | `425b3c637cc79e7ac2c509302d4ade0e326363f668668339b01a7d3df4fffbb5` | 1994 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/artifact-index.py` | `99944ab5e49520efccb5af71000f0fcd4931af4bfbdf87cb5b43863971f75bd0` | 720 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/artifact-index.receipt.json` | `7a8b2f94527d2a8facd914bc8b782c95d35725c1ece68713bc32fbb0538a6ad3` | 802 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/artifact-index.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/artifact-index.stdout` | `3a311ee5c4160de56ac484705dc78f9747a387de99f7cd6a1e53457ee57b5be7` | 10564 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/carrier-diagnostic.receipt.json` | `7645ce3cc63ae4fbca8da58d9e4642bcc5c545e92e487e7db0870f418c80e3b9` | 746 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/carrier-diagnostic.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/carrier-diagnostic.stdout` | `070800a0d6a7aaaff1e07661c65c765b2f866235665aadb953ba70a939b90b27` | 122 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/cleanup-cache.receipt.json` | `4caa23e8916a93a6e8f0c7b9c1894ebd3a5af730654ae742f2e68a67722a3ce1` | 804 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/cleanup-cache.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/cleanup-cache.stdout` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/construction.json` | `b2616d303ac7b21109f0098ca7fc1462f0608fa29d06ffbc41dd4a98f079e925` | 2469 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-add.receipt.json` | `7993e00bc16420c86295b45e9562affa8f663d399e9da2caef6598efc80d3c06` | 1555 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-add.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-add.stdout` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-archive.receipt.json` | `01f176cf8ea1d965303190f38577e8903e205ed18f431aebb16f69b01e99e518` | 1281 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-archive.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-archive.stdout` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-bytes.receipt.json` | `1dd8ee6c88bb03d6315defde680c232e56789a1558bf1ab26b1d7bb387e37b99` | 790 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-bytes.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-bytes.stdout` | `e2e08ea18dba30b88fd69609eb351488bb746cbe3ff526c364cd4c1e75dbac68` | 4497 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-commit.receipt.json` | `f651bcd6f6a9e4ef3e8bd4db3be321ca040845b847c91a261bdfe94b216918c6` | 1006 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-commit.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-commit.stdout` | `3e8aa9d9551113fa8cc4f40c98b7c92c8640fb5a532d9958d4f6e6f6eeb5cacf` | 1419 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/control-tree.tar` | `e8b21754a9dec66cd7d2edf48f6b0077b9533d90459974da6b883af7e95e00b7` | 184320 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-bytes.receipt.json` | `0982572adca755bf602d9e1c44fdea1b62a67d0f355672d0f4eca729fe419127` | 790 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-bytes.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-bytes.stdout` | `8def34320940e8628da28a70768ee109ab61432bfd5c3cb01e9352e6089f584c` | 3443 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-repaired.receipt.json` | `370f16ce6c952e1df1982985aa3ffa2029705c2a15f5fb81617d84bd68a49db3` | 1036 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-repaired.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-repaired.stdout` | `afa4cc794aad76161a1570f46fde93e024585c61a98b441dbf216124bceba98b` | 1394 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-tree.receipt.json` | `679f0fe5013bca6612161f6ea49787eafd471536426607e6137528ae12c91c93` | 834 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-tree.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine-tree.stdout` | `9f9de7463d85364e79c7e794ee993b4cf12a55a070c93140682cbd4d85b54ded` | 82 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine.receipt.json` | `d979e95a5a323014aede758d93218468109f914b294c497b7c7f013e06e2a0a0` | 1036 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/pristine.stdout` | `cfb493f83436e46c5c431a5fd421d2ad26e97be0df0eab13ed745b43708e4278` | 104 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restore.receipt.json` | `d4c46efc745770a52ef019a384646600b14353eaad8c5e7448e236e6dbd224db` | 1008 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restore.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restore.stdout` | `5119a394aa57c237f38aae7be090a6ee40ee78749cb5a3081878c5f42b3215e4` | 1465 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restored-bytes.receipt.json` | `5651b66fff2c71fc5348020a137279b0289ff1cb9bc13ae29137e5c2a843ce16` | 790 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restored-bytes.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restored-bytes.stdout` | `74cd5780ea0b5c3fa8209a74325262f1b99fe8ea87d74c96ee0dc6b4cb0605fd` | 3443 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restored.receipt.json` | `836c224e6b5c66e89c7284f102224198c71e021c78e72901ede9e32103fae288` | 1036 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restored.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/restored.stdout` | `06e640bd4b5f511bcfb33fe02ab89226cbd43aeabe3aae6636304d8ee308bd04` | 914 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/rg-null.receipt.json` | `9f704b7767ccdf79d18ef945473dfbc91b33e31f2e7a45d9e22a35d64063b73e` | 826 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/rg-null.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/rg-null.stdout` | `180a240935d1b8a03660c91262e5f2402c4c5ac68d04cc3617cd5c2a39902d2c` | 2665 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/run-command.py` | `30e563df1bf6407f15937f7dd3c9f7835198dc05989bc31993084fa9f38261d7` | 1920 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/snapshot.py` | `19e2b6faa837dfa07df709ea2dc1baa9afa7f5f5339c05169c9efc38fdf39c28` | 1370 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/source-hashes.receipt.json` | `e50e8a0467f3d63d319ba8609a139324eabe8a33adb143d8510a0fe4862f9465` | 2112 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/source-hashes.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/source-hashes.stdout` | `8ea342147709b2c52cc735daf798be31c94a7ed1cdde0c473bc5c0cddb99706b` | 1430 |

CONTROL CtlC1AllFalse met_target=no
