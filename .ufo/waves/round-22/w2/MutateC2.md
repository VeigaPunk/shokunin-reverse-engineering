# MutateC2 — author-side mutation probe

## Scope and verdict

**Mutation verdict: killed.** A one-line unconditional `matched` return in the private clone's `check()` made the contradictory error-code receipt count as accounted. The unchanged fixture detector rejected that result against its independently declared `observed_mismatch` expectation. Pristine and restored runs both passed every existing C2 control.

Axes: **coverage** (exercise a receipt/row contradiction) and **calibration** (require the declared rejection status, count, and exit rather than accepting the counter's own conclusion). This is finite, author-side detector evidence, **not outside admission** or a claim-level verification of production R22-C2.

Only this report and its same-name `MutateC2.json` attachment were written in the lane. All code mutations were restricted to:

```text
/tmp/kaidoku-r22-MutateC2.kp9MsTAV/repo
```

The frozen claims name baseline `7787fea4d6fd718726de92ed20759d11ce7b8b48`. The private local clone's HEAD was `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67`; the target bytes matched the lane before mutation. This probe does not purport to measure R22-C2 at the frozen baseline.

## Mutant

Target: `.ufo/waves/round-22/tools/count-c2.py`, `check()`, immediately after its definition at line 87. Exactly one line was inserted and later removed:

```diff
 def check(row, root, rev):
+    return "matched"
     if row["placement"] not in PLACEMENTS:
         return "bad_placement"
```

This is an intentional unconditional-acceptance defect, not a proposed production change. The original body remained byte-identical below the inserted early return. Outside the private clone, no source, configuration, index, manifest, or state was edited; the reused fixture runner's Git initialization, configuration, staging, and commits were confined to its temporary repositories inside that clone.

## Expected detector and fixture

The existing `counter-fixtures.py` was reused without edits. It defines its own T2 list and fixed expectations, invokes the candidate counter as a subprocess, and compares actual exit, accounted count, claim ID, and the targeted status. Expectations were not extracted from the mutated counter.

- Positive `all_fourteen`: fourteen well-formed rows whose receipts have `ok: false`, matching `meta.command`, and `error.code: capability_unavailable`. Independent expectations are exit **0**, accounted count **14**, claim `R22-C2`. This case has no separately fixed status expectation (`expected_status: null`); actual first-verb status was `matched` in all three phases.
- Negative `wrong_code`: the `inspect-packet-fields` receipt alone changes its error code to `invalid_request`; its disposition row still says `error:capability_unavailable`. Independent expectations are exit **1**, accounted count **13**, claim `R22-C2`, and first-verb status **`observed_mismatch`**. The decisive negative expectation is explicitly declared in `counter-fixtures.py:92-106`, not computed from counter output.

The relevant synthetic receipt/row contrast is:

```json
{"verb":"inspect-packet-fields","observed":"error:capability_unavailable","receipt_envelope":{"ok":false,"error":{"code":"invalid_request"},"meta":{"command":"inspect-packet-fields"}}}
```

These are synthetic fixture envelopes, not retained real REA observations. Their purpose is to test the counter's stated agreement contract.

## Exact bounded command

Setup commands, all completed successfully:

```sh
mktemp -d /tmp/kaidoku-r22-MutateC2.XXXXXXXX
# stdout: /tmp/kaidoku-r22-MutateC2.kp9MsTAV

git clone --no-local --quiet /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kaidoku-r22-MutateC2.kp9MsTAV/repo
# stdout/stderr: empty
```

The following **same detector argv and environment override** were used once for pristine, mutated, and restored bytes. Working directory was the private clone; each call was bounded by a 120-second subprocess timeout. `TMPDIR` kept every fixture repository and its temporary Git writes inside that clone.

```sh
TMPDIR=/tmp/kaidoku-r22-MutateC2.kp9MsTAV/repo \
python3 -I -B \
  /tmp/kaidoku-r22-MutateC2.kp9MsTAV/repo/.ufo/waves/round-22/tools/counter-fixtures.py \
  --claim C2 \
  --counter /tmp/kaidoku-r22-MutateC2.kp9MsTAV/repo/.ufo/waves/round-22/tools/count-c2.py \
  --root /tmp/kaidoku-r22-MutateC2.kp9MsTAV/repo
```

Full, unabridged detector stdout/stderr and actual exits are retained in `MutateC2.json`, under each `phases[]` capture. Decoding a phase's `stdout` exposes all seven cases, each including its exact counter argv (with temporary fixture root and committed revision), counter stdout, stderr, actual exit, fixed expectations, and comparison result. The attachment also retains focused decoded stdout excerpts for the positive and contradictory-code cases. All three detector stderr streams and all 21 counter stderr streams were empty.

## Actual positive and negative results

| Phase | Detector exit | Detector stdout `finding` | Controls meeting oracle |
|---|---:|---|---:|
| Pristine | 0 | `counter_controls_clean` | 7/7 |
| Mutated | 1 | `counter_controls_failed` | 3/7 |
| Restored | 0 | `counter_controls_clean` | 7/7 |

Below, exits are the **counter subprocess** exits, not the enclosing detector's exit.

| Phase | Case | Expected exit/count/status | Actual exit/count/status | Oracle comparison |
|---|---|---|---|---|
| Pristine | `all_fourteen` | 0 / 14 / not constrained | 0 / 14 / `matched` | pass |
| Pristine | `wrong_code` | 1 / 13 / `observed_mismatch` | 1 / 13 / `observed_mismatch` | pass |
| Mutated | `all_fourteen` | 0 / 14 / not constrained | 0 / 14 / `matched` | pass |
| Mutated | `wrong_code` | 1 / 13 / `observed_mismatch` | **0 / 14 / `matched`** | **fail: mutant killed** |
| Restored | `all_fourteen` | 0 / 14 / not constrained | 0 / 14 / `matched` | pass |
| Restored | `wrong_code` | 1 / 13 / `observed_mismatch` | 1 / 13 / `observed_mismatch` | pass |

Actual decoded stdout on `wrong_code` had `mismatched: ["inspect-packet-fields"]` before mutation and after restoration, but `mismatched: []` under the mutant. The row's observed assertion remained `error:capability_unavailable` throughout.

The same unchanged suite also rejected the mutant on `probe_alias`, `outside_path`, and `duplicate_json`: each incorrectly returned exit 0, count 14, and status `matched`. `duplicate_row` and `empty_section` continued to meet their negative expectations because those decisions occur outside `check()`; together with the positive control these account for the mutant's 3/7 passing controls. These are additional observations from the one assigned mutation, not additional mutation probes.

## Exact-byte restoration evidence

SHA-256 of `count-c2.py`:

| Location / phase | SHA-256 |
|---|---|
| Lane before probe | `ded1a0e855b2e3c3aacb0dd9a12fd34e29397e9d8d5b741b6c29611450cc642e` |
| Private clone pristine | `ded1a0e855b2e3c3aacb0dd9a12fd34e29397e9d8d5b741b6c29611450cc642e` |
| Private clone mutated | `fd84ef714c22f7d9838525abb9af7381531d24babdd9ee3fb9b9f9011a8cffc6` |
| Private clone restored | `ded1a0e855b2e3c3aacb0dd9a12fd34e29397e9d8d5b741b6c29611450cc642e` |
| Lane after restoration | `ded1a0e855b2e3c3aacb0dd9a12fd34e29397e9d8d5b741b6c29611450cc642e` |

The unchanged detector's SHA-256 was `c5b495672ea7cba50f58eb28e89097d6510ccb4cda3351d92d1883f6da5dae11` in all three phases. Restoration removed only the inserted line. The final command, run from the clone, completed successfully (exit 0):

```sh
sha256sum .ufo/waves/round-22/tools/count-c2.py .ufo/waves/round-22/tools/counter-fixtures.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c2.py && cmp -s .ufo/waves/round-22/tools/count-c2.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c2.py
```

Its digest output is recorded in the attachment; `cmp -s` emitted no output and returned 0. The restored detector then retained the pristine 7/7 outcome.

## Limits and tooling

Observed: the existing bounded detector kills this unconditional-acceptance mutant specifically on the independently expected contradictory-code rejection, with healthy positive and restored controls. Inference: it is sensitive to this defect class for these finite fixtures. Unknown/not exercised: completeness against other possible defects, real provider availability, authentic REA Evidence, and production claim admission. No baseline failure or execution blocker occurred.

No REA command, target execution, debugger attachment, remote connection, device contact, child dispatch, integration, or admission was performed. The only execution was the explicitly requested local counter/fixture probe and local setup/hash commands. No build, lint, formatter, or unrelated test was run. Temporary fixture repositories were cleaned by the existing runner; the private clone remains with its counter restored exactly.

Installed or updated tools: **none**. Existing tools observed: Python **3.14.8** (`python3 --version`) and Git **2.56.0** (`git --version`). No package transaction or service change was performed.
