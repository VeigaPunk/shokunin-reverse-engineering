# C1SelfTest — `c1-counter.py --selftest` (round 49, wave 1, pre-freeze)

Counter under test: `.ufo/waves/round-49/draft/tools/round-49/c1-counter.py`, sha256 `d6d70cb7ecc789b5ac0b0cbb7ee5b656abeea395cea9a158249d9a4723a95779` (3374 lines). Not run: `--data-run`, any non-offline arm.

## Verdict
**Selftest is green and stable (47 cases, 0 failures, exit 0, byte-identical JSON x4) but it does NOT discriminate most frozen clauses.** Mutation test (clause forced True in a scratch copy, selftest re-run): **only 11 of 34 CLAUSES+BINDINGS are killed; 23 survive.** Nine of those never fail in ANY case, and one binding is a tautology in code.

## 1. Runs (UTC 2026-10-28, all `python3 -I -B <counter> --selftest --work $S/selfN`, TMPDIR=$S, cwd=$S)
| run | exit | stdout sha256 | wall |
|---|---|---|---|
| 1 | 0 | e92726cdb1a065a6d48a3ff608f984990e9af28cfd1a7f2732b3ed5a655870ab | not timed individually (runs 1-4 loop: 42.34 s total, ~10.6 s each) |
| 2 | 0 | same | (in loop) |
| 3 | 0 | same | (in loop) |
| 4 | 0 | same | (in loop) |
| 5 (`C1_SELFTEST_DETAIL=1`, stdout) | 0 | same | 11 s |

Output JSON: `{"cases":47,"green_ok":1,"red_ok":46,"failures":[],"prefix_probes":6,"receipt_probes":5,"selftest":"c1-counter"}` + 11 probe_results. It contains no wall-time field, so stability is full byte equality, not "modulo wall time". Plain `bc` is absent on this host (my first wall-time attempt failed; not a counter issue). Receipts: `C1SelfTest/selftest-out.json`, `detail.tsv` (per-case failing sets), `coverage.txt`.

## 2. Case list (47; want exit in brackets)
green [0]; do-nothing; receipt missing (v2be); v3 receipt fed to v1; v2 receipt fed to v1; fabricated oracle-only envelope; rerun yields no evidence object; rerun environment error [2 rerun_env_error]; v2 nonstandard magic zlqs; truncated superblock; bytes_used beyond file; s_major contradicts handler; metadata block uncompressed; metadata length off directory table; BE magic on LE carrier; carrier padded past chunk end; oracle census sha flipped; receipt publishes unlisted regular file; symlink row published as regular; output_tree digest mismatch; depth-limited gap; missing-extractor-dependency gap; receipt path `..` provenance; provenance of /kaidoku-r42/; trailing-slash published file; x_extract2 prefix; receipt added at freeze not fresh; score receipt relabelled REA evidence; stale evidence id; subject digest names another carrier; carriers.json fifth (v2.1) carrier; carriers.json drops carrier; handler disagrees with s_major; all-LE; carriers.json changed after freeze [2]; carrier bytes changed after freeze [2]; oracle tree edited after freeze [2]; frozen path touched-then-restored [2]; no Core section; row names only v1; row cites other entry; frontier note absent; entry absent; entry cites one S-id; S139 opened earlier; S138 row missing; coverage map lacks stem. (+11 prefix/receipt probes, separate from the 47.)

## 3. Gap list — clauses with no selftest case that reds when the clause is false
Method: `C1SelfTest/mutate.py <clause>` copies the counter to scratch, drops that one clause from `matched` (CLAUSES, c1-counter.py L2137) or from the `met_target` conjunction (BINDINGS, L2218), runs `--selftest`; "SURVIVES" = 0 failures, i.e. no case depends on that clause. No-op control: 47 cases, 0 failures. Results: `mutation-results.jsonl` (34 lines).

**A. Never listed as failing in any single-carrier/binding case (outside the do-nothing / receipt-missing / fifth-carrier mass cases) — zero evidence the clause can fail:**
- `carrier_present`, `carrier_pin_ok`, `carrier_size_ok` — only reachable by a carrier blob wrong at the FREEZE itself; post-freeze edits are pre-empted into exit 2 `frozen_path_changed`. No case plants a bad pin/size/mode at the freeze.
- `carrier_fresh_ok` — `spec_json(prior_pins=...)` exists (L2878) but **no case calls it**; the PRIOR_PIN_CANDIDATES path is also untested.
- `oracle_ok` — no case feeds a malformed oracle block (a bad census row is probed only via sha flip, which hits tree_ok/oracle_hits_ok).
- `gap_rule_ok` — fires only on an uncovered nonregular kind; every carrier has zero nonregular rows, no case plants one.
- `family_coverage` — `carriers.json drops v2be` leaves v2le, so it never goes False; no case removes both v1 or both v2.
- `frozen_tables_valid` — **tautology**: `res['frozen_tables_valid'] = True` (L1995) is set before anything is checked; invalid JSON raises Unevaluable (exit 2) first. The binding can never be false; it is decorative.
- `oracle_tool_ok` — the selftest spec has **no top-level `oracle` block** (`spec_json` L2918), so the function returns the "advisory True" branch every time; the real carriers.json DOES carry `oracle.tool`/`tool_sha256`, so the sha/version/executable branches the data run will take are never exercised.

**B. Fail only incidentally (co-failing with another clause in every case that reds them; forcing them True changes no verdict):**
`layout_ok`, `carve_ok`, `subject_pin_ok`, `handler_ok`, `oracle_hits_ok`, `gaps_ok`, `nonregular_unpublished_ok`, `evidence_id_ok` (all co-fail with `projection_ok` or each other), `receipt_present`, `operation_ok`, `chunks_ok` (fail only in receipt-missing / do-nothing / fifth-carrier mass cases, always alongside `receipt_fresh`/`evidence_envelope_ok`), and BINDINGS `carriers_spec_ok`, `entry_present`, `province_core_section`, `endianness_coverage` (e.g. `entry absent` also reds `sourced`; `no Core section` also reds core_row+frontier_note; carriers_spec cases also red other clauses/projection). Note `operation_ok` and `chunks_ok` have NO case that sets operation != extract_firmware / provider != unblob or a failed chunk; `handler_ok` cases (v3/v2 receipt) do assert `want_fail=…handler_ok` but still survive because `projection_ok` also reds.

**C. Killed (>=1 case needs the clause):** `tree_ok`(1), `receipt_fresh`(1), `evidence_envelope_ok`(1), `projection_ok`(2), `path_shape_ok`(1), `run_provenance_ok`(2), and BINDINGS `province_core_row`(2), `frontier_note`(1), `sourced`(3), `coverage_map_row`(1). (11 total.)

## 4. Suggested additions (for the L1; I did not edit the draft)
1. Case: carrier blob with wrong pin/size/mode committed AT the freeze (assert `carrier_pin_ok`/`carrier_size_ok`/`carrier_present`, with receipts rehosted so projection still passes if feasible).
2. Case: `prior_pins=[pin of v1le]` -> `carrier_fresh_ok` red.
3. Case: selftest spec with a top-level `oracle` block (wrong `tool_sha256`, non-executable path, wrong version) -> `oracle_tool_ok` red; mirror real carriers.json shape.
4. Case: a nonregular census row of a kind outside GAP_RULE.allowed -> `gap_rule_ok` red; malformed oracle block -> `oracle_ok` red.
5. Case: both v2 carriers dropped/relabelled -> `family_coverage` red.
6. Cases with `operation != extract_firmware` / `provider.id != unblob` and a failed chunk with otherwise identical projection -> isolate `operation_ok`/`chunks_ok`.
7. Delete `frozen_tables_valid` from BINDINGS or make it check something (it is `True` by construction).
8. Make sole-discriminator mutation part of the selftest (per-clause "red with only this clause false") so B-class clauses stop surviving.

## 5. Commands/receipts
- `python3 -I -B <counter> --selftest --work $S/selfN` x4 — exit 0 each, sha above.
- `C1_SELFTEST_DETAIL=1 ...` — exit 0, 47 DETAIL lines (`detail.tsv`, sha 'errd' in this dir), analysis `analyze.py` -> `coverage.txt`.
- `python3 mutate.py <NAME>` x35 (34 clauses + NOOP), xargs -P8 — NOOP: 47/0 failures; results in `mutation-results.jsonl`.
- Mutants run from `$S/mut/<name>/tools/round-49/` with `tools/round-27` symlinked to the lane (counter's `find_xpin` need).
- No tools installed. Scratch `/fast/scratch/hyaku/kaidoku-r49/C1SelfTest` removed after copy.
