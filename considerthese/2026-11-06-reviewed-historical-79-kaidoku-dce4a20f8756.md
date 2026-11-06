# Kaidoku: local writes and other readers

[Lamport](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/How-to-Make-a-Multiprocessor-Computer-That-Correctly-Executes-Multiprocess-Programs.pdf), September 1979 journal scan: sequential consistency requires a combined ordering that preserves each processor's program order. Individually sequential processors are insufficient.

[Sewell et al., x86-TSO](https://www.cl.cam.ac.uk/~pes20/weakmemory/cacm.pdf), May 2010 author manuscript: buffered writes and reads from a thread's own buffer distinguish local observation from shared memory. This is an assembly-level programmer's model, not a processor blueprint or replacement for sequential reasoning.

Its scope is coherent write-back memory, excluding exceptions, misaligned or mixed-size accesses, non-temporal operations, self-modification and page-table changes. Naming a helper “publish” needs evidence about the reader, not merely the writer's local result. Neither reading establishes a present target's behavior.

Selected extracted prose read; scan columns interleave, so no proof or instruction-example verification claimed. IEEE copyright and no established broad manuscript reuse grant remain. Original commentary and links only; no target execution.

Optional exercises omitted; originals retained.
