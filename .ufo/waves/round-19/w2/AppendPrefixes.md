# W2 — AppendPrefixes: no-harm byte-prefix audit (LOG, SCORECARD, prior lessons/reports/predictions/run evidence)

- Seat: KaidokuR19.AppendPrefixes-3 · 2026-10-20 · read-only lane (only this report written)
- B = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; current committed tip = `refs/heads/main` = `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; current working tree also checked.
- Axes (godspeed): (1) LOG/SCORECARD byte-prefix at B; (2) no-rewrite of protected classes across every changed file; (3) completeness/honesty of the modification inventory.

## Verdict

**PASS — no-harm holds.** LOG.md and SCORECARD.md at B are byte prefixes of both the committed tip and the working tree (pure EOF appends). Zero deletions, zero renames in B..main. No prior lesson, prior wave report, prediction, or retained run-evidence file was modified or rewritten. All 12 structurally edited files are living/current-round targets named by the claims (routed-defect tools, gates, PROVINCE freshness, SKILL registry, corpus row tables). Observations only; no defect found.

## Method and commands (all run in LANE; read-only git; observation unless labelled)

```
git --no-optional-locks rev-parse refs/heads/main                       # → d0690fd44f46d8a7fe9da5f01c6be723d12abd41, EXIT=0
git --no-optional-locks log --oneline 8a8da7e..refs/heads/main          # 85589ac, a1140e7, 4f6c73f, 5e364bd, d0690fd, EXIT=0
git --no-optional-locks merge-base --is-ancestor 8a8da7e... refs/heads/main   # EXIT=0 (B is an ancestor; no history fork)
git --no-optional-locks diff --name-status -z 8a8da7e..refs/heads/main  # classified per-file (below), EXIT=0
git --no-optional-locks status --porcelain                              # worktree drift snapshot, EXIT=0
```

Byte-prefix rule applied per modified file: `current[:len(B_blob)] == B_blob` with `len(current) >= len(B_blob)`, blobs read via `git cat-file blob REV:path`; working tree read directly for LOG/SCORECARD. Status counts over all 320 changed paths: **M=15, A=305, D=0, R=0, T=0** (python classification, EXIT=0).

### Core check — LOG and SCORECARD byte prefix (observation)

| File | B bytes | tip bytes | worktree bytes | B is prefix (tip) | B is prefix (worktree) | Δ |
|---|---|---|---|---|---|---|
| LOG.md | 146,631 | 148,954 | 148,954 | True | True | +2,323 |
| SCORECARD.md | 174,530 | 177,846 | 177,846 | True | True | +3,316 |

```
git --no-optional-locks diff --stat 8a8da7e..refs/heads/main -- LOG.md SCORECARD.md
# LOG.md       | 35 +++++++++++++++++++  SCORECARD.md | 32 ++++++++++++++++++++  2 files changed, 67 insertions(+), 0 deletions; EXIT=0
```

Single hunks, both at EOF: LOG.md `@@ -2215,3 +2215,38 @@` (new section starts LOG.md:2218 `## 2026-10-20 — round-19: routed r18 defects, province freshness, toolchain replay`); SCORECARD.md `@@ -2469,3 +2469,35 @@` (SCORECARD.md:2472 `## Round 19 — routed r18 defects, province freshness, toolchain replay, 2026-10-20`). Prior bytes untouched; worktree == tip for both (absent from porcelain).

### Protected classes — no rewrite (observation)

Protected-path diff, everything that changed under prior rounds / lessons / state:

```
git --no-optional-locks diff --name-status 8a8da7e..refs/heads/main -- \
  .ufo/waves/round-17 .ufo/waves/round-18 corpus/lessons corpus/knowledge .ufo/state MANIFEST.json   # EXIT=0
# M .ufo/waves-17/tools/receipt-validate.py; M round-18 tools jj-red-before.py, revpin.py, routed-defects.py
# M corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md; A knowledge/2026-10-20-r19-...; A lessons/round-19.md
# (nothing under .ufo/state, MANIFEST.json, round-17/18 runs, round-17/18 lessons, round-17/18 wave reports)
```

- Prior lessons `corpus/lessons/round-17.md`, `round-18.md`, `round-18-verifier-spotcheck.md`: absent from the change list → byte-identical to B. `round-19.md` is a new file (A) — allowed (this round's lesson).
- Prior wave reports (`round-17/w*`, `round-18/w*` report .md): absent from change list → untouched.
- Predictions: all 19 files under `.ufo/waves/round-19/predictions/` are A at `a1140e7`; `git diff --name-only a1140e7..refs/heads/main -- .ufo/waves/round-19/predictions` → empty (EXIT=0), i.e. frozen and never touched after; `sha256sum -c predictions/SHA256SUMS` from `.ufo/waves/round-19/` → **19 OK, EXIT=0** (worktree bytes match frozen manifest).
- Retained run evidence: `round-17/runs/**`, `round-18/runs/**` absent from change list. Round-19 `runs/`, `evidence/`, `predictions/`: 214 tracked files, **0 files touched in more than one commit** (each added exactly once, never rewritten post-add). No carrier executed, no log rewritten.
- `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`: M but byte-prefix (+6,183 bytes, 41 added lines, 0 deleted) — append-only, content preserved.

### Complete modification inventory, B..main (observation)

**15 modified (3 byte-prefix appends, 12 structural edits), 305 added, 0 deleted/renamed.**

Byte-prefix appends: `LOG.md`, `SCORECARD.md`, `corpus/knowledge/2026-10-19-arc3-r12-…md` (above).

Structural edits (numstat `git diff --numstat 8a8da7e..main`, EXIT=0) — every one a claims-named living target, none protected:

| File | +/− | Why (claims.json / carried list) |
|---|---|---|
| `.ufo/waves/round-18/tools/routed-defects.py` | 126/36 | C1 R18 defect routing/gates |
| `.ufo/waves/round-18/tools/jj-red-before.py` | 229/21 | carried: env scrub + path guard |
| `.ufo/waves/round-18/tools/revpin.py` | 11/6 | carried: `:6` @- wording |
| `.ufo/waves/round-17/tools/receipt-validate.py` | 130/8 | C1 R18-VALIDATOR-DIGEST |
| `.ufo/gates/custody-pair/custody-pair.py` + README | 66/2, 8/3 | carried: repo-root records the argument |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | 133/15 | C1 R18-HEAD-ALIASES |
| `PROVINCE.md` | 17/17 | C2 freshness rewrites (stale pin/doctor/cache statements re-verified 2026-10-20; matches amendment "3 stale statements each") |
| `SKILL.md` | 37/11 | C1 registry/lint-limit updates |
| `corpus/QUALITY.md` | 1/0 | row 22 appended (per-seat cause records) |
| `corpus/README.md` | 3/1 | knowledge/lesson index rows added; one index line extended to include the r19 knowledge doc |
| `corpus/SOURCES.md` | 3/0 | S037, S038 rows + census note (matches claims: rows opened this round) |

305 added files: round-19 claims/contract/tools/verify, wave-1 specs/patches/reports, wave-2 records, `predictions/`, `evidence/` (incl. `runs/t1250-*/` Ghidra-bound logs), new knowledge + lesson docs. Full lists were enumerated by the classification run; spot-list above is representative, counts exact.

### Uncommitted working-tree drift at review time (observation; inference labelled)

Porcelain snapshot: 8 modified, 2 untracked — `.ufo/waves/round-19/tools/routed-r18.py`, `wave2-registration.json`, `wave2-registry.json`, `verify.py`, `SKILL.md`, `corpus/lessons/round-19.md`, `corpus/knowledge/2026-10-20-r19-…md`, `.ufo/waves/round-17/tools/receipt-validate.py`; untracked `evidence/wave-outcomes/w1-terminal.json`, `w2/`. **Inference:** in-flight wave-2 work by the integration owner/siblings, consistent with the wave-2 assignment ("verification expected-red safeguards" commit d0690fd + later uncommitted edits). None of these is LOG.md/SCORECARD.md or a protected artifact; `receipt-validate.py` (prior-round tool) carries further uncommitted edits on top of its committed routed-defect fix — tools are the declared fix targets, so this is in-scope, but flagging it since it is uncommitted lane state.

## Findings by severity

- **Critical / High / Medium: none.** All acceptance-relevant invariants verified and hold.
- **Low-1 (observation):** `corpus/README.md` contains the only deletion in the corpus (1 line rewritten to extend the knowledge index). Not a protected class; recorded for completeness.
- **Low-2 (observation):** SCORECARD round-19 section ends with a forward reference ("Final measured verdict appended after integration") — an intentionally open append slot, consistent with the append-only protocol; it is not a rewrite.
- **Low-3 (calibration, observation):** my first per-file provenance parse mis-handled `git log` blank-line framing and returned "0 files"; I discarded it and re-ran with a corrected parser before using the result. Reported so no stale number circulates.

## Residual risk and verification gaps

- Scope is B→current only; pre-B history authenticity not re-audited.
- Added files are provenance-checked (single-commit touch) but their content is not independently re-derived here (e.g., I did not re-run `routed-r18.py`/`c1-census` — other seats judge claim substance; this seat judges bytes/no-rewrite).
- The lane worktree is concurrently mutating; the prefix verdicts are true for the observed snapshot (tip d0690fd + worktree at check time). LOG/SCORECARD were not in the dirty set, so committed == worktree for them.
- No tools installed (none needed); no production edits; no clone needed (pure read-only audit, no mutation tests required by this attack).
