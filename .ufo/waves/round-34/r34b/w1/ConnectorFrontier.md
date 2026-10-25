# ConnectorFrontier — province home of the R34-C2 shortcut-replay gate

Seat: leaf, drafting only. No lane doc was written; every draft below is text for the L1.
Base for reading: HEAD `b917ea64ebbeab49b8258d71ffb34e700715ffe6` (committer 2026-10-25T04:22:31-03:00 = 07:22:31Z).
Frozen claim: `claims.json` at `c79bbe7b0959132b9873ff3431cf5eb313b58b33` (04:13:11-03:00 = 07:13:11Z).
Read-only throughout; no ELF carrier, fixture or reader was executed as a program of interest; no network; no tool installed.

## 1. Axes named (this decision's axes, not the round's)

| axis | what this report moves | expected sign |
|---|---|---|
| depth (claim axis) | gives the round-34-instrument registry its missing row and states the gate's measured limits, so a CLEAN cannot be read as more than it is | up |
| calibration | no score, no verdict, no re-scoring of R34-C1 or R34-C2 | unchanged |
| coverage | no artifact surface is touched; no PROVINCE Core or Frontier row is earned | unchanged |
| contract integrity (second order) | separates "instrument registered" from "criterion admitted" and from "surface owned" | up |
| verification (second order) | names the exact verdict map, pins and the red cases a later citation needs | up |

None of these is harmed by the move proposed in §3; §8–§9 are the harm checks.

## 2. Evidence: what the gate actually is, measured

| fact | pointer |
|---|---|
| It is a verdict on a *counter*, not on an artifact: it spawns `config.counter.argv` once per registered reader and reads back only `matched` / `target` / `met_target` from the last JSON line | `tools/round-34/replay-gate.py:76-102` (`run_counter`), `:104-131` (`evaluate`) |
| Its green surface is eight 512-byte synthetic `.mrec` fixtures (`4d524543` magic, not ELF) and eight Python readers; the green counter reorders the name pool and rewrites each `name_off` on an opaque temporary copy, so only record-array traversal survives | `tools/round-34/mini-fix/mini-counter.py:1-9,27-95`; `fixtures/alpha.mrec` = 512 B, sha256 `d1de0e6f…2ad44` |
| Verdict map is 0 CLEAN / 2 REFUSED / 3 UNEVALUABLE, plus 1 for selftest failure | `replay-gate.py:14-16,119-131,283-309` |
| The class list is caller-supplied, config-driven, with a floor of three | `replay-gate.py:31` (`MIN_SHORTCUTS = 3`), `:58`; seven classes registered in `gate-config-mini.json` |
| The config's `predicate` field is required to exist but never compared to anything | `replay-gate.py:41-45`; the only other `predicate` occurrences are selftest literals (`:150,188`) |
| Readers run with `PATH=/usr/bin:/bin`, `HOME=/tmp`, `LANG=C`, 300 s timeout; no REA, no provider, no network | `replay-gate.py:78-82` |
| 26 pins of `claims.json` instruments match the working tree | `python3` sha256 loop, 2026-10-25T07:22:41Z: `pins 26 match 26` (exit 0) |
| The receipts are committed — but after the freeze commit, not in it: at `c79bbe7b` the wave directory holds only `claims.json` | `git ls-tree -r c79bbe7b -- .ufo/waves/round-34/r34b` → 1 path; `git log -- after/c2-at-instruments.json` → `b917ea64` |

Independent runs (scratch copy `…/ConnectorFrontier/r34-root/tools/round-34/`, whose `replay-gate.py` sha256 `8fa94b23…`, `gate-config-mini.json` `4483f385…`, `gate-config-naive.json` `72b12941…`, `c2-shortcut-gate-counter.py` `41d59703…` equal the claim pins):

| command (cwd = scratch root) | exit | output | UTC |
|---|---|---|---|
| `python3 -I -B tools/round-34/replay-gate.py --selftest` | 0 | 12 cases, `failures: 0`, `mutants_killed: 3` | 2026-10-25T07:21:41Z |
| `… --root . --config tools/round-34/gate-config-mini.json --json-out …/green-mini.json` | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=7 shortcuts_over_target=-` | 07:21:41Z |
| `… --config tools/round-34/gate-config-naive.json --json-out …/red-naive.json` | 2 | `REPLAY_GATE_REFUSED … shortcuts_over_target=label-memorization` | 07:21:42Z |
| `… --config …/config-3class.json` (probe: only `all-false`, `size-keyed`, `fixed-slice`) | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=3` | 07:21:43Z |
| `… --config …/config-predicate-junk.json` (probe: `predicate` = `X: a sentence that is not the frozen predicate.`) | 0 | `REPLAY_GATE_CLEAN … shortcuts_below_target=7` | 07:21:44Z |

Receipts for all five runs: `/fast/scratch/hyaku/kaidoku-r34b/w1/ConnectorFrontier/receipts/`. The two probe configs exist only in that scratch copy; no pinned instrument was edited.

## 3. Decision: SKILL.md registry — **registry only**; not Core, not the bar

The gate is a lane instrument whose identity is (entry command, verdict map, selftest spelling, pins, write scope, owner). That is exactly the shape of the `## Round-34 instrument registry` table (`SKILL.md:1182-1190`), which already carries this round's other three instruments; the sibling tables `### Round-27/28 measurement registry` (`:948`) and `### Round-29 measurement registry` (`:957`) are the same pattern one round family earlier. Nothing in the gate earns a Core row or a bar row, and no other home can hold that row's fields.

It is currently registered **nowhere**: `grep -rn 'replay-gate\|replay gate\|shortcut-replay' SKILL.md PROVINCE.md corpus/README.md corpus/QUALITY.md corpus/lessons/round-34.md` returns 0 hits (2026-10-25T07:19Z). The sibling instruments from the same freeze commit are registered (`SKILL.md:1186-1188`). The gap is a missing row, not a missing decision.

### 3a. Exact draft row (append to `## Round-34 instrument registry`)

```
| P34-shortcut-replay gate | gate | `python3 -I -B tools/round-34/replay-gate.py --root <lane> --config tools/round-34/gate-config-mini.json [--json-out <receipt>]`; red case uses `--config tools/round-34/gate-config-naive.json` | 0 `REPLAY_GATE_CLEAN`; 2 `REPLAY_GATE_REFUSED` (a registered shortcut class reached the config target); 3 `REPLAY_GATE_UNEVALUABLE` (`config_*`, `counter_*`, `positive_control_below_target`); selftest failure 1 | `python3 -I -B tools/round-34/replay-gate.py --selftest`: 12 isolated outer-CLI cases (6 verdict/config, 3 config refusals, 3 mutant kills), 2026-10-25T07:21:41Z exit 0, `mutants_killed=3` | `.ufo/waves/round-34/r34b/claims.json` instruments and `.ufo/waves/round-34/r34b/instruments.json` (26 pins, 26/26 match 2026-10-25T07:22:41Z); receipts `.ufo/waves/round-34/r34b/{before,after,controls}/` first committed at `b917ea64`, not at the freeze `c79bbe7b` | read-only over `--root`; writes only `--json-out`; spawns readers with `/usr/bin/python3`, `PATH=/usr/bin:/bin`, 300 s timeout | kaidoku |
```

### 3b. Exact draft sentence (the one this seat was asked for)

> Round-34 registers the pre-freeze structure-blind shortcut-replay gate as a lane instrument, not a Core surface and not a QUALITY criterion: `python3 -I -B tools/round-34/replay-gate.py --root <lane> --config <config>` prints `REPLAY_GATE_CLEAN` (exit 0) only when the registered structural reader reaches the config's target and no registered shortcut class does, `REPLAY_GATE_REFUSED` (exit 2) when one does, and `REPLAY_GATE_UNEVALUABLE` (exit 3) otherwise; its verdict is relative to the caller-supplied class list (three-class floor, seven classes registered) and to a `predicate` field it carries but never compares, so it advances no Frontier bullet and retires none.

## 4. Why the other two homes are wrong

### PROVINCE Core — wrong on the table's own admission rule

1. `PROVINCE.md:31-33`: "ground moves to Core only after an end-to-end probe lands a `LOG.md` entry citing its `evidence_id` and subject sha256." The gate emits no REA evidence id and no subject digest; its counter receipt carries `matched`/`target`/`met_target` only (`replay-gate.py:88-102`). The Core table's four columns (`PROVINCE.md:42`) cannot be filled.
2. Every "Round-N additions to Core" row since round 30 names a REA verb on a carrier (`PROVINCE.md:330-359`: `inspect-rust-binary`, `inspect-sqlite-database`, `inspect`). The round-32 precedent that author-built synthetic carriers *can* enter Core works only because they were fed through `inspect` and left envelopes in `corpus/evidence/round-32/c1/` (`PROVINCE.md:357-359`). The gate never calls REA; "synthetic" is not the disqualifier, "no REA operation" is.
3. PROVINCE has **no** round-33 or round-34 section (`grep -n 'Round-3[34]' PROVINCE.md` → 0 hits, 07:19Z). Core entry would make an instrument the lane's only round-34 domain row, and `corpus/README.md:1-3` ("A row is written when its file exists") would owe a `corpus/knowledge/` entry that has no artifact to describe.
4. Cross-lane cost: Core is the lane's published surface map, refreshed by `rea doctor`, and its rows are read by other lanes as this lane's REA capability (`PROVINCE.md:64-72` registry paragraph). A Python gate with no provider would be read there as REA capability.

### QUALITY.md bar — wrong by the bar's own structure

1. The bar's table is four columns `# | criterion | why (lesson) | supersedes` (`corpus/QUALITY.md:9`); it has no place for an entry command, verdict map, selftest spelling, pin path, write scope or owner. The bar can *name* a checker inside a criterion (as rows 33, 48, 52 do) but cannot *home* one.
2. The criterion this gate enforces already exists: **row 67** (`corpus/QUALITY.md:77`), written from `corpus/lessons/round-34.md` M34-4 for the same failure family. Adding the gate as a row duplicates 67; editing 67 is excluded by the bar's preamble — "A criterion is replaced by a new row naming the row it supersedes, never rewritten" (`:5-7`). The conformance obligations a new gate owes are likewise already rows 61 (outer-CLI self-invocation) and 66 (schema refusal).
3. The bar's rows bind *material admission* and each cites the lesson and red case that produced it. Today's evidence for the gate is its own synthetic surface plus the C2 counter, not a lesson about findings. If a lesson is earned later (e.g. that #67's "for example, size" example is not the class that fires on a given surface — in the red case `size-keyed` stays below target while `label-memorization` fires), that is a *new* row superseding 67 in a later round, not this gate's home.

## 5. Which frontier bullet: **none**

No PROVINCE `## Frontier` bullet is advanced: PE subtypes, recorded crashes >32 MiB, alternate providers, macOS-only surfaces, EVM extended, RISC-V, `.jsc`, adb device surface, operator-blocked engines (`PROVINCE.md:73-95`) are artifact surfaces; the gate touches no artifact. The `corpus/README.md ## Frontier` list is the same class of bullets.

The nearest candidate, and why it is still "no": the stopped **R34-C1 GNU version-needs depth** target. The gate would have refused C1's size-keyed replay *before* the freeze, but it does not run a reader on any carrier and does not re-open or re-score C1 — `claim-stop.json` binds the stop, and `SKILL.md:1203` already says "Apply QUALITY 67 before any future counter freeze; do not reuse this target as admission." Wiring the gate into that bullet would annex the stopped ground by instrument fiat.

Draft statement to use instead of a bullet (mirrors `PROVINCE.md:309-311` and `:332`):

> This round's registry row neither retires a Frontier bullet nor moves one to Core; the only target it guards is a *future* counter freeze on ground the lane still has to earn.

## 6. The ownership question it raises (adjacency)

**Primary — who owns the shortcut-class list?** The verdict is relative to `config.shortcuts`, not to a lane-fixed taxonomy: `MIN_SHORTCUTS = 3` (`replay-gate.py:31`) and the walk only over listed classes (`:112-118`). Measured: a three-class config scores `REPLAY_GATE_CLEAN` with `shortcuts_below_target=3`, indistinguishable in the verdict line from the seven-class CLEAN except by that count (07:21:43Z vs 07:21:41Z). The gate is `--root`/`--config` parameterised, so another lane could ship kaidoku's readers into its own tree and obtain CLEAN against its own three classes. No artifact today owns "which classes count", "who may add or omit one", or "does a CLEAN transfer between configs". This belongs in `PROVINCE ## Adjacent`'s bucket — "Ground the lane refuses or defers — reported to the orchestrator, never absorbed" (`PROVINCE.md:99`) — as a craft-boundary question, and in the round-34 lesson's routed limits. Do not add an Adjacent bullet yet: an Adjacent bullet is a domain refusal, and this is instrument custody inside the lane.

**Secondary — CLEAN is not carrier capability.** A CLEAN states that eight author-built 512-byte fixtures survive permutation under this counter; it says nothing about a shipped artifact or a structural reader on one. If a later round cites CLEAN as evidence a reader handles a real carrier, the gate has swallowed the stopped C1 ground. The registry row's "kind: gate" and the limits column are the only guards; the bar row that would generalise it (see §4.3) is a later act.

## 7. Contradictions and measured limits that constrain the sentence

| # | state | evidence | effect on the draft |
|---|---|---|---|
| C1 | The frozen `predicate_identity` clause is false for two of its three named sites. Config predicate == `claims[0].predicate` (237 chars); the C2 counter's `PREDICATE` constant and the after/control receipts carry a different 351-char sentence. | `claims.json:52`; `c2-shortcut-gate-counter.py:23-27`; `after/c2-at-instruments.json:"predicate"`; string comparison run 07:20Z | already disclosed as `PREDICATE_IDENTITY_FALSE` in `.ufo/waves/round-34/r34b/predicate-reconciliation.json` with repair route "QUALITY 68". The row must not restate predicate identity. |
| C2 | The gate never compares that `predicate` field, so "under the counter's own predicate" is carried, not enforced. | `replay-gate.py:41-45`; my junk-predicate probe: CLEAN, exit 0, 07:21:44Z | this probe is the operational red case for the prospective row 68; the registry row's limits must say the field is carried, not compared, until an instrument supersession (`QUALITY 33`) adds enforcement. |
| C3 | Exit `2` collides with the lane-wide "2 = could-not-evaluate" convention used by the gates registered at `SKILL.md:964,1003,1047-1048,1073,1092,1188`; here `2 = REFUSED` and `3 = UNEVALUABLE`. | `replay-gate.py:14-16` | the row must print the map verbatim; never abbreviate to "0/1/2". |
| C4 | The receipts the claim names are committed one commit **after** the freeze (`b917ea64`), not at `c79bbe7b`. | `git ls-tree -r c79bbe7b -- .ufo/waves/round-34/r34b` → 1 path; `git log -- after/c2-at-instruments.json` → `b917ea64` | cite the gate result only against `b917ea64` (or later), per `QUALITY 18/52`; the row's pin column points at the claims `instruments` map and `instruments.json`, not at the freeze tree. |
| C5 | Seven classes are registered; the floor is three, and the verdict line reports the below-target count only. | probe 07:21:43Z | the row states the floor and the registered count together. |

## 8. Second-order effects across the four surfaces

- **Runtime.** None introduced: the gate reads under `--root`, spawns readers with a stripped environment and 300 s timeout, and writes only `--json-out` (`replay-gate.py:78-82,305-308`). Registering it binds no service, port or provider.
- **Contract.** The registry row becomes the only place that says what CLEAN means; if it omits C2/C3/C5 the next round will over-read a CLEAN. The claim's own `predicate_identity` stays disclosed, not repaired.
- **Substrate.** The instrument's substrate is `/usr/bin/python3` alone — no REA pin, no Ghidra build. That is precisely why it cannot sit beside Core rows that pin `rea-agents@6.5.0`/`6.7.0` + Ghidra 12.1.4 (`PROVINCE.md:42-44,64-72`).
- **Verification.** A later citation of this row needs: the committed receipts at `b917ea64`, the selftest line (12 cases / 3 mutants), and the red case (`label-memorization`). All three are named in the draft row; the two probes I ran are *not* commit-worthy evidence of the claim — they are the limits, and they live in scratch.

## 9. Risks of the recommended move

- **R1** — A row without C2's limit lets a future round claim row-68 conformance from a CLEAN. Mitigation: the limits cell states the `predicate` field is carried, not compared, until a supersession.
- **R2** — A CLEAN from a three-class config reads as exhaustive. Mitigation: state the floor and the registered count (C5).
- **R3** — Citing "exit 2" without the map reads as "could not evaluate" to every other gate row in the same file. Mitigation: print the map (C3).
- **R4** — If the L1 later hardens the gate to compare predicates, that is an instrument change after the freeze: `QUALITY 33` requires an appended `instrument_supersessions` entry and a re-taken before record, and `QUALITY 34/55` forbid re-reading the frozen C2 receipt as the new instrument's result.
- **R5** — Placing it in Core would be read cross-lane as REA capability and would owe a corpus row the gate cannot support (§4.1–4.4).

## 10. What I ran and what I did not

Ran: the five gate invocations in §2 (exits 0/0/2/0/0, UTC 07:21:41–07:21:44Z), the 26-pin sha256 check (07:22:41Z, 26/26), read-only `git ls-tree`/`git log`/`git status`, and text greps. Nothing was written outside `/fast/scratch/hyaku/kaidoku-r34b/w1/ConnectorFrontier/` and this report.

Not run, and therefore not claimed: the C2 counter (`c2-shortcut-gate-counter.py`) — I cite its committed receipt at `b917ea64`, I did not reproduce it; no ELF carrier, fixture or reader executed as a program of interest; no REA call; no network; no package install (no tool was needed).

## Verdict

**R34B-C2 gate home: SKILL.md registry only (round-34 instrument registry row, §3a sentence §3b).** Not Core — the gate emits no REA evidence id or subject digest and PROVINCE admits Core ground only through an end-to-end REA probe. Not the QUALITY bar — the criterion already exists as row 67 and the bar's four columns cannot hold an instrument; the only bar act this round earns is the already-routed prospective row 68, which the gate currently cannot support (C2). No Frontier bullet is advanced; the only ground it guards is the stopped C1 target, which stays stopped. Ownership question raised: who owns the shortcut-class list on which every CLEAN depends.
