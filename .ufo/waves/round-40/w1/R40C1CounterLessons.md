# R40C1CounterLessons — counter-failure history → round-40 counter checklist

Verdict: **DONE** — checklist delivered at
`.ufo/waves/round-40/w1/artifacts/R40C1CounterLessons/checklist.md` (24 failure classes with
per-class check + one-line test; clause-by-clause c1/c2 counter reviews; pre-freeze ordering
gate; named minimum red-case sets for both round-40 successors).

Seat: R40C1CounterLessons (leaf; no subagents, no background jobs, no installs, no VCS
mutation). Lane base read at `fa6a8a3f`; round-39 tool bytes read at the lane tip.

## What was read (evidence)

- `corpus/QUALITY.md` in full — admission rows 1–82 plus round-20/round-34 corrections.
- `corpus/lessons/round-35…39-verifier-spotcheck.md` in full (5 files, 723 lines).
- `tools/round-39/c1-counter.py` (969 lines: docstring, all clause helpers :172–352, `measure`
  :380–553, `main`, full selftest case list), `tools/round-39/c2-counter.py` (783 lines:
  `measure` :150–410, full selftest), `tools/round-39/sqfs-triage.py` v1 head (grammar +
  features), `tools/round-39/heldout-gen.py` recipe table (grep).
- `plans/round-40-claims.md` (DRAFT) for both predicates, kill controls and class lists.
- Round-39 mutant reports: `w2/R39W2TriageMutants.md` (18/39 interpreter survivors, named),
  `w2/R39W2C1Mutants.md` (7 survivors + 1 equivalent, named), `w2/R39W2C2Mutants.md`
  (9 genuine missing tests + 5 equivalent, named).
- Round-39 closure §5 (R39-CL1..CL6) and `plans/round-39-claims.md:79` (disclosed fabrication
  limit).

## Findings the round-40 counters must absorb (top of the checklist)

C1 successor (`tools/round-40/` successor of `c1-counter.py`):
1. R39-CL5 is structural: `run_provenance_ok` is a self-declared substring inside the hashed
   envelope, and `evidence_id_ok` re-mints with the producer's own rule — both are satisfiable
   by anyone holding the digest code. The rerun binding from the draft is the only real
   provenance: the counter runs REA itself at scoring time and compares a fixed semantic
   projection (path-suffix+sha publication set, gap multiset, handler set, failed-chunk flags —
   never evidence ids, which are params-keyed and necessarily differ across output directories,
   QUALITY 14/15).
2. `c1-counter.py:313 first_add` takes the **last** `--diff-filter=A` commit (no `--reverse`);
   a receipt added pre-freeze, deleted and re-added post-freeze launders `receipt_fresh`.
   `c2-counter.py:71` has the correct primitive — port it and add the red case.
3. The AVM non-vacuity bindings must be per-carrier `marker AND first-metadata-length-decodes-LE`
   with the two decodes differing — otherwise the marker-only `--endian avm` body satisfies the
   binding and kill control 4 is vacuous (the writer must emit a first metadata length ≥ 256).
4. The gap rule must be a frozen artifact read at the freeze revision (draft: "fixed in the
   freeze from development recon"), listed in FROZEN_PATHS, failing closed — not hardcoded kinds
   as in `gaps_ok` :285.
5. c1 has no `met_target_consistent` recomputation (c2 does): a mutant flipping `met_target`
   alone would pass; copy c2's check + cases (QUALITY 72).
6. Six of the seven r39 C1 mutant survivors (`gaps-set`, `gaps-kind`, `oracle-nosha`,
   `prov-isabs`, `xz-ver`, `sid-bounds`) are missing tests, each with a named fixture in the
   checklist; `ev-noprefix` is equivalent (xpin always mints `ev_`).

C2 successor (v2 of `sqfs-triage.py` + successor of `c2-counter.py`):
1. `envelopes_valid` currently **requires** `operation == 'extract_firmware'` for every
   envelope — the v2 out-of-domain class violates that by design; split into digest-required +
   operation-recorded, with the out-of-domain class expecting `unclassified` (R39-CL1).
2. Score (label, action) pairs; enforce unique labels per row (duplicate label → malformed
   table, exit 2) so a label is a row decision (R39-CL3); report `distinct_decisions`.
3. Add `v2_marker_unique` (findall, QUALITY 77 — first-marker-wins is shadowable) and
   `v1_block_unchanged` (draft keeps block 18 byte-identical).
4. Drop the `expected_label`-falls-back-to-class-name default: a manifest row without an
   explicit expected label must be malformed, not silently graded.
5. Control inputs + generators land in the freeze commit and replay there (R39-CL4, QUALITY 80);
   the `corruption_bad_minor` generator erratum is fixed before the freeze or it is frozen bytes.
6. The 18 surviving interpreter mutants split into held-out-killable (use replicate variation of
   non-decision features: typename site, `-be` command position, sasquatch basename forms,
   non-squashfs handlers, P=0/2 vs >0) and selftest-only; both detectors report per mutant on
   `(exit, verdict)` triples.

Cross-cutting (both): exit code + argv + pins in every score receipt (R39-CL6, QUALITY 73/39);
history-based frozen-drift with restore-does-not-unblock (QUALITY 79); controls scored before
data (QUALITY 48/50); SKILL registry rows with outer-CLI selftests (R38-CL2, QUALITY 61); token
boundaries and section-scoped placement checks (QUALITY 54/77); negative-existence claims via
`absence-sweep.py` rooting (QUALITY 82); carrier screening output committed with the freeze
(QUALITY 43); vendor-member provenance chains in the carrier spec (R37-CL2).

## Limits

- Static review only: no counter or gate was executed this wave (frozen-carrier discipline and
  the wave plan reserve execution for the counter-authoring seats); every code citation is from
  reading committed bytes at the current tip, not from a run.
- The checklist is advisory input to the freeze; the L1 integrates it. Where the draft claims
  already name a fix (rerun binding, action scoring), the checklist adds the missing selftest
  red cases and the vacuity traps, not a new design.
- No installs or updates (nothing needed); scratch `/fast/scratch/hyaku/kaidoku-r40/R40C1CounterLessons`
  removed on finish.
