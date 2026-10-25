# R35Audit37 — census receipt counts (round 35, wave 1)

Seat: R35Audit37 (leaf member; no subagent dispatch). Item: **Verify census receipt counts**.
Read-only verification; no lane writes except this report. No VCS mutation.

## Scope
Verified the round-35 census-start receipt `.ufo/waves/round-35/assimilation/census-start.txt`
against (a) frozen claim D-1, (b) the actual `corpus/SOURCES.md` content at the base revision
`aa04633a686d49756763b1feed4be6830d5bb479`, (c) a re-run of the census validation command used by the
receipt, and (d) the git commit ordering / hash pin recorded in `.ufo/waves/round-35/claims-canonical.json`.

## Verification commands and output

### 1. Receipt content vs D-1 claim
`read .ufo/waves/round-35/assimilation/census-start.txt`:
- `rows=106` (line 19) — claim: 106 rows ✓
- `EXIT=0` (line 16) — claim: exit 0 ✓
- W04 warnings: exactly 9 lines — S033, S047, S054, S062, S069, S083, S090, S092, S102 — claim: 9 W04 warnings ✓
- Manual frozen census block: `tiers A=100 B=5 C=1`, `status mined=102 rejected=4`, `duplicate_ids=0` (lines 18-23)
- Header: `Captured 2026-10-25 (L1 prep, before the freeze commit)` — consistent with commit date.

### 2. Independent recount of SOURCES.md at base revision (immutable git object)
`git show aa04633a686d49756763b1feed4be6830d5bb479:corpus/SOURCES.md` parsed with the registry table shape
(`| S### | ... |` rows):

```
rows=106          (106 `| S[0-9]{3}` data rows in ## Registry section)
tiers:  A=100  B=5  C=1        (sum 106)
statuses: mined=102  rejected=4 (sum 106)
duplicate_ids=0
```

All match the receipt's frozen counts exactly. Kind distribution also sums to 106
(code 28, community 4, dataset 12, docs 36, own-work 9, paper 6, spec 8, tool 3).

### 3. Re-run of the receipt's census command (read-only, same argv)
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku; echo "EXIT=$?"
```
Output: exactly the same 9 W04 lines (S033/S047/S054/S062/S069/S083/S090/S092/S102), then
`kaidoku  ok  .../corpus/SOURCES.md`, then `EXIT=0`. No E-findings → `malformed=0` consistent.
`corpus/SOURCES.md` is byte-unchanged since base (see §5), so the re-run reflects the base state.

### 4. Hash pin
`sha256(census-start.txt)` = `b6ce2b1773c60af4e3f5b14b7a63ba9743cae1eeec121b1ada50178a3d7af10a`
— identical for working tree, blob at `d2729cba`, and the `frozen_inputs` pin in `claims-canonical.json` ✓

### 5. D-1 commit ordering
- `git rev-list aa04633a..HEAD -- corpus/SOURCES.md` → **empty** (no post-base commit touches SOURCES.md yet).
- `git rev-list aa04633a..HEAD -- .ufo/waves/round-35/assimilation/census-start.txt` → `d2729cba` only.
- `d2729cba`'s parent is exactly `aa04633a` (instruments-first prep is the *first* commit after base; receipt included there).

⇒ "census-start receipt committed no later than the first commit that changes corpus/SOURCES.md after the base" holds (trivially, since no such SOURCES.md commit exists, and the receipt is in the first post-base commit).

## Findings
No falsifications found in scope. All census receipt counts check out:
- rows=106 ✓ (recounted from base git object)
- EXIT=0 ✓ (re-run of validate, exit 0)
- 9 W04 warnings ✓ (S033/S047/S054/S062/S069/S083/S090/S092/S102; re-run identical)
- tiers A=100/B=5/C=1, mined=102/rejected=4, duplicate_ids=0 ✓
- Receipt committed in first post-base commit (d2729cba, parent = base) and byte-identical at HEAD and against the frozen hash pin.

## Severity
- No defects, no severity-1/2/3 findings in scope.

## Residual risk / limits
- The validate re-run executes against the current worktree, not the exact base instant; equivalence rests on `corpus/SOURCES.md` having no commits and no tracked modifications since base (verified via `git rev-list` empty + clean `git status` for tracked files).
- `w1-settle.json` / `w2-settle.json` (D-2 seat accounting) are out of this item's scope and were not inspected; `w1-settle.json` is present only as an untracked wave-1 artifact.
- The receipt records a manual second source (`CORPUS.md v1 commands`) whose exact commands are not listed in the receipt; its numbers were independently reproduced here from the base git object, so the values are verified independent of those commands.
- No write/network/VCS access to sibling or fleet repos was made; no `/fast/scratch` find/du.

## Conclusion
Census receipt counts are correct and consistent with the base revision, the frozen claim D-1, the live tool output, and the committed hash pin. Advisory evidence stands without falsification.
