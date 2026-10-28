# R45W2MutC1Landing — mutation of the landing (R45-C1 depth)

Seat `R45W2MutC1Landing`, round 45 wave 2, adversarial falsification of the committed
landing. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`. Landing `e715263cb51b713c342ab992d527fe9d61d6f8ff`.
Amendments `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` (A1), `fedd11bf` (A2),
`f59565b782c18b0eb691bec12f52d2f80d9f5032` (A3, the seat spec's revision).
Read-only on the lane: no write, commit, stage or stash; every mutation was applied to a
copy under this seat's scratch, and the lane's `SKILL.md`, `plans/` and `tools/` are
byte-clean (`git status --porcelain -- plans/round-45-claims.md tools/round-45/ SKILL.md`
printed nothing).

**Verdict vocabulary**: `holds` (the artefact survives the attack, with the command that
shows it) / `falsified` (the artefact is wrong; input, differing value, fix) /
`survived` (a mutant the instrument did not catch — a hole) / `not run` (with the reason).

## 0. What was mutated, and what a kill means

| target | identity |
|---|---|
| graded surface | `SKILL.md` at `f59565b7`, 1661 lines, sha256 `36a396ce12f666e1ec1d3449209b866691c927fde377e23bbc4057fda8fe8b1a` |
| the block | rule block 22 of 22 in `## Queue-drain craft`, lines 547–611 (5,613 bytes), marker on line 583, table = header + separator + **10 data rows** |
| the interpreter | `tools/round-45/frozen-path-preflight.py` at the freeze, 315 lines, sha256 `633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b`, `--selftest` = `cases=11 failures=0` |
| the counter (frozen, unmodified) | `tools/round-45/c1-counter.py` at the freeze, sha256 `2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509`, own `--selftest` = `cases=9 failures=0` |

A mutant is **killed** when the frozen counter exits 1 with a clause-specific `failing`
string, or exits 2 `could_not_evaluate`. A mutant **survives** when the counter exits 0
`met_target: true`.

Fixtures: `git -C "$D" init -q` inside `/fast/scratch/hyaku/kaidoku-r45/R45W2MutC1Landing/fixtures/<tag>`,
carrying the real bytes at `f59565b7` for exactly the seven paths the counter reads
(`SKILL.md`, the interpreter, `plans/round-45-claims.md`, and the four files block 22
cites, so line counts are the landing's). Before the first commit each fixture asserted
`git -C "$D" rev-parse --show-toplevel == $D`. Every mutant is one commit on top of a
pristine `freeze` commit; commit dates are pinned (`2026-10-28T16:00:00+0000`) so two
consecutive runs produced identical receipt bytes (15/15 receipts, same stdout sha256).
The counter reads git objects only, so the minimal fixture is the counter's own
`make_repo` shape and cannot change a verdict.

## 1. Baselines (a failing baseline would make every mutant inconclusive)

| baseline | command | exit | receipt |
|---|---|---|---|
| lane, freeze→A3 | `c1-counter.py --root <lane> --freeze f762b727 --rev f59565b7` | **0** | `rule_blocks 22`, `block22_present 1`, `rows 10`, `refs 8`, `unresolved []`, `selftest 11/0`, `met_target true`; stdout sha256 `90597e617067fe4f…` |
| pristine fixture | same, `--root fixtures/m0-pristine`, freeze=rev | **0** | identical values to the lane row (rows 10, refs 8) |
| do-nothing control | `--freeze f762b727 --rev f762b727` | **1** | byte-identical (as JSON) to the frozen `controls/ctl-c1-0-do-nothing.json` |

All three are green/expected, so the mutants below are interpretable.

## 2. The six assigned mutations — all six caught

| # | mutation | exit | `failing` string | file sha256 before → after | stdout sha256 |
|---|---|---|---|---|---|
| m1 | delete the marker line only (`-  <!-- freeze-integrity-table v1 -->`) | 1 | `block22_present 0 != 1`, then `block22_rows 0 < 8`, `block22 table header lacks trigger/arm/exit/receipt`, `block22_refs 0 < 4` | `36a396ce…` → `bb7e681085e2cb7e…` | `7ec97cfefbd24093…` |
| m2 | drop the table to 7 data rows (delete `unknown freeze or rev`, `no touch…`, `FREEZE equals REV`) | 1 | `block22_rows 7 < 8` (the only reason) | → `b2cb95d5b3440fec…` | `7405e15c999c0a71…` |
| m3 | one exit cell `2` → `3` on the `pathspec (--require-pathspec)` row | 1 | `block22 exit cells outside {0,1,2}: 1` | → `26c0135b04f3ee63…` | `0b98cb9f1c4fcfef…` |
| m4 | one citation one line past the file's end: `corpus/lessons/round-45.md:12-17` → `:12-188` (the file is 187 lines) | 1 | `unresolved citations: ['corpus/lessons/round-45.md:12-188']` | → `594a2a2e257a9fd6…` | `2e688cd94d300df9…` |
| m5 | remove the `S140` token (both occurrences in the block: prose and the dirty row) | 1 | `block22 does not cite S140` | → `95e40bc171992cd9…` | `da0d98b088f87687…` |
| m6a | break the interpreter so its selftest fails — the `--check-dirty` arm body deleted (315 → 308 lines), body placed **at the freeze** (rev = freeze) | 1 | `preflight selftest {'ok': False, 'exit': 1, 'cases': 11, 'failures': 1}` | `633ebc05…` → `0861d831d0b3ac43…` | `2accc23035821552…` |
| m6b | same broken body, committed **after** the freeze (`M tools/round-45/frozen-path-preflight.py`) | 2 | `{"counter":"round-45-c1","verdict":"could_not_evaluate","reason":"frozen_path_changed","frozen_path_changed":["tools/round-45/frozen-path-preflight.py"]}` | `633ebc05…` → `0861d831d0b3ac43…` | `7b942b02725d4209…` |

**m6 is one mutation with two honest placements, and the placement decides the arm.**
`tools/round-45/` is frozen, so a landed break can only arrive through a frozen-path
touch: the counter then refuses to score (exit 2) rather than reporting a pass — that is
m6b, and it is the stronger answer. The selftest clause itself is exercised when the
interpreter at the freeze is already broken (or the freeze is re-pointed), which m6a
shows exits 1 with the red case named. Neither placement can reach `met_target: true`:
the counter's clause 6 is not bypassable by a broken interpreter that still fails its own
cases.

**Verdicts for the six: all `holds`.** The artefact — a 22-block craft section with one
marked 10-row table, in-`{0,1,2}` exit cells, in-set resolving citations, `S140` and the
interpreter cited, and an interpreter whose 11 red cases pass — is what the counter
measures, and each clause is exercised on the genuine bytes, not only on the counter's
synthetic `good_block()` fixtures.

## 3. Probes the six do not reach (seven more mutants)

| # | mutation | exit | `failing` string | verdict |
|---|---|---|---|---|
| m1b | a **second** marker inserted inside block 21 (rule-block count unchanged at 22) | 1 | `block22_present 2 != 1` (+ the same three cascades) | killed — clause 2 holds **from above** too. `R45-CL7` says the counter's *selftest* has no two-marker fixture; the code at the landing is correct |
| m8 | a 23rd `- **23.` block appended to `## Queue-drain craft` | 1 | `rule_blocks 23 != 22` | killed — clause 1 holds from above as well (same CL7 note: case-set gap, not a code gap) |
| m3b | exit cell `1` → `2` on the `touched` row — a **legal** value that contradicts the gate | **0** | `[]`, `met_target true` | **survived — new hole (§4.1)** |
| m4b | citation replaced by `LOG.md:99999` (a path outside the validated set) | **0** | `[]`; `block22_refs` 8 → 7, still ≥ 4 | survived — already routed (`R45-CL9` A2, `R45-CL13` b) |
| m4c | citation moved to an **in-range** line of a file that does not support it: `corpus/lessons/round-44.md:18-19` → `corpus/lessons/round-45.md:1-2` | **0** | `[]`; refs stay 8 | survived — already routed (`R45-CL13` b: resolution is path+line, not topicality) |
| m7 | all 10 data rows replaced by `\| zzz \| yyy \| 1 \| www \|` (structure intact, semantics empty) | **0** | `[]` | survived — already routed (`R45-CL4`, `R45-CL13`) |
| m6c | interpreter replaced by a 4-line stub that prints `PREFLIGHT_SELFTEST: cases=11 failures=0` and exits 0 | **0** | `[]` | survived — already routed (`R45-CL13` a: no sha256 pin) |

`m6c` is the reproduction that matters most for calibration: wave 1 showed the stub passing
on the critic's 44-line forgery; this run shows it passing **against the genuine landing** —
the 5,613-byte block is untouched and only the instrument is gutted, and the counter still
prints `met_target: true`. The landed block is genuine; clause 6 is self-certifying.

## 4. Findings

### 4.1 NEW — the exit column is domain-checked, never compared with the arm (`m3b`)

Input: the genuine block, one character changed —
`| any commit in FREEZE..REV touches a frozen path | commit (git log --name-status, S141) | 1 | … |`
becomes `… | 2 | …`. Counter exit **0**, `met_target: true`, receipt
`counter-m3b.json`. The counter reads `exit_col` and accepts any cell in `{0,1,2}`
(`c1-counter.py` `evaluate`: `row[exit_col].strip("` ") not in {"0","1","2"}`); nothing
ties the cell to what the arm actually returns.

I checked the landed table against the frozen interpreter by reading its source, and the
table is **right on 10/10 rows**: commit/restored/blob/dirty/bulk-sweep → 1
(`ok = not touched and not blob_changed and not restored and not dirty`, line 142; exit at
line 155); pathspec → 2 (`{"reason": "pathspec_required"}`, line 90); unknown freeze, unknown
rev and non-ancestor → 2 (lines 77, 81, 84); clean and empty range → 0 (exit at line 155
with `ok` true). Line numbers are the frozen interpreter's. So this survivor is a **coverage hole in the measure, not a
misstatement in the landing**: any of the ten exit cells could be flipped to another legal
value and R45-C1 would still score 0. I find no routed item that names this class (`CL4` is
"semantically empty rows"; `CL13(c)` is header substring tests; `CL13(e)` is block counting).
The frozen sentence claims only "every row's exit cell is exactly one of `0`,`1`,`2`", so
this **does not falsify R45-C1** — it bounds what the depth claim can mean.
Round-46 re-freeze: bind each row's exit to a literal invocation of its arm, or add one
exit-only mutant per row to the counter's case set.

### 4.2 Reached by this wave's landing bytes but already in the record (no new routing)

- `m4b` / `m4c` → `R45-CL9` (A2) and `R45-CL13` (b). The citation arm validates
  `corpus/(knowledge|lessons)/**.md` and `plans/**.md` only, with or without a line
  selector (the landed block has one line-less ref, `plans/round-45-claims.md`, which
  counts toward `refs`), and it validates ranges, not support.
- `m7` → `R45-CL4` / `R45-CL13` (structurally valid, semantically empty rows pass).
- `m6c` → `R45-CL13` (a). Reproduced on the genuine block (§3).

### 4.3 What survived that would *falsify* the landed artefact: nothing

I tried to make a true reading of the block disagree with the counter and could not:
22 rule blocks in the craft section, exactly one marker, a 10-row table with header
`trigger | arm | exit | receipt` and all exit cells in `{0,1,2}`, 8 located references
(all resolving at `f59565b7`), `S140` and the interpreter path both present, `S141` present
in the commit row, `S140`/`S141` rows real at `corpus/SOURCES.md:146-147`, the interpreter
present with 11/11 red cases green. The block also states its own limits in prose
(arm-covering-not-isolating, the `--dirty-pathspec` false-clean, the plain-form commit arm,
the merge blindness) — I did not find a prose claim that the counter contradicts.

## 5. Record checks (read-only, lane)

| check | command | result |
|---|---|---|
| four score receipts reproduce | frozen counter at each recorded rev, diffed against `l1/scores/c1-at-*.json` | **all identical**: `e715263c` (refs 6), `1f4b27f8` (refs 7), `fedd11bf` A2 (refs 8), `f59565b7` A3 (refs 8); all exit 0, rows 10, selftest 11/0. `record-compare.json` |
| do-nothing control reproduces | `--freeze f762b727 --rev f762b727` | identical to `controls/ctl-c1-0-do-nothing.json` (exit 1, **five** reasons) |
| frozen paths untouched through HEAD | `git log -1 --format=%H -- tools/round-45/`; `git status --porcelain -- plans/round-45-claims.md tools/round-45/ SKILL.md` | last touch = `f762b727` (the freeze itself); status empty → no commit in `FREEZE..HEAD` touches a frozen path, so the A3 score is admissible |
| counter selftest from the freeze bytes | `git show f762b727:tools/round-45/c1-counter.py` → `--selftest` | `C1_SELFTEST: cases=9 failures=0` — matches `R45-CL7`'s "9-case selftest" (the claim's `cases >= 11` is the *preflight's* selftest, which is 11/0) |
| cited sources exist | `git show f59565b7:corpus/SOURCES.md` | `S140` at line 146, `S141` at line 147; both cited by the block |

Two record notes, neither falsifying:

1. **Ticket metadata is stale, not wrong.** The ticket names A1 `1f4b27f8` as "the measured
   revision". The lane re-measured at A2 (`fedd11bf`) and A3 (`f59565b7`) and `SCORECARD`/
   `LOG` record those; all four revisions score 0 and the A1 receipt reproduces exactly.
   The seat spec's `f59565b7` is the newest, which is why every mutant in §2–§3 was built
   on it (the block's located references grew 6 → 7 (A1) → 8 (A2, A3); the table stayed at
   10 rows and every exit cell unchanged).
2. **LOW — the claims' "Before" sentence under-enumerates its own receipt.**
   `plans/round-45-claims.md` (R45-C1) says the do-nothing control exits 1 with
   `rule_blocks 21 != 22`, `block22_present 0 != 1`, `block22_rows 0 < 8`,
   `block22_refs 0 < 4` — four reasons. The frozen receipt, and my re-run, carry a fifth:
   `block22 table header lacks trigger/arm/exit/receipt`. Nothing claimed is false
   (the exit code and all four listed reasons hold); a round-46 erratum should append the
   fifth, since the file is frozen.

## 6. Not run (and why)

- **C2 registry rows** — other seats' surface; I made no SKILL.md registry mutation and do
  not report a calibration verdict.
- **Per-arm isolation of the preflight** (`R45-CL15`: deleting `restored` or the blob arm
  alone leaves 11/0; the `--dirty-pathspec` false-clean) — already reproduced in wave 1 on
  the frozen bytes. My m6a is an aggregate selftest failure, not an isolation probe.
- **Merge-commit blindness** (`R45-CL6`) — needs a merge fixture whose resolution edits a
  frozen path; outside this seat's six and already routed with a reproducer.
- **Live fetch of S140/S141** — source seat `R45W2Src141`; I verified only that the rows
  exist and that the block parses the formats the rows describe.
- **A receipt-column mutation** (empty the `receipt` cells while keeping the header) was
  predicted to survive by the same argument as m7/§4.1 but was not run; no claim here rests
  on it.

## 7. Reproduction

```sh
S=/fast/scratch/hyaku/kaidoku-r45/R45W2MutC1Landing   # tmp/fixtures only; recreated by the driver
D=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-45/w2/R45W2MutC1Landing
export TMPDIR="$S/tmp" HYAKU_SCRATCH="$S/tmp"

# baseline (must be 0)
python3 -I -B tools/round-45/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze f762b7273e3f6ca3c710bb37d5de92a4a4417aec \
  --rev f59565b782c18b0eb691bec12f52d2f80d9f5032 --json-out "$S/baseline.json"

# every mutant, from the frozen counter; driver.py was copied into this report directory
python3 "$D/driver.py"
```

`driver.py` (sha256 `5dc23a4342d07e23651d5eddb5602ab38b41f97fd5329056b8635045eda4bf62`, copied here)
builds the seven real-byte fixture paths with `git show <rev>:<path>`, commits with pinned
dates, applies one named mutation, and runs the frozen counter per fixture.
`diffs.txt` (sha256 `46dfe92ef4d6e76b2b46eccdb770513c9e4bce28d02e67e874e49b45a8db75cb`)
holds the verbatim `git diff` of every mutant. `receipts.json` holds command, exit, UTC,
stdout sha256 and the counter's receipt for all 15 runs; `checks.json` and
`record-compare.json` hold the baselines and the four receipt comparisons.

## 8. Environment and cleanup

Python 3.14.8, git 2.56.0. No installs, no upgrades, no PATH writes (pacman untouched —
nothing was needed). Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W2MutC1Landing` was
removed after the receipts above were copied here. One temporary file, `/tmp/prev.json`,
was written solely to compare two consecutive runs for determinism and was deleted
immediately; no receipt depends on it, and nothing else was written under `/tmp` or
anywhere in the lane outside this seat directory. No restoration of the lane was necessary:
the mutations were applied exclusively to fixture copies, the lane's `SKILL.md` was never
opened for writing, and it still hashes `36a396ce12f666e1…` at `f59565b7` (the before/after
hashes in §2 are those of the fixture copies).
