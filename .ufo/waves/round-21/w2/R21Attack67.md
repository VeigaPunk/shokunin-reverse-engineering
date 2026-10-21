# R21Attack67 — C2 boolean last_line guard mutation

## Scope and axes

- **Calibration:** finite mutation sensitivity only; distinguish a killed scratch mutant from a defect in production or approval of C2.
- **Depth:** test the malformed-boolean / explicit-integer-bound distinction with the frozen negative and a retained positive control.
- **Containment:** one external scratch comparator, exact-byte restoration, then removal. This is author-side advisory evidence; no judge, integration, or outside-verifier status is claimed.

Frozen claim: `.ufo/waves/round-21/claims.json:9` (C2). The allowed source was `.ufo/waves/round-21/tools/compare-first-failure.py`, original lines 66–72. No C1 predicate, production source, lane Git/jj/index, fleet/sibling/domain source, provider/account/routing configuration, or analyzed carrier was changed or executed.

## Mutant and independent detector

**R21Attack67-M1:** remove only the two original source lines 67–68 from the isolated copy:

```diff
         bound = envelope['last_line']
-        if type(bound) is not int or bound < 0:
-            raise ValueError('invalid_last_line')
         observed = envelope['first_failure']
```

The removed byte sequence occurred exactly once. The mutated bytes equaled pristine bytes with just that sequence removed; no failure-shape, envelope-presence, equality, error-handling, selftest, or output code was altered. Restoration reinserted exactly these lines before the final run.

The oracle was fixed **before the first run**, outside the comparator and its selftest. It used only the two assigned frozen cases, copied literally from `.ufo/waves/round-21/fixtures/battery.json` under `C2`, with expectations justified by `.ufo/waves/round-21/fixture-contract.json:20,32`:

| Fixture | Shared prediction | Extractor output | Expected comparator exit / finding |
| --- | --- | --- | --- |
| `boolean_last_line` | `{"first_failure":{"h1":null}}` | `{"first_failure": null, "last_line": true}` | 2 / `comparison_unevaluable` |
| `bounded_silent_positive` | `{"first_failure":{"h1":null}}` | `{"first_failure": null, "last_line": 8}` | 0 / `failure_match` |

The expected rejection is not inferred from the mutant or learned from a pristine execution: the frozen contract says a bool is not a line count. The additional literal expected result for the negative was `{"error":"invalid_last_line","finding":"comparison_unevaluable","match":null,"observed":null,"predicted":null}`; for the positive it was `{"finding":"failure_match","last_line":8,"match":true,"observed":null,"predicted":null}`. Both stayed unchanged for all three phases.

The independently authored inert extractor was only:

```python
from pathlib import Path
import sys
sys.stdout.write(Path(sys.argv[1]).read_text(encoding='utf-8'))
```

The detector ran each comparator CLI with `-I -B`, a 10-second per-case timeout, captured both streams and the exit code, parsed stdout, and required the frozen expected exit, the literal expected JSON object, and empty comparator stderr. It ran exactly these two independent cases with two Python thread-pool workers. The outer detector CLI had a 25-second timeout and returned 0 only if both cases passed, otherwise 1. The detector argv, detector bytes, fixture bytes, prediction bytes, and extractor bytes were identical across pristine/mutated/restored phases (hash evidence below). No broader battery, Git helper, built-in selftest, nineteen-case retrospective regression, build, formatter, or other runtime was run.

## Outputs and local findings

| Phase | Case | Expected exit | Actual exit | Actual finding | Detector case |
| --- | --- | ---: | ---: | --- | --- |
| pristine | `boolean_last_line` | 2 | 2 | `comparison_unevaluable` | green |
| pristine | `bounded_silent_positive` | 0 | 0 | `failure_match` | green |
| mutated | `boolean_last_line` | 2 | 0 | `failure_match` | red |
| mutated | `bounded_silent_positive` | 0 | 0 | `failure_match` | green |
| restored | `boolean_last_line` | 2 | 2 | `comparison_unevaluable` | green |
| restored | `bounded_silent_positive` | 0 | 0 | `failure_match` | green |

Outer detector exits were **0 → 1 → 0**, with findings **`detector_clean` → `detector_failed` → `detector_clean`**. All three outer stderr strings and all six comparator stderr strings were empty. No timeout or crash was observed.

- **R21Attack67-F1 — KILLED:** `boolean_last_line` changed from the declared unevaluable rejection (exit 2) to a false-clean match (exit 0) only after the bound guard was removed. The mutant returned `{"finding":"failure_match","last_line":true,"match":true,"observed":null,"predicted":null}`. The fixed independent detector rejected that result. Baseline failure did not occur.
- **R21Attack67-F2 — positive retained:** `bounded_silent_positive` stayed exit 0 / `failure_match` with `last_line: 8` in all three phases. The kill was not obtained by indiscriminately breaking successful bounded silence.
- **R21Attack67-F3 — restoration/containment:** scratch bytes were restored exactly before the restored run; restored detector stdout/stderr matched pristine exactly. Production source SHA-256 and bytes matched their initial values. The owned external temporary directory was then removed.

This supports sensitivity of these two independent controls to this precise guard deletion. It does not establish all malformed-bound handling, the negative/string-bound cases, all of C2, C1 isolation, the nineteen retained matches, new forecasts, cryptographic evidence authentication, or any outside acceptance. No production defect was demonstrated by this probe.

## Hashes and restoration

| Object/state | SHA-256 |
| --- | --- |
| Production source before | `990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c` |
| Scratch pristine | `990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c` |
| Scratch guard-deletion mutant | `ebd9b5b8da17ebdb82e0f1e44c5e5dfcb4b4104fbfe8b42d09cce06307efb271` |
| Scratch restored | `990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c` |
| Production source after | `990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c` |

Exact-byte scratch restoration: `True`. Exact-byte production-source equality: `True`. Identical fixed detector/input hashes across phases: `True`. Scratch removed: `True` (`/tmp/kaidoku-r21-attack67-37iu6jc1`). Hashing was local Python SHA-256; no Git/jj operations were used. The observed frozen fixture/contract hashes matched the existing expected manifest (`2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba` / `04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6`); no independent commit-authentication check is claimed.

## Complete retained command/stream evidence

The following JSON retains the actual argv, exit, stdout and stderr for every detector CLI invocation. The detector's stdout is retained losslessly as a JSON string, including its trailing newline, and contains each actual comparator argv, exit, raw stdout and stderr, expected values, parsed result, and case decision. Empty streams are `""`; no output is elided. This records captured detector/comparator streams, not an independently instrumented internal extractor receipt.

```json
{
  "cleanup": {
    "existed_before_cleanup": true,
    "exists_after_cleanup": false,
    "removed": true,
    "scratch_path": "/tmp/kaidoku-r21-attack67-37iu6jc1"
  },
  "local_mutation_verdict": "killed",
  "mutation": {
    "guard_occurrences_in_pristine": 1,
    "id": "R21Attack67-M1",
    "mutant_sha256": "ebd9b5b8da17ebdb82e0f1e44c5e5dfcb4b4104fbfe8b42d09cce06307efb271",
    "only_guard_removed": true,
    "removed_original_lines": [
      67,
      68
    ]
  },
  "restoration": {
    "restored_raw_stderr_equals_pristine": true,
    "restored_raw_stdout_equals_pristine": true,
    "same_detector_and_fixtures_all_phases": true,
    "same_detector_argv_all_phases": true,
    "scratch_exact_original_bytes": true,
    "scratch_restored_sha256": "990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c",
    "source_after_sha256": "990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c",
    "source_exact_original_bytes": true
  },
  "runs": [
    {
      "argv": [
        "/usr/bin/python",
        "-I",
        "-B",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/detector.py",
        "--comparator",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py",
        "--fixtures",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/fixtures.json"
      ],
      "exit": 0,
      "fixed_inputs_sha256": {
        "boolean_last_line.json": "c6d925075b3710b96397b0a3ea14a9521789f32dcb8cd6d332c875cd7955001a",
        "bounded_silent_positive.json": "fddfcd668b61a7dd08b161e4c14f3d5841ece053ffe693781e21c60d072414fa",
        "detector.py": "6487a7854e91b6885d3ac321ef92ade48c9c2320f966afd70b42651219255262",
        "extractor.py": "c8ce979c2002884f592379e5b3641f9eab95f6b098d82fa0aa99a39104675b4a",
        "fixtures.json": "f3c3da5c0dd4063bf0671e84174e33294701c456a106f0f04cd1d9afd28507a9",
        "prediction.json": "87506da68595eb57e664a9a6030df97f0576af0f80626152c2e9ac0875d33ee3"
      },
      "phase": "pristine",
      "stderr": "",
      "stdout": "{\"cases\": [{\"argv\": [\"/usr/bin/python\", \"-I\", \"-B\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py\", \"--prediction\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/prediction.json\", \"--log\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/boolean_last_line.json\", \"--extractor\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/extractor.py\"], \"exit\": 2, \"expected_exit\": 2, \"expected_result\": {\"error\": \"invalid_last_line\", \"finding\": \"comparison_unevaluable\", \"match\": null, \"observed\": null, \"predicted\": null}, \"id\": \"boolean_last_line\", \"ok\": true, \"parsed\": {\"error\": \"invalid_last_line\", \"finding\": \"comparison_unevaluable\", \"match\": null, \"observed\": null, \"predicted\": null}, \"stderr\": \"\", \"stdout\": \"{\\\"error\\\": \\\"invalid_last_line\\\", \\\"finding\\\": \\\"comparison_unevaluable\\\", \\\"match\\\": null, \\\"observed\\\": null, \\\"predicted\\\": null}\\n\"}, {\"argv\": [\"/usr/bin/python\", \"-I\", \"-B\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py\", \"--prediction\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/prediction.json\", \"--log\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/bounded_silent_positive.json\", \"--extractor\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/extractor.py\"], \"exit\": 0, \"expected_exit\": 0, \"expected_result\": {\"finding\": \"failure_match\", \"last_line\": 8, \"match\": true, \"observed\": null, \"predicted\": null}, \"id\": \"bounded_silent_positive\", \"ok\": true, \"parsed\": {\"finding\": \"failure_match\", \"last_line\": 8, \"match\": true, \"observed\": null, \"predicted\": null}, \"stderr\": \"\", \"stdout\": \"{\\\"finding\\\": \\\"failure_match\\\", \\\"last_line\\\": 8, \\\"match\\\": true, \\\"observed\\\": null, \\\"predicted\\\": null}\\n\"}], \"finding\": \"detector_clean\"}\n",
      "subject_sha256": "990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c",
      "timeout_seconds": 25
    },
    {
      "argv": [
        "/usr/bin/python",
        "-I",
        "-B",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/detector.py",
        "--comparator",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py",
        "--fixtures",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/fixtures.json"
      ],
      "exit": 1,
      "fixed_inputs_sha256": {
        "boolean_last_line.json": "c6d925075b3710b96397b0a3ea14a9521789f32dcb8cd6d332c875cd7955001a",
        "bounded_silent_positive.json": "fddfcd668b61a7dd08b161e4c14f3d5841ece053ffe693781e21c60d072414fa",
        "detector.py": "6487a7854e91b6885d3ac321ef92ade48c9c2320f966afd70b42651219255262",
        "extractor.py": "c8ce979c2002884f592379e5b3641f9eab95f6b098d82fa0aa99a39104675b4a",
        "fixtures.json": "f3c3da5c0dd4063bf0671e84174e33294701c456a106f0f04cd1d9afd28507a9",
        "prediction.json": "87506da68595eb57e664a9a6030df97f0576af0f80626152c2e9ac0875d33ee3"
      },
      "phase": "mutated",
      "stderr": "",
      "stdout": "{\"cases\": [{\"argv\": [\"/usr/bin/python\", \"-I\", \"-B\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py\", \"--prediction\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/prediction.json\", \"--log\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/boolean_last_line.json\", \"--extractor\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/extractor.py\"], \"exit\": 0, \"expected_exit\": 2, \"expected_result\": {\"error\": \"invalid_last_line\", \"finding\": \"comparison_unevaluable\", \"match\": null, \"observed\": null, \"predicted\": null}, \"id\": \"boolean_last_line\", \"ok\": false, \"parsed\": {\"finding\": \"failure_match\", \"last_line\": true, \"match\": true, \"observed\": null, \"predicted\": null}, \"stderr\": \"\", \"stdout\": \"{\\\"finding\\\": \\\"failure_match\\\", \\\"last_line\\\": true, \\\"match\\\": true, \\\"observed\\\": null, \\\"predicted\\\": null}\\n\"}, {\"argv\": [\"/usr/bin/python\", \"-I\", \"-B\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py\", \"--prediction\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/prediction.json\", \"--log\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/bounded_silent_positive.json\", \"--extractor\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/extractor.py\"], \"exit\": 0, \"expected_exit\": 0, \"expected_result\": {\"finding\": \"failure_match\", \"last_line\": 8, \"match\": true, \"observed\": null, \"predicted\": null}, \"id\": \"bounded_silent_positive\", \"ok\": true, \"parsed\": {\"finding\": \"failure_match\", \"last_line\": 8, \"match\": true, \"observed\": null, \"predicted\": null}, \"stderr\": \"\", \"stdout\": \"{\\\"finding\\\": \\\"failure_match\\\", \\\"last_line\\\": 8, \\\"match\\\": true, \\\"observed\\\": null, \\\"predicted\\\": null}\\n\"}], \"finding\": \"detector_failed\"}\n",
      "subject_sha256": "ebd9b5b8da17ebdb82e0f1e44c5e5dfcb4b4104fbfe8b42d09cce06307efb271",
      "timeout_seconds": 25
    },
    {
      "argv": [
        "/usr/bin/python",
        "-I",
        "-B",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/detector.py",
        "--comparator",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py",
        "--fixtures",
        "/tmp/kaidoku-r21-attack67-37iu6jc1/fixtures.json"
      ],
      "exit": 0,
      "fixed_inputs_sha256": {
        "boolean_last_line.json": "c6d925075b3710b96397b0a3ea14a9521789f32dcb8cd6d332c875cd7955001a",
        "bounded_silent_positive.json": "fddfcd668b61a7dd08b161e4c14f3d5841ece053ffe693781e21c60d072414fa",
        "detector.py": "6487a7854e91b6885d3ac321ef92ade48c9c2320f966afd70b42651219255262",
        "extractor.py": "c8ce979c2002884f592379e5b3641f9eab95f6b098d82fa0aa99a39104675b4a",
        "fixtures.json": "f3c3da5c0dd4063bf0671e84174e33294701c456a106f0f04cd1d9afd28507a9",
        "prediction.json": "87506da68595eb57e664a9a6030df97f0576af0f80626152c2e9ac0875d33ee3"
      },
      "phase": "restored",
      "stderr": "",
      "stdout": "{\"cases\": [{\"argv\": [\"/usr/bin/python\", \"-I\", \"-B\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py\", \"--prediction\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/prediction.json\", \"--log\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/boolean_last_line.json\", \"--extractor\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/extractor.py\"], \"exit\": 2, \"expected_exit\": 2, \"expected_result\": {\"error\": \"invalid_last_line\", \"finding\": \"comparison_unevaluable\", \"match\": null, \"observed\": null, \"predicted\": null}, \"id\": \"boolean_last_line\", \"ok\": true, \"parsed\": {\"error\": \"invalid_last_line\", \"finding\": \"comparison_unevaluable\", \"match\": null, \"observed\": null, \"predicted\": null}, \"stderr\": \"\", \"stdout\": \"{\\\"error\\\": \\\"invalid_last_line\\\", \\\"finding\\\": \\\"comparison_unevaluable\\\", \\\"match\\\": null, \\\"observed\\\": null, \\\"predicted\\\": null}\\n\"}, {\"argv\": [\"/usr/bin/python\", \"-I\", \"-B\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/compare-first-failure.py\", \"--prediction\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/prediction.json\", \"--log\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/bounded_silent_positive.json\", \"--extractor\", \"/tmp/kaidoku-r21-attack67-37iu6jc1/extractor.py\"], \"exit\": 0, \"expected_exit\": 0, \"expected_result\": {\"finding\": \"failure_match\", \"last_line\": 8, \"match\": true, \"observed\": null, \"predicted\": null}, \"id\": \"bounded_silent_positive\", \"ok\": true, \"parsed\": {\"finding\": \"failure_match\", \"last_line\": 8, \"match\": true, \"observed\": null, \"predicted\": null}, \"stderr\": \"\", \"stdout\": \"{\\\"finding\\\": \\\"failure_match\\\", \\\"last_line\\\": 8, \\\"match\\\": true, \\\"observed\\\": null, \\\"predicted\\\": null}\\n\"}], \"finding\": \"detector_clean\"}\n",
      "subject_sha256": "990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c",
      "timeout_seconds": 25
    }
  ],
  "setup": {
    "axes": [
      "calibration: distinguish detector sensitivity from production failure",
      "depth: malformed boolean bound versus bounded silence",
      "containment: external scratch only and exact restoration"
    ],
    "frozen_hashes": {
      "claims.json": "4031488cb792eac159517927584fc7c18da65ddc427d985c4c0ce5dc4077947a",
      "fixture-contract.json": "04f54077f09bd68f9314f2c9b9febf10cb4b0434990dee51ea797fda9aa700f6",
      "fixtures/battery.json": "2ff59eb249f0535ec3ff840d0c10f9fbf6fcf41b952bbe1bde4874e62fb752ba",
      "fixtures/expected.json": "a792b3fae1dc383f1ed1476b8536fe93196e90eaf77dddb88ff296f1794eb315"
    },
    "python_executable": "/usr/bin/python",
    "python_version": "3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]",
    "scratch": "/tmp/kaidoku-r21-attack67-37iu6jc1",
    "scratch_before_sha256": "990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c",
    "source_before_sha256": "990bc17c6dd5a4fc80d89e27a30c26916ec9f42e012a94c1f3ea69f6bb92ef5c",
    "source_matches_scratch": true,
    "source_path": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py"
  }
}
```

## Tools and disposition

Existing CPython `3.14.8` at `/usr/bin/python` was used for the inert detector/comparator/extractor and bounded hash work. No tool was installed or updated, and no package/service/boot change was made. The only retained write in the lane is this requested report; the one external scratch tree was restored and removed. Local mutation verdict: **killed**. No production patch is proposed.

Report: .ufo/waves/round-21/w2/R21Attack67.md
