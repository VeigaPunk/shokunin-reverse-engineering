# RevValidatorPaths — receipt-validate.py path resolution and the da64646 prediction

Verdict: **exit 1**, measured on 8/8 `da64646` receipts (`invalid=8, unreadable=0, valid=0`).
The validator resolves every payload through the **absolute path strings stored in the receipt**;
there is no receipt-relative or rebase resolution. The receipts fail today because the pass-1 log
tree was replaced between `da64646` and `A`, not because of the missing `carrier.md5_pre` /
`binding.md5_ok` fields.

Shorthand: `RV` = `.ufo/waves/round-17/tools/receipt-validate.py` (last touched by `d0ab299`, S,
2026-10-20 14:47:24Z; working tree clean against HEAD `9011581`). Round 18 has no second copy
(`find .ufo/waves/round-18 -name 'receipt-validate*'` → empty), so this is the one canonical runtime.

Axes named before measuring: **A1 calibration** (does a right-looking claim survive re-execution?),
**A2 operability** (can the L1 actually reproduce a verdict from a historical receipt?), **A3 depth**
(what does a red mean — tampering, or a stale checkout?).

## Direct answer: yes, absolute paths, no rebase

- `walk_pairs` takes the stored string verbatim — `path = node.get("path")` (RV:294) — then
  `verify_file` does `os.path.isfile(path)` (RV:206) and `sha256_file(path)` (RV:215). No prefix
  is ever stripped or joined with the receipt's own directory.
- `verify_pin_entries` iterates the pins mapping and passes **its keys**, which are absolute
  filesystem paths, straight to `verify_file` (RV:267).
- `check_binding` pulls the log path out of `retained_logs[…].files.ghidra.log.path` (RV:154) and
  `open(path, "rb")` (RV:158); a missing file becomes `text = ""` (RV:160), so both line checks
  fail (RV:164-169).

Consequence: a receipt is bound to one host/checkout. Feeding receipts extracted from git does not
validate the tree they were recorded against — it validates whatever now sits at those paths.

## Prediction (formed before the validator run below)

From the code plus a path sweep of the eight `da64646` receipts:

- every receipt records 5 payload nodes: the carrier (live, digest matches) and `ghidra.log` +
  `script.log`, each committed **twice** (`retained_logs[0]` and `steps.analyze.retained_logs[0]`);
- all 292 pin entries (pre+post, incl. `predictions/pro-op.prediction.json`, `selection.py`, the
  carrier) resolve and match;
- all four repo-internal payload nodes per receipt point at `…/runs/<label>/logs/rea-ghidra-<OLD>/`
  directories that were **deleted** by the second pass.

Predicted exit: **1** — `missing_file` ×4 per receipt plus `binding_mismatch`, never 2 (the receipt
JSON itself is readable), never 0 (two committed log files per receipt are gone).

## Measured (independent run, not Validate16Run's result)

```
$ python3 -I RV <(git show da64646:…/calib-esbuild-0.25.12/receipt.json) … (8 receipts)
{"exit":1,"counts":{"invalid":8,"receipts":8,"unreadable":0,"valid":0}}
VALIDATOR_EXIT=1
```

Per receipt: `checks_performed=333`; 7 receipts produce 5 findings
(`binding_mismatch` at `$.bound_sessions`, `missing_file` ×4), `pro-aether` produces 6 (adds
`sha256_mismatch` at `$.steps.analyze.stdout`, because HEAD's `analyze.json` differs from the
`da64646` blob). 41 findings total.

Control, same tool and revision, the 8 live second-pass receipts:

```
{"exit":0,"counts":{"invalid":0,"receipts":8,"unreadable":0,"valid":8}}
LIVE_VALIDATOR_EXIT=0
```

So the red is environmental, not a tool regression.

## Why 1 and not 0 or 2 — exact chain

1. `classify` → `carrier` (`steps` is a dict, `carrier` is a dict), RV:98-109.
2. `check_required` passes: `CARRIER_REQUIRED` (RV:60-64) does **not** list `carrier.md5_pre` or
   `binding.md5_ok`, and `CARRIER_STEP_REQUIRED` (RV:65-68) does not either. The missing fields are
   not findings.
3. `check_binding` (RV:119) recomputes the carrier MD5 from live bytes (RV:143-150) and requires the
   retained log to carry three line-anchored records. The log is missing, so `logfile_ok` and
   `target_ok` are false and the conjunction at RV:177 appends `binding_mismatch`.
4. `walk_pairs` (RV:285) reaches each `path` node (RV:294) and `verify_file` emits `missing_file`
   (RV:206-213).
5. `validate_paths` counts `invalid` (RV:493-494); `unreadable` is 0, so the ladder at RV:495-499
   selects **1**.

Exit 2 is reachable only for an unreadable/non-JSON receipt or absent `pins.py` (RV:30-31,
RV:732/RV:737, RV:495-496); none applies here. `pins.py` is present and the JSON parses.

## Counterfactual at da64646 — inference, not observation

I did not check out `da64646` (lane rules forbid git writes). Static substitution instead:

- every repo-internal payload path resolves as a `da64646` blob with **exactly** the recorded
  sha256: 4/4 payload nodes (2 distinct log files, each committed twice), 0 mismatches, 0 absent;
  each external carrier (`/usr/bin/op`, `/usr/bin/shfmt`, …) matches 1/1;
- re-running the binding predicate on the `da64646` log blobs reproduces
  `logfile_ok=true, target_ok=true, md5_ok=true` for 8/8, and `pins.compare(pre, post)` reproduces
  the recorded `equal=true/changed=[]/missing=[]/errors=[]` for 8/8.

Therefore the **same** validator would have returned **0** on these receipts at `da64646`. Today's
**1** is entirely path relocation.

## Findings by severity

**High — the R17-VALIDATE16 remedy will produce a red, not the green it is meant to substantiate.**
`corpus/lessons/round-17-verifier-spotcheck.md:138` (item 2; the brief cites `:139`) proposes
retaining a run over `git show da64646:…/receipt.json`. Any faithful execution now yields exit 1
(measured above), because RV:294/RV:206 resolve absolute payload paths and the pass-1 `logs/`
directories were deleted. Note `SCORECARD.md:2364` also says "MD5-anchored binding" — the
**recomputed** MD5 anchor is real (RV:143-150, RV:174-177); the *recorded* field is not.
Recommendation: correct the count to the 8 second-pass receipts (which do exit 0),
or land a path-rebase option and validate a materialized pass-1 tree, and in either case record
that the `da64646` red at HEAD means "pass-1 tree replaced", not "receipt invalid".

**High — receipts are not relocatable, and the sanctioned sandbox cannot reproduce them.**
Because recorded paths are absolute, validating from the contract's only permitted write location
(a `mkdtemp` clone) still reads the **original lane's** bytes; the clone's own `da64646` tree is
never consulted. That makes a green historical validation unreproducible out of tree and makes a
red ambiguous between "stale checkout" and "tampering". Suggested fix: `--root SRC=DST` (or
`<stem>_relpath` alongside `<stem>_path`) applied at RV:294, RV:267 and RV:154, so one receipt
works against any materialized copy. This is a genuine operability gap, not a style preference.

**Medium — exit semantics conflate "bytes missing" with "bytes changed".**
`missing_file` and `sha256_mismatch` both count as `invalid` (RV:493-498). For a historical audit,
an all-payload-missing receipt is *unevaluable at this revision*; RV:30-31 already reserves that
notion for exit 2 ("cannot evaluate"), but only for receipt-level failures. Either promote
"every recorded payload path absent" to unreadable/2 or add a distinct exit 3 so a stale tree is
not reported as an invalid receipt. As written, `pro-aether`'s single `sha256_mismatch`
(RV:225-232) and a wholesale deleted tree produce the same code.

**Medium — the md5-field premise does not affect any validator verdict.**
`carrier.md5_pre` and `binding.md5_ok` are never read by `check_binding`; `md5_ok` is a local
variable initialised to `None` (RV:173) and `None` passes the test at RV:177. Measured: the live 8
receipts also have **no** `carrier.md5_pre`, and their recorded `binding` is only
`{"logfile_ok":true,"target_ok":true}` with no `md5_ok`, yet they exit 0. `da64646` receipts have
no `binding` at all. So R17-PRODUCER-REV is a provenance defect only — do not cite field absence as
a validator failure cause, and do not expect re-running the validator to surface it.

**Low — duplicate commitments double-count findings.** Each log is recorded in both
`retained_logs[0]` and `steps.analyze.retained_logs[0]`, so two missing files yield four
`missing_file` findings. Harmless but inflates the report a reader will parse.

**Low — reproduction trap with stdin.** Eight `/dev/stdin` arguments read one stream: the first
receipt parses, the rest see EOF and become `invalid JSON` → `unreadable` → **exit 2**, not 1.
Use one process per receipt or process substitution (`/dev/fd/N`), as done above.

## Residual risk and verification gaps

- The counterfactual "0 at da64646" is inference from blob digests plus an emulation of
  `check_binding` and `pins.compare`; no checkout was executed.
- I did not read Validate16Run's output (per the assignment); the run above is my own.
- The tool's stated limitation stands (`RV:34-37`): it proves the bytes present **now** match; it
  cannot prove pass-1 bytes were unmodified during the run.
- I did not run `--selftest`; the verdict rests on direct execution over the real receipts, which
  is stronger for this question.
- External carriers were assumed unchanged; checked — every carrier digest still matches its
  receipt (5/5 payload nodes per receipt: 4 blobs + 1 external).

## Commands and exit codes (observed)

| # | Command (abridged) | Exit |
|---|---|---|
| 1 | `git rev-parse --short HEAD` → `9011581` | 0 |
| 2 | `git ls-tree -r --name-only da64646 -- .ufo/waves/round-17/runs` → 8 `receipt.json` | 0 |
| 3 | path/digest sweep of the 8 receipts (Python, read-only) → 4 missing nodes, 292/292 pins ok each | 0 |
| 4 | `python3 -I RV <(git show da64646:…/receipt.json) ×8` | **1** |
| 5 | `python3 -I RV .ufo/waves/round-17/runs/*/receipt.json` (8 live) | **0** |
| 6 | blob substitution at `da64646` → 4/4 repo blobs + 1/1 external carrier match per receipt | 0 |
| 7 | emulated binding + `pins.compare` on `da64646` blobs → 8/8 true | 0 |

No installs or upgrades were performed; nothing outside this file was written; no git/jj writes.
