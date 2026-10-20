# Round-19 wave-2 C3 knowledge review

**Axes:** calibration (holdout and decision boundary), freshness (Go 1.25.0 evidence), depth (carrier and evidence-model scope).

Review is read-only at observed main tip `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`, except this report. Findings below distinguish artifact observations from interpretation.

## Findings

### Medium — The Go 1.25.0 `vet` prediction predates this round; qualify “held-out artifact” as outcome-held-out

**Observation.** The R18 entry says Go 1.25.0 was already represented in the synthetic cohort, while the official toolchain binaries had not been run by Ghidra (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:47-60,98-105`). More specifically, the earlier R18 wave-2 review recorded an emulator prediction for Go 1.25.0 `vet`: H1 `invalid_index 13902080` (`.ufo/waves/round-18/w2/KnowledgeEntryReview.md:84-100`). R19 freezes that same H1-only index for `t1250-vet` (`.ufo/waves/round-19/predictions/decision-rule.json:21-28`), then records it in the run log (`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:34-42`). The earlier review excerpt does not provide a carrier digest, so exact byte identity between that earlier candidate and the R19 `t1250-vet` digest is **not established here**.

**Interpretation.** The R19 observation is held out from a prior Ghidra run and is not version-held-out; the entry correctly says both (`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:9-19`). It is not, however, a novel emulator prediction for the `vet` candidate. The earlier predicted index was public before the R19 analysis. The knowledge entry's “previously unrun” wording is accurate, but it should make the earlier prediction exposure explicit; the frozen rule’s “none was in the round-17/18 ... prediction sets” (`decision-rule.json:27`) should distinguish a formal frozen prediction set from an earlier published candidate prediction. This narrows the calibration novelty; it does not negate the observed log match or establish that the earlier and current bytes are identical.

### Medium — The canonical C3 claim still describes applications and a broader version family

**Observation.** The C3 `claim` still says “held-out Go 1.25.0 application ELFs,” and its falsifiable statement says “held-out go1.25.x carriers” (`.ufo/waves/round-19/claims.json:26-27`). The amendment itself corrects this to previously unrun Go 1.25.0 toolchain ELFs, artifact-held-out rather than version-held-out, not applications (`claims.json:37,40`); the knowledge entry and all eight carrier rows also use the toolchain/artifact-specific scope (`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:9-17`; `.ufo/waves/round-19/predictions/carriers.tsv:1-8`). R18 already contained Go 1.25.0 synthetic carriers (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:47-60`).

**Finding.** The knowledge entry is properly bounded, but the canonical claim fields remain contradictory rather than being superseded. A reader consuming `claims.json` without interpreting its amendment can infer application coverage or a Go-version holdout that this cohort does not supply. Recast the canonical claim and falsifiable string as the observed Go 1.25.0 toolchain-artifact cohort; keep application coverage and version generalization out of the result.

### Medium — A carrier was executed despite the wave contract

**Observation.** The contract says “Never execute a carrier binary” and lists the C3 Go 1.25.0 `bin/go` path among carriers (`.ufo/waves/round-19/contract.md:39-42`). The round-19 lesson records that the install-record seat ran `go version` using Go 1.24.6/1.25.0 `bin/go`, including a C3 carrier (`corpus/lessons/round-19.md:88`). The knowledge entry also discloses an install-record seat's `bin/go version` invocation outside the analysis runner and says it was not used as outcome evidence (`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:11`).

**Finding.** “No carrier was executed by the analysis runner” is narrowly accurate, but it does not satisfy the broader no-execution contract. Treat this as a disclosed process exception, not as an execution-free wave. The available evidence does not show that the version query affected the static Ghidra observations; it also does not waive the contract violation.

## Checks that support the stated limits

- **One pass:** the retained run log shows the eight labels in sequence, once each, ending with aggregate exit 1 because `vet` compare exited 1 (`.ufo/waves/round-19/runs/run-log.txt:1-19`). The knowledge entry correctly limits this to one pass and does not claim repeatability (`.../2026-10-20-r19-go125-toolchain-replay.md:21-38,64`).
- **Silent is not safe:** the seven non-D observations have empty `symbol_analysis_failures`, `invalid_index_reads` and `eof_reads` in the retained observation JSONs (command below). That establishes no such event in the captured observations, not correct type recovery or safety. The entry makes that distinction at lines 59-61; the receipt itself warns that polling may omit lines written after the final copy (`runs/t1250-vet/receipt.json:24`).
- **Evidence boundary:** `runs/t1250-vet/analyze.json:1` is `binary_overview` Evidence about the `vet` subject. The failure is in the provider log, not a field in that Evidence; the knowledge entry says this explicitly (`.../2026-10-20-r19-go125-toolchain-replay.md:48-53,64`). Receipt log hashes and bindings are retained producer/receipt-chain evidence, not an REA Evidence assertion of the log’s contents (`runs/t1250-vet/receipt.json:1892-1914`). This limitation is appropriately disclosed.

## Residual risks and verification gaps

- Scope is one Go 1.25.0 linux/amd64 toolchain release, REA 6.5.0, Ghidra 12.1.4, one positive (`vet`), seven quiet controls, one pass. It does not establish application coverage, Go-version generality, deterministic repeatability, target behavior, recovery quality, or that quiet carriers are correctly decoded.
- “Silent” remains bounded to retained log prefixes: receipt capture is polling-based and can miss post-final-poll lines (`runs/t1250-vet/receipt.json:24`). The entry appropriately says “no failure observed in retained prefix” (`.../2026-10-20-r19-go125-toolchain-replay.md:61`).
- The knowledge entry records eight historical receipt validations and explains why a live replay against the changed validator bytes is not equivalent (`.../2026-10-20-r19-go125-toolchain-replay.md:44-46`). This review queried the retained validation JSON summaries; it did **not** rerun the validator or independently re-hash all logs. The receipt JSON itself is producer-authored and is not independent authenticity evidence.
- The runner deletes an existing per-label output directory before a rerun (`.ufo/waves/round-19/run-carriers.sh:262-276`); no repeat pass was run. Preserve this pass before any future remeasurement.
- No LSP device was exposed in the available tool set. This review concerns Markdown/JSON/evidence and makes no source-caller or semantic-reference claim; no grep result is used as semantic proof.

## Commands and exits

Commands were read-only and run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

```text
find .ufo/waves/round-19/runs -mindepth 2 -maxdepth 2 -name compare.json -type f | wc -l
8; exit 0
```

```text
jq -s 'map(select(.exit == 0 and .counts.valid == 1 and .counts.invalid == 0 and .counts.unreadable == 0)) | length' .ufo/waves/round-19/evidence/receipt-validation/t1250-*.json
8 retained validation summaries; exit 0
```

```text
jq -s 'map(select(.steps.analyze.argv[0] == "npx" and .steps.analyze.argv[3] == "analyze" and .steps.analyze.exit == 0)) | length' .ufo/waves/round-19/runs/t1250-*/receipt.json
8 analyze-step receipts; exit 0
```

```text
jq -s 'map(select(.symbol_analysis_failures == [] and .invalid_index_reads == [] and .eof_reads == [])) | length' .ufo/waves/round-19/runs/t1250-{go,gofmt,asm,cgo,compile,cover,preprofile}/observation.json
7 non-D observations with no recorded failure/read; exit 0
```

No carrier, REA analysis, build, suite, or install was run for this review.