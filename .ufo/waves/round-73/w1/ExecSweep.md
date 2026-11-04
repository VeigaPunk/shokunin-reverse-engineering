# ExecSweep — frozen declaration command sweep

Axes: frozen-command fidelity; receipt completeness; environment-value minimization.

Ran the five assigned commands once, concurrently, from the lane with TMPDIR and --work explicitly bound to the exclusive scratch directory. No source edits, extra test commands, installs, or git writes. The base-tool probe changes only --tool to tools/round-72/packed-elf.py; its --rev and --receipt remain the frozen declaration arguments.

| Command | rc | Receipt outcome |
|---|---:|---|
| Declaration probe | 1 | 11/12; failed A2_threaded_path; A12 true |
| Declaration audit | 1 | mismatch_count 6 |
| Declaration r73 mutations | 1 | survivor_count 0; git_reader_env_dropped killed_wrong_case |
| Base-tool probe | 1 | 8/12; failed A2_threaded_path, A10_run_binding, A11_checker_env, A12_kernel_witness |
| Base audit | 1 | mismatch_count 6 |

## Exact requested observations

Both audit mismatch lists: `D1_c2_evidence_hash`, `D2_c2_pin_conjunct`, `D3_record_gate_disclosures`, `D4_c3_exit_code`, `D5_provenance_trio_open`, `D6_nudge_rationale`.

Mutation verdicts:
- `git_reader_env_dropped`: `killed_wrong_case`; failed `[checker-readelf-allowlisted-exec]`; expected `git-reader-allowlisted-exec`.
- `readelf_env_dropped`: `killed`; failed `[checker-readelf-allowlisted-exec]`.
- `implicit_capsule_dropped`: `killed`; failed `[implicit-capsule-polluted-raw-log]`.

Declaration A12: `ok=true`, `genuine_ok=true`, `lie_clean=true`, `forged_detected=true`. Genuine git/readelf kernel samples have keys `[HOME, LANG, PATH, TMPDIR]` and `canary_present=false`. Forged git/readelf child samples have those same four keys, `keys_exact=true`, `canary_present=false`; forged kernel samples include additional keys and `canary_present=true`.

Base-tool A12: `ok=false`, `genuine_ok=false`, `lie_clean=true`, `forged_detected=true`; genuine checker rc 1. Genuine kernel samples still have the four keys and canary absent; forged kernel samples have additional keys and canary present.

A2 retained observation: all eight recorded argv0s are `/fast/scratch/hyaku/kaidoku-r73/l1/upx-r73`, while `expect_upx` is `/fast/scratch/hyaku/kaidoku-r73/ExecSweep/upx`; `defects=[]`, `missing=[]`, `module_default=/usr/bin/upx`.

## Receipt heads

Full retained outcomes, A12 observations, rc values, and 16-line receipt heads are also in `ExecSweep/command-results.json`.

### declaration-probe (rc 1)
Receipt: `.ufo/waves/round-73/w1/ExecSweep/declaration-probe.json`
```json
{
 "arms": [
  {
   "id": "A1_hash_before_exec",
   "observed": {
    "env_keys": [
     "HOME",
     "LANG",
     "PATH"
    ],
    "impostor_executed": false,
    "rc": 2,
    "stderr_tail": "{\"claim\": \"R71\", \"schema\": \"kaidoku-r71-packed-elf-v1\", \"unevaluable\": \"packer_mismatch: sha256 ae40e0f57c0b08bee31955d48195d9854c7c7669fe0c351292dccdf1d0d5ccad != pin cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969\"}",
    "stdout": "",
    "traceback": false,
    "unevaluable": "packer_mismatch: sha256 ae40e0f57c0b08bee31955d48195d9854c7c7669fe0c351292dccdf1d0d5ccad != pin cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
```

### declaration-audit (rc 1)
Receipt: `.ufo/waves/round-73/w1/ExecSweep/declaration-audit.json`
```json
{
 "atoms": [
  {
   "detail": "the record's C2 target sha re-derives from the receipt's own rev, or a round-73 correction names both values",
   "evidence": {
    "blob_matches": true,
    "correction_block": false,
    "correction_names_wrong": false,
    "receipt_rev": "e67f3a1b1f79bcd5ce56dd4f64edb4ed18f903ff",
    "receipt_target_sha256": "602b305d79222222c1f17c51cc10365246ecfc184cdd4afd8f773a0f5fd5f0e2",
    "stated_tokens": [
     "39a2193e"
    ],
    "wrong_tokens": [
     "39a2193e"
    ]
```

### declaration-mutations (rc 1)
Receipt: `.ufo/waves/round-73/w1/ExecSweep/declaration-mutations.json`
```json
{
 "expected_survivors": 0,
 "instrument": "tools/round-73/packed-elf.py",
 "killed": [
  "readelf_env_dropped",
  "implicit_capsule_dropped"
 ],
 "killed_wrong_case": [
  "git_reader_env_dropped"
 ],
 "mutants": [
  {
   "applied": true,
   "cases": 38,
   "expect_case": "git-reader-allowlisted-exec",
   "failed": [
```

### base-tool-probe (rc 1)
Receipt: `.ufo/waves/round-73/w1/ExecSweep/base-tool-probe.json`
```json
{
 "arms": [
  {
   "id": "A1_hash_before_exec",
   "observed": {
    "env_keys": [
     "HOME",
     "LANG",
     "PATH"
    ],
    "impostor_executed": false,
    "rc": 2,
    "stderr_tail": "{\"claim\": \"R71\", \"schema\": \"kaidoku-r71-packed-elf-v1\", \"unevaluable\": \"packer_mismatch: sha256 96042ff843ec666559198762af93a3cdbbf9ea6f28a4296f4629a800ef3d66c1 != pin cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969\"}",
    "stdout": "",
    "traceback": false,
    "unevaluable": "packer_mismatch: sha256 96042ff843ec666559198762af93a3cdbbf9ea6f28a4296f4629a800ef3d66c1 != pin cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969"
```

### base-audit (rc 1)
Receipt: `.ufo/waves/round-73/w1/ExecSweep/base-audit.json`
```json
{
 "atoms": [
  {
   "detail": "the record's C2 target sha re-derives from the receipt's own rev, or a round-73 correction names both values",
   "evidence": {
    "blob_matches": true,
    "correction_block": false,
    "correction_names_wrong": false,
    "receipt_rev": "e67f3a1b1f79bcd5ce56dd4f64edb4ed18f903ff",
    "receipt_target_sha256": "602b305d79222222c1f17c51cc10365246ecfc184cdd4afd8f773a0f5fd5f0e2",
    "stated_tokens": [
     "39a2193e"
    ],
    "wrong_tokens": [
     "39a2193e"
    ]
```

## Retention and risks

- Five receipts and command-results.json retained under the exclusive ExecSweep directory. Probe receipts are shape-only derivatives: environment `values`, `home`, and `tmpdir` fields (including embedded JSON) are redacted. The frozen probe initially emitted allowlisted values directly to its JSON output; those values are not retained. No raw full-environment dump or credential-value query was requested.
- Declaration results do not equal the requested green expectations; no result was repaired, rerun, or reinterpreted. Zero mutation survivors alone is not a green battery: its rc is 1 and one mutant is killed_wrong_case.
- The base-tool probe uses the provided round-73 route receipt unchanged; no substitute route was generated.
- Scratch copy matched pinned UPX sha256 `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969`; scratch removed in finally after all five commands completed. No tools installed or upgraded.
- LSP unavailable in this seat tool inventory; no symbol changes or source refactors performed.

## Self-evaluation

Accuracy 4: raw exit codes and receipt observations retained; environment-value redaction means probe files are not byte-identical originals. Completeness 5: all five requested commands, receipt heads, mismatch lists, mutant cases and A12 fields supplied. Clarity 4: receipt heads are intentionally truncated to 16 lines; full receipts are linked. Actionability 5: exact failed-arm IDs and wrong-case evidence retained without changing instruments. Conciseness 4: duplicate heads retained because explicitly requested. Overall 4.4. Improvement: frozen instruments should emit shape-only receipts directly; this sweep does not modify them. Self-check: all observed failures remain visible.

Report: /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-73/w1/ExecSweep/ExecSweep.md
