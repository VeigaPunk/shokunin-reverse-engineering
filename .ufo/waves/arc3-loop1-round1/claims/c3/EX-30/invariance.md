# EX-30 (c3) — invariance check: recipe A before/after EX-28's edit

Seat: EX-30 | chain: c3 | role: executor | wave: arc3-loop1-round1
Date: 2026-10-19. HEAD at all measurements: `e845c2b524ad2e59871e004c51a1386e192a74ab` (no seat commits; parent integrates after the wave).

Task as frozen: run measurement recipe A at HEAD (before) and again after EX-28's edit
lands (poll); corpus surfaces must be untouched — expect 81/81, 13/13 both sides;
`git status --porcelain` must show no corpus/knowledge changes.

## Status

- T0 (before EX-28): COMPLETE — captured below.
- T1 (after EX-28): PENDING — polling `.ufo/gates/c1-census-v10.py` sha256 every 60 s
  (max 25 checks). T0 marker: `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`.

## T0 — before EX-28's edit (2026-10-19 ~06:59-03:00)

Recipe A (SCORECARD.md:86-124), run from the lane repo via `/dev/shm/ex30/recipeA.py`
(verbatim recipe body; script file copy in this dir is not kept — the recipe text is
in SCORECARD.md and the runner was the frozen heredoc, saved at
`recipeA-t0.txt` / `recipeA-pinned-t0.txt` outputs):

```
$ python3 recipeA.py HEAD
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [], "revision": "HEAD", "rule_blocks": 13}
```

Pinned to the explicit sha (not just `HEAD`), run twice, byte-identical:

```
$ python3 recipeA.py e845c2b524ad2e59871e004c51a1386e192a74ab
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [], "revision": "e845c2b524ad2e59871e004c51a1386e192a74ab", "rule_blocks": 13}
```

→ 81/81, 13/13, missing [], dangling [], 10.0/10.0 — the expected before-side values.

Corpus surface digests (working tree), for byte-identity comparison at T1:

- recipe-A-read surfaces (`corpus/README.md`, `SKILL.md`, `corpus/knowledge/*.md`):
  83 files, sorted sha256sum list aggregate
  `7480345a3aaa736c4b060fe2e9cfaeba6c96f2204950370027047f2087a4d634`
  (per-file list: `corpus-surfaces-sha-t0.txt`).
- whole `corpus/` tree: 95 files, aggregate
  `ad0526087e53809700acafbfa8bb4acacb67662f72f76a086c55f91eb055172a`
  (per-file list: `corpus-full-sha-t0.txt`).

Repo state:

```
$ git status --porcelain -- corpus/
(empty)
$ git status --porcelain
 M .ufo/waves/arc2-loop1-round10/C3.md
?? .ufo/gates/__pycache__/
?? .ufo/waves/arc3-loop1-round1/
```

(` M .ufo/waves/arc2-loop1-round10/C3.md` pre-exists this seat's work — visible in the
first status capture at 06:58 before any of my commands; `__pycache__` likewise
pre-existing at T0. Both unrelated to corpus.)

Auxiliary (not the frozen recipe): worktree-read variant of recipe A (same logic,
files read from the working tree instead of git objects) → 81/81, 13/13, identical
JSON apart from the `surface` field. This catches uncommitted corpus drift that the
git-object recipe cannot see.

Auxiliary c3 context: census v10 at HEAD → `VERDICT: PASS (stale=0 ambiguous=0
undeclared=0 unresolved=0)`, exit 0, sha256 of output
`3b677b8ee47eccb217616eba641fc0b66f72e53634a5ae51a92f8b04e2a22418` — byte-identical
to the captures of EX-26, SC-6 and RV-11 (4-way agreement). Note for the chain: the
census already PASSes at HEAD, so the E22 disposition is a re-key/header-record, not
a repair of a failing verdict.

## T1 — after EX-28's edit

PENDING (poll in progress). Will record: new census-instrument sha256, recipe A re-run
(HEAD + pinned), corpus digests re-run and diff, `git status --porcelain` re-run,
census re-run for corroboration.

## Attacks / refutations

A1 — "recipe A is blind, so an invariance check via recipe A is vacuous."
Ran perturbation injections in a scratch copy (`cp -a` of the lane repo to
`/dev/shm/ex30/repo-copy`; no git mutations anywhere, scratch removed at close):

- A: broke one coverage-map token in `corpus/README.md`
  (`2026-10-13-mcp-registrations` → `…registrationX`) → worktree variant:
  `mapped 80, missing ["2026-10-13-mcp-registrations"], dangling ["2026-10-13-mcp-registration"], coverage 9.88`.
- B: pointed one SKILL.md craft citation past EOF
  (`2026-10-13-r7-01-queue-a-ops.md:84-91` → `:99999`) → worktree variant:
  `citation_resolved_rules 12, depth_score 9.23`.
- C: removed `corpus/knowledge/2026-10-13-asar-surface.md` → worktree variant:
  `knowledge_files 80, mapped 79, dangling` grew by that stem.

Verdict A1: the measurement logic IS sensitive in all three drift directions. But the
*frozen* recipe, run against `HEAD`, reported 81/81, 13/13 unchanged under every
injection — it reads git objects (`git show REV:path`), so it cannot see uncommitted
worktree drift. Hence the corpus-untouched guarantee is carried by (i) the T0/T1
digest comparison of the worktree (sensitive: perturbed README sha `53994ae2…` vs T0
`7c0cf671…`) plus (ii) the auxiliary worktree-read variant; the frozen recipe alone
would not have caught an uncommitted corpus edit.

A2 — "maybe EX-28's edit target overlaps recipe A's read set." Checked:
`git ls-files .ufo/gates/` → the census instrument is tracked, and recipe A reads only
`corpus/knowledge/*.md`, `corpus/README.md`, `SKILL.md` (git objects). Disjoint by
construction; T1 confirms empirically.

A4 — "is the frozen recipe sensitive to *committed* drift, or is it broken in some
other way?" Ran it against recorded older revisions: `b910a33` → 80/80, 11/11
(SCORECARD.md:1066 records the same); `3395b6d` → 78/78, 9/9 (SCORECARD.md:515).
Verdict: the recipe is faithful on committed history and re-derives the SCORECARD's
recorded values exactly; its only blind spot is uncommitted worktree state (A1).

A3 — "/tmp scratch is fine." Refuted by the environment: `/tmp` is a `usrquota` tmpfs
whose user quota is exhausted (writes fail with `Disk quota exceeded` at 06:58, with
3.1 G free — EDQUOT, not ENOSPC). Scratch moved to `/dev/shm/ex30`; noted for the
wave (other seats may hit the same wall).
