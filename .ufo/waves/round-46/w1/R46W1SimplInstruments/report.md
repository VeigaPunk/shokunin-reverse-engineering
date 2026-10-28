# R46W1SimplInstruments — YAGNI review of `tools/round-46/`

Seat: leaf member, no subagent dispatch. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Scratch: `/fast/scratch/hyaku/kaidoku-r46/R46W1SimplInstruments` (`TMPDIR`/`HYAKU_SCRATCH` both set to it;
nothing under `/tmp` was used or cited). Read-only on the lane except this report directory; no git
mutation anywhere, no commit, no stage, no install.

---

## 0. What was measured — two byte sets, both named by sha256

The lane advanced while this seat was running. Two byte sets were measured, and every number below
says which one it came from.

| label | commit | `attest.py` | `gate.py` | `registry.py` | `census.py` |
|---|---|---|---|---|---|
| **F4** | `0425224756791b414454df28a9abf93dcdf154ce` | `e6c44d2d…532346` | `847aa33b…c853223` | `5e16e4af…f2da73` | `960c516d…c1fd5` |
| **F5** | `332f48849966073e2f165c13f952eb4c8e165e39` (current) | `c4056131…ad8e5c` | `c3ba6b93…38897c` | `5e16e4af…f2da73` | `960c516d…c1fd5` |

`census.json` at F5 is `573ec008…133e`; `SKILL.md` is `9bb902a1…86f5c`; block 23's pin
`sha256:c4056131…ad8e5c` equals the current `attest.py` (read-only check, not a claim of mine).

F5 (= `332f4884`, commit "close the two HIGH instrument defects wave 1 found") changed **only**
`gate.py` and `attest.py`, i.e. the frozen instrument was edited again after F4 and re-declared.
That is a fact about the lane, not something I caused; both byte sets were re-measured after it.

Baselines (receipts `R1`/`R2` at F4, `R13`/`R14` at F5; exit 0 in all four):

    attest.py   --selftest : F4 `cases=16 failures=0`   F5 `cases=18 failures=0`
    registry.py --selftest : F4 `cases=12 failures=0`   F5 `cases=12 failures=0`

## 1. Verdict

25 deletion probes (24 distinct — `M26` repeats `M20` under a second id) were built and run, each in
its own scratch copy of the whole `tools/round-46/` directory (so `import gate` and every fixture
behave exactly as shipped), with the lane as `--root`.

* **9 are dead weight.** Both selftests stay green at the same case count, and both counters still
  exit 0 with the same receipt values. Total removal: ~30 lines, all of it cosmetic. §2.
* **12 keep the selftests green but are not dead weight**: a recorded control receipt reads the
  field (§3.1–3.3), the claims' own `Before` evidence cannot be regenerated without the code
  (§3.2), the code is a named arm of block 23 (§3.4–3.7), or it is frozen bytes/provenance (§3.8).
* **3 are live and must not be deleted**: two registry clauses with their own red cases, and the
  `dirty` arm, which F5 wired and asserted (§4).
* **1 of the green deletions turns a red verdict into a clean one** (`-z`), reproduced on a
  tamper+restore fixture (§3.6). The shipped bytes are correct; the *arm has no isolating red case*,
  so a future edit can silently reopen R45-CL18. This is the finding worth the L1's attention.

Nothing is landable inside round 46: every candidate lives under `tools/round-46/`, frozen. §6 is the
round-47 action list.

### 1.1 The prompt's freeze commit no longer scores (blocking for the landing evidence)

The prompt declares freeze `31820472784284727546808acc31b3ea1e73919b`. Measured at the current HEAD:

    $ python3 -I -B tools/round-46/attest.py  --root . --freeze 3182047… --rev HEAD --no-battery   # R5
    exit 2  reason=frozen_path_changed
    frozen_path_changed = ["tools/round-46/", "tools/round-46/attest.py",
                           "tools/round-46/gate.py", "tools/round-46/registry.py"]
    $ python3 -I -B tools/round-46/registry.py --root . --freeze 3182047… --rev HEAD --no-battery  # R6
    exit 2  reason=frozen_path_changed

Five commits touch frozen paths: `50862e4a`, `65678df0`, `04252247`, `332f4884` (and `3182047`
itself is the base). The claims file's own re-derivation rule still returns the stale base:

    $ git log --format=%H -1 -- plans/round-46-claims.md
    31820472784284727546808acc31b3ea1e73919b

while the last commit touching the frozen set is `332f4884`. With freeze `332f4884`, both counters
score clean at the current HEAD (`c0112995`, `R9`/`R10`, exit 0 both, `met_target: true`; C1 rows 13,
refs 9, rule_blocks 23, battery 9/9/0/1/0; C2 scope 38, registered 38, thin [], absent []). So an
admissible score exists — but only against a freeze the claims file cannot derive, which is the same
"the scope is whatever the measured revision says" pathology the round is closing, one level up.

## 2. Deletions that are dead weight (measured green at both byte sets)

"Selftest after deletion" is `cases/failures` printed by each tool's own `--selftest`, run from the
mutated copy; "counters" is the mutated copy scoring the real lane at `--freeze 332f4884 --rev HEAD`
(`0/0` = both exit 0, `met_target` true, receipt values unchanged).

| id | file:line | removed | selftest after deletion | counters | why no clause needs it |
|---|---|---|---|---|---|
| M02 | `attest.py:266-272` | `_rows_lines()` | att `18/0`, reg `12/0` | 0/0 | AST sweep over all four modules: never loaded as a `Name`; no clause names it; selftest never calls it |
| M03 | `attest.py:69,78` | `SPECS[*]["vocab"]` | att `18/0`, reg `12/0` | 0/0 | key is never read — the vocabulary clause dispatches on `spec["routed"]`; `vocab` is a leftover mirror of `ARMS` |
| M15 | `attest.py:310` | second return value of `_table_indexes_lines` (caller uses `[0]`) | att `18/0`, reg `12/0` | 0/0 | the `data` half is dead at its only call site |
| M05 | `registry.py:445-447` | `SCOPE6` | att `18/0`, reg `12/0` | 0/0 | round-45 fixture constant, never referenced |
| M06 | `registry.py:319-324` + loop | the `"skill"` element of every `MUTATIONS` tuple and the `_,` unpack | att `18/0`, reg `12/0` | 0/0 | `run_battery` dispatches on `name` and never reads element 1 |
| M07 | `registry.py:253-254` | inner `def fix(m)` in `m_substring_cell` | att `18/0`, reg `12/0` | 0/0 | nested function never called; the rewrite is done by the `lambda` two lines below |
| M08 | `registry.py:236` | `head = mid.splitlines()[0] …` in `m_fenced` | att `18/0`, reg `12/0` | 0/0 | assigned, never used |
| M25 | `registry.py:54` | `SPECS["r45"]["house"]` | att `18/0`, reg `12/0` | 0/0 | `house` is read only when `strict_header` is true; `r45.strict_header` is false in every reachable combination |
| M11 | `census.py:20` | `import subprocess` | att `18/0`, reg `12/0` | 0/0 | unused import (AST) |

Removal budget if all nine land: 30 lines removed, 8 added, four files touched.

## 3. Selftest-green deletions that are **not** dead weight

Each row below deletes code that no clause of `plans/round-46-claims.md` reads, and both selftests stay
green — which is exactly why the seat asks for them to be examined and not just counted. The
discriminator in every case is a **second consumer**: a recorded control receipt, a block-23 arm, or
the frozen bytes themselves.

### 3.1 Receipt fields are the recorded controls' payload (M04, M09)

`attest.py:183,197,224,239,249` (`block_title`, `header_ok`, `cited`, `cites`, `pin_expected`) and
`registry.py:167` (`registry_rows`) are written, never read by a clause, and deleting them keeps both
selftests at `18/0` and `12/0`. But they are what `.ufo/waves/round-46/controls/ctl-c1-fidelity.json`
and `ctl-c2-fidelity.json` contain. Regenerating the fidelity command at the same revs reproduces the
recorded file **key-for-key and value-for-value** (0 keys only-new, 0 keys only-old, 0 value diffs;
`R7`). Deleting these fields would make every regenerated control a strict subset of the recorded one —
the fidelity comparison would quietly stop being a comparison. **Keep.**

### 3.2 `SPECS["r45"]` is a second claim's instrument (M13)

Deleting the `r45` spec (`attest.py:72-81`) keeps both selftests green and both counters at 0/0, so the
selftest screen calls it dead. It is not:

    base:  --spec r45 --profile v1 --freeze f762b727 --rev f59565b7
           exit 0, met_target true, rule_blocks 22, block_present 1, rows 10, refs 8, unresolved []
    M13:   argparse: invalid choice: 'r45' (choose from 'r46')   exit 2

The claims' `Before` section cites exactly those numbers as `controls/ctl-c1-fidelity.json`. Removing
the spec removes the ability to produce the control. **Keep**, and note the general rule for this
round: *selftest-green is necessary, not sufficient, evidence of deadness.*

### 3.3 F5's receipt fields are dropped by both counters (M23, M24; also `blob_changed`)

`gate.py:179-185` now computes `frozen_from`, `blob_changed` and `dirty` into the `freeze_state`
receipt. Neither counter propagates them: `evaluate()` rebuilds its `update({...})` from a fixed
five-key list (`freeze`, `frozen_derived`, `frozen_path_changed`, `touched` (count), `restored`).
Measured: deleting `frozen_from` (M23) or the `"dirty"` receipt entry (M24) keeps `18/0` + `12/0`, the
counters exit 0, and the emitted receipt is key-identical to the base receipt apart from the `battery`
block. So in the **official counting command's output** these fields do not exist.

They are not free to delete, though: wave-1 peer control receipts read them directly from `gate`
(`.ufo/waves/round-46/w1/R46W1CritDenominator/tamper-f5.json` and
`…/R46W1RevScratch/pending-dirty-arm-scope.json` both carry `frozen_from`, `dirty`, `blob_changed`).
The cheap fix is to *surface* them (`evaluate`'s update dict gains the three keys) rather than delete
them, so the official receipt and the reviewer's hand-assembled receipt stop disagreeing. Either way it
is a round-47 edit: recomputing them and dropping them is the only thing that is certainly wrong.

### 3.4 `gate.out_path` — load-bearing guard with no red case (M12)

Deleting `GRADED` and `out_path()` (`gate.py:35,198-212`) plus the two `main` guards keeps both
selftests green and the counters at 0/0 — no case exercises a refused `--json-out`. The guard is not
decoration; with it deleted, the same command overwrites the graded surface in a fixture lane:

    base/F4/F5 bytes : exit 2, "--json-out inside a graded or frozen surface: SKILL.md",
                       canary SKILL.md survives
    M12 copy         : exit 2 (evaluation refused), canary SKILL.md REPLACED by the receipt JSON

This is R45-CL22 reproduced by deleting code no clause needs. **Keep**, and give it the red case the
row already promises.

### 3.5 `gate.TEMP_PARTITIONS` — named arm, no case (M17)

Deleting the `/tmp`/`/var/tmp` refusal (`gate.py:219`) keeps `18/0` + `12/0`; no case sets a temporary
root (the selftests always run under `HYAKU_SCRATCH`). Block 23 row R45-CL20 says `scratch()` refuses a
temporary partition and returns could-not-evaluate; nothing exercises that. **Keep as an arm**, add a
case (set `HYAKU_SCRATCH=/tmp`, expect exit 2).

### 3.6 `-z` in the history arm — deletion makes a tamper+restore score **clean** (M19)

Deleting `-z` from `gate.history_touched` (`gate.py:99`) keeps both selftests green (`18/0`, `12/0`)
and the counters at 0/0 on the shipped artefact. On a fixture that tampers a frozen tool and restores
it in the next commit — the exact defect R45-CL18 names and block 23 row 8 claims closed — the two
instruments disagree:

    base gate (c3ba6b93):  exit 2  touched=[tools/round-46/tool.py]
                                   blob_changed=[]  restored=[tools/round-46/tool.py]
    M19  gate (3920682e):  exit 0  CLEAN   touched=[]  blob_changed=[]  restored=[]

The existing case `red-frozen-touched-is-exit-2` does not catch it because it edits the claims file
*without* restoring: the **blob** arm refuses that one, so the history arm is never the reason a case
is red. The shipped bytes are correct (measured green-for-red above); what is missing is an isolating
case — tamper **and** restore — which is also the only fixture in which the `merge` arm (M18,
`--diff-merges=first-parent`) matters. On an evil-merge fixture, base names the path
(`touched=[tool.py]`, `restored=[tool.py]`) and M18 loses it (`touched=[]`) while the blob arm still
exits 2 — arm detail unasserted, verdict safe. **Keep both flags; add the tamper+restore case.**

### 3.7 `MALFORMED` reason branch (M20/M26)

Deleting `attest.py:91-92` keeps `18/0` + `12/0` and the counters at 0/0: the malformed-heading case
asserts exit 2 only, and without the branch the generic "no `## Queue-drain craft ` section" still
exits 2. The claims' kill rule names the distinction ("clause: malformed"), so this is a named clause
with a weaker case than the prose. **Keep**; assert the reason string if the row is to stay.

### 3.8 `census.py` — `per_claims_file` and the `WORKTREE` adapter (M10, M16)

* `per_claims_file` (`census.py:40,57,73`): no clause reads it — `registry.load_scope` reads `paths`
  only — and deleting it keeps `18/0` + `12/0`. But `census.json` is a **frozen path**, so the deletion
  is only executable together with a re-freeze, and regenerating would rewrite frozen bytes. It is also
  the artefact's only provenance (which claim file named which tool). **Keep; round-47 candidate at
  most** — and then decide provenance vs. minimalism on the record, not by accident.
* the `--rev WORKTREE` branch (`census.py:38-41`): unused by any clause (the counting command passes a
  committed rev); deleting it keeps both selftests green. It is the only second read path in the
  census. **Removable**, but it is a pre-commit convenience, not dead weight in the "cannot change a
  verdict" sense — it can only change how the census is produced, not what it means.

## 4. Live arms (deletions that turn a red case green — do not delete)

| id | code | selftest after deletion | verdict |
|---|---|---|---|
| M21 | `registry.py:190-192` presence (`absent_at_rev`) | reg `12/1`, att `18/0` | live — `red-absent-at-rev` is the red case |
| M22 | `registry.py:180-184` exact cell 0 (`strict_cell`) | reg `12/1`, att `18/0` | live — `red-substring-cell` is the red case |
| M01 | `gate.py:132-140` `dirty()` | F5: att `18/18`, reg `12/12` (every case crashes) | live at F5 |

M01 is the one result that **changed between the byte sets**: at F4 the function had no caller anywhere
in the lane (AST sweep, and the counter scored a dirty frozen path clean — exit 0), so it was dead
weight *and* block 23 row R45-CL15's "the dirty scope is the union of the pathspecs" was not
implemented. F5 wired it into `freeze_state` and added `red-dirty-frozen-tool-is-exit-2`; at F5 a dirty
frozen path is exit 2 `frozen_worktree_dirty`. Recorded at both byte sets:

    F4 gate 847aa33: dirty tools/round-46/attest.py → freeze_state exit 0 (clean)
    F5 gate c3ba6b9: dirty tools/round-46/attest.py → freeze_state exit 2

## 5. Cross-cutting findings for the L1 (all measured, none fixed by me)

**5.1 Three control receipts the claims name do not exist.** `plans/round-46-claims.md` cites
`controls/ctl-c1-1-v1-profile.json` (C1 `Before`), `controls/ctl-c2-1-v1-profile.json` and
`controls/ctl-c2-2-ghost-tool.json` (C2 `Before`). The directory holds `ctl-c1-0-do-nothing.json`,
`ctl-c1-fidelity.json`, `ctl-c2-0-do-nothing.json`, `ctl-c2-1-v1-scope.json`, `ctl-c2-fidelity.json`.
The `-1-v1-scope` file is a different artefact (`counter: round-45-c2`, scope 6), so the two "the v1
clause set accepts every forgery" controls and the ghost-tool control are absent from the record.
I produced the missing measurement at the landed artefact instead (not at the freeze — at the freeze
block 23 does not exist, and `run_battery` would exit 2 "cannot build a battery"):

    R11 attest --profile v1  : exit 0, met_target true, battery 9/9 v1-green, v2_green 0
    R12 registry --profile v1: exit 0, met_target true, battery 7/7 v1-green, v2_green 0

That is the round-45 hole demonstrated on the round-46 artefact: the v1 clause set still calls a
perfectly forged battery green. It belongs in `controls/` under the names the claims use.

**5.2 The satisfiability-preflight numbers are wrong.** The claims say "`attest.py --selftest` prints
`cases=15 failures=0` … and `registry.py --selftest` prints `cases=11 failures=0`". Measured by
extracting each freeze candidate's own files and running its selftest (receipt `R8` plus the
`rev` runs):

| rev | attest cases | registry cases |
|---|---|---|
| `3182047` (declared freeze) | 15 | **12** |
| `50862e4a` | 15 | **12** |
| `65678df0` | 16 | **12** |
| `04252247` | 16 | **12** |
| `332f4884` (current) | **18** | **12** |

`registry.py` has printed `cases=12` at every rev, including the declared freeze — the "11" was never
true. `attest.py` has printed 15, 16 and now 18. Neither number is a predicate clause, so the claim
still scores; but the preflight sentence is evidence that is false at its own freeze, which is the
class this round exists to punish.

**5.3 Clause 4 grades the arm *token*, not the arm's wiring.** §3.4–3.6 are the proof: four block-23
rows name arms whose code can be deleted with both selftests green, and one of those deletions (M19)
produces the R45-CL18 false-clean. The battery (`forgeries_total == 9`) mutates only the *artefact*
(rows, refs, marker, pin); no forgery touches `gate.py`. So the instrument's own discrimination story
is: clause-level red cases exist for the artefact, and the shared freeze core is covered by exactly two
cases (`red-frozen-touched-is-exit-2`, plus F5's shrink/dirty pair). A row-per-arm case, or an amended
row that says "arm named, arm not isolated", would close the gap honestly.

**5.4 The artefact pin cannot see the re-freeze it is pinned across.** A4 re-pinned block 23 to the F5
interpreter in the same breath as F5 changed the interpreter, and clause 6 checks the pin against
`--rev`. So the pin proves "the row and the bytes agree now", never "the bytes are the frozen ones".
That is the stated `R45-CL19` limit (squash) in a different costume, and the freeze-integrity arm is
what is meant to cover it — which is why §1.1 matters.

## 6. Action list — round 47 or a declared re-freeze only (nothing is landable now)

1. Delete the nine dead items in §2 (`_rows_lines`; two `vocab` keys; `_table_indexes_lines`' second
   return; `SCOPE6`; `MUTATIONS`' second element; `m_substring_cell`'s inner `fix`; `m_fenced`'s
   `head`; `r45.house`; `import subprocess`). Expected after deletion: att `18/0`, reg `12/0`,
   counters 0/0 — already measured in scratch for all nine.
2. Add the tamper+restore case (`-z` arm) and the `/tmp`-root case (`TEMP_PARTITIONS`), and a refused
   `--json-out` case (`out_path`). Each has a measured fixture in §3.4–3.6.
3. Surface `frozen_from`/`dirty`/`blob_changed` in both counters' receipts (or delete them and accept
   that peer reviews must re-derive). Decide once; the current split is the worst option.
4. Re-declare the freeze with a commit that can be re-derived (`git log -1 -- frozen paths` must equal
   the declared base), and regenerate every control receipt the claims name, including the three
   missing ones, with the numbers §5.2 measures.
5. Do **not** delete: `SPECS["r45"]`, the receipt fields in §3.1, `MALFORMED`, `out_path`/`GRADED`,
   `TEMP_PARTITIONS`, the merge/`-z` flags, `census.per_claims_file`.

## 7. Evidence and contract compliance

Receipts are in `receipts/` beside this file: `runs.jsonl` (command, exit, stdout sha256, UTC, rev),
one `R*.txt`/`R*.json` per run, the three probe harnesses' full output (`muts.out`, `muts2.out`,
`muts3.out`, `muts4.out`), the demo outputs (`demo_out.json`, `demo2_out.json`, `demo3_out.json`,
`demo_m12.json`), and `R15-provenance.txt` (HEAD, re-derived freeze, frozen-touch commits, core-path
`git status --porcelain` empty, sha256 of `SKILL.md` and the four tools).

Key receipts cited above:

| id | what | exit | stdout sha256 | UTC |
|---|---|---|---|---|
| R1 | attest `--selftest` (F4) | 0 | `0bf8f4c6…296dd8` | 2026-10-28T17:08:39Z |
| R2 | registry `--selftest` (F4) | 0 | `0fa8c31a…d11872e` | 2026-10-28T17:08:42Z |
| R5 | attest @ freeze `3182047` | 2 | `04c96d85…76db9b12` | 2026-10-28T17:08:48Z |
| R6 | registry @ freeze `3182047` | 2 | `5b2eacb4…327cc6d9` | 2026-10-28T17:08:48Z |
| R7 | attest `--spec r45 --profile v1` fidelity | 0 | `41933911…a47d6fc` | 2026-10-28T17:08:48Z |
| R9 | attest v2 @ freeze `332f4884` (rev `c0112995`) | 0 | `16d4cb5c…a5aabedd` | 2026-10-28T17:12:17Z |
| R10 | registry v2 @ freeze `332f4884` | 0 | `4206266f…3a20e38d` | 2026-10-28T17:12:18Z |
| R11 | attest `--profile v1` at landed artefact | 0 | `99d4e40d…d6e0c04a` | 2026-10-28T17:11:45Z |
| R12 | registry `--profile v1` at landed artefact | 0 | `d0f33fa6…c13a67c99` | 2026-10-28T17:11:46Z |
| R13 | attest `--selftest` (F5) | 0 | `6aa73c61…9f46dfa6` | 2026-10-28T17:15:39Z |
| R14 | registry `--selftest` (F5) | 0 | `0fa8c31a…d11872e` | 2026-10-28T17:15:40Z |

Harness outputs (sha256, in `receipts/probe-output-sha256.txt`): `muts.out` `b0df2a75…`,
`muts2.out` `12833118…`, `muts3.out` `a7658a6a…`, `muts4.out` `302cbbad…`, `demo_out.json`
`86a85326…`, `demo2_out.json` `90980cf8…`, `demo3_out.json` `563f8662…`, `demo_m12.json`
`3954eb65…`.

Compliance: the lane's `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md` were never
written (core-path `git status --porcelain` empty in `R15`); every mutation ran from a copy under the
scratch root; every fixture repo asserted `git rev-parse --show-toplevel` equals its own directory
before its first commit; no `/tmp` path was written or cited; no package was installed, so there is no
install to record; the scratch tree was removed after the receipts above were copied here.
