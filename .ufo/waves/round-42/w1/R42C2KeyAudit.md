# R42C2KeyAudit — generator→manifest→counter key audit (QUALITY 83/84)

**Verdict: CONFIRMED** — M41-1/R41-CL1 reproduced statically and empirically at base `c4a38ea` (generator writes `declared`, counter reads `class_expected.features`/`features`/`declared_features`, combos unresolvable); key table and stdlib checker delivered (red on the r41 pair, green on a fixed pair); 3 additional interface findings (one defect-class dead read `rea_params`, two forward flags for the round-42 drafts).

Base audited: `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (lane `main` has moved to `ae5dc3f3…`; all line numbers below are of the pinned-commit copies preserved under `artifacts/R42C2KeyAudit/fixtures/`). Writer universe per assignment: `tools/round-41/heldout-gen-v3.py` only. Readers: `tools/round-41/c2-counter.py`, `tools/round-41/c1-counter.py`, then the round-42 drafts present under `.ufo/waves/round-42/w1/artifacts/{R42C2Gen,R42C2Counter,R42C1Counter}/`.

Evidence commands and exit codes are in `artifacts/R42C2KeyAudit/runs.log`; checker outputs in `audit-r41.json`, `audit-v4gen-vs-r41counter.json`; C1-port diff in `audit-r42c1-port.diff` (1904 diff lines, 1272 changed). All scratch was removed; the citations below are the artifacts copies.

---

## 1. Writer inventory — `heldout-gen-v3.py` (fixtures/gen-r41.py)

### 1.1 `manifest.json` top level (written at 1837–1839)

| key | line | notes |
|---|---|---|
| `seed` | 1771 | read by counter (1059, 1223) |
| `round` | 1772 | no reader |
| `claim` | 1773 | no reader |
| `generator` | 1774 | read (1062); `.name` 1065, `.sha256` 1067; `.writer` 1779–1784, `.partial_pin` 1785–1793 unread |
| `action_vocabulary` | 1795 | no reader |
| `action_set` / `action_source` | 1796/1797 | no reader |
| `label_actions` / `new_labels` / `new_label_tokens_binding` | 1798–1802 | no reader |
| `rea` | 1803–1806 | **no reader** — counter reads `rea_params` (dead, F2) |
| `declared_schema` | 1807–1823 | no reader; its `location` text names `carriers[].declared` as the binding location — the writer's contract statement |
| `families` | 1824–1829 | no reader (`combo.class_expected: null` at 1826 is by design) |
| `replicate_variation` | 1830 | no reader |
| `out_of_domain` | 1831–1833 | no reader |
| `classes` | 1834 | read (1046) |
| `carriers[]` | 1835 | read (1047) |

### 1.2 Carrier entries — class shape (1349–1383)

`id` 1350, `class` 1351, `label` 1352, `action` 1353, `arm` 1354, `endian` 1355, `compression` 1356, `tree` 1357, `content` 1358, `symlinks` 1359, `corruption` 1360, `damage` 1361, `layout` 1362, `chunks` 1363, `nested` 1364, `rea` 1365, `operation` 1366, `carrier` 1368, `sha256` 1369, **`declared` 1372** (the binding tuple: handler_set, gap_kinds, gap_dependencies, be_argv, symlink_removed, published — `DECLARED_FIELDS` 573–574), `declared_extras` 1373 (`extraction_failed`, `max_depth`), `class_expected` 1377–1382 (`label` 1378, `action` 1379, `reported_only` 1380, **`features` 1381** — 8 subkeys incl. the two extras).

### 1.3 Carrier entries — combo shape (1443–1470)

`id` 1444, `class` 1445, `family` 1446, `combo_index` 1447, `factors` 1448, `label` 1449 (**statically null**), `action` 1450 (**null**), `arm` 1451, `endian` 1452, `compression` 1453, `tree` 1454, `content` 1455, `symlinks` 1456, `corruption` 1457, `damage` 1458, `nested` 1459, `rea` 1460, `operation` 1461, `carrier` 1462, `sha256` 1463, **`declared` 1464**, `declared_extras` 1465–1466, `class_expected` 1469 (**statically null**).

### 1.4 Other documents the generator writes

- `tree.json` class 1384–1395 (`seed, class, id, endian, compression, label, action, declared, declared_extras, class_expected, nested, chunks, oracle`); combo 1471–1477 (`seed, class, id, factors, endian, compression, declared, class_expected:null, oracle`). **No counter reads tree.json.**
- `run.json` 1607–1639 (extract run) / 1664–1694 (OOD run): `id, class, arm, operation, max_depth, expected_label, expected_action, class_expected, declared, declared_extras, factors, exit_code, rea_argv, unblob_command, home_bin_on_path`, plus `error/stdout_head/stderr_head` on failure, plus `ok, subject_sha256, digest_matches_carrier, duration`, plus the `shape` merge (1529–1548: `operation, provider, handlers, failed_chunks, gap_kinds, gap_dependencies, diagnostics, be_argv, symlink_removed, depth_limited_paths, parameters{max_depth}, files, coverage`). **No counter reads run.json**; the generator's own `--verify` does (1889–1911).
- `envelope.json` / `rea-full.json(.gz)` 1555–1576: REA 6.5.0 envelope passthrough (writer of record: REA runtime). This is what c2-counter actually reads.

## 2. Reader inventory — `c2-counter.py` (fixtures/counter-r41.py)

### 2.1 Manifest-level reads

| key | line | written by generator? |
|---|---|---|
| `classes` | 1046 | yes (1834) |
| `carriers` | 1047–1048, regen 1212 | yes (1835) |
| `seed` | 1059; regen 1223 | yes (1771) |
| `generator.name` / `generator.sha256` | 1065 / 1067 | yes (1775 / 1777) |
| `rea_params` | 1459 | **NO — dead read** (gen writes `rea` 1803). Advisory only (`binding: False`), feeds `res['advisory_rea_params']` |
| `class_features`, `classes_features`, `feature_tuples`, `features_by_class`, `class_tuples` | 1487–1489 | **NO — dead reads** (class-map candidates; gen has no top-level feature map) |

### 2.2 Per-carrier reads (the M41-1 site)

| key | line | verdict per shape |
|---|---|---|
| `id` | 1050, 1099, 1105, 1116, 1218, 1229, 1495 | written (1350/1444) |
| `class` | 1051–1052, 1056, 1099, 1105, 1219, 1241, 1462, 1494–1529 | written (1351/1445) |
| `arm` | 1109, 1220, 1241, 1264 | written (1354/1451) |
| `sha256` | 1230 | written (1369/1463) |
| `carrier` | 1231, 1246; regen 1215 | written (1368/1462) |
| `class_expected` | 1106, 1117, 1221–1222, 1497 | class shape yes (1377); combo **statically null** (1469) |
| `class_expected.features` | 1498–1499 | class shape yes (1381); combo **unreachable** |
| `features` | 1500–1501 | **NO — dead read** (no carrier entry ever writes a top-level `features`) |
| `declared_features` | 1502–1503 | **NO — dead read** |
| class-map fallback `man[decl_key][class]` | 1504–1505 | **dead** (no candidate map exists) |
| `expected_label` / `expected_action` | 1119–1120 | **dead on manifest entries** (written only in run.json 1610–1611); combos therefore land in the class-map `missing` bucket by design (`res['combos'].class_expected_null`, 1104–1107) |
| `envelope` | 1243 | **dead** — counter infers `<carrier-dir>/envelope.json` (1244–1249, `envelope_inferred`) |
| `max_depth` | 1471 | **dead on entries** (gen nests it: `rea.max_depth` 1365/1460, `declared_extras.max_depth` 1373) |

### 2.3 Envelope reads (`envelope.json` data object; writer of record: REA 6.5.0 runtime, passthrough 1555–1576)

`data` 452–453; `subject.digest.sha256` 457–459 (envelope digest binding); `normalized_result` 522, 580; `chunks[].handler` 587; `chunks[].extraction_failed` 590; `extraction_gaps[].kind` 597; `extraction_gaps[].dependencies` 602; `diagnostics[].report` 526, 616; `report.__typename__` 617, 622; `report.command` 527–528; `raw_result` 529, 621; `files` 628; declared-tuple field vocabulary via `FEATURE_ALIASES` 638 + `FEATURE_KEYS` 156–157 (`handler_set, gap_kinds, gap_dependencies, be_argv, symlink_removed, published, extraction_failed`) — **field names inside the tuple agree** with the generator's `declared` (573–574); only the container key is mismatched. `(label, action)` extraction `_pair` 760–763.

## 3. Reader inventory — `c1-counter.py` (fixtures/c1-counter-r41.py)

**No overlap with the audited writer by construction:** its inputs are `.ufo/waves/round-41/c1/carriers.json` (280), `gap-rule.json` (281), `corpus/evidence/round-41/c1/<id>/after.json` (282, default receipt 1530), PROVINCE/knowledge/SOURCES (283–285) — none authored by `heldout-gen-v3.py`. So every c1 read below is "no writer in the audited writer set", with the real writer named. Receipt-side reads of `selection`/`locations` appear only in selftest fixture builders (2213, 2253, 2269, 2602–2603, 2657) and are **not** reads of the measuring code — excluded.

Spec reads (writer: L1's frozen `carriers.json` / gap rule): `claim` 503, 587; `structural` 506, 518; `allowed` 519, 532; `required` 533, 540, 546; `removed` 547 + `diagnostic` 552, `kinds` 553, `disposition` 554, `silent` 555, model 574–577; `carriers` 589; `target` 592; `projection` 594; `prior_pins` 598; per-carrier `id` 603, 610, 666; `sha256` 610, 666; `external` 617; `path`/`oracle`/`nonregular` 618–620; `receipt` 667; `oracle_root` 670.

Receipt reads (writer: REA 6.5.0 runtime; committed via `c1-run.sh`): `subject.digest.sha256` 1259, 1597–1599; `operation` 1601; `provider.id` 1600–1602; `evidence_id` 1672 (recomputed 389–396 via `tools/round-27/xpin-attribute.mjs`); `parameters.output_directory` 1642–1644 (provenance 768–778); `parameters.max_depth/max_output_bytes/max_output_files` 1403–1405, 1411–1412 (rerun replay); `normalized_result`: `files[].relative_path/sha256/size` 980–981, 1291–1295; `files[].mime_type` 1293; `files[].md5/sha1` 1246, 1295; `chunks[].handler` 1308; chunk `range.offset/length` 1308; `chunks[].extraction_failed` 990–993, 1309; `extraction_gaps[].kind/relative_path/dependencies/handler` 1075–1076, 1318, 1360; `unpublished_entries[].kind/relative_path` 1322–1325; `derivations[].parent_path/child_path/handler` 821–822, 865, 1358–1360; `depth_limited_paths[]` 817–818; `diagnostics[].report.__typename__/link` 910–911, 1334–1342; `diagnostics[].input_path` 1107, 1341; `engine.name/version` 1362–1364; `published_bytes` 1365; `coverage` 1366. Carrier superblock raw bytes 703–717 (layout probe, not JSON).

## 4. The M41-1 core, reproduced

- **Writer**: `declared` at 1372 (class) and 1464 (combo); the manifest's own `declared_schema.location` (1807–1823) documents `carriers[].declared` as the binding location.
- **Reader**: resolution chain 1497–1505 tries `class_expected.features` → `features` → `declared_features` → class map `man[decl_key][class]` (candidates 1487–1489). It never tries `declared`.
- **Static consequence**: class carriers resolve via `class_expected.features`; the 12 combos resolve to nothing → `feat_missing` → `observed_features_match_declared` false.
- **Empirical anchor (real freeze data)**: `corpus/evidence/round-41/c2/heldout/manifest.json` has 52 carriers; `carriers[-1]` (C12) writes `declared`+`declared_extras` with `class_expected`, `features`, `declared_features` all null; `carriers[0]` carries `class_expected.features` (8 subkeys). Score receipt `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`: `bindings.observed_features_match_declared = false`, `declared_features.source = "class_expected.features"`, `missing = C01..C12`, `by_class.combo = "declared-tuple-incomplete"` — exactly the round-41 lesson §Mistakes M41-1 and `## Routed defects` R41-CL1.

Aggravating factor (already in the lesson, visible in the code): the counter's own docstring (81–83) documents the manifest contract as "class_expected (label, action, features) or `features`" while the generator documents `carriers[].declared` — two seats froze two different written contracts, and the pre-freeze dry run exercised `c2-controls.py`, not the frozen counter.

## 5. Additional findings

- **F1 (defect-class, same interface, non-blocking): dead read `rea_params`** — c2-counter 1459 reads a top-level `rea_params` map; the generator writes `rea` (1803–1806) and per-carrier `rea` (1365/1460). Effect today: `res['advisory_rea_params'].declared` is always `{}` (binding explicitly `False`), so the advisory depth report is vacuous. Route to the round-42 counter: read exactly one declared-tuple key and fix or drop the advisory map.
- **F2 (fragile-by-design, no defect): fallback-only resolutions** — `envelope` (1243), `expected_label`/`expected_action` (1119–1120), `max_depth` (1471) are read but never written where they are read; all resolve only via designed fallbacks (inference from `carrier`; class-map missing bucket; advisory absence). Harmless today, but the round-42 one-key rule (R41-CL1) should also state where the envelope pointer and depth live, or the new counter inherits the same inference layers.
- **F3 (forward flag, R42C1Counter port)**: the port (artifacts/R42C1Counter/c1-counter.py, 1904-line diff vs r41) reads new per-carrier spec keys `handler` (must be one of `squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`) and a `superblock` block (`magic`, `endianness`, `variant`, `major`==3, `minor`, `compression`), and `claim` must equal `R42-C1`. **No writer of those keys exists yet** — the round-41 carriers.json shape lacks both, so every carrier fails spec validation (fail-closed, safe direction) until the C1 spec writer emits exactly this shape at the freeze. The port also reads `counter`/`counter_sha256` from score receipts (D4 sha-of-counter recording).
- **F4 (v4 standin generator)**: `R42C2Counter/standin-heldout-gen-v4.py` writes the one-key contract — `declared_features` as "THE ONLY declared-tuple key" (docstring 15–16, entry 242), and its selftest **fails** if any carrier carries `declared`, `features` or `class_expected` anywhere in the manifest (279–292). Probed against the r41 counter it resolves GREEN — but only through the r41 counter's *last* fallback (`declared_features`, counter:1502); the dead `rea_params` + five class-map candidates persist. `R42C2Gen/` is absent (no v4 generator draft beyond this standin), so the full v4 pair audit waits for the real `tools/round-42/{heldout-gen-v4.py,c2-counter.py}` drafts.

## 6. Checker deliverable — `key-audit.py`

Stdlib-only (`ast`/`argparse`/`json`/`tempfile`) static contract checker: extracts carrier-entry writer shapes (dict literals with the `{id, sha256}` fingerprint, null-ness + one level of subkeys) and the counter's declared-tuple resolution paths (two-pass dataflow over `.get()`/subscript chains in functions containing `observed_features_match_declared`, plus class-map candidate tuples) and fails when any shape has no resolving path. Documented limits: depth-2 paths, interior functions only, opaque-non-null for call-valued bindings.

| run | result | exit |
|---|---|---|
| `--selftest` (embedded fixed pair / broken pair) | `fixed want GREEN got GREEN [ok]` / `broken want RED got RED [ok]` | 0 |
| `--gen fixtures/gen-r41.py --counter fixtures/counter-r41.py` | **RED** — `build_carrier:1349` resolves via `class_expected.features` (counter:1498); **`build_combo_carrier:1443` UNRESOLVED**; dead reads `features` (1500), `declared_features` (1502); dead manifest keys `rea_params`, `class_features`, `classes_features`, `feature_tuples`, `features_by_class`, `class_tuples` | 1 |
| `--gen fixtures/gen-fixed.py --counter fixtures/counter-fixed.py` | **GREEN** — `build_class:18` and `build_combo:24` both resolve via `declared_features` (counter:14) | 0 |
| `--gen …/R42C2Counter/standin-heldout-gen-v4.py --counter fixtures/counter-r41.py` | GREEN via `declared_features` fallback (counter:1502); `rea_params` + 5 class-map keys still unwritten | 0 |

Fixed pair on disk (fixtures/gen-fixed.py, fixtures/counter-fixed.py) is the R41-CL1 target shape: ONE key `declared_features`, written by both entry shapes, read under exactly that key.

## 7. Round-42 draft status

- `artifacts/R42C2Gen/` — **absent** (nothing to audit yet).
- `artifacts/R42C2Counter/` — 4 standins; `standin-heldout-gen-v4.py` audited (§5 F4); `standin-sqfs-triage-v4.py`/`standin-indep-eval-v4.py` are interpreter/evaluator, not manifest readers; no v4 `c2-counter.py` draft exists.
- `artifacts/R42C1Counter/` — port audited (§5 F3); no interface with `heldout-gen` (separability holds).

## 8. Tooling record

No tools installed or upgraded (stdlib Python only, per operator 2026-10-19 channel order nothing was needed). No pacman transactions, no writes outside this seat's report + artifacts dir, no VCS mutation (read-only `git show`/`rev-parse` only).

## 9. Residual risk and verification gaps

- The checker is contract-scoped (declared-tuple resolution), not a full semantic audit; the complete read/write tables above were assembled by grounded reading of the pinned copies, not mechanically, so a key read via dynamic construction (`getattr`-style) would be invisible — none observed in these files.
- Envelope-side keys are attributed to the REA 6.5.0 runtime schema via the generator's passthrough; the envelope writer itself was not audited.
- The round-42 verdict on the real one-key pair awaits the `tools/round-42/{heldout-gen-v4.py,c2-counter.py}` drafts (`R42C2Gen` absent); re-run `key-audit.py --gen … --counter …` on them before freeze.
- c1-counter selftest-only fixture writes (`selection`, `locations`) were excluded from its read list by inspection; a future counter version that starts *reading* them would need them re-added.
