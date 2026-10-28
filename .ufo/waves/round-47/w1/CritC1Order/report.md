# CritC1Order — R47-C1 clause 7 (`order`) is a source-text lint, not a check on the arm

Seat `CritC1Order`, wave `round-47/w1`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Read-only on the lane; all writes are this file plus `.ufo/waves/round-47/w1/CritC1Order/receipts/`.
Scratch `/fast/scratch/hyaku/kaidoku-r47/CritC1Order` (removed at yield, receipts copied here).
No installs, no pacman, no git/jj mutation outside throwaway fixtures.

**Verdict (one line): predicate too weak — clause 7 can be satisfied with `history_touched` returning
`[]`, and the full counter then exits 0 `failing: []` on a range that added and deleted a frozen path
inside merge commits; what closes it is an oracle pair over `freeze_state` (genuine ⇒ exit 2, flags
dropped ⇒ exit 0) plus an argv capture, not a better substring count.**

## 1. Objects measured, and their bytes

| object | bytes at the first freeze `5017e1f7` | bytes at measurement |
|---|---|---|
| `tools/round-46/gate.py` | `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` | same (`c3ba6b93…`, HEAD and worktree) |
| `tools/round-47/exact.py` | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` | `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5` (A6) |
| clause-7 lines of `exact.py` (`38-39`, `256-265`) | `5441b10834908fc1178f458f90f04ceb7733a459e7b2d15aeb0a1db7af408393` | **identical** (`diff` empty; `clause7-at-freeze.txt` / `clause7-at-HEAD.txt`) |

The freeze series is now `5017e1f7 → A1 9018c53b → A2 62e33f7d → A3 2e4ae43 → A4 1e2c310 → A5 07d2894e
→ A6 f54b3b6d`; the landing is `a0753786` (block 24) and `31b092d1` (A7 measurement). My seat's prompt
named `5017e1f7` as the freeze; A6 (`f54b3b6d`) is the declared one in `corpus/lessons/round-47.md:3-5`.
The clause-7 bytes are the same in all seven, so every receipt below applies at every member of the
series; `01a4bca7` is the `exact.py` the last receipts executed.

## 2. What the clause actually binds

`plans/round-47-claims.md:101-103`, computed at `tools/round-47/exact.py:256-264`:

```python
gtext = files(GATE46)                      # gate.py bytes at --rev, as text
n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)
if n_ok != 1 or n_bad != 0:
    failing.append(f"gate.py flag order: {n_ok} correct, {n_bad} reversed")
```

with `ORDER = '"-m", "--diff-merges=first-parent"'` and
`REVERSED = '"--diff-merges=first-parent", "-m"'` (`exact.py:38-39`).

**It protects exactly this:** the two quoted tokens appear once, comma-adjacent and in that order,
inside `tools/round-46/gate.py` at `--rev`, and nowhere in the file in the reverse adjacency. That is a
two-substring lint over one committed file.

**It does not protect, each measured below:**

| not protected | forgery | clause 7 | arm |
|---|---|---|---|
| the executed call (the literal may sit in a comment) | F1 | green | dead |
| the rest of the argv (`--format=`, `--name-status`) | F2 | green | dead |
| that `freeze_state` calls `history_touched` at all | F3 | green | dead |
| runtime argv construction (`git()` rewrites args) | F4 | green | reordered |
| a second, decoy history arm that is the one called | F5 | green | dead |
| the module that is *executed* being the module scored | §5 R4 | green | forged at rev |
| the **order** meaning what the claim says it means | §4 | red only on text | both orders detect |

## 3. Counterexamples — fixture, command, exit

All fixtures are throwaway repos with `git -C "$D" init -q`, identity configured per fixture, and
`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D` before the first commit. The scored
block is `exact.good_block()` inside `exact.skill_text()` (the counter's own selftest artefact), so
clauses 1–6, 8 are green in every case and clause 7 is the only variable. Driver:
`receipts/e2e_clause7.py`; receipt: `receipts/e2e_clause7.out.json`.

| # | forgery (gate.py edit; block bytes unchanged) | `count(ORDER)` | `count(REVERSED)` | `score()` exit | `freeze_state` on a merge-only tamper |
|---|---|---|---|---|---|
| gen | none (`c3ba6b93…`) | 1 | 0 | **0** | **exit 2**, `frozen_path_changed ["tools/round-47/decoy.txt"]` |
| F1 | literal moved to a comment; call is `git log --name-status -z --format= …` | 1 | 0 | **0** `failing []` | **exit 0**, `touched []` |
| F2 | call keeps the literal, loses `"--format="` | 1 | 0 | **0** `failing []` | **exit 0**, `touched []` |
| F3 | `freeze_state`: `touched, err = [], None` (call removed) | 1 | 0 | **0** `failing []` | **exit 0**, `touched []` |
| F4 | `git()` reorders `-m` before `--diff-merges=…` at runtime; call text untouched | 1 | 0 | **0** `failing []` | arm runs, order inverted |
| F5 | new `history_touched_quiet` (no flags, returns `[]`), `freeze_state` calls it; canonical function untouched | 1 | 0 | **0** `failing []` | **exit 0**, `touched []` |
| C0 | control: the literal replaced by the reversed pair (the one thing the clause reads) | 0 | 1 | **1** `["gate.py flag order: 0 correct, 1 reversed"]` | — |

The tamper fixture is the R45-CL6 shape: `base..tip` adds `tools/round-47/decoy.txt` **inside** a
merge commit and deletes it **inside** a second merge commit, so `git diff base tip` is empty, no
ordinary commit touches the path, and only the merge-diff arm can see it. The genuine gate reports
`frozen_path_changed: ["tools/round-47/decoy.txt"]`; every blind forgery reports the range clean.

```
$ python3 e2e_clause7.py        # cwd=/fast/scratch/hyaku/kaidoku-r47/CritC1Order
exit 0 · stdout sha256 f6276447de700311ac1cd880f5e7255bbd8ad589b6e4c15bfd27913a5187f99a
```

## 4. Full counter, end to end: exit 0 on a tampered range

`receipts/cli_probe.py` → `receipts/cli_probe.out.json`. Four fixture repos, identical except for
`tools/round-46/gate.py` and the merge-only decoy; the command is the claim's own counting command,
`python3 -I -B tools/round-47/exact.py --root <fixture> --freeze <F> --rev <R>`, run with `cwd` = the
fixture and `HYAKU_SCRATCH` set.

| case | gate.py | tamper | exit | stdout sha256 | receipt fields |
|---|---|---|---|---|---|
| R1 | genuine at freeze and rev | merge-only add+delete of `tools/round-47/decoy.txt` | **2** | `803bf25c45e3bc93…` | `frozen_path_changed ["tools/round-47/decoy.txt"]` |
| R2 | F2 forged at freeze and rev | same | **0** | `f01ab017d023c03b…` | `failing []`, `gate_order_literal 1`, `gate_order_reversed 0`, `frozen_path_changed []`, battery `4/4/0/1/0` |
| R3 | F2 forged | none | **0** | `36468473d6c8feca…` | `failing []` |
| R4 | **genuine at freeze, F2 forged at rev only** | same | **0** | `d25fc7c083dd165e…` | `failing []`, `frozen_path_changed []` |

Per-case hashes differ between runs only because each fixture's path and commit ids are fresh; the
last full run's own stdout sha256 is `a840207eb28c317024a74eb228c558028c65062a017f4a51ecc6983f20b21c67`
(2026-10-28T18:02:21Z), and every case's exit is stable across the three runs of this driver.

R4 is the composition that matters: `tools/round-46/gate.py` is **not** in round 47's frozen set
(`plans/round-47-claims.md:203-206` names only the claims file and `tools/round-47/`), so a landing
commit may rewrite the instrument that performs the freeze check, clause 7 blesses the rewritten bytes
(1/0), and the rewritten `freeze_state` certifies a frozen surface that was tampered with inside merges
as clean. The counter prints `failing: []` and exits 0. This is `R47-CL1`'s class (graded bytes ≠
executed bytes) reached from the other side: the landed revision's instrument is what runs.

## 5. Behavioural matrix: what the *order* does, and what the clause's neighbours do

`receipts/merge_probe.py` → `receipts/merge_probe.out.json`; git 2.56.0; parser is a replica of
`gate.history_touched`'s token walk and the genuine function's output is shown beside it.

Fixture A — ordinary merge, both parents edited the frozen path, resolution differs from both
(net `M frozen/x.txt`):

| argv | raw bytes | parsed touched (before set dedupe) |
|---|---|---|
| `-m --diff-merges=first-parent --name-status -z --format=` (canonical) | 45 | 3 × `frozen/x.txt` |
| `--diff-merges=first-parent -m --name-status -z --format=` (reversed) | 60 | 4 × `frozen/x.txt` |
| `-m` only | 60 | 4 × `frozen/x.txt` |
| `--diff-merges=first-parent` only | 45 | 3 × `frozen/x.txt` |
| neither | 30 | 2 × `frozen/x.txt` |
| pair split by `--name-status` | 45 | 3 × `frozen/x.txt` |
| no `--format=` | 498 | **[]** |
| no `--name-status` | 149 | **[]** |
| `--format=` first | 45 | 3 × `frozen/x.txt` |
| `gate.history_touched` (genuine) | — | `["frozen/x.txt"]` |

Fixture B — the merge-only add/delete tamper, net tree clean, no ordinary commit touches the path:

| argv | raw bytes | parsed touched (deduped) |
|---|---|---|
| canonical | 38 | `frozen/novel.txt` |
| **reversed** | 76 | `frozen/novel.txt` |
| `-m` only | 76 | `frozen/novel.txt` |
| `--diff-merges=first-parent` only | 38 | `frozen/novel.txt` |
| neither | 0 | **[]** |
| pair split | 38 | `frozen/novel.txt` |
| no `--format=` | 412 | **[]** |
| no `--name-status` | 306 | **[]** |

Three results, none of which the clause reads:

1. **The reversed order does not blind the arm.** Both orders, and either flag alone, find the
   merge-only tamper; only dropping both flags, or breaking the output format/status, empties the
   parse. "Reversed ⇒ blind" is false (it is what `corpus/lessons/round-46.md:66-70` and the landed
   row assert); the drafting seat reached the same conclusion from a different fixture
   (`.ufo/waves/round-47/w1/C1Order.md` §4 F2, case D: reversed *over-reports*, exit 2 on a path the
   merge never touched). So the order is verdict-relevant only in the **false-positive** direction;
   no measured order weakness can hide a tamper.
2. **The load-bearing tokens are the ones the clause does not name.** `--format=` and
   `--name-status` decide whether the arm parses anything at all; the clause is indifferent to both
   and to where `--format=` sits.
3. **The adjacency test is stricter than the behaviour it claims to protect** (`-m` alone and
   `--diff-merges` alone both work), so it rejects a text variant (`fixture gate.py` reversed) that
   still detects, and accepts text variants that do not detect.

## 6. Reconciliation with the drafting seat (`C1Order.md`)

Additive, not a restatement. `C1Order` correctly established: the literal is already `1/0` at the
freeze (its F4), a comment+reversed live argv scores green (its F1), the "blinds the arm" prose is
false and the effect is over-report (its F2), and `gate.py`'s bytes are unpinned (its F4). What its
report does not contain, and what changes the disposition:

- Its F1 forgery leaves the arm **working** (the live argv is reversed; the parse still finds the
  tamper). The class that matters is the arm **stopped**: F2/F3/F5 above return `[]` and score
  `failing: []`, and R2/R4 show the whole counter green while a frozen path is tampered inside
  merges. "False touch" is a wrong answer; `[]` is no answer, and only the latter makes the freeze
  check vacuous.
- Its repair shape — "count the two tokens on the live `git(` call line, or pin `gate.py`'s sha256" —
  is defeated by F4 (the call line is untouched, `git()` rewrites argv), by F5 (a decoy call line is
  the one executed), and by any pin taken without asserting that the pinned bytes are the loaded
  module (R4).
- Its F2 conclusion "the order is load-bearing on the verdict (good: the clause pins something real)"
  is too generous. Pinning the order prevents an over-report, which is a record-accuracy property;
  it does not make the arm's *silence* detectable, which is what the routed defect (R46-CL6) was
  about. The row's `exit 1` cell therefore measures a source-text change, not a failed defence.
- Its F5 (selftest flag unreachable) and F3 (citation path set) are unaffected by this seat; not
  re-run here.

## 7. The landed row's causal claim is false (landing edit, pin unaffected)

`SKILL.md:639` (HEAD `a0753786`): "one flag reorder (`--diff-merges=first-parent -m`) prints a merge
twice and blinds the arm". Measured: prints the merge diff once per parent — true (38 → 76 bytes);
blinds the arm — **false** (fixture B: both orders find `frozen/novel.txt`; the drafting seat's case D
shows the reversed order instead *over-reports*). The block's pins cover `exact.py`, not `SKILL.md`,
so correcting the row is a landing edit that only requires the counter to be re-run
(`c1-at-A7` would remain exit 0).

## 8. Impacted axes

- **depth** (claim R47-C1) — the `order` row's arm is the one this seat attacked: the row's `exit 1`
  is produced by a substring count, and the counter is green while the arm it names is silent. No
  other axis is touched: no knowledge entry, coverage row or province row is involved.
- Adjacent, not claimed: `R47-CL1` (executed ≠ graded bytes) gains a concrete end-to-end receipt (R4).

## 9. Smallest safe correction

`exact.py` is frozen at `01a4bca7…`/A6 and the round's `c1-at-A7` receipt is green; I did not touch
frozen bytes. Two routes, in order of preference:

**A. Route it (no frozen edit), and stop claiming the arm.** Record as a round-48 defect
(`R47-CL9`): "a clause whose green survives `history_touched → []` is a lint, not a check; the
`order` row's `exit 1` measures a source substring". Correct `SKILL.md:639`'s "blinds the arm" to the
measured effect ("prints the merge diff once per parent; a wrong order can attribute a side-branch
change to the merge — over-report, not blindness"), and state in the round report that the `order`
arm is a *textual* binding whose behavioural defence is routed, not measured. This is the
"predicate holds for clauses 1–6, too weak for clause 7" outcome and needs no re-freeze.

**B. If an amendment is still permissible before the final reported measurement**, add one battery
case that fails every forgery above, and nothing else. The replacement predicate is an **oracle
pair**, not a count:

```
# fixture: base..tip adds frozen/decoy.txt inside merge1 and deletes it inside merge2;
# net tree diff empty; no ordinary commit touches the path (receipts/merge_probe.py fixture_b)
want = gate.freeze_state(d, freeze, rev, CLAIMS)          # must be 2, naming frozen/decoy.txt
blind = gate_text.replace('"--name-status", "-z",\n            "--format=",',
                          '"--name-status", "-z",')       # literal kept, arm silent
got  = freeze_state_of(blind_module, d, freeze, rev)      # must be 0, touched []
pass iff want[0] == 2 and decoy in want[3] and got[0] == 0
```

plus three cheap structural assertions that a count cannot express:

1. **argv capture** — monkeypatch `gate.git` (or `subprocess.run`) and call
   `gate.history_touched(d, base, tip, ["frozen/"])`; assert the observed argv prefix equals
   `["log", "-m", "--diff-merges=first-parent", "--name-status", "-z", "--format="]`. Catches F4 and
   any flag the clause does not name.
2. **call graph** — AST-assert that `freeze_state` contains a call to `history_touched`, and that no
   other module under `tools/` defines a second merge-history arm. Catches F3 and F5.
3. **the measured module is the executed module** — resolve the imported `gate` module's `__file__`,
   sha256 it, and compare with `gate.show(root, rev, GATE46)`; mismatch is exit 2. Catches R4.

If B is chosen, the clause-7 text can stay (it is necessary but not sufficient); the battery case is
what makes the row's `exit 1` mean the arm failed.

## 10. Not run, and limits

- Not run: `tools/round-47/record.py` (R47-C2) — another seat's surface.
- Not run: the counter against the **landed** block 24; my fixtures use the counter's own
  `good_block()`/`skill_text()`, so the clause-7 verdict is isolated from every other clause. The
  landed artifact is scored by `c1-at-A7.json` (`failing []`, `gate_order_literal 1`), which I read,
  not re-ran.
- Not constructed: a merge edit that **first-parent mode misses and separate mode sees** inside
  `base..tip`. In every range where a path changes only in a merge, the change must conflict, so a
  parent commit in the range changes it too; the measured fixtures agree with that reasoning, but the
  negative is a finite measurement, not a proof.
- The probe's "raw bytes" counts include duplicate entries the genuine parser dedupes; that is stated
  in the table because the landed row's "prints a merge twice" is exactly a raw-multiplicity claim.

## 11. Receipts

`UT` = UTC start of the run. Stdout hashes are of the probe's JSON on stdout; the full receipts are
`receipts/*.out.json` and `receipts/receipts.jsonl`.

| # | command | exit | stdout sha256 | UT |
|---|---|---|---|---|
| 1 | `python3 merge_probe.py` (cwd `/fast/scratch/hyaku/kaidoku-r47/CritC1Order`) | 0 | `af650b3d409d7c6792d2fb9b933a1328722cd8e469af30b482922315ef1b9040` | 2026-10-28T17:59:40Z |
| 2 | `python3 e2e_clause7.py` (same cwd) | 0 | `f6276447de700311ac1cd880f5e7255bbd8ad589b6e4c15bfd27913a5187f99a` | 2026-10-28T17:59:40Z |
| 3 | `python3 cli_probe.py` (3 cases, before R4) | 0 | `0b64291b48ba9c0b6aa1f8f442325dbe1492ae84837e866c710c3884c90a7bcf` | 2026-10-28T17:59:40Z |
| 4 | `python3 cli_probe.py` (4 cases, final) | 0 | `a840207eb28c317024a74eb228c558028c65062a017f4a51ecc6983f20b21c67` | 2026-10-28T18:02:21Z |
| 5 | `git show 5017e1f7:tools/round-47/exact.py \| sed -n '38,39p;256,265p'` vs worktree | 0 | `5441b108…` both sides (`clause7-at-freeze.txt`, `clause7-at-HEAD.txt`) | 2026-10-28T18:03Z |
| 6 | `git show HEAD:tools/round-46/gate.py \| sha256sum` | 0 | `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` | `receipts/frozen-bytes.txt` |

Every fixture ran as a one-commit-per-step repo under `HYAKU_SCRATCH`, toplevel asserted, and was
removed with the scratch root. Installs: none.
