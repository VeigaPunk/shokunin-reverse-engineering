# CriticGate — round-22 counter gate registry / self-invocation / two-evidence contract

Seat `KaidokuR22R.CriticGate-6` (critic, leaf). Author-side review only; not outside admission.
Judged on: coverage, calibration. Lane read-only; every mutation ran in a private clone.

## Subject under attack

- Gates: `.ufo/waves/round-22/tools/count-c1.py` (sha256 `5fbc6868…dd61`) and `count-c2.py` (`ded1a0e8…642e`) at `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67` (= lane HEAD, worktree bytes identical). Both were changed after the freeze commit `75f04a4` (`git diff 75f04a4 2ee3d9f`). Those changes add the SOURCES registry linkage to C1, `row.probe == row.verb` to C2, and `--selftest` to both. `frozen/count-c*.py` are byte-identical to the `75f04a4` sources (`d7f67075…`, `d3bec8db…`).
- Contract: `SKILL.md:679-691` ("Round-22 measurement registry", rows `round22-C1` :683, `round22-C2` :684, `round22-capture-probes` :685). Governing clauses: `PROTOCOL.md:380-406` (Verdict, Self-test, Two evidences, Registry).
- Claims: `claims.json:15` (sourced), `:20-21` (C1 after_target/falsifiers), `:31-32` (C2), `:36` (separability). Disposition table: `PROVINCE.md:172-199`. Rules being sharpened: `corpus/QUALITY.md:39-40` (rows 29, 30).

## Commands and observed exits

Harness `/tmp/criticgate-r22/harness.py` (sha256 `5cd317b0…b068`). I ran `python3 -I -B /tmp/criticgate-r22/harness.py` and it exited 0 in 22.5 s. Scratch: `git clone -q --no-hardlinks <LANE> /tmp/criticgate-r22-ygumr_3c/lane`, detached at `2ee3d9f`. The full argv, exit, stdout summary and stderr tail for each of the 30 runs are in `.ufo/waves/round-22/w2/CriticGate.json`. No REA call, no device, no target execution and no install. Only these two report files were written to the lane.

| id | argv (counter, root, rev) | exit | observed |
|---|---|---|---|
| X0-c1-B | lane `count-c1.py`, lane, `7787fea` | 1 | k=0 |
| X0-c1-H | lane `count-c1.py`, lane, `2ee3d9f` | 1 | k=1 `[identify-flutter-build]` |
| X0-c2-B | lane `count-c2.py`, lane, `7787fea` | 1 | accounted 0 |
| X0-c2-H | lane `count-c2.py`, lane, `2ee3d9f` | 0 | accounted 14, mismatched [], foreign [] |
| X1 | c1, scratch commit with `corpus/SOURCES.md` deleted | **1** | no JSON; stderr `kaidoku_r20_mention_helpers.Refusal: command_failed git exit=128: fatal: path 'corpus/SOURCES.md' does not exist` |
| X1b | c2, scratch commit with `inspect-packet-fields.json` = 200000 nested `[` | **1** | no JSON; stderr `RecursionError: Stack overflow … while decoding a JSON array` |
| X1c | c1/c2, rev `deadbeef×5` | 2 / 2 | `unevaluable` (holds) |
| X2 | c1, entry `source:` reduced to `S053 <own evidence path>` | 1 | **k=1 still** |
| X2b | successor c1, S051–S053 status `mined`→`candidate` | 1 | k=0 (successor discriminates) |
| X3 | c1 at `2ee3d9f`, *uncommitted* worktree edit making r21 `bind` return unbound | 1 | **k=0** (same rev, output still names `2ee3d9f`); restored → k=1 |
| X4 successor | `count-c1.py --selftest` | 0 | `counter_controls_clean` 6/6 |
| X4 mutants | drop `mined` / drop opened-date / drop S051 floor / used-by → any S051+ row / exit2→1 | **0 ×5** | all `counter_controls_clean` |
| X4 effect | drop-`mined` mutant on X2b commit | 1 | **k=1** where successor gives 0 |
| X5 successor | `count-c2.py --selftest` | 0 | `counter_controls_clean` 7/7 |
| X5 mutants | ok-field ignores value / ok-empty always true / drop placement / drop reason / ignore foreign_rows / receipt_absent→matched / exit2→1 | **0 ×7** | all `counter_controls_clean` |
| X6 | c2, frida receipts with `devices: []` and `processes: []` | 0 | **14/14** |
| X7 | c2, every `.run.json` and `runs.json` deleted | 0 | **14/14** |
| X8 | `--selftest` on a copy staged outside a lane tree (as `verify.py:45-50` stages) | 1 | `IndexError: 4` |

The lane itself was read only. I checked all 15 `evidence/c2/*.run.json` files: each `stdout` equals its receipt bytes, and the five ADB runs carry `{'REA_ADB_PATH': '/usr/bin/false'}`. The current receipts are therefore consistent; the problem is that the gate never checks this.

## Findings

### F1 — Unevaluable inputs exit 1 (`failed`), violating the declared verdict map (fixable defect; calibration)
- Counterexamples: X1 and X1b, both exit 1 with a traceback. `SKILL.md:683-684` declares 2 = unevaluable, and `PROTOCOL.md:380-383` fixes 1 = `failed` fleet-wide. A missing SOURCES file or an over-deep receipt is therefore graded as a failed measurement.
- C1 cause: `count-c1.py:44`, `:54` and `:69` call `r20.git_show`, which raises `r20.Refusal` (a plain `Exception`, `round-20/tools/verb-coverage.py:42-61`), outside the only `except r20.Refusal` (`count-c1.py:39-42`). The `main` handler at `:107` does not catch it either.
- C2 cause: `count-c2.py:98-101` catches only `ValueError`, and `:170` omits `RecursionError`. C1 includes `RecursionError` at `:107`, so the two counters are inconsistent.
- Smallest correction:
  - C1: extend the `try` at `count-c1.py:39` to cover `:43-74`.
  - C2: add `RecursionError` to `count-c2.py:100` (giving `receipt_unevaluable`) and to `:170`.
  - Add one fixture case for each to `counter-fixtures.py`.

### F2 — The self-test does not pin the predicates the registry advertises (fixable defect; coverage and calibration)
- C1: four mutants that each delete one registry subpredicate (`count-c1.py:47`: `>= 51`, `== "mined"`, `== "2026-10-21"`; `:57` used-by path) all pass `--selftest` (X4). X4-effect shows this matters: the drop-`mined` mutant counts 1 where the successor counts 0.
- The only source negative is `source: none` (`counter-fixtures.py:77-78`). The checklist at `SKILL.md:687-689` and `QUALITY.md:39` ("opened, mined row whose used-by names that entry") is therefore unproven by any self-test.
- C2: seven mutants pass (X5). Every fixture row uses `error:capability_unavailable` (`counter-fixtures.py:63-66`), yet three of the 14 real rows depend on the `ok-empty`/`ok-field` branches (`PROVINCE.md:189,191,192`; `count-c2.py:111-117`). Those branches, `bad_placement` (:88-89), `missing_reason` (:90-91), `receipt_absent` (:95-97) and the `foreign_rows` exit rule (:174) are all untested.
- Neither counter's exit-2 path is exercised, although the registry declares it and the CounterSelfInvocation seat required an invalid-revision case.
- Smallest correction (fixtures only, expected values fixed by hand):
  - C1: `status_not_mined`, `opened_other_date`, `pre_round_id` (S050), `used_by_other_path` (each exit 1, k 0); `sources_absent` and `invalid_rev` (exit 2).
  - C2: `ok_empty_nonempty` and `ok_field_wrong_value` (`observed_mismatch`); `bad_placement`; `missing_reason`; `receipt_absent`; `foreign_row` (exit 1, count 14); `invalid_rev` and `deep_receipt` (exit 2 or `receipt_unevaluable`).

### F3 — C1's self-test asserts no stable finding-id (fixable defect against `PROTOCOL.md:385-387`)
- `counter-fixtures.py:131-132` treats `data['claim']` as `finding_id`, but that field is the constant `"R22-C1"`. `count-c1.py:76-89` emits no `finding` on the 0/1 paths, and `expected_status` is `None` for every C1 case (`:74,88`). Any JSON carrying `claim: R22-C1` with the right count passes.
- C2 checks status only for `T2[0]` (`:130`).
- Smallest correction: emit `finding` (`t1_complete` / `t1_incomplete`) plus a per-target status from `count-c1.py`, and assert the finding per case. For C2, assert the mutated verb's status and that the other 13 are `matched`.

### F4 — C1's verdict is not a function of the revision it names (fixable defect; two-evidence revision identity)
- `count-c1.py:26-30` and `:34-35` load the round-21 and round-20 helpers from `Path(root)/<path>`, which is the *worktree*, not `REV`.
- X3: at the same `--rev 2ee3d9f`, an uncommitted helper edit moves k from 1 to 0, and the output still reports `"rev": "2ee3d9f…"`. This contradicts `PROTOCOL.md:392-394` ("A verdict names the revision it was measured against").
- `verify.py:52-53` checks that B, REV and the worktree agree only inside the producer run. The registered standalone command (`SKILL.md:683`) pins no helper digests.
- Smallest correction: load both helpers from `git show REV:<path>` into a temp module (or pin their SHA-256 in `count-c1.py` and exit 2 `helper_tampered` on mismatch), and list them under the row's pinned values.

### F5 — The registered self-invocation depends on its location and tests worktree fixtures, never REV (fixable defect)
- `count-c1.py:99-100` and `count-c2.py:159-160` derive the lane root from `Path(__file__).parents[4]`, and `counter-fixtures.py:117-118` copies its dependencies from that live tree.
- X8: the same script staged outside a lane exits 1 with `IndexError: 4`, which is neither clean nor 2. `verify.py:45-50` deliberately stages REV copies and so cannot use the registered `--selftest`. It calls the fixture module directly, and that path is not what `SKILL.md:683-684` registers.
- Smallest correction: give `--selftest` an explicit `--root`, read fixtures and dependencies via `git show <rev>:` (or pin their digests), and map setup failure to exit 2.

### F6 — The two-evidence obligation has no retained green half, and the red half's provenance is unpinned (fixable; calibration)
- Current authored evidence is only `verify/before-c1.json`, `before-c2.json` (09:39) and `red-C1.json`, `red-C2.json` (09:51:39.12 / .41). No retained successor self-test green, no after-measurement, and no `verify.py` output (no `summary.json`) exist. `QUALITY.md:39` requires "same-fixture red/green outcomes", and the uncommitted `corpus/lessons/round-22.md:23-24,59-60` describe the green as future work.
- The red receipts' argv name `tools/count-c*.py`, which now hash to the successor. File mtimes show `frozen/` created at 09:51:39.41, after `red-C1.json` (09:51:39.12), and successor edits at 09:51:58 and 09:52:06. `counter-fixtures.py` was edited at 09:54:13, after both red runs.
- [INFERENCE] The red runs used the pre-edit bytes at the `tools/` path. Re-executing the retained argv today gives `counter_controls_clean`, exit 0 (my X4/X5 successor runs), so each receipt contradicts its own argv. The receipts carry no counter digest or source rev. Their expected tuples do match the current fixtures (checked).
- `verify.py:62` runs red against worktree `root/W/frozen/…` rather than `git show rev:`, and `frozen/` is missing from the digest loop at `verify.py:47-50`.
- `frozen/` holds counter source, not an input snapshot with an `expected.json` of digests, so under `PROTOCOL.md:395-397` it is at best `unpinned (legacy)`. There is no name collision: `find .ufo/waves -path '*/frozen/*' -name 'count-c*.py'` finds only round-22.
- Smallest correction:
  - Add `frozen/count-c1.py` and `frozen/count-c2.py` to the `verify.py:47` digest loop.
  - Execute the red runs from `git show rev:` copies.
  - Run `verify.py` at a named commit and commit its output.
  - Annotate the existing red receipts as "pre-edit bytes at the tools/ path, digest unrecorded", or supersede them with the producer's digested red runs.

### F7 — Self-citation satisfies the source registry (tradeoff for the judge; coverage)
- X2: an entry whose `source:` line is only `S053`, the own-work row whose anchor is the entry's own evidence file (`corpus/SOURCES.md` S053), still counts k=1.
- `claims.json:15` is literally met. However, the source gate then adds no authority beyond the evidence binding it is supposed to accompany.
- Correction, if "sourced" is meant as more than linkage: require at least one cited row with kind other than `own-work` (`cells[3]`). Otherwise, state "linkage only, own-work rows suffice" in the `SKILL.md:683` row.

### F8 — C2's `ok-field` observations are weaker than the reasons beside them (fixable; calibration)
- X6: `devices: []` and `processes: []` still match 14/14 and exit 0. `PROVINCE.md:191-192` say "Provider successfully enumerated local descriptors" and "returned local process names/PIDs".
- The observed predicates (`cleanup_error=null`, `device_id="local"`) do not bind those claims. This violates the spirit of `QUALITY.md:40` ("a parsed empty list is scoped…").
- Smallest correction: add grammar `ok-nonempty:<path>` at `count-c2.py:111-117`, and set rows 191/192 to `ok-nonempty:devices` / `ok-nonempty:processes`. Otherwise, narrow the reason text to what is checked.

### F9 — Producing records are not bound, so the false-client control is unenforced (fixable; calibration)
- X7: deleting every `.run.json` and `runs.json` leaves 14/14 and exit 0. `PROVINCE.md:175-177,181` assert that the ADB rows are `REA_ADB_PATH=/usr/bin/false` controls and that each argv/env sits beside its receipt. `count-c2.py:87-121` checks neither, so a receipt produced by the real adb with device contact would be indistinguishable.
- `cutter-command-missing.run.json` has no `env_overrides` key, and its argv (`ffffffff-…`, `0`) is not issued by the registered producer `capture-probes.py:30` (which produced `cutter-command.json`, `VALIDATION_ERROR`). That receipt comes from an unregistered producer (`SKILL.md:685`).
- Smallest correction: in `check()`, require a sibling `<stem>.run.json` at REV with:
  - `stdout ==` the receipt text;
  - `argv[:4] == ['npx','-y','rea-agents@6.5.0',verb]`;
  - for `*adb*` verbs, `env_overrides == {'REA_ADB_PATH':'/usr/bin/false'}`;
  - on failure, status `run_record_mismatch`.

  Also add the missing-session request to `capture-probes.py`, or register its producer.

### F10 — The registered C1 gate gives the same exit before and after (tradeoff; coverage)
- X0: B exits 1 with k=0, and the final tree exits 1 with k=1. The claim's discriminator (k≥1) exists only in the `verify.py:59` lambda. `SKILL.md:683` admits this, so under `PROTOCOL.md:412-414` the registered gate is permanently red and the admitting predicate is unregistered.
- Smallest correction: add `--min-exercised N` (0 when count ≥ N) to `count-c1.py` and register it as the claim entry, or register `verify.py` as the claim gate.

## Not falsified (tried)
- An invalid revision returns exit 2 `unevaluable` for both counters (X1c).
- missing_source and probe_alias are now caught by the successors (X4/X5 successor).
- The registry rows carry all eight `PROTOCOL.md:401-403` fields.
- Receipt bytes equal the retained `.run.json` stdout for all 15 receipts.
- Not examined (other seats cover them): heading-prefix spoof and duplicate sections in C2, and the C1-only/C2-only separability matrix.

## Impacted axes
- coverage: F2, F3, F4, F7, F10.
- calibration: F1, F2, F6, F8, F9.

## Blockers / installs
- None. No tool installed or updated.
