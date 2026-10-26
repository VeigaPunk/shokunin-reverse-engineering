# R36MutantC1 — mutation test of `tools/round-36/c1-counter.py` (round 36, wave 1)

Seat: R36MutantC1 (leaf, no subagents). Date: 2026-10-26. Judged axes: coverage, calibration.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`,
freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`).

## Scope and method

The frozen 14-case selftest of `c1-counter.py` is the behavioral detector. Protocol per mutant:

1. `cp` the pristine lane counter into seat scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36MutantC1`
   (layout `S/round-36/c1-counter.py` + `S/round-36/selftest/dev-*` + `S/round-27/xpin-attribute.mjs`,
   because `selftest()` resolves fixtures and xpin relative to the script's own directory).
2. Apply exactly one mutation to the **scratch copy** with a surgical string edit (lane file never opened
   for writing).
3. Run `python3 -I -B $S/round-36/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
   with `HYAKU_SCRATCH=$S TMPDIR=$S` (fixture repos and xpin scratch land in seat scratch).
4. Restore pristine bytes, verify sha256.

No REA CLI campaign run was needed: the selftest exercises only the committed dev fixtures and the
frozen xpin tool via `node`; `rea-agents` itself was never invoked (only its 6.5.0 package root is
passed to xpin for the evidence-id rule). No tools were installed or upgraded (operator authorization
2026-10-19 recorded as unused; no pacman transactions; sasquatch untouched). No VCS command touched the
lane; the only git activity was inside disposable fixture repos created by the counter's own selftest
under scratch.

## Baseline (pristine bytes)

```
$ python3 -I -B $S/round-36/c1-counter.py --selftest --pkg65 …/rea-agents
{"selftest": "c1-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}
EXIT=0
```

Pristine sha256 (lane file and scratch copy identical):
`5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5`.

## Results: 10 mutants, 8 killed / 2 survived

| # | Mutant (site in `c1-counter.py`) | Diff | Verdict | Killing case(s) (selftest `failures`) |
|---|---|---|---|---|
| M1 | `matched()` sha equality flip | `sha == fs` → `sha != fs` | **killed** | `green: want 0 got 1` |
| M2 | `matched()` suffix → substring | `fp.endswith('/' + rel)` → `('/' + rel) in fp` | **SURVIVED** | none in frozen suite — see finding F1 |
| M3 | drop evidence-id check | remove `and d.get('before_evidence_id_ok') and d.get('after_evidence_id_ok')` | **killed** | `forged oracle-copy envelope: want 1 got 0` |
| M4 | drop `before_oracle_hits == 0` | remove `and d.get('before_oracle_hits') == 0` | **SURVIVED** | none in frozen suite — see finding F2 |
| M5 | drop `carriers_unchanged` gate | `met_target = bool(res['carriers_matched'] == TARGET and bind_ok)` | **killed** | `carriers changed after freeze: want 1 got 0` |
| M6 | accept any heading | `section()` takes first `## ` line instead of `lines.index(heading)` | **killed** | `province row outside round-36 section: want 1 got 0` |
| M7 | accept S-id substring | `S\d{3,}` + trailing boundary → `S\d{3}` (entry token `S1070` matches registry `S107`) | **killed** | `S-id substring S1070: want 1 got 0` |
| M8 | ignore used-by | drop `and ENTRY in used` from registry-row condition | **killed** | `used-by lacks entry: want 1 got 0` |
| M9 | TARGET 4 → 3 | `TARGET = 4` → `TARGET = 3` | **killed** | `green: want 0 got 1`, plus `after := before (no sasquatch)`, `forged oracle-copy envelope`, `before := after`, `oracle changed after freeze` (all `want 1 got 0`) |
| M10 | off-by-one on oracle_files | `d['oracle_files'] = len(oracle)` → `len(oracle) + 1` | **killed** | `green: want 0 got 1` |

Raw selftest outputs (exit codes in parentheses):

```
M1  {"cases": 14, "green_ok": 0, "red_ok": 13, "failures": ["green: want 0 got 1"]}                     (1)
M2  {"cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}                                          (0)  SURVIVED
M3  {"cases": 14, "green_ok": 1, "red_ok": 12, "failures": ["forged oracle-copy envelope: want 1 got 0"]} (1)
M4  {"cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}                                          (0)  SURVIVED
M5  {"cases": 14, "green_ok": 1, "red_ok": 12, "failures": ["carriers changed after freeze: want 1 got 0"]} (1)
M6  {"cases": 14, "green_ok": 1, "red_ok": 12, "failures": ["province row outside round-36 section: want 1 got 0"]} (1)
M7  {"cases": 14, "green_ok": 1, "red_ok": 12, "failures": ["S-id substring S1070: want 1 got 0"]}       (1)
M8  {"cases": 14, "green_ok": 1, "red_ok": 12, "failures": ["used-by lacks entry: want 1 got 0"]}        (1)
M9  {"cases": 14, "green_ok": 0, "red_ok": 9,  "failures": ["green: want 0 got 1", "after := before (no sasquatch): want 1 got 0", "forged oracle-copy envelope: want 1 got 0", "before := after: want 1 got 0", "oracle changed after freeze: want 1 got 0"]} (1)
M10 {"cases": 14, "green_ok": 0, "red_ok": 13, "failures": ["green: want 0 got 1"]}                     (1)
```

M9 note (calibration detail): with `TARGET=3`, every red case that leaves exactly 3 carriers intact
flips to green — the target constant is load-bearing for 5 of the 13 red cases, not just the green one.

## Findings (coverage gaps in the frozen selftest)

### F1 — path-suffix matching is uncalibrated (M2 survived)

`matched()` accepts an oracle row when a published file equals `rel` or ends with `'/'+rel`. Weakening
that to substring containment (`'/'+rel in fp`) passes all 14 frozen cases: no fixture publishes a path
that contains `/<rel>` without ending in it. A receipt that publishes `dir/name.bin.tmp` (same sha256)
would be counted as publishing oracle file `name.bin` under the mutant.

Killability demonstrated on the scratch copy by adding one case (validated red-on-pristine first):

- `DEMO suffix-vs-substring renamed published path` — K1 `after.json` re-signed (evidence id recomputed
  with the frozen xpin tool) with published path `firmware.bin_extract/a.txt` renamed to
  `firmware.bin_extract/a.txt.tmp` (sha unchanged). Pristine 16-case run: `{"cases": 16, "green_ok": 1,
  "red_ok": 15, "failures": []}` exit 0. M2 16-case run: `{"cases": 16, "green_ok": 1, "red_ok": 14,
  "failures": ["DEMO suffix-vs-substring renamed published path: want 1 got 0"]}` exit 1.

(First attempt used an extra oracle.tsv row instead; it was masked by the `oracle_frozen` freeze-vs-rev
comparison, because case files are only varied at the data commit. The working discriminator varies the
after envelope, which is not freeze-checked.)

### F2 — the `before_oracle_hits == 0` half of the predicate is uncalibrated (M4 survived)

Dropping `before_oracle_hits == 0` passes all 14 frozen cases. The suite never constructs a before
receipt that keeps the sasquatch gap **and** already publishes oracle files: `before := after` is caught
by `before_sasquatch_gap is True`, `after := before` by the after-side gap check, and the forged case
mutates only `after.json`. So the "paired no-sasquatch receipt publishes none of them" clause is
enforced only in combination with the gap check, never on its own.

Killability demonstrated on the scratch copy by adding one case (validated red-on-pristine in the same
16-case run above):

- `DEMO before publishes oracle rows with gap kept` — K1 `before.json` = dev-before envelope with
  `normalized_result.files` set to oracle copies (`firmware.bin_extract/`-prefixed, shas from
  `dev-oracle.tsv`), `extraction_gaps` kept (sasquatch gap true), `evidence_id` re-signed to the
  recomputed value via the frozen xpin tool. M4 16-case run: `{"cases": 16, "green_ok": 1, "red_ok": 14,
  "failures": ["DEMO before publishes oracle rows with gap kept: want 1 got 0"]}` exit 1.

Both findings are suite-coverage findings, not counter defects: on pristine bytes the counter is
correct; the mutants only show which behaviors the frozen detector does not pin down. Per the kill
rule, the counter is not changed after the freeze commit — the fix path (if L1 wants it) is a 15th/16th
selftest case in a future round's freeze, not an edit to this one.

## Restoration evidence

- Lane file `tools/round-36/c1-counter.py` sha256 before first mutation and after all runs:
  `5533e17d022a7e25a442ec650743b3958a5c86a44a0194eed08fe3085e6581b5` (identical; the lane file was
  never written — every mutation was applied to the scratch copy).
- Scratch copy restored to pristine after every mutant run; post-restore sha256 matched
  `5533e17d…` each time (verified after M1–M10 and again after the demo runs).
- Seat scratch `/fast/scratch/hyaku/kaidoku-r36/R36MutantC1` removed at end of seat (selftest fixture
  repos are additionally removed per-case by the counter's own `finally` block).
- No sibling lane, fleet-repo, or `/home/vgpnk/Projects/shokuknow` file was written; no VCS-mutating
  command was run anywhere.

## Verdict

Frozen selftest: 8/10 menu mutants killed, 2/10 survived; with two added cases, 10/10 killable.
Detector quality on the frozen suite is good but not complete: the two unpinned behaviors are (F1)
strict path-suffix matching of published files against oracle rows and (F2) the before-receipt
publishes-nothing clause standing alone from the gap check.
