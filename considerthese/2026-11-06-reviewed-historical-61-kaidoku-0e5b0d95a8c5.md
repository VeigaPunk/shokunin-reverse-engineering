# Kaidoku: declarations do not establish connectivity

[Sagiv, Reps and Wilhelm](https://research.cs.wisc.edu/wpis/papers/popl96.pdf),1996 prepublication manuscript: shape graphs approximate possible heap arrangements. Nodes are named by sets of variables rather than allocation sites; summary nodes combine locations. Sharing information and materialization improve precision. Nonpointer behavior is abstracted, so even the concrete semantics intentionally omits information.

Their [2002 manuscript](https://research.cs.wisc.edu/wpis/papers/toplas02.pdf) generalizes analysis through selectable predicates and three-valued structures. Unknown values preserve incomplete information; focusing refines alternatives rather than discovering one certain arrangement. Predicate choice controls precision. The presented analysis addresses one procedure.

The earlier construction remains a concrete account of representation choices; the later framework makes those choices configurable. Neither is evidence that a recovered binary declaration establishes actual object connectivity. No analyzer or reconstruction was executed, and no proof was independently validated.

Selected rendered primary pages read. The later copy has placeholder publication fields and conditional ACM copying terms; no general republication grant established for either manuscript. Original commentary and links only.

Optional exercises omitted; originals retained.
