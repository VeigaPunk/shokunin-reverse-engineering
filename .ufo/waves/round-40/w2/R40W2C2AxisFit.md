# R40W2C2AxisFit — R40-C2 attacked as a depth claim: the 26/26 is a self-consistent re-derivation, and two rows carry instructions their own cells contradict

**Verdict: DEFECTS FOUND** on the axis attribution, not on the predicate's arithmetic. I attacked the
claim's *depth* reading — that `SKILL.md`'s craft section gained a decision table a reader can act on —
and could not break the score: `c2-counter.py` reproduces **26/26, all 24 bindings true, exit 0** at
`42c10a58` in my own run, the v2 table bytes are identical at the freeze and at the measured revision,
the base `SKILL.md` is refused with exit 2, and a post-freeze table edit is refused
(`v2_table_identical` false, `met_target` false, exit 1). What does not survive: **69 % of the scored
envelopes were already decided by the round-39 table** (measured, not inferred — 18/26 on the scored
set), **the expected answer is generated from the same class map the table was written to**, the
eighth declared field (`dependencies`) never changes a decision, and row 4's `action` cell contradicts
its own `cause` for the branch that `cause` explicitly names while the row's sibling
(`escaping-symlink-removed`, gap cell `*`) silently absorbs any combined gap set — a partial failure
with escaping links is told `expect-link-absent`.

Role: critic (leaf). Nothing committed, pushed, frozen, edited or installed; the lane tree was not
touched (it already carries another seat's ` M SKILL.md`; all my reads used committed blobs). Every
measurement below ran the **frozen** interpreter from `git show 42c10a58:tools/round-40/sqfs-triage-v2.py`
against the **committed** 26 envelopes, on mutant `SKILL.md` copies under
`/fast/scratch/hyaku/kaidoku-r40/R40W2C2AxisFit` (removed at finish). Full transcript and artifacts:
`.ufo/waves/round-40/w2/artifacts/R40W2C2AxisFit/` (`measurements.txt`, `table-nodeps.diff`,
`table-placebo.diff`, `syn-partial-mixed.envelope.json`, `c2-rerun-at-42c10a58.json`,
`c2-mutated-table-sandbox.json`).

## The axes I held fixed

| axis | what I measured | verdict |
|---|---|---|
| did the surface move | `git diff --numstat fa6a8a3f..42c10a58 -- SKILL.md` = `33 1`; the only commit touching `SKILL.md` in that range is `7fce3086`; block 19 at `SKILL.md:348-375` (marker `:361`, actions `:362`, table `:363`, 11 rows), block 18 supersession at `:331-333` | **moved**, one commit, no later touch |
| does the base refuse | frozen interpreter on `fa6a8a3f:SKILL.md`, exit 2, `marker absent from the craft section` | **unmoved at base** |
| does the counter reproduce | my run: `matched 26, n 26, bindings_ok true, bindings_false [], exit 0, distinct_decisions 12` | **reproduces** |
| is it gameable after the freeze | sandbox clone (`git clone --shared`, toplevel verified, fixture identity `fx`), one action cell changed, re-committed: `matched 24, met_target false, bindings_false ["v2_table_identical"], exit 1` | **refused** |
| instrument selftest | `sqfs-triage-v2.py --selftest` → `cases=45 pass=45 fail=0`, exit 0 | **green** |

I found no arithmetic error, no binding lie, and no forged receipt in R40-C2. The defects are in what
the 26/26 is evidence *for*.

## Findings

### F1 — 18 of the 26 scored envelopes are round-39 v1 ground; 2 more are the abstention pair
`CTL-C2-2.md` (the v1 table transcribed into the v2 grammar with the adopted actions), scored by the
frozen interpreter **on the scored held-out set**, not on the dev set, returns **18/26** and misses
exactly `clean-empty`, `mixed-symlinks`, `partial-body-failure`, `out-of-domain` (2 envelopes each).
`CTL-C2-4.md` (no domain guard) returns 24/26. So the MET verdict's *new* content is 8 envelopes, of
which 2 (`H25`/`H26`) are `unclassified`/`none` — the absence of a decision — leaving **6 envelopes
(3 classes, 23 %) of genuinely new triage**. With two replicates per class the independent decision
count is 13, not 26.

This matters because prompt §6 item 9 names the failure mode exactly: *"Re-scoring a rule the lane
already holds on new inputs … is quality work, never coverage or depth."* v2 is not a re-score of a
rule the lane holds — it is a new table — but the depth delta is three rows plus a guard, and the
26/26 headline reports the whole closed set. A reader of the SCORECARD/report will read the delta as
4.3× larger than it is.
*Smallest safe correction*: state the partition next to the score — `26/26 = 18 v1 ground + 2
abstention + 6 new (clean-empty, mixed-symlinks, partial-body-failure)` — in the C2 SCORECARD row and
the entry's **Scoring** paragraph. No code change.

### F2 — the expected answer is the class name the generator generated the input from
`heldout-gen-v2.py` writes `manifest.label_actions` (class → label/action) statically and stamps
`carriers[i].label` from it; the class name also drives the injected feature (a `partial-body-failure`
carrier is *built* by injecting an `extractor-failure` gap beside published files). The table was then
authored to those labels. The 26/26 therefore tests the **feature extractor against the synthesised
class construction**, and the label semantics against nothing. It cannot distinguish "this is the
right label and action for this real image" from "this row reproduces the generator's map", which is
why the dev run answered all 13 classes before the held-out bytes existed (F3).
Contrast C1, whose predicate binds the label to an independent oracle (`sqfs-list.py`, sasquatch
crosscheck) over real vendor bytes. `QUALITY.md:28` (row 28) and `:69` (row 69) are the same shape:
expected outcomes must not be derived from the artefact's own decision data.
*Smallest safe correction*: one sentence in the entry — "the pair is the generator's class map; the
score shows the reader's feature extraction maps these envelopes onto the intended rows, not that the
row's label is right for a real firmware outcome" — and let a later round bind one v2 label to a real
carrier (C1's L1/L2 already are such carriers).
[INFERENCE] on intent; observation on the mechanism (`manifest.json:label_actions`, the injection
described in the entry's **What v2 adds**).

### F3 — the 13 class answers were committed *in the freeze*, and the claim calls the result "held-out"
`git log --diff-filter=A -- .ufo/waves/round-40/w1/artifacts/R40C2HeldoutGen/dev-run` → `7fce3086`
(the freeze, 16:13:52-03:00). That commit carries `c2-dev-scores.json` with
`controls["ADOPTED:SKILL.md"] = {matched: 26, meets_target: true}` and
`interpreter-vs-generator.txt` = `interpreter vs generator: 26/26 (label, action) pairs agree`. So at
the freeze the lane held a response for **all 13 classes**. The held-out run changes the bytes, not
the decisions; it re-observes. The claim (`plans/round-40-claims.md:102`) and the entry
(`corpus/knowledge/2026-10-26-r40-sqfs-triage-v2.md`, **Scoring**) call it a "held-out set" without
that note.
`QUALITY.md:44` is the rule: a test whose answers the lane already holds is called a
**re-observation**, and *"the count of pre-seen items is committed with the freeze"* — the count is
committed, the word is not. The claim's own kill rule (`claims:120-121`) treats `26/26` on the 26 dev
envelopes as a stop condition; the adopted table reached exactly that and was exempted by being
called "ADOPTED" rather than "a control". That exemption is defensible in letter (a table scoring on
its own filtered dev set is expected, not a shortcut) but it should be said out loud.
*Smallest safe correction*: in the claim and the **Scoring** paragraph, "held-out **bytes**; the 13
decisions were already answered by the dev run committed with the freeze" — one clause.

### F4 — the eighth field is inert: a seven-field table scores 26/26
Setting every `dependencies` cell of the 11 v2 rows to `*` (artifact `table-nodeps.diff`) scores
**26/26** with the frozen interpreter on the same envelopes. `D` is redundant with `H` on this class
set — a `missing-extractor-dependency` gap with `squashfs_v4_be` always names `sasquatch-v4be`, with
`squashfs_v4_le` always `sasquatch` — and every other row declares `D = none` or `*`. `SKILL.md:348-350`
says the table "reads eight fields … the six of rule block 18 plus `operation` and `provider.id`";
seven decide it. The entry's **Limits** discloses that "a table with one load-bearing cell per label
can also score every envelope" and that provider is not tested alone; it does not disclose that a
*declared* input never reaches a decision.
*Smallest safe correction*: drop "reads eight fields" to "screens eight fields; seven decide the
scored classes and `D` is redundant with `H` on them" (or add a `dep-missing-other` envelope where
`D` is the discriminator — out of scope for a frozen table).

### F5 — row 4's `action` contradicts its own `cause`; the row's damage branch is instructed, not labelled
`avm-marker-be-dropped` (`SKILL.md:368`) has `action = wrap-extractor-be`, and its `cause` says: *"walk
the inode-table metadata headers little-endian first: if they land on `directory_table_start` the image
is AVM layout and its failure is damage (**keep it**); otherwise rerun through a PATH wrapper …"*. The
row's answer for the branch it names is therefore `preserve-failure`, but the scored action is
`wrap-extractor-be`. Both branches share the row's feature vector (`H=squashfs_v4_be`,
`G=extractor-failure`, `D=none`, `BE=no`), so a reader acting on the *action column* — the interface the
claim sells, "(label, action) pair" — wraps a damaged genuine AVM-layout image, the exact error C1 spent
the round separating (marker ≠ layout). No held-out envelope reaches the branch: `H17`/`H18` are the
doctored-marker standard-BE case. The entry discloses that `cause` is unscored; it does not disclose
that `cause` here prescribes a *different action* than the scored cell.
*Smallest safe correction*: split the row — `avm-genuine-damaged` (`G=extractor-failure`, `BE=no`,
`P=*`, preceded by the layout pre-check in its cause) → `preserve-failure`, before row 4 — or delete
the "keep it" branch from row 4's cause and state the layout pre-check once above the table as a
procedure that selects the row to apply. `preserve-failure` already exists in the vocabulary, so the
fix is in-grammar.

### F6 — gap kinds match as exact sets, so a partial failure with escaping links is told `expect-link-absent`
`triage.py:604` is `frozenset(values) == payload`: a row's gap-kind cell must **equal** the envelope's
gap-kind set. Consequences, measured with the frozen interpreter:

- The round's own C1 carriers are all `unclassified`: `V1/V2/L1/L2` carry
  `G = {depth-limited, unpublished-entry}` and no row carries that set (`in-tree-symlink-metadata`
  requires exactly `unpublished-entry`). This is **disclosed** in the entry's Limits ("not covered: …
  `depth-limited` envelopes"), and the frozen gap rule (`c1/gap-rule.json`, `structural.depth-limited: 1`)
  makes that the designed C1 profile — so it is an inherited ceiling, not a regression.
- **Undisclosed**: `H11` plus one injected `extractor-failure` gap (a partial extraction: 5 files
  published, one link escaped, one kept) is labelled `escaping-symlink-removed` / `expect-link-absent`
  (row 8, `G=*`). The reader is told to look for an absent path and loses `salvage-partial` ("keep the
  published files … mark the run incomplete"). No selftest case has a multi-kind gap set: the mixed
  fixture is asserted to have `G == ['unpublished-entry']` (`c_mixed_before_escaping`), and the only
  ordering case is a two-row synthetic.

This is the one finding that produces a **harmful** instruction rather than a missing one, and it hits
the two new rows' own subject matter (partial failure + symlink mix) on a realistic combination.
*Smallest safe correction*: make the failure rows *contains*-matches (partial/body/avm match when the
set includes `extractor-failure`, which is already tested before the symlink rows) and keep exact
equality only for the `none` cells; add the selftest `G={extractor-failure, unpublished-entry}` → row 6.

### F7 — block 18's supersession says "routing", and block 18 still carries actions
`SKILL.md:331-333`: *"Superseded **for routing** by rule block 19 (table v2, round 40); this v1 table stays
as the round-39 record and mislabels mixed-link images, partial failures, empty trees and non-firmware
envelopes"*. The sentence is placed before the v1 table and its four-item list is **accurate** — I
measured the v1 misses on the scored set (F1) and they are exactly those four classes. But the scope word
is "routing": block 18's `cause -> action` cells still carry procedures (`install the sasquatch-v4be
4.5.1 binary on that PATH`, `rerun through a PATH wrapper … that appends -be`), and the only one that is
now *wrong* — the avm row's unconditional wrapper — is exactly the refinement v2 made (F5) and is absent
from the list of v1 defects. A reader is told v1 is superseded where it needs a label, and left free to
take an action from it where v2 changed the action.
*Smallest safe correction*: `Superseded for routing and for the action column` (or `take no action from
this table`), and add the avm row to the list — the v1 sentence already has the room.

## The four questions I was set

1. **Did the craft section really move?** Yes — `33 / 1` lines in one commit (`7fce3086`), block 19 with
   the v2 marker, actions line and 11 rows, block 18 gaining the supersession sentence; v1 bytes
   unchanged; base refused with exit 2; table bytes identical at freeze and measured; a post-freeze edit
   is refused by the counter. No finding.
2. **Re-scoring v1 ground or new decisions?** Both, and the ratio is unfavourable to the headline:
   measured on the scored set, **18/26 v1**, **2/26 abstention**, **6/26 new** (3 classes); 13 independent
   decisions, not 26.
3. **Inflated by the two out-of-domain envelopes?** Marginally, and not for free: the guard costs
   exactly 2 (`CTL-C2-4` = 24/26), the entry discloses that operation and provider move together. Their
   real weight is that they are *abstentions*, not triage — 7.7 % of a 26-envelope headline that already
   includes 69 % v1 ground.
4. **Do blocks 18 and 19 conflict?** Not on routing — the supersession sentence is placed before the v1
   table, is accurate, and the reader is warned. Two live seams remain: the "for routing" scope (F7) and,
   stronger, a conflict **inside** block 19 — row 4's `action` versus its own `cause` (F5), plus row 8
   swallowing combined gap sets with a wrong action (F6).

## What I could not falsify

- The counter's arithmetic, bindings and receipt: independent re-run, exit 0, `bindings_false: []`,
  `frozen_paths_changed: []`, `met_target_consistent: true`.
- The freeze discipline for the table: an edited table in a sandbox clone is refused
  (`v2_table_identical` false, `met_target` false).
- The controls' non-triviality: catch-all 4/26, rotated actions 2/26, v1 transcribed 18/26, no guard
  24/26 — none reaches the target, so the claim is not a do-nothing pass. (Row 48/50's demand.)
- The cited sources: `S112`, `S118`-`S121`, `S123` rows exist and the round-39 evidence rows
  `corpus/evidence/round-39/c1/K5,K6/after.json` the mixed row cites resolve. (Note: the counter never
  checks this — F6's placebo table with `source = -` scores 26/26 — but the citations are in fact
  resolvable, so this is a scoring blind spot, not a citation defect.)

## Axes: does C2 move depth?

`AXES.md:11` defines depth as *"verifiable technical detail — decision tables with real thresholds,
named error signatures, cited sources"* with the bar *"a reader can act on `SKILL.md` alone"*. Judged by
the surface: the craft section gains 11 rows, a domain guard, an action token per label and a
layout-discrimination procedure — **a real, if narrow, depth increment** (3 rows + guard). Judged by the
measurement: the 26/26 scores none of the axes' named substance (placebo cause/source = 26/26), is
dominated by v1 ground, and its expected answers come from the generator's own class map. Judged by
the bar: on the round's own four measured carriers the table returns `unclassified`, and on a realistic
combined gap set it returns a wrong action. Net: **depth moved; the MET verdict overstates by how much,
and two rows should not ship as written.**

## Limits of this review

- I did not re-run REA/unblob on any carrier (no vendor bytes, no new runs); the C1 carrier
  classifications use the committed `after.json` receipts.
- `SKILL.md` in the working tree is modified by another seat (` M SKILL.md`, tip `0b15c8b2` ≠ measured
  `42c10a58`); every SKILL read used `git show 42c10a58:SKILL.md`, so nothing here depends on that edit.
- F2's "intent" reading is inference; its mechanism is observed in `manifest.json` and the generator's
  class construction.
- No tool installed, nothing frozen, no VCS mutation; the sandbox clone lives at
  `/fast/scratch/hyaku/kaidoku-r40/R40W2C2AxisFit/fx.*` and the whole scratch tree is removed.

Report: .ufo/waves/round-40/w2/R40W2C2AxisFit.md
