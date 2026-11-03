# Primary source reading, 2026-11-03

Only owned notes and tiny quotes retained, no downloaded page copies.

## GABI 4.3 draft, chapter8, Dynamic Linking
https://gabi.xinuos.com/elf/08-dynamic.html
Read sections8.3 and8.4 through web tool. PT_DYNAMIC locates the dynamic array. Its signed tag determines integer versus virtual-address interpretation; do not derive meaning solely from tag parity because exceptions exist. DT_NULL terminates the array. DT_NEEDED indexes the DT_STRTAB address-based table; relative needed-entry order matters. DT_STRSZ provides table byte length. Names describe linked dependencies, not verification of files at runtime. Dynamic lookup behavior requires external context and is outside this static reader. Short quote: “[source quotation omitted in selective export; consult the cited source]”.

Admit: typed tag semantics, explicit termination, ordering, pointer-versus-index distinction. Reject inference: a name or successful decode establishes authentic dependency content or runtime binding. A stricter single-origin/mapping profile is local conservatism, not a universal ABI prohibition.

## GABI 4.3 draft, chapter4, String Table
https://gabi.xinuos.com/elf/04-strtab.html
Read full short chapter. Table references are byte indices; substring references and repeated occurrences are legal. Bounds and first/last NUL requirements concern the recorded table, not whatever NUL happens to occur later in the file. Offset zero denotes null/no name depending on context. Short quote: “[source quotation omitted in selective export; consult the cited source]”.

Admit: byte-index semantics and substring acceptance. Reject inference: offsets must coincide with previously discovered string starts. Raw bytes need not be silently coerced through a text codec.
