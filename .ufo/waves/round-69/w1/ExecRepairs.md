# ExecRepairs — round 69, w1: R68-V4 repair prepared for landing

Seat `ExecRepairs` (executor, leaf). Delivered: a complete, tested repair draft for
`corpus/lessons/round-68-verifier-spotcheck.md` §5 defect **R68-V4**, a red-before/green-after
receipt, and the exact append-only `LOG.md` correction text. **No tracked lane file was edited**;
nothing was committed; the L1 owns the landing. Details and full evidence: `w1/ExecRepairs/repair.md`.

## 1. What the defect names, and what was measured

| # | filed claim | measurement | verdict |
|---|---|---|---|
| a | the legacy ledger "stops at round-52" | `tail -n +2 corpus/claim-freezes.tsv \| grep -c .` = **21** rows; rounds **14-32, 34, 35**; max round **35**; no `round-52` row; 0 blank rows; sha256 `2a840d72…` | **false** — it stops at round-35 |
| b | the gate "reported 20 exact of 36 on every round from 53 on" | round-24 gate run **read-only** at four revisions: `f78fc766` → `exact 20 of 21`, `6ffa9ce1` → `20 of 36`, `d7d9a62` (base) → `20 of 36`, `3f3d20fc` (HEAD) → `20 of 37`; `stray ["round-35"]`, exit 1 at each | **false as written** — `exact` is 20 throughout, but `of` is the lane's `claims.json` population and grows (21 → 36 → 37) |
| c | the failure branch's `${got:-absent}` is unreachable | missing path → `git show` rc 128, empty stdout → `sha256sum` = `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; `got` is NONEMPTY, so `:-` never fires; the branch prints `got e3b0c442…` | **confirmed** |

Supporting observations: the ledger's stray `round-35` row can never match because round-35's
container is `claims-frozen.json` (its `claims.json` was removed at `13d7a815`) and the round-24 gate's
expected set is `.ufo/waves/round-N/claims.json` only; rounds **36-52 never carried a `claims.json`**
(`git log --all --diff-filter=A` over their paths is empty), so the ledger dropped nothing there; the
round-24 gate's bytes are identical (`8a71fe84…`) at every revision measured and its only effects are
six read-only `git` subcommands plus a JSON print — it **can** be run read-only, and it was, rather
than only cited.

## 2. What was prepared

- **Hunk A** — replaces the erratum comment (current lines 31-36) with nine lines that state the true
  row set, the true last round, the stray-row mechanism by commit, and the measured
  `20 of 21` / `20 of 36` / `20 of 37` denominators. All widths ≤ 100, inside the file's own
  comment convention.
- **Hunk B** — wraps the digest in the presence idiom the same script already uses one step below
  (`git cat-file -e … 2>/dev/null`), so `got` is genuinely empty when the path is absent and
  `${got:-absent}` becomes reachable; the compare, both messages' text, `fail=1` and every exit code
  are unchanged.
- **Ready file:** `w1/ExecRepairs/prefile-check.patched.sh` (52 → 59 lines, sha256 `d19a6508…`).
  `sh -n` passes; `patch -p1` from the lane root against HEAD's bytes reproduces it byte-for-byte
  (`evidence/patch.diff`, `08e1c43f…`).

## 3. Red-before / green-after (`evidence/redgreen.out`, `fb730f07…`)

Three throwaway git fixtures in scratch (toplevel asserted before every commit) plus the real lane
root read-only:

| cell | before (HEAD's script) | after (hunk B) |
|---|---|---|
| ledger present, byte-identical to the pin | `retired …` / PASS / exit 0 | identical |
| ledger present, bytes changed | `got f062ae34…` / FAIL / exit 1 | identical text |
| **ledger absent at `HEAD`** | `got e3b0c442…` / FAIL / exit 1 | **`got absent`** / FAIL / exit 1 |
| real lane root, read-only | step 2 `retired`, step 3 `exit=1`, final FAIL | identical byte-for-byte |

The absent cell is the red→green; the other three show no behaviour change, and the real-tree row
proves hunk B changes only the diagnostic.

## 4. LOG.md correction (append-only, never a rewrite)

`LOG.md:4137` keeps its bytes. `repair.md` §5 carries the exact block to append: a
`## 2026-11-03 — round 69, KaidokuR69 — correction: …` heading in the round-65/66/67 shape, then the
measured correction bullet, a "filed bytes are not rewritten" bullet, and the files-touched bullet. A
one-line variant is included for folding into an existing round-69 bullet if the L1 prefers no heading.
Both are additions; neither touches line 4137.

## 5. Collision recorded (the L1 must choose)

At **23:38:55**, after this seat's 23:36 copy, a third party left an **uncommitted** repair of the same
defect in `tools/round-29/prefile-check.sh` (sha256 `9a403dc1…`, 58 lines, 16 insertions / 10 deletions
vs HEAD; HEAD unchanged at `3f3d20fc`). This seat did not make or touch it; the bytes and the diff are
retained as `evidence/prefile-check.as-found-in-worktree.sh` and
`evidence/worktree-diff-vs-head.diff`.

Verified on a scratch copy of those bytes (`sh -n` OK): pin-match PASS/exit 0, changed FAIL/exit 1, and
absent prints `ledger1 legacy ledger absent at <rev>` / FAIL / exit 1. So it satisfies (a) and (c) and
deletes the (b) falsehood. It leaves three things open: its cited `awk … | sort -u` lists the rows that
exist rather than printing the "no row 36-68" negative (and does not mention round 33); it carries only
the `20 of 21` reading, not the denominator growth; and it prints `got` unguarded after removing the
stderr suppression (harmless in all three cells).

**Land exactly one.** If the as-found edit wins, hunks A/B are redundant and only §5's LOG correction is
still required. If this draft wins, land `prefile-check.patched.sh`. The two agree on message and exit
code in every fixture except the absent cell's wording (`got absent` vs `absent at <rev>`), which is
cosmetic.

## 6. Evidence, limits, tools

- Receipts in `w1/ExecRepairs/evidence/`: `patch.diff`, `redgreen.out`,
  `prefile-check.as-found-in-worktree.sh`, `worktree-diff-vs-head.diff`, and the four round-24 gate
  runs (`r24-gate-at-{f78fc766,6ffa9ce1,d7d9a62…,head}.json`).
- **Observation:** hunk B adds one `git cat-file -e` per run; step 2 remains a byte-identity pin and
  still cannot pass on a tree where the ledger is absent (by design).
- **Inference (disclosed):** a present-but-unreadable blob would still report the empty digest, because
  `git show`'s stderr suppression is deliberately untouched (minimal diff). Named, not proposed — it is
  outside the three defects.
- **Unknown:** none of the three defects is falsified; no claim predicate was re-read or re-frozen.
  Every number above was produced by a command run in this seat; the full commands are quoted in
  `repair.md` §2.
- No tool was installed or upgraded; no pacman transaction ran; scratch
  `/fast/scratch/hyaku/kaidoku-r69/ExecRepairs/` is removed before yielding.
