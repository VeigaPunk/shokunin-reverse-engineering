# R44CritC2 — adversarial review of R44-C2 (draft + rubric design)

Seat: `R44CritC2` (critic). Scope: `plans/round-44-claims.md` §R44-C2 (calibration rubric,
controls, landing mechanics, frozen paths, separability) plus the w1-spec C2 seats
(R44C2Rubric / R44C2Counter / R44C2Controls / scouts). Not reviewed: R44-C1 mechanics
(R44CritC1's lane), except where C1 touches C2's frozen paths — which turns out to be
the strongest defect found here (F1).

## Verdicts up front

| # | Question assigned | Verdict |
|---|---|---|
| A1 | Is a 0-mismatch census at base an automatic honest stop — and is it run before the freeze? | **Yes in mechanism, no in reliability.** Scheduled pre-freeze (draft `Red-before controls`, CTL-C2-0 = frozen counter scored at `--rev BASE`; both counters must be dry-run before the freeze per the freeze-integrity rule). But the verdict rides on an un-frozen, single-author census and an unguarded BASE..FREEZE gap. See F2. |
| A2 | Can the seeded-mismatch control be gamed? (corrupt something NOT in the rubric → caught?) | **In-rubric corruption is caught; out-of-rubric corruption is structurally uncatchable** — and the draft already discloses this. The live holes are subtler: the drop-list is a laundering channel, and the control doesn't test attribution. See F3. |
| A3 | Does re-deriving catch a wrong count, or can check and file drift together? | **Re-derivation catches it for pure count checks, but three self-reference channels remain open**: (i) a check argv may read its command out of the file under test; (ii) the appended-repair note is free text the check re-reads; (iii) verdict-vs-receipt checks (category e) read mutable receipt files unless pinned. See F4. |
| A4 | Is `planned (round N+1)` vs "what N+1 worked" decidable? | **Not decidable as specified — this is the weakest rubric entry.** Evidence below: a missing `## Round 37`, duplicated `## Round 34`/`## Round 25` headings, steer markers embedded *inside* the planned line itself, and method-constraints that N+1 demonstrably violated. Exact hardening check in F6. |

## Pre-freeze census evidence (my own read-only probes, seat `R44CritC2`)

Commands run against lane `fc5eb54a` (base `c29360e3`; `git diff --stat c29360e3..HEAD` shows
the only base→HEAD changes are `plans/round-44-claims.md` and `.ufo/waves/round-44/w1*` —
no C2 rubric-target file moved).

- Command A (SCORECARD `## Measurement recipes` A verbatim) at `c29360e3` and at `fc5eb54a`:
  `{"mapped":137,"knowledge_files":137,"missing":[],"dangling":[],"citation_resolved_rules":21,"rule_blocks":21}`,
  exit 0, stdout sha256 `9c927a9b240ff98af32750fd8cb6b7be4cc1edf9af69866a6e47427ffdbf6400` (normalized).
  → Rubric categories (b) headline numbers and (f) map-row-vs-file count are **clean at base**.
- Capability `Evidence pointer` cells: all 22 path pointers I extracted resolve (categories a clean).
- `## Round <N>` sections: **no `## Round 37`** exists; `planned (round 37)` at SCORECARD:3400.
  `## Round 34` appears **twice** (:3328 and :3352 "run-6 re-dispatch"); `## Round 25` plus
  `## Round 25 attempt 3` (:2948, :3057). Nine `planned (round` rows total; rounds 37 absent,
  round 44 is current.
- Round-43 claim-table verdicts vs cited receipts: `c1-at-77d196c6.json` `{exit_code:0,
  met_target:true, matched:78}` ↔ verdict "met" ✓; `c2-at-77d196c6.json` `{exit_code:1}`
  ↔ verdict "not met" ✓. Category (e) spot-checks clean on the two rows sampled.

So the base is NOT a guaranteed mismatch-free census: the round-37 dangling plan is a real
in-scope statement whose verdict depends entirely on how the fuzzy category-(d) check is
written (F6) — and there are further latent mismatches the fuzzy check will classify
inconsistently (r25 method-constraint, r36/r38 counter-successor bundle, r38 stub-counter
disclosure).

## F1 — STRONGEST DEFECT: C1's landing breaks C2's frozen-path walk (cross-claim coupling)

The draft's `## Separability` claims C1 and C2 "share only `corpus/README.md` … and
`corpus/SOURCES.md`" and that C2's rubric tolerates this. Walk the mechanics instead:

1. `## Frozen paths` freezes `corpus/README.md` **and** `corpus/SOURCES.md` byte-for-byte
   (draft :217-219) "frozen to pin the statement text the rubric checks".
2. The freeze-integrity rule (draft :21-24): "no commit in `FREEZE..REV` touches a frozen
   path of that claim … M/D/R/T/U are changes". An **M is an M** — appending rows is a
   touch. There is no "appends allowed" clause for plain freeze walk; the only carve-out is
   C2's own `expected_edit`-bound repair path (draft :230-233 and the c2-counter spec:
   "appended C2 repair notes are allowed ONLY … only as an appended dated block whose diff
   the rubric's `expected_edit` clause binds").
3. C1's landing inserts a coverage-map row mid-table into `corpus/README.md` (C1 predicate
   draft :37, :76) and appends S138/S139 into `corpus/SOURCES.md` (:37, :77). The README map
   row is an insertion inside `## Coverage map`, not even an EOF append.
4. Therefore at any `REV` where C1 has landed, C2's `frozen_path_changed` is non-empty →
   exit 2 → `met_target` unreachable. Conversely if C2 scores first, C1's own predicate is
   unaffected (C1 doesn't freeze README's byte blob — its binding is the presence of the
   Round-44 row).

The "tolerance" the draft asserts exists only at the *rubric-entry* layer ("the row count
check … reads the count at REV, not a frozen integer", :183) — **but the freeze-integrity
walk operates on file bytes, not rubric semantics**. A check that tolerates a changed file
is worthless when the score itself refuses to evaluate. The only current escape is
*ordering*: score C2 at a REV before C1's README/SOURCES commits land. The draft nowhere
says this; if the L1 lands C1's documentation first (the natural order — C1's measured
revision is its landing commit), C2 becomes permanently unmeasurable for the round, and a
"2 never counts" exit means the claim can neither pass nor honestly stop.

Note the asymmetry: C2's *own* repair path was designed for exactly this (named-path,
diff-bound relaxations), and C1's shared-file deltas are deterministic at freeze time —
the map-row stem `2026-10-28-r44-squashfs-v1v2-core` and the S138/S139 row ids are already
decided in the draft.

**Impacted axes:** calibration (claim may be unmeasurable), coverage (ordering dependency
couples C1's landing discipline to C2).

**Smallest safe correction:** extend C2's `expected_edit` clause to name C1's two shared-file
deltas as *alternates*: `corpus/README.md` may differ at REV by either (a) an appended dated
C2 repair block, or (b) exactly the insertion of a `## Coverage map` row whose first cell
contains `2026-10-28-r44-squashfs-v1v2-core` (row-identity check over the inserted block,
not numstat — the M43-2 lesson); `corpus/SOURCES.md` by either (a) the C2 note or (b) exactly
the appended S138/S139 rows. Declare in the plan text: "C2 measurable at REV with or without
the C1 landing; any other delta to these two files re-reds." Do NOT solve it by ordering
silence — order-dependent measurability is a hidden coupling, exactly what the separability
section claims absent.

## F2 — The honest-stop check runs pre-freeze, but the census is a single point of failure

Mechanism check: the draft does schedule the census before the freeze — wave-1 seats
R44ScoutCalib/R44C2Readme/R44C2Shonen/R44C2Plan enumerate statements at the base,
R44C2Rubric freezes `asserted` + verdicts, and CTL-C2-0 = "counter at the freeze scores
the base and exits non-zero iff mismatches > 0". If the frozen rubric records 0 mismatches,
the counter exits 0 at base → the kill rule fires → honest stop. The wiring is real.

Two reliability holes:

**(a) Enumeration completeness is un-frozen.** The rubric only checks the statements its
authors enumerated. Under-enumeration manufactures a false honest stop; over-enumeration of
already-broken statements manufactures a live claim on noise. The seat prompts partially
deputize this (R44C2SentReview is assigned union-completeness review — good), but the draft
binds nothing into the frozen artifact. Worse: the R44C2Rubric prompt's "drop any statement
whose value cannot be re-derived mechanically (record dropped ids + reason)" is a **laundering
channel** — a statement whose base verdict is `mismatch` can be dropped as "not mechanically
re-derivable" and never reaches the census count. Dropped-with-verdict-mismatch = silent
disposal of the very signal the claim exists to repair.

**(b) The BASE..FREEZE gap is unguarded.** Census `asserted`/`line_at_base` are captured at
`c29360e3`; the freeze commit's parent will be later (currently `fc5eb54a`). Any edit to
SCORECARD/SHONEN/README between the census commit and the freeze makes the frozen
`line_at_base`/`asserted` strings stale — the counter then either mis-parses (exit 2 DoS)
or worse, a moved statement passes a `line_at_base` text-equality check on the *wrong* line.
The frozen-path rule only covers `FREEZE..REV`, never `BASE..FREEZE`.

Also: "the frozen rubric's mismatch count equal to the frozen value" (draft :128) is an
**aggregate-count** gate — a counter that reports the right count with the wrong per-ID
vector passes CTL-C2-0. Kill decisions need per-ID fidelity, not arithmetic.

**Impacted axes:** calibration.

**Smallest safe correction:** (i) `c2-rubric.json` gets a frozen `census` block: for every
enumerated OR dropped statement `{id, file, line_at_base, verdict_at_base}`; entries whose
`verdict_at_base == 'mismatch'` may not be dropped without a named `not-checkable-because`
reason reviewed at freeze. (ii) A freeze-gate step: re-derive every `asserted` string at
`FREEZE^` (the freeze parent) and require byte-equality with the frozen `asserted`; a moved
statement is a freeze blocker, not a silent stale pin. (iii) CTL-C2-0 compares the per-ID
verdict vector, not the count.

## F3 — Seeded-mismatch control: in-rubric corruption caught; the gaming is in the gaps

Draft CTL-C2-1: "one rubric statement is edited wrong (e.g. an evidence path deleted or a
count decremented); the counter must report the mismatch and exit non-zero."

Direct answer to the assigned question: **corrupting something NOT in the rubric is never
caught — by design** ("a mismatch outside the frozen set is a new-found defect for the
lesson, not counter ground", :169). That's a disclosed limit, not a defect. The defect is
that the control only proves the counter detects *a* mismatch:

- **No attribution required.** A counter that prints `mismatches: 1` with no id, or with the
  wrong id, satisfies "report the mismatch and exit non-zero". An always-report-mismatch bug
  (or a second latent base mismatch) passes CTL-C2-1 while the counter is actually broken —
  the same class that already burned this lane: round-38's c2-counter "admits a stub at the
  unresolved path and also scores 0" (SCORECARD:3410 area, R38-C2 "met by the frozen counter,
  which is shown non-discriminating"), and round-36's "admits shadow-row and decoy shortcuts".
- **One seed, one category.** A counter whose check for category (e) (verdict-vs-receipt) is
  always-green is invisible if the seed corrupts a category-(a) pointer. Nothing in the
  control samples per-category detection.
- **`expected: 'superseded'` is an unconditional green lane.** The rubric schema lets an
  entry carry `expected:'superseded'`. If "makes the check pass" means "a supersession marker
  exists", then *any* corruption of that statement is masked by the marker — a seeded
  mismatch on such an entry can never red. The seeded-entry spec must forbid seeding
  `expected:'superseded'` entries.

**Impacted axes:** calibration.

**Smallest safe correction:** freeze the seeded list (one entry per rubric category, marked
`seed: true`); CTL-C2-1's acceptance = "the counter reports a mismatch **attributed to
exactly the seeded id set** and every other entry's verdict is unchanged vs CTL-C2-0's
receipt" — i.e. the control verifies the *delta*, not the non-zero exit. Forbid
`expected:'superseded'` entries as seeds.

## F4 — Self-reference: three channels where check and file can drift together

The draft's defense — "every rubric check re-derives the asserted value independently" —
holds only if the check's *derivation* is frozen and its *inputs* aren't the repair surface.
Three channels break that:

**(i) Check argv reading the file under test.** Nothing forbids a check whose command is
extracted from SCORECARD itself (e.g. "run the command named in the cell"). An appended C2
repair block may contain a new code block — appended notes live in SCORECARD/SHONEN/README
per the landing mechanics — and a lazy argv builder (`take the last ```bash block`) parses
the attacker's note as its own rule. The check then verifies the note's rule, not the
statement.

**(ii) The appended repair note supplies the compared value.** The repair rule is "the
rubric's check is re-run against the appended note and must pass" (:229-230). For any
non-pure-derivation check (verdict-vs-receipt, supersession-marker, `path:line` where the
note supplies the line) the appended note IS the asserted string. A dishonest repair note
asserts whatever makes the check true; the rubric's `expected_edit` binds *edit shape*
("appended dated block"), not the note's *content*. So the "repair" {append note:
"corrected: count is 9/9"} passes while nothing was recounted — check and file drifted
together, via the sanctioned path.

**(iii) Receipt files are mutable inputs.** Category (e) checks a `met`/`not met` verdict
against "the cited receipt's exit code". Cited receipts live at
`.ufo/waves/round-<N>/l1/scores/*.json` — ordinary files. If a receipt path is not on the
frozen-path list (R44RevFreeze is checking this; the draft's list names round-42/43 scores
for the *controls* but does not explicitly name the older receipts category-(e) rows cite),
a post-freeze edit of the receipt flips the check while the verdict text is frozen —
silent co-drift. Even frozen-at-REV receipts leave the same hole if the freeze binds bytes
not the receipt's own `measured_revision` semantics.

**Impacted axes:** calibration.

**Smallest safe correction:** (a) Freeze hygiene rule: every check argv embeds its
derivation — no check may source a command, regex, or scope from the file it asserts about;
extracting the *asserted value* from the frozen text is allowed, extracting the *rule* is
not. (b) Each repairable entry carries `expected_repair`: the exact asserted string the
appended note must state, frozen at freeze time where derivable statically (pinned-rev
counts), or for REV-relative entries (map count, rule count) the frozen procedure yields
`expected_repair_at_rev` the counter computes *before* reading the note — the note's value
is compared `==` to the counter-computed one, never consulted as input. (c) Category (e)
checks read receipts `git show <cited measured_rev>:<path>` (revision-immutable) and
require the receipt's own `measured_revision`/exit fields to agree — mutable worktree bytes
are never the oracle.

## F5 — Category (b)/(e) pin-vs-REV ambiguity (fixable, but write it down)

(b) says counts "reproduce under its own `command A` at REV" while the Owned-axes cells pin
older revs (`e1c83313`, `d4b4b4fb`). Headline counts are historical facts about the pin;
re-derived at REV they fail whenever the tree moved (133→137 files already). The scout spec
has the right reading ("re-run the pinned command **at its declared rev**") but the draft
text says REV — one careless rubric author manufactures mass false-mismatches (or, by
"fixing" them at REV, rewrites history). Same for (e): the verdict must be checked against
the receipt *as committed at the cited measured revision*, not the receipt's current blob.
One-line rubric-schema fix: every entry carries `evaluate_at` ∈ {`base`, `pin`, `rev`},
defaulting to `pin` for categories (b),(c),(e) and `rev` for (a),(f). Cheap, worth saying
explicitly since it decides whether the claim is even evaluable.

## F6 — WEAKEST RUBRIC ENTRY: category (d) `planned` vs `worked` — undecidable as specified

Concrete evidence from the base text:

1. **Missing N+1 section.** `planned (round 37)` (SCORECARD:3400) exists; `## Round 37` does
   not. Round 38 did work the named surface (BE SquashFS v4) — so "match" under a
   next-*existing*-round reading, "mismatch" under literal N+1 semantics. The draft never
   says which. A rubric author deciding ad hoc is a fudgeable oracle.
2. **Multiple sections per N.** `## Round 34` (:3328) and `## Round 34, run-6 re-dispatch`
   (:3352); `## Round 25` and `## Round 25 attempt 3`. "What round N worked" is a *set*, and
   the extractor must union it or arbitrarily pick — two reasonable check implementations
   disagree.
3. **Steer-marker circularity.** The escape hatch — "or carry an explicit `(after a steer)` /
   `superseded` marker" — is vacuous in both directions: every recent planned line contains
   `(after a steer)` *inside the plan itself* (:3434, :3452, :3466, :3498 — the marker
   qualifies when the plan takes effect, not that a steer occurred), and a bare `superseded`
   with no citation is a free opt-out that any dishonest repair can append (F4-ii).
4. **Method-constraints hide mismatches.** `planned (round 26)` required "the counting script
   and expected values committed before any REA run" (SCORECARD:3072); round 26 ran a
   pre-freeze REA probe and committed the counter after the data (:3077, :3129 disclosure).
   A surface/axis match says "planned: depth → worked: depth ✓"; the actual promise was
   violated. Similarly `planned (round 37)` bundled "the C1 counter's successor fixed per
   QUALITY 77/78 before data (… reproduction as provenance)" — round 38's closure records
   post-scoring amendment of the predicate, controls fixed after the freeze, and an
   existence-only C2 counter (M38-1..M38-9). Fuzzy `planned≈worked` hides every one of these.
5. **Steer events are unverifiable.** "After a steer" cannot be decided from repo state —
   nothing in the card records "the operator steered X". The marker means "this plan is
   historical, see elsewhere"; without binding to a cited replacement, it's a wildcard.

**Exact hardening check** (proposed rubric entries, three mechanical sub-checks per planned row):

```
entry plan_match_<N>:
  planned_terms = frozen parse of the planned line:
      {axis_token, surface_tokens (quoted paths/handlers/claim-refs like R40-CL1),
       instrument_tokens (named tools/predicates to refreeze or fix)}
  next_rounds   = all `## Round <M>` headings with M = least integer > N present;
                  if none exists -> verdict 'dangling' (mismatch unless the plan
                  carries a frozen `superseded:` citation that resolves — below)
  worked_surface = union over `## Round M` sections of {claim table axis tokens +
                   surface cell tokens}
  PASS iff  planned_terms.surface_tokens ⊆ worked_surface.tokens
        AND planned_terms.instrument_tokens ⊆ worked_or_noted
            (each instrument token either appears in the claim tables or in an
             append-only closure note as "not pursued, reason <X>")
        AND every `superseded:`/`after-a-steer` marker on the plan line is bound:
            marker carries `superseded: <citable artifact>` whose citation resolves
            at REV (a file:line, a claims.md line, or a `## Round` heading)
```

The `superseded:` binding sub-check is the part that converts the wildcard into an assertion:
"superseded by round-44 planned item at SCORECARD:3507" is checkable; bare "superseded" fails.
This also gives the round-37 row a definite verdict under declared semantics: **mismatch,
because no `## Round 37` exists and the planned line carries no `superseded:` citation** —
or `match` only if the rubric freezes a "next existing round" rule *as a stated semantic*,
in which case it must *also* verify the instrument bundle (QUALITY 77/78 successor fixes),
which round 38 demonstrably did not fully deliver. Either way it must be a declared,
re-derivable rule — not a human shrug at census time.

## Lower-severity flags (record, don't block)

- **Rubric-size DoS.** Hundreds of Capability rows × pointer checks in scratch clones — the
  freeze-time refusal of unevaluable entries can be tripped by resource exhaustion, and
  "2 never counts" makes a slow rubric an unmeasurable claim. Keep the rubric at
  one-entry-per-statement (not per-pointer-cell) where cells share a check.
- **"no network" is unenforced.** Check argv is arbitrary code; nothing stops a check
  curling the network or invoking REA — a non-deterministic check is an unstable rubric.
  Freeze-time audit only; consider running checks with a cleared `PATH`/env allowlist.
- **ScoutCalib prompt scope.** The seat prompt reads "`## Capabilities` rows" — capability
  rows also live in `### Capability addition` tables (:2214, :2381, R42's :3481). Ensure
  the census counts all five tables, not just the first.
- **`w1.ready` vs `w1.ready.partial` both present** — cosmetic, but the dispatch records
  37 seats; fine.

## What I'd tell the canonical judge

F1 is a **reject-worthy defect**: as written, C1 and C2 are not separable — C1's own landing
trips C2's `frozen_path_changed`, so the claim's measurability depends on undeclared commit
ordering. F2/F3/F4/F6 are **fixable pre-freeze** and every correction above is rubric/plan
text plus check semantics — none widens scope. If the L1 wants to keep this claim, freeze
F1's carve-outs, F2's census block + freeze-parent re-derivation, F3's delta-attribution
control, F4's argv-hygiene + `expected_repair` binding + receipt-at-pin reads, and the
F6 three-part check. If those land, C2 is a real claim with an honest-stop branch; if they
don't, C2 is a fuzzy self-audit wearing a counter's clothes.

## Receipts (seat `R44CritC2`; honest capture — read-only probes only)

| command | exit | stdout sha256 | wall |
|---|---|---|---|
| `git -C kaidoku-shokunin rev-parse HEAD` | 0 | `fc5eb54a…` (output `fc5eb54a2b79faee82866a27b40c8c2f1767b1eb`) | <1s |
| `git diff --stat c29360e3..HEAD` | 0 | — (7 files: plans + .ufo/waves/round-44 only) | <1s |
| command-A heredoc at `c29360e3` | 0 | `{"mapped":137,"knowledge_files":137,"missing":[],"dangling":[],"rule_blocks":21}` | ~3s |
| command-A heredoc at `fc5eb54a` | 0 | `9c927a9b240ff98af32750fd8cb6b7be4cc1edf9af69866a6e47427ffdbf6400` (normalized keys) | ~4s |
| pointer-resolution loop (22 capability evidence paths) | 0 | — (all `OK`, zero `MISS`) | <1s |
| `grep -n "^## Round" SCORECARD.md` | 0 | — (30 sections; `Round 34`×2, `Round 25`×2, **no Round 37**) | <1s |
| `python3 -c …` on `.ufo/waves/round-43/l1/scores/c{1,2}-at-77d196c6.json` | 0 | — (C1 `{exit:0,met:true,78}`, C2 `{exit:1}`) | <1s |

No writes outside `.ufo/waves/round-44/w1/R44CritC2.md`. No tool installs. No frozen-path
touches. `tools/round-44/` is empty at this commit (pre-freeze); the rubric/counter/controls
files reviewed here are the draft spec plus the w1-spec seat contracts, not landed bytes.
