# R22-C1 duplicate-name / nonfinite-number review

## Finding

**P3 — A floating-point overflow in unused envelope metadata is accepted as a nonfinite value.** This is a parser strictness gap, not an evidence-ID/operation binding bypass.

`count-c1.py::bind_cli` decodes the whole CLI envelope with `r21.decode`, checks `ok`, refusal state, and `meta.command`, then serializes only `envelope["data"]` for the second `r21.bind` call (`.ufo/waves/round-22/tools/count-c1.py:54-68`). The helper rejects duplicate object members and explicit JSON constants `NaN`/`Infinity`/`-Infinity` (`.ufo/waves/round-21/tools/verb-coverage.py:24-36`), but supplies no `parse_float` handler or post-decode finite-number check. Python's default float parser maps `1e999` to `inf`. When that token is in `meta.score`, the decoded metadata is neither checked nor passed into the second binding parse, so the otherwise valid envelope is counted.

Concrete scratch-repository result: the clean positive control counted all six T1 verbs, exit 0; adding `"score": 1e999` to the `identify-flutter-build` envelope's `meta` still reported `c1_complete`, 6/6, exit 0, with that evidence listed as bound. The same overflow in `data` did **not** count: `json.dumps(envelope["data"])` renders the float as `Infinity`, which the helper's second decode rejects; result 5/6, exit 1. Thus the gap is specifically whole-envelope validation, not a general failure of the record binder.

This finding is limited: it does not forge the cited evidence ID, operation, command, or successful `ok` state. If the contract means only to reject the non-standard JSON tokens `NaN` and `Infinity`, then `1e999` is a legal JSON number and this is a host-float strictness edge rather than a contract violation. If the intended invariant is that no decoded evidence envelope contains a non-finite numeric value, the current behavior violates it. Narrow fix: in C1, reject any decoded float for which `math.isfinite` is false across the entire envelope before accepting it (or use a strict `parse_float` when decoding); add a fixture with `1e999` in `meta`. Keep the existing duplicate-name hook.

## Duplicate names and explicit nonfinite constants

No bypass found for duplicate JSON names. I mutated both the envelope (`ok: false` followed by duplicate `ok: true`) and nested `data.operation` (wrong value followed by the matching duplicate). Both files became unsupported candidates; `identify-flutter-build` was not exercised, count fell to 5/6, exit 1. The duplicate-pair hook runs during the first decode of the complete envelope, so duplicate keys at either depth cannot exploit last-key-wins parsing.

Explicit `NaN` and `Infinity` in envelope metadata were likewise rejected and not counted (5/6, exit 1). The existing C1 selftest's `duplicate_json` case also passes its expected refusal control.

## Commands and observed results

Runtime used: Python 3.14.8 and Git 2.56.0 already available; no tools installed. Mutants and commits were confined to temporary `/tmp/r22-c1-json-*` repositories. Each matrix case ran the exact child argv shown in the JSON attachment, of the form:

```text
/usr/bin/python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --root <temporary-repo> --rev <fixture-commit>
```

All matrix subprocesses had empty stderr. The counter writes a large one-line JSON document (including the 153-command catalog); exact selected stdout fields and each exact argv/exit are recorded in `C1Duplicate.json`.

| Case | Observed stdout fields | Exit |
|---|---|---:|
| Clean positive | `claim=R22-C1`, `finding=c1_complete`, `t1_exercised_count=6`; identify target exercised with cited ID and path | 0 |
| Duplicate nested `operation` | `finding=c1_incomplete`, count 5; identify target false, file in `unsupported_candidates` | 1 |
| Duplicate envelope `ok` | `finding=c1_incomplete`, count 5; identify target false, file in `unsupported_candidates` | 1 |
| `NaN` in `meta.score` | `finding=c1_incomplete`, count 5; identify target false, file in `unsupported_candidates` | 1 |
| `Infinity` in `meta.score` | `finding=c1_incomplete`, count 5; identify target false, file in `unsupported_candidates` | 1 |
| `1e999` in `meta.score` | `finding=c1_complete`, count 6; identify target remains exercised/bound | 0 |
| `1e999` in `data` | `finding=c1_incomplete`, count 5; identify target false, file in `unsupported_candidates` | 1 |

Also ran:

```text
python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-22/tools/count-c1.py --selftest
```

Observed exit 0, stderr empty, `counter_controls_clean`; all 18 current C1 fixture controls passed, including `all_six` (count 6/exit 0), `duplicate_json` (count 0/exit 1), and `helper_drift` (count 6/exit 0). The attached JSON includes the compact per-case output summary.

## Residual risk / verification gaps

The overflow case is a narrowly scoped parser-policy issue; the task's stated local binding limitation remains in force, and this review does not establish cryptographic authenticity or source relevance. No production files were changed. The exposed tool inventory provided no LSP device/status route, so no LSP semantic caller/definition/diagnostics checks were available; no grep result is used as semantic proof. No REA device, target execution, or external connection was used.
