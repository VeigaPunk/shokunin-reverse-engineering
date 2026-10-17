# CB2 — rewrite-class adversary

## CLAIM
The rounds 2/3/4/7 SCORECARD in-place edits (plus an unflagged round-1 edit) breach the letter of "appended, never rewritten" but not its purpose: they are living-status updates that alter no score, verdict, or evidence claim, and no record section was touched. Recommend: adjudicate as a disclosed formal deviation, not evidence corruption; round 10 appends only.

## METHOD
Read-only. `git diff --numstat <c>^ <c> -- SCORECARD.md LOG.md` for the nine records commits plus `c343939`; `git diff --unified=0` hunk-range analysis against each pre-image's first `## luna-round-` heading; `git log -S`/`git show <c>^:SCORECARD.md` for disclosure and old-cell recovery; read lane-A seats W2/W3/W7/W9/N1 and `corpus/QUALITY.md:5`. No probes.

## FINDINGS
SCORECARD ins/del, LOG del=0 in every commit: `a4bd355` 40/4, `a9580eb` 60/8, `0772d54` 55/7, `cfc84c2` 46/1, `6e2ee8f` 32/1; `f0e8cde`, `411175e`, `a280e07`, `6e83a20`, `c343939` pure-append. The class is real, spans five commits, and starts at round 1 — lane A flagged only 2/3/4/7.

For breach: five of ten records commits delete lines from the mandated record; repo precedent elsewhere is supersede-by-naming (`corpus/QUALITY.md:5`) and append-only knowledge errata.

Against breach: every deletion falls at pre-image line ≤68 — the living "Owned axes"/"Open gaps" region (first round heading at :234-237 in each pre-image); arc-wide `git diff --unified=0 a4bd355 6e83a20 -- SCORECARD.md` hunks only at :23, :56-69, :71(+2), :270(+342) — no `## luna-round-N` section was ever modified. No score changed (calibration 0→10, depth 10, coverage 72/72→78/78 both 10.0). Old cells survive in git (`git show a9580eb^:SCORECARD.md | grep -c '0/9 → 9/9 preselected'` → 1) and in-tree at `SCORECARD.md:177`; round 1 self-disclosed the practice (`SCORECARD.md:265-267`), round 4 disclosed its pointer fix (`:71-72`).

## THREATS
The goal text is not in-repo; I used the parent's paraphrase — its exact scope over living sections is unverifiable here. Lane-A seats found the same four diffs; my additions are round 1's unflagged 4-deletion edit and the frozen-record proof. Deletions verified by git/numstat only; no semantic re-audit of every surviving cell.

## VERDICT
FINDING: five records commits (`a4bd355`, `a9580eb`, `0772d54`, `cfc84c2`, `6e2ee8f`) rewrote living SCORECARD cells in place — a formal departure from appended-never-rewritten, but immaterial to evidentiary integrity (record sections frozen, before-states preserved, no score/verdict changed); disclose at closeout, append only in round 10.
