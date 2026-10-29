# RevC1MissReceipt — R50-C1 landed receipt, field-by-field re-derivation (wave 4, falsify)

Seat: RevC1MissReceipt (leaf). Scope: re-derive `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`
against the frozen counter `tools/round-50/c1-counter.py` at freeze
`435d41fd4ad9211d1579fc447936fb33d2b74467`, receipts commit `646d29c9df4ef77499248f95589cb9526c6dea19`,
lane tip per assignment `c67b741e8f6bd8d64adbdb15e059d47fde004c77` (live HEAD has since advanced to
`db61a907`; the receipt, entry, tables, and counter are unchanged between them — verified below).

## Verdict

**RECEIPT HOLDS. Every re-derivable field reproduces exactly; there is no STOP finding.**
209/209 recomputed fields match, 14/14 `bindings` keys match, `bindings_false` reproduces as exactly
`['province_core_section','province_core_row']`, all four evidence ids recompute to the stored values,
`counter_sha256` is triply confirmed, and the measured miss (2/4, exit 1) is independently reproduced.
One minor doc-accuracy finding (SCORECARD row overclaims the rerun; §3) — the scoring verdict is
unaffected.

## 1. Field-by-field re-derivation

Method: imported the frozen counter (byte-identical copy of the freeze blob) as a module and re-ran
every clause that does not invoke REA, from the pinned carrier bytes in the frozen cache, frozen
tables via `git show FREEZE:path`, and the committed envelopes via `git show REV:path`. Full
transcript: `RevC1MissReceipt/rederive-out.txt` (209 OK, 0 DIFF), harness: `RevC1MissReceipt/rederive-c1.py`.

| Receipt field | Landed value | Re-derived | Result |
|---|---|---|---|
| `revision` | `646d29c9df4ef77499248f95589cb9526c6dea19` | receipts commit exists; ancestor of tip `c67b741e` | OK |
| `freeze` | `435d41fd4ad9211d1579fc447936fb33d2b74467` | FREEZE commit; ancestor of receipts commit | OK |
| `predicate` / `target` / `projection_profile` | `P50-C1` / `4` / `plus-extractor` | frozen carriers.json (`claim`, `target`, `projection`) | OK |
| `carrier_ids` | `[g7581, g7582, c6490, c6430]` | frozen carriers.json order | OK |
| `rea_parameters` | `{max_depth:1, max_output_bytes:536870912, max_output_files:100000}` | frozen carriers.json | OK |
| `counter_sha256`, `counter_frozen_sha256` | `9820811bf29f…9bd813` | `git show 435d41fd:…/c1-counter.py \| sha256sum` = worktree = tip blob = receipt value (`RevC1MissReceipt/counter-sha-checks.txt`) | OK |
| `frozen_path_changed` | `[]` | module's own `frozen_drift()`: no M/D/R/T/U on frozen paths in `435d41fd..646d29c9`; no A under `tools/round-50/`; no A of any freeze-existent path; all 9 named frozen blobs byte-identical freeze↔rev | OK |
| `carriers_unchanged` / `gap_rule_unchanged` | `true` / `true` | blobs byte-identical freeze↔rev | OK |
| `frozen_tables_valid` / `tables_absent_at_freeze` | `true` / `[]` | carriers.json + gap-rule.json parse at freeze; all 8 oracle/nonregular tables exist at freeze | OK |
| `carriers_spec_problems` / `gap_rule_problems` | `[]` / `[]` | module's `carriers_spec()` / `gap_rule_model()` | OK |
| `prior_pins` | 18 pins (sorted) | union of `carriers[].sha256` from `.ufo/waves/round-41/c1/carriers.json` + `tools/round-49/carriers.json` and `pins` from `tools/round-42/prior-pins.json`, all at freeze, via module's `prior_pins()` | OK |
| `prior_pin_sources` | 3 files | same (round-50 carriers.json has no `prior_pins` key; `tools/round-49/prior-pins.json` absent at freeze) | OK |
| per-carrier `carrier_present/pin_ok/fresh_ok/layout_ok/compression/carve_ok` | e.g. all true, `[4,4,4,4]` | sha256 of cached bytes == frozen pins; superblock probe (`hsqs`, v4.0, xz, `mkfs_time==bytes_used`, table starts); carve `length==bytes_used==size` | OK ×4 |
| per-carrier `oracle_ok` / `oracle_files` / `oracle_rederived_ok` | 3955/4709/4556/4564, all true | frozen TSVs parse; fresh `/usr/bin/unsquashfs` 4.7.5 re-extraction (counter's exact `rederive_oracle`, scratch dir) equal to the frozen table in both directions, all four carriers | OK ×4 |
| per-carrier `receipt_present/digest/adds/first_add/fresh` | digests `30db72bd…/2c21f264…/ff481957…/f250f315…`, adds `[646d29c9]` | `git show REV:corpus/evidence/round-50/c1/<id>/after.json` sha256 == receipt digest; `git log -m --full-history --diff-filter=A` first add = receipts commit, a strict descendant of freeze | OK ×4 |
| `evidence_digests` | 4 path/sha256 pairs | equal to per-carrier `receipt_digest` and to recomputed digests | OK |
| per-carrier envelope clauses (`evidence_envelope_ok`, `subject_pin_ok`, `operation_ok`, `handler_ok`, `chunks_ok`, `extract_root*`, `oracle_hits_ok` 4556/4564/4709/3955 hits, `extra_published []`, `nonregular_unpublished_ok`, `path_shape_ok`, `run_provenance_ok`, `parameters_ok`, `diagnostics` 3/3/1/1, `removals`) | as landed | recomputed with module helpers against committed envelopes | OK ×4 |
| per-carrier `gaps_ok` / `gaps_note` | c6430/c6490 `true`; g7581/g7582 `false` with the dev/pts note | module's `disposition_check()` against envelope `extraction_gaps` + `diagnostics` and frozen nonregular tables/gap rule | OK ×4 |
| per-carrier `evidence_id_ok` | all true | recomputed via frozen `tools/round-27/xpin-attribute.mjs` + rea-agents 6.5.0 package (package.json sha256 `a5003023…` matches receipt `rerun_toolchain.rea.pin`); stored ids `ev_f42519…/ev_9f0bfa…/ev_eb2df4…/ev_f7a3a3…` recompute exactly | OK ×4 |
| per-carrier `matched` | c6430/c6490 true; g7581/g7582 false | conjunction of the 23 frozen `CLAUSES` (all true for the two Cable carriers; `gaps_ok` false, and `projection_ok` false, on the two 758x) | OK |
| `carriers_matched` | `2` | count of matched == 2 | OK |
| `failing` | `[g7581:gaps_ok, g7581:projection_ok, g7582:gaps_ok]` | g7581 false clauses = gaps_ok + projection_ok; g7582 = gaps_ok only; sorted per `failing_lists()` | OK |
| `met_target` | `false` | `carriers_matched(2) != target(4)` and two bindings false | OK |
| `exit_code` | `1` | `0 if met_target else 1` (frozen main) | OK |
| `bindings` (all 15 keys) | see receipt | recomputed with module regexes/section parsers against `git show REV:…` (PROVINCE, entry, SOURCES, README, carriers.json, gap-rule): `RevC1MissReceipt/bindings-rederive.txt` | 14/14 OK, `frozen_tables_valid` inherited |
| `bindings_false` | `['province_core_section','province_core_row']` | PROVINCE at rev has no `## Round-50 additions to Core` heading (the landed section is `## Round-50 measured, not promoted (R50-C1 honest stop)`); hence row binding false with `province_core_rows_seen []` | OK |
| `opened_source_rows` / `entry_source_ids` | `[S243,S244,S245,S249]` | entry `source:` lines name exactly those S-ids; each SOURCES row is opened `2026-10-28` and its used-by cites the entry | OK |
| `entry_present` / `coverage_map_row` / `frontier_note` | true/true/true | entry blob exists at rev; README `## Coverage map` row maps the stem; PROVINCE line 448 carries the mark, the stem, and `LE-AVM` | OK |
| `compression_detail` | `[4,4,4,4]` | layout probe of the four cached byte sets | OK |
| receipt file identity | — | worktree sha256 `e1e0ac17…` == `git show HEAD:…` blob; counter `--verify-receipt` exit 0, `{"ok": true}` (`RevC1MissReceipt/receipt-identity.txt`) | OK |

## 2. The g7581/g7582 asymmetry, from the receipt's own fields

- **g7581** fails three clauses: `gaps_ok=false`, `projection_ok=false`, hence `matched=false`.
  `projection_error` records the counter's own fresh REA rerun dying with `execution_failure`:
  unblob ENOENT on `readlink '…/rea-firmware-Ft6F7W/extracted/firmware.bin_extract/usr/www.myfritz/avme/cgi-bin/luacgi'`
  (a dangling symlink inside unblob's own extract tree), exit 1, `retryable: false` — the frozen
  counter retries only `provider_timeout`, so this is scored, not retried.
- **g7582** fails only `gaps_ok=false`; its rerun succeeded (`projection_diff []`), so
  `projection_ok=true`.
- **Common miss cause**: each 758x frozen nonregular table carries 13 `char-device` rows
  (`dev/pts/0-7` = `136:0-7`, `dev/tiatm` = `230:0`, `dev/led` = `247:0`, `dev/ttyp0-2` = `3:0-2`).
  The frozen rule marks `char-device` required and silently admits only `247:0`, so `dev/led` is
  admitted and the other 12 have neither a gap nor a `MaliciousSymlinkRemoved` removal in the
  committed envelopes (envelope `extraction_gaps`: 636 `unpublished-entry` + 1 `depth-limited`,
  none under `dev/*`). The two Cable carriers have a single `247:0` char-device each → `gaps_ok` true.
- **Note truncation**: `gaps_note` prints `sorted(missing)[:8]`, i.e. only `dev/pts/0..7`; the
  "twelve char-device entries with no disposition" stated in the README coverage row and the entry
  is nonetheless exact (12 = 13 required − 1 silent; verified against envelope gap paths).

## 3. Findings

1. **MINOR — doc accuracy (SCORECARD.md:3796).** The attempt-2 row says "the counter's rerun
   reproduced every projection". The receipt itself records `projection_ok: false` for g7581
   (execution_failure above). `PROVINCE.md:442` states it correctly ("reproduced the projection on
   three carriers and failed on g7581 … whose projection stays unverified — the miss does not
   depend on it"). Recommend the L1 amend the SCORECARD row to the PROVINCE wording. The scoring
   verdict is unaffected: `gaps_ok` alone makes g7581 miss, so the flake is not load-bearing.
2. **NOTE — rerun flakiness is disclosed but worth re-measuring next round.** g7581's committed
   envelope shows a complete extraction (4556/4556 oracle hits, `oracle_ok` true), so the rerun
   `ENOENT` is environmental (unblob's own tree), not a property of the pinned bytes; g7582's
   identical-by-class bytes reran green. Recorded as a receipt field; honest.

No STOP findings. All fields named in the seat spec reproduce.

## 4. Not re-run (seat bounds) and residual risk

- The C1 counter's full predicate command invokes REA and is **not** run here (L1 owns it). The
  three green `projection_ok` values (c6430/c6490/g7582) are therefore checked for internal
  consistency only (`ok=true`, `projection_diff=[]`, toolchain pinned in `rerun_toolchain`);
  g7581's is verified from its recorded `projection_error`.
- Frozen counter offline `--selftest`: **exit 0 — 169 cases, `green_ok` 17, `red_ok` 152**
  (run from the lane worktree, writes only under scratch `--work`; transcript
  `RevC1MissReceipt/selftest-out.txt`).
- Carrier bytes were read from the shared cache `/fast/scratch/hyaku/kaidoku-r50/carrier-cache`
  after verifying each file's sha256 against the frozen pins; the lane tree was not written.

## 5. Artifacts (`.ufo/waves/round-50/w4/RevC1MissReceipt/`)

- `rederive-out.txt` / `rederive-c1.py` — 209-field comparison (0 DIFF) + harness
- `bindings-rederive.txt` — all-bindings comparison (ALL EQUAL)
- `counter-sha-checks.txt` — freeze/tip/worktree counter sha256
- `receipt-identity.txt` — receipt sha256 (worktree==HEAD) + `--verify-receipt` exit 0
- `c1-counter-frozen.py` — byte-identical copy of the freeze counter used for the re-derivation
- `selftest-out.txt` / `selftest-err.txt` — frozen counter offline selftest

Selftest (frozen counter, offline): **exit 0 — 169/169 cases** (`green_ok` 17, `red_ok` 152), 2026-10-29T21:48Z.
