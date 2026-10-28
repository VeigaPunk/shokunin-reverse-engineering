# R45W2Pins — pin falsification, round 45 wave 2

Seat `R45W2Pins`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, HEAD
`a63d109faa050207d4c184471889049741c9ebbf` (`main`). Read-only on the lane and the fleet repo;
all writes confined to this report dir and `/fast/scratch/hyaku/kaidoku-r45/R45W2Pins`.
Receipts: `receipts.json` in this directory (19 entries, each command + exit + stdout sha256 + UTC).
No installs.

**Scope attacked.** Every 7–40 char hex token in the round-45 sections of `LOG.md`
(lines 3234–3316), `SCORECARD.md` (3519–3592) and `corpus/lessons/round-45.md` (whole) — 13
unique tokens, 7 of them commit pins — plus the arithmetic pins those sections assert
(revision identity, wave seat counts, source-row counts, block-22 shape) and the reverse
direction: which round-45 commits in `FREEZE..main` the record never cites.

## Verdicts

| # | attacks | verdict |
|---|---|---|
| A1 | the "identical values" clause for `e715263c`/`1f4b27f8`/`fedd11bf`/A3 (`SCORECARD.md:3581,3591`; `LOG.md:3316`) | **falsified** |
| A2 | wave-2 seat count "32" and its cited source (`SCORECARD.md:3527-3528`; `LOG.md:3273-3274`) | **falsified** |
| A3 | the record's completeness in the reverse direction (`FREEZE..main`) | **falsified** (8 of 12 uncited; see table) |
| A4 | all 13 hex tokens: commit-ness and ancestry vs `main` | holds (12 resolve; 1 is a sha256, correctly labelled) |
| A5 | freeze re-derivation and the freeze arm over `FREEZE..main` | holds |
| A6 | block 22's predicate shape at A3 (blocks, marker, rows, header, exit cells, refs) | holds |
| A7 | C1 and C2 predicates re-run independently at five revisions | holds (predicate met) — see A1 for the record's description |
| A8 | the six registry rows and the A3 `c1-run.sh` correction | holds |
| A9 | the claims file's "before" state for the preflight at the base | holds |
| A10 | the round-44 pin `c86ea508` (432 paths, 8 fixture paths, author/committer split) | holds |
| A11 | source-row frontier `139 → 141` and S140/S141 presence | holds |
| A12 | wave-1 seat ledger (40 seats, produced/dead split) | holds |

## Falsified

### A1 — "every earlier measurement reports the same values" is false on `block22_refs`

The record asserts value identity across revisions in three places:

- `SCORECARD.md:3591` — "the values are identical at `e715263c`, `1f4b27f8`, `fedd11bf` and A3"
- `SCORECARD.md:3581` — "`1f4b27f8` is the first met measurement, and every value is identical at both" (A1 vs A2)
- `LOG.md:3316` — "every earlier measurement (`e715263c`, `1f4b27f8`, `fedd11bf`) reports the same values"

The record's own receipts contradict it. `block22_refs`:

| rev | `block22_refs` | receipt |
|---|---|---|
| `e715263c` | **6** | `.ufo/waves/round-45/l1/scores/c1-at-e715263c.json` |
| `1f4b27f8` (A1) | **7** | `…/c1-at-1f4b27f8.json` |
| `fedd11bf` (A2) | **8** | `…/c1-at-A2.json` |
| `f59565b7` (A3) | **8** | `…/c1-at-A3.json` |

Independent re-run reproduces exactly 6/7/8/8 (`receipts.json` entries 15,17 plus the
scratch re-runs at `1f4b27f8`/`fedd11bf`; all exit 0, `met_target true`, `frozen_path_changed []`).
The cause is real and benign — A1 adds a `corpus/knowledge/` citation (6→7) and A2 adds a
citation in block 22 (7→8) — but the sentence says *values*, not *verdicts*, and one of the
values it enumerates changes. `LOG.md:3301-3303` states `block22_refs 8` at A2 while
`LOG.md:3243-3245` states `block22_refs 7` at A1 in the same section, so the section is
internally inconsistent about a number it also calls identical.

**Fix.** Replace "the values are identical" with "the verdict and every clause outcome are
identical (`met_target true`, `failing []`, `frozen_path_changed []`); `block22_refs` rises
6 → 7 → 8 as A1 and A2 add citations." Same repair at `SCORECARD.md:3581` and `LOG.md:3316`.

### A2 — wave 2 had 36 seats, not 32; the cited results file does not exist

- `SCORECARD.md:3527-3528` — "Wave 1: 40 seats; wave 2: 32 seats (counts from
  `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`)."
- `LOG.md:3273-3274` — "wave 1 40 seats and wave 2 32 seats … read from
  `{r45-w1,r45-w2}-results.json`".

Ground truth at HEAD:

| source | value | receipt |
|---|---|---|
| `.ufo/waves/round-45/w2-dispatch.json` `counts` | `{"spawn": 36, "resume": 0, "total": 36}` | `receipts.json` #8 (exit 0) |
| `.ufo/waves/round-45/w2-spec.json` `items` length | `36` | `receipts.json` #8 (same invocation) |
| `.ufo/waves/round-45/r45-w2-results.json` | **absent** — `ls` exit 2 | `receipts.json` #9 |

The 32 is not a rounding of an in-flight file; it is contradicted by the only two wave-2
ledgers that exist, both committed at `faa875bc`. Wave 1 is consistent (spec 40, dispatch 40,
results 40; `receipts.json` #10), so the defect is specific to wave 2. The citation is also
structurally wrong for wave 2: `r45-w2-results.json` cannot be cited before wave 2 closes,
and at HEAD only `w2.ready` / `w2.ready.dispatched` exist.

**Fix.** "Wave 1: 40 seats (`.ufo/waves/round-45/r45-w1-results.json`); wave 2: 36 seats
(`.ufo/waves/round-45/w2-dispatch.json`, `counts.total = 36`; `w2-spec.json` has 36 items).
`r45-w2-results.json` is written when wave 2 closes and is not yet available."

### A3 — the reverse check: 8 of 12 round-45 commits in `FREEZE..main` are never cited

`git log f762b727..main` returns 12 commits, all self-labelled `round-45:` (`receipts.json` #0,
sha256 `c50ff054…`). The record cites four by hash: `e715263c` (landing), `1f4b27f8` (A1),
`fedd11bf` (A2), `f59565b7` (A3). Uncited:

| commit | subject | reflected in the record? |
|---|---|---|
| `9ff920cd` | wave-1 spec, dispatch, registry, do-nothing control receipts | evidence cited **by path** (`controls/*.json`), never by hash |
| `abfeda50` | first LOG/SCORECARD round-45 record + `*-at-1f4b27f8` receipts | it *is* the record's first version |
| `faa875bc` | wave-2 spec, dispatch, registry | **no** — and it is the ledger that refutes A2 |
| `14340d41` | A2 re-measurement record + A2 receipts | reflected in the A2 paragraph |
| `92b4970c` | mine M45-3, route R45-CL13/CL14 | lesson only (see below) |
| `1d04c6af` | A3 as measured revision + A3 receipts | it *is* the A3 record paragraph |
| `a63d109f` | route R45-CL17 | lesson only (see below) |
| `0ee50aaf` | land wave-1 record: 497 files, 25 report dirs, `w2.ready` | partially — no seat-report count |

Submission of the record does not require hashing every commit, and `1d04c6af` cannot cite
itself. The damaging part is not the missing hashes but that two uncited commits carry routed
defects that the two summary records then drop:

- **R45-CL13 / R45-CL14 are HIGH severity** (`corpus/lessons/round-45.md:142,160`) — the frozen
  C1 and C2 predicates are met on genuine bytes but are **not discriminators**. Yet `grep` counts:
  CL13 → LOG 0, SCORECARD 1 (a parenthetical), lesson 2; CL14 → LOG 0, **SCORECARD 0**, lesson 2.
- **R45-CL16** appears in LOG/SCORECARD only inside the A3 prose ("routes R45-CL15/CL16"),
  never in a routing list; **R45-CL17** (`a63d109f`) appears in **neither** `LOG.md` nor
  `SCORECARD.md` (lesson only, line 188).
- Both `planned (round 46)` lists (`SCORECARD.md:3562`, `LOG.md:3288-3292`) enumerate only
  CL6, CL7, CL3, CL2 and R36-CL5/R40-CL2/R41-CL3. The round's two HIGH items (CL13, CL14) and
  the two later HIGH items (CL15, CL17) are absent from the list that round 46 will actually read.

**Fix.** Add the eight commits to the round-45 record as a revision list (or cite them where
their content is used), and extend both `planned (round 46)` lists to carry CL13–CL17 with
severity. Until then the record's routing surface understates its own findings.

## Holds

### A4 — every token resolves; the one non-commit is correctly labelled
13 unique tokens. Seven distinct commit pins, all resolving and all ancestors of `main`:

| token | full commit | role | ancestry |
|---|---|---|---|
| `149133d4` (+40-char) | `149133d47aa7e90796f96047afe6d251a3e65b2c` | base | ancestor |
| `f762b727` (+40-char) | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | freeze | ancestor |
| `e715263c` (+40-char) | `e715263cb51b713c342ab992d527fe9d61d6f8ff` | landing | ancestor |
| `1f4b27f8` (+40-char) | `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` | A1 | ancestor |
| `fedd11bf` (+40-char) | `fedd11bf5ff9fe42d061169f78d77df59af4eca1` | A2 | ancestor |
| `f59565b7` (40-char) | `f59565b782c18b0eb691bec12f52d2f80d9f5032` | A3 | ancestor |
| `c86ea508` | `c86ea508188c50e2645b1f9bba65df4177cda6b1` | round-44 violating commit | ancestor |

Chain is linear and confirmed: base → freeze → landing → A1 → A2 → A3 (`merge-base
--is-ancestor` YES at each step). `git log --merges freeze..main` is empty (`receipts.json` #4),
which independently supports the record's statement that "the measured range contains no merge".

`34336cf7` is **not** a commit — `git cat-file -e 34336cf7^{commit}` fails and no object
disambiguates. It is the leading 8 hex of the stdout sha256
`34336cf79d729e6a85a3ac7a3eda998388011213f33aaa1cba2d8187fcefc7d3`, and the record labels it
as such (`corpus/lessons/round-45.md:18` "receipt sha256"; `:145` "receipt sha256"). The digest
matches `.ufo/waves/round-45/w1/R45W1CritC1/receipts.json` `/8/stdout_sha256` exactly, so the
citation resolves. **Verdict: holds** — classification note only: this seat's `cat-file` test
flags it because it is a content digest, not a revision pin; it is not an unknown hash.

### A5 — freeze is derivable and the freeze arm is clean
`git log --format=%H -1 -- plans/round-45-claims.md` → `f762b727…` (`receipts.json` #3, exit 0),
matching the claims file's own re-derivation rule. Over `FREEZE..main`:

- `git log --name-only --format= FREEZE..main -- plans/round-45-claims.md tools/round-45/` →
  empty, sha256 `e3b0c442…` (`receipts.json` #1)
- `git diff --stat FREEZE..main -- <both frozen paths>` → empty, sha256 `e3b0c442…` (#2)

So A2 and A3 are admissible revisions for both counters; the append-only amendments touched
`SKILL.md`, the lesson and the record, never the frozen bytes. The claims file's wording
"the commit that first contains this file and `tools/round-45/`" is loose — the directory was
first added at `8bb1090a` in round 44 — but the operative clause (first commit containing the
claims file) is exact, so the pin stands.

### A6 — block 22's shape at A3, parsed independently of the counter
Independent parse of `git show f59565b7:SKILL.md` (`receipts.json` #14):

- `^- \*\*` blocks inside `## Queue-drain craft`: **22** at A3, **21** at the base `149133d4`
- blocks containing `<!-- freeze-integrity-table v1 -->`: **1**
- header exactly `| trigger | arm | exit | receipt |`
- data rows: **10**; exit cells `1,1,1,1,2,1,2,2,0,0` — all in `{0,1,2}`
- 8 `path:line` references, all resolving; `S140` and `tools/round-45/frozen-path-preflight.py`
  both present in the block

(The counter's `rule_blocks 22` is reproduced exactly; an earlier naive split of mine printed 23
because it counted the section's prose segment — my artifact, not a defect, and withdrawn.)

### A7 — C1 and C2 predicates re-run at five revisions
`receipts.json` #15–#18 plus the scratch re-runs: at `e715263c`, `1f4b27f8`, `fedd11bf`,
`f59565b7` and `a63d109f`, both counters exit 0 with `met_target true`,
`frozen_path_changed []`, `failing []`; C2 reports `registered` = all six, `unregistered []`,
`thin []`, `scope_size 6`. The predicate is met at every pinned revision **and at HEAD**, so
the post-round commits do not disturb the score. What is false is only the record's description
of *how* the values compare (A1).

### A8 — registry rows and the A3 correction
At A3, `SKILL.md` carries exactly six rows whose first cell is a scope path (`SKILL.md:1652-1657`),
each exit cell naming `0`, `1` and `2`. The `tools/round-44/c1-run.sh` row carries A3's correction
verbatim — "it does not run the oracle (`c1-oracle.py` is the counter's)" and "`0` … or `--dry-run`
printed the plan and wrote nothing" — so the A3 amendment is present in the graded surface, not
only in the record.

### A9 — the preflight's claimed "before" state
`git show 149133d4:tools/round-45/frozen-path-preflight.py`: 107 lines (A3: 315), and `grep -c`
returns 0 for `selftest`, `restored`, `dirty` and `require-pathspec` (`receipts.json` #13; grep
exit 1 = no match). The claims file's "untested single-arm gate: no worktree arm, no pathspec
requirement for a directory freeze, and no restore classifier" is accurate at the base.

### A10 — the round-44 pin used as evidence
`c86ea508`: 432 paths (`receipts.json` #5), 8 of them under `tools/round-44/control-fixtures/`
(#6), author `2026-10-28 09:57:16 -0300` vs committer `2026-10-28 10:43:43 -0300` (#7). All three
facts match `corpus/lessons/round-45.md:16` exactly, wrecked-stamp pair included.

### A11 — source frontier
`corpus/SOURCES.md` rows: 139 at the base `149133d4`, 141 at A3 (`receipts.json` #11, #12) —
the record's "139 → 141" holds, and rows S140 (`git-status`) and S141 (`git-diff-tree`) are
present with their top URLs.

### A12 — wave-1 ledger
`r45-w1-results.json`: `seats` 40, 40 result entries, 15 with `output: null` (`receipts.json`
#10) — i.e. 25 producing seats, which matches the landing commit's "25 seat reports and dirs"
(`0ee50aaf`). The record's 40-seat wave-1 count holds. Note the results schema names the role
field `agent`, not `role`; the record's "role mix" is derivable from `agent`.

## Not run

- **S140/S141 top-URL re-fetch.** Out of this seat's pin scope; S141's quote word count was
  already refuted by a wave-1 seat and corrected in A2 (23 → 20), and A10/A11 verify what this
  seat can verify offline. A live fetch would not change any pin verdict here.
- **Direct execution of the preflight's `dirty`/`restored`/`blob` arms.** Covered by wave-1
  seats and already routed as R45-CL15/R45-CL16 (arm-covering but not arm-isolating;
  `--dirty-pathspec` false-clean). Re-running them would restate a known open item, not test a pin.
- **Command A / the depth-coverage proxy end to end.** Outside the pin set; its two inputs that
  are checkable here (craft block count A6, SOURCES count A11) both hold.

## Drift note for the L1

The brief pins "amendment A1 `1f4b27f8` (the measured revision)". The record at HEAD says the
round's measured revision is **A3** (`SCORECARD.md:3590`, `LOG.md:3315`) and calls A1 "the first
met measurement". All three anchors in the brief (freeze, landing, A1) resolve and are ancestors,
so nothing in A4 changes; but the brief's pin set predates A2/A3 and should be re-read against
HEAD before the round is closed.

## Receipts

`.ufo/waves/round-45/w2/R45W2Pins/receipts.json` — 19 entries. Decisive ones:

| # | command | exit | stdout sha256 |
|---|---|---|---|
| 0 | `git log --format='%H %s' f762b727..main` | 0 | `c50ff054…` (12 commits) |
| 1 | `git log --name-only --format= f762b727..main -- plans/round-45-claims.md tools/round-45/` | 0 | `e3b0c442…` (empty) |
| 2 | `git diff --stat f762b727..main -- <both frozen>` | 0 | `e3b0c442…` (empty) |
| 4 | `git log --merges --oneline f762b727..main` | 0 | `e3b0c442…` (empty) |
| 5 | `git show --name-only --format= c86ea508 \| wc -l` | 0 | `fd8584da…` (432) |
| 6 | `… \| grep -c tools/round-44/control-fixtures/` | 0 | `aa67a169…` (8) |
| 8 | `w2-dispatch.json counts` + `w2-spec.json items` | 0 | `5daf1830…` (36 / 36) |
| 9 | `ls .ufo/waves/round-45/r45-w2-results.json` | 2 | `e3b0c442…` (absent) |
| 10 | `w1-results seats / len / null outputs` | 0 | `4b7c3ef1…` (40 / 40 / 15) |
| 13 | `git show 149133d4:…preflight.py \| grep -c selftest` | 1 (no match) | `9a271f2a…` (0) |
| 14 | independent block-22 parse at f59565b7 | 0 | `2c32655f…` (22/1/10) |
| 15–18 | `c1-counter` / `c2-counter` at e715263c and f59565b7 | 0 | `cb869305…`, `a292755a…`, `90597e61…`, `a352f65c…` |

Scratch `/fast/scratch/hyaku/kaidoku-r45/R45W2Pins` removed after copying these receipts.
