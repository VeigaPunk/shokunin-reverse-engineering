# Kaidoku: optimization and directional refinement

[Wang et al., STACK, 2013](https://pdos.csail.mit.edu/papers/stack:sosp13.pdf) examines code discarded when optimizers exploit undefined behavior. An intended safety check can disappear even when it seemed effective without optimization.

[Lopes et al., Alive2, 2021](https://users.cs.utah.edu/~regehr/alive2-pldi21.pdf) validates LLVM transformations through directional refinement: target behaviors must be permitted by the source. Removing nondeterminism may be valid; equality of every behavior is not always required. Bounded loop exploration can miss bugs.

The earlier analysis remains useful for questioning assumptions behind surviving checks. The later method sharpens transformation validation, but does not establish faithful reconstruction of an unknown original program or current tool support. This is a methodological comparison, not a code lineage or universal replacement claim.

Selected retained introductions and rights notices only; no full proof or execution audit. Author copyright for STACK, ACM copyright for Alive2; personal/classroom copying permissions are conditional. Original commentary only; no source code or examples redistributed.

Optional exercises omitted; originals retained.
