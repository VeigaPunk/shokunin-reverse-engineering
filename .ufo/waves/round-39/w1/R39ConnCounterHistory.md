# R39ConnCounterHistory — cross-round counter-history connector (wave 1, pre-freeze)

**Verdict: DEFECTS FOUND** — the DRAFT round-39 designs repeat at least three historical counter-falsification
classes and fix four others; one class (receipt fabrication) I reproduced live against the draft C1 predicate
shape. All findings are design-level and pre-freeze: nothing in the lane was written except this report and
`.ufo/waves/round-39/w1/artifacts/R39ConnCounterHistory/`.

Axes named (round-39 declared): **coverage** (R39-C1) and **depth** (R39-C2).

Method: read the DRAFT claims, SCORECARD rounds 32–38, QUALITY rows 55–81, the r35/r36/r38 critic falsifier
files, the r38 claims/counter, the round-36 SKILL table, and the r38-w2 AVM probe envelopes; then reproduced
the cheapest fabrication class against the draft's C1 integrity gate. No REA run, no unblob/sasquatch run, no
K5/K6 contact, no tool installs (the only execution was `node tools/round-27/xpin-attribute.mjs` on my
fixture, exactly as the frozen counters call it), no VCS mutation. Scratch removed; cited bytes copied to my
artifacts dir.

---

## 1. Live reproduction: an r39-C1-shaped fabricated receipt passes the draft's only integrity gate

The draft P39-C1 asks, per carrier, that a committed after-receipt name `squashfs_v4_be`, publish every
oracle `(relative-path suffix, sha256)`, carry `unpublished-entry` gaps exactly on in-tree symlinks, none for
escaping ones, hold `subject.digest == pin`, and **"recompute to its stored evidence id under the rea-agents
6.5.0 rule"**. I built that receipt for K1 from frozen public lane bytes only:

- inputs: K1 pin from `.ufo/waves/round-38/c1/carriers.json`, 5 rows of `corpus/evidence/round-37/c1/K1/oracle.tsv`,
  the one in-tree symlink from `K1/src` (`link-to-hello` — observed `corpus/evidence/round-38/c1/K2/after.json`
  carries the identical gap shape, `kind: unpublished-entry`);
- construction: ~40 lines of python3 stdlib (the projection function is copied from
  `.ufo/waves/round-36/w1/R36CriticC1Shortcut.md` §3, which matched REA's id byte-for-byte for both forged
  and genuine records);
- result (commands and outputs preserved in §A below): stored id `ev_313f5a17…` recomputes as
  **6.5.0 rule = 6.7.0 rule = stored** (`xpin-attribute` verdict `both`), and REA's own `parseEvidence`
  **accepts** the record under both pins. Artifact: `artifacts/R39ConnCounterHistory/fabricated-K1-after.json`
  (sha256 `37941e32…`), plus a paired fabricated before-receipt (`0e260a06…`) in the r38-v2 paired-arm shape,
  which v2/v3 showed is equally forgeable (`R38CriticClaimsC1.md` §5b).

Every clause of P39-C1 that touches the receipt is satisfied by this fabrication. The remaining clauses are
the PROVINCE/SOURCES/README bindings (see rank 2) and the temporal clause — "first added in a commit that
descends from the freeze" — which a fabrication satisfies by committing after the freeze (this kills r38's
`same-commit-freeze` class `s`, and is a genuine improvement over r38). **What the fabrication cannot satisfy
is a provenance clause — and the draft predicate has none.** This is QUALITY 78 verbatim: "a receipt-integrity
check … is not provenance: anyone holding the producer's digest code can re-hash a fabricated envelope"; and
`R36CriticC1Shortcut.md` §8: "No binding over claimant data can make 'receipt fabricated from the oracle'
red; only (1) [the counter/harness executes] closes it." The r36 round closed this with four independent
non-author reproductions (`.ufo/waves/round-36/w1/R36ExecReproK*.md`); the r38 round never closed it and its
C1 stopped; the r39 draft inherits the r38 predicate shape with a **receipt-only counter**, and lists "a
fabricated receipt" in the kill rule — a control that can only *stop* C1, never let it pass honestly.

---

## 2. Ranked exposure list (historical class → draft design → cheapest test)

Ranking: recurrence × decisiveness against a coverage/depth verdict × test cost. "Exposed" = the draft as
written can be met by the historical shortcut; "addressed" = the draft structurally fixes it; "partial" = the
text gestures at it but the mechanism is not in the predicate/kill list.

### Rank 1 — Fabricated receipt with re-minted evidence id (r36 F1–F11, r38 §3/§5b; QUALITY 78) → R39-C1. **EXPOSED — CONFIRMED LIVE (§1).**
- Cheapest test: already run (this seat, §1, cost seconds). For the freeze: the L1 should decide pre-freeze
  whether C1 is to be *passable*. If yes, the predicate needs a provenance clause (non-author independent
  re-run per carrier naming the package root, as r36 did) or the counter/harness must execute the extraction
  itself (r36 critic correction 2). The kill-rule control alone guarantees the claim can only ever stop.

### Rank 2 — Surface-binding shortcuts: decoy heading / reused row / stem-prefix / stub entry (r36 C2 A1–A4, r38 falsifier matrix `e h j m`; QUALITY 77) → R39-C1 bindings. **EXPOSED.**
- The draft C1 predicate repeats r38's binding language almost verbatim: "`PROVINCE.md` holds a
  `## Round-39 additions to Core` row naming `squashfs_v4_be` that cites the round-39 knowledge entry, which
  cites a `SOURCES.md` row opened 2026-10-26 whose used-by lists that entry", "coverage-map row naming the
  entry stem". Each binding has a scored r38 bypass: `e` decoy duplicate heading (`section()` first match),
  `h` reuse of an existing opened-2026-10-26 row (green in r38 v1/v2/v3 — the draft's own "opened 2026-10-26"
  wording is the same condition that made S110 reuse pass), `j` README stem-prefix substring, `m` one-line
  stub entry (`entry_present` = path exists). The draft's C1 kill list (do-nothing, copied r38 receipts,
  fabricated receipt, materialise-the-symlink, wrong gap kind, escaping-kept) contains **no** surface-binding
  control — the same control-coverage gap r36 C2 documented ("the frozen control set covers deletion, junk
  counts and suffix-visible substitution only").
- Cheapest test: port the four r38 recipes (they are single text edits with verbatim constructions in
  `R38CriticClaimsC1.md` §2) into fixture repos and score the new counter pre-freeze. Cost: minutes.

### Rank 3 — Frontier-note supersession binding green while saying the opposite (r38 §4) → R39-C1. **EXPOSED (inherited-binding recurrence risk).**
- r38's `frontier_note` binding was true already at the freeze: two pre-existing PROVINCE lines contain
  "big-endian" and "superseded" while saying big-endian stays Frontier; do-nothing scored it `true`. The r39
  draft repeats "a round-39 frontier note supersedes the big-endian part of the Frontier bullet" with no
  structural condition (old bullet text absent; note inside the round-39 section; "stays here" removed).
- Cheapest test: evaluate the would-be binding expression against the **base** revision `a2f64e1d`. If it is
  true at base (r38's was), the binding is inherited and will certify an unmoved surface.

### Rank 4 — Lexical table meets target without causal content (r32 C2v3; QUALITY 58) → R39-C2. **PARTIAL.**
- The r39-C2 interpreter assigns class labels from a SKILL.md table (signature → cause → action). A table
  whose signature column is the literal diagnostic strings observed on development envelopes passes if the
  held-out envelopes' diagnostics carry distinguishing keywords — the r32 shape (word-bag credited 4/4;
  denial credited 4/4; frozen target could not distinguish). I confirmed the BE diagnostics are enumerable
  and stable: `rea-k1-orig.json` → `MaliciousSymlinkRemoved`, `rea-k1-avm.json` →
  `ExtractCommandFailedReport` + `extractor-failure` gap. The draft's kill control "the round-36 table
  transcribed into the interpreter grammar" covers the LE-prose-table variant only; a development-envelope
  keyword table is the general class.
- Cheapest test: pre-freeze, hand-author a table mapping only the diagnostic typenames/gap kinds seen on
  development carriers to the seven classes; if the frozen interpreter scores it `matched == N` on the
  held-out set, stop C2 by the r32 precedent (this control is the C2 analog of the C1 "fabricated receipt"
  control and should be in the kill list).

### Rank 5 — Held-out determinism and class-set registration (r34b; QUALITY 69/70 + the round's own correction) → R39-C2. **PARTIAL — mechanism right, two residuals.**
- The draft's held-out design (seed = freeze commit hash; generator assigns labels before any REA run;
  byte-identical regeneration; subject-digest binding; manifest first-added no later than envelopes) is the
  QUALITY-69 mechanism done right — this is the strongest part of the draft. Residuals: (a) "every carrier
  regenerates byte-identically from that seed" requires the squashfs toolchain pinned in the freeze
  [INFERENCE: `tools/round-37/gen-squashfs.py` shells an external mksquashfs; I did not open its source to
  confirm the invocation] — if the tool version is not pinned, the byte-identical clause is unverifiable and
  a regeneration drift would be indistinguishable from tampering; (b) the class list is "draft; finalised
  from wave-1 recon" — per QUALITY 70's correction, set equality detects a *dropped* class, not an unfaithful
  one; `no-squashfs-chunk` conditional on "if recon shows it distinct" is exactly a class the recon could
  silently drop to the floor.
- Cheapest tests: (1) regenerate the held-out set twice (two instants, same seed) and `cmp` the carriers;
  (2) frozen interpreter asserts registered class set == pinned set (count + names) and the counter carries
  a one-class-dropped red fixture; (3) one development carrier per class whose expectation derives from its
  generation (`mini-counter-fresh` pattern, `.ufo/waves/round-34/r34b/w1/CtlMultiset-files/`).

### Rank 6 — Coupled counter / hidden cross-claim prerequisite (r35 F1) → R39-C1/C2 separability. **ADDRESSED ON PAPER; implementation is the exposure.**
- The draft states separability explicitly ("C2 reads SKILL.md, its tools and its own held-out evidence
  only; C1 reads … its own receipts"). r35's defect was not text but a check-time prerequisite (C2 failed
  when C1's SOURCES change was absent). Watch the specific r39 coupling vectors: C1's temporal clauses and
  "no frozen C1 path changed after the freeze" must not accidentally read C2's `tools/round-39/` paths; C2's
  "table bytes equal the freeze" must not read C1 receipts; both counters share `--freeze` semantics.
- Cheapest test: two cross-fixtures — (i) C2-complete state with zero C1 data, (ii) C1-complete state with
  zero C2 data — each counter must be clean or honestly unevaluable, never failed-by-the-other's-absence.

### Rank 7 — Carrier-byte swap vs JSON-only pin compare (r38 `l`; QUALITY 55) → R39-C1 carriers. **PARTIAL.**
- r38's `carriers_unchanged` compared `carriers.json` text only; swapping K1's bytes to text stayed green.
  The draft binds the *envelope's* subject digest to the pin and says "no frozen C1 path changed after the
  freeze", but the predicate does not say the counter re-hashes the carrier **bytes** at the measured
  revision (K5/K6 are new images — the only carriers whose bytes have never been extraction-verified).
- Cheapest test: one-byte flip in a K5/K6 copy → frozen counter must refuse (carrier-mutation control in the
  kill list; it is absent).

### Rank 8 — Stub at the path meets existence-only checks (r38 C2; QUALITY 81) → R39-C1 entry/SOURCES row; R39-C2 manifest. **EXPOSED (kill list has the receipt-space variant only).**
- The C1 kill list does carry "a 'materialise the symlink' receipt with no gap" — the receipt-space analog of
  the r38 stub. But the knowledge entry ("entry cites a SOURCES.md row…") and the SOURCES row itself have no
  stub control: r38 `m` showed a one-line entry body passes `entry_present`. The draft's C2 manifest clause
  ("held-out manifest is first added in a commit descending from the freeze and no later than its envelopes")
  should also bind the manifest's rows to the generator's actual carrier digests, not existence + order.
- Cheapest test: stub-entry (body = one `source:` line) and stub-SOURCES-row fixtures pre-freeze; manifest
  row/digest cross-check red fixture.

### Rank 9 — Post-freeze amendment / controls not in the freeze commit (r38 attempt 1; QUALITY 79/80) → both claims. **ADDRESSED IN TEXT; verify mechanically.**
- The draft invokes QUALITY 79 explicitly ("judged only by the predicate, counter and kill rule present in
  this file's first freeze commit"). QUALITY 80's recurrence risk (M38-2: control generators fixed after the
  freeze) is not addressed in text: the draft does not say the kill-rule control generators/fixtures land
  **in** the freeze commit, nor that receipts replay at the freeze revision.
- Cheapest test: run `tools/round-38/freeze-drift.py` (or its r39 successor) over the claims file, both
  counters, **and** the control-generator paths at the measured revision; require empty commit lists; replay
  one control receipt at the freeze revision.

### Rank 10 — Substring row-id citation / single-spelling zeros (r35 F2 minor; QUALITY 45/56/57) → R39-C1 SOURCES citation. **ADDRESSED (keep the r38 mechanism).**
- r38's `sid_tokens` was boundary-exact and its `i` case (entry cites `S1120` when only `S112` exists) held
  red. The r39 predicate's "cites a `SOURCES.md` row … whose used-by lists that entry" needs the same
  boundary-exact row-id parsing plus the QUALITY-45 rule (the counter accepts only the claim-named row, not
  another valid new row).
- Cheapest test: keep/extend the r38 selftest cases `i` and add `red-cites-other-new-row`.

---

## 3. Synthesis: what the draft already fixes (keep these)

- **Symlink rule stated before data.** This is the correct response to the r38 honest stop (K2's in-tree
  symlink gap met "no extraction gap" under v1) *and* to M38-1 (post-scoring amendment): the rule is now a
  frozen premise, not a post-data repair. It converts the r38 stop cause into a stated, testable condition.
- **Temporal binding of receipts** ("first added in a commit that descends from the freeze") kills r38 class
  `s` (same-commit-freeze).
- **C2 held-out with seed = freeze hash** is the QUALITY-69 fresh-content mechanism (rank 5); the
  pre-freeze-stated rule + post-freeze generation ordering is right.
- **Explicit separability clause** for C1/C2 (rank 6).
These four should be preserved verbatim in the freeze; ranks 1–8 are the gaps to close or consciously accept
before the freeze commit.

## 4. The one bounded move (connector proposal)

**Pre-freeze, add to the C1 kill-rule control suite a scored, committed "fabricated receipt with re-minted
ids" control built by a non-author seat — and have the freeze decide provenance in the predicate text:**
either (a) C1 can only ever stop on that control (honest-stop design, coverage not claimed), or (b) add the
r36-style provenance clause (independent non-author re-run per carrier, package root named) so a green C1
means something. This is one decision, it protects the coverage axis without touching depth, and it is the
cheapest of all the ranked tests because the recipe is §1 above and its cost is seconds. Doing nothing
leaves the round's headline claim in the exact shape that has falsified twice (r36 F1, r38 §3/§5b).

## 5. Risks of this analysis

- The r39 counters do not exist yet (`tools/round-39/` absent at base) — every "exposed" finding is about the
  **draft predicate/kill-list text**, not scored code. The rank-2/3/8 recipes are decision-equivalence
  inferences from r38's matrix on byte-similar binding language [INFERENCE, per `R38CriticClaimsC1.md` §1's
  method]. The rank-1 finding is *demonstrated*, not inferred.
- I did not open `tools/round-37/gen-squashfs.py` source (rank 5a is marked INFERENCE).
- The AVM/diagnostic enumeration in rank 4 rests on two committed r38-w2 envelopes only; recon may surface
  more typenames, which strengthens (not weakens) the lexical-table exposure.
- Held-out discipline kept: no K5/K6 contact, no held-out carrier built, no REA run; the fabrication demo
  used only committed K1-K4 metadata and the lane's own xpin tool on my scratch fixture.

## A. Evidence log (exact commands, outputs, exits)

Fabrication (scratch, since removed; artifacts copied to my artifacts dir):

```
python3 (stdlib)  # build record from carriers.json pin + K1/oracle.tsv (5 rows) + K1/src symlink
# after adding subject{format:raw-binary,architecture:null,local_path}, provider{id,name,version:26.6.4},
# predicate_type:observation, parameters:{}, confidence:observed, authority:controlled-replay,
# limitations:[], locations:[], evidence_links:[], analysis_profile:null, raw_result:{exit_code:0},
# environment:null  →  minted ev_313f5a17dbc03c9d347c9e8f66f12ab6a87f35cbdde857648d46f31d5bd58777

node tools/round-27/xpin-attribute.mjs --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
     --pkg67 <same> fabricated-K1-after.wrapped.json
→ fabricated-K1-after.wrapped.json  ev_313f5a17…  ev_313f5a17…  ev_313f5a17…  both   (exit 0)
node tools/round-27/xpin-attribute.mjs --parse --pkg65 <same> --pkg67 <same> fabricated-K1-after.wrapped.json
→ parseEvidence-6.5.0 accept   parseEvidence-6.7.0 accept   (exit 0)
```

Envelope-structure reads (committed bytes): `rea-k1-orig.json` → 1 diagnostic
`MaliciousSymlinkRemoved` (target `hello.txt`), 5 files, gap-free, `squashfs_v4_be` chunk at 0;
`rea-k1-avm.json` → 1 diagnostic `ExtractCommandFailedReport` (WARNING), 0 files, one `extractor-failure`
gap, `squashfs_v4_be` chunk; `corpus/evidence/round-38/c1/K2/after.json` → one
`unpublished-entry` gap on `firmware.bin_extract/var/lib/run-link`. AVM probe dir:
`.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/` (diagnostics live at
`data.normalized_result.diagnostics[].report.__typename__` — note the trailing double underscore in the raw
key; the assignment text's single-underscore form is the JSON-path shorthand).

Tooling: none installed/upgraded/removed; pacman untouched; sasquatch/sasquatch-v4be/unblob untouched; no
network fetches. VCS: read-only lane git only; no fixture repo was needed for the demo (no counter exists to
score); no lane or fleet mutation.

Artifacts: `.ufo/waves/round-39/w1/artifacts/R39ConnCounterHistory/`
- `fabricated-K1-after.json` (sha256 `37941e32646cc3c92a851716c5bad4ea728c4134d45e32c40f036ab921c85efd`)
  — schema-valid, parseEvidence-accepted, id-verified r39-C1-shaped fabrication for K1.
- `fabricated-K1-before.json` (sha256 `0e260a068061227ad7db08241661e5741d91f2132a93f6459bcdc7d2606a7be2`)
  — paired-arm fabrication in the r38-v2 before shape (missing-extractor-dependency on `sasquatch-v4be`).

Report: `.ufo/waves/round-39/w1/R39ConnCounterHistory.md`
