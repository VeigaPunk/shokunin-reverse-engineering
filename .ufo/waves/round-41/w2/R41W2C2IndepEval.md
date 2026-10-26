# R41W2C2IndepEval — third evaluator vs frozen evaluator/interpreter

**Verdict: DONE — the R41-C2 landing survives an independent falsification attempt.** I wrote a third
evaluator **only** from the frozen `**Label precedence (frozen ...)**` text in
`plans/round-41-claims.md` (lines 109–132), ran it on all 52 held-out envelopes plus the 4 committed
round-40 C1 receipts, and compared it with the recorded frozen evaluator (`indep-eval-v3.py`) and
frozen interpreter (`sqfs-triage-v3.py`) outputs. **Zero disagreements**: 56/56 inputs get the same
(label, action) pair from my evaluator, the frozen evaluator, and the frozen interpreter, and every
observed feature tuple equals the tuple the manifest declares (52/52, including all 12 combos whose
declared tuples live under manifest key `declared` — corroborating the known `observed_features_match_declared`
binding defect as a counter key-lookup bug, not a data defect).

I attacked: the C2 depth claim's core measurement — whether the frozen precedence text, read
independently, produces the same labels as the frozen evaluator and the frozen interpreter on the held-out
envelopes and on the four real round-40 receipts.

---

## 1. Method

The precedence text defines features of one REA envelope and 12 first-match-wins steps. I implemented
them verbatim in `artifacts/R41W2C2IndepEval/third_eval.py` (stdlib only), without opening
`indep-eval-v3.py`, `sqfs-triage-v3.py` or the SKILL v3 table (per seat bounds). Feature extraction:

- **OP** = `envelope.operation`; **PR** = `envelope.provider.id` (exact, case-sensitive).
- **H** = `normalized_result.chunks[].handler` ∪ `normalized_result.extraction_gaps[].handler`, nulls dropped.
- **G** = set of `normalized_result.extraction_gaps[].kind`.
- **D** = union of gaps' `dependencies`, compared by exact name (never substring).
- **BE** = `yes` if any `diagnostics[].report.command` (a recorded string child argv) carries the token
  `-be`; `no` if commands are recorded and none carries it; `n/a` if none is recorded.
- **SR** = `yes` iff some `diagnostics[].report.__typename__ == "MaliciousSymlinkRemoved"`.
- **P** = `len(normalized_result.files)` (absent reads 0).

Steps 1–12 applied in order, first match wins. For step 5, I apply the text's `(failing chunk's handler
(else H))` literally using H as the fallback; the actual inputs exercise `squashfs_v4_be` at this
step and produce the same outcome under either reading.

Reference outputs for the frozen pair were taken from the committed score receipt
`.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`:
`.carriers[]` rows carry `expected_label/expected_action` (frozen evaluator) and `label/action`
(frozen interpreter) per held-out envelope; `real_receipts.rows.{V1,V2,L1,L2}` carry both for the
round-40 receipts. The receipt itself records `matched: 52`, `distinct_decisions: 13`
(`unclassified_expected/observed: 2`). [INFERENCE] I treat those recorded fields as faithful outputs
of the two frozen tools at revision e9a24d07 (they are the claim's official counter receipt; the
counter's own `pair_match` flags agree with my re-derivation: 52/52 true).

## 2. Commands run (all exit 0)

```
python3 -I -B .../third_eval.py <52 heldout envelope.json> <4 round-40 after.json> --json-out artifacts/full-results.json
python3 -I -B .../compare3.py > artifacts/comparison.json
```

- `compare3.py` runs `third_eval.py` on the same 56 inputs, joins each result with the receipt rows,
  and emits a row per input with `mine / evaluator / interpreter / step` plus three agreement flags.
- Exit codes: both scripts exit 0; all 56 inputs parsed; no exceptions.
- Outputs: `artifacts/full-results.json` (features + step + decision per input, sha256
  `ed2d763b…f050`), `artifacts/comparison.json` (56-row table, sha256 `fbee1f66…81ee`),
  `artifacts/comparison-summary.txt` (sha256 `ac0be4c4…b6b`).

## 3. Results

### 3.1 Agreement (the headline measurement)

| Comparison | Matches |
|---|---|
| third evaluator vs frozen evaluator | **56/56** |
| third evaluator vs frozen interpreter | **56/56** |
| frozen evaluator vs frozen interpreter (recorded pair_match / re-derived) | 56/56 |
| observed feature tuple vs manifest-declared tuple | **52/52** |

All 56 inputs agree on both label and action. There are **no disagreements to adjudicate**; the third
observer reproduces both frozen tools.

### 3.2 Decision distribution on the 52 held-out envelopes (labels as produced by all three)

| (label, action) | count | step |
|---|---|---|
| clean / none | 4 | 11 |
| clean-empty / confirm-empty | 2 | 11 |
| escaping-symlink-removed / expect-link-absent | 2 | 9 |
| in-tree-symlink-metadata / count-gap | 3 | 10 |
| mixed-symlinks / audit-symlinks | 3 | 8 |
| dep-missing-be / install-extractor-be | 2 | 3 |
| dep-missing-le / install-extractor-le | 2 | 3 |
| avm-marker-be-dropped / wrap-extractor-be | 2 | 5 |
| body-extractor-failure / preserve-failure | 4 | 6 |
| partial-body-failure / salvage-partial | 14 | 4 |
| no-squashfs-chunk / inspect-input | 2 | 2 |
| unclassified / none | 2 | 1 |
| depth-limited / raise-depth | 10 | 7 |

13 distinct decisions, matching the frozen counter's `distinct_decisions: 13`; 2 unclassified
(H25/H26, out-of-domain via step 1: `operation = inspect_firmware_regions`, `provider.id = binwalk`).

### 3.3 Round-40 C1 receipts (all four → depth-limited / raise-depth, step 7)

V1, V2, L1, L2 all carry G = {depth-limited, unpublished-entry, …} with a `squashfs_v4_be` chunk and
no diagnostics → step 7 fires before the symlink steps. All three observers agree on all four.

### 3.4 Combo carriers (12/12 agree; tuple check passes)

Combos C01–C12 have `class_expected: null` and their declared tuples under manifest key `declared`;
my independent observed-tuple extraction matches `declared` on all 12 (and on all 40 named classes
against `class_expected.features`). This supports the frozen counter's honest-stop finding that
`observed_features_match_declared` is false **only** because the counter looks for combo tuples under
`class_expected.features`/`features`/`declared_features` — the underlying data satisfies
observed = declared = 52/52.

### 3.5 Readings taken where the text allows more than one implementation

These are the only places a different reading could have produced a different label; I record what I
chose and why, and whether the data exercises the difference:

1. **BE token test** — I use whitespace-split token equality to `-be`. Alternative: substring test.
   On this dataset both readings coincide (no recorded command contains `-be` as a substring inside a
   different token; `sasquatch-v4be` is a single token and is not `-be`, and is not treated as
   carrying it under either reading). No envelope discriminates.
2. **Step 5 fallback** — the text says "the failing chunk's handler (else H)". I interpret "else H"
   as using H when no failing-chunk handler is available, rather than using a gap handler. The held-out
   step-5 envelopes do have a failing chunk handler, so no observed outcome depends on the fallback.
3. **Step-3 "dependency gap naming neither"** — not exercised: all `missing-extractor-dependency`
   gaps name `sasquatch-v4be` or `sasquatch` exactly (4 envelopes).
4. **Step-11 "absent reads 0"** — `files` is present in all 56 envelopes; `published` ⇔ P>0 is
   consistent with the manifest's `published` declaration everywhere.

No other normative ambiguity was reachable in the data.

## 4. Conclusion

The frozen precedence text, implemented independently, reproduces the frozen evaluator and the frozen
interpreter exactly on every held-out envelope and on the four round-40 receipts. The C2 landing's
central measurement (interpreter ≡ evaluator on 52/52) is corroborated by a third, text-only reader;
the claim's honest stop remains solely the `observed_features_match_declared` counter key-lookup
defect, which the data itself does not exhibit. Nothing in this review falsifies R41-C2; the
landing's scoring evidence is internally consistent.

## 5. Bounds / hygiene

- Wrote only: `.ufo/waves/round-41/w2/R41W2C2IndepEval.md` and
  `.ufo/waves/round-41/w2/artifacts/R41W2C2IndepEval/` (third_eval.py, compare3.py, full-results.json,
  comparison.json, comparison-summary.txt).
- No git/jj mutations (read-only reads only); no REA/unblob runs (not needed); no tools installed;
  scratch `$S` removed before finish.
