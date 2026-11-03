# Source reading notes,2026-11-03

Opened official Xinuos gABI4.3 DRAFT program-loading and ELF-header chapters directly. No complete third-party page is retained. URLs: https://gabi.xinuos.com/elf/07-pheader.html and https://gabi.xinuos.com/elf/02-eheader.html.

Program loading7.1 defines p_offset as file origin and p_vaddr as memory origin, separate fields; p_filesz may be smaller than p_memsz. Section7.2 PT_LOAD assigns initialized bytes first, then zero fill, and forbids filesz greater than memsz. LOAD entries ordered by ascending vaddr. Alignment0/1 needs no alignment; otherwise power-of-two and vaddr/offset congruence. Page-size alignment is additional platform-dependent information, not established by p_align alone. Section7.3 separates link-time addresses from loaded addresses: do not infer an actual process mapping, load bias or ASLR from this reader. Section7.5 explains section contents are transparent to program headers and the usual NOBITS contribution; the profile will not use section names to decide file-backing.

Header2.1 defines offsets, record sizes/counts and EXEC/DYN types. Header2.2 establishes class/data/version interpretation. Reader profile intentionally supports only ELF64LE version1 EXEC/DYN. A no-section-table fixture is useful: section lookup cannot be the authority for segment query results. A poisoned unused section-header pointer is not followed and does not make this a full ELF validator.

Own conservative choices, not source claims: refuse extended program numbering; bound size/count/query; retain ambiguous overlapping candidate provenance without loader precedence; do not traverse section/dynamic metadata or certify the artifact loadable. An equal byte sequence at two distinct file offsets is still two candidate mapping origins.

Short quotations for eventual registry/lesson: program-loading7.2 PT_LOAD: “[source quotation omitted in selective export; consult the cited source]” ELF-header2.1 e_phentsize: “[source quotation omitted in selective export; consult the cited source]”. These were read in rendered web text and are manually located, not claimed as machine-verified raw HTML substrings.
