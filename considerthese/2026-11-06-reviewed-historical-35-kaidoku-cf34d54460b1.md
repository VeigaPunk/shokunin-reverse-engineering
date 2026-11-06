# Correspondence is not whole-program equivalence

[BinHunt](https://people.eecs.berkeley.edu/~dawnsong/papers/2008%20binhunt_icics08.pdf),2008, combines graph matching with symbolic basic-block comparison. Intermediate-representation simplification can lose precision. Local output agreement and register permutations do not establish whole-function equivalence or surrounding execution context.

[iBinHunt](https://dbgao.github.io/icisc12.pdf),historically identified as2012, crosses function boundaries and narrows candidates using input-field taint tags. Its matching rule can accept blocks through matched predecessors or successors without semantic equivalence. Incomplete coverage, system-call modeling and taint limitations remain. No current ranking.

The older function-bounded question remains useful for a stable routine. Representation helps when inlining or reorganization obstructs that question, but correspondence, local behavior and whole-artifact claims need separate evidence. Missing correspondence can reflect missing observations rather than a semantic change.

Selected prose read, not a proof audit. BinHunt bears Springer copyright. The original institutional2012 and CC BY-NC-ND attribution is historical, not renewed author-copy clearance. Original commentary and links only; no paper passages, figures or code copied. No binary, solver, benchmark or candidate execution.

Optional exercises omitted; originals retained.
