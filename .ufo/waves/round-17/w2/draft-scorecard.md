# Draft — SCORECARD.md `## Round 17` (w2 author-side draft, not integrated)

Status: DRAFT for L1 integration. Not an admission and not a measured closure. Every number below is either (a) read from committed evidence at lane revision `da64646adcb19c1ede7537b799b8c7d283fe43da` (cited with its command in `DraftScorecardR17.md`), or (b) a `{FINAL:...}` slot for the post-integration verification run. No outside verification is claimed. Shape follows `SCORECARD.md:2294-2348` (round 16).

---

## Round 17 — retained Go carrier diagnostics and routed r16 defects, 2026-10-20

Baseline: `b563c799d97774aae4351276fe43cb897311e349` (`.ufo/waves/round-17/claims.json` `baseline`).
Predictions frozen before the first carrier run at `271167473d87ef710f07ecdd98caf0ce12091686` (`.ufo/waves/round-17/predictions/`; no later diff to that directory at `da64646`).
Committed pre-falsify source revision: `da64646adcb19c1ede7537b799b8c7d283fe43da`. Final measured source revision: `{FINAL:REV}`.
Producer evidence: per-carrier `.ufo/waves/round-17/runs/<label>/receipt.json`, `observation.json`, `compare.json`; full argv/exit record `{FINAL:producer-record path}`; LOG round-17 and `corpus/lessons/round-17.md`; knowledge `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`.

| Claim / axis | Existing numeric proxy | Falsifiable supplemental before→after, command and measured revision | Author-side verdict / limits |
|---|---|---|---|
| C1 calibration | 10.0→10.0, delta 0; three owned finite proxies tie at 10.0 at baseline | (a) temporal-sweep unqualified sites 4→0: `python3 -I -B .ufo/waves/round-17/tools/temporal-sweep.py --root <LANE> --rev da64646 --sites-rev b563c79` gives sites 4, corrected 4, unqualified 0 (baseline command with `--rev b563c79`: corrected 0, unqualified 4); final `{FINAL:sweep unqualified}` at `{FINAL:REV}`. (b) `pins.py --selftest` red case: mutated temp file named, compare exit 1; selftest `CLEAN cases=7`. (c) `invocation-audit.py` unlabelled-variant rows 2→{FINAL:unlabelled}; at `da64646` the count is 11 of 17 rows. (d) QUALITY row 19 presence 0→1 (`corpus/QUALITY.md:29`). | {FINAL:verdict_C1}. Sub-claims (a), (b), (d) are mechanically discharged at `da64646`; (c) is not (11 unlabelled rows at `da64646`, 2 at baseline). Limit: `pins.py` proves identical bytes at two instants, never unchanged throughout. The sweep covers only the lane files named in `contract.md` plus `corpus/knowledge/`. |
| C2 depth | 10.0→10.0, delta 0 (measured); main capability table 4 rows at baseline (`SCORECARD.md:619-622`) | Retained carrier runs carrying pinned carrier, REA Evidence ID, and retained-log sha256 with a prediction comparison: 0→8 at `da64646` (8/8 `bound_sessions` length 1, `unbound_sessions` empty; 16 retained log files whose sha256 equals the committed blobs; pins pre/post 146 entries, equal in 8/8). Prediction mismatches reported: 0 of 8. `compare.py` exit 0 ×8. `receipt-validate.py` on the 8 receipts: exit 1 at `da64646` (8 invalid); final `{FINAL:validate exit}`. | {FINAL:verdict_C2}. The 8-run retention target is met; the capability entry condition (validator exit 0) is not met at `da64646`. Limit: polling copy of `ghidra.log`/`script.log` at 0.5 s; lines after the last poll before REA deletes its runtime root can be missing. |
| coverage | knowledge mapping 94/94→95/95 (`measure.py`, missing and dangling empty at both revisions); SOURCES 23→30 rows | `python3 -I -B .ufo/waves/round-17/measure.py da64646` and baseline `measure.py b563c79`; SOURCES tiers A21/B1/C1→A26/B2/C2; statuses mined22/rejected1→mined28/rejected2; `{FINAL:measure exit}` | {FINAL:verdict_coverage}. Depth on held Go ground, not expansion of domain surface. |
| operability | no owned numeric proxy (controls and selftests only) | `controls.py b563c79 da64646` exit 0 at `da64646`: 20 lesson prefixes, 94 knowledge prefixes and the LOG old prefix retained; five prior verifier files unchanged; 14,943 pre-existing `.ufo/waves/**` and `evidence/**` blobs checked, all unchanged; QUALITY admission rows 18→20 with prior rows byte-identical; craft 17/17. Selftests at `da64646`: pins 7, log-extract 8, predict 17, compare 10, receipt-validate 5, all `CLEAN`. Final `{FINAL:controls exit}`, `{FINAL:selftest exits}`. | {FINAL:verdict_operability}. The `receipt-validate` selftest is clean while the 8 real receipts are invalid; the selftest does not exercise the producer's shape. |
| freshness | no owned numeric proxy | Carrier, `selection.py`, prediction and 143 installed Go data files (146 pinned paths) hashed pre and post for each run; 8/8 equal at the two instants retained. No mid-run map is retained. | {FINAL:verdict_freshness}. Identical bytes at two instants only; no continuity claim. |
| adjacency | no owned numeric proxy | local source-model, installed data and documentation evidence only | {FINAL:verdict_adjacency}. No sibling gate, config or engine ownership taken. |

The supplemental counts are not expertise scores or unbiased calibration measures. The three-way lowest-axis tie is worked through calibration; no proxy is retired or relabeled.

### Named correction — R16-PROVENANCE (append-only; no r16 bytes rewritten)

The r16 section (`SCORECARD.md:2294-2348`) contains no temporal-stability sentence at the baseline. The corrections for the four r16 sites are carried where the sites are: `LOG.md:2059-2062` and `corpus/lessons/round-17.md:85-88` (each `R16-PROVENANCE` line names the exact `file:line` and says temporal stability is not evidenced). No SCORECARD correction is invented for a sentence that does not exist here.

### Capability addition — conditional, NOT entered at `da64646`

Target: main `## Capabilities` table, rows at `SCORECARD.md:619-622`. Round-13 and round-14 rows sit in round sub-tables (`SCORECARD.md:2135`, `:2207`); whether they are appended to the main table is an L1 decision outside this claim.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| retained REA Ghidra-session log capture for caller-selected Go carriers | For a carrier pinned by path and SHA-256, runs REA 6.5.0 analyze with per-poll copies of the session-bound `ghidra.log` and `script.log`, extracts GoApiSnapshot and GoRttiMapper diagnostics, and compares them with predictions committed before the run | `.ufo/waves/round-17/runs/<label>/receipt.json` (8 retained at `da64646`); `receipt-validate.py` exit {FINAL:validate exit}; `python3 -I -B .ufo/waves/round-17/tools/carrier-run.py --carrier <PATH> --label <LABEL> --out-dir <DIR> --pin <PREDICTION>` | round-17 |

Entry condition: `receipt-validate.py` exit 0 on the retained receipts. At `da64646` the condition is false (exit 1, 8 invalid). If `{FINAL:validate exit}` is not 0, no row is added and the stagnation counter does not reset.

Prediction vs observation (committed at `da64646`; each `compare.json` `all_match: true`):

| Carrier (label; path; sha256[:16]) | Go version (`inspect-go-binary`) | Predicted untested / snapshot / bootstrap / route | Observed untested / snapshot / bootstrap / route | Match |
|---|---|---|---|---|
| calib-shfmt; `/usr/bin/shfmt`; `58f765638eed5309` | go1.27.0-X:nodwarf5 | 1.27.0 / none / missing / none | 1.27.0 / none / missing / none | yes (calibration, pilot-seen) |
| calib-esbuild-0.25.12; kimi-code pnpm; `bab29b2ca7a9e89b` | go1.23.12 | none / 1.23.12 / loaded / info | same | yes (calibration, pilot-seen) |
| pro-notesmd-cli; `~/.local/bin/notesmd-cli`; `412dc532d278b9e4` | go1.25.8 | none / 1.25.8 / loaded / fallback to 1.25.0 | same | yes |
| pro-aether; `/usr/bin/aether`; `06c91f55df4117e5` | go1.25.14 | none / 1.25.14 / loaded / fallback to 1.25.0 | same; unpredicted analyzer EOF after bootstrap (cause UNKNOWN) | yes; failure recorded, not hidden |
| pro-esbuild-0.21.5; pnpm; `b567f467fdac92c6` | go1.20.12 | none / 1.20.12 / loaded / info | same | yes |
| pro-containerd-shim; `/usr/bin/containerd-shim-runc-v2`; `d3aa80d720b80f70` | go1.27.2-X:nodwarf5 | 1.27.2 / none / missing / none | same | yes |
| pro-esbuild-0.27.7; pnpm; `c638273fcf95573c` | none (no build-info record) | hand prediction: no version, no route | no version; analyzer errors `unable to get GoRttiMapper` | yes, by absence of lines; not a discriminating route test |
| pro-op; `/usr/bin/op`; `f4ac474fd0202c73` | go1.26.8 | 1.26.8 / none / missing / none | same | yes |

Limits:
- One host, one REA version (6.5.0), one provider (Ghidra 12.1.4), one run per carrier; all eight are x86-64 Linux ELF. No determinism claim beyond the two repeated Evidence IDs (`calib-shfmt` `ev_2b29a1dd…`, `calib-esbuild-0.25.12` `ev_391dbfe6…`, both matching the pilot).
- Log capture is a polling copy; absence claims hold only up to the last retained line.
- Pins prove equal bytes at the pre and post instants. `carrier-run.py` performs a mid-run check every 30 s but records only a changed result; no mid-run map or check count is retained at `da64646`.
- The 8/8 result counts exit codes. `snapshot_label` is non-discriminating (request echo). The `pro-esbuild-0.27.7` row matches by absence of lines.
- Out-of-range carriers (1.26.8, 1.27.0, 1.27.2) show missing-base bootstrap failure. On this host the declared range and installed bases cover the same minors, so the advisory range check is not separated from the missing base by these runs.
- No Go 1.27 symbol recovery is claimed. Patched-content correctness, the cause of the aether EOF, and fallback-data effects are not established.
- Author-side evidence only; not outside verification and not a promotion.

Stagnation: `{stagnation_before}/10` → `{FINAL:stagnation after}/10`. The last explicit counter in the lane is `3/10` at `SCORECARD.md:1500`; round 14 reset the capability interval (`SCORECARD.md:2226`); round 15 and round 16 entered no capability and no reset (`SCORECARD.md:2248`, `:2317`). [INFERENCE: pre-round counter 2/10; L1 must confirm from the full history.] An entry resets to 0/10; no entry gives 3/10.

### Executed controls and frontier

- `controls.py b563c79 da64646`: exit 0 at `da64646`; final `{FINAL:controls exit}` at `{FINAL:REV}`. Old-prefix, frozen-blob, verifier and QUALITY checks as listed under operability above; no semantic audit.
- `measure.py da64646`: exit 0 at `da64646`; `{FINAL:measure exit}` at `{FINAL:REV}`. Run receipts 8; SOURCES rows 23→30.
- Invocation audit: `invocation-audit.py --root <LANE> --rev da64646` gives 17 rows, 6 exercised_match, 11 unlabelled_variant (baseline 7 rows, 5 exercised_match, 2 unlabelled_variant). Final `{FINAL:invocation counts}`.
- Swarm (committed evidence): W1 spawned 78 seats (executor14/scout20/reviewer12/scribe10/connector8/critic6/revenger4/sentinel2/simplifier2; `LOG.md:2051`); dispatch refused twice at the host job cap (78 each) and spawned on the third identical attempt (`wave1-dispatch-attempts.json`). Completion of the 78 seats is `{FINAL:W1 completion evidence}`: it is not evidenced by any committed registry field at `da64646`. No W2 result is cited because the W2 files are not committed. Refusals are retained, not replaced by passes. L1 holds the canonical planner seat; author seats are not outside reviewers.

Learning trends: **expansion unchanged** (same Go ground; the new evidence deepens route-level diagnosis of held Go code, not domain coverage). **Quality** {FINAL:quality verdict}. **Discernment** {FINAL:discernment verdict}; the two routed outside defects are carried as dated, line-exact corrections, and no outside sample was drawn in this round.

Planned: {FINAL:planned_next}. SHONEN stays `[~]`. No promotion, no `[x]`, no outside verification by author seats, and no following round started here.
