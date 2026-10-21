# R21Attack66 — duplicate-member last-wins mutation probe

## Verdict and axes

**KILLED**, not survived or inconclusive. Finding **R21Attack66-F1**: the independently frozen `duplicate_member_ambiguity` case detects removal of duplicate-member rejection, while the same-record positive remains green. This is author-side advisory mutation evidence, not an integration or outside-verifier verdict.

- **Calibration (C1):** distinguish ambiguous contradictory operation members from a valid same-record operation/id pair. Pristine and restored ambiguity inputs exit 2; the mutant falsely exits 0. The positive stays at exit 0 throughout.
- **Depth:** establish causal detector sensitivity through the same bounded CLI runs on pristine, minimally mutated, and byte-exact restored copies, with immutable independent expectations, full output capture, and SHA-256 evidence. This does **not** exercise or establish the separate C2 first-failure claim.

Scope: exactly one two-line mutation in one owned external tempfile copy of `.ufo/waves/round-21/tools/verb-coverage.py`, exactly two frozen inert inputs, three phases, six child CLI invocations. No production tool or fixture edits.

## Independent detector and input authority

Read the frozen claim in `.ufo/waves/round-21/claims.json:8-9`. C1 explicitly limits itself to local evidence binding, not cryptographic Evidence authentication or security certification.

The expected exits are taken unchanged from `.ufo/waves/round-21/fixtures/battery.json:4-10,81-87`, independently corroborated by `.ufo/waves/round-21/fixture-contract.json:6,17`:

- `same_record_positive`: exit **0**, exact id and exact operation in the same successful supported record.
- `duplicate_member_ambiguity`: exit **2**, contradictory duplicate operation names cannot select last-wins success.

Before running, the complete battery and contract bytes matched their independently frozen SHA-256 entries in `.ufo/waves/round-21/fixtures/expected.json:3-6`. They also remained unchanged afterward. Evidence strings were copied verbatim from the fixture fields as UTF-8, without parsing/reserializing the inner JSON; the duplicate `operation` members therefore remain present. No expectations were derived from the mutant or rewritten after observing it.

The bounded detector invokes the successor CLI directly using the C1 successor argument shape documented by `.ufo/waves/round-21/battery.py:92-100`. It compares exits to the frozen expected exits. The report additionally records and checks the expected finding/bound shape and empty stderr. It does **not** run `battery.py`, its Git materialization, any broad suite, or the implementation's selftest.

Frozen selected inputs and separately held expected shapes:

```json
{
  "duplicate_member_ambiguity": {
    "evidence": "{\"evidence_id\":\"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\",\"operation\":\"inspect_artifact\",\"operation\":\"inspect_wasm_artifact\"}",
    "expected_bound": null,
    "expected_exit": 2,
    "expected_finding": "evidence_unevaluable",
    "sha256": "2e7d153e3308c14697eb2043c2a7f6802feccad0ec480f226914c83694951920"
  },
  "same_record_positive": {
    "evidence": "{\"evidence_id\": \"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\", \"operation\": \"inspect_wasm_artifact\"}",
    "expected_bound": true,
    "expected_exit": 0,
    "expected_finding": "evidence_bound",
    "sha256": "92c60f2ca66141bc0403d735b65948ef97a019ad5751844c4e431b86cb3112df"
  }
}
```

## Mutation and causal point

Original behavior-bearing point: `.ufo/waves/round-21/tools/verb-coverage.py:24-30`, `pairs()`; `decode()` installs it as `object_pairs_hook` at line 36. The parser's duplicate exception reaches `bind()`'s unevaluable result at lines 100-101 before any record can bind.

Only these two lines were deleted from the external scratch copy:

```diff
 def pairs(items):
     result = {}
     for key, value in items:
-        if key in result:
-            raise ValueError('duplicate_member: ' + key)
         result[key] = value
     return result
```

This is a plausible loss of duplicate-key validation: unguarded dictionary assignment implements last-wins. The first `operation` value is `inspect_artifact`, the later value is `inspect_wasm_artifact`; the latter now overwrites the former and matches the unchanged requested `inspect-wasm-artifact`. No matching, refusal, output, or expected-fixture code was changed. The mutated copy was confirmed to differ from the original by precisely this two-line deletion.

## Observed detector results

| Phase | Frozen case | Expected exit | Actual exit | Actual finding ID | Detector |
| --- | --- | ---: | ---: | --- | --- |
| pristine | `duplicate_member_ambiguity` | 2 | 2 | `evidence_unevaluable` | PASS |
| pristine | `same_record_positive` | 0 | 0 | `evidence_bound` | PASS |
| mutated | `duplicate_member_ambiguity` | 2 | 0 | `evidence_bound` | FAIL — false clean |
| mutated | `same_record_positive` | 0 | 0 | `evidence_bound` | PASS |
| restored | `duplicate_member_ambiguity` | 2 | 2 | `evidence_unevaluable` | PASS |
| restored | `same_record_positive` | 0 | 0 | `evidence_bound` | PASS |

All six stderr streams were exactly empty. The mutant's negative is a **clean false acceptance**, not a crash: actual stdout reports `evidence_bound`, `bound: true`, and `pathless: false`. Its exit 0 contradicts the frozen negative expectation of 2. Baseline 2/2 and restoration 2/2 pass; mutant 1/2 passes. The negative alone kills this mutant, with the positive retained. No coverage gap is demonstrated for this one defect, and no broader coverage or mastery claim follows.

## Exact CLI capture

Interpreter: `/usr/bin/python`, Python `3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`. Each invocation used `-I -B`, a 30-second timeout, and the scratch directory as `cwd`. The two independent cases were executed concurrently inside each phase; mutation/restoration happened only between completed phases. These are the same argv values and same input bytes across all three phases. The following records retain every actual argv, stdout, stderr, exit, observed finding, and detector decision without truncation; JSON `\n` preserves the output's final newline.

```json
[
  {
    "argv": [
      "/usr/bin/python",
      "-I",
      "-B",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/verb-coverage.py",
      "--evidence",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/duplicate_member_ambiguity.json",
      "--verb",
      "inspect-wasm-artifact",
      "--evidence-id",
      "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ],
    "bound": null,
    "case_id": "duplicate_member_ambiguity",
    "cwd": "/tmp/kaidoku-r21-attack66-po7i7ypo",
    "detector_pass": true,
    "exit": 2,
    "exit_matches_frozen": true,
    "expected_bound": null,
    "expected_exit": 2,
    "expected_finding": "evidence_unevaluable",
    "finding": "evidence_unevaluable",
    "phase": "pristine",
    "stderr": "",
    "stdout": "{\"bound\": null, \"error\": \"duplicate_member: operation\", \"finding\": \"evidence_unevaluable\"}\n",
    "timeout_seconds": 30
  },
  {
    "argv": [
      "/usr/bin/python",
      "-I",
      "-B",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/verb-coverage.py",
      "--evidence",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/same_record_positive.json",
      "--verb",
      "inspect-wasm-artifact",
      "--evidence-id",
      "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ],
    "bound": true,
    "case_id": "same_record_positive",
    "cwd": "/tmp/kaidoku-r21-attack66-po7i7ypo",
    "detector_pass": true,
    "exit": 0,
    "exit_matches_frozen": true,
    "expected_bound": true,
    "expected_exit": 0,
    "expected_finding": "evidence_bound",
    "finding": "evidence_bound",
    "phase": "pristine",
    "stderr": "",
    "stdout": "{\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}\n",
    "timeout_seconds": 30
  },
  {
    "argv": [
      "/usr/bin/python",
      "-I",
      "-B",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/verb-coverage.py",
      "--evidence",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/duplicate_member_ambiguity.json",
      "--verb",
      "inspect-wasm-artifact",
      "--evidence-id",
      "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ],
    "bound": true,
    "case_id": "duplicate_member_ambiguity",
    "cwd": "/tmp/kaidoku-r21-attack66-po7i7ypo",
    "detector_pass": false,
    "exit": 0,
    "exit_matches_frozen": false,
    "expected_bound": null,
    "expected_exit": 2,
    "expected_finding": "evidence_unevaluable",
    "finding": "evidence_bound",
    "phase": "mutated",
    "stderr": "",
    "stdout": "{\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}\n",
    "timeout_seconds": 30
  },
  {
    "argv": [
      "/usr/bin/python",
      "-I",
      "-B",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/verb-coverage.py",
      "--evidence",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/same_record_positive.json",
      "--verb",
      "inspect-wasm-artifact",
      "--evidence-id",
      "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ],
    "bound": true,
    "case_id": "same_record_positive",
    "cwd": "/tmp/kaidoku-r21-attack66-po7i7ypo",
    "detector_pass": true,
    "exit": 0,
    "exit_matches_frozen": true,
    "expected_bound": true,
    "expected_exit": 0,
    "expected_finding": "evidence_bound",
    "finding": "evidence_bound",
    "phase": "mutated",
    "stderr": "",
    "stdout": "{\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}\n",
    "timeout_seconds": 30
  },
  {
    "argv": [
      "/usr/bin/python",
      "-I",
      "-B",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/verb-coverage.py",
      "--evidence",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/duplicate_member_ambiguity.json",
      "--verb",
      "inspect-wasm-artifact",
      "--evidence-id",
      "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ],
    "bound": null,
    "case_id": "duplicate_member_ambiguity",
    "cwd": "/tmp/kaidoku-r21-attack66-po7i7ypo",
    "detector_pass": true,
    "exit": 2,
    "exit_matches_frozen": true,
    "expected_bound": null,
    "expected_exit": 2,
    "expected_finding": "evidence_unevaluable",
    "finding": "evidence_unevaluable",
    "phase": "restored",
    "stderr": "",
    "stdout": "{\"bound\": null, \"error\": \"duplicate_member: operation\", \"finding\": \"evidence_unevaluable\"}\n",
    "timeout_seconds": 30
  },
  {
    "argv": [
      "/usr/bin/python",
      "-I",
      "-B",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/verb-coverage.py",
      "--evidence",
      "/tmp/kaidoku-r21-attack66-po7i7ypo/same_record_positive.json",
      "--verb",
      "inspect-wasm-artifact",
      "--evidence-id",
      "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    ],
    "bound": true,
    "case_id": "same_record_positive",
    "cwd": "/tmp/kaidoku-r21-attack66-po7i7ypo",
    "detector_pass": true,
    "exit": 0,
    "exit_matches_frozen": true,
    "expected_bound": true,
    "expected_exit": 0,
    "expected_finding": "evidence_bound",
    "finding": "evidence_bound",
    "phase": "restored",
    "stderr": "",
    "stdout": "{\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}\n",
    "timeout_seconds": 30
  }
]
```

## Hashes and restoration evidence

The deleted guard was restored through the edit tool's captured exact-text register before the restored CLI phase. Restored scratch bytes compare exactly equal to the original source snapshot, not merely semantically equivalent. The restoration phase reproduces the pristine findings and exits. SHA-256 changes only in the mutated scratch copy:

```json
{
  "expected_manifest_after_sha256": "a792b3fae1dc383f1ed1476b8536fe93196e90eaf77dddb88ff296f1794eb315",
  "expected_manifest_sha256": "a792b3fae1dc383f1ed1476b8536fe93196e90eaf77dddb88ff296f1794eb315",
  "fixture_contract_after_sha256": "04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6",
  "fixture_contract_sha256": "04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6",
  "fixtures_battery_after_sha256": "2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba",
  "fixtures_battery_sha256": "2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba",
  "scratch_mutated_sha256": "af035eec835efafdb1eab149022933d32394f3aba1ce041fe11f7b7c634079ed",
  "scratch_pristine_sha256": "77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc",
  "scratch_restored_sha256": "77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc",
  "selected_inputs_sha256": {
    "duplicate_member_ambiguity": "2e7d153e3308c14697eb2043c2a7f6802feccad0ec480f226914c83694951920",
    "same_record_positive": "92c60f2ca66141bc0403d735b65948ef97a019ad5751844c4e431b86cb3112df"
  },
  "source_after_sha256": "77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc",
  "source_pristine_sha256": "77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc"
}
```

Observed restoration/cleanup facts:

```json
{
  "contract_unchanged": true,
  "exact_bytes_restored": true,
  "external_scratch_removed": true,
  "frozen_fixture_unchanged": true,
  "inert_input_bytes_unchanged": true,
  "manifest_unchanged": true,
  "source_unchanged": true
}
```

The owned external directory `/tmp/kaidoku-r21-attack66-po7i7ypo` and all its copied validator/fixture files were removed after restoration and capture. Original source, complete fixture, contract, and expected-manifest before/after hashes are identical. The sole durable write is this report at the assigned lane path.

## Bounds and nonclaims

No production execution, carrier/native execution, REA producer, Git/jj/index operation, model/routing/account/provider/credential probe, sibling mutation, delegation, runtime judgment, host mutation, build, formatter, or broad test suite was performed. No tool was installed or updated; the existing Python interpreter sufficed. No C2 or external verifier status is asserted. This completes the one assigned mutation probe only.

Report: `.ufo/waves/round-21/w2/R21Attack66.md`
