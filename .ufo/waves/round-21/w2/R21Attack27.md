# R21Attack27 — C2 `missing_index`

## Axes and scope

- **Depth (C2):** exercised only frozen case `missing_index` through the actual successor CLI.
- **Calibration (C1):** not exercised; this run makes no C1 claim.
- No production or fixture files were edited. No analyzed carrier or provider was invoked.

## Findings by severity

### No actionable finding in the scoped case

The case supplies a predicted failure with integer index `9`, while its bounded extractor observation omits `index` (`fixtures/battery.json:275-288`). The independent fixture contract declares exit **2** because the failure index member must exist; nullable and absent are distinct (`fixture-contract.json:34`). The frozen battery case also declares `expected_exit: 2` (`fixtures/battery.json:275-276`). The successor returned exit **2** and reported `observation: missing_index`, matching both expected exits.

The successor requires all four failure members (`tools/compare-first-failure.py:37-39`); its exception path reports `comparison_unevaluable` and exit 2 (`:73-74`), and the CLI prints that result (`:116-118`).

### Exact execution record

Used an external `/tmp` temporary directory containing the fixture-derived prediction, an empty inert log placeholder, and an extractor stub that wrote the fixture's exact `stdout` and exited 0. The actual temporary directory existed for the invocation and was removed afterward (`/tmp/r21-missing-index-2vyfpd3m`; `tempdir_exists_after_cleanup=false`).

Actual argv:

```json
["/usr/bin/python", "-I", "-B", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-21/tools/compare-first-failure.py", "--prediction", "/tmp/r21-missing-index-2vyfpd3m/prediction.json", "--log", "/tmp/r21-missing-index-2vyfpd3m/inert.log", "--extractor", "/tmp/r21-missing-index-2vyfpd3m/inert_extractor.py"]
```

Expected exit: **2** (frozen case and independent fixture contract).

Observed stdout (including trailing newline):

```text
{"error": "observation: missing_index", "finding": "comparison_unevaluable", "match": null, "observed": {"kind": "invalid_index", "phase": "analysis", "va": null}, "predicted": {"index": 9, "kind": "invalid_index", "phase": "analysis", "va": null}}
```

Observed stderr: empty.

Observed exit: **2**.

This establishes the result only for this fixture-provided observation through the successor CLI. The successor documentation describes the extractor as caller-owned code, not a sandbox, and says the analyzed carrier is not executed (`tools/compare-first-failure.py:2-6`); this run used only the inert stdout stub.

## Nearby counterexample — UNRUN

`boolean_index` keeps prediction index `9` and supplies observation index `true` (`fixtures/battery.json:291-304`). The contract independently declares exit **2** because a boolean is not a failure index (`fixture-contract.json:35`). It was **not executed** here; it would test the distinct bool-versus-int rejection path.

## Residual risk and verification gaps

- Only `missing_index` was run; no other C2 case, full battery, retained R20 regression, or C1 check is covered.
- The extractor output was canned from the fixture, so this does not validate a real extractor or carrier. No analyzed carrier/provider execution occurred.
- The `lsp` route is unavailable in this environment: `read xd://lsp` returned “No such tool.” No LSP status, references, definition, or diagnostics were available; no grep output was used as semantic proof.
- No installs or updates were made.

Report trailer: `.ufo/waves/round-21/w2/R21Attack27.md`
