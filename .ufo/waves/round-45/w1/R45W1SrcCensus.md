# R45W1SrcCensus — report

Seat `R45W1SrcCensus`, round 45 wave 1, lane `kaidoku`. Leaf seat; no subagents dispatched (the
lane-bounds "single labrat" slot was not needed and not used).
Evidence directory: `.ufo/waves/round-45/w1/R45W1SrcCensus/` — `report.md` (full receipt narrative)
and `receipts.log` (24 receipts, each with exact command, exit code, stdout sha256, UTC stamp).
Base `149133d4`, freeze `f762b727…`, HEAD at measurement `faa875bc`. Instrument set: frozen
`plans/round-45-claims.md` + `tools/round-45/` (read, never written); measured tools
`scripts/sources-census.sh` (host repo) and `kaidoku-shokunin/tools/round-38/registry-immutable.sh`.
No install performed (nothing was missing). Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W1SrcCensus`
removed after the ledger copy.

## Findings

**F1 (calibration, invocation).** The prompt's `--base/--head` flags do not exist in
`tools/round-38/registry-immutable.sh`; its documented form is positional
`registry-immutable.sh LANE BASE REV`. All guard receipts use the documented form with the prompt's
values in that order. A seat that pastes the prompt's flags gets the lane-unknown death path, not a
score.

**F2 (calibration, the assigned interval is vacuous).** `corpus/SOURCES.md` is byte-identical at
base and at the freeze — same sha256 `90a10fdd…`, 139 rows — so the assigned guard receipt
(`149133d4 → f762b727`) exits 0 with empty stdout because *nothing differed*. Recorded, but it must
not be cited as evidence of append-only discipline. The informative intervals are
`f762b727 → HEAD` and `149133d4 → HEAD`: 139 → 141 rows, both exit 0, empty stdout (R6a/R6b). The
two added ids are `S140`, `S141`, both from `e715263c` (12:33:03Z), i.e. after the freeze.

**F3 (calibration, claim-citation scoping hazard).** At the freeze, `S140`/`S141` are **absent** from
the registry (grep count 0); they land at `e715263c`. `SOURCES.md` is explicitly not frozen, so this
is legal — but R45-C1's clause "the block cites `S140`" is only resolvable against a `--rev` at or
after `e715263c`. A wave-2 seat that checks the S140 citation while materialising `SOURCES.md` at the
freeze will report it unresolvable and mis-score C1. Score at a rev that includes the landing commit.

**F4 (depth, the guard is not a registry-membership checker).** A row-shaped line appended under
`## Leads` gives the guard exit 0 (R9a) while the census gives exit 1 with
`E12 S900 row outside Registry section` (R9b). Same asymmetry for an existing row relocated out of
`## Registry` (R8: one E12, exit 1; the guard's `rows()` has no section filter, so it reads the row as
unchanged). Any claim resting on "no registry row changed" must run the census as well; the guard
alone proves only per-row cell stability within whatever the file contains.

**F5 (calibration, `--file` is not a revision census).** `validate --file` derives the used-by root
as `realpath(dirname(file))/..` (`scripts/sources-census.sh:497-501`); on a snapshot outside a lane
tree every used-by misses (R7a: 231 E11, exit 1; R7b: **the same bytes R1 validates clean** → 233 E11,
exit 1). Do not read `--file` E11 lines as lane findings and do not use `--file` for a claim's
before/after census. To census a revision, materialise the file at `<lane>/corpus/SOURCES.md` inside a
lane whose targets exist.

**F6 (depth, three-way count agreement).** `141` from the prompt's `grep`, from the guard's stricter
`^ {0,3}\| *S[0-9]{3,} *\|`, and from the census `rows` metric (R3, R4); tier A 133 + B 7 + C 1 = 141;
status mined 136 + rejected 5 = 141; queued 0; `missing` 0; no invalid enums. W04 = 14 lines over
10 distinct URLs (rea-agents tarball ×5, nine singletons), zero E lines, exit 0 — the clean-lane
answer, since W codes never set the exit status (`:795-806`).

**F7 (calibration, W04 count is unchanged by this round).** 14 W04 at the freeze bytes (R7a) and 14 at
HEAD: the two appended rows (`S140`, `S141`, distinct URLs) added no duplicate-URL warning. The
census's W04 arm fires per (url, new scope) pair, not per duplicate group — 14 rows, 10 URLs.

**F8 (depth, exit codes are semantic).** Guard `--selftest` 5/5 pass, exit 0 (R5): append 0,
in-place cell 1 (`S002 changed columns: 6`), deletion 1, reorder 1, allowed-cells 0. The guard's
positive receipt is therefore meaningful where there is delta, which is why F2 matters. Census exit
codes exercised red in this run: 1 for E03/E12 (R8, R9b) and 2 remains reserved for usage/env.

**F9 (calibration, frozen bytes intact, one worktree caveat).** No commit in `f762b727..HEAD` touches
`plans/round-45-claims.md` or `tools/round-45/`, and both the committed and worktree diffs against the
freeze are empty (R10). `git log --format=%H -1 -- plans/round-45-claims.md` re-derives the freeze.
Caveat: the frozen *directory* holds two git-ignored `__pycache__/*.pyc` files (R14) — a
`--pathspec tools/round-45/` arm that enumerates the filesystem instead of git objects would see files
the freeze does not contain. Not a violation; a trap for the dirty arm.

**F10 (calibration, instrument provenance).** `tools/round-38/registry-immutable.sh` was extended in
place at `52b0eb29` (round 39, +100/−2): the deletion arm, reorder arm and `--selftest` are that
commit's. The note that commit added still asserts inside the same file that
"`tools/round-38/registry-immutable.sh` is unchanged by this seat". The guard exercised here is the
extended version, not the round-38 delivered bytes; `tools/round-39/` holds no copy.

**F11 (depth, the guard has no could-not-evaluate arm — it cannot say "I did not run").** Three
probes:
(a) a nonexistent lane path, and a directory that is not a repository, both yield **exit 0 with empty
stdout** and a git fatal on stderr only — a silent pass, the round-44 defect class;
(b) an unresolvable **rev** yields exit 1 with one `S<n> row deleted (append-only)` per base row
(139 lines for a typo'd sha) — fabricated findings;
(c) an unresolvable **base** yields the same, one line per *rev* row (139 at the freeze, 141 at HEAD);
the count tracks the rev side because an empty first file keeps `NR==FNR` true across the whole second
file (awk collapse). Exit 2 is never emitted. Consequence: the guard's exit 0 is admissible only when
lane, revs and a non-empty base row set are independently known good.

**F12 (depth, positive control that makes receipt 2 a real reading).** Reverse interval on the real
lane (`HEAD` → freeze) exits 1 with exactly two lines, `S140` and `S141 row deleted (append-only)`.
So the guard does read this registry's 139/141 rows, even though the assigned base → freeze interval
has no delta; and it independently confirms S140/S141 are the only rows added after the freeze.

**F13 (dependency, R45-C2 preconditions).** All six paths in `tools/round-45/registry-scope.json` exist
at HEAD *and* at the freeze (`git cat-file -e`), and that file's six paths equal the set named by the
two claim files (R13). `scope_size == 6` is falsifiable rather than assumed; the C2 score itself is
another seat's.

## Retained evidence (exact)

| # | command | exit | stdout sha256 | reading |
|---|---|---|---|---|
| 1 | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | 0 | `9f32a8a8…acf19` | 14 W04, 0 E, `ok` |
| 2 | `bash tools/round-38/registry-immutable.sh . 149133d4… f762b727…` | 0 | `e3b0c442…` (empty) | no row changed outside the three cells; interval has zero delta (F2) |
| 3 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | 0 | `85a0e6eb…` | `141` |
| 4 | `bash scripts/sources-census.sh census --root … kaidoku` | 0 | `01eb62a2…` | rows 141; A133/B7/C1; mined136/rejected5 |
| 5 | `bash tools/round-38/registry-immutable.sh --selftest` | 0 | `e08d3d03…` | `SELFTEST cases=5 pass=5 fail=0` |
| 6a/6b | guard `149133d4→HEAD`, `f762b727→HEAD` | 0/0 | empty/empty | 2 legal appends, nothing else |
| 7a/7b | census `validate --file` on freeze copy / on HEAD bytes | 1/1 | `b8bb159d…`/`ef326043…` | 231/233 E11 = `--file` root artefact (F5) |
| 8 | census on a copy with `S141` moved under `## Leads` | 1 | `844d2539…` | one `E12` |
| 9a/9b | guard / census on a fixture appending a row under `## Leads` | 0 / 1 | empty / `31f74089…` | guard hole, census net (F4) |
| 10 | `git diff --stat`/`git log` freeze vs HEAD on frozen paths | 0 | empty | frozen bytes intact |
| 11 | rows+sha of `SOURCES.md` at base/freeze/HEAD | 0 | — | 139/139/141; base sha == freeze sha |
| 12 | census on two rows, same URL, one backticked one bare | 1 | — | E04 0, W04 0 → duplicate detection is backtick-sensitive; live impact nil (S038/S047 both backticked) |
| 13 | `git cat-file -e` × 6 scope paths | 0 | — | present at HEAD and freeze |
| 14 | `git status --porcelain --ignored -- tools/round-45/` | 0 | — | 2 ignored `.pyc` inside the frozen directory |
| 15a | guard, nonexistent lane / non-repo dir | 0 / 0 | empty | silent pass: cannot distinguish "clean" from "did not run" (F11) |
| 15b | guard, unresolvable rev (base = `149133d4`, rev = `deadbeef…`) | 1 | 139 lines, all `row deleted (append-only)` | fabricated findings, not exit 2 (F11) |
| 15c | guard, unresolvable base vs freeze / vs HEAD | 1 / 1 | 139 / 141 `row deleted` lines | count tracks the rev side (awk `NR==FNR` collapse) (F11) |
| 16 | guard reverse interval `HEAD → f762b727` on the real lane | 1 | `S140 row deleted` + `S141 row deleted` | positive control: arm live on the real file; only two rows added post-freeze (F12) |

## Risks handed to the L1

1. **Do not cite receipt 2 alone** as append-only evidence (zero delta). Cite 6a/6b plus 5, or say so
   explicitly.
2. Wave-2 scoring must pick a `--rev` ≥ `e715263c`, else C1's `S140` citation is unresolvable (F3).
3. Any landing row that claims "registry unchanged" should name the census E12 arm, not just the
   round-38 guard (F4).
4. If the landing cites the round-38 guard as an untouched round-38 instrument, that provenance is
   wrong (F10); cite it as the round-39-extended guard at `52b0eb29`.
5. Exit-cell honesty, two cases. The census emits `0` clean / `1` findings / `2` usage-env, so its
   registry row can carry all three. The **guard emits only `0` and `1`** — it has no
   could-not-evaluate path (F11) — so a registry row for it that writes `0`, `1` and `2` would be
   false, while a row writing "0/1" would score `thin` under R45-C2's third-column rule. The guard is
   outside R45-C2's six-path scope, so this is not a blocker; if the landing registers it anyway,
   register the gap in prose (0 clean, 1 violation *or* unreadable rev, no 2, and exit 0 on an
   unreadable lane) rather than inventing a 2 cell.

## Axis read (for the L1's scoring, not a score)

- depth: F4, F5, F8, F11, F12 give behaviour, not exit codes — the guard's section hole, its missing
  could-not-evaluate arm (silent pass and fabricated findings), the census's file-mode root, and the
  discriminating selftest plus the reverse-interval positive control.
- calibration: F1, F2, F3, F7, F10 — the instrument's own claims about itself (invocation form, interval
  meaning, provenance header) checked against the bytes.
- coverage: F6 — three independent row counters agree at 141, and the W04 layer is the same 14/10 at
  the freeze and at HEAD.

## Cleanup

`/fast/scratch/hyaku/kaidoku-r45/R45W1SrcCensus` removed after copying `receipts.log`; the two git
fixtures lived inside it and are gone. Nothing under `/tmp` was used as evidence.
