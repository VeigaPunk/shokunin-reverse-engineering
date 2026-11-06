# Kaidoku: termination needs more than local decrease

[Podelski–Rybalchenko](https://swt.informatik.uni-freiburg.de/berit/papers/transition-invariants.pdf),2004: a finite well-founded cover must contain whole computation segments, not only individual transitions. A locally decreasing quantity does not automatically cover later resets.

[Kroening and colleagues](https://www.kroening.com/papers/cav2010-2.pdf),2010: progressive unwinding and transitivity checks construct compositional transition invariants. The algorithm is not complete for terminating programs, even finite-state ones. Its implementation analyzes ANSI-C, not stripped binaries.

The refinement changes how termination arguments are obtained; it does not remove their semantic premises. The earlier whole-segment obligation remains an effective question for reviewing a recovered loop. Identify entry assumptions, every returning route, arithmetic width and signedness, and helpers whose completion is unknown. An unsuccessful argument is not itself demonstrated nontermination. Eventual return also does not promise acceptable latency or successful work. No proof, analyzer run or target execution occurred.

Retained copies bear IEEE and Springer notices; no open republication grant established. Selected text and a rendered definition page were inspected, not every proof. Original commentary and links only.

Optional exercises omitted; originals retained.
