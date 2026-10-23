CONTROL TARGET NOT MET — prescribed C2v3 NoReader vocabulary/README shortcut was rejected (exit 1).

# A2C2NoReader — new attempt-2 end-to-end control

UTC report: 2026-10-23T06:49:40.301534+00:00

## Counterexample, axes, and bounded finding

- **Calibration:** exercised. Four rows take their first and second cells verbatim from the four pinned MANIFEST capability labels, name their corresponding rounds, and use the same irrelevant `README.md` evidence cell. No capability evidence content was opened.
- **Coverage:** ARM64X Frontier→Core was not exercised by this seat. No depth measurement or axis score is claimed.
- **Observed:** `statements=4 match=0 target=4 reverse_mismatch=4`, exit **1**, on exactly one frozen-counter run. All four forward diagnostics stop at the resolving-anchor requirement; all four rows also produce reverse mismatches.
- **Target:** `statements=4 match=4 target=4 reverse_mismatch=0`, exit **0**. It was not met. This is not a passing vocabulary shortcut or a first-line FALSIFIED/honest-stop finding.
- **Smallest safe correction:** none to counter, predicate, target, or lane data. Retain this rejected control; do not present it as an honest calibration repair. No admission or canonical-judge decision is made here.
- **Limit:** this one failed shortcut does not establish that other NoReader controls fail, nor that anchor contents demonstrate the claimed capabilities. The description-overlap branch was not reached for these rows (source control flow at `tools/round-32/c2-capability-calibration-v3.py:163-170`).

## Frozen inputs and isolation

- Scratch/clone: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone`.
- Starting freeze: `f382e3b7978e6091a19ca93277c15a75c0016b43`.
- Sandbox committed revision: `b8c508e0059fcb79eab240101fd37b2b820cf9be`.
- Base referenced by the unchanged counter: `283aad7fe56d82f4ed4f8e43f099c2e1ceed5525`.
- Fleet pin: `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.
- Only `SCORECARD.md`'s Capabilities section was changed in the clone. Commit stdout records one changed file, four insertions, seven deletions. Full requested diff is below.
- The production lane received only this scoped Report. No fleet/sibling files, lane code/docs/index, routes, or production Git/jj state were written by issued commands. All direct Git write commands used the absolute sandbox `-C` path with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` absent from the environment.
- The counter's mandated `--fleet` argument is the real fleet path; the frozen counter performs its own read-only pinned-object lookup there. For fixture-label extraction only, the same fleet commit was fetched into the sandbox object database; the worktree remained on the lane freeze until the control commit.
- No underlying capability evidence was opened or executed. The irrelevant README was checked with `git cat-file -e`, not read; its content was only hashed. The counter itself reads the pinned MANIFEST and base/candidate SCORECARD, enumerates tree paths, and does not execute the anchor files.
- No REA, Ghidra, carrier executable, model/runtime switch, or delegation was used. No held item or attempt-1 control was inspected or retried.

### Source locations

The actual pinned MANIFEST blob was opened by the sandbox `git show` command recorded below before generating the four rows. Its complete blob is 1242275 bytes, SHA-256 `2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f`; only the four relevant labels are retained as fixture bytes. Source object location: `cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json` in [sandbox Git objects](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.git), opened 2026-10-23 UTC.

- round 13: `MANIFEST.json:6311` at `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.
- round 14: `MANIFEST.json:7195` at `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.
- round 17: `MANIFEST.json:8293` at `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.
- round 27: `MANIFEST.json:13932` at `cef00867ab3279ac2c2d10421e3e62c0e5d693f3`.

The actual frozen counter's anchor gate was reopened at lines 154–183 on 2026-10-23 UTC: [local frozen source](file:///fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py), SHA-256 `5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f`. No prose source quotations are used; the complete fixture and Git diff below are retained artifacts.

## Complete generated Capabilities section

UTF-8 bytes: 1077; SHA-256 `3e218997840072acafbad5e8612a176557ae17678d108d6074f02655af775888`. Generation rule: emit the existing section/table headings, then one row per `(round, capabilities_added item)` at the fleet pin, setting cells to `[item, item, backticked README.md, round N]`, followed by one blank line. This section replaces everything from `## Capabilities` up to (not including) the next level-two heading.

```markdown
## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | `README.md` | round 13 |
| local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence) | local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence) | `README.md` | round 14 |
| retained REA Ghidra-session log capture | retained REA Ghidra-session log capture | `README.md` | round 17 |
| cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27) | cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27) | `README.md` | round 27 |

```

## Exact counter invocation and complete result

UTC start: 2026-10-23T06:47:40.200973+00:00  
UTC end: 2026-10-23T06:47:40.253877+00:00  
CWD: `/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone`

```sh
timeout 300 python3 -I -B tools/round-32/c2-capability-calibration-v3.py --root /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone --rev b8c508e0059fcb79eab240101fd37b2b820cf9be --fleet /home/vgpnk/Projects/shokunin
```

Exact argv is also retained in the command ledger below. Python subprocess environment had the three Git override variables unset. The fixture process tree had `RLIMIT_AS=4294967296` bytes and `RLIMIT_FSIZE=1048576` bytes; GNU `timeout 300` bounded the counter, with an outer 310-second cleanup guard. Observed exit: **1**; no timeout.

Complete stdout:

```text
round-13	P2-mismatch	row 1 evidence names no resolving anchor path (anchors: corpus/SOURCES.md, corpus/lessons/round-13.md)
round-14	P2-mismatch	row 2 evidence names no resolving anchor path (anchors: .ufo/waves/round-14/fixtures/expected.json, .ufo/waves/round-14/tools/quote-fidelity.py, .ufo/waves/round-14/verification.json)
round-17	P2-mismatch	row 3 evidence names no resolving anchor path (anchors: .ufo/waves/round-17/run-carriers.sh)
round-27	P2-mismatch	row 4 evidence names no resolving anchor path (anchors: tools/round-27/xpin-attribute.mjs)
reverse	P2-mismatch	row 1 names MANIFEST-closed round(s) [13] without a credited capability
reverse	P2-mismatch	row 2 names MANIFEST-closed round(s) [14] without a credited capability
reverse	P2-mismatch	row 3 names MANIFEST-closed round(s) [17] without a credited capability
reverse	P2-mismatch	row 4 names MANIFEST-closed round(s) [27] without a credited capability
statements=4 match=0 target=4 reverse_mismatch=4
```

Complete stderr: empty.

The irrelevant file resolves at the committed revision: `git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone cat-file -e b8c508e0059fcb79eab240101fd37b2b820cf9be:README.md` exited 0 with empty stdout and stderr. Resolution alone did not satisfy the frozen anchor requirement.

## Complete committed diff

Command: `git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone diff --no-ext-diff --no-textconv f382e3b7978e6091a19ca93277c15a75c0016b43 b8c508e0059fcb79eab240101fd37b2b820cf9be -- SCORECARD.md`. Exit 0; stderr empty. Full stdout (3383 UTF-8 bytes):

```diff
diff --git a/SCORECARD.md b/SCORECARD.md
index e90a5a01..0586746e 100644
--- a/SCORECARD.md
+++ b/SCORECARD.md
@@ -616,13 +616,10 @@ Retired: none.
 
 | Capability | What it can now do | Evidence pointer | First-working round |
 |---|---|---|---|
-| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |
-| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |
-| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s — the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) — before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |
-| contained user-service analyze of oversized PEs (analyzer-disable recipe) | runs REA/Ghidra analyzes of 91.6MB-class PEs as caller-independent systemd user services with registry-validated analyzer disables and memory caps — the paired demonstrations: r7 wall-fall (ev_a4aa9b0d…) and the r8 natural control (oom-kill; disable proven necessary) | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` | arc2-loop1-round7 |
-| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |
-
-Rows entered through rounds that demonstrated each capability running (`AXES.md` §Capabilities); the conformance rollout itself entered none.
+| source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | `README.md` | round 13 |
+| local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence) | local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence) | `README.md` | round 14 |
+| retained REA Ghidra-session log capture | retained REA Ghidra-session log capture | `README.md` | round 17 |
+| cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27) | cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27) | `README.md` | round 27 |
 
 ## Saturation
 
```

## File hashes and sizes

Frozen SCORECARD before replacement: SHA-256 `bba9f55de85001d6259ed728bdec82a20dd49830ccb9e01634909bb14c9c38e3`.

Post-commit hash command: `sha256sum /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/README.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims-v3.json /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims.json`; exit 0; stderr empty.

```text
00e2be3a2066c46b9ef394da0b278878cdc2c45381e412d8e9ed4c2957a939c1  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md
63ffe86cc6e62ae770bb3e7d52890f8a098527b44066ce11a03a63fdd6a2d06e  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/README.md
5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py
a3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims-v3.json
8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims.json
```

Size command: `stat -c '%s %n' /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py`; exit 0; stderr empty.

```text
273054 /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md
15665 /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py
```

The candidate SCORECARD and all generated fixture/receipt/report artifacts are below 1 MiB. Git object transport is repository metadata, not a generated fixture payload.

## Preparation observations and process cleanup

Before clone creation, `df -h /fast` exited 0 and printed:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1p2  804G  559G  245G  70% /fast
```

Initial UTC checkpoint: `2026-10-23T06:45:23Z`. Exact clone setup command (cwd `/fast/scratch/hyaku/kaidoku-r32`, tool timeout 650 seconds; each Git command separately bounded to 300 seconds):

```sh
mkdir -p /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone clone --no-local --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kaidoku-shokunin . && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300 git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone checkout --detach f382e3b7
```

Observed successful exit 0, full relevant output:

```text
Cloning into '.'...
HEAD is now at f382e3b7 round-32: freeze R32-C2 v3 (supersedes v2 before any seat or data: an irrelevant-path control met v2) — anchored evidence and description, before receipts
```

The first fleet-object fetch was additionally constrained by a 1-MiB per-file limit and exited 128 (`fatal: fetch-pack: invalid index-pack output`). The clone's empty FETCH_HEAD was reopened. Only that preparation fetch was retried, with the Git transport file-size limit removed while retaining the 4-GiB address-space cap; it exited 0. The causal role of the file-size limit in the first error is [INFERENCE]; the before/after results are observed. No scored control was retried or modified after scoring.

Every subprocess launched by the receipt runner used its own process group; its group received SIGKILL cleanup after synchronous collection (including on timeout), ignoring only ProcessLookupError when already gone. The earlier bounded clone/checkout completed synchronously. No long-lived service was started.

Installed/updated tools: **none**. Exercised versions: Python 3.14.8; Git 2.56.0.

## Exact command ledger

Each entry retains UTC, argv, cwd, exit, limits, and full relevant stdout/stderr. The sole large MANIFEST stdout is reduced to its four relevant labels, with complete blob hash/size retained; no underlying evidence bytes are substituted. The initial failed fetch has a real 1-MiB file-size limit; subsequent Git transport commands do not.

```json
[
  {
    "utc_start": "2026-10-23T06:46:10.826586+00:00",
    "utc_end": "2026-10-23T06:46:11.223435+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "fetch",
      "--no-tags",
      "/home/vgpnk/Projects/shokunin",
      "cef00867ab3279ac2c2d10421e3e62c0e5d693f3"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone fetch --no-tags /home/vgpnk/Projects/shokunin cef00867ab3279ac2c2d10421e3e62c0e5d693f3",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": 1048576,
    "exit": 128,
    "timed_out": false,
    "stdout": "",
    "stderr": "fatal: fetch-pack: invalid index-pack output\n"
  },
  {
    "utc_start": "2026-10-23T06:46:40.318367+00:00",
    "utc_end": "2026-10-23T06:46:40.980347+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "fetch",
      "--no-tags",
      "/home/vgpnk/Projects/shokunin",
      "cef00867ab3279ac2c2d10421e3e62c0e5d693f3"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone fetch --no-tags /home/vgpnk/Projects/shokunin cef00867ab3279ac2c2d10421e3e62c0e5d693f3",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "",
    "stderr": "From /home/vgpnk/Projects/shokunin\n * branch              cef00867ab3279ac2c2d10421e3e62c0e5d693f3 -> FETCH_HEAD\n"
  },
  {
    "utc_start": "2026-10-23T06:46:40.980458+00:00",
    "utc_end": "2026-10-23T06:46:40.984137+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "show",
      "cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone show cef00867ab3279ac2c2d10421e3e62c0e5d693f3:MANIFEST.json",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stderr": "",
    "stdout_relevant": {
      "fleet_revision": "cef00867ab3279ac2c2d10421e3e62c0e5d693f3",
      "source": "MANIFEST.json",
      "source_sha256": "2e089615936dae60d1b4ab3883dbbc8ed7608018b9c7f4694209207d84b3207f",
      "source_bytes": 1242275,
      "statements": [
        {
          "round": 13,
          "label": "source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim)",
          "lines": [
            6311
          ]
        },
        {
          "round": 14,
          "label": "local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence)",
          "lines": [
            7195
          ]
        },
        {
          "round": 17,
          "label": "retained REA Ghidra-session log capture",
          "lines": [
            8293
          ]
        },
        {
          "round": 27,
          "label": "cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27)",
          "lines": [
            13932
          ]
        }
      ]
    },
    "stdout_omission": "Unrelated MANIFEST entries omitted; full source hash and byte count retained."
  },
  {
    "utc_start": "2026-10-23T06:46:40.987895+00:00",
    "utc_end": "2026-10-23T06:46:40.989051+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "rev-parse",
      "HEAD"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone rev-parse HEAD",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "f382e3b7978e6091a19ca93277c15a75c0016b43\n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:46:40.989104+00:00",
    "utc_end": "2026-10-23T06:46:40.990427+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "python3",
      "--version"
    ],
    "shell_display": "python3 --version",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "Python 3.14.8\n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:46:40.990488+00:00",
    "utc_end": "2026-10-23T06:46:40.991583+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "--version"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone --version",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "git version 2.56.0\n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:47:39.324617+00:00",
    "utc_end": "2026-10-23T06:47:40.195001+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "-c",
      "core.hooksPath=/dev/null",
      "-c",
      "commit.gpgsign=false",
      "-c",
      "user.name=A2C2NoReader control",
      "-c",
      "user.email=a2c2noreader@invalid",
      "commit",
      "--only",
      "--no-verify",
      "--no-gpg-sign",
      "-m",
      "r32 a2 control: manifest-label NoReader capabilities with README pointers",
      "--",
      "SCORECARD.md"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone -c core.hooksPath=/dev/null -c commit.gpgsign=false -c 'user.name=A2C2NoReader control' -c user.email=a2c2noreader@invalid commit --only --no-verify --no-gpg-sign -m 'r32 a2 control: manifest-label NoReader capabilities with README pointers' -- SCORECARD.md",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "[detached HEAD b8c508e0] r32 a2 control: manifest-label NoReader capabilities with README pointers\n 1 file changed, 4 insertions(+), 7 deletions(-)\n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:47:40.195125+00:00",
    "utc_end": "2026-10-23T06:47:40.196900+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "rev-parse",
      "HEAD"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone rev-parse HEAD",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "b8c508e0059fcb79eab240101fd37b2b820cf9be\n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:47:40.196999+00:00",
    "utc_end": "2026-10-23T06:47:40.199729+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "diff",
      "--no-ext-diff",
      "--no-textconv",
      "f382e3b7978e6091a19ca93277c15a75c0016b43",
      "b8c508e0059fcb79eab240101fd37b2b820cf9be",
      "--",
      "SCORECARD.md"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone diff --no-ext-diff --no-textconv f382e3b7978e6091a19ca93277c15a75c0016b43 b8c508e0059fcb79eab240101fd37b2b820cf9be -- SCORECARD.md",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "diff --git a/SCORECARD.md b/SCORECARD.md\nindex e90a5a01..0586746e 100644\n--- a/SCORECARD.md\n+++ b/SCORECARD.md\n@@ -616,13 +616,10 @@ Retired: none.\n \n | Capability | What it can now do | Evidence pointer | First-working round |\n |---|---|---|---|\n-| pre-registered two-lane live battery on REA 6.5.0 | runs a 10-leg frozen-prediction battery with hashed per-lane receipts and cross-lane replay verification | `.ufo/waves/luna-round-6/receipts/` + `receipts-B/`; report `.ufo/reports/luna-round-6/kaidoku.md` | luna-round-6 |\n-| version-symmetry battery on REA 6.4.0 | repeats the battery form on the second pin, proving per-name 6.5-only absence/refusal with a live control leg | `.ufo/waves/luna-round-8/receipts/`; `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` | luna-round-8 |\n-| config custody pre/post-pair for live-probe rounds | freezes the five operator paths' sha256s \u2014 the three client configs (Devin mcp_config.json, OMP mcp.json, Kimi config.toml) plus the two shell env carriers (~/.bashrc, ~/.profile) \u2014 before the round's first probe and re-verifies byte-identity after the battery closes, producing a zero-drift 6-line 5-hash receipt pair | `.ufo/waves/arc2-loop1-round2/receipts/config-pre-pair.txt` + `config-post-pair.txt`; comparison in `.ufo/reports/arc2-loop1-round2/kaidoku.md` | arc2-loop1-round2 |\n-| contained user-service analyze of oversized PEs (analyzer-disable recipe) | runs REA/Ghidra analyzes of 91.6MB-class PEs as caller-independent systemd user services with registry-validated analyzer disables and memory caps \u2014 the paired demonstrations: r7 wall-fall (ev_a4aa9b0d\u2026) and the r8 natural control (oom-kill; disable proven necessary) | `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` + `.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json` | arc2-loop1-round7 |\n-| cross-pin evidence-ID attribution for saved REA envelopes | attributes a saved envelope to the `rea-agents` 6.5.0 id rule, the 6.7.0 rule, both or neither, from its bytes, using each installed package's own canonical digest code | `tools/round-27/xpin-attribute.mjs`; checker `tools/round-27/c2-xpin-check.py`; seat report `.ufo/waves/round-27/w1/BuildXpinTool.md`; receipts `corpus/evidence/round-27/c2/` | round 27 |\n-\n-Rows entered through rounds that demonstrated each capability running (`AXES.md` \u00a7Capabilities); the conformance rollout itself entered none.\n+| source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | source-curation registry (22 opened rows, scoped tiers, ordered study paths, reasoned rejection; no domain-operation claim) | `README.md` | round 13 |\n+| local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence) | local raw-quote/heading regression audit (bounded retained-defect controls; committed CLI and frozen evidence) | `README.md` | round 14 |\n+| retained REA Ghidra-session log capture | retained REA Ghidra-session log capture | `README.md` | round 17 |\n+| cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27) | cross-pin evidence-ID attribution for saved REA envelopes (tools/round-27/xpin-attribute.mjs, SCORECARD ## Capabilities, first-working round 27) | `README.md` | round 27 |\n \n ## Saturation\n \n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:47:40.199807+00:00",
    "utc_end": "2026-10-23T06:47:40.200921+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "git",
      "-C",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "cat-file",
      "-e",
      "b8c508e0059fcb79eab240101fd37b2b820cf9be:README.md"
    ],
    "shell_display": "git -C /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone cat-file -e b8c508e0059fcb79eab240101fd37b2b820cf9be:README.md",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:47:40.200973+00:00",
    "utc_end": "2026-10-23T06:47:40.253877+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "timeout",
      "300",
      "python3",
      "-I",
      "-B",
      "tools/round-32/c2-capability-calibration-v3.py",
      "--root",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
      "--rev",
      "b8c508e0059fcb79eab240101fd37b2b820cf9be",
      "--fleet",
      "/home/vgpnk/Projects/shokunin"
    ],
    "shell_display": "timeout 300 python3 -I -B tools/round-32/c2-capability-calibration-v3.py --root /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone --rev b8c508e0059fcb79eab240101fd37b2b820cf9be --fleet /home/vgpnk/Projects/shokunin",
    "timeout_seconds": 310,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": 1048576,
    "exit": 1,
    "timed_out": false,
    "stdout": "round-13\tP2-mismatch\trow 1 evidence names no resolving anchor path (anchors: corpus/SOURCES.md, corpus/lessons/round-13.md)\nround-14\tP2-mismatch\trow 2 evidence names no resolving anchor path (anchors: .ufo/waves/round-14/fixtures/expected.json, .ufo/waves/round-14/tools/quote-fidelity.py, .ufo/waves/round-14/verification.json)\nround-17\tP2-mismatch\trow 3 evidence names no resolving anchor path (anchors: .ufo/waves/round-17/run-carriers.sh)\nround-27\tP2-mismatch\trow 4 evidence names no resolving anchor path (anchors: tools/round-27/xpin-attribute.mjs)\nreverse\tP2-mismatch\trow 1 names MANIFEST-closed round(s) [13] without a credited capability\nreverse\tP2-mismatch\trow 2 names MANIFEST-closed round(s) [14] without a credited capability\nreverse\tP2-mismatch\trow 3 names MANIFEST-closed round(s) [17] without a credited capability\nreverse\tP2-mismatch\trow 4 names MANIFEST-closed round(s) [27] without a credited capability\nstatements=4 match=0 target=4 reverse_mismatch=4\n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:48:01.776906+00:00",
    "utc_end": "2026-10-23T06:48:01.783849+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "sha256sum",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/README.md",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims-v3.json",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims.json"
    ],
    "shell_display": "sha256sum /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/README.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims-v3.json /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims.json",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "00e2be3a2066c46b9ef394da0b278878cdc2c45381e412d8e9ed4c2957a939c1  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md\n63ffe86cc6e62ae770bb3e7d52890f8a098527b44066ce11a03a63fdd6a2d06e  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/README.md\n5955e8ace76d93c7891a43ca282f129c8874cd1878a05c9f29e0b81d3cab2f9f  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py\na3be7e40df5a96cfa50df192adaef5b8f7b1c6e1470c560510f872185ec5171d  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims-v3.json\n8aa0672cf60d40b7afc53ebc4714e22c3e9f138d4af7ab0abc5039930878b435  /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/.ufo/waves/round-32/claims.json\n",
    "stderr": ""
  },
  {
    "utc_start": "2026-10-23T06:48:23.415357+00:00",
    "utc_end": "2026-10-23T06:48:23.418869+00:00",
    "cwd": "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone",
    "argv": [
      "stat",
      "-c",
      "%s %n",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md",
      "/fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py"
    ],
    "shell_display": "stat -c '%s %n' /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py",
    "timeout_seconds": 300,
    "memory_limit_bytes": 4294967296,
    "file_size_limit_bytes": null,
    "exit": 0,
    "timed_out": false,
    "stdout": "273054 /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/SCORECARD.md\n15665 /fast/scratch/hyaku/kaidoku-r32/a2audit/A2C2NoReader/clone/tools/round-32/c2-capability-calibration-v3.py\n",
    "stderr": ""
  }
]
```

Report: .ufo/waves/round-32/a2audit/A2C2NoReader.md
