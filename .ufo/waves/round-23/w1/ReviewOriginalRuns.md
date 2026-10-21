# R22 identify run/envelope review

## Findings

- **No `stdout`/envelope byte mismatch observed for either retained identify record.** I read the Round-22 records and performed only a local comparison of each JSON-decoded `run.stdout` string against the paired envelope file bytes (`jq -j '.stdout' RUN.json | cmp -s - ENVELOPE.json`); both `cmp` exits were **0**. The hashes of each decoded stdout and its envelope were identical:
  - Positive classification: `.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.run.json` → `identify-flutter-build-saber.envelope.json`; SHA-256 `143af76e3969c6a79f591115a55b0fd581dfab13a10db5c72fda0b8306f9904b`. The retained argv is `npx -y rea-agents@6.5.0 identify-flutter-build /tmp/kd22probe/saber.apk --format json --full-output`; exit `0`, stderr empty, target SHA-256 `de4813f95bdd6ae54adc5a6142be0762c177a782caaed6ed51dae482f6acb720`, envelope `ok:true`, `flutter_detected:true` (coverage `partial`). The run record labels its producer “KaidokuR22R L1 recovery, not inherited W1” (`...identify-flutter-build-saber.run.json:15`).
  - Negative classification: `.ufo/waves/round-22/evidence/c1/identify-godot-run.json` → `identify-godot.envelope.json`; SHA-256 `1ea324b258f06d3f45274eb60f1225f380dcf6ae5adc15e257933c57ea045b0a`. Retained argv is `npx -y rea-agents@6.5.0 identify-flutter-build /home/vgpnk/.local/share/godot/export_templates/4.7.2.stable/android_release.apk --format json --full-output`; exit `0`, stderr empty, target SHA-256 `6d1bb2cfa126a1b1c87e064a35b3cbd181bef0ec784dec1efd1d64dffa8be6cb`, envelope `ok:true`, `flutter_detected:false` (coverage `complete`). This is a successful negative identification, **not** a typed refusal or command failure. The R22 claim explicitly excludes typed refusals from its count (`.ufo/waves/round-22/claims.json:13-22`).

- **The saved R22 provenance result includes both records and marks both passing.** `.ufo/waves/round-22/verify/final/provenance.json:2,5-11,157-168` pins `source_rev` `e9db7e2d5798ff3d5f1ba5ccd76bb86f2cc5c1bb`; the positive and negative pair rows each say `stdout_equal:true` and `pass:true`, and `historical_copy_equal_data:true`. `verify.py:157` explicitly adds the non-`.run.json`-suffix negative run/envelope pair; lines 161-180 compare retained run stdout to raw envelope text, command metadata to the argv verb, exit to envelope `ok`, and the copied negative evidence object to `envelope.data`. The stored verifier invocation in `verify/final-producer.json:2-17` records exit `0`. These are recorded results, not a verifier rerun in this review.

- **Low-severity verification limitation:** the current `verify.py` pass predicate (`.ufo/waves/round-22/verify.py:164-172`) does not bind the argv target operand to `data.parameters.path` / `subject.local_path`, compare `subject.digest.sha256` with `normalized_result.target.sha256`, or require/check stderr. Thus its `pass:true` is a local run/envelope consistency result, not by itself proof that the recorded invocation operated on the envelope's subject. In the two records inspected here, the argv target path and both envelope paths agree, and the subject and normalized target SHA-256 values agree; this is an observed property of these artifacts, not an assertion made by that predicate. No mismatch was found.

## Exact offline consistency-check plan

No REA producer needs to be invoked again. Use the pinned revision from `provenance.json` and its four `git show REV:path` blobs (two run records and two envelopes), not a newly produced output. For each pair:

1. Parse the run record, extract its `stdout` without adding a newline (`jq -j '.stdout'`), then byte-compare it to the original envelope blob (`cmp -s`). Do not parse and reserialize the envelope for this comparison.
2. Parse the stdout/envelope and independently check: `run.exit` corresponds to top-level `ok`; `run.stderr` is retained; argv's command and target operand match envelope `meta.command`, `data.operation`, `data.parameters.path`, and `subject.local_path`; `subject.digest.sha256` equals `normalized_result.target.sha256`; and the result's `flutter_detected` value describes positive versus negative identification. Record each pair's comparison exit and SHA-256s.
3. Keep the copied-data check separate: compare `identify-godot.evidence.json` structurally to `identify-godot.envelope.json`'s `data`. Do not treat that copy check as proof of producer identity.

Steps 1 and the current observed cross-field path/digest facts were checked read-only here. The existing verifier records steps 1 and 3; its source does not implement all of step 2's target-binding assertions.

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/ReviewOriginalRuns.md` — SHA-256: recorded in the final handoff (kept external to avoid a self-referential digest).

## Installs

None.

## Open risks

- Neither identify run record contains an `env_overrides` field (`provenance.json` reports `env_overrides_retained:false` for both). This is missing evidence, not evidence that no overrides were active. The positive run also explicitly identifies itself as an L1 recovery, not an inherited W1 run; the negative run has no producer field. Do not attribute either record to an earlier producer beyond what is recorded.
- The equality check establishes byte consistency between retained local files only. It does not authenticate the producer, establish the execution environment, or independently re-hash the original APKs in this review. No REA command, APK, device, or target was run/opened.
- No `lsp` device is mounted in this session (`read xd://lsp` returned “No such tool”); no LSP status/references/definition/diagnostics were available. `verify.py` source claims above are literal-path/line inspection, not LSP semantic proof.