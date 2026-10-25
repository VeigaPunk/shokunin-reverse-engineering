# AWhatRemains — R34-C2 post-stop: falsification of the stop's reach, and the claims its bytes still support

Seat: `L1Kaidoku34-2.AWhatRemains` (critic, wave 2). Round 34 / run-6 re-dispatch, attempt 1.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; all execution from a scratch clone).
Scratch: `/fast/scratch/hyaku/kaidoku-r34b/w2/AWhatRemains/`.
Window: 2026-10-25T07:29:29Z … 2026-10-25T07:44:04Z (UTC throughout).
Frozen subject: claim `R34-C2`, freeze `c79bbe7b0959132b9873ff3431cf5eb313b58b33`, stop record `cd75b92e`.
Tooling: none installed; `python3 -I -B` (system interpreter) only. No ELF carrier, fixture, reader or production
reader was executed as a program of interest; readers ran only as children of a counter. R34-C1's production
reader was not executed.

**Verdict in one line:** the stop is correct and its decisive counterexample reproduces, but it is narrower than its
own public record: the only instrument-enforced facts are the 26 file digests and "a *gate file* at this path prints
REFUSED/CLEAN against *this config*"; every broader reading ("at revision X", "the gate discriminates", "the green
surface forces traversal", "the selftest kills its mutants", "five classes reach 8/8") needs an explicit narrowing,
and four of them are already false as stated.

---

## 1. What I reproduced (exact evidence)

Clone: `git archive c79bbe7b | tar -x -C $S/clone` (07:29:29Z). Frozen-instrument hashes in the clone equal the pins:
`replay-gate.py 8fa94b23…`, `c2-shortcut-gate-counter.py 41d59703…`.

| # | argv (abridged to the load-bearing parts) | exit | UTC | result |
|---|---|---|---|---|
| R1 | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b… --json-out receipt-at-frozen.json` (in the c79bbe7b clone) | 0 | 07:29:37Z | `GATE_COUNTER_OK … clauses_failed=-`; receipt **JSON-equal** to committed `after/c2-at-instruments.json` |
| R2 | `python3 -I -B tools/round-34/mini-fix/mini-counter.py --root . --control-reader probes/nameset.py --seed {alt-1, alt-2, kaidoku-r34-mini-v1}` | 0,0,0 | 07:29:35Z | 8/8 each; `nameset.py` sha256 `2e8feaea…88b97` (equals stop's bound source) |
| R3 | `freeze-integrity.py --root . --round 34 --claims .ufo/…/r34b/instruments.json --rev cd75b92e…` | 0 | 07:30:20Z | `CLEAN pins=26 freeze=b917ea64ebbe rev=cd75b92e…`; every pinned path `commits_after_freeze=0` |
| R4 | same tool, `--claims .ufo/…/r34b/claims.json` | 3 | 07:30:20Z | `ERROR schema code=instruments_missing` (F1 reproduces) |
| R5 | naive + permuted counters over all eight registered classes | 0/1 as scored | 07:31:49Z | naive: structural 8, label-memorization 8, size-keyed 1, rest 0; permuted: structural 8, size-keyed 1, rest 0 |
| R6 | gate over scratch configs: `green3` (3 classes), `green2` (2), `red6` (7 minus label-memorization) | 0, 3, 0 | 07:32:21Z | `CLEAN 3`; `UNEVALUABLE config_shortcut_count`; **`CLEAN` on the red config once the over-target class is dropped** |
| R7 | `m3-gate.py` (`for item in config["shortcuts"][:-1]:`) `--selftest`; then `--config gate-config-naive.json` | 0; 0 | 07:32:27Z | selftest `cases 12, failures 0, mutants_killed 3`; red case **`REPLAY_GATE_CLEAN`** |
| R8 | pinned counter with `--gate probes/fake-selftest-gate.py` (fabricates only the selftest summary) | 0 | 07:32:27Z | `GATE_COUNTER_OK … mutants_killed=3` |
| R9 | pinned counter over `clone-m3` (gate `9027b2e5…` ≠ pin, red config `076cdfb1…` ≠ pin) | 0 | 07:32:46Z | `GATE_COUNTER_OK`; pins never read |
| R10 | pinned counter `--root emptyroot`; and `--rev deadbeef…` on the clean clone | 2; 0 | 07:32:46Z | `finding=gate_absent`; `GATE_COUNTER_OK` with `measured_revision=deadbeef…` |
| R11 | nameset on six further seeds `s0..s5` | 0 ×6 | 07:33:09Z | 8/8 each (9 seeds total, seed-invariant) |
| R12 | `tabledigest.py` (sha256 of emitted bytes → stored answer) on default / `alt-1` / `s3` | 0 / 1 / 1 | 07:33:58Z | 8/8 / 0/8 / 0/8 — memorization tracks the **seed**, not the format |
| R13 | gate with `positive_control.class="structural"` pointing at `nameset.py` | 0 | 07:33:09Z | `REPLAY_GATE_CLEAN` — positive class is a label |
| R14 | five hardened variants `s2b_string_name_keyed`, `s2c_string_pool_noheader`, `s2b_record_sig`, `s2b_digest_replay`, `s2b_label_hash_replay` on the frozen counter | 0 ×5 | 07:42:02Z | 8/8 each |
| R15 | gate with each of the six registered as an extra shortcut | 2 ×6 | 07:43:11Z | `REFUSED`, class named |
| R16 | `no-reader-gate.py` (spawns nothing) through the pinned counter; `met-only-counter.py` through the gate | 0; 0 | 07:43:11Z | `GATE_COUNTER_OK`; `REPLAY_GATE_CLEAN` with `matched=0` |
| R17 | twelve carriers hashed against `.ufo/waves/round-34/expected.json`; `git diff 54a87a5..HEAD` on C1 reader/counter/carriers/manifest | 0 | 07:43:48Z | 12/12 sha+size match; empty diff |
| R18 | `mini-counter-rename.py` (same-length renaming + per-run expected) over structural and the six memorizers | 0; 1 ×6 | 07:40:36Z / 07:42:16Z | structural 8/8; nameset, `s2b_string_name_keyed`, `s2c_string_pool_noheader`, `s2b_record_sig`, `s2b_digest_replay`, `s2b_label_hash_replay` all 0/8 |
| R19 | `mini-counter-rename.py` with `tabledigest-rename.py` (sha256 of renamed bytes at the default seed → replay) | 0 | 07:42:29Z | 8/8 — renaming alone does not defeat a fixed-seed digest table |

Fixture geometry checked directly: all eight fixtures are 512 bytes, with **eight distinct** SONAME multisets of
cardinality 1–6 (07:33:45Z) — so a sorted-name-set key is fully discriminating on this set.

---

## 2. Attacks on the stop and on the five disclosed defects

**A1 — the stop's five defects are not the round's public five.** `claim-stop.json` lists F1 pins, F2 predicate,
F3 class-drop, **F4 M3 skip-last-row**, F5 untracked receipts. `SCORECARD.md:3357` lists six: (1) pins, (2) predicate,
(3) class-drop, **(4) relabelled `structural`**, **(5) no-reader gate + `met_target` not cross-checked**, **(6) `--rev`
echo**. F4 is absent from SCORECARD; (4)(5)(6) are absent from the stop. Two authorities, two lists — a future round
citing "the five defects" is citing whichever file it happened to open. `claim-stop.json` must be declared binding for
F1–F5 (it is the landed stop record) and SCORECARD's six marked as the reconciled superset; otherwise renumber.

**A2 — F1's repair is advisory.** The container is byte-identical to `claims[0].pins` (26/26) and R3 proves it works,
but no instrument reads it: `frozen_claims_sha256` appears **only** in `instruments.json` (`grep` 07:40:54Z), and the
C2 counter never hashes a pinned file (A3). So "pins are enforced" is true **only when a human adds
`--claims instruments.json --rev …`**.

**A3 — "at the measured revision" is an echo, not a binding.** `--rev` is copied into the receipt and nothing else
(R10: `deadbeef…` → exit 0). Worse, the counter reads whatever root it is pointed at: `clone-m3` (mutated gate,
mutated red config) returns `GATE_COUNTER_OK` (R9). The six clauses are therefore a statement about *the bytes present*,
not about the revision named in the receipt.

**A4 — the selftest clause is self-attested.** The counter takes `failures`/`mutants_killed` from the gate's own stdout.
A gate that fabricates only `--selftest` output passes with `selftest_failures=0, mutants_killed=3` (R8). F4 is the
sharper version: M3 genuinely runs the selftest and genuinely passes it (R7).

**A5 — F4's true scope.** M3 survives the selftest in every configuration. It turns the **frozen** red case CLEAN
because `label-memorization` is the last row (R7). With the row moved to the middle (`red-reordered.json`), M3 is
REFUSED again (07:32:27Z), and the *counter* would then return OK over the mutated root (R9). So M3 is invisible to the
gate's selftest and caught by the C2 counter only by row-order luck.

**A6 — the positive control is a label.** The gate excludes any row whose `class` equals the configured positive
class. Registering `nameset.py` as `class="structural"` yields CLEAN (R13). The frozen config does point at the real
`structural.py`, which does walk `records_off`/`name_off` (verified by reading it), so the stop's factual sentence is
true — but no instrument checks structure, and "relabel a shortcut `structural`" (SCORECARD defect 4) is the same hole
on the red side.

**A7 — "five unregistered classes" is true at the target but not reproducible from committed bytes.** I scored the
five variant readers at 8/8 (R14), but their sources live only in
`/fast/scratch/hyaku/kaidoku-r34b/w1/MutShortcutClasses/variants/`, not in lane VCS. The only committed class sources
are `nameset.py` (`2e8f…`), `pathkey.py`, and `mini-counter-fresh.py` under `w1/CtlMultiset-files/`. A future round
may cite the *scores*; it may not claim a committed, re-runnable artifact for four of the five.

**A8 — the stop's own counterexample is stronger than the stop says, in one direction and weaker in another.**
Stronger: nameset is seed-invariant (9/9) and its key is proven invariant by construction (pool reordering preserves
the token multiset). Weaker: the transform is deterministic at the default seed and the output filename is
`opaque-<sha256(transformed)[:20]>.data`, so *any* memorization keyed on the emitted bytes or the filename reaches 8/8
(R12, R14 `s2b_label_hash_replay`) — the stop's "identity-defeating" phrase is simply false for this counter. Both
directions are already touched in w1 (`ExecPermuteAudit` sha-identity 1/474 per single-name fixture; `MutShortcutClasses`
§3.3–3.4); the stop does not carry either.

---

## 3. Claims a future round could defensibly make, ranked by falsifiability

**Ranking criterion.** Rank 1 = refutable by one command against committed bytes, with a named fatal counterexample
and no new data needed. Rank rises as the decisive test needs reconstruction (new readers, new seeds) or as the claim's
scope depends on files outside the lane. Every claim below is phrased so that *one* observed counterexample refutes it;
the "narrowing" column is what must be in the sentence for it not to be already false.

### C1 (rank 1) — Frozen-instrument integrity
**Claim.** "At `cd75b92e`, the 26 files pinned in `.ufo/waves/round-34/r34b/instruments.json` are byte-identical to
their sha256 pins, unmodified since freeze commit `b917ea64`, and the `tools/round-34` tree is byte-identical to
`c79bbe7b`."
**Evidence.** R3 (`CLEAN pins=26`, exit 0); `git ls-tree -r c79bbe7b -- tools/round-34 | sha256sum` =
`git ls-tree -r HEAD …` = `c3d3a29b…`; direct `sha256sum` of counter/gate/configs/micro-counter equals the pins.
**Narrowing.** Exactly 26 instrument files; excludes `claims.json`, `SCORECARD.md`, the predicate text, the stop record,
and all of `.ufo/…/w1`. "Frozen" means tree identity, not that the frozen sentence is true.
**Decisive falsifier.** Any one changed byte in a pinned path at the measured rev → `freeze-integrity: FAIL changed=1`.
**Smallest safe correction.** Make `c2-shortcut-gate-counter.py` call the same pin check (or embed `instruments.json`
digests) and exit 2 on mismatch, so its exit 0 is itself the integrity statement.

### C2 (rank 2) — Absence control
**Claim.** "With no `tools/round-34/replay-gate.py` under the root, the pinned counter is UNEVALUABLE, exit 2,
`finding=gate_absent`."
**Evidence.** R10 (07:32:46Z); committed `before/c2-at-base.txt`; `git cat-file -e ec3125ad:tools/round-34/replay-gate.py`
exits 128 (07:40:54Z).
**Narrowing.** `gate_present` is `Path.is_file()` only; it proves a path exists, not which bytes. A junk gate at that
path passes the presence clause and is killed by the red clause instead (`controls/gate-junk-clean.py.json`: exit 1,
`red_refused=false`).
**Decisive falsifier.** Point `--root` at any tree containing the path → clause true regardless of content.
**Smallest safe correction.** Replace `is_file()` with the pinned digest comparison from C1.

### C3 (rank 3) — Schema floor vs class-set identity
**Claim.** "The gate refuses a config with fewer than 3 shortcuts (`config_shortcut_count`) or duplicate classes; it
does **not** assert that the registered set equals the frozen seven."
**Evidence.** R6: `green2` → exit 3 `config_shortcut_count`; `green3` → `REPLAY_GATE_CLEAN` (07:32:21Z); `red6` →
`REPLAY_GATE_CLEAN`; source `MIN_SHORTCUTS = 3`.
**Narrowing.** Says nothing about 4–7 class configs; a config that drops `label-memorization` loses the only red
refusal in the frozen set.
**Decisive falsifier.** `--config red6.json` → CLEAN, exit 0 (already observed).
**Smallest safe correction.** Before any verdict, assert `sorted(classes) == pinned_classes` (or count == 7 **and**
set equality against a frozen list), and fail `UNEVALUABLE` otherwise.

### C4 (rank 4) — Registered refusal and the registration flip
**Claim.** "At the pinned bytes the gate refuses the frozen red config: exit 2, `REPLAY_GATE_REFUSED`,
`shortcuts_over_target=label-memorization`; and registering any target-met class in the green config flips
`CLEAN` → `REFUSED` naming it."
**Evidence.** R1 red block; R15: nameset + the five variants each → `REFUSED` exit 2 (07:43:11Z).
**Narrowing.** The refusal is a function of the *registered list only*: drop the class (R6), relabel it `structural`
(A6), or skip the last row (R7) and the same fixtures print CLEAN. The red reader is the purpose-built
`naive-counter.py` (no transform), never a production reader.
**Decisive falsifier.** `--config red6.json` → CLEAN; `m3-gate.py --config gate-config-naive.json` → CLEAN.
**Smallest safe correction.** Class-set assertion (C3) + reserved positive label (a shortcut may not use
`structural`) + red-last case (C5).

### C5 (rank 5) — Selftest scope
**Claim.** "The gate's selftest runs 12 cases with 0 failures and kills exactly three enumerated mutants
(`always-clean`, `no-positive-check`, `vacuous-no-shortcut-floor`); a skip-last-row mutant survives it and turns the
frozen red case CLEAN."
**Evidence.** R7 (`{"cases":12,"failures":0,"mutants_killed":3}`, exit 0); `MUTANTS` list; m3 selftest + red CLEAN;
R8 (fabricated summary accepted).
**Narrowing.** The predicate-B phrase "kills every mutant of its own refusal … branches" is **false**: the refusal
branch's row-completeness is untested. The clause is self-attested, so it certifies the gate's report, not the gate.
**Decisive falsifier.** `m3-gate.py --selftest` → exit 0, 3/3 killed, then red → CLEAN.
**Smallest safe correction.** Add a red-last selftest case and assert the row count equals the config's shortcut count;
have the *counter* run a mutation of the gate it reads, not trust the gate's summary.

### C6 (rank 6) — Clause reproduction vs revision/pin binding
**Claim.** "The six clauses reproduce JSON-equal on a root whose instrument hashes equal the pins; the counter itself
binds neither `--rev` nor the pins."
**Evidence.** R1 (JSON-equal receipt, exit 0, 07:29:37Z); R9 (mutated root → `GATE_COUNTER_OK`, gate `9027b2e5…`,
red config `076cdfb1…`); R10 (`--rev deadbeef…` → exit 0).
**Narrowing.** "At revision c79bbe7b" must be evidenced by C1 plus my archive run, never by the receipt's
`measured_revision` or by a plain `--root <lane>` run at another commit. The receipt also carries no argv.
**Decisive falsifier.** R9 or R10 (already run).
**Smallest safe correction.** Record argv and the sha256 of gate, configs and counter in the receipt; fail closed when
they differ from the pins.

### C7 (rank 7) — Reachability of the green target without traversal
**Claim.** "The green target is reachable without reading the header, the record array or `name_off`:
(i) content-multiset memorization, 8/8 at nine seeds; (ii) transformed-digest replay, 8/8 at the counter's default
seed and 0/8 at any other seed; (iii) filename-hash replay, 8/8 because the output name is
`opaque-<sha256(transformed)[:20]>.data`."
**Evidence.** R2, R11 (nameset); R12 (`tabledigest` 8/8 default, 0/8 `alt-1`/`s3`); R14 (`s2b_digest_replay`,
`s2b_label_hash_replay`); fixture multiset check (8 distinct keys); `permute()` source rewrites `name_off` only.
**Narrowing.** These are memorizations of the eight synthetic payloads under a layout-only transform: all six score
0/8 under the perturbed-payload control (`w1/MutShortcutClasses.md` §3.4) and the digest/filename classes are
seed-sensitive. This is **not** evidence about the R34-C1 carriers, and four of the five variant sources are
uncommitted (A7).
**Decisive falsifier.** Payload/flag perturbation per fixture → all six 0/8 while structural stays 8/8 (w1 receipt);
or a fresh non-default seed → digest class 0/8 (R12).
**Smallest safe correction.** (a) same-length **renaming** of the pool, not reordering (R16: with per-run expected,
structural 8/8 and all six 0/8 — probe `probes/mini-counter-rename.py`, sha `2dc88856…`); (b) a fresh unpredictable
seed per run, because at the default seed even the renaming transform is memorizable by digest
(`tabledigest-rename.py` 8/8, 07:42:29Z); (c) perturb at least one payload field so memorization and decoding diverge.

### C8 (rank 8) — Registration falsifies, and the correction's limits
**Claim.** "Registering a target-met class turns the same frozen gate from CLEAN to REFUSED with byte-identical
fixtures; the refusal mechanism is sound while the registered set is not exhaustive."
**Evidence.** R15; R1 green/red rows.
**Narrowing.** "Sound" means the `over` list is computed correctly — not that an *unregistered* class is refused, not
that the class list is pinned, and not that a gate mutant cannot skip it.
**Decisive falsifier.** Omit the class from the config → CLEAN (R6); the flip needs the class to be registered.
**Smallest safe correction.** Freeze the class list itself into the pin container (C1) and assert set equality (C3).

### C9 (rank 9) — What the C2 counter cannot certify
**Claim.** "The counter's six clauses certify agreement between a gate-shaped process's printed fields and the
counter's expected labels; a gate that spawns no counter or reader prints the three expected verdicts and receives
`GATE_COUNTER_OK` (exit 0). `met_target` is never cross-checked against `matched`: a receipt with
`met_target=true, matched=0` clears the gate."
**Evidence.** R16 (`no-reader-gate.py`, sha `4ce0cf51…` → `GATE_COUNTER_OK`; `met-only-counter.py` → CLEAN with
`matched=0`, 07:43:11Z). This is SCORECARD defect (5); I confirm it with my own receipts.
**Narrowing.** Bounds C4/C5 to statements about the *frozen gate file's* behaviour, not about anything the counter
verified independently. `green_positive_meets_target` does check `matched == 8` in the counter, so the counter is
stricter than the gate on the positive row — but both trust the printed fields.
**Decisive falsifier.** R16 (already run).
**Smallest safe correction.** In `run_counter`, require `matched == target iff met_target` and reject otherwise;
hash-bind the gate (C6) and run at least one gate-side mutation from the counter.

### C10 (rank 10) — C1 containment and the bookkeeping stop
**Claim.** "R34-C1's reader, counter, manifest and twelve carriers are unchanged since `54a87a5` and were not executed
this round; no capability row and no owned-axis change entered SCORECARD (coverage/depth/calibration stay 10)."
**Evidence.** R17: 12/12 carriers match sha+size; empty `git diff 54a87a5..HEAD` for reader/counter/manifest/carriers;
`SCORECARD.md` diff since base is 48 insertions confined to the run-6 section, no R34 capability row; `w1/
RevR34C1Untouched.md`.
**Narrowing.** "Not executed" is an absence-of-evidence audit (grep of receipts), not a positive proof; my
contribution is hashing bytes only. The score statement is bookkeeping, not measurement.
**Decisive falsifier.** One carrier digest mismatch, or one R34 row in the capabilities table.
**Smallest safe correction.** None needed for this round; for the next, bind a no-exec claim to a syscall/audit record
rather than a grep.

**Why this order.** C1–C3 and C6–C7 have one-command fatal tests against committed bytes; C4–C5 need one derived
config or one mutated source; C7's seed leg needs new probes (run here, 6 seeds + 3 digest seeds); C8's evidence
partly lives outside VCS; C9 is formal (a synthetic gate/counter); C10 is documentary. Nothing above rank 6 can be
stated without C1's hash check in the same sentence, because the counter itself does not bind what it measured.

---

## 4. Claims that must be withdrawn (already false as stated)

- **W1** "The gate makes the counter's predicate executable / the green surface forces record traversal." False:
  six structure-blind classes reach 8/8 (C7); the only transform is a pool reordering with a fixed default seed.
- **W2** "`identity-defeating`" (predicate B). False: permuting the pool preserves the token multiset, and the output
  filename is a sha256 of the emitted bytes. 9/9 seeds for nameset; 8/8 for filename/digest replay at the default seed.
- **W3** "`--rev` / the receipt records the measured revision." False: R10; the receipt has no argv.
- **W4** "The selftest kills every mutant of its own refusal, positive-control and shortcut-floor branches." False:
  three mutants only; M3 (skip last row) survives and turns the red case CLEAN (R7).
- **W5** "The counter certifies the gate ran readers." False: R16.
- **W6** "The predicate is byte-identical in claims, config, counter and receipt." False: A `7c6c17f0…` (claims +
  configs) vs B `8340aea5…` (counter + receipts); no instrument reads the value (grep 07:40:54Z).
- **W7** "Five unregistered classes reach 8/8" **as a committed-artifact claim**. Scores reproduce (R14) but four of
  the five readers are not in lane VCS; state "five scores were observed, one of them from a committed source".

---

## 5. Residual defects to route (not repaired; frozen bytes)

| id | defect | evidence | smallest safe correction |
|---|---|---|---|
| D1 | stop's F1–F5 ≠ SCORECARD's (1)–(6); F4 missing from SCORECARD, (4)(5)(6) missing from stop | `claim-stop.json`; `SCORECARD.md:3357` | declare the stop JSON binding; mark SCORECARD's six as superset and renumber |
| D2 | counter binds neither `--rev` nor pins; OK on a mutated root | R9, R10 | digest-check at entry; argv+hashes into receipt |
| D3 | selftest/mutant clause is self-attested by the gate's stdout | R8 | counter-side mutation; never accept the gate's own summary |
| D4 | positive control trusted by class label | R13 | reserved positive class; resolve positive path from the pin, not from config text |
| D5 | deterministic transform + digest-bearing output filename | R12, R14; `mini-counter.py` `permute`, `score` naming | fresh per-run nonce seed; random filename; renaming + payload perturbation |
| D6 | 4 of 5 "five classes" readers uncommitted | R14 paths; lane `git ls-files` | commit variant sources with hashes before citing them |

---

## 6. Tooling record

No installs, no upgrades, no pacman transaction. `python3` (system), `git archive`/`cat-file`/`ls-tree` (read-only),
`sha256sum`. All control probes are in
`/fast/scratch/hyaku/kaidoku-r34b/w2/AWhatRemains/probes/` with these digests: `nameset.py 2e8feaea…`,
`tabledigest.py 4bdfdde7…`, `tabledigest-rename.py d4ee6c67…`, `mini-counter-rename.py 2dc88856…`,
`m3-gate.py 9027b2e5…`, `fake-selftest-gate.py af0da6e3…`, `no-reader-gate.py 4ce0cf51…`,
`met-only-counter.py 55325926…`. No lane file other than this report was written.

**FINAL VERDICT: the stop stands — R34-C2 is correctly denied capability and score — but only six of its statements
survive unqualified: 26 pinned digests, the gate-absent control, the schema floor, the registered-only red refusal and
registration flip, the three enumerated mutants, and the JSON-equal six-clause receipt on hash-verified bytes. Every
stronger sentence ("at the revision", "the gate discriminates", "forces traversal", "kills its mutants", "five
committed classes") is either false as stated or needs the counter to bind hashes it currently never reads; the
minimal repair is a pin check at counter entry plus class-set equality, a reserved positive label, a red-last selftest
case, and a nonce-seeded renaming/perturbing transform.**
