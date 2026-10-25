# Scribe — SKILL.md registry rows for the round-34 replay gate and C2 counter

Seat `ScribeSkillRegistry` (kaidoku round 34, run-6 re-dispatch, wave 1). Leaf seat: no
subagent dispatch, no REA, no network, no lane writes except this report. Prompt read in full at
`.ufo/waves/round-34/r34b/w1/prompts/ScribeSkillRegistry.md`; operator tooling directive read at
`/home/vgpnk/.omp/agent/RULES.md`. Interpreter `/usr/bin/python3` = Python 3.14.8. No tool was
installed, upgraded or downloaded (nothing to record under the tooling rule).

Lane revision states that matter here (all read, none written):

| when | revision | what |
|---|---|---|
| 07:13:11Z | `c79bbe7b0959132b9873ff3431cf5eb313b58b33` | freeze: `r34b/claims.json` **and** all C2 instruments first added (one commit) |
| 07:13:21Z | — | `before/c2-at-base.txt` written at base `ec3125ad…` (`gate_absent`) |
| 07:13:24Z | — | `after/c2-at-instruments.json` written (production receipt over the frozen bytes) |
| 07:13:52Z | — | five control receipts under `controls/` |
| 07:24Z | `b917ea64ebbeab49b8258d71ffb34e700715ffe6` | L1 lands before/production/control receipts, `instruments.json` (26-pin container), `predicate-reconciliation.json` |
| 07:24Z | `cd75b92e583735729546b0ea3b250f2df6d0652a` | L1 stops R34-C2 on the unregistered content-multiset shortcut; `claim-stop.json` |

`SKILL.md` and `tools/round-34/**` are byte-unchanged from `c79bbe7b` to `cd75b92e`
(`git diff --stat c79bbe7b..HEAD -- SKILL.md tools/round-34` prints nothing, exit 0), so every line
number and digest below holds at the current tip.

## 1. The row format actually in the file, and the assignment's conflict

Read at `SKILL.md` (1207 lines, tip `cd75b92e`):

| section | line | header | columns |
|---|---|---|---|
| `### Round-27/28 measurement registry` | 948 (heading), 950 (header), 951 (separator), rows 952–955 | `\| Name \| Kind / owner \| Entry / verdict map \| Self-invocation \| Pinned values / write scope \|` | **5** |
| `## Round-34 instrument registry` | 1182 (heading), rows 1186–1188 | `\| name \| kind \| entry command \| verdict map \| self-test command/spelling \| pinned-value path \| write scope \| owner \|` | **8** |

The assignment says "8-field registry format used in … `### Round-27/28 measurement registry`" and
names the fields *name, what it does, exact command, freeze commit, what it refuses, limits, evidence
directory, first-working round*. No table in `SKILL.md` has those eight columns: the round-27/28
section is **5** columns, and the only **8**-column table is the round-34 instrument registry, whose
eight columns are different again. Every cell in both tables is one physical line; the round-27/28
rows additionally carry a `Counter sha256 …` clause, a `Green at tip (selftest cases=N failures=0,
exit 0, UTC); freeze receipt …` clause and an explicit write scope.

Resolution taken (cheap, harms nothing): **Block A is the primary insertion block**, using the eight
fields the assignment names, written in the round-27/28 registry's one-line phrasing and pin clauses.
**Block B** is the same two instruments re-expressed in the round-34 8-column header already in the
file, so the L1 can append inside `## Round-34 instrument registry` instead. **Block C** is the
5-column variant for `### Round-27/28 measurement registry`. Land exactly one of the three; the
content is identical.

## 2. Block A — primary insertion block (8 named fields)

Insert after the end of `## Round-34 post-control limits and stopped claim` (tip line 1207), as: one
blank line, the lead-in sentence, one blank line, the table.

> R34-C2 was stopped in wave 1 (`claim-stop.json`); these rows register the frozen instruments and
> their measured limits as historical evidence, not as admission dependencies of any live claim.

```markdown
### Round-34 shortcut-replay registry (R34-C2, stopped)

| name | what it does | exact command | freeze commit | what it refuses | limits | evidence directory | first-working round |
|---|---|---|---|---|---|---|---|
| round34-C2-replay-gate | Generic, config-driven pre-freeze replay gate (QUALITY 67): runs the config's counter argv once per reader, reads only the counter's own receipt fields (matched, target, met_target), requires the registered positive control to meet the config target, and refuses CLEAN when any registered shortcut class meets it. Verdicts REPLAY_GATE_CLEAN 0, REPLAY_GATE_REFUSED 2, REPLAY_GATE_UNEVALUABLE 3. R34-C2 is stopped: the pinned seven classes stay below target, an unregistered content-multiset shortcut reaches 8/8 | `python3 -I -B tools/round-34/replay-gate.py --root <LANE> --config tools/round-34/gate-config-mini.json [--json-out <RECEIPT>]` (green surface); `--config tools/round-34/gate-config-naive.json` (red surface, exit 2 expected); `--selftest` (12 cases, 3 mutant kills). With no `--config`, argparse exits 2 with no verdict line, the same code as REFUSED | `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (2026-10-25T04:13:11-03:00 = 07:13:11Z), the only commit that touches it; sha256 `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` | exit 3: config schema != 1, a missing `predicate`/`counter`/`positive_control`/`shortcuts`, a counter argv without exactly one `{reader}`, a non-integer target < 1, fewer than 3 shortcuts, a duplicate shortcut class, an absent positive or shortcut file, an unreadable receipt, a non-int matched/target or non-bool met_target, a receipt target != config target, or a positive control below target. exit 2: any registered shortcut meets target. It does **not** refuse a shortcut whose class string equals the positive control's class | Verdict covers **registered** classes only; class names compare literally, so a shortcut classed `structural` that meets target is excluded from the over-target scan and the gate prints CLEAN (probe `cfg-class-collision.json`, exit 0, 07:22:19Z). A relative `--root` is not absolutised, so reader paths resolve against the caller's cwd and the run lands UNEVALUABLE `counter_receipt_fields` (07:21:42Z). The counter's own predicate string is never compared with the config's. No row-count assertion: the pinned green config trimmed to its first three shortcuts (all-false, size-keyed, fixed-slice) still returns CLEAN (probe `cfg-floor3.json`, exit 0, 07:28:05Z), and `load_config` checks only `len(shortcuts) >= 3`. 300 s per counter run, env restricted to PATH/HOME/LANG. Green surface is eight 512-byte synthetic record-chain fixtures; the pin set omits content-multiset, seed-replay and repo-file shortcuts, so CLEAN means "no registered class", never "no shortcut" (`nameset.py` matched 8/8 at seeds kaidoku-r34-mini-v1, alt-1, alt-2, 07:24:54Z). Reads no ELF carrier and never executes one | `.ufo/waves/round-34/r34b/` — `after/c2-at-instruments.json` (sha256 `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9`, reproduced byte-identically on a clean clone 07:19:39Z), `after/c2-at-instruments.txt`, `before/c2-at-base.txt`, `controls/` (5 receipts plus `controls/gates/`), `claim-stop.json`, `instruments.json` (26-pin container, sha256 `224cc44124c52c4bf1135a5994c8366590887334317bf5eff22b70ffc5a8a6b6`, CLEAN at `b917ea64` 07:24:45Z) | 34 (`c79bbe7b`; no replay gate exists at `ec3125ad` or `f432c8e3` — before receipt `gate_absent`); stopped in the same round after wave 1 |
| round34-C2-counter | One command that scores the frozen six-clause R34-C2 predicate: gate selftest (failures=0, mutants_killed=3), red config (the naive shape-only counter must return exit 2 REPLAY_GATE_REFUSED with `label-memorization` over target), green config (the mini counter must return exit 0 REPLAY_GATE_CLEAN with seven classes below target and positive matched=8), and a present gate; prints one stable verdict line and writes one JSON receipt. All six clauses hold on the frozen bytes; that is not the whole test (see the gate row) | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> --json-out <RECEIPT>`; exit 0 GATE_COUNTER_OK, 1 GATE_COUNTER_MISS with the failed clause(s) named, 2 GATE_COUNTER_UNEVALUABLE (`gate_absent` or `pinned_input_absent`). `--gate <PATH>` is a control-only override; production uses the pinned default `tools/round-34/replay-gate.py` | `c79bbe7b0959132b9873ff3431cf5eb313b58b33`; sha256 `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72` | exit 1 unless **all** of selftest_clean, mutants_killed=3, red_refused (exit 2, verdict REFUSED, `label-memorization` in classes_over_target), green_clean, green_positive_meets_target=8 and gate_present hold; exit 2 for an absent gate or either absent config; uncaught errors are not a predicate result | `--rev` is recorded only: the counter reads no Git objects and compares no instrument byte with `--rev` or the claims/instruments pins, so it scores the working tree. `red_refused` pins the single class name `label-memorization`, so a red refusal for any other class fails the clause. `green_positive_matched` is hardcoded 8 and is absent from the receipt's `target` map although `claims[0].target` carries it. The receipt has no UTC field, so file mtime is the only time evidence. Byte-identical receipts depend on the default seed `kaidoku-r34-mini-v1` and the frozen mini counter (reproduced byte-identically, 07:19:39Z). Inherits the gate's class-name and relative-root limits. No ELF carrier, R34-C1 reader or R34-C1 carrier is executed or scored | `.ufo/waves/round-34/r34b/` — `after/c2-at-instruments.{json,txt}`, `before/c2-at-base.txt`, `controls/` (do-nothing, always-clean, junk-clean, no-positive-check, vacuous-no-floor), `claim-stop.json`, `instruments.json`, `predicate-reconciliation.json` | 34 (`c79bbe7b`); stopped in the same round after wave 1 |
```

Optional third row, if the L1 wants the fixture surface registered as its own instrument (not
required by the assignment): `round34-C2-surface | probe | python3 -I -B
tools/round-34/mini-fix/mini-counter.py --root <LANE> --control-reader <READER> [--seed <SEED>]
(green) and naive-counter.py (red); 0 matched==target, 1 below target, 3 typed refusal or absent
reader | c79bbe7b… | — | eight 512-byte synthetic fixtures, no carriers; deterministic under the
default seed | .ufo/waves/round-34/r34b/ | 34`.

## 3. Block B — drop-in rows for the existing `## Round-34 instrument registry` (8 columns)

Append as two rows after the `Schema-validating freeze integrity` row (tip line 1188).

```markdown
| P34-shortcut-replay gate | gate, historical (claim stopped) | `python3 -I -B tools/round-34/replay-gate.py --root <LANE> --config tools/round-34/gate-config-mini.json [--json-out <RECEIPT>]`; `--config tools/round-34/gate-config-naive.json` for the red surface; `--selftest` | 0 REPLAY_GATE_CLEAN; 2 REPLAY_GATE_REFUSED (and also argparse usage exit 2 without a verdict line); 3 REPLAY_GATE_UNEVALUABLE; unlocked config schema and a positive control below target are UNEVALUABLE, never CLEAN | same script `--selftest`: 12 cases (6 verdict, 2 schema, positive-absent, 3 mutant kills), exit 0/1; these are gate tests, not coverage of any ELF parser | `.ufo/waves/round-34/r34b/claims.json` `claims[0].pins` and `instruments.json` (26 pins); gate `8fa94b23…`, configs `4483f385…` and `72b12941…` | read-only measure; `--json-out` writes one receipt; selftest writes a unique `kaidoku-r34-gate-*` temp dir | kaidoku |
| P34-shortcut-replay six-clause counter | gate, historical (claim stopped) | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> --json-out <RECEIPT>` | 0 all six clauses hold; 1 GATE_COUNTER_MISS with clauses_failed named; 2 GATE_COUNTER_UNEVALUABLE (gate_absent, pinned_input_absent) | none in the instrument: it runs the gate's selftest and reports its 12 cases and 3 mutants | counter `41d59703…`; pins as above; `--rev` is a label only, no Git read and no pin check | read-only measure; `--json-out` writes one receipt; no temp files beyond the gate's | kaidoku |
```

## 4. Block C — 5-column variant for `### Round-27/28 measurement registry`

```markdown
| round34-C2 | gate / kaidoku (historical; R34-C2 stopped) | `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root <LANE> --rev <REV> --json-out <RECEIPT>`; 0 all six clauses hold (selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 gate_present), 1 GATE_COUNTER_MISS with clauses_failed named, 2 GATE_COUNTER_UNEVALUABLE (gate_absent or pinned_input_absent). Runs the gate `tools/round-34/replay-gate.py` on the red config (naive shape-only counter must be refused, `label-memorization` over target) and the green config (mini counter, seven registered classes below target, structural positive 8). `--rev` is recorded only: no Git read, no instrument-byte check, so it scores the working tree; no ELF carrier or R34-C1 reader runs | entry command without `--json-out` prints one verdict line and writes nothing; the counter has no selftest of its own and reports the gate's 12 cases and 3 mutants. Frozen bytes reproduced byte-identically on a clean clone at `c79bbe7b` (07:19:39Z, receipt sha256 `da78f444…`) | Counter sha256 `41d597036eb60f2e264c3682ce006198d11682e899273aa73a8b84d3e79a5a72` and gate sha256 `8fa94b2332a6574cccf42972a38a9b3f55a52e9979b19a32f58c7019081c7558` (`claims[0].pins`, 26 entries; `instruments.json` container CLEAN at `b917ea64`). Refuses a CLEAN verdict if the positive control is below target or any registered shortcut meets target; an unregistered content-multiset shortcut meets target 8 (`nameset.py`), which is why the claim is stopped; read-only measure, receipt only via `--json-out`, gate selftest writes a private temp dir |
```

## 5. What I ran (every check, exact exit, UTC)

All runs 2026-10-25 UTC. Rows marked *(clone)* ran in
`/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeSkillRegistry/clone` (a `--no-hardlinks` clone checked
out at `c79bbe7b` for E1–E15 and, after `git fetch`, at `cd75b92e` for E16–E18 and E20; the fetched
commits do not touch `tools/round-34/**`); nothing was run against the lane working tree.

| # | command | observed | exit | UTC |
|---|---|---|---|---|
| E1 | `git clone --no-hardlinks kaidoku-shokunin clone && git checkout c79bbe7b` | `rev-parse HEAD` = `c79bbe7b…` | 0 | 07:19:34Z |
| E2 | *(clone)* `python3 -I -B tools/round-34/c2-shortcut-gate-counter.py --root . --rev c79bbe7b… --json-out c2-repro.json` | `GATE_COUNTER_OK finding=shortcut_gate_discriminates selftest_failures=0 mutants_killed=3 red=REPLAY_GATE_REFUSED green=REPLAY_GATE_CLEAN green_positive_matched=8 clauses_failed=-`; receipt sha256 `da78f444…` **byte-identical** to `after/c2-at-instruments.json` | 0 | 07:19:39Z |
| E3 | *(clone)* gate `--config gate-config-mini.json` | `REPLAY_GATE_CLEAN finding=no_shortcut_meets_target shortcuts_below_target=7 shortcuts_over_target=-` | 0 | 07:19:37Z |
| E4 | *(clone)* gate `--config gate-config-naive.json` | `REPLAY_GATE_REFUSED finding=shortcut_meets_target shortcuts_below_target=6 shortcuts_over_target=label-memorization` | 2 | 07:19:37Z |
| E5 | *(clone)* gate `--selftest` | `{"cases": 12, "failures": 0, "mutants": 3, "mutants_killed": 3}` | 0 | 07:19:37Z |
| E6 | *(clone)* gate with no `--config` | usage on stderr, no verdict line | 2 | 07:19:37Z |
| E7 | *(clone)* `tools/round-34/freeze-integrity.py --round 34 --rev c79bbe7b --claims .ufo/waves/round-34/r34b/claims.json` | `ERROR schema code=instruments_missing where=instruments` | 3 | 07:20:29Z |
| E8 | *(clone)* `tools/round-29/freeze-gate.py --root . --rev c79bbe7b` | `audited 25 clean 7 flagged 18`; the string `r34b` appears nowhere in the report | 0 | 07:21:28Z |
| E9 | *(clone)* gate with a 3-shortcut config whose third class is `structural` (absolute root) | `REPLAY_GATE_CLEAN … shortcuts_below_target=2` while that shortcut meets target 8 | **0** | 07:22:19Z |
| E10 | *(clone)* the same config with relative `--root clone` | `REPLAY_GATE_UNEVALUABLE finding=counter_receipt_fields` | 3 | 07:21:42Z |
| E11 | *(clone)* gate with a 2-shortcut config | `REPLAY_GATE_UNEVALUABLE finding=config_shortcut_count` | 3 | 07:22:19Z |
| E12 | *(clone cwd)* `mini-counter.py --root . --control-reader seed_replay.py` (my own unregistered shortcut: re-derives the default-seed permutation from the committed fixtures and answers from `expected.json`) | `matched 8 met True` | 0 | 07:23:11Z |
| E13 | *(clone)* gate with `seed-replay` registered as an 8th class | `REPLAY_GATE_REFUSED … shortcuts_over_target=seed-replay` (the gate works on registered classes) | 2 | 07:23:18Z |
| E14 | pin audit over `claims[0].pins` at `c79bbe7b` | `pins 26 mismatch []` | 0 | 07:19:34Z |
| E15 | `git log --diff-filter=A` for `r34b/claims.json` and each instrument | all first added at `c79bbe7b`, 2026-10-25T04:13:11-03:00 | 0 | 07:19:34Z |
| E16 | *(clone at tip)* `freeze-integrity --round 34 --rev b917ea64 --claims …/instruments.json` | 26× `ok sha=… commits_after_freeze=0`; `freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=b917ea64ebbeab49b8258d71ffb34e700715ffe6` | 0 | 07:24:45Z |
| E17 | *(clone at tip)* `freeze-integrity --round 34 --rev c79bbe7b --claims …/instruments.json` | `ERROR no commit adds .ufo/waves/round-34/r34b/instruments.json at c79bbe7b…` | 2 | 07:24:45Z |
| E18 | *(clone at tip)* `mini-counter.py` with `CtlMultiset-files/nameset.py`, seeds `kaidoku-r34-mini-v1`, `alt-1`, `alt-2` | `matched 8 met True` at all three seeds | 0 | 07:24:54Z |
| E19 | `git diff --stat c79bbe7b..HEAD -- SKILL.md tools/round-34` | no output (both unchanged to `cd75b92e`) | 0 | 07:24:19Z |
| E20 | *(clone)* gate with the pinned green config trimmed to its first three shortcuts | `REPLAY_GATE_CLEAN … shortcuts_below_target=3` — the class drop is invisible | 0 | 07:28:05Z |

Receipts I produced carry no UTC field; times above are wall-clock readings around each command.

## 6. Findings

- **F1 — the claim is stopped, and the registry must say so.** `claim-stop.json` (sha256
  `e6303d06…`) records `verdict: falsified measure; honest stop after wave-1, before any capability
  or score credit`, while `frozen_counter_verdict.exit = 0` still holds on the frozen bytes. A row
  that registered the instruments as a live admission gate would overstate them. Independent
  reproduction E18: `nameset.py` (`2e8feaea…`) reaches 8/8 under the frozen mini counter at three
  seeds, reading no header, no record array and no `name_off`.
- **F2 — the pins had no enforced container at the freeze.** `r34b/claims.json` (`de3afbfb…`) keeps
  its 26 pins under `claims[0].pins`; `tools/round-34/freeze-integrity.py` requires a top-level
  `instruments` map and returned exit 3 `instruments_missing` (E7). Conflict, verbatim:
  `corpus/QUALITY.md:43` — "A round's counting instruments are committed before its claims file and
  pinned there by sha256 (`instruments`); the freeze commit is the one that first adds
  `claims.json`." Here one commit (`c79bbe7b`) first adds claims **and** instruments, and the
  container only arrived at `b917ea64` (E16, E17) — a post-freeze addition whose CLEAN run is at
  `b917ea64`, not at `c79bbe7b`. The container's digests match `claims[0].pins` byte for byte, so no
  frozen instrument changed; the ordering claim in QUALITY 33 is nonetheless not observable.
- **F3 — neither freeze gate discovers this claims file.** `tools/round-29/freeze-gate.py` matches
  `^\.ufo/waves/(round-[0-9]+)/(claims…\.json)$` (source line 57); `r34b/claims.json` has an extra
  directory, and the gate's 25-row report never mentions `r34b` (E8). So the frozen claim's own file
  is neither audited for `INSTRUMENT_*` findings by the discovery gate nor schema-checked by the
  round-34 gate (E7). Registry rows are, for this claim, the only public pin statement.
- **F4 — `predicate_identity` is false as written.** Conflict, verbatim: `claims[0].predicate_identity`
  — "The same sentence is the gate config's `predicate` field, the C2 counter's PREDICATE constant
  and the receipt label". Measured: claims/config sentence A
  `P34-shortcut-replay: a finite structural-decoding counter is frozen only after registered
  structure-blind shortcut readers are scored under the counter's own predicate and none meets the
  target, while a registered structural reader does.` (31 words, sha256 `7c6c17f0…`) versus the
  counter's `PREDICATE` constant and receipt field B `P34-shortcut-replay: the committed replay gate
  refuses the shape-only counter whose label-keyed memorization meets its target, clears the
  identity-defeating counter on the same eight fixtures where every registered shortcut class stays
  below target, and its selftest kills every mutant of its own refusal, positive-control and
  shortcut-floor branches.` (46 words, sha256 `8340aea5…`). No instrument reads either value. The L1
  independently reached the same finding and landed `predicate-reconciliation.json` (`d6d4f7e5…`).
- **F5 — a class-name collision is exempt from the refusal scan.** `evaluate()` computes
  `over = [row for row in findings if row["met_target"] and row["class"] != positive_spec["class"]]`;
  `load_config` rejects duplicate classes among **shortcuts** only. A shortcut classed `structural`
  that meets target is therefore excluded: E9 prints `REPLAY_GATE_CLEAN`, exit 0. The production
  configs are unaffected (no such class), so the C2 receipt stands; the gate is generic and a future
  user inherits the hole.
- **F6 — a relative `--root` corrupts the run instead of failing loudly.** `resolve()` does not
  absolutise the root, so `--root clone` yields reader paths like `clone/tools/...` passed to a
  counter whose cwd is `clone`; the receipt loses its fields and the gate reports
  `UNEVALUABLE counter_receipt_fields` (E10) — an unevaluable, not a wrong verdict, but it is a
  spurious verdict for a correct config.
- **F7 — CLEAN is class-set relative, and the frozen set is incomplete.** Two independent
  unregistered shortcuts meet the green target: my seed-replay reader (E12, re-derives the committed
  permutation under the fixed default seed `kaidoku-r34-mini-v1` and answers from `expected.json`)
  and the wave's `nameset.py` content-multiset reader (E18). E13 shows the gate mechanism refuses
  either one once registered; the pinned configs register neither, and `label_keyed.py` is pinned
  (`f727c152…`) but registered nowhere.
- **F8 — the counter's `--rev` is a label.** Source read: `receipt["measured_revision"] = args.rev`
  and nothing else consumes it; no pin is re-hashed, so a modified working tree is scored as the
  revision. The after receipt proves determinism of the frozen bytes (E2), not that the measured
  bytes were the revision's.
- **F9 — receipt time and target-map drift.** `after/c2-at-instruments.json` has no UTC field; the
  only time evidence is mtime (`07:13:24Z`, E-evidence in §5). `claims[0].target` carries
  `green_positive_matched: 8`; the counter's `TARGET` dict does not, and its clause hardcodes `8`.
- **F10 — receipt provenance is now committed.** At first audit the before/after/controls files were
  untracked (`git status --porcelain` showed `?? .ufo/waves/round-34/r34b/{after,before,controls,…}`);
  `b917ea64` landed them. The registry's evidence pointers are now committed paths, and the receipt
  bytes are unchanged by that commit (E2 hash equals the committed file's hash).
- **F11 — the registered class set can shrink without any signal.** Trimming the pinned green config
  to its first three shortcuts still returns `REPLAY_GATE_CLEAN` with `shortcuts_below_target=3`
  (E20, exit 0); `load_config` refuses only fewer than `MIN_SHORTCUTS = 3` and duplicate classes.
  Nothing compares the registered set with the pinned set, so a config edit that deletes classes 4–7
  keeps the green verdict. This corroborates the L1's `claim-stop.json` F3 route ("assert class
  count == pinned count before CLEAN") independently of its own runs.

No conflict was found in the control receipts: `do-nothing` exit 2 `gate_absent`, and the four gate
mutants each fail a distinct clause (`red_refused`, `selftest_clean`, `mutants_killed`,
`selftest_clean`), matching `claim-stop.json` and `w1/RevControls.md`.

## 7. Out of scope / not done

- No SCORECARD/LOG/SKILL/PROVINCE/corpus write; Sections 2–4 are drafts only.
- No ELF carrier, fixture or reader was executed as a program of interest; readers ran only as
  arguments of the counters and the gate. No R34-C1 reader or carrier was touched.
- I did not run the production counter against the lane working tree (clone only), and I did not
  re-derive the eight fixtures from `build.py` (`w1/ExecGreenIndependence.md` owns that).
- I did not evaluate `CtlMultiset-files/pathkey.py` or the `assimilation/` guard-proof material; the
  stop record and E18 cover the decisive class.
- No tool install; nothing to record under the tooling directive.

## 8. Artifacts

| path | sha256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r34b/w1/ScribeSkillRegistry/c2-repro.json` (E2, byte-identical to the lane receipt) | `da78f44419ecf83935e1fe6b1cd72f611c5a0e7e03029e97580d515a0796f3e9` |
| `…/coll.json` (E9 collision receipt, exit 0) | `77410ac6cd428249da0b4f54996c97cf6feb087987dff5589f49d2c3d8a9de19` |
| `…/cfg-class-collision.json` | `72cca243d5b0bcad48e6e90d0a9cc8790279a579d2f616f447478db74382bc21` |
| `…/cfg-two-shortcuts.json` | `29bda607f66dbb8c1ba389c09fb463820c26d040eb2937857b391b10bf3bc49f` |
| `…/cfg-floor3.json` (E20, three-class floor still CLEAN) | `28a4dde509ee8a868168f1369429478e0660071af756d7b64aecb088aac64bd9` |
| `…/cfg-with-seed.json` | `0b642889039f53ebe3ed8633718b5f01e27e6645119e2b34e0d115c2ffea745a` |
| `…/seed_replay.py` (my unregistered shortcut, E12) | `4fc10956db326ccbd89967dec63d676e46cd6a730a6ea9f9f2c52586ffca6b55` |
| `…/sr.json` (first seed-replay attempt, wrong offsets, matched 0) | `aed8df0d21009aae493417fecd4b74cd2ed27f03dbc6009d8866eda13322539d` |
| `…/sr2.json` (E12 run, matched 8) | `c1e25a4f718e6ad0d2c4a84f97ee3b9b1330fe760fbbd213a10c09ed9810a078` |
| `…/freeze-gate-r29.json` (E8 report) | `0bf09e7abc50c0469fc9604e9491a16eec8fd8c7ee30086e7d87a07f8abe1614` |
| `…/clone/` (scratch clone, `c79bbe7b` then `cd75b92e`) | — |

VERDICT: DRAFT-COMPLETE — two registry rows (gate, counter) drafted three ways for the three table
shapes in `SKILL.md`, with the R34-C2 stop, the 26-pin container, the predicate split and the
class-set hole all stated in the rows; the frozen counter reproduced byte-identically (exit 0,
07:19:39Z) and the decisive unregistered shortcut reproduced at 8/8 (exit 0, 07:24:54Z); eleven
findings (F1–F11) carry command, exit and UTC; no lane file was written except this report.
