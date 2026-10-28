# R44C2Shonen — SHONEN.md assertion census (round 44, wave 1, C2 rubric input)

Seat: `R44C2Shonen` · lane `kaidoku` · read-only; no claim data run, no REA, no
`tools/round-44/c1-run.sh`. Sibling seat `R44ScoutCalib` owns
SCORECARD.md + corpus/README.md; this report is the SHONEN.md slice only.

## Receipt

| field | value |
|---|---|
| command | `python3 census.py` (`.ufo/waves/round-44/w1/artifacts/R44C2Shonen/census.py`, cwd `/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Shonen`) |
| exit code | 0 |
| stdout sha256 | `58e4f285de3e2430e5eccb69f0d219e7894abd51649143718c7ab3d640636700` (census-out.json, byte-identical to `R44C2Shonen.json`) |
| script sha256 | `dd9b0230d9244aff7b1590f2e6298677f2d010efe540a2d3cc84ffb990224151` |
| wall time | 0.516 s |
| base rev | `c29360e3ba5381a5ab69e372d0d9577970f85018` |
| subject | `SHONEN.md` blob `afeee543775114804328065150379642799b4e60` — identical at base and worktree HEAD (`fc5eb54a`); no uncommitted changes |

## Method

Every SHONEN.md statement of form `path:line`, `path:a-b`, `N of M`, or a bare
path pointer was enumerated from the committed blob (18 lines; assertions all
live on lines 6–18). For each: the **pinned rev** is the `at <hex>` qualifier in
the same bullet (absent → `resolves_at_pinned = "no pin"`); **resolve** means
`git cat-file -e <rev>:<path>` (dirs: non-empty `ls-tree`), `1 ≤ lo ≤ hi ≤
wc -l` for line pointers plus a content spot-check, and re-derivation under the
lane's own recipe for `N of M` (`command A` = `tools/round-36/c2-counter.py
::command_a` verbatim — rule blocks are `^- **` splits of the `## Queue-drain
craft` section). Nothing was executed beyond `git` read-only queries.

## Headline

**44 assertions, 0 stale-without-marker.** Every pinned pointer resolves at its
pin and at base; every unpinned pointer resolves at base. For the C2 rubric this
means the SHONEN.md surface contributes **zero base-state mismatches** — the
census supports (does not decide) the CTL-C2-0 honest-stop question.

## Enumerated assertions (id → verdict)

Pinned `path:line`/range assertions — all resolve at pin and base:

| id | assertion | pin | at pin | at base |
|---|---|---|---|---|
| S01 | `SKILL.md:81-449` craft section; 20/20 resolvable | e1c83313 | ✓ (command A 20/20; craft span 81–453) | ✓ bounds; note¹ |
| S02 | v3 table `SKILL.md:387-449` | e1c83313 | ✓ (marker :434) | ✓ bounds (marker now :440) |
| S03 | v2 table `SKILL.md:348-375` | 4d62ee5a | ✓ (marker :361) | ✓ bounds (marker now :371) |
| S04 | v1 table `SKILL.md:316-343` | 52b0eb29 | ✓ (marker :333) | ✓ bounds (marker now :339) |
| S05–S07 | `20/20`, `19/19`, `18/18` rule blocks | e1c83313 / 4d62ee5a / 52b0eb29 | ✓ exact under command A | ✓ (base reads 21/21 — expected, block 21 added) |
| S08 | `21/21` command A (round-43 note) | — | no pin | ✓ 21/21, 137/137 mapped, missing [] dangling [] |
| S09 | `tools/round-40/sqfs-triage-v2.py` (45-case selftest) | 4d62ee5a | ✓ | ✓ |
| S37 | `PROVINCE.md:97-125` Adjacent; refusal :116-118; tooling :119-125; byte-identical at 52b0eb29 | 52b0eb29 | ✓ content-verified | ✓ **byte-identical to pin** |
| S38 | `PROVINCE.md:378-384` round-39 appends (:378 heading, :382 row, :384 note) | 52b0eb29 | ✓ exact | ✓ exact (appends sit at EOF) |
| S41 | v4: 13 columns, 15 rules, marker `sqfs-triage-table v4` | eb8215ac | ✓ (marker :521, 13 cols, 15 rows) | ✓ (marker :525, same shape) |
| S42 | v4 region hash `92540586…` | d1681696/6b9e64fe/77d196c6 | ✓ substance² | ✓ substance² |
| S43 | `3\t0` required vs `4\t0` observed numstat | 6b9e64fe..77d196c6 | ✓ (`4 0` diff; `checks.sources_numstat_three_additions == false`) | ✓ |

Bare paths / globs / N-of-M score claims — all resolve at base:

| id | assertion | result |
|---|---|---|
| S10–S11 | `tools/round-39/{sqfs-triage.py,c2-counter.py}` | exist |
| S12 | selftests 35/35 + 27/27 (w2 seats) | both `R39W2C2Rescore/*-selftest.txt` receipts committed |
| S13–S16 | w2 artifact paths (Rescore selftest, IndepEval, Shortcut, AxisFit) | all exist |
| S17–S20 | `corpus/evidence/round-{39,40,41,42}/c1/` | all exist |
| S21 | `corpus/lessons/round-39.md` | exists |
| S22 | `tools/round-43/c1-counter.py` | exists |
| S23–S24 | `R41W2Repro*.md`, `R40W2Repro*.md` | 3 + 3 matches |
| S25 | v4 evaluator 78/78 @ eb8215ac | receipt `c2-at-eb8215ac.json`: `matched 78 n 78` (met_target false — the R42-C2 stop SHONEN names) |
| S26–S29 | C1 met 4/4 @ eb8215ac, 4/4 @ e9a24d07, 3/4 stop @ 42c10a58, 6/6 @ 6fdaf4f1 | all receipts confirm `carriers_matched`/exit exactly |
| S30, S32 | 26/26 held-out (v2) + independent eval | `c2-at-42c10a58.json` matched 26/26 exit 0; `R40W2C2IndepEval.md` states 26/26 |
| S31 | r43 c1-counter matched 78/78 exit 0 | receipt `c1-at-77d196c6.json`: `matched 78 n 78 met_target true exit 0` |
| S33–S36 | LOG round-{39,40,41,42} entries | headings exist (`## 2026-10-26 — round N …` / `## Round 42`) |
| S39 | `PROVINCE.md:386-394` round-40 block | exact at base |
| S40 | `PROVINCE.md:157`, `:376` dated round-39 pointers | dated `[2026-10-26: superseded…]` markers present — lane's own supersession convention |
| S44 | 136-check audit | `EXPECTED_LINT_CHECKS = 136` in `c2-score-r43.py`; receipt `copy_audit_checks 136`, `copy_audit_136_checks true` |

¹ S01 note: at `e1c83313` the craft section spans :81-453; the asserted
`:81-449` is the 20-block region minus the last four lines (v3 status text).
Bounds resolve both sides; the literal "craft section" referent is a 4-line
under-claim at the pin. Advisory, not a resolution failure.

² S42 note: the substance — v4 marker-through-table region byte-identical
across `d1681696`, `6b9e64fe`, `77d196c6`, `eb8215ac` and base — verifies (my
re-derivation gives one sha256 at every rev). The literal constant `92540586`
was not reproduced under my region delimiter (I get `99cd54d7`, 13 857 bytes vs
the knowledge entry's 13 856 — a trailing-newline/delimiter convention
difference, per `corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md`'s
recipe: marker line through end of first table). **Rubric suggestion: pin the
canonical region recipe from `tools/round-43/c1-counter.py`'s
`anchor_region_*` fields rather than a hand-rolled delimiter.**

## Not enumerated (narrative, out of spec form)

Line 7 "v3/v4 status paragraphs repaired R42-V3 before the freeze" (verified —
both paragraphs present at base); line 10 "78 carriers built only from pinned
MIT fixtures"; line 13 tuple-check ordering + CTL-C1-2/4; line 16 "sasquatch
matrix is Frontier packaging inventory only". None carry a `path:line`, `N of
M`, range, or bare-path pointer.

## Drift observation for the rubric writer

SKILL.md grew +118 lines since `52b0eb29`; every `path:line` pointer into it
still *bounds-resolves* at base, but the asserted offsets no longer point at
the same content (e.g. `SKILL.md:316-343` at base covers craft prose, not the
v1 table now at :339). This is normal append-only drift with in-file
qualifiers naming the pinning rev — **not** stale-without-marker. If the
rubric wants content-anchored checks rather than bounds checks, the check
command should grep the marker inside the asserted range or resolve at the
pinned rev (as SHONEN's own text directs via `at <hex>`).

## Disclosed limits

- Selftest counts (35/35, 27/27, 45, 26-of-26) are pointer-resolved to their
  committed receipts; this seat did not re-execute the interpreters (outside
  the census brief; counters' `--selftest` arms belong to the C2 counter dev).
- `resolves_at_pinned`/`resolves_at_base` booleans + the full
  `check_command`/verbatim observed values are in `R44C2Shonen.json`.
- No install, no network, no mutation of any tracked file; scratch confined to
  `/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Shonen`.
