# R41C2AxisFit — axis fit of the round-41 draft, attacked before the freeze

**Verdict: DEFECTS FOUND.** The axis naming holds (C1 is coverage, C2 is depth) and both targets are
out of reach for a do-nothing control, but the draft cannot be frozen as written: **C2's central clause is
unsatisfiable** (its text-derived evaluator has no action to compare — one action of twelve is derivable),
**C2's held-out set is fully enumerated by the claims file itself** (an 18-row lookup table ties the target
without the rule the claim exists to test), **C1's carrier set is not one concrete value** (V4 is
conditional on a check the draft does not define), and **two C1 clauses name work no counting command
performs** (the fetch chain, pre-freeze freshness). Every finding below is fixable before the freeze
without new data; §8 is a drop-in replacement for both predicates.

Seat: critic (leaf). Read-only git; no VCS mutation; no REA, unblob, sasquatch or extractor run of any
kind; **no carrier was touched** — no reserved image (5490/5491/7560/3490), no member of one, no L3/L4,
and no round-40 carrier was downloaded, carved, extracted or re-run. Every number below is a read of
committed bytes plus the draft text. Wrote only this file and
`.ufo/waves/round-41/w1/artifacts/R41C2AxisFit/` (index + sha256 in §10). Scratch
`/fast/scratch/hyaku/kaidoku-r41/R41C2AxisFit` removed at exit. No tool installed or upgraded; no pacman
transaction.

Lane base read: `49096c7e6f226af0c750c4b003be58883cb6049f`. Draft: `plans/round-41-claims.md:19-101`.

## Axes named (Godspeed)

| axis | what this review moves |
|---|---|
| **coverage** | whether C1's numeric target measures the vendor surface it names, or a fixture the lane already counts |
| **depth** | whether C2's target can distinguish the precedence rule from an enumeration of the class list it publishes |
| **calibration** | whether each clause is one the closure can re-derive from committed bytes, and whether the before→after is the same sentence in plan, counter and receipt |

## 1. The five questions, answered

| question | R41-C1 | R41-C2 |
|---|---|---|
| (a) right axis for the surface changed? | **yes — coverage.** The class is named Frontier at the base in three places (`PROVINCE.md:384`, `PROVINCE.md:386-394` "Still Frontier: AVM-BE bodies (this measurement included) … nested `filesystem_core` images below depth 1", `corpus/README.md:248-251`), the only AVM-named knowledge entry is `corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md`, whose own title ends "(round 40, measured, not promoted)", and the SCORECARD coverage proxy counts mapped knowledge files (130/130). Caveat: the *extraction outcome* was already measured in round 40; the round-41 delta is the fixed instrument plus the promotion, and the round-40 `planned` row said "keep the four round-40 carriers and receipts as data" while the draft scores four **fresh** carriers (`SCORECARD.md` round-40 `planned`). That deviation is a strengthening, but it must appear in `## Changes from the draft`. | **content: depth; measure: not yet.** The surface is `SKILL.md` `## Queue-drain craft` rule block 20 (`SKILL.md:81-375` at the base, 19 blocks). v3 changes the rule (a containment test over gap sets, a precedence order, one new label), so it is not a re-score of held ground. But the target is `matched/N` over a class list the claims file publishes (§3, C2-2), which an exact-set lookup ties without the rule. |
| (b) causally separable? | **yes, data- and verification-separable**, with three couplings that must be written down: the marker/layout rule has two owners (C1's `layout_probe`, C2's rule 5), C2's row-5 action contradicts C1's new Core ground if left unscoped (R40-CL5 M2/M3), and the writer read-sets must be pinned apart (§4). | same |
| (c) can a do-nothing control reach the target? | **no.** `carriers_matched` is the conjunction over `CLAUSES`, which begins with `receipt_present`; the measured round-40 do-nothing receipt records `0/4, exit 1, met_target false` at the freeze (A4 4.1), and the counter's own selftest pins the case. | **no.** Base `SKILL.md` has zero v3 markers (A3 3.2), so the v3 interpreter exits 2; at the freeze the counter exits 2 `no_manifest_at_rev` (A4 4.3). **But** a *shortcut* control does reach it (C2-2). |
| (d) after-state = one concrete value, one command over committed bytes? | **partly.** `carriers_matched == 4` + bindings is one counter run; the draft splits the state across the counter and `c1-extra.py` ("supplementary gate met"), and it needs **network + two pinned binaries + two extractors**, because vendor carrier bytes are never committed (they are pinned by URL → image → member → carve). The draft must say so. | **no.** There is no target sentence at all: no count, no exit code, no binding list, and the action half has no expectation (C2-1, C2-4). |
| (e) universal words the counting commands do not enumerate | 23 quantified phrases audited, **7 open or holey** — plus one ("every binding true") closed only by reading the frozen counter's `BINDINGS` tuple (A5 §C1). Worst: the fetch chain, pre-freeze freshness, "every regular file" (one-directional), "first added" (overwrite hole). | 10 audited, **6 open or holey**, and the freeze-integrity rule's "a frozen path of that claim" is a 34th open phrase (A5 §C2 and its last table). Worst: "(label, action) pair", "never reading", "every held-out envelope" (no N), the missing target, the missing minimal-table control. |

### 1.1 What the concurrent build had landed when this seat ran (read, not run)

The wave is live, so I re-read the lane before writing. Under `tools/round-41/` (untracked, mtime 17:28)
`fetch-vendor.py`, `c1-run.sh`, `c1-extra.py`, `mk-l-carriers.py` and `sqfs-list.py` exist; no
`c1-counter.py`, no C2 tool. Three observations change the *status* (not the substance) of my findings:

- `fetch-vendor.py:199-208` now compares `member_sha256` and fails closed when the cell is absent, with
  selftest cases at `:356-360` — R40-CL6 is closed **at the tool**. What C1-3 asks for is that the chain be
  part of the *measurement*, and that is still missing (`c1-extra.py` has no fetch/chain binding).
- `mk-l-carriers.py:78-80,102-104,133-148` builds and asserts **both** collision directions at build time,
  which is stronger than the check I was going to ask for; what is still unbound is that the frozen L3/L4
  were produced by *that* builder (no builder sha in the carrier spec, no assertion in `c1-extra.py`).
- `c1-run.sh:117-123` uses the `/kaidoku-r41/` provenance segment, so C1-10's first limb is already met.

Everything else below stands: the texts I quote are the draft's, and none of the five tools touches the
claims file's wording. The tools are untracked and may still change before the freeze; I did not run any of
them.

## 2. R41-C1 — findings

### C1-1 (blocking) · V4 is not one concrete value, and its selection rule collides with the freshness clause

Draft `:49-50`: "**V4** vendor: the nested `filesystem_core.squashfs` … **if it is AVM-BE and fits REA's
entry budget at depth 1**; fallback the 5491 wrapper member."

Three defects in one sentence. (i) A conditional carrier means the freeze does not fix the set the target
counts; §6 item 9 requires the after-state to be one concrete value, which is why the draft is labelled
"(draft)" — it must be resolved *at the freeze*, not by fallback at scoring time. (ii) "REA's entry
budget" is an undeclared number. The only committed statement of it is `tools/round-40/c1-run.sh:484-485`
("vendor AVM members exceed the 10000 staged-entry budget at the default depth"); the draft gives V3's
`inodes 104` but not V4's, and never says whether "fits" means `inodes <= 10000` (a superblock parse) or a
real run. (iii) If it means a run, the draft contradicts itself: `:32` says the carriers are ones "none of
which any REA or unblob run touched before the freeze".

Also: V4 is the nested core, while `PROVINCE.md:394` and `corpus/README.md:251` both leave "nested
`filesystem_core` images below depth 1" Frontier. If V4 is that image promoted to a top-level carrier, the
frontier note must say which sub-clause moves and which stays, or the coverage surface is ambiguous.

**Smallest safe correction.** Pin one member per carrier in the freeze commit; state V4's `inodes`,
`bytes_used`, `member_sha256` and the budget number in the same table as V3's; drop "fallback" (a carrier
that cannot be pinned by a superblock parse is an honest stop, not a rewrite). Reword the surface
paragraph to name the two sub-clauses separately: "AVM-BE bodies" moves; "nested `filesystem_core` below
depth 1" moves only if the frozen V4 carrier *is* that image run at depth 0, otherwise it stays.

### C1-2 (blocking for honesty) · the freshness clause is unenumerable and narrower than the reservation

`:32` "none of which any REA or unblob run touched before the freeze". No committed byte records the
absence of a run; `receipt_fresh` only proves the *receipt* is absent at the freeze. And the sentence is
narrower than the reservation it restates: the reservation forbids **any extractor**, while the oracle arm
itself runs `sasquatch-v4be -f -no-exit-code` directly (`tools/round-40/c1-run.sh:299-301`) to cross-check
`oracle.tsv`. So as written the clause is simultaneously unverifiable and false for the workflow that
produces its own oracles.

**Correction.** Replace with what is checkable, and disclose the one run that is not an REA/unblob run:

> no commit in `FREEZE..REV` other than a carrier's own receipt adds a file naming that carrier as an REA
> subject (checked by `first_add`), and at the freeze each carrier's only extraction ever performed is the
> oracle arm's `sasquatch-v4be -f -no-exit-code` listing recorded in its `oracle-run.json` (path, version,
> sha256, argv, exit).

### C1-3 (blocking) · the fetch chain is not in any counting command

`:40-41` "for vendor carriers the fetch chain checks image sha256 → member sha256 (R40-CL6) → carrier
sha256". Measured: `tools/round-40/c1-counter.py:1030-1035` reads `<pin>.bin` from `--carrier-cache` and
re-hashes it (good); `fetch-vendor.py:78-107` performs the chain but is never invoked by the counter or by
`c1-extra.py`; `carriers_spec` requires only `('url','image_sha256','member','length')`
(`c1-counter.py:491-494`), so even the `member_sha256` cell that the round-40 `carriers.json` already
carries is unchecked. R40-CL6 is therefore not closed by the draft's text alone.

**Correction.** (i) `fetch-vendor.py` compares `member_sha256` — **landed at `tools/round-41/
fetch-vendor.py:199-208` during this seat's run**; what remains is `carriers_spec` requiring the cell.
(ii) Each vendor carrier commits a `fetch.json` (image_sha256, member_sha256, carrier_sha256, ok) produced
by that run; `c1-extra.py` checks all three digests against `carriers.json` and that the cache file
re-hashes to the pin. Then the chain is one command over committed bytes (the log) plus three digest
comparisons, and `fetch-vendor.py --selftest` (which now runs a fake fetcher on both new drifts) is the
instrument demonstration.

### C1-4 (high) · "publishes every regular file of the frozen independent oracle" has no converse, and "independent" is false for L3/L4

Measured: `oracle_hits_ok = (hits == oracle_files)` (`c1-counter.py:1085-1086`), where `hits` counts
oracle rows that found a matching published file (`:635-640`). A receipt that publishes the oracle *plus
any number of extra regular files* passes. Round-40's U3 is un-closed.

Second half: for V3/V4 the oracle is `sqfs-list.py` cross-checked by `sasquatch-v4be` — two producers that
share no code, which is the best available and was validated in round 40. For L3/L4 both producers read
bytes the lane's own writer produced, and one of them is the tool under measurement; `PROVINCE` and the
round-40 wave-2 oracle report do not make lane-built oracles independent.

**Correction.** Bind the set equality: the published regular-file set, resolved through the extract root,
**equals** the oracle row set (same paths, same sha256, no extras, and the receipt's `published_bytes`
equals the oracle size sum). For L3/L4 make `mk-l-carriers.py` emit `oracle.tsv`/`nonregular.tsv` from the
tree it writes — a third producer, independent of both the reader and `sasquatch-v4be` — and have
`c1-extra.py` require the three-way agreement.

### C1-5 (high) · "first added in a commit descending from the freeze" is satisfied by a post-add overwrite

Measured in a scratch fixture (A1): `first_add()` (`c1-counter.py:706-713`) returns the **oldest** add, and
`receipt_fresh` (`:1069-1071`) only asks `add != freeze` and `is_ancestor(freeze, add)`. A receipt added
after the freeze and then overwritten keeps `receipt_fresh == true`, and no clause compares the blob at
`REV` with the blob introduced by that add (the two `git rev-parse` outputs in A1 differ). Round-40's U5
therefore stands.

**Correction.** `receipt_fresh` becomes: the path is absent at `FREEZE`; its first add `A` descends from
`FREEZE`; and `git rev-parse REV:path == git rev-parse A:path`. One extra git call per carrier; add the
"add, then overwrite" case to the counter's selftest (the fixture in A1 is the red case).

### C1-6 (high) · two of the four carriers are lane-built, in a target named `carriers_matched == 4`

Round-40's axis-fit U9 asked for `vendor_matched` / `supplemental_matched` to be split, and the split was
never adopted. Repeating the shape is not fatal (all four must pass, so a vendor failure cannot be masked),
but the *coverage* content rests entirely on V3/V4: the SCORECARD coverage proxy and the PROVINCE surface
are the vendor class, and prompt §6 item 9 says "counting rows a sourceless fixture also counts is never
coverage". Today a reader cannot tell whether the promotion was earned on vendor bytes or on the two
images the lane wrote itself.

**Correction.** The receipt prints `vendor_matched` (of 2) and `lane_matched` (of 2) separately, the target
is `vendor_matched == 2 and lane_matched == 2`, and the SCORECARD row cites the vendor count. Also add
"no carrier pin equals a round-40 carrier pin" to `carriers_spec` — cheap, and it closes the relabel path
for any L3/L4 that ends up byte-identical to round-40's L1/L2.

### C1-7 (medium) · "both-direction collisions" is a fixture property no command sees

`:52-53` requires L3/L4 to carry "a regular file whose path ends with a symlink's path, and a symlink whose
path ends with a regular file's path". The counter's *selftest* pins both directions (the prototype diff
adds five cases, `.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/c1-counter-exact-match.diff:176-211`),
but nothing checks that the committed carriers carry them. A mis-built L3/L4 (say, both collisions missing)
would pass every clause.

**Correction.** `carriers.json` names the two expected pairs per lane carrier, and `c1-extra.py` checks
`oracle.tsv`/`nonregular.tsv` contain both (one regular path that is a proper suffix of a symlink path, one
symlink path that is a proper suffix of a regular path) before the counter runs — or, cheaper now that the
builder self-asserts (`tools/round-41/mk-l-carriers.py:133-148`), pin the builder's sha256 in the carrier
spec and record it in the receipt, so the checked property is tied to the frozen bytes.

### C1-8 (medium) · clauses stated as prose presence, and the frozen path set unnamed

`:43-44` "says what it supersedes" is reduced by `c1-extra.py:frontier_content` to the token `supersede`;
that is the strongest enumerable form (round-40 D4), so the claim should *say* it is a token test.
`:15` "a frozen path of that claim" never names the set; round-40's C1 set is a code constant and its C2
set omits the writer (A4 4.4).

**Correction.** Enumerate both frozen tuples in the claims file (C1: claims, counter, runner, `c1-extra`,
`fetch-vendor`, `sqfs-list`, `gen-squashfs`, `mk-l-carriers`, `carriers.json`, `gap-rule.json`, every
`oracle.tsv`/`nonregular.tsv`/`oracle-run.json`, every receipt, the entry, PROVINCE/README/SOURCES; C2: the
interpreter, the generator, the writer it loads, the evaluator, the counter, the claims file, the held-out
manifest and every envelope). This is also the only way `frozen_path_changed` can be re-derived by a
closure.

### C1-9 (low) · the unmoved-command must name its instrument

Measured (A3 3.2): the round-40 v2 interpreter at the base exits **0** and labels H13 `dep-missing-be`,
because the v2 table is already at the base. Only the **v3** interpreter exits 2. The draft says "the
frozen v3 interpreter", which is correct; the risk is a closure reaching for the v2 one. Keep the sentence
and add the base SHA and the marker count (`grep -c 'sqfs-triage-table v3' → 0`) as the literal command.

### C1-10 (low) · run provenance, projection profile, gap-rule shape

`parameters.output_directory` must carry the round-41 scratch segment (landed:
`tools/round-41/c1-run.sh:117-123` enforces `/kaidoku-r41/`; the counter side is the round-40
`provenance_ok`, `c1-counter.py:596-604`); `gap-rule.json`'s `claim` cell is compared to `'R40-C1'` and must become
`'R41-C1'`; the projection profile is `plus-extractor`. None is in the draft text; all are one-line port
requirements that will otherwise be discovered at scoring time.

## 3. R41-C2 — findings

### C2-1 (blocking) · the predicate asks the text-derived evaluator for an action the text never defines

`:90-93` requires "the (label, **action**) pair that the frozen independent evaluator (written from the
precedence text above …) gives it". Measured (A2): the precedence block contains exactly one of the
eleven round-40 action tokens — `none`, in rules 1 and 12 (`(unclassified, none)`). It derives a label for
all 13 labels and an action for **one**. An evaluator restricted to that text cannot emit the pair for the
other 12, so the clause is unsatisfiable exactly as round-40's "same semantic projection" clause was, and
the same trap follows: at scoring time the temptation is to narrow the claim after data, which §6 item 9
forbids.

**Correction (smallest safe).** Split the expectation by source and say it:
- labels: the frozen evaluator, written from the precedence text, never reading the table, interpreter or
  generator class map;
- actions: the frozen `<!-- sqfs-triage-actions: … -->` line plus a frozen `label → action` map committed
  in the freeze (the round-40 generator already supports this via `--actions-file`, and the map is 13
  lines);
- the pair is the conjunction, and the receipt prints `matched_labels` and `matched_actions` separately.

### C2-2 (blocking for depth) · the held-out set is enumerated in the claims file, so a lookup table ties the target

`:93-94` names all five combined classes, and "v2's 13 classes" is committed text (`heldout-gen-v2.py`
`RECIPES`, `DEFAULT_CLASSES`), two replicates each → 18 classes, 36 envelopes, **every one of them named in
the claims file**. A 13-row table with one exact-set cell per class (no containment operator, no precedence,
no combined-set reasoning) reproduces the labels on all 36. That is the shortcut round-40's closure D3
asked the next table to be scored against ("expected labels must not come from the generator's class map
alone"), and the evaluator fixes the labels' *authority* without touching the inputs' *enumerability*.

**Correction.** Keep the 18 published classes as the regression floor and add an unpublished arm:
`n_unpublished >= 6` classes drawn by the same frozen generator from the same outcome space, **names not in
the claims file** (freeze the count, not the names), with `matched_unpublished == n_unpublished` as a
separate gated binding. Candidate classes a fitted table provably misses: `missing-extractor-dependency`
with **both** tokens in `D`; `extractor-failure` with `P > 0` on an LE handler; an unknown gap kind
alongside `unpublished-entry`; `depth-limited` with `P = 0` on a handler that also failed; `unclassified`
reached by "anything else" (for example `G = {unknown-chunk-handler}` with a squashfs handler present).

### C2-3 (high) · rule 3 is ambiguous, and the natural implementation of "names" makes it fire twice

`:77-78` "`dep-missing-be` if D names `sasquatch-v4be`, `dep-missing-le` if D names `sasquatch`". Measured
(A2): the committed round-40 envelopes carry `D=['sasquatch-v4be']` (H13, H14) and `D=['sasquatch']`
(H15, H16). `sasquatch` is a substring of `sasquatch-v4be`, so an implementation that reads "names" as a
contains/substring test (the very operator the v3 table adds) satisfies **both** branches on H13/H14; an
exact-token implementation satisfies one. The text orders the branches and defines "names" nowhere, so the
table and the evaluator can diverge before any new data exists — and the divergence would be reported as
the claim's failure, not as the text's.

**Correction.** "rule 3: `missing-extractor-dependency` ∈ G → `dep-missing-be` if D **contains the exact
token** `sasquatch-v4be`; **else** `dep-missing-le` if D contains the exact token `sasquatch`; **else**
`unclassified`." Define "names" once, above the list, as exact token membership in the gap's
`dependencies` array.

### C2-4 (high) · no target, no count, and "every held-out envelope" is vacuously true at N = 0

The predicate has no target sentence (C1 has one at `:60`). §6 item 9 asks each after-state to be one
concrete value; here it is a clause list plus an unstated N. `matched == n` with `n == 0` is true.

**Correction.** Add, verbatim in the plan, the same sentence in the counter and the same label in the
receipt:

> Target: `matched == 36` of `n == 36` published envelopes **and** `matched_unpublished == n_unpublished`,
> `every binding true`, exit 0.

### C2-5 (high) · three of the five new classes cannot be produced by the current generator

Measured (A3 3.3): `run_rea` builds its argv without `--max-depth` (`heldout-gen-v2.py:901-902`), the 13
`RECIPES` carry no depth knob (0 hits for `max.depth`), and no recipe nests an image. But every round-40 C1
carrier run at `--max-depth 1` carries `('depth-limited', None)` as its first gap (V1 697 files, V2 8, L1 7,
L2 6 — all `coverage=partial`), i.e. the depth flag, not nesting, is the determinant. So
`depth-limited alone`, `depth-limited+in-tree` and `depth-limited+mixed` require a **per-class `max_depth`**
in the generator plus the writer's nesting-free path — new code, never exercised.

Round 40's M40-5 is exactly this failure mode (a recipe trusted from recon failed on a fresh seed and cost a
freeze fix). The draft requires no dry run for C2; only C1 has the QUALITY 83 dry-run bullet.

**Correction.** Add to the draft: "pre-freeze dry run (QUALITY 83): on a sandbox clone, the round-41
generator produces all 18 classes at seed `sha256("dev41")`, and the evaluator and the generator's class
map agree on all 36 envelopes; any class that cannot be produced is moved to `Not claimed` before the
freeze. The dry run must also confirm that the 18 classes' eight-feature vectors are pairwise distinct or
carry the same precedence label: the precedence is a *function of the features*, so two classes with one
vector and two labels are unlabelable before any table exists, and the generator's class map would then
disagree with the evaluator on a class the claim itself chose."

### C2-6 (high) · independence is asserted, not observable; and rule 5 forces a label on a split the envelope cannot decide

`:92` "never reading the table, the interpreter or the generator's class map" cannot be checked, and after
C2-1's fix the action map is a fourth input the evaluator must not read. Note also that rule 5
(`extractor-failure`, `P = 0`, `BE = no`, handler `squashfs_v4_be` → `avm-marker-be-dropped`) cannot
distinguish a **doctored marker on a standard-BE body** (which does need `-be`) from a **genuine AVM-layout
body that failed** (which must never be given `-be`, because after C1 lands the layout — not the marker —
is what decides the argv). The envelope carries no layout field, so the label is a coin-flip on two
opposite-damage classes, and the v2 action (`wrap-extractor-be`, `SKILL.md:368`) is the wrong instruction
for the second. That is R40-CL5's M2/M3, still open, and it becomes a contradiction between two Core
statements the moment C1 lands.

**Correction.** (i) Mechanise independence: the counter runs the evaluator in a scratch tree containing
only the envelopes and the evaluator, with `SKILL.md`, the interpreter, the generator and the action map
absent, and records the exit; that is an observed "never reading". (ii) Scope rule 5: the label requires
`BE = no` **and** a recorded golden-file check of the layout, and its action becomes the conditional
"walk the inode-table metadata header little-endian first; if it lands on `directory_table_start` the body
is AVM layout and the failure is damage — keep it, never wrap it; else rerun through the wrapper"; add the
matching frozen action token.

### C2-7 (medium) · two live tables again (R40's P7, not implemented)

`SKILL.md` keeps block 19's v2 table live and adds block 20's v3 table. A reader then has two graders for
the same envelope; v2 answers `unclassified` for every combined set (its gap cells are exact sets,
`sqfs-triage-v2.py:245-257`), which is a safe failure but a second authority. Round-40 solved this shape
by replacing block 18's rows with a pointer.

**Correction.** Block 19 keeps its prose, its table rows become one line — "table v2 (frozen at
`c4895cf1:SKILL.md:361-375`) lives in `corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`; where the two
disagree the v3 table governs" — and the counter gates that the craft section holds exactly one live
`<!-- sqfs-triage-table ` comment line and that it is v3. **Measured caution:** the raw substring
`<!-- sqfs-triage-table ` already occurs 4 times in `SKILL.md` (two real markers, two backticked quotations
in the instrument registry at `:1383`, `:1401`), so the gate must be section-scoped and line-anchored, not
a global count (A3 3.1).

### C2-8 (medium) · N/N still cannot see table size; the controls do not include the shortcuts that matter

Round-40's executed result stands un-refuted: an 8-row, **7**-non-`*`-cell table reaches 20/20 on the
frozen round-39 set with every cell load-bearing. Nothing in P41-C2 reports `distinct_decisions` or
cell necessity, and the control list (`:99-101`) omits (i) a minimal-cell table, (ii) an 18-row exact-set
lookup (C2-2), and (iii) the identity control "evaluator replaced by the generator's class map", which is
the only control that shows the evaluator does work.

**Correction.** Report `distinct_decisions` and `non_load_bearing_cells` in the receipt; add the three
controls. C2-2's unpublished arm is the gate that makes (ii) fail; (iii) must fail on at least one
envelope or the evaluator is a transcription of the class map.

### C2-9 (medium) · the C2 frozen set omits the writer and the held-out data (R40-CL3)

Measured (A4 4.4): `FROZEN = (INTERP, GEN, COUNTER, CLAIMS)` at `c2-counter.py:75`, while the generator
loads `tools/round-39/gen-squashfs.py` (`:80-82`) and the after-state includes "carriers regenerate
byte-identically". A post-freeze writer edit is invisible. Add the writer path(s), the held-out manifest
and every envelope (the manifest ordering is already bound: `manifest_before_envelopes`), and the evaluator.

### C2-10 (low) · wording

`:68` "adds combined-gap-set rows" misdescribes the change: combined sets do not get new *rows* — they get
the same labels through a containment test and a stated precedence order; v3 adds exactly **one** row
(`depth-limited-nested`). Say that, because the row count is what a reviewer will count.

## 4. Separability

**Data-separable: yes.** C1 reads PROVINCE/README/SOURCES/knowledge/receipts/oracles/carriers; C2 reads
SKILL/interpreter/evaluator/generator/held-out. No byte is shared; C1's carriers are images, C2's are
generated envelopes.

**Verification-separable: yes.** C2 can be scored with C1 failed (nothing in the C2 counter reads
PROVINCE), and C1 can be scored with C2 failed (nothing in the C1 counter reads SKILL's craft section).

**Three couplings to write down (none fatal, one admission-relevant):**

1. **The marker/layout rule has two owners.** C1's `layout_probe` (`c1-counter.py:510-590`) and C2's rule 5
   are the same rule used in two directions. One wrong model of `mkfs_time == bytes_used` + LE block
   lengths falsifies both claims in one round. Give the rule one owner (C1) and have C2's row cite the
   Core entry without re-deriving the layout.
2. **C2's row-5 action contradicts C1's new Core ground** (C2-6) — if it lands unscoped, the round harms
   depth while moving coverage, and AXES' "no trade" rule rejects the round. Fix scoping in the same
   freeze.
3. **Writer read-sets.** C1's lane-built carriers use the AVM writer (`gen-squashfs.py --endian
   avm-genuine`, `mk-l-carriers.py`); C2's generator loads `tools/round-39/gen-squashfs.py` at its
   manifest sha256. Say in P41-C2 that the round-41 C1 writer is outside C2's read-set and that C2's
   writer is pinned, or a C1 writer change silently breaks C2's regeneration binding.

**A fourth, mechanical coupling:** both claims freeze `plans/round-41-claims.md`, so a single post-freeze
edit to either predicate exits 2 for both. Correct, but it means the claims file must be final at the
freeze — which is exactly what the `## Changes from the draft` section is for.

## 5. Do-nothing controls (question (c)), measured

- **C1.** The measured round-40 do-nothing receipt is `{"target":4,"carriers_matched":0,"exit_code":1,
  "met_target":false}` at the freeze (A4 4.1), and the code path is structural: `CLAUSES` starts with
  `receipt_present`, `matched` is their conjunction. A do-nothing cannot reach 4/4. The draft's
  `CTL-C1-0` is the right control; add the two shortcut controls it already names *plus* the pin-distinctness
  check (C1-6), which is what makes "relabelled round-40 receipts" fail for the lane-built carriers rather
  than only for the vendor ones.
- **C2.** Base `SKILL.md` has no v3 marker, so the v3 interpreter exits 2; at the freeze the counter exits 2
  `no_manifest_at_rev`. A do-nothing cannot reach `matched == n`. **But** the shortcut that matters is not a
  do-nothing: it is an 18-row exact-set table (C2-2), which ties the published set with no rule. That is the
  control the draft must build before data, and the one that, if it reaches the target, proves the target is
  too weak rather than the control invalid.

## 6. One concrete value, one command (question (d))

**C1** — the value is `carriers_matched` (say `4`) with `met_target == true`. One command is the counter;
the draft also requires `c1-extra.py`, so write both command lines into the claim and say that `--base` and
`--carrier-cache` are part of the measurement. Say plainly that the bytes are **not** all committed: the
vendor carriers are re-materialised by the pinned fetch chain, so the command needs network plus
`unblob 26.6.4`, `sasquatch` and `sasquatch-v4be` 4.5.1, and `npx rea-agents@6.5.0`. §6 item 9's "over
committed bytes" is satisfied for the pins, oracles, receipts, gap rule and doc bindings, and not for the
vendor images — which the licence makes unavoidable and which round 40 already disclosed.

**C2** — the value is `matched` / `n` plus the bindings. One command is the counter, provided the counter
itself invokes the evaluator (otherwise the evaluator's output becomes a fifth committed artifact that the
closure must trust). Write the target line (C2-4), name the bindings, and say the envelopes are committed
so the command is offline.

## 7. Universal words the counters do not enumerate (question (e))

A5 audits 23 C1 phrases and 10 C2 phrases (plus the freeze-integrity rule) against the round-40 clause
names. The eight that matter:

| claim | phrase | why the counter cannot close it |
|---|---|---|
| C1 | "none of which any REA or unblob run touched before the freeze" | no committed byte records the absence of a run; narrower than the reservation it restates |
| C1 | "the fetch chain checks image sha256 → member sha256 → carrier sha256" | `fetch-vendor.py` is outside every counting command; `carriers_spec` does not even require `member_sha256` |
| C1 | "publishes every regular file …" | one direction only; extras pass |
| C1 | "first added in a commit descending from the freeze" | overwrite after the first add still passes (A1) |
| C1 | "nested-name collisions in both directions" | a fixture property; only the selftest sees it |
| C2 | "the (label, action) pair … the evaluator gives it" | 11 of 12 actions have no derivation in the text (A2) |
| C2 | "for all held-out envelopes" | no N in the claim; vacuously true at N = 0; and the set is enumerated in the same file |
| C2 | "never reading the table, the interpreter or the generator's class map" | a process promise; only observable by running the evaluator where those paths are absent |

## 8. Drop-in replacement text

**P41-C1 (replaces `:31-44` and `:60`)**

> At the measured revision, for each of the four carriers frozen in `.ufo/waves/round-41/c1/carriers.json`
> (ids exactly `V3`, `V4`, `L3`, `L4`; one pin, one oracle and one non-regular table each; no pin equal to
> a round-40 carrier pin; the two lane-built carriers' tables contain both collision directions named in
> the spec), the round-41 REA 6.5.0 `extract-firmware` after-receipt (`--max-depth 1`, unblob 26.6.4,
> `sasquatch`/`sasquatch-v4be` 4.5.1 on the child PATH) is absent at `FREEZE`, its first add descends from
> `FREEZE`, **and the blob at `REV` equals the blob at that add**; it names the `squashfs_v4_be` handler
> with no failed chunk; the **set** of published regular files, resolved through the chunk extract root,
> **equals** the frozen oracle row set (paths and sha256), and no non-regular entry is published at its
> exact path; every gap is allowed by the frozen gap rule and every required non-regular kind carries one;
> the subject digest equals the carrier pin, the receipt recomputes to its evidence id, the
> `parameters.output_directory` carries the `/kaidoku-r41/` segment, the carrier bytes hash to the pin and
> carry the AVM layout (big-endian `sqsh`, v4.0, `mkfs_time == bytes_used`, metadata block lengths
> little-endian); a counter-time rerun of the same bytes has the same `plus-extractor` projection; each
> vendor carrier's committed `fetch.json` carries `image_sha256`, `member_sha256` and `carrier_sha256`
> equal to `carriers.json`, and its only pre-freeze extraction is the oracle arm's `sasquatch-v4be -f
> -no-exit-code` listing; PROVINCE holds a `## Round-41 additions to Core` row naming the AVM layout and
> citing the entry, the entry cites a SOURCES row absent at the base whose used-by names it, a
> `Round-41 frontier note` names the heading, the stem and the token `supersede` and says which Frontier
> sub-clause stays (nested `filesystem_core` below depth 1, unless V4 is that image at depth 0), and
> `corpus/README.md` maps the stem. **Target: `vendor_matched == 2`, `lane_matched == 2`,
> `carriers_matched == 4`, every binding true, `c1-extra.py` exit 0, counter exit 0** — measured by
> `fetch-vendor.py` (materialise, chain verified) then `c1-counter.py --carrier-cache` then
> `c1-extra.py --base <base>`; the bytes that are not committed are the vendor images, pinned by the chain.

**P41-C2 (replaces `:90-97`, adding a target line)**

> At the measured revision, the frozen v3 interpreter, reading only the SKILL v3 table (exactly one live
> `<!-- sqfs-triage-table ` comment line in `## Queue-drain craft`, and it is v3), gives **every** held-out
> envelope in the frozen manifest (`n == 36` published envelopes: 18 classes × 2) the **label** that the
> frozen evaluator gives it — the evaluator written from the precedence text above, run in a scratch tree
> where `SKILL.md`, the interpreter, the generator and the action map are absent (recorded exit 0) — **and**
> the **action** that the frozen `label → action` map committed in the freeze gives that label; the
> generator's own class expectation agrees with the evaluator on every envelope (a disagreement is reported
> and fails); `matched_unpublished == n_unpublished` (`n_unpublished >= 6`, classes drawn by the same
> generator, names not in this file); seed = the freeze hash; carriers regenerate byte-identically; the
> receipt prints `matched_labels`, `matched_actions`, `distinct_decisions` and `non_load_bearing_cells`;
> the v3 table bytes equal the freeze bytes. **Target: `matched == 36` of `n == 36`,
> `matched_unpublished == n_unpublished`, every binding true, exit 0.**

## 9. Limits

- No carrier run: I did not run REA, unblob, `sasquatch`/`sasquatch-v4be`, or any extractor, and did not
  download or carve any image. C1's carrier-level statements are therefore about the **instrument and the
  text**, not about V3/V4/L3/L4's bytes; V3's superblock numbers are the draft's, unverified by me by
  design (the seat that owns V3 owns that read).
- C2's 36-envelope set does not exist. My statements about it are [INFERENCE] from the 26 committed
  round-40 envelopes, the frozen generator's recipe schema, and round-40's executed 7-cell result.
- The 7-cell/20 result I rely on for C2-8 is committed round-40 wave-1 evidence
  (`.ufo/waves/round-40/w1/artifacts/R40C2AxisFit/min7-score.txt`), not a measurement of mine.
- I did not read the round-40 independent evaluator
  (`.ufo/waves/round-40/w2/artifacts/R40W2C2IndepEval/eval-v2-indep.py`): my seat does not allow it.
  Nothing in C2-1/C2-2/C2-6 depends on it — those findings come from the precedence text and the frozen
  generator.
- [INFERENCE] "REA's entry budget" = the 10000 staged-entry limit recorded in `c1-run.sh`; the draft does
  not name the number, so C1-1's third limb is a reading, not a measurement.

## 10. Artifacts

Rebuildable; each file states its own command. Directory
`.ufo/waves/round-41/w1/artifacts/R41C2AxisFit/`:

| file | what it holds | sha256 |
|---|---|---|
| `a1-first-add-overwrite.txt` | scratch-git fixture: a receipt added after the freeze then overwritten keeps `receipt_fresh`, and the two blobs differ | `195a2772eb2d788b16db6568b20b1d482b62b2bec58b8441c90de5369fc414a7` |
| `a2-precedence-actions.txt` | the precedence block derives 13 labels and 1 action; measured `dependencies` values H13–H16 | `c8777e9abc1bf37ae5fbee973563147b8d92618eaecbd86cde662a4759c082c4` |
| `a3-instrument-facts.txt` | marker counts (4 raw / 2 real), the v2 interpreter exits 0 at the base, the generator has no `--max-depth`, all four round-40 carriers carry `depth-limited` | `6f988c1225ab0aff9ec865ef977e7df13a0844f812b9d2f44cfc7d3270049676` |
| `a4-do-nothing-and-clauses.txt` | the measured do-nothing receipt, the one-directional oracle clause, the `no_manifest_at_rev` exit, `FROZEN` without the writer | `869a59b7cdd3cb14f022e8517958dc6800ef1e815723914e1b6839610b2cc237` |
| `a5-universal-words.md` | the 33 phrase rows plus the freeze-integrity rule: phrase → enumerator → verdict | `b93068f1db5755c58d12716e2dd5cf5c19873b0b0804a1763f649744045e1ab7` |

Hygiene: scratch `/fast/scratch/hyaku/kaidoku-r41/R41C2AxisFit` (with its fixture clones under it) is
removed before this seat yields; nothing cited depends on it. No vendor bytes or extracted vendor
files were copied anywhere. No VCS mutation; writes confined to this file and the artifact directory above;
no `~/.local/bin` write; no tool installed or upgraded.

**Report:** `.ufo/waves/round-41/w1/R41C2AxisFit.md`
