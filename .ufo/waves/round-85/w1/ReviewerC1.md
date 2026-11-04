# ReviewerC1 — R85-C1 attack findings

Full table, receipts and evidence paths: `.ufo/waves/round-85/w1/ReviewerC1/attack.md`.

- BASE re-run agrees with `pre/c1/base-freeze-precheck.json` (F1 CLEAN, F2 CLEAN, refused 0/2). The do-nothing control misses the target.
- Candidate (`ExecPredBind/candidate/tools/round-85/predicate-bind.py`, sha256 a99f8f18…) reaches the target receipt: F1 FLAGGED `PB_NO_PREDICATE_PATH:R85-F1`, F2 FLAGGED `PB_PREDICATE_NEGATED:R85-F2`, round-84 CLEAN, `refused 2`, `accepted 1`, control fires, `mismatches []`, exit 0.
- Drift (D1, decisive): the plan lists `none` as a negation token; the candidate deliberately drops it. With the plan's list the round-84 positive control is FLAGGED (`PB_PREDICATE_NEGATED:R84-C1`, `R84-C2`), so the target is unreachable literally. L1 must adjudicate; the kill rule's "changed predicate" clause is arguably triggered.
- Drift (D2–D5): candidate refuses on ANY negated path (plan: "at least one"), claims a "declared with the plan" decision not in the plan, defines sentences with `;` too, refuses empty claims, and exits 1 on an all-CLEAN run without `--expect` (docstring says 0).
- Forgeries accepted by the candidate: `NOT` uppercase (A03), `doesn't` (A15), `scores nothing` (A16), producer-only pin (A06), corpus `.sh` (A07), `mismatches none` (A11).
