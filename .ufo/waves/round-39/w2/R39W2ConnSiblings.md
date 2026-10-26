# Seat R39W2ConnSiblings — sibling pattern scan + C1-limit closure analysis

**Verdict: CONFIRMED** — kaidoku's disclosed C1 limit (a fabricated after-receipt whose
evidence id is re-minted under the public 6.5.0 rule satisfies every receipt-only clause)
is real and stands as disclosed; no single sibling-lane gate closes it, but one composed
mechanism — a **counter-drawn live re-query leg** — closes its practical channel, and
every ingredient already exists in sibling lanes. Details, citations and the
recommendation below.

Scope: read-only scan of `/home/vgpnk/Projects/shokunin/*-shokunin` (22 lanes) for three
patterns; no lane files mutated; no tools installed (nothing new was needed — this scan
used only `read`/`grep`/`bash` reads; tool/version/channel record: none).

---

## 1. Pattern A — held-out set seeded by a freeze commit hash

**Only kaidoku uses it.** `tools/round-39/heldout-gen.py` takes `--seed <FREEZE>`; the
frozen claims (`plans/round-39-claims.md`, freeze `8fcda41c`) bind "its seed is the freeze
commit hash" and the data procedure is
`heldout-gen.py --seed <FREEZE> --out corpus/evidence/round-39/c2/heldout --run`.

Sibling alternatives (all cited by path):

- **tameshi-shokunin** — *sealed authored* held-out sets, no seed derivation: the set is
  "written after the freeze by seats who did not write the tool, and the counter validates
  each copy" (`.ufo/reports/round-32/tameshi.md:35-37`); 14 sealed copies at
  `.ufo/evidence/round-33/heldout/` (`.ufo/reports/round-34/tameshi.md:76-77`); per-copy
  authoring receipts `.ufo/evidence/round-34/dev/authoring-receipts.json`; rule entry
  `corpus/knowledge/witness-equivalence-rule.md`.
- **chousa-shokunin / mado-shokunin** — counters take integer seeds
  (`corpus/evidence/round39/c1-count.py --seed N`, `.ufo/reports/round-39/chousa.md:79-80`;
  `mado count-v5.py --seed 28c1a8c0ffee0001`, `.ufo/reports/round-28/mado.md:81-83`).
  Seeds are run-time parameters, not commit-hash-derived.
- **kumitate-shokunin** — replayable HMAC-SHA256 stream, caller-chosen hex seed
  (`--seed 2676cbe767adc1820fd316e02a7b9020` over a frozen shape TSV;
  `.ufo/waves/round-44/probe/p44d-count.mjs:49,134`; usage
  `.ufo/waves/round-44/falsify/CtlPostDataA.md:14`). Replayable, not freeze-derived.
- **kengaku-shokunin** — round-39 falsification varied `PYTHONHASHSEED` to prove no printed
  line depends on interpreter hash seed (`.ufo/waves/round-39/falsify/F39C1Rerun.md:27,50`)
  — a determinism robustness check, not a data-set seeding scheme.

Coverage note: freeze-hash seeding is a kaidoku innovation; siblings either author sets
socially (tameshi) or parameterize runs (chousa/mado/kumitate). None would catch a
pre-freeze leak of kaidoku's C2 held-out set, because none of them reproduce kaidoku's
"data cannot exist before the freeze" property — that property is exactly what the
freeze-derived seed buys.

## 2. Pattern B — executable decision table read from SKILL.md

Two instances:

- **kaidoku-shokunin** — `tools/round-39/sqfs-triage.py` reads only the SKILL.md
  craft-section triage table after `<!-- sqfs-triage-table v1 -->` (frozen predicate
  P39-C2; table bytes must be byte-identical at freeze and measured revision).
- **kotoba-shokunin** — `verifiers/check_gate_registry.py:5,21,354-356` reads the
  `## Gate registry` table out of SKILL.md at a revision (`t.read("SKILL.md")`), parses
  header cells lower-cased, and grades gate conformance from it. Fleet-sanctioned home:
  `PROTOCOL.md:398` makes SKILL.md the lane registry home and closure grades no gate
  conformant without a row there (L0 question, kotoba round-73, `.ufo/l0-questions.md:174`).

Contrast: mado's round-27/28 frozen data rule (`tools/mado-wsrules.py`) is an *independent
reimplementation* of a pinned upstream behavior (Hyprland workspacerules JSON from config
bytes), not a table read from SKILL.md (`.ufo/reports/round-27/mado.md:69-73`). It is
relevant to pattern C instead, as a repro-network technique.

Depth note: kaidoku's version is stricter than kotoba's — the triage table's *labels* are
scored against a held-out oracle, while kotoba's registry rows are structural conformance.
Neither lane currently defends the table itself against a post-freeze semantic rewrite
that keeps bytes identical; both freeze bytes instead. That is the correct call, since a
byte-identical rewrite is a no-op.

## 3. Pattern C — the re-minted-receipt provenance limit (fabricated receipts)

Kaidoku's disclosure, restated: CTL-C1-3 built six fabricated after-receipts with evidence
ids re-minted by the lane's own public tool `tools/round-27/xpin-attribute.mjs` under the
rea-agents 6.5.0 rule and the counter scored them 6/6, exit 0
(`.ufo/waves/round-39/w1/R39C1Controls.md:3,25,67` — "no receipt-only refusal exists").
`run_provenance_ok` in `tools/round-39/c1-counter.py` (docstring lines 4-70) only requires
`parameters.output_directory` to *name* `/kaidoku-r39/`; since the minting rule is public,
anyone can fabricate payload + id without running REA.

Where siblings stand on exactly this class:

| Lane / gate | Path | Closes which sub-channel? |
|---|---|---|
| kama r43 hexrun-census | `.ufo/reports/round-43/kama.md:57` | **Authorship, operationally** — names the same limit ("the evidence files are committed bytes the counter cannot tie to GitHub") and closes it out-of-band: "the closure re-queries a sample". |
| tameshi r32-34 sealed set | `corpus/knowledge/witness-equivalence-rule.md`, `.ufo/evidence/round-34/dev/authoring-receipts.json` | **Authorship, socially** — non-author seats author after freeze; per-copy authoring receipts committed; counter validates each copy. Round-32 closure recheck: "RerunV2 reproduction evidence-verified (0/22 differ, two seeds)" (MANIFEST.json rounds[32] rechecks). |
| mori r39 C7 | `.ufo/waves/round-39/count-c7.py` (checks `live_rows_v2`, `drift_kill_v2`) | **Pre-computation + fabrication** — the expected post-state is *drawn at run time* (seeded) and printed in the receipt, "so a probe that hard-codes the expected flip string cannot know it in advance"; and every named id "has a committed source copy at <rev>" (kills self-consistent clones citing nonexistent sources). A fabricated kaidoku receipt with re-minted id over real carrier bytes would still pass mori-style checks — mori closes the *content* channel, not the *run* channel. |
| tsukuroi r38 q82 counter | `tools/score-storage-arm-r38-q82.py` | **Cached/rewritten answers** — the counter runs the census itself inside `unshare -rm` over a fresh `os.urandom` tree bind-mounted over the production path, "so neither the path nor a cached answer distinguishes a view from production use". Directly maps to a receipt copied from an earlier round and re-minted. |
| chousa r35-36 witness | `tools/mechanism-witness.py` | **No-run fabrication** — out-of-band execution witness: gate runs under `bash -x` with a private PS4 marker; fixture per-seed random temp prefix/id shape "so a fingerprint-specific shortcut has nothing stable to key on". Stated limit: an engine that knows it is traced can still defeat it. |
| chousa r38 C2 | `.ufo/reports/round-38/chousa.md:33` | **Explicitly NOT this limit** — RECEIPT_BINDING_MATCH binds receipts to verifier bytes, and the erratum narrows it: "integrity + self-consistency, NOT authorship; the verifier-mutant pass-through class named with `verifier_sha256` carried". Useful negative evidence: byte-binding receipts does not close re-mint fabrication. |

## 4. Direct answer: would any sibling gate close kaidoku's disclosed C1 limit?

**No single one.** The limit has three sub-channels, and the siblings partition them:

1. *Pre-computation* (fabricate payload+id before any run): closed only by counter-drawn
   entropy — mori's drawn state and tsukuroi's counter-side randomization both embody it,
   but neither is wired to receipt ids.
2. *No-run* (receipt claims a run that never happened): chousa's trace witness closes it
   for gate runs, with an admitted anti-instrumentation escape hatch.
3. *Authorship* (who produced the bytes): kama's closure re-query and tameshi's
   non-author-authoring + authoring receipts close it operationally/socially — and this is
   exactly the closure kaidoku's own claims already invoke ("Provenance therefore rests on
   independent wave-2 re-runs that compare the semantic payload of each committed
   receipt", `plans/round-39-claims.md` R39-C1 "Disclosed limit").

Kaidoku's wave-2 repro seats (R39W2ReproK1/K2/K4/K6, R39W2HeldRepro*) are the tameshi/kama
pattern executing now. That is the fleet-standard closure and it is the right one — but it
is social; a counter over committed bytes alone stays blind, as chousa's r38 erratum
proves.

## 5. Recommended transferable mechanism (one)

**A counter-drawn live re-query leg, fused from tsukuroi q82 + mori c7 + chousa
mechanism-witness, and already named in kaidoku's own wave-1 controls report.**

Concretely, for a future round (r40+; the r39 counters are frozen and this seat changes
nothing frozen): add to the coverage counter a live leg —

- the counter draws k ≥ 2 carrier indices from a committed run seed (mori: drawn state is
  printed into the receipt, so the run stays re-derivable);
- creates the REA output directory itself via `mkdtemp` under `/kaidoku-r39/<round>/`
  (tsukuroi: counter-side randomization, so neither path nor cached answer is
  distinguishable or pre-computable);
- runs REA 6.5.0 itself on the frozen carrier bytes from a clean clone, with the same
  arm conventions as `tools/round-39/heldout-gen.py:390-399` (`before` arm strips
  `$HOME/.local/bin` from PATH; `REA_UNBLOB_COMMAND` absolute);
- requires the committed receipt's *semantic projection* (handler, chunks, published
  oracle files + sha256, gap multiset, subject pin) to equal the live envelope for the
  drawn carriers — never comparing evidence ids or `raw_result` across runs
  (kaidoku's own wave-1 lesson, `w1/R39C1Controls.md:101-104`).

Why this closes the disclosed limit: a fabricated receipt would have to embed the
counter's unpredictable outdir into its hashed projection, i.e. be fabricated *inside* the
counter run — at which point it is a run. The minting rule stays public; it stops
mattering. Kaidoku's own wave-1 controls report already recommended exactly this shape:
"the measurement happens in the counter … counter-chosen outdir, or an independently
executed witness run — otherwise CTL-C1-3 stays green" (`w1/R39C1Controls.md:108-111`).

Pointers for the implementing lane:
- counter-side randomization + cached-answer defense: `tsukuroi-shokunin/tools/score-storage-arm-r38-q82.py` (predicate and exit map in its docstring);
- drawn-at-runtime state printed in receipt: `mori-shokunin/.ufo/waves/round-39/count-c7.py` (`drift_kill_v2`, DRAWN_STATES);
- out-of-band execution witness (optional belt-and-suspenders for the non-drawn carriers): `chousa-shokunin/tools/mechanism-witness.py`;
- non-author authorship separation retained as the operational layer: `tameshi-shokunin/corpus/knowledge/witness-equivalence-rule.md` + `.ufo/evidence/round-34/dev/authoring-receipts.json`;
- in-lane precedent that counters may execute tools under test: kaidoku round-34 mini-counter ran a control-reader tool (`.ufo/reports/round-34/kaidoku.md:90-92`).

Risks, stated: (a) the leg makes the counter non-hermetic (needs unblob 26.6.4 and
sasquatch-v4be on the child PATH) — mitigate with the existing arm-env convention and a
could-not-evaluate exit 2 that never scores as met (kengaku's verify/audit split,
`kengaku-shokunin/.ufo/waves/round-39/falsify/F39C1Rerun.md`, is the model for separating
the deciding run from the audit); (b) run cost — drawing k=2 of 6 keeps it bounded while
making fabrication of all six require six independent guesses; (c) REA refuses a
pre-existing outdir, so the counter must use a fresh outdir per drawn carrier (already the
REA contract); (d) a fabricator who also controls the counter run is outside any
counter's threat model — that residual is unchanged and is the social layer's job.

## 6. Evidence quality and limits

- All citations are live reads against the current worktrees, 2026-10-26; lane tips move,
  but every cited path is committed corpus/report material.
- [INFERENCE] Round numbers differ across lanes (kaidoku r39 ↔ chousa r39 ↔ tsukuroi r40);
  "sibling" here means fleet-lane, not same-round. The mechanisms compared are the
  relevant ones regardless of round.
- [INFERENCE] No sibling was found to bind receipt evidence-ids to counter-drawn entropy;
  the recommendation is a synthesis, grounded in the four cited implementations, not an
  observed whole.
- Nothing in this scan re-runs or re-scores kaidoku's C1/C2 counters; the falsification
  of the landing is the other wave-2 seats' job. This seat confirms the disclosed limit's
  diagnosis and supplies the closing mechanism.
