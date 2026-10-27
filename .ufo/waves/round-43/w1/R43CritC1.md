# R43CritC1 — attack of the DRAFT P43-C1 (v4 triage table re-scored on a fresh held-out set)

VERDICT: DEFECTS FOUND — the draft predicate is **unreachable as written** (its new lookup binding
is falsified by the committed round-42 receipt: the frozen control scores 19/24 on identical class
structure) and the claim is **mislabeled as depth** under AXES.md and prompt §6 item 9 (the SKILL
table does not move one byte; the work is generator honesty + a fresh-input re-score). Both are
fixable before the freeze; concrete quote→replacement text in §6. The kill-rule controls in (b)
hold: no do-nothing, relabelled, or hand-edited manifest reaches `matched == 78` under the carried
round-42 clause set.

All probes read-only over committed bytes (git show / jq / sha256sum / python3). No REA, unblob,
sasquatch, unsquashfs or 7z run; no published-image byte touched. No tools installed or upgraded.
Artifacts: `.ufo/waves/round-43/w1/artifacts/R43CritC1/` (`probe-log.txt`, `lookup-19-of-24.txt`).

---

## 1. (a) Is this a depth move? NO as drafted — and the draft's own "Surface moved" paragraph admits it

**Bytes that move (round 43):**
- `plans/round-43-claims.md` (new)
- `tools/round-43/{c1-counter.py, heldout-gen-v4r43.py, c2-controls-r43.py}` (new; the refusal is a
  port-side change to manifest finalization)
- `corpus/evidence/round-43/c1/heldout/` (new data, post-freeze)
- `corpus/SOURCES.md` (+1 row, S135 — 0 occurrences at the base, verified)

**Bytes that do NOT move:** the SKILL v4 table region. Measured: the region (marker line
`<!-- sqfs-triage-table v4 -->` through the end of the first markdown table after it) hashes

```
ac85bdc16607159aa4d628ecf2521dd6a57e7ef48beeab62a437976b7e6328af
```

at **both** `d1681696` (round-42 freeze) and `6b9e64fe` (round-43 base) — it is already unmoved
before the round starts, and the claim keeps it that way. The draft says so itself: *"This claim
does not change one table byte."*

**The exact command that shows the table unmoved** (the draft's stated command — "the round-43 C1
counter at the freeze exits 2 (`no_manifest_at_rev`)" — is the *do-nothing control*, not the
table-unmoved witness; a reader cannot tell the table from the absence of data):

```
for r in d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b <FREEZE> <REV>; do
  git show "$r:SKILL.md" \
    | awk '/<!-- sqfs-triage-table v4 -->/{f=1} f{print} f&&/^\|[[:space:]]*clean-empty/{exit}' \
    | sha256sum
done
# all three must print ac85bdc16607159aa4d628ecf2521dd6a57e7ef48beeab62a437976b7e6328af
```

The enforceable form is the counter's own `v4_block_identical` binding (region at REV == region at
freeze == region at `d1681696`; `skill_block_drift` over `d1681696..REV` empty). The round-43
counter must compare the region at **three** revisions — `d1681696`, FREEZE, REV — the draft text
binds only REV-vs-`d1681696`.

**Axis ruling.** Prompt §6 item 9, verbatim: *"Re-scoring a rule the lane already holds on new
inputs, or counting rows a sourceless fixture also counts, is quality work, never coverage or
depth."* Block 21 is a rule the lane holds: it is committed, frozen since `d1681696`, cited by the
round-42 closure, and it was *measured* 78/78 against its evaluator on 78 held-out envelopes in
round 42 (receipt `c2-at-eb8215ac.json`, `matched 78, n 78`) — the round stopped on the
*generator's honesty*, not on any table property. Completing the stopped measurement on a fresh
seed adds measurement integrity, not verifiable technical detail. AXES.md depth: *"decision tables
with real thresholds, named error signatures, cited sources — a reader can act on SKILL.md alone."*
Nothing new enters SKILL.md. The lane's own registry agrees: the refusal semantics are QUALITY.md
row 85, filed under M42-2 *"sharpens 83, 84"* — a quality row, not a depth surface. The round-42
closure verdict on this exact table was *"depth unchanged (claim not met; no depth improvement
credited)"*; nothing in the draft changes what the table is.

Steelman considered and rejected: "the table stopped unscored, so this is the first completed
score, not a re-score." §6.9 has no stopped-score exception; the withheld thing was a measurement
outcome, not detail; and §6.9's companion rule — *"Name the axis by the surface the round changes,
not by the number it produces"* — names the generator/counter/evidence here, not SKILL.md.

**Impact:** calibration is the honest axis (the lane's self-reporting infrastructure can no longer
over-declare — "overreach caught" is the calibration signal; the tie at 10 makes any owned axis a
lowest axis, so the round shape stays valid with C1=calibration, C2=coverage). Alternative if the
L1 insists on depth: land routed defect R42-V3's demanded in-SKILL status line for block 21 as the
claim's moved surface (§6, change 1b) — one line outside the frozen table region.

---

## 2. (b) Can a do-nothing control, the relabelled round-42 manifest, or a hand-edited manifest reach `matched == 78` with every binding true? NO — provided the port keeps the carried clause set

The draft carries the round-42 load-bearing bindings: `seed == freeze`, first-add-after-freeze,
regen byte-identity, `envelope.subject.sha256 == carrier sha256`, counter-computed
`observed == declared`. Verified against the frozen counter (`tools/round-42/c2-counter.py:159-181`
CLAIM_BINDINGS) and the committed manifest:

| attack | verdict | binding that stops it |
|---|---|---|
| do-nothing | NO | counter raises `no_manifest_at_rev` (exit 2) before scoring (`measure()`, `man_b is None`) |
| round-42 manifest relabelled to `corpus/evidence/round-43/c1/heldout/` | NO | the committed manifest declares `seed = d1681696…` (verified) — a round-42 freeze hash can never equal the round-43 freeze hash (a different commit); `seed_matches_freeze` false. Independently, regen with `--seed <r43-freeze>` rebuilds different carrier bytes → `carriers_regenerated` false. Note the relabelled copy IS "first added after the freeze" when committed post-freeze, so CTL-C1-1's parenthetical "(seed ≠ freeze; manifest not first-added after the freeze)" is half wrong — the seed binding is the real catcher (fix in §6.5) |
| hand-edited manifest (declared tuples edited) | NO, with one disclosure | carrier bytes cannot be hand-edited (`carriers_regenerated` runs the frozen generator with `--seed <freeze>`; `carriers_committed` ties committed bytes to the manifest digests; `envelopes_valid` ties each envelope to its carrier by subject digest). A manifest whose `declared_features` are edited *away* from the envelopes fails `observed_features_match_declared`, which the counter computes **from the committed envelope bytes with its own frozen extraction** — the manifest's own `generator.tuple_check` record is not trusted for this. Editing declared *toward* the envelopes produces exactly the honest manifest (see (c)) |

The residual surface is the disclosed limit, unchanged from round 42: the counter never re-runs
REA on the committed carriers (regen runs the generator **without** `--run`), so envelope bytes are
trusted committed evidence. A fabricated-but-internally-consistent envelope set that both the
interpreter and the evaluator label identically is indistinguishable by design — that is the
claim's disclosed limit ("agreement with an independent evaluator cannot tell this table from any
other table labelling the same envelopes the same way"), not a new hole.

**Gap the freeze must close (kill rule):** no committed control demonstrates the *counter* side of
the hand-edit defense — a manifest whose declared tuple is edited to mismatch its envelope, fed to
the frozen round-43 counter, exiting non-zero with `observed_features_match_declared` false. CTL-C1-2
is generator-side only. Add CTL-C1-4 (§6.6); it is cheap on the dev arm.

---

## 3. (c) The refusal: "declare the observed by reading the envelope first" is a vacuous implementation the draft accidentally permits; pin the semantics

The draft says the port *"replaces the generator's declared-tuple predictor with a measured one"*
and *"REFUSES to write the manifest unless every observed tuple equals the tuple the manifest would
declare"*. Read literally, a port may implement: run REA → extract observed → **declare the
observed** → the check is vacuously true → write. Under that implementation the refusal certifies
nothing, and `observed_features_match_declared` becomes true by construction with no informational
content beyond "an envelope exists".

The intended semantics (QUALITY.md row 85, verbatim): *"a generator writes a declared feature tuple
**only after comparing it** with the tuple its own `--run` observed, refusing the manifest on any
difference."* I.e.: the declared tuple remains the **predictor's** tuple — a pure pre-run function
of (class, drawn factors, fixture pins), written before the REA run; the refusal compares
*prediction vs observation* per carrier and exits 3 `declared_tuple_unobserved` with the per-carrier
diff list, writing nothing. This is what makes the draft's own C02 sentence coherent: *"Combo C02's
round-42 shape … must appear among the new seed's combos with the manifest declaring what was
observed, including `depth-limited`"* — it forces the **predictor to be amended** to model REA
6.5.0's `depth-limited` minting beside a failing chunk at the depth ceiling (the round-42
predictor emitted `{extractor-failure, unpublished-entry}`; the run observed
`{depth-limited, extractor-failure, unpublished-entry}` — re-verified from committed bytes,
`artifacts/R43CritC1/probe-log.txt` §3), and the refusal then *proves the amended prediction was
observed*. Under the vacuous reading that demonstration evaporates.

**What stops a generator that lies about what it observed:** the refusal stops the *accidental* lie
(predictor drift — the entire M42-2 class). It cannot and need not stop a *deliberate* liar; the
liar's surface is bounded downstream: the counter recomputes the observed tuple from committed
envelope bytes (frozen extraction), envelopes are bound to carriers by subject digest, carriers to
the seed by regen, and the seed to the freeze hash. A self-consistent lie across all four is the
disclosed fabrication limit, unchanged from round 42.

**Binding the draft must add** (fixable defect, not tradeoff): the refusal currently compares
*generator-extracted* observed against the declaration, but the claim binding is evaluated by the
*counter's* `observed_features`. These are two independent implementations. If they diverge, the
generator writes a manifest the counter then rejects — an honest stop, but a wasted round discovered
only at measure time. Bind the port to the counter's extraction (import or mirror the frozen
`observed_features`/`canon_features` algorithm, equivalence demonstrated in the QUALITY 84 dry run).

Recommended additional auditability (should, not must): record the predictor's tuple per carrier
under a separate manifest key (e.g. `predicted_features`, outside the six-field binding) so the
committed manifest durably shows *prediction confirmed*, not just *declaration consistent*; today
that evidence exists only in the refusal's stdout diff list and CTL-C1-2's receipts.

---

## 4. (d) `combo_unseen_majority >= 12` — the bound is right; the newly-added lookup binding is falsified by committed evidence

Two separate things in the draft sentence:

> *"the frozen lookup control `.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` run through the
> frozen interpreter scores strictly fewer than half of the held-out `combo` envelopes
> (`combo_unseen_majority` ≥ 12 of 24)"*

**The lookup binding is empirically false on identical class structure.** Committed receipt
`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`: `lookup.score = 19`, `n_combos = 24`,
`below_half = false`, `binding = false` ("reported, not bound (L1 freeze decision)") — see
`artifacts/R43CritC1/lookup-19-of-24.txt`. Why: CTL-C2-7's rows are per-label precedence *patterns*,
not exact-tuple keys — its `depth-limited` row (handler `squashfs_v4_*`, gap kinds `*`, published
`>0`) matches any v4 envelope with files regardless of gaps, and the `unknown-residue` /
`partial-body-failure` rows do the same for other shapes. Measured consequence: the lookup was
correct on 19/24 held-out combos while only **5/24** combos had observed tuples inside the dev
named-class union (`combo_unseen_majority.seen_in_dev = [C03, C07, C12, C13, C16]`). Lookup score
is not monotone in the unseen statistic, so on a new seed with the same class structure the lookup
binding is expected to fail exactly as it did in round 42 — the claim would honestly stop at
`matched == 78` with the lookup binding false. Round 42 left this control **reported, not bound**,
for exactly this reason (freeze amendment recorded in the receipt and `plans/round-42-claims.md`).
If the canonical judge keeps the `< half` binding, P43-C1 is unreachable; if the intent was the
parenthetical only, the sentence as drafted is a landmine for the porting seat. **Smallest safe
correction: delete the binding, keep the control byte-identical (`lookup_control_identical`,
already in the carried clause set) and its score reported** (§6.2).

**`>= 12 of 24` is the right bound** — it is `ceil(24/2)`, exactly as the frozen round-42 counter
computes it (`majority_need = (len(combos) + 1) // 2`, binding string
`len(unseen) >= ceil(n_combos/2)`), and it is the sole bound anti-lookup witness per the round-42
freeze decision. What the draft must restore is the **union definition** round 42 carried and the
draft dropped: the union of the named-class declared tuples in the frozen round-42 dev-arm manifest
(`corpus/evidence/round-42/c2/dev/manifest.json`, `carriers[].declared_features`, canonicalized;
39 distinct tuples, re-verified). Using the round-43 held-out's *own* named-class union would be
strictly weaker — a lookup induced from the held-out named classes would be invisible to it. Also
note the residual seed-lottery: with the seed fixed to the freeze hash, `unseen` is determined by
the draw (round 42: 19). If the freeze seed yields 11, the claim honestly stops; to fail **loudly
at data time instead of after committing a dead set**, add `--verify` to the data-procedure command
(the port inherits `verify()`, which already recomputes the observed unseen majority and exits 1 on
FAIL) and add the C02-shape assertion below (§6.3, §6.4).

---

## 5. (e) Missing bindings and kill rules

1. **Lookup binding** — falsified; remove (§4, §6.2).
2. **Union definition for `combo_unseen_majority`** — dropped by the draft; restore verbatim from
   the round-42 counter (§6.3).
3. **The C02-shape requirement is unoperationalized** — "must appear among the new seed's combos"
   is a property of a seed the L1 cannot choose (the seed **is** the freeze hash). Make it a
   generator-side loud assertion executed during the `--run` data procedure (exit 4, nothing
   written) and keep it out of the counter's binding list (§6.4).
4. **No counter-side anti-hand-edit control** — add CTL-C1-4 (§6.6).
5. **Writer not in the frozen-paths list** — the round-42 counter auto-freezes the writer scope
   (`tools/round-39/gen-squashfs.py`, named by the generator's manifest record) at the freeze; the
   draft's C1 frozen paths name the round-42 tools, fixtures, dev arm and receipts but never the
   writer. Name it (§6.7).
6. **S135 binding is not concrete** — "whose license basis is cited by the new SOURCES row S135"
   binds nothing checkable. Bind the row's cells (id, URL = the unblob 26.6.4 LICENSE pinned URL,
   digest) — or freeze `corpus/SOURCES.md` for C1 (§6.8).
7. **Generator-vs-counter extraction equivalence** — see §3 (§6.4).
8. **Three-way region compare** — see §1 (§6.8).

Kill-rule set after corrections: CTL-C1-0 do-nothing (exit 2) ✓; CTL-C1-1 relabel (seed) ✓;
CTL-C1-2 refusal red/green ✓; CTL-C1-3 shortcut controls re-scored below target ✓; **CTL-C1-4
counter-side declared-edit rejection (new)**. The do-nothing kill rule remains sound: no control
meets the target, so C1 proceeds to data.

---

## 6. Smallest safe corrections (quote → replacement)

**1a. (recommended) Re-label the claim off depth** — quoted:
> `## R43-C1 — depth: the v4 SquashFS triage table scored on a fresh held-out set under a generator that refuses unobserved declarations`
> `R43-C1 works depth, R43-C2 works coverage.`

Replacement:
> `## R43-C1 — calibration: the v4 SquashFS triage table scored on a fresh held-out set under a generator that refuses unobserved declarations`
> `R43-C1 works calibration (the lane's scoring infrastructure can no longer declare what its own run did not observe — the M42-2 overreach class is now mechanically caught; QUALITY 85), R43-C2 works coverage. The tie at 10 makes every owned axis a lowest axis, so the round shape is unchanged.`

**1b. (alternative, only if the L1 keeps a depth claim)** — add the R42-V3 surface as the moved
bytes, quoted:
> `This claim does not change one table byte: it re-freezes the frozen table …`

Replacement:
> `This claim changes one SKILL byte outside the frozen table region: rule block 21 gains the in-SKILL claim-status line routed defect R42-V3 demands ("scored: R43-C1, see .ufo/waves/round-43/l1/scores/ …; stopped unscored at round 42, receipt .ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json"), added before the freeze and frozen as a C1 path. The v4 table region itself still does not change one byte …`

**2. Remove the lookup binding** — quoted:
> `the frozen lookup control `.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` run through the frozen interpreter scores strictly fewer than half of the held-out `combo` envelopes (`combo_unseen_majority` ≥ 12 of 24)`

Replacement:
> `the frozen lookup control `.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md` is byte-identical to its frozen bytes (`lookup_control_identical`), and its score on the held-out `combo` envelopes is reported, not bound — the committed round-42 receipt scores it 19/24 on the round-42 held-out combos (`below_half: false`), and its per-label pattern rows are not monotone in the unseen statistic, so a `< half` binding would be unreachable on identical class structure; the bound anti-lookup witness is `combo_unseen_majority` ≥ 12 of 24`

**3. Restore the union definition** — append to the predicate after `combo_unseen_majority`:
> `… where UNSEEN means the combo's observed six-field tuple lies outside the union of the named-class declared tuples in the frozen round-42 dev-arm manifest `corpus/evidence/round-42/c2/dev/manifest.json` (`carriers[].declared_features`, canonicalized), exactly as the frozen round-42 counter computes it (`len(unseen) >= ceil(n_combos/2)`); the round-43 held-out's own named-class tuples are NOT the union`

**4. Pin the refusal semantics + extraction equivalence + C02-shape assertion** — quoted:
> `the generator runs REA on every carrier, extracts the observed six-field feature tuple from each envelope it produced, and REFUSES to write the manifest unless every observed tuple equals the tuple the manifest would declare; on refusal it exits non-zero and writes no manifest.`

Replacement:
> `the generator's declared tuple remains the predictor's tuple — a pure pre-run function of (class, drawn factors, fixture pins) — and its predictor is amended to model REA 6.5.0's depth-limited minting beside a failing chunk at the depth ceiling (the C02 fix); after the `--run` the generator extracts the observed six-field tuple from each envelope it produced using the same extraction algorithm as the frozen counter's `observed_features` (equivalence demonstrated in the QUALITY 84 dry run) and REFUSES to write the manifest unless every observed tuple equals the predictor's tuple (exit 3 `declared_tuple_unobserved`, per-carrier diff list on stdout, no manifest write); the data-procedure command carries `--verify` so the observed unseen majority and byte-identical regen are checked loudly before any commit, and the run additionally exits 4 `c02_shape_absent` (nothing written) unless at least one combo envelope's observed tuple contains both extractor-failure and depth-limited — the C02 shape`

**5. Fix the CTL-C1-1 rationale** — quoted:
> `CTL-C1-1 the round-42 held-out manifest copied to the round-43 path: the counter exits non-zero (seed ≠ freeze; manifest not first-added after the freeze);`

Replacement:
> `CTL-C1-1 the round-42 held-out manifest copied to the round-43 path: the counter exits non-zero (`seed_matches_freeze` false — the copied manifest declares the round-42 freeze seed `d1681696…`, and `carriers_regenerated` false under `--seed <round-43 freeze>`);`

**6. Add the missing kill control** — new bullet after CTL-C1-3:
> `CTL-C1-4 counter-side hand-edit rejection: a dev-arm manifest with one carrier's `declared_features` edited to a value its committed envelope does not observe, scored by the frozen round-43 counter, exits non-zero with `observed_features_match_declared` false (the counter computes the observed tuple from envelope bytes, never from the manifest's `generator.tuple_check` record)`

**7. Frozen paths, add the writer and the status line (if 1b) and SOURCES** — quoted:
> `C1: this file; `tools/round-43/{c1-counter.py,heldout-gen-v4r43.py,c2-controls-r43.py}`; the round-42 frozen tools …`

Replacement (append):
> `…; the SquashFS writer `tools/round-39/gen-squashfs.py` (named by the generator's manifest record, auto-frozen by the counter's writer scope at the freeze); the S135 row cells of `corpus/SOURCES.md` (id, pinned LICENSE URL, digest) — or `corpus/SOURCES.md` in full; [if 1b: the block-21 claim-status line region of `SKILL.md`]`

**8. Predicate, region compare + S135** — quoted:
> `the v4 table region of `SKILL.md` (from the line containing `<!-- sqfs-triage-table v4 -->` through the end of the first markdown table after it) is byte-identical to the same region at `d1681696``

Replacement:
> `the v4 table region of `SKILL.md` (from the line containing `<!-- sqfs-triage-table v4 -->` through the end of the first markdown table after it) is byte-identical to the same region at `d1681696` at the freeze and at the measured revision (sha256 `ac85bdc16607159aa4d628ecf2521dd6a57e7ef48beeab62a437976b7e6328af` at `d1681696` and at the base); `corpus/SOURCES.md` carries row S135 naming the unblob 26.6.4 LICENSE at its pinned URL with its committed digest`

**Also (implementation notes for the port, not predicate text):** the r42 counter's
`manifest_generator_path` binding whitelists generator names `('heldout-gen-v4.py', GEN)` — the
round-43 counter must accept `heldout-gen-v4r43.py`; the data-procedure command should include
`--verify` (see 4 above); the refusal red case (CTL-C1-2) must document its exact invocation
(reading the committed r42 C02 manifest + envelope, exiting 3) so the receipt is reproducible.

---

## Evidence

- `artifacts/R43CritC1/probe-log.txt` — region hashes at `d1681696` and base (identical);
  receipt lookup 19/24 `below_half: false`; receipt `combo_unseen_majority` (need 12, unseen 19,
  seen [C03,C07,C12,C13,C16], union source the dev manifest); C02 declared
  `{extractor-failure, unpublished-entry}` vs observed `{depth-limited, extractor-failure,
  unpublished-entry}` re-derived from `envelope.data.normalized_result.extraction_gaps` and
  `rea-full.json`; manifest seed `d1681696…`, 28 classes, 78 carriers; CLAIM_BINDINGS list;
  QUALITY.md row 85 verbatim; S135 absent at base.
- `artifacts/R43CritC1/lookup-19-of-24.txt` — the falsification of the draft's lookup binding with
  the mechanism (pattern rows, not exact-tuple keys).
- No REA/unblob/sasquatch run; no third-party image touched; no tools installed or upgraded;
  scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43CritC1` removed on exit.
