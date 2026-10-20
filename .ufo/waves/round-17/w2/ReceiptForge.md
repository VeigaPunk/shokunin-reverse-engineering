# ReceiptForge — wave-2 falsification of receipt-validate.py

Target: `.ufo/waves/round-17/tools/receipt-validate.py` at lane HEAD `95e34db`
(hardened mid-wave: `classify` now accepts dict `steps`; `check_binding` added).
Source receipt: `runs/pro-notesmd-cli/receipt.json` (regenerated 11:30 by a
concurrent peer; session `rea-ghidra-eK7Drd`, carrier `notesmd-cli` sha
`412dc532…800802d`).

Harness: `w2/receipt-forge.py` — copies `runs/pro-notesmd-cli` to a fresh
`/tmp/kr17-forge-*` dir per forgery, rewrites receipt paths to the copy,
applies one of 28 mutations, runs
`python3 -I -B tools/receipt-validate.py <forged>/receipt.json`. Retained
workroot: `/tmp/kr17-forge-g3er8q8m`; full JSON: `/tmp/kr17-forge-final.json`.
Reproduce: `python3 -I -B .ufo/waves/round-17/w2/receipt-forge.py [--keep]`.

## Verdict table (exit code of receipt-validate.py)

| forgery | exit | catching findings |
|---|---|---|
| control (pristine copy) | 0 | — (real receipt validates green) |
| shape-normalize (steps dict→list) | 0 | — |
| edit-ghidra-log (bytes only) | 1 | sha256_mismatch, size_mismatch |
| edit-ghidra-log-rehash (bytes+digest updated) | **0** | none |
| edit-log-keep-binding (Go version→1.99.0 + forged snapshot line, digests updated) | **0** | none |
| swap-log-other-run (pro-op log + digests updated) | 1 | binding_mismatch |
| swap-log-keep-meta (pro-op log, digests stale) | 1 | binding_mismatch, sha256_mismatch, size_mismatch |
| synthesize-bound-session (self-authored 3-line log + fake session dir) | **0** | none |
| synthesize-carrier-lie (carrier→/usr/bin/shfmt + fake session naming shfmt sha) | **0** | none |
| pins-pre-forge-nofix (pins_pre carrier sha=0..0) | 1 | pins_compare_mismatch |
| pins-pre-forge-consistent (+ pins_compare forged to equal:false/changed:[carrier]) | **0** | none |
| normalize+pins-forge | **0** | none |
| delete-bound-sessions (key removed) | **0** | none |
| bound-to-unbound (session moved to unbound_sessions) | **0** | none |
| normalize+delete-bound | **0** | none |
| delete-retained-logs (key + logs/ gone) | 1 | missing_field, missing_file, binding_mismatch |
| normalize+delete-retained | 1 | missing_field, missing_file, binding_mismatch |
| normalize+empty-retained (retained_logs:[] top+step, logs/ gone) | 1 | binding_mismatch |
| carrier-sha-lie (sha256_post=f..f) | 1 | binding_mismatch, sha256_mismatch |
| carrier-path-swap (path+sha→/usr/bin/shfmt, argv untouched) | 1 | binding_mismatch |
| normalize+carrier-swap | 1 | binding_mismatch |
| evidence-id-receipt (analyze.evidence_id→pro-op's) | **0** | none |
| evidence-id-file (analyze.json edited + stdout_sha256 updated) | **0** | none |
| stdout-swap (analyze.json←pro-op + sha updated) | **0** | none |
| step-exit-flip (analyze exit 0→1, argv[3] mutated) | **0** | none |
| binding-flags-flip (recorded binding{logfile_ok,target_ok}→false) | **0** | none |
| timestamps-scramble (ended_at_utc, pins_post.taken_at_utc before start) | **0** | none |
| normalize+log-forge (normalized + rehashed forged log) | **0** | none |

**15 of 26 actual forgeries exit 0** (control and shape-normalize are
the two non-forgery rows; 28 mutations total). A forgeable receipt passes
whenever the forger updates every recorded digest consistently and preserves
(or fabricates) the two binding substrings.

## Findings

### F1 — `pins_pre` of any doubly-pinned path is never checked against live bytes
`verify_pin_entries` skips every `pins_pre` entry whose path also appears in
`pins_post` (`receipt-validate.py:234` — "post is authoritative"). The real
receipt pins the identical set in both snapshots, so *every* `pins_pre`
entry is unverified. Forging `pins_pre` carrier sha256+size and rewriting the
recorded `pins_compare` to `{equal:false, changed:[carrier]}` yields a green
receipt that fabricates a mid-run carrier mutation (`pins-pre-forge-consistent`,
exit 0). Without the compare fix the forger is caught only by internal
consistency (`pins_compare_mismatch`), never by live bytes. A forged receipt
can also claim "stable during run" for a carrier that *did* change — nothing
recomputes pins_pre→post against the true pre-state (unknowable), so the
limit is inherent, but the report should state that pins_pre is
receipt-internal evidence only.

### F2 — deleting `bound_sessions` disables the entire binding check
`check_binding` returns silently when the key is absent
(`receipt-validate.py:124-125`) and `bound_sessions` is not in
`CARRIER_REQUIRED` (`:59-63`). `delete-bound-sessions`,
`normalize+delete-bound`, and `bound-to-unbound` (real session moved to
`unbound_sessions`, which is never inspected) all exit 0 — every binding
forgery below then passes unchecked. Note the asymmetry: `bound_sessions:[]`
fails with `no_bound_session` (`:131`) while *deleting* the key passes.
Absence is safer than emptiness — backwards.

`receipt-validate.py:142-143` requires only that the retained ghidra.log
contain `Using log file: <bound_dir>/ghidra.log` and
`IMPORTING: file://<bound_dir>/target-<carrier sha[:12]>.bin`. Consequences:

- Any in-place edit preserving those substrings passes:
  `edit-ghidra-log-rehash` (forged ERROR line appended) and
  `edit-log-keep-binding` (`Go version 1.25.8`→`1.99.0`, forged
  `Using Go API snapshot for go1.99` appended) — both exit 0. The log
  *content* the predictions/compare chain consumes is unbound.
- A wholly self-authored 3-line log satisfies it:
  `synthesize-bound-session` fabricates `/tmp/kr17-forged-aaaaaa/rea-ghidra-ZZfake`,
  rewrites every recorded path/digest, deletes the real session log →
  **exit 0**. The receipt "proves" a Ghidra session that never existed.
- `synthesize-carrier-lie` (exit 0) combines F3+F4: carrier swapped to
  `/usr/bin/shfmt`, fake session log names `target-<shfmt sha12>.bin` —
  a green receipt for an analyze of shfmt that never ran.

### F4 — `carrier.path` is never cross-checked against pins entries or step argv
`carrier-path-swap` is caught only indirectly (the fake sha broke the
log substring match → `binding_mismatch`), not because path≠argv target or
path∉pins entries. `synthesize-carrier-lie` shows completing the forgery is
trivial: with a fake log, carrier↔argv↔pins disagreement validates green.

### F5 — `evidence_id` and stdout provenance are unbound
`steps.analyze.evidence_id` replaced with the donor run's evidence id → exit 0.
Editing `analyze.json`'s evidence_id + updating `stdout_sha256` → exit 0:
stdout bytes are digested but never parsed, so the recorded `evidence_id`
field is never re-derived from or compared to them. `stdout-swap` (donor's
analyze.json + updated sha) → exit 0: receipt and stdout describe different
runs and pass anyway. This is the prediction-chain gap: `compare.py` consumes
`observation.json` derived from the log — with F3 the whole
prediction/observation/evidence chain can be forged to consistency.

### F6 — step semantics, timestamps, recorded binding flags are never verified
`step-exit-flip` (analyze `exit` 0→1, `argv[3]` mutated) → exit 0.
`timestamps-scramble` (`ended_at_utc` and `pins_post.taken_at_utc` moved
before `started_at_utc`) → exit 0 — `rerun_pins_compare` verifies only
`{equal, changed, missing, errors}`, explicitly not timestamps.
`binding-flags-flip` (recorded `{logfile_ok:false,target_ok:false}` while
derived binding is fine) → exit 0: recorded flags are superseded by
re-derivation, so a false "binding failed" claim also validates.

### F0 (historical, already fixed by L1) — shape misclassification
At the pre-hardening revision (`da64646`'s validator), `classify` required
`steps` to be a list (`:98` old); `carrier-run.py` emits a dict. Every real
round-17 receipt — including the pristine control — failed
`unrecognized_shape` while 306 deeper checks silently ran green. Fixed in
`95e34db` (`classify` `:96-104`, `_iter_steps` `:110-113`); noted here for
provenance since the fix comment already cites this seat.

## What does get caught
Raw byte tampering with stale digests (`sha256_mismatch`, `size_mismatch`);
inconsistent pins_compare (`pins_compare_mismatch`); removing `retained_logs`
(`missing_field` — it is required — plus `missing_file` from per-step copies
and `binding_mismatch`); naive carrier sha lies; naive cross-run log swaps.

## Net assessment
The validator checks (a) internal digest consistency of recorded (path, sha,
size) commitments and (b) a two-substring log self-reference gated on a
removable key. Everything else — session existence, log content beyond two
lines, evidence ids, argv, exits, timestamps, pins_pre history, carrier↔argv
binding — is receipt-internal and forgeable. Hardening directions (advisory,
L1's call): require `bound_sessions` in CARRIER_REQUIRED and reject empty;
hash-pin the two binding lines' surrounding context or require the retained
log digest to also satisfy log-extract expectations; parse `analyze.json`
and re-derive `evidence_id`; require `carrier.path` ∈ pins entries and equal
to the trailing non-flag argv token; sanity-check timestamp ordering.

## Method notes / calibration
- No installs; stdlib only; `python3 -I -B`; scratch under `/tmp` only.
- Observation vs inference: every exit code/finding above is an observed run
  of the current validator (`/tmp/kr17-forge-final.json`); per-forgery
  descriptions of intent are mine.
- Caveat: `runs/` was being regenerated by peers during this run (mtimes
  11:30–11:34); results were taken against the regenerated
  `pro-notesmd-cli` receipt. The validator (`tools/receipt-validate.py`) was
  committed and unmodified in the working tree throughout.
