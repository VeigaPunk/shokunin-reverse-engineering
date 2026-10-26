# R42C1Mutants — mutation test of the round-41 C1 counter clauses round 42 keeps

**Verdict: DEFECTS FOUND** — 22 single-logic mutants of `tools/round-41/c1-counter.py`
(at base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`, byte-identical to lane HEAD `fdabdfa`,
git blob `57c628fe6e2c52b8a94100c04107735f911a33e8`, sha256 `bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc`):
**12 killed** by the offline `--selftest`, **10 SURVIVED**. Every survivor is a coverage
gap the round-42 port of the counter must close in its selftest; none of them is by itself
evidence that the counter's contract is wrong, and no contract text was changed.

All runs were on a disposable sandbox clone (`git clone --shared` of the lane, then
`checkout c4a38ea…`; `git rev-parse --show-toplevel` asserted equal to the clone dir before
any work). The lane itself was never modified; no git mutation touched the lane or fleet.

## Method (the one behavioral detector, three phases)

Detector = `python3 tools/round-41/c1-counter.py --selftest --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`
(offline, deterministic; drives `measure()` in-process with simulated REA runners; 97 cases:
12 green + 85 red, plus 6 matcher probes (3 discriminating exact-vs-legacy), 8 root probes
and 7 spec probes).

- **Pristine**: exit 0, 97 cases, `failures: []` — 12.4 s.
- **Mutant**: one minimal logic edit applied (string asserted to occur exactly once),
  detector re-run, full stdout/stderr kept per mutant (`artifacts/R42C1Mutants/runs/M<id>.out/.err/.diff`).
- **Restored**: pristine bytes written back after every mutant, sha256 re-verified against
  `bbabbfec…`; a final detector run on the restored bytes exits 0 with 97 cases and no failures.

Harness: `artifacts/R42C1Mutants/mutate.py` (phases `baseline` / `mutants [--only]` / `final` / `restore`).
Full machine-readable results: `artifacts/R42C1Mutants/results.json`; hash log:
`artifacts/R42C1Mutants/hash-log.txt`.

Environment: python 3.14.8, git 2.56.0, node v24.21.0, `HYAKU_SCRATCH=/fast/scratch/hyaku`,
`TMPDIR` inside the seat scratch. **Tooling: nothing installed or upgraded** (no pacman, no
uv, no npx installs needed; the npx cache for rea-agents 6.5.0 already existed and the offline
selftest never invokes REA).

## Results table

| mutant | single-logic mutation (area) | killed? | by which case | case the round-42 port must add |
|---|---|---|---|---|
| M01 | `extract_rel`: whole-segment root equality → raw string `startswith` (non-segment-bounded prefix; `rootX/rest` counts as inside `root`) | **NO — SURVIVED** | — (exit 0, 0 failures over all 97 cases) | Oracle-shadow shape: publish `firmware.bin_extract_extra/var/info.txt` (sha `f20`) besides the real `firmware.bin_extract/var/info.txt`, and freeze the oracle row `_extra/var/info.txt` (same sha/size) next to `var/info.txt`. Exact matcher: the stray file is outside the root → 1/2 rows → exit 1, `oracle_hits_ok` false. Prefix mutant: 2/2 → green. Use `same_run` |
| M02 | `same_rel`: exact root-mapped equality → legacy `endswith('/'+rel)` rule (R40-CL1 reintroduced) | yes (9 failures) | path probes `dir 1: regular usr/bin/busy vs symlink entry bin/busy`, `deeper-than-oracle file vs oracle row usr/bin/busy`, `nested chunk root file vs outer-root table row lib/x` + the `>= 3 discriminating probes` assertion + cases `regular usr/bin/busy does not satisfy…`, `deeper file with the oracle row sha256…`, `gap on usr/bin/busy…`, `two chunks: nested chunk file…`, `padded carrier: same rows one level too shallow` | none (covered) |
| M03 | `subject_root`: >1 squashfs root no longer fails closed; deepest root guessed (`len(roots)==1` → `roots`) | yes (6 failures) | root probes `two roots without a hint`, `two portion chunk roots`, `ambiguous handler chunks`; case `two chunks with oracle_root: the nested file is another namespace` (want 0 got 1); `two handler chunks and no input handler chunk fail closed` (want_fail clause shuffle) | none (covered) |
| M04 | `subject_root`: frozen `oracle_root` hint accepted without checking it names a real derivation root | **NO — SURVIVED** | — | Add a root probe on the existing `two_wrong_recs` receipt (hint `no.such.root`): assert `(None, src)` with `src` starting `oracle_root` and containing `not among`. Today only the end-to-end exit is asserted, and it stays red under the mutant (root `no.such.root` matches nothing) |
| M05 | `path_parts`: `.` segments no longer dropped | **NO — SURVIVED** | — | Case: V4 publishes `firmware.bin_extract/./var/info.txt` (same sha/size) against oracle row `var/info.txt`, `same_run`, want 0. Pristine normalizes → green; mutant keeps `./var/info.txt` → 0 hits → `oracle_hits_ok` red |
| M06 | `oracle_hits_ok`: hit-set equality (`hits == oracle_files`) → `hits > 0` | yes (2 failures) | `deeper file with the oracle row sha256 does not publish oracle bin/busy`; `two chunks: the nested chunk file does not publish outer-root row lib/x` | none (covered; the single-oracle-file V4 shape alone does NOT kill it — the killer needs ≥2 oracle rows with one shadowed) |
| M07 | `nonregular_published`: exact matcher → legacy suffix matcher | yes (1 failure) | `regular usr/bin/busy does not satisfy the symlink entry bin/busy` (want 0 got 1) | none (covered) |
| M08 | `disposition_check`: structural allowance read as `limit + 1` | yes | `structural gaps over the allowance` (want_fail `gaps_ok` no longer failing) | Keep, but re-anchored: today the case stays red only via the projection backstop (default sim runner reruns the pristine receipt). Rebuild it with `same_run` on the mutated receipt so `gaps_ok` itself is the only red clause |
| M09 | `disposition_check`: `required` default flips to False (`need = required.get(kind, False)`) | yes | `required gap missing (symlink materialised)` (want_fail clause shuffle) | Same re-anchoring note as M08: kill today arrives via `nonregular_unpublished_ok`+projection, not the required-default rule itself. Add a shape whose materialised entry is not published under the root (so only the required-default clause turns green) |
| M10 | `disposition_check`: gap-kind membership dropped (any kind allowed if the entry kind has any allowance) | yes | `disallowed gap kind on a symlink entry` (want_fail clause shuffle) | Same re-anchoring note: use `same_run` so only `gaps_ok` differs |
| M11 | `handler_ok`: exact `squashfs_v4_be` → any `squashfs_v4*` handler | yes | `chunk handler is the LE handler` (want_fail clause shuffle) | Re-anchor with `same_run` (today the projection backstop kills it) |
| M12 | `HANDLER_RE`: lookarounds dropped → substring match in the PROVINCE row cell | **NO — SURVIVED** | — | Case: `_province(cell='`xsquashfs_v4_bex`')` → want 1, want_fail `b:province_core_row`. Pristine regex rejects the non-segment-bounded token; substring mutant accepts → green |
| M13 | `evidence_ids`: stored id compared to itself (`(f[2], f[2])`) — recompute result never checked | yes (indirect) | `evidence id stale after an edit` (want_fail `evidence_id_ok` missing; the case stays red only via the projection backstop) | Add a dedicated case: take a green receipt, substitute a different but well-formed `ev_<64hex>` id, touch nothing else → projection unchanged, so `evidence_id_ok` is the ONLY false clause (want 1 want_fail `evidence_id_ok`) |
| M14 | `projection`: diagnostics projected as typename only (R41C1DevCore 7.3 reverted) | yes | `a rerun that removed a different link breaks the projection` (want 1 got 0) | none (covered) |
| M15 | `REPLAY_PARAMS`: `--max-depth` no longer replayed to the rerun | **NO — SURVIVED** | — | Offline argv probe: write a fake `npx` shim on PATH that records `"$@"` and exits 1; call `make_real_runner(...)(b'x', 'PROBE', {'max_depth': 3, 'max_output_bytes': 1, 'max_output_files': 1})` (expect `RerunEnvError`), then assert the recorded argv contains `--max-depth 3`. The existing depth cases only exercise injected runners, never the replay |
| M16 | `make_real_runner`: REA pin `rea-agents@6.5.0` → `rea-agents@6.0.0` in the rerun argv | **NO — SURVIVED** | — | Same fake-npx probe; additionally assert the argv carries `rea-agents@6.5.0`. `--selftest` injects every runner, so the whole real-rerun argv assembly is unpinned offline (only `--selftest-rea` touches it, which is not part of the offline detector) |
| M17 | `frozen_drift`: carrier `path` entries no longer added to the frozen set | yes (2 failures) | `carrier bytes changed after freeze` (want 2 got 1); `carrier bytes changed then restored` (want 2 got 0) | none (covered) |
| M18 | `met_target`: endpoint-equality clauses (`carriers_unchanged`, `gap_rule_unchanged`) removed from the verdict | **NO — SURVIVED** | — | Not killable through the commit harness: every harness-reachable divergence appears in the `freeze..rev` name-only log, and `frozen_drift` covers exactly those paths, so the drift check supersedes both endpoint clauses in every case (a rename is caught because `--no-renames` logs the old path too). Record as accepted redundancy, or pin the True side with a direct probe (`measure(...)['carriers_unchanged'] is True` on the green fixture) and say so in the port's comment |
| M19 | `main()`: `res['exit_code']` hardcoded to 0 — met and miss both exit 0 | **NO — SURVIVED** | — | CLI probe: run the counter as a subprocess on the do-nothing fixture (freeze files only, no receipts → no rerun → no REA needed) and assert exit 1 and `exit_code: 1` in the printed JSON. `--selftest` asserts `met_target` in-process and maps exits itself, so `main()`'s 0/1 mapping is never executed |
| M20 | `main()`: Unevaluable branch returns 1 instead of 2 — unevaluable and target-miss indistinguishable | **NO — SURVIVED** | — | CLI probe: green fixture receipts committed, run the counter with `npx` stripped from PATH (real runner → `RerunEnvError`) and assert exit 2, reason `rerun_env_error` |
| M21 | selftest loop: FrozenPathChanged recorded as exit 1 instead of 2 | yes (9 failures) | all nine freeze-drift cases (`carrier bytes changed after freeze`, `carrier bytes changed then restored`, `oracle changed…`, `nonregular table changed…`, `carriers.json changed…`, `gap-rule.json changed…`, `gap-rule.json touched then restored`, `counter edited after freeze`, `claims edited after freeze` — all want 2 got 1) | none (covered) |
| M22 | `disposition_check`: gap-to-entry uniqueness `len(hits) != 1` → `not hits` (a gap path may match multiple entries; first wins) | **NO — SURVIVED** | — | Case: nonregular rows `bin/x\tsymlink\t../t` and `bin/x\tdevice\t` (same rel, distinct kinds — parse-legal), rule with `removed.silent: {'device': ['empty-target']}`, receipt carries exactly one `unpublished-entry` gap on `bin/x`, `same_run`, want 1 want_fail `gaps_ok`. Mutant resolves the gap against the row dict (last-wins → device), which silences both rows → green |

Counts: 22 mutants (assignment asked ≥ 15), 12 killed, 10 survived, 0 inconclusive
(baseline passed, so every verdict is conclusive).

## Coverage findings for the round-42 port (ordered by severity)

1. **The CLI contract is unpinned (M19, M20).** `--selftest` drives `measure()` in-process
   and maps `met_target`→exit itself; `main()` — the only thing a receipt consumer actually
   runs — is never executed by the offline detector, so both the 0/1 verdict mapping and the
   unevaluable-exits-2 rule can rot silently. The two CLI probes above are cheap and offline
   (no REA: the do-nothing fixture never reruns; the second strips `npx` from PATH on purpose).
2. **The real-rerun argv/parameter replay is unpinned (M15, M16).** Every offline case
   injects a runner, so `REPLAY_PARAMS` (the clause that makes the rerun about the image, not
   the flags — routed R39-CL5 machinery) and the frozen REA pin in `make_real_runner` are only
   exercised by `--selftest-rea`. The fake-npx argv probe pins both offline.
3. **Exact-path identity has two unpinned shapes (M01, M05), both in `extract_rel`/`path_parts`.**
   Round-41 closure D5 made the matcher segment-bounded; nothing tests the boundary itself
   (`rootX` ≠ `root`) or the `.`-segment normalization. Both prescriptions are one-case fixes
   built from existing helpers (`pub`/`entry`/`same_run`).
4. **Fail-closed root derivation is under-probed (M04).** The bad-hint end-to-end case cannot
   distinguish "hint validated" from "hint names a dead root that matches nothing"; only a
   root probe on `(root, source)` can.
5. **Handler/regex boundaries (M12) and gap-to-entry uniqueness (M22)** each need one new
   fixture shape (near-miss handler token in the PROVINCE cell; same-path two-kind nonregular
   rows). M22's killer also exposes that `by_rel` is last-wins on duplicate rels — worth a
   sentence in the port's comment even after the case lands.
6. **Calibration note on the kills:** M08–M11 and M13 were killed only by the `want_fail`
   clause assertion while the projection backstop (sim rerun of the pristine receipt) kept
   the case red. The round-42 port should rebuild those cases on the `same_run` pattern so the
   target clause alone turns the verdict, exactly as the round-41 path-identity cases already
   do; otherwise deleting the target clause is invisible whenever a receipt edit also breaks
   the projection.
7. **Accepted redundancy (M18):** `carriers_unchanged`/`gap_rule_unchanged` are implied by
   `frozen_drift` on every harness-reachable input. Either document them as belt-and-suspenders
   or pin their True side with a direct probe; do not spend a case trying to flip them through
   commits — it is not reachable.

## Restoration evidence

- Pristine sha256 before the first mutant: `bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc`
  (= `git show c4a38ea…:tools/round-41/c1-counter.py` blob `57c628fe…`, byte-identical at lane HEAD `fdabdfa…`).
- After every mutant the harness wrote the pristine bytes back and re-hashed: `restored_sha256_matches: true`
  for all 22 records (`results.json`); `hash-log.txt` logs each step.
- Incident, disclosed: the first full mutant batch was killed by the 300 s tool deadline after
  M19, **mid-M20**, leaving M20's mutated bytes (`2f7d3913bbccd3797efd7109c50fe01269343deebb667cac2eb729530ad4e5c4`)
  on the clone file. The pre-state guard added to the harness refused to continue
  (`old_occurrences: 0`), the bytes were restored from the git blob (`--phase restore`,
  blob sha256 verified `bbabbfec…` before write), M20 was re-run properly (SURVIVED), and the
  final detector run on the restored pristine bytes passed (97 cases, exit 0). The accidental
  mutated-bytes "final" run of the first attempt is itself consistent with M20's survival mode
  (`--selftest` never calls `main()`), but the recorded final evidence is the clean rerun.
- Clone working tree at the end: sha256 `bbabbfec…` = pristine. Scratch
  `/fast/scratch/hyaku/kaidoku-r42/R42C1Mutants` (clone included) is removed at seat finish;
  every cited artifact lives in `artifacts/R42C1Mutants/`.

## Limits

- The detector is the counter's own `--selftest`; nothing here validates the counter against
  real REA output (`--selftest-rea` and the carriers are other seats' scope; no published
  image was touched — the reserved-carrier rule is respected trivially: the offline selftest
  fabricates all carriers).
- Kill predictions for the prescribed new cases are code-derived, not executed: they are
  marked as prescriptions for the round-42 port, [INFERENCE] on their exact pristine-green /
  mutant-red behavior until the port runs them.
- Mutants are single-logic edits at the named clause only; no compound mutants were tried,
  so the table says nothing about interaction effects.
