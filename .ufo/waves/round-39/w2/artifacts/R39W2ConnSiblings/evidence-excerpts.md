# Evidence excerpts — seat R39W2ConnSiblings (all read-only, 2026-10-26)

## Pattern A — freeze-hash-seeded held-out
- kaidoku (only instance): tools/round-39/heldout-gen.py `--seed <FREEZE>`;
  plans/round-39-claims.md P39-C2: "its seed is the freeze commit hash".
- tameshi alternative: .ufo/reports/round-32/tameshi.md:35-37 "The set is written after
  the freeze by seats who did not write the tool, and the counter validates each copy."
- chousa/mado: integer run seeds (.ufo/reports/round-39/chousa.md:79-80;
  .ufo/reports/round-28/mado.md:81-83).
- kumitate: replayable HMAC stream (.ufo/waves/round-44/probe/p44d-count.mjs:49,134).
- kengaku: PYTHONHASHSEED robustness only
  (.ufo/waves/round-39/falsify/F39C1Rerun.md:27,50).

## Pattern B — executable decision table read from SKILL.md
- kaidoku: tools/round-39/sqfs-triage.py (frozen; table after `<!-- sqfs-triage-table v1 -->`).
- kotoba: verifiers/check_gate_registry.py:5,21,354-356 — reads `## Gate registry` in
  SKILL.md at rev; PROTOCOL.md:398 makes SKILL.md the registry home (.ufo/l0-questions.md:174).
- mado contrast: tools/mado-wsrules.py is an independent reimplementation of pinned
  upstream behavior, not a SKILL.md table read (.ufo/reports/round-27/mado.md:69-73).

## Pattern C — re-minted-receipt provenance limit
- kaidoku disclosure: .ufo/waves/round-39/w1/R39C1Controls.md:3,25,67 —
  CTL-C1-3 "ids re-minted with tools/round-27/xpin-attribute.mjs (6.5.0 rule)"
  → "exit 0, 6/6 as drafted — no receipt-only refusal exists"; fix shape at :108-111
  ("counter-chosen outdir, or an independently executed witness run").
- kaidoku counter rule: tools/round-39/c1-counter.py docstring lines 4-70 —
  run_provenance_ok only requires output_directory to name /kaidoku-r39/;
  evidence_id_ok recomputes under the public 6.5.0 rule.
- kama r43: .ufo/reports/round-43/kama.md:57 — "the evidence files are committed bytes
  the counter cannot tie to GitHub (the closure re-queries a sample)".
- tameshi: corpus/knowledge/witness-equivalence-rule.md;
  .ufo/evidence/round-34/dev/authoring-receipts.json (per-copy kill/accept witness).
- mori r39: .ufo/waves/round-39/count-c7.py — drawn post-state printed in receipt;
  every named id needs a committed source copy.
- tsukuroi r38: tools/score-storage-arm-r38-q82.py — counter-side os.urandom tree,
  unshare -rm, cached-answer defense.
- chousa: tools/mechanism-witness.py — bash -x PS4 trace witness, per-seed random
  fixtures; .ufo/reports/round-38/chousa.md:33 — RECEIPT_BINDING_MATCH is "integrity +
  self-consistency, NOT authorship".

## Recommendation grounding
- counter-drawn live re-query = tsukuroi q82 randomization + mori c7 drawn state +
  chousa witness; named in kaidoku w1/R39C1Controls.md:108-111; in-lane counter-executes-
  tool precedent .ufo/reports/round-34/kaidoku.md:90-92.

Commands used (read-only): git show of the frozen claims; grep over fleet lanes for
`heldout-gen|held-out set`, `re-?mint|remint`, `--seed`, `SKILL\.md`, `freeze` in
*/tools/*.py; python3 json.loads on tameshi authoring-receipts.json and kasegi claims.json.
No installs; no writes outside this report and this artifact.
