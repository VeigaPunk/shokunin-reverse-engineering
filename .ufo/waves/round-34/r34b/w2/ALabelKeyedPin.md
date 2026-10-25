# ALabelKeyedPin — is the pinned-but-unregistered `readers/label_keyed.py` (a) inert pin, (b) dropped-to-CLEAN, or (c) coverage hole?

Verdict first: **(a) inert extra pin** — with one bookkeeping consequence (a fresh F3 instance) and one naming consequence (an F2-adjacent ambiguity), both already covered by the disclosed defect ledger. **It does not affect the stop.**

All commands below ran in scratch copy `/fast/scratch/hyaku/kaidoku-r34b/w2/ALabelKeyedPin/repo` (byte copy of `tools/round-34/`); lane tree untouched, no VCS mutation. Readers ran only as `python3` subprocesses via a counter (the frozen counters or the frozen `replay-gate.py`). Timestamps UTC at run time.

## 1. Committed state

- `label_keyed.py` sha256 `f727c1527052d1fdefb909ac07a8912ee410cdcfcb045cea956fff803038351a` is pinned in `claims[0].pins` (`.ufo/waves/round-34/r34b/claims.json`) and in the `instruments` map of `.ufo/waves/round-34/r34b/instruments.json`. The two maps are byte-identical 26-entry sets (verified by dict comparison, script in §5).
- It is registered in **neither** `gate-config-mini.json` nor `gate-config-naive.json`: both list the same 8 readers (positive `structural` + 7 shortcut classes). `grep -rn label_keyed tools/round-34` → only the file itself; the C2 counter's red clause checks class name `"label-memorization"` (`c2-shortcut-gate-counter.py:116`), i.e. `label_replay_full.py`.
- History: `git log --follow -- tools/round-34/mini-fix/readers/label_keyed.py` → exactly one commit, `c79bbe7b` (the freeze itself, msg: "…seven shortcut classes, red and green configs"). It was never registered in any committed config — "dropped" is not supported by history either.
- The reader (committed bytes): selects `TEMPLATE.get(os.path.basename(sys.argv[1]), [])`; TEMPLATE covers only `alpha.mrec` (1 of its 3 records) and `gamma.mrec` (1 of 5).

## 2. Measured scores (scratch copy, frozen bytes)

| reader | counter | matched | met_target | exit |
|---|---|---|---|---|
| label_keyed | mini-counter, seed `kaidoku-r34-mini-v1` | 0 | false | 1 |
| label_keyed | mini-counter, seed `alt-1` | 0 | false | 1 |
| label_keyed | mini-counter, seed `alt-2` | 0 | false | 1 |
| label_keyed | naive-counter | 0 | false | 1 |
| label_replay_full (registered `label-memorization`) | mini-counter | 0 | false | 1 |
| label_replay_full | naive-counter | 8 | true | 0 |
| structural | mini-counter | 8 | true | 0 |

Exact argv: `python3 -I -B tools/round-34/mini-fix/{mini,naive}-counter.py --root . --control-reader tools/round-34/mini-fix/readers/<r>.py [--seed <s>]`, run 2026-10-25T07:32–07:33Z from `/fast/scratch/hyaku/kaidoku-r34b/w2/ALabelKeyedPin/repo`.

Zero on the green surface is structural, not luck: `mini-counter.py:114` passes `opaque-<sha20>.data` as basename; `TEMPLATE.get` therefore returns `[]` for every fixture. Zero on the red surface is because both memorized rows are partial (alpha 1/3 records, gamma 1/5) so `canonical` equality fails even with intact basenames.

## 3. Would registering it flip a clause? (the (b) test)

Wrote `files/gate-config-{mini,naive}-pluslabel.json` in scratch: the frozen config plus an eighth shortcut `{"class":"label-keyed","path":"tools/round-34/mini-fix/readers/label_keyed.py"}`. Commands, 2026-10-25T07:33Z:

- `python3 -I -B tools/round-34/replay-gate.py --root . --config ../files/gate-config-mini-pluslabel.json --json-out /tmp/green-pluslabel.json` → `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=8`, exit 0; rows: structural 8/8 met; `label-keyed` 0/8; `label-memorization` 0/8.
- `python3 -I -B tools/round-34/replay-gate.py --root . --config ../files/gate-config-naive-pluslabel.json` → `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_over_target=label-memorization`, exit 2; `classes_over_target` unchanged (label-keyed not in it).

So its absence cannot have manufactured CLEAN: registering the pin leaves every clause value identical. Not (b).

## 4. Domination (the (c) test)

AST `ast.literal_eval` of both TEMPLATE dicts on the committed files: `label_keyed`'s output set is a strict subset of `label_replay_full`'s for every label (alpha: 1 of 3 rows; gamma: 1 of 5; other six labels: ∅ ⊆ full). Both key on `os.path.basename(sys.argv[1])` — the identical input channel. Therefore any input where `label_keyed` meets a target, the registered `label-memorization` also meets it; the class can never be the unique witness and its omission hides no channel. Not (c) — the channel is scored. (Note this is the opposite of the actual stop falsifier: `nameset.py` is a basename-independent, permutation-invariant SONAME-multiset key — an unregistered channel.)

## 5. Consequence for the stop

- Reproduced the decisive counterexample on the scratch copy: `nameset.py` sha256 `2e8feaea92eedb8d73e80c098d39534e5e7755b81d32babf38029ee4e2a88b97` (matches `claim-stop.json`), `mini-counter --control-reader ../files/nameset.py` → matched 8, `met_target: true` on all three seeds, exit 0, 2026-10-25T07:33Z. The stop's falsification stands independent of this pin.
- The stop's "registered seven classes stay below the green target" remains literally true; even counting the unregistered pinned ninth reader it is still "below target" (0/8), so the sentence is not weakened by the pin.
- The pin is a live instance of **F3** (registered-set ≠ pinned-set invisible; pins pin files, classes exist only in config text): a pinned shortcut program exists that no predicate exercises. It also collides with **F2**: `c2-shortcut-gate-counter.py` predicate (lines 23–27) says the red case's "label-keyed memorization meets its target", while the clause checks class `label-memorization` → `label_replay_full.py`; the file literally named `label_keyed.py` is not the reader in that role and never meets a target. A reader of the predicate could believe `label_keyed.py` was exercised and failed; it was neither.
- Repair direction for the L1 (not landed here): assert `pinned reader files ⊆ registered reader paths` (or delete the pin); optionally rename the predicate phrase to match the registered class.

## Final verdict

VERDICT: `tools/round-34/mini-fix/readers/label_keyed.py` is an **inert extra pin** — pinned in both 26-entry pin maps, registered in no config, unreachable by either counter, scoring 0/8 on both frozen surfaces, and strictly dominated by the registered `label-memorization` reader on its own channel. Not a class dropped to reach CLEAN (registration flips no clause; verified) and not a coverage hole (the basename channel is scored by the registered superset). It does not affect the stop; it adds a second instance to disclosed defects F3 (pin/config asymmetry) and F2 (predicate naming vs. exercised reader).

No tools installed; no installs needed.
