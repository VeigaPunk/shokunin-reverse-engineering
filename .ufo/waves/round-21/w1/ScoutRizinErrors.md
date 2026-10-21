# R20 Rizin retained error envelopes

## Scope and axes

Read-only inspection of the named R20 Rizin PE evidence and its verifier/source-note records only. Axes: calibration (separate the observed output from causal interpretation) and depth (compare both retained refusal formats with the Rizin command-level error record). No Rizin, REA, provider, or carrier was executed; no external URL was opened; no production/source-row files were changed.

## Observed facts — high confidence

- Missing-path and directory inputs both returned the same default-format refusal. Their receipts record CLI `exit: 1`, empty stderr, and `evidence_ids: []`; the input kinds are respectively `nonexistent_path` and `directory`. Default TOON stdout has six fields/lines: `code: invalid_request`, `category: invalid_input`, a generic message, `retryable: true`, and `remediation.action`. Sources: `evidence/c2/rizin-pe/03-missing-path/receipt.json:7-14` and `stdout.toon:1-6`; `04-directory-path/receipt.json:7-14` and `stdout.toon:1-6`. The stdout hashes are identical within this pair (`5bf61c…d0b08`).
- `--format json --full-output` retains the equivalent outer shape: `ok:false`, `error` with the same code/category/message/retryable/remediation fields, and `meta` with `command:"execute-rizin-command"` plus duration. Both missing-path and directory receipts still record exit 1, empty stderr, and no Evidence IDs; both stdout files are 293 bytes with SHA-256 `eeb353…a1f24`. Sources: `07-missing-json-full/receipt.json:7-14` and `stdout.json:1`; `08-directory-json-full/receipt.json:7-14` and `stdout.json:1`.
- The retained unknown-command example is a distinct shape, not a REA refusal: its receipt records CLI exit 0 and Evidence ID `ev_27ac86a5783d8c598fb3a043b82b01cef7154d493710a6bd1800c1815ec9c4e6` (`05-unknown-command/receipt.json:7-14`). Its Evidence stdout has `operation: execute_rizin_command`, with `raw_result.stderr` containing Rizin's `ERROR: Command 'kr20_unknown_command' does not exist.`; raw `exit_code` is 0 and `completion_status` is `complete` (`05-unknown-command/stdout.toon:14-42`). The verifier likewise distinguishes this as a command-level error, not a REA refusal (`w2/EntryRizinQuality.md:18`).

## Interpretation — bounded

The four path-error records are refusal envelopes, but they are not Evidence records carrying a matching Evidence ID and operation: their receipts have empty `evidence_ids`; the JSON `meta.command` is the CLI command name, not an Evidence `operation`. Therefore these exact retained records do **not** instantiate fixture-contract C1 `error_envelope` as worded (which requires the matching ID and operation to remain inside the typed refusal envelope). They can inform error-shape fixtures, but that C1 case requires a separate synthetic envelope with those identity fields.

The R20 installed-source note attributes the two path failures to the generic `invalid_input` projection and says the output does not expose the underlying filesystem cause. Exact located quote (11 words): “The tool output does not itself identify the failing filesystem operation” (`evidence/c2/rizin-pe/rea-cli-source-notes.md:14`). Its cited implementation anchors are retained second-hand in that note: `ReverseEngineeringService.js:150-168` and `:617-622` (`rea-cli-source-notes.md:7-8`). The note says ordinary digest failures are converted to `AnalysisInputError`, excluding access-denied and timeout (`:7`); this is source-backed interpretation, not an observed error field. `w2/EntryRizinClaims.md:8-9` independently flags overgeneralizing that mapping and notes that output does not expose errno.

## Remaining unknowns

- No evidence here establishes error behavior for other REA failures or Rizin versions; `provider.version` in the retained command observation is null (`05-unknown-command/stdout.toon:10-12`).
- This scout did not reopen the installed `dist/` implementation itself or any external documentation; only the retained R20 source note and verifier report were inspected. No upstream URL/date is newly asserted.
- No current R21 validator behavior was tested or reviewed; these findings are advisory historical evidence only.

## Checks / handoff

No tests, build, lint, formatter, smoke, or REA/Rizin execution was run. Parent should run the stable changed-path smoke and final suite once, after integration, as assigned.

Report: .ufo/waves/round-21/w1/ScoutRizinErrors.md
