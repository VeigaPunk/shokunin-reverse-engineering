# R40W2C1Mutants — mutation test of the C1 counters (round 40, wave 2)

**Verdict: DEFECTS FOUND** — 3 `--selftest` coverage gaps (external-carrier load path untested; oracle row-compare only pinned by count deltas; `frontier_content`'s `supersede` conjunct never isolated) and 1 scoring nondeterminism hazard (a transient REA no-data rerun silently demotes `projection_ok` instead of raising `rerun_env_error`). **The frozen verdicts themselves were not overturned**: both counters reproduce the frozen receipts byte-for-verdict at `42c10a58`, 17/20 mutants are selftest-killed, and every mutant that moves the real verdict except the selftest-caught M16 only *deepens* the honest stop. Attacked: the load-bearing clauses of `tools/round-40/c1-counter.py` and `tools/round-40/c1-extra.py` as frozen at `42c10a58cb2cae3a4a0122af35a0cf95ac718043` (bytes `8d288e4c…f17e81`, `5ba40129…f7fbb0`), via 20 single-logic mutants, each run through its own `--selftest` **and** a real scoring run at the measured revision in a sandbox with a rebuilt vendor cache.

## Method

- Sandbox: `git clone --shared` of the lane into scratch, `checkout 42c10a58…`; `git rev-parse --show-toplevel` asserted equal to the clone before any fixture work. Lane VCS untouched (read-only `git show`/`diff` only); mutant bytes were written only into the **clone's working tree** (`git show REV:path` is all the counters read, and `frozen_drift` reads `git log`, not the worktree, so mutants cannot self-trigger the drift binding). Pristine bytes restored + sha256-asserted after **every** mutant run.
- Vendor cache rebuilt: `python3 -I -B tools/round-40/fetch-vendor.py --root <sandbox> --rev 7fce3086… --cache $S/cache` → exit 0; V1 `ac4098bd…8e95` (5 442 392 B) and V2 `5ccc7614…089b` (26 013 550 B) both pin-matched. Bytes stayed in scratch (AVM licence); cited by sha256 only.
- Real verdict command (per mutant, on the mutated clone working tree):
  `python3 -I -B tools/round-40/c1-counter.py --root <sandbox> --rev 42c10a58… --freeze 7fce3086… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --carrier-cache <cache> --json-out …` (c1-extra: `--base fa6a8a3f…` instead of `--pkg65`).
- Baseline reproduced before the campaign: counter selftest **70/70** (`green_ok 5, red_ok 65`), real verdict **exit 1, matched 3/4, only L2 fails `nonregular_unpublished_ok`**, `carriers_unchanged`/`gap_rule_unchanged` true, drift `[]` — identical to `.ufo/waves/round-40/l1/scores/c1-at-42c10a58.json`; extra selftest **7/7**, real verdict **exit 0, met true, all four carriers `ok`** — identical to `c1-extra-at-42c10a58.json`.
- Mutants: each replaces exactly one occurrence of one logic-bearing expression (`src.count(old)==1` asserted); diffs in `mutants/`. Generator + driver in `scripts/`.

## Mutant table (baseline = exit 1, matched 3/4, failing = L2 `nonregular_unpublished_ok` only)

| id | clause attacked | selftest kills? | real verdict changes? | missing selftest case |
|----|----------------|-----------------|----------------------|------------------------|
| M01 | `layout_ok` LE walk: ambiguity guard dropped | KILLED — `metadata length plausible both ways (no identity)` | no | — |
| M02 | `layout_ok`: AVM marker inverted (`!=`) | KILLED — `green (4 AVM carriers…)` | yes: matched 3→0, `layout_ok` fails all four (stop deepens) | — |
| M03 | `gaps_ok`: structural allowance opened (`if False:`) | KILLED — by **crash**: `KeyError: 'depth-limited'` in the `over` comprehension (`selftests/st-M03-rerun.err`) | no | note: st3 `path-less gap kind with no structural allowance` dies as a crash, not a clean red |
| M04 | `gaps_ok`: structural allowance strictened (`>=`) | KILLED — `structural gap within its frozen allowance` | yes: matched 3→0, `gaps_ok` fails all four (each carries exactly 1 `depth-limited` = the frozen allowance) | — |
| M05 | required-gap default turned off | KILLED — `required gap missing (symlink materialised)` | no (real `gap-rule.json` pins `required.symlink=true` explicitly) | — |
| M06 | `same_rel`: suffix matching dropped | KILLED — `green` | yes: matched 3→0 (`oracle_hits_ok`+`gaps_ok` all four) | — |
| M07 | `oracle_hits_ok`: hit count vacuous (`>= 0`) | KILLED — `oracle file missing from the published set` | no | — |
| M08 | projection `rel_suffix`: keeps chunk extract dir | KILLED — `green` | no [INFERENCE: committed receipts and counter reruns share the same extract-dir stem `firmware.bin_extract` at this revision, so keeping the prefix preserves equality; the suffix rule is only exercised by the selftest's rehost model] | — |
| M09 | `projection_diff`: always-equal | KILLED — `oracle-only fabrication with re-minted evidence id` | no (latent: a same-handler fabrication on L1/V1/V2 would now pass at scoring time; L2 still fails `nonregular_unpublished_ok`) | — |
| M10 | external-carrier load: cache key truncated to 32 hex | **SURVIVED** (70/70 pass) | yes: matched 3→1 (V1+V2 `carrier_present/carrier_pin_ok/layout_ok/projection_ok` all fail) | **any `external`/`--carrier-cache` fixture at all** — the selftest only ever uses `path` carriers |
| M11 | `frozen_drift` spec keys drop `nonregular` | KILLED — `nonregular table changed after freeze: want 2 got 1` | no | — |
| M12 | `receipt_fresh` accepts a freeze-commit add | KILLED — `receipt added at freeze: want 1 got 0` | no | — |
| M13 | `handler_ok`: any handler | KILLED — `chunk handler is the LE handler` | no | — |
| M14 | `chunks_ok`: failed flag blinded (`is None`) | KILLED — `failed chunk` | no | — |
| M15 | `sourced` binding: opened-date check dropped | KILLED — `source row opened earlier` | no (campaign run hit a transient REA no-data on V2 — see Finding C2; two re-runs under the mutant reproduce the baseline verdict exactly) | — |
| M16 | `met_target` gate: `carriers_matched == target` dropped | KILLED — `do-nothing (freeze files only): want 1 got 0` | **INVERTED: exit 1→0, `met_target` true at matched 3/4** — the honest stop would have been scored MET | — |
| E01 | `oracle_rederived`: row compare → row counts | **SURVIVED** | no (gate stays green) | equal-count content edit of `oracle.tsv` (the only red case, `trimmed-oracle`, differs in count) |
| E02 | `sourced_new`: base-absence check dropped | KILLED — `old-sid-with-used-by` | no | — |
| E03 | `oracle_rederived`: pin compare broken (`.upper()`) | KILLED — `green` (the pin check is shared by the `path` branch) | yes: gate flips 0→1 (`met` true→false, all carriers "pin mismatch") | — |
| E04 | `frontier_content`: `supersede` requirement dropped | **SURVIVED** | no | a red line carrying mark+heading+stem but **no** supersede word — `presence-only-frontier-note` lacks *both* heading and supersede, so the conjunct is never isolated |

Score JSONs: `scores/base-*.json` (pristine), `scores/mut-<id>-*.json` (per mutant), `scores/restored-*.json`, `scores/sum-<id>.json` (driver summaries), `scores/mut-M15-rerun{1,2}.json` (stability re-runs). 16 counter + 4 extra mutants; generator asserts single-occurrence patches.

## Findings

- **F1 (M10, coverage):** the external-carrier load leg (`external` + `--carrier-cache`, i.e. how V1/V2 bytes enter the counter) has **zero selftest coverage**. A mutant that breaks vendor-byte loading passes 70/70. Scoring still notices functionally (verdict moves), so this is a regression-suite hole, not a live hole — but nothing in `--selftest` would catch a subtler loader regression.
- **F2 (E01, coverage):** c1-extra's `oracle_rederived` red case is count-differential only; a future weakening of the row compare to counts passes its own selftest and leaves the gate green. Backstopped elsewhere: the main counter's `oracle_hits_ok`+`projection_ok` bind oracle content to published files and to a fresh run.
- **F3 (E04, coverage):** the `supersede` conjunct of `frontier_content` is enforced **only** by c1-extra (c1-counter's `frontier_note` checks mark+stem+AVM-layout token, not supersession), and the selftest never isolates it. A landing note without any supersession wording would pass `--selftest`; the pristine gate does still reject it at scoring time.
- **C1 (M16, calibration):** the whole NOT-MET verdict funnels through the single `carriers_matched == target` term of `met_target`. One token flips the honest stop into MET at 3/4. The selftest's `do-nothing` case catches it — that case is the only defense, and it holds.
- **C2 (M15 run 1, nondeterminism):** observed once: the V2 rerun returned JSON with `ok:false, exit 1, stderr ''` and the counter recorded `projection_ok:false` with a `projection_error` payload — **not** `rerun_env_error`/exit 2. A single unlucky REA run would have changed the frozen score from "3/4, L2-only" to "2/4, V2+L2" without any code or data change. Two immediate re-runs under the identical mutant were clean, so the frozen all-`projection_ok:true` receipt was not affected; but score receipts carry a nondeterministic failure mode that is silently folded into `matched`.
- **C3 (M04, calibration):** all four carriers carry exactly one structural `depth-limited` gap against a frozen allowance of exactly 1 — the verdict sits on the `>` vs `>=` boundary of the allowance check. The boundary is load-bearing and currently correct.
- **C4 (M06/M08, calibration):** the L2 false positive (`usr/bin/busy` published regular file suffix-matches the `bin/busy` symlink row, per L2 `nonregular.tsv`/`oracle.tsv`) cannot be repaired by dropping suffix matching — that breaks `oracle_hits_ok` everywhere (M06). The honest stop genuinely hinges on `same_rel`'s suffix semantics; any fix must be narrower than exact-match. And per M08, projection equality does not currently depend on the suffix normalization at all (shared extract-dir stem), so `rel_suffix`'s stripping is defensive only at this revision [INFERENCE, see table].

## Restoration evidence

- Per mutant: pristine bytes rewritten and sha256-asserted after the run (`sum-<id>.json: restored_sha256`); final campaign line "target bytes pristine".
- Post-campaign detector runs on restored bytes: counter exit 1 / matched 3 / L2-only — identical to baseline; extra exit 0 / met true — identical to baseline (`scores/restored-*.json`).
- Lane bytes before and after the campaign: `tools/round-40/c1-counter.py` `8d288e4cf203d74557aa81df556d6a95c1bcde99acabf189638c4142b6f17e81`, `tools/round-40/c1-extra.py` `5ba40129f5ec96448c217e4fb22c885dff85fee4745c39389caf6cf6cab7fbb0` — unchanged; no VCS mutation anywhere (fixture clone only).

## Tooling and limits

- No tools installed or upgraded; no pacman transactions. Used host `python3 3.14`, `node v24.21.0`, `npx 11.19.0`, the pinned `rea-agents@6.5.0` package root, and the existing `~/.local/bin/unblob` + `sasquatch-v4be` (untouched, never reinstalled or moved). No subagents, no `agent://all`.
- Real-verdict runs execute the full rerun clause (real REA per carrier, ~9 s wall each at `--max-depth 1` replay). One transient REA failure observed in 20×4 reruns (Finding C2) and re-characterized with two clean re-runs.
- Vendor firmware bytes never copied into the lane; cited by sha256. Scratch removed after artifact copy.
