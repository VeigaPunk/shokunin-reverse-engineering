# R41W2C1Run — C1 harness defect review

**Verdict: DEFECTS FOUND.** I attacked the `tools/round-41/c1-run.sh` after-arm
defect that made V4 the only carrier without a `run.json`. Confirmed: the arm
fails with `jq: Argument list too long` at line 547 whenever the envelope-data
summary exceeds Linux's per-argument cap (131071 bytes) — reproduced on a
synthetic 1600-symlink AVM-genuine carrier (exit 126, identical error line) and
quantified against the real receipts (only V4 crosses the threshold: 146561 B
vs V3 18441 B, L3 1479 B, L4 1465 B). Confirmed: `after.json` is written
*before* the failure and is byte-for-byte the complete REA `data` object
(same-run envelope identity; projection-equal to an independent REA run).
Confirmed: **no counter clause reads `run.json`** — the C1 score path consumes
`after.json` + oracle/nonregular tables + docs only, so V4's missing `run.json`
does not affect the R41-C1 MET verdict (4/4 at e9a24d07, `projection_ok true`).
Delivered: minimal fix (pass summary and receipt via files + `--slurpfile`),
validated end-to-end on the synthetic carrier and at V4 scale.

## 1. Root cause

The after arm builds a JSON `summary` of the receipt (files/gaps/unpublished
detail arrays) in a shell variable, then passes it to jq as one argv element:

- line 546: `receipt=$(jq -n ... --argjson summary "$summary" ...)` (inside the receipt builder),
- line 576: `... --argjson receipt "$receipt" --argjson summary "$summary" \` (final run.json builder).

Linux `MAX_ARG_STRLEN` = 131072 bytes per single argument (incl. NUL). V4's
summary (1017 non-regular rows → 612 gap details + 611 unpublished entries) is
146561 B → `execve` returns `E2BIG` → `jq: Argument list too long`. The harness
has `set -euo pipefail`, so the failure at line 547 terminates the script
immediately (exit 126 = failed exec): after.json (already `mv`-ed at line 541)
lands in the outdir; run.json is never written; the error line is the only
stderr. This exactly matches the committed V4 state (`after.json` 2852279 B
present; `run.json` absent; `run-harness-failure.log` = the single line,
byte-identical (sha256 879b7325…) to `l1/c1-run-V4.log`).

## 2. Reproduction

Synthetic carrier: 640 regular files + 1600 in-tree relative symlinks (160
dirs), AVM-genuine gzip SquashFS v4, sha256
`c1336c15e8e3a6d9564e945f5aff233e5f7a707682d4d00708ec1d1a08494f15` (2401
inodes, 265864 B). Builder: `artifacts/R41W2C1Run/gen-synth-carrier.py`.

```
C1_KEEP_ENVELOPE=1 bash tools/round-41/c1-run.sh after \
    $S/synth-carrier.sqsh $S/out-synth $S/harness-scratch
exit 126; stderr:
  tools/round-41/c1-run.sh: line 547: /home/vgpnk/.local/bin/jq: Argument list too long
ls out-synth -> after.json only (859130 B); no run.json
```

This is the same failure line and state as V4. `l1/c1-run-V4.log` and
`corpus/evidence/round-41/c1/V4/run-harness-failure.log` are identical 86-byte
files with exactly that line.

Threshold proof (jq 1.8.2 at `/home/vgpnk/.local/bin/jq`):

```
single arg 131071 chars -> exit 0
single arg 131072 chars -> exit 126, "Argument list too long (os error 7)"
2000 small args -> exit 0        (total argv size is not the limit)
```

## 3. after.json is the complete REA `data` object

Write path: `jq -c '.data' envelope.json > scratch/after.json`, then `mv` into
the outdir (lines 516, 541) — both before the failing line. Proofs:

1. **Same-run identity**: an instrumented scratch copy (not the repo file) copied
   the envelope out right after the `mv`; `after.json` sha256
   `96cb2e357e978634fddb38be52d5c524d66c2d1b48560213fba4b15ae01670a8` ==
   `jq -c '.data' env-before-failure.json` sha256. After.json is exactly the
   envelope's `data` member.
2. **Independent rerun**: my own REA CLI run (rea-agents@6.5.0, same flags) on
   the same bytes projects equal under the counter's plus-extractor profile
   (files/chunks/gaps/unpublished/diagnostics + subject/derivations/engine/
   published_bytes/coverage) — `project-compare.py` in artifacts prints
   `equal: True`, 640/1601/1600, subject = carrier sha.
3. **V4 schema identity**: the committed V4 after.json has exactly the same
   16 top-level keys and the same `normalized_result` key set as a fresh REA
   6.5.0 data object; `files 6349`, `gaps 612`, `unpublished 611`,
   `diagnostics 4` (MaliciousSymlinkRemoved), single `squashfs_v4_be` chunk with
   `extraction_failed false`, `subject == carrier pin ce27ebca…087f`, `operation
   extract_firmware`, `provider unblob`, `parameters.max_depth 1 /
   max_output_files 10000`, output_directory under `/kaidoku-r41/`. The score
   receipt `l1/scores/c1-at-e9a24d07.json` independently records V4
   `receipt_present true`, `oracle_hits 6349/6349`, `evidence_id_ok true`,
   `projection_ok true` (`projection_diff []`), `matched true`.

## 4. Fix (minimal, in artifacts)

Replace both argv-passed big values with files read via `--slurpfile`
(`$summary[0]` / `$receipt[0]`, the canonical jq pattern). Summary and receipt
are the only inputs that scale with receipt size; every other `--argjson` is
bounded (argv, superblock, env digest, stderr_head ≤ 8000 B …). Full unified
diff: `artifacts/R41W2C1Run/fix.diff` (4 hunks, 58 lines). Changes:

1. `summary=$(jq -c '…')` → `jq -c '…' > $scratch/summary.json`; add the
   `else` branch writing `null` when there is no data; pre-seed
   `$scratch/receipt.json` with `null`.
2. `receipt=$(jq -n … --argjson summary "$summary" …)` → `jq -n …
   --slurpfile summary "$scratch/summary.json" … '{…} + $summary[0]' >
   $scratch/receipt.json`.
3. Final run.json jq: `--argjson receipt "$receipt" --argjson summary "$summary"`
   → `--slurpfile receipt "$scratch/receipt.json" --slurpfile summary
   "$scratch/summary.json"`; filter uses `$receipt[0]` / `$summary[0]`.

Validation (synthetic carrier, same env):

```
bash c1-run-fixed.sh after $S/synth-carrier.sqsh $S/out-fixed2 $S/harness-fixed2
exit 0; run.json written; receipt_written true; data_extracted true
run.json: summary_files 640, receipt_sha d32b9c65… == after.json sha == envelope-data sha
```

V4-scale check with the real V4 summary (146561 B): the receipt-style jq via
`--slurpfile` completes and yields `files 6349, gaps 612, unpublished 611`.

## 5. Does any counter clause depend on run.json? No.

- `grep run\.json tools/round-41/c1-counter.py c1-extra.py` → no matches; a
  lane-wide grep finds only writers (c1-run.sh itself) and unrelated older-round
  tools. `plans/round-41-claims.md` references only `oracle-run.json`; the
  predicate P41-C1 is defined over the after-receipt (`after.json`).
- The counter's receipt bindings all read after.json/oracle/nonregular/docs;
  `run_provenance_ok` reads `parameters.output_directory` **from after.json**.
  c1-extra.py reads no receipts.
- The e9a24d07 score receipt shows all V4 bindings true with exit 0 — the score
  was computed with V4's run.json missing.

## 6. Separate finding (calibration): intermittent unblob ENOENT flake

While validating, two of thirteen REA runs on the synthetic carrier failed with
`execution_failure` / `ENOENT: no such file or directory, readlink
'<stage>/extracted/firmware.bin_extract/dN0/lNN'` (a different directory each
time); the other eleven (fresh outdirs) succeeded. A pre-existing outdir causes
a separate, deterministic refusal (`Extraction output root already exists`).
The ENOENT failure is REA/unblob-environment nondeterminism on many-symlink
trees (comparable to the iteration-order symlink behavior documented in
`w1/R41C1DevCore.md` §6) — not a harness defect and unrelated to the E2BIG
issue. It did not affect the V4 counter-time rerun (`projection_ok true`), but
any future rerun of a large carrier should treat a one-off `ENOENT`/`retryable:
false` execution failure as retryable-in-practice.

## 7. Residual risk / verification gaps

- I did not rerun the full `c1-counter.py` myself (needs the vendor cache
  rebuild); I cite the committed score receipt at e9a24d07 and the counter's
  code path instead. The synthetic run demonstrates the harness behavior, not
  the vendor carrier itself.
- V4 after.json completeness vs a fresh V4 rerun is asserted via schema identity
  + the counter's recorded `projection_ok true`; I did not rerun REA on V4
  bytes (vendor download not needed for this seat's conclusion).
- The flake rate (2/13) is a small sample; only its existence and non-causal
  relation to the harness are claimed.

## 8. Artifacts

- `artifacts/R41W2C1Run/fix.diff` — minimal fix patch (original → fixed).
- `artifacts/R41W2C1Run/gen-synth-carrier.py` — synthetic carrier builder.
- `artifacts/R41W2C1Run/project-compare.py` — projection comparison tool.
- `artifacts/R41W2C1Run/evidence.md` — full command/exit/digest transcript.
