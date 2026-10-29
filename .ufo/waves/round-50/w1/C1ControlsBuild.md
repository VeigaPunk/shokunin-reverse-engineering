# C1ControlsBuild — R50-C1 control fixtures and driver (wave 1, pre-freeze)

Seat `C1ControlsBuild`; lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. No `--data-run`, no write outside `.ufo/waves/round-50/w1/C1ControlsBuild*` and scratch `/fast/scratch/hyaku/kaidoku-r50/C1ControlsBuild` (removed at the end). Tools installed: none. Vendor bytes: one image downloaded to scratch (`FRITZ.Box_7530-08.25.image`, sha256 `b17fe5cd…35e9c`, matches the L1 probe), carved to the carrier `e822655a…199e` (34 003 969 B, equals `C1CarrierSelect`'s pin); nothing vendor is in the lane tree.

## Verdict

**Built and exercised; the controls work as designed against the draft port, and they find four plan-level defects the L1 must resolve before the freeze.** Against the draft round-50 counter (`C1CounterPort`, snapshot sha256 `716287fe77b30daa2d67b57b57e129196d20d6f7e328fa8d7667d6fcd974c305`) on a synthetic rehearsal lane, all eight arms behave, POS reaches exit 0 with `carriers_matched 4`/all bindings true, and CTL-C1-4 fails **exactly** `layout_ok` with `carriers_matched 3/4`. Against the round-41 counter as the stand-in on the round-41 freeze, five of six arms behave and CTL-C1-2 **does not** go red on the two carriers a real REA rerun can be compared on (a genuine finding, not a driver bug). Not run: any score against the *final* round-50 counter or the four real vendor carriers (the counter is mid-port; the host is at load 48-72 so REA's fixed 120 s deadline cannot be met for a7530/a7590).

## Findings the L1 must act on (most important first)

| # | finding | evidence |
|---|---|---|
| F1 | **A counter-time REA rerun that times out is scored `projection_ok` false**, indistinguishable from a forged receipt. REA 6.5.0 has a fixed `FIRMWARE_LIMITS.timeoutMs = 120000`; a7530 takes 48 s on a quiet host (7 CPU-min) and 126-129 s at load 50-60. On the draft port every projection verdict at load ~50 was a `provider_timeout` (even the genuine POS receipt went red). The port should return exit 2 for `projection_error`; the driver already refuses to credit those verdicts (`could_not_evaluate` for c2/c2x/pos, and c4/c1b on the swapped slot). Run `gen`/`score`/the data run on a quiet host. | `receipts/out-r50b/{pos,c2,c2x,c1}/counter.json` (`projection_error.error.code = provider_timeout`, `timeout_ms 120000`); `receipts/score-r50b.log`; a7530 gen retries `[126.4, 129.3, 127.7, 126.4, 126.2] s` (`gen --controls pos` at load 51-62); quiet run 48.05 s, `user 7m12s` |
| F2 | **REA default budgets fail a7530** (`Staging entry budget exceeded (10000)`; 15 150 inodes, 13 366 regular, 172 089 096 B). Needs `--max-depth 1 --max-output-files 100000 --max-output-bytes 536870912` (both are schema maxima; 536870912 is the cap for bytes). Receipt 6 065 003 B; handler `squashfs_v4_le`, 13 366 files, partial, 852 unpublished entries, 5 `MaliciousSymlinkRemoved`. REA's report cap is 8 MiB (`FIRMWARE_LIMITS.reportBytes`) — a7590 should be checked. Sent to L1 and `C1RunPort`. | `receipts/a7530-rea-probe.txt` (the three runs, exit codes, timings); planted values in `control-fixtures-a7530-draft/pos/manifest.json` `captured[0]` |
| F3 | **CTL-C1-2 is red only through facts the oracle does not carry.** Stand-in (round-41 counter): the oracle-only forgery of the lane-built carriers L3/L4 is **green on all 19 clauses incl. `projection_ok`** → `carriers_matched 2`, control `misbehaved`. Rehearsal lane **without** a link chain REA removes: forgery `carriers_matched 4/4`. Rehearsal lane **with** the chain (`lib/libx.so*` ending at an absolute target): forgery red on exactly `projection_ok` on all four slots. The extra arm **c2x** (same forgery + the `MaliciousSymlinkRemoved` rows read off a published receipt, no REA run) reaches `carriers_matched 4/4` with every per-carrier clause true. All four frozen carriers have ≥ 1 removed link (`C1OracleBuild/chain.json`: 5,5,1,1), so plain c2 is red on real data, but the plan's "red: rerun projection / evidence id" is wrong on the id (the driver re-mints it) and its limit (3) should add "an oracle forgery that also copies the removal diagnostics equals a real run". | `receipts/out-r41/c2/receipt.json` (`carriers_matched 2`, L3/L4 `[]`); `receipts/out-small/c2/receipt.json` (`projection_ok` x4, `attributed_alone` empty); `receipts/out-small/c2x/receipt.json` (`carriers_matched 4`) |
| F4 | **CTL-C1-1 cannot trip the layout clause**: a receipt has no superblock. c1 trips `subject_pin_ok`, `handler_ok`, `run_provenance_ok` (+`parameters_ok`, path clauses) on every slot (rehearsal, all four slots). Extra arm c1b (BE carrier `L3` + its verbatim round-41 receipt in slot 0) is **refused** by the draft counter: exit 2 `oracle_env_error` (its independent `unsquashfs` arm reads a different-endian file). Change the plan text to "(red, subject/handler/provenance clauses)" or decide c1b's refusal is the intended reading. | `receipts/out-small/c1/receipt.json`, `.../c1b/receipt.json` (`stdout_tail`) |
| F5 | The port **binds the running counter to its blob at the freeze** (`counter_not_frozen`, exit 2) — any control scoring needs the counter committed at `tools/round-50/c1-counter.py` in the freeze; the driver takes `--counter <LANE>/tools/round-50/c1-counter.py`. | observed on the first small-lane score (counter not committed in the lane: `c0`/`pos` stdout `reason counter_not_frozen`, exit 2; 8 of 8 arms flagged); that run is not saved as a receipt, the fix (counter committed at its path) is in `mk-rehearsal-lane.py` and every saved score was made with it |
| F6 | Kill rule wording: "the do-nothing tree scoring any carrier clause green" cannot be literal (`carrier_present`, `carrier_pin_ok`, `carve_ok`, `layout_ok` are legitimately green with no receipt). Implemented as "any receipt-derived clause" (`RECEIPT_CLAUSES` in the driver). | `receipts/out-small/c0/receipt.json` `diag.receipt_clauses_green {}` |
| F7 | A counter crash exits 1 (Python traceback), the same code as "not met"; the driver requires a parseable verdict, so a crashing counter makes every control `misbehaved` rather than "as expected" (seen on the mid-edit port: `NameError: OPENED`). | observed on the first draft-port score (`stderr_tail ... NameError: name 'OPENED' is not defined`, exit 1, 5 of 5 arms `misbehaved: no readable verdict`); not saved as a receipt; the judge behaviour is the `judge()` branch `the counter wrote no readable verdict` |
| F8 | `DevArmA` receipts are for the **uncarved 34 005 000-byte member** (subject digest `df6c22dd…`, an extra 8-byte chunk at 34004992): not valid positive-control receipts for the carved pin. `gen --pos-envelopes` refuses any receipt whose subject digest is not the carrier pin. | `C1DevArmA/receipts/7530-big.envelope.json.gz` subject; `--pos-envelopes` refusal in `c1-controls.py:import_receipt` |

## What was built

Under `.ufo/waves/round-50/w1/C1ControlsBuild/tools/round-50/`:

| file | sha256 | purpose |
|---|---|---|
| `c1-controls.py` | `bca264c1b385559290d649b7f7fbee4f7bbc343b4b280aa14ba0f6da557f5bfb` | `gen` / `score` / `selftest`; stdlib; `--counter`, `--lane`; constants scraped from the counter by AST |
| `mk-rehearsal-lane.py` | `1e4e2452f5e61b8fbba1d02c5a6b1c501a8ec4457d03ddd3711a1d5965e834b2` | throwaway lane of four synthetic LE AVM-marker carriers + the counter under test at its frozen path |
| `control-fixtures/README.md` | (see file) | which clause each control must trip; procedure; plan-wording corrections |
| `control-fixtures-rehearsal/` | — | `gen` output on the rehearsal lane (212 KB) |
| `control-fixtures-a7530-draft/` | — | `gen` output on a 1-carrier table of the REAL a7530 carrier (2.4 MB; c3 and c4 are real REA captures, pos is my own genuine REA receipt imported through `--pos-envelopes`) |

Controls (README has the clause table): c0 do-nothing; c1 round-41 BE receipts verbatim (`from_lane` + sha pin, no copy); c2 oracle-only fabrication, id re-minted through the frozen xpin; c3 real capture with `sasquatch` removed from a REPLACED child PATH; c4 round-36 `K1` carved to `bytes_used` (70 482 B, `hsqs`, xz, `mkfs_time 0`) re-pinned into slot 0 of a sandbox freeze, genuine receipt, other slots hold the genuine pos receipts; pos real receipts + landing blocks applied to the freeze bytes at score time. Extras (off by default): c1b, c2x. Fixtures are gzip (mtime 0) + a manifest of sha256/size; score refuses a fixture that does not hash to its manifest or (inside the lane) differs from the freeze blob.

## Commands and receipts (all UTC 2026-10-29 01:0x; scratch removed afterwards)

`receipts/final.log` is the transcript of the final pass; each control's `receipt.json` carries `command`, `exit_code`, `stdout_sha256`, `utc`.

| check | command (abridged) | exit | result |
|---|---|---|---|
| driver selftest | `python3 -I -B c1-controls.py selftest --work $S/st3` | 0 | 20/20 (`receipts/selftest.json`) |
| rehearsal lane | `mk-rehearsal-lane.py --lane $S/clone --base-rev 7c678ae6… --counter port-snapshot4.py --gap-rule C1GapRule/gap-rule.json --out $S/small` | 0 | freeze `a20083eb247c3427f135d7144d366b9da702aabd` (`receipts/small.json`) |
| gen (rehearsal) | `c1-controls.py gen --lane $S/small --freeze a20083eb… --counter port-snapshot4.py --pkg65 …/rea-agents --controls c0,c1,c1b,c2,c3,c4,pos,c2x` | 0 | 8 generated, 24 s |
| **score (rehearsal, draft port)** | `c1-controls.py score … --controls c0,c1,c1b,c2,c2x,c3,c4,pos` | **0** | `failures []`, `kill_rule_fires false`; summary sha256 `cb06c074…8da8` |
| gen (stand-in) | `gen --lane $S/clone --freeze d764389e… --counter tools/round-41/c1-counter.py --pos-from-lane --controls c0,c1,c2,c3,c4,pos` | 0 | 6 generated |
| **score (stand-in = round-41 counter)** | `score … --controls c0,c1,c2,c3,c4,pos` | **1** | `failures ["CTL-C1-2"]` (F3); summary `a8f55492…4785` |
| driver mutation: always-green counter | `STUB_MODE=green score … --counter stub` | 1 | c0,c1,c2,c3,c4 `misbehaved`, **kill rule fires** (c0,c1,c4), POS ok; `eada120d…9046` |
| driver mutation: always-red counter | `STUB_MODE=red score …` | 1 | POS `misbehaved`; c0 and c2 still "as expected" (an always-red counter satisfies them — POS is the only guard); `c367a423…7764` |

Per control, rehearsal lane (draft port), `receipts/out-small/<k>/receipt.json`:

| control | exit | `carriers_matched` | clause result | stdout sha256 prefix |
|---|---|---|---|---|
| c0 | 1 | 0 | 6 doc bindings false; no receipt-derived clause green | `0b09a215` |
| c1 | 1 | 0 | every slot: `subject_pin_ok`, `handler_ok`, `run_provenance_ok`, `parameters_ok`, `gaps_ok`, `oracle_hits_ok`, `nonregular_unpublished_ok`, `projection_ok` | `770a03ea` |
| c1b | 2 | — | refused: `oracle_env_error` (accepted as "not a match") | `0edf7325` |
| c2 | 1 | 0 | every slot exactly `projection_ok` | `abab0cf9` |
| c2x | 1 | **4** | no clause false (informational; F3) | `fdc7e672` |
| c3 | 1 | 0 | slot a7530: `chunks_ok`, `gaps_ok`, `nonregular_unpublished_ok`, `oracle_hits_ok`, `projection_ok`; planted gap kind `missing-extractor-dependency` | `5f62ad54` |
| c4 | 1 | **3** | slot a7530 exactly `layout_ok`; other three slots `[]`, `matched == 3 == other slots planted` | `a69f3cee` |
| pos | 0 | 4 | all clauses, all 9 bindings true | `13766b04` |

Stand-in (round-41 counter; BE handler, round-41 constants; `V3`/`V4` bytes absent so those slots are red on carrier clauses by construction): c0 exit 1 / 0; c1 1 / 0 (`subject_pin_ok`); **c2 1 / 2 (L3, L4 green: misbehaved)**; c3 1 / 0 (L3 capture without `sasquatch-v4be`); c4 1 / 2 (slot V3 `layout_ok`+`handler_ok`+`carve_ok` — the BE counter cannot isolate a LE standard carrier, so exactness is asserted only when the handler is LE); pos 1 / 2 (L3, L4 matched, all six doc bindings true; `compression_coverage` needs V3/V4 bytes).

## Limits of this evidence

* The rehearsal carriers are synthetic; they prove the pipeline, not the vendor images. The real a7530 was exercised for generation only (`control-fixtures-a7530-draft`: c0,c1,c1b,c2,c3,c4,pos,c2x generated in 8.6 s because the heavy REA is imported; c3 and c4 are genuine REA captures; not scored, load).
* The draft port was mid-edit; layout/handler names are taken from its constants, not from a frozen counter. `CLAUSE_ALIASES` in the driver is the one table to align (`layout_ok`, `parameters_ok`, `carrier_fresh_ok`, … are the draft's names).
* POS landing text is a fixture written to the port's documented regexes (`AVM marker`, `LE AVM`/`AVM-LE` token searched with the stem removed, `OPENED_DATES`); the real landing is the L1's.
* c4's table swap assumes the port keeps the committed `path` branch for non-external carriers (it does in the draft); the swapped carrier is also placed in the control's carrier cache.
* The a7530 gen/REA runs happened at load 48-72; only the F1 retries (5 × `provider_timeout`) and the quiet 48 s run are timing evidence.

## Open decisions (for the L1)

1. Resolve F3/F4 in the plan text (limit (3) and the CTL-C1-1 wording); decide whether c1b and c2x enter the frozen default set (c2x is informational and cannot be red by design).
2. Have the port treat `provider_timeout` as exit 2 (F1) before the freeze; the controls need a quiet host.
3. Commit `tools/round-50/control-fixtures/**` (gen on a quiet host with all four carriers cached; est. ~9 MB gzip incl. c2x, ~2.4 MB for one carrier as measured) with the freeze and score with the lane's own counter.
