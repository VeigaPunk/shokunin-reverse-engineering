# ScoutOperatorLessons — operator lesson files and the QUALITY→lesson citation map (round 20, W1)

Written 2026-10-20T17:49:46-03:00 (clock at write).

Verdict: **`corpus/lessons/operator-*.md` is empty at `14f0260ad319ecc26994381b2415d5a999003375` and has
never existed on any ref**, so "for each, does QUALITY.md or SKILL.md cite it?" has an empty domain.
`corpus/QUALITY.md` cites lessons in exactly 7 of its 22 admission rows (rows 16–22, `:26-32`; 12 distinct
lesson paths, all resolving at the baseline); `SKILL.md` cites exactly one lesson path (`SKILL.md:443`).

Read-only scout: no REA/provider/analyze call, no Ghidra, no Go toolchain execution, no gate run, no tool
install/update. Every read is revision-pinned (`git --no-optional-locks show 14f0260…:<path>`), never `HEAD`.

Axes named before measuring:
- **calibration** — does the empty operator set still hold at the r20 baseline, and do the prior seat's
  statement and the QUALITY anchors match the bytes?
- **coverage** — which rows carry a resolvable lesson path vs a bare round label; which lesson files are
  never cited by either target file.
- **depth** — do the cited line anchors land on the routed substance, not merely the right file?

Labels: `[OBS]` = Git object/worktree bytes at the pinned rev, or live clock output; `[INF]` = inference.

## 1. `corpus/lessons/operator-*.md`

`[OBS]` Zero such files at the baseline, and none in repository history:

| command (in LANE) | result | exit |
|---|---|---|
| `ls corpus/lessons/operator-*.md` | `No such file or directory` | 2 |
| `find corpus/lessons -maxdepth 1 -name 'operator-*.md' \| wc -l` | `0` | 0 |
| `git ls-tree -r --name-only $REV -- 'corpus/lessons/operator-*.md'` | 0 lines | 0 |
| `git log --all --pretty=format: --name-only --diff-filter=ADMR \| sort -u \| grep -i 'operator-'` | no match, 0 lines | 1 |
| `git ls-tree -r --name-only $REV \| grep -i 'operator'` | `.ufo/waves/round-18/w1/ScoutOperatorLessons.md` only | 0 |
| `grep -i 'operator' .ufo/waves/round-20/claims.json` | 0 lines | 1 |

`[OBS]` The only `operator`-matching path at the rev is a prior **seat report**, not a lesson. Neither
target file references any `operator-<name>.md`: `grep -cE 'operator-[A-Za-z0-9._-]+\.md'` = `0` in both
`SKILL.md` and `corpus/QUALITY.md` (exit 1, no match). The 6 `SKILL.md` lines matching `operator-` (`:72`,
`:196`, `:356`, `:358`, `:385`, `:448`) are `operator-owned`/`operator-mutable` prose — never lesson paths;
`grep -c 'operator' corpus/QUALITY.md` = `0` (exit 1). Round-20 `claims.json` names no operator lesson.

Cross-record `[OBS]`: `corpus/lessons/round-17.md:129` independently states "No `corpus/lessons/operator-*`
file exists."; `round-17.md` is unchanged between `9011581` and `14f0260` (the delta adds only
`round-18.md`, `round-18-verifier-spotcheck.md`, `round-19.md`, `round-19-verifier-spotcheck.md`).
`[INF]` The r20 target re-asks a question already settled at r18; the empty set is stable across three rounds.

Calibration note on the prior seat `[OBS]`: `.ufo/waves/round-18/w1/ScoutOperatorLessons.md:19-20` cites that
`round-17.md` sentence at `:127`; the measured line is **129** (`grep -n 'operator-\*'` on the rev blob,
exit 0). Off by 2. `[INF]` harmless to its verdict, but the anchor should not be copied forward.

## 2. QUALITY rows → lessons (admission criteria, `corpus/QUALITY.md`)

| row | line | lesson path(s) cited, as written | co-cited non-lesson anchor |
|---|---|---|---|
| 16 | `:26` | `corpus/lessons/round-14.md`; `corpus/lessons/round-13-verifier-spotcheck.md` | — ("round-13 lesson Mistakes #3/#4" named with no path) |
| 17 | `:27` | `corpus/lessons/round-15.md`; `corpus/lessons/round-14-verifier-spotcheck.md` | — |
| 18 | `:28` | `corpus/lessons/round-16.md`; `corpus/lessons/round-15-verifier-spotcheck.md:181-188` | `.ufo/waves/round-16/documentation-red.json` |
| 19 | `:29` | `corpus/lessons/round-16-verifier-spotcheck.md:183`; `corpus/lessons/round-17.md` | `.ufo/waves/round-16/verification.json:419` |
| 20 | `:30` | `corpus/lessons/round-17.md` | `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` |
| 21 | `:31` | `corpus/lessons/round-17-verifier-spotcheck.md` (`:108`, `:137`); `corpus/lessons/round-18.md` | — |
| 22 | `:32` | `corpus/lessons/round-18-verifier-spotcheck.md:146,197`; `corpus/lessons/round-19.md` | `.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-red.exit` |

Rows 1–15 (`:11-25`) cite **no** lesson path: rows 1–3 cite `CORPUS.md`/`PROTOCOL.md`; rows 4–9 cite bare
`r1` labels; rows 10–12 `r3`; rows 13–14 `r4`; row 15 cites two `corpus/knowledge/` files (and `r9-02`).
The signals table (rows 1–6, `:38-43`) cites `SKILL.md`/`CORPUS.md` only. No row cites an operator lesson.

## 3. SKILL.md

`[OBS]` One lesson citation in the whole file — `SKILL.md:443`: "Evidence and limits:
`corpus/lessons/2026-10-15-round-1-recovery.md`; `LOG.md`, Interactive round-1 recovery." No operator path
(§1). `[INF]` SKILL.md is a procedure document, not a lesson-to-criterion map; QUALITY is the only one of
the two that carries lesson lineage.

## 4. Coverage read

- `[OBS]` 7/22 admission rows carry a lesson path (rows 16–22). QUALITY names 12 distinct paths; SKILL adds
  1 (`2026-10-15-round-1-recovery.md`) → union 13 of the 26 lesson `.md` files.
- `[OBS]` Never cited by either file (13): `2026-10-13-round-1.md`, `2026-10-13-round-2.md`,
  `2026-10-13-round-3.md`, `2026-10-13-round-4.md`, `2026-10-15-round-1-admission-correction.md`,
  `2026-10-15-round-1.md`, `2026-10-18-caller-independent-services.md`,
  `2026-10-18-mechanism-matched-walls.md`, `2026-10-18-wave-dispatch-counting.md`,
  `round-12-verifier-spotcheck.md`, `round-12.md`, `round-13.md`, `round-19-verifier-spotcheck.md`.
- `[OBS]` `corpus/QUALITY.md:4` states "every criterion cites the lesson that produced it." Measured form is
  7/22 with a path. `[INF]` Rows 1–15 predate the row-cites-lesson convention (the header itself says
  "Thin at mint"), so this is a lineage gap, not an r20 regression — and the r20 claim C1 `falsified_if`
  ("any QUALITY row 1-22 changed") means fixing it is out of scope for this round.
- `[OBS]` The bare labels are not resolvable to a unique file: `corpus/lessons/round-1.md` and
  `corpus/lessons/round-9.md` do not exist (exit 2), while three round-1-scoped lesson files do
  (`2026-10-13-round-1.md`, `2026-10-15-round-1.md`, `2026-10-15-round-1-recovery.md`). `[INF]` A path-only
  census therefore under-counts real lesson references; it misses at least `round-13.md`, which row 16 names
  in prose ("round-13 lesson Mistakes #3/#4") with no path.
- Boundary note `[OBS]`: `round-19-verifier-spotcheck.md` is uncited by QUALITY/SKILL but is the r20
  outside-check target (`contract.md`, "Previous outside check"), so it is reachable from the wave contract,
  not from the quality bar.

## 5. Anchor resolution (depth)

Every cited anchor was read at the rev and lands on the substance the row describes:

| row | anchor | measured content |
|---|---|---|
| 18 | `round-15-verifier-spotcheck.md:181` | `## Routed defects and reviewer adjudication`; `:185-188` are the four numbered routes ("Invocation consistency" … "Historical SHONEN wording") |
| 19 | `round-16-verifier-spotcheck.md:183` | `1. **R16-PROVENANCE — unsupported temporal stability wording.**` |
| 21 | `round-17-verifier-spotcheck.md:108` / `:137` | `:108` pin-map table row carrying `pin_checks` `{changed:[],entries:146,equal:true,…}`; `:137` `1. **R17-PINMAP.**` |
| 22 | `round-18-verifier-spotcheck.md:146` / `:197` | `:146` `- **Dead seats.**`; `:197` `5. **R18-DEADSEAT-RECORD.**` |

`[OBS]` All 12 QUALITY paths and the 1 SKILL path exist as blobs at the rev (`git cat-file -e`, 13/13
EXISTS, exit 0 each): no dangling lesson citation in either file. `round-13.md` is the only lesson named
without a path.

## 6. Commands and exit codes (observed)

```text
$ git --no-optional-locks rev-parse refs/heads/main
d1d981d2cc041dda4656c5b01d2c8445d8d17124
EXIT=0
$ git --no-optional-locks merge-base --is-ancestor 14f0260 refs/heads/main
EXIT=0
$ git --no-optional-locks diff --stat 14f0260 refs/heads/main -- corpus/QUALITY.md SKILL.md corpus/lessons/
(no output)
EXIT=0
$ git --no-optional-locks status --porcelain -- corpus/QUALITY.md SKILL.md corpus/lessons/
(no output)
EXIT=0
$ ls corpus/lessons/operator-*.md
ls: cannot access 'corpus/lessons/operator-*.md': No such file or directory
EXIT=2
$ find corpus/lessons -maxdepth 1 -name 'operator-*.md' | wc -l
0
EXIT=0
$ git --no-optional-locks ls-tree -r --name-only 14f0260 -- 'corpus/lessons/operator-*.md' | wc -l
0
EXIT=0
$ git --no-optional-locks log --all --pretty=format: --name-only --diff-filter=ADMR | sort -u | grep -i 'operator-'
(no output)
EXIT=1
$ grep -c 'corpus/lessons/' corpus/QUALITY.md          # 7 lines: :26-:32
7
EXIT=0
$ grep -c 'operator' corpus/QUALITY.md
0
EXIT=1
$ grep -c 'operator-' SKILL.md
6
EXIT=0
$ grep -cE 'operator-[A-Za-z0-9._-]+\.md' SKILL.md corpus/QUALITY.md
SKILL.md:0
corpus/QUALITY.md:0
EXIT=1
$ grep -i 'operator' .ufo/waves/round-20/claims.json | wc -l
0
EXIT=0            # grep itself exit 1 (no match); wc is the piped status
$ git --no-optional-locks cat-file -e 14f0260:corpus/lessons/<each cited file>   # 13 files
EXISTS 13/13, EXIT=0 each
```

Working-tree copies of `QUALITY.md`/`SKILL.md`/`corpus/lessons/` are byte-identical to the baseline
(`diff --stat` empty; `status --porcelain` empty), so every anchor above also describes the live lane.

## 7. Workspace note

`refs/heads/main` has advanced to `d1d981d…` (baseline is an ancestor); no target-file content changed, so
the measurements remain baseline-faithful because all reads are hash-pinned. Concurrent r20 seats are
writing `.ufo/waves/round-20/`; none of their files is used as evidence here. This scout wrote only this
report. No tool installs or updates.
