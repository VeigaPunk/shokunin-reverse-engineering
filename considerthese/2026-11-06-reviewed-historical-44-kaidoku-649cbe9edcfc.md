# Kaidoku: specify the dependency policy

[Newsome and Song's expanded TaintCheck report](https://bitblaze.cs.berkeley.edu/papers/taintcheck-full.pdf), May2004 updated July2005, separates input selection, propagation and prohibited uses. Default propagation omits condition flags, missing indirect branch influence; address-based table lookup propagation is optional. Its labels therefore do not explain every dependency.

[Clause and colleagues' Dytan](https://doi.org/10.1145/1273463.1273490),2007, adds configurable control dependence using postdominators and definitions covering unchanged branch values. Its safety argument assumes conservative control-flow and memory-access recovery. The prototype limits memory handling to statically identifiable locations; completeness for arbitrary binaries does not follow.

Name the propagation policy before interpreting a label. A useful inspection clue does not prove absence of influence; more markings alone do not establish greater accuracy. No binary analysis, implementation or proof validation performed.

The retrieved Dytan mirror matches the original recorded hash, not a verified author-copy identity; conditional ACM copying terms apply. No open TaintCheck reuse grant established. Original commentary only, no paper or code redistribution.

Optional exercises omitted; originals retained.
