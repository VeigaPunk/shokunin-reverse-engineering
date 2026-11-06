# Kaidoku: a library symbol can acquire executable storage

The [Solaris11.4 guide](https://docs.oracle.com/en/operating-systems/solaris/oracle-solaris/11.4/linkers-libraries/copy-relocations.html), January2026 edition, explains copy relocations using historical SunOS data interfaces. The linker reserves executable storage; the runtime linker copies library data there and other references bind to that copy.

For static reconstruction, distinguish the data's source, allocated destination and relocation record. An executable symbol does not alone prove the application originally defined that data. Unlike RELR encoding or IFUNC selection, this is a data-placement and interface-size question.

The historical error-array example exposes a compatibility cost: executable allocation fixes an expected size, so growing library data can require relinking. A functional accessor hides that representation; position-independent applications can avoid copy relocations. These are documented alternatives, not measured universal improvements.

This Solaris explanation supports conceptual ELF interpretation, not an untested Linux-loader guarantee. No binary or command executed. Oracle copyright notice read; redistribution permission unestablished. Original commentary only. Optional exercises omitted; originals retained.
