# R46W1RegA — receipts

Seat: `R46W1RegA`, kaidoku round 46, wave 1, tag `reg-a`.
Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Freeze: `31820472784284727546808acc31b3ea1e73919b`
Scratch: `/fast/scratch/hyaku/kaidoku-r46/R46W1RegA` (removed after these receipts were copied here).
Installs: **none** (no pacman/uv/npx transaction; `sasquatch`, `unblob` and rea-agents 6.5.0 were
already present: `sasquatch`/`unblob` on PATH at `~/.local/bin`, rea-agents 6.5.0 at
`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`).

Every instrument was read at the freeze, never from the worktree:

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse \
    31820472784284727546808acc31b3ea1e73919b:tools/round-41/c1-counter.py \
    31820472784284727546808acc31b3ea1e73919b:tools/round-42/c1-counter.py \
    31820472784284727546808acc31b3ea1e73919b:tools/round-43/heldout-gen-v4r43.py
57c628fe6e2c52b8a94100c04107735f911a33e8   tools/round-41/c1-counter.py
12857720b3cb2a5b12310410e45603ed77101a97   tools/round-42/c1-counter.py
e252a6526f7f2d2988a486c59ad78a7f8d84be14   tools/round-43/heldout-gen-v4r43.py
```

Working copies (`git show <freeze>:<path>` into scratch) hashed:

```
bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc  r41.py
0f5052f99a976cfdd391d3e8330b644ca403b146095ca73e14f3859ab9d1483c  r42.py
6ab0114d555a09a93ab61459c7adb76a45957a35dc69671b64e7733225aca97a  r43.py
```

## 1. Command receipts (stdout sha256 of the combined stream, exit code captured directly)

cwd for every row below is the lane root; `HYAKU_SCRATCH` and `TMPDIR` pointed at the scratch dir.

| UTC | label | exit | stdout sha256 | command |
|---|---|---|---|---|
| 2026-10-28T16:52:43Z | r41-help | 0 | 23b57b8858ffb2b382370e730b75dbd0d25a78e82f57630f22cebf724d9a4dc4 | python3 -I -B tools/round-41/c1-counter.py --help |
| 2026-10-28T16:52:43Z | r41-no-rerun | 2 | bb5dc710045c002d610500996ff06d2cdb44a207e1139f121e7cb9dd40512966 | python3 -I -B tools/round-41/c1-counter.py --no-rerun |
| 2026-10-28T16:52:43Z | r41-missing-args | 2 | c37ba70cacc79e8fe3a78d4d8b44862d44ac8a25a07e63fb2f91876945529155 | python3 -I -B tools/round-41/c1-counter.py --root . --rev HEAD |
| 2026-10-28T16:52:43Z | r41-selftest | 0 | 61ca2add5625f1c945106b56865baa9a5e72789a05417df7af6f46d54e2391f7 | python3 -I -B tools/round-41/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> |
| 2026-10-28T16:53:10Z | r42-help | 0 | 0905fb79378ceb058504f4478d2d3f831ea2e7c91c301ac3cb2b550041337794 | python3 -I -B tools/round-42/c1-counter.py --help |
| 2026-10-28T16:53:10Z | r42-no-rerun | 2 | 734e7add283be4ddb4bdf8c9beaa2460638efb89659bbcda12982afc27e8cfa0 | python3 -I -B tools/round-42/c1-counter.py --no-rerun |
| 2026-10-28T16:53:10Z | r42-verify-receipt-missing | 2 | bfdd9c3a7c3736b2b083a9016f7695838b9dcb38b27048fa1913298e89cc732e | python3 -I -B tools/round-42/c1-counter.py --verify-receipt ./no-such-receipt.json |
| 2026-10-28T16:53:10Z | r42-selftest | 0 | e028af8cf40feec19e60149f8eba5ddb0d49fe051a6c75f2f3ec68831d220791 | python3 -I -B tools/round-42/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> |
| 2026-10-28T16:53:50Z | r43-help | 0 | 6d401f809a13657d1c14109e5f12de0664280c62f087b6fc6871f7b6bd8cb3c9 | python3 -I -B tools/round-43/heldout-gen-v4r43.py --help |
| 2026-10-28T16:53:50Z | r43-selftest-tuple | 0 | 916ce4e86633be66707b865f99544d386488f133978d4ad2fbda7d0e07006283 | python3 -I -B tools/round-43/heldout-gen-v4r43.py --selftest-tuple --scratch <scratch> |
| 2026-10-28T16:53:51Z | r43-bad-seed | 1 | 072d5954767b042109baa20a8957a36be0867d5fc77c48dbeb2f0c3fcdf310d6 | python3 -I -B tools/round-43/heldout-gen-v4r43.py --seed abc --scratch <scratch> |
| 2026-10-28T16:53:51Z | r43-tuple-check-nodir | 2 | 0a3aceeba773425e0bafb2af7562557339dbd7293faca13ff5730df4b693b6b7 | python3 -I -B tools/round-43/heldout-gen-v4r43.py --tuple-check <scratch>/absent-dir |
| 2026-10-28T16:53:51Z | git-cat-file-pins | 0 | 65adf76fda8afee457014fe84fe6e13ff5cf93a50adf2c50f20f3a3bc152a713 | git cat-file -e <freeze>:<path> for the six pinned-value candidates |
| 2026-10-28T16:53:51Z | git-blob-shas | 0 | 8f86a7c912b485aac12fdb9e4ebc7a05c1d8f7c28c6a93741929470678aeb288 | git rev-parse <freeze>:<three paths> |

Observed bodies (tails, verbatim):

* `r41-help`: argparse surface `--root --rev --freeze --pkg65 --json-out --unblob
  --carrier-cache --rea-timeout --no-rerun --selftest --selftest-rea`.
* `r41-no-rerun`: `{"detail": "P41-C1 binds a fresh REA run of each carrier; --no-rerun cannot be scored", "reason": "rerun_disabled"}`
* `r41-missing-args`: `usage: --root --rev --freeze --pkg65 required`
* `r41-selftest`: `{"selftest": "c1-counter", "cases": 97, "green_ok": 12, "red_ok": 85, "path_probes": 6, "path_probes_discriminating": 3, "root_probes": 8, "spec_probes": 7, ...}`
* `r42-help`: same surface plus `--work --dev-carrier --verify-receipt`.
* `r42-no-rerun`: `{"detail": "P42-C1 binds a fresh REA run of each carrier; --no-rerun cannot be scored", "reason": "rerun_disabled"}`
* `r42-verify-receipt-missing`: `{"ok": false, "reason": "[Errno 2] No such file or directory: './no-such-receipt.json'", "verify": "./no-such-receipt.json"}`
* `r42-selftest`: `{"selftest": "c1-counter", "cases": 121, "green_ok": 14, "red_ok": 107, "path_probes": 6, "path_probes_discriminating": 3, "root_probes": 9, "spec_probes": 14, "prefix_probes": 6, "receipt_probes": 6, ...}`
* `r43-selftest-tuple`: `tuple-check selftest: 17/17 passed`, including six `exit=3` refusal cases and `verify green before the mutation, red after it ... before=0 after=1`.
* `r43-bad-seed`: `--seed must be at least 16 hex characters, got 'abc'`
* `r43-tuple-check-nodir`: `tuple_check: no manifest.json under <scratch>/absent-dir`
* `git-cat-file-pins`: `.ufo/waves/round-41/c1/carriers.json PRESENT`, `.ufo/waves/round-41/c1/gap-rule.json PRESENT`, `.ufo/waves/round-42/c1/carriers.json PRESENT`, `.ufo/waves/round-42/c1/gap-rule.json PRESENT`, `tools/round-42/fixtures.json PRESENT`, `tools/round-43/fixtures.json ABSENT`.

## 2. Exit-path derivation (source at the freeze, line numbers from `git show <freeze>:<path>`)

`tools/round-41/c1-counter.py`

* `main()` at 1743. `--no-rerun` → `return 2` (`rerun_disabled`) at 1771; missing
  `--root/--rev/--freeze/--pkg65` → `return 2` at 1774; `Unevaluable` (including
  `FrozenPathChanged`) → `return 2` at 1788; otherwise `exit_code = 0 if met_target else 1`
  at 1790 and that is the return value at 1798.
* No path returns any code other than 0, 1, 2.

`tools/round-42/c1-counter.py`

* `main()` at 2654. `--verify-receipt`: unreadable/unparseable → `return 2` (2701-ish),
  else `return 0 if ok else 1` (2705). `--no-rerun` → 2; missing args → 2; `Unevaluable` → 2;
  measure path → `0 if met_target else 1`, and a failed receipt identity stamp after a
  successful measure → `return 2` (`receipt_identity_failed`).
* No path returns any code other than 0, 1, 2.

`tools/round-43/heldout-gen-v4r43.py`

* `main()` at 3986. `--tuple-check` → `run_tuple_check_dir` at 3345: no `manifest.json` →
  `return 2` (3350), tuple difference → `return 3` (3359).
* `finalize_manifest` (3321) refuses with `return EXIT_DECLARED_TUPLE_UNOBSERVED` (3335);
  `EXIT_DECLARED_TUPLE_UNOBSERVED = 3` (3140).
* `--run` per-carrier REA error → `return 1` (4163); `--verify`/`regen_check` mismatch →
  `return 1 if (status or regen) else 0` (4178); build without `--run` → 0.
* `raise SystemExit('<string>')` for a short seed (4077), a missing `--out` (4110), an
  existing `manifest.json` under `--out` (4114), etc. — CPython exits 1 and prints the
  string; measured by `r43-bad-seed` (exit 1).

## 3. Row validation against the frozen checker (`tools/round-46/registry.py` @ the freeze)

`tools/round-46/{registry.py,census.py,gate.py,census.json}` were copied out of the freeze to
scratch and the frozen `score()` was driven in-process over `rows.md` (never over `SKILL.md`).
Driver: `probe.py` beside this file; each mode is one process, one exit code.

| UTC | label | exit | stdout sha256 | command |
|---|---|---|---|---|
| 2026-10-28T16:55:53Z | probe-rows | 0 | 6d66d0ad618943ef4ba56948de5195e90cf57f7cc4c121fa4878a4ba22207b6f | python3 -I -B probe.py rows |
| 2026-10-28T16:55:53Z | probe-A | 1 | 6f93e4ceb42c7b37c2ca0ac03007215f5816d853c21e4f5c809e63d9073d1c4e | python3 -I -B probe.py A |
| 2026-10-28T16:55:54Z | probe-B | 0 | 933787689e232d3963180da059f1b09d322c76b6e5d15928eb9206d0f0613260 | python3 -I -B probe.py B |
| 2026-10-28T16:55:54Z | probe-M0 | 0 | 563f424ea1df9ba53130fb351b7a2daf3aedaae70428b0879ddf7ff12d467a0f | python3 -I -B probe.py M0 |
| 2026-10-28T16:55:54Z | probe-M1 | 1 | 91558ace7876e3ea877ac0287092771be500357858b0b430f08f772132b4b027 | python3 -I -B probe.py M1 |
| 2026-10-28T16:55:54Z | probe-M2 | 1 | db6320dd735cabfe1f632ae17a34f5aaa1f27b823cec053d029839481435c42a | python3 -I -B probe.py M2 |
| 2026-10-28T16:55:54Z | probe-M3 | 1 | 356ccfc5a1c6e91985d15ba694bc24fc31c090b8b7a7175223c44a561d116947 | python3 -I -B probe.py M3 |
| 2026-10-28T16:55:54Z | probe-M4 | 1 | f727dcbd0ebcb345a66792f2530b837ff0734ee892a3cffc1296de8a2054473c | python3 -I -B probe.py M4 |
| 2026-10-28T16:55:54Z | probe-pins | 0 | 000e20cabd0604013caed9a26539d8578dfc4b6835ce35f2a5a0c386746d0081 | python3 -I -B probe.py pins |
| 2026-10-28T16:55:54Z | probe-census | 0 | 316e0bec982c451bb9b9e48a31eef14ab6953575b75f6aada2197f7bc3b987ab | python3 -I -B probe.py census |

Results:

* `rows` — 3 rows, 7 cells each, cell 1 exactly the backticked path, verdict map binds
  `0=`, `1=` and `2=`: PASS, exit 0.
* `A` (real frozen census, 38 paths, my 3 rows only) — `scope_size 38`,
  `header_ok true`, `registered` = the three, `thin []`, `absent_at_rev []`,
  `unregistered_count 35`, `failing ['unregistered: 35 of 38']`, exit 1.
  **Exit 1 is the 35 census paths other seats own, not a defect in these three rows.**
* `B` (scope = exactly these three paths) — `registered` = the three, `unregistered []`,
  `thin []`, `absent_at_rev []`, `failing []`, `met_target true`, exit 0.
* `M0` unmutated control green (exit 0); `M1` prose-digit verdict map → `thin` lists all
  three; `M2` rows inside a fence → `registry_rows 0`, all three unregistered; `M3` cell 0 a
  suffix of the scope path → that one path unregistered; `M4` three-cell header →
  `header != house schema (7 cells)`. All four red (exit 1).
* `pins` — `default_fixture_pins()` resolves to
  `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-42/fixtures.json` (exists),
  `EXIT_DECLARED_TUPLE_UNOBSERVED = 3`.
* `census` — `scope_size 38`, `named_but_absent 0`, all three of my paths `true`.

## 4. Cleanup

`/fast/scratch/hyaku/kaidoku-r46/R46W1RegA` was removed after this file and `probe.py` were
copied here. Lane tree untouched (read-only `git show`/`rev-parse`/`cat-file` only); the only
writes are `.ufo/waves/round-46/w1/R46W1RegA/` and `.ufo/waves/round-46/w1/R46W1RegA.md`.
