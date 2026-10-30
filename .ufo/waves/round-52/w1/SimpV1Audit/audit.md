# SimpV1Audit — dead weight in the v1 instruments (for the v2 port)

Scope: `tools/round-50/c1-counter.py` (4836 lines), `tools/round-50/c1-controls.py` (1817),
`tools/round-50-c3/sqfs-triage-v5.py` (2311). Lines are at base `c525de54`. Read-only; no lane
write. Method: AST reference counts over module names, grep for call sites across the lane,
existence checks of every path the counter names (`git cat-file -e c525de54:<path>`), and
offline runs (receipts in `receipts/`). "KEEP-with-question" = the L1 must confirm before anyone
drops it. Nothing marked DROP is claimed dead without a measured reference count or a claim text
that names the replacement.

Vocabulary: **DROP** = unreachable or superseded by the v2 claims text. **KEEP** = reachable and
claim-relevant. **Q** = KEEP-with-question. **MUST-CHANGE** = keep the idea, the constant/literal
moves to round-52.

## 1. Measured dead names (AST, zero or definition-only references)

| file:line | name | refs | call | why |
|---|---|---|---|---|
| c1-counter.py:396 | `PROV_SEGMENT = '/kaidoku-r50/'` | 1 (def) | DROP | only consumer is controls `consts()` fallback behind `PROV_BASE` (c1-controls.py consts) |
| triage-v5.py:291 | `DEFAULT_SKILL = LANE + '/SKILL.md'` | 1 (def) | DROP | `run()` takes `--rev`/`--skill`; the default is never read |
| triage-v5.py:1817 | `_missing_ids(entries)` | selftest only | DROP | returns `entry['envelope']`, asserted only against itself; production never calls it |
| c1-counter.py:1328 | `legacy_same_rel` | selftest probe (:3660) | Q | round-40 matcher kept as the *discriminator proof* for path probes; not a production path. Drop only with the probe rows |
| c1-controls.py:85 `RECEIPT_CLAUSES` | 2 refs | Q | used once; tied to the v1 receipt-derived green/red check that the v2 control set drops |

## 2. Names that name a clause or path that does not exist (dead aliases / candidates)

| file:line | item | evidence | call |
|---|---|---|---|
| c1-controls.py:91 `CLAUSE_ALIASES['marker']` | `'marker_ok'`, `'superblock_ok'` | neither string occurs in c1-counter.py (0 hits); the counter's clause is `layout_ok` | DROP the two dead alias names (the table itself is only used by the v1 control arms) |
| c1-counter.py:388-389 `PRIOR_PIN_CANDIDATES` | `tools/round-50/prior-pins.json`, `tools/round-49/prior-pins.json` | ABSENT at c525de54 (only `tools/round-42/prior-pins.json` exists) | DROP the two absent candidates. Q: keep the round-42 entry (it is the only one that exists) |
| c1-counter.py:391-392 `REA_PKG_CANDIDATES` | `tools/round-50/rea-pkg.json`, `tools/round-49/rea-pkg.json` | ABSENT at c525de54 (only `tools/round-42/rea-pkg.json` exists) | DROP the two absent candidates. Q: keep round-42 |
| c1-counter.py:386-387 `PRIOR_CARRIER_TABLES` | `.ufo/waves/round-41/c1/carriers.json`, `tools/round-49/carriers.json` | both EXIST | KEEP (the claim's anti-replay source); add `tools/round-50/carriers.json` per the claim |

Note the selftest cases that write `tools/round-50/rea-pkg.json` (c1-counter.py ~:3010-3050 area,
"rea-pkg pin edited after the freeze", "no rea-pkg pin at the freeze") exercise a path that is
absent in the real lane. They are synthetic-only and must be re-pointed, not copied.

## 3. Round-50-specific literals that must move to round-52 (MUST-CHANGE, not drops)

- c1-counter.py:393 `OPENED_DATES = ('2026-10-28','2026-10-29')` → `('2026-10-30',)` per the claim.
- c1-counter.py:396-397 `PROV_BASE = '/fast/scratch/hyaku/kaidoku-r50/'`; :485 `scratch_root()`
  literal `'kaidoku-r50'`; c1-controls.py consts() and `--work` default `'kaidoku-r50'`; triage-v5
  is clean of this literal but its docstring predicate names it.
- c1-counter.py:404 `COUNTER_PATH = 'tools/round-50/c1-counter.py'`; :425
  `FROZEN_PREFIXES = ('tools/round-50/',)` → `tools/round-52/`. Keep round-50 as frozen input only.
- c1-counter.py:393 window and the `ENTRY`/`STEM`/`CORE_HEADING`/`FRONTIER_MARK` constants (round-50 strings; line not re-read, grep the symbol).
- triage-v5.py:317 `INSTRUMENT_RELPATH = 'tools/round-50-c3/sqfs-triage-v5.py'` and :319
  `FROZEN_TOOL_TREES` → `tools/round-52/`.
- triage-v5.py:1256 `'other_tools_round50_changed'` and :1280 — rename to round-52 key.
- triage-v5.py:2109, :2117, :2194 — selftest reads `plans/round-50-attempt2-claims.md` and asserts
  a predicate fragment. Re-point to `plans/round-52-claims.md`.
- triage-v5.py:298-306 `PREDICATE` — the same sentence must be rewritten to the R52-C2 predicate
  (claim requires it verbatim in claims, docstring and receipt).

## 4. v1 control arms: DROP for the v2 pre-freeze set

The claim's pre-freeze controls are exactly: CTL-OLD (reproducibility, 2 of 4), CTL-NEW (4 of 4),
CTL-DN (do-nothing), CTL-JUNK (impossible rule), M1–M4 rule mutations, and the retry control.
Every item below serves a v1 arm the claim does not name, or needs a live REA run, which
"no REA runs this wave" forbids.

| file:line | item | call | reason |
|---|---|---|---|
| c1-controls.py:432 `argv = ['npx','-y', REA_PIN, ...]` | DROP | violates the counter's own S1 rule (no npx); the counter owns the rerun |
| c1-controls.py:69 `REA_PIN`; :73 `REA_ATTEMPTS = 5`; :74 `LAST_ATTEMPTS = {}` (global, mutated at ~:461) | DROP | `REA_ATTEMPTS=5` disagrees with the counter's `MAX_REA_ATTEMPTS=3` (c1-counter.py:1923); the retry policy belongs to the counter only |
| c1-controls.py:380 `stripped_path`; :413 `capture_real`; :465 `rehome`; :472 `mint_ids`; :503 `real_receipt` | DROP | REA dev-arm capture; no REA this wave |
| c1-controls.py:529 `forge_receipt` | DROP | oracle-only forgery is the c2 arm, not a claim control |
| c1-controls.py:918 `spec_c3`; :943 `spec_c4` | DROP | need a live REA capture (sasquatch-absent; standard-LE via REA). The layout clause is covered by CTL-OLD/M-set rule scoring without REA |
| c1-controls.py:837 `spec_c1b` | DROP | "EXTRA ARM, not in the default set"; reads round-41 L3 paths at the round-50 base |
| c1-controls.py:981 `import_receipt`; :1043 `spec_pos`; :1070 `spec_pos_lane`; :1785 `--pos-from-lane`; :1787 `--pos-envelopes` | DROP | STAND-IN POS reads the lane's own round-50 landing at `DEFAULT_BASE_REV` (:67, `7c678ae6`); no positive control of this shape is in the claim. Q: if the L1 wants a post-freeze positive, it is a fresh build, not this code |
| c1-controls.py:1095 `spec_c2x` | Q | "ATTACK ARM, informational" (oracle + removal-list forgery). Useful to the falsify wave; not a pre-freeze control. Needs `forge_receipt` (DROP) so DROP with it unless the L1 keeps forgery |
| c1-controls.py:108-110 `K1_PATH`, `FOREIGN_SOURCES`, `TEMPLATE_RECEIPT` | DROP | round-36/round-41 receipt sources; consumed only by DROP arms |
| c1-controls.py `spec_c1` (`FOREIGN_SOURCES` consumer) | DROP | copies round-41 BE receipts into LE slots (CTL-C1-1) |
| c1-controls.py `spec_c0` | KEEP | do-nothing, the analog of CTL-DN |
| tools/round-50/control-fixtures/{c0..c4,pos} (committed) | leave frozen | under the frozen `tools/round-50/` tree; cannot be removed (freeze-drift) |

## 5. Counter flags with no in-lane caller

| file:line | flag | evidence | call |
|---|---|---|---|
| c1-counter.py:2526 `--no-rerun` | KEEP | the claim text names it ("`--no-rerun` … exits 2 `rerun_disabled`") |
| c1-counter.py:2527-2528 `--selftest-rea`, :2529 `--dev-image` | DROP (Q) | real-REA dev arm; the docstring says "Not exercised by the porting seat"; no caller in the lane; forbidden this wave |
| c1-counter.py:2530 `--verify-receipt` | Q | no caller in any round-50/round-52 script (grep: hits only in other rounds' artifacts). Identity is already proven in-process by `write_receipt` (~:557-569). Drop unless the L1 wants an external verifier |
| c1-counter.py:595 `find_rea_pkg` | DROP (Q) | searches the npm `_npx` cache — the ambient resolution the S1 rule forbids; reached only by `--selftest` with no `--pkg65` |
| c1-counter.py `lane_le_avm_image` (~:4597) and `selftest_rea` (~:4630) | DROP (Q) | only consumers are the `--selftest-rea` arm above; mksquashfs-built image is a dev fixture |
| c1-counter.py:2520-2522 `--work` help and default | MUST-CHANGE | default names `kaidoku-r50` |

## 6. Triage v5: DROP for v6

| file:line | item | call | reason |
|---|---|---|---|
| triage-v5.py:230 `MARKER_V4`; :231 `REFUSED_MARKERS`; :599-611 `parse_skill` v4 fallback | DROP (Q) | the v4 fallback is the v5 red-before witness. Claim's do-nothing is the v5 table at base (v5 marker present at base) so the fallback never runs at base |
| triage-v5.py:1420 `VOCAB_V4`; :1427 `V4_ROWS` (15 rows); :1462 `_v4_full_rows`; :1833 `c_v4_table_is_red_before` (selftest); :1802 `do-nothing-v4` in `emit_mutant`; :1703 `do-nothing-v4` control | DROP | red-before witness for a table v6 no longer reads; replaced by v5-at-base do-nothing per the claim |
| triage-v5.py:1673 `corpus_control` two-scope design | KEEP | the corpus scope is the honest non-vacuity evidence (see §8 finding 3) |
| triage-v5.py:2268 `--print-v5-block`, `--emit-mutant` | KEEP (Q) | keep the flags, rename to v6 |

## 7. Triage v5 bindings that cannot fail, and features the v6 claim needs but v5 lacks

These are not drops. They are where "reachable" and "claimed" disagree.

- **`evaluator_missing` binding is vacuous.** triage-v5.py:1301 `except Exception` wraps
  `evaluate(feat)`. `evaluate()` (:923) never raises: `features()` always sets every key it reads.
  So `evaluator_missing` is `[]` by construction and the claim's `evaluator_missing 0` cannot go
  red. Either prove it can fail (a fixture with a malformed tuple that makes evaluate raise) or
  state in the claim that the binding is structural.
- **Freeze-drift is report-only.** triage-v5.py:1256-1281 computes `frozen_path_changed` as
  `other_tools_round50_changed` and `instrument_unchanged`, but `run()` never exits 2 on them. The
  claim's "freeze-drift **gating** (routed defect 3)" is absent in v5. This is ADD, not port.
- **No executability audit and no census clause exist in v5.** The claim's `executability_violations`
  and `census_outside` bindings have no implementation to port. Both are ADD.
- **Counter lacks the ENOENT retry, `law_shape_ok`, `census_rederived_ok`, `depth_gap_recorded`,
  `re_scored_pins`.** All are ADD.

## 8. Defects and tensions the L1 must see before the freeze

1. **The round-51 v6 draft does not parse.** `.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py:288`
   contains the edit-tool residue `CUT 1033.=1033` inside the Python source (`SyntaxError`, measured).
   Do not port from it without repair.
2. **Naive ddwrt move is wrong (measured offline, no REA).** Putting `squashfs_v3_ddwrt` into
   `NO_READER_FAMILIES` (triage-v5.py:~ NO_READER_FAMILIES) flips 8 corpus labels: the failed body
   `dmg_Z3_v3ddwrt_inode_table` to `no-reader-failure`, **and seven clean `*_ddefault` envelopes to
   `clean-unverified`**, which contradicts the claim's "keep `clean`". Removing ddwrt only from
   `READER_BACKED_V1V3` flips exactly one envelope (`dmg_Z3`) to `body-extractor-failure`, not to the
   new row. The v6 route must add a dedicated `legacy-body-unreadable` step between v5 precedence 7
   and 8 and must not touch `NO_READER_FAMILIES`.
3. **The no-reader failure branch is vacuous on the corpus.** Run of v5 on the 126-envelope corpus:
   `pair_mismatches 0`, 17 rules, label distribution has **no `no-reader-failure` row at all**
   (clean-unverified 19, legacy-body-failure 7, …). The branch is exercised only by the selftest
   fixture `v2ns-failed`. The claim's "v6 flips the FAILED-body pair" is measured on the one ddwrt
   envelope only. Disclose this when the audit counts violations.
4. **Retry tension.** The counter maps REA `provider_timeout` exhaustion to `RerunEnvError` (exit 2,
   `measure`), while the claim says an exhausted projection failure is "missed" (exit 1). The claim
   does not state exit for provider-timeout exhaustion. Ask the L1 which.
5. **Retry count mismatch.** Controls `REA_ATTEMPTS = 5` (c1-controls.py:73) vs counter
   `MAX_REA_ATTEMPTS = 3` (c1-counter.py:1923).
6. **`npx` survives in the controls** (c1-controls.py:432), contrary to S1.
7. **Round-41 `marker_ok`/`superblock_ok` alias names** (c1-controls.py:91) never existed in the counter:
   the alias table was written for a different counter.

## 9. Measured evidence (receipts in `receipts/`)

- Triage v5 on the frozen 126-envelope corpus at `c525de54`: exit 0, `pair_mismatches 0`,
  `evaluator_missing 0`, 17 rules. Receipt `receipts/v5-corpus.json`, stdout sha256
  `291c93b0c714692c73faa67de98fdbb93459b8d90a57564abcf75fe66c045413`.
- Counter offline selftest (`tools/round-50/c1-counter.py --selftest`): exit 0, 169 cases,
  green_ok 17, red_ok 152. Uses the simulated REA runner; the only external process is the node
  xpin evidence-id helper. No `extract-firmware` run. stdout sha256
  `77dd01728df021c95c39b7192959460101b7952963fe529710313392e46e37ff`.
- Not run: controls selftest, REA, any carrier read, `--selftest-rea`, any unsquashfs/sasquatch run.

## 10. Tools

Installed: none. `pyflakes` was already at `/home/vgpnk/.local/bin/pyflakes`; not run (AST scan
used instead). No PATH directory touched.
