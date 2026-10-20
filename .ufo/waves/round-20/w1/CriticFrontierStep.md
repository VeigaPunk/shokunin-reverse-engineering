# CriticFrontierStep — attack on the round-20 frontier step

Target: `claims.json:42` `frontier_step` (SOURCES rows C2-sourced; census before/after;
mined mistake round-19 D1 → `corpus/lessons/round-20.md ## Mistakes`) against
`/home/vgpnk/Projects/shokunin/CORPUS.md:64-148` (SOURCES contract v1, frozen).

Commands run (all exit 0 unless noted):
- `git rev-parse refs/heads/main` → `d1d981d2cc…` (post-baseline; baseline `14f0260` is
  refs/heads/main at dispatch per `contract.md:4`)
- `grep -nE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | wc -l` → `39` (rows S001–S039)
- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` →
  `kaidoku W04 S033 duplicate url … ; kaidoku ok`, exit 0 (warnings are non-fatal)
- `git status --porcelain --ignored -- .ufo/waves/round-19` → still lists
  `?? …/scratch-custody/custody-pair-selftest-k_zd4w5n/{repo-fixture,repo-sub-fixture}/`
- `grep -n "scratch|selftest|worktree|residue" corpus/QUALITY.md` → no matches

## F1 (calibration) — the frontier step is uncounted and unmeasured

OBSERVATION: `claims.json:42` writes `frontier_step` as prose. Unlike C1–C3 it has no
`falsified_if` and no counting command. The only related counters are
`verb-coverage.py` (commands named in entries + `ev_` + existing evidence path —
`gen-wave1.py` VerbCoverageTool spec) and `routed-r19.py` (D-items). Neither counts:
(a) new SOURCES rows, (b) their conformance, (c) `used-by`/`mined` linkage to the new
entries, (d) the `## Mistakes` row. So a wave where all five rows are malformed, all
five `used-by` cells dangle, and the Mistakes row is fabricated still reports C2
green — `falsified_if` (`claims.json:30`) only requires "an entry with retained run
evidence" for ≥3 verbs, and says nothing about the mined-row clause in
`claims.json:25`.

INFERENCE: this is the deepest defect — the frontier step exists only in prose; the
judge has no instrument to fail it. Smallest correction: extend `verb-coverage.py`'s
`exercised` check to also require the naming entry's `source:` line cite an `S###` row
whose `status` at REV is `mined` and whose `used-by` at REV contains the entry's path;
and add a frontier-step conformance item to `routed-r19.py` or the final census.

## F2 (coverage) — `## Gate` obligations for new rows have no seat

OBSERVATION: SOURCES rule 1 (CORPUS.md:112-115) requires the round lesson's `## Gate`
to record, per new row, the URL, access date, and a ≤25-word located quote; and rule 2
(:116-118) requires every in-place `status`/`used-by` change be logged old→new in the
lesson. Wave-1 assignments (`wave1-assignments.json`) cover row drafting
(`SourceWabtRelease`, `SourceRizinDocs`, `SourceHarmonyDocs`, `SourceWasmSpec`,
`SourceGo1246`, `SourceObjdumpDocs` — all `status queued` per `gen-wave1.py:43-48`),
`## Mistakes` drafting (`DraftLessonMistakes`), and registry review
(`ReviewSourcesRegistry`). No seat drafts the `## Gate` quote table, the
queued→mined old→new log, or the search-log note (rule 5, :126-128). In round 19 the
Gate held exactly this (`corpus/lessons/round-19.md:20-51`, used-by old→new at :143-148).
INFERENCE: L1 must integrate it, but nothing in the plan checks it; a lesson without
`## Gate` is itself a known fleet defect class (M089, CORPUS.md:178). Correction:
extend `DraftLessonMistakes`/`DraftCoverageRows` scope or add the Gate to the L1
integration checklist with the census as witness.

## F3 — what makes a row non-conformant (attack surface the plan exposes)

Mechanical (census-checkable, CORPUS.md:133-148): NF≠13, `|` inside a cell, reused id,
enum violations (kind/tier/status), `community` at tier A, `mined` row whose `used-by`
paths don't exist. The plan's own failure modes:

1. **Placeholder `S0NN` → collision or reuse.** `gen-wave1.py:46` ships drafts with
   `S0NN`; claims.json:24 says ids "assigned at integration". Two scribes reporting
   overlapping drafts or an L1 renumber that hits S040 twice → duplicate-id row.
   Baseline shows the real risk: S032/S033 already triggered W04 duplicate-url.
2. **`mined` written before `used-by` target exists.** If a row lands `mined` in a
   commit where the knowledge entry isn't yet tracked, the used-by-existence census
   (:146-147) reads the working tree — at a REV measured earlier than integration the
   row is conformant-or-dangling depending on order. Rows must land `queued` and flip
   `mined` only with the citing entry; the flip is an in-place change needing the
   old→new log (rule 2) — see F2.
3. **Duplicate URL, different scope.** `SourceGo1246` targets
   `https://go.dev/dl/?mode=json&include=all` — the exact URL S038 already registers
   for go1.25.0 (`SOURCES.md:44`). Contract permits it (scoped tier), but census W04
   will warn; the integration must declare it like round 19 did (`spotcheck:165-167`),
   not let it surface as a surprise.
4. **Bare-homepage anchor.** `SourceHarmonyDocs` offers `gitee.com/openharmony/docs`
   or a developer.huawei.com portal (`gen-wave1.py:541-543`); a repo-root URL without
   "exact section/heading/page/line plus revision" violates :99-100. Same risk for
   `SourceRizinDocs` citing `book.rizin.re` wholesale.
5. **`opened` format.** Contract asks ISO *date* (:105); SRC spec asks scribes to log
   `date -Iseconds` access time (`gen-wave1.py:44`). Datetime-in-`opened` is a
   foreseeable non-conformant cell.
6. **Semantic non-conformance the census cannot see**: fabricated/wrong-location
   quote, `teaches` not grounded by the anchor, tier A for a source that isn't primary
   *for that scope*, `recheck` claiming `on-release` for an immutable document
   (WasmSpec — the HTML spec has no release cadence; a wrong cadence is dishonest
   metadata). Only rule-1 re-opening catches these; assign it or it won't happen.

## F4 — what makes the "sourced" claim hollow

C2's statement (`claims.json:25`) requires each entry to cite "a mined SOURCES row".
Hollowness modes, by strongest counterexample first:

- **Source doesn't cover the claim scope.** The six scribe sources are upstream docs
  for the *underlying* tools/formats (WABT release assets, rizin book, binutils
  manual, Wasm spec, HarmonyOS docs, go.dev JSON). But the C2 entries' claims are
  about what *rea-agents@6.5.0* does. A row can be tier-A and still not support the
  entry — e.g. the binutils manual documents `objdump -i`, not what
  `list-objdump-architectures` returns (REA runs objdump with its own argv; that fact
  lives in the revenger output / run receipt, not in any SOURCES row). The honest
  pattern from round 19 is dual-citation: `source:` names both the S### row (scoped to
  what the source actually teaches) and the retained receipt/evidence. If any entry
  cites only the S### row for a REA-behavior claim, the sourced claim is hollow —
  tier inflation by scope (CORPUS.md:96-97: "A: primary *for that scope*").
- **`queued` row cited as if mined.** Rule 4 (:123-125): expansion counts only
  entries citing a `mined` row. If the L1 integrates entries while rows stay
  `queued`, C2's "mined SOURCES row" clause fails even though the counting tool
  passes (F1).
- **`used-by` written but entry lacks the provenance trio.** CORPUS.md:163-170
  requires `source:`/`verified-at:`/`recheck:` first; an entry citing S0NN in prose
  only is freshness-sweep-invisible — a repeat of a documented fleet defect.

## F5 — what makes the mined mistake's fix unfalsifiable (D1)

OBSERVATION: the D1 residue is real and still present in the working tree
(`git status --porcelain --ignored` output above; `spotcheck:180-181`). The fix
interface (`contract.md:38-40`) is *refusal*: exit 2 `scratch_inside_worktree` when
`--scratch` is inside a worktree. But "a fix is shown able to fail" (CORPUS.md:179-184)
demands a red-before where "the same command exits non-clean for the named reason,
with the fix as the only delta".

- **No command can produce the strict red-before.** Pre-fix,
  `custody-pair.py selftest --scratch <in-worktree>` runs the whole selftest and
  exits 0 (it never refuses); the residue is a post-condition, not a non-clean exit.
  The only honest red-before artifact is (a) pre-fix run + residue-sweep output
  (`git status --porcelain --ignored` or `find` for nested `.git`), or (b) the
  *new* refusal probe run against the *old* tool bytes at REV `14f0260` showing the
  missing refusal. If the lesson claims "selftest exited non-clean before the fix",
  it's fabricated — the pre-fix selftest exits 0. The `## Mistakes` row must name
  which artifact is the red-before; `DraftLessonMistakes` is explicitly told to
  state this (`gen-wave1.py:560-562`) but nothing verifies the claim.
- **`captured-by` is `none` — and nothing fixes that.** `QUALITY.md` has no
  scratch-hygiene criterion (grep above). The fix adds a tool refusal but no
  QUALITY row captures the *class* (selftest residue inside the lane). This is the
  documented failure mode: "prose-only lessons did not hold: C01, C02, C07 and C10
  recurred after capture" (CORPUS.md:176-178). The two drafted QUALITY rows
  (`DraftQualityRows`, `gen-wave1.py:564-567`) cover D2 (timestamps) and D3
  (carrier exec) — not D1. INFERENCE: D1 without a capture criterion is the mined
  mistake most likely to recur; smallest correction is a #25 row or a stated
  rationale for `captured-by: none` beyond "no row exists".
- **Class misfit risk.** The §5 vocabulary (:174-176) has no residue/hygiene class.
  `landing` (C09: "marker, missing SHONEN, placeholder, overwrite") is the nearest,
  but untracked fixture residue is not an evidence-landing defect. A row that
  force-fits `landing` without justification, or invents a class, is non-conformant
  in opposite directions; the draft should defend the pick.
- **`--live` sweep is lane-state-dependent.** The D1 substance check
  (`gen-wave1.py:66-68`) greps `git status --porcelain --ignored` under `LANE/.ufo`
  — but the r19 residue is still there. If nobody removes the two untracked fixture
  dirs, the `--live` check fails at integration for an unrelated leftover; if a
  seat deletes them, that's a lane write the contract reserves to the L1. Either
  way it's a sequencing dependency no seat owns.

## Impacted axes & smallest safe corrections

- calibration — F1: no counter can fail the frontier step. Extend `verb-coverage.py`
  `exercised` (mined+used-by linkage) and route a SOURCES-conformance + Gate check
  through `routed-r19.py` or the final census record.
- coverage — F2/F5-last: `## Gate` quote table, old→new log, search-log note, and the
  in-worktree residue cleanup have no owner; assign or the step is partial by
  construction.
- depth — F4: scope each new row to what its anchor teaches and require entries to
  dual-cite S### + receipt; single-source tier-A claims about REA behaviour are
  hollow. F5: name the red-before artifact class honestly (refusal-probe-vs-old-bytes
  or residue-sweep), and either add a QUALITY capture row for selftest-lane-residue
  or justify `captured-by: none`.
