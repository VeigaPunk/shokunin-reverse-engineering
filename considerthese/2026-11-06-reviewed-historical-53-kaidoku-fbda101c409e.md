# Kaidoku: recognizing a state does not reset it

[Angluin](https://homepages.math.uic.edu/~lreyzin/papers/angluin87.pdf),1987, organizes membership answers into observation tables. Closed, consistent tables support conjectures; exact learning also requires equivalence confirmation or counterexamples from a teacher. Agreeable observations alone do not provide that access.

[Rivest and Schapire](https://people.csail.mit.edu/rivest/pubs/RS89.pdf),1989, replace reset access with homing sequences whose observed outputs identify the ending state. They do not force every starting state to the same endpoint. Separate learners correspond to homing outputs; inconsistent continuations can refine a presumed sequence.

The general treatment still assumes counterexamples and strong connectivity. Without the latter, observation can become confined to an inescapable component. These assumptions limit application to arbitrary stateful software; neither paper proves a recovered model complete merely because inspected interactions agree.

Record observation setup separately from state labels. Recognition does not establish reversibility. No target, solver or inference procedure executed.

Academic Press reserves reproduction rights; ACM permits conditional copying, with republication requiring permission. Original commentary only.

Optional exercises omitted; originals retained.
