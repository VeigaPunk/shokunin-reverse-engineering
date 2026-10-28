# R45W2CommandA — adversarial falsification: command A and the axis verdicts

Seat `R45W2CommandA`, kaidoku-shokunin round 45 wave 2. Read-only on the lane tree; every
mutation below is a **copy** under `S=/fast/scratch/hyaku/kaidoku-r45/R45W2CommandA`
(two `git init`-ed fixtures, toplevel asserted before the first commit and before each
mutation commit). No lane file, no frozen path, no `plans/`, `tools/`, `corpus/`, `LOG.md`
or `SCORECARD.md` was written. No install was needed and none was made.

Frozen inputs as given: freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, landing
`e715263cb51b713c342ab992d527fe9d61d6f8ff`, A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`,
A2 `fedd11bf5ff9fe42d061169f78d77df59af4eca1`, measured revision A3
`f59565b782c18b0eb691bec12f52d2f80d9f5032`. Command A is the block extracted verbatim from
`SCORECARD.md` `## Measurement recipes` (1530 bytes, sha256
`6cc5081894f7f4aee2ff9c894b12d5cec5c38883a9341c0d9b9ed62f15cb4804`), run unmodified.

## 1. Command A at both required revisions — both numbers CONFIRMED exactly

| revision | `knowledge_files` | `mapped` | `rule_blocks` | `citation_resolved_rules` | `coverage_score` | `depth_score` |
|---|---|---|---|---|---|---|
| base `149133d4` (context) | 138 | 138 | 21 | 21 | 10.0 | 10.0 |
| landing `e715263c` | 138 | 138 | 22 | **21** | 10.0 | **9.55** |
| A1 `1f4b27f8` | 138 | 138 | 22 | 22 | 10.0 | 10.0 |
| A2 `fedd11bf` | 138 | 138 | 22 | 22 | 10.0 | 10.0 |
| **A3 `f59565b7` (measured revision)** | **138** | **138** | **22** | **22** | **10.0** | **10.0** |

Raw stdout, A3 (exit 0):

```json
{"citation_resolved_rules": 22, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 138, "mapped": 138, "missing": [], "revision": "f59565b782c18b0eb691bec12f52d2f80d9f5032", "rule_blocks": 22}
```

Raw stdout, landing (exit 0):

```json
{"citation_resolved_rules": 21, "coverage_score": 10.0, "dangling": [], "depth_score": 9.55, "knowledge_files": 138, "mapped": 138, "missing": [], "revision": "e715263cb51b713c342ab992d527fe9d61d6f8ff", "rule_blocks": 22}
```

* **"138/138 and 22/22 at the measured revision" — holds.** Both values reproduce exactly at
  A3, and identically at A1 and A2. `missing []`, `dangling []`, `coverage_score 10.0`.
* **"the landing alone read 21/22 before A1" — holds.** `citation_resolved_rules 21`,
  `depth_score 9.55` (= round(10·21/22, 2)). Recomputing the recipe's own rule loop per block
  identifies the single failure as **rule 22 only** (`failing rule numbers: [22] of 22`); the
  other 21 blocks resolve at the landing as well. So the record's `21/22` is one block, not
  a diffuse degradation.
* Mechanism, from the A1 diff alone (`git diff e715263c 1f4b27f8 -- SKILL.md`): A1 inserts one
  `corpus/knowledge/...md:40-66` reference plus one honest-limit paragraph. Nothing else in
  the craft section changes. That is the whole of `9.55 → 10.0`.

## 2. Verdicts

`holds` = the claimed artefact survives the input I gave it. `falsified` = the artefact is
wrong, with the exact input and the differing value. Exit codes are semantic (0 met, 1 not
met, 2 could-not-evaluate); no `2` is treated as a pass.

### V1 — block 22's citation resolves and discusses red/green cases — **holds**

Input: `git show f59565b7:corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`
then lines 40–66.

* File length at the measured revision (and at the landing): **79 lines** ≥ 66, so `:40-66`
  is inside the file. The recipe's bound check `1 <= 40 <= 66 <= 79` passes; `c1-counter`
  independently reports `block22_unresolved_citations []`.
* The window does discuss the gate's red/green cases, not just line numbers that happen to
  exist: green target `8/8` per class (lines 42–46), "Registering any of them flips the same
  gate to `REFUSED`" (48), "the frozen green surface did not force it" (54), "prints `CLEAN`
  even on the red config" (59), "dropping classes down to `MIN_SHORTCUTS = 3` still prints
  `CLEAN`" (60).
* Precision caveat (does not flip the verdict): the window is contiguous and over-broad.
  The 3-verdict/exit table (`REPLAY_GATE_CLEAN|REFUSED|UNEVALUABLE`) is at 16–20 and the
  red/green **config definitions** at 24 and 30–31 — all outside `:40-66`. A reader who
  follows only the citation meets the *outcomes* (`REFUSED`, `CLEAN`, `8/8`) without their
  definitions, and lines 50–53 are S106 `readelf` mechanism detail. `:40-49,54-60` would cite
  the same evidence tightly. Severity: low, calibration.

### V2 — "22/22 certifies block 22's knowledge grounding" — **FALSIFIED**

The depth proxy counts a block as resolved iff it contains ≥1 `corpus/knowledge/*.md` ref
whose line span fits inside the file. It never reads whether the cited knowledge is the one
the block is about, nor how much of it is cited. Measured on a scratch fixture holding the
A3 `SKILL.md` + `corpus/knowledge` + `corpus/README.md` (baseline reproduces A3: 22/22, 10.0):

| mutation of block 22's single knowledge cite (fixture copy) | `citation_resolved_rules` | `depth_score` |
|---|---|---|
| baseline (A3 bytes) | 22 | 10.0 |
| **M1** → `corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:1-66` (topically unrelated, 979 lines) | **22** | **10.0** |
| **M2** → same r34b file, `:1-1` (the title line only) | **22** | **10.0** |
| **M3** (control) → same r34b file, `:160-170` (past EOF) | 21 | 9.55 |

M1 and M2 score identically to the real citation; M3 shows the proxy discriminates only on
presence and line bounds. So `depth_score 10.0` is not evidence that block 22's rule is
grounded in the cited knowledge, and the `9.55 → 10.0` movement is a *documentation* repair
(one pointer added to a block that already carried 6 resolving non-knowledge citations —
`c1-counter` reads `block22_refs 6` at the landing), not a depth gain. This is consistent
with the record's own `met (instrument non-discriminating)` verdict on R45-C1 (R45-CL13/14),
but the **depth axis row** and the "quality improved … the depth proxy held at 22/22"
learning-trend sentence still read as if 22/22 carried that weight. Route: restate the depth
row as "citation-presence proxy held at 22/22", or add a fidelity clause (the cite must name
a file whose `sources:`/subject matches the block).

### V3 — the depth axis verdict at the endpoints — **holds**

Base `149133d4`: `rule_blocks 21`, `citation_resolved_rules 21`, `depth_score 10.0`.
Measured A3: `22/22`, `10.0`. `10 → 10` is correct at both endpoints, and the intermediate
`9.55` at the landing is disclosed in the record (header paragraph of `## Round 45`). No
number in that row is wrong; V2 attacks what the number is taken to mean.

### V4 — `SCORECARD.md:3581` ("every value is identical at both") — **FALSIFIED**

Input: `c1-counter` at `1f4b27f8` and at A2 `fedd11bf`, same `--freeze f762b727`.

| field | `1f4b27f8` | `fedd11bf` |
|---|---|---|
| `block22_refs` | **7** | **8** |
| `rule_blocks` / `block22_rows` / `met_target` / `failing` | 22 / 10 / true / [] | 22 / 10 / true / [] |

The record's own receipts say the same: `.ufo/waves/round-45/l1/scores/c1-at-1f4b27f8.json`
→ `block22_refs 7`; `…/c1-at-A2.json` → `block22_refs 8`. The sentence contradicts its own
two receipts. Fix: "the verdict fields (`met_target`, `failing`, `rule_blocks`,
`block22_rows`) are identical at both; `block22_refs` is 7 at `1f4b27f8` and 8 at A2."

### V5 — `SCORECARD.md:3591` ("the values are identical at `e715263c`, `1f4b27f8`, `fedd11bf` and A3") — **FALSIFIED**

| revision | `block22_refs` (c1-counter) | `citation_resolved_rules` / `depth_score` (command A) |
|---|---|---|
| `e715263c` | **6** | **21 / 9.55** |
| `1f4b27f8` | **7** | 22 / 10.0 |
| `fedd11bf` | **8** | 22 / 10.0 |
| A3 `f59565b7` | **8** | 22 / 10.0 |

Both instrument families move across the four revisions; only the verdicts
(`met_target true`, `failing []`, exit 0) are invariant. The sentence is false for the fields
it names, and doubly so if "the values" means the axis values (depth is 9.55 at `e715263c`).
Fix: "the **verdicts** are identical at all four revisions; `block22_refs` reads 6/7/8/8 and
command A reads 21/22 blocks at `e715263c` before A1."

Note the immutable `## Round 45` table is *right*: its R45-C1 "after" cell says
`block22_refs 7` measured at `c1-at-1f4b27f8` and my run reproduces 7. Only the two
append-only amendment sentences overstate identity, which is the risk of append-only prose:
it is checked less than the table it amends.

### V6 — `SKILL.md:590`, table row 5 (pathspec arm) — **FALSIFIED (narrow)**

Row as landed: `a frozen path is a directory at FREEZE and no pathspec covers it | pathspec
(--require-pathspec) | 2 | uncovered_frozen_dirs[]; a whole-tree scan is refused`.

Fixture D2: freeze commit `16c3288` contains `tools/round-45/` as a directory; clean tree.

* `--require-pathspec` **alone**, no `--pathspec`, no `--freeze-path` → **exit 0**,
  `verdict clean`, and **no `uncovered_frozen_dirs` key at all**. The row's exit 2 does not fire.
* `--require-pathspec --freeze-path tools/round-45`, still no `--pathspec` → exit 2,
  `reason pathspec_required`, `uncovered_frozen_dirs ["tools/round-45"]` — the row's receipt,
  but only when a second flag the arm cell does not name is also passed.
* `--freeze-path tools/round-45` without `--require-pathspec` → exit 0 clean.

So the arm needs **two** flags and the cell names one. A caller who reads the ordered
decision list literally and passes the named flag gets `clean` on a directory freeze with no
pathspec coverage — the round-44 defect shape the row exists to refuse. The block's prose
elsewhere does say an invocation must name every frozen path with `--pathspec` **and** the
matching `--freeze-path` values, so a careful reader recovers; the row alone does not.
Fix: `pathspec (--require-pathspec plus --freeze-path <dir>)`.

### V7 — table rows 1, 2, 3, 4, 9, 10 exit cells — **hold**

Same fixture (freeze `16c3288` → touch `a274b7f` → restore `d8090a9`):

| row | invocation | observed |
|---|---|---|
| 1 touch | `--pathspec tools/round-45/ --freeze-path tools/round-45` @ touch | exit **1**, `verdict frozen_path_changed`, `touched[{commit, path, status:"M"}]` |
| 2 restored | same @ restore | exit **1**, `restored ["tools/round-45/c1-counter.py"]`, `blob_changed []` — disjoint as the receipt cell claims, and the restore does **not** un-block |
| 3 blob/tree oid | same @ touch | `blob_changed ["tools/round-45", "tools/round-45/c1-counter.py"]` — the directory entry is the subtree oid, as the cell says |
| 4 dirty | `--check-dirty` with a modified frozen file in the worktree | exit **1**, `dirty [" M tools/round-45/c1-counter.py"]` |
| 9 clean | clean tree | exit **0**, `verdict clean` |
| 10 empty range | `--freeze X --rev X` | exit **0**, `verdict clean` |

The "exit column is the gate's" reconciliation is also true where it matters: on the same
touch/restore the *counter* exits **2** `frozen_path_changed` with no `met_target` key
(V8), while the gate exits 1. The claims file's "a touch makes the counter exit 2" and the
table's row-1 `1` are both correct once the sentence between them is read.

### V8 — counter freeze arm (exit 2, restore does not un-block) — **holds**

`python3 -I -B tools/round-45/c1-counter.py --root <fixture> --freeze 16c3288 --rev <rev>`:

* at touch `a274b7f`: exit **2**, `{"frozen_path_changed": ["tools/round-45/c1-counter.py"], "reason": "frozen_path_changed", "verdict": "could_not_evaluate"}`, no `met_target`.
* at restore `d8090a9`: exit **2**, same payload. History, not tip equality, as claimed.

### V9 — block 22's `--dirty-pathspec` false-clean disclosure — **holds (disclosure is accurate)**

Dirty the frozen file in the worktree, then:
`--check-dirty --dirty-pathspec SKILL.md --pathspec tools/round-45/ --freeze-path tools/round-45`
→ exit **0**, `verdict clean`, `dirty []`. The flag really does replace the dirty arm's scope
instead of adding to it, exactly as block 22 states and routes (R45-CL15). Good: a disclosed
limit that reproduces is worth more than an undisclosed one.

### V10 — finding: the dirty arm cannot see an *ignored* file inside a frozen directory

The arm parses `git status --porcelain -z` without `--ignored`. The lane at the measured
revision contains `tools/round-45/__pycache__/` (gitignored via `.gitignore:1`, mtime
2026-10-28T15:32:44Z — pre-existing, not created by this seat; every invocation here uses
`-B`), and the gate over both frozen pathspecs reports `dirty []`, `verdict clean`, exit 0.
Severity low — `git add -A` will not stage ignored files, so a sweep cannot commit them and
blob scoring is unaffected — but the block's headline failure mode is "files sitting dirty
under a frozen directory", and an ignored file does sit there today while the gate reads
clean. If that is intended, say it; otherwise `--ignored` (or a documented exclusion) closes it.

### V11 — finding: the exit-2 receipt does not echo its own inputs

`c1-touch` and `c1-restore` produce **byte-identical stdout**
(sha256 `0db762f175737cad808e625fa7b5672b6896e6ec140d85747d9ce3a3a1d864ec`): the could-not-
evaluate JSON carries `counter`, `frozen_path_changed`, `reason`, `verdict` — no `rev`, no
`freeze`. Two different admissibility refusals are indistinguishable receipts, so the receipt
cannot be tied to the measurement it refused. Low severity (the command line carries it);
the fix is one line: add `rev`/`freeze` to the exit-2 payload.

## 3. Receipts

Every receipt: exact command, exit, sha256 of stdout, UTC. Fixture commits:
D1 baseline `c4b3d81945e947c4328ddb2dff89eaaf22df732a` (A3 bytes copied), M1
`3fa78e0b0202fa1486f31af81b4e8029ac4dce11`, M2 `959d070edeed417a4999b4813bc7e8d715e9dd69`,
M3 `5f62ab57feff28d795bb89fe1d1104c0dc3b20b4`; D2 freeze `16c328842b34c268f380e084261a212904923774`,
touch `a274b7f2b8f51701d6f008c8722b543e61782a28`, restore `d8090a95cdb90734a938aff50aae7f5ebaf1157e`.

| receipt | exit | stdout sha256 | UTC |
|---|---|---|---|
| `A-149133d4` command A @ base | 0 | `759dc7bbd53166dbcd406aba14b3ee4d6540d3335f47fe94116f3601c407bf11` | 2026-10-28T16:03:08Z |
| `A-e715263c` command A @ landing | 0 | `bbbf9e61726c07405c6eb000b306843b06a1f7285fb11890abb2c0d7dc15ae94` | 2026-10-28T16:03:09Z |
| `A-1f4b27f8` command A @ A1 | 0 | `b8f35e3e9f2be3aaf37f30a5f49136010ef0a310e55d705b00ad959e86c97f9a` | 2026-10-28T16:03:09Z |
| `A-fedd11bf` command A @ A2 | 0 | `d715884080e8de26a58f8b0ecc24357115a9d3c5a08ed038e34e0cf68ef379ca` | 2026-10-28T16:03:09Z |
| `A-f59565b7` command A @ measured | 0 | `ea7c9d876ae05de7203a143a10d6c14888f7aaf94d1562786746aa2d6df3bbb9` | 2026-10-28T16:03:09Z |
| `c1-e715263c` c1-counter @ landing | 0 | `cb869305df9b64d68e106ce1acfa326dd6d73c8b15f18b07d7546b898c5cc95f` | 2026-10-28T16:03:09Z |
| `c1-1f4b27f8` c1-counter @ A1 | 0 | `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b` | 2026-10-28T16:03:09Z |
| `c1-fedd11bf` c1-counter @ A2 | 0 | `5bbfa17f1ea8c695f3105ec3532d6f6cec2869539d1b59c983098814e159480f` | 2026-10-28T16:03:10Z |
| `c1-f59565b7` c1-counter @ measured | 0 | `90597e617067fe4f17399c7e114f36ff5ce7e7da24cb3ce7d06d3b43e57b6f18` | 2026-10-28T16:03:10Z |
| `c2-A3` c2-counter @ measured | 0 | `a352f65c098e76f8a00dcb8a86725036f85fc26e86aef0d57db61061e42041d4` | 2026-10-28T16:03:10Z |
| `fixture-baseline` command A @ D1 baseline | 0 | `e26ddf7edbc3dc5068d36b27ea300598c84d352620bbb003c73ba4149db12894` | 2026-10-28T16:03:16Z |
| `M1-unrelated` command A @ M1 | 0 | `cd7ead0584bb2f123592b8fcc878bbf54af94abe9314ae2d08113d5964ce3fe6` | 2026-10-28T16:03:16Z |
| `M2-one-line` command A @ M2 | 0 | `db655c8efdafdcc4153d29a4785669f2acc74576ca2378bbe5570ff395be5e6f` | 2026-10-28T16:03:16Z |
| `M3-out-of-range` command A @ M3 | 0 | `f4dab15b84a61f7005a2a75d76213d1f271a312ab7ca12507ad00499d11636cd` | 2026-10-28T16:03:16Z |
| `gate-clean` preflight @ freeze | 0 | `fa29a71594f6e41509f18ec53882160c8f424ea1ae572998f5bb282610e8b5d8` | 2026-10-28T16:03:16Z |
| `gate-touched` preflight @ touch | 1 | `8df7c5415fe27a3696b6b73bb939b17a8322dd77377fbcbc38d14196824c642d` | 2026-10-28T16:03:16Z |
| `gate-restored` preflight @ restore | 1 | `871f3692a85e741ac461b584ef8e28f07da3adf780cb0b60db7ff649cc4fcebb` | 2026-10-28T16:03:16Z |
| `gate-A4-require-with-fp` `--require-pathspec --freeze-path` | 2 | `987f30d1c20c15eb147d30dd157eeb4e3799e481cbfd2c32b15e6c4c1d418580` | 2026-10-28T16:03:16Z |
| `gate-A2-require-only` `--require-pathspec` alone → clean | 0 | `7f4d84f147af6c572156a1eb98b838e22a0a06386763c057107a5087c41b76cb` | 2026-10-28T16:03:16Z |
| `c1-touch` counter @ touch | 2 | `0db762f175737cad808e625fa7b5672b6896e6ec140d85747d9ce3a3a1d864ec` | 2026-10-28T16:03:16Z |
| `c1-restore` counter @ restore | 2 | `0db762f175737cad808e625fa7b5672b6896e6ec140d85747d9ce3a3a1d864ec` | 2026-10-28T16:03:16Z |
| `gate-lane-dirty` lane gate, `--check-dirty`, both pathspecs | 0 | `565f72513f20c7737a59da495e62062c33cd68f95a75d59348ddf18392d1ea7d` | 2026-10-28T16:03:32Z |

Full TSVs (`receipts.tsv`, `receipts-fixture.tsv`) and the captured stdout of every run are
beside this report. `$S` was removed after these were copied; the fixture commit ids above
are the only handles to D1/D2, both of which were scratch.

## 4. What the L1 has to reconcile

1. **V2** is the real attack on an axis verdict: `22/22` is a presence-and-bounds proxy. It is
   true, it is reproducible, and it does not mean what the depth row implies. Either restate
   the row (cheap, honest) or bind a fidelity clause next round.
2. **V4/V5** are two false identity sentences in append-only prose at the measured revision.
   They are contradicted by the record's own receipts. Fix the wording; do not re-measure —
   every measurement in the table is correct.
3. **V6** is a live false-clean in the decision list that block 22 tells the reader to follow
   in order. It is one clause of one cell, and the surrounding prose already says the right
   thing.
4. **V10/V11** are instrument-quality, both low; V10 is the one that matches the round's own
   headline failure mode.

No claim in `plans/round-45-claims.md` is falsified by this seat: R45-C1's target
(`failing == []`, exit 0) and R45-C2's target (`unregistered []`, `thin []`) both reproduce at
the measured revision, and command A's two numbers are exact. What fails is the *inference*
drawn from the depth number and three sentences of record prose plus one table cell.
