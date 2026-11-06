# Kaidoku: preserve rounding boundaries

[Goldberg](https://web.cs.hacettepe.edu.tr/~bil220/p5-goldberg.pdf), March1991: the retained journal article explains why evaluation precision, parentheses and algebraic rewrites affect floating-point semantics. Familiar real-number identities are insufficient justification for a recovered computation’s simplification.

[Monniaux](https://arxiv.org/pdf/cs/0701192v5): the retained copy bears a May2008 version identifier but a November2024 title-page date. Selected sections explain how historical x87 register spills can change rounding, and how rounding through an intermediate format can differ from direct rounding. The date discrepancy is unresolved; journal byte identity and current compiler behavior are not claimed.

This develops implementation-sensitive verification rather than replacing numerical error analysis. For reconstruction, distinguish preserving intermediate values from preserving a particular output decision. A more accurate rewrite can still misdescribe the artifact. Keep unresolved conversion boundaries explicit; no binary execution or numerical experiment occurred.

Goldberg’s printed ACM notice permits copying conditionally, not unrestricted republication. The original record reports restricted arXiv distribution rights; no general adaptation grant is claimed. Original commentary and links only.

Optional exercises omitted; originals retained.
