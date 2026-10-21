# R22-W2 ControlAppendOnly — LOG/SCORECARD baseline byte-prefix control review

- **Seat:** KaidokuR22R.ControlAppendOnly-6 (leaf; author-side review only — no admission emitted)
- **Scope:** no-harm control "LOG/SCORECARD prefixes preserved" (claims.json `no_harm`), repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- **Baseline B:** `7787fea4d6fd718726de92ed20759d11ce7b8b48` (round-21 land)
- **Revision observed:** HEAD = `2ee3d9f51c6a995d1aefe48f6a44cfd08d492d67` ("round-22: retain static frontier evidence and calibrated catalog dispositions"), `main` resolves to the same commit. Worktree is detached at this rev; assignment's "current branch main" holds at the ref level.
- **Caveat per target:** this is the *current* candidate revision, not a "final" claim. Every verdict below is conditioned on this rev and MUST be re-evaluated at the actual final revision.

## Commands and observed results

All commands run from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; exits 0 unless noted.

### 1. State census

`git status --short --branch` → `## HEAD (no branch)`; tracked modifications: ` M corpus/lessons/round-22.md` (uncommitted, post-HEAD working-tree edit); untracked round-22 wave files (`w1/`, `w2/`, `wave1-*`, `wave2-*`, `claims.json`-era artifacts). LOG.md and SCORECARD.md are **clean** in the worktree.

`git diff --stat 7787fea4d6fd718726de92ed20759d11ce7b8b48 HEAD -- LOG.md SCORECARD.md` → `LOG.md | 30 ++++`, `SCORECARD.md | 21 ++++`, "51 insertions(+)", 0 deletions. `git log` B..HEAD shows exactly **one** touching commit: `2ee3d9f`.

### 2. Byte-prefix verification (the control itself)

For each file, baseline blob extracted via `git cat-file blob B:<file>` → `/tmp/base_<file>`; HEAD blob likewise → `/tmp/head_<file>`; then `cmp -n $(stat -c%s /tmp/base_<file>) /tmp/base_<file> /tmp/head_<file>`:

- `LOG.md`: **PREFIX-OK** — `HEAD[0:161682] == baseline bytes` (baseline blob `d015a66a60d003e415d7d0a629c6f0d6c48421d7`, 161682 B; HEAD blob `3cb1fae190a0267068d672229d2c9a244095a249`, 163547 B; appended = 1865 B). Baseline content SHA-256 `3caca21b84e15fc5adcb854f706b96e8e0933042835c9132874978bca5c7edff`.
- `SCORECARD.md`: **PREFIX-OK** — `HEAD[0:196503] == baseline bytes` (baseline blob `41f058e5aae0bc6b4e1ff236c6497e88d701cc8c`, 196503 B; HEAD blob `6ab9831489ea0a5db802ba8ca21158b84f25cb94`, 198155 B; appended = 1652 B). Baseline content SHA-256 `8f43d15e26613e10275a5edbac248fa0081dc5cd75b45e9984d3feca36b128b3`.

Boundary hygiene: both baseline blobs end `64 2e 0a 0a` (`"d.\n\n"` — newline + blank line), so each append begins on a fresh line. First appended bytes: LOG.md → `## 2026-10-21 — round-22: uncovered static evidence and honest catalog dispositions`; SCORECARD.md → `## Round 22 — uncovered catalog evidence and calibrated dispositions`. `git diff` hunks confirm append position (LOG.md `@@ -2453,2 +2453,32`, SCORECARD.md `@@ -2726,2 +2726,23`), i.e. appends are at EOF.

`git hash-object LOG.md SCORECARD.md` vs `git rev-parse HEAD:<file>` → worktree files are **byte-identical to HEAD blobs** (`3cb1fae…`, `6ab9831…`).

### 3. File census at B

`git ls-tree -r --name-only B | grep -E '(^|/)(LOG|SCORECARD)(\.md)?$'` → 25 entries: root `LOG.md`, `SCORECARD.md`, plus 23 fixture files (arc3-loop1 round1/round2 scratch/fixture SCORECARDs, round-17 temporal-attack fixtures). `git diff --name-status B..HEAD` shows only root `LOG.md`/`SCORECARD.md` as `M`; **no fixture LOG/SCORECARD file was touched** (every other B..HEAD path is `A` or an unrelated `M`).

### 4. Mechanical enforcement chain

- Round-22 `verify.py` (`.ufo/waves/round-22/verify.py`) does **not** itself check LOG/SCORECARD prefixes. It records `prior-controls`: `[python -I -B] .ufo/waves/round-21/controls.py --root <root> --before B --after <rev>`, expected exit 0 (verify.py:64).
- Round-21 `controls.py` **does** enforce it (controls.py:82,86): `prefix={x: blob(after,x).startswith(blob(before,x)) for x in ['LOG.md','SCORECARD.md']}` and `ok = not changed and all(prefix.values()) and ...`. `blob()` uses `git show <rev>:<path>` — committed bytes, immune to worktree edits. Failure mode: `controls_failed`, exit 1 → verify.py `prior-controls` check `pass:false` → `summary['pass']=false`, exit 1.
- Same controls.py:81 also enforces `prior corpus/knowledge` + `corpus/lessons` byte-identity and controls.py:83-84 the QUALITY.md prior-row prefix (`new_rows[:len(old_rows)]==old_rows`), covering the sibling no-harm items.
- Residual risk: `controls.py`'s prefix check uses `str.startswith` on full bytes — correct for append-only. Edge note: if a *final* rev ever deleted LOG.md/SCORECARD.md, `blob(after,x)` would raise `subprocess.SubprocessError` → `controls_unevaluable`, exit 2 ≠ expected 0 → still caught as failure. Coverage of fixture LOG/SCORECARD files is **not** in controls.py's prefix dict (only the two root files), but fixtures are tracked under `corpus/knowledge`/`.ufo/waves/round-20/`? — fixtures under `.ufo/waves/arc3-*` and `.ufo/waves/round-17/` are **outside** `prior` (line 80 scopes to `round-20/`, `corpus/knowledge/`, `corpus/lessons/`). Fixture mutation would evade controls.py; the claims' `no_harm` wording "LOG/SCORECARD prefixes preserved" most plausibly refers to the root pair (the records files), but L1 may wish to confirm scope.

### 5. Appended-content honesty spot checks (calibration axis)

- LOG append: states R22-C1/C2 moves, names B and declaration `75f04a446c61761182145c058e545551ca4ecd76` (verified `git rev-parse 75f04a4` → identical), records "lost W1 dispatched93 but parent Anthropic429 terminated every seat with zero reports … no output is credited" — consistent with the wave-2 recovery framing.
- SCORECARD append: baseline counts recorded honestly (`B count0/6 … exit1`, `B count0/14, exit1`), scores `10.0→10.0 delta0`, no capability/ownership/mastery claim — consistent with `not_claimed`.
- Cosmetic style (non-blocking): generated appends omit spaces around numbers (`claim22 attempt1`, `reported57/132`, `dispatched93`, `capability17`, `window10`, `QUALITY29–30`, `exits0`, `count0→k of6`). Cosmetic only; does not affect bytes-before-boundary.

## Invariants for L1 verification at the final revision R

1. `git show R:LOG.md | head -c 161682` must equal `git show B:LOG.md` byte-for-byte (equivalently `blob(R) .startswith(blob(B))`, or `cmp -n <base_size>`). Same for `SCORECARD.md` at 196503 bytes. `cmp` exit must be 0.
2. Any appended bytes must begin after index 161682 / 196503 respectively and start at a line boundary (invariant observed: baseline ends `\n\n`, append starts `## `).
3. `git diff --name-status B R` must show at most `M LOG.md`, `M SCORECARD.md` for those names — no `D`, no `R`, and zero entries among the 23 fixture LOG/SCORECARD paths enumerated at B.
4. Round-22 verify chain: `prior-controls` (round-21 `controls.py --before B --after R`) must exit 0, which mechanically re-asserts invariants 1 (plus prior-file byte-identity and QUALITY row-prefix) — but only when verify.py is actually run against R. If R ≠ `2ee3d9f`, my `cmp` observation does not transfer; rerun.
5. Worktree-vs-rev identity: `git hash-object LOG.md` == `git rev-parse R:LOG.md` holds only if the worktree is the judged state; currently true (`3cb1fae`, `6ab9831`).
6. Worktree drift to watch: `corpus/lessons/round-22.md` is modified-but-uncommitted at observation time; controls.py reads committed blobs so uncommitted drift cannot corrupt its verdict, but it also means worktree state is not what the counters see.

## Findings

- **No defect found** in the LOG/SCORECARD prefix control at rev `2ee3d9f`: both root files are strict byte-prefix extensions of B; append boundaries are clean line boundaries; fixture files untouched.
- **Residual risk (low, scope):** the controls.py prefix dict covers only root `LOG.md`/`SCORECARD.md`; 23 fixture files under `.ufo/waves/arc3-*/` and `.ufo/waves/round-17/` are protected neither by the prefix check nor by `prior_files` byte-identity (out of `round-20|corpus/knowledge|corpus/lessons` scope). No evidence of fixture mutation B..HEAD (name-status clean), but the mechanical net has a gap if "LOG/SCORECARD" is read broadly.
- **Residual risk (low, procedural):** prefix preservation is enforced only via `prior-controls` inside verify.py; claims.json `no_harm` lists it as a separate item, so a final state that never runs verify.py would leave this item verified only by this review's `cmp` observation at `2ee3d9f` — re-run per invariant 1/4 at the true final revision.
- **Verification gap (none blocking):** I did not execute verify.py or controls.py (read-only scope; lane bounds). All prefix findings derive from `git cat-file` + `cmp -n` on committed blobs, which is the same byte equality controls.py tests.

## Tooling

No installs or updates performed (none needed; pacman transactions paused host-wide per directive). Tooling rules file `/home/vgpnk/.omp/agent/RULES.md` not consulted because no install was attempted.
