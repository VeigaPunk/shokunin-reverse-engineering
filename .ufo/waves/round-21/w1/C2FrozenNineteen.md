# C2 frozen-nineteen review

**Axes:** C1 calibration (tied-lowest); C2 depth. This assignment reviews C2 only. **Scope:** retrospective read-only inspection of the round-20 comparator/extractor, the named `verb-coverage.py` predicate, retained nineteen comparator artifacts and their Ghidra logs. No producer, runtime, validator, or test was executed; no production file was edited.

## Finding

### P2 — a missing failure `index` escapes as a crash instead of a typed invalid-input result

In `.ufo/waves/round-20/tools/compare-first-failure.py:20-25`, `validate_failure` obtains `index` with `value.get(field)`, so an absent key is treated like explicit JSON `null` and passes validation. `same_failure` then directly indexes `predicted["index"]` / `observed["index"]` at line 34. The caller at lines 81-99 catches only `OSError` and `ValueError`; a `KeyError` from either absent member therefore escapes the comparison path instead of yielding the contract's exit 2 for malformed input. This violates the frozen C2 `missing_index` case (an absent index is distinct from a present nullable index).

**One reviewer-specified synthetic positive/negative pair (not executed, supplementary; do not change the frozen denominator):**

- Positive: prediction `first_failure.h1 = {"kind":"eof","index":null,"va":null,"phase":"analysis"}`; extractor emits `{"first_failure":{"kind":"eof","index":null,"va":null,"phase":"analysis"},"last_line":4}`. Expected: exit 0, `match:true` (explicit nullable EOF index is valid).
- Negative: same prediction and envelope, but omit `index` from the observed `first_failure`. Expected: exit 2 with an invalid/missing-index finding and no uncaught traceback. On the inspected baseline, the validator lets the omission through and the later direct lookup raises `KeyError` (source-derived expectation; not run).

This is a schema/error-path defect, not evidence that any of the retained nineteen comparisons was a false match. It is narrower than a general claim about comparator correctness.

## Retained nineteen: observed compatibility

The retained `.ufo/waves/round-20/evidence/compare-rerun/summary.txt:1-19` records all 19 comparisons as `exit=0`, `logsha_ok=y`. I read each corresponding one-line `t1246-*.json` artifact; the recorded pairs are 8 matching non-null `invalid_index` kind/index pairs and 11 `null`/`null` pairs. No retained comparison record shows a kind or index disagreement.

| Pair | Frozen prediction and observed failure | Raw-log witness |
|---|---|---|
| `addr2line` | `invalid_index / 22078465` | `runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log:186` |
| `compile` | `invalid_index / 36421889` | `runs/t1246-compile/logs/rea-ghidra-Q6goA3/ghidra.log:384` |
| `go` | `invalid_index / 35082496` | `runs/t1246-go/logs/rea-ghidra-2PFXTv/ghidra.log:593` |
| `nm` | `invalid_index / 22070273` | `runs/t1246-nm/logs/rea-ghidra-xpz849/ghidra.log:195` |
| `objdump` | `invalid_index / 13816064` | `runs/t1246-objdump/logs/rea-ghidra-uLjgCv/ghidra.log:196` |
| `pprof` | `invalid_index / 27091201` | `runs/t1246-pprof/logs/rea-ghidra-hCPl3X/ghidra.log:472` |
| `trace` | `invalid_index / 25696001` | `runs/t1246-trace/logs/rea-ghidra-Vwh31x/ghidra.log:577` |
| `vet` | `invalid_index / 13791488` | `runs/t1246-vet/logs/rea-ghidra-AW49O8/ghidra.log:230` |

For each non-null case, the retained comparison JSON (`evidence/compare-rerun/t1246-<name>.json:1`) reports the same kind/index as the matching raw `Invalid index:` line. Predicted phase is `markup_walk` while observed phase is `markup`; predicted VA is populated while observed VA is null. That is an intentional equality: `same_failure` compares only kind and index (`compare-first-failure.py:28-34`), and its selftest explicitly exercises differing phase/VA (`:111-115`). The 11 null/null pairs are `asm`, `buildid`, `cgo`, `covdata`, `cover`, `doc`, `fix`, `gofmt`, `pack`, `preprofile`, and `test2json`; their comparison artifacts each record `match:true` and null/null. These are bounded first-failure observations, not proof that every analyzer or the overall target succeeded.

The extractor reports `last_line` separately and defines null as absence only through that bound (`first-failure-extract.py:134-149,189-195`). The R20 comparator recognizes an envelope by the presence of both `first_failure` and `last_line`, then projects the `first_failure` member (`compare-first-failure.py:72-78`). I did not infer unbounded silence from the null comparison records. R20's verifier spot-check also called for asymmetric-null/kind negatives under `R20-EVIDENCE`; the finding above supplies the specific absent-versus-null index error path, not a new forecast or a changed historical outcome.

`verb-coverage.py:136-165` counts a target as exercised only when a cited Evidence ID, same-entry cited C2 artifact path, operation token(s), and no refusal/error token bind. This is a separate C2 coverage predicate; it neither establishes nor changes first-failure kind/index compatibility. No finding in that predicate is made by this scoped review.

## Residual risk and verification gaps

- **Not run:** no tests, build, lint, validator, or smoke. Parent should run the frozen round-21 C2 battery after integration, preserving all twenty fixed cases and the nineteen historical exact-artifact matches; specifically assert the proposed explicit-null/missing-index pair returns 0/2 without traceback. Parent owns the one stable changed-path smoke and final suite.
- No `lsp` device/server was exposed in this session, so references, definition, and diagnostics requests were unavailable. Direct source reads support the cited control-flow finding; literal log matching was used only as retained-text evidence, not as semantic caller proof.
- No install/update was needed.

Report: .ufo/waves/round-21/w1/C2FrozenNineteen.md