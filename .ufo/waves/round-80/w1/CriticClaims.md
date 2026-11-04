# CriticClaims — round 80 adversarial falsification

**Role.** Find the claim false or the counter blind. Attack the frozen sentences
(`plans/round-80-claims.md`, guard `84d68e90`), not the seats' intentions.

**State read.** The lane landed two commits while this seat was reading:
`253fc817` (the three instruments + base arms) and `b8260107` (gate cases 37).
Every measurement below is at `b8260107` for the target arms and at `16dfa009`
for the base arms, with the lane tree otherwise untouched. The three claims'
**landing receipts** (`c1-at-landing`, `c2-at-landing`, `c3-at-landing`) were not
all present when this seat measured: `c1-at-landing.json` exists; C2's target
receipt does not (the repair is unlanded); C3's target receipt does not. Numbers
below are this seat's own re-runs, not the L1's.

**Method.** Re-derived every count from committed bytes with an independent
script (`git show <rev>:<path>` + sha256 of the blob), re-ran each frozen
predicate command byte-for-byte, and mutated the gate's nine clauses to measure
the survivor set. Evidence receipts are in `w1/CriticClaims/`.

---

## 1. Verdict per claim (measured, not read from the L1's receipts)

| claim | frozen target | measured at `b8260107` | base arm at `16dfa009` | verdict |
|---|---|---|---|---|
| R80-C1 | cases 4, green 2, cand_false_greens 0, control 4, cand_green_refusals 0, control 0; live 5/5 | **all six hold**, `ok true`, `--validate` defects `[]`, exit 0 | candidate = round-79 impl: `candidate_false_greens 4`, `candidate_red` = all four red ids, exit 1 | **predicate verified as written** (with the caveats in §6) |
| R80-C2 | receipts 34, flagged 1, expected_control_flags 1, unexpected 0 | **flagged 2, unexpected 1** (`c2-at-landing.json`) — the repair is not landed; target arm unmet | 34 / 2 / 1 / 1, `--validate` defect-free, exit 1 | **target not yet met**; and the rule cannot report the defect class it cites (§5) |
| R80-C3 | guards 9, rows 9, bound 9, survivors 0, pristine.cases 37, failures 0, target_pin.matched true | guards 9, rows 9, bound 9, survivors 0, pristine 37/0, `--validate` `[]`, exit 0; **`target_pin.matched false`** under the frozen command | 9 / 0 / 0 / 9, pristine 29, exit 1 | **predicate FAILS verbatim** on `target_pin.matched`; passes only with a flag the frozen command omits |

C1's live arm was also re-derived at `--rev 16dfa009` and at `b8260107`:
`checks_total 5, matched 5, mismatches 0, unparsed 0, duplicates []`, exit 0.
The live record is exact-token-clean (all five pointed slices delimit their
tokens), so the strict rule does not regress the round-79 reading.

---

## 2. Do-nothing-control reachability (`reachability`)

| claim | vacuous path | blocked by | blocked? |
|---|---|---|---|
| C1 | refuse every token | `candidate_green_refusals 0` (2 green bind cases) + the live 5/5 arm | **yes** — measured: the two greens bind under both impls, and a refuse-all candidate would score 2 |
| C1 | refuse every `kind: record` input (report the duplicate on any record) | **nothing in the battery** — both green cases are `kind: bind`; there is no green record control. The separate live arm's `duplicates []` is the only clean record, and it is a different command whose value can be a default empty list | **no at the battery level**; only the live arm, weakly |
| C1 | report the duplicate id but collapse the count (`duplicates: [id]`, `checks_total 5`) | **nothing** — `duplicate_refused()` at `tools/round-80/strictness-battery.py:87-91` accepts EITHER `cell_id in duplicates` OR (`checks_total > 5` and `not ok`), while the claim's Rule requires "every declared cell is counted **and** the receipt carries the duplicate id" | **no** — the predicate does not test the Rule's conjunction |
| C1 | emit the live 5/5 as a constant | nothing binds the live receipt's checks to the committed `PROVINCE.md`; no re-derivation clause exists (contrast C3's explicit `pristine.cases` re-derivation and C2's committed-blob rule) | **no** — a hardcoded live arm passes |
| C2 | flag nothing | `flagged 1` + `expected_control_flags 1` | **yes** — `flagged 0` is not the target |
| C2 | flag everything | `unexpected 0` | **yes** |
| C2 | declare the failing receipt's `rev` symbolic and rely on the tip | `bound_at()` returns the tip **before** consulting the declared rev: `("@HEAD@", tip_digest)` → bound; `("main", tip_digest)` → bound; `("eee…", tip_digest)` → bound (measured with the tool's own `FakeResolver`) | **no** — the frozen kill rule's symbolic-rev clause is not enforced |
| C2 | rewrite the flagging receipt's digest to the tip blob | the rule admits the tip first (`tools/round-80/receipt-provenance.py:123`), so `flagged 1` is reachable by an edit that is indistinguishable from a genuine re-run | **no** |
| C3 | zero guards / zero rows report `survivors 0` | `guards 9` and `rows 9` are literal predicate constants; at base the same tool reports rows 0 / survivors 9, so no zero-row path reaches 0 | **yes**, but by the predicate constant, not the instrument (the tool exits 0 on `guards>0`) |
| C3 | a case that fails on everything "kills" every mutant | `pristine.failures 0` forbids a case that fails pristine | **yes** |
| C3 | one case binding two clauses | nothing — `bind()` checks clause↔row bijection only; `case` distinctness is never checked. Measured: one case asserting `validate_receipt(...)["defects"][:2]` fails on **both** mutant G03 and mutant G04 | **no** — see §6.5 |

---

## 3. Empty-set and population gaming (`gaming`)

| class | input | caught? |
|---|---|---|
| receipt removed instead of repaired | delete `c2-at-landing.json`, or drop its `instrument` block | **caught** by the kill rule and by `receipts 34` (33 ≠ 34) |
| window narrowed | `--from-round 60 --to-round 78` | **caught**: receipts 33, flagged 1 → `receipts 34` fails |
| **relocation into `/attacks/`** | move `c2-at-landing.json` to `l1/scores/attacks/` (excluded by path) and add one copy of a passing receipt so the count stays 34 | **not named** by the kill rule ("deleted, or its `instrument` block removed"); `receipts 34` is preserved; only a diff read catches it |
| **disclosed population change** | the kill rule permits a `receipts` count other than 34 *with* a disclosed change; the predicate still says 34, so a disclosed swap is admissible by text | **not caught** by the counter |
| **row whose case is declared but not written** | a row naming a case absent from `--selftest` | **caught**: absent case = survivor (measured base arm: 9 survivors) |
| **case that asserts a constant** | a case whose assertion does not read `validate_receipt` | caught only if the mutant still fails it; a case asserting a source literal is not distinguished by the frozen predicate (the round-79 closure already named this class) |
| **table row whose fragment matches two clauses** | e.g. `: refused ` | **caught** by the landed uniqueness check (`bind()`, `hits > 1 → defect`) and by the tool's own selftest |
| **fixture set weakened after the freeze** | edit `.ufo/.../strictness.json` | mostly anchored by `control_false_greens 4`; but nothing pins the fixture file's digest in the predicate, and a drift that keeps the control at 4 is undetectable |
| **C1 population removal** | drop a red fixture | **caught** by the literal `cases 4` |
| **C2 the flagging receipt "repaired" by rewriting its digest** | set `instrument.sha256` = sha256 of the tip blob (`40905d39…`, already carried by two receipts) | **not caught**; the row then reads `bound, matched_rev=<tip>`, the same shape as the rev-forgery control |

---

## 4. Axis labelling (`axis_rulings`)

### 4.1 R80-C1 is not calibration — the labels are swapped with C2

The round contract §9 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/kaidoku-round-80.md:551`):

> "A calibration claim must count mismatches between the lane's self-assessment
> (SCORECARD/SHONEN) and observed repo state. It cannot be an assertion."

and `:564`:

> "Name the axis by the surface the round changes, not by the number it produces
> (kaidoku r29). Re-scoring a rule the lane already holds on new inputs … is
> quality work, never coverage or depth."

Measured facts:

- C1's counter reads `PROVINCE.md` pointer cells against live client configs and
  `.bashrc`. It never reads `SCORECARD.md` or `SHONEN.md`. At base it counts
  **zero** self-assessment mismatches: the live 5/5 is *true* (all five pointed
  slices delimit their tokens — measured). C1 counts *red-fixture discrimination
  the lane never claimed*, not a self-assessment mismatch. **Not calibration by
  §9.**
- The same surface was recorded as **freshness** in round 79:
  `SCORECARD.md:6144` — `| R79-C2 | freshness | capability acquisition (line-bound
  pointer binding) | … |`; `plans/round-79-claims.md:17` — "C2's axis is
  `freshness` (the record's live pointers), which the lane reports every round
  and which is not a second calibration claim"; the round-79 closure's own note
  (`SCORECARD.md:6190-6191`) records CriticClaims' §9 reading that R79-C2 is "a
  strictness increment on the round-78 pointer rule rather than a new surface".
  R80-C1 changes the same instrument's *match rule* — exactly the round-79
  "planned next" item (b), "a duplicate-cell rule and an anchored
  (word-boundary) pin match in `pointer-bind.py`".
- `AXES.md` freshness is "drift detection — skill claims re-verified against
  live surfaces; stale items flagged or fixed". That is C1, verbatim.
- C2 counts: `SCORECARD.md:6144` marks the round-79 row **verified** citing
  `.ufo/waves/round-79/l1/scores/c2-at-landing.json`; observed state says that
  receipt's `instrument.sha256` (`a0044c4c…`) matches no committed blob. That is
  a **SCORECARD-vs-repo mismatch**, i.e. calibration by §9's sentence.

**Ruling.** The two axis names are reversed: C1 is freshness (drift detection on
the record), C2 is calibration (a self-assessment entry that does not match repo
state). Consequence: as written, R80-C1 is a second freshness increment on a
held surface, labelled by the number it produces (`candidate_false_greens`), the
exact §9 defect the clause names. The claim's opening sentence, "Three claims on
three distinct axes" (`plans/round-80-claims.md:5-11`), is false under the
lane's own recorded labels: C1 and C2 are both freshness work and count as one
claim under `AXES.md` ("two claims on one axis in one round count as one
claim"). The lowest-axis obligation survives only because C3 (depth, tied at
10.0) is a genuine depth move and because C2 (mislabelled) would move
calibration.

**Smallest safe correction.** Land the SCORECARD rows with the labels swapped
(C1 → freshness, C2 → calibration) and say so in the round report, or state in
one sentence why the same `pointer-bind.py` surface is freshness in round 79 and
calibration in round 80. Do not land a second freshness move on the pointer
surface under a calibration label.

### 4.2 `freshness` entering as an owned axis

Legitimate in principle (`AXES.md` lets a lane own a subset; the round-79
closure's Q5 note — "`freshness` is a fleet axis, not a lane-owned proxy" — is
recorded but not a prohibition), **provided** the row is recorded as a change
with reason and a derivable score. The claim gives the reason (spot-check item 4)
and a measured baseline — `receipts 34, flagged 2`, which this seat re-derived
exactly — so the baseline is measured, not invented. **Gap:** no 0–10 mapping is
declared. The lane's convention is `round(10 * numerator / denominator, 2)`
(`SCORECARD.md`, "Scores use…"), which yields `32/34 → 9.41` at base and
`33/34 → 9.71` at target. The claim must name that mapping or the row is an
opinion under the SCORECARD contract. Also record that entering at 9.41 makes
freshness the *lowest* owned axis by construction; the baseline is real, but the
choice to own the axis is made in the same round that moves it.

### 4.3 R80-C3: depth or quality work on a held instrument?

`AXES.md` depth is "verifiable technical detail — decision tables with real
thresholds, named error signatures, cited sources". The SKILL block *is* a
decision table with the nine exact triggers, so the surface moved is the table,
not the gate's refusals (the gate refuses exactly the same inputs before and
after; the instrument's capability is unchanged). **Ruling: depth is defensible
for the table; it is not capability acquisition.** The claim types it "Capability
acquisition" — that is the wrong §9 type for an instrument whose behaviour is
unchanged. Call it a depth move (table + isolating cases) and drop the capability
row, or keep the capability row and drop the depth claim. It cannot be both.

---

## 5. Causal separability and file overlap (`file_overlap`)

**Write sets (claim surfaces, not landing bookkeeping):**

- `W(C1)` = { `tools/round-80/strictness-battery.py`, `tools/round-80/pointer-bind.py` }
- `W(C2)` = { `tools/round-80/receipt-provenance.py`, `.ufo/waves/round-79/l1/scores/c2-at-landing.json` }
- `W(C3)` = { `tools/round-80/guard-battery.py`, `tools/round-78/attack-gate.py`, `SKILL.md` }
- `W(landing)` = { `SCORECARD.md` } — all three claims append a capability row in
  the same round, a literal counterexample to "no two claims write the same file"
  (`plans/round-80-claims.md:11`) unless "file" means claim surface only.

**Read sets:**

- `R(C1)` = { `PROVINCE.md`, `tools/round-79/pointer-bind.py`, `.ufo/waves/round-80/l1/fixtures/strictness.json` }
- `R(C2)` = { the 34 `l1/scores/*.json` receipts of rounds 60–79, and the
  committed blobs of their 12 distinct `instrument.path` values —
  `tools/round-68/registry-conformance.py`, `tools/round-68/packed-elf.py`,
  `tools/round-69/packed-elf.py`, `tools/round-70/packed-elf.py`,
  `tools/round-76/record-audit.py`, `tools/round-76/plan-command.py`,
  `tools/round-77/verdict-bind.py`, `tools/round-77/prefile-receipt.py`,
  `tools/round-78/surface-recheck.py`, **`tools/round-78/attack-gate.py`**,
  `tools/round-79/gate-mutation.py`, `tools/round-79/pointer-bind.py` }
- `R(C3)` = { `tools/round-78/attack-gate.py`, `SKILL.md` }

**Intersection.** `R(C2) ∩ W(C3) = { tools/round-78/attack-gate.py }` — C2's
counter hashes a file C3 edits (two of the 34 receipts name it as their
instrument: `round-78/l1/scores/c1-at-record.json`, `c1-at-tip.json`). Verdict:
**no verdict dependency today** — both receipts declare pre-edit commits
(`93753d88`, `51c08cda`) and their digests match at those commits, so C3's edit
does not flip them. The other cross relations are empty. But the claims'
separability sentence only forbids reading another's *receipt*; it does not
forbid reading another claim's *file*, and this pair exists. Disclose it.

**C2's `matched_rev` is the point, not the revision.** 24 of the 32 bound rows
report `matched_rev = b8260107` (the round-80 tip), including round-68/69/70
receipts; only 6 report their declared rev and 2 report a third revision
(`a8908930`). `bound_at()` checks the tip first (`receipt-provenance.py:123`), so
whenever the instrument file still exists at the tip the declared rev is never
consulted. That is *measured* false provenance in the receipt's own field, and
it is the mechanism by which the rev-forgery control stays green.

---

## 6. Kill-rule gaps (`kill_rule_gaps`), with the input that exercises each

**G1 (C3, blocker).** The frozen predicate requires `target_pin.matched true` but
its command omits `--expect-sha256`. The seat spec
(`.ufo/waves/round-80/gen-w1.py:261-262`) defines `matched` **false when the flag
is absent**. Measured at `b8260107`: without the flag `target_pin = {actual
df6fb856…, expected "", matched false}`, exit 0, `ok true`; with
`--expect-sha256 df6fb856…` → `matched true`. The frozen sentence therefore fails
verbatim. *Input:* the predicate command exactly as written.
*Smallest correction:* record the predicate as run **with** `--expect-sha256
<sha256 of the gate blob at the measured rev>` in the landing receipt and the
round record (the claims file is frozen; the omission must be disclosed, not
silently fixed), or redefine `matched` as self-consistency (`actual ==
instrument.sha256`) so the flag is unnecessary. Do not report `target_pin.matched
true` from a receipt produced without the flag — the base receipt already records
`matched false` for exactly that reason.

**G2 (C3, contract identity).** The frozen cell is "message **prefix**"; the SKILL
header says "message **fragment**"; the code tests fragment membership plus
uniqueness and its docstring admits it (`tools/round-80/guard-battery.py:16-21`).
Measured: for G03–G06 the frozen string is **not a prefix** of the source literal
(it begins with `f"{fixture.get('id')}`) nor of the rendered message (which
begins with the fixture id); it is only a substring. The docstring's claim that
the test is "strictly narrower than prefix matching" is false: it rejects
prefix-valid fragments (e.g. `fixture`, unique as a prefix of G02) and accepts
non-prefix fragments (`: fixture dir mismatch`). §9 requires "the same sentence
in the plan, the same condition in the counter's code and the same label in the
receipt" (`.ufo/prompts/kaidoku-round-80.md:562`; §9 opens at `:546`). *Smallest correction:* rename
the cell to "message fragment" in the claim's Rule and state the uniqueness
condition, and replace the docstring's "strictly narrower" sentence with
"membership plus uniqueness; the nine frozen strings are unchanged".

**G3 (C3, duplicate authority).** `gen-w1.py:271,276` instruct ExecGuard to
expect base `survivors 9`; `gen-w1.py:446` instructs ReviewerC3 to "Confirm the
base shape (8 survivors, 1 killed at `: refused without a reason`)". Both are
primed for the same revision. Measured: with the battery's declared-case
semantics, base = 9 survivors (rows 0); with "does any existing case detect the
deletion", base = **8 undetected, 1 detected** — and the detected one is exactly
`red-validate-refused-no-reason` (clause 5, line 794), while the other eight
survive with 29/29 green. ReviewerC3's sentence will read as a deviation from the
frozen claim. *Smallest correction:* reword ReviewerC3 to "8 clauses have no
isolating case and 1 already does (clause 5); the battery's `survivors` is 9
because no row is declared at base".

**G4 (C3, case injectivity).** The bijection is clause↔row only; two rows may
name one case. Measured: one case asserting `defects[:2] == [<id>: fixture dir
mismatch, <id>: base.accepted is not a bool]` fails on mutant G03 **and** mutant
G04. `pristine.cases 37` (= 29 + 8) forces eight new cases, so a shared pair needs
a filler to keep 37, but the predicate cannot see it. *Input:* rows G03 and G04
naming one case, plus a filler case. *Smallest correction:* add
`len({r["case"] for r in rows}) == len(rows)` to `bind()` and one selftest case
for a shared case. (Not present in the landed table: the nine case names are
distinct.)

**G5 (C2, declared rev never constrains).** `bound_at()` checks the tip first, so
a receipt declaring `rev: "@HEAD@"`/`main` whose digest equals the tip is
**bound** (measured with the tool's own `FakeResolver`: all three return the
tip). The frozen kill rule says a symbolic rev "accepted as a committed
revision" is a kill; the tool accepts it. The selftest case
`red-symbolic-rev-not-a-commit` uses a working-tree-only digest, so it is unbound
for the wrong reason and never exercises this path. *Input:* any receipt with
`rev "@HEAD@"` and the tip digest. *Smallest correction:* in `bound_at`, when a
declared rev is present require `HEX40` **and** `git cat-file -e <rev>^{commit}`
before the tip check; if it fails, return "" regardless of tip/history.

**G6 (C2, the rev-forgery control is green).** Measured row:
`prov-forged-rev.json`, `declared_rev eeee…` (not a commit object),
`verdict bound`, `matched_rev b8260107` (the round-80 tip), `expected_control
false`. The round-69 control built to test rev forgery is certified as
provenance-bound. The predicate's `unexpected 0` **requires** this. A rule that
binds the digest to the declared revision reports **6 flagged** (the 2 known + 2
round-76 at-landing + 2 round-79 `c2-*-final`), not 1. *Smallest correction:*
either (a) add `prov-forged-rev.json` to `expected_controls` and re-freeze
`flagged 2 / expected_control_flags 2`, or (b) record the narrowing explicitly
("the sweep binds the digest, not the revision; a receipt naming a non-commit
revision is out of scope") and do not claim the round-79 rev-defect class is
closed. Do not land the sentence "every landing-class receipt's instrument digest
names a committed blob" as if it covered the rev.

**G7 (C2, repair indistinguishable from forgery).** The tip is the first
disjunct; the cheapest repair of `c2-at-landing.json` is to overwrite
`instrument.sha256 a0044c4c…` with the tip digest `40905d39…` (already carried by
`c2-at-base-final.json` and `c2-path-only-final.json`). The resulting row is
`bound, matched_rev=<tip>` — the same shape as `prov-forged-rev`. The kill rule
forbids deletion and `instrument`-block removal, not a blind digest rewrite.
*Smallest correction:* require the repaired receipt to carry a fresh `checked_at`
and a re-run at a named rev with `matched_rev` equal to that rev (not the tip),
and add "a digest copied from the tip without a re-run" to the kill rule.

**G8 (C1, duplicate rule half-tested).** `duplicate_refused()`
(`tools/round-80/strictness-battery.py:87-91`) accepts the id in `duplicates`
**or** `checks_total > 5 and not ok`, while the Rule requires both. *Input:* a
candidate returning `checks_total 6` with `duplicates: []`, or `duplicates:
[<id>]` with `checks_total 5`. Both score `candidate_false_greens 0`. *Smallest
correction:* require `cell_id in duplicates` **and** `checks_total == 6`, and add
a green record control (a clean five-cell record must report `duplicates []`).
The landed candidate implements both halves, so this is a predicate defect, not
an artifact defect.

**G9 (C1, live arm unpinned).** The battery receipt
`.ufo/waves/round-80/l1/scores/c1-at-landing.json` carries no `rev` and its
`candidate`/`control` blocks carry paths but **no sha256**. The receipt therefore
cannot prove which candidate build scored 0; a later edit leaves it valid-looking.
*Smallest correction:* add `rev` and both impl digests to the receipt and
`--validate`. (Compare C2, which records `rev`, `tip`, and per-row
`matched_rev`.)

**G10 (C1, symbolic rev inconsistency).** `tools/round-80/pointer-bind.py --rev
HEAD` exits 0 with 5/5 but its own `--validate` then reports `record rev is not a
40-hex commit` (exit 1); C2 and C3 refuse a non-40-hex `--rev` with exit 2. The
frozen predicate requires a defect-free `--validate`, so the live arm is only
valid with a full hash — but C1's kill rule has no clause for it, unlike C2's.
*Smallest correction:* reject a non-40-hex `--rev` in `pointer-bind.py` (exit 2)
or record the rev as 40-hex unconditionally.

---

## 7. Smallest safe corrections, ranked

1. **C3 predicate:** record `--expect-sha256 <gate digest>` with the target
   receipt, or redefine `target_pin.matched`; the frozen sentence as written
   fails (measured).
2. **C2 rev binding:** declared rev first, must be a commit; this flags
   `prov-forged-rev` and changes the target numbers — the judge must choose
   between re-freezing `flagged 2` and recording the narrowing. Do not claim the
   rev class is closed otherwise.
3. **C1 duplicate rule:** require the conjunction, and add a green record control.
4. **C3 case injectivity:** one line in `bind()` plus one selftest case.
5. **Axis labels:** swap C1↔C2 on the SCORECARD rows, or justify the relabel in
   one sentence; state the freshness 0–10 mapping.
6. **C2 repair provenance:** a re-run at a named rev, not a copied tip digest.
7. **C1 receipt provenance:** `rev` + impl digests in the battery receipt.
8. **Disclose** the `R(C2) ∩ W(C3) = { tools/round-78/attack-gate.py }` pair and
   the shared `SCORECARD.md` write.

---

## 8. What holds (not attacked, so the judge knows the scope)

- C1's six numbers and both arms reproduce exactly; the live record is
  exact-token-clean; `--validate` is defect-free; the control reproduces the old
  weakness (4 false greens) for the stated reasons (2 substring binds, 2
  duplicate collapses — measured).
- C1's `pristine`/fixture arithmetic: reds 4, greens 2, control 4 — the
  fixtures are real reds and real greens, and a refuse-all candidate fails.
- C2's base population is **34**, not the 141 `*.json` files: only 34 carry an
  `instrument.path` + 64-hex `instrument.sha256`; all 34 exist at `16dfa009`;
  the two flags are exactly `prov-forged-instrument.json` and
  `c2-at-landing.json`; `--validate` on the base receipt is defect-free.
- C3's `pristine.cases 37 = 29 + 8` is *derived*, not invented: I measured the
  base selftest at 29 and exactly eight clauses with no isolating case; clause 5
  (`: refused without a reason`) is the one pre-existing case. Base arm
  9/0/0/9 verified. The nine table rows are four-cell, distinct, and each
  fragment matches exactly one clause.

---

```json
{
  "seat": "CriticClaims",
  "round": 80,
  "measured_rev": "b826010756ee32b13702899d9c6f83df55925d58",
  "base_rev": "16dfa009bf143080dfcdfc5f9ec34bd359536d90",
  "declaration": "84d68e90f8a1ea3a3a7f94a208695c21023c0472",
  "reachability": [
    {"claim": "R80-C1", "vacuous_path": "refuse every token", "blocked_by": "candidate_green_refusals 0 on the two green bind cases + live 5/5 arm", "blocked": true},
    {"claim": "R80-C1", "vacuous_path": "refuse every kind:record input (no green record control in the battery)", "blocked_by": "only the separate live arm's duplicates []", "blocked": false},
    {"claim": "R80-C1", "vacuous_path": "report duplicates but collapse checks_total (or count 6 without duplicates); duplicate_refused() accepts either half", "blocked_by": "nothing; the Rule's conjunction is not tested", "blocked": false},
    {"claim": "R80-C1", "vacuous_path": "emit the live 5/5 as a constant", "blocked_by": "nothing; no re-derivation clause binds the live receipt to the committed PROVINCE", "blocked": false},
    {"claim": "R80-C2", "vacuous_path": "flag nothing", "blocked_by": "flagged 1 + expected_control_flags 1", "blocked": true},
    {"claim": "R80-C2", "vacuous_path": "flag everything", "blocked_by": "unexpected 0", "blocked": true},
    {"claim": "R80-C2", "vacuous_path": "declare rev @HEAD@/main/eeee with a tip-matching digest (bound_at returns the tip first)", "blocked_by": "nothing; measured bound for @HEAD@, main, eeee", "blocked": false},
    {"claim": "R80-C2", "vacuous_path": "rewrite the flagging digest to the tip blob 40905d39", "blocked_by": "nothing; tip is the first disjunct", "blocked": false},
    {"claim": "R80-C3", "vacuous_path": "zero guards or zero rows reporting survivors 0", "blocked_by": "guards 9 and rows 9 as literal predicate constants; base reports rows 0 / survivors 9", "blocked": true},
    {"claim": "R80-C3", "vacuous_path": "a case that fails on everything kills every mutant", "blocked_by": "pristine.failures 0", "blocked": true},
    {"claim": "R80-C3", "vacuous_path": "one case binding two clauses", "blocked_by": "nothing; bind() checks clause-row bijection only (measured: one case fails mutants G03 and G04)", "blocked": false}
  ],
  "gaming": [
    {"class": "receipt deleted / instrument block removed", "caught": true},
    {"class": "window narrowed to exclude the failing receipt", "caught": true},
    {"class": "receipt relocated into an /attacks/-named dir with a compensating receipt to keep 34", "caught": false},
    {"class": "disclosed population change (kill rule permits it)", "caught": false},
    {"class": "row whose declared case is not written", "caught": true},
    {"class": "case asserting a source literal or a constant", "caught": false},
    {"class": "table fragment matching two clauses", "caught": true},
    {"class": "fixture set weakened after the freeze while control stays at 4", "caught": false},
    {"class": "C2 flagging digest overwritten with the tip digest", "caught": false}
  ],
  "axis_rulings": [
    {
      "claim": "R80-C1",
      "axis_claimed": "calibration",
      "ruling": "not calibration; freshness by the lane's own recorded label and by AXES.md's definition. The counter reads PROVINCE.md vs live files and counts zero SCORECARD/SHONEN mismatches (the live 5/5 is true). §9: 'A calibration claim must count mismatches between the lane's self-assessment (SCORECARD/SHONEN) and observed repo state.' Round 79 recorded the same surface as freshness (SCORECARD.md:6144; plans/round-79-claims.md:17), and the round-79 closure recorded CriticClaims' reading that it is 'a strictness increment on the round-78 pointer rule rather than a new surface'.",
      "smallest_correction": "land the row as freshness or state one sentence why the surface changed axis"
    },
    {
      "claim": "R80-C2",
      "axis_claimed": "freshness",
      "ruling": "calibration by §9: it counts a SCORECARD-vs-repo mismatch (SCORECARD.md:6144 'verified' citing c2-at-landing.json whose digest matches no committed blob). Freshness as an owned axis is otherwise legitimate with a measured baseline (32/34 = 9.41) and a stated reason, but the 0-10 mapping is undeclared and the Q5 note (freshness is a fleet axis, not a lane-owned proxy) is being reversed.",
      "smallest_correction": "swap the C1/C2 labels and state the round(10*n/d,2) mapping"
    },
    {
      "claim": "R80-C3",
      "axis_claimed": "depth",
      "ruling": "depth is defensible for the decision-table surface only; the instrument's refusals are unchanged, so it is not a capability acquisition. The claim types it capability acquisition and depth at once.",
      "smallest_correction": "call it depth (table plus isolating cases) and drop the capability row, or keep the capability row and drop depth"
    }
  ],
  "file_overlap": {
    "writes": {
      "C1": ["tools/round-80/strictness-battery.py", "tools/round-80/pointer-bind.py"],
      "C2": ["tools/round-80/receipt-provenance.py", ".ufo/waves/round-79/l1/scores/c2-at-landing.json"],
      "C3": ["tools/round-80/guard-battery.py", "tools/round-78/attack-gate.py", "SKILL.md"],
      "shared_landing": ["SCORECARD.md"]
    },
    "read_write_intersection": ["tools/round-78/attack-gate.py"],
    "intersection_note": "C2 hashes attack-gate.py blobs for the two round-78 receipts (c1-at-record, c1-at-tip); C3 edits that file. No verdict flips today because both receipts declare pre-edit commits (93753d88, 51c08cda). The claims' sentence forbids reading another's receipt, not another's file; disclose the pair.",
    "counter_intersection": "empty: no counter reads another claim's round-80 receipt"
  },
  "kill_rule_gaps": [
    {"id": "G1", "claim": "R80-C3", "gap": "predicate requires target_pin.matched true but the command omits --expect-sha256; measured false without it (expected \"\"), true with it", "severity": "blocker"},
    {"id": "G2", "claim": "R80-C3", "gap": "frozen relation is 'message prefix'; code and SKILL header use 'fragment' membership+uniqueness; G03-G06 frozen strings are not prefixes of source or rendered messages", "severity": "high"},
    {"id": "G3", "claim": "R80-C3", "gap": "ExecGuard spec expects survivors 9; ReviewerC3 spec expects 8 survivors + 1 killed at the same base revision", "severity": "high"},
    {"id": "G4", "claim": "R80-C3", "gap": "no case injectivity: two rows may name one case (demonstrated one case failing on mutants G03 and G04)", "severity": "medium"},
    {"id": "G5", "claim": "R80-C2", "gap": "symbolic/non-commit declared rev accepted when the digest matches the tip (measured @HEAD@, main, eeee all bound)", "severity": "high"},
    {"id": "G6", "claim": "R80-C2", "gap": "prov-forged-rev.json (declared rev eeee..., not a commit) is verdict 'bound' at the tip; the predicate's unexpected 0 requires it. Strict declared-rev rule reports 6 flagged, not 1", "severity": "high"},
    {"id": "G7", "claim": "R80-C2", "gap": "repair by copying the tip digest (40905d39) is indistinguishable from a genuine re-run and is not named by the kill rule", "severity": "high"},
    {"id": "G8", "claim": "R80-C1", "gap": "duplicate_refused() accepts cell_id in duplicates OR checks_total>5 and not ok; the Rule requires both", "severity": "medium"},
    {"id": "G9", "claim": "R80-C1", "gap": "battery receipt carries no rev and no impl digests; the candidate build cannot be pinned", "severity": "medium"},
    {"id": "G10", "claim": "R80-C1", "gap": "pointer-bind accepts --rev HEAD (5/5, exit 0) but its own --validate then reports 'record rev is not a 40-hex commit' (exit 1); C2/C3 refuse non-40-hex revs", "severity": "low"}
  ],
  "receipts": {
    "c1_battery_target": "w1/CriticClaims/c1-battery-head.json",
    "c1_battery_base": "w1/CriticClaims/c1-base-battery.json",
    "c1_live": "w1/CriticClaims/c1-live-head.json",
    "c2_target": "w1/CriticClaims/c2-head.json",
    "c3_target_no_flag": "w1/CriticClaims/c3-head-noexpect.json",
    "c3_target_with_flag": "w1/CriticClaims/c3-head-expect.json",
    "c3_clause_mutations": "w1/CriticClaims/clause-mutations.json",
    "c1_round79_live": "w1/CriticClaims/live79-at-head.json"
  },
  "measured": {
    "c1": {"cases": 4, "green_cases": 2, "candidate_false_greens": 0, "control_false_greens": 4, "candidate_green_refusals": 0, "control_green_refusals": 0, "live_checks_total": 5, "live_matched": 5, "live_mismatches": 0, "live_unparsed": 0, "live_duplicates": [], "base_candidate_false_greens": 4},
    "c2": {"receipts": 34, "flagged": 2, "expected_control_flags": 1, "unexpected": 1, "target_flagged": 2, "bound_rows": 32, "matched_rev_eq_tip": 24, "strict_declared_rev_flagged": 6},
    "c3": {"guards": 9, "rows": 9, "bound": 9, "survivors": 0, "pristine_cases": 37, "pristine_failures": 0, "target_pin_matched_without_flag": false, "target_pin_matched_with_flag": true, "base_survivors": 9, "base_pristine_cases": 29, "base_clauses_detected_by_existing_case": 1, "base_clauses_undetected": 8}
  }
}
```
