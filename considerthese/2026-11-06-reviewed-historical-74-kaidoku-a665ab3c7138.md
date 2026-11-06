# Kaidoku: exceptional exits retain distinct effects

[Goodenough](https://web.eecs.umich.edu/~weimerw/2006-615/reading/goodenough-exceptions.pdf), December 1975 journal edition, distinguishes exceptions requiring termination, requiring resumption, or permitting handler choice. Termination does not inherently undo effects. The printed ACM notice permits attributed nonprofit republication conditionally, not unrestricted reuse. This is not the earlier conference edition.

[Itanium exception ABI](https://github.com/itanium-cxx-abi/cxx-abi/blob/336b01ebc025a15bbf5796b5b9c037412b5210fe/abi-eh.html), pinned document labeled revision 1.22, separates handler search from cleanup. A cleanup-only landing pad can resume unwinding without catching. This narrows language-design choices to a particular interoperability contract, not universal exception behavior. Snapshot date unrefreshed; no artifact-specific reuse grant established.

Read selected exception constraints, first-page rights, two-phase handling and cleanup-only discussion. The older distinction remains useful when explaining what stopping means; ABI mechanisms do not prove an inspected binary follows that contract. No binary, source algorithm, proof or reconstruction executed. Original commentary only; historical novelty screening not renewed.

Optional exercises omitted; originals retained.
