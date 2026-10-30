# MutControlsV2 — round-51 control designs: dead-control attack

Seat: MutControlsV2 (mutation tester, leaf member). Wave: r51 w1 (build).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base rev `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.
Scope: attack the **control designs** named in `plans/round-51-claims.md` (R51-C1 controls, R51-C2
controls) for dead controls. Nothing in the lane tree was modified; all measurement ran in
`/fast/scratch/hyaku/kaidoku-r51/w1-MutControlsV2` on a `git clone --shared` fixture at the base
rev with the round-51 carriers table + law rule committed on top.

**No REA run, no data run, no network, no vendor bytes.** Every number below is measured.

## What the controls actually score (the mechanism, first)

The R51-C1 controls are scored by `tools/round-51/c1-counter.py --controls` (F2 in the counter
docstring). That mode evaluates **only** the disposition verdict (`gaps_ok` AND
`nonregular_unpublished_ok`) of one named gap rule over the committed envelopes
`<receipts>/<id>/after.json`, using the oracle/non-regular tables the carriers table names.
It exits `0` iff `matched == len(per)` — i.e. **iff every carrier it happened to score is
clean**. It does **not** evaluate the carrier/provenance/freshness/projection/binding clauses, and
it has **no** target check, **no** expected-id check, and **no** `carriers_scored == 4` check
(verified by grep over the function body, lines 2692-2788).

Measured arms (`probe/measurements.tsv`, exit + `carriers_scored` + `dispositions_matched`):

| arm | rule | exit | scored | matched | stdout sha256 |
|---|---|---|---|---|---|
| CTL-OLD | `tools/round-50/gap-rule.json` | 1 | 4 | **2** | `4546ebc4b937…` |
| CTL-NEW (law) | law rule | 0 | 4 | **4** | `78001ef8bad7…` |
| MUT require-char-device + 247:0 only | | 1 | 4 | 2 | `4546ebc4b937…` |
| MUT all-13 whitelist (on law base) | | **0** | 4 | **4** | `78001ef8bad7…` |
| MUT strict subset of 13 (on law base) | | **0** | 4 | **4** | `78001ef8bad7…` |
| MUT `allowed[char-device]=[unpublished-entry]` | | **0** | 4 | **4** | `78001ef8bad7…` |
| MUT required=true + strict subset of 13 | | 1 | 4 | 2 | `4546ebc4b937…` |
| MUT required=true + all-13 whitelist | | **0** | 4 | **4** | `78001ef8bad7…` |
| CTL-JUNK (every kind required, impossible allowance) | | 1 | 4 | 0 | `426c1c4afa1a…` |
| CTL-DN (absent receipts dir) | | 1 | 4 | 0 | `426c1c4afa1a…` |

The three identical stdout hashes are the point: **three different rule files produce byte-identical
output.**

## The dead-control table

Legend — **skips**: the claimed work the control does not exercise. **observes**: the exact
observable. **passes-while-false**: how the control can be green while the claim is false.

### R51-C1

| control | skips | observes | passes-while-false |
|---|---|---|---|
| **CTL-OLD** (old rule → 2, exit 1) | the law derivation itself; the new rule; the device census; whether the *new* rule is used at all | `dispositions_matched` of the **r50** rule = 2 (g7581, g7582 red on `dev/pts/*`) | **No.** It is red for a *known, already-committed* reason (the r50 rule misses the 12 FRITZ!Box details). It proves the counter still reproduces the r50 miss; it says nothing about the law. Redundancy: it is a re-measurement of `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (carriers_matched 2). Keep it, but it is **not** independent evidence for C1. |
| **CTL-NEW** (new law rule → 4, exit 0) | **the entire point of the round**: that the rule is the *law* rather than a detail whitelist | the **disposition verdict only** of one rule over the four r50 envelopes | **YES — this is the primary dead control.** Measured: the all-13 whitelist, a strict subset of 13, and `allowed[char-device]=[unpublished-entry]` all score **4/4, exit 0** — byte-identical stdout to the law rule (`78001ef8bad7…`). The disposition verdict is *extensionally identical* over these four carriers for the law rule and for the forbidden whitelist, because under `required[char-device]=false` no device row is ever consulted. So CTL-NEW is green for a rule the claim explicitly forbids ("the law, not a detail whitelist"). Only the **`law_shape_ok` binding** (counter lines 2596-2617) separates them — and `--controls` **does not evaluate bindings**. |
| **CTL-DN** (do-nothing tree → exit 1 or 2) | everything; it is a liveness probe | exit code of the mode over a receipts dir with no envelopes | **Partly.** Accepts exit 1 *or* 2 and asserts no count, so a **crashing** counter passes it: an uncaught exception in the counter exits **1** (measured), indistinguishable from a deliberate "not met". Weakly dead. Tighten to: exit ≠ 0 **and** the receipt exists **and** names the reason. |
| **CTL-JUNK** (junk rule → 0 of 4, exit 1) | the law; the device census | `dispositions_matched` = 0 because the junk rule forbids the `unpublished-entry` gap kind on every row | **No** — it is red for the right reason (the rule is absurd). But it is **redundant with CTL-OLD** in the sense that both are "some other rule is red"; its unique value is that the junk rule is *not* a whitelist shape. Keep, but it does not witness the law. |
| **MUT require-char-device + 247:0 only** | — | red (2/4) | **No.** Correctly red: `required[char-device]=true` re-requires a disposition on 12 details with no allowance. This is the one mutation that genuinely discriminates. |
| **MUT strict subset of the thirteen** (the M50 partial-widening trap, `MutC1Counter` F10) | — | **green (4/4)** — measured | **YES.** As the claim writes it ("whitelisting a strict subset of the thirteen stays red"), this mutation is **not red**. It is red only in the *other* base — `required=true` + subset (measured 2/4, red). On the **law base** (`required=false`), the whitelist is never consulted, so any subset is a **no-op**: the counter's `required.get(kind, ...)` lookup makes a non-required kind skip the disposition check entirely. The mutation is therefore either a **no-op** (green) or a **different mutation** (red). The claim's wording and the sibling's draft (`ExecControls/c1-controls.py`, `strict-subset-NN` built on the `new` base) are the green case. **Either the base must be `required=true` or the expectation must change to "the whitelist is irrelevant under the law" — but then it witnesses nothing.** |
| **MUT all-thirteen whitelist** (the forbidden alternative) | — | **green (4/4)** — measured | **YES.** The claim says the law "is not a detail whitelist", yet the whitelist scores exactly as the law does over the four carriers. **The only witness that separates them is `law_shape_ok`, which `--controls` never evaluates.** This is the single most important gap in the C1 control set: the rule-shape claim is unwitnessed by the control mode the controls use. |
| *(missing)* **rule-shape control** | — | — | **MISSING.** A control that runs the *new* rule through the **binding** path (`law_shape_ok`: `allowed` for the four device kinds empty, `removed.silent` naming no device detail, `required[char-device] is false`) and must be **false** for the all-13 whitelist, a strict subset, and `allowed[char-device]=[unpublished-entry]`. Measured: all three are green under `--controls`; all three must be red under `law_shape_ok`. Without this control the round can freeze a 13-detail whitelist and every named control will still pass. |
| *(missing)* **wrong-carrier-set control** | — | — | **MISSING.** `--controls` exits 0 iff every carrier it *scored* is clean, and it never checks `carriers_scored == 4` or the expected id set. Measured: a carriers table listing **only c6430+c6490** (the two Cable-class carriers, both clean under **both** rules) gives `carriers_scored 2, dispositions_matched 2, exit 0` — **green**. So a counter (or table) that scores only the two easy carriers passes CTL-NEW while the two FRITZ!Box carriers — the ones the whole round is about — are never examined. **A control must assert `carriers_scored == 4` and the four ids.** |
| *(missing)* **counter-identity control** | — | — | **MISSING.** `--controls` prints `dispositions_matched`, not `carriers_matched`. The sibling draft reads `doc.get('carriers_matched')` → **always `None`**. So the count assertion is structurally dead in the draft: `observed_count` returns `None`, `count_ok` is `None == 2` → `False` for CTL-OLD/CTL-NEW/CTL-JUNK, so those three report `misbehaved` **for a field-name reason, not a semantic one**, while every mutation arm with `expected_count=None` reports `expected` **no matter what it observed**. Measured: with the draft's own command line (no `--rev`), the counter prints `usage: --controls requires --root --rev` and exits **2** — and the draft scores **CTL-OLD, CTL-NEW, CTL-JUNK as `misbehaved`** and **all 12 subset mutants as `expected`** on that single usage error. **The whole battery scored green on a usage error.** |
| *(missing)* **crash-vs-red control** | — | — | **MISSING.** Exit **1** is overloaded: "not met" and "the instrument crashed" are the same code (measured: an uncaught exception exits 1). Every control arm that accepts exit 1 as "red" therefore also accepts a broken instrument. Distinguish by requiring a receipt file that parses and names a reason. |

### R51-C2

| control | skips | observes | passes-while-false |
|---|---|---|---|
| **do-nothing** (v5 table at base → audit red) | the v6 route change itself | the executability audit's violation count on the v5 table | **No** — red is the correct before-state (MutTriV6 measured D2=1 naming `dmg_Z3_v3ddwrt_inode_table`). But note the **before-arm is blocked**: the v5 instrument refuses a non-ancestor freeze (measured exit 2, "freeze is not an ancestor of"), so the base arm must run `--freeze` = the base rev or an ancestor of it. The claim's before-arm must name the freeze it uses. |
| **junk table** (syntactically valid, wrong labels → `pair_mismatches > 0`) | the audit; the census | the evaluator-vs-table label comparison | **No.** Red for the right reason. **Redundant with the v5 battery**: v5 already commits an identical junk table and measures 126 mismatches (MutTriV6 confirms 126 → 126 unchanged). |
| **audit-guard-deleted mutant** → red | — | whether removing the guard changes the audit's verdict | **YES, as specified.** MutTriV6 measured: deleting the new row flips the **pair** detector (1) but leaves the **audit** at **0** (the body falls to `preserve-failure`, which prescribes no cross-read). A coordinated table+evaluator mutation is invisible to both detectors. The control must therefore assert *which* detector fires, and the instrument must fail closed when the detector is absent (receipt key required + verdict refused without the detector + a clone-and-delete selftest case). As written, "audit-guard-deleted → red" is satisfiable by the pair detector alone, i.e. by the wrong witness. |
| **row-swapped** (new row's action swapped) | — | pair mismatch count | **Partly.** MutTriV6 measured the swap flips the pair detector (51 → 52). But the claim's kill rule says "any mutation green → stop"; a swap that is caught by the pair detector but leaves the audit at 0 is only half-witnessed. The **precedence** is load-bearing: with the new row **above** `legacy-body-failure`, the "glob broadened back" mutant is **GREEN (0/0)** — nothing observes it, so the guard around it is dead (MutTriV6 F2). The control must pin the row's position, not just the swap. |
| **census-guard-deleted** → red | — | `census_outside` | **YES, as specified.** MutTriV6: deleting the census check reports "0 outside" and goes **green** unless the instrument fails closed. The census re-derive is a *new* trust boundary (it re-derives from the registry markers, a different surface from the frozen census bytes); deleting the guard must be **refused**, not merely scored 0. Also: `census3.json` must be derived from the **staged** freeze `SKILL.md`, or the freeze scores D3 = the number of new registry rows (MutTriV6 landmine). |
| *(missing)* **detector-fail-closed control** | — | — | **MISSING.** Nothing in the named set asserts that the instrument **refuses** when a detector is deleted. Both guard-deleted arms are green-by-omission as specified. Add: delete the audit → the instrument must exit 2 (refused), not 0 with "0 violations". |
| *(missing)* **v6-label-preservation control** | — | — | **MISSING.** The claim requires "v6 must keep every v5 label unchanged except the one ddwrt FAILED-body pair". No named control asserts that. MutTriV6 measured the do-nothing count moving **19 → 20** and action-swapped **51 → 52** — so the frozen expectations must be **20 and 52**, not the v5 numbers. Without a control that pins "exactly one pair changed", a v6 table that re-routes other families passes every named control. |
| *(missing)* **reader-census-binding control** | — | — | **MISSING.** The audit's reader census is a new trust boundary: flipping it disables the executability detector silently (MutTriV6 F3). It needs its own binding to the round-49 `v3-readers` receipt, and a control that a flipped census is red. |

## Amendment check (the claims file was amended concurrently, wave-1 F1–F11)

The claims file gained a `## Wave-1 amendment record` while this seat was working (F1 carrier set,
F2 rule-scoped controls, F3 rule shape, F4 mutation set M1–M4, F9 CTL-OLD relabelled). I re-ran
every arm against the **current** counter bytes (sha256 `48a6c9a58c13…`, then `565fafd2ee23…`)
and re-read the amended control text. **F3/F4 address the shape gap in principle but the
instrument does not yet implement what the text needs:**

- **F3 says** `allowed[device kinds] = []`, `required['char-device'] = false`, `removed.silent`
  naming no device detail. **Measured**: the counter's `law_shape_ok` does enforce exactly that
  (lines ~2596-2617) — but it is a **binding**, and `--controls` **never evaluates bindings**
  (`law_shape_ok`/`shape_notes`/`DEVICE_KINDS` are all absent from `controls_mode`, verified).
  So **M1 ("the all-thirteen whitelist must be RED") cannot be scored through `--controls` at
  all** — the mode has no shape clause to make it red.
- **F4/M2 is the right instrument** (a fourteenth, unlisted device separates the law from any
  detail whitelist). **Measured** with the census carrying `dev/ttyS0 4:64`: the law rule is
  **green 4/4** and every `required=true` whitelist is **red 0/4** — the arm works, **but only
  for whitelists that also set `required=true`**. A whitelist with `required=false` (which is
  what the sibling draft's `new` base and its 12 subset mutants use) stays **green 4/4 even
  with the 14th device**, because `required=false` makes the disposition check skip device rows
  entirely. So M2 as specified does **not** discriminate the draft's own mutants.
- **The sibling's `new` base rule fails the law-shape clause it exists to witness.** The draft
  sets `required['char-device']=False` **and** `removed.silent['char-device'] = list(DETAILS_13)`
  — measured `law_shape_ok=False` ("names 13 detail(s)"). Under F3 that is the **forbidden**
  detail-whitelist shape; under the disposition verdict it is inert. It is green under both
  verdicts and wrong under one.
- **A fourth, independent way the sibling draft is dead:** it writes its rules to `--out`
  (outside the lane) and passes **absolute paths**, but the counter resolves `--gap-rule` through
  `git show <rev>:<path>` — measured: an out-of-repo path is **exit 2 "rule absent"**, the same
  rule committed inside the repo is **exit 0**. Every arm of that draft is exit 2 on the rule
  lookup alone.
- The amended text also introduces `--provenance-base` and `--receipt-fresh-base` flags — **not
  yet present** in the counter (`--gap-rule`, `--receipts`, `--controls` are).

**Net: the amended claim text closes the *design* gap I found (F3's shape clause, F4's M2
14th-device arm), but the instrument and the control driver do not yet implement it, and the M2
arm as written does not discriminate the `required=false` whitelist shapes the draft actually
uses.** The recommendations below stand, with M2 promoted to mandatory.

## Redundant controls (named)

- **CTL-JUNK (C1) vs the junk-table control (C2) vs v5's committed junk table** — three arms
  measuring the same shape ("a syntactically valid but absurd rule is red"). C2's is fully
  carried over from v5 (126 → 126, MutTriV6). Not harmful, but not independent evidence.
- **CTL-OLD (C1) vs the committed r50 after-receipt** — CTL-OLD re-measures a number already
  committed at `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json` (`carriers_matched 2`).
  Its only new value is as a **port regression check** on the v2 counter; it should be labelled
  as such so it is not counted as independent support for the law.
- **MUT require-char-device + 247:0 (C1) vs CTL-OLD** — the r50 rule *is* "required +
  247:0 only" on the device kinds; measured stdout hashes are **identical**
  (`4546ebc4b937…` for both). The same red is measured twice.

## The most important findings

1. **The C1 rule-shape claim is unwitnessed.** The claim insists the rule is the law "not a
   detail whitelist", but `--controls` scores only the disposition verdict, under which the law
   rule and the all-thirteen whitelist are **extensionally identical** over the four carriers
   (both 4/4, exit 0, byte-identical stdout `78001ef8bad7…`). The all-13 whitelist, a strict
   subset, and `allowed[char-device]=[unpublished-entry]` are all **green**. Only `law_shape_ok`
   separates them, and `--controls` never evaluates bindings. **A rule-shape control is
   mandatory before the freeze.**
2. **The claim's own strict-subset mutation is green, not red.** "Whitelisting a strict subset of
   the thirteen stays red" holds only on a `required=true` base (measured 2/4, red). On the law
   base it is a **no-op** (4/4, green). The claim and the sibling draft
   (`ExecControls/c1-controls.py`) both use the law base — so the M50 partial-widening trap the
   claim names is not actually being tested.
3. **No wrong-carrier-set control, and the mode has no target check.** A carriers table with
   only the two Cable-class carriers gives `carriers_scored 2, dispositions_matched 2, exit 0` —
   green — so the two FRITZ!Box carriers that motivate the round can be absent and CTL-NEW still
   passes. The mode must assert `carriers_scored == 4` and the expected id set.
4. **The sibling's control draft scores a usage error as a full green battery.** It omits
   `--rev` (the mode requires it), reads a field the mode never emits (`carriers_matched`; the
   mode emits `dispositions_matched`), and accepts exit 1 *or* 2 for every mutation arm. Measured:
   with its own command line, all three named controls report `misbehaved` and **all twelve subset
   mutants report `expected`** — all on `usage: --controls requires --root --rev`. A battery that
   scores green on a usage error is the definition of a dead control.
5. **Exit 1 is overloaded** ("not met" and "the instrument crashed" are the same code). Every arm
   that accepts exit 1 as red also accepts a broken instrument. Controls must require a parsing
   receipt that names the reason.

## What the L1 should change before the freeze

1. **Make `--controls` evaluate `law_shape_ok`** (or add a separate shape arm). Without it, the
   amended F4/M1 arm ("the all-thirteen whitelist must be RED") is **unscoreable** — measured:
   the shape clause exists in the counter but only on the binding path.
2. **Make M2 (the fourteenth-device arm) mandatory and fix its base.** Measured: M2 separates the
   law (green 4/4) from every **`required=true`** whitelist (red 0/4) — but a `required=false`
   whitelist (the sibling draft's actual base and all 12 of its subset mutants) stays **green**
   even with the 14th device. M2 must therefore also cover the `required=false` whitelist shapes,
   which only `law_shape_ok` can red. Both arms are needed.
3. **Fix the sibling's `new` base rule**: it currently sets
   `removed.silent['char-device'] = list(DETAILS_13)` — measured `law_shape_ok=False`, i.e. the
   rule the claim forbids. The frozen rule must have **no** device details under `removed.silent`.
4. **Fix the sibling's interface (four independent breaks, all measured):** pass `--rev`; read
   `dispositions_matched`/`carriers_scored` (not `carriers_matched`); write the rule fixtures
   **inside** the repo so `--gap-rule` resolves through git at `--rev`; and require a parsing
   receipt with a named reason rather than accepting "exit 1 or 2".
5. Add the **wrong-carrier-set control** and assert `carriers_scored == 4` + the expected ids
   (measured: a 2-carrier table is green).
6. Fix the **strict-subset mutation's base**: it is red only with `required=true` (measured
   2/4); on the law base it is a no-op (green).
7. For C2: freeze the **new** expectations (**20** do-nothing, **52** action-swapped per
   MutTriV6), pin the new row's **precedence position**, add the **detector-fail-closed** control
   (guard deleted → exit 2, refused) and the **v6-label-preservation** control (exactly one pair
   changed), and bind the **reader census** to the round-49 `v3-readers` receipt.
8. Name the **before-arm's freeze** for C2: the v5 instrument refuses a non-ancestor freeze
   (measured exit 2), so the base arm needs `--freeze` = the base rev.
9. The amended text names `--provenance-base` / `--receipt-fresh-base` flags — implement them or
   amend the text; they are absent from the counter today.

## Evidence

- `probe/measurements.tsv` — every arm: exit, `carriers_scored`, `dispositions_matched`,
  stdout sha256.
- `probe/receipt.txt` — the exact command line, exit code, `carriers_scored`,
  `dispositions_matched`, stdout sha256 and stderr for every arm, run 2026-10-30T05:24:47Z
  against the counter at sha256 `028dde4ae38b1c6f64d3ee93a1ca724c4ec16161b5f66ef5d3ba45f29edc4117`
  on fixture rev `97b429f6ad681c5242a09e30530ed045231247bd`. (The counter file is being
  edited by the sibling seat during this wave — the numbers reproduce across two independent
  runs at two different counter hashes, but **re-run the receipt at the freeze**.)
- `probe/receipt-m2.txt` — the amendment-check measurements: the M2 fourteenth-device arm, the
  `law_shape_ok` evaluation of the sibling draft's own rules, and the `--gap-rule` path-resolution
  probe. Run 2026-10-30T05:26:22Z against the counter at sha256 `565fafd2ee23…`.
- `probe/probe2.py` / `probe3.py` / `probe4.py` / `probe6.py` — the offline probes:
  candidate-rule scoring against the committed r50 `after.json` envelopes, the whitelist
  equivalence, and the carrier-set vacuity.
- `probe/fixture-carriers-4.json`, `probe/fixture-gap-rule-law.json`, `probe/rule-*.json` — the
  exact rule fixtures scored.
- Commands and receipts: `probe/` in this seat directory; scratch
  `/fast/scratch/hyaku/kaidoku-r51/w1-MutControlsV2` (removed after copying).
- Tools installed: none.
