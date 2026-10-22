# R26-C2 before-measurement, seat KaidokuR26.C2BeforeManual (independent, no lane counter)

REV = base a0639d8e61e486e2a716ff94cddd89a73200a02c throughout. Measured with plain
`git show`/`grep`/`cat-file` plus SCORECARD `## Measurement recipes` recipe A, run
verbatim in a sandbox clone. The lane instrument tools/round-26/c2-calibration.py was
never read or run. UTC of the verification block: 2026-10-22T12:16:54Z.

## Method and evidence chain

- Sandbox clone: `git clone -q <lane> <seat>/clone`; clone HEAD c27f445e (freeze commit);
  `git cat-file -e a0639d8e…` exit 0. All measurement on Git objects at base; lane untouched.
- Blobs extracted at base (exit 0 each): SCORECARD.md, SHONEN.md, SKILL.md, README.md,
  evidence/round-1-2026-10-15/result.json. Hashes in the manifest below.
- Command A: recipe text copied byte-for-byte into `<seat>/cmdA.py`, run as
  `python3 -I -B ../cmdA.py <rev>` with cwd = the sandbox clone (the recipe's
  "run from this lane repo" satisfied by the clone, per assignment).
- No tools installed or upgraded (none needed).

## Command A runs (exit 0 in all three; excerpts verbatim)

- At base a0639d8e…: `{"citation_resolved_rules": 17, … "knowledge_files": 108, "mapped": 108, "missing": [], "dangling": [], … "rule_blocks": 17}`.
- At 638fb211: `{"citation_resolved_rules": 9, … "knowledge_files": 72, "mapped": 72, … "rule_blocks": 9}`.
- At 3395b6d: `{"citation_resolved_rules": 9, … "knowledge_files": 78, "mapped": 78, … "rule_blocks": 9}`.
- Token resolution: `git cat-file -t` → `638fb211` commit, `3395b6d` commit, `75af886a` commit (all exit 0).

## Per-item results (all six rules evaluated literally from claims.json R26-C2.rules)

- **K1 — MISMATCH.** Depth row observable cell, first N/M token = `9/9` (observation:
  cell text begins `9/9 queue-drain rule blocks have resolvable file/range citations at
  `638fb211`; recount 17/17 at `08c7a729…``). Command A at base gives rule_blocks = 17
  and citation_resolved_rules = 17, not 9. Inference per rule K1: mismatch.
- **K2 — MISMATCH.** Craft span at base: heading line `## Queue-drain craft (rounds 5-12,
  distilled in round 13)` at SKILL.md line 81 (grep, exit 0); next `## ` line is 319;
  lines 315–318 are empty and line 314 is the last non-blank (awk dump
  `314:[  `.ufo/waves/arc3-loop1-round12/claims/c2/EX-16.md`).]`, `315:[]`…`318:[]`).
  So the required string is `SKILL.md:81-314`; the evidence cell holds
  `SKILL.md:77-191` and `SKILL.md:81-318` only. Inference: mismatch.
- **K3 — PASS.** First 7-40 hex after the word `measured` in the depth evidence cell =
  `638fb211` (8 hex); resolves as a commit; command A at 638fb211 gives
  rule_blocks = 9 == citation_resolved_rules = 9 == the K1 N (9). Inference: pass.
- **K4 — MISMATCH.** Coverage row first N/M token = `108/108`; command A at base gives
  mapped = 108 == knowledge_files = 108, so the at-REV leg holds. The `measured` token in
  the coverage evidence cell is `3395b6d` (7 hex); it resolves, but command A there gives
  78/78, not the same 108/108. Inference under the literal reading of "gives the same
  N/M under command A": mismatch (see ambiguity A1).
- **K5 — MISMATCH.** Calibration evidence cell `measured` token = `75af886a`;
  result.json at base line 4: `"measured_revision": "c265db9bd3c0883fbaf4487f839559c85a736826"`.
  `75af886a` is not a prefix of that string (it is itself a resolvable commit, exit 0,
  but the rule asks only for the prefix relation). Inference: mismatch.
- **K6 — MISMATCH.** SHONEN.md box line `- [~] No cross-domain bleed (PROVINCE.md still
  accurate)`; the next physical line contains `province-version alignment is contested
  by the 6.5.0/207/v42 observations` (grep -c contested = 1, on that line). Pointer leg
  holds: `PROVINCE.md:95-116` fits; PROVINCE.md at base has 303 lines (`git show … |
  wc -l` = 303); the bare `:114-116` and `88-116` fragments do not match the
  `PROVINCE.md:A-B` pattern, so only 95-116 is in scope. Inference: mismatch on the
  `contested` word.

**Total: 5 mismatches (K1, K2, K4, K5, K6), 1 pass (K3), items 6.** Observation: this
equals claims.json `before_expected` ("5 of 6 by reading at base (K3 expected to hold…)").

## Ambiguity flags

- **A1 (K4, material):** "gives the same N/M under command A" has an unclear antecedent —
  the same N/M as the observable cell's first token (108/108), or internally consistent
  at the measured revision (78 == 78). The literal first reading fails at base; the
  second would pass. I used the literal reading; the instrument author should pin the
  antecedent because a mutation test can flip K4 between readings.
- **A2 (K1/K2, disclosed by design, not defective):** both items pin the stale first
  token `9/9` and the span `SKILL.md:81-318` even though the same row discloses the
  17/17 recount and the span "at `08c7a729`". The items measure the stale wording, which
  is the repair target ("go from the before count to 0"), but the rule text nowhere says
  "first token supersedes any later recount in the same cell" — worth one sentence in
  the instrument to prevent a false red/green debate.
- **A3 (K2/K3 boundary, minor):** command A splits the craft on `## Queue-drain craft `
  (trailing space) while K2 defines H by `## Queue-drain craft` (no trailing space). At
  base both hit the same heading; they diverge only if the heading ever loses its
  trailing text. No effect on this measurement.
- **A4 (K6, minor):** "every PROVINCE.md:A-B or PROVINCE.md:A pointer in it" — the line
  also carries relative fragments (`:114-116`, `88-116`) that the literal pattern
  excludes. If the intent was to check those too, the pattern needs widening; at base
  both fragments (114-116, 88-116) are also inside 303 lines, so no verdict change.

## Residual risk and verification gaps

- I did not run the lane counter; per assignment this is the independent before value.
  Divergence risk: only if the lane counter reads the cells with a different "first N/M"
  or "first hex after measured" extractor than the literal one used here (A1/A2).
- Command A was executed in a sandbox clone, not the lane worktree; the recipe intends
  Git objects, so this is faithful, but it is a stated deviation from "run from this
  lane repo".
- 75af886a, 638fb211, 3395b6d resolve in the clone's object store (fetched from the
  lane), exit 0; no independent confirmation that these are the canonical upstream
  objects beyond the clone provenance (unknown, accepted).
- No REA runs were made: R26-C2 involves no carrier and no envelope; correct per claims.

## Manifest (scratch root /fast/scratch/hyaku/kaidoku-r26/seats/KaidokuR26.C2BeforeManual)

- cmdA.py — recipe A verbatim — sha256 236dde1da2d78b5ee2f4827fb884901857385fe1f40bbb09bbb4b4ab4f6e9b01
- src/SCORECARD.md (git show base) — sha256 cfe8b5257c90b14b3f7cbe1349d6117a78494632096ab1fa2594e189038d977a
- src/SHONEN.md (git show base) — sha256 120cd2b3bb5f9e0c2bcc943bf8cf74c6c35cf887e85fe2caa660901d36ff2ddb
- src/SKILL.md (git show base) — sha256 cf047307dbab77369ffe31de3f7f4eeab797293c085253eba28d6978a735ad42
- src/README.md (git show base) — sha256 63ffe86cc6e62ae770bb3e7d52890f8a098527b44066ce11a03a63fdd6a2d06e
- src/evidence_round-1-2026-10-15_result.json (git show base) — sha256 0a03434f69a07197a426837f13cd0cca1793c66856a64c73b367695ae45e1342
- clone/ — sandbox clone of the lane (read-only use; no writes, no jj, no git mutations)

Verdict: at base, R26-C2 stands at 5 of 6 items mismatched (K3 holds); the C2 repair
wave must clear exactly K1, K2, K4, K5, K6 to reach the target of 0 mismatches.
