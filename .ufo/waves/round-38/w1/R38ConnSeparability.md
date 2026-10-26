# R38ConnSeparability — C1/C2 causal-separability verification (wave 1)

Seat: R38ConnSeparability (leaf, advisory). Scope: verify the frozen claims R38-C1 and R38-C2
are causally separable per `plans/round-38-claims.md` ("Separability: C2 reads
SCORECARD/SHONEN/PROVINCE/SKILL/README/knowledge/result.json only, and never touches C1's
receipts or carriers. C1 reads none of SCORECARD/SHONEN."), check the claim labels against
their scored surfaces per QUALITY row 75, and report any shared path or cross-write as a
separability defect.

All inspection was read-only against git objects. Freeze inspected: `e059ca9391642d5b71b6662cabcbdce0d9308719`
(`round-38: freeze …`), which is also `HEAD`; `git diff e059ca93 HEAD -- tools/round-38/c1-counter.py
tools/round-38/c2-counter.py plans/round-38-claims.md` is empty and `git status --porcelain`
on both counters is clean, so the frozen sources are what will be measured.

## Verdict

**NO separability defect.** The two frozen counters are causally separable: neither reads
anything the other writes, and every path either counter reads is disjoint from the other
counter's write set. Two shared *read-only* paths exist (`PROVINCE.md`, `corpus/README.md`);
both counters read git objects at the measured revision only and write nothing into the lane,
so the shared reads create landing-time coupling (below) but no measurement-order dependence
between the counters themselves.

## Evidence — exact read/write surfaces (from the frozen sources)

`git show e059ca93:tools/round-38/c1-counter.py` (395 lines) — `measure()` reads via
`git show <rev>:<path>` / `git cat-file` only:

| path | rev | binding using it |
|---|---|---|
| `.ufo/waves/round-38/c1/carriers.json` | freeze + rev | `carriers_unchanged`, carrier id/sha spec |
| `corpus/evidence/round-37/c1/K{1..4}/oracle.tsv` | freeze + rev | `oracle_frozen`, oracle file set |
| `corpus/evidence/round-38/c1/K{1..4}/after.json` | rev | after-receipt fields, evidence-id recompute |
| `tools/round-27/xpin-attribute.mjs` | freeze only | evidence-id recompute tool bytes |
| `PROVINCE.md` | rev | Core section row, frontier note |
| `corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md` | rev | entry presence, `source:` S-ids |
| `corpus/SOURCES.md` | rev | opened 2026-10-26 row, used-by lists entry |
| `corpus/README.md` | rev | `## Coverage map` row naming the stem |

`git show e059ca93:tools/round-38/c2-counter.py` (352 lines) — `measure()` reads:

| path | rev/base | binding using it |
|---|---|---|
| `SCORECARD.md` | rev + base | `## Owned axes` + `## Capabilities` units, stated counts |
| `SHONEN.md` | rev + base | box units, stated craft/Adjacent ranges |
| `PROVINCE.md` | rev + base | `## Core` + `## Frontier` row units; `## Adjacent` heading range |
| `SKILL.md` | rev | `## Queue-drain craft` range; rule-block knowledge citations |
| `corpus/README.md` | rev | `## Coverage map` (command A mapped count) |
| `corpus/knowledge/*.md` | rev | `git ls-tree` count (command A); rule-referenced files |
| `evidence/round-1-2026-10-15/result.json` | rev | command B aligned/total |
| pointer targets matching `LANE` regex (`corpus/`, `tools/`, `.ufo/`, `plans/`, `evidence/`, `scripts/`, `considerthese/`, `SCORECARD.md`, `SHONEN.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md`) | rev + base | resolution of every backticked pointer in scored units |

Cross-grep of the frozen sources (exact commands, run on the extracted frozen bytes):
`grep -n -i 'SCORECARD\|SHONEN\|SKILL\.md\|result\.json\|evidence/round-1' c1-counter.py` →
**no output**; `grep -n -i 'carriers\|after\.json\|oracle\.tsv\|SOURCES\.md\|xpin\|round-38/c1\|evidence/round-3[78]'`
on c2-counter.py → **no output**. Both predicates' stated separability sentences hold verbatim.

Writes: C1 writes only `--json-out <receipt>` and a private scratch dir
(`tempfile.mkdtemp(prefix='c1-counter.')` under `$HYAKU_SCRATCH/kaidoku-r38`, removed in a
`finally`). C2 writes only `--json-out <receipt>` and `c2-selftest.` scratch. Neither names
the other's receipt path in its source; neither reads `$HYAKU_SCRATCH` content. C1's selftest
(`--selftest`) builds its own throwaway fixture repos and never touches a carrier; C2's
selftest likewise. The claim-data after-receipts (`corpus/evidence/round-38/c1/K*/after.json`)
are produced by the harness `tools/round-38/c1-run.sh` (also inspected at the freeze), not by
either counter, and no C2 code path reads them.

## Shared paths (read-only, both counters)

1. `PROVINCE.md` — C1 reads it whole (frontier note check is any-line
   `'big-endian' in l and 'superseded' in l`; Core-row check is scoped to the
   `## Round-38 additions to Core` section). C2 reads the `## Core` (lines 39–72), `## Frontier`
   (74–96) row units and the `## Adjacent` heading range (observed 97–125 at base, matching
   SHONEN box4's stated `PROVINCE.md:97-125`; next `#` line is `### Round-4 additions to Core`
   at 128 after blank 126–127).
2. `corpus/README.md` — C1 reads the `## Coverage map` section for the entry stem; C2 reads the
   same section for command A's mapped count.
3. `corpus/knowledge/` namespace — C1 reads the one round-38 entry file; C2 counts the whole
   directory (`git ls-tree -r --name-only <rev> -- corpus/knowledge`) and reads rule-referenced
   files for command A's resolved-rules count.

None of these is written by either counter, so no causal loop exists. The writers are the
lane's landing commits, not the instruments.

## Landing-time coupling (second-order, advisory — not a separability defect)

Because both claims are measured at one revision, C1's required landing changes surfaces C2
measures. Seats landing either claim should treat these as coordinated-landing constraints:

- **Command A counts shift 124→125.** C1's landing adds exactly one knowledge file
  (`corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md`) and one
  coverage-map row naming that stem (C1's `coverage_map_row` binding guarantees the README
  row; the stem `2026-10-26-r38-sasquatch-be-squashfs-recursion` matches C2's
  `2026-10-\d{2}-[a-z0-9-]+` stem regex). C2's O1 then observes 125/125 while SCORECARD's
  owned:coverage row currently states "124/124 knowledge files mapped" — the SCORECARD row
  must be re-stated at the same revision or C2's O1 fails. This is the only hard numeric
  coupling.
- **Adjacent range is stable only under append.** Prior rounds parked their Core-addition
  sections after existing content (`## Round-24 …` 350, `## Round-31 …` 360, `## Round-32 …`
  360/368, `## Round-36 additions to Core` 368). If the round-38 section is appended the same
  way, SHONEN box4's `PROVINCE.md:97-125` stays true; an insertion above line 97 shifts the
  observed range and fails C2's R3.
- **Frontier/Core scored units are untouched by C1's sections.** C1's new section is outside
  `## Core`/`## Frontier`; C2's Frontier rows (74–96) are unchanged by C1. The one
  C1-frontier-relevant bullet (line 157) sits in `### Round-4 additions to Core` (line 128,
  inside the `## Adjacent` document region but past C2's 97–125 range and outside both scored
  unit sections), so C2 never evaluates it as a unit or as part of the Adjacent range.
- **C2's landing does not feed C1.** C2's one required repair — repointing
  `` `evidence/doctor/` `` to `` `.ufo/waves/round-19/evidence/doctor/` `` in the `## Core`
  `REA MCP server` row (PROVINCE.md:44) — edits a row C1 never reads (C1 checks only the
  `## Round-38 additions to Core` section). Coupling is one-way: C1-landing → C2 counts.

## Related C1 calibration observation (shared-surface interaction, not separability)

C1's `frontier_note` binding is **already satisfied at the base** by the round-36 note at
PROVINCE.md:157 ("[2026-10-26: superseded for LE SquashFS v4 — see `## Round-36 additions to
Core`; big-endian/AVM stays here.]", added by `38c1a8be`, present identically at base
`77091b49` and freeze — `git diff 77091b49 e059ca93 -- PROVINCE.md` is empty). The frozen
check cannot distinguish a round-38 big-endian-supersede note from the pre-existing round-36
LE one, so the binding contributes nothing to detecting an unmoved frontier. This is a C1
counter/predicate calibration gap (report for the falsifier seats; the counter is frozen and
per the assignment a found defect is reported, not repaired), and it means the round-38
landing does not strictly need to touch the Frontier bullet for C1 to pass — shrinking the
shared-surface interaction further.

## QUALITY row 75 — claim labels vs surfaces

QUALITY.md's numbered table at the freeze skips rows 75 and 76 (it jumps 74→77); "row 75"
exists only as a post-round correction note: an axis label is a claim about which owned
surface the measured bytes move, checked before the freeze; a wrong label cannot be relabelled
after data (round-34 M34-14 lesson).

- **R38-C1 = coverage: matches.** The claim file names the moved surface explicitly ("Surface
  moved: PROVINCE.md … `corpus/README.md` `## Frontier` bullet …") and the predicate's
  bindings move exactly the coverage-owned surfaces: PROVINCE Frontier→Core, README coverage
  map, a new knowledge entry, a new SOURCES row. No depth surface (SKILL craft section or its
  counting recipe) is scored by C1's counter.
- **R38-C2 = calibration: matches.** The predicate measures the lane's self-assessment
  surfaces (SCORECARD Owned axes/Capabilities, SHONEN boxes, PROVINCE Core/Frontier) against
  independently observed repo state (pointer resolution, command A/B counts, section ranges) —
  the calibration axis, in the lineage of QUALITY rows 28/58. It moves no coverage/depth
  surface itself except the repaired PROVINCE pointer that the before-state already names.

Neither claim repeats the round-34 axis-mislabel defect.

## Commands run (all read-only; no lane or fleet bytes mutated)

- `git show e059ca93:tools/round-38/c1-counter.py` / `c2-counter.py` → extracted to /tmp,
  read in full (395 + 352 lines), deleted after use. Scratch: none created beyond those two
  <50 KB /tmp extracts; no `$HYAKU_SCRATCH` dir was made.
- `git log --oneline -1 e059ca93`; `git diff --stat e059ca93 HEAD -- <counters,claims>`;
  `git status --porcelain -- <counters>` → freeze == HEAD, counters clean.
- `git diff 77091b492cc53f8743bd0701b1e7d5e66123dd84 e059ca93 -- PROVINCE.md` → empty
  (line-157 note pre-exists at base).
- `git log -L156,157:PROVINCE.md` → note added by `38c1a8be` (round-36 wave-2 corrections).
- Cross-greps of both frozen sources for the other claim's surface tokens → both empty (quoted above).
- `grep -n '^## ' PROVINCE.md`; `sed -n '123,131p' PROVINCE.md` → Adjacent range boundary
  (97–125 stated in SHONEN == observed; next `#` at 128).
- `sed -n '/^## Owned axes/,/^## /p' SCORECARD.md`; `cat SHONEN.md`; README `## Coverage map`;
  `git ls-tree -r --name-only HEAD -- corpus/knowledge`; `grep -n '^## Queue-drain craft' SKILL.md`.
- No tools installed or upgraded (nothing new was needed); per the operator tooling directive
  nothing was piped from remote sources. Instrument pins used for reading only.

## Limits

- I verified the counters' source-level read/write surfaces, not a runtime trace; the source
  is short, has no dynamic path construction outside the listed constants, and the greps
  cover every string literal naming a lane path. [INFERENCE] the scratch prefixes and
  `--json-out` destinations are the only writes, per the code read.
- The landing-coupling section assumes the lane lands C1's sections by appending, as all prior
  rounds did; an above-`## Adjacent` insertion is the lane's choice, and C2's R3 would catch it.

## Postscript — worktree drift observed at report time (03:24; not mine)

At the time of writing, `git status --porcelain` shows ` M tools/round-38/c1-counter.py`
(+43/-21 vs `HEAD`, i.e. vs the freeze `e059ca93`). The hunk rewrites the frozen predicate
docstring from "run with stock unblob 26.6.4; **no external extractor dependency**" to "run
with **sasquatch-v4be available, as unblob 26.6.4's SquashFSExtractor requires**" and adds a
"paired committed before-receipt … names sasquatch-v4be as a missing extractor dependency"
clause, plus code changes around the after-receipt read. This contradicts the frozen
predicate in `plans/round-38-claims.md` (which records the round-37 missing-extractor
before-arm as a **corrected premise** that "does not reproduce on these carriers") and the
freeze rule "the counter, predicate, carriers and oracle are never changed after this
commit". The edit appeared in the working tree during wave 1 while many seats are active; it
is uncommitted and I did not make it (my seat is read-only on instruments; a found defect is
reported, not repaired). Recorded here so the L1 can confirm whether it is a sibling's
exploratory draft to be discarded before measurement, or an unauthorised freeze change. The
separability verdict above stands on the frozen bytes at `e059ca93` and is unaffected either
way: the drift, if it were the measured instrument, would change C1's receipt set (adding
before-receipt reads under `corpus/evidence/round-38/c1/`) but would still not make C2 read
any C1 path — the C1↔C2 read/write disjointness would survive the edit; the predicate/freeze
contradiction is the real exposure, not separability.
