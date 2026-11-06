# Give recovered targets an approximation contract

[Value-set analysis2004](https://research.cs.wisc.edu/wisa/papers/cc04/BR04.pdf) combines memory regions with numeric offsets and alignment. Summarized objects require weak updates retaining previous possibilities. Yet the prototype can omit unresolved indirect edges, reporting unsafe instructions; library calls act as identity transformers. This is not whole-program coverage.

[Control-flow reconstruction2009](https://www.plai.ifi.lmu.de/publications/vmcai09-cfr.pdf) solves values and edges together. Its best-result claim is relative to the chosen abstraction; widening preserves overapproximation while losing that precision guarantee. The manuscript explicitly differs slightly from proceedings.

[Alternating reconstruction2012](https://dslab.epfl.ch/pubs/alternatingCFR.pdf) uses trace targets to bridge imprecise transfers. Results can contain both missing and extra edges. Relative soundness covers a restricted program obeying those introduced branch restrictions, not the unrestricted executable. Single-trace experiments are not complete behavioral evidence.

Separate representation uncertainty from unmodeled behavior. Smaller target sets need not support stronger conclusions.

Selected prose read; no proof or analyzer tested. No open paper reuse grant established. Commentary only, no code, figures or training.

Optional exercises omitted; originals retained.
