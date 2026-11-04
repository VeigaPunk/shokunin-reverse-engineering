# ExecRecordAgreement — R86-C1 counter hardening (executor, candidate only)

## Result

- Candidate: `.ufo/waves/round-86/w1/ExecRecordAgreement/candidate/tools/round-86/record-agreement.py`.
- Selftest: `SELFTEST cases=48 failures=0`, exit 0 (`selftest.json`, `selftest.txt`).
- Lane at BASE `2cf0b7ff93c698809bed321f7338276a22d6beb9` (candidate, `--rev`): exit 1, `mismatches` = A1, A2, A3, `agreed 0/3` (`base.json`). Matches the BASE pre-receipt's verdict.
- Lane control (`--control substring-only`): `mismatches []`, exit 0 (`control.json`). The control still accepts the defective records.
- Refusals: `--worktree` with `--rev` → exit 2; unknown `--control` → exit 2.
- Production file untouched (sha `99cb8f…`); no commit; no edit outside the seat directory; `claims.json` and `pre/` untouched.
- No tools installed or upgraded.

Per-hunk changes and the reason for each are in `ExecRecordAgreement/notes.md`; the unified diff is `ExecRecordAgreement/candidate-vs-production.diff`.

## What the hardening found in the counter (production defects, all fixed in the candidate)

1. **A3 located the wrong object.** The production counter required exactly one `| coverage |` line in the whole SCORECARD and found 23 (history sections). The candidate reads the row under `## Owned axes`. This is a locating change; see decision F2 below.
2. **A2 read the first triple-quoted string** in the file and the first `if not case_present` regex match. Candidate uses `ast` (exactly one `not case_present` If, exactly one assigned status, `ast.get_docstring`).
3. **A1 `supersedes S303` was a prefix match** (`S3031` passed). Anchored.
4. **A1 repeated `count` words, duplicate ids, and over-long id lists** could pass. Rejected.
5. **`--rev` did not verify the revision**; an unresolvable revision returned exit 1 with mismatches, contrary to the docstring. Now exit 2.
6. **`git show` read trees and applied textconv.** Replaced by `cat-file -t` (must be a blob) and `cat-file blob`.
7. **The selftest printed `cases+1`**, a phantom case. The count is now real.

## Decisions and facts for the L1 (not changed by me)

- **F1 — pinned instrument.** `claims.json` pins the production counter at `99cb8f…`; the candidate is `a8c5a3…`. Integrating it requires a recorded instrument supersession by the L1.
- **F2 — A3 row selection (decision).** The plan says "the `| coverage |` row"; the candidate selects the Owned-axes row. Without this, A3 cannot be reached without rewriting history.
- **F3 — plan's BASE description of A3 is inaccurate.** The row names five receipts (r67, r68, r75, r76, r84); the newest r84 predates its round 85. Still a mismatch.
- **F4 — no round-85 `l1/scores` receipt exists** at BASE. A3 needs a committed receipt with a blob `rev` at the measured revision.
- **F5 — the repair's A1 count is 7, not 3.** Other URL rows at BASE: S079, S080, S083, S090, S092, S119, S123.
- **F6 — grammar trap.** Every S-id after the count clause is part of the declared list; a mention of S303 after the count fails. Place it before the count.
- **F7 — residuals.** A non-covering receipt named by the A3 row need not exist; A2 is a sentence check; A1 covers one sentence shape.

## Reachability (fixture, not a measurement)

A fixture built from BASE bytes, with a `count 7` supersession row (seven ids), the docstring sentence set to `survived`, and a round-85 receipt, reaches `agreed 3/3`, exit 0 (`ExecRecordAgreement/receipts/repair-fixture-simulation.json`, mode `worktree-fixture`). The target is reachable under the frozen rules; the lane itself is not repaired.

## Checks the main agent should run

- `python3 -I -B .ufo/waves/round-86/w1/ExecRecordAgreement/candidate/tools/round-86/record-agreement.py --selftest` → `SELFTEST cases=48 failures=0`.
- `python3 -I -B <candidate> --root . --rev 2cf0b7ff93c698809bed321f7338276a22d6beb9 --json-out <receipt>` → exit 1, 3 mismatches (BASE).
- The same with `--control substring-only` → exit 0, 0 mismatches.

## Scope note

The seat spec asked for this report at the w1 level rather than inside the seat directory; I wrote it there because the name is seat-specific and the path was given explicitly.
