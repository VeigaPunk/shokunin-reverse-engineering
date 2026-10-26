# R41C2Mutants — mutation sweep of the round-40 C2 tooling round 41 keeps

**Verdict: CONFIRMED** — all 12 documented round-40 survivors (5 counter, 7 interpreter) reproduce
byte-for-byte on the round-41 base `49096c7e` and still survive their detectors; this report delivers
the exact selftest case (inputs + expected) that kills each of the 11 actionable ones, verified
empirically against pristine and mutant copies (11/11 killed), plus **11 new mutants** on the clauses
v3 adds (contains-form parsing, evaluator-vs-table comparison, class_expected binding,
restore-does-not-unblock), all killed by their own new cases, plus 1 new mutant (N14) the existing
battery already pins. One correction to the round-40 report: its suggested M11 kill case does not
work as specified; the working kill needs a `matched`-field assertion (evidence below).

## 1. Scope, detectors, base bytes

- Attacked: what round 41 keeps from round 40's C2 tooling — `tools/round-40/c2-counter.py` and
  `tools/round-40/sqfs-triage-v2.py` at the lane base `49096c7e6f226af0c750c4b003be58883cb6049f`
  (extracted via `git show 49096c7e:…` into scratch; worktree files are byte-identical to the base
  blobs: `9bd792494ca042d840371e525ed6ea6a1f841f68415e4c405c41c13057183dd1` and
  `336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617`).
- Detector D-selftest: `python3 -I -B <copy> --selftest`. Pristine counter: exit 0,
  `{"cases": 42, "green": 11, "red": 31, "pass": 42, "fail": 0}`. Pristine interpreter: exit 0,
  `SELFTEST cases=45 pass=45 fail=0`.
- Detector D-heldout (interpreter only, re-derivation evidence): the 26 committed held-out envelopes
  against the base `SKILL.md` blob (`926dac301cf0281e2b35b6736b6f6ee869a0a1b415fd5207f9de3959c4ca0054`)
  — pristine 26/26, every survivor 26/26 (survives both detectors, as documented in round 40).
- All mutants are scratch copies under `/fast/scratch/hyaku/kaidoku-r41/R41C2Mutants/`; the lane was
  never written. No sandbox clone needed (the counter reads the lane read-only; the selftest builds
  its own throwaway git fixtures under `$HYAKU_SCRATCH/kaidoku-r40`).

## 2. Re-derivation on the base bytes — 12/12 documented survivors confirmed

| Mutant (r40 id) | Locus (single logic change) | D-selftest at base | D-heldout at base |
|---|---|---|---|
| M02-regen-seed-vacuated | `regenerated_seed_matches_freeze` := True | exit 0, 42/42 → **survives** | n/a (counter) |
| M03-regen-digest-dropped | regen compare drops regenerated sha vs manifest pin | exit 0, 42/42 → **survives** | n/a |
| M04-regen-arm-dropped | regen compare drops regenerated arm vs manifest arm | exit 0, 42/42 → **survives** | n/a |
| M11-pair-match-label-only | `pair_match` compares label only | exit 0, 42/42 → **survives** | n/a |
| M19-writer-sha-vacuated | `writer_matches_manifest` := True | exit 0, 42/42 → **survives** | n/a |
| M05-last-marker-wins | marker scan keeps going (last v2 marker wins) | exit 0, 45/45 → **survives** | 26/26 → survives |
| M07-none-set-cell-accepts-any | set cell `none` accepts any values | exit 0 → **survives** | 26/26 → survives |
| M15-repeated-set-member-accepted | repeated-member check disabled | exit 0 → **survives** | 26/26 → survives |
| M26-string-provider-ignored | bare-string provider forced `''` | exit 0 → **survives** | 26/26 → survives |
| M28-blank-line-walk-disabled | blank-line walk between vocab and header disabled | exit 0 → **survives** | 26/26 → survives |
| M30-nr-diagnostics-be-source-dropped | BE command source `normalized_result.diagnostics` dropped | exit 0 → **survives** | 26/26 → survives |
| M10-fnmatch-normcase | `fnmatchcase`→`fnmatch` | exit 0 → **survives** | 26/26 → survives |

Raw outputs: `artifacts/R41C2Mutants/derive-results.json`; mutant sources `artifacts/R41C2Mutants/mutants/`.
M10 is **POSIX-equivalent**, re-confirmed by probe on this host: `os.path.normcase` is the identity
(`squashfs_v4_BE` unchanged) and `fnmatch` ≡ `fnmatchcase` on all four probe calls
(`squashfs_v4_{BE,be}` vs `squashfs_v4_?e` → False/False, True/True). Not actionable in this lane;
platform note only.

## 3. Exact selftest cases the v3 counter must add (kill the 5 counter survivors)

Method: the cases were added to a scratch copy of the base counter
(`artifacts/R41C2Mutants/counter_case_patch.py`, patches P1–P9; cased copy in the patch script's
output `counter-cased.py`), pristine runs **48/48 pass** (42 original + 6 new), then each mutant was
re-derived on the cased copy and must fail exactly its own case. Per-case pristine receipts
(`counter-cased-pristine-debug.err`, `C2CASE_DEBUG=1`):

| New case (name in the counter's case grammar) | `build()` params | want | Pristine observed | Mutant kill signal |
|---|---|---|---|---|
| `regenerated manifest seed is foreign` | `regen_seed='0'*64` (stub generator writes a foreign `seed` into the regenerated manifest while still deriving carrier bytes from `--seed`) | exit 1, false: `regenerated_seed_matches_freeze` | exit 1, `bindings_false=['regenerated_seed_matches_freeze']`, matched 8 | M02: binding True → `not false (got True)` + `want exit 1 got 0` → **KILLED** |
| `committed carrier and pin tampered together` | `muts={'pin_swap'}` (H01 body → `b'pin-swap-body'`, manifest pin and envelope digest updated to match, so only the *regenerated* bytes disagree) | exit 1, false: `carriers_regenerated` | exit 1, `['carriers_regenerated']`, matched 8 | M03: regen sha compare dropped → all green, exit 0 → **KILLED** |
| `manifest arm flipped against regeneration` | `muts={'arm_flip'}` (H01 `arm` → `before`; regen says `after`) | exit 1, false: `carriers_regenerated` | exit 1, `['carriers_regenerated']`, matched 8 | M04: arm compare dropped → exit 0 → **KILLED** |
| `wrong expected action on both carriers of one class` | `muts={'wrong_action_both'}` (H03+H04 `expected_action` → `install-extractor`) | exit 1 **and receipt `matched == 6`** | exit 1, `['carriers_regenerated','row_decisions_consistent']`, matched 6 | M11: matched 8 ≠ 6 → **KILLED** (see correction below) |
| `declared writer sha does not match the freeze blob` | `gen_obj='good'`, `writer_decl='{"path": "tools/round-39/gen-squashfs.py", "sha256": "f"*64}'` (committed manifest declares a writer digest; the freeze blob is absent) | exit 1, false: `writer_matches_manifest` | exit 1, `['writer_matches_manifest']`, matched 8 | M19: binding True → exit 0 → **KILLED** |
| `frozen path edited then restored before rev` | `frozen_restore=GEN` (mid-range commit edits `tools/round-40/heldout-gen-v2.py`; the claim commit restores the exact freeze bytes) | exit 2 | exit 2, `frozen_path_changed`, matched None | N01 (tip-only scan): diff `freeze..rev` empty → full green pipeline → `want exit 2 got 0` → **KILLED** |

**Correction to the round-40 M11 suggestion.** R40W2C2CounterMutants.md proposed "wrong
`expected_action` on both carriers of one class → pristine exit 1 on the pair mismatch alone; with M11
it exits 0". That is not reachable in this fixture grammar: a label-right/action-wrong expected pair
always shares its interpreter row with the true pair of the same label, so `row_decisions_consistent`
fires under the mutant too, and the regen cross-check also compares expected pairs
(`carriers_regenerated` fires as well — pristine observed `['carriers_regenerated',
'row_decisions_consistent']`). The working kill asserts the receipt's **`matched` field** (6 pristine
vs 8 under M11), which required a small harness extension (optional 7th case element `want_matched`,
patch P5). Verified: M11's cased battery fails exactly that one assertion.

Harness extensions the v3 counter port must carry for these cases (all in
`counter_case_patch.py`): stub-generator seed override (P1/P2), `pin_swap`/`arm_flip`/
`wrong_action_both` fixture mutations (P3a/P3b), edit-then-restore commit support (P4a/P4b),
`want_matched` case element (P5a/P5b), writer-declaration injection into the committed manifest's
generator object (P7/P8). Mutant sources: `artifacts/R41C2Mutants/cased-mutants/`; verdicts
`counter-case-results.json`.

## 4. Exact selftest cases the v3 interpreter must add (kill the 6 actionable interpreter survivors)

Verified against the real v2 tool (pristine passes, mutant fails) with the tool's own fixture helpers
(`artifacts/R41C2Mutants/interp_case_driver.py`, results `interp-case-results.json`); restated in v3
grammar inside `artifacts/R41C2Mutants/v3-interp-preview.py` (selftest 17/17, including all six).
For v3, swap the marker string for `<!-- sqfs-triage-table v3 -->`; everything else is identical.

| Case | Fixture (marker + vocabulary line + rows; envelope) | Expected (pristine) | Mutant observed |
|---|---|---|---|
| `K-M05-two-markers-first-wins` | craft section with **two** v3 markers, each followed by a full table (row `first-table`, then prose, then row `second-table` action `inspect-input`); envelope: any in-domain envelope (H01 analog) | exit 0, pair `(first-table, none)` | M05 → `(second-table, inspect-input)` |
| `K-M07-none-set-cell-rejects-nonempty` | rows: `trap` (`gap kinds=none`, deps `*`, handler `squashfs_v4_le`, files `>0`, action `inspect-input`) **before** `right` (`gap kinds=unpublished-entry`, deps `none`, files `>0`, action `count-gap`); envelope: G={unpublished-entry}, D=∅, P=1, H={squashfs_v4_le}, SR=no | exit 0, pair `(right, count-gap)` | M07 → `(trap, inspect-input)` |
| `K-M15-repeated-set-member-rejected` | row `dup` with `gap kinds=unpublished-entry+unpublished-entry`; envelope: clean analog | exit 2 (malformed set cell) | M15 → exit 0, `(unclassified, none)` |
| `K-M26-string-provider-used` | row `strprov` provider `unblob`; envelope with `"provider": "unblob"` as a **bare string** (minimal `normalized_result`) | exit 0, pair `(strprov, none)` | M26 → `(unclassified, none)` |
| `K-M28-blank-lines-tolerated` | vocabulary line, then **two blank lines**, then header/separator/row `x`; envelope: clean analog | exit 0, pair `(x, none)` | M28 → exit 2 |
| `K-M30-nr-diagnostics-be-source` | row `avmR` (handler `squashfs_v4_be`, gaps `extractor-failure`, deps `none`, be `no`, files `0`, action `preserve-failure`); envelope whose sasquatch command appears **only** under `normalized_result.diagnostics[].report.command` (no `-be` token, no `data.diagnostics`, no `raw_result`), G={extractor-failure}, P=0, H={squashfs_v4_be} | exit 0, pair `(avmR, preserve-failure)` (BE=no ⇒ AVM row) | M30 → `(unclassified, none)` (BE falls back to `n/a`) |

M10 (`fnmatchcase`→`fnmatch`): no case can kill it on this host — POSIX-equivalent (§2 probe).
Record as a platform note, not a test gap.

## 5. New mutants on the clauses v3 adds — 11 derived, all killed (+1 already pinned)

New mutants N01/N14 target the **real base counter** (the restore-does-not-unblock machinery already
exists there: `frozen_changes` walks `git log freeze..rev -- FROZEN` and any hit raises
`Unevaluable('frozen_path_changed')` → exit 2). N04–N07 target the contains-form clause and N08–N13
the evaluator-vs-table and class_expected clauses of a **v3 reference preview** written only from the
draft claims' text (`v3-interp-preview.py` selftest 17/17, `v3-counter-preview.py` selftest 7/7 —
previews are reference targets for the cases, not the contract). Every mutant is a single-logic
string replacement; every kill is its own case; pristine previews pass everything.

| New mutant | Clause | Locus | Killed by (case) | Verdict |
|---|---|---|---|---|
| N01-frozen-scan-tip-only | restore-does-not-unblock | `frozen_changes` range walk → `git diff --name-only freeze rev` (net-change detection) | counter case `frozen path edited then restored before rev` (§3 last row) | **KILLED** (real base code) |
| N14-unevaluable-exit-1 | restore-does-not-unblock (exit shape) | Unevaluable receipt `exit_code` 2→1 | **existing v2 battery** (9 failures: receipt `exit_code` 1 ≠ process exit 2 on every exit-2 case) | killed — positive pin, no new case needed |
| N04-contains-parsed-as-exact | contains-form parsing | contains cell matched as exact set (`payload <= frozenset(values)` → `==`) | `c_combined_partial_in_tree` + `c_combined_depth_in_tree` (2-member gap sets must match `⊇` rows) | **KILLED** |
| N05-contains-accepted-in-deps-column | contains-form parsing | `⊇` accepted in the `dependencies` column (grammar scope widened) | `c_contains_in_deps_rejected` (exit 2 expected) | **KILLED** |
| N06-contains-repeated-member-accepted | contains-form parsing | repeated-member check disabled for contains cells | `c_contains_repeated_member_rejected` + `c_repeated_set_member_rejected` | **KILLED** |
| N07-rules-reversed | contains-form parsing / precedence | `classify` iterates `reversed(rules)` (last match wins) | `c_combined_partial_mixed` + `c_combined_depth_mixed` (partial/depth precedence beats mixed) | **KILLED** |
| N08-evaluator-compare-label-only | evaluator-vs-table | pair comparison drops the action half | `c_eval_action_deviates_generator_agrees` (evaluator and generator agree on a wrong action; table has the right one) | **KILLED** |
| N09-evaluator-crash-backfilled | evaluator-vs-table | crashed evaluator backfilled from the table's own answer (scoring the table against itself — the D3 failure mode) | `c_evaluator_crashes` | **KILLED** |
| N10-evaluator-first-replicate-only | evaluator-vs-table | comparison samples only the first replicate per class | `c_eval_deviates_on_second_replicate` | **KILLED** |
| N11-class-expected-dropped | class_expected | binding vacuated | `c_generator_label_disagrees` | **KILLED** |
| N12-class-expected-not-gating | class_expected | binding recorded but excluded from `bindings_ok` (reported, not failed) | `c_generator_label_disagrees` (exit must be 1) | **KILLED** |
| N13-class-expected-first-replicate-only | class_expected | binding samples only the first replicate per class | `c_generator_disagrees_on_second_replicate` | **KILLED** |

Mutant sources and verdicts: `artifacts/R41C2Mutants/preview-mutants/`,
`preview-mutant-results.json`; drivers `preview_mutant_driver.py` (anchors asserted unique, count==1).

## 6. v3 preview assumptions (for re-anchoring if the freeze differs)

- Contains syntax [INFERENCE from the draft's "no contains-operator" control]: set cell `⊇kind[+kind…]`
  in the `gap kinds` column only; `*`/`none`/exact `a+b` unchanged from v2.
- Label precedence encoded as row order per the draft's 12 rules; new label `depth-limited-nested`
  with action `audit-depth` [INFERENCE — the draft fixes no action for it]; evaluator action map =
  v2 actions + `audit-depth` [INFERENCE].
- The counter preview compares (label, action) pairs from a stub interpreter ("table") and a stub
  independent evaluator (its own map, never the table), over a JSON fixture — the real v3 counter
  keeps git-based fixtures; only the clause logic and cases transfer.

## 7. Integrity

- Lane never written by this seat. Tracked hashes before == after the whole battery:
  `tools/round-40/c2-counter.py` `9bd79249…83dd1`, `tools/round-40/sqfs-triage-v2.py`
  `336c621c…b8617`, `SKILL.md` `926dac30…0054` == base blob. `git status --porcelain` shows only
  untracked sibling outputs (`.ufo/waves/round-41/`, `corpus/evidence/round-41/`, `tools/round-41/`,
  `plans/round-41-claims.md`) — none created by this seat. No git/jj mutation of any kind.
- Tooling installed: **none** (python3 stdlib + read-only git; no pacman/uv/npx/cargo activity;
  sasquatch, sasquatch-v4be, unblob untouched; no vendor bytes downloaded or copied).
- Mutant files are scratch copies; every mutation was applied with a unique-anchor assertion
  (count==1) and the pristine copy re-verified green before/after each battery.
- Scratch `/fast/scratch/hyaku/kaidoku-r41/R41C2Mutants` and this seat's fixture leftovers under
  `$HYAKU_SCRATCH/kaidoku-r40` removed at the end; cited evidence copied to
  `artifacts/R41C2Mutants/` (2.0 MB, all files < 5 MB).
- Disclosure: the `$HYAKU_SCRATCH/kaidoku-r40` cleanup swept stale `gen.*`/`c2-counter.*`/
  `sqfs-triage-v2-selftest.*`/`c2-case.*` entries modified within the last 4 h (1365 entries, the
  bulk of them this seat's ~12 counter-selftest runs, which the round-40 tool itself never removes).
  Because that directory is shared, a concurrent sibling running the same counter battery in that
  instant could have had in-flight fixture dirs removed; peer `T49MutC2Counter` was warned to rerun
  if its battery saw sudden fixture errors. No lane or VCS state was touched by the sweep.

## 8. Limits

- Single-logic textual mutants only; no compound mutants. Detector = `--selftest` (+ D-heldout for
  interpreter re-derivation); the counter's real-run detector at `42c10a58` was not re-run — the
  round-40 wave-2 report already covers it and the base bytes equal the round-40 freeze blob for both
  files.
- The five counter kill cases and the restore fixture require the small `build()`/harness extensions
  of §3; they are delivered as patches, not as edits to any lane file (the L1 integrates).
- Preview-based verdicts (N04–N13) are kills *of my preview*; they demonstrate the cases are
  load-bearing for the clause semantics as drafted. If the frozen v3 grammar differs (e.g. a different
  contains token), the cases re-anchor mechanically but the mutant strings must be re-derived against
  the frozen code — that re-derivation is the natural wave-2 follow-up once v3 exists.
