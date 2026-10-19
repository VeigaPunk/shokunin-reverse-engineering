# Proposed change (PATCH TEXT — NOT APPLIED) — SEAT EX-15 / chain c1

Target: `.gitignore` (repo root)
Origin: containment corroboration — `.ufo/gates/__pycache__/` was created in-window at
2026-10-19 06:58:37 by a C3 seat importing `.ufo/gates/c1-census-v10.py`, and it was
**not** ignored (`.gitignore` contains no `__pycache__` pattern; `git check-ignore` returned
no rule). It showed up as `?? .ufo/gates/__pycache__/` in `git status --porcelain` and would
be swept into an integration commit. EX-26 removed it at 07:03 (verified absent 07:03:42),
but any future census run that imports the instrument will recreate it.

This patch is a proposal only. No seat may apply it (the parent integrates records).

## Diff

```diff
--- a/.gitignore
+++ b/.gitignore
@@
+# Python bytecode caches — created whenever a seat imports an instrument
+# (e.g. .ufo/gates/c1-census-v10.py) instead of running it as a script.
+__pycache__/
+*.py[cod]
```

## Placement note

Append at the end of `.gitignore`. The existing file has no `pycache`/`__pycache__` rule
(verified: `grep -rn "pycache\|__pycache__" .gitignore` → no match). Exact insertion point is
the parent's choice; the two patterns are order-independent with respect to existing rules.

## Effect

- `git status --porcelain` stops reporting `?? .ufo/gates/__pycache__/` after any census run.
- Removes the class of leak entirely, rather than relying on each seat remembering to clean up.
- Does not affect tracked files: `__pycache__/` is currently untracked and no tracked path
  matches either pattern (checked at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`).

## Alternative considered and rejected

Adding `-B`/`PYTHONDONTWRITEBYTECODE=1` to the seat instructions instead. Rejected because it
depends on every seat's cooperation across 64 seats and gives no protection against a seat
that runs the census the ordinary way — the `.gitignore` rule is enforced by git regardless of
seat behaviour.
