# R21Attack65 — exact-operation guard mutation

## Result and axes

**Finding `R21Attack65-F1`: KILLED.** One assigned mutation, one unchanged two-case detector, three phases. Actual detector exits were **0 → 1 → 0** (pristine → mutated → restored). The positive control stayed green throughout; `operation_in_notes` alone became `clean=false` under mutation. This is local author-side mutation evidence, not a canonical-runtime verdict or independent acceptance of the round.

- **Calibration:** distinguish a structurally bound operation from the same token appearing only in notes.
- **Depth:** isolate sensitivity to a single operation-match guard, preserve the positive control, then establish exact-byte restoration and behavioral recovery. No C2 comparator result is claimed.

## Claim, scope, and mutation

Read frozen `claims.json` C1: record-bound exact operation/id/refusal evidence must replace token co-occurrence; negatives must not be accepted and positives must remain accepted. This probe covers only the exact-operation component, not cryptographic authentication or the full C1 denominator.

Production source (read/copy/hash only): `.ufo/waves/round-21/tools/verb-coverage.py`, `bind`, line 88. The entire mutation was the following single-line guard change in **external scratch only**, `/tmp/r21attack65-m330lkwg/verb-coverage.py`:

```diff
-            if record.get('evidence_id') != evidence_id or record.get('operation') != operation:
+            if record.get('evidence_id') != evidence_id:
```

The exact evidence-id condition, supported-record traversal, refusal checks, and objdump special handling were untouched. The plausible defect is omission of operation equality while retaining id equality.

## Independent expected detector

Oracle provenance: `.ufo/waves/round-21/fixture-contract.json` C1 `same_record_positive` (line 6) and `operation_in_notes` (line 9), and the two identically named inert cases in `.ufo/waves/round-21/fixtures/battery.json`. These inputs and expected outcomes were frozen outside the target validator and materialized before the pristine run. No target selftest, target import, or target-generated expectation was used.

| Frozen case id | Expected validator exit | Expected finding | Expected bound |
|---|---:|---|---|
| `same_record_positive` | 0 | `evidence_bound` | `true` |
| `operation_in_notes` | 1 | `evidence_unbound` | `false` |

Requested verb was `inspect-wasm-artifact`; cited id was `ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa` in every invocation. Input file contents were UTF-8 with no trailing newline:

`same_record_positive.json`:
```json
{"evidence_id": "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "operation": "inspect_wasm_artifact"}
```

`operation_in_notes.json`:
```json
{"evidence_id": "ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "operation": "inspect_artifact", "notes": "inspect_wasm_artifact"}
```

The detector compared actual subprocess exit, parsed `finding`, and boolean `bound` against the independent oracle. It ran the two independent fixture CLIs concurrently with five-second per-CLI timeouts; the enclosing subprocess had a twenty-second bound. All phases used exactly the same detector command, cwd, inputs, and expectations:

```text
/usr/bin/python3 -I -B /tmp/r21attack65-m330lkwg/detector.py
cwd: /tmp/r21attack65-m330lkwg
```

All actual inner argv are retained losslessly below. Only scratch `verb-coverage.py` changed between phases.

## Actual bounded results

| Phase | Case id | Validator exit | Finding | Bound | Detector case clean |
|---|---|---:|---|---|---|
| pristine | `same_record_positive` | 0 | `evidence_bound` | `true` | `true` |
| pristine | `operation_in_notes` | 1 | `evidence_unbound` | `false` | `true` |
| mutated | `same_record_positive` | 0 | `evidence_bound` | `true` | `true` |
| mutated | `operation_in_notes` | 0 | `evidence_bound` | `true` | `false` |
| restored | `same_record_positive` | 0 | `evidence_bound` | `true` | `true` |
| restored | `operation_in_notes` | 1 | `evidence_unbound` | `false` | `true` |

All six validator stderr streams and all three enclosing detector stderr streams were empty. No timeout or JSON parse failure occurred. Mutant `operation_in_notes` returned successful JSON (`evidence_bound`, exit 0), not a crash; the independent detector rejected that false acceptance with exit 1. The pristine baseline passed both controls, so this is not an inconclusive baseline failure.

## Hashes and restoration

SHA-256:

| Object / phase | SHA-256 |
|---|---|
| Production source before | `77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc` |
| Scratch pristine | `77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc` |
| Scratch mutated | `c312e52bf557914497dbd088b56af6dcce039bb5863910a5e58b0381046ba948` |
| Scratch restored | `77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc` |
| Production source after | `77db29fde196c2a0db19a522d21cf8bf315a383250c7115fda71f04bd141e2cc` |

Scratch restored bytes were compared directly with the original copied bytes: **equal**, 9051 original bytes. Production before/after hashes matched. After restoration, the same two-case detector again exited 0. Detector, oracle, and both fixture hashes were unchanged at the mutation and restored stages:

```json
{
  "detector.py": "6c969394a274f06c9f56f30b445833daaa5d0488d9ecad2ea9b35cb836da7368",
  "expected.json": "0d48a6f5fd6027fe7399bf0e54d0ef82797960675cf64fce98b25fac7c9fef8c",
  "operation_in_notes.json": "4f4c1c284548b255f9f5c65baa5d0376dadaf6268c5326ad3c3f43b896145331",
  "same_record_positive.json": "92c60f2ca66141bc0403d735b65948ef97a019ad5751844c4e431b86cb3112df"
}
```

Restored external scratch cleanup was executed and observed:

```json
{
  "path": "/tmp/r21attack65-m330lkwg",
  "removed": true,
  "restored_before_removal": true
}
```

## Retained independent detector and oracle

The following detector/oracle text is retained in this report because external scratch was removed. Re-encoded SHA-256 values were matched to the unchanged artifacts above before writing this report.

`detector.py`:
```python
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
cases = json.loads((root / 'expected.json').read_text(encoding='utf-8'))


def detect(case):
    argv = [sys.executable, '-I', '-B', str(root / 'verb-coverage.py'),
            '--evidence', str(root / case['fixture']), '--verb', case['verb'],
            '--evidence-id', case['evidence_id']]
    process = subprocess.run(argv, cwd=root, stdin=subprocess.DEVNULL,
                             capture_output=True, text=True, timeout=5, check=False)
    actual = None
    parse_error = None
    try:
        actual = json.loads(process.stdout)
    except ValueError as error:
        parse_error = str(error)
    clean = (process.returncode == case['expected_exit']
             and isinstance(actual, dict)
             and actual.get('finding') == case['expected_finding']
             and actual.get('bound') is case['expected_bound'])
    return {'id': case['id'], 'argv': argv, 'cwd': str(root),
            'expected_exit': case['expected_exit'],
            'expected_finding': case['expected_finding'],
            'expected_bound': case['expected_bound'],
            'exit': process.returncode, 'stdout': process.stdout,
            'stderr': process.stderr, 'parsed': actual,
            'parse_error': parse_error, 'clean': clean}


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(detect, cases))
clean = all(result['clean'] for result in results)
print(json.dumps({'clean': clean, 'cases': results}, sort_keys=True))
raise SystemExit(0 if clean else 1)
```

`expected.json`:
```json
[
  {"id":"same_record_positive","fixture":"same_record_positive.json","verb":"inspect-wasm-artifact","evidence_id":"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","expected_exit":0,"expected_finding":"evidence_bound","expected_bound":true},
  {"id":"operation_in_notes","fixture":"operation_in_notes.json","verb":"inspect-wasm-artifact","evidence_id":"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","expected_exit":1,"expected_finding":"evidence_unbound","expected_bound":false}
]
```

## Complete execution receipts

Lossless JSON strings retain **all stdout and stderr**, including final newlines, and actual argv, cwd, and exits for all three enclosing detector invocations. Each stdout contains the corresponding two inner validator receipts with their actual argv/stdout/stderr/exit; `clean` is the independent detector's comparison, not a validator output field.

```json
[
  {
    "argv": [
      "/usr/bin/python3",
      "-I",
      "-B",
      "/tmp/r21attack65-m330lkwg/detector.py"
    ],
    "cwd": "/tmp/r21attack65-m330lkwg",
    "exit": 0,
    "stage": "pristine",
    "stderr": "",
    "stdout": "{\"cases\": [{\"argv\": [\"/usr/bin/python3\", \"-I\", \"-B\", \"/tmp/r21attack65-m330lkwg/verb-coverage.py\", \"--evidence\", \"/tmp/r21attack65-m330lkwg/same_record_positive.json\", \"--verb\", \"inspect-wasm-artifact\", \"--evidence-id\", \"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"], \"clean\": true, \"cwd\": \"/tmp/r21attack65-m330lkwg\", \"exit\": 0, \"expected_bound\": true, \"expected_exit\": 0, \"expected_finding\": \"evidence_bound\", \"id\": \"same_record_positive\", \"parse_error\": null, \"parsed\": {\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}, \"stderr\": \"\", \"stdout\": \"{\\\"bound\\\": true, \\\"finding\\\": \\\"evidence_bound\\\", \\\"pathless\\\": false}\\n\"}, {\"argv\": [\"/usr/bin/python3\", \"-I\", \"-B\", \"/tmp/r21attack65-m330lkwg/verb-coverage.py\", \"--evidence\", \"/tmp/r21attack65-m330lkwg/operation_in_notes.json\", \"--verb\", \"inspect-wasm-artifact\", \"--evidence-id\", \"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"], \"clean\": true, \"cwd\": \"/tmp/r21attack65-m330lkwg\", \"exit\": 1, \"expected_bound\": false, \"expected_exit\": 1, \"expected_finding\": \"evidence_unbound\", \"id\": \"operation_in_notes\", \"parse_error\": null, \"parsed\": {\"bound\": false, \"finding\": \"evidence_unbound\"}, \"stderr\": \"\", \"stdout\": \"{\\\"bound\\\": false, \\\"finding\\\": \\\"evidence_unbound\\\"}\\n\"}], \"clean\": true}\n"
  },
  {
    "argv": [
      "/usr/bin/python3",
      "-I",
      "-B",
      "/tmp/r21attack65-m330lkwg/detector.py"
    ],
    "cwd": "/tmp/r21attack65-m330lkwg",
    "exit": 1,
    "stage": "mutated",
    "stderr": "",
    "stdout": "{\"cases\": [{\"argv\": [\"/usr/bin/python3\", \"-I\", \"-B\", \"/tmp/r21attack65-m330lkwg/verb-coverage.py\", \"--evidence\", \"/tmp/r21attack65-m330lkwg/same_record_positive.json\", \"--verb\", \"inspect-wasm-artifact\", \"--evidence-id\", \"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"], \"clean\": true, \"cwd\": \"/tmp/r21attack65-m330lkwg\", \"exit\": 0, \"expected_bound\": true, \"expected_exit\": 0, \"expected_finding\": \"evidence_bound\", \"id\": \"same_record_positive\", \"parse_error\": null, \"parsed\": {\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}, \"stderr\": \"\", \"stdout\": \"{\\\"bound\\\": true, \\\"finding\\\": \\\"evidence_bound\\\", \\\"pathless\\\": false}\\n\"}, {\"argv\": [\"/usr/bin/python3\", \"-I\", \"-B\", \"/tmp/r21attack65-m330lkwg/verb-coverage.py\", \"--evidence\", \"/tmp/r21attack65-m330lkwg/operation_in_notes.json\", \"--verb\", \"inspect-wasm-artifact\", \"--evidence-id\", \"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"], \"clean\": false, \"cwd\": \"/tmp/r21attack65-m330lkwg\", \"exit\": 0, \"expected_bound\": false, \"expected_exit\": 1, \"expected_finding\": \"evidence_unbound\", \"id\": \"operation_in_notes\", \"parse_error\": null, \"parsed\": {\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}, \"stderr\": \"\", \"stdout\": \"{\\\"bound\\\": true, \\\"finding\\\": \\\"evidence_bound\\\", \\\"pathless\\\": false}\\n\"}], \"clean\": false}\n"
  },
  {
    "argv": [
      "/usr/bin/python3",
      "-I",
      "-B",
      "/tmp/r21attack65-m330lkwg/detector.py"
    ],
    "cwd": "/tmp/r21attack65-m330lkwg",
    "exit": 0,
    "stage": "restored",
    "stderr": "",
    "stdout": "{\"cases\": [{\"argv\": [\"/usr/bin/python3\", \"-I\", \"-B\", \"/tmp/r21attack65-m330lkwg/verb-coverage.py\", \"--evidence\", \"/tmp/r21attack65-m330lkwg/same_record_positive.json\", \"--verb\", \"inspect-wasm-artifact\", \"--evidence-id\", \"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"], \"clean\": true, \"cwd\": \"/tmp/r21attack65-m330lkwg\", \"exit\": 0, \"expected_bound\": true, \"expected_exit\": 0, \"expected_finding\": \"evidence_bound\", \"id\": \"same_record_positive\", \"parse_error\": null, \"parsed\": {\"bound\": true, \"finding\": \"evidence_bound\", \"pathless\": false}, \"stderr\": \"\", \"stdout\": \"{\\\"bound\\\": true, \\\"finding\\\": \\\"evidence_bound\\\", \\\"pathless\\\": false}\\n\"}, {\"argv\": [\"/usr/bin/python3\", \"-I\", \"-B\", \"/tmp/r21attack65-m330lkwg/verb-coverage.py\", \"--evidence\", \"/tmp/r21attack65-m330lkwg/operation_in_notes.json\", \"--verb\", \"inspect-wasm-artifact\", \"--evidence-id\", \"ev_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"], \"clean\": true, \"cwd\": \"/tmp/r21attack65-m330lkwg\", \"exit\": 1, \"expected_bound\": false, \"expected_exit\": 1, \"expected_finding\": \"evidence_unbound\", \"id\": \"operation_in_notes\", \"parse_error\": null, \"parsed\": {\"bound\": false, \"finding\": \"evidence_unbound\"}, \"stderr\": \"\", \"stdout\": \"{\\\"bound\\\": false, \\\"finding\\\": \\\"evidence_unbound\\\"}\\n\"}], \"clean\": true}\n"
  }
]
```

## Interpretation and bounds

`R21Attack65-F1` establishes that this independent negative detects omission of exact operation matching while the same-record positive remains accepted. It does **not** establish general validator soundness, additional mutant coverage, C2 depth acceptance, cryptographic Evidence authentication, or an outside-verifier result. No production defect was demonstrated by the pristine run; no contract was changed.

Only the expressly authorized inert Python detector/validator CLI runs and local hashes were executed. No REA producers, analyzed/native carriers, builds, formatters, broad suites, Git/jj/index mutations, routing/provider/account/config probes, package transactions, or service changes occurred. No tools were installed or updated. Production source was never edited; the sole repository write is this report. No scratch scaffold remains.

Report: .ufo/waves/round-21/w2/R21Attack65.md
