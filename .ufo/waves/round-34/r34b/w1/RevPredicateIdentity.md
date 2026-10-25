# RevPredicateIdentity — word-level predicate identity (R34-C2)

Seat: reviewer. Mode: read-only on the lane; every executable probe ran on a copy under
`/fast/scratch/hyaku/kaidoku-r34b/w1/RevPredicateIdentity/`. No lane file was written except this
report. No tool installed or upgraded this wave (nothing needed; `python3` = `/usr/bin/python3`,
Python 3.14.8).

Revision facts (read-only): `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD`
→ `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (exit 0, 2026-10-25T07:19Z). `claims.json`,
`replay-gate.py`, `c2-shortcut-gate-counter.py` are byte-identical to their frozen blobs at
c79bbe7b (sha256 compared, exit 0). All 25 instrument pins in `claims.json: pins` verify (25/25 OK).

Inputs, full sha256 of the predicate strings (computed 2026-10-25T07:20:17Z):

| where | sentence | sha256 | words |
|---|---|---|---|
| `claims.json` `claims[0].predicate` | **A** | `7c6c17f0cca6c680507d4eec33b4c0c82a76c4f73e9a98ceb4bde54a9a96279b` | 31 |
| `gate-config-mini.json` `predicate` | A (identical) | same A | 31 |
| `gate-config-naive.json` `predicate` | A (identical) | same A | 31 |
| `c2-shortcut-gate-counter.py` `PREDICATE` | **B** | `8340aea51154fc0e4e2c00684a12893603677c5caa7769d7e63b70f5392611c8` | 46 |
| `after/c2-at-instruments.json` `predicate` | B (identical) | same B | 46 |
| all five `controls/*.json` `predicate` | B (identical) | same B | 46 |
| `mini-fix/mini-counter.py` `PREDICATE` | **C** = "P34-mini-records: eight equal-size synthetic record-chain fixtures decode to exactly their expected name/flags/value records on opaque permuted copies; only record-array traversal associates a name with its record." | `09988625205de2eb…` | 28 |
| `replay-gate.py` docstring line 2 | "P34-shortcut-replay: pre-freeze structure-blind replay gate." | n/a (label + 6-word tail, no obligation) | 8 |

A (claims, verbatim): *"P34-shortcut-replay: a finite structural-decoding counter is frozen only
after registered structure-blind shortcut readers are scored under the counter's own predicate and
none meets the target, while a registered structural reader does."*

B (counter, receipt, verbatim): *"P34-shortcut-replay: the committed replay gate refuses the
shape-only counter whose label-keyed memorization meets its target, clears the identity-defeating
counter on the same eight fixtures where every registered shortcut class stays below target, and its
selftest kills every mutant of its own refusal, positive-control and shortcut-floor branches."*

## 1. Word-level diff, A vs B (difflib on whitespace tokens)

| op | A fragment | B fragment |
|---|---|---|
| replace | `a finite structural-decoding` | `the committed replay gate refuses the shape-only` |
| replace | `is frozen only after` | `whose label-keyed memorization meets its target, clears the identity-defeating counter on the same eight fixtures where every` |
| delete | `structure-blind` | — |
| replace | `readers are scored under the counter's` | `class stays below target, and its selftest kills every mutant of its` |
| replace | `predicate` | `refusal, positive-control` |
| replace | `none meets the target, while a registered structural reader does.` | `shortcut-floor branches.` |

A and B share only the label `P34-shortcut-replay:` and the tokens `the`/`target`/`and`/`counter`.
There is no word-level identity: 0 of 31 A-words map contiguously beyond isolated function words.
A vs receipt and A vs the five control receipts are the same diff (receipts carry B).

## 2. The frozen `predicate_identity` field is falsified as written

`claims.json claims[0].predicate_identity` asserts: *"The same sentence is the gate config's
`predicate` field, the C2 counter's PREDICATE constant and the receipt label; …"*.

- "gate config's `predicate` field" — **true** for both configs (identical to A).
- "the C2 counter's PREDICATE constant" — **false**: the constant is B, not A.
- "the receipt label" — **false twice**: the receipt has no `label` key at all, and its `predicate`
  field is B, not A (verified: receipt keys are `clauses, exit, finding, gate_path, gate_present,
  green, measured_revision, met_target, mutants_killed, predicate, red, selftest_exit,
  selftest_line, selftest_failures, target`).
- "the gate's own verdict lines are the frozen labels REPLAY_GATE_CLEAN / REPLAY_GATE_REFUSED /
  REPLAY_GATE_UNEVALUABLE" — **true** (`replay-gate.py:14-17` docstring and `evaluate()` returns).

## 3. No instrument evaluates predicate identity (probes)

Copy of the pinned tree at `/fast/scratch/…/RevPredicateIdentity/repro`; each mutant is an isolated
copy. Command shape (identical for every row, `cwd` = mutant root):
`python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <mutant> --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33 --json-out <mutant>/receipt.json`

| probe | mutation | exit | line result | met_target | UTC |
|---|---|---|---|---|---|
| baseline | none (pinned bytes) | 0 | `GATE_COUNTER_OK … clauses_failed=-` (identical to `after/c2-at-instruments.txt`) | true | 07:19:04Z |
| M1 | green config `predicate` replaced by `P34-NOT-THE-FROZEN-SENTENCE: nothing here is registered.` | 0 | OK | true | 07:19:12Z |
| M2 | red config `predicate` = `""` | 0 | OK | true | 07:19:15Z |
| M3 | green config `shortcuts` trimmed 7 → 3 classes | 0 | OK, `shortcuts_below_target=3` | true | 07:19:17Z |
| M4 | counter `PREDICATE` rewritten to `P34-UNREGISTERED-CLAIM: …` | 0 | OK; receipt echoes the unregistered text | true | 07:19:20Z |
| M5 | counter `TARGET` += `"green_positive_matched": 9` | 0 | OK; receipt `target.green_positive_matched=9` while clause passes at matched=8 | true | 07:19:46Z |

Mechanism (code, not inference): `replay-gate.py:43` only asserts the key `predicate` **exists** in
the config (`for key in ("predicate", …): if key not in value: raise`); the value is never read,
never compared, never emitted — the gate payload is `verdict/finding/rows/classes_over_target` plus
`config`/`root` paths only (`replay-gate.py:291-311`). The C2 counter writes
`receipt = {"predicate": PREDICATE, "target": TARGET, …}` (`c2-shortcut-gate-counter.py:73`) with no
comparison to the config, to C, or to `claims.json`. `freeze-integrity.py` checks only `pins`
sha256s (`freeze-integrity.py:457-467`) — no predicate text.

Consequence: the receipt's `predicate` field is an echo of whichever constant the counter file
carries; it can never evidence which predicate was applied. The identity is documentary only, and
the documentary claim is false.

## 4. Target fields vs `TARGET` dict vs receipt clauses

| item | set |
|---|---|
| `claims.json` `target` | `green_positive_matched, green_verdict, mutants_killed, red_verdict, selftest_failures` |
| counter `TARGET` | `green_verdict, mutants_killed, red_verdict, selftest_failures` |
| receipt `target` | identical to counter `TARGET` |
| kill_rule clause list | `gate_present, green_clean, green_positive_meets_target, mutants_killed, red_refused, selftest_clean` |
| receipt `clauses` | identical to kill_rule (6/6, names and count) |
| counter `clauses` | identical to kill_rule (6/6) |

- **Clause-name identity: PASS.** The kill rule's six clauses appear verbatim and complete in both
  the counter and the receipt.
- **Target-field identity: FAIL.** `claim.target − receipt.target = {green_positive_matched}`;
  `claim.target == receipt.target` is `False`. The claim asserts these are equal; they are not.
- **Clause the frozen target names that the counter does not evaluate as a target**: the positive
  control threshold. `clauses.green_positive_meets_target` is computed as
  `receipt["green"]["positive_matched"] == 8` — a hardcoded literal
  (`c2-shortcut-gate-counter.py:121`), not `TARGET["green_positive_matched"]`, and not the config's
  `target` (which the gate only cross-checks against the *counter's* emitted target,
  `replay-gate.py:98`). M5 demonstrates the separation concretely: the receipt's declared target can
  read 9 while the clause passes at 8, exit 0. The other three target-bound clauses (`selftest_clean`,
  `mutants_killed`, `red_refused`, `green_clean`) do read `TARGET`, so the divergence is specific to
  the positive-control threshold.
- Vocabulary mismatch (name level, semantics OK): `green_verdict`→`green_clean`,
  `red_verdict`→`red_refused`, `selftest_failures`→`selftest_clean`; only `mutants_killed` is
  spelled identically in both vocabularies.

## 5. Registration boundary

The claims predicate says "registered structure-blind shortcut readers … none meets the target".
The gate's floor is `MIN_SHORTCUTS = 3` (`replay-gate.py:34,56`), not the seven classes the freeze
commit message and the pinned config name. M3 shows a green config registering 3 classes still
yields `REPLAY_GATE_CLEAN`, `shortcuts_below_target=3`, `met_target=true`, exit 0. The frozen set is
therefore held by the config pin (`4483f385…`, verified), not by any clause; no clause reads
`shortcuts_below_target`, which the receipt nonetheless prints (7) as if measured.

## 6. Predicate referent vs measured object

A's subject is "a finite structural-decoding counter"; B's subject is "the committed replay gate".
The thing actually scored each run is `mini-fix/mini-counter.py` (predicate C, "P34-mini-records")
over eight author-built 512-byte `.mrec` fixtures. The claim's own `instrument_notes` says these
fixtures "are never domain evidence" and that the production reader is not run. So A's "frozen only
after" obligation is about a counter whose freeze is not measured here, while the scored surface is
the gate's synthetic green fixture. This is a scope boundary of the predicate, not a clause miss —
no clause names it — but it means A cannot be read as a statement about the R34-C1 production
counter, and B (the sentence the receipts carry) is the only sentence whose subject matches what
ran.

## Findings, by severity

**HIGH-1 — the frozen identity claim is false at word level, and nothing measures it.**
`claims.json:claims[0].predicate_identity` asserts one sentence across config / counter constant /
receipt. The config carries A (31 words), the counter and every receipt carry B (46 words), the
mini counter carries C (28 words) under a different label `P34-mini-records`. Six probes (M1, M2,
M4 plus baseline) pass unchanged with the predicate text rewritten, empty, or relabelled, because
`replay-gate.py:43` requires the key and never reads the value and
`c2-shortcut-gate-counter.py:73` echoes a constant. Evidence: §1, §2, §3.

**HIGH-2 — the frozen `green_positive_matched` target field is not bound to its clause.**
It is absent from the counter `TARGET` and from `receipt.target`; the clause uses literal `8`
(`c2-shortcut-gate-counter.py:121`); M5 shows a receipt target of 9 with the clause still passing at
8 and exit 0. The claim's "target fields equal the counter's TARGET dict" is false, and a receipt
consumer diffing claim target against receipt target finds a missing key. Evidence: §4, M5.

**MED-1 — the "registered" shortcut set is not enforced by any clause.**
Green floor is 3 classes; M3 keeps CLEAN/exit 0 with 3 registered classes while the receipt prints
`shortcuts_below_target=7` for the pinned set. At this revision the pin holds the seven-class set, so
freeze-time integrity is intact; the gate alone would accept a shrunken registration. Evidence: §5.

**LOW-1 — predicate referent mismatch.** A names a "finite structural-decoding counter" and a
freeze-ordering obligation; the measured object is the synthetic mini counter, which the claim's own
instrument notes exclude from domain evidence. Evidence: §6.

**LOW-2 — name-level vocabulary mismatch** between three of five target field names and their
clause names (§4). Semantic binding is correct; only the spelling diverges.

**Residual risk.** The receipt that evidences the only successful production run of this claim
(`.ufo/waves/round-34/r34b/after/*`, `controls/*`) is **untracked** — `git ls-files
.ufo/waves/round-34/r34b` returns 1 path (`claims.json`); `git status --porcelain` shows
`after/`, `before/`, `controls/`, `assimilation/` as `??`. Freeze-integrity cannot cover them, so the
receipt is a working-tree artifact whose `predicate` (B) is unversioned text.

**Verification gaps.** (i) I did not re-run the gate's own selftest in isolation beyond what the C2
counter invokes (the counter's baseline run covers it: `selftest_failures=0, mutants_killed=3`).
(ii) I did not verify that M1/M2/M3 mutant trees were otherwise untouched beyond the named edit
(each built by `cp -a` from the pinned copy). (iii) The `readers/` were executed only as python by
the counter, never as binaries, per the hard rules; fixture bytes were only hashed.

**Deliverable to L1 (draft text, not landed):** either (a) correct
`predicate_identity` to state the evaluated truth — config carries sentence A; counter/receipt carry
sentence B; the six-clause kill rule, not any string equality, is the binding predicate — or (b)
declare the divergence as a known, harmless documentation defect with the clause set as the frozen
predicate. Also state that `green_positive_matched` is a claim-side threshold evaluated by a literal
in the counter, not a `TARGET` member.

VERDICT: PREDICATE_IDENTITY_FALSE — configs carry sentence A verbatim (claims == mini == naive,
sha256 `7c6c17f0…`), but the counter's `PREDICATE`, the receipt, and all five control receipts carry
sentence B (`8340aea5…`, 46 words vs 31), the mini counter carries a third predicate
(`P34-mini-records`), and no instrument reads or compares any of them (probes M1/M2/M4 pass
unchanged); clause-name identity PASSES 6/6, while `claim.target` differs from `receipt.target` by
`green_positive_matched`, which the counter evaluates as a hardcoded literal (M5: target 9, clause
passes at 8) and the registered shortcut set is not clause-bound (M3: 3 classes still CLEAN).
