# R35Audit46 — prefreeze data exposure (w1, advisory)

Item: check prefreeze data exposure; read-only or private /tmp only; no lane writes.
Scope: lane reads at HEAD ee0c865c (advanced from 3ecf4298 during the audit; base aa04633a and freeze 2323d197 verified ancestors at 3ecf4298), private /tmp only. No lane production writes, VCS untouched, no find/du under /fast/scratch, no delegation.

## Prefreeze data inventory — committed and hash-stable
- Prep captures + census receipt were committed at the instruments-first commit d2729cba (2026-10-25 05:08) and are present at the freeze commit 2323d197 (16:12): `git ls-tree -r --name-only 2323d197 -- .ufo/waves/round-35/prep/ .ufo/waves/round-35/assimilation/census-start.txt` → 4 paths.
- Worktree bytes match every frozen hash in `claims-canonical.json`: census-start.txt `b6ce2b17…`, c1 counter `e28792c7…`, c2 counter `576c14dd…`, plans/round-35-claims.md `45b644a4…`. No drift between mutable worktree and frozen bytes.

## Exposure findings
1. **CONFIRMED — prefreeze capture duplicated world-readable into shared /tmp.** `/tmp/jsc2js-readme.md` (mode 644, mtime 15:58) sha256 `df85060f38fd9ba5…` is byte-identical to `.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md`. A freeze-cited capture exists as a world-readable shared-tmp copy (staleness/divergence risk if the capture is ever re-fetched).
2. **PATTERN — other world-readable shared-/tmp staging of round data** (mode 644/755): `/tmp/r35_p2.json` (100 jsc2js release objects; same source family as the prep page captures), `/tmp/r35-w1-dispatch.json` (sha `510a2a3b…` ≠ lane `w1-dispatch.json` `e25ea6cf…` — a variant copy of wave coordination data), `/tmp/r35-plan.json` (64-item list), assorted `r35c1-*`/`r35w1-*` control receipts, `r35_falsify.py`, `r35_probe_usedby.py`. Contrast: several seats correctly used private 0700 dirs (`/tmp/r35-A-trio-*`, `/tmp/r35audit12-*`). Mixed discipline; shared-tmp staging is the round's dominant exposure channel. None of these paths feed the frozen counters (probe below), so this is hygiene, not score integrity.
3. **Residue** — `tools/round-35/__pycache__/*.cpython-314.pyc` (gitignored; flags=0 timestamp-validated; pyc mtime+size equal the frozen sources; built 16:17 by non-`-B` import-style runs). Only consulted on import, never for `__main__` runs; advisory.
4. **Counters are exposure-clean**: only `git show`/`ls-tree`/`git log` reads; writes only caller `--json-out` plus selftest `tempfile.TemporaryDirectory` (empirical mkdtemp mode 0700); no network; both selftests green (`C1_SELFTEST: ok green=0 red=1`, `C2_SELFTEST: ok green=0 red=1`); no `/tmp/r35c{1,2}-selftest-*` residue after runs; lane `git status --porcelain` hash unchanged across all runs.

## Mutation probe — one defect: worktree contamination of the frozen score
Invariant challenged (claims plan, C1 Controls): "the counter reads immutable git objects only — no worktree … at score time". Plausible defect: verdict flips when the full after-state exists only as worktree bytes.
Setup: `git clone --no-hardlinks` lane → private /tmp dir (mode 700); detector = C1 counter extracted from freeze rev (sha `e28792c7…` verified before and after); scratch HEAD `ee0c865c`; pristine status 0 lines.
- **P1 pristine:** exit 1 — `C1_FAIL: entry_missing×2; registry_row_missing:S125; registry_row_missing:S129; province_missing×2; readme_missing×2` (stable red baseline).
- **P2 mutant:** both knowledge entries + S125/S129 SOURCES rows + PROVINCE/README coverage written to worktree only (5 status lines, no commit) → exit 1, failing list byte-identical to P1.
- **P3 mutant:** worktree `claims-canonical.json` predicate tampered (`P35-c1:` → `P35-TAMPERED-c1:`) → exit 1, identical; the predicate gate read the freeze-rev object, not the worktree copy.
- **P4 restore:** `git checkout -- .` + `git clean -fdq` (scratch only) → status 0 lines, HEAD unchanged `ee0c865c`, extracted instrument sha unchanged.
- **P5 restored rerun:** output byte-identical to P1.
**Verdict: MUTANT KILLED** — C1 scoring is immune to worktree contamination; no score-time exposure via mutable worktree bytes. C2 corroboration (not independently mutated; single-probe scope): identical git-object-only accessors in source, and C2 at HEAD fails `D2_settle_missing` for both settle receipts even though untracked `w1-settle.json` exists in the lane worktree — untracked data is invisible to the counter.

## Limits
- /tmp scan was single-level `ls -la`; seat subdir contents not enumerated. No find/du under /fast/scratch.
- Ancestry checks ran at lane HEAD 3ecf4298; probe ran at its descendant ee0c865c.
- Advisory only: no score computed, no predicate/scope altered, no lane or VCS mutation.
