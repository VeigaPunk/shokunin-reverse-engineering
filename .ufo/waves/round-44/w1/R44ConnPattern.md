# R44ConnPattern — cross-axis pattern finder, round 44 wave 1

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (base `c29360e3`, HEAD `fc5eb54a` draft claims).
Scratch: `/fast/scratch/hyaku/kaidoku-r44/probe-ConnPattern/` (repos under `cases/`; no lane git mutation).
Probe tool: `.ufo/waves/round-44/w1/artifacts/R44ConnPattern/freeze_walk_probe.py`.
Receipt: `.ufo/waves/round-44/w1/R44ConnPattern/freeze-walk-probe.receipt.json`
(command `python3 -I -B …/freeze_walk_probe.py`, exit 0, stdout sha256 `2be6014cac7d…` (prefix), wall time recorded in receipt).

## Axes

1. **Freeze-walk correctness** — does the walk report every commit in `FREEZE..REV` that changes a frozen path, per the draft freeze rule (merge diffs included; M/D/R/T/U and A-of-a-frozen-blob are changes; a later restore does not un-block; tree-level blob backstop).
2. **Single source of truth** — one walk implementation, not four drifting copies.
3. **Receipt identity** — `counter_sha256` must cover every byte the verdict depends on.
4. **Diff size / separability** — C1 and C2 landings must stay independent (draft §Separability).

## Finding 1 — the freeze walk is NOT identical across counters (four variants in the lane)

AST comparison of `frozen_drift` (`ast.dump` hashes, from `tools/round-4{1,2,3}/*counter.py`):

| counter | `frozen_drift` | merge-aware (`-m --diff-merges=first-parent`) | status filter | tree blob backstop |
|---|---|---|---|---|
| round-42 `c1-counter.py` (the draft's **named port source**) | 21 L, `530e1a28` | no (`git log --name-only`) | none (A counted always) | no |
| round-43 `c1-counter.py` | 44 L, `37b53874` (+`kind_at`, `commits_touching`) | yes | M/D/R/T/U, A iff frozen path was a blob | yes |
| round-42 `c2-counter.py` | 28 L, `73783a4a` | no | M/D/R/T/U (A excluded) | no |
| round-41 `c2-counter.py` | 31 L, `98dc47cd` | no | M/D/R/T/U | no |

Only round-43 C1 satisfies the draft's freeze rule as written. Its own docstring says so: "plain `git log` suppresses merge diffs entirely".

**Probe (control, scored before any round-44 data).** Four scratch scenarios, each run through the round-42 walk, the round-43 walk, and the round-43 walk with `--full-history`:

| scenario | r42 walk | r43 walk | r43 + `--full-history` | endpoint bytes differ |
|---|---|---|---|---|
| linear edit then restore | touched | touched | touched | no |
| merge commit itself edits the frozen file (conflict-free side merge + edit) | **NOT touched** | touched | touched | yes |
| side branch edits then restores, merged | touched | touched | touched | no |
| delete then re-add | touched | touched | touched | no |

Result: the round-42 walk misses the merge-commit edit. Because round-42 has no tree backstop, nothing else catches it at the endpoint level, so the **do-nothing port of round-42 would let a frozen-byte change pass**. The round-43 walk plus backstop catches it. This is the do-nothing control and it is red, which is the reason to port round-43's walk, not round-42's.

**Consequence for the L1 (concrete, actionable):**
- The C1 port must take `frozen_drift` / `kind_at` / `commits_touching` / `MERGE_AWARE` from `tools/round-43/c1-counter.py`, not from `tools/round-42/c1-counter.py`. The draft's "port of round-42" text should name round-43 for the walk.
- `tools/round-43/c1-counter.py` is absent from the draft's frozen-path list. The walk's source must be frozen (the port diff is auditable only if its source is). Add it.
- `--full-history` made no difference on the four scenarios. Not adopted: no scenario showed a need, and the change would alter a proven walk. Logged as an open question, not a recommendation.

## Finding 2 — `python3 -I` blocks a shared module

Verified on Python 3.14.8: `python3 -I -B counter.py` cannot `import freeze_check` from its own directory (`No module named 'freeze_check'`); a `sys.path.insert` would work, but it defeats the isolation the counters' docstrings promise. The lane's convention is single-file stdlib counters (`tools/round-4*/` — every counter is self-contained), and the freeze rule hashes exactly one counter file (`counter_sha256`). A shared module would add a second dependency whose bytes the receipt does not hash, so it needs either a receipt change or a silent identity gap.

## Finding 3 — the lane already copies, helper by helper

Same-name helpers are byte-identical copies across counters (`ast.dump` hashes match): `show`, `sha256_bytes`, `present`, `full_rev`, `is_ancestor`, `first_add`, `Unevaluable` appear identically in round-42/43 C1 and round-41/42 C2. Copy has been the convention for about fifteen rounds. The walk is the one helper that diverged, which is exactly the failure mode that a copy invites.

## Question 1 — shared `tools/round-44/freeze_check.py`?

**Keep separate for the code. Do not create the module.** Reasons, by diff size:
- Module: ~66 walk lines moved, plus an import shim (`sys.path` hack, breaks `-I`), a receipt change to hash the module (`counter_sha256` would no longer cover the walk), a new frozen-path entry, and a second file to freeze. Larger than the copy.
- Copy: C2's counter is a new file, so the 66 lines are new text in a new file; C1 changes one function (replace the 21-line round-42 walk with the 66-line round-43 walk, which is the port itself).
- The walks are not identical in policy anyway. C2 (per draft C2 landing mechanics) must relax `frozen_path_changed` for rubric-named paths and bind the diff to exact expected bytes. The shared part is the primitive `touched(root, freeze, rev, path) -> commits` plus the endpoint-blob compare; the policy stays per counter.

**The one small deduplication (the answer to "ONE"):** pin the walk behaviour, not its text. Both counters' `--selftest` run the same four scenario recipes from the probe (linear edit/restore, merge-commit edit, side-merged restore, delete/re-add) and assert the touched/untouched outcome. A future edit to either copy that loses the merge-commit case then fails both selftests, and nothing needs to be imported. Cost: ~45 lines of recipe per counter, all in selftest code that is already frozen.

## Question 2 — oracle binding (C1) vs rubric binding (C2)

C1: receipt vs independent reader. The reader is `unsquashfs` 4.7.5 (and the unblob `__output__` tree, S138), pinned as frozen `oracle.tsv`/`carriers.json` bytes at freeze; the receipt is REA 6.5.0 with sasquatch. A second comparison, receipt vs counter-time REA rerun, checks producer self-consistency.

C2: asserted vs re-derived. The statement's value (a SCORECARD count, a SHONEN `path:line`, a map-row count) is compared with a value the counter recomputes at REV from git objects. The reference is recomputed live, not pinned.

**The contract both satisfy:** *reference independence under a frozen projection.* The reference side never reads the subject's stored value. Both sides are normalised by the same frozen projection function, the comparison is equality, and "could not derive" is a separate outcome (exit 2, never a pass or a mismatch).

Known failure mode in the lane, from the round-42 C1 oracle work: a subject artifact that the reference side can reproduce (`core`, "oracle-closed") is satisfiable without running. The C2 analogue: a rubric check that reads the observed value from the same statement text it compares is oracle-closed. Rubric review should require each check's observed side to come from a source the statement's author did not write (git object, command output, or a file the statement does not quote).

**Recommendation: keep the two bindings separate.** The shared part is one sentence of contract, not code. The comparison bodies are a few lines each and differ in normalisation.

## Verdict (the one recommendation)

- Code: **keep separate**, no `freeze_check.py`.
- Required correction, not optional: C1's walk comes from round-43, and `tools/round-43/c1-counter.py` joins the frozen-path list.
- The one dedup: both counters' selftests assert the same four walk scenarios (behavioural pin, no import).

## Limits and not-verified

- The probe covers four scenarios, not the full space. It does not prove the round-43 walk is complete; it shows round-42 is incomplete and round-43 covers the cases probed.
- `--full-history` was tested on the same four scenarios only.
- No C2 rubric exists yet at base; the C2 claims above are the draft text, not measured data.
- No lane file other than this report and the artifact/receipt paths was written. No git mutation in the lane. No c1-run.sh run.
