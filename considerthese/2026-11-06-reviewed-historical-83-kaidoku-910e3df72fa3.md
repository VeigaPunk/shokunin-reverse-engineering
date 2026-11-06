# Kaidoku: retention is not future use

McCarthy, Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I (1960):
https://www-formal.stanford.edu/jmc/recursive.pdf

Accessibility from base registers governs reclamation in the described list representation. This supplies historical grounding for distinguishing reachable storage from an application's future intentions. The retained author retypesetting changes notation; it is not exact original typography. Reuse remains uncleared.

Boehm and Weiser, Garbage Collection in an Uncooperative Environment (1988):
https://www.hboehm.info/spe_gc_paper/preprint.pdf

Conservative scanning reduces required representation cooperation but can mistake integers for references and retain unnecessary storage. The described implementation assumes an accessible pointer to each accessible object's beginning; interior-pointer handling requires changes. Stop-and-collect behavior also limits severe real-time uses.

This broadens usable representations rather than proving retained objects will be used again. Neither reading identifies an unknown target's allocator or authorizes disposal. Selected primary sections were read. The later artifact is an author preprint, with Wiley copyright and a qualified author-site posting notice, not general redistribution permission. No source artifacts or execution results included.

Optional exercises omitted; originals retained.
