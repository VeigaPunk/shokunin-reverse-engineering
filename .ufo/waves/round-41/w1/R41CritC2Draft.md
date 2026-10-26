# R41CritC2Draft — attack on the DRAFT R41-C2 (SquashFS triage table v3)

**DEFECTS FOUND** — the draft's independence claim is falsified by its own precedence text, its
five "combined classes" carry **zero** decisions of their own, the one genuinely new row is a
function of a run parameter the precedence does not read, and two of REA's six gap kinds have no
clause at all. Every number below was measured this session; the four committed round-40 C1
receipts are the sharpest evidence and were labelled three different ways by three readers.

Seat bounds honoured: writes only this report and
`.ufo/waves/round-41/w1/artifacts/R41CritC2Draft/`; no lane/fleet file, no VCS mutation, no
vendor or reserved carrier opened (REA ran on fresh lane-built trees and on the four committed
round-40 **C1 receipts** only); no installs; scratch `/fast/scratch/hyaku/kaidoku-r41/R41CritC2Draft`
removed at finish. Read-only: `plans/round-41-claims.md`, `SKILL.md`, `corpus/lessons/round-40*`,
`.ufo/waves/round-40/w2/*`, `tools/round-40/*`, `corpus/evidence/round-40/c1/*`, fleet `AXES.md`,
fleet `corpus/QUALITY.md`, and the REA 6.5.0 package. I did **not** read
`w2/artifacts/R40W2C2IndepEval/eval-v2-indep.py` (my item does not name it); nothing below depends
on it.

## 0. The six questions, answered

| # | question | answer |
|---|---|---|
| 1 | is an evaluator written from the precedence text independent of the table? | **No, and it cannot be.** Both are renderings of the same 12 clauses; the test measures transcription fidelity, not triage correctness. It *does* satisfy round-40 D3's letter (labels not from the generator's map) and not its purpose. |
| 2 | does `class_expected` re-introduce the generator's class map? | **Yes, twice.** As a *veto* (disagreement fails the claim) and, worse, the map is a `class → (label, action)` table, so for every combined class it is **identical to a base class's pair** and the check is vacuous — it cannot see that a carrier failed to exhibit its combined feature set (measured: 6/6). |
| 3 | can a table copied mechanically from the precedence pass, and is that depth? | **It passes by construction** (the precedence is already a table: 11 data rows + a guard). That is transcription, not depth; the measured depth delta is **one row**. |
| 4 | which combined classes can REA actually produce? | partial+in-tree **yes** (4/4); depth-limited+in-tree **yes, and it is the modal real outcome** (4/4 committed C1 carriers); depth-limited alone **yes** at `--max-depth 1`; partial+mixed **not observed (0/6)**; depth-limited+mixed **unproven** — see §4. |
| 5 | is depth the right axis? | Depth is the right axis for one row; the rest is **quality** (R40-CL5 prose repairs). `AXES.md:11` asks for "decision tables with **real thresholds**"; v3 has no threshold, while REA itself branches on `maxDepth < 10` (`FirmwarePublication.js:23-24`) — the threshold is right there and unused. |
| 6 | what control/binding is missing? | Six, listed in §6 with red fixtures: expected-source binding, evaluator-before-table ordering, interpreter pin, observed-feature-set binding, real-carrier control, pre-seen/decision count. |

## 1. The precedence text decides **labels only** — the action half is not in it (decisive)

`plans/round-41-claims.md:75-88` gives a pair in clause 1 and **a bare label in clauses 2–12**:

```
 2. no `squashfs_v4_*` handler in H → `no-squashfs-chunk`.
 7. `depth-limited` ∈ G → `depth-limited-nested` (new), whatever symlink gaps accompany it.
```

The predicate (`:90-97`) scores **"(label, action) pair"**. Therefore an evaluator "written from the
precedence text" cannot emit the action for any envelope outside clause 1. I implemented the text
literally and it says so:

```
$ python3 -I -B precedence-probe.py <4 C1 receipts> <4 probe envelopes>
...
# distinct (label, action) pairs the precedence decides on this set: 2
#   ('depth-limited-nested', None)
#   ('partial-body-failure', 'salvage-partial')
# labels with no action token in the v2 vocabulary: ['depth-limited-nested']
```

`depth-limited-nested` — the **only** new label in v3 — has no token in the v2 actions line
(`SKILL.md:362`: `none inspect-input install-extractor-be install-extractor-le wrap-extractor-be
preserve-failure salvage-partial audit-symlinks expect-link-absent count-gap confirm-empty`). So the
evaluator must either borrow the table's own actions line or invent a token, and either way the pair
it produces is **not derivable from the stated source**. This is a QUALITY row-28 failure ("must not
… derive expected outcomes from its decision code") in the design, not in the implementation.

*Smallest safe correction:* state the action in every clause, in the precedence text, e.g.
`2 → (no-squashfs-chunk, inspect-input)`, `7 → (depth-limited-nested, raise-depth)`, `3 → (…,
install-extractor-be|le)`, and freeze the resulting 12-line `label → action` map as a **separate
commit before** the table (§6 B2). Then the evaluator's output is a pair for every clause and the
"never reads the table" sentence becomes true.

## 2. The combined classes carry no decisions — measured on the draft's own precedence

Clauses 4 and 7 say "**whatever other gaps** / **whatever symlink gaps accompany it**". So:

* `partial`, `partial+in-tree`, `partial+mixed` → one label, one action → **one pair**;
* `depth-limited alone`, `+in-tree`, `+mixed` → one label, one action → **one pair**.

The round-40 counter's `row_decisions_consistent` binding (`tools/round-40/c2-counter.py:756-762`)
requires each expected pair to map to exactly one row, so the table is *forbidden* to give a
combined class its own action even if the author wanted to. Consequence: of the draft's
"13 + 5 classes, two replicates each" (36 envelopes), `distinct_decisions` is **13, not 18**, and
the marginal decision content over round-40 is **one row**. Measured on the 8 envelopes above:

```
# distinct (label, action) pairs the precedence decides on this set: 2
```

The claim bills "adds combined-gap-set rows" (`:68`) as the depth increment; measured, the combined
classes add **no rows** — they only test that a row's gap cell is a wildcard, which is exactly the
"33 of 69 cells are individually inert" weakness round-40 already filed
(`w2/R40W2C2Shortcut.md` §2b).

*Smallest safe correction:* either (a) give each combined class its **own action** so it owns a
distinct pair (`partial+in-tree → salvage-partial-and-count-gap`,
`partial+mixed → salvage-partial-after-audit`, `depth-limited+in-tree → raise-depth-and-count-gap`),
which `row_decisions_consistent` permits and which makes the refinement measurable; or (b) keep one
row and say in the claim and the entry: "the depth delta is one pair (`depth-limited-nested`); the
combined classes are absorption controls for clause 4 and clause 7, not new decisions." Option (b)
is honest and cheap; option (a) is what makes v3 worth a round. Either way the phrase "adds
combined-gap-set rows" must go.

## 3. `class_expected` is vacuous for exactly the classes it is meant to police

The draft (`:95-96`): "the generator's own class expectation agrees with the evaluator on every
envelope (a disagreement is reported and **fails the claim**)." Two defects:

**3a — it is a veto, and the cheap way to satisfy a veto is to align the evaluator to the map.**
That is round-40 D3's defect re-entering through the failure consequence: the map is written by the
generator author from the class list, so "disagreement ⇒ claim fails" makes the map a co-authoritative
label source. A correct evaluator that contradicts a wrong map can only fail the round.

**3b — the map stores the same pair for every combined class, so agreement is automatic and blind.**
`heldout-gen-v2.py:1068` writes `'label_actions': dict(ACTIONS)`, a static `class → (label, action)`
map (`ACTION_SETS` at `:105-153`, `interp` vocabulary at `:120-133`); `:908-909` stamps each carrier. Since clause 4 and clause 7 collapse the combined
classes onto a base pair, a carrier that was *built* as `partial+mixed` but *behaved* as
`partial+in-tree` produces the same map pair and the check passes. **Measured:** I built six
carriers from a `partial+mixed` recipe (escaping + in-tree links + `partial` damage) and **all six**
came back `SR = false`, `G = {extractor-failure, unpublished-entry}` — the envelope is
`partial+in-tree`, not the class the recipe names:

```
$ python3 -I -B comboprobe.py … 41c2d0ff1cebabe1
H03  probe-mixed-partial   …  gap_kinds [extractor-failure, unpublished-entry]  symlink_removed false  P 7
$ python3 -I -B nested.py …         # 4 further seeds
seed a1b2c3d4e5f60718 … gap_kinds [extractor-failure, unpublished-entry] symlink_removed false
seed 1122334455667788 … (same)      seed 99aabbccddeeff00 … (same)
seed 0f1e2d3c4b5a6978 … (same)
```

A pair-only `class_expected` check reports "agree" for all six. The binding is therefore not a
check on the held-out set at all.

*Smallest safe correction:* replace the pair check with an **observed-feature-set** binding —
`observed_features[class]` (handler set, gap-kind set, SR, `P > 0`, `depth_limited_paths` shape,
`max_depth`) must equal the recipe's declared set, computed from the envelope at scoring time; any
mismatch fails the **generation** (reported as `class_construction_mismatch`, with the carrier and
its seed) before it can reach a label comparison. And demote the map-to-evaluator comparison from
"fails the claim" to "reported", with the *evaluator* as the expected source (§6 B1). Fix it at
freeze, not at score.

## 4. Reachability: what REA 6.5.0 actually produces (measured)

All runs: `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output [--max-depth N]`,
`REA_UNBLOB_COMMAND=~/.local/bin/unblob`, unblob 26.6.4, sasquatch-v4be 4.5.1. Features computed as
the v2 grammar computes them.

| class in the draft | measured? | envelope features | verdict |
|---|---|---|---|
| partial+in-tree | **yes, 4/4** | `G={extractor-failure, unpublished-entry}`, P 3–7, BE yes | producible |
| partial+mixed | **0/6** | every damaged run has `SR=false` (no `MaliciousSymlinkRemoved`) | not observed; construction-fragile |
| depth-limited alone | **yes** | flat image at `--max-depth 1`: `G={depth-limited}`, P 1 | producible — but see §5 |
| depth-limited+in-tree | **yes, 4/4 real** | V1/V2/L1/L2 receipts: `G={depth-limited, unpublished-entry}`, SR false, P 697/8/7/6 | the modal **real** outcome |
| depth-limited+mixed | **no** | no run produced SR with a depth ceiling | unproven, `[INFERENCE]` likely rare (SR needs a completed extraction; the ceiling run still completed and produced SR=false on the real carriers) |

Two source facts that bound this table and that the draft should state:

* `dist/firmware/FirmwarePublication.js:288-293` — a chunk's `extractor-failure` gap is **suppressed**
  when a dependency row covers that chunk, when `chunk.encrypted`, or when `handler === null`. So
  `G ⊇ {missing-extractor-dependency, extractor-failure}` is impossible **within one chunk** and
  possible only across chunks. That makes the draft's clause-3-before-clause-4 ordering a real
  decision with a real input: a two-chunk task with a dep-missing chunk and a partial-failure chunk
  is labelled `dep-missing-be` → action `install-extractor-be`, and the reader is never told that
  chunk B published salvageable files. The draft added combined handling to clauses 4 and 7 and not
  to 3; that asymmetry is unexplained.
* `dist/firmware/FirmwarePublication.js:273-303` emits six gap kinds and v3 has clauses for four.
  `unknown-chunk-handler` and `encrypted-chunk` (`:286-287`) fall through clause 2 only when the
  *handler set* is empty of squashfs handlers; a task with one clean squashfs chunk and one
  `handler: null` or `encrypted: true` chunk reaches clause 12 → `(unclassified, none)`. That is a
  reachable, informative AVM outcome (encrypted regions are common firmware shapes) labelled as
  nothing. A third hole: `. :161-181` (and `:194`, `:204`) choose `UNNAMED_DEPENDENCY_CONTINUATION`
  when `dependencies` is empty, so a `missing-extractor-dependency` gap with `D = ∅` hits clause 3
  with neither branch true and falls to clause 12 — `unclassified`.

*Smallest safe correction:* add three clauses before clause 12 —
`encrypted-chunk ∈ G → (encrypted-region, treat-unexamined)`,
`unknown-chunk-handler ∈ G → (unknown-handler, inspect-region-or-narrow-range)`,
`missing-extractor-dependency ∈ G, D = ∅ → (dep-missing-unnamed, install-nothing)`. Then bind
`gap_kinds_covered ⊇ {the six kinds in GAP_CONTINUATIONS}` as a predicate clause, so table v4
cannot again leave half the producer's vocabulary unlabelled.

## 5. `max_depth` is a decision boundary the precedence never reads (the strongest defect)

Identical bytes, three run depths, three different labels — measured on **one flat, clean,
symlink-free, single-file squashfs** (`flat.py`, carrier sha256
`6e61f96f2d97d380b4a394dab68949347699ac49700de0814fd444ee32f4c208`):

| `--max-depth` | gaps | P | `depth_limited_paths` | draft label |
|---|---|---|---|---|
| 1 | `{depth-limited}` | 1 | `["$output/firmware.bin_extract"]` | `depth-limited-nested` |
| 2 | ∅ | 1 | `[]` | `clean` |
| 3 | ∅ | 1 | `[]` | `clean` |

The nested image behaves the same way (depth 1 → `depth-limited` on the extract root; depth 2 →
`depth-limited` on `…/inner.sqsh_extract`; depth 3 → ∅, P 3). Consequences, all measured:

1. **`depth-limited` at `--max-depth 1` is not a nested-image signal.** It attaches to the
   *extraction root* of any successful image. So at C1's own settings, v3's clause 7 labels every
   clean extraction `depth-limited-nested` → action must be "raise depth" for an image with nothing
   nested in it. A false positive on the table's most common case.
2. **`clean` and `clean-empty` are unreachable at `--max-depth 1`.** The label function is a
   function of `max_depth`, a field the precedence does not take as input (`:73-74` lists OP PR H G
   D BE SR P; `parameters.max_depth` is in every envelope — I read `max_depth: 1` on all four C1
   receipts, `3` on round-40 C2's H21).
3. **`depth-limited-nested` is a misnomer for the real carriers**: their `depth_limited_paths` is
   `["$output/firmware.bin_extract"]` — the root, not a nested child. And on those same envelopes
   it **shadows clause 10**, discarding 263/85/2/2 retained entries: the label the reader gets is
   "raise depth", while the actionable fact is "hundreds of entries exist as metadata only". That is
   R40-CL5's absorption defect (escaping row absorbing combined sets) reintroduced in the opposite
   direction, one round after it was filed.
4. **REA itself distinguishes the two cases**, and says so in the continuation text
   (`FirmwarePublication.js:23-24`): `maxDepth < MAX_EXTRACTION_DEPTH` → "rerun with a higher
   max_depth (up to 10)"; at the ceiling → "rerun with `path` set to a published child below this
   path … each child restarts the depth budget", and with no eligible child → "the depth budget
   cannot be restarted; treat the region as unexamined." Three instructions, one label.

*Smallest safe correction:* add two features — `max_depth` (integer, read only from
`parameters.max_depth`) and `ceiling_path_is_root` (is every `depth_limited_paths` entry the
extract root?) — and split the row:

```
7a. `depth-limited` ∈ G, max_depth < 10, path is a nested child → (depth-limited-nested, raise-depth)
7b. `depth-limited` ∈ G, path is the extract root, P > 0  → (depth-limited-at-root, extraction-complete;
                                                              nested descent stopped at the budget)
7c. `depth-limited` ∈ G, max_depth = 10                   → (depth-limited-ceiling, reroot-or-unexamined)
```

and place both *after* the symlink clauses (or give the combined pair its own action, §2) so the
real carriers' retained-entry count is not swallowed. This single change is the largest depth gain
available to the round: it adds a real numeric threshold, which is what `AXES.md:11` asks for, and
it is grounded in the producer's own branch.

**Careful:** adding `max_depth` opens the id-leak channel the round-40 shortcut audit named — every
envelope's `parameters.path`, `subject.local_path` and `raw_result` paths carry the carrier id
(`…/H21/carrier.sqsh`), and the manifest maps id → class. Bind a **whitelist**: the evaluator's and
interpreter's feature extractors read only `operation`, `provider.id`, chunk `handler`,
`extraction_gaps[]` (`kind`, `dependencies`), `diagnostics[].report.{kind,command}`,
`files` length, `depth_limited_paths`, and `parameters.max_depth` as an integer; a red selftest must
show a path-valued column being refused (`path_feature_refused`).

## 6. Missing controls and bindings (each with the red fixture that must exist)

`c2-counter.py` at round 40 carried 25 bindings (receipt
`.ufo/waves/round-40/l1/scores/c2-at-42c10a58.json`). The v3 port needs five more and one demotion;
the draft names none of them.

| id | binding (name) | what it asserts | red fixture the lane must commit before data |
|---|---|---|---|
| B1 | `expected_source_is_evaluator_output` | the expected pairs are read from `heldout/labels-v3.json`, whose sha256 equals `sha256(frozen evaluator(envelopes))` recomputed at score time; the manifest's `label_actions` is **not** read for scoring | labels file with one flipped pair → exit 1, `expected_source_is_evaluator_output` false. Today's counter reads `expected_label`/`expected_action` off the manifest carriers (`c2-counter.py:548-557`, fed by `heldout-gen-v2.py:908-909`) — a v3 port that keeps those lines scores against the class map and the whole independence sentence is void. |
| B2 | `evaluator_predates_table` | the evaluator's first commit is an ancestor of the table's first commit, and no later commit touches it (same shape as `manifest_before_envelopes`) | a sandbox clone where the evaluator is added after the table → exit 1 |
| B3 | `interpreter_sha_matches_freeze` | the v3 interpreter bytes equal the freeze bytes (round-40 bound only *presence*: `interpreter_present_at_freeze`) | one-cell interpreter change → exit 1 |
| B4 | `observed_features_match_declared` | per class, the envelope's feature set equals the recipe's declared set (§3b) | the six `partial+mixed` envelopes above → exit 1 naming `class_construction_mismatch` |
| B5 | `declared_max_depth` | the held-out set declares its `--max-depth` and every envelope's `parameters.max_depth` equals it | one envelope at depth 2 in a depth-1 set → exit 1 |
| B6 | `gap_kinds_covered` | the label set covers all six `GAP_CONTINUATIONS` kinds | an envelope with `encrypted-chunk` reaching clause 12 → exit 1 |

Plus three **controls** the kill rule needs (`:99-101` omits them):

* `CTL-C2-7` — **v3 minus the depth row**: must score below target on dev **and** in the held-out
  set, otherwise the new row carries nothing.
* `CTL-C2-8` — **v3 on the four committed round-40 C1 receipts**: `labels == depth-limited-*` for
  all four, `unclassified` for none. This is the free, real-byte control available today: the frozen
  v2 table labels all four `unclassified  none` (measured, exit 0, command in §7), so v3 gains real
  traction only if it stops doing that. No generator, no new bytes, and it makes the marker row
  answerable with the lane's only genuine firmware.
* `CTL-C2-9` — **precedence transcription**, declared explicitly as *the intended table, exempt from
  the kill rule* (round-40's F3 flagged the undeclared version of this exemption: the dev run had
  answered all 13 classes in the freeze commit, and `ADOPTED` was exempted from a kill rule that
  targeted exactly that count). Because the adopted table *is* the transcription, a kill rule that
  fires on "a control at target" has no admissible reading unless this is stated.

## 7. Evidence (commands, outputs, exit codes)

```
# real-carrier features (digest-bound)
$ python3 -I -B real-carrier-features.py --root <lane>            # exit 0
V1 … gap_kinds depth-limited,unpublished-entry  gap_count 264  SR False  P 697  unpub 263  max_depth 1
V2 … gap_kinds depth-limited,unpublished-entry  gap_count  86  SR False  P   8  unpub  85  max_depth 1
L1 … gap_kinds depth-limited,unpublished-entry  gap_count   3  SR False  P   7  unpub   2  max_depth 1
L2 … gap_kinds depth-limited,unpublished-entry  gap_count   3  SR False  P   6  unpub   2  max_depth 1

# frozen v2 table on the same four receipts
$ python3 -I -B tools/round-40/sqfs-triage-v2.py --skill SKILL.md <V1 V2 L1 L2 after.json>
V1 … unclassified  none      V2 … unclassified  none
L1 … unclassified  none      L2 … unclassified  none                     # exit 0

# draft precedence on the same four + four probe envelopes → 2 distinct pairs, 1 actionless
$ python3 -I -B precedence-probe.py …                                    # exit 0

# combined-gap probe (4 carriers + one refused call)
$ python3 -I -B comboprobe.py "$PWD/probe" 41c2d0ff1cebabe1               # exit 0
H01..H04: ok true, G={extractor-failure, unpublished-entry}, SR false, P 5/6/7/3
refused: exit 1, ok false, error.code=unreadable_output,
         error.details.reason="Staging entry budget exceeded (1)", no `data` envelope

# nested depth + 4 partial+mixed seeds
$ python3 -I -B nested.py "$PWD/probe2"                                  # exit 0
depth 1: G={depth-limited} dl=["$output/firmware.bin_extract"] P 2
depth 2: G={depth-limited} dl=["…/inner.sqsh_extract"]          P 3
depth 3: G={}                                                   P 3
4 seeds "both link kinds + partial": G={extractor-failure, unpublished-entry}, SR false (4/4)

# flat image, three depths
$ python3 -I -B flat.py                                                  # exit 0
depth 1: G={depth-limited} P 1   depth 2: G={} P 1   depth 3: G={} P 1
```

Also relevant, no run needed: the refused call returns **no `data` object at all**, so a refused
`extract_firmware` has no envelope and no features. The draft's predicate quantifies over "every
held-out envelope", which silently excludes every REA refusal; the v3 block should say so in one
sentence (`ok=false` ⇒ no label; read `error.code`), and `no-squashfs-chunk` should be gated on a
*completed* analysis (`ok=true`, empty handler set) so the two are not conflated.

## 8. Predicate changes, as a block the L1 can adopt

Replace `:90-97` with:

> **P41-C2.** At the measured revision, for every envelope of the frozen held-out set (declared
> `max_depth`, ≥2 replicates/class), the frozen v3 interpreter — pinned by `interpreter_sha_matches_freeze`
> — reading only the SKILL v3 table (bytes equal to the freeze), gives the **pair** that the frozen
> evaluator gives it, where the expected pairs are read from `heldout/labels-v3.json` (sha256 =
> the evaluator's recomputed output, `expected_source_is_evaluator_output`) and the evaluator
> (`evaluator_predates_table`, never reads the table, the interpreter or the class map) was written
> from the precedence text of this claim, which now states an action for every clause; the
> generator's class map is committed and compared, **reported** as `class_map_agreement`, and any
> disagreement blocks the freeze (envelope rebuilt) rather than failing the claim at score time;
> `observed_features_match_declared` holds for every class; `gap_kinds_covered ⊇` the six kinds in
> REA's `GAP_CONTINUATIONS`; `distinct_decisions ≥` (number of distinct expected pairs) and the
> claim states that count; carriers regenerate byte-identically; the four committed round-40 C1
> receipts, labelled by the same interpreter, all receive a `depth-limited-*` pair and none
> `unclassified`; the refusal case (`ok=false`, no envelope) is reported as out-of-table.

and add to the claim body, next to the score: the partition
`36 envelopes = 13 pairs, of which 12 were decided by v2 and 1 is new`, and
`the only pair this round exercises against real firmware bytes is the new one — the four committed
C1 carriers (4/4 `depth-limited-*`); the other twelve pairs are only ever measured on generator
output`.

## 9. Not attacked / limits

* I did not verify the v3 table's *content* — there is none yet; the draft is the precedence text.
* I did not attempt to produce `encrypted-chunk` or `unnamed-dependency` envelopes; those holes are
  argued from producer source (`FirmwarePublication.js:165-204`, `:286-287`) and marked as such.
* `depth-limited+mixed` reachability is unproven, not disproven: my constructions never produced
  `MaliciousSymlinkRemoved` alongside any gap, and the committed real carriers have `SR=false`.
* Actionability of `raise-depth` for `depth-limited-at-root` is `[INFERENCE]` — I did not re-run a
  real AVM carrier at `--max-depth 2` (reserved images), and the C1 receipts' bytes are vendor
  members I did not re-extract.
* No claim about round-40's independent evaluator's quality: I did not open it (seat restriction);
  my independence argument is structural and holds whatever that file contains.
