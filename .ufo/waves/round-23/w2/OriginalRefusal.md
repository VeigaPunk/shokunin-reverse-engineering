# OriginalRefusal: R23-C1 source review of the decode-invalid-decoder pair

Seat: KaidokuR23.OriginalRefusal (leaf, source review only; author-side, not independent admission).
Candidate: 2838351450ff1ee4baa620c962a1153450d53311 ("round-23: retain measured four-of-six coverage and refusal controls").
Baseline: aa1450b82f9ede35aada63efe8a34e01c6e02f72.

Pair under review (committed candidate bytes):
- `.ufo/waves/round-23/evidence/c1/decode-invalid-decoder.envelope.json`: blob d1dacc54712722843e1019c358989f4b47089698; sha256 04697e72e9cabc9dae1385731ea3f2becf8a4bb94dc2334f067180b3b1008292; 991 bytes; 1 line.
- `.ufo/waves/round-23/evidence/c1/decode-invalid-decoder.run.json`: blob 7b6ee4bb6786196140c1b14b273737356634a184; sha256 518181aa69dfc844601dbec60f7b8794bbde769d27a075e428398a214e45262c; 1733 bytes; 25 lines.

Method: `git show 2838351…:PATH`, `git rev-parse`, `git ls-tree`, `git log` on committed objects, plus in-memory JSON parsing and sha256 of those bytes. No producer rerun. `count-c1.py` and `describe-signals.py` were read via `git show`, not executed. No tests, builds, or worktree reads used as evidence.

## Verdict

- **Exclusion holds.** The pair is `ok:false`, `error.code = execution_failure`, `retryable:false`, `provider_id = sigrok-recording`, process exit 1 (run.json:21), and provider `diagnostics.exit_code = 1`. It has no `data`, `subject`, `evidence_id`, or `tool` key, and no 64-hex token. It cannot bind to a T1 verb. It is not absent-provider and not `invalid_request`.
- **Several claims attributed to this pair are not retained for it:** `environment` (KD:2), launcher `tool.sha256` (KD:101–102), and input `subject` `uart-hi.bin` (CoverageMap.md:72).
- **No field of this pair has an independent binding.** The run file has no digest anywhere. The input carrier is never checked by the verifier. The runtime pins were captured four minutes after the run from worktree paths. The runtime is gitignored and absent from the commit. No Python interpreter is pinned.
- **Source linkage is directory-level only.** The S060 row (SOURCES.md:66) does not enumerate the pair.

## Findings

Severity is by impact on what the knowledge entry asserts. None changes the count.

### F1 [overclaim, high] "environment" is not retained
- Claim: `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md:2`: "exact producing argv/environment/stdout/stderr/exit retained in adjacent .run.json files".
- Observed: run.json keys are `argv`, `cwd`, `env_overrides`, `exit`, `stdout`, `stderr`, `captured_at`. `env_overrides` (run.json:18–20) holds only `REA_SIGROK_COMMAND`. Nothing records the inherited environment, and `tool-runtime-pins.json` lists file hashes only.
- The producer's stderr shows environment dependence: "Consider setting $PYTHONHOME" (envelope `error.details.diagnostics.stderr`).
- Partly derivable: `.ufo/waves/round-23/tools/sigrok-cli.sh` (blob 3a806cbb…, sha256 50fe4359…) exports `LD_LIBRARY_PATH`, `LD_PRELOAD`, `PYTHONPATH`, and `SIGROKDECODE_DIR`. That needs the worktree wrapper at 14:38:59 to equal the committed bytes, which nothing in the pair records.

### F2 [overclaim, high] launcher `tool.sha256` and the L4 field set do not apply to this pair
- Claim: KD:101–102: "The original envelopes' `tool.sha256` identifies the launcher, SHA256 50fe4359…". W1 `ConnectSourceChain.md:31` (L4) lists "ev id, annotations text, window, diagnostics" for the signal envelopes.
- Observed: the envelope's top-level keys are `ok`, `error`, `meta` only. It has no `data`, `tool`, `subject`, `evidence_id`, `hardware_acquisition`, or `resource_limiter`. Neither pair file contains 50fe4359… or any 64-hex token. The four successful signal envelopes (inventory, uart-help, decode-uart-hi, decode-official-uart) carry `data.normalized_result.tool.sha256`; this one does not.
- Launcher identity for this pair is argv text only: `npx -y rea-agents@6.5.0` (run.json:3–5). The npm package bytes are neither retained nor bound.

### F3 [unbound, high] input carrier is not retained as `subject`; it is a path string only
- Claim: `.ufo/waves/round-23/w1/CoverageMap.md:72` lists this pair's subject as `uart-hi.bin`.
- Observed: the envelope has no `subject`. The only trace is argv[4] (run.json:2–16): `…/evidence/c1/uart-hi.bin`.
- `.ufo/waves/round-23/tools/describe-signals.py:57` runs the carrier check (lines 58–62: `carrier_sha256`, `subject_digest_matches_carrier`, `argv_target_matches_subject`) only when `data.get('subject')` is truthy. For this record it never runs, and no discrepancy field is emitted. The verify record row for this name (`.ufo/waves/round-23/verify/initial/signal-records.json`, blob d6750da…) has `subject: null` and neither carrier key.
- The committed `uart-hi.bin` has sha256 4a2e729f… (matches KD:39), so the path resolves to committed bytes. Nothing in this run binds its input to them. That digest is bound only in other records: the decode-uart-hi envelope's `data.subject.digest.sha256` and `generate-uart.run.json`.

### F4 [unbound] `run.json` has no digest anywhere
- sha256 518181aa… of the run file appears in none of the 146 in-scope committed files (round-23 non-vendored tree, `corpus/SOURCES.md`, `corpus/knowledge/2026-10-21*`, `corpus/lessons/round-23*`).
- Its only bindings are git blob 7b6ee4bb… (commit integrity) and `stdout` equal to the envelope bytes (`describe-signals.py:43`; I re-observed equality). That is same-record consistency, not independent corroboration.
- `captured_at` (run.json:24, 2026-10-21T14:38:59.564971+00:00) is unbound.

### F5 [unbound, later instant] "pinned" runtime and interpreter identity
- `.ufo/waves/round-23/tool-runtime-pins.json` (sha256 02ef8379…, 2833 bytes): `captured_at` 2026-10-21T14:42:59.166503+00:00, which is 3 min 59.6 s after the run's `captured_at` (run.json:24). Producer: "Python pathlib.read_bytes/hashlib.sha256 on listed paths", over worktree absolute paths (`pins[].path`), not commit objects.
- The eight pins are: `sigrok-cli.sh` (50fe4359…, equal to the committed blob), sigrok-cli ELF (10fed05a…), `libsigrok.so.4`, `libsigrokdecode.so.4`, uart `pd.py`, and host `libgmodule`, `libglib`, `libgio`. No Python interpreter, libpython, or sigrok Python bindings are pinned, though the stderr shows Python prefix resolution failing.
- `.ufo/waves/round-23/.gitignore:1` is `/runtime/`. The sigrok runtime is not in the commit: no `squashfs` path exists in the 19,098-file candidate tree.
- Result: wrapper identity matches at 14:42:59 (observed). Identity at 14:38:59 is an inference that the bytes did not change in four minutes [INFERENCE]. Runtime and interpreter identity at the producing instant are unknown.

### F6 [linkage] the S060 row does not enumerate the pair
- `corpus/SOURCES.md:66` (S060) lists `inventory.envelope.json`, `decode-uart-hi.envelope.json`, and `decode-official-uart.envelope.json` only. Its anchor, "Original ok/meta.command/data records", describes success records. This pair has no `data`.
- KD line 1 cites "S060 original REA6.5.0 envelopes in .ufo/waves/round-23/evidence/c1/", which is directory-level. S060's used-by includes the KD (observed), so entry-level linkage exists. Row-level artifact linkage for this pair does not.

### F7 [attribution] "exit1" is two separate fields
- KD:84–85: "an actual `execution_failure`, exit1, in `…decode-invalid-decoder.envelope.json`". In the envelope, the 1 is `error.details.diagnostics.exit_code`, the provider's exit. The REA process exit 1 exists only at run.json:21. Both are 1 (no contradiction), but each should be cited by its location.

### F8 [attribution] stderr is not in run.json's `stderr` field
- KD:2 says stderr is retained in `.run.json`. W1 `ConnectSignalFirmware.md:70` attributes the ImportError row to the run file.
- Observed: run.json:23 is `"stderr": ""`. The sigrok stderr is at envelope `error.details.diagnostics.stderr`, and appears only as escaped text inside run.json:22 (`stdout`). It is retained, but the field is the envelope's.

### F9 [mechanism] exclusion is enforced by the id gate, not by refusal classification
- The pair has zero 64-hex tokens and zero `ev_` tokens. `count-c1.py:111` builds `ids` from the KD text. `count-c1.py:122–123` call `bind_new` only when `eid in blob`. For this pair that gate is never satisfied, so the refusal guard at `count-c1.py:51` is never reached for it.
- The outcome is correct. The mechanism matters: a refusal envelope that carried a KD-listed hash would be caught only by line 51. W1 `CriticVacuity.md:81` ("the counter correctly blocks it") is right on outcome and inexact on mechanism.
- W1 `CounterRefusals.md:231` (N9) holds. "Never reaches bind_cli (:158 skips it)": line 158 is in the R22 legacy counter's measure loop (`.ufo/waves/round-22/tools/count-c1.py:157–158`), with the same id gate. "Invisible in R23 output" also holds: the R23 result dict (`count-c1.py:128–133`) has no refusal or uncounted field.

### F10 [timing, unbound] the predicted refusal is not bound to the run
- `.ufo/waves/round-23/predictions.json` (sha256 2ec069ad63616f95076a993e89198100438d30f806d167152d211d4d7efc4817) contains `"refusal": {"expected_exit": 1, "decoder": "round23_nonexistent_decoder"}`. Observed: run.json:21 exit 1 matches.
- No committed tool reads this file. The only round-23 script mention is a string in `gen-wave2.py:52`.
- Its only commit is `2b40aec`, dated 2026-10-21T11:56:57-03:00 (14:56:57 UTC). That is after the pair's run (14:38:59 UTC). KD:80 calls it the "initial predictions.json"; no committed timestamp supports "initial" relative to the runs [INFERENCE: worktree content may predate the commit; not retained].

### F11 [wording] "rejected held witness"
- KD:86 says "It is a rejected held witness"; `corpus/lessons/round-23.md:33` says "Rejects as held witnesses". The phrase is self-contradictory and could be read as a counted witness. Use "uncounted refusal control".

### F12 [not applicable] generic provider declarations
- KD:111–116 (prlimit ceilings; `hardware_acquisition:not-performed`) describe success-envelope fields (`resource_limiter`, `hardware_acquisition`). This pair has neither. Do not cite them for it.

### F13 [verifier coverage] `describe-signals.py` is silent on this record
- Lines 57–62 skip the input checks for error records (F3). Line 44 echoes `env_overrides` without checking it. The carrier mapping at line 58 is never executed for this record.
- The verify wrapper's `passed: true` coincides with `expected_exit 0` and `exit 0`. How `passed` is derived is [INFERENCE: exit-code match; the harness is not committed].

## Positive confirmations (observed)

- P1: `run.stdout` equals the envelope bytes (991 bytes; sha256 04697e72…; run.json:22).
- P2: envelope `ok:false`; `error.code` and `error.category` are `execution_failure`; `retryable:false`; `provider_id` is `sigrok-recording`; `operation` is `decode_signal_recording`; `meta.command` equals argv[3] (`decode-signal-recording`).
- P3: argv[6] `round23_nonexistent_decoder` agrees with the provider's stderr ("No module named 'round23_nonexistent_decoder'").
- P4: the pair's blob IDs are identical at verify rev 6615aeae… and candidate 2838351…. The verify record's bytes therefore apply to the candidate for this pair.
- P5: not absent-provider (`provider_id` present) and not `invalid_request` (code is `execution_failure`). The doc's refusal to rewrite is supported by the bytes.
- P6: this is the only `ok:false` envelope among the six `evidence/c1/*.envelope.json` files.
- P7: committed `sigrok-cli.sh` sha256 50fe4359… equals `pins[0]`.
- P8: committed `uart-hi.bin` sha256 4a2e729f… equals KD:39.

## Claimed field matrix

| # | Claimed field or fact | Where claimed | Retained for this pair | Independently bound | Verdict |
|---|---|---|---|---|---|
| 1 | `ok:false`, `execution_failure`, `retryable:false` | KD:84–88 | Yes (envelope) | No; same-record equality. Envelope sha in self-generated verify record | Holds, unbound |
| 2 | `provider_id`, `operation` | implied by KD:86 | Yes | No | Holds |
| 3 | process exit 1 | KD:84 | Yes (run.json:21) | No; run file unhashed | Holds; attribution F7 |
| 4 | provider `exit_code` 1 | KD:84 (implicit) | Yes (diagnostics) | No | Holds |
| 5 | argv | KD:2 | Yes (run.json:2–16) | argv[3] vs `meta.command` only (describe:64) | Holds, partly checked |
| 6 | stdout | KD:2 | Yes (run.json:22) | Same-record equality only | Holds, unbound |
| 7 | stderr | KD:2; ConnectSignalFirmware:70 | Text yes (envelope; in stdout). run.json:23 empty | No | Misattributed, F8 |
| 8 | environment | KD:2 | Overrides only (run.json:18–20) | No | NOT RETAINED, F1 |
| 9 | launcher `tool.sha256` 50fe4359… | KD:101–102 | No `tool` key | Pins at 14:42:59 match commit blob; not for this pair | NOT RETAINED, F2 |
| 10 | REA 6.5.0 identity | KD header; S060 | argv string only | No npm integrity | Version string only, F2 |
| 11 | input subject `uart-hi.bin` and digest | CoverageMap:72 | No `subject`; argv path only | Verifier skips (describe:57–62) | NOT RETAINED; unbound, F3 |
| 12 | evidence id "none" | CoverageMap:72 | Correctly absent | n/a | Consistent |
| 13 | annotations, window, normalized diagnostics | ConnectSourceChain:31 (L4) | Absent (no `data`) | n/a | Not applicable |
| 14 | prlimit ceilings; `hardware_acquisition` | KD:111–116 | Absent | n/a | Not applicable, F12 |
| 15 | sigrok runtime "pinned" (ELF 10fed05a…) | KD:103–106; SOURCES:66 | Pins only (8 files) | Later instant (14:42:59); worktree read; runtime gitignored | Unbound at producing instant, F5 |
| 16 | Python interpreter identity | stderr only | Not pinned | No | NOT RETAINED, F5 |
| 17 | wrapper bytes at run time | run.json:18–20 (path) | Path only | Commit blob = pins at 14:42:59; not proven at 14:38:59 | Partly bound, F5 |
| 18 | `captured_at` 14:38:59 | run.json:24 | Yes | No | Retained, unbound |
| 19 | source linkage | KD line 1; SOURCES:66 | Row omits the pair | Used-by includes KD (entry-level only) | Partial, F6 |
| 20 | predicted refusal exit 1 | predictions.json `refusal` | Yes | No reader; committed after the run | Unbound, F10 |
| 21 | exclusion from count | KD:86; claims falsifiers | n/a | `count-c1.py:122–123` id gate | Holds; mechanism F9 |

## W1 re-evaluation against candidate 2838351

| W1 item | Claim | Status at candidate |
|---|---|---|
| ConnectSignalFirmware.md:70 | row: subject `uart-hi.bin`; stderr ImportError on run row; exit 1 | Partly holds. Exit 1 yes (run.json:21). ImportError text yes (envelope and stdout), but run `stderr` is empty (run.json:23). Subject not retained, F3 |
| ConnectSignalFirmware.md:76 | "correctly retained with stderr and exit 1" | Holds; cite envelope for stderr, F8 |
| CoverageMap.md:72 | row: (991); none; subject `uart-hi.bin`; execution_failure, exit1 | Size, id, code, and exit hold. Subject does not, F3 |
| CoverageMap.md:131–133 | must not count; "deliberate typed refusal" | Outcome holds. "Typed refusal" is loose wording: this is a provider execution error, not input validation |
| CoverageMap.md:280–282 | only `ok:false` file in evidence/c1 | Holds (six envelopes checked) |
| CoverageMap.md:327–329 | falsifier: must stay visibly uncounted | Holds at entry level (KD:86–88). Not listed in the S060 row, F6 |
| CounterRefusals.md:172 | no `data`, no `evidence_id` | Holds |
| CounterRefusals.md:231 (N9) | never reaches bind_cli (:158 skips it); invisible in R23 output | Holds. Line 158 is the R22 legacy gate; R23's is line 123. Invisible: holds, F9 |
| CounterRefusals.md:321 | envelope `04697e72…` | Holds (prefix of 04697e72e9cabc9dae…) |
| CriticSeparation.md:28 | five envelopes: run.stdout == envelope bytes | Holds for this pair (P1). Other four not reviewed (out of scope) |
| CriticSeparation.md:55 | "calibration-type material" | Opinion; not testable from bytes; not evaluated |
| CriticVacuity.md:81 | "counter correctly blocks it" | Outcome holds; mechanism inexact, F9 |
| ConnectSourceChain.md:31 | L4 list incl. ev id, annotations, window, diagnostics, "pinned carriers" | Does not apply to this pair. Carriers are not in tool-runtime-pins.json (8 tool files only) |
| ConnectSourceChain.md:265 | decode-invalid-decoder must not bind | Holds (zero id overlap) |
| PlannerDataWalk.md:100 | absent subject and evidence id; control, not witness | Holds |
| ReviewRegistryHome.md:61 | KD cites the decode-invalid-decoder envelope | Holds at entry level. Not at row level, F6 |
| SchemaFlutter.md:140 | `invalid_request` in Flutter projection | Different provider and operation; not evidence about the sigrok pair |
| lessons/round-23.md:25–26, 33 | invalid_request not substituted; "rejects as held witnesses" | Holds on outcome; wording, F11 |
| gen-wave2.py:32 | this seat's spec | Consistent with bytes |

## Produced files and hashes

- `.ufo/waves/round-23/w2/OriginalRefusal.md` (this report). Its sha256 is in the final message.
- No other files written in the repository.
- Scratch files `/tmp/run.json`, `/tmp/env.json`, and `/tmp/signal-records.json` were created by me, outside the allowed write paths, and removed (`rm -f`, exit 0). Disclosed as a process deviation.
- Early navigation used shell `grep` over `git show` and `git ls-tree` output. It was read-only over committed bytes; later checks used Python over committed bytes.

## Installs

None.

## Commands run (exit codes)

- `git show 2838351…:PATH` (several dozen): exit 0 for all listed paths.
- `git rev-parse --verify --quiet <rev>:PATH`: exit 0 for present blobs. Exit 1 for the verify record at 6615aea, which is absent at that rev (expected).
- `git ls-tree -r --name-only 2838351…`: exit 0.
- `git log --format=… 2838351… -- .ufo/waves/round-23/predictions.json`: exit 0.
- `git status --short`, `git log --oneline -5`: exit 0.
- Python in-memory parsing, hashing, and scans over committed bytes: exit 0.
- Not run: `count-c1.py`, `describe-signals.py`, `sigrok-cli.sh`, `npx`/`rea-agents`, any test, build, or formatter.

## Open risks and unknowns

1. The wrapper, sigrok runtime, and Python bytes at the producing instant (14:38:59) are unknown. The worktree was not read, per assignment.
2. The runtime pins are a later-instant read by the same lane. They are not an independent binding.
3. No replay was performed. The knowledge entry's `recheck:` command (describe-signals) does not verify the input carrier or the environment.
4. `npx -y rea-agents@6.5.0` package bytes are unverified. The version string is the only identity.
5. `r21.refused` (`count-c1.py:51`) was not reviewed. It is not reached on this pair's path (F9).
6. The other four signal records were not source-reviewed. F5 and F6 likely apply to them in part [INFERENCE].
