# Kaidoku: packed relocations are still pointer evidence

The [gABI4.3 draft](https://gabi.xinuos.com/elf/06-reloc.html) distinguishes ordinary REL/RELA records from RELR tables. RELR compresses clustered relative relocations using address entries and bitmaps. Decoding produces locations whose stored values receive the load displacement; it does not recover symbol names.

This reduces metadata size, not the number of pointer locations requiring adjustment. A reader limited to REL/RELA can therefore miss evidence rather than prove that pointers need no relocation. Odd-address relocations remain outside RELR and require the older forms.

[glibc2.36 NEWS](https://github.com/bminor/glibc/blob/glibc-2.36/NEWS), released August2022, records DT_RELR support, linker prerequisites and exclusion of lazy binding. That historical milestone does not establish support in another loader, analyzer or target. Encoding support and correct artifact interpretation remain separate questions.

Selected specification and release sections read; no binaries analyzed or tools tested. The live gABI page remains labeled draft with reserved copyright. NEWS permits copying under retained notices and modified-version attribution. Original commentary and links only; no source redistribution or assimilation.
