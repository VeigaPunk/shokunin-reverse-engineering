CONTROL REJECTED: all 12 JSON-null envelopes failed committed/live comparison; target not met, exit 1. This control did not falsify C1.

# A2C1Garbage — new end-to-end C1 Garbage control

- Receipt UTC observation: 2026-10-23T06:48:50Z. Launch-batch UTC observation: 2026-10-23T06:47:10Z; measured wall time 91.37 seconds. These are outer observations, not per-carrier timestamps.
- Axes: **coverage** (C1, exercised); **calibration** (C2 context read, not scored here). No depth claim or canonical admission judgment.
- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, production files read-only except this assigned report.
- Owned scratch: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage`.
- Sandbox: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox`.
- Starting revision: `f382e3b7978e6091a19ca93277c15a75c0016b43` (C1 unchanged at freeze `9a73680a`, base `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`). Read both claims.json C1 and claims-v3.json C2.
- Exactly one fixture commit: `a1335f9e16e6209c443721f970f654074d033a22`, author and committer `ctl <ctl@local>`, UTC commit time 2026-10-23T06:46:45Z. This is a sandbox-only commit, not a lane commit.
- Exactly one scoring invocation; no `--write-evidence`, counter/input modification, carrier execution, rebuild, delegation, model switch, or held-item access.

## Counterexample and bounded result

All `k01.json` through `k12.json` were newly committed as the five bytes `null\n` (JSON null), not junk rows. A new entry cites S099 and a table row under the existing Core heading names ARM64X and that entry. The fixture deliberately supplies the two documentation gates without any committed REA envelope or evidence ID.

Observed: every carrier was `P1-fail` specifically because its committed envelope differs from its live envelope. Both documentation gates were 1. The final target was not met:

```text
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
Command exited with code 1
```

[INFERENCE from the executed, hashed source] The live oracle/REA predicate succeeded before each committed comparison: `measure` invokes `committed_check` only after the live verdict equals P1-pass (counter lines 198–202). Thus these are not provider-failure rejections. Measure mode does not emit the raw per-REA envelopes, stderr, exits, or timestamps; none are claimed as separately observed receipts.

Impacted axis: coverage provenance. This control tests rejection of committed JSON null despite live reader success and passing document gates; it does not establish general malformed-envelope coverage, C2 calibration, or actual coverage acquisition.

Smallest safe correction: none indicated by this control. Keep the frozen counter, predicate, inputs and target unchanged. Preserve this negative-control fixture/receipt before data; do not integrate its counterfeit Core row as lane knowledge. Canonical acceptance remains outside this review.

## Exact scoring invocation and full receipt

Working directory:

```text
/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox
```

Exact shell command (tool timeout 920 seconds; launched counter bounded by GNU timeout 900 seconds, TERM then KILL after 10 seconds):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout --signal=TERM --kill-after=10s 900 python3 -I -B tools/round-32/c1-arm64x-positive.py --root /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox --rev a1335f9e
```

The revision argument resolves to the full committed sandbox revision above. Observed job `bg_98`, complete output:

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

Wall time: 91.37 seconds

Command exited with code 1
```

No separate counter stderr was displayed. The tool labels nonzero exit as failed; here exit 1 is the observed negative-control outcome, not a timeout.

### Resolved provider environment

Exact command, same Bash environment and sandbox working directory, exit 0:

```sh
printenv GHIDRA_INSTALL_DIR JAVA_HOME
```

Full stdout:

```text
/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC
/usr/lib/jvm/java-21-openjdk
```

Both values were already exported for the sole Bash scoring run. No provider-failure receipt occurred in this seat. No unchanged retry was performed after the parent reported other seats' Eval environment omissions.

Frozen source `run_rea`, lines 95–100, constructs the following argv once per pinned path, with cwd `/tmp`, a cleaned Git environment, and timeout 600 seconds:

```text
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k01.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k02.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k03.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k04.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k05.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k06.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k07.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k08.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k09.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k10.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k11.dll", "--format", "json", "--full-output"]
["npx", "-y", "rea-agents@6.5.0", "inspect", "/fast/scratch/hyaku/kaidoku-r32/carriers/k12.dll", "--format", "json", "--full-output"]
```

These argv are source-derived, not separately traced subprocess receipts. The frozen counter itself performed the live REA scoring.

## Construction and command evidence

All Git invocations used absolute `-C` and unset `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`. No lane/fleet Git write occurred.

1. Capacity, exact argv `df -h /fast`, exit 0:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  559G  245G  70% /fast
```

No rebuild was performed.

2. Frozen revision resolution, exact command, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse f382e3b7
```

```text
f382e3b7978e6091a19ca93277c15a75c0016b43
```

3. Clone and checkout, exact commands, both exit 0:

```sh
mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin sandbox
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox checkout --detach f382e3b7978e6091a19ca93277c15a75c0016b43
```

```text
Cloning into 'sandbox'...
done.
HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) — anchored evidence and description, before receipts
```

4. Fixture files were created using the write tool; Core row inserted using the edit tool. Exact committed diff follows below. Twelve envelope writes were 5 bytes each; the new entry was 213 bytes. `wc -c` measured the entire 14 affected files at 40,953 bytes, including the complete 40,680-byte PROVINCE.md, below 1 MiB. Fixture staging/commit were capped at 4 GiB virtual address space; no such limit was imposed on Ghidra.

5. Exact staging and sole commit command, timeout 900, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox add -- PROVINCE.md corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md corpus/evidence/round-32/c1/envelopes && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE prlimit --as=4294967296 -- git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox -c user.name=ctl -c user.email=ctl@local -c commit.gpgsign=false -c core.hooksPath=/dev/null commit -m 'control(round-32): A2 C1 JSON-null garbage envelopes'
```

Full stdout:

```text
[detached HEAD a1335f9e] control(round-32): A2 C1 JSON-null garbage envelopes
 14 files changed, 18 insertions(+)
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k01.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k02.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k03.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k04.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k05.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k06.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k07.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k08.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k09.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k10.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k11.json
 create mode 100644 corpus/evidence/round-32/c1/envelopes/k12.json
 create mode 100644 corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
```

6. Exact fixture-diff capture command, exit 0:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox show --format=fuller --binary --no-ext-diff a1335f9e -- PROVINCE.md corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md corpus/evidence/round-32/c1/envelopes
```

Its full output was also retained at `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/fixture.patch`, SHA-256 `b1d8a7e1a40fa28d3914d268c67dde9bbeb3005f3cb96088d1695aad43009240`.

## Observed SHA-256 identities

Hashes below were observed with `sha256sum`; paths are relative to the sandbox except the explicitly absolute package/patch paths. The counter, oracle, carrier list and predictions match their C1 frozen hashes in claims.json.

```text
7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a  tools/round-32/c1-arm64x-positive.py
17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686  tools/round-32/arm64x_oracle.py
8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e  corpus/evidence/round-32/c1/carriers.tsv
fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b  corpus/evidence/round-32/c1/predictions.tsv
8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  .ufo/waves/round-32/claims.json
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  .ufo/waves/round-32/claims-v3.json
3eca3d36ddcf01b8a5026e798eaeeb52e9ce6596bd54f65ef174647d3021af63  PROVINCE.md
d65a4840d10a08cc3546756936103d9450015c226875165fdbb23e299e73751b  corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k01.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k02.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k03.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k04.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k05.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k06.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k07.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k08.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k09.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k10.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k11.json
38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed  corpus/evidence/round-32/c1/envelopes/k12.json
a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json
b1d8a7e1a40fa28d3914d268c67dde9bbeb3005f3cb96088d1695aad43009240  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/fixture.patch
```

### Reopened source evidence

Reopened the actual sandbox counter after the run at lines 69–87, 109–126 and 193–205. The relevant source quote at line 122 is: “committed envelope differs from the live envelope (full comparison)”. Location: `tools/round-32/c1-arm64x-positive.py:121–122`; URL: `file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Garbage/sandbox/tools/round-32/c1-arm64x-positive.py`; reopened 2026-10-23, revision `a1335f9e16e6209c443721f970f654074d033a22`, SHA-256 `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a`.

## Full fixture diff

This is the captured fixture artifact, not a proposed lane cutover:

```diff
commit a1335f9e16e6209c443721f970f654074d033a22
Author:     ctl <ctl@local>
AuthorDate: Fri Oct 23 03:46:45 2026 -0300
Commit:     ctl <ctl@local>
CommitDate: Fri Oct 23 03:46:45 2026 -0300

    control(round-32): A2 C1 JSON-null garbage envelopes

diff --git a/PROVINCE.md b/PROVINCE.md
index d9d4cf4c..1be84559 100644
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -41,6 +41,7 @@ Surfaces owned now — each verified on this host 2026-10-13.
 
 | Surface | Ports / paths / config keys | Liveness / readiness probe | Verified evidence |
 |---|---|---|---|
+| ARM64X hybrid PE (Garbage negative control) | Frozen round-32 carriers | JSON null envelopes; not coverage evidence | `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` |
 | REA MCP server | `~/.config/devin/mcp_config.json` + `~/.omp/agent/mcp.json` + `~/.kimi-code/config.toml` — config files pin `rea-agents` (Devin/OMP/Kimi 6.7.0 since 2026-10-20 13:35:56 -03; see surface summary) with env `GHIDRA_INSTALL_DIR`, `JAVA_HOME` | `binary_session {}` would inspect a running attached client; not exercised this round. CLI: `rea doctor` (6.7.0 doctor: no devin/omp registration finding, separate Kimi JSON registration missing) | round-19 re-grepped pin/sha256 record `.ufo/waves/round-19/evidence/province-pins-integrated.json`; doctor outputs in `evidence/doctor/`; historical readiness probe 2026-10-13 |
 | `rea` CLI | npx cache `~/.npm/_npx/*/node_modules/rea-agents` — no `rea` on PATH; 153 commands on the 6.5.0/6.7.0 pins, 127 on 6.4.0 (historical) | `npx -y rea-agents@6.4.0 --version` → `6.4.0` (2026-10-13 receipt) | wave 01/02/03 catalogs |
 | Ghidra provider | `GHIDRA_INSTALL_DIR` (876 MB install); headless `support/analyzeHeadless`; native decompiler `Ghidra/Features/Decompiler/os/linux_x86_64/decompile`; 39 processor modules; 34 features incl. PyGhidra/BSim | `rea doctor` → providerInspections `ghidra: configured+available`, 8/8 checks | `application.version=12.1.4`, build 2026-09-21, rev 8b6bbb85 |
diff --git a/corpus/evidence/round-32/c1/envelopes/k01.json b/corpus/evidence/round-32/c1/envelopes/k01.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k01.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k02.json b/corpus/evidence/round-32/c1/envelopes/k02.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k02.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k03.json b/corpus/evidence/round-32/c1/envelopes/k03.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k03.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k04.json b/corpus/evidence/round-32/c1/envelopes/k04.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k04.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k05.json b/corpus/evidence/round-32/c1/envelopes/k05.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k05.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k06.json b/corpus/evidence/round-32/c1/envelopes/k06.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k06.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k07.json b/corpus/evidence/round-32/c1/envelopes/k07.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k07.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k08.json b/corpus/evidence/round-32/c1/envelopes/k08.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k08.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k09.json b/corpus/evidence/round-32/c1/envelopes/k09.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k09.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k10.json b/corpus/evidence/round-32/c1/envelopes/k10.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k10.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k11.json b/corpus/evidence/round-32/c1/envelopes/k11.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k11.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/evidence/round-32/c1/envelopes/k12.json b/corpus/evidence/round-32/c1/envelopes/k12.json
new file mode 100644
index 00000000..19765bd5
--- /dev/null
+++ b/corpus/evidence/round-32/c1/envelopes/k12.json
@@ -0,0 +1 @@
+null
diff --git a/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
new file mode 100644
index 00000000..e9ad2574
--- /dev/null
+++ b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
@@ -0,0 +1,5 @@
+# Round-32 ARM64X hybrid PE — Garbage negative control
+
+Source citation: S099.
+
+All twelve committed envelope files contain JSON `null`. This control does not record ARM64X coverage or claim a live evidence ID.
```

## Closure

- Sent the completed job's kill request via `write proc://bg_98/kill`. Tool response: `Background job bg_98 is already failed.` The counter parent had exited; detached-descendant status was not separately observed.
- No tools installed or updated; existing REA 6.5.0 cache used.
- No production code/docs/index or lane/fleet Git/jj state was written. No fixture retry or unrelated verification was run.
- Full receipt and fixture diff are retained above so L1 can commit the control record before data.

Report: .ufo/waves/round-32/a2audit/A2C1Garbage.md
