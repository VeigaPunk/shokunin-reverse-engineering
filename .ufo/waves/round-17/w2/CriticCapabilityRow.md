# W2 CriticCapabilityRow — attack on the planned row `retained REA Ghidra-session log capture`

Seat: KaidokuR17.CriticCapabilityRow, an author-side advisory critic, not an outside reviewer. Lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da`; tools unchanged since `2711674`, which was committed before the runs. Axes: calibration, depth.
Target: the draft row `w1/draft-scorecard.md:44`, its entry condition `:46`, claim C2 (`claims.json:22`, "+1 only if the capture runs and its receipt validates"), and the AXES test (`/home/vgpnk/Projects/shokunin/AXES.md:62-64`: a capability enters only when the round demonstrates it running). The "standalone" test comes from lane precedent (`SCORECARD.md:1089-1094`).
Method: read-only. I ran the round-17 tools against the retained files. Scratch work was in `/tmp/kr17-ccr/` only: a copy of the validator with a 2-line patch, and a harness with an injected fake runner. I launched no REA analyze and executed no carrier. No installs.

## Verdict

- **Runs:** yes. 8/8 runs show analyze exit 0, an evidence id, exactly one bound session, and `pins_compare.equal` true.
- **Verifies:** **NO at da64646.** The pre-registered entry gate fails on every retained receipt (F1).
- **Standalone:** partial. There are four coupling defects (F3, F4, F7, F8).

The row must not enter as drafted. It becomes admissible after one shape-only validator fix, which must be disclosed as a post-observation gate repair (tradeoff for the judge, below), plus the limits in §Row limits.

## Findings

### F1 — BLOCKER (calibration): `receipt-validate.py` rejects all 8 retained receipts
- **Producer:** `tools/carrier-run.py:309,349` writes `steps` as a **dict**, keyed by step name.
- **Validator:** `tools/receipt-validate.py:98` classifies a receipt as `carrier` only when `steps` is a **list**.
- **Validator selftest:** its carrier fixture uses a list (`receipt-validate.py:470`). So the selftest is green against a shape the producer never emits.
- **Contract:** `contract.md:43` says "every step {…}" and never fixes the container type. That gap is how the two tools ended up disagreeing.
- **Command:** `python3 -I -B tools/receipt-validate.py runs/{calib-esbuild-0.25.12,calib-shfmt,pro-aether,pro-containerd-shim,pro-esbuild-0.21.5,pro-esbuild-0.27.7,pro-notesmd-cli,pro-op}/receipt.json`
  - Output: `exit=1`, `{"invalid":8,"receipts":8,"unreadable":0,"valid":0}`.
  - Every receipt shows `kind=unknown`, the single finding `unrecognized_shape`, and 306 checks.
- **What still holds:** none of the 306 checks is a digest mismatch. The bytes are consistent; only the gate fails.
- **What never ran:** the carrier required-field and per-step checks (`:271-307`).
- **Strongest counterexample to "a trivial fix closes it":** I made a scratch copy with `:98` accepting `(list, dict)` and `:284` iterating `.values()`.
  - Same 8 receipts: `exit=0`, `{"invalid":0,"valid":8}`, `kind=carrier`, 336 checks each.
  - So the receipts are well-formed once the classifier accepts them.
- **Smallest fix:**
  - Make that 2-line change in the real validator.
  - Add a selftest case that validates the receipt carrier-run's own selftest writes (the real producer shape), not a hand-built list.
  - Re-run the validator on the 8 receipts and retain its stdout and exit.
- **Tradeoff the judge must rule on:** the gate was fixed after it was seen failing. That fix must be disclosed in LOG and SCORECARD as a shape-only repair: no digest or pin rule loosened, and 30 more checks run, not fewer. It must not be presented as "validated first time".

### F2 — HIGH (calibration): drift during the run is recorded but exits 0; SKILL says exit 1
- **Code:** carrier-run records `pins_changed_during_run` (`carrier-run.py:427-433`). But its exit decision (`:376-383`) reads only the pre/post compare. The validator never reads that field either.
- **What the docs claim:** `SKILL.md:532` says "exit … 1 pin drift" and "pinned pre, every 30 s, and post".
- **Counterexample:** `python3 -I -B /tmp/kr17-ccr/harness.py`, case T3. The fake child rewrote the fake carrier bytes mid-run, then restored the bytes and mtime. `PIN_CHECK_S` was set to 0.
  - Output: `"exit": 0, "pins_compare_equal": true, "pins_changed_during_run": {"changed": ["…/carrier.bin"]}`.
  - Validator on that receipt (scratch copy): `exit=0`, status `valid`, findings `[]`.
- **Harm to the retained evidence:** none observed. `pins_changed_during_run` is absent in 8/8 receipts (jq `.steps.analyze.pins_changed_during_run` is `null`). Checks ran only every 30 s.
- **Smallest fix:**
  - Return 1 at `carrier-run.py:376` when any step carries `pins_changed_during_run`.
  - Add a validator finding for that field.
  - Until then, the row and SKILL must say mid-run checks are "recorded, not gating".

### F3 — MEDIUM (standalone/depth): a symlink or relative `--carrier` loses the carrier digest and the session binding
- **Code:** `pins.snapshot` keys entries by realpath (`tools/pins.py:66`). `carrier-run.py:301,347` look up the raw path.
- **Counterexample:** harness case T2, `--carrier` given as a symlink.
  - Output: `"carrier": {"path": "…/carrier-link"}` with no `sha256_pre`, while the realpath key is present among the pin keys.
  - `bind_session(..., None)` returns `{"logfile_ok": false, "target_ok": false}`.
  - Validator on that receipt: `exit=1`, `missing_field $.carrier`.
- **[INFERENCE, code read `:351-357,:381`]:** in live private-root mode this means bound = 0, so exit 2, after a full analyze.
- **Harm to the evidence:** none. All 8 carriers are regular, non-symlink absolute files (observed with `ls -la`).
- **Smallest fix:** `carrier = os.path.realpath(carrier)` at the start of `run()`. Until then, the row limit is "absolute canonical path only".

### F4 — MEDIUM (calibration): the row text and evidence pointer overclaim and cite an unexercised argv
- **Overclaim:** the draft row (`w1/draft-scorecard.md:44`) says the tool "extracts Go analyzer diagnostics and compares them". carrier-run does neither. Extraction and comparison are separate steps chained by `run-carriers.sh:24-26`, which also uses `jq`.
- **Comparison outputs are outside the receipt:** `grep -c observation runs/calib-shfmt/receipt.json` gives `0`. Their integrity is the git blob only.
- **Pointer argv not exercised:** the pointer gives `python3 -I …carrier-run.py --carrier … --label … --out-dir …`. The exercised argv (receipt `orig_argv`) was:
  - `python3 -I -B`;
  - `--timeout 1500 --poll 0.5`;
  - 144 `--pin` arguments (jq count 8/8), giving 146 pinned paths.
  - pro-op additionally ran with `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` (`rea_ghidra_env`).
  - This is the R16-INVOCATION defect class again, inside the very round that discharges it.
- **Smallest fix:**
  - Name the row for capture only; w1 `CriticCapabilityPreclaim` F6 asked the same.
  - Point at `runs/*/receipt.json` plus the retained validator exit plus the SKILL entry `run-carriers.sh <LABEL>` (`SKILL.md:532`).
  - Label the bare argv as an unexercised variant.
  - Note pro-op's startup-timeout env.

### F5 — MEDIUM (depth/calibration): tail loss is real in 8/8; the round's own tools cannot detect it
- **Last retained line:** `tail -n 1 runs/*/logs/*/ghidra.log` shows all 8 end at `ANALYZING changes made by post scripts: file:///…/target-<sha12>.bin`. No bridge or post-analysis line was retained.
- **Timing:** `last_copy_utc` is 0.50–1.00 s before `steps.analyze.ended_at_utc` in 8/8 (for example shfmt 13:47:36.762 against 13:47:37.309). The "final best-effort" scan (`carrier-run.py:439`) never added bytes. [INFERENCE: REA had already removed the root.]
- **What was captured:** `grep -c "REPORT: Analysis succeeded"` gives 1 in each of the 8 logs. Go diagnostics come before it (shfmt Go lines 82-89, marker 119, log 125 lines). So the C2 Go-field comparisons fall inside the captured window.
- **Earlier corrections not integrated:**
  - `log-extract.py` emits no `analysis_succeeded_present` / `last_line` field; its observation keys lack one.
  - The w1 fixes (rotation prefix rule, held-fd capture: `w1/CriticCapabilityPreclaim.md:50-78`) are not in the tool.
- **Smallest fix:** in the row, state "prefix ends at the last retained line, 8/8 cut at the post-script re-analysis; absence valid only before `Analysis succeeded`". Optionally add the marker field to log-extract.

### F6 — MEDIUM (calibration, "verifies"): the binding gate has never been shown able to fail
- **Code:** the selftest injects a runner (`carrier-run.py:543-547`). With an injected runner, `private_root` is None, so the exactly-one-bound-session gate (`:381`) is inactive.
- **Selftest fixture:** it writes no `Using log file:` or `IMPORTING:` lines, so `bind_session` is never exercised green or red.
- **Commands:** `carrier-run.py --selftest` gives `SELFTEST: CLEAN cases=2`. `receipt-validate.py --selftest` gives `SELFTEST: CLEAN cases=5`.
- **Live runs:** they exercised only the green path: bound 1/1 and unbound 0 in 8/8, with `logfile_ok` and `target_ok` true.
- **Smallest fix:** a selftest case in private-root mode where a fake log lacks the `IMPORTING …target-<sha12>` line, expecting exit 2.

### F7 — LOW (standalone): a hard-wired round-16 pin
- **Code:** by default carrier-run pins the round-16 `selection.py` (`carrier-run.py:37,284`). If that path is missing, the pin entry errors and the run returns 2 before any analyze (`:303-306`, with `pins.py:40-42` producing the error).
- **Carriers are not retained in the repo:** they are host files (`/usr/bin/{shfmt,aether,containerd-shim-runc-v2,op}`, the pnpm store, `~/.local/bin`). A re-run depends on host state; a sha mismatch would be detectable.
- **Smallest fix:** row limit "lane-local tool; carriers pinned by sha, not retained".

### F8 — LOW (hygiene/provenance)
- **(a) Private parents are never removed.** `session_parent_leftovers=["node-compile-cache"]` in 8/8, so `:366-367` never runs `rmdir`. `ls -d /tmp/kr17-rea-*` shows 8 run parents still present, each containing `node-compile-cache`. The row and SKILL must not imply cleanup.
- **(b) `runs/run-log.txt` lists 7 of the 8 runs.**
  - calib-shfmt is missing: its receipt shows it ran 13:47:05–13:47:37Z, and the log begins with calib-esbuild at 10:47:42-03.
  - Under `run-carriers.sh:15`'s `rm -rf`, a full invocation would have started with calib-shfmt (first line of `carriers.tsv`). So the shfmt invocation is retained only through its receipt `orig_argv`.
  - Prediction freeze before the first run is confirmed: commit `2711674` at 10:46:45-03, first pin at 10:47:05-03.
  - Smallest fix: cite receipts, not run-log, as the run record.

## Row limits the row must carry (compressed)
1. **Not complete.** A polling prefix, cut at post-script re-analysis in 8/8. Absence claims are valid only before `REPORT: Analysis succeeded`, which is present in 8/8.
2. Only `ghidra.log` and `script.log` are copied; `session.json` is never copied. Each log dir holds exactly those two files in 8/8, and 0 64-hex strings appear in the logs.
3. **Side channel.** It reads REA 6.5.0's private `rea-ghidra-` root under a private `TMPDIR`. This is an undocumented internal; the prefix is visible in `dist/cli-runtime/binary-BVOr2mgE.js:5926`, and the npx-resolved `package.json` version is 6.5.0. The log is outside REA Evidence: the evidence-id ↔ log link comes from the receipt's step window plus in-log path/sha12 binding.
4. Mid-run 30-s pin checks are recorded, not gating (F2), until fixed.
5. The carrier must be an absolute canonical path (F3), until fixed.
6. The validator passes only after the disclosed shape-only repair (F1).
7. Extraction and comparison are separate tools whose outputs are not receipt-committed (F4).

## Checked with no finding
- Digest integrity of all receipt-committed files: 306 checks unpatched, 336 patched, 0 mismatches.
- Analyze exit 0 and evidence id present: 8/8.
- `pins_compare.equal`: 8/8.
- One bound session and 0 unbound sessions: 8/8.
- Every receipt records `log_capture_limit`.
- Compare exit 0 in 8/8, with classifications as logged: 3 `bootstrap_missing`, 4 `snapshot_loaded`, 1 `other`.
- The REA socket-root prefix `rea-ghidra-socket-` (`binary-BVOr2mgE.js:5342`) could match `rea-ghidra-*` only when the socket path exceeds 107 bytes. In that case it falls back to `/tmp`, outside the private glob; no foreign session was tracked in 8/8.

Installs/updates: none.
