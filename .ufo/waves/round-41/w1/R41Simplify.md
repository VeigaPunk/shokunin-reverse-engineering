# R41Simplify — YAGNI review of what round 41 ports from the round-40 counters

**Verdict: DONE** — 15 deletion candidates ranked by safety (13 applied to scratch copies with the
surviving selftests green; 2 ranked but not applied), 2 structural candidates, 1 explicit
anti-candidate (`run.json`/`oracle-run.json`/`provenance.json` must stay), 4 deletions the draft's own
text *forces*, and 10 defects: 4 clauses no ported code can grade, 3 claims that are process rather
than data, and 3 places where the port and the draft disagree.
The safe tier was applied to scratch copies and the surviving selftests pass: c1 2217 → 2044 lines
(74/74 cases), c2 1364 → 1288 lines (38/38 cases). No lane file was edited, no VCS mutation, no
extractor run on any carrier.

Seat: simplifier (leaf). Report at `.ufo/waves/round-41/w1/R41Simplify.md`; artifacts in
`.ufo/waves/round-41/w1/artifacts/R41Simplify/`. Scratch `/fast/scratch/hyaku/kaidoku-r41/R41Simplify`
removed at exit; no scratch path is cited as evidence.

## Axes (Godspeed)

| axis | what this review moves |
|---|---|
| **coverage** | C1: the four carrier-oracle/symlink/gap checks must survive while the *duplicate* authorities around them (a second instrument, a second projection-profile convention, a second "unchanged" check) go |
| **depth** | C2: the graded decision must be the (label, action) pair against an independent evaluator, not the row index the port carries from round 40 |
| **calibration** | the gap between what `plans/round-41-claims.md` asserts and what the ported code can enumerate (6 items, §6 — all of them round-40 lessons that recurred) |

## Method

For each candidate I asked the round-40 simplifier's question, sharpened: *which clause of
`plans/round-41-claims.md` becomes weaker or ungraded if this is deleted?* A candidate that weakens
no named clause **and** removes a second convention, an unused option, or a duplicate check is a
deletion. Every candidate was then applied to a scratch copy (never the lane) and the counter's own
`--selftest` was run to see whether a surviving case depended on it — the counts below are measured,
not estimated, except where marked [EST].

Deletion proof: there is **no `lsp` device in this session** (`read xd://lsp` → `No such tool`), so
candidates were proved by an `ast` Load-reference scan (`artifacts/callsite-scan.txt`: c1 45
top-level defs / 0 unreferenced, c2 30 / 0) plus the patched-variant selftests. No cold-start LSP
result was recorded as absence.

## 1. What the two claims actually bind vs what the code binds

P41-C1 names, in one sentence, 17 per-carrier properties plus documentation and freeze integrity.
Mapping them onto the round-40 counter shows three kinds of port work:

| P41-C1 phrase | round-40 code | port action |
|---|---|---|
| four frozen carriers, target 4 | `carriers_spec`, `IDS`, `TARGET` | rename ids; keep |
| receipt `--max-depth 1`, unblob 26.6.4, sasquatch-v4be 4.5.1 | **nothing binds depth or versions** | **add** (§6 D-1, D-2) |
| first added in a commit descending from the freeze | `receipt_fresh` | keep |
| `squashfs_v4_be`, no failed chunk | `handler_ok`, `chunks_ok` | keep |
| every oracle file at the **exact** path + sha256 | `same_rel` (suffix!) | **replace** (R40-CL1) |
| no non-regular entry at its exact path | `nonregular_published` + `same_rel` | **replace** (same function) |
| gaps only as the gap rule allows | `gap_check` (path + structural families) | keep whole |
| subject digest = pin, recomputes to its evidence id | `subject_pin_ok`, `evidence_id_ok` | keep |
| carrier pin + AVM marker + LE block lengths | `layout_probe` | keep (identity tiebreak load-bearing) |
| counter-time rerun, same `plus-extractor` projection | `projection`/`projection_diff` | **fix the profile** (§2 M1) |
| vendor fetch chain image → **member** → carrier | external validation has no `member_sha256` | **add** (§6 D-2b) |
| SOURCES row **absent at the base**, used-by lists it | `sourced` checks a shared date | **add** base-absence (§6 D-4) |
| frontier note names the heading, stem, what it supersedes | `frontier_note` checks 2 of 3 | **add** supersession (§6 D-4) |
| frozen **independent** oracle | none in the counter (the oracle is data); `c1-extra.py` re-derives it, and that gate is already ported | fold in (X1) or name it in the Target (D-5) |

P41-C2 names: v3 marker + table bytes = freeze bytes; every envelope's (label, action) equal to a
**frozen independent evaluator's**; seed = freeze hash; carriers regenerate byte-identically; the
generator's own expectation agrees with the evaluator; two replicates per class. Nothing about
block 18, nothing about row indices, nothing about envelope ordering. That is what §3 deletes.

## 1a. Port state observed at review time (untracked in the lane)

`git status` at `49096c7e` shows three untracked paths: `plans/round-41-claims.md` (the draft),
`.ufo/waves/round-41/` (this wave) and `tools/round-41/`. The last one already carries **five** ported
tools — `c1-extra.py` (389 lines, grown from 262), `c1-run.sh` (606), `fetch-vendor.py` (424, from
190), `mk-l-carriers.py` (282), `sqfs-list.py` (1585) — and **neither counter** (no
`tools/round-41/c1-counter.py`, no `c2-counter.py`). Three consequences for this list:

1. **`member_sha256` is already fixed in the port** (§6 D-2b corrected): `tools/round-41/fetch-vendor.py:199-208`
   requires `external.member_sha256` and fails closed with link `member_sha256` when the spec omits
   it. The remaining gap is that the counter's `carriers_spec` does not require the key, so a spec
   that omits it passes the counter and fails only at fetch time.
2. **The gate grew, and is now stricter than the draft** (D-8): its `frontier_content` also demands
   the round-40 "measured, not promoted" record phrase, which the draft's predicate does not state.
3. **The gate keeps a cross-round reader fallback** (D-9): `tool_dir()` prefers
   `tools/round-41/sqfs-list.py` but silently falls back to `tools/round-40/sqfs-list.py`, which
   contradicts the gate's own "reader bytes AT THE FREEZE" claim and lets the oracle be re-derived by
   a reader the freeze does not name.

## 2. C1 removals, ranked by safety (safest first)

The patch `artifacts/c1-yagni.diff` is the measured safe tier + the forced replacement:
`+157 / −330`, 2217 → 2044 lines, `--selftest` 74 cases green.

| # | candidate | size | clause it would weaken if deleted | risk | measured |
|---|---|---|---|---|---|
| **1** | `carriers_unchanged` + `gap_rule_unchanged` (three lines in `measure`, two in the `met_target` formula, two in `main`'s summary print) | 7 lines | none — `frozen_drift` already inspects every commit in `FREEZE..REV` for `CARRIERS` and `GAPRULE` (both are in `FROZEN_PATHS`) and exits **2** `frozen_path_changed`, which is strictly stronger than "bytes differ at REV" | none | cases *carriers.json changed after freeze*, *-touched-then-restored*, *gap-rule changed/restored*, *claims edited* all still exit 2 via drift |
| **2** | `frozen_tables_valid` binding | 4 lines | none — `gap_rule_model()` already returns a problem for "not a JSON object", so `gap_rule_ok` is false on exactly the same input | none (the receipt loses one granular flag) | case *gap rule is JSON but not an object* retargeted to `b:gap_rule_ok`, still red |
| **3** | `--no-rerun` option and its 12-line branch | 13 lines | none — the rerun is part of P41-C1; an unknown flag already exits 2 (`argparse`), the same unevaluable class | loses the `rerun_disabled` reason token; nothing in `c1-run.sh` references it | no selftest case existed (dead by construction) |
| **4** | per-carrier `receipt` key + its validation + the `receipt_override` fixture hook | 9 lines | none — round-40 `carriers.json` never uses it; P41-C1 names one receipt location per carrier | the claim must state the convention `corpus/evidence/round-41/c1/<id>/after.json`, else the path is unstated | `spec_json(receipt_override=…)` was never called by any case |
| **5** | `meta_flag_le` / `meta_flag_be` / `block_size` decodes in `layout_probe` | 3 lines | none — nothing reads them; `layout_ok` is decided by `le_plausible`/`le_identity` | none (report-only fields) | no case reads them |
| **6** | `compression_coverage` binding, `GZIP_ID`, `XZ_IDS`, `d['compression']` | 8 lines | P41-C1 does not claim leg coverage; the L3/L4 bytes are sha-pinned at the freeze, so the compressor identity cannot drift | an authoring error (both lane carriers on one leg) would no longer fail a score; the draft's own carrier bullet ("L3 xz, L4 gzip") is the only guard left | case *no xz carrier* rewritten as a green invariant (*every carrier on the xz leg still scores*) and passes |
| **7** | projection **profile choice**: `PROFILES`, `DEFAULT_PROFILE`, `PROJECTION_KEYS_BY_PROFILE`, the `carriers.json` `'projection'` key, the profile branches in `projection()`/`projection_diff()`; `carriers.json` naming a profile becomes a `carriers_spec_ok` problem | ~35 lines + 1 case | **strengthens** `projection_ok`: a freeze can no longer downgrade to `core`, which the round-40 code documents as oracle-closed ("a forger holding the oracle and non-regular tables can reproduce it without running") | the freeze loses the ability to *re-measure* the weaker profiles; the case documenting that calibration limit disappears with them (the invariant case stays) | 74 cases green; the oracle-closed fabrication (`published_bytes + 1`) is still refused |
| **8** | `selftest_rea` + `DEV_AVM_IMAGE` + `--selftest-rea` | 165 lines + 5 | none — it exercises no clause; it is an entry point | loses the only pre-freeze *real* two-run projection-stability proof; also its hard-coded `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs` repeats closure **D1** (lineage outside the lane repo) | replaced by P41-C1's own QUALITY-83 dry run on the four *committed* dev carriers, which is a real-run check on lane bytes; `--selftest` unchanged (74/74) |
| **9** | `OPENED = '2026-10-26'` and the `opened`-cell check in `sourced` | 2 lines + 3 | none *after* §6 D-4: P41-C1 replaces "opened this round" with "row absent at the base", which makes the date constant dead (and the date is shared by rounds 39 and 40, so it never separated rounds — round-40 defect #14) | deleting it *without* adding base-absence makes `sourced` vacuous | dependency stated; the base-absence check is `c1-extra.py`'s `sourced_new` |

Forced, not optional (the draft *cannot* be scored without these):

| candidate | why it is forced | evidence |
|---|---|---|
| `same_rel` → `extract_rel` + exact equality, applied at all three call sites (`oracle_hits`, `nonregular_published`, `gap_check`) | P41-C1 requires exact paths, and P41-C1's L3/L4 carriers are explicitly built with **both-direction nested-name collisions**. Under the suffix rule the regular file `…_extract/usr/bin/busy` satisfies the symlink entry `bin/busy`, so `nonregular_unpublished_ok` fails on a faithful extraction — the claim would fail on its own carriers | prototype `.ufo/waves/round-40/w2/artifacts/R40W2C1Refreeze/c1-counter-exact-match.diff`; 5 collision cases (incl. the reverse direction and the materialised-link case) all green in the variant |
| round-40 path constants (`CARRIERS`, `GAPRULE`, `AFTERDIR`, `ENTRY`, `STEM`, `CORE_HEADING`, `FRONTIER_MARK`, `PROV_SEGMENT`, `IDS`) | round-41 paths; `PROV_SEGMENT` is the one to think about (§6 D-3) | — |
| docstring lines tied to the deleted code | the module docstring *is* the predicate text embedded in the scorer; leaving `--no-rerun`, the four profiles, `compression_coverage`, `frozen_tables_valid` or "same relative-path suffix" in it recreates exactly the prose/code drift that R40-CL5 was filed for | the patch fixes them |

## 3. C2 removals, ranked by safety

Patch `artifacts/c2-yagni.diff`: `+8 / −84`, 1364 → 1288 lines, `--selftest` 38/38.

| # | candidate | size | clause it would weaken if deleted | risk | measured |
|---|---|---|---|---|---|
| **1** | **v1 / base invariance** entirely: `MARKER_V1`, `derive_base`, `commits_touching`, `--base`, `v1_table_present`, `v1_table_identical`, `res['table']['v1']`, plus the now-dead fixture data (`V1_HEADER`, `V1_ROWS`, the `v1_base`/`v1_freeze`/`v1_rev` plumbing, ~30 more lines) | ~80 lines, 3 cases | none — P41-C2 names no block-18 property | **round 41 is going to edit block 18's verb** (the draft's own prose-repair list: "L1 (block-18 verb)"), so a byte-identity check on the v1 table would be *actively wrong* next round | 3 cases deleted; 38/38 green |
| **2** | `arms_valid` (`arm ∈ {after, before, ood}`) | 3 lines | none — no clause reads `arm`; it is a hard-coded vocabulary that duplicates the generator, and round 41's combined classes may introduce a new arm value, which would fail a valid manifest | none (ids/classes bindings remain) | no case ever exercised it (dead by construction) |
| **3** | `manifest_before_envelopes` + the `envelope_first_add` loop | 6 lines, 1 case | none — P41-C2 names no ordering; `manifest_after_freeze` is kept | a manifest may predate its envelopes; the table-bytes and regeneration bindings still bind the data | case deleted; 38/38 |
| **4** | envelope-path inference from the carrier's sibling directory | 9 lines, 1 case | none — the round-41 manifest is written by the round-41 generator, which can name `envelope` | the manifest must name `envelope` per carrier (make it a spec problem, not a silent `None`) | case *envelope path omitted, sibling inferred* inverted to *manifest entry without an envelope path cannot be scored* (exit 1, `envelopes_valid` false) |
| **5** | `writer_matches_manifest` | 2 lines | none — the binding passes vacuously when the manifest omits the writer sha | loses the check that the materialised writer is the declared one; `res['writer']` still records both shas | no case (dead by construction) |
| **6** | **row / decision machinery**: `infer_index_base`, `parse_table_only`, `TABLE_ONLY_LINE`, `parse_v2_rows`, `parse_tab_results`, the tab and `--table-only` fallbacks, `NOMATCH_PAIR`, `distinct_decisions`, `distinct_row_list`, `row_decisions_consistent`, `decision_pairs`, `row_source` | ~150 lines [EST], 7 cases (of 42) | P41-C2 grades the **(label, action) pair against the independent evaluator**; the row index is not a decision in the new predicate, and `row_decisions_consistent` (same pair ⇒ same row) is an ambiguity check the evaluator subsumes | (a) the counter must then require the v3 interpreter's `--json` to carry `label` and `action` for every envelope — pin that in the freeze; (b) keep a 3-line anti-silence binding ("any envelope without a label+action is unevaluable"), or a table that silently matches nothing reads as "not met" for the wrong reason; (c) four of the seven cases become *interpreter contract* cases, not red controls | not implemented in the variant (fixture rewrite); the 5 non-row deletions above were implemented and green |

Also dead in c2 and cheap to drop with #1: `CLAIMS` in `FROZEN` stays (it is freeze integrity), but
`skill_doc(v1_rows, …)`'s first parameter and the `ABSENT` sentinel exist only for the v1 cases.

## 4. Selftest cases that only test removed code

**C1 (70 cases; the port also inherits 5 collision cases from the prototype, so 74-75):**

| case | after the deletion |
|---|---|
| `no xz carrier (compression coverage)` | only tested `compression_coverage`; rewritten as a green invariant |
| `gap rule is JSON but not an object at the freeze` | only tested `frozen_tables_valid`; retargeted to `b:gap_rule_ok`, still red |
| `explicit core profile accepts a projection-identical (oracle-closed) fabrication` | **delete** — it exists only to demonstrate the `core` profile |
| `unknown projection profile in carriers.json` | rewrite: naming *any* profile is now a `carriers_spec_ok` problem |
| *(none)* for `--no-rerun`, `--selftest-rea`, the `receipt` key, `meta_flag_*`, `block_size` | dead by construction — no case ever touched them |

**C2 (42 cases → 38):**

| case | after the deletion |
|---|---|
| `v1 table edited after freeze` | delete (v1 check gone) |
| `v1 block removed at rev` | delete (idem) |
| `explicit --base equal to derived base` | delete (`--base` gone) |
| `envelope before manifest` | delete (`manifest_before_envelopes` gone) |
| `envelope path omitted, sibling inferred` | invert (see §3 #4) |
| `green: all bindings, labels and actions` | drop `v1_table_present`/`v1_table_identical` from its `want_true` list |
| *(none)* for `arms_valid`, `writer_matches_manifest` | dead by construction |
| `tab interface…` ×3, `json results without row index`, `interpreter reports rows only` ×2 (`rowonly`, `rowonly1`), `interpreter reports rows only and v2 header lacks action` | go only if §3 #6 lands: 2 survive as JSON-contract cases, 5 collapse into one "no label+action in `--json` ⇒ unevaluable" case |

## 5. What must not be deleted (the traps)

1. **`gap_check`'s two families.** The structural family (`relative_path: null`, allowance per kind)
   is not optional for round 41: P41-C1 mandates `--max-depth 1` receipts, and a depth-1 run on V4
   (the *full* 5491 rootfs) will emit many `depth-limited` null-path gaps. If the frozen round-41
   `gap-rule.json` keeps round-40's `structural: {"depth-limited": 1}`, every vendor carrier fails
   `gaps_ok`. This is a data calibration to settle at the freeze, not a code deletion. [INFERENCE on
   the count; the mechanism is in `gap_check` and was exercised by 4 structural cases.]
2. **`required` in the gap rule.** It is what distinguishes a materialised symlink from a clean
   extraction (the *required gap missing* case). Deleting the `required` map weakens `gaps_ok`.
3. **The layout identity tiebreak** (`le_identity` when both decodes are plausible). On vendor
   superblocks the first metadata block length can be plausible both ways; without the identity
   test `layout_ok` becomes a coin flip.
4. **`evidence_id_ok`.** P41-C1 names "recomputes to its evidence id" explicitly (round-40's
   simplifier recommended dropping it; the L1 kept it and round 41 re-states it). It is also the only
   clause that makes `parameters` (hence `run_provenance_ok`) tamper-evident.
5. **`receipt_fresh`.** `is_ancestor(freeze, first_add) and first_add != freeze` is what kills
   "receipt committed in the freeze commit".
6. **`carriers_spec`'s external-shape validation** — but it must *gain* `member_sha256` (§6 D-2b),
   the key round-40 committed but nothing reads.
7. **`frozen_drift`'s path set.** If `c1-extra.py` is folded in (§X1), the oracle reader
   (`sqfs-list.py`) and the lane builders (`gen-squashfs.py`, `mk-l-carriers.py`) must stay frozen:
   they are the reproduction chain for pinned bytes.

## 6. Draft defects (the inverse list: what the port must **add**)

These are clauses P41-C1/P41-C2 assert that no ported code can grade. Each one is a round-40 lesson
recurring, which is the calibration finding of this review.

| id | draft text | why it is ungraded | cheapest fix |
|---|---|---|---|
| **D-1** | "(`--max-depth 1`, unblob 26.6.4, sasquatch-v4be 4.5.1)" inside P41-C1 | the counter replays whatever depth the receipt records (`REPLAY_PARAMS`); nothing compares it to 1. Round-40 `carriers.json` even carried `"rea_parameters": {"max_depth": 1}`, **a key no code reads** | either add `parameters.max_depth == 1` as a clause (one line in `measure`, and read the frozen `rea_parameters` if it stays), or drop the parenthetical |
| **D-2** | "unblob 26.6.4, sasquatch-v4be 4.5.1" | no clause reads a version (round-40 lesson #3 recurs) | bind them from the receipt evidence dir's `run.json` (which already records both, plus the sasquatch-v4be path/sha256) or mark "not graded" |
| **D-2b** | "the fetch chain checks image sha256 → **member sha256** (R40-CL6) → carrier sha256" | **the chain is fixed in the port** (`tools/round-41/fetch-vendor.py:199-208`, fails closed when `member_sha256` is absent) but the *counter's* `carriers_spec` still validates only `url`/`image_sha256`/`member`/`length`, so a `carriers.json` that omits `member_sha256` passes the counter and fails only at fetch time (exit 1, not a spec problem) | require `member_sha256` (64 hex) in `carriers_spec`'s external key list, and delete the `receipt`-style optionality |
| **D-3** | `run_provenance_ok` at `/kaidoku-r41/` vs the QUALITY-83 dry run | the dry run "scores the round-40 V1/V2/L1/L2 receipts 4/4"; those receipts record `/kaidoku-r40/…` in `parameters.output_directory`, so a `-r41` segment check makes the dry run 0/4 on a clause that is not about the carrier | decide at the freeze: accept `/kaidoku-r4[0-9]/` (still anti-relabel, since `parameters` is hashed into the evidence id), or state the dry run as "4/4 on every clause except provenance" |
| **D-4** | "cites a SOURCES row **absent at the base** whose used-by lists it"; "a frontier note names that heading and the entry stem and **says what it supersedes**" | the counter's `sourced` checks a *date* both rounds share and `frontier_note` checks only marker+stem+AVM token; the base-absence and supersession semantics live in the **second instrument** `c1-extra.py` (`sourced_new`, `frontier_content`) | fold those two bindings into the counter (see X1) and delete `OPENED` |
| **D-5** | "Target: `carriers_matched == 4`, every binding true, **supplementary gate met**" | "the supplementary gate" is named nowhere in the draft: no file, no exit code, no binding list. Round 40's *frozen* text named it (`python3 -I -B tools/round-40/c1-extra.py --root … --rev … --freeze … --base … --carrier-cache … --json-out …`, exit 0 — `.ufo/waves/round-40/w2/artifacts/R40W2C1AxisFit/claims-at-freeze.md:74`), so the draft dropped the only enumerable part of the phrase | name the instrument, its argv and its three bindings in the Target sentence, or fold them into `BINDINGS` and drop the phrase (X1) |
| **D-6** | "none of which any REA or unblob run touched before the freeze" (appositive inside P41-C1) | unobservable from git — an unrun check is not a clause (round-40 lesson #18 recurs; the same sentence already appears as a process note in the carriers bullet) | delete the appositive from the predicate sentence; keep the bullet |
| **D-7** | C2: "the frozen independent evaluator (written from the precedence text … never reading the table, the interpreter or the generator's class map)" | the *ordering constraint* is process, not data: nothing in the repo shows the evaluator was written first | cheap, honest fix: freeze the evaluator in a commit that precedes the table commit, and bind `first_add(evaluator) < first_add(table-block)` — or mark it not graded |
| **D-8** | "a `Round-41 frontier note` … names that heading and the entry stem and says what it supersedes" | the **ported gate is stricter than the draft**: `tools/round-41/c1-extra.py:142-156` (`note_verdict`) also requires the round-40 "measured, not promoted" record phrase (`R40_RECORD`) on the same line. A PROVINCE.md written to the draft's three conditions fails the gate | state the fourth condition in the predicate, or drop it from the gate; either way one text |
| **D-9** | (no draft text) | `tools/round-41/c1-extra.py`'s `tool_dir()` silently falls back to `tools/round-40/sqfs-list.py` when the round-41 reader is absent, so `oracle_rederived` can pass on a reader the freeze does not name — the check then proves a different producer agrees, not the frozen one | make the round-41 path mandatory (exit 2 when absent); keep the fallback only inside `--selftest` |

## 7. Structural candidates (biggest weight, needs the L1's call)

**X1 — fold `c1-extra.py` into the counter, or name it in the Target — but stop paying for both.**
The port already carries the gate (`tools/round-41/c1-extra.py`, 389 lines, +127 on round 40) and not
the counter, so this decision is pre-freeze, not post-hoc. P41-C1 states `sourced_new` ("absent at
the base"), `frontier_content` ("says what it supersedes") and `oracle_rederived` ("frozen
**independent** oracle") *inside the same sentence* as the counter's own bindings; two instruments for
one predicate mean two exit codes for one score, duplicate `show`/`sids`/`scratch` helpers,
duplicate `ENTRY`/`STEM`/`HEADING` constants, and a Target sentence that cannot be evaluated from one
receipt. Folding in costs one python-only reader run at scoring time (`sqfs-list.py --layout avm`,
stdlib, no extractor) and deletes 389 lines plus a `FROZEN_PATHS` entry. Risk: the *scoring argv*
changes (one instrument, one receipt); `score-receipt.sh` takes the counter argv generically, so it
needs no edit, and `c1-run.sh` never invokes a counter (it is a producer harness). If the L1 keeps
the two-instrument split, then D-5 must name the gate, its argv and its three bindings in the Target
sentence — and D-8/D-9 must be settled either way.

**X2 — `c1-run.sh`'s `oracle` arm (604-line harness) stops being a *scoring* dependency** once X1
lands: the counter re-derives the oracle from the frozen reader itself, so the harness is the
operator's runbook, not the evidence. Keep the harness, drop it from `FROZEN_PATHS` (the claim never
names it) — but only after X1, because today the oracle's cross-check (`sasquatch-v4be` agreement) is
recorded in `oracle-run.json` and read by nobody. Tradeoff: after X1 the *cross-check* is ungraded;
the reader-vs-receipt comparison is graded.

**X3 — do not delete the three unread sidecars** (`run.json`, `oracle-run.json`,
`provenance.json`): they are the only place the tool versions D-2 needs are recorded, and they cost
no code. Bind from them; do not delete the receipt-side `score-receipt.sh` exit-code record either
(the freeze rule "every score receipt records the scorer's exit code" needs it).

## 8. Totals and evidence

| file | base | after safe tier | delta | selftest |
|---|---|---|---|---|
| `tools/round-40/c1-counter.py` | 2217 lines / 105417 B / sha `8d288e4c…` | 2044 / 95569 / sha `8995a21b…` | **−173 lines** (patch +157/−330) | 74/74 cases, exit 0 |
| `tools/round-40/c2-counter.py` | 1364 / 62703 / sha `9bd79249…` | 1288 / 59039 / sha `2d9c1161…` | **−76 lines** (patch +8/−84) | 38/38 cases, exit 0 |
| `tools/round-41/c1-extra.py` (X1) | 389 lines in the port (262 at the base) | 0 if folded into the counter | **−389** | gate has its own `--selftest`; not run here (it needs `--tools DIR`) |
| `tools/round-41/{c1-counter,c2-counter}.py` | **absent** | — | the port must still be written; every candidate above lands in it | — |

The two patches plus every command, version and output are in
`artifacts/R41Simplify/{c1-yagni.diff,c2-yagni.diff,callsite-scan.txt,selftest-evidence.txt}`.
They apply to the base blobs, not to the lane tree (nothing was edited there).

One port note that is not a deletion: c1's `met_target` consults the explicit `BINDINGS` tuple, so
diagnostic keys may sit in `bindings` safely; c2's `bindings_ok = all(v is True for v in b.values())`
iterates **every** key, so any diagnostic boolean added to `b` silently becomes a binding. Round 41
should use an explicit tuple there too (calibration of the same kind as `frozen_tables_valid`).

## 9. Tradeoffs / what I did not decide

- **Deleting the profile choice also deletes the evidence for why `plus-extractor` is required.** The
  invariant case (`published_bytes + 1` is refused) survives; the `core`-accepts-fabrication case does
  not. I judged the invariant the load-bearing one; if the L1 wants the calibration artefact in the
  scored file, keep `PROFILES` and only forbid the `projection` key.
- **`selftest_rea` is the only check that a *real* rerun projects identically.** The QUALITY-83 dry
  run covers it on four committed carriers (heavier, and on lane bytes instead of a host path), but
  only if the dry run is actually done pre-freeze. If it is dropped for time, keep `selftest_rea` and
  repoint it at a committed carrier.
- **The row machinery (§3 #6) is the one large deletion I did not implement.** It needs the v3
  interpreter contract pinned to `--json` label+action; that is an authoring constraint the freeze
  must state, which is why it is ranked medium and not safe.
- I did not evaluate whether C1/C2 land — no carrier or envelope data exists yet. Every sizing
  statement is about clause structure and code weight, not extraction.

## 10. Bounds honoured

- Wrote only this report and `.ufo/waves/round-41/w1/artifacts/R41Simplify/`; no lane tool, plan,
  corpus, SKILL, PROVINCE, SCORECARD or fleet-root file touched; no `~/.local/bin` write.
- No VCS mutation (only `git show`/`git log` via read-only commands), no fixture commit outside
  scratch, no subagent, no `agent://all`.
- No REA, unblob, sasquatch or extractor run on any carrier (reserved or development); no network
  fetch; no install or upgrade; no pacman transaction. The selftest's REA runner is in-process and
  simulated; the only external processes were `git`, `python3` and `node tools/round-27/xpin-attribute.mjs`
  inside scratch fixtures.
- Read-only inspection of the untracked round-41 port (`tools/round-41/*`) to compare the draft
  against what the lane already has; nothing there was edited.
- Scratch removed at exit; vendor bytes never copied into the lane (none were downloaded).
