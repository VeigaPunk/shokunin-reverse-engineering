# Scoped report

Report: .ufo/waves/round-72/w1/CriticClaims.md

Counterexamples: frozen A11 accepts forged clean shim/summary records while an actual child inherits the canary; frozen A10 accepts contradictory `met=false` checker JSON when its binding clauses and exit status satisfy the arm; capsule audit accepts internally consistent wholly forged clean records, including with omitted digest (null, not true). Missing binding clauses fail closed; a canary actually present in raw capsule bytes is rejected.

Frozen predicates remain intact against these component attacks: no full 11/11 pinned-route conjunction or mutation/tamper predicate was falsified. Do not treat this as landing verification. Arithmetic agrees: 9/11 base, one named mutant, 46 genuine records, seven shapes, declared attack fraction 5/16 = 31.25% (31% rounded).

Evidence: c1-wrapper.json, c2-verdict.json, c3-capsule.json, denominators.json; exact replay command and smallest safe corrections in the main report. Driver reads frozen blobs at 34fe7aa70b627d92e2d27dbce308d9f5bebda63d, creates one explicit scratch directory, retains results under this directory, and removes scratch in finally. Final replay exited 0. No production edits, installs, or canonical judgment.
