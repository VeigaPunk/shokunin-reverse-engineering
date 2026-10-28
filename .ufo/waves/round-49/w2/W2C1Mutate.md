# W2C1Mutate — round 49 wave 2: C1 counter mutation falsification

## Verdict

The frozen counter (`tools/round-49/c1-counter.py`, blob `471e13cf6699841c9c395760af31b06fa76dbb93`, identical at FREEZE `decc5697…` and REV `29883d4e…`) reproduces its landing measurement: `--selftest` exit 0 (52 cases, `failures []`) and the C1 score exit 0 (`carriers_matched 4`, `target 4`, `failing []`, `bindings_false []`, `frozen_path_changed []`). Falsification of the five edit families found **two witness gaps that no control catches** (m01 provenance substring; m10 `core.quotePath`) and **three constant-to-round-48 mutants that the selftest cannot see** (m11–m13; only the landed-bytes score kills them). The other **eleven** mutants (m02–m09, m14–m16) were killed by `--selftest` with a named case; m14 and m16 are also red at score level, m15 is score-green by design.

Counter bytes were not modified; all mutants are scratch copies.

## Method

- Frozen copy: `git -C <lane> archive 29883d4e… tools/round-27 tools/round-49` extracted to `$S/base`; `sha256(c1-counter.py) = ac83715b…d287f`; `git hash-object` = `471e13cf…` = FREEZE blob.
- 16 single-point mutants, each a scratch copy of `base/` edited with the `edit` tool (diffs in `artifacts/mutant-diffs.txt`, one hunk each, verified).
- Per mutant: `--selftest` (offline) and the C1 score (real REA 6.5.0 rerun, `--root <lane> --rev 29883d4e… --freeze decc5697…`). Every counter run used `python3 -I -B`, `GIT_NO_REPLACE_OBJECTS=1`, scratch `--work`.
- Two targeted unit probes (`artifacts/probe.py`, `probe.out`) where the selftest and score are silent.
- No tracebacks in any stderr (`grep -c Traceback` = 0 for all 34 runs): every exit 1 is the counter's own verdict.
- Tools installed: none. Used existing `python3`, `git`, `node` v24.21.0, `unblob`/`sasquatch`/`unsquashfs` already on PATH.

## Baselines (UTC 2026-10-28, approx. 22:3x–22:4x)

| run | command (abridged) | exit | stdout sha256 | key result |
|---|---|---|---|---|
| base selftest | `python3 -I -B $S/base/tools/round-49/c1-counter.py --selftest --pkg65 $PKG --work $S/work/base-st` | 0 | `27f9604223e5d19ab2272b6beec66f4b4772a80a7d3666d92459408659e08b1f` | cases 52, green 1, red 51, failures [] |
| base score | `… --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 29883d4ec35a31a8393c4ffb220888c44c0bb022 --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --pkg65 $PKG --json-out …/base-score.json` | 0 | `ae830b210a799c2b5ec6a67dd629562f0b170e46574f3b70646003f6b6b64657` (stdout); receipt `70925186880fe0906a8f904cf5390d4592f0b97d6c12b45bc626f4d4ea16e35d` | carriers_matched 4, failing [], bindings_false [], frozen_path_changed [] |

Score receipt and selftest/score stdout for every run: `artifacts/out/`.

## Findings table (16 mutants)

sel = `--selftest` exit; score = C1 score exit; sha = first 16 hex of the stdout sha256 (full list in `artifacts/out/*.stdout`; mutant counter sha256 in `artifacts/mutant-sha256.txt`).

| id | edit (base → mutant) | sel | selftest case that fires / note | score | score failing | verdict |
|---|---|---|---|---|---|---|
| m01 | `provenance_ok`: `output_directory.startswith(PROV_BASE)` → `PROV_BASE in output_directory` | **0** | none | **0** | [] | **SURVIVES both (witness gap)**. Probe: `/tmp/a/fast/scratch/hyaku/kaidoku-r49/x` base False / m01 True; `/home/u/lane/fast/scratch/hyaku/kaidoku-r49/x` False / True |
| m02 | `provenance_ok`: drop `..` test (CUT 1189–1190) | 1 | "receipt path climbing out of the run (.. provenance)" | 0 | [] | killed by selftest |
| m03 | `provenance_ok`: segment substring `PROV_SEGMENT in` | 1 | "provenance under /tmp is refused", "segment inside a lane path" | 0 | [] | killed by selftest |
| m04 | quiet rule: `quiet_ok = True` | 1 | "unpublished-entries row on a carrier with no non-regular member"; "a gap … trips the quiet rule" | 0 | [] | killed by selftest |
| m05 | quiet rule: drop `unpub` term | 1 | "unpublished-entries row …" (v1le) | 0 | [] | killed by selftest |
| m06 | quiet rule: drop `gaps(env)` term | 1 | "a gap … trips the quiet rule" (v2be) | 0 | [] | killed by selftest |
| m07 | quiet rule: `not (nonreg and …)` (inverted) | 1 | both quiet cases | 0 | [] | killed by selftest |
| m08 | `frozen_drift`: added file under frozen prefix ignored (`if False:` at 1675) | 1 | "a NEW file added under tools/round-49/ after the freeze" | 0 | [] | killed by selftest |
| m09 | `frozen_drift`: whole `A` branch disabled (`if False:` at 1671) | 1 | same NEW-file case | 0 | [] | killed by selftest |
| m10 | `frozen_drift`: drop `-c core.quotePath=false` | **0** | none | **0** | [] | **SURVIVES both (witness gap)**. Probe: added `tools/round-49/ä.py` after FREEZE → base `["tools/round-49/plain.py","tools/round-49/ä.py"]`, m10 `["tools/round-49/plain.py"]` (miss) |
| m11 | `CORE_HEADING` → `## Round-48 additions to Core` | **0** | none (selftest fixtures take the same constant) | 1 | bindings_false: `province_core_section`, `province_core_row` | selftest survivor; killed only by landed-bytes score |
| m12 | `FRONTIER_MARK` → `Round-48 frontier note` | **0** | none (fixture uses constant) | 1 | bindings_false: `frontier_note` | same |
| m13 | `STEM` → `2026-10-28-r48-…` | **0** | none (fixture uses constant) | 1 | bindings_false: `frontier_note`, `coverage_map_row` | same |
| m14 | `PROV_BASE` → `/fast/scratch/hyaku/kaidoku-r42/` | 1 | green case; "provenance of another round (/kaidoku-r42/)" | 1 | all four `run_provenance_ok` | killed by both |
| m15 | `PROV_BASE` → `/fast/scratch/hyaku/` (round-agnostic) | 1 | "provenance of another round (/kaidoku-r42/)" | 0 | [] | killed by selftest only (score green as expected: real receipts pass a looser prefix) |
| m16 | `TARGET = 4` → `5` | 1 | green case | 1 | bindings_false: `carriers_spec_ok` | killed by both |

Sha256 prefixes (selftest stdout / score stdout), from the runs:
m01 `0f2a0f0f6b2fb678` / `ae830b210a799c2b`; m02 `64c4af3c2ce716c0` / `ae830b210a799c2b`; m03 `b6e7584f7249c5bf` / `ae830b210a799c2b`; m04 `582d239b042a34c2` / `ae830b210a799c2b`; m05 `cddd71df5ad3bb27` / `ae830b210a799c2b`; m06 `ed2c90c2190d1924` / `ae830b210a799c2b`; m07 `999a21f4332654b8` / `ae830b210a799c2b`; m08 `af73ce3a0bffbd2b` / `ae830b210a799c2b`; m09 `ff572b0469c6585f` / `ae830b210a799c2b`; m10 `ccba2a882e8e20f8` / `ae830b210a799c2b`; m11 `4e053d62eb192985` / `d01d2a1f49a4260d`; m12 `2a7c463ee91c83e7` / `b6a53ccd4bcd22f5`; m13 `05ab3aedde9ff5c9` / `9c4b1af8a054c86f`; m14 `262042c05c57bab1` / `6d71727663cfe3df`; m15 `b7e58574fa5e9810` / `ae830b210a799c2b`; m16 `1ae64216e304be09` / `207930f12d795cb3`.

Reproduce one row: `python3 -I -B $S/mut/<id>/tools/round-49/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work $S/work/<id>-st`; score: same path with `--root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 29883d4ec35a31a8393c4ffb220888c44c0bb022 --freeze decc5697bfd4ec1e9de4a762ad199d9bd9c4230d --pkg65 … --json-out …`.

## Witness gaps (for the L1 to disclose; the counter is frozen and is not patched)

1. **G1 — provenance is not a prefix test in any control (m01 survives selftest and score).** `provenance_ok` is claimed as a prefix test in the plan (R49-C1 `run_provenance_ok`, and the plan's wave-1 disposition). The selftest case named `provenance under /tmp is refused (prefix, not substring)` uses `/tmp/kaidoku-r49/x`, which does not contain `PROV_BASE` (`/fast/scratch/hyaku/kaidoku-r49/`), so it cannot distinguish prefix from substring; the lane-path case uses `PROV_SEGMENT` and is not `PROV_BASE`-bearing either. The landed receipts carry proper prefixes, so the score cannot see it. Probe output shows the predicate differs (`artifacts/probe.out`). A relabelled receipt whose `output_directory` embeds the base inside a lane path would pass this clause.
2. **G2 — `core.quotePath=false` has no witness (m10 survives selftest and score).** Probe (`artifacts/probe.out`): a non-ASCII added file under `tools/round-49/` is reported by the base walk and missed by m10, because git quotes the whole path so `is_frozen` fails. No selftest case and no landed-tree path has a non-ASCII name, so the wave-1 disposition "C1 walk aligned (non-ASCII names)" is an unwitnessed claim in the counter.
3. **G3 — the selftest is self-referential for the round-49 constants (m11–m13).** `_province()` and `_readme()` (counter lines ~2768–2796) default to `CORE_HEADING`, `FRONTIER_MARK`, `STEM`, so renaming a constant renames the fixture too. Only the score's presence bindings on the landed bytes kill these; they are disclosed limit (2) of the plan, and they are the only control.
4. Score-level survivors m02–m09, m15 are expected: the landed data never exercises those clauses; they are witnessed only by selftest.

Not run: the wave-1 full single-point mutation census (35 of 75 survived per `w1/C1CounterMut.md`); not re-derived here. Controls CTL-C1-0..4 were not re-run (other seats).

## Artifacts

- `artifacts/out/` — every selftest and score stdout/stderr/exit, `base-score.json` (receipt), `base-selftest.stdout`.
- `artifacts/frozen-c1-counter.py` — the frozen counter copy used as base (`sha256 ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f`).
- `artifacts/mutant-diffs.txt`, `artifacts/mutant-sha256.txt` — exact mutant edits and sha256s.
- `artifacts/probe.py`, `artifacts/probe.out` (sha256 `75fae9027a258b57f04a978773fe7c1d8f82e3ed644954af176761c3639d7320`).
- Scratch `$S` removed after copy; the lane tree, FREEZE and REV were only read via `git archive` / `git show` / counter git reads.
