# C3 review — calibration, coverage, depth

## Findings

### High — “first failure” has no unique oracle

**Observation:** C3 claims the “FIRST Go-analysis failure” and gives `kind`, `index`, `va`, and `phase`, but the contract leaves `kind` open (`"invalid_index"|"eof"|...`) and defines no ordering, event domain, coordinate units, or h0/h1 mapping (`.ufo/waves/round-20/claims.json:36`; `.ufo/waves/round-20/contract.md:76-81`). The existing extractor treated `eof_reads`, `invalid_index_reads`, and `symbol_analysis_failures` as distinct event families (`.ufo/waves/round-17/tools/log-extract.py:23-35`). In a retained t1250-vet log, `GolangSymbolAnalyzer` reports “Go analysis failure” at line 186, followed by its cause `Invalid index: 13902080` at line 229 (`.ufo/waves/round-19/runs/pass2/t1250-vet/logs/rea-ghidra-PEkTou/ghidra.log:186,229`; extracted fields at `.ufo/waves/round-19/verify/log-extract-t1250-vet.stdout:55-60,73-75`).

**Inference:** “first diagnostic”, “first read-boundary failure”, and “root cause” can produce different answers on an already-bound example; matching is not reproducible until one is chosen. An open-ended kind and unnamed index/VA domains also permit incomparable predictions to be reported as matches.

**Pin now:** Define the failure event set and precedence (including wrapper errors versus causes), stable `kind`/`phase` values, what `index` and `va` measure, and exact comparator fields. Define which hypothesis is masked (`h1` or `h0`) and score h0/h1 separately without post-hoc best-of-two. Add cases for the t1250-vet ordering, multiple events, and each kind/coordinate.

### High — silence can be confused with incomplete capture

**Observation:** The contract says `null` means predicted silent and allows comparison exit 2 for unevaluable input (`.ufo/waves/round-20/contract.md:78-81`). A round-19 bound receipt explicitly warns that polling may omit log lines written after the final poll (`.ufo/waves/round-19/runs/pass2/t1250-vet/receipt.json:23-24`); the existing receipt validator documents that it checks current bytes and cannot detect bytes modified and restored during the run (`.ufo/waves/round-17/tools/receipt-validate.py:45-52`). The legacy extractor also explicitly excludes a torn final line (`.ufo/waves/round-17/tools/log-extract.py:31-35`).

**Inference:** `--require-mid-maps` and a valid digest do not, by themselves, establish that a log is complete. Treating “no parsed event” as silence can therefore convert a missing/truncated failure into a false match.

**Pin now:** Reserve observed silence for a demonstrably complete run/log. Missing logs, incomplete polling, parse gaps, or torn/truncated endings MUST yield unevaluable (exit 2) and be excluded from both numerator and denominator. Keep this distinct from the forecast’s `null`.

### Medium — the retrospective cohort must not enter predictive k/N

**Observation:** The round-19 pass2 run log records eight t1250-go1.25.0 runs on 2026-10-20, ending at 16:31:01 -03; the round-20 claim commit `d1d981d2cc041dda4656c5b01d2c8445d8d17124` is timestamped 17:43:06 -03, and `claims.json:6` defines its committer time as the declaration instant (`.ufo/waves/round-19/runs/pass2/run-log.txt:1-19`; `.ufo/waves/round-20/claims.json:6`). Those outcomes were already extracted and compared: t1250-vet had an observed single invalid index against a three-index prediction, with `all_match: false` (`.ufo/waves/round-19/verify/compare-t1250-vet.stdout:2,51-60`). The round-19 lesson explicitly records prior vet-prediction exposure and the unmasked-variadic full-walk weakness (`corpus/lessons/round-19.md:187-190`). C3 calls the round-19 check retrospective, but its single `k/N` and `first_failure_bound` field do not name a cohort (`.ufo/waves/round-20/claims.json:37-39`).

**Inference:** The replay is useful as a development/regression check, not independent prediction evidence. Without an explicit cohort boundary in the measure output, a reader can misread known round-19 outcomes as contributing to the held-out score.

**Pin now:** Emit separately labelled `retrospective-known` and `held-out` counts/results; compute `k/N` only over frozen go1.24.6 held-out carrier identities. Add a falsifier/test showing inclusion or removal of any round-19 log cannot change held-out `k` or `N`. Describe the retro result as replay only, not out-of-sample accuracy.

### Medium — freeze/push order and carrier membership need auditable bindings

**Observation:** C3 requires a prediction freeze/push before analysis and says runs before the push falsify it (`claims.json:36,39`), but the contract specifies tool interfaces rather than a freeze/push evidence record (`contract.md:76-81,88-92`). The source inventory identifies 20 go1.24.6 ELFs (`.ufo/waves/round-20/w1/SourceGo1246.md:27-29`); the arm record names those carriers and their digests (`.ufo/waves/round-20/evidence/carrier-guard/manual-arm.json:4-20`). The claim’s threshold is only `N >= 8` and gives no selection rule (`claims.json:37`).

**Inference:** A receipt can pass `--require-mid-maps` without the contract requiring that its mid-run maps bind the exact forecast and emulator blobs from the named freeze commit. A local freeze commit alone also does not prove it was pushed before the first run. The minimum of eight leaves room for unreported/post-hoc carrier exclusions from the 20-file population.

**Pin now:** Freeze a manifest of the full 20-carrier inventory (path + SHA-256) and the selected set before any held-out result; require N>=8 and no post-result additions/drops. Bind every prediction to its carrier digest and bind each run’s pre/mid maps to the frozen prediction, emulator, snapshot inputs, and carrier. Retain the freeze commit OID plus evidence of the pushed ref, and require the earliest analyze `started_at_utc` to follow that push. Add falsifiers for missing/extra/changed carriers, an unpinned forecast, a run before push, N<8, and post-run carrier removal.

## Verification gaps and residual risk

- **Observation:** `.ufo/waves/round-20/tools/` was absent at review time, so I could not inspect or execute the C3 implementation/measure logic. The review is against the claim, contract, and retained round-19 evidence only; no C3 runtime checks were run.
- **Observation:** `xd://lsp` returned “No such tool”; no LSP status/references/definition/diagnostics were available. I used direct reads for the cited source and artifacts; text search was used only to locate log records.
- **Residual risk:** Even with these falsifiers, the retrospective go1.25.0 cohort cannot establish held-out predictive performance. State the held-out population and environment limits; contract identifies go1.24.6 toolchain ELFs and Ghidra 12.1.4 (`contract.md:88-94`).

## Commands and exits

- `cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git log --oneline -5 refs/heads/main && echo "---" && git rev-parse refs/heads/main && echo "---status---" && git status --porcelain | head -40; echo "exit=$?"` — exit 0 (read-only state inspection).
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show -s --format='%cI %H' refs/heads/main` — exit 0 (`2026-10-20T17:43:06-03:00 d1d981d2cc041dda4656c5b01d2c8445d8d17124`).
- No Go toolchain, REA, Ghidra, test, or C3 measurement command was run. No tools were installed or updated.
