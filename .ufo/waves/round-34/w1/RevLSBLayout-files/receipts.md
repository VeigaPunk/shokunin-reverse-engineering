# RevLSBLayout evidence receipts — S103 reopen, 2026-10-23

Seat: KaidokuR34.RevLSBLayout. Freeze/sandbox rev 54a87a51a865ab931fd355e767303337b05cccf4 (verified `git rev-parse HEAD` in sandbox). Read-only reviewer: no project code executed; only read/grep/curl/sha256sum/diff/cp.

## Probes (argv, UTC, result)

1. 2026-10-23T10:5xZ `sha256sum` on sandbox captures:
   - lsb-symversion.html = 982fe1208c76eda09d8619f3907783899e4e73b19c34f3e22314fb36cc8f7f91 (= claims.json S103 row + frozen_inputs)
   - glibc-elf.h = fd6e7f3e3c74ee9d64b9f92ce3cc31b34413ca2622a167320ea053ce9a68110f (= claims.json)
   - knowledge md = d721189c…a639; approved-skill-section.txt = c156effc…2ba6; expected.json = f22e7e3b…7974d — all equal claims.json.
2. 2026-10-23T10:57:55Z `curl -sS -o lsb-live.html https://refspecs.linuxfoundation.org/LSB_5.0.0/LSB-Core-generic/LSB-Core-generic/symversion.html` → HTTP/2 200, etag "4aa5-51682c5423837", last-modified Wed, 20 May 2015 12:43:14 GMT, 19109 bytes, sha256 982fe120… identical. `diff` captured vs live: BYTE-IDENTICAL.
3. 2026-10-23T10:57:55Z `curl -sS -o glibc-live-elf.h https://raw.githubusercontent.com/bminor/glibc/d2097651cc57834dbfcaa102ddfacae0d86cfb66/elf/elf.h` → HTTP 200, 195524 bytes, sha256 fd6e7f3e… identical. `diff -q`: BYTE-IDENTICAL.
4. `grep -n` line pins, LSB capture (1196 lines): §10.7.4 heading 611-612; sh_link paragraph starts 615, sh_link token 634, sentence ends 640; DT_VERNEEDNUM 626; Verneed typedef 671-677 (fields 672-676, `}` 677); Figure 10-3 caption 683; vn_version desc quote 717; Vernaux typedef 839-845; Figure 10-4 caption 851; vna_other meaning 937; Elfxx prefix quote 102-112; `grep -c '0x'` = 0 (no hex tokens anywhere in capture).
5. `grep -n` line pins, glibc capture (4483 lines): Elf64_Half=uint16 line 28; Elf64_Word=uint32 line 33; SHT_GNU_verneed 0x6ffffffe line 459; Elf64_Verneed 1124-1133 (vn_version 1126, vn_cnt 1127, vn_file 1128-1129, vn_aux 1130, vn_next 1131-1132); VER_NEED_CURRENT 1 line 1138; Elf64_Vernaux 1153-1161 (vna_hash 1155, vna_flags 1156, vna_other /* Unused */ 1157, vna_name 1158, vna_next 1159-1160); VER_FLG_WEAK 0x2 line 1085.
6. `grep -n` instrument tools/round-34/elf-version-needs.py (read-only, NOT run): LIMITS at :75 (entries 1024, aux 4096, string 1024, section 65536, input 536870912); error names no_section_table/shnum_extended/verneed_link/strtab_offset/error.io.read/error.io.size at :136,139,156,201,218,221; EXIT_BY_CLASS = {"malformed": 12, "unsupported": 11, "io": 13} at :229.
7. Archival copies in this directory: lsb-live.html, glibc-live-elf.h (sha256 re-verified at copy time, equal to frozen).

## Quotes retained verbatim (capture line numbers)

- vn_version, lsb-symversion.html:717, 21 words: "Version of structure. This value is currently set to 1, and will be reset if the versioning implementation is incompatibly altered."
- sh_link, lsb-symversion.html:634-640 (sentence start 615): "The sh_link member of the section header (see figure 4-8 in System V ABI) shall point to the section that contains the strings referenced by this section."
- vna_other, lsb-symversion.html:937, first sentence: "Object file version identifier used in the .gnu.version symbol version array." (second sentence on hidden bit 15 follows on the same line)
- Elfxx prefix, lsb-symversion.html:102-112, 20 words: "The prefix Elfxx in the following descriptions and code fragments stands for either "Elf32" or "Elf64", depending on the architecture."
- Verneed, lsb-symversion.html:671-677: vn_version, vn_cnt, vn_file, vn_aux, vn_next (Elfxx_Half ×2 then Elfxx_Word ×3).
- Vernaux, lsb-symversion.html:839-845: vna_hash, vna_flags, vna_other, vna_name, vna_next (Elfxx_Word, Elfxx_Half, Elfxx_Half, Elfxx_Word, Elfxx_Word).
- vn_file LSB wording, lsb-symversion.html:~730: "Offset to the file name string in the section header, in bytes." (anomalous LSB prose; see report nuance)

Locator used (7 words, ≤25): "LSB 5.0.0 §10.7.4, capture lsb-symversion.html:717".

No tool was installed or upgraded (pacman pause respected; curl/sha256/diff/grep preinstalled). Answering model for this seat is not visible in-seat; no safety refusal and no transport switch occurred.
