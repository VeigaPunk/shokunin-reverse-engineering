# ControlPriorKnowledge — R22 W2 reviewer report

Seat: `KaidokuR22R.ControlPriorKnowledge-6` (reviewer, leaf).
Scope: no-harm control for "prior corpus/knowledge files byte-identical B→final"
(claims.json `no_harm[0]`; expanded control read over every `corpus/` byte at
baseline). B = `7787fea4d6fd718726de92ed20759d11ce7b8b48` (exists: `git cat-file
-t` → `commit`). HEAD = `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67` on `main`.
This is a review of the current tree (worktree, per assignment — uncommitted
bytes included), not an outside admission and not a final-after claim: `rev`
final does not exist yet and the tree was still mutating during this review.

## Verdict

PASS at observation time (last full sweep 2026-10-21T13:08:34Z, snapshot
re-confirmed 13:10:25Z): every `corpus/` path present at B survives in the
worktree with identical blob SHA-1; zero deletions repo-wide; every modified
tracked file under `corpus/` is append-only (0 baseline lines removed);
uncommitted in-flight edits observed during review were likewise additive.

## Commands and observed results

1. Baseline inventory:
   `git ls-tree -r 7787fea... -- corpus/` → 136 entries
   (`corpus/knowledge/` 103 files incl. `.gitkeep`, `corpus/lessons/` 30 files
   incl. `.gitkeep`, plus `QUALITY.md`, `README.md`, `SOURCES.md`); all `100644 blob`.

2. Worktree inventory: `find corpus -type f | wc -l` → 138
   (`knowledge` 104, `lessons` 31). Delta = exactly 2 new files:
   `corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md`,
   `corpus/lessons/round-22.md` — both match authorized touches
   (`corpus/knowledge/2026-10-21-r22-*.md`; lessons `round-22.md` = frontier_step
   Mistakes vehicle).

3. Byte-identity sweep (run twice, once knowledge-only, once full corpus —
   `git ls-tree -r B -- corpus/` piped per-path to `test -f`, `test -L`,
   `git hash-object`, `stat -c '%a'`):
   - All 103 baseline `corpus/knowledge/` files: worktree `git hash-object`
     equals baseline blob SHA; all modes 644. No MISSING / CHANGED / SYMLINK.
   - Full-corpus sweep → exactly three CHANGED lines, all authorized-touch files
     outside `knowledge/`:
     `QUALITY.md` B=430c00cf…→W=e0f65cc0…, `README.md` B=83b0550c…→W=0a2dc1ec…,
     `SOURCES.md` B=54a4e988…→W=3b58ca38….
   - Zero MISSING, zero SYMLINK-NOW, zero mode anomalies.

4. `git diff --name-status B` (excluding `.ufo` additions) →
   `M LOG.md`, `M PROVINCE.md`, `M SCORECARD.md`, `M SKILL.md`,
   `M corpus/QUALITY.md`, `M corpus/README.md`, `M corpus/SOURCES.md`,
   `A corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md`,
   `A corpus/lessons/round-22.md`. **Zero `D` entries.**

5. Append-only checks — `git diff B -- <f> | grep -c '^-[^-]'`:
   `SOURCES.md`=0, `QUALITY.md`=0, `README.md`=0, `PROVINCE.md`=0, `SKILL.md`=0.
   Prefix preservation (adjacent no_harm rows, checked informally):
   `head -c $(len(B:file)) file == git show B:file` → `LOG.md PREFIX-PRESERVED`,
   `SCORECARD.md PREFIX-PRESERVED`.

6. Strays: `find corpus -type l -o -name __pycache__ -o -name '*.pyc'` → empty;
   `git ls-files --others --exclude-standard -- corpus/` → empty;
   `git ls-files -s -- corpus/` modes all `100644`.
   `.gitignore` = `__pycache__/`, `*.pyc` only.

7. In-flight edits observed mid-review (tree mutating; both additive):
   - `git status --porcelain -- corpus/` at 13:10:25Z → `M corpus/SOURCES.md`,
     `M corpus/knowledge/2026-10-21-r22-flutter-static-boundary.md`,
     `M corpus/lessons/round-22.md`.
   - `git diff HEAD -- corpus/knowledge/...flutter...md`: +14 lines, appended
     `## Round-22 source qualification` section (S054 supersedes S052 teaching
     clause; inference vs documentation boundary). File is post-baseline →
     outside the byte-identity invariant regardless.
   - `git diff HEAD -- corpus/SOURCES.md`: +1 row `| S054 |` appended after S053.
   - `git diff HEAD -- corpus/lessons/round-22.md | grep -c '^-[^-]'` → 0.

8. Grounded baseline counter run (read-only; counter reads only git objects at
   `--rev` via `git show`, loads revision-pinned helpers into a tempfile dir):
   `python3 -I -B .ufo/waves/round-22/tools/count-c1.py --root <LANE> --rev B`
   → **exit 1**; JSON: `catalog_zero_count 20`, `catalog_mentioned_count 133`,
   all six T1 verbs inside `catalog_zero` — matches claims.json `before_expected`.

## Invariants for L1 verification (final-rev recipes)

The counter (`count-c1.py`) reads only `git show <rev>:<path>` — worktree state
is irrelevant to it; L1 must re-run all of these at the FINAL commit:

- `git diff --name-status B <FINAL> -- corpus/knowledge/` → only `A` rows;
  every `A` path matches `corpus/knowledge/2026-10-21-r22-*.md`. Any `M`, `D`,
  `R`, or `T` entry breaks no_harm[0].
- `for p in $(git ls-tree -r B --name-only -- corpus/knowledge/):`
  `git show B:$p == git show <FINAL>:$p` byte-for-byte for all 103 paths
  (blob-SHA equality suffices; modes all `100644`).
- `git diff B <FINAL> -- corpus/SOURCES.md corpus/QUALITY.md | grep -c '^-[^-]'`
  → 0 (prior SOURCES/QUALITY rows byte-preserved; reordering also trips this).
- LOG.md / SCORECARD.md: `head -c $(len(B:file)) <FINAL>:file == B:file`
  (prefix preservation; verify at final, not on uncommitted tree).
- `git diff --name-status B <FINAL> | grep -c '^D'` → 0 repo-wide.
- `count-c1.py --rev <FINAL>` exit code and `t1_exercised_count` must be
  reported exactly as measured (k/6); do not preclaim 6/6 — current worktree
  shows only the `identify-flutter-build` knowledge entry landed.

## Residual risk / verification gaps

- Tree was live-mutating during review (SOURCES.md S054 row and the flutter
  entry's qualification section appeared between snapshots). All observed
  mutations were additive; a destructive edit could still land before final.
  The 13:08/13:10 sweeps are point-in-time evidence, not a guarantee.
- `SKILL.md` modified vs B — outside this lane's named no-harm list (touches do
  name PROVINCE.md for C2; SKILL.md delta is append-only per invariant 5's
  method but content scope belongs to whichever seat owns it; flagging for L1
  awareness only).
- New-file admission (does `2026-10-21-r22-flutter-static-boundary.md` satisfy
  C1 counting: bound non-refused record, evidence_id, S051+ source citation)
  is the C1 verifier's call, not this lane's; S051–S054 `used-by` cells do name
  the entry in current worktree SOURCES.md.
- `git hash-object` computes content SHA over raw file bytes; byte-identity
  observed is strong. No `.gitattributes` present (find found none) → no
  attribute-driven normalization ambiguity.

No tools installed (read-only git/python3/find/stat; per contract, no install
expected). Blockers: none — full scope observable; only the final-rev re-run is
deferred by definition.
