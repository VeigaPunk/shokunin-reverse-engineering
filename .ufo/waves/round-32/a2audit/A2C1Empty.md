EMPTY CONTROL REJECTED: the provider-bound frozen counter reported carriers=12 pass=0 target=12 entry_ok=1 province_ok=1; exit 1. No shortcut met the frozen target in this control.

# A2C1Empty — new attempt-2 pre-data control

UTC report timestamp: 2026-10-23T06:52:44+00:00
Seat: KaidokuR32A2.A2C1Empty

## Axes and counterexample

- Coverage: C1 ARM64X hybrid PE Frontier→Core. Counterexample attempted: add an S099-bearing entry and a real row inside the pre-existing `## Core` table, with no envelope files at all. This is stronger than an unchanged-tree control because both documentation gates are green.
- Calibration: avoid treating documentation as demonstrated coverage, or a provider failure as discrimination. No C2 counter was run by this seat.
- Observed scope: one new sandbox fixture commit, one initial environment-masked scoring run, and one scoring run with the actual missing provider-environment prerequisites supplied. No unchanged scoring retry.
- Canonical admission/judgment: not performed by this seat. The findings below report the frozen counter's output only.

## Sandbox identity and construction

Sandbox: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone`
Frozen parent: `f382e3b7978e6091a19ca93277c15a75c0016b43` (f382e3b7).
Control revision: `e8e468b74471e9f32359e709b0ed94e72a0b22d6`.
Author and committer: `ctl <ctl@local>`; exactly one fixture commit; no amend.
Round base from the frozen claims: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
C1 freeze remains 9a73680a; C2 v3 freeze remains f382e3b7. Both claims files were read; neither was edited.

Setup command (observed exit 0; timestamps for this first shell command were not captured):

```sh
mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone checkout --detach f382e3b7
```

Full setup output:

```text
Cloning into '/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone'...
done.
HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) — anchored evidence and description, before receipts
```

Before construction, `df -h /fast` exited 0 and printed:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  559G  245G  70% /fast
```

Only fixture paths changed: `PROVINCE.md` and `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md`. Their complete resulting files total 41,583 bytes (40,766 + 817), below 1 MiB; the diff adds ten lines. Fixture/metadata subprocesses in the recorded receipt had RLIMIT_AS=4,294,967,296 bytes. Ghidra scoring was deliberately not given that address-space cap. No carrier rebuild or carrier execution occurred.

Committed envelope absence command (exit 0, empty stdout and stderr):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone ls-tree -r --name-only e8e468b74471e9f32359e709b0ed94e72a0b22d6 -- corpus/evidence/round-32/c1/envelopes
```

The tool directory read of sandbox `corpus/evidence/round-32/c1` showed only `inputs/`, `predictions.tsv`, and `carriers.tsv`; no envelope directory was present. The S099 citation is the frozen claim's citation, not a claim that this seat independently re-opened or learned from the external Microsoft page. `corpus/SOURCES.md` was intentionally unchanged: this is a negative-control fixture, not a capability entry for admission.

## Initial masked receipt — not discrimination evidence

UTC 2026-10-23T06:47:26+00:00 → 2026-10-23T06:47:35+00:00.
Exact argv:

```sh
timeout --signal=TERM --kill-after=10s 900s python3 -I -B tools/round-32/c1-arm64x-positive.py --root /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone --rev e8e468b74471e9f32359e709b0ed94e72a0b22d6
```

Execution cwd: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone`. GIT_DIR, GIT_WORK_TREE, and GIT_INDEX_FILE were absent from the subprocess environment. Eval's GHIDRA_INSTALL_DIR and JAVA_HOME were both null (recorded independently at 2026-10-23T06:48:06Z). Other checked REA_GHIDRA_* override keys were also null. Counter exit: 1; stderr: empty; outer timeout: false.

Full stdout:

```text
k01	P1-fail	exit 1 ok False
k02	P1-fail	exit 1 ok False
k03	P1-fail	exit 1 ok False
k04	P1-fail	exit 1 ok False
k05	P1-fail	exit 1 ok False
k06	P1-fail	exit 1 ok False
k07	P1-fail	exit 1 ok False
k08	P1-fail	exit 1 ok False
k09	P1-fail	exit 1 ok False
k10	P1-fail	exit 1 ok False
k11	P1-fail	exit 1 ok False
k12	P1-fail	exit 1 ok False
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

All failures occurred at the live-REA status gate, before the committed-envelope comparison. Raw inner REA envelopes/errors are not emitted or retained by the frozen counter in measure mode; this seat did not invent their contents. This run alone is unevaluable as evidence for Empty-control discrimination.

The independent shell diagnostic `printenv GHIDRA_INSTALL_DIR JAVA_HOME` exited 0 and returned:

```text
/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC
/usr/lib/jvm/java-21-openjdk
```

This observed difference supplied a concrete missing prerequisite. The next run changed only those two environment keys, not the fixture, counter, inputs, revision, predicate, or target.

## Provider-bound scoring receipt

UTC 2026-10-23T06:48:54+00:00 → 2026-10-23T06:50:36+00:00.
Exact argv was unchanged:

```sh
timeout --signal=TERM --kill-after=10s 900s python3 -I -B tools/round-32/c1-arm64x-positive.py --root /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone --rev e8e468b74471e9f32359e709b0ed94e72a0b22d6
```

Explicit environment overrides:

```text
GHIDRA_INSTALL_DIR=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC
JAVA_HOME=/usr/lib/jvm/java-21-openjdk
```

Execution cwd: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone`. GIT_DIR, GIT_WORK_TREE, and GIT_INDEX_FILE remained unset. GNU timeout cap: 900 seconds, TERM then KILL after 10 seconds. Counter exit: 1; stderr: empty; outer timeout: false. No --write-evidence invocation occurred.

Full stdout, including every P1 verdict and the final counter line:

```text
k01	P1-fail	committed envelope absent
k02	P1-fail	committed envelope absent
k03	P1-fail	committed envelope absent
k04	P1-fail	committed envelope absent
k05	P1-fail	committed envelope absent
k06	P1-fail	committed envelope absent
k07	P1-fail	committed envelope absent
k08	P1-fail	committed envelope absent
k09	P1-fail	committed envelope absent
k10	P1-fail	committed envelope absent
k11	P1-fail	committed envelope absent
k12	P1-fail	committed envelope absent
carriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)
```

Frozen requested target: `carriers=12 pass=12 target=12 entry_ok=1 province_ok=1`, exit 0.
Observed provider-bound result: `carriers=12 pass=0 target=12 entry_ok=1 province_ok=1`, exit 1.

Evidence boundary: the reason `committed envelope absent` is directly observed for k01–k12. [INFERENCE from frozen source flow] reaching that reason means the earlier live-result judge returned P1-pass for each carrier; raw live REA exit/envelope values are not separately printed by measure mode. The result is bounded to these twelve frozen inputs and this Empty fixture. It does not establish counter soundness against any other control.

## Re-opened source evidence

Source re-opened 2026-10-23: [sandbox counter, lines 109–113](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone/tools/round-32/c1-arm64x-positive.py#L109), revision `e8e468b74471e9f32359e709b0ed94e72a0b22d6`, SHA-256 `7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a`. Exact three-word reason at line 113: “committed envelope absent”. Lines 198–202 condition the committed check on the preceding P1-pass result. Lines 219–223 require all twelve passes plus both doc gates for exit 0. This is source-flow evidence, not an additional test or an amendment to the frozen predicate.

## Smallest safe correction and limitations

No counter correction is indicated by this control; do not weaken, repair, or rescale the frozen target. The execution harness must supply the configured GHIDRA_INSTALL_DIR and JAVA_HOME values when using Eval subprocesses; retain both receipts so the original masked failure cannot be mistaken for discrimination. No coverage gain or canonical round admission is claimed. The missing committed envelopes are deliberate, not a fixture defect to repair.

Process cleanup: initial scoring group 3278168: ProcessLookupError: no process group remained after counter exit. Provider-bound scoring group 3479765: ProcessLookupError: no process group remained after counter exit. Every other launched command was synchronous and had exited before report construction. No long-lived service was started.

Tool installs/updates: none explicitly performed. Existing pinned rea-agents@6.5.0 was invoked only by the frozen counter. Operator RULES.md was read before construction; no pacman transaction occurred. No model/runtime reroute, delegation, fleet/sibling production write, lane Git/jj write, or held-item inspection occurred.

## File hashes

Exact argv (cwd `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone`, observed exit 0, stderr empty):

```sh
sha256sum tools/round-32/c1-arm64x-positive.py tools/round-32/arm64x_oracle.py tools/round-32/build-arm64x-carriers.sh .ufo/waves/round-32/claims.json .ufo/waves/round-32/claims-v3.json corpus/evidence/round-32/c1/carriers.tsv corpus/evidence/round-32/c1/predictions.tsv corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s PROVINCE.md corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json
```

Full stdout:

```text
7a534be655f940728879e1d25e43a20685371e25232ded94eeb2d5bcc0800f1a  tools/round-32/c1-arm64x-positive.py
17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686  tools/round-32/arm64x_oracle.py
7da284da5986295263c69a8b7ee779638428d3bb6c9d5c9d8fb224c40a737ba3  tools/round-32/build-arm64x-carriers.sh
8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  .ufo/waves/round-32/claims.json
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  .ufo/waves/round-32/claims-v3.json
8cf97b37f72bf5b494ac5993a88051e4697038c8f66606e2a6e17fda1bf3d16e  corpus/evidence/round-32/c1/carriers.tsv
fd8049498e519d13c9bd28415327a0bafa75c43684b2d1998d8e5d769737c56b  corpus/evidence/round-32/c1/predictions.tsv
7c29f128a447f8ce481159961b14932d7011c6af3bc55a1830387d433864ba2d  corpus/evidence/round-32/c1/inputs/loadconfig-arm64.s
c043b74850a4c3033d21fa22701eb808a6b0bd5b46fd2bfab08d4ae43332c0d4  corpus/evidence/round-32/c1/inputs/loadconfig-arm64ec.s
9af2f732046e9bcbd6d65ee6e2b89017bdd04c6dba3b3e75873812682fc0b12f  PROVINCE.md
fb69ecaa72a82c29602bd07b53123004b7abed8da093fa1f842a915c09af3dad  corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c  /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json
```

The counter, oracle, builder, carrier manifest, predictions, and two assembler input hashes equal the values in frozen claims.json. The fixture diff below leaves those files untouched.

## Complete fixture diff

Exact argv (UTC 2026-10-23T06:51:09+00:00, exit 0, stderr empty):

```sh
git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone show --format=fuller --no-ext-diff --binary --unified=0 e8e468b74471e9f32359e709b0ed94e72a0b22d6 -- PROVINCE.md corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
```

Full stdout:

```diff
commit e8e468b74471e9f32359e709b0ed94e72a0b22d6
Author:     ctl <ctl@local>
AuthorDate: Fri Oct 23 03:46:59 2026 -0300
Commit:     ctl <ctl@local>
CommitDate: Fri Oct 23 03:46:59 2026 -0300

    control: round-32 attempt-2 C1 Empty (doc gates only)

diff --git a/PROVINCE.md b/PROVINCE.md
index d9d4cf4c..df633cc2 100644
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -51,0 +52 @@ Surfaces owned now — each verified on this host 2026-10-13.
+| ARM64X hybrid PE (`inspect`) | Frozen round-32 carriers, REA 6.5.0 | `npx -y rea-agents@6.5.0 inspect <carrier> --format json --full-output` | Empty negative-control fixture only; no committed envelopes: `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` |
diff --git a/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
new file mode 100644
index 00000000..db1e1b51
--- /dev/null
+++ b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md
@@ -0,0 +1,9 @@
+source: S099 — Microsoft Learn, Arm64X PE files — https://learn.microsoft.com/en-us/windows/arm/arm64x-pe (citation fixed by the round-32 claim)
+verified-at: 2026-10-23 (empty-control construction only; no capability verified)
+recheck: python3 -I -B tools/round-32/c1-arm64x-positive.py --root <sandbox-clone> --rev <committed-control-revision>
+
+# Round 32 C1 — Empty control
+
+This isolated negative-control fixture contains the S099 citation and an actual row in the existing Core table. It deliberately contains no committed REA envelope and names no evidence ID. No carrier observation or ARM64X capability is asserted here.
+
+The fixture isolates the frozen counter's committed-envelope requirement from its documentation gates. It is not production evidence and must not be admitted as a capability record.
```

## Structured command receipt

All captured command argv, UTC boundaries, exits, stdout, stderr, caps, and scoring-process cleanup details follow. Capture records used subprocess argument arrays, not shell interpolation. Git environment keys were unset for every listed git call; commit identity overrides are included separately.

```json
{
  "report_utc": "2026-10-23T06:52:44+00:00",
  "base_revision": "f382e3b7978e6091a19ca93277c15a75c0016b43",
  "control_revision": "e8e468b74471e9f32359e709b0ed94e72a0b22d6",
  "git_environment_unset": [
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE"
  ],
  "commit_identity_environment": {
    "GIT_AUTHOR_NAME": "ctl",
    "GIT_AUTHOR_EMAIL": "ctl@local",
    "GIT_COMMITTER_NAME": "ctl",
    "GIT_COMMITTER_EMAIL": "ctl@local"
  },
  "initial_eval_provider_environment": {
    "GHIDRA_INSTALL_DIR": null,
    "JAVA_HOME": null,
    "REA_GHIDRA_COMMAND": null,
    "REA_GHIDRA_PYTHON": null,
    "REA_GHIDRA_STARTUP_TIMEOUT_MS": null
  },
  "steps": [
    {
      "utc_start": "2026-10-23T06:46:58+00:00",
      "utc_end": "2026-10-23T06:46:58+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "git",
        "-C",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
        "rev-parse",
        "HEAD"
      ],
      "exit": 0,
      "stdout": "f382e3b7978e6091a19ca93277c15a75c0016b43\n",
      "stderr": "",
      "memory_cap_bytes": 4294967296
    },
    {
      "utc_start": "2026-10-23T06:46:58+00:00",
      "utc_end": "2026-10-23T06:46:59+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "git",
        "-C",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
        "add",
        "--",
        "PROVINCE.md",
        "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
      ],
      "exit": 0,
      "stdout": "",
      "stderr": "",
      "memory_cap_bytes": 4294967296
    },
    {
      "utc_start": "2026-10-23T06:46:59+00:00",
      "utc_end": "2026-10-23T06:46:59+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "git",
        "-C",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
        "-c",
        "user.name=ctl",
        "-c",
        "user.email=ctl@local",
        "-c",
        "commit.gpgSign=false",
        "commit",
        "--no-verify",
        "-m",
        "control: round-32 attempt-2 C1 Empty (doc gates only)",
        "--",
        "PROVINCE.md",
        "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
      ],
      "exit": 0,
      "stdout": "[detached HEAD e8e468b7] control: round-32 attempt-2 C1 Empty (doc gates only)\n 2 files changed, 10 insertions(+)\n create mode 100644 corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md\n",
      "stderr": "",
      "memory_cap_bytes": 4294967296
    },
    {
      "utc_start": "2026-10-23T06:46:59+00:00",
      "utc_end": "2026-10-23T06:46:59+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "git",
        "-C",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
        "rev-parse",
        "HEAD"
      ],
      "exit": 0,
      "stdout": "e8e468b74471e9f32359e709b0ed94e72a0b22d6\n",
      "stderr": "",
      "memory_cap_bytes": 4294967296
    },
    {
      "utc_start": "2026-10-23T06:47:26+00:00",
      "utc_end": "2026-10-23T06:47:35+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "timeout",
        "--signal=TERM",
        "--kill-after=10s",
        "900s",
        "python3",
        "-I",
        "-B",
        "tools/round-32/c1-arm64x-positive.py",
        "--root",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
        "--rev",
        "e8e468b74471e9f32359e709b0ed94e72a0b22d6"
      ],
      "exit": 1,
      "stdout": "k01\tP1-fail\texit 1 ok False\nk02\tP1-fail\texit 1 ok False\nk03\tP1-fail\texit 1 ok False\nk04\tP1-fail\texit 1 ok False\nk05\tP1-fail\texit 1 ok False\nk06\tP1-fail\texit 1 ok False\nk07\tP1-fail\texit 1 ok False\nk08\tP1-fail\texit 1 ok False\nk09\tP1-fail\texit 1 ok False\nk10\tP1-fail\texit 1 ok False\nk11\tP1-fail\texit 1 ok False\nk12\tP1-fail\texit 1 ok False\ncarriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)\n",
      "stderr": "",
      "outer_timeout": false,
      "memory_cap_bytes": null,
      "process_group": 3278168,
      "cleanup": "ProcessLookupError: no process group remained after counter exit"
    },
    {
      "utc_start": "2026-10-23T06:48:54+00:00",
      "utc_end": "2026-10-23T06:50:36+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "timeout",
        "--signal=TERM",
        "--kill-after=10s",
        "900s",
        "python3",
        "-I",
        "-B",
        "tools/round-32/c1-arm64x-positive.py",
        "--root",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
        "--rev",
        "e8e468b74471e9f32359e709b0ed94e72a0b22d6"
      ],
      "environment_overrides": {
        "GHIDRA_INSTALL_DIR": "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC",
        "JAVA_HOME": "/usr/lib/jvm/java-21-openjdk"
      },
      "exit": 1,
      "stdout": "k01\tP1-fail\tcommitted envelope absent\nk02\tP1-fail\tcommitted envelope absent\nk03\tP1-fail\tcommitted envelope absent\nk04\tP1-fail\tcommitted envelope absent\nk05\tP1-fail\tcommitted envelope absent\nk06\tP1-fail\tcommitted envelope absent\nk07\tP1-fail\tcommitted envelope absent\nk08\tP1-fail\tcommitted envelope absent\nk09\tP1-fail\tcommitted envelope absent\nk10\tP1-fail\tcommitted envelope absent\nk11\tP1-fail\tcommitted envelope absent\nk12\tP1-fail\tcommitted envelope absent\ncarriers=12 pass=0 target=12 entry_ok=1 (ok) province_ok=1 (ok)\n",
      "stderr": "",
      "outer_timeout": false,
      "memory_cap_bytes": null,
      "process_group": 3479765,
      "cleanup": "ProcessLookupError: no process group remained after counter exit"
    },
    {
      "utc_start": "2026-10-23T06:51:09+00:00",
      "utc_end": "2026-10-23T06:51:09+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "git",
        "-C",
        "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
        "show",
        "--format=fuller",
        "--no-ext-diff",
        "--binary",
        "--unified=0",
        "e8e468b74471e9f32359e709b0ed94e72a0b22d6",
        "--",
        "PROVINCE.md",
        "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
      ],
      "exit": 0,
      "stdout": "commit e8e468b74471e9f32359e709b0ed94e72a0b22d6\nAuthor:     ctl <ctl@local>\nAuthorDate: Fri Oct 23 03:46:59 2026 -0300\nCommit:     ctl <ctl@local>\nCommitDate: Fri Oct 23 03:46:59 2026 -0300\n\n    control: round-32 attempt-2 C1 Empty (doc gates only)\n\ndiff --git a/PROVINCE.md b/PROVINCE.md\nindex d9d4cf4c..df633cc2 100644\n--- a/PROVINCE.md\n+++ b/PROVINCE.md\n@@ -51,0 +52 @@ Surfaces owned now — each verified on this host 2026-10-13.\n+| ARM64X hybrid PE (`inspect`) | Frozen round-32 carriers, REA 6.5.0 | `npx -y rea-agents@6.5.0 inspect <carrier> --format json --full-output` | Empty negative-control fixture only; no committed envelopes: `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md` |\ndiff --git a/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md\nnew file mode 100644\nindex 00000000..db1e1b51\n--- /dev/null\n+++ b/corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md\n@@ -0,0 +1,9 @@\n+source: S099 — Microsoft Learn, Arm64X PE files — https://learn.microsoft.com/en-us/windows/arm/arm64x-pe (citation fixed by the round-32 claim)\n+verified-at: 2026-10-23 (empty-control construction only; no capability verified)\n+recheck: python3 -I -B tools/round-32/c1-arm64x-positive.py --root <sandbox-clone> --rev <committed-control-revision>\n+\n+# Round 32 C1 — Empty control\n+\n+This isolated negative-control fixture contains the S099 citation and an actual row in the existing Core table. It deliberately contains no committed REA envelope and names no evidence ID. No carrier observation or ARM64X capability is asserted here.\n+\n+The fixture isolates the frozen counter's committed-envelope requirement from its documentation gates. It is not production evidence and must not be admitted as a capability record.\n",
      "stderr": "",
      "memory_cap_bytes": 4294967296
    },
    {
      "utc_start": "2026-10-23T06:51:09+00:00",
      "utc_end": "2026-10-23T06:51:09+00:00",
      "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C1Empty/clone",
      "argv": [
        "wc",
        "-c",
        "PROVINCE.md",
        "corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md"
      ],
      "exit": 0,
      "stdout": "40766 PROVINCE.md\n  817 corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md\n41583 total\n",
      "stderr": "",
      "memory_cap_bytes": 4294967296
    }
  ]
}
```

Report: .ufo/waves/round-32/a2audit/A2C1Empty.md
