# R43W2C2Registry — corpus/SOURCES.md falsification

## Evaluation identity

- Measured revision: `5856614ac4bf7f2363bbcd1956644474a82108e5` (lane HEAD at evaluation).
- FREEZE: `f3f8db389416d094b1ddeb1215ddcf914bfc0d1c`; BASE: `6b9e64fe7e0de202d9383baad5792fbfe039a743`.
- Plan read first: `plans/round-43-claims.md` at the measured tree; its recorded blob/hash is not independently checked here.
- `git merge-base --is-ancestor FREEZE REV`: exit 0 (ancestor confirmed).

## Results

- Rows (`^| S[0-9]`): BASE 134; FREEZE 137; REV 137. Counts meet the stated final count.
- BASE→REV diff: **4 insertions, 0 deletions**, not the frozen plan's claimed exact `3 insertions, 0 deletions`. The diff consists of exactly the three S135/S136/S137 table rows **and an additional blank line** before `## Paths`. This is a concrete discrepancy in the byte-level numstat predicate/receipt, even though the row-level addition count is three.
- FREEZE→REV `corpus/SOURCES.md` diff is empty; freeze blob SHA-256 and REV/worktree file SHA-256 are both `251ec4a72ee3dcf1f0f5e45debc001be2333c0340b661e616ebceaaedb62c68c`. Thus frozen registry bytes are unchanged after FREEZE.
- BASE blob SHA-256: `8c6c53143741b03a4261049b50844d2179be3b139f0f2769c7e2acc147bf2ed5`. The displayed complete BASE→REV diff shows only appended S135–S137 and a blank line, with no deletion or modification of base rows; all base row bytes remain.
- Used-by entries: S135 names `corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md`; that file exists and cites S135. S136 and S137 both name `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`; that file exists and its front matter cites both. `grep`/search results also show S135 referenced by the v4 entry and S136/S137 by the assimilation entry.
- Registry rows are exactly S135/S136/S137 as additions. S135 row has the pinned LICENSE URL and digest `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`; S136 and S137 are the plan's two assimilation sources.

## Receipt cross-check

Committed `.ufo/waves/round-43/l1/scores/c2-at-09ab56b8.json` is for revision `09ab56b8fdc2efcc3b58b203644537d84dd5ac9e`, not this measured REV. It records `sources_numstat: "4\t0\tcorpus/SOURCES.md"`, `rows_total: 137`, `sources_sha256_at_rev` equal to the FREEZE/REV hash above, and `exit_code: 1` / `checks_ok: false`. The measured tip is later than that receipt. Its 4/0 numstat agrees with the independently recomputed result and contradicts the plan's exact 3/0 expectation; do not treat the receipt's failed overall score as a passing C2 claim.

## Commands and evidence

Commands run (all read-only, in `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`):

1. `git log --oneline -15; git rev-parse HEAD; git status --porcelain` — HEAD `5856614ac4bf7f2363bbcd1956644474a82108e5`; unrelated worktree changes were present (`.ufo/waves/round-43/w2.ready`, `SCORECARD.md`, `SHONEN.md`, `.ufo/waves/round-43/w2.ready.dispatched`, and untracked wave directory); `corpus/SOURCES.md` was not listed as modified.
2. `git merge-base --is-ancestor f3f8db389416d094b1ddeb1215ddcf914bfc0d1c 5856614ac4bf7f2363bbcd1956644474a82108e5` — exit 0.
3. `git diff --numstat 6b9e64fe7e0de202d9383baad5792fbfe039a743..5856614ac4bf7f2363bbcd1956644474a82108e5 -- corpus/SOURCES.md` — `4  0  corpus/SOURCES.md`.
4. `git diff 6b9e64fe..5856614a -- corpus/SOURCES.md` — showed S135, S136, S137 additions and an extra blank line; no removed lines.
5. `git diff --stat f3f8db38..5856614a -- corpus/SOURCES.md` — empty (exit 0).
6. `wc -l corpus/SOURCES.md; sha256sum corpus/SOURCES.md; git show <REV/FREEZE/BASE>:corpus/SOURCES.md | sha256sum; git show <REV/FREEZE/BASE>:corpus/SOURCES.md | grep -c '^| S[0-9]'` — 240 physical lines at REV; hashes and row counts reported above.
7. Read receipt via `read` and searched knowledge entries with `grep` tool. Relevant source rows are in `corpus/SOURCES.md` at the measured blob; entries are as identified above.

Limitations: no alternate full semantic validator/LSP was queried for Markdown; this attack is a byte/diff/count and used-by existence check. No scratch directory was created, no fixtures/extractors run, no installation, no VCS mutation. No artifacts beyond this report were needed.

**Finding:** Registry freeze integrity and row retention/count hold, but the frozen BASE→REV numstat assertion is false by one blank-line insertion (4/0 observed rather than 3/0 required).