# R41W2C1Mutants — mutation audit of the frozen `c1-counter.py`

**Verdict: DONE** — 29 single-logic mutation probes on `tools/round-41/c1-counter.py` (frozen at `d764389e…`; scored against receipts at `e9a24d07…`). Baseline pristine passes both detectors (selftest 97/97, exit 0; real data `met_target` 4/4, exit 0). Of 29 mutants: **14 killed by the selftest**, **3 killed by the real-data counter** (M01, M09, M13 — all three also killed by the selftest), **2 inconclusive** on real data due to a transient REA/unblob rerun flake (M16, M22; clean reruns pass), **13 fully survived** both detectors. The real-data detector adds no unique kill beyond the selftest in this population; the 13 survivors (plus the 2 flaky reruns) are coverage findings — each names an untested clause branch below.

Attacked item: the C1 counter's round-41 clauses — exact-path rule, root derivation, disposition, removal projection, member/nested digest checks, carve length, frozen-path drift, oracle-hit equality, gap counts — on the frozen byte-identical copy of the counter, evaluated by the same two bounded detectors the claim scores with.

---

## 1. Method

1. **Baseline first** (pristine file, immaculate):
   - `python3 -I -B tools/round-41/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` → exit 0, 97 cases (12 green / 85 red; 6 path probes, 3 discriminating; 8 root probes; 7 spec probes). Recorded: `artifacts/R41W2C1Mutants/baseline-selftest.out`.
   - Real-data run mirroring `l1/score.sh`: `python3 -I -B …/c1-counter.py --root <LANE> --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f --pkg65 <PK> --carrier-cache /fast/scratch/hyaku/kaidoku-r41/cache --json-out baseline-real.json` → exit 0, `met_target` true, `carriers_matched` 4, every binding true, every rerun `projection_ok` true. Recorded: `artifacts/R41W2C1Mutants/baseline-real.json|.stdout`.
   - Baseline prerequisite verified: vendor cache pins (read-only reuse of L1's cache — no network fetch, no vendor bytes copied): `c4f74f54…f872a.bin` 30233394 B and `ce27ebca…087f.bin` 32720860 B; `sha256sum` equals both pins in the frozen `carriers.json`.
2. **Mutant generation** (26 loci, 29 probes — M01…M32 minus unused numbers): each mutant is the pristine file with exactly one logic change applied by unique-anchor replacement (generator asserted `src.count(anchor)==1`; `diff` verified single-hunk for every mutant). Full spec + predictions: `artifacts/R41W2C1Mutants/mutants-spec.json`; unified diffs: `artifacts/R41W2C1Mutants/unified.diff`.
3. **Detector runs per mutant** (both identical to baseline, same env `TMPDIR=<scratch>`, `HYAKU_SCRATCH=/fast/scratch/hyaku`, `python3 -I -B`):
   - Selftest: `--selftest --pkg65 <PK>` → exit 0 = not killed.
   - Real data: `--root <LANE> --rev e9a24d07… --freeze d764389e… --pkg65 <PK> --carrier-cache <CACHE> --json-out real-<ID>.json` (full counter, including live per-carrier REA 6.5.0 reruns) → exit 0 = not killed.
   - Because `--selftest` locates `xpin-attribute.mjs` relative to the script path, mutants ran from a scratch mirror `$S/fx/tools/round-41/<ID>/c1-counter.py` with `tools/round-27/xpin-attribute.mjs` copied at `$S/fx/tools/round-27/` (sha256 identical to the lane file `8ea638379a4397dfc901334767d8015c88b16cf36c7f86e6a5beaf03a5d7f708`). A first sweep placed mutants in a bare scratch dir and failed for *all* mutants (`xpin not found`); that sweep was discarded as environmental (invalid detector), not scored.
4. **Flake separation** (M16/M22): after their first real runs failed, both were rerun (mutated), plus pristine twice — `rerun-*.json|.out` in artifacts. See §3.

No tools were installed or updated (nothing needed: `npx -y rea-agents@6.5.0` and `~/.local/bin/unblob` pre-existing; tooling rules read, no transaction).

---

## 2. Results

`ss` = selftest exit (green/red of 97); `real` = real-data exit / `met_target` / `carriers_matched`; failing real clause(s) listed per carrier where `matched` false.

| ID | Mutated clause (single logic) | ss | ss killed | real | Failing real clause(s) | Verdict | Survivor → missing case |
|----|-------------------------------|----|-----------|------|------------------------|---------|--------------------------|
| M01 | `extract_rel`: exact whole-segment prefix → suffix matcher (R40-CL1 defect reintroduced) | 1 (0/83) | yes | 1 / F / 0/4 | `oracle_hits_ok` + `gaps_ok` on all 4 (gap rows fail to resolve; hits 0) | KILLED-BOTH | — |
| M02 | `strip_rel`: `lstrip('/')` removed (only `./` peeled) | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | no `/`-prefixed oracle row in any table; leading-slash branch dead on all data |
| M03 | `same_rel`: `strip_rel(rel)` normalization dropped | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | `strip_rel` is inert on real + selftest data (`./`/`/` prefixes never occur) |
| M05 | `receipt_paths`: `chunks[].input_path` contribution dropped | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | extract-root confirmation still reached via files; chunk input-path source untested |
| M06 | `squashfs_roots`: handler prefix match → exact `squashfs_v4_be` | 1 (12/84) | yes | 0 / T / 4/4 | — | KILLED-SS | prefix-vs-exact handler discrimination only exercised by selftest |
| M07 | `subject_root`: ambiguity branch ignored (`if roots:` returns first) | 1 (11/84) | yes | 0 / T / 4/4 | — | KILLED-SS | multi-root ambiguity only exercised by selftest |
| M08 | `subject_root`: `oracle_root` hint membership check dropped | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | frozen-table error branch (`hint not in roots`) untested — no hint in `carriers.json`, no red case |
| M09 | `disposition_check`: structural allowance `>` → `>=` | 1 (10/85) | yes | 1 / F / 0/4 | `gaps_ok`: `structural gaps over allowance {'depth-limited': [1, 1]}` on all 4 | KILLED-BOTH | — |
| M10 | `disposition_check`: gap path must match exactly 1 non-regular entry → ≥1 (multi-match allowed) | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | multi-match gap-path case untested (no two non-regular rows share a rel) |
| M11 | `disposition_check`: structural count increment dropped (`+1` → `+0`) | 1 (12/84) | yes | 0 / T / 4/4 | — | KILLED-SS | per-carrier structural count only guarded by the selftest (note string) |
| M12 | `disposition_check`: required default `bool(allowed.get(kind))` → `False` | 1 (12/84) | yes | 0 / T / 4/4 | — | KILLED-SS | device/fifo/socket disposition only guarded by the selftest |
| M13 | `disposition_check`: removal-kind acceptance inverted (`not in` → `in`) | 1 (11/84) | yes | 1 / F / 3/4 | `gaps_ok` on V4: `removal at 'lib/libbroadbandcfg.so' names a 'symlink' entry; removed.kinds is ['symlink']` | KILLED-BOTH | — |
| M14 | `disposition_check`: gap ∧ removal exclusivity dropped | 1 (12/84) | yes | 0 / T / 4/4 | — | KILLED-SS | exclusivity only enforced in selftest fixtures |
| M15 | `disposition_check`: unresolvable removal (`rel is None`) now skipped instead of failing closed | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | unresolvable removal branch untested (every removal resolves) |
| M16 | `diagnostic_rel`: root-run scan deepest-first → shallowest-first | 0 (12/85) | no | 1 / F / 3/4 | `projection_ok` on V3 — rerun died: `ENOENT readlink …/bin/ping6`; clean rerun: 0 / T / 4/4 | INCONCLUSIVE-FLAKE | root-run direction untested (single run per link) |
| M17 | `projection`: diagnostics `input_path` fallback dropped | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | diagnostic fallback branch untested (all diagnostics resolve via `link`) |
| M18 | `rel_suffix`: trailing `_extract` dir kept when it is the last segment | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | trailing-extract-dir path shape untested |
| M19 | `projection`: `norm()` always uses `rel_suffix` (root mapping bypassed) | 1 (11/85) | yes | 0 / T / 4/4 | — | KILLED-SS | projection root-mapping only discriminated by the selftest |
| M20 | `carriers_spec`: `member_sha256` removed from frozen external-key requirement | 1 (12/85) | yes | 0 / T / 4/4 | — | KILLED-SS (spec probe) | member-digest presence only enforced by the spec probe; counter never re-verifies member hash at run time |
| M21 | `carriers_spec`: `nested.sha256` relaxed to any string (64-hex check dropped) | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | malformed `nested.sha256` value unguarded (only missing-key case is probed) |
| M22 | `carve_ok` (external): `length == bytes_used == size` → `length == bytes_used` | 0 (12/85) | no | 1 / F / 3/4 | `projection_ok` on V3 — rerun died: `ENOENT readlink …/bin/gzip`; clean rerun: 0 / T / 4/4 | INCONCLUSIVE-FLAKE | size-equality clause appears redundant when `bytes_used == len(raw)` holds |
| M24 | `layout_probe`: AVM marker clause (`mkfs_time == bytes_used`) dropped | 1 (12/84) | yes | 0 / T / 4/4 | — | KILLED-SS | marker enforcement only exercised by the selftest |
| M25 | `frozen_drift`: `nonregular` path dropped from the frozen-path watch | 1 (12/84) | yes | 0 / T / 4/4 | — | KILLED-SS | post-freeze drift of nonregular tables only guarded by the selftest |
| M26 | `carrier_fresh_ok`: prior-pin guard dropped (`pin not in prior` removed) | 1 (12/83) | yes | 0 / T / 4/4 | — | KILLED-SS | CTL-C1-1 (relabelled round-40 receipts) only blocked by the selftest |
| M27 | `evidence_id_ok`: `ev_` prefix check dropped | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | recomputed ids are always `ev_`-prefixed; prefix check untested |
| M28 | `carriers_unchanged` binding forced true | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | post-freeze `carriers.json` mutation untested (unchanged in data) |
| M29 | `gap_rule_ok`: uncovered-kinds check dropped | 1 (12/84) | yes | 0 / T / 4/4 | — | KILLED-SS | uncovered-kind rejection only guarded by the selftest |
| M31 | `oracle_hits`: digest equality dropped (path-only hits) | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | oracle row published with a wrong digest at the same path untested |
| M32 | `oracle_hits_ok`: `==` → `>=` (over-match allowed) | 0 (12/85) | no | 0 / T / 4/4 | — | SURVIVED | hits > files shape untested |

**Totals.** Killed: M01, M06, M07, M09, M11, M12, M13, M14, M19, M20, M24, M25, M26, M29 = 14 (selftest); real-data kills 3 (M01, M09, M13), all a subset of the selftest kills. Inconclusive-flake: M16, M22. Full survivors: M02, M03, M05, M08, M10, M15, M17, M18, M21, M27, M28, M31, M32 = 13. Real-data detector adds **zero unique kills** over the selftest here.

## 3. Real-data flake evidence (M16, M22)

First real runs of M16 and M22 exited 1 with `met_target` false, `projection_ok` false on V3 only; `projection_error` records a REA `execution_failure`:
- M16: `ENOENT: no such file or directory, readlink '…/rerun-V3/rea-firmware-lZ7vJk/extracted/firmware.bin_extract/bin/ping6'`
- M22: `ENOENT: … readlink '…/rerun-V3/rea-firmware-ZbosH3/extracted/firmware.bin_extract/bin/gzip'`

Both mutants alter only post-extraction logic (M16: `diagnostic_rel` scan order; M22: `carve_ok` arithmetic) and cannot influence unblob's extraction. Reruns of both mutants (same detector, same bytes) plus two pristine reruns all passed (`met_target` true, 4/4, `projection_ok` true): `rerun-*.json|.out` in artifacts. Cause: in-tree symlink deletion/readlink race inside unblob 26.6.4 on the V3 rootfs — the same class of iteration-order nondeterminism the claim discloses for removal sets (plans/round-41-claims.md, R41-C1 disclosed limits), here manifesting as a hard `ENOENT` sometimes. These two real runs are therefore **inconclusive**, not kills; verdicts above reflect the clean reruns.

## 4. Calibration (predictions vs outcome)

Predicted selftest kills (9): M01, M06, M07, M08, M09, M13, M20, M21, M24 → 8 confirmed; **M08 survived** (selftest has no `oracle_root`-hint-membership red case). Predicted survivors that the selftest did kill (7): M11, M12, M14, M19, M25, M26, M29 (selftest is stricter than assumed on structural-count text, required-default, exclusivity, projection norm, drift-nonregular, prior-pin and uncovered-kinds). Predicted real kills (3): M01, M09, M13 — all confirmed, all deterministic. M16/M22 predicted survivors; first runs flaked (see §3). All other predictions held (18/21 strict hits; 20/23 counting the two flaky reruns as clarified).

## 5. Coverage findings (survivor → missing case)

1. **M08** — `oracle_root` hint membership error branch (`hint not in roots` → fail-closed) is never exercised: `carriers.json` carries no hint and no selftest red case covers it. A future frozen table naming a wrong root would pass validation until path clauses happen to fail.
2. **M10** — a gap path matching >1 non-regular rows is untested (no duplicate rel rows anywhere; no red case). The `len(hits) != 1` guard is one-sided.
3. **M15** — unresolvable removal diagnostic (`diagnostic_rel → None`) untested; real receipts always resolve.
4. **M16** — `diagnostic_rel` root-run direction (deepest vs shallowest) untested; every link has exactly one root run.
5. **M17** — diagnostics `input_path` fallback in `projection` untested (all diagnostics resolve via `link`).
6. **M18** — `rel_suffix` trailing-`_extract` case untested.
7. **M21** — malformed `nested.sha256` *value* (non-64-hex string) unguarded once the key exists; only the missing-key case is probed. A vendor spec with a bad nested digest would pass the counter (the fetcher is where the hash is checked).
8. **M27/M28** — evidence-id `ev_` prefix and `carriers_unchanged` binding are untested by both detectors; both only ever see the passing state.
9. **M31/M32** — oracle-hit equality is only exercised in the all-match direction; digest-mismatch-at-same-path and over-hit shapes are untested.
10. **M02/M03** — `strip_rel` normalization (`./`, `/` prefixes) is dead on every current table and fixture.
11. **M05** — `receipt_paths` chunk `input_path` contribution is dead w.r.t. root confirmation (files alone suffice on all four carriers).
12. **M20/M22/M24/M26** — member-digest presence, carve size-equality, AVM marker and prior-pin guard are each enforced only on *one* side of the detectors (marker and prior-pin only by selftest; member presence only by the spec probe; carve size not at all — all data satisfy them).

None of these are defects in the counting logic as scored — every survivor is a *positive* claim-clause that the current data satisfies, so the mutants do not disturb the verdict. They bound where the counter's future regression coverage would need new cases.

## 6. Restoration evidence & bounds

- Pristine `tools/round-41/c1-counter.py` sha256 before and after the audit: `bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc` (identical; never written by this seat).
- `git -C <LANE> status --porcelain -- tools/round-41/c1-counter.py plans/round-41-claims.md .ufo/waves/round-41/c1/` → empty; no VCS mutation performed (read-only git only). Lane HEAD at end: `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (read-only observation).
- All mutants lived under scratch `$S` (`/fast/scratch/hyaku/kaidoku-r41/R41W2C1Mutants`); no lane file outside the report and artifact paths below was written by this seat.
- Vendor bytes never copied: cache files reused read-only at their lane-owner path; only their sha256 (== frozen pins) are cited.
- Scratch removed at exit (nothing of the audit persists outside the artifact dir).

## 7. Evidence trail

Artifacts: `.ufo/waves/round-41/w2/artifacts/R41W2C1Mutants/` — `mutants-spec.json` (29 probes + predictions), `unified.diff` (one hunk per mutant), `table.json`, `ss-summary.json`, `baseline-selftest.out`, `baseline-real.json|.stdout`, `ss-<ID>.out` ×29, `real-<ID>.json|.out` ×29, `rerun-<ID>.json|.out` ×4 (pristine ×2, M16, M22).

Key commands (exact):
- Selftest sweep: `for d in $S/fx/tools/round-41/M*; do python3 -I -B "$d/c1-counter.py" --selftest --pkg65 $PK > ss-<ID>.out; done` (385 s; exit codes per table).
- Real sweep: `python3 -I -B "$d/c1-counter.py" --root $LANE --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f --pkg65 $PK --carrier-cache /fast/scratch/hyaku/kaidoku-r41/cache --json-out real-<ID>.json` (576 s; exit codes per table).
- Flake reruns: same real command for pristine-v2, M16, M22 → all exit 0, `met_target` true, 4/4.
- Cache pin verification: `sha256sum /fast/scratch/hyaku/kaidoku-r41/cache/*.bin` = `c4f74f54…f872a`, `ce27ebca…087f` (== `carriers.json` pins).
