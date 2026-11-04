Seat: ScribeLesson (scribe). You draft the round-85 lesson and the routed-defect corrections. You do not commit and you do not write the lane tree.

# Write `<wave dir>/candidate/corpus/lessons/round-85.md`
Sections, in order: a title line naming the round; `## Gate` (candidates considered; admitted; rejected with reason and flip condition; the spot-check result left as `pending: non-author closure`); the S304 Gate facts are supplied by ScribeSource (its `report.md`, read it when it exists — poll with one `sleep 60` check per call, at most 20 calls, then proceed without it and say so); `## Mistakes` with one row per mistake: class · evidence pointer · captured-by · fix.

Mistake M85-1 (routed from `corpus/lessons/round-84-verifier-spotcheck.md` R2 and R3):
- R2 claimed the S303 `teaches` reason names the npm tarball URL in "five scopes (S083/S090/S092/S119/S123)". Count it yourself at 91eeb72f: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 91eeb72f:corpus/SOURCES.md | grep -n -F 'rea-agents-6.5.0.tgz'` and list the row ids. Report the exact count and ids.
- R3: the r84 lesson cites `l1/waves/round-84/w1/SentinelScope/esc-receipt.json`. Run a pointer sweep over the r84 lesson: `grep -o 'l1/waves/round-84[^ )`]*' corpus/lessons/round-84.md | sort -u | while read p; do test -e "$p" && echo "ok $p" || echo "MISSING $p"; done` (run from the lane root at 91eeb72f: use `git -C … show 91eeb72f:corpus/lessons/round-84.md` into your scratch file first). Expected RED on the wording. Then show the corrected pointer `.ufo/waves/round-84/w1/SentinelScope/esc-receipt.json` resolves (GREEN), by `test -e` in the lane tree (read-only).
- Captured-by: none. Fix: the appended correction in this lesson plus the sweep command above (shown red before the correction, green after).

Routed defect R4 (M84-4, no evidence pointer for a removed `met = all(arms)` field): find the commit that removed the field: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin log --oneline -S 'met = all(arms)' 91eeb72f -- tools` (read-only). Report the hash(es) and the line of removal. Write it as an appended correction.

# Appended corrections (new text only; do NOT rewrite the round-84 lesson or spot-check; name them "Correction, round 85")
Within the lesson, a `## Corrections (append-only)` section with: C-R2 (seven rows, ids and count from your grep, citing the r84 spot-check §4); C-R3 (corrected pointer and resolution proof); C-R4 (commit hash evidence).

# Draft `candidate/corpus/QUALITY.md` addendum? NO. Do not touch QUALITY.md. Instead, in your report, propose exactly one QUALITY criterion (text, ≤3 lines) that the M85-1 fix would add, citing this lesson, for the L1 to decide.

# Deliverables (wave dir /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-85/w1/ScribeLesson/)
`candidate/corpus/lessons/round-85.md`; `sweep-red-before.txt` and `sweep-green-after.txt` (the exact command outputs); `r2-r4-evidence.txt` (grep and log outputs); `report.md` (≤ 60 lines: what you wrote, the S304 gate facts used, open questions); `DONE` marker last.
