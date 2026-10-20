# MutMidmap — round 19 wave 2 mutation probe

## Findings and calibration

- **[OBSERVATION] Assigned file-regression mutant: KILLED.** At pristine `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, `routed-r18.py --strict` returned **0**, `open_count=0`. After restoring **only** `.ufo/waves/round-17/tools/receipt-validate.py` to B bytes and committing `a4cf7e0693bee96d52aef6dd9fcd86ac83d5e272` in the private clone, the same detector returned **1**, `open_count=1`, and **R18-MIDMAP-LISTSTEP alone reopened** (`named=true`, `substance=false`). With the original bytes restored and committed as `6b4d5ac09a9852d22bada62e1521e57a5169fc2a`, the same detector returned **0**, `open_count=0`.
- **[OBSERVATION] Non-subcommand argument bypass already exists in pristine bytes.** A checked `inspect-go-binary` step whose filename argument is exactly `analyze` and an unchecked actual `analyze` step passed the **full** receipt validator with `--require-mid-maps` (exit 0, no findings). A checked `search` step with `--pattern analyze` did too. These remained accepted after restoration. This is not a mutant kill: both fail the challenged invariant before mutation.
- **[OBSERVATION] Duplicate/conflicting identity inputs are also accepted.** Two `analyze` entries with duplicate `step` or duplicate `name`, only the first checked, passed. An inspect step with contradictory `step`/`name` declarations, one of them `analyze`, also rescued the unchecked actual analyze step in either field order.
- **[INFERENCE / LIMIT]** The argument cases violate the documented **subcommand** boundary. The duplicate/conflict observations expose an ambiguity/coverage gap; the current prose does not explicitly define identity precedence, uniqueness, or whether every repeated analyze entry must be checked. Their proposed red expectations are explicitly hypotheses, not a newly imposed contract or four additional demonstrated regressions. No production repair, integration, or overall-round judgment is made here.

Axes named for this probe: **calibration** (separate killed regression from pre-existing gaps and undefined identity policy), **freshness** (pin the observed main tip and re-observe it at the end), **depth** (two non-subcommand cases, duplicate `step`/`name`, both conflicting-field directions, full-validator controls).

## Scope and freshness

- Private `tempfile.mkdtemp(prefix="kr19-w2-MutMidmap-")` clone: `/tmp/kr19-w2-MutMidmap-t6nvjpq3`. Cloned with `--no-hardlinks`, then detached explicitly at the observed main tip.
- Main tip at both observations: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; commit metadata: `2026-10-20T16:15:31-03:00 round-19: wave-two assignment records and verification expected-red safeguards`.
- Probe window: **2026-10-20T19:15:52.527715+00:00 → 2026-10-20T19:17:18.517603+00:00**.
- B: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. The mutant is a commit atop the observed tip, **not** a checkout of the whole repository to B.
- The only tracked path changed by the mutant commit is `.ufo/waves/round-17/tools/receipt-validate.py`; the actual `diff-tree` output is retained below. The restored commit's complete tracked tree equals the observed tip's tree.
- The detector used was the cloned copy of the assigned tool `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/routed-r18.py`. Its bytes matched that supplied absolute path before the probe and stayed unchanged across all three runs: SHA-256 `dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b`.
- Production writes: **this report only**. All Git writes, fixture creation, and tests were in the private scratch clone (the routed detector itself extracts revision objects to its own temporary directories). No delegation, builds, broad suite, formatter, REA/Ghidra invocation, carrier execution, client-config access, or installs/updates. Existing tools: Python **3.14.8**, Git **2.56.0**; no installation channel/record needed because nothing was installed or updated.

## Expected detector and exact source anchors

All repository-relative anchors here refer to `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` unless a revision is explicitly named; they were read from the lane or its identical clone.

- Claim C1 and its stated counting command: `.ufo/waves/round-19/claims.json:10-14`; unchanged C1 amendment: `:38`.
- Original routed requirement: `corpus/lessons/round-18-verifier-spotcheck.md:193` (list checks must be on analyze, not any step).
- Documented list identity boundary: `.ufo/waves/round-17/tools/receipt-validate.py:34-39`, `:134-149`, `:486-491`.
- Behavior-bearing points: `_is_analyze_step` returns true for either declared identity (`:145-147`) or **membership anywhere** in argv (`:148-149`); list validation then uses `any` across matching entries (`:602-611`). There is no uniqueness/all-matching-entries test in this branch. **[INFERENCE]** This explains the accepted arguments and ambiguous-identity fixtures; it is not evidence of real REA execution.
- Routed expected red/green pair: `.ufo/waves/round-19/tools/routed-r18.py:90-115`; it imports tools from the requested revision, places checks only on inspect for red, then only on analyze for green. Evaluation records substance/named status and counts open defects at `:292-312`; strict exit selection is at `:401-403`.
- **Detector limitation by inspection:** its `pc` at `:97-98` has no retained map; `:110` checks only presence of `mid_checks_absent`, not absence of every finding. Therefore its word “clean” at `:115` is scoped to that code, not full-receipt validity. The supplemental cases below use actual retained map bytes, real `pins.snapshot`/`pins.compare`, and the full validator CLI, rather than treating that narrow green as full validation.

## Restoration and hash evidence

| State | Commit | Validator SHA-256 | Routed strict exit | open / named-open / substance-open |
|---|---|---|---:|---|
| pristine | `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` | `9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45` | 0 | 0 / 0 / 0 |
| B-file mutant | `a4cf7e0693bee96d52aef6dd9fcd86ac83d5e272` | `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145` | 1 | 1 / 0 / 1 |
| restored | `6b4d5ac09a9852d22bada62e1521e57a5169fc2a` | `9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45` | 0 | 0 / 0 / 0 |

The B Git blob and mutated working file both hashed to Git object `bf0438862c41cb8ff2170396184f3db2a36d6e04`. Restored full-tree identity and observed full-tree identity both were `b344427155950539dd93926882071beea28970a4`. Restoration executed in a Python `finally` block around mutation and detectors, before any result interpretation. Detector subprocesses had a 180-second bound; each supplemental validator subprocess had a 30-second bound. Mutated routed/identity probes ran concurrently; restored routed/identity probes also ran concurrently. The restoration waited for both mutated probes to finish, avoiding mixed-byte reads.

**Verdict:** the single assigned file-revert mutant is **KILLED**, not inconclusive: its baseline was green, it made precisely the targeted routed substance check red, and exact-byte restoration returned it to green. The supplemental baseline counterexamples are **existing coverage findings**, not additional mutants or kills.

## Supplemental full-validator observations

The synthetic-only driver is `/tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py:18-87` (fixture creation) and `:90-110` (fixed-manifest checks and bounded CLI collection), SHA-256 `c1363f54dd7bd6b864856bc3620a27b9feb0ee8d7b21cd305a568a49f3ec3f0b`.

Fixed fixture directory: `/tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz`. Manifest: `/tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json`, SHA-256 `393ade40ac4ddf5310bd8a0ccf50f4d7618bbb029a058d1d982d83ccc854e178`. Fixtures were generated once while pristine, then reused unchanged for mutant and restored runs; the driver checks each receipt hash before each CLI run. Actual map, pinned text-file, and synthetic log commitments are rechecked by the validator. The file named `analyze` is plain fixture text, never executed. The synthetic log uses the repository selftest's binding-record syntax; it is **not** an observed REA/Ghidra log and does not claim an analysis occurred. No recorded receipt argv was executed.

| Fixture | Pristine exit | Mutated exit | Restored exit | Observed findings |
|---|---:|---:|---:|---|
| `control_off_analyze` | 1 | 0 | 1 | pristine/restored: `mid_checks_absent` at `$.steps[1].pin_checks`; mutant: none |
| `control_on_analyze` | 0 | 0 | 0 | none |
| `argv_filename_token` | 0 | 0 | 0 | none |
| `argv_search_pattern_token` | 0 | 0 | 0 | none |
| `duplicate_step_identity` | 0 | 0 | 0 | none |
| `duplicate_name_identity` | 0 | 0 | 0 | none |
| `conflicting_step_name` | 0 | 0 | 0 | none |
| `conflicting_name_step` | 0 | 0 | 0 | none |

Exact fixture anchors (all below `/tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/`):

- `argv_filename_token.receipt.json:68-80`: argv subcommand is `inspect-go-binary`, filename argument at `:73` is `analyze`, checks begin `:80`; real analyze argv is `:98-105` and its checks are empty at `:110`.
- `argv_search_pattern_token.receipt.json:68-82`: argv subcommand is `search`, `--pattern` value at `:75` is `analyze`; real analyze argv is `:100-107`, empty checks at `:112`.
- `duplicate_step_identity.receipt.json:68-96,99-117`: both subcommands and `step` declarations are analyze; first checks begin `:80`, second checks are empty at `:111`.
- `duplicate_name_identity.receipt.json:68-81,99-112`: both subcommands and `name` declarations are analyze; first checked, second empty.
- `conflicting_step_name.receipt.json:68-97,100-112`: checked inspect has `name=analyze` at `:80` and `step=inspect-go-binary` at `:97`; actual analyze checks empty at `:112`.
- `conflicting_name_step.receipt.json:68-97,100-112`: checked inspect has `name=inspect-go-binary` at `:80` and `step=analyze` at `:97`; actual analyze checks empty at `:112`.
- Controls: `control_off_analyze.receipt.json:68-110`; `control_on_analyze.receipt.json:68-100`.

**[OBSERVATION]** All accepted receipts reported `counts={invalid:0, receipts:1, unreadable:0, valid:1}`, `findings=[]`, stderr empty. The off-analyze red control reported one invalid receipt and precisely the absent-check finding in pristine/restored. The collector's process exit 0 means it collected results, **not** that every challenged invariant passed. Its `expected_exit=1` on duplicates/conflicts denotes the explicitly labeled hypothesis above.

**[INFERENCE]** The fixed two-fixture routed detector distinguishes the assigned old any-step implementation but does not establish correct subcommand parsing or unambiguous per-analyze identity. Pristine/restored `open_count=0` coexists with the two demonstrated argument-boundary counterexamples. No claim is made about affected retained object-shaped receipts or C2/C3 artifacts.

## Actual commands, exit codes, and captured output

The transcript below contains actual executed argv and stdout/stderr (no hypothetical reruns). Concurrent subprocess results are listed in completion order. These two shell observations were additionally made outside the collector:

```text
$ git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
exit=0
$ python3 --version && git --version
Python 3.14.8
git version 2.56.0
exit=0
```

```text
$ git clone -q --no-hardlinks --branch main /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-w2-MutMidmap-t6nvjpq3
exit=0
```

```text
$ git -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 checkout -q --detach d0690fd44f46d8a7fe9da5f01c6be723d12abd41
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 rev-parse HEAD
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 log -1 '--format=%H %cI %s' d0690fd44f46d8a7fe9da5f01c6be723d12abd41
d0690fd44f46d8a7fe9da5f01c6be723d12abd41 2026-10-20T16:15:31-03:00 round-19: wave-two assignment records and verification expected-red safeguards
exit=0
```

```text
$ sha256sum /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-19/tools/routed-r18.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/routed-r18.py
9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45  /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py
dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-19/tools/routed-r18.py
dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/tools/routed-r18.py
exit=0
```

```text
$ python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutMidmap-t6nvjpq3 --rev d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --strict
{
  "defects": [
    {
      "id": "R18-MIDMAP-LISTSTEP",
      "named": true,
      "substance": true,
      "why": "non-analyze-only list receipt -> mid_checks_absent; analyze-carrying list receipt clean"
    },
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    },
    {
      "id": "R18-STRICT-BASELINE",
      "named": true,
      "substance": true,
      "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"
    },
    {
      "id": "R18-HEAD-ALIASES",
      "named": true,
      "substance": true,
      "why": "6 aliases exit 2, refs/heads/main evaluates; lint limit registered"
    },
    {
      "id": "R18-DEADSEAT-RECORD",
      "named": true,
      "substance": true,
      "why": "4 seats without a report at a245bb0, each with cause and source"
    },
    {
      "id": "R18-REGISTRY-PINNED",
      "named": true,
      "substance": true,
      "why": "both rows name an existing path or state no persisted baseline"
    },
    {
      "id": "R18-INSTALL-RECORD",
      "named": true,
      "substance": true,
      "why": "go1.24.6 and go1.25.0 recorded with full sha256 and go.dev channel"
    }
  ],
  "named_open": 0,
  "open_count": 0,
  "rev": "d0690fd44f46d8a7fe9da5f01c6be723d12abd41",
  "substance_open": 0
}
exit=0
```

```text
$ python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py --root /tmp/kr19-w2-MutMidmap-t6nvjpq3 --prepare
{"fixture_root": "/tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz", "manifest": "/tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json", "manifest_sha256": "393ade40ac4ddf5310bd8a0ccf50f4d7618bbb029a058d1d982d83ccc854e178", "recorded_commands_executed": false, "synthetic_only": true}
exit=0
```

```text
$ python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py --root /tmp/kr19-w2-MutMidmap-t6nvjpq3 --manifest /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json --stage pristine
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/control_off_analyze.receipt.json
exit=1
{"basis": "documented invariant", "case": "control_off_analyze", "counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0}, "expected_exit": 1, "findings": [{"code": "mid_checks_absent", "detail": "analyze step has no mid-run pin checks", "where": "$.steps[1].pin_checks"}], "stage": "pristine", "stderr": "", "validator_exit": 1}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/control_on_analyze.receipt.json
exit=0
{"basis": "positive control", "case": "control_on_analyze", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 0, "findings": [], "stage": "pristine", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/argv_filename_token.receipt.json
exit=0
{"basis": "documented subcommand-vs-argument boundary", "case": "argv_filename_token", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "pristine", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/argv_search_pattern_token.receipt.json
exit=0
{"basis": "documented subcommand-vs-argument boundary", "case": "argv_search_pattern_token", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "pristine", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/duplicate_step_identity.receipt.json
exit=0
{"basis": "hypothesis: every repeated analyze needs checks", "case": "duplicate_step_identity", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "pristine", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/duplicate_name_identity.receipt.json
exit=0
{"basis": "hypothesis: every repeated analyze needs checks", "case": "duplicate_name_identity", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "pristine", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/conflicting_step_name.receipt.json
exit=0
{"basis": "hypothesis: conflicting identity must not rescue unpinned analyze", "case": "conflicting_step_name", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "pristine", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/conflicting_name_step.receipt.json
exit=0
{"basis": "hypothesis: conflicting identity must not rescue unpinned analyze", "case": "conflicting_name_step", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "pristine", "stderr": "", "validator_exit": 0}
{"accepted_challenges": ["argv_filename_token", "argv_search_pattern_token", "duplicate_step_identity", "duplicate_name_identity", "conflicting_step_name", "conflicting_name_step"], "cases": 8, "collector_exit_semantics": "0 means collected, not all invariants held", "stage": "pristine"}
exit=0
```

```text
$ sha256sum /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json
c1363f54dd7bd6b864856bc3620a27b9feb0ee8d7b21cd305a568a49f3ec3f0b  /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py
393ade40ac4ddf5310bd8a0ccf50f4d7618bbb029a058d1d982d83ccc854e178  /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json
exit=0
```

```text
$ git -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 restore --source 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 --staged --worktree -- .ufo/waves/round-17/tools/receipt-validate.py
exit=0
```

```text
$ sha256sum /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py
70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145  /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 rev-parse 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:.ufo/waves/round-17/tools/receipt-validate.py
bf0438862c41cb8ff2170396184f3db2a36d6e04
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 hash-object /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py
bf0438862c41cb8ff2170396184f3db2a36d6e04
exit=0
```

```text
$ git -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 -c core.hooksPath=/dev/null -c commit.gpgsign=false -c 'user.name=MutMidmap Probe' -c user.email=mutmidmap@invalid commit -q -m 'MutMidmap probe: restore only receipt validator to B bytes' -- .ufo/waves/round-17/tools/receipt-validate.py
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 rev-parse HEAD
a4cf7e0693bee96d52aef6dd9fcd86ac83d5e272
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 diff-tree --no-commit-id --name-only -r a4cf7e0693bee96d52aef6dd9fcd86ac83d5e272
.ufo/waves/round-17/tools/receipt-validate.py
exit=0
```

```text
$ python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py --root /tmp/kr19-w2-MutMidmap-t6nvjpq3 --manifest /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json --stage mutated
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/control_off_analyze.receipt.json
exit=0
{"basis": "documented invariant", "case": "control_off_analyze", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/control_on_analyze.receipt.json
exit=0
{"basis": "positive control", "case": "control_on_analyze", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 0, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/argv_filename_token.receipt.json
exit=0
{"basis": "documented subcommand-vs-argument boundary", "case": "argv_filename_token", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/argv_search_pattern_token.receipt.json
exit=0
{"basis": "documented subcommand-vs-argument boundary", "case": "argv_search_pattern_token", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/duplicate_step_identity.receipt.json
exit=0
{"basis": "hypothesis: every repeated analyze needs checks", "case": "duplicate_step_identity", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/duplicate_name_identity.receipt.json
exit=0
{"basis": "hypothesis: every repeated analyze needs checks", "case": "duplicate_name_identity", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/conflicting_step_name.receipt.json
exit=0
{"basis": "hypothesis: conflicting identity must not rescue unpinned analyze", "case": "conflicting_step_name", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/conflicting_name_step.receipt.json
exit=0
{"basis": "hypothesis: conflicting identity must not rescue unpinned analyze", "case": "conflicting_name_step", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "mutated", "stderr": "", "validator_exit": 0}
{"accepted_challenges": ["control_off_analyze", "argv_filename_token", "argv_search_pattern_token", "duplicate_step_identity", "duplicate_name_identity", "conflicting_step_name", "conflicting_name_step"], "cases": 8, "collector_exit_semantics": "0 means collected, not all invariants held", "stage": "mutated"}
exit=0
```

```text
$ python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutMidmap-t6nvjpq3 --rev a4cf7e0693bee96d52aef6dd9fcd86ac83d5e272 --strict
{
  "defects": [
    {
      "id": "R18-MIDMAP-LISTSTEP",
      "named": true,
      "substance": false,
      "why": "list-shaped receipt with pin_checks only on a non-analyze step is accepted"
    },
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    },
    {
      "id": "R18-STRICT-BASELINE",
      "named": true,
      "substance": true,
      "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"
    },
    {
      "id": "R18-HEAD-ALIASES",
      "named": true,
      "substance": true,
      "why": "6 aliases exit 2, refs/heads/main evaluates; lint limit registered"
    },
    {
      "id": "R18-DEADSEAT-RECORD",
      "named": true,
      "substance": true,
      "why": "4 seats without a report at a245bb0, each with cause and source"
    },
    {
      "id": "R18-REGISTRY-PINNED",
      "named": true,
      "substance": true,
      "why": "both rows name an existing path or state no persisted baseline"
    },
    {
      "id": "R18-INSTALL-RECORD",
      "named": true,
      "substance": true,
      "why": "go1.24.6 and go1.25.0 recorded with full sha256 and go.dev channel"
    }
  ],
  "named_open": 0,
  "open_count": 1,
  "rev": "a4cf7e0693bee96d52aef6dd9fcd86ac83d5e272",
  "substance_open": 1
}
exit=1
```

```text
$ git -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 restore --source d0690fd44f46d8a7fe9da5f01c6be723d12abd41 --staged --worktree -- .ufo/waves/round-17/tools/receipt-validate.py
exit=0
```

```text
$ sha256sum /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py
9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45  /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py
exit=0
```

```text
$ git -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 -c core.hooksPath=/dev/null -c commit.gpgsign=false -c 'user.name=MutMidmap Probe' -c user.email=mutmidmap@invalid commit -q -m 'MutMidmap probe: restore exact observed-tip validator bytes' -- .ufo/waves/round-17/tools/receipt-validate.py
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 rev-parse HEAD
6b4d5ac09a9852d22bada62e1521e57a5169fc2a
exit=0
```

```text
$ git --no-optional-locks -C /tmp/kr19-w2-MutMidmap-t6nvjpq3 rev-parse 'd0690fd44f46d8a7fe9da5f01c6be723d12abd41^{tree}' '6b4d5ac09a9852d22bada62e1521e57a5169fc2a^{tree}'
b344427155950539dd93926882071beea28970a4
b344427155950539dd93926882071beea28970a4
exit=0
```

```text
$ python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py --root /tmp/kr19-w2-MutMidmap-t6nvjpq3 --manifest /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json --stage restored
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/control_off_analyze.receipt.json
exit=1
{"basis": "documented invariant", "case": "control_off_analyze", "counts": {"invalid": 1, "receipts": 1, "unreadable": 0, "valid": 0}, "expected_exit": 1, "findings": [{"code": "mid_checks_absent", "detail": "analyze step has no mid-run pin checks", "where": "$.steps[1].pin_checks"}], "stage": "restored", "stderr": "", "validator_exit": 1}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/control_on_analyze.receipt.json
exit=0
{"basis": "positive control", "case": "control_on_analyze", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 0, "findings": [], "stage": "restored", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/argv_filename_token.receipt.json
exit=0
{"basis": "documented subcommand-vs-argument boundary", "case": "argv_filename_token", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "restored", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/argv_search_pattern_token.receipt.json
exit=0
{"basis": "documented subcommand-vs-argument boundary", "case": "argv_search_pattern_token", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "restored", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/duplicate_step_identity.receipt.json
exit=0
{"basis": "hypothesis: every repeated analyze needs checks", "case": "duplicate_step_identity", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "restored", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/duplicate_name_identity.receipt.json
exit=0
{"basis": "hypothesis: every repeated analyze needs checks", "case": "duplicate_name_identity", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "restored", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/conflicting_step_name.receipt.json
exit=0
{"basis": "hypothesis: conflicting identity must not rescue unpinned analyze", "case": "conflicting_step_name", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "restored", "stderr": "", "validator_exit": 0}
$ /usr/bin/python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/conflicting_name_step.receipt.json
exit=0
{"basis": "hypothesis: conflicting identity must not rescue unpinned analyze", "case": "conflicting_name_step", "counts": {"invalid": 0, "receipts": 1, "unreadable": 0, "valid": 1}, "expected_exit": 1, "findings": [], "stage": "restored", "stderr": "", "validator_exit": 0}
{"accepted_challenges": ["argv_filename_token", "argv_search_pattern_token", "duplicate_step_identity", "duplicate_name_identity", "conflicting_step_name", "conflicting_name_step"], "cases": 8, "collector_exit_semantics": "0 means collected, not all invariants held", "stage": "restored"}
exit=0
```

```text
$ python3 -I -B /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-19/tools/routed-r18.py --root /tmp/kr19-w2-MutMidmap-t6nvjpq3 --rev 6b4d5ac09a9852d22bada62e1521e57a5169fc2a --strict
{
  "defects": [
    {
      "id": "R18-MIDMAP-LISTSTEP",
      "named": true,
      "substance": true,
      "why": "non-analyze-only list receipt -> mid_checks_absent; analyze-carrying list receipt clean"
    },
    {
      "id": "R18-VALIDATOR-DIGEST",
      "named": true,
      "substance": true,
      "why": "wrong digest refused, true digest accepted; 8/8 retained copies re-hash"
    },
    {
      "id": "R18-STRICT-BASELINE",
      "named": true,
      "substance": true,
      "why": "strict run at 9011581 exit 1 (open 6), bytes and tool bound"
    },
    {
      "id": "R18-HEAD-ALIASES",
      "named": true,
      "substance": true,
      "why": "6 aliases exit 2, refs/heads/main evaluates; lint limit registered"
    },
    {
      "id": "R18-DEADSEAT-RECORD",
      "named": true,
      "substance": true,
      "why": "4 seats without a report at a245bb0, each with cause and source"
    },
    {
      "id": "R18-REGISTRY-PINNED",
      "named": true,
      "substance": true,
      "why": "both rows name an existing path or state no persisted baseline"
    },
    {
      "id": "R18-INSTALL-RECORD",
      "named": true,
      "substance": true,
      "why": "go1.24.6 and go1.25.0 recorded with full sha256 and go.dev channel"
    }
  ],
  "named_open": 0,
  "open_count": 0,
  "rev": "6b4d5ac09a9852d22bada62e1521e57a5169fc2a",
  "substance_open": 0
}
exit=0
```

```text
$ sha256sum /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-19/tools/routed-r18.py /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json
9276b1984cd58fd321f028b51a20bb490bb4362728eb286c27faf5ce00646d45  /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-17/tools/receipt-validate.py
dc1b7058c0d6e22b7fb1b3668045f523257c1d6f91fd57af781195219924038b  /tmp/kr19-w2-MutMidmap-t6nvjpq3/.ufo/waves/round-19/tools/routed-r18.py
c1363f54dd7bd6b864856bc3620a27b9feb0ee8d7b21cd305a568a49f3ec3f0b  /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-identity-probe.py
393ade40ac4ddf5310bd8a0ccf50f4d7618bbb029a058d1d982d83ccc854e178  /tmp/kr19-w2-MutMidmap-t6nvjpq3/midmap-fixtures-4ii8upcz/manifest.json
exit=0
```

```text
$ git --no-optional-locks -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
exit=0
```

Report: .ufo/waves/round-19/w2/MutMidmap.md
