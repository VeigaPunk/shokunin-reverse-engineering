# FB1 — format 2: lane-A round-10 report-format audit (16 sample + frame)

## CLAIM
Report-format sentinel ("format 2", per `.ufo/waves/luna-round-9/SB4.md:1` precedent), read-only 22:44–22:46 -03: on the frozen 57-file lane-A frame and its 16-file sample, the five-section sequence, ≤400-word cap, and one-line `^(CLEAN|FINDING)` verdict are clean frame-wide 56/57 — sole defect: `F1.md`'s sixth `## ` heading.

## METHOD
Frame = `.ufo/waves/luna-round-10` lane-A subset, rule `stem[1:2] != 'B'` (excludes 12 lane-B arrivals during the run, e.g. `TB1.md`); 57 files, list+hashes `/tmp/fb1r10-laneA.txt`, frame aggregate sha256 `f91190f7a05b06460ef2177ee97595809d5ffe437ecfc45c77efe1d70a41dba7`. Sample = ranks `(57i+8)//16`, i=1..16 → `A4 C1 D1 D4 F2 N2 P1 R3 R6 S2 S5 W3 W6 X1 X4 Y4` (aggregate `765c152b3a908115af48544742d0bae29167314d4ec7e81612446082887aacf3`); strict every-4th (the arc rule) yields 14 at n=57, so an even-spread variant anchored at rank 4 was used. Per file, python: `## ` heading list == `CLAIM/METHOD/FINDINGS/THREATS/VERDICT`; whitespace word count; last non-blank line `^(CLEAN|FINDING)`; verdict-section non-blank line count; `\r` bytes; citation categories. HEAD `c3439392` = briefed `6e83a20` + 1 (`git rev-list --count 6e83a20..HEAD` → `1`); `git show --stat c3439392` → `LOG.md 16 +`, `SCORECARD.md 12 +` (0 deletions, 22:42:01); `git status -uno` empty; frame re-hashed identical after checks.

## FINDINGS
- 56/57 exact five-heading sequence; `F1.md:11` inserts `## Work performed` between FINDINGS and THREATS (`sha256 9a8e6d21…`).
- Word cap 57/57 (max 370 `X2.md`; sample max 352 `X4.md`).
- Verdicts 57/57 single-line `^(CLEAN|FINDING)` (49 FINDING / 8 CLEAN); verdict sections one non-blank line.
- Citations: 51 path:line of any extension, 1 seat shorthand (`R8.md:9`), 5 exact command+output (`C2 D6 N2 X2 Y4`); no file lacks an evidence form. Sample 16/16 clean: 14 path:line, 2 command (`N2`, `Y4`).
- Reported, not failed: `X4.md:10` embeds `# kaidoku luna-round-10 — arc closeout` plus `### ` subsections inside FINDINGS (five `## ` exact); 29/57 lack trailing LF; no `\r`.

## THREATS
Structural, not semantic. The strict rule rejects extra `## ` headings, so X4's embedded H1/subsections and the missing trailing LFs are reported for parent adjudication, not failed. Frame = saved files, not a dispatch roster; lane-A names landing after the freeze are outside the hash. Lane-B reports excluded by rule. HEAD moved off the briefed commit mid-wave by another writer; this seat wrote only this file. Word cap is whitespace-split.

## VERDICT
FINDING: 16/16 sample and 56/57 frame conform; `F1.md` carries a sixth `## ` heading (`## Work performed`).
